# DEU S0 类别盘点：FUNDAMENTAL（2026-11-15）——目标集 fundamental93（重开裁定）

> 任务：DEU × FUNDAMENTAL 类别 S0 盘点。交付目标 = **ATOM**（所有臂只用同一数据集字段，group 字段 sector/subindustry/industry 豁免；免 IS_Ladder 只看 2Y——**2Y≥1.58 是硬闸**；无跨集 add，同集 add 走登记制：权重来源+腿 corr<0.7；每塔点亮=每集 3 因子）。
> 排除面三型（已收敛 / 伪集 / 数据层排除）逐集以**本轮 DB 读数**重新认定，不照抄上役实例。
> ⚠ 判死档/dead 标记不得单独作排除依据（AGENTS.md §7.5）；判死前须过六维穷尽闸（§7.6），缺维只能 PROVISIONAL。
>
> **命名说明（不覆写他槽档案）**：今日已存在 `S0_DATASET_SCAN_FUNDAMENTAL_20261115.md`（他槽，目标集 fnd72，本 run 未改其一字）与 11-14 的 `S0_DATASET_SCAN_FUNDAMENTAL_20261114.md`（目标集 fnd86）、`S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md`（目标集 fnd72 重开）。本档为独立目标集（fnd93）的 S0，沿 `..._FND72_...` 的目标集特化命名先例。
>
> **换集理由（核心裁定）**：他槽今日 S0 档第 29 行把 fnd93 记为「12 臂水平 ≤0.53 + 论坛 no_result ⇒ 实质关闭」。本轮 DB 重读发现该判定**只用了 `backtest_results` 一条证据通道**，漏掉了 `alphas` 通道里 6 条已过 2Y 硬闸的 fnd93 活体臂（S 1.59–1.70 / 2Y 1.59–2.32 / prod 全 NULL）。这正是 AGENTS.md §8.11⑦ 登记的盲区（MCP 直连仿真不写 expressions/backtest_results，对只看那两表的「已收敛/已测」清单隐形）。按 §7.5「判死标记不得单独作排除依据 + 收割优先于重挖」，fnd93 应判为**可收割近闸池**而非「实质关闭」，故重开为本轮目标集。

## 一、区域面（本轮 MCP / DB 实读）

- 工具：经 `LocalToolSearch` 加载只读面 `select:get_dead_datasets,get_dead_ends,query_dataset_profile,query_field_profile,get_region_overview,get_campaign_summary`，逐个 `DeferredToolCall` 调用。
- DEU（`get_campaign_summary` 本轮）：**214 波（192 closed）/ 70 死路 / submit_ready=1**。与他槽 S0 档:10 一致。
- `query_dataset_profile(DEU, category=FUNDAMENTAL)` 与 `query_field_profile(DEU, dataset=fundamental45)`：**均 0 行**（本会话实跑）。DEU 的 dataset/field profile 表整体为空 ⇒ 逐集状态**不走 profile 表**，全部以 `backtest_results`+`expressions`+`alphas`+`ledger_kv` 四通道为准（见 §五盲区）。旁证：`query_dataset_profile(EUR,FUNDAMENTAL)` 同调用返回 10 行正常数据 ⇒ 空是 DEU 专属，非工具故障。

## 二、排除面（逐集以本轮 DB 读数重认定）

DEU=region_id 10。FUNDAMENTAL 类别在 `datasets` 表登记 11 集（fundamental1/6/17/22/31/45/72/86/89/90/93）。逐集本轮读数：

| 数据集 | 本轮读数（通道） | 排除类型与理由 |
|---|---|---|
| **fundamental1** | backtest 0 行 DEU；alphas 含已提交 ACTIVE | A 已收敛：pwaQ0bx3 S 1.60/2Y 2.01/prod 0.6821 已提交（他槽 S0 档:23 引 waveBE242）；不再加注 |
| **fundamental6** | expressions 88 / backtest 26 / best_s 1.07 / best_2y 1.00 | A 已收敛：ATOM 天花板 1.15（他槽 S0 档:24）；2Y 天花板 1.00 远低于 1.58 硬闸 |
| **fundamental17** | expressions 10 / backtest 10 / best_s 0.31 | A 已收敛：台账 0 passed + 拥挤。⚠ `fundamental17` 在 `get_dead_datasets(DEU)` 19 键之列，但**排除依据是台账读数+拥挤，不是 dead 标记**（§7.5） |
| **fundamental22** | backtest 11 行 / best_s 1.72（疑映射伪信号） | B 伪集：RIC↔BBID 映射表（他槽 S0 档:35 引 waveBE242:265）；best_s 1.72 是映射伪信号不可信。**永不复检** |
| **fundamental45** | backtest **0 行（全区域）** / alphas **0 行** | A 已收敛（QA 线）：「78 臂收敛 S≤1.04」源自他区域/他通道（waveBE242:6），DEU 本地 backtest/alphas 均 0 行。**保留量级参照**：基线 S 0.96/2Y 1.73/sub 0.72（waveBE242:35，2026-11-14 事实非承诺） |
| **fundamental72** | backtest 53 / best_s 1.47 / best_2y 1.53；今日三波 25 臂 provisional | 活体（他槽今日目标集）：provisional 判弱入档，S 面 @SUBINDUSTRY 三波死（0.68/0.25/0.21），2Y 裸锚活体。六维 D3/D6 未达，**不可判死**。本 run 不动他槽焦点 |
| **fundamental86** | backtest 20 / best_s 0.91 / best_2y 1.07 | 活体第二优先：N1PkQxEw prod 0.6347 判净、1YW6xk3W prod 0.5593 判净（他槽 S0 档:54），S 是唯一缺口。六维未达，远未到判死线 |
| **fundamental89** | backtest 20 / best_s 0.98 / best_2y 1.91；死档 id 1576 | A 已收敛：六维终判死（2026-11-14，他槽 S0 档:27 + `get_dead_ends` id 1576 本轮）。**不外推为 fnd93 先验**（两者虽同属应计族，但 waveBE242:251 明文禁止跨集外推） |
| **fundamental90** | expressions 4 / backtest 0；死档 id 1551 | A 已收敛（capped）：三轴穷尽 S 1.20 距闸 32%，剩 46 字段停广扫；2Y 塔位 ×4 已入册，塔位储备非重挖面 |
| **fundamental31** | backtest 0 行 DEU | 未探（DEU 无臂）：coverage 0.3955/48 字段（datasets id 1004）。低优先备选，非本轮目标 |
| **digital_ad_spend** | — | C 数据层排除：探针 lc 25/sc 25 宽度塌缩、CW 0.5 挂（他槽 S0 档:41）。数据层排除非信号死 |
| **alpha_factor_lib** | — | C 数据层排除：BE251 超窄账户签名（他槽 S0 档:42） |

**排除面小结**：A 已收敛 6 集（fnd1/6/17/45/89/90）+ B 伪集 1 集（fnd22）+ C 数据层排除 2 集（digital_ad_spend/alpha_factor_lib）= 9 集排除；活体 fnd72（他槽焦点）/ fnd86（第二优先）/ fnd31（未探低优先）；**fnd93 经本轮重裁从「实质关闭」改判为可收割近闸池 = 本轮目标集（§三）**。

## 三、目标集：fundamental93（重开裁定 + 机制假设）

### 3.1 改判证据（本轮 DB 实读，双通道对照）

fnd93 的「已收敛/实质关闭」先验（他槽 S0 档:29）**只引用了 `backtest_results` 通道**。本轮把 `alphas` 通道并读，结论反转：

- **`backtest_results`（DEU, dataset=fundamental93）**：8 行，best_s **0.36** / best_2y 1.24。全部 `-rank(ts_mean(fnd93_accruals_d1_*,22))` 形式的**水平/平滑秩**臂（1YN153PM/xAr9a7on/88R7qW2a/A1VYdX2R/LLMqxowa/GrWYvj7x/kqNb5p98/gJewzNLm）。→ 这是他槽据以判「水平 ≤0.53」的那批。
- **`alphas`（region_id=10, dataset=fundamental93）**：16 行，其中 **6 条高 2Y 活体臂不在 `backtest_results` 里**（本会话逐 id 核对：`SELECT alpha_id FROM backtest_results WHERE alpha_id IN (那6条)` 返回空 ⇒ 它们只存在于 alphas，即 MCP 直连仿真通道，§8.11⑦ 盲区）：

| alpha_id | 表达式（纯 fnd93 单集） | S | 2Y | sub | TO | prod |
|---|---|---|---|---|---|---|
| YBbZAXvN | `-rank(ts_mean(fnd93_liability_d1_current_t,22))` | 1.70 | **2.32** | 1.16 | 0.380 | NULL |
| MhHyLY69 | `-group_rank(ts_mean(fnd93_accruals_d1_mean,22),subindustry)` | 1.70 | **1.60** | 1.46 | 0.362 | NULL |
| wWPcygbY | `-rank(ts_mean(fnd93_accruals_d1_mean,22))` | 1.65 | **1.63** | 1.36 | 0.363 | NULL |
| RYtSG1Lr | `-rank(ts_mean(fnd93_accruals_d1_current_t,22))` | 1.64 | **1.59** | 1.25 | 0.370 | NULL |
| r0jEGh24 | `-rank(ts_mean(fnd93_accruals_d1_dts,63))` | 1.59 | 1.15 | 1.38 | 0.239 | NULL |
| KJh7h1VN | `-rank(ts_mean(fnd93_accrualsratio_d1_asset_change,22))` | 1.23 | 1.26 | 1.00 | 0.457 | NULL |

  状态全 `UNSUBMITTED`、`prod_correlation` 全 NULL。universe/delay/neutralization 列为 NULL（MCP 直连未回填），需在收割时经 `get_alpha_details` 核对平台 code/settings 确认 DEU/TOP500/D1 配置归属。
- **判读**：同一批表达式在 `backtest_results` 里 S≤0.36、在 `alphas` 里 S 1.59–1.70 —— 不是信号变了，是**两条通道对应不同配置快照**（alphas 高 S 臂的中性化/宇宙未回填，疑为非 SUBINDUSTRY 或不同 decay 的更优配置）。无论配置如何，**2Y≥1.58 硬闸已被 4 条臂（YBbZAXvN/MhHyLY69/wWPcygbY/RYtSG1Lr）真实跨过**，且全部 prod 未测 = 零仿真配额即可收割。

### 3.2 ATOM 合规性

- 46 个 signal 字段全 `fnd93_*`（`s1_semantic_fundamental93`，blocked=0），单一数据集。6 条臂仅用 `fnd93_accruals_d1_*` / `fnd93_liability_d1_*` / `fnd93_accrualsratio_d1_asset_change`，group 字段仅 subindustry（豁免内）。**无跨集 add**，纯单集 ATOM。
- 字段画像（datasets id 1011）：46 字段，value_score 5，delay 1。

### 3.3 机制假设（驱动臂表设计）

> **一句话机制假设**：fnd93 的「应计-递延税-流动负债」会计质量族在 DEU 的定价是**反转/质量折价**——高应计与高流动负债扩张的公司未来收益被低估其盈余低质量，做空高应计（`-rank(ts_mean(accruals))`）捕捉质量溢价；信号在**水平/平滑秩**几何下即有效，且对 `subindustry` 中性化不敏感（group_rank 版 MhHyLY69 sub 1.46 最高）。

### 3.4 判死闸距离（六维，AGENTS §7.6）

fnd93 在 DEU 仅 8 条 backtest 臂 + 16 条 alphas 臂，**远未到判死线**：
- D1 结构互异模板：实测仅「水平秩 / 平滑秩 / group_rank / ts_delta」~4 类 < 10 ✗
- D2 字段族自测：46 字段中实测仅 ~6 个（accruals_d1_mean/current_t/dts、liability_d1_current_t、accrualsratio_d1_asset_change、tax_accruals_51）✗（其余 deferred_tax_expense/liability、expense_d1、liability_d1_mean/max/min 等族未测）
- D3 矩全家：有水平+一阶差（kqNb5p98 ts_delta），缺二阶波动、信噪比 ✗
- D4 分组轴：仅 subindustry（1 个）< 2 ✗
- D5 非线性：0 条（无 signed_power/ts_rank/trade_when/bucket）✗
- D6 配置：alphas 高 S 臂配置未回填，待核；backtest 臂单配置 ✗

⇒ fnd93 任何「关闭/判死」表述均不成立（缺 D1–D6 全部维度举证），只能记 **PROVISIONAL-活体**。本轮裁定：**可收割近闸池**，优先收割 4 条已过 2Y 硬闸臂。

## 四、判读基准（S/2Y/sub/TO 预期 + 符号指纹）

- **硬闸**：2Y≥1.58（ATOM 免 IS_Ladder）。参照点：fnd93 已有 YBbZAXvN 2Y 2.32 / MhHyLY69 1.60 / wWPcygbY 1.63 / RYtSG1Lr 1.59 四件过闸 ⇒ 该集 2Y 天花板已被实证捅破，新臂设计以「保住 2Y≥1.58 同时抬 S 与 sub」为目标。
- **S 预期**：过闸臂 S 区间 1.59–1.70。量级参照（2026-11-14 事实非承诺）：fnd45 基线 S 0.96/2Y 1.73/sub 0.72。
- **sub 预期**：过闸臂 sub 1.16–1.46（均 >0.75 稳健线）。group_rank 形（MhHyLY69）sub 最高 1.46 ⇒ subindustry 中性化提升子宇宙稳健。
- **TO 预期**：水平秩 22 日平滑臂 TO 0.24–0.46（24%–46%），偏中频。63 日平滑（r0jEGh24）TO 降至 0.239 ⇒ 拉长平滑窗可压 TO，但 2Y 同步降至 1.15（跌破硬闸）⇒ **TO 与 2Y 存在权衡，22 日窗是当前 2Y 最优点**。
- **符号指纹**：机制为**做空高应计/高负债**（表达式前缀 `-`）。若新臂出现「做多高应计 S 为正」或「衰减不对称」= 符号错/机制不在，立即停。预期：`-rank(ts_mean(accruals_d1_*,22))` 族 S 应稳定为正且 2Y 跟随；衰减对称 = 机制在。

## 五、盲区与证据通道声明

- **DEU 的 query_dataset_profile / query_field_profile 全 0 行**（本会话实跑）⇒ 类别分母与逐集状态不走 profile 表，走 `backtest_results`+`expressions`+`alphas`+`ledger_kv` 四通道。
- **§8.11⑦ 盲区实证**：fnd93 的 6 条高 2Y 臂只存在于 `alphas`，不在 `backtest_results`/`expressions`（MCP 直连仿真不写后两表）。他槽今日 S0 档:29 的「fnd93 实质关闭」正是只读后两表得出的结论，被本轮推翻。**任何「已收敛/已测/已关闭」清单必须标注它由哪条通道得出、对什么盲视**。
- **本轮未做（如实）**：平台相关性（prod/self-corr）、`get_alpha_details` 配置核对、年度分年（get_alpha_yearly_stats）、任何新仿真——S0 盘点边界内零平台调用。6 条臂的 universe/delay/neutralization 配置归属、prod/self-corr、近十年持仓连续性均**未测**，是收割槽的下一动作，不在本档承诺范围。
- 高 S 的 `alphas` 行与低 S 的 `backtest_results` 行共享表达式但指标不同，配置快照差异**未在本轮定位**（需 `get_alpha_details` 读平台 settings），本档只登记现象不作配置臆断。

## 六、产物与复跑

- 本档：`tracking/DEU/atom_orthogonal/S0_DATASET_SCAN_FUNDAMENTAL_FND93_20261115.md`
- 一次性核验脚本（logs/，用完可删）：`_tmp_deu_fnd.py` / `_tmp_deu_fnd2.py` / `_tmp_deu_fnd3.py` / `_tmp_deu_fnd4.py` / `_tmp_deu_fnd5.py` / `_tmp_deu_fnd6.py` / `_tmp_deu_fnd7.py`（全部 sqlite 只读，唯一写入是 logs/ 临时脚本本身）。
- 复跑口径：`world-quant-brain-mcp/.venv/Scripts/python.exe -X utf8 logs/_tmp_deu_fnd{,4,5,6,7}.py`；PRODCORR_CEILING=0.70（`src/wqb/config.py` 本轮实读）。
- 不覆写他槽档案：`S0_DATASET_SCAN_FUNDAMENTAL_20261115.md`（fnd72 目标）与本档（fnd93 目标）并存，结论冲突处（fnd93 状态）以本档双通道 DB 读数为准，建议下一槽在矩阵档案中登记该更正。
