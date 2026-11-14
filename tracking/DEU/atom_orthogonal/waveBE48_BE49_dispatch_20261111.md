# BE48/BE49 派发记录（2026-11-11 10:0x）

| 波 | 数据集 | 臂数 | sim | 设置 |
|---|---|---|---|---|
| BE48 | institutions1 | 6 | 218THQ6H25iNcMjfFblkdVs | INDUSTRY/decay4/trunc0.08 |
| BE49 | insider_agg_matrix | 10 | 2gjOc31ty4Q7a18t2UO5Lha | 同上 |

臂设计（v2 L1 正交网格 + 论坛文献臂）：
- BE48: conviction 金额比(主)/股数比(姊妹)/subindustry 对照/无平滑对照/显著性加权/valueeur 三窗 max 归并
- BE49: conviction 单腿 industry/subindustry/高管版/directional 三窗 max/双腿 add/卖侧反向/净流量差/买卖占比/Δ 变化面/zscore 水平面

下一轮（BE50/BE51 预设计）：pattern_scores（LoMW 文献臂：形态成熟度 max-similarity、峰度做空）+ option1（Xing-Zhang-Zhao 文献臂：vec_stddev(vi) 微笑斜率、Δ66 IV 变化）。
