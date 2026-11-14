# INSIDERS 二次攻坚 · Step 1 设计与数据集分析（2026-11-11 晚）

> 用户指令：再次锁 INSIDERS，说明挖掘思路与数据集分析。

## 一、数据集分析（实测字段清单）

### insiders1（8 字段，全 VECTOR，cov 0.5343）

| 字段 | 用途现状 | 状态 |
|---|---|---|
| insd1_holdings | Δ66 平滑（1.06）/ ts_ir（0.97）/ 仓位占比分母 / ts_rank·zscore（空心）| ✅ **核心字段** |
| insd1_shares | 仓位占比分子 / 交易量 | ✅ 已用 |
| insd1_valueeur | valueeur/holdings（0.74）/ ts_ir 变体（1.06→弱）| ✅ 已用（次级）|
| insd1_tradesignificance | sig 加权（0.72）/ sig==3 门控（2Y 1.34）| ✅ 已用 |
| insd1_price | 仅 ts_rank(price,66)（0.93 空心）| ⚠️ **只测了水平分位，相对价格未测** |
| insd1_value | 未测 | ❌ 未测（valueeur 已覆盖同信息）|
| insd1_gvkey | 公司 ID | — 无数值语义 |
| transaction_currency_code | 币种 | — 元数据 |

### insider_agg_matrix（34 字段，全 MATRIX，cov 0.5342-1.0）

| 类别 | 字段 | 状态 |
|---|---|---|
| 大额交易价值 | significant_value_1/2/3/4 | ✅ SV1·SV2 已测、**SV3/SV4 未单独测** |
| 集中度 | 由 SV1-4 构造 HHI / Top2 | ⚠️ HHI 已测、Top2 未测 |
| 方向指标 | directional_indicator | ✅ 已测（单用 TO 偏置，与 SV1 相乘 2Y 1.43）|
| 买卖股数总量 | total_buy/sell_shares、total_top_*、total_secondary_* | ✅ 已用（买卖比 0.62）|
| **平均买卖股数** | avg_buy/sell_shares | ✅ 已用（鲸鱼集中度 0.61）|
| **平均（高管/直接）** | **avg_top_buy/sell_shares、avg_secondary_*** | ❌ **6 个字段全未测** |
| 高管大额榜 | top_significant_value_1-4 | ❌ **4 个全未测**（value_1 已证不可访问）|
| 方向大额榜 | directional_significant_value_1-4、top_directional_significant_value_1-4 | ❌ **8 个全未测**（value_1 已证不可访问）|
| 方向指标 2 | directional_indicator_2 | ❌ 已证不可访问 |

**结论：34 字段中 4 个已证不可访问、约 12 个已用、约 18 个未测**（其中 6 个 avg_* 待验可访问性）。
⇒ **字段面远未穷尽**——这是我二次攻坚的主要依据。

## 二、挖掘思路（分层递进，每层都要归因）

1. **机制层**：先把「内部人在做什么」翻译成数学量。已知持仓变化(Δ66 1.06) > 大额金额(0.86) > 买卖比(0.62)，说明**持仓维度是正确载体**。
2. **构造层**：只有改变排序的算子有效（单调变换在 group_rank 下是空操作，已逐位实证）。
3. **组合层**：三正交排序（变化×信噪比×集中度）产生真实协同；同源双腿无增益。
4. **中性化层**：个股级信号禁行业中性 → market 外层 1.24 → 嵌套 1.27 → **cap 分桶 1.40**。
5. **设置层**：nan ON 必须；decay/truncation 无效；**平台中性化轴从未扫过**（全程 SUBINDUSTRY）。

## 三、本轮切入点（两个从未测过的轴）

### 轴 1：平台中性化（batch 级设置，此前 150 臂全用 SUBINDUSTRY）
- A 批 = **MARKET**，B 批 = **CROWDING**（同 8 臂）
- 假设：表达式内已有 cap 桶 + sector + market 三层，平台中性化可能被大幅覆盖；但 CROWDING（拥挤度中性）可能带来额外的风格剥离

### 轴 2：未测字段与新机制（8 臂）

| # | 臂 | 机制 | 依据 |
|---|---|---|---|
| 1 | 冠军对照 | cap桶三正交 | 锚点 1.40/1.54 |
| 2 | 去 cap 桶 | 测 cap 桶的纯贡献 | 归因 |
| 3 | C→**活动加速比** Σ22/Σ252(shares) | **「突压」结构**：近期交易相对长期基线激增 | 论坛 72 赞「维基突压」思想迁移 |
| 4 | C→**Top2 集中度** SV1/(SV1+SV2) | 前两笔占优程度 | 未测集中度变体 |
| 5 | C→**高管平均买卖比** avg_top_buy/avg_top_sell | **CMP 2012 高管更知情**（首次测 avg_top_*）| 18 个未测字段中信息密度最高 |
| 6 | C→**SV3** 单测 | 第三大笔价值 | 未测字段 |
| 7 | C→**交易价相对** price/ts_mean(price,252) | 内部人成交价相对自身历史（溢价买入=强信念）| price 字段只测过水平分位 |
| 8 | **活动加速比单腿** + cap桶 | 该机制的独立强度 | 判断是否值得作主腿 |

## 四、判读线

- 任一臂 **S ≥ 1.45** ⇒ 新机制有效，进定向补
- 任一臂超冠军（1.40/1.54）⇒ 替换主腿
- 全部 ≤ 1.40 ⇒ 该轴关闭，继续下一批（avg_secondary_* / top_significant_value_2-4 / decay 0·2·8 / pasteurization）