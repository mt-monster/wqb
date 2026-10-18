# 项目布局审计报告（project_layout_audit_20261014）

> 范围：**只看结构与文件组织**——目录层级、文件归类、命名一致性、公共/业务边界、重复与冗余、
> 空目录、入口位置。不评价算法实现、业务流程与运行时行为。
> 口径：所有结论均出自机器级证据（`git ls-files` / `git check-ignore` / `find` / `diff -rq` /
> 仓库自带闸门读数），未做主观估算。证据采集时间 2026-10-14。

---

## 0. 结论速览

| 判级 | 问题 | 一句话 |
|---|---|---|
| **P0** | 根目录多出一棵完整 skills 树 `wq-brain-ra-usa/`（455 件，未跟踪、未忽略、零引用） | 第二技能源 + 不可恢复债，且现有 16 道闸**没有一道看得见它** |
| **P0** | 索引里有**幽灵路径**：`reports/ra_pipeline_stage_review_20260927/` 23 件仍挂在 `git ls-files`，磁盘已无此目录（删除未暂存），连带让 `audit_structure` **S16 FAIL=1** | pre-commit 第②步就红，全仓提交被卡；修法只是「把删除暂存」 |
| **P0** | 大量源码**只以工作区未跟踪文件存在**（13 份 docs/reference/EUR、5 份 output_report/DEU-GBR、1 份新守护测试） | 正是 AGENTS.md §7 红线禁止 `git clean` 的根因仍在持续产生 |
| **P1** | `tracking/` 占全仓跟踪文件 **64%**（2704/4216），其中 `tracking/mining/` 1053 件、MB 级 JSON 直入库，且 `MANIFEST.json` 从未生成 | 数据湖既拖慢仓库又无索引 |
| **P1** | `tracking/USA/robustness|perfmax/<实验名_时间戳>/` 的 65 个运行中间产物（`all_exprs.txt`、`variants_*.txt`、`plan/score/dispatch*.json`）**已被 git 跟踪** | 运行期产物落进业务目录并入版本控制，违反 §5 规约 0 与 §8.13 |
| **P2** | 公共层 `src/wqb/` 顶层仍有 **26 个散模块**；`tools/` 顶层 **154 个 .py**（主题下沉 0 进展）；`tools/mcp_py` 无扩展名 | 边界清晰但布局半成品 |
| **P2** | `docs/` 顶层混放长期规范与带日期的一次性报告（12 份），并有二进制 `docs/alpha模板.docx` | 违反 §8.13「docs = 长期规范 / SOP」与「路径纯 ASCII」 |
| **P3** | 快照目录 `*_refs` 后缀语义无人声明；`reports/` 子目录混用连字符与下划线；空目录 153 个（几乎全在 gitignore 区） | 观感与可发现性问题，不阻塞 |

闸门现状读数（本次实测）：`audit_structure` **FAIL=1 / WARN=5**；`audit_skill_drift` B=4（基线内）、分叉 0；
`doc_path_refs` 新增死指针 0（基线 BROKEN 1 = `.clinerules/skills` 已豁免）；`audit_destructive_default` 新增 0；
`repo_governance_check` 报「抢救点独有源码 **845 件** 未逐件裁决」+「被 gitignore 排除的源码类文件 **1707 件**」。

> **交付后状态（2026-10-15 00:52，批次A–I 收口时的总读数；细节以 §10 为准）**
> 上表 **P0 三条 / P1 两条 / P2 两条 / P3 一条全部有处置**：根技能树三份归档 + 机制拒绝、
> 幽灵路径已暂存并升级为 S20、`tracking/` 89 件运行产物保盘出库并升级为 S18、
> `docs/` 日期报告与 `.docx` 整理并升级为 S16 规则⑥、`mcp_py` 改名并升级为**全仓 S21**、
> `tools/` 顶层数据件归属升级为 S11⑦、`reports/` 子目录风格升级为 S16⑦、
> 空目录 153 → **7**（`find -type d -empty` 排除 `.git` 实测：4 个 `attic/json_archive/**` 归档占位、
> `cache/_scratch/pt` 与 `pt2` 已被 retention 策略④收空、1 个在第三方 `cnhkmcp` 包内）。
> 闸门读数从交付时的 **FAIL=1 / WARN=5** 变为 **FAIL=0 / WARN=5**（5 条均为存量基线项，同一批）。
> ⚠ **该 00:40 读数已被外部事件覆盖**：00:48:51 另一个会话把 **44 个 `tools/*.py` 跟踪件从工作树删掉且未暂存**，
> 全套读数现为 **FAIL=1 / WARN=7**（唯一 FAIL = S20）。不是本治理引入的回归，**且 44/44 可从 HEAD 无损取回**
> （实测 612,960 B / 13,322 行）；处置属「取回 or 暂存删除」二选一，**需用户或写入会话拍板**，见 §10.12。
> ⚠ 仍红的只有「大量源码只以未跟踪形态存在」这一条的**存量部分**：它要的是逐件裁决（入库 or gitignore），
> 属 §10.6 的「需用户点头」清单，不是布局问题。

---

## 1. 结构概览

### 1.1 磁盘体量与文件分布（实测）

| 顶层目录 | 体积 | 文件数 | git 跟踪数 | 性质 |
|---|---|---|---|---|
| `world-quant-brain-mcp/` | 764 MB | 17 750 | 61 | MCP 包（**`.venv` 独占 739 MB**，跟踪的只是源码） |
| `data/` | 419 MB | 10 | 0 | live 库 + 备份（整体 gitignore，受 `test_retention` 硬闸 ≤2 份） |
| `cache/` | 387 MB | 4 519 | 0 | 断点/探针/**pytest tmp（`cache/_scratch/pt`）** |
| `tracking/` | 97 MB | 13 841 | **2 704** | 区域战役 + 共享数据湖 |
| `research-data/` | 40 MB | 319 | 0 | 外部数据包（只读） |
| `logs/` | 12 MB | 1 775 | 0 | 日志与临时脚本 |
| `tests/` | 10 MB | 442 | 213 | 测试套件 |
| `Claude/` | 8 MB | 524 | 436 | **skills 唯一源**（51 个 skill 目录） |
| `results/` | 7 MB | 222 | 0 | 续跑 checkpoint（被 3 个脚本硬编码引用） |
| **`wq-brain-ra-usa/`** | 6 MB | **455** | **0** | **异常：`Claude/skills/` 的全量拷贝** |
| `tools/` | 6 MB | 358 | 222 | CLI 工具链（顶层 154 .py + 14 个主题子目录） |
| `attic/` | 6 MB | 309 | 41 | 日期化归档 |
| `src/` | 5 MB | 280 | 120 | 规范核心包 `wqb` |
| `output_report/` / `reports/` / `docs/` | 4/4/3 MB | 212/118/97 | 180/137/89 | 产物出口 / 人工审计 / 长期规范 |

### 1.2 跟踪文件构成

- 扩展名：`.json` 2228（52.8%）、`.py` 975、`.md` 781、`.txt` 186、无扩展名 17。
- 顶层分布：`tracking` 2704 · `Claude` 436 · `tools` 222 · `tests` 213 · `output_report` 180 ·
  `reports` 137 · `src` 120 · `docs` 89 · `world-quant-brain-mcp` 61 · `attic` 41 · 根 13。
- `tracking/` 二级：`mining` 1053 · KOR 434 · EUR 297 · USA 296 · IND 174 · GBR 153 · MEA 105 ·
  ASI 57 · HKG 45 · DEU 19 · reference 17 · AMR 16 · GLB 11 · FORUM 8 · JPN 6 · CHN 5。

### 1.3 入口文件位置（判定：合理，不动）

| 入口 | 位置 | 评价 |
|---|---|---|
| MCP 服务 | `world-quant-brain-mcp/main.py` | 包内，正确 |
| 本地 DB 后端 | **根 `wqb_db_mcp.py`（2827 行）** | 因 `.mcp.json` 直接指根而**必须住根**（ROOT_ALLOWLIST 已登记）；体量是结构债，拆分已评估并暂缓（§8.4 第 9 条） |
| 可安装包 | `src/wqb/`（`pyproject` 正式声明） | 正确 |
| 门禁权威 | `tools/wave_gate.py`（入口 shim + `tools/wave_gate_pkg/` 12 模块） | 分层清晰 |
| 域常量单源 | `src/wqb/config.py` | 正确 |
| 测试路由 | `pytest.ini` + 根 `conftest.py` + `tests/conftest.py` | 正确 |

> 结论：**「入口在哪里」不是本项目的问题**；问题集中在 §2 的归类、冗余与布局半成品。

---

## 2. 主要布局问题（按层级）

### A. 根层

**A-1 游离 skills 全量树 `wq-brain-ra-usa/`（新发现，最高优先）**

机器证据：
- 顶层 51 个条目 = `Claude/skills/` 的 51 个条目，**名单零差异**（`diff <(ls …) <(ls …)` 空输出）；
- 内容 `diff -rq` 仅 **16 行差异**，其中 15 行是运行期产物只存在于规范源（`__pycache__` ×12、`parsetab.py`、
  `config.json`、`ace.log`），**真实内容差异只有 1 个文件**：`wq-brain-ra-usa/wq-brain-ra-gbr/references/analyst-channel-breakthrough.md`
  与 `Claude/skills/…` 同名文件不一致；
- 该目录**未被 gitignore**（`git check-ignore` 无命中）、**未被跟踪**、`git status` 显示为 `?? wq-brain-ra-usa/`；
- **代码零合法访问路径**：`src/wqb/workflow/_common.py::_skill_roots()` 的搜索链为
  `WQ_SKILLS_DIR` > Claude 安装位 > `~/.claude` > codex/cline/agents > 历史 Agent 位 > 仓库 `Claude/skills/`，
  **不含 `repo_root/<skill-name>`**；全仓 `wq-brain-ra-usa` 字面量只命中该 skill 自己的 frontmatter 与
  `tests/fixtures/skill_capabilities_baseline.json`。

危害（三条，按严重度）：
1. **不可恢复债**：455 个文件全部只活在未跟踪工作区，一旦清理即永久丢失（AGENTS.md §7 红线的形成机制正在被复制）；
2. **第二技能源**：任何把 skill 搜索根配到仓库根的误操作（`WQ_SKILLS_DIR=.`）都会让它**盖过规范源**，
   而它已经与源有 1 处内容分叉；
3. **治理盲区**：S7 明确「只扫顶层文件，目录交给 S9/S10」（源码 `check_s7_root_allowlist` 里 `if p.is_dir(): continue`），
   S9 只校**已声明目录是否存在**，S10 只管区域子目录 —— 于是**没有任何一道闸检查「是否存在未声明的顶层目录」**，
   本次 `audit_structure` 对它的读数就是 `S7 [OK]`。

**A-2 根级未登记目录**：`.claude/`（被 `.gitignore:34` 整目录忽略 → 1707 个源码类文件永不可入库；S15 已确认它是联接、
非真拷贝，但忽略规则本身把镜像变成黑洞）、`.clinerules/`（未跟踪，`doc_path_refs` 里已作为误报豁免）、
`__pycache__/`（1 MB 垃圾）、`.qoder-cn/mcp.json`（本机 MCP 配置，未入库属设计内）。
→ 治理动作 = 把 `.qoder-cn`、`.clinerules` 这类**本机宿主目录**显式写进 gitignore，让它们不出现在 `git status` 的噪声里。

### B. 数据与资产层（`tracking/`）

**B-1 数据湖无索引 + 大块 JSON 直入库**
`tracking/mining/` 有 1053 个跟踪文件（= 全仓 25%），单文件最大 2.85 MB（`tracking/ASI/asi_d1_data_quality.json`）、
`tracking/FORUM/forum_ppa_posts.json` 2.51 MB、`field_inspect_usa_*.json` 一批 0.5–1.4 MB。
索引器 `tracking/reference/tooling/generate_manifest.py` 存在但 `tracking/MANIFEST.json` **磁盘上不存在（从未生成）**，
AGENTS.md §1 已注明「当前未生成」。→ 消费方无法回答「这个湖里有啥」。

**B-2 运行期产物落进业务目录并被跟踪**
`tracking/USA/robustness/NEU_IND_*/`、`tracking/USA/perfmax/RR6bv6rz_*/` 共 **65 个跟踪件**
（43 个 `.txt` + 22 个 `.json`：`all_exprs.txt`、`variants_D1000.txt`、`dispatch_spec.json`、`plan.json`、`score.json`、
`dispatch.log`）。这些是消融/派发实验的中间产物，语义上属 `results/`（续跑断点，已 gitignore），
位置上却躺在 `tracking/<REGION>/` 下且**进了版本控制**。目录名 `NEU_IND_20261008_1525` 用大写 + 时间戳，
与 §8.13 的文件命名风格也不一致（S16 只校顶层，管不到）。

**B-3 报告混进非报告目录**
`tracking/` 顶层有 7 个 `robustness_*.md`（日期后缀合规，但归属错位：人工复盘 → `reports/`）；
未跟踪的 `tracking/USA/campaign_20261014/` 里是 `01_S0_S1_dataset_field_profile.md` /
`02_wave_ledger.md` / `03_skill_findings.md` —— 战役**产物**按 §8.13 应进 `output_report/`（且台账类应入库而非落文件）。

### C. 代码层（公共 vs 业务边界）

**C-1 公共包顶层散模块**
`src/wqb/` 已有 8 个子包（workflow 32 · store 18 · expression 11 · profiles 10 · research 8 · modeb 5 · memory 5 · search 3），
但顶层还有 **26 个单文件模块**（`config.py`、`db_conn.py`、`waiver.py`、`wave_results_contract.py`、`towers.py`、
`shape_quota.py`、`recon_evidence.py`、`step_*.py` …）。边界方向是对的（S2「src 不引用 tools」= OK），
缺的是**契约/工具类模块的收纳**。

**C-2 `tools/` 主题下沉零进展**
`tools/THEMES.json` 已声明 19 个 kebab 主题、顶层 100% 已归属，S11 机械校归属；但顶层仍有 **154 个 .py**，
本次读数「已下沉 **0** 个」。实测耦合：171 处 `sys.path` 注入（S1 WARN）。→ 结构性决定没问题，缺执行批次。

**C-3 `tools/` 顶层杂物**
- `tools/mcp_py`：**无扩展名的 Python 脚本**（`file` 判定 UTF-8 Python），违反「文件名即类型可辨」，S14 按脚本名登记，
  可发现性差；
- 6 份 `README_*.md`（`README_ECONOMIC_MECHANISM_TEMPLATES` / `_FIELD_SCORER_V2` / `_GEM_OPTIMIZATION` /
  `_OPTIMIZATION` / `_PERF_MAX`）+ 主 `README.md`：工具文档散在顶层，与「19 主题目录」布局互相矛盾；
- 顶层 3 个 JSON（`THEMES.json` 设计内、`audit_structure_baseline.json` 设计内、`skeleton_quota.json` 数据配置，
  归属应指向 `tools/gates/` 或主题目录）；
- `tools/__pycache__/` 混在源目录树里。

**C-4 单点大文件（已知债，登记即可，不在本次动手范围）**
`wqb_db_mcp.py` 2827 行（拆分已评估并暂缓）、`world-quant-brain-mcp/labs_data_analysis_agent.py` 2062 行
（`read_text()` 整文件粘进 BRAIN Labs，**设计内不可拆**）、`src/wqb/workflow/nodes/campaign.py` 2021 行、
toolkit `gate.py` 1739 行。

### D. 文档与产物层

**D-1 `docs/` 顶层混放两类东西**
长期规范/SOP（`env_and_switches.md`、`ledger_keys.json`、`mining_ledger.md`、`modeb_*.md`）与
一次性带日期报告（`dryrun-audit-20260925.md`、`region_universe_update_report.md`）同居顶层；
另有 `docs/alpha模板.docx`（**中文 + 二进制**，直接违反 §8.13「路径一律纯 ASCII」与「中文放正文，别放文件名」）；
`docs/reference/` 顶层有 `CODE_QUALITY_SUMMARY.md`、`INTEGRATION_COMPLETE.md` 这类**结论式**大写命名（应为 `reports/`）。
子层 `design/ experience/ governance/ plans/ reference/` 划分本身是清晰的。

**D-2 `reports/` 命名与索引一致性**
- **S16 FAIL 的真实根因 = 重命名只入了一半索引（不是命名规则打架）**。实测：
  `git ls-files reports/ra_pipeline_stage_review_20260927` = **23 件仍在索引**，而磁盘上该目录**已不存在**
  （`git status` 显示 23 条 `' D'` = 删除**未暂存**）；新路径 `…_refs/` 的 23 件已 `A ` 入索引。
  `_s16_targets()` 的取面是 `git ls-files`（索引，含已暂存），所以它照样扫到旧路径下那 9 个「缺日期」的 `.txt`。
  两侧违规数恰好都是 9 —— 新路径那 9 个同名文件**一个都没被 S16 判违规**，
  证明 `_refs` 目录名命中了 `S5_EXEMPT_PREFIXES` 前缀豁免，**不存在「S5 与 S16 互相打架」**。
- **修法极小且不损历史**：把删除暂存即可 —— `git add -A -- reports/` 或 `git rm -r --cached reports/ra_pipeline_stage_review_20260927`，
  之后重跑 `audit_structure --only s16` 应转 `FAIL=0`。
  ⚠ **陷阱**：pre-commit 跑在**建提交对象之前**，扫的正是索引；只 `git add` 新路径不会让 FAIL 消失，
  「索引里有幽灵路径」这件事会一直卡住第②步，从而卡住整条提交链。
- **同类形态还有 1 处**：`reports/skills_review_20260929`（索引 2 件）↔ `…_refs`（索引 2 件）。
  这暴露一个可复用的结构缺口：**没有任何闸校「索引里的路径必须在工作树存在」**，
  于是「目录改名 = `cp` 新名 + 删旧名，但旧名删除不入索引」这种半截重命名可以长期潜伏
  （本报告把它登记为 §7 的 **S20 索引↔工作树一致性**）。
- 子目录风格混用：`eur-mining` `forum-experience` `gbr-campaign-final` `project-audit` `tooling-research`（连字符）
  vs `dataset_experience` `forum_alpha_research`（下划线）；
- `reports/diff_t4_20261010.py` 属「diff 脚本混入产物位」这一类（§8.12 规则⑤的同类形态在 `reports/` 侧再现），未跟踪。

**D-3 `*_refs` 后缀无登记语义**
`ra_pipeline_stage_review_20260927_refs/`、`skills_review_20260929_refs/` 两个快照目录，其用途只在
`reports/inventory_consolidated_*.md` 的方法注释里间接出现，AGENTS.md §8.13 没有这一类目录的归属条目。
→ 新 Agent 无法判断「该写进 `_refs` 还是原目录」。

### E. 冗余 / 空目录

- **skills 跨 skill 复制**：B 类 4 组（`validator.py` / `helpful_functions.py` / `ace_lib.py` / `diversity_enhancer.py`，
  已入基线棘轮）+ GEM 内嵌 A 类 4 组（设计内，由 `sync_gem_embedded_skill.py` 同步）。**未登记分叉 = 0**，
  即当前无静默分叉，属可控存量。
- **根 `wq-brain-ra-usa/` 才是真正未登记的巨型冗余**（455 件，见 A-1）。
- **空目录 153 个**：绝大多数在 gitignore 区 —— `cache/_scratch/pt/test_*`（pytest tmp 根，被保留但无人清理；
  `tools/retention.py` 三条策略覆盖 `data/*.bak*`、`cache/_probe/*.db`、`logs/`，**不含 `cache/_scratch`**）、
  `attic/json_archive/**`（归档遗留）。活跃源码树内**没有成规模的空目录**，此项不是问题。
- `.pytest_cache/`、`__pycache__/`（根 + tools/ + 各 skill scripts/）散落，属运行期噪声。

---

## 3. 推荐目录组织方案（最小改动版）

原则：**不重造布局**。AGENTS.md §8.13 的归属表已经是完备且自洽的，本次要做的不是新标准，
而是「把违反 §8.13 的存量迁回去」+「把 §8.13 没被机械覆盖的两条空白补成闸」。

```
wqb/
├── (根)                 # 只留 ROOT_ALLOWLIST：入口 + 配置 + 三件套文档
├── src/wqb/             # 公共核心包
│   ├── config.py        #   域常量单源（保留在顶层，被全网引用）
│   ├── paths.py
│   ├── contracts/       # 【建议收纳】wave_results_contract / registry_contract /
│   │                    #   recon_evidence / waiver / wave_id / submit_verdict_core
│   ├── store/ workflow/ expression/ profiles/ research/ modeb/ memory/ search/
│   ├── metrics/         # 【建议收纳】step_eval / step_events / step_scoring /
│   │                    #   shape_quota / towers / region_rotation / quota
│   └── db/              # 【建议收纳】db_conn / db_write_lock
├── tools/               # CLI 层：按 19 主题下沉（S11 已校归属，需开始逐批执行）
│   ├── gates/ verdict/ fields/ backtest/ ledger/ probe/ rotation/ research/
│   ├── code-audit/ data-repair/ lib/ legacy/ wave_gate_pkg/ git-hooks/
│   ├── docs/            # 【建议】README_*.md 五份并入（或指向 tools/README.md 的分页）
│   └── README.md        #   唯一索引；mcp_py → mcp_ping_helper.py（补扩展名）
├── world-quant-brain-mcp/   # 业务 MCP 前端（含 .venv，跟踪面 61 件）
├── wqb_db_mcp.py            # 本地 DB 后端：住根是设计内（体量债走 §8.4 第 9 条专项）
├── Claude/skills/           # skills 唯一源（51）
├── tracking/<REGION>/       # 区域业务：config/ scripts/ reference/ candidates/ + archive/
├── tracking/mining/         # 共享数据湖 —— 必须配 MANIFEST.json 才可继续增长
├── data/ cache/ logs/ results/   # 运行期（gitignore；cache/_scratch 纳入 retention）
├── reports/                 # 人工审计/复盘（<主题>_<YYYYMMDD>.md；子目录 kebab-case，存量 4 个登记）
├── output_report/           # 战役/评审产物唯一出口
├── docs/                    # 长期规范/SOP（日期报告外迁 reports/）
└── attic/<主题>_<YYYYMMDD>/ # 归档而非删除
```

---

## 4. 可迁移 / 重构清单（按类别，含目标位与手法）

| 类别 | 具体件 | 目标位 | 手法 | 备注 |
|---|---|---|---|---|
| **游离技能树** | `wq-brain-ra-usa/`（455 件） | `attic/stray_skills_root_20261014/` | 先核那 1 个分叉文件是否要回并 → 再整体移动 | **不是删除**（§7）；核 refs=0 已做完 |
| **运行中间产物（已入库）** | `tracking/USA/{robustness,perfmax}/*_2026100*/` 65 件 | `results/`（gitignore）或 `attic/usa_ablation_20261008/` | `git rm --cached` + 移盘，保留可回溯 | 判据：`plan/score/dispatch/all_exprs/variants` = 派发断点，非结论 |
| **战役产物 md** | `tracking/USA/campaign_20261014/0{1,2,3}*.md` | 台账进 `wqb-db`；叙述进 `output_report/` | 按 §5 规约 0 走 upsert | 禁止继续 `Write` 到 `tracking/*/` |
| **顶层报告** | `tracking/robustness_*.md` ×7 | `reports/robustness_<YYYYMMDD>.md` | `git mv` 保历史 + 同步引用 | §A 已做过一轮同类（apply2） |
| **一次性脚本** | `reports/diff_t4_20261010.py`（未跟踪） | `logs/_tmp_*.py` 或按判据留作 `reports/` 证据脚本 | 核 refs 后定 | §8.12 规则⑤同类 |
| **无扩展名脚本** | `tools/mcp_py` | `tools/mcp_ping_helper.py` | 改名 + `tools/README.md` 同步 | S14 登记名要一起改 |
| **工具文档** | `tools/README_*.md` ×5 | `tools/docs/`（或并入 README 分页） | 移动 + 改主 README 链接 | 顶层只留一个索引 |
| **docs 日期报告** | `docs/dryrun-audit-20260925.md`、`docs/region_universe_update_report.md` | `reports/` | `git mv` + 改名（日期作后缀） | 保持 docs = 长期规范 |
| **docs 二进制** | `docs/alpha模板.docx` | `research-data/` 或 `attic/`，并改名 ASCII | 移动 + 改引用 | §8.13 纯 ASCII 直违 |
| **数据湖索引** | — | 生成 `tracking/MANIFEST.json` | 跑 `generate_manifest.py` | ⚠ 该脚本会顺带把 >500 KB 件 zip 进 `tracking/archive/large/`，跑前先确认这一副作用是否可接受 |
| **S16 FAIL（幽灵路径）** | 索引里的 `reports/ra_pipeline_stage_review_20260927/**` 23 件 + `reports/skills_review_20260929/**` 2 件（磁盘已无） | 无 | `git add -u -- reports/`（**不是 `-A`**：§7 禁止顺带把别人的未跟踪件拖进暂存面）把删除暂存 | **不改文件名**：新 `_refs` 侧已被 S5 前缀豁免，实测 0 违规 |

> 迁移统一约束：一律 `git mv`（不是删除）、一次一个主题、每批跑
> `pytest tests/ -x` + `python tools/audit_structure.py` + `python tools/sync_skills.py --check`。

**§4 状态（2026-10-15 批次I 收尾时逐条复核）**：上表 11 行里 **9 行已执行**（游离技能树三份归档、
运行中间产物 89 件出库、`tracking/robustness_*.md` 回迁、`mcp_py` 改名、5 份工具文档进 `tools/docs/`、
2 份 docs 日期报告外迁、`.docx` ASCII 化、幽灵路径已暂存且升级为 S20 闸）。两处更正与两处未决：
⚠ 目标名实际落成 **`tools/mcp_http_caller.py`**，不是本表与 §3 树注释初写的 `mcp_ping_helper.py`
（改名时发现它是个通用 HTTP 调用器而非 ping 助手，按内容定名）；⚠ 运行产物行数交付时写 65，**实测 89**（§10.1#1）。
未决两行均**需用户点头**：`tracking/USA/campaign_20261014/` 战役产物 md 的台账化处置（§10.6），
以及 `reports/diff_t4_20261010.py` 的归属——复核实测它被 `output_report/deu_field_name_verification_20261010.md`
的第 121/201 行**引用两次**、且已在 `audit_structure.py:445` 的 `S5_EXEMPT_PREFIXES` 登记为**可重跑证据脚本**，
故「留 `reports/`」是成立的一支，但定夺权在其归属会话 / 用户，本轮不动。

---

## 5. 优先级与执行建议

**P0（今天，30 分钟内可清，且卡着提交）**
1. 处置 `wq-brain-ra-usa/`：回并 1 个分叉文件 → 整树进 `attic/stray_skills_root_20261014/`；
2. 暂存 `reports/` 的删除（幽灵路径），把 pre-commit 恢复到 `FAIL=0` —— 一条 `git add -A -- reports/`，不动文件名；
3. 把 13 份 `docs/reference/EUR/*.md`、5 份 `output_report/DEU_*|GBR_*.md`、
   `tests/unit/07_docs_skills/test_skill_no_hyphenated_report_paths.py` 与
   `docs/governance/output_dirs_taxonomy.md` 逐条裁决：入库 or 进 gitignore ——
   这是 §7「禁止 `git clean`」的**源头减量**动作。

**P1（本周，各为独立批次，互不阻塞）**
4. `tracking/USA/{robustness,perfmax}` 运行产物出库（`git rm --cached` + 归档）；
5. `tools/` 主题下沉首批 1 个主题（建议 `verdict` 或 `fields`，文件数少、refs 面清晰），
   验证配方可行后再批量推进（171 处 sys.path 是主要摩擦，按主题逐批降）；
6. `tracking/mining` 的 `MANIFEST.json` 生成（先确认 zip 副作用）；
7. 报告归属回迁（`tracking/robustness_*.md` → `reports/`）。

**P2（下个治理轮）**
8. `src/wqb/` 顶层散模块收纳（contracts / metrics / db 三个子包）；
9. `docs/` 顶层整理（日期报告外迁、`.docx` 迁出、大写命名改 snake_case）；
10. ~~`reports/` 子目录命名统一为 snake_case，并登记 `*_refs` 的语义~~ —— **交付时这条建议的方向是错的，
    批次G 已作废并更正（后半句「登记 `*_refs` 语义」已落地于 §8.13）**。权威 = AGENTS.md §8.13
    「目录：小写 kebab-case」，S11 的 19 个主题目录与 S17 的顶层目录都按它建；给 `reports/` 单开一套 snake
    等于再多一个风格例外。改名代价实测（`git grep -o -h` 行数/文件数）：`dataset_experience` 40/24、
    `forum_alpha_research` 20/12、`ra_pipeline_stage_review_20260927_refs` 43/17、`skills_review_20260929_refs` 9/5
    —— 四个不合规存量**没有一个**能单件安全改名（含 `template_families.json` 里的目录名与 S16 基线键）。
    **实际落地** = `audit_structure` S16 **规则⑦**：新建一层子目录必须 kebab（跟踪件 FAIL / 在途件 WARN），
    存量 4 条进 `S16_DIR_LEGACY` 逐条带代价证据、移出条件是「改名后旧路径 refs=0」；
    伞的失效判据取磁盘而非 git 跟踪面。守卫 `tests/unit/07_docs_skills/test_audit_structure_s16_dir_style.py`
    含**口径反查**用例（读 §8.13 那句声明的样式）—— 谁再照本条旧建议批量改 snake，本闸全部拦下，
    他必须来改这条测试，改时即读到这段裁决。
11. `tools/retention.py` 增补 `cache/_scratch/pt/` 策略（当前 153 个空目录主要来源）。

**P3（观感/可发现性）**
12. `tools/mcp_py` 补扩展名；`__pycache__` 与 `.pytest_cache` 的 gitignore 补全；
    宿主目录（`.qoder-cn`/`.clinerules`）显式登记。

### 5.1 本节 12 条的落地状态（2026-10-15 批次I 收尾时逐条**实测**复核，不凭记忆）

| # | 状态 | 读数 / 归属 |
|---|---|---|
| 1 | ✅ | 两份根技能树归档 `attic/root_skills_mirror{,2}_20261014/`，**同日第三次再现**见 §10.7；机制侧 `S17` + `sync_skills._is_repo_root_or_ancestor()` + `pull_skills.is_repo_root_dest()`（§9.1 第 2/3 条） |
| 2 | ✅ | 幽灵路径 25 件已暂存清掉；**并升级为闸**：`S20 索引↔工作树一致`，实测 `git ls-files --deleted` = 0（§9.1 第 1 条） |
| 3 | ⏳ **需用户点头** | 逐条裁决「入库 or gitignore」属对他人产物的处置权。现复核 = `docs/reference/EUR` 8 份（跟踪 2 + 未跟踪 6，§10.1#2）；`repo_governance_check` 的未跟踪源码仍是先行指标 |
| 4 | ✅ | **89 件**出库（`git rm -r --cached` **保盘不删**，磁盘 98 件一件不少），批次A/B/C；复发由 `S18` 拦（§10.2） |
| 5 | ✅ 首批 + ⏳ 逐批 | 首批 `db` 主题 2 件 `git mv` 进 `tools/db/`，`S11` 新读数「已下沉 23 个（THEMES 登记 ∩ 磁盘核验）」；**批量推进是长期程序**，配方与耦合数据在 `tools/README.md`「目录结构与迁移状态」 |
| 6 | ⏳ **需用户点头** | `MANIFEST.json` 未生成（工具 `generate_manifest.py` 已就绪、`--dry-run` 实测索引面 13867 件/78.2 MB）。缺的是「谁负责刷新」= S19，与生成动作互锁（§9.2 第 2 行） |
| 7 | ✅ | 批次D：4 件 `git mv` → `reports/`，skill 侧输出位同批改（生成端止血），S18 规则③拦复发 |
| 8 | ⏳ **需用户点头** | 87 文件 / 121 处 `from wqb.<模块>`（`db_conn` 单件 66 文件 71 处）+ 两个 MCP 服务需重启；属性式模块 patch 实测 = 0（§9.2 第 1 行） |
| 9 | ✅ | 批次E + §9.1 第 6 条：日期报告外迁、`.docx` ASCII 化、大写命名改 snake。实测全仓非 ASCII 跟踪件 **0**（§6 第 4 条注） |
| 10 | ✅ **且方向已作废** | 见本条原文的删除线与批次G：权威 = kebab，`S16 规则⑦` 新建即守 + 存量 4 条带代价登记 |
| 11 | ✅ | `retention.py` 五条策略（④ `cache/_scratch/pt/` basetemp 按签名判形、≥24 h；⑤ 顶层散件默认不动）；首轮实跑回收 **749 个目录 / 65.3 MB** |
| 12 | ✅ 三条全落地 | ① `mcp_py` → `tools/mcp_http_caller.py`（§9.1 第 5 条），并由 **批次I = S21** 把「必须有扩展名」从 `tools/` 顶层补到**全仓跟踪面**；② `git check-ignore -v` 实测 `__pycache__`（`.gitignore:10 **/__pycache__/`）、`.pytest_cache`（:79）；③ 宿主目录 `.qoder-cn`（:105）、`.clinerules`（:207）、`.workbuddy`（:25）、`.claude`（:34）**均已忽略**（`.vscode` 不在盘上，无需登记） |

⇒ **本节 12 条除 #3 / #6 / #8 三条明写「需用户点头」外全部闭合**；#5 的「批量推进」是长期程序而非未决项。

---

## 6. 命名规范（建议正式采纳为机械口径）

现有 §8.13 四条 + 本次补齐五条，建议照 §8.12 的做法写进 `audit_structure`（§7 第 7 条：
「同一类漂移出现第二次，就写工具或写测试把它机械拦住」）：

1. **目录**小写 kebab-case；`_` 前缀 = 同层内部/横切；第三方源码只进 `vendor/`。
   豁免（平台数据标识 / 历史名）：`tracking/<REGION>` 三字母大写、`Claude/`、`output_report/`。
2. **文件**纯 snake_case；包内私有实现 `_` 前缀；**活探针禁止 `test_` 前缀**（用 `probe_*`/`*_live`）。
3. **日期**人工报告与产物带 `YYYYMMDD` **作后缀**、不带杠；`docs/plans/` 保持 `YYYY-MM-DD-<主题>.md` 前缀；
   机器产物 `*_ideas.md`/`*_campain.md` 不强制日期（同名覆盖语义）。
4. **路径纯 ASCII**，无空格 / 中文 / Windows 保留名。（交付时的活样本违规：`docs/alpha模板.docx`
   —— **已消除**，§3 实施记录第 6 条 `git mv` 为 `docs/reference/alpha_template_community.docx`。）
   2026-10-15 复测：`git ls-files` 全索引面非 ASCII 文件名 **0 件**，`docs/` 面亦 **0 件**。
   ⚠ 机械面只覆盖一部分：S16 的取面先按 `S16_SUFFIXES`（报告类扩展名）筛，
   **`.docx` 这类二进制名不在面内** ⇒ 这次是人工改名 + 本报告登记读数，没有闸会抓到下一个。
5. **文件必须有扩展名**（新增）：无扩展名脚本不可被发现、`file` 判定与工具链都不认
   （反例 `tools/mcp_py`）。
   ✅ **已机械化（批次I，2026-10-15）= S21 跟踪件扩展名**，取面从 `tools/` 顶层扩到**全仓索引面**。
   落地时对本条口径的两处修正见 §10.11：点开头文件天然合法（判据不得用 `Path().suffix == ""`）、
   以及名字型 / 路径型两类豁免不可互换。
6. **技能目录名 == frontmatter `name`，纯 kebab**（已有契约）；
   **技能源唯一 = `Claude/skills/`**（新增）：任何顶层 `<skill-name>/` 目录都是事故，
   因为 `_skill_roots()` 从不解析仓库根层的技能名目录。
7. **同一父目录内风格不混用**（新增）：`reports/` 不得同时存在 `forum-experience` 与 `dataset_experience`。
8. **运行期产物命名 = `<实验/用途>_<YYYYMMDD_HHMMSS>/`，且必须落在 gitignore 路径**
   （`results/` `cache/` `logs/`）—— 名字带时间戳者**不得进版本控制**。
9. **快照/参考位需登记语义**：`*_refs` 这类后缀若继续使用，必须在 §8.13 写明「谁写、给谁读、是否入库」。

---

## 7. 机械守卫（结论 → 落地状态）

| 缺口 | 现状 | 建议闸 | 状态 |
|---|---|---|---|
| 未声明的顶层目录 | `check_s7_root_allowlist` 对 `p.is_dir()` **无条件 continue**（`ROOT_SKIP_DIRS` 因此形同虚设）；S9 只校「声明的在不在」，方向相反 | **S17 顶层目录白名单**：非点开头顶层目录必须在名单内，新增即 FAIL（不进基线） | ✅ **已落地** |
| 业务目录混入运行期产物 | 无任何闸看 `tracking/**/` 里的 `.log/.txt/时间戳目录`（实测 65 件已入库） | **S18 tracking 产物纯度**：`tracking/<REGION>/` 下出现 `*.log`、`<名>_<YYYYMMDD_HHMM>*/`、或 `dispatch/plan/score` 套件 → FAIL（存量入基线，棘轮只减） | ✅ **已落地（批次C，2026-10-14）** 实测 `--only s18` FAIL=0 WARN=0：`tracking/` 索引面 2611 件（交付时写 65 件是**已入库违规件数**，不是索引面），无时间戳目录、无 `.log`、顶层只 4 个登记件；守卫 `test_audit_structure_s18_runtime_purity.py` |
| **目录名对「按扩展名取面」的闸结构性失明** | S16 此前四面全是文件（`_s16_targets()` 按 `S16_SUFFIXES` 筛），于是 `reports/` 同层 5 个 kebab 与 4 个不合规并存无人报；与批次F 的「S11 看不见顶层非 `.py` 数据件」同族 | **S16 规则⑦**：`reports/`+`output_report/` 一层子目录名必须 kebab（跟踪件 FAIL / 在途件 WARN），存量 4 条进 `S16_DIR_LEGACY` 逐条带代价证据，伞失效判据取**磁盘**而非 git 面 | ✅ **已落地（批次G）** 取面实测 9 个一层目录、0 个未跟踪；守卫 `test_audit_structure_s16_dir_style.py` 9 例（含 `< 3` 判据回归、口径反查、fail-closed） |
| 数据湖无索引 | `MANIFEST.json` 从未生成，1053 件跟踪文件仍在增长 | **S19**：`tracking/mining/` 存在但 `MANIFEST.json` 缺失 → FAIL | ⏳ 待做 |
| 索引里的幽灵路径 | 全仓未暂存删除恰好 **25 件**（`git ls-files --deleted`），**100% 在 `reports/`**（两组 23 + 2）；无闸校这件事 | **S20 索引↔工作树一致**：`git ls-files --deleted` 非空即 FAIL，报错点名修法 `git add -u -- <路径>` | ✅ **已落地** |
| 「文件必须有扩展名」只在 `tools/` 顶层机械化（§6 规则⑤） | S11 取面 = `tools/*` 一层；S16/S18 取面先按 `S16_SUFFIXES` 筛扩展名 ⇒ 三条合起来，对**仓库其余 4000+ 件的无扩展名件**完全失明。活样本就是本轮亲手抓到的 `tools/mcp_py` | **S21 跟踪件扩展名**：取面 `git ls-files -z`（**整索引面、不带 pathspec**），基名不含 `.` ⇒ FAIL；两类豁免（名字型 `Makefile`/`Dockerfile`… 与路径型 `tools/git-hooks/*`）不可互换，路径型条目从盘上消失 ⇒ WARN 催删 | ✅ **已落地（批次I，2026-10-15）** 实测跟踪面 **4107 件、无扩展名 4 件且全部在白名单** ⇒ **违规 0、不建基线**；未跟踪件 80 个中 0 违规；守卫 `test_audit_structure_s21_extension.py` **11 passed**（含两条 fail-closed、伞半径互不替换、变异反查） |

### 7.1 S17 落地时被自己的首跑纠正的一处（重要，别照抄原建议）

**S17 不能按 §1 动态生成白名单。** 本报告初版建议的口径是「顶层目录集合 = §1 声明集 ∪ gitignore 运行期集
∪ `ROOT_SKIP_DIRS`」，实测这个写法**会在一个干净仓库上永久变红**：§1 只声明业务/代码目录，从不声明
`__pycache__`，而任何在仓库根跑 `python`（含 pytest）的动作都会把它建回来。本闸首跑即 FAIL，
offender 就是根 `__pycache__` —— 判红不指向任何可修事实，只会逼人 `--no-verify`。

落地口径改为三条，理由写进常量注释与 AGENTS.md §8.12：

- 非点开头目录必须在 `S17_TOP_DIR_ALLOWLIST`（**显式常量**；新增顶层目录 = 先在 §1 立项再登记，
  与 S11「顶层只减不增」同哲学：白名单不追随机器生成物）；
- **点开头目录一律放行**（`.claude` / `.clinerules` / `.qoder-cn` / `.workbuddy` 等宿主配置随客户端增减，
  逐个登记必然反复误红）；
- **机器自生成目录**（`__pycache__` / `.venv` / `.venvs` / `node_modules` / `.cache`）跳过，
  但**必须在 OK 读数里点名**（`另跳过机器自生成目录 ['__pycache__']`）—— 静默跳过 = 下一轮又把它当事故查一遍。

配套 `tests/unit/07_docs_skills/test_audit_structure_s17_s20.py` 12 例，含
「AGENTS.md §1 声明集 ⊆ S17 白名单」的**反向一致性反查**（两边打架时该修的是白名单，不是文档），
以及 S20 的 fail-closed 用例（`git` 命令失败**不得**当作通过 —— 与 S16 的「取不到受控清单不当作通过」同口径）。

---

## 7A. 本轮执行记录（报告交付后，按「最佳方案」授权推进）

| # | 动作 | 结果与证据 |
|---|---|---|
| 1 | 游离 skills 树归档 | **归档前复核分叉，结论与 §2.A-1 初判不同：那 1 个 GBR 分叉已自愈。** 复测 `diff -rq -x __pycache__ -x parsetab.py -x config.json -x ace.log wq-brain-ra-usa Claude/skills` = **0 行差异**（两份 `analyst-channel-breakthrough.md` 同为 18:47、8738 字节，字节相同）⇒ **无需回并任何内容**。整树 `mv` 至 `attic/root_skills_mirror_20261014/`（51 个顶层条目完整保留，可回溯）；仓库根不再有 `wq-brain-ra-usa/` |
| 2 | 解 pre-commit 卡点 | `git add -u -- reports/` 暂存 25 件删除 ⇒ `git ls-files --deleted` = **0**；旧路径从索引摘除（`git ls-files reports/ra_pipeline_stage_review_20260927` = 0），新路径 `…_refs/` 23 件**完好未动**，历史不损。`audit_structure` 读数 **FAIL 1 → 0**（WARN=5 均为存量基线项） |
| 3 | 新增 S17 + S20 | `tools/audit_structure.py` 实现 + `CHECKS` 注册 + 模块 docstring 两条 + S7 条目更正为「只校文件」；负例实测可红（临时顶层目录 → FAIL；临时未暂存删除 → FAIL 且报出数量与修法）；正例 `S17 [OK] 顶层 16 个目录全部已声明` / `S20 [OK]` |
| 4 | S17 误红自纠 | 首跑因根 `__pycache__` FAIL ⇒ 增 `S17_MACHINE_DIRS` 跳过集并在读数点名（见 §7.1）；复测该形态转 OK，真未声明目录仍 FAIL |
| 5 | 治理文档同步 | `AGENTS.md` §8.12（S 清单补 S13–S17/S20、FAIL 阻断集加 S17/S20、新增专门说明块）、§4 钩子口径 `S1–S16` → `S1–S20`；`tools/git-hooks/pre-commit` 头注 `S1–S14` → `S1–S20`（**两处原本就互相打架**：文档写 S16、钩子写 S14，本轮一并纠正） |

**明确未做（及原因）**

- **未提交**：本轮只做了两处索引操作 + 三个文件内容改动；工作区另有 **70 件修改、65 件未跟踪、
  34 件已暂存新增、25 件已暂存重命名**属并行会话，
  按 §7 第 1/2 条须显式挑路径、按主题成 commit —— 待用户点头后再做。
- **未动在途件**：`tracking/USA/campaign_20261014/`、`reports/diff_t4_20261010.py`、
  13 件 `docs/reference/EUR/*.md`、5 件 `output_report/DEU_*|GBR_*.md`、新守护测试
  `test_skill_no_hyphenated_report_paths.py`。这些「只以未跟踪形态存在」的源码是 §7 禁 `git clean`
  的存量风险源头，但属并行会话的在途工作，**不代其裁决**。
- **未跑 `sync_skills.py --apply`**：`test_sync_skills_reports_no_drift` 当前红，属已知自愈项
  （仓库副本新于安装位：GBR 三个新引用文件未同步；`wq-brain-ra-usa/references/unlit-tower-campaign-20261014.md`
  在 3 个安装位陈旧）。同目录 `test_skill_lint` 亦红，因另一会话正在改 `wq-brain-superalpha/SKILL.md`
  （`git diff` 可见其已加 `<!-- from config.prod_corr_max -->`，基线里那条待其自行 `--update-baseline` 摘除）。
  这两条**不由我代做**：前者会替别人的在途 skill 改动决定同步时机，后者要改的是别人的 fixture。
- **S19 未落地**（需先读 `generate_manifest.py` 的 >500 KB zip 副作用，并与「谁负责重跑 MANIFEST」一起裁决，
  属需用户点头的 P1 批次）。~~S18 未落地~~ —— **本行交付时准确，批次C 已落地**（见 §7 表首行与 §10）。

---

## 8. 本次已执行的验证与未验证项

已验证（机器级）：顶层目录体积与文件数、`git ls-files` 扩展名/顶层分布/大文件、
`git check-ignore -v`、`audit_structure`（全量读数，含新增 S17/S20 的正例与负例）、
`audit_skill_drift`、`doc_path_refs`、`audit_destructive_default`、`repo_governance_check`、
`diff -rq` 全量比对（归档前后各一次）、空目录全量枚举、`_skill_roots()` 解析链源码核对、
`pytest tests/unit/07_docs_skills/test_audit_structure_s17_s20.py` **12 passed**、
**根 `tests/` 全量回归（3184 passed / 6 failed / 22 skipped，6 条失败逐条取证见下表）**、
`git ls-files --deleted` 复测 = **0**、`audit_structure` 在全量回归之后复测仍 **FAIL=0 WARN=5**。

### 根 `tests/` 全量回归读数（本轮最后一次运行，已执行）

`pytest tests/ -q` = **6 failed / 3184 passed / 22 skipped（198 s）**。
按 §4 失败诊断纪律逐条取 traceback，**6 条全部归因到并行会话的在途改动，无一落在我改的 5 个文件上**
（我动的只有 `tools/audit_structure.py`、`test_audit_structure_s17_s20.py`、`AGENTS.md`、
`tools/git-hooks/pre-commit`、本报告；这 6 个测试文件对上述内容**零引用**，已 grep 核对）：

| # | 失败测试 | 根因（实测证据） | 归属 |
|---|---|---|---|
| 1 | `test_db_write_guards::test_no_naked_connect_outside_whitelist` | 白名单外裸 `sqlite3.connect` 共 8 处，全部在 `tools/fields/skeleton_panel.py`（7）与 `tools/gates/operator_coverage_audit.py`（1）——两件 `git status` 均为 **`A `（并行会话已暂存的新文件）** | 并行会话 |
| 2 | `test_index_tables::test_env_registry_covers_every_env_var_read_by_code_and_nothing_is_stale` | 未登记变量 `WQ_MCP_LOOP`：`git show HEAD:world-quant-brain-mcp/main.py \| grep -c WQ_MCP_LOOP` = **0**，即它来自 `main.py` / `wqb_db_mcp.py` 的**未提交**改动（事件循环策略），而 `docs/env_registry.json` 干净未动 | 并行会话（§8.10「先登记再写文案」未走完） |
| 3 | `test_profiles_layer::test_region_skills_exist_and_match_cells_and_settings` | 6 个孤儿分支文件（DEU 2 / GBR 3 / USA 1），含 `GBR_pv_channel_breakthrough_20261014.md`、`unlit-tower-campaign-20261014.md`（**今日**新增）→ 加引用文件后未跑 `-m wqb.profiles render --apply` | 并行会话 |
| 4 | `test_audit_fixes::test_sync_skills_reports_no_drift` | 安装位落后仓库：GBR 3 件新引用 MISSING + `wq-brain-ra-usa/references/unlit-tower-campaign-20261014.md` 在 3 个安装位 STALE | 并行会话（跑 `sync_skills.py` 自愈，不代决定同步时机） |
| 5 | `test_skill_lint::test_no_new_skill_lint_violations_and_baseline_never_goes_stale` | 他人 `git diff` 给 `wq-brain-superalpha/SKILL.md` 加了 `<!-- from config.prod_corr_max -->`，基线那条变陈旧，须由改动方 `--update-baseline` | 并行会话（改的是别人的 fixture） |
| 6 | `test_op_arity::test_no_false_positives_on_accepted_alpha_corpus` | 语料**直接读 `data/wqb.db`**（`alphas.expression` ∪ `backtest_results.code` 里有 `alpha_id` 的行）：2 条平台已接受的 `quantile(…, 8)` 被元数检查误杀。DB 内容由战役会话持续写入，与静态代码无关 | 数据面漂移（战役会话写入的语料） |

**为什么没有一条能算我引入的**：① 1/3/4/5 点名的是磁盘上**别人新增/修改的文件**，我一件未动；
② 2 的触发条件（`WQ_MCP_LOOP`）在 HEAD 里不存在，只活在我的改动之外的未提交 diff 里；
③ 6 走的是生产库语料，本会话**未对 `data/wqb.db` 做任何写入**；
④ 我唯一新增的测试文件与 S17/S20 在全量运行里**通过**（3184 例含之）。
未做 `git stash` 对照 —— 工作区有 **70 件修改、65 件未跟踪、34 件已暂存新增、25 件已暂存重命名**
（除我这三个文件与本轮 25 件重命名外均属并行会话），
stash 会连带别人的在途工作，代价高于本次已足够的证据链。

未执行 / 未验证：
- **未裁决** 845 件抢救点独有源码与 1707 件被忽略源码类文件的具体归属（属 `snapshot_adjudicate` 专项）；
- **未判定** `generate_manifest.py` 的 >500 KB zip 副作用是否可接受（生成前先读该脚本）；
- 未跟踪的 `reports/diff_t4_20261010.py` 与 `tracking/USA/campaign_20261014/` 属**并行会话在途工作**，
  本报告只给归属判据，不代其移动。

> ↑ 本节写于 §7A/§9 之前。**「未判定 zip 副作用」一条已被 §9.2 取代**（已读该脚本并加了
> `--dry-run` / `--no-archive`）；其余两条仍然有效。

---

## 9. §3 实施记录（同日晚些，按「按 §3 推荐目录组织方案实施」指令执行）

原则与 §3 一致：**最小改动、`git mv` 保历史、一次一个主题、每批跑全套验证**。
下面每条都带机器读数；**没有读数的写法一律不写**。

### 9.1 已落地

| # | §3 条目 | 动作 | 机械读数 / 证据 |
|---|---|---|---|
| 1 | 根层白名单 | `audit_structure` 新增 **S17**（顶层目录必须已声明）+ **S20**（索引不得挂幽灵路径）；S7 口径更正为「只校文件」 | `S17 [OK] 顶层 16 个目录全部已声明（另跳过机器自生成目录 ['__pycache__']）`；守护测试 `test_audit_structure_s17_s20.py` |
| 2 | 游离技能树 | 两份都按「核三项 → 归档」处置：`attic/root_skills_mirror_20261014/`（19:40）与 **同日 20:01 再生的第二份** `attic/root_skills_mirror2_20261014/`（含 README 记明指纹与回滚法） | 归档前 `diff -rq` **零条 `Only in wq-brain-ra-usa`**（无独有件）、`git ls-files` = **0** ⇒ 搬走不丢信息；`repo_governance_check` 的未跟踪源码 **488 → 72**（差 416 件全部来自这一份镜像） |
| 3 | 复发机制从「人工归档」升级为「机制拒绝」 | ① `sync_skills.py::_is_repo_root_or_ancestor()`：枚举与显式 `--target` 两路都拒仓库根/祖先；② `pull-brain-skills/scripts/pull_skills.py::is_repo_root_dest()`：`--dest == 仓库根/祖先` **exit 3 且无 `--allow-live-dest` 逃生口** | 第二份同名件 mtime 与 `Claude/skills/` **逐纳秒相同** ⇒ 是保留 stat 的拷贝（`copy2` / `copytree` 语义），不是原地改名或硬链接（实测 inode 不同、`nlink=1`）。sync 那条已实测拒根生效（`WQ_SKILLS_DIR=<repo>` ⇒ stderr「已拒绝 1 个安装位」且其余 6 位照常同步），所以嫌疑是**绕过 sync_skills 的写入**；本仓自有工具里剩下的唯一 `--dest` 可指到仓库根、且按 `<dest>/<skill-name>/` 落盘的，就是 `pull_skills.py`（其 `live_roots()` 只列活跃 skill 根，**不含仓库根本身**）⇒ 补该条。守卫：新增 2 个测试（含「默认暂存位 `attic/import_staging` 不得被误杀」）⇒ `test_pull_skills_safety.py` **12 passed**。若第三次再现，写入方在我们工具之外，S17 会阻断提交，处置见 `attic/root_skills_mirror2_20261014/README.md` |
| 4 | `tools/` 顶层杂物：工具文档 | 5 份 `README_*.md` `git mv` 进 `tools/docs/`，`tools/README.md` 保持**唯一索引** | `git status` 5 条 `R`；`git grep "tools/README_(PERF_MAX\|OPTIMIZATION\|…)\.md"` 除新址外 **0 命中**（无死指针） |
| 5 | `tools/mcp_py` 无扩展名 | **原地改名** `tools/mcp_http_caller.py`（不是归档：它有 `__main__`，是在用 CLI），并顺手拆掉内嵌的 `D:\…\wqb-share-03` 绝对路径与退役的 `127.0.0.1:8876` 端点 —— 缺 `.py` 正是它对 S4/S14 **完全隐形**的原因 | `tools/README.md` 第 235 行登记；新读的 2 个环境变量已按 §8.10 先登记 `docs/env_registry.json` 再 `index_tables.py env --apply`（`[APPLIED] env-table` → `--check` `[OK]`） |
| 6 | `docs/` = 长期规范 | 5 件迁出/归位：`dryrun-audit-20260925.md`→`reports/dryrun_audit_20260925.md`、`region_universe_update_report.md`→`reports/region_universe_update_20260911.md`（补日期后缀）、`S1_FIELD_CATALOG_CACHE_GUIDE.md`→`docs/reference/s1_field_catalog_cache_guide.md`（ASCII 化）、2 件 `modeb_*`→`docs/design/`；`docs/alpha模板.docx`→`docs/reference/alpha_template_community.docx` | `ls -p docs` 现只剩规范件 + 8 个主题子目录；全仓非 ASCII 文件名扫描 = **0 件**；该 `.docx` 由 `.gitignore:128` 专行忽略（**未入库，只修名字**） |
| 7 | 运行期：`cache/_scratch` 入保留策略 | `retention.py` 从 3 条策略扩到 **5 条**：④ `cache/_scratch/pt/` 的 pytest basetemp（按签名 `^(?:test_\|pytest-).+\d$` 判形，≥24 h）⑤ 顶层散件（**默认不动**，需 `--scratch-files`，且 `*_spec.json`/`*_variants.txt`/`*.items.json` 永不收） | 首轮 `--apply` 回收 **749 个 basetemp 目录 / 65.3 MB**；守护 `tests/unit/01_store_db/test_retention.py`；AGENTS.md §8.4 第 6 项已同步为五条 |
| 8 | `tools/` 按主题下沉开始执行 | 首批选 **db** 主题 2 件（`git mv` 进 `tools/db/`）。选它的判据是实测引用面最小：`Claude/skills/**` **零命令引用**，外部耦合只有 1 个测试的 `sys.path` 注入 + 4 处文档指针 | `S11 [OK] 顶层 153 个与基线一致（基线 153、已下沉 23、未归属 0）`；`S14 [OK] 149 个受控 CLI 全部登记`；两件的 `--help` 与 `db_lock_audit --once` 实跑过 |
| 9 | 「下沉进度」必须可度量 | S11 旧读数 `len(baseline) − len(now & baseline)` 是**反向失真**的：真迁完并按闸提示移出基线后它就归零。改为 **`THEMES.moved_files` ∩ 磁盘实核**（顶层少一个**且**子目录多一个才算），登记与磁盘不符 ⇒ **FAIL** | 新读数 `已下沉 23 个（THEMES 登记 ∩ 磁盘核验）`；守护 `test_audit_structure_s11_moved.py` **5 passed**（含 `ac2cf35`「子目录新建冒充下沉」负例） |
| 10 | 数据湖索引器工具化 | `generate_manifest.py`：去本机盘符（`_find_repo_root()`）、`generated` 不再硬写 `2026-08-14`、加 `--dry-run` / `--no-archive`、加 `total_bytes`、`main(argv)` + `sys.exit` | `--dry-run` 读数：**索引面 13867 件 / 78.2 MB，其中 >500 KB 的 19 件合计 17.8 MB**（零写盘） |

### 9.2 评估后不做 / 暂缓（每条给实测判据，不是「没时间」）

| 条目 | 结论 | 实测判据 |
|---|---|---|
| `src/wqb/{contracts,metrics,db}` 收纳 15 个散模块 | **未做，需用户单独点头** | 按 §8.4 第 9 那一问做了机械清点（取面 = 3817 个跟踪件，排除 `src/wqb/` 包内自引用与 `attic/`）：**属性式模块 patch = 0** —— 正则命中的 2 处是 `tools/campaign_intel.py` SQL 里的 `e.wave_id=w.id` 列赋值，人工核过不是 `setattr(mod, …)` 形态 ⇒ 最坏那类风险不存在。暂缓的真实理由是外部引用面：**87 个文件 / 121 处 `from wqb.<模块>`**，其中 `db_conn` 单件 66 文件 71 处（它还持有 `DIRECT_CONNECT_WHITELIST`，被裸连接守护测试当单源读），且两个 MCP 服务正在运行、改包路径要重启才生效。另外 `git mv src/wqb/step_scoring.py src/wqb/metrics/` 被权限闸按 §8.4-9 + 台账既有「暂缓」决定拦下 ⇒ 属需明示的结构性改动，不该夹在布局清理里顺手做 |
| 生成 `tracking/MANIFEST.json` | **未生成**（工具已就绪） | §5 P1 自己写明 `tracking/` 占跟踪文件 64%：一次生成 ≈2.9 MB 机器产物入库，而**没有刷新闸**（S19 未落地）→ 立刻变成新的幽灵索引（§8.4 第 3 条 `mining/` 战例同形态）。且默认路径会把 19 件 >500 KB 另拷进 `tracking/archive/large/`；要产出需先定「谁负责重跑」再 `--no-archive` 单飞 |
| `reports/` 连字符子目录改 snake_case | **不改名，只登记语义** | 实测 `_refs` 是 2026-10-10 输出目录治理 **P2-C** 的同名消歧后缀（`<主题>_<日期>.md` 与同名目录并存 → 目录加 `_refs`，主体因被 `closure_ledger.py` + tests + skills 文档 20+ 处引用而不动）。消费方就是**报告主体自己的复现命令**（`ra_pipeline_stage_review_20260927.md:6,516,1234-1319`、`skills_review_20260929.md:6,2372-2374`）⇒ 再改一次名 = `doc_path_refs` 的**新增 BROKEN**（棘轮硬闸）。本轮把正确语义写进 AGENTS.md §8.13，**并更正了本报告交付时我初登记错的出处**（曾误记为「`snapshot_adjudicate` 的抢救点目录」——实测 `docs/governance/snapshot_adjudication.md` 里 `_refs/` 命中为 **0**，只有恰好含该子串的文件名） |
| `forum` 主题下沉（第二批候选） | **放弃本批** | 实测 `forum_cache_builder.py` 单件被 3 份 skill 文档 + `docs/env_and_switches.md` + `docs/env_registry.json` + `docs/skills_review_closure.json` 按名引用，并有专用路径测试 `test_forum_cache_builder_paths.py`；且 `forum_recon*.py` 的归属在 `THEMES.json` 里挂在 **gates** 主题下 —— 主题边界要先裁。已写进 `THEMES.json._moved_20261014.not_moved_this_batch` |
| S18（tracking 存量基线）/ S19（MANIFEST 刷新闸） | **未落地** | 二者互锁：S19 的价值取决于 MANIFEST 是否产出，而后者见上一行 ⇒ 同批决策。S18 需先给 `tracking/` 存量建基线，属 P1 独立批次 |

### 9.3 收尾验证（本轮最后一次，全部实跑）

| 检查 | 读数 |
|---|---|
| `pytest tests/ -q` | **6 failed / 3193 passed / 23 skipped（183 s）** |
| `audit_structure.py` | **FAIL=0** WARN=5（5 条均为存量基线项：S1 172 处 `sys.path`、S13 `PPA_USA` 登记项已不存在、S16 40 件存量 + 2 件在途、S6 4 组跨 skill 复制） |
| `sync_skills.py --check` | `[OK] 6 个安装位全部一致`（本轮跑过 `--apply`：18 个文件 × 6 位） |
| `doc_path_refs.py` | **0 BROKEN**；2 条 UNTRACK 告警不阻断——其一是本轮新增的 `test_audit_structure_s11_moved.py` 被 AGENTS.md 引用 ⇒ **该测试须与 AGENTS.md 同批提交** |
| `audit_destructive_default.py` | 扫 455 个 `.py`，基线 0 条，**无新增高危** |
| `audit_node_registration.py` | 五处一致 **20 = 20 = 20 = 20 = 20**，退出码 0 |
| `repo_governance_check.py`（不带 `--warn`，硬判） | **exit 1**：未跟踪源码 72 件（并行会话存量；根镜像归档前是 488）。钩子里它是告警位，**不阻断** |

**6 条失败的归属**（沿 §8 那张表，本轮又清掉 2 条）：

- 已清掉：`test_s17_passes_on_this_repo`（根镜像归档）、`test_sync_skills_reports_no_drift`（跑 `sync_skills.py` 自愈）。
- 仍红 6 条，逐条取证，**无一落在我改的文件上**：① `test_no_naked_connect_outside_whitelist` —— 8 处裸 `sqlite3.connect` 全在 `tools/fields/skeleton_panel.py`(7) 与 `tools/gates/operator_coverage_audit.py`(1)，两件 `git status` 均为 **`A `（他人已暂存的新文件）**、HEAD 里不存在；② `test_weighted_leg_mixes…` —— 4 行命中全在 `Claude/skills/wq-brain-ra-gbr/references/`（含今日新增 `GBR_first_full_gate_alpha_20261014.md`）；③ `test_no_new_skill_lint_violations…` —— 他人给 `wq-brain-superalpha/SKILL.md` 加了 `<!-- from config.prod_corr_max -->`，基线那条须由改动方 `--update-baseline`；④ `test_env_registry_covers…` —— 唯一未登记变量是 `WQ_MCP_LOOP`，`git show HEAD:world-quant-brain-mcp/main.py \| grep -c` = 0 ⇒ 来自未提交 diff（**本轮我自己引入的 2 个变量已按 §8.10 先登记再 `--apply`**）；⑤ `test_no_false_positives_on_accepted_alpha_corpus` —— 语料直读 `data/wqb.db`，本会话未写库；⑥ `test_region_skills_exist_and_match_cells_and_settings` —— 6 个孤儿分支文件（DEU 2 / GBR 3 / USA 1），他人加引用件后未跑 `-m wqb.profiles render --apply`。

### 9.4 未提交，待用户决定

本轮**没有做任何 commit**（用户未要求）。工作区态势：**88 件修改、69 件未跟踪、37 件已暂存新增、
34 件已暂存重命名、4 件 `RM`**；其中属本轮主题的才该进同一个 commit，按 §7 第 1/2 条显式挑路径，
禁止 `git add -A`。需要用户点头的三件事：

1. **是否现在成 commit**（若要，我按主题拆：布局批次 / S17-S20+S11 读数 / retention / pull_skills 拒绝 / 文档同步）；
2. **`src/wqb` 收纳要不要做**（87 文件 / 121 处 import 的批量改路径 + 重启两个 MCP 服务）；
3. **`MANIFEST.json` 的归属决策**：产出（并立刻补 S19 刷新闸）还是维持「工具就绪、不产出」。

---

## 10. 交付后同日续做记录（批次A–I，2026-10-14 晚间起，批次I 收到 10-15 凌晨）

用户指令 = 「看报告其它地方还有哪些需要完善继续推进，直到达到目标架构」。
方法沿用 §8.12 那条：**先改生成端（工具缺省 / skill 指令），再清存量入闸面，再补机械闸，
再写非空过 + fail-closed 守卫，最后同步治理文档**。下面 §10.1 是本报告自身的更正面 ——
**读这份报告必须以本节为准**。

### 10.1 本报告交付时的四处失实（按此读原文）

| # | 原文位置 | 原写法 | 实测更正 |
|---|---|---|---|
| 1 | §1 P1 表、§2.B-2、§4 表、§7 表 | `tracking/USA/{robustness,perfmax}` 运行产物 **65 件** | **89 件**。65 只数了 `robustness/`，`perfmax/` 另有 **24** 件。口径 = `git ls-tree -r HEAD -- tracking/USA/robustness tracking/USA/perfmax`；按文件名首段分：`variants_*` 54 · `dispatch*` 13 · `plan.json` 9 · `score(.json)` 6 · `all_exprs.txt` 5 · `match`/`sim` 各 1。S18 的 docstring 从一开始就写的 89，两边打架过 ⇒ **以 89 为准**（闸内数字来自实测，报告正文来自目测） |
| 2 | §1 P0 表、§5 P2#3、§7A | **13 份** `docs/reference/EUR/*.md` 只以未跟踪形态存在 | 现复核 **8 份**：已跟踪 2（`analyst_dataset_analysis.md`、`mining_experience_by_category.md`）+ 未跟踪 6（日期 20261010–20261014）。该路径自 2026-10-12 起**零提交**、HEAD 只 2 件 ⇒ 差额 5 份从未入库且已不在盘上。**这条就是 P0 那条红线的活样本**：只以工作区未跟踪形态存在的产物会无声消失，且 `git checkout`/`reflog`/`fsck` 全都救不回来 |
| 3 | §3 树注释、§5 P2 第 10 条 | 「`reports/` 子目录命名统一为 **snake_case**」 | **方向错，作废**。权威 = AGENTS.md §8.13「目录：小写 kebab-case」（S11 的 19 个主题目录、S17 的顶层目录都按它建）。已在原处就地更正并写明代价实测（见批次G） |
| 4 | §7 表「S18 ⏳ 待做」、§7A「S18/S19 未落地」 | S18 未落地 | **S18 已落地（批次C）**：`--only s18` 实测 FAIL=0 WARN=0，`tracking/` 索引面 2611 件、顶层只 4 个登记件。S19 仍未落地（需用户点头，见 §10.6） |

### 10.2 批次台账（A–I）

| 批次 | 动作 | 关键证据 | 落地的闸 |
|---|---|---|---|
| **A** | 度量 `tracking/` 运行产物入库面 + 定位生成端 | 89 件（见 §10.1#1），9 个时间戳目录，全部是 `plan/dispatch/score/all_exprs/variants` = **续跑断点非结论**；写入方 = `tools/verdict/perf_max.py` 缺省 `plan_dir = tracking/<region>/perfmax/<alpha_id>_<时间戳>/` | — |
| **B** | **止血**：生成端缺省输出位改到 gitignore 路径 | 缺省改 `results/perfmax/<region>/`；`.gitignore:194/195` 新增 `tracking/*/perfmax/`、`tracking/*/robustness/` | — |
| **C** | 清存量 + 拦复发 | `git rm -r --cached`（**保盘不删**，§7「归档而非删除」）⇒ 索引面 89 件全部 `D `，磁盘 98 件一件不少；旧 robustness 报告 `git mv` 保历史 | **S18 tracking 产物纯度**：① 时间戳运行目录 ② `*.log` ③ `tracking/` 顶层白名单。判据取**索引面而非磁盘**（违规的定义是「进了版本控制」）；**FAIL 不进基线** |
| **D** | `brain-alpha-robustness` 报告回迁 `reports/` | `tracking/robustness_*.md` ×4 `git mv` → `reports/`，另 3 份新落 `reports/`；skill 侧报告输出位同批改；`src/wqb/robustness_record.py` 随动 | S18 规则③（该层只允许 `.gitignore`/`MANIFEST.json`/`README.md`/`region_config.json`） |
| **E** | `docs/` 结论式报告外迁 | `docs/reference/CODE_QUALITY_SUMMARY.md` → `reports/code_quality_summary_20260819.md`、`INTEGRATION_COMPLETE.md` → `reports/diversity_enhancer_integration_20260817.md`、`docs/dryrun-audit-20260925.md` → `reports/dryrun_audit_20260925.md`、`docs/region_universe_update_report.md` → `reports/region_universe_update_20260911.md`（全部 `RM`，日期改后缀，§8.13 三条同时合规） | S16 规则⑥（**docs 面**）：此前 S16 只看 `reports/`+`output_report/`+`tracking/` 顶层，`docs/` 整层失明；现受控面实测 82 个跟踪件 + 7 个在途件 |
| **F** | `tools/` 顶层**数据件**归属 | `tools/skeleton_quota.json` → `tracking/KOR/reference/skeleton_quota.json`（带 `_owner` 溯源键）；顶层非 `.py` 件实测 = 3（`README.md`/`THEMES.json`/`audit_structure_baseline.json`），全部在 `TOOLS_TOP_DATA_ALLOWLIST` | **S11 取面扩到「顶层非脚本件」**（新增第⑦条）+ 移除第二处 fail-open（见 §10.4）；搬出过程抓到一条真 bug（见 §10.5） |
| **G** | `reports/` 子目录风格 | 一层目录实测 9 个：5 kebab + 4 不合规（`dataset_experience`、`forum_alpha_research`、两个 `*_refs`）；`output_report/` 现无一层子目录。改名代价实测（`git grep -o -h` 行数/文件数）= 40/24、20/12、43/17、9/5 ⇒ **没有一个能单件安全改名** | **S16 规则⑦**：新建即守 kebab（跟踪件 FAIL / 在途件 WARN），存量进 `S16_DIR_LEGACY` 逐条带代价证据，移出条件 = 「改名后旧路径 refs=0」；伞失效判据取**磁盘**而非 git 面。守卫 `test_audit_structure_s16_dir_style.py` 9 例，变异核验两次都被抓（`< 3`→`< 2`、FAIL→WARN） |

| **H** | 测试**直写生产库**的第二、第三条路径（门面有闸，store 与 toolkit 没有） | 一手证据：`tests/unit/04_gates/test_inspect_mode_failclosed_p1p1.py` 用 subprocess 起 `tools/wave_gate.py`，子进程拿 CLI 缺省库位 = `data/wqb.db`，实测写入 `KOR/gate_ws2_pytest_inspect_model109`（`updated_at=2026-10-14T23:27:21`）；库里同期还有 **5 个**测试写入窗口共 **24 行 / 23 个键名**（判据与逐条见 §10.10.4）；10-15 按「白名单七件逐件过」再抓到 toolkit `_lib/db.py` 这条第三路径（§10.10.7） | 判定本体上移到**唯一连接工厂** `wqb.db_conn.reject_production_db_under_tests()`，`CampaignStore.__init__` 与 `wqb_db_mcp` 门面共用一份，toolkit `_lib/db.connect()` **委托**同一份（不复制判据）；守卫 `TestProductionDbGuardUnderTests` 7 例（含「不得出现第二份判定」的源码级反查 + 「临时库照常可建」的非空过对照） |
| **I** | §6 规则⑤「文件必须有扩展名」补到**全仓**（此前只有 S11 管 `tools/` 顶层） | 独立复算：跟踪面 **4107 件**，基名不含 `.` 的 **4 件** = `tools/git-hooks/{pre-commit,commit-msg}` + `world-quant-brain-mcp/{Dockerfile,Makefile}`，**全部已在白名单** ⇒ 违规 0；未跟踪面 **80 件 / 0 违规**。⇒ **本闸无基线**（空债面建基线 = 留永久通道，同 S16 docs 面的取舍） | **S21 跟踪件扩展名**：取面 `git ls-files -z` 不带 pathspec；判据 = `"." not in name`（**不是** `Path().suffix == ""`）；两类豁免伞不可互换；FAIL 不进基线 + 两条 fail-closed。守卫 11 例，**变异反查顺手挖出一条死分支**（详见 §10.11） |

### 10.3 一条同族发现：**「按扩展名取面」的闸对目录名同样是结构性失明**

本轮三次撞上同一族，且三次都是**人读目录才发现、闸一道不报**：

1. S11 缺「顶层**无扩展名**件」（批次前，`tools/mcp_py`）；
2. S11 缺「顶层**非 `.py` 数据**件」（批次F，`tools/skeleton_quota.json`）；
3. S16 缺「**目录名**」（批次G，`reports/` 混风格）—— 因为 `_s16_targets()` 按 `S16_SUFFIXES` 筛文件，目录根本不在取面里。
4. **同族的第四个方向（批次I）：不是「按扩展名筛」，而是「只在局部有闸」** —— 规则⑤「文件必须有扩展名」
   本身按名字判、不受扩展名筛影响，但它**只挂在 S11 的 `tools/*` 一层面**上 ⇒
   仓库其余 4000+ 件同样无人校。判据正确、覆盖面局部，结果与失明一样。

⇒ 新增闸时的自检两句：**这个闸的取面是文件面还是目录面？它按不按扩展名筛？**
按扩展名筛的闸默认看不见无扩展名件、看不见非脚本数据件、看不见目录名。
**以及：这条约定挂在哪个目录上？其余目录有没有同一件事在发生？**
⚠ **不要和 §10.10.6 混引**：那条是「取面对了、判据形状错」，与取面失明无关。

### 10.4 本轮移除的两处 fail-open（pre-commit 只拦 FAIL，所以这类写法等于闸会静默消失）

- `audit_structure.py` S11：旧代码 `if not baseline: return` —— 「`.py` 存量清单读不到」连带**关掉同闸其余全部检查**，读数只剩一行 WARN，看着像本闸已评估。现只跳过确实依赖基线的 `added`/`gone` 两条，其余照校；负例 = `test_baseline_missing_does_not_disable_the_rest`。
- S16 规则⑦：取面抛 `RuntimeError` 时**必须 FAIL**，不得当作「目录风格全部合规」（同 S14/S16/S18/S20 口径）；负例 = `test_fail_closed_on_git_error`。
- 同批修正一处**判据方向**：伞失效（登记项对应目录已不在）若用 git 跟踪面判，会把「目录还在、只是暂无跟踪件」误报成伞失效，而这条 WARN 让人做的动作恰恰是**删条目** ⇒ 改为磁盘判据 `_s16_dir_on_disk()`。这条与 §8.13 里「别按 S13 的 WARN 提示把 `PPA_USA` 删掉」是同一坑的两个方向。

### 10.5 批次F 搬家搬出的一条真 bug（值得单独记）

`skeleton_quota.json` 迁走后，`tracking/KOR/scripts/build_wave.py:load_quota_config()` 落到兜底
`skeleton_tags.DEFAULT_QUOTA` —— **两个形状不匹配**（前者是 `{"dimensions": {dim: {name: {cap, min}}}}`，
后者是扁平结构），于是 `.get("dimensions")` 取空 ⇒ **多维配额静默返回 0 候选**，波次照开、照跑、照入库，
只是永远选不出东西。复现：改前 `picked=[]`、改后 `picked=3`。
修法 = 新增 `default_quota_config()` 把兜底归一成同一形状 + 找不到配置文件时打印 `[warn] …改用代码缺省（仅 cap、无 min）`。

> **纪律：搬一个数据件，要顺手核它每一个读取方的兜底路径。缺省值形状不匹配 = 静默罢工，比缺文件更糟。**

### 10.6 需用户点头的未决项（本轮一律未动）

| 项 | 状态 | 为什么不能由我裁 |
|---|---|---|
| 成 commit（按主题拆） | 未做 | 用户未要求；工作区并行会话量大。收尾复测快照（`git status --porcelain` 共 **342** 条）：暂存面 **176** = 89 删除 + 45 重命名（37 `R `/8 `RM`）+ 40 新增（37 `A `/3 `AM`）+ 2 修改，工作区另 95 件未暂存修改、**71 未跟踪**。⚠ 这组数在并行会话下每分钟都在漂，只作**量级**依据：按 §7 第 1/2 条必须显式挑路径，绝不 `git add -A` |
| `src/wqb/{contracts,metrics,db}` 收纳 | 未做 | 外部引用面 87 文件 / 121 处 `from wqb.<模块>`（`db_conn` 单件 66/71），且两个 MCP 服务正在运行 |
| `MANIFEST.json` + S19 | 未做 | 先定「谁负责重跑」，否则立刻变成新的幽灵索引（§8.4 第 3 条 `mining/` 战例同形态） |
| `docs/reference/EUR` 8 件（2 跟踪 + 6 未跟踪） | 未动 | 6 件是并行会话在途产物（含今日），不代裁决 |
| 快照台账 PENDING 514 件 | 未动 | 逐件裁决属治理专项，且 `f676a72` 已加改名识别止幻影 |
| 第三方包 `cnhkmcp`（QuantFlow） | 只报告 | 卸载/打补丁属对外部代码的写操作。已实测**排除**它是根镜像写入方：`general_tools_directory()` 的落位恒为 `<wd>/.quantflow/general_tools/<tool_key>`，而仓库根没有 `.quantflow` |
| `ledger_kv` 里可机械识别的 24 行测试形态件（23 个键名；判据与逐条清单见 §10.10.4） | **一律未动** | 删行 = 对生产库的写操作。且这 24 行是**下限**：10-04 那个窗口 17 行里只有 4 行带指纹，其余与真实波次命名同形；F1 前三批与 F3 全部与真实写入同分钟共写（123/403/708/854/1064 行）⇒ 按键名形状与时间窗都切不开。逐条裁决留给数据主人 |
| `tracking/USA/campaign_20261014/`（盘上 5 件，未被 gitignore） | 未动 | ⚠ 一旦 `git add`，**S18 规则① 当场 FAIL**：`S18_RUN_DIR_RE = ^[^/]+_\d{8}(?:_\d{2,6})?$` 命中 `campaign_20261014`。这不是误报 —— 该目录里是 `01_S0_S1_*.md … 04_final_report.md` 的**叙述件**，§4 该行给的路径就是「台账进 `wqb-db`、叙述进 `output_report/`」；改由谁在什么时候做，属该会话的事 |
| `reports/diff_t4_20261010.py`（未跟踪）留 `reports/` 还是落 `logs/_tmp_*.py` | 未动 | 复核实测（批次I）：被 `output_report/deu_field_name_verification_20261010.md` 第 121/201 行引用，且已在 `audit_structure.py:445` 的 `S5_EXEMPT_PREFIXES` 登记为可重跑证据脚本 ⇒ 「留 `reports/`」有成立依据，但**入库/处置是对他人会话产物的裁决**，且它一旦入库就进入 S5/S16 的受控面（`reports/` 里的 `.py` 需靠豁免条目放行），归属该由 DEU 那条工作流的主人定 |

### 10.7 第三份根 skills 镜像（第 3 次复发）——两条旧猜测被证伪

仓库根第 3 次长出整棵 skills 树（51 个顶层条目 / 457 件），按已入闸的 SOP 处置：`diff -rq` 复核 ⇒ 零分叉 ⇒
**整树 `mv` 至 `attic/root_skills_mirror3_20261014/`（不删）**。过程里把上一轮写在 AGENTS.md 的两条猜测都推翻了：

- ❌「源树 = 某个安装位」→ ✅ **源树就是仓库 `Claude/skills/`**：与 7 个安装位逐位 `diff` 得 0/121/107/44/44/112/138 行差异，与仓库副本 0 行。
- ❌「`cp -r` 或 ZIP 导出」→ ✅ 同名件 mtime 与源树**逐纳秒相同** = `copy2`/`copytree`（ZIP 不可能：DOS 时间戳只有 2 秒分辨率），而 `tools/` 与 `src/` 里 `copytree` 零命中；且镜像里**缺 3 个被 gitignore 的件** ⇒ 不是 `cp -r` 而是 gitignore-aware 的写入方。
- 我们自己的两条写入通道都已带机制拒绝并经实测复现（`sync_skills._is_repo_root_or_ancestor()`、`pull_skills.is_repo_root_dest()`），第三条候选 `cnhkmcp` 已排除（见 §10.6）。

⇒ **结论按可执行的那一面写**：闸追不到「谁写的」，但 S17 追得到「写了没有」——复发即 pre-commit 阻断。
这条已写进 AGENTS.md §3.5 与镜像归档 README；旧写法（凭猜的两句）已在两处一并更正。

### 10.8 目标架构（§3）达成度对照

| §3 目标 | 状态 |
|---|---|
| 仓库根只有声明过的目录与白名单文件 | ✅ S17 + S7；根 skills 树 0。磁盘 22 个目录 = 闸的**声明面 16** 全部已声明 + 机器自生成 `__pycache__` 1 个跳过 + 点开头目录 5 个按规放行（写「17 个」会把跳过项算进声明面，与 `--only s17` 读数打架） |
| `tools/` 顶层只减不增、每件事有主题归属、数据件有归属 | ✅ S11（153 个 `.py` 冻结基线 + 3 个非脚本件全在允许清单） |
| `docs/` = 长期规范/SOP，日期报告外迁 | ✅ 批次E + S16 规则⑥（docs 面入闸） |
| 报告/产物命名四条 | ✅ S16①–⑤，存量 40 件基线只减 |
| `reports/` 子目录风格统一 | ✅ 批次G：新建即守 + 存量 4 条带代价登记 |
| `tracking/` 入库面不含运行期产物 | ✅ S18（索引面 FAIL，不进基线） |
| 索引不挂幽灵路径 | ✅ S20（实测 `git ls-files --deleted` = 0） |
| 全仓跟踪件必须有扩展名（§6 规则⑤） | ✅ **批次I = S21**：跟踪面 4107 件，无扩展名 4 件全在白名单 ⇒ 违规 0、**不建基线**；此前只有 S11 管 `tools/` 顶层 |
| `tracking/mining` 数据湖有索引 | ⏳ 需用户点头（S19 + 刷新责任） |
| `src/wqb` 散模块收纳 | ⏳ 需用户点头 |

### 10.9 收尾验证（批次A–G 那一轮的最后一次，全部实跑；批次H 的读数见 §10.10.5，最终读数见 §10.10.8）

| 检查 | 读数 |
|---|---|
| `pytest tests/ -q` | **7 failed / 3240 passed / 22 skipped（203 s）**；其中 `test_sync_skills_reports_no_drift` 跑一次 `sync_skills.py`（同步 5 个文件 × 6 位）后**当场转绿**（复测 50 passed），其余 **6 条与 §9.3 逐条取证的那 6 条完全同一**（裸 `sqlite3.connect`／GBR 加权腿反例／superalpha 基线／`WQ_MCP_LOOP` 未登记／语料直读真库／6 个孤儿分支文件），**没有一条落在我改的文件上**，也不由我代做（§7 不代并行会话裁决在途件） |
| `audit_structure.py` | **FAIL=0** WARN=4（S1 存量 `sys.path`、S6 4 组跨 skill 复制、S16 40 件存量基线 + 2 件在途命名） |
| `--only s16` / `--only s11` / `--only s18` | FAIL=0 WARN=2 ／ FAIL=0（非脚本件 3 个全在允许清单） ／ FAIL=0 WARN=0 |
| `doc_path_refs.py` | ✅ **无新增死指针**（BROKEN 1 = 基线 1：`.clinerules/skills`，2026-10-06 逐条复核为「有意缺席」），受控活文档 **375** 份（清理临时脚本后复测；早前写的 379 未逐件追因——本闸的受控面比 `docs/**.md + Claude/skills/**.md + 4 个 README` 的朴素 glob 窄，口径只认工具自己的读数）；4 条 UNTRACK 提示不阻断 = 本轮 3 个新守护测试（`s11_moved`/`s16_dir_style`/`s18_runtime_purity`，**须与 AGENTS.md 引用同批提交**）+ 并行会话的 `output_report/GBR_field_profile_cds_20261013.md` |
| `sync_skills.py --check` | **全部安装位与仓库一致**（6 位）。中途出现过 1 条 STALE（他人今日新增 `wq-brain-ra-gbr/references/combo-candidate-inventory.md`），按 §8.12 跑一次 `sync_skills.py`（5 个文件 × 6 位）自愈 |
| `audit_destructive_default.py` | 扫 455 个 `.py`，基线 0 条，**无新增高危** |
| `audit_node_registration.py` | 五处一致，**无漂移**（20 = 20 = 20 = 20 = 20） |
| `repo_governance_check.py`（硬判，不带 `--warn`） | **exit 1**：未跟踪源码 **75** 件（并行会话存量）；钩子里它是告警位，**不阻断** |
| S16 规则⑦ 非空过核验 | 两处变异都被抓：`< 3`→`< 2` 使取面重新混入顶层 `.md`；FAIL→WARN 使新建 snake 目录失去阻断 |

**同族数字（供下次复核口径）**：S13 磁盘非区域目录 6 个 vs 登记 7 项（差的 `PPA_USA` 走
`NON_REGION_DIRS_ALLOW_ABSENT` 静音）；根镜像三份归档件数 455 / 457 / 457。

### 10.10 批次H：门面的闸守住了，直写路径没有（2026-10-14 深夜起，10-15 凌晨收到第三条）

这一批不属于 §3 目标架构，是 §8.4 第 9/11 项那条台账的收尾 —— 由本批次那轮全量回归**当场抓到**，
所以按 §4 第 7 条（同一类失效第二次出现就机械拦住）推进。

存量清单的复现口径直接给在这里（`logs/_tmp_*.py` 会被 `tools/retention.py` 收掉，不能当证据载体）：

```sql
-- 只读：sqlite3 "file:data/wqb.db?mode=ro"
SELECT region, key, updated_at, count(*) OVER () AS total
FROM ledger_kv
WHERE lower(key) LIKE '%wiso%' OR lower(key) LIKE '%covtest%' OR lower(key) LIKE '%wtest%'
   OR lower(key) LIKE '%wsemtest%' OR lower(key) LIKE '%selftest%' OR lower(key) LIKE '%pytest%'
   OR key LIKE '%0123456789%' OR key LIKE '%\_test' ESCAPE '\'
ORDER BY updated_at;
```

#### 10.10.1 一手证据（不是推断，是库里的一行）

`tests/unit/04_gates/test_inspect_mode_failclosed_p1p1.py` 用 subprocess 起 `tools/wave_gate.py`，
子进程拿的是 CLI 缺省库位 = **生产 `data/wqb.db`**，实测写入：

```
region=KOR  key=gate_ws2_pytest_inspect_model109  updated_at=2026-10-14T23:27:21
```

同分钟共写 **1** 行 —— 即这一笔是纯测试写入，与真实批次无关。该类不是第一次：库里同期还躺着
§8.4 第 9 项记的 2026-10-04 一批，以及更早的 09-28 / 09-29 / 10-03 三批（全量清单见 §10.10.4）。

#### 10.10.2 为什么门面那份闸管不到这条路径

`wqb_db_mcp._reject_production_db_under_tests()` 挂在门面的 `get_db_path()` 上，而
`tools/` 与 toolkit 的直写路径走 `wqb.store.CampaignStore` —— **一行都不经门面**
（`CampaignStore.__init__` 自己 `Path(self.path).parent.mkdir()` + `db_connect(self.path)`）。
所以 10-04 把门面守住之后，同一类失效照旧发生。这就是 §8.4 第 9 项那条铁律的第二个方向：
**闸加在哪个入口，等价于只守那个入口**。

闸放在**构造连接**时而不是 `commit()` 时，理由也是实测的：`connect()` 里的
`PRAGMA journal_mode=WAL` 是**持久化的库级属性**，`ensure_schema()` 会 `CREATE TABLE`
—— 门店一开就已经改了库文件字节，等 commit 才拦，隔离失效已经落了地。

#### 10.10.3 修法：判定本体上移到唯一连接工厂

| 位置 | 改动 |
|---|---|
| `src/wqb/db_conn.py` | **新增判定本体** `production_db_path()`（从本文件 `__file__` 向上探测 `pyproject.toml` + `src/wqb` 双标记推仓库根，§8.13 层数无关口径）与 `reject_production_db_under_tests(path, *, entry)` |
| `src/wqb/store/campaign.py` | `__init__` 里 `mkdir` 之前调一次，`entry="CampaignStore"` |
| `wqb_db_mcp.py` | 原函数**保留同名**（`tools/code-audit/db_mcp_split.py` 的 `SKIP_FUNC` 认这个名字），函数体改为委托同一实现，`entry="wqb-db 门面"` |
| 测试侧 | `_run_wave_gate` 用 `env={**os.environ, "WQB_DB_PATH": str(tmp / "wqb.db")}` 注入临时库 —— `PYTEST_CURRENT_TEST` 会被子进程继承，所以这条路径从「闸看不见」变成「闸能看见」 |

放行口径四条，两边**完全一致**（同一套语义才不会出现「门面拦、store 放」）：
不在 pytest 下 ⇒ 不管（生产服务/CLI 正常写库是设计内行为）；`WQB_ALLOW_REAL_DB=1` ⇒ 放行；
其余走 `WQB_DB_PATH` 或显式传临时库路径。`docs/env_registry.json` 该条文案已同步指向新的判定本体。

守卫 = `tests/unit/01_store_db/test_db_write_guards.py::TestProductionDbGuardUnderTests` 7 例
（写本课时是 6 例，第三条路径抓出来后补到 7 例，见 §10.10.7），
其中两例专门反「以后又各写一套判据」：
`test_facade_and_store_share_one_implementation` 扫门面 + `src`/`tools`/三个 toolkit 目录，
断言 `reject_production_db_under_tests` 的**定义**只落在 `src/wqb/db_conn.py` 一处；
`test_tmp_db_still_constructs_under_pytest` 用 `tmp_path/ws/data/wqb.db` 这个**恰好以
`/data/wqb.db` 结尾**的形状做正反对照（§10.10.6）。

#### 10.10.4 存量清单：`ledger_kv` 里可机械识别的 24 行测试形态件（23 个键名）——**下限，且一律未动**

库的总行数 6117、`DISTINCT key` 4787 —— ⚠ `ledger_kv` 的主键是 `id`，唯一性在
**(region, key)**，所以「按键名数」会少数：`forum_recon_negative_0123456789` 就有
`GLOBAL` 与 `KOR` 两行。下面的计数是**行**级。三条判据取并集，判据名随表给出：

| 判据 | 行数 | 键名形状 | 同分钟共写 | 能否单独摘除 |
|---|---|---|---|---|
| **F1** 键名含测试夹具指纹（`wiso`/`covtest`/`wtest`/`wsemtest`/`selftest`/`pytest`） | 16 | `ckpt_wisotest1-3`、`gate_wisotest1-3_intraday_pv_feats`（09-28）· `wave_meta_covtest`/`covtest3` + `diversity_report_wcovtest*`（09-29）· `gate_wsemselftest_fundamental17`、`gate_wsemtest_filter_fundamental17`、`gate_wtest_g9_{clean,mix,real}_model109`（10-03）· `gate_ws2_pytest_inspect_model109`（10-14 本次） | 123 / 403 / 708 / **1** | 只有 10-14 那 1 行所在窗口是纯测试窗口；前三批与真实写入**混在同一分钟** |
| **F2** 键名内嵌假 alpha id `0123456789` | 4 | `forum_recon_0123456789`、`forum_recon_error_0123456789`、`forum_recon_negative_0123456789` ×2（GLOBAL/KOR） | **4** | 可判定为测试写入（§8.4 第 9 项那批）|
| **F3** 只以 `_test` 结尾、不落 F1 | 4 | `judge_test`（09-02）· `review_os_decay_test`（10-01，同分钟共写 854）· `s6_verdict_campaign_20260922_zero_competition_test`（10-02，共写 1064）· `review_os_failopen_test`（10-03，共写 708） | 1 / 854 / 1064 / 708 | **不能**：可能是人名里的 `_test`，也可能是真实结论 |

⇒ **为什么这批不清**（两条，都必须写出来而不是省略成「待清理」）：
① 删 `ledger_kv` 行是**对生产库的写操作**，属须用户点头的动作（AGENTS.md §7 红线之外的一般写纪律）；
② 更要紧的是**这 24 行只是下限，且切不开**：
- 2026-10-04T03:00–03:41 那个窗口实测 **17 行**，其中只有 4 行（F2 的 `forum_recon_*_0123456789`）带指纹；
  其余 `KOR/gate_ws2_oth466_d33_other466`、`KOR/ckpt_ws2_oth466_d33`、`KOR/ckpt_ws2_oth466_d34`、
  `KOR/gate_cache_risk71`、`KOR/gate_ws2_risk71_d32_risk71`… 与真实波次**命名同形、不含任何夹具指纹**，
  机械判据抓不到（同窗还躺着一行 `WORKFLOW/judge_MP3XxlPn`，是真实 alpha id ⇒ 这个窗本来就混着真实写入）。
- 按时间窗反查也不可靠：§8.4 第 9 项当年记该窗 `ledger_kv` **5 行**，今天按
  `updated_at LIKE '2026-10-04T03:33%'` 复测只 **4 行** —— 少的那行是 `updated_at` 被后续写入覆盖了。
- F1 前三批所在分钟共写 123/403/708 行，F3 三条共写 854/1064/708 行：同批件里既有测试写入也有真实波次结论。

逐条判据（哪几行能安全摘）留给用户或该数据的主人裁；本批次只负责**止住复发**。

#### 10.10.5 本批验证读数（全部实跑）

| 检查 | 读数 |
|---|---|
| 修复前后全量对照 | 错判据那轮 **11 failed / 3209 passed / 27 errors（171 s）** → 判据改对后 **7 failed / 3246 passed / 22 skipped（180 s）** ⇒ **27 个 ERROR 全清**，多出的 6 个 passed 是新增的守卫用例 |
| `index_tables.py env --apply` 后复测 | `test_embedded_blocks_match_the_generators` **转绿**（本轮新增 `src/wqb/db_conn.py` 读取点后，嵌入表与生成结果本就不一致 —— 按 §8.10 走重生成，不手改 `docs/env_and_switches.md`）⇒ 剩 **6 failed**，与 §9.3/§10.9 逐条取证的那 6 条**完全同一**，无一落在本批改的文件上 |
| 定向复测（`04_gates` + `01_store_db` + `06_wave_pipeline` 相关件） | **108 passed**，唯一红的是 §9.3 那条并行会话的裸 `sqlite3.connect` |
| 生产库探针（只读，`file:data/wqb.db?mode=ro`） | 闸生效后**没有新的测试写入**：`ledger_kv` 里 `updated_at` 晚于 2026-10-14T23:27:21 的测试形态件 = 0；§10.10 内联 SQL 复跑得 24 行 / 23 键名，与建闸前同数（即本批只读、未动库） |
| 守卫非空过 | 6 例覆盖：store 拒生产库 / 门面与 store 单一实现 / 临时库照常可建（正反对照）/ 放行须显式声明 / 非 pytest 下不管 / Windows 两种路径写法都拦住 —— 这 6 例是**抓到第三条路径之前**的读数，第 7 例（toolkit 委托）见 §10.10.7 |
| 定向复测（`test_db_write_guards` + `test_index_tables` + `test_inspect_mode_failclosed_p1p1` + `test_docs_consistency`） | **480 passed / 2 failed**，两条红 = §9.3 已取证的并行会话件（裸 `sqlite3.connect` ×8 在 `tools/fields/skeleton_panel.py`+`tools/gates/operator_coverage_audit.py`；`WQ_MCP_LOOP` 未登记来自 `main.py`/`wqb_db_mcp.py` 的未提交改动），**本批 6 例守卫全绿**（补第 7 例后复测 20 passed / 1 failed，同一条红） |
| `audit_structure.py`（本批后） | **FAIL=0** WARN=5（比 §10.9 多的那 1 条 = 并行会话新在途件 `docs/reference/KOR_analyst_field_profiling.md` 的 S16 命名提示，不阻断） |
| `doc_path_refs.py` | 活文档 **375** 篇 / 候选引用 506 条 / BROKEN 1 = 基线 1 ⇒ **无新增死指针**。⚠ 本批一度把复现口径写成「探针脚本在 `logs/_tmp_h_ledger_probe*.py`」—— 那些件会被 `tools/retention.py` 收掉，**不能当证据载体**，已改成把只读 SQL 直接内联在 §10.10 上方，并用该 SQL 复跑确认 `count(*)=24 / count(DISTINCT key)=23` |

#### 10.10.6 一条新的失效形态：**判据形状错误 —— 用后缀匹配代替「同一个文件」的身份比较**

§10.3 记的是「按扩展名取面的闸看不见目录」，这条不是同一族，别再混着引：
**取面对了，判据形状错**。第一版把「是不是生产库」写成 `path.endswith("/data/wqb.db")`，
于是**正确隔离**的 `tmp_path/ws/data/wqb.db` fixture 被判成生产库 —— 一轮回归 **27 个 ERROR**，
全是本来就写临时库的正常用例。修法 = `normcase(realpath())` 与 `production_db_path()` 做
**身份相等**比较，而不是形状后缀。

⇒ 可执行的自检一句：**写「是不是 X」的判据时，先问 X 的唯一身份是什么。**
路径类判据几乎总是身份问题（同一个 inode/文件），不是字符串形状问题；
用后缀/前缀匹配的判据，必然在同一命名惯例下产生假阳性 —— 而它的报错长得像「闸在工作」，
所以比假阴性更难发现（这次是靠 27 个 ERROR 的数量异常才发现的）。
这条已写进 `db_conn.reject_production_db_under_tests()` 的 docstring 与 AGENTS.md §8.4 第 11 项。

#### 10.10.7 收工时又抓到**第三条路径**（2026-10-15 凌晨，同一批的延续）

写完 §10.10.3 后自查「闸加在哪个入口 = 只守那个入口」这条推论还没走完：把
`DIRECT_CONNECT_WHITELIST` 七个白名单件逐个过了一遍，发现 toolkit 侧还有独立取连接路径 ——
`Claude/skills/wq-brain-campaign-toolkit/scripts/_lib/db.py`（为「技能装在仓库外也能跑」
而落地的同构工厂，模块 docstring 自己就写着「与 `src/wqb/db_conn.py` 同口径」）。
它下面挂的 `_lib/ledger.py` / `_lib/registry.py` / `_lib/wave_results.py` / `_lib/region_gates.py`
**全部经这个 `connect()` 取连接，且都被 `tests/` 直接驱动**（命中测试文件数 9/7/6/4）。
⇒ 库里 2026-09-29 那批 `wave_meta_covtest*` / `diversity_report_wcovtest*` 的来源就是这条，
不是 store 那条。

**修法不是再复制一份判据**（那正好违反本批刚写的 `test_facade_and_store_share_one_implementation`），
而是 `connect()` **委托** `wqb.db_conn` 的判定本体：`wqb` 导入失败只发生在「技能装在仓库外」，
那种场景服务真实战役运行而不是 pytest，放行属设计内。守卫新增一例
`test_toolkit_lib_db_delegates_to_core_guard`：先断言 `mod.default_db_path()` 解析出来
**就是生产库**（这正是静默写库的形状），再断 `connect()` 抛「隔离未生效」、传临时库照常可建。

其余三个白名单件（GEM `headless_runner/run.py`、`trailSomeAlphas/run_pipeline.py`、
`feature_engineering.py`）实测连接点附近**无 `INSERT` / `UPDATE` / `commit` / `CREATE TABLE`**
⇒ 只读取数，不逐个加闸；把「白名单 + 只读」作为判据形态，而不是拿复制粘贴守卫凑全覆盖率。

验证（本小节全部实跑）：`test_db_write_guards.py` **20 passed / 1 failed**（红的仍是他人的裸
`sqlite3.connect`）；`10_toolkit_scripts` + `01_store_db` + `06_wave_pipeline` 三组
**745 passed / 1 failed / 5 skipped（80 s）** ⇒ 新闸**没有打断任何既有测试**（这些用例本来就走
显式临时库或 `WQB_DB_PATH`，所以闸一挂上全都绿——这同时说明此前那批污染件来自**没设 env 的旧用例**，
不是这批测试）。`_lib/db.py` 已按 §8.12 跑 `tools/sync_skills.py` 同步到 6 个安装位。

#### 10.10.8 批次H 收尾核验（三条路径全部入闸后的最终读数，2026-10-15 00:04–00:09 实跑）

| 检查 | 读数 |
|---|---|
| 全量回归 `pytest tests/ -q`（含第 7 例守卫） | **6 failed / 3248 passed / 22 skipped（202 s）**。与 §10.9 的 7 failed 相比少的那条是 `test_sync_skills_reports_no_drift` —— 本批改了 toolkit `_lib/db.py` 并跑过 `sync_skills.py`，它本就该绿。剩下的 **6 条与 §9.3 逐条取证的那 6 条完全同一**（裸 `sqlite3.connect` / sf_sweeps 加权腿反例 / skill_lint 基线 / `WQ_MCP_LOOP` 未登记 / op_arity 语料直读真库 / profiles_layer 孤儿分支文件），**没有一条落在本批改的文件上** |
| 生产库「今日零写入」核验（只读 `file:…?mode=ro`） | 跨零点跑完整套回归后，`ledger_kv` 里 `updated_at >= 2026-10-15` 的行数 = **0**，全表 `MAX(updated_at)` 仍是建闸前那条一手证据 `2026-10-14T23:27:21`。同口径顺带核了 5 张写面：`wave_results` 0（MAX 2026-10-05T18:15:31）、`registry_empirical` 0（MAX 2026-10-14T16:36:23）、`backtest_results` 0（MAX 2026-10-14T16:05:35）、`expressions` 0（MAX 同 23:27:21）、`alphas` 0（MAX 2026-10-14T19:56:06） |
| 端到端非空过（专门跑曾污染的那条通道） | 单独跑 `tests/unit/04_gates/test_inspect_mode_failclosed_p1p1.py` → **8 passed**（其中 2 例**真的**起 `tools/wave_gate.py` 子进程，前置夹具满足、未 skip）。跑前/跑后用**比 §10.10.4 更宽**的探测面 `key LIKE '%pytest%' OR '%_test%' OR '%test_%' OR '%0123456789%'` 计数：两次都是 **29 行 / 29 个 (region, key)**、`MAX(updated_at)` 逐字不变 ⇒ 这条通道现在要么写临时库、要么响亮报错，**不再静默写生产**。（29 与 §10.10.4 的 24 不是同一口径：这里用宽谓词只为**抓变化**，且按 (region,key) 去重；§10.10.4 那 24 行是三条具名判据的并集、按键名去重） |

⚠ 有一项**想做而没做成**：本想手工起一次不带 `WQB_DB_PATH` 的 `wave_gate.py` 子进程，
直接看它报错而不是写库，用来证明「CLI 直写」这条通道在真实调用下也被拦。权限层按
「潜在生产库写操作」拒绝执行该命令，因此改为依赖上面两行等价证据：单元守卫
`test_store_rejects_production_db_under_pytest` 覆盖判定本体，端到端 8 passed +
计数不变覆盖子进程通道。若要补这一步，需用户在非 pytest 环境下自行执行。

### 10.11 批次I：§6 规则⑤ 机械化 = S21 跟踪件扩展名（2026-10-15 凌晨）

**为什么这一批做它**：§6 九条命名口径里，规则⑤「文件必须有扩展名」是**唯一一条只在局部机械化**的——
S11 只在 `tools/` 顶层校它，S16/S18 的取面又先按 `S16_SUFFIXES` 筛扩展名。
§10.3 那条同族发现（「按扩展名取面的闸结构性失明」）在这里的体现是：三条闸合起来，
对**仓库其余位置的无扩展名件**完全失明，而规则⑤的活样本 `tools/mcp_py` 恰恰就是这个形态
（它带着 `D:\...` 绝对路径和已退役端点在顶层躺了很久，S4 盘符扫描按 `*.py` 取面 ⇒ 一行不报）。

**取面与判据（三条都是落地时定下来的，不是初稿）**

| 口径 | 取法 | 为什么 |
|---|---|---|
| 取面 | `git ls-files -z`，**不带 pathspec** | 本闸要的是「整条索引面」。带 pathspec 就退回 S11 的局部失明。守护用 `test_s21_face_is_the_whole_index_not_a_pathspec` 断言命令**逐字**是 `["git","ls-files","-z"]` —— 这类「取面参数」写错时读数照样是绿的，只能这样钉住 |
| 判据 | 基名不含 `.` ⇒ FAIL（`"." not in name`） | 见下面第一条被纠正的口径 |
| 拦截时机 | 索引面 ⇒ `git add` 之后、建提交对象之前即拦 | 与 S20 那条教训同一机制（pre-commit 跑在 commit 前，已暂存新件已在 `ls-files` 面内）。**未跟踪件不受本闸管**：实测未跟踪 80 件、0 违规；不校它们是为了不把并行会话的在途草稿判红（S16 有未跟踪 WARN 预检，本闸刻意不做——无扩展名草稿 `logs/_tmp_x` 是 §8.13 允许的一次性形态） |

**落地时被自己的写法纠正的两处**（§8.5 那条纪律的又一次应用：判据必须**既拦得住事故、又不拦工具约定的既有形态**）

1. **`Path(p).suffix == ""` 是错的判据。** 直觉写法第一版就是这么写的，实测会把 `.gitignore`、
   `.mcp.json`、`.env.example`、`docs/.keep` 每一个点开头文件判成违规 —— 与 S17 首跑被根
   `__pycache__` 误红（§7.1）完全同族。改成「基名不含 `.`」后，点开头文件因为名字里**本来就带点**
   而自然通过，不需要任何豁免条目。
   ⚠ 这条纠正顺带挖出一处**死分支**：第一版除了 `suffix` 判据还写了 `if name.startswith("."): continue`。
   守卫里做变异反查时（把那两行的 `continue` 改成不 continue）读数**仍然是绿的** ⇒ 该分支永不可达，
   因为它想救的件已经被外层判据放过了。删掉，并加一条**反向断言**防止它被「顺手补个豁免」写回来：
   `assert 'if name.startswith("."):' not in src.split("def check_s21_files_have_extension")[1]`。
   **教训：变异测试不只是证「判据承重」，也会证「某行不承重」——不承重的判据行是下一轮读代码时的误导源。**
2. **两类豁免伞不可互换。** `S21_EXEMPT_NAMES`（`Makefile`/`Dockerfile`/`Containerfile`/`LICENSE`/
   `LICENCE`/`NOTICE`/`Vagrantfile`/`Procfile`）按**名字**豁免、任何位置生效——这些件由工具按全名识别，
   加扩展名等于让它们认不出来。`S21_EXEMPT_PATHS`（`tools/git-hooks/pre-commit`、
   `tools/git-hooks/commit-msg`）按**完整路径**豁免——git 硬要求 hook 无名可改。
   把 hook 名塞进名字型伞，`任意目录/pre-commit` 会一起获得豁免 ⇒ 守卫
   `test_s21_exemption_kinds_are_not_interchangeable` 同时断 `'pre-commit' not in S21_EXEMPT_NAMES`
   与「`scripts/pre-commit` 必须 FAIL」。
   路径型条目对应的件从面里消失 ⇒ **WARN 催删条目**（同 S13/S11/S16 那个坑：留着失效条目就是一条永久豁免通道）。

**读数（全部实跑，2026-10-15）**

| 检查 | 读数 |
|---|---|
| `audit_structure.py --only s21` | `[OK] S21 跟踪件扩展名: 跟踪面 4107 件，无扩展名件全部落在白名单内（名字豁免命中 ['Dockerfile', 'Makefile']；路径豁免命中 ['tools/git-hooks/commit-msg', 'tools/git-hooks/pre-commit']）` |
| 独立复算（不走被测代码，直接 `git ls-files -z` + `git status --porcelain -uall`） | 跟踪面 **4107 件**、基名不含 `.` 的 **4 件** = `tools/git-hooks/{pre-commit,commit-msg}` + `world-quant-brain-mcp/{Dockerfile,Makefile}`，与闸的白名单命中集**逐一相同** ⇒ 违规 0；未跟踪 **80 件 / 0 违规** |
| 是否建基线 | **不建**。实测违规 0 ⇒ 空债面上放一个基线键，等于给「以后往里塞豁免」留永久通道（同 S16 的 `docs/` 面无基线取舍，§8.12 已记） |
| 守卫 `tests/unit/07_docs_skills/test_audit_structure_s21_extension.py` | **11 passed（0.22 s）**：注册反查 · 取面不带 pathspec · dotfile 与白名单放过 · 事故形态可红且报错给得出「改名并同步引用，不是删除」 · 两类伞不可互换 · 伞失效 WARN · 两条 fail-closed（`git` 失败 / 空集） · 真实面非空过（面 ≥3000 且独立复算 offender 集 == 白名单四件） · 白名单路径件必须在盘上 · `suffix` 判据的变异反查 |
| 变异件残留 | 变异用例把 mutant 写在 `logs/_tmp_s21_mutant_audit_structure.py`（§8.13 规定的一次性草稿位、gitignored、且不在 `test_db_write_guards` 的 SCAN_ROOTS 内），`finally` 里 unlink ⇒ 复跑后 `ls logs/_tmp_s21*` = **0 件**。（初版把 mutant 放 `tmp_path` 直接 `RuntimeError: 仓库根未找到` —— `audit_structure` 的模块级 `_bootstrap_src()` 向上找 `pyproject.toml + src/wqb` 双标记，**仓库外的件 exec 不了**；这是「变异件必须落在仓库内」的一条通用坑，记下来省下一轮） |

**治理文档同步四处**：AGENTS.md §8.12（S 清单加 S21、FAIL 阻断集加 S21、新增专门说明块含 `suffix` 坑）、
§8.13 命名规范（把规则⑤从「报告 §6 的建议」升为正文条目，写明两类豁免与点开头文件判据）、
§4 钩子口径 `S1–S20` → `S1–S21`、`tools/git-hooks/pre-commit` 头注同步（并顺手注明 **S19 尚未落地**，
避免「S1–S21」被读成每条都存在）。本批未动任何 skill 文件 ⇒ 不需要 `sync_skills.py`。

### 10.11.1 批次I 收尾验证（全部实跑，2026-10-15 00:40–00:52）

| 检查 | 读数 |
|---|---|
| `audit_structure.py` 全套 | **FAIL=0 WARN=5**（00:40 读数；同 §10.9 / §10.10.8，本闸未新增任何一条。**00:48:51 起被外部事件改写 ⇒ FAIL=1 / WARN=7，见 §10.12**） |
| `doc_path_refs.py` | **exit 0，✅ 无新增死指针**；`[UNTRACK] 5` 条 = 本轮与前几轮的守卫测试文件尚未入库（`s11_moved` / `s16_dir_style` / `s18_runtime_purity` / `s21_extension`）+ 并行会话的 `output_report/GBR_field_profile_cds_20261013.md`。**这些是「提交时要一起 `git add`」的清单，不是缺陷** |
| 目标组 `pytest tests/unit/07_docs_skills/ -q` | **1089 passed / 2 failed / 2 skipped（80 s）** |
| 全量 `pytest tests/ -q` | **7 failed / 3259 passed / 22 skipped（212 s）**。passed 从 §10.10.8 的 3248 涨到 3259 = **+11，与本批新增守卫用例数逐一对上** ⇒ 新用例确实在收集面内且全绿 |
| ⚠ 本表读数的**时效** | 这套「FAIL=0 / WARN=5」是 **00:40 的真实读数**，收口取证（00:52–01:01）时同一命令已变成 **FAIL=1 / WARN=7** —— 变的不是本批代码，是**工作树在 00:48:51 被另一会话删掉 44 个跟踪件**。见 §10.12，读数按时刻分列，不做「更正」抹平 |
| 失败归属 | 6 条与 §10.10.8 完全同一（裸 `sqlite3.connect` / sf_sweeps 加权腿 / skill_lint 基线 / `WQ_MCP_LOOP` 未登记 / op_arity 语料直读真库 / profiles_layer 孤儿分支），**没有一条落在本批改的文件上**。第 7 条 = `test_sync_skills_reports_no_drift`：漂移件是并行会话正在写的 `Claude/skills/wq-brain-ra-eur/references/_combo-candidate-inventory.md`（仓库 mtime `00:41:12` / 12540 B vs 安装位 `00:30:49` / 9800 B，六个安装位同一件陈旧）。本批未动任何 skill ⇒ **不代其同步**（§8.4 第 10 条「并行会话的在途工作不要跨会话代管」；他们 `sync_skills.py` 一次即自愈）。⚠ 提交时要过钩子第 ⑥ 步，必须先有人跑那一次同步 |

⚠ **同步治理文档时自己被棘轮逮到一次**（值得记，这正是 `doc_path_refs` 该有的行为）：
新写的两处 AGENTS.md 正文用了完整旧路径 `tools/mcp_py` ⇒ **新增 BROKEN 1 条、exit≠0**（该件已改名，
字面路径不可达）。改为与既有写法一致的「旧名 `mcp_py`」后 `[doc_path_refs] ✅ 无新增死指针（BROKEN 1 = 基线 1）`。
**口径：正文引用已下架路径时写「旧名 X」，不要写完整旧路径。**

⚠ **§6 剩下的未机械化项**（别把本批读成「九条全有闸了」）：规则①目录 kebab 只在 `reports/`+`output_report/`
一层子目录与顶层目录上有闸（S16⑦ / S17），**任意深度**的目录名没有面；规则②「文件纯 snake_case」
只有 `docs/` 面校到「不含大写字母」这一半（S16⑥），**下划线/驼峰混用没有判据**，「活探针禁止 `test_` 前缀」
仍只有文档 + 个案处置；规则④非 ASCII 只在**报告类扩展名面**上有效（见 §6 第 4 条注）；
规则⑨靠 `_refs` 语义登记而非闸。这几条目前没有活样本，按 §4 第 7 条「同类漂移第二次才机械化」处理，不预先建闸。

---

### 10.12 交付后取证：00:48:51 工作树掉出 44 个 `tools/*.py` 跟踪件（S20 上线当天就逮到一次真人事故）

**一句话**：批次I 收口复跑时全套读数从 00:40 的 `FAIL=0 / WARN=5` 变成 **`FAIL=1 / WARN=7`**，
唯一 FAIL 是 **S20 索引↔工作树一致：44 个文件在索引里但工作树已不存在（删除未暂存）**，
44 件**全部**在 `tools/` 顶层。这条不是本批引入的回归，也不是 §2 那条老 P0 复发——
是**另一个会话在 00:48:51 的一次未暂存删除**。S20 从落地到抓到一次真实事件，隔了不到 24 小时。
**处置权在写入方**：本节只出证据、影响面与两条互斥选项，不代其恢复、也不代其把删除暂存（§8.4 第 10 条）。

**取证时间线（读数按时刻分列，不抹平）**

| 时刻 | 读数 / 证据 |
|---|---|
| 00:26 / 00:31 / 00:39 | 本批写 `audit_structure.py`（S21）、`pre-commit` 头注、`AGENTS.md` —— 三者都不删件 |
| **00:40** | `audit_structure.py` 全套 **FAIL=0 / WARN=5**，S20 `[OK] 索引无未暂存删除`（§10.11.1 表） |
| **00:48:51** | `tools/` **目录** mtime（§8.5：目录项增删才改目录 mtime，文件 mtime 看不出删除） |
| 00:52 | `reports/` 目录 mtime = 本报告最后一次编辑；`.git/index` mtime 仍是 **23:24:11** ⇒ 00:48 那批删除**一个都没进暂存面**，与 ` D`（45 项里 44 项在 tools/）自洽 |
| 00:53 → 00:56 → 00:59 | 顶层 `.py` 计数 **108 → 109**，`tools/super_build.py` 在 **00:56:04 被重新写回**；`tools/` 目录 mtime 同步推到 00:56:04 后不再动 |

**归属：排除了四种解释后才落到「并行会话的未暂存删除」**

| 候选解释 | 判据 | 结论 |
|---|---|---|
| 本批（批次I）删的 | S21 只读索引、守卫用例只 `unlink` 自己写在 `logs/` 的 mutant；本批 diff 面不含任何 `tools/*.py` 删除 | **排除** |
| 「按主题下沉」搬走了（`tools/` → `tools/<theme>/`） | 顶层 108 + 子目录 **57**（17 个主题目录逐个清点）= 165，**没有一个 44 件名单里的基名出现在 `tools/` 任何子目录**；`git status --porcelain -- tools` 里未跟踪件 **0**；`tools/THEMES.json` 的 diff 只登记 `db` 主题 2 件 + `mcp_http_caller` / `operator_coverage_audit` 两个名字，**没有任何一条把 44 件写进 `moved_files`** | **排除**：是删除，不是搬家 |
| 归档进 `attic/`（§7「归档而非删除」） | 44 个基名全仓 `find`（排除 `.git`）**零命中**；`attic/` 无今日新增子目录（最新仍是 `import_staging` 10-06） | **排除** |
| 被 `git stash` 收走 / 搬进另一份工作副本 | `git stash list` **空**；`D:\coding\traeCN_project\wqb-01\` 确实是第二份仓（HEAD `99d4044`，2026-09-20），里面有 20/44 件，但那是**它们被删除之前就已存在的老快照**，不是目的地 | **排除** |
| 并行会话未暂存删除 | 同期活动件在改：`logs/_kor_d271.txt` 00:45、`logs/_kor_d271_plan.json` 00:45、`data/wqb.db` 00:49、`output_report/SA_region_selection_analysis_20261014.md` 00:51、`.workbuddy/memory/2026-10-14.md` 00:52、`logs/_kor_d272.txt` 00:52；且 00:56 有一件被写回 | **成立**（唯一与全部观测自洽的解释） |

**为什么这 44 件不是「脏索引」而是「功能已断」**：44 件**全部**在活跃面里被按名引用
（扫 `AGENTS.md`/`CLAUDE.md`/`README.md`/`docs/`/`Claude/skills/`/`src/`/`tools/`/`tests/`/`world-quant-brain-mcp/`/`tracking/reference/` = 3587 个文件，
token 级基名匹配，**零引用的件 = 0**）。按引用数排前几位：
`wave_gate` 600、`submit_verdict` 473、`forum_recon` 251、`campaign_intel` 211、`mode_b_qualify` 130、`forum_recon_wave` 92、
`sa_probe` 50、`batch_status` 47、`sync_platform_alphas` 35、`batch_submit_verdict` 19。
其中 **14 件是 AGENTS.md 正文点名的**（§6 场景表指定工具 `batch_status` / `sa_probe` / `submit_verdict` / `super_build`〔已于 00:56 回来〕 / `wave_gate`，
§1 续跑硬编码引用 `backfill_longcount`，§8.11 `forum_recon*` / `step9_audit`，§8.6 收批链等）。直接后果三条：

1. **全仓提交被卡住**：pre-commit 第 ② 步 `audit_structure` FAIL 即阻断，S20 不进基线豁免（§8.12）。
   本批 §10.11.1 已登记的「过钩子第 ⑥ 步要先跑一次 `sync_skills.py`」现在前面还多了一道。
2. **S2→S3→S5 链路断**：`src/wqb/workflow/nodes/wave_gate.py` 是 subprocess 转发 `tools/wave_gate.py`（§8.1 分层图），
   目标件不在盘上 ⇒ `wave_gate` / `unified_gate` 节点必失败；`tools/wave_gate_pkg/`（13 个模块）还在，缺的只是入口 shim。
3. **§6 指定工具不可用**：一次性脚本又开始被重新造出来的条件正是这个（§6 开头的因果）。
4. **§1 声明的续跑断点链断一半**：`results/` 的 checkpoint 被 `backfill_longcount.py`、
   `batch_submit_verdict.py`、`prod_blocked_recheck.py` 硬编码引用，前两个**在这 44 件里**、第三个还在盘上。
   断点文件本身没动（`results/` gitignored、不受影响），但**读它们的人不在了**。

**可恢复性核验（只读，未动工作树）**：44/44 件在 `HEAD` 里都有 blob ——
`git cat-file -e HEAD:<路径>` 逐个真跑，**0 缺失**；合计 **612,960 字节 / 13,322 行**。
⚠ 这与 §7 红线说的「只以未跟踪形态存在的源码」**不是同一类**：那类删了救不回来，
跟踪件删除可以从 HEAD 无损取回。**但取回的前提是别把删除连同一次 `git add -A` 提交出去**——
提交后历史里仍有，代价从「一条 checkout」升到「翻历史 + 逐件比对」。

**01:01 采集的名单（44 件，全部 `tools/<名>.py`，基名）**

```
archive_submit_ready   atom_labeler           audit_dead_code      audit_file_sizes
backfill_2y_from_platform  backfill_longcount batch_status         batch_submit_verdict
build_field_index      campaign_intel         category_field_triage complexity_scan
concept_overlap        diag_forum_read        discover_datasets    dynamic_recipe_weighter
economic_mechanism_templates  fetch_dataset_assets  field_quality_scorer  field_quality_scorer_v2
field_semantic_classify  fix_wave_backfill    fix_wave_vectors     forum_recon
forum_recon_wave       gen_field_inspect_packs  market_regime_adapter  mode_b_qualify
modeb_improvement_pipeline  ppa_handoff       preflight_wave       prod_first_screen
quota_status           role_cluster           sa_probe             seed_region_priors
skeleton_origin_report step9_audit            step_event_log       submit_verdict
sync_platform_alphas   triage_prodcorr_batch  validate_fields_batch  wave_gate
```

**两条互斥处置（等用户拍板，本会话一条都没执行）**

| 选项 | 命令形态 | 适用前提 |
|---|---|---|
| A 取回（判定为误删） | 逐件、路径来自现场重采的清单：Git Bash 下 `git ls-files --deleted -- tools \| xargs -d '\n' -n 20 git checkout --`；PowerShell 下按 §5 第 1 条先写 `logs/_tmp_restore_tools.py`（读清单 → 逐件 `subprocess.run(["git","checkout","--",p])`），**不要用 `$(...)` 内联** | 该会话并没有打算删（例如搬移脚本只跑了删除半边） |
| B 暂存删除（判定为有意退役） | `git add -u -- tools/<旧路径>`（**逐个/白名单式**，配合 `docs/governance/snapshot_adjudication.md` 台账给每件写可复核依据） | 该会话在做退役/下架，且愿意为 44 件补齐 §7 的裁决依据 |

⚠ **两个必须避开的写法**：① **不要 `git checkout -- tools/`**（目录级 pathspec 会连带把并行会话
在 `tools/` 的 **18 个 ` M`** 一起回退，等于跨会话覆盖他人在途改动）；② **不要为了「让闸变绿」先 `git add -A`**
（§7 第 1 条；本仓禁止顺带把未跟踪件拖进暂存面，这里还叠加「删除半边」的风险）。

**为什么不能给一个「权威名单」收尾**：取证期间树在漂（00:56:04 一件被写回、顶层计数 108↔109），
`git ls-files --deleted` 与 `os.path.exists` 两条独立取面在 00:58 前后给出的**集合大小相同但成员会换**。
并发写入者拿不到原子快照 ⇒ 任何清单都要**在执行前重新采一次**，上面两条命令都写成「现场生成」的形式正是为此。
清单快照落在 `logs/_tools_ghost_20261015.txt`（01:01 采，44 行，gitignored，`retention.py` 的草稿件不在回收口径内）。

**S20 这一条的设计取舍事后被验证是对的**（也是本节存在的理由）：取面用 `git ls-files -z --deleted`
（索引 vs 工作树），**判据是「磁盘上没有」而不是「git status 里有没有红字」**——后者要人去看，
前者在 pre-commit 第 ② 步必红；刻意 `FAIL` 且**不进基线**（§8.12：幽灵路径当场暂存即清，没有合法存量形态）。
首跑当日的 §2 老 P0（`reports/…_refs/` 23 件）与本次 44 件是**同一形态换目录再现**，
按 §4 第 7 条「同类第二次即机械化」，这条闸已经在了，**不需要再加闸**，需要的是把裁决补上。


