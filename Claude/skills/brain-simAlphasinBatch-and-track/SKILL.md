---
last_verified: 2026-08-23
name: brain-simAlphasinBatch-and-track
description: "WorldQuant BRAIN alpha 批量提交与跟踪（JSON 输入 → CSV 续跑）+ 战役执行入口。当用户要求 批量回测/批量提交 alpha、断点续传、查看 simulation_status.csv、重跑失败项、调并发、战役 pipeline、 七槽填槽模式、配额闸、跨区临时批跑 时调用。S3 编排器入口；执行后端为 wq-brain-campaign-toolkit 引擎。"
layer: L3
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - TaskCreate
---

## 持久化铁律（DB 单轨）

战役产物只写入 `data/wqb.db`（经 `wqb.store` / `mcp__wqb-db__*`）。**禁止**把 `final_expressions.json` / `alpha_list.json` / `candidates/*.json` / `cache/*batches*.json` / `results/*.csv` 当交接真相源；Agent 禁止 Write 这些文件。静态配置与凭证除外。








# Brain Sim Alphas Batch Track（独立批量跟踪）

## 角色定位

- **编排器（`wq-brain-ra-pipeline`）S3 入口 = 本 skill**。本 skill 是批量跟踪与战役执行的单一入口。
- **执行后端 = `wq-brain-campaign-toolkit`**（引擎实现层，本 skill 通过 subprocess 调用其脚本）。两 skill 是"入口/引擎"关系，不重复实现。
- **独立 skill，不依赖 `brain-makeSomeGem`**——只要输入符合 `alpha_list.json` 格式即可。

## 衔接协议
- **上游**：S3 前置 `brain-inspectRawTemplate-create-Setting`（产出 `settings_candidates.json` + `alpha_list.json`，并默认写 **expressions 表**）；或用户直接提供的合规 `alpha_list.json`。**表达式输入默认读库**：引擎 `pipeline.py --from-db` 默认启用（文件模式已废弃），从 **expressions 表**（`data/wqb.db`，结构化真相源）按 region+wave 取表达式；`alpha_list.json`/`--file` 仅为兼容输入与排障。
- **本 skill 角色**：S3 批量回测与战役执行单一入口。**并发纪律（七槽填槽 SOP、C≈7 Token-Bucket 锁定在飞数）的唯一权威定义在 `wqb-concurrency` 技能（§8）**，本 skill 只引用不重复实现。
- **下游**：回测结果双写 **backtest_results 表**（`mcp__wqb-db__*` 可查）；`simulation_status.csv`（+ 战役目录 `results/`）为排障兼容产物，交 S4 链首步 `brain-how-to-pass-AlphaTest` 做失败项定位与阈值判定（查历史回测优先读库）。

## 运行环境

所有 Python 命令使用 MCP venv：`$WQ_PY`，确保依赖（requests/pandas/ply）可用。不要使用系统 Python。

PowerShell 中用 `;` 链命令（不要用 `&&`）；路径检查用 `Test-Path`、`Get-ChildItem`、`Import-Csv`。

## 输入/输出契约

| 类型 | 默认路径 | 说明 |
|---|---|---|
| alpha 输入 | `data/alpha_list.json`（兼容根目录 `alpha_list.json`） | 待回测的表达式+设置列表 |
| 状态输出 | `outputs/simulation_status.csv`（用户可指定） | 续跑的唯一真相源（文件级） |
| 多样性报告 | `outputs/diversity_report.json`（开启增强时生成） | 增强前后指标+动作记录 |
| **回测结果（结构化真相源）** | `data/wqb.db` → **backtest_results 表**（pipeline.py 双写） | 引擎脚本直写；库为跨阶段查询接口，CSV/JSON 仅为排障兼容 |
| **波级台账** | `data/wqb.db` → wave_results / ledger_kv 表（`--write-ledger` 时） | 正式回写走 toolkit 幂等 CLI；会话内轻量回写可用 `mcp__wqb-db__upsert_wave_result` / `upsert_ledger_key` |

**入库总原则**：流程产物一律入数据库（结构化真相源），文件仅作排障与断点续跑兼容；S4 链查历史回测优先读 backtest_results 表（`mcp__wqb-db__*` 查询工具），文件缺失不阻塞。

## 凭据

- 首选：`configs/config.json`（仓库内不含此文件，需按 `configs/README.md` 自建）
- 兜底：环境变量 `BRAIN_EMAIL` / `BRAIN_PASSWORD`
- 禁止把凭据硬编码进代码或文档。

## 标准命令（MCP 工具调用）

**推荐**：使用 `mcp__wq-brain-http__workflow_batch_track` MCP 工具（workflow 引擎快捷方式）：

```
# S3 批量回测跟踪
mcp__wq-brain-http__workflow_batch_track(
  region="KOR",
  wave="36A",
  dataset="model219",
  concurrency=7,  # 七槽填槽
  max_rounds=3
)

# 批次状态查询（单次，非轮询）
mcp__wq-brain-http__batch_status(simulation_ids=["<id1>", "<id2>"])
```

**兼容模式**（旧 PowerShell 链，逐步淘汰）：

```powershell
# 在本 skill 所在目录运行（<skills_root> 按实际安装根替换，通常为 ~/.qoder-cn/skills）
Set-Location "<skills_root>/brain-simAlphasinBatch-and-track"
python scripts/batch_simulator.py --config configs/config.json --alpha-json data/alpha_list.json --output-csv outputs/simulation_status.csv --batch-size 3 --concurrency 2 --detached
# ⚠️ 上面的 --concurrency 2 / --batch-size 3 只适用于「非编排的跨区临时批」（保守试探）。
# 战役目录内的正式 wave 一律走七槽填槽 concurrency=7（唯一权威 wqb-concurrency §8），
# 不要照抄这两个数字去跑正式波次。

# 查询后台任务状态（替换 task_id）
python scripts/batch_simulator.py --status "<task_id>" --tail-lines 60
```

## 长任务执行规则

1. **启动前预检**：`configs/config.json` 存在（或 env 凭据就绪）、`data/alpha_list.json` 存在。
2. **默认后台执行**：大批量用 `--detached`，每 60–180 秒轮询一次。
3. **进度真相源 = 输出 CSV**，不是终端 tail。终端超时不等于失败。
4. **超时处理**：命令跟踪超时时，先查 CSV 是否存在、文件大小是否变化、行数是否增加；artifact 仍在更新就继续轮询。
5. **失败判定**（两个条件同时满足才算失败）：
   - 进程看似停止或不可达，且
   - CSV 无进展持续 ≥ 3 分钟。
6. **每轮轮询最少检查**：CSV 存在 / 总行数 / `status` 分布（`COMPLETE/COMPLETED`、`ERROR/FAIL`、其他）。
7. **最终摘要必含**：CSV 路径、总行数、各 status 计数、下一步建议（续跑 / 仅重跑失败项 / 降并发）。

## 续跑语义

- 续跑键 = `fingerprint` + 同一输出 CSV 文件。
- 声明"无法续跑"前必须先核对：同一 CSV 路径、alpha 内容/settings/type 未变。
- 不要随意改 fingerprint 逻辑，除非用户明确要求。

## 多样性增强（双路径）

多样性增强现已集成到两条执行路径：

| 路径 | 脚本 | 触发方式 | 场景 |
|---|---|---|---|
| 战役引擎（S2 选波） | `../wq-brain-campaign-toolkit/scripts/build_wave.py` | `--enhance-diversity always`（默认）/ auto / never | 战役目录内正式 wave 回测 |
| ad-hoc 批量（本 skill 自带） | `scripts/batch_simulator.py` | `--enhance-diversity always`（默认）/ auto / never | 非编排跨区临时批 |

ad-hoc 批量路径使用本 skill 自带 `scripts/diversity_enhancer.py`；战役引擎路径的多样性增强由 `../wq-brain-campaign-toolkit/scripts/build_wave.py` 内部实现。**默认即走多样性路**（`always`），无需显式传参；显式 `--enhance-diversity never` 可关闭。

**模式**：
```powershell
--enhance-diversity always  # 默认，强制增强
--enhance-diversity auto    # 多样性不足时自动增强
--enhance-diversity never   # 禁用
```

**自动增强触发阈值**：
- 算子熵 < 2.0
- 算子覆盖率 < 50%
- 新颖度 < 80%
- 结构相似度 > 70%

**增强方式**：结构变异（swap_branches/insert_layer/delete_layer）、算子替换（ts_rank → ts_scale）、事件门控（trade_when/if_else）、分组包裹（group_rank/group_zscore）。

**产出**：`diversity_report.json`（CSV 同目录），含原始/增强后指标、改进建议、动作记录。

## 战役引擎能力（本 skill 调用 `wq-brain-campaign-toolkit` 作为执行后端）

本 skill 是批量跟踪与战役执行的**单一入口**；以下能力由 `wq-brain-campaign-toolkit`（引擎实现层，相对路径 `../wq-brain-campaign-toolkit/`）提供，本 skill 调用它们完成 S1–S6 各阶段执行。两 skill 是"入口/引擎"关系，不重复实现。

| 阶段 | 能力 | 引擎脚本（`../wq-brain-campaign-toolkit/scripts/`） | 产出 |
|---|---|---|---|
| S1 | 字段扫描（typed catalog） | `scan_fields.py` | `reference/<region>_<dataset>_fields.json` |
| S1 | 数据集评分+探针计划 | `score_datasets.py` | `reference/<region>_dataset_ranking.json`（mode/tier/tier_note） |
| S2 | 候选生成（去重/分桶/骨架配给）+ 多样性增强 | `build_wave.py`（`--enhance-diversity auto/always/never`） | `candidates/*.json` + `candidates/<region>_wave<wave>_diversity_report.json` |
| S2 | 5 闸预检（语法/字段白名单/VECTOR 包裹/不可访问算子/毒模式） | `gate.py` | 闸门报告 |
| S3 | 七槽填槽模式（7 批 multisim 同提、统一轮询、即收即补；并发纪律权威定义见 **`wqb-concurrency`** §8；**填槽内容**（组合优先 vs 弱探针）硬约束见 **`wq-brain-ra-pipeline` 步 4/步 6**，本表不复写；pipeline.py 2026-08-21 代码落地，支持 `--max-rounds` 多轮） | `pipeline.py`（七槽模式） | checkpoint JSON + alpha id |
| S3 | 挂起熔断/退避/配额闸（机制沿用） | `pipeline.py`（内部 poller） | STALLED 检测、ET 日历日配额闸 |
| S4 | 评审墙诊断 | `review_wave.py` | `reviews/<region>_review_<wave>.json`（walls + 候选/near） |
| S4 | 三灯探针评分 | `score_datasets.py --probe-score` | 三灯报告 |
| S5 | 配额查询（ET 日历日 4/1 口径） | `pipeline.py quota` | 配额状态 |
| S6 | 多样性审计 | `diversity_audit.py` | 同质报告 |
| S6 | 台账回写 | `campaign.py ledger`（内部 LedgerStore） | `ledger_kv` 表（data/wqb.db，SQLite 后端） |

**调用规则**：
- 本 skill 通过 `subprocess` 调用引擎脚本，命令统一用 `python ../wq-brain-campaign-toolkit/scripts/<script>.py --campaign-dir tracking/<REGION> ...`。
- 引擎脚本的 `--campaign-dir` 参数指向战役目录（`tracking/<REGION>/`），所有产出落到该目录下的 `reference/`、`candidates/`、`results/`、`reviews/` 子目录。
- 配置基准：`tracking/<REGION>/config/settings.json`（region/universe/delay/中性化）与 `config/thresholds.json`（闸门阈值、`dataset_health`、`poll` 退避参数）。
- 引擎细节（算子约束、poll-and-quota 参数、campaign-dir 契约）见 `../wq-brain-campaign-toolkit/references/` 下各文档；本 skill 文档不重复，按需引用。
- **填槽内容**：有空槽补单数据集组合批，禁止五数据集同时首探；细则只引用 `wq-brain-ra-pipeline` 步 4/步 6，本 skill 不复写。

**与传统 batch_simulator.py 的关系**：
- `batch_simulator.py`（本 skill 自带）= 多批并发 ThreadPool 的轻量跟踪器，用于非编排跨区临时批。
- 引擎脚本（`pipeline.py` 等）= 战役目录内的正式执行路径，七槽填槽模式 + 熔断 + 配额闸。
- 两者共存：编排器/正式战役走引擎脚本；ad-hoc 批量跟踪走 `batch_simulator.py`。

## 输出契约

每次返回：
1. status CSV 路径
2. 总行数与各 `status` 计数
3. submitted/skipped/completed/failed 摘要（如可用）
4. 下一步建议（如降并发或仅重跑失败项）

## 参考文件

- 字段与文件映射：[reference.md](reference.md)
- 触发示例：[examples.md](examples.md)


## 工具化纪律（tools/ 通用工具，勿再写一次性脚本）

批次/子任务状态查询与轮询**不要手写** `check_*batch*.py`，用通用工具（内置 429 退避）：

```powershell
& $WQ_PY tools/batch_status.py --ids <sim_or_multisim_id> [...] --watch --json <落盘路径>
# --interval 轮询间隔秒（默认 20）  --max-waits 最大次数（默认 180 = 60min）
```

每波门禁同理走 `tools/wave_gate.py`（见 `wq-brain-ra-pipeline` 步 5），
禁止新建 `tracking/<R>/scripts/_gate_waveNN.py`。
