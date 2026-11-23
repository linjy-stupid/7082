"""风险与绩效指标：全部由价格序列确定性计算（无 LLM 参与）。

指标：
  - 年化波动率（日收益标准差 × √252）
  - beta（vs SPY，日收益协方差/方差）
  - 最大回撤（MDD）
  - VaR 95%（历史法，日收益 5% 分位）
  - CVaR 95%（VaR 以下日收益均值）
  - 近一年回报
"""
from __future__ import annotations

import math

import numpy as np

from .prices import download_prices, load_prices


def compute_risk(ticker: str, benchmark: str = "SPY", window: int = 252) -> dict:
    download_prices(ticker)
    download_prices(benchmark)
    df = load_prices(ticker)
    bm = load_prices(benchmark)

    rets = df["Close"].pct_change().dropna()
    bm_rets = bm["Close"].pct_change().dropna()

    joined = np.log1p(rets).to_frame("r").join(
        np.log1p(bm_rets).to_frame("b"), how="inner"
    )
    r = joined["r"].to_numpy()
    b = joined["b"].to_numpy()

    vol_ann = float(np.std(r, ddof=1) * math.sqrt(252) * 100.0)
    beta = float(np.cov(r, b, ddof=1)[0, 1] / np.var(b, ddof=1))

    cum = np.cumprod(1.0 + r)
    peak = np.maximum.accumulate(cum)
    mdd = float((cum / peak - 1.0).min() * 100.0)

    var95 = float(np.percentile(r, 5) * 100.0)
    tail = r[r <= np.percentile(r, 5)]
    cvar95 = float(tail.mean() * 100.0) if len(tail) else None

    closes = df["Close"].to_numpy()
    ret_1y = (
        float((closes[-1] / closes[-window] - 1.0) * 100.0)
        if len(closes) > window else None
    )

    return {
        "vol_ann_pct": round(vol_ann, 2),
        "beta_vs_benchmark": round(beta, 3),
        "mdd_pct": round(mdd, 2),
        "var95_daily_pct": round(var95, 2),
        "cvar95_daily_pct": round(cvar95, 2) if cvar95 is not None else None,
        "ret_1y_pct": round(ret_1y, 2) if ret_1y is not None else None,
        "n_days": int(len(r)),
        "benchmark": benchmark,
        "window": window,
        "last_date": str(df.index[-1].date()),
    }
