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

（待本战役波次写入）
