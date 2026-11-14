# GBR delay1 socialmedia12 GEM Ideas（TOP700 / INDUSTRY / decay6）

**Dataset**: socialmedia12
**Region**: GBR
**Delay**: 1

数据集：socialmedia12（6 字段，其中真信号字段仅 2 个 MATRIX：scl12_sentiment / scl12_buzz；其余为 entity_profile 类元数据）。六法在线评测 2026-11-14（批 `1aMpjN96D4nX8Fq15ymeeEet` @NONE/dec0/nanOFF）：
- 法1 覆盖：scl12_sentiment **lc/sc = 187/63 = 250/700（36%）**；scl12_buzz **352/0 = 50%**（元数据 cov=0.0 完全失真，实测有数据）
- 法2 非零：sentiment 251（与覆盖同）⇒ 零值可忽略；buzz 352（同覆盖）
- 法3 频率：sentiment N=22 变化 **590/700（84%）**、N=5 变化 382（55%）⇒ **日更偏高**；buzz N=22 变化 **619（88%）** ⇒ 日更
- 法6 形态：sentiment `ts_zscore>0` 占 **113/250 = 45%**（对 50% 参考）⇒ 近似对称，无强偏斜
- ★读数警示：**裸用时 buzz 的 lc/sc = 352/0 是纯单边多头暴露**（EUR 实证同类字段中性化后衰减 84-98%）⇒ 六法只作形态诊断，可交付性必须在 INDUSTRY 中性化后看。

死路规避：
- 不使用长 backfill（120）——论坛 GC81559/YR99599 双实证：长回填会**制造虚假覆盖**（把几个月前的一条记录填到今天），自相关极高、IS 虚稳。
- 不用 STATISTICAL 中性化（论坛实测 0.72 vs INDUSTRY 1.38）；不用 NONE（0.41）。
- decay 不用 ≥10（论坛实测 Sharpe 腰斩），取 4-6。

文献锚：
- **Tetlock (2007, JF)** 媒体内容→市场情绪→价格压力；**Bollen-Kapitan (2011)** Twitter 情绪预测日度市场；**MDPI (2025)《News vs. Social Media》**：Twitter 情绪的效应**持续为正且显著**，而传统新闻与搜索的效果更不规则。
- **论坛 HS65681（21 赞）**：USA D1 社媒情绪天花板 **0.63**（`ts_mean(ts_rank(twitter_sentiment_l2,20),20)` 模式）；aggregated 系列信息量是单源的 3 倍；**INDUSTRY 1.38 > STATISTICAL 0.72 > NONE 0.41**；decay **6 最优**（≥10 腰斩）。
- **论坛 QW94165（44 赞）**：社媒信号**衰减快**、需 **ts_mean 平滑去噪**、覆盖不足需回填。
- **评论 YR99599 的三点质询（重要防线）**：① INDUSTRY 高分可能来自「稀疏行业被裁票」而非剥离 beta ⇒ **必须看 lc/sc 与权重集中度**；② 高换手 + 低 margin 是提交硬约束；③ 覆盖必须实测非 NaN 票数，不看信号有无输出。

**Concept**: 社媒情绪水平（sentiment level）
- **Mechanism**: 社媒净情绪高 = 散户关注与买入压力为正（Tetlock 2007；MDPI 2025 实证 Twitter 情绪持续为正效应）；行业内相对化剥离「科技板块天然讨论度高」的行业 beta
- **Fields**: `scl12_sentiment`
- **Implementation Example**: `group_rank(ts_backfill({scl12_sentiment}, 5), industry)`
- **Direction**: 正
- **expected_exposure**: retail sentiment level（行业中性）

**Concept**: 社媒关注度 buzz 水平
- **Mechanism**: buzz = 相对情绪成交量，关注度本身携带信息（Barber-Odean 注意力交易）；但六法实测裸用 **352/0 纯单边**，必须在行业内相对化才可交付
- **Fields**: `scl12_buzz`
- **Implementation Example**: `group_rank(ts_backfill({scl12_buzz}, 5), industry)`
- **Direction**: 正
- **expected_exposure**: attention volume（行业中性）

**Concept**: 情绪 × 关注度共振（sentiment-buzz confirmation）
- **Mechanism**: 高情绪 + 高关注 = 真实的共识形成（而非少数噪音帖）；论坛实测两者结合优于单用。用同源对偶价差形式（rank 差）而非加权相加
- **Fields**: `scl12_sentiment`, `scl12_buzz`
- **Implementation Example**: `group_rank(subtract(ts_rank(ts_backfill({scl12_sentiment}, 5), 22), ts_rank(ts_backfill({scl12_buzz}, 5), 22)), industry)`
- **Direction**: 正（情绪相对关注度超配）
- **expected_exposure**: sentiment-minus-buzz divergence

**Concept**: 情绪动量（短期变化）
- **Mechanism**: 社媒情绪的**变化**先于价格（Bollen 2011）；论坛 HS65681 的最强模式即 `ts_mean(ts_rank(field,20),20)` 型（先时序排名再平滑）
- **Fields**: `scl12_sentiment`
- **Implementation Example**: `group_rank(ts_mean(ts_rank(ts_backfill({scl12_sentiment}, 5), 20), 20), industry)`
- **Direction**: 正
- **expected_exposure**: sentiment momentum（论坛最强基线复刻）

**Concept**: 情绪突增反转（over-attention reversal）
- **Mechanism**: 社媒关注突增常伴随散户追高与随后回落（Da-Engelberg-Gao 注意力反转）；GBR 的 sentiment27 实证：慢速水平优于脉冲，故本概念作为**对照臂**保留，不预设方向
- **Fields**: `scl12_sentiment`
- **Implementation Example**: `multiply(-1, group_rank(ts_zscore(ts_backfill({scl12_sentiment}, 5), 22), industry))`
- **Direction**: 负（反转假设）
- **expected_exposure**: attention spike reversal（对照）

**Concept**: buzz 关注度动量
- **Mechanism**: 关注度上升 = 增量资金入场（散户参与度提升）；用 5/22 双窗比值捕捉持续扩张而非单日尖峰
- **Fields**: `scl12_buzz`
- **Implementation Example**: `group_rank(divide(ts_mean(ts_backfill({scl12_buzz}, 5), 5), add(ts_mean(ts_backfill({scl12_buzz}, 5), 22), 0.001)), industry)`
- **Direction**: 正
- **expected_exposure**: attention expansion

**Concept**: 行业内情绪离散度（dispersion）
- **Mechanism**: 行业内社媒情绪的离散度高 = 分歧大（Miller 1977 分歧→高估→负收益）；用 group_std_dev 构造，是**分组轴特有**的结构信号
- **Fields**: `scl12_sentiment`
- **Implementation Example**: `multiply(-1, group_rank(group_std_dev(ts_backfill({scl12_sentiment}, 5), industry), industry))`
- **Direction**: 负（分歧大做空）
- **expected_exposure**: disagreement dispersion

多样性自检：Expected Exposure 6 种（情绪水平/关注水平/共振/动量/反转/分歧）✓；字段族 2（sentiment、buzz）✓；分组轴 industry 主 + sector/subindustry 备 ✓；时间尺度 4（5/20/22/252）✓；算子数 3-6 全部 ≤8 ✓。
⚠ 防御性约束（回应 YR99599）：每臂回报必查 **lc/sc 与 sub_universe_sharpe**，若 lc/sc < 100 即判定「稀疏剪裁」而非真信号。
