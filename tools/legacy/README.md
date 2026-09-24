# tools/legacy/ — 已完成的一次性脚本归档区

本目录存放**已跑完、无外部引用**（repo 内 refs=0）的一次性/批量脚本。
归档是**移动而非删除**：文件仍在版本库、git 历史完整保留，需要时可直接调用。

## 归档判据（二选一，2026-09-25 扩展）

**判据 P（一次性脚本，同前）** —— 三条同时满足：
1. 脚本本身是 `backfill_*` / `migrate_*` / `triage_*` / `submit_<alpha_id>*` 一次性类型；
2. `grep -rl <basename> --include="*.py" --include="*.md" --include="*.json"` 全库命中数 = 0
   （即没有任何模块 import、文档指引、JSON 配置引用它）；
3. 不属于平台闸门/生成链路/相关性落库等**持续复用**工具。

**判据 D（纯死模块，2026-09-25 新增）** —— 三条同时满足：
1. 全库 **import 数 = 0**（用 `logs/_tmp_refscan.py` 的 token 级计数，非子串 grep）；
2. **既无 `__main__` 守卫也无 argparse 入口** —— 即它是库模块而非可独立运行的 CLI 工具，
   落到本目录等同删除功能，不存在"人工按需调用"的漏判；
3. mtime 距今 ≥ 7 天（排除并发会话在飞的近期产物）。

> **关键教训（务必先读再做）**：「refs=0」≠「死代码」。多数 `tools/*.py` 是**命令行工具**，
> 自然不会被任何模块 import（如 `field_axis.py`、`combo_precheck.py`、`discover_datasets.py`），
> 它们只是没被 README 登记。**只有同时缺 `__main__` 入口才算真死代码。**
> 反例：`tools/pipeline_integration.py` 被 grep 到，但命中处是 `diversity_extract.py` 里的
> **ledger key 字符串** `pipeline_integration_{dataset}`，不是 import —— 子串匹配会系统性高估引用，
> 必须用 token 级计数 + 人工确认。

> 注意：`submit_batch.py`（refs=106）、`submit_verdict.py`（refs=60）等高频脚本**不得归档**，
> 它们由 skills 与 `src/wqb` 直接依赖。

## 当前归档清单（2026-09-25，18 个文件）

### A. 零引用一次性脚本（13 个）

| 文件 | 类型 | 归档理由 |
|---|---|---|
| `backfill_2y_six.py` | 一次性回填 | refs=0，2Y Sharpe 回填已跑完 |
| `backfill_fingerprints.py` | 一次性回填 | refs=0，fingerprint 回填已跑完 |
| `migrate_campaign_state.py` | DB 迁移 | refs=0，campaign_state 迁移已完成 |
| `migrate_db_schema.py` | DB 迁移 | refs=0，schema 迁移已完成 |
| `migrate_field_validation.py` | DB 迁移 | refs=0，field_validation 迁移已完成 |
| `migrate_ideas_to_db.py` | DB 迁移 | refs=0，ideas 入湖已完成 |
| `submit_883wzj1w.py` | 单 alpha 提交 | refs=0，文件名即 alpha_id，专例脚本 |
| `submit_883wzj1w_writeback.py` | 单 alpha 回写 | refs=0，上一条的回写续作 |
| `triage_pass4_check.py` | 一次性分诊 | refs=0，PASS4 体检已出结论 |
| `triage_platform_status_sweep.py` | 一次性分诊 | refs=0，平台状态扫描已跑完 |
| `triage_salvage_neut.py` | 一次性分诊 | refs=0，中性化抢救已跑完 |
| `triage_salvage_top300.py` | 一次性分诊 | refs=0，TOP300 抢救已跑完 |
| `triage_softdelete_batch1.py` | 一次性分诊 | refs=0，软删批 1 已跑完 |

### B. 遗留重复实现（1 个）

| 文件 | 类型 | 归档理由 |
|---|---|---|
| `gate.py` | 遗留通用闸门（16KB） | 被 toolkit 的 `gate.py`（58KB，8 闸权威）取代；**代码零引用**——`tools/wave_gate.py:567` 经 `_TOOLKIT_CANDIDATES` 加载 toolkit 版，`unified_gate.py:134` 调 `tools/wave_gate.py`，全库无 .py 调用本文件。详见 `AGENTS.md §8.1` |

### C. 纯死模块（4 个，2026-09-25 归档，判据 D）

| 文件 | 原位置 | LOC | 归档理由 |
|---|---|---|---|
| `death_level.py` | `src/wqb/death_level.py` | 89 | 唯一来自 `src/wqb` 包的零引用模块：无 import、无 `__main__`，drop-in 移除不影响任何调用链 |
| `calibrate_q3_alphas.py` | `tools/` | 116 | Q3 alpha 校准一次性脚本，无 CLI 入口，已无调用方 |
| `corr_batch_head_candidates.py` | `tools/` | 98 | 批量头部候选相关性脚本，无 CLI 入口，功能已被 `check_correlation` 链路覆盖 |
| `n1qmj_decorrelate_variants.py` | `tools/` | 143 | N1QMJ 去相关变体生成，无 CLI 入口，该 alpha 已结案 |

### D. 已彻底回收（2 个，2026-09-25，回收站可恢复）

| 文件 | LOC | 处理理由 |
|---|---|---|
| `_align_batch_verdict.py` | 31 | **从未入库（untracked）**、无 import、无 `__main__` → 归档无意义（git 历史不可恢复），直接进回收站 |
| `_pyramid_map.py` | 161 | 同上；金字培层级映射草稿，未在版本库中 |

### E. 保留观察（不归档，2026-09-25 判定）

以下 5 个虽满足「refs=0」，但 **有 `__main__` 入口** 或 **近期有写入**，属「未登记的 CLI 工具」或
「并发会话在飞产物」，**不得归档**：

| 文件 | 保留理由 |
|---|---|
| `tools/triage_platform_status_sweep_v3.py` | mtime 2026-09-24 22:36，并发会话在飞，避免误删在写文件 |
| `tools/db_maintenance.py` | 有 `__main__`；且为 2026-09-20 17:15 落盘的一批 DB 维护 CLI，属未登记工具 |
| `tools/operator_diversity_analyzer.py` | 有 `__main__`，算子多样性分析 CLI，属未登记工具 |
| `tools/discover_datasets.py`、`tools/fix_db_residuals.py`、`tools/populate_external_fields.py` | 三个均以 2026-09-20 16:58 同批落盘（疑似同一次 DB 迁移），全部带 `__main__` CLI |

其余 CLI 类零引用工具（15 个）见 `reports/code_structure_survey_20260925.md` 的 Tier 2 治理项。

## 恢复方式

```bash
git mv tools/legacy/<file>.py tools/<file>.py   # 重新挂回活跃区
```

移出后需重新用上面的判据核查引用，并同步更新本索引。
