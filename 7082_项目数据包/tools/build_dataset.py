"""一键抓取三家公司的官方数据并写入 Fact 台账。

用法（在 project 目录下）：
    .venv/Scripts/python.exe -m tools.build_dataset

数据流：
    SEC companyfacts (XBRL) ──> data/<TICKER>/companyfacts.json
    SEC submissions          ──> data/<TICKER>/submissions.json
    Yahoo Finance (yfinance) ──> data/<TICKER>/prices_1d.csv
                                ──> data/<TICKER>/registry.json（全部 Fact）
"""
from __future__ import annotations

import json
from datetime import date, timedelta

from . import sec
from .calc import pct, yoy
from .config import CIK, DATA_DIR, TICKERS
from .prices import download_prices, price_summary
from .provenance import Fact, now_hkt
from .registry import Registry
from .risk import compute_risk

REVENUE_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "SalesRevenueNet",
]
NET_INCOME_TAGS = ["NetIncomeLoss", "ProfitLoss"]
OP_INCOME_TAGS = ["OperatingIncomeLoss"]
GROSS_PROFIT_TAGS = ["GrossProfit"]
ASSET_TAGS = ["Assets"]
EQUITY_TAGS = [
    "StockholdersEquity",
    "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
]
CFO_TAGS = ["NetCashProvidedByUsedInOperatingActivities"]
EPS_TAGS = ["EarningsPerShareDiluted"]
CAPEX_TAGS = [
    "PaymentsToAcquirePropertyPlantAndEquipment",
    "PaymentsToAcquireProductiveAssets",
    "PaymentsForCapitalImprovements",
    "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities",
]


def _retrieved_at(ticker: str) -> str:
    meta = json.loads(
        (DATA_DIR / ticker / "companyfacts.meta.json").read_text(encoding="utf-8")
    )
    return meta["retrieved_at"]


def _url(ticker: str) -> str:
    return f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK[ticker]}.json"


def _add_series(
    reg: Registry,
    ticker: str,
    name: str,
    tags: list[str],
    unit: str = "USD",
    kind: str = "annual",
    forms: tuple[str, ...] = ("10-K", "10-Q"),
    n: int = 5,
) -> list[Fact]:
    tag, series = sec.pick_tag(ticker, tags, unit=unit, kind=kind, forms=forms)
    if not series:
        print(f"  [warn] {ticker}.{name}: 未找到任何 tag {tags}")
        return []
    retrieved = _retrieved_at(ticker)
    out: list[Fact] = []
    for it in series[-n:]:
        fact = Fact(
            key=f"{ticker}.{name}.{it['end']}",
            value=it["val"],
            unit=unit,
            source=f"SEC EDGAR XBRL — {tag}",
            source_url=_url(ticker),
            retrieved_at=retrieved,
            form=it.get("form"),
            accession=it.get("accn"),
            period_start=it.get("start"),
            period_end=it["end"],
            fy=it.get("fy"),
            fp=it.get("fp"),
            filed=it.get("filed"),
            note=f"tag={tag}",
        )
        reg.add(fact)
        out.append(fact)
    print(f"  {ticker}.{name}: {len(out)} 期（{tag}，{out[0].period_end} → {out[-1].period_end}）")
    return out


def _match_prev_year(facts: list[Fact], end_str: str, tol: int = 25) -> Fact | None:
    """找一年前同季度的 Fact（季度 end 日期因 53 周财年会漂移几天）。"""
    target = date.fromisoformat(end_str) - timedelta(days=365)
    best = None
    for f in facts:
        if not f.period_end:
            continue
        d = abs((date.fromisoformat(f.period_end) - target).days)
        if d <= tol and (best is None or d < best[0]):
            best = (d, f)
    return best[1] if best else None


def _add_quarterly(
    reg: Registry,
    ticker: str,
    name: str,
    tags: list[str],
    unit: str = "USD",
    n_out: int = 8,
    n_fetch: int = 13,
) -> list[Fact]:
    """最近季度值入账，并为最近 n_out 个季度计算同比。"""
    tag, series = sec.pick_tag(ticker, tags, unit=unit, kind="quarterly")
    if not series:
        print(f"  [warn] {ticker}.{name}: 无季度数据")
        return []
    retrieved = _retrieved_at(ticker)
    facts: list[Fact] = []
    for it in series[-n_fetch:]:
        fact = Fact(
            key=f"{ticker}.{name}.{it['end']}",
            value=it["val"],
            unit=unit,
            source=f"SEC EDGAR XBRL — {tag}",
            source_url=_url(ticker),
            retrieved_at=retrieved,
            form=it.get("form"),
            accession=it.get("accn"),
            period_start=it.get("start"),
            period_end=it["end"],
            fy=it.get("fy"),
            fp=it.get("fp"),
            filed=it.get("filed"),
            note=f"tag={tag}",
        )
        reg.add(fact)
        facts.append(fact)
    for cur in facts[-n_out:]:
        prev = _match_prev_year(facts, cur.period_end)
        if not prev:
            continue
        val = yoy(cur.value, prev.value)
        if val is None:
            continue
        reg.add_derived(
            f"{ticker}.{name}_yoy.{cur.period_end}",
            val,
            "ratio_pct",
            [cur.key, prev.key],
            note=f"季度同比：{cur.period_end} vs {prev.period_end}",
            retrieved_at=retrieved,
        )
    print(f"  {ticker}.{name}: {len(facts)} 季（{facts[0].period_end} → {facts[-1].period_end}）")
    return facts


def _add_quarterly_ytd(
    reg: Registry,
    ticker: str,
    name: str,
    tags: list[str],
    unit: str = "USD",
    n_out: int = 8,
) -> list[Fact]:
    """季度现金流：10-Q 只报 YTD，用差分还原单季。"""
    tag = None
    series: list[dict] = []
    for t in tags:
        raw = sec.get_ytd_series(ticker, t, unit=unit)
        if raw:
            series = sec.ytd_to_quarters(raw)
            tag = t
            break
    if not series:
        print(f"  [warn] {ticker}.{name}: 无 YTD 数据")
        return []
    # 只保留真正的单季（80~100 天）
    series = [s for s in series if 80 <= _days(s.get("q_start"), s["end"]) <= 100]
    retrieved = _retrieved_at(ticker)
    facts: list[Fact] = []
    for it in series[-14:]:
        fact = Fact(
            key=f"{ticker}.{name}.{it['end']}",
            value=it["val"],
            unit=unit,
            source=f"SEC EDGAR XBRL — {tag}（YTD 差分）",
            source_url=_url(ticker),
            retrieved_at=retrieved,
            form=it.get("form"),
            accession=it.get("accn"),
            period_start=it.get("q_start"),
            period_end=it["end"],
            fy=it.get("fy"),
            fp=it.get("fp"),
            filed=it.get("filed"),
            note=f"tag={tag}; 单季值 = 当期 YTD − 上期 YTD",
        )
        reg.add(fact)
        facts.append(fact)
    for cur in facts[-n_out:]:
        prev = _match_prev_year(facts, cur.period_end)
        if not prev:
            continue
        val = yoy(cur.value, prev.value)
        if val is not None:
            reg.add_derived(
                f"{ticker}.{name}_yoy.{cur.period_end}",
                val, "ratio_pct", [cur.key, prev.key],
                note=f"季度同比：{cur.period_end} vs {prev.period_end}",
                retrieved_at=retrieved,
            )
    print(f"  {ticker}.{name}: {len(facts)} 季（YTD 差分，{facts[0].period_end} → {facts[-1].period_end}）")
    return facts


def _days(start: str | None, end: str) -> int:
    if not start:
        return 0
    return (date.fromisoformat(end) - date.fromisoformat(start)).days


def build_ticker(ticker: str, rebuild: bool = True) -> Registry:
    print(f"\n=== {ticker} ===")
    sec.download_companyfacts(ticker)
    sec.download_submissions(ticker)
    download_prices(ticker)
    reg = Registry(ticker)
    if rebuild:
        # 数据集构建器语义：每次从零重建，避免旧的错误 Fact 残留
        reg.facts = {}

    revenue = _add_series(reg, ticker, "revenue", REVENUE_TAGS)
    net_income = _add_series(reg, ticker, "net_income", NET_INCOME_TAGS)
    op_income = _add_series(reg, ticker, "operating_income", OP_INCOME_TAGS)
    gross_profit = _add_series(reg, ticker, "gross_profit", GROSS_PROFIT_TAGS)
    cfo = _add_series(reg, ticker, "cfo", CFO_TAGS)
    capex = _add_series(reg, ticker, "capex", CAPEX_TAGS)
    eps = _add_series(reg, ticker, "eps_diluted", EPS_TAGS, unit="USD/shares")
    assets = _add_series(
        reg, ticker, "assets", ASSET_TAGS, kind="instant", forms=("10-K",), n=3
    )
    equity = _add_series(
        reg, ticker, "equity", EQUITY_TAGS, kind="instant", forms=("10-K",), n=4
    )

    # ---- 派生指标（全部由 calc.py 计算，inputs 可递归溯源）
    retrieved = _retrieved_at(ticker)
    if len(revenue) >= 2:
        cur, prev = revenue[-1], revenue[-2]
        val = yoy(cur.value, prev.value)
        if val is not None:
            reg.add_derived(
                f"{ticker}.revenue_yoy.{cur.period_end}",
                val, "ratio_pct", [cur.key, prev.key],
                note="营收同比增速", retrieved_at=retrieved,
            )
            print(f"  {ticker}.revenue_yoy: {val:.2f}%")
    if revenue and gross_profit:
        cur_r = revenue[-1]
        gp = next((g for g in reversed(gross_profit) if g.period_end == cur_r.period_end), None)
        if gp:
            val = pct(gp.value, cur_r.value)
            if val is not None:
                reg.add_derived(
                    f"{ticker}.gross_margin.{cur_r.period_end}",
                    val, "ratio_pct", [gp.key, cur_r.key],
                    note="毛利率 = 毛利/营收", retrieved_at=retrieved,
                )
                print(f"  {ticker}.gross_margin: {val:.2f}%")
    if revenue and net_income:
        cur_r = revenue[-1]
        ni = next((x for x in reversed(net_income) if x.period_end == cur_r.period_end), None)
        if ni:
            val = pct(ni.value, cur_r.value)
            if val is not None:
                reg.add_derived(
                    f"{ticker}.net_margin.{cur_r.period_end}",
                    val, "ratio_pct", [ni.key, cur_r.key],
                    note="净利率 = 净利润/营收", retrieved_at=retrieved,
                )
                print(f"  {ticker}.net_margin: {val:.2f}%")

    # ---- FCF = 经营现金流 - CAPEX（按同期匹配）
    fcf_count = 0
    for c in cfo:
        cap = next((x for x in capex if x.period_end == c.period_end), None)
        if not cap:
            continue
        reg.add_derived(
            f"{ticker}.fcf.{c.period_end}",
            c.value - cap.value,
            "USD",
            [c.key, cap.key],
            note="FCF = 经营现金流 − CAPEX",
            retrieved_at=retrieved,
        )
        fcf_count += 1
    if fcf_count:
        print(f"  {ticker}.fcf: {fcf_count} 期")

    # ---- 季度序列（营收/净利润/经营现金流）与季度同比
    _add_quarterly(reg, ticker, "revenue_q", REVENUE_TAGS)
    _add_quarterly(reg, ticker, "net_income_q", NET_INCOME_TAGS)
    _add_quarterly_ytd(reg, ticker, "cfo_q", CFO_TAGS)

    # ---- 风险指标（L09：波动率/beta/MDD/VaR/CVaR，全部由价格计算）
    rk = compute_risk(ticker)
    rk_note = (
        f"窗口 {rk['n_days']} 交易日，基准 {rk['benchmark']}；"
        f"源：Yahoo Finance 日收盘价"
    )
    reg.add(Fact(
        key=f"{ticker}.risk.vol_ann.{rk['last_date']}",
        value=rk["vol_ann_pct"], unit="ratio_pct",
        source="calculated (tools/risk.py) from Yahoo Finance",
        source_url=f"https://finance.yahoo.com/quote/{ticker}/history",
        retrieved_at=now_hkt(), form="market-data",
        period_end=rk["last_date"], note="年化波动率；" + rk_note,
    ))
    reg.add(Fact(
        key=f"{ticker}.risk.beta.{rk['last_date']}",
        value=rk["beta_vs_benchmark"], unit="ratio",
        source="calculated (tools/risk.py) from Yahoo Finance",
        source_url=f"https://finance.yahoo.com/quote/{ticker}/history",
        retrieved_at=now_hkt(), form="market-data",
        period_end=rk["last_date"], note="beta vs " + rk["benchmark"] + "；" + rk_note,
    ))
    reg.add(Fact(
        key=f"{ticker}.risk.mdd.{rk['last_date']}",
        value=rk["mdd_pct"], unit="ratio_pct",
        source="calculated (tools/risk.py) from Yahoo Finance",
        source_url=f"https://finance.yahoo.com/quote/{ticker}/history",
        retrieved_at=now_hkt(), form="market-data",
        period_end=rk["last_date"], note="最大回撤；" + rk_note,
    ))
    reg.add(Fact(
        key=f"{ticker}.risk.var95.{rk['last_date']}",
        value=rk["var95_daily_pct"], unit="ratio_pct",
        source="calculated (tools/risk.py) from Yahoo Finance",
        source_url=f"https://finance.yahoo.com/quote/{ticker}/history",
        retrieved_at=now_hkt(), form="market-data",
        period_end=rk["last_date"], note="VaR 95% 日收益（历史法）；" + rk_note,
    ))
    if rk["cvar95_daily_pct"] is not None:
        reg.add(Fact(
            key=f"{ticker}.risk.cvar95.{rk['last_date']}",
            value=rk["cvar95_daily_pct"], unit="ratio_pct",
            source="calculated (tools/risk.py) from Yahoo Finance",
            source_url=f"https://finance.yahoo.com/quote/{ticker}/history",
            retrieved_at=now_hkt(), form="market-data",
            period_end=rk["last_date"], note="CVaR 95% 日收益（历史法）；" + rk_note,
        ))
    print(
        f"  {ticker}.risk: vol {rk['vol_ann_pct']}% | beta {rk['beta_vs_benchmark']} | "
        f"MDD {rk['mdd_pct']}% | VaR95 {rk['var95_daily_pct']}% | "
        f"CVaR95 {rk['cvar95_daily_pct']}%"
    )

    # ---- 行情摘要（Yahoo，非 SEC）
    ps = price_summary(ticker)
    reg.add(Fact(
        key=f"{ticker}.price_close.{ps['last_date']}",
        value=ps["close"], unit="USD/share",
        source=ps["source"], source_url=ps["source_url"],
        retrieved_at=ps["retrieved_at"], form="market-data",
        period_end=ps["last_date"],
        note=f"收盘价；52周高 {ps['high_52w']:.2f} / 低 {ps['low_52w']:.2f}；"
             f"近一年回报 {ps['ret_1y_pct']}%；文件 sha256={ps['sha256'][:16]}…",
    ))
    print(f"  {ticker}.price_close: {ps['close']:.2f} USD ({ps['last_date']})")

    reg.save()
    print(f"  -> 已写入 {len(reg.facts)} 条 Fact: {reg.path}")
    return reg


def main() -> None:
    for t in TICKERS:
        build_ticker(t)


if __name__ == "__main__":
    main()
