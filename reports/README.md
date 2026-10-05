# reports/ 索引与归属判据

> 本目录 = **人工审计与复盘**报告。战役/ideas/评审**产物**一律落 `output_report/`
> （2026-10-01 组织审计定案的报告唯一出口）。完整判据表见 [`AGENTS.md` §8.13](../AGENTS.md)。
> 最后整理：2026-10-04。新增报告请同时更新本文件的主题分组。
>
> 目录结构类需求只看一份：**`structure_review_20261004.md`**（布局复审当前权威）；
> 代码结构债（P1–P11）仍看 `code_structure_survey_20260925.md`，两边不重复。

---

## 一、放这里还是放 `output_report/`？

| 情况 | 去处 |
|---|---|
| 工具按路径直写的产物（ideas 批次报告、fulltest 报告、归档快照） | `output_report/` |
| 人（或 Agent 受人指派）写的审计、复盘、口径核对 | `reports/`（本目录） |
| 长期规范 / SOP / 速查（不是一次性结论） | `docs/` |
| 结论已收口、正文只作留痕的一次性审查 | 留本目录，**不删**（是审查证据） |

**命名**：`<主题>_<YYYYMMDD>.md`（日期作后缀，不写 `2026-10-04_xxx.md`）。

## 二、两条多版本谱系：以最新为入口

同一评审出现过 v1→v4 并列平铺，新 Agent 无法判断该读哪份。以下 **加粗 = 当前入口**，
其余为过程留痕（保留不删，但不要在它们之上做决策）：

| 谱系 | 过程件 | 当前入口 |
|---|---|---|
| RA/skills 阶段评审 | `ra_pipeline_stage_review_20260927.md`、`ra_pipeline_stage_review_v3_20260928.md`、`skills_pipeline_stage_review_20260927.md`、`skills_stage_review_v2_20260927.md`、`skills_review_20260929.md`、`skills_review_20260929_closure.md`、`skills_full_review_20260929.md` | **`ra_pipeline_stage_review_v4_20260928.md`**（该谱系最后一版） |
| 结构/组织审计 | `code_structure_survey_20260925.md`（P1–P11 结构债台账）、`temp_and_deadcode_scan_2026-08-28.md`、`tmp_cleanup_2026-08-30.md` | **`output_report/org_audit_20261001.md`** + `output_report` 内 2026-10-03/04 治理记录；结构债台账仍以 `code_structure_survey_20260925.md` 为唯一明细（AGENTS.md §8.4 第 5 项指派，两边不重复列举） |

⚠ 日期后缀不统一的旧件（`db_schema_audit_2026-08-26.md`、`feature_engineering_eval_2026-08-27.md`、
`tmp_cleanup_2026-08-30.md`、`toolkit_usage_review_2026-08-31.md`、`decommission_cause_analysis_20260920.md`
等）属**存量**，按 §8.13「存量不强制回改」保留；新建报告一律紧凑式。

## 三、豁免：以下不是"散落脚本"，勿当一次性产物归档

- **`dataset_experience/`** —— skill 约定的活路径，被 `src/wqb/research/dataset_experience.py`
  与 3 个 skill 共 8 处引用（2026-10-01 审计"主动不做"项，移动即断链）。
- **带日期前缀的 `.py`** —— 常是审查结论的**可重跑证据**（报告正文写着
  「可复现：`python reports/xxx.py`」），已由 `audit_structure.py` 的 `S5_EXEMPT_PREFIXES` 登记豁免。
  判据全文见 `tools/legacy/README.md`。
- **子目录命名**（`forum-experience/`、`gbr-campaign-final/`、`project-audit/` kebab
  与 `dataset_experience/`、`skills_review_20260929/`、`tooling-research/` snake 并存）——
  存量混用，新建一律 kebab-case（§8.13）。

## 四、主题分组速查

| 主题 | 代表文件 |
|---|---|
| 结构与代码债 | `structure_review_20261004.md`（**目录布局复审，当前权威**）、`code_structure_survey_20260925.md`（P1–P11 代码结构债台账，与布局不重叠）、`db_mcp_split_20261004.md`（拆 `wqb_db_mcp.py`：尝试/回滚/移交件）、`db_schema_audit_2026-08-26.md`、`db_table_structure_review_2026-08-26.md`、`db_concurrent_write_lock_audit_20260920.md` |
| skills / 流水线评审 | 见第二节谱系表；子目录 `skills_review_20260929/`、`ra_pipeline_stage_review_20260927/` |
| 属性与标签治理 | `alpha_properties_audit_20260920.md`（规范源在 `src/wqb/alpha_properties.py` + `docs/alpha_properties_spec.md`） |
| EUR 战役逐日探针/机制 | `eur_d1_*` 共 15 份 |
| 论坛情报与知识迁移 | `forum_alpha_inspiration_taxonomy_20261002.md`、`forum_to_skills_integration_plan_20261002.md`；子目录 `forum_alpha_research/`、`forum-experience/` |
| 工具链使用与退役 | `toolkit_usage_review_2026-08-31.md`、`decommission_cause_analysis_20260920.md`、`rescue_campaign_20260915.md`、`inventory_submittable_20260909.md`、`usa_superalpha_feasibility_20260914.md` |
| 特征工程 | `feature_engineering_eval_2026-08-27.md`、`field_inventory_analysis_20260929.md` |

## 五、机器守护

```
python tools/audit_structure.py --only s5    # reports/ 散落脚本（WARN，豁免见第三节）
```

⚠ 本文件**不在** `S9` 的校验范围内（S9 只校 AGENTS.md §1 职责表与 `docs/README.md` 目录树），
所以这里的子目录名靠人工维护；新增主题分组时请同步第二节。
