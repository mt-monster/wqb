---
last_verified: 2026-09-29
name: brain-sim-alphas-in-batch-and-track
description: "批量发起 alpha 回测并跟踪（发起回测 ≠ 提交 alpha）：手写 / 外部 alpha 列表的批量回测、断点续跑、失败项重跑，用 batch_simulator.py 或 workflow_batch_track。战役目录内正式波次的入口选用见本文；并发调优找 wqb-concurrency，战役引擎参数找 wq-brain-campaign-toolkit。"
layer: L3
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - TaskCreate
---

# Brain Sim Alphas Batch Track（批量回测跟踪）

## 职责边界

- **本 skill 负责**：**S3 的批量仿真入口之一**——批量发批 / 跟踪 / 断点续跑，回测结果入库（`backtest_results`）；并给出**入口选用表**（下节）。**整链走 `wq-brain-ra-pipeline`。**
- **本 skill 不做**：**不提交 alpha**（提交是 L5；这里的 `--submit` / 「提交」一律指**提交回测**）；不做门禁（门禁是 `tools/wave_gate.py`）、不生成表达式；**不写 `settings.json`**（静态配置：建战役目录时由人补，缺失时 `workflow_campaign` 节点按 DB 补建）；不管并发调优（`wqb-concurrency`）与配额（toolkit）。
- **上游 / 下游**：上游 = RA 步 5 已过闸的批次（DB `expressions` 表），或用户直给的合规 alpha 列表；下游 = S4 评审（`brain-how-to-pass-alpha-test` 起，读 `backtest_results`）。

## 入口选用表（S3 有三个入口，各管一类场景）

| 场景 | 入口 | 说明 |
|---|---|---|
| 战役目录内、DB 里已有本波表达式，要整波过闸后回测 | **`mcp__wq-brain-http__workflow_batch_track`**（推荐） | 节点内含区域闸；七槽填槽；细则 RA 步 6 §6.1 |
| 战役目录内、要调引擎参数 / 调试 | toolkit `pipeline.py run …`（`wq-brain-campaign-toolkit`） | 引擎本体；`--submit` = 发起回测 |
| **手写 / 外部来源的 alpha 列表，或非战役目录的跨区临时批** | **本 skill 的 `scripts/batch_simulator.py`**（兼容路径） | CSV 是进度缓存；见下 |

**并发纪律（七槽填槽、C≈7、账户级仲裁）的唯一权威在 `wqb-concurrency`（§8）**，本 skill 只引用。填槽内容（组合优先 vs 弱探针）的硬约束在 RA 步 4 / 步 6，这里不复写。

## 持久化铁律（DB 单轨）

战役产物只写入 `data/wqb.db`（经 `wqb.store` / `mcp__wqb-db__*`）。**禁止**把 `final_expressions.json` / `alpha_list.json` / `candidates/*.json` / `results/*.csv` 当**跨阶段交接的真相源**；Agent 不 Write 这些文件。跨阶段交接一律走 DB：表达式 = `expressions` 表，结果 = `backtest_results` 表，波结论 = `wave_results`。

> `simulation_status.csv` 是 `batch_simulator.py` **断点续跑的进度缓存**（记录哪些 multisim 已提交 / 回收），不是交接真相源——下游 S4 优先读 `backtest_results`，CSV 缺失不阻塞。上面的「禁止」针对「拿 CSV 当跨阶段交接依据」，不针对引擎自己续跑时读写它；二者不矛盾。

## 输入 / 输出契约

| 类型 | 默认 | 说明 |
|---|---|---|
| alpha 输入（默认） | `data/wqb.db` → `expressions` 表（`pipeline.py --from-db`，缺省启用） | 按 region + wave 取待回测表达式 |
| alpha 输入（兼容） | `data/alpha_list.json` | **已废弃的文件模式**：仅 `batch_simulator.py` 的跨区临时批 / 排障 |
| 状态输出 | `outputs/simulation_status.csv`（用户可指定） | 进度缓存，非真相源 |
| **回测结果** | `backtest_results` 表 | 引擎直写；`batch_simulator.py` 同时入库，CSV 降为导出视图 |
| 波级台账 | `wave_results` / `ledger_kv` | 回写路径见 toolkit SKILL §3 写入矩阵 |

## 凭据

凭据**由脚本 / MCP 自己读取**：**agent 不读取 `.env`、不打印、不把口令放命令行**（AGENTS.md）。标准环境变量名 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（与 MCP 服务、toolkit 同名）；`batch_simulator.py` 的解析顺序是 `--config`（`configs/config.json`，本地文件、已被 `.gitignore`，格式见 `configs/README.md`）→ 环境变量（`CREDENTIALS_*`，另认旧别名 `BRAIN_EMAIL` / `BRAIN_USERNAME` / `BRAIN_PASSWORD`）→ 工作区 `world-quant-brain-mcp/.env`。禁止把凭据硬编码进代码或文档。

## 运行环境

所有 Python 命令用 MCP venv：`$WQ_PY`（依赖 requests / pandas / ply），不要用系统 Python。PowerShell 用 `;` 链命令（不用 `&&`）；路径检查用 `Test-Path`、`Get-ChildItem`、`Import-Csv`。

## 标准命令

**推荐**（战役内正式波次）：`mcp__wq-brain-http__workflow_batch_track`：

```
mcp__wq-brain-http__workflow_batch_track(region="KOR", wave="<W>", dataset="<ds>", concurrency=7, max_rounds=3)
mcp__wq-brain-http__batch_status(simulation_ids=["<id1>", "<id2>"])     # 单次状态查询，非轮询
```

> MCP 节点的 `concurrency` 是节点内部参数（映射七槽填槽）；CLI 层**禁止**给 `pipeline.py run` 拼 `--concurrency`（argparse 未声明，会被 `validate_argv` 拦截）——两者不是一回事。

**兼容路径**（`batch_simulator.py`，跨区临时批 / 手写列表）。⚠️ **先看警告**：下面的 `<B>` / `<C>` 是**占位**，不是推荐值——旧文的示例数字是保守的试探值，被人当默认抄进了正式波次；**战役目录内的正式 wave 一律走七槽填槽**，不要用本路径。

```powershell
Set-Location "<skills_root>/brain-sim-alphas-in-batch-and-track"      # 真相源 = 仓库 Claude/skills，各宿主安装位同名
& $WQ_PY scripts/batch_simulator.py --config configs/config.json --alpha-json data/alpha_list.json `
    --output-csv outputs/simulation_status.csv --batch-size <B> --concurrency <C> --detached
& $WQ_PY scripts/batch_simulator.py --status "<task_id>" --tail-lines 60      # 查询后台任务
```

## 长任务与失败判据（两条路径，各写各的）

**MCP / 引擎路径**（`workflow_batch_track` + `workflow_task_status`，**没有 CSV**）：进度看任务状态与 `backtest_results`；在飞回测 progress 连续 `WAIT_THRESHOLDS.sim_stall_min`（60 分钟）无变化判 `STALLED`、总时长超 `sim_timeout_min`（360 分钟）判超时（数字唯一来源 `src/wqb/config.py::WAIT_THRESHOLDS`）。发批超时返回 `outcome_unknown` 时**禁止盲目重发**，按 toolkit SKILL §7 的恢复顺序处理。

**兼容 CLI 路径**（`batch_simulator.py`，进度真相源 = **输出 CSV**，不是终端 tail；终端超时不等于失败）：

1. **启动前预检**：凭据就绪（`configs/config.json` 存在或环境变量已设）、`data/alpha_list.json` 存在。
2. 大批量用 `--detached`，每 60–180 秒查询一次；命令跟踪超时时先看 CSV 是否存在、大小是否变化、行数是否增加，仍在更新就继续等。
3. **失败判定（两个条件同时满足）**：进程看似停止或不可达，**且** CSV 无进展持续 ≥ 3 分钟。**这条只回答「本地进程还活着吗」**；平台侧「仿真卡住了吗」是 60 分钟那条——两者判的是不同层，别互相替代。
4. 每轮最少检查：CSV 存在 / 总行数 / `status` 分布（`COMPLETE` / `ERROR` / 其他）。
5. 最终摘要必含：CSV 路径、总行数、各 status 计数、下一步建议（续跑 / 仅重跑失败项 / 降并发）。

## 续跑语义（CSV 路径）

续跑键 = `fingerprint` + 同一输出 CSV。声明「无法续跑」前必须先核对：同一 CSV 路径、alpha 的内容 / settings / type 未变。不要随意改 fingerprint 逻辑，除非用户明确要求。

## 多样性增强（`--enhance-diversity`，缺省 `never`）

`batch_simulator.py` 与 toolkit `build_wave.py` 都有 `--enhance-diversity never | auto | always`，**缺省 `never`**（2026-09-29 起，此前缺省 `always`）。原因：增强会**结构变异 / 替换外层算子（如 `ts_rank → ts_scale`）/ 追加 novel、random 式**，与 GEM 铁律（显式 idea 的表达式保持经济方向，算子多样性是语义多样性的结果）和 RA「不补参数变体凑数」冲突；`auto` 的触发阈值（算子熵 < 2.0、覆盖率 < 50%、新颖度 < 80%、结构相似度 > 70%）是经验值、没有实证依据。需要时**显式**传 `auto` / `always`（例如为降 prod 相关性有意试所有算子），并留意产出的 `diversity_report.json`（原始 / 增强后指标 + 动作记录）。战役引擎路径的增强由 `build_wave.py` 内部实现；本 skill 自带 `scripts/diversity_enhancer.py` 只服务 `batch_simulator.py`。

## 战役引擎能力

本 skill 不再复制「阶段 → 脚本 → 产物」映射表（那是第三份拷贝）。**阶段与脚本**见 `wq-brain-campaign-toolkit` SKILL §1 的分工表与 §6 子命令表；**产物落点**见其「产物契约」表（以 DB 为准）。调用引擎脚本统一 `--campaign-dir tracking/<REGION>`，配置基准是 `config/settings.json` 与 `config/thresholds.json`。

## 输出契约

每次返回：① 任务 / 批次标识（MCP 路径 = `task_id` 与 multisim id；CLI 路径 = status CSV 路径）；② 总数与各 `status` 计数；③ submitted / skipped / completed / failed 摘要（如可用）；④ 下一步建议（降并发 / 仅重跑失败项 / 转 S4）。

## 情景卡

### 情景 SA-A　手写 20 条 alpha 做一次跨区临时回测

- **前置状态**：用户给了一份合规 `alpha_list.json`，不在任何战役目录里。
- **步骤**：① 确认凭据已由环境提供（不读 `.env`）；② `batch_simulator.py … --detached`（`<B>` / `<C>` 按用户意图，正式波次不走这条）；③ 每 60–180 s `--status` 查询；④ 以 CSV 行数与 status 分布汇报；⑤ 结果同时在 `backtest_results`。
- **分支**：进程不可达且 CSV ≥ 3 分钟无更新 → 用**同一 CSV** 续跑；改了 alpha 内容 → 会重跑（fingerprint 变了）。
- **完成定义**：输出契约四项齐全。
- **反例**：把这条路径用于战役正式波次；拿 CSV 当 S4 的输入。

### 情景 SA-B　整波过闸后发批，结果卡在 `outcome_unknown`

- **步骤**：`workflow_task_status` → 按 multisim_id 查 `backtest_results` → 两处都空且任务已死才重发（toolkit SKILL §7）。
- **反例**：超时就重发；`TaskStop` 强杀（制造孤儿，见 `wqb-concurrency` §4）。

## 参考与工具化纪律

- 字段与文件映射：[reference.md](reference.md)；触发示例：[examples.md](examples.md)；CLI 使用说明：[README.md](README.md)。
- 批次 / 子任务状态查询与轮询**不要手写** `check_*batch*.py`，用通用工具（内置 429 退避）：

```powershell
& $WQ_PY tools/batch_status.py --ids <sim_or_multisim_id> [...] --watch --json <落盘路径>
# --interval 轮询间隔秒（缺省 20）  --max-waits 最大次数（缺省 180 = 60 分钟）
```

每波门禁走 `tools/wave_gate.py`（RA 步 5），禁止新建 `tracking/<R>/scripts/_gate_waveNN.py`。
