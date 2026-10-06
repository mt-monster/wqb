# 分支与抢救点策略（branch policy）

> 建立：2026-10-06 ｜ 依据：本仓库 2026-09 至 10 月连续两次资产损失事故的复盘
> 相关工具：`tools/code-audit/repo_governance_check.py`（先行指标）、`tools/audit_structure.py`（结构契约）

## 0. 第一条铁律

**在本仓库不要运行 `git clean -fd`（以及 `git checkout .` / `git reset --hard`
这类会丢弃工作区的命令）。**

原因不是"习惯了危险操作"，而是本仓库曾长期存在**只以未跟踪文件形式存在的源码**：

| 事故 | 丢失物 | 事后实证 |
|---|---|---|
| 2026-10 清理 | `tools/` 下 17 个被 AGENTS.md / tools/README.md / MEMORY 引用的工具 | 清理后 `tools/*.py` = 142，S11 基线要求 159；`git ls-files` 命中 0，从未入库 |
| 同期 | `docs/experience/02_signal_patterns.md` 的 §10–§16 + `methodology_rules.json` 的 7 条规则 | HEAD 版仅 9 节；而已提交的 CHANGELOG 引用「§14」、`optimization-v1/SKILL.md` 引用「§12」 |

两起事故的**共同前兆是同一个数字**：未跟踪的源码类文件数 > 0。
`repo_governance_check.py` 就是把这个数字变成可执行的检查（退出码 1 = 有未跟踪源码）。

> 2026-10-06 起，该数字已归零并入库（commit `08c026b` … `dc18a1a`）。
> 在它持续为 0 之前，铁律不免除。

## 1. 分支模型

- **`main` 是唯一长期分支**，也是唯一有意义的提交目标。
- **`wip/<date>-<topic>`**：短期工作分支，约定**当日合并或当日删除**；不允许长期滞留。
  长期滞留的 wip 分支会被误当成"已合并"而删掉，其上未合入的内容随之只能在
  `git fsck` 里考古。
- **`preserve/*` tag**：抢救点，**永久保留、永不合并**。语义是"这是某时刻工作区的
  快照，供日后取件用"，不是一条开发线。

## 2. 现有抢救点（8 个，全部为 annotated tag）

| tag | commit | 内容 |
|---|---|---|
| `preserve/snap-worktree-1006` | `70c6331` | 2026-10-06 工作区快照 |
| `preserve/snap-worktree-1006b` | `8f171d9` | 同上，晚一版 |
| `preserve/wip-DANGER-restore-1006-0056-gutted` | `22a8e4a` | 事故后受控快照（tracked 侧） |
| `preserve/wip-DANGER-restore-1006-0056-gutted-untracked` | `05b64a6` | 同上（untracked 侧） |
| `preserve/wip-cline-restore-1005-1929` | `ce8358c` | cline 会话抢救；**含完整 16 节经验库与 24 条机器规则** |
| `preserve/wip-cline-restore-1005-1929-untracked` | `4910e65` | **含 17 个已恢复工具 + 大量未跟踪产物** |
| `preserve/wip-cline-restore-1006-0023` | `6232801` | 同期另一版 |
| `preserve/wip-cline-restore-1006-0023-untracked` | `07719c9` | 同期另一版（untracked 侧） |

保留这些 tag 的实质意义：**它们是唯一持有那批未入库内容的对象根**。
删 tag 等于让对应 blob 进入可被 `git gc` 回收的状态。

### 取件方法

```bash
# 列某个抢救点里的文件
git ls-tree -r --name-only preserve/wip-cline-restore-1005-1929 | head

# 看某文件内容
git show preserve/wip-cline-restore-1005-1929:docs/experience/02_signal_patterns.md

# 与当前 main 比较「谁是谁的子集」（判断是否纯追加、可安全恢复）
git diff --numstat main preserve/wip-cline-restore-1005-1929 -- <path>
```

**取件纪律**：恢复前先用 `git diff --numstat` 确认方向。
`deleted=0` 表示"快照 = main + 追加"，恢复不可能覆盖现有内容（本次 §10–§16 即按此判据恢复）。
若 `deleted>0`，那就是**分叉**而不是损失，必须逐文件判断，禁止整体 checkout。

## 3. 两个 `wip/DANGER-*` 分支

`wip/DANGER-restore-1006-0056-gutted`（`22a8e4a`）与
`wip/DANGER-restore-1006-0056-gutted-untracked`（`05b64a6`）**故意保留为分支**：

- 分支名里的 `DANGER` 是给未来的自己看的警告：这批内容处于"被清空/半清空"状态。
- **永不合并进 `main`**。它们的作用是"把损坏现场原样冻住"，便于日后比对
  "到底哪些东西曾经存在过"。
- 它们与 `preserve/*` tag 指向同一 commit，tag 是保险，分支是路牌。

## 4. 卫生检查

```bash
python tools/code-audit/repo_governance_check.py          # 人类可读
python tools/code-audit/repo_governance_check.py --quiet  # 只看退出码（可进 CI）
```

输出四类读数：
1. **未跟踪源码类文件数**（唯一先行指标，应为 0）；
2. 被 gitignore 排除的源码类文件数（设计内排除，但**若含结论/报告类即为隐患**）；
3. 相对各远端的 ahead/behind（领先未推送 = 只在本地存在）；
4. 抢救点与 DANGER 分支是否安在。

> 已实证的第 2 类隐患：`tracking/.gitignore` 曾整目录忽略 `DEU/reports/`、
> `DEU/scripts/` 与 `USA/reports/*.md`，使这两个区域的报告**永久落不了库**。
> 2026-10-06 已改为与其它区域同口径（只忽略 `tmp_` / `archive`）。

## 5. 尚未处理 / 已裁决

### 5.1 远端同步

- `origin/main`：**已同步**。2026-10-06 推送了 P2/P3 两个提交（`0a89cbe..4bf3bab`，
  共 30 个文件）。此前的缺口（落后 5 个提交）已清零。
- `gitcode/main`：仍落后本地 `main` **109 个提交**。**用户明确指示"先不管"**，
  故本文件不再把它列为待办；推送是外发动作，需用户再次明确指令。

### 5.2 `git gc --prune=now` —— 判定不安全，不执行

本机同时存在 cline（`refs/cline/checkpoints/*`）与 codex（`refs/codex/turn-diffs/*`）
的 ref 命名空间，且有正在运行的回测/选区进程（含另一个工作副本 `D:/coding/hw_project/wqb`）。
在这些 ref 与进程存在期间做 prune，可能回收掉**只被这些 ref 引用**的 blob。
保持现状；若要清理，须先确认上述 ref 命名空间与并行进程都已停止。

### 5.3 抢救点比对：6 个"可恢复"文件的**终局裁决 —— 不回迁**

抢救点 `4910e65` 内仍可 `git checkout` 取回以下 6 件（此前列为"待人工决策"）。
2026-10-06 逐件核验后**裁决：全部不回迁**。

**核验方法与结论**

| 文件 | 活动引用核验 | 裁决依据 |
|---|---|---|
| `tools/direct_submit.py`（已丢失） | 全仓只命中我自己的治理文档 | ① `tools/wave_gate.py`·`quality_predict.py` 里的 `direct_submit` 是 `qp_summary["direct_submit"]` **计数字段键**，不是该脚本；② `DIRECT_CONNECT_WHITELIST`（7 项，`test_db_write_guards.py::test_whitelist_files_exist` 断言必须存在）**不含它**；③ 提交链已被 MCP `workflow_submit_alpha` + `tools/super_build.py submit` 覆盖 |
| `tools/harvest_batch.py`（已丢失） | 同上 | `pipeline.py` 里的 `_harvest_batch_alphas` 是**本地函数**（非该脚本）；收批已统一走 `tools/harvest_multisim.py`（支持多 multisim 批量收） |
| `tools/self_batch.py`（已丢失） | 同上 | 零活动引用；self 侧走 MCP `check_self_correlation` 与 `brain-calculate-alpha-selfcorr-quick` |
| `tools/harvest_by_expr.py`（已丢失） | 同上 | 零活动引用；按表达式收批的需求已由 `harvest_multisim` 覆盖 |
| `tools/eu_field_coverage.py`（已丢失） | 仅历史报告引用 | 活文档 `wq-brain-ra-pipeline/references/ppa-mining-experience.md` 已明写**前者不存在**；`reports/` 里的引用是**时点记录**（描述当时存在过什么），不是待办 |
| `tools/gate.py`（已丢失） | 无 | `AGENTS.md` L363 早已标注「代码零引用的遗留文件（**已归档**）」；表达式预检职责由 `wqb.expression.op_arity.ensure_safe_for_dispatch` 与 `tools/code-audit/*` 承接 |

**不回迁的第二重理由（工程侧）**：`tools/` 顶层有 S11 硬闸「只减不增」，基线 159 项
**不含**这些文件 —— 从抢救点 checkout 回 `tools/` 顶层会把基线顶爆（新增即 FAIL）。
要解就得"恢复即重冻基线"，而重冻基线等于给一个零引用文件发永久通行证，**收益为负**。

**若将来确实需要**：正确路径是**在主题子目录里新写一个工具**（如
`tools/verdict/` / `tools/ledger/`），而不是从抢救点把旧文件 checkout 回 `tools/` 顶层。
抢救点 `4910e65` 保留不动，作为"曾存在过什么"的唯一证据。

> ⚠ 连带影响：`MEMORY.md §4` 与部分 skill 里指向 `direct_submit.py` /
> `harvest_batch.py` / `self_batch.py` / `harvest_by_expr.py` 的命令**都已失效**，
> 勿照抄执行 —— MEMORY 侧已于 2026-10-06 改指真实通道（`tools/harvest_multisim.py`）。

