# 7082 项目 — 引用与置信度总表

> 由 `tools/citations.py` 自动生成。对齐 L6 Technique 5：每个数字都要有 source line，
> 缺失的数据写 `data unavailable`（见 `UNAVAILABLE.md`）。

## 各公司引用台账

| 公司 | Fact 数 | high | medium | low | 明细 |
|---|---|---|---|---|---|
| NVDA | 120 | 68 | 52 | 0 | [data/NVDA/citation_map.md](NVDA/citation_map.md) |
| MSFT | 114 | 68 | 46 | 0 | [data/MSFT/citation_map.md](MSFT/citation_map.md) |
| PLTR | 120 | 68 | 52 | 0 | [data/PLTR/citation_map.md](PLTR/citation_map.md) |

**合计**：354 条 Fact，high 204 / medium 150 / low 0。

## 使用规则

1. **high**：报告可直接引用，粘贴 `source line` 列即可（含 accession，审阅者可点开原文）。
2. **medium**：报告写 *computed by us from [上游 Fact]*；行情写 *Source: Yahoo Finance, retrieved <日期>*。
3. **low**：不得作为结论依据，只能作为线索，并注明来源与日期。
4. 报告里的每个数字都必须能在 `registry.json` 找到；`tools/verify.py` 会同时检查数字出处与引用覆盖。

## sources_cited 汇总

- **NVDA**：SEC EDGAR, computed, Yahoo Finance
- **MSFT**：SEC EDGAR, computed, Yahoo Finance
- **PLTR**：SEC EDGAR, computed, Yahoo Finance

## 辅助数据源（不进 Fact 台账，用于叙事与前瞻）

| 公司 | 数据 | 条数/规模 | 引用写法 | 文件 |
|---|---|---|---|---|
| NVDA | Earnings call transcript | 49,068 字符 | `[Q2 2027 earnings call, 2026-08-26, StockAnalysis/Quartr]` | [Q22027.txt](NVDA/transcripts/Q22027.txt) |
| NVDA | Earnings call transcript | 43,362 字符 | `[Q3 2027 earnings call, 2026-11-17, StockAnalysis/Quartr]` | [Q32027.txt](NVDA/transcripts/Q32027.txt) |
| NVDA | Seeking Alpha 公开 RSS（标题/链接） | 20 条 | `[Seeking Alpha, <标题>, <日期>]` | [seekingalpha.json](NVDA/seekingalpha.json) |
| NVDA | Yahoo 分析师共识/目标价 | mean 265.23456 (130.0–515.0) | `[Yahoo Finance analyst consensus, retrieved 2026-11-18]` | [yahoo_estimates.json](NVDA/yahoo_estimates.json) |
| MSFT | Earnings call transcript | 53,933 字符 | `[Q1 2027 earnings call, 2026-10-28, StockAnalysis/Quartr]` | [Q12027.txt](MSFT/transcripts/Q12027.txt) |
| MSFT | Earnings call transcript | 61,570 字符 | `[Q4 2026 earnings call, 2026-07-29, StockAnalysis/Quartr]` | [Q42026.txt](MSFT/transcripts/Q42026.txt) |
| MSFT | Seeking Alpha 公开 RSS（标题/链接） | 20 条 | `[Seeking Alpha, <标题>, <日期>]` | [seekingalpha.json](MSFT/seekingalpha.json) |
| MSFT | Yahoo 分析师共识/目标价 | mean 636.12427 (440.0–870.0) | `[Yahoo Finance analyst consensus, retrieved 2026-11-18]` | [yahoo_estimates.json](MSFT/yahoo_estimates.json) |
| PLTR | Earnings call transcript | 41,709 字符 | `[Q2 2026 earnings call, 2026-08-03, StockAnalysis/Quartr]` | [Q22026.txt](PLTR/transcripts/Q22026.txt) |
| PLTR | Earnings call transcript | 45,833 字符 | `[Q3 2026 earnings call, 2026-11-02, StockAnalysis/Quartr]` | [Q32026.txt](PLTR/transcripts/Q32026.txt) |
| PLTR | Seeking Alpha 公开 RSS（标题/链接） | 20 条 | `[Seeking Alpha, <标题>, <日期>]` | [seekingalpha.json](PLTR/seekingalpha.json) |
| PLTR | Yahoo 分析师共识/目标价 | mean 222.9 (80.0–273.0) | `[Yahoo Finance analyst consensus, retrieved 2026-11-18]` | [yahoo_estimates.json](PLTR/yahoo_estimates.json) |

> 辅助数据不得当作财务事实：transcript 只能引用管理层原话；
> Seeking Alpha 只有元数据（正文受订阅限制，未获取）；
> 分析师共识是第三方预期，须与公司披露分开表述。
