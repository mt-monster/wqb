# Brain Labs Data-Analysis Agent — 规范

> `alpha-template-labs-data-analysis` skill 调用的仿真前原始数据分析代理的规范。它只回答一个问题：
> **该数据集在 Stage 2 候选设计之前，是否存在 Python 原生优势？**
> 流程与「人工暂停点」以 [../SKILL.md](../SKILL.md) 为准；本文只写输入 / 输出契约与字段形态分类。
> 引擎实现：`world-quant-brain-mcp/labs_data_analysis_agent.py`（本文与之不一致时以代码为准，并修本文）。

## 1. 目的

在 Brain Labs 里检查 USA/TOP3000/D1 的 MATRIX 数据集：覆盖 / 缺失 / 频率 / 离群值 / 相关性，把发现转成 Python 原生抽取机制。它是仿真**之前**的研究步骤，产物是线索，不是可提交的 alpha。

## 2. 输入

- `dataset_id`（如 `imbalance5`）
- `region` / `universe` / `delay`（缺省 USA / TOP3000 / 1）
- `fields`：至多**两个 MATRIX 字段**（VECTOR / GROUP 字段不进 Python 设计，仅 Python 轨道）

## 3. 诊断项（Labs 里跑）

覆盖（非 NaN 占比，按日）· 缺失（模式，不只是条数）· 真零 vs 哨兵值 · 更新频率 · 离群值 / 分布形状 · 换手 proxy · 字段相关性（与候选 peer 字段）。

## 4. 字段形态分类（引擎 `classify_field`）

| `field_classification` | 判据（摘要） | 抽取倾向 |
|---|---|---|
| `binary_or_categorical` | 近似取值数 ≤ 12 | 事件门 / 分组键，不做连续 rank |
| `low_frequency_step` | 覆盖 > 0.6 且日变化率 < 3% | 阶梯型：先回填，取「变化」而非水平 |
| `dense_bounded_score` | 覆盖 > 0.6 且值域约 [0,1] 且变化率 ≥ 3% | 有界分数：先验证状态切换，不直接吃水平值 |
| `sparse_event` | 零占比 > 80% | 事件型：单个事件衰减向量 + 触发条件 |
| `ratio_or_scale_sensitive` | \|p99 / p50\| > 100 | 尺度敏感：先 rank / 截尾再用 |
| `dense_continuous` | 其余 | 常规 zscore / rank |

判据数值以引擎为准（`classify_field`）；这里的表述只用于选抽取倾向。

## 5. 硬规则

- 不调用 `submit_alpha`；不仿真（除非用户明确要求进入 Stage 3）。
- 引擎内置合规约束：拒绝价量字段与直接市场数据字段（价格 / 收益 / 市值 / 股本 / 成交量），命中标 `diagnostic_only`。
- 不用 VECTOR / GROUP 字段做 Python alpha 设计（仅 Python 轨道）。
- 不照抄论坛公式（论坛只用于诊断、字段方向、失败模式、预处理线索）。
- 最终推荐 = 一个机制、至多两个 MATRIX 字段。
- 与 WebDataScope 离线体检交叉验证：一致 ⇒ 高置信；不一致 ⇒ 以 Labs 实时数据为准。

## 6. 输出契约（`ingest` 生成的 artifact 的主要键）

```json
{
  "dataset_id": "imbalance5",
  "labs_metrics": {"imb5_score": {"coverage_by_date": {"mean": 0.91}, "zero_ratio": 0.0}},
  "field_classification": {"imb5_score": "dense_bounded_score"},
  "constraint_checks": {"violations": [], "artifact_decision_use": "production_decisive"},
  "preprocessing_actions": [],
  "alpha_optimization_plan": [{"priority": 1, "candidate_family": "score_transition_without_market_data_context"}],
  "accepted_mechanisms": [{"field": "imb5_score", "decision": "accept", "reason": "…"}],
  "rejected_fields_or_mechanisms": [{"field": "imb5_mktcap", "decision": "reject", "reason": "…"}],
  "python_alpha_implications": ["…"]
}
```

- 键名以引擎实际输出为准；`constraint_checks.violations` 为空时 `artifact_decision_use` = `production_decisive`，非空则降为 `diagnostic_only`。
- 缺省输出路径 `tracking/runs/<ts>_labs_data_analysis_<dataset_id>.json` 会被 git 跟踪；建议用 `--output tracking/_scratch/…` 指向不入库的目录。这是**一次性分析输出**，不是战役产物，不入 DB，下游不读取。 <!-- lint:counterexample: 同上：缺省输出路径，文档正是在说明「别用这个目录」 -->
