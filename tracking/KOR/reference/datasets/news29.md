# news29 — Significant Developments Data（KOR / TOP600 / D1）

> 画像日期：2026-11-17 · 数据源：`get_datafields(dataset_id=news29, region=KOR, universe=TOP600, delay=1, filter_sharpe=false, 不传 max_fields)`。
> 三重对账：`count=12 == platform_count=12`，`complete=true`。字段全量 12/12，**无抽样**。
> 归档：`tracking/KOR/reference/datasets/<dataset_id>.md`（手工维护）。

## 1. 数据集体征

| 项 | 值 |
|---|---|
| 字段数 / 类型 | **12 / 12 全 VECTOR** |
| 数据集级覆盖 | 0.467（field 级 0.0095–0.8649；以 field 级为准）|
| aC | 全集 aC ≤ 11（最高 `nws29_topic1`=11）⇒ **极冷门** |
| 经济轴 | 事件**重要性**（significance）× 头条标记（frontpage）× 主题码（topic）|

## 2. 字段族（按 description）

### 族 A — 重要性（可当信号，须反向）
| 字段 | cov | aC | description 要点 |
|---|---:|---:|---|
| `nws29_significance` | 0.2459 | 5 | 重要性 **1=High/2=Med/3=Low** ⇒ 数值越小越重要，须取负/反向 |
| `nws29_full_significance` | 0.8649 | 4 | 同上，Full 版覆盖更高（名 vs desc 差异：两个版本同机制）|

→ 预处理：cov 0.246/0.865；低覆盖版须 `ts_backfill`；one-hot 型整数 ⇒ `vec_avg` 后 `group_rank`，不必 `ts_delta`（非单边恒正流量，是等级码）。

### 族 B — 头条标记（稀疏二值）
`nws29_frontpage` 0.2459/aC3、`nws29_full_frontpage` 0.8649/aC1 → 1=Reuters 头条。
→ 稀疏二值 ⇒ `trade_when(>0, signal, -1)` 门控，禁裸 rank。

### 族 C — 主题码（只作分组轴，禁算术）
`nws29_topic1` 0.2459/aC11、`nws29_full_topic1` 0.8649/aC0、`event_secondary_topic_code` 0.8649/aC1、`event_tertiary_topic_code` 0.8649/aC0、`nws29_topic2` 0.0409/aC2、`nws29_topic3` 0.0095/aC0 → 编码字段，只作 group 参数。

### 族 D — 文本（不作数值信号）
`company_event_headline_text_full` / `company_event_description_text_full` 0.2459/aC1 → 文本字段，六法不适用；若做 NLP 需外部模型，本轮不碰。

## 3. 头部字段先验（铁律 0.1）

1. `nws29_topic1` aC **11** — 主题码 ⇒ 头部轴 = **事件类型分类**，非重要性程度。
   **方向纠偏**：本集信息核心在「事件类型 × 重要性」，纯重要性单腿方向可能偏——优先做「重要性在主题内的相对排序」。
2. `nws29_significance` aC5、`nws29_full_significance` aC4、`nws29_frontpage` aC3。

## 4. 可用性 / 分布 / 频率（静态推定 [inferred]）

- 类型：全 VECTOR → `vec_avg` 先聚合。
- 分布：等级码 / 二值 ⇒ `point_mass` [inferred]，门控 + `group_rank`，禁 `ts_zscore` 直接上。
- 频率：事件驱动 [inferred]，窗口 ≥63d。
- 近十年：须 `get_alpha_yearly_stats` 逐年验证。

## 5. 已试记录（追加，不覆盖）

### 5.1 「≥5 结构互异族 + 每族完整梯度」补齐战役（2026-11-22）
> 达标标准见记忆 template-family-count-rule / imbalance-news-template-gradient-compliance。KOR/TOP600/D1/INDUSTRY/decay4/trunc0.08。
> 论文闸 PASS（18 篇/10 作者，含 JFE《Multifrequency News and Stock Returns》）。
> 字段：仅 significance/frontpage 两族可作信号（topic 码只作分组、文本不碰）。族定义 H水平/G门控/E事件密度/B比率/R分位。

**L1 外层全类别替换（逐族推进）**
| 族 | wave | 最优 | S | 2Y | 判 |
|---|---|---|---:|---:|---|
| H 重要性 | `s2_news29_T1_significance_L1_d1` | `aka86d3w` `group_rank(full_sig)` | 0.39 | 0.95 | 正向（重要度高→跑赢）优于反向（−0.49）；**全臂 CW=1.0 超闸**（one-hot 等级码权重集中）|
| G 头条门控 | `s2_news29_T2_frontpage_L1_d1` | `6XMQ8Z0P` `trade_when(frontpage>0,·)` | 0.22 | 0.39 | 门控后 longCount=2 极稀疏、CW=0.5；头条二值无定价力 |
| R 分位/差分/密度 | `s2_news29_T3_quantile_L1_d1` | `KPgpd1zx` `-ts_delta(66)` | 0.56 | 0.83 | 反号差分 S0.56 但 TO0.0092 过低+CW0.5；**全臂 CW=1.0**（quantile/zscore/rank）；std_dev `e7aPwjVd` S0.38 但 2Y−0.49 |

**L1 结论**：H/G/R 三族（含 D 差分/B 比率/E 事件密度变体）24 臂全灭、0 near；**CW=1.0 是结构性主墙**——significance/frontpage 是 one-hot 等级码/稀疏二值，横截面大量并列⇒极端权重集中。最高正 S0.39–0.56 全卡 CW/TO。

### 5.2 L2 内层时序全类别替换（验证平滑窗能否修 CW）
| 族 | wave | 内层替换最优 | S | 判 |
|---|---|---|---:|---|
| H | `s2_news29_T1_significance_L2_d1` | `kqaM2ovd` `ts_mean(44)` | 0.49 | 内层 S0.49/2Y1.24 但 CW=1.0；平滑窗降 CW 的臂（mean126 CW0.14/backfill66 CW0.18）S 塌到 0.02–0.12 ⇒ **CW 与 S 互斥，平滑窗无法在保 S 同时修 CW** |
| R | `s2_news29_T3_delta_L2_d1` | `QP0AXwXW` `decay(delta66,44)` | 0.56 | 反号差分 S0.56/2Y0.83 但 TO0.0092 过低+CW0.5；⚠`leaYXoXO` S11.18 是零持仓病态臂（longCount=0/TO=1.0/2Y=0，checks.fail 三项），**非候选** |

### 5.3 收口判定（2026-11-22）
**news29 梯度补齐完成：H/G/R 三族（R 内含 D 差分/B 比率/E 事件密度变体）× L1+L2 = 7 wave / 56 臂，全部入库。**
- **族数诚实标注**：本集 12 字段仅 significance/frontpage 两族可作信号，topic 码只作分组轴、文本不碰。按模板族计数规则（字段族×算子几何×机制语义），实际可落地 **3 个结构互异族**（H 重要性水平 / G 头条门控 / R 相对偏离含差分比率密度变体）——**受字段落地性限制，凑不满独立 5 族**，不硬凑同构族冒充。
- **0 全闸、无真 near**：最高可读正 S0.49–0.56（H mean44 / R 反号差分），但 H 卡 CW=1.0、R 卡 TO0.0092+CW0.5；唯一"过 near 线"的 S11.18 臂是零持仓病态读数，非候选。
- **主墙 = CW=1.0 结构性权重集中 + 2Y 负**：significance 是 one-hot 等级码（1=High/3=Low）、frontpage 是稀疏二值，横截面大量并列⇒极端权重。L2 平滑窗验证 CW 与 S 互斥（降 CW 的臂 S 塌到 0.02–0.12，保 S 的臂 CW=1.0）；事件门控（G 族）longCount=2 极稀疏。
- **不判死**：记「梯度证据完整、信号层弱 + 等级码权重结构墙」；翻案需外部新信息源，不得外推其它 news 集。论文闸 PASS（JFE《Multifrequency News and Stock Returns》）。未提交任何 alpha。
