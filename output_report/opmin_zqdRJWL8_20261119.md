# zqdRJWL8 第三颗战役（DEU/D1/SENTIMENT 塔）

日期：2026-11-19 20:07–21:30　区域：DEU / TOP500 / D1
塔：`DEU/D1/SENTIMENT` ×**1.8**（当季 **2/3**，差 1 颗点亮）

---

## §1 目标定义：为什么"继续优化 zqdRJWL8"等于"补第三颗"

`zqdRJWL8` 本身是未提交的源件：

```
group_rank(ts_zscore(vec_avg(snl27_kurtosis), 44), market)
```
S 1.26 / F 0.64 / TO 24.59% / sub 1.06 / 2Y 1.73｜3 FAIL（LOW_SHARPE、LOW_FITNESS、CONCENTRATED_WEIGHT）

但它的优化版 **`vRAvXvZb` 已经 ACTIVE**：

```
d = ts_backfill(vec_avg(snl27_totaldomains), 22);
k = ts_backfill(vec_avg(snl27_kurtosis), 8);
group_rank(ts_target_tvr_hump(ts_zscore(pasteurize(multiply(k, inverse(power(d, 2.25)))), 48), target_tvr=0.215), sector)
```
S 1.63 / F 1.02 / 2Y 2.31 / sub 1.12 / self 0.3276 / prod 0.5614｜全闸通过｜六维 ops 8 + T3 +3 + T4 +2

### 关键读数：原骨架本身就是孪生件

`compute_mutual_correlation(["zqdRJWL8", "vRAvXvZb"])` ⇒ **0.8702**（6 年日频，1539 点）

⇒ **把 `zqdRJWL8` 优化到全闸的路线在数学上就不通**：它的任何形态都会与已提交件 0.87 相关。

**故本轮真实目标 = 为 `DEU/D1/SENTIMENT` 塔产出第三颗**（倍率 1.8×，全账户最高档之一），且必须与现有两颗都 <0.7。

## §2 塔内现有两颗的身份

`get_user_alphas(stage=OS, region=DEU)` 实测：

| 件 | 信息源 | S | F | TO | self | prod |
|---|---|---|---|---|---|---|
| **`vRAvXvZb`**（`DEU_R_snl27kurt_01`） | `snl27_kurtosis × totaldomains^-2.25` | 1.63 | 1.02 | 20.2% | 0.3276 | 0.5614 |
| **`bl6OWZ2M`**（`DEU_R_alpha_01`） | `snt7_all_languages_views` + `snl27_relpopularity08` 正交化 | **2.03** | **1.61** | 16.1% | **0.0306** | 0.6671 |

`bl6OWZ2M` 的表达式（本轮最重要的线索）：

```
a = ts_backfill(vec_avg(snt7_all_languages_views), 22);
vector_neut(ts_quantile(ts_ir(ts_mean(max(a, ts_delay(a,5)), 5), 22), 252, driver="gaussian"),
            ts_backfill(vec_avg(snl27_relpopularity08), 22))
```

⇒ `sentiment7` 必须经 **`ts_backfill(22)` → `max(a, ts_delay(a,5))` → `ts_mean(5)` → `ts_ir(22)` → `ts_quantile(252)` → `vector_neut`** 六层稳定化才能用。

---

## §3 sentiment27：封闭（字段已被耗尽）

报告 `opmin_zqdRJWL8_20261118.md` §4.3 已在同一骨架下扫完全部 11 个数值字段：

| 字段 | S | 判定 |
|---|---|---|
| **`snl27_kurtosis`** | **1.26** | 唯一有效 |
| `snl27_totaldomains` | 0.87 | 次优 |
| `snl27_skewness` | 0.54 | 弱 |
| `snl27_top50pctranking` | 0.23 | ≈0 |
| `snl27_avgranking` | 0.20 | ≈0 |
| `snl27_relpopularity08` / `1` | 0.19 / 0.15 | ≈0 |
| `snl27_topranking` | 0.09 | ≈0 |
| `snl27_top50/75pctrankingavg` | 0.03 / 0.02 | ≈0 |
| `snt27_rank` | −0.03 | ≈0 |

⇒ **只有"分布形态"（高阶矩）携带 alpha，"分布位置"系全无信息。**

### 3.1 本轮再测 10 种 kurtosis 变体（全部失败）

| 形态 | S | F | TO | 2Y | sub | FAIL |
|---|---|---|---|---|---|---|
| `ts_kurtosis(ku, 66)` | 0.81 | 0.42 | 14.8% | 1.72 | −0.63 | 3 |
| `ku × skewness` | 0.75 | 0.28 | 26.5% | 1.28 | −0.40 | 5 |
| `ku / skewness` | 0.72 | 0.26 | 27.2% | 1.14 | 0.36 | 4 |
| `ts_rank(ku, 252)` | 0.68 | 0.25 | 23.1% | 1.15 | 0.53 | 4 |
| `ts_delta(ku, 22)` | 1.13 | 0.49 | 29.9% | 1.96 | 0.76 | 3 |
| 分母 `totalcountrydomains^2` | 1.05 | 0.53 | 20.2% | 1.34 | 0.98 | 4 |
| 分母 `avgranking` | 0.96 | 0.43 | 22.6% | 0.83 | 0.35 | 5 |
| 分母 `top50pctrankingavg` | 1.15 | 0.57 | 22.4% | 1.32 | 0.37 | 5 |
| `ku × relpopularity1` | 0.99 | 0.41 | 27.6% | 1.30 | 0.57 | 4 |
| **`ku / totaldomains`（不取幂）** | **1.40** | 0.70 | 27.3% | 1.75 | **1.03** | 3 |

**⇒ 确认 `^2.25` 幂次是 kurtosis 的唯一峰值（报告 §11 的 11 点扫描），该字段已耗尽。**

---

## §4 sentiment7：找到 5 颗 0 FAIL，但全部撞孪生封死

### 4.1 第一批（10 形态，未用稳定链）—— 全部失败

| 形态 | S | TO | 2Y | sub |
|---|---|---|---|---|
| `views` w44 / w22 / w88 | 0.61 / 0.49 / 0.55 | **85% / 88% / 82%** | −0.19 / −0.46 / −0.20 | −0.27 / −0.28 / −0.27 |
| `all_languages_views` | 0.62 | 84.6% | −0.10 | −0.18 |
| `ts_delta` / `ts_returns` | 0.59 / 0.62 | 82.6% / 83.1% | −0.04 / 0.09 | −0.08 / −0.07 |
| 语言占比 | 0.30 | 77.0% | 0.36 | −0.06 |

**TO 85% 的根因**：`vec_avg(snt7_*)` 后序列每日剧烈跳变（cov 0.7357，股票进出频繁）。⇒ 必须用 `bl6OWZ2M` 的六层稳定链。

### 4.2 第二批（稳定链 + 换正交化基）—— 5 颗 0 FAIL

| 件 | 正交化基 | S | F | 2Y | sub | TO | invest |
|---|---|---|---|---|---|---|---|
| **`O0WNkAbd`** | 双层（relpop + totaldomains） | **1.99** | **1.50** | 2.43 | **1.11** | 17.9% | 1.51 |
| **`omaLvE9J`** | totaldomains | 1.96 | 1.47 | 2.42 | **1.11** | 17.9% | 1.45 |
| **`Jj8Nmegm`** | avgranking | 1.91 | 1.41 | 2.40 | 1.05 | 17.9% | 1.39 |
| **`npadovZ8`** | skewness | 1.91 | 1.42 | 2.18 | 0.93 | 18.1% | 1.35 |
| **`88NjrRao`** | kurtosis | 1.87 | 1.39 | 2.27 | 0.98 | 18.1% | 1.22 |
| `mLamAoqK` | `ts_ir` 窗口 66 | 1.98 | **1.54** | 2.28 | 1.09 | 19.7% | 1.17（1 FAIL） |
| `omaLvE3J` | 信号源换 `snt7_views` | 0.92 | 0.49 | 1.41 | 0.46 | — | 3 FAIL |
| `pdaREdn6` | 去掉 `ts_quantile` | 1.17 | 0.72 | 1.30 | 0.33 | — | 4 FAIL |
| `vRAr91dw` | `ts_zscore` 替 `ts_ir` | **−0.50** | — | −1.26 | −0.83 | — | 4 FAIL |

**承重件确认**：`ts_ir` 不可替代（换 `ts_zscore` → S −0.50）、`ts_quantile` 必需（去掉 → S 1.17）、`ts_mean` 5 天最优（改 22 → S 1.34）、信号源必须 `all_languages_views`（换 `views` → S 0.92）。

### 4.3 互相关：全部撞孪生封死

| 件 | vs `bl6OWZ2M` |
|---|---|
| `O0WNkAbd` | **0.9849** |
| `omaLvE9J` | **0.9843** |
| `Jj8Nmegm` | **0.9810** |
| `npadovZ8` | 0.8056 |
| `88NjrRao` | **0.7938（最低）** |

且 `O0WNkAbd`/`omaLvE9J`/`Jj8Nmegm` 三件彼此 **0.99+**；`npadovZ8`/`88NjrRao` 彼此 **0.9816**。

**⇒ 信号主体（`snt7_all_languages_views` 的 `ts_ir`）是共同的，换正交化基只能把相关从 0.985 削到 0.794，仍 >0.7。**

---

## §5 sentiment33：NLP 情绪，两个方向都不通

### 5.1 字段结构

**255 字段 = 5 组关键词 `fkw1..fkw5` × 9 种方法 `method_1..9` × {pos/neg/neut/obj} [× raw/filtered]**，覆盖率全部 **0.3152–0.3258**（TOP500 中约 163 只票）。

最热门字段：`fkw1_method_3_neg`（alphaCount 12 / 8 用户）＞`fkw1_method_3_filtered_neg`（8/7）＞`fkw1_method_2_filtered_obj`（6/5）＞`fkw1_method_2_filtered_neg`（5/4）＞`fkw1_method_3_pos`（4/4）。

### 5.2 第一批（未稳定化）—— 全部失败，同样 TO 爆表

| 形态 | S | TO | DD | 2Y | FAIL |
|---|---|---|---|---|---|
| Method3 净情绪 | 0.22 | **88.8%** | **70.6%** | −1.89 | 6 |
| Method3 filtered neg | 0.46 | 88.4% | 44.2% | −0.80 | 6 |
| Method2 filtered 净情绪 | 0.11 | 88.7% | 69.5% | −1.90 | 6 |
| Method2 filtered obj | 0.06 | 81.9% | 60.8% | −1.07 | 6 |
| Method3 净情绪 `ts_delta` | −0.32 | 38.4% | 39.2% | −0.14 | 4 |
| **情绪波动（`ts_mean(abs(ts_delta),66)`）** | **0.61** | **6.1%** | 20.0% | 0.28 | 4 |
| fkw2 Method3 filtered pos | 0.38 | **95.3%** | 40.8% | −0.76 | 6 |
| fkw3 Method4 pos | 0.34 | 85.5% | 35.1% | −0.76 | 6 |
| model7 score1 fkw4 | 0.37 | 82.7% | 35.1% | −0.05 | 5 |
| Method3 neg 占比 | 0.42 | 86.4% | 41.0% | −0.68 | 5 |

**唯一 TO 正常的是"先 `abs(ts_delta)` 再平滑"的波动率版（6.1%）** —— 再次验证"必须先稳定化"。

### 5.3 第二批（套用 `bl6OWZ2M` 六层稳定链）—— 10 条全部 FAIL

平台只返回裸 `FAIL`，无细节。最可能原因：**`ts_ir` 的分母（标准差）对情绪分数恒定的股票为 0 ⇒ 除零产生 INF**。`snt7` 的浏览量是连续大正数所以不触发；`snt33` 的情绪分数大量股票恒为 0。

隔离测试已派发（5 条，逐步加层定位）。

---

## §6 结论

**`DEU/D1/SENTIMENT` 第三颗在现有三个数据集内均不可达：**

| 数据集 | 状态 |
|---|---|
| `sentiment27` | 只有 `kurtosis` 有信号，其最优形态（`^2.25` 幂次）已被 `vRAvXvZb` 占据；任何变体 S ≤1.40 或与原骨架相关 0.87 |
| `sentiment7` | 正确用法（六层稳定链 + relpopularity 正交化）已被 `bl6OWZ2M` 占据；5 颗 0 FAIL 变体全部相关 0.79–0.98 |
| `sentiment33` | 未稳定化时 TO 85%+；稳定化后 `ts_ir` 除零导致整批 FAIL；且覆盖率仅 0.3258 |

**孪生封死在这里表现得极为彻底**：同一信号主体的任何参数/基变换都无法把相关压到 0.7 以下。第三颗只能等平台新增 sentiment 类数据集，或改用完全不同类别的数据集（但那不再属于 SENTIMENT 塔）。

### 本轮有效判据（可复用）

1. **`zqdRJWL8` vs `vRAvXvZb` = 0.8702** —— 源件与其优化版同源，任何"继续优化源件"的请求都该先测这个数。
2. **VECTOR 事件类数据的 TO 陷阱**：`vec_avg` 后直接做时序算子会得到 85%+ TO。必须走 `ts_backfill(22) → max(x, ts_delay(x,5)) → ts_mean(5) → ts_ir(22) → ts_quantile(252)` 六层稳定化。
3. **`ts_ir` 是不可替代的核心算子**（换 `ts_zscore` 直接 −0.50），但它对"恒定值序列"会除零 ⇒ 情绪分数类数据不可用。
4. **正交化基只能改变边缘 1–2%**：5 个不同基的相关跨度仅 0.79–0.985，无法突破孪生阈值。
5. **`ts_std` 不是可用算子**，波动率要用 `ts_mean(abs(ts_delta(x,1)), W)`。

### 5.4 隔离测试：崩溃点已定位，但更重要的结论是「无信号」

把六层稳定链逐层拆开（5 条，全部 COMPLETE 不再 FAIL）：

| 件 | 构造 | S | F | TO | DD | 2Y | FAIL |
|---|---|---|---|---|---|---|---|
| `zqd8PY2O` | `max` + `ts_mean`（最简） | 0.37 | 0.23 | 9.1% | 26.4% | −0.27 | 4 |
| `O0WNbrMd` | + `ts_ir` + `ts_zscore` | 0.20 | 0.10 | 8.8% | 34.2% | 0.21 | 4 |
| `e7abd9Gg` | + `ts_quantile`（无 `ts_ir`） | 0.38 | 0.24 | 9.9% | 22.8% | −0.34 | 4 |
| `2r5waO6w` | + `max`+`mean`+`ts_zscore` | 0.39 | 0.24 | 9.2% | 23.3% | −0.15 | 4 |
| `LLKNg9z2` | 只 `ts_backfill` + `ts_zscore` | 0.03 | 0.01 | 4.8% | 66.9% | 0.87 | 4 |

**两个结论**：

1. **TO 全部回落到 4.8%–9.9%**（对比第一批的 77%–95%）⇒ 稳定链的「压 TO」作用是真实的，与 `sentiment7` 的表现一致。
2. **但 S 全部 ≤0.39、DD 22%–67%** ⇒ **`sentiment33` 的 NLP 情绪分数本身不携带 alpha**。这不是处理链问题（处理链已证明能把 TO 从 89% 压到 9%），而是信息本身无效。

⇒ 上一批 10 条全 FAIL 的具体组合问题（`group_rank(ts_quantile(ts_ir(...)))` 直接串联）已无追查价值，因为即使跑通也无信号。

## §5.5 sentiment33 封盘

| 维度 | 结果 |
|---|---|
| 覆盖率 | 0.3152–0.3258（TOP500 中约 163 只票） |
| 最热字段 | `fkw1_method_3_neg` alphaCount 12、`fkw1_method_3_filtered_neg` 8 |
| 未稳定化 | TO 77%–95%、DD 35%–71%、S ≤0.46 |
| 六层稳定链 | TO 降到 4.8%–9.9%，但 **S 0.03–0.39** |
| 判定 | **无 alpha，封盘** |
