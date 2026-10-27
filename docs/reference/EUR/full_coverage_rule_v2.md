# EUR 全量覆盖口径 v2（维度级，2026-10-20 生效）

> 替代 v1「字段级 100%」。依据：21,928 个未测字段全测需 ≈65,800 次仿真 ≈ 91 天连续运行，
> 而其中约 34% 是同一信号的名称变体（去数字/窗口后期次后只剩 14,415 个基座）。

## 一、新规则（三条闸）

| 闸 | 口径 | 默认参数 | 失败后果 |
|---|---|---|---|
| **1. 维度覆盖闸** | 每个语义维度（`semantic_family`，字段数 ≥ N 的族）**至少被 1 条候选表达式触及** | `--dim-min-size 3` | FAIL |
| **2. 模板族闸** | 本数据集已试 ≥3 个结构模板族 | `--min-families 3` | FAIL |
| **3. 边界算子闸** | 表达式中算子的参数落在 `boundary_ops_eur.json` 合法档；近闸候选须试完 min_coverage 档 | — | FAIL |

**小数据集回退**：字段总数 ≤ max(10, 2×dim-min-size) 时，整集视为 1 个维度 ⇒ 等价于要求全部字段被触及（成本本来就低）。

## 二、字段级 100% 何时仍需

仅两种情况：

1. **近闸深挖**：某维度已出现「近闸候选」（cheap gate 过但 RA 未全过）⇒ 把该维度的同族字段穷尽
2. **判死**：数据集判死前，必须每个维度都实测过（`dim_coverage_bt = 1.0`），不是每个字段

```bash
# 近闸深挖：显式切回字段级
python tools/full_coverage_gate.py --region EUR --dataset <ds> \
  --exprs-file <cand>.txt --coverage-mode field --near-gate --gate-mode enforce
```

## 三、两条「覆盖」口径必须分清

| 口径 | 判定 | 用途 | EUR 现状（178 集） |
|---|---|---|---|
| **实测口径** `dim_coverage_bt` | 维度内 ≥1 字段 `n_tests>0` | **判死/升档的唯一依据** | 全维度过：**22 个（12%）** |
| **静态口径** `dim_coverage_static` | 维度内 ≥1 字段 `verdict != UNTESTED` | 仅作参考 | 全维度过：104 个（58%） |

⚠️ 静态口径虚高 82 个数据集——那些字段是「被判 UNUSABLE 但从未跑过回测」，**不算测过**。

## 四、可复用的量化口径

| 指标 | 公式 |
|---|---|
| 维度覆盖率 | `covered_dims / required_dims`（required = 字段数 ≥ dim_min_size 的族） |
| 数据集优先级 EV | `valueScore × avg_field_coverage × (n_untested/n_fields) / (1 + alphaCount/1000)` |
| 字段级冗余度 | `distinct_bases / n_fields`（去数字/窗口/期次后） |

## 五、命令速查

```bash
PY=./world-quant-brain-mcp/.venv/Scripts/python.exe

# 派发前：维度闸（新默认）
$PY tools/full_coverage_gate.py --region EUR --dataset <ds> \
    --exprs-file cache/_xxx.txt --campaign-dir tracking/EUR --gate-mode enforce

# 看某集缺哪些维度（JSON 里有 missing_dims + missing_sample_fields）
$PY tools/full_coverage_gate.py --region EUR --dataset <ds> \
    --exprs-file cache/_xxx.txt --gate-mode warn --json

# 全局维度覆盖盘点（实测口径）
$PY tools/query_profile.py dims --min-dim-cov 1.0

# 单集字段级明细
$PY tools/query_profile.py fields --dataset <ds> --untested
```

## 六、迁移说明

- **历史波不回溯**：v1 口径下的判死结论若只过了字段级闸，按 v2 需重判（静态口径虚高）
- **今日起的新波**：一律走 `--coverage-mode dimension`（默认），字段级降级为 INFO 提示
- **判死前必查**：`query_profile.py dims --min-dim-cov 1.0` 里必须有该数据集，否则不允许 seal_dead_end
