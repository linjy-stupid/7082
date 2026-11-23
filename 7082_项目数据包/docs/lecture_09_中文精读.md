# Lecture 9 逐页中文精读

**原文件**：`lecture_09.pdf`（84 页；正文页脚编号 2/60–60/60，PDF 密码 `student`）
**课程**：AI × Finance｜Lecture 9 of 10｜Dr. Z.C. Lin｜Week 9｜Module III · Applications（L8–L10）第 2 讲
**用途**：期末复习——Final Exam 11 月 30 日，权重 40%，覆盖 L6–L10（术语保留英文，考试为英文选择题 + 简答）

> 📌 **本讲定位**：**组合与风险管理**——Part A 用经典框架（MPT/MVO/CAPM、风险指标与绩效指标）立"标尺"，Part B 用 AI 改进组合构建（ML 修输入、RL 直接优化、LLM 补宏观推理），Part C 给出本讲 signature 的多智能体投资委员会，Part D 用 LLM 做价格模型看不见的文本风险控制。

---

## 第 1 页 · Portfolio & Risk Management with AI（封面）

**Portfolio & Risk Management with AI**——AI 驱动的组合与风险管理
Lecture 9 of 10｜Dr. Z.C. Lin｜Week 9｜Dept. of Electrical and Electronic Engineering, HKU

> 💡 标题两个关键词：**Portfolio**（组合构建）+ **Risk**（风险度量与控制），AI 是贯穿两者的新工具。

---

## 第 2 页 · Lecture Overview（本讲概览）

**位置**：Module III – Applications（L8–L10）**第 2 讲（共 3 讲）**。

本讲的结构安排很明确：把经典组合/风险理论（MPT、MVO、CAPM、risk & performance metrics）**压缩成评估标尺（约 40%）**，其余篇幅全部给新前沿——**AI 驱动的组合构建**、**多智能体投资委员会（multi-agent investment committee）**、**LLM 驱动的风险控制**。

**反复出现的主题（The Recurring Theme）**：经典理论给我们**标尺（yardsticks）**；AI 给我们更好的**估计（estimation）**、**优化（optimization）**，以及通过多智能体范式得到的**人类投委会的可扩展代理（scalable proxy）**。

> 💡 全讲一句话：**经典负责"什么叫好"，AI 负责"怎么做得更好"。**

---

## 第 3 页 · Learning Objectives（学习目标）

学完本讲，你应当能够：

1. **把经典组合与风险框架当作评估标尺**——risk/return、MPT、efficient frontier、CAPM/beta、VaR/CVaR/MDD、Sharpe/Sortino；
2. **理解 AI/ML 如何改造组合构建**——ML 修输入、RL 直接优化、LLM 做动态配置；
3. **掌握多智能体投资委员会范式**——analyst agents 辩论、PM 综合、risk-officer agents 否决；
4. **学习 LLM 驱动的风险控制技术**——earnings-call tone、ESG + knowledge-graph 传染、基准测试。

> 💡 四个目标与 Part A/B/C/D **一一对应**，也是 Appendix A 的四大考点块。

---

## 第 4 页 · Lecture Roadmap（本讲路线图）

| Part | 内容 | 占比 |
|---|---|---|
| **A** | 经典标尺（压缩）：risk & return → MPT/MVO → CAPM/beta → risk metrics → performance metrics | **∼40%** |
| **B** | AI 构建组合：ML for inputs → RL 直接优化 → LLM 动态配置 | **∼25%** |
| **C** | **SIGNATURE**：多智能体投资委员会——analysts debate → PM synthesizes → risk officers veto | **∼20%** |
| **D** | LLM 驱动的风险控制——earnings-call tone → crash risk；ESG+KG contagion；PIXIU/FinMA benchmark | **∼15%** |

**The Bridge（桥梁）**：Part A 的各类指标，成为 Part B–D 中**每一个 AI 系统的评估标尺**。

> 💡 记住 40/25/20/15 这张权重表——它同时就是考试分组的来源。

---

## 第 5 页 · 章节扉页

**Part A — Classic Frameworks**：经典框架，压缩为评估标尺，不做推导。

> 💡 先立标尺：这一部分不推导公式，只提炼评价 AI 策略所需的词汇与直觉。

---

## 第 6 页 · The Goal of Part A（Part A 的目标）

本部分的目标**不是**让你推导 Markowitz，而是给你**评估一个 AI 交易系统所需的词汇与直觉**。

**每个 AI 策略都逃不出这些指标**：本课程中所有 AI 策略，最终都由本部分引入的 risk metrics 与 performance metrics 来评判——**记直觉，不记代数（memorize the intuition, not the algebra）**。

> 💡 这一页定调：Part A 是"评分标准"，不是"数学课"。

---

## 第 7 页 · 章节扉页

**Risk & Return**——收益与风险，一切指标的起点。

> 💡 从最基础的两个量开始：收益 r 与风险 σ²。

---

## 第 8 页 · Return and Risk（收益与风险）

**收益（return）**是投资在一段时间内的盈亏：

```
r = (v_t − v_0) / v_0
```

要区分两种收益：

| 概念 | 方向 | 含义 |
|---|---|---|
| **期望收益 E[r]** | forward-looking（前瞻） | 投资决策真正需要的量 |
| **历史平均收益 r̄** | backward-looking（回溯） | 唯一可直接观测的代理 |

**用历史收益估计未来期望收益，是投资中最核心、也最困难的问题。**

**风险（risk）**是结果的不确定性，习惯上用 variance / standard deviation 度量：

```
σ² = (1/N) · Σ_i (r_i − r̄)²
```

方差越大 = 可能收益的分布越宽 = 风险越大。这是一个**刻意简化**的定义——它的局限（**fat tails、asymmetry**）留到 §4 讨论。

> 💡 两个公式必须会写；"E[r] 由 r̄ 估计"这句话是简答题的万能开头。

---

## 第 9 页 · Portfolio Risk Decomposition（组合风险分解）

**Part A 最重要的一个思想**：持有多只资产时，组合总风险可以拆成两类：

| 风险类型 | 来源 | 可分散？ |
|---|---|---|
| **Systematic risk**（市场风险） | 全市场冲击（衰退、战争、加息） | **否**——影响所有资产 |
| **Idiosyncratic risk**（特质风险） | 公司/行业特定事件（CEO 离职、药物试验失败） | **是**——约 **30+ 只不相关**股票即可基本消除 |

**分散化的力量（The Power of Diversification）**：把收益**不完全相关**的资产组合起来，可以在**不降低期望收益**的前提下降低组合总风险。这几乎是金融里唯一的"免费午餐"。

> 💡 必背：**系统风险不可分散，特质风险可分散（∼30+ uncorrelated names）**。

---

## 第 10 页 · Why Correlation Matters（相关性为何重要）

两资产组合的方差：

```
σ_p² = w₁²σ₁² + w₂²σ₂² + 2·w₁·w₂·ρ₁,₂·σ₁·σ₂
```

**分散化的杠杆**就在最后一项——由相关系数 **ρ₁,₂** 驱动。当 **ρ 很低或为负**时，这一项缩小甚至变负，把组合风险**拉到低于各资产风险的加权平均**。

数值例子见 Case Study 1（第 27 页）。

> 💡 公式第三项 = 分散化攻击的靶点；**ρ 是杠杆**。

---

## 第 11 页 · 章节扉页

**Modern Portfolio Theory (MPT)**——现代组合理论。

> 💡 Markowitz 把“选股”变成“在风险-收益平面上选点”。

---

## 第 12 页 · Markowitz's Big Idea（Markowitz 的核心思想）

Harry Markowitz 1952 年的论文 **《Portfolio Selection》** 把投资重新表述为在 **(risk, return) 对**上的最优化问题：

> 给定某一风险水平，存在一个使期望收益最大的组合；所有这类最优组合构成的集合，就是 **efficient frontier（有效前沿）**。

在 (risk, return) 平面上，前沿是一条**凹曲线（concave curve）**：曲线**下方**的组合被支配（dominated，同风险下能拿到更高收益），曲线**上方**不可达（unattainable）。理性投资者持有前沿上的某个组合，按自己的风险承受度选点。

> 💡 记 **1952 + Portfolio Selection + efficient frontier = 凹曲线 + 下方被支配/上方不可达**。

---

## 第 13 页 · The Efficient Frontier — Visualized（有效前沿示意）

图：横轴 **Risk (σ)**，纵轴 **Expected Return**。

- 曲线即 **Efficient Frontier**；
- 曲线**下方**为 **DOMINATED**（同风险下收益更低，被支配）；
- 曲线**上方**为不可达区域——除非**加杠杆（leverage）或拥有 alpha**。

> 💡 一句话：前沿 = "**同风险下收益最高**"的边界；想站到它上面，要么借杠杆，要么有真 alpha。

---

## 第 14 页 · Mean-Variance Optimization (MVO)（均值-方差优化）

MVO 是**找出前沿组合的配方**。给定输入——期望收益向量 **µ** 与协方差矩阵 **Σ**——求解权重 **w**，两种等价表述：

- **maximize return** subject to a **variance cap**（在方差上限下最大化收益）；
- **minimize variance** `wᵀΣw` subject to a **target return**（在目标收益下最小化方差）。

**直觉**："**用风险最低的方式达到我的收益目标**。"（讲义刻意跳过矩阵代数——直觉才重要。）

> 💡 MVO 的两个优化式子是同一枚硬币的两面，选择题常考"哪个是最小化、哪个是最大化"。

---

## 第 15 页 · MVO's Fatal Flaw — "Error Maximization"（MVO 的致命缺陷：误差最大化）

**Part A 最重要的一页，也是 AI 进入画面的原因。**

**问题**：MVO 对输入**极其敏感（exquisitely sensitive）**。期望收益或协方差的**微小估计误差**，会产生截然不同、常常**极端且集中**的组合——这就是 **error maximization** 问题：**优化器把你的估计噪声放大成了组合权重**。

例子：如果你告诉 MVO 资产 X 的期望收益是 **9%** 而不是真实的 **8%**，它可能把组合的 **60%** 押到 X 上。优化器**完全按你说的做**——只是你说的是垃圾输入。

**这正是 AI/ML 要填的缺口**：更好的 µ 和 Σ → 更少的噪声进入优化器 → 更稳定的组合。

> 💡 全讲因果链：**MVO 敏感 → error maximization → 才有 Part B 的三条 AI 路线**。

---

## 第 16 页 · 章节扉页

**CAPM, Beta & Factor Investing**——资产定价：从单因子到多因子。

> 💡 单因子定价回答：承担市场风险，该拿多少回报？

---

## 第 17 页 · CAPM & the Security Market Line（CAPM 与证券市场线）

CAPM 把期望收益**钉在单一风险因子——市场**上：

```
E[R_i] = R_f + β_i · (E[R_m] − R_f)
```

- **R_f** = risk-free rate；**(E[R_m] − R_f)** = market risk premium（市场风险溢价）；
- **β_i = cov(R_i, R_m) / var(R_m)**，衡量对市场的敏感度：

| β 取值 | 含义 |
|---|---|
| β = 1 | 与市场同步 |
| β > 1 | 放大市场波动 |
| 0 < β < 1 | 减弱市场波动 |
| β < 0 | 与市场反向 |

**SML（Security Market Line）** 把 E[R_i] 对 β_i 作图。资产若落在 SML **上方**，说明它提供的收益超过其 beta 应有的水平 → **"undervalued"（低估）**。

> 💡 公式 + β 的四种读法 + "SML 上方 = 低估"是选择题三连。

---

## 第 18 页 · Factor Investing & Smart Beta（因子投资与 smart beta）

因子投资的观点：**市场不是唯一被定价的风险**，长期收益由**多个因子**驱动。**Smart beta** 通过 ETF 提供对因子的**规则化暴露**，定位介于"便宜的市值加权指数"与"昂贵的主动管理"之间。

| 因子 | 一句话逻辑 |
|---|---|
| **Value** | 相对基本面便宜（低 P/E、低 P/B） |
| **Size** | 小盘股历史上跑赢 |
| **Momentum** | 赢家短期内继续赢 |
| **Quality** | 盈利、低负债、盈利稳定 |
| **Low volatility** | 低波动股票的风险调整后收益更好 |

> 💡 五个因子名 + smart beta 的"中间层"定位，是概念题常客。

---

## 第 19 页 · 章节扉页

**Risk Metrics**——方差不够用，换一套风险工具箱。

> 💡 方差只描述离散度；真实风险还要看尾部与回撤。

---

## 第 20 页 · Beyond Variance（超越方差）

Variance 把上行与下行**一视同仁**，且**忽略尾部形状**。真实的风险管理用更丰富的工具箱：

| 指标 | 告诉你什么 | 弱点 |
|---|---|---|
| **VaR**（Value at Risk） | 给定置信水平与期限下的**最大损失**。"95% 1-day VaR = $1M" → 95% 概率单日损失 < $1M | **不说明超过阈值后能有多惨** |
| **CVaR / ES** | 最差 **(1 − confidence)%** 尾部内的**平均损失** | 需要更多数据；仍假设某种分布 |
| **MDD**（Max Drawdown） | 最大峰谷跌幅：**(Peak − Trough) / Peak** | 不说明**恢复要多久** |
| **Tracking Error** | (组合收益 − 基准收益) 的**标准差** | **低 TE ≠ 好**——可能只是风险暴露不足 |
| **Variance / std dev** | 收益的离散度 | 上下行不分；假设正态 |

> 💡 五个指标的"定义 + 弱点"必须成对记忆，Appendix A 的 §4–5 就考这个。

---

## 第 21 页 · VaR vs. CVaR, and Why Drawdown Matters（VaR 与 CVaR；回撤为何重要）

**VaR vs CVaR 的直觉**：

| 对比 | VaR | CVaR / ES |
|---|---|---|
| 做法 | 在 5% 最差情形处**画一条线** | 对这条线**后面的一切取平均** |
| 回答的问题 | "阈值在哪？" | "**越过阈值后平均亏多少？**" |
| 尾部信息 | 无 | 有 |
| 适用 | 常规风险报告 | **有偶发崩盘的策略**；监管（Basel III）已从 VaR 迁移到 CVaR/ES |

**Maximum Drawdown——行为面指标**：**50% 的回撤需要 100% 的涨幅才能回本**，而投资者往往在**底部赎回**。因此 MDD 是基金的**生存指标（survival metric）**。

> 💡 考点句：**VaR 画线，CVaR 算线后的平均**；50% → 100% 的回本算术。

---

## 第 22 页 · Risk Frameworks（风险框架）

**Risk Parity（风险平价）**：让每项资产对组合的**风险贡献（risk contribution）相等**，而**不是资金相等**——债券波动低，所以分到更多资金。目标是**没有单一资产主导风险预算**，使配置在 regime shifts 下比等权或市值加权更有韧性。

**Stress Testing vs Scenario Analysis**：

| 方法 | 做法 | 例子 | 时间方向 |
|---|---|---|---|
| **Stress testing** | 把**特定历史灾难**重放到今天的组合上："如果过去重演，我们能活下来吗？" | 2008 GFC、2020 COVID crash、2022 rate shock | 历史冲击 |
| **Scenario analysis** | 假设**前瞻性经济情景**，追踪组合影响 | soft landing、stagflation、hard landing | 未来想象 |

区别一句话：stress testing 用**历史冲击**；scenario analysis 想象**可能没有精确历史先例的前瞻冲击**。

> 💡 三组概念一起考：risk parity（按风险分资金）、stress（重放历史）、scenario（假设未来）。

---

## 第 23 页 · 章节扉页

**Performance Evaluation Metrics**——收益必须按风险调整后才能比较。

> 💡 收益不能裸比——必须除以某种风险。

---

## 第 24 页 · The Yardstick for Every AI Strategy（每个 AI 策略的标尺）

| 指标 | 公式 | 用哪种风险做调整 |
|---|---|---|
| **Sharpe Ratio** | (R_p − R_f) / σ_p | **总波动率**（total volatility） |
| **Sortino Ratio** | (R_p − R_f) / σ_d | **仅下行偏差**（downside deviation） |
| **Treynor Ratio** | (R_p − R_f) / β_p | **系统风险**（β） |
| **Information Ratio** | (R_p − R_b) / σ_excess | 相对基准的 **tracking error** |

**Which Ratio When?（什么时候用哪个）**

- 独立看总风险 → **Sharpe（默认）**；
- 关注不对称/下行 → **Sortino**；
- 作为分散化整体的一部分持有 → **Treynor**；
- 主动管理者跑赢基准 → **Information Ratio**。

> 💡 四个比率的分母是唯一记忆点：**σ_p / σ_d / β_p / tracking error**。

---

## 第 25 页 · Key Lesson: High Sharpe Can Hide Tail Risk（高 Sharpe 可能掩盖尾部风险）

Sharpe 的分母是**总波动率**。于是"**稳定小赚 + 偶发巨亏**"的策略会呈现：Sharpe 很好（总波动低），但 Sortino 很糟（下行偏差高）。

**Never Evaluate a Strategy with a Single Metric（永远不要用单一指标评价策略）**——这是构建 AI 交易系统时**最重要的评估习惯**：一个回测 Sharpe 很高的模型，仍可能是"等待发生的灾难"（见 Case Study 2）。

> 💡 这是全讲最实用的一句话，简答题可直接引用。

---

## 第 26 页 · 章节扉页

**Case Study 1: Two-Asset Portfolio**——两资产组合的数值演示。

> 💡 用两只股票把“相关性 = 分散化杠杆”算成数字。

---

## 第 27 页 · Setup & Results（设置与结果）

**设置**：两只股票各投一半。Stock A：E[r_A] = 8%，σ_A = 12%；Stock B：E[r_B] = 15%，σ_B = 25%。组合期望收益**恒为** 0.5×8% + 0.5×15% = **11.5%**，与相关性无关。

| 相关系数 ρ | 组合 σ_p | 解读 |
|---|---|---|
| **−1** | **6.5%** | 完美对冲——风险远低于加权平均（18.5%） |
| **0.4** | **15.9%** | 典型股票对——有意义的分散化 |
| **+1** | **18.5%** | 无分散化——风险 = 加权平均 |

**Lesson**：同样的期望收益（11.5%），风险却仅因相关性不同而从 **6.5% 变到 18.5%**——这就是为什么"**寻找低相关资产**"是组合构建的核心任务。

> 💡 四个数字背下来：**11.5% / 6.5% / 15.9% / 18.5%**。

---

## 第 28 页 · 章节扉页

**Case Study 2: High Sharpe, Low Sortino**——高 Sharpe、低 Sortino 的陷阱。

> 💡 同一个策略：Sharpe 说很好，Sortino 说很糟。

---

## 第 29 页 · The Numbers & The Lesson（数字与教训）

**设置**：一个卖期权策略（如 short put spreads）——大多数月份赚取稳定小额权利金，偶尔爆仓。

```
R_p = 10%，R_f = 2%
总波动率 σ_p = 6%（稳定权利金让总波动显得很低）
下行偏差 σ_d = 12%（罕见崩盘主导下行）

Sharpe  = (10% − 2%) / 6%  = 1.33   ← 看起来很棒
Sortino = (10% − 2%) / 12% = 0.67   ← 其实平庸
```

**Lesson**：Sharpe 会被"**在压路机前捡硬币（picking up pennies in front of a steamroller）**"的策略骗过。只惩罚下行的 **Sortino** 才揭示了隐藏的尾部风险。回测 Sharpe 很好的模型，仍可能是等待发生的灾难。

> 💡 **1.33 vs 0.67** 是必记数字；它解释了第 25 页的"单一指标禁忌"。

---

## 第 30 页 · 章节扉页

**Part B — AI Transforms Portfolio Construction**：AI 改造组合构建——主攻 MVO 的 error-maximization 缺陷，三条路线。

> 💡 三条 AI 路线，全部围绕 MVO 的 error maximization 展开。

---

## 第 31 页 · Three Ways AI Attacks Error Maximization（AI 攻误差最大化的三条路）

Part A 以 MVO 的致命缺陷收尾：**坏输入导致的 error maximization**。Part B 给出三种 AI 打法：

1. **Improving the inputs（§6）**——用 ML 得到更好的 **µ** 和 **Σ**；
2. **Replacing predict-then-optimize with direct RL optimization（§7）**；
3. **Adding qualitative macro reasoning via LLMs（§8）**。

> 💡 三条路线 = 三个小节号 = Appendix A 的 §6–8，一一对应别记混。

---

## 第 32 页 · 章节扉页

**ML for Portfolio Inputs**——先修"输入"。

> 💡 最直接的一条路：先修输入端的 µ 与 Σ。

---

## 第 33 页 · ML for Return Forecasting & Covariance Estimation（ML 做收益预测与协方差估计）

MVO 只需要两个输入：**µ** 与 **Σ**，而两者都出了名地难估。

| 输入 | 难点 | ML 解法 |
|---|---|---|
| **µ 期望收益** | 噪声大、非平稳 | 用 L4 的监督学习工具箱——**gradient-boosted trees、ensembles、neural nets**——从特征预测未来收益，作为喂给优化器的 µ。更好的 µ → 更少估计噪声 → 更少 error maximization |
| **Σ 协方差** | 原始样本协方差噪声大 | ① **shrinkage estimators**（向结构化目标收缩）；② **factor models**（协方差 = 因子协方差 + 残差）；③ **deep covariance prediction**（以市场 regime 为条件的神经网络） |

> 💡 协方差的三个补救名词（shrinkage / factor model / deep covariance）是本节唯一硬考点。

---

## 第 34 页 · 章节扉页

**RL for Direct Portfolio Optimization**——跳过两步法，直接学权重。

> 💡 不再先预测再优化，而是让 agent 直接输出权重。

---

## 第 35 页 · Skipping the Two-Step: Direct RL Weights（跳过两步：RL 直接输出权重）

传统做法是两步 **predict-then-optimize**（先预测收益 → 再跑 MVO）。**强化学习 agent 直接学权重**：通过**最大化跨期的风险调整收益**来学习。

| 要素 | 在组合 RL 中的含义 |
|---|---|
| **State** | 当前市场特征 + 当前持仓/头寸 |
| **Action** | 目标组合权重 **w_t**（连续向量、和为 1、带约束） |
| **Reward** | 风险调整收益，例如 **differential Sharpe ratio**（在线、可微的近似） |

> 💡 **State / Action / Reward** 三要素是 §7 的标准选择题。

---

## 第 36 页 · Advantages over Predict-Then-Optimize（相对两步法的优势）

- **Regime adaptation**——agent 从奖励信号中**隐式学会**"高波动 regime 下多持现金"；
- **Constraints in the policy**——换手率上限、禁止做空、行业上限**写进动作空间**，而不是事后硬加；
- **No error-maximization cascade**——不再有一个脆弱的独立优化器去放大噪声。

**这就是 FinRL 的 portfolio mode**（L8 见过）。当目标**路径依赖**（如"一年内最大化 Sharpe 且回撤有上限"）而一次性优化器处理不好时，RL 最合适。

> 💡 三个优势 + "FinRL portfolio mode" 出处，是 §7 的采分点。

---

## 第 37 页 · 章节扉页

**LLM-Driven Dynamic Asset Allocation**——LLM 做动态资产配置。

> 💡 量化模型读不懂 Fed 声明，LLM 可以。

---

## 第 38 页 · Filling the Qualitative-Reasoning Gap（填补定性推理的空白）

纯量化模型对**定性宏观推理**是盲的——而 CIO 读一份 Fed 声明正是在做这种推理。LLM 可以填这个缺口。

**FinGPT Robo-Advisor 模式（三步）**：

1. **喂宏观输入**：Fed statements、CPI prints、yield-curve moves、sentiment indices、news；
2. **LLM 推断 regime**（如"利率见顶、信用利差走阔、情绪谨慎 → 防御性倾斜"）；
3. **输出高层资产配置（high-level asset allocation）**，再交给**量化优化器**细化到个券权重。

> 💡 关键分工：**LLM 定大类，optimizer 定个券**。

---

## 第 39 页 · The Critical Caveat — Division of Labor（关键警告：分工）

**例子**：LLM 读到鹰派 FOMC 声明 + 走弱的就业数据 + 上升的 VIX → 建议**减少股票暴露、增加久期（duration）**。只喂价格数据的纯因子模型会**滞后**于这个判断。

**Do NOT Ask the LLM to Predict Prices Directly（不要让 LLM 直接预测价格）**：有 **hallucination risk**，且**没有数值校准（no numerical calibration）**。让它做擅长的事——**从文本判断 regime 与 sentiment**——然后把数字交给量化优化器。

> 💡 金句：**"The LLM is the macro strategist, not the stock picker."**

---

## 第 40 页 · 章节扉页

**Part C — Multi-Agent Investment Committee**：用 LLM agents 模拟人类投资委员会（本讲 signature）。

> 💡 本讲 signature：用 agents 复刻投委会的辩论与否决。

---

## 第 41 页 · The Multi-Agent Investment Committee（多智能体投资委员会）

前沿的 AI-in-finance 研究正在用**多个 LLM agents** 模拟真实的投资委员会，每个 agent 承担**专门化角色**。

> 核心想法一句话：**用多个 LLM agents 模拟一个真实的投资委员会。**

> 💡 Part C 的全部内容都从这句话展开：**角色分工 + 辩论 + 否决**。

---

## 第 42 页 · The Concept（概念）

本节展开"为什么委员会有效"以及"agents 如何模仿它"。

> 💡 概念页，承接下一页的两大支柱。

---

## 第 43 页 · Why Committees Work — and How Agents Mimic Them（委员会为何有效，agents 如何模仿）

真实投委会之所以有效，靠两件事：

1. **多元专家视角**——value analyst、growth analyst、macro strategist 各看一角；
2. **独立风险监督**——有 risk officer **可以杀掉一笔交易**。

**多智能体的模仿**：多个 LLM analyst agents，各自**扮演不同投资专业人士**（不同专长、不同数据、不同视角），通过**辩论（DEBATE）**得出选股结论；随后 **risk-officer agents** 从多个风险维度**审查并约束**该结论，拥有**否决权（veto power）**。

**收益（payoff）**：多元视角 + 风险监督，但**自动化、可扩展**——人类委员会一周开一次会；agent 委员会可以**每天、对全市场每只股票**运行。

> 💡 两个支柱：**diverse perspectives + independent risk oversight**；卖点是 scalable。

---

## 第 44 页 · Architecture（架构）

三层：analyst agents → PM agent → risk-officer agents。

> 💡 下一页给出完整拓扑图，务必能默画。

---

## 第 45 页 · The Three-Layer Architecture（三层架构）

```
                    TARGET STOCK（例如 AAPL）
                              │
     ┌───────────┬────────────┼────────────┬───────────┐
  Value       Growth      Momentum       Macro          ← 第 1 层：Analyst Agents
     └───────────┴────────────┼────────────┴───────────┘
                    PORTFOLIO MANAGER (PM) AGENT — synthesizes
                              │  初步建议：ticker + direction + size
     ┌───────────┬────────────┼────────────┬───────────┐
 Drawdown    Volatility   Liquidity   Concentration     ← 第 3 层：Risk Officer Agents
     └───────────┴────────────┼────────────┴───────────┘
              FINAL DECISION：approve/execute 或 veto/reduce
```

| 层 | 角色 | 职责 | 输出 |
|---|---|---|---|
| 1 | **Analyst Agents**（Value / Growth / Momentum / Macro） | 各自视角**独立**分析 | thesis：bullish/bearish/neutral + 理由 |
| 2 | **PM Agent** | **综合与加权**，不做独立研究 | 初步建议：ticker + direction + size |
| 3 | **Risk Officer Agents**（Drawdown / Volatility / Liquidity / Concentration） | 各管**一个**风险维度，可否决 | approve / 约束规模 / veto |

> 💡 三层 + 八个角色（4 analyst + 1 PM + 4 risk officer，其中 PM 单列）= 考试画图题。

---

## 第 46 页 · Analyst Agents (Diverse Perspectives)（分析师 agents：多元视角）

每个 analyst 用**自己的视角独立**分析目标股票，产出 thesis（bullish/bearish/neutral + 推理）。**关键在于：每个 agent 有不同的数据访问与不同的评价标准**——这才让它们**有分歧地产出（disagree productively）**，而不是互相附和。

| Agent | 视角（Lens） | 数据 | 典型问题 |
|---|---|---|---|
| **Value Analyst** | 基本面 | 财务报表 | 相对内在价值便宜吗？P/E、P/B、DCF、margin of safety |
| **Growth Analyst** | 扩张 | 财务 + 行业报告 | 收入/盈利在增长吗？TAM、competitive moat |
| **Momentum Analyst** | 价格行为 | 价格/成交量 | 趋势向上还是向下？技术信号 |
| **Macro Analyst** | 宏观背景 | 宏观指标、新闻 | 利率/周期是否有利于该行业？ |

> 💡 四类 analyst 的 **lens + 数据 + 问题**三列，正好是 group project 要写具体的部分。

---

## 第 47 页 · Portfolio Manager Agent（组合经理 agent）

PM **综合所有 analyst 的 theses**，对它们**加权**（例如：降息周期中给 growth analyst 更高权重；深价值股则给 value analyst 更高权重），形成**初步仓位建议**（**ticker + direction + size**）。

**Aggregator — Not Analyst（是聚合者，不是分析师）**：PM 的职责是**综合与加权**，不是做独立研究。

> 💡 判断题高频：**PM 不做独立研究**。

---

## 第 48 页 · Risk Officer Agents (Each One Dimension, with Veto)（风险官 agents：一人一维度，带否决权）

这是"委员会"与"一群评论家（panel of pundits）"的分水岭。每个 risk officer **只拥有一个风险维度**，可以约束或杀掉这笔交易：

| Risk officer | 检查什么 | 权力 |
|---|---|---|
| **Drawdown Risk Officer** | 是否会把组合 MDD 推过上限？ | **VETO** |
| **Volatility Risk Officer** | 组合波动是否会超预算？ | 要求**更小仓位** |
| **Liquidity Risk Officer** | 压力下股票流动性够不够退出？ | 标记**流动性差的股票** |
| **Concentration Risk Officer** | 是否造成行业/资产**过度集中**？ | **限制配置比例 %** |

**决策规则**：所有 risk officers 通过 → **execute**；任何一个否决 → **reduce size 或 reject**。否决权是**安全刹车（safety brake）**，防止一个自信的 PM 因单一想法**炸掉整个组合（blow up the book）**。

> 💡 四个 officer 的权力并不相同：只有 Drawdown 是硬 VETO，其余是"降规模/打标/设上限"。

---

## 第 49 页 · 章节扉页

**Reference Systems**——真实存在的参考系统。

> 💡 这个范式已有真实系统落地，不是思想实验。

---

## 第 50 页 · Real Systems Instantiating This Paradigm (Part 1)（真实系统一）

这不是科幻——已有多个真实系统实现了该范式：

- **AlphaAgents（arXiv 2508.11152）**：面向**股票研究与组合管理**的**基于角色的多智能体系统**。核心主张：**角色专门化（role specialization）提升决策质量**——把"分析"与"决策"拆给不同的专家 agent，优于单个 monolithic LLM。
- **AI Hedge Fund（virattt/ai-hedge-fund）**：最流行的**教学示例**。agents 模仿著名投资者：**Ben Graham agent**（深价值）、**Warren Buffett agent**（合理价格买质量）、**Phil Fisher agent**（成长/scuttlebutt）。每个 agent 投 **buy/sell/hold**——非常适合教学，因为每个 prompt 都编码了一套**连贯且有名字的投资哲学**。

> 💡 两个名字 + 各自一句主张：AlphaAgents = 角色专门化；AI Hedge Fund = 名人风格投票。

---

## 第 51 页 · Real Systems Instantiating This Paradigm (Part 2)（真实系统二）

- **"Signal or Noise"（arXiv 2604.17327）**：直接检验一个学术问题——**多智能体 LLM 的 strong-buy 推荐能否跑赢随机选股？** 结论：**能**——多智能体 ensemble 识别出的 alpha 超出经典因子模型的捕捉范围；但**signal-to-noise ratio 很重要**——**聚合与过滤（aggregation and filtering）必不可少**。
- **Layered-Memory Multi-Agent Framework（Joshi-Bongale）**：给 agents 配**分层记忆**（短期市场状态 + 长期经验教训）用于股票/基金交易——记忆让 agent 能想起"**上次 Fed 加息 75bp 时，这个因子表现不佳**"。

> 💡 记住结论："能跑赢随机，但不是免费的——需要聚合过滤"。

---

## 第 52 页 · 章节扉页

**Designing the Debate**——设计"辩论"本身才是难点。

> 💡 让 agents 真吵架，而不是互相附和——这是设计难点。

---

## 第 53 页 · Rules for Productive Dissent（让分歧有产出的规则）

最难的设计问题：让 agents **有分歧地产出**，而不是**塌缩成共识回声（consensus echo）**——因为它们常常共享同一个 LLM backbone。

1. **给每个 agent 不同的数据和不同的标准**——value analyst 看财报，momentum analyst 只看图；它们**必须**得出不同结论；
2. **设置明确的"devil's advocate"角色**——有一个 agent 的职责就是**反对正在形成的共识**；
3. **要求每个 agent 陈述反对自己论点的理由**——强制智识上的诚实；
4. **使用结构化辩论协议**：**Round 1（独立分析）→ Round 2（互相批评）→ Round 3（修正建议）**。

> 💡 四条规则 + 三轮协议，简答题按点给分。

---

## 第 54 页 · The Correlated-Error Risk（相关误差风险）

如果每个 agent 都用同一个底层 LLM（如全是 GPT-4），它们可能共享**相同的盲点**——例如在阅读生物科技公司申报文件时的系统性偏差。

**缓解措施**：不同 agent 用**不同模型家族**；用**不同 prompting 风格**；注入**"随机化人格（randomized persona）"**，避免所有 agent 用同一种方式推理。

> 这是**组合风险中相关性概念的多智能体类比**：一个**完全相关**的 agent 委员会，**没有任何分散化收益**。

> 💡 本讲最漂亮的一句类比，讨论题/简答题都能用。

---

## 第 55 页 · 章节扉页

**Case Study 3: Multi-Agent Committee on AAPL**——完整走一遍三层架构。

> 💡 AAPL 案例：4 位 analyst → PM → 4 位 risk officer 的完整闭环。

---

## 第 56 页 · Round 1 — Independent Analyst Theses（第一轮：独立论点）

**Part C 的核心案例。**

| Analyst | Thesis | 观点 |
|---|---|---|
| **Value** | P/E ∼30，高于 10 年均值；DCF 公允价值 ∼$160 → 合理到略贵 | **NEUTRAL** |
| **Growth** | Services 收入 ∼20% 复合增长，margin 扩张，生态锁定强 → 增长被低估 | **BULLISH** |
| **Momentum** | 站上 200 日均线，MACD 为正，相对行业强度为正 → 趋势完好 | **BULLISH** |
| **Macro** | Fed 仍鹰派，强美元打击海外收入，消费走弱 → 逆风 | **BEARISH** |

> 💡 记分布：**两多、一中、一空**——这正是后面 PM "加权"的素材。

---

## 第 57 页 · Round 2 (Critique) & PM Synthesis（第二轮批评与 PM 综合）

**Round 2 — Critique**：Value 质疑 Growth："Services 增长是真的，但**已经反映在估值倍数里**。" Growth 反驳 Macro："AAPL 的 services 是**抗衰退**的。" 辩论浮现出核心张力：**贵估值 vs 可持续增长**。

**PM 综合**："两多、一中、一空。增长逻辑可持续，但 **Macro 的利率逆风对 mega-cap 是真实的**。→ 初步建议：**modest overweight，3% 仓位**（相对 5% 的中性上限）。"

> 💡 PM 的动作 = **数票 + 权衡 + 打折**（因为宏观逆风，把仓位压到 3%）。

---

## 第 58 页 · Risk-Officer Review & Final Decision（风险官审查与最终决策）

| Officer | 检查 | 结论 |
|---|---|---|
| **Volatility** | AAPL beta ∼1.2；3% 仓位使组合波动在预算内 | **Approve，但上限 3%** |
| **Liquidity** | 全球流动性前五的股票 | **Approve** |
| **Concentration** | 组合已有 18% tech；加 3% AAPL → 21%，低于 25% 上限 | **Approve** |
| **Drawdown** | 仓位足够小：AAPL 跌 30% 也只损失组合 **0.9%**（3% × 30%） | 在 MDD 预算内，**Approve** |

**Final Decision：Execute 3% Overweight AAPL**。

**两个教训**：① **辩论防止了追高**（value 与 macro 对 growth 的热情形成推回）；② **risk officers 把交易规模定到"错了也能活"**。"Signal or Noise" 的发现在此适用：这类 ensemble **可以跑赢随机选择——但前提是辩论真实、风险刹车有效**。

> 💡 0.9% 这笔账要会算；本案例 = 全讲四部分的浓缩演示。

---

## 第 59 页 · 章节扉页

**Part D — LLM-Driven Risk Control**：**价格模型完全看不到的文本风险信号**。

> 💡 价格是结果，文本是先行信号。

---

## 第 60 页 · Beyond Price-Based Risk Metrics（超越基于价格的风险指标）

Part A 的风险指标（VaR、CVaR、MDD）都是**基于价格（price-based）**的——它们**只有风险已经反映到价格上之后**才看得见。

**LLM 带来的是文本信号（text-based risk signals）**——价格模型**完全错过**的那一类。

> 💡 Part D 的定位句：**price-based 看结果，text-based 看苗头**。

---

## 第 61 页 · 章节扉页

**Earnings Call Tone — Crash Risk**——电话会语气 → 崩盘风险。

> 💡 同一份电话会记录：词频模型看词，LLM 看行为。

---

## 第 62 页 · Beyond Surface Sentiment（超越表面情绪）

朴素情绪模型只会**数电话会记录里的正负词**。LLM 读的是**管理层的微妙行为**：

- **Evasiveness（回避）**——躲开分析师的直接提问；
- **Excessive hedging（过度对冲措辞）**——"we expect"、"approximately"、"going forward"、"we are comfortable with..." 激增；
- **Increased uncertainty language（不确定性语言增加）**——更多条件句、更少明确承诺。

**研究发现**：LLM 从电话会记录中抽取的 **"management uncertainty factor"**，与**未来股价崩盘风险**相关——**管理层往往在数字变差之前就知道情况在恶化，而这种认知会从语气中泄漏出来**。传统情绪分析**系统性地漏掉**这一点。

> 💡 三个语言特征 + 一句"管理层先知道，语气先泄漏"。

---

## 第 63 页 · 章节扉页

**ESG + Knowledge-Graph Supply Chain Risk**——ESG + 知识图谱的供应链风险。

> 💡 风险沿供应链走，图比单股分析看得远。

---

## 第 64 页 · The Contagion Scenario（传染情景）

讲的是**传染风险（contagion risk）**——风险沿**供应链链接**从一家公司跳到另一家。

**情景**：新闻曝出 **Company A**（一家供应商）犯下严重的环境违规。

1. **LLM 事件抽取**——读新闻，抽出：entity = A，event type = environmental violation，severity = high；
2. **Knowledge-Graph（KG）传播**——KG 记录 **A 供应 B 40% 的部件** → B 的供应链现在有风险 → **在市场定价之前**减持 B；
3. **Multi-hop cascade（多跳级联）**——A 的违规 → B（直接客户）→ C（B 的客户）——风险沿链条传播。

> 💡 三步：**抽取 → 图传播 → 多跳**；40% 这个数字是触发器。

---

## 第 65 页 · Why This Matters（为何重要）

**单股分析的盲点**：单股分析看着 A 说"A 有麻烦"，**看不到 B 和 C 通过 A 也有麻烦**。

**KG + LLM 的组合**捕捉到了**价格模型和单名分析都捕捉不到**的传染。这是 LLM（entity/relation extraction）+ 图方法的**前沿应用**。

> 💡 盲点 = 只看单只股票；解法 = 图上的关系推理。

---

## 第 66 页 · 章节扉页

**Case Study 4: Earnings Call Tone — Crash Risk**——语气信号案例。

> 💡 词频模型打 neutral 的电话会，如何提前预警 −18%。

---

## 第 67 页 · The Signal that Word-Count Sentiment Missed（词频情绪漏掉的信号）

某 CEO 的季度电话会，与之前几个季度相比：

- **Margin 下滑**；分析师问**为什么**时，CEO **回避**，转向"我们聚焦长期"；
- **对冲措辞**（"we expect"、"approximately"、"seasonally adjusted"）比此前电话会**上升 40%**；
- 对前瞻指引问题的**直接回答**被替换成"我们下季度会提供更多细节"。

**结果**：词频情绪模型给这次电话会打 **"neutral"**（没有灾难性的负面词）。LLM 则标记出**升高的 management uncertainty** → 一个 **crash-risk signal**。**数周后**，公司**预先公告业绩不及预期**；股价**下跌 18%**。

> 💡 三个细节（回避、+40% hedging、拒绝给指引）+ 结果 **−18%**。

---

## 第 68 页 · 章节扉页

**Case Study 5: ESG + Knowledge Graph Supply Chain Risk**——供应链级联案例。

> 💡 A 的违规如何传导到 B、C——以及如何在定价前减仓。

---

## 第 69 页 · The Cascade（级联）

**设置**：**Company A**（特种化学品供应商）收到 **EPA 违规通知**。新闻**数小时内**进入 A 的股价（A 跌 **12%**）。但是：KG 显示 **A 供应 Company B 关键聚合物部件的 40%**；**B 在 6–9 个月内没有合格的第二供应源**；而 **B 又供应 Company C**（一家大型汽车 OEM）。

**结果**：LLM+KG 风险系统**在卖方更新 B 的模型之前**就标记 B（以及较弱的 C）需要减仓。**Risk officer 将 B 的仓位砍半**。随后一个月，随着 B 的 margin guidance 下修，**B 跌 9%**——agent 委员会因为**推理了传染、而不只是 A**，避开了一大部分损失。

> 💡 关键数字：**A 供应 B 的 40%、B 无替代源 6–9 个月、B 最终 −9%**。

---

## 第 70 页 · 章节扉页

**PIXIU / FinMA Benchmark**——部署之前先测评。

> 💡 没有基准测试的 LLM 风控，等于没有回测的量化策略。

---

## 第 71 页 · Measure Before You Trust（先测量，再信任）

部署任何 LLM 风险系统之前，必须**测量它在金融任务上的水平**。

**PIXIU（chancefocus/PIXIU）**：一个综合性的**金融 LLM 基准**，带有覆盖**forecasting、classification、extraction、generation** 的任务数据集；明确包含**风险相关任务**：**credit scoring、financial fraud detection、extreme sentiment/crisis identification**。**FinMA** 是配套的**微调模型线**；**PIXIU 是评估框架（evaluation harness）**。

纪律：在信任 LLM 去读电话会（§13）或抽取 ESG 事件（§14）之前，先让它在 **PIXIU 的风险任务子集**上跑分。**如果在 financial fraud detection 上得分很差，就不要把它用于该用途**。**Evaluate before you deploy**——与量化模型回测同等的纪律。

> 💡 别混淆：**FinMA = 模型，PIXIU = 评测框架**。

---

## 第 72 页 · 章节扉页

**Deployed Example: DojoAgents**——已落地的例子。

> 💡 零售端已能上传持仓截图，做多模态风险诊断。

---

## 第 73 页 · Multimodal Portfolio Risk Diagnosis（多模态组合风险诊断）

Part C 与 Part D 的想法**不只是研究**——已在开源产品中出货。**DojoAgents**（Lecture 6 §7.3b 介绍过）实现了**面向零售用户**的组合风险控制版本：

- **Multimodal intake**——上传持仓截图；agent 识别 **40+ 个持仓**，无需手工录入；
- **Risk re-grouping**——按**市场、行业、供应链位置**重新分组——揭示许多看似"分散"的持仓其实是**同一个赌注**；
- **Risk diagnosis**——标记**过度集中、主题暴露重叠、缺少防御性资产**——正是 **Concentration 与 Drawdown Risk Officers（§10）**的工作；
- **Action loop**——提出再平衡建议，并**持续跟踪**新组合。

> 💡 四个功能正好对应本讲四部分：结构化数据 + 多维风控 + LLM 推理 + 行动闭环。

---

## 第 74 页 · The Lesson（教训）

生产环境中的风险 agents 之所以成功，是因为把本讲的各块拼在一起：**结构化组合数据（Part A 指标）+ 多维风险检查（Part C risk officers）+ 对非结构化上下文的 LLM 推理（Part D）**——并且放在**防止数字幻觉的 guardrails（护栏）**之内。

> 💡 **guardrails** 是关键词：LLM 可以推理，但数字必须来自结构化数据。

---

## 第 75 页 · 章节扉页

**Summary**——小结。

> 💡 标尺、AI 改造、agent 委员会、文本风控——四条线在此汇合。

---

## 第 76 页 · Key Takeaways (Part 1)（要点一）

1. 经典组合理论（**MPT/MVO/CAPM**）与风险/绩效指标（**VaR、Sharpe、Sortino**）是你的**评估标尺**——它们定义了"好"是什么；
2. **MVO 的 error-maximization 缺陷正是 AI 的入口**：**ML 改进输入**、**RL 直接优化权重**、**LLM 补充定性宏观推理**；
3. 前沿是**多智能体投资委员会**：多元 analyst agents 辩论、PM 综合、带**否决权**的 risk-officer agents 让系统活下去。

> 💡 三条 = Part A + Part B + Part C。

---

## 第 77 页 · Key Takeaways (Part 2)（要点二）

4. LLM 打开了**文本风险信号**（earnings-call tone、ESG + knowledge-graph contagion），这是**价格模型看不见**的；
5. **永远先评估你的 LLM（PIXIU/FinMA）再让它管风险**——与量化模型回测同等纪律；
6. **生产系统（DojoAgents）把四部分合为一体**——结构化指标、多维风险检查、LLM 推理，全部置于**anti-hallucination guardrails** 之内。

**收束句**：经典理论给我们**标尺**；AI 给我们**更好的估计、优化，以及人类投委会的可扩展代理**。

> 💡 六条 takeaway 与四个学习目标严格对应，考前扫这一段最快。

---

## 第 78 页 · Further Reading（延伸阅读）

| 资源 | 主题 |
|---|---|
| **AlphaAgents（arXiv 2508.11152）** | 面向选股的基于角色多智能体系统 |
| **AI Hedge Fund（virattt/ai-hedge-fund）** | 名人投资者风格委员会，开源、适合教学 |
| **"Signal or Noise"（arXiv 2604.17327）** | 多智能体 LLM 选股能否跑赢随机？ |
| **FinMem（arXiv 2311.13743）** | 分层记忆交易 agents → Lecture 10 |
| **PIXIU / FinMA（chancefocus/PIXIU）** | 含风险任务的金融 LLM 基准 |
| **Grinold & Kahn, Active Portfolio Management** | IR、alpha、residual risk 的经典量化教材 |
| **Markowitz (1952), Portfolio Selection** | MPT 原始论文 |
| **FinRL（AI4Finance-Foundation/FinRL）** | 组合优化的 RL |

**End of Lecture 9. Next: Lecture 10 — Automatic Research & Investment using AI（Quant 3.0）。**

> 💡 三个 arXiv 号 + 一个 GitHub 仓，选择题可能直接问"哪个是 benchmark"。

---

## 第 79 页 · 章节扉页

**Open Exercises & Discussion (Optional)**——开放练习与讨论（可选）。

> 💡 可选练习：一道架构设计（对 group project 有用）+ 两道开放讨论。

---

## 第 80 页 · Design an Investment-Committee Agent Topology（设计投委会 agent 拓扑）

**可选设计练习——课后自己完成。**

**任务**：选一个情景（例如"一只必须把相对 S&P 500 的 tracking error 控制在 5% 以内的美国大盘股基金"），并指定：

1. **哪些 analyst agents**——命名，给每个一个 lens 和一个数据源；
2. **它们的数据源**——**要具体**（例如"**Value Analyst reads SEC 10-K filings via EDGAR API**"）；
3. **辩论协议**——几轮、每轮做什么、谁扮演 devil's advocate；
4. **哪些 risk officers，以及各自的否决条件**——例如"**Concentration Officer vetoes if any sector exceeds 25%**"。

画出架构，并**论证为什么选这些 agent 而不是别的**——**设计选择编码了你认为 alpha 与风险究竟在哪里的判断**。

> 💡 这道题就是 group project 架构的模板（见文末专节）。

---

## 第 81 页 · Two Questions（两个讨论问题）

**Q1：Bias Reduction vs. Correlated Errors**——多个 LLM agents 辩论时，是**降低偏差**（多元视角相互抵消），还是**放大共同盲点**（都建在同一个 LLM backbone 上）？如何设计**有产出的分歧**？**类比**：完全相关的股票组合没有分散化收益；完全相关的 agent 委员会同样没有。

**Q2：The Future of Asset Management?**——多智能体投委会是否是 5–10 年后资产管理真实运作方式的缩影？**提示**：监管问责（regulatory accountability）、LP 对"agent 委员会"的信任、每天运行大量 agents 的**延迟/成本**、共享 backbone LLM 带来的**模型风险**。

> 💡 Q1 的答案骨架 = 第 53–54 页；Q2 的答案骨架 = 提示里的四个词。

---

## 第 82 页 · Appendix（附录）

课程信息参考资料——**不考内容（not examined content）**。

> 💡 可以跳过。

---

## 第 83 页 · Appendix A: Exam Review Checklist（考点清单扉页）

正式考点清单的扉页。

> 💡 下一页才是内容。

---

## 第 84 页 · Appendix A — Exam Review Checklist（L9 期末考点清单）

**本讲内容属于期末考试范围**（**11 月 30 日，权重 40%，覆盖 L6–L10**——完整考试结构见 Lecture 1 附录 A）。

| § | 可考内容 |
|---|---|
| **1–3** | Systematic vs. idiosyncratic risk、diversification；MPT/efficient frontier；MVO 及其 error-maximization 缺陷；CAPM、beta、factor investing |
| **4–5** | VaR vs. CVaR、MDD、tracking error；Sharpe、Sortino、Treynor、Information Ratio 及各自适用场景 |
| **6–8** | ML 估计 µ/Σ；RL 直接组合优化（state、action、reward）；LLM 动态配置与分工 |
| **9–12** | 多智能体投委会架构（analyst、PM、risk-officer 三层）；参考系统；设计有产出的分歧 |
| **13–15** | Earnings-call tone 作为崩盘风险信号；ESG + knowledge-graph 传染；PIXIU/FinMA 基准的用途 |

**题型**：多项选择 + 1–2 道简答（QA）题（期末，1.5 小时）。

> 💡 五个分组覆盖全讲，下一节把它们展开成 15 个小节。

---

## 本讲考点（依据 Appendix A，展开为可考小节 1–15）

> 说明：Appendix A 只给出 5 个分组（1–3 / 4–5 / 6–8 / 9–12 / 13–15）。结合正文里的分节引用（第 8 页的 §4、第 31 页的 §6–8、第 71 页的 §13–14、第 73 页的 §10），可还原 15 个小节如下；页码为对应精读页。

| § | 可考内容 | 页码 | 必背一句话 |
|---|---|---|---|
| **1** | Risk & return：r 与 σ² 的定义；E[r] vs r̄；systematic vs idiosyncratic risk；diversification | 8–10 | 特质风险可用 **∼30+ 只不相关**资产分散掉，系统风险不能 |
| **2** | MPT / efficient frontier；MVO 的两种表述；**error maximization** | 12–15 | MVO 把输入的估计噪声**放大成极端集中权重** |
| **3** | CAPM、SML、beta；factor investing 与 smart beta | 17–18 | β 衡量对市场的敏感度；**SML 上方 = 低估** |
| **4** | VaR vs CVaR、MDD、tracking error；方差的局限（fat tails、asymmetry） | 20–22 | **VaR 只画线，CVaR 才回答尾部多深** |
| **5** | Sharpe / Sortino / Treynor / Information Ratio 及适用场景；高 Sharpe 掩盖尾部风险 | 24–25 | 分母分别是 **σ_p / σ_d / β_p / tracking error**；**禁止单一指标** |
| **6** | ML 估计 µ/Σ：return forecasting；shrinkage、factor models、deep covariance | 33 | 协方差三招：**shrinkage / factor model / deep covariance** |
| **7** | RL 直接优化：state、action、reward；相对 predict-then-optimize 的优势 | 35–36 | reward 常用 **differential Sharpe ratio**；这就是 **FinRL portfolio mode** |
| **8** | LLM 动态配置：FinGPT robo-advisor 三步；division of labor | 38–39 | **LLM 定 regime/大类，quant optimizer 定个券**；不让 LLM 直接预测价格 |
| **9** | 多智能体投委会理念：委员会为何有效 | 43 | 两大支柱：**diverse perspectives + independent risk oversight** |
| **10** | 三层架构：analyst → PM → risk officers（veto） | 45–48 | 四个 officers 各管一个维度，**Drawdown 拥有硬 VETO** |
| **11** | 参考系统：AlphaAgents、AI Hedge Fund、Signal or Noise、layered memory | 50–51 | **role specialization** 优于单一 monolithic LLM；ensemble 能跑赢随机但要聚合过滤 |
| **12** | 设计 productive dissent：四条规则、三轮协议、correlated-error risk | 53–54 | 同一 backbone → 同一盲点；**完全相关的 agent 委员会无分散化收益** |
| **13** | Earnings-call tone → crash risk | 62、67 | **evasiveness + hedging↑ + 不确定性语言** = management uncertainty 信号 |
| **14** | ESG + knowledge-graph 供应链传染 | 64–65、69 | **LLM 事件抽取 + KG 多跳传播**，在市场定价前减仓 |
| **15** | PIXIU/FinMA 基准 | 71 | **部署前先测评**，与量化模型回测同等纪律；FinMA 是模型、PIXIU 是 harness |

**四个最容易设陷阱的反差**：

- **VaR vs CVaR**：VaR 说"95% 概率损失 < $1M"，但**不说过线后多惨**；CVaR = 最差 (1−confidence)% 尾部的**平均损失**；
- **Sharpe vs Sortino**：一个**稳定小赚 + 偶发巨亏**的卖期权策略，Sharpe = 1.33、Sortino = 0.67——**高 Sharpe 可以完全掩盖尾部风险**；
- **PM vs Analyst**：PM 是 **aggregator**，只做综合与加权，**不做独立研究**；
- **agent 的数量 ≠ 分散化**：共享同一 LLM backbone 的委员会，与完全相关的股票组合一样，**没有分散化收益**。

---

## 本讲与 group project 的关系

原文对项目设计有三处**可直接引用**的支撑，均不需要额外发挥：

**1）多智能体投委会架构可作为项目架构参考。**
第 45 页给出的三层拓扑（**analyst agents → PM agent → risk-officer agents → final decision**）就是一份现成的系统架构图：第一层按不同 lens 独立产出 thesis，第二层由一个 PM 角色**综合加权**并给出 ticker + direction + size，第三层由各管一个维度的 risk officers 做**约束与否决**（第 48 页：全票通过才 execute，任一否决则 reduce/reject）。第 43 页说明了这样设计的理由——**多元视角 + 独立风险监督**，且相对人类委员会**可扩展**（人类一周一次，agents 可每日全市场运行）。第 80 页的设计练习更直接要求"画出架构并论证为什么选这些 agent 而不是别的"，与项目里"架构 + 设计理由"的写法同构。

**2）analyst agents 的数据源要具体。**
第 46 页已给出四类 analyst 的 lens 与数据类别（Value → 财务报表；Growth → 财务 + 行业报告；Momentum → 价格/成交量；Macro → 宏观指标与新闻）。第 80 页则把要求提得更硬：数据源**必须具体**，原文示范为"**Value Analyst reads SEC 10-K filings via EDGAR API**"。也就是说，项目文档里不能只写"uses financial data"，而要写到**具体接口/文件/字段**这一层。

**3）anti-hallucination guardrails。**
第 74 页总结生产系统的成功要素：**结构化组合数据（Part A 指标）+ 多维风险检查（Part C risk officers）+ 对非结构化上下文的 LLM 推理（Part D）**，全部置于**防止数字幻觉的 guardrails** 之内；第 77 页再次把"inside anti-hallucination guardrails"列为第 6 条 takeaway。落地含义与第 39 页的分工一致：**LLM 负责 regime / sentiment / 文本事件判断，数值与计算交给结构化数据与优化器**，不要让 LLM 直接生成价格或风险数字。

**可额外借用的一条**：第 71 页的评估纪律——先在你的任务子集上测量 LLM（PIXIU/FinMA 式的思路），再决定是否让它承担该风险任务；第 53 页的三轮辩论协议（独立分析 → 批评 → 修正）也可直接写进项目的 agent 交互流程。除此之外，原文没有对 group project 提出其他要求。
