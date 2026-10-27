# 代码库治理评审 — 2026-10-27

> **⚠ 修复已执行（2026-10-27 晚，用户裁定「全部修复」）**：§0–§9 是**修复前**的快照，其中的
> FAIL 58 / S16 FAIL 20 / 133 条幽灵路径等数字**保留当时读数**（它们是根因证据，不应被改写成
> 修复后的样子）。**实际执行、与建议的偏差、修复后实测见 §10**。
> 已闭合：P0-P1 / P2 / P3（代码面）/ P4 / P6 / P7 / P8 / P9 / P10；
> 按原建议留给他人：P0-P5（USA 在途文档，`skill_lint` 基线不得更新）；
> 仍待用户裁定：CI runner OS（§4-P3 后半）。
>
> **性质**：人工审计 / 复盘（按 AGENTS.md §8.13 落 `reports/<主题>_<YYYYMMDD>.md`）。
> **范围**：整仓——工作树 + git 索引 + 四道质量闸 + 测试面 + 技能树 + 磁盘。
> **只读声明**：本轮**未**提交、未删除、未归档移动、未写库、未改任何源码或文档；
> 只在 `logs/` 下建了临时测量脚本（gitignored，清单见 §9）。
> **快照口径**：所有计数均为 **2026-10-27 20:15 前后** 的单点读数。审计期间并行会话动过索引
> （见 §1.1），复跑数字会漂，凡时效敏感的结论都附了复跑命令。
> **权威源**：治理规约以 `AGENTS.md` 为准；本文只给证据与建议，不新增规约、不改基线。

---

## 0. 一页结论

**当前工作树处于「不可提交」状态**——这不是判断，而是可复现的硬事实：

```
git config core.hooksPath   → tools/git-hooks   （钩子已挂载，会真实执行）
python tools/audit_structure.py → FAIL=58  WARN=5  exit=1
   其中 S20「索引↔工作树一致」直接拦下：133 个文件在索引里、工作树已不存在
```

也就是说：**现在任何人 `git commit` 都会被本地钩子挡回**，除非先解决那 133 条幽灵路径。

而这 133 条**一条根因、四个症状**——这是本轮最重要的发现：

| 症状 | 表现 | 为什么难发现 |
|---|---|---|
| S20 FAIL | 133 条幽灵路径 | 只有本地钩子会跑，CI 在干净检出上永远看不到 |
| S16 FAIL 20 | 10-26 有人把这些文件当「已删除」从命名基线里清掉，但索引里还在 ⇒ 闸判为「新增违规」 | 看着像「新文件命名不合规」，实际是基线被提前清理 |
| `doc_path_refs` **假绿** | BROKEN 12 = 基线 12，「✅ 无新增死指针」 | 该闸用**索引**判存在：未暂存删除 ⇒ 认为文件还在（§2.3） |
| `closure_ledger` 测试红 3 条 | 报告文件确实不在磁盘上 | 只在全量测试里显形 |

**除了这 133 条，代码本身没有失控**：18 条测试红里 0 条是产品逻辑回归，全是
「闸门判据 vs 新增产物」「文档指针 vs 被删文件」「测试隔离 vs 并行会话」三类治理面冲突
（第 18 条是守护探针不认 `async def`，属同一类：**判据与代码形态脱节**）。

| 判断 | 结论 | 依据 |
|---|---|---|
| 索引能直接提交吗 | **不能** | S20 阻断；另有 13 条结构违规在已暂存新增件上（CI 必红） |
| 索引里是什么 | **466 件纯新增，0 修改、0 删除** | 审计中途被并行会话重置：764（含 166 M / 132 D / 12 个半暂存）→ 466 纯新增（§1.1） |
| CI 能绿吗 | **当前一定不能** | 钩子自检步方向反了（干净 runner 必失败，§4-P3）+ 13 条结构违规（§4-P6）+ 18 个 skill_lint 新键（§4-P4/P5）+ 18 条测试红（附录 A.3） |
| 57 份被删报告安全吗 | **不安全** | 0 份留副本；6 份是真依赖（`closure_ledger` 读文件 + AGENTS/docs 引用），4 份被 `dataset_experience` 知识库引用（§2.4） |
| 最大的单点浪费 | **≈533 MiB** | `data/` 有 2 份备份，策略只留最新 1 份（§5-P11） |
| 最大的技术债 | **`wave_gate` 两套活实现** | `tools/wave_gate.py` 1678 行仍在跑，`tools/wave_gate_pkg/` 无人 import，AGENTS.md 却称它是「~140 行 shim」（§6-P2-16） |
| 需要用户拍板 | **3 项** | ① 133 条删除的去向（§4-P1）② gate-5 分母假阳性怎么修（§4-P4）③ `tools/` 战役栈是退役还是活的（§5-P14） |

**建议执行顺序**：`§4-P1（133 条）→ P2（报告）→ P10（提交守护 3 行）→ P3（CI 步）→ P6（结构面）→ P7（测试）→ P4/P5（gate-5 与 skill 文档）→ §5 拆提交`。

---

## 1. 实测基线

### 1.1 工作树与索引（快照 2026-10-27T20:15）

| 指标 | 读数 | 说明 |
|---|---|---|
| `git status --porcelain` | **889 行** | = 466 A + 193 M + 133 D + 97 ?? |
| 已暂存 | **466**，**全部是新增（A）** | 0 个暂存修改、0 个暂存删除 |
| 未暂存修改（ M） | **193** | 含 `src/wqb/**` 26、`Claude/skills` 65、`tools` 34、`tests` 24、MCP 11 |
| 未暂存删除（ D） | **133** | `reports` 57 · `tracking` 40（全部 EUR）· `output_report` 32 · `tools` 3 · `Claude` 1 |
| 未跟踪（??） | **97** | `tools/` 53 · `output_report` 19 · `tracking` 9 · `reports` 5 · 其余 11 |
| 半暂存（MM） | **0** | 审计开始时是 **12**，中途被并行会话重置（见下） |

**已暂存 466 件的构成**：

| 区域 | 件数 | 明细 |
|---|---|---|
| `docs/reference` | 202 | **EUR 196** + IND 1 + 5 份根级 runbook/速查 |
| `Claude/skills` | 127 | USA 105 · IND 17 · EUR 2 · DEU 2 · toolkit 1 |
| `tools` | 53 | 顶层 35 + `data-repair/` 14 + `git-hooks/` 2 + `fields/` 1 + `docs/` 1 |
| `tracking` | 28 | — |
| `tests` | 20 | — |
| `reports` | 17 | — |
| `output_report` | 10 | — |
| `world-quant-brain-mcp` | 3 | — |
| `src/wqb` | 2 | 新模块 |
| `attic` | 2 | 含 1 个改名 |
| `.github` / `.opencode` | 1 / 1 | `gates.yml` / `opencode.jsonc` |

> ### ⚠ 审计期间索引被重置（这条本身是治理发现）
>
> 审计开始时（同一会话早前实测）：**764 暂存 = A 465 / M 166 / D 132 / R 1，其中 12 个 `MM` 半暂存**。
> 约两小时后复测：**466 暂存，全部是 A**。也就是说有并行会话把**修改与删除整体退出了索引**，只留下新增。
>
> 后果有两面：
> - **好的**：12 个半暂存件消失了。此前的最高风险是 `src/wqb/submit_verdict_core.py` 等 12 个文件
>   「一半在索引、一半在工作树」，其中未暂存的一半正是 PPA 实时通道判定
>   （`"ppa_channel"` / `"ppa_tag_only"`）——提交索引等于上线半个行为变更。现在这个风险不存在了。
> - **坏的**：证明**本仓的索引是所有并行会话共享的可变状态**，任何「索引里有什么」的结论只有分钟级有效期。
>   §5-P10 的拆提交必须放进**独立 worktree**，否则拆到一半又会被别人重置。
>
> 复跑：`git status --porcelain | cut -c1-2 | sort | uniq -c`

### 1.2 四道质量闸（pre-commit 与 CI 同源）

| 闸 | 读数 | 阻断级 | 备注 |
|---|---|---|---|
| `tools/audit_structure.py` | **FAIL 58 / WARN 5**，exit=1 | 阻断 | 基线 2026-10-26 00:54 冻结 |
| `tools/code-audit/doc_path_refs.py` | BROKEN 12（基线 12）· UNTRACKED 0 | 棘轮 | **当前是假绿**，见 §2.3 |
| `tools/skill_lint.py` | 45 条，**新增 18 个键 / 19 行** | 棘轮 | 全部 `POISON:equal_weight_leg_add` |
| `tools/code-audit/audit_destructive_default.py` | **新增高危 2 条** | 棘轮 | 同一未跟踪文件，见 §3-B5 |

**FAIL 58 的构成**（这是「闸说有问题」，不等于「58 个问题」）：

| 闸项 | 条数 | 落点 | 在已暂存件上？（CI 会红） |
|---|---|---|---|
| S20 索引↔工作树一致 | **1**（含 133 个路径） | 未暂存删除 | 否（干净检出无此问题）· **但本地提交被它挡死** |
| S16 报告命名 | **1**（含 20 个文件） | 存量文件的基线被提前清理（§2.2） | 否 · 本地红 |
| S14 `tools/README` 登记 | **1**（含 10 个脚本） | `tools/` | **是，10 个全部已暂存** |
| S11 `tools/` 顶层冻结 | **3** | ① `detach_launch.ps1`（未跟踪）② 54 个新顶层脚本 ③ 54 个无主题归属 | 其中 2 个已暂存 |
| S4 硬编码盘符 | **52** | 42 个文件，41 个未跟踪 | 仅 1 个：`tools/_r24b_sweep.py:16` |

⇒ **CI 真正会拦的面 = 13 条 / 11 个文件**（S14 10 + S11 2 + S4 1）。S16/S20 共 21 条只在本地红。

**WARN 5 条**：S1 262 处 `sys.path`（设计内）；S14 `backfill_check_columns.py` 已不在磁盘（正当退役，同步基线即可）；
S16 基线内 20 条存量 + 2 条未跟踪（`output_report/s0_select_usa_20261027.json`、`webdata_usa_d1_20261027.csv`）；
S6 4 组跨 skill 同名副本（`ace_lib.py` / `diversity_enhancer.py` / `helpful_functions.py` / `validator.py`）。

### 1.3 测试面（`pytest tests/ -q --no-header`，2026-10-27 20:30 跑完）

| 指标 | 读数 |
|---|---|
| 收集 | **3901**（18 failed + 3811 passed + 72 skipped） |
| 用时 | 266.53s（04:26） |
| 失败 | **18 条 / 10 个文件** |
| 0 条产品逻辑回归 | 18 条全是「闸门判据 vs 新增产物 / 文档指针 vs 被删文件 / 测试隔离 vs 并行会话」 |

| 失败文件 | 条数 | 类 | 处置 |
|---|---|---|---|
| `test_field_catalog_cache_completeness.py` | 6 | D 测试隔离 | §4-P9 |
| `test_closure_ledger.py` | 3 | C 被删报告 | §4-P1 ② |
| `test_submit_chain_defaults.py` | 2 | F 守护形态脱节 | §4-P10 |
| `test_db_write_guards.py` | 1 | B 裸 sqlite | §4-P7 |
| `test_region_query_guard.py` | 1 | B 行号漂移 | §4-P7 |
| `test_skill_lint.py` | 1 | B 新增 18 键 | §4-P4 / P5 |
| `test_profiles_layer.py` | 1 | B ASI 漂移 | §4-P8 |
| `test_audit_structure_s11_dataface.py` | 1 | 本机 | 未跟踪 `detach_launch.ps1` |
| `test_docs_consistency.py` | 1 | 本机 | 未跟踪 `glb_campaign_runbook_20261026.md` |
| `test_sd_portability.py` | 1 | 本机 | 15 个未跟踪探针硬编码盘符 |

⚠ **读数在审计期间从 16 漂到 18**：并行会话在 20:00 前后把 `workflow_submit_alpha` 由
`def` 改成 `async def`（2026-10-27「提交假死」修复），而 `test_submit_chain_defaults._defaults()`
只认 `ast.FunctionDef`、不认 `ast.AsyncFunctionDef` ⇒ 该用例从「通过」变成「找不到函数」。
**这不是回归，是守护被打盲**：`confirm_submit is False` / `color is None` / `robustness_audited is False`
这三条提交安全断言，此刻一条都没在跑（§4-P10）。

后 3 条与整个 CI 面无关：未跟踪件不在干净检出里，属产出它们的会话。逐条清单见附录 A.3。

### 1.4 提交面之外：磁盘与 git 对象

| 项 | 读数 | 政策 | 可回收 |
|---|---|---|---|
| `data/wqb.db`（live） | 583,053,312 B（556 MiB） | 硬保护，永不删 | — |
| `data/*.bak*` | 2 份：558,571,520 + 577,302,528 B | 只留最新 1 份 | **≈533 MiB** |
| `data/` 合计 | 1.67 GB | — | — |
| git 松散对象 | 12,800 个 / 54,062 KB | — | `git gc` 后大幅压缩 |
| `tmp_obj_*` 垃圾 | **351 个 / 1,025 KB** | 自动清理 | 全部 |

⚠ 备份删除、`git gc` 属**用户确认后**动作（`tools/retention.py` 默认 dry-run）。本节只登记数字。

---

## 2. 核心发现：一条根因，三道闸红 + 一个假绿

### 2.1 事实

`git ls-files -d` = **133 个文件**在索引里、工作树已不存在：

| 目录 | 件数 | 性质 |
|---|---|---|
| `reports/` | 57 | 批量清理（多数是 8–10 月的审计/复盘） |
| `tracking/EUR/` | 40 | 战役脚本与中间件（含 1 个 `cells.json.bak_*`） |
| `output_report/` | 32 | 战役产物（EUR/IND 的 ideas、状态报告） |
| `tools/` | 3 | **正当退役**（`retired_paths` 已登记） |
| `Claude/skills/wq-brain-ra-eur/references/_probe-sop.md` | 1 | **改名未完成**：新路径已暂存进 `attic/`，旧路径删除没暂存 |

### 2.2 三个症状

1. **S20 FAIL（133）** —— 闸的本职，报得对。它拦的是「索引挂着幽灵路径」，正是 §8.12 记录过的事故形态。
2. **S16 FAIL（20）** —— 看着像「20 个新文件命名不合规」，实际是 **10-26 的基线清理把还活着的文件删了**：
   `tools/audit_structure_baseline.json` 的 `_s16_note` 写着「2026-10-26 清理：移除 20 条已删文件的僵尸条目（40→20）」，
   而实测这 20 个文件**索引里全在、磁盘上全不在**——正是 §8.4 第 9 项/§8.12 反复记的那个坑：
   **冻结或清理基线前必须先确认工作树完整，否则会把「文件丢失」固化成「已迁移」**（S11 的注释里也有同一句教训）。
3. **`closure_ledger` 3 条测试红** —— `tools/closure_ledger.py:46/48/57` 直接 `read_text()` 两份被删报告。

### 2.3 一个假绿（**这条比三个红更值得记**）

`doc_path_refs.py` 当前输出「BROKEN 12（基线 12）✅ 无新增死指针」。但 `reports/skills_review_20260929.md`
等 5 份文件**磁盘上根本没有**，AGENTS.md 还指着它们。原因在 `classify()`：

```python
if is_boot(t) or t in tracked or is_ignored(t):
    continue          # ← t in tracked（索引）即视为存在，从不看磁盘
```

⇒ **未暂存删除 = 该闸完全失明**。三面同时成立时才看得见它：本地钩子（暂存后才报）、
`pytest`（closure_ledger 读文件）、以及人眼。

**纪律（建议写进 §8.12 那一族）**：凡「以 git 索引为取面的闸」，对**未暂存删除**天然失明；
交付前应以 `git ls-files -d` 作为独立自查项（S20 已机械化，保留它）。

### 2.4 133 条里哪些不能随便删

对 133 个文件名做全仓跟踪面扫描（排除同批被删件），**38 个有外部提及**，其中真正承重的
**10 个文件**（6 份报告 + 4 份 EUR 证据链）列在下表，另有 1 个 `.bak` 属「本来就该删、但文档指着它」：

| 被删文件 | 引用方 | 性质 |
|---|---|---|
| `reports/skills_review_20260929.md` | `tools/closure_ledger.py:46` | **代码硬依赖**（read_text） |
| `reports/skills_review_20260929_closure.md` | `tools/closure_ledger.py:48` | **代码硬依赖** |
| `reports/alpha_properties_audit_20260920.md` | `docs/alpha_properties_spec.md`、`tools/README.md`、`tools/alpha_properties.py` | 文档 + 代码注释 |
| `reports/code_structure_survey_20260925.md` | `AGENTS.md` §8.4 第 5 项 | 规约正文引用 |
| `reports/db_mcp_split_20261004.md` | `AGENTS.md` §8.4 第 9 项、`tools/code-audit/db_mcp_split.py` | 规约正文 + 工具 |
| `reports/db_concurrent_write_lock_audit_20260920.md` | `src/wqb/db_conn.py`、`src/wqb/db_write_lock.py`、测试 | 源码注释里的依据 |
| `reports/eur_d1_20260924_{fundamental17_measurement_repair,news46_mechanisms,news50_mechanisms}.md`、`reports/eur_d1_20260925_other460_probability_probe.md` | `reports/dataset_experience/eur_*_campain.md` | 知识库里的证据链 |
| `tracking/EUR/config/cells.json.bak_before_vectorn_neut_fix_20261010` | `docs/reference/EUR/fundamental72_campaign_20261010.md` | 备份件本身不该入库，但文档指着它 |

其余 95 条**零外部引用**（`tests/` 里那几处是命名规则的字符串夹具，不依赖文件存在）。

### 2.5 处置决策表（§4-P1 的执行依据）

| 类别 | 件数 | 处置 | 理由 |
|---|---|---|---|
| `tools/` 3 件 | 3 | **暂存删除**（`git add -u --`） | `retired_paths` 已登记，属正当退役 |
| `_probe-sop.md` | 1 | **暂存删除**（补齐改名） | 新路径已在 `attic/` 且已暂存；DEU/GBR/KOR 各有自己的同名文件，引用不受影响 |
| `reports/` 中承重 6 件 | 6 | **`git restore --` 取回** | 代码/规约/知识库硬依赖（§2.4） |
| `reports/` 其余 | 51 | **归档而非删除**：先取回 → 落 `attic/reports_pre202610_20261027/` → 再暂存删除 | §8.13「归档而非删除」；`attic/*` 已 gitignore，不污染索引 |
| `tracking/EUR/` 40 | 40 | **同上**（先核引用：仅 1 个 `.bak` 被引用，且该引用应改指 `cells.json`） | 战役脚本属产物、不该长期入库，但删前要留档 |
| `output_report/` 32 | 32 | 先判「是否仍是活产物」；`EUR_delay1_news85_ideas.md` 被 `tracking/EUR/task_plan.md` 引用 ⇒ 取回或改引用 | 机器产物可归档，但引用要同步 |
| `tracking/EUR/config/cells.json.bak_*` | 含在上条 | **暂存删除 + 文档去掉引用** | 备份件本就不该入库 |

> ⚠ 顺序固定：**先 restore 承重件 → 再归档其余 → 最后才 `git add -u` 暂存删除**。
> 反过来做，`git restore` 就找不到 blob 了（删除一旦暂存，工作树里已无可恢复的副本）。

---

## 3. 其余根因（B–F）

### B. 闸门判据 vs 新增产物（13 条 CI 阻断 + 2 条未跟踪）

- **B1 S14 未登记 10 个**（全部已暂存）：`campaign_report.py`、`gem_pilot_sample.py`、`kor_near_gate_watch.py`、
  `kor_year_probe.py`、`kor_year_sweep.py`、`l1_backfill_validate.py`、`l1_ladder.py`、`prod_wait.py`、
  `reset_low_cov_skips.py`、`submit_rravgrn0.py`。
- **B2 S11 归属 2 个**（已暂存）：`_r24b_sweep.py`、`prod_wait.py` 未进 `tools/THEMES.json`；
  另有 1 个未跟踪非脚本件 `tools/detach_launch.ps1`。
- **B3 S4 盘符 1 个**（已暂存）：`tools/_r24b_sweep.py:16`。
- **B4 skill_lint 18 个新键**：全部 `POISON:equal_weight_leg_add`。其中 **12 个是分母假阳性**
  （`divide(..., add(...))` / `(...)/(...)`）——见 §4-P4，这是本轮唯一「闸判对了但判据错了」的项。
- **B5 `audit_destructive_default` 2 条**：都在**未跟踪**的 `tools/_pvpc_gen_preflight.py:22`
  （模块级 `.dump()` + `open(...,'w')`，另硬编码 `ROOT = r"D:\coding\traeCN_project\wqb"` 并在导入时连生产库）。
  **这是活隐患，但不属 CI 面，归并行会话**。

### C. 文档 / 产物被删，引用与代码还活着

即 §2 的整条链路。补一句：`reports/repo_stale_review_20261019.md:116-118` 自己定的规矩是
「先跑引用扫描，把 0 引用且 ≥30 天的迁 `attic/`」——**当前的 57 份不是这么删的**（0 份留副本、6 份承重）。

### D. 测试隔离机制静默失效（6 条红，含假绿的一半）

`tests/unit/02_workflow/test_pipeline_error_isolation.py:19-27` 在导入前从 `sys.modules` 弹出
`pipeline` / `gate` / `_lib.wqb_store` / `_lib.ledger` / … 共 12 个模块并重新导入 ⇒ 产生**新的模块对象**。
另一个测试（`tests/unit/10_toolkit_scripts/test_field_catalog_cache_completeness.py:84`）用

```python
monkeypatch.setattr(wqb_store, "get_store", lambda ctx=None: store)
```

打在**已被替换的旧对象**上；而 `field_catalog_cache.py` 在调用时才 `from _lib.wqb_store import get_store`
（78/101/171/211/224/250 行）⇒ 解析到新对象 ⇒ 真 `CampaignStore` ⇒ 生产库守卫拒绝 ⇒ **单跑绿、全量红 6 条**。

与 AGENTS.md §8.4 第 9 项同源：**按属性 patch 在模块对象被换掉后不报错，只静默失去作用**。
这次它幸运地「响亮地红」，但同一机理的另一半（patch 打空且该路径不抛错）就是假绿。

### E. 两套活实现 / 三份分叉（结构债，不阻断）

- `tools/wave_gate.py` **1678 行 / 30 个函数**仍在生产路径上跑；`tools/wave_gate_pkg/` 存在
  （`cli.py` 368 行）但**生产代码零 import**，且 `_semantic_gate`（5013 vs 4951 字符）、`_waiver_phase`、
  `_extract_fields_from_expr` **函数体已分叉** ⇒ 两份活的实现。
- `campaign_semantics.py` **三份**：`tools/`（610 行，已暂存，被已暂存的 `tools/full_template_campaign.py:168` import）
  vs `Claude/skills/wq-brain-ra-ind/scripts/ind_campaign/`（642）vs `…/wq-brain-ra-usa/…/usa_campaign/`（642，已跟踪）。
- 196 份 EUR 文档批量进 `docs/reference/EUR/`：若按 §8.13「docs 只放长期规范」，需逐份判它是规范还是某天快照。

### F. 守护探针与代码形态脱节（2 条红，安全面，审计期间新增）

`test_submit_chain_defaults` 的 AST 探针只认 `ast.FunctionDef`，而并行会话把
`workflow_submit_alpha` 改成了 `async def` ⇒ 探针找不到函数、**4 条提交安全默认值断言全部停摆**。
不是代码坏了，是「判据按形态写死」这一类盲区的第 N 次复现（同族：S11 只认 `.py`、
S20 只认索引、S16 只按扩展名取面）。改法与验收见 §4-P10。

---

## 4. P0 — 今天做（每项含命令与验收）

### P0-P1 处置 133 条幽灵路径（**先做，否则提交被 S20 挡死**）

按 §2.5 决策表执行。前两步可以立刻做（无争议）：

```bash
# ① 3 个正当退役 + 1 个改名补齐（4 件，无争议）
git add -u -- tools/backfill_check_columns.py tools/legacy/fix_stale_fk_20260928.py tools/legacy/opswap_driver.py
git add -u -- Claude/skills/wq-brain-ra-eur/references/_probe-sop.md

# ② 取回 6 份承重报告
git restore -- reports/skills_review_20260929.md reports/skills_review_20260929_closure.md \
  reports/alpha_properties_audit_20260920.md reports/code_structure_survey_20260925.md \
  reports/db_mcp_split_20261004.md reports/db_concurrent_write_lock_audit_20260920.md

# ③ 其余 52 份 reports + 32 份 output_report + 40 份 tracking/EUR：先落档，再暂存删除
#    归档脚本写到 logs/_tmp_restore_archive.py（§5 规约），先 --dry-run 打清单人工核，再执行：
#      deleted = git ls-files -d  (按目录过滤)
#      git show HEAD:<path> > attic/reports_pre202610_20261027/<相对路径>
#    核对：落档件数 == 拟删件数，且 0 字节文件为 0
git add -u -- reports output_report tracking/EUR
```

验收：`git ls-files -d | wc -l` = 0；`python tools/audit_structure.py --only s20` 转绿；
`python tools/audit_structure.py --only s16` 的 FAIL 从 20 降到 **6**（剩下的是 6 个 `_ideas_v2.md`，见 P2）或 0（若一并归档）。

> ⚠ **不要**为了「让 S20 变绿」执行 `git add -A`（§7 第 2 条）；也**不要**用 `git checkout -- .`
> 取回——目录级 pathspec 会连带回退他人在 `tools/` 的在途修改。

### P0-P2 被删报告的归档与引用修复

包含在 P1 的 ③，独立列出因为它有自己的验收：

1. 6 份承重件已 restore ⇒ `pytest tests/unit/07_docs_skills/test_closure_ledger.py -q` 3 条转绿。
2. 4 份 `eur_d1_*` 证据链被 `reports/dataset_experience/eur_*_campain.md` 引用：
   若归档，需把这 4 处引用改成 `attic/` 路径（或改为「见 git 历史 <commit>」）。
3. `tracking/EUR/config/cells.json.bak_*` 删除后，`docs/reference/EUR/fundamental72_campaign_20261010.md`
   的引用改为 `cells.json`。

验收：`python tools/code-audit/doc_path_refs.py --include-history` 的 BROKEN 数不高于本次基线（21）。

### P0-P3 CI 钩子步方向反了（**不改，CI 永远不可能绿**）

`.github/workflows/gates.yml` 第 4 步：

```yaml
- name: 钩已挂载自检
  run: sh tools/git-hooks/install.sh --check
```

`install.sh --check` 的判据是 `git config core.hooksPath == tools/git-hooks`；
**干净 runner 上这个值必然为空** ⇒ exit 1 ⇒ 后面所有闸与测试一步都不会跑。
「防止 CI 绿了但本地没钩」的设计，实际效果是「CI 永远不绿」。

```yaml
# A. 先装再查（推荐，语义与原意一致）
- run: sh tools/git-hooks/install.sh
- run: sh tools/git-hooks/install.sh --check
# B. 或者干脆删掉这两步（CI 不需要本地钩子）
```

**另需裁定 runner OS**：`runs-on: ubuntu-latest`，但本仓 Windows 优先（`D:\`、`C:\Users\`、PowerShell、
`.venv/Scripts/python.exe`）。建议先换 `windows-latest` 求「能复现」，或保留 ubuntu 但**首跑全部加
`continue-on-error: true` 只作观测**，拿到基线后再收紧。

验收：`act` 或一次 `workflow_dispatch` 试跑，确认钩子步之后能走到 pytest 并留下日志。

### P0-P4 gate-5 分母假阳性（**需用户裁定**）

**这是本轮唯一「闸判对了但判据错了」**，有真实生产影响。实测（`logs/_tmp_gate5_denom_probe.py`）：

| 表达式 | 期望 | 实测 |
|---|---|---|
| `divide(subtract(a,b), add(a,b))` | 放行 | **blocked** ❌ |
| `(a - b) / (a + b)` | 放行 | **blocked** ❌ |
| `divide(subtract(a,b), add(ts_mean(a,20), ts_mean(b,20)))` | 放行 | **blocked** ❌ |
| `ts_rank(divide(subtract(a,b), add(add(a,b),1)),66)` | 放行 | **blocked** ❌ |
| `divide(add(rank(a),rank(b)), 2)` | 拦 | blocked ✅ |
| `add(rank(a),rank(b))` | 拦 | blocked ✅ |

`(X−Y)/(X+Y)` 是**净额/总额归一化**的标准写法（新 USA profile 文档与真实 alpha 里都有）。
18 个 skill_lint 新键中 **12 个属于这一类**。

修法必须**同时覆盖两个检测器**（否则破坏既有不变量 `test_same_math_different_syntax_is_not_judged_oppositely`）：

| 检测器 | 位置 | 缺的上下文 |
|---|---|---|
| `_detect_equal_weight_leg_add` | `Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py:690`（调用点 514） | 该 `add()` 是否**处于除法分母位** |
| `_detect_infix_leg_sum` | 同文件 :808（调用点 516） | 该 `+` 是否**在除号右侧** |

**请裁定（三选一，代价递增）**：

1. **窄修（推荐）**：两处都加「分母位跳过」——顶层 `/` 或 `divide(x, D)` 的第二参数是 `add(...)`/`+` 时不判等权腿。不影响「加总不同信号」的拦截。
2. 只修 infix 侧：**不可接受**，同数学两种写法结论相反。
3. 关掉 gate-5 等权腿规则：**不可取**，它拦的是真实的过拟合形态（`add(add(D1,D2),add(D3,D4))` 四腿平铺）。

**不要做的事**：不要复活 2026-10-21 那个「同数据集合成豁免」。今天 14:01 另一会话已在
`attic/gate5_atom_exemption_revert_20261027/README.md` 记录其 fail-open 三条原因（`_field_dataset` 只为多数据集批次构建、
infix 判据不一致、测试契约冲突）。**本轮只修分母，不碰豁免。**

验收：上表 6 条全符合期望 + `pytest tests/unit/04_gates/ -q` 全绿 + skill_lint 新增从 18 降到 **6**。

### P0-P5 剩余 6 个 skill_lint 新键（在飞会话处置，**不得改基线**）

| 类型 | 位置 | 处置 |
|---|---|---|
| 同族聚合（需人工判） | `pv149` 67/96、`pv63` 254 | 确为「同族字段加总」→ 按裁定 B（2026-10-22）改写；否则补 `<!-- lint:counterexample -->` |
| 灰色（分母 + 其他） | `pv63` 122 | 随 P4 复测后定 |
| 已记录失败案例 | `atom` 2270/2381（`add(z60, z120)`） | 补 `<!-- lint:counterexample -->` |
| 四腿交付记录 | `atom` 1020、`insider` 40 | 同上 |

**铁律**：`tests/fixtures/skill_lint_baseline.json` **不得更新**——更新等于把违规变成永久豁免通道，
与 §8.12 对 S11/S16「空债面不建基线」同源。这些属 USA 战役在途工作，**由该会话或用户处置**。

### P0-P6 结构面 13 条 / 11 个已暂存文件

| 类别 | 文件 | 动作 |
|---|---|---|
| S14 未登记（10） | 见 §3-B1 | 各在 `tools/README.md` 加一行（场景 / 用法 / 是否一次性） |
| S11 归属（2） | `_r24b_sweep.py`、`prod_wait.py` | 在 `tools/THEMES.json` 补主题归属 |
| S4 盘符（1） | `tools/_r24b_sweep.py:16` | 换 `from wqb.paths import repo_root` |

**不要一次登记 54 个**：其中 52 个未跟踪、属并行会话在途探针，登记等于替别人背书归属。
只登记**已暂存的 2 个**。

验收：`python tools/audit_structure.py --only s4,s11,s14` 在「已暂存件」上零违规。

### P0-P7 14 个已暂存工具的裸 `sqlite3.connect`

`tests/unit/01_store_db/test_db_write_guards.py` 实测指向 **27 个文件、28 处调用**
（`_dataset_report.py` 一个文件占 2 处），
其中 **14 个已暂存**（CI 会红），13 个未跟踪（归并行会话）：

```
已暂存：export_fields_for_tagging.py  full_coverage_gate.py    full_template_campaign.py
        gem_pilot_sample.py          gen_eur_field_profiles.py  gen_llm_field_tags.py
        kor_year_sweep.py            l1_backfill_validate.py    load_field_profiles_to_db.py
        query_profile.py             verify_platform_fields.py
        data-repair/check_usa_os_subset.py  review_alloc_risk.py  review_os_decay.py
未跟踪：_ab_adopt.py _ab_template.py _dataset_report.py _e1_probe_pp.py _grp_rank_probe.py
        _lowcov_status.py _modelfam_probe.py _pvpc_gen_preflight.py _pv_preclose_sweep.py
        _test_carrier_upgrade.py _unlit_sweep.py _wide_probe.py sreq_precheck.py
```

改法：走 `wqb.db_conn`（`src/` 内）或 toolkit `_lib/db.py`（skill 内）——§8.4 第 11 项明令
**三条路径共用一份判定本体，不要复制第三份守卫**。

**同批修 `test_region_query_guard`**：基线钉的 `tools/wave_gate.py:1641` 已漂到 `1411`。
该处 SQL 有 `WHERE d.name=?` 作用域（启发式假阳性）。正确处置 = **重钉行号到 1411**，不删基线条目。

验收：`pytest tests/unit/01_store_db/test_db_write_guards.py tests/unit/01_store_db/test_region_query_guard.py -q` 全绿。

### P0-P8 ASI profile 漂移（1 条）

`Claude/skills/wq-brain-ra-asi/SKILL.md:61` 的 universe 是 `MINVOL1M`，`tracking/ASI/config/settings.json` 是 `TOP500`。
区域 skill 是**生成物**（§8.14），手改无效：

```bash
$WQ_PY -m wqb.profiles render --region ASI --apply
$WQ_PY tools/sync_skills.py --apply
$WQ_PY -m wqb.profiles check
```

验收：`pytest tests/unit/09_core/test_profiles_layer.py -q` 全绿 + `profiles check` 零差异。

### P0-P9 测试隔离机制（D 类，3 行 + 一条不变量）

```python
# tests/unit/10_toolkit_scripts/test_field_catalog_cache_completeness.py
def _patch_store(monkeypatch, store):
    import importlib, sys
    live = importlib.import_module("_lib.wqb_store")   # 取 sys.modules 里的现役对象
    assert sys.modules["_lib.wqb_store"] is live       # 生效断言：patch 必须打在活对象上
    monkeypatch.setattr(live, "get_store", lambda ctx=None: store)
```

**系统性建议（P2）**：`test_pipeline_error_isolation.py` 的「弹出 `sys.modules` 再导入」应改为
**保存 / 恢复**（`try/finally` 放回原对象），或把该用例放进 subprocess。
判据：卸载类用例不得让别人的 monkeypatch 落到悬空对象上。

验收：`pytest tests/ -q` 的 6 条转绿，且单跑仍绿。

### P0-P10 提交工具的默认值守护被 async 改造打盲（**新增：安全面**）

**事实**：并行会话在 2026-10-27 把 `world-quant-brain-mcp/tools_workflow.py` 的
`workflow_submit_alpha` 从 `def` 改成 `async def`（提交假死修复，注释里写明是 P0）。
`tests/unit/05_submit_quota/test_submit_chain_defaults.py` 的 AST 探针只认 `ast.FunctionDef`：

```python
if isinstance(n, ast.FunctionDef) and n.name == func:   # ← async def 是 AsyncFunctionDef
```

⇒ 探针走完没命中，抛 `找不到 workflow_submit_alpha`，**两条用例红**；
而这恰恰是最不该静默的那两条：`confirm_submit is False`（默认只预检不提交）、
`color is None`（GREEN 须挣得）、`robustness_audited is False`（稳健性声明 fail-closed）、
`verify_timeout == WAIT_THRESHOLDS["submit_flip_wait_s"]`。

**为什么归类为安全面而非普通红**：这 4 条断言是**不可逆动作**的最后一道静态保险。
它们现在红，所以看得见；但如果有人按「测试过时」把它删掉或改成 `pytest.skip`，保险就永久消失了。
本轮不改代码，只登记改法。

**改法（3 行）**：

```python
_FUNC = (ast.FunctionDef, ast.AsyncFunctionDef)
...
if isinstance(n, _FUNC) and n.name == func:
```

并加一条**不变量测试**：对 `tools_workflow.py` 里每个 `@mcp.tool()` 装饰的函数，
断言探针都能取到（取不到就红）——否则下次再有 sync→async 改造，还是同一处静默失守。
同族盲区已排查：`tests/unit/07_docs_skills/test_se_docs.py`（4 处）、`test_sf_docs.py`（1 处）
也都是 `ast.FunctionDef` 单条件，但它们扫的是 `feature_engineering` / `skill_eval` 等**同步**函数，
当前不受影响；改法相同，可一并加固（P2）。

验收：`pytest tests/unit/05_submit_quota/test_submit_chain_defaults.py -q` 4 条全绿，
且把 `workflow_submit_alpha` 临时改回 `def` 后仍绿（两个形态都要能读到）。

---

## 5. P1 — 本周（拆分与回收）

### P1-P10 按主题拆提交（独立 worktree 里做）

当前索引 = **466 件纯新增**，可拆性比审计开始时（764 件混合）好得多。但仍然跨 7 条工作流：

| 序 | 主题 | 内容 | 前置 |
|---|---|---|---|
| 1 | `chore(gates)` | `.github/workflows/gates.yml`（修完 P3）+ 四闸脚本 + 其测试 | 无 |
| 2 | `feat(usa)` | `Claude/skills/wq-brain-ra-usa/**`（105）+ 相关 docs/reports | P5 处置 |
| 3 | `feat(ind)` | `Claude/skills/wq-brain-ra-ind/**`（17）+ runbook + `reports/ind_*` | P14 裁定 |
| 4 | `feat(eur)` | `Claude/skills/wq-brain-ra-eur/**` + `docs/reference/EUR/**`（196，先定去向） | P13 |
| 5 | `chore(tools)` | `tools/` 53（**先做完 P6 登记与 P7 连接改造**） | P6/P7 |
| 6 | `chore(tests)` | `tests/` 20 新增 | 依赖 2–5 的实现 |
| 7 | `chore(cleanup)` | 报告/产物的归档与删除 | P1/P2 |

**必须在独立 worktree 里做**（`git worktree add ../wqb-gov-split gov-split-20261027`），理由有三：
① 索引已被证明会被并行会话重置（§1.1）；② 开发树有未跟踪在途件；③ 拆分过程要反复 `restore`，
在共享树里做会让别人看到文件瞬间消失（§8.4 第 10 项的事故形态）。

每提交前：`pytest tests/ -x -q` + `python tools/audit_structure.py` + `python tools/sync_skills.py --check`。

> ⚠ **不要**先 `git commit` 再「以后拆」——那会把 7 条工作流固化成一个历史节点，bisect 失效。

### P1-P11 磁盘回收（≈533 MiB + git 对象）

```bash
$WQ_PY tools/retention.py            # dry-run，确认「要删的那份备份」是旧的
$WQ_PY tools/retention.py --apply    # 需用户点头
git gc --prune=now                   # 回收 351 个 tmp_obj + 160 个 prune-packable
```

**不要动** live `wqb.db` 与 `-wal`/`-shm`（`test_retention.py` 硬保护）。

### P1-P12 `tracking/EUR` 40 个删除先核引用

见 §2.5。唯一被引用的是 `cells.json.bak_*`（文档指着它）——那说明**文档本身该改**，
而不是把 `.bak` 留在版本控制里。

### P1-P13 196 份 EUR 文档的位置（需定策）

`docs/reference/EUR/` 新增 196 份。§8.13 判据：**读者会不会照它长期做决定**——
会且长期有效 ⇒ `docs/`；某天快照 ⇒ `reports/`；战役自动产物 ⇒ `output_report/`。
建议先按文件名分桶抽检 20 份定规则，再批量；不要 196 份一起塞进 `docs/` 再说。

### P1-P14 `tools/` 战役栈：退役还是活的（**需用户裁定**）

| 方向 | 证据 |
|---|---|
| 退役 | `docs/reference/ind_campaign_runbook_20261025.md:9/62/761` 明写 `tools/campaign_supervisor.py`、`tools/wqb_campaign/fields.py` 已迁 / 不再存在 |
| 活的 | 同 runbook 的 `:69/:70/:581` 仍在使用这两个路径；`tools/campaign_semantics.py`（610 行）**已暂存**且被同样**已暂存**的 `tools/full_template_campaign.py:168` import |

- 判退役 ⇒ 这批已暂存工具应出索引并归档，runbook 三处历史行补 `已迁` 关键词（顺带清 2 条 doc_path_refs）。
- 判活的 ⇒ 修 runbook 的三处「已迁」表述。

不能两个都留。这也是 4 条文档死指针的根源。

### P1-P15 `campaign_semantics.py` 三分叉收敛

先 `diff` 定位 32 行差在哪：若是区域常量 ⇒ 抽到 `tracking/<R>/config/`（§8.14「区域差异写数据不写代码分支」）；
若是纯重复 ⇒ 保留 skill 版（可随 skill 安装生效），`tools/` 版改为 import。

---

## 6. P2 — 结构债（分批，不急但持续放血）

| # | 债 | 实测 | 建议 |
|---|---|---|---|
| P2-16 | **`wave_gate` 两套活实现** | `tools/wave_gate.py` 1678 行 / 30 函数；`wave_gate_pkg/cli.py` 368 行；生产零 import pkg；`_semantic_gate` 等三函数已分叉 | 二选一：① 完成 pkg 化并删旧实现（先跑 `validate_argv` 契约与 `_compat` 晚绑定测试）② 归档 pkg，明确 `tools/wave_gate.py` 是唯一实现 |
| P2-17 | **AGENTS.md 该条失实** | 第 995 行称 `tools/wave_gate.py` 是「~140 行入口 shim」，实际 1678 行 | 随 P2-16 结论一并改写 |
| P2-18 | **S16 机器产物豁免漏版本号** | `S16_MACHINE_SUFFIXES = ("_ideas.md", "_campain.md")` 是 `endswith` 精确匹配 ⇒ `_ideas_v2.md` 不豁免 | 扩成前缀+版本正则（`_ideas(_v\d+)?\.md`），或生成器改名 `_ideas_<YYYYMMDD>.md` |
| P2-19 | **262 处 `sys.path` 注入** | S1 WARN 基线内 | 新脚本直接 `from wqb.…`；存量按「单文件迁移配方」逐次顺手换，**不批改** |
| P2-20 | **4 组跨 skill 同名副本** | `ace_lib.py`/`diversity_enhancer.py`/`helpful_functions.py`/`validator.py` | 改任一份必须四处同覆盖；建议加一条内容哈希一致性测试替代人工记忆 |
| P2-21 | **S16 基线 20 条存量** | 基线内 | 新建即守，存量不回改；但**清理基线前必须先确认工作树完整**（§2.2 的坑） |
| P2-22 | **`skill_lint` 键截断致计数偏差** | 键 = `check\|file\|norm[:80]\|msg[:60]`，pv103 的 4 行塌成 1 键 ⇒ 打印 19 行 / 计 18 个 | 改 summary 为「新增 N 键 / M 行」或键里加行号 |
| P2-23 | **`wqb_db_mcp.py` 拆分** | §8.4 第 9 项已实测回滚（6 类耦合，2 类会写坏数据 / 造假绿） | **不要拆** |
| P2-24 | **`output_report/` 两个未跟踪件命名违规** | `s0_select_usa.json`、`webdata_usa_d1.csv` | ✅ 2026-10-27 已改名：`s0_select_usa_20261027.json` / `webdata_usa_d1_20261027.csv` |
| P2-25 | **`docs/env_and_switches.md` 2 条 UNTRACKED 提示** | 指向 `src/wqb/prod_queue.py`、`tools/wqb_tools_shim.py`（均未跟踪） | 二选一：入库，或按 P14 同型判定后从文档删除 |
| P2-26 | **AGENTS.md 体量** | 单文件承载 §1–§8.14 全部治理规约 | 不建议现在拆（大量文档按行号引用它）；若拆，做成「索引 + 分册」并保留原锚点 |

---

## 7. 明确不要做的事

每条在本仓都有已发生的代价，不是泛泛而谈：

1. **不要 `git clean`（任何 flag）** —— `tools/` 一次丢过 17 个被文档引用的脚本，`docs/experience/02_signal_patterns.md` 丢过 332 行，均**从未入库，救不回来**。
2. **不要 `git add -A` / `git add .`** —— 889 行工作树 + 并行会话，会把别人的在途件拖进你的提交。
3. **不要 `git checkout -- tools/`** 或任何目录级 pathspec —— 会连带回退他人在该目录的 30+ 在途修改件。
4. **不要 `git stash`** —— 多会话共享一棵树，会卷走别人的改动。
5. **不要先暂存删除再 restore** —— 删除一旦进索引，工作树里已无可恢复副本（§2.5 的顺序）。
6. **不要更新任何基线**（`skill_lint_baseline.json` / `audit_structure_baseline.json`）来消红 —— 等于给空债面留永久豁免通道。
7. **不要复活「同数据集合权腿豁免」** —— `attic/gate5_atom_exemption_revert_20261027/` 已记三条 fail-open 原因。
8. **不要拆 `wqb_db_mcp.py`** —— 6 类耦合已实测。
9. **不要移动 / 删除 97 个未跟踪件** —— 其中 53 个是 `tools/` 顶层探针，属并行会话在途工作。
10. **不要删 DB 行 / 删备份 / 跑 `git gc`** —— 不可逆写操作，须用户确认。
11. **不要读 / 打印 / 提交 `.env`**，不要 `--no-verify` 绕钩，不要改 `tracking/mining/`。
12. **不要为过闸而改判据方向** —— 本轮 2 条 doc_path_refs 是措辞假阳性、4 条是 runbook 自述历史，
    正确处置是**补措辞关键词**（`不存在` / `已迁`），不是删文档、更不是删检查。

---

## 8. 局限与未验证项

1. **CI 从未真正执行过**。P3 的「永远不绿」是读 `install.sh --check` 退出码语义的**静态推断**；
   `ubuntu-latest` 上 `audit_structure` / `pytest` 的行为**完全未知**。
2. **所有计数是单点快照**，且审计期间索引被并行会话重置过一次（§1.1）、测试红从 16 漂到 18（§1.3）。
   数字漂移属正常，**不要**把本文
   数字写进其他文档当基线（本仓已有 171/159 对不上的先例，§8.12 明令「计数以工具输出为准」）。
3. **`test_field_catalog_cache_completeness` 的 6 条红**是「测试顺序确定性」结论，依赖 pytest 收集顺序；
   换 CI 可能不复现，也可能换个形态复现。需一次真 CI 确认。
4. **133 条的「外部引用」扫描是文件名级**（`git grep -F <basename>`），会漏「按路径目录引用而非全名」的写法，
   也会有同名碰撞（如 `_probe-sop.md` 在 DEU/GBR/KOR 各有一份，已人工排除）。
5. **未审计的面**：`research-data/` 与 `extensions/`（gitignore、只读）、`cache/` 内部结构、`attic/` 各归档包内容、
   MCP 包测试（`world-quant-brain-mcp/tests/` 需独立 venv，本轮未跑）、`docs/` 正文陈述是否为真（只查了路径存在性）。
6. **`tools/_pvpc_gen_preflight.py` 的 2 条高危未处置** —— 属并行会话，仅登记。
7. **备份「哪份更新」是按大小推断的**，`retention.py` dry-run 时才按 mtime 定。

---

## 9. 复现命令

```bash
# 结构与闸（与 pre-commit / CI 同源）
python tools/audit_structure.py
python tools/audit_structure.py --only s4,s11,s14     # 只看 CI 会拦的三项
python tools/audit_structure.py --only s16,s20        # 只看本地红的两项
python tools/code-audit/doc_path_refs.py              # 注意：未暂存删除时假绿
python tools/code-audit/doc_path_refs.py --include-history
python tools/skill_lint.py
python tools/code-audit/audit_destructive_default.py

# 幽灵路径与引用面
git ls-files -d                                       # 133 条
python logs/_tmp_ghost_refs.py                        # 本轮新增：133 条的外部引用扫描

# 测试面
python -m pytest tests/ -q --no-header
python -m pytest tests/unit/05_submit_quota/test_submit_chain_defaults.py -q                              # 2 条红：AST 不认 async def
python -m pytest tests/unit/10_toolkit_scripts/test_field_catalog_cache_completeness.py -q                 # 单跑应绿
python -m pytest tests/unit/02_workflow/test_pipeline_error_isolation.py \
                 tests/unit/10_toolkit_scripts/test_field_catalog_cache_completeness.py -q                 # 连跑应变红（复现 D 类）

# gate-5 分母探针（本轮新增）
python logs/_tmp_gate5_denom_probe.py

# 索引 / 磁盘
git status --porcelain | cut -c1-2 | sort | uniq -c
git diff --cached --name-only | wc -l
git ls-files -o --exclude-standard | wc -l
ls -l data/*.bak* ; python tools/retention.py        # dry-run
git count-objects -v
```

**本轮创建的临时脚本**（全在 `logs/`，gitignored，可随时删）：
`_tmp_gov_snapshot2.py`（分区统计）、`_tmp_ghost_refs.py`（幽灵路径引用扫描）、
`_tmp_s16_new.py`（S16 新违规逐条）、`_tmp_gate5_denom_probe.py`（分母假阳性探针）、
`_tmp_gov_ci_face.py`（CI 面）、`_tmp_gov_lint_rows.py`（lint 行级）、
`_tmp_naked_split2.py` / `_tmp_naked_state.py`（裸 sqlite 站点与暂存归属）；
抓取输出 `_tmp_audit_full2.txt`、`_tmp_ghosts.txt`、`_tmp_naked_sites2.txt`、`_gov_pytest_20261027*.log` 等。

> ⚠ **上面这些探针已在收尾时按 §8.13「一次性脚本用完即删」清掉**（`logs/` 本就不入版本控制），
> 所以本节命令**不能照抄复跑**。唯一被常驻化的是分母位那一组：
> `tests/unit/04_gates/test_gate5_denominator_masking.py`（22 例，见 §10.3）。

> 附注：`reports/` 属 doc_path_refs 的**非活文档面**（`LIVE_PREFIX` 只含 `docs/` 与 `Claude/skills/`），
> 故本文引用的已删路径不会被该闸判成死指针——不需要为本文补豁免词。

---

## 附录 A：精确清单

### A.1 CI 会拦的 13 条结构违规（11 个已暂存文件）

| 闸 | 文件 | 说明 |
|---|---|---|
| S4 | `tools/_r24b_sweep.py:16` | 硬编码盘符 |
| S11 | `tools/_r24b_sweep.py`、`tools/prod_wait.py` | 2026-10-26 冻结后新增顶层脚本 + 无 `THEMES.json` 归属 |
| S14 | `campaign_report.py` · `gem_pilot_sample.py` · `kor_near_gate_watch.py` · `kor_year_probe.py` · `kor_year_sweep.py` · `l1_backfill_validate.py` · `l1_ladder.py` · `prod_wait.py` · `reset_low_cov_skips.py` · `submit_rravgrn0.py` | 未在 `tools/README.md` 登记 |

（另有 `tools/detach_launch.ps1` 属未跟踪件，不进 CI 面。）

### A.2 skill_lint 19 行 / 18 键（全为 `POISON:equal_weight_leg_add`）

| 类型 | 位置 | 件数 |
|---|---|---|
| 分母假阳性（P4 修） | `pv103` 156/157/158/232 · `pv63` 120 · `pv63` 122(灰) · `other359` 88/93/94 · `news` 142 · `board-gov` 309 · `pv149` 93 | 12 |
| 同族聚合（P5 判） | `pv149` 67/96 · `pv63` 254 | 3 |
| 已记录失败案例 | `atom` 2270/2381 | 2 |
| 四腿交付记录 | `atom` 1020 · `insider` 40 | 2 |

均在 `Claude/skills/wq-brain-ra-usa/references/` 下。

### A.3 18 条测试红的归属

| 用例 | 条数 | 类 | 处置 |
|---|---|---|---|
| `test_field_catalog_cache_completeness` | 6 | D | P0-P9 |
| `test_closure_ledger` | 3 | C | P0-P1 ② |
| `test_submit_chain_defaults` | 2 | F | P0-P10（`AsyncFunctionDef` 盲区，审计期间新出现） |
| `test_db_write_guards` | 1 | B | P0-P7（27 文件 / 28 处） |
| `test_region_query_guard` | 1 | B | P0-P7（重钉 1641→1411） |
| `test_skill_lint` | 1 | B | P0-P4 / P5 |
| `test_profiles_layer` | 1 | B | P0-P8 |
| `test_audit_structure_s11_dataface` | 1 | **本机** | 未跟踪 `tools/detach_launch.ps1` |
| `test_docs_consistency` | 1 | **本机** | 未跟踪 `docs/reference/glb_campaign_runbook_20261026.md` 硬编码 `~/.workbuddy/skills/…` |
| `test_sd_portability` | 1 | **本机** | 15 个未跟踪探针硬编码 `D:\` / `C:\Users\` |

合计 **6+3+2+1+1+1+1+1+1+1 = 18**。汇总行：`18 failed, 3811 passed, 72 skipped, 1 warning in 266.53s`。

**后 3 条在干净克隆上不可复现**（未跟踪件不在 CI 的检出面上），由产出它们的会话处置。

### A.4 133 条幽灵路径按目录

```
reports/          57
tracking/EUR/     40
output_report/    32
tools/             3   （正当退役：backfill_check_columns.py + legacy 2 个）
Claude/skills/…    1   （改名未完成：wq-brain-ra-eur/references/_probe-sop.md）
```

其中 **38 条有外部提及**，承重 10 条见 §2.4；**95 条零外部引用**。

---

## 10. 修复执行记录（2026-10-27 晚，用户裁定「全部修复」）

> §0–§9 保持修复前快照不动。本节给**做了什么、和报告建议差在哪、现在是什么读数**。

### 10.1 总览

| 项 | 状态 | 修复后验收 | 与报告建议的偏差 |
|---|---|---|---|
| P0-P1 133 条幽灵路径 | ✅ | `git ls-files -d` = **0**；S20 绿；S16 FAIL **0** | restore 6→**33**、归档 123→**100**（引用面实测多于估计，见 10.2） |
| P0-P2 报告引用 | ✅ | `test_closure_ledger` **4 passed**；`doc_path_refs` 默认模式 BROKEN 16（基线 12，+4 均非本例引入） | 报告写的 `--include-history` 不是可用口径（536 条，历史文档本来就在引旧路径） |
| P0-P3 CI 钩子步 | ✅ 代码面 | 改为「`sh -n` + 装→查」；新增未验证项注释 | **未**加 `continue-on-error`；runner OS 仍待用户裁定（见 10.7） |
| P0-P4 gate-5 分母 | ✅ | 新增 22 例常驻回归（含变异反查）；`tests/unit/04_gates/` **252 passed**；lint 18 键 → **7 键** | 实际清掉 **11 行 / 11 键**，不是 12（`pv63:122` 不是分母，见 10.3） |
| P0-P5 剩余 lint 键 | ⏸ 按原建议留给 USA 会话 | 仍 **8 行 / 7 键** | 未改 `skill_lint` 基线，未动他人 4 份在途文档 |
| P0-P6 结构面 | ✅ | S14 / S11 / S4 在**已暂存件**上零违规 | 只登记已暂存的 2 个归属；52 个未跟踪脚本不代登记（§8.4 第 10 项） |
| P0-P7 裸 `sqlite3.connect` | ✅ | 14/14 改走 `wqb.db_conn`；两个守卫用例绿；行号重钉 `wave_gate.py:1411` | `data-repair/` 下 2 个同批改掉 |
| P0-P8 ASI profile 漂移 | ✅ | `SKILL.md` universe = TOP500，与 `settings.json` 一致（生成物重渲） | 未手改生成块 |
| P0-P9 测试隔离 | ✅ | 6 条转绿（全量复测见 10.6） | 采纳「取现役模块对象 + 生效断言」 |
| P0-P10 提交守护 `async` 盲区 | ✅ | 4 条安全断言回绿 + 新增「探针能取到每个 `@mcp.tool()`」不变量 | 两种 `def` 形态都认，断言本身未放松 |

### 10.2 P0-P1 执行细节

**为什么 restore 从 6 变 33**：报告 §2.4 只核出 38 条有外部提及、其中 10 条承重。执行时对 133 条做了
**全仓活文件扫描**（8,385 个文件，排除同批被删件与 `.workbuddy/` / `.claude/` 私有记录），实测
**50 条有活引用**。多出的引用方主要是报告没扫到的两类：

- `docs/governance/snapshot_adjudication.md` 的 `rule` 行**逐字引用**取证文件
  （`reports/db_schema_audit_20260826.md`、`db_table_structure_review_20260826.md` 等）——
  删掉它们会让「抢救点裁决台账」自身失去依据；
- `tools/step_funnel.py:25`（代码注释）依赖 `db_schema_audit_20260826.md`、
  `docs/governance/output_dirs_taxonomy.md` 依赖 `output_report/USA_1_news_sentiment_nlp_ideas.md`。

⇒ 50 条里 **33 条 restore**（全部有活引用）、另 17 条引用方自身也在同批被删（dead-to-dead）随大流归档。
最终 **restore 33 / 归档+删除 100**。

**执行的命令**（一律显式路径，未用任何目录级 pathspec）：

1. `git restore -- <33 个路径>` —— 恢复后与 HEAD blob 逐字节一致（`git status` 对这 33 个路径零输出）；
2. 归档：`attic/reports_pre202610_20261027/<path>` ← `git show 02bd3c9:<path>`，
   **100 件 / 967,248 B / 0 字节文件 0 个 / 逐件回读一致**；目录分布
   `tracking/EUR` 40 · `output_report` 30 · `reports` 26 · `tools`(含 legacy) 3 · skills 1；
   `attic/` 整目录 gitignore，不污染索引；README 记了清单、来源提交与恢复方法；
3. `git add -u -- <100 个显式路径>` —— **没有**照抄 §4-P1 的
   `git add -u -- reports output_report tracking/EUR`：目录级 pathspec 会把他人在三个目录下的
   在途修改一起拖进暂存面（§7 第 1/2 条）；
4. `docs/reference/EUR/fundamental72_campaign_20261010.md:154` 的 `.bak` 引用已改指
   `tracking/EUR/config/cells.json`（附 attic 存档路径），不留死指针。

**S16 的两个更正**：

- 报告预测「S16 由 20 降到 6（剩下 6 个 `_ideas_v2.md`）」**不成立**：那 6 个 `_ideas_v2` 与
  `IND_wave131_feature_engineering.md`、`d9_status_backfill_rollback_20260928_batch2.json` 等
  **恰好是零引用件**，已随 14 条一起归档出库，基线条目也随之消失；
- 真正留下的是 **6 个 restore 回来的承重件自己的命名违规**：4 份 `eur_d1_*` 证据链 +
  `skills_review_20260929_closure.md`（`tools/closure_ledger.py` 直接读写）+
  `financing_mode_b1.md`（仅有测试夹具提及）。它们**早于 2026-10-08 冻结**，属 §8.13
  「存量不强制回改」，改名会打断 `reports/dataset_experience/eur_*_campain.md` 与
  `closure_ledger` 的已知引用 ⇒ 按存量**回登** `s16_naming_violations`，并把 10-26 那次
  「可删」的判断错误写进 `_s16_note`（ghost ≠ 已删，§8.4 第 9 项的老教训）。
  相对 HEAD 的 40 条 → **26 条**，仍只减不增（14 条随真删除出库）。

### 10.3 P0-P4 实现与实测

`Claude/skills/wq-brain-campaign-toolkit/scripts/gate.py` 新增四个辅助函数
（`_paren_close` / `_operand_span` / `_top_level_arg_spans` / `_denominator_spans` + `_mask_denominators`）：

- 分母位 = 中缀 `/` 的右操作数 + `divide(x, D)` 的第二实参；**引号内**（`range="0,1,0.1"`）的 `/` 不算；
- 两个检测器都先 `_mask_denominators()` 再判（分母内容替换成常量 `0`，`_is_signal_leg` 判为非腿），
  函数式与中缀走同一套 mask ⇒ 不破坏 `test_same_math_different_syntax_is_not_judged_oppositely`；
- **价差收集仍走原式**（否则 `subtract(a,b)/(a+b)` 的价差判定会被 mask 掉）；
- `GATE_CODE_VERSION` `2026-10-03.1` → **`2026-10-27.1`**，让逐条缓存失效（否则旧缓存给出旧结论）。

验收实测：报告 §4-P4 表中 6 条 + 4 组函数式/中缀同判 + 6 条不回归 = **16/16 符合期望**
（当时的临时探针，收尾时已删——可复跑的版本就是下面这份常驻用例）。

**同一批已固化成常驻回归**：`tests/unit/04_gates/test_gate5_denominator_masking.py`（22 例，
`check_one` 全链路而非只调检测器），含三组必须保留的用例与两条防伪绿：

- 分母位 9 例必须放行 / 真混腿 6 例必须拦（**分子位混腿 + 分母归一化同现**的
  `divide(add(rank(a),rank(b)), add(c,1))` 也必须在拦的一侧）；
- **变异反查** `test_masking_is_what_makes_the_difference`：把 `_mask_denominators` 换成恒等函数后
  `(a-b)/(a+b)` 必须重新判毒 —— 否则「掩码被删、恰好别处改松」也会让第一组全绿，绿得来源不明；
- `GATE_CODE_VERSION` 取「不早于 2026-10-27.1」（**不等值**断言，以后再 bump 不该变红）。

`pytest tests/unit/04_gates/ -q` = **252 passed**（原 230 + 新增 22）；
`tools/sync_skills.py` 同步 5 文件 → 5 个安装位，`--check` 零漂移。

`skill_lint` 实测 19 行 / 18 键 → **8 行 / 7 键**（清掉 11 行 / 11 键）。更正报告 §A.2：
`pv63:122` 被记为分母类，实测其**分子** `add(nibw, wain)` 是真正的同族字段加总，不是分母，
故不在本次修复范围——剩余 8 行正好就是 §4-P5 列的那 8 行。

### 10.4 其余各项的一句话交付

- **P0-P3**：`.github/workflows/gates.yml` 的钩子步改为
  `sh -n pre-commit && sh -n commit-msg && install.sh && install.sh --check`——干净 runner 上
  「装→查」必然通过，验的是安装器与钩脚本本身能用；文件头补了「runner OS 未验证、
  首跑只取证、不得加 `continue-on-error`」的注释。
- **P0-P6**：`tools/README.md` 补登 10 个已暂存脚本（场景 / 用法 / 一次性提示，含
  `campaign_report.py` 的「无 argparse，传任何参数都会直接开跑」警示）；`tools/THEMES.json`
  补 `prod_wait.py` / `_r24b_sweep.py` 主题归属；`_r24b_sweep.py:16` 的盘符换 `repo_root()`。
- **P0-P7**：14 个已暂存工具全部改走 `wqb.db_conn`（`data-repair/` 下 2 个同批）；
  `test_region_query_guard.py` 的行号基线 **1641→1411 重钉**（不删条目，启发式假阳性按原位跟随）。
- **P0-P8**：`$WQ_PY -m wqb.profiles render --region ASI --apply` 重渲后
  `SKILL.md` 的 universe 由 `MINVOL1M` 变为 `TOP500`，与 `tracking/ASI/config/settings.json` 一致；
  `tools/sync_skills.py --apply` + `profiles check` 零差异。
- **P0-P9**：`test_field_catalog_cache_completeness.py` 的 `_patch_store()` 改为
  `importlib.import_module("_lib.wqb_store")` 取**现役模块对象**，并断言
  `sys.modules["_lib.wqb_store"] is live`（patch 打空立即红，不再静默）。
- **P0-P10**：`test_submit_chain_defaults.py` 的 AST 探针改为
  `isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))`；新增
  `test_probe_sees_every_mcp_tool_in_tools_workflow`——探针枚举 `@mcp.tool()` 函数时
  **故意不复用同一个常量**，这样被测探针再收窄成只看同步函数时会立刻红。

### 10.5 修复后四道闸（2026-10-27 晚实测）

| 闸 | 读数 | 归因 |
|---|---|---|
| `tools/audit_structure.py` | **FAIL 53 / WARN 4**（修前 58 / 5） | FAIL = S11 **2** + S4 **51**，**全部落在 52 个未跟踪的 `tools/*.py`**（并行会话在途探针）；**已暂存件零违规**。WARN = S1 存量 267 处 `sys.path`（设计内）+ S16 基线 26 条存量 + 2 条未跟踪在途件 + S6 4 组已知副本 |
| `tools/code-audit/doc_path_refs.py`（默认模式） | BROKEN **16**（基线 12）· UNTRACKED 2 | +4 全部来自并行会话：staged `ind_campaign_runbook_20261025.md` 引用 2 个不存在的 `tools/` 路径；`.github/copilot-instructions.md`（skill 文档引用，盘上已无该文件）；`output_report/brain-alpha-judge`（`docs/env_and_switches.md`，该文档正被他人在途修改）。**与 P1 的删除无关**（P1 的 133 条均不在其列） |
| `tools/skill_lint.py` | **新增 7 键 / 8 行**（修前 18 键 / 19 行） | 全部在 4 份 **USA 在途文档**：`_usa-atom-delivery-log-20261020.md` 1020/2270/2381、`_usa-insider-field-profile-20261022.md` 40、`_usa-pv149-field-profile-20261023.md` 67/96、`_usa-pv63-order-flow-field-profile-20261020.md` 122/254（= §4-P5 原表）。基线未动 |
| `tools/code-audit/audit_destructive_default.py` | **新增 2 条** | 同一个未跟踪件 `tools/_pvpc_gen_preflight.py:22`（模块级 `.dump()` + `open(...,'w')`），归并行会话 |
| `tools/sync_skills.py --check` | ✅ 全部受维护安装位一致 | — |
| `tools/audit_node_registration.py` | ✅ 五处一致，无漂移 | — |

### 10.6 全量测试（`pytest tests/ -q --tb=short`，2026-10-27 晚）

```
4 failed, 3850 passed, 71 skipped in 226.40s (0:03:46)
```

（这是把 P4 的 22 例新回归一并计入后的终态；未含新用例那一次是 `4 failed / 3828 passed / 71 skipped`，
逐红结论完全一致。3850 − 3828 = 22 = `test_gate5_denominator_masking.py` 的用例数。）

修前基线是 **18 failed / 3811 passed / 72 skipped**，净清 **14 条**：P9 6 + P2 3 + P10 2 +
P7 的 `test_region_query_guard` 1 + P8 的 `test_profiles_layer` 1 + `test_audit_structure_s11_dataface` 1。
最后那条不是本轮改的：工作树里同日出现 `.ps1` / `.sh` 归脚本（`TOOLS_TOP_SCRIPT_SUFFIXES`）
的未暂存改动 ⇒ `detach_launch.ps1` 不再被当作「未登记数据件」。**该改动不属 P0 项、本轮未暂存也未认领**。

剩余 4 条**全部可归因，无一由本轮改动引入**：

| 用例 | 归因 | 机器判据 |
|---|---|---|
| `test_db_write_guards::test_no_naked_connect_outside_whitelist` | 剩余 **14 处**裸 `sqlite3.connect` 全在 `tools/` 的**未跟踪**在途探针（`_ab_adopt.py`、`_wide_probe.py`、`sreq_precheck.py`、`_pvpc_gen_preflight.py` …） | 逐个 `git ls-files --error-unmatch` = 全部 untracked；本轮 P7 清掉的 14 个已暂存件**一处都不再出现**（28→14，正好是清掉的那一半） |
| `test_docs_consistency::test_no_hardcoded_skill_root_in_docs` | 未跟踪 `docs/reference/glb_campaign_runbook_20261026.md:4,17` 硬编码 `~/.workbuddy/skills/wq-brain-ra-glb/scripts/` | 干净克隆不可复现（未跟踪件不在检出面） |
| `test_sd_portability::test_no_author_drive_paths_in_runtime_string_constants` | **20 处**盘符全在未跟踪件（`_ab_adopt` / `_e1_probe_pp` / `_grp_rank_probe` / `_detach_probe` 等，含 4 个非下划线前缀的新探针 `attribution_scan.py` / `backfill_year_profile.py` / `hook_selftest.py` / `wqb_tools_shim.py`） | 同上；比 §A.3 记的 15 处多 5 处，是并行会话同期新增 |
| `test_skill_lint::test_no_new_skill_lint_violations_and_baseline_never_goes_stale` | **8 行 / 7 键**，全在 4 份 **USA 已跟踪在途文档**（即 §4-P5 原表） | 基线 `skill_lint_baseline.json` 未动；归属 USA 会话 |

**时长口径**：中间那一次跑到 **756.82s**，是并行会话同时占机（当时本机另有三批 venv python 在跑）
造成的；终态复跑 **226.40s**，与旧基线 266.53s 同量级 ⇒ **不判性能回归**。
若用中间那次当基线会得出「慢了 2.8 倍」的错误结论——取耗时要挑空载。

### 10.7 仍未闭合（需用户 / 对应会话）

1. **P0-P5 的 8 行 lint**：4 份 USA 在途文档（已暂存），按 2026-10-22 裁决 B 改写表达式或
   补 `<!-- lint:counterexample -->`；**`tests/fixtures/skill_lint_baseline.json` 不得更新**。
2. **CI runner OS 裁定**（§4-P3 后半）：`ubuntu-latest` vs `windows-latest`。代码已改成「首跑可取证」，
   但「能否在 ubuntu 上跑完全套」只能由一次 `workflow_dispatch` 回答。
3. **52 个未跟踪顶层脚本 + `detach_launch.ps1` + `_pvpc_gen_preflight.py`**：S11/S4/destructive 的
   全部剩余红都源自它们。按 §8.4 第 10 项归产出会话（下沉 `tools/<主题>/`、或迁
   `tracking/<REGION>/scripts/`、或归档；`_pvpc_gen_preflight.py` 另需加干跑闸）。
4. **4 条 doc BROKEN**：归各自文档的写入方（见 10.5 第三行的归因）。
5. **P1/P2 档建议**（拆分提交、≈533 MiB 回收、EUR 文档定策、`tools/` 战役栈去留、
   `campaign_semantics` 三分叉、`wave_gate` 两套活实现）均**未动**，仍在 §5/§6 待议。
6. ⚠ **上面这 4 条会直接卡住 pre-commit**：钩子第 ⑥ 步是 `pytest tests/ -x`，红一条即 BLOCKED。
   也就是说**在本机清掉这 4 条之前，任何提交都过不去**（`--no-verify` 是红线，别用）。
   它们的共同入口是同一批未跟踪件 ⇒ 优先让产出会话把 52 个 `tools/*.py` 处置掉（下沉 / 迁走 / 归档），
   4 条里会有 3 条随之消失；第 4 条（USA lint）另由 USA 会话处置。

**本轮没有提交**：`git status` 里那 100 条归档删除**已暂存**（S20 要它；`git ls-files -d` = 0，
其中 1 条被 git 的重命名检测显示成 `R`，用 pathspec 单查仍是 `D`），其余改动
（代码 / 基线 / 本报告 / 新增测试）**未暂存**。怎么切提交按 §7 由用户定。
