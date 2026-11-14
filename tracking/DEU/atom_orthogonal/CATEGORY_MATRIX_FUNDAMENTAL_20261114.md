# CATEGORY_MATRIX — DEU × FUNDAMENTAL 日终矩阵（2026-11-14）

- 性质：日终收尾档案（只写档案，零平台调用；本 run 仅 1 波 = w1 fundamental86）。
- 证据来源（全部本会话实读或本 run 回执）：
  ① `S0_DATASET_SCAN_FUNDAMENTAL_20261114.md`（全文实读，逐集状态的原始 path:line 引用以该档为准，本矩阵引其行号）；
  ② `WAVE_w1_fundamental86_20261114.md`（本 run 归因档，本会话所写）；
  ③ DB 回执：`upsert_wave_result(DEU, w1)` → `action=inserted, verdict=PARTIAL, status=closed, source_file=pipeline:auto`（本 run）；
  ④ run 收尾 rollup 两行（ask 给定）：数据集终态=「本 run 无数据集终态变更」、跨波待处理提交链候选=`1YW6xk3W（目标集 fundamental86，prod 已判净未跑链）`。
- 未做/不做（如实）：平台相关性、prod 复测、年度分年、self-corr 均未跑（单槽边界 + 日终零平台调用约束）；本矩阵不新增任何判读，只汇总既有档案状态。

## §1 本 run 波次与产出

| 项 | 值 | 出处 |
|---|---|---|
| 波 | w1（fundamental86，DEU/TOP500/D1，SUBINDUSTRY/decay4/trunc0.08） | WAVE_w1 档案头 |
| 臂 | 10/10 COMPLETE、errors=0，multisim=`2hhCTvc8m58gbZB1eHMXe7x7` | 同上 + 收割回执（ask 步骤⑥⑦） |
| 落库 | backtest_rows n=10/0 跳过；wave_results DEU/w1 = PARTIAL（n_pass=0/n_near=2，closed，source_file=pipeline:auto） | 收割步骤⑦回执 + 本 run DeferredToolCall 回执 |
| bestSharpe | 0.91（臂8 N1PkQxEw bucket 交互 avg×rel_val，DD 12.18% 最低） | WAVE_w1 §1/§2 |
| datasetStatus | **active（继续加注）**——非终态类变更（无 dead_proposed/data_excluded/capped 转换） | WAVE_w1 §4 |
| near×2 | N1PkQxEw（S 0.91；CW 0.109432 距平台 limit 0.1 差 0.0094）、1YW6xk3W（S 0.76；F 0.83 距 fitness_min 1.0 差 0.17） | WAVE_w1 §5 |
| 数据层排除 | 字段级：`fnd86_insider_trading_score`（LC 8→11 + CW 0.5 FAIL，臂1/5 记 data_excluded 形态，≠信号死）；集级不排除 | WAVE_w1 §3 |

## §2 逐集终态矩阵（类别 12 集；状态引 S0 盘点行号，本 run 未改写任何一行的先验）

| 数据集 | 终态 | 类型 | 状态依据（S0_DATASET_SCAN_FUNDAMENTAL_20261114.md:NN） |
|---|---|---|---|
| fundamental1 | capped（已收割） | A 已收敛 | :29 —— pwaQ0bx3 S 1.60/F 1.40/2Y 2.01/prod 0.6821 已提交 ACTIVE（2026-11-14，waveBE242:441-461）；网格收敛封顶 1.53→1.60；剩余仅待跨族合成授权 |
| fundamental6 | capped | A 已收敛 | :30 —— ATOM 天花板 1.15；oiadpq 单点 1.73 被 Wje5K71x 占用（DATASET_DISPOSITION_MAP_20261111.md:14）；台账 26 臂 0 passed |
| fundamental17 | 浅探排除（非判死依据） | A 已收敛 | :31 —— 台账 10 臂 0 passed + 拥挤；dead 标记不作单独依据（AGENTS §7.5 实证在案） |
| fundamental22 | pseudo（伪集，永不复检） | B 伪集 | :37 —— RIC↔BBID 映射表冒充质量/ESG（waveBE242:265）；3 颗 ra_clean 疑映射伪信号 |
| fundamental45 | converged（保留量级参照） | A 已收敛 | :25 —— QA 78 臂收敛 S≤1.04；基线 S 0.96/2Y 1.73/sub 0.72（waveBE242:35，非现行承诺） |
| fundamental72 | data_excluded（CF/BS 明细）+ 主面不再加注 | C 数据层排除 | :45 —— CF/BS 明细宽度 2–5（死档 DEU-FND72-CF-DETAIL-SPARSE）；EBIT 主面近闸件 WjOLdO7o 1.42/2Y 1.82 但 11-14 处置=不再加注（waveBE242:421） |
| fundamental86 | **active（本类别唯一活体）** | — | 本 run w1 十臂：bestSharpe 0.91、2Y 条件化复活（臂3 1.07）、近闸×2；六维闸 D1–D6 远未触（WAVE_w1 §6；S0 :58-70 零命中基线） |
| fundamental89 | dead（六维终判死，2026-11-14） | A 已收敛 | :26 —— 今日 22 臂 + 历史 20 臂，S 天花板 ~1.0、2Y ≤1.02 vs 闸 1.58，D1–D6 逐维举证（waveBE242:240-251）；死档 DEU-FND89-NONCURRENT-ACCRUAL-CEILING（get_dead_ends id 1576）；**不外推为 fnd86 先验**（waveBE242:251 明文） |
| fundamental90 | capped（塔位储备已入册） | A 已收敛 | :27 —— 42 臂 S 平台 0.84–0.88，剩余结构手段全部实测；2Y 过闸塔位 ×4 已入册（gJa7kj7v 0.84/1.68） |
| fundamental93 | converged（实质关闭） | A 已收敛 | :28 —— 12 臂水平 ≤0.53 + 论坛 no_result + 文献正解跨集不可 ATOM；资产增长种子 0.53/2Y 0.95 已登记 |
| alpha_factor_lib | data_excluded | C 数据层排除 | :44 —— BE251 臂 DD 71%/199%/83%、margin −0.5~−5.7%（超窄账户签名） |
| digital_ad_spend | data_excluded | C 数据层排除 | :43 —— 探针 lc 25/sc 25（~50/500），CW 0.5 vs limit 0.1 挂；数据层排除非信号死 |

排除面小结（S0 :47）：12 集中 11 集三型排除完毕，唯一未排除 = fundamental86（本 run 开波并判 active）。

## §3 今日（2026-11-14）类别产物索引（mtime 本会话 `ls -la` 实测）

| 文件（atom_orthogonal/） | mtime | 内容 |
|---|---|---|
| waveBE242_FND89_ACCRUAL_ATOM_20261114.md | 14:05 | fnd89 六维终判死 + fnd1 收割提交 ACTIVE + fnd45 QA/基线读数 + fnd90/93/17 排除读数（本矩阵 §2 各行原始证据均在该档） |
| S0_DATASET_SCAN_FUNDAMENTAL_20261114.md | 15:42 | FUNDAMENTAL 类别盘点：排除面三型 11 集 + 目标集 fnd86 判死闸距离核对 + 判读基准 |
| WAVE_w1_fundamental86_20261114.md | 16:19 | 本 run w1 十臂逐臂归因（active / 0.91 / near×2 / insider 字段数据层排除） |
| CATEGORY_MATRIX_FUNDAMENTAL_20261114.md | 本档 | 日终矩阵 |

- 同日非本类别产物（不在本矩阵范围，仅列名）：waveBE239_BE240_OPSCAN_design/verdict（02:08/02:17）、FIELD_PROFILE_MODEL238（00:29）、LEDGER_MDL238_BE232_234 / BE235_237（01:10/01:34）、FINAL_DELIVERY_20261114（02:26）。
- 在档支撑件（非今日）：`_recheck_expr_only.json`（w1 查重通道一：fnd86 used=1/untested=6）、`cov0_audit_final_20261109.csv`（fnd86 字段存在性探针 ac 87）、`DATASET_DISPOSITION_MAP_20261111.md`（单点占用台账）——三者均在 atom_orthogonal/（`ls` 本会话核验）。

## §4 提交链与待确认

- **待用户确认候选：[]（rollup 给定，本 run 无）**。
- **跨波待处理提交链候选：1YW6xk3W**（目标集 fundamental86；rollup 注「prod 已判净未跑链」）。注意：w1 归因档 §8 已如实登记「相关性查询未做（单槽在相关性员）」——prod 净是 rollup 层状态，本 run 未亲自跑相关性；提交链余下步骤（近十年/self-corr/篮内互相关+塔位配额，AGENTS §7.5 五道闸顺序）均未跑，待下一槽执行。
- N1PkQxEw（near-gate#1）未出现在 rollup 待处理清单：其 prod 状态本 run 无读数，**不作推断**；w1 档案既定指令仍为「先测 prod 再扫参」。
- 区域语境（S0 :11,17，转引）：DEU 211 波/70 死路/submit_ready=1（3q0gZE0N，prod 槽位排队，waveBE242:492）——非本 run 产物，rollup 未列待确认，本矩阵仅登记语境。

## §5 变更声明

- **本 run 无数据集终态变更**（rollup 给定；本 run 唯一状态赋值 = fundamental86 → active，系首波加注延续，非终态转换）。
- 今日类别面累计（含同日他档）：fundamental89 六维终判死（waveBE242，他档）；fundamental1 收割提交 ACTIVE（waveBE242:441-461）；两者均非本 run 动作，本矩阵仅汇总。

## §6 盲区与证据通道声明

- DEU 的 query_dataset_profile / query_field_profile 全 0 行（S0 :12-15 本会话实读）⇒ 逐集状态不走 profile 表，全部以 S0 盘点（get_mining_yield/get_dead_ends/get_field_catalog + 本地档案三通道）为准。
- expressions 表不含 MCP 直连仿真（AGENTS §8.11 ⑦）；w1 十臂由收割步骤⑥⑦回执与本 run DB 写入覆盖。
- 本矩阵零平台调用、零 DB 写入（唯一 DB 交互为本 run 早前的 wave_results 插入，回执已录 §1）。
