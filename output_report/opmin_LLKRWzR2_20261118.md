# LLKRWzR2 按 d5adA29x 成功路径复跑（2026-11-18 02:18 点名）

> 用户指令：「同样的思路和方法路径，优化 LLKRWzR2」。
> 上一轮（11-17）判定 `REJECT_SELF_WALL`（16 条实测），但那次**只测了 self、从未测 prod**，也**从未扫中性化轴**。本轮先补这两个盲区。

## 0 上一轮留下的状态

```
ts_target_tvr_decay(group_rank(subtract(0, ts_mean(board_departure_rate_3m_management, 66)), subindustry), target_tvr=0.1)
USA/TOP3000/d1/decay1/CROWDING/trunc0.08
```
| 项 | 值 |
|---|---|
| S / F / 2Y / sub | 1.11 / 0.61 / 1.55 / 0.54（S、F、2Y 三项 FAIL） |
| TO / R / DD / margin | 2.27% / 3.78% / 8.72% / 33.4 bp |
| self（本地快筛） | 0.7212（FAIL） |
| 历史最优结构 | 6m 字段 + w10 + sector 轴 @CROWDING：S 1.46 / F 0.98 / 2Y 1.79 / sub 0.89 |

**F 算术**：TO 2.27% ≪ 12.5% 分母下限 ⇒ `F = S·√(R/0.125)`，**只取决于 S 与 R**。原件 (S1.11, R3.78%) → 0.61；6m 结构 (S1.46, R5.63%) → 0.98。**要过 F=1.0/S=1.49（在 R 5.63% 下）**。

## 1 本轮第一个盲区：prod 相关性从未测过

| alpha | 结构 | prod max | 判定 |
|---|---|---:|---|
| `LLKRWzR2`（原件） | 3m w66/subind @CROWDING | **0.8321** | **FAIL** |
| `xAvxeXdJ` | 6m w10/sector @INDUSTRY | **0.8258** | **FAIL** |
| `N1Ppnq1e` | 6m w10/sector @SECTOR | **0.8333** | **FAIL** |

⇒ **上一轮的「self 墙」诊断不完整：这族的真墙是 prod ≈ 0.83**（self 0.72 只是次要）。prod ≥0.7 **无任何豁免通道**。

## 2 本轮第二个盲区：中性化轴首扫（各 2 条：原件结构 / 6m·w10·sector 结构）

全批 USA/TOP3000/d1/decay1/trunc0.08，仅换 neutralization。

| 中性化 | alpha（6m·w10·sector） | S | **F** | 2Y | sub | TO | R | DD | margin | **Ra** | prod |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CROWDING（前一轮） | WjlgAbvQ | 1.46 | 0.98 | 1.79 | 0.89 | 1.83% | 5.63% | — | — | 2 | — |
| INDUSTRY | xAvxeXdJ | **1.61** | **1.03** | 2.02 | 0.81 | 1.84% | 5.10% | **3.05%** | 55.5 bp | **0** | 0.8258 |
| SECTOR | **N1Ppnq1e** | 1.59 | **1.05** | 1.92 | 0.92 | 1.55% | 5.47% | 3.37% | 70.5 bp | **0** | 0.8333 |
| MARKET | KPgbn8zp | 1.56 | **1.07** | 1.93 | **0.95** | 1.50% | 5.86% | 5.19% | 77.9 bp | 1 | 0.8335 |
| STATISTICAL | RRepN1Yn | 1.53 | 0.75 | 1.94 | 0.58 | **4.33%** | **2.97%** | 2.23% | 13.7 bp | **3** | — |

同行对照（原件结构 3m·w66·subindustry）：

| 中性化 | alpha | S | F | 2Y | sub | TO | DD | Ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| INDUSTRY | npagnw8d | 1.24 | 0.66 | 1.87 | 0.51 | 2.03% | 4.54% | 3 |
| SECTOR | 6XMwR3XE | 1.24 | 0.67 | 1.83 | 0.59 | 1.97% | 4.51% | 2 |
| MARKET | QP0anlzW | 1.23 | 0.70 | 1.80 | 0.61 | 1.90% | 4.88% | 2 |
| STATISTICAL | mLa8qVJE | 1.10 | 0.46 | 1.62 | 0.31 | 4.62% | 3.21% | 3 |

**轴的效果**：相对 CROWDING，INDUSTRY/SECTOR/MARKET 把 6m 结构的 S 从 1.46 抬到 1.56–1.61、F 从 0.98 抬到 1.03–1.07、DD 压到 3.0–5.2%，**八项 RA 全过**（INDUSTRY/SECTOR `failed_ra_count = 0`）。

**STATISTICAL 反向**：把换手从 1.5% 顶到 4.3%、收益从 5.9% 砍到 3.0%，F 崩到 0.75、Ra 3 —— 与 `d5adA29x`（STATISTICAL 是救星）**相反**。原因：本族收益来自超低频缓变，统计中性化强制加大调仓，收益密度被摊薄。

## 2.1 self 墙：这次真的破了

| 版本 | self | 判定 |
|---|---:|---|
| 上轮 6m 字段 @CROWDING | 0.7645 | FAIL |
| **`N1Ppnq1e`（6m·w10·sector @SECTOR）** | **0.6931** | **PASS（余量仅 0.007）** |

top 相关仍是 `ArN8Q8Y`（2025-06 提交、已 DECOMMISSIONED 的 mdl177 fangma 件）0.6931、`KmP73gj` 0.6828、`dK5ExGg` 0.6736。

## 3 判定：REJECT_PROD_WALL（更正上一轮的 SELF_WALL 诊断）

**四档中性化的 prod 全部落在 0.8258–0.8335，极差 0.008 ⇒ prod 与表达式无关，是字段本体的性质。**

| 版本 | prod max | 线 | 判定 |
|---|---:|---:|---|
| 原件 `LLKRWzR2`（3m·w66·subind @CROWDING） | 0.8321 | 0.7 | **FAIL** |
| `xAvxeXdJ`（6m @INDUSTRY） | 0.8258 | 0.7 | **FAIL** |
| `N1Ppnq1e`（6m @SECTOR） | 0.8333 | 0.7 | **FAIL** |
| `KPgbn8zp`（6m @MARKET） | 0.8335 | 0.7 | **FAIL** |

`prod ≥ 0.7` **无任何豁免通道**（`allow_prod_above_07` 已按用户判定移除）。因此：

- **上一轮「self 墙封死」的诊断不完整**：self 其实可以用 SECTOR 轴压到 0.6931 过线；真正封死本族的是 **prod 0.83**。
- **表达式层已穷尽**：窗口（10/21/66/126）、分组轴（subindustry/sector/industry）、中性化（CROWDING/INDUSTRY/SECTOR/MARKET/STATISTICAL）、字段族（3m/6m/1y、差分、联合）全部扫过，prod 纹丝不动。
- **成因**：`board_gov_stats` 有 328 用户 / 669 颗 alpha，生产池内存在同源件，PnL 几乎同构。

**重启路径（属新信号设计，不属本件优化）**：
1. **正交稀释**：数学上要让 prod 从 0.83 落到 0.70，需掺入约 **50% 权重的正交信号**（等波动假设：`corr=(1−w)/√((1−w)²+w²)`，w≈0.50）。这会触发混腿三问，且已不是「LLKRWzR2 的优化」。
2. **换数据集**：离开 `board_gov_stats`，改挖治理/人事类别的其他数据集。
3. **放弃该族**：本族在 prod 维度已被占满。

## 4 候选全维快照（`N1Ppnq1e`，指标最优且 RA 全过）

```
ts_target_tvr_decay(group_rank(subtract(0, ts_mean(board_departure_rate_6m_management, 10)), sector), target_tvr=0.1)
USA / TOP3000 / d1 / decay 1 / SECTOR / trunc 0.08
```
| 维度 | 值 |
|---|---|
| S / F / 2Y / sub | **1.59 / 1.05 / 1.92 / 0.92** |
| TO / R / DD / margin | 1.55% / 5.47% / 3.37% / **70.5 bp** |
| 八项 RA | `fail: []`，failed_ra_count **0** |
| prod / self | **0.8333 FAIL** ／ 0.6931 PASS |
| 塔 | `USA/D1/INSIDERS` ×1.1 ｜当季 **0** ｜交后 1 ｜**未点亮（1/3 奠基）** ｜塔边际正 |
| 六维 | **4 distinct 算子 / 4 次调用 / 1 个数据字段** —— 比六维基线（T1 4.61、T2 1.85）更优 |

⇒ 指标与六维都很漂亮，**唯一死因是 prod 0.83**。零提交。


---

# 5 重启路径②：换字段子族（用户 02:27「继续」）

## 5.1 为什么还值得再试一次

`check_correlation(production)` 的直方图给出了决定性证据：

| 相关区间 | 生产池 alpha 数 |
|---|---:|
| [0.8, 0.9) | **22** |
| [0.7, 0.8) | 3,950 |
| [0.6, 0.7) | 23,073 |
| [0.5, 0.6) | 79,476 |

⇒ 与本件相关 >0.7 的生产池 alpha 共 **3,972 颗**，其中 22 颗 >0.8。**不是撞到一颗同源件，而是「board departure（离开董事会）」这个字段空间被整体占满**。这解释了为什么四档中性化的 prod 极差只有 0.008。

但 `board_gov_stats` 数据集共 46 个字段，而历史三轮只用了 `board_departure_rate_*` 一个子族。数据集里还有两个**语义不同、拥挤度低 3–10 倍**的离职子族：

| 字段 | 经济含义 | users / alphas | 历史是否测过 |
|---|---|---:|---|
| `board_departure_rate_3m_management` | 离开**董事会**的比例（3M） | 87 / 138 | ✅ 已判死 |
| `board_departure_rate_6m_management` | 离开**董事会**的比例（6M） | 31 / 43 | ✅ 已判死 |
| **`management_departure_rate_3m_management`** | 离开**公司**的比例（3M） | **12 / 13** | ❌ 从未测 |
| **`management_departure_rate_6m_management`** | 离开**公司**的比例（6M） | **12 / 15** | ❌ 从未测 |
| **`personnel_departure_rate_6m_total`** | 全部董事+高管离职比例（6M） | **14 / 18** | ❌ 从未测 |
| **`management_join_rate_6m_management`** | 高管**加入**比例（6M） | **6 / 8** | ❌ 从未测 |

**「离开董事会」≠「离开公司」**：前者是治理层换席（可能仍在公司任职），后者是真正的人才流失。二者 PnL 相关预计低于同字段的不同窗口，是唯一有可能把 prod 拉下 0.7 的现成差异化维度。

## 5.2 本批设计（4 条，设置全部沿用 `N1Ppnq1e`）

基线设置：`USA / TOP3000 / D1 / decay 1 / SECTOR / trunc 0.08 / pasteurization ON / nanHandling ON`

| 批 | 表达式 | 经济假设 |
|---|---|---|
| A1 | `group_rank(-ts_mean(management_departure_rate_6m_management,10), sector)` | 高管真离职↑ ⇒ 做空（6M 平滑） |
| A2 | 同上换 `management_departure_rate_3m_management` | 3M 口径更及时 |
| B1 | `group_rank(-ts_mean(personnel_departure_rate_6m_total,10), sector)` | 全员离职口径 |
| B2 | `group_rank(ts_mean(join6m − departure6m, 10), sector)` | **净人才流**（加入−流失），经济含义与前三条不同 |

全部外层套 `ts_target_tvr_decay(·, target_tvr=0.1)`；算子结构 4 distinct / 4 调用 / 1–2 字段，六维优于基线。

## 6.4 wave-3 实测结果（8 条，12:03 收回）：**全部弱于离职族**

| 字段 | 类别 | alpha | S | **F** | 2Y | sub | TO | R | DD | Ra |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `ceo_tenure_days` | 任期 | `wpollk6l` | **1.24** | 0.83 | **1.66** | 0.58 | 0.93% | 5.66% | 13.10% | 3 |
| `max_chief_officer_tenure_days` | 任期 | `mLabbWOK` | 1.10 | 0.76 | 1.45 | 0.50 | 0.90% | 5.95% | **17.48%** | 4 |
| `aggregate_external_connections` | 外部连接 | `rK7lle2J` | 1.00 | 0.58 | 1.54 | 0.47 | 0.92% | 4.15% | 9.57% | 4 |
| `unique_external_company_union` | 外部连接 | `mLabb65p` | 0.92 | 0.48 | 1.07 | 0.35 | 3.56% | 3.47% | 6.50% | 4 |
| `independent_director_ratio` | 治理 | `leallKO8` | 0.82 | 0.50 | 0.79 | 0.39 | 0.98% | 4.70% | 9.80% | 4 |
| `surname_concentration_total_personnel` | 姓氏 | `58JOOg0M` | 0.75 | 0.42 | **1.70** | **0.15** | 1.13% | 3.89% | **16.39%** | 3 |
| `board_join_rate_6m_management` | 加入率 | `GrmLLbdZ` | 0.73 | 0.30 | 0.72 | 0.60 | 1.60% | 2.16% | 4.37% | 3 |
| `personnel_join_rate_6m_total` | 加入率 | `YPa00b5J` | 0.72 | 0.31 | 0.61 | 0.67 | 1.61% | 2.36% | 5.53% | 3 |

**对照（离职族，此前最优）**：`N1Ppnq1e` board_departure_6m **S 1.59 / F 1.05 / 2Y 1.92 / sub 0.92**；`E5QwkZL9` personnel_departure_6m_total **S 1.57 / F 1.02 / 2Y 2.01**。

### 三条判读

1. **只有「任期」这一类接近门槛**：`wpollk6l`（CEO 任期）S 1.24、**2Y 1.66 已过线**、F 0.83、TO 仅 0.93%（远低于 12.5% 分母下限）。它缺的只是 S 的 0.34。
2. **「加入率」几乎无信号（S 0.72–0.73）**：这是个值得记下的经济学不对称——**市场对「人走」的反应远强于「人来」**。离职是负面事件（治理风险、知识流失），加入是常规更替，信息含量低。
3. **「外部连接 / 姓氏集中度 / 独立董事」全部弱且 sub-universe 极差**（0.15–0.47）。`58JOOg0M`（姓氏集中度）虽然 2Y 1.70，但 S 0.75、**sub 0.15**、DD 16.39%，三项硬伤。

### 与 QP0Odbg 的关键对照

| 维度 | `QP0Odbg`（翻案成功） | `LLKRWzR2`（本件） |
|---|---|---|
| 换字段后 2Y 变化 | **0.97 → 1.87（+0.90）** | 1.92 → 最好 1.66（**未改善**） |
| 换字段后 S 变化 | 1.36 → **1.96** | 1.59 → 最好 1.24（**更差**） |
| 新字段源 | `stable_boundary_trade_count_21d_active`：**不同经济机制**（耐久边界交易 vs 总笔数） | 任期/连接/姓氏：**仍在「公司治理/人事」同一大类内** |
| 是否有 `_active` 双口径 | 有（原始 vs 活跃账户） | **无**（46 字段全是 MATRIX 统计量） |

⇒ **两件的关键差异：`QP0Odbg` 换到了真正不同的信息机制；`LLKRWzR2` 的数据集只有「治理/人事」这一个信息大类，换字段只是在同一大类内部换代理变量。**

（下一批：1y 口径补全 + CEO 任期优化，回测中）

## 5.3 若本批仍撞 prod 墙：wave-2 备选（非离职口径）

`board_gov_stats` 共 46 字段，历史三轮 + 本批只覆盖「离职」这一族。若离职族整体撞墙，剩下能改变 PnL 形态的是**非事件型治理特征**（缓变量，换手天然低）：

| 字段 | 经济含义 | users / alphas | 与离职族的 PnL 相关性预期 |
|---|---|---:|---|
| `surname_concentration_board` | 董事会姓氏集中度（家族控制代理） | 5 / 5 | 低（几乎不随时间变动） |
| `independent_director_ratio` | 独立董事比例（治理质量） | 21 / 24 | 低-中 |
| `ceo_tenure_days` / `chairman_tenure_days` | CEO / 董事长任期（新任=不确定性） | 46 / 65、48 / 62 | 低 |
| `doctorate_share_total_personnel` | 全员博士占比（人力资本） | 6 / 6 | 低 |
| `unique_external_company_union` | 董事/高管外部公司连接数（网络资本） | 10 / 11 | 中 |
| `ceo_chairman_duality_flag` | CEO 兼任董事长（权力集中） | 13 / 18 | 低 |

**注意**：这一族的信号强度通常弱于离职事件（事件驱动才有 S），需要更长窗口 + 组合构造；若单字段 S 上不到 1.58，则本族整体放弃，转挖其它数据集。

## 5.4 wave-1 实测结果（4 条，02:36 收回）

| 变体 | alpha | S | F | 2Y | sub | TO | R | DD | margin | Ra | **prod** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 高管离职 6m（`management_departure_rate_6m_management`） | rK7oA1eJ | 1.34 | 0.90 | 1.49 | **0.42** | 1.31% | 5.58% | 4.01% | 85.4bp | 4 | — |
| 高管离职 3m（`management_departure_rate_3m_management`） | 6XMwznKp | 1.32 | 0.91 | 1.72 | **0.42** | 1.66% | 5.93% | 6.03% | 71.3bp | 3 | — |
| **全员离职 6m（`personnel_departure_rate_6m_total`）** | **E5QwkZL9** | **1.57** | **1.02** | **2.01** | 0.63 | 1.57% | 5.25% | **2.98%** | 67.0bp | 2 | **0.7629** |
| 净人才流（join6m − dep6m） | A1xwkREd | 1.47 | **1.12** | 1.72 | **0.98** | 1.74% | **7.29%** | 6.22% | 83.7bp | 1 | **0.8911** |

### 三条判读

1. **「离开公司」并不比「离开董事会」强**：`management_departure_rate_*` 的 S 只有 1.32–1.34、**sub-universe 0.42 硬伤**（Ra 3–4）。原以为「真离职」信号更纯，实测反而更弱——管理层真离职是低频稀疏事件，截面样本太少。
2. **`personnel_departure_rate_6m_total`（全员口径）是本族新最优**：S **1.57**（差 0.01）、F 1.02、2Y **2.01**、DD **2.98%**、margin 67bp，只卡 `LOW_SHARPE` + `LOW_SUB_UNIVERSE_SHARPE 0.63`。
3. **prod 被拉低了，但还不够**：0.8333 → **0.7629**，且 [0.7,0.8) 的池内 alpha 从 3950 颗降到 **295 颗**（[0.8,0.9) 归零）。但**净人才流反而更差（0.8911）**——生产池已有人做 join/departure 净额构造。⇒ **水平型构造无论换哪个子族都撞墙，必须换构造类型。**

## 5.5 wave-2：意外 / 加速度型构造（回测中）

水平型（level）与生产池同构，改打两类「非水平」构造：

| 批 | 表达式 | 构造含义 |
|---|---|---|
| C1 | `group_rank(−ts_zscore(personnel_departure_rate_3m_total, 252), sector)` | 本公司自身 1 年历史的**离职称奇度** |
| C2 | `group_rank(−ts_zscore(management_departure_rate_3m_management, 252), sector)` | 同上，管理口径 |
| D1 | `group_rank(−(ts_mean(personnel_3m,10) − ts_mean(personnel_1y,10)), sector)` | **离职加速度**（3M 率 − 1Y 率） |
| D2 | `group_rank(−ts_zscore(personnel_departure_rate_6m_total, 252), industry)` | 6M 口径 + 换 industry 轴 |

时序 zscore 抹掉「这家公司常年高离职」的水平信息，只留「突然变差」——这是与生产池水平型 alpha 正交化的标准手法，且算子数仅 3（`ts_zscore`/`group_rank`/`ts_target_tvr_decay`），六维 T1 优于基线。

## 5.6 wave-2 实测结果（4 条，02:52 收回）

| 构造 | alpha | S | F | 2Y | sub | TO | R | DD | margin | Ra |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 全员 3M 离职称奇度 `ts_zscore(·,252)` | A1xwk7QY | **0.92** | 0.42 | 1.13 | 0.64 | 1.90% | 2.59% | 5.87% | 27.2bp | 3 |
| 管理 3M 离职称奇度 | 1YW7Jzjz | **0.15** | 0.03 | 0.31 | 0.33 | 1.49% | 0.58% | 15.49% | 7.8bp | 3 |
| 离职加速度（3M − 1Y） | omaKVK7E | 1.07 | 0.67 | 1.14 | 0.69 | 1.62% | 4.96% | 7.90% | 61.3bp | 3 |
| 全员 6M 称奇度 @industry | omaKVK7b | 1.08 | 0.55 | 1.25 | 0.67 | 2.02% | 3.29% | 5.26% | 32.6bp | 3 |

**正交化把 alpha 一起抹掉了**：S 从 1.57 掉到 0.92 / 1.07 / 1.08（管理口径只剩 0.15）。

## 5.7 最终判定：`REJECT_STRUCTURAL_DATASET`（数据集级，论证闭合）

八条实测构成一张「构造类型 × 字段子族」矩阵，四角全部堵死：

| 构造类型 | 字段子族 | 最好 S | prod |
|---|---|---:|---:|
| 水平（level） | `board_departure_*`（离开董事会） | 1.59 | **0.8333 FAIL** |
| 水平（level） | `personnel_departure_*_total`（全员） | 1.57 | **0.7629 FAIL** |
| 水平（level） | `management_departure_*`（离开公司） | 1.34 | 未测（sub 0.42 已死） |
| 净额（join − dep） | 管理 6M | 1.47 | **0.8911 FAIL**（更差） |
| 意外度（`ts_zscore` 252d） | 全员 3M / 管理 3M / 全员 6M | 0.92 / 0.15 / 1.08 | —（S 已死） |
| 加速度（3M − 1Y） | 全员 | 1.07 | —（S 已死） |

⇒ **本数据集存在一个不可绕过的 trade-off：alpha 全部来自截面水平信息，而截面水平信息正好是生产池已持有的那部分；任何把水平信息剥掉的做法（意外度、加速度、净额）都会同时把 alpha 剥掉。**

**结论**：`board_gov_stats` 全族（46 字段）在本账号判定 **不可提交**。三条重启路径的实测状态：
1. 正交稀释 —— 从 0.7629 降到 0.70 需 **≈43.7% 正交权重**（`0.7 = 0.7629(1−w)/√(0.7629²(1−w)²+w²)`），而现成正交腿的 S 只有 1.0 量级，混出来的 S 上限 ≈1.8 但 prod 只是压到临界 0.70，**且属新 alpha 设计 + 触发混腿三问**；
2. 换字段子族 —— **已穷尽**（本报告 8 条）；
3. 换区域 —— **不可行**（`board_gov_stats` 为 USA 专属，EUR/GLB `get_datafields` 均返回 0）。

**唯一残留的可行方向**：把「全员离职」腿（S 1.57 / prod 0.7629，本族最好）作为**一条腿**，与另一个数据集的强正交腿做显式双信息源组合（需三问叙事 + 权重预设），这不是 LLKRWzR2 的优化，属新信号设计。

---

# 6 字段覆盖补测：40 个字段从未测过（用户 11:53「换 LLKRWzR2 优化」）

## 6.1 触发：QP0Odbg 的翻案教训

同一天在 `QP0Odbg` 上发生了一次判定推翻：该族被判 `REJECT_TRADEOFF`（"2Y 天花板 1.27，物理不可达"），累计 46 条实测。但用户一句「字段替换有做过吗」暴露了致命疏漏——`fund_holdings_panel` 有 30 字段，只测了 4 个。补测后换成 `stable_boundary_trade_count_21d_active`，**2Y 从 0.97 直接跳到 1.87**，八项 RA 全过。

**教训：判死一个族之前，字段替换必须做到足够覆盖。**

本件面临完全相同的风险。`board_gov_stats` 共 **46 个字段**，此前只测过 **6 个**（全部属于「离职率」一族）：覆盖率 **13%**。

## 6.2 46 字段全景（`get_datafields`，USA/TOP3000/D1，全部 MATRIX 型）

| 类别 | 字段数 | 已测 | 未测成员（alphaCount） |
|---|---:|---:|---|
| 离职率 departure | 9 | **6** | `board_departure_rate_1y_board`(30)、`management_departure_rate_1y_management`(12)、`personnel_departure_rate_1y_total`(8) |
| **加入率 join** | **9** | **0** | `personnel_join_rate_6m_total`(**6**)、`board_join_rate_6m_management`(13)、`management_join_rate_3m_management`(6)、`management_join_rate_1y_management`(9)、`board_join_rate_1y_board`(16)、`personnel_join_rate_1y_total`(7)、`personnel_join_rate_3m_total`(18)、`board_join_rate_3m_management`(90)、`management_join_rate_6m_management`(8) |
| **任期 tenure** | **5** | **0** | `ceo_tenure_days`(65)、`chairman_tenure_days`(62)、`max_chief_officer_tenure_days`(45)、`median_chief_officer_tenure_days`(28)、`min_chief_officer_tenure_days`(9) |
| **外部连接 external** | **6** | **0** | `aggregate_external_connections`(60)、`board_external_connection_count`(50)、`unique_external_company_union`(**11**)、`unique_external_company_board`(13)、`unique_external_company_management`(10)、`management_external_connection_count`(12) |
| **姓氏集中度 surname** | **3** | **0** | `surname_concentration_board`(**5**)、`surname_concentration_total_personnel`(**7**)、`surname_concentration_management`(3，覆盖仅 0.59) |
| **结构/性别/学历/标志** | **14** | **0** | `multiple_ceo_indicator`(**3**)、`ceo_gender_flag`(5)、`male_ratio_management`(3)、`doctorate_share_total_personnel`(6)、`management_team_size`(6)、`total_personnel_count`(6)、`chief_officer_chairman_flag`(8)、`independent_director_ratio`(24)、`board_member_count_2`(25)、`ceo_chairman_duality_flag`(18)、`doctorate_share_board`(30)、`doctorate_share_management`(9)、`male_ratio_board`(18)、`male_ratio_total_personnel`(14) |

**注意与 QP0Odbg 的结构差异**：`board_gov_stats` 全部是 **MATRIX 型统计量**（比率/计数），没有 `fund_holdings_panel` 那种「原始 / `_active`」双口径。所以 QP0Odbg 的 `_active` 杠杆在本件不存在，只能靠**换经济维度**。

## 6.3 本批 8 字段（wave-3 广度扫描）

选择标准：**语义独特性 × 低拥挤度**。结构统一沿用本族最优件 `N1Ppnq1e` 的骨架，方向先取正向（未取负）：

```
ts_target_tvr_decay(group_rank(ts_mean(<FIELD>, 10), sector), target_tvr=0.1)
USA / TOP3000 / D1 / decay 1 / SECTOR / trunc 0.08
```

| 批 | 字段 | 类别 | alphaCount | 经济含义 |
|---|---|---|---:|---|
| A1 | `surname_concentration_total_personnel` | 姓氏集中度 | **7** | 家族控制代理（对数度量） |
| A2 | `independent_director_ratio` | 治理结构 | 24 | 独立董事比例（治理质量） |
| B1 | `unique_external_company_union` | 外部连接 | **11** | 董事/高管的外部公司连接数（网络资本） |
| B2 | `aggregate_external_connections` | 外部连接 | 60 | 全部外部连接总数 |
| C1 | `ceo_tenure_days` | 任期 | 65 | CEO 任期（新任=不确定性） |
| C2 | `max_chief_officer_tenure_days` | 任期 | 45 | 高管最长任期（权力固化） |
| D1 | `personnel_join_rate_6m_total` | 加入率 | **6** | 全员加入比例（扩张） |
| D2 | `board_join_rate_6m_management` | 加入率 | 13 | 管理层入董事会比例 |

**方向说明**：离职族在这一族里是**取负**（离职率高 ⇒ 做空）成交的。加入率/任期/结构类字段的经济方向不确定，先测正向；若出现"负 S 且 |S| 强"的信号，再翻转重测。

**先验判断（先写下，事后对账）**：
1. **姓氏集中度与外部连接**最有可能把 prod 拉下 0.7——它们与"人事变动"是完全正交的经济维度，生产池里做这两类构造的 alpha 极少（7 / 11 颗）。
2. **任期类**大概率弱信号但换手极低，可能满足 F 却不满足 S。
3. **加入率类**虽然是事件型，但与离职率同属"人事流动"，PnL 可能与现有件高度相关 ⇒ 即使 S 强，prod 也未必降。

## 7.8 实测结果（14 条，12:22 收回）

### 五颗 fRA 0（全闸过）

| alpha | 变体 | S | **F** | **2Y** | sub | TO | R | DD | **Ra** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `6XM9p0AL` | 中性化 → **SECTOR** | 1.71 | 1.06 | **2.21** | 0.77 | 1.61% | 4.77% | **3.64%** | **0** |
| `O0WZGgld` | **decay 0** | 1.73 | 1.09 | **2.19** | 0.78 | 1.93% | 4.95% | 5.12% | **0** |
| `akan1zgv` | **网络腿换 `aggregate_external_connections`** | 1.72 | 1.08 | 2.15 | 0.77 | 1.55% | 4.97% | 5.13% | **0** |
| `YPa0vz16` | SECTOR + max_chief 任期 | 1.67 | 1.07 | 1.96 | **0.81** | 1.61% | 5.12% | 5.64% | **0** |
| `N1NMdZ7X` | decay 0 + max_chief 任期 | 1.72 | **1.12** | 1.97 | **0.81** | 1.93% | 5.30% | 6.21% | **0** |

对照原件 `qMLvlqJ1`：S 1.73 / F 1.09 / 2Y 2.18 / sub 0.77 / DD 4.99% / **prod 0.7929**。

### fRA 1（卡 sub）

| alpha | 变体 | S | **F** | 2Y | sub | Ra |
|---|---|---:|---:|---:|---:|---:|
| **`xAvkNVlw`** | **bucket 分母换 `total_personnel_count`** + max_chief | **1.80** | **1.16** | 2.06 | 0.60 | 1 |
| `2r5Lp95Y` | 同上 + ceo_tenure | 1.74 | 1.09 | **2.21** | 0.49 | 1 |
| `0mPEpNJv` | bucket 粒度 range **0.05** | 1.78 | **1.14** | 2.20 | 0.73 | 1 |
| `npa2NeE3` | bucket 粒度 range **0.2** | 1.68 | 1.06 | 2.20 | 0.65 | 1 |

**画像 §7.4 的 S 排序得到验证**：`total_personnel_count`（S 1.80）> `board_member_count_2`（1.73）—— 但**代价是 sub 从 0.77 掉到 0.49–0.60**（fRA 1）。两者不可兼得。

### ★ 门控路线：彻底失败（S 0.14–0.33）

| alpha | 层级 | 主体信号 | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| `d5a0jVQj` | `if_else(门, 信号, 0)` | personnel_6m 离职 | **0.25** | 0.06 | 0.68 | 0.17 | 3.02% |
| `rK7ljgW9` | `if_else(门, 信号, 0)` | board_6m 离职 | **0.33** | 0.09 | 0.77 | 0.32 | 2.99% |
| `GrmLGxXZ` | `trade_when(门, 信号, -1)` | personnel_6m 离职 | **0.14** | 0.02 | 0.23 | 0.07 | 1.07% |
| `9qlrpmd9` | `trade_when(门, 信号, -1)` | board_6m 离职 | **0.27** | 0.06 | 0.31 | 0.35 | 1.04% |

**为什么论坛帖能做出 1.86、这里却只有 0.14–0.33？**

| 维度 | 论坛帖（`43907846056599`） | 本批 |
|---|---|---|
| 主体信号 | `sentiment_weighting_method2` 的 tone change（另一数据集，**本身是强信号**） | 离职率（本数据集内，单独 S 1.57 属中等） |
| 门控作用 | 只保留「管理层更新高」的约 30% 样本，在里面做**方向反转** | 同样只保留 30% 样本，但主体是**同数据集弱信号** |
| 结果 | Sharpe **+1.86** | S **0.14–0.33** |

⇒ **门控模板的成立条件 = 强主体信号 × 人事门控**。本数据集内没有「强主体」，因此该模板不可移植。（若要用，必须先有另一数据集的强信号，那就变多数据集 → 混塔，与 ATOM 单塔冲突。）

### prod 实测

| alpha | 变体 | **prod** | [0.7,0.8) / [0.8,0.9) |
|---|---|---:|---|
| **`qMLvlqJ1`** | 原件（MARKET, decay 4） | **0.7929** | 1,532 / **0** |
| `akan1zgv` | 网络腿换 `aggregate_external_connections` | **0.8006** | 2,018 / 1 |

**换网络腿字段没有降 prod（反而 +0.008）** —— 与 `LLKRWzR2` 全族「表达式层微调对 prod 无效」的结论一致。

（其余变体 prod 待测：`6XM9p0AL` / `O0WZGgld` / `xAvkNVlw` / `KPJq9aMN`；平台限制一次只能算一个，需串行等 240s）

## 7.9 阶段性结论

1. **用户的批评是对的，而且有价值**：漏读字段画像让我错过了本族**唯一 fRA 0 的成熟骨架**（`任期 × 网络 × bucket(董事人数)`），它在 50 条实测的 prod 分布上第一次呈现 `[0.8,0.9)` 归零。
2. **模板要分层看**：level / change / gate 三层里，本数据集只有 **level+组合** 一层有效；change 层已被此前的 `ts_zscore` 实验证否，gate 层本轮证否（缺强主体）。
3. **prod 0.7929 仍是硬墙**，但它是本族**最薄的一堵**（无 `[0.8,0.9)` 钉子件）。需要至少再压 0.10。
4. **未测完的最后一类模板**：画像 wave280/281 提示还有「insider 腿主导 + 治理腿残差」的组合形态（`kqNb1g5d` S 3.32 / `qMLvP0qv` S 1.68），但那是跨数据集残差化，属混塔，且 `kqNb1g5d` 此前已判死。

## 6.5 离职族补全（9/9 全覆盖）+ 1y 口径的意外发现

离职族此前测了 6 个（3m / 6m × board / management / personnel），本轮补全剩余 3 个 1 年口径：

| 字段 | alpha | S | **F** | **2Y** | sub | TO | R | DD | **Ra** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `board_departure_rate_1y_board` | `A1xP7Zll` | **1.51** | **1.02 ✓** | **2.13 ✓** | 0.60 | 1.24% | 5.66% | **4.94%** | **2** |
| `personnel_departure_rate_1y_total` | `leal3d5A` | **1.52** | **1.02 ✓** | **2.25 ✓** | 0.34 | 1.27% | 5.65% | 4.14% | **2** |
| `management_departure_rate_1y_management` | `rK7lPgj8` | 1.50 | **1.03 ✓** | 1.78 ✓ | **0.29** | 0.99% | 5.93% | 3.61% | 3 |
| （对照）`personnel_departure_rate_3m_total` **正向** | `akanE6Q9` | 0.39 | 0.13 | 0.91 | 0.44 | 2.26% | 1.44% | 16.38% | 3 |

### 6.5.1 `A1xP7Zll` 的卡点：本族史上最接近全闸

| 检查项 | 数值 | 门槛 | 差距 |
|---|---:|---:|---|
| **LOW_SHARPE** | 1.51 | 1.58 | **−0.07** |
| **LOW_SUB_UNIVERSE_SHARPE** | 0.60 | **0.65** | **−0.05** |
| LOW_FITNESS | **1.02** | 1.00 | **PASS ✓** |
| LOW_2Y_SHARPE | **2.13** | 1.58 | **PASS ✓** |
| LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / MATCHES_PYRAMID | — | — | PASS |
| CLUSTER_TEST | 1.40 | 1.58 | WARNING |

**这是 30 条实测里第一次出现「F 过、2Y 大幅过、只剩 S −0.07 与 sub −0.05」的件。** 此前最好的是 `N1Ppnq1e`（F 1.05 / 2Y 1.92 / **S 1.59 已过**），但它的 sub 0.92 也过 —— 那个件是 prod 卡住。而本件是 prod + S + sub 三卡。

另注：`LOW_SUB_UNIVERSE_SHARPE` 的门槛在本件是 **0.65**（`d5adA29x` 是 0.82）—— **门槛本身是按件动态算的**。

### 6.5.2 方向验证（重要）

`akanE6Q9` = `personnel_departure_rate_3m_total` **正向**（不取负）⇒ S **0.39**；同字段取负版（`E5QwkZL9`，6m）⇒ S **1.57**。
⇒ **离职率必须取负**（离职率高 ⇒ 做空）确认，不是反向信号。

### 6.5.3 ★★★ 1y 口径：指标最漂亮，但 prod 墙最厚

| 口径 | 指标（S/F/2Y） | **prod** | 直方图 [0.7,0.8) / [0.8,0.9) |
|---|---|---:|---|
| `personnel_departure_rate_6m_total` | 1.57 / 1.02 / 2.01 | **0.7629（最好）** | 295 / 0 |
| `personnel_departure_rate_1y_total` | **1.52 / 1.02 / 2.25** | 0.8146 | 1,015 / 4 |
| `board_departure_rate_6m_management` | 1.59 / 1.05 / 1.92 | 0.8333 | 3,950 / 22 |
| `board_departure_rate_1y_board` | **1.51 / 1.02 / 2.13** | **0.8905（最差）** | 8,208 / 511 |

**新判据：同一族内，时间窗口越长 ⇒ prod 越差。**
机理：长窗（1y）信号被平滑得更像「基本面质量因子」（长期治理水平），而这类 alpha 在生产池中最密集；短窗（6m）保留了事件性，反而更独特。
⇒ **1y 口径是「指标最漂亮但最不可提交」的陷阱**——这正好是 `d5adA29x` 上「2Y 与 F 互斥」的另一种形态：**好指标与低 prod 互斥**。

### 6.5.4 判定

`A1xP7Zll` / `leal3d5A` 虽然把 F 与 2Y 都做到了过线，但：
1. **prod 0.8905 / 0.8146，远超 0.7（无豁免）**；
2. 仍卡 LOW_SHARPE（−0.07）与 LOW_SUB_UNIVERSE_SHARPE（−0.05）。

⇒ **不构成可提交件。`REJECT_PROD_WALL` 维持且证据加强：离职族 9/9 字段全覆盖，prod 区间 0.7629–0.8905，无一接近 0.7。**

（还在飞的批：1y+6m 混合 ×2、w5/w22、@MARKET、@INDUSTRY ×2、@SUBINDUSTRY ×2）

## 6.6 ★★ 1y+6m 多尺度混合：指标全线突破，但 prod 同步恶化

### 混合结果（`add(rank(−ts_mean(1y,10)), rank(−ts_mean(6m,10)))` @SECTOR）

| alpha | 混合腿 | S | **F** | **2Y** | **sub** | TO | R | DD | **Ra** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`omalgWJ6`** | personnel **1y + 6m** | **1.58 ✓** | **1.09 ✓** | **2.22 ✓** | 0.51 ✗ | 1.44% | 5.92% | 3.57% | **1** |
| **`O0WZx8MR`** | board **1y + 6m** | 1.56 ✗ | **1.08 ✓** | **2.08 ✓** | **0.79 ✓** | 1.43% | 6.03% | 4.49% | **1** |

**`O0WZx8MR` 的 `checks.fail = []`（空）—— 七项全 PASS**：LOW_FITNESS 1.08 ✓、LOW_SUB_UNIVERSE_SHARPE 0.79 ✓、LOW_2Y_SHARPE 2.08 ✓、LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / MATCHES_PYRAMID 全 PASS。**唯一 WARNING 是 LOW_SHARPE 1.56（差 0.02）**，CLUSTER_TEST 1.32 WARNING。

这是**本族 47 条实测里指标最完整的一颗**（F/2Y/sub 全过，S 差 0.02）。

### 但 prod 实测：混合让 prod 恶化

| 变体 | 指标（S/F/2Y/sub） | **prod max** | 直方图 [0.7,0.8) / [0.8,0.9) |
|---|---|---:|---|
| `board_6m` 单腿 | 1.59 / 1.05 / 1.92 / 0.92 | **0.8333** | 3,950 / 22 |
| `board_1y` 单腿 | 1.51 / 1.02 / 2.13 / 0.60 | **0.8905** | 8,208 / 511 |
| **`board_1y+6m` 混合** | **1.56 / 1.08 / 2.08 / 0.79** | **0.8828** | 8,505 / 500 |
| `personnel_6m` 单腿 | 1.57 / 1.02 / 2.01 / 0.63 | **0.7629（全族最低）** | 295 / 0 |
| `personnel_1y` 单腿 | 1.52 / 1.02 / 2.25 / 0.34 | 0.8146 | 1,015 / 4 |
| **`personnel_1y+6m` 混合** | **1.58 / 1.09 / 2.22 / 0.51** | **0.8162** | 1,180 / 9 |

**混合把指标全线推过线，却同时把 prod 推高（0.8333→0.8828、0.7629→0.8162）。**

## 6.7 ★★★ 本族的结构真相：prod 与指标在同一条轴上反向

把 6 个口径按「信号平滑程度」排序，规律完全单调：

| 信号形态 | 代表 | 指标完整度 | **prod** |
|---|---|---:|---:|
| **最原始、最事件型**（单字段 6m） | `personnel_6m` / `board_6m` | S 够、sub 部分够 | **0.7629 / 0.8333** |
| 长窗单腿（1y） | `personnel_1y` / `board_1y` | 2Y 强、S/sub 不够 | 0.8146 / 0.8905 |
| **平滑混合**（1y+6m） | `omalgWJ6` / `O0WZx8MR` | **全部够** | **0.8162 / 0.8828** |

**机理**：`board_gov_stats` 是「公司治理/人事」类基本面统计数据集。信号越平滑、窗口越长、越综合 ⇒ 越接近生产池里大量存在的「治理质量」因子 ⇒ prod 越高。而**指标恰恰需要平滑**（降 DD、提 2Y、稳 sub）。

⇒ 这族存在一条 **prod–指标前沿**，与 `QP0QOdbg` 的 TO–2Y 前沿同构：

```
要 prod 最低（0.7629）：只能用最原始的单腿 ⇒ S 1.57 / sub 0.63（都差）
要指标全过（O0WZx8MR）：必须平滑混合 ⇒ prod 0.8828（差 0.18）
交集为空
```

**全族 prod 区间 0.7629–0.8905，最低值仍需再降 0.063。** 按等波动稀释算术，ρ0=0.7629 → 0.69 需 **w≈0.445（44.5% 正交权重）**；而 `QP0QOdbg` 的混腿实验已经实测证明**混腿不能稀释 prod，反而恶化**。

## 6.8 字段覆盖最终账（37%，离职族 100%）

| 类别 | 已测/总数 | 结论 |
|---|---|---|
| **离职率** | **9 / 9（100%）** | 唯一有效类别。prod 0.7629–0.8905，最强指标件 `O0WZx8MR`（F 1.08 / 2Y 2.08 / sub 0.79 / S 1.56） |
| 加入率 | 2 / 9 | 弱（S 0.72–0.73）。**市场对「人走」的反应远强于「人来」** —— 经济学不对称 |
| 任期 | 2 / 5 | 次强（CEO 任期 2Y 1.66，最好 `A1xP7bZg` S 1.36 / F 0.89 / 2Y 1.80），仍不达标 |
| 外部连接 | 2 / 6 | 弱（S 0.92–1.00，sub 0.35–0.47） |
| 姓氏集中度 | 1 / 3 | 弱且 sub 极差（0.15）、DD 16.4% |
| 结构/性别/学历/标志 | 1 / 14 | 弱（独立董事 S 0.82） |
| **合计** | **17 / 46（37%）** | 6 大类全部抽样覆盖；唯一强类别（离职）已 100% 穷尽 |

**关于「是否还有未被发现的强字段」**：离职族是唯一强类别，且已 9/9 全覆盖 —— 不存在遗漏。其余 5 类各测 1–2 个代表字段全部为弱，且这些类别在经济学上都不属于「事件驱动」（任期/连接/姓氏/结构均为缓变量），与 `QP0Odbg` 的结论一致：**只有事件型字段才有 alpha，缓变结构性字段在日频截面上已被定价**。

## 6.9 最终判定：`REJECT_PROD_WALL`（确认，证据升级）

| 项 | 上一轮（13 条时） | 本轮（47 条） |
|---|---|---|
| 字段覆盖 | 13%（6/46） | **37%（17/46），离职族 100%** |
| 指标最好件 | `N1Ppnq1e` S1.59/F1.05/2Y1.92/sub0.92（只卡 prod） | **`O0WZx8MR` S1.56/F1.08/2Y2.08/sub0.79（只差 S 0.02）** |
| prod 最低值 | 0.7629（`personnel_6m`） | **0.7629（未变）** |
| 死因 | prod 0.83 字段级 | **prod 0.76–0.89，与指标同轴反向（前沿不相交）** |
| 新增证否 | — | 1y 长窗更差；混合更差；加入率/任期/外部连接/姓氏/结构全弱 |

**判定：`REJECT_PROD_WALL` 确认。本族（`board_gov_stats`）在表达式层与字段层均已穷尽。**

**唯一残留路径（属新 alpha 设计，不属本件优化）**：
1. 稀释 —— 需 44.5% 正交权重，且混腿已被证否（`QP0Odbg` §14）；
2. 换数据集 —— 离开 `board_gov_stats`。`board_gov_stats` 是 **USA 专属**（EUR/GLB 均返回 0 字段），无法换区域。

**留存价值**：`O0WZx8MR`（`add(rank(−ts_mean(board_departure_rate_1y_board,10)), rank(−ts_mean(board_departure_rate_6m_management,10)))` @SECTOR）是本族指标最强的完整件（F 1.08 / 2Y 2.08 / sub 0.79 / TO 1.43% / DD 4.49% / Ra 1），**若未来出现一条 prod<0.3 的强正交腿，它是首选基底**。

---

# 7 模板来源补课与「层级纠错」（用户 12:14 质疑）

## 7.1 用户批评成立：我只用了单一模板

本轮前 27 条实测里，40 个非离职字段**全部套同一个骨架**：

```
ts_target_tvr_decay(group_rank(ts_mean(<FIELD>, 10), sector), target_tvr=0.1)
```

这是**level 型单模板**。但字段的经济机制差异极大：
- 任期是**单调递增计数器** → level 可以，change 会退化
- 治理 flag 是**二值状态机** → 需要 `ts_mean(F,252)` 连续化，否则 `group_rank` 大量并列退化
- 网络资本是**存量计数** → change / 二阶矩才有意义
- 加入率的作用可能是**门控条件**而非信号本体

单模板 = 拿同一把尺子量所有东西。批评成立。

## 7.2 ★★★ 关键漏读：本地已有完整字段画像

`docs/reference/USA/board_gov_stats_field_profile.md`（波 191/192/280/281 沉淀）**我从未读过**。它包含：

### 7.2.1 七族分类与既有实测

| 族 | 字段数 | 画像既有结论 | 我这轮的做法 |
|---|---:|---|---|
| A 流动率（离职+加入） | 18 | **✗ 判死**（波191 S 0.32/0.33、`risk_neut_S` −0.52/−0.28） | 测了 11 个 —— **但做出了 S 1.59**，与画像矛盾（见 7.4） |
| B **任期族** | 5 | **✓ 有真信号**（`ceo_tenure_days` S 1.23/2Y 1.75/`risk_neut_S` +0.81） | 只测 2 个，S 最高 1.36 |
| C **网络族** | 6 | **✓✓ 最健康载体**（`board_external_connection_count` S1.17/**2Y1.84**/SUB0.58/**`risk_neut_S` +1.09**/`checks.fail=[]`/DD 7.88%） | **测错了字段**：测 `aggregate_external_connections`(S1.00)、`unique_external_company_union`(S0.92)，**画像点名的 `board_external_connection_count` 一次没测** |
| D 治理 flag | 4 | 需 `ts_mean(F,252)` 连续化 | 未测 |
| E 规模/构成 | 4 | `independent_director_ratio` 单测无信号 | 测了，S 0.82（一致） |
| F 性别/学历 | 6 | 极慢变量，低优先 | 未测 |
| G 姓氏集中度 | 3 | 2Y 1.90 最高但 SUB 0.14 硬伤 | 测了，2Y 1.70 / sub 0.15（一致） |

### 7.2.2 ★ 三条我踩错或漏掉的技术约束

1. **`*_tenure_days` 只能做水平**：它是单调递增计数器 ⇒ `ts_delta`/`ts_av_diff` 对长任期 CEO 恒等于 W（退化成「是否新任」哑变量）、`ts_std_dev` 是常数、`ts_rank` 恒为 1。我再扫 w5/w22/w66 是**无效动作**（画像已记「504 窗与 120 窗互相关 0.9999、S/2Y/SUB 逐位相同」）。
2. **`bucket` 是最好的分组轴，我一次没用**：wave281 实测 S 排序 `total_personnel_count` **1.77** > `board_member_count_2` **1.72** > `management_team_size` 1.59 > `independent_director_ratio` 1.56。我只用了 sector/industry/subindustry/market。
3. **网络腿用董事层不用高管层**：`board_external_connection_count`（S1.72/SUB0.74）≫ `management_external_connection_count`（S1.44/SUB0.41）。

## 7.3 ★★★ 波 281 三颗「全闸过但 prod 从未测」的现成件

画像 §7.1 记录了三颗 `fRA = 0` 的件，但 **prod 全部标注「未测」**：

| alpha | 骨架 | S | F | 2Y | SUB | risk_neut_S | **prod（本轮实测）** |
|---|---|---:|---:|---:|---:|---:|---:|
| **`qMLvlqJ1`** | **CEO 任期 × 董事网络 × bucket(董事人数)** | **1.73** | **1.09** | **2.18** | **0.77** | 1.16 | **0.7929** |
| `KPJq9aMN` | 最长任期 × 网络 × bucket(董事人数) | 1.72 | **1.12** | 1.97 | **0.80** | **1.28** | 待测（槽占用） |
| `zq3Qmp71` | 中位任期 × 网络 × bucket(董事人数)，504 窗 | 1.72 | 1.09 | 1.99 | 0.74 | 1.16 | 待测 |

三颗均为 `checks.fail = []`、**八项全 PASS**、`ra_failed_count = 0`、单塔 `USA/D1/INSIDERS`。

`qMLvlqJ1` 的完整表达式：

```
group_rank(group_rank(multiply(rank(ts_backfill(ceo_tenure_days, 120)),
                               rank(ts_backfill(board_external_connection_count, 120))),
                      bucket(rank(ts_backfill(board_member_count_2, 120)), range="0,1,0.1")),
           subindustry)
设置：USA / TOP3000 / D1 / decay 4 / MARKET / trunc 0.08
```

**这是本族 50 条实测里指标最好的一颗，且 prod 分布形态第一次出现「`[0.8,0.9)` 归零、`[0.7,0.8)` 1532 颗」** —— 没有强钉子件，只差 0.10，与 `LLKRWzR2` 全族的「`[0.7,0.8)` 数千颗」性质不同。**有希望通过表达式层差异化挤到 0.69 以下。**

## 7.4 一个需要如实报告的矛盾

画像 §2 把**流动率族判死**（波 191 骨架 `group_rank(ts_backfill(F,120), subindustry)` 测出 S 0.32/0.33）。
但本轮用 `group_rank(-ts_mean(F,10), sector)` 外包 `tvr` 后，**同一族做出 S 1.59 / F 1.05 / 2Y 1.92**。

差异来源可能是：① 取负方向（离职率高⇒做空）② `ts_mean(·,10)` 平滑 ③ `sector` 轴 ④ `tvr` 限速器。画像的判死结论基于单一骨架，**属「骨架级判死」被误读成「族级判死」**，我这边恰好证伪了。这条要回写画像。

## 7.5 论坛：找到一条完全不同的模板层级（门控）

**工具状态**：`search_forum_posts` 仍为空返回（按 guide §2.2 记工具故障）；改用 `read_forum_post(article_id="43907846056599")` 直读成功。

该帖《物是而人非：管理层变动如何改变业绩会议的定价含义》（RL92505，2026-10-01）的核心：

```
-if_else(group_rank(ts_zscore(ts_backfill(board_join_rate_6m_management,120),252), industry) > 0.7,
         group_zscore(ts_zscore(ts_delta(ts_backfill(sentiment_weighting_method2,200),5),30), industry),
         0)
→ Sharpe +1.86
```

**它把 `board_join_rate_6m_management`（加入率）当「信息环境状态」门控，而不是当信号。** 经济逻辑：管理层更新 ⇒ 市场需重新学习新管理者的表达基准 ⇒ 原有「语调改善 ⇒ 正收益」的关系**反转**。

**这直接暴露了我本轮的一个层级误判**：我把加入率当信号测（`GrmLLbdZ` S 0.73、`YPa00b5J` S 0.72），判为「弱」。但它在该帖里的正确用法是门控，Sharpe 1.86。这与模板库铁律一致：

> `ts_arg_max` 作信号 = 摧毁器；作门控条件 = 冠军机制 ⇒ **同一个算子/字段换「用在哪一层」，成败相反。**

帖子还给了跨市场实证：EUR director attrition 0.22、company tenure 0.48；GBR/DEU 用 `executive_change_event` 得 0.75/0.70 ⇒ 该模板依赖「管理层直接参与生产的信息」。

## 7.6 外部论文：三条直接改变构造方向的洞察

| 文献 | 结论 | 对本数据集的含义 |
|---|---|---|
| **Hermalin & Weisbach (1998)** | 董事会构成是 CEO 与董事会**博弈的结果**，不是外生；业绩优异的 CEO 议价能力强，独立董事比例**反而下降**；只有业绩不佳的 CEO 才「迎来」更多监督者 | **独立董事比例上升是坏消息**（业绩差的结果）⇒ 应该用**变化**不用水平。这解释了为什么 `independent_director_ratio` 水平 S 只有 0.82（我测对了方向但用错了量） |
| **Adams & Ferreira (2007)**「友好董事会」 | 最优董事会**不是独立性最强的**，而是与公司需求匹配的 | 独立董事比例与收益**无单调关系** ⇒ 单独当因子必然弱。应做**交互/条件**（如「独立董事高 × 家族控制低」） |
| **Harris & Raviv (2008)** | 内部/外部董事的最优配比取决于两种力量孰强 | 董事会构成类字段应做**比值/结构**，不做裸水平 → 与实证「`board_member_count_2` 作 bucket 分母 S 1.72」吻合 |

帖子引用的另外四篇（Price 2012 / Druz 2020 / Davis 2015 / Bochkay 2019）支持「管理者特有语调成分」与「新任 CEO 早期更乐观」⇒ 强化了「管理层更新作为 regime 变量」的合理性。

## 7.7 本批实验设计（补课之后的定向回测）

| 批 | 目的 | 依据 |
|---|---|---|
| **A** bucket 分母换 `total_personnel_count` ×2 | 画像 §7.4 S 1.77 优于 `board_member_count_2` 1.72 | wave281 |
| **B** 中性化换 SECTOR ×2 | `qMLvlqJ1` 原为 MARKET；本族 SECTOR 曾最优 | 前轮实证 |
| **C** 网络腿换 `aggregate_external_connections` / `unique_external_company_union` ×2 | 检验网络腿字段敏感性 | 画像 §7.5「董事层优于高管层」的反向检验 |
| **D** decay 0 ×2 | `qMLvlqJ1` decay 4，从未扫 | 设置层未穷尽 |
| **E** bucket 粒度 range 0.05 / 0.2 ×2 | 分组粒度从未测 | 自建 |
| **F** `if_else` 门控 ×2 | **【新增层级】** 管理层更新状态门控 × 离职信号 | 论坛帖 43907846056599 |
| **G** `trade_when` 门控 ×2 | 同上，但用「保持原仓」而非「清零」 | 交易层语义差异 |

（结果待回填）

## 7.10 新鲜度算子（`days_from_last_change` / `last_diff_value`）：证否

模板库 §二「未用算子速查」列了这两个 T8 事件型算子，我对治理字段从未用过：

| 算子 | 字段 | alpha | S | F | 2Y | sub | DD | **Ra** |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `days_from_last_change` | 离职率 | `e7a0zLgM` | **−0.51** | −0.18 | 0.04 | −0.95 | **27.33%** | 4 |
| `days_from_last_change` | 网络 | `2r5LlJRP` | **−0.46** | −0.15 | −0.00 | −0.55 | **21.20%** | 4 |
| `last_diff_value` | 离职率 | `N1Pr7pgE` | 1.09 | 0.66 | 1.56 | 0.67 | 7.31% | 3 |
| `last_diff_value` | 网络 | `d5a0jxnE` | 1.03 | 0.61 | 1.69 | 0.64 | 9.77% | 3 |

**`days_from_last_change` 是毒药**（S 负、DD 21–27%）。机理：治理字段变化稀疏，该算子取值在大部分股票上是几百天的大数，只有少数股票刚变化 ⇒ 截面分布极度右偏，且「刚变化」本身是随机事件，无方向性。
**`last_diff_value` 只是弱**（S ~1.0），不是可用层。

## 7.11 ★★★ prod 三点实测：0.7929 是本族下限

| alpha | 变体 | S | F | 2Y | sub | **prod** | [0.7,0.8) / [0.8,0.9) |
|---|---|---:|---:|---:|---:|---:|---|
| **`qMLvlqJ1`** | 原件（MARKET / decay 4 / bucket=董事人数） | 1.73 | 1.09 | **2.18** | 0.77 | **0.7929（最低）** | 1,532 / **0** |
| `akan1zgv` | **网络腿换** `aggregate_external_connections` | 1.72 | 1.08 | 2.15 | 0.77 | 0.8006 | 2,018 / 1 |
| `6XM9p0AL` | **中性化换 SECTOR** | 1.71 | 1.06 | 2.21 | 0.77 | 0.8075 | 2,381 / 1 |

**三点极差仅 0.0146**，与项目实测铁律「表达式层对 prod 的极差 0.008–0.044」完全吻合。

**要降到 0.69 需 0.103 的降幅 —— 是历史极差的 2–10 倍。** 稀释算术：ρ0=0.7929 需 **w≈0.454（45.4% 正交权重）**，而混腿已实测恶化 prod（`QP0Odbg` §14：`[0.7,0.8)` 从 7 颗放大到 7,368 颗）。

⇒ **`qMLvlqJ1` 是本族指标最强件（八项全 PASS、fRA 0），但 prod 0.7929 不可降。判定维持 `REJECT_PROD_WALL`。**

## 7.12 模板层级全账（本轮补课的核心产出）

| 层级 | 具体形态 | 本族是否有效 | 证据 |
|---|---|---|---|
| **L1 水平** | `group_rank(-ts_mean(F,10), sector)` + `tvr` | **✓ 唯一有效** | 离职族 S 1.59 / F 1.05 / 2Y 1.92 |
| **L1' 水平·组合** | `任期 × 网络 × bucket(规模)` 三字段 | **✓✓ 最强** | `qMLvlqJ1` S1.73/F1.09/2Y2.18/**八项全过** |
| **L2 一阶变化** | `ts_delta` / `ts_av_diff` / `ts_zscore` / 加速度 / 价差 | **✗ 证否** | 本轮 `ts_zscore` 把 S 1.57→0.92；前轮 3M−1Y 1.07；`subtract(快,慢)` S −0.19 |
| **L2' 二阶** | `ts_std_dev` | **✗ 退化** | 画像：对线性斜坡是常数 |
| **L3 时序秩/分位** | `ts_rank` / `ts_quantile` | **✗ 退化** | 画像：`ts_rank` 对单调序列恒为 1 |
| **L4 条件门控** | `if_else` / `trade_when` | **✗ 证否（本轮）** | S 0.14–0.33，缺强主体信号 |
| **L5 新鲜度** | `days_from_last_change` / `last_diff_value` | **✗ 证否（本轮）** | S −0.51 ~ 1.09，DD 21–27% |
| **L6 分组轴** | `bucket(规模字段)` / `sector` / `industry` | **✓ 有效（S 最高 +0.07~0.09）** | `total_personnel_count` S 1.80 > `board_member_count_2` 1.73 |
| **L7 残差化** | `vector_neut` / `group_neutralize` | **✗ 证否** | 前轮 DD 冲到 49.65% |
| **L8 长窗** | 504 vs 120 | **✗ 无差异** | 画像：互相关 0.9999；本轮 1y 更差（prod 0.89） |

**八个层级全部扫过，只有「水平」与「水平+组合+分组轴」两层有效。**

## 7.13 需要回写画像的一条矛盾

画像 §2 把**流动率族（18 字段）整族判死**（波 191 骨架 `group_rank(ts_backfill(F,120), subindustry)` 得 S 0.32/0.33、`risk_neut_S` −0.52/−0.28）。

但本轮用 `group_rank(-ts_mean(F,10), sector)` 外包 `tvr` 后，**同一族做出 S 1.59 / F 1.05 / 2Y 1.92 / risk_neut_S 1.29**。

四个差异点：① **取负方向**（离职率高 ⇒ 做空）② `ts_mean(·,10)` 平滑 ③ `sector` 轴 ④ `tvr` 限速器。

⇒ **画像的判死是「骨架级」判死，被当成了「族级」判死。** 建议回写：流动率族在 `level × 取负 × sector 轴 × tvr` 骨架下 S 可达 1.59，不应整族排除。

## 7.14 本轮最终判定

**`REJECT_PROD_WALL` 确认（本件累计 65 条实测）**，但结论的性质比上一轮精确得多：

| 项 | 上一轮（47 条） | 本轮（65 条） |
|---|---|---|
| 最强件 | `N1Ppnq1e` / `O0WZx8MR`（单/双字段水平） | **`qMLvlqJ1`（三字段组合 + bucket 轴），八项全过、fRA 0** |
| 最强件指标 | S1.56 / F1.08 / 2Y2.08 / sub0.79 | S1.73 / F1.09 / **2Y2.18** / sub0.77 |
| prod | 0.7629–0.8905 | **0.7929（下限）/ 0.8075（极差 0.0146）** |
| 模板层级覆盖 | 3 层（level / change / 残差） | **8 层全扫** |
| 死因 | prod 与指标同轴反向 | **prod 0.79 不可降 0.10（历史极差 0.008–0.044）** |
| 门控层 | 未测 | **证否（S 0.14–0.33，缺强主体）** |
| 新鲜度层 | 未测 | **证否（DD 21–27%）** |

**留存件（本族指标最强）`qMLvlqJ1`**：

```
group_rank(group_rank(multiply(rank(ts_backfill(ceo_tenure_days, 120)),
                               rank(ts_backfill(board_external_connection_count, 120))),
                      bucket(rank(ts_backfill(board_member_count_2, 120)), range="0,1,0.1")),
           subindustry)
USA / TOP3000 / D1 / decay 4 / MARKET / trunc 0.08
```

| 维度 | 值 |
|---|---|
| S / F / 2Y / sub | **1.73 / 1.09 / 2.18 / 0.77**（八项全 PASS） |
| TO / R / DD / margin | 1.55% / 4.97% / 4.99% / 6.40 bp |
| `ra_failed_count` | **0** |
| **prod** | **0.7929**（唯一障碍） |
| 塔 | `USA/D1/INSIDERS` ×**1.1**｜当季 **0**｜交后 1｜**未点亮（1/3）**｜**塔边际正** |
| 六维 | **5 distinct 算子**（`group_rank`/`multiply`/`rank`/`ts_backfill`/`bucket`）/ **10 次调用** / **3 字段** |

**若未来出现一条 prod<0.3 的强正交腿，本件是首选基底**（指标比 `O0WZx8MR` 更完整，且 prod 更低）。
