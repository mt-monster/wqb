# attic/ 归档清理评估报告

**日期**：2026-09-28  
**范围**：`attic/`（隔离归档区，AGENTS.md 定义为"只读归档，勿回迁进活跃代码"）  
**方法**：目录体积/类型/时间剖面 + `git status` 对账 + 与活跃树差异比对（diff/find）+ 测试引用扫描（`grep attic`）

---

## 一、结论先行

`attic/` 总量 **18 MB / 1053 文件**，由 6 个**带日期戳**的子目录构成。经逐项目核查：

- **3 个目录必须保留**（含测试锁定项、已删代码的唯一副本、当日安全备份）；
- **3 个目录为低价值运营/快照归档**，可清理（合计约 **2.9 MB**，占总量 ~16%，功能零风险）。

**重要更正**：初步扫描曾误判 `toolkit_zero_ref_20260928/` 为"活跃代码的冗余副本"。实测 `git status` 显示这 7 个脚本已从活跃树删除（`D`），attic 副本是**唯一留存**，故必须保留。

---

## 二、总览

| 子目录 | 文件数 | 体积 | 日期 | 性质 |
|---|---|---|---|---|
| `wip_20260928/` | 550 | 15 MB | 09-28 | 当日 git WIP 安全备份（patch + untracked 全量） |
| `async_tasks_20260925/` | 479 | 2.7 MB | 09-25 | `tools/cleanup_async_tasks.py` 归档的超龄异步任务运行日志 |
| `toolkit_zero_ref_20260928/` | 7 | 72 KB | 09-28 | 7 个已从活跃树移除的工具脚本唯一副本 |
| `experience_output_path_20260924/` | 12 | 112 KB | 09-24 | 经验挖掘工具跨 4 host 生成的 markdown 输出 |
| `ra_pipeline_shell_20260928/` | 4 | 68 KB | 09-28 | 3 个 shell/runner 脚本的旧版快照（与活跃版 DIFFERS） |
| `step_metrics_20260917/` | 1 | 4 KB | 09-17 | 已下线的 step_metrics 节点归档（含 README 决策留痕） |

---

## 三、逐项分析

### 🟢 保留（不可删）

**1. `step_metrics_20260917/`** — *测试锁定*
- `tests/unit/test_step_funnel_p5.py` 显式断言 `os.path.isdir(attic/step_metrics_20260917)` 且 `README.md` 存在；`registry.py`/`wqb_db_mcp.py` 亦注释指向其复活步骤。
- 删除将导致单测失败且丢失节点下线决策留痕。**保留。**

**2. `toolkit_zero_ref_20260928/`** — *已删代码的唯一副本*
- 含 `budget_planner / campaign_mutex / composition_validator / distill_experience / family_atlas / os_feedback / signal_classifier` 共 7 个 `.py`。
- `git status --short` 显示这 7 个文件在活跃 `campaign-toolkit/scripts/` 下均为 `D`（已删除，未提交）。活跃树其余位置（含 `.venv` 内打包副本）亦无同名校验版本。
- 即：attic 副本是当前**唯一**留存，正是归档区的本职。**保留。**（如后续确认这些脚本确属应删死代码，可连同 attic 一并处理，但须经你明确裁决。）

**3. `wip_20260928/`** — *当日安全备份*
- 今日强制 git 同步前的 WIP 备份：`wip_tracked.patch`（206 文件差异，`git apply -R` 可还原）、`untracked/`（328 项未跟踪全量复制）、`STATUS.txt`、`RESUME.md`。
- 是今日 sync 的回滚锚点。建议**至少保留至确认同步稳定后**再议清理。注：内含一个异常文件 `untracked/-`（3.4 MB，文件名即 `-`），为备份时的边角产物，不影响备份可用性。

### 🟡 建议清理（低价值 / 可重生成，功能零风险）

**4. `async_tasks_20260925/`** — 2.7 MB / 479 文件
- 内容：异步任务（如 `batch_track_EUR_*`）的 `meta.json` / `stdout.log` / `stderr.log` / `*.out` / `*.err` 运行日志，对应 2026-09-17 前后的历史运行。
- 性质：`tools/cleanup_async_tasks.py` 按"归档而非删除"约定落入此处。**无任何活跃代码或测试引用**。
- 风险：撤销此归档会偏离该工具的"archive not delete"设计约定；但删除本身不影响功能。清理前请确认不再需要回溯这些历史运行日志。

**5. `experience_output_path_20260924/`** — 112 KB / 12 文件
- 内容：经验挖掘工具对 `eur_fundamental23 / eur_news46 / eur_news50` 跨 `claude/codex/repository/workbuddy` 4 个 host 生成的 markdown（各 3 份 = 12）。
- 性质：工具可重生成的输出产物，非源码。**无引用**。
- 清理安全，仅丢失一份 09-24 的跨 host 对比快照。

**6. `ra_pipeline_shell_20260928/`** — 68 KB / 4 文件
- 内容：`dataset_health_check.py` `ralph_daily_loop.py` `ralph_runner.py` `daily_state.template.json`。
- 性质：经 diff，**三者均与活跃版本不同**（活跃版位于 `wq-brain-ppa-mining/scripts/` 及 `.venv` 内打包副本，且内容有差异）→ 此处为**旧版快照**。
- 清理安全（活跃新版已存在）；仅当你需要保留旧版变体时才保留。

---

## 四、待确认清理清单（合计约 2.9 MB）

| 目录 | 体积 | 原因 | 影响 |
|---|---|---|---|
| `attic/async_tasks_20260925/` | 2.7 MB | 历史异步任务运行日志，无引用，可重生成 | 零（偏离 cleanup 工具约定，但功能无影响） |
| `attic/experience_output_path_20260924/` | 112 KB | 工具可重生成输出，无引用 | 零 |
| `attic/ra_pipeline_shell_20260928/` | 68 KB | 活跃脚本的旧版快照（DIFFERS），无引用 | 零（仅失旧版变体） |

> 不选入清理：`step_metrics_20260917/`（测试锁定）、`toolkit_zero_ref_20260928/`（已删代码唯一副本）、`wip_20260928/`（当日备份，建议稳定后再议）。

---

## 五、建议执行方式

- 清理项均为"归档而非生产依赖"，删除不影响任何测试或运行（已扫描确认无活跃引用）。
- 仍建议按你的偏好**先移入回收站（可恢复）**再观察，而非硬删除。
- `step_metrics` 与 `toolkit_zero_ref` 两项**切勿删除**——前者破测试，后者丢代码。
- 执行后建议跑 `pytest -q` 复验（主要守护 `test_step_funnel_p5.py` 仍绿）。

---

## 六、附带发现（非本次清理范围，供你知悉）

- `git status` 显示 `campaign-toolkit/scripts/` 下 7 个脚本（即 attic `toolkit_zero_ref` 那 7 个）处于**未提交删除（`D`）**状态。这是今日强制 git 同步后的工作树状态，与 attic 归档相互独立。若这些脚本是误删，attic 副本可随时回迁；若确属下线，建议把 attic 视为其正式归宿。是否与"清理"相关由你裁定。
