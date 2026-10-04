---
last_verified: 2026-10-04
name: wq-brain-campaign-toolkit
description: "战役目录内执行引擎（gate / pipeline / build_wave / score_datasets / review_wave / campaign.py 的 ledger·registry·wave）的用法与契约。要跑战役脚本、查子命令与台账键、处理超时或重发时使用；何时用、怎么判由 wq-brain-ra-pipeline 定。"
layer: L-TOOL
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__wqb-db__get_wave_result
  - mcp__wqb-db__list_wave_results
  - mcp__wqb-db__get_latest_wave
  - mcp__wqb-db__get_ledger_key
  - mcp__wqb-db__list_ledger_keys
  - mcp__wqb-db__get_submit_ready
---

# wq-brain-campaign-toolkit（战役引擎层）

## 职责边界

- **本 skill 负责**：战役目录（`tracking/<REGION>/`）内**执行引擎的用法与契约**——`scripts/` 下各脚本与 `campaign.py` 子命令的参数、写入矩阵、重发安全与异步恢复规则，以及闸门 / 探针 / 配额 / 台账的细则（`references/`）。
- **本 skill 不做**：不做区域选择（`wq-brain-campaign-matrix` / `brain-next-move-analysis`）；不做提交判定（`tools/submit_verdict.py`）、不直接提交 alpha；**不定义「何时用、怎么判、用什么阈值」**（那是 `wq-brain-ra-pipeline` 与各方法论 skill）；**不是任何表的「唯一写入方」**——`wave_results` / `registry_empirical` / `ledger_kv` 各有多个入口，见 §3 写入矩阵。
- **上游 / 下游**：上游 = `wq-brain-ra-pipeline`（编排）、`brain-sim-alphas-in-batch-and-track`（S3 主要调用方）以及以子进程调用本引擎的 workflow 节点（`workflow_campaign` / `workflow_batch_track`）；下游 = `data/wqb.db` 各表与 ledger 键（键契约见 `docs/ledger_keys.json`）。

## 1. 定位与分工

三角分工：`wq-brain-ra-pipeline` = when / what；`wq-brain-campaign-matrix` = where（给定区域后查表）；**本 skill = how（战役目录内怎么执行）**。所有脚本用 MCP venv：`$WQ_PY`；引擎脚本为标准库实现（仅闸 1 需要 `alpha-expression-verifier`，经 `WQ_VALIDATOR_DIR` 探测）。

**toolkit（`scripts/`）与仓库 `tools/` 的分工**——同一阶段常常两边各有一步，别在 toolkit 里复制 `tools/` 的逻辑，也别反过来：

| 阶段 | toolkit `scripts/` | 仓库 `tools/` |
|---|---|---|
| S0 选集 | `score_datasets.py`（评分 / 探针计划 / 三灯） | `campaign_intel.py s0-select`（默认剔已点亮塔）、`region_status.py`、`field_inspect_gate.py`（体检硬门） |
| S1 字段 | `scan_fields.py`（typed catalog） | `field_semantic_classify.py`（语义归类） |
| S2 选波 | `build_wave.py`（去重 / 分桶 / 配给，**不生成**表达式）、`assemble_priors.py`、`diversity_extract.py` | — |
| S2→S3 门禁 | `gate.py`（闸 0–9） | **`wave_gate.py`**（= `gate.py` + 体检硬门 + 闸 SEM / PF / 2b / 2.6 + 区域闸；**每波必走它**，也是 MCP 节点 `workflow_execute node="wave_gate"`） |
| S3 发批 / 收批 | `pipeline.py`（七槽填槽）、`metrics_cache.py` | `submit_batch.py`（批量**派发仿真**，不是提交 alpha）、`batch_status.py`（状态轮询）、`harvest_multisim.py`（收批入库） |
| S4 评审 | `review_wave.py` | `campaign_intel.py prod-first`、`step_funnel.py`、`forum_recon.py`（收批时 `pipeline.py --forum-recon` 自动跑 `forum_recon_wave.py`） |
| S5 提交判定 | — | `submit_verdict.py`（唯一权威）；SUPER 只走 `super_build.py` |
| S6 回写 | `campaign.py ledger` / `registry` / `wave`、`diversity_audit.py`、`dataset_experience`（`campaign.py dataset-experience`） | `campaign_intel.py mark-saturated`、`export_wave_ledger_md.py`、`step_funnel.py` |

工具索引与参数见 `tools/README.md`；缺参数就改工具（保持 `--help` 自文档），反复新建一次性脚本说明工具化不彻底（AGENTS.md §6）。

## 2. 环境与调用约定

1. 所有脚本统一 `--campaign-dir <路径>`（缺省 = 当前工作目录）。
2. **region 只从 `config/settings.json` 的 `region` 派生**，并校验与战役目录名一致（不一致即报错；测试可用 `CAMPAIGN_SKIP_DIR_CHECK=1`）。禁止从目录名或命令行猜。
3. **凭据**：脚本自己按 `CREDENTIALS_EMAIL/PASSWORD` → `WQ_USERNAME/WQ_PASSWORD` → `BRAIN_CREDENTIALS`（JSON 路径）/ `~/.brain_credentials` → `MCP_CONFIG_FILE` / `~/.brain_mcp_config.json` 的顺序读取。**agent 不得读取、打印这些文件或 `world-quant-brain-mcp/.env`**（AGENTS.md 红线），也不把凭据写进命令行。
4. 平台级约束只有一份：`config/platform_constraints.json`；区域 ranking / catalog / rules 计数入库。
5. **Agent 持久化只走 `mcp__wqb-db__*` 或本引擎 CLI，禁止 Write / Copy 战役 json / csv**；`build_wave` / `gate` / `wave_gate` / `pipeline` 走 `--from-db`。
6. **开波区域闸的模式**（`build_wave.py` / `tools/wave_gate.py` 开波前跑 catalog / signal_floor / stop_rules / backlog）：

| 入口 | 缺省 | 命中时 |
|---|---|---|
| 命令行 `--gate-mode` > 环境变量 `WQB_GATE_MODE` > 按日期缺省 | **2026-10-11 及以前 warn（只告警）；2026-10-12 起 enforce**（日期唯一事实源 `_lib/region_gates.WARN_SUNSET`，每次运行第一行打印模式来源与倒计时） | enforce：exit 2，本波不产出门禁结论（不是表达式问题） |
| workflow 节点（campaign S2 / S3、batch_track） | 不看这个模式，**一律 enforce** | 同上 |

放行停波区域写台账 `stop_rules_override` 留痕；`--gate-mode warn` 只作临时回退。

## 3. 写入矩阵（谁能写哪张表）

| 表 / 键 | 校验的唯一实现 | 入口（同一份契约） | 适用 |
|---|---|---|---|
| `wave_results` | `wqb.wave_results_contract.upsert_wave_result` | MCP `upsert_wave_result`（会话内首选）· `campaign.py wave upsert / import`（无 MCP、批量）· 引擎收批 / 评审（`pipeline.py`、`review_wave.py`、`harvest_multisim`） | 逐波结论，RA 步 9 |
| `registry_empirical` | `wqb.registry_contract` | MCP `seal_dead_end` / `upsert_registry_empirical` · `campaign.py registry …` | 跨会话结论，schema 见 matrix §4 |
| `ledger_kv` | 键契约 `docs/ledger_keys.json` | MCP `upsert_ledger_key`（merge / replace / append；**共享键禁 replace**）· `campaign.py ledger set`（整值覆盖）· 引擎脚本（按各键的写入方） | 战役台账 |
| SQL 表 `submit_ready` | `wqb.store.submit_queue` | S3 收批（harvest 钩子）自动入队、提交后自动退役；`tools/submit_queue.py` | **提交队列的唯一事实源**（MCP `get_submit_ready` 读它；ledger 同名键只是 legacy 审计副本） |

会话内轻量回写用 MCP，无 MCP / 批量用 CLI，两者写同一张表、同一份校验，任选其一，不要两边各写一遍。

## 4. 战役目录契约

`tracking/<REGION>/config/settings.json`（仿真设置 + `_multi_sim_batch_size`）与 `config/thresholds.json`（阈值）**必需**；`reference/` 存 typed catalog 与区域生成约束。区域没有目录或缺 `thresholds.json` 时的行为、完整 schema、每个文件的 必需 / 可选 / 历史 标记见 [`references/campaign-dir-contract.md`](references/campaign-dir-contract.md)。

## 5. 典型流程（PowerShell；`$TK` = `$WQ_TOOLKIT_DIR`）

```powershell
$CD = "tracking/<REGION>"
# S0：评分前先校准——先 dry-run 人工审（甜区 ac 是否异常巨大 / strong_acs 是否空），确认无异常再写
& $WQ_PY "$TK/score_datasets.py" --campaign-dir $CD --calibrate --dry-run
& $WQ_PY "$TK/score_datasets.py" --campaign-dir $CD --calibrate
& $WQ_PY "$TK/score_datasets.py" --campaign-dir $CD
# S1
& $WQ_PY "$TK/scan_fields.py" --campaign-dir $CD --dataset <ds>
& $WQ_PY "$TK/score_datasets.py" --campaign-dir $CD --probe-plan <ds> --fields 6
# S2（表达式由 brain-make-some-gem 生成入库；这里只做选波后处理）
& $WQ_PY "$TK/build_wave.py" --campaign-dir $CD --from-db --dataset <ds> --wave <W>
# 门禁：每波走 tools/wave_gate.py（含体检硬门 / 闸 SEM / PF / 2b），见 ra-pipeline 步 5；下面只是 toolkit 内的 gate.py
& $WQ_PY "$TK/gate.py" --campaign-dir $CD --dataset <ds> --from-db --wave <W>
# S3：先看计划（不带 --submit 只打印计划），再 --dry-run 校验，最后 --submit（= 发起回测，不是提交 alpha）
& $WQ_PY "$TK/pipeline.py" --campaign-dir $CD run --dataset <ds> --wave <W> --dry-run
& $WQ_PY "$TK/pipeline.py" --campaign-dir $CD run --dataset <ds> --wave <W> --submit --review --write-ledger
# S4 / S6
& $WQ_PY "$TK/review_wave.py" --campaign-dir $CD --multisim <id> --tag <W> --write-ledger
& $WQ_PY "$TK/diversity_audit.py" --campaign-dir $CD
& $WQ_PY "$TK/pipeline.py" --campaign-dir $CD quota
```

`--max-rounds N` 启用多轮即收即补（缺省 1 = 单轮全提全收）；`--serial` 一次只提 1 批（排障用）。**术语固定**：发起回测 = **dispatch**（消耗仿真并发槽位），提交 alpha = **submit**（消耗 ET 日提交额度）。`pipeline.py` 没有任何提交 alpha 的动作。

## 6. 子命令一览

`campaign.py --campaign-dir <DIR> <子命令> …`：

| 子命令 | 转发到 | 职责 |
|---|---|---|
| `scan-fields` | `scan_fields.py` | typed catalog 字段扫描（`--dataset` / `--limit` / `--zero-comp`）；**过滤必须是 `dataset.id=`**，裸 `dataset=` 会被平台静默忽略 |
| `score` | `score_datasets.py` | 数据集评分 / `--probe-plan` / `--probe-score`（三灯）/ `--calibrate`，细则 [`probe-scoring-v2.md`](references/probe-scoring-v2.md) |
| `gate` | `gate.py` | **8 闸 + 可选闸0**（子闸 1b / 2b / 2b-2，附加闸 9）；闸表由代码生成（`gate.py --print-gate-table`，INDEX 已收录），细则 [`gate-rules.md`](references/gate-rules.md) |
| `build-wave` | `build_wave.py` | 选波后处理（去重 / 分桶 / 骨架配给 / near 加权 / 选波权威化）；数量与身份契约见 [`selection-plan.md`](references/selection-plan.md) |
| `assemble-priors` | `assemble_priors.py` | 从 DB 确定性组装 GEM priors（内部映射见 RA `assemble-priors-internals.md`）；**回写后必须再跑** |
| `pipeline` | `pipeline.py` | 端到端编排（七槽填槽）与 `quota`，细则 [`poll-and-quota.md`](references/poll-and-quota.md) |
| `review` | `review_wave.py` | walls 诊断 + 台账回写 |
| `dataset-experience` | `dataset_experience.py` | 数据集 / 字段经验 Markdown（保留人工复盘段），方法见 `brain-dataset-mining-experience` |
| `metrics` | `metrics_cache.py` | alpha IS 指标读穿缓存（`--multisim=<id>` / `--refresh`） |
| `diversity` | `diversity_audit.py` | 多样性审计（累积进台账 `diversity_history`） |
| `diversity-extract` | `diversity_extract.py` | 单数据集多样性榨取，见 [`diversity-extract.md`](references/diversity-extract.md) |
| `s2-mark` | `s2_compliance_mark.py` | S2 合规标记：**可选**记录，缺记录只打印提示、不阻断（`pipeline.py` 对它不再 `--force`） |
| `ledger` | `_lib/ledger.py` | 台账 CLI：`keys / get / set / mark-dead / add-wave / submit-ready / backup`；`set-verdict` 与 `submit-ready` 已废止（见 [`ledger-schema.md`](references/ledger-schema.md)） |
| `registry` | `_lib/registry.py` | registry 幂等 CLI：`add-dead-end / add-win / upsert-campaign / add-orphan / list / get`（必填参数见 matrix §4） |
| `wave` | `_lib/wave_results.py` | `wave_results` CLI：`upsert / import / get / list`（`--verdict` 只收 PASS / FAIL / PARTIAL；`--finding` 可重复） |

不经 `campaign.py` 的独立脚本：`harvest.py`（兼容：把 multisim 子仿真指标收割到 `results/<ms>_metrics.json` 文件；**DB 收批用 `tools/harvest_multisim.py` / MCP `harvest_multisim_results`**）、`check_ledger_sync.py`（文件时代校验，见 [`ledger-schema.md`](references/ledger-schema.md)）、`neutralization_sweep.py`（生成设置对照批的 alpha_list，兼容产物）。

**已归档**（不要再调用，`scripts/` 里已无这些文件）：`distill_experience` / `os_feedback` / `family_atlas` / `budget_planner` / `campaign_mutex` / `signal_classifier` / `composition_validator` → `attic/toolkit_zero_ref_20260928/`；`migrate_templates` / `compose_signals` / `param_opt` / `ortho_prescreen` / `proxy_prescreen` / `rescue_checklist` / `calibrate_probe` / `fit_mix_weights` / `build_mix` / `adhoc` / `param_matrix` / `diversity_slots` / `composition_templates` → `attic/tools_archive_20260831/`；`references/enhancement-v2.md`、`S2_COMPLIANCE_*`、`DIVERSITY_EXTRACT_*`（描述的正是这些已归档或已撤回的机制）→ `attic/toolkit_docs_20260929/`。需要旧逻辑去 attic 取，先补调用方与测试再启用。

**产物契约（脚本 → DB 落点；DB 是唯一战役真相源，静态配置 `settings.json` / `thresholds.json` / `platform_constraints.json` 仍是文件）：**

| 入口 | 落点 |
|---|---|
| `scan_fields.py` | `fields` 表（typed catalog）；缓存 `catalog_<ds>` |
| `score_datasets.py` | ledger `s0_ranking`；`--calibrate` → `thresholds.dataset_health` + `dataset_empirical_prior`；`--mark-dead` → `<ds>_dead`。白名单 `s0_whitelist` 由 agent 用 **merge** 写入 |
| S1 台账 | `campaign.py ledger set "s1_<ds>_d<delay>"` / MCP `upsert_ledger_key` |
| `diversity_extract.py` | ledger `diversity_<ds>` / `diversity_matrix_<ds>` / `diversity_evaluation_<ds>` + `expressions` |
| `build_wave.py --from-db` | `expressions`（`selected` / `superseded`）+ ledger `wave_meta_<wave>` |
| `gate.py --from-db` | `gate_results` 表 + ledger `gate_cache_<ds>` / `gate_w<wave>_<ds>` |
| `pipeline.py` | `backtest_results` 表、ledger `ckpt_w<W>`（checkpoint）、`wave_results`（`--review` 时）、`region_kb` 的波后刷新 |
| `review_wave.py --write-ledger` | ledger `review_<tag>` / `near_pool` / `salvage_pool`（另在 `submit_ready` 键留 legacy 审计副本）；`workflow_campaign` S4 **节点**路径另写 `s4_walls_<region>_<wave>`（审计） |
| `diversity_audit.py` | ledger `diversity_audit_latest` / `diversity_history` |
| `methodology_rules` 区域计数 | ledger_kv（全局规则仍用 toolkit `config/methodology_rules.json`） |

## 7. 重发安全与异步恢复（最容易被略过的规则）

MCP 桥接超时会返回 `outcome_unknown` 且 `retry_safe=false`：**服务端可能已经收下这批**。此时**禁止盲目重发**（同一批会变成孤儿模拟占槽，也可能重复回测）。恢复顺序：

1. `mcp__wq-brain-http__workflow_task_status`（任务查询会核对进程创建时间与可执行文件；PID 身份不符或无法核实时返回 `unknown`，以明确退出码 / 成功标记优先判终态；旧目录任务缺终态时的历史日志推断**不能代替** DB 收批核验）；
2. 按 `multisim_id` 查 `backtest_results`（`mcp__wqb-db__*` 或 `tools/step_funnel.py --wave`）；
3. **两处都空且任务确已死亡**，才允许重发；重发前先过一遍 `tools/expr_lint.py` / `wave_gate`，避免坏式连坐。

RA 步 6 的「超时恢复清单」指向本节。救援池的来源排除是另一件事：`exclude_dataset` 依据同区域同 alpha_id 的回测 / 表达式来源排除，未知来源不作跨集腿；**数据集不同只证明来源不同，不证明 Prod / Self 相关性合格**（属 `get_salvage_pool` / RA 步 7）。

## 8. S0 评分机制（函数名即入口，不用审计工单号）

`score_datasets.py` 的分数 = `(0.4·coverage + crowd_penalty(alphaCount) + 0.2·breadth + 0.1·valueScore + empirical_prior) × category_weight[0.9~1.15]`；tier 按本区域数据集分布的**分位**切（缺省 tier1 ≥ P60、tier2 ≥ P30，`coverage_hard_min` 缺省 0.7，代码缺省见 `score_datasets.assign_quantile_tiers` 与 `thresholds.dataset_health`，细则 [`probe-scoring-v2.md`](references/probe-scoring-v2.md)）。新机制**缺省关闭 / 中性**，无对应台账时行为与旧版一致；`src/wqb/config.py::DATASET_HEALTH_SCORING` 是缺省事实源。

| 机制 | 作用 | 开关（`dataset_health`） | 读取的台账键 |
|---|---|---|---|
| 经验强度先验 | 分数叠加 `empirical_weight × clamp(ceiling_ratio)`，把目标从「干净 + 低拥挤」拉向「过闸概率」 | `empirical_weight`（0 = 关）/ `empirical_prior_neutral` | `dataset_empirical_prior`（由 `--calibrate` 写） |
| 饱和再验证降级 | 命中的数据集降 `excluded`，且不被保底带复活 | `saturation_demotion_enable` | `saturated_datasets`（**写入口 = `campaign_intel.py mark-saturated`**，S6 判某集被 prod 墙卡死时调用；合并式、缺省 dry-run、`--remove` 可撤销） |
| 饱和区拍平 model | 区域进入饱和态时 model 类 `category_weight` 封顶 1.0 | `flatten_model_when_saturated` | 由 `saturated_datasets` 非空推导 |
| universe 一致性守卫 | `s0_ranking` / `s0_whitelist` 的 universe ≠ `settings.universe` → `[WARN]`，提示重生成 + 白名单复核 | 常开 | `settings.json` |
| calibrate token 去重 | 剔除 group 变量关键字，防甜区污染 | 常开（calibrate 内） | — |

`s0_ranking.ranking[].score` = **信号强度榜**（哪个集能出好 alpha）；`pyramid_view` = **点塔战略榜**（哪个集点亮金字塔）。两榜语义分离：先看信号分定候选，再用点塔分排提交优先级，**勿相加或混排**。`s0_whitelist.candidates[].override` 手工捞回自动判死 / 排除集时必须写 `{reason, auto_tier, auto_excluded_by}`。`seat_model`（`campaign_intel s0-select` 读）目前**没有写入方**（`docs/ledger_keys.json` 登记为 orphan），缺省 `seats_per_dataset_default: 2`。

## 9. 闸门

闸编号的唯一注册表是 `gate.py` 的 `GATE_REGISTRY`（INDEX 里的闸表由 `gate.py --print-gate-table` 生成、测试比对）。文档里「5 闸」= 闸 1–5，「8 闸」= 闸 1–8（+ 可选闸 0，子闸 1b / 2b / 2b-2，附加闸 9）。`tools/wave_gate.py` 的闸 SEM / PF / 2b / 2.6 与逃生口总表在 INDEX「闸与逃生口总表」。逐闸细则见 [`gate-rules.md`](references/gate-rules.md)；下面只写容易读错的三点：

- **闸 7（longCount）目前只有 WARN**：`0 ≤ longCount < 80` 标 WARN，**没有任何代码读取区域 profile 的 `longcount_verdict` / `cw_gate` 把它升成 FAIL**（那两个键是文档级约定，见 RA `region-profile-contract.md`）。小宇宙区域（KOR / HKG / TWN）要按 FAIL 处理，由 agent 依 profile 自行执行。CW（持仓集中度）是回测后指标，不进静态闸，在步 7 评审处理。
- **闸 8（EVENT 类型）= 引用 `type==EVENT` 的字段即 FAIL**：平台没有 `ts_event_*` 系列（KOR wave16 实测 8/8 ERROR），旧口径「必须改用 `ts_event_*`」已作废——先做**单条探针**（§11 的二分协议）。
- **闸 6 契约过期是 FAIL-CLOSED**：`consumed_batches` 达 `expires_after_batches`（缺省 10）→ 阻断提交并**自动续约**新契约，要求按新契约重跑闸门；不是「过期就不再拦」。

## 10. fail-fast：失败性质判定（步 7 评审用）

评审先判**失败性质**再决定继续投入（机器实现 `_lib/rules.py::classify_failure`，阈值见 `FAIL_FAST_THRESHOLDS`，每条信号的量化口径在 [`docs/experience/fail_fast_rules.md`](docs/experience/fail_fast_rules.md)）：**七个无效努力信号**命中结构性信号（远期衰减 / 变体不变 / 相似度墙），或 `max_sharpe < 1.0`，或命中 ≥ 2 项 → `STOP_STRUCTURAL`（止损换方向）；仅命中参数层信号 → `RETRY_FIXABLE`（杠杆 = decay / neutralization / gate / 换历史位置表达）。纪律：**AI / 自动化只做研究效率（整理 / 统计 / 打标 / 复盘），不自动提交、不刷规则**。

> **经验库双轨（2026-09-29）**：`config/methodology_rules.json` 是**机器消费层**——本引擎 `RuleStore.query()` 会在 `build_wave` / `pipeline` / `gate` / `review_wave` 注入命中规则（硬拦截只有 `dead_end`（`block_pattern`）/ `universe_lever` / `explore_contract` 三类，`strategy` / `diagnosis` 仅提示）。与之**同源**的**人读层**在仓库 [`docs/experience/`](docs/experience/README.md)（索引 `README.md`：01 平台闸门 / 02 信号模式 / 03 区域数据集 / 04 工程纪律 / 05 反模式）。**改一边必须同步另一边**，否则出现「文档写了但流程不认」。2026-09-28 实证入库的五条：`sub_universe_ratio_gate_v1`、`pyramid_lighting_platform_only_v1`、`mixed_signal_leg_ban_v1`、`same_family_consecutive_submit_v1`、`region_stop_invest_v1`。

## 11. 平台报错二分排障（单条探针，不用 multisim）

multisim 是**连坐**语义：批内任一子模拟 ERROR，其余全部 CANCELLED。**排障时禁止再用 multisim 二分**（JPN `Invalid data field close` 实证：3 条 multisim 二分 → 3 条全 ERROR，两批白烧）。

1. 先本地：`python tools/campaign_intel.py ghost-audit`（幽灵算子）→ `wave_gate.py --expr`（语法 / 字段 / 区域非法字段）。
2. 仍需平台定位时，用**单条** `mcp__wq-brain-http__create_simulation`，按「最简 → 最复杂」逐层加：`rank(field)` → `rank(vec_avg(field))`（VECTOR）→ 加一层 `ts_*`（`ts_delta(field,5)`）→ 加 group / bucket；**第一条报错的层即病灶**。
3. 报错文本与表达式无关时（如 `Invalid data field close` 而式中无 close）先查区域数据可用性：`get_datasets(region, delay, universe, category=pv)` 看 pv1 是否存在（JPN / TOP1600 / D1 无 pv1 → 任何 `ts_*(vec_*(…))` 必错）。
4. 结论写入 `references/regions/<R>.md` 硬事实 + `platform_constraints.json`（`region_invalid_fields` / `region_vector_ts_forbidden`）+ GEM 侧预闸 `pipeline_pregate.py`，让 GEM 预闸与闸 2b 在下一波前拦住——三处同步，不留口头记忆。
5. `pipeline.py` 收批日志里 `隔离坏式=N 重发批=M` 是兜底信号：N > 0 说明预闸缺规则，回到第 4 步补规则。

## 12. 开关与入口（按绝对日期，不写「今日」）

| 入口 | 作用 | 何时用 |
|---|---|---|
| `pipeline.py run … --prod-first [--prod-first-top-k 2]` | 评审后自动调 `campaign_intel prod-first`：每信号族最强 1 条探 prod，写 `prod_first_<wave>`（**注意**：`campaign_intel prod-first` 自身 `--top-k` 缺省 3，这里 pipeline 透传缺省 2） | 新信号族第一波（步 5b）；族级 STOP 后不再投变体 |
| `pipeline.py run … --forum-recon` | 评审、prod-first 之后自动调 `tools/forum_recon_wave.py`：对本波共同卡住的墙（全灭时为「有无解法」）问一次论坛，每波 ≤ 1 次，结果落 ledger（`forum_recon_<qkey>` / `_negative_` / `_error_` + 完成标记 `forum_recon_wave_<wave>`）；只读、不阻断，故障不占本波额度。`batch_track` 节点缺省带上，`forum_recon=False` 可关 | 收批（默认路径）；离线 / 无论坛凭据的环境关掉 |
| `pipeline.py run … --batch-type probe` | 探针批：与 `repair` 同样豁免闸 6 多样性契约与 qp 预估标注 | 单集 8 条首探 |
| `campaign_intel.py xr-probe --exprs-file f --regions USA,GLB,HKG --tag t --write-ledger` | 跨区探针：按各区 settings 发 multisim → 收批入库（wave = `probe_<tag>`）→ 写 `GLOBAL/xr_probe_<tag>` | 判「机制能不能搬」，≤ 10 条 / 区 |
| `campaign_intel.py prod-first … --probe-timeout 600` | 单条 PC 硬超时 + 进程锁 `data/.prod_first.lock` | 平台 PC 单并发；并跑第二个被拒（退出码 3） |
| `campaign_intel.py backlog-drop [--include-gated] [--close-backtested] --apply` | 积压清理：> N 天未动且无回测的波标 dropped；已回测却仍 pending / gated 的波标 closed | `wave-ttl-check` WARN 时；缺省 dry-run |
| `campaign_intel.py s0-select`（缺省剔已点亮塔，`--include-lit` 保留） | 用户规则（2026-09-19）：已点亮塔不开战役 | 每次 S0 |
| `wave_gate.py --batch-type repair\|probe` | 跳过 qp 质量预估标注（修复批实测 S2.1 却被预估 0.65 BLOCK） | 修复 / 探针批 |
| `tools/prod_saturation_gate.py` | 字段「饱和」须有 prod 撞墙证据（已知 prod 中 ≥ 50% 且 ≥ 2 条 ≥ 0.7）；无 prod 信息只列 candidate；仅凭本账户 IS 过闸次数不再判饱和 | 自动（`wave_gate` 内） |

另有两条**数据行为**：`expressions.settings_json` 里的仿真键（decay / neutralization / universe / truncation …）会作为 per-item override 随批提交（同一波内表达式文本必须不同；非仿真键 `note` / `status_change` 自动剔除）；`harvest_multisim_results` 直接接受 `harvest_multisim_alphas` 的嵌套输出并自动补 `dataset`。启动期 `[wave-key-check]` / `[wave-ttl-check]` 每进程只打一次（`WQB_STARTUP_CHECKS=0` 关闭）。

## 13. 纪律

1. **原子写**：台账一律走 `make_ledger_store(ctx)`（缺省 SQLite 后端，`ledger_kv` 表；旧 JSON 后端已弃）；双遍重放 + 幂等 mutation。
2. **单进程单登录**；429 退避口径见 [`poll-and-quota.md`](references/poll-and-quota.md)。
3. 战役数据只按脚本既定产物写入；手工编辑先备份。**禁止第二权威实现**——一次性脚本模式已淘汰。
4. **提交配额是稀缺资源，但与回测并行槽位是两个独立机制**：`pipeline.py` 缺省**不**因提交额度中止回测发起（区域 `thresholds.submit_quota.enabled=true` 才启用该闸，`--force` 可越过；缺省关闭是 2026-08-26 用户指令）；未过 gate 不提交 alpha。
5. 选波 / 填槽的优先级（win 换腿、跨金字塔位、prod-first、弱探针上限）**只在 RA 步 4 / 步 6 与 `src/wqb/config.py::MINING`**，本 skill 不复写。类型为 `strategy` 的规则会在 `build_wave` / `pipeline` 打印 `[rules][strategy:…]`。
6. 新增 / 修改 workflow 节点的注册同步（四处）是开发者流程，见 AGENTS.md「变更影响面」，不在挖矿 skill 里。

## 14. 台账落盘（单轨 DB）

**波结论**回收后写 `wave_results`（不再手写 `wave<N>_results.json`）：

```powershell
# 一键导入现成 wave<N>_results.json（幂等，默认 status=closed）
& $WQ_PY "$TK/campaign.py" --campaign-dir tracking/<REGION> wave import --file <文件>
# 手填 / 更新（合并写入：只改本次给出的字段；--wave 用波号原字符串，--verdict 只收 PASS/FAIL/PARTIAL；
# 不给 --status 时：带 --verdict 即结案，否则已有波保持原状态、新波 open）
& $WQ_PY "$TK/campaign.py" --campaign-dir tracking/<REGION> wave upsert --wave 63 `
    --focus "…" --context "…" --verdict FAIL --status closed --finding "…" --finding "…"
& $WQ_PY "$TK/campaign.py" --campaign-dir tracking/<REGION> wave get --wave 63      # 写后验证
```

`WAVE_LEDGER.md` 是从数据库**生成**的快照（`python tools/export_wave_ledger_md.py --region <R>`，覆盖写，勿手改、勿当写入入口）。`review_wave.py --write-ledger` 写 ledger 键（`review_<tag>` 等，键契约见 `docs/ledger_keys.json`）。MCP 查询工具的清单与用法见 INDEX 工具表，不在此复制。

## 情景卡

### 情景 TK-A　`create_multi_simulation` 超时返回 `outcome_unknown`

- **前置状态**：发批调用超时，返回 `outcome_unknown`、`retry_safe=false`。
- **步骤**：① `workflow_task_status` 看任务是否还活着；② 按 multisim_id 查 `backtest_results`；③ 有行 → 走收批；无行且任务在跑 → 等，不重发；无行且任务已死 → 才重发（先过闸）。
- **完成定义**：该批要么已收批入库，要么确认死亡后只重发了一次。
- **反例**：看到超时就立刻重发（同一批双份占槽）；`TaskStop` 强杀（服务端已提交的仿真仍在跑，只会制造孤儿，见 `wqb-concurrency`）。

### 情景 TK-B　新数据集首波报 `Invalid data field close`

- **前置状态**：JPN / TOP1600 / D1，式中并无 close。
- **步骤**：按 §11 的二分协议：本地 ghost-audit → 单条 `create_simulation` 逐层加 → 查区域是否有 pv1 → 把结论写进 profile + `platform_constraints.json` + `pipeline_pregate.py`。
- **完成定义**：下一波 GEM 预闸 / 闸 2b 在本地就拦住同类式子。
- **反例**：用 multisim 二分；只在对话里记住「JPN 不能用 ts_*(vec_*)」。

### 情景 TK-C　评分前校准，dry-run 输出异常

- **前置状态**：`score_datasets.py --calibrate --dry-run` 打出甜区 `ac` 高达 8560–21508。
- **步骤**：疑似拥挤度口径把区域全部 alpha 算成了数据集拥挤，甜区反转会**反向奖励超拥挤**——**不要 apply**，先查 `ac` 来源；`strong_acs` 为空（无 best ≥ 1.5 的强信号）则甜区退回缺省 50–1000，确认该区确实要甜区逻辑再 apply；无实测数据的区（alphas 表空）护栏会跳过、不写。
- **完成定义**：写入 `thresholds.dataset_health` 的值经人工看过。
- **反例**：不看 dry-run 直接 apply。
