# Skill 调用链（薄索引）

> **本文件只做索引，不承载流程正文。** 权威来源：
> - 挖掘流程（when / what / 怎么挖、九步 SOP、每步输入输出与失败分支）→
>   [`Claude/skills/wq-brain-ra-pipeline/SKILL.md`](../../Claude/skills/wq-brain-ra-pipeline/SKILL.md)
> - 项目规约（Shell 引号 / 工具化 / skill 契约 / 命名 / 运行环境）→ [`AGENTS.md`](../../AGENTS.md)
> - 分层、阶段表、闸门阶梯、命名例外 → [`Claude/skills/INDEX.md`](../../Claude/skills/INDEX.md)
>
> **2026-09-11 重写**：此前本文件逐条复制了调用链正文，已与代码/流程实质漂移——阶段标签把 GEM 标成
> S4、把提交判定标成 S6；仍把 `brain-alpha-judge` 当提交判定权威（其已于 2026-08-31 自我弃用）；
> 引用不存在的 MCP 名 `mcp__wq-brain-http__submit_alpha`；写死 `.qoder-cn` 安装位路径；示例给出
> `concurrency: 7`（`pipeline.py` 根本没有该参数）。**改流程只改 `wq-brain-ra-pipeline/SKILL.md`。**

## 阶段 → 入口 → 执行体（唯一对照表）

| 步 | 阶段 | 入口（MCP / CLI） | 执行体 / 后端 | 产物（真相源） |
|---|---|---|---|---|
| 1 | S-PRE 查表 | `wq-brain-campaign-matrix` + `mcp__wqb-db__get_*` | —（只查表，不执行） | 配置包（参数，不落盘） |
| 2 | S0 体检 | `mcp__wq-brain-http__workflow_campaign(stage="S0")` | toolkit `score_datasets.py` | ledger `s0_ranking` / `s0_whitelist` |
| 3 | S1 字段 | `workflow_campaign(stage="S1")` + `workflow_feature_engineering` | toolkit `scan_fields.py` | `fields` 表 + ledger `s1_<ds>_d<delay>` |
| 4 | S2 生成 | `workflow_gem`（强制）；priors 用 `workflow_campaign(subcommand="assemble-priors")` | `brain-make-some-gem` headless_runner；toolkit `assemble_priors.py` | `expressions`(status=gem) + `priors_snapshot_<region>` |
| 5 | S2→S3 门禁 | `workflow_execute(node="wave_gate")`（2026-09-11 新增节点）或 CLI：`tools/campaign_intel.py ghost-audit` + `tools/wave_gate.py` | `tools/wave_gate.py`（内含 `field_inspect_gate.py`）+ toolkit `gate.py` | `gate_results` |
| 6 | S3 七槽回测 | `workflow_batch_track` | toolkit `pipeline.py` → `BrainApiClient.create_multi_simulation` | `backtest_results` / `wave_results` / checkpoint |
| 7 | S4 诊断 | `workflow_campaign(stage="S4")` + `wq-brain-alpha-optimization-v1` | toolkit `review_wave.py` | ledger `s4_walls_*` + `salvage_pool` |
| 8 | S4→S5 判定 | `mcp__wq-brain-http__submit_verdict`（**唯一权威**）→ 用户确认 → `workflow_submit_alpha` | `tools/submit_verdict.py` | `submit_ready` 池 |
| 9 | S6 回写 | `mcp__wqb-db__upsert_wave_result` / `upsert_registry_empirical` / `upsert_ledger_key` | toolkit `campaign.py`（ledger / registry / wave） | `wave_results` + `registry_empirical` |

## 易错点（2026-09-11 逐项核对过）

- **步 5 没有 workflow 节点**；`workflow_campaign(stage="S2")` 只路由到 `build_wave.py`＝**选波**（步 4 已调），
  不能拿它代替门禁。门禁必须走仓根 `tools/` CLI。
- **`workflow_chain` 覆盖步 2/3/4/5/6**。registry 实注 8 个节点：`campaign` / `feature_engineering` /
  `gem` / `batch_track` / `wave_gate` / `judge` / `submit_alpha` / `superalpha`；步 1/7/8/9 无节点。
- **提交类与评审节点禁止入自动链**：`submit_alpha` / `superalpha` 须用户确认后单独调用；
  `judge` 自 2026-08-31 起仅为**参考层**（PPA 人工核对清单 + trend score），不构成提交依据。
- 提交 MCP 工具名是 **`workflow_submit_alpha`**（不存在名为 `submit_alpha` 的 MCP 工具；
  直连 DB 侧的批量提交工具是 `submit_batch`）。
- 并发纪律唯一权威 = `wqb-concurrency §8`；`pipeline.py` **没有 `--concurrency` 参数**，
  n_slots 由内部锁定 `min(7, 批数)`，把 `concurrency: 7` 拼进命令只会得到 warning / argparse 拒绝。
- 表达式输入默认 **`--from-db`**（读 `expressions` 表）；`alpha_list.json` / `simulation_status.csv`
  仅作排障与断点续跑兼容，**不是**交接真相源（战场产物只入 `data/wqb.db`）。
- 依赖/路径：`WQ_VALIDATOR_DIR` / `WQ_TOOLKIT_DIR` 或自动搜索安装位；**禁止**写死 `C:\Users\...` 或 `.qoder-cn/skills/...` 绝对路径（见 `AGENTS.md §6`）。

## 环境变量

见 [`INDEX.md §运行环境铁律`](../../Claude/skills/INDEX.md)（`$WQ_PY` / `$WQ_TOOLKIT_DIR` / `$WQ_VALIDATOR_DIR`
与凭证链）。换机器只改该处定义。

---

*文档版本：2026-09-11（取代 2026-08-27 版）。关联规约：`AGENTS.md §5/§6`、`INDEX.md`。*
