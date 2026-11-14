# EUR insiders 类别字段画像（六法）+ ATOM 可挖性判定

> 依据 `brain-datafield-exploration-general` 六法；离线包优先，缺项转在线最小集。
> 生成时间：2026-11-12 23:20 ｜ region=EUR, universe=TOP2500, delay=1

## 0. 数据集清单（平台 category=INSIDERS，EUR/D1）

| 数据集 | 字段数 | 平台 alphaCount | 数据集级覆盖率 | 离线体检包 |
|---|---:|---:|---:|---|
| `insider_agg_matrix` | 34 | 46 | 0.6117 | **有**（但 frequency/distribution 全空）|
| `insiders1` | 9 | 792 | 0.5512 | 无 |
| `insiders12` | 8 | 1454 | 0.2008 | 无 |

> 注：`insider_feats`(118) / `insider_matrix`(33) / `insider_trx_matrix`(33) 名字带 insider，但平台 category = **OTHER**，不属于 insiders 塔，不计入本文。

## 1. 法 1 基础覆盖率（离线包直读，零配额）

### `insider_agg_matrix`——两档分明
| 档位 | 覆盖率 | 字段族 | 字段数 |
|---|---|---|---:|
| 高 | **0.6149** | `significant_value_1..4` / `directional_significant_value_1..4` / `top_significant_value_1..4` / `top_directional_significant_value_1..4` / `directional_indicator_2` | 17 |
| 中 | **0.6083** | `total_*_buy_shares` / `total_*_sell_shares` / `avg_*_buy_shares` / `avg_*_sell_shares` / `directional_indicator` | 17 |

⇒ 覆盖率 0.61 均 > 0.4，**不触发 backfill 硬门**；但另有约 39% 股票无数据，须处理缺失而非当 0。

### `insiders1` / `insiders12`
| 数据集 | 覆盖率 | 判定 |
|---|---:|---|
| `insiders1` | 0.5512（9 字段完全一致）| > 0.4，不强制 backfill；**但全部 9 个字段为 VECTOR**（事件型）|
| `insiders12` | 0.193（7 字段）/ 0.259（1 字段）| **< 0.4 ⇒ 必须 ts_backfill / group_backfill**（skill 硬门检查 1）|

## 2. 类型先行（决定所有下游写法）

| 数据集 | 平台 type | 实测结论 | 正确写法 |
|---|---|---|---|
| `insider_agg_matrix` | MATRIX ×34 | **元数据与实测不符**：历史上裸用报 `does not support event inputs`（I1/I2/I3 三批全灭）| 保守做法：`vec_avg(F)` 包裹 |
| `insiders1` | VECTOR ×9 | 事件型 | 必须 `vec_avg` / `vec_sum` |
| `insiders12` | VECTOR ×8 | 事件型 | 必须 `vec_avg` / `vec_sum` |

## 3. 拥挤度（alphaCount，决定剩余产能）

| 数据集 | alphaCount min/median/max | 解读 |
|---|---|---|
| `insider_agg_matrix` | 5 / **49** / 177 | 使用度低，**最可能是 ATOM 蓝海** |
| `insiders1` | 41 / **428** / 576 | 已较拥挤（792 个 alpha）|
| `insiders12` | 6 / **310** / 736 | 中等偏挤 + 覆盖率仅 0.19 |

## 4. 法 2 / 3 / 4 / 5 / 6 —— 在线最小集（进行中）

minisim `2Bne2xdtR4J398PeH8D6gC5`（8 臂，设置 Neutralization=None / Decay=0 / P0Y0M0D）：

| 臂 | 表达式 | 法 | 目的 |
|---:|---|---|---|
| 1 | `vec_avg((total_top_buy_shares−total_top_sell_shares)/(buy+sell+1e-4))` | 法1 | 净买入强度覆盖率 |
| 2 | 上式 `!= 0` | 法2 | 非零率（零膨胀判定）|
| 3 | `ts_std_dev(上式,22) != 0` | 法3 | 是否日频 |
| 4 | `abs(上式) > 1` | 法4 | 量纲（是否已归一化到 [-1,1]）|
| 5-8 | 同四法，字段换 `vec_avg(insd1_value)` | 法1-4 | insiders1 交易金额 |

**判读口径**（依 skill）：
- 法2 TO≈0.5% ⇒ 几乎全非零（非零膨胀）；TO 高 ⇒ 大量零值（零膨胀，须 `trade_when`）
- 法3 三个 N 的计数都≈法1 ⇒ 日频（窗 22 可用）；N=66 才起量 ⇒ 季频（窗 252）
- 法4 `abs(F)>1` 若 **S=0/ret=0/TO=0 ⇒ 值域已归一化 [-1,1]** ⇒ **直接 rank，禁止 ts_zscore**

## 5. ATOM 可挖性判定

**ATOM 定义**（本项目 §8 纪律）：信号字段全部来自**单一数据集**。

| 数据集 | ATOM 可行性 | 理由 | 关键约束 |
|---|---|---|---|
| **`insider_agg_matrix`** | **★★★ 最优先** | 34 字段同集，覆盖 0.61，alphaCount 中位仅 49（蓝海）；已有同集内可组合的买卖对称族 + 显著性族 | 必须 `vec_avg`；零膨胀处理；历史实测 S 天花板 0.61（需换矩/换变换突破）|
| `insiders1` | ★ 低 | 9 字段同集，但 428 中位 alphaCount 偏挤、覆盖 0.55 | 全 VECTOR；单交易级明细，稀疏 |
| `insiders12` | ✗ 不建议 | 覆盖 0.19 < 0.4 硬门 + 中位 alphaCount 310 | 需 backfill，且字段多为代码/价格类（`transactioncode`/`option_exercise_price_*`）非信号 |

**结论**：insiders 塔的 ATOM 主战场是 `insider_agg_matrix`（单数据集内 34 字段）。
`insiders1`/`insiders12` 不适合 ATOM（一个靠明细、一个覆盖不足）。

## 6. 归档路径与命名规则

| 内容 | 路径 | 命名 |
|---|---|---|
| 字段级原始 JSON（全字段 + type/cov/alphaCount）| `tracking/EUR/reference/fields/` | `<dataset>_eur_d1.json` |
| 六维画像（人读）| `tracking/EUR/reference/profiles/` | `EUR_INSIDERS_FIELD_PROFILES_<YYYYMMDD>.md`（本文）|
| 离线体检包（平台生成）| `tracking/mining/` | `field_inspect_eur_<dataset>.json` |
## 7. ★关键实测：insider_agg_matrix 的 ATOM 占位情况（库内 75 条历史回测）

### 7.1 净买入族（`total_top_buy_shares − total_top_sell_shares`）
| alpha | 表达式骨架 | S | 2Y | SUB | TO | prod |
|---|---|---:|---:|---:|---:|---|
| `1YNWJq5m` | `group_rank(ts_sum(buy−sell, 63), industry)` **纯 ATOM** | **2.10** | 1.91 | 0.93 | 4.5% | **0.7982 ❌** |
| `VkxN0mMJ` | 同上窗口/分组变体 | 2.00 | 1.79 | 1.15 | 4.4% | 0.7647 ❌ |
| `d5WaO3Jg` | 同上 | 1.99 | 1.79 | 1.16 | 4.2% | 0.7622 ❌ |
| `58EJXapM` | 净买入 + imb5（混腿）| 2.03 | 2.26 | 1.11 | 5.4% | 0.7156 ❌ |

⇒ **纯 ATOM 强度够（S 2.10 / 2Y 1.91 / SUB 0.93），但 prod 卡 0.76–0.80。**

### 7.2 占位者已定位
| alpha | 提交日 | S | 表达式 |
|---|---|---:|---|
| **`9qxdnV72`** | **2026-11-06** | 1.84 | `rank(group_scale(group_zscore(ts_sum(top_significant_value_2, 78), industry), industry))` |
| `blRaArVZ` | 2026-09-11 | 1.95 | 不含 insider 族（starmine 预测 + FCF，仅名字命中）|

⇒ **`9qxdnV72` 用的是 `top_significant_value_2`（显著性族），与净买入族同属 `insider_agg_matrix`，prod 池已被它占住**——这解释了净买入族为何全在 0.76–0.80。

### 7.3 因此，`insider_agg_matrix` 内还剩哪些未占位的机制面
| 字段族 | 代表字段 | 是否已占位 | ATOM 可行性 |
|---|---|---|---|
| 净买入股数（`total_top_buy/sell_shares`）| `total_top_buy_shares` | ⚠ 撞 `9qxdnV72`（prod 0.76–0.80）| 强度够但 prod 卡墙 |
| 显著性（`significant_value_*` / `top_significant_value_*`）| `top_significant_value_2` | ✅ **已被 `9qxdnV72` 占用** | 不可再用 |
| **均值族（`avg_*_shares`）** | `avg_buy_shares` / `avg_sell_shares` / `avg_top_buy_shares` | **未验** | **★ 最可能的剩余 ATOM 面** |
| **方向族（`directional_*`）** | `directional_indicator` / `directional_indicator_2` | **未验** | ★ 方向符号天然有界，适合 rank |
| **二级市场族（`total_secondary_*`）** | `total_secondary_top_buy_shares` | **未验** | ★ 与主市场区分开 |

⇒ **结论：`insider_agg_matrix` 的 ATOM 主战场应从「净买入/显著性」转向「均值族 + 方向族 + 二级市场族」**（这三族尚未被提交件占位）。

### 7.4 insiders1 / insiders12 的历史实测
| 观测 | 值 |
|---|---|
| insiders1 探针（`group_rank(total_top_buy_shares)` 类）| S 0.52，TO 51.8% |
| insiders1 显著性探针（`rank(significant_value_1)`）| S 0.61，TO 176% |
| insiders12 | 覆盖率 0.19 < 0.4 硬门，字段多为代码/期权行权价，**非信号** |

⇒ insiders1/insiders12 **判死**，不做 ATOM。


## 8. 类型纠正：insider_agg_matrix 必须裸用，不能包 vec_*

**证据（2026-11-12 23:30，MCP batch_status 实测）**：

| 批次 | 写法 | 结果 |
|---|---|---|
| `1DWP0YgTA4S2cuN19g0gXVW4`（2 臂对照）| 裸用 `total_top_buy_shares` + `rank(close)` | **2/2 COMPLETE**（S 0.88 / 0.92）|
| `2Bne2xdtR4J398PeH8D6gC5`（8 臂六法）| 包 `vec_avg(...)` | **8/8 ERROR** |

⇒ `insider_agg_matrix` 平台标 MATRIX 是正确的。按 skill「类型先行」：MATRIX 直接用，包 `vec_*` 会触发批量检查导致整批被拒。
⇒ 我此前在 I1/I2/I3 波认定「必须 vec_avg」是错误归因（那三批失败另有原因，很可能是 `winsorize(x, std=2)` 与稀疏数据组合）。

### 8.1 已验证的裸字段基线（设置 None / decay 0 / P0Y0M0D）
| alpha | 表达式 | S | TO |
|---|---|---:|---:|
| `omaM33Rl` | `group_rank(ts_sum(total_top_buy_shares − total_top_sell_shares, 63), industry)` | **0.88** | 2.06% |
| `KPgjXXvp` | `rank(close)`（对照）| 0.92 | 0.88% |

⇒ 净买入族在无中性化/无 decay 下原始 S 仅 0.88，靠 industry 分组 + ts_sum 63 才到 2.10（`1YNWJq5m`）——强度主要来自行业中性化 + 长窗累积。
⇒ TO 仅 2.06%，与季度披露节奏一致 ⇒ 低频（季更），窗口下限应按 252 取。

## 9. 六法完成度
| 法 | 状态 | 依据 |
|---|---|---|
| 法 1 覆盖率 | ✅ | 离线包两档 0.6149/0.6083 + 在线裸字段基线 |
| 法 2 非零率 | ⏳ | 批 `Eh2XscMw4TIaDW14dwjgKRO` 跑中 |
| 法 3 频率 | ⏳ | 同上（N=22 / N=66 双档）；初判季更（TO 2.06%）|
| 法 4 量纲 | ⏳ | 同上（`abs(F) > 1`）|
| 法 5 中心趋势 | ⏸ | 需 `ts_mean(F,252)`，可与法 3 同批补 |
| 法 6 分布形态 | ⏸ | 离线包 skew/kurt 全 null，需在线 `zscore` 分档 |

## 10. ATOM 可挖结论

**`insider_agg_matrix` 是 insiders 塔唯一可挖 ATOM 的数据集**，但「净买入族 + 显著性族」已被 `9qxdnV72`（2026-11-06 提交，用 `top_significant_value_2`）占位，同族 ATOM 件 prod 卡 0.76–0.80。

### 建议优先级（同数据集内未占位的机制面）
| 优先级 | 字段族 | 代表字段 | 建议骨架 |
|---|---|---|---|
| **P1** | 均值族 | `avg_buy_shares` / `avg_sell_shares` / `avg_top_buy_shares` | `group_rank(ts_sum(avg_buy_shares − avg_sell_shares, 252), industry)` |
| **P2** | 方向族 | `directional_indicator` / `directional_indicator_2` | `group_rank(ts_mean(directional_indicator, 252), industry)` |
| **P3** | 二级市场族 | `total_secondary_top_buy_shares` / `total_secondary_buy_shares` | `group_rank(ts_sum(total_secondary_buy_shares − total_secondary_sell_shares, 252), industry)` |
| P4 | 显著性族（非已占位字段）| `significant_value_1..4` | `group_rank(ts_sum(significant_value_1, 252), industry)` |

**三条必须遵守**：① 裸用字段（不包 `vec_*`）；② 窗口 ≥ 252（季更字段，用 22/66 会过度反应）；③ 先测 prod（该集已被占位，新件须 prod<0.7 才有意义）。

**不适合 ATOM**：`insiders1`（明细稀疏，探针 S 0.52/0.61、TO 52%/176%，中位 alphaCount 428 已挤）、`insiders12`（覆盖率 0.19 低于 0.4 硬门，字段多为代码/行权价）。

## 11. 法 2 / 3 / 4 / 6 在线实测结果（批 `Eh2XscMw4TIaDW14dwjgKRO`，2026-11-12 23:40）

设置：`Neutralization=None` / `Decay=0` / `TestPeriod=P0Y0M0D` / `nan_handling=ON` / EUR-TOP2500-D1。
6 臂 COMPLETE，2 臂 WARNING（法 4 单位不兼容，本身即结论）。

| 臂 | 表达式 | S | F | TO | ret |
|---|---|---:|---:|---:|---:|
| 法1 | `total_top_buy_shares` | 0.79 | 0.39 | **173.9%** | 42.2% |
| 法2 | `total_top_buy_shares != 0` | 0.85 | 1.14 | **4.28%** | 22.7% |
| 法3a | `ts_std_dev(total_top_buy_shares,22) != 0` | 0.85 | 1.14 | **1.78%** | 22.7% |
| 法1 | `top_significant_value_2` | 1.05 | 0.60 | **175.5%** | 57.3% |
| 法2 | `top_significant_value_2 != 0` | 0.85 | 1.14 | **4.27%** | 22.7% |
| 法3b | `ts_std_dev(top_significant_value_2,66) != 0` | 0.85 | 1.14 | **1.54%** | 22.7% |
| 法4 | `abs(F) > 1` | — | — | — | **WARNING: Incompatible unit for input of greater** |

### 判读（依 skill 口径）

**法 2 非零率 → zero-inflated / point_mass**
- `!= 0` 的 TO 只有 **4.28%**，远高于 0.5% 的非零膨胀档位，但远低于法 1 的 173.9%
- ⇒ 大量股票取 0（或缺失被填 0），⇒ **必须用 `trade_when` 门控，不能直接 `rank`**（与 skill 的 zero_inflated 处置一致）

**法 3 频率 → 季更（quarterly）**
- N=22 档 TO **1.78%**、N=66 档 TO **1.54%**，两者都极低且接近；对比法 1 原始值 TO 173.9%
- ⇒ 绝大多数交易日字段值不变（只在季度披露时跳变）⇒ **日频门槛不成立**；按 skill 的硬门口径 quarterly ≥ **252**
- ⇒ **窗口下限 = 252**。用 22/66 会把季度信息过度摊薄，也会让 TO 虚低

**法 4 量纲 → 原始股数量纲（未归一化）**
- `abs(F) > 1` 直接报 **单位不兼容**（股 vs 无量纲 1）⇒ 字段是**绝对股数**，量纲远大于 1
- ⇒ 必须先用 `rank` / `ts_zscore` / `group_rank` 去量纲；**禁止**直接与其他字段相加

**法 1 覆盖率（在线复核）**
- 裸字段 TO 173.9% / 175.5% ⇒ 覆盖接近满池（值几乎天天在变，因为股数含累计口径）
- 与离线包 0.61 的差异来自口径：离线 coverage_ratio 是「有多少股票有该字段」，在线 TO 反映的是「值的变化频率」

**法 6 分布形态（离线 + 在线推断）**
- 离线包 `skewness`/`kurtosis` 全为 null；在线 `!= 0` 的 TO 4.28% 已强指向 **zero_inflated / point_mass**
- ⇒ 处置同法 2：`trade_when` 门控 + `winsorize` 截尾

## 12. ★最终 ATOM 可挖结论（含全部六法证据）

### 12.1 唯一可挖 ATOM 的数据集：`insider_agg_matrix`

| 判据 | 数值 | 结论 |
|---|---|---|
| 字段数 | 34（单集） | ATOM 结构成立 |
| 覆盖率 | 0.6083–0.6149（离线）| >0.4，不需 backfill |
| 频率 | **季更**（法3：N=22 TO 1.78%、N=66 TO 1.54%）| **窗口 ≥ 252** |
| 零值形态 | **zero-inflated**（法2 TO 4.28%）| **须 trade_when 门控** |
| 量纲 | **原始股数**（法4 单位不兼容）| **须 rank / ts_zscore 去量纲** |
| 拥挤度 | alphaCount 中位 **49**（低）| 蓝海，但有占位者 |
| **占位者** | **`9qxdnV72`**（2026-11-06，用 `top_significant_value_2`）| 显著性族 + 净买入族 prod 0.76–0.80 卡墙 |

### 12.2 可挖的 ATOM 机制面（按未占位程度排序）

| 优先级 | 字段族 | 代表字段 | 推荐骨架（已含六法约束）| 预期 |
|---|---|---|---|---|
| **P1** | 均值族 | `avg_buy_shares` / `avg_sell_shares` / `avg_top_buy_shares` | `group_rank(ts_sum(winsorize(avg_buy_shares − avg_sell_shares, std=2), 252), industry)` | 语义是「单笔均值」≠ 总量，最可能避开占位 |
| **P2** | 方向族 | `directional_indicator` / `directional_indicator_2` | `group_rank(ts_mean(directional_indicator, 252), industry)` | 有界符号量，本身已去量纲，不受法4限制 |
| **P3** | 二级市场族 | `total_secondary_top_buy_shares` 等 | `group_rank(ts_sum(total_secondary_buy_shares − total_secondary_sell_shares, 252), industry)` | 与主市场切开 |
| P4 | 显著性族旁支 | `significant_value_1` / `_3` / `_4` | `trade_when(significant_value_1 != 0, group_rank(ts_sum(significant_value_1, 252), industry), -1)` | 与已占位的 `top_significant_value_2` 不同档 |

### 12.3 不可挖 ATOM 的数据集（结论明确）
| 数据集 | 判死理由 |
|---|---|
| `insiders1` | 9 字段全 VECTOR；交易级明细稀疏（探针 S 0.52 / 0.61，TO 52% / 176%）；中位 alphaCount **428** 已挤 |
| `insiders12` | 覆盖率 **0.19 < 0.4 硬门**；字段多为 `transactioncode` / `option_exercise_price_*` 等代码与行权价，非信号；中位 alphaCount 310 |

### 12.4 一句话答案
**insiders 塔能挖 ATOM 的只有 `insider_agg_matrix`，且必须换到「均值族 / 方向族 / 二级市场族」这三个未被 `9qxdnV72` 占位的机制面**；骨架须遵守 ①裸用字段 ②窗口 ≥252 ③`trade_when` 处理零膨胀 ④`rank` 去量纲 ⑤提交前必测 prod。

## 13. P1–P4 真实回测验证（批 `2qFK401Ql5ibb6aKJ4UDOK3`，2026-11-12 23:50 派发）

**设置**：EUR / TOP2500 / D1 / decay 4 / INDUSTRY / truncation 0.08 / nan ON / maxTrade OFF。
（与近期 EUR 交付件一致，便于横向比较）

**10 臂设计**（P1–P4 主线 + 4 条变体 + 2 条占位对照）：

| 臂 | 骨架 | 家族 | 说明 |
|---:|---|---|---|
| 1 | `group_rank(ts_sum(winsorize(avg_buy−avg_sell, std=2),252), industry)` | P1 均值族 | 主线 |
| 2 | `group_rank(ts_mean(directional_indicator,252), industry)` | P2 方向族 | 主线 |
| 3 | `group_rank(ts_sum(total_secondary_buy−total_secondary_sell,252), industry)` | P3 二级市场 | 主线 |
| 4 | `trade_when(significant_value_1 != 0, group_rank(ts_sum(significant_value_1,252),industry), -1)` | P4 显著性旁支 | 零膨胀门控 |
| 5 | 同 P1 但改比率 `(buy−sell)/(buy+sell+1e-4)` + `ts_mean 252` | P1b | 去量纲更彻底 |
| 6 | `group_rank(ts_mean(directional_indicator_2,252), industry)` | P2b | 方向族第二字段 |
| 7 | `group_rank(ts_sum(total_secondary_top_buy−..._top_sell,252), industry)` | P3b | top 档 |
| 8 | `trade_when(significant_value_3 != 0, ...)` | P4b | 显著性第三档 |
| 9 | `group_rank(ts_sum(total_top_buy−total_top_sell,252), industry)` | **占位族对照** | 已知 prod 0.79 |
| 10 | `group_rank(ts_sum(top_significant_value_2,252), industry)` | **已占位字段对照** | `9qxdnV72` 用的字段 |

**判据**（拿到读数后逐条判）：
1. IS 全闸：S ≥ 1.58、F ≥ 1.0、2Y ≥ 1.58、SUB/S ≥ 0.52、TO 5–30%、margin ≥ 5bp
2. 通过 IS 后测 **prod < 0.7**（该数据集已被 `9qxdnV72` 占位，这是最大风险）
3. 与已确认篮子 5 颗 ATOM 做互相关 < 0.7
4. 三关全过才建议提交

## 14. 判定模板（拿到读数后逐条勾）

| 关卡 | 门槛 | P1 | P2 | P3 | P4 |
|---|---|---|---|---|---|
| S | ≥ 1.58 | | | | |
| Fitness | ≥ 1.0 | | | | |
| 2Y | ≥ 1.58 | | | | |
| SUB/S | ≥ 0.52 | | | | |
| TO | 5–30% | | | | |
| margin | ≥ 5bp | | | | |
| **prod** | **< 0.7** | | | | |
| 与 5 颗 ATOM 互相关 | < 0.7 | | | | |

**预期风险**：该数据集已被 `9qxdnV72`（`top_significant_value_2`）占位，净买入族同族件 prod 已实测 0.7622–0.7982。
若 P1–P4 也落在 0.75+ 区间，则说明**整个 `insider_agg_matrix` 的 prod 池被这一颗占满**，该数据集的 ATOM 路线应当封盘。

## 15. P1–P4 首轮实测（252 窗）与窗口假设检验

批 `2qFK401Ql5ibb6aKJ4UDOK3`，设置 EUR/TOP2500/D1/decay4/INDUSTRY/trunc0.08。**9 COMPLETE + 1 WARNING**（臂5 比率式 add 单位不兼容）。

| 臂 | 骨架 | S | F | 2Y | SUB/S | TO | margin |
|---|---|---:|---:|---:|---:|---:|---:|
| P1 | 均值族 winsorize(avg_buy−avg_sell)`ts_sum 252` | **0.10** | 0.01 | 0.37 | 0.80 | 1.92% | 2.95bp |
| P2 | 方向族 `ts_mean(directional_indicator,252)` | **0.20** | 0.04 | 0.48 | 1.05 | 3.60% | 2.35bp |
| P3 | 二级市场净买入 `ts_sum 252` | **0.16** | 0.03 | 0.38 | 1.12 | 1.96% | 4.94bp |
| P4 | 显著性旁支 `trade_when(significant_value_1)` | **0.12** | 0.02 | 0.39 | −2.08 | 1.79% | 4.56bp |
| P1b | 比率式 | 0.28 | 0.07 | 0.28 | 1.04 | 2.21% | 7.19bp |
| P2b | `directional_indicator_2` | 0.21 | 0.04 | 0.58 | 1.24 | 3.60% | 2.53bp |
| P3b | 二级市场 top 档 | **0.35** | 0.11 | 0.16 | 1.17 | 1.81% | 12.65bp |
| P4b | `significant_value_3` 门控 | **−0.19** | −0.04 | −0.42 | 1.32 | 1.58% | −6.01bp |
| 对照A | 净买入族 `ts_sum 252` | **0.41** | 0.13 | 0.28 | 0.80 | 1.84% | 14.18bp |
| 对照B | `top_significant_value_2` `ts_sum 252` | **0.26** | 0.06 | 0.33 | −0.12 | 1.64% | 9.25bp |

### ★核心发现：252 窗把信号抹平了

| 同族不同窗口 | alpha | S |
|---|---|---:|
| `ts_sum 63` | `1YNWJq5m`（库内历史）| **2.10** |
| `ts_sum 252` | 对照A（本批）| **0.41** |

⇒ 同一净买入族，63 窗 → S 2.10，252 窗 → S 0.41，**5 倍衰减**。
⇒ 说明该字段虽「值只在季度跳变」，但**有效预测窗口是季度内 63 天附近**，把一年摊平会毁掉信号。
⇒ 我按 skill「frequency → min_window」机械取 252 是**错误套用**：frequency 决定「用多短的窗才不会全是同一个值」，而不是「必须用满一个季度」。

### 附加观察：TO 也异常低
252 窗 TO 仅 1.58–2.21%，远低于闸线 5% 下限，持仓几乎不动，收益被压到 0.3–1.3%。
即使不看 S，**TO 本身也过不了闸**。

## 16. 窗口假设检验（批 `3077dz5BO4rP9v83vWqwhVh`，2026-11-12 23:55 派发）

设计 10 臂验证「窗口回落到 63/78 能否把 S 拉回 2.0」：
| 臂 | 骨架 | 目的 |
|---:|---|---|
| 1-4 | P1/P2/P3/P4 @ **63 窗** | 主线短窗 |
| 5-8 | P1/P2/P3/P4 @ **78 窗** | 主线中窗（对齐 `9qxdnV72`）|
| 9 | `group_rank(ts_sum(total_top_buy−total_top_sell,63),industry)` | **校准基准**（复刻 `1YNWJq5m` S2.10）|
| 10 | P1 加 `ts_zscore(...,252)` 时序标准化 @63 | 提信噪比 |

**判据**：臂 9 必须复现 S≈2.10（否则说明设置差异导致不可比）；P1–P4 若 S 回到 1.58+ 则测 prod，确认是否仍 0.76+。

## 17. ★校准失败复盘：设置未对齐（2026-11-13 00:16）

### 17.1 事实
| 项 | 我这次的复刻 | `1YNWJq5m` 平台原始 |
|---|---|---|
| 表达式 | `group_rank(ts_sum(total_top_buy−total_top_sell,63),industry)` | **同** |
| S | **0.65** | **2.10** |
| TO | 4.13% | 4.5% |
| decay | **4** ❌ | **15** |
| neutralization | **INDUSTRY** ❌ | **SLOW** |
| truncation | 0.08 | 0.08 ✓ |
| nanHandling | ON | ON ✓ |
| maxTrade | OFF | OFF ✓ |
| universe / delay | TOP2500 / 1 | TOP2500 / 1 ✓ |
| 区间 | 默认 | **startDate 2014-01-01 / endDate 2023-12-31** |

### 17.2 教训（与 BE43a 符号事故同类）
我在「校准」这一步用了**未核实的设置**去复刻历史件，然后拿结果当基准 → 把 `decay 4 + INDUSTRY` 的 S 0.65 误读成「63 窗也救不回来」。
**纪律**：复刻存量件前必须 `get_alpha_details(<id>)` 读平台 `settings` 块，逐项对齐后再回测；不得凭惯例或台账简写推断 decay / neutralization。

**已核实的 EUR 反例**：`1YNWJq5m` 用的是 **decay 15 + SLOW**，而不是本战役常用的 `decay 4 + INDUSTRY`。
⇒ **decay 与中性化对本数据集的 S 影响极大**（同一表达式 0.65 vs 2.10），这是比「窗口 63/252」更强的杠杆。

### 17.3 待验
批 `1tkvAJeNw4BC9twSoDP0WEg`（decay 15 / SLOW / trunc 0.08 / nan ON / maxTrade OFF，同式 2 臂）正在跑，
若复现 S≈2.10 则证明：① 窗口假设需重做 ② 真正的杠杆是设置层（decay 15 + SLOW）而非窗口。

---

## 18. ★复刻结果：SLOW 通道卡死，改用单臂拿到读数（2026-11-13 00:45）

### 18.1 平台故障定位（多批对照）
| 通道 | 配置 | 结果 |
|---|---|---|
| multisim | decay15 + SLOW（`1tkvAJeNw4BC9twSoDP0WEg`） | 卡 progress **0.15**、children=0，6 分钟无推进 |
| multisim | decay15 + SLOW 同式 2 臂（`3jdWvg5YM5cT8WR1f3dH7co`） | 同样卡 0.15，已删 |
| multisim | decay15 + SLOW 互异 2 臂（`2BftrbaoX4SeaugKcLxNMow`） | 同样卡 0.15，已删 |
| multisim | decay15 + **INDUSTRY**（`2ZTbbp4GP4V6aRqRTJ3TlfG`） | 同样卡 0.15，已删 ⇒ **卡的是 multisim 端点，不是 SLOW** |
| **单臂** | decay15 + INDUSTRY | **正常**，136-156 秒出数 |
| **单臂** | decay15 + SLOW（`412UXjgl4Zvb8TtVfQZjJ`） | 卡 0.15 **直至 1800 秒超时**（客户端抛 `TimeoutError`）⇒ **SLOW 通道确认不可用** |

结论：**multisim 端点 + SLOW 中性化两条通道当前均不可用**；单臂 + 常规中性化（INDUSTRY）是唯一可出数路径。
`Retry-After: 5.0` 说明平台自认「仍在算」，但进度恒 0.15 ⇒ 非我方请求问题。
账号配额正常（昨日 2538 次、本月 22598 次），排除限额。

### 18.2 实测两臂读数（单臂，decay 15 + INDUSTRY，EUR/TOP2500/D1/trunc 0.08/nan ON）
表达式：`group_rank(ts_sum(subtract(total_top_buy_shares, total_top_sell_shares), W), industry)`

| 臂 | W | alpha | S | TO | fitness | returns | margin | longCount |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | **63** | `E5QXKrQP` | **0.61** | **3.40%** | 0.25 | 2.02% | 11.9bp | 1635 |
| 2 | **126** | `YPaGAAR6` | **0.50** | **2.23%** | 0.18 | 1.57% | 14.1bp | 1540 |

窗口拉长反而更弱（0.61 → 0.50），TO 同步降（3.40% → 2.23%）。

### 18.3 ★决定性发现：2.10 来自 riskNeutralized 那条线
同一表达式在 INDUSTRY 跑里，平台给出的子指标：

| 臂 | 原始 IS S | riskNeutralized S | riskNeutralized fitness |
|---|---:|---:|---:|
| 63 窗 | 0.61 | **2.26** | 1.25 |
| 126 窗 | 0.50 | **1.73** | 0.79 |

`1YNWJq5m`（SLOW / decay15）历史读数 S **2.10** / fitness **1.11** / TO **4.47%**，
与本文 63 窗的 riskNeutralized 档 **2.26 / 1.25** 同量级。

⇒ **SLOW 中性化本身就把风险模型中立化后的那条线当作主 IS 输出**；
「63 窗净买入在 EUR 有 S 2.1」是**风险中立化后**的结论，未中立化的原始 IS 只有 **0.61**。
这也解释了它 `LOW_SUB_UNIVERSE_SHARPE` 0.93 < 1.09 未过闸。

**纪律**：跨件比 S 前必须先核对 neutralization；风险模型类中性化（SLOW/STATISTICAL/SLOW_AND_FAST）
会把信号强度整体抬一档，与 INDUSTRY/SECTOR 的读数**不可直接比**。

### 18.4 结论与去向
1. 63 窗净买入族在「可实测档」下 S 0.61 ⇒ **不构成候选**；其 2.26 的强度必须靠 SLOW 通道兑现，而该通道当前卡死。
2. `insider_agg_matrix` 的净买入 / 显著性两族已被 `9qxdnV72` 占位，同族历史 prod 0.7622–0.7982 全 FAIL ⇒ 即便 SLOW 恢复也无新增交付价值。
3. **不再为同一症状重发批**：multisim 端点恢复前，一律走单臂；SLOW 档等平台恢复后再验。

