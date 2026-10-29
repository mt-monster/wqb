---
last_verified: 2026-10-29
name: wqb-test-failure-triage
description: "wqb 工作区 pytest 失败的分簇诊断纪律与固化检查表。当用户说'测试红了 / 全量回归有失败 / 这 N 个失败怎么解决 / 修复测试 / pytest 失败'或跑完 pytest 看到非全绿时触发。提供 7 步诊断顺序（完整 traceback → 根因聚类 → 端到端最小复现 → 区分期望过时 vs 代码回归 → 查状态文件 → 新失败定性 → 沉淀固化）、workflow 节点四处同步审计、漂移类型速查表（skills 安装位 / INDEX 计数 / NodeMeta 签名 / 状态文件陈旧 / ledger 白名单契约），并防把生产 bug 当测试过时改掉。"
layer: L7
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Edit
version: "1.0"
agent_created: true
---

# wqb 测试失败分簇诊断

## 职责边界

- **本 skill 负责**：pytest 红了之后的**诊断顺序与根因定性** —— 取完整 traceback、按根因聚类、端到端最小复现、判断是「期望过时」还是「代码回归」。
- **本 skill 不做**：改业务代码修 bug（那属于具体模块的修复任务）；改 skill 文档合同（→ `CONTRACT.md` + 本仓 `tests/unit/07_docs_skills/`）；平台侧闸门判定（→ `submit_verdict` / [`brain-how-to-pass-alpha-test`](../brain-how-to-pass-alpha-test/SKILL.md)）。
- **上游 / 下游**：上游 = 任意一次 pytest 结果（本地或 CI）；下游 = 定位到具体模块后交回该模块的修复任务，并把同类漂移固化成守护测试。

> 来源：2026-09-18 一次"7 个既有失败全清零"的实战。当时 7 个失败聚成 5 个根因，
> 其中 **1 个是真实生产 bug** —— 若按"测试期望过时"改掉断言，会把
> `build_wave.py` 族类配额静默截断开波永久埋掉。

## 0. 铁律

**先复现，再断言。** 任何"看起来像测试写错了"的失败，都必须先做端到端最小复现，
用真实行为对照断言。**只改测试期望是最危险的修复方式** —— 它会静默吞掉生产 bug。

## 1. 七步诊断顺序

| # | 步骤 | 动作 | 反模式 |
|---|---|---|---|
| 1 | 取完整 traceback | `pytest <file> -q --tb=long`（或 `--tb=short`） | 只看 `-q` 汇总行就动手 |
| 2 | 根因聚类 | 把失败按根因分组，一组一修 | 逐条修（7 个失败常只有 3–4 个根因） |
| 3 | ★ **端到端最小复现** | 写最小脚本跑真实代码路径，打印真实输出 | **直接改断言期望值** |
| 4 | 定性 | 复现结果 ≠ 断言 → 先假设**代码**有问题；复现结果 == 断言但与新契约不符 → 改测试 | 默认"测试过时" |
| 5 | 查状态文件 | 带 checkpoint/续跑的工具，先看状态文件是否陈旧 | 反复重跑同一命令 |
| 6 | 新失败定性 | 回归中冒出的新失败先确认是否自己引入（`git stash` 对照 / env 相关） | 全部当成自己改坏的 |
| 7 | 沉淀固化 | 同类漂移出现第二次 → 写工具或测试机械拦住 | 靠人记 |

## 2. 最小复现模板（第 3 步）

不要读代码猜，直接跑出真实行为。以 `build_wave.py` 为例（当时就这样抓到的）：

```python
# 临时脚本 OK（logs/_tmp_*.py），完成即删
import subprocess, tempfile, json, re
from pathlib import Path
# 1) 临时库 + 最小战役目录  2) 造 N 条同质候选
# 3) 跑真脚本（子进程，隔离 env）  4) 打印真实产物
for size in (3, 6, 12):
    r = subprocess.run([...'--size', str(size)...], capture_output=True, text=True, env=env)
    print(f'--size {size}: selected={re.search(r"\"selected\": (\d+)", r.stdout).group(1)}')
# 期望 <= size；实测恒为 2 → 暴露真实 bug
```

**判据**：若真实输出**与断言差了一个系统性偏差**（如恒为 2 而非随参数变化），
就是代码 bug，不是测试过时。

## 3. 已知漂移类型速查表（2026-09-18 实测）

| 类型 | 症状 | 修复 |
|---|---|---|
| **workflow 节点登记缺失** | 3 个测试同时红（test_workflow / skill_integrity×2） | `python tools/audit_node_registration.py` 列全部缺口 |
| **skills 安装位漂移** | `test_sync_skills_reports_no_drift` + `test_toolkit_copies_in_sync` 红 | `python tools/sync_skills.py`（仓库=源，安装位=派生物） |
| **INDEX 计数漂移** | `test_mcp_tool_counts_match_index` 红 | 同步 `Claude/skills/INDEX.md` 基准段（workflow 节点数 / wqb-db 工具数） |
| **NodeMeta 签名漂移** | `test_registry_meta_matches_node_signature` 红，报 sig vs meta 差异 | 补 `registry.py` 的 `optional_params`（含 `_context`/`dry_run` 除外） |
| **状态文件陈旧** | 工具报「[续跑] 已完成，跳过」但实际没改 | 加 `--fresh`（必要时 `--apply --db-backup`） |
| **ledger 白名单契约漂移** | `test_real_db_no_schema_drift` 红 | `tools/normalize_ledger_whitelist.py --region X --fresh --apply --db-backup` |

## 4. workflow 节点四处同步（最常踩）

新增/修改 workflow 节点时必须同步**四处**，漏一处测试即红：

| # | 位置 | 改什么 |
|---|---|---|
| ① | `src/wqb/workflow/registry.py` | `register()` + `NodeMeta`；`required_params`/`optional_params` 与 `run()` 签名逐字一致（`_context`/`dry_run` 除外） |
| ② | `tests/unit/test_workflow.py` | `test_registry_lists_all_core_nodes` 期望节点集合 |
| ③ | `tests/unit/test_skill_integrity.py` | `_DRY_RUN_CASES` 干跑用例表 |
| ④ | `Claude/skills/INDEX.md` | workflow 节点计数 |

一次跑完：`python tools/audit_node_registration.py`（退出码 1 = 有漂移并列出全部缺口）。
守护测试：`tests/unit/test_docs_consistency.py::test_node_registration_audit_is_clean`。

## 5. 收尾清单

```bash
python -m pytest tests/ -q --tb=line -p no:cacheprovider   # 必须全绿
$WQ_PY tools/sync_skills.py --check                        # 全安装位一致
$WQ_PY tools/audit_node_registration.py                    # 节点四处一致
```

- 改了 skill → **必须**跑 `python tools/sync_skills.py`（运行时按安装位加载，只改仓库=没改）。
- 修完在 `.workbuddy/memory/YYYY-MM-DD.md` 记：根因分类 + 哪个是真实 bug + 复现命令。
- 同类漂移第二次出现 → 按第 7 步写成工具/测试，别靠人记。
