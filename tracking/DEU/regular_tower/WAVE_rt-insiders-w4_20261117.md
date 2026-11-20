# WAVE rt-insiders-w4 — `insiders1` 逐臂归因（DEU/TOP500/D1，第二批 10 臂，2026-11-17）

- 日期：2026-11-17；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集 / 目标塔：`insiders1`（塔 **INSIDERS**）；**纯 ATOM 单集**（DB `atom_flag=atom` 10/10），无第二数据集腿
- ⚠ **波号沿用**：`rt-insiders-w4` 在 2026-11-16 已有一批（multisim `16sDwR4al4DY9pWCuwiSHey`，ts_ir 窗宽/事件条件/机构持股斜率三轴，best 0.89、best sub 0.68、best margin 62.63bp，verdict=PARTIAL，17 条 findings，见 DB 行 id 2239）；本档是**同波号第二批**（multisim `2SBhbD8Du4RR8xqptQnTNuX`），DB 行按 merge 语义由本批更新。
- 配置（`get_alpha_details` 10/10 逐臂回显一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=**0**、truncation=0.08、nanHandling=**ON**、maxTrade=OFF、FASTEXPR、`startDate=2014-01-01`、`endDate=2023-12-31` —— 探针口径，生产档（decay4/nanOFF）五波未扫，读数只在 decay0/nanON 档内比较。
- 派发/收割（ask 转录，本档未重跑派发）：查重（11-16 旧表 10 条与本轮无一全同）；`preflight_expressions` valid=true / unknown_fields=[]（holdings/shares/tradesignificance/valueeur 4 字段在位）；`operator_audit` safe=true；`create_multi_simulation` 一次 10 臂；`batch_status` 首轮 10/10 COMPLETE errors=0；`harvest_multisim_alphas` 一次成功；`upsert_backtest_rows` n=10（带 checks 原文）。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0（平台 LOW_SUB 动态）/ TO 0.01–0.70 / margin≥5bp / CW≤0.10（平台 limit）/ failed_ra_count=0 且 checks.fail=[] / self·prod<0.70（未测 null，归相关性员）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

本表 10/10 臂经 `mcp__wq-brain-http__get_alpha_details` 逐臂实读复核，与 ask 转录**逐值一致**；表达式与 `mcp__wqb-db__list_expressions(DEU, rt-insiders-w4)` 的 2026-11-17T23:33 批次（id 110378–110387）逐条同序同值。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔 | RA fail（平台 checks.fail） |
|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|
| 1 | `RRepnnqn` | **Δmean66+bf250**÷shares-IR-avg，sector（CW 修复对照） | 0.95 | 0.65 | 0.35 | 0.17 | **6.03%** | 9.93% | 19.42bp | 96/130 | INSIDERS eff1 | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.5/0.1@2014-01-29**, LOW_SUB(0.17/0.45), LOW_2Y |
| 2 | `npagMMYq` | **av_diff+bf250**÷shares-IR-avg，sector | 0.73 | 0.43 | 0.76 | 0.40 | 10.60% | 12.28% | 8.11bp | 101/133 | INSIDERS eff1 | **3（健康臂最少）**：LOW_SHARPE, LOW_FITNESS, LOW_2Y（**CW+LOW_SUB pass**） |
| 3 | `xAvx00Qg` | Δmean66÷**shares-IR-max**，sector | 1.26 | 1.14 | **1.06** | 0.31 | 10.24% | 10.87% | 19.95bp | 61/122 | INSIDERS eff1 | 4：LOW_SHARPE(1.26/1.58), **CW 0.5@2014-01-29**, LOW_SUB(0.31/0.6), LOW_2Y（F pass） |
| 4 | `VkNpggE0` | Δmean66÷**shares-IR-sum**，sector | **1.28** | **1.17** | 1.05 | 0.35 | 10.22% | 11.29% | **20.46bp** | 61/122 | INSIDERS eff1 | 4：LOW_SHARPE(1.28/1.58), **CW 0.5@2014-01-29**, LOW_SUB(0.35/0.61), LOW_2Y（F pass） |
| 5 | `d5axAA7E` | Δmean66÷**valueeur-IR-avg**，sector | **1.28** | 1.16 | 1.03 | **0.38** | 10.12% | 10.25% | 20.43bp | 61/122 | INSIDERS eff1 | 4：LOW_SHARPE(1.28/1.58), **CW 0.5@2014-01-29**, LOW_SUB(0.38/0.61), LOW_2Y（F pass） |
| 6 | `Jj8pZZX2` | **裸 shares-IR-max** `rank(ts_ir(bf(vec_max(shares),250),66))` | 0.09 | 0.02 | −0.44 | 0.48 | 10.35% | 24.20% | 1.17bp | 61/62 | INSIDERS eff1 | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y（CW+LOW_SUB pass；sub 0.48 来自近零 S 退化结构不可用） |
| 7 | `vRAL33Jz` | Δmean66÷(shares-IR-avg**+0.5**)，sector | 1.22 | 1.08 | 0.98 | 0.31 | 10.12% | 10.81% | 19.43bp | 61/122 | INSIDERS eff1 | 4：LOW_SHARPE(1.22/1.58), **CW 0.5@2014-01-29**, LOW_SUB(0.31/0.58), LOW_2Y（F pass） |
| 8 | `QP0aLL5g` | Δmean66÷**shares-ts_rank**，sector | 1.17 | 0.96 | 0.94 | 0.23 | **13.98%** | 10.22% | 13.54bp | 61/122 | INSIDERS eff1 | 5：LOW_SHARPE, LOW_FITNESS(0.96/1.0), **CW 0.5@2014-01-29**, LOW_SUB(0.23/0.55), LOW_2Y |
| 9 | `Xgap552X` | Δmean66÷**tradesignificance 裸水平(bf250)**，sector | 1.18 | 1.03 | 0.95 | 0.24 | 9.98% | 11.43% | 19.14bp | 61/122 | INSIDERS eff1 | 4：LOW_SHARPE(1.18/1.58), **CW 0.5@2014-01-29**, LOW_SUB(0.24/0.56), LOW_2Y（F pass） |
| 10 | `E5QwXXgR` | **正向 disp**（ts_mean 壳）`rank(ts_mean(disp66))` | 0.31 | 0.14 | −0.33 | −0.54 | 8.99% | 23.39% | 5.86bp | **54/53** | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(−0.54/0.15), LOW_2Y（CW pass） |

- **平台 `status`**：10/10 = `UNSUBMITTED`（IS）。
- **本波极值**：best S **1.28**（臂4/臂5 并列，全战役新高：w3 1.27 → +0.01）/ best F **1.17**（臂4；全波 5 条 F 平台 pass：臂3/4/5/7/9）/ best 2Y **1.06**（臂3）/ 健康臂 best sub **0.38**（臂5）/ best margin 20.46bp（臂4）。
- **0 达标**：10/10 臂 `failed_ra_count` 3–5，**无一条过 RA 全闸**（5 条 F pass 但 S/CW/SUB/2Y 挂）。

### §1.1 平台实读限值

| 闸 | 平台实读 limit | 备注 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10） | ask 判读基准即此 |
| LOW_FITNESS | **1.0**；臂3 1.14 / 臂4 1.17 / 臂5 1.16 / 臂7 1.08 / 臂9 1.03 进 `checks.pass` | **本波 5 条过 F 闸**（战役单波最多；此前 w2 1 条、w3 2 条） |
| LOW_2Y_SHARPE | **1.58** | 全臂挂 |
| CONCENTRATED_WEIGHT | **0.10**；挂闸 7 臂（臂1/3/4/5/7/8/9，value 0.5@2014-01-29）；臂2/6/10 pass | 挂闸 7 臂全部是 **ts_delta(ts_mean) 分子形态**（bf250 有无不论）；pass 的 3 臂 = av_diff+bf250 / 裸 IR / 裸 disp |
| LOW_SUB_UNIVERSE_SHARPE | 逐臂动态；臂2/6 判 pass | sub≥1.0 是本地 review 线 |

## §2 符号指纹逐条（ask 六条）

| # | 判据 | 本波实测 | 结论 |
|---|---|---|---|
| ① | 整式取反 S(−e)≈−S(e) 即停 | **跨波镜像对**：臂10 正向 disp（ts_mean 壳）S **+0.31** vs w3 批2 臂8 `reverse(disp)` −0.31：S/F/2Y/sub/margin/pnl 全镜像（pnl ±2,717,867/±2,717,866）、TO **0.0899 逐位相同**、LC/SC 54/53 ↔ 53/54 镜像互换；DD 0.2339 vs 0.4823 非镜像（取反回撤不对称=指标性质） | **镜像成立且 \|S\|=0.31 有方向信息量 ⇒ 不触发停**；方向读数：disp 正向为正（与 w2 ts_sum 壳裸 disp 0.74 同向）；反向形态死（w3 已记），正向弱活 |
| ② | 去第二腿回落 1.0–1.30 | 纯 ATOM。**臂6 裸 shares-IR-max 0.09**（补 w3 最大归因缺口）⇒ IR 裸腿近零，ratio 结构放大的是**归一化**贡献而非分母信号；臂7 裸 count（w3）0.77 同理。**分子裸腿（Δmean66）仍全战役未测** ⇒ 对照缺口收窄至分子侧 | 带内（1.28）；分母侧回落证据成立（0.09/0.77 ≪1.0），分子侧仍未测 |
| ③ | decay0/4/8 对照 | **仅 decay0**（10/10 平台回显）；decay4/8 五波未跑 | **未测**（D6 未达，全战役累计；本波是距闸最近的一波，D6 成了唯一能区分「配置层 vs 信号层」的未测轴） |
| ④ | LC/SC<60/60 = backfill 假填充 | ⚠ **ask 读数自相矛盾更正**：收割说明称「LC<60 无（最低臂10 54/53）」——54/53 **双侧均 <60**，机械判据实际命中臂10。**本轮实跑 `get_alpha_yearly_stats` ×3**（E5QwXXgR / VkNpggE0 / d5axAA7E）：**全部 10/10 年 LC>0 且 SC>0**、有机增长（臂10 27/27→77/75；臂4 15/44→112/183；臂5 15/43→110/183）⇒ **非 backfill 假填充** | 假填充排除（实测裁决）；臂10 年度弱信号但真数据（2017 −1.08 / 2022 −0.42 / 2023 −0.22） |
| ⑤ | 费率分组正反两桶 | 无 bucket/费率分桶臂 | **N/A 未测** |
| ⑥ | 首臂 S<1.58 或 sub<0.39 即停 | 臂1 S=0.95<1.58 **机械命中**；臂4/5 1.28>基线 1.27（战役新高）且 5 条 F pass ⇒ 波内有进展 | 两读法并登：**机械命中 / 实质不触发**；AGGMATRIX-DEAD 0.92 不外推 |

## §3 通道判读（本波四个单变量轴）

### 3.1 CW 修复通道：**证伪**（本波最重要的负结论）

| 臂 | 分子形态 | CW | S |
|---|---|---|---:|
| 臂1 `RRepnnqn` | Δmean66 **+ bf250** | **0.5 挂 @2014-01-29** | 0.95（vs 无 bf 基线 A1x3AN0l 1.27，**−0.32**） |
| 臂2 `npagMMYq` | **av_diff + bf250** | **pass** | 0.73 |
| w3 臂4 `RRergbme` | av_diff + bf250 ÷ conc | pass | 0.89 |

⇒ w3 批2「下一步②CW 修复对照（Δmean 分子加 ts_backfill）」的假设**证伪**：bf250 修不掉 Δmean 的 CW（仍 0.5@首月），且压掉新鲜度使 S −0.32、TO 6.03% 暴降。**CW 伪影绑定 `ts_delta(ts_mean(·))` 分子形态本身**（bf 有无不改）；CW-clean 的唯一出口是 av_diff 系（S 上限 0.89）。**本族「CW pass 且 S≥1.27」的组合不存在**（两臂无一人同时达成）。

### 3.2 分母统计量闭组完成：**轴关闭**

同分子（Δmean66）同壳（group_rank,sector）同配置，vec 统计量梯：

| 分母 | S | 来源 |
|---|---:|---|
| vec_count（事件计数 IR） | 1.23 | w3 批2 臂5 |
| vec_avg | 1.27 | w3 批2 臂6 |
| **vec_max** | 1.26 | 本波臂3 |
| **vec_sum** | **1.28** | 本波臂4 |
| **valueeur-vec_avg** | **1.28** | 本波臂5 |

⇒ **全距 0.05（噪声级）**：分母统计量维度平坦关闭；战役新高 1.28 的 +0.01 是噪声级。臂5 的价值在次级指标：**sub 0.38 健康 sub 新高**（此前 0.32）+ 年度画像最温和（2017 −0.11，get_alpha_yearly_stats 实读）。

### 3.3 分母正则与替代形

- **臂7（+0.5 正则）1.22 vs 臂6/w3臂6（无正则）1.27：Δ−0.05 非零** ⇒ w2「+0.5 正则零效应」锚（conc 分母 ≫0.5）**不适用于 IR 分母**（shares-IR 数值小，正则扰动可观）；修正 w2 结论适用范围：仅对大数值分母成立。
- **臂8（ts_rank 归一分母）1.17**：S −0.10、TO +3.76pp、F 0.96 ⇒ 无增益。
- **臂9（tradesignificance 裸水平分母）1.18/F 1.03**：序数分母可行（距基线 −0.09），**tradesignificance 从「裸水平近零」（w1批2 −0.23）变为「作分母有效」**——该字段的信号不在水平而在归一化用途；单波内不构成杠杆。

### 3.4 归因闭合（w3 遗留缺口的补测）

- 臂6 裸 IR 0.09 + w3 臂7 裸 count 0.77 ⇒ **分母侧回落证据闭合**（两个裸腿都远低于复合 1.23–1.28）；**分子裸腿（Δmean66）是本族最后一个未测对照**（全战役最大归因缺口收窄至分子侧）。

## §4 稀释铁律

- 本波零乘法复合、零 bucket ⇒ 稀释铁律直接对象为零。
- 壳层/正则对照全部 ≥0：+0.5 正则 −0.05、ts_rank 壳 −0.10、bf250 分子 −0.32——**无一条复合/改造高于其裸对照**；本波全部增益方向都来自「分母块替换」（w3 已入册杠杆的闭组收尾）。

## §5 宽度塌缩 / CW / 数据层

- **0 条 data_excluded**：年度分年 3/3 臂 10/10 年 LC/SC>0、8/10 臂 pnl 为正（+0.62M~+10.70M）、TO 6.03–13.98% 全部 <0.70 ⇒ **数据存在且可交易**。
- CW 挂闸 7 臂全部 Δmean 分子形态（bf 有无不改，§3.1）——表达层（首月建仓伪影），与数据层分开登记；臂6 DD 24.20%、臂10 DD 23.39% 是近零/弱信号的路径噪声，非塌缩（LC 61/62、54/53 健康）。

## §6 塔位判读（点塔相关性）

- 平台 `pyramids` 逐臂实读 **10/10 = DEU/D1/INSIDERS×1.6（effective=1）**、`ra.pyramid_short` 10/10 = `insiders` ⇒ **塔归属 = insiders 10/10 臂**（点塔入口全部成立）。
- **点位 ≠ 点亮**：10/10 臂 RA fail≥1 ⇒ 本批实际点亮 INSIDERS 塔 **0 颗**，塔计数不变。
- 纯 ATOM：无第二塔位申请。

## §7 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`**（维持全战役口径）。依据：

1. **判死六维盘点**：D1 累计互异 >10 ✓；**D2 ✓**（w3 批2 首次达成：5 个可测信号字段全部有平台实测）；D3 ✓（水平/一阶差/二阶波动/比值）；D4 ✓（sector/industry/market/subindustry/bucket）；D5 ✓；**D6 ✗（唯一未达维，五波仅 decay0/nanON 一套）** ⇒ 按 AGENTS §7.6 不得判死/封集/作邻接先验。
2. **数据层无排除**（§5）。
3. **信号层爬升收顶**：S 演进 0.81→0.89→1.16→1.27→1.28；分母统计量闭组平坦（§3.2）⇒ **ATOM 单集路线在本配置内收敛于 ≈1.28（= BE176 带 1.0–1.30 上缘）**：分子形态（Δmean/av_diff）、分母字段（valueeur/shares/tradesignificance）、分母统计量（count/avg/max/sum）、正则（+0.5）、分组轴（4 点）、窗轴（22/66/126/252）全部扫过——**剩余 0.30 缺口不在这六个已测维度内**；配置轴（D6）是最后一个未测自由度，测完前不作路线终判。
4. **DB 侧一致**：`get_dead_ends(DEU)`（前 ask 实读）不含 insiders1。
5. 路线层条件：若 D6 档（decay4/nanOFF）读数亦 ≤1.0–1.30，则 ATOM 路线具备正式 capped 证据（两配置 × 全维度）；本波不预判。

**波 verdict = `PARTIAL`**（判定表 `src/wqb/wave_results_contract.py:79-90` / `verdict_from_counts`：n_pass=0 / **n_near=2**）：

- **臂4 `VkNpggE0`（S 1.28）**：S≥1.2 ✓ + 距 S 闸 **0.30 ✓** + CW 0.5 vs 0.1 差 **0.40 ✓**（边界）+ sub 0.35 距平台动态限 0.61 差 0.26 ✓；F 1.17 平台 pass。
- **臂5 `d5axAA7E`（S 1.28 并列）**：同条件（S 距闸 0.30 / CW 0.40 / sub 0.38 距 0.61 差 0.23）；F 1.16 pass。
- **机械命中出名额（如实登记）**：臂3 S 1.26（距闸 0.32 ✓）、臂7 S 1.22（S≥1.2 ✓）、臂8 F 0.96 距 F 闸 **0.04** ✓——均按 S 降序与 ≤2 名额不列。
- **稳健性**：n_near≥1 不依赖任何单一口径 ⇒ PARTIAL 稳健。
- ⚠ 本行 (DEU, rt-insiders-w4) verdict 维持 PARTIAL（11-16 批 n_near=2 → 本批 n_near=2，枚举不变）；11-16 批结论保留在旧 findings。

## §8 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

1. `VkNpggE0`（S 1.28）：全战役并列最高、F 1.17 pass、margin 20.46bp。缺口 = CW 0.5@2014-01-29（Δmean 形态属性，本波证伪 bf250 修复）+ sub 0.35/0.61 + 2Y 1.05。**先测 prod/self**（与臂5 同族，prod 相关性高但仍须按臂分别测）。
2. `d5axAA7E`（S 1.28 并列）：**年度画像最温和（2017 −0.11）+ 健康 sub 新高 0.38**——两并列臂中稳健性画像更优者。

## §9 newLever 登记

**空串（本波不入册新杠杆）**。逐项核对：
1. 分母统计量闭组（count/avg/max/sum/valueeur-avg 1.23–1.28）：**平坦 = 轴关闭**，是排除性结论非杠杆。
2. tradesignificance 序数分母（1.18/F 1.03）：单波内、距基线 −0.09（未超基线），不构成杠杆。
3. +0.5 正则（−0.05）与 ts_rank 壳（−0.10）：负向排除。
4. w3 已入册的「分母通道」杠杆由本波**闭组收尾确认**（无更优分母统计量），不是新证。
⇒ 无满足「跨波实证 + 归因对照」的新增杠杆。

## §10 绿芽 / 死轴 / 终态

**绿芽（活体结构）**：
1. `VkNpggE0` / `d5axAA7E` Δmean66÷IR（S 1.28 并列战役新高 / F pass / 年度宽度有机增长）——**d5axAA7E 稳健画像更优**（2017 −0.11、sub 0.38）；共同短板 CW 首月伪影（形态属性，修复已证伪）与 sub。
2. `npagMMYq` av_diff+bf250÷shares-IR（0.73 / **CW+LOW_SUB 双 pass** / RA 3 健康臂最少 / sub 0.40 健康 sub 次高）——**本波唯一 CW 干净的 Δ 族近亲**（av_diff 系 CW-clean 定律第二次成立）。
3. `Xgap552X` tradesignificance 分母（1.18/F 1.03 pass）——序数分母可行，tradesignificance 字段的第二生命（分母用途）。
4. disp 正向（臂10 +0.31 镜像实测有方向信息）——弱活轴，与 w2 裸 disp 0.74 同向。

**死轴**：
1. bf250-Δmean CW 修复：证伪（CW 仍 0.5 且 S −0.32，§3.1）——**从「下一步」清单移除**。
2. 分母统计量维度：count/avg/max/sum/valueeur-avg 全距 0.05 ⇒ 关闭。
3. +0.5 正则（IR 分母上 −0.05）与 ts_rank 归一分母（−0.10 + TO +3.76pp）：关闭（w2 零效应锚适用范围已修正）。
4. disp 反向（w3 臂8 −0.31）：死；正向弱活（+0.31）。
5. 裸 shares-IR 主信号（0.09）：死（只配当分母）。

**终态**：
- 波 **PARTIAL**（0 达标 / 2 近闸）；best S **1.28**（`VkNpggE0`/`d5axAA7E` 并列）/ best 2Y **1.06**（`xAvx00Qg`）/ best F **1.17 平台过闸**（5 条过闸为战役单波最多）。
- 数据集 `insiders1` = **provisional**；**ATOM 单集路线在本配置内收敛 ≈1.28**（六维已测全，剩 D6 一个自由度）；CW-clean+高S 组合不存在。
- 塔：INSIDERS **10/10 臂归属**，**实际点亮 0**。
- 提交链**未推进**（0 达标；near 件 prod/self null）。
- **取证：不需要新论坛取证**（卡点 = D6 配置档 + prod 测试，全部本地/账号可行动）。

**下一步（按优先级）**：
1. near 件先测 prod/self（VkNpggE0 / d5axAA7E；两条同族，测一条可预估另一条相关性量级但须分别测）；
2. **D6 配置档：生产档 decay4/nanOFF 重跑本族头名（臂4/臂5 结构）**——指纹③判据（decay4 相对 decay0 掉>30% = 快变分量别用）与路线终判（≤1.0–1.30 则 ATOM capped）一次完成；
3. 分子裸腿对照 `group_rank(rank(Δmean66),sector)`（本族最后一个未测对照，把 ratio 结构增益归因闭合）；
4. 若 D6 亦收敛 ≤1.30：ATOM 路线正式 capped，转配对/跨集四形态（gating/grouping/residual/ratio，AGENTS §7.7）；
5. 不再重复：bf250-Δmean CW 修复、分母统计量变体、+0.5 正则、ts_rank 分母、22/126 窗、market/industry/subindustry 轴。

## §11 证据通道与盲区

**实跑核验（本档，全部只读）**：
- `mcp__wq-brain-http__get_alpha_details` ×10（10/10 success）：code/settings/metrics/ra/checks.fail（value·limit·date）/checks.pass/pyramids.list 逐臂取回，与 ask 转录逐值一致；pyramids 10/10 = DEU/D1/INSIDERS×1.6 eff1；臂3/4/5/7/9 LOW_FITNESS 在 checks.pass。
- `mcp__wq-brain-http__get_alpha_yearly_stats` ×3（E5QwXXgR / VkNpggE0 / d5axAA7E）：指纹④查证（§2-④，含 ask 矛盾读数的实测裁决）。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w4)`：20 条（11-16 批 id 109942–109951 + 本批 110378–110387 与臂序同序同值，atom_flag=atom 10/10）。
- `mcp__wqb-db__get_wave_result(DEU, rt-insiders-w4)`：读得 id 2239（11-16 批 PARTIAL 版，17 条 key_findings 在案——本批落库时原样保留）。
- 判定表：`src/wqb/wave_results_contract.py:79-90`（本轮未重读文件，上下文前次 ask 已读，verdict_from_counts 语义不变）。
- 前 ask 实读存档引用：`get_dead_ends(DEU)` 无 insiders1；w1–w3 批2 档案与 DB 行。

**盲区（如实登记，不猜不补）**：
1. decay4/8 与 nanOFF 未扫（D6 唯一缺维；本波后它同时是「路线终判」的最后一轴）。
2. 分子裸腿（Δmean66）未测 ⇒ ratio 结构的分子侧归因仍开放。
3. prod/self 全 null（归相关性员）；near 件的 prod 未测。
4. 年度分年仅 3 臂（臂10/4/5）；其余 7 臂未逐年核。
5. 指纹①本波无同波取反对（跨波镜像对成立但 DD 非镜像，判读口径沿前波）；指纹⑤ bucket 未测。
6. 臂6 sub 0.48 / 臂10 sub −0.54 均为近零/弱 S 退化结构产物，不作 sub 证据。
7. 波号复用：本批与 11-16 批共用 wave 号 rt-insiders-w4，DB 行两批 findings 并存、verdict 维持 PARTIAL——两批读数以各自档案为准。
