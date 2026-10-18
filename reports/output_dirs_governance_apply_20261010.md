# 输出目录治理 · 第三轮整改执行（2026-10-10）

> 承接 `output_dirs_governance_review3_20261010.md`（第三轮复核）的 A–F 六项，用户批准「同意全部修复」。
> 本文件是**执行记录**（改了什么 / 怎么验的 / 哪里与复核结论有出入）。
> 基线：复核时 `audit_structure` FAIL=0 WARN=4、`doc_path_refs` BROKEN=0 UNTRACKED=1、
> `tracking/` 顶层 1 个带杠件。

## 1. 执行结果

| 项 | 处置 | 状态 |
|---|---|---|
| **P1-A** `tracking/2026-10-09_robustness.md` 带杠 | 改名 `robustness_20261009.md` | ✅ |
| **P1-B** `results/` 8 份结论类 md 躺 gitignore | 迁 `reports/`（同 basename） | ✅ 已 0 残留 |
| **P2-C** `reports/` 同名文件+目录并存 | 目录加 `_refs` 后缀（不动 `.md`） | ✅ 零死引用 |
| **P2-D** §8.13 文档与实现漂移 | 补规则④ + 机器产物豁免 + 未跟踪 WARN 预检 + 文档收敛 | ✅ 6 个新测试 |
| **P3-E** `forum_alpha_research/` 混运行产物 | 升级为证据登记（脚本已不可重跑） | ✅ 见 §4 |
| **P3-F** skill 引未入库 `skeleton_panel.py` | 维持未跟踪 | ✅ 并行会话在途 |

**验证（全绿）**：`audit_structure` **FAIL=0**；`doc_path_refs` **BROKEN=0 且 UNTRACKED 归零**（复核时 1）；
`pytest tests/` **3155 passed / 5 failed / 23 skipped**，5 个失败**全在本轮改动之外**（见 §5）。

## 2. P1-A：不只是改名，补了「写盘即见」的预检

改名只解决这一个文件。复发根因是 S16 的扫面 `_s16_targets()` **只取 git 跟踪的** ——
那是 `audit_structure.py` 明写的有意取舍（在途文件不该拦别人的提交），但代价是违规在
`git add` 前**完全隐形**，一 add 就 FAIL，且不在基线（属迟到地拦）。这正是 S16 的立项理由
「文字纪律守不住持续的写入」，同一个坑第二轮复发。

新增 `_s16_untracked()`：用 `git ls-files --others --exclude-standard` 取在途件，**只 WARN 不 FAIL、
不进基线**。语义刻意与主检查区分：预检是「提醒写的人」，FAIL 留给「进索引的那一刻」。

**已实测非空**（不是写完就放着）：造 `tracking/2026-10-10_precheck_probe.md` →
S16 打印 `1 个未跟踪（在途）报告文件名违反 §8.13，git add 后会转为 FAIL: ['tracking/2026-10-10_precheck_probe.md']`；
删除后复检恢复静默，全程 FAIL=0。`tests/unit/07_docs_skills/test_audit_structure_s16.py`
新增 `test_untracked_prescan_sees_the_recurring_violation_shape` 守住复发形态。

## 3. P2-D：收敛文档与实现的漂移

复核结论是「两个里必须收敛一个」。选择**补齐实现**而非放宽文档 —— 因为 87 个无日期件里
绝大多数是历史报告，文档说「一律」而实现不判，等于让人以为欠债只有 40 个。

新增规则④「**人工撰写的报告必须带日期**」。落地时发现**一刀切会误伤机器产物**：
`*_ideas.md`（62 个）+ `*_campain.md`（§8.13 明写「既定文件名，非笔误」）由生成器模板拼名，
消费方依赖**同名覆盖** —— `feature_engineering.py` 的 `stale_ideas_md_path` 比对、
`dataset_experience.py` 生成 + `step9_audit.py` 校验。塞日期会让同一数据集每跑一次多一个文件、
stale 比对失效。故开 `S16_MACHINE_SUFFIXES` 豁免，且**豁免只针对规则④**：
带杠 / 日期不在末尾 / 非 ASCII 对机器产物照样判（`test_machine_exemption_does_not_relax_other_rules` 守边界）。

存量 25 件进 `s16_naming_violations` 基线（15 → 40），WARN 不阻断、只减不增；
豁免的 53 件**未进**基线。AGENTS.md §8.12 与 §8.13 两处同步改口径。

> ⚠ 基线 15→40 是**登记欠债**，不是新增违规 —— 棘轮语义不变（新增仍 FAIL）。
> 但它把欠债从「隐形」变成「可见」，这正是目的：下一个人看到的 40 才是真实规模。

## 4. P3-E：复核结论有一处失实，已按事实重写

复核写「大文件未入库」，实测 `git ls-files` 显示 **7 个文件全部已跟踪**。真正的问题是
**脚本已不可重跑**：硬编码 `http://localhost:8876/mcp`，而本仓库 MCP 是 8000/8001
（`docs/experience/04_engineering.md` 记载 8876 是 `~/.workbuddy/mcp.json` 的历史配置）。
`read_posts.json`(146 KB) / `search_results.json`(171 KB) 是**被引用的事实依据**
（`output_report/forum_mining_experience_20260913.md:321` 点名读取），不是冗余。

处置：**不动文件**，改为在 `reports/forum_alpha_research/` 记一条证据说明（出仓会破坏该引用）。
教训同 §8.5 铁律：结构性结论必须先用机器级证据核验。

## 5. 5 个测试失败：全部先于本轮存在，均与改动无关

按 §4 纪律逐个定性（**单独跑即复现**，排除共享状态争用）：

| 失败 | 根因 | 归属 |
|---|---|---|
| `test_no_naked_connect_outside_whitelist` | `tools/fields/skeleton_panel.py:97,105` 裸 `sqlite3.connect` | **P3-F**，并行会话未跟踪在途件 |
| `test_real_data_dir_backup_count_within_policy` | `data/` 实测 6 个 `*.bak_*` > 阈值 2 | 并行会话造了 4+ 备份 |
| `test_second_holder_times_out_degraded` | DB 写锁 | 并发/环境（全量跑才现，单独跑绿） |
| `test_live_holder_is_respected[src]` / `[toolkit]` | DB 写锁 | 同上 |

改动文件（`audit_structure.py` / `baseline.json` / `AGENTS.md` / `legacy/README.md` /
`test_audit_structure_s16.py` / 改名与迁移的报告）与 `01_store_db` 无交集。
`test_no_naked_connect` 那条是**好闸**：它逮到了我没动的真问题，佐证「不改别人在途件」的克制是对的。

## 6. 未做 / 留观

- **未提交任何改动**：§7 要求按主题切分提交、只提交自洽且可验证的改动。当前工作树混着并行会话的
  `kor_full_gate_candidates_20261009.md`（已 staged）、`data/` 备份、`skeleton_panel.py`，**不宜由我代为提交**。
- **P3-F 与 `data/` 备份数是并行会话的在途债**，需它们的主人处置；`skeleton_panel.py` 要么入库并登记
  `tools/README.md` + 改走 `wqb.db_conn`，要么移出 skill 引用。
- **存量 40 个命名欠债**：未回改（§8.13「存量不强制回改」）。建议随各自文件被触碰时顺手改（改一个从基线移一个）。
- 第二轮明确「不做」的两项（`reports/` 子目录风格、`output_report/` 分区）**维持不做**，触发条件不变。
