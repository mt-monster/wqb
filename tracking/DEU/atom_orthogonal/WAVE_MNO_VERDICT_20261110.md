# DEU 第三席寻觅：波 M / N / O 归因判死台账（2026-11-10）

> 背景：借券族 CV 闸维持 0.60 ⇒ E569ZE7L 本轮不出货，继续找别的机制族。
> 本轮扫描全部 172 个 DEU 数据集，挑出**有供数且塔未点亮**的族逐一实测。

## 一、选族扫描（172 集全量，cov ≥ 0.4 字段数 ≥ 3）

排除已穷尽族（analyst / fundamental / shortinterest / predictive_starmine / news17·81·7 /
institutions6 / insider / option1 / fund_holdings / global_seasonal / techindi / workforce /
sentiment7 / socialmedia12 / earningscall / event_sentiment）后，仍有供数的候选：

| 数据集 | 字段数 | cov≥0.4 | maxcov | maxuc | 塔状态 | 判定 |
|---|---:|---:|---:|---:|---|---|
| model25 | 217 | 207 | 1.0 | 243 | model=3 已点亮 | 禁混集合内，不选 |
| **risk60** | 5 | 5 | 0.835 | **127** | **risk=0 未点亮** | 实测（波 N）判死 |
| model216 / model30 / model26 / model264 / model109 / model250 / model238 / model28 / model106 / model36 / model53 / model307 / model313 / model262 | — | — | — | — | model 已点亮 | 禁混集合内，不选 |
| dl_riskfree_returns | 133 | 133 | 1.0 | 99 | risk 类 | 收益率类，非因子面 |
| pv30 / pv29 / pv109 | — | — | — | — | pv=0 但属 PV 禁混集合 | 禁混集合内，不选 |
| **sentiment27** | 18 | 18 | **0.912** | 38 | **sentiment=1 未点亮** | 实测（波 M）判死 |
| other47 / other455 / other532 / other545 / other699 / other250 | — | — | — | — | other=2 | 禁混集合内，不选 |
| **news104** | 11 | 11 | **0.963** | 24 | **news=0 未点亮** | 实测（波 N）判死 |
| **news18 / news50 / news38 / news20** | 70/37/3/46 | 全 | 0.6~0.98 | 6~11 | news=0 | 未测（后续候选） |
| pattern_scores / multifactor_return_pred | 504/648 | 全 | 1.0/0.54 | 24/14 | 模型输出 | 伪预测型，类 global_seasonal，暂不选 |

## 二、波 M：sentiment27（Tranco 域名排名）—— 判死

10 条（S 范围 -0.56 ~ +0.58，2Y -1.07 ~ +0.95）

| 候选 | S | 2Y | 符号 |
|---|---:|---:|---|
| vR1WRVmz | 0.58 | 0.23 | + |
| YP1RPdQM | 0.49 | 0.13 | + |
| zq3lqzOV | 0.29 | -0.58 | + |
| xArJAang | 0.22 | 0.62 | + |
| rKRZKmWj | 0.09 | -0.77 | + |
| QPvwPdEr | 0.02 | -1.07 | + |
| omExmeVm | -0.26 | 0.66 | − |
| GrWZrvkx | -0.26 | 0.61 | − |
| KPJWPRkk | -0.34 | 0.95 | − |
| xArJAann | -0.56 | 0.01 | − |

**判据 ME**：符号混乱（正负各半）⇒ **真噪声**，不是方向问题（对比借券族全负 = 方向反）。

**归因**：Tranco 域名排名衡量的是**网站热度**（DNS 流量 + 浏览器扩展 + 网络爬虫），
反映的是企业知名度/营销投入，**不是市场信息**。知名度变化与股票收益无横截面定价力。
论坛线索「维基百科关注度的私域信号在德国DEU市场的因子化尝试」（72 赞）指的是
**Wikipedia 浏览量（snt7）** 与 **Tranco（snl27）作为辅助腿的 vector_neut 组合**，
不是 snl27 单腿的加速度。⇒ 波 O 转测 snt7。

## 三、波 N：news104 + risk60 —— 判死

10 条（S 范围 -0.91 ~ +0.60，2Y -1.24 ~ +0.92）

**news104（cov 0.963）**：nws104_prob_pos / sentiment / novelty / relevance / confidence 五字段
→ 全部 S ≤ 0.60 且符号混乱。
**归因**：news104 是**事件级**数据（一条新闻一个观测），每日到达的新闻只覆盖少数公司；
DEU TOP500 面板上大部分股票多数日期无新闻 ⇒ 事件型情绪在截面上的有效样本太少，
且情绪概率的截面差异被覆盖度差异淹没。

**risk60（cov 0.835, uc 127）**：rsk60_crowding / offer / last / lending_fee_bid_rate
→ 全部 S ≤ 0.60，符号混乱（omExm3Zl -0.91、QPvwP26W -0.87）。
**归因**：risk60 与已成功出货的 shortinterest3（shrt3_bar）是**同一信息面**
（借券费率/拥挤度），DEU 生产池已覆盖；而 risk60 的 VECTOR 事件更新频率比 shortinterest3 更低
（快照制 vs 逐笔），信息量更弱 ⇒ 同机制内更差的数据源。

**判据 MF**：同一信息面存在**已出货的数据源**时，优先用已验证的那个；
新数据源若与之同机制但信息量更低 ⇒ 直接判死，不做参数穷举。

## 四、波 O：snt7（Wikipedia 浏览量）—— 在飞

复刻 OS 池已成功件 bl6OWZ2M 的骨架（`ts_ir(ts_mean(x,5),22)` + `ts_quantile(...,252)`，
nanHandling ON + decay2 + trunc0.02 + SUBINDUSTRY），以及加速度结构对照。8 条。

## 五、方法论要点（判据 MG / MH）

- **MG：族级判死必须先看符号一致性。** 全负 = 方向反（翻转重测，最高产）；
  正负混合 = 真噪声（判死，别再穷举）。本轮借券族与 news/sentiment 族的分界正是这个判据。
- **MH：同机制内有多个数据源时，先用已出货的那个。** 新源若信息量更低（更新频率/覆盖方式更差）
  ⇒ 直接判死，不浪费波次。
- **MI：事件型数据集（每条观测是一篇新闻/一次借券成交）不适合直接做截面因子** ——
  有效样本量 = 有事件的股票数，多数日子为 NaN，截面差异被覆盖度差异淹没。
  必须先 ts_backfill 转成时间序列面板（本轮 shortinterest3 就是这么做的）才有效。

## 六、待测队列（后续候选）

- **news18（70 字段 cov 0.979, uc 11）**、**news50（37, cov 0.764）**、
  **news20（46, cov 0.919）**、**news38（3, cov 0.599）** —— news 塔仍完全未点亮（0），
  值得用「先 backfill 转面板」的写法再测一轮。
- 其它 cov 高的族：other47（18, uc30）、other532（8, uc18）—— 属禁混集合 OTHER，仅可与集合外 category 组腿。
- pattern_scores（504, cov 1.0, uc24）：模型输出评分，类 global_seasonal（已判死），优先级低但可留作兜底。
