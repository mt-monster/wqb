# 疯狗模式 PPA 挖掘进展（ASI，2026-10-22）

## 一、学习了什么（帖子 `44317394262423`【疯狗模式】）

**核心结构**：两个字段各自分桶后做笛卡尔积，得到一个**高基数合成分组轴**，再在轴内对 data 排序。

```
group_rank(<data>, group_cartesian_product(bucket(rank(g1), range="0.2,1,0.2"),
                                          bucket(zscore(g2), range="-4,4,1")))
```

作者结论：**「PC 平均较低，但的确有信号」**；PPA theme 要求同 Category；豁免分组字段不被 PPA 支持 ⇒ 该模式与 PPA 天然契合。

**但它没写、我实测补上的两点**：
1. **「随机 data」是最容易误读的地方** —— 纯随机 data 在本区 10/10 无信号；作者自己补了一句「随机也可以改成让 AI 来帮你选择」，这句才是可用的部分。
2. 它解决的是**相关性**，不是**盈利强度**。

---

## 二、PPA 的真实闸门（已从代码核实，不是猜）

```python
PPA_CHECK_NAMES = {LOW_TURNOVER, HIGH_TURNOVER, LOW_SUB_UNIVERSE_SHARPE,
                   LOW_ROBUST_UNIVERSE_SHARPE, LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO,
                   LOW_ROBUST_UNIVERSE_RETURNS, LOW_INVESTABILITY_CONSTRAINED_SHARPE}
```

| 事实 | 含义 |
|---|---|
| **不含** `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y` / `LOW_ASI_JPN` | PPA 门槛确实低于 RA |
| **含全部 robust 三项** | **robust 不是 RA 专属闸**（我一开始判错了，已更正） |
| 无 Sharpe 下限 | ⚠ **近零 S 的 alpha 会「假通过」**，必须自加 S≥1.0 / F≥1.0 前置 |

---

## 三、本轮实际产出

### 3.1 已验证的最好一条：`1YjNMGWK`

```
ts_mean(subtract(0.5, group_rank(corr_last_trade_price_with_volume,
        group_cartesian_product(bucket(rank(std_bid_price_first_quarter_volumeclock), range="0.2,1,0.2"),
                                bucket(rank(kurtosis_ask_price_interval), range="0.1,1,0.1")))), 3)
ASI / MINVOL10M / D1 / decay 30 / INDUSTRY / trunc 0.08
```

| 项 | 值 | PPA 线 |
|---|---:|---|
| Sharpe | **1.45** | ≥1.0 ✅ |
| Fitness | **1.01** | ≥1.0 ✅ |
| Turnover | 0.183 | 1~70% ✅ |
| self_corr | **0.391** | <0.7 ✅ |
| **PPAC** | **0.083** | <0.5 ✅ |
| robust 比例 | **0.717** | ≥0.90 ❌ |
| **ppa_failed** | **2** | 0 ❌ |

**结论：不是合格 PPA。** 只差 robust。

### 3.2 三条实测杠杆（按效果排序）

1. **`neutralization=INDUSTRY` 是 F 的主杠杆**

   | neut | 最高 S | 最高 F |
   |---|---:|---:|
   | **INDUSTRY** | 1.53 | **0.98** |
   | SUBINDUSTRY | 1.55 | 0.94 |
   | SECTOR | 1.35 | 0.86 |
   | MARKET | 1.23 | 0.79 |

2. **`ts_mean(·,3)` 是 PPA 线正确的降 TO 算子**：TO 0.374→0.204，margin 4.97→8.93bp（+80%），F 0.72→0.86。
   而 **`hump` 彻底摧毁信号**（S 1.45→0.45）、**`ts_decay_linear` 只降 TO 不升 margin**。

3. **`decay 30` 优于 20/15/10**（同 INDUSTRY）：F 0.91~0.98 → 0.89~**1.01**。

### 3.3 疯狗模式的价值被量化

`1YjNMGWK` 的 **PPAC = 0.083、self = 0.391** —— 帖子「PC 平均较低」**成立**。
合成分组轴确实造出了与 Power Pool 几乎不相关的持仓。

### 3.4 换 data 字段失败

`corr_last_high_with_interval_{ask_2,bid,high_2,low,twap,vwap}` 与 `momentum_ask_price_*` 共 10 个字段，
全部 **S ≈ 0（−0.78 ~ 0.31）** ⇒ **`corr_last_trade_price_with_volume` 是不可随手替换的强方向字段。**

---

## 四、当前战绩与唯一阻塞点

| 项 | 状态 |
|---|---|
| **合格 PPA** | **0 / 10** |
| 卡点 | **robust 比例 0.717~0.880，需 ≥0.90**（9/9 全族同样 2 项 FAIL） |
| 已解决 | S、F、TO、self、PPAC、算子数、字段数、ATOM |

**robust 是这一族的共同墙**，且与 F 反向：把 F 推到 1.01 的那条（decay 30）robust 反而最差（0.717）。

---

## 五、下一步（已定位方向）

robust = 「可扩展 universe 上的表现保持」。本轮 mad-dog 的**轴字段多为长尾微结构字段**
（`std_bid_price_first_quarter_volumeclock`、`kurtosis_ask_price_interval`），
在扩容 universe 上覆盖/稳定性差，最可能是 robust 崩的原因。

**处方**：
1. 轴字段改用**高覆盖 + 粗粒度**类（`mean_bid_ask_size_ratio_daily`、`momentum_vwap_daily`、
   `slippage` 日频聚合、`vwap_to_*` 比率）
2. 并测 `truncation 0.05`（分散持仓）

**资源现状**：日仿真余量 ~250；REGULAR 配额今日剩 1 颗（PPA 不占此额度，但只能在 web UI 手工提交）。

---

*批次：wave611 校准 → wave612/613 定位信号与方向 → wave614b 降 TO 谱 → wave616 中性化网格 → wave617 decay 微调 → wave618 换字段；*
*共约 70 次仿真、8 批。证据链见 `.workbuddy/memory/2026-10-22.md` §四~§七。*
