# Wave R2 派发记录（组合结构 · 与 R1 并行双构型）

- 理由：论坛 risk70 帖实测「单字段直用最高 S0.41」⇒ R1（单字段直用）预期弱；R2 走**组合结构**独立路线
- R1 仍在飞（progress 0.1）；Wave5b（旧 SM 目标 news18）已 COMPLETE 释放槽位 ⇒ 并发 2/2
- 不属铁律 G 违规：R2 不是 R1 的参数微调，而是「单字段 vs 组合结构」两条并行探针线

## 8 条（R2-01..R2-08）
1. 风险调整特异收益（dsrt/√srisk）反转
2. 风险收缩幅度 srisku−srisk
3. risk88 纯残差 ts_decay_linear 反转（论坛「时序衰减」）
4. risk88 纯残差 5 日均反转（论坛「纯残差更适合均值回归」）
5. 风险调整反转 ts_zscore 66
6. 流动性门控残差反转（论坛「剔薄流动性」）
7. risk59 借券费率 vs DTC 价差
8. 特异风险低波

- multisim: `so5Rb8b34yy9yPdZVdLY0g`
- location: https://api.worldquantbrain.com/simulations/so5Rb8b34yy9yPdZVdLY0g
- 设置：KOR/TOP600/D1 · STATISTICAL · decay4 · trunc0.08
