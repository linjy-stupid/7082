# 7082 项目缺口清单（Gap Analysis）

> 生成：2026-11-18（数据搜集补完后）
> 用途：一眼看清**老师要求 vs 现状**，以及**还缺什么、谁来做、何时截止**。
> 项目：ELEC7082 Group Project — LLM Research Agent（30%，**2026-11-29 23:59 截止**）

---

## 一、权威要求与来源（已核实）

| 来源 | 内容 | 本地状态 |
|---|---|---|
| **L01 第 5 页** | Group Project 30%，Submit by **Nov 29, 23:59** | ✅ |
| **L01 第 6-7 页** | 2–3 人；Yahoo Finance 量价 + SeekingAlpha + SEC EDGAR 10-K/10-Q + 电话会；function calling 编排；每家 ≤10 页 A4；≤10 分钟录像 | ✅ |
| **L01 第 47-48 页 Appendix B** | 里程碑：10/5 组队 → L6-L7 TA check → 公司名单 L8-L9 → 11/29 提交；评分练四件事（结构化 prompt、工具调用、多 LLM 链、accuracy/coverage/citation 评估） | ✅ |
| **Moodle General 区**（`docs/general_2026-11-18.docx`） | 组队 2–3 人，**10/5 前**注册；**“项目要求详见 Lecture 1 notes”**（官方确认 L01 是唯一完整要求页）；公司名单已发布 | ✅ 已归档 |
| **LO6 课堂（10-26）口头** | 至少一家公司**若干季度**数据；结合**财报正文、电话会记录、金融新闻、研究报告**；**提出并检验假设**；能把任务分解为多步推理 | ⚠️ 仅录音总结 |

> **结论**：L02–L09 的 slides 没有新增硬性要求；L06 的 “Project Core/映射表” 与 L09 的 agent 拓扑练习是**指导或可选练习**，不是交付要求。

## 二、公司名单与选定

Moodle General 区名单（16 家）：

| 市场 | 公司 |
|---|---|
| US | AAPL、**NVDA**、**MSFT**、**PLTR**、CSCO |
| CN | 688256.SH 寒武纪、601138.SH 工业富联、002230.SZ 科大讯飞、002415.SZ 海康威视 |
| JP | 9984.T SoftBank、7203.T Toyota |
| KR | 005930.KS Samsung、000660.KS SK Hynix |
| TW | 2330.TW TSMC、2317.TW Foxconn / Hon Hai |

**本组选定：NVDA / MSFT / PLTR**（均在名单内，覆盖 AI 芯片、云软件、AI 数据分析三种商业模式）。✅

## 三、数据搜集完成度

| 老师要求的数据 | 状态 | 位置 / 说明 |
|---|---|---|
| SEC EDGAR 10-K / 10-Q / 8-K | ✅ 完整 | `data/<T>/filings/`；354 条 XBRL Fact 台账 |
| Yahoo Finance 量价 | ✅ 完整 | 3 年日线 + SPY 基准 |
| **电话会 transcript** | ✅ 完整 | 每家 2 季，共 6 份（`data/<T>/transcripts/`，StockAnalysis/Quartr） |
| 金融新闻 | ✅ 完整 | Yahoo 10 条/家 + SA RSS 20 条/家（元数据） |
| **研究报告（SeekingAlpha）** | ⚠️ 仅标题 | 正文 403 + 订阅墙；`data/UNAVAILABLE.md` 已写标准表述 |
| 分析师预期（前瞻） | ✅ 补充 | `data/<T>/yahoo_estimates.json`（目标价/EPS/营收共识/评级） |
| 引用与置信度 | ✅ 完整 | `data/CITATION_MAP.md`（high 204 / medium 150 / low 0） |
| **数据交叉核对（L6 防线 3）** | ⚠️ 仅抽查 | 尚无系统化 `crosscheck.py`；已核对 NVDA FY2026 revenue（SEC vs Yahoo 一致） |

## 四、交付物缺口（最严重）

| 交付物 | 老师要求 | 现状 |
|---|---|---|
| **Agent 代码** | 多步 LLM research agent，function calling | ❌ `agent/` 为空 |
| **Prompts** | 系统提示词 + Rule 1–5 + JSON schema + CoT + few-shot | ❌ `prompts/` 为空 |
| **工具封装** | `get_price()`、`get_financials()` 等给 LLM 调 | ❌ 只有底层抓取函数，未包装成 tool |
| **多 LLM 串联** | analyst → summarizer → report writer | ❌ 无 |
| **三家公司报告** | 每家 ≤10 页 A4 | ❌ `reports/` 只有校验自测 |
| **演示录像** | ≤10 分钟，讲框架/方法（不讲公司内容） | ❌ 无 |
| **报告质量评估** | accuracy / coverage / citation | ❌ `eval/` 为空 |
| **“提出并检验假设”** | LO6 口头强调 | ❌ 尚未设计进 agent 流程 |

## 五、信息缺口

| 缺口 | 影响 | 建议 |
|---|---|---|
| 提交格式/平台/命名规范 | 11/29 提交可能不合规 | 查 HKU 邮箱（老师 11-02 说邮件说明）；问 TA（Chaoyi XING u3013979@connect.hku.hk） |
| 组队注册是否完成 | 未注册会被随机分组 | 与组员确认 10/5 前已通过链接注册 |
| L10（11/23）可能补充要求 | 最后调整机会 | 上课后核对并更新本文件 |
| LO9（11-16）录音 | 可能有口头通知 | 无本地录音；如组员有可补 |
| NVDA Q3 FY2027 的 10-Q | 电话会（11-17）已开，10-Q 未 filed | 报告注明 “per earnings call, not yet in 10-Q” |

## 六、下一步（建议顺序，倒排 11/29）

1. **本周（11/19–11/22）**：确认组队/提交格式；搭 agent 骨架 + prompts + 工具封装；用 NVDA 跑通端到端。
2. **11/23–11/25**：三家报告初稿（每份 ≤10 页）；跑 `verify.py` 清零；补 `crosscheck.py`。
3. **11/26–11/27**：录像（≤10 分钟，讲框架/方法）；eval（citation coverage、数字校验通过率）。
4. **11/28**：整合、自查、按提交格式打包。
5. **11/29 23:59**：提交。

> 数据侧已封版；**从现在起瓶颈在 agent、报告、录像三件事**。
