# 输出目录治理落地报告（2026-10-08）

> 前置：`reports/output_dirs_governance_review_20261008.md`（审计与分级建议）
> 执行范围：用户选定「**落地安全子集**」——只改**干净已跟踪**文件，凡与 148 个并行会话在途变更重叠的目标一律暂缓（守"不跨会话代操作"铁律）。
> 纪律：改名前 `git grep` 核引用、改名后同步替换引用（固定字符串无正则）、排除在途文件与 `attic/` 归档、全程未 `commit`（避免卷入在途变更）。

---

## 0. 一页结果

| 类别 | 数量 | 状态 |
|---|---|---|
| reports 日期带杠 → `YYYYMMDD` | 10 | ✅ 已落地（+4 引用文件同步） |
| output_report 日期置末 | 2 | ✅ 已落地（0 引用，直接 rename） |
| AGENTS.md §8.13 规范更新 | 3 条判据 | ✅ 已落地 |
| campain → campaign（原 P0） | 8 | ↩️ **已回退**（发现是既定命名约定，非拼写错误） |
| 与在途冲突项 | 4 类 | ⏸️ 暂缓（见 §3） |

---

## 1. 已落地清单

### 1.1 reports 日期带杠 → YYYYMMDD（10 个 rename）
`db_schema_audit` / `db_table_structure_review` / `feature_engineering_eval` / `alpha_templates_forum` / `glb_forum_experience` / `ppa_forum_experience` / `progress` / `temp_and_deadcode_scan` / `tmp_cleanup` / `toolkit_usage_review`（日期 `2026-08-2x` → `202608xx`）。

引用同步（4 个文件，经 `git grep` 定位、固定字符串替换、复核无断链）：
- `tools/step_funnel.py`（docstring 引用 `db_schema_audit_20260826.md:59`）
- `reports/db_concurrent_write_lock_audit_20260920.md`
- `output_report/forum_mining_experience_20260913.md`
- `Claude/skills/wq-brain-campaign-toolkit/config/template_families.json`（evidence source 引用 `ppa_forum_experience_20260807.md`）

### 1.2 output_report 日期置末（2 个 rename）
- `ra_pipeline_stage_audit_20260916_v3.md` → `ra_pipeline_stage_audit_v3_20260916.md`
- `GLB_RA_campaign_20260919_S-PRE_to_S1.md` → `GLB_RA_campaign_S-PRE_to_S1_20260919.md`
（均 0 引用，直接 rename。）

### 1.3 AGENTS.md §8.13 规范更新（3 条判据，新文件强制）
1. **output_report vs reports 边界判据**：workflow/战役自动产出（ideas/candidates/wave 结果/工具直写）→ `output_report/`；人工撰写的审计/评审/复盘/演练/价值评估 → `reports/`。
2. **文件名区域码大写豁免**：`DEU/EUR/GBR/GLB/IND/KOR/MEA/USA/ASI` 开头大写是平台数据标识（同 `tracking/<REGION>` 豁免），不属 snake_case 违规；纯英文大写（`ANALYST_`/`READY_`）不豁免。
3. **`campain` 既定命名约定**：写入规范，防止后人再误判为拼写错误。

---

## 2. ★ 关键纠错：campain 是既定命名约定，非拼写错误

审计报告曾把 `reports/dataset_experience/*_campain.md` 的 `campain` 列为"拼写错误"并建议批量改 `campaign`。落地核查发现这是**审计失误**：

- `wq-brain-ra-pipeline/references/step1-inventory.md:61` 明确写 **"`campain` 是既定文件名，非笔误"**。
- `src/wqb/research/dataset_experience.py:223` 用 `f'{region}_{ds}_campain.md'` **生成**新经验文件。
- `tools/step9_audit.py:216` 按 `_campain.md` **校验**经验文件存在性（注释亦标"注意历史拼写 campain"）。
- `brain-dataset-mining-experience`、`wq-brain-ra-pipeline`、`step9-writeback`、`tools/README.md` 均按该后缀引用。

单改文件名会造成与生成/校验代码的**系统性不一致**（step9_audit 将按 campain 找不到 campaign 文件而误报缺失，代码仍生成 campain 新文件）。

**处置**：已将 8 个改名文件 + 6 个引用方用 `git checkout HEAD` **精确回退**（避免反向 sed 误改正文中正确的 campaign 单词），`dataset_experience/` 已恢复 9 个 campain 文件原状，`git status` 无残留。该约定已写入 §8.13 防再犯。

> 若日后真要统一为 campaign，须作为**独立重构专项**：连 `dataset_experience.py` 生成、`step9_audit.py` 校验、两个测试文件、全部存量与在途文件一并改，并回归测试——不可夹在日常改名里单点处理。

---

## 3. 暂缓清单（含原因）

| 项 | 原因 | 建议时机 |
|---|---|---|
| `output_report/ANALYST_*.md`（3 个）→ snake_case | **在途（A）**：并行会话正写的 DEU analyst 产物 | 其提交后 |
| `usa_analyst_consensus_campain.md` | **在途（A）**；且 campain 系既定命名，本不应改 | 不动 |
| `tools/audit_structure.py` 机器守卫扩展（output_report/reports 命名 FAIL 规则） | **在途（M）**：并行会话正在改守卫 | 其提交后另行扩展 |
| `selfcorr_quick_out/` 归并 | 需改 `skill.py` + `doc_path_refs`/`repo_governance_check`；其中 `doc_path_refs` baseline fixture **在途（M）** | 其提交后 |
| output_report ideas 补日期（P2） | ① 存量不强改；② 高频检索类（final/candidates/summary）在无日期文件中无对象；③ EUR/IND/DEU 正处并行挖掘活跃期，改 ideas 断引用/冲突风险 > 收益 | 新文件日期强制已入 §8.13 前置约束 |
| reports 子目录 snake→kebab（P2） | `dataset_experience/` 含在途文件 | 存量可缓 |
| `sync_skills` 同步 | 我的 `template_families.json` 是 evidence source 说明文字（非 SOP 逻辑，不致"读旧 SOP"）；全量 sync 会卷入并行会话 2 个在途 skills 修改（`wq-brain-ra-deu/SKILL.md`、`regions/DEU.md`） | 并行会话提交后统一 sync |

---

## 4. 验证（复审计）

- 保留 rename **12**（日期带杠 10 + 日期置末 2），无断链（旧名 `git grep` 归零）。
- reports 日期带杠残留 **0**；日期置末旧文件已不存在。
- campain 引用方全部 clean（回退无残留）；ANALYST 3 个在途未动。
- 本次治理变更**未 commit**，与 148 个并行会话在途变更并存于工作区/staging——提交时请用 `git add` 指定本报告 §1 所列路径单独提交，避免卷入在途工作。

---

## 5. 本次变更文件清单（供单独提交）

**rename（12）**：见 §1.1/§1.2（`git status` 中 `R ` 状态，排除 campain）。
**引用同步（4）**：`tools/step_funnel.py`、`reports/db_concurrent_write_lock_audit_20260920.md`、`output_report/forum_mining_experience_20260913.md`、`Claude/skills/wq-brain-campaign-toolkit/config/template_families.json`。
**规范（1）**：`AGENTS.md`（§8.13 三条判据）。
