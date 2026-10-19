# other106 — KOSPI 200 Index（成分股变更快照）

> **字段画像档案** · KOR / TOP600 / Delay=1 · 生成日期 2026-07-19
> 数据来源：`get_datafields(dataset_id=other106, filter_sharpe=false)` 全量拉取（15/15）
> 关联：[`references/other.md`](../../../Claude/skills/wq-brain-ra-kor/references/other.md)

## 一、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | **15**（**全部 VECTOR**，无 MATRIX） |
| 结构 | **4 组 `_cls`/`_nxt`（变更前/变更后）配对** + 4 个分类编码 + 1 个价格对 + 1 个事件字段 |
| coverage | **全部 0.4032–0.404**（极窄且高度一致） |
| 白空间（alphaCount ≤ 2） | **0 / 15**（最空字段 ac=9） |
| 塔 | **macro ×1.4**（⚠ 平台实测分类为 `macro`，非 `other`；`pyramids.list` 回读为 `KOR/D1/MACRO`） |
| **更新频率** | **事件驱动 + 快照式**：`_cls` 与 `_nxt` 是**一次变更的前后两个时点**，非时间序列 |
| 已提交 RA | 0 |
| **综合判定** | ❌ **判死**（1 条探针 S −0.16；有效截面失衡 longCount 136 / shortCount 463） |

## 二、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 字段 |
|---|---|---:|---|
| **K1 权重因子** | 指数调整权重因子 / 自由流通因子 / CAP 率 | 6 | `adjusting_factor_cls|_nxt`、`free_float_factor_cls|_nxt`、`capping_factor_cls|_nxt` |
| **K2 指数权重** | **INDEX SHARE（指数内权重）** | 2 | `index_share_cls`(ac 23) / **`index_share_nxt`(ac 55，头部轴)** |
| **K3 价格快照** | 变更前/后收盘价 | 2 | `price_cls`(ac 27) / `price_nxt`(ac 17) |
| **K4 分类编码** | 指数代码 / KOSPI 6 位代码 / KRX 行业代码 | 4 | `index_code1`(15)、`index_code2`(9)、`ksic_cls`(14)、`slc_ciik`(11) |
| **K5 股本事件** | **配股新增股份** | 1 | `newshares_following_rightsissue`(ac 41) |

> ⚠ **`_cls` / `_nxt` 不是时间窗，是同一事件的前后快照** ⇒ 二者相减 = **一次变更事件的发生量**，
> 这是本数据集唯一有真实信息的方向；单独使用任一侧只是「变更前的权重水平」或「变更后的权重水平」，属存量代理。

## 三、字段全表

| # | 字段 | 类型 | cov | uc | ac | 类 | 可用性 |
|---|---|---|---:|---:|---:|---|---|
| 1 | **`oth106_ospi_ca_eq_index_share_nxt`** | VECTOR | 0.404 | 40 | **55** | K2 | ⭐ **头部轴**：变更后指数权重 |
| 2 | `oth106_ospi_ca_eq_price_cls` | VECTOR | 0.404 | 23 | 27 | K3 | ⚠ 价格为存量代理 |
| 3 | `oth106_ospi_ca_eq_index_share_cls` | VECTOR | 0.404 | 17 | 23 | K2 | ⭐ 与 #1 配对，**差分即事件** |
| 4 | `oth106_ospi_ca_eq_newshares_following_rightsissue` | VECTOR | 0.4032 | 22 | 41 | K5 | ⚠ 配股稀释事件（独立机制） |
| 5 | `oth106_ospi_ca_eq_adjusting_factor_nxt` | VECTOR | 0.4032 | 26 | 30 | K1 | ⚠ 与 #6 配对 |
| 6 | `oth106_ospi_ca_eq_adjusting_factor_cls` | VECTOR | 0.404 | 17 | 20 | K1 | ⚠ |
| 7 | `oth106_ospi_ca_eq_capping_factor_cls` | VECTOR | 0.404 | 19 | 19 | K1 | ⚠ |
| 8 | `oth106_ospi_ca_eq_capping_factor_nxt` | VECTOR | 0.404 | 11 | 13 | K1 | ⚠ |
| 9 | `oth106_ospi_ca_eq_free_float_factor_nxt` | VECTOR | 0.404 | 16 | 19 | K1 | ⚠ 与 #10 配对 |
| 10 | `oth106_ospi_ca_eq_free_float_factor_cls` | VECTOR | 0.404 | 16 | 19 | K1 | ⚠ |
| 11 | `oth106_ospi_ca_eq_price_nxt` | VECTOR | 0.404 | 15 | 17 | K3 | ⚠ |
| 12 | `oth106_ospi_ca_eq_index_code1` | VECTOR | 0.404 | 13 | 15 | K4 | ❌ **离散编码，裸 rank 无意义** |
| 13 | `oth106_ospi_ca_eq_ksic_cls` | VECTOR | 0.4032 | 11 | 14 | K4 | ❌ 6 位分类码，离散 |
| 14 | `oth106_ospi_ca_eq_slc_ciik` | VECTOR | 0.4032 | 11 | 11 | K4 | ❌ KRX 行业码，离散 |
| 15 | `oth106_ospi_ca_eq_index_code2` | VECTOR | 0.404 | 9 | 9 | K4 | ❌ 离散编码 |

## 四、0.1 字段质量先验（头部 = 最强经济轴）

`index_share_nxt`(55) > `newshares_following_rightsissue`(41) > `adjusting_factor_nxt`(30) > `price_cls`(27) > `index_share_cls`(23) > …

⇒ **头部轴 = 指数权重（INDEX SHARE）**。与 0.2 分类一致，**无方向偏误**。

## 五、A-1 五问 + A-2 收益来源声明

| 问 | 答案 |
|---|---|
| **1 时间维度** | **事件前后快照差分**（`_nxt − _cls`）⇒ 信息量在「变更」本身，不在任一水平 |
| **2 相对性** | 排序差异 ⇒ `rank`/`group_rank` |
| **3 被定价的是谁** | **广度**（权重变化方向）——被再平衡的成分股 |
| **4 有无博弈** | 拥挤博弈存在（指数再平衡被抢跑）⇒ 这是**短期价格压力**，修复期短 |
| **5 事件性** | **强事件**（再平衡日）⇒ 必须控换手 |

**A-2 收益来源声明**：

- **谁在被定价**：指数再平衡中的**流动性提供方 / 抢跑交易者**
- **为什么会被错**：**制度性需求冲击**（被动基金必须按公告权重买卖）⇒ 临时价格压力在公告后数日内反转
- **错了多久修复**：**数日至 2 周**（再平衡效应的经典时窗）
- **预期方向**：**权重被上调 ⇒ 公告后先涨后跌（压力）**；方向句明确，可测

### ⚠ 结构性风险（三条，必须写进任何结论）

1. **有效截面只有 40%**：`cov 0.404` ⇒ TOP600 中仅约 40%（KOSPI200 成分股）有值，60% 为 NaN。
   ⇒ 任何形态都必须 backfill，否则被迫在 40% 截面上做等权多空，longCount/shortCount 严重失衡。
2. **`macro63` 的教训在此重复适用**：`other106` 与 `macro63` 同为「指数成分数据集」，
   而 `macro63` 已实测**横截面零方差**（KOSPI 内无 WTIDJH 成分股）。⇒ **组装前必须先验方差**，
   不能只看 cov。本数据集有真实成分股（KOSPI200 在 TOP600 内约 40%），故风险低于 macro63，但**仍需首测确认非零方差**。
3. **K4 四个分类编码字段不可直接用**：离散编码做 `rank` 无经济含义（等同于按代码大小排序）。

## 六、预处理决策（②.b 查表）

| 读数 | 决策 |
|---|---|
| 全字段 VECTOR | ⇒ 必须 `vec_avg` / `vec_max` 降维（**计数/权重类用 `vec_avg`；`vec_max` 对快照类更合适**） |
| cov 0.404 | ⇒ **`ts_backfill(F, 66)` 必做**（< 0.4 阈值边缘，60% 缺失会毁掉多空平衡） |
| 事件前后快照 | ⇒ **核心信号 = `subtract(vec_avg(_nxt), vec_avg(_cls))`**（同源同一数据集、单一经济含义「权重变更量」⇒ 合规） |
| 强事件型 | ⇒ `ts_target_tvr_decay(·, target_tvr=0.22)` 控换手 |
| K4 离散编码 | ⇒ 排除 |

## 七、待测清单

| 组 | 候选骨架 | 机制 |
|---|---|---|
| **G-权重变更** | `ts_target_tvr_decay(signed_power(group_rank(winsorize(rank(ts_backfill(subtract(vec_avg(index_share_nxt), vec_avg(index_share_cls)),66)), std=0.24), sector), 3.5), target_tvr=0.22)` | 再平衡压力（权重上调→短期承压） |
| **G-权重水平** | 同上换 `vec_avg(index_share_nxt)` 单侧 | 指数权重水平（拥挤度代理） |
| **G-自由流通变更** | `free_float_factor_nxt − _cls` | 流通盘调整 |

## 八、结论

- 头部轴清晰（指数权重），机制明确（制度性需求冲击 ⇒ 数日反转），**可组装**。
- 但**三重结构性风险**（40% 有效截面 / 快照非时序 / 与 macro63 同类的成分数据方差风险）⇒ 预期强度不高。
- **首测必须先确认方差非零**（`macro63` 前车之鉴），再判死活。
## 九、实测记录（2026-07-19 回填）

| alpha | 核心结构 | S | F | TO | 2Y | long/short |
|---|---|---:|---:|---:|---:|---|
| `9qEwEo9V` | `subtract(vec_avg(index_share_nxt), vec_avg(index_share_cls))` 权重变更量 | **−0.16** | −0.05 | 0.0433 | −0.57 | **136 / 463** |

**结论修正**：
1. **判死**。翻转符号约 +0.16，距闸线 1.58 差 1.42。
2. **§五 风险 1 被实测证实**：`cov 0.404` 导致 60% 股票无值，backfill 后 longCount 136 / shortCount 463，
   **多空比例 1:3.4 严重失衡** ⇒ 横截面排序在有效子集上退化为准等权 ⇒ S 贡献极低。
   **⚠ 这条是「覆盖率陷阱」的第二个实例（第一个是 macro63 的零方差）**：
   覆盖率 0.4 左右的成分股/指数类数据集，在 TOP600 全域上做横截面排序天然失衡，
   **首测就要看 longCount/shortCount 比值，比 S 更快发现问题**。
3. **§五 风险 3 未触发**：方差非零（alpha 有实际持仓与 pnl），故与 `macro63` 的恒等信号不同类。
4. **平台分类纠正**：本数据集 `category = macro`（塔 ×1.4），此前误记为 `other`。
