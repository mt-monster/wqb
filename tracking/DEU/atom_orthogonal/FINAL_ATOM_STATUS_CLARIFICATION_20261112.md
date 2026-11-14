# ★最终盘点：本轮新挖件无一为 ATOM（重要澄清）

日期：2026-11-12

## 一、ATOM 判定口径的澄清（我此前理解有偏差）

**ATOM = 单数据集 + 单塔。** 关键是「塔」这一维：

| 构造 | 塔数 | ATOM？ |
|---|---:|---|
| 纯 insd1_* 字段（无 cap 桶、无他类字段）| 1 | ✅ |
| 纯 significant_value_* 字段 | 1 | ✅ |
| **+ `bucket(rank(cap))`** | **2（PV 也计入）** | ❌ **失去 ATOM** |
| **+ predictive_starmine 的 analyst 腿** | 2（MODEL 计入）| ❌ |
| **+ oth455_* 腿** | 2（OTHER 计入）| ❌ |

**我此前以为 `cap` 桶只是「顺带点了 PV 塔、白赚倍率」，实际上它直接让 alpha 失去 ATOM 标签。**
这个认知偏差影响很大——`cap` 桶我几乎每波都在用。

## 二、本轮新挖件的 ATOM 状态核实

| alpha | S | 塔 | 有 cap 桶？| ATOM？ |
|---|---:|---|---|---|
| WjlMlWJd | 2.21 | PV+INSIDERS+ANALYST | ✅ 有 | ❌ |
| npa9PKWw | 1.74 | INSIDERS+OTHER | ❌ 无 | ❌（OTHER 计塔）|
| d5apW38x | 2.36 | INSIDERS+MODEL | ❌ 无 | ❌（MODEL 计塔）|
| leadEXnl | 2.20 | INSIDERS+MODEL | ❌ 无 | ❌ |
| 0mPqGEgq | 1.74 | INSIDERS+MODEL | ❌ 无 | ❌ |
| mLapKbd2 | 1.64 | INSIDERS+OTHER | ❌ 无 | ❌ |
| MP6OgoPr | 1.81 | INSIDERS+MODEL | ❌ 无 | ❌ |

⇒ **本轮新挖的 18 颗里，ATOM 数 = 0。**

### 18 颗里的 ATOM 件是存量

篮子中确实是单塔（ATOM）的 5 颗：

| alpha | 塔 | S | 来源 |
|---|---|---:|---|
| 78Yk8VR1 | SHORTINTEREST | 1.68 | **存量（本战役前已提交）** |
| d5a2vxzY | SHORTINTEREST | 1.60 | **存量** |
| GrW9OxmG | ANALYST | 1.62 | **存量** |
| zq3eb7No | ANALYST | 2.01 | **存量** |
| RREPm361 | ANALYST | 2.02 | **存量** |

⇒ 这 5 颗是真正的 ATOM，但都不是本轮新挖的（用户 11-08 曾明确「只算本战役新挖」）。

## 三、这意味着什么

**「优先 ATOM」这个目标，本轮新挖件交付数为 0。**

原因链：
1. insiders 单数据集上限 1.33（11 条路线验证）< 1.58 ⇒ 纯 ATOM 过不了闸
2. 要达到 1.58+，必须加第二个数据集的腿 ⇒ 塔数变 2 ⇒ 不是 ATOM
3. 加 `cap` 桶同理（PV 计塔）

⇒ **在 DEU insiders 上，ATOM 与 S≥1.58 互斥**，这是本文档的核心结论。

## 四、若一定要 ATOM，唯一出路是换数据集

| 数据集 | 单集最好像素 | 说明 |
|---|---|---|
| insiders1 | 1.33 | 已 11 条路线穷尽 |
| insider_agg_matrix | 0.93 | 已穷尽 |
| analyst7 | 0.80 | 已测 10 臂 |
| **其他未试** | ? | news104 / shortinterest3 / institutions6 / sentiment27 / risk60 / other455 等 |

但注意：这些数据集单腿历史读数多在 0.4-1.4，且很多已被判死（见判死清单）。

## 五、结论

| 目标维度 | 达成情况 |
|---|---|
| 20 个 regular alpha | **18 颗**（平台口径全过闸）|
| 优先 ATOM | **0 颗新挖**（5 颗 ATOM 均为存量）|
| 闸5 组合形态 | 18 颗中 13 颗违反（用户已知情）|

⇒ 三者不可兼得，需用户明确取舍。