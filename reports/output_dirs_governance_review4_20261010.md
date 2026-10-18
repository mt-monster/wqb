# 输出目录规范复核（第四轮 · 2026-10-10）

> 上游：[`output_dirs_governance_review3_20261010.md`](output_dirs_governance_review3_20261010.md)（第三轮复核）→
> [`output_dirs_governance_apply_20261010.md`](output_dirs_governance_apply_20261010.md)（第三轮整改，FAIL=0 收尾）。
> 本轮回答三个问题：**① 第三轮整改有没有守住；② 当天新出现的漂移是什么；③ 复发 3 次的带杠命名到底为什么治不住。**
>
> 判据：AGENTS.md §8.13（`output_report/` = 产物唯一出口、`reports/` = 人工审计；日期 `YYYYMMDD` 作后缀、不带杠、纯 ASCII）
> 与 §8.12 结构守护（S7 根目录白名单 FAIL 阻断）。

---

## 0. 一句话结论

**归属层面守住了，但两道闸正红，且找到了复发 3 次的真正根因。**

- 第三轮整改项**全部保持**（`results/` 结论 md 零残留、同名文件+目录冲突归零、`skeleton_panel.py` 已入库、S16 未跟踪预检上线并真的逮到了今天的违规）。
- 但当前 `audit_structure` **FAIL=2**（S7 根目录 19 个散件 + S16 `deu_t4_targets.json`），`doc_path_refs` **BROKEN=1** ⇒ **pre-commit 正被阻断**。
- ★ `tracking/2026-10-XX_robustness.md` 带杠命名**已复发 3 次**（10-09 改过、10-10 再犯）——根因不在写的人、也不在闸，而在 **`brain-alpha-robustness/SKILL.md:30,110` 把带杠路径写成了规范**。前三轮只改名 + 加闸，从没治过指令源头。

| 闸 | 第三轮收尾（10-10 早） | 现在（10-10 晚） | 判定 |
|---|---|---|---|
| `audit_structure` | FAIL=0 WARN=4 | **FAIL=2 WARN=7** | ❌ 恶化 |
| `doc_path_refs` | BROKEN=0 UNTRACKED=0 | **BROKEN=1 UNTRACKED=0** | ⚠ 新增 1 |
| `tracking/` 顶层带杠件 | 0 | **1（未跟踪，预检已 WARN）** | ❌ 第 3 次复发 |
| `results/` 结论 md | 0 | **0** | ✅ 保持 |
| `reports/` 同名文件+目录 | 0（`_refs` 改名） | **0** | ✅ 保持 |

---

## 1. 第三轮整改保持性核验（实测）

| 第三轮项 | 承诺 | 现状 | 证据 |
|---|---|---|---|
| P1-B `results/` 8 份结论 md 迁出 | 只迁 md、断点不动 | ✅ **0 残留**，断点 json 未动 | `Get-ChildItem results -Filter *.md` 空 |
| P2-C 同名文件+目录 | 目录加 `_refs` | ✅ **0 冲突**（4 处改名已 staged） | 9 个子目录逐一比对无同名 md |
| P2-D 规则④ + 机器产物豁免 | 文档与实现收敛 | ✅ 基线 40、豁免件未进基线 | S16 WARN 基线 40 |
| P2-D 未跟踪预检 | 只 WARN 不 FAIL | ✅ **真的逮到了** `tracking/2026-10-10_robustness.md` | S16 WARN 行 |
| P3-F `skeleton_panel.py` | 并行会话在途 | ✅ **已入库**（`git ls-files` 命中），UNTRACKED 归零 | `doc_path_refs` |

---

## 2. 新问题（按优先级）

### P0-1 ★ S7 FAIL：19 个根级散件（阻断全仓提交）

```
_diag2..8.py  _diag_macro.py  _fields_multi.py  _fields_of.py  _macro_datasets.py
_prod2.py _prod3.py _prod_check.py  _simchk.py _simst.py  _tower.py _tower2.py  harvest_wave.py
→ 全部 ?? 未跟踪；根目录现存 21 个 .py
```

- **S7 扫磁盘不看 git 状态** ⇒ 即使未跟踪也 FAIL，而 S7 是 pre-commit **硬阻断**项
  ⇒ **此刻任何人的提交都被这 19 个文件拦住**，与第三轮收尾时 FAIL=0 相比是**当天新出现**的。
- 形态 = §8.4 已归档过的「根目录污染」复发（`attic/root_clutter_*`），按 §8.13 路由应去
  `tools/`（可复用）/ `logs/_tmp_*.py`（一次性）/ `tracking/<R>/scripts/`（区域探针）。
- ⚠ **归属并行会话在途工作**（第三轮 P3-F 同款克制）：不由我代删代迁，需其主人处置，或用户明确批准后按 §8.13 归位。

### P0-2 S16 FAIL：`output_report/deu_t4_targets.json` 已 staged 无日期

第三轮预检**当时就 WARN 过这个文件**，现已 `git add`（`A` 状态）⇒ 按设计转为 FAIL——
「迟到地拦」预言如实发生。改名 `deu_t4_targets_YYYYMMDD.json` 并同步引用，或确认属机器产物快照后
走 §8.13 例外登记。同样注意它是并行会话 staged 的。


### P1-3 ★★★ 根因：skill 文档写死了违规路径（前三轮均未治）

`Claude/skills/brain-alpha-robustness/SKILL.md`：

- `:30` — `"report_path": "tracking/<日期>_robustness.md"`
- `:110` — 「报告追加到 `tracking/YYYY-MM-DD_robustness.md`」

**写报告的会话是照 skill 执行的** ⇒ 每天产出一个带杠文件 ⇒ 治理改名 + S16 加闸 ⇒ 下个会话照旧。
10-06~10-08 的 4 个已改名、10-09 复发被改、**10-10 又复发**——闸有效（预检 WARN 逮到），
但 WARN 拦不住「按规范写作」的人。这正是 S16 立项语句「文字纪律守不住持续的写入」的完整形态：
**当写入指令本身违规时，闸只能事后提醒。**

**修法（结构性，一处根治）**：
1. SKILL.md 两处改为 `tracking/robustness_YYYYMMDD.md`；
2. `python tools/sync_skills.py --apply` 同步 6 个安装位（否则运行时优先位还是旧文）；
3. 今天未跟踪的 `tracking/2026-10-10_robustness.md` 改名（文件是并行会话在途，需批准）；
4. 加守护测试：扫 skill 文档不得出现带杠日期路径模式（与 `test_audit_structure_s16.py` 互补——
   S16 守磁盘产物，新测试守**指令源**）。

### P1-4 闸盲区：`output_report/` 混入 `.py` 无闸

`output_report/diff_t4.py`（未跟踪）。第三轮人工核过「0 子目录、0 .py」，但**没有机械闸守**：
S16 扫描面 `S16_SUFFIXES = {.md,.json,.txt,.csv,.html}` **不含 `.py`** ⇒ 产物目录混入脚本永不报。
建议给 S16（或 S7 式目录检查）补一条：`output_report/**/*.py` → FAIL（脚本按 §8.13 去 `tools/` 或 `logs/_tmp_*.py`）。

### P2-5 `doc_path_refs` BROKEN=1：`.clinerules/skills` ← AGENTS.md:135（误报）

AGENTS.md 第 135 行是 **Cline 客户端的外部搜索路径清单**（`dist/lib.mjs` 实测登记），
仓库**有意不建**项目级 skills 副本（§3.5 明写 wqb 侧不为 `.claude/skills` 复制）。
这不是死指针，是**对「外部工具会去找、而我们故意没有」的路径的描述** ⇒ 应做**豁免登记**，
不是建目录。暴露 `doc_path_refs` 对「外部路径 vs 仓库路径」无区分能力，属误报家族。

### P2-6 基线滞留（棘轮信用损耗）

| WARN | 数量 | 含义 |
|---|---|---|
| S11 | 76 个已不在 tools 顶层 | 迁移成功但基线没同步移出 |
| S14 | 76 个 README 登记已不存在 | 同上（README 侧） |
| S13 | `PPA_USA` 登记已不存在 | NON_REGION_DIRS 残留 |

棘轮「只减不增」的前提是基线诚实；**迁移成功却不收基线**，会让 WARN 长期噪音化、
真新增被淹。S11 的报文本就提示了「请同步移出」，属低风险例行同步。

### P3-7 存量欠债（维持现状）

S16 基线 40 条（`output_report/` 手工无日期报告、`reports/` 的 `eur_d1_20260924_*` 日期不在末尾等）
按 §8.13「存量不强制回改」，触碰时顺手改、改一条从基线移一条。

---

## 3. 建议执行顺序

| # | 项 | 动作 | 风险 | 归属 |
|---|---|---|---|---|
| 1 | **P0-1** 根目录 19 散件 | 按 §8.13 归位（tools / logs/_tmp / tracking scripts / 死件归档）；**先确认归属再动** | 高（并行会话在途 + 阻断提交） | 并行会话 / 需用户批准 |
| 2 | **P0-2** `deu_t4_targets.json` | 改名带 YYYYMMDD + 同步引用 | 低（已 staged，不改就一直红） | 同上 |
| 3 | **P1-3** skill 根因 | SKILL.md 两处改名 → `sync_skills.py --apply` → 守护测试 | 低 | **我可直接做**（文档 + 同步） |
| 4 | **P1-4** 补 `output_report/**/*.py` 闸 | S16 扩扫面 + 测试 | 低（新增 FAIL 面，需同步测试） | 我可做 |
| 5 | **P2-5** `.clinerules/skills` | `doc_path_refs --update-baseline` 登记豁免（注明外部搜索路径语义） | 低 | 我可做 |
| 6 | **P2-6** 基线同步 | S11/S14/S13 滞留项按报文提示移出 | 低（纯基线整理） | 我可做 |
| 7 | P3-7 存量 | 触碰时顺手改 | — | 全体 |

**明确不建议做的**（沿用第二、三轮结论，现状未变差）：`output_report/` 分区（E）、`reports/` 子目录风格统一（D）。
触发条件仍是「出现找不到某份报告的实际投诉」。

---

## 4. 本轮验证读数

```
[audit_structure] FAIL=2 WARN=7
  FAIL S7  根目录白名单: 19 个根级散件（_diag*/_tower*/harvest_wave.py 等，全部未跟踪）
  FAIL S16 报告命名: output_report/deu_t4_targets.json 缺日期（已 staged）
  WARN S16 基线内存量 40 ｜ WARN S16 未跟踪预检: tracking/2026-10-10_robustness.md
  WARN S11 76 个已迁出未收基线 ｜ WARN S14 76 个 README 滞留 ｜ WARN S13 PPA_USA 残留 ｜ WARN S6 漂移 4 组
[doc_path_refs] BROKEN 1（.clinerules/skills ← AGENTS.md:135，误报待豁免）｜ UNTRACKED 0

output_report/ 186 件：0 子目录 ✅ ｜ 1 个 .py（diff_t4.py，未跟踪，无闸）｜ 65 件文件名无日期（机器产物豁免 53，基线 40）
reports/       115 件 / 9 子目录 ｜ 同名文件+目录冲突 0 ✅ ｜ 13 件日期不在末尾（基线内）
results/       结论 md 0 残留 ✅ ｜ 断点 json 未动 ✅
tracking/顶层  1 件带杠（未跟踪，预检已 WARN）｜ robustness_2026100{6,7,8,9}.md 已合规
```

> 复现：`python tools/audit_structure.py`；`python tools/code-audit/doc_path_refs.py`；单项 `--only s16` / `--only s7`。
>
> ⚠ 本轮**只出审计与建议**：P0-1/P0-2 与 `tracking/2026-10-10_robustness.md` 属并行会话在途件，未动；
> P1-3 起的 4 项我可执行，待批准。
