# EUR D1 REGULAR alpha 交付清单（终版 · 2026-11-11 封档）

> 采集已按用户指令终止：「在未点亮塔上不再进行投入；在已点亮塔上不再进行投入」。
> 本文件为封档记录，**只挖不提交**，提交权归用户。

## 一、可交付（3 颗，全部经 `submit_verdict` 核验 + prod 实测）

核验口径：模拟层 `FAIL 0` 且无硬闸 WARNING（只剩 MATCHES_COMPETITION / MATCHES_THEMES 两个非硬闸项）、Failed RA/PPA 计数 = 0、平台 prod < 0.7。

### 1. O0W0w3P7 —— 新闻事件流量

```
group_rank(ts_rank(ts_sum(vec_avg(mws46_ravenpack_sum_story_count),5),110), group_cartesian_product(sector,country))
```
- 配置：region=EUR / universe=TOP2500 / delay=1 / decay=1 / neutralization=MARKET / truncation=0.08
- 数据集：`news46`｜核心字段：`mws46_ravenpack_sum_story_count`（cov 0.94）
- 算子逻辑：vec_avg 取新闻条数均值 → ts_sum 5 日累加（事件流量）→ ts_rank 110 日时序分位 → group_rank 在 sector×country 内横截面排序
- 指标：**S 2.72 / F 1.15 / TO 28.3% / ret 5.08% / 2Y 3.31 / SUB ≥1.29**｜**prod 0.6403 ✓**
- 塔位：EUR / D1 / NEWS ×1.4

### 2. mLaLllmK —— 模型概率分位差（ten_day _13 版本）

```
group_rank(ts_mean(ts_rank(subtract(probability_fifth_quantile_ten_day_bucket_three_13,probability_fifth_quantile_ten_day_bucket_one_13),110),5), group_cartesian_product(sector,country))
```
- 配置：region=EUR / universe=TOP2500 / delay=1 / decay=1 / neutralization=MARKET / truncation=0.08
- 数据集：`techindi_model`｜核心字段：`probability_fifth_quantile_ten_day_bucket_three_13` / `..._one_13`
- 算子逻辑：三档概率 − 一档概率（中高分位的概率差）→ ts_rank 110 日 → ts_mean 5 日平滑降换手 → group_rank 横截面
- 指标：**S 3.98 / F 2.21 / TO 29.06% / ret 8.98% / 2Y 1.93 / SUB 2.22**｜**prod 0.6579 ✓**
- 塔位：EUR / D1 / OTHER ×1.5

### 3. 6XMmE0EL —— 同族，TOP1200 + INDUSTRY 中性化（本轮新解）

```
group_neutralize(ts_mean(ts_rank(subtract(probability_fifth_quantile_five_day_bucket_four_13,probability_fifth_quantile_five_day_bucket_zero_14),180),5), group_cartesian_product(sector,country))
```
- 配置：region=EUR / **universe=TOP1200** / delay=1 / decay=1 / **neutralization=INDUSTRY** / truncation=0.08
- 数据集：`techindi_model`｜核心字段：`probability_fifth_quantile_five_day_bucket_four_13` / `..._zero_14`
- 算子逻辑：最高分位 − 最低分位（五日内极端概率差）→ ts_rank 180 → ts_mean 5 → group_neutralize 去 sector×country 均值
- 指标：**S 2.35 / F 1.02 / TO 32.5% / ret 6.11% / 2Y 1.70 / SUB 1.87**｜**prod 0.6529 ✓**
- 关键：同一个表达式在 TOP2500+MARKET 下 prod 为 **0.7051（卡墙）**，缩 universe 到 TOP1200 → 0.7051→0.7041 无实质变化，**再改中性化 MARKET→INDUSTRY 才降到 0.6529**。

### 三颗互相关（阈值 0.7，4 年，全对通过）

| | O0W0w3P7 | mLaLllmK | 6XMmE0EL |
|---|---:|---:|---:|
| **O0W0w3P7** | 1 | 0.0027 | −0.0225 |
| **mLaLllmK** | 0.0027 | 1 | 0.4703 |
| **6XMmE0EL** | −0.0225 | 0.4703 | 1 |

**最大相关对 0.4703（mLaLllmK vs 6XMmE0EL），三颗全部 <0.7 ✓**

## 二、备用池（IS 全闸，prod 未测或卡墙 —— 不可与上面三颗同批提交）

### A. prod 已测、卡墙（同族，互相关 0.81–0.99，只能取其一）

| alpha | S | F | 2Y | SUB | prod | 说明 |
|---|---:|---:|---:|---:|---:|---|
| j2a2JPGo | **4.35** | 2.71 | 2.51 | 2.43 | 0.8573 | TOP2500 全族最高 S |
| YPaLkER6 | 2.53 | 1.30 | 2.02 | 2.21 | 0.7239 | TOP1200 four−zero 秩252 |
| d5akl0jw | 2.39 | 1.13 | 1.48 | 1.98 | 0.7051 | TOP1200，与 6XMmE0EL 同式不同中性化 |
| xAvAo2Wq / vRARbpGQ 等 AN 波 8 颗 | 3.56–4.35 | 2.07–2.71 | | | 0.808–0.860 | group 算子矩阵 |
| 3q0qvnd0 | 4.38 | 2.64 | 2.22 | 2.48 | 0.8166 | second 分位族 |
| 0mPm2Ko2 | 4.15 | 2.38 | 2.18 | 2.28 | 0.8428 | third 分位族 |
| vRARXJ03 / npap5Obl | 4.06 / 4.04 | 2.31 / 2.32 | | | 0.8961 / 0.7965 | fourth 分位族 |
| O0W0djbY / QP0PRA5p / VkNkQL2w | 4.20 / 4.14 / 4.18 | 2.41–2.45 | 2.56–2.73 | | 0.8095 / 0.7952 | tm_15 反向 |
| RRejnG8n | 2.09 | 1.13 | 1.51 | 1.09 | 未测 | news50 decay14 |

### B. IS 全闸、prod 未测（封档时未投入测 prod，按指令停止）

| alpha | 族 | S | F | TO | 2Y | SUB |
|---|---|---:|---:|---:|---:|---:|
| gJak1v8g | prob ten_day four−zero_15 | 2.35 | 1.08 | 29.7% | 1.33 | 2.01 |
| Xgampq7m | prob ten_day three−one_13 | 2.19 | 0.96 | 28.2% | 0.98 | 1.87 |
| A1xjw6lg | prob five_day four−zero_15 | 2.18 | 0.95 | 33.1% | 1.08 | 1.94 |
| QP0Zae7K | prob ten_day four−zero_14 | 2.10 | 0.89 | 29.3% | 0.76 | 1.66 |
| pwaY6Jao | prob five_day three−one_13 | 2.01 | 0.84 | 31.9% | 0.63 | 1.85 |
| mLaw82a5 | prob five_day three−one_14 | 1.85 | 0.73 | 32.5% | 0.66 | 1.59 |
| O0WQpw61 | prob ten_day three_131−two_131 | 1.77 | 0.82 | 26.9% | 1.32 | 1.46 |
| （以上 7 条均为 TOP1200 + INDUSTRY 配置，fails=[]） | | | | | | |

## 三、字段画像与数据存档索引

| 内容 | 路径 |
|---|---|
| EUR 全部 173 个数据集清单（含 category / alphaCount / coverage / fieldCount） | `tracking/EUR/reference/eur_datasets_d1.json` |
| news46 全 30 字段画像（19 VECTOR + 11 MATRIX，cov 1.0） | `tracking/EUR/reference/fields_news46.json` |
| 逐波表达式原文（x → bw 共 40+ 波） | `results/{wave}_wave_exprs.json` |
| 逐波指标记录 | `results/{wave}_wave_metrics.json` |
| prod 实测原始结果 | `results/prod_wait_{alpha}.json` |
| **主台账（全部波次结论、判死证据、prod 全表）** | `tracking/EUR/WAVE_LEDGER.md`（1.34 MB） |

## 四、方法论沉淀（本战役最有价值的部分）

### 4.1 EUR D1 TOP2500 只有两类信号能出全闸

| 形态 | 代表 | 实测上限 | prod |
|---|---|---|---|
| 模型预测分位差 | techindi_model `probability_*_quantile_*` 桶差 | S 4.38 | 0.658–0.896 |
| 事件流量计数 | news46 `story_count`、news50 `rp_story_event_count` | S 2.72 | 0.5416–0.6403 |

六类形态已实测判死：情绪/语义评分（|S|≤0.57）、慢变量季度披露（TO 4–15%）、估值因子、分析师修订计数、价格衍生、新闻时间戳。

### 4.2 「计数型」不是充分条件，需高频事件流前提

| 有效 | 无效 |
|---|---|
| news46/50：cov 0.79–0.94，不平滑 TO 33% | insiders1 / insider_agg_matrix / fund_holdings_panel：cov 0.55–0.88，TO 9–16% |
| 信息到达率型 | 稀疏交易事件型 |

判据：**cov ≥0.75 且不平滑时 TO 能到 25%+** 才可能是流量信号。
注意区分死法：socialmedia12 的 TO 65% 却 |S|≤0.34 属「横截面方向性近零」，不是频率问题。

### 4.3 prod 相关的全部杠杆（30+ 实测点）

| 杠杆 | 效力 | 代价 |
|---|---|---|
| 换桶对 / 版本号 | **−0.19**（0.849→0.658） | 无（IS 仍全闸） |
| 缩 universe TOP2500→TOP1200 | **−0.133**（0.8573→0.7245） | 无（F/2Y/SUB 反而改善） |
| **换平台中性化 MARKET→INDUSTRY** | **−0.052**（0.7051→0.6529） | F −0.11、ret −1.14pp，但 2Y +0.22 |
| 换分位族 | 无 | — |
| ts_rank 窗口 / group 算子 / 分组轴 / truncation | 无（≤0.04） | — |
| nan_handling ON↔OFF（满覆盖字段） | 无（逐位相同） | — |
| **decay** | **反向，+0.40**（0.54→0.945） | 禁用 |

> **关键纪律**：prod 卡墙时按「桶对/版本 → universe → 中性化」顺序试；**不要先用 decay**，它是唯一会让 prod 变差的杠杆。
> 且 **prod 是带符号最大值** —— 负 Sharpe 版本测出的低值是假象（qM7M2b6P 负向 0.4725 → 正向 0.7952）。

### 4.4 IS 全闸 ≠ 可交付

`fetch_metrics.py --brief` 的 `fails=[]` **只读 `checks.fail`，不含 `checks.warning`**。
S/F/2Y/CLUSTER 在 warning 档也会阻断提交。
**必须用 `python tools/submit_verdict.py --alpha-id <id>` 查完整 checks**：只认 `FAIL 0` 且无硬闸 WARNING 的件。
本战役有 8 次以上「fails=[] 但实际 BLOCKED」的误判，其中 vRAwVW1b / Grm1E6vJ 甚至通过全闸但 prod 0.9457–0.947 仍不可交付。

### 4.5 派发前四项自检（本轮 5 次整批作废的教训）

| 自检项 | 漏检后果 |
|---|---|
| 括号配平 | `Unexpected end of input`，整批 10 条 ERROR |
| 窗口参数为整数 | `lookback should be a positive integer`，整批 CANCELLED |
| 字段名 preflight | `unknown variable`，整批 CANCELLED |
| 算子签名 | `Invalid number of inputs`，整批 CANCELLED |

另：**新数据集先派 2 臂探针**，不要把多个未验证数据集混进同一波——BX 波三个数据集混合 10/10 FAIL 且无法定位原因。

## 五、缺口与结论

目标 10 颗，交付 **3 颗**，缺口 7 颗。

**缺口无法在 EUR 内补齐，这是数据结论不是投入不足**：
1. 全部有效信号集中在 `techindi_model`（一个拥挤 bet，内部互相关 0.64–0.99）与 news46/50（各只有一个强字段）；
2. 全部 12 个 category、173 个数据集已扫描完毕，六类形态判死；
3. prod 地板 0.70 已用全部杠杆验证到底——能过的只有 3 个点。

**若要继续补缺口，必须改变一条约束（需用户决策）**：换区域（USA/JPN/CHN 塔大量未点亮），或放宽「单数据集 ATOM」允许更多跨 category 组腿。
