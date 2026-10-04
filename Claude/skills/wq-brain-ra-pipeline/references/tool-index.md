# 工具索引：步 → MCP 工具 / 节点 / CLI · 整链执行

> 主 SOP 见 [`../SKILL.md`](../SKILL.md)。**按步查工具**（旧附录按「逻辑名 → 模块」排，且只覆盖 22 个工具、含第 3 处「唯一权威」）。
> MCP 调用名 = `mcp__<server>__<注册名>`：`wq-brain-http`（平台侧）与 `wqb-db`（本地库）两个 server。**MCP 应用尽用**：能走 MCP 的步骤走 MCP，CLI 只用于「无对应 MCP」或「无 MCP 时」。
> 工具 / 节点**总数**的唯一基准是 [INDEX「MCP 工具/节点计数」](../../INDEX.md)；每个节点的参数以 `workflow_list_nodes` 为准（不在这里抄）。维护规则：新增 / 改名 MCP 工具或节点时同步本表（`tools/skill_lint.py` 会检查文中工具名是否已注册）。

## T.1 步 → 工具

| 步 | MCP 工具（主路径） | 节点（`workflow_execute(node=…)`；括号内为独立 MCP 入口） | CLI（无 MCP / 无对应 MCP） |
|---|---|---|---|
| 1 S-PRE | `wqb-db`：`get_campaign_summary` / `get_dead_ends` / `get_dead_datasets` / `get_mining_yield` / `get_cross_region_lessons`；`wq-brain-http`：`get_messages`（PPA 主题） | `inventory_scan`（`wqb-db` `workflow_inventory_scan`） | `tools/build_gate_prior_from_inventory.py`、`tools/select_ra_basket.py` |
| 2 S0 | `wq-brain-http`：`workflow_campaign(stage="S0")` | `campaign` | `tools/campaign_intel.py s0-select` / `xr-probe` |
| 3 S1 | `workflow_campaign(stage="S1")`、`get_datafields`、`create_multi_simulation(validate_fields=true)` | `campaign`；`feature_engineering`（可选，产物**仅人读**） | `tools/field_semantic_classify.py`、`tools/gen_field_inspect_packs.py` |
| 4 S2 | `workflow_campaign(subcommand="assemble-priors")`、`workflow_gem` | `gem`；`gem_wave`（`wqb-db` `workflow_gem_wave`：GEM + 去重 + 分桶 + 骨架配给 + 选波，增强入口） | `Claude/skills/brain-make-some-gem/scripts/headless_runner/run.py`（LLM 通道故障时的 `--ideas-file` 旁路） |
| 5 门禁 | `preflight_expressions`（VECTOR 用 `auto_fix_vector=true`）、`operator_audit`（**平台算子表**审计，不是表达式级幽灵检查） | `wave_gate`；`unified_gate`（`wqb-db` `workflow_unified_gate`：幽灵算子 + 多样性 + 体检 + 8 闸预检，增强入口） | `tools/campaign_intel.py ghost-audit`、`tools/wave_gate.py` |
| 6 S3 | `workflow_batch_track`、`workflow_task_status`、`batch_status`、`harvest_multisim_alphas` + `wqb-db` `harvest_multisim_results` | `batch_track`；`auto_harvest`（`wqb-db` `workflow_auto_harvest`：**只读**核对已入库的批） | toolkit `pipeline.py`（`--review` 收批后写 `wave_results` 并刷新 `region_kb`） |
| 5b / 7 S4 | `workflow_campaign(stage="S4")`、`check_correlation`、`check_self_correlation`、`compute_mutual_correlation`；`wqb-db` `get_salvage_pool` | `campaign`；`auto_review`（`wqb-db` `workflow_auto_review`：预筛 + walls 诊断 + 辅助腿检索）；按需 `alpha_booster` / `modeb_improve`（批量变体器，护栏见步 7 §7.8） | `tools/campaign_intel.py prod-first` / `s4-prescreen`；`brain-calculate-alpha-selfcorr-quick` |
| 8 提交 | `submit_verdict`（**否决权威**）；`check_correlation(refresh=True)`；`workflow_submit_alpha`（**不可逆**，`confirm_submit=True` 仅在用户确认后单独调用）；PPA 交接 `tools/ppa_handoff.py`；SUPER `workflow_superalpha` | `judge`（参考评审，不放行）、`submit_alpha`、`superalpha`——**提交类节点不入链** | `tools/submit_verdict.py`；`tools/quota_status.py` |
| 9 S6 | `wqb-db`：`upsert_wave_result` / `seal_dead_end` / `upsert_registry_empirical` / `upsert_ledger_key`；`wq-brain-http`：`workflow_campaign(subcommand="dataset-experience"\|"assemble-priors")`、`value_factor_trendScore`、`performance_comparison` | `auto_pyramid`（`wqb-db` `workflow_auto_pyramid`：点塔进度回写） | `tools/step_funnel.py`、`tools/campaign_intel.py pyramid` / `mark-saturated` |
| 横向 | — | `forum_recon`、`forum_recon_wave`（波级默认取证，收批时自动；触发表见 [`forum-recon-triggers.md`](forum-recon-triggers.md)） | `tools/forum_recon.py`、`tools/forum_recon_wave.py`；步 4 → 5 之间的形状配额体检 `tools/shape_quota_check.py`（[`step4-generation.md`](step4-generation.md) §4.5.1） |

「增强入口」= 把若干步合并成一个节点的便利封装；**它们不改变各步的完成定义**——完成定义只认各步细则里的产物（表 / 台账键 / 文件），节点返回 `success=true` 不等于完成。
`hypothesis_round` / `structural_reconstruct` 是研究类节点（前者对饱和数据集做假设优先实验，后者实测仅 1 行产出，降为实验性），不在九步主路径上。

## T.2 整链执行（可选）：`workflow_chain`

一条链只能串**节点**；下面这些步骤没有单一节点或不该入链：步 1 的库存分流（要按篮子状态判断）、步 7 的逐候选人审、步 8 的提交判定与确认、步 9 的判死封存（要人核对）。链式调用**先干跑再实跑**：

```
mcp__wq-brain-http__workflow_chain  dry_run=true  chain=[
  {"node": "campaign",            "params": {"region": "$REGION", "stage": "S0"}},
  {"node": "gem",                 "params": {"region": "$REGION", "dataset_id": "$DS", "delay": $DELAY, "universe": "$UNIVERSE", "data_type": "$DTYPE"}},
  {"node": "wave_gate",           "params": {"region": "$REGION", "dataset": "$DS", "wave": "$W"}},
  {"node": "batch_track",         "params": {"region": "$REGION", "wave": "$W", "dataset": "$DS"}}
]
```

- **干跑证明什么 / 不证明什么**：干跑逐节点把真实命令构建出来（不起子进程、不写库）并**校验命令能否被目标脚本的 argparse 接受**，`failed_at` 指出首个断点。它**不证明**：LLM 通道可达（GEM；`402` 时干跑照样 OK）、配额与并发可用、平台鉴权有效、写库成功、字段 / 算子被平台接受。**干跑绿 ≠ 能跑。**
- **异步 join**：`join_async=True`（缺省）时，gem / batch_track / campaign / feature_engineering 这类「启动即返回」的节点，链会等其后台任务到终态再走下一步，任务失败即按该步失败中止（否则下游必然读到上游尚未落库的空结果）。要「只发起不等待」传 `join_async=false`，再用 `workflow_task_status` 跟踪；单步等待上限 `join_timeout_sec`（缺省 1800 s）。
- **gem 后紧跟 batch_track 而中间没有 wave_gate 时，`workflow_chain` 自动插入 `wave_gate`**（inspect 模式取显式传参 > `WQB_INSPECT_MODE` > `warn`；闸 PF 开），防止自动链跳过门禁。
- **提交类节点不入链，由代码强制**：`submit_alpha` / `superalpha` 只要带 `confirm_submit=True` 出现在链里，`wqb.workflow.executor.execute_chain` 就**整链拒绝、一步都不执行**（干跑也拒；`confirm_submit` 缺省 / 为假的提交类步骤只做预检，允许入链）。守护测试 `tests/unit/02_workflow/test_workflow_chain_irreversible_guard.py`。真正的提交只能是用户确认后的**单独一次**调用。

## T.3 MCP 名与实现位置（排障用）

| 逻辑名 | MCP 调用名（全名，勿凭记忆猜） | 定义处 |
|---|---|---|
| workflow 战役 / GEM / 批量跟踪 / 特征工程 | `mcp__wq-brain-http__workflow_campaign` / `workflow_gem` / `workflow_batch_track` / `workflow_feature_engineering` | `world-quant-brain-mcp/tools_workflow.py` |
| workflow 链 / 执行 / 节点清单 / 任务状态 | `mcp__wq-brain-http__workflow_chain` / `workflow_execute` / `workflow_list_nodes` / `workflow_task_status` | `tools_workflow.py` |
| workflow 提交 / SuperAlpha / 判定 / 结构重构 | `mcp__wq-brain-http__workflow_submit_alpha` / `workflow_superalpha` / `workflow_judge` / `workflow_structural_reconstruct` | `tools_workflow.py` |
| 库存盘点 / 合并选波 / 合并门禁 | `mcp__wqb-db__workflow_inventory_scan` / `workflow_gem_wave` / `workflow_unified_gate` | `wqb_db_mcp.py` |
| 收批核对 / 自动评审 / 点塔回写 | `mcp__wqb-db__workflow_auto_harvest` / `workflow_auto_review` / `workflow_auto_pyramid` | `wqb_db_mcp.py` |
| 提交判定 / 批量派发 / SA 探针 / 算子审计 / 批状态 | `mcp__wq-brain-http__submit_verdict` / `submit_batch` / `sa_probe` / `operator_audit` / `batch_status`（`submit_batch` 是**派发仿真**，不是提交 alpha） | `world-quant-brain-mcp/tools_ops.py` |
| 精确设置直连派发（MCP 数组参数间歇损坏时的绕行；无对应 MCP，CLI） | `python tools/ind_sim_submit.py --path <exprs.txt> --decay N --neutralization X`——settings 全显式（含 `nanHandling` / `maxTrade` 强度闸），`--preflight-catalog` 可先预检字段名；对照 `tools/submit_batch.py` 固定 nanHandling=OFF / maxTrade=OFF，两者与 MCP 批**不可比**（见决策表 D5） | `tools/ind_sim_submit.py` / `tools/submit_batch.py` |
| 表达式预检 | `mcp__wq-brain-http__preflight_expressions` | `tools_data.py` |
| 回测收割 → 入库 | `mcp__wq-brain-http__harvest_multisim_alphas` → `mcp__wqb-db__harvest_multisim_results` | `tools_sim.py` / `wqb_db_mcp.py` |
| 直写库 | `mcp__wqb-db__upsert_expressions` / `upsert_gate_result` / `upsert_backtest_rows` / `upsert_field_catalog` / `upsert_ledger_key` / `upsert_wave_result` / `upsert_registry_empirical`；批量改状态 `set_expression_status`（只传 id / 状态过滤，不回传正文） | `wqb_db_mcp.py` |
| `workflow_judge`（**参考层**，非提交裁决） | `mcp__wq-brain-http__workflow_judge` | `tools_workflow.py`。返回的 `verdict`（READY / REVIEW / BLOCK）只是摘要，优先读 `checklist`（逐闸事实）与 `degraded_gates`（取不到数的闸）；**`degraded_gates` 非空 ⇒ `verdict` 不可作提交依据**（降级闸此前会静默凑出 READY） |
