# 步 6（S3）细则：并发回测——入口、设置、故障处置

> 主 SOP 见 [`../SKILL.md`](../SKILL.md) 步 6。**并发参数的唯一来源是 `wqb.config.CONCURRENCY` 与 [`wqb-concurrency`](../../wqb-concurrency/SKILL.md) §8**——本文不复写数字，账户级槽位仲裁细节也在那里。

## 6.1 S3 入口选用

| 场景 | 入口 |
|---|---|
| 表达式来自 DB，要整波闸（**推荐**） | `mcp__wq-brain-http__workflow_batch_track`（先过三道开波闸；区域命中停止规则时不发批） |
| 手写 alpha_list / 需要自定义批 | [`brain-sim-alphas-in-batch-and-track`](../../brain-sim-alphas-in-batch-and-track/SKILL.md) |
| 调试 / 底层 | toolkit `pipeline.py`（`--review` 收批后自动写 `wave_results` 并刷新 `region_kb`） |
| 战役目录驱动 | `workflow_campaign(stage="S3")`（等价入口，同样先过三道开波闸） |

填槽内容（波内配额）仍以步 4 为准。设置展开需要时用 [`brain-inspect-raw-template-create-setting`](../../brain-inspect-raw-template-create-setting/SKILL.md)（`--from-db`），它不是第三条生成器。

## 6.2 调用（按需，不是顺序清单）

```
# 发批（异步返回 task_id；并发由 pipeline 内部锁定为 min(7, 批数)，不从外部传）
mcp__wq-brain-http__workflow_batch_track  region=$REGION  wave=$W  dataset=$DS
# 后台任务状态（不要 shell 翻日志）
mcp__wq-brain-http__workflow_task_status  task_id="<上一步返回的 task_id>"
mcp__wq-brain-http__workflow_task_status  prefix="batch_track"          # 列最近任务
# 批次状态（单次，非轮询）
mcp__wq-brain-http__batch_status          simulation_ids=["<id1>", "<id2>"]
# 手动补收 / 审计某批：一键收 multisim 全部 alpha 详情（并行），再入库
mcp__wq-brain-http__harvest_multisim_alphas  multisimulation_location="/simulations/<id>"
mcp__wqb-db__harvest_multisim_results        region=$REGION  wave=$W  alphas=<上一步的整个返回值>
# 只核对已入库的某批（只读报告：条数 / 关联 / 过闸率）
mcp__wqb-db__workflow_auto_harvest           region=$REGION  wave=$W  multisim_id=<id>
```

入库即级联本波 `wave_results` 暂定结论（评审会覆盖）与 `salvage_pool`；`multisim_id` 写进每条回测行。

## 6.3 设置与探针规则

1. **设置跟 win**：EUR 实证 `SUBINDUSTRY` + `decay4`；可另探本区合法档（`TOPCS1600` / `delay0` 等，以 `config.REGIONS` 为准）。⚠ `ILLIQUID_MINVOL1M` 对 USA / ASI / EUR 已被平台**永久停提**（2026-09-14 公告），不得再作对照探针档。
2. **设置层先验（默认开）**：`pipeline.py run` 装载 settings 后读 `region_kb.gate_priors`（缺则 `gate_priors_local`），`by_decay` / `by_neutralization` 里**样本 ≥ 30 且过闸率 ≥ 当前设置 × 2** 的格子自动改写本波设置，并打印 `[settings-prior] decay 4→14：当前 3.9%(n=408) vs 实测 28.3%(n=46) lift×7.2`（GBR 实证：decay=14 28.3% n=46 vs decay=4 3.9% n=408，而三波仍跑 decay4 → 0/44）。
   **覆盖关系**：显式 `--set decay=…` / `--neutralization` 钉住的维度**不动**；`--no-settings-prior` 或区域 `thresholds.json` `settings_prior.enabled=false` 关闭。想让 win 设置优先，就显式 `--set` 钉住。
3. 弱探针、组合批的定义与配额见步 4 细则 4.1（不在此重复）。
4. **prod-first 探针**：只在步 5b 定义一次（[`decision-table.md`](decision-table.md) D0-P）；本步只需记住「S3 收批后必调」。
5. 表达式从 `mcp__wqb-db__list_expressions` 取。**安全规则（最前）**：禁止自动提交 alpha——`workflow_submit_alpha` / `submit_alpha` 的 `confirm_submit=True` 只在步 8 用户确认后单独调用；`pipeline.py --submit` 与 `submit_batch` 是**派发仿真**，不是提交 alpha（词义见 GLOSSARY）。
6. `s2_compliance_w<wave>` 缺失不再中止、不再需要 `--force`（闸 2 / 3 的真正保障是 typed catalog：缺目录 stage_gate 直接 FAIL）。`pipeline.py` 所有中止路径返回 **rc = 2**（detached 启动器据此判断）。

### 6.3.1 QUICK / FULL 仿真模式（硬规则）

平台 2026-09-21 起支持 `simulationMode: QUICK / FULL`。**QUICK 没有 visualization / correlation / theme 检查，产出的 alpha 不可提交。**
本仓库的 MCP 工具与 pipeline **没有暴露该参数**（代码零命中），所以缺省全部是 FULL。若手工 / 新工具用了 QUICK：**产出仅用于探针信号判断，不得进入步 7 / 8，必须 FULL 复测，并在本波 `key_findings` 记录 simulationMode**——否则它会缺 correlation / theme 检查却被当通过。

## 6.4 故障处置

| 故障现象 | 判据（怎么确认是这一类） | 处理 |
|---|---|---|
| 8 子模拟全 ERROR | **先看 `message`**：属瞬态类（如 "try again"、连接超时）才重发；确定性 ERROR（非法字段 / 算子）重发只会烧配额 | 瞬态 → 重发相同表达式（USA/D0 3 次确认）；确定性 → 先归因再改表达式 |
| CROWDING 连续 2 次全 ERROR | 重发仍失败 | **跳过**该中性化 |
| fatal operator 级联 CANCEL 整批 | 批内含不确定算子（ts_entropy：20 条全 CANCEL） | **隔离不确定算子到独立小批次**（提交前预防）；提交后的连坐由 pipeline 自动处理（见下） |
| 瞬态 "try again" 整批命中 | e10a / e10b | **拆成 5 条 / 批**重试 |
| **429 THROTTLED** | 账户级限速 | ① 等待退避（MCP 内建 `Retry-After` + 指数）；② `WQB_GLOBAL_SLOTS=<n>` 降账户级并发（缺省 7；0 关闭；由 `_lib/slots.py` 仲裁）；③ 批大小 ≤ 5。**注意**：外部往 pipeline 传非 7 的并发只会收到 warning，不会降并发 |
| MCP 超时无 result | 服务进程假死 | 在 WQ BRAIN 控制台查看该批（进程排障命令依 OS 而异，见 wqb-concurrency） |
| "took too much resource" | **真问题**：model26 364 字段实证 | 去 backfill 或缩短窗口 |
| `create_multi_simulation` / `preflight_expressions` / `batch_get_alpha_metrics` 报 `must be array` | MCP 数组参数在 WorkBuddy 宿主的 DeferExecuteTool 通道上**间歇性**被损坏，**与表达式内容无关**；`upsert_expressions` 还会把 `[[...]]` 压成字面量 `"item"` 的脏行（WorkBuddy 记忆 2026-10-02 / 10-03） | 不要重试、不要改表达式。绕行：`tools/submit_batch.py`（settings 固定，与 MCP 批不可比）/ `tools/ind_sim_submit.py`（settings 全显式）直连 `POST /simulations`；写库走 `CampaignStore.upsert_expressions(region=, wave=, items=[...])`（形参是 `items`），**写后必复核**行内容 |
| **进程被宿主回收**（停在提交中途、stderr 全空、无 traceback；2026-10-02 GLB 12:25 / 12:29 两次） | 外部 SIGKILL 特征，不是代码异常；`workflow_task_status` 此时给不出可信终态 | **重启前先用 `batch_status` 核实每批终态**，COMPLETE 的批写进 checkpoint 的 terminal 集再续跑：平台对「同一 (表达式, 设置)」幂等去重，重提 RUNNING / COMPLETE 的批只会白烧槽位、拿回同一批 alpha（实测两个不同 multisim 返回逐位相同的 alpha 集合）。长任务跨 turn 存活不可靠：同 turn 内前台盯到关键节点，或分批续跑；`batch_track` detached 被判启动失败时前台直跑 `pipeline.py` |
| **`workflow_task_status` 的 failed 判据偏粗** | 无显式终态（`status` / `returncode`）的旧布局任务：进程已死 + stderr 非空即判 `failed`（`src/wqb/workflow/tasks.py` 推断分支）；而 `[gate] …` / `[slots] …` 的正常日志也写 stderr | 以 `batch_status` + stdout 为准；有显式终态的任务不受影响 |
| **checkpoint 不能判进度** | `ckpt_w<wave>` 存 ledger、**每轮覆盖**，只留最后一轮的 batches（实测波 1 只剩 2 批且已 HTTP 404 失效，`gate.total` 是更早一次小波的残留）；还会缓存失败态（`batch_gates ok=False`） | 进度以平台 `batch_status` 为准；重跑前先删 checkpoint 里的失败段 |
| multisim 创建阶段卡死 | 父任务 progress 停在 0.1 且 child_count=0 超过 10 分钟（经验值；children 列表滞后于 progress，0.35 在跑时 harvest 仍可能报 no children）。其余阶段仍按 `WAIT_THRESHOLDS.sim_stall_min` 判 `STALLED` | 直接重发（旧任务无害、不占配额）；部分子任务 ERROR 时同批其余可能被标 CANCELLED（≠ 表达式错，重发即跑）；单次上限 10 条 |

`create_multi_simulation` 要求 ≥ 2 条表达式；**先归因再决定重发 / 跳过 / 拆批**。

- **连坐隔离已自动化**（`pipeline.py` 默认开，`--no-isolate-errors` 关）：某批 ERROR 时解析子模拟 `status / message / regular`，定位真正报错的坏式 → 回写 `expressions.status='fail'`（reason = 平台错误正文）→ 其余无辜表达式作为「重发批」**优先于** pending 队列在下一个空槽重发一次（重发批再 ERROR 不再重发）。JPN w7/w8 实证：一条 `bucket()` 缺 range / 一个平台不认的字段，整批 8 条连坐，10 批丢 8 批 64 条。
- **积压清理（每波结束时）**：判据只有一套——`pending + gated` 占比与 `unconsumed` 溢出比由 `step_funnel.py` 与开波积压闸给出（见 [`loop-and-stop.md`](loop-and-stop.md)）；清理走 `python tools/campaign_intel.py backlog-drop --region $REGION`（默认 dry-run），并把近闸积压纳入下一波（`build_wave --from-db` 重取）；**禁止无脑新建表达式堆库**。

## 6.5 完成定义

本波全部 multisim 到**终态**，且 `backtest_results` 行数 = 波内表达式数（含 ERROR / CANCELLED 的标记行）。整批 CANCELLED → 回步 5。
