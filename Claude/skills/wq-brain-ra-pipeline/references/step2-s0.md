# 步 2（S0）细则：数据集体检 + 金字塔配置

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 2。评分机制的实现细节在 `wq-brain-campaign-toolkit` §8（S0 评分机制）与 `references/probe-scoring-v2.md`，本文只写**何时用、怎么判、写到哪**。

## 2.1 有序清单（按此顺序，不要先锁白名单再读约束）

| # | 动作 | 调用 | 说明 |
|---|---|---|---|
| ① | 选集增强 | `python tools/campaign_intel.py s0-select --region $REGION --delay $DELAY --universe $UNIVERSE --top-n 15 --target $TARGET_SEATS` | `recommend_datasets`（平台真实点塔）× `get_mining_yield`（历史产出率）× `get_dead_datasets`（判死清单）三方交叉；无战役目录的跨区试探另有 `xr-probe` |
| ② | 校准（写盘） | `mcp__wq-brain-http__workflow_campaign(region, stage="S0", calibrate=true)` | 反学 category 权重 + 拥挤甜区，写回 `thresholds.json`；**不产出排名** |
| ③ | 打分 | `mcp__wq-brain-http__workflow_campaign(region, stage="S0")` | 按新阈值产出 `s0_ranking`；②③ 都要，③ 不是冗余重跑 |
| ④ | 按硬约束筛（2.3） | — | 已点亮塔不进白名单、至少 2 个非 MODEL … |
| ⑤ | 锁白名单 | `mcp__wqb-db__upsert_ledger_key(region, "s0_whitelist", {…}, mode="merge")` | 见 2.4；**用 merge，禁整值覆盖共享键**（2026-09-25 事故） |
| ⑥ | 体检包核对 | 见 2.5 | 白名单数据集须有 `field_inspect` 包 |

可选 ②′：`calibrate=true dry_run=true` 只预览不写盘，仅**新区 / 校准结果可疑**时才审。审两处异常：甜区 `ac`（alphaCount）异常巨大（如 MEA 8560–21508，反向奖励超拥挤）/ `strong_acs` 空（无强信号）→ **不要 apply**，先查 `ac` 来源（口径错会把区域全部 alpha 算成数据集拥挤，甜区反转后反向奖励超拥挤）；`strong_acs` 空则确认该区确实要甜区逻辑再 apply；再**回步 1 复核 `thresholds.json` 或手改**。处置表见 toolkit `references/probe-scoring-v2.md` §二。`recommend_datasets` 不能替代体检。

## 2.2 `s0-select` 输出标记 → 含义 → 动作

| 标记 / 列 | 含义 | 动作 |
|---|---|---|
| `hist_yield_rate` / `hist_backtested` | 历史产出率（严格口径）/ 样本量；`None` = 处女地 | `yield = 0` 且 `bt ≥ 8`（样本量下限 8：低于它产出率噪声过大）的集已被实证判死，不投槽位 |
| `maxS` / `fld` | 本区该集历史 max\|sharpe\| / 字段数 | 参考 |
| `[跨区弱:REG:maxS@bt]` | 同集在其它区 ≥16 条回测且 max\|S\|<1.0 | 降权（排在健康集之后、判死之前）；细则 `step1-inventory.md` §1.4 |
| `[跨区RA-clean:REG:n]` | 其它区的正证据 | 加分参考 |
| `fields<5` → `仅条件腿` | 只能做 `trade_when` / bucket 辅助腿或事件探针 | **不进主攻**；与步 3 的「字段数 < 10」阈值分开：< 5 仅条件腿，< 10 移出白名单 |
| `lit=Y` | 该 category 已点亮（当季 ACTIVE ≥ 3） | **直接剔除**（硬约束 0） |
| `[WARN] 结构性不可达` | 存活 top-n 的 Σ`est_seats` < `--target` | 扩集 / 换区，不在不足座位上反复打磨 |

**座位**：`--target N` = 本战役目标独立座位数（缺省建议 ≈ 3 × 目标塔数，因为一座塔要 3 颗点亮）；每候选带 `est_seats`（同族高互相关只算 1 座位）。`seat_model` 台账目前**没有写入方**（`docs/ledger_keys.json` 登记为 orphan），缺省每集按 2 个座位估——这是占位值，不是实测。

## 2.3 白名单硬约束（0–7）：哪些有代码执行，哪些是准则

| # | 约束 | 类型 | 执行点 / 反例 |
|---|---|---|---|
| 0 | **已点亮塔不进白名单**（2026-09-19 用户定案）：当季 ACTIVE ≥ 3 的 category（`recommend_datasets.category_lit=true`）不得作战役**主数据集**；其字段只能在未点亮塔主信号里作**辅助腿**（条件 / group / bucket / 中性化）。剩余全是已点亮塔 → 换区，不挖 | 硬（`s0-select` 剔 `lit=Y`） | 「候选」≠「白名单」：win 族（约束 1）进候选，但已点亮者不进白名单 |
| 1 | 读 `registry_empirical` win 层：已验证配方的数据集族**必须进候选** | 准则 | 与约束 0 冲突时以 0 为准 |
| 2 | `pyramid_quota_enable`：白名单至少 **2 个非 MODEL**（PV / NEWS / ANALYST / institutions）；不够则 tier2 上提，`tier_note=pyramid_quota` | 硬（`score_datasets`） | 全 MODEL 的白名单会把 PV / NEWS 整座金字塔挤出 generate 池 |
| 3 | `category_weight` 只允许 0.9–1.15 | 硬（config `MINING`） | 反例：1.3 vs 0.7 抹掉整座金字塔 |
| 4 | `*_dead` 仍排除；**主导腿禁用 ≠ 整集判死** | 硬 + 准则 | 情景：某集的主导字段 SELF ≥ 0.9 被禁，其余字段仍可用 → 不判死整集 |
| 5 | **白名单外禁止 generate / simulate** | 硬（闸 2） | 例外：`xr-probe` 本来就是跨区 / 跨集探测 |
| 6 | **饱和路由**：目标 dataset 平台 `alphaCount ≥ 1 万`（拥挤线；经验值，出自 2026-09-12 的实测样本），或该集**连续 2 波**模板全灭（`gate_results.all_pass` 全 0）→ 切 `brain-alpha-research-hypothesis-first`（**dormant，先看该 skill 的状态说明**），不再做模板遍历 | 准则 | 转 hypothesis-first 后步 5–8 仍照走（门禁与提交判定不因换生成路径而豁免） |
| 7 | **体检包就位**：白名单数据集须有 `field_inspect` 包（2.5） | 准则 + 模式开关 | 缺包按 `--inspect-mode` 处理，并写 `inspect` waiver |

## 2.4 `s0_whitelist` 最小形态

```json
{"universe": "TOP2500", "delay": 1, "datasets": ["pv1", "analyst4"],
 "entries": [{"dataset": "pv1", "tier": 1, "reason": "未点亮塔 × 高产出 × 未判死"}]}
```

读取一律经 `wqb.ledger_whitelist.normalize`（该键历史上有 5 种互不兼容形态）；wqb-db MCP 的 `upsert_ledger_key` 会自动归一契约键。写入前先 `get_ledger_key` 读现值，用 `mode="merge"` 增量写。

## 2.5 体检包（开区前置；治「三连复发」）

锁白名单后、进步 3 generate **之前**，须为白名单数据集补齐 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`。缺包时步 5 体检硬门**不生效**：低覆盖 / 厚尾 / 稀疏事件的预处理约束会一路裸奔到仿真。

```
ls tracking/mining/field_inspect_*.json                                  # ① 先查已有包（现状以 ls 为准）
python tools/gen_field_inspect_packs.py --all --dry-run                  # ② 缺则生成——纯离线：只读本地 WebData ZIP，不发平台请求、不耗配额
python tools/gen_field_inspect_packs.py --region <REGION> --delay <D>
```

**区域切换预筛自检**（field-quality §3，用户 2026-08-05 定的纪律）：换到一个新区回测前，先 `python tools/prescreen_gate.py --region <R>`（exit 0 = PASS / 1 = BLOCK）。BLOCK → 先按 [`brain-alpha-research-field-quality`](../../brain-alpha-research-field-quality/SKILL.md) §2 预筛并 `--record` 登记，或（数据包不覆盖该区时）`--record --source exempt` 登记免预筛理由。这是**工具级自检**，没有接入 workflow 节点。

**数据源覆盖边界**（勿误判为「忘了生成」）：本地快照 `research-data/WebData_20260219_V0.10.9.zip`（160 条数据集，仅 ASI / CHN / EUR / GLB / JPN / KOR / USA 七区；as_of 2026-09-17）**早于本期战役选集**——JPN 白名单 12 集中 0 集、DEU 9 集中 0 集落在快照内。这些区的包**无法由本地数据生成**，须先更新 WebDataScope 导出包再跑 ②。此前可显式降级 `--inspect-mode warn`，**但必须写 `inspect` waiver**（`python tools/waiver.py new --gate inspect …`，见 AGENTS.md §8.1.2），不得默认静默通过。

**缺包行为**（`tools/wave_gate.py --inspect-mode {off,warn,enforce}` / `WQB_INSPECT_MODE`；节点 `wave_gate` 同名参数）：`warn` = 缺省，告警放行；`enforce` = fail-closed，缺包即整波拦截，**新数据集首波自动升 enforce**。开新区 / 新数据集建议直接 `enforce`（同一 KOR/model109 无包：`warn` → EXIT 0 / PASS；`enforce` → EXIT 1 / FAIL）。三个同构闸（体检 / SEM / 区域闸）缺省值各异，总表见 [INDEX「闸与逃生口总表」](../../INDEX.md)。

## 2.6 评分机制增强（默认 OFF，需区域 `thresholds.json` 显式 opt-in；机制见 toolkit §8）

| 增强 | 何时打开 |
|---|---|
| **经验强度先验**（`empirical_weight > 0`） | 新区已有实测 best_sharpe：把目标从「数据干净 + 低拥挤」拉向「能过闸概率」 |
| **饱和再验证降级**（读 `saturated_datasets`） | 命中集自动降 `excluded` 且不被保底带复活（EUR `le8Y68K2` 一夜 prod 0.6929 → 0.9932、全族归零的教训）。**写入方 = `python tools/campaign_intel.py mark-saturated …`**（步 9 第 ⑥ 步调用；2026-09-29 补，此前该台账全仓库无写入方、这一项是空转）；无台账时零影响 |
| **universe 一致性守卫** | 默认随 score 生效：台账 universe ≠ `settings.universe` 即 `[WARN]`（跨 universe 的 coverage / alphaCount 不可比），白名单须据新 universe 复核重建 |
| **饱和拍平 model** | 区域进入饱和态时 model 类 `category_weight` 封顶 1.0；`score` = 信号强度榜，`pyramid_view` = 点塔战略榜，勿混排 |
| **calibrate token 去重** | 已内置（根治甜区污染），无需操作 |

## 2.7 产物与失败分支

- **产物**：ledger `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>`（键契约见 `docs/ledger_keys.json`）；本步 findings 写本波 `wave_results.key_findings`。
- **失败分支**：配额筛后仍无非 MODEL → 写 findings，不要退回纯 MODEL；全部被硬排除 → 回步 1 换 region（转 matrix 选区）。
