"""报告数字溯源校验。

规则：报告中出现的每个数值都必须能在 Fact 台账中找到（允许四舍五入误差）。
找不到的数字 = 疑似幻觉，必须删除、改写或补充数据源。

匹配约束（防止「巧合匹配」）：
  - 带 %      只匹配 ratio_pct 类 Fact
  - 带 B/M/K  只匹配 USD 类 Fact 的对应缩放（十亿/百万/千）
  - 无后缀    只匹配 Fact 原始值（不做缩放）

用法：
    .venv/Scripts/python.exe -m tools.verify reports/NVDA_draft.md NVDA MSFT PLTR
"""
from __future__ import annotations

import re
import sys

from .registry import Registry

_NUM = re.compile(
    r"(?<![\w.\-])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
    r"(?:\s*(%|billion|million|thousand|bn|mn|[BMK]))?",
    re.IGNORECASE,
)
_YEAR = re.compile(r"^(19|20)\d{2}$")

_BIG = {"B", "BILLION", "BN"}
_MID = {"M", "MILLION", "MN"}
_SMALL = {"K", "THOUSAND"}


def _to_float(raw: str) -> float:
    return float(raw.replace(",", ""))


def extract(text: str) -> list[dict]:
    """抽取候选数字，跳过日期与独立年份。"""
    out = []
    for m in _NUM.finditer(text):
        raw = m.group(1)
        if _YEAR.match(raw):
            continue
        before = text[max(0, m.start() - 1):m.start()]
        after = text[m.end():m.end() + 1]
        if before == "-" or after == "-":     # 日期片段
            continue
        out.append({
            "raw": m.group(0).strip(),
            "value": _to_float(raw),
            "suffix": (m.group(2) or "").upper(),
            "context": text[max(0, m.start() - 45):m.end() + 45].replace("\n", " "),
        })
    return out


def _best(num: float, facts: list[tuple[str, float, str]], scale: float,
          tol: float) -> tuple[str, float] | None:
    best = None
    for key, val, _unit in facts:
        target = val / scale
        if target == 0:
            if num == 0 and best is None:
                best = (key, 0.0)
            continue
        err = abs(num - target) / abs(target)
        if err <= tol and (best is None or err < best[1]):
            best = (key, err)
    return best


def _match(item: dict, facts: list[tuple[str, float, str]], tol: float):
    num, suffix = item["value"], item["suffix"]
    if suffix == "%":
        return _best(num, [f for f in facts if f[2] == "ratio_pct"], 1.0, tol)
    if suffix in _BIG:
        return _best(num, [f for f in facts if f[2] == "USD"], 1e9, tol)
    if suffix in _MID:
        return _best(num, [f for f in facts if f[2] == "USD"], 1e6, tol)
    if suffix in _SMALL:
        return _best(num, [f for f in facts if f[2] == "USD"], 1e3, tol)
    return _best(num, facts, 1.0, tol)


def verify_text(
    text: str,
    tickers: list[str],
    tol: float = 0.006,
    verbose: bool = True,
) -> list[dict]:
    facts: list[tuple[str, float, str]] = []
    for t in tickers:
        reg = Registry(t)
        for k, f in reg.facts.items():
            if isinstance(f.value, (int, float)):
                facts.append((k, float(f.value), f.unit))

    unmatched: list[dict] = []
    matched = 0
    for item in extract(text):
        hit = _match(item, facts, tol)
        if hit:
            matched += 1
            if verbose:
                print(f"[OK]   {item['raw']:<14} -> {hit[0]}  (err {hit[1]*100:.3f}%)")
        else:
            unmatched.append(item)
            if verbose:
                print(f"[MISS] {item['raw']:<14} ...{item['context']}...")

    if verbose:
        print(f"\n匹配 {matched} 个；未匹配 {len(unmatched)} 个")
        if unmatched:
            print("未匹配数字（疑似无出处，必须处理）：")
            for u in unmatched:
                print(f"  - {u['raw']}  |  {u['context']}")
    return unmatched


def main() -> int:
    if len(sys.argv) < 3:
        print("用法: python -m tools.verify <报告文件> <TICKER...>")
        return 2
    text = open(sys.argv[1], encoding="utf-8").read()
    unmatched = verify_text(text, sys.argv[2:])
    return 0 if not unmatched else 1


if __name__ == "__main__":
    raise SystemExit(main())
