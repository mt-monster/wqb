# EUR/OTHER `other571`（Wikipedia 浏览量）战役台账（2026-11-06）

> 定位：EUR/OTHER 第 3 号跃迁目标（前两个：`techindi_model` prod 封盘、`news_sentiment_dl` 无信号封盘）。

## 一、数据集画像

**30 个 MATRIX 字段，全部是 Wikipedia 公司页面浏览量的分窗口聚合。**
（字段描述原文：`oth571_views14d` = "Total Wikipedia company page views ... over the trailing 14-day window **ending 14 days ago**"）

| 轴 | 取值 |
|---|---|
| 窗口 | `today` / `7d` / `14d` / `28d` / `84d` / `1y` |
| 时段 | `morning` / `afternoon` / `evening` / `night` |
| 设备 | `mobile` / `desktop` |

覆盖：0.7009（1y 族）- 0.7806（7d 族）；拥挤度 **aC 1-9**（最挤 `views28dmobile` 9、`views7dmobile` 9）。

**两个关键性质**：

1. **数据有 14 天滞后**（窗口"ending 14 days ago"）。这既是缺点（注意力效应的即时部分拿不到）也是优点
   （天然低换手，因为同一信息多日不变）；而注意力 -> 反转的经典效应窗口是 1-4 周，14 天滞后仍落在效应期内。
2. **device 轴是真正的结构维度**：mobile 浏览量代理**零售注意力**，desktop 代理**机构/专业注意力**。
   两者之比是「谁在看这家公司」的直接度量，与「多少人看」正交。

## 二、模板库（10 个，结构互异）

| 编号 | 模板名 | 结构 | 算子数 | 信息维度 | 来源 |
|---|---|---|---:|---|---|
| R01 | 关注度水平 | `rank(views7d)` | 2 | 一阶：被关注程度 | Da-Engelberg-Gao |
| R02 | 异常关注度 | `rank(views7d / views84d)` | 4 | 短窗相对长窗（剔除规模） | 自建（标准异常量构造） |
| R03 | 关注度加速度 | `rank(ts_delta(views7d, 22))` | 3 | 一阶差分 | 自建 |
| R04 | 关注度时序分位 | `rank(ts_zscore(views7d, 252))` | 4 | 相对自身历史 | 自建 |
| R05 | 零售 vs 机构注意力 | `rank(views7dmobile / views7ddesktop)` | 4 | **参与主体结构** | 自建（本集独有维度） |
| R06 | 日内时段结构 | `rank(views7devening - views7dmorning)` | 4 | 关注发生的时间带（亚洲/欧美时区分工） | 自建 |
| R07 | 移动端占比 | `rank(views28dmobile / views28d)` | 4 | 零售参与度（28d 稳健版 R05） | 自建 |
| R08 | 关注度期限斜率 | `rank(views7d - views84d)` | 3 | 长短窗差（与 R02 的比值版互补） | 自建 |
| R09 | 关注度分歧 | `rank(views7dmobile/views7ddesktop) - rank(views84dmobile/views84ddesktop)` | 8 | 参与结构的变化率 | 自建 |
| R10 | 关注 x 极端度交互 | `rank(views7d / views84d) x rank(ts_zscore(views7d,252))` | 8 | 异常度与持续性的交互 | 论坛·置信度加权 |

维度自检：水平(R01)、相对长窗(R02/R08)、变化(R03)、时序分位(R04)、
主体结构(R05/R07/R09)、时间带(R06)、交互(R10) —— **7 个互不重叠维度，10 个结构**。

## 三、探针批

设置档：EUR / TOPCS1600 / delay 1 / decay 2 / SUBINDUSTRY / trunc 0.08 / VERIFY / nan ON / pasteur ON / maxTrade OFF。

| 批 | multisim | 模板 | 表达式 |
|---|---|---|---|
| R1 | `3wTPw69CF55eaXH11KkDOTtl` | R02 / R05 | `rank(views7d/views84d)` / `rank(views7dmobile/views7ddesktop)` |
| R2 | `ykz4T7om56UbtqqsRGNMv8` | R03 / R04 | `rank(ts_delta(views7d,22))` / `rank(ts_zscore(views7d,252))` |

预注册判据同前：S >= 1.58 / F >= 1 / sub/S >= 0.5303 / TO < 70% => 测 prod；prod < 0.70 则登记并点亮 EUR/OTHER。

风险标注：cov 0.70-0.78 偏薄；`1y` 族覆盖最低（0.7009），若用 1y 做分母需留意有效样本数对 CONCENTRATED_WEIGHT 的影响。
