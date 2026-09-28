# EUR D1 数据集挖掘经验索引

更新：2026-09-25。本次任务新增实验范围为 wave245–254，共6个主数据集、57条已完成回测、53个实际使用字段；另附辅助输入pv1的经验，不重复计数回测。完整合格 Regular 仍为0。所有结论限定本轮设置与时间范围，不覆盖工作区其他会话的全部历史。

| 数据集 | 文件 | 完成数 | 核心经验 |
|---|---|---:|---|
| news46 | [eur_news46_campain.md](eur_news46_campain.md) | 5 | 均值语气/新颖度/影响排序差与年度变化均弱，停止本轮结构 |
| news50 | [eur_news50_campain.md](eur_news50_campain.md) | 8 | VECTOR聚合及分类器分歧无合格信号；冷门和类型合规不足以保证收益 |
| fundamental23 | [eur_fundamental23_campain.md](eur_fundamental23_campain.md) | 18 | 融资依赖有强度，前四个强候选Prod均超.7；Mode B2盈利暴露剥离仍Prod .7432，年度均态相关性未核实 |
| fundamental17 | [eur_fundamental17_campain.md](eur_fundamental17_campain.md) | 14 | 8主假设＋4水平对照＋2条口径复验；报告利润水平S1.13，标准化利润水平S1.18，修正差额S-.50；保留盈利水平研究线索，未获Mode B资格 |
| other455 | [eur_other455_campain.md](eur_other455_campain.md) | 4 | 客户网络月收益2主假设＋2对照；最高S.32/RN-.07，匹配掩码未证实；关闭已测结构并留存问题 |
| other460 | [eur_other460_campain.md](eur_other460_campain.md) | 8 | MODEL方向概率四组配对，最高S.07；概率差未显改善，2Y全负，关闭八个已测结构并保留期限/校准问题 |
| pv1（辅助） | [eur_pv1_campain.md](eur_pv1_campain.md) | 已含other455的4条 | returns仅作公开基线；同参数不保证持仓掩码一致，不再扫描窗口或镜像 |

示例中的news18/new18未出现在本轮实际实验中。wave250年度均态候选的相关性仍未核实；wave251–254已完成S3/S4/S6，对照和测量复验没有带来合格Alpha。253的4条已产生Alpha并完成收割，但平台子任务终态为WARNING，不能表述为检查全通过。诊断模拟、旧库存复核和未回测表达式均不计入57条。

经验由 `brain-dataset-mining-experience` 技能管理，主流程S6更新，下一轮S-PRE/S1/S2读取。数据仍以DB为权威；自动块是统计证据，块外是经审查的中文机制复盘。无新数据时刷新幂等，人工复盘不会被覆盖。
