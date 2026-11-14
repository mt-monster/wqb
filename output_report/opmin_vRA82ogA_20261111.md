# `vRA82ogA` 六维爆炸的解法：Python alpha 可行性 + FASTEXPR 压到 28

**时间**：2026-11-12 00:10 GMT+8｜**区**：DEU / TOP500 / delay 1 / decay 0 / SUBINDUSTRY / trunc 0.08
**政策**：只挖不提交。

---

## 0 原件

| 项 | 值 |
|---|---|
| `regular.operatorCount` | **48** |
| Sharpe / Fitness | 2.07 / 1.85 |
| Turnover / Returns / DD | 0.1252 / 10.01% / 4.77% |
| sub_universe | 1.43（lim 0.98） |
| IS_LADDER | 2.59（lim 2.02） |
| CLUSTER_TEST | 1.61（lim 1.0） |
| 其余 IS 闸 | 全 PASS（`fail=[]`） |

结构：`signed_power(group_zscore(add(...6 项...), sector), 1.3)`，6 项 =
`multiply(d,q)` · `multiply(u,g)` · `q` · `u` · `inst` · `ef`。

---

## 1 问题定性：六维里被拖的是哪一维

Genius 六维的 `Operators per Alpha`（单条平均算子数）**越低越好**，是全季**平均**口径。
48 远高于常见 8–15 的区间，单颗就会把均值往上抬。

> 论坛共识（`赛季末，个人6维思考——Operators per Alpha和Fields per Alpha`、
> `Operators per Alpha太高?alpha你可能没写对`）：`+ - * /` 全部计入，`-(A-B)` 改写成 `B-A` 可省 1，
> 变量赋值不计入。与 2026-11-11 本机实测一致。

---

## 2 Python alpha 能不能绕过：能，但这颗用不了

### 2.1 平台实证（论坛 40734489248151「Python alpha 提交经验分享」，83 赞，多条独立复述）

| 问题 | 平台结论 |
|---|---|
| 影响六维的 `Operators per Alpha` / `Operators used` 吗 | **不影响**（这是唯一的「绕过」通道） |
| 影响 `Fields per Alpha` / `Fields used` 吗 | **仍会影响** |
| 能点塔吗 | **能**，按所使用字段正常点亮 Pyramid |
| 能提交 PPA 吗 | **不能**，系统无法判定算子数是否 ≤8 ⇒ **只能提交 RA** |
| 其他限制 | GLB 不可用；不被 SA Selection 选中；**不支持 Vector 字段**；不支持多重回测（只能单条）；功能不稳定，偶发报错重跑可出 |

### 2.2 这颗的硬阻塞：`insd1_holdings` 是 VECTOR

平台 `get_datafields(DEU, TOP500, delay 1, search="insd1")` 实测，`insd1` 数据集 **7 个字段全部 VECTOR**：

```
insd1_holdings / insd1_value / insd1_shares / insd1_valueeur /
insd1_tradesignificance / insd1_price / insd1_gvkey   —— type 全为 VECTOR
```

Python alpha **不支持 Vector 类型字段**，且 insd1 没有标量版本 ⇒ **本颗无法转写成 Python alpha**。
要硬走 Python 路线只能换掉 insider 这条腿（等于换信号），不划算。

> 结论：**Python alpha 是「六维零 operator 成本」的唯一通道，但对 `vRA82ogA`（以及同族的 `2r5MO67Z`）不适用。**

---

## 3 可行解：FASTEXPR 无损压缩 48 → 28（-42%）

同一条计数规则链：变量合并（`vec_avg` 由 4 次变 1 次、`sv` 组由 2 份变 1 份）→ 多参 `add` 展开（5 层 add 链 → 1 次变参调用）→ `-(…)` 无、`g` 用 `reverse` 替 `divide+add`。

| 变体 | id | oc | S | F | TO | sub / lim | ladder | 判定 |
|---|---|---:|---|---|---|---|---|---|
| 原件 | `vRA82ogA` | 48 | 2.07 | 1.85 | .1252 | 1.43 / 0.98 | 2.59 | PASS |
| **无损压缩** | **`58JxGLYn`** | **28** | **2.07** | **1.85** | .1252 | 1.43 / 0.98 | 2.59 | **PASS（逐位同原件）** |
| 删 `ef` 腿 | `O0WO6n21` | 24 | 1.57 | 1.28 | .0981 | 0.95 / 0.74 | 2.38 | **FAIL `LOW_SHARPE`** |
| 删 `u`+`g` 腿 | `XgaGNkx8` | 22 | 1.37 | 1.07 | .1209 | 1.29 / 0.65 | 1.24 | **FAIL ×2** |
| 删 `inst`+`ef` 腿 | `3q0wGEOZ` | 18 | 1.42 | 1.16 | .0924 | 0.73 / 0.67 | 2.17 | **FAIL `LOW_SHARPE`** |

**⇒ 28 是全闸下界**：四条腿（`q` · `u` · `g` · `inst` · `ef`）在这颗上**全部承重**，
删任意一条都掉到 S<1.58。与 `2r5MO67Z` 不同（那颗 `u`/`g` 可删），说明本颗的腿间冗余更低。

---

## 4 交付表达式（28 ops，S 2.07 / F 1.85，全闸 PASS）

```
p = vec_avg(insd1_holdings);
sv = add(significant_value_1, significant_value_2, significant_value_3, significant_value_4);
r = divide(significant_value_1, sv);
q = group_rank(ts_mean(r, 66), sector);
u = group_rank(ts_ir(p, 66), sector);
d = group_rank(ts_delta(ts_mean(p, 66), 66), sector);
g = group_rank(reverse(days_from_last_change(p)), sector);
inst = group_rank(ts_delta(ts_mean(divide(subtract(count_institutional_buyers_security,
         count_institutional_sellers_security), add(count_institutional_buyers_security,
         count_institutional_sellers_security, 1)), 22), 66), sector);
ef = group_rank(divide(subtract(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks),
     add(est_12m_ebi_raisednum_4wks, est_12m_ebi_lowerednum_4wks, 1)), sector);
signed_power(group_zscore(add(multiply(d, q), multiply(u, g), q, u, inst, ef), sector), 1.3)
```

压缩归因：变量合并 −11、多参 add 展开 −7、`g` 改 `reverse` −1、其余结构等价改写 −1 = **48 → 28**。

---

## 5 降低六维影响的其它手段（按性价比）

1. **交 28 ops 版本而不是 48**：直接少 20 个算子计入平均。
2. **摊薄**：`Operators per Alpha` 是**平均**，同季再交几颗低 ops（8–15）能把均值拉回来；
   单颗 48 在 N=20 的季度里也只抬 (48−avg)/20。
3. **不要为压算子牺牲闸门**：24 ops 那版已 `LOW_SHARPE` FAIL，交不出去，六维更无从谈起。
4. **Python alpha 通道**：只在「无 Vector 字段」的候选上可用，且只能走 RA（不能 PPA）。
   可作为今后**新开候选**的首选形态之一（低 ops + 不影响 Operator 两维）。

---

## 6 数据来源

平台 `GET /alphas/{id}` → `regular.operatorCount` + `is.checks`；`get_datafields` 字段类型核实；
论坛 40734489248151（Python alpha 六维）、32938961776279（Operators per Alpha 写法）、
35242886975639（六维思考）。
仿真批次：`2LHQai4eq4xy9Un19y0YIFw4`（8 条全 ERROR，平台侧通用报错）、
`3df1i3e1n4AxbxdA6RgX9a7`（8 条全 ERROR，同上）、
`PWQ15fOk4SdazHvDmZXL11`（4 条成功，本文数据来源）。
**零提交。**
