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
last_verified: 2026-09-02
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

---

## 九步流水线

每步含 **目的 / MCP 调用 / 产物 / 失败分支**。任一步 FAIL 就地回退，不允许跳过继续。

### 区域 Profile 路由（2026-08-25 落地）

九步骨架全区域共用，**区域差异通过 profile 注入**：`references/regions/<REGION>.md` 每区一份（USA/EUR/KOR/IND/ASI/GBR/HKG/MEA/GLB/CHN/TWN），YAML front-matter 声明静态配置/数据集红黑榜/priors/闸门覆盖/循环策略，正文写明变体理由。

四个注入点：

| 注入点 | profile 字段 | 影响步骤 |
|---|---|---|
| 入口裁决 | `entry_verdict`（active / probe-only / frozen） | 步 1 |
| 生成先验 | DB KB 优先：region_kb win/dead + template_kb 骨架 组装 priors.json；profile 静态 priors 仅兜底 | 步 4 |
| 闸门特化 | `gate_overrides`（CW / longCount / prod_corr 阈值） | 步 5、步 7、步 8 |
| 循环策略 | `loop_policy`（探针上限、快判死、停止条件） | 步 2、步 6、循环表 |

规则：profile 与骨架正文冲突时**profile 优先**（它是区域实证结晶）；profile 缺字段回落骨架默认；profile 未覆盖的 region 走通用处女地模板（参照 ASI profile）；`frozen` 区域（当前仅 MEA）步 1 即拒，唯一后门见该区 profile。

### 步 1（S-PRE）查表

目的：region 先验，避免重复已判死路径。可选并行：`brain-nextMove-analysis`（日报，不产出配置）、`brain-forum-browse`。

**先读区域 profile**：`Read references/regions/<REGION>.md`，按 front-matter 渲染本区专属 SOP（后续各步标注"profile"处按其覆盖执行）；`entry_verdict: frozen` 则按该区 profile 的入口裁决处理，不继续步 2。

**开工前置（每次新战役/新会话必做）**：
- **算子审计（ghost-op guard）**：调 `mcp__wq-brain-http__operator_audit`（无 expressions 参数）拉取平台实时算子列表，与 catalog 对比。幽灵算子清单与替换表见 `docs/reference/operators_notes.md`；论坛帖引用这些名字时先替换再进批。
- **PPA 主题匹配门禁**：调 `mcp__wq-brain-http__get_messages`（limit=30）扫描 `type=="ANNOUNCEMENT"` 标题含 "Power Pool" 的公告，解析当期主题的 region/delay/universe/中性化集合/禁止数据集/有效时间。PPA 提交必须**精确匹配**主题；不在当期主题的达标候选标 YELLOW + WAIT_THEME_ROTATION。RA 常规提交不受主题限制。

```
mcp__wqb-db__get_campaign_summary  region=$REGION
mcp__wqb-db__get_dead_ends         region=$REGION
mcp__wqb-db__get_dead_datasets     region=$REGION
mcp__wqb-db__get_cross_region_lessons
```

详细口径见 [wq-brain-campaign-matrix](../wq-brain-campaign-matrix/SKILL.md)。

* **产物**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号。

* **失败分支**：registry 全空 = 新区域，进步 2 并在步 9 写 campaign；`get_dead_datasets` 已覆盖全部候选则停止，转 `brain-nextMove-analysis` 选新区域。

### 步 2（S0）数据集体检 + 金字塔配置

调 `mcp__wq-brain-http__workflow_campaign`（stage="S0"）。无战役目录的跨区试探才用本目录 `scripts/dataset_health_check.py`。
锁白名单后必须 `mcp__wqb-db__upsert_ledger_key(region, "s0_whitelist", {...})`。`recommend_datasets` 不能替代体检。

硬约束：

1. 读 `registry_empirical` win 层：已验证配方的数据集族必须进候选。
2. `pyramid_quota_enable`：白名单至少 **2 个非 MODEL**（PV / NEWS / ANALYST / institutions）；不够则 tier2 上提，`tier_note=pyramid_quota`。
3. `category_weight` 只允许 0.9–1.15，禁止 1.3 vs 0.7 抹掉整座金字塔。
4. `*_dead` 仍排除；主导腿禁用 ≠ 整集判死。
5. 白名单外禁止 generate / simulate。

```
# 评分前先校准（实测反学 category 权重 + 拥挤甜区）：先 dry-run 人工审，确认无异常再 apply
# 审两处异常：甜区 ac 异常巨大（如 MEA 8560-21508 反向奖励超拥挤）/ strong_acs 空（无强信号）
# 详见 wq-brain-campaign-toolkit/references/probe-scoring-v2.md「评分前必做：calibrate 自学习校准」
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S0"  calibrate=true  dry_run=true
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S0"  calibrate=true
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S0"
mcp__wqb-db__get_ledger_key  region=$REGION  key=s0_ranking
```

* **失败分支**：配额后仍无非 MODEL 则写 findings，不要退回纯 MODEL 七槽；全部硬排除 则回步 1 换 region。

### 步 3（S1）字段扫描 + 理解

必做 typed catalog。字段理解用 `mcp__wq-brain-http__workflow_feature_engineering`（独立调用，ideas 回写 `s1_<ds>_d<delay>`，`source=standalone`）。深查可前置 dataset/datafield exploration。

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
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S6"  subcommand="assemble-priors"
```

assemble-priors 内部映射（供核对，勿手写）：

1. `wins`（按序，合计≤6 条）：① `get_ledger_key("GLOBAL", "region_kb")` → `templates[]` 通用模板 → `{"id": <name>, "key": "skeleton=<skeleton>; evidence=<evidence>; source_region=<source_region>"}`；② `get_ledger_key($REGION, "region_kb")` → `win_recipes[]` → `{"id": <name>, "key": "skeleton=<skeleton>; evidence=<evidence>; settings=<settings>"}`；③ `get_ledger_key("KB", "template_kb")` → `validated` 含本区的模板 → `{"id": "<id> <name>", "key": "skeleton=<skeleton>; iron_law=<iron_law>"}`。
2. `dead_ends`（按序，合计≤12 条）：① region_kb → `dead_patterns[]`（字符串直传）；② template_kb → `failed` 含本区的模板 → `{"family": "<id> <name>", "reason": "<failed 原因>"}`；③ profile `priors.signal_families_exclude` 并入。
3. region_kb 未命中/为空 → 兜底用本区 profile front-matter 静态 priors（`win_recipes` + `signal_families_exclude`）。
4. `GLOBAL/region_kb` 的 `methodology[]` 与 `signal_family_rules[]` 作为 `region_context` 注入 GEM prompt（见 `economic_priors.py` 的 `compact_priors_text()` 输出）。
5. `KB/community_tpl_kb` **不进 priors**（候选未实证，注入稀释 concept-first）。它服务两个场景：步 5 多样性 FAIL 回本步补骨架时按 `category` 检索换腿参考（占位符按 `placeholder_conventions` 替换）；Mode B Step B1 找骨架。**取骨架前必查键内 `ghost_operator_advisory`**：含幽灵/未验证算子（如 sigmoid/ts_entropy/ts_skewness/ts_percentage/ts_decay_exp_window 等）的骨架必须替换已验证等价算子（映射表见键内与人读手册 `docs/reference/community_tpl_library_sequel.md` §十八）或先 `mcp__wq-brain-http__preflight_expressions` 实测，否则整批 ERROR/CANCELLED。

生命周期闭环：本协议使 DB KB 成为 S2 先验唯一上游——S6 回写 region_kb / template_kb 后，下一次 S2 先验自动变新；profile 静态 priors 仅作 DB 空时的种子，不再手工更新。

```
$DELAY    = (settings.json).delay
$UNIVERSE = (settings.json).universe
$DTYPE    = (catalog).data_type
# 确定性组装 priors 并写 DB 快照（priors_snapshot_<region>）——DB 为单一事实源
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S6"  subcommand="assemble-priors"
mcp__wqb-db__get_ledger_key  region=$REGION  key="s1_${DS}_d${DELAY}"
# GEM 生成（ideas_file 可从 S1 ledger 自动注入，也可显式传入覆盖）
mcp__wq-brain-http__workflow_gem  region=$REGION  dataset_id=$DS  delay=$DELAY  universe=$UNIVERSE  priors_file="<priors_path>"
# 注：priors_file 已可省略——GEM 经 load_priors(region) 从 DB 快照直读，文件仅降级兜底
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  dataset=$DS  wave=$W
```

消费 `methodology_rules`（build-wave 配给，不替代 GEM）。该 `$DS` 本区域从未跑过 GEM 则必须先跑 GEM。
未验证 DB 有表达式，不得声称步 4 成功。

* **失败分支**：GEM 未入库则按超时恢复清单查任务，确认失败才回退，不要手写；候选不足则 enhance / 扩组合，仍不足换数据集。

### 步 5（S2→S3）门禁

禁止新建 `_gate_waveNN.py`。禁止写 `cache/gate_wave*.json`。

**生成→回测双硬门（orchestrator 迁移，回测前必过）**：
1. **多样性守卫 check_batch**：每批表达式提交前通过 `wqb.expression.validator.check_batch(...)`：≥3 dual-field、≥2 outer wrappers、≥2 windows、≥2 group variables、≥2 shape signatures；混入非对称 shape（`op1(A)-op2(B)` / `A-op2(B)` / `rank(A) vs group_rank(B,g)`）；轮转 13 范式 P1-P13（含 5 论坛范式 + 12 非对称变体）。
2. **体检→表达式硬门 check_expr_against_inspect**：函数在 `tools/webdata_quality.py`（不在 `wqb.expression.validator` 里）。字段体检结果按数据集分文件落在 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`（由 `tools/webdata_quality.py --export-expr <path>` 生成；缺文件先跑一次生成）。对每条表达式调用 `check_expr_against_inspect(expr, result)`。5 条硬门：低覆盖(cr<0.4)必须含 `ts_backfill`；高偏度(|skew|>2)必须含 `rank`/`winsorize`/`signed_power`；厚尾(kurt>8)必须含 `rank`/`winsorize`；单边恒正/负不能直接用原始水平；稀疏事件(zero_inflated/point_mass)必须用 `trade_when`。任一 `ok=False` 拒绝，修复后重验。
3. 流程：`check_batch → check_expr_against_inspect → 下方 wave_gate → 步 6 create_multi_simulation`。

```
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S2"  dataset=$DS  wave=$W
```

VECTOR 用 `mcp__wq-brain-http__preflight_expressions`（auto_fix_vector=true）；repair 批加 `--skip-diversity-gate`。

- **失败分支**：语法 FAIL 必须先修；多样性 FAIL 则回步 4 补骨架（可查 `KB/community_tpl_kb` 按 category 检索候选骨架，占位符按 `placeholder_conventions` 替换，并先查 `ghost_operator_advisory` 做幽灵算子替换）；若 2 跨集 FAIL 则拆回单集组合，不停挖。

### 步 6（S3）七槽回测

并发唯一来源 [wqb-concurrency](../wqb-concurrency/SKILL.md) §8。
S3 入口也可走 [brain-simAlphasinBatch-and-track](../brain-simAlphasinBatch-and-track/SKILL.md) 或 toolkit，填槽内容仍以本步为准。
设置展开需要时用 [brain-inspectRawTemplate-create-Setting](../brain-inspectRawTemplate-create-Setting/SKILL.md)（`--from-db`），不是第三条生成器。

1. 空槽补组合批，不用裸探针凑数。
2. 弱探针最多 1 槽；已有近闸字段时为 0。
3. 设置跟 win：EUR 实证 `SUBINDUSTRY` + `decay4`。可另探 `ILLIQUID_MINVOL1M` / `TOPCS1600` / `delay0`。
4. prod-first：每槽先 1-2 条骨架查 `prod_corr`；≥0.7 停扩换腿。
5. 表达式从 `mcp__wqb-db__list_expressions` 取。`mcp__wq-brain-http__submit_verdict` 判定 SUBMITTABLE 见步 8，禁止自动提交 alpha。

```
# concurrency 默认 7（七槽填槽），429 时降至 ≤5
mcp__wq-brain-http__workflow_batch_track  region=$REGION  wave=$W  dataset=$DS  concurrency=7
# 批次状态查询（单次，非轮询）
mcp__wq-brain-http__batch_status  simulation_ids=["<id1>", "<id2>"]
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

- **积压清理（每波结束时）**：只读 SQL 查积压 `SELECT region, status, COUNT(*) FROM expressions WHERE region=? GROUP BY status`——若 `pending`+`gated` > 本波表达式数 2 倍，说明 S2→S3 断链，本波结束优先把近闸积压纳入下一波（`build_wave --from-db` 重取），禁止无脑新建表达式堆库。

### 步 7（S4）诊断改进

```
mcp__wq-brain-http__workflow_campaign  region=$REGION  stage="S4"  dataset=$DS  wave=$W
```

阈值不达标见 [brain-how-to-pass-AlphaTest](../brain-how-to-pass-AlphaTest/SKILL.md)。
用 [wq-brain-alpha-optimization-v1](../wq-brain-alpha-optimization-v1/SKILL.md)（Mode B 70% / Mode A 30%）。
按需：`brain-calculate-alpha-selfcorrQuick`（本地快筛）/ `brain-explain-alphas`（按需归因：Mode B 换概念前查概念重叠，非每候选必经）。
`brain-alpha-repair` 只作配方查表。

- **失败分支**：`prod_corr ≥0.7` 则 Mode B 换概念；同一想法 >10 种结构仍不过 则步 9 记 `dead_end`，回步 2。
- **prod 验证排队调度**：多候选时走串行泳道（本地检查全批先跑、prod 队列恒保持 1 在飞、等待期插本地活），细则见 [references/prod-corr-avoidance.md](references/prod-corr-avoidance.md) §7（含 7 天结果缓存与 `refresh` 终验）。

### 步 8（S4→S5）稳健闸与提交判定

S4→S5 必经 [brain-alpha-robustness](../brain-alpha-robustness/SKILL.md)（反过拟合/稳健性闸）。

**提交判定链（顺序执行；最终提交判定唯一权威 = 第 2 步 submit_verdict）**：

1. **Failed-count 资格门（研究侧硬前置）**：进入提交流程前，从 `is.checks` 计算 WebDataScope failed counts（规则见 [references/webdatascope-failed-gates.md](references/webdatascope-failed-gates.md)）。REGULAR 要求 `Failed RA == 0`；PPA 要求 `Failed PPA == 0`。比只看 `result=="FAIL"` 严格（WARNING/ERROR 也计数）。枚举每个 counted item 的 name/limit/value；非零 → 回步 7 修复，不进入提交。

```
mcp__wq-brain-http__submit_verdict  alpha_id=<ALPHA_ID>
```

2. **submit_verdict 零成本判定（提交层权威）**：`mcp__wq-brain-http__submit_verdict` 给出模拟层 checks + GET `/alphas/{id}/submit` 双视图（403 盲区唯一权威），确认无 FAIL 且提交层 200。**是否提交的最终判定以本步为准。**
3. **brain-alpha-judge（可选参考层，非提交判定权威）**：PPA 主题匹配/相关性门控的**人工核对清单** + value-factor trend score（防挤同一金字塔）参考；PPA 主题不匹配 → `WAIT_THEME_ROTATION`。其 READY/REVIEW/BLOCK 三态输出仅作评审参考，不构成提交依据（judge 已于 2026-08-31 自我弃用最终判定角色）。

**submit_verdict 判定 SUBMITTABLE / judge 参考评审 READY 都只报告、等用户确认**。确认前禁止 `mcp__wq-brain-http__workflow_submit_alpha` / `mcp__wq-brain-http__submit_batch`。
pipeline `--submit` = 提交回测，不是提交 alpha。

* **失败分支**：`PASS_CHEAP` 则可提交；PROD/SELF 不过 则回步 7；配额耗尽按 ET 日历日（00:00 ET 重置）等待。

### 步 9（S6）复盘回写

未回写视为本波未完成。细节见 [wq-backtest-monitor](../wq-backtest-monitor/SKILL.md) §14。

```
mcp__wqb-db__upsert_wave_result  region=$REGION  wave=$W  verdict=<PASS|FAIL|PARTIAL>  ...
mcp__wqb-db__upsert_registry_empirical  region=$REGION  ...
mcp__wqb-db__upsert_ledger_key  region=$REGION  key="s6_verdict_<wave>"  ...
```

OS ACTIVE / 全闸 PASS 必须 `add-win`（mix 比例、中性化、decay、快/慢腿）。
- **prod 饱和反馈 S0**：若本波候选全部被 `prod_corr >= 0.7` 卡死（submit_verdict BLOCKED 原因含 PROD_CORRELATION），除 `add-dead-end` 外须在 ledger `submit_ready_blocked` 追加该数据集/信号族饱和记录；下一轮 S0（步 2）体检读取，把该数据集按拥挤处理（即使平台 alphaCount≤50 也降优先级），避免重复撞墙。

---

## 整链执行（可选）

九步可以整条交给 `mcp__wq-brain-http__workflow_chain`，**先干跑再实跑**：

```
mcp__wq-brain-http__workflow_chain  dry_run=true  chain=[
  {"node": "campaign",            "params": {"region": "$REGION", "stage": "S0"}},
  {"node": "feature_engineering", "params": {"region": "$REGION", "dataset_id": "$DS", "delay": $DELAY, "universe": "$UNIVERSE"}},
  {"node": "gem",                 "params": {"region": "$REGION", "dataset_id": "$DS", "delay": $DELAY, "universe": "$UNIVERSE", "data_type": "$DTYPE"}}
]
```

干跑会逐节点把真实命令构建出来（不 subprocess、不写库），`failed_at` 指出首个断点。
**提交类节点不入链**：`submit_alpha` / `superalpha` 的 `confirm_submit=True` 必须在步 8
经用户明确确认后单独调用，禁止塞进自动链。

## 循环与停止

步 2 → 步 9 为一波。

| 条件 | 动作 |
|---|---|
| 连续 3 波全 FAIL 且无新 dead_end | 该 region 暂停，转 `brain-nextMove-analysis` |
| 白名单被 dead_end 全覆盖 | 停止 |
| 连续 3 波 gate 通过率=0（`gate_results.all_pass` 全 0） | 该区信号族/数据集判死，转 `wq-brain-campaign-matrix` 换数据集，或转 `brain-nextMove-analysis` 换区域 |
| ACTIVE RA ≥10 | 可转 `wq-brain-superalpha`（先 `mcp__wq-brain-http__sa_probe --region $REGION`） |
| 配额耗尽 | 挂起提交，继续步 2 → 9。 |
| 用户要求持续日循环 | 每个 NY 日先 `brain-nextMove-analysis`，再从步 1 跑；日界 21:30 ET |

可选外壳：`scripts/ralph_daily_loop.py` / `ralph_runner.py`（状态模板 `templates/daily_state.template.json`）。循环体仍是上面九步，不是第二套 SOP。

---

## 快捷入口

**发批 / 回测批次**（用户已给表达式列表）：直接走步 5，跳过 S0–S2。未给列表则从步 2 走完整链。

**一键战役 / auto campaign**：步 1 matrix 后 步 2 体检（不可跳过）则配置包写回 `settings.json` 后 步 3。matrix 失败即停。默认先干跑看 gate 通过率，确认后再提回测。用户说「自动提交回测」可跳过二次确认；**提交 alpha 仍要步 8 用户确认**。

---

## PPA 分支

仅当 `get_messages` 当前 Power Pool 主题匹配 region/delay/universe 时挖 PPA；不匹配则挖 RA。
经验细则 [references/ppa-mining-experience.md](references/ppa-mining-experience.md)。
PPA 日循环停止闸：submit-ready ≥4（ET 日历日 REGULAR 4/日配额保守占用）。PPA 提交仍须用户确认。
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
