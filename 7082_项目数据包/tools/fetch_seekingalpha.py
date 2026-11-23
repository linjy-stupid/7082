"""Seeking Alpha 公开 RSS 抓取（老师要求的数据源之一）。

边界（合规）：
  - 只抓 SA 官方公开 RSS：https://seekingalpha.com/symbol/<T>/feed.xml
  - 不绕过付费墙、不模拟登录、不请求 /api 内部接口
  - RSS 版权声明限定「personal, non-commercial use」——课程作业属此范围；
    本项目只保存标题/作者/日期/链接等元数据，不转载正文。

落盘：data/<TICKER>/seekingalpha.json

用法：
    .venv/Scripts/python.exe -m tools.fetch_seekingalpha
"""
from __future__ import annotations

import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from .config import DATA_DIR, TICKERS
from .provenance import now_hkt

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36 7082-course-research"
)
FEED = "https://seekingalpha.com/symbol/{ticker}/feed.xml"
MIN_INTERVAL = 1.0


def _get(url: str, retries: int = 3) -> str:
    last = None
    for i in range(retries):
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
            if r.status_code == 200:
                return r.text
            last = f"HTTP {r.status_code}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        time.sleep(MIN_INTERVAL * (i + 1))
    raise RuntimeError(f"抓取失败 {url}: {last}")


def _parse_date(raw: str | None) -> str | None:
    if not raw:
        return None
    try:
        return datetime.strptime(raw, "%a, %d %b %Y %H:%M:%S %z").isoformat()
    except ValueError:
        return raw


def fetch(ticker: str) -> list[dict]:
    root = ET.fromstring(_get(FEED.format(ticker=ticker)))
    items = []
    for it in root.findall("./channel/item"):
        authors, symbols = [], []
        for c in it.findall("category"):
            if c.get("type") == "author":
                authors.append(c.text or "")
            elif c.get("type") == "symbol":
                symbols.append(c.text or "")
        items.append({
            "title": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "published": _parse_date(it.findtext("pubDate")),
            "guid": it.findtext("guid"),
            "authors": authors,
            "symbols": symbols,
            "is_primary": ticker in symbols,
        })
    return items


def main() -> None:
    for t in TICKERS:
        items = fetch(t)
        payload = {
            "ticker": t,
            "source": "Seeking Alpha public RSS feed",
            "source_url": FEED.format(ticker=t),
            "retrieved_at": now_hkt(),
            "usage_note": (
                "RSS 版权声明限定 personal, non-commercial use；本文件只保存"
                "标题/作者/日期/链接元数据，不转载正文。正文需订阅，未获取。"
            ),
            "n_items": len(items),
            "items": items,
        }
        p = DATA_DIR / t / "seekingalpha.json"
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{t}: {len(items)} 条 -> {p}")
        for it in items[:3]:
            print(f"  - [{it['published'][:10] if it['published'] else '?'}] {it['title'][:80]}")
        time.sleep(MIN_INTERVAL)


if __name__ == "__main__":
    main()
