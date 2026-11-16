# DEU S0 类别盘点：FUNDAMENTAL（2026-11-15）——目标集 fundamental72

> 任务：DEU × FUNDAMENTAL 类别 S0 盘点（交付目标=ATOM：单集字段、group 字段豁免、免 IS_Ladder 只看 2Y≥1.58 硬闸、每塔点亮=每集 3 因子）。排除面三型逐集以**本轮 DB 读数**重认定（不照抄上役实例）；目标集按机制先验+历史臂数+判死闸距离选定。
> ⚠ **命名说明**：`S0_DATASET_SCAN_FUNDAMENTAL_20261114.md`（早槽，目标集 fnd86）与 `S0_DATASET_SCAN_FUNDAMENTAL_FND72_20261114.md`（后半槽，目标集 fnd72 重开）均为 11-14 档案、被 `CATEGORY_MATRIX_FUNDAMENTAL_20261114.md:5` / `CATEGORY_MATRIX_FUNDAMENTAL_20261115.md:6` 按行号引用——不覆写他槽档案，本档为 11-15 新档。
> 判死纪律：AGENTS.md §7.5（判死标记不得单独作排除依据）+ §7.6（六维穷尽闸，缺维只能 PROVISIONAL）+ §8.11 ⑤（cov=0 不是数据存在性判据）。
> 先验来源（本轮 MCP 实读）：`get_region_overview` / `get_campaign_summary(DEU)` / `get_dead_datasets(DEU)`（19 键）/ `get_dead_ends(DEU)`（70 条全表）/ `query_dataset_profile(DEU,FUNDAMENTAL)`（0 行，§七盲区）/ `get_mining_yield(DEU, by_dataset=True, strict=True)` / `get_alpha_by_id`（KPJmRpGN / RREALzx0 / LLKO3vZ9 / gJaqYgQl / 1YW6xk3W / N1PkQxEw 六条）/ `get_submit_ready(DEU)`；本地档案逐条 path:line。

## 一、区域面（本轮 MCP 实读）

- DEU：**214 波（192 closed）/ 70 死路 / submit_ready=1**（`get_campaign_summary` 本轮；11-14 S0 档:11 记 211/189、11-15 矩阵:9 记 214/192，为同日多槽写入自然漂移，以本轮为准）。
- 类别语境：FUNDAMENTAL 塔 **1/3 点亮、×1.8 乘数**（waveBE242:452 fnd1 闸②）；fnd1 已收割提交 ACTIVE（pwaQ0bx3，2026-11-14，篮 17→18/20，waveBE242:461）。
- 上役承接（11-14/15 两槽）：fnd72 三波 25 臂 provisional 判弱入档（CATEGORY_MATRIX_FUNDAMENTAL_20261115.md:19-21，本会话全文实读）；fnd86 w1 十臂 active（WAVE_w1_fundamental86_20261114.md:67-71）。
- ⚠ **submit_ready 口径差如实登记**：`get_campaign_summary` 计 1，`get_submit_ready(DEU, READY)` 本轮实读返回 11 行（kqNRX1ZP/Vkxnb8QG/…，全部 corr_stale=true：missing/aged）——两工具口径不同（前者或按新鲜度过滤），不深究、不作本轮承重证据。

## 二、排除面（12 集逐集以本轮读数重认定）

**12 集清单**：fundamental1 / 6 / 17 / 22 / 45 / 72 / 86 / 89 / 90 / 93 + alpha_factor_lib + digital_ad_spend（沿 11-14/11-15 两矩阵 §2 同一面；`query_dataset_profile(DEU)` 0 行，类别分母走本地矩阵，§七）。

### A. 已收敛（7 集）

| 数据集 | 本轮读数（DB 台账 = get_mining_yield 本轮） | 排除理由（证据 path:line） |
|---|---|---|
| fundamental1 | 2 expr / 0 bt | **已收割**：pwaQ0bx3 S 1.60/F 1.40/2Y 2.01/prod 0.6821 已提交 ACTIVE（waveBE242:441-461）；网格收敛封顶 1.53→1.60，剩余仅待跨族合成授权（waveBE242:405-406） |
| fundamental6 | 88 expr / 26 bt / 0 passed | ATOM 天花板 1.15 + 主面 0.37（waveBE242:422）；oiadpq 单点 1.73 被 Wje5K71x 占用（DATASET_DISPOSITION_MAP_20261111.md:14） |
| fundamental17 | 10 expr / 10 bt / 0 passed / ra_unknown 0 | 台账 0 passed + 拥挤（waveBE242:422「浅探（已标死，拥挤）」）。⚠ `fundamental17_dead` 键在列（get_dead_datasets 本轮）——仅作参考，排除依据是台账读数+拥挤，非 dead 标记（AGENTS §7.5） |
| fundamental45 | （本轮 get_mining_yield 输出截断未见其行，沿引 11-14 S0 档:22 读数） | QA 78 臂收敛 S≤1.04（waveBE242:6）；12/12 矩阵「穷尽（0.96 塔位×2）」（waveBE242:412）。**保留为本役量级参照**（基线 S 0.96/2Y 1.73/sub 0.72，waveBE242:35，2026-11-14 事实非承诺） |
| fundamental89 | 24 expr / 20 bt / 0 passed | **六维终判死（2026-11-14）**：22+20 臂、S 天花板 ~1.0、2Y ≤1.02 vs 闸 1.58、D1–D6 逐维举证（waveBE242:240-251）+ 死档 id 1576（get_dead_ends 本轮）；不外推为邻接集先验（waveBE242:251 明文） |
| fundamental90 | 4 expr / 0 bt | **capped**：42 臂 S 平台 0.84–0.88、剩余结构手段全部实测（waveBE242:346-372）；死档 id 1551（get_dead_ends 本轮）三轴穷尽 S 1.20 距闸 32%、剩余 46 字段停广扫；2Y 过闸塔位 ×4 已入册——塔位储备面非重挖面 |
| fundamental93 | 8 expr / 8 bt / 0 passed | 12 臂水平 ≤0.53（waveBE242:108-123）+ 论坛 no_result（:261）+ 文献正解跨集不可 ATOM（:261）；实质关闭 |

### B. 伪集（1 集）

| 数据集 | 本轮读数 | 排除理由 |
|---|---|---|
| fundamental22 | 12 expr / 11 bt / **3 ra_clean** / ra_unknown 6 | RIC↔BBID 映射表伪集（waveBE242:265，字段名头「质量/ESG」实为映射）；3 颗 ra_clean 疑映射伪信号；11-07 vec_avg 水平 2 几何 S 0.48（DATASET_USABILITY_MASTER_20261111.md:17）。**永不复检** |

### C. 数据层排除（2 集）

| 数据集 | 排除理由 |
|---|---|
| digital_ad_spend | 宽度塌缩：探针 lc 25 / sc 25（~50/500），CW 0.5 vs limit 0.1 挂（waveBE242:125-126）——数据层排除非信号死 |
| alpha_factor_lib | 宽度塌缩：BE251 臂 DD 71%/199%/83%、margin −0.5~−5.7%（超窄账户签名，waveBE242:378-380） |

**小结**：12 集中 10 集三型排除完毕（上表 10 行）；fnd72（目标集，§四）与 fnd86（活体第二优先，§三）不入排除面。

## 三、候选对局：fnd72 vs fnd86（本轮类别面核心权衡，两类均非排除）

上役之后类别内仅剩两个活体，本轮必须二选一出具理由。

### 3.1 fnd86 梯度面（本轮 DB 复核）

- **台账**：20 expr / 20 bt / 0 passed（get_mining_yield 本轮；11-14 S0 档:53 记 10/10，本 run w1 后翻倍）。
- **w1 十臂读数**（WAVE_w1_fundamental86_20261114.md:19,21，本会话全文实读）：best = N1PkQxEw bucket 交互 S 0.91/F 0.70/2Y 0.97/DD 12.18%；1YW6xk3W 交叉双门 S 0.76/F 0.83/margin 0.0121（PnL 全波最高）；梯度链 裸 0.19–0.59 → 门控 0.59–0.76 → bucket 0.91。
- **本轮新读数（get_alpha_by_id，11-15 矩阵 §4 明言「本 run 无读数不作推断」处，本轮零成本补上）**：N1PkQxEw **prod=0.6347 判净**（corr_checked_at 2026-11-14T16:20:55）；1YW6xk3W **prod=0.5593 判净**（:16:21:13）——两颗 near 件均无相关性障碍，S 是唯一缺口。
- **2Y 条件化复活首证**：臂3 自门控 2Y=1.07（对照裸水平 0.00/−1.17 死轴，WAVE_w1:29）。
- **六维**：D1 ~7 类机制 <10 / D3 二阶波动矩缺 / D6 单配置（WAVE_w1:87-92）——远未到判死线。
- **11-14 矩阵判定**：本类别唯一活体（active，:33）；下波方向六条已备（WAVE_w1:98-103）。

### 3.2 fnd72 近闸族（本轮 DB 复核）

- **台账**：35 expr / 35 bt / 0 passed（get_mining_yield 本轮；= 11-14 S0 档:48 记 10 + 本 run 三波 25，口径闭合）。
- **在册近闸资产（get_alpha_by_id 本轮 DB 原值，均 UNSUBMITTED、stage=IS、dataset_id=1902）**：
  - **RREALzx0**（IS q_ebit 三 delta 秩乘，FAST 格）：S **1.42** / F 0.95 / 2Y 1.43 / TO 14.47% / sub 0.83 / margin 8.98bp / LC-SC 182-201；**prod=null / self=null（均未测）**。
  - **KPJmRpGN**（IS q_is_oper_inc 同几何，FAST 格）：S **1.38** / F 0.90 / **2Y 1.58（已触 ATOM 2Y 硬闸）** / TO 14.82% / sub 0.92 / LC-SC 185-197；**prod/self 均 null**。
- **本 run 三波判弱的范围限定**（CATEGORY_MATRIX_20261115.md:17-21）：25 臂全 RA fail、w3 verdict=FAIL，S 面 @**SUBINDUSTRY** 格 best 0.68/0.25/0.21——而近闸件是 **FAST 格**（11-05 近失波），WAVE_w1 档 §1 特记实证 **FAST 1.42 vs SUBINDUSTRY 0.20 = 7x 缺口**；FAST 配置轴从未进臂表扫描（仅 2 条历史近失件）。
- **2Y 裸锚**（get_alpha_by_id 本轮）：LLKO3vZ9（rank(a_ebit)）S 0.07/**2Y 1.51**/**prod 0.4875 判净**；gJaqYgQl（rank(a_is_oper_inc)）S 0.11/**2Y 1.53**/**prod 0.487 判净**——2Y 轴活体且无相关性障碍。
- **波 4 前置已满足**：4 探针开门线全过（cf_cash_from_oper/cf_net_inc/bs_q_1_tot_asset/季度水平格，LC+SC 134–155 ≥50，死档 1573 协议，CATEGORY_MATRIX_20261115.md:66）。
- **11-15 矩阵处方**（:71 standing state）：「2Y 裸锚活体 + 未扫自由度（**FAST 配置轴** / 比值·SNR 腿 / 宇宙·delay / 裸 rank 门控形未派发）= 下波设计输入；判死引用前必须先补 D3 比值腿 + D6 第二配置」。
- **六维**（11-14 S0 档:68-75 + 11-15 矩阵:21）：D2（IS 年度标量族/CF q 族/BS q_1/q_2 族/通用名 MATRIX 族未测）、D3（比值/SNR 腿三波零实测）、D5（门控类仅弱证）、D6（三波单配置）未达——PROVISIONAL 级，不可判死。

### 3.3 对局裁决：fnd72 优先，fnd86 降第二优先（不排除）

| 轴 | fnd72 | fnd86 | 裁决 |
|---|---|---|---|
| S 缺口（至 1.58 闸） | **0.16–0.20**（1.42/1.38 在册） | 0.67（0.91 全波最佳） | fnd72 优（4 倍差距） |
| 2Y（ATOM 唯一硬闸） | **1.58 已触闸**（KPJmRpGN）+ 裸锚 1.51/1.53 prod 净 | 条件化首证 1.07，未达 | fnd72 优 |
| 机制先验硬度 | **自身近失波实证**（FAST 格 delta 秩乘） | 跨集 lever C 迁移先验（fnd90→fnd86，迁移率 1/3 教训 s2_nearmiss_rescue_20261104.md:4962） | fnd72 优 |
| 未扫自由度 | FAST 配置轴（7x 实证缺口）/D3 比值·SNR/D6 宇宙·delay（11-15 矩阵:71 处方） | bucket 加密/门控叠加/D3 二阶矩/D6 变维（WAVE_w1:98-103） | 平（各有明确处方） |
| 下波前置 | **波 4 探针开门线已全过**（11-15 矩阵:66） | 需重新组波 | fnd72 优 |
| 反方证据 | 三波 25 臂 RA 全 fail + w3 FAIL + 两条修复路径证伪（11-15 矩阵:17-21）——**但判弱范围限 SUBINDUSTRY 格** | 单波无跨波复证；0.91→1.58 无实证支撑档位 | fnd86 反方更轻 |

**裁决依据**：S 缺口 4 倍差距 + 2Y 硬闸已触 + 波 4 前置已备 + 机制先验为自身实证 ⇒ **目标集 = fundamental72**；fnd86 反方证据更轻（无判弱史）、梯度清晰、near×2 prod 已净（本轮复核），**列为类别内第二优先活体**（moreTargetsRemain=true 的主体），不排除。

## 四、目标集 fundamental72：判死闸距离核对

### 4.1 在档死档与判死标记（不作单独依据，逐条复核）

- registry 死档两条（get_dead_ends 本轮，dead_at 2026-10-31，evidence_wave 107）：① `DEU-FND72-CF-DETAIL-SPARSE`（id 1573）：CF 明细/部分 BS 明细覆盖 <2%（LC-SC 2–5），CW 结构性必挂——**数据层排除，臂表继续遵守**（rule：只用 BS 主表 + cf_net_inc + cf_cash_from_oper；派发前 rank(F) 探针验 LC+SC ≥50——波 4 前置已按此协议过线）；② `DEU-FND72-NARROW-BREADTH`（id 1574）：十模板 S 上限 0.37、年报宽面仅 12–14% 覆盖（60–70/500）。
- ledger 层：**无 `fundamental72_dead` 键**（11-14 S0 档:54 核验沿引；get_dead_datasets 本轮 19 键不含 fnd72）——判死从未升格。
- 关联工具档：`DEU-TVRL-SLOW-SIGNAL-BREAK`（id 1575）：年报级慢变量 + 宽度<100 上 **ts_target_tvr_decay 禁用**；`DEU-BACKFILL-WINDOW-SUB-CLIFF`（id 1577）：慢变量 bf 基线 66，W=22 禁用。
- **六维现状**（11-14 S0 档:64-75 六维表 + 11-15 矩阵:21 本 run 更新）：D1 ✓（wave107 十模板 + 近失波 + 本 run 三波 25 臂）；D2 ✗（IS 年度标量族/CF q 族/BS q 族/通用名 MATRIX 族未测）；D3 部分（水平/一阶差/二阶分位有，**比值/SNR 腿零实测**）；D4 ✓ 3 轴（industry/SUBINDUSTRY/sector，bucket/market 未扫）；D5 部分（ts_rank 一类 + trade_when 弱证）；D6 ✗（**三波单配置**，宇宙/delay/decay 从未变过）⇒ **PROVISIONAL 级，远未到判死线**——「NARROW-BREADTH」子断言（IS 族缺失）已被 11-05 近失波部分证伪（季度 IS 标量族产出 S 1.42/1.38 近闸件，11-14 S0 档:75）。

### 4.2 采用理由（出具）

1. **类别内最近近闸族**：RREALzx0 S 1.42 / KPJmRpGN S 1.38 + 2Y 1.58 已触 ATOM 唯一硬闸——S 缺口 0.16–0.20 为 FUNDAMENTAL 类别内在册资产最小值（fnd86 缺口 0.67）。
2. **收割优先于重挖（AGENTS §7.5）**：两颗近闸件 prod/self 均 null（本轮 DB 复核）——补测相关性是**零仿真配额**动作，可能直接把候选送进提交链（每集 3 因子点塔路径：近闸件×2 + 新臂×1）；「prod 未知多半是检索盲区而非平台阻塞」。
3. **三波判弱不封集**：判弱范围限 SUBINDUSTRY 格 S 面 + 两条修复路径（门控推 2Y、gBF 修 CW）证伪；**FAST 配置轴有 7x 实证缺口**（1.42 vs 0.20）且从未进臂表——11-15 矩阵:71 已明文列为「下波设计输入」；11-14「不再加注」处置已被用户指定重开取代（11-15 矩阵 §2.1.2）。
4. **波 4 前置已备**：4 探针开门线全过（LC+SC 134–155，死档 1573 协议）——下一波可直接进主臂设计。
5. **未扫维度便宜且明确**：FAST 轴条件化（bucket/门控）、D3 比值/SNR 腿、D6 宇宙/delay 变维——全部不与三波已扫维度重复。
6. **反方证据如实登记**：① 三波 25 臂 RA 全 fail、w3 verdict=FAIL（11-15 矩阵:17-19）；② 近闸件为 11-05 历史件、本 run 未复证，prod/self 未测可能撞墙（收割动作先行即为此排除）；③ 结构上限假说（fnd72/fnd45 两集同停 1.42 ⇒ DEU/TOP500/D1 REGULAR 结构上限，处方=换 universe/delay，s2_nearmiss_rescue_20261104.md:4930-4937）——该假说恰把 D6 宇宙/delay 轴指为处方自由度，与本役加注方向一致而非相悖。

## 五、机制假设（驱动臂表设计，一句话）

**fnd72 IS 季度标量族（q_ebit / q_is_oper_inc）的盈利改善动量（三 delta 秩乘几何）在 FAST 中性化下活体**（RREALzx0 S 1.42 / KPJmRpGN S 1.38 + 2Y 1.58；SUBINDUSTRY 格 7x 缺口三波证死）；加注优先序 = ①近闸件 prod/self 补测收割（零仿真）→ ②FAST 配置轴条件化（bucket/门控/比值·SNR 腿）→ ③D6 宇宙·delay 变维；硬边界：CF/BS 明细不派（死档 1573）、TVR 层禁用（id 1575）、bf 窗口基线 66（id 1577）、门控推 2Y 与 gBF 修 CW 两条修复路径不复跑（11-15 矩阵:18-19 证伪）。

## 六、判读基准（S/2Y/sub/TO + 符号指纹）

| 轴 | 预期 | 依据 |
|---|---|---|
| S | FAST 近闸族天花板 **1.38–1.42**（本轮 DB）；缺口 0.16–0.20，新臂目标带 **1.5–1.7**（条件化/变维档）；SUBINDUSTRY 格三波死（0.68/0.25/0.21）**不复跑**；量级参照 = fnd45 基线 **S 0.96 / 2Y 1.73 / sub 0.72**（waveBE242:35，2026-11-14 事实，非现行承诺） | get_alpha_by_id 本轮 + CATEGORY_MATRIX_20261115.md:21 |
| 2Y | 近闸族 **1.43–1.58**（KPJmRpGN **已触 ATOM 2Y 硬闸 1.58**）；裸锚 1.51/1.53 且 **prod 已判净**（0.4875/0.487，本轮 DB）；目标 ≥1.58；裸水平 2Y<1.0 记「机制需条件化」指纹不记死 | get_alpha_by_id 本轮（LLKO3vZ9/gJaqYgQl） |
| sub | 近闸族 **0.83–0.92**（本轮 DB）；裸锚 0.33–0.39；分组轴沿用 sector（低覆盖面实证 sector>industry>subindustry，s2_nearmiss_rescue_20261104.md:4963）；**<0.75 记稳健告警** | get_alpha_by_id 本轮 |
| TO | 近闸族 **14.5–14.8%**（本轮 DB）；目标 <20%，>25% 记结构性告警；**TVR 层禁用**（慢变量+宽度，死档 id 1575）；bf 窗口基线 66（id 1577） | get_alpha_by_id 本轮 + get_dead_ends id 1575/1577 |
| 符号指纹 | **盈利改善→做多**（三 delta 同向乘积正向已证，RREALzx0/KPJmRpGN）；**衰减对称（翻转后 \|S\| 同量级）= 机制在/符号错，翻转保留；单向 = 事件型**；CW 挂 = **数据层指纹**（宽度塌缩）不改符号重试（死档 id 1573） | 11-14 S0 档:101 判读基准沿引 + get_dead_ends id 1573 |

## 七、证据通道与盲区声明（AGENTS §8.11 ⑦）

1. **query_dataset_profile / query_field_profile 对 DEU 全 0 行**（本轮实读 count=0；两档 11-14 S0 :12-15/:11 同盲区）⇒ 逐集状态不走 profile 表；类别分母（12 集）沿 11-14/11-15 矩阵 §2 同一面。
2. `get_mining_yield` 本轮输出尾部截断：fundamental45 行未见于本轮输出——沿引 11-14 S0 档:22 读数（QA 78 臂收敛的原始证据在 waveBE242:6/:412，不依赖该行）。
3. expressions/backtest_results 表不含 MCP 直连仿真（AGENTS §8.11 ⑦）；fnd72 台账 35 expr 与「10（11-14 前）+ 25（本 run 三波）」口径闭合；近闸件 2 臂在 alphas 表 dataset_id=1902 未计入 get_mining_yield 的 fnd72 行（10 vs 12 口径差，11-14 S0 档:48 已登记，本轮 35 vs 37 同构沿引）。
4. 本轮 get_alpha_by_id 六条均为 DB 原值；N1PkQxEw/1YW6xk3W 的 prod 判净读数为本轮新增（11-15 矩阵:64-65 原登记「prod/self 均未测」，其中 fnd72 侧 LLKO3vZ9/gJaqYgQl 的 prod 亦已被并行槽补测判净——corr_checked_at 2026-11-14/15，本轮复核确认）。
5. 判死纪律执行记录：fnd17 的排除依据 = 台账 0 passed + 拥挤（非 dead 键）；fnd89 六维终判死为读数合规死（D1–D6 逐维举证在 waveBE242:240-251）；fnd90/fnd93 的 dead 标记未单独使用（分别以 42 臂 S 平台/12 臂 ≤0.53 读数为据）；fnd72 死档按 PROVISIONAL 级引用、仅字段层硬边界（CF/BS 明细）生效。

---

## 八、本轮补充核查（2026-11-15 二次 S0 run，`data/wqb.db` 直读，逐条 SQL）

> 背景：本会话为独立的 S0 盘点 run，对同一类别面做**独立复核**。下列读数为本 run 用 `sqlite3` 只读直查 `data/wqb.db` 所得（MCP `query_dataset_profile`/`query_field_profile` 对 DEU 返回 0 行，故改走 `backtest_results`/`datasets`/`alphas` 直查）。**本段不推翻上文结论（目标集仍 = fnd72），但新增两项上文未覆盖的读数与一项新候选面，并登记一处口径漂移。**

### 8.1 台账读数复核（SQL，本 run）

- **DEU 整体**：`get_campaign_summary(DEU)` 本轮实读 `waves.total=214 / closed=192 / dead_ends=70 / submit_ready=1` —— 与上文 §一 完全一致。
- **DEU FUNDAMENTAL 类别分母 = 13 集**（非上文的 12 集）：`SELECT ... FROM datasets d JOIN regions r ON d.region_id=r.id WHERE r.name='DEU' AND d.category='FUNDAMENTAL'` 返回 13 行：
  `alpha_factor_lib(201) / digital_ad_spend(9) / fundamental1(123) / fundamental17(135) / fundamental22(1) / fundamental31(48) / fundamental45(12) / fundamental6(196) / fundamental72(1031) / fundamental86(7) / fundamental89(407) / fundamental90(66) / fundamental93(46)`（括号内 = `field_count`）。
  ⇒ **缺项 = `fundamental31`**（DEU `field_count` 48 / `coverage` 0.3955 / `alpha_count` 14），上文 §二 的 12 集清单未收录。
- **逐集臂数（按 `code` 字段前缀正则抽取，`region='DEU'`，本 run）**：

  | 数据集 | 臂数 | best S | best 2Y | best sub |
  |---|---|---|---|---|
  | fnd6 | 364 | 1.80 | 2.19 | 1.26 |
  | fnd45 | 249 | 1.42 | 2.25 | 1.12 |
  | fnd72 | 181 | 1.50 | 2.83 | 1.23 |
  | fnd90 | 140 | 1.09 | 1.76 | 0.97 |
  | fnd1 | 90 | 1.60 | 2.17 | 1.38 |
  | fnd89 | 74 | 1.33 | 1.91 | 0.78 |
  | fnd93 | 49 | 0.85 | 1.53 | 0.82 |
  | fnd86 | 27 | 0.94 | 1.13 | 0.77 |
  | fnd22 | 9 | 0.50 | 1.37 | 0.50 |
  | fnd17 | 2 | 0.31 | 0.60 | 0.30 |
  | **fnd31** | **0** | — | — | — |

  ⚠ **口径漂移如实登记**：本 run 的臂数（fnd6 364 / fnd45 249 / fnd72 181）显著高于上文 §二/§三 引用的 `get_mining_yield` 台账（fnd6 26 bt / fnd45 78 臂 / fnd72 35 bt）。原因：`backtest_results` 的 `dataset` 列对 10091 行 DEU 记录为 NULL（本 run 实测），真实数据集归属只能从 `code` 的字段前缀推断；而 `get_mining_yield` 走 `dataset` 列，故系统性少计。**本 run 的臂数以 `code` 前缀为准（更接近真实扫描面）；上文台账数以 `dataset` 列为准（更接近“已登记”面）——两者不可混用。**

- **ATOM 2Y≥1.58 硬闸命中臂数（本 run，按 `two_year_sharpe>=1.58`）**：fnd45 **75** / fnd1 **43** / fnd72 **35** / fnd6 **25** / fnd89 **14** / fnd90 **6**；fnd93 / fnd86 / fnd17 / fnd22 / fnd31 = **0**。

### 8.2 活跃波（11-14 / 11-15）二次读数 —— 对上文 §3.2「三波判弱」范围的复核

- **`wave='mcp-20261115'`（今日）fnd72 实测 48 臂**：`MAX(sharpe)=1.50 / MAX(two_year_sharpe)=2.83 / MAX(sub_universe_sharpe)=1.23`；其中 **32 臂 2Y≥1.58**、45 臂 S≥1.0。最佳臂 `vRA9K5Zw` S 1.44 / **2Y 2.83** / sub 1.15 / TO 14.36% / LC-SC 196-186。
  - 今天这批 arm 的公共骨架（code 原样）为 `hump(tail(winsorize(group_rank(multiply(multiply(rank(ts_delta(divide(fnd72_s_pit_or_is_q_is_oper_inc,fnd72_s_pit_or_bs_q_1_bs_tot_asset),200)),rank(ts_delta(...,150))),rank(ts_rank(...,1008))),sector),std=3),lower=...,upper=...,newval=0.5),hump=...)` —— **几何 = 季度 IS 盈利/资产比的 delta 秩乘 + sector 分组 + tail/hump**，与上文 §五 机制假设（q_is_oper_inc 盈利改善动量）**同族**，但用 `sector` 分组 + `tail` 而非上文近闸件的 FAST 格。今日仅动 4 个 fnd72 字段：`s_pit_or_bs_q_1_bs_tot_asset` / `s_pit_or_is_q_ebit` / `s_pit_or_is_q_is_oper_inc` / `s_pit_or_is_q_sales_rev_turn`。
  - ⇒ 这是对 §3.2「三波判弱限 SUBINDUSTRY 格」的**进一步旁证**：同一家族换 sector 分组 + 参数微调即产出 2Y 2.83，说明 S/2Y 的瓶颈在配置/几何而非信号本身。
- **`wave in ('mcp-20261114','mcp-20261115')` 逐集复核**：

  | 数据集 | 臂数 | 2Y≥1.58 | S≥1.0 | top S | top 2Y |
  |---|---|---|---|---|---|
  | fnd45 | 91 | 30 | 5 | 1.04 | 2.25 |
  | fnd1 | 83 | 43 | 65 | 1.60 | 2.17 |
  | fnd72 | 48 | 32 | 45 | 1.50 | 2.83 |
  | fnd90 | 36 | 6 | 0 | 0.88 | 1.76 |
  | fnd89 | 22 | 0 | 0 | 0.98 | 1.11 |
  | fnd93 | 10 | 0 | 0 | 0.53 | 0.95 |

- **fnd45 收敛复核（本 run）**：两波 91 臂，`MAX(sharpe)=1.04` —— 与上文/上役「QA 78 臂收敛 S≤1.04」读数**一致**。全时 high-S 臂（1.42 / 1.39 …）全部落在 `wave='mcp-20261105'`（更早一波），当前波已回到 1.04 平台 ⇒ 收敛结论成立，fnd45 维持排除面（已收敛）。
- **fnd1 机制（本 run 新读数）**：当前两波 83 臂、65 臂 S≥1.0、43 臂 2Y≥1.58 —— 看上去“很强”，但**字段集中度极高**：全时 90 臂中 76 臂只用 `fnd1_board_characteristics_filtered_timerole` 一个字段（其余 6 个字段合计 14 臂）。即 fnd1 的 S 1.58–1.60 几乎全来自**单字段**（董事会特征 time-role），非多因子塔。⇒ 上文「fnd1 已收割提交 ACTIVE」结论不受影响；但若本役要 fnd1 点塔（每集 3 因子），**3 因子不能都落在这同一字段**——这是对“每塔点亮=每集 3 因子”目标的一条硬约束，建议进臂表前先在 S1 验其余 6 字段（attrition3yr / director_characteristics / timebrd / stdevage / succession）的独立 Alpha 能力。**本轮未验（超出 S0 范围），如实标记为未做。**

### 8.3 新候选面：fundamental31（DEU 全零未探）——本 run 唯一实质新增

- **读数（本 run）**：`backtest_results` 中 `code LIKE '%fundamental31%'` 或 `'%fnd31%'` 且 `region='DEU'` = **0 行**；`expressions` 中 `fnd31` 的 DEU 记录 = **0 行**（28 条 fnd31 表达式全在 EUR：wave 286×18 / 282×8 / s2_expansion_cs1600×2）；`alphas` 表中 `dataset_id → fundamental31` 的记录 = **0 行**（任何区）。
- **数据面**：`datasets` 表 DEU `fundamental31` 行：`field_count=48 / coverage=0.3955 / delay=1 / status=NULL`。（该行 `alpha_count=14` 与 `alphas` 表 0 行矛盾 —— `datasets.alpha_count` 为旧快照脏值，不作依据。）
- **跨区对照（同一 datasets 表）**：fundamental31 在 USA `3423` alpha、EUR `7146` alpha、GLB `773`、KOR `506`、HKG `118`、GBR `0`(platform_empty) —— 是**跨区高出货集**，而非伪集或死集。
- **判死档核对（本 run）**：`get_dead_datasets(DEU)` 19 键 **不含 fundamental31**；70 条 `get_dead_ends(DEU)` **无 fundamental31 条目** ⇒ 从未被判死，也从未实测。
- **六维（按 AGENTS §7.6）**：D1 0 模板 / D2 0 字段族自测 / D3 0 矩 / D4 0 轴 / D5 0 非线性 / D6 0 配置 —— **全零，最远未到判死线**。
- **定位**：按 ask「目标集：历史臂数少且六维未穷尽 = 远未到判死线」，fnd31 是本类别**唯一真正的未探面**。但它**不与 ATOM 的近闸优势叠加**（0 臂、0 近闸件、无自身机制实证），vs fnd72（S 缺口 0.16–0.20、2Y 已触闸、今日 2Y 2.83）优先序明确靠后。
- **裁决**：**目标集仍 = fundamental72**（理由未变：最近近闸族 + 收割优先 + 2Y 硬闸已触 + 今日 2Y 2.83 复证）；**fundamental31 登记为本类别第三优先活体**（= `moreTargetsRemain=true` 的补充主体之一），进臂表面之前须先做 S1 字段体检（DEU 48 字段 / cov 0.3955，`query_field_profile` 对 DEU 为 0 行 ⇒ 必须走平台 `/data-fields` 实查，本 run 未做）。**本 run 未对 fnd31 派发任何仿真。**

### 8.4 判读基准补充（本 run 实测，供臂表设计）

| 轴 | fnd72 今日实测（`wave='mcp-20261115'`, sector 分组族） | 对上文 §六 的关系 |
|---|---|---|
| S | 1.44–1.50（top 6 臂 1.28–1.50） | 与上文「新臂目标带 1.5–1.7」吻合，已抵达下沿 |
| 2Y | **2.22–2.83**（32/48 臂 ≥1.58） | **远优于**上文「近闸族 1.43–1.58」——ATOM 硬闸在本族已不是瓶颈 |
| sub | 1.01–1.23 | 优于上文「近闸族 0.83–0.92」，稳健线（0.75）安全 |
| TO | 14.1–18.1% | 与上文「近闸族 14.5–14.8%、目标 <20%」一致，无需 TVR |
| 宽度 | LC-SC ≈ 196-186 ~ 231-151（合计 320–383） | 远高于死档 1573 的 ≥50 开门线 ⇒ 数据层健康 |

⇒ **本 run 判读基准修正建议**：fnd72 的瓶颈已从「2Y 不足」转为「S 不足（1.44–1.50 vs 1.58 目标）与因子去重」；下一波应优先查**今日 48 臂与历史近闸件的 self/prod 相关性**（今日臂均 UNSUBMITTED、prod 未测），以确认它们是 3 个正交因子还是同一因子的参数变体——这是「每集 3 因子点塔」的直接前置。

### 8.5 本 run 未能完成 / 未做（如实登记）

1. **`query_dataset_profile` / `query_field_profile` 对 DEU 返回 0 行**（本 run 实读 `count=0`）——DEU 的字段级覆盖率、verdict、n_tests 无法从本地 profile 表取得；`field_profile` 表按 `dataset_id` join DEU = 0 行。⇒ fnd31 的字段体检、fnd72 其余 1027 字段的覆盖情况**本 run 未验**（须平台 `/data-fields`）。
2. **今日 48 臂的相关性（self/prod）**：`backtest_results` 无相关性列，`alphas` 表中这些 arm 的 `prod_correlation` 多数为 NULL（本 run 查 DEU FUNDAMENTAL prod-clean 池仅 5 行：fnd72×3 / fnd86×2，且这 5 行 2Y 均 <1.58）⇒ 3 因子去重结论**本 run 未得出**。
3. **判死档取证**：本 run 只读 `get_dead_ends`/`get_dead_datasets` 结果，未逐条复核 payload 内的 forum_recon 证据；沿用上文 §四 的引用。
4. 本 run **未派发任何仿真**（S0 阶段只读）。
