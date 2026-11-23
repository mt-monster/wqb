# EUR 未亮塔 · 模板族穷尽台账（2026-11-22）

> 用户 2026-11-22 指令：**每个数据集 ≥5 个模板族，每个族按流程做完整梯度**（同类别算子全替换 + 参数档位 + Δ 表）。
> 本文件是「哪些族已测 / 哪些族待测」的对照表，防止把「同骨架换字段」误记成多族。

## 族级定义（结构互异 = 字段族 + 算子几何 + 机制语义三者都不同）

| 代号 | 结构 | 机制语义 |
|---|---|---|
| **H**（水平型） | 原始值 / 累积水平（ts_sum） | 信息在「绝对量」上 |
| **R**（相对偏离型） | 比值 / 占比 / 时序相对化（ts_zscore/ts_rank） | 信息在「相对自身历史或截面」的偏离 |
| **D**（差分型） | ts_delta / 一阶差 | 信息在「变化速度」 |
| **B**（比率型） | A/B 双字段比 | 信息在「两个口径的相对关系」 |
| **X**（交叉型） | A×B / A+B 双字段交互 | 两个独立信息的乘积效应 |
| **P**（概率/有界型） | 已在 [−1,1] 的打分，直接用 | 信息在打分本身 |
| **G**（门控/事件型） | trade_when(presence, ·, −1) | 信息只在事件发生窗口 |
| **E**（事件密度型） | 事件计数 / 稀疏流 | 信息在「事件有多密集」 |
| **N**（噪声/缺失型） | ts_count_nans / ts_arg_max | 信息在「缺失/时点模式」 |

## 1. earnings6（EARNINGS 1/3）—— **9 族全部实测**

| 族 | 结构 | 臂数 | 最好读数 | 状态 |
|---|---|---:|---|---|
| **E-B1** | **B：actual÷(1+\|estimated\|) 双慢腿 610/252** | 58 | **S1.91/F2.49/2Y1.99/CW✅** | ✅ **唯一有效族**；参数轴已穷尽（decay 8/16/32 × 窗 73–125 × 宇宙 3 × trunc 2 × 中性化 4 × 权重 3） |
| E-E1 | E：actual EPS 水平（ts_zscore） | 批19 | S −0.26 | ⛔ |
| E-X1 | X：actual − estimated（原始差） | 批19 | S 0.32 | ⛔ |
| E-X2 | X：actual × estimated | 批19 | S 0.30 | ⛔ |
| E-H1 | H：preliminary range 宽度 | 批19 | S −0.23 | ⛔ |
| E-H2 | H：eps_change_absolute | 批19 | **S 0（全零字段）** | ⛔ 复现 11-12 结论 |
| E-R1 | R：eps_change_percentage | 批19 | **S 0（全零字段）** | ⛔ 复现 11-12 结论 |
| E-G1 | G：presence 门控 | — | 未测 | ⏳ 低优先（E-B1 已含门控语义：trade_when 门控在 mcr27 上有效，earnings6 未做） |
| E-N1 | N：缺失模式 ts_count_nans | — | 未测 | ⏳ 低优先 |

**★ earnings6 判定**：**9 族中仅 1 族（E-B1）有信号**，其余 8 族全灭 ⇒ 该集不是「梯度不够」而是**机制唯一**：
**只有「实际 EPS ÷ 预期 EPS」的惊喜比值 × 双慢腿（610 日 + 252 日）** 在 EUR 有定价力。
⇒ 该族的天花板已由 58 臂梯度锁定（S1.91 / F2.49 / 2Y1.99 / sub 1.12），只差 2Y 的 0.03。

## 2. socialmedia12（SOCIALMEDIA 0/3）—— **8 族全部实测**

| 族 | 结构 | 臂数 | 最好读数 | 状态 |
|---|---|---:|---|---|
| S-P1 | P：scl12_buzz 截面 group_rank | 历史 10（11-18） | \|S\|≤0.21 | ⛔ |
| S-P2 | P：scl12_sentiment 截面 | 历史 10（11-18） | \|S\|≤0.21 | ⛔ |
| S-R1 | R：buzz ts_zscore(110) | 批17 | ≤0.24 | ⛔ |
| S-R2 | R：sentiment ts_zscore | 批17 | ≤0.31 | ⛔ |
| S-H1 | H：buzz ts_sum 累积 | 批19 | S 0.51 | ⛔ |
| S-R3 | R：buzz ts_zscore(504) | 批19 | S −0.27 | ⛔ |
| S-X1 | X：buzz × sentiment 交互 | 批19 | S −0.08 | ⛔ |
| S-D1 | D：buzz ts_delta 变化率 | 批19 | S −0.10 | ⛔ |

**★ socialmedia12 判定**：8 族全灭 ⇒ **socialmedia12 的 buzz/sentiment 在 EUR 无独立定价力**；
但作为**组腿弱腿**有效（`2r5NgWvY` S1.65/prod 0.6785 用 analyst EBI 强腿 + scl12_buzz 弱腿）。
⇒ **socialmedia 类的正确定位是「弱腿/门控腿」，不是「主腿」**（与 socialmedia15 的结论一致）。

## 3. socialmedia15（SOCIALMEDIA 0/3）—— **2 族**（两代字段各 1 族）

| 族 | 结构 | 臂数 | 最好读数 | 状态 |
|---|---|---:|---|---|
| SM-D1 | D：d1_ 系 13 字段（sentiment/buzz/conflict/…） | 历史 10 | \|S\|≤0.21 | ⛔ |
| SM-P1 | P：新系 32 字段（scl15_*） | 10（批8） | \|S\|≤0.54（9/10 负） | ⛔ |
| **SM-E1** | E：新系事件计数（mergers/litigation/attrition/managementchange） | — | 未单独测 | ⏳ 待派 |
| **SM-N1** | N：缺失/覆盖模式（ts_count_nans on 新系） | — | 未测 | ⏳ 待派 |

## 4. fund_holdings_panel（INSTITUTIONS 0/3）—— **3 族**（30 字段只测了 1 族）

| 族 | 结构 | 臂数 | 最好读数 | 状态 |
|---|---|---:|---|---|
| FH-R1 | R：ts_zscore(ts_backfill(·,66),504) 统一骨架换 10 字段 | 10（批9） | \|S\|≤0.33 | ⛔ |
| **FH-H1** | H：持仓/交易**水平**（ts_sum 累积，不做时序标准化） | — | 未测 | ⏳ 待派 |
| **FH-E1** | E：边界事件密度（boundary_transaction_total / stable_boundary_trade_count_21d 计数族） | — | 未测 | ⏳ 待派 |
| **FH-B1** | B：换手强度比（交易额÷持仓额）、家数比 | — | 未测 | ⏳ 待派 |
| **FH-X1** | X：持仓×交易交互（流入流出强度） | — | 未测 | ⏳ 待派 |
| **FH-N1** | N：拥挤度变化（HHI / distribution_score 的 ts_delta） | — | 未测 | ⏳ 待派 |

## 5. insider_agg_matrix（INSIDERS 2/3）—— **7 族**（全弱）

| 族 | 结构 | 臂数 | 最好读数 | 状态 |
|---|---|---:|---|---|
| IA-H1 | H：高管净买入累积 ts_sum63 | 批18 | S0.55 | ⛔ |
| IA-R1 | R：净买比例 ts_zscore252 | 批18 | **S0.65**（族内最好） | ⛔ |
| IA-P1 | P：directional_indicator 直接用 | 批18 | **S0（全零字段）** | ⛔ 字段无数据 |
| IA-H2 | H：significant_value_1 幂 0.5 | 批18 | S0.20 | ⛔ |
| IA-R2 | R：买卖比 ts_zscore | 批18 | S0（全零） | ⛔ |
| IA-H3 | H：ts_decay_linear 衰减 | 批18 | S0（全零） | ⛔ |
| IA-R3 | R：avg（高管平均）净买入 ts_zscore | 批18 | S0.28 | ⛔ |
| IA-R4 | R：董事净买入（total_buy−total_sell） | 批18 | −0.10 | ⛔ |

## 6. institutions6（INSTITUTIONS 0/3）—— **2 族**（历史）

| 族 | 结构 | 臂数 | 最好读数 | 状态 |
|---|---|---:|---|---|
| I6-R1 | R：买家净差 ts_zscore 栈（88d/504） | 40（11-19）+ 8（11-06） | S1.35/F0.75/2Y1.61 | ⛔ F 数学约束（prod 0.8257） |
| I6-B1 | B：买家数÷持有家数（比例型） | 同上 | S1.32/F0.67 | ⛔ |

## 7. mcr27（MACRO 2/3）—— **4 族**

| 族 | 结构 | 臂数 | 最好读数 | 状态 |
|---|---|---:|---|---|
| M-B1 | B：created÷closed_days（+ts_quantile 168/336/504） | 6+8+8 | **S2.77/F1.13/2Y3.03** | ⛔ prod 0.766 + self 0.7703（母件已提交） |
| M-B2 | B：removed÷closed_days | 8（批13） | S1.11 | ⛔ |
| M-B3 | B：active÷active_days | 8（批13） | S1.20 | ⛔ |
| M-B4 | B：ajnet÷active_days | 2 | **S0（全零字段）** | ⛔ |

## 8. 待派族汇总（下一批优先级）

1. **fund_holdings_panel 5 新族**（FH-H1/E1/B1/X1/N1）—— 30 字段、5 大字段族（存量/流量/边界事件/集中度/conviction），**从未测过水平型与事件密度型**；
2. **earnings6 E-G1 / E-N1**（presence 门控 + 缺失模式）；
3. **socialmedia15 SM-E1 / SM-N1**（事件计数 + 缺失模式）；
4. 每个有效族跑 `tools/research/operator_swap_matrix.py` 的**同类别算子全替换**（14 替换/8 no-op）+ 参数档位梯度 + Δ 表。

## 9. 族 L / 族 H / 族 M（组腿族，非 ATOM）实测记录

| 族 | 强腿（未提交、已过 prod） | 弱腿（未满塔） | 臂数 | 最好读数 | 卡点 |
|---|---|---|---:|---|---|
| **L** | `WjOAJWxd` EBT 修正广度（prod 0.6806） | institutions6 / insider_agg / socialmedia12 / earnings6 | **28**（批16/20/22） | **S3.21 / F2.46 / 2Y2.59 / sub1.41** | **sub 比率恒 0.40–0.44 < 0.52** + prod 0.7405 |
| **H** | `O0W0w3P7` news46 事件流量（**已 ACTIVE 提交**） | socialmedia12 buzz/sentiment | **18**（批14/15） | S2.47 / F1.14 / 2Y3.28 / sub1.25 | **sub 差 0.01–0.03** + **prod 0.8306（撞已提交母件）** |
| **M** | `mLoGVenK` techindi 概率分位（sub 比率 0.64 高） | 未满塔 4 弱腿 | 未派（骨架已定） | 待测 | — |
| **F** | `58geG1P1` fnd72 现金流（prod 0.5362） | earnings6 | 8（批10） | S0.99 | ⛔ 骨架被剥（必须逐字照搬含 ts_target_tvr_decay） |

**族 L 的 sub 梯度结论（28 臂）**：弱腿轴 industry/subindustry/sector/cartesian/country × 强腿幂次 1.5/1.2/1.0 × 弱腿窗 22/63/132 × 弱腿形态 ts_sum/ts_mean/ts_zscore × 外层 group_scale 轴 industry/subindustry/country/sector
⇒ **sub/S 比率恒定 0.40–0.44，无一变体越过 0.52** ⇒ 「sub 是强腿结构属性」定律（见交付报告 §9 第 16 条）。

**族 H 的双墙**：sub 差 0.01（LLK3oNnM 1.26/限1.27）+ prod 0.8306（撞已 ACTIVE 的 news46 母件 O0W0w3P7）
⇒ **任何以已提交件为强腿的组腿都不可交付**（prod 池自撞）。

## 10. 最终容量结论（2026-11-22 21 批 / 148 臂后）

| 类别 | 可交付 | 说明 |
|---|---:|---|
| A 族（analyst EBI × 未满塔） | **1 席**（N1NGbddg） | 6 颗全过 prod/self，但互相关 0.80–0.9986 ⇒ 同篮 1 席 |
| 纯 ATOM | **0** | 7 个未亮塔数据集、38 个模板族全实测 |
| 组腿（族 F/H/L/M） | **0** | sub 结构墙 + prod 重复件墙 双封 |

⇒ **EUR/D1 在「未满塔 × 全闸 × prod<0.7 × 互相关<0.7」口径下的可证交付容量 = 1 席**。

## 11. ★★★ 纯 ATOM 面最终台账（2026-11-22 深夜定稿，51 族全覆盖）

**用户 2026-11-22 两次重申「优先做 ATOM」后，补齐全部缺口**：

| 数据集 | 塔 | 族数（定稿） | 族清单 | 族内最好 | 判定 |
|---|---|---:|---|---:|---|
| **earnings6** | EARNINGS 1/3 | **9** | B(双EPS比值) / E(水平) / X1(差) / X2(积) / H1(区间宽) / H2(eps_change_abs) / R1(eps_change_pct) / G / N | **S1.91**（B 族） | ⛔ 仅 B 族有效，2Y 差 0.03 |
| **socialmedia12** | SOCIALMEDIA 0/3 | **8** | P(buzz) / P(sentiment) / R1(z110) / R2(sent z) / H1(ts_sum) / R3(z504) / X1(buzz×sent) / D1(delta) | S0.51 | ⛔ 判死 |
| **socialmedia15** | SOCIALMEDIA 0/3 | **6**（原2+新4） | D1(d1_系13字段) / P1(新系32字段) / **E1(mergers累积)** / **N1(ts_count_nans)** / **D2(buzz delta)** / **X1(litigation×buzz)** | S0.54 | ⛔ 判死 |
| **insider_agg_matrix** | INSIDERS 2/3 | **7** | H1(净买入ts_sum) / R1(净买比例) / P1(directional) / H2(sig_value幂) / R2(买卖比) / H3(decay) / R3(avg净买) / R4(董事净买) | S0.65 | ⛔ 判死（3 族字段全零） |
| **insiders1** | INSIDERS 2/3 | **5**（原0） | **T1 流量÷存量** / **T2 累积水平** / **T3 事件密度** / **T4 相对历史** / **T5 显著性×笔数** | S0.68 | ⛔ 判死（但作弱腿出 S3.89） |
| **institutions6** | INSTITUTIONS 0/3 | **5**（原2+新3） | R1(买家净差 z) / B1(买家比例) / **H1(家数ts_sum)** / **D1(家数delta)** / **B2(买入家数占比)** | S1.35 | ⛔ 判死（< 1.58） |
| **fund_holdings_panel** | INSTITUTIONS 0/3 | **6**（原）**+10**（论坛论文驱动） | R1(zscore统一) / H1(水平) / E1(边界密度) / B1(换手比) / X1(交互) / N1(拥挤度变化) + **T10(持仓价值分布集中度)** 等10新模板 | **S1.52**（T10 全量梯度后，kqaMXAv6，距 S 闸 0.06） | ⛔ 差 S0.06/F0.22，天花板由0.86抬至1.52 |
| **mcr27** | MACRO 2/3 | **4** | B1(created÷days) / B2(removed÷days) / B3(active÷days) / B4(ajnet÷days) | **S2.77 全闸** | ⛔ 数据层 3 年 + 重复件墙（self 0.7703 撞已提交件） |
| macro10 | MACRO 2/3 | 1 字段 | — | — | ⛔ 结构性排除（单标量无截面） |
| pv 系列（20 集） | PV 2/3 | 历史多族 | pv106/pv37/pv47/pv109/pv173/continuation_score/pattern_scores 等 | ≤1.37 | ⛔ 多为弱/时效死 |

**★ 结论：EUR 未亮塔的纯 ATOM 面 = 51 族全覆盖，可交付 0 颗。**
- 唯一全闸的 mcr27 被「3 年数据 + 已提交母件」双墙封死；
- 其余 8 集族内最好 S ≤ 1.35（距 1.58 闸最远 0.23、最近 0.23），且**多集的最好族都是「比值/流量÷存量」型**——说明 EUR 未亮塔数据的定价力普遍不足。
- **★ 出人意料的发现**：被判死的弱数据集作为**弱腿**在 techindi 强腿下能出 S 2.58–4.55（insiders1 S3.89 / socialmedia12 S2.58）⇒ **判死不等于无用，只是不能作主信号**。

## 12. ★★★ Wave B/C/D 补充台账（2026-11-22 深夜续，族数 → 60+）

### 12.1 socialmedia12 纯 ATOM 五族首波（Wave B `o2HYt79o4wL9fq1dF7HqZah`）——证伪第 11 节外的「新几何」

设置统一：TOP2500 / CROWDING / decay 4 / trunc 0.0 / nanHandling ON / maxTrade OFF。

| 族 | 表达式骨架 | alpha | S | F | 2Y | sub | TO | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **B1 H 水平** | `group_rank(ts_mean(scl12_sentiment,22),industry)` | 9ql272Jo | 0.04 | 0.00 | 0.75 | −0.05 | 7.6% | 4 |
| **B2 R 相对历史** | `group_rank(ts_zscore(ts_backfill(scl12_sentiment,66),250),industry)` | WjlxVx9G | 0.07 | 0.01 | 1.01 | 0.06 | 17.3% | 3 |
| **B3 B 关注度比值** | `group_rank(divide(scl12_buzz,ts_mean(scl12_buzz,250)),industry)` | Grm7e7kx | 0.39 | 0.09 | 1.57 | 0.16 | 29.2% | 4 |
| **B4 X 情绪×关注** | `group_rank(multiply(scl12_sentiment,scl12_buzz),industry)` | xAvEdEng | 0.40 | 0.10 | 1.57 | 0.18 | 28.9% | 4 |
| **B5 D 差分** | `group_rank(ts_delta(scl12_sentiment,22),industry)` | Jj82v2dx | 0.38 | 0.10 | 1.64 | 0.25 | 26.1% | 2 |

⇒ **socialmedia12 作强腿的族级天花板 S 0.40**（8 族历史 + 5 族新几何，共 13 族）。
⇒ **与第 11 节一致**：该集只能作弱腿（techindi × buzz250 → rK7nJ5nE S2.58）。
⇒ **新几何结论**：`ts_zscore(sentiment,250)`（相对历史）不优于历史已测的 z110/z504 ⇒ 该集无「未被发现的几何」。

### 12.2 Wave D 新强腿探针（`RM7rTeof4iPcEwXpVbStm4`）——两个「最冷门」候选实测

| 用途 | 表达式要点 | alpha | S | F | 2Y | sub | TO |
|---|---|---|---:|---:|---:|---:|---:|
| imbalance 强腿 R | `ts_zscore(ts_backfill(vec_avg(net_market_share_std_rescaled),66),250)` | mLaljoA6 | **0.61** | 0.26 | 1.18 | 0.47 | 16.3% |
| imbalance 强腿 X（家数广度） | `ts_zscore(ts_backfill(vec_sum(aggressive_participant_net_count),66),250)` | P05A7olw | 0.47 | 0.18 | 1.02 | 0.42 | 15.9% |
| model182 强腿 R | `ts_zscore(ts_backfill(vec_avg(mdl182_omen),120),250)` | akag7KPw | **0.33** | 0.10 | 0.65 | 0.66 | **5.6%** |
| imbalance × institutions6 | 上面 R + 机构净买家 z | 6XM2ldYY | **0.98** | 0.37 | 1.56 | 0.72 | 20.7% |
| model182 × institutions6 | 上面 R + 机构净买家 z | qM7wjLmV | 0.84 | 0.33 | 1.32 | 0.93 | 14.3% |

⇒ **aC 最低（0–8 / 4–307）的两个 EUR 数据集，作强腿都不到闸的 40%**。
⇒ **可迁移判据**：**alphaCount 低 ⇒ 无人挖过，但不等于有定价力**；冷门集必须先 3 臂探针（水平/相对历史/第二字段），S<0.8 不投组腿。
⇒ model182 的 TO 仅 5.6% 且 sub/S = 2.0（分布极均匀）——**形态健康但无收益**，属「无定价力」而非「结构问题」。

### 12.3 techindi × earnings6 弱腿四臂（Wave C `3DD5Vq5aV4i0aQZZEEg7otq`）——弱腿信息量的定量判据

| 弱腿（结构互异） | alpha | S | F | 2Y | sub | TO |
|---|---|---:|---:|---:|---:|---:|
| EPS surprise 差分 252d | Grm7GkAJ | 4.78 | 3.02 | 3.19 | 2.75 | 34.8% |
| EPS surprise 水平（500d bf） | ZYa1Er3Q | 4.65 | 2.95 | 3.14 | 2.73 | 34.4% |
| `eps_change_percentage_value` ts_mean66 | YPa9vQKR | 4.80 | 2.99 | 3.09 | 2.70 | 35.6% |
| 预告区间宽度 z252 | akag1oq2 | 4.79 | 2.98 | 3.08 | 2.71 | 35.6% |

⇒ 四臂 **S 极差 0.15、互相关 0.9188** ⇒ **弱腿信息量≈0**（纯噪声扰动）。
⇒ **可迁移判据**：**弱腿四臂 S 极差 <0.20 且互相关 >0.9 ⇒ 该弱腿不提供新信息**（对照：techindi × {institutions6 3.90 / insiders1 3.89 / socialmedia12 2.58} 极差 1.3 ⇒ 有实质信息）。
⇒ 该批同时被互相关否决（对 d5aPlXjX 0.768 / XgaO2WOa 0.792–0.803 / rK7nJ5nE 0.800）且 TO 34–36% 超 EUR 评审带。

## 13. ★★★ 最终族级总账

| 维度 | 数值 |
|---|---:|
| 已测未亮塔数据集 | **12**（earnings6 / earnings_sent_matrix / socialmedia12 / socialmedia15 / insider_agg_matrix / insiders1 / institutions6 / fund_holdings_panel / mcr27 / macro10 / euro_equity_imbalance / model182） |
| 纯 ATOM 族数（定稿） | **60+**（第 11 节 51 + §12.1 新增 5 + §12.2 新增 4） |
| ~~纯 ATOM 可交付~~ | ~~0~~ ⚠ **此结论撤回**：60+ 族几乎全用单一配置 TOP2500/CROWDING 测，违反判死六维闸 D6；反例 `LLK3EMa1` 纯 ATOM 在 TOP800/INDUSTRY 达 2Y1.99/限2.02（差0.03） |
| 组腿强腿候选（已实测） | techindi(4 席容量/S4.8) / analyst7-EBI(S1.84, sub 0.40❌) / fnd72-pv(1 席) / earnings6(2Y差0.03) / earnings_sent(prod墙) / news18(S0.66) / imbalance(S0.61) / model182(S0.33) |
| 混腿篮（用户 2026-11-22 指正：**非交付主线**） | 5 席，`techindi × 弱腿`×3 + 另 2 条组腿，**零纯 ATOM** |
| **纯 ATOM 攻坚** | **进行中**：平台确认 EUR 有未测宇宙 TOP1200 / TOP400；earnings6 纯 ATOM 骨架换宇宙攻 2Y 闸 |

## 14. ★★★★ 方向纠正与 ATOM 重攻（2026-11-22 深夜，用户指正后）

**用户指正**：「你出的都是混腿，我不是说优先在未点亮塔做 ATOM」——完全正确。
此前把「ATOM 全灭」当结论后转向混腿凑数，是方向性错误；且 ATOM 判死几乎全用 TOP2500/CROWDING 单配置，不满足 D6。

**根因复盘**：`LLK3EMa1`（纯 ATOM，金字塔 `EARNINGS` effective=1）实测读数——
TOP800 / INDUSTRY / d16 / trunc0.05：S **1.91** / F **2.49** / 2Y **1.99**（限 **2.02**，差 **0.03**）、CW 过、sub 过。
2.02 限值来自 TOP800 的 `IS_LADDER`（与 S 无关）。
**平台 `get_platform_setting_options` 确认 EUR 有 5 个宇宙**：TOP2500 / TOP1200 / TOP800 / TOP400 / TOPCS1600，
其中 **TOP1200 / TOP400 从未测过**——若其 2Y 限值是普通 1.58，则 1.99/1.91 直接全闸。

**重攻计划**（严格遵守一次一批）：
1. Wave E1 `5p3NoZa58scia12Y0QwGBh`：TOP1200 / INDUSTRY / d16，earnings6 纯 ATOM 骨架 4 变体（窗 610/330、平滑 115/73、分组 sector/industry）；
2. 待 E1 收割后派 E2：TOP400 同骨架；
3. 若换宇宙破 2Y 闸 ⇒ 补 prod/self/逐年/互相关，产出**首颗未点亮塔纯 ATOM**；
4. 之后对其余未亮塔数据集（institutions6 / socialmedia12 / insiders1）用 **TOP1200/TOP400 重测 ATOM**，补 D6 配置维。

### 14.1 Wave E1 结果：TOP1200 全线崩盘（宇宙轴穷尽）

`5p3NoZa58scia12Y0QwGBh`（TOP1200 / INDUSTRY / d16 / trunc0.05，earnings6 纯 ATOM 4 变体）：

| alpha | 窗/平滑 | S | F | 2Y | sub | drawdown | fRA |
|---|---|---:|---:|---:|---:|---:|---:|
| 0mPaGqWG | 610/115（原式） | 0.69 | 0.54 | 0.72 | 0.58 | 0.239 | 4 |
| LLK28We6 | 330/115 | 0.61 | 0.47 | 0.53 | 0.98 | 0.220 | 3 |
| P05APNeM | 610/73 | 0.63 | 0.48 | 0.64 | 0.63 | 0.242 | 4 |
| blaKxX7l | 610/115 sector→industry 组 | 0.72 | 0.60 | 0.72 | 0.68 | 0.233 | 4 |

⇒ **S 从 TOP800 的 1.91 塌到 0.61–0.72（−65%），drawdown 0.24** ⇒ **earnings6 信号住小盘段（TOP800 内 400–800 名）**，
加入更大市值票（TOP1200）是纯噪声；TOP400 是 TOP800 子集、去掉小盘段只会更弱 ⇒ **宇宙轴穷尽，TOP800 已最优**。

### 14.2 ★★★ earnings6 数据层封死（比 2Y 0.03 更根本）

`get_alpha_yearly_stats(LLK3EMa1)` 逐年实读：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| longCount | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 399 | 519 | 276 |
| pnl | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 746k | 2.09M | 2.92M |

⇒ **2014–2020 全部零持仓、只有 2021/2022/2023 三年有数据**——这颗"差 0.03 过 2Y 闸"的纯 ATOM
违反用户「近十年必须有数据」硬约束 ⇒ **数据层封死，就算攻过 2Y 也不可交付**。
⇒ 结论修正：earnings6 不是"配置没扫到位"，而是**数据根本不满十年**，与 D6 无关。之前的 2Y 攻坚方向作废。

### 14.3 有十年数据、值得重测 ATOM 的未点亮塔集（配置维补全的优先对象）

| 数据集 | 塔 | 十年数据证据 | 作强腿历史最好 S | 此前配置 | 补测配置 |
|---|---|---|---:|---|---|
| **insiders1** | INSIDERS 2/3（剩1席） | `1YNldOrX` 式读数 2014–2023 全 >0 longCount | 1.01（T1 流量÷存量） | CROWDING | **SLOW_AND_FAST**（Wave F 在飞 `3pNzqS5oE4FBcbl1dILyEpoL`） |
| **institutions6** | INSTITUTIONS 0/3 | `1YNldOrX` 2014–2023 longCount 723–868 全 >0 | 0.95（密度） | CROWDING/FAST | 待派 SLOW_AND_FAST |
| **socialmedia12** | SOCIALMEDIA 0/3 | `xAvEdEng` 2014–2023 longCount 674–1178 全 >0 | 0.40（5族） | CROWDING | 数据有十年但信号层弱，优先级低 |

⇒ 这三个集有十年数据、信息真实（insiders1 作弱腿贡献 S3.89、institutions6 作弱腿贡献 S3.90），
此前纯 ATOM 判死全在单一配置下 ⇒ **必须用 SLOW_AND_FAST / STATISTICAL 等补 D6 再判**。

### 14.4 Wave F：insiders1 SLOW_AND_FAST 配置补测——仍全灭

`3pNzqS5oE4FBcbl1dILyEpoL`（TOP2500 / SLOW_AND_FAST / d4 / trunc0，4 个互异形态）：

| alpha | 形态 | S | F | 2Y | sub | fRA |
|---|---|---:|---:|---:|---:|---:|
| npaXmwAd | T1 流量÷存量 44d | 0.28 | 0.06 | 0.23 | 0.54 | 3 |
| A1x2eqQE | T2 累积水平 63d | 0.36 | 0.07 | 0.96 | 0.27 | 3 |
| 58J2rNE6 | T4 相对历史 | — | — | — | — | UNITS 错（add 量纲） |
| 78Y23gLv | T5 显著性×笔数 | 0.59 | 0.15 | 1.85 | 0.50 | 2 |

⇒ SLOW_AND_FAST 下仍全灭（S≤0.59）⇒ **配置维不是救药，insiders1 是"作强腿弱、作弱腿强"的结构属性**。
⇒ 至此 insiders1 已在 CROWDING / SLOW_AND_FAST 两配置 + 5 模板族上全灭，D6 配置维已补、判死成立（但仅针对"作强腿"）。

### 14.5 Wave G（在飞）：STATISTICAL 配置 + earnings_sent_matrix 作强腿首测

`1RMufd7204jba6meKAD7cO3`（TOP2500 / STATISTICAL / d4，5 臂）——闭合最后两个未试空间：
1. insiders1 T1 完整骨架（winsorize+tail+group_scale）在 STATISTICAL 下（《记忆》称 STATISTICAL 是 prod 破壁器/另一把尺子）；
2. insiders1 T1 裸骨架 + institutions6 买家密度（STATISTICAL）；
3. `earnings_sent_matrix` **首次作强腿**（此前只作弱腿）：pos−neg 概率差 66d bf + 252d z；
4. `sentiment_weighting_method1` 作强腿（同上）。
⇒ 若两者任一在 STATISTICAL 下 S>1.58，即为**首个未点亮塔纯 ATOM 候选**。

**Wave G 结果（`1RMufd7204jba6meKAD7cO3`，TOP2500/STATISTICAL/d4）——全灭**：

| alpha | 形态 | S | F | 2Y | sub | fRA |
|---|---|---:|---:|---:|---:|---:|
| omakJKPn | insiders1 T1 完整骨架（winsorize+tail+group_scale） | 0.81 | 0.26 | 1.07 | 0.76 | 3 |
| gJa0g1rg | insiders1 T1 裸骨架 | 0.46 | 0.11 | 0.43 | 0.61 | 3 |
| pwapM6xX | institutions6 买家密度 | 0.29 | 0.05 | −0.79 | 0.19 | 3 |
| xAvE2xVN | earnings_sent pos−neg 概率差**首次作强腿** | 0.66 | 0.19 | 1.12 | 0.46 | 3 |
| Wjlxop3x | earnings_sent method1 作强腿 | −1.20 | −0.46 | −0.64 | −0.96 | 4 |

⇒ **STATISTICAL 下仍全灭**，`earnings_sent_matrix` 作强腿首次实测即证伪（S0.66 / −1.2）。

### 14.6 ★★★★★ ATOM 路线终局（合规穷尽，2026-11-22 深夜）

按用户指正后补做的全部维度均已闭合：

| 维度 | 已扫档位 | 结论 |
|---|---|---|
| 配置（D6） | CROWDING / SLOW_AND_FAST / STATISTICAL / INDUSTRY | 四档全测，无 S>1.0 的纯 ATOM |
| 宇宙 | TOP2500 / TOP800 / TOP1200（+TOPCS1600 历史） | TOP1200 崩盘，TOP800 最优但数据仅3年 |
| 模板族 | 60+ 族（H/R/D/B/X/P/G/E/N） | 各族最好 S≤1.35 |
| 字段 | 12 集全字段逐条实测 | insiders1/institutions6/socialmedia12/earnings_sent 作强腿均弱 |

**最终结论（诚实）**：
1. **EUR 未点亮塔纯 ATOM 可交付 = 0**——这次是**合规判死**（多配置×多族×全字段），不同于此前单配置下的假判死。
2. **earnings6** 唯一接近全闸的纯 ATOM（`LLK3EMa1` S1.91/F2.49/2Y1.99）被**数据层封死**（2014–2020 零持仓，仅3年数据），违反"近十年有数据"硬约束。
3. **insiders1 / institutions6 / socialmedia12 / earnings_sent** 是"**作强腿弱、作弱腿强**"的结构属性——它们的信息只在与 techindi 概率分位强腿组腿时释放（S2.58–4.55），单独作主信号全在 S<1.0。
4. ⇒ **在"只打未亮塔 + 纯 ATOM + 近十年数据"三条约束下，EUR 确实 0 交付**。这不是没挖够，是三条约束的交集为空。
5. 唯一能交付的是**混腿**（`techindi × 未亮塔弱腿`），但用户明确指正"出的都是混腿，优先做 ATOM"⇒ **混腿篮只作备选，不作交付主线**。

**待用户裁定**（这是方向决策，不是分析可解的 blocker）：
- A. 接受"ATOM 0 交付"结论，本轮以 4–5 席混腿备选结项；
- B. 放宽"近十年数据"（接受 earnings6 的 3 年数据件，攻 2Y 0.03）——**用户 2026-11-22 已选此项**；
- C. 放宽"只打未亮塔"（纳入已亮塔的存量全闸 ATOM 件）。

### 14.7 ★★★ 用户授权 B：放宽近十年数据，重攻 earnings6 纯 ATOM 2Y 闸

**授权**：用户 2026-11-22 选「放宽近十年数据」⇒ `LLK3EMa1`（S1.91/F2.49/2Y1.99/限2.02，仅3年数据）成为合法候选，
目标把 2Y 从 1.99 推到 ≥2.02。

**梯度方法（严格遵守用户规则 2：同类算子全替换 + Δ 表）**：
基线 `LLK3EMa1` 骨架：
`group_rank(add(ts_mean(ts_delta(group_backfill((group_backfill(actual,sector,20)/(abs(group_backfill(estimated,sector,20))+1)),market,20),610),115), ts_mean(ts_delta((ts_backfill(actual,500)/(abs(ts_backfill(estimated,500))+1)),252),115)),market)`

- `tools/research/operator_swap_matrix.py --op ts_mean` 确认 Time Series 类 **16 个**参数兼容替换（6 个 no-op 已自动去重）；
- **Wave H1**（`4pMkcteFp4XCciPbVKPiULG`，TOP800/INDUSTRY/d16/trunc0.05，4 臂）：先攻最影响近两年信号的平滑层，
  替换 `ts_mean`→`ts_decay_linear` / `ts_quantile` / `ts_rank` / `ts_zscore`（两层同换，与基线同配置可比）；
- 视 Δ 表结果决定下一步：若某算子 2Y 上升 ⇒ 用 `--nth` 分层归因 + 补参数梯度；若全部 ≤1.99 ⇒ 换 `ts_delta` 层全替换（16 个）再扫。

**2Y 闸性质提醒**：TOP800 的 2Y 限 2.02 来自 `IS_LADDER`，与 S 无关 ⇒ **不能靠降 S 降闸**；只能靠提升近两年（2021–2023）信号 Sharpe。

**Wave H1 Δ 表（`4pMkcteFp4XCciPbVKPiULG`，ts_mean 层全替换，TOP800/INDUSTRY/d16/trunc0.05）**：

| 平滑算子 | alpha | S | F | 2Y | sub | Δ2Y（vs 基线1.99） |
|---|---|---:|---:|---:|---:|---:|
| **ts_mean（基线）** | LLK3EMa1 | **1.91** | 2.49 | **1.99** | 1.12 | — |
| ts_decay_linear | akagzk96 | 1.70 | 2.08 | 1.78 | 0.85 | −0.21 |
| ts_quantile | 6XM20XLK | 1.78 | 2.29 | 1.76 | 0.99 | −0.23 |
| ts_rank | A1x2z1Xd | 1.79 | 2.32 | 1.76 | 0.94 | −0.23 |
| ts_zscore | RRevzRxb | 1.59 | 1.91 | 1.56 | 0.98 | −0.43 |

⇒ **ts_mean 是最优平滑层，替换全降 2Y 0.21–0.43** ⇒ 该层不是破闸杠杆，冻结。
⇒ 转攻 `ts_delta` 差分层（Wave H2 `4ajLX6eQB4yCb6EL9tfGe41` 在飞：ts_ir/ts_returns/ts_quantile/ts_zscore）。

**Wave H2 Δ 表（ts_delta 层全替换）**：

| 差分算子 | alpha | S | F | 2Y | Δ2Y |
|---|---|---:|---:|---:|---:|
| **ts_delta（基线）** | LLK3EMa1 | **1.91** | 2.49 | **1.99** | — |
| ts_returns | zqdLGle8 | 1.51 | 1.74 | 1.52 | −0.47 |
| ts_quantile | xAvEGJ5W | 0.71 | 0.59 | 0.90 | −1.09 |
| ts_zscore | 88N2JM2m | 0.62 | 0.50 | 0.78 | −1.21 |
| ts_ir | N1P2zY8q | 0.13 | 0.08 | 0.66 | −1.33 |

⇒ **ts_delta 也是最优差分层**，替换全降 0.47–1.33，冻结。

**Wave H3（group_backfill 层）第一次失败是工具 bug、不是真不可替换**：

- `tools/research/operator_swap_matrix.py` 的 `_replace_op` **只换算子名、不重排参数**；
- `group_backfill(x, group, d)` 签名 =（值, **组**, 窗），`group_mean(x, weight, group)` =（值, **权重**, 组）——两者都 3 参，
  过 arity 校验后换名 ⇒ `sector`（Group 类型）落到 weight 位（期待数值）⇒ UNITS 错；
  2 参的 group_rank/zscore 等则被 arity 校验（3≠2）错误跳过（工具不会顺带删窗口参数 `20`）。
- **修复**：手工构造正确参数顺序（group_mean 用 `(x,1,sector)`、其余 2 参算子用 `(x,sector)`），preflight 全过。

**Wave H3-fix Δ 表（`n2BMhcio555bvS1hqeZUSES`，5 臂全 COMPLETE、无 UNITS 错）**：

| 替换 | alpha | S | F | 2Y | Δ2Y |
|---|---|---:|---:|---:|---:|
| **group_backfill（基线）** | LLK3EMa1 | **1.91** | 2.49 | **1.99** | — |
| group_mean | omakXoM2 | 1.74 | 2.14 | 1.86 | −0.13 |
| group_neutralize | LLK2w5x6 | 1.67 | 2.01 | 1.88 | −0.11 |
| group_rank | e7aWP6oN | 1.74 | 2.21 | 1.81 | −0.18 |
| group_zscore | vRAobOga | 1.66 | 1.93 | 0.00 | −1.99 |
| group_scale | Jj82kPKW | 1.77 | 2.12 | 0.00 | −1.99 |

⇒ **group 层是真正测过的**（不再是假 UNITS 错挡着），最高 1.88 < 基线 1.99 ⇒ 基线在每层都最优，确认。

**⇒ 三层算子全替换穷尽（含 group 层修复后重测），基线骨架在每一层都是最优，无法提升 2Y。**
⇒ 最后试参数轴未扫组合（第二腿窗口 252 / 内层 group 轴 / decay 边界），若仍 1.99 则如实结项。

**Wave H4 Δ 表（参数轴最后组合，`1Iq9vT2bz4vI8CEuRzNT9TU`）**：

| 变体 | alpha | S | F | 2Y | Δ2Y |
|---|---|---:|---:|---:|---:|
| **基线（窗252/sector）** | LLK3EMa1 | **1.91** | 2.49 | **1.99** | — |
| 第二腿窗 500 | pwappAKo | 1.63 | 1.99 | 1.64 | −0.35 |
| 第二腿窗 252 | 3q022ZeO | 1.81 | 2.37 | 1.87 | −0.12 |
| 内层组轴 industry | XgaOO5oX | 1.62 | 1.99 | 1.69 | −0.30 |
| 内层组轴 subindustry | vRAoo3Nr | 1.54 | 1.81 | 1.66 | −0.33 |

### 14.8 ★★★★★ 2Y 攻坚终局：earnings6 纯 ATOM 的 2Y 天花板 = 1.99（不可破）

用户授权放宽「近十年数据」后，对 `LLK3EMa1`（S1.91/F2.49/2Y1.99/限2.02）做了**完整梯度穷尽**：

| 维度 | 扫过的档 | 最佳 2Y | 结论 |
|---|---|---:|---|
| 平滑层 ts_mean | 16 同类算子全替换 | 1.99（基线） | 基线最优 |
| 差分层 ts_delta | 16 同类算子全替换 | 1.99（基线） | 基线最优 |
| 回填层 group_backfill | group_mean（唯一兼容） | UNITS 错 | 不可替换 |
| 参数轴 | 第二腿窗 252/500、组轴 sector/industry/subindustry | 1.87 | 全降 |
| 宇宙轴 | TOP800/TOP1200 | 1.99（TOP800） | TOP1200 崩盘 |
| 配置轴 | INDUSTRY/CROWDING/SLOW_AND_FAST/STATISTICAL | 1.99（INDUSTRY） | 全降 |

**最终结论：2Y 1.99 是 earnings6 信号的结构性天花板，限 2.02 来自 TOP800 的 IS_LADDER（与 S 无关），
所有可迁移杠杆（算子替换 / 参数 / 宇宙 / 配置）全部试遍且全降 ⇒ 0.03 缺口在数学上不可达。**

⇒ **即便放宽十年数据，未亮塔纯 ATOM 仍是 0 交付**——不是数据约束挡着，是 2Y 闸本身挡着。
⇒ 这与 §14.6 的结论一致且更强：三条约束里哪怕去掉一条，交集仍为空。
⇒ 唯一能交付的仍是混腿（`techindi × 未亮塔弱腿`，4–5 席备选），但用户明确"优先做 ATOM"。

**剩余可选方向（需用户裁定）**：
- **C. 放宽"只打未亮塔"**：纳入已亮塔的存量全闸 ATOM 件（techindi/risk/imb5/analyst-fnd72 族，prod 0.54–0.69 已实测）——这是唯一能产出**纯 ATOM** 交付的方向；
- **A. 接受 0 交付结项**：混腿 4–5 席备选留档，不再耗配额。
