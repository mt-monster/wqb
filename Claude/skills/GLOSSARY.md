# 术语与词表（跨 skill 共用）

> **用途**：skill 文本里**同一个词只许一种含义**。这里登记本库采用的词、弃用的别名、以及「唯一实现」的宣称（谁说了算、在哪、哪个测试守）。
> 新 skill / 新段落用这里的词；发现别名 → 改文，不要在别处另立定义。
> **代码可导出的内容不在这里抄**：闸表与逃生口总表在 [`INDEX.md`](INDEX.md)（由代码生成）、阈值在 `src/wqb/config.py`、
> ledger 键在 `docs/ledger_keys.json`（仓库根相对路径，下同）、放行协议在 `AGENTS.md` §8.1.2。
> 来源：`reports/skills_review_20260929.md` 的 X-2 / X-4 / X-5 / X-6 / X-7。

## 1. 术语表

| 词 | 本库采用的含义 | 弃用 / 易混的说法 | 定义所在 |
|---|---|---|---|
| **并发令牌** `sim_token` | 平台同时在飞的仿真上限（Token-Bucket，`slots=7`，安全瞬时 ≤6） | 裸写「槽」 | `config.CONCURRENCY` |
| **波内配额** `wave_quota` | 一波里表达式要满足的配比（如「跨金字塔 ≥2 条」） | 裸写「槽」「七槽」 | `config.MINING`；ra-pipeline 决策表 D8 |
| **批** | 一次 multisimulation（8 条子模拟；一轮 7 批同提） | 「槽」 | wqb-concurrency |
| **dispatch（派发）** | 把表达式派去仿真：`POST /simulations`（`tools/submit_batch.py`、MCP `submit_batch` / `create_multi_simulation`） | 「批量提交」「submit」 | brain-sim-alphas-in-batch-and-track |
| **submit（提交）** | 把**已存在**的 alpha 提交上平台：`POST /alphas/{id}/submit`（`workflow_submit_alpha(confirm_submit=True)`、`super_build.py submit`）——**不可逆** | 把 dispatch 也叫「提交」 | worldquant-submit-alpha [`submit-chain.md`](worldquant-submit-alpha/references/submit-chain.md) |
| **提交层信息** | `POST /submit` 响应里的 checks。`GET /alphas/{id}/submit` 在本平台恒 404，**不是**信息来源 | 「提交层视图」（指 GET 的那个） | submit-chain.md §3 |
| **corr_slot** | 相关性计算的账号级单并发；忙时立即返回 `correlation_busy` | 「配额」 | `config.WAIT_THRESHOLDS` |
| **submit_quota** | 每个 **ET 日历日**：REGULAR 4 + SUPER 1 + PPA 1（三者并行不互占） | 「周额度」（已废止）、48h / 24h 滚动 | `wqb.timeutil`、`tools/quota_status.py` |
| **信号族（family）** | 表达式引用的**字段集合**（去算子 / 常数），如 `snt21_pos_mean+snt21_pos_max`——prod-first 探针的分组单位（每族只探最强 1 条）；`dead_end` 记录里的 `family` 是人给的族名 | 与「骨架」混用 | `tools/campaign_intel.py::_pf_family` |
| **骨架指纹（skeleton）** | 表达式里**前 2 个算子调用名**（如 `rank→ts_backfill`）——闸 PF 的判据，也是 ledger `prod_family_<region>_<family>` 键里的那个 family。比字段更准：同字段换骨架，prod 由 0.76–0.82 降到 0.46–0.57（`mdl135_d01_icc` 实证） | 叫成「信号族」 | `tools/wave_gate.py::_pf_family` |
| **meets_internal_line** | Sharpe>1.58 且 Fitness>1.0（停止规则 A 的「达标」） | 裸写「达标」 | `config.GATES_PLATFORM` |
| **ra_clean** | `is.checks` 里 RA 18 项没有任何非 PASS/PENDING（Failed RA = 0） | 裸写「达标」「零硬闸失败」 | `config.compute_webdata_failed_counts` |
| **review_passed** | 评审闸全过，波结论 `PASS` | 「GREEN 波」 | `wave_results.verdict` |
| **ATOM alpha** | 只用**单一数据集**字段的 alpha（允许的分组字段除外），享受放宽的提交口径（以近 2 年 Sharpe 为准） | 把「ATOM 提交口径」与 judge 的 `SINGLE_DATA_SET` 标签当两件事 | brain-how-to-pass-alpha-test `reference.md`；放宽的具体阈值**只引用官方表**，不在别处写数字 |
| **FAIL / PENDING / WARNING** | `FAIL` 挡；`PENDING` = 结果未出，**不据此判死也不据此放行**；`WARNING` 见 §2.4 | 一个词三种范围 | §2.4 |
| **判死（按粒度）** | 候选=淘汰；字段搭配=禁配；**家族=`dead_end`（范围 = region × 信号族名）**；数据集=`<ds>_dead` 台账键；波=`FAIL` | 「判死」不带粒度 | registry / ledger-keys |
| **否决权威 / 放行权威** | 否决权威**只能拦不能放**（`submit_verdict`、Failed-count 门、prod 实测）；放行权威 = **用户明确确认 + `confirm_submit=True` 的 POST**（不可逆） | 「唯一权威」 | submit-chain.md §1 |
| **IS 衰减比 / IS→OS 衰减** | 前者 = IS 内部 `last_year/full_period`；后者 = 提交后平台 OS 相对 IS 的衰减 | 都叫「衰减比」 | brain-alpha-robustness |
| **内部严线 / 平台线** | 内部严线 = 研究阶段省配额的本地预筛（`GATES_INTERNAL`）；平台线 = 提交阶段平台检查的官方线（`PLATFORM_CHECK_LINES`、`GATES_PLATFORM`）。**Sharpe 有三条不同的线，别互相顶替**：LOW_SHARPE 1.25（D1）、LOW_2Y_SHARPE 1.58、内部 1.58 | 「合格线」不带层 | `src/wqb/config.py` |
| **编号体系** | `Ln ≡ Sn`（阶段，L0–L6 = S0–S6）；「步」= ra-pipeline 的 9 步；「闸」= gate.py 闸 0–9（wave_gate 另有 SEM / PF / 体检等，见 INDEX 总表）；「关」= wq-backtest-monitor 的检查点 | 混用 L / S / 步 / 闸 / 关 | INDEX |

## 2. 状态词表（分层）

> 原则：**一层一套词**；颜色只用于 alpha 提交标签，不用于任何 verdict。跨层路由必须写清「读哪个字段 / 哪个退出码」。

### 2.1 alpha 级（一颗候选此刻能不能往下走）

| 系统 | 取值 | 谁产出 | 路由怎么读 |
|---|---|---|---|
| `submit_verdict` | `SUBMITTABLE` / `UNVERIFIABLE` / `BLOCKED` / `ALREADY_SUBMITTED`（退出码 0 / 10 / 1 / 11） | `wqb.submit_verdict_core.decide` | **看退出码**。`SUBMITTABLE` 现实中不会出现（依赖恒 404 的 GET）；`UNVERIFIABLE` = 模拟层干净但提交层无信息 → 仍须 prod 实测 + 用户确认，**不是放行** |
| judge / `workflow_judge` | `READY` / `REVIEW` / `BLOCK` | `judge_alpha.py`（参考评审） | 只作排序 / 参考；**不放行**。路由条件里的「READY」指 judge 或 s4-prescreen，不是 `submit_verdict` |
| `s4-prescreen` | `READY` / `REVIEW` / `REJECT` | `campaign_intel.py s4-prescreen` | S4 预筛压缩 |
| robustness | `PASS` / `CONDITIONAL` / `REJECT` | brain-alpha-robustness | 稳健性闸（判定写台账 `robustness_<alpha_id>`，`submit_verdict` 读取：REJECT → BLOCKED，CONDITIONAL / 无记录只提示） |

### 2.2 波级

`wave_results.verdict` ∈ **`PASS` / `PARTIAL` / `FAIL`**（`wqb.wave_results_contract.VERDICT_OK`；旧写法 `GREEN:` / `RED:` / `全灭` 读取时归一）。
`status` ∈ `open` / `closed`。**波结论不用颜色词。**

### 2.3 区域级 / 家族级

| 系统 | 取值 | 出处 |
|---|---|---|
| `entry_verdict`（区域 profile front-matter） | `active` / `probe-only` / `frozen` | ra-pipeline `references/regions/*.md`；`region_rotation.py`、`region_status.py` 读取 |
| prod-first 族级建议 | `EXPAND` / `STOP` | `campaign_intel.py prod-first` |
| hypothesis-first 假设状态 | `rejected` / `partially_supported` / `supported` / `needs_refinement`（**dormant**，见该 skill） | brain-alpha-research-hypothesis-first |

### 2.4 检查结果词（`is.checks[].result`）

- **`FAIL`**：挡。
- **`PENDING`**：结果未出（如 SELF / PROD 相关性未算完）。**不挡提交，但也不能据此放行**——放行须 prod 实测 <0.7。
- **`WARNING`** 分两类：
  - **硬闸类**：检查名 ∈ `config.RA_CHECK_NAMES`（RA 18 项）或 `PPA_CHECK_NAMES`（7 项）→ 资格门里**计入失败**（`check_counts_as_failed`：非 PASS 且非 PENDING）；
    其中 `LOW_FITNESS` / `LOW_SHARPE` / `LOW_2Y_SHARPE` 在提交层被平台重新评估为 FAIL（`SUBMIT_HARD_GATE_WARNINGS`，KOR PPA 2026-08-22 实锤）。
  - **提示类**：其余（描述长度 / 格式 / 主题…）不挡。
- 名单以代码为准：`wqb.config.RA_CHECK_NAMES` / `PPA_CHECK_NAMES`、`wqb.submit_verdict_core.SUBMIT_HARD_GATE_WARNINGS`。

### 2.5 基础设施 / 轮询状态（不是 verdict）

`POST /submit` 四态（200 明确通过 / 201·202 异步受理 / 200 空体 / 403 失败）、`STALLED` / `TIMEOUT`（在飞回测卡住，`WAIT_THRESHOLDS.sim_*`）、
`ASYNC_STUCK`（提交后窗口内未翻转且已补发）、`correlation_busy`（相关性单并发忙）。见 submit-chain.md §4。

### 2.6 颜色（**只用于 alpha 提交标签**）

`GREEN` / `BLUE` / `RED` / `YELLOW` / `PURPLE`（平台只接受这 5 个值）。提交态默认 `BLUE`（待观察）；`GREEN` 须由 OS 结果挣得；`PURPLE` 仅 PPA 通道。
规范与校验 = `src/wqb/alpha_properties.py`（`docs/alpha_properties_spec.md`）。**波结论、区域状态、评审灯都不再用颜色词。**

## 3. 「唯一」宣称登记表

> 「唯一权威 / 唯一事实源 / 唯一入口 / 唯一真相源」这类宣称**只在本表登记**：每条对应一个实现位置和一个守它的测试。
> 别处想说「以 X 为准」，写「见 X」并链接本表的行；不要再自称唯一。`tests/unit/07_docs_skills/test_glossary_docs.py` 检查本表的路径与测试真实存在，
> 并对 SKILL.md 里的「唯一…」措辞做**只减不增**的棘轮（`tests/fixtures/authority_claims_baseline.json`）。

| 宣称 | 唯一实现 | 守护测试 |
|---|---|---|
| gate.py 闸编号与闸表 | `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py`（`GATE_REGISTRY`）→ INDEX 由代码生成 | `tests/unit/04_gates/test_gate_registry_docs.py` |
| 闸与逃生口总表 / waiver 协议 | `src/wqb/waiver.py`（`GATE_POLICIES`）→ INDEX switch-table | `tests/unit/09_core/test_waiver.py` |
| 提交层判定（**否决权威**） | `src/wqb/submit_verdict_core.py::decide`（CLI / MCP / 批量共用） | `tests/unit/05_submit_quota/test_submit_verdict_core.py` |
| RA / PPA Failed-count 口径 | `src/wqb/config.py::compute_webdata_failed_counts` | `tests/unit/05_submit_quota/test_r3_failed_count_single_source.py` |
| 平台线 / 内部线 / 提交准入线 | `src/wqb/config.py`（`PLATFORM_CHECK_LINES`、`GATES_INTERNAL`、`GATES_PLATFORM`） | `tests/unit/01_store_db/test_threshold_relations.py` |
| 等待 / 退避 / 卡住阈值 | `src/wqb/config.py::WAIT_THRESHOLDS` | `tests/unit/07_docs_skills/test_wait_thresholds.py` |
| ET 日历日与提交配额口径 | `src/wqb/timeutil.py`、`tools/quota_status.py` | `tests/unit/09_core/test_timeutil.py`、`tests/unit/05_submit_quota/test_quota_et_day.py` |
| 波结论（verdict）写入与枚举 | `src/wqb/wave_results_contract.py` | `tests/unit/01_store_db/test_n30_wave_results_writers.py` |
| ledger 键（用途 / 写入方 / 读取方） | `docs/ledger_keys.json` | `tests/unit/01_store_db/test_ledger_key_catalog.py` |
| `s0_whitelist` 读取契约 | `src/wqb/ledger_whitelist.py` | `tests/unit/01_store_db/test_ledger_whitelist_schema_p0p4.py` |
| 时间炸弹（到期 / 翻转） | `docs/time_bombs.json` | `tests/unit/09_core/test_time_bombs.py` |
| skill 文档「内容为真」检查 | `tools/skill_lint.py`（基线 `tests/fixtures/skill_lint_baseline.json`） | `tests/unit/07_docs_skills/test_skill_lint.py` |
| 幽灵算子清单 | `src/wqb/config.py::GHOST_OPERATORS`（∪ `platform_constraints.ghost_ops`，减去账号不可用者） | `tests/unit/09_core/test_ghost_operator_lists.py` |
| 区域清单 | `src/wqb/config.py::REGIONS` | `tests/unit/07_docs_skills/test_docs_consistency.py` |
| MCP 工具 / 节点计数 | INDEX「MCP 工具/节点计数」段 | `tests/unit/07_docs_skills/test_docs_consistency.py` |
| 提交链默认值（不可逆动作默认不执行、颜色缺省不是 GREEN） | `world-quant-brain-mcp/tools_workflow.py`、`src/wqb/workflow/nodes/submit_alpha.py` | `tests/unit/05_submit_quota/test_submit_chain_defaults.py` |
| alpha 属性（name / color / tags） | `src/wqb/alpha_properties.py` | `tests/unit/02_workflow/test_alpha_properties_patch_partial.py` |
