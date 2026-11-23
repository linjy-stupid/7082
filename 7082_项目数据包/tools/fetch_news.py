"""抓取 Yahoo Finance 新闻（标题/来源/时间/链接/摘要）。

新闻属于辅助数据：报告中引用必须标注媒体名与日期，不得当作事实性财务数据。

用法：
    .venv/Scripts/python.exe -m tools.fetch_news
"""
from __future__ import annotations

import json

import yfinance as yf

from .config import DATA_DIR, TICKERS
from .provenance import now_hkt


def fetch_news(ticker: str, n: int = 10) -> list[dict]:
    raw = yf.Ticker(ticker).news or []
    out: list[dict] = []
    for item in raw[:n]:
        c = item.get("content", item)
        out.append({
            "title": c.get("title"),
            "publisher": ((c.get("provider") or {}).get("displayName")),
            "published": c.get("pubDate"),
            "link": ((c.get("canonicalUrl") or {}).get("url")),
            "summary": c.get("summary"),
        })
    return out


def main() -> None:
    for t in TICKERS:
        items = fetch_news(t)
        payload = {
            "ticker": t,
            "source": "Yahoo Finance news (via yfinance)",
            "source_url": f"https://finance.yahoo.com/quote/{t}/news",
            "retrieved_at": now_hkt(),
            "note": "新闻为辅助信息，引用需标注媒体与日期",
            "n_items": len(items),
            "items": items,
        }
        p = DATA_DIR / t / "news.json"
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{t}: {len(items)} 条 -> {p}")
        for it in items[:2]:
            print(f"  - [{it['publisher']}] {it['title']}")


if __name__ == "__main__":
    main()
