# BE46 ERROR 判决 + BE46b 重派（2026-11-12 凌晨）

## 一、BE46 全臂 ERROR 根因（sim 8tjf522Y4h590YpGzP51bd，6/6 ERROR）

`Incompatible unit for input of "group_rank" at index 1, expected "Unit[Group:1]", found "Unit[]"`

**pv29 聚类标签是 MATRIX 类型，group_* 第二参数要求 GROUP 类型**——类型不匹配。
preflight_expressions 只查字段存在性，不查类型匹配（BE31 老坑第三次重演：scope→类型→单位）。

## 二、修复：bucket(rank(x), range=...) 桥接

`bucket(rank(x), range="0,1,0.1")` 输出 GROUP 类型，可直接作 group_* 第二参数。
**先例：已提交 ACTIVE 件 bl6AvMkN 本身就用此骨架**
`group_neutralize(add(rank(a), rank(b)), bucket(rank(ts_mean(b,66)), range="0,1,0.1"))`（S1.61）。
pv29 标签是并列整数（同簇同 rank），bucket 后同簇落同桶 ⇒ 簇分组语义保真。

## 三、BE46b 派发（sim 4jSD1u6Wb4Vk9Ih11Cz4eFeT，5 臂，全部 12 算子）

基线腿（sector 内层，正号）：news = group_rank(Δ66(backfill132(NWS)), sector)；I7 = group_rank(ts_rank252(backfill(insd1_holdings)),sector)

| 臂 | 外层 | 分组 |
|---|---|---|
| 1 | group_neutralize(add(news,I7), ·) | bucket10簇（level10_top600, 0.1 分位） |
| 2 | group_neutralize(add(news,I7), ·) | bucket20簇（level20_top600, 0.05） |
| 3 | group_neutralize(add(news,I7), ·) | **市值五分位桶**（risk88 alternative_market_cap_usd，cov1.0） |
| 4 | group_zscore(add(news,I7), ·) | bucket10簇（zscore vs neutralize 对照） |
| 5 | group_zscore(·, market) | 新闻腿内层 bucket10簇 + I7 腿市场 rank（混合几何） |

臂 3 说明：市值桶是经典风格分组（CLAUDE.md「bucket 自定义分组」典型用法）；
risk88 作分组字段用途不占信号（RISK 塔未点亮，合规）。

## 四、判读预案

- 某臂 S≥1.58 且 F/sub/2Y 全过 → 候选 #12 管道（self/prod 终验）；
- 全灭 → D4 分组轴维度真正穷尽（标准轴 + 聚类桶 + 市值桶），NEWS 线判死档案升级为七维。
