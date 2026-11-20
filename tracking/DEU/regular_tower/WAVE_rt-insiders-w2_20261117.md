# WAVE rt-insiders-w2 — `insiders1` 逐臂归因（DEU/TOP500/D1，第二批 10 臂，2026-11-17）

- 日期：2026-11-17；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集 / 目标塔：`insiders1`（塔 **INSIDERS**）；**纯 ATOM 单集**（DB `atom_flag=atom` 10/10），无第二数据集腿
- ⚠ **波号沿用**：`rt-insiders-w2` 在 2026-11-16 已有一批（multisim `opjxw6pb4USbZxCLVgrUEf`，5 atom + 5 配对 institutions6、UNITS 已修干净、best 0.89、verdict=PARTIAL、newLever 已入册「conc×fresh 乘法」，见 DB 行 id 2230）；本档是**同波号第二批**（multisim `3MvErzaEX4WGbduaOPRI6sD`），DB 行按 merge 语义由本批更新。
- 配置（`get_alpha_details` 10/10 逐臂回显一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=**0**、truncation=0.08、nanHandling=**ON**、maxTrade=OFF、FASTEXPR、`startDate=2014-01-01`、`endDate=2023-12-31` —— 探针口径，生产档（decay4/nanOFF）三波未扫，读数只在 decay0/nanON 档内比较。
- 派发/收割（ask 转录，本档未重跑派发）：查重（11-16 旧表 10 条与本轮无一全同）；`preflight_expressions` valid=true / unknown_fields=[]（insd1_holdings/insd1_valueeur 2 字段在位）；`operator_audit` safe=true（group_neutralize/group_zscore 实测在位）；`create_multi_simulation` 一次 10 臂；`batch_status` 第 2 次 10/10 COMPLETE errors=0；`harvest_multisim_alphas` 一次成功；`upsert_backtest_rows` n=10（带 checks 原文）。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0（平台 LOW_SUB 限值逐臂动态，本批实读 0.04–0.55）/ TO 0.01–0.70 / margin≥5bp / CW≤0.10（平台 limit）/ failed_ra_count=0 且 checks.fail=[] / self·prod<0.70（未测 null，归相关性员）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

本表 10/10 臂经 `mcp__wq-brain-http__get_alpha_details` 逐臂实读复核，与 ask 转录**逐值一致**；表达式与 `mcp__wqb-db__list_expressions(DEU, rt-insiders-w2)` 的 2026-11-17T21:42:28 批次（id 110277–110286）逐条同序同值。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔 | RA fail（平台 checks.fail） |
|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|
| 1 | `1YWg036Q` | IR÷(conc+0.5) `group_rank(divide(ts_ir(vec_avg(holdings),66), add(ts_sum(conc66),0.5)),sector)` | **1.01** | **0.80** | 1.09 | 0.27 | 9.06% | 12.42% | 17.34bp | 60/124 | INSIDERS eff1 | 4：LOW_SHARPE(1.01/1.58), LOW_FITNESS(0.8/1.0), LOW_SUB(0.27/0.48), LOW_2Y(1.09/1.58) |
| 2 | `A1x3EXqX` | IR÷离散度 `group_rank(divide(ts_ir(holdings,66), ts_sum(vec_stddev(ve)/add(vec_sum(ve),1e-4),66)),sector)` | 0.75 | 0.52 | 1.13 | 0.00 | 8.71% | 17.40% | 13.97bp | **53**/117 | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.0/0.36), LOW_2Y |
| 3 | `88NLXWk7` | 同臂1 核、壳换 `group_zscore(,sector)`（无 +0.5） | 0.11 | 0.03 | −0.40 | 0.06 | 16.04% | **39.66%** | 1.89bp | **24/36** | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, **CW 0.260904/0.1@2014-12-11**, LOW_2Y（sub 平台 pass） |
| 4 | `XgaKMZwb` | Δ(mean66)÷conc `group_rank(divide(ts_delta(ts_mean(vec_avg(holdings),66),66), ts_sum(conc66)),sector)` | **1.16** | **1.01（平台 PASS，全战役 insiders1 系首次）** | 0.98 | 0.26 | 9.81% | **10.50%** | 19.31bp | 61/122 | INSIDERS eff1 | 4：LOW_SHARPE(1.16/1.58), **CW 0.5/0.1@2014-01-29**, LOW_SUB(0.26/0.55), LOW_2Y |
| 5 | `mLaXQn2W` | 臂1 结构、窗 66→**126**（去 +0.5） | 0.85 | 0.57 | 1.16 | 0.06 | 5.61% | 17.60% | 19.82bp | 77/131 | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.06/0.4), LOW_2Y |
| 6 | `A1x3EXYd` | 臂2 结构、窗 66→**126** | 0.66 | 0.39 | **1.27** | −0.11 | 5.37% | 20.31% | 16.44bp | 70/129 | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(−0.11/0.31), LOW_2Y |
| 7 | `1YWg031J` | w1 `akaOL28W` 同核 + `group_zscore(,market)` 外层 | **1.01** | **0.80** | 1.09 | 0.26 | 9.12% | 12.49% | 17.31bp | 60/124 | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.26/0.48), LOW_2Y |
| 8 | `gJa3LNwQ` | 离散度裸单腿 `rank(ts_sum(vec_stddev(ve)/add(vec_sum(ve),1e-4),66))` | 0.74 | 0.46 | 0.61 | **0.41（平台 PASS）** | 4.14% | 14.32% | **23.71bp** | 99/139 | INSIDERS eff1 | **3（全波最少）**：LOW_SHARPE, LOW_FITNESS, LOW_2Y |
| 9 | `YPaAY3nJ` | holdings 裸水平 `group_neutralize(ts_zscore(ts_backfill(vec_avg(holdings),252),66),subindustry)` | 0.09 | 0.02 | 0.11 | −0.13 | **25.10%** | 29.83% | 0.65bp | **40/43** | INSIDERS eff1 | 5（全波最多）：LOW_SHARPE, LOW_FITNESS, **CW 0.265899/0.1@2014-01-23**, LOW_SUB(−0.13/0.04), LOW_2Y |
| 10 | `Grmo9jYZ` | `multiply(-1, 臂9)` | −0.09 | −0.02 | −0.11 | 0.13 | **25.10%** | 26.35% | −0.65bp | **43/40** | INSIDERS eff1 | 4：LOW_SHARPE, LOW_FITNESS, **CW 0.265899/0.1@2014-01-23**, LOW_2Y |

- **平台 `status`**：10/10 = `UNSUBMITTED`（IS）。
- **本波极值**：best S **1.16**（臂4，全战役 insiders1 系新高，此前 1.01）/ best F **1.01**（臂4，唯一过 F 闸）/ best 2Y **1.27**（臂6）/ best sub **0.41**（臂8，平台 PASS）/ best margin **23.71bp**（臂8）/ 最低 DD **10.50%**（臂4）。
- **0 达标**：10/10 臂 `failed_ra_count` 3–5，**无一条过 RA 全闸**（臂4 F 过但 S/CW/SUB/2Y 四闸挂）。

### §1.1 平台实读限值

| 闸 | 平台实读 limit | 备注 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10） | ask 判读基准即此（1YWaRlJm fail payload 同值） |
| LOW_FITNESS | **1.0** | 臂4 value 1.01 进 `checks.pass` |
| LOW_2Y_SHARPE | **1.58** | 全臂挂 |
| CONCENTRATED_WEIGHT | **0.10**；臂3 0.260904@2014-12-11、臂4 0.5@2014-01-29、臂9/10 0.265899@2014-01-23 挂 | 臂4/9/10 挂点均在样本首月（建仓期伪影型）；臂3 在年末 |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂动态** 0.04–0.55：臂1 0.48 / 臂2 0.36 / 臂4 0.55 / 臂5 0.4 / 臂6 0.31 / 臂7 0.48 / 臂9 0.04；臂3/8/10 判 pass | sub≥1.0 是本地 review 线；臂8 sub 0.41 平台 PASS |

## §2 符号指纹逐条（ask 六条）

| # | 判据 | 本波实测 | 结论 |
|---|---|---|---|
| ① | 整式取反 S(−e)≈−S(e) 且 TO/DD/LC 逐位相同=方向层无净信息即停 | **臂9/臂10 镜像对**：S 0.09/−0.09、F 0.02/−0.02、2Y 0.11/−0.11、margin ±0.65bp、pnl ±837,084 严格镜像；TO **0.2510 逐位相同**；LC/SC 40/43 ↔ 43/40 镜像互换；DD 0.2983 vs 0.2635 不同（取反回撤不对称=指标性质，沿 w1批2 口径不作反证）。**\|S\|=0.09≈0** | **双向零净信息 ⇒ 指纹①判停**：holdings 裸水平 zscore+group_neutralize(subindustry) 轴两向皆无信号（轴死）；且 TO 25.10% 全波最高、margin 0.65bp，无残值 |
| ② | 去第二腿回落 1.0–1.30（BE176 上限带） | 纯 ATOM 无第二腿；本波复合读数臂1 **1.01**、臂4 **1.16** 均落在带内；裸分子腿（ts_ir / Δmean）仍未测 | 带内，未破顶未证伪；对照不完整（缺裸分子） |
| ③ | decay0/4/8 对照 | **仅 decay0**（10/10 平台回显）；decay4/8 一条未跑 | **未测**（D6 未达，全战役累计） |
| ④ | LC/SC<60/60 = backfill 假填充 | LC<60 警戒臂：臂2 53/117、臂3 24/36、臂9 40/43；60/61 边界：臂1/4/7 | **本轮实跑 `get_alpha_yearly_stats` ×4**（A1x3EXqX / 88NLXWk7 / YPaAY3nJ / XgaKMZwb）：**全部 10/10 年 LC>0 且 SC>0**、逐年有机增长（臂4 15/44→108/183；臂3 6/7→41/70；臂9 9/9→78/82；臂2 16/45→90/179）⇒ **非 backfill 假填充**，是 insiders1 覆盖逐年增长的真数据 |
| ⑤ | 费率分组正反两桶 | 无 bucket/费率分桶臂（bucket 仅 11-16 旧批臂9 用过） | **N/A 未测** |
| ⑥ | 首臂 S<1.58 或 sub<0.39 即停 | 臂1 S=1.01<1.58 **机械命中**；但收割说明判读「不触发」——臂4 S 1.16>基线 1.01（波内有超基线进展 +0.15）且 F 首次过闸 | 两读法并登：**机械命中 / 实质不触发**（先验对照：`DEU-INSIDER-AGGMATRIX-DEAD` 0.92 属 insider_agg_matrix 集，不外推 insiders1；BE176 带 1.0–1.30——臂4 1.16 在带内但逼近中段） |

**臂1/臂7 近全同对（本波最强复现证据）**：
- **臂7 `1YWg031J` vs w1 `akaOL28W`（同核仅加 market 外层）**：S 1.01/1.01、F 0.80/0.80、2Y 1.09/1.09、sub 0.26/0.26、TO 9.12%/9.12%、DD 12.49%/12.49%、margin 17.31/17.31bp、LC/SC 60/124 同、pnl 8,147,690 vs 8,147,691（差 1€）——**读数逐位相同 ⇒ market 外层对已 sector 分组的核零效应（实测）**，同时构成 w1 核心的跨波复现锚 #2。
- **臂1 vs 臂7（同族差 +0.5 分母正则）**：S/F/2Y/LC 全同，TO 差 0.06pp、margin 差 0.03bp、sub 0.27 vs 0.26 ⇒ +0.5 正则无实质效应（conc 分母 ≫ 0.5）。

## §3 稀释铁律

| 复合/壳层形态 | 读数 | 对照 | 差 | 判定 |
|---|---|---|---|---|
| 臂3 `group_zscore(,sector)` 壳 | 0.11/0.03/2Y −0.40/DD 39.66%/LC 24 | 臂1 同核 `group_rank` 壳 1.01/0.80/1.09/DD 12.42%/LC 60 | **S −0.90** / F −0.77 / TO +6.98pp / DD +27.24pp / LC 60→24 | **稀释实锤（壳低于单腿=稀释）**：zscore 壳在本核上崩溃（薄截面 24/36 + 年度 2017 S −1.63 / 2023 S −1.72 结构不稳）⇒ 该核保留 rank 壳 |
| 臂2 IR÷离散度复合 | 0.75 | 臂8 离散度裸单腿 0.74 | **+0.01 ≈ 0** | 非稀释但**零增益**（对照 w1 conc 分母复合 +0.20）⇒ 分母轴 conc ≫ disp |
| 臂5/臂6 126 慢窗 | 0.85 / 0.66 | 臂1/臂2 同构 66 窗 1.01 / 0.75 | −0.16 / −0.09 | **慢窗损 S**（margin 微升 +2.48bp/+2.47bp 但 sub 0.27→0.06 / 0.00→−0.11 大降） |

- 本波零乘法复合（`multiply` 仅作取反对照）；11-16 旧批的 multiply 复合结论不受影响。
- **无一条复合/壳层形态高于其对应单腿**（臂4 的 1.16 是新分子形态 Δ(mean66)÷conc，不是既有腿的叠加壳；其同族对照臂1 1.01 用的是 ts_ir 分子——两种分子从未同波共测裸版，见 §8）。

## §4 宽度塌缩 / 数据层

- **0 条 data_excluded**：年度分年 4/4 臂 10/10 年 LC/SC>0、无零持仓年；6/10 臂 pnl 为正（+24k~+9.70M）、TO 4.14–25.10% 全部 <70% ⇒ **数据存在且可交易**。
- CW 挂闸 4 臂全部单独登记（与塌缩分开）：臂3 0.260904@2014-12-11（薄截面 24/36 期，表达层）；臂4 0.5@2014-01-29、臂9/10 0.265899@2014-01-23（**挂点均在样本首月** = 建仓期伪影型，与 11-16 旧批臂1 首日尖峰同型；宽度 61/122 等健康非塌缩）。臂9/10 的 CW 与其近零信号并存，轴死是主结论。
- 臂3 DD 39.66% + LC 24/36 是本波最差结构（zscore 壳），表达层。

## §5 塔位判读（点塔相关性）

- 平台 `pyramids` 逐臂实读 **10/10 = DEU/D1/INSIDERS×1.6（effective=1）**、`ra.pyramid_short` 10/10 = `insiders` ⇒ **塔归属 = insiders 10/10 臂**（点塔入口全部成立）。
- **点位 ≠ 点亮**：10/10 臂 RA fail≥1 ⇒ 本批实际点亮 INSIDERS 塔 **0 颗**，塔计数不变。
- 纯 ATOM：无第二塔位申请。

## §6 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`**（维持全战役口径，无终态转换）。依据：

1. **判死六维盘点（本批口径）**：
   | 维 | 现状 | 判定 |
   |---|---|---|
   | D1 结构互异模板 ≥10 | 单波互异机制 **5**（IR÷conc / IR÷disp / Δmean÷conc / disp 裸 / holdings 水平 zscore-GN；臂3/5/6/7/10 为壳/窗/取反变体）；累计战役互异 >10 | 单波 ✗ / 累计 ✓ |
   | D2 字段族自测 | 本波仍 2 信号字段（holdings/valueeur）；**`insd1_shares` 全战役从未实测** | **✗** |
   | D3 矩全家 | 水平 ✓（臂9）、一阶差 ✓（臂4 Δmean66）、二阶波动 ✓（臂1/2/5/6 ts_ir）、比值 ✓（全部 ÷ 构造） | **✓** |
   | D4 分组轴 ≥2 | sector（臂1–6）、**market（臂7，本战役首次）**、subindustry 作 group_neutralize 键（臂9/10） ⇒ **单波 ≥2 达**（但 market 外层实测零增益、bucket 未扫） | **✓**（带零增益注记） |
   | D5 非线性 ≥1 | group_zscore / group_neutralize / ts_zscore / group_rank | ✓ |
   | D6 配置 ≥2 | 全战役仅 decay0/nanON 一套；生产档 decay4/nanOFF 三波未扫 | **✗** |
   ⇒ 缺 **D2、D6**（D1 单波内）⇒ 按 AGENTS §7.6 **不得判死/封集/作邻接集先验**。
2. **数据层无排除**（§4）。
3. **信号层弱但有活体且在逼近**：best 1.16 全战役新高、F 首次过闸（臂4）；仍在 BE176 带 1.0–1.30 内。
4. **DB 侧一致**：`mcp__wqb-db__get_dead_ends(DEU)`（上一 ask 实读）不含 insiders1；`DEU-INSIDER-AGGMATRIX-DEAD` 不外推。
5. 路线层：ATOM 单集路线维持 BE176 封顶 1.0–1.30（臂4 1.16 在带内中段，未破顶）。

**波 verdict = `PARTIAL`**（判定表 `src/wqb/wave_results_contract.py:79-90` / `verdict_from_counts`：n_pass=0 / **n_near=2**）：

- **臂4 `XgaKMZwb`（S 1.16）**：CW 0.5 vs limit 0.1 **差 0.40（≤0.4 边界机械命中）**，但挂点 2014-01-29 样本首月、宽度 61/122 健康、DD 10.50% 全波最低 ⇒ 可修单日伪影非塌缩（与 w1 批「负 Sharpe 塌缩臂不列」的排除逻辑相反面：本臂是全波最强结构）；F 闸已过；S 距闸 0.42 临界出带；sub 0.26 距平台动态限 0.55 差 0.29（≤0.4）、距本地线 1.0 差 0.74。
- **臂1 `1YWg036Q`（S 1.01）**：F 0.80 距 F 闸 1.0 **0.20 ✓**（与 w1 `akaOL28W` 同格）；S 距闸 0.57、2Y 距闸 0.49、sub 距平台限 0.48 差 0.21。
- **臂7 `1YWg031J`（S 1.01）**：与臂1 同格同读数（market 零效应孪生），因 ≤2 名额不单列，登记为同格。
- **机械命中但出名额（如实登记）**：臂6 `A1x3EXYd` 2Y 1.27 距 1.58 闸 **0.31（≤0.4）**——但 S 0.66 排序在臂4/臂1 之后，按「≤2 条按 S 降序」出名额；臂2 2Y 1.13 距闸 0.45 出带。
- **稳健性**：若近闸只认 S/F/2Y 强度闸，n_near=1（臂1 F 0.20）⇒ 仍 PARTIAL；**判定对 sub 口径不敏感**。
- ⚠ 本行 (DEU, rt-insiders-w2) verdict 维持 PARTIAL（11-16 批 n_near=2 → 本批 n_near=2，枚举不变）；11-16 批结论保留在旧 findings。

## §7 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

1. `XgaKMZwb`（S 1.16）：全战役 insiders1 系新高、F 平台 PASS、DD 10.50% 最低；触发 = CW 差 0.40@2014-01-29（建仓期伪影可修）+ sub 距平台动态限 0.29。**先测 prod/self**（归相关性员；prod 雷在核心不在搭档）。年度 2017 S −0.36 / 2020 S −0.81 两年负——推进前须按十年纪律复核。
2. `1YWg036Q`（S 1.01）：F 0.80 距闸 0.20（唯一入带强度缺口）；与 w1 `akaOL28W` 近全同 ⇒ prod 若已测过 akaOL28W 可直接复用结论（相关性员槽位）。

## §8 newLever 登记

**空串**。候选逐一核对：
1. **Δ(mean66)÷conc 分子形态**（臂4 1.16 > 臂1 ts_ir 分子 1.01，Δ+0.15）：单波内、且两种分子（ts_ir vs Δ-of-mean）的**裸版从未在任何波跑过** ⇒ 归因对照不完整，不入册。
2. IR÷conc 复合增益（w1 +0.20）：仍缺裸分子腿（全战役盲区延续），且本波臂1/臂7 读数与 w1 全同=复现而非新证。
3. market 外层 / +0.5 正则 / 126 慢窗 / zscore 壳 / disp 分母复合：全部零增益或负向（排除性结论，非杠杆）。
⇒ 无满足「跨波实证 + 归因对照（裸 vs 改造）」的新杠杆。

## §9 绿芽 / 死轴 / 终态

**绿芽（活体结构）**：
1. `XgaKMZwb` Δ(mean66)÷conc（S 1.16 新高 / F 1.01 平台过闸 / DD 10.50% 最低 / 年度宽度有机增长）——全战役最强 insiders1 系结构；短板 CW 首月尖峰、sub 0.26、2017/2020 两年负。
2. `1YWg036Q` / w1 `akaOL28W` / `1YWg031J` 同族三复现（读数互差 ≤0.07bp/0.06pp）——IR÷conc 家族读数高度可复现，F-gap 0.20 是最近强度缺口。
3. `gJa3LNwQ` 离散度裸单腿（sub 0.41 全波最高且平台 PASS / margin 23.71bp 全波最高 / RA 3 全波最少 / LC 99/139 健康）——**sub 目标函数下的最优形态**。
4. `mLaXQn2W` 126 窗（margin 19.82bp、2Y 1.16）——margin/sub 权衡观察点，低优先级。

**死轴**：
1. holdings 裸水平 zscore+group_neutralize(subindustry)：臂9/10 镜像 |S|=0.09（指纹①判停），TO 25.10% 最高 —— 双向皆无信号。
2. `group_zscore(sector)` 壳：0.11 vs 同核 rank 壳 1.01（−0.90 稀释 + DD 39.66%）—— 壳层死，保留 rank 壳。
3. 126 慢窗：两族同向损 S（−0.16/−0.09）且 sub 大降 —— S 轴随窗变慢单调变差。
4. IR÷离散度复合：Δ+0.01 零增益（弱于 conc 分母 +0.20）—— 分母轴 conc ≫ disp（disp 裸腿仍有 sub 价值，见绿芽 3）。

**终态**：
- 波 **PARTIAL**（0 达标 / 2 近闸）；best S **1.16**（`XgaKMZwb`）/ best 2Y **1.27**（`A1x3EXYd`）/ best F **1.01 平台过闸**（臂4）。
- 数据集 `insiders1` = **provisional**；ATOM 路线维持 BE176 封顶（1.16 在带内未破顶）。
- 塔：INSIDERS **10/10 臂归属**，**实际点亮 0**。
- 提交链**未推进**（0 达标；near 件 prod/self null）。
- **取证：不需要新论坛取证**（卡点 = 配置轴与 sub/CW 伪影，本地可行动；fieldscan 8/8 字段 + 9 篇 paper recon 存量在案）。

**下一步（按优先级）**：
1. near 件先测 prod/self（XgaKMZwb 优先；若 akaOL28W/1YWg036Q 已测可直接迁移结论）；
2. 补裸分子对照：`group_rank(rank(ts_delta(ts_mean(vec_avg(insd1_holdings),66),66)),sector)` 与 `rank(ts_ir(vec_avg(insd1_holdings),66))` —— 把臂4 的 +0.15 与臂1 的 +0.20 归因坐实（分子贡献 vs 除法壳层）；
3. 配置维补生产档 decay4/nanOFF（D6，全战役欠账）；
4. 补 `insd1_shares` 字段族（D2 最后一个未测信号字段，ARMTABLE A4 单变量设计可用）；
5. CW 首月伪影修复线：臂4 类结构加 `trade_when` 或样本首月截断类守卫，验证 CW 0.5→≤0.1 后 S 是否保持 ≥1.16；
6. 不再重复：holdings 裸水平 zscore±GN（双向 0.09）、zscore 壳（稀释 0.90）、126 慢窗（两族同向损 S）、market 外层（零效应）、+0.5 分母正则（零效应）。

## §10 证据通道与盲区

**实跑核验（本档，全部只读）**：
- `mcp__wq-brain-http__get_alpha_details` ×10（10/10 success）：code/settings/metrics/ra/checks.fail（value·limit·date）/checks.pass/pyramids.list 逐臂取回，与 ask 转录逐值一致；pyramids 10/10 = DEU/D1/INSIDERS×1.6 eff1；臂4 LOW_FITNESS 在 checks.pass（value 1.01）。
- `mcp__wq-brain-http__get_alpha_yearly_stats` ×4（XgaKMZwb / 88NLXWk7 / YPaAY3nJ / A1x3EXqX）：指纹④查证（§2-④）。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w2)`：20 条（11-16 批 id 109740–109749 + 本批 110277–110286 与臂序同序同值，atom_flag=atom 10/10）。
- `mcp__wqb-db__get_wave_result(DEU, rt-insiders-w2)`：读得 id 2230（11-16 批 PARTIAL 版，19 条 key_findings 在案——本批落库时原样保留）。
- 判定表已读：`src/wqb/wave_results_contract.py:79-90`。
- 上一 ask 实读存档引用：`get_dead_ends(DEU)` 无 insiders1；w1 批2 档案（akaOL28W 读数与年度分年）。

**盲区（如实登记，不猜不补）**：
1. decay4/8 与 nanOFF 未扫（D6，全战役三波欠账）。
2. 裸分子对照缺失（ts_ir 裸 / Δmean 裸从未跑）⇒ 臂4/臂1 的增益归因不完整（newLever 因此为空）。
3. `insd1_shares` 未测（D2）。
4. prod/self 全 null（归相关性员）；near 件的 prod 未测。
5. 年度分年仅 4 臂（指纹④警戒臂+近闸臂）；其余 6 臂未逐年核。
6. bucket/费率分桶未测（指纹⑤ N/A）；bucket 分组轴全战役仅 11-16 旧批 1 条。
7. CW 首月伪影成因未验（臂4/9/10 挂点均在 2014-01；11-16 旧批臂1 同型）。
8. 波号复用：本批与 11-16 批共用 wave 号 rt-insiders-w2，DB 行两批 findings 并存、verdict 维持 PARTIAL——两批读数以各自档案为准。
