# 分支与抢救点策略（branch policy）

> 建立：2026-10-06 ｜ 依据：本仓库 2026-09 至 10 月连续两次资产损失事故的复盘
> 相关工具：`tools/code-audit/repo_governance_check.py`（先行指标）、`tools/audit_structure.py`（结构契约）、
> `tools/code-audit/snapshot_adjudicate.py`（抢救点独有文件的三态裁决台账）
>
> ⚠ **本文件不复制会漂移的计数**（基线项数、远端落后提交数、快照缺文件数）。
> 2026-10-06 实测：写死的 `109`（gitcode 落后）落盘当天就变成 `112`；「398 个跟踪文件被抹」
> 实测是 `402`；S11 基线在 AGENTS.md 写 `171`、本文写 `159`。取数一律现跑：
> `python tools/code-audit/repo_governance_check.py`、`python tools/audit_structure.py --only s11`。

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
  ⚠ 例外只在本文 §3 逐条登记：违反「当日删除」而故意保留的分支必须在这里写明理由，
  否则它就是下一个会话眼里的「可以删」（已发生过：`wip/DANGER-*` 违反了本约定，
  却被 §3 追认成「故意保留」——追认可以，但不得反过来拿追认当「约定本来就有例外」）。
- **`preserve/*` tag**：抢救点，**永久保留、永不合并**。语义是"这是某时刻工作区的
  快照，供日后取件用"，不是一条开发线。

### 1.1 「永久保留」的物理定义（2026-10-06 新增，硬约定）

**任何称「永久保留」的 ref，必须同时存在于 ≥ 2 个介质**，否则这个说法不成立。

理由：本文 §2 自己写明这些 tag 是「唯一持有那批未入库内容的对象根」、删 tag 等于
让 blob 进入可被 `git gc` 回收的状态；而实测 `git ls-remote --tags origin` **为空**，
远端只有 `main` 一条 ref —— 即全部抢救内容与「已裁决放弃的内容」共用**一台机器一块盘**，
而这棵树历史上已被抹过两次。

落地手段（二选一并常备）：

```powershell
# ① 本地冷备：单文件包含全部分支与 tag，可在新目录 clone 回来
git bundle create "$env:USERPROFILE\wqb_backups\wqb-preserve-<YYYYMMDD>.bundle" --tags --branches
git bundle verify "$env:USERPROFILE\wqb_backups\wqb-preserve-<YYYYMMDD>.bundle"

# ② 外发（属外发动作，每次都要用户明确确认）
git push origin --tags
```

§4 的读数会把「相对各远端的 ahead」与「preserve tag 个数」一起打出来；
**ahead > 0 就是「永久保留」目前只在单介质上**。

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

### 2.1 抢救点里到底有什么（已变成可读数的台账）

「对象库里有、`main` 没有」的文件不再靠人临时比 `ls-tree`（历史上正是这么漏掉
`src/wqb/semantic_ledger.py` 这种可取回件的）：

```powershell
python tools/code-audit/repo_governance_check.py          # 读数：★ 抢救点独有源码 N 个
python tools/code-audit/snapshot_adjudicate.py --check    # 台账是否仍与对象库一致
python tools/code-audit/snapshot_adjudicate.py --apply    # 改完 fixture 重生正文
```

逐件三态裁决（`RESTORED` / `DROPPED` / `ARTIFACT` / `PENDING`）在
[`snapshot_adjudication.md`](snapshot_adjudication.md)（生成物）；人工唯一入口是
`tests/fixtures/snapshot_adjudication.json`，**判 `DROPPED` 不写依据会被工具直接拒**。
`PENDING` 非零 = 欠债可见，不允许伪装成「已收尾」。

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

## 3. 两个 `wip/DANGER-*` 分支（逐条裁决，2026-10-06）

`wip/DANGER-restore-1006-0056-gutted`（`22a8e4a`）与
`wip/DANGER-restore-1006-0056-gutted-untracked`（`05b64a6`）**故意保留**（即 §1「当日删除」
的显式例外）：

- 分支名里的 `DANGER` 是给未来的自己看的警告：这批内容处于"被清空/半清空"状态。
- **永不合并进 `main`**。它们的作用是"把损坏现场原样冻住"，便于日后比对
  "到底哪些东西曾经存在过"。
- 它们与 `preserve/*` tag 指向同一 commit，tag 是保险，分支是路牌。

2026-10-06 逐件定级（不再笼统写「都留着」）：

| ref | 内容实测 | 裁决 |
|---|---|---|
| `22a8e4a`（tracked 侧） | 相对 `main` = 630 files / +5159 / −94689；`Claude/skills` 只剩 32 个 vs main 434（**差 402**，而分支说明写的「398」本身就是漂的数）——对 `main` 是「纯损坏 + 分叉旧版」 | 取证价值**低于** untracked 侧。完成 §1.1 的双介质备份后可**降为 tag-only**（删分支留 tag = 对象不丢、路牌变少）。本轮**未删**：删 ref 是不可逆动作，等用户点头 |
| `05b64a6`（untracked 侧） | 只 4 件，其中 `tests/unit/01_store_db/test_corr_single_source.py` **不在 main** | **必留**。但该测试断言的是 `_corr_cache.py` 的第三版契约（`CORR_FRESH_SECONDS` / `source_detail`，main 与快照两份实现都没有），取回即 7 红 —— 已在台账里裁决 `DROPPED`（附可复核验据），**属未合入分叉线，由该线所有者整线合并** |

## 4. 卫生检查

```bash
python tools/code-audit/repo_governance_check.py          # 人类可读
python tools/code-audit/repo_governance_check.py --quiet  # 只看退出码（可进 CI）
```

输出五类读数：
1. **未跟踪源码类文件数**（唯一先行指标，应为 0）；
2. 被 gitignore 排除的源码类文件数（设计内排除，但**若含结论/报告类即为隐患**）；
3. 相对各远端的 ahead/behind（领先未推送 = 只在本地存在；参 §1.1 硬约定）；
4. 抢救点与 DANGER 分支是否安在；
5. **★ 抢救点独有源码数**（对象库有、`main` 没有）—— 逐件裁决看 §2.1 的台账。

> 已实证的第 2 类隐患：`tracking/.gitignore` 曾整目录忽略 `DEU/reports/`、
> `DEU/scripts/` 与 `USA/reports/*.md`，使这两个区域的报告**永久落不了库**。
> 2026-10-06 已改为与其它区域同口径（只忽略 `tmp_` / `archive`）。

## 5. 尚未处理 / 已裁决

### 5.1 远端同步

- `origin/main`：**已同步**（2026-10-06 推过 P2/P3 两个提交）。具体 ahead/behind **不写在本文**，
  跑 `python tools/code-audit/repo_governance_check.py` 看读数。
- `gitcode/main`：镜像长期落后。**用户明确指示"先不管"**，故本文件不把它列为待办；
  推送是外发动作，需用户再次明确指令。（历史上这里写死过「落后 109 个提交」，
  实测已变 112 —— 就是本文顶部那条「不复制会漂移的计数」约定的由来。）
- ⚠ **推 `main` 不等于备份了抢救点**：`--tags` / `--branches` 不会随普通 push 上去。
  实测 `git ls-remote --tags origin` 为空 —— 即 §1.1 的硬约定目前**未满足**，
  靠 `git bundle` 本地冷备临时达成（需用户确认后才能真正外发）。

### 5.2 `git gc --prune=now` —— 判定不安全，不执行

本机同时存在 cline（`refs/cline/checkpoints/*`）与 codex（`refs/codex/turn-diffs/*`）
的 ref 命名空间，且有正在运行的回测/选区进程（含另一个工作副本 `D:/coding/hw_project/wqb`）。
在这些 ref 与进程存在期间做 prune，可能回收掉**只被这些 ref 引用**的 blob。
保持现状；若要清理，须先确认上述 ref 命名空间与并行进程都已停止。

### 5.3 抢救点比对：6 个"可恢复"文件的终局裁决 —— 不回迁

抢救点 `4910e65` 内仍可 `git checkout` 取回以下 6 件（此前列为"待人工决策"）。
2026-10-06 逐件核验后**裁决：全部不回迁**；逐件依据已录入机读台账
`tests/fixtures/snapshot_adjudication.json`（正文见 §2.1），并同时登记进
`tools/audit_structure_baseline.json` 的 `retired_paths` 由 **S12 拦复活**
（光写在文档里的裁决扳不住另一个会话的 `git checkout`）。

**核验方法与结论**

> ⚠ **「丢失件是否存在」必须三源交叉**（2026-10-06 治理评审补的硬口径）：
> 1. `git ls-files`（main 受控集）；
> 2. `git ls-tree -r <每个 preserve/* tag 及其 ^3>`（**对象库**，含快照的未跟踪父提交）；
> 3. `git log --all --diff-filter=D -- <path>`（曾入库又被删的记录）。
>
> **任一为「有」就不得写「从未存在」**，只能写「不在 main，存在于 <ref>，裁决 = …」。
> 实锤错例：同日曾按 `git ls-files` + 磁盘存在性把 `src/wqb/semantic_ledger.py` 判成
> 「全仓从未落地」（实为 `git cat-file -s 4910e65:…` = 2407 字节）。该误判的后果是
> **指使下一个 Agent 放弃一个可取回的模块**。守卫测试：
> `tests/unit/07_docs_skills/test_governance_gates_selfcheck.py`。

| 文件 | 活动引用核验 | 裁决依据 |
|---|---|---|
| `tools/direct_submit.py`（已丢失） | 全仓只命中我自己的治理文档 | ① `tools/wave_gate.py`·`quality_predict.py` 里的 `direct_submit` 是 `qp_summary["direct_submit"]` **计数字段键**，不是该脚本；② `DIRECT_CONNECT_WHITELIST`（7 项，`test_db_write_guards.py::test_whitelist_files_exist` 断言必须存在）**不含它**；③ 提交链已被 MCP `workflow_submit_alpha` + `tools/super_build.py submit` 覆盖 |
| `tools/harvest_batch.py`（已丢失） | 同上 | `pipeline.py` 里的 `_harvest_batch_alphas` 是**本地函数**（非该脚本）；收批已统一走 `tools/harvest_multisim.py`（支持多 multisim 批量收） |
| `tools/self_batch.py`（已丢失） | 同上 | 零活动引用；self 侧走 MCP `check_self_correlation` 与 `brain-calculate-alpha-selfcorr-quick` |
| `tools/harvest_by_expr.py`（已丢失） | 同上 | 零活动引用；按表达式收批的需求已由 `harvest_multisim` 覆盖 |
| `tools/eu_field_coverage.py`（已丢失） | 仅历史报告引用 | 活文档 `wq-brain-ra-pipeline/references/ppa-mining-experience.md` 已明写**前者不存在**；`reports/` 里的引用是**时点记录**（描述当时存在过什么），不是待办 |
| `tools/gate.py`（已丢失） | 无 | `AGENTS.md` L363 早已标注「代码零引用的遗留文件（**已归档**）」；表达式预检职责由 `wqb.expression.op_arity.ensure_safe_for_dispatch` 与 `tools/code-audit/*` 承接 |

**不回迁的第二重理由（工程侧）**：`tools/` 顶层有 S11 硬闸「只减不增」，基线**不含**
这些文件 —— 从抢救点 checkout 回 `tools/` 顶层会把基线顶爆（新增即 FAIL）。
要解就得"为零引用文件重冻基线"，而重冻基线等于给它发永久通行证，**收益为负**。

**若将来确实需要**：正确路径是**在主题子目录里新写一个工具**（如
`tools/verdict/` / `tools/ledger/`），而不是从抢救点把旧文件 checkout 回 `tools/` 顶层。
抢救点 `4910e65` 保留不动，作为"曾存在过什么"的唯一证据。

> ⚠ 连带影响：`MEMORY.md §4` 与部分 skill 里指向 `direct_submit.py` /
> `harvest_batch.py` / `self_batch.py` / `harvest_by_expr.py` 的命令**都已失效**，
> 勿照抄执行 —— MEMORY 侧已于 2026-10-06 改指真实通道（`tools/harvest_multisim.py`）。

## 6. 会话隔离（2026-10-06 新增，与 §0 铁律同级）

工作丢失的**根因不是分支模型，是多写者共用一棵未提交的工作树**。
实测：同一棵树上同时跑多个 Agent 会话时，一次 `git clean` / 一次 `stash + reset`
（Cline 的 checkpoint restore 就是这个）就能一夜抹掉多次未提交内容；
本会话期间也实到过一次「别人的未跟踪文件把我主干的守卫测试跑红」。

硬约定：

1. **每个并行会话一棵工作树**：
   ```powershell
   git worktree add ..\wt-<session> -b wip/<session>-<topic>
   ```
   或干脆独立 clone。禁止多个写会话共享同一目录。
2. **动手前先自保**：`git diff --binary --output=logs/wip_backup_<YYYYMMDD>.patch`（`logs/` 已 gitignore）。
3. **暂存必须用精确 pathspec**，禁 `git add .` / `git add -A`；`git restore --staged`
   也只给路径，不给 `.`（它会连带取消**别人** stage 的文件）。
4. **不跨会话代删/代改他人在途的未跟踪文件**。它把主干测试跑红时，先把事实
   报给用户裁决，而不是删掉它或改测试迁就它。
5. **闸自身的定义文件**（`src/wqb/**`、`tools/git-hooks/**`、`tools/audit_*.py`、
   `tests/fixtures/*_baseline.json`）属「改了就影响别人能不能提交」的一类：
   改它们另起分支、跑一次全量、人工确认后再合。

