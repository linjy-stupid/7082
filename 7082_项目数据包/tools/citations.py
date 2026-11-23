"""引用与置信度：让台账里的每个数字都能直接写成报告里的 source line。

对齐 L6 Technique 5「Hallucination Control」：
  - Rule 2：每个数字必须能给出 source line
  - 输出字段：confidence ∈ {high, medium, low}、sources_cited

生成：
  data/<TICKER>/citation_map.md   单家公司完整引用表
  data/CITATION_MAP.md            三家汇总 + 置信度统计

用法：
    .venv/Scripts/python.exe -m tools.citations
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from .config import CIK, DATA_DIR, TICKERS
from .registry import Registry
from .provenance import Fact

_TAG = re.compile(r"tag=([A-Za-z0-9_]+)")


# ---------------------------------------------------------------- 链接
def _cik_nodash(ticker: str) -> str:
    return CIK[ticker].lstrip("0")


def filing_index_url(ticker: str, accession: str) -> str:
    """SEC filing 索引页（可点开看到 10-K/10-Q 原文与全部附件）。"""
    return (
        f"https://www.sec.gov/Archives/edgar/data/{_cik_nodash(ticker)}/"
        f"{accession.replace('-', '')}/{accession}-index.htm"
    )


def concept_url(ticker: str, fact: Fact) -> str | None:
    """XBRL concept API：只含某一个 tag 的全部申报值，复核单个数字最快。"""
    m = _TAG.search(fact.note or "")
    if not m:
        return None
    tag = m.group(1)
    taxonomy = "dei" if tag.startswith("dei") else "us-gaap"
    return (
        f"https://data.sec.gov/api/xbrl/companyconcept/CIK{CIK[ticker]}/"
        f"{taxonomy}/{tag}.json"
    )


def source_link(ticker: str, fact: Fact) -> str:
    """该 Fact 最直接的复核入口。"""
    if fact.accession:
        return filing_index_url(ticker, fact.accession)
    return fact.source_url or concept_url(ticker, fact) or ""


# ---------------------------------------------------------------- 引用串
def citation(ticker: str, fact: Fact) -> str:
    """报告里可直接粘贴的 source line（Rule 2）。"""
    if fact.inputs:
        return f"[computed: {fact.note or 'derived'}; inputs: {'; '.join(fact.inputs)}]"
    if fact.form in ("10-K", "10-Q") and ("差分" in (fact.note or "") or "YTD" in (fact.note or "")):
        return (
            f"[computed from {fact.form} YTD, filed {fact.filed or 'n/a'}, "
            f"quarter end {fact.period_end}, acc {fact.accession or 'n/a'}]"
        )
    if fact.form == "market-data":
        if "risk." in fact.key:
            return (
                f"[computed from Yahoo Finance daily closes, window ending "
                f"{fact.period_end or 'n/a'}, retrieved {(fact.retrieved_at or '')[:10]}]"
            )
        return (
            f"[Yahoo Finance, {fact.period_end or 'n/a'} close, "
            f"retrieved {(fact.retrieved_at or '')[:10]}]"
        )
    if fact.form in ("10-K", "10-Q", "8-K"):
        gap = None
        if fact.filed and fact.period_end:
            try:
                gap = (date.fromisoformat(fact.filed) - date.fromisoformat(fact.period_end)).days
            except ValueError:
                gap = None
        # 季度值可能来自一年后 10-Q 的「比较期」披露，此时不能标成该财年季度
        if fact.form == "10-Q" and gap is not None and gap > 300:
            return (
                f"[10-Q filed {fact.filed}, comparative period end {fact.period_end}, "
                f"acc {fact.accession or 'n/a'}]"
            )
        period = f"{fact.period_start}→{fact.period_end}" if fact.period_start else (fact.period_end or "")
        if fact.fp == "FY":
            label = f"FY{fact.fy}" if fact.fy else ""
        elif fact.fp:
            label = f"{fact.fp} FY{fact.fy}" if fact.fy else fact.fp
        else:
            label = f"FY{fact.fy}" if fact.fy else ""
        return (
            f"[{fact.form} {label}, {period}, filed {fact.filed or 'n/a'}, "
            f"acc {fact.accession or 'n/a'}]".replace("  ", " ").replace(" ,", ",")
        )
    if fact.source_url:
        return f"[{fact.source}, retrieved {(fact.retrieved_at or '')[:10]}]"
    return f"[{fact.source}]"


# ---------------------------------------------------------------- 置信度
def confidence(fact: Fact) -> str:
    """按来源可核验程度分级（对齐 L6 输出 schema）。"""
    note = fact.note or ""
    if "差分" in note or "YTD" in note:
        return "medium"                    # 由 YTD 差分还原，非申报原文单季值
    if fact.form in ("10-K", "10-Q", "8-K") and not fact.inputs:
        return "high"                      # SEC 官方申报，可直接点开复核
    if fact.inputs:
        return "medium"                    # 确定性计算，递归可溯源
    if fact.form == "market-data":
        return "medium"                    # 第三方行情（Yahoo Finance）
    return "low"


def sources_cited(ticker: str, facts: list[Fact]) -> list[str]:
    """一份 Fact 集合实际用到的数据源清单（对齐输出字段 sources_cited）。"""
    seen: list[str] = []
    for f in facts:
        if f.form in ("10-K", "10-Q"):
            s = "SEC EDGAR"
        elif f.form == "8-K":
            s = "SEC 8-K"
        elif f.form == "market-data":
            s = "Yahoo Finance"
        elif f.inputs:
            s = "computed"
        else:
            s = f.source
        if s not in seen:
            seen.append(s)
    return seen


# ---------------------------------------------------------------- 导出
def _fmt(v) -> str:
    if isinstance(v, (int, float)):
        return f"{v:,.0f}" if abs(v) >= 1000 else f"{v:.2f}"
    return str(v)


def export_ticker(ticker: str) -> Path:
    reg = Registry(ticker)
    rows = [
        "# " + ticker + " — 引用台账",
        "",
        "> 由 `tools/citations.py` 自动生成。报告中引用任何数字，直接从本表复制 source line。",
        "> 置信度规则：`high` = SEC 官方申报直接值；`medium` = 确定性计算或第三方行情；`low` = 其他。",
        "",
        "| Fact key | 值 | 单位 | 期间 | 置信度 | source line（可复制） | 复核链接 |",
        "|---|---|---|---|---|---|---|",
    ]
    for k in sorted(reg.facts):
        f = reg.facts[k]
        link = source_link(ticker, f)
        rows.append(
            f"| `{k}` | {_fmt(f.value)} | {f.unit} | {f.period_end or ''} | "
            f"**{confidence(f)}** | `{citation(ticker, f)}` | {link} |"
        )
    out = DATA_DIR / ticker / "citation_map.md"
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return out


def export_all() -> Path:
    lines = [
        "# 7082 项目 — 引用与置信度总表",
        "",
        "> 由 `tools/citations.py` 自动生成。对齐 L6 Technique 5：每个数字都要有 source line，",
        "> 缺失的数据写 `data unavailable`（见 `UNAVAILABLE.md`）。",
        "",
        "## 各公司引用台账",
        "",
        "| 公司 | Fact 数 | high | medium | low | 明细 |",
        "|---|---|---|---|---|---|",
    ]
    total = {"high": 0, "medium": 0, "low": 0}
    for t in TICKERS:
        reg = Registry(t)
        c = {"high": 0, "medium": 0, "low": 0}
        for f in reg.facts.values():
            c[confidence(f)] += 1
        for k in total:
            total[k] += c[k]
        lines.append(
            f"| {t} | {len(reg.facts)} | {c['high']} | {c['medium']} | {c['low']} | "
            f"[data/{t}/citation_map.md]({t}/citation_map.md) |"
        )
    lines += [
        "",
        f"**合计**：{sum(total.values())} 条 Fact，"
        f"high {total['high']} / medium {total['medium']} / low {total['low']}。",
        "",
        "## 使用规则",
        "",
        "1. **high**：报告可直接引用，粘贴 `source line` 列即可（含 accession，审阅者可点开原文）。",
        "2. **medium**：报告写 *computed by us from [上游 Fact]*；行情写 *Source: Yahoo Finance, retrieved <日期>*。",
        "3. **low**：不得作为结论依据，只能作为线索，并注明来源与日期。",
        "4. 报告里的每个数字都必须能在 `registry.json` 找到；`tools/verify.py` 会同时检查数字出处与引用覆盖。",
        "",
        "## sources_cited 汇总",
        "",
    ]
    for t in TICKERS:
        reg = Registry(t)
        lines.append(f"- **{t}**：{', '.join(sources_cited(t, list(reg.facts.values())))}")

    lines += [
        "",
        "## 辅助数据源（不进 Fact 台账，用于叙事与前瞻）",
        "",
        "| 公司 | 数据 | 条数/规模 | 引用写法 | 文件 |",
        "|---|---|---|---|---|",
    ]
    for t in TICKERS:
        # 电话会 transcript
        tdir = DATA_DIR / t / "transcripts"
        if tdir.exists():
            metas = sorted(tdir.glob("*.meta.json"))
            for mp in metas:
                m = json.loads(mp.read_text(encoding="utf-8"))
                lines.append(
                    f"| {t} | Earnings call transcript | {m['n_chars']:,} 字符 | "
                    f"`[{m['period']} earnings call, {m['call_date']}, StockAnalysis/Quartr]` | "
                    f"[{mp.name.replace('.meta.json', '.txt')}]({t}/transcripts/{mp.name.replace('.meta.json', '.txt')}) |"
                )
        # Seeking Alpha RSS
        sap = DATA_DIR / t / "seekingalpha.json"
        if sap.exists():
            sa = json.loads(sap.read_text(encoding="utf-8"))
            lines.append(
                f"| {t} | Seeking Alpha 公开 RSS（标题/链接） | {sa['n_items']} 条 | "
                f"`[Seeking Alpha, <标题>, <日期>]` | [seekingalpha.json]({t}/seekingalpha.json) |"
            )
        # Yahoo 预期
        yp = DATA_DIR / t / "yahoo_estimates.json"
        if yp.exists():
            y = json.loads(yp.read_text(encoding="utf-8"))
            pt = y.get("price_targets") or {}
            lines.append(
                f"| {t} | Yahoo 分析师共识/目标价 | mean {pt.get('mean')} ({pt.get('low')}–{pt.get('high')}) | "
                f"`[Yahoo Finance analyst consensus, retrieved {y['retrieved_at'][:10]}]` | "
                f"[yahoo_estimates.json]({t}/yahoo_estimates.json) |"
            )

    lines += [
        "",
        "> 辅助数据不得当作财务事实：transcript 只能引用管理层原话；",
        "> Seeking Alpha 只有元数据（正文受订阅限制，未获取）；",
        "> 分析师共识是第三方预期，须与公司披露分开表述。",
    ]
    out = DATA_DIR / "CITATION_MAP.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> None:
    for t in TICKERS:
        p = export_ticker(t)
        print(f"{t}: {p}")
    p = export_all()
    print(f"汇总: {p}")


if __name__ == "__main__":
    main()
