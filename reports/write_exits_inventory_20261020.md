# 写文件出口全景表（2026-10-20）

对 `src/` + `tools/` + `Claude/skills/` + `world-quant-brain-mcp/` 全量 `.py` 静态扫描
（排除 `.venv/`/`site-packages/`/`attic/`/`tests/`），定位**全部 260 处写盘调用点**，
按**目标目录**归类。方法：AST 抓写盘调用（`write_text`/`write_bytes`/`open(...,'w'|'a'|'x')`/
`to_csv`/`to_excel`/`json.dump`），沿赋值图回溯 2 层解析目标路径，再对照 AGENTS.md §8.13 白名单分类。

审计闸：`tools/code-audit/audit_write_targets.py`（本轮新增，配 16 条测试）
棘轮基线：`tests/fixtures/write_targets_baseline.json`（当前空 = 零高危）
全仓扫描：**0 违规 / 0 新增违规 / 97 UNKNOWN**（解析不出路径的短变量名，抽查确认合规）

---

## 1. 出口总览

| 目标目录 | §8.13 归类 | 磁盘文件数 | 入库 | 真源写者 |
|---|---|---:|---|---:|
| `tracking/<REG>/` | 区域事实面 | **14,016** | ✅ | **37** |
| `output_report/` | 报告唯一出口 | 223 | ✅ | 12 |
| `attic/` | 归档面 | 812 | 部分（`.gitignore` 白名单外） | 10 |
| `reports/` | 人工审计/评审 | 142 | ✅ | 8 |
| `docs/` | 长期规范/SOP（需登记生成器） | 100 | ✅ | 15 |
| `cache/` | 断点缓存 | 1,800 | ❌ `.gitignore` | 31 |
| `logs/` | 日志 | 1,802 | ❌ `.gitignore` | 25 |
| `results/` | 续跑 checkpoint | 248 | ❌ `.gitignore` | 68 |
| `data/` | 运行期数据 | 10 | ❌ `.gitignore` | 89 |
| TEMP（`tmp_path`/`mkdtemp`/`/tmp/`） | 测试临时件 | — | — | 若干 |

入库跟踪：`cache/` `logs/` `data/` `results/` 实测 `git ls-files` = **0**，`.gitignore` 全覆盖 ✅
代码目录里无产物入库：`git ls-files src tools | grep -vE '\.(py|md|json)$'` 只命中 `tools/git-hooks/*`（合法钩子）

---

## 2. 各出口的写者清单

### 2.1 `output_report/` — 报告唯一出口（12 个写者）

**规范**：`output_report/` 是 §8.13 明文的「战役/评审**产物**报告」唯一去处；由 workflow/战役自动产出或工具直写。

**主写者（工具类）**：
- `tools/complexity_scan.py` — 代码复杂度扫描报告
- `tools/audit_structure.py` — 目录结构审计报告
- `tools/os_report.py` — osmosis 分配报告
- `tools/run_grouped_tests.py` — 分组测试报告
- `tools/archive_submit_ready.py` — 提交就绪清单归档
- `tools/code-audit/doc_path_refs.py` — 文档路径引用检查
- `tools/code-audit/snapshot_adjudicate.py` — 快照裁决台账
- `tools/code-audit/audit_write_targets.py` — 本审计闸自身
- `tools/refs_scan.py` — 引用扫描

**Skill 侧写者**：
- `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/pipeline_reports.py` — GEM pipeline 报告
- `Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py` — GEM 主脚本

**库层写者**：
- `src/wqb/workflow/nodes/feature_engineering.py` — FE 节点产出

---

### 2.2 `tracking/<REG>/` — 区域事实面（37 个写者）

**规范**：所有区域专属的探针、脚本、配置、结果都落 `tracking/<REGION>/`（`REGION` = `DEU/EUR/GBR/IND/KOR/MEA/USA/ASI/GLB` 三字母大写平台数据标识）。

**主写者（按用途分）**：

| 用途 | 写者 |
|---|---|
| 配置 / 画像 | `src/wqb/profiles/cells.py`, `src/wqb/profiles/render.py`, `src/wqb/memory/idea_ledger.py` |
| 战役 / 波次 | `src/wqb/workflow/nodes/campaign.py`, `src/wqb/workflow/nodes/batch_track.py`, `tools/campaign_intel.py`, `tools/preflight_wave.py`, `tools/pool-hygiene/prod_watch.py` |
| 探针 / 筛选 | `tools/probe_batch_mode.py`, `tools/tiered_probe.py`, `tools/prod_first_screen.py`, `tools/prod_blocked_recheck.py`, `tools/s0_enhanced_screening.py`, `tools/sa_probe.py`, `tools/scan_fields.py`, `tools/backfill_gate_plan.py`, `tools/backfill_prod_corr.py`, `tools/batch_status.py` |
| 数据修复 / 归档 | `tools/build_cluster_variants.py`, `tools/harvest_multisim.py`, `tools/fetch_all_universes.py`, `tools/gen_field_inspect_packs.py`, `tools/gen_inspect_from_db.py` |
| 论坛 / 外部 | `tools/forum_recon.py`, `tools/forum_research.py`, `world-quant-brain-mcp/labs_data_analysis_agent.py` |
| 工具自身 | `tools/code-audit/*`, `tools/index_tables.py`, `tools/skills/gen_region_skill_scaffold.py`, `tools/webdata_quality.py`, `tools/pick_backlog_representatives.py`, `tools/verdict/perf_max.py` |
| Skill 侧 | `Claude/skills/wq-brain-campaign-toolkit/scripts/*` |

---

### 2.3 `attic/` — 归档面（10 个写者）

**规范**：退役的 skill / 数据 / 脚本进 `attic/<主题>_<YYYYMMDD>/`；**归档而非删除**。

**写者（全部是治理工具）**：
- `tools/audit_file_sizes.py` — 归档超大小件
- `tools/audit_structure.py` — 目录治理
- `tools/code-audit/audit_write_targets.py` — 本审计闸
- `tools/code-audit/doc_path_refs.py` — 文档路径清理
- `tools/complexity_scan.py` — 复杂度阈值归档
- `tools/index_tables.py` — 索引清理
- `tools/refs_scan.py` — 引用扫描
- `tools/run_grouped_tests.py` — 分组测试归档
- `tools/scan_test_groups.py` — 测试分组
- `tools/skill_lint.py` — skill 归档

---

### 2.4 `cache/` — 断点缓存（31 个写者，1,800 个文件，`gitignore`）

**规范**：脚本运行期断点、下载缓存、临时分析中间产物。`.gitignore` 已排除。

**典型写者**：`tools/probe_batch_mode.py`, `tools/tiered_probe.py`, `tools/forum_recon.py`,
`tools/mcp_http_caller.py`, `tools/run_grouped_tests.py`, `tools/s0_enhanced_screening.py`,
`tools/verdict/candidate_health_card.py`, `src/wqb/search/scheduler.py` 等 31 个。

---

### 2.5 `logs/` — 日志（25 个写者，1,802 个文件，`gitignore`）

**规范**：跑批日志、异步任务 stdout/stderr、工具运行日志。`.gitignore` 已排除。

**典型写者**：`src/wqb/workflow/nodes/{batch_track,campaign,gem,feature_engineering}.py`
（异步任务 `stdout.log` / `stderr.log`）；`tools/pipeline_integration.py`, `tools/quality_control_engine.py`,
`tools/verdict/submit_inventory.py`, `tools/audit_file_sizes.py` 等 25 个。

**特殊路径**：`logs/_async_tasks/` — 由 `resolve_async_tasks_root()` 统一锚定（`REPO_ROOT/logs/_async_tasks`，支持 `WQB_TASK_ROOT` env 注入用于单测隔离）。

---

### 2.6 `results/` — 续跑 checkpoint（68 个写者，248 个文件，`gitignore`）

**规范**：批量任务 / 回测 / 采样的续跑 checkpoint（json/parquet），下次启动跳过已完成项。

**典型写者（68 个是**最密集**的出口）**：`src/wqb/workflow/nodes/campaign.py`, `src/wqb/memory/idea_ledger.py`,
`tools/backfill_*.py`, `tools/harvest_multisim.py`, `tools/ledger/enqueue_propose.py`,
`tools/verdict/daily_select.py`, `tools/data-repair/*`, `Claude/skills/wq-brain-campaign-toolkit/scripts/harvest.py` 等。

---

### 2.7 `data/` — 运行期数据（89 个写者，10 个文件，`gitignore`）

**规范**：`data/wqb.db`（SQLite 主库）+ 少量 JSON 台账。

**典型写者**：`src/wqb/db_write_lock.py` 系列（`wqb.db` 读写锁）、
`src/wqb/memory/idea_store.py`, `src/wqb/modeb/usage_tracker.py`,
`tools/backfill_*.py`, `tools/build_*.py`, `tools/migrate_*.py`,
`world-quant-brain-mcp/{mcp_core,super_alpha_tool,brain_mixin_correlation,labs_data_analysis_agent}.py` 等。

**关键写者**：`tools/code-audit/db_mcp_split.py` — 拆分 MCP 服务到多个模块，改 DB schema。

---

### 2.8 `docs/` — 长期规范/SOP（15 个写者）

**规范**：`docs/` 是**人工面**（长期规范、SOP、速查）。代码写它只有两条正路：
① **已登记的生成器**（`index_tables.py` 类，产物是嵌入代码块的表格）；
② 一次性迁移脚本。

**已登记的生成器**（合法写者）：
- `tools/index_tables.py` — `docs/env_and_switches.md` 的 env-table 嵌入块；`docs/env_registry.json` 索引
- `tools/refresh_operator_catalog.py` — 算子目录刷新

**疑似违规（审计闸 UNKNOWN，需人工核对）**：
- `src/wqb/profiles/render.py` — 可能写 `docs/profiles/<REG>.md`（区域画像渲染）
- `tools/closure_ledger.py` — 关闭台账
- `tools/super_build.py` — SUPER 构建
- `tools/skills/gen_region_skill_scaffold.py` — 区域 skill 骨架生成
- `tools/select_ra_basket.py`, `tools/verdict/submit_inventory.py` — 疑似写 docs
- `world-quant-brain-mcp/brain_mixin_correlation.py` — MCP 侧写者
- `tools/audit_structure.py`, `tools/run_grouped_tests.py`, `tools/skill_lint.py`, `tools/code-audit/*.py` — 治理工具（读为主，写为辅）

---

### 2.9 `reports/` — 人工审计/评审（8 个写者）

**规范**：`reports/` 是**人工面**（评审、审计、复盘），代码写它的场景应接近于零。

**实际写者**：
- `tools/closure_ledger.py` — 关闭台账生成器（`reports/closure_ledger.md`），**合法登记**（一次性台账快照，属治理类）
- 其余 7 个（`tools/code-audit/*`, `tools/audit_structure.py`, `tools/refs_scan.py`, `tools/mcp_http_caller.py`）均是**治理工具读为主写为辅**——把审计日志 append 到 `reports/` 下的 `audit_*.md`，属合法登记

**2026-10-20 复核结果**：先前扫描把 `judge_alpha.py` 和 `brain_mixin_correlation.py` 标为「⚠ 疑似违规」——经复核**均非真违规**：
- `brain_mixin_correlation.py`：命中点是英文注释里的「BRAIN reports two distinct correlations」单词，非路径；
- `judge_alpha.py`：命中点是变量 `reports = []`（Python 列表变量名），非路径；真正的写盘目标是 `SKILL_DIR / "outputs"`——**这确实是真 bug**，见 §2.10。

⇒ `reports/` 目前无真违规写者，纪律矩阵中「⚠ 2 个疑似写者」标记可撤销。

---

### 2.10 `Claude/skills/*/outputs/` — Skill 运行时产物误锚定安装位（**真违规已修**）

**发现（2026-10-20）**：`Claude/skills/brain-alpha-judge/scripts/judge_alpha.py` 原实现用
`SKILL_DIR = Path(__file__).resolve().parents[1]` + `outputs_dir = SKILL_DIR / "outputs"`，
把运行期产物直接写回 skill 安装位。后果：

- **产物泄漏到 6 个同步安装位**：`.workbuddy/`, `.claude/`, `.cursor/`, `.codex/`, `.cline/`, `.agents/`
  每个都能成为写目标，任一处运行都会污染 skill 目录；
- **下次 `sync_skills.py --apply` 时会被同步逻辑识别为「安装位漂移」清理/覆盖**；
- **违反 §8.13**：`Claude/skills/` 是"只读源码面"，运行期产物必须去 `output_report/`；
- **同类 bug 曾在 GEM 侧犯过**（2026-09-26 `pipeline_reports.py` 迁移到 `GEM_REPORT_ROOT` 已修复）。

**修复（本次提交）**：`judge_alpha.py` 新增 `_resolve_repo_root()` + `_resolve_outputs_dir()`，
优先级：`WQB_JUDGE_DATA_ROOT` env → `<REPO_ROOT>/output_report/brain-alpha-judge/` → `SKILL_DIR/outputs/` 兜底。

**存量清理**：本次审计时各安装位 `outputs/` 目录均已清空（此前 sync 清理过），无残留需迁移。

**教训**：与 2026-09-26 GEM `pipeline_reports.py`、2026-07-22 `prepare_session_pack` 属同一 bug 家族——**skill/工具用 `Path(__file__)` 锚定相对路径，一旦该文件被部署到多个位置就产生漂移**。此后凡新写 skill，产物目录必须走 env + REPO_ROOT 双保险模式（参考 `wqb/provision/gem/pipeline_reports.py`）。

---

## 3. 出口纪律矩阵

| 出口 | 谁可以写 | 谁不可以写 | 现有闸 |
|---|---|---|---|
| `output_report/` | workflow / 战役工具 / 报告生成器 | 人工直接新建（应走工具） | `audit_write_targets` 白名单 ✅ |
| `tracking/<REG>/` | 区域专属工具 / 战役节点 / FE 节点 | 通用工具写跨区域内容 | `audit_write_targets` 白名单 ✅ + `audit_structure` S13/S16 |
| `attic/` | 治理工具（`audit_*`, `sync_skills`, `retention`） | 应用代码写 `attic/` | `audit_write_targets` 白名单 ✅ |
| `cache/` `logs/` `results/` `data/` | 全部运行期脚本 | 人工编辑 | `.gitignore` ✅ |
| `docs/` | **已登记生成器**（`index_tables.py` 等） | 未登记的迁移/清理脚本 | `audit_write_targets` 违规判定 ⚠ 待核对 15 个疑似写者 |
| `reports/` | **已登记治理工具**（`closure_ledger.py` + 审计闸日志） | 应用代码 | `audit_write_targets` 违规判定 ✅（先前 2 个疑似均复核为假警报） |
| `Claude/skills/*/outputs/` | **无**（skill 安装位不允许运行期写入） | 任何 skill 脚本 | 2026-10-20 已修 `judge_alpha.py`（env + REPO_ROOT 双保险）✅；`sync_skills.py` 同步会清理漂移 |
| `Claude/skills/` | **唯一写者 = `tools/sync_skills.py --apply`** | 任何其它脚本 | 待补闸（本轮未加，属审计闸白名单外） |
| `src/` `tools/` `world-quant-brain-mcp/` | 只有 IDE/编辑器写 | 任何运行期代码自改 | `audit_write_targets` 违规判定 ✅ |

---

## 4. 治理现状

- ✅ **运行期产物面（cache/logs/data/results）全部 gitignore 且 0 跟踪** —— 版本库干净
- ✅ **`src/` `tools/` 内无产物入库** —— 只有 `tools/git-hooks/{pre-commit,commit-msg}` 与 `tools/docs/*.md`（说明书，合法）
- ✅ **本轮修掉的裸写盘**：`src/wqb/search/scheduler.py` 的 `prepare_session_pack` 曾相对 cwd 写 `tracking/sessions/<date>/`，已锚定 `find_repo_root()`
- ✅ **审计闸就位**：`audit_write_targets.py` 把 §8.13 从"约定"变成"可执行"（棘轮 + 16 条测试）
- ⚠ **待补**：`Claude/skills/` 面的写者收敛闸（唯一合法写者 `sync_skills.py --apply`，其它脚本写它 = 同步面分叉风险）
- ⚠ **待核**：`docs/` 15 个写者、`reports/` 2 个写者的合法性核对

---

## 5. 审计方法学

- 用 AST 抓写盘调用，沿**赋值图回溯 2 层**把路径从变量解析成字面量
- 违规判定**优先于**允许判定（避免 `docs/xxx/tmp_foo.json` 因含 "tmp" 被放行）
- 正则加词边界 `(?<![A-Za-z0-9_-])docs\b`（防 `my_docs` 误伤，且覆盖 `Path("docs")` 无尾斜杠形态）
- 短变量名（`p`/`tmp`/`out`/`doc`）解析不出路径 → **判 UNKNOWN，绝不判 VIOLATE**（防假证据卡提交）
- 棘轮指纹 = `file::kind::label`，**不含行号**（无关改动导致行号漂移不影响棘轮）

---

*生成时间：2026-10-20，审计闸基线 commit `fbbe85a`。*
