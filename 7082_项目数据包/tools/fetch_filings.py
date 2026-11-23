"""下载最新 10-Q 全文与 8-K earnings release（exhibit 99.x）。

用法（在 project 目录下）：
    .venv/Scripts/python.exe -m tools.fetch_filings
"""
from __future__ import annotations

from . import sec
from .config import TICKERS


def main() -> None:
    for t in TICKERS:
        print(f"\n=== {t} ===")

        qs = sec.latest_filings(t, "10-Q", 1)
        if qs:
            q = qs[0]
            p = sec.download_filing_text(
                t, q["accession"], q["primary_doc"], form="10-Q"
            )
            print(f"  10-Q {q['filing_date']} -> {p.name} ({p.stat().st_size:,} bytes)")
        else:
            print("  [warn] 未找到 10-Q")

        ks = sec.latest_filings(t, "8-K", 20)
        found = next((k for k in ks if "2.02" in (k.get("items") or "")), None)
        if not found:
            print("  [warn] 最近 20 份 8-K 中没有 Item 2.02（earnings release）")
            continue
        p = sec.download_8k_exhibit(
            t, found["accession"], primary_doc=found["primary_doc"]
        )
        if p:
            print(
                f"  8-K {found['filing_date']} items={found['items']} "
                f"-> {p.name} ({p.stat().st_size:,} bytes)"
            )
        else:
            print(f"  8-K {found['filing_date']}: 未找到 exhibit 99.x")


if __name__ == "__main__":
    main()
