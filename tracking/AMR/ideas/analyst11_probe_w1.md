# analyst11 (ESG) 8 机制探针 — AMR wave s2_analyst11_d1

**Dataset**: analyst11
**Region**: AMR
**Delay**: 1


数据集：analyst11（MSCI ESG KPI），MATRIX（无需 vec_*），445 字段，245 零用户（冷门）。
设计原则（调研修订版 2026-09-28，论坛+开源文献融合）：
- 分组轴统一 **sector**：Analyst-ESG 子分类官方推荐 SECTOR/INDUSTRY 中性化（论坛 36224596669335），
  而非跟 win 的 subindustry；ESG 评分有 size/sector 偏差，sector 分组消结构差异。
- ESG 动量**短窗优先**（22/66）：MSCI 研究 ESG Momentum>Tilt（年化主动 2.2% vs 1.1%），
  1/3/6 月窗最强、12 月窗脆弱（tilt 超额 2/3 集中最后两年=水平效应混入）。
- 时序机制裹 `ts_backfill(F, 66)`：ESG 覆盖仅 0.54–0.78，~21% 公司从未评级（论坛 34421736616855）。
- **规避 `ts_entropy`（幽灵算子，不在 operators_verified.json）**，ESG 排名不稳定性用
  `ts_std_dev(group_rank(...), N)` 合法几何近似；`neg` 亦不合法，反向信号用 `subtract(1, ts_rank(x, N))`。
- 信号几何分化定律（analyst48 两轮 16 条实证）：价差/偏离几何活（S≈0.5），水平/动量/分歧度几何死——
  本轮动量/分歧机制是 ESG 文献强主张，专测该定律在 ESG 域是否失效。

**Concept**: ESG 总分的行业内相对水平——ESG 领先者在行业内的质量溢价（sector 对齐官方推荐）
- **Implementation Example**: `group_rank(ts_backfill({anl11_2_gse}, 66), sector)`
- **Rationale**: ESG 总分（E/S/G 平均）组内水平是 ESG 溢价文献基准机制（tilt）；sector 分组控制行业 ESG 结构差异（Analyst-ESG 官方推荐轴），backfill 填充评级缺失。

**Concept**: ESG 评级提升动量——3 月窗 rating change（短窗动量，文献最强窗）
- **Implementation Example**: `ts_zscore(ts_delta(ts_backfill({anl11_2_gse}, 66), 66), 252)`
- **Rationale**: ESG rating change 是文献最强预测机制；1/3/6 月窗动量最强（MSCI：动量年化主动 2.2% > tilt 1.1%），66 日 delta 捕捉季度评级迁移，长窗 zscore 剔水平效应（MSCI 数据水平效应会压过动量）。

**Concept**: ESG 评分稳定性溢价——做多稳定/做空波动（跨数据源稳健的新溢价源）
- **Implementation Example**: `subtract(1, ts_rank(ts_std_dev(ts_backfill({anl11_2_gse}, 66), 252), 252))`
- **Rationale**: Springer 2024：ESG 评分稳定性溢价（做多稳定/做空波动），跨 MSCI/Sustainalytics 数据源稳健；`ts_std_dev` 衡量评级波动，反向排序（neg 不合法，subtract(1, rank) 等效）使稳定者得高分。

**Concept**: 治理（G）分歧度——G 评级的行业内排名不稳定性（G 分歧独立定价 2.16% 年化）
- **Implementation Example**: `ts_std_dev(group_rank(ts_backfill({anl11_2g}, 66), sector), 252)`
- **Rationale**: 论坛实证：G 治理分歧单独有 2.16% 年化溢价而综合 ESG 分歧无定价效应；ts_entropy 是幽灵算子，`ts_std_dev(group_rank(...))` 是排名不稳定性（=市场分歧）的合法几何近似。

**Concept**: 治理分偏离价差——当前治理水平相对自身年度均值的价差（subtract 价差几何，analyst48 唯一活形态）
- **Implementation Example**: `subtract(rank(ts_backfill({anl11_2g}, 66)), rank(ts_mean(ts_backfill({anl11_2g}, 66), 252)))`
- **Rationale**: subtract 价差几何是 analyst48 全场唯一活形态（S=0.51）；治理分相对自身基准的偏离捕捉治理改善/恶化事件，剔除水平效应。

**Concept**: 区域-行业 ESG 竞争地位——平台预计算 region-sector 百分位（零成本横截面标准化）
- **Implementation Example**: `rank({anl11_creptcesgergse})`
- **Rationale**: 平台预计算的 region-sector 内 ESG 百分位排名已含行业调整，直接 rank 作相对 ESG 地位信号；users=1 极冷门，拥挤度最低。

**Concept**: 社区投资（CIT）pillar 异常——冷门 pillar 的横截面信号（Citizenship/慈善/人权维度）
- **Implementation Example**: `group_rank(ts_backfill({anl11_cit_totalcor}, 66), sector)`
- **Rationale**: CIT 是 ESG 最少被定价的 pillar（users=2），hybrid score 多 KPI 加权；冷门 pillar 拥挤度最低，机制多样性需要；sector 分组对齐官方推荐轴。

**Concept**: 员工（EMP）pillar 改善——员工待遇/多样性的短期改善信号（短窗修正）
- **Implementation Example**: `ts_zscore(ts_delta(ts_backfill({anl11_2pme}, 66), 66), 252)`
- **Rationale**: EMP pillar（薪酬/员工满意度/多元）改善与人力资本回报相关；修正因子文献：3 月滚动修正是最强窗（top-bottom 年化 5–6.7%），66 日 delta 捕捉短改善事件，长窗 zscore 标准化。