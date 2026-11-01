# KOR / D1 / TOP600 数据集清单与未点亮塔排队（2026-10-30 快照）

> 数据源：`mcp__wq_brain_http__get_datasets(region=KOR, delay=1, universe=TOP600)` 返回 **185 个数据集 / 15 categories**；
> 点亮状态：`get_pyramid_alphas()` 实测本季度 KOR/D1；乘数：`get_pyramid_multipliers()`。
> 用法：这是**数据集级**排队表，进入某数据集前必须再做**字段级画像**（见 `news_sentiment_transfer.md` §0 的反面教材 news54）。

## §1 点亮状态与乘数（KOR/D1）

| category | lit / 3 | 乘数 | 本轮处置 |
|---|---|---|---|
| fundamental | **3/3 满** | 1.6 | ⛔ 不派发（已满，且 submit_ready 里 `LLZ6wZO2` 正卡在这条：3/3 满故不提） |
| model | **3/3 满** | 1.6 | ⛔ 不派发 |
| shortinterest | **4/3 满** | 1.4 | ⛔ 不派发 |
| analyst | 2/3 | 1.6 | 仅剩 1 席，留作最后补位 |
| pv | 2/3 | 1.4 | 仅剩 1 席，且用户禁令限制 PV 组腿 |
| other | 1/3 | 1.6 | 有 2 席，但用户禁令限制 OTHER 组腿；单数据集 ATOM 仍可 |
| **news** | **0/3** | **1.6** | ⭐ 本轮主攻 |
| **sentiment** | **0/3** | **1.6** | ⭐ 本轮主攻（`news_sentiment_transfer` 已画像） |
| **institutions** | 0/3 | 1.4 | 下一批 |
| **macro** | 0/3 | 1.4 | 下一批 |
| **risk** | 0/3 | 1.3 | risk59 一阶矩族在挖（wave 202） |
| **insiders** | 0/3 | 1.2 | 待排 |
| **earnings** | 0/3 | 1.1 | 待排 |
| **imbalance** | 0/3 | 1.0 | 待排 |
| **socialmedia** | 0/3 | 1.0 | 待排 |

⇒ **未点亮塔共 9 个，合计 27 席空缺**；乘数 1.6 的 news/sentiment 是成本收益最高的两个。

## §2 未点亮塔数据集清单（按乘数降序）

### news（1.6，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| news79 | .8563 | 85 | 320 | 899 | 饱和 |
| **news50** | .6254 | 81 | 56 | 113 | 备选（未画像） |
| news7 | .6327 | 56 | 121 | 372 | 注意力/提及频率 |
| **news38** | .7971 | 45 | 88 | 227 | 覆盖最好 |
| **news85** | .6325 | 23 | 33 | 52 | 备选（论坛「涨跌反应差」帖） |
| news54 | .6914 | 40 | 31 | 43 | ❌ **字段级否决**：全是事件日历元数据，唯一数值 `mws54_factor` cov .2449 |
| news18 | .5709 | 29 | 293 | 1012 | 饱和 |
| news59 | 1.0000 | 2 | 277 | 2396 | 极饱和 |
| news104 | .2671 | 11 | 35 | 85 | ❌ cov<0.4 换集 |
| 其余 15 个 | .22–.74 | 2–93 | — | 8–212 | 见 §4 原始表 |

### sentiment（1.6，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| **news_sentiment_transfer** | **.9654** | 23 | 1–23 | 1–29 | ✅ **已画像 → wave 203** |
| other553 | .6243 | 21 | 66 | 96 | 备选 |
| sentiment27 | .3989 | 29 | 437 | 1871 | 饱和 + 低覆盖 |
| sentiment21 | .3812 | 138 | 54 | 94 | cov<0.4 |
| sentiment23 | .2648 | 156 | 35 | 54 | cov<0.4 |
| sentiment26 | .3570 | 19 | 29 | 48 | cov<0.4（论坛：突发新闻密度） |

### institutions（1.4，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| institutions6 | .9996 | 11 | 313 | 1003 | 高覆盖但饱和；`scan_fields` 必须 `filter_sharpe=false`（否则只见 4/11） |
| fund_holdings_panel | .8093 | 30 | 111 | 219 | 机构持仓面板（USA wave 239 已用过，跨区需重扫） |

### macro（1.4，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| macro63 | 1.0000 | 1 | 81 | 192 | 单字段，机制空间窄 |
| other106 | .4038 | 15 | 117 | 307 | 刚过 cov 0.4 线 |

### risk（1.3，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| risk70 | .9798 | 96 | 1218 | 7963 | 极饱和 |
| risk88 | .9727 | 64 | 489 | 1405 | 饱和 |
| **risk59** | .9806 | 16 | 220 | 561 | ⭐ wave 201/202 在挖：**方差族死、一阶矩族活** |
| risk71 | .6658 | 7 | 150 | 344 | 需先解决 2Y 全族 ≤0.16 |
| risk60 / risk68 | 1.0 / .9914 | 5 / 5 | 83 / 342 | 211 / 757 | 小字段集 |
| risk72 | .6246 | 5 | 163 | 400 | — |

### insiders（1.2，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| insiders5 | .8918 | 53 | 802 | 4959 | 高覆盖但极饱和 |
| insiders1 | .3526 | 9 | 201 | 548 | cov<0.4 |

### earnings（1.1，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| earnings3 | .6603 | 8 | 644 | 2616 | 饱和；纯事件计时腿（MEA 已有配方，跨区需重扫） |

### imbalance（1.0，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| imbalance5 | .8559 | 2 | 486 | 1384 | 仅 2 字段 |

### socialmedia（1.0，0/3）
| dataset | cov | fields | users | alphas | 备注 |
|---|---|---|---|---|---|
| other100 | 1.0000 | 1 | 154 | 399 | 单字段（category 标 socialmedia） |
| socialmedia39 | 1.0000 | 1 | 182 | 576 | 单字段 |

## §3 未点亮塔中 coverage < 0.40 的（KOR 策略规则：CW 先查覆盖率，<40% 换集）

16 个：sentiment23(.2648/156)、sentiment21(.3812/138)、news23(.3288/93)、news46(.3418/44)、news36(.2261/43)、
sentiment27(.3989/29)、news31(.3541/25)、news17(.2692/24)、news84(.3702/23)、news48(.2698/22)、news73(.2676/22)、
news3(.2592/19)、sentiment26(.3570/19)、**news104(.2671/11)**、other7(.2938/11)、insiders1(.3526/9)。

⚠ 例外：`sentiment23`/`sentiment21` 字段数 156/138，若机制足够强可先做**覆盖率补偿**（`ts_backfill` 或门控）再评估，
但按既定规则本轮**不优先派发**。

## §4 排队顺序（本轮战役）

1. **risk59**（1.3，在挖）→ wave 202 反向 + CW 居中，读数后决定是否继续一阶矩族
2. **news_sentiment_transfer**（1.6，sentiment）→ wave 203，5 机制族
3. **news50 或 news85**（1.6，news）→ wave 204
4. **institutions6 / fund_holdings_panel**（1.4）→ wave 205
5. **macro63 / other106**（1.4）→ wave 206
6. 剩余：insiders5 → earnings3 → imbalance5 → socialmedia39

⚠ 排队不等于承诺：每一步都要过 §0 的字段级画像 + 双通道取证 + 归因，读数不合格就换集不硬推。
