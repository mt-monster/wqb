---
name: wq-brain-ra-pipeline
description: "REGULAR Alpha 挖掘的编排入口（九步：S-PRE→S6）。当用户要求在某区域开战役 / 从零到提交 / 一键战役（auto campaign）/ 持续自我探索或日内循环 / 挖 regular alpha 并跑到可提交时使用。已进入九步链之后的单点动作（选集、批量回测、提交）由对应 skill 承接；PPA / Power Pool 仅当当前主题匹配 region/delay/universe 时作为本 SOP 的分支，不另起编排器。本 skill 只编排，每一步调既有 skill 或 MCP 工具"
layer: L-RA
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__wqb-db__*
  - mcp__wq-brain-http__*
version: "3.2"
last_verified: 2026-09-30
---

# WQ BRAIN RA Pipeline（REGULAR Alpha 挖掘编排 SOP）

## 职责边界

- **本 skill 负责**：九步（S-PRE→S6）的编排与阶段决策——何时挖、在哪挖、走哪条分支，以及每步的调用顺序、判据、完成定义与失败去向（规定「怎么调」，不实现能力）
- **本 skill 不做**：不亲自动手——不产表达式（→ `brain-make-some-gem`）、不发批（→ `brain-sim-alphas-in-batch-and-track`）、不判提交（`submit_verdict` 只有**否决权**；放行 = 用户明确确认，见 `worldquant-submit-alpha`）
- **上游 / 下游**：上游 = 用户意图 + 区域 profile；下游 = 各步调用的 L0–L6 skill、MCP 工具与 `tools/*.py`（步 → 工具索引见 [`references/tool-index.md`](references/tool-index.md)）

> 本文件只写**规则与每步的骨架**；细则、证据、事故、情景卡在 `references/`，日期与变更在 [`../CHANGELOG.md`](../CHANGELOG.md)。旧版（v2.x）把这些混在一起，规则被埋在起因后面。

## 怎么读这份 SOP

**冲突裁决**（高 → 低）：用户显式指令（须留痕，即 waiver）> 代码 fail-closed 闸（唯一放行 = waiver）> 区域 profile > 决策表（[`references/decision-table.md`](references/decision-table.md)）> 本正文。**唯一例外**：prod 墙处置表 D0-P 不接受区域改写。
**红线不可覆盖**（`wqb.waiver.RED_LINES`）：提交前的用户确认、凭据（`world-quant-brain-mcp/.env`：禁止读取、打印、提交）、平台限额。例：用户说「继续挖 MEA」（frozen 区）→ 只能走 MEA profile 写明的 probe-only 后门。

**每步固定模板**：目的 / 前置 / 调用 / 产物 / 完成定义 / 失败分支（现象 → 动作 → 回哪步）/ 不做 / 细则。**「FAIL」有三种含义**——闸结果 FAIL、工具报错（`success=false` / 退出码 ≠ 0）、波结论 `FAIL`，各处会点名是哪种。任一步失败按该步失败分支回退，**不许跳过继续**。

**编号**：正文只用「步 N」；`S` 编号只出现在 MCP 参数处（`stage="S0"`）。

| 步 | 1 | 2 | 3 | 4 | 5 | 5b | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| 阶段 | S-PRE | S0 | S1 | S2 | S2→S3 | S3 收批后 | S3 | S4 | S4→S5 | S6 |

**术语**（同一个词一种含义，全表见 [`../GLOSSARY.md`](../GLOSSARY.md)）：**波内配额** = 一波里表达式的配比（旧称「七槽」）；**并发令牌** = 账户同时在飞的仿真上限（`slots=7`）；**批** = 一次 `create_multi_simulation`（8 条子模拟）。**dispatch（派发仿真）** = `POST /simulations`（`pipeline.py --submit`、`submit_batch` 都是它）；**submit（提交）** = 把 alpha 提交上平台，**不可逆**。信号族 = 字段集合，骨架指纹 = 前 2 个算子。

**变量**（前置块列全；缺则回问，不猜）：

| 变量 | 来源 | 说明 |
|---|---|---|
| `$REGION` | 用户 | 必填 |
| `$DELAY` / `$UNIVERSE` | `tracking/$REGION/config/settings.json` | 开新区先补 |
| `$DS` | 步 2 白名单（ledger `s0_whitelist`） | 数据集 id |
| `$W` | 步 4 选波产出的波号 | **字符串**（`97` 与 `s2_<ds>_d1` 都可） |
| `$DTYPE` | catalog 的 `data_type` | VECTOR 比例先用 `get_datafields` 确认 |
| `$TARGET_SEATS` | 用户 / 战役目标 | 独立座位数，缺省建议 ≈ 3 × 目标塔数 |

**分工**：本 skill = when / what；[`wq-brain-campaign-matrix`](../wq-brain-campaign-matrix/SKILL.md) = where（用户没给 REGION / 数据集时先调，多区并列 → 回问用户）；[`wq-brain-campaign-toolkit`](../wq-brain-campaign-toolkit/SKILL.md) = how（战役目录内执行引擎）；单条表达式修复 → `wq-brain-alpha-optimization-v1`；SUPER 组套 → `wq-brain-superalpha`；提交 → `worldquant-submit-alpha`；PPA 主题核查 → `wq-brain-ppa-mining`（不作编排器）。

## 运行前置

- **MCP 应用尽用**：能走 MCP 的步骤走 MCP（判据：有对应 MCP 工具即用；CLI 只用于「无对应 MCP」或「无 MCP 时」，清单见 `tool-index.md`）。网络调用走 MCP venv（`$WQ_PY`，定义见 [INDEX「运行环境铁律」](../INDEX.md)），禁止手写 requests；中文 JSON 走 `@file`（AGENTS.md §5）。
- **阈值不复写**：这里「复写」= 拷贝 `src/wqb/config.py` 的 `GATES*` 闸门值；区域 / 机制经验阈值允许，但**必须带出处**（波 / 日期 / 样本量）。
- 提示词模板（开新区 / 续波 / 发批 / 单条修复 / 日循环）见 [`references/ra-campaign-prompt.md`](references/ra-campaign-prompt.md)。

## 经验库（软层）：按步读实证

仓库 [`docs/experience/`](docs/experience/README.md)（2026-09-29 建立）沉淀已付学费的实证结论——**走到某一步先读对应篇**，不读等于重复踩坑：

| 当前在做的步 | 读 | 关键收益 |
|---|---|---|
| 步 1 选区选集 | [`03_region_dataset.md`](docs/experience/03_region_dataset.md) | 12 区过闸率排序 + MEA / IND / DEU 停投结论：profile 管「这个区怎么配」，03 管「这个区值不值得挖」 |
| 步 3–4 设计信号 | [`02_signal_patterns.md`](docs/experience/02_signal_patterns.md) | 组合形态铁律（含等权 `add(rank(A),rank(B))` 同属违规）、破闸合规旋钮 |
| 步 7 诊断改进 | [`05_antipatterns.md`](docs/experience/05_antipatterns.md) | 已证伪路径清单，避免在死路上继续烧模拟次数 |
| 步 8 提交判定 | [`01_platform_gates.md`](docs/experience/01_platform_gates.md) | 提交层四闸 + SUB 比值律 + 配额 / 相关性取数口径 |
| 改链路 / skill / DB | [`04_engineering.md`](docs/experience/04_engineering.md) | skill 单点写入、DB 写锁、节点五处同步 |

这些 md 是给人 / Agent 读的**软层**，**不进**上面「冲突裁决」链：与代码闸 / 决策表冲突时以后者为准，并回写经验库。**机器强制层另有其物**：`wq-brain-campaign-toolkit/config/methodology_rules.json`（全局）+ `tracking/<REGION>/reference/`（区域），由 `RuleStore.query()` 在 `build_wave` / `pipeline` / `gate` / `review_wave` 注入；两轨同源，**改一边要同步另一边**（`tests/unit/test_experience_kb_refs.py` 守引用锚点）。

## 区域 Profile

`references/regions/<REGION>.md`，每区一份（YAML front-matter + 正文；区域清单与 profile / 战役目录的对齐表见 [INDEX §区域清单](../INDEX.md)，权威是 `config.REGIONS`）。**开新区前必须先补 profile + `tracking/<R>/config/`**；无 profile 的区域走通用处女地模板（参照 ASI profile）。

| 注入点 | profile 字段 | 影响步骤 | 谁读 | 缺失回落 |
|---|---|---|---|---|
| 入口裁决 | `entry_verdict`：`active` / `probe-only` / `frozen` | 步 1 | **代码**（`region_rotation` / `region_status`） | `unknown`（区域轮转降权） |
| 生成先验 | `priors` | 步 4 | **代码**（`assemble-priors` 在 DB KB 空时兜底；GEM 读 priors 段） | 无先验 |
| 闸门特化 | `gate_overrides` | 步 5 / 7 / 8 | **文档**（agent 读了照办；代码不消费） | 全局默认 |
| 循环策略 | `loop_policy` | 步 2 / 6 / 循环 | **文档** | 全局默认 |

规则：profile 与正文冲突时 profile 优先（区域实证结晶）；profile 缺字段回落骨架默认；`entry_verdict` 三态的默认含义见 [`step1-inventory.md`](references/step1-inventory.md) §1.1，profile 只写与默认不同的部分。键的「谁读」、正文固定模板、`last_verified` 的含义、区域缺口见 [`region-profile-contract.md`](references/region-profile-contract.md)。

## 九步流水线

### 步 1（S-PRE）查表与库存分流

- **目的**：region 先验，避免重复已判死路径；判「先清库存」还是「开新挖」。
- **前置**：已读区域 profile（`frozen` → 步 1 即拒，只留 profile 写明的后门）。
- **调用**（顺序）：① 库存盘点 `tools/build_gate_prior_from_inventory.py` → `tools/select_ra_basket.py` ② 查表 `get_campaign_summary` / `get_dead_ends` / `get_dead_datasets` / `get_mining_yield` ③ **跨区死路**（`get_dead_ends` 不传 region、`get_cross_region_lessons`）④ PPA 主题（仅含 PPA 分支时）。
- **产物**：universe / delay / 中性化 / 排除集 / 排除信号族 / 当前波号 → 落 `settings.json`，步 2 再写 ledger `s0_ranking` / `s0_whitelist`。
- **完成定义**：给出分流结论——篮子条数 ≥ target **且**覆盖 ≥ 3 座未点亮塔 → **跳步 7 / 8**；否则进步 2，只补缺口塔。
- **失败分支**：registry 全空 = 新区域 → 步 2，并在步 9 写 campaign；`get_dead_datasets` 已覆盖全部候选 → 停，转 matrix 选区；库存足够 → 跳步 7 / 8。
- **不做**：不用 `LIKE` 直扫 sqlite 找跨区死路（`model1` 会误命中 `model109`）；region 作用域查询**不能**代替跨区检查；论坛**默认不查**（只在 [`forum-recon-triggers.md`](references/forum-recon-triggers.md) 列出的场合查）。
- **细则**：[`step1-inventory.md`](references/step1-inventory.md)；情景卡 RA-01（库存够不够）；跨区横比另读 [`03_region_dataset.md`](docs/experience/03_region_dataset.md)。适用决策表：D4。

### 步 2（S0）数据集体检 + 金字塔配置

- **目的**：选出本战役的数据集白名单（点塔均匀、跨区死路已排除）。
- **前置**：步 1 分流为「进步 2」；`settings.json` 已有 universe / delay。
- **调用**（**有序**，不要先锁白名单再读约束）：① `campaign_intel.py s0-select` ② `workflow_campaign(stage="S0", calibrate=true)`（写 `thresholds.json`，**不产出排名**）③ `workflow_campaign(stage="S0")`（产出 `s0_ranking`）④ 按白名单硬约束筛 ⑤ 锁 `s0_whitelist`（`upsert_ledger_key(..., mode="merge")`，禁整值覆盖共享键）⑥ 体检包核对。
- **产物**：ledger `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>`。
- **完成定义**：`s0_whitelist` 已写，且每个白名单数据集有 `field_inspect` 体检包（缺包 → 缺省 `warn` 告警放行；`--inspect-mode off` 才要 `inspect` waiver）。
- **失败分支**：配额筛后仍无非 MODEL → 写 findings，**不要退回纯 MODEL**；全部被硬排除 → 回步 1 换区。
- **不做**：**已点亮塔（当季 ACTIVE ≥ 3 的 category）不进白名单**（用户 2026-09-19 定案，`s0-select` 默认剔）；不用 `recommend_datasets` 代替体检；不整值覆盖 `s0_whitelist`。
- **细则**：[`step2-s0.md`](references/step2-s0.md)（含白名单硬约束 0–7 的「硬 / 准则」分栏与执行点）。适用决策表：D4 / D6 / D13。

### 步 3（S1）字段扫描 · 结构体检 · 字段语义归类

- **目的**：字段是什么类型 / 覆盖多少（typed catalog）、这个数据集能不能挖、这个字段能不能当信号（闸 SEM 前置）。
- **前置**：步 2 白名单。
- **调用**：`workflow_campaign(stage="S1", dataset=$DS)`；然后 `python tools/field_semantic_classify.py --region $REGION --dataset $DS --write-ledger`（**本地、零配额、秒级，GEM 之前必做**）。
- **产物**：`fields` 表 + ledger `catalog_<ds>` / `s1_prefix_<ds>` / `s1_semantic_<ds>`。
- **完成定义**：`catalog_<ds>` 里 coverage > 0 的字段数 ≥ 10，且 `s1_semantic_<ds>` 已写。
- **失败分支**：字段数 < 10 → 回步 2 把该集移出白名单（**< 5 → 仅条件腿**）；`catalog_<ds>` 覆盖为空 → 写 `<ds>_dead`；`wave_gate` 报缺 `s1_semantic_<ds>`（exit 2）→ 跑上面的 classify，**不要** `--skip-semantic-gate` 蒙混。
- **不做**：不把 `workflow_feature_engineering` 的产物（确定性模板渲染，非 LLM 推理）当 ideas 注入 GEM；不指望 GEM 侧已过滤非信号字段——**过滤只在步 5 的闸 SEM 才真正落地**。
- **细则**：[`step3-s1-semantic.md`](references/step3-s1-semantic.md)（两条必做铁律：字段级覆盖审计、验活幽灵字段）。适用决策表：D13。

### 步 4（S2）概念优先生成 + 选波

- **目的**：为白名单数据集产出候选表达式并选成一波（GEM 强制；`build-wave` 只去重 / 分桶 / 骨架配给，**不产表达式**）。
- **前置**：步 3 完成；有胜绩则本波**至少 2 个波内配额位按机制换腿**；时间窗口只用 1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260（其它窗口须给解释或实测证据）。
- **调用**：`workflow_campaign(stage="S2", subcommand="assemble-priors")` → `workflow_gem`（`pipeline_mode` 缺省 `phased`）→ `workflow_campaign(stage="S2", dataset=$DS, wave=$W)`（选波）。**取骨架前必查 `KB/community_tpl_kb` 的 `ghost_operator_advisory`**。
- **产物**：`expressions`（status `gem` / `enhanced` / `selected`）、ledger idea、`priors_snapshot_<region>`。
- **完成定义**：`list_expressions` 查到本波条目——**未验证 DB 有表达式，不得声称步 4 成功**。
- **失败分支**：GEM 报「no meta.json within 90s」→ **先查 LLM 通道**（`402` 余额不足会被误报；干跑验证不了可达性），不要重试；候选不足 → 显式扩容或分波，**不补参数变体凑数**；机制枯竭 → `forum_recon`（触发表 #2）。
- **不做**：不手写表达式（**手写 ideas ≠ 手写表达式**）；不手写 priors；不加权 / 等权相加两条信号腿（CLAUDE.md「禁止混信号调参」；允许的组合形态见步 7 §7.7）；不每个字段套一层 `rank`。
- **细则**：[`step4-generation.md`](references/step4-generation.md)（含 §4.5.1 模板形状配额与形状源）、[`assemble-priors-internals.md`](references/assemble-priors-internals.md)。适用决策表：D3 / D6 / D11。

### 步 5（S2→S3）门禁

- **目的**：在配额之前拦下坏表达式（一条坏式 ERROR 会取消整批 8 条兄弟）与同质化批。
- **前置**：本波表达式已入库；含 VECTOR 字段先 `preflight_expressions(auto_fix_vector=true)`。
- **调用**：① `python tools/campaign_intel.py ghost-audit --region $REGION --exprs-file <txt>`（幽灵算子硬闸，零配额，先拦）② `python tools/wave_gate.py --campaign-dir tracking/$REGION --dataset $DS --wave $W --from-db`（节点等价 `workflow_execute(node="wave_gate")`；`workflow_campaign(stage="S2")` 是**选波**，不能代替本步）。
- **产物**：`gate_results`。**闸清单只在 [INDEX 两张生成表](../INDEX.md)**（`GATE_REGISTRY` / `waiver.GATE_POLICIES`），这里不复述编号与开关。
- **完成定义**：`get_gate_result(region, wave, dataset)` 有本波记录且 `all_pass=1`（门禁脚本崩溃 = ERROR 终态、退出码 2，不是 FAIL）。
- **失败分支**：闸 → 现象 → 动作 → 回哪步 → 能否豁免的全表见 [`step5-gates.md`](references/step5-gates.md) §5.2；开波区域闸命中（exit 2）→ 消化积压 / 补 catalog / 换区，用户显式要求继续才写 waiver。
- **不做**：不新建 `_gate_waveNN.py`、不写 `cache/gate_wave*.json`（用 `wave_gate.py`，结果落 `gate_results`）；不以为 `validate_expressions` / `preflight_expressions` 查了幽灵算子（**不查**）；不把「干跑绿」当「LLM 可达」。
- **细则**：[`step5-gates.md`](references/step5-gates.md)；情景卡 RA-05（体检包缺失）。适用决策表：D1 / D2。

### 步 5b：prod-first 探针（S3 收批后必调；定义只在这里）

- **目的**：在同一信号族投入第二波之前，先知道它撞不撞 prod 墙（IND intraday_pv_feats 连投 3 波 24 条后才查 prod = 0.79–0.92，整族报废）。
- **调用**：`python tools/campaign_intel.py prod-first --region $REGION --wave $W --write-ledger`（族内最强 1 条，平台实测，**串行**；`--top-k` 缺省 3）。闸 PF 是它的代码级固化（骨架级：已知死骨架 → 拦整波，新骨架 → WARN）。
- **产物**：族级 `EXPAND` / `STOP`；`alphas.prod_correlation`；ledger `prod_first_<wave>`。
- **处置**：**只有一张表——决策表 [D0-P](references/decision-table.md)**（< 0.60 扩变体；0.60–0.70 不扩变体、当天进步 8；0.70–0.75 只许 1 次结构性尝试；≥ 0.75 或尝试失败 → dead_end）；数值例见情景卡 RA-04。
- **不做**：**禁止用 `POST /submit` 探测 prod**（通过即提交，无撤回）；prod 一律 `check_correlation`（只读）。总纲见 [`prod-corr-avoidance.md`](references/prod-corr-avoidance.md)。

### 步 6（S3）并发回测

- **目的**：把本波表达式跑成回测行。
- **前置**：步 5 `all_pass=1`；并发参数以 `wqb.config.CONCURRENCY` 与 [`wqb-concurrency`](../wqb-concurrency/SKILL.md) §8 为准（不在本文复写数字）。
- **调用**：`workflow_batch_track region=$REGION wave=$W dataset=$DS`（先过三道开波闸；异步返回 `task_id`，用 `workflow_task_status` 跟踪，**不要 shell 翻日志**）；手写 alpha_list 走 `brain-sim-alphas-in-batch-and-track`；调试用 toolkit `pipeline.py`。
- **产物**：`backtest_results` / `wave_results` 暂定结论 / `salvage_pool`（收批入库即级联；`multisim_id` 写进每条回测行）。
- **完成定义**：本波全部 multisim 到**终态**，且 `backtest_results` 行数 = 波内表达式数（含 ERROR / CANCELLED 的标记行）；整批 CANCELLED → 回步 5。
- **失败分支**：故障表（全 ERROR / 连坐 CANCEL / 429 / 超时）见 [`step6-backtest.md`](references/step6-backtest.md) §6.4：**先归因再决定重发 / 跳过 / 拆批**；确定性 ERROR 重发只会烧配额。
- **不做**：**QUICK 模式产物不可提交**（无 visualization / correlation / theme 检查）——仅作探针，必须 FULL 复测并在 `key_findings` 记 `simulationMode`；不往 pipeline 传非 7 的并发（只收 warning）；`pipeline.py --submit` 是派发仿真，**不是**提交 alpha。
- **细则**：[`step6-backtest.md`](references/step6-backtest.md)。适用决策表：D5 / D8 / D11。

### 步 7（S4）诊断改进

- **目的**：这一波的候选下一步去哪——提交链 / 改进 / 判死。
- **前置**：步 6 完成定义满足；prod-first（步 5b）已跑。
- **调用**：`s4-prescreen`（全灭直接判死）→ `workflow_campaign(stage="S4", dataset=$DS, wave=$W)`（评审；解析不到 alpha_id 即 FAIL，用其列出的字符串波号重试）→ 逐候选链（selfcorr-quick → `check_self_correlation` → `compute_mutual_correlation` → `check_correlation` → `brain-alpha-robustness` → judge）。
- **产物**：ledger `s4_walls_<region>_<wave>`、`salvage_pool`；每条候选有去向。
- **完成定义**：本波每条候选都有去向——进步 8 / 留 near / salvage（带墙名）/ 判死（进步 9）。
- **失败分支**：卡闸 → `get_salvage_pool(boost_dim=…)` 找辅助腿；Mode B 2–3 轮仍卡墙 → 找武器（`forum_recon` 触发表 #4，每波 ≤ 1 次）；同一想法 > 10 种结构仍不过 → 步 9 记 `dead_end`。
- **不做**：**任何两条独立信号腿相加（加权 / 等权 / `add` / 中缀 `+`）一律违规**；辅助腿只能以**条件 / 分组 / 残差**三式入场；`risk_neutralized_sharpe ≤ 0` 且 raw ≥ 1.58 → 停止调参；**门禁通过 ≠ 合规**。IS→OS 衰减折算**不抬高 IS 阈值**。
- **细则**：[`step7-diagnose.md`](references/step7-diagnose.md)（墙与池的判据、组合形态**唯一一份**允许清单、辅助腿入场三式、§7.6.1 提交层四闸与 SUB 比值律）；事故 [`incidents.md`](references/incidents.md) I-1。适用决策表：D0 / D0-P / D1 / D2 / D3 / D12 / D14。

### 步 8（S4→S5）稳健闸与提交判定

- **目的**：决定哪些候选值得请用户确认提交。**本步不执行提交。**
- **前置**：步 7 的候选已过稳健性（[`brain-alpha-robustness`](../brain-alpha-robustness/SKILL.md)，S4→S5 必经；结论写台账 `robustness_<alpha_id>`，`submit_verdict` 读取——`REJECT` → `BLOCKED`，无记录只提示）。
- **调用**（有序检查清单，任一步说「不」就停）：① **资格门** `Failed RA == 0`（`compute_webdata_failed_counts`；名单内仍有 `PENDING` 时 `Failed=0` 只表示「暂无失败」，待其算完再判）② `submit_verdict`（**否决权威**，退出码 `1` BLOCKED / `10` UNVERIFIABLE / `11` ALREADY_SUBMITTED）③ prod 实测 `check_correlation(alpha_id, refresh=True)` < 0.7 ④ **用户明确确认** ⑤ 才可 `workflow_submit_alpha(confirm_submit=True)`（**不可逆**，单独调用；执行与四态响应处置见 [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md)，SUPER 走 `wq-brain-superalpha`，PPA 走 web UI 交接）。
- **产物**：候选清单 + 每条的证据（资格门 / verdict 退出码 / prod 值）交用户。
- **完成定义**：清单已交用户；**用户确认后**提交，`get_alpha_details` → `status == ACTIVE` 且 `dateSubmitted` 非空。
- **失败分支**：PROD / SELF 不过 → 回步 7；配额耗尽（按 **ET 日历日**）→ 挂起提交，继续步 2 → 9。
- **不做**：`UNVERIFIABLE`（现实中最好的结果）**不是放行**；确认前禁止一切**真提交**入口——`workflow_submit_alpha` / `submit_alpha` 节点（`confirm_submit=True`）、`workflow_superalpha`（`confirm_submit=True`）、`super_build.py submit`（`submit_batch` 与 `pipeline.py --submit` 是**派发仿真**，不是提交，别混）；**没有零成本的 POST 探测**；`PASS_CHEAP` 只代表过了 IS 廉价闸，**绝不等于可提交**。
- **同日提交**：prod 0.60–0.70 的候选**当天**请用户确认，不先做变体（IND pv103 `mLm2xG1K` S 3.83、prod 0.6997，先做变体的 1 小时里外部同款把 prod 顶到 1.0000，整族封死）；这**不豁免** robustness，只豁免「同族变体探索」——同族第二颗的变体放在第一颗 ACTIVE 之后。
- **细则**：全链状态机与不可逆动作块见 [`worldquant-submit-alpha/references/submit-chain.md`](../worldquant-submit-alpha/references/submit-chain.md)；**提交前读** [`01_platform_gates.md`](docs/experience/01_platform_gates.md)（四闸 + SUB 比值律：把 sharpe 压到刚过线会同步降低 SUB 要求，「sharpe 越高越好」在提交层是错的；诊断侧见步 7 §7.6.1）；[`ppa-vs-ra.md`](references/ppa-vs-ra.md)；[`webdatascope-failed-gates.md`](references/webdatascope-failed-gates.md)。适用决策表：D1 / D9。

### 步 9（S6）复盘回写

- **目的**：把这一波的结论写回库，让下一波的先验自动变新。
- **前置**：步 7 / 8 已有去向；先跑 `tools/step_funnel.py` 定位掉得最狠的一跳。
- **调用**（**有序**，全流程见 [`step9-writeback.md`](references/step9-writeback.md) §9.1）：① `step_funnel` ② 判 verdict（`PASS` ≥ 1 条过全部评审闸 / `PARTIAL` 0 达标但 ≥ 1 条 near / `FAIL` 0 达标 0 near）③ `campaign_intel.py pyramid` ④ `upsert_wave_result`（key_findings 一次带齐）⑤ 判死 `seal_dead_end`（先取证——收批时 `forum_recon_wave` 已默认问过一次；把 `question_key` 传给它，取证闸 fail-closed，规则见 §9.5）/ 胜绩 `upsert_registry_empirical(layer="win")` ⑥ 全波撞 prod 墙 → `campaign_intel.py mark-saturated` ⑦ 逐数据集 `dataset-experience` ⑧ 再跑一次 `assemble-priors`。
- **产物**：`wave_results.verdict`（**唯一结论源**）、`registry_empirical`、`priors_snapshot_<region>`、`reports/dataset_experience/*_campain.md`。
- **完成定义**：`step9-writeback.md` §9.7 的清单全勾；**缺任何一项 = 本波未完成**（GEM 对 stale 先验快照只 WARN 不阻断，只能由本步兜底）。
- **失败分支**：`upsert_wave_result` 被拒（verdict 不可辨认）→ 用返回的 `suggestion` 核对后显式传枚举，原文进 `key_findings`。
- **不做**：不写 `s6_verdict_<wave>` / `wave<N>_verdict`（已废止，双写会分叉）；不往五张 `step_*` 表写（恒 0 行）；**未选、未回测不能写成 dead_end**；不在 win 里记混合比例。
- **细则**：[`step9-writeback.md`](references/step9-writeback.md)；情景卡 RA-06（判死粒度）。适用决策表：D1 / D9。

## 循环与停止

**一波 = 步 2 → 步 9。** 开波前有四道自动闸（catalog 前置 / signal_floor / stop_rules / backlog；零配额、干跑也走）；命中即拒绝开波并给出放行写法（waiver）。
**用户显式要求继续**才写 waiver（`stop_rules` / `backlog` 只有用户能批，≤ 30 天，`expires_at` 必填），**不要**靠 `--gate-mode warn` 绕过。规则、缺省数字、数字例、放行协议、转向路由（SuperAlpha / 配额耗尽 / 日循环）全在 [`loop-and-stop.md`](references/loop-and-stop.md)。

## 整链执行（可选）

`mcp__wq-brain-http__workflow_chain`（**先 `dry_run=true`**）可串 `campaign` / `gem` / `wave_gate` / `batch_track` 等节点；**干跑只验命令链能构建，不证明 LLM 可达、配额可用、平台鉴权有效**。**提交类节点不入链——由代码强制**：`submit_alpha` / `superalpha` 带 `confirm_submit=True` 出现在链里，`execute_chain` 整链拒绝。步 → 节点表、异步 join、自动插入 `wave_gate` 见 [`tool-index.md`](references/tool-index.md) T.2；工具 / 节点**总数**以 [INDEX.md「MCP 工具/节点计数基准」](../INDEX.md)为准（这里不裸写数字）。

## PPA 分支

仅当**当期 Power Pool 主题匹配** region / delay / universe 时挖 PPA（步 1 实时重扫公告，禁止复用 settings 快照）；不匹配走 RA。同一条九步，只在步 1 / 2 / 4 / 7 / 8 有差异，配额是**独立通道**（`POWER_POOL_SUBMISSION` 1 / ET 日，不占 REGULAR 4 / 日）；**PPA 提交渠道有限制**（MCP 预检不够时 agent 停下交接，用户在 web UI 提交）。逐步差异表见 [`ppa-vs-ra.md`](references/ppa-vs-ra.md)。

## Artifact 契约

**战役产物（事实源）只入 `data/wqb.db`，禁止 Write 战役 json / csv。** 一次性中间文件（`cache/candidates.json`、`cache/basket.json`、`--exprs-file <txt>`、`--json <out>`）可写但**可丢弃、不作事实源**。ledger 键的用途 / 写入方 / 读取方 / 缺失行为 → `docs/ledger_keys.json`（测试守）。

| 阶段 | 入库 | 唯一写入方 |
|---|---|---|
| S0 | ledger `s0_ranking` / `s0_whitelist` / `s0_calibrate_<region>` / `*_dead` | `score_datasets.py`（toolkit）；手工锁白名单 `upsert_ledger_key(mode="merge")` |
| S1 | ledger `catalog_<ds>` / `s1_prefix_<ds>` / `s1_semantic_<ds>`；`fields` 表 | `workflow_campaign(S1)`；`field_semantic_classify.py`；字段目录 `upsert_field_catalog` |
| S2 | `expressions`（status `gem` / `enhanced` / `selected`）；ledger idea；`priors_snapshot_<region>` | `workflow_gem` 落库 + `assemble-priors`；直写 `upsert_expressions` |
| S2→S3 | `gate_results`（`all_pass` / `fail_reasons`） | `wave_gate` / `gate.py`；直写 `upsert_gate_result` |
| S3 | `backtest_results` / `wave_results` / checkpoint；ledger `prod_first_<wave>` | `pipeline.py`（toolkit）；收割 `harvest_multisim_alphas` + `harvest_multisim_results` |
| S4 | ledger `s4_walls_<region>_<wave>`（`workflow_campaign` S4 节点写）或 `review_<tag>`（`review_wave.py --write-ledger` CLI 写）；`salvage_pool` | `review_wave.py`；补池 `backfill_salvage_pool` |
| S6 | `wave_results.verdict`（唯一结论源）+ `registry_empirical` + ledger `saturated_datasets`；`reports/dataset_experience/*_campain.md`（每个回测过的数据集一份；本波涉及的由步 9 ⑦ 逐个刷新，**不是只对判死 / win 集生成**） | `upsert_wave_result` / `seal_dead_end` / `upsert_registry_empirical` / `mark-saturated` / `dataset-experience` |

## 反模式（每条：因 X 发生过 Y → 改用 Z）

- 再 invoke `brain-deepExplore` 或按其旧 S2-D / S2-M 必跑、停止闸 4 覆盖 RA——该 skill 已废止 → 走步 4。
- 手写 `_gate_waveNN.py` / `w*_batches.json` / 把 GEM `final_expressions.json` 当真相源 → 用 `wave_gate.py`，结果落 `gate_results`。
- 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填波 → 概念优先 + priors。
- **QUICK 产物进步 7 / 8**：缺 correlation / theme 检查却被当通过 → 必须 FULL 复测。
- **确认前 POST /submit「探一下」**：通过即提交，无撤回 → 预检用 `confirm_submit=False`，prod 用 `check_correlation`。
- **`--skip-semantic-gate` 无留痕**：整波退化为货币 / 汇率叉乘（KOR fundamental17 首波 49.4%）→ 先跑 classify；确需跳过写 `semantic` waiver。
- **双写已废止的 `s6_verdict_<wave>`**：结论分叉、停止规则 B 失灵 → 只写 `wave_results.verdict`。
- **把 LLM 402 下的干跑绿当可运行**：GEM 报「no meta.json」→ 先查 LLM 通道。
- `submit_verdict` 通过后自动 `workflow_submit_alpha`；调用已废弃的 `glb_pipeline` / `gbr_pipeline` / `glb_alpha_machine`；把 `brain-feature-implementation` 当主链入口（它在 GEM 内部）；手写 PowerShell 替代 MCP 调用；手写 requests；跳过步 9；`combination(alpha(...))`。
- 更多事故与起因：[`references/incidents.md`](references/incidents.md)。
