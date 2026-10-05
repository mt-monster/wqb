# diversity_extract.py：单数据集多样性榨取（可选工具，缺省流程不用）

> 合并自根目录三份说明（`DIVERSITY_EXTRACT_README` / `SUMMARY` / `QUICKSTART`，共 546 行，已归档到 `attic/toolkit_docs_20260929/`）与 gate-rules 里的旧小节。**一个工具一页。**

**什么时候用**：单个数据集已有信号（不是白纸），想在同一数据集内先把「字段 / 算子结构 / 参数」三个维度榨干，再决定进多数据集阶段。它**不是**「补变体凑数」的工具——RA 明令不得补参数变体凑数，`L3` 的参数变体只算**参数敏感性检验**，不能冒充独立机制。

## 用法

```powershell
& $WQ_PY "$TK/campaign.py" --campaign-dir tracking/<REGION> diversity-extract --dataset <ds> [--rounds 3] [--size 8] [--max-ppac 0.7]
# 跳过某一段：--skip-audit（用已有报告）/ --skip-generation（用已有表达式）/ --skip-ppac / --skip-evaluation
# --integrate-pipeline：把榨取产物接进 ra-pipeline 编排（可选）
```

本工具没有 `--dry-run` 开关；想只看审计，用 `--skip-generation --skip-ppac --skip-evaluation`。

## 四步流程

1. **深度审计**：字段按经济含义分组（valuation / growth / quality / momentum / sentiment / volatility / liquidity / size）、算子树分桶、参数空间映射，产出多样性潜力报告。
2. **分轮生成**：`L1` 字段多样性（不同经济含义的字段）→ `L2` 算子结构多样性（同字段不同算子：`ts_rank` / `ts_zscore` / `ts_delta` / `rank` / `zscore` / `quantile` …）→ `L3` 参数空间多样性（同结构不同窗口，**窗口只取 5 / 22 / 66 / 252**——旧值 10 / 20 / 60 / 120 / 250 无实测依据，2026-09-29 已收敛）。
3. **PPAC 矩阵**：基于回测结果算两两 PPAC，更新多样性矩阵（`--max-ppac` 缺省 0.7）。
4. **效果评估**：结构多样性（算子熵 / 结构相似度 / 新颖度 / 覆盖率）+ PPAC 多样性（平均 / 最大 / 低 PPAC 比例）→ 建议。

## 产物：只进 DB（没有 `candidates/` / `reviews/` 文件）

| 内容 | 落点 |
|---|---|
| 多样性潜力报告 | ledger 键 `diversity_<ds>` |
| PPAC 矩阵 | ledger 键 `diversity_matrix_<ds>` |
| 效果评估 | ledger 键 `diversity_evaluation_<ds>` |
| 各轮表达式 | `expressions` 表（TAG = D01 / D02 / D03 …） |

键契约见 `docs/ledger_keys.json`。生成的表达式**仍要走闸**（`wave_gate`），和 `build_wave` 的产物一样。

## 建议怎么读（`evaluation.recommendation`）

| 值 | 条件 | 含义 |
|---|---|---|
| `enter_multi_dataset` | 总表达式 ≥ 15 且低 PPAC 比例 ≥ 0.7 且新颖度 ≥ 0.8 | 单集榨取充分，可进多数据集阶段 |
| `continue_extraction` | 总表达式 ≥ 10 且低 PPAC 比例 ≥ 0.6（其余中间态同样落这里） | 效果良好，再榨 1–2 轮 |
| `adjust_strategy` | 总表达式 < 5 | 调整生成策略或换数据集 |

阈值是代码里的经验值（`_lib/diversity_extractor.py::_make_evaluation`），不是平台规则。
