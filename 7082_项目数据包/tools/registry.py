"""Fact 登记表：报告里出现的每个数字都必须在此登记。"""
from __future__ import annotations

import json
from pathlib import Path

from .config import DATA_DIR
from .provenance import Fact


class Registry:
    """单家公司的数字台账，落盘 data/<TICKER>/registry.json。"""

    def __init__(self, ticker: str):
        self.ticker = ticker
        self.path: Path = DATA_DIR / ticker / "registry.json"
        self.facts: dict[str, Fact] = {}
        if self.path.exists():
            self.load()

    # ---------------------------------------------------------------- CRUD
    def add(self, fact: Fact) -> None:
        self.facts[fact.key] = fact

    def get(self, key: str) -> Fact:
        return self.facts[key]

    def add_derived(
        self,
        key: str,
        value: float,
        unit: str,
        inputs: list[str],
        note: str = "",
        source: str = "calculated (tools/calc.py)",
        source_url: str = "",
        retrieved_at: str = "",
    ) -> Fact:
        """登记一个由其他 Fact 计算得出的数字（保留输入键以便递归溯源）。"""
        fact = Fact(
            key=key,
            value=value,
            unit=unit,
            source=source,
            source_url=source_url,
            retrieved_at=retrieved_at,
            inputs=inputs,
            note=note,
        )
        self.facts[key] = fact
        return fact

    # ---------------------------------------------------------------- IO
    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(
                {k: v.to_dict() for k, v in sorted(self.facts.items())},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def load(self) -> None:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self.facts = {k: Fact(**v) for k, v in raw.items()}

    # ---------------------------------------------------------------- views
    def by_name(self, name: str) -> list[Fact]:
        """按 key 的中段名筛选，如 by_name('revenue')。"""
        return [f for f in self.facts.values() if f.key.split(".")[1] == name]

    def latest(self, name: str) -> Fact | None:
        items = self.by_name(name)
        if not items:
            return None
        return sorted(items, key=lambda f: f.period_end or "")[-1]

    def to_table(self) -> str:
        lines = [f"{'key':<45} {'value':>18} {'unit':<10} {'period':<12} {'form':<6}"]
        for k, f in sorted(self.facts.items()):
            v = f"{f.value:,.0f}" if isinstance(f.value, (int, float)) else str(f.value)
            lines.append(
                f"{k:<45} {v:>18} {f.unit:<10} {str(f.period_end or ''):<12} {str(f.form or ''):<6}"
            )
        return "\n".join(lines)
