# RA 流水线：优化 phase 复验报告 + skills 优化方案（2026-09-11）

> 复验对象：2026-09-11 落地的"流水线自洽性修复"全部改动（P0×4 / P1×7 / P2 若干）。
> 方法：只读断言脚本 `logs/_tmp_verify_20260911.py`（72 项断言）+ 全量 pytest + 功能探测。
> 结论：**全部 24 项原始改进项已验证生效；复验额外发现并当场修复 4 项此前未发现的真实缺陷。**

---

## 一、复验结果

### 1.1 总体

| 维度 | 结果 |
|---|---|
| 断言脚本 | **72 项，PASS 70**；2 项 FAIL 经逐行核对为**检测器误判**（多行引用块的续行，标记词在上一行）→ 实等价 72/72 |
| `pytest tests/ -q` | **531 passed** |
| 仓库 ↔ 安装位 | `tools/sync_skills.py --check` → **4/4 [OK]，零漂移**（含新增 INDEX.md / DEU.md / ra-campaign-prompt.md） |
| 4 个改动脚本 | `py_compile` 通过；`gate._validator_dirs()`、`skeletons.load_region_priors("DEU")` 功能探测通过 |
| 安装位残留 | 孤儿 4 项 + `.bak_*` 17 项 → 已清零 |

### 1.2 复验新发现并修复的 4 项真实缺陷

| ID | 缺陷 | 影响 | 处置 |
|---|---|---|---|
| **N1** | **4 处代码的技能根搜索链缺主安装位**：`run_pipeline._load_template_families` / `skeletons.load_region_priors` / `assemble_priors._profile_path` / `gate._validator_dirs` 只探 `.trae-cn` `.qoder-cn` `.cursor` `.workbuddy` | **高**：拿不到 `~/.claude/skills`（主安装位）与仓库副本 → 会静默解析到**旧拷贝**（与 GBR 跑满 180 条、ra-pipeline 落后 67 行同源的那类 bug） | 四处在链路前端补 `~/.claude/skills` → `~/.codex/skills` → 历史位 → **仓库自带 `Claude/skills`（`__file__` 推导，git clone 即可用）**；功能探测确认解析到 `Claude/skills` 且目标存在 |
| **N2** | `ppa-mining-experience.md` 与 `wqb-concurrency/SKILL.md` 仍硬编码 `.qoder-cn` 路径 | 中：换机器即失效，违反 `AGENTS.md §6` | 改 `<SKILL_ROOT>` / `$WQ_TOOLKIT_DIR` |
| **N3** | skills 树内残留 `assemble_priors.py.bak_20260910`；安装位另有 17 个 `.bak_*`（sync 忽略 `.bak_` → 永远不被发现） | 低（噪音）但会误导"谁是当前版本" | 全部移入 `attic/legacy_skill_refs_20260911/` |
| **N4** | **闸编号第三种口径**：`gate-rules.md` 标题称"gate 6 闸"、`SKILL.md` 前文称"7 闸"、AGENTS/ra-pipeline 称"5 闸"——而 `gate.py` 模块头亲述 **8 闸 + 可选闸0** | 中：读者无法判断"这批到底过了几道闸" | 把**闸编号唯一基准**写进 `INDEX.md §gate.py 闸编号`（闸0–8 全表），其余文件改为引用该表；`gate-rules.md` 同步标注"5 闸=闸1–5" |

### 1.3 验证方法与可复现性

- 断言脚本位于 `logs/_tmp_verify_20260911.py`（gitignored；`python logs/_tmp_verify_20260911.py` 可重跑）。
- 覆盖面：INDEX.md 内容与同步、ra-pipeline 步5/整链/闸语义、11 区 thresholds、调用链文档、区域三表一致、
  DEU profile 契约、toolkit/contract/gate-rules、sim-alphas、ppa-mining、4 处代码技能根、P2 全部清理项、
  以及"全 skills/docs 旧名 + `.qoder-cn` 残留"的全局扫描。

---

## 二、skills 优化方案（按优先级）

> 原则：**把"人工审计"变成"可执行断言"**。本次 24 项改进里，有 5 项（N1/N2/N3/N4 + `.qoder-cn`）本可通过一条测试提前拦下。

### P0（防复发，收益最高）

| # | 方向 | 具体建议 |
|---|---|---|
| **1** | **新增文档-代码一致性测试** | 新建 `tests/unit/test_docs_consistency.py`，断言：① 阈值节 schema（六节/扁平两版）与 contract 一致；② 闸编号在 INDEX/AGENTS/toolkit/gate-rules 只出现一种口径；③ 区域三表（`config.REGIONS` / profiles / tracking 目录）互含；④ 每个 profile frontmatter 含 4 必需键；⑤ **全 skills/docs 无 `~/.xxx/skills` 硬编码主路径**；⑥ 文档中出现的相对链接与文件路径真实存在。→ 这 6 条正好覆盖本次全部缺陷类型。 |
| **2** | **技能根解析单源化** | 4 处脚本各自维护搜索链（N1 根因）。建议在 toolkit/`trailSomeAlphas` 各加一层薄 helper（或让脚本 `sys.path` 引入 `src/wqb/workflow/_common._skill_roots()`），统一"env → claude → codex → 历史位 → 仓库"顺序；`_common` 已是权威，禁止再各写一份。 |
| **3** | **步5 门禁入 MCP（治本）** | H2/H3 的根因是 `wave_gate` 没有 workflow 节点，导致"整链"无法覆盖步5。建议新增 `wave_gate` 节点（包装 `tools/wave_gate.py`，统一 dry-run 契约 + `validate_argv`），使步2→步9 真正可链；否则文档只能一直注明"步5 不在 MCP"。 |

### P1（结构与卫生）

| # | 方向 | 具体建议 |
|---|---|---|
| **4** | **sync 增加 `--prune-orphans`** | 现状：sync 只增不删 → 本次清了 21 项 ONLY-AT-INSTALL 残留（含 `.bak_*`、`validate_skills.py`、`checklist.md`）。建议加 `--prune-orphans`（默认 dry-run 打印，`--apply` 生效；白名单保护 `code-optimization`/`dead-code-cleanup`/`gold-analysis`/`jin10-news`/`.system` 等非 WQ 全局技能与迁移标记）。 |
| **5** | **skills 树内运行产物外迁** | GEM 运行产物（`data/*_idea_*.json`、`final_expressions.json`、`ace.log`）与 `.bak_*` 落在 skills 目录里，会污染同步面与"当前版本"判断。建议产物目录改到 `logs/`（gitignored）或加进 `sync_skills.IGNORE_DIRS`，并在 `INDEX.md` 声明"skills 树只放可执行代码与文档"。 |
| **6** | **阈值 schema 两版收敛** | KOR/IND/DEU 是扁平形态，其余是六节。建议给这 3 区补 `hard_gates`/`quick_scan` 两节（值从扁平键映射），或反向把六节收敛为扁平——**二选一，不要长期并存**；收敛后由 P0-1 的断言守住。 |
| **7** | **`signal_floor` 值按区实证回填** | 本次统一填 `0.5/2`（EUR/GBR/GLB 的标准值），但语义上窄截面区（GBR `narrow_cross_section: true`）与小宇宙区（KOR/HKG，`cw_gate=FAIL`）应有不同 floor。建议按各区历史 `max\|sharpe\|` 分布回填，并回写 profile 佐证。 |

### P2（卫生与文档）

| # | 方向 | 具体建议 |
|---|---|---|
| **8** | **根目录瘦身** | 现存 9 个 `_tmp_check_*.py`、`scratch_hkg{1,2,3}.json`、`ace.log`、`Claude outputs/`、`MCP_INSTALLATION_GUIDE.md`（与已归档的 `INSTALLATION_GUIDE.md` 疑似同源）。建议按"结论落地即归档 `attic/`"的既有纪律清理。 |
| **9** | **提交纪律显式化** | 两轮都遇到"脏树跨多条工作流"。建议在 `AGENTS.md` 加一节：提交前用 `git status --porcelain` 分类，按主题拆 commit，**禁止 `git add -A`**；跨工作流改动用显式路径清单（本次即用此法）。 |
| **10** | **`docs/plans/2026-08-18-wqb-optimization-plan.md` 的 P1 续做** | 该计划记有"122 个活跃脚本硬编码 `C:/Users/MENGTAO/...`（4 种 skill 根）"。本次只清了 skills 面，`tools/`、`mining/`、`tracking/*/scripts` 面仍可能有存量，建议按同一断言（P0-1 第⑤条）批量扫一遍。 |

---

## 三、提示词方案（摘要）

完整可复用模板已落地：**`Claude/skills/wq-brain-ra-pipeline/references/ra-campaign-prompt.md`**
（并在 `SKILL.md` 顶部登记入口，避免再出现"存在但无人引用"的孤儿）。

设计要点：

1. **三条铁律**：不复制数字（阈值只引用 `config.GATES` 与区域 thresholds）／入口唯一（只认 ra-pipeline）／
   闸门前置（把"过闸"写成每步验收条件，而不是最后判）。
2. **主提示词**：角色 → 目标 → 4 条硬约束 → **九步执行顺序**（步0 明确"库存优先"三件套：
   profile 路由 / `build_gate_prior_from_inventory` + `select_ra_basket` / 算子审计 + PPA 主题门）
   → 强制输出表格式 → 停止条件 → 禁止清单。
3. **4 个场景变体**：续波（含积压检查）、发批（跳过步1–4 但白名单外禁止发批）、单条修复（闸位→病因映射）、
   日循环（三通道配额：先提 PPA 那 1 颗）。
4. **验收自检表**：7 条（库存先扫 / 白名单内 / 步5 落库 / 七槽配给 / prod-first / 提交三条件 / 三处回写）。

**为什么这套提示词能提高过闸率**：它把历史失败模式逐条前置成硬约束——
"库存未清就开新挖""生成端 `rank(field)`""PROD/SIZE 撞墙后才换腿""跳过步5 门禁""窄闸区用宽截面阈值"
这五类死因，分别在步0/步4/步7(D14)/步5/步2(signal_floor) 被拦截。

---

## 四、优化方案落地记录（2026-09-11 当日完成，10/10）

| # | 方案 | 落地内容 | 验收 |
|---|---|---|---|
| P0-1 | 文档-代码一致性测试 | 新增 `tests/unit/test_docs_consistency.py`（**9 组断言**：阈值 schema 两版、闸编号单一口径、区域三表互含、profile frontmatter 契约、无硬编码技能根、**全 skills markdown 相对链接可解析**、无 `.bak_`、旧 skill 名不回流、sync 保留 prune 入口）。**该测试首跑即揪出 10 个真实缺陷**（8 个断链 + 1 处 README 硬编码安装位路径 + 1 处历史描述） | 198 passed |
| P0-2 | 技能根解析单源化 | 新增两份同序 helper（toolkit `scripts/_lib/skill_roots.py`、gem `trailSomeAlphas/skill_roots.py`），重构 4 处调用点（`run_pipeline` / `skeletons` / `assemble_priors` / `gate`）；新增 3 条守护测试（镜像内部一致、与 `_common._skill_roots()` 同序、以仓库副本兜底） | 解析探测：`gate` 首选已变为主安装位 `.claude`；`skeletons.load_region_priors("DEU")` 正常 |
| P0-3 | 步5 门禁入 MCP（治本） | 新增 `src/wqb/workflow/nodes/wave_gate.py`（遵守 dry-run 契约 + `validate_argv`），注册进 registry（第 8 个节点），补 3 条测试，更新 5 处文档（ra-pipeline 步5/整链、skill_call_chain、AGENTS §3.5、INDEX 映射表） | 733 passed；`workflow_execute(node="wave_gate")` 可入链，整链覆盖扩展为步 2/3/4/5/6 |
| P1-4 | sync 孤儿清理 | `--prune-orphans [--apply]`：判据"顶层条目仓库完全不存在"，默认只打印、`--apply` 移入 `attic/sync_orphans_<date>/<host>/`（保留 `PROTECTED_ORPHANS` 白名单与 `.`/`migration` 放行）；同时处理 symlink 与 Windows **directory junction** 两类悬空链接 | 首次执行归档 8 个改名遗留悬空 junction（2009-10 改名残留），并留下 `dangling_symlinks.txt` 备查 |
| P1-5 | 运行产物与孤儿分报 | sync 报告把 `data/`、`outputs/`、`*.log`、`.bak_` 等归为 `[runtime]` 单独计数，不再淹没真孤儿 | 报告噪音显著下降 |
| P1-6 | 阈值 schema 收敛 | KOR/IND/DEU 补 `quick_scan` + `hard_gates`（纯别名节、无消费方 → 零行为变更）；**刻意不补 `probe_scoring_v2`**（会改 S0 评分行为，需单独实证） | 11/11 区均含两节；schema 判定仍走"六节 or 扁平版"二分 |
| P1-7 | `signal_floor` 实证回填 | 按每区历史"每波 max\|sharpe\|"的 p25 回填，规则**只上调、不下调**、样本 ≥8 波：IND `0.5→1.2`（p25 1.27 / 29 波）、MEA `0.5→1.2`（p25 1.26 / 47 波）、USA `0.5→0.9`（p25 0.93 / 13 波）；其余区写入 `_evidence` 说明（EUR/GBR/KOR p25 本就在 0.5 附近；ASI/CHN/DEU/GLB/HKG 样本不足） | 11/11 区均有 `_evidence` 或实证值 |
| P2-8 | 根目录瘦身 | 归档 13 个临时件（9 `_tmp_check_*.py` + 4 `scratch_hkg*.json`）与 `Claude outputs/`；`MCP_INSTALLATION_GUIDE.md` 归位到 `world-quant-brain-mcp/docs/` | 根目录临时件清零 |
| P2-9 | 提交纪律显式化 | `AGENTS.md` 新增 **§7 提交纪律**：禁 `git add -A`、按主题拆 commit、显式路径清单、提交前扫密钥、**并行写入者注意**（被漂移断言拦下先重同步、共享文件只追加不覆写）、归档而非删除 | — |
| P2-10 | 硬编码技能根续做 | 扫描 `tools/` + `mining/` + `tracking/*/scripts` 全部 `.py`：**0 处命中**（该项此前已达标，无需改动） | 0 命中 |

**落地期额外修正（非原方案，验证/测试暴露）**：
1. `brain-forum-browse` 8 个 markdown 的**断链修复**（references 早期按主题拆分、后合并 → 链接未跟随）：可一一对应的改指（`unique-contribution→contribution-and-diversity`、`gap-detection→recon-and-gap`、`run-contract/run-modes→modes-and-contract` 等），无落点的去链接并加"参考资料已合并"说明。
2. `brain-make-some-gem/.../headless_runner/README.md` 的硬编码 `Set-Location ".cursor\skills\..."` + `C:/Python313/python.exe` → 改 `<SKILL_ROOT>` / `$WQ_PY`。
3. `tests/unit/test_scheduler.py::test_plan_non_usa_region` 断言过期（KOR 期望 TOP3000）——**并行工作流已把 `config.py` 的 KOR 档改为 TOP600**（与 tracking settings / KOR profile / decision-table 三处一致），测试未跟随；已按四重佐证修正为 TOP600。
4. `tests/unit/test_workflow.py` 节点集与 `test_skill_integrity._DRY_RUN_CASES` 随新节点同步（7→8）。

**最终验收**：`pytest tests/ -q` → **733 passed**；`tools/sync_skills.py --check` → **4/4 [OK]**；
`tools/sync_skills.py --prune-orphans` → **0 孤儿**。
