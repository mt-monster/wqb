---
name: wq-brain-ra-pipeline
description: "REGULAR Alpha 挖掘唯一编排入口。当用户要求在某区域挖 RA / 开战役 / 从零到提交 / 挖 regular alpha / 挖因子 / 持续自我探索 / 日内循环 / 一键战役 / auto campaign / 选数据集/中性化/窗口 / 批量回测 / 发批 / 提交批次 / 达到可提交 Alpha 后停止时使用。PPA / Power Pool 仅当当前主题匹配 region/delay/universe 时作为本 SOP 的分支，不另起编排器。本 skill 只做编排，每一步调既有 skill 或 MCP 工具"
layer: L-RA
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "2.2"
last_verified: 2026-09-15
---

# WQ BRAIN RA Pipeline（唯一挖掘编排 SOP）

`brain-deepExplore` 已废止并入本文件。不要再读、再 invoke 那份 skill。

三角分工：

| skill                       | 职责                                        |
| --------------------------- | ----------------------------------------- |
| **本 skill**                | when / what / 怎么挖 Regular Alpha（S-PRE→S6）|
| `wq-brain-campaign-matrix`  | where = 查表选区选集                            |
| `wq-brain-campaign-toolkit` | how = 战役目录内执行引擎                          |

单条表达式修复走 `wq-brain-alpha-optimization-v1`。SUPER 组套走 `wq-brain-superalpha`。
PPA 主题核查可查 `wq-brain-ppa-mining`，编排仍走本 SOP 的 PPA 分支。

## 运行前置（一次性）

```powershell
# $WQ_PY 定义见 INDEX.md「运行环境铁律」，本文件只引用不复制
$REGION = "KOR"        # 唯一输入
```

铁律：**MCP 应用尽用**——能走 MCP 工具的步骤一律走 MCP，不手写 PowerShell 命令。
网络调用走 MCP venv（`$WQ_PY`）；禁止手写 requests。PowerShell 用 `;`；中文 JSON 走 `@file`（AGENTS.md §5）。
阈值不复写，引用 `src/wqb/config.py` 的 `GATES`。

阶段决策见 [references/decision-table.md](references/decision-table.md)。优先级：用户显式指令 > 决策表 > 本正文。
提示词模板（开新区 / 续波 / 发批 / 单条修复 / 日循环，以"可过闸 REGULAR alpha"为目标）见 [references/ra-campaign-prompt.md](references/ra-campaign-prompt.md)。

---

## 九步流水线

每步含 **目的 / MCP 调用 / 产物 / 失败分支**。任一步 FAIL 就地回退，不允许跳过继续。

### 区域 Profile 路由（2026-08-25 落地）

九步骨架全区域共用，**区域差异通过 profile 注入**：`references/regions/<REGION>.md` 每区一份，YAML front-matter 声明静态配置/数据集红黑榜/priors/闸门覆盖/循环策略，正文写明变体理由。

现有 **12 个** profile：`ASI` `CHN` `DEU` `EUR` `GBR` `GLB` `HKG` `IND` `KOR` `MEA` `TWN` `USA`。
**区域的权威清单是 `src/wqb/config.py::REGIONS`（14 个）**，profile / 战役目录 / 区域清单三者的对齐表见 [`INDEX.md §区域清单`](../INDEX.md)——任何区域的增删都要同步那张表。
未被 profile 覆盖的是 `AMR`、`JPN`（`config.REGIONS` 有该区，但**本工作区未启用**：无 profile、无战役目录）。

四个注入点：

| 注入点 | profile 字段 | 影响步骤 |
|---|---|---|
| 入口裁决 | `entry_verdict`（active / probe-only / frozen） | 步 1 |
| 生成先验 | DB KB 优先：region_kb win/dead + template_kb 骨架 组装 priors.json；profile 静态 priors 仅兜底 | 步 4 |
| 闸门特化 | `gate_overrides`（CW / longCount / prod_corr 阈值） | 步 5、步 7、步 8 |
| 循环策略 | `loop_policy`（探针上限、快判死、停止条件） | 步 2、步 6、循环表 |

规则：profile 与骨架正文冲突时**profile 优先**（它是区域实证结晶）；profile 缺字段回落骨架默认；profile 未覆盖的 region（**当前仅 `AMR` / `JPN`**）走通用处女地模板（参照 ASI profile），**且开新区前必须先补 profile + `tracking/<R>/config/`**（DEU 曾被这条漏掉，见 `references/regions/DEU.md` 开头注）；`frozen` 区域（当前仅 MEA）步 1 即拒，唯一后门见该区 profile。

### 步 1（S-PRE）查表

目的：region 先验，避免重复已判死路径。可选并行：`brain-next-move-analysis`（日报，不产出配置）、`brain-forum-browse`。

**先读区域 profile**：`Read references/regions/<REGION>.md`，按 front-matter 渲染本区专属 SOP（后续各步标注"profile"处按其覆盖执行）；`entry_verdict: frozen` 则按该区 profile 的入口裁决处理，不继续步 2。

**开工前置（每次新战役/新会话必做）**：
- **库存盘点（2026-09-08 新增，先于一切新挖）**：账户已有三万条以上已回测 IS alpha，
  其中约 11% 通过 IS 硬闸。**先清库存，再开新挖**——实证是数量级差异：
  2026-09-07 会话前半段跨四区 170 次新回测产出 0 条可提交 RA，后半段一次库存扫描产出 20 条。

  ```powershell
  # 1) 枚举 + 资格门复算 + 写回过闸率先验（供步 4 GEM 消费）
  python tools/build_gate_prior_from_inventory.py --regions all `
      --emit-candidates cache/candidates.json --write-priors
  # 2) 去参数网格 + OS 撞车预筛 + 篮内正交 + 平台复核
  python tools/select_ra_basket.py cache/candidates.json --target 20 --out cache/basket.json
  ```

  只有当候选池不足以覆盖目标金字塔时，才进入步 2 开新挖。
  两条硬约束：① `compute_mutual_correlation` 本地算 PnL、不占平台相关性配额，
  必须先用它去同族冗余与 OS 撞车，再进限流队列；
  ② 篮子敲定以 `GET /alphas/{id}` 的 detail 端点 `is.checks` 无 `result==FAIL` 为准，
  `submit_verdict` 在处女提交（404）时只返回 `UNVERIFIABLE`，不构成可提交依据。
- **PPA 主题匹配门禁**：调 `mcp__wq-brain-http__get_messages`（limit=30）扫描 `type=="ANNOUNCEMENT"` 标题含 "Power Pool" 的公告，解析当期主题的 region/delay/universe/中性化集合/禁止数据集/有效时间。PPA 提交必须**精确匹配**主题；不在当期主题的达标候选标 YELLOW + WAIT_THEME_ROTATION。RA 常规提交不受主题限制。

```
mcp__wqb-db__get_campaign_summary  region=$REGION
mcp__wqb-db__get_dead_ends         region=$REGION
mcp__wqb-db__get_dead_datasets     region=$REGION
# 实测产出率（2026-09-06 新增）：选区/选集的最硬先验，开波前必看
mcp__wqb-db__get_mining_yield                              # 全区排名
mcp__wqb-db__get_mining_yield  region=$REGION  by_dataset=true   # 本区按数据集拆
```

**产出率读法（两个比率含义不同，别混）**：
- `conversion` = 已回测 / 已生成 —— 低 = **流水线**问题（S2→S3 断链，生成远超回测吞吐）。修管道，别换区。
- `yield_rate` = 达标 / 已回测 —— 低 = **标的**问题（这个区/集本身不出货）。换区/换集，别加生成量。
- **2026-09-19 严格口径（默认 `strict=true`）**：达标 = sharpe/fitness 过线 **且 `ra_failed_checks` 为空**（robust/2Y/CW/换手全过）；
  另给 `prod_clean` / `prod_blocked` / `prod_wall_ratio`（已测 prod 的撞墙占比）。旧口径只看 sharpe/fitness 时 IND 显示 34% "产出率"
  而实际可提交 0（严格口径 12.6%，其中已测 prod 的 86% 撞墙）——选区先验被系统性高估。`yield_rate_loose` 保留旧口径对照。

2026-09-06 实测基线：IND 35.7% / MEA 19.9% / KOR 4.2% / EUR 2.0% / USA 1.4% / GBR 0%（180 条回测零达标）。
`yield_rate` 连续为 0 且样本 ≥100 的区，不要再投槽位；`conversion < 10%` 的区先清积压再开新波
（EUR 4.4%、USA 7.1% 都是积压堆库的典型）。

详细口径见 [wq-brain-campaign-matrix](../wq-brain-campaign-matrix/SKILL.md)。

* **产物**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号。

* **失败分支**：registry 全空 = 新区域，进步 2 并在步 9 写 campaign；`get_dead_datasets` 已覆盖全部候选则停止，转 `brain-next-move-analysis` 选新区域。

### 步 2（S0）数据集体检 + 金字塔配置

调 `mcp__wq-brain-http__workflow_campaign`（stage="S0"）。无战役目录的跨区试探才用本目录 `scripts/dataset_health_check.py`。
锁白名单后必须 `mcp__wqb-db__upsert_ledger_key(region, "s0_whitelist", {...})`。`recommend_datasets` 不能替代体检。

**⚠ 开区硬前置：体检包必须先落地（2026-09-17 P1-1，治「三连复发」）**：锁白名单后、进步 3 generate **之前**，
必须为白名单数据集补齐 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`。缺包时步 5 体检硬门
**不生效**——低覆盖/厚尾/稀疏事件的预处理约束会一路裸奔到仿真（历史三连复发的主因）。

```
# ① 先查已有包（实测 320 个：HKG 172 / USA 104 / EUR 19 / CHN 11 / GLB 6 / ASI 5 / JPN 2 / KOR 1；DEU·IND·GBR·MEA·TWN 为 0）
ls tracking/mining/field_inspect_*.json

# ② 缺包则生成（**纯离线**：只读本地 WebData ZIP，不发平台请求、不耗配额、无 429 风险）
python tools/gen_field_inspect_packs.py --all --dry-run                  # 先看 ZIP 里有哪些 region×delay
python tools/gen_field_inspect_packs.py --region <REGION> --delay <D>    # 再按区生成
```

**⚠ 数据源覆盖边界（2026-09-17 实测，勿误判为「忘了生成」）**：本地快照
`research-data/WebData_20260219_V0.10.9.zip`（160 条数据集、仅 ASI/CHN/EUR/GLB/JPN/KOR/USA 七区）
**早于本期战役选集** —— JPN 白名单 12 集中 **0 集**、DEU 白名单 9 集中 **0 集**落在该快照内
（DEU 在快照里连条目都没有）。这些区域的体检包**无法由本地数据生成**，需先更新 WebDataScope
导出包再跑 ②。在此之前可显式降级，但**必须在台账记因**，不得默认静默通过。

**步 5 缺包行为可切换（2026-09-17 P1-1）**：`tools/wave_gate.py --inspect-mode {off,warn,enforce}`
（或环境变量 `WQB_INSPECT_MODE`），workflow 节点 `wave_gate` 同名参数透传。
`warn` = 灰度默认（告警放行）；`enforce` = **fail-closed，缺包即整波拦截**。开新数据集/新区域建议 `enforce`。
实测对照（同一 KOR/model109，无包）：`warn` → EXIT 0 / PASS；`enforce` → EXIT 1 / FAIL。

**选集增强（2026-09-09 新增，`tools/campaign_intel.py s0-select`）**：S0 评分前先用它做三方交叉——
`recommend_datasets`（平台真实点塔状态，非本地推断）× `get_mining_yield`（本区历史产出率先验）
× `get_dead_datasets`（台账判死清单）。产出「未点亮塔 × 高产出 × 未判死」候选清单，
判死（ledger_dead 或 yield=0@足够样本）自动沉底。它把 S0 从「本地 alphaCount 推断饱和」
升级为「平台 pyramid 端点实测点亮」，直接服务主攻未点亮塔目标：

```
python tools/campaign_intel.py s0-select --region $REGION --delay $DELAY --universe $UNIVERSE --top-n 15 --target $TARGET_SEATS
```

输出 `hist_yield_rate`（历史产出率，None=处女地无历史）与 `hist_backtested`（样本量）；
`yield=0 且 bt≥8` 的集已被实证判死，不要再投槽位。
**2026-09-19 先验增强**：① `hist_yield_rate` 改用严格口径（RA-clean，与 `get_mining_yield(strict)` 同源）；
② 新列 `maxS`（本区该集历史 max|sharpe|）与 `fld`（字段数）；③ **跨区负先验** `[跨区弱:REG:maxS@bt]`——同集在其它区
≥16 条回测且 max|S|<1.0 视为弱（news/sentiment 在 USA/EUR/IND 同型全灭实证），`[跨区RA-clean:REG:n]` 为正证据；
④ `fields<5` 的集标 `仅条件腿`（只能做 trade_when/bucket 辅助腿或事件探针，不进主攻）。跨区弱 / 仅条件腿的集
排在健康集之后、判死之前。**背景**：此前只按未点亮塔分排序，IND 把 earnings3/insiders1/macro63/shortinterest5
这类结构性弱集推到前排，7 集 197 条回测 0 候选。
**回填**：`backtest_results.dataset` 曾恒 NULL（pipeline 未传 dataset，已修）→ 按集产出率把当天刚跑完的集显示为
"从未回测"；历史行用 `python tools/backfill_backtest_dataset.py`（只填空）回填后再看本榜。

**座位可达性（P1，2026-09-14 新增）**：`--target N`=本战役目标独立座位数（如 EUR 目标 20 颗过闸）。
每候选带 `est_seats`（同族高互相关只算 1 座位；读 `seat_model` 台账，无则默认 2）；存活 top-n 的
Σ`est_seats` < target 即 `[WARN] 结构性不可达` —— 此时应扩集/换区，而非在不足座位上反复打磨。

硬约束：

0. **已点亮塔不进白名单（2026-09-19 用户定案，硬规则）**：本区/本延迟下平台 `get_pyramid_alphas` 当季 ACTIVE ≥3 的 category（`recommend_datasets.category_lit=true`，如 IND 的 model/analyst/risk/other/fundamental）**不得作为战役主数据集**开 GEM/选波；其字段只能在未点亮塔主信号的表达式里作**辅助腿**（条件/group/bucket/中性化）。`campaign_intel s0-select` 输出的 `lit=Y` 候选直接剔除；剩余全是已点亮塔时换区，不挖。

1. 读 `registry_empirical` win 层：已验证配方的数据集族必须进候选。
2. `pyramid_quota_enable`：白名单至少 **2 个非 MODEL**（PV / NEWS / ANALYST / institutions）；不够则 tier2 上提，`tier_note=pyramid_quota`。
3. `category_weight` 只允许 0.9–1.15，禁止 1.3 vs 0.7 抹掉整座金字塔。
4. `*_dead` 仍排除；主导腿禁用 ≠ 整集判死。
5. 白名单外禁止 generate / simulate。
6. **饱和路由（2026-09-12 新增）**：目标 dataset 平台 `alphaCount ≥ 1 万`，或该数据集连续 2 波模板全灭（`gate_results.all_pass` 全 0）→ 强制切 `brain-alpha-research-hypothesis-first`（节点 `workflow_execute` node="hypothesis_round"，每假设派发主假设/消融/对照/变体 4 条），不再做模板遍历。
7. **体检包就位（2026-09-17 新增）**：白名单数据集须有 `field_inspect` 包（见上方开区硬前置）；缺包须先补，或显式 `--inspect-mode warn` 降级并在台账记因。

```
# ⚠ 本段是「2 步必需 + 1 步可选」，**不是三次重复**（2026-09-17 P2-7 澄清为何第三步不能删）：
#   必需 ① `calibrate=true`  → 反学 category 权重 + 拥挤甜区，写回 thresholds.json（cmd_calibrate）
#   必需 ② 裸 `stage="S0"`  → 按新阈值打分产出 s0_ranking（cmd_score）
#            ⚠ ① **不产出排名**，所以 ② 是必需步，不是冗余重跑（实测 cmd_calibrate 只写 thresholds.json）
#   可选 ①′ `calibrate=true dry_run=true` → 只预览不写盘，仅**新区/校准结果可疑**时才需要审
# 审两处异常：甜区 ac 异常巨大（如 MEA 8560-21508 反向奖励超拥挤）/ strong_acs 空（无强信号）
# 详见 wq-brain-campaign-toolkit/references/probe-scoring-v2.md「评分前必做：calibrate 自学习校准」
# ①′ 先审（可选；确认无需人工介入则跳过）：
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S0"  calibrate=true  dry_run=true
# ① 校准（写盘）+ ② 打分（产出排名）—— 两步都要：
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S0"  calibrate=true
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S0"
mcp__wqb-db__get_ledger_key  region=$REGION  key=s0_ranking
```

**评分机制增强（2026-09-14，score_datasets.py；默认 OFF/中性，需区域 `thresholds.json` 显式 opt-in，机制细节见 wq-brain-campaign-toolkit SKILL.md §6.x）**：

- **P0 经验强度先验**：`empirical_weight>0` 时 `score()` 叠加 `empirical_prior`（数据源=calibrate 写入的 `dataset_empirical_prior` 台账，`ceiling_ratio`=实测 best_sharpe/gate_sharpe），把目标从「数据干净+低拥挤」拉向「能过闸概率」。
- **P2 饱和再验证降级**：score 读 `saturated_datasets` 台账，命中集自动降 `excluded` 且不被保底带复活 —— prod 饱和归零的集不再靠 coverage 分赖在白名单。
- **P3 universe 一致性守卫**：台账 `s0_ranking`/`s0_whitelist` 的 universe ≠ `settings.universe` 即 `[WARN]`（coverage/alphaCount 跨 universe 不可比，分位线与硬闸判据错位）；本次 score 以新 universe 重生成覆盖，白名单须据新 universe 复核重建。
- **P5 饱和拍平 model + 榜分离**：`_region_saturated` 时 model 类 `category_weight` 封顶 1.0；`score`=信号强度榜（哪个集出好 alpha），`pyramid_view`=点塔战略榜（哪个集点亮金字塔），语义分离勿混排。
- **P6 calibrate token 去重**：`_expr_fields` 去重 + 剔除 group 变量关键字（subindustry/industry/sector…），根治甜区污染。

* **失败分支**：配额后仍无非 MODEL 则写 findings，不要退回纯 MODEL 七槽；全部硬排除 则回步 1 换 region。

### 步 3（S1）字段扫描 + 理解

必做 typed catalog。**深度字段理解用 `mcp__wq-brain-http__workflow_feature_engineering`（⚠ 2026-09-17 P3-11 收口：按需 / 仅人读参考 / 禁注入 GEM）**——独立调用，ideas 回写 `s1_<ds>_d<delay>`，`source=standalone`。深查可前置 dataset/datafield exploration。

> ⚠ **为何是"按需 + 禁注入"（2026-09-15 ② 实证，GBR intraday_pv_feats）**：该节点产出的是**确定性模板渲染**
> （8 问框架 + `rank(ts_mean({f},66))`），**不含 LLM 推理**。把它当 ideas 喂给 GEM，会让 GEM
> **一行 LLM 都不调**、整波退化为模板展开——正是"每个字段套一个 rank"的同质化堆。
> 因此：① 它**不是必做项**（节点与 runner 已主动跳过 `source ∈ {feature_engineering_node, standalone*}` 的模板文档）；
> ② 产物**仅供人读参考**；③ **禁止注入 GEM**（如需覆盖须显式传 `ideas_file`）。
> 生成侧的唯一权威是步 4 的**概念优先 GEM + priors 注入**。

```
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S1"  dataset=$DS
```

- **产物**：`fields` 表 + ledger S1 决策。
- **字段分级风险筛查（prod-corr 规避，orchestrator 迁移）**：`mcp__wq-brain-http__get_datafields` 后按 `users` 分级——`users ≥ 50` 只做信号方向验证不投入候选打磨（prod_corr 必超）；`users 10-49` 进候选池、提交前必须实测 prod_corr；`users 0-9` 优先候选池（理论 prod_corr≈0）。冷门字段（users≤9）占批次预算 ≥50%；已确认超标的字段族（如 GLB techindi `predicted_first_quantile_ten_day_return_*`）不再投任何变体。完整规避画像见 [references/prod-corr-avoidance.md](references/prod-corr-avoidance.md)。
- **失败分支**：字段数 <10 则退回步 2 白名单外。VECTOR 比例用 `get_datafields` 确认，步 4 必须传对 `data_type`。

### 步 4（S2）选波：概念优先生成

**生成器 = `mcp__wq-brain-http__workflow_gem`，强制调用**
`build-wave` 只去重 / 分桶 / 骨架配给，不产表达式。增强需求走 GEM 生成策略（增强 = 对已有 idea 的变体扩展，经 priors/ideas 注入实现）。

**可选** `mcp__wq-brain-http__workflow_campaign`（subcommand="diversity-extract"）做方向参考，**不替代** GEM，不强制先行。

硬约束：

1. 先读 win 层（= `region_kb.win_recipes`，与 priors.json 同源）。有胜绩则本波至少 2 槽按**机制**换腿。EUR 已验证：`0.4 × 慢 MODEL 残差 + 0.6 × 快 PV`，中性化/decay 跟 win。
2. GEM 概念优先：机制 → 1-2 个具体字段 id → 一个 Implementation Example。禁止「每个字段套 rank」。必须带 `priors_file`。
3. 有信号：`|Sharpe|≥1.0` / `PASS_CHEAP` / registry 标明有 IS 但卡 prod。复合后 `|S|<0.5` 不再入选波池。
4. 七槽（Token-Bucket C≈7，2026-08-25 起）：≥2 跨金字塔；≥1 win 换腿；弱探针最多 1 槽且仅当本波尚无近闸字段。
5. 若 2 跨集：能合并 catalog 就合并；否则拆成慢腿批 + 快腿批同波对照，不要停挖。
6. **时间窗口意义**（解释）：只用 1/5/22/66/252/504/1008/1260 标准窗口；其他窗口必须给出明确解释或实际测试证据。
7. **禁止 add(A,B) 混信号**（CLAUDE.md）：防过拟合，警惕 `add(A,B)` 模式；优先单数据集 atom alpha，双数据集不要总是同一金字塔组合（均匀点塔）。
8. **字段角色区分**（CLAUDE.md）：区分主信号 vs 辅助信号 vs group/bucket 字段；辅助信号可考虑 bucket 自定义分组；group 类型字段可用 `group_*` 操作符。
9. **金字塔点亮**（CLAUDE.md）：一个金字塔需 3 颗 alpha 点亮，尽可能多点塔且均匀分布。

**priors.json 组装：首选 `mcp__wq-brain-http__workflow_campaign`（subcommand="assemble-priors"），以下协议仅作其内部映射说明，勿手写组装**。GEM 管道只消费 `wins`（≤6）与 `dead_ends`（≤12）两个键（`economic_priors.py`），其余键会被忽略：

```
# assemble-priors 从 DB KB（region_kb win/dead + template_kb + profile 静态先验）确定性组装
# 并落 <campaign>/priors/<region>_priors.json（含 sha256），取代手写 get_ledger_key 三读
# 阶段标 S2（priors 是 S2 上游产物，Artifact 契约表亦记在 S2）；路由实际按 subcommand
# 走 campaign.py，与 stage 无关——不要把这里的 stage 当成"属于 S6"。
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  subcommand="assemble-priors"
```

assemble-priors 内部映射（供核对，勿手写）：

1. `wins`（按序，合计≤6 条）：① `get_ledger_key("GLOBAL", "region_kb")` → `templates[]` 通用模板 → `{"id": <name>, "key": "skeleton=<skeleton>; evidence=<evidence>; source_region=<source_region>"}`；② `get_ledger_key($REGION, "region_kb")` → `win_recipes[]` → `{"id": <name>, "key": "skeleton=<skeleton>; evidence=<evidence>; settings=<settings>"}`；③ `get_ledger_key("KB", "template_kb")` → `validated` 含本区的模板 → `{"id": "<id> <name>", "key": "skeleton=<skeleton>; iron_law=<iron_law>"}`。
2. `dead_ends`（按序，合计≤12 条）：① region_kb → `dead_patterns[]`（字符串直传）；② template_kb → `failed` 含本区的模板 → `{"family": "<id> <name>", "reason": "<failed 原因>"}`；③ profile `priors.signal_families_exclude` 并入。
3. region_kb 未命中/为空 → 兜底用本区 profile front-matter 静态 priors（`win_recipes` + `signal_families_exclude`）。
4. `GLOBAL/region_kb` 的 `methodology[]` 与 `signal_family_rules[]` 作为 `region_context` 注入 GEM prompt（见 `economic_priors.py` 的 `compact_priors_text()` 输出）。
5. `KB/community_tpl_kb` **不进 priors**（候选未实证，注入稀释 concept-first）。它服务两个场景：步 5 多样性 FAIL 回本步补骨架时按 `category` 检索换腿参考（占位符按 `placeholder_conventions` 替换）；Mode B Step B1 找骨架。**取骨架前必查键内 `ghost_operator_advisory`**：含幽灵/未验证算子（如 sigmoid/ts_entropy/ts_skewness/ts_percentage/ts_decay_exp_window 等）的骨架必须替换已验证等价算子（映射表见键内与人读手册 `docs/reference/community_tpl_library_sequel.md` §十八）或先 `mcp__wq-brain-http__preflight_expressions` 实测，否则整批 ERROR/CANCELLED。

生命周期闭环：本协议使 DB KB 成为 S2 先验唯一上游——S6 回写 region_kb / template_kb 后，下一次 S2 先验自动变新；profile 静态 priors 仅作 DB 空时的种子，不再手工更新。**2026-09-15 起 region_kb 由 pipeline 波后自动刷新**（`recent_waves` / `gate_priors_local` / `updated_at`，见步 9），不再依赖人工回写才更新。

**gate_priors 分流（2026-09-15 ①）**：`region_kb.gate_priors`（库存实测过闸率）按维度分两路消费——
`by_operator_count` / `by_field_family` 进 GEM prompt（表达式层能作用）；`by_decay` / `by_neutralization` 是仿真设置，
**不进 prompt**，由步 6 `pipeline.py run` 的 settings prior 直接改写本波设置（`_lib/region_kb.py`）。
assemble-priors 快照里的 `settings_prior` 键只是只读展示。此前两者全塞 prompt → LLM 改不了 decay，S3 永远用
settings.json 固定值（GBR decay=14 28.3% n=46 vs decay=4 3.9% n=408 而三波仍跑 decay4 → 0/44）。

```
$DELAY    = (settings.json).delay
$UNIVERSE = (settings.json).universe
$DTYPE    = (catalog).data_type
# 确定性组装 priors 并写 DB 快照（priors_snapshot_<region>）——DB 为单一事实源
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  subcommand="assemble-priors"
mcp__wqb-db__get_ledger_key  region=$REGION  key="s1_${DS}_d${DELAY}"
# GEM 生成。pipeline_mode: phased（缺省）/ skeleton（代码组装、语法构造保证）/ single（一次性 LLM，不推荐）
mcp__wq-brain-http__workflow_gem  region=$REGION  dataset_id=$DS  delay=$DELAY  universe=$UNIVERSE  data_type=$DTYPE  pipeline_mode="phased"
# 注：priors_file 已可省略——GEM 经 load_priors(region) 从 DB 快照直读，文件仅降级兜底
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  dataset=$DS  wave=$W
```

**ideas 注入规则（2026-09-15 ②）**：S1 ledger 的 `ideas_md_path` 只有在 `source` 为 LLM/人工产出（`s2_nested`、手写）时才自动注入 GEM；
`source ∈ {feature_engineering_node, standalone, standalone_v2}` 的文档是 `feature_engineering.py` 的**确定性模板渲染**
（8 问框架 + `rank(ts_mean({f},66))` 式模板），注入后 GEM 一行 LLM 都不调、整波退化为模板展开（GBR intraday_pv_feats 实证）——
现节点与 runner 都跳过这类文档、改走概念优先自含生成；显式 `ideas_file` 仍可覆盖。
**生成侧预闸（2026-09-19 扩展）**：除下述 quantile 归一化与毒模式丢弃外，`pipeline_pregate` 现还做：`hump(x, k)` → `hump(x, hump=k)`
（平台只认命名参数）；`bucket(rank(x))` 缺 range → 补 `range="0,1,0.1"`，非 rank 输入丢弃；区域非法 group 字段丢弃
（`platform_constraints.json` `region_invalid_group_fields`，JPN=sector/subindustry/industry）；非标窗口按别名表归一
（20/21→22、60/63/65→66、250/255→252、500→504、1000→1008、1250→1260，其余非标窗只 WARN）；**同骨架换字段变体封顶**
（`WQB_GEM_MAX_PER_SKELETON`，缺省 12/骨架——JPN analyst_revision_horizons 1026 字段渲染出 7538 条几乎全是同骨架换字段）。
**原有**：GEM 落盘前自动做 `quantile(x, driver="gaussian"[, sigma=1.0])` → `quantile(x)` 无损归一化（平台默认 driver，语义不变；
闸 4 ARITY 312 次命中的根因）并丢弃加权混合毒模式（闸 5 同源正则），步 5 门禁只作兜底。

消费 `methodology_rules`（build-wave 配给，不替代 GEM）。该 `$DS` 本区域从未跑过 GEM 则必须先跑 GEM。
未验证 DB 有表达式，不得声称步 4 成功。

* **失败分支**：GEM 未入库则按超时恢复清单查任务，确认失败才回退，不要手写；候选不足则 enhance / 扩组合，仍不足换数据集。

### 步 5（S2→S3）门禁

禁止新建 `_gate_waveNN.py`。禁止写 `cache/gate_wave*.json`。

**生成→回测双硬门（orchestrator 迁移，回测前必过）**：
1. **多样性守卫（唯一执行口径 = toolkit `gate.py:check_batch_diversity`，即闸6）**：由 `wave_gate.py` 在提交前自动调用。判据三源：①**自学习契约** `explore_contract`（`rules.get_active_contract`；`repair` 类默认豁免；契约过期 **FAIL-CLOSED** 并自动续约）；②**收益来源多样性**（读 DB idea ledger 的 `expected_exposure`：同批 >60% 表达式共享同一 exposure 且字段族相同 → FAIL；无 exposure 元信息 → WARN 不阻断）；③**家族天花板预检**（主导腿信号族占比 ≥2/3 → WARN 不阻断，wave94/95/98/104 实证 SELF≥0.9 必死）。
   - ⚠ **不要再把 `wqb.expression.validator.check_batch` 当判据**（2026-09-17 P2-10 三口径收敛）：实测它只实现 **4** 条形状闸（`shape_signatures` / `outer_wrappers` / `group_vars` / `windows`，各 ≥2），**全仓零调用方**，且与上述执行口径判据不同。历史正文并列两套口径 + 一条"两者判据不同"的注，易被误读成"调了前者就过了闸"。它现在只作**方法论参考**（形状维度自检），不构成门禁。
2. **体检→表达式硬门（2026-09-06 已接线，不必手工调）**：`tools/wave_gate.py` 内置调用 `tools/field_inspect_gate.py`，逐条比对字段体检结果，违规计入 FAIL 硬阻断。5 条硬门：低覆盖(cr<0.4)必须含 `ts_backfill`；高偏度(|skew|>2)必须含 `rank`/`winsorize`/`signed_power`；厚尾(kurt>8)必须含 `rank`/`winsorize`；单边恒正/负不能直接用原始水平；稀疏事件(zero_inflated/point_mass)必须用 `trade_when`。
   - 体检包路径 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`，由 `python tools/webdata_quality.py --zip <WebDataScope数据包> --export-expr <path>` 生成。
   - **缺体检包时本闸不生效**，wave_gate 会打印 `[inspect] 体检硬门未生效` 并给出生成命令 —— 看到这行就说明这一波的预处理约束没人把关（低覆盖/厚尾/稀疏事件会一路裸奔到仿真）。**现状（2026-09-11 实测）：`tracking/mining/` 有 320 个体检包、318 个 `fields` 非空**（HKG 172 / USA 104 / EUR 19 / CHN 11 / GLB 6 / ASI 5 / JPN 2 / KOR 1；DEU / IND / GBR / MEA / TWN 为 0），可用 `ls tracking/mining/field_inspect_*.json` 先查；缺哪个区域/数据集就现生成。注意历史版本曾误记"全仓库暂无可用体检包"——那是只看了 git 跟踪视角（当时仅 2 个空包入库），磁盘实况以 ls 为准。
   - 单独自查：`python tools/field_inspect_gate.py --region USA --dataset model267 --exprs-file <txt>`。
3. 流程：`check_batch（gate.py 闸6 批级多样性）→ wave_gate（闸1–5 + 闸7/8 数据质量 + 体检硬门）→ 步 6 create_multi_simulation`（闸编号唯一基准见 `Claude/skills/INDEX.md §gate.py 闸编号`）。
   - **脚本归属（2026-09-07 校正）**：`wave_gate.py` / `preflight_wave.py` / `field_inspect_gate.py` 在**仓库根 `tools/`**；`gate.py` / `pipeline.py` / `build_wave.py` / `score_datasets.py` / `assemble_priors.py` 在 **toolkit `scripts/`**（`Claude/skills/wq-brain-campaign-toolkit/scripts/`）。调用时别找错目录。`--wave` 参数全链路为**字符串**（支持 `97` 与 `s2_xxx_d1` 两种形态；wave_gate 曾因 `type=int` 导致字符串波号无法进门禁，2026-09-07 已修复）。
   - ~~注：第 1 点的 `wqb.expression.validator.check_batch` 是**方法论口径**；可执行路径上实跑的是 toolkit `gate.py:check_batch_diversity`（契约式自学习闸 + 收益来源多样性 + 家族天花板）。两者判据不同，不要以为调了前者就过了闸。~~
     ↳ **2026-09-17 P2-10 已收敛**：该双口径注已并入第 1 点正文，此处不再保留两份判据（详见第 1 点）。

**本步既有 MCP 节点也有 CLI**（2026-09-11 起）：`workflow_execute(node="wave_gate", params={region,dataset,wave,...})`
（遵守 dry-run 契约 + argv 契约校验）；等价 CLI 走仓根 `tools/`。两者同一实现，节点只是把 CLI 包成可入链的一步。
注意 `workflow_campaign(stage="S2")` 只路由到 `build_wave.py`＝**选波**（步 4 已调），**不要拿它代替本步门禁**。

```powershell
# ① 幽灵算子硬闸（纯本地、零配额，先拦——含幽灵算子会整批 CANCELLED 连坐）
python tools/campaign_intel.py ghost-audit --region $REGION --exprs-file <候选表达式.txt>
# ② 每波门禁（语法 + gate.py 5 闸 + 体检硬门 + 多样性），一键落盘 gate_results
python tools/wave_gate.py --campaign-dir tracking/$REGION --dataset $DS --wave $W --from-db
#    候选不在库时： --exprs-file <候选表达式.txt> ；单条自查： --expr <表达式>
# ③ 仅当需要重建波次时才回选波（等价 workflow_campaign stage="S2" → build_wave.py）
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  dataset=$DS  wave=$W
```

VECTOR 用 `mcp__wq-brain-http__preflight_expressions`（auto_fix_vector=true）；repair 批给 `wave_gate.py` 加 `--skip-diversity-gate`。

**闸 2b 区域非法 group 字段（2026-09-19）**：`gate.py check_one` 按 `platform_constraints.json` `region_invalid_group_fields[region]`
判 FAIL（JPN 的 sector/subindustry/industry：POST 可接受、执行必 `Invalid data field` 并连坐整批）。本地语法闸同时新增
`bucket()` 必带 `range=`/`buckets=`（validator 规则；此前只拦 hump 不拦 bucket，JPN w7 因此丢一批）。

**幽灵算子硬闸（2026-09-09 新增，`tools/campaign_intel.py ghost-audit`）**：GEM 产物入库后、
wave_gate 前跑它——检测表达式是否含平台不认的幽灵算子（sigmoid/ts_entropy/ts_skewness 等）。
幽灵算子会触发整批 CANCELLED 连坐（批内一条坏式 ERROR 取消全部兄弟任务），必须在 dispatch 前拦下：

```
python tools/campaign_intel.py ghost-audit --region $REGION --exprs-file <候选表达式.txt>
```

退出码 1 = 有幽灵算子（违规式隔离到独立小批或换已验证等价算子，映射表见 `KB/community_tpl_kb` 的
`ghost_operator_advisory`）。纯本地检测，零配额。

- **失败分支**：语法 FAIL 必须先修；多样性 FAIL 则回步 4 补骨架（可查 `KB/community_tpl_kb` 按 category 检索候选骨架，占位符按 `placeholder_conventions` 替换，并先查 `ghost_operator_advisory` 做幽灵算子替换）；若 2 跨集 FAIL 则拆回单集组合，不停挖。

### 步 5b：新信号族的 prod-first 探针（2026-09-19 实证后升为硬门）

**任何新信号族在投入第二波之前，必须先用 1–2 条骨架查 `check_correlation(production)`**（`tools/campaign_intel.py prod-first --region R --wave W --top-k 2 --write-ledger --json <out.json>`，`--json` 需要文件路径）。
实证：IND intraday_pv_feats 价量相关反转连投 3 波 24 条（S 4.4–6.5 全 IS 过）后才查 prod = 0.79–0.92，整族报废；pv103 尾盘反转 8 条同理。
判定：家族首探 prod ≥ 0.7 → 记 dead_end 换机制，不做任何去相关变体（bucket/门控/平滑实证都破不了 prod 墙）；0.60–0.70 → 直接进步 8。

### 步 6（S3）七槽回测

并发唯一来源 [wqb-concurrency](../wqb-concurrency/SKILL.md) §8。
S3 入口也可走 [brain-sim-alphas-in-batch-and-track](../brain-sim-alphas-in-batch-and-track/SKILL.md) 或 toolkit，填槽内容仍以本步为准。
设置展开需要时用 [brain-inspect-raw-template-create-setting](../brain-inspect-raw-template-create-setting/SKILL.md)（`--from-db`），不是第三条生成器。

1. 空槽补组合批，不用裸探针凑数。
2. 弱探针最多 1 槽；已有近闸字段时为 0。
3. 设置跟 win：EUR 实证 `SUBINDUSTRY` + `decay4`。可另探 `ILLIQUID_MINVOL1M` / `TOPCS1600` / `delay0`。
   **设置层先验（2026-09-15 ①，默认开）**：`pipeline.py run` 装载 settings 后读 `region_kb.gate_priors`
   （缺则 `gate_priors_local`），`by_decay` / `by_neutralization` 里样本 ≥30 且过闸率 ≥ 当前设置 ×2 的格子
   自动改写本波设置并打印 `[settings-prior] decay 4→14：当前 3.9%(n=408) vs 实测 28.3%(n=46) lift×7.2`；
   显式 `--set decay=…` / `--neutralization` 钉住的维度不动；`--no-settings-prior` 或区域 `thresholds.json`
   `settings_prior.enabled=false` 关闭。win 设置想优先就显式 `--set` 钉住。
4. prod-first：每槽先 1-2 条骨架查 `prod_corr`；≥0.7 停扩换腿。
5. 表达式从 `mcp__wqb-db__list_expressions` 取。`mcp__wq-brain-http__submit_verdict` 判定 SUBMITTABLE 见步 8，禁止自动提交 alpha。
6. **S2-COMPLIANCE 已降级为提示（2026-09-15 ⑥）**：`s2_compliance_w<wave>` 缺失不再中止、不再需要 `--force`；
   闸 2/3 的真正保障是 typed catalog（缺目录 stage_gate 直接 FAIL）。`pipeline.py` 所有中止路径现返回 rc=2
   （此前恒 0，detached 启动器把"中止"当"成功"）。

```
# 七槽填槽由 pipeline.py 内部锁定 n_slots=min(7, 批数)，不从外部传
# （2026-09-06：曾往命令里拼 --concurrency 7，而 pipeline.py 根本没这个参数，
#  argparse exit=2 + detached 不看退出码 = S3 每次"启动成功"却从未真跑过。
#  concurrency 形参现仅作计划元数据，传非 7 会收到 warning。）
mcp__wq-brain-http__workflow_batch_track  region=$REGION  wave=$W  dataset=$DS

# 后台任务状态（batch_track 异步返回 task_id 后用它跟踪，不要 shell 翻日志）
mcp__wq-brain-http__workflow_task_status  task_id="<上一步返回的 task_id>"
mcp__wq-brain-http__workflow_task_status  prefix="batch_track"      # 列最近任务

# 批次状态查询（单次，非轮询）
mcp__wq-brain-http__batch_status  simulation_ids=["<id1>", "<id2>"]

# 收批压缩（2026-09-09 新增）：一键收 multisim 全部 alpha 详情（并行拉取），
# 替代「get_multisimulation_children + lookINTO×N + get_alpha_details×N」的 18 次调用链，
# 压成 2 次（本工具 + wqb-db harvest_multisim_results 入库）。手动补收/审计某批时用：
mcp__wq-brain-http__harvest_multisim_alphas  multisimulation_location="/simulations/<id>"
mcp__wqb-db__harvest_multisim_results  region=$REGION  wave=$W  alphas=<上一步返回的 alphas 列表>
```

* **失败分支**：整批 CANCELLED 则回步 5；429 则降并发、批大小 ≤5。

**批次级故障处理协议（orchestrator 迁移）**：

| 故障现象 | 处理 | 依据 |
|---|---|---|
| 8 子模拟全 ERROR | **重发相同表达式** | USA/D0 3次确认 |
| CROWDING 连续 2 次全 ERROR | **跳过**该中性化 | 重发仍失败 |
| fatal operator 级联 CANCEL 整批 | **隔离不确定算子到独立小批次** | ts_entropy: 20条全CANCEL |
| 瞬态 "try again" 整批命中 | **拆成 5 条/批**重试 | e10a/e10b |
| 429 THROTTLED | 指数退避 | 账户级限速 |
| MCP 超时无 result | 查 MCP 服务进程(PID)，到 WQ BRAIN 控制台查看 | b87/b92/b93 |
| "took too much resource" | **真问题**——去 backfill 或缩短窗口 | model26 364字段 |

`create_multi_simulation` 要求 ≥2 条表达式；先归因再决定重发/跳过/拆批。

- **连坐隔离已自动化（2026-09-19，`pipeline.py` 默认开，`--no-isolate-errors` 关）**：某批 ERROR 时解析子模拟
  `status/message/regular`，定位真正报错的坏式 → 回写 `expressions.status='fail'`（reason=平台错误正文）→ 其余无辜
  表达式作为"重发批"**优先于** pending 队列在下一个空槽重发一次（重发批再 ERROR 不再重发）。JPN w7/w8 实证：
  一条 `bucket()` 缺 range / 一个平台不认的字段，整批 8 条连坐，10 批丢 8 批 64 条。上表"隔离不确定算子到独立小批次"
  仍适用于**提交前**的预防；提交后的连坐由 pipeline 自动处理。
- **账户级槽位仲裁（2026-09-19，`_lib/slots.py`）**：多条 pipeline 同跑时用 `logs/_slots/` 的 token 文件跨进程计数，
  在飞 ≥ `WQB_GLOBAL_SLOTS`（缺省 7）即等待；terminal 释放，进程死亡/超龄 token 自动回收。`WQB_GLOBAL_SLOTS=0` 关闭。
  排障：`python Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/slots.py` 打印当前占坑。

- **积压清理（每波结束时）**：只读 SQL 查积压 `SELECT region, status, COUNT(*) FROM expressions WHERE region=? GROUP BY status`——若 `pending`+`gated` > 本波表达式数 2 倍，说明 S2→S3 断链，本波结束优先把近闸积压纳入下一波（`build_wave --from-db` 重取），禁止无脑新建表达式堆库。

### 步 7（S4）诊断改进

```
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S4"  dataset=$DS  wave=$W
```

节点会先从 `backtest_results` 解析本波 alpha_id（精确 wave → `s2_<dataset>_d*` 标签）再拼
`review_wave.py --alphas … --tag <wave> --write-ledger`；解析不到即 FAIL（干跑也 FAIL）并列出该区最近波次。
（2026-09-15 ④ 修复：此前只传 `--tag`，实跑必 `need --multisim or --alphas` rc=2 而干跑报 success。）
评审里 `risk_neutralized_sharpe ≤ rn_sharpe_min`（默认 0）现直接判 `RN_EXPOSURE` 墙、不进候选（`walls()`/`passes()` 已接线，
阈值在 `thresholds.review.rn_sharpe_min`）。

阈值不达标见 [brain-how-to-pass-alpha-test](../brain-how-to-pass-alpha-test/SKILL.md)。
用 [wq-brain-alpha-optimization-v1](../wq-brain-alpha-optimization-v1/SKILL.md)（Mode B 70% / Mode A 30%）。
按需：`brain-calculate-alpha-selfcorr-quick`（本地快筛）/ `brain-explain-alphas`（按需归因：Mode B 换概念前查概念重叠，非每候选必经）。
`brain-alpha-repair` 只作配方查表。

**prod-first 探针（2026-09-19 新增，`tools/campaign_intel.py prod-first`，S3 收批后**必调**）**：全区绑定约束是
PROD_CORRELATION（2026-09-18 库存 22/22 撞墙 0.80-0.99；IND 已测 104 条 73% 撞墙），而 prod 检查此前排在链尾。
本命令对本波每个信号族（字段集合）最强 1 条**串行**跑平台 prod（单并发排队），族级给 EXPAND / STOP：
`STOP(prod≥0.7)` 的族**不再扩变体**（决策表 D0：撞 prod 墙 → 换白名单不同数据集，勿磨同腿），
结果写 `alphas.prod_correlation`（已有行）+ ledger `prod_first_<wave>`：

```
python tools/campaign_intel.py prod-first --region $REGION --wave $W --top-k 3 --write-ledger
```

实证：IND w172 sentiment21 三族 prod 0.16-0.50（干净，墙在 robust 0.24/limit 1.0 而非 prod）——
prod-first 与下文 robust 判定合起来，才能在扩批前分清"prod 墙"与"结构墙"。

**near 池不再收结构性死信号（2026-09-19）**：`review_wave.is_near` / pipeline 评审同口径——sharpe 过 near 线但
`robust_universe_sharpe / limit < near.robust_min_ratio`（缺省 0.5，`thresholds.json` 可调）的行打 `ROBUST_STRUCTURAL`
墙、不入 near。此前 IND w172 四条 raw 1.76 / robust 0.24 的行按 sharpe 入 near → 全灭波记 PARTIAL → 停止规则 B
（连续 3 波 FAIL）永不触发；metrics 行现带 `robust_sharpe/robust_limit/sub_universe_sharpe`。

**S4 预筛压缩（2026-09-09 新增，`tools/campaign_intel.py s4-prescreen`）**：S3 收批后、进 S4 评审链前，
先批量拉指标分层 READY/REVIEW/REJECT——REJECT（全灭）直接判死不进 S4 链，只对 READY/REVIEW 走完整
selfcorrQuick→check_self_correlation→compute_mutual_correlation→check_correlation→robustness→judge 链。
评审效率提升约 8 倍（8 条候选从 8 次逐条评审压到 1 次预筛 + 仅存活者进链）：

```
python tools/campaign_intel.py s4-prescreen --ids-file <本波 alpha_id 清单.txt>
```

**卡闸辅助腿检索（Mode B 组合增强）**：主信号卡某闸时，从 salvage 池找跨数据集正交辅助腿，
替代人工翻历史波次：

```
mcp__wqb-db__get_salvage_pool  region=$REGION  boost_dim=<boost_2y|boost_cw|boost_tvr|boost_sharpe>  exclude_dataset=<主信号数据集>  min_sharpe=1.0
```

卡 2Y 闸用 `boost_2y`、卡 CW/子宇宙用 `boost_cw`、卡 tvr 用 `boost_tvr`、信号弱用 `boost_sharpe`。

**组合形态合规（路线 A，2026-09-13 定案）**：取到辅助腿后**禁止任何加权混合**
（`0.5*rank(A)+0.5*rank(B)`、`add(multiply(0.5,rank(A)),multiply(0.5,rank(B)))` 均被 gate 闸5 block）——
仅允许结构交互（ts_corr / ratio / 价差 / 条件 / 分组）或 SuperAlpha combo；
构造细则见 [wq-brain-alpha-optimization-v1](../wq-brain-alpha-optimization-v1/SKILL.md)「组合腿救援」构造纪律。

- **风险中性化硬规则（2026-09-08 新增；2026-09-15 ⑦ 已接线进 `review_wave.walls()/passes()`，墙名 `RN_EXPOSURE`）**：收割后必看 `risk_neutralized_sharpe`。
  `risk_neutralized_sharpe <= 0` 且 `sharpe >= 1.58` ⇒ 该 alpha **就是它自己声称的那个因子暴露**，
  不是暴露之上的超额——直接记 `dead_end`，**禁止继续调参**（调参只会让暴露更纯）。
  实证：HKG w4 七条里六条 `risk_neutralized_sharpe` 在 −0.33 ~ −0.57，raw sharpe 却非零；
  而 w3 的 `O0roWEM7`（risk_neutralized 0.96 ≈ raw 1.17）是约 150 次回测中唯一的真信号特征。
  该值已入 `backtest_results.risk_neutralized_sharpe`，步 9 需与 GEM 声明的 `Expected Exposure`
  比对后回写 `template_kb`（兑现进 `validated`，未兑现进 `failed`）。
- **失败分支**：`prod_corr ≥0.7` 则 Mode B 换概念；同一想法 >10 种结构仍不过 则步 9 记 `dead_end`，回步 2。
- **prod 验证排队调度**：多候选时走串行泳道（本地检查全批先跑、prod 队列恒保持 1 在飞、等待期插本地活），细则见 [references/prod-corr-avoidance.md](references/prod-corr-avoidance.md) §7（含 7 天结果缓存与 `refresh` 终验）。

### 步 8（S4→S5）稳健闸与提交判定

> **prod 0.60–0.70 的候选当天提交，不先做变体（2026-09-19 血的教训）**：IND pv103 尾盘反转 mLm2xG1K（S 3.83，IS 全过，prod 0.6997）
> 因为先花 1 小时做去相关变体，期间外部用户提交了同款，复查 prod = 1.0000，整族封死。规则：`submit_verdict` READY 且 prod < 0.7 → 立即请用户确认提交；
> 同族第二颗的变体探索放在第一颗 ACTIVE 之后。



S4→S5 必经 [brain-alpha-robustness](../brain-alpha-robustness/SKILL.md)（反过拟合/稳健性闸）。

**提交判定链（顺序执行；最终提交判定唯一权威 = 第 2 步 submit_verdict）**：

1. **Failed-count 资格门（研究侧硬前置）**：进入提交流程前，从 `is.checks` 计算 WebDataScope failed counts（规则见 [references/webdatascope-failed-gates.md](references/webdatascope-failed-gates.md)）。REGULAR 要求 `Failed RA == 0`；PPA 要求 `Failed PPA == 0`。比只看 `result=="FAIL"` 严格（WARNING/ERROR 也计数）。枚举每个 counted item 的 name/limit/value；非零 → 回步 7 修复，不进入提交。

```
mcp__wq-brain-http__submit_verdict  alpha_id=<ALPHA_ID>
```

2. **submit_verdict 零成本判定（提交层权威）**：`mcp__wq-brain-http__submit_verdict` 给出模拟层 checks + GET `/alphas/{id}/submit` 双视图（403 盲区唯一权威），确认无 FAIL 且提交层 200。**是否提交的最终判定以本步为准。**

**submit_verdict 判定 SUBMITTABLE 只报告、等用户确认**。确认前禁止 `mcp__wq-brain-http__workflow_submit_alpha` / `mcp__wq-brain-http__submit_batch`。
pipeline `--submit` = 提交回测，不是提交 alpha。

* **失败分支**：`PASS_CHEAP` 则可提交；PROD/SELF 不过 则回步 7；配额耗尽按 ET 日历日（00:00 ET 重置）等待。

### 步 9（S6）复盘回写

未回写视为本波未完成。细节见 [wq-backtest-monitor](../wq-backtest-monitor/SKILL.md) §14。

**开步先看漏斗（2026-09-17 新增，`tools/step_funnel.py`）**：回写结论前先跑一次步级漏斗，
用数据定位"这一波/这个区在哪一跳掉得最狠"，避免凭印象写 verdict：

```
python tools/step_funnel.py --region $REGION            # 文本视图
python tools/step_funnel.py --region $REGION --json      # 机器可读
python tools/step_funnel.py --region $REGION --wave $W   # 只看单波
```

- **只读推导**：数据全部来自既有 4 张表 + ledger（`expressions` / `gate_results` /
  `backtest_results` / `wave_results`），**不建表、不写库、不产生任何新数据**。
- 输出 S2 生成池（含 `unconsumed = gem+selected+pending+gated` 溢出比）/
  S2→S3 门禁（批次粒度 + 表达式粒度双口径）/ S3 回测（含过廉价闸数、最佳 sharpe）/
  S4→S5 就绪 / S6 verdict 分布 / 转化链 / **瓶颈定位**。
- ⚠ 口径局限（工具已自标）：各步取的是**各自表的存量**，时间窗不完全一致 →
  链上数值**可能不单调**，仅用于定位瓶颈，不作精确转化率引用。
- ★ 五张 `step_*` / `*_summary` 表**恒 0 行且不应填充**（评估结论见
  `tools/step_funnel.py` 头部：自动采集是 TODO 空壳、质量指标可从既有表推导、
  增益指标是反事实估算无客观来源）。**要步级视图就用本工具，不要往那五张表写。**

**自动部分（2026-09-15 ③）**：`pipeline.py --review` 收批后除写 `wave_results` 外，会自动刷新 `region_kb`：
`recent_waves`（近 20 波摘要：wave/dataset/n/candidates/near/best_sharpe/verdict）、`gate_priors_local`
（本地 backtest_results 重算的 by_neutralization / by_operator_count / by_field_family 过闸率；本地行无 decay 维度，
decay 仍以 `tools/build_gate_prior_from_inventory.py --write-priors` 的 `gate_priors` 为准）与 `updated_at`。
下一波步 4 assemble-priors / 步 6 settings prior 读到的因此总是最新。**手动部分**（win / dead_end / seal / pyramid）仍按下文执行。
`wave_results.verdict` 只接受 PASS / FAIL / PARTIAL：`mcp__wqb-db__upsert_wave_result` 会把 `FAIL_xxx：…` / `CLOSED_DEAD_END_…` 这类
前缀形态归一到枚举并把原文搬进 `key_findings[0]`，无法辨认的直接拒绝——描述性结论请写 `key_findings`。

```
mcp__wqb-db__upsert_wave_result  region=$REGION  wave=$W  verdict=<PASS|FAIL|PARTIAL>  ...
mcp__wqb-db__upsert_registry_empirical  region=$REGION  ...
mcp__wqb-db__upsert_ledger_key  region=$REGION  key="s6_verdict_<wave>"  ...
```

**判死封存（2026-09-13 新增：先沉降、再封存）**：任何 `dead_end` 回写前先调
`seal_dead_end`——把该 idea 涉及波次的失败候选沉降入 salvage_pool（收集宽），
并把残值列表回填 `dead_end.salvage`（原 schema 预留字段，此前恒 null）。
救援动用仍守各区 `mode_b_qualification` 资格线（动用严），本工具不改动用侧：

```
mcp__wqb-db__seal_dead_end  region=$REGION  entry_id=<DEAD_END_ID>  family=<族名>  wave_numbers=[W1,W2,...]
```

OS ACTIVE / 全闸 PASS 必须 `add-win`（mix 比例、中性化、decay、快/慢腿）。

**点塔进度回写（2026-09-09 新增，`tools/campaign_intel.py pyramid`）**：每波 S6 必调，
把本区点塔进度（各 catalog 已点亮/未点亮/还差几颗）嵌入 `wave_result.key_findings`，
让下一波 S0 选集直接消费平台真实塔状态（而非本地推断）：

```
python tools/campaign_intel.py pyramid --region $REGION --delay $DELAY
# 输出末尾的 [key_findings] 单行直接拷进 upsert_wave_result 的 key_findings 列表
```

**提交多样性监控（防同质化降权）**：每提交 3-5 颗后调一次，若多样性评分下降则切换目标塔：

```
mcp__wq-brain-http__value_factor_trendScore  start_date=<本季初>  end_date=<今天>
```

**提交后 IS→OS 衰减归因（可选，反哺 IS 阈值校准）**：提交后 T+1 调
`mcp__wq-brain-http__performance_comparison alpha_id=<ID>`，把 IS→OS 衰减写进 wave_result，
验证「提交时 IS 指标是否虚高」。
- **prod 饱和反馈 S0**：若本波候选全部被 `prod_corr >= 0.7` 卡死（submit_verdict BLOCKED 原因含 PROD_CORRELATION），除 `add-dead-end` 外须在 ledger `submit_ready_blocked` 追加该数据集/信号族饱和记录；下一轮 S0（步 2）体检读取，把该数据集按拥挤处理（即使平台 alphaCount≤50 也降优先级），避免重复撞墙。

---

## 整链执行（可选）

九步中**步 2/3/4/5/6 有 workflow 节点**（registry 注册 8 个：`campaign` / `feature_engineering` / `gem` / `batch_track` / `wave_gate` / `judge` / `submit_alpha` / `superalpha`）。步 1 查表、步 7 S4 评审、步 8 提交判定、步 9 复盘回写**无节点**，需按对应章节单独执行（2026-09-11 审计纠正：旧文称"九步可以整条交给 workflow_chain"，与 registry 实际能力不符；同批新增 `wave_gate` 节点，使步 5 门禁首次可入链）。链式调用先干跑再实跑：

```
mcp__wq-brain-http__workflow_chain  dry_run=true  chain=[
  {"node": "campaign",            "params": {"region": "$REGION", "stage": "S0"}},
  {"node": "feature_engineering", "params": {"region": "$REGION", "dataset_id": "$DS", "delay": $DELAY, "universe": "$UNIVERSE"}},
  {"node": "gem",                 "params": {"region": "$REGION", "dataset_id": "$DS", "delay": $DELAY, "universe": "$UNIVERSE", "data_type": "$DTYPE"}}
]
```

干跑会逐节点把真实命令构建出来（不 subprocess、不写库）并**校验命令能否被目标脚本的
argparse 接受**，`failed_at` 指出首个断点。

**异步 join（2026-09-06）**：`workflow_chain` 默认 `join_async=True` —— gem / batch_track /
campaign / feature_engineering 都是"启动即返回"，链会等上一步的后台任务到终态再走下一步，
任务失败即按该步失败中止。此前没有这个机制，实跑时下游节点必然读到上游还没落库的空结果，
链只在干跑下"看着通"。要"只发起不等待"就传 `join_async=false`，然后自己用
`workflow_task_status` 跟踪；单步等待上限 `join_timeout_sec`（默认 1800s）。

**提交类节点不入链**：`submit_alpha` / `superalpha` 的 `confirm_submit=True` 必须在步 8
经用户明确确认后单独调用，禁止塞进自动链。

## 循环与停止

步 2 → 步 9 为一波。

| 条件 | 动作 |
|---|---|
| **停止规则闸自动拦截**（2026-09-15 ⑦ SQL 化，`workflow_campaign(stage="S2"/"S3")` 前置，零配额、干跑也走） | 规则 A：该区 `backtest_results` ≥100 条且达标（S>1.58 & F>1.0）0 条；规则 B：最近 3 个 closed 波 `verdict` 全 FAIL（verdict 已强制枚举，见步 9）。命中即拒绝开波并给出台账覆盖写法。**用户显式要求继续**时写 `mcp__wqb-db__upsert_ledger_key(region, "stop_rules_override", {"reason": "<用户指令与理由>", "until": "YYYY-MM-DD"})` 放行（SOP：用户指令优先，但台账留痕；GBR 已按 09-12「stay in GBR」指令写入，至 09-30）。阈值在 `thresholds.json` `diversity.stop_rules`（`yield_min_backtests` 100 / `consecutive_fail_waves` 3 / `enabled`）。 |
| 连续 3 波全 FAIL 且无新 dead_end | 该 region 暂停，转 `brain-next-move-analysis`（现由上一行规则 B 机械判定） |
| 白名单被 dead_end 全覆盖 | 停止 |
| 连续 3 波 gate 通过率=0（`gate_results.all_pass` 全 0） | 该区信号族/数据集判死，转 `wq-brain-campaign-matrix` 换数据集，或转 `brain-next-move-analysis` 换区域 |
| **信号天花板闸自动拦截**（2026-09-06 接线） | **参数唯一权威位置 = `tracking/<REGION>/config/thresholds.json` 的 `diversity.signal_floor`**（2026-09-17 P2-12 明确；**不在** references/regions/*.md 的 profile 里，profile 只写区域画像）。`workflow_campaign(stage="S2"/"S3")` 前置自动判定：最近 `min_batches` 个波次 `max\|sharpe\| < max_sharpe_floor` 即拒绝开波（`max_sharpe_floor` 缺省 0.5 / `min_batches` 缺省 2；**语义注意**（2026-09-17 改版）：整节缺失时改为 **fail-closed** —— 回落默认 `max_sharpe_floor=0.5 / min_batches=2` 继续判定并输出 `warning`（旧行为是静默放行，与停止闸使命矛盾）；**仅显式 `enabled:false` 才放行**。`thresholds.json` 不可读时同理。**实测 13/13 区域均已配该节**（AMR ASI CHN DEU EUR GBR GLB HKG IND JPN KOR MEA USA，2026-09-17 复核；旧文档记「11 区」为漏计 AMR/GLB）。2026-09-11 按实证回填（规则：每波 max\|sharpe\| 的 p25、**只上调不下调**、样本≥8 波）：**IND=1.2 / USA=0.9 / MEA=1.2**，其余区域维持 0.5 —— 对高信号区 0.5 形同虚设（USA 曾 0/13 波、MEA 0/47 波低于 0.5）。注意 `_evidence` 里"样本 0 波"指的是**回填需 ≥8 波的样本门槛未达**（故不上调 floor），**不是**该区闸失效：DEU 实测 `batches=2 / max_sh=1.7 / verdict=ok`（2026-09-17）。纯 DB 判定零配额，干跑也走。被拦即换 universe / 换数据集 / 换区域，不要绕过。历史教训：这套配置早就写好了却零调用方，GBR 因此跑满 180 条回测、`max\|sharpe\|=1.04`、达标 0 条。 |
| ACTIVE RA ≥10 | 可转 `wq-brain-superalpha`（先 `mcp__wq-brain-http__sa_probe --region $REGION`） |
| 配额耗尽 | 挂起提交，继续步 2 → 9。 |
| 用户要求持续日循环 | 每个 NY 日先 `brain-next-move-analysis`，再从步 1 跑；日界 21:30 ET |

可选外壳：`scripts/ralph_daily_loop.py` / `ralph_runner.py`（状态模板 `templates/daily_state.template.json`）。循环体仍是上面九步，不是第二套 SOP。

---

## 快捷入口

**发批 / 回测批次**（用户已给表达式列表）：直接走步 5，跳过 S0–S2。未给列表则从步 2 走完整链。

**一键战役 / auto campaign**：步 1 matrix 后 步 2 体检（不可跳过）则配置包写回 `settings.json` 后 步 3。matrix 失败即停。默认先干跑看 gate 通过率，确认后再提回测。用户说「自动提交回测」可跳过二次确认；**提交 alpha 仍要步 8 用户确认**。

---

## PPA 分支

仅当 `get_messages` 当前 Power Pool 主题匹配 region/delay/universe 时挖 PPA；不匹配则挖 RA。
经验细则 [references/ppa-mining-experience.md](references/ppa-mining-experience.md)。
PPA 日循环停止闸：submit-ready ≥4。**配额是三条并行通道**：`REGULAR_SUBMISSION` 4/日 + `SUPER` 1/日 + **PPA 独立的 `POWER_POOL_SUBMISSION` 1/日**（均 00:00 ET 重置）——PPA 那颗**不占** REGULAR 额度，故日循环应**当天优先提 PPA 那一颗**。PPA 提交仍须用户确认。
不要把 `wq-brain-ppa-mining` 当编排器调用。

---

## Artifact 契约

战役产物只入 `data/wqb.db`。禁止 Write 战役 json/csv。

| 阶段 | 入库 | 由谁写 |
|---|---|---|
| S0 | ledger `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>` / `*_dead` | `score_datasets.py`（toolkit）；手工锁白名单用 `mcp__wqb-db__upsert_ledger_key` |
| S1 | ledger `s1_<ds>_d<delay>` + ideas.md 路径；`field_catalog` | `scan_fields.py` / `workflow_feature_engineering`；字段目录 `mcp__wqb-db__upsert_field_catalog` |
| S2 | `expressions` status=`gem`/`enhanced`；ledger idea；`priors_snapshot_<region>` | `workflow_gem` 落库 + `assemble-priors`；直写用 `mcp__wqb-db__upsert_expressions` |
| S2→S3 | `gate_results`（`all_pass` / `fail_reasons`） | `wave_gate` / `gate.py`；直写用 `mcp__wqb-db__upsert_gate_result` |
| S3 | `backtest_results` / `wave_results` / checkpoint | `pipeline.py`（toolkit）；收割用 `mcp__wq-brain-http__harvest_multisim_alphas` + `mcp__wqb-db__harvest_multisim_results` / `upsert_backtest_rows` |
| S4 | ledger `s4_walls_<region>_<wave>`；`salvage_pool` | `review_wave.py`；补池用 `mcp__wqb-db__backfill_salvage_pool` |
| S6 | `wave_results.verdict` + `registry_empirical` + ledger `s6_verdict_<wave>` | `mcp__wqb-db__upsert_wave_result` / `upsert_registry_empirical` / `upsert_ledger_key` |

> 「由谁写」列 2026-09-05 补：此前 `upsert_expressions` / `upsert_gate_result` /
> `upsert_backtest_rows` / `upsert_field_catalog` / `harvest_multisim_*` 这几个写库工具
> 在任何 skill 里都找不到归属，表里却写着这些表要落库——谁落没写清，就会有人手写脚本绕过。

---

## 反模式

- 再 invoke `brain-deepExplore` 或按其旧 S2-D/S2-M 必跑、停止闸 4 覆盖 RA。
- 手写 `_gate_waveNN.py` / `w*_batches.json` / 把 GEM `final_expressions.json` 当真相源。
- 手写 requests；跳过步 9；在本文件复写阈值；`combination(alpha(...))`。
- 七槽全裸探针；七槽全 MODEL + 固定 COUNTRY/decay6。
- 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填槽。
- submit_verdict READY 后自动 `workflow_submit_alpha`。
- 调用已废弃的 `glb_pipeline` / `gbr_pipeline` / `glb_alpha_machine`。
- 直接把 `brain-feature-implementation` 当主链入口（它在 GEM 内部）。
- 手写 PowerShell 命令替代 MCP 工具调用（能走 MCP 的步骤一律走 MCP）。

---

## 附录：工具名映射表（2026-09-07 P2-2）

MCP 工具调用名 = `mcp__<server>__<注册名>`。注册名与所在模块不同名不同处，查表调用，勿凭记忆猜：

| 逻辑名（文中惯称） | MCP 调用名 | 实际定义处 |
|---|---|---|
| workflow 战役 | `mcp__wq-brain-http__workflow_campaign` | world-quant-brain-mcp/tools_workflow.py |
| workflow 特征工程 | `mcp__wq-brain-http__workflow_feature_engineering` | tools_workflow.py |
| workflow GEM | `mcp__wq-brain-http__workflow_gem` | tools_workflow.py |
| workflow 批量跟踪 | `mcp__wq-brain-http__workflow_batch_track` | tools_workflow.py |
| workflow 链 | `mcp__wq-brain-http__workflow_chain` | tools_workflow.py |
| workflow 执行 | `mcp__wq-brain-http__workflow_execute` | tools_workflow.py |
| workflow SuperAlpha | `mcp__wq-brain-http__workflow_superalpha` | tools_workflow.py |
| workflow 提交 | `mcp__wq-brain-http__workflow_submit_alpha` | tools_workflow.py |
| workflow 判定（**参考层**，非提交裁决） | `mcp__wq-brain-http__workflow_judge` | tools_workflow.py。返回 `verdict`（READY/REVIEW/BLOCK）**只是摘要**，请优先读 2026-09-17 新增的 `checklist`（逐闸事实）与 `degraded_gates`（取不到数的闸）。**`degraded_gates` 非空 ⇒ `verdict` 不可作提交依据**（降级闸此前会静默凑出 READY）。 |
| 节点清单 | `mcp__wq-brain-http__workflow_list_nodes` | tools_workflow.py |
| 任务状态 | `mcp__wq-brain-http__workflow_task_status` | tools_workflow.py |
| 提交判定（唯一权威） | `mcp__wq-brain-http__submit_verdict` | tools_ops.py |
| 批量提交 | `mcp__wq-brain-http__submit_batch` | tools_ops.py（非 workflow 族） |
| SA 探针 | `mcp__wq-brain-http__sa_probe` | tools_ops.py（非 workflow 族） |
| 表达式预检 | `mcp__wq-brain-http__preflight_expressions` | tools_data.py（非 workflow 族） |
| 回测收割 | `mcp__wq-brain-http__harvest_multisim_alphas` | tools_sim.py |
| 直写表达式 | `mcp__wqb-db__upsert_expressions` | wqb_db_mcp.py |
| 批量改表达式状态（只传 id/状态过滤，不回传正文） | `mcp__wqb-db__set_expression_status` | wqb_db_mcp.py |
| 直写门禁结果 | `mcp__wqb-db__upsert_gate_result` | wqb_db_mcp.py |
| 直写回测行 | `mcp__wqb-db__upsert_backtest_rows` | wqb_db_mcp.py |
| 直写字段目录 | `mcp__wqb-db__upsert_field_catalog` | wqb_db_mcp.py |
| 直写 ledger | `mcp__wqb-db__upsert_ledger_key` | wqb_db_mcp.py |

> 维护规则：改 MCP 工具名/归属时同步更新本表；新增 workflow_* 工具须登记。工具/节点计数**唯一基准 = `Claude/skills/INDEX.md`「MCP 工具/节点计数基准段」**（当前 wq-brain-http 68 / wqb-db 36 / workflow 节点 9，测试守护），本表不另维护数字。
