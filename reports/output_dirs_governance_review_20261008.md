# 输出目录规范性审计与治理建议（2026-10-08）

> **范围**：`output_report/`、`reports/`、`selfcorr_quick_out/`、仓库根级散落文件
> **判据**：`AGENTS.md` §8.13（目录归属与命名规范）、§8.4/§8.5（审计纪律）
> **方法**：机器盘点（find/grep 精确统计）+ 抽样精读（验证"产物 vs 复盘"分工真实性，避免 §8.5 仅凭文件名下结论的教训）

---

## 0. 一页结论

| 维度 | 评级 | 要点 |
|---|---|---|
| 仓库根散落输出 | ✅ 合规 | 根级 13 个文件全部为配置/文档/入口，无 `sa_*.log`/`dump.rdb`/`0` 类违规 |
| 目录定位（output_report vs reports） | ⚠️ 边界模糊 | "评审/审计"主题两头分流；`output_report` 混有审计复盘性质文件 |
| 命名规范 | ❌ 执行松散 | 缺日期、日期带杠、日期后挂版本、拼写错误、子目录命名混用 |
| 孤立输出目录 | ⚠️ 待决策 | `selfcorr_quick_out` 根级孤立，被 skill + 2 个 audit 工具白名单引用 |

**总评**：内容分工骨架（产物→`output_report`、复盘→`reports`）基本成立，无大规模错位堆积；但命名规范执行松散、个别文件定位错位、存在一个待决策的孤立目录。属"**骨架正确、执行松散**"。治理重点：**划清边界判据 + 明确违规小批量修正 + 机器守卫前置**。

---

## 1. 分目录发现（精确统计）

### 1.1 `output_report/`（报告唯一出口）— 150 文件 / 1.8MB
构成：144 md, 3 json, 2 txt, 1 csv；全部 2026 年。

| 检查项 | 数量 | 判定 |
|---|---|---|
| 无 YYYYMMDD 日期后缀 | **64** | ❌ 违规，集中在 ideas 产物（EUR 27、IND 14、USA 8、MEA 5、KOR 4 等） |
| 文件名大写字母开头 | 94 | ⚠️ 其中 **91 为区域码**（DEU/EUR/GBR/GLB/IND/KOR/MEA/USA，存量惯例）；**3 为纯英文大写 `ANALYST_*`**（违规） |
| 日期后缀后仍挂内容（`_v2`/`_v3`/`S-PRE_to_S1`） | 2 | ❌ 违规（日期应置最末）：`ra_pipeline_stage_audit_20260916_v3.md`、`GLB_RA_campaign_20260919_S-PRE_to_S1.md` |
| 定位错位（审计复盘性质混入产物出口） | ≥1 实测 | ❌ `ra_pipeline_stage_audit_20260916.md` 实测为"价值评估/审计/演练/自我纠错"内容，按"人工复盘"应属 `reports/` |

### 1.2 `reports/`（人工审计与复盘）— 96 文件 / 3.1MB
构成：59 md, 14 py, 10 txt, 6 sh, 6 json, 1 html。

| 检查项 | 数量 | 判定 |
|---|---|---|
| 日期带杠（`YYYY-MM-DD` 而非 `YYYYMMDD`） | **10** | ❌ 违规（`db_schema_audit_2026-08-26.md`、`feature_engineering_eval_2026-08-27.md`、`tmp_cleanup_2026-08-30.md` 等） |
| 无日期 `.md` | **23** | ❌ 违规（`dataset_experience/*.md`、`eur_mining_report.md`、`GBR_goal_final_report.md` 等） |
| `campain` 拼写错误（应 campaign） | **9** | ❌ 质量问题（`dataset_experience/` 系列） |
| snake_case 顶层子目录（应 kebab-case） | **4** | ❌ 违规（`dataset_experience`/`forum_alpha_research`/`ra_pipeline_stage_review_20260927`/`skills_review_20260929`） |
| `forum_alpha_research/` 可复用工具脚本（无日期 `.py`） | **3** | ❌ 定位错位（`gather_search_v2.py`/`make_digest.py`/`read_posts.py`，应进 `tools/`） |

### 1.3 `selfcorr_quick_out/`（孤立根目录）— 2 文件 / 7.1MB
- `os_alpha_pnls.pickle`（7.2MB，**数据产物**）、`alpha_results_10-03_GLB.xlsx`（9.8KB，**报告**）。
- **命名违规**：目录含下划线（非 kebab-case）；xlsx 日期 `10-03` 非 YYYYMMDD、`GLB` 大写。
- **归属**：被 `brain-calculate-alpha-selfcorr-quick` skill（`scripts/skill.py`）+ `tools/code-audit/{doc_path_refs,repo_governance_check}.py` 白名单引用 → 非乱放，是"**被豁免的孤立目录**"。
- 按 §8.13：报告应进 `output_report/`、数据应进 `cache/` 或 `results/`，不应独立根目录。

---

## 2. 边界模糊根因

§8.13 把 `output_report` 定义为"战役 / ideas / **评审产物**"，把 `reports` 定义为"**人工审计与复盘**"。"评审产物"与"审计复盘"语义高度重叠，导致 `ra_pipeline`（7 vs 4）、`skills`（10 vs 8）等主题在两头各留版本，检索靠运气——这正是 §8.13 自述反例（"同一份 review 两个目录各留一版"）仍在发生的证据。抽样实测：`output_report/ra_pipeline_stage_audit_20260916.md` 通篇是"审计/价值评估/演练/自我纠错"，按"人工复盘"应属 `reports/`。

---

## 3. 治理建议（分级）

### P0 — 明确违规、量小、可直接改（建议本轮处理）
1. `reports` 10 个日期带杠 → 重命名为 `YYYYMMDD`（如 `db_schema_audit_2026-08-26.md` → `db_schema_audit_20260826.md`）。
2. `reports` 9 个 `campain` → `campaign` 批量修正。
3. `reports/forum_alpha_research/` 3 个工具脚本 → 可复用则迁 `tools/` 并登记 `tools/README.md`；一次性则补日期进对应带日期目录。
4. `output_report` 3 个 `ANALYST_*` → snake_case（`analyst_*`）。
5. `output_report` 2 个日期后挂版本 → 日期置最末（如 `..._v3_20260916.md`）。

> ⚠ P0 全部为"改名"，执行前须核 `refs=0`（`git grep -w <name>`），避免断引用（与 §8.4 归档纪律同源）。

### P1 — 边界/归属，需决策
6. **划清判据（消除两头分流）**：建议写进 §8.13 ——
   - "凡**人工撰写**的审计/评审/复盘/演练/价值评估 → `reports/`"
   - "凡 **workflow/战役自动产出**（ideas、candidates、wave 结果、工具直写）→ `output_report/`"
   并据此把 `output_report` 里的审计复盘类文件（`ra_pipeline_stage_audit` 等）回迁 `reports/`。
7. **`selfcorr_quick_out` 二选一**：
   - ① 归并（xlsx→`output_report` 规范命名、pickle→`cache/` 或 `results/`），同步改 `skill.py` + 2 个 audit 工具；
   - ② 维持现状但在 §8.13 登记为"合法例外目录"（注明被 3 处引用，搬迁需同步）。
   建议 ①，长期更干净。

### P2 — 存量命名，不强制回改（§8.13 原则），新文件强制
8. `output_report` 64 个 ideas 产物补日期后缀：存量不强改，但建议对高频检索类（`final_report`/`candidates`/`summary`）做一次性批量补日期（dry-run 先行）。
9. 区域码大写开头（91 个）：建议**保留大写**作为平台数据标识，并在 §8.13 明文豁免（与 `tracking/<REGION>` 目录豁免同逻辑）；纯英文大写（`ANALYST`/`READY`）不在豁免列。
10. `reports` 4 个 snake_case 子目录 → kebab-case（存量可缓，新增强制）。

### 机器守卫（把规范从"人守"变"机器守"）
11. 现有 `audit_structure` S7/S8/S9 守 `tools/`；建议扩展守卫覆盖 `output_report/` 与 `reports/`：**新增文件**若无 `YYYYMMDD` 日期后缀 / 含带杠日期 / 含空格·中文·保留名 / 纯英文大写开头 → `FAIL`。区域码大写与 `reports` 带日期子目录的 `.py`（可重跑证据）走白名单。

---

## 4. 复核入口

- 统计复算：见本报告 §1 各表（`find`/`grep` 命令可重跑）。
- 边界抽证：`output_report/ra_pipeline_stage_audit_20260916.md`（审计复盘性质实测）。
- 归属引用：`grep -rl selfcorr_quick_out tools/ Claude/ src/`。
