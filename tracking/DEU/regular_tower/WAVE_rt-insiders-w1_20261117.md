# WAVE rt-insiders-w1 — `insiders1` 逐臂归因（DEU/TOP500/D1，第二批 10 臂，2026-11-17）

- 日期：2026-11-17；槽：regular_tower（纯本地归因；判读不改写邻接集先验，跨区不外推）
- 主集 / 目标塔：`insiders1`（塔 **INSIDERS**）；**纯 ATOM 单集**（DB `atom_flag=atom`、`atom_n_datasets=1` 10/10），无第二数据集腿
- ⚠ **波号沿用**：`rt-insiders-w1` 在 2026-11-16 已有一批（multisim `2MK3Hr1eg57S8Mv11Wfx5MXF`，5 atom + 5 配对 institutions6、5 臂 UNITS，best 0.81，verdict=FAIL，见 `WAVE_rt-insiders-w1_20261116.md`）；本档是**同波号第二批**（multisim `1TOC1nd9z4C7bMI12RErvgde`）。DB wave_results 行 (DEU, rt-insiders-w1, id 2228) 按 merge 语义由本批更新。
- 配置（`get_alpha_details` 10/10 逐臂回显一致）：DEU/TOP500/D1、neutralization=SUBINDUSTRY、decay=**0**、truncation=0.08、nanHandling=**ON**、maxTrade=OFF、pasteurization=ON、unitHandling=VERIFY、FASTEXPR、`startDate=2014-01-01`、`endDate=2023-12-31` —— 探针口径，与生产档 `tracking/DEU/config/settings.json`（decay4/nanOFF）不同，读数只在 decay0/nanON 档内比较。
- 派发/收割（ask 转录，本档未重跑派发）：`preflight_expressions` valid=true / unknown_fields=[]（insd1_holdings/price/tradesignificance/valueeur 4 字段平台实查在位）；`operator_audit` safe=true / violations=[]；查重 `list_expressions(DEU, rt-insiders-w1)` 既有 11 条 2026-11-16 历史表达式与本轮 10 臂无一全同、无臂跳过；`create_multi_simulation` 一次 10 臂；`batch_status` 第 3 次 10/10 COMPLETE errors=0；`harvest_multisim_alphas` 一次成功（无 404）；`upsert_backtest_rows` n=10（带 checks 原文）。
- 判读基准（ask 给定）：S≥1.58 / F≥1.0 / 2Y≥1.58 / sub≥1.0（平台 LOW_SUB 限值动态，本批实读见 §1.1）/ TO 0.01–0.70 / margin≥5bp / CW≤0.10（平台 limit）/ failed_ra_count=0 且 checks.fail=[] / self·prod<0.70（未测，null，归相关性员）。

## §1 臂序读数表（平台实读，按臂序；勿按 alpha id 猜）

本表 10/10 臂经 `mcp__wq-brain-http__get_alpha_details` 逐臂实读复核，与 ask 转录**逐值一致**；表达式与 `mcp__wqb-db__list_expressions(DEU, rt-insiders-w1)` 的 2026-11-17T20:01:44 批次（id 110207–110216）逐条同序同值。

| # | alphaId | 结构（简） | S | F | 2Y | sub | TO | DD | margin | LC/SC | 塔（pyramids） | RA fail（平台 checks.fail） |
|---|---|---|---:|---:|---:|---:|---|---:|---|---|---|---|
| 1 | `6XMErP2L` | sig 裸水平 `rank(ts_backfill(vec_avg(insd1_tradesignificance),252))` | −0.23 | −0.07 | 0.43 | 0.51 | 7.06% | 27.75% | −3.7bp | 101/88 | INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y |
| 2 | `akaOL28W` | **IR÷集中度复合** `group_rank(divide(ts_ir(vec_avg(insd1_holdings),66), ts_sum(divide(vec_max(insd1_valueeur),add(vec_sum(insd1_valueeur),1e-4)),66)), sector)` | **1.01** | **0.80** | **1.09** | 0.26 | 9.12% | 12.49% | 17.31bp | 60/124 | INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.26/0.48), LOW_2Y |
| 3 | `LLKR9bw9` | Δ66-IR `rank(ts_ir(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66),252))` | 0.35 | 0.17 | 0.24 | 0.07 | 4.52% | 11.62% | 13.31bp | 61/60 | INSIDERS×1.6（eff 1） | 5：LOW_SHARPE, LOW_FITNESS, **CW 0.5/0.1@2014-03-05**, LOW_SUB(0.07/0.17), LOW_2Y |
| 4 | `RRerVZoo` | 集中度裸水平 `rank(ts_sum(divide(vec_max(insd1_valueeur),add(vec_sum(insd1_valueeur),1e-4)),66))` | 0.81 | 0.50 | 0.84 | 0.20 | 4.73% | 13.90% | **20.42bp** | 129/140 | INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.20/0.38), LOW_2Y |
| 5 | `ZYao0wvY` | sign 频率 `rank(ts_sum(sign(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),1)),66))` | 0.00 | 0.00 | −0.55 | −0.11 | 12.98% | 20.44% | 0.4bp | 96/98 | INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(−0.11/0.0), LOW_2Y |
| 6 | `WjlgPw2k` | `multiply(-1, 臂5)` | −0.00 | −0.00 | 0.55 | 0.11 | 12.98% | 25.50% | −0.4bp | 98/96 | INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y |
| 7 | `kqaKVk6K` | 新鲜度÷sig `group_rank(divide(subtract(252,days_from_last_change(ts_backfill(vec_avg(insd1_holdings),252))), ts_mean(vec_avg(insd1_tradesignificance),66)), sector)` | 0.74 | 0.46 | 0.54 | 0.11 | 5.98% | 13.05% | 16.49bp | 112/155 | INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.11/0.35), LOW_2Y |
| 8 | `O0W9rwXd` | 价格位置 `rank(divide(ts_backfill(vec_avg(insd1_price),250), ts_mean(ts_backfill(vec_avg(insd1_price),250),250)))` | 0.63 | 0.34 | 0.21 | **0.63** | 8.51% | **7.72%** | 8.47bp | 109/109 | INSIDERS×1.6（eff 1） | 3：LOW_SHARPE, LOW_FITNESS, LOW_2Y（CW+LOW_SUB pass） |
| 9 | `88NL3kWo` | `multiply(-1, 臂8)` | −0.63 | −0.34 | −0.21 | −0.63 | 8.51% | 39.35% | −8.47bp | 109/109 | INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(−0.63/−0.3), LOW_2Y |
| 10 | `58JvQ7KN` | 新鲜度 ts_rank `ts_rank(subtract(252,days_from_last_change(ts_backfill(vec_avg(insd1_holdings),252))),252)` | 0.64 | 0.36 | 0.47 | 0.15 | 10.92% | 11.55% | 7.07bp | 107/135 | INSIDERS×1.6（eff 1） | 4：LOW_SHARPE, LOW_FITNESS, LOW_SUB(0.15/0.3), LOW_2Y |

- **平台 `status`**：10/10 = `UNSUBMITTED`（IS）。
- **本波极值**：best S **1.01** / best F **0.80** / best 2Y **1.09**（三者同在臂2 `akaOL28W`）/ best sub **0.63**（臂8）/ best DD **7.72%**（臂8）/ best margin **20.42bp**（臂4）/ 最宽 112·155（臂7）。
- **0 达标**：10/10 臂 `failed_ra_count` 3–5，**无一条过 RA 全闸**。

### §1.1 平台实读限值

| 闸 | 平台实读 limit | 与 ask 基准的关系 |
|---|---|---|
| LOW_SHARPE | **1.58**（10/10） | 一致 |
| LOW_FITNESS | **1.0**（10/10） | 一致 |
| LOW_2Y_SHARPE | **1.58**（10/10） | 一致 |
| CONCENTRATED_WEIGHT | **0.10**（臂3 实挂 value 0.5@2014-03-05；其余 9 臂 pass） | ask 的 CW≤0.10 即平台 limit |
| LOW_SUB_UNIVERSE_SHARPE | **逐臂动态**：臂2 0.48 / 臂3 0.17 / 臂4 0.38 / 臂5 0.0 / 臂7 0.35 / 臂9 −0.3 / 臂10 0.3；臂1/6/8 判 pass | ⚠ ask 静态口径「平台 LOW_SUB 限值 0.39」与本批动态实读不符（0.0–0.48），以逐臂实读为准；sub≥1.0 是本地 review 线 |

## §2 符号指纹逐条（ask 六条）

### ① 整式取反 —— **本战役首次具备实测对照（2 对）**

- **臂8/臂9（价格位置比率 ±）**：S 0.63/−0.63、F 0.34/−0.34、2Y 0.21/−0.21、sub 0.63/−0.63、margin ±8.47bp、pnl ±3,716,723 **全部严格镜像**；TO 0.0851 **逐位相同**；LC/SC 109/109 两侧相同；**DD 0.0772 vs 0.3935 不同** —— 回撤对取反天然不对称（−x 的最大回撤 ≠ x 的最大回撤），属指标性质而非信息不对称。⇒ S(−e)=−S(e) 精确成立且 |S|=0.63 ⇒ **该轴有 0.63 的方向信息量，不触发"停"**；方向读数取正向（价格高于 250 日均值→做多），且正向侧 DD 结构远优于反向（7.72% vs 39.35%）。
- **臂5/臂6（sign(Δ1) 66 日频率 ±）**：S 0.00/−0.00、F 0.00/−0.00、2Y −0.55/0.55、sub −0.11/0.11、margin ±0.4bp、pnl ±26,482 **严格镜像**；TO 0.1298 **逐位相同**；LC/SC 96/98↔98/96（取反预期互换）；DD 0.2044 vs 0.2550 不同（同上，指标性质）。⇒ **双向 |S|=0.00：方向层零净信息，指纹①判"停"** —— 该形态（`ts_sum(sign(Δ1 holdings),66)`）两向皆无信号，**轴死（本档口径）**。
- 判读纪律：S/2Y/sub/margin/pnl 镜像 + TO/LC-SC 相同即成立；DD 的不对称是数学性质，不作为"逐位相同"的反证，也不作为信息差证据。

### ② 去第二腿回落（BE176 带 1.0–1.30）

唯一复合臂2（ts_ir(holdings) ÷ ts_sum(集中度)）S **1.01 落在 1.0–1.30 带内**（下缘）——未破顶、未证伪上限；其可测单腿 = 分母腿 臂4（集中度裸 rank）0.81 ⇒ 复合高于该腿 **+0.20**；**分子腿（holdings IR 裸）本波未测** ⇒ "去第二腿"只能做一半，回落带判读记"一致但对照不完整"。

### ③ decay0/4/8 对照

**仅 decay0**（10/10 平台回显 decay=0），decay4/8 一条未跑 ⇒ **未测**（配置层单点，D6 未达）。

### ④ LC/SC<60/60 backfill 查证（本轮唯一新增平台调用：`get_alpha_yearly_stats` ×2）

臂2 60/124、臂3 61/60 恰在边界 ⇒ 逐年实读：

| 臂 | 结果 |
|---|---|
| 臂2 `akaOL28W` | **10/10 年 LC>0 且 SC>0**（2014 17/46 → 2023 106/184，逐年增长）；pnl 8/10 年为正（2017 S −0.5、2020 S −0.3 两年负） |
| 臂3 `LLKR9bw9` | **10/10 年 LC>0 且 SC>0**（2014 7/9 → 2023 131/127）；pnl 6/10 年为正 |

⇒ **非 backfill 假填充**：边界宽度是 insiders1 字段覆盖逐年增长（早年薄、2019 后放量）的真数据。臂2 若日后作提交候选，须按十年纪律逐年复核（2017/2020 两年 pnl 为负）；本波无候选，仅登记。

### ⑤ 费率分组正反两桶

**无 bucket/费率分桶臂** ⇒ 未测（N/A）；且本波无同核 group-vs-bare 对照对（臂2/6/7 是 group_rank、臂1/3/4/5/8/9/10 是裸 rank，但核不同）⇒ 分组轴增益本波不可判（累计：11-16 波已证 sector 零增益 −0.03、bucket 零作用）。

### ⑥ 首臂停

臂1 S=−0.23<1.58 即命中停条件（ask 转录以臂2 S 1.01<1.58 且 sub 0.26<0.39 记，两臂均满足）；后续臂为既定批次收尾，全波读数确认低于闸。先验对照：`DEU-INSIDER-AGGMATRIX-DEAD` 上限 0.92 属 `insider_agg_matrix` 数据集（**≠ insiders1**，get_dead_ends 实读核对）；insiders1 的先验上限是 BE176 的 1.0–1.30——本波 best 1.01 落在两先验之间，与"insider 族 DEU 单集强度不足"方向一致，但按 §7.5 判死标记不单独作依据。

## §3 稀释铁律

- 本波**零乘法复合**（2 条 `multiply(-1,…)` 是取反对照臂，非多腿）；复合形态 2 条：
  - **臂2（IR÷集中度）1.01 vs 其分母腿 臂4（集中度裸）0.81：复合 +0.20 ⇒ 非稀释**（本战役迄今最大的复合增益对照；atom-w1 的 ÷sig 对照仅 +0.04 且 sub 净损）。但分子腿未测 ⇒ 归因不完整（§8）。
  - 臂6（新鲜度÷sig）0.74 vs 新鲜度裸：本波未测裸新鲜度（atom-w1 臂6 新鲜度÷(sig+0.5) 0.34，形态不同不可直接对照）⇒ 不可判。
- ⇒ **无"复合低于对应单腿"的稀释实锤**；可测对照仅一对。臂2 的 +0.20 不得入册（缺裸分子腿，见 §8）。

## §4 宽度塌缩 / 数据层

- **0 条 data_excluded**：10/10 臂 LC/SC 60–155、7 臂 pnl 为正（+26k~+8.15M）、TO 4.5–13.0% 正常；年度分年证实无零持仓年（§2-④）⇒ **数据存在且可交易**。
- CW 挂闸仅臂3（0.5 vs 0.1 @2014-03-05，LC 61/60 双侧贴边）：**表达层**（Δ66-IR 在早年薄覆盖期集中），非数据层排除；同波其余 9 臂 CW pass。
- 臂5/6 DD 20.44%/25.50% 偏高但 LC/SC 96/98 健康 ⇒ 高回撤是零收益信号的路径噪声，不构成塌缩。

## §5 塔位判读（点塔相关性）

- 平台 `pyramids` 逐臂实读 **10/10 = DEU/D1/INSIDERS×1.6（effective=1）**、`ra.pyramid_short` 10/10 = `insiders` ⇒ **塔归属 = insiders 10/10 臂**（点塔入口全部成立）。
- **点位 ≠ 点亮**：10/10 臂 RA fail≥1 ⇒ 本批实际点亮 INSIDERS 塔 **0 颗**，塔计数不变。
- 纯 ATOM 单集：无第二塔位申请。

## §6 datasetStatus 裁决 + 波 verdict

**datasetStatus = `provisional`**。依据：

1. **判死六维盘点**：
   | 维 | 现状 | 判定 |
   |---|---|---|
   | D1 结构互异模板 ≥10 | 单波 8 种（sig 裸水平 / IR÷集中度 / Δ66-IR / 集中度裸 / sign 频率 / 新鲜度÷sig / 价格位置 / 新鲜度 ts_rank；取反 2 臂不计独立）；累计四波（BE176 30 + 11-16 w1 10 + atom-w1 9 + 本波 10 = 59 臂）互异机制 >10 | 累计 ✓ |
   | D2 字段族自测 | 本波 4 信号字段（holdings/valueeur/price/tradesignificance）；**`insd1_shares` 从未实测**（gvkey/currency 论坛归编码标签不挖，ARMTABLE §一） | **✗** |
   | D3 矩全家 | 水平 ✓（臂1/4/8）、一阶差 ✓（臂3 Δ66、臂5 Δ1 sign）、二阶波动 ✓（臂2/3 ts_ir）、比值 ✓（臂2 IR÷集中度、臂6 新鲜度÷sig、臂8 price÷mean） | **✓ 单波 4/4** |
   | D4 分组轴 ≥2 | 本波仅 sector+裸对照 ✗（累计 sector+bucket（11-16 臂4）=2，边际达） | 单波 ✗ |
   | D5 非线性 ≥1 | ts_rank（臂10）、sign（臂5/6）、group_rank | ✓ |
   | D6 配置 ≥2 | insiders1 全战役只扫过 decay0/nanON 一套；生产档 decay4/nanOFF 从未跑，配置层死/活未判 | **✗** |
   ⇒ **缺 D2、D6（D4 单波内）** ⇒ 按 AGENTS §7.6 **不得判死/封集/作邻接集先验**。
2. **数据层无排除**（§4，0 条 data_excluded）。
3. **信号层弱但有活体**：best 1.01 是 insiders1 系战役新高（此前 ATOM 上限带 1.0–1.30、atom-w1 best 0.74）——但仍未破 1.30 上限。
4. **DB 侧一致**：`mcp__wqb-db__get_dead_ends(DEU)` 实读，判死清单**不含 insiders1**（`DEU-INSIDER-AGGMATRIX-DEAD` 是 insider_agg_matrix 数据集，其"insiders 塔不可点亮"表述只在 22 模板/0.92 上限的**该集**证据范围内成立，**不外推到 insiders1**）。
5. 路线层：ATOM 单集路线维持 BE176 封顶 1.0–1.30（本波复合 1.01 在带内下缘，未破顶）。

**波 verdict = `PARTIAL`**（判定表 `src/wqb/wave_results_contract.py:79-90` / `verdict_from_counts`：n_pass=0 / **n_near=2**）：

- **臂2 `akaOL28W`**：F 0.80 距 F 闸 1.0 **0.20 ✓**（S 距 1.58 闸 0.57 ✗、2Y 距 1.58 闸 0.49 ✗、sub 0.26 距平台动态限 0.48 差 0.22 为次级记录）。
- **臂8 `O0W9rwXd`**：sub 0.63 距本地 sub 线 1.0 **0.37 ✓**（其平台 LOW_SUB 实际 pass、本地线更严；F 距闸 0.66 ✗、S 距闸 0.95 ✗）。
- 其余 8 臂全部出带：臂7 F 0.54 ✗、臂4 F 0.50 ✗（刚出）、臂3 CW 0.5 vs 0.1 机械差 0.4 但 S 0.35/sub 0.07 无经济含义（沿前两波口径不列）、臂1 margin −3.7bp 无近闸意义、臂5/6/9 零或负。
- **稳健性**：若近闸只认 S/F/2Y 强度闸，n_near=1（akaOL28W F 0.20）⇒ 仍 PARTIAL；**判定对 sub 口径不敏感**。
- ⚠ 本行 (DEU, rt-insiders-w1) 的 verdict 由 11-16 首批 FAIL 更新为本批 PARTIAL（merge 语义，ask 指定落库）；11-16 首批结论保留在其档案与本行 key_findings 首条。

## §7 近闸候选（≤2，按 S 降序；先测 prod 再扫参）

1. `akaOL28W`（S 1.01）：F 0.80 距 1.0 闸 0.20。**先测 prod/self**（归相关性员；prod 雷在核心不在搭档）；若 prod<0.70，扫参方向 = 补分子腿裸对照与 sub 修复（平台限 0.48），不是加壳。
2. `O0W9rwXd`（S 0.63）：sub 0.63 距本地 1.0 线 0.37；平台侧 LOW_SUB 已 pass。若推进，sub 提升优先于 S。

## §8 newLever 登记

**空串**。候选杠杆「ts_ir(holdings) ÷ ts_sum(集中度)」（臂2 1.01 > 分母腿 0.81，+0.20）是**单波内、且缺分子腿裸对照**——`rank(ts_ir(vec_avg(insd1_holdings),66))` 从未在任何波跑过；跨波角度 atom-w1 臂9（同分子 ÷(sig+0.5)）0.74 与本波 1.01 的差同时混入分母与壳层两个变量 ⇒ 归因对照不完整，不满足「跨波实证 + 裸 vs 改造」入册标准。下一波单变量补齐后再议。

## §9 绿芽 / 死轴 / 终态

**绿芽（活体结构）**：
1. `akaOL28W` IR÷集中度复合（S 1.01/F 0.80/2Y 1.09 三极值同臂；复合>分母腿+0.20；落 BE176 带内下缘）——insiders1 系战役新高，短板 sub 0.26（平台限 0.48）与 LC 60 早年薄（2014–2018 17–31）。
2. `O0W9rwXd` 价格位置比率（sub 0.63 本波最高 / DD 7.72% 本波最低 / LC-SC 109/109 对称；取反对照证明正向侧 DD 远优）。
3. `RRerVZoo` 集中度单腿跨波复现：与 11-16 `oma3GYeb`（同核无 +1e-4）读数一致至 ±0.01（S 0.81/F 0.50/TO 4.73%/LC 129·SC 140，margin 20.39→20.42bp 差 0.03bp）⇒ 该腿读数可复现，是臂2 复合的分母基线。
4. 新鲜度轴双形态 0.64–0.74（臂10 ts_rank 0.64、臂6 ÷sig 0.74）——弱但两次独立为正，低优先级保留。

**死轴**：
1. `sign(Δ1 holdings)` 66 日频率：S=0.00 双向严格镜像（指纹①判停）。
2. `tradesignificance` 裸水平：本波 −0.23、atom-w1 同字段水平 0.07，两波近零（atom-w1 的 2Y 1.37 残值另记，不随本波撤销）。

**终态**：
- 波 **PARTIAL**（0 达标 / 2 近闸）；best S **1.01** / best 2Y **1.09**（同臂 akaOL28W）。
- 数据集 `insiders1` = **provisional**（不判死、不 data_excluded、不封集）；ATOM 路线维持 BE176 封顶（1.01 在带内未破顶）。
- 塔：INSIDERS **10/10 臂归属**（单塔 eff1），**实际点亮 0**。
- 提交链**未推进**（0 达标；near 件 prod/self 未测）。
- **取证：不需要新论坛取证**（卡点 = 配置轴与 sub，本地可行动；本集已有 `DEU/forum_recon_fieldscan_insiders1_20261116` 8/8 字段与 9 篇 paper recon 存量；70-赞帖 1.68 的 404 冲突已在 ARMTABLE §四登记，recon 不可解 404）。

**下一步（按优先级）**：
1. near 件先测 prod/self（akaOL28W 优先；相关性员槽位）；
2. 补分子腿裸对照 `rank(ts_ir(vec_avg(insd1_holdings),66))`——把臂2 的 +0.20 归因坐实（IR 分子的贡献还是除法壳层）；
3. 配置维至少补一档生产档 decay4/nanOFF（D6），否则配置层死/活永远分不开；
4. 补 `insd1_shares` 字段族（D2 最后一个未测信号字段；ARMTABLE A4 已有单变量设计）；
5. sub 修复线：臂2 sub 0.26 是最近的可行动闸缺口（平台限 0.48）；
6. 不再重复：sign 频率轴（双向 0）、sig 裸水平（两波近零）、11-16 已证零增益的 sector/bucket 分组。

## §10 证据通道与盲区

**实跑核验（本档，全部只读）**：
- `mcp__wq-brain-http__get_alpha_details` ×10（10/10 success）：code/settings/metrics（含 LC/SC/pnl）/ra（failed_ra_count/pyramid_short）/checks.fail（value·limit·date）/pyramids.list 逐臂取回，与 ask 转录逐值一致；pyramids 10/10 = DEU/D1/INSIDERS×1.6 eff1。
- `mcp__wq-brain-http__get_alpha_yearly_stats` ×2（akaOL28W / LLKR9bw9）：指纹④查证（§2-④）。
- `mcp__wqb-db__list_expressions(DEU, rt-insiders-w1)`：21 条（11-16 批 11 + 本批 10，id 110207–110216 与臂序同序同值，atom_flag=atom 10/10）。
- `mcp__wqb-db__get_wave_result(DEU, rt-insiders-w1)`：读得 id 2228（11-16 首批 FAIL 版，verdict/19 条 key_findings 在案）。
- `mcp__wqb-db__get_dead_ends(DEU)`：判死清单实读，无 insiders1 条目。
- 判定表已读：`src/wqb/wave_results_contract.py:79-90`（VERDICT_TABLE + verdict_from_counts）。

**盲区（如实登记，不猜不补）**：
1. decay4/8 与 nanOFF 未扫（D6；配置层死/活未判）。
2. 分子腿裸对照缺失（臂2 的 +0.20 归因不完整；newLever 因此为空）。
3. 同核 group-vs-bare 对照缺失（分组轴增益本波不可判）。
4. `insd1_shares` 未测（D2）。
5. prod/self 全 null（归相关性员）；near 件的 prod 未测。
6. 年度分年仅取 2 臂（指纹④边界臂）；其余 8 臂未逐年核（十年纪律在提交链才硬性）。
7. bucket/费率分桶未测（指纹⑤ N/A）。
8. 波号复用：本批与 11-16 批共用 wave 号 rt-insiders-w1，DB 行 verdict 已由 FAIL 更新为 PARTIAL——两批读数以各自档案为准。
