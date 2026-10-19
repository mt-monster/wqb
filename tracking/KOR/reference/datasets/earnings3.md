# earnings3 — Earnings Date Data

> **字段画像档案** · KOR / TOP600 / Delay=1 · 生成日期 2026-07-19
> 数据来源：`get_datafields(dataset_id=earnings3, filter_sharpe=false)` 全量拉取（8/8，无字段被过滤）
> 关联：[`references/earnings.md`](../../../Claude/skills/wq-brain-ra-kor/references/earnings.md)

## 一、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | **8**（全部 MATRIX，无 VECTOR） |
| 结构 | **2 个日历口径 × 2 个时间方向 × 2 个量纲 = 2×2×2 严格矩阵** |
| coverage 分布 | 0.7756 × 2｜0.7232 × 2｜0.5825 × 2｜0.5599 × 2（**无字段 ≥0.8**） |
| 白空间（alphaCount ≤ 2） | **0 / 8**（最空字段 ac=199） |
| 塔 | earnings ×1.1 |
| **更新频率** | **事件驱动**：`*_interval` 是「距上次/下次财报的交易日数」，日更但**在财报日阶梯跳变**；`*_reptime` 是公告时刻编码 |
| 已提交 RA | 0（未点亮） |
| **综合判定** | ⚠ 待实测（机制成立、横截面有效性存疑，见 §五） |

## 二、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 字段 |
|---|---|---:|---|
| **E1 财报新鲜度** | **距上次财报已过交易日数**（`should be negative or zero` / `always non-positive`） | 4 | `ern3_all_delay_1_pre_interval`(cov .7232)、`ern3_pre_interval`(**cov .7756**，ac **616** 最拥挤) |
| **E2 财报倒计时** | 距下次财报交易日数 | 2 | `ern3_all_delay_1_next_interval`(cov .5599)、`ern3_next_interval`(cov .5825) |
| **E3 公告时刻** | 财报公告时刻（HHMM 或 session code） | 4 | `*_pre_reptime`(cov .7756 / .7232)、`*_next_reptime`(cov .5825 / .5599) |

**日历口径差异**（同族成对，易被误当独立字段）：

| 口径 | 含义 | pre_interval cov | next_interval cov |
|---|---|---|---|
| `ern3_*`（裸名） | 该股所属市场 | **0.7756**（更高） | 0.5825 |
| `ern3_all_delay_1_*` | **全部亚洲（ASI）** 统一日历，1 日延迟 | 0.7232 | 0.5599（更低） |

> ⚠ 裸名口径覆盖率全面高出 4–6 个百分点 ⇒ **优先用裸名口径**；ASI 口径覆盖更低，且 1 日延迟会引入时点错配。

## 三、字段全表

| # | 字段 | 类型 | cov | uc | ac | 类 | 单边性 | 可用性 |
|---|---|---|---:|---:|---:|---|---|---|
| 1 | `ern3_pre_interval` | MATRIX | **0.7756** | 281 | **616** | E1 | **单边非正**（always non-positive） | ⭐ 头部轴 |
| 2 | `ern3_pre_reptime` | MATRIX | 0.7756 | 241 | 536 | E3 | 离散编码 | ⚠ HHMM/session code，**非连续量，裸 rank 无意义** |
| 3 | `ern3_all_delay_1_pre_interval` | MATRIX | 0.7232 | 267 | 594 | E1 | 单边非正 | ⭐ 次优（同族，口径更宽但有 1 日延迟） |
| 4 | `ern3_all_delay_1_pre_reptime` | MATRIX | 0.7232 | 180 | 340 | E3 | 离散编码 | ⚠ 同 #2 |
| 5 | `ern3_next_interval` | MATRIX | 0.5825 | 137 | 285 | E2 | **单边正**（天数递减到 0） | ⚠ cov 0.58 < 0.6，且信息与 E1 互补性弱 |
| 6 | `ern3_next_reptime` | MATRIX | 0.5825 | 108 | 199 | E3 | 离散编码 | ⚠ |
| 7 | `ern3_all_delay_1_next_interval` | MATRIX | 0.5599 | 175 | 351 | E2 | 单边正 | ⚠ cov 最低 |
| 8 | `ern3_all_delay_1_next_reptime` | MATRIX | 0.5599 | 116 | 200 | E3 | 离散编码 | ⚠ |

## 四、0.1 字段质量先验（头部 = 最强经济轴）

按 `alphaCount` 降序：`ern3_pre_interval`(616) > `ern3_all_delay_1_pre_interval`(594) > `ern3_pre_reptime`(536) > `ern3_all_delay_1_pre_reptime`(340) > `ern3_all_delay_1_next_interval`(351)…

⇒ **头部轴 = 「距上次财报的交易日数」**（E1），且**裸名口径压倒 ASI 口径**。这与 0.2 的分类一致，无方向偏误。

## 五、A-1 五问 + A-2 收益来源声明

| 问 | 答案 |
|---|---|
| **1 时间维度** | **事件间隔**（距上次财报天数），非存量水平、非流量 ⇒ 日更但阶梯跳变 |
| **2 相对性** | 排序差异 ⇒ `rank` / `group_rank` |
| **3 被定价的是谁** | **广度**（事件时点分布）而非强度 —— 本数据集**没有** surprise / actual 字段，只有日期与时刻 |
| **4 有无博弈** | 无拥挤博弈；但 cov 0.78 ⇒ 22% 股票无值 ⇒ **禁裸 rank**（会迫成等权多头） |
| **5 事件性** | **是** ⇒ 必须门控或控换手（用 `ts_target_tvr_decay`，非 `hump`） |

**A-2 收益来源声明**：

- **谁在被定价**：财报公告前后的**信息不对称交易者**（公告后价格漂移的接受者）
- **为什么会被错**：**注意力有限** —— 财报信息量大、需逐条解析，投资者只对头条反应，漂移延续数周
- **错了多久修复**：**数日至数周**（PEAD 经典 1–3 个月，本区按 22d 窗实现）
- **预期方向**：**新鲜财报 → 后续漂移**（方向取决于好坏，本数据集无 surprise 字段 ⇒ 只能做「新鲜度」方向，方向句为「最近发布财报的股票相对更活跃/更具信息含量」）

> ⚠ **机制上的诚实边界**：经典 PEAD 依赖「好坏」判断，而本数据集**只有日期没有数值**，
> 因此能做的是**财报新鲜度/事件临近度**，不是真正的 PEAD。这是机制强度的主要折扣项，
> 也是本数据集预期 S 不高的原因。

## 六、预处理决策（②.b 直接查表）

| 读数 | 决策 |
|---|---|
| `pre_interval` **单边非正** | ⇒ **铁律 A**：`ts_delta(F, N)` 取变化率（财报事件本身在 `ts_delta` 上表现为正向跳变）；或取 `-F` 还原为「天数」正向 |
| cov 0.7756（<0.8） | ⇒ `ts_backfill(F, 66)` 前置（季频事件，窗口取 66d） |
| 事件驱动、阶梯跳变 | ⇒ 控换手用 **`ts_target_tvr_decay(·, target_tvr=0.22)`**，**禁用 `hump`**（实测极敏感） |
| 0.5 < cov < 0.6（E2） | ⇒ 覆盖偏窄，多头被压窄，优先级下调 |
| MATRIX（无 VECTOR） | ⇒ 不需 `vec_*` 降维 |
| 全组**无字段 ≥0.8 cov** | ⇒ 任何形态都必须 backfill，禁裸 rank |

## 七、待测清单（按机制分组）

| 组 | 候选表达式骨架 | 机制 |
|---|---|---|
| **G-新鲜度** | `ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(-ts_backfill(ern3_pre_interval,66)), std=0.24), sector), 3.5), target_tvr=0.22)` | 财报新鲜度排序 |
| **G-事件跳变** | `ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(ts_backfill(ts_delta(ern3_pre_interval,66),66)), std=0.24), sector), 3.5), target_tvr=0.22)` | 财报发生事件（铁律 A 形态） |
| **G-倒计时** | 同上换 `ern3_next_interval` | 财报临近效应 |

## 八、结论

- **机制成立但强度存疑**：本数据集是「财报日期/时刻」而非「财报惊喜」，只能做新鲜度与事件临近，
  无法做经典 PEAD ⇒ 预期 S 中等（参照同区 `news_sentiment_transfer` S 0.07、`macro63` 全零的量级）。
- **必须 backfill**：全组 cov < 0.8，裸 rank 会退化。
- **头部轴已确认**（`ern3_pre_interval`，裸名口径），与 0.2 分类一致，无方向偏误 ⇒ 可直接组装。
- **三个骨架各 1 条探针即可给出结论**；若 S < 1.0 则本数据集判死。