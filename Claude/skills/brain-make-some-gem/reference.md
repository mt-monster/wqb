# brain-make-some-gem Reference

## Folder Layout

```text
brain-make-some-gem/
├── SKILL.md
├── reference.md
└── scripts/
  ├── headless_runner/
  │   ├── run.py
  │   ├── config.json
  │   └── README.md
  └── trailSomeAlphas/
    ├── run_pipeline.py
    ├── README.md
    └── skills/
      ├── brain-data-feature-engineering/
      └── brain-feature-implementation/
```

## Functional Responsibility
- `scripts/headless_runner/run.py`
  - User-facing entrypoint for parameterized runs
  - Handles config, retries, and orchestration
- `scripts/trailSomeAlphas/run_pipeline.py`
  - Core prompt + fetch + implement + merge pipeline
- `scripts/trailSomeAlphas/skills/brain-feature-implementation/data/...`
  - Final expression artifacts and intermediate outputs

## 直接命令（workflow 节点不可用时）

```bash
cd scripts/headless_runner
python run.py --config config.json \
  --data-category <CATEGORY> --region <REGION> --delay <DELAY> \
  --dataset-id <DATASET_ID> --universe <UNIVERSE> \
  --instrument-type EQUITY --data-type <MATRIX|VECTOR> \
  --priors-from-db --detached
```

## Long-Task Controls
- `--detached`: 后台启动并立即返回
- `--task-id`: 指定任务 ID
- `--tasks-dir`: 任务根目录（默认 `../outputs/tasks`，仓库战役用 `logs/_async_tasks`）
- `--status <task_id> --tail-lines 60`: 查询后台任务状态
- `--dry-run`: 只校验并打印命令，不执行

状态查询示例：

```bash
cd scripts/headless_runner
python run.py --status <task_id> --tail-lines 60
```

## 看实时生成过程（2026-09-25）

`--detached` 写死 `DETACHED_PROCESS|CREATE_NO_WINDOW` + stdout 重定向到文件，MCP 服务自身也无控制台，所以终端里天生看不到。两种补法：

- `--detached --console`（= `workflow_gem(console=True)`）：另弹一个真实控制台窗口滚动输出，
  同时经 `_ConsoleFileTee` 双写**同一份** `stdout.log`，所以 `--status` / `workflow_task_status`
  / 闸门读取面全部不变。代价：任务寿命绑在那个窗口上 —— 关窗口 = 杀任务，而 phased
  无断点（mapping 只在内存累加、Phase 3 才落盘），中途被杀 = 整波丢弃。只在人盯盘时开。
- `--watch <task_id> --tasks-dir <root> [--from-start]`：对任意在飞任务做 tail -f，
  `meta.status` 进终态自动收尾，Ctrl+C 只退跟随、不动任务。**看而不抢输出流**，默认用这个。

## Artifact Paths
- Ideas markdown:
  - `scripts/trailSomeAlphas/skills/brain-data-feature-engineering/output_report/{region}_delay{delay}_{datasetID}_ideas.md`
- Final expressions:
  - `scripts/trailSomeAlphas/skills/brain-feature-implementation/data/{datasetID}_{region}_delay{delay}/final_expressions.json`

## Known Failure Modes
- `401 Incorrect authentication credentials`:
  - Credentials issue from config/env, not pipeline logic.
- Missing config fields:
  - `scripts/headless_runner/run.py` should fail fast and print missing keys.
- Empty/invalid expression output:
  - Check dataset/data_type match and operator filtering conditions.
