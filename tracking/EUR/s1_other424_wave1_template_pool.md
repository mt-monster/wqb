# EUR × other424 · W1 模板池（2026-11-09，复活复查波：FHP 式路径 3）

> 转类依据：残池清空后按「死因=几何级/未判死」筛选的复活候选——other424 画像 ✅「A1 适用」但从未判死/深挖；OTHER 塔 ×1.5（2/3 差 1）。
> 3 字段全 MATRIX：dividend_growth_factor_score（GRID 预测股息增长，aC49）/ oth424_divyld（股息率，aC95）/ oth424_mktcap（市值，aC36，规范化/门控用）。
> 机制：股息增长预测 = 可证实的管理层信号（非注意力族，prod 风险结构不同于 sentiment26）；股息率 = value 收益源。
> 设置 TOPCS1600/SUBIND/decay4。判读：近闸臂 → 立即族代表 prod 预判（FHP 教训）；全波 |S|<0.5 → 整集归档。
> 覆盖：3/3 字段全覆盖（10 式）；模板 10 结构（level-z×2 轴/动量×2/rank/整形栈/门控/mktcap 对照）——小字段集结构空间有限，10 式已穷尽合法结构。

| # | 结构 | 表达式 |
|---|---|---|
| 1 | GRID country level-z | group_zscore(dividend_growth_factor_score,country) |
| 2 | GRID industry level-z | group_zscore(dividend_growth_factor_score,industry) |
| 3 | GRID 动量 | ts_delta(dividend_growth_factor_score,22) |
| 4 | GRID 分位 | ts_rank(dividend_growth_factor_score,66) |
| 5 | GRID 整形栈（ATOM 席位栈） | rank(hump(winsorize(group_zscore(dividend_growth_factor_score,country),std=2),hump=0.002)) |
| 6 | divyld country level-z | group_zscore(oth424_divyld,country) |
| 7 | divyld 动量22 | ts_delta(oth424_divyld,22) |
| 8 | divyld 动量5 | ts_delta(oth424_divyld,5) |
| 9 | 大盘门控 GRID | trade_when(greater(rank(oth424_mktcap),0.2),group_zscore(dividend_growth_factor_score,country),0) |
| 10 | mktcap 水平对照 | group_zscore(rank(oth424_mktcap),country) |
