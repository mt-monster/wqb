# WAVE rt-insiders-atom-w1 — `insiders1` 逐臂归因（DEU/TOP500/D1，纯 ATOM 单集）

- 日期：2026-11-17；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集 / 目标塔：`insiders1`（塔 **INSIDERS**）；**纯 ATOM 单集**，无第二数据集腿
- 配置（`get_alpha_details` 9/9 逐臂回显一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=**0**、truncation=0.08、nanHandling=**ON**、maxTrade=OFF、maxPosition=OFF、pasteurization=ON、unitHandling=VERIFY、FASTEXPR、simulationMode=FULL；`startDate=2014-01-01`、`endDate=2023-12-31`
  - ⚠ 与区域生产档 `tracking/DEU/config/settings.json:8,12,16`（decay=**4**、nanHandling=**OFF**、2013-01-01 起）不同 ⇒ 本波是**探针口径（decay0/nanON）**，读数只能在 decay0/nanON 档内比较，不能与生产档跨档比。
- 派发/收割（ask 转录，本档未重跑派发）：`create_multi_simulation` 一次派发 9 臂 → multisim `1S6Yod8454zMcoRHrXWjPGq`；`batch_status` 轮询 4 次，前 3 次 child_count=0/parent_status=null（队列注册滞后），第 4 次 child_count=9 / terminal=9 / errors=0 / all_terminal=true（全 COMPLETE，无 ERROR/CANCELLED）；`harvest_multisim_alphas(multisimulation_location=…1S6Yod8454zMcoRHrXWjPGq)` 一次成功（未走 404 兜底），total=9/complete=9/error_count=0；`upsert_backtest_rows(DEU, rt-insiders-atom-w1, insiders1, 9)` → n=9。本档另做独立只读复核（见 §7）。
- 参考：`FIELD_insiders1_20261117.md`（本轮最新字段档案）；insiders 单集上限锚点 `tracking/DEU/atom_orthogonal/BE176_INSIDERS1_CEILING_130_20261112.md`（三波 1.22/1.30/1.19 收敛）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

指标经 `mcp__wq-brain-http__batch_get_alpha_metrics`（9/9 success）与 `get_alpha_details` 逐臂（9/9）复核，与 ask 转录**逐值一致**。`failed_ra`/`checks.fail` 以 `get_alpha_details` 实读为准。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔（pyramids.list） | RA fail（平台 checks.fail） |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|---|---|
| 1 | `A1x3MPal` | 臂2 核 ÷ (tradesignificance+0.5) | 0.64 | 0.37 | 1.16 | −0.23 | 3.51% | 16.35% | 24.1bp | 81/130 | DEU/D1/INSIDERS×1.6（eff 1） | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.5/0.1@2014-02-03**, LOW_SUB(−0.23/0.30), LOW_2Y |
| 2 | `e7aro0qp` | 臂1 裸核（去 ÷significance） | 0.60 | 0.34 | 0.67 | −0.01 | 3.22% | 18.23% | 24.9bp | 82/130 | DEU/D1/INSIDERS×1.6（eff 1） | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.5/0.1@2014-02-03**, LOW_SUB(−0.01/0.28), LOW_2Y |
| 3 | `j2agb0d9` | tradesignificance 纯水平 | 0.07 | 0.01 | **1.37** | 0.47 | 5.83% | 12.01% | 0.99bp | 139/136 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y(1.37/1.58) |
| 4 | `LLKRA1lM` | price / ts_mean(price,250)（价格位置） | 0.60 | 0.28 | 1.15 | **0.59** | 7.20% | **5.46%** | 7.7bp | 140/150 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y |
| 5 | `Wjlg6Gaj` | Δ66(holdings) / mean250(holdings) | 0.60 | 0.41 | 0.81 | −0.15 | 4.99% | 12.14% | **23.4bp** | **41**/101 | DEU/D1/INSIDERS×1.6（eff 1） | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.5/0.1@2014-01-31**, LOW_SUB(−0.15/0.28), LOW_2Y |
| 6 | `XgaK5n2X` | 新鲜度[250−days_from_last_change] ÷ (sig+0.5) | 0.34 | 0.13 | 0.22 | 0.00 | 5.39% | 12.97% | 7.1bp | 138/149 | DEU/D1/INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.00/0.16), LOW_2Y |
| 7 | `vRAm3ler` | ts_sum(sign(Δ1 holdings),66)（符号频率） | 0.29 | 0.11 | **0.05** | 0.23 | **12.27%** | 12.61% | 2.8bp | 93/101 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y |
| 8 | `omaYMl3k` | tradesignificance ÷ (rank(ts_ir(Δ66))+.5)（臂1 反向） | 0.56 | 0.39 | **1.18** | **−0.28** | 9.60% | **21.56%** | 12.9bp | **32**/86 | DEU/D1/INSIDERS×1.6（eff 1） | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.2857/0.1@2014-03-04**, LOW_SUB(−0.28/0.27), LOW_2Y |
| 9 | `O0W9EZn1` | ts_ir(holdings 水平,66) ÷ (sig+0.5) | **0.74** | **0.47** | 1.13 | 0.35 | 5.71% | 14.30% | 17.6bp | 88/132 | DEU/D1/INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y |

- **平台 `status`**：9/9 = `UNSUBMITTED`；`stage=IS`。仿真终态 9/9 COMPLETE、errors=0。
- **本波极值**：best S **0.74**（臂9 `O0W9EZn1`）/ best 2Y **1.37**（臂3 `j2agb0d9`）/ best F 0.47（臂9）/ best sub 0.59（臂4）/ best DD 5.46%（臂4）/ best margin 23.4bp（臂5）/ 最宽 140·150（臂4）。
- **0 达标**：9/9 臂 `failed_ra_count` ≥3，**无一条过 RA 全闸**。

### 1.1 平台实读限值（本轮 `checks.fail` 实读）

| 闸 | 平台实读 limit | 备注 |
|---|---|---|
| LOW_SHARPE | **1.58**（9/9） | 与 ask 基准一致 |
| LOW_FITNESS | **1.0**（9/9） | 一致 |
| LOW_2Y_SHARPE | **1.58**（9/9，year=2） | 一致 |
| CONCENTRATED_WEIGHT | **0.10**（臂1/2/5 value=0.5、臂8 value=0.2857） | ask 的 CW≤0.10 即平台 limit；0.5 仅本地 review 参考 |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂动态**：臂1 0.30 / 臂2 0.28 / 臂5 0.28 / 臂6 0.16 / 臂8 0.27；臂3/4/7/9 判 pass | ⚠ sub≥1.0 是内部 review 线，**不是平台闸限**；但本波 0 达标对 sub 口径不敏感（见 §6） |

## §2 逐臂归因条目

### 2.1 holdings 核族（臂1/2/5/8/9）——水平 IR > Δ 核，是唯一「更强且更干净」的结构

1. **臂9 `O0W9EZn1`（ts_ir(holdings 水平,66) ÷ (sig+0.5)）**：S **0.74**/F **0.47**/2Y 1.13/sub 0.35/TO 5.71%/DD 14.30%/margin 17.6bp/LC 88·SC 132；只挂 3 闸（S/F/2Y），**无 CW、无 sub fail**。**vs 臂1（Δ 核）**：S +0.10、F +0.10、sub +0.58（−0.23→0.35）、margin 高约 6bp，且 **CW 由满值挂闸（臂1 0.5）变为 pass**。⇒ 本波唯一「更强且更干净」的核心，但 S 仍距闸 0.84、F 距闸 0.53，**不构成近闸**。
2. **臂1 `A1x3MPal`（Δ66 of ts_mean66 → ts_ir252）÷ (sig+0.5)**：S 0.64/F 0.37/2Y 1.16/sub −0.23/TO 3.51%/DD 16.35%/margin 24.1bp/LC 81·SC 130；CW 0.5 满值挂闸。**vs 臂2（同核裸版）** 见 §3.1。
3. **臂2 `e7aro0qp`（臂1 同核裸版，无 ÷significance）**：S 0.60/F 0.34/2Y 0.67/sub −0.01/LC 82·SC 130；CW 0.5 挂闸。⇒ 裸核 S 0.60 **已远低于 BE176 的单集上限带 1.0–1.30**：本波既不支持「insiders1 单集可破顶 1.58」，也**不构成对上限的证伪**，只是再次落在上限之下。
4. **臂5 `Wjlg6Gaj`（Δ66 / mean250 比率）**：S 0.60/F 0.41/2Y 0.81/sub −0.15/TO 4.99%/DD 12.14%/margin **23.4bp（本波最高）**/LC **41**·SC 101；CW 0.5 挂闸。margin 最高但 **LC 41 单侧偏薄 + CW 满值挂闸 = 宽度塌缩**（同 prior wave 的「无回填 / 稀疏事件流被当逐日量」形态），归**表达层**，不作数据层排除。
5. **臂8 `omaYMl3k`（sig ÷ (rank(ts_ir(Δ66))+.5)，臂1 的反向比率）**：S 0.56/F 0.39/2Y **1.18**/sub **−0.28（本波最低）**/TO 9.60%/DD **21.56%（本波最高）**/margin 12.9bp/LC **32**·SC 86；CW 0.2857 挂闸。**vs 臂3（纯 sig 水平）**：S **+0.49**、F **+0.38**，但 sub **−0.75**、DD **+9.6pp**、LC 139→32 ⇒ **S/F 升而稳健性/宽度净稀释**。2Y 1.18 距 1.58 闸 0.40（边界）是它唯一近闸入口。

### 2.2 非 holdings 单腿（臂3/4/6/7）

6. **臂3 `j2agb0d9`（tradesignificance 纯水平）**：S **0.07**/F 0.01/2Y **1.37（本波最高）**/sub 0.47/TO 5.83%/DD 12.01%/margin **0.99bp**/LC 139·SC 136（健康宽）。⇒ 纯 significance 水平**强度层近乎全灭**（S 0.07、margin 0.99bp），但 **2Y 1.37 是最近的硬闸缺口（距 1.58 仅 0.21）**，宽度/回撤健康 ⇒ 作为**近闸锚**记录，不作为强度候选。
7. **臂4 `LLKRA1lM`（price / ts_mean(price,250)，价格位置 M8）**：S 0.60/F 0.28/2Y 1.15/sub **0.59（本波最高）**/TO 7.20%/DD **5.46%（本波最低）**/margin 7.7bp/LC **140·SC 150（本波最宽）**；只挂 3 闸。⇒ 本波**最健康的低回撤结构**（宽度最宽、DD 最低、sub 最高），代价是 margin/收益低 ⇒ S 只到 0.60。**无裸 price 单腿对照**，无法把「0.60」归因于比率壳层还是 price 轴本身（盲区，§8）。
8. **臂6 `XgaK5n2X`（新鲜度 ÷ (sig+0.5)）**：S 0.34/F 0.13/2Y 0.22/sub 0.00/TO 5.39%/DD 12.97%/margin 7.1bp/LC 138·SC 149；LOW_SUB 0.00 vs 0.16 挂。⇒ 新鲜度轴在此几何**弱**（2Y 0.22、sub 0.00）；**无裸新鲜度对照**，不能断定是除法壳层还是轴本身。
9. **臂7 `vRAm3ler`（ts_sum(sign(Δ1),66)，净增持日频率）**：S 0.29/F 0.11/2Y **0.05（本波最低）**/sub 0.23/TO **12.27%（本波最高）**/DD 12.61%/margin 2.8bp/LC 93·SC 101；只挂 3 闸。⇒ **符号频率轴（M5）在本档全灭**：2Y 0.05、换手最高、margin 2.8bp。

## §3 符号指纹 / 稀释铁律

### 3.1 符号指纹逐条（ask 六条）

| # | 判据 | 本波实测 | 结论 |
|---|---|---|---|
| ① | 整式取反 S(−e)≈−S(e) 且 TO/DD/LC 逐位相同=方向层无净信息即停 | **0 条翻符号臂**（9 条表达式全为正向 rank 结构，无前置负号 / `multiply(-1,…)`） | **未测**（无对照臂）⇒ 不得据此判「机制在」或「方向死」 |
| ② | 去第二腿应回落≈1.0–1.30（BE176 insiders1 ATOM 上限） | **纯 ATOM，无第二数据集腿**；最接近的「去分母」对照 = 臂2 裸核 S **0.60**（vs 臂1 0.64） | 裸核 0.60 **低于 BE176 上限带下限 1.0** ⇒ 本波落在上限之下，未破顶、未证伪 |
| ③ | decay0/4/8 对照，decay4 相对 decay0 掉>30%=快变分量别用 | **仅 decay0**（9/9 臂 decay=0）；decay4/8 一条未跑 | **未测**（配置层单点，D6 未达） |
| ④ | LC/SC<60/60 = backfill 假填充 | 无臂两侧同时 <60；臂5 LC**41**/SC101、臂8 LC**32**/SC86 为**单侧偏薄但另侧健康** | 非「假填充」；记为**宽度不对称**（thin long side），归表达层 |
| ⑤ | 费率分组正反两桶应同向单调，各桶与裸跑逐位相同=轴无信息 | **无 bucket/费率分桶臂**；9/9 只用 `group_rank(…, sector)` 单一分组轴 | **N/A（未测）**；分组轴单一，无法判 axis 信息量 |
| ⑥ | 首臂 S<1.58 或 sub<0.39 即停（DEU-INSIDER-AGGMATRIX-DEAD 0.92 上限 / 单腿 1.36 先验） | **首臂 臂1 `A1x3MPal` S 0.64<1.58、sub −0.23<0.39 → 触发即停**；后续 8 臂全部确认低于闸 | **触发停扫信号**；9 臂整体与「insiders1 单集强度封顶」一致 |

### 3.2 稀释铁律（乘法 / bucket 低于对应单腿 = 稀释）

- **本波零乘法、零 bucket** ⇒ 稀释铁律的**直接对象为零**（不是"复合全死"，是"未测乘法/bucket 复合"）。
- 唯一可做的**单变量除法对照**：
  - **臂1 vs 臂2（÷significance）**：S **+0.04**、F **+0.03**、2Y **+0.49（0.67→1.16）**、sub **−0.22**、TO +0.29pp、CW 不变（均 0.5 挂）。⇒ **对 S/F 不是稀释、2Y 是唯一显著正项**，但 sub 净损；仍远低闸。
  - **臂8 vs 臂3（sig 裸 → sig ÷ rank(IR)）**：S **+0.49**、F **+0.38**，但 2Y −0.19、sub **−0.75**、DD **+9.6pp**、LC 139→32、CW 由 pass 变挂 ⇒ **S/F 升而稳健性/宽度严重稀释**。
- ⇒ 本波**没有一条复合形态在「S/F/2Y/sub/宽度」上全面高于其对应单腿**；唯一"净升"的 ÷significance 也只升 S/F/2Y、损 sub，与「复合需全面高于单腿才值留」的纪律不符。

### 3.3 宽度塌缩 + CONCENTRATED_WEIGHT 单独登记（数据层 ≠ 信号死 ≠ 表达层）

| 臂 | LC/SC | CW（value vs limit 0.10） | 归因 |
|---|---|---|---|
| 臂1 `A1x3MPal` | 81/130 | **0.5** @2014-02-03 挂 | 表达层：Δ 核的稀疏中的单名集中 |
| 臂2 `e7aro0qp` | 82/130 | **0.5** @2014-02-03 挂 | 表达层：同核裸版，CW 由核继承（非分母造成） |
| 臂5 `Wjlg6Gaj` | **41**/101 | **0.5** @2014-01-31 挂 | 表达层：Δ/mean 比率，LC 单侧薄 + CW 满值 |
| 臂8 `omaYMl3k` | **32**/86 | **0.2857** @2014-03-04 挂 | 表达层：反向比率，LC 最薄 |
| 臂3/4/6/7/9 | 88–150 | pass | 无塌缩（臂9 88/132、臂4 140/150 最宽） |

- **本波 0 条 data_excluded**：同集同配置下 5 条臂 LC 88–150、pnl 正、TO 3.5–12.3% 正常区间 ⇒ **数据存在且可交易**，无「字段无数据」证据。CW 塌缩的四臂（1/2/5/8）一律归**表达层**，不得登记 `data_excluded`，也不得登记信号死。

## §4 塔位判读（点塔相关性）

平台 `get_alpha_details.pyramids` 逐臂实读（**9/9**）：

- **目标塔 INSIDERS 出现 9/9 臂**，全部为**单塔** `DEU/D1/INSIDERS`×1.6（`effective=1`）；`ra.pyramid_short` 9/9 = `insiders`。
- **点位 ≠ 点亮**：9/9 臂 `failed_ra_count` ≥3（3–5），**本波实际点亮 INSIDERS 塔 0 颗**，塔计数不变。
- **纯 ATOM 单集**：全部表达式只引用 `insd1_holdings / insd1_tradesignificance / insd1_price`，无第二数据集字段 ⇒ 无「双塔/配腿」形态，本波不产生第二塔位申请。
- ⇒ 点塔入口成立（9/9 群属 INSIDERS），但 0 点亮。

## §5 判死六维闸盘点（D1–D6；本波自身口径）

| 维 | 本波现状 | 判定 |
|---|---|---|
| **D1 结构互异模板 ≥10** | **仅 9 臂（<10）= 探针**；结构互异约 **6–7**：sig 水平(臂3)/price 位置(臂4)/Δ÷mean(臂5)/新鲜度(臂6)/符号频率(臂7)/水平 IR(臂9)；臂1/2/8 为同一 holdings-Δ IR 机制的裸/÷sig/反向三变体（按「换常数、同机制变体不计独立」口径 <10） | **✗ 未达** |
| **D2 字段族自测** | 只用了 `insd1_holdings`/`insd1_tradesignificance`/`insd1_price` **3/8 字段**；`insd1_valueeur`/`shares`/`value`/`gvkey`/`currency_code` 本波未测 | **✗ 未达** |
| **D3 矩全家（水平/一阶差/二阶波动/比值 各≥1）** | 水平 ✓（臂3/臂4/臂9）、一阶差 ✓（臂1/2/5/7）、二阶波动 ✓（ts_ir 臂1/2/8/9）、比值 ✓（臂1/4/5/8/9） | **✓ 达（4/4）** |
| **D4 分组轴 ≥2** | **仅 `sector` 一个分组轴**（9/9 全 `group_rank(…, sector)`）；无 bucket / market / industry 等第二轴 | **✗ 未达** |
| **D5 非线性 ≥1** | `group_rank` / `ts_ir` / `sign` / `days_from_last_change` / `ts_backfill` | **✓ 达** |
| **D6 配置 ≥2** | **仅 1 套**：decay0 + nanHandling ON + SUBINDUSTRY + trunc0.08；生产档 decay4/nanOFF 一条未扫 | **✗ 未达** |

⇒ 缺 **D1 / D2 / D4 / D6**（且臂数 9<10 = 探针）⇒ 按 AGENTS §7.6「探针不产生判死」，**不得判死、不得封集、不得作邻接数据集/族的先验**。所有弱读数只在「decay0/nanON/SUBINDUSTRY/单一 sector 轴」这一格内成立。

## §6 近闸候选（ask 口径：S≥1.2 或距任一硬闸 ≤0.4；≤2 条，按 S 降序）

逐条按平台实读限值核对：

- **S≥1.2：无**（最高 0.74，臂9）。
- **距 S 闸（1.58）≤0.4：无**（最接近臂9，差 0.84）。
- **距 F 闸（1.0）≤0.4：无**（最接近臂9 F 0.47，差 0.53）。
- **距 2Y 闸（1.58）≤0.4**：**臂3 `j2agb0d9` 2Y 1.37，差 0.21（本波最近）**；**臂8 `omaYMl3k` 2Y 1.18，差 0.40（边界，≤0.4）**。臂4 `LLKRA1lM` 2Y 1.15 差 0.43、臂1 1.16 差 0.42 —— **均刚好出 0.4 带**。
- **距本地 sub 线（1.0）≤0.4**：需 sub≥0.6，最高为臂4 0.59（差 0.41）—— **刚好出带**；无满足。
- **CW 0.5 vs 0.10「差 0.4」**：臂1/2/5 机械命中 ≤0.4，但 **CW=0.5 是宽度满值塌缩（结构缺陷）**，且这些臂 sub 为 −0.23/−0.01/−0.15、S 仅 0.60–0.64（距闸 0.94–0.98）；按 prior wave §8 同口径**记「机械命中但无经济含义」，不列入 near**（否则会把负 sub + CW 满值挂闸的臂当可推进件，与「先测 prod」意图相反）。
- **距 TO/margin 带**：9/9 TO 3.2–12.3% 均在 0.01–0.70 内（非挂闸）；margin 低于 5bp 的臂3(0.99bp)/臂7(2.8bp) 是收益层弱，非 RA 硬闸挂项。

⇒ **near 池（按 S 降序，≤2）**：
1. `omaYMl3k` S 0.56 —— 2Y 1.18 距 1.58 闸 0.40（边界）＋ CW 0.2857 超 0.10；但 sub −0.28、DD 21.56%、LC 32（弱）。
2. `j2agb0d9` S 0.07 —— 2Y **1.37 距闸 0.21（最近）**、宽度 139/136、CW/sub pass；但 S 0.07 近平、margin 0.99bp（强度层弱）。

（`LLKRA1lM` 2Y 1.15 差 0.43、`O0W9EZn1` 2Y 1.13 差 0.45 虽是最健康的结构，但**按口径出 0.4 带**，不列入 near，仅在 §2/§9 作绿芽登记。）

## §7 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`**。依据：

1. **探针**：本波仅 **9 臂（<10）** ⇒ 按 ask「探针（<10 条）不产生判死」+ AGENTS §7.6，**不能终判死/封集**。
2. **数据层无排除**：0 条 data_excluded（5 条臂 LC 88–150、pnl 正、TO 正常，§3.3），CW 塌缩归表达层。
3. **信号层弱但非死**：best S 0.74 / best 2Y 1.37，`insd1_holdings` 水平 IR 核心是活体（§2.1-1）；弱≠死。
4. **六维 D1/D2/D4/D6 未达**（§5）⇒ 不得作邻接集先验。
5. **DB 侧一致**：`mcp__wqb-db__get_dead_datasets("DEU")` 返回 **19 个判死集，不含 `insiders1`**（含 `insider_trx_matrix`，是不同数据集）。
6. **单集路线封顶只记路线层**：BE176 已把 insiders1 **单数据集（ATOM）** 上限收敛在 1.0–1.30（三波 1.22/1.30/1.19），本波 9 臂 0.07–0.74 **全部低于该带** ⇒ 记「ATOM 单集路线 capped（勿再重复扫同集同构窗）」的**路线级排除**，**不改写数据集终态**（数据集可继续用于合法跨集形态，只是不得把「insiders1 单集冲 1.58」当活路）。

**波 verdict = `PARTIAL`**（判定表 `src/wqb/wave_results_contract.py:79-90` / `verdict_from_counts`：PASS=≥1 达标 / PARTIAL=0 达标但 ≥1 近闸 / FAIL=0 达标 0 近闸）。本波 **n_pass=0 / n_near=2** ⇒ **PARTIAL**，未自造枚举值。

- **稳健性**：该 PARTIAL 依赖 2Y 近闸带；把 2Y 距离阈值收紧到 <0.4（严格小于）则仅臂3（0.21）入带，仍 ≥1 near ⇒ 结论不变（仍 PARTIAL）。若把「近闸」只认 S/F 强度闸，则本波退为 FAIL —— 但 ask 口径明确「距任一硬闸 ≤0.4」，2Y 是硬闸，故按 PARTIAL。
- **不是「全灭到无信息」**：best S 0.74 / 9/9 S>0（0.07–0.74）、臂4 DD 仅 5.46%、臂3 2Y 1.37，是「真实但远不到 S/F 闸」的弱信号。

## §8 newLever 登记 + 证据通道 / 盲区

**newLever = 空串（本波不入册新杠杆）**。理由：

1. **唯一单变量对照（÷tradesignificance，臂1 vs 臂2）是单波内、量小且 sub 净损**（S/F/2Y 微升、sub −0.22），非跨波实证。
2. **「水平 IR > Δ 核」（臂9 vs 臂1，S +0.10/F +0.10/sub +0.58/CW pass）也是单波内对照**，缺跨波裸对照，不入册。
3. 入册需「**跨波实证 + 裸 vs 改造对照**」，本波两条都不满足 ⇒ 空串。

**本轮实跑核验（只读）**：
- `mcp__wq-brain-http__batch_get_alpha_metrics(9 ids)`：9/9 success，S/F/2Y/sub/TO/DD/margin/`failed_ra_count` 与 ask 转录逐值一致。
- `mcp__wq-brain-http__get_alpha_details` ×9：逐臂取回 `code`/`settings`（9/9 同一探针档）/`metrics`（含 longCount/shortCount）/`ra.ra_failed_checks`/`checks.fail`（含 value·limit·date）/`pyramids.list`（9/9 = DEU/D1/INSIDERS×1.6，eff 1）。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-atom-w1, insiders1)`：9 条，`alpha_id`/`expression` 与臂表**逐条同序同值**，`atom_flag=atom`、`atom_n_datasets=1`（9/9 纯 ATOM）。
- `mcp__wqb-db__get_wave_result(DEU, rt-insiders-atom-w1)`：**未找到**（本档为首次写入）。
- `mcp__wqb-db__get_dead_datasets("DEU")`：19 集，不含 `insiders1`。

**盲区（如实登记，不猜不补）**：
1. **翻符号对照未测**（0 条反号臂）⇒ 方向层结论不可下（§3.1-①）。
2. **decay4/8 未扫**（仅 decay0）⇒ 配置层死/活未判（D6，§3.1-③）。
3. **无 bucket/费率分桶**（仅 sector 单轴）⇒ 分组轴信息量不可判（§3.1-⑤、D4）。
4. **无裸单腿对照**：price(臂4)/新鲜度(臂6)/Δ66(臂5) 均缺「裸」同核对照 ⇒ 无法把各自读数归因于壳层还是轴本身。
5. **self/prod 相关性全 null**：按分工归相关性员，本档不测、不猜；near 候选的 prod 需下一步单独测。
6. **年度分年未取**：未跑 `get_alpha_yearly_stats`；十年跨度只在全期指标层评估。
7. **D2 字段族未覆盖**：`valueeur`/`shares`/`value` 本波未测（FIELD 档已测过，但本波自身不成立）。
8. `create_multi_simulation` 不暴露 start/end，平台回显 2014-01-01→2023-12-31（与 settings.json 2013-01-01 不同）—— 原样记录平台值，不作推断。

## §9 终态

- **波**：`PARTIAL`（0 达标 / 2 近闸）；best S **0.74**（`O0W9EZn1`）/ best 2Y **1.37**（`j2agb0d9`）/ best F 0.47 / best sub 0.59（`LLKRA1lM`）/ best DD 5.46%（`LLKRA1lM`）。
- **数据集**：`insiders1` = **provisional**（不判死、不 data_excluded、不封集）。ATOM 单集路线**已由 BE176 封顶 1.0–1.30**（路线级排除，本波 9 臂全部低于该带，未重复该路线）。
- **塔位**：INSIDERS **9/9 臂归属**（单塔 ×1.6，eff 1），**实际点亮 0**。
- **绿芽（活体结构，留给下一波）**：
  1. `O0W9EZn1` 水平 IR ÷ significance（S 0.74/F 0.47，3 挂、无 CW/sub fail、宽度 88/132）—— 本波最强最干净核心；
  2. `LLKRA1lM` 价格位置比率（sub 0.59/DD 5.46%/宽度 140·150）—— 低回撤健康件，缺 margin/收益；
  3. `j2agb0d9` 纯 significance 水平 2Y 1.37（近闸锚，宽度/回撤健康）。
- **提交链**：**未推进**（0 达标；near 件 prod/self 未测）。
- **下一步（按优先级）**：
  1. **不再重复 insiders1 单集同构窗扫**（BE176 三波 + 本波 9 臂均低于 1.0–1.30 封顶带，重复无增量）；
  2. 若要继续本集，先把 **near 候选的 prod 相关性**测了（arm8/arm3；prod 雷在核心不在搭档），再决定是否扫参；
  3. 补 **D4 第二分组轴**（industry/market/bucket）与 **D6 生产档**（decay4/nanOFF），否则无法区分「配置层死 vs 信号层死」；
  4. 补 **翻符号对照臂**（θ → −θ）与**裸单腿对照**（price/新鲜度/Δ66），否则方向与壳层贡献永远分不开；
  5. 若走跨集，只许 gating/grouping/residual/ratio 四形态（AGENTS §7.7），且第二腿不得用 PV/MODEL/OTHER 类。
