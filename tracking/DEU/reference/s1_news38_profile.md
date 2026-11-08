# news38（story_analytics_*）字段画像 —— DEU/TOP500/D1 —— 2026-11-03

**来源**：MCP `get_datafields`（兜底通道）；§86 真新鲜池最后一集，至此真新鲜 6 集全部画像完毕（other47/news50/news38/analyst44/analyst9/insider_matrix[封存待裁定]）。

- **仅 3 个 VECTOR 字段**，cov 0.5992，alphaCount 合计 26（story_analytics_category=12 / metric_value=8 / relevance_score=6）——不是「字段少=贫瘠」，而是**事件流结构**：一条故事级 analytics 流。
- 字段三元组：**category**（analytics 类型/分类码，Integer）× **metric_value**（该类型下的数值）× **relevance_score**（综合/滚动 analytics 分，如情绪、注意力）。
- **机制箱**：①按 category 分桶取特定 analytics 类型的 metric_value 做信号（bucket 结构：category=分组轴、value=信号）②relevance_score 作 gate/加权 ③同一故事的多类型 analytics 交叉（category 差异=信息结构）。
- **注意**：category 是 Integer 码——**必须先摸清码表**（哪些值对应情绪/注意力/其它），盲 group_rank(category) 无意义；metric_value 的语义随 category 变化，混 category 直接 add/subtract=混信号（禁）。
- 排队位置：低于 news50（★3 字段可玩性有限，适合做窄而深的事件型小波或门控源）。

## 复核补记：category 码表问题（2026-11-03 05:0x 解除）

get_datafields 重拉三字段描述，`story_analytics_category` 官方描述关键句：「Integer code representing the analytics type or classification for the story/event, **which must be dynamically label-mapped per module and date** via NIO_IX overlay…」。

**结论：不存在静态码表**——同一 Integer 码的语义随 module 和日期漂移。推论：
- 机制箱①「按 category 分桶取 metric_value」**结构性废弃**（跨期分桶=用漂移的标签切数据，非平稳）；
- metric_value 直接混 category 聚合 = 混信号（禁）——metric_value 实际可用面只剩「经 relevance_score 门控后的窄窗事件取值」；
- **可用面收窄为两条**：`relevance_score`（复合分，直接信号/门控）+ 事件流计数密度（vec_count 结构，参照 GBR news17 ACTIVE 塔腿机制）。

**排队裁定**：news38（3 字段 / cov 0.5992 / 可用面 2 条）**降级为门控源/窄事件小波备选**，不再作为主力矿脉；下一矿脉优先序移交 sentiment7（注意力型，EUR search_interest 同型 ts_rank 受益者）/ news17（GBR vec_count×similarity 机制迁移）。

