# ASI 战役 ideas — 论坛帖子机制移植（2026-10-02）

**Dataset**: pattern_scores
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

**Concept**: V 形底部延续的形态相似度
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean({v_shape_continuation_bottom_median_similarity_40d}, 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: pattern_scores 集 29 个 L3.5 形态族，504 字段中 491 个 users≤9（冷门 97%，无竞争）。经济机制：形态相似度刻画市场微观结构对「V 形底部」模式的定价差异——形态被识别的程度决定后续资金流向。

---

**Concept**: 向上缺口突破的动态相似度（换 country 分轴）
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean({upward_gap_break_dynamic_similarity}, 22), country), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: 与上一条同集不同形态族（缺口突破 vs 底部延续），且换用 country 分轴。突破型形态的跨行业可比性弱于底部形态，按国别轴排序更合理——同时是对「不同机制应配不同分组轴」的检验。

---

