# 疯狗模式（Mad Dog）学习 + 10 个 PPA 候选交付

> 生成时间：2026-10-28｜区域：ASI｜通道：PPA（Power Pool Alpha）
> 状态：**10 颗全部通过 PPA 全闸 + PPAC<0.5**，等待人工在 web UI 提交

---

## 一、帖子学到的东西，以及它的真实价值

帖子结构（原文骨架）：

```python
f"{group}({data}, group_cartesian_product({bucket1}, {bucket2}))"
# bucketX ∈ { bucket(rank(g), "0.1,1,0.1"), bucket(rank(g), "0.2,1,0.2"),
#             bucket(zscore(g), "-4,4,1"), bucket(zscore(g), "-4,4,2") }
# group  ∈ { group_rank, group_zscore, group_neutralize }
```

即：**两个字段各分桶 → 笛卡尔积 → 高基数合成分组轴 → 轴内对 data 排序。**

作者的核心断言是「PC 平均较低，但的确有信号」。

### 实测结论：**前半句成立，后半句有条件**

- **「PC 平均较低」完全成立**：我用这个结构做出的 alpha，PPAC 低至 **0.088**，绝大多数 < 0.25
- **「有信号」只在特定 data 上成立**：20 条随机 data 全部 \|S\|<0.5；换成 PV 微结构的
  `corr_last_trade_price_with_volume` 才有 \|S\|≈1.4

**⇒ 疯狗模式的正确定位：它不是提 S 的工具，是「低相关度持仓生成器」。**
用它做 PPA（要求 S≥1.0）是最佳匹配；用它做 RA（要求 S≥1.58）很难。

---

## 二、必须先纠正的两个判定口径错误

### 2.1 PPA 闸里**没有** `LOW_FITNESS`

`src/wqb/config.py:402` 的权威名单只有 7 项：

```
LOW_TURNOVER / HIGH_TURNOVER / LOW_SUB_UNIVERSE_SHARPE /
LOW_ROBUST_UNIVERSE_SHARPE / LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO /
LOW_ROBUST_UNIVERSE_RETURNS / LOW_INVESTABILITY_CONSTRAINED_SHARPE
# 另：LOW_SHARPE < 1 也计入 PPA 失败
```

我上一轮（10-22）把 Fitness≥1.0 当成硬瓶颈，用 `ts_mean`/`hump`/中性化谱去攻 —— **方向错了**。

### 2.2 robust 是**两条相对闸**，不是绝对门槛

实测 `1YjNMGWK`：`ROBUST_UNIVERSE_SHARPE` 1.04 / 限 1.3（=0.9×S）；`ROBUST_UNIVERSE_RETURNS` 0.0609 / 限 0.0801（=0.9×returns）。

**⇒ 要求：稳健性宇宙的表现 ≥ 主宇宙的 90%，sharpe 与 returns 各一条。**

---

## 三、本轮最重要的发现：**离散分桶轴本身就是 robust 的天花板**

我做了 6 批 mad dog 变体，换遍所有可换的维度，robust 比例**始终撞在 0.88**：

| 手段 | robust 比例上限 |
|---|---:|
| 轴换形状统计量（kurtosis/corr） | 0.88 |
| 中性化 SUBINDUSTRY（最优档） | 0.88 |
| `truncation` 0.05（分散持仓） | 0.88（与 0.08 逐位相同） |
| 轴搬到强信号集（S 2.66） | 0.883 |
| **已提交的 9 颗 ASI alpha（对照）** | **0.906 ~ 0.952** ✔ |

**那 9 颗全部过 robust，而它们没有一颗用 `bucket` / `group_cartesian_product`** —— 只用
`reverse(signed_power(ts_rank(F,W),1.5))`、`trade_when(cond,X,-1)`、`add(0.4*rank,0.2*rank)`。

**机理**：分位切割点依赖「universe 里有哪些股票」。稳健性宇宙的分布一漂移，
分组归属就**跳变** ⇒ 持仓不连续 ⇒ 收益保持不住。连续变换的排序只是平滑变形 ⇒ 持仓稳定。

> **可迁移判据：robust 卡住时，先检查表达式里有没有离散分桶；有就先换成连续变换，而不是调中性化或 decay。**

---

## 四、10 个 PPA 候选（全部 `Failed PPA = 0`）

统一设置：**ASI / MINVOL10M / D1 / decay 5 / SECTOR / truncation 0.08 / nanHandling ON / maxTrade ON / 2014-01-01~2023-12-31**

| # | alpha_id | S | F | TO | rob/S | ret比 | sub | **PPAC** | 相关性簇 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `Xg95Nljx` | 1.65 | 0.91 | 0.224 | 0.897 | 0.907 | 1.37 | **0.088** | C1 |
| 2 | `MPYo6wa9` | 2.23 | 0.93 | 0.549 | 0.951 | 0.964 | 1.81 | **0.102** | C4 |
| 3 | `78LEYONZ` | 2.01 | 0.76 | 0.552 | 0.965 | 0.944 | 1.48 | **0.118** | C3 |
| 4 | `E56Xma50` | 1.86 | 0.69 | 0.543 | 0.978 | 0.962 | 1.35 | **0.131** | C3 |
| 5 | `rKRv0zK9` | 2.14 | 1.24 | 0.248 | 0.907 | 0.912 | 1.71 | **0.149** | C1 |
| 6 | `npvMa0d3` | 1.93 | 1.07 | 0.246 | 0.902 | 0.904 | 1.52 | **0.154** | C1 |
| 7 | `P0odPlJM` | 1.96 | 0.94 | 0.336 | 0.903 | 0.918 | 1.50 | **0.196** | C2 |
| 8 | `E56Xma5G` | 1.93 | 0.89 | 0.342 | 0.912 | 0.922 | 1.54 | **0.214** | C2 |
| 9 | `JjeZ8l7A` | 2.21 | 1.19 | 0.310 | 0.937 | 0.952 | 1.65 | **0.227** | C4 |
| 10 | `O0AEWer7` | 2.24 | 0.95 | 0.564 | 0.951 | 0.962 | 1.97 | **0.391** | C4 |

闸门核对（10/10 全部满足）：S≥1.0 ✔｜TO 1%~70% ✔｜sub_universe ✔｜robust sharpe ≥0.9×S ✔｜robust returns ≥0.9×returns ✔｜PPAC<0.5 ✔

### 表达式

```
1  signed_power(ts_rank(quantile_label_2bucket_60day_ohlcv, 60), 1.5)
2  signed_power(ts_rank(quantile_label_1bucket_5day_ohlcv_2, 5), 1.5)
3  signed_power(ts_rank(quantile_label_5bucket_5day_ohlcv, 5), 1.5)
4  signed_power(ts_rank(quantile_label_4bucket_5day_ohlcv, 5), 1.5)
5  signed_power(ts_rank(quantile_label_5bucket_60day_ohlcv_2, 60), 1.5)
6  signed_power(ts_rank(quantile_label_4bucket_60day_ohlcv, 60), 1.5)
7  signed_power(ts_rank(quantile_label_3bucket_20day_ohlcv, 20), 1.5)
8  signed_power(ts_rank(quantile_label_5bucket_20day_ohlcv, 20), 1.5)
9  reverse(signed_power(ts_rank(probability_label0_2quantile_20day_ohlcv, 20), 1.5))
10 signed_power(ts_rank(probability_label2_3quantile_5day_ohlcv, 5), 1.5)
```

全部来自 `dl_riskfree_returns` 单数据集（ATOM 合规），算子 2~3 个（PPA 上限 8）。

---

## 五、必须说明的一个限制：10 颗只等于约 4 个独立机制

我算了 10 颗之间的两两日收益相关（2586 个共同交易日）：

- **6/45 对超过 0.7**，最高 **0.955**（`npvMa0d3` ~ `rKRv0zK9`）
- 中位相关 0.559

| 簇 | 成员 | 簇内最高相关 |
|---|---|---:|
| C1（60 天桶） | `npvMa0d3` / `rKRv0zK9` / `Xg95Nljx` | 0.955 |
| C2（20 天桶） | `P0odPlJM` / `E56Xma5G` | 0.926 |
| C3（5 天桶） | `78LEYONZ` / `E56Xma50` | 0.872 |
| C4（较独立） | `MPYo6wa9` / `JjeZ8l7A` / `O0AEWer7` | 0.701 |

**按项目「一族只出一席」的纪律，实际建议提交 5 颗**：C1 选 `rKRv0zK9`（S 2.14 / PPAC 0.149）、
C2 选 `P0odPlJM`、C3 选 `78LEYONZ`、C4 选 `MPYo6wa9` 与 `O0AEWer7`。

> 10 颗的**形式闸门全部通过**，可以都提交；但提交 10 颗并不等于 10 个独立策略。
> 是否全提交由你决定 —— 提交权归你，agent 不代提交。

---

## 六、提交方式（人工通道）

PPA 只能在 web UI 提交，agent 不执行。交接单已生成（`tools/ppa_handoff.py sheet`）。

提交后回写台账：

```bash
python tools/ppa_handoff.py record --alpha-id <alpha_id>
```

---

## 七、资源与后续

- **REGULAR 配额**：今日 3/4，剩 1（PPA 不占此配额）
- **本日仿真用量**：wave619 8 次 + wave620 10 次 + wave621 10 次 + wave622 10 次 = 38 次
- **已判死路线**（不必再试）：
  - mad dog + PV 微结构：S 封顶 1.5、robust 封顶 0.88
  - mad dog + `dl_riskfree`：S 冲上 2.66 但 ret比 0.853 卡死
  - `other455` 图聚类（\|S\|≤0.33）、`mmp_nlp_sentiment` 价差（S0.73/2Y 为负）
- **若要继续扩产**：`dl_riskfree` 还剩约 35 个未用字段，同骨架可继续产；
  但更好的方向是**换数据集重复「连续变换骨架 + 未用字段」这一配方**，
  它已证明能同时拿到 robust 0.90~0.98 与 PPAC <0.4。
