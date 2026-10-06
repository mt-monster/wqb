# 仓库结构与治理评估 — wqb

- 评估时间：2026-10-06 16:40 (+08:00)
- 评估对象：`D:\coding\traeCN_project\wqb`（HEAD = `0a89cbe`）
- 评估方式：只读。`git ls-files / ls-tree / status / count-objects / config / log` + 磁盘文件核对
- **未做的事**：未跑 pytest、未跑任何回测、未改动仓库任何文件

---

## 0 一句话结论

**事故抢救已经成功，主干 `main` 现在是历史上最完整的一条线；但"引发事故的那个条件"仍然处于 armed 状态——22 个被文档/记忆明确引用的核心源码文件至今没有入库，只要再跑一次 `git clean -fd`，就是第二次事故。**

所以本次评估的排序很明确：**先补入库（P0），再谈任何清理与分支收敛（P1/P2）**。顺序反了就是再犯一次。

---

## 1 事实基线

| 项 | 值 |
|---|---|
| 主干 | `main` = `0a89cbe`（2026-10-06 15:40），与 `origin/main` **0 差异** |
| 提交总数 | 175（首提交 2026-08-02，历时 65 天） |
| 提交节奏 | 近 30 天 7–27 commits/日；今日 7 个 |
| 追踪文件 | 3,952 |
| `.git` | 77 MB |
| 工作区 | 2.3 GB（其中 data/ 964M、MCP .venv 763M、cache/ 302M 均已被 ignore） |
| 本地分支 | 9（主干 1 + 抢救引用 8） |
| 远端 | 2（`origin` = GitHub，`gitcode` = gitcode.com） |
| 钩子 | `core.hooksPath = tools/git-hooks`，`pre-commit` 72 行（存在，非默认位置） |
| CI | **无**（无 `.github/`、无 `.gitlab-ci.yml`） |
| 未提交变更 | 57 条（24 M / 32 ?? / 1 A） |

---

## 2 分支与主干

### 2.1 主干健康度：好

`main` 与远端完全同步，提交信息规范（`fix(db):` / `feat(mcp):` / `chore(tools):` 等 conventional commits），有实质性重构与文档联动。这是健康的。

### 2.2 八个抢救引用：全部 2026-10-06 生成，全部未合并

| 分支 | 性质 | 相对 main | 处置建议 |
|---|---|---|---|
| `snap/worktree-1006b` | **15:20 冻结快照**，含当前工作区 53 个条目 | 落后 1 / 领先 1 | 确认吸收后转 tag |
| `snap/worktree-1006` | 03:50 快照 | 落后 7 / 领先 1 | 转 tag |
| `wip/DANGER-restore-1006-0056-gutted` | 事故取证（Claude/skills 只剩 32） | 落后 7 / 领先 1 | **保留**，取证用 |
| `wip/DANGER-...-untracked` | 同上，未跟踪部分 | 落后 7 / 领先 1 | 保留 |
| `wip/cline-restore-1005-1929` (+`-untracked`) | 另一条工作线 | 落后 9 / 领先 1 | 死线，转 tag 后删 |
| `wip/cline-restore-1006-0023` (+`-untracked`) | 同线后续 | 落后 7 / 领先 1 | 死线，转 tag 后删 |

### 2.3 抢救完整性：**成功**

`main` 的 `Claude/skills/` 有 **432** 个文件；事故分支只剩 **32**。`main` 相对事故分支仅缺 8 个文件，其中 5 个已在磁盘上（只是未跟踪）。抢救彻底。

### 2.4 一个值得注意的信号

抢救过程中出现了 **5 对 `wip/*-untracked` 分支**——需要专门开一条分支来冻结"未跟踪文件"。这说明"未跟踪文件"不是偶发，而是**结构性缺陷**。这个 workaround 本身就是病症；药是入库，不是再开分支。

---

## 3 双远端

| 远端 | 地址 | 状态 |
|---|---|---|
| `origin` | `git@github.com:mt-monster/wqb.git` | 主，`main` 同步 |
| `gitcode` | `https://gitcode.com/MT_monster/wqb.git` | **落后 104 个提交**（无分歧，纯落后） |

`gitcode` 是失同步的镜像。要么推齐，要么明确它是"废弃远端"。

---

## 4 工作区状态 ★ 风险集中区

57 条变更拆开看：

### 4.1 32 个未跟踪里，**22 个是源码/文档**（应入库）

```
src/wqb/region_catalog.py          ← MEMORY §3 明确引用（RegionCatalog）
src/wqb/towers.py                  ← 未在任何文档中登记
src/wqb/store/_corr_cache.py       ← prod 相关性缓存层
src/wqb/store/_api_cache.py
tests/unit/01_store_db/test_corr_cache_cross_table.py
tests/unit/01_store_db/test_region_query_guard.py
tests/unit/01_store_db/test_submit_ready_health_cols_20261006.py
tools/scan_backup_ra.py            ← MEMORY §4「盘点前必跑」
tools/submit_inventory.py
tools/probe_sa_candidates.py
tools/probe_sa_unsubmitted.py
tools/verify_region_op.py
tools/category_sweep.py            ← 快照后新增
tools/category_probe.py            ← 快照后新增
tools/enqueue_propose.py
tools/backfill_alpha_metrics_from_platform.py
tools/candidate_health_card.py
Claude/skills/wq-brain-ra-pipeline/references/category-sweep.md          ← 快照后新增
Claude/skills/wq-brain-ra-pipeline/references/signal-hypothesis-construction.md ← 快照后新增
tracking/EUR/GOAL_20_ACCUMULATION.md
tracking/EUR/scripts/gen_wave342.py
tracking/KOR/scripts/preflight.py
```

### 4.2 9 个是报告产物（按 AGENTS.md「output_report/ = 报告唯一出口」也属入库范围）

8 个 `output_report/DEU_*` `GBR_*` + 1 个 `reports/kor_zero_tower_sweep_20261006.md`。

### 4.3 安全网现状：**部分失效**

`snap/worktree-1006b` 在 15:20 冻结了 53 个条目，**但 15:20 之后的新产出没有保护**：

- 新增未跟踪：`category-sweep.md`、`signal-hypothesis-construction.md`、`tools/category_probe.py`、`tools/category_sweep.py`
- 新增修改：`SKILL.md`（16:36）、`preflight_wave.py`（16:15）、`sync_platform_alphas.py`（16:15）

即**冻结快照是一次性手工动作，不是常设机制**。

### 4.4 根因判定

上次事故根因 = `git clean -fd` 清掉未跟踪文件（证据：`.git/index` mtime 与文件消失时间吻合，`world-quant-brain-mcp/` 是 git 跟踪目录）。

**该条件今天仍然成立**：`tools/scan_backup_ra.py`（记忆里写"盘点前必跑"）此刻就是未跟踪状态。→ **P0**。

---

## 5 结构调整体

### 5.1 追踪分布

| 目录 | 追踪文件 | 占比 |
|---|---|---|
| `tracking/` | 2,597 | 66% |
| `Claude/` | 432 | 11% |
| `tools/` | 213 | |
| `tests/` | 202 | |
| `output_report/` | 118 | |
| `src/` | 115 | |
| `reports/` | 91 | |
| 其余 | ~180 | |

`tracking/mining/` 单目录 1,053 个追踪文件，是"共享数据湖"，AGENTS.md 已声明勿动。**66% 的追踪文件是挖掘台账而非代码**——这让 `git status`/`git log` 的信号被稀释，但符合本项目"台账即资产"的定位，属可接受，只需意识到。

### 5.2 ★ `tracking/.gitignore` 的区域不对称（建议修）

```gitignore
DEU/reports/          # 整个目录被忽略
DEU/scripts/          # 整个目录被忽略
```

而 GBR(153)/EUR(295)/KOR(433)/USA(204) 的区域脚本是**入库**的。

后果：**DEU 战役的脚本与报告不进版本控制**——而 DEU 恰好是当前正在打的战役区（今天还在产出 `output_report/DEU_*` 四份报告）。这与"报告唯一出口 `output_report/`"的治理口径直接冲突，形成一个**未登记的孤岛**。

### 5.3 `attic/` 有 35 个文件被追踪（与 ignore 规则冲突）

`attic/` 在根 `.gitignore` 里，但已有 35 个文件被追踪——`.gitignore` **不会** untrack 历史文件。AGENTS.md 承认这是"早期存量"。属可接受的遗留，但应显式豁免或清理，不要让它悬着。

---

## 6 工程卫生指标

### 6.1 对象库有垃圾（并发 git 操作的脚印）

```
loose objects : 8,709      in-pack : 6,389
garbage       :   351 个 tmp_obj_* （1.00 MiB）
prune-packable:   160
```

`tmp_obj_*` 是 `git add`/`hash-object` 被中断留下的临时对象。351 个 = **本机长期存在多个 agent 会话并发操作同一工作区**（与 MEMORY §4「并发 tools/ 重组会反复删/移自建文件」互相印证）。松散对象 8,709 > 打包 6,389，说明很久没 gc。

### 6.2 提交者身份分裂为 4 个

```
99  MENGTAO <mthyzx@gmail.com>
40  Claude  <noreply@anthropic.com>
34  MENGTAO <mthyzx@126.com>
 2  MENGTAO <mt@wqb.local>
```

同一个人的 3 个邮箱 → `git shortlog`/blame 归因不准。

### 6.3 文档-现实漂移

`MEMORY.md §4` 仍写「收割 `harvest_batch.py <multisim_id>`；批量 self `self_batch.py`」，但两者磁盘上**已不存在**（功能已被 `tools/harvest_multisim.py` 等吸收）。`tools/quota_status.py` 存在但记忆里标了「当日恒显 0/4」的坑——需确认是否已修。

### 6.4 已有的良性治理（应当表扬并保持）

- `.gitignore` 已按日期分段、逐条注明理由与实例，质量高于多数生产仓库
- 钩子 `core.hooksPath = tools/git-hooks` 存在（避开默认位置，防误删）
- AGENTS.md 已定义「五处同步」等跨文件一致性契约 + 守护测试
- `data/` 备份数受 `test_retention.py` 硬闸 ≤2

---

## 7 治理建议（按优先级）

### P0 — 消除事故根因（今天做完）

1. **把 22 个未跟踪源码 + 9 个报告入库**，建议分 3 个语义提交：
   - `feat(store): corr_cache / api_cache 层 + 3 个单测`
   - `feat(src): towers / region_catalog 落库登记`
   - `chore(tools,reports): category_sweep 工具族 + DEU/GBR/KOR 报告`
   先做这一步，其余都排在它后面。
2. **在入库完成前，冻结一切 `git clean`**。建议写进 AGENTS.md 红线（与"不得 `--no-verify`"同级），并加一条 pre-commit 兜底。
3. **把"关键路径必须 tracked"变成可执行检查**：在 `tools/git-hooks/pre-commit` 或 CI 里加一句——凡 `MEMORY.md` / `AGENTS.md` 中出现的仓库内路径，必须 `git ls-files` 命中，否则拒提交。这比"记得手动盘点"可靠得多。

### P1 — 分支收敛

4. **把 8 个抢救分支降级为 tag**（`git tag preserve/<name> <sha>` 后删 branch）。理由：分支会随 fetch/clone 传播、污染 `git branch` 信号；tag 同样能永久保留对象，且不参与日常操作。
5. **建立短期工作分支约定**：agent 会话一律在 `wip/<date>-<topic>` 上作业，**当日合并或丢弃**，不跨日挂分支。`snap/*` 只在事故时手工创建。
6. `wip/DANGER-*` 建议**保留为取证分支**（不进 tag 清理），但要在 README 里写清"永不合并"的原因，避免后人误 merge。

### P2 — 工程卫生

7. `git gc --prune=now`（**先确认无并发 agent 会话在跑**）清 351 个垃圾对象 + 松散对象。
8. 统一提交者身份：固定 `git config user.email`，或用 `.mailmap` 把 3 个邮箱归并到一个。
9. 修 `tracking/.gitignore` 的 DEU 不对称——要么放开 `DEU/reports/`、`DEU/scripts/`，要么把其它区也统一排除并写清理由。二选一，不要留特例。
10. `attic/` 35 个追踪文件：二选一定案 —— `git rm --cached` 全部退出追踪，或在 `.gitignore` 里显式写 `!attic/` 并声明"attic 是入库归档"。
11. 同步 `gitcode` 镜像（`git push gitcode main`），或明确废弃该远端。
12. 同步文档：修 `MEMORY.md §4` 的 `harvest_batch/self_batch` 指向现行脚本。
13. **补一条最小 CI**：`pytest --collect-only` 数量校验 + 关键单测子集 + P0-3 的 tracked 校验。当前零 CI 意味着所有守护测试都靠人记得跑。

### P3 — 可选项

14. 建立 `docs/governance/untracked_allowlist.md`：把"允许未跟踪"的文件列成白名单，让 `git status` 里的 `??` 有解释。
15. 定期（每周）跑一次本评估的同款命令，把"未跟踪源码数"作为**唯一指标**盯——它是事故的唯一先行指标。

---

## 8 本次未覆盖

- 未跑测试套件 → **不知道当前代码是否功能正常**（本报告只评估结构与版本控制状态）
- 未检查 `world-quant-brain-mcp/.env` 之外的凭据泄漏面
- 未逐文件审 `src/` 115 个模块的内部质量（超出"结构治理"范围）

---

*本文件由只读评估生成，未改动仓库任何其他文件。*
