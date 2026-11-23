# 7082 项目数据总览

> 公司：NVDA / MSFT / PLTR（均在老师 Moodle General 区 16 家公司名单内）
> 构建时间：2026-11-18
> 原则：**报告中每个数字都必须能在 `registry.json` 找到出处；找不到的数字不许进终稿。**

## 一、目录结构

```
project/
├── data/
│   ├── NVDA/
│   │   ├── companyfacts.json      # SEC XBRL 全量原始数据（627 个标签，4 MB）
│   │   ├── submissions.json       # SEC 文件列表（10-K/10-Q/8-K）
│   │   ├── prices_1d.csv          # Yahoo Finance 日线（3 年 OHLCV）
│   │   ├── registry.json          # ★ Fact 台账（120 条，报告唯一数字来源）
│   │   ├── relations.json         # 10-K 原文中的客户/供应链证据（71 条）
│   │   ├── news.json              # Yahoo 新闻（10 条）
│   │   ├── seekingalpha.json      # Seeking Alpha 公开 RSS 元数据（20 条）
│   │   ├── yahoo_estimates.json   # 分析师共识/目标价/评级分布
│   │   ├── transcripts/           # ★ 电话会全文（JSON+TXT，最近 2 季）
│   │   └── filings/               # 10-K / 10-Q / 8-K 原文纯文本（各 3 份）
│   ├── MSFT/  （同上，114 条 Fact，39 条关系证据）
│   ├── PLTR/  （同上，120 条 Fact，29 条关系证据）
│   ├── CITATION_MAP.md            # ★ 引用与置信度总表（含 transcript/SA/预期）
│   ├── UNAVAILABLE.md             # ★ data unavailable 标准表述（L6 Rule 1）
│   └── GAP_ANALYSIS.md            # ★ 缺口清单（老师要求 vs 现状，下一步）
├── docs/
│   ├── general_2026-11-18.docx    # ★ Moodle General 区原文（要求以 L01 为准 + 16 家公司名单）
│   ├── general_2026-11-18.txt     # 纯文本提取
│   ├── lecture_08_中文精读.md
│   └── lecture_09_中文精读.md
├── tools/
│   ├── config.py                  # 路径、SEC User-Agent、CIK、财年口径
│   ├── provenance.py              # Fact 数据类（溯源字段）
│   ├── sec.py                     # SEC EDGAR 访问（限速/重试/缓存）
│   ├── prices.py                  # Yahoo Finance 价格
│   ├── risk.py                    # 波动率/beta/MDD/VaR/CVaR
│   ├── calc.py                    # 确定性计算（安全表达式）
│   ├── registry.py                # Fact 台账读写
│   ├── build_dataset.py           # 一键重建台账
│   ├── fetch_filings.py           # 下载 10-Q / 8-K
│   ├── extract_relations.py       # 从 10-K 提取跨公司证据
│   ├── fetch_news.py              # 抓新闻
│   ├── fetch_transcripts.py       # ★ 抓电话会全文（StockAnalysis/Quartr）
│   ├── fetch_seekingalpha.py      # ★ 抓 SA 公开 RSS（标题/作者/日期）
│   ├── fetch_estimates.py         # ★ 抓 Yahoo 分析师共识/目标价
│   ├── citations.py               # ★ 引用串 + confidence + CITATION_MAP
│   └── verify.py                  # ★ 报告数字校验器
├── reports/                       # 报告草稿与校验
└── .venv/                         # Python 3.14 虚拟环境
```

## 二、registry.json 的 Fact 字段

```json
{
  "NVDA.revenue.2026-01-25": {
    "key": "NVDA.revenue.2026-01-25",
    "value": 215940000000,
    "unit": "USD",
    "source": "SEC EDGAR XBRL — Revenues",
    "source_url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json",
    "retrieved_at": "2026-11-18T01:xx:xx+08:00",
    "form": "10-K",
    "accession": "0001045810-26-000021",
    "period_start": "2025-01-27",
    "period_end": "2026-01-25",
    "fy": 2026, "fp": "FY", "filed": "2026-02-25",
    "note": "tag=Revenues",
    "inputs": null
  }
}
```

派生指标（同比、毛利率、FCF）的 `inputs` 记录输入 Fact 的 key，可递归溯源到 SEC 原文。

## 三、已覆盖的数据

| 类别 | 内容 | 来源 |
|---|---|---|
| 年度财务（5 年） | 营收、净利润、营业利润、毛利、CFO、CAPEX、EPS、总资产、股东权益 | SEC XBRL |
| 派生指标 | 营收同比、毛利率、净利率、**FCF = CFO − CAPEX** | tools/calc.py |
| 季度财务 | 营收/净利润 13 季 + 同比；现金流 10–14 季（YTD 差分） | SEC XBRL |
| 行情 | 3 年日线 OHLCV、收盘价、52 周高低 | Yahoo Finance |
| 风险指标 | 年化波动率、beta(vs SPY)、最大回撤、VaR95、CVaR95 | tools/risk.py |
| 10-K 全文 | 最新年报 | SEC EDGAR |
| 10-Q 全文 | 最新季报 | SEC EDGAR |
| 8-K | 最新 earnings press release（官方管理层评论） | SEC EDGAR |
| 跨公司证据 | 客户集中度、供应链、互相提及的原句 + 字符偏移 | 10-K 原文 |
| 新闻 | 10 条/家（标题/媒体/时间/链接） | Yahoo Finance |
| 电话会 transcript | 最近 2 季完整全文（NVDA Q3/Q2 FY2027；MSFT Q1 FY2027/Q4 FY2026；PLTR Q3/Q2 2026） | StockAnalysis（Quartr 转录） |
| Seeking Alpha | 20 条/家（标题/作者/日期/链接，不含正文） | SA 公开 RSS |
| 分析师预期 | EPS/营收共识（0q/+1q/0y/+1y）、目标价、评级分布 | Yahoo Finance |

## 四、常用命令

```bash
# 重建全部 Fact 台账（约 2–3 分钟）
.venv/Scripts/python.exe -m tools.build_dataset

# 下载最新 10-Q / 8-K
.venv/Scripts/python.exe -m tools.fetch_filings

# 提取跨公司关系证据
.venv/Scripts/python.exe -m tools.extract_relations

# 抓新闻
.venv/Scripts/python.exe -m tools.fetch_news

# 抓电话会全文（每家公司最近 2 季）
.venv/Scripts/python.exe -m tools.fetch_transcripts --n 2

# 抓 Seeking Alpha 公开 RSS
.venv/Scripts/python.exe -m tools.fetch_seekingalpha

# 抓 Yahoo 分析师共识/目标价
.venv/Scripts/python.exe -m tools.fetch_estimates

# 生成引用台账与 confidence 总表
.venv/Scripts/python.exe -m tools.citations

# 校验报告中的每个数字
.venv/Scripts/python.exe -m tools.verify reports/xxx.md NVDA MSFT PLTR
```

## 五、数据源与合规

| 源 | 性质 | 要求 |
|---|---|---|
| SEC EDGAR | 官方 | User-Agent 必填（`SEC_UA` 环境变量），限速 ≤10 req/s（已内置 0.15 s 间隔） |
| Yahoo Finance | 第三方市场数据 | 报告须标注 "Source: Yahoo Finance, retrieved <日期>" |
| 8-K press release | 官方 | 可替代电话会记录；引用注明 8-K 与日期 |
| 新闻 | 第三方 | 引用须标注媒体名与日期，不得当作财务事实 |
| StockAnalysis / Quartr transcript | 第三方（公开） | 引用写 "StockAnalysis/Quartr transcript, <日期>"；口头数字不冒充 10-Q |
| Seeking Alpha RSS | 第三方（公开元数据） | 只能引标题/作者/日期；正文受订阅限制，未获取 |
| Yahoo 分析师共识 | 第三方预期 | 与公司披露分开表述，标注 "analyst consensus" |

## 六、已知限制

1. **Q4 单季在 XBRL 中通常不单列**（10-K 只报年度）——季度序列会出现缺口，报告用「年度趋势 + 最新季度同比」。
2. **现金流量表在 10-Q 只报 YTD**——已用差分还原单季（`sec.ytd_to_quarters`）。
3. **电话会 transcript 已获取**——用 StockAnalysis 公开全文（Quartr 转录，最近 2 季）；Seeking Alpha 正文仍受订阅限制，只保留公开 RSS 元数据。
4. **Yahoo 新闻质量参差**——只作事件线索，不作数据源。
5. **NVDA/MSFT/PLTR 财年不同**——报告图表必须标注 FY 口径（NVDA 1 月底、MSFT 6 月底、PLTR 12 月底）。
