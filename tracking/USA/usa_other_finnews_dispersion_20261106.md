# USA / OTHER 面 finnews_nlp_scores 战役台账

日期：20261106｜区域：USA TOP2000 D1｜category：OTHER（塔位 2，差 1 颗点亮，倍率 1.4）

## 0. 为什么重新开 OTHER 面

USA 塔位实读（get_pyramid_alphas，D1）：16 个 category 里只有 model(4) / analyst(6) 已点亮，
其余 14 个全未点亮。其中 other = 2、risk = 2，都只差 1 颗即点亮，且 other 倍率 1.4 为全表最高。
因此 OTHER 是 USA 最高价值塔位，不是可有可无的面。

## 1. 关键排重：三个 OTHER 数据集其实是同一份情绪的三种切法

实测 get_datafields 字段名比对：

| 数据集 | 字段数 | aC | 字段结构 | 判定 |
|---|---:|---:|---|---|
| mmp_nlp_sentiment | 1650 | 81 | Benzinga 情绪/主题 | 已判死（情绪水平最强 0.69） |
| finnews_nlp_scores | 105 | 13 | Dow Jones Newswires 情绪 7 统计族 x 3 极性 x 5 变体 | 本轮主攻 |
| ai_news_scores | 105 | 31 | RavenPack 情绪同名族（negative/positive/neutral_score_*） | 同机制，暂不派 |
| other596 | 420 | 314 | 同上 + std/conf 前缀 oth596_2* | 同机制，暂不派 |

结论：三者底层都是 Dow Jones / RavenPack 新闻情绪。**再测一次「情绪水平」必然重复 mmp 的判死结果**。
唯一没被覆盖过的是**分布维度**——finnews 每个极性都给了 min/max/median/mean/stddev/95% 置信上下界共 7 个统计量，
这是 mmp（只有均值与主题净差）没有的结构，也是本轮全部模板的信息来源。

字段编号坑（实测，务必记住）：
- average_* / median_* / minimum_* / lower_confidence_* / upper_confidence_*：negative/neutral/positive 均有 _1.._5；
- stddev_negative 有 _1.._5，但 stddev_neutral / stddev_positive 只有 _2.._6（没有 _1）；
- maximum_negative / maximum_positive 只有 _2.._6，maximum_neutral 有 _1.._5。
⇒ 跨极性同变体取数时优先用 _2 或 _3，避免踩不存在的组合。

## 2. 模板池（12 个结构互异模板，含来源）

| # | 模板名 | 信息维度 | 骨架要点 | 来源 | 状态 |
|---|---|---|---|---|---|
| T1 | 精度加权情绪 | 方向 x 精度 | 净情绪均值 / 同日两极性 stddev 之和 | 自建（贝叶斯逆方差加权）+ Diether-Malloy-Scherbina 2002 口径 | **已派发** |
| T2 | 报道注意力（条数代理） | 纯注意力 | (stddev / CI宽度)^2 ∝ 报道条数 n | Da-Engelberg-Gao 2011 ASVI + Barber-Odean 2008 注意力买入 | **已派发** |
| T3 | 情绪动量 | 变化率 | ts_delta(ts_mean(净情绪,22),66) | 论坛帖 18641983716503 + Wang-Zhang-Zhu 2018 The Momentum of News | 备料 |
| T4 | 情绪意外 | 偏离自身历史 | 净情绪均值 - ts_mean(净情绪,252) | 自建（标准化意外） | 备料 |
| T5 | 分歧度做空 | 横截面分歧 | -group_rank(stddev, sector) | Diether-Malloy-Scherbina 2002 意见分歧 | 备料 |
| T6 | 尾部冲击 | 极值相对均值 | (max_neg - mean_neg) / stddev_neg | Tetlock 2007 + Chan 2003 新闻冲击漂移 | 备料 |
| T7 | 故事侧偏度 | 分布形状 | (mean - median) / stddev | 自建（Pearson 第二偏度系数） | 备料 |
| T8 | 中性占比（关注度无方向） | 纯关注度 | neutral_mean / (pos+neg+neut) | 自建（注意力剥离方向） | 备料 |
| T9 | 情绪失衡比 | 方向（比值化） | (pos - neg) / (pos + neg) | 自建（尺度无关，抗行业差异） | 备料 |
| T10 | 置信区间全偏 | 统计显著性 | CI 下界 > 0.5 才算情绪确立（sign 一致性） | 自建（单侧显著性检验） | 备料 |
| T11 | 跨变体模型分歧 | 模型间不一致 | average_*_1 - average_*_5 | 自建（两个 NLP 版本对同一批新闻的分歧） | 备料（有前科，慎用） |
| T12 | 共识-极端交互 | 条件信号 | 低 stddev 且高 |均值-0.5| 才取信号 | 自建（精度门控） | 备料 |

模板数量 12 ≥ 10，且差异落在信息维度（方向/变化/意外/分歧/尾部/形状/注意力/显著性/模型不一致）上，不是换窗口。

## 3. 已派发批次

### 批次 A（mid = 1u2VUVesM4ALaCEjm3cASML）

统一设置：USA / TOP2000 / D1 / decay 0 / STATISTICAL / trunc 0.08 / unit VERIFY / nan ON / pasteurization ON / maxTrade OFF。
decay 取 0 是刻意的：本轮要读两种构造的**原始换手率**，再决定 decay 档，而不是一上来就平滑掩盖。

下简称 net = average_positive_sentiment_score_1 - average_negative_sentiment_score_1。

E1（T1 精度加权情绪，算子 3）：
group_rank(ts_mean(net, 22) / ts_mean(stddev_positive_sentiment_score_2 + stddev_negative_sentiment_score_2, 22), sector)

E2（T2 报道注意力，算子 4）：
-group_rank(ts_mean(power(divide(stddev_negative_sentiment_score_2, upper_confidence_negative_sentiment_2 - lower_confidence_negative_sentiment_2), 2), 22), sector)

gate 结果：validate_expressions 返回 valid=true、unknown_fields=[]。
注意其 warning 称 stddev_negative_sentiment_score_2 / stddev_positive_sentiment_score_2 查表失败 6 次——
这两个字段已由 get_datafields 全量枚举直接确认存在（在 105 字段清单的尾段），不是不存在，属查表超时。

## 4. 本轮的定量约束（决定要不要继续磨这条面）

fitness 反推：F ≈ S x sqrt(|returns| / max(TO, 0.125))。
推论一：TO >= 12.5% 时，F≥1 需要 S x sqrt(ret/TO) ≥ 1；returns 只有 4-5% 的新闻情绪类，
需要 S 接近 4 才能过 F —— 这就是 techindi 的 P4-P0 有 S 2.29 却被 F 0.59 拦死的根因。
推论二：**把 TO 压到 12.5% 以下，公式分母锁死在 0.125**，此时 F ≈ 0.632 x S（ret=5%），
S 1.58 即可让 F 恰好压线 1.0。⇒ 新闻情绪面必须做低换手，高换手路线在 F 上是死路。

## 5. 待办

- [ ] 收批次 A 指标，读 E1/E2 的 S / F / TO / 2Y / returns
- [ ] 按 TO 实测值决定 decay 档与是否需要 hump（不要先把 hump 当默认）
- [ ] 若 E1 或 E2 的 S ≥ 1.0，沿该模板做参数扩展（窗口 22/63/126 与分组轴 sector/subindustry）
- [ ] 若两条 S 都 < 0.6，按 T3/T4/T6/T10 换信息维度，不要在同模板上调参数

## 6. 批次 A 结果：新闻情绪分布维度全灭（finnews_nlp_scores）

| alpha | 模板 | S | F | TO | 2Y | sub | returns | 判定 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| omEPzje5 | T1 精度加权情绪 | -0.34 | -0.06 | 18.82% | -0.81 | -0.05 | -0.63% | ❌ |
| xArlz7aw | T2 报道注意力 | -0.01 | 0.00 | 19.16% | -1.44 | -0.45 | -0.02% | ❌ |

T2 的 S -0.01 配 2Y -1.44，是「不同区间方向完全相反」的纯噪声特征，不是弱信号。
TO 19% 也高于 12.5% 的关键阈值，两条都不具备可修复性。

**新闻情绪族结案（跨数据集、跨区域累计）**：mmp_nlp_sentiment 8 构造（最强 0.69）
+ finnews_nlp_scores 2 构造（-0.34 / -0.01）+ HKG news_sentiment_transfer 6 构造（全 ≤0.51）
= 16 个结构互异构造，无一超过 |S| 0.7。**新闻情绪方向/分歧/注意力/尾部四条信息维度全部无信号**，
不是模板不足，是这个信息源在日频横截面里已被消化。

（唯一例外仍是 techindi 的 S 2.29，但 F 0.59 卡死，见另一份台账。）

## 7. 批次 B–F 结果：sustainable_profit 盈利质量面（10 构造）

数据集体检：403 字段，**全部 VECTOR 类型**（必须 vec_avg），覆盖率 0.60-0.65（需 ts_backfill），aC 20 极低。

| alpha | 构造 | S | F | TO | 2Y | sub | ret | vol=ret/S |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A1VLOKnY | GP/NOA level，sector | 0.85 | 0.38 | 6.21% | 0.65 | 0.83 | 2.51% | 2.95% |
| QPvW5XnG | 外部融资/NOA 反向，sector | -0.09 | -0.01 | 6.20% | 0.53 | -0.01 | -0.26% | — |
| O0A65mqR | GP/NOA level，**subindustry** | **1.01** | 0.45 | 5.61% | **1.16** | 0.72 | 2.46% | 2.44% |
| 58EGq69n | GP/NOA 年度变化（趋势） | 0.18 | 0.04 | 7.60% | 0.38 | 0.23 | 0.50% | — |
| omEP9gN2 | 三盈利指标复合 | 0.96 | 0.43 | 5.70% | 1.28 | 0.81 | 2.47% | — |
| O0A65xGb | GP/NOA + ts_mean 63，subindustry | **1.13** | 0.53 | 5.10% | **1.60** | 0.71 | 2.78% | 2.46% |
| e751q6Zg | 同上，窗口 126 | 1.10 | 0.51 | 5.01% | 1.56 | 0.77 | 2.71% | — |
| bl6xW81R | 同上，窗口 252 | 1.09 | 0.50 | 4.91% | 1.62 | 0.83 | 2.66% | — |
| 6XdGYokL | 同 O0A65xGb，universe TOP3000 | 1.04 | 0.47 | 4.64% | 1.60 | 0.67 | 2.57% | — |
| wpQNJ206 | 同 O0A65xGb + signed_power 几何 | 1.09 | 0.49 | 4.32% | **1.67** | 0.71 | 2.50% | — |
| 2rAGaMwZ | 经济利润差（RNOA-借贷成本） | 0.62 | 0.22 | 5.42% | 1.23 | 0.53 | 1.64% | — |
| mLoKrpmX | 暂时性收入占比反向 | 0.15 | 0.02 | 4.65% | 0.90 | 0.03 | 0.34% | — |

### 7.1 有真实效果的两个杠杆

- **分组轴 sector → subindustry：S 0.85 → 1.01（+0.16），2Y 0.65 → 1.16（+0.51）**。
  盈利质量是子行业内可比的概念，子行业分组是对的；这与借券面「sector 全闸过、subindustry 崩」正好相反。
- **63 日平滑：S 1.01 → 1.13（+0.12），2Y 1.16 → 1.60（+0.44）**。基本面数据季度更新，63 日平滑对齐报告节奏。

### 7.2 三个无效杠杆（均已实测）

- **复合多指标无效**：三盈利指标（GP/NOA、CFO/NOA、GP/OA）复合 S 0.96 < 单指标 1.01。三者相关性太高，
  没有噪声可分散，只摊薄了最强的那一腿。**同概念多指标平均不等于提高信噪比**。
- **窗口加长无效**：63/126/252 得 1.13/1.10/1.09，单峰在 63，加长只损失信息。
- **宇宙与几何无效**：TOP3000 得 1.04（< TOP2000 的 1.13）；signed_power 得 1.09（略降 S，但 2Y 1.67、TO 4.32% 是副作用利好）。

### 7.3 饱和判定

10 个构造覆盖「分组轴 2 档 x 窗口 4 档 x 宇宙 2 档 x 权重几何 2 档 x 复合有无」的笛卡尔空间，
**S 上限 1.13、2Y 上限 1.67、TO 稳定在 4.3-6.2%**。USA 的主要闸是 LOW_SHARPE limit 1.58，差 0.45（40%）。
按 F 公式，vol 只有 2.46% 时 F=1 需要 **S ≥ 1.72**，差 0.59。

**根因判断**：GP/NOA 是 Novy-Marx (2013) 的公开因子，主字段 alphaCount 83，在 USA 已被充分套利。
数据集自称 sustainable_profit，但真正未被用过的字段（aC=0）——经济利润差 0.62、暂时性收入 0.15——都更弱。
⇒ **这个数据集的上限就是 S 1.13，不是模板不足**。带原语料 VECTOR 聚合可能损失了一部分横截面信息，但不足以补 0.45。

## 8. 结论与交接

1. **USA/OTHER 面本轮两条新路都走不通**：新闻情绪分布维度 -0.34/-0.01；盈利质量上限 1.13。
   加上此前 OPTION 天花板 0.93、mmp 最强 0.69、techindi F 卡死，OTHER 与 OPTION 两个塔位缺口本轮未收割。
2. **最有价值的方法论产出**是 7.1 / 7.2 两个杠杆的正负实证，以及 §4 的 F 公式二次推导（已入 Agent Memory）：
   低波动信号（vol≈2.5%）在 USA 需要 S≥1.72 才能让 F 过 1，比 1.58 线更高——**低换手慢变量在 F 维度是逆风**。
3. **USA 面已系统性证明难挖**：本轮新增 OPTION/OTHER 共 18 个构造全灭，出货仍只能靠 READY 池存量 3 颗。
   ⇒ 下一步应转向**完全未开采的区域**（ASI other 仅差 1 颗点亮、AMR 16 个 category 全零），
   而不是继续在 USA 换数据集——USA 的 S 1.58 线叠加高效市场，单位仿真产出比明显低于其他区。

## 9. 本轮全部仿真 alpha 清单

omEPzje5 / xArlz7aw（新闻情绪）｜A1VLOKnY / QPvW5XnG（GP/NOA 与外部融资）｜
O0A65mqR / 58EGq69n（subindustry 与趋势）｜omEP9gN2 / O0A65xGb（复合与平滑）｜
e751q6Zg / bl6xW81R（窗口 126/252）｜6XdGYokL / wpQNJ206（TOP3000 与 signed_power）｜
2rAGaMwZ / mLoKrpmX（经济利润差与暂时性收入）。全部 UNSUBMITTED，S 均 < 1.58 ⇒ 无一颗可提交。
