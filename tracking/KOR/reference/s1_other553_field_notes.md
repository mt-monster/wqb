# KOR other553 字段理解与特征工程建议（S1/S2 合规补充文档）

数据集：other553（KOR/TOP600/delay1，VECTOR 21，cov 0.48-0.74 偏低，判定 PROBE）。
分析师预期修正三族：`est_*`（EPS 预期）、`ptg_*`（目标价）、`rec_*`（评级），`sal_*`（营收预期）。
VECTOR 型：每字段为分析师向量，聚合用 `vec_avg`；覆盖偏低处补 `ts_backfill`。

## 字段分类与理解

- **est 族（主信号候选）**：`est_estvalue`（当前一致预期）、`est_preestvalue`（前值）、
  `est_analyst`（覆盖分析师数）、`est_yearspeakcnt`（年内创新高次数）、`est_isprevspeak`。
  修正量 = `estvalue − preestvalue`，即初始信号；峰计数 = 进阶信号（动量持续性）。
- **ptg/rec 族（进阶信号）**：`ptgvalue/preptgvalue`（目标价现值/前值）、
  `recvalue/prerecvalue`（评级现值/前值）、`rec_yearspeakcnt`。
- **sal 族（辅助确认）**：`sal_estvalue/sal_preestvalue` 营收预期，与 est 族双信号确认。
- **字段角色**：est 修正 = 主信号；ptg/rec = 独立主信号候选；sal = 辅助确认（只进组合条件腿）。

## 特征工程建议

1. **修正幅度×置信**：`(estvalue−preestvalue)×(1−isprevspeak)`，非前高时修正更有效。
2. **双信号确认**：`ts_corr(est_estvalue, sal_estvalue, 22)` EPS 与营收预期同向协同。
3. **方向切换**：`if_else(修正>0, rank(est), −rank(est))` 上修做多/下修做空。
4. **事件门控**：分析师数 22 日增量 >0 时才持有目标价修正（覆盖扩张确认）。
5. **组内相对**：`group_rank(修正, industry)` 行业内相对强弱。
6. **预处理**：VECTOR 必裹 `vec_avg`；cov 偏低字段（ptg/rec）补 `ts_backfill(...,66)`；
   `quantile` 仅 1 参；预期暴露=分析师修正（earnings revision），与 KOR 有效面一致。

来源：brain-makeSomeGem（s2_nested）+ 本文档；候选池来源=skill。
