"""Yahoo Finance 分析师预期与评级（forward-looking 数据）。

用途：老师要求分析公司「recent and forward-looking trajectory」，
预期数据（EPS/营收共识、目标价、评级分布）补上前瞻部分。
口径：第三方共识数据，报告中须标注 "Source: Yahoo Finance, retrieved <日期>"。

落盘：data/<TICKER>/yahoo_estimates.json

用法：
    .venv/Scripts/python.exe -m tools.fetch_estimates
"""
from __future__ import annotations

import json
import math
from typing import Any

import pandas as pd
import yfinance as yf

from .config import DATA_DIR, TICKERS
from .provenance import now_hkt


def _clean(v: Any) -> Any:
    """DataFrame/dict → JSON 友好结构，NaN → None。"""
    if isinstance(v, dict):
        return {str(k): _clean(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_clean(x) for x in v]
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    if hasattr(v, "isoformat"):
        return v.isoformat()
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    return str(v)


def _df_to_dict(df: pd.DataFrame | None) -> dict | None:
    if df is None or df.empty:
        return None
    return _clean(df.reset_index().to_dict(orient="records"))


def fetch(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    out: dict[str, Any] = {"ticker": ticker}

    try:
        out["price_targets"] = _clean(t.analyst_price_targets)
    except Exception as e:
        out["price_targets"] = None
        out["price_targets_error"] = f"{type(e).__name__}: {e}"

    for key, attr in [
        ("earnings_estimate", "earnings_estimate"),
        ("revenue_estimate", "revenue_estimate"),
        ("recommendations", "recommendations"),
        ("earnings_dates", "earnings_dates"),
    ]:
        try:
            out[key] = _df_to_dict(getattr(t, attr))
        except Exception as e:
            out[key] = None
            out[key + "_error"] = f"{type(e).__name__}: {e}"

    try:
        cal = t.calendar or {}
        out["calendar"] = _clean(cal)
    except Exception as e:
        out["calendar"] = None
        out["calendar_error"] = f"{type(e).__name__}: {e}"

    out.update({
        "source": "Yahoo Finance (via yfinance)",
        "source_url": f"https://finance.yahoo.com/quote/{ticker}/analysis",
        "retrieved_at": now_hkt(),
        "usage_note": "第三方共识/预期数据，不是公司披露；报告中须标注来源与日期，不可当作事实。",
    })
    return out


def main() -> None:
    for t in TICKERS:
        data = fetch(t)
        p = DATA_DIR / t / "yahoo_estimates.json"
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        pt = data.get("price_targets") or {}
        print(f"{t}: target mean={pt.get('mean')} range={pt.get('low')}~{pt.get('high')} -> {p}")


if __name__ == "__main__":
    main()
