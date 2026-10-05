# ASI 战役 ideas — 论坛帖子机制移植（2026-10-02）

**Dataset**: pv13
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

**Concept**: 暴露披露置信度的双轴几何合成 —— 披露质量 × 行业相对位置
- **Implementation Example**: `ts_target_tvr_decay(multiply(group_rank(winsorize(ts_mean(vec_avg({exposure_estimation_confidence_score}), 22), std=4), subindustry), group_rank(ts_mean(ts_backfill(vec_avg({exposure_estimation_confidence_score}), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)`
- **Rationale**: 论坛实证该骨架 ASI Sharpe 2.70。披露置信度高 = 业务边界清晰、可被同业比较，在细分行业内获得信息质量溢价；按 country 分轴消化国别间整体披露水平差异。前置 winsorize 修复原帖自认缺陷（字段页明写 must be winsorized）。VECTOR 字段须先 vec 聚合。

**Concept**: vec 聚合口径的归因对照 —— 收益来自评分水平还是覆盖记录数
- **Implementation Example**: `ts_target_tvr_decay(multiply(group_rank(winsorize(ts_mean(vec_avg({exposure_estimation_precision_score}), 22), std=4), subindustry), group_rank(ts_mean(ts_backfill(vec_sum({region_exposure_percent_maximum}), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)`
- **Rationale**: 原帖作者指出 vec_sum 混入「单元素评分高低」与「有效记录条数」两信息（2 个 0.8 求和 1.6 > 4 个 0.6 求和 2.4 但均分更低）。此条与上一条仅差 vec 聚合口径，可直接归因：差异大则长度信息有贡献，接近则评分本身主导。

**Concept**: 单腿剥离对照 —— 披露质量腿独立是否即有信号
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean(ts_backfill(vec_avg({customer_revenue_share_percent}), 252), 66), country), lambda_min=0, lambda_max=1, target_tvr=0.028)`
- **Rationale**: 原帖作者列出的第三个待验证缺陷——缺三分支拆分对照。若单腿已接近双腿强度，说明乘法只是换了一批股票而非真实改进；单腿显著更弱才证明几何乘有独立价值。本条为归因基线。

**Concept**: 披露估计精度腿 —— 置信度的姐妹经济量
- **Implementation Example**: `ts_target_tvr_decay(multiply(group_rank(winsorize(ts_mean(vec_avg({exposure_estimation_precision_score}), 22), std=4), subindustry), group_rank(ts_mean(ts_backfill(vec_avg({exposure_estimation_precision_score}), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)`
- **Rationale**: 精度（误差幅度）与置信度（可靠程度）同源不同经济量。按 L4 族内换经济量的合规方向（不换腿不加权），验证该族信号是否只集中在单一聚合维度——ASI 判死记录 `ASI-OTH36-SINGLE-MECHANISM-EXHAUSTED` 的教训正是「数据集不拥挤≠有多个可用信号」。

**Concept**: 区域敞口集中度腿 —— 收入绑定单一地区的风险（反向）
- **Implementation Example**: `ts_target_tvr_decay(multiply(group_rank(reverse(ts_mean(ts_backfill(vec_avg({region_exposure_percent_maximum}), 252), 66)), subindustry), group_rank(ts_mean(ts_backfill(vec_avg({region_exposure_percent_maximum}), 252), 66), country)), lambda_min=0, lambda_max=1, target_tvr=0.028)`
- **Rationale**: 最大区域收入敞口占比越高 = 收入绑定单一地区、地域集中风险越大，方向取反做多分散暴露者。属 pv13 族内 size_level 子类，与置信度腿（other 子类）不同经济机制，构成跨子类探针。

**Concept**: 单一客户集中度腿 —— 客户依赖风险（反向）
- **Implementation Example**: `ts_target_tvr_decay(group_rank(reverse(ts_mean(ts_backfill(vec_avg({customer_revenue_share_percent}), 252), 66)), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.028)`
- **Rationale**: 单一客户收入占比越高 = 客户依赖风险越大。该字段覆盖仅 0.3831 属稀疏字段，本条兼作覆盖率压力测试——若因覆盖不足触发 LONG_COUNT 闸，则该字段族整体判死。子行业轴单腿，避免与置信度腿重复机制。

---

**Concept**: V 形底部延续的形态相似度
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean({v_shape_continuation_bottom_median_similarity_40d}, 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: pattern_scores 集 29 个 L3.5 形态族，504 字段中 491 个 users≤9（冷门 97%，无竞争）。经济机制：形态相似度刻画市场微观结构对「V 形底部」模式的定价差异——形态被识别的程度决定后续资金流向。

**Concept**: 向上缺口突破的动态相似度（换 country 分轴）
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean({upward_gap_break_dynamic_similarity}, 22), country), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: 与上一条同集不同形态族（缺口突破 vs 底部延续），且换用 country 分轴。突破型形态的跨行业可比性弱于底部形态，按国别轴排序更合理——同时是对「不同机制应配不同分组轴」的检验。

**Concept**: 上升扇贝形态的延续强度
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean({upward_scallop_similarity_median}, 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: continuation_score 集 12 族、560 字段中 548 个 users≤9（冷门 98%）。扇贝形态（多波小幅上涨后加速）是趋势加速的经典图形，与缺口突破构成不同机制族。验证 PV 塔两个不同数据集是否都有效。

**Concept**: 信用结构违约概率反向 —— 信用风险溢价
- **Implementation Example**: `ts_target_tvr_decay(group_rank(reverse(ts_mean(ts_backfill({mdl28_sm_structural_credit_structural_pd_pct}, 252), 22)), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: model28 集 125 字段全部 users=0（零竞争），cov 0.974。1 年违约概率百分比越高风险越高故取反。经济机制是信用风险溢价：违约概率高者被市场过度惩罚，其后续收益更高。本条同时服务点塔目标——ASI/D1/model 当前 1/3 未点亮。

**Concept**: 违约距离腿 —— 资产安全垫的横截面定价
- **Implementation Example**: `ts_target_tvr_decay(group_rank(ts_mean(ts_backfill({mdl28_sm_structural_credit_structural_distance_to_default}, 252), 22), subindustry), lambda_min=0, lambda_max=1, target_tvr=0.05)`
- **Rationale**: 违约距离（资产价值超出违约点的标准差数，越高越安全）不取反，与上一条 pd 反向腿构成同族对照：两者 Sharpe 接近则信用风险在本区是单调因子；distance 显著更强则「安全垫」比「违约概率」更好定价。model 塔第 2 颗候选。

---

## 形态纪律（每批必守）

- 算子个数 **< 10**（项目铁律，`regular.operatorCount` 口径）
- **禁**任何 `add` / 中缀 `+` 组合两条独立信号腿；`multiply` 为允许的几何合成
- 时间窗口只用 `1 / 5 / 22 / 66 / 252 / 504 / 1008 / 1260`
- **探针先行**：每族先放 1 条，`|S| ≥ 0.5` 才扩批
- VECTOR 字段必须先 `vec_avg` / `vec_sum` / `vec_max` 聚合，禁止裸用
- MATRIX 预测类字段前置 `winsorize(x, std=4)`