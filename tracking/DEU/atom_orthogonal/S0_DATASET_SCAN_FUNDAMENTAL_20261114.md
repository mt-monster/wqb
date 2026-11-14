# DEU S0 类别盘点：FUNDAMENTAL（2026-11-14）

> 任务：DEU × FUNDAMENTAL 类别 S0 盘点——排除面三型重认定（已收敛 / 伪集 / 数据层排除），目标集 = **fundamental86**（用户指定），
> 核对其判死闸距离（六维 D1–D6 + 历史臂数）并出具采用理由；判读基准含 S/2Y/sub/TO 预期与符号指纹。
> 先验来源：本轮 MCP 实读（`get_mining_yield(region=DEU, by_dataset=True, strict=True)` / `get_dead_datasets(DEU)` / `get_dead_ends(DEU)` /
> `get_field_catalog(DEU, fundamental86)` / `get_campaign_summary(DEU)` / `get_region_overview()`）+ 本地档案（逐条 path:line）。
> 判死纪律：AGENTS.md §7.5（判死标记不得单独作排除依据）+ §7.6（六维穷尽闸，缺维只能 PROVISIONAL）+ §8.11 ⑤（cov=0 不是数据存在性判据）。

## 一、区域面（本轮 MCP 实读）

- DEU：211 波（189 closed）/ 70 死路 / submit_ready=1（`get_campaign_summary`，本会话）。
- ⚠ **证据通道盲区（如实登记，AGENTS.md §8.11 ⑦ 纪律）**：`query_dataset_profile` 与 `query_field_profile`
  在 region=DEU 下均返回 **0 行**（本会话两次实读；该两表只有 EUR 数据，updated_at 2026-10-25）。
  ⇒ DEU 数据集级/字段级先验**不走 profile 表**，本档案全部改用
  `get_mining_yield`（backtest_results 台账）+ `get_field_catalog`（平台缓存 2026-09-23）+ 本地战役档案三通道。
- 类别语境：FUNDAMENTAL 塔 1/3 点亮、×1.8 乘数（`waveBE242_FND89_ACCRUAL_ATOM_20261114.md:452` fnd1 闸②）；
  pwaQ0bx3（fnd1）已于 2026-11-14 提交 ACTIVE（同档 :461，篮 17→18/20）；submit_ready=1 为 3q0gZE0N（:492，prod 槽位排队）。

## 二、排除面（三型，逐集以本轮读数重认定）

### A. 已收敛（历史臂数 + 天花板读数）

| 数据集 | 本轮读数 | 排除理由（证据） |
|---|---|---|
| fundamental45 | QA 78 臂收敛 S≤1.04（waveBE242:6）；基线 S 0.96/2Y 1.73/sub 0.72（:35）；12/12 矩阵「穷尽（0.96 塔位×2）」（:412） | QA 面已收敛不再加注；**保留为本役量级参照**（非承诺） |
| fundamental89 | 六维终判死（2026-11-14，今日 22 臂 + 历史 20 臂；S 天花板 ~1.0；2Y ≤1.02 vs 闸 1.58；D1–D6 逐维举证，waveBE242:240-251）；旧轴另载死档 DEU-FND89-NONCURRENT-ACCRUAL-CEILING（`get_dead_ends` id 1576） | 六维合规死，判死依据=读数。**不外推为 fnd86 先验**（同档 :251 明文「不改写邻接数据集先验」） |
| fundamental90 | 破闸失败：42 臂 S 平台 0.84–0.88（BE250 收割 waveBE242:346-372），剩余结构手段（合成/锐化/包装/窗/轴/平滑）全部实测；2Y 过闸塔位 ×4 已入册（gJa7kj7v 0.84/1.68 等，:372） | S 闸无可见闭合路径；塔位储备已登记，不再开主攻 |
| fundamental93 | 实质关闭：12 臂水平 ≤0.53（BE245/BE248，:108-123,268-287）+ 论坛 no_result（:261）+ 文献正解（治理×税）跨集不可 ATOM（:261） | 弱水平 + 检索穷尽；资产增长种子 0.53/2Y 0.95 已登记（:121-123） |
| fundamental1 | **已收割**：pwaQ0bx3 S 1.60/F 1.40/2Y 2.01/prod 0.6821 已提交 ACTIVE（:441-461）；网格收敛封顶 1.53→1.60（:388-406） | 剩余仅待「跨族合成授权」再启（:405-406），本役不开 |
| fundamental6 | ATOM 天花板 1.15 + 主面 0.37（:422）；oiadpq 单点 1.73 被 Wje5K71x 占用（DATASET_DISPOSITION_MAP_20261111.md:14）；台账 26 臂 0 passed（get_mining_yield 本轮） | 单点已被占用 + 类别内收敛 |
| fundamental17 | DEU 台账 10 臂 0 passed（get_mining_yield 本轮）；11-14 矩阵「浅探（已标死，拥挤）」（waveBE242:422） | ⚠ 排除依据 = **台账 0 passed + 拥挤**，非 dead 标记本身（`get_dead_datasets` 含 fundamental17，但 AGENTS.md §7.5 实证死标记集仍在出货，标记不作单独依据） |

### B. 伪集

| 数据集 | 排除理由（证据） |
|---|---|
| fundamental22 | RIC↔BBID 映射表伪集：字段名头「质量/ESG」实为映射表（waveBE242:265），其 3 颗 ra_clean 疑似映射伪信号、**永不复检**；11-07 vec_avg 水平 2 几何 S 0.48 判死（DATASET_USABILITY_MASTER_20261111.md:17） |

### C. 数据层排除

| 数据集 | 排除理由（证据） |
|---|---|
| digital_ad_spend | 宽度塌缩：探针 lc 25 / sc 25（~50/500），CONCENTRATED_WEIGHT 0.5 vs limit 0.1 挂（waveBE242:125-126）——数据层排除，非信号死 |
| alpha_factor_lib | 宽度塌缩：BE251 臂 DD 71%/199%/83%、margin −0.5~−5.7%（超窄账户签名，:378-380） |
| fundamental72 | CF/BS 明细宽度 2–5（死档 DEU-FND72-CF-DETAIL-SPARSE，`get_dead_ends` id 1573；数据层排除非信号死）；EBIT 主面有近闸件 WjOLdO7o 1.42/2Y 1.82（s2_nearmiss_rescue_20261104.md:4941）但 11-14 处置=不再加注（waveBE242:421） |

**排除面小结**：FUNDAMENTAL 12 集中 11 集三型排除完毕（上表 11 行），唯一未排除 = **fundamental86**。

## 三、目标集 fundamental86：判死闸距离核对

### 3.1 台账事实（本轮实读）

- **历史臂数**：expressions 10 / backtested 10 / **passed 0**（strict S≥1.58 & F≥1.0，`get_mining_yield` 本轮 DEU fnd86 行）；prod_clean=0，ra_unknown=0（10 行 RA 状态均已知）。
- **字段面**：7 字段全 MATRIX，1–10 十分位复合评分（earnings/fundamental/relative_valuation/price_momentum/risk/insider_trading/average 七支柱，higher=better；`get_field_catalog(DEU, fundamental86)` 本轮）。平台竞争度：earnings_score 25u/40a 最挤，**insider_trading_score 0u/0a（零竞争）**，risk/momentum/valuation 2–5u。
- **数据存在性**：字段级探针已核——fnd86_earnings_score 真实有数（ac 87，跨度 **2014–2023** 无空窗，cov0_audit_final_20261109.csv:29）。宽度 87/500 ≈ 17%（窄）。
- **判死-撤判链**：11-04 曾因 cov0 判死（s2_nearmiss_rescue_20261104.md:4953）→ 11-05 **撤回**（:4973「证据不成立…必须用字段级 cov 或探针重新取证」）→ 11-09 探针证存在（csv:29）→ 11-14 矩阵标「**近穷尽（7 字段 0 passed）**」而非终判死（waveBE242:423）。

### 3.2 六维距离（AGENTS.md §7.6 口径，逐维举证）

| 维 | 合格线 | fnd86 现状 | 判定 |
|---|---|---|---|
| D1 结构互异模板 ≥10 | ≥10 个不同经济机制/算子几何 | 有读数可考的仅 **5 臂**（deu_campaign_20261030.md:512-516）：水平 rank 0.94 / ts_delta66 **静默全 NaN** / ts_zscore252 0.46 / 两臂 subtract 0.57、0.38——结构同族（group_rank 一层 + 少量 ts 变换），且 1 臂系 NaN 无效 | **✗ 远未达** |
| D2 字段族自测 | 每个可用字段族 ≥1 条实测 | 只测过 **1/7**（earnings_score）；`_recheck_expr_only.json`（atom_orthogonal/）记 used=1 / untested=6；insider_trading_score（零竞争）/risk/momentum/valuation/average/fundamental 六支柱从未单测 | **✗ 远未达** |
| D3 矩全家 | 水平/一阶差/二阶波动/比值各 ≥1 | 水平 ✓（0.94）；一阶差那条因未 backfill 全 NaN（无效读数）；二阶波动 ✗ 从未；比值 ✗（subtract≠比值） | **✗ 未达** |
| D4 分组轴 ≥2 | sector/industry/subindustry/market/bucket | 仅 sector 一轴（:512-516） | **✗ 未达** |
| D5 非线性 ≥1 | signed_power/ts_rank/ts_quantile/trade_when/bucket | 零命中 | **✗ 未达** |
| D6 配置 ≥2 | 宇宙×中性化×decay 变一维 | 单配置（DEU/TOP500/D1/SUBINDUSTRY/decay4） | **✗ 未达** |

**结论：六维零命中，距判死线极远。**「近穷尽」标签所依据的 10 臂不满足 D1（≥10 结构互异——可见 5 臂里 1 臂无效、余 4 臂同族），
按 §7.6 探针（<10 有效臂）只能输出「继续/停止加注」，不构成判死。**fnd86 可以合法开波。**

### 3.3 采用理由（出具）

1. **类别内唯一活体**：其余 11 集全部三型排除（§二），fnd86 是 FUNDAMENTAL 类别内唯一「未收敛、非伪集、非数据层排除」且有 6/7 字段从未单测的集。
2. **撤判链闭环**：旧死档证据链已被本仓纪律撤回（:4973），数据存在性已由字段级探针重取证（csv:29）——引用旧死档作排除即违反 §7.5。
3. **零竞争字段面**：insider_trading_score 0 用户 0 alpha（`get_field_catalog` 本轮），risk/momentum/valuation 2–5u——新臂 prod 相关性风险低于 earnings_score 拥挤面。
4. **类别级杠杆已备**：fnd90 实证「成熟公开评分水平被定价，条件化是正解」——杠杆 C `trade_when(自身动量>0, group_rank(评分, sector), -1)` 在评分族 S+0.7~0.9 / 2Y+1.8~2.0（waveBE242:283-284,309-317）。fnd86 与 fnd90 同为「公开复合评分」形态，杠杆可迁移但**必须本集实测**（nearmiss §54.8.2 杠杆迁移率 1/3 教训，s2_nearmiss_rescue_20261104.md:4962）。
5. **两个结构性先敌已有解药**（设计约束，非排除理由）：① TO 40%（:512 实测，是 fnd89/fnd1 族 3–5% 的 10 倍）→ 派发前预平滑；② CW 0.5 FAIL + 多空 75/231 偏斜（:512）→ gBF 形态修 CW（fnd1 BE259 实证，:429-431）。

## 四、机制假设（驱动臂表设计）

**公开复合评分族：水平已被定价（可复现天花板 ~0.94），信号在「未测支柱字段 + 跨支柱相对构造 + 杠杆C 条件化」三轴**；
TO 40% 与 CW 偏斜是本集两个先敌，臂表必须以 ts_backfill→平滑→gBF/tail 形态预处理，裸 rank 一律不派。
未测字段优先序：insider_trading_score（零竞争）→ risk_score → price_momentum_score → relative_valuation_score → average/fundamental_score；
跨支柱相对构造（sentiment27 教训：信号在字段间相对关系不在水平，dead_ends id 1585）与「改善动量门控」（杠杆 C）并行成臂。

## 五、判读基准（S/2Y/sub/TO + 符号指纹）

| 轴 | 预期 | 依据 |
|---|---|---|
| S | 裸水平复现 ~0.94 天花板；条件化/未测字段组合目标带 **1.2–1.6**（杠杆 C 实证上界 +0.7~0.9）；量级参照 = fnd45 基线 **S 0.96 / 2Y 1.73 / sub 0.72**（2026-11-14 事实，waveBE242:35，非现行承诺） | deu_campaign_20261030.md:512-525 + waveBE242:283-284 |
| 2Y | 裸水平 2Y 0.00/−1.17（本集最弱轴，:512,514）；DEU FUNDAMENTAL 2Y 为天然达标轴 + 杠杆 C 2Y+1.8~2.0 ⇒ **条件化后 ≥1.58 可期待**；裸水平 2Y<1.0 记「机制需条件化」指纹，**不记死** | waveBE242:38（2Y 天然轴）+ :309-317（杠杆 C） |
| sub | lc 87 ≈ 17% 宽度 ⇒ 分组轴必须粗（sector/bucket）；参照下沿 fnd45 sub 0.72；低覆盖细分组实证 sector 1.30 > industry 0.38 > subindustry 0.30（nearmiss §54.8.3，s2_nearmiss_rescue_20261104.md:4963） | cov0_audit_final:29 + nearmiss |
| TO | **本集特异**：裸 rank TO 40% 实测（:512），F 闸结构性必挂（S 0.94 → F 0.39 实证同排）；预平滑（ts_backfill + ts_mean/ts_decay_linear + trade_when 保持）后目标 <20%，平滑后仍 >25% 记结构性告警 | :512 + fnd1 平滑形态 waveBE242:399 |
| 符号指纹 | score higher=better ⇒ 水平做多高分；**衰减对称（翻转后 |S| 同量级）= 机制在/符号错，翻转保留**；单向 = 事件型，禁止对称放大；动量门控符号先验 = 分数改善→做多（fnd90 同构） | S0_DATASET_SCAN_20261113.md:67 + waveBE242:37 |

## 六、证据通道与盲区声明（AGENTS.md §8.11 ⑦）

1. 「10 臂 0 passed」来自 DB backtest_rows 聚合（get_mining_yield，本会话）；本地档案只定位到 **5 臂读数**
   （deu_campaign_20261030.md:512-516，2026-10-30 战役）。其余 ~5 臂未在本地档案定位到逐臂读数——口径差异如实登记，不影响 0 passed 结论。
2. `query_dataset_profile`/`query_field_profile` 对 DEU 全空（本会话实读）⇒ DEU 无 profile 表先验；字段目录取自平台缓存（fetched_at 2026-09-23，`get_field_catalog` cache_metadata）。
3. 平台字段级 coverage 报 0.0 与探针实证（ac 87）矛盾——按 §8.11 ⑤ 以探针为准，coverage 字段不作可用性判据。

## 七、S0 产物清单

- 排除面 11 行（三型）+ 目标集 1 集（fnd86）+ 判读基准一节，全部证据 path:line 或本会话 MCP 调用名。
- 本役臂表设计入口：§四机制假设 + §五判读基准；派发前预检项 = ①全臂带 ts_backfill 预处理；②TO 预算（裸 TO 40% 先敌）；
  ③CW 预算（gBF 形态）；④首臂必含 1 条零竞争字段单测（insider_trading_score，D2 补维）。
