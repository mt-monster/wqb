# earnings_sent_matrix 模板池（DEU/TOP500/D1）—— 2026-11-03

## 取证来源
- 论坛 43620895448343（YW86963，EUR 实测 alpha XgbXWEWm）：概率差 > argmax 标签（S 1.2-1.5）；signed_power(·,3) 把 prod 0.9→0.64；事件稀疏期 CW 病根（2014-01 单票 10.78%），trunc 0.08→0.04 修；backfill 250 缓解覆盖但 S 掉 1.3。
- 论坛 43691562191895（KK37637）：事件窗变化 > 绝对水平；Q&A vs 演讲稿、CEO vs 高管差异（本数据集无分段字段，用双周期/标签跳变近似）。
- 论文① Loughran-McDonald 系（annual report tone → distress/returns）：负面语气=风险，方向先验「净情绪正→多」。
- 论文② Earnings conference calls & textual tone 增量信息（Huang-Lehavy-Zang-Zheng 系）：电话会语气对截面收益有增量预测力。

## 字段真身（平台实查 2026-11-03，仅 7 字段，MATRIX 型）
P=positive_sentiment_probability_3(ac76) / N=negative_sentiment_probability_3(27) / U=likelihood_of_neutral_tone(31) /
W1=sentiment_weighting_method1(38) / W2=sentiment_weighting_method2(15) / L=overall_sentiment_score(10,argmax标签) / intraday_delay_indicator(4,不作信号)
⚠️ 论坛帖的 polarity/confidence/surprise/_5 变体在 DEU 不存在——双腿差自算 subtract(P,N)。

## 12 互异模板（结构轴：时序z差 / 截面rank / 不确定性 / 事件变化 / 水平 / 双周期价差 / 分歧度 / 秩尾放大 / 事件门控 / 衰减记忆 / 标签跳变 / 方法背离）
| # | 骨架 | 机制 | 来源 |
|---|---|---|---|
| T1 | signed_power(subtract(ts_zscore(P,252), ts_zscore(N,252)), 3) | 净语气时序标准化+保号幂（降 prod） | 论坛主模板 |
| T2 | group_rank(subtract(P,N), subindustry) | 净情绪截面 | 论文① |
| T3 | subtract(0, group_rank(U, subindustry)) | 语气模糊=不确定=利空 | 论文②+论坛评论 |
| T4 | group_rank(ts_delta(subtract(P,N), 22), subindustry) | 语气环比转变（事件窗变化>水平） | 论坛 43691562191895 |
| T5 | group_rank(W1, subindustry) | 加权 tone 水平基线 | 论文② |
| T6 | subtract(ts_zscore(D,22), ts_zscore(D,252))，D=subtract(P,N) | 短窗情绪相对长窗偏移（同机制双周期价差） | 自建 |
| T7 | subtract(0, group_rank(add(P,N), subindustry)) | 情绪极端/分歧大=风险 | 自建（分歧度） |
| T8 | group_neutralize(signed_power(subtract(group_rank(D, subindustry),0.5),3), subindustry) | 秩尾放大壳（有界秩输入增益最大） | memory 实证 |
| T9 | trade_when(greater(ts_rank(D,252),0.75), signed_power(subtract(group_rank(D,subindustry),0.5),2), 0) | 高情绪事件窗稀疏入场（避 CW） | 论坛 CW 修法+trade_when |
| T10 | group_rank(ts_decay_linear(D,22), subindustry) | 事件型短窗衰减记忆（近期事件权重高） | 自建 |
| T11 | group_rank(ts_delta(L,66), subindustry) | argmax 标签跳变=基调切换事件 | 论坛（标签弱但结构对照） |
| T12 | subtract(0, subtract(group_rank(W1,subindustry), group_rank(W2,subindustry))) | 双聚合法背离=测量不确定性=利空 | 自建（同概念双方法净额，合规） |

方向先验：T1/T2/T4/T5/T6/T8/T9/T10/T11 高值→做多（净情绪正）；T3/T7/T12 已取负（风险向）。
设置：DEU 标准 decay4/trunc0.08/SUBINDUSTRY。⚠️ CW 预案（论坛病根）：撞 CONCENTRATED_WEIGHT 时 trunc 0.08→0.04 本地对照。
合规自查：无 add/subtract 双独立信号腿（D=P−N 与 W1−W2 均为同机制净额）；窗口 22/66/252 全白名单；trade_when 三参齐。
---

## 波 1 全景归因（2026-11-03，12/12 收批，DEU 标准设置）

| # | alpha | S | 2Y | F | TO | margin | fRA | 闸型 |
|---|---|---|---|---|---|---|---|---|
| T1 论坛主模板 | vR1vK6Vr | 0.24 | 0.48 | 0.07 | 72.7% | 1.7bp | 6 | TO+CW+LOW_SUB 全撞 |
| T2 净情绪截面 | vR1vRRRd | −0.05 | −0.16 | −0.01 | 72.7% | −0.3bp | 6 | 同上 |
| T3 不确定性利空 | e75xlv6g | −0.25 | 0.41 | −0.07 | 73.1% | −1.8bp | 6 | 方向翻车 |
| T4 语气转变 | npv8pZL3 | 0.07 | −0.12 | 0.01 | 3.6% | 1.8bp | 5 | 稀疏✓ 无信号 |
| T5 W1 水平 | LLMdLgrv | −0.07 | −0.21 | −0.01 | 72.5% | −0.5bp | 5 | 全撞 |
| T6 双周期价差 | KPJEPKNN | 0.22 | −0.32 | 0.06 | 42.1% | 1.6bp | 4 | 弱 |
| T7 分歧度 | kqNZqLdk | 0.22 | −0.50 | 0.06 | 73.1% | 1.6bp | 5 | 全撞 |
| T8 秩尾放大壳 | N1NRxQG7 | −0.06 | −0.11 | −0.01 | 72.6% | −0.4bp | 6 | **壳对零基信号无效（放大噪声）** |
| T9 事件门控 | zq3RqbNX | **0.62** | 0.41 | 0.36 | **3.1%** | **27.6bp** | 4 | CW 0.5/0.1（论坛病根） |
| T10 衰减记忆 | LLMdVRLm | 0.06 | −0.10 | 0.01 | 72.1% | 0.4bp | 6 | **ts_decay_linear 不降 TO（事件字段）** |
| T11 标签跳变 | 3qoeQgk6 | 0.19 | 0.49 | 0.10 | 8.2% | 7.7bp | 4 | 稀疏✓ 弱 |
| T12 方法背离 | gJe9kQNQ | −0.01 | −0.30 | 0.00 | 21.2% | −0.2bp | 5 | 死 |

### 归因（按模板族）
1. **幅度缺口是根本问题**：全场 S ∈ [−0.25, 0.62]，最强 T9 距闸 1.58 差 **2.5 倍**。论坛 EUR 配方（S 1.65-1.9）**不迁移 DEU/TOP500**——与 SLOW 配方教训同型。
2. **稀疏结构修 TO 不修幅度**：trade_when（T9 TO 3.1%）与 ts_delta（T4 TO 3.6%）把换手打到健康区，但幅度不动；非稀疏模板（T1/T2/T3/T5/T7/T8/T10）全撞 TO 72%+ 与 CW。
3. **两个算子事实**：① ts_decay_linear(·,22) 对事件字段**不降 TO**（72%），别拿它当平滑降换手杠杆；② 有界秩放大壳对 S≈0 的基信号**无效**（T2 −0.05 → T8 −0.06），壳只能放大已有信号、不能创造信号。
4. **CW 病根复现**（T9 CW 0.5/0.1）与论坛诊断一致（事件稀疏期单票超重）；但 trunc 0.04 只修 CW 不修 S 0.62，单发 CW 探针不改变结局。

### 波 1 终判：**封盘**
- 12 互异模板（含论坛 EUR 实测配方 + 论文先验 + 3 个自建机制轴）全族扫尽，无一触及 S 1.0。
- 唯一正收益方向=事件稀疏门控（T9/T11 族），但幅度缺口 2.5 倍不可由设置杠杆补齐。
- **备选矿脉（未投）**：earnings_call_*（ac=45，2012 起）接 earnings6 的 surprise 做「语气×业绩意外」双数据集组合（须查塔配额：earnings 类非 trio，可与目标塔组但限 3/组合）。

