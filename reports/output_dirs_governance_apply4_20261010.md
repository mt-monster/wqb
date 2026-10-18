# 输出目录治理 · 第四轮整改执行（2026-10-10）

> 承接 [`output_dirs_governance_review4_20261010.md`](output_dirs_governance_review4_20261010.md)。
> 用户批准「**落地所有治理建议**」+「给出文件分类归纳完整方案」。本文件是执行记录。
> 与前几轮不同的一点：执行中**发现并处置了一起 76 文件误删事件**（§3），并**修正了复核报告的两条建议**
> （§4：P2-6 的前提被证据推翻、`PPA_USA` 是有意保留）——照 §8.5 纪律，结构性结论必须以机器证据为准。

## 1. 执行结果

| 项 | 处置 | 状态 |
|---|---|---|
| **P0-1** 根目录 19 散件 | 全部归位 `logs/_tmp_*.py`（用户选「立即归位」，明知 `_prod3.py` 在跑） | ✅ S7 转 OK |
| **P0-2** `deu_t4_targets.json` 缺日期 | `git mv` → `deu_t4_targets_20261010.json` + 引用同步 | ✅ |
| **P1-3** 带杠命名复发根因 | SKILL.md 两处改 `tracking/robustness_YYYYMMDD.md` + sync 6 安装位 + **指令源守护测试** + 在途件改名 + 台账 report_path 更正 | ✅ 复发链路三层全堵 |
| **P1-4** 产物目录混 .py 无闸 | S16 **规则⑤**（跟踪 FAIL / 在途 WARN）+ 测试；`diff_t4.py` 迁 `reports/diff_t4_20261010.py`（S5 豁免登记）+ AGENTS.md §8.12 同步 | ✅ |
| **P2-5** `.clinerules/skills` 误报 | `doc_path_refs --update-baseline` 豁免登记（基线 BROKEN 1） | ✅ |
| **P2-6** 基线同步 | ⚠ **修正后执行**：不做 S11/S14 冻结（前提被推翻，见 §3）、`PPA_USA` 不清（有意保留，见 §4） | ✅ 按事实收敛 |
| **P3-7** 存量 40 | 不动（触碰即改的棘轮制） | ✅ 维持 |
| 分类方案 | `docs/governance/output_dirs_taxonomy.md`（长期规范）+ `docs/README.md` 索引 | ✅ |

## 2. P0-1：19 个根目录散件归位

全部是并行会话（GBR 提交前流程）的在途探针脚本，逐个核实后按 §8.13「一次性脚本 → `logs/_tmp_*.py`」归位：

```
_diag2..8.py / _diag_macro.py  → logs/_tmp_diag{2..8}.py / _tmp_diag_macro.py   # 平台字段诊断
_fields_multi.py / _fields_of.py / _macro_datasets.py → logs/_tmp_fields_*.py 等
_prod2.py / _prod3.py / _prod_check.py → logs/_tmp_prod*.py                     # prod 相关性检查（在跑）
_simchk.py / _simst.py / _tower.py / _tower2.py → logs/_tmp_sim*/_tower*.py      # 仿真状态/点塔
harvest_wave.py → logs/_tmp_harvest_wave.py   # 与外部主副本 wqb-scripts/gbr_probe/ 同源的会话副本
```

- 归位时 `_prod3.py` 有两个进程在运行（Python 已加载脚本，搬移不中断执行）；并行会话的**后续调用会按旧路径失败**。
  已在 `.workbuddy/memory/2026-10-10.md` 尾部追加交接注记（新路径清单），供该会话查阅。
- 根目录现存 `.py` 仅 `conftest.py` / `wqb_db_mcp.py`（均白名单）→ **S7 转 OK**。
- `logs/_tmp_*` 属 gitignore 运行区、retention 到期回收 —— 与「一次性脚本用完即删」的语义一致；
  若后续证明某件有复用价值（如 `harvest_wave.py`），再按 §6 纪律工具化进 `tools/`（登记 README + THEMES）。

## 3. ★ 执行中的意外发现：76 个 tools/ 脚本误删事件（已恢复）

复核时 S11/S14 报「76 个已不在顶层/已不存在」，**复核报告把它归因为「迁移成功但基线没同步」（P2-6）——这个前提是错的**。执行时逐项核实：

- 抽样 5 个（`ab_test_framework.py`/`backfill_catalogs.py`/`combo_precheck.py`/`waiver.py`/`region_status.py`）
  在 `tools/` 全树（含 legacy、attic、仓库全域）**均不存在**，非「下沉到主题目录」；
- `git status` 显示 76 个 ` D`（**未暂存**删除——索引仍在跟踪），staged 的 `THEMES.json` 改动仅 +1 行注册，与迁移无关；
- 决定性证据：全量 pytest 收集期 **9 个 ModuleNotFoundError**（`test_shape_quota.py` import `shape_quota_check`、
  `test_cluster_variants.py` import `build_cluster_variants`……）——**这些脚本有活跃测试在用，删除是误删**。

**处置**（按 S14 报文「若是误删就从 HEAD 取回」）：精准 `git checkout -- <76 个删除路径>`，
只恢复删除项、不碰任何在途修改（含本次治理改动）。恢复后 9 个收集错误消失。
**未做基线冻结**：`--freeze-tools-top` / `--freeze-unregistered` 会把这 76 个从基线抹掉——
若不是恢复而是冻结，误删信号就被洗白、文件将永久缺位（HEAD 之外无人再记得它们）。
留观：删除方（未知会话/工具）若有意清理，应走 `git rm` + 归档 `attic/` + 基线同步的完整链路，而不是工作树裸删。


## 4. 对复核报告的两处修正（证据优先，§8.5）

1. **`PPA_USA` 白名单不清**。复核 P2-6 建议清理 `NON_REGION_DIRS` 的 `PPA_USA` 残留。查证：
   `.workbuddy/memory/2026-10-06.md:3825` 明载「白名单是**防 FAIL 保险**，删掉会把「运行期目录复现」
   从良性 WARN 变成 FAIL，故保留」，且 `tools/ppa_handoff.py` 仍会写 `tracking/PPA_USA/`（目录可复现）。
   ⇒ **有意保留，不清理**；S13 该条 WARN 属设计内噪音。
2. **S11/S14 不冻结基线**。原建议假设「迁移成功未收基线」，实际是误删事件（§3）。
   冻结会把误删从「可恢复的异常」变成「被基线认可的常态」。误删恢复后两条 WARN 自行消失。

## 5. P1-3：复发 3 次的带杠命名——三层堵死

| 层 | 修前 | 修后 |
|---|---|---|
| **指令源** | `brain-alpha-robustness/SKILL.md:30,110` 写死 `tracking/<日期>_robustness.md` / `tracking/YYYY-MM-DD_robustness.md` | `tracking/robustness_YYYYMMDD.md`；`sync_skills.py --apply` 同步 6 安装位（`--check` 全绿） |
| **磁盘产物** | S16 WARN 预检（事后） | 保留；在途的 `tracking/2026-10-10_robustness.md` 已改名 `robustness_20261010.md` |
| **台账** | `GBR::robustness_3qVP6pNO.report_path` 指向旧名 | merge 模式更正为新名（只改该键，不动其他字段） |

新增守护测试 `tests/unit/07_docs_skills/test_skill_no_hyphenated_report_paths.py`：
全量扫 `Claude/skills/**/*.md` 的带杠日期路径模式（正则对现有语料实测零误报）+ 点名守
robustness skill 的模板串。**S16 守产物（事后），该测试守指令源（事前）**——复发循环的两头都断。

## 6. P1-4：S16 规则⑤（产物目录不得混入脚本）

- `_s16_script_hits()`：扫 `output_report/**/*.py`，按 git 跟踪态分岔——**跟踪 FAIL / 在途 WARN**
  （与命名预检同一取舍：在途文件不该拦别人提交，但写盘即见）。
- `diff_t4.py` 迁 `reports/diff_t4_20261010.py`：它是 `deu_field_name_verification_20261010.md`
  点名的**可重跑证据脚本**，与 `dryrun_chain_runner_*` 同语义 → `S5_EXEMPT_PREFIXES` 登记豁免（写明理由）。
  报告内 3 处引用已同步（含改名说明）。
- AGENTS.md §8.12 S16 段同步规则⑤（措辞不引具体旧路径，避免制造新死指针——首版就踩了，已修）。
- 测试：`test_output_report_scripts_are_caught`（注入跟踪/在途各一验证分岔 + 真实仓库自检为 0）。

## 7. 分类方案（长期规范）

`docs/governance/output_dirs_taxonomy.md`：① 目录职责总表（每类文件的唯一去处 + 守闸 + 反例）；
② 命名即分类（`output_report/` 平铺的决策理由与前缀读法）；③ 存量欠债棘轮策略；
④ 闸门映射表（规矩 → 闸 → 语义）；⑤ 例外登记流程（先例 `campain` / 机器产物的处理路径）。
`docs/README.md` 索引已更新（S9 守声明目录存在）。

**明确维持不做**（与二、三轮一致）：`output_report/` 物理分区、`reports/` 子目录风格统一。
触发重新考虑的条件已写进方案：出现「找不到报告」的实际投诉，或单目录突破 400 件。

## 8. 验证读数

```
[audit_structure] FAIL=0 WARN=4（WARN= S16 基线存量 40 / S6 漂移 4 组 / S1 sys.path 存量 / S13 PPA_USA 有意保留）
[doc_path_refs]   BROKEN 基线 1（.clinerules/skills 外部搜索路径误报，已豁免登记）｜ UNTRACKED 0
[sync_skills]     全部安装位与仓库一致（6 位）
[pytest tests/]   4 failed, 3159 passed, 23 skipped（234.8s）
```

4 个失败逐个定性（§4 纪律：先看单跑绿不绿）：

| 失败 | 单跑 | 归属 |
|---|---|---|
| `test_second_holder_times_out_degraded` | ✅ 6 passed（与下面两个合跑） | DB 写锁共享争用（全量跑才现，已知环境形态） |
| `test_live_holder_is_respected[src]` / `[toolkit]` | ✅ 同上 | 同上 |
| `test_no_naked_connect_outside_whitelist` | ❌ 单跑也红 | **并行会话在途债**：`tools/fields/skeleton_panel.py`（5 处）+ `tools/gates/operator_coverage_audit.py`（1 处）裸 `sqlite3.connect`——第三轮 apply 已报过 skeleton_panel 同款，非本次改动集（本次零 sqlite 写入），修法是改走 `wqb.db_conn` |

本次改动文件（`audit_structure.py` / 两个测试文件 / `AGENTS.md` / `docs/` 两件 / SKILL.md+安装位 / 报告与改名件）
与 `tests/unit/01_store_db/` 无交集；新增的两个测试文件全绿（24 passed 含参数化）。

## 9. 未做 / 留观

- **未提交任何改动**：工作树混着并行会话的在途产物（`A` 状态的 DEU/GBR 报告等），按 §7 纪律不代提交；
  本次治理改动清单见 §1，可作为独立提交主题。
- `logs/_tmp_*.py` 19 件属 gitignore 运行区，随 retention 到期回收；有复用价值者届时再工具化。
- 76 误删事件的**责任方未定位**（未知会话或某清理工具）；建议观察是否复发——若复发，
  应给清理类工具加「tools/ 受控文件」保护名单（独立任务）。
- `reports/diff_t4_20261010.py` 未跟踪（与被它引用的两个 json 一样属运行证据）；入库与否随
  `deu_field_name_verification_20261010.md` 的提交批次走。
