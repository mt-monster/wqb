# EUR institutions6 · ATOM 专项挖掘与归因（2026-11-19）

> 用户指令：基于已有字段画像，先看 institutions6，再按三路证据（平台论坛 / 外部论文 / 模板库）组建 alpha 回测；回测结果做归因与 PnL 分析；针对缺口逐一覆盖破闸所需全部算子及边界用法，对近闸候选定向挖掘、不盲目扫参，记录每个候选表现与淘汰原因。
> 全程 EUR/D1；**未提交任何 alpha**；40 臂全部 COMPLETE，零失败，均经 `create_multi_simulation`（并发槽 2）。

## 1. 三路证据（先证后测）

### 1.1 平台论坛（MCP 确定性通道：`search_forum_posts_local`，扫描 1000 帖 / 命中 17）
| 帖 | 关键内容 | 对本役的作用 |
|---|---|---|
| 【Alpha Idea】乘法门控误杀→时空对偶协同（IND，`GrOXE7YP`） | **institutions6 同源配方**：`Buyer_Ratio = buyers/(buyers+sellers)`，`ts_zscore(·,252)` 慢变量；单腿 A（机构）**S1.11/F0.72/prod 0.7549**；乘法 `rank×rank` 必杀空头端，须改对称 z 加和；`group_neutralize(industry)` + `ts_decay_linear(3)` 压 TO 提 margin | 直接给出本题**唯一活内核**与目标量级（单腿 ~1.1）；EUR 实测 S1.08 与其高度吻合 |
| 因子构造日记·alpha 灵感（GBR） | `aggregate_share_count_institutions` 作分母归一；`(buyers−sellers)/holders` 作**门控**反而伤信号（S1.28→0.99）；「有多少家机构在买」≠「买了多少股」 | 预警：家数门控/家数不对称不是主信号；与第 1 波实测一致（家数不对称 S0.60/2Y−0.85） |
| Before You Submit: Five Stress Tests（71 赞） | 逐年拆解、单年亏损需解释 | 支撑本报告的逐年归因口径 |

### 1.2 外部论文（`tools/research/paper_search.py --diverse`：**20 篇 / 16 作者 / diverse_ok=true**）
核心锚：
- *Institutional Ownership and Return Predictability Across Economically Unrelated Stocks*（J. Financial Intermediation 2017，DOI 10.1016/j.jfi.2016.07.004）——机构持股变化对未来收益的横截面预测力；
- *Institutional Herding and Future Stock Returns*（2008，SSRN 1107523）——机构羊群强度预测收益；
- *Diversified but crowded: Evidence from 13F holdings*（Finance Research Letters 2026，DOI 10.1016/j.frl.2026.110885）——13F 拥挤度，与本役 prod 墙同向；
- *Return Predictability in Firms with Complex Ownership Network*（2020）、Pension Fund Herding（2011）、Taiwan herding（2013/2017）等。

### 1.3 模板库与边界算子（`tracking/EUR/reference/boundary_ops_eur.json`）
合法档：ts_zscore {22,66,252,504}｜ts_rank {22,66,252}｜winsorize 12 档 std｜signed_power 9 档｜ts_quantile {22,66}｜ts_mean 长窗须含 66｜ts_decay_linear {1..252}｜hump 9 档（须命名参数）｜tail 4 档｜分组轴 group_rank{subindustry,industry,sector,market}、group_neutralize{+country,exchange}。
禁：同数据集加权两腿相加（`equal_weight_leg_add`）、跨集价差（破 ATOM）。

## 2. 40 臂全表（五波 + 补测；S/F/2Y/TO 单位如上）

### 波 1 结构探针（10 臂，TOP2500/SUBINDUSTRY/decay4）
| # | 机制 | alpha | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| 1 | 家数不对称 (buyers−sellers)/holders·group_rank | P052v0Aw | 0.60 | 0.23 | **−0.85** | 5.4% |
| 2 | **买家比例 z252（论坛配方）** | Grmbkr7Q | **1.08** | 0.54 | **1.06** | 9.0% |
| 3 | 家数差 ts_delta63 | A1xNk12X | 0.12 | 0.02 | −0.13 | 9.4% |
| 4 | 市值净流÷持仓市值 z252 | RRebdRoj | 0.09 | 0.01 | 0.62 | 7.1% |
| 5 | 股数净流÷存量 z252 | LLKNkLw6 | 0.31 | 0.07 | 1.26 | 7.6% |
| 6 | 机构持股家数占比·group_rank | rK7OAKwo | −0.10 | −0.02 | 0.59 | 1.6% |
| 7 | 占比 ts_delta252 | Wjlb9jRO | 1.06 | **1.32** | 0.84 | 4.1% |
| 8 | 户均持仓规模 z252 | GrmbkrNZ | 0.75 | 0.43 | 0.56 | 4.9% |
| 9 | 股数净流 z252·group_rank | A1xNk18d | 0.24 | 0.04 | 0.35 | 7.1% |
| 10 | 零膨胀掩码 trade_when(·,-1) | VkNaOkbG | **−0.54** | −0.19 | −0.03 | 3.9% |

**归因**：唯一有方向且在 2Y 上 >1 的是**买家比例**；资金流族（市值/股数）全灭；家数不对称在 SUBINDUSTRY 下 2Y 为负（解释旧档「ATOM S0.16」的来源）；掩码毁交叉截面（S−0.54，与 SOP「trade_when 单边置 -1 破坏横截面排序」一致）。

### 波 2 定向破闸（8 臂，SUBINDUSTRY）
| # | 杠杆 | alpha | S | F | 2Y | TO | 判定 |
|---|---|---|---:|---:|---:|---:|---|
| 11 | 截面化后置 group_rank | gJabxarg | 1.01 | 0.46 | 1.13 | 9.1% | 无效 |
| 12 | signed_power 1.4 | kqaoQavd | 1.03 | 0.51 | 0.96 | 10.3% | 无效 |
| 13 | signed_power 2 | omaLVaRn | 0.88 | 0.42 | 0.69 | 12.8% | 恶化 |
| 14 | winsorize 0.3（前置） | RRebde9z | 0.93 | 0.41 | 1.07 | 10.4% | 无效 |
| 15 | **ts_decay_linear 3（论坛平滑）** | 3q0Xz01N | **1.07** | **0.53** | 1.10 | 8.1% | 小幅有效 |
| 16 | 换读数：买家÷holders | YPabQaEw | 0.99 | 0.44 | 0.98 | 10.0% | 同族等效 |
| 17 | **买方对称对照：卖家÷holders** | 78YNJYvZ | **−0.85** | — | −0.96 | 7.9% | **对称翻转 ⇒ 真因子** |
| 18 | ts_quantile 66 | O0WNoWMg | 0.89 | 0.32 | 0.74 | 16.3% | 无效 |

### 波 3 设置轴（6 臂）
| # | 设置 | alpha | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| 19 | decay_linear3 @ **INDUSTRY** | N1PaOMgL | **1.18** | **0.66** | **1.18** | 7.7% |
| 20 | group_rank @ INDUSTRY | zqd8Wa5K | 1.02 | 0.46 | 1.14 | 9.1% |
| 21 | decay_linear3 @ INDUSTRY/decay6 | 2r5wKmOY | 1.17 | 0.65 | 1.20 | 7.0% |
| 22 | base @ INDUSTRY/decay6 | 9qljRWjK | 1.18 | 0.66 | 1.18 | 7.5% |
| 23 | decay_linear3 @ CS1600 | kqaoK8m8 | 1.06 | 0.59 | 0.94 | 7.8% |
| 24 | base @ CS1600 | xAv3nlmg | 1.07 | 0.60 | 0.90 | 8.7% |

**归因**：**中性化 INDUSTRY ≫ SUBINDUSTRY**（S 1.07→1.18、F 0.53→0.66）；**TOP2500 ≫ TOPCS1600**（S 1.18 vs 1.06、2Y 1.18 vs 0.94）；**decay 4≈6**（无增益）。

### 波 4 边界算子档穷举（10 臂，INDUSTRY）
| # | 档 | alpha | S | F | 2Y | TO | 判定 |
|---|---|---|---:|---:|---:|---:|---|
| 25 | ts_zscore **504** | 2r5w7Zzb | 0.98 | 0.51 | 1.05 | 7.2% | 长窗劣于 252 |
| 26 | ts_mean 66（裸均值） | 9qljw61d | 0.18 | 0.04 | −1.53 | 2.2% | 裸均值毁信号 |
| 27 | **winsorize 0.35（后置）** | Jj8NpXZE | **1.25** | 0.65 | 1.22 | 7.1% | **S 波段最佳** |
| 28 | signed_power 1.8 | 2r5w7ZbJ | 1.08 | 0.61 | 0.95 | 11.5% | 无效 |
| 29 | signed_power 3 | RRebpane | 0.80 | 0.37 | 0.52 | 17.6% | 恶化 |
| 30 | ts_quantile 22 | 0mPX7Qvq | 0.66 | 0.17 | 1.14 | 24.6% | 无效 |
| 31 | hump=0.01 | blabLPEN | 0.59 | 0.22 | **2.20** | **0.89%** | TO 破 5% 下限，不可用 |
| 32 | **group_neutralize country** | O0WNpmaR | 1.24 | **0.68** | **1.36** | 8.7% | **2Y 波段最佳** |
| 33 | ts_rank 252 | 9qljw6Qq | 1.20 | 0.66 | 1.18 | 8.4% | 与 zscore 等效（SOP #51） |
| 34 | tail lower=0.1 | P052plEq | 1.18 | 0.67 | 1.12 | 9.7% | 持平（未毁腿） |

### 波 5 有效杠杆组合（4 臂，INDUSTRY）
| # | 组合 | alpha | S | F | 2Y | TO |
|---|---|---|---:|---:|---:|---:|
| 35 | **winsorize 0.35 + country** | **GrmbwmmO** | **1.32** | **0.67** | **1.48** | 7.3% |
| 36 | winsorize 0.35 + decay_linear3 | d5abxa9w | 1.25 | 0.65 | 1.24 | 6.3% |
| 37 | winsorize 0.35 + market | KPgNbgVE | 1.25 | 0.65 | 1.22 | 7.1% |
| 38 | decay_linear3 + country | pwaR6aW3 | 1.23 | 0.67 | 1.41 | 7.8% |

### 波 6 补测（2 臂）
| # | 档 | alpha | S | F | 2Y | TO | 判定 |
|---|---|---|---:|---:|---:|---:|---|
| 39 | ts_rank 66（第二档补齐） | d5ab0l1K | 0.99 | 0.43 | 0.88 | 13.6% | 劣于 252 |
| 40 | ts_mean(5) 前置平滑（持仓集合改变型） | xAv3kmbJ | 1.21 | 0.65 | 1.45 | 6.8% | 略劣于不平滑 |

## 3. 归因与 PnL 分析（最优件 GrmbwmmO）

### 3.1 缺口分解（对照用户硬闸：S>1.58 / F>1.0 / 2Y≥1.58 / sub≥0.52·S / prod<0.7）
| 闸 | 实测 | 缺口 | 性质 |
|---|---:|---:|---|
| S | **1.32** | −0.26 | 信号强度不足（40 臂天花板） |
| F | **0.67** | −0.33 | **结构性**：F=S·√(ret/max(TO,0.125))；当前 ret 3.26%、TO 7.3% ⇒ F=1.32×√(0.0326/0.125)=0.67。若 S=1.58 需 ret≥5.0% 才到 F=1.0，而本族 ret 天花板 ~3.3–4.0% |
| 2Y | **1.48** | −0.10 | 最接近，靠 country 轴从 1.18 抬到 1.48 |
| sub | 1.00 | 过（限 0.52×1.32=0.69） | ✅ |
| TO | 7.3% | 过 | ✅ |
| prod | **0.8257** | −0.13 | 中度拥挤（直方图 [0.7,0.8] 仅 8 颗 / [0.8,0.9] 1 颗），非密墙 |

### 3.2 逐年拆解（N1PaOMgL，S1.18 代表件；GrmbwmmO 同族结构）
| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S | 1.39 | 0.49 | **0.02** | 1.05 | 1.38 | 1.53 | 1.49 | **2.85** | 1.64 | **0.57** |
| pnl（万） | 36.7 | 15.6 | 0.8 | 23.4 | 30.8 | 38.7 | 76.1 | 83.1 | 79.0 | 17.2 |
| 持仓 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

- **十年满仓**（longCount/shortCount 全 >0、pnl 全正）⇒ 满足近十年（含放宽后的九年口径）。
- 信号 2017–2022 稳定（S1.05–2.85），**2016 空窗（0.02）、2023 衰减（0.57）**——2Y 缺口（1.48）主要来自 2023。
- PnL 单调复利型，无尖峰依赖；DD 3.3–4.2%（低波动慢信号）。

### 3.3 为什么 S 到不了 1.58（40 臂证据）
1. **算子家族已穷举**：截面族（group_rank/neutralize×4 轴）、时序族（ts_rank/zscore/quantile/mean/decay_linear）、非线性（signed_power 1.4/1.8/2/3、tail、hump）、掩码族——**无一突破 1.32**。S 随幂次单调下降（1.4→0.88、2→0.88、3→0.80），最好的形态恰是最朴素的 winsorize+z+country。
2. **设置轴已闭合**：INDUSTRY 最优（SUBINDUSTRY −0.10、CS1600 −0.12、decay 无增益）。
3. **论坛独立证据一致**：同字段同构造在 IND 单腿 S1.11——跨区都指向「该读数单集天花板 ≈1.1–1.3」。
4. **P 值意义**：这不是「没调好」，而是**信息源强度上限**——买家比例是低波动慢变量（TO 7%），ret 天花板 3.3%，F 的数学约束使其在 S<1.58 时永远过不了 F>1.0。

## 4. 淘汰原因全表（按族）

| 族 | 代表臂 | 最好读数 | 淘汰原因 |
|---|---|---|---|
| 家数不对称 (buyers−sellers)/holders | P052v0Aw / Grmbkr7Q 变体 | S0.60 / 2Y−0.85 | SUBINDUSTRY 下 2Y 为负；仅作小腿（已用于 N1NGbddg） |
| 资金流（市值/股数净额） | RRebdRoj / LLKNkLw6 | S0.31 | 无横截面信号（流量被规模主导） |
| 存量占比/户均规模 | rK7OAKwo / GrmbkrNZ | S−0.10 / 0.75 | 水平量无预测力；2Y<1 |
| 家数变化 ts_delta | A1xNk12X | S0.12 | 差分放大披露噪声 |
| 零膨胀掩码 trade_when | VkNaOkbG | S−0.54 | 未触发置 -1 破坏横截面排序 |
| 买家比例（唯一活内核） | GrmbwmmO | **S1.32/F0.67/2Y1.48** | S/F 上限 + prod 0.826 —— **限投档，非死** |
| 非线性/幂次族 | signed_power 3 / ts_quantile | ≤1.08 | 单调恶化（信号头部不集中） |
| hump | blabLPEN | S0.59/TO0.89% | TO 跌破内部 5% 下限 |

## 5. 近闸 prod 早查：执行与流程固化

- 按用户新指令，对近闸最优件 GrmbwmmO（S1.32/2Y1.48，缺口 ≤0.26）执行早查：**prod = 0.8257** ⇒ 按三档决策归「**限投**」（只许持仓集合改变型杠杆；本波补测的 ts_mean(5) 即为该档尝试，S1.21 未改善）。
- 流程已固化：`docs/experience/01_platform_gates.md` **§16.3 近闸即查 prod**（触发条件 S≥1.38 ∧ F≥0.8 ∧ 2Y≥1.38 ∧ sub/S≥0.52；只查族代表；三档决策 ≥0.85 停族 / 0.70–0.85 限投 / <0.70 放行；prod 会漂移交付前 refresh 终验）。
- 与既有 `prod_first_skeleton_v1` 兼容：那条管 S 弱时早筛，本条管近闸时必查。

## 6. 判定

- **institutions6 ATOM 最佳读数修正**：旧记录「ATOM S0.16」来自家数不对称变体；本役 40 臂把真实上限抬到 **S1.32/F0.67/2Y1.48/sub1.00/TO7.3%（GrmbwmmO，纯 ATOM，pyramid=INSTITUTIONS）**。
- **仍不可交付**：S/F 双缺口（F 受数学约束不可与 S 分离）+ prod 0.8257。**PROVISIONAL / 族级**（不判数据集死：prod 会漂移；买家比例族的 2Y 已 1.48，若平台出现更强的机构读数或产线池漂移，可复用本报告的 GrmbwmmO 作为起点）。
- **投入建议**：按 prod 三档 = 限投；下一步只值得等 prod 池漂移后复测，或换 institutions 类别新数据集（当前该类别仅 2 集，均已挖尽）。

## 7. 产物

- 画像：`tracking/EUR/reference/profiles/eur_institutions_institutions6_profile_20261118.md`（11/11 PASS）
- 本报告：`output_report/EUR_institutions6_atom_campaign_20261119.md`
- 论文检索原始：`logs/_tmp_papers_institutions6.json`（20 篇 / 16 作者）
- 流程固化：`docs/experience/01_platform_gates.md` §16.3
- 臂数：**40 臂（6 波）全 COMPLETE，0 失败；未提交任何 alpha**

## 8. ★ 复跑验证（2026-11-19 用户指令「重新再跑一遍上一波的数据集回测」）

按原设置档分 6 批重跑全部 40 臂（同表达式 + 同设置）：

| 批 | 内容 | 新 alpha id | 读数对照 |
|---|---|---|---|
| A | 波4 边界档 10 臂 @INDUSTRY/decay4 | 全新 id（O0WNGaQv…P052G9Nx） | **10/10 逐位一致**（S/F/2Y/TO 完全相同） |
| B | 波5 组合 4 + 波6 补测 2 + 设置轴 INDUSTRY 2 | 6 条**被平台去重**（原 id）；2 条新 id | **8/8 一致**（QP0bGmXK=1.18/0.66/1.18 ↔ N1PaOMgL；0mPXpnWv=1.02/0.46/1.14 ↔ zqd8Wa5K） |
| C | 波1 结构探针 10 臂 @SUBINDUSTRY/decay4 | 全新 id | **10/10 一致** |
| D | 波2 定向破闸 8 臂 @SUBINDUSTRY/decay4 | 全新 id | **8/8 一致** |
| E | 设置轴 decay6 2 臂 | 批返回 0 子任务（去重） | 原 id `2r5wKmOY` 1.17/0.65/1.20、`9qljRWjK` 1.18/0.66/1.18 **不变** |
| F | 设置轴 CS1600 2 臂 | 新 id | **2/2 一致**（1.06/0.59/0.94；1.07/0.60/0.90） |

**结论**：40/40 臂读数完全可复现（同表达式 + 同设置 ⇒ 同 S/F/2Y/TO），EUR institutions6 结论稳定。

**工程观察（新）**：平台去重行为**不一致**——同一批重跑中，有的返回原 alpha id（B 批 6 条），有的生成新 id（A/C/D/F 批全部），还有的批直接返回 0 子任务（E 批）。⇒ **不能靠「有没有新 id」判断是否真跑了**；复跑判据只能是「读数逐位对照」。

## 9. ★★ 全量设置网格（用户 2026-11-19 指令「宇宙和中性化要全测」）

**网格**：EUR 全部 **5 宇宙** × 全部 **12 中性化** = 60 组合；每格 2 个表达式（winsorize0.35 内核 + 原核），其余设置固定（decay4 / trunc0.08 / nanON / maxTradeOFF / TOP 系列）。59/60 已产出；TOP400×SLOW 排队长未产出（属最弱宇宙 × 风险线，不影响结论）。

### 9.1 档位性质判定（先定哪档可作交付依据）

`get_alpha_details` 签名：**标准档**（NONE/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/COUNTRY）均报告 `risk_neutralized_sharpe`（同一信号恒为 **1.02**）；**风险中性化线**（STATISTICAL / FAST / SLOW / SLOW_AND_FAST / CROWDING / REVERSION_AND_MOMENTUM）**不报告该字段**——主 S 即风险中性化 PnL。
⇒ 交付依据只认标准档；风险线读数仅记录（与 SOP「STATISTICAL/SLOW_AND_FAST 是另一把尺子」同源）。

### 9.2 标准档 S 矩阵（winsorize / plain）

| 宇宙 | NONE | MARKET | SECTOR | INDUSTRY | SUBINDUSTRY | COUNTRY |
|---|---|---|---|---|---|---|
| TOP2500 | −0.13 / 0.24 | 1.08 / 1.06 | 1.16 / 1.13 | **1.25 / 1.18** | 1.18 / 1.08 | 1.12 / 1.09 |
| TOPCS1600 | −0.06 / 0.32 | 1.19 / 1.08 | 1.25 / 1.12 | 1.06 / 1.07 | 1.05 / 0.90 | **1.26 / 1.16** |
| TOP1200 | −0.14 / 0.17 | 0.81 / 0.80 | 0.90 / 0.87 | 0.96 / 0.91 | 0.76 / 0.70 | 0.84 / 0.81 |
| TOP800 | −0.06 / 0.21 | 0.66 / 0.70 | 0.72 / 0.75 | 0.79 / 0.77 | 0.61 / 0.59 | 0.65 / 0.65 |
| TOP400 | 0.02 / 0.23 | 0.56 / 0.53 | 0.63 / 0.57 | 0.55 / 0.47 | 0.32 / 0.30 | 0.51 / 0.45 |

### 9.3 风险中性化线 S 矩阵（仅记录，不作交付依据）

| 宇宙 | CROWDING | FAST | SLOW | STATISTICAL | SLOW_AND_FAST | REVERSION_AND_MOMENTUM |
|---|---|---|---|---|---|---|
| TOP2500 | 1.02 / 0.99 | **1.72 / 1.62** | 1.18 / 1.06 | 1.37 / 1.30 | 1.18 / 1.06 | 1.29 / 1.22 |
| TOPCS1600 | 1.01 / 0.85 | 1.63 / 1.38 | 1.03 / 0.74 | 1.07 / 0.92 | 0.98 / 0.70 | 1.17 / 0.98 |
| TOP1200 | 0.91 / 0.87 | 1.33 / 1.18 | 1.03 / 0.83 | 1.20 / 1.08 | 0.96 / 0.75 | 1.11 / 1.04 |
| TOP800 | 0.82 / 0.85 | 1.12 / 1.01 | 0.90 / 0.76 | 0.88 / 0.80 | 0.84 / 0.68 | 1.04 / 1.03 |
| TOP400 | 0.73 / 0.66 | 0.82 / 0.69 | 待补 | 0.57 / 0.51 | 0.53 / 0.42 | 1.05 / 0.97 |

### 9.4 网格结论（四条）

1. **标准档全域最优 = TOPCS1600 × COUNTRY：S1.26 / F0.76 / 2Y1.55**（2Y 仅差 0.03，S 差 0.32，F 差 0.24）；第二 TOPCS1600×SECTOR（1.25/0.74/1.26）、第三 TOP2500×INDUSTRY（1.25/0.65/1.22）。
2. **宇宙形状**：TOP2500 ≈ TOPCS1600 ≫ TOP1200 ≫ TOP800 ≫ TOP400（标准档 S 从 1.26 单调降到 0.63）⇒ 该信号住大中盘，小宇宙结构性不足（与 pv47 相反）。
3. **中性化形状**：标准档内 MARKET/SECTOR/INDUSTRY/COUNTRY 四档同档（S 1.05–1.26），**NONE 全宇宙崩**（−0.14~0.32，DD 最高 93–104%）⇒ 该信号必须做行业/市场相对化；风险线 FAST/STATISTICAL 抬高 S（1.72/1.37）但属另一把尺子且 F 仍 <1.0（FAST 0.90）。
4. **无任何标准档组合过闸**：S 天花板 1.26 < 1.58、F 天花板 0.76 < 1.0、2Y 天花板 1.55 < 1.58 ⇒ 全网格复核后「institutions6 ATOM 不可交付」结论**不变且更强**（60 格全量覆盖，非抽样）。

## 10. 设置轴两段式（2026-11-19 用户裁定「EUR 独有」→ 落 EUR skill）

用户追问「跑全部宇宙和中性化能否对近闸候选破闸、有没有必要」。评估结论：**对低波动慢信号族不能破闸**（组合叠加仅 +0.00~0.07 S；F=S·√(ret/max(TO,0.125)) 把 F 锁在 S 上，本族 F≥1 需 S≥1.66–1.85），且全网格 120 次仿真/候选、并发上限 7、排队 15min ⇒ **默认不全跑**。

纪律已成文：**`Claude/skills/wq-brain-ra-eur/rules/settings-axis-two-stage.md`**（EUR 独有，非 docs/experience 通用层），要点：
- 标准档 6（NONE/MARKET/SECTOR/INDUSTRY/SUBINDUSTRY/COUNTRY，有 `risk_neutralized_sharpe`）/ 风险线 6（其余，另一把尺子）；
- 第一段 5 宇宙 × {INDUSTRY, COUNTRY} = 10 格；仅当最优格距 S 与 F 各 ≤0.10 才展开 5×6=30 格；风险线仅交付确认时 1 列；
- 工程备注：表达式内 `group_neutralize` + 设置 `NONE` → ERROR；平台去重不一致，复跑只认读数逐位对照。

已 `sync_skills` 到 5 个安装位（`--check` 全 OK），守护测试 149 passed。

### 10.1 近闸候选（country 组合内核）第一段全表（5 宇宙 × {INDUSTRY, COUNTRY}）

表达式：`group_neutralize(winsorize(ts_zscore(buyers/(buyers+sellers),252), std=0.35), <axis>)`，decay4/trunc0.08/nanON/maxTradeOFF。

| 宇宙 | INDUSTRY 设置（S/F/2Y） | COUNTRY 设置（S/F/2Y） |
|---|---|---|
| TOP2500 | 1.32 / 0.67 / 1.48 | 1.12 / 0.61 / 1.37 |
| **TOPCS1600** | **1.35 / 0.75 / 1.61** ← 最优 | 1.26 / 0.76 / 1.55 |
| TOP1200 | 1.06 / 0.53 / 1.43 | 0.84 / 0.45 / 1.16 |
| TOP800 | 0.83 / 0.40 / 0.84 | 0.65 / 0.33 / 0.60 |
| TOP400 | 0.54 / 0.22 / 0.84 | 0.51 / 0.24 / 0.82 |

**判定（按两段式规则）**：第一段最优 = CS1600×INDUSTRY（S1.35/F0.75/**2Y1.61 首次过 2Y 闸**），距 S 闸 0.23、F 闸 0.25，均 >0.10 ⇒ **不展开第二段**（剩余 ~18 格不跑）。
**新发现**：组合增益在 CS1600 最大（基础内核 1.06 → 组合 1.35，**+0.29**；TOP2500 仅 +0.07）⇒ 双重中性化（表达式内 country + 设置 INDUSTRY）在跨国宇宙价值最高。
**结论不变**：institutions6 ATOM 最佳标准档读数抬到 S1.35/F0.75/2Y1.61，仍双闸不足 ⇒ PROVISIONAL。

### 10.2 双重中性化线索验证（cartesian 组合分组）

论坛 [BRAIN TIPS] 推荐用 `densify(group_cartesian_product(industry, country))` 做双重中性化（避免顺序中性化互相抵消）。在 CS1600 实测：

| 表达式内分组 | 设置 | S | F | 2Y |
|---|---|---:|---:|---:|
| `country`（顺序式，当前最优） | INDUSTRY | **1.35** | **0.75** | **1.61** |
| `densify(group_cartesian_product(industry, country))` | INDUSTRY | 1.22 | 0.64 | 1.51 |

⇒ **cartesian 组合分组劣于顺序式 country 中性化**（−0.13 S / −0.11 F / −0.10 2Y）。可能原因：industry×country 在 CS1600 上切出过多小组（论坛同帖警告的 group-size 问题）。**该线索否证，不再投入**。

**近闸候选网格最终状态**：第一段 10 格 + cartesian 2 格 = 12 格（6 批/12 次仿真），对照全网格 60 格/120 次，两段式省 ~80%。最优仍为 **CS1600×INDUSTRY（country 组合）S1.35/F0.75/2Y1.61**；S/F 双缺口 >0.10 ⇒ 按规则停止，不展开第二段。

### 10.3 指标手册在 institutions6 上的实践（2026-11-20）

用户指令：「这套在 institutions6 上实践了没」+「实践大于约束，有确定实践可考虑放开 ATOM」。已补两项实践：

**A. ATOM 内窗口换档（2Y↔S 交换路径）**，CS1600×INDUSTRY：

| 窗口/读数 | S | F | 2Y |
|---|---:|---:|---:|
| **ts_zscore 252（基线）** | **1.35** | **0.75** | **1.61** |
| ts_zscore 66 | 1.03 | 0.45 | 0.92 |
| ts_zscore 504 | 0.95 | 0.45 | 1.38 |
| ts_rank 66 | 1.01 | 0.44 | 1.06 |
| ts_rank 22 | 0.70 | 0.19 | 1.24 |

⇒ **252 是甜点；短窗同时伤 S 与 2Y**（13F 慢变量，短窗只加噪）。「2Y 换 S」的窗口路径在本族**不成立**。

**B. 破 ATOM 的流动性残差（手册头号 S 杠杆）**，显式引入 PV 内置字段：

| 表达式 | S | F | 2Y | 判定 |
|---|---:|---:|---:|---|
| `vector_neut(signal, rank(ts_mean(volume*close,20)))` | 1.22 | 0.71 | 1.28 | ❌ 劣于对照 |
| 上 + `group_neutralize(..., country)` | 1.22 | 0.67 | 1.57 | ❌ |
| `ts_regression(signal, rank(liquidity), 252, rettype=0)` | 0.74 | 0.30 | 0.32 | ❌ 严重劣化 |
| **ATOM 对照（group_neutralize country）** | **1.35** | **0.75** | **1.61** | — |

**为什么无效（可预测的）**：论坛该案例的前提是 `risk_neutralized_sharpe ≫ S`（信号被风险暴露拖累，S 0.99 vs RN 1.38）。本信号 **RN=1.02 < S=1.35**，没有可剥离的风险拖累 ⇒ 残差化只加噪。
⇒ **新增前置判据：做流动性残差前先读 `risk_neutralized_sharpe`；RN ≲ S 时不要做**（直接跳过，不必烧配额）。

**工程坑**：`sqrt(volume*close)` 被 `unitHandling=VERIFY` 拒绝（`Unit[TSPrice:2,TSShare:1]` 不能开方）⇒ 流动性代理必须无量纲化（`rank(ts_mean(volume*close,20))`）。

**结论**：指标手册在 institutions6 上**已实践**；两项实践均为负结果，且各自的失败原因可解释（慢变量窗口无甜点区；RN<S 无风险拖累可剥）。**放开 ATOM 未带来增益，本候选仍不可交付**（S1.35 天花板、F 需 S≥1.82）。
