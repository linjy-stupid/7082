# Lecture 8 逐页中文精读

**原文件**：`lecture_08.pdf`（67 页 PDF = 53 张编号幻灯片（页脚 x/53）+ 14 张章节分隔页/标题页，无页码；PDF 密码 `student`）
**课程**：AI × Finance｜Lecture 8 of 10｜Dr. Z.C. Lin｜Week 8｜Module III · Applications（L8–L10）**第 1 讲（共 3 讲）**
**用途**：期末复习（**期末 11 月 30 日，权重 40%，覆盖 L6–L10**；术语保留英文，考试为英文选择题 + 1–2 道简答）

> 📌 **本讲定位**：Module III 的开篇。先用"广角"扫过 **AI 在金融业的六条业务线**（credit、fraud、robo-advisory、InsurTech、payments、RegTech）与 **GNN 反欺诈/反洗钱**，再用"长焦"盯住 **算法交易（algorithmic trading）**——从 VWAP/TWAP/HFT 的执行机制，一路深入到 **强化学习（RL）** 的组件、Bellman 方程、三类方法、训练技巧、结构性局限，最后落到开源库 **FinRL**。全讲的底色：**AI 已是横跨整个金融业的水平层（horizontal layer），但每条业务线有自己的数据、风险与 make-or-buy 经济学；生产里有效的与仍停留在研究阶段的，要分清楚**。

---

## 第 1 页 · 封面

**AI Across the Finance Industry: Algorithmic Trading & Reinforcement Learning** — AI 跨越金融业：算法交易与强化学习

Lecture 8 of 10｜Dr. Z.C. Lin｜Week 8｜Dept. of Electrical and Electronic Engineering, HKU

> 💡 标题三块拼图：**行业全景（Across the Finance Industry）+ 算法交易（Algorithmic Trading）+ 强化学习（RL）**——正是本讲的三段结构。

---

## 第 2 页 · Lecture Overview（本讲概览）

**位置**：Module III – Applications（L8–L10），**三讲中的第 1 讲**。

本讲做两件事：

1. **把镜头拉宽**——从单一 ML 技术扩展到**整个行业图景**（one ML technique → the entire industry landscape）；
2. **再钻深**——深入**算法交易机制**与**强化学习**。

**反复出现的主题（The Recurring Theme）**：

- AI 如今是横跨整个金融业的**水平层（horizontal layer）**，不再是 quant（量化分析师）的专属细分领域；
- 但每条业务线有**自己的数据、自己的风险、自己的 make-or-buy 经济学**；
- 讲者承诺**诚实区分**：什么是生产环境里真正work的，什么还只是研究（what works in production and what is still research）。

> 💡 一句话记住："AI 是全行业的地板，不是某一间房的家具"——但每间房的地板厚度不同。

---

## 第 3 页 · Learning Objectives（学习目标）

学完本讲，你应当能够：

1. **把 AI 应用映射到主要金融业务线**——credit（信贷）、fraud（欺诈）、advisory（投顾）、insurance（保险）、payments（支付）、RegTech（监管科技）；
2. **理解算法交易机制**——VWAP / TWAP / HFT，以及 **urgency–impact trade-off**（紧迫性与市场冲击的权衡）；
3. **掌握交易的强化学习基础**——agent、state、action、reward、**Bellman 直觉**、value / policy / **actor-critic**；
4. **评估 AI 在金融中的 build-vs-buy 决策**——何时自研、何时买厂商方案。

> 💡 四个目标 = 本讲的四块内容：业务线全景（目标 1）、执行算法（目标 2）、RL 理论（目标 3）、工程经济学（目标 4，落在第 64 页讨论题）。

---

## 第 4 页 · Lecture Roadmap（本讲路线图）

**两个 Zoom（Two Zooms）**：

| 阶段 | 内容链条 |
|---|---|
| **Zoom out（拉远）** | Business-line map（业务线地图）→ **GNN for fraud/AML** |
| **Zoom in（拉近）** | Algo trading（算法交易机制）→ **RL fundamentals** → **RL method types** → **RL training tips** → **RL limitations** → **FinRL** |

原文表述：先拉远看整个行业（业务线与 GNN 反欺诈），再拉近专门看交易（算法机制 → RL：基础 → 方法 → 实用技巧 → 局限 → 把一切串起来的开源库）。

> 💡 这是"漏斗式"结构：**行业（宽）→ 交易（窄）→ RL（更窄）→ FinRL（落地）**。

---

## 第 5 页 · 章节分隔页

**AI Business-Line Panorama** — AI 业务线全景

（正式内容从第 6 页开始，共 5 条业务线 + 1 张汇总表。）

---

## 第 6 页 · Credit Scoring（信用评分）

**What AI does（AI 做什么）**：ML 模型——尤其是**梯度提升树（gradient-boosted trees：XGBoost、LightGBM）**，并越来越多用神经网络——估计借款人的**违约概率（PD, probability of default）**。

**输入不再局限于 FICO 式传统变量**，而加入 **alternative data（另类数据）**：交易模式、房租/水电缴费记录、就业稳定性。

**Value Created（创造的价值）**：

- 决策从**数天缩短到数秒**；
- 更准确的风险定价；
- **financial inclusion（金融普惠）**——**thin credit files（薄信用档案）** 人群可以按**行为**而非**历史**被评分。

**Key Risk — Bias & Fairness（关键风险：偏差与公平）**：

- 用历史数据训练的模型会**继承历史歧视**（原文举例 **redlining**，即历史上对特定社区的拒贷做法）；
- **另类数据可能成为受保护属性的代理变量（proxy for protected attributes）**；
- 监管方 **US CFPB**（美国消费者金融保护局）与 **EU AI Act** 正在积极介入（actively circling this space）。

> 💡 信贷评分是"另类数据创造价值"与"另类数据制造歧视"同一枚硬币的两面——**普惠与代理歧视只隔一层**。

---

## 第 7 页 · Fraud Detection — An AI Arms Race（欺诈检测：一场 AI 军备竞赛）

**The 2025 Reality（2025 年的现实）**：据行业报告（**Feedzai 2025**），**超过一半的欺诈如今涉及 AI 或 deepfake**——包括：

- **voice cloning**（语音克隆）冒充高管；
- 用窃取的 **PII**（个人身份信息）合成 **synthetic identities**（合成身份）；
- **deepfake 视频绕过 video KYC**（远程视频身份核验）。

**The Defense Stack（三层防御）**：

| 层 | 方法 | 作用 |
|---|---|---|
| ① | **Generative AI detectors** | 识别合成语音/视频中的不一致：**artifacts（伪影）、spectral anomalies（频谱异常）、lip-sync mismatch（唇音不同步）** |
| ② | **Graph Neural Networks（GNN，§2 详讲）** | 检测**串通账户组成的团伙（rings）**，而不只是孤立的坏交易 |
| ③ | **Real-time transaction-pattern scoring** | 流式 ML 在**毫秒级**标记异常，常常在钱离开银行之前 |

**The Arms Race（军备竞赛）**：检测变强 → 攻击者的生成也变强——**持续循环**。这就是为什么欺诈检测是少数**必须让模型永久重训（perpetual retraining）**的领域之一。

> 💡 三层防御对应三种攻击面：**假脸（检测器）→ 假身份网络（GNN）→ 假交易（实时评分）**。

---

## 第 8 页 · Robo-Advisory（智能投顾）

**What it is（是什么）**：基于用户**风险画像（risk profile）**的自动化组合配置。

- **第一代**（Betterment、Wealthfront）用 **mean-variance optimization（均值-方差优化）**；
- **当前一代**越来越多叠加 **LLM-powered advice（LLM 驱动的建议，回顾 L6）**，用户可以自然语言提问，例如 "Should I rebalance into bonds?"（我该不该把仓位再平衡到债券？）

**Value Created — Democratization（价值：民主化）**：

- 过去需要 **$1M+ 门槛**的财富管理，如今 **$100** 即可获得；
- 费率更低：**0.25% vs 人工投顾的 1–2%**；
- 有纪律、**无情绪（emotion-free）**的再平衡。

**Key Risk（关键风险）**：

- **Suitability（适当性）**——**不得推荐不适合的产品**；
- **Over-trust（过度信任）**——用户可能把 LLM 自信的回答当成"金融福音"，而它充其量只是一个 **heuristic（启发式规则）**。

> 💡 投顾的 AI 化把"门槛"降下来了，却把"信任风险"顶上去了——**suitability 是合规底线，over-trust 是行为风险**。

---

## 第 9 页 · Insurance Tech（InsurTech，保险科技）

AI 贯穿保险**价值链（value chain）**的四个环节：

| 环节 | AI 应用 |
|---|---|
| **Underwriting（承保）** | ML 定价，纳入 **telematics（车联网驾驶行为）**、**wearables（可穿戴设备健康数据）**、**satellite imagery（卫星影像：作物/洪水风险）** |
| **Claims processing（理赔）** | **计算机视觉**从照片/无人机影像评估车损、屋顶损伤；**NLP** 对理赔文本做分诊（triage）；低严重度案件**直通处理（straight-through processing）** |
| **Dynamic pricing（动态定价）** | **usage-based insurance**（"pay how you drive"，按驾驶行为付费） |
| **Fraud detection（反欺诈）** | 与银行业相同的 **GNN/异常检测栈** |

**Key Risk — Adverse Selection & Fairness（逆向选择与公平）**：

- 如果**定价过度个性化（too personalized）**，**低风险池（low-risk pool）会萎缩**，保险的**风险汇聚（risk pooling）**功能就会破裂；
- 监管方会**限制定价的颗粒度（cap how granular pricing can get）**。

> 💡 保险的本质是"风险池"，AI 越能把人分开定价，池子就越薄——**精算精度与保险功能天然对立**。

---

## 第 10 页 · Payments & RegTech（支付与监管科技）

**Payments（支付）**：

- **每笔交易实时欺诈评分**——决定 **allow / challenge / block**（放行/挑战/拦截），**同步于刷卡（synchronous with the swipe）**，**<100 ms** 内完成；
- **AI routing**——为每笔交易选择**最便宜/最快**的通道（rail）；
- **跨境（cross-border）**：**FX optimization（外汇优化）** 与 **sanctions screening（制裁名单筛查）**，用 NLP/实体消解（entity resolution）。

**RegTech（Regulatory Technology，监管科技）**：

- **Automated compliance monitoring**——NLP 把法规**映射到政策（mapping regulations to policies）**；
- **AML**——GNN 检测 **funnel accounts（漏斗账户）** 与 **layering（分层转移）**；
- **Regulatory change tracking**（监管变化追踪）；
- **Trade surveillance（交易监察）**——识别 **spoofing（幌骗）**、**front-running（抢先交易）**。

**Key Risk：false positives（误报）**——一条淹没分析师的 AML 警报，**比没有模型更糟**（an AML alert that floods analysts with noise is worse than no model）。

> 💡 支付看**延迟**（<100 ms），RegTech 看**信噪比**——一个怕慢，一个怕吵。

---

## 第 11 页 · Summary Table — Six Business Lines（六条业务线汇总表）

| Business Line（业务线） | Dominant AI Methods（主导方法） | Value Created（价值） | Key Risk（关键风险） |
|---|---|---|---|
| **Credit scoring**（信用评分） | XGBoost、神经网络、另类数据 | 更快更准、金融普惠 | **Bias & fairness**（偏差与公平） |
| **Fraud detection**（欺诈检测） | GenAI detectors、GNN、实时 ML | 抓 deepfake 与团伙、在资金转出前拦截 | **Arms race**、false negatives（漏报） |
| **Robo-advisory**（智能投顾） | 组合优化、LLM 建议 | 财富管理民主化、低费率 | **Suitability**、over-trust |
| **InsurTech**（保险科技） | CV、telematics、NLP | 更快理赔、动态定价 | **Adverse selection**、fairness |
| **Payments**（支付） | 实时 ML、AI 路由 | <100 ms 止诈、降低成本 | **Model latency**、evasion（规避） |
| **RegTech**（监管科技） | NLP、GNN、交易监察 | 合规自动化、降成本 | **False-positive flood**（误报洪水） |

**The Pattern（规律）**：**创造的价值越大，风险越集中在 fairness / false positives / adversarial evasion 上**——**AI is never a free lunch**（AI 从来不是免费午餐）。

> 💡 这张表是 Appendix A 第 1 条考点，**六行必须能默写"方法—价值—风险"三列配对**。

---

## 第 12 页 · 章节分隔页

**GNN for Fraud & AML** — 用于欺诈与反洗钱的图神经网络

---

## 第 13 页 · The Problem: Fraud Happens in Networks（问题：欺诈发生在网络里）

洗钱与有组织欺诈**不是孤立事件**，而发生在**网络**中。一条典型的洗钱链：

**Mule account（骡子账户，收款）→ Funnel account → Funnel account → Funnel account（漏斗账户，层层转移）→ Cash-out（取现：crypto/ATM）**

- 一圈 **mule accounts** 接收存款；
- 资金穿过多个 **funnel accounts** 以**掩盖轨迹（layering，分层）**；
- 最终通过**加密货币或 ATM 取现（cash-out）**。

**关键**：**没有任何单笔交易看起来明显犯罪**——犯罪藏在**连接的模式（pattern of connections）**里，而不在任何一个节点上。

> 💡 一句话：**"每一笔都合法，合起来是洗钱"**——这就是行级模型失效的根本原因。

---

## 第 14 页 · Why Traditional ML Misses This（为什么传统 ML 看不到）

**传统 ML**（逻辑回归、XGBoost）**孤立地给每笔交易打分**——它看到的只是**一行（one row）**的特征：金额、时间、商户。

**The Blind Spot（盲点）**：它看不到"**这个账户从 12 个 mule 收钱，而这 12 个 mule 又向 3 个已知坏账户转过钱**"。**网络信号对它是不可见的**。

**更糟的是**：欺诈者**故意让每笔交易保持小额且可信**，正是为了规避行级模型（row-level models）。

> 💡 这页是 GNN 存在的理由：**行级特征天然干净 ≠ 账户清白**。

---

## 第 15 页 · GNN: Models Nodes and Edges（GNN：建模节点与边）

**Graph Neural Network（GNN）** 把世界表示成**图（graph）**：

- **Nodes（节点）** = 账户、商户、设备、电话号码；
- **Edges（边）** = 交易、共享设备、共享地址。

图上可能出现的结构：**normal cluster（正常簇）**、**isolated（孤立节点）**、**suspicious ring/funnel（可疑团伙/漏斗）**。

**信息传播机制（propagation）**：沿边传播信息——**每个节点先从邻居更新自己的表示，再从邻居的邻居更新**。经过几轮之后：

> **每个节点的表示都编码了它的局部邻域结构（local neighborhood structure）**——身处可疑簇内的节点会获得一个"**可疑邻域**"嵌入，**即使它自己那一行的特征是干净的**。

> 💡 GNN 的魔法一句话：**"看你跟谁玩"**——特征可以伪装，邻居关系很难伪装。

---

## 第 16 页 · Application: AML（应用：反洗钱）

三类可检测的模式：

- **Funnel-account detection（漏斗账户检测）**——**高入度（high in-degree）+ 高出度（high out-degree）+ 低个人余额留存（low personal balance retention）**；
- **Layering pattern（分层模式）**——长长的**过桥账户（pass-through accounts）链**；
- **Mule networks（骡子网络）**——**共享设备/地址**、并汇聚到**同一 cash-out** 的账户簇。

**The Payoff（回报）**：基于 GNN 的 AML **能大幅降低误报率（cut false-positive rates dramatically）**，因为它不再标记"**恰好处于干净邻域中的可信交易**"。

> 💡 注意逻辑：GNN 不只提高**召回**（抓团伙），更提高**精度**（少冤枉好人）——这正好回应第 10 页"误报比没有模型更糟"。

---

## 第 17 页 · 章节分隔页

**Algorithmic Trading Mechanics** — 算法交易机制

（从这里开始进入"长焦"部分：算法交易 → RL。）

---

## 第 18 页 · What Is Algorithmic Trading?（什么是算法交易）

**定义**：用**计算机程序与数学模型**自动化交易——计算机**按规则执行交易，每笔交易无需人工干预（without human intervention per trade）**。

**规模**：研究估计**算法占美国股票成交量的 60–70%**。

> 💡 记数字：**算法交易 = 美股成交量 60–70%**；下一页的 HFT 是 50–60%——两个区间高度重叠，别混。

---

## 第 19 页 · Steps in Algorithmic Trading（算法交易的五个步骤）

| 步骤 | 内容 | 关键点 |
|---|---|---|
| **1. Strategy design（策略设计）** | 入场/出场信号：移动平均、**RSI**、**Bollinger Bands（布林带）**、均值回归、统计套利 | 外加**风险管理与仓位 sizing** |
| **2. Backtesting（回测）** | 指标：**年化收益、Sharpe ratio、最大回撤（max drawdown）、胜负比** | 防三种陷阱：**lookahead bias（前视偏差）、survivorship bias（幸存者偏差）、overfitting（过拟合）** |
| **3. Execution infrastructure（执行基础设施）** | 券商/交易所 **API**、延迟、订单类型、执行质量 | 从"想法"到"能下单" |
| **4. Risk controls（风险控制）** | **自动止损、动态对冲、仓位限额、敞口上限（exposure caps）** | 硬约束，非事后补救 |
| **5. Monitoring（监控）** | 实时绩效跟踪、参数调整、**kill-switches（熔断开关）** | 上线后不是结束 |

> 💡 第 2 步的三个偏差（lookahead / survivorship / overfitting）是简答题常见采分点——**回测最容易被"未来信息"和"只看到活下来的样本"骗**。

---

## 第 20 页 · Algorithmic Trading in Portfolio Management（组合管理中的算法交易）

三种典型用途：

- **Rebalancing（再平衡）**——当权重**漂移超过阈值**时，自动**卖出赢家/买入输家**以恢复目标权重；
- **Factor harvesting（因子收获）**——系统性偏向 **value（价值）、momentum（动量）、quality（质量）** 因子，并通过交易维持暴露；
- **Execution optimization（执行优化）**——用 **VWAP/TWAP（下一页）** 把**实施组合决策的成本**降到最低。

**Reported Benefits（报告收益）**：更快执行、减少人为错误与情绪、**优化执行使交易成本降低 10–30%**、持续风险监控。

> 💡 注意 10–30% 是**交易成本**的降幅，不是收益的增幅——选择题常在这两个名词之间挖坑。

---

## 第 21 页 · High-Frequency Trading（HFT，高频交易）

**HFT 是算法交易的极端端**：**超低延迟（ultra-low-latency，微秒级）**、持仓**数秒到数毫秒**、每笔交易**无人在环（no human in the loop）**。**HFT 公司占美股成交量的 50–60%**。

**Milliseconds Matter（毫秒值钱）**：

- 公司在**硬件与 co-location（交易所数据中心内的服务器托管）**上花费**数千万美元**；
- 著名的 **Spread Networks** 项目花 **3 亿美元**建**芝加哥—纽约光纤**，只为削掉 **3 毫秒**传输时间；
- **微波（microwave）网络**后来又把延迟相对光纤压低 **30–40%**。

**策略**：**market making（做市）**、**statistical arbitrage（统计套利）**、**latency arbitrage（延迟套利）**。

**2010 Flash Crash（闪电崩盘）**：道琼斯指数**数分钟内暴跌约 1,000 点**随后恢复；**HFT 既被指责、也被认为对稳定有贡献**。

> 💡 三个数字：**3 亿美元 / 3 毫秒 / 50–60% 成交量**——把"速度如何被定价"讲透的一页。

---

## 第 22 页 · The Speed Arms Race（速度军备竞赛）

**机制**：一旦一家公司更快，**优势就会衰减（the edge decays）**，直到所有人再次投资——这是一场 **Red Queen's race（红皇后竞赛）**：**你花越来越多的钱，只为留在原地**。

**扩散**：HFT 如今已超出股票——进入 **FX（外汇）、commodities（商品）、cryptocurrencies（加密货币）**。

**呼应前文**：这与 **L1 的 "arms race for alpha"（阿尔法军备竞赛）**、**L7 的 alpha-decay treadmill（阿尔法衰减跑步机）** 是**同一个模式**——**速度只是又一种会被套利掉的资源（speed is simply one more resource that gets arbitraged away）**。

> 💡 与 L1/L7 打通的一句话：**数据、速度、模型，凡是能买到的优势，最终都会被竞争抹平**。

---

## 第 23 页 · Execution Algorithms: VWAP（执行算法：VWAP）

**问题背景**：大型机构要交易**大单（big size）**（例如买入 **100,000 股**），**不能直接下市价单**——那会**推动价格对自己不利（move the price against itself）**，这就是 **market impact（市场冲击）**。**执行算法（execution algorithms）**把**母单（parent order）**切成许多**子单（child orders）**。

**VWAP — Volume-Weighted Average Price（成交量加权平均价）**：

**VWAP = Σ(Price_t × Volume_t) / Σ Volume_t**

**切单逻辑**：**当日历史成交量高时多交易、低时少交易**——成交量高峰出现在**开盘/收盘集合竞价（open/close auctions）** 与 **午间高峰（lunch peaks）**。

**Goal（目标）**：**匹配当日 VWAP**——它是**事实上的执行基准（the de-facto execution benchmark）**。

**Best for（最适合）**：**流动性好、成交量分布可预测（liquid markets with predictable volume profiles）**的市场。

> 💡 VWAP 的关键词是**"藏进成交量里"**：跟着市场的呼吸节奏下单，让冲击被成交量吸收。

---

## 第 24 页 · Execution Algorithms: TWAP & Implementation Shortfall（TWAP 与实施缺口）

**TWAP — Time-Weighted Average Price（时间加权平均价）**：

**TWAP = Σ Price_t / N**

**切单逻辑**：**把订单在时间上均匀切开（evenly over time）**。**Goal**：**忽略成交量的纯时间均匀执行**。**Best for**：**流动性差或成交模式反复无常（illiquid or erratic）**的市场——成交量规律不可靠时用它。

**VWAP vs TWAP 对比表**：

| Feature（特征） | VWAP | TWAP |
|---|---|---|
| **Volume sensitivity（对成交量敏感）** | **Yes** | **No** |
| **Goal（目标）** | 匹配自然成交量、降低冲击（match natural volume, reduce impact） | 均匀时间执行、减少滑点（even time-based execution, reduces slippage） |
| **Best for（适用）** | 流动性好、成交量可预测（liquid, predictable volume） | 流动性差或剧烈波动（illiquid or volatile markets） |

**Implementation Shortfall（实施缺口）——第三个基准**：**最小化"决策价格（decision price）"与"最终执行价格（final execution price）"之间的差距**，同时权衡 **market impact（市场冲击）** 与 **opportunity cost（机会成本）**。

> 💡 三个基准的哲学不同：**VWAP 对标市场（跟量）、TWAP 对标时间（匀速）、IS 对标自己的决策价（少后悔）**。

---

## 第 25 页 · The Trade-Off: Urgency vs. Market Impact（权衡：紧迫性 vs 市场冲击）

**执行算法都活在同一条权衡曲线上**：

- **执行快（FAST）→ 市场冲击高（high market impact）**；
- **执行慢（SLOW）→ 冲击低，但价格可能漂移（price may drift）**。

**三类成本的对应工具**：

| 成本类别 | 管理手段 |
|---|---|
| **Market impact（市场冲击）** | 限价单（limit orders）、切单（order slicing，如 VWAP）、**dark pools（暗池）** |
| **Transaction costs（交易成本）** | 限价单、**TWAP**、在流动性好的市场交易 |
| **Risk（执行期间的不利变动）** | 限价/止损单、**VWAP 分散（spreading）** |

**No Free Lunch（没有免费午餐）**：**你要么付冲击、要么付风险**。**算法的工作，是为订单的紧迫程度找到曲线上最便宜的那个点（the cheapest point on the curve）**。

> 💡 一句可背的简答：**"快 = 冲击；慢 = 风险；执行算法的全部意义是在这两者之间按紧迫度取最优。"**

---

## 第 26 页 · 章节分隔页

**Reinforcement Learning for Trading** — 用于交易的强化学习

---

## 第 27 页 · From Rules to Learning（从规则到学习）

**范式切换**：从**基于规则的算法**（VWAP/HFT 遵循**固定配方 fixed recipes**）走向**基于学习的算法**。

**What Is RL（什么是强化学习）**：

> 强化学习是 ML 的一个子领域：**agent（智能体）通过与 environment（环境）交互、获得 reward（奖励），来最大化累积奖励（maximize cumulative reward）——不需要标注数据（no labeled data needed）**。它**从经验中学习（learns from experience）**，就像人类交易员**试错（trial and error）**那样。

> 💡 与 L4–L7 的分水岭：**监督学习有答案，RL 只有分数（scalar reward）**。

---

## 第 28 页 · Core Components（核心组件）

| Component（组件） | In trading（在交易中） | Meaning（含义） |
|---|---|---|
| **Agent** | 交易算法 | 决策者（The decision-maker） |
| **Environment** | 市场（价格、订单簿、其他参与者） | agent 交互的对象 |
| **State s_t** | 当前价格、收益率、持仓、指标 | "发生了什么"的快照 |
| **Action a_t** | 买 / 卖 / 持有（或仓位大小） | agent 做的事 |
| **Reward R_t** | 利润，或风险调整后收益减去成本 | 标量反馈信号（scalar feedback） |

**交互循环**：**观察 s_t → 选择 a_t → 获得 r_t 并进入 s_(t+1)**。

> 💡 五个组件是 RL 简答题的"定义题标准答案"，**必须能逐项映射到交易语境**。

---

## 第 29 页 · Policy（策略）

**Policy π 是 agent 的策略——把状态映射到动作（maps states to actions）**。

- **Deterministic policy（确定性策略）**：**π: S → A**——给定状态，**永远同一个动作**；
- **Stochastic policy（随机策略）**：**π(a|s)**——给定状态，返回**动作上的概率分布**。

**为什么需要随机策略**：在**部分可观测（partially-observable）**或**对抗性（adversarial）**环境中**必不可少**——**防止 agent 因为总做同一件事而被对手利用（prevents the agent from being exploited by always doing the same thing）**。

**RL 的全部目的**：**找到使期望累积奖励最大化的策略**（find the policy that maximizes expected cumulative reward）。

> 💡 确定性 = 可预测 = 可被抢跑；随机策略在交易里还有**隐蔽意图**的作用。

---

## 第 30 页 · Value Functions（价值函数）

价值函数估计"**身处某个情境有多好**"——是 agent 内部的**记分卡（scorecard）**。

**State Value Function（状态价值函数）**：
**V(s) = E[future reward | S_t = s]**
读法："**如果我在状态 s，从这里往后我预期能得到多少总奖励？**"

**Action Value Function（动作价值函数，Q-function）**：
**Q(s,a) = E[future reward | S_t = s, A_t = a]**
读法："**如果我在状态 s 并采取动作 a，我预期能得到多少总奖励？**"

**Why Q Is More Useful（为什么 Q 更有用）**：**如果知道所有动作的 Q(s,a)，最优策略就是"选 Q 最大的那个动作"**——策略可以**直接读出**，无需另做优化。

> 💡 V 回答"这个局面好不好"，**Q 回答"这个局面下这步棋好不好"**——有 Q 就有策略。

---

## 第 31 页 · The Bellman Equation — One Page of Intuition（Bellman 方程：一页直觉）

**Bellman 方程是 RL 的核心递归思想（central recursive idea）**。一个状态的价值拆成两块：

**V(s) = r + γ · V(s′)**

（其中 **r = immediate reward（即时奖励）**；**γ·V(s′) = discounted value of next state（下一状态价值的折现值）**。）

**一句话直觉**：

> **"我现在的价值 = 我立刻拿到的奖励 +（折现后的）我下一步所在之处的价值。"**

原文强调：**直觉到此为止，无需推导（no derivation needed for intuition）**。

**Discount factor γ ∈ [0,1]（折现因子）控制时间偏好**：

- **γ 接近 1 → 有耐心、长视（patient, long-horizon）**；
- **γ 接近 0 → 贪婪、短视（greedy, myopic）**。

> 💡 期末必考句式：**"value = reward + γ × next-state value"**——能写出这个式子并解释 γ 就拿到基本分。

---

## 第 32 页 · Why Discount, and Why Bellman Matters（为什么要折现、Bellman 为何重要）

**Why discount at all（为什么要折现）——三个理由**：

1. **(a) 未来的奖励是不确定的（uncertain）**；
2. **(b) 现在的钱比以后的钱更值钱（time value of money）**；
3. **(c) 它让数学收敛（it makes the math converge）**。

**The Power of the Recursion（递归的力量）**：

> Bellman 方程把"**最大化终身总奖励**"这个**巨大且不可解（enormous, intractable）**的问题，转化成**局部递归（local recursion）**：**只要我知道所有下一状态的价值，我就能算出当前状态的价值**。

**因此**：**RL 算法本质上都是"从经验中巧妙估计这些价值函数、再从中导出好策略"的方法**（RL algorithms are, at their core, clever ways to estimate these value functions from experience, and then derive a good policy from them）。

> 💡 Bellman 的价值 = **把"一辈子"的问题拆成"下一步"的问题**——这就是动态规划的灵魂。

---

## 第 33 页 · The RL Process（RL 的流程）

四个步骤：

1. **Initialize（初始化）**——任意的策略与价值函数；
2. **Interact（交互）**——观察状态、选择动作（**explore or exploit**）、获得奖励、观察下一状态；
3. **Learn（学习）**——用观测到的 **(s, a, r, s′)** 转移**更新策略/价值**（Q-learning、policy gradient 等）；
4. **Iterate（迭代）**——持续循环，策略**向最优改进**。

**Exploration vs. Exploitation（探索与利用）**：

> agent 应该做**目前看起来最好的**（exploit），还是**尝试可能更好的新动作**（explore）？**过度利用 → 卡在局部最优（local optimum）；过度探索 → 永不收敛（never converges）**。

> 💡 这个张力是贯穿全讲的暗线：第 46 页说它是"训练慢且不稳定"的根源之一。

---

## 第 34 页 · 章节分隔页

**RL Method Types** — 强化学习方法类型

---

## 第 35 页 · Value-Based Methods（基于价值的方法）

**思路**：**学一个价值函数（V 或 Q），再间接导出策略**——例如"选 Q 最高的动作"。

**Examples & Strength（例子与优势）**：

- **Q-learning、SARSA、DQN（Deep Q-Network）**——DQN 就是**用神经网络近似 Q 函数**的 Q-learning；
- **优势**：**稳定、易于理解（stable, well-understood）**；**动作集离散且小（discrete and small，如 buy/sell/hold）时表现好**。

**Limitation（局限）**：**在连续动作空间与探索方面吃力（struggles with continuous action spaces and with exploration）**。

> 💡 记法：**value-based 先"估值"再"选最大"**——所以只擅长"选项少"的题。

---

## 第 36 页 · Policy-Based Methods（基于策略的方法）

**思路**：**直接参数化策略**（例如 **π_θ(a|s)** 用神经网络表示），**对期望奖励做梯度上升（gradient ascent）**来优化参数。

**Examples & Strength**：

- **REINFORCE、PPO（Proximal Policy Optimization）**；
- **优势**：**能处理连续动作空间**（"买/卖多少"而不只是"买/卖/持"）；**能学随机策略（stochastic policies）**。

**Limitation**：**高方差（high variance）、样本效率低（sample-inefficient）、易陷局部最优（prone to local optima）**。

> 💡 对比记忆：**policy-based 直接学"怎么做"，不再绕道价值函数**——灵活但吵（高方差）。

---

## 第 37 页 · Actor-Critic Methods（演员-评论家方法）

**思路**：**两者结合**——**Actor（演员，即策略）提出动作**；**Critic（评论家，即价值函数）评估动作**；**Actor 用 Critic 的反馈来更新**。

**Examples & Strength**：

- **A2C（Advantage Actor-Critic）、DDPG、SAC（Soft Actor-Critic）**；
- **优势**：**比纯策略方法方差更低（lower variance）**；**能处理复杂、高维环境**——**现代深度强化学习（Deep RL, DRL）的主流方法都在这里（where most modern Deep RL methods live）**。

**Limitation**：**实现更复杂**；**稳定性与收敛是真实的工程难题（real engineering concerns）**；**计算密集（compute-intensive）**。

> 💡 一句话：**Actor 负责"出招"，Critic 负责"打分"，打分反过来指导出招**——兼顾灵活与稳定。

---

## 第 38 页 · Comparison Table（三类 RL 方法对比表）

| Type（类型） | Examples（例子） | Strength（优势） | Limitation（局限） | Best for（最适合） |
|---|---|---|---|---|
| **Value-based** | Q-learning、DQN | 稳定、简单 | 只能离散动作、探索能力弱 | **离散动作（buy/sell/hold）** |
| **Policy-based** | REINFORCE、PPO | 连续动作、随机策略 | 高方差、样本饥渴（sample-hungry） | **连续仓位 sizing** |
| **Actor-Critic** | A2C、DDPG、SAC | 方差更低、复杂环境 | 复杂、不稳定、算力重 | **大多数现代 DRL** |

**How to Choose（怎么选）**：

- **离散小动作集（buy/sell/hold）→ value-based**；
- **连续动作（"多少"）→ policy-based 或 actor-critic**；
- **复杂环境 → actor-critic（现代 DRL 主流）**。

> 💡 这张表是 Appendix A 第 5 条考点，**"类型—例子—优势—局限—适用"五列要能整行复述**。

---

## 第 39 页 · 章节分隔页

**RL Training Tips for Finance** — 金融场景的 RL 训练技巧

---

## 第 40 页 · Rich Data & Higher Frequency（丰富数据与更高频率）

**Tip 1：Extensive Interaction with the Environment（与环境充分交互）**

- **RL 需要丰富的数据**。**不要只依赖历史价格**——把**新闻情绪（news sentiment）、社交媒体信号（social-media signals）、经济指标（economic indicators）**并入**环境状态**；
- **只靠历史价格数据 → 对单一已实现的价格路径过拟合（overfitting to one realized price path）**。

**Tip 2：Use Higher-Frequency Data（使用更高频数据）**

- **分钟级或秒级数据**带来**更细的决策**与**更多的训练转移（more training transitions）**；
- **代价**：**复杂度与算力剧增（compute dramatically）**，并引入**微观结构噪声（microstructure noise）**。

> 💡 两条 tips 的共同逻辑：**RL 是"数据饥渴 + 路径依赖"的——喂它一条价格曲线，它只会背下那条曲线**。

---

## 第 41 页 · Multi-Objective Reward & Simplified Actions（多目标奖励与简化动作）

**Tip 3：Multi-Objective Optimization（多目标优化）**

奖励**不只是利润（not just profit）**：

**reward = PnL − λ1 · inventory vol − λ2 · slippage − λ3 · fees**

即：**盈亏 − 库存波动惩罚 − 滑点惩罚 − 费用惩罚**。

- **λ 权重可以按市场状态（regime）自适应调整（adaptively tuned by regime）**；
- 目的：**防止 agent 学出"只看 PnL"的不稳定策略——那种策略会反复折腾仓位（churns the book）**。

**Tip 4：Simplify Actions（简化动作）**

- **离散化（Discretize）**：**buy/sell/hold，或少数几档离散 size**，以**降低学习难度**；
- **连续的二维动作（size + direction，仓位大小 + 方向）远比三选一的离散选择难学（far harder to learn）**，尤其在**数据有限**时。

> 💡 这条公式的 λ 三项就是"用奖励函数做风控"——**把库存、滑点、费用写进 reward，而不是写进事后规则**。

---

## 第 42 页 · Enrich (Carefully) the State Representation（谨慎地丰富状态表示）

**Tip 5：Enrich the State（丰富状态）**

- 加入**技术指标、宏观数据、情绪（sentiment）**——**但要避免噪声过载（avoid noise overload）**。

**Practical Case — High-Frequency State Features（实务案例：高频状态特征）**：

| 特征 | 含义 |
|---|---|
| **Order imbalance** | 订单簿买卖失衡 |
| **Price-volume slopes** | 价量斜率 |
| **Micro-price impact** | 微价格冲击 |
| **Recent trade density** | 近期成交密度 |

- 均经 **EWMA 去噪（EWMA-denoised）**；
- **Critical constraint（关键约束）**：**每个特征都必须在交易时刻实时可得（available in real-time at the trading moment）——绝不允许未来信息（no future information allowed）**。

> 💡 这一页在训练层面重复了第 19 页的 **lookahead bias**：**特征工程的第一条纪律是"时间同步"**。

---

## 第 43 页 · 章节分隔页

**RL Limitations in Finance** — RL 在金融中的局限

---

## 第 44 页 · Lack of Realistic Environments — The Sim2Real Gap（缺乏真实环境：仿真到现实的鸿沟）

**总体判断**：**尽管炒作不断，金融 RL 仍主要是研究，实际生产应用有限（mostly research, with limited live production use）**——原因是**结构性的（structural）**。

**The Gap（鸿沟）**：

> RL agent 在**模拟器（simulator）**中训练，但**模拟器无法准确建模"市场如何对 agent 自己的交易作出反应"**——即 **market impact（市场冲击）** 与**其他参与者的对抗性反应（adversarial response）**。结果：**agent 对模拟器过拟合，在现实中失败**。

**Mitigation（缓解手段，四条）**：

1. **Domain randomization（域随机化）**——随机化**撮合延迟（matching delay）、冲击参数（impact parameters）、滑点分布（slippage distributions）**；
2. **Mix with historical replay（混合历史回放）**；
3. **Shadow accounts（影子账户）**——上线前做 **A/B 测试**；
4. **Controllable drawdown caps（可控回撤上限）**。

> 💡 **sim2real gap** 是本讲最重要的"反鸡汤"概念：**你的交易会改变市场，而你的模拟器不知道**。

---

## 第 45 页 · Limited & Non-Stationary Data; Low SNR（数据有限且非平稳；低信噪比）

**Limited & Non-Stationary Data（数据有限且非平稳）**：

- 金融数据是**有限的（finite）**且**不断切换状态（regime-shifting）**；
- **在股票 A 上学到的策略，未必适用于股票 B**；**2018 年work的策略，2024 年可能失效**；
- **Mitigation（缓解）**：
  - **Concept-drift detection（概念漂移检测）**——用 **PSI / KS 检验** 触发**重训窗口（retraining windows）**；
  - **Prioritized experience replay（优先经验回放）**——**给近期经验更高权重**。

**Low Signal-to-Noise Ratio（低信噪比）**：

- **金融收益大部分是噪声（mostly noise）**；
- **RL 需要大量手工特征工程（manual feature engineering）来滤噪**——这引入**专家偏差（expert bias）**并**限制可扩展性（limits scalability）**。

> 💡 两个缓解手段的名字要记：**PSI/KS 用于概念漂移检测，prioritized experience replay 用于"重近轻远"**。

---

## 第 46 页 · No Action Labels & Slow Convergence（没有动作标签，收敛慢）

**核心事实**：与监督学习不同，**RL 没有"正确动作"标签（no "correct action" labels）**——**它只从标量奖励（scalar rewards）学习**。

**The Consequence（后果）**：

- **训练因此缓慢且不稳定（slow and unstable）**；
- **探索-利用的张力持续存在（persistent exploration-vs-exploitation tension）**；
- **收敛不被保证（Convergence is not guaranteed）**。

> 💡 到这里四条局限集齐：**sim2real gap → 非平稳/数据有限 → 低 SNR → 无标签/慢收敛**——正好对应 Appendix A 第 6–7 条。

---

## 第 47 页 · 章节分隔页

**FinRL — Open-Source DRL Library** — FinRL：开源深度强化学习库

---

## 第 48 页 · What FinRL Provides（FinRL 提供什么）

**FinRL**（来自 **AI4Finance Foundation**）是**首个专门面向量化金融的开源深度强化学习（Deep Reinforcement Learning）库**，**为教育与研究而设计（designed for education and research）**——原文称其为**"课程项目与 demo 的绝佳起点（an excellent starting point for course projects and demos）"**。

**A Full Pipeline（一条完整流水线）**：

| 步骤 | 内容 |
|---|---|
| **1. Environment setup（环境搭建）** | 为**股票、ETF、加密货币、组合**构建市场模拟（**state space、action space、reward function**） |
| **2. DRL agent training（智能体训练）** | **多个算法开箱即用（out of the box）**：**DQN、DDPG、PPO、A2C、SAC** |
| **3. Backtesting（回测）** | **绩效指标（performance metrics）**、**与基准比较（comparison to benchmarks）** |
| **4. Evaluation（评估）** | **标准化图表与报告（standardized plots and reports）** |

**GitHub**：`AI4Finance-Foundation/FinRL`（**arXiv: 2011.09607**）。

> 💡 记住四个词：**环境 → 训练 → 回测 → 评估**；再记五个算法：**DQN / DDPG / PPO / A2C / SAC**。

---

## 第 49 页 · Why It Matters for This Course（为什么对这门课重要）

**FinRL Handles the Machinery（FinRL 负责"机械部分"）**：

> FinRL **处理 RL 的机械（the RL machinery）**——**训练循环（training loops）、经验回放缓冲（replay buffers）、算法实现（algorithm implementations）**——好让学生**专注于真正重要的、金融特有的决策**：**state design（状态设计）、reward engineering（奖励工程）、evaluation（评估）**。

**原文点睛**：

> **"那正是领域知识所在之处，也是 alpha（如果有的话）的所在之处。"**
> （That is exactly where domain knowledge lives and where the alpha (if any) is found.）

> 💡 这句话说明了课程的工具哲学：**库替你写循环，你自己决定"看什么、奖什么、怎么评"**——后者无法外包。

---

## 第 50 页 · 章节分隔页

**Case Study 1: Deepfake Fraud vs. GenAI Anti-Fraud** — 案例一：深度伪造欺诈 vs 生成式 AI 反欺诈

---

## 第 51 页 · The Attack（攻击）

**The Attack — 2019（2019 年的经典案例）**：

> 欺诈者用**语音克隆（voice cloning）**冒充一家**英国能源公司 CEO**，指示其**匈牙利子公司**向境外账户电汇 **€220,000（约 $243K）**——该子公司的**董事总经理（managing director）"听出了"老板的口音（"recognized" his boss's accent）**，于是批准了转账。**直到真正的 CEO 打电话询问这笔转账，事情才被发现**。

**Beyond voice（语音之外）**：

- **Deepfake 视频绕过 video KYC**——把一张**合成人脸（synthesized face）**举到摄像头前；
- **Synthetic identities（合成身份）**——**伪造的 PII 组合**，被**大规模（at scale）**用于申请贷款与信用卡。

**The 2025 Scale（2025 年的规模）**：据 **Feedzai 2025 欺诈趋势报告**，**超过 50% 的欺诈涉及 AI 或 deepfake**。**生成式 AI 变成商品化工具（commodity tooling）的那一刻，攻击面就扩大了**。

> 💡 案例的三个数字/事实：**2019 年、€220,000、口音被骗过**——说明**"人耳"作为身份验证已经失效**。

---

## 第 52 页 · The Defense & The Arms Race（防御与军备竞赛）

**The Defense — Three Layers（三层防御）**：

1. **GenAI detectors（生成式 AI 检测器）**——寻找合成语音/视频中的**伪影**：**spectral fingerprints（频谱指纹）、lip-sync mismatches（唇音不同步）、frame inconsistencies（帧间不一致）**；
2. **GNN**——检测**合成身份申请背后的欺诈团伙（fraud rings）**；
3. **Real-time anomaly scoring（实时异常评分）**——对**每一笔交易**打分。

**The Arms Race（军备竞赛）**：

> **检测与生成协同演化（co-evolve）**。检测器变强，攻击者的生成也变强；**这个循环是永久的（permanent）**。**欺诈检测是少数"永久重训不是可选项"的 ML 领域之一——一个冻结的模型会在数周内衰减（a frozen model decays in weeks）**。

> 💡 与第 7 页完全对应：**第 7 页讲原理，第 51–52 页用 2019 案例把它讲成故事**——两页互为表里。

---

## 第 53 页 · 章节分隔页

**Case Study 2: FinRL Stock Trading Demo** — 案例二：FinRL 股票交易演示

---

## 第 54 页 · Setup & Walkthrough (Steps 1–3)（设置与流程：第 1–3 步）

**Setup（设置）**：用 **FinRL** 搭建一个 **Dow Jones 30 只成分股**的环境，训练一个 **PPO agent**，**回测**，并与 **buy-and-hold（买入持有）基准**比较。

| 步骤 | 具体内容 |
|---|---|
| **1. Environment（环境）** | **30 只道指成分股、数年日频 OHLCV**；**state = 近期价格/技术指标 + 当前组合权重**；**action = 连续组合权重（continuous portfolio weights）**；**reward = 日组合收益减去交易成本** |
| **2. Train PPO（训练 PPO）** | **actor-critic 学习把状态映射到组合再平衡决策（portfolio rebalancing decisions）** |
| **3. Backtest（回测）** | 在**留出的测试期（held-out test period）**运行学到的策略；计算**累计收益、Sharpe、最大回撤** |

> 💡 注意这里的 action 是**连续组合权重**（不是 buy/sell/hold）——正好呼应第 38 页"连续动作 → policy-based/actor-critic"。

---

## 第 55 页 · Walkthrough (Steps 4–5) & The Critical Caveat（第 4–5 步与关键警告）

**4. Compare（比较）**：**PPO agent 在回测中常常战胜 buy-and-hold（often beats buy-and-hold）**，**尤其在震荡市场（choppy markets）**——方式是**在回撤之前降低敞口（reducing exposure before drawdowns）**。

**5. What the agent "learned"（agent 学到了什么）**：大致是一个**动量与均值回归的混合体（a momentum-and-mean-reversion hybrid）**：

- **持续上涨后增加敞口**；
- **急跌后减仓（trim after sharp drops）**；
- **横盘市场避免频繁交易（avoid churn in flat markets）**。

**The Caveat — and It Is Critical（关键警告，而且极其关键）**：

> **回测成功 ≠ 实盘成功（Backtest success ≠ live success）**。agent 是在**同一段历史市场**上训练与测试的，而那段市场**不会对它的（微小的、模拟的）交易作出反应**。**在生产中，面对真实的市场冲击、状态切换（regime shifts）与对抗性对手（adversarial counterparties），同一个策略可能亏钱**。**sim2real gap 才是全部的关键（the entire ballgame）**。
> **把 FinRL 的结果当作"假设生成器（hypothesis generator）"，而不是印钞机（not a money printer）**。

> 💡 金句可背：**"FinRL 是假设生成器，不是印钞机"**——这句话本身就是一道简答题的答案。

---

## 第 56 页 · 章节分隔页

**Case Study 3: VWAP vs. TWAP Execution** — 案例三：VWAP 与 TWAP 执行

---

## 第 57 页 · Setup & Both Approaches（设置与两种方法）

**Setup（设置）**：一只基金需要在**一个交易日内买入 100,000 股**某只**流动性好的大盘股**，且**不推动价格（without moving the price against itself）**。

**VWAP Approach（VWAP 方案）**：

- **预测当日成交量分布**——历史上呈 **U 形（U-shape）**：**开盘/收盘重、午间轻**；
- 按该分布切分 100,000 股，原文给出的**示例权重**：

| 时段 | 下单比例 |
|---|---|
| **前 30 分钟（first 30 min）** | **约 25%** |
| **上午中段（mid-morning）** | **约 15%** |
| **午间（lunch）** | **约 10%** |
| **下午中段（mid-afternoon）** | **约 20%** |
| **收盘前（into the close）** | **约 30%** |

**TWAP Approach（TWAP 方案）**：同样的 100,000 股**切成等份**——例如 **100 张子单、每张 1,000 股**，**每约 4 分钟一张**，覆盖 **390 分钟**的美股交易时段。

> 💡 注意 VWAP 的五档权重合计正好 **100%**（25+15+10+20+30）——考选择题时可能让你判断哪档最重（**收盘 30%**）。

---

## 第 58 页 · When Each Fits（各自何时适用）

| 算法 | 适用场景 |
|---|---|
| **VWAP** | **流动性好、成交量模式可靠**的股票——**"藏在成交量里"（hiding in the volume）以最小化市场冲击** |
| **TWAP** | **流动性较差或走势反复（erratic）**、成交量模式不可靠的股票；或目标只是**"稳定地待在市场里"（be in the market steadily）** |
| **Implementation shortfall** | **紧急订单（urgent orders）**——此时**主导风险是价格跑掉（price running away），而不是市场冲击** |

**权衡（as always）**：**更快 = 更多冲击；更慢 = 更少冲击，但更多不利变动的暴露（adverse moves）**。

> **艺术在于把算法与订单的紧迫程度匹配起来（matching the algorithm to the order's urgency）。**

> 💡 三个基准的"一句话适用条件"是简答题高频：**VWAP 看成交量、TWAP 看时间、IS 看紧迫**。

---

## 第 59 页 · 章节分隔页

**Summary** — 总结

---

## 第 60 页 · Key Takeaways (Part 1)（要点回顾·上）

1. **AI 如今是横跨整个金融业的水平层**——credit、fraud、advisory、insurance、payments、RegTech。**每条线有自己的方法、价值与风险**；反复出现的风险是 **fairness（公平）、false positives（误报）、adversarial evasion（对抗性规避）**。
2. **欺诈是一场 AI 军备竞赛**——**2025 年 >50% 的欺诈涉及 AI/deepfake**；银行用 **GenAI detectors、GNN（看团伙而非孤立行）、实时评分** 三层防御。
3. **算法交易按规则自动化执行**；**VWAP 按成交量切单（slices by volume）**、**TWAP 按时间均匀切单（slices evenly by time）**；**HFT 是微秒级速度的极端端**。**普适权衡：urgency vs. market impact**。
4. **强化学习 = agent + environment + state + action + reward，无需标签**。**Bellman 方程（value = reward + γ × next-state value）是核心递归**。

> 💡 这四条对应"行业全景（1–2）+ 算法交易（3）+ RL 定义（4）"，是 Part 1 的骨架。

---

## 第 61 页 · Key Takeaways (Part 2)（要点回顾·下）

5. **三类 RL 方法族**：**value-based（DQN，离散动作）**、**policy-based（PPO，连续动作）**、**actor-critic（A2C/DDPG/SAC，现代 DRL 主流）**。
6. **RL 训练技巧**：**丰富的多源数据、更高频率、多目标奖励（PnL − risk − slippage − fees）、简化的离散动作、谨慎丰富的实时状态**。
7. **RL 的局限是结构性的**：**sim2real gap、非平稳且有限的数据、低 SNR、无动作标签/慢收敛**。
8. **FinRL 是金融领域的开源 DRL 库**——**它处理机械部分，让你专注于 state/reward/evaluation 的设计**。**Backtest ≠ live**。

**全讲收束句（原文）**：

> **AI in finance is a horizontal capability layer — but every business line's edge decays, every model needs perpetual retraining, and every backtest needs a sim2real reality check.**
> （金融中的 AI 是一层水平能力层——但**每条业务线的优势都会衰减**，**每个模型都需要永久重训**，**每个回测都需要一次 sim2real 的现实检验**。）

> 💡 三个"每个（every）"是全讲的价值观：**优势会衰减、模型会过期、回测会撒谎**。

---

## 第 62 页 · Further Reading（延伸阅读）

- **FinRL** — AI4Finance Foundation，GitHub `AI4Finance-Foundation/FinRL`；**arXiv: 2011.09607**。
- **FINRA** — *Artificial Intelligence in the Securities Industry*（**监管者视角 regulator perspective**）。
- **Feedzai** — *2025 AI Fraud Trends*（行业现状报告）。
- **Optional**：**Sutton & Barto, *Reinforcement Learning: An Introduction***——**RL 的经典教科书（canonical RL textbook，免费在线）**。
- **Optional**：**Mnih et al. (2015), *Human-level control through deep reinforcement learning***——**原始 DQN 论文（Nature）**。

**End of Lecture 8. Next: Lecture 9 — Risk Management & AI Governance.**（L8 结束，下一讲：风险管理与 AI 治理。）

> 💡 两个必记的引用：**Sutton & Barto（RL 圣经）与 Mnih 2015（DQN 原始论文）**。

---

## 第 63 页 · 章节分隔页

**Open Discussion (Optional)** — 开放讨论（可选）

---

## 第 64 页 · Two Questions（两个讨论问题）

**可选——课后自行思考与讨论（Optional — think and discuss on your own after class）**。

**Q1：Build vs. Buy for Fraud Detection（反欺诈自建还是外购）**

> 银行应该**自建**自己的 AI 反欺诈栈（**专有、昂贵、完全控制**），还是**外购厂商方案**（**更便宜、更快、差异化更少**）？

**Hints（提示）**：

- **数据就是护城河（data is the moat）**——**厂商看到的是很多银行的"广度"，你看到的是自己客户的"深度"**；
- **速度 vs 控制（speed vs. control）**；
- **监管问责（regulatory accountability）**；
- **人才（talent）**。

**Q2：RL in Trading — Production or Research?（交易中的 RL：生产还是研究？）**

> 考虑到 **sim2real gap** 与**非平稳性（non-stationarity）**，RL 今天对**实盘交易**是否实用，还是仍以**研究**为主？

**Hints（提示）**：

- **门槛最低的地方在哪里？——执行优化（execution optimization），而不是 alpha 生成（not alpha generation）**；
- **"production-ready（可上生产）"需要什么条件？**
- **与"监督式预测 + 规则化执行（supervised forecast + rule-based execution）"作对比**。

> 💡 Q2 的提示其实给出了讲者的倾向：**RL 在"执行"这一层最可行，在"找 alpha"这一层最难**。

---

## 第 65 页 · Appendix（附录分隔页）

> **Course-information reference material — not examined content**
> （课程信息参考资料——**不考内容**）

---

## 第 66 页 · Appendix A: Exam Review Checklist（附录 A 标题页）

（标题页，无正文；内容见下一页。）

---

## 第 67 页 · Appendix A — Exam Review Checklist（本讲可考内容清单）

**本讲内容属于期末考试范围**：**Final Exam（11 月 30 日，权重 40%，覆盖 L6–L10**——完整考试结构见 Lecture 1 的 Appendix A）。

| § | Examinable content（可考内容） |
|---|---|
| **1** | **六条业务线**（credit、fraud、robo-advisory、InsurTech、payments、RegTech）：**主导方法、价值、关键风险** |
| **2** | **GNN 直觉**：节点/边；**为什么行级 ML 漏掉网络欺诈**；**funnel / mule / layering 模式** |
| **3** | **算法交易步骤**；**HFT 与 co-location**；**VWAP vs TWAP 公式与用例**；**urgency-vs-impact 权衡** |
| **4** | **RL 核心组件**（agent、state、action、reward）；**policy**；**价值函数（V、Q）**；**Bellman 方程直觉**；**折现因子 γ** |
| **5** | **三类 RL 方法族**（value-based、policy-based、actor-critic）：**例子、优势、局限** |
| **6–7** | **RL 训练技巧**（多目标奖励、状态/动作设计）；**结构性局限**（sim2real gap、非平稳、低 SNR、无标签） |
| **8** | **FinRL 流水线及其角色**（处理 RL 机械，而非提供 alpha） |

**Format（题型）**：**多项选择题 + 1–2 道简答题（QA）**（期末，**1.5 小时**）。

> 💡 附录 A 是复习的"官方大纲"——**8 条编号就是 8 个复习模块，按编号顺序过一遍即可覆盖本讲**。

---

## 本讲考点（依据 Appendix A）

> 以下 8 条严格对应第 67 页 Appendix A 的 8 个编号；括号内为原文关键词，便于对照英文试卷。

1. **六条业务线三列表**（§1）：credit scoring（**XGBoost/神经网络/另类数据 → 快、准、普惠 → 偏差与公平**）、fraud detection（**GenAI detectors/GNN/实时 ML → 拦截 deepfake 与团伙 → 军备竞赛、漏报**）、robo-advisory（**组合优化/LLM → 民主化、低费 → suitability、过度信任**）、InsurTech（**CV/telematics/NLP → 快理赔、动态定价 → 逆向选择、公平**）、payments（**实时 ML/AI 路由 → <100 ms 止诈、降本 → 延迟、规避**）、RegTech（**NLP/GNN/监察 → 合规自动化 → 误报洪水**）。规律：**价值越大，风险越集中于 fairness / false positives / adversarial evasion**。
2. **GNN 直觉**（§2）：**nodes = 账户/商户/设备/电话，edges = 交易/共享设备/共享地址**；行级 ML（LR、XGBoost）只看**一行特征**，看不见"12 个 mule 同时向 3 个坏账户转账"这种**网络信号**；欺诈者故意让**每笔交易小额可信**；可识别模式三种——**funnel account（高入度 + 高出度 + 低余额留存）、layering（长链 pass-through）、mule network（共享设备/地址并汇至同一 cash-out）**；GNN 沿边**传播**、几轮后节点表示编码**局部邻域**，从而**大幅降误报**。
3. **算法交易与执行算法**（§3）：五步（**策略设计 → 回测 → 执行基础设施 → 风险控制 → 监控**）；回测三陷阱（**lookahead bias、survivorship bias、overfitting**）；**算法占美股成交量 60–70%**、**HFT 占 50–60%**、**HFT 延迟微秒级**、**co-location** 与 **Spread Networks 3 亿美元 / 3 毫秒**；**VWAP = Σ(P_t×V_t)/ΣV_t**（按量、适合流动性好且量可预测）、**TWAP = ΣP_t/N**（按时间、适合流动性差/量不可靠）、**implementation shortfall**（最小化决策价与执行价之差，兼顾冲击与机会成本）；**urgency vs market impact：快=冲击，慢=价格漂移**。
4. **RL 基础**（§4）：**agent / environment / state / action / reward** 五组件及交易映射；**policy** 确定性 π: S → A 与随机 π(a|s)（随机策略在部分可观测/对抗环境必要）；**V(s) = E[future reward | S_t=s]**、**Q(s,a) = E[future reward | S_t=s, A_t=a]**（有 Q 即可"选最大"得策略）；**Bellman：V(s) = r + γ·V(s′)**，**γ→1 长视、γ→0 短视**，折现三理由（未来不确定、货币时间价值、数学收敛）。
5. **三类 RL 方法**（§5）：**value-based**（Q-learning、SARSA、**DQN**；稳定简单；仅离散小动作、探索弱）；**policy-based**（**REINFORCE、PPO**；连续动作、随机策略；高方差、样本饥渴、局部最优）；**actor-critic**（**A2C、DDPG、SAC**；低方差、复杂高维；实现复杂、不稳定、算力重）；**选择规则：离散→value-based；连续→policy/actor-critic；复杂→actor-critic**。
6. **RL 训练技巧**（§6）：①多源数据（新闻情绪、社媒、经济指标，**不能只用历史价格**）；②更高频（更多转移，但噪声与算力上升）；③**多目标奖励 reward = PnL − λ1·inventory vol − λ2·slippage − λ3·fees**，λ 可按 regime 自适应；④**简化动作**（离散 buy/sell/hold 优于连续二维）；⑤**谨慎丰富状态**（order imbalance、price-volume slopes、micro-price impact、trade density，**EWMA 去噪**，且**必须实时可得、不许未来信息**）。
7. **RL 结构性局限**（§7）：**sim2real gap**（模拟器无法建模自身交易的市场冲击与对手反应；缓解=domain randomization、历史回放、shadow accounts、回撤上限）；**数据有限且非平稳**（缓解=**PSI/KS 概念漂移检测**触发重训、**prioritized experience replay**）；**低 SNR**（需手工特征工程，带来专家偏差、限制扩展）；**无动作标签**（只有标量奖励→训练慢且不稳定、探索-利用张力、**不保证收敛**）。
8. **FinRL**（§8）：AI4Finance Foundation 的**首个面向量化金融的开源 DRL 库**（arXiv:2011.09607）；四段流水线 **环境 → 训练（DQN/DDPG/PPO/A2C/SAC）→ 回测 → 评估**；角色是**替你处理 RL 机械（训练循环、replay buffer、算法实现），你专注 state design / reward engineering / evaluation——领域知识与 alpha 所在**；**backtest ≠ live，FinRL 是假设生成器而非印钞机**。

**附：易混数字速记**

| 数字/事实 | 归属 |
|---|---|
| **60–70%** | 算法交易占**美股成交量** |
| **50–60%** | **HFT** 占美股成交量 |
| **>50%** | 2025 年涉及 AI/deepfake 的**欺诈占比** |
| **<100 ms** | 支付实时欺诈评分决策时限（allow/challenge/block） |
| **10–30%** | 优化执行带来的**交易成本降幅** |
| **0.25% vs 1–2%** | 智能投顾费率 vs 人工投顾费率 |
| **3 亿美元 / 3 毫秒** | Spread Networks 芝加哥—纽约光纤 |
| **€220,000 ($243K)** | 2019 年语音克隆诈骗金额 |
| **100,000 股 / 390 分钟 / 100 张子单** | VWAP-TWAP 案例参数 |

---

## 本讲与 group project 的关系

> 原则：只写 L8 原文明确支持的内容，不作推断。

**1. FinRL 被原文明确称为课程项目的起点参考。** 第 48 页原文：FinRL "**designed for education and research — an excellent starting point for course projects and demos**"。这是本讲唯一一处直接提到 **course projects** 的表述。

**2. 原文界定了"库做什么、你做什么"的分工。** 第 49 页：FinRL 负责 **RL machinery（training loops、replay buffers、algorithm implementations）**，学生应把精力放在 **state design、reward engineering、evaluation** 这三个金融特有决策上——原文称"**那正是领域知识所在，也是 alpha（若有）所在**"。若项目采用 RL 路线，这三项就是需要自己设计并在报告中论证的部分。

**3. Case Study 2 提供了一条可直接照搬的链路模板。** 第 54–55 页：**Dow 30 → 环境（OHLCV + 技术指标 + 当前权重；动作为连续组合权重；奖励为日收益减交易成本）→ 训练 PPO → 留出期回测（累计收益、Sharpe、最大回撤）→ 与 buy-and-hold 比较**。同时原文给出必须写进结论的限定：**backtest ≠ live**，结果只应作为 **hypothesis generator**，因为 **sim2real gap**（训练/测试市场不会对 agent 的交易作出反应）。

**4. 需核实的一处**：本任务提到的"若难以展示所有公司报表，可用其他平台/数据源但须引用标注"这一表述，**在 `lecture_08_extracted.txt` 全 67 页中未出现**（已对 project / platform / data source / cite / citation / report / annual 等关键词逐一检索，与 course project 相关的仅第 48 页 "course projects and demos" 一处）。该要求更接近 **L1 的 Group Project 说明（LLM Research Agent，见 L1 附录 B）** 与 **L6 的引用纪律（每个数字必须标注来源，缺失则写 "data unavailable"）**，引用时应以 L1 / L6 原文为准，不宜归到 L8。

> 💡 一句话：**L8 对项目的直接贡献是"工具 + 模板 + 警告"——FinRL 是起点，PPO 回测是模板，sim2real 是必须在报告里承认的边界。**
