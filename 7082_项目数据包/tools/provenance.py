"""数据溯源：每个进入报告的数字都必须能回答「哪来的、什么时候抓的、原文在哪」。

Fact 是本项目的唯一数字载体。LLM 不得凭空产生数字；
报告里的每个数值都必须能在 registry 中找到对应的 Fact。
"""
from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

HKT = timezone(timedelta(hours=8))


def now_hkt() -> str:
    return datetime.now(HKT).isoformat(timespec="seconds")


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class Fact:
    """一个可引用、可复核的数据点。"""

    key: str                          # 报告引用键，如 "NVDA.revenue.FY2026"
    value: float | int | str
    unit: str                         # USD / USD/share / ratio_pct / count
    source: str                       # 数据源名称
    source_url: str                   # 可直接点开的原文链接
    retrieved_at: str                 # 抓取时间（HKT）
    form: str | None = None           # 10-K / 10-Q / 8-K / market-data
    accession: str | None = None      # SEC accession number
    period_start: str | None = None
    period_end: str | None = None
    fy: int | None = None
    fp: str | None = None             # FY / Q1 / Q2 / Q3 / Q4
    filed: str | None = None          # SEC 文件提交日
    note: str | None = None
    inputs: list[str] | None = None   # 计算类 Fact 的输入键（可递归溯源）

    def to_dict(self) -> dict:
        return asdict(self)
