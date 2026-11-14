# BE46 派发：pv29 统计聚类自定义分组轴（NEWS×I7 线最后未试杠杆，2026-11-12 凌晨）

## 一、依据

- NEWS×I7 线 31 臂天花板 1.52，判死前穷尽度六维中 D4（分组轴）只覆盖了 sector/industry/market 标准轴；
- CLAUDE.md 设计准则明确提示「有些字段适合做 group 或者 bucket 自定义分组」；
- pv29 数据集（PV 塔，未点亮，作信号已探针死）的 50 个字段全部是**统计聚类标签**（cov 1.0，
  level 2/10/20/50 × top100/200/400/600/800/1200/all 变体）——作分组轴而非信号使用，
  属于「分组字段」用途，不占信号配额，且不违反禁混（分组不携带信号方向）。

## 二、派发内容（sim 8tjf522Y4h590YpGzP51bd，6 臂）

基线几何：P05JM61x = group_zscore(add(news Δ66 正腿, I7), market)，S 1.46；
天花板构造：QP010j5W（外层 group_rank）与 YPaPX3JJ（relevance 加权）均 1.52。

| 臂 | 变体 | 分组轴 |
|---|---|---|
| 1 | 基线 | 内层 sector → level10 聚类（top600 变体，≈10 簇） |
| 2 | 基线 | 内层 → level20 聚类（≈20 簇） |
| 3 | 基线 | 内层 → level50 聚类（≈50 簇，细粒度） |
| 4 | 外层 group_rank | 内层 level10 聚类 |
| 5 | relevance 加权 | 内层 level20 聚类 |
| 6 | 基线（内层 sector 不变） | **外层 group_zscore(market→level10 聚类)** —— 信号级聚类中性化 |

算子数 10-12 ✓；设置 DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON（同基线波）。

## 三、判读预案

- 若某臂 S≥1.58 且 F/sub/2Y 全过 → 该臂进入 self/prod 终验（候选 #12 管道）；
- 若全臂 S ≤1.55 → 分组轴杠杆证伪，NEWS 线判死升级为「七维穷尽」，D4 记「标准轴+聚类轴全试」；
- 注意 -1/10000 等特殊标签会形成垃圾组，若 S 结构异常先查此。
