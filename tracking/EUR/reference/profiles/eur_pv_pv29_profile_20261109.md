# EUR × pv29 字段画像（2026-11-09）

> 80/80 全量（complete=true）；Derived Industry Classification（统计聚类行业分类）
> 塔位：PV(×1.1)；拥挤度：aC 165 / uC 109；os_is 0.2973

## 一、字段结构
全部为**统计聚类分组字段**：industry_grouping_level{2,5,10,20,50,100}_{universe}_variant{NNN}——按收益协方差把股票聚成 2/5/10/20/50/100 类，覆盖各宇宙（top100-top1200/all）。MATRIX 版 cov 0.93-1.0，GROUP 版 cov 0.08-0.48（TOP200 小宇宙版）。

## 二、判定
1. **GROUP/MATRIX 分组字段，不是信号字段**——只能作 group_* 算子第二参数（分组轴）
2. **已实测判死**（2026-10-18 修订）：pv29/pv30 聚类轴作分组对 prod 无效（KPmnqaGg prod 0.926 高于基线，S/2Y/robust 全面劣化）——「换轴不是 prod 杠杆」
3. **判定：结构性排除**（分组轴原料，非信号；换轴实测无效）
