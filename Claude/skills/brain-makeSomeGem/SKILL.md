---
last_verified: 2026-09-05
name: brain-makeSomeGem
description: "S2 概念优先的 GEM alpha 表达式生成器（headless_runner）。当需要为某个 region/dataset/delay/universe 组合生成候选 alpha 表达式、跑 GEM、补候选池、按 priors 做增强变体扩展时使用。触发词：生成表达式 / 跑 GEM / makeSomeGem / 选波生成 / 概念优先生成 / final_expressions。编排入口是 wq-brain-ra-pipeline 步 4，标准调用走 mcp__wq-brain-http__workflow_gem，本 skill 描述其后端引擎与产物契约。"
layer: L2
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
  - mcp__wqb-db__*
---

# brain-makeSomeGem（S2 表达式生成引擎）

## 定位声明

- **本 skill 不是编排器**。唯一挖掘编排 SOP 是 `wq-brain-ra-pipeline`（步 4 = 本 skill）。
- **标准调用方式 = `mcp__wq-brain-http__workflow_gem`**（workflow `gem` 节点）。它负责：解析 skill 目录 → 组装 headless_runner 命令 → 执行 → 校验 `final_expressions.json` → 自动跑质量预估 → 标记 Mode B。
- 只有在 workflow 节点不可用（skill 目录解析失败、需要 workflow 未暴露的 run.py 参数）时，才按下方「直接命令」小节手工执行。
- `brain-feature-implementation` 与 `brain-data-feature-engineering` 在本管道**内部**被调用，**不要**把它们当主链入口。

## 上下游

| 位置 | 内容 |
|---|---|
| **上游** | 步 3（S1）`s1_<ds>_d<delay>` ledger 的 ideas.md；`assemble-priors` 落的 `priors_snapshot_<region>` |
| **本 skill** | 概念优先生成候选表达式 → `final_expressions.json` |
| **下游** | 步 5（S2→S3）门禁：`check_batch` 多样性守卫 → `check_expr_against_inspect` 体检硬门 → `wave_gate` 5 闸预检 |

## 概念优先铁律（与 ra-pipeline 步 4 硬约束同源，此处不复写阈值）

1. **机制 → 1-2 个具体字段 id → 一个 Implementation Example**。禁止「每个字段套 rank」式枚举。
2. 必须带 priors。默认从 DB 快照直读（`priors_from_db=True`，fail-closed：无快照即报错，不静默无 priors 运行）；`priors_file` 仅作显式覆盖/降级兜底。
3. GEM 管道只消费 priors 的 `wins`（≤6）与 `dead_ends`（≤12）两个键（`economic_priors.py`），其余键会被忽略。
4. 只用标准时间窗口 1/5/22/66/252/504/1008/1260；其他窗口必须给出解释或实测证据。
5. 取骨架前必查 `KB/community_tpl_kb` 的 `ghost_operator_advisory`，先做幽灵算子替换再进批，否则整批 ERROR/CANCELLED。

## 标准调用（推荐）

```
mcp__wq-brain-http__workflow_gem  region=$REGION  dataset_id=$DS  delay=$DELAY  universe=$UNIVERSE  data_type=$DTYPE
```

`data_type` 必须与 S1 `get_datafields` 确认的 VECTOR/MATRIX 比例一致——传错会导致整批表达式类型不匹配。
`ideas_file` 可省略：默认从 S1 ledger 自动注入；显式传入则覆盖。
`priors_file` 可省略：默认走 DB 快照。

返回含 `expression_count` / `quality_estimation` / `mode_b_required`（`EXPECTED_BLOCK > 0` 时为真）。

## 直接命令（仅当 workflow 节点不可用）

```bash
cd scripts/headless_runner
python run.py --config config.json \
  --data-category <CATEGORY> --region <REGION> --delay <DELAY> \
  --dataset-id <DATASET_ID> --universe <UNIVERSE> \
  --instrument-type EQUITY --data-type <MATRIX|VECTOR> \
  --priors-from-db --detached
```

长任务控制：`--detached` 后台启动并立即返回；`--task-id` 指定任务 ID；`--tasks-dir` 任务根目录（默认 `../outputs/tasks`）。
状态查询：`python run.py --status <task_id> --tail-lines 60`。
`--dry-run` 只校验并打印命令，不执行。

其余可选参数（`--pipeline-mode phased` / `--max-expressions` / `--require-operators` / `--regen-ideas` 等）见 [reference.md](reference.md)。

## 产物契约

`final_expressions.json` 按序查找两个位置（`gem` 节点 `_find_final_expressions` 同口径）：

1. `scripts/trailSomeAlphas/skills/brain-feature-implementation/data/{datasetID}_{region}_delay{delay}/final_expressions.json`
2. `scripts/headless_runner/outputs/{datasetID}_{region}_delay{delay}/final_expressions.json`

**`final_expressions.json` 不是真相源**——战役产物只入 `data/wqb.db`（`expressions` 表 status=`gem`/`enhanced`）。该文件仅为管道中间产物，落库后以 DB 为准。未验证 DB 有表达式，不得声称步 4 成功。

## 失败分支

| 现象 | 处理 |
|---|---|
| GEM 未入库 | 先按 `--status <task_id>` 查后台任务，确认失败才回退，不要手写脚本 |
| 候选不足 | enhance / 扩组合；仍不足则换数据集 |
| `401 Incorrect authentication credentials` | 凭据/配置问题，不是管道逻辑问题 |
| 缺 config 字段 | run.py fail-fast 并打印缺失键 |
| 输出为空或非法 | 核对 dataset 与 `data_type` 是否匹配、算子过滤条件是否过严 |
| 无 priors 快照 | 先跑 `workflow_campaign(stage="S6", subcommand="assemble-priors")` |

## 反模式

- 步 4 不跑 GEM，或 GEM 只产 `rank({field})` 却拿去填槽。
- 把 `final_expressions.json` 当真相源。
- 直接把 `brain-feature-implementation` 当主链入口（它在本管道内部）。
- 手写 PowerShell/requests 替代 `workflow_gem`。
