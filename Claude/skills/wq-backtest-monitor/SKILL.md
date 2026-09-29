---
last_verified: 2026-09-29
name: wq-backtest-monitor
description: "S6 监控与复盘：盯在飞回测（进度 / ETA / 卡住判定）、盘点候选的提交状态（对齐 submit_verdict 标签，PASS_CHEAP 不称可提交）、按统一骨架出复盘报告，并触发 + 核验 S6 台账回写（回写 SOP 只在 wq-brain-ra-pipeline 步 9）。用户要求盯回测任务 / 看任务情况 / 盘点挖掘任务 / 回测效率 / 哪些 alpha 可提交 / 复盘时使用。REGULAR / PPA / SUPER 通用；不做 OS 表现监控与重着色（目前没有承接者）。"
layer: L6
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - mcp__wqb-db__get_wave_result
  - mcp__wqb-db__list_wave_results
  - mcp__wqb-db__get_latest_wave
  - mcp__wqb-db__get_ledger_key
  - mcp__wqb-db__list_alphas_by_wave
version: "1.1"
agent_created: true
---

# WQ 回测监控与复盘（S6）

## 职责边界

- **本 skill 负责**：S6 的**监控与复盘**——在飞任务的进度 / ETA / 卡住判定、候选的提交状态盘点、统一骨架的复盘报告，以及**触发并核验**台账回写。
- **本 skill 不做**：**不是** `wave_results` / `registry_empirical` 的写入 SOP 或写入方——回写的顺序、契约、判死封存只在 RA [`step9-writeback.md`](../wq-brain-ra-pipeline/references/step9-writeback.md)，写入由 MCP `upsert_*` 或 toolkit 幂等 CLI 执行；不改表达式、不提交（提交只经 `worldquant-submit-alpha` / `wq-brain-superalpha`，且须用户明确确认）；**不做 OS 表现监控与重着色**（BLUE → GREEN / YELLOW / RED）——目前**没有任何 skill / 工具承接**（旧 OS 回流脚本已归档，`alpha_properties.COLOR_*` 只是常量），RA step9 §9.8 已登记，**不要假设有人在做，也不要在报告里承诺**。
- **上游 / 下游**：上游 = 在跑的回测任务与 S5 落地（`worldquant-submit-alpha` / `wq-brain-superalpha`）；下游 = 复盘报告 + 台账（→ `wq-brain-campaign-matrix` 下次查表读到最新死路 / 胜绩，反哺 S-PRE）。

**铁律（DB 单轨）**：战役产物只写进 `data/wqb.db`（`wqb.store` / `mcp__wqb-db__*`）；`final_expressions.json` / `alpha_list.json` / `results/*.csv` 这类文件不当交接真相源，agent 不写它们。**运行态证据可读、但不是真相源**：checkpoint（ledger 键 `ckpt_w<wave>`）与 `batch_status.py` 的输出说明「现在跑到哪了」，**结果**以 `backtest_results` / `alphas` 为准。

## 1. 日常读什么，故障时才枚举进程

| 场景 | 做法 |
|---|---|
| **日常**（用户问「跑得怎么样」） | 进度 = checkpoint：`mcp__wqb-db__get_ledger_key region=$REGION key=ckpt_w$W`（`batches[]` 含 `multisim` / `status` / `submitted_at`）+ `$WQ_PY tools/batch_status.py --ids <multisim id …> [--watch]`（退出码 0 = 全部终态且无 error）；结果 = `mcp__wqb-db__list_alphas_by_wave` / `backtest_results` |
| **故障排查**（疑似卡住 / 进程失踪 / 找不到谁在写库） | 进程枚举——Linux：`ps -eo pid,etimes,args \| grep -E "pipeline.py\|batch_status.py\|harvest" \| grep -v grep`；Windows PowerShell：`Get-CimInstance Win32_Process \| Where-Object { $_.CommandLine -match 'pipeline\.py\|batch_status\.py' } \| Select-Object ProcessId, CreationDate, CommandLine` |

日常战役由 pipeline 托管；进程枚举**只在故障排查时**做，不是每次汇报的固定动作。

## 2. 判停与卡住（STALLED / TIMEOUT）

- **阈值只有一处**：`wqb.config.WAIT_THRESHOLDS`——`sim_stall_min`（progress 无变化即 `STALLED`）与 `sim_timeout_min`（总超时）；执行体是 toolkit `_lib/poller.py` 的 `DEFAULT_POLL`（区域 `thresholds.json` 的 `poll` 节可覆盖），两者相等由 `tests/unit/test_wait_thresholds.py` 守。**`STALLED` / `TIMEOUT` 即判停**，不等「看起来没动静」。
- 其它等待阈值（提交翻转、prod 相关性轮询等）同在 `WAIT_THRESHOLDS`；轮询退避参数见 toolkit [`poll-and-quota.md`](../wq-brain-campaign-toolkit/references/poll-and-quota.md)。
- **并发参数不在此复述**：只看 `config.CONCURRENCY` 与 [`wqb-concurrency`](../wqb-concurrency/SKILL.md) §8；本页也不下「瓶颈在信号发现还是吞吐」这类带时点的判断（那是复盘报告的结论，不是规则）。

## 3. ETA（强制章节，每次汇报不可省略）

**对每个在飞的 campaign wave 给一行**：`wave / 进度 done÷total / 预期完成 MM-DD HH:MM / 置信度`。

- **进度取证**：checkpoint 的 `batches[]`——每批只有 `submitted_at` 与终态 `status`（`RUNNING` / `COMPLETE` / `ERROR` / `SUBMIT_FAIL`），**没有完成时间戳**，所以用**吞吐法**：`total_batches = ceil(过闸表达式数 ÷ 单批条数)`（单批条数读 settings `_multi_sim_batch_size`，缺省 8）；`done` = 已到终态的批数；`rate = done ÷ (now − 最早 submitted_at)`；`ETA = now + (total_batches − done) ÷ rate`。这是粗估（七槽并行、批耗时不等）。
- **置信度**（经验值，未做标定）：已运行 < 30 min = 低，30–60 min = 中，> 60 min = 较高。
- **`done = 0`**（尚无完成批）→ ETA 写「未知：尚无完成批」，不编造。
- **与判停联动**：某 wave 无进度超过 `sim_stall_min` → ETA 一栏写「已挂起（STALLED）」并走上节判停，**不再报一个数**。
- **开放型任务**（没有固定总数）：报实时吞吐 +「至耗尽或手动停止」。**没有进度证据**的任务：标「未知」并写明原因，建议补进度记录。

## 4. 提交状态盘点（强制章节，每次汇报不可省略）

对每个候选给出**一行**，全部取自既有口径（不再另立分级）：

| 列 | 取自 |
|---|---|
| `alpha_id` / 所属 wave | `alphas` / `backtest_results` |
| IS 结论 | Failed RA（`config.compute_webdata_failed_counts`；`PENDING` = 暂无失败但**待复查**，不是通过）；只过廉价闸者写 `PASS_CHEAP` |
| prod 读数 | `alphas.prod_correlation` + `alphas.corr_checked_at`——**读数带时间**；prod 值会在一小时内漂移，提交前终验必须 `check_correlation(refresh=True)` |
| 稳健性 | ledger `robustness_<alpha_id>`（`get_ledger_key`）：`REJECT` 会让 `submit_verdict` 判 `BLOCKED` |
| `submit_verdict` 标签 | `SUBMITTABLE` / `BLOCKED` / `UNVERIFIABLE` / `ALREADY_SUBMITTED`（词义见 [GLOSSARY](../GLOSSARY.md)；`UNVERIFIABLE` **不是放行**） |

**三级分类**（映射到上表，不凭印象）：

- ✅ **已正式提交**：`alphas.status` 为 `ACTIVE` / `SUBMITTED`（平台核对过）。
- ✅ **待提交（仍须用户确认）**：在提交队列 SQL 表里——`$WQ_PY tools/submit_queue.py list --region $REGION`（默认只列 READY）。**注意**：ledger 键 `submit_ready`（达标缓冲池）与同名 SQL 表**不是同一物**，以 SQL 表为准；且 `submit_verdict ≠ BLOCKED`、Failed RA = 0、prod 读数按 D0-P 可放行。
- 🔶 **仍需验证**：其余全部（含只过廉价闸的 `PASS_CHEAP`）。

**结论句式**（可检）：「N 个候选：a 已提交，b 待提交（须用户确认），c 仍需验证」。**绝不称 `PASS_CHEAP` 为「可提交」**——报告里这类候选标「研究仿真 IS 闸通过、提交未验证」。

## 5. 复盘报告骨架（编号用 R1–R4，避免与本 skill 章节号混淆）

所有「盯回测 / 看进度 / 盘点」类报告用同一个四层骨架，不遗漏 §3 ETA 与 §4 提交状态盘点：

- **R1 背景**：任务范围、账号 / 区域、时间窗。
- **R2 分析维度**：进度与 ETA（§3）/ 漏斗（`tools/step_funnel.py`）/ 提交状态盘点（§4）/ 失败归因。
- **R3 核心发现**：汇总 → 分维 → 全局 → 逐项核查。
- **R4 结论与建议**：结论先行 / 问题 / 行动 / 风险。

报告用通用工具（Read / Bash / Grep / Glob）生成，写在回复里或用户项目的 `reports/`；**修改报告骨架前先与用户确认**。填好的样例见 [`references/scenarios.md`](references/scenarios.md)。

## 6. S6 台账回写：触发并核验（写入 SOP 只在 RA 步 9）

复盘报告产出后，**触发** RA 步 9 的有序流程（[`step9-writeback.md`](../wq-brain-ra-pipeline/references/step9-writeback.md) §9.1：漏斗 → verdict → 点塔 → `upsert_wave_result` → 判死 / 胜绩 → 饱和 → 数据集经验 → 刷新先验快照），**核验**其完成定义（§9.7）。`wave_results.verdict` 为空的记录**不算复盘完成**——枚举 `PASS` / `FAIL` / `PARTIAL`，判定表见 §9.3（不要在这里另写一份）。

**核验命令**：`mcp__wqb-db__get_wave_result region=$REGION wave_number=$W`，`verdict` 必须非空。

**写失败怎么办**：返回 `error` / 被拒（verdict 不是枚举、`closed` 没带 verdict）→ 按返回里的 `suggestion` 核对后**显式传枚举**重试一次；仍失败 → 改用下面的无 MCP 逃生阀（同一个写入函数，见 INDEX「共享产物归属表」），并把失败原因报告给用户——**不得静默跳过**，也不得把「报告写好了」当成「已回写」。

**无 MCP 的逃生阀**（toolkit 幂等 CLI；先 `--dry-run` 校验，确认后去掉它再写；`$WQ_TOOLKIT_DIR` = `Claude/skills/wq-brain-campaign-toolkit/scripts`）：

```bash
CD=tracking/$REGION
$WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD wave upsert --wave $W --verdict PARTIAL --finding "<一条 key_finding>" --dry-run
$WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-dead-end --id <ID> --family <族> --reason "<原因>" --rule "<规则>" --dry-run
$WQ_PY $WQ_TOOLKIT_DIR/campaign.py --campaign-dir $CD registry add-win --id <ID> --what "<信号概念>" --key "<设置与骨架>" --dry-run
```

`wave upsert` 的 `--finding` 可重复；`--candidates` / `--batches` / `--extra` 的 JSON 走 `@file`（中文 / JSON 参数一律走文件通道，AGENTS.md §5），临时文件写在会话 scratchpad，用完删除。**不要**再写 `wave<N>_verdict` / `s6_verdict_<wave>` 这类旧键（`ledger set-verdict` 写的就是它，已废止）：结论只有 `wave_results.verdict` 一个来源。

**方法论规则计数由代码自动完成，不要手工回写**：`times_applied` 在 `gate.py` 消费契约与 `pipeline.py` 校验 universe 杠杆时递增，`times_succeeded` / `confidence` 在 `pipeline.py` 收批评审后由 `validate_rules` 更新（规则存于 ledger 键 `methodology_rules`）——手工再 +1 会重复计数。

**写入路径的归属**：波级 = `wave_results`，数据集层 = `registry_empirical`，其余 ledger 键各有登记的写入方与读取方，见 [`docs/ledger_keys.json`](docs/ledger_keys.json)（本 skill 不新增键）。

## 7. 工作纪律

1. **label 碰撞**：用完整字段名，别截断成同名覆盖。
2. **断点续跑**：只把拿到 pid（有 multisim / alpha id）的确定结果算「已完成」。
3. **universe 合法性取 `wqb.config.REGIONS[region]['universes']`**，不凭记忆判（各区档位不同，如 EUR 默认 `TOP2500`）；非法档位平台回 400。
4. **止损 / 转向不在此定义**：区域 / 波次级停止规则见 RA [`loop-and-stop.md`](../wq-brain-ra-pipeline/references/loop-and-stop.md)，单 alpha 改进的止损见 `wq-brain-alpha-optimization-v1`。
5. **红线**：`status = RUNNING` 的战役，其 checkpoint（ledger `ckpt_w<W>`）与运行脚本**不得修改、移动、删除**。
6. **新监控脚本**放 `tools/`：头部 docstring 含 用法 / 退出码 / 运行环境 三段，`import _pyenv` 接入 venv（参照 `tools/batch_status.py`），**只读**，并补单测。用户自己的 `scan_*.py` 与平台 `results/` 数据不归类、原地保留。

情景卡（日常一波收尾 / 挂起处置 / 汇报样例）见 [`references/scenarios.md`](references/scenarios.md)。
