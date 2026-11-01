# GBR/TOP700/D1 塔位权威盘点 + 口径修正（2026-10-30）

> 触发：用户指示「暂不提交，继续挖」。本轮不打仿真，全部用平台只读接口 + 本地库完成。
> 结论先行：**GBR 只剩一条点塔路径 = 提交那 3 条 PV+FUNDAMENTAL 双塔 alpha；其余 11 个真空塔在 GBR 数据侧无可行路径。**

---

## 1. 权威塔位实测（唯一事实源：平台 get_pyramid_alphas + get_pyramid_multipliers）

本季度（2026-10-01 ~ 2026-12-31）GBR D1 已提交分布：

| 塔 | 现值 | 状态 | D1 乘数 | 缺口 |
|---|---|---|---|---|
| **model** | **5** | ✅ 已点亮 | 1.5 | — |
| **analyst** | **3** | ✅ 已点亮 | 1.6 | — |
| **pv** | **1** | 差 2 | 1.4 | 2 |
| **other** | **1** | 差 2 | 1.6 | 2 |
| **fundamental** | **0** | 差 3 | 1.6 | 3 |
| **sentiment** | **0** | 差 3 | **1.7（最高）** | 3 |
| news | 0 | 差 3 | 1.6 | 3 |
| earnings | 0 | 差 3 | 1.3 | 3 |
| institutions | 0 | 差 3 | 1.4 | 3 |
| insiders | 0 | 差 3 | 1.5 | 3 |
| risk | 0 | 差 3 | 1.3 | 3 |
| option | 0 | 差 3 | 1.5 | 3 |
| socialmedia | 0 | 差 3 | 1.3 | 3 |
| macro | 0 | 差 3 | 1.3 | 3 |
| shortinterest | 0 | 差 3 | 1.2 | 3 |
| imbalance | 0 | 差 3 | 1.0 | 3 |

合计已提交 **10 条**（5+3+1+1）。GBR D0 全塔为 0 —— D1 才是战场。

**跨区对照（同季度）**：EUR D1 = analyst 7 / fundamental 3 / model 3 / pv 2 / risk 2 / news 1 / insiders 1 / other 1 / sentiment 1；KOR D1 = shortinterest 4 / fundamental 3 / model 3 / analyst 2 / pv 2 / other 1；IND D1 = pv 9 / news 4 / other 4 / analyst 3 / model 3 / fundamental 3 / risk 3 / macro 2 / earnings 2 / institutions 1。
⇒ 同一塔位在别区能出货（如 KOR shortinterest 4、IND news 4），说明是 **GBR 数据侧材料缺失**，不是平台机制不允许。

---

## 2. 三个必须修正的认知错误（本轮实证推翻）

### 2.1 信用/违约类因子归 MODEL，不归 RISK

| alpha | 字段语义 | 实测塔位 |
|---|---|---|
| `3qVa2Lze` | `annualized_pd_2_year_jc7`（2 年期年化违约概率） | **GBR/D1/MODEL**（`pyramid_short: "model"`，乘数 1.5） |
| `npPWX19w` | `mdl28_sm_structural_multiple_credit_structural_leverage`（信用结构杠杆） | **GBR/D1/MODEL**（`pyramid_short: "model"`） |

⇒ 「找 RISK category 数据集做 RISK 塔」这条路在 GBR 上从前提就错了：**平台的 MATCHES_PYRAMID 归因把信用风险类统一并入 MODEL**。RISK 塔（0/3）在 GBR 事实上被 MODEL 吞并。
⇒ 附带影响：`annualized_pd` 族（ds=111）之前被当作「RISK 塔点亮路径」是误判。该族 7 条全闸通过候选里 4 条 prod 0.99+ 已饱和，**整族对点塔零价值**。

### 2.2 塔位不能从 dataset_id 推断

`dataset_id=291` 一个槽位同时装着两种塔位的候选：

| alpha | 表达式要点 | 塔位 |
|---|---|---|
| `rKRkL9QE` | `divide(fnd6_capxy, cap)` | **PV + FUNDAMENTAL**（effective 2） |
| `WjOkLGWx` | `divide(fnd6_newq_cheq, cap)` | **PV + FUNDAMENTAL**（effective 2） |
| `9qxQamje` | `ts_backfill(tm_17_r1_r5_r10_rh_ah3_glb_d1_r10_q1, 126)` | **OTHER**（effective 1） |

⇒ `dataset_id` 只是「最后一次回测用的数据集标签」，与塔位无因果关系。**任何按 dataset category 映射塔位的盘点都必须重做**（本轮之前的 183 集「未点亮塔数据集三方交叉」结论在方向上仍成立，但判据需要换成塔位实测）。

### 2.3 本地库的近似闸 ≠ 平台闸；`region_id=7` ≠ GBR

反例 `YPxLWdpv`（本地 `region_id=7`、S3.36/F1.49/TO64.66%/2Y1.89）：

```
settings.region = "EUR"        ← 实为 EUR 回测
settings.universe = "TOPCS1600"
longCount 575 + shortCount 825 = 1400
failed_ra_count = 1            ← LOW_SUB_UNIVERSE_SHARPE 1.63 < 1.78，连全闸都没过
pyramids.list = [EUR/D1/OTHER]
```

⇒ 本地 `region_id=7` 会混入 EUR；本地自算的 `sub_universe_sharpe >= 0.4743*sharpe` 只是 GBR 的系数，**别区的 limit 不同**。
⇒ **唯一可信的全闸判据 = 平台 `ra.failed_ra_count` / `checks.fail`**；`get_alpha_details.settings.region` 是唯一可信的区域判据。
⇒ 本轮之前那个「282 条全闸通过池」口径作废。用 `batch_get_alpha_metrics`（含 `failed_ra_count`）重筛。

---

## 3. 两条被判死的路径（本轮新增）

### 3.1 `tm_*` 时序模型族 —— prod 全面饱和，OTHER 塔此路不通

`9qxQamje`（S3.42 / F1.37 / TO53.19% / 2Y2.11 / SUB2.40 / drawdown 2.36% / `failed_ra=0`）归 **OTHER** 塔，看似是 OTHER 0→1 的最强单条，但同字段同骨架的兄弟全部撞墙：

| alpha | 与 9qxQamje 的差别 | prod |
|---|---|---|
| `9qxQamje` | —（`group_rank(·, sector)`） | **未测** |
| `N1NogQ87` | 只把 `sector` 换成 `industry` | **0.8439** |
| `O0Av1nZd` | `ts_av_diff(·,22)` + industry | 0.8333 |
| `kqNlzEAK` | `ts_av_diff(·,22)` + sector | 0.8719 |
| `88R1XNo7` | `ts_av_diff(·,22)` + industry | 0.7736 |
| `3qoLJb16` / `rKRX8Jd1` | `ts_av_diff(·,22)` + subindustry | 0.7945 / 0.7919 |
| `YP1qR9wA` | signed_power 变体 | 0.7716 |
| `npvVQ8WE` | `ts_av_diff(·,40)` | 0.7343 |
| `XgJzLbl1` 等 19 条（`tm_16` 族，ds=257） | 平滑化写法 | 0.8413 / 0.8891 / 1.0 |

⇒ **整个 `tm_*` 族 prod 落在 0.73–1.0**，`9qxQamje` 唯一「未测」只因换了分组轴，不是干净。
⇒ **判死**：`tm_*` 族不投 prod 时隙；OTHER 塔在 GBR 无可用材料（`other47` 8/8、`other384` 6/6、`other455` 探针此前已判死）。

### 3.2 `quant_factor_lib + risk60` —— 权重混合违规，全族弃用

15 条全闸通过候选（`RRAQYp7d` S1.82 / F1.43 / 2Y**2.59**；`LL5a6pdn` 2Y**2.62**）形态全部是：

```
subtract( hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)), hump=0.001),
          multiply(rank(ts_mean(vec_avg(rsk60_offer),22)), 0.5) )
```

- 违规点 1：`multiply(rank(B), 0.3 / 0.5 / 0.7)` 权重混合两个信号；
- 违规点 2：`kqJrX3Pz`(0.3) / `RRAQYp7d`(0.5) / `VkdjX2QA`(0.7) 只扫权重网格 —— 典型混信号调参 + 参数扫描双重违规。

⇒ **判死**，不论指标多好（2Y 2.6 / TO 3.7% 很诱人）都不可用。这是本轮唯一「指标漂亮但因违规被主动放弃」的族。

---

## 4. 唯一的真·增量：`fnd6_xxx / cap` 族 = PV+FUNDAMENTAL 双塔弹药库

平台权威口径（`batch_get_alpha_metrics` 的 `failed_ra_count`）筛出 **10 条全闸通过**，全部同一机制骨架：

```
骨架：rank/group_rank( ts_quantile( ts_av_diff( divide(fnd6_<X>, cap), W ), Q, driver=gaussian ) )
     W ∈ {168, 252}，Q ∈ {56, 84}，外层 rank 或 group_rank(·, industry/subindustry)
```

| alpha | 字段 | S | F | TO | 2Y | SUB | invest_ratio | margin(bp) | prod |
|---|---|---|---|---|---|---|---|---|---|
| `rKRkL9QE` | `fnd6_capxy / cap` | 2.21 | **2.05** | 8.33% | 2.51 | 1.77 | 0.8733 | 25.94 | **0.6783 ✅** |
| `QPveQvOg` | 二阶差分 `av_diff(av_diff(capxy/cap,252),252)` | 2.06 | 1.78 | 7.49% | 2.47 | 1.68 | 0.8786 | 24.86 | **未测 ★** |
| `N1NM5WK8` | `capxy/cap` + `group_rank(industry)` | 2.05 | 1.80 | 8.98% | 2.26 | 1.68 | 0.8927 | 21.40 | 未测 |
| `P0oerpjp` | `capxy/cap` (168/56) | 1.98 | 1.70 | 8.26% | 2.10 | 1.70 | 0.9495 | 22.31 | 未测 |
| `0mYoANkv` | `cap / fnd6_newa2_re`（反向） | 1.89 | 1.54 | 11.66% | 2.08 | 1.12 | 0.7831 | 14.22 | **0.6932 ✅** |
| `6XdxzNb5` | `fnd6_newa2_re / cap` | 1.75 | 1.40 | 11.67% | 2.22 | 1.27 | 0.8114 | 13.64 | 未测 |
| `WjOkLGWx` | `fnd6_newq_cheq / cap` | 1.72 | 1.26 | 9.31% | 2.09 | 0.94 | 0.8488 | 14.53 | **0.6577 ✅** |
| `kqNRXm5k` | `capxy/cap` + `ts_zscore(·,168)` | 1.70 | 1.33 | 7.98% | 2.02 | 1.52 | 0.9647 | 19.05 | 未测 |
| `88RAnmAX` | `cap / fnd6_ewq_teqq` | 1.67 | 1.40 | 12.26% | 1.89 | 1.06 | 0.8982 | 14.39 | 未测 |
| `9qxoa3mx` | `cap / fnd6_cptnewq_ceqq` | 1.59 | 1.35 | 12.25% | 1.89 | 1.00 | 0.8679 | 14.78 | 未测 |
| ~~`RREXA1qn`~~ | `fnd6_cptnewq_atq / cap` | 1.77 | 1.44 | 11.08% | 1.55 | 1.20 | 0.8249 | 14.85 | 未测（`failed_ra=1`，2Y 1.55<1.58） |
| ~~`0mYo9Ok1`~~ | `fnd6_gpy / cap` (168/56) | 1.73 | 1.39 | 8.41% | 1.47 | 1.55 | 0.9711 | 19.27 | 未测（`failed_ra=1`） |
| ~~`P0oeqZap`~~ | `Δ(capxy/cap)` (168/56) | 1.64 | 1.32 | 11.21% | 1.32 | 1.15 | 0.6524 | 14.52 | 未测（`failed_ra=1`） |

**要点**：
1. 三条已测 prod 都落在 **0.6577–0.6932**，余量仅 0.007–0.042 —— 这是个**薄余量族**，第 4 条及以后撞墙概率不低。
2. 机制上「自由现金流 / 市值 = FCF 收益率」本身是经典价值因子 ⇒ 归 PV 合理；同时 FCF 是基本面科目 ⇒ 归 FUNDAMENTAL 合理，**双塔归因有经济学基础，不是巧合**。
3. 该族字段池远未用尽：本地 `fnd6_` 字段共 **2233 个**（ds=368 838 / ds=1481 279 / ds=658 266 / ds=1189 258 / ds=172 197 / ds=858 197 / ds=1006 196），GBR 侧已用不到 10 个。
4. 但注意：**继续在 `capxy/cap` 上换窗口（168/56 ↔ 252/84）只是参数变体**，属伪多样性；真扩招必须换科目（`fnd6_ewq_*` / `fnd6_cptnewq_*` / `fnd6_newa2_*` 都是不同财务科目）。

---

## 5. 结论与建议

**GBR/TOP700/D1 的可行集已被压到单一动作**：

- 提交 `rKRkL9QE`（prod 0.6783）+ `0mYoANkv`（0.6932）+ `WjOkLGWx`（0.6577）
- ⇒ 三条都是 **PV + FUNDAMENTAL 双塔**（effective 2），提交后 **pv 1→4（点亮）+ fundamental 0→3（点亮）**，一次两个塔
- ⇒ 这是 GBR 目前**唯一**能点新塔的动作

**其余 11 个真空塔判定无路径**（数据侧证据）：
- `sentiment`(1.7) / `news`(1.6) / `insiders`(1.5) / `institutions`(1.4) / `shortinterest`(1.2) / `socialmedia`(1.3)：对应 category 的 GBR 数据集已全部判死（sentiment7/snl27/sentiment27/sentiment33；news17/18/20/38/48/50/104；insiders1 + institutions1 同源；institutions4/18/25/6；shortinterest3/29；socialmedia39）
- `earnings` / `macro` / `option`：GBR coverage = 0
- `imbalance`：cov 0.16–0.18 且字段只有 2×2 自由度
- `risk`：语义上被 MODEL 吞并（见 §2.1）
- `other`：`tm_*` prod 饱和 + `other47/384/455` 判死（见 §3.1）

**下一步可选（按价值排序）**：
1. **提交那 3 条** → 一次点亮双塔（当前挂起，等用户）
2. 若继续加厚 FUNDAMENTAL：为 `QPveQvOg` / `N1NM5WK8` / `P0oerpjp` 测 prod，凑出第 4–6 条备用（薄余量族，谨慎）
3. 若要在 GBR 点更多塔：**材料不存在**，只能转区（IND 已点亮 7 塔、EUR 5 塔、KOR 4 塔，是更成熟的战场）
