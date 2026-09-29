# brain-make-some-gem 参考（查表用）

> 流程、铁律与排障见 [`SKILL.md`](SKILL.md)。本文只放目录结构、参数与路径速查；2026-09-29 由英文旧稿重写——旧稿把已迁走的深嵌套路径当产物位置、把 `cd` + 裸 `python` 当标准命令。

## 目录结构

```text
brain-make-some-gem/
├── SKILL.md · reference.md · examples.md
└── scripts/
    ├── headless_runner/        run.py（无 UI 入口）· config.example.json（模板）· README.md
    │                           （config.json = 用户自建的凭据文件：已 .gitignore、不参与 sync_skills、agent 不读不写）
    └── trailSomeAlphas/        run_pipeline.py（主流水线）· pipeline_*.py · economic_priors.py · skeletons*.py · skill_roots.py
        └── skills/             内嵌兜底副本：brain-feature-implementation（scripts/ 是硬依赖 + SKILL.md 副本）
                                              brain-data-feature-engineering（三个 GENERATED 副本，无 SKILL.md）
```

## 模块职责

| 模块 | 职责 |
|---|---|
| `headless_runner/run.py` | 参数解析、凭据注入（环境变量 > config.json）、`--detached` 后台启动与 `--status` / `--watch`、LLM 通道的不可重试错误（401 / 402 / 403） |
| `run_pipeline.py` | 主流水线：取字段 → 生成 / 读取 ideas → 渲染模板 → 校验 + 预闸 → **写 `expressions` 表**（`status=gem`） |
| `pipeline_paths.py` | 路径常量、skill 目录解析（env > skill_roots > 内嵌兜底）、`GEM_DATA_ROOT` / `GEM_REPORT_ROOT` |
| `pipeline_llm.py` / `pipeline_prompts.py` | Moonshot 调用（SSE + 退避重试）/ prompt 组装（概念优先规则 + priors + 算子清单） |
| `pipeline_pregate.py` | 生成侧预闸（规则表在 RA `step4-generation.md` §4.4） |
| `pipeline_reports.py` / `pipeline_placeholders.py` / `pipeline_data.py` | ideas markdown 的渲染 / 落盘 / 解析 / 占位符卫生 / 凭据与会话、字段后缀 |
| `pipeline_kb.py` / `economic_priors.py` | `CampaignStore` 与模板族绑定 / priors 文本化（`compact_priors_text`） |
| `skeletons*.py` | skeleton mode：骨架库 + 语义填槽（代码组装表达式） |

## 参数：`workflow_gem`（MCP）与节点

| 参数 | MCP `workflow_gem` | 节点 `gem`（`workflow_execute`） | 缺省 |
|---|:-:|:-:|---|
| `region` / `dataset_id` / `delay` / `universe` | ✓ | ✓ | 必填 |
| `data_category` | ✓ | ✓ | 按平台 category 推断 |
| `instrument_type` / `data_type` | ✓ | ✓ | `EQUITY` / `MATRIX`（**须与字段类型一致**） |
| `priors_file` / `priors_from_db` | ✓ | ✓ | 空 / `True`（DB 快照，缺则 fail-closed） |
| `ideas_file` | ✓ | ✓ | 空（S1 ledger 自动注入） |
| `detached` / `launch_only` / `console` | ✓ | ✓ | `True` / `False` / `False`（`console` 仅 Windows） |
| `pipeline_mode` | ✓ | ✓ | MCP 缺省 `None`（→ config → `phased`）；节点缺省 `phased` |
| `batch_size` / `require_operators` / `require_count` / `prod_first` / `prod_first_top_k` | — | ✓ | 100 / 空 / 2 / `False` / 2 |
| `dry_run` | ✓ | 经 executor 注入 | `False`（**只验证命令构建，验证不了 LLM**） |

## `run.py` 常用参数

`--config`（缺省 `config.json`，相对 `run.py` 所在目录）· `--data-category` / `--region` / `--delay` / `--dataset-id`（必填）· `--universe`（缺省 `TOP3000`，**其它区域必须显式给合法档位**，取 `config.REGIONS[<R>]["default_universe"]`）· `--instrument-type` · `--data-type MATRIX|VECTOR|GROUP` · `--ideas-file` / `--regen-ideas` · `--pipeline-mode single|phased|skeleton` · `--priors-file` **xor** `--priors-from-db <REGION>`（互斥，后者要带区域值）· `--db-path` · `--max-expressions`（缺省 24 / 模板）· `--require-operators` / `--require-count`（软提示）· `--detached` / `--task-id` / `--tasks-dir`（相对路径按 `run.py` 目录解析）· `--status` / `--watch` / `--from-start` / `--tail-lines` · `--dry-run`。完整清单以 `run.py --help` 为准。

## 产物路径

| 产物 | 位置 |
|---|---|
| 表达式中间产物 | `<仓库根>/data/gem_runs/{DATASET}_{REGION}_delay{DELAY}/final_expressions.json`（`WQB_GEM_DATA_ROOT` 可覆盖）——**不是真相源** |
| 真相源 | `data/wqb.db` 的 `expressions` 表（`status=gem`，wave = `s2_<DS>_d<DELAY>`）；ledger `s2_<DS>_d<DELAY>_idea`；自含生成路径回写 `s1_<DS>_d<DELAY>`（`source=s2_nested`） |
| GEM 自生成 ideas 报告 | `data/gem_runs/output_report/gem_{REGION}_delay{DELAY}_{DATASET}_ideas.md`（人工写的用 `manual_` 前缀，见 FE） |
| 后台任务 | `--tasks-dir/<task_id>/`：`meta.json` · `stdout.log` · `stderr.log` |

## 环境变量

`CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（BRAIN，标准名）· `MOONSHOT_API_KEY` / `MOONSHOT_BASE_URL` / `MOONSHOT_RETRIES` / `MOONSHOT_RETRY_BACKOFF`（LLM）· `WQB_GEM_DATA_ROOT`（产物根）· `WQB_FI_SKILL_DIR` / `WQB_DFE_SKILL_DIR`（skill 目录覆盖）· `WQB_GEM_MAX_PER_SKELETON`（同骨架封顶，缺省 12，0 关闭）· `GEM_META_TIMEOUT_SEC`（节点等 meta.json 握手，缺省 90）。
