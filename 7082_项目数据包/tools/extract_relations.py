"""从 10-K 原文提取跨公司关系证据（客户集中度、供应链、互相提及）。

输出 data/<TICKER>/relations.json：
  - 每条证据保留原句、关键词、字符偏移、源文件
  - 供后续「多跳推理」使用（L02：一家公司的 CAPEX = 另一家的收入）

用法：
    .venv/Scripts/python.exe -m tools.extract_relations
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .config import DATA_DIR, TICKERS

PATTERNS = {
    "customer_concentration": re.compile(
        r"[^.]{0,250}(accounted for|concentration of|largest customer|top customer|"
        r"one customer|single customer)[^.]{0,250}\.", re.I
    ),
    "supplier": re.compile(
        r"[^.]{0,250}(foundry|contract manufacturer|sole source|single source|"
        r"supplier|supply chain)[^.]{0,250}\.", re.I
    ),
}
CROSS = {
    "NVDA": ["Microsoft", "Palantir"],
    "MSFT": ["NVIDIA", "Palantir"],
    "PLTR": ["NVIDIA", "Microsoft"],
}


def _latest_10k(ticker: str) -> Path | None:
    """filings 文件名不含表单类型，需读同名 .meta.json 判断 form。"""
    d = DATA_DIR / ticker / "filings"
    best: tuple[str, Path] | None = None
    for p in d.glob("*.txt"):
        meta_p = p.with_name(f"{p.stem}.meta.json")
        if not meta_p.exists():
            continue
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        if meta.get("form") != "10-K":
            continue
        if best is None or meta.get("retrieved_at", "") > best[0]:
            best = (meta.get("retrieved_at", ""), p)
    return best[1] if best else None


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def extract(ticker: str) -> dict:
    src = _latest_10k(ticker)
    if not src:
        return {"ticker": ticker, "error": "10-K text not found"}
    text = src.read_text(encoding="utf-8")
    out: list[dict] = []
    seen: set[str] = set()

    for label, pat in PATTERNS.items():
        for m in pat.finditer(text):
            sent = _clean(m.group(0))
            if not (60 <= len(sent) <= 500):
                continue
            key = sent[:120]
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "type": label,
                "sentence": sent,
                "char_offset": m.start(),
                "source_file": src.name,
            })

    # 互相提及（跨公司线索）
    for other in CROSS.get(ticker, []):
        pat = re.compile(rf"[^.]{{0,200}}\b{other}\b[^.]{{0,200}}\.", re.I)
        for m in pat.finditer(text):
            sent = _clean(m.group(0))
            if not (40 <= len(sent) <= 400):
                continue
            key = sent[:120]
            if key in seen:
                continue
            seen.add(key)
            out.append({
                "type": f"mentions_{other}",
                "sentence": sent,
                "char_offset": m.start(),
                "source_file": src.name,
            })

    out.sort(key=lambda x: (x["type"], x["char_offset"]))
    result = {
        "ticker": ticker,
        "source_file": src.name,
        "source_path": str(src),
        "n_matches": len(out),
        "matches": out,
    }
    (DATA_DIR / ticker / "relations.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result


def main() -> None:
    for t in TICKERS:
        r = extract(t)
        print(f"{t}: {r.get('n_matches', 0)} 条证据 -> data/{t}/relations.json")
        if r.get("n_matches"):
            for m in r["matches"][:3]:
                print(f"  [{m['type']}] {m['sentence'][:110]}…")


if __name__ == "__main__":
    main()
