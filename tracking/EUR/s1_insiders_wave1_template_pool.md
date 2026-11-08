# S1 · EUR Insiders 第 1–2 波模板池

- 建池时间：2026-11-07｜字段画像：`docs/reference/EUR/insiders_field_profile_20261107.md`
- 派发档：`EUR / TOPCS1600 / delay 1 / decay 4 / SUBINDUSTRY / truncation 0.08 / unitHandling VERIFY / pasteurization ON / maxTrade OFF`，**`nan_handling: OFF`**（覆盖注入修复，见 §3）
- 模板数 **15**（要求 ≥10）。互异维度：**矩**（水平比率 / 隐含计数 / 一阶差分 / 极值 / 时序秩 / 二阶标准化 / 双比率差）× **角色档**（全体董事 / 董事直持 / 高管直持 / 全体高管）× **信息加工**（比率 / 广度 / 背离 / 趋势 / 支配度）× **平台自带指标**。

核心复用子式（记作 `NB`）= 净买入比率：
`NB(x) = divide(subtract(x_buy, x_sell), add(x_buy, x_sell))`

## 模板清单

| # | 名称 | 矩 / 几何 | 机制 | 表达式 | 算子 | 状态 |
|---|---|---|---|---|---|---|
| NB1 | 净买入比率（全体董事） | 水平比率 | Lakonishok–Lee：净买入（非买入总额）预测收益 | `group_rank(divide(subtract(total_buy_shares, total_sell_shares), add(total_buy_shares, total_sell_shares)), industry)` | 4 | **w1 已派** |
| NB2 | 买入广度（隐含人数） | 推导计数 | 多数人买 > 单人大买：`total/avg` = 参与人数 | `group_rank(divide(total_buy_shares, avg_buy_shares), industry)` | 2 | **w1 已派** |
| NB3 | 高管-全体背离 | 双比率之差 | 角色档背离：高管（最接近信息源）净买而全体董事净卖 | `group_rank(subtract(NB(top), NB(all)), industry)` | 8 | **w2 已派** |
| NB4 | 净买入趋势加速度 | 一阶差分 | Cohen–Malloy–Pomorski 机会型：偏离自身基线 | `group_rank(ts_delta(ts_mean(NB(all), 22), 66), industry)` | 6 | **w2 已派** |
| NB5 | 高管直持净买入 | 水平比率（最窄档） | 最严角色口径，噪声最小 | `group_rank(NB(total_secondary_top), industry)` | 4 | 待派 |
| NB6 | 广度差（买人数−卖人数） | 计数差 | 内部人意见分歧的方向化度量 | `group_rank(subtract(divide(total_buy_shares, avg_buy_shares), divide(total_sell_shares, avg_sell_shares)), industry)` | 5 | 待派 |
| NB7 | 显著性支配度 | 梯度比 | Seyhun：单笔越大越有信息；头号交易相对次号交易的支配 | `group_rank(divide(significant_value_1, significant_value_2), industry)` | 3 | 待派（**符号未知**） |
| NB8 | 平台方向指标 | 单场 + 平滑 | 平台自算整体方向偏置 | `group_rank(ts_mean(directional_indicator, 22), industry)` | 3 | 待派（符号未知） |
| NB9 | 方向指标增强 | 单场 + 平滑 | 增强版方向偏置，可与 NB8 做一致性检验 | `group_rank(ts_mean(directional_indicator_2, 22), industry)` | 3 | 待派 |
| NB10 | 净买入年度峰值 | 极值（时序 max） | 一年内最强的内部人买入时刻仍在起作用（慢信号，低换手） | `group_rank(ts_max(NB(all), 252), industry)` | 5 | 待派 |
| NB11 | 机会型 z 分数 | 二阶标准化 | 当前净买入相对自身 252 日分布的偏离 = 机会型交易 | `group_rank(ts_zscore(NB(all), 252), industry)` | 5 | 待派 |
| NB12 | 高管单笔规模占比 | 均值比 | 高管平均单笔相对全体平均单笔 = 高管下注力度 | `group_rank(ts_mean(divide(avg_top_buy_shares, avg_buy_shares), 22), industry)` | 4 | 待派 |
| NB13 | 买压基线（对照组） | 水平 | 证伪「异常买入 vs 买压本身」：裸买入总额是否有信号 | `group_rank(ts_mean(total_buy_shares, 66), industry)` | 3 | 待派（对照组专用） |
| NB14 | 净买入时序秩 | 时序 rank | 当前净买入在自身 252 日中的分位（与 NB11 同轴不同矩） | `group_rank(ts_rank(NB(all), 252), industry)` | 5 | 待派 |
| NB15 | insiders1 欧元总额 | 向量和 | 跨市场可比的交易金额（方向待诊断） | `group_rank(vec_sum(insd1_valueeur), industry)` | 3 | 待派（依赖 §4 诊断 3） |

## 派发记录

### 第 1 波（NB1 / NB2）
- multisimulation：`XjwiialX4ujcr41dNfRpnBb`
- 目的：先用最经典的两条机制建立基线，同时验证「覆盖率注入」是否也是该集「几乎无人生还」的原因。

### 第 2 波（NB3 / NB4）
- multisimulation：`3XXZGJ4x14EFb7x56ZFZiga`
- 目的：角色档背离 vs 时序加速度，两个方向都与 NB1 正交。

## 纪律备注

- **本集全部 MATRIX 字段 ⇒ 不存在 `event input` 限制**，可以自由做标量算术（与 `analyst45` 全 VECTOR 的情形相反）。
- 已被证伪 / 严禁的写法：`add(multiply(w1,A), multiply(w2,B))`（同数据集加权两腿相加，`poison_structures.equal_weight_leg_add`）；跨数据集 `subtract`（破 ATOM）。
- NB1/NB3/NB4/NB5/NB6 等含 `divide(·, add(buy, sell))` 的子式在「买卖皆无」时是 `0/0`；`nan_handling OFF` 下这会自然变成「无持仓」而不是「做空」，这正是我们要的语义，但仍需用 `longCount/shortCount` 复核。


## 7. 论坛情报驱动的补充模板（2026-11-07 检索所得，第 3 波起）

### 7.1 三条直接影响策略的情报
1. **买侧已饱和**：帖《【Data】怎么用 insiders：买侧已经写烂》直言买入方向被反复挖掘 ⇒ 应把重心移到**卖压侧**与**仓位比**。
2. **EUR 已存在净买卖配方**：帖《把两个不同量纲的内部人交易额相除：EUR/TOP2500 上从 0.77 到 1.89》报告 `total_top_buy_shares − total_top_sell_shares` 的 **63 日窗口**做到 **Sharpe 1.90 / Fitness 1.00**（EUR/TOP2500）。⇒ 直接的「净买卖差分」已被占据，**重复它只会撞 self/prod 相关性**，只能当 benchmark 对照，不能当交付件。
3. **卖压侧在 GLB 被做到 2.18**：帖《从 0.47 到 2.18：一个 GLB 内部人卖压信号的完整研究记录——四次证伪、一次诊断和一次掩码》 — 卖压 + `group_rank` 子行业内部排名 + 掩码。⇒ **EUR 的卖压侧尚无人报告**，是当前最空的角。

### 7.2 新增模板
| # | 名称 | 矩 / 几何 | 机制 | 表达式 | 算子 | 状态 |
|---|---|---|---|---|---|---|
| SP1 | 卖压总额（全体董事） | 水平 + 长窗和 | 内部人卖出＝知情者的负面私人信息；买侧饱和后的空位 | `group_rank(ts_sum(total_sell_shares, 66), industry)` | 3 | 第 3 波候选（正号，做空高卖压） |
| SP2 | 卖压占比 | 比率（非镜像） | `sell/(buy+sell)` 与 NB1 不是简单取负（分母不同） | `group_rank(divide(total_sell_shares, add(total_buy_shares, total_sell_shares)), industry)` | 3 | 第 3 波候选 |
| SP3 | 高管卖压 | 水平 + 长窗和 | 最严角色档的卖压，信息含量最高 | `group_rank(ts_sum(total_top_sell_shares, 66), industry)` | 3 | 第 3 波候选 |
| SP4 | 净买卖额（对照基准） | 水平差 + 63/66 窗 | **论坛已报告 EUR S1.90**，只作 benchmark 校准本波读数是否同量级 | `group_rank(ts_sum(subtract(total_top_buy_shares, total_top_sell_shares), 66), industry)` | 4 | 仅对照，不作交付 |
| CV1 | 仓位比（conviction ratio） | 向量和之比 | DEU 帖：`交易股数/交易后持股` 天然做规模标准化，例行小额被大分母压成 0，只留异常重仓 | `group_rank(divide(vec_sum(insd1_shares), vec_sum(insd1_holdings)), industry)`（insiders1） | 4 | 待派（依赖 insiders1 方向诊断） |
| CV2 | 显著交易集中度 | 份额比 | 头号显著交易在显著交易总和中的占比 = 单笔支配度（替代 NB7 的除法口径） | `group_rank(divide(significant_value_1, add(significant_value_1, significant_value_2)), industry)` | 3 | 待派 |

### 7.3 纪律推论
- **不得交付 NB1 的直接线性变体**（`ts_sum(buy−sell, 63/66)`）：该组合已被论坛公开且已在 EUR/TOP2500 打出 S1.90，重复实现只会撞 self correlation。
- NB1（比率口径）与 SP4（差分口径）**量纲不同**，前者无量纲、后者是股数水平 —— 即便同源也不是同一个 alpha，但仍需在提交前跑 `compute_mutual_correlation` 互测。
- 卖压侧做多/做空的符号**必须按实测**：文献说内部人卖出信息量弱于买入（Lakonishok–Lee），但 GLB 实证卖压更强，两者冲突 ⇒ 以 EUR 实测为准。
