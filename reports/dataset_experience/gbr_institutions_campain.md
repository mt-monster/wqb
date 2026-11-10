# GBR Institutions 数据集全字段画像与选集档案（2026-11-08）

区域：GBR / TOP700 / D1（SUBINDUSTRY / decay4 / trunc0.08）
范围：Institutions category 全部 5 个数据集、66 个字段（全量拉取 complete=true，禁止抽样）
归档路径：`reports/dataset_experience/gbr_institutions_campain.md`
命名规则：`<region小写>_<dataset>_campain.md`（历史沿用 campain 拼写，勿改；本文件覆盖 category 级扫描 + 选定集深挖）
上游证据：MCP get_datafields（平台实时）× 本地 field_profile --query --region GBR（历史测试）；塔盘点 get_pyramid_alphas（2026-11-08 实读）

## 一、塔点亮快照（选集前置闸）

GBR D1：model 6 ✱lit / news 3 ✱lit / analyst 3 ✱lit / pv 4 ✱lit / fundamental 3 ✱lit / shortinterest 3 ✱lit；
**institutions 0（未点亮，目标塔）**、other 1、sentiment/risk/earnings/macro/socialmedia/insiders/option/imbalance 全 0。
已点亮塔数据集一律不选 ⇒ institutions 类全绿可挖，倍率 1.4。

## 二、Category 扫描：5 数据集候选清单与选定理由

| 数据集 | cov | 字段数 | aC/uC | valueScore | 裁定 | 理由 |
|---|---:|---:|---:|---:|---|---|
| **fund_holdings_panel** | 0.9099 | 18 | 294/173 | 3.0 | **✅ 选定（主攻）** | 日频账户级交易面板（唯一日频源）；两个 WEAK 近闸字段（S1.26/S1.24）；EUR 论坛实战帖同集配方可移植；18 字段中 8 个 aC≤10 冷门 |
| institutions6 | 1.0 | 11 | 942/423 | 2.0 | ⏸ 暂缓（次选） | 季度报数持仓 → 本地画像全族 DEAD/DEAD_STATIC（to_med 0.018–0.038 近静态）；942 alpha 拥挤。除非主攻枯竭再按 M1-M3 重测 |
| institutions1 | 0.3118 | 7 | 52/34 | 5.0 | ❌ 排除 | coverage < 0.6（UNUSABLE 刀切线）；欧洲内幕交易 VECTOR |
| institutions4 | 0.39 | 6 | 47/38 | 4.0 | ❌ 排除 | coverage < 0.6 且本体是 identifier 映射类（非信号） |
| institutions25 | 0.0 | 24 | 90/54 | 5.0 | ❌ 排除 | GBR TOP700 coverage=0（无数据；GBR 域不适用 short-selling 面板） |

## 三、fund_holdings_panel 全字段画像（18/18，全 VECTOR，须先 vec_* 聚合）

本地画像列：n_tests / to_med / S_best / 2Y_best / verdict（历史配方，供参照非结论）。

| 字段 | cov | aC | 更新频率 | 分布特征 | 可用性 | 潜在 alpha 适用性 | 本地画像 |
|---|---:|---:|---|---|---|---|---|
| **boundary_transaction_total** | 0.9286 | 51 | 日频 | 离散计数右偏 | 高 | 新建仓/清仓边界事件强度 → 机构信息事件 ★主攻 | 9 / 0.094 / **S1.26 / 2Y1.52 / WEAK** |
| boundary_transaction_total_active | 0.8912 | 43 | 日频 | 离散计数右偏 | 高 | 同上（活跃账户口径） | 1 / 0.087 / S-0.49 DEAD |
| **stable_boundary_trade_count_21d** | 0.9286 | 57 | 日频 | 离散计数右偏 | 高 | 冷启动账户(21d 无边界交易)的边界交易 → 新信息/信念建立 ★主攻（EUR 论坛赢家字段） | 4 / 0.320 / **S1.24 / 2Y1.49 / WEAK** |
| stable_boundary_trade_count_21d_active | 0.8912 | 45 | 日频 | 离散计数右偏 | 中 | 同上（活跃口径） | 1 / 0.090 / S-0.58 DEAD |
| boundary_transaction_usd_value | 0.9286 | 7 | 日频 | 金额右偏重尾 | 中 | 边界事件金额（冷门 aC7） | 2 / 0.318 / S-0.51 DEAD（历史或方向反） |
| boundary_transaction_usd_value_active | 0.8912 | 6 | 日频 | 金额右偏 | 中 | 同上 | 1 / 0.086 / S-0.51 DEAD |
| top_weighted_transaction_number | 0.9286 | 13 | 日频 | 离散计数 | 中 | conviction 持仓交易数（跟单信念） | 2 / 0.188 / S0.07 DEAD_COUNT |
| top_weighted_transaction_number_active | 0.8912 | **0** | 日频 | 离散计数 | 中 | **平台零使用处女字段** | 1 / 0.072 / S0.07 DEAD |
| large_trade_count_50bps | 0.9286 | 9 | 日频 | 离散计数 | 中 | >0.5% AUM 大单数（信息强度） | 3 / 0.159 / S0.64 DEAD_COUNT |
| large_trade_count_50bps_active | 0.8912 | 9 | 日频 | 离散计数 | 中 | 同上 | 1 / 0.084 / S-0.42 DEAD |
| security_transaction_usd_value | 0.9286 | 40 | 日频 | 金额右偏重尾 | 中 | 总交易金额（规模轴/分母） | 1 / 0.067 / S-0.33 DEAD |
| security_transaction_usd_value_active | 0.8912 | 10 | 日频 | 金额右偏 | 中 | 同上（冷门 aC10） | 1 / 0.079 / S-0.57 DEAD |
| transaction_account_total | 0.9286 | 38 | 日频 | 离散计数 | 高 | 交易账户广度（注意力）——但 to 0.362 高换手 | 1 / 0.362 / S-0.12 DEAD_COUNT |
| transaction_account_total_active | 0.8912 | 21 | 日频 | 离散计数 | 高 | 同上 | 1 / 0.079 / S-0.40 DEAD |
| herfindahl_index_transactions | 0.9286 | 33 | 日频 | [0,1] 集中度 | 高 | 交易方集中度 HHI（信息不对称轴） | 3 / 0.152 / S0.57 DEAD |
| herfindahl_index_transactions_active | 0.8912 | 9 | 日频 | [0,1] | 高 | 同上（冷门） | 1 / 0.095 / S-0.01 DEAD |
| transaction_value_distribution_score | 0.9286 | 13 | 日频 | [0,1] 分布分 | 高 | 交易金额分布拥挤度 | 2 / 0.298 / S0.24 DEAD |
| transaction_value_distribution_score_active | 0.8912 | 5 | 日频 | [0,1] | 高 | 同上（冷门） | 1 / 0.092 / S0.01 DEAD |

**关键结构性事实**：
1. 全部 18 字段是 VECTOR —— 表达式必须先 `vec_avg/vec_sum` 聚合（平台铁律）。
2. base/_active 成对：_active 只计活跃账户、cov 低 0.04、历史全灭——主攻 base 口径。
3. USD 金额类历史 S 全负（−0.33~−0.57）——金额量纲在本区反向或弱；计数类才有 WEAK 信号。
4. 近十年覆盖待探针后以 get_alpha_yearly_stats 核验（连续多年空窗判废）。

## 四、机制映射（经济含义）与模板库（≥10 结构互异）

机制（外部先验）：
- **M-A 边界事件**：新仓建立/清仓 = 机构调仓的信息事件（initiation drift 文献）→ 做多高边界活动。
- **M-B 冷启动信念**：stable_21d = 21 个交易日未动过的账户重新建仓 → 新信息非从众（EUR 论坛赢家，S0.93/2Y2.28 @TOP2500）。
- **M-C 活动自历史 surprise**：当前活动 / 年均活动 —— 事件强度标准化。
- **M-D 冷启动 vs 总搅动差**：stable − total = 信念性 vs 流动性交易的分离。
- **M-E 时效量纲**：ts_arg_max —— 距活动峰值天数（GBR 结构级实证有效）。
- **M-F 活动波动率**：ts_std_dev —— 不确定性/事件密度。
- **M-G 非线性凸性**：signed_power² —— 极端事件加权（GBR：给 2Y 压 S）。
- **M-H 事件门控**：trade_when 只在高活动分位持仓。

模板库（探针波 w1，两批 16 条，算子数均 ≤7）：

| # | 结构 | 表达式骨架 | 来源 |
|---|---|---|---|
| T1 | 截面z+时序平滑 | ts_decay_linear(group_zscore(vec_avg(F),subind),20) | 论坛 41049370096663（EUR 同集冠军配方） |
| T2 | 截面z+时序平滑(sector) | 同上 sector 轴 | 论坛原版轴 |
| T3 | 自历史分位 | group_rank(ts_rank(vec_avg(F),66),subind) | 自建（ASI 新配方） |
| T4 | 时效量纲 | group_rank(ts_arg_max(vec_avg(F),66),subind) | GBR skill 结构级发现 |
| T5 | 原始信号中性化+平滑 | ts_decay_linear(group_neutralize(vec_avg(F),subind),10) | GBR skill「作用位置」发现 |
| T6 | 稳健形态 | group_zscore(winsorize(vec_avg(F),std=4),industry) | 论坛改进帖模板库 |
| T7 | 事件门控 | trade_when(ts_rank(vec_avg(F),66)>0.7, group_rank(...), -1) | GBR 放行形态 |
| T8 | 非线性凸性 | signed_power(group_zscore(vec_avg(F),sector),2) | GBR skill（2Y 杠杆） |
| T9 | 双窗 add | add(ts_mean(vec_avg(F),5), ts_mean(vec_avg(F),120)) | GBR 放行形态 |
| T10 | 活动surprise比率 | divide(vec_avg(F), ts_mean(vec_avg(F),252)) | GBR 放行形态 |
| T11 | 行业内相对差 | subtract(group_rank(stable,subind), group_rank(total,subind)) | GBR 放行形态（M-D） |
| T12 | 变化量纲 | group_rank(ts_delta(ts_mean(vec_avg(F),5),22),subind) | 自建 |
| T13 | 活动波动率 | group_rank(ts_std_dev(vec_avg(F),66),subind) | 论坛改进帖模板库引申 |

派发：w1-A = S2KXafbI4gZbFsiPXfA4oW（stable_boundary 中心，T1-T8）；w1-B = 49FhpW4Tn586bKMiZeYmF3t（total+组合，T9-T13+B2/B3）。

## 五、外部情报登记

- 论坛：【实战记录】信号灯系统 EUR fund_holdings_panel（post 41049370096663，22 赞）：赢家字段 stable_boundary_trade_count_21d，冠军配方 ts_decay_linear(group_zscore(vec_avg(F),sector),20)；holder_account_total 最差（GBR 无此字段）。
- 论坛：【实战分析】验证与改进（post 41049450679191，23 赞）：字段类型模板库——交易计数类 ts_decay_linear+group_zscore / 持仓价值类 ts_rank+rank / 集中度类 -rank+ts_mean；评论 JR57542：先截面 z 后时序平滑优于反序（USA 实证）。
- 论坛：【Alpha Idea】IND 机构持股广度新鲜度门（4335875566967，24 赞）：institutions6 计数字段做门控的思路（暂缓集参考）。
- 论文：台湾三大法人从眾行为（政大 2019 硕论）：从眾买进组合有正异常收益但规模调整后消失 —— 支持计数类信号做行业内相对化（subindustry 轴）而非纯水平。

## 六、探针实测结果（2026-11-08，31 条结构，GBR/TOP700/D1，SUBINDUSTRY · decay4 · trunc0.08）

设置与区域默认档一致（未换档 ⇒ 结果可比）。全部 alpha 均 `failed_ra_count` 3–5，无一条接近闸线。

### 6.1 第一波（T1–T13 模板，stable_boundary 与 boundary_total 双中心）

| ID | 结构 | 字段 | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| gJeVALAK | ts_decay_linear(group_zscore(F,sector),20) | stable_boundary | **0.94** | 0.31 | 0.40 | 1.44 |
| 9qxOvkY2 | ts_decay_linear(group_zscore(F,subindustry),20) | stable_boundary | 0.67 | 0.12 | 0.85 | 0.77 |
| npv5JrJa | group_rank(ts_rank(F,66),subind) | stable_boundary | −0.17 | −0.02 | 0.44 | −0.22 |
| mLoW3Q3W | group_rank(ts_arg_max(F,66),subind) | stable_boundary | −0.40 | −0.12 | 0.10 | −1.50 |
| 3qovbJrg | ts_decay_linear(group_neutralize(F,subind),10) | stable_boundary | 0.71 | 0.22 | 0.41 | 0.84 |
| MPYNWVRL | group_zscore(winsorize(F),industry) | stable_boundary | 0.84 | 0.17 | 0.85 | 0.99 |
| 78LRAlb2 | trade_when 事件门控 | stable_boundary | 0.67 | 0.22 | 0.23 | 1.31 |
| A1V8WEMd | signed_power(group_zscore(F,sector),2) | stable_boundary | 0.66 | 0.17 | 0.74 | 1.13 |
| Vkxb9zpG | add 双窗(5,120) | boundary_total | **1.03** | 0.26 | **0.82 ✗** | 0.85 |
| GrW5azoZ | group_rank(ts_rank(F,66),subind) | boundary_total | 0.77 | 0.35 | 0.23 | 1.38 |
| mLoW3789 | group_rank(ts_arg_max(F,66),subind) | boundary_total | −0.06 | 0.00 | 0.48 | 0.16 |
| RREw3zpa | divide(F, ts_mean(F,252)) | boundary_total | −0.23 | −0.05 | 0.10 | −0.52 |
| MPYNWzpz | subtract(rank stable, rank total) | 双字段 | −0.46 | −0.08 | 0.70 | −0.74 |
| wpQkmGRd | group_rank(ts_delta(ts_mean(F,5),22),subind) | boundary_total | 0.09 | 0.01 | 0.29 | 0.30 |
| zq3nMGm1 | group_rank(ts_std_dev(F,66),subind) | boundary_total | 0.92 | 0.22 | **0.75 ✗** | 1.37 |
| O0AXYzZb | group_rank(ts_std_dev? no: T1 sector) | boundary_total | 0.32 | 0.10 | 0.05 | 1.30 |

### 6.2 第二波（聚合口径 × 字段族，全部 sector 轴 + decay_linear 20）

| ID | 结构 | 字段 | S | F | TO | 2Y |
|---|---|---|---:|---:|---:|---:|
| 2rAozqjx | vec_sum | stable_boundary | 0.85 | 0.29 | 0.36 | 1.54 |
| zq3n6wrV | vec_max | stable_boundary | 0.87 | 0.29 | 0.36 | 1.53 |
| LLMYabMa | vec_avg | large_trade_count_50bps | 0.15 | 0.03 | 0.23 | 0.67 |
| E56PW06r | vec_avg | top_weighted_transaction_number | 0.06 | 0.01 | 0.15 | 0.55 |
| QPvpkrvG | vec_avg | herfindahl_index_transactions | 0.09 | 0.01 | 0.40 | −1.14 |
| 58Ed07E5 | stable/total 比率 | 双字段 | 0.47 | 0.08 | 0.61 | 1.41 |
| j2YKRlaE | vec_avg（平台 aC=0 处女字段） | top_weighted_transaction_number_active | 0.04 | 0.00 | 0.25 | 0.53 |
| omE05wav | vec_count | stable_boundary | −0.14 | −0.02 | 0.56 | 1.10 |

### 6.3 第三波（几何微调：轴 / 窗长）

| ID | 结构 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| rKRMgm39 | stable sector decay60 | 0.92 | 0.31 | 0.40 | 1.54 |
| YP1oKdK6 | stable industry decay20 | 0.94 | 0.25 | 0.58 | 1.29 |
| wpQkxVx6 | total sector decay20 | 0.80 | 0.26 | 0.38 | 1.39 |
| omE05e5l | large_trade sector decay60 | 0.21 | 0.05 | 0.20 | 0.72 |
| O0AXPvPJ | stable−total 行业内相对差 | −0.30 | −0.08 | 0.16 | −0.62 |
| MPYNRAoM | ts_delta22 stable sector | 0.55 | 0.12 | 0.46 | 0.06 |
| npv5RbMw | stable sector decay5 | 0.80 | 0.22 | 0.51 | 1.26 |

### 6.4 归因与结论

**① 字段级**：`stable_boundary_trade_count_21d` 是本集唯一有真实信号的字段（多结构重复出现 0.8–0.94）；`boundary_transaction_total` 次之（0.77–1.03，但高 S 那条 TO 0.82 挂 HIGH_TURNOVER）；金额类（USD/EUR value）与集中度类（HHI、分布分、conviction 计数）全部 S≈0 甚至负 —— **金额量纲在本区无信息，计数广度才有**。
**② 几何级**：`ts_decay_linear(group_zscore(F, sector), 20)` 是全族最优点（论坛 EUR 冠军配方在 GBR 同样最优，跨区可移植）；轴 `sector > industry > subindustry`（与外层中性化 SUBINDUSTRY 互补，sector 轴额外提供行业层信息）；decay 窗 20 ≈ 60 > 5。
**③ 聚合级**：vec_avg ≈ vec_max ≈ vec_sum（0.85–0.94），vec_count 无效 —— 说明信号在「有无/强弱」，不在账户分布形状。
**④ 天花板判定**：31 条结构（含 8 类聚合 × 8 个字段族 × 3 种分组轴 × 4 档窗长 × 事件门控 / 非线性 / 相对差 / 双窗）全部落在 **S ≤ 1.03（且该条 TO 挂闸），干净最优 0.94**；本地画像 17 条历史测试 S_best 1.26。**距 LOW_SHARPE 1.58 差 0.55+，距 F 1.0 差 0.69** ⇒ 判 `GBR-FUNDHOLDINGS-DEAD` 由 inferred 升级为 **payload 级实证**（31 条实测记录为本条目证据）。
**⑤ 例外留档**：`stable_boundary` + sector + decay 20 的组合 S 0.94 / 2Y 1.44 / TO 0.40 是全族最优残值，若将来本区换中性化档或换宇宙（TOP700→更大池）可作 re-probe 起点，不属当前可提交候选。
