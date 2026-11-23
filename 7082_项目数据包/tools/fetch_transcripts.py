"""Earnings-call transcript 抓取（老师要求的数据源之一）。

来源：StockAnalysis 的公开电话会全文页（转录由 Quartr 提供），无需登录、无付费墙。
仅抓取公开页面，遵守 robots.txt 与合理频率（每请求间隔 1.2 s）。

落盘：
  data/<TICKER>/transcripts/<period>.json   结构化（说话人分段）
  data/<TICKER>/transcripts/<period>.txt    可读全文（可直接喂给 LLM）
  data/<TICKER>/transcripts/<period>.meta.json  来源/URL/抓取时间/sha256

用法：
    .venv/Scripts/python.exe -m tools.fetch_transcripts          # 每家公司最近 2 季
    .venv/Scripts/python.exe -m tools.fetch_transcripts --n 4    # 最近 4 季
"""
from __future__ import annotations

import argparse
import json
import re
import time
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from .config import DATA_DIR, TICKERS
from .provenance import now_hkt, sha256_text

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36 7082-course-research"
)
SLUG = {"NVDA": "nvda", "MSFT": "msft", "PLTR": "pltr"}
BASE = "https://stockanalysis.com/stocks/{slug}/transcripts/"
MIN_INTERVAL = 1.2
_DATE = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? (\d{1,2}), (20\d\d)")


def _get(url: str, retries: int = 3) -> str:
    last = None
    for i in range(retries):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            if r.status_code == 200:
                return r.text
            last = f"HTTP {r.status_code}"
        except Exception as e:  # 网络类错误
            last = f"{type(e).__name__}: {e}"
        time.sleep(MIN_INTERVAL * (i + 1))
    raise RuntimeError(f"抓取失败 {url}: {last}")


def list_quarters(ticker: str) -> list[dict]:
    """列出财报电话会季度（过滤掉会议/投资者日等非财报条目）。"""
    html = _get(BASE.format(slug=SLUG[ticker]))
    slug = SLUG[ticker]
    pat = re.compile(rf"/stocks/{slug}/transcripts/(\d+)-q(\d)-(20\d\d)/?")
    seen: dict[str, dict] = {}
    for m in pat.finditer(html):
        tid, q, y = m.group(1), int(m.group(2)), int(m.group(3))
        url = f"https://stockanalysis.com/stocks/{slug}/transcripts/{tid}-q{q}-{y}/"
        seen.setdefault(url, {"url": url, "quarter": q, "year": y, "id": tid})
    items = sorted(seen.values(), key=lambda x: (x["year"], x["quarter"]), reverse=True)
    return items


def parse_transcript(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    title = None
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(s.string or "")
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and d.get("@type") == "WebPage" and d.get("name"):
            title = d["name"]
            break
    if not title:
        h1 = soup.find("h1")
        title = h1.get_text(" ", strip=True) if h1 else ""

    panel = soup.find(id="transcript-panel-full")
    if not panel:
        raise RuntimeError("页面无 transcript 面板（可能被付费墙或改版）")
    art = panel.find(attrs={"role": "article"})
    if not art:
        raise RuntimeError("页面无 transcript 正文")

    sections: list[dict] = []
    for block in art.find_all("div", recursive=False):
        spk = block.find(
            "div", class_=lambda c: c and "font-bold" in c and "text-lg" in c
        )
        speaker = spk.get_text(" ", strip=True) if spk else None
        text = " ".join(
            p.get_text(" ", strip=True) for p in block.find_all("p")
        ).strip()
        if not text:
            continue
        sections.append({"speaker": speaker or "Unknown", "text": text})

    summary = None
    for p in soup.find_all("p", class_=lambda c: c and "leading-relaxed" in c):
        t = p.get_text(" ", strip=True)
        if t and "transcripts are provided" not in t:
            summary = t
            break

    # 页面固定格式："Earnings Call: Q3 2027 Nov 17, 2026"
    body = soup.get_text(" ", strip=True)
    m = re.search(
        r"Earnings Call:\s*Q\d+\s+\d{4}\s+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\.?\s+\d{1,2},\s+20\d\d)",
        body,
    ) or re.search(r"Last updated:\s*((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                    r"[a-z]*\.?\s+\d{1,2},\s+20\d\d)", body)
    call_date = None
    if m:
        try:
            call_date = datetime.strptime(
                re.sub(r"\s+", " ", m.group(1)), "%b %d, %Y"
            ).date().isoformat()
        except ValueError:
            call_date = None

    return {
        "title": title,
        "summary": summary,
        "call_date": call_date,
        "sections": sections,
    }


def _period_label(quarter: int, year: int) -> str:
    return f"Q{quarter} {year}"


def fetch_one(ticker: str, item: dict) -> Path:
    q, y = item["quarter"], item["year"]
    period = _period_label(q, y)
    html = _get(item["url"])
    time.sleep(MIN_INTERVAL)
    data = parse_transcript(html)

    out_dir = DATA_DIR / ticker / "transcripts"
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{period.replace(' ', '')}"

    txt_lines = [
        data["title"] or f"{ticker} {period} Earnings Call Transcript",
        f"Source: StockAnalysis (transcripts provided by Quartr), retrieved {now_hkt()}",
        f"URL: {item['url']}",
        f"Company: {ticker}   Period: {period}   Call date: {data['call_date'] or 'n/a'}",
    ]
    if data["summary"]:
        txt_lines += ["", "Summary:", data["summary"]]
    txt_lines.append("")
    for s in data["sections"]:
        txt_lines += ["=" * 60, s["speaker"], s["text"], ""]
    txt = "\n".join(txt_lines)

    payload = {
        "ticker": ticker,
        "period": period,
        "title": data["title"],
        "summary": data["summary"],
        "call_date": data["call_date"],
        "source": "StockAnalysis (transcripts provided by Quartr)",
        "source_url": item["url"],
        "retrieved_at": now_hkt(),
        "n_sections": len(data["sections"]),
        "n_chars": len(txt),
        "sha256": sha256_text(txt),
        "sections": data["sections"],
    }
    (out_dir / f"{stem}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (out_dir / f"{stem}.txt").write_text(txt, encoding="utf-8")
    (out_dir / f"{stem}.meta.json").write_text(
        json.dumps(
            {k: payload[k] for k in ("ticker", "period", "call_date", "source",
                                     "source_url", "retrieved_at", "n_sections",
                                     "n_chars", "sha256")},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"{ticker} {period}: {len(data['sections'])} 段, {len(txt):,} 字符 -> {out_dir / stem}")
    return out_dir / f"{stem}.txt"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=2, help="每家公司抓最近 N 季")
    ap.add_argument("--tickers", nargs="*", default=TICKERS)
    args = ap.parse_args()

    for t in args.tickers:
        items = list_quarters(t)[: args.n]
        print(f"{t}: 找到 {len(items)} 个目标季度 {[f'Q{i['quarter']} {i['year']}' for i in items]}")
        for it in items:
            fetch_one(t, it)


if __name__ == "__main__":
    main()
