# 输出目录规范复核（第二轮 · 2026-10-08 23:5x）

> 第一轮治理（改名 12 + 下沉 5 + 22 次提交）已落盘。**本轮复核的是「治理是否守得住 + 还漏了什么」**，
> 结论先说：**主体规范已稳住，但治理面漏了 `tracking/`，且发现一类会永久丢资产的隐患（报告落进 gitignore 目录）。**

判据：AGENTS.md §8.13（目录归属与命名规范：人工审计复盘 → `reports/`，自动/战役产物 → `output_report/`；
日期一律 `YYYYMMDD` **作后缀**；路径纯 ASCII；归档 → `attic/<主题>_<YYYYMMDD>/`）。

---

## 1. 上轮治理的保持情况（复审计）

| 指标 | 第一轮后 | 现在 | 判定 |
|---|---|---|---|
| `output_report/`+`reports/` 日期带杠 | 0 | **0** | ✅ 守住了 |
| 非 ASCII / 含空格文件名 | 0 | **0** | ✅ 守住了 |
| 未跟踪源码（`repo_governance_check`） | 68 | **3** | ✅ 大幅改善（提交治理的直接效果） |
| 根目录散件（S7） | 0 | **0**（仅 9 个白名单入口/配置文件） | ✅ 守住了 |
| `output_report/` 规模 | 156 | **159**（并行会话新增 3） | ⚠ 见 §2.E |
| 快照台账 PENDING | 512 | **527**（改名带来 12 条幻影 + 3 条后来） | ⚠ 见 §2.C |

---

## 2. 新发现（按优先级）

### P1 · 必须修

**A. 治理面漏了 `tracking/`：顶层 4 个「日期带杠」文件（违反 §8.13）**

```
tracking/2026-10-06_robustness.md
tracking/2026-10-07_robustness.md
tracking/2026-10-07_robustness_E5ReEnpP.md
tracking/2026-10-08_robustness.md
```

第一轮只扫了 `output_report/` 与 `reports/`，`tracking/` 顶层 55 个 `.md` 未纳入扫描面。
`robustness` 是**每夜自动追加**的产物 ⇒ 每天 1 个带杠文件在累积。
修法：改名 `tracking/robustness_<YYYYMMDD>.md`（产物类亦可移 `output_report/`），并同步引用（`doc_path_refs` 会守）。

**B. ★ 报告类 md 落在 gitignore 目录内 ⇒ 不入库，`git clean -fd` 即永久丢失**

已实测 `git check-ignore` 命中 `.gitignore:176 /cache/`、`177 /results/`：

| 文件 | 性质 | 风险 |
|---|---|---|
| `cache/eur_analyst_fields_report.md` | **分析报告（结论资产）** | 高：不该放运行缓存目录 |
| `logs/session/{findings,progress,task_plan}.md` | 会话草稿 | 中：属运行期，但同样丢 |
| `results/*.md`（`inventory_consolidated_20261005~08`、`submit_report_*` 等） | 运行期盘点产物 | 中：`results/` 续跑断点不可动，这 6 个 md 不是断点 |

修法：结论类报告（`eur_analyst_fields_report.md`）迁 `output_report/`；`results/` 的 md 若为盘点结论也应迁出（**只迁 md，不动 checkpoint json**）。

**C. 抢救点台账 845 件 / PENDING 527 —— 改名会持续制造幻影项**

台账按 **HEAD vs 抢救点快照** 口径：在 main 里改一次名，快照里的旧名就多一条「独有件」（上轮 +12）。
这不是一次性债，而是**每改一次名就 +1 条**的机制性问题。
修法（建议交工程实现）：`snapshot_adjudicate.py` 增加**改名识别** —— 按 blob 比对，若快照里的旧名与 main 中某新名内容相同，判 `RENAMED → <新名>` 而非 PENDING。

### P2 · 建议修

**D. `reports/` 结构与内容混杂**

- 9 个子目录里 **2 个日期化**（`ra_pipeline_stage_review_20260927/`、`skills_review_20260929/`）对 **7 个连字符主题**
  （`dataset_experience/`、`eur-mining/`、`forum-experience/`、`forum_alpha_research/`、`gbr-campaign-final/`、
  `project-audit/`、`tooling-research/`）——风格不统一。
- `reports/forum_alpha_research/` 混着**运行产物** `read_posts.json` / `search_results.json`（应出仓）
  与 3 个无日期脚本（`gather_search_v2.py` / `make_digest.py` / `read_posts.py`）。
- 20 个 py/sh 里 18 个文件名无日期（其中 15 个位于日期化目录下，靠**目录名**提供日期上下文 ⇒ 可接受；
  真正缺日期上下文的是 `forum_alpha_research/` 那 3 个）。

**E. `output_report/` 159 个文件全平铺 + 12 组近重复**

无子目录，检索性随规模下降；且存在 12 组「同产物多版本并存」：

```
IND_d1_model{16,32,36,144,252}_ideas{,_v2}.md        # 5 组
ra_pipeline_stage_audit_20260916{,_v3}.md
dryrun_chain_result_20260927{,_v2}.json / dryrun_chain_runner_20260927.py
opswap_experiment_20260930 · skills_review_20260929 · ra_pipeline_stage_review_2026092{7,8}
```

建议：① 按 `output_report/ideas/<REGION>/` 分区（工具直写方需同步改路径，须先查写方）；
② 版本后缀统一规则（`_v2` 保留但旧版按 §7 归档进 `attic/`）。

### P3 · 可选

| 项 | 现状 | 建议 |
|---|---|---|
| **F. S16 命名守卫** | 命名规范只写在 §8.13，无机械闸 | 加进 `audit_structure`：新建文件违规 FAIL，15 条「日期非后缀」存量入基线（§8.13 明示存量不回改） |
| **G. `selfcorr_quick_out/`** | 未跟踪、**0 文件**（空目录） | 直接删（仍是上一轮「既定豁免」的残留壳） |
| **H. `cache/` 373M、3072 文件** | 运行期目录 | 用 `tools/retention.py` 清理（注意备份数硬闸 ≤2） |

---

## 3. 边界判据复检（人工复盘 vs 自动产物）

第一轮写入 §8.13 的判据执行效果：

- `output_report/` 命中 lesson/review/audit 关键词 **20 个**，但**多数是工具直写的审计扫描产物**
  （`operator_usage_audit_*.json`、`skill_workflow_dryrun_audit_*`、`attic_cleanup_audit_*`）⇒ 按判据**留** output_report 正确，不迁。
  真正像「人工复盘」的仅 `DEU_session_lessons_20261007.md`、`GBR_campaign_lessons_20261007.md` 等 2–3 件。
- `reports/` 中疑似自动产物仅 2 件，其中 `temp_and_deadcode_scan_*` 实为审计复盘 ⇒ **留** reports 正确。

⇒ **边界判据健康，不建议再做批量回迁**（第一轮的结论仍然成立：37 件疑似逐件精读的收益低于移动风险）。

---

## 4. 建议执行顺序

1. **A + B**（半天内）：`tracking/` 4 个改名 + 结论类报告迁出 gitignore 目录；改完跑 `doc_path_refs` + `audit_structure`。
2. **G**（顺手）：删空目录 `selfcorr_quick_out/`。
3. **F**（1 次）：S16 命名棘轮闸（含 15 条存量基线）。
4. **C**（1 次，需改 `snapshot_adjudicate.py`）：改名识别规则，止住幻影项累积。
5. **D + E**（择机，需先查工具写方）：`reports/` 子目录统一 + `output_report/` 分区。

> ⚠ A/B 涉及文件移动与改名，属破坏性动作，落地前请确认；本轮只出审计与建议，未执行。
