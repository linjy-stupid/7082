"""SEC EDGAR 官方数据访问层。

数据来源全部为 SEC 官方公开接口：
  - XBRL companyfacts: https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json
  - submissions:       https://data.sec.gov/submissions/CIK##########.json
  - 原始文件:          https://www.sec.gov/Archives/edgar/data/...

所有下载落盘 data/<TICKER>/，并写 .meta.json 记录 URL、抓取时间、SHA256。
"""
from __future__ import annotations

import json
import time
from datetime import date
from pathlib import Path

import requests

from .config import CIK, DATA_DIR, SEC_MIN_INTERVAL, SEC_UA
from .provenance import now_hkt, sha256_file

_session = requests.Session()
_session.headers.update({"User-Agent": SEC_UA, "Accept-Encoding": "gzip, deflate"})
_last_request = 0.0


def _get(url: str, retries: int = 3) -> bytes:
    """带限速与重试的 GET；403 视为 UA 不合规直接报错。"""
    global _last_request
    for attempt in range(retries):
        wait = SEC_MIN_INTERVAL - (time.time() - _last_request)
        if wait > 0:
            time.sleep(wait)
        _last_request = time.time()
        try:
            r = _session.get(url, timeout=30)
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
            continue
        if r.status_code == 403:
            raise RuntimeError(
                "SEC 返回 403：User-Agent 不合规。请设置环境变量 "
                "SEC_UA='你的姓名 你的邮箱' 后重试。"
            )
        if r.status_code >= 500 and attempt < retries - 1:
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        return r.content
    raise RuntimeError("unreachable")


def _ticker_dir(ticker: str) -> Path:
    d = DATA_DIR / ticker
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write_meta(path: Path, meta: dict) -> None:
    (path.parent / f"{path.stem}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------- companyfacts

def download_companyfacts(ticker: str, force: bool = False) -> Path:
    p = _ticker_dir(ticker) / "companyfacts.json"
    if p.exists() and not force:
        return p
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK[ticker]}.json"
    content = _get(url)
    p.write_bytes(content)
    _write_meta(p, {
        "ticker": ticker,
        "source": "SEC EDGAR XBRL companyfacts (official)",
        "source_url": url,
        "retrieved_at": now_hkt(),
        "bytes": len(content),
        "sha256": sha256_file(p),
    })
    return p


def load_companyfacts(ticker: str) -> dict:
    p = download_companyfacts(ticker)
    return json.loads(p.read_text(encoding="utf-8"))


def _duration_days(item: dict) -> int | None:
    if "start" not in item:
        return None
    return (date.fromisoformat(item["end"]) - date.fromisoformat(item["start"])).days


def get_series(
    ticker: str,
    tag: str,
    unit: str = "USD",
    kind: str = "annual",
    forms: tuple[str, ...] = ("10-K", "10-Q"),
) -> list[dict]:
    """从 companyfacts 提取某个 us-gaap 标签的时间序列。

    kind:
      annual    - 期间长度 350~380 天（年报口径）
      quarterly - 期间长度 70~110 天（单季口径）
      instant   - 无 start 的时点值（资产/负债等资产负债表项目）
    """
    facts = load_companyfacts(ticker)
    node = facts.get("facts", {}).get("us-gaap", {}).get(tag)
    if not node:
        return []
    items = node.get("units", {}).get(unit, [])
    picked: list[dict] = []
    for it in items:
        if it.get("form") not in forms:
            continue
        d = _duration_days(it)
        if kind == "annual" and (d is None or not 350 <= d <= 380):
            continue
        if kind == "quarterly" and (d is None or not 70 <= d <= 110):
            continue
        if kind == "instant" and d is not None:
            continue
        picked.append(it)
    # 同一 period_end 只保留最新提交的版本（更正后的数据优先）
    best: dict[str, dict] = {}
    for it in picked:
        key = it["end"]
        if key not in best or it.get("filed", "") > best[key].get("filed", ""):
            best[key] = it
    return sorted(best.values(), key=lambda x: x["end"])


def get_ytd_series(
    ticker: str,
    tag: str,
    unit: str = "USD",
    forms: tuple[str, ...] = ("10-K", "10-Q"),
) -> list[dict]:
    """提取 YTD（年初至今）序列：期间 70~300 天，含 10-Q 的 3/6/9 个月与 10-K 的年度值。

    现金流量表在 10-Q 中通常只报 YTD，不能直接当单季值用，
    必须用 ytd_to_quarters() 差分。
    """
    facts = load_companyfacts(ticker)
    node = facts.get("facts", {}).get("us-gaap", {}).get(tag)
    if not node:
        return []
    items = node.get("units", {}).get(unit, [])
    picked = []
    for it in items:
        if it.get("form") not in forms:
            continue
        d = _duration_days(it)
        if d is None or not 70 <= d <= 380:
            continue
        picked.append(it)
    best: dict[tuple, dict] = {}
    for it in picked:
        k = (it.get("start"), it["end"])
        if k not in best or it.get("filed", "") > best[k].get("filed", ""):
            best[k] = it
    return sorted(best.values(), key=lambda x: x["end"])


def ytd_to_quarters(items: list[dict]) -> list[dict]:
    """同一财年（start 相同）内按 end 排序，逐期相减得到单季值。

    Q1 = YTD(3m)；Q2 = YTD(6m) - YTD(3m)；Q3 = YTD(9m) - YTD(6m)；Q4 = FY - YTD(9m)。
    """
    from collections import defaultdict

    groups: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        groups[it.get("start")].append(it)
    out: list[dict] = []
    for start, group in groups.items():
        group.sort(key=lambda x: x["end"])
        prev_val = 0.0
        prev_end = None
        for it in group:
            out.append({
                **it,
                "val": it["val"] - prev_val,
                "q_start": prev_end or it.get("start"),
            })
            prev_val = it["val"]
            prev_end = it["end"]
    return sorted(out, key=lambda x: x["end"])


def pick_tag(
    ticker: str,
    candidates: list[str],
    unit: str = "USD",
    kind: str = "annual",
    forms: tuple[str, ...] = ("10-K", "10-Q"),
) -> tuple[str | None, list[dict]]:
    """在多个候选 tag 中选数据最新的那个。

    不能简单取"第一个有数据的 tag"：公司会换标签
    （NVDA 的 RevenueFromContractWithCustomerExcludingAssessedTax 只到 FY2022，
    之后改用 Revenues）。这里按最新 period_end 比较，并列时取期数多的。
    """
    best_tag, best_series = None, []
    for tag in candidates:
        series = get_series(ticker, tag, unit=unit, kind=kind, forms=forms)
        if not series:
            continue
        if (
            not best_series
            or series[-1]["end"] > best_series[-1]["end"]
            or (
                series[-1]["end"] == best_series[-1]["end"]
                and len(series) > len(best_series)
            )
        ):
            best_tag, best_series = tag, series
    return best_tag, best_series


# ------------------------------------------------------------------- filings

def download_submissions(ticker: str, force: bool = False) -> Path:
    p = _ticker_dir(ticker) / "submissions.json"
    if p.exists() and not force:
        return p
    url = f"https://data.sec.gov/submissions/CIK{CIK[ticker]}.json"
    content = _get(url)
    p.write_bytes(content)
    _write_meta(p, {
        "ticker": ticker,
        "source": "SEC EDGAR submissions (official)",
        "source_url": url,
        "retrieved_at": now_hkt(),
        "bytes": len(content),
        "sha256": sha256_file(p),
    })
    return p


def latest_filings(ticker: str, form: str = "10-K", n: int = 2) -> list[dict]:
    """返回最近 n 份指定类型的 SEC 文件（按提交日倒序）。"""
    download_submissions(ticker)
    p = DATA_DIR / ticker / "submissions.json"
    subs = json.loads(p.read_text(encoding="utf-8"))
    rec = subs["filings"]["recent"]
    out: list[dict] = []
    for i, f in enumerate(rec["form"]):
        if f != form:
            continue
        out.append({
            "ticker": ticker,
            "form": f,
            "accession": rec["accessionNumber"][i],
            "primary_doc": rec["primaryDocument"][i],
            "filing_date": rec["filingDate"][i],
            "report_date": rec["reportDate"][i],
            "items": rec.get("items", [""] * len(rec["form"]))[i],
        })
        if len(out) >= n:
            break
    return out


def _html_to_text(html: str) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    lines = (line.strip() for line in soup.get_text("\n").splitlines())
    return "\n".join(line for line in lines if line)


def download_8k_exhibit(
    ticker: str,
    accession: str,
    primary_doc: str | None = None,
    force: bool = False,
) -> Path | None:
    """下载 8-K 的 earnings press release（exhibit 99.x 或公司自定义命名）。

    NVDA 等公司不用 "99" 命名（q2fy27pr.htm / q2fy27cfocommentary.htm），
    因此按关键词回退匹配。
    """
    cik = CIK[ticker].lstrip("0")
    acc = accession.replace("-", "")
    out_dir = _ticker_dir(ticker) / "filings"
    out_dir.mkdir(exist_ok=True)
    idx_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/index.json"
    idx = json.loads(_get(idx_url).decode("utf-8"))
    items = idx["directory"]["item"]
    cand = [
        it for it in items
        if it["name"].lower().endswith((".htm", ".html"))
        and not it["name"].lower().startswith("r")
        and "index" not in it["name"].lower()
        and (primary_doc is None or it["name"] != primary_doc)
    ]
    ex = [it for it in cand if "99" in it["name"].lower()]
    if not ex:
        ex = [
            it for it in cand
            if any(k in it["name"].lower()
                   for k in ("press", "pr.", "release", "commentary"))
        ]
    if not ex:
        ex = cand
    if not ex:
        return None
    ex.sort(key=lambda x: x.get("size", 0), reverse=True)
    name = ex[0]["name"]
    out = out_dir / f"{accession}_8k_{name}.txt"
    if out.exists() and not force:
        return out
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{name}"
    text = _html_to_text(_get(url).decode("utf-8", errors="ignore"))
    out.write_text(text, encoding="utf-8")
    _write_meta(out, {
        "ticker": ticker,
        "source": "SEC EDGAR 8-K exhibit (official)",
        "source_url": url,
        "form": "8-K",
        "accession": accession,
        "retrieved_at": now_hkt(),
        "chars": len(text),
        "sha256": sha256_file(out),
    })
    return out


def download_filing_text(
    ticker: str,
    accession: str,
    primary_doc: str | None = None,
    form: str = "10-K",
    force: bool = False,
) -> Path:
    """下载 10-K/10-Q 主文档并转纯文本，落盘 data/<TICKER>/filings/。"""
    cik = CIK[ticker].lstrip("0")
    acc_nodash = accession.replace("-", "")
    out_dir = _ticker_dir(ticker) / "filings"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{accession}_{primary_doc or 'main'}.txt"
    if out.exists() and not force:
        return out

    if primary_doc is None:
        idx_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/index.json"
        idx = json.loads(_get(idx_url).decode("utf-8"))
        cand = [
            it for it in idx["directory"]["item"]
            if it["name"].lower().endswith((".htm", ".html"))
            and not it["name"].lower().startswith("r")
        ]
        cand.sort(key=lambda x: x.get("size", 0), reverse=True)
        if not cand:
            raise RuntimeError(f"{ticker} {accession}: 找不到 HTML 主文档")
        primary_doc = cand[0]["name"]

    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_nodash}/{primary_doc}"
    text = _html_to_text(_get(url).decode("utf-8", errors="ignore"))
    out.write_text(text, encoding="utf-8")
    _write_meta(out, {
        "ticker": ticker,
        "source": "SEC EDGAR filing (official)",
        "source_url": url,
        "form": form,
        "accession": accession,
        "retrieved_at": now_hkt(),
        "chars": len(text),
        "sha256": sha256_file(out),
    })
    return out
