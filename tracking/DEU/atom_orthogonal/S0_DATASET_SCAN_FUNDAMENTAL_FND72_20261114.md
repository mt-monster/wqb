# DEU S0 类别盘点：FUNDAMENTAL — 目标集 fundamental72（2026-11-14）

> 任务：DEU × FUNDAMENTAL 类别 S0 盘点，**目标集 = fundamental72（用户指定）**——核对其判死闸距离（六维 D1–D6 + 历史臂数）并出具采用理由；排除面三型逐集以本次 DB 读数重认定；判读基准含 S/2Y/sub/TO 与符号指纹。
> ⚠ **命名说明**：`S0_DATASET_SCAN_FUNDAMENTAL_20261114.md` 已被今日早槽 S0（目标集 fnd86，mtime 15:42）占用并被 `CATEGORY_MATRIX_FUNDAMENTAL_20261114.md:5` 按行号引用——**不覆写他槽档案**（AGENTS §7 并行写入纪律），本档用集名后缀 `..._FND72_20261114.md`，与早槽档互为补充、不互改。
> 先验来源（本轮 MCP 实读）：`get_dead_datasets(DEU)` / `get_dead_ends(DEU)` / `get_mining_yield(DEU, by_dataset=True, strict=True)` / `get_field_catalog(DEU, fundamental72)` / `get_alpha_by_id(KPJmRpGN)` / `get_alpha_by_id(RREALzx0)` / `list_ledger_keys(DEU)` / `get_campaign_summary(DEU)` / `get_region_overview()`；本地档案逐条 path:line。
> 判死纪律：AGENTS.md §7.5（判死标记不得单独作排除依据）+ §7.6（六维穷尽闸，缺维只能 PROVISIONAL）+ §8.11 ⑤（cov=0 不是数据存在性判据）。

## 一、区域面（本轮 MCP 实读）

- DEU：212 波（190 closed）/ 70 死路 / submit_ready=1（`get_campaign_summary(DEU)` 本轮；早槽档 :11 记 211/189，为同日他槽写入后的自然漂移，以本轮为准）。
- ⚠ **证据通道盲区（AGENTS §8.11 ⑦，如实登记）**：`query_dataset_profile(region=DEU)` 与 `query_field_profile(region=DEU, dataset=fundamental72 / keyword=fnd72)` 本轮均返回 **0 行**；EUR 对照查询返回 10 行（updated_at 2026-10-25）⇒ 工具本身正常，**DEU 画像表整区未入库**。DEU 先验全部改走 `get_mining_yield`（backtest_results 台账）+ `get_field_catalog`（平台缓存）+ 本地档案三通道。

## 二、排除面（FUNDAMENTAL 类别 12 集，逐集以本轮读数重认定）

### A. 已收敛

| 数据集 | 本轮读数 | 排除理由（证据） |
|---|---|---|
| fundamental1 | 已收割：pwaQ0bx3 S 1.60/F 1.40/2Y 2.01/prod 0.6821 提交 ACTIVE（2026-11-14，waveBE242_FND89_ACCRUAL_ATOM_20261114.md:441-461）；DB 台账仅 2 expr 0 bt（get_mining_yield 本轮） | 网格收敛封顶，剩余仅待跨族合成授权（:405-406） |
| fundamental6 | DB 台账 26 bt / 0 passed（get_mining_yield 本轮）；oiadpq 单点 1.73 被 Wje5K71x 占用（DATASET_DISPOSITION_MAP_20261111.md:14） | 单点占用 + 类别内收敛（waveBE242:424「浅探 主面 0.37 + ATOM 天花板 1.15」） |
| fundamental17 | DB 台账 10 bt / 0 passed（get_mining_yield 本轮）；11-14 矩阵「浅探（已标死，拥挤）」（waveBE242:422）；ledger 有 `fundamental17_dead` 键（list_ledger_keys 本轮） | 排除依据 = **台账 0 passed + 拥挤**；dead 键仅作参考不作唯一依据（AGENTS §7.5） |
| fundamental45 | QA 78 臂收敛 S≤1.04（waveBE242:6）；基线 S 0.96/2Y 1.73/sub 0.72（waveBE242:35，**本役量级参照，非承诺**）；51 臂判弱（s2_nearmiss_rescue_20261104.md:4940） | QA 面收敛不再加注；近闸件 WjOLdO7o（S 1.42）属 **fnd45** 而非 fnd72（:4941，详见 §7 更正） |
| fundamental86 | DB 台账 20 bt / 0 passed（get_mining_yield 本轮）；本日早槽 w1 已开（10 臂 bestSharpe 0.91 / 近闸×2，CATEGORY_MATRIX_FUNDAMENTAL_20261114.md:15-20），跨波候选 1YW6xk3W 在途 | **非本役目标（用户指定 fnd72）+ 他槽在途**，不并槽重复加注 |
| fundamental89 | 六维终判死（D1–D6 逐维举证，waveBE242:240-251；今日 22 臂 + 历史 20 臂，S 天花板 ~1.0）+ 死档 DEU-FND89-NONCURRENT-ACCRUAL-CEILING（get_dead_ends id 1576） | 六维合规死；**不外推为 fnd72 先验**（waveBE242:251 明文） |
| fundamental90 | 42 臂 S 平台 0.84–0.88（waveBE242:346-372），2Y 过闸塔位 ×4 已入册（:372）；DB 台账 4 expr 0 bt | S 闸无闭合路径；塔位储备已登记 |
| fundamental93 | 12 臂水平 ≤0.53（waveBE242:108-123,268-287）+ 论坛 no_result（:261）；DB 台账 8 bt / 0 passed（本轮） | 弱水平 + 检索穷尽 |

### B. 伪集

| 数据集 | 排除理由（证据） |
|---|---|
| fundamental22 | RIC↔BBID 映射表伪集（waveBE242:265）；DB 台账 12 expr / 11 bt / 3 ra_clean 疑映射伪信号（get_mining_yield 本轮）；11-07 vec_avg 水平 2 几何 S 0.48（DATASET_USABILITY_MASTER_20261111.md:17）。**永不复检** |

### C. 数据层排除

| 数据集 | 排除理由（证据） |
|---|---|
| digital_ad_spend | 宽度塌缩：探针 lc 25/sc 25（~50/500），CW 0.5 vs limit 0.1（waveBE242:125-126） |
| alpha_factor_lib | 宽度塌缩：BE251 臂 DD 71%/199%/83%、margin −0.5~−5.7%（waveBE242:378-380） |

**小结**：12 集中 11 集三型排除完毕；唯一目标 = 用户指定的 **fundamental72**（§三）。
工具面异常（非数据集）：query_dataset_profile / query_field_profile 对 DEU 全 0 行（本轮实读）⇒ 记入盲区，不影响排除结论。

## 三、目标集 fundamental72：判死闸距离核对

### 3.1 台账事实（本轮实读）

- **历史臂数**：`get_mining_yield(DEU, by_dataset=True, strict=True)` → fundamental72：**expressions 10 / consumed 10 / backtested 10 / passed 0 / ra_clean 0 / prod_clean 0 / prod_blocked 0 / ra_unknown 0**（10 行 RA 状态均已知失败，prod 全未测）。另有近失波 2 臂在 alphas 表挂 dataset_id 1902：RREALzx0 / KPJmRpGN（get_alpha_by_id 本轮，created 2026-11-05）——**10 vs 12 口径差如实登记**：get_mining_yield 的 dataset 归属来自 expressions/backtest_rows 标注，近失波 2 臂未计入 fundamental72 名下。
- **字段面**（`get_field_catalog(DEU, fundamental72)` 本轮 + atom_orthogonal/fundamental72_fields.csv，1031 字段）：MATRIX 347 / VECTOR 684；平台 cov 列全 0.0（§8.11 ⑤：coverage 字段不作可用性判据）；**334 字段有平台用户足迹（uc>0）**，头部：`fnd72_s_pit_or_cf_a_cf_cash_from_oper` uc 70/ac 110（最挤）、`fnd72_s_pit_or_bs_q_1_bs_tot_asset` uc 17/ac 30、`total_liabilities_and_equity_value` uc 14/ac 20、`fnd72_s_pit_or_is_q_ebit` uc 11/ac 13、`fnd72_s_pit_or_is_q_sales_rev_turn` uc 7/ac 9、`fnd72_s_pit_or_is_a_ebit` uc 7/ac 8、`fnd72_s_pit_or_is_a_net_income` uc 6/ac 8。
- **在册近闸资产（get_alpha_by_id 本轮，DB 原值）**：
  - **RREALzx0**：`group_rank(·rank(ts_delta(fnd72_s_pit_or_is_q_ebit,240))·rank(ts_delta(...,176))·rank(ts_rank(...,1008)), sector)`，DEU/TOP500/D1/**FAST**；**S 1.42 / F 0.95 / 2Y 1.43 / TO 14.47% / sub 0.83** / margin 8.98bp / DD 9.29% / LC-SC 182-201；UNSUBMITTED，**prod_correlation=null / self_correlation=null（均未测）**。
  - **KPJmRpGN**：同几何于 `fnd72_s_pit_or_is_q_is_oper_inc`；**S 1.38 / F 0.90 / 2Y 1.58（已触 2Y 闸）/ TO 14.82% / sub 0.92** / margin 8.57bp / DD 9.62% / LC-SC 185-197；UNSUBMITTED，**prod/self 均 null**。
  - 两臂 neutralization=**FAST**，对 wave107 的 SUBINDUSTRY 构成第二套配置（D6 证据）。
- **ledger 面**（list_ledger_keys(DEU) 本轮）：**无 `fundamental72_dead` 键**（对照：`fundamental17_dead` 存在）；亦无 catalog/s1/s2 任何 fnd72 专属键（catalog_cache_fundamental17/6/86/89/90/93 均在，fundamental72 缺席）⇒ fnd72 的判死只存在于 registry dead_ends 层，从未升格为 ledger 判死键。

### 3.2 判死档距离（get_dead_ends 本轮 + 本地档，逐维对 AGENTS §7.6）

**在档两条死档（registry 层，均 dead_at 2026-10-31）**：
1. `DEU-FND72-CF-DETAIL-SPARSE`（id 1573，evidence_wave 107）：CF 明细/部分 BS 明细在 DEU/TOP500 覆盖 <2%（2–5 只），宽度≤5 时 CW(limit 0.1) 结构性必挂；F3 FCF/TA S 0.24、F6 三表 regime S 0.36、F7 Piotroski S −0.14 全灭且均触 CW。**「不是机制不成立，是字段没数据」= 数据层排除**。rule：只用 BS 主表 + cf_net_inc + cf_cash_from_oper 三字段族；派发前 1 条 rank(F) 探针验 longCount+shortCount ≥50。
2. `DEU-FND72-NARROW-BREADTH`（id 1574，evidence_wave 107）：十个结构互异模板（Sloan 应计/FCF/现金转化率/应计-CF 相关性倒U/三表 regime/Piotroski/回归残差/留存收益/折旧强度…）全灭，S 上限 0.37 距 1.58 差 4.3 倍；根因=年报字段仅 12–14% 覆盖（60–70/500），可用子集只有 TA+CFO+NI；methodology_tag=cross_region_prior_falsified（deu_campaign_20261030.md:11637-11701 §109、:11808）。

**关联工具档（跨集规律，非 fnd72 专属）**：`DEU-TVRL-SLOW-SIGNAL-BREAK`（id 1575）：年报级慢变量 + 宽度<100 上 ts_target_tvr_decay 禁用（F2 无 TVR 宽度 60-61/TO 11.92% → 套 TVR 宽度 5-5/TO 55.59%）。`DEU-BACKFILL-WINDOW-SUB-CLIFF`（id 1577）：慢变量 bf 窗口取 66；W=22 禁用；W=252 仅在 SUB≥0.30 余量时试。

**六维对照表**：

| 维 | 合格线 | fnd72 现状（本轮证据） | 判定 |
|---|---|---|---|
| D1 结构互异模板 ≥10 | ≥10 不同经济机制/算子几何 | wave107 十模板（死档 id 1574 payload + deu_campaign:11808） | **✓ 已达**（10 全灭，天花板 0.37 限于年报宽面） |
| D2 字段族自测 | 每个可用字段族 ≥1 实测 | 已实测：BS 主表 + CF 两行 + CF/BS 明细（证 cov<2%）+ IS 季度标量（EBIT/oper_inc，11-04）；**未实测**：IS 年度标量族（is_a_ebit uc7/is_a_net_income uc6/is_a_sales_rev_turn uc5）、CF q 族、BS q_1/q_2 全族、非 fnd72 前缀通用名 MATRIX 族（total_liabilities_and_equity_value uc14 等）——334 个有足迹字段中绝大多数无本地实测记录 | **✗ 未达**（部分族有先验足迹但零本地实测） |
| D3 矩全家 | 水平/一阶差/二阶波动/比值各≥1 | 水平✓（Sloan/RE，wave107）；比值✓（FCF/TA、现金转化率）；一阶差✓（RREALzx0/KPJmRpGN ts_delta240/176，DB 本轮）；二阶/分位✓（ts_corr 倒U wave107、ts_rank1008 近失波）——**证据散在两波档案，未按 D3 口径逐项留痕** | **部分达标（未逐项留痕）** |
| D4 分组轴 ≥2 | sector/industry/subindustry/market/bucket | 实际用过：industry（wave107 样例表达式，deu_campaign:11580-11581）+ SUBINDUSTRY（wave107 配置）+ sector（RREALzx0/KPJmRpGN，DB 本轮）；market/bucket 未测 | **✓ 达标（3 轴），bucket/market 2 轴未扫** |
| D5 非线性 ≥1 | signed_power/ts_rank/ts_quantile/trade_when/bucket | ts_rank（近失波，DB 本轮）；**trade_when 门控 / bucket / ts_quantile / signed_power 零实测** | **部分达标（仅 ts_rank 1 类）** |
| D6 配置 ≥2 | 宇宙×中性化×decay 至少变一维 | 中性化 2 套（SUBINDUSTRY wave107 / FAST 近失波）；**宇宙（恒 TOP500）×delay（恒 D1）×decay 从未变过** | **部分达标（宇宙/delay 轴未扫）** |

**结论：`DEU-FND72-NARROW-BREADTH` 不满足六维全达标 ⇒ 按 §7.6 只能作 PROVISIONAL 级排除，不是终判死。** 其中真正立得住的是**数据层排除**（CF/BS 明细 cov<2% 实证、年报宽面 12–14% 实证——这两条经本轮死档 payload 复核仍然成立）；而「IS 族缺失 / fnd72_s_ 标量路线封闭」子断言（deu_campaign:11585-11589）**已被 2026-11-04 近失波部分证伪**：季度 IS 标量族（fnd72_s_pit_or_is_q_*）实际产出 S 1.42/1.38 近闸件，且字段目录显示该族有 uc 5–11 平台足迹（get_field_catalog 本轮）。ledger 层无 fundamental72_dead 键、get_dead_datasets 19 集不含 fnd72 ⇒ 判死从未升格。

### 3.3 采用理由（出具）

1. **判死非终判死、标记不作唯一依据**：§7.5 纪律 + 本集判死不满足 §7.6 六维（D2/D5/D6 未达，D3 未留痕）⇒ 引用死档整集排除不成立；死档中有效的只是字段层数据排除（CF/BS 明细、年报宽面），本役臂表遵守之但不被其封集。
2. **在册近闸资产 = 类别内除 fnd1（已交付）外最近的近闸族**：RREALzx0 S 1.42/F 0.95 + KPJmRpGN 2Y 1.58 已触闸、F 距闸 0.05–0.10、S 距闸 0.16–0.20（DB 本轮原值）。**prod/self 均 null** ——「收割优先于重挖」（AGENTS §7.5）：先补测 prod/self（零仿真配额）即可判定这两条是否直接进提交链，再谈新臂。
3. **未扫维度明确且便宜**：D5 门控类（trade_when/bucket）、D6 宇宙×delay、D2 的 IS 年度标量族与通用名 MATRIX 族（uc 5–14 用户足迹、零本地实测）——臂表可直接落这些维，不与已扫维度重复。
4. **反方证据如实登记（不回避）**：① 11-14 处置「fnd72 浅探+强负先验（宽度 2-5），不再加注」（waveBE242:420，早槽档引 ：421 有 1 行漂移）；② §54.5 结构上限假说：fnd72 与 fnd45 两个不相关数据集全期 S 同停 1.42 ⇒ 读作 DEU/TOP500/D1 REGULAR 结构上限，处方=换 universe/换 delay/换区域（s2_nearmiss_rescue_20261104.md:4930-4937）——注意该判据原文写「两个以上」，实证基数恰为 2 集，处于判据边界；③ 千字段面 684 个 VECTOR 的强负先验（waveBE242:141）。本役加注期望值必须来自近闸件收割与未扫维度，**不在 1.42 几何上换皮重跑**；若结构上限解释成立，D6 的 universe/delay 轴正是其处方所指向的自由度。

## 四、机制假设（驱动臂表设计）

**fnd72 存活面 = IS 季度标量族（`fnd72_s_pit_or_is_q_ebit` / `is_oper_inc`）的 delta×ts_rank×group_rank 复合几何（S 1.42 已证，DB 本轮）**；S 缺口 0.16–0.20 的候选解锁轴按优先序：
① **近闸件收割**：RREALzx0/KPJmRpGN 补测 prod/self（零仿真）→ 过闸即入提交链；
② **D5 门控/非线性**：trade_when(盈利改善动量>0, 主腿) 与 bucket/ts_quantile 形态——近失波只有 ts_rank 一种非线性，门控未测；
③ **D6 配置轴**：universe/delay 变维（§54.5 处方轴）+ decay 扫描；
④ **D2 补族**：IS 年度标量族（is_a_ebit/is_a_net_income/is_a_sales_rev_turn，uc 5–7）与通用名 MATRIX 族单测（每族 ≥1 条，先过宽度探针）。
**硬边界（数据层排除，臂表全部遵守）**：CF 明细/BS 明细一律不派（cov<2% 实证，死档 id 1573）；年报宽面骨架先 rank(F) 探针验 longCount+shortCount ≥50；ts_target_tvr_decay 禁用（死档 id 1575）；bf 窗口基线 66（死档 id 1577）。

## 五、判读基准（S/2Y/sub/TO + 符号指纹）

| 轴 | 预期 | 依据 |
|---|---|---|
| S | 季度 IS delta 秩乘几何天花板 **1.42**（RREALzx0 DB 本轮）；裸年报宽面天花板 **0.37**（wave107）；§54.5 结构上限假说下纯几何加注期望有限，新自由度臂目标带 **1.5–1.7**；量级参照 = fnd45 基线 **S 0.96/2Y 1.73/sub 0.72**（waveBE242:35，2026-11-14 事实，非承诺） | get_alpha_by_id 本轮 + s2_nearmiss_rescue_20261104.md:4930-4937 |
| 2Y | DEU 天然达标轴（waveBE242:38）；本集近闸族 2Y **1.43–1.58**（KPJmRpGN 已触 1.58 闸）；目标 ≥1.58，裸水平 2Y<1.0 记「机制需条件化」指纹不记死 | get_alpha_by_id 本轮 + waveBE242:38 |
| sub | 近闸族 sub **0.83–0.92**（DB 本轮）；分组轴主用 sector（低覆盖面实证 sector>industry>subindustry，nearmiss §54.8.3）；sub<0.75 记稳健告警 | get_alpha_by_id 本轮 + s2_nearmiss_rescue_20261104.md:4963 |
| TO | 近闸族 **14.5–14.8%**（DB 本轮）；年报宽面基线 11.92%（无 TVR，死档 id 1575 payload）；目标 <20%，>25% 记结构性告警；**TVR 层禁用**（慢变量+宽度<100） | get_alpha_by_id 本轮 + get_dead_ends id 1575 |
| 符号指纹 | **衰减对称（翻转后 |S| 同量级）= 机制在/符号错，翻转保留；单向 = 事件型**（waveBE242:37）。IS delta 符号先验 = 盈利改善→做多（三 delta 同向乘积已证正向，RREALzx0/KPJmRpGN）；CW 是年报/明细字段的结构性死法（宽度≤5 必挂，死档 id 1573）——CW 挂 = 数据层指纹，不改符号重试 | waveBE242:37 + get_dead_ends id 1573 |

## 六、证据通道与盲区声明（AGENTS §8.11 ⑦）

1. 「10 bt / 0 passed / prod_clean 0」来自 DB 台账（get_mining_yield，本轮）；近失波 2 臂（RREALzx0/KPJmRpGN）在 alphas 表 dataset_id=1902（get_alpha_by_id 本轮）但未计入 get_mining_yield 的 fundamental72 行 —— 10 vs 12 口径差如实登记，不影响 0 passed 结论（两臂 S 1.38–1.42 未过 1.58）。
2. `query_dataset_profile`/`query_field_profile` 对 DEU 全 0 行（本轮实读，EUR 对照正常）⇒ DEU 无 profile 先验；字段目录取自 `get_field_catalog` 平台缓存 + 本地 `fundamental72_fields.csv`（1031 行，2026-11-10 落盘）。
3. 平台 cov 列全 0.0 与近闸件 LC-SC 182-201 的实测矛盾——按 §8.11 ⑤ 以探针/回测实测为准，coverage 字段不作可用性判据。
4. expressions 表不含 MCP 直连仿真盲区已知（AGENTS §8.11 ⑦ 实例二）；本档近失波 2 臂经 get_alpha_by_id 独立核得，未依赖 expressions 聚合。

## 七、与今日早槽 S0 档的关系（更正一条归属）

- 早槽档 `S0_DATASET_SCAN_FUNDAMENTAL_20261114.md:45` 将 **WjOLdO7o（S 1.42/2Y 1.82）记为 fnd72 的近闸件——归属有误**：该件是 **fundamental45 电话会 NLP** 的 LDA 主题意外臂；fnd72 的近闸件是 **KPJmRpGN/RREALzx0**（s2_nearmiss_rescue_20261104.md:4930 与 :4941 原文均为「对比 fundamental72 的 KPJmRpGN」）。本档已按 DB 原值更正（get_alpha_by_id 本轮）；早槽档不回改（他槽产物，且 CATEGORY_MATRIX :32 引用其行号）。
- 早槽档结论「fnd72 主面不再加注」是 11-14 槽位期望值判断（waveBE242:420），本档按用户指定目标重开 S0，两档并存：反方证据（结构上限假说 + 宽度负先验）已在 §3.3 第 4 条完整登记。
