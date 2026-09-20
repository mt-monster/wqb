# tools/legacy/ — 已完成的一次性脚本归档区

本目录存放**已跑完、无外部引用**（repo 内 refs=0）的一次性/批量脚本。
归档是**移动而非删除**：文件仍在版本库、git 历史完整保留，需要时可直接调用。

## 归档判据（三条同时满足）
1. 脚本本身是 `backfill_*` / `migrate_*` / `triage_*` / `submit_<alpha_id>*` 一次性类型；
2. `grep -rl <basename> --include="*.py" --include="*.md" --include="*.json"` 全库命中数 = 0
   （即没有任何模块 import、文档指引、JSON 配置引用它）；
3. 不属于平台闸门/生成链路/相关性落库等**持续复用**工具。

> 注意：`submit_batch.py`（refs=106）、`submit_verdict.py`（refs=60）等高频脚本**不得归档**，
> 它们由 skills 与 `src/wqb` 直接依赖。

## 当前归档清单（2026-09-20，14 个文件）

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

## 恢复方式

```bash
git mv tools/legacy/<file>.py tools/<file>.py   # 重新挂回活跃区
```

移出后需重新用上面的判据核查引用，并同步更新本索引。
