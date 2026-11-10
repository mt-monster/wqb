# 8 族之外可补充测试的机制族（论坛 + 外部论文检索报告，2026-11-09 22:10）

## 检索方法
- 外部论文：web_search 8 个机制族 × 学术关键词（全部命中实证文献）
- BRAIN 论坛：search_forum_posts 多轮检索（中文/英文/单关键词均返回空——论坛检索通道异常，结论以外部论文为主）
- DEU 季节性专文命中：《Seasonalities in the German stock market》（直接以德国市场为研究对象）

## 一、未测机制族清单（8 族之外，按可测性排序）

### A. 经典动量 / 52 周高点（论文：Decomposing momentum / 52-Week-High Effect）
- 机制：过去 12-1 月收益（跳过最近月）或当前价相对 52 周高点距离
- DEU 数据：pv30（285 字段，未开波）+ pv20 returns_6d + 价格字段；GA 检索通道可用
- 为什么没测过：战役全程聚焦预期面/基本面，**纯价格动量从未做过专门波**
- 风险：PV 类（pv20 滑点/techindi）已死，但那是**衍生指标**——原始价格动量是不同信号源

### B. MAX 彩票效应（论文：MAX Effect 1.03%/月）
- 机制：最近月最大日收益（高偏度=彩票需求=低估后续）
- DEU 数据：pv30 / pv20 日收益分布 / GA 算子（max/abs 可构造）
- 与已封盘的「偏度」不同：之前测的是 skew_bid_ask（微观结构偏度），MAX 是**收益分布偏度**

### C. 净股票发行/回购（论文：Net Stock Issuance Anomaly，发行商落后回购商 8%/年）
- 机制：净发行（发行-回购）高的公司后续低估
- DEU 数据：fnd72 amt_of_tsy_stock（库存股=回购）、dividend 字段、fnd89 资本字段
- 为什么没测过：fnd72 按「PIT 水平」扫（AX），**回购/发行比率**这个学术标准构造没测

### D. 公告日溢价（论文：Earnings Announcement Premium / Frazzini-Lamont）
- 机制：公告周持股比非公告周收益高——事件时点持股倾斜
- DEU 数据：fnd72 announcement_dt / fnd89 字段
- 实现：trade_when(临近公告日, 1, 0) 类事件时点——但 DEU 有 trade_when 毒性记录（MPYVkXWo 2Y 0.08），需谨慎

### E. 隔夜/日内收益分解（论文：Nearly All the Equity Premium Is Earned Overnight）
- 机制：隔夜收益溢价、日内收益均值零
- DEU 数据：intraday_pv_feats（585 字段，含 open/close/intraday_return）
- 注意：该集微观结构模板死了（AQ），但隔夜-日内**收益分解**是不同机制（不是盘口流）

### F. 利率敏感度溢价（论文：Stock returns' sensitivity to interest rates）
- 机制：对利率变化的 beta（高敏感=久期长=利率上行受损）
- DEU 数据：model140（3 字段 sinc_comp/sinc_neut/sinc_sensitivity，探针活 2014-2023）
- 最小代价：仅 3 字段、1 波可扫

### G. 季节性（论文：Seasonalities in the German stock market——直接 DEU 专文！）
- 机制：同月/同周收益持续性（Heston-Sadka）
- DEU 数据：global_seasonal_model（2018+ 起始，borderline）+ mdl250_eq_seasonality（Wave 39 S 1.14 弱）
- 专文直接研究德国市场——先验最高，但数据起始晚是硬伤

### H. 特质（残差）动量（论文：Residual Momentum: A Cleaner Momentum Signal / Blitz）
- 机制：对市场残差做动量（剔除 beta 后的纯阿尔法动量）
- DEU 数据：risk68 rsk68_residual_return（探针活）+ GA 构造
- Wave 81 裸水平 -1.03 且 TO 0.91——但那是**水平**，**ts_delta 动量构造**没测

## 二、与已封盘 8 族的正交性判断

| 新族 | 与已封盘族的重叠 | 正交性 |
|---|---|---|
| A 经典动量 | 黑箱动量（AZ）不同源——原始价格 vs ML 衍生 | 高 |
| B MAX | 偏度死的是微观结构偏度 | 高 |
| C 回购 | 应计死的是权责发生制 | 高（现金流口径） |
| D 公告日历 | 与 SUE 死不同（日历时点 vs 惊喜幅度） | 中高 |
| E 隔夜分解 | 微观结构死的是盘口流 | 中高 |
| F 利率敏感 | 宏观未扫 | 高 |
| G 季节性 | model250 季节性弱（S1.14）但那是单字段 | 中 |
| H 特质动量 | risk68 裸水平死，动量构造未测 | 中高 |

## 三、建议测试包（3 波 × 10 模板）

- **Wave A**：经典动量/52w 高点/MAX（pv30 + pv20 价格字段 + GA 算子）——覆盖 A/B
- **Wave B**：回购/资产增长/净派发（fnd72 库存股 + fnd89 资产字段 + fnd90 股息）——覆盖 C
- **Wave C**：隔夜分解（intraday_pv_feats）+ 利率敏感（model140）+ 特质动量（risk68）——覆盖 E/F/H

全部在 DEU 现有数据集内可测，不违反「不得换数据集」约束（用已审计的探针活集）。
