# 未跟踪文件白名单（untracked allowlist）

> 建立：2026-10-06 ｜ 执行者：`tools/code-audit/repo_governance_check.py`
> 上位文档：[`branch_policy.md`](branch_policy.md) §0 铁律
>
> ⚠ **本节 §1 的表与代码常量 `EXPECTED_UNTRACKED_PREFIXES` 是逐条对齐的双轨**（2026-10-06 接上线）：
> 以前文档自述「执行者 = 本脚本」而代码里那个常量声明后从未被使用（`= ()`），两边已分叉
> ——代码多 `outputs`、文档多 `.claude/.codex/.cline`。现在对齐由
> `tests/unit/07_docs_skills/test_governance_gates_selfcheck.py` 机械守护：**改一边不改另一边即红**。
> 代码侧是**可执行投影**（单一事实源），本节是给人看的说明。

## 判据只有一句话

**凡是"重跑能再得到"的，可以不入库；凡是"人的判断与结论"的，必须入库。**

前者是运行产物，后者是资产。事故从来不是丢了中间产物，而是丢了结论、脚本与规则。

## 1. 允许长期未跟踪（运行产物 / 外部数据）

| 路径 | 性质 |
|---|---|
| `logs/` | 日志、异步任务输出、测试 XML |
| `cache/` | 断点、中间 JSON |
| `results/` | checkpoint（注意：被多个 `backfill_*` / `batch_*` 脚本硬编码引用，**不可移动**） |
| `data/` | `wqb.db` 及备份（**含真实持仓/alpha 数据，绝不入库**） |
| `attic/` | 日期化归档包（只读） |
| `research-data/` | 外部数据包（`operators_platform_*.json` 被 `op_arity.py` 读取，整目录不可动） |
| `extensions/` | 浏览器扩展源 |
| `selfcorr_quick_out/` | 相关性快筛缓存（pickle/xlsx） |
| `outputs/` | 工具默认输出目录（与 `output_report/` **不是同一个**：后者受控入库） |
| `.claude/` | skill 安装位镜像（仓库内手工镜像，由 `tools/sync_skills.py` 单向生成） |
| `.codex/` | skill 安装位镜像（同上） |
| `.cline/` | skill 安装位镜像（同上） |
| `.agents/` | skill 安装位镜像（同上） |

## 2. 明确禁止未跟踪（源码 / 结论）

- `src/`、`tests/`、`tools/`、`Claude/` 下的任何 `.py` / `.md` / `.json`
- `docs/`、`reports/`、`output_report/` 下的任何文档
- `tracking/**/scripts/*.py`（区域战役脚本）与 `tracking/**/reports/*.md`（区域结论）
- `AGENTS.md` / `README.md` / `.mailmap` 等根级治理文件

违反的后果是可预测的：**下一次清理就把它们带走**，而且事后无法从 git 找回
（`git log --diff-filter=D` 查不到，因为它们从未进入任何 commit）。

## 3. 设计内被 gitignore 的例外（不是缺陷）

以下"被忽略的源码类文件"是**有意**排除的，不计入隐患：

- `tracking/*/reference/*.json` —— 字段体检/互相关探针等**数据转储**（可重跑）
- `tracking/**/candidates/` —— 候选波次 JSON（可重跑）
- `tracking/**/scripts/tmp_*.py`、`tracking/**/scripts/archive/` —— 草稿与归档
- `attic/` 全部 —— 归档

⚠ 但"整目录忽略"是危险模式：它会把**结论类**文件一起挡在库外。
已发生的实例：`tracking/.gitignore` 里 `DEU/reports/` + `DEU/scripts/` +
`USA/reports/*.md` 三行整目录忽略，导致两个区域的报告永久无法入库。
2026-10-06 已收敛为与其它区域同口径（只忽略 `tmp_` / `archive`），
`repo_governance_check.py` 的"被忽略源码类文件"一栏就是为发现这类模式而设。

## 4. 判定流程

新增一个文件后，只问一个问题：

```
它会因为清理而消失吗？   → 会 → 必须入库（或显式写进本文件的第 3 节）
                       → 不会（在 logs/ cache/ … 下）→ 可以不入库
```

拿不准时跑：

```bash
python tools/code-audit/repo_governance_check.py
```

**先行指标 = 未跟踪的源码类文件数。它应当是 0。**
不是 0 时不要放着不管——它此刻就是"下次清理的损失清单"。
