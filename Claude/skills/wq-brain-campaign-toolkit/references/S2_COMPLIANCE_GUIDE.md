# S2 合规记录与检查清单（**提示级，不阻断**）

> 2026-09-29（skills 审查 RA-76）：本文旧版把 `pipeline.py run` 写成「强制校验 `s2_compliance_w<wave>`、缺失中止、`--force` 逃生」——那是 **2026-08-26 ~ 09-15** 的行为。
> 2026-09-15（降级 ⑥）起：缺记录只打印一行提示，**不中止、不需要 `--force`**。以代码为准：`scripts/pipeline.py` 的 `_check_s2_compliance` 调用处（「S2 合规记录：仅提示，不再中止」）。

## 现状一句话

| 路径 | 行为 |
|---|---|
| `pipeline.py run`（跑批入口） | 有记录 → 打印 `[S2-COMPLIANCE] 记录存在: …`；没有 → 打印 `[S2-COMPLIANCE] 无合规记录（仅提示，不阻断）: …`，**继续往下跑** |
| 工作流预检节点（`src/wqb/workflow/nodes/campaign.py`，预检通过后） | 记录缺失且 S1 台账 `s1_<dataset>_d1` 有 `ideas_md_path` → **自动补录**（`candidate_pool_source=skill`，`notes` 写 `auto-marked by preflight`）；补录失败只记警告 |
| `campaign.py s2-mark`（= `scripts/s2_compliance_mark.py`） | **可选**的手工标记；写 `ledger_kv` 的 `s2_compliance_w<wave>`（键目录见 `docs/ledger_keys.json`） |

## 为什么降级（证据）

- 校验只验「有一条台账指向一份文档、文档含『字段 / 特征 / 建议』三个词、来源标记为 `skill`」，**不验内容**；文档本身由确定性模板渲染（8 问框架），对表达式质量零贡献。
- 手工批（GEM Mode B 等）没有特征工程文档，旧硬闸只能靠 `--force` 绕过——**闸变成了每次都要绕的仪式**。
- 真正保障「字段白名单 / 类型 / 不可访问算子」的是 **typed catalog**（`stage_gate` 缺目录会 FAIL），不是这条记录。

## 检查清单（自查，仍可用）

`references/S2_COMPLIANCE_CHECKLIST.md`：进入 S2 前的自查模板（是否基于 `brain-data-feature-engineering` 的输出构建候选、字段 / 窗口 / 中性化各写了理由）。
它是**给 agent 的自我提醒**，不是机器闸；勾选与否不影响 `pipeline.py` 的行为。

## 想留一份可审计的记录时（可选）

```bash
# 1. 特征工程文档（brain-data-feature-engineering 产出）
#    例：tracking/KOR/feature_engineering_kor_streetaccount1_20260826.md
# 2. 写入合规标记
$WQ_PY campaign.py --campaign-dir tracking/KOR s2-mark --wave 36 \
    --doc-path tracking/KOR/feature_engineering_kor_streetaccount1_20260826.md \
    --candidate-pool-source skill --notes "brain-data-feature-engineering 生成"
```

- `s2-mark` 自己的 `--force` = **覆盖已存在的记录**（重复标记同一波会拒绝），与 `pipeline.py` 的 `--force` 无关。
- 手工构建候选池就如实写 `--candidate-pool-source manual`——现在它不会被拦，只是留下事实。

## 别把两个 `--force` 弄混

`pipeline.py run --force` 只越过**配额闸**（提交配额耗尽时继续，会用光当日额度）与 **universe 判死规则**闸；**与 S2 合规无关**。细节见 [`poll-and-quota.md`](poll-and-quota.md)。

## 文件

| 文件 | 说明 |
|---|---|
| `references/S2_COMPLIANCE_CHECKLIST.md` | 自查模板 |
| `scripts/pipeline.py::_check_s2_compliance` | 只读校验，结果仅打印 |
| `scripts/s2_compliance_mark.py` | 手工标记（`campaign.py s2-mark`） |
| `src/wqb/workflow/nodes/campaign.py`（预检节点） | 预检通过后自动补录 |

## 版本

- **2.0**（2026-09-29）：与 2026-09-15 降级对齐；删除「硬闸 / 逃生阀 / 故障排查」三节（对应的报错已不存在）。
- 1.0（2026-08-26）：初版（两层防御：清单 + `pipeline.py` 硬闸）。
