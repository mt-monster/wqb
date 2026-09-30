# USA / analyst7 / D1 / TOP3000 机制优先 ideas（wave85：coverage 流 + 分歧状态，8 探针快判死）

**Dataset**: analyst7
**Region**: USA
**Delay**: 1

背景：analyst7 为 untried 新集（USA 零回测），按 8 探针快判死预算执行。跨区先验 MEA:12 RA-clean。死路约束（勿触）：修订宽度（raised/lowerednum 比值）、forward E-P 收益率动量（prod 0.93）、评级修正（rec_* 饱和）、value/quality 水平、flash EPS revision；破壁须换信号类型（GLOBAL-CROSS-DATASET-SAME-DOMAIN-LOCK）。体检包约束：低覆盖（cr<0.4）字段必须 ts_backfill；zero_inflated 字段必须 trade_when 门控；单边恒正字段不做原始水平多空，用排名/变化/与基准差；窗口按更新频率取最小（quarterly≥252、monthly≥120，体检硬门强制）。字段全 MATRIX。反向取号统一 `scale(-rank())` 或 group_rank 正向（禁 reverse(rank())）。占位符 `{...}` 统一放在各示例末位字段处（模板前缀唯一，供 exposure 映射精确归属）。

**Concept**: 覆盖流扩张：分析师覆盖数同比上升 → 关注流入 → 中期延续（信号类型=注意力流量，非水平）
- **Implementation Example**: `group_rank(ts_delta(ts_backfill(est_q_ebs_num, 252), 252), bucket(rank(ts_backfill({est_q_ebs_num}, 252)), range="0,1,0.2"))`
- **Expected Exposure**: attention_flow
- **Rationale**: 覆盖变化是注意力流量（正交于估值/修正方向族）；按覆盖规模自身分桶内比较消规模效应救 sub（桶腿避开 zero_inflated 字段）；候选主字段 est_q_ebs_num

**Concept**: 注意力期限倾斜：12m 长线覆盖相对季度覆盖占比上升 → 长线资金关注加深
- **Implementation Example**: `group_rank(divide(ts_backfill(est_12m_ebs_num, 22), ts_backfill({est_q_ebs_num}, 22)), subindustry)`
- **Expected Exposure**: attention_flow
- **Rationale**: 长短端覆盖比是注意力结构（比值几何，非加权拼腿）；两腿均低覆盖故 ts_backfill；候选主字段 est_12m_ebs_num

**Concept**: 注意力期限倾斜（差分几何对照）：同机制换 rank 差结构，检验比值几何是否为构造伪象
- **Implementation Example**: `group_rank(subtract(rank(ts_backfill(est_12m_ebs_num, 22)), rank(ts_backfill({est_q_ebs_num}, 22))), subindustry)`
- **Expected Exposure**: attention_flow
- **Rationale**: subtract(rank,rank)=与基准差（合规价差形态）；与上一条构成同机制双几何对照；候选主字段 est_12m_ebs_num

**Concept**: 分歧状态（长窗）：分析师分歧度相对自身历史升高 → 不确定性状态 → 风险溢价/过度反应
- **Implementation Example**: `trade_when(not_equal(est_12m_ebi_std, 0), group_rank(ts_zscore({est_12m_ebi_std}, 252), subindustry), -1)`
- **Expected Exposure**: uncertainty
- **Rationale**: 分歧 regime 是状态信号（正交于修正方向/收益率动量）；zero_inflated 须 trade_when 门控；zscore=与自身基准差（恒正字段合规形态）；候选主字段 est_12m_ebi_std

**Concept**: 分歧状态（季度腿换腿）：同机制换季度口径分歧字段
- **Implementation Example**: `trade_when(not_equal(est_q_opr_std, 0), group_rank(ts_zscore(ts_backfill({est_q_opr_std}, 252), 252), subindustry), -1)`
- **Expected Exposure**: uncertainty
- **Rationale**: q 口径 opr 分歧度；quarterly 更新频率要求慢窗；候选主字段 est_q_opr_std

**Concept**: 分歧扩张速度：当前分歧高于 28 天前 → 不确定性正在扩张（变化量比水平更接近信息流）
- **Implementation Example**: `trade_when(not_equal(est_q_opr_std, 0), group_rank(subtract(rank(ts_backfill(est_q_opr_std, 252)), rank(ts_backfill({est_q_opr_std_28d}, 252))), subindustry), -1)`
- **Expected Exposure**: uncertainty
- **Rationale**: 双序 rank 差化解纯多头样本警告；28d 镜像字段提供真实变化轴；候选主字段 est_q_opr_std

**Concept**: 相对分歧（变异系数）：分歧/均值比 → 尺度无关的不确定性度量
- **Implementation Example**: `trade_when(not_equal(est_q_opr_std, 0), group_rank(ts_mean(divide(est_q_opr_std, abs({est_q_opr_mean})), 252), subindustry), -1)`
- **Expected Exposure**: uncertainty
- **Rationale**: CV=std/|mean| 剔除量纲（比值几何非拼腿）；252d 窗满足季度更新频率约束；候选主字段 est_q_opr_std

**Concept**: 慢快结构交互：慢覆盖流 × 快分歧排名（跨周期交互，win 配方结构；乘法交互非加权相加）
- **Implementation Example**: `trade_when(not_equal(est_12m_ebi_std, 0), multiply(group_rank(ts_delta(ts_backfill({est_q_ebs_num_28d}, 252), 252), subindustry), ts_rank(est_12m_ebi_std, 252)), -1)`
- **Expected Exposure**: attention_uncertainty_interaction
- **Rationale**: 慢变量提供 2Y 稳健性、快排名提供低相关（SLOW-X-FAST-MIX 铁律）；multiply 交互不含权重相加；慢腿用 28d 镜像腿（避免 est_q_ebs_num 复用超 max_field_repeat=3）；候选主字段 est_q_ebs_num_28d

生成约束：窗口只用 22/66/252/504/1008/1260 且按字段更新频率取最小（quarterly≥252、monthly≥120，体检硬门强制）；每条 1–2 个字段；禁止 add(A,B) 腿混合与加权混合；zero_inflated 字段必须 trade_when 门控且不做裸辅助腿；cr<0.4 字段必须 ts_backfill；禁用幽灵算子；不生成同字段窗口网格变体（8 探针预算）。
