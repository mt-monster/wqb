# DEU D1 战役 · 可视化战果面板

> 生成 2026-08-01 · 数据源：platform API（get_alpha_details / check_self_correlation / get_alpha_yearly_stats）


## 一、最终提交篮（5 颗互不相关候选）

| alpha | 机制 | S | F | TO | 2Y | prod | self | 覆盖 | 闸 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|
| `MPY9VNY9` | PS diff engine | **1.70** | 1.28 | 24.3% | 1.48 | 0.5986 | 0.2703 | 10/10 | fRA=0 | S2 winner; vs npvwXA8l 0.92 same-family -> this |
| `Vkxnb8QG` | time-momentum (pv30) | **1.61** | 1.34 | 15.6% | 1.70 | 0.6384 | 0.6379 | 10/10 | fRA=0 | self ceiling 0.6379 closest to 0.7 |
| `bl62jGgM` | predicted_surprise x5 (model24) | **1.78** | 1.50 | 14.0% | 1.75 | **0.8098 FAIL** | 0.6417 | 10/10 | fRA=0 | prod 第 11 次补查 6.6s 落地 = 0.8098 > 0.7 红线；5 腿 add 复合撞墙预判命中，**实质出局** |
| `1YNv6Ymk` | tm_15 diffts126/10 (other384) | **2.28** | 1.25 | 37.9% | 1.60 | **0.7983 FAIL** | 0.1335 | 10/10 | fRA=0 | prod 8.0s 落地 = 0.7983 > 0.7 红线；**单字段结构也撞墙**（预判「低风险」证伪），**实质出局**；直方图 0.7-0.8 桶 n=34、0.6-0.7 n=100 |
| `QPveY7Kg` | vector_neut news x sentiment | **2.03** | 1.16 | 37.1% | 2.40 | 0.6671 | 0.0242 | 5/10 | fRA=0 | 2014-2018 LEADING GAP 5y -> user ruling needed |

**互相关**：5 颗两两 <0.25（4 年日收益）；MPY9VNY9↔npvwXA8l=0.92 同族二选一已定 MPY9VNY9。

**S 分布**：QPveY7Kg 2.03 / 1YNv6Ymk 2.28 / bl62jGgM 1.78 / MPY9VNY9 1.70 / Vkxnb8QG 1.61 —— 5 颗全部 ≥1.58 线。

**self 分布**：QPveY7Kg 0.02 ←─── Vkxnb8QG 0.64 ── 线 0.7（余量最小）


## 一·B、队列复查新发现（2026-10-31 submit_ready 重扫）

| alpha | 机制 | S / F / 2Y | prod | self | 覆盖 | 状态 |
|---|---|---|---|---|---|---|
| `QPKKMg6Q` | netprofit_y1 残差（subtract group_mean，非双腿 add） | 1.65 / 1.47 / 1.58 | **0.807 FAIL**（10-30 缓存命中） | **0.668 ✓** | **满 10 年无空窗** ✓ | prod 撞墙出局；直方图 0.1-0.5 通铺 = 修正因子族拥挤特征 |
| `kqNRX1ZP` | snt7+snl27 vector_neut 双重中性 | **2.06 / 1.86 / 2.37** | **0.7706 FAIL**（4.2s 落地） | **0.051 ✓** | ⚠ 2014-2018 五年 leading gap | prod 撞墙出局；self 0.05 全场最干净也没用——prod 由信号类别决定 |

**self 一票否决（出局）**：
- `E56AzejK`（inst1+oth455，2Y 2.79）self **0.918** vs 已提交 `2rmGAPqN`
- `58gGQmlN`（prod 0.683 ✓ 本可过）self **0.941** vs `2rmGAPqN` —— **inst1 tail 族被 2rmGAPqN 整族钉死**
- eps_y1 四兄弟（kqJqQL08 / RREXxW6z / 6Xdx65eK / 1YNv8qaK）与 Vkxnb8QG 同骨架，互相关必撞，不烧槽


## 二、数据集矿脉盘点（本轮 10 集）

| 数据集 | 机制族 | 状态 | 本区峰值 | 判决 |
|---|---|---|---|---|
| `fundamental1` | fundamental_scores | **CLOSED** | - | sum_tree REJECT 0.5663 |
| `fundamental6` | OIBD / OIADPQ | **CLOSED** | 1.73 | 2nd dual-pass only 1.14; ceiling oiadpq 1.73 |
| `model28` | drift/dd/rank_float/vol/lev | **CLOSED** | 1.10 | 5 families exhausted; drift>S, vol 0.16, lev NEG |
| `model24` | predicted_surprise | **CLOSED** | 1.78 | bl62jGgM dual-pass |
| `pv30` | pv_ohlcv_tm/fitz_* | **CLOSED** | 1.61 | Vkxnb8QG dual-pass; desk tm/fitz all fail |
| `other384` | tm_* | **CLOSED** | 2.28 | 1YNv6Ymk dual-pass; diffts63/504 0.32-0.45 |
| `snt7 / snl27` | news sentiment | **CLOSED** | 2.03 | QPveY7Kg dual-pass (leading gap) |
| `news81` | btc news full-market | **DEAD** | - | cov=0 in TOP500 -> dead-end |
| `analyst7 / news38 / news48` | news/pnl | **DEAD** | - | cov=0 in TOP500 -> dead-end |
| `risk60` | datatime 12-13Y time-invariant | **DEAD** | - | cov 1.0 but ZERO cross-sec signal |

## 三、跨区引擎迁移实证表（本轮核心方法论）

| 引擎 / 机制 | 迁移结论 | 实测证据 |
|---|---|---|
| OIBD accel (USA 1.73 -> DEU) | **PARTIAL** | 1.73@DEU vs 4.44@USA; TOP500 wide-cap hard ceiling |
| EPS/revenue accel | **OK** | DEU model28 drift 1.10 = same family scaled |
| Model-inferred vol / low-vol anomaly | **REJECTED** | DEU asset_vol 0.16 / REVERSE sign |
| Model-inferred leverage | **REJECTED** | DEU -0.15 / -0.79 NEG |
| Momentum / TF | **REJECTED** | cluster + prod 0.98 |
| Same skeleton must pick field | **CONFIRMED** | drift 1.10 vs vol 0.16 vs lev NEG |
| Slow-var 1st accel > level | **CONFIRMED x3** | DEU oiadpq + drift, USA EPS |
| TF alpha cluster > bet same field | **CONFIRMED** | news38 128 -> news81 0; bet group not alpha |

## 四、待用户裁定项

1. **QPveY7Kg leading gap（2014-2018 五年空窗）**：S 2.03 / self 0.02 最强候选，但按「禁连续多年空窗」口径应除名。除名则提交篮 4 颗；保留则 5 颗（S>2 全灭）。

2. **提交授权**（不可逆 POST）：bl62jGgM / 1YNv6Ymk 的 prod 撞墙概率预估（add-5 腿高 / 单字段低），是否按此概率顺序排队提交。

3. **5 个 trio×非trio 名额**已占满 5/5，后续组合类候选不再受理。


## 五、下一轮建议（跨区方法论落地）

1. **TF/多数据集 CLUSTER 出 alpha**：news38 跨 3 data31 128 条全过 vs news81 单集 0 条 ⇒ 优先组「数据集 cluster」而不是赌单集。

2. **慢变量一阶加速度**（ts_mean(252)−ts_mean(504)）已是三区验证的黄金骨架，找下一个慢变量字段（利率/商品/汇率/宏观）。

3. **低波/杠杆/方差类模型推断字段不再优先**（两区证伪）；水平类才可能有信号但撞 prod。

4. **TOP500 wide-cap 天花板已证**：DEU/USA 皆是；找 alpha 要往「冷字段 × 借贷费率分母」这类挤压型信号走。
