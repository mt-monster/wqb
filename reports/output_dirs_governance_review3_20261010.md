# 输出目录规范复核（第三轮 · 2026-10-10）

## 处置状态（2026-10-10 收尾，用户批准全部修复）

| 项 | 动作 | 结果 |
|---|---|---|
| **P1-A** tracking 带杠复发 | `git mv tracking/2026-10-09_robustness.md tracking/robustness_20261009.md` + S16 补**未跟踪件 WARN 预检** | ✅ tracking 顶层带杠件 0；预检上线即逮到 `output_report/deu_t4_targets.json`（并行会话在途），证明「写盘即见」 |
| **P1-B** results/ 结论类 md | 8 份 `.md` 迁入 `reports/`（断点 json 未动） | ✅ `results/` 已无 `.md` |
| **P2-C** 同名文件+目录 | 目录加 `_refs` 后缀（`.md` 主体不动——`closure_ledger.py` + tests + skills 文档 20+ 处引用） | ✅ 4 处引用已同步 `_refs` |
| **P2-D** 文档↔实现漂移 | S16 补规则④「人工报告必须有日期」+ `S16_MACHINE_SUFFIXES` 机器产物豁免；AGENTS.md §8.13/§8.12 改为「有日期则作后缀 / 人工报告必须有日期」 | ✅ 文档与实现收敛；5 个新测试守护 |
| **P3-F** skill 引用未入库脚本 | 不改（`skeleton_panel.py` 是并行会话在途 `A`，非我改动集；治它要改 skill 文档，超出本治理） | ⏸ 记录 |

验证：`audit_structure FAIL=0`、`doc_path_refs BROKEN 0 / UNTRACKED 0`、S16 测试 21 passed、
全量 `3155 passed, 5 failed`——5 个失败全在 `tests/unit/01_store_db/`（`logs/_dblock` 锁争用 +
并行会话在途的 `skeleton_panel.py`/`operator_coverage_audit.py` 裸 sqlite + data 备份数），
与本次 4 文件改动集无关（单文件跑锁类 3 个即绿，其余 2 个溯源到未入库的在途脚本）。

---


> 上游：[`output_dirs_governance_review2_20261008.md`](output_dirs_governance_review2_20261008.md)（提出 A–H）、
> [`output_dirs_governance_apply2_20261009.md`](output_dirs_governance_apply2_20261009.md)（A/B/C/F/G 落地；**D/E/H 明确不做**）。
> 本轮只回答两个问题：**① 10-09 之后有没有新增漂移；② 已落地的闸门有没有盲区。**

判据：AGENTS.md §8.13（`output_report/` = 产物唯一出口、`reports/` = 人工审计；日期 `YYYYMMDD` 作后缀、不带杠、纯 ASCII）。

---

## 0. 一句话结论

主体合规：`audit_structure FAIL=0 WARN=4`、`doc_path_refs BROKEN 0`。
但**第二轮 A 项刚改掉的「tracking 顶层日期带杠」在 10-09 复发了**，且 S16 **看不见它** —— 因为 S16 只扫 git 跟踪文件。
另有 8 份结论类报告仍躺在 gitignore 的 `results/`（B 项只迁了一半）。

| 闸门 | 10-09 | 现在（10-10） | 判定 |
|---|---|---|---|
| `audit_structure` | FAIL=0 WARN=4 | **FAIL=0 WARN=4** | ✅ 持平 |
| `doc_path_refs` | BROKEN 0 / UNTRACKED 0 | **BROKEN 0 / UNTRACKED 1** | ⚠ 新增 1 条未跟踪源码引用 |
| `output_report/` 命名违规（新增） | 0 | **0** | ✅ 15 个未跟踪件全部合规 |
| `tracking/` 顶层带杠件 | 0（改名后） | **1** | ❌ **复发** |

---

## 1. 现状盘点（实测）

### `output_report/`（产物唯一出口）
- **175 个文件、0 子目录、0 个 .py** —— 写方脚本没有污染产物目录，符合 §8.13。
- 扩展名：169 `.md` / 3 `.json` / 2 `.txt` / 1 `.csv`。
- 跟踪 160 / **未跟踪 15**（GBR 战役在途 + DEU 4 件）。
- 15 个未跟踪件命名**全部合规**（`_YYYYMMDD` 后缀、无杠、纯 ASCII）—— 并行会话的写入纪律是好的。
- **62 个文件（35%）文件名无日期**，主体是 `*_ideas.md`（S1 产物）。

### `reports/`（人工审计）
- 101 个跟踪件、9 个子目录。
- 子目录风格**两分**：2 个下划线日期化（`ra_pipeline_stage_review_20260927/`、`skills_review_20260929/`）对 7 个 kebab 主题（`dataset_experience/`、`eur-mining/`、`forum-experience/`、`forum_alpha_research/`、`gbr-campaign-final/`、`project-audit/`、`tooling-research/`）—— 即第二轮 D 项。
- **2 组「同名文件 + 同名目录并存」**：`ra_pipeline_stage_review_20260927.md`(197 KB) 与 `ra_pipeline_stage_review_20260927/`；`skills_review_20260929.md`(490 KB) 与 `skills_review_20260929/`。
- 版本堆积比 10-08 更重：`ra_pipeline_stage_review` 已有 **md + _v3 + _v4 + 目录**四态；`skills_review_20260929.md`(490 KB) + `_closure`(249 KB) + 目录；`dryrun_chain_result{,_v2}.json`。

---

## 2. 新发现

### P1-A ★ `tracking/2026-10-09_robustness.md` 复发，且 S16 拦不住

第二轮 A 项把 `tracking/2026-10-0{6,7,7,8}_robustness.md` 改为 `robustness_YYYYMMDD.md`（commit `48eb39e`），
并同步把 `tracking/*.md` 顶层纳入 S16 扫面。**10-09 又出现了一个带杠件**，且当前处于**未跟踪**状态。

更关键的是**为什么 S16 没报 FAIL**——不是闸没写，是闸看不见：

```
_naming_violations('tracking/2026-10-09_robustness.md')
  → ['日期带杠（应为 YYYYMMDD 无杠）']        # 规则本身能判出违规

_s16_targets() 只取 git ls-files（已跟踪）
  → 该文件是 '??' 未跟踪 ⇒ 不在扫描面 ⇒ 闸静默通过
```

这是**设计内的取舍**（`audit_structure.py:1180-1182` 明写：未跟踪的在途文件不该拦住别人的提交），
但后果恰好命中 S16 当初的存在理由（「文字纪律守不住持续的写入」）：**同一个违规在 `git add` 之前完全隐形，
而一旦 `git add`，pre-commit 就会 FAIL**（该路径不在基线上）。所以它是「迟到地拦」，不是「不拦」。

该文件是并行会话**手写**的中文审计报告（4 037 字节，非工具生成）⇒ 不是 cron 复发，而是**写入时点的命名纪律问题**。

### P1-B `results/` 仍有 8 份结论类 md 落在 gitignore 区

第二轮 B 项只迁了 `cache/eur_analyst_fields_report.md`，原文写明「`results/` 的 md 若为盘点结论也应迁出（**只迁 md，不动 checkpoint json**）」——**未执行**，且又新增了 2 份 10-09 的：

| 文件 | 性质 |
|---|---|
| `results/inventory_consolidated_2026100{5,6,7,8}.md` | 盘点结论（4 份） |
| `results/scope_eligibility_platform_20261009.md` | 平台口径结论 |
| `results/osmosis_rerank_platform_20261009.md` | 平台口径结论 |
| `results/enqueue_glb_batch_20261007.md` | 派发记录 |
| `results/submit_report_20261006.md` | 提交记录 |

已实测 `.gitignore:177 /results/` 命中 ⇒ **这些结论不入库**，与 `results/` 的续跑断点共享同一个「丢不了也留不下」的位置。
⚠ 约束仍在：`backfill_longcount.py` / `batch_submit_verdict.py` / `prod_blocked_recheck.py` **硬编码引用 `results/` 续跑断点**，只能迁 `.md`，断点 json 一律不动。

另有 `logs/session/{findings,progress,task_plan}.md` 3 份仍在（B 项标「中」风险，未迁）。

### P2-C `reports/` 同名文件 + 同名目录并存（检索歧义）

2 组（见 §1）。同名时 `reports/<stem>/` 与 `reports/<stem>.md` 相邻，检索与引用都要猜是哪个。
属第二轮 E 项的同源问题，且规模已长到 4 态版本。

### P2-D §8.13 措辞与 S16 实现存在漂移（守的是什么）

§8.13 写「产物与报告**一律** `YYYYMMDD` 作后缀」，而 S16 实现只在**文件名已含日期**时校验格式与位置；
**完全无日期的文件名不判违规**（`_naming_violations` 三条里没有「必须带日期」）。
于是 `output_report/` 62 个无日期件长期稳定存在、且永不会进基线也永不会 FAIL。

两种收敛方向（二选一，不要各写一半）：
- 若「一律」是硬要求 → 给 S16 加第四条规则，并把 62 件进基线（棘轮只减不增）；
- 若只是推荐 → 把 §8.13 改为「**带日期时** `YYYYMMDD` 作后缀」，让文档与实现一致。

按仓库「文档与实现不得漂移」的纪律，这一条**必须处理一个**，否则下一个人读 §8.13 会以为 62 件是违规。

### P3-E `reports/forum_alpha_research/` 混着运行产物

3 个无日期脚本（`gather_search_v2.py`、`make_digest.py`、`read_posts.py`）+ 2 个 json（`read_posts.json`、`search_results.json`）+ `digest.txt`。
S5 因前缀豁免不判失败，但这些是**运行期产物**，按 §8.13 应出仓（`logs/`）或进 `attic/`。

### P3-F `doc_path_refs` UNTRACKED 1：活文档引用未入库源码

```
tools/fields/skeleton_panel.py
  <- Claude/skills/wq-brain-ra-gbr/references/_field-profile-playbook.md
```

skill 文档是活文档、`.py` 未入库 ⇒ 只在本机存在，克隆后该 playbook 指向空。
不属输出目录问题，但同属「未跟踪即失」家族，一并登记。

---

## 3. 建议执行顺序

| # | 项 | 动作 | 风险 |
|---|---|---|---|
| 1 | **P1-A** | `git add` 前先改名 `tracking/robustness_20261009.md`；**同时给 S16 补「未跟踪件预检」**：`audit_structure` 单跑时对未跟踪报告件额外报 WARN（列名不判 FAIL，保持「不拦别人提交」的原设计） | 改闸需同步测试；预检只 WARN 不改现有 FAIL 语义 |
| 2 | **P1-B** | 迁 8 份 `results/*.md` → `output_report/`（**只迁 .md**，断点 json 一律不动；迁完跑 `doc_path_refs`） | 涉及移动，需先确认无脚本引用这些 md |
| 3 | **P2-D** | 二选一收敛（加规则 / 改措辞），只做一个 | 改 S16 需新增测试并进基线 |
| 4 | **P2-C** | 2 组同名冲突：把 `*.md` 主体并入对应目录（或目录改 `_refs/`），消歧义 | 涉及移动，需同步引用 |
| 5 | **P3-E/F** | `forum_alpha_research/` 运行产物出仓；`skeleton_panel.py` 入库 | 低 |

> **不建议做的**（沿用第二轮结论，且现状未变差）：`output_report/` 175 件分区（E，收益仅是观感，
> 命名已被 S16 守住）、`reports/` 子目录统一风格（D，纯观感）。真要动，触发条件是**出现「找不到某份报告」的实际投诉**。

---

## 4. 本轮验证读数

```
[audit_structure] FAIL=0 WARN=4
  WARN S16 基线内存量违规 15（存量，只减不增）
  WARN S13 登记项 PPA_USA 磁盘已不存在（可从 NON_REGION_DIRS 清理）
  WARN S6 skills 漂移 4 组（已登记基线）
  WARN S1 tools sys.path 171 处存量（脚本直跑需要）
[doc_path_refs] BROKEN 0（基线 0）｜ UNTRACKED 1
output_report/  175 件：169 md / 3 json / 2 txt / 1 csv；0 子目录；0 py；跟踪 160 / 未跟踪 15（命名全合规）
reports/        101 件跟踪；9 子目录；62 个 output_report 文件名无日期（35%）
```

> 复现：`python tools/audit_structure.py`；`python tools/code-audit/doc_path_refs.py`；
> 单项 `--only s16`；S16 基线 `tools/audit_structure_baseline.json::s16_naming_violations`（15 条）。
>
> ⚠ 本轮**只出审计与建议**：P1-A 的改名、P1-B/P2-C 的迁移属破坏性动作，未执行，落地前请确认。
