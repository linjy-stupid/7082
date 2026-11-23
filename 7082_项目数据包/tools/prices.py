"""股价与成交量：Yahoo Finance（经 yfinance）。

注意：Yahoo 是市场数据聚合源，不是 SEC 官方文件。
报告中引用股价时必须标注 "Source: Yahoo Finance" 与抓取时间。
"""
from __future__ import annotations

import json
from pathlib import Path

import yfinance as yf

from .config import DATA_DIR
from .provenance import now_hkt, sha256_file


def _dir(ticker: str) -> Path:
    d = DATA_DIR / ticker
    d.mkdir(parents=True, exist_ok=True)
    return d


def download_prices(
    ticker: str,
    period: str = "3y",
    interval: str = "1d",
    force: bool = False,
) -> Path:
    p = _dir(ticker) / f"prices_{interval}.csv"
    if p.exists() and not force:
        return p

    df = yf.Ticker(ticker).history(
        period=period, interval=interval, auto_adjust=False, actions=False
    )
    if df.empty:
        raise RuntimeError(f"{ticker}: Yahoo Finance 返回空数据（可能被限流，稍后重试）")

    df.index.name = "Date"
    df.to_csv(p, encoding="utf-8")
    (p.parent / f"prices_{interval}.meta.json").write_text(
        json.dumps({
            "ticker": ticker,
            "source": "Yahoo Finance (via yfinance)",
            "source_url": f"https://finance.yahoo.com/quote/{ticker}/history",
            "retrieved_at": now_hkt(),
            "interval": interval,
            "requested_period": period,
            "rows": int(len(df)),
            "first_date": str(df.index[0]),
            "last_date": str(df.index[-1]),
            "sha256": sha256_file(p),
            "note": "市场数据，非 SEC 官方；auto_adjust=False，保留原始 OHLC",
        }, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return p


def load_prices(ticker: str, interval: str = "1d"):
    import pandas as pd

    p = download_prices(ticker, interval=interval)
    df = pd.read_csv(p, index_col=0)
    # pandas 3.x 下 parse_dates=True 对 index_col 不再生效，显式转换
    df.index = pd.to_datetime(df.index, utc=True)
    return df


def price_summary(ticker: str) -> dict:
    """返回可写入 registry 的行情摘要（含来源与抓取时间）。"""
    df = load_prices(ticker)
    last = df.iloc[-1]
    meta = json.loads(
        (DATA_DIR / ticker / "prices_1d.meta.json").read_text(encoding="utf-8")
    )
    closes = df["Close"]
    return {
        "ticker": ticker,
        "last_date": str(df.index[-1].date()),
        "close": float(last["Close"]),
        "volume": int(last["Volume"]),
        "high_52w": float(closes.tail(252).max()),
        "low_52w": float(closes.tail(252).min()),
        "ret_1y_pct": round(
            100.0 * (float(closes.iloc[-1]) / float(closes.iloc[-252]) - 1.0), 2
        ) if len(closes) > 252 else None,
        "source": meta["source"],
        "source_url": meta["source_url"],
        "retrieved_at": meta["retrieved_at"],
        "sha256": meta["sha256"],
    }
