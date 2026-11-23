# data unavailable 清单（L6 Rule 1 标准表述）

> 老师 L6 Technique 5 Rule 1：**没给过的数字不许说；拿不到就写 "data unavailable"，不许猜。**
> 本文件是报告里遇到缺失数据时的标准写法。生成时间：2026-11-18。

## 一、确实拿不到（报告中必须写 data unavailable）

| 项目 | 原因 | 报告里的标准写法 | 可用的替代 |
|---|---|---|---|
| Seeking Alpha 研报/文章正文 | 订阅墙 + 站点对非浏览器请求返回 403；不绕付费墙 | `data unavailable: Seeking Alpha article body (subscription required)` | 只引用公开 RSS 的**标题、作者、日期**：`[Seeking Alpha, "<headline>", <date>]` |
| Seeking Alpha 电话会 transcript | 同上（订阅墙） | 不需要写 unavailable——已取得等价全文 | StockAnalysis / Quartr 的公开完整 transcript（见 `data/<T>/transcripts/`） |
| 另类数据（卫星图像、刷卡、App 排名） | 全部付费，且非本项目硬性要求 | `data unavailable: alternative data (paid vendor)` | 不替代；报告中说明不在范围内 |
| 分析师模型原文/目标价推导过程 | 卖方研报不公开 | `data unavailable: sell-side model (proprietary)` | 只引用 Yahoo Finance 汇总的共识数字（标注第三方） |
| NVDA FY2027 Q3 的 10-Q | 电话会 2026-11-17 已开，但 10-Q 尚未出现在 SEC（截至 2026-11-18） | `data unavailable: NVDA Q3 FY2027 10-Q (not yet filed as of 2026-11-18)` | 该季度数字只能引电话会 transcript，并注明 "per earnings call, not yet in 10-Q" |
| MSFT 2024-06 之前的季度现金流 | 早期 10-Q 的 YTD XBRL 不完整 | `data unavailable: MSFT quarterly cash flow before 2024-06 (XBRL YTD incomplete)` | 用年度现金流 + 现有 10 季趋势 |
| 10-K 中 Q4 单季 | 10-K 只报全年，XBRL 不单列 Q4 | `data unavailable: Q4 standalone (not separately reported in 10-K)` | 用全年减前三季推算时须注明 "derived" |

## 二、拿得到但不属于"事实"（引用规则）

| 数据 | 文件 | 引用规则 |
|---|---|---|
| Seeking Alpha RSS 元数据 | `data/<T>/seekingalpha.json` | 只能写标题/日期作事件线索，**不得**当作分析结论或财务事实 |
| Yahoo Finance 新闻 | `data/<T>/news.json` | 同上：标题作线索，标注媒体与日期 |
| 分析师共识/目标价 | `data/<T>/yahoo_estimates.json` | 写 "Yahoo Finance analyst consensus, retrieved <日期>"，与公司披露分开 |
| 电话会 transcript | `data/<T>/transcripts/*.txt` | 引用写 "management stated on <Q> <FY> earnings call (StockAnalysis/Quartr)"；口头数字不能冒充 10-Q 数字 |

## 三、报告模板句式

```
数据缺失时：
  data unavailable: <项目>（原因：<subscription / not yet filed / not disclosed>）。
  替代：<来源>（如无替代则写 "not estimated"）。

引用 transcript：
  Management guided ... on the Q3 FY2027 earnings call
  (StockAnalysis/Quartr transcript, 2026-11-17).

引用 Seeking Alpha：
  Seeking Alpha headline flagged ... (Seeking Alpha RSS, 2026-11-18);
  article body unavailable (subscription).
```

## 四、原则

1. **宁可写 unavailable，不写估计值**——估计值必须标注 `our estimate` 并给出方法。
2. 替代来源必须**同类**：官方替代官方（8-K 替代 transcript），公开替代付费（StockAnalysis 替代 SA）。
3. 每个替代都要在报告脚注写明原来源为何不可得。
