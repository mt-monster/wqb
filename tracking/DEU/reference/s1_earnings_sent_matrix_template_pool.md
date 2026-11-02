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
