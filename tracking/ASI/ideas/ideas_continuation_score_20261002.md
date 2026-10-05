# ASI 战役 ideas — 论坛帖子机制移植（2026-10-02）

**Dataset**: continuation_score
**Region**: ASI
**Delay**: 1


> **格式说明**：`**Implementation Example**` 内必须是含 `{exposure_estimation_confidence_score}` 占位符的**模板**（GEM 注入真实字段），
> 具体字段由 GEM 从本数据集字段池按概念匹配。下方「本波拟用字段」仅作约束提示，不进模板。

## 来源机制（论坛实证，JB71859 2026-09-28，30 赞）

原帖骨架 `ts_target_tvr_decay(multiply(group_rank(模型预测, subindustry), group_rank(暴露置信度, country)), 0, 1, 0.028)`，Sharpe 2.70 / TVR 5.80%。

**机制内核（保留）**：两腿用**不同分组轴**组内排序（业务轴比同业 / 国别轴消化整体水平差），以**几何乘**非线性合成，最后用**目标换手算子**统一控速。

**本区移植约束**：模型腿字段属 `dl_riskfree_returns`，ASI 判死记录认定该集为**单座位**（5d/20d/60d 互相关 0.88-0.99）且已被 P02wbJAM 提交（prod 0.67）⇒ 模型腿不可照抄，改为**保留形态、更换信号腿**。`multiply` 属算子几何（非线性合成），不违反「禁止两腿加权相加」铁律；严禁退化为 `add` / 中缀 `+`。

**本波拟用字段（约束提示）**：`exposure_estimation_confidence_score`（披露置信度，VECTOR）、`exposure_estimation_precision_score`（披露精度）、`region_exposure_percent_maximum`（最大区域敞口，反向）、`customer_revenue_share_percent`（客户集中度，反向）。

---

---

**Concept**: 上升扇贝形态的延续强度
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean({upward_scallop_similarity_median}, 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: continuation_score 集 12 族、560 字段中 548 个 users≤9（冷门 98%）。扇贝形态（多波小幅上涨后加速）是趋势加速的经典图形，与缺口突破构成不同机制族。验证 PV 塔两个不同数据集是否都有效。

---

