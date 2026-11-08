# news104 开波设计：论坛+论文取证 + 模板池（2026-11-03）

## 一、数据集与字段面（get_datafields 实拉，cov 0.963 全字段）

news104 Archive News Data（category=news 非目标塔，11 字段，ac 100/uc 57，金字塔 x1.8）——事件级 VECTOR，须 vec_ 聚合。

| 字段 | 语义 | 机制角色 |
|---|---|---|
| nws104_sentiment | 三元情绪 1/0/-1 | 主信号质量 |
| prob_pos/prob_ntr/prob_neg | 三概率（和=1，成分数据） | 分布层净情绪/确信度 |
| relevance | 1=主提及,<1=次要 | 加权/门控（论坛 WL27618） |
| novelty | 1=首发,>1=24h 内重复/更新 | 新奇度过滤（论坛 WL27618） |
| confidence | 情绪置信 0-1 | 质量门控 |
| marketimpactscore | -5..+5 前向 1 分钟影响估计 | 影响面 |
| automessage/headlineonly | 自动推送/仅标题旗标 | 噪声结构 |

## 二、论坛取证（search_forum_posts 2026-11-03）

| 帖 | 要点 | 对模板的启示 |
|---|---|---|
| WL27618《别再用裸 sentiment——relevance 加权+新颖度过滤》31 赞 | 裸 ssc 排序 S 波动大；不是每条新闻都值得定价 | T2/T3：relevance 加权、novelty 过滤 |
| YW86963《财报电话会"情绪概率差"》EUR 事件情绪+低相关设计 15 评 | [正/中/负]三概率是分布，「正面概率−负面概率」是分布层净情绪 | T1/T4：prob 差与确信质量 |
| RR65633《WSJ 悲观度→短期反转与量》 | 悲观度每 1 std 次日 -8.1bp（负向→反转买入） | T9：负情绪集中=反转面 |

## 三、论文取证（web_search 2026-11-03）

- **Didisheim et al. (2026) The inefficient pricing of news**（670 万 Reuters 文章）：「纯新闻」=文章中不可预测残差——意外成分强预测未来收益；**负面语气+密集数字内容的题材反应不足、模糊/高媒体关注的题材过度反应** ⇒ T3 新奇/意外面 + T9 反转面双向先验。
- Barber-Odean (2008) 注意力与新闻驱动买入；Tetlock (2007) 媒体悲观度预测次日反转 ⇒ 短窗（5 日内）设计。
- Nikkei DeBERTa：human vs investor 双视角情绪互补 ⇒ 分类器分歧面（sentiment vs prob 差背离）可做独立臂。

## 四、模板池（12 个结构互异 ✓）

骨架约定：事件级 VECTOR 先 vec_ 聚合→时间层加工→group_rank/subindustry 分组（水平型判据：新闻情绪是「今天变了」时效型，允许 ts 归一化；计数/规模面一律 ts_rank/ts_ir 去规模混淆）。全波 DEU/TOP500/D1/SUBINDUSTRY/decay4/trunc 0.08。

| # | 机制 | 表达式 | 来源 |
|---|---|---|---|
| T1 | 分布层净情绪 | `group_rank(ts_mean(subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg)), 5), subindustry)` | forum YW86963 |
| T2 | relevance 加权净情绪 | `group_rank(ts_mean(multiply(subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg)), vec_avg(nws104_relevance)), 5), subindustry)` | forum WL27618 |
| T3 | 新奇度结构 | `group_rank(ts_ir(vec_avg(nws104_novelty), 22), subindustry)` | forum WL27618 + paper 新奇定价 |
| T4 | 确信质量（去中性质量） | `group_rank(ts_mean(subtract(1, vec_avg(nws104_prob_ntr)), 5), subindustry)` | 论文成分数据 |
| T5 | 影响质量 | `group_rank(ts_ir(vec_sum(nws104_marketimpactscore), 22), subindustry)` | 字段机制 |
| T6 | 情绪脉冲 | `group_rank(ts_ir(ts_mean(vec_sum(nws104_sentiment), 5), 22), subindustry)` | 自建·时效型 |
| T7 | 密度×净情绪 | `group_rank(multiply(vec_count(nws104_sentiment), subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg))), subindustry)` | GBR vec_count×similarity 骨架迁移 |
| T8 | confidence 加权 | `group_rank(ts_mean(multiply(subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg)), vec_avg(nws104_confidence)), 5), subindustry)` | Nikkei 双视角 |
| T9 | 负情绪反转面 | `group_rank(subtract(0, ts_mean(vec_avg(nws104_prob_neg), 5)), subindustry)` | forum RR65633 + paper 反应不足 |
| T10 | 噪声流结构 | `group_rank(subtract(1, ts_mean(vec_avg(nws104_automessage), 5)), subindustry)` | 自建·信息质量 |
| T11 | 持续性密度 | `group_rank(ts_sum(greater(subtract(vec_avg(nws104_prob_pos), vec_avg(nws104_prob_neg)), 0), 22), subindustry)` | 自建 |
| T12 | 情绪-影响背离 | `group_rank(ts_ir(subtract(vec_sum(nws104_marketimpactscore), vec_sum(nws104_sentiment)), 22), subindustry)` | Nikkei 互补视角 |

**窗口理由**：5/22 均白名单（短窗=新闻定价滞后天级）；T3/T5/T6/T12 用 ts_ir(22) 归一去规模。

**量纲自检**：prob/relevance/novelty/confidence 均 0-1 无量纲可乘；marketimpactscore(-5..+5) 与 sentiment(-1..1) **不同量纲禁直接 add**（T12 已改为 subtract 前各自 vec_sum——⚠ 复查：subtract 两不同量纲字段也可能 UNITS 告警，预检观察，若有告警改为各自 group_rank 后再差）。

**验收预锁**：prod<0.7 + self<0.70 + S≥1.58 + 2Y≥1.58 + RA=0 + 覆盖无连续多年空窗。

## 五、波 1 收批（2026-11-03 05:50 全 12/12 收齐，runner 正常收尾）

| 臂 | alpha | S | F | TO | 读数 |
|---|---|---|---|---|---|
| T1 净情绪差 | LLMdE3W6 | -0.24 | -0.04 | 0.446 | 弱反向 |
| T2 relevance 加权 | 9qx78kY9 | -0.16 | -0.02 | 0.442 | 弱 |
| T3 新奇度 | MPYLdEko | 0.24 | 0.07 | 0.177 | 全波最大但远低于闸 |
| T4 确信质量 | leA3Enrx | 0.16 | 0.02 | 0.413 | 弱 |
| T5 影响质量 | qML6Y8oO | 0.11 | 0.02 | 0.155 | 弱 |
| T6 情绪脉冲 | LLMdmWAv | 0.16 | 0.03 | 0.166 | 弱 |
| T7 密度×净情绪 | P0oOYrwM | 0.03 | 0.00 | 1.265 | 交互臂死（TO 还爆） |
| T8 confidence 加权 | YP1gEw2J | -0.20 | -0.03 | 0.447 | 弱反向 |
| T9 负情绪反转 | YP1gEA9v | 0.18 | 0.03 | 0.402 | 弱 |
| T10 噪声流 | wpQE2evQ | -0.19 | -0.06 | 0.333 | 弱 |
| T11 持续性密度 | A1V7rNaR | 0.03 | 0.00 | 0.118 | 死 |
| T12 情绪-影响背离 | O0AxMNmv | -0.13 | -0.03 | 0.161 | 弱 |

**族判死定案**：12/12 臂 |S|<=0.24，含条件/交互假设臂（T7/T8/T12）也全弱——「信号只在条件侧」假设被否定。DEU news104 概率成分新闻情绪在 SUBINDUSTRY 分组的直接形态下无可用信号，**该族封盘，不再加变体**（归因纪律：全波收齐才判，判死即封）。方向观察：情绪臂普遍微弱负向（与重庆大学论文的 DEU 反应过度一致），但幅度全是噪声级，不足以支撑反转模板续挖。
