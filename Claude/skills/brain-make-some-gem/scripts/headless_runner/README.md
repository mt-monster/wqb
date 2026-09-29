# brain-make-some-gem 无 UI 独立运行说明

> **标准入口是 MCP 工具 `mcp__wq-brain-http__workflow_gem`**（见上级 [`SKILL.md`](../../SKILL.md)）。本文只在 workflow 节点不可用、或想用 `--ideas-file` 绕过 LLM 时手工运行 `run.py` 用。

## 目录结构

- `run.py`：无 UI 入口（本质是调 `../trailSomeAlphas/run_pipeline.py`）
- `config.example.json`：配置模板；`config.json`：**用户自建**的运行配置——已 `.gitignore`、不参与 `sync_skills`，**agent 不读、不写、不打印它**
- `../trailSomeAlphas/`：核心流水线代码

## 1) 配置

`cp config.example.json config.json` 后填写：

| 项 | 来源（高 → 低） | 说明 |
|---|---|---|
| `moonshot_base_url` / `moonshot_model` | `config.json`（必填，非密钥） | LLM 供应商是 Moonshot（OpenAI 兼容接口；模型缺省 `kimi-k2.6`） |
| BRAIN 账号 | 环境变量 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（标准名，与 MCP 服务同名；旧别名 `BRAIN_USERNAME` / `BRAIN_EMAIL` / `BRAIN_PASSWORD` 仍认）→ `config.json` 的 `brain_email` / `brain_password` | 环境变量齐了就不必写进 `config.json` |
| LLM 密钥 | 环境变量 `MOONSHOT_API_KEY` → `config.json` 的 `moonshot_api_key` | **给了 `--ideas-file` 就不调 LLM，不需要密钥** |

启动时打印 `[cred] BRAIN 凭据来源=… ；LLM 密钥来源=…`——**只打印来源，不打印值**。环境变量优先于 `config.json`（此前是 `config.json` 无条件覆盖）。**口令不要写在命令行参数里**（`run_pipeline.py` 虽有 `--username` / `--password` / `--moonshot-api-key`，命令行会进 shell 历史与进程列表）；缺凭据时 `run.py` 报错退出，不耗平台资源。

## 2) 运行

在仓库根，`$WQ_PY` = MCP venv 解释器；`<HR>` = `Claude/skills/brain-make-some-gem/scripts/headless_runner`（`--config` / `--tasks-dir` 的相对路径按 `run.py` 所在目录解析，所以**不需要 `cd`**；仓库战役的任务根用绝对路径 `<仓库根>/logs/_async_tasks`）：

```powershell
& $WQ_PY <HR>/run.py --config config.json --data-category <CATEGORY> --region <REGION> --delay <DELAY> `
    --dataset-id <DATASET_ID> --universe <UNIVERSE> --instrument-type EQUITY --data-type <MATRIX|VECTOR|GROUP> `
    --priors-from-db <REGION> --db-path <仓库根>/data/wqb.db --detached --tasks-dir <仓库根>/logs/_async_tasks
```

`--priors-from-db` **必须带区域值**（旧文的写法漏了值，会把后面的 `--detached` 当成它的参数而报错）；`--db-path` 显式给库路径，避免从当前目录向上找不到 `data/wqb.db`。常用可选参数：`--ideas-file <path>`（不调 LLM）、`--regen-ideas`、`--pipeline-mode single|phased|skeleton`（缺省 `phased`）、`--max-expressions`、`--require-operators` / `--require-count`（**软提示**，强制点在下游闸 6）、`--max-fields` / `--max-operators` / `--no-operators-in-prompt`、`--moonshot-base-url` / `--moonshot-retries` / `--moonshot-retry-backoff`。完整清单以 `run.py --help` 为准。

**先做参数检查（不执行）**：加 `--dry-run`。⚠ 它**只验证命令构建**，验证不了 LLM 可达性 / 余额——`402 Insufficient Balance` 时干跑照样显示 OK。

## 3) 结果输出

- 中间产物：`<仓库根>/data/gem_runs/<DATASET>_<REGION>_delay<DELAY>/final_expressions.json`（`WQB_GEM_DATA_ROOT` 可覆盖）——**不是真相源**。战役产物只入 `data/wqb.db`：`run_pipeline.py` 收尾时**自己**把通过校验的表达式写进 `expressions` 表（`status=gem`，wave = `s2_<DATASET>_d<DELAY>`；`run_pipeline.py --wave` 可改，`run.py` 不转发该参数），并打印 `[db] expressions/<REGION>/<wave> n=… status=gem`；用 `mcp__wqb-db__list_expressions(region, wave)` 核对，**看不到行就不算成功**。`workflow_gem` 节点在此之上还做来源标注、质量预估与 `mode_b_required`，手工运行没有这几步。
- GEM 自生成的 ideas 报告：`data/gem_runs/output_report/gem_<REGION>_delay<DELAY>_<DATASET>_ideas.md`。
- 旧位（`scripts/trailSomeAlphas/skills/brain-feature-implementation/data/…`、`scripts/headless_runner/outputs/…`）只是历史兜底，**勿再用于新跑**。
