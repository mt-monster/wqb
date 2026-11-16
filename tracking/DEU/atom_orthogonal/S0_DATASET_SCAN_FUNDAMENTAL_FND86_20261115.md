# DEU S0 类别盘点：FUNDAMENTAL（2026-11-15）——目标集 fundamental86（收割优先）

> 任务：DEU × FUNDAMENTAL 类别 S0 盘点（atom_orthogonal 战役，交付目标 = ATOM：单数据集字段，group 轴豁免，2Y≥1.58 硬闸）。
> 本档与今日既有两份 S0 并存不冲突：`S0_DATASET_SCAN_FUNDAMENTAL_20261115.md`（他槽，目标 fnd72，在途 w1–w3）、`S0_DATASET_SCAN_FUNDAMENTAL_FND93_20261115.md`（目标 fnd93 重开裁定）。本档目标 = **fundamental86**，理由是「收割优先于重挖」（AGENTS §7.5★）：fnd86 已有两条 prod 判净近闸臂（N1PkQxEw prod 0.6347 / 1YW6xk3W prod 0.5593，均 < PRODCORR_CEILING 0.70），唯一缺口是 S（天花板 0.91 距闸 1.58）；而 fnd93 的 6 条高 S 臂 universe/neutralization/delay 全 NULL（幻影/配置快照未核），fnd72 是并行会话在途焦点，fnd31 零探无近闸臂。

## 一、区域面（本轮 MCP / DB 实读）

- 工具：经 `LocalToolSearch` 加载只读面 `select:mcp__wqb-db__get_dead_datasets,mcp__wqb-db__get_dead_ends,mcp__wqb-db__query_dataset_profile,mcp__wqb-db__query_field_profile,mcp__wqb-db__get_region_overview,mcp__wqb-db__get_campaign_summary`，逐个 `DeferredToolCall` 调用（本会话实跑）。
- DEU（`get_campaign_summary` 本轮回执）：**214 波（192 closed）/ 70 死路 / submit_ready=1**。
- `query_dataset_profile(DEU, category=FUNDAMENTAL)` = **0 行**；`query_dataset_profile(DEU)` 不带 category = **0 行**；`query_field_profile(DEU, family=盈利与财务)` = **0 行**（全部本会话实跑）。底层核验：`dataset_profile` 表 `region='DEU'` 0 行、`field_profile_full` 表 `region='DEU'` 0 行（sqlite 只读直查 `data/wqb.db`）⇒ **DEU 的画像表整体为空，逐集状态全部走 `datasets`+`backtest_results`+`expressions`+`alphas`+`ledger_kv` 五通道**（证据盲区，见 §五）。
- `get_dead_datasets(DEU)` = 19 键（含 `fundamental17`）；`get_dead_ends(DEU)` 中 FUNDAMENTAL 相关：`DEU-FND72-CF-DETAIL-SPARSE`（id 1573）、`DEU-FND72-NARROW-BREADTH`（id 1574）、`DEU-FND89-NONCURRENT-ACCRUAL-CEILING`（id 1576）、`DEU-FUND90-THREE-AXIS-EXHAUSTED-20261030`（id 1551）、`DEU-BACKFILL-WINDOW-SUB-CLIFF`（id 1577，工具规律跨集）。⚠ 判死档只作参考不作唯一依据（§7.5）。

## 二、排除面（逐集以本轮 DB 读数重认定；DEU=region_id 10，`datasets` 表 FUNDAMENTAL 13 集）

| 数据集 | 本轮读数（通道） | 排除类型与理由 |
|---|---|---|
| fundamental1 | DEU backtest 0 行；alphas 含已提交 ACTIVE（pwaQ0bx3 S1.60/2Y2.01/prod 0.6821，他槽 S0 档引 waveBE242） | **A 已收敛**：已提交 ACTIVE 占位，不再加注 |
| fundamental6 | DEU backtest 26 行（4 波）/ best_s 1.07（LLMbXJ76）/ best_2y 1.00；alphas 18 行 | **A 已收敛**：ATOM 天花板 1.15（他槽 S0 档:24），2Y 天花板 1.00 远低于 1.58 硬闸 |
| fundamental17 | DEU backtest 10 行 / best_s 0.31 / alphas 10 行全 COMPLETE | **A 已收敛**：台账 0 passed + 拥挤。在 `get_dead_datasets` 19 键之列，但排除依据 = 台账读数+拥挤，**不是 dead 标记**（§7.5） |
| fundamental22 | DEU backtest 11 行：best_s 1.72 的 4 行 code='R99' 占位伪行（payload `failed_checks` 空、universe/neut 全 NULL）；真实表达式天花板 = 0.42（波104 vec_count/vec_avg/ts_zscore） | **B 伪集**：S1.72 系映射表伪信号（code='R99' 非表达式），不可复现；字段仅 1 个向量字段 `fnd22_value`，真实信号面已测 5 类几何全 ≤0.42。**永不复检** |
| fundamental45 | DEU backtest **0 行** / alphas **0 行** / expressions 0 行（全区域） | **A 已收敛（QA 线）**：「78 臂收敛 S≤1.04」源自他区域通道（waveBE242:6），DEU 本地零臂。仅保留量级参照（基线 S 0.96/2Y 1.73/sub 0.72，2026-11-14 事实非承诺） |
| fundamental72 | DEU backtest 53 行：波107（10 臂，SUBINDUSTRY，S≤0.37）+ **w1/w2/w3（28/8/7 臂，FAST 中性化，2026-11-14/15 在途）**；w1 best ZYaqv2L0 S 1.47/F 1.03/2Y 1.16（闸线 1.58，FAIL LOW_SHARPE 差 0.11、LOW_2Y 差 0.42，payload 实读） | **活体（并行会话在途焦点）**：w1–w3 用 `fnd72_s_pit_or_is_q_*` PIT 季度利润表标量字段——正是 10-31 死档 id 1574 声称「全部 not found」的字段族 ⇒ 死档针对的是年报 BS/CF 明细（id 1573/1574 判据成立范围仅限明细字段），PIT 标量族为新自由度。provisional，六维 D3/D6 未达。**本轮不动他槽焦点** |
| fundamental86 | DEU backtest 20 行（波110 十臂 + w1 十臂）/ best_s **0.91**（N1PkQxEw）/ best_2y 1.07；alphas 20 行，**N1PkQxEw prod 0.6347 / 1YW6xk3W prod 0.5593 均判净**（< PRODCORR_CEILING 0.70） | **本轮目标集**（见 §三） |
| fundamental89 | DEU backtest 20 行 / best_s 0.98 / best_2y 1.91；死档 id 1576（三波 24 臂四轴穷尽，S 天花板 0.98 距闸 1.61×） | **A 已收敛**：六维终判死（2026-11-14 复核维持）。**不外推为邻接应计族（fnd93）先验**（waveBE242:251 明文） |
| fundamental90 | DEU backtest 0 行 / expressions 4；死档 id 1551（三轴穷尽 S 上限 1.20 距闸 32%，剩 46 字段停广扫） | **A 已收敛（capped）**：塔位储备已入册（2Y 塔位 ×4），非重挖面 |
| fundamental93 | DEU backtest 8 行（fnd93_accruals_probe，S≤0.36）；alphas 16 行，其中 **6 条 S 1.59–1.70/2Y 1.59–2.32 但 universe/neutralization/delay 全 NULL、prod 全 NULL**（YBbZAXvN/MhHyLY69/wWPcygbY/RYtSG1Lr/r0jEGh24/KJh7h1VN） | **PROVISIONAL-待核**：今日 FND93 S0 档已裁「重开收割」，但这 6 条臂配置未回填（MCP 直连幻影风险未除——同表达式在 backtest_results DEU 实测 S≤0.36，alphas 表 S 1.7 疑为跨区/异配置快照，本会话核对 `alphas.region_id=10` 但 `universe IS NULL`）。配置归属未核实前**不构成收割就绪面**，且已有他槽 S0 档占用该集 |
| fundamental31 | DEU backtest **0 行** / expressions 0 行 / alphas 0 行（**全区域零臂**）；datasets id 1004：48 字段、coverage 0.3955 | **未探（零先验）**：完全未开，无任何臂数支撑其优先级高于 fnd86 的 prod 判净近闸池（收割优先于重挖）。列为 fnd86 之后的备选 |
| alpha_factor_lib | DEU backtest 0 行 / alphas 0 行；datasets id 969：65 字段、coverage 0 | **C 数据层排除**：BE251 超窄账户签名（他槽 S0 档:42），coverage 0 零覆盖 |
| digital_ad_spend | DEU backtest 0 行；alphas 3 行（含 RREA0LZg S −11.71 异常行，疑脏数据）；datasets id 992：9 字段、coverage 0 | **C 数据层排除**：探针 lc 25/sc 25 宽度塌缩、CW 0.5 挂（他槽 S0 档:41），数据层排除非信号死 |

**排除面小结**：A 已收敛 6 集（fnd1/6/17/45/89/90）+ B 伪集 1 集（fnd22）+ C 数据层排除 2 集（alpha_factor_lib/digital_ad_spend）= 9 集排除；fnd72（他槽在途焦点）与 fnd93（他槽 S0 已占、配置未核）本轮避让；fnd31 零探备选；**fnd86 = 本轮目标集**。

## 三、目标集：fundamental86（收割优先裁定）

### 3.1 选定理由（机制先验 + 历史臂数 + 判死闸距离）

- **历史臂数少**：仅 2 波 20 臂（波110 十臂 + w1 十臂），远未到判死线（§3.3 六维）。
- **prod 判净近闸池已存在**（收割优先于重挖，§7.5★）：N1PkQxEw（S 0.91/F 0.70/2Y 0.97/sub 0.55/TO 0.057，prod 0.6347）与 1YW6xk3W（S 0.76/F 0.83/2Y 0.71/sub 0.35/TO 0.025，prod 0.5593），两条 prod 均 < 0.70 判净 ⇒ **零仿真配额即有两条候选腿**，唯一缺口是 S（0.91 距 1.58 差 0.67）。
- **机制先验**：fnd86 是 7 字段的综合评分集（average/fundamental/earnings/price_momentum/relative_valuation/risk/insider_trading score）。w1 最佳 N1PkQxEw = `group_rank(group_backfill(ts_mean(ts_backfill(fnd86_average_score,250),22),sector,250), bucket(...relative_valuation...))` —— **平均评分水平型 + 估值分桶**形态，机制 = 基本面质量-估值复合溢价。
- **判死闸距离**：无任何 fnd86 死档；六维未达（§3.3），「判死」无从谈起。

### 3.2 机制假设（驱动臂表设计）

> **一句话机制假设**：fnd86 的「基本面综合评分 × 相对估值」复合因子在 DEU/TOP500 定价的是**质量-估值错配溢价**——average_score 高的公司（基本面质量好）在估值分桶低位时被市场低估，做多高质量-低估值组合；信号载体是**平滑水平秩**（ts_backfill 250 + ts_mean 22），估值分桶（bucket）提供非线性自由度，S 缺口需靠**未测机制轴**（二阶矩/信噪比/分组轴切换/非线性/配置轴）补足而非重复水平型。

### 3.3 判死闸距离（六维，AGENTS §7.6）

| 维度 | 现状（本轮 DB 读数） | 达标 |
|---|---|---|
| D1 结构互异模板 | 20 臂覆盖 ~6 类：水平秩 / 平滑秩（ts_mean+backfill）/ 一阶差 ts_delta / trade_when 门控 / 比值 divide / 评分分歧 subtract(rank,rank)；缺二阶波动、峰值距离、自引用分桶 | ✗（<10） |
| D2 字段族自测 | 7 字段中已测 6（average/fundamental/earnings/price_momentum/relative_valuation/risk/insider_trading——insider_trading 已测 kqaeVEY6 −0.39、j2aN3zKW 0.22）；全字段族至少 1 条实测 | 近达（6/7 族有实测，insider 族已实测） |
| D3 矩全家 | 有水平（O0WKrQjb ts_backfill 0.52）+ 一阶差（gJa7QkV0 ts_delta 0.56）；**缺二阶波动（ts_std_dev 单用）、信噪比** | ✗ |
| D4 分组轴 | sector 主导（绝大多数臂）；bucket 已出现（N1PkQxEw）；**缺 subindustry/industry/market 对照** | ✗（<2 明确对照） |
| D5 非线性 | trade_when 门控有（1YW6xk3W/9qxPJqR9/rK7Q5pw9）；**缺 signed_power/ts_rank/ts_quantile** | 部分 |
| D6 配置 | 全部 DEU/TOP500/D1/SUBINDUSTRY/decay4 **单配置**；无宇宙×中性化×decay 变体 | ✗ |

⇒ fnd86 距判死线很远（D1/D3/D4/D6 全缺），任何「关闭」表述不成立，记 **PROVISIONAL-活体收割池**。

### 3.4 ATOM 合规性

- 7 个字段全 `fnd86_*_score`，单一数据集（datasets id 1008，field_count 7，MATRIX，value_score 4，delay 1）。现有臂 group 字段仅 sector/bucket（豁免内）。**无跨集 add**，纯单集 ATOM。

## 四、判读基准（S/2Y/sub/TO 预期 + 符号指纹）

- **硬闸**：2Y≥1.58（ATOM 免 IS_Ladder）。fnd86 当前 best_2y = 1.07（rK7Q5pw9），**2Y 与 S 双缺**——这是与 fnd93（2Y 已过闸、只缺配置核实）的本质差异，本轮目标是把 S 从 0.91 抬向 1.58 同时把 2Y 从 1.07 抬向 1.58。
- **S 预期**：天花板 0.91（N1PkQxEw）。量级参照（2026-11-14 事实非承诺）：fnd45 基线 S 0.96/2Y 1.73/sub 0.72。fnd86 与 fnd45 同属 FUNDAMENTAL 慢变量评分/质量族，S 量级应在同区间；0.91→1.58 缺口 0.67 需靠 §3.3 未探轴（二阶矩/信噪比/subindustry 分组/signed_power/配置变体）补，不指望水平秩再加窗。
- **2Y 预期**：当前 1.07，缺口 0.51。w1 的 2Y 分布：rK7Q5pw9 1.07 / N1PkQxEw 0.97 / 1YW6xk3W 0.71 ⇒ 2Y 随 S 同向但弹性不足，**抬 2Y 优先于抬 S**（2Y 硬闸，S 还有 FAST/异配置回旋）。
- **sub 预期**：N1PkQxEw sub 0.55（>0.52 稳健线边缘）、1YW6xk3W sub 0.35（欠账）。sub 是次级缺口，subindustry 分组轴（D4 未探）是抬 sub 的首选杠杆。
- **TO 预期**：fnd86 全臂 TO 0.025–0.090（2.5%–9%），慢变量评分族天然低 TO，**无换手墙**；TO 不是本集约束，压低 TO 的杠杆（ts_mean 长窗）可自由用于换 S/2Y。
- **符号指纹**：机制 = 做多高 average_score（表达式正号水平秩）。N1PkQxEw / O0WKrQjb / rK7Q5pw9 正号水平臂 S 全为正（0.52–0.91），insider_trading_score 正号臂 S 为负（kqaeVEY6 −0.39）⇒ **average/fundamental 族正号为机制在；insider 族负号（反向）为符号指纹**。若新臂「做空 average_score S 为正」= 符号错/机制翻转，立即停。**衰减对称**（ts_backfill 250 + ts_mean 22 的平滑衰减两侧同向）= 机制在；衰减不对称 = 符号错。

## 五、盲区与证据通道声明

- **DEU 的 query_dataset_profile / query_field_profile 全 0 行**（本会话实跑）⇒ 类别分母与逐集状态不走 profile 表，走 `datasets`+`backtest_results`+`expressions`+`alphas`+`ledger_kv` 五通道。
- **§8.11⑦ 盲区实证**：fnd93 的 6 条高 S 臂只在 `alphas` 表、universe 全 NULL（MCP 直连通道，不写 backtest_results/expressions）；fnd22 的 S1.72 系 code='R99' 占位伪行（同表内伪信号）。⇒ 本档所有「S 天花板」一律以 `backtest_results` 的 DEU 实测 + 真实表达式（code 非占位符）为准，`alphas.sharpe` 在 universe 为 NULL 时不采信。
- **fnd72 w1–w3 为并行会话在途波**（2026-11-14/15，FAST 中性化）：本档只登记其存在与判读（w1 S 1.47 差闸 0.11），不抢占、不将其读数外推为 fnd86 先验（FAST vs SUBINDUSTRY 配置不同，fnd72 vs fnd86 字段族不同）。
- **本轮未做（如实）**：平台相关性复测（fnd86 的 prod 0.6347/0.5593 是 alphas 表既有读数，本轮未回源）、`get_alpha_details` 配置核对、年度分年、任何新仿真——S0 盘点边界内零平台调用。fnd86 两条判净臂的 self-corr、近十年持仓连续性**未测**，是收割槽的下一动作。

## 六、产物与复跑

- 本档：`tracking/DEU/atom_orthogonal/S0_DATASET_SCAN_FUNDAMENTAL_FND86_20261115.md`
- 证据出处（全部本会话实跑）：
  - MCP：`get_campaign_summary(DEU)`（214 波/70 死路/1 submit_ready）、`get_dead_datasets(DEU)`（19 键）、`get_dead_ends(DEU)`（id 1551/1573/1574/1576/1577 等 FUNDAMENTAL 相关档）、`query_dataset_profile/query_field_profile(DEU)` = 0 行。
  - DB 直查（sqlite 只读，`data/wqb.db`）：`datasets`（region_id=10，FUNDAMENTAL 13 集：id 969/992/1001/1002/1003/1004/1005/1006/1007/1008/1009/1010/1011）；`backtest_results`（region='DEU' 逐集臂数/天花板/波次）；`alphas`（region_id=10 逐集行数/prod/universe NULL 幻影识别）；`expressions`（fnd22 code='R99' 伪行识别、波104 真实臂）。
- 复跑口径：`world-quant-brain-mcp/.venv/Scripts/python.exe -X utf8` + sqlite3 只读连接（本会话全部查询均为只读 SELECT，零写入）。
- PRODCORR_CEILING=0.70（`src/wqb/config.py`，与今日 FND93 S0 档复跑口径一致）。
- 不覆写他槽档案：与 `S0_DATASET_SCAN_FUNDAMENTAL_20261115.md`（fnd72）、`S0_DATASET_SCAN_FUNDAMENTAL_FND93_20261115.md`（fnd93）并存，三档目标集互不重叠。
