# DEU 分段复盘：model264 / model28 / shortinterest-rates / insider_agg_matrix

固定设置：region=DEU / delay=1 / universe=TOP500 / neutralization=SUBINDUSTRY / decay=4 / truncation=0.08 / nanHandling=OFF / pasteurization=ON / unitHandling=VERIFY / maxTrade=OFF

---

## 一、本段四批判死的全表

### 1.1 MODEL264-A（`DzD2ZaAZ4EeciAddYhVxxB`）：4 腿族平衡探测，10/10 REJECT

天花板 **S 0.53**。

| alpha | 结构 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| 2rAebz7P | `div_payout_l3 − payable_to_l3` 估值质量 | **0.53** | 0.27 | 0.23 | 0.0741 |
| wpQWMxex | bookp_fy1+bookp+psale+divyld_bb 四腿 add | **0.53** | 0.28 | 0.56 | 0.1116 |
| omEZM5V5 | `group_rank(es_ebit_fy1_r1m_l3, sector)` 单腿 REV | 0.47 | 0.23 | 0.55 | 0.1029 |
| gJeLEOxg | 四指标 (l3−l1) 净方向 add | 0.45 | 0.22 | 0.61 | 0.0933 |
| pwd3Ar6X | 新闻情绪三腿 add | 0.45 | 0.13 | −0.21 | 0.3200 |
| LLM3Aak1 | es_ebit+ebitda+sale+roe 四腿 l3 add | 0.43 | 0.21 | 0.57 | 0.0898 |
| 88RXd9LV | `amihud − vol_vo_p_1m` | 0.11 | 0.01 | 0.84 | 0.3214 |
| E56xXWKK | bookp+psale+divyld 时序变化 66d | 0.03 | 0.00 | 1.02 | 0.3647 |
| 0mY503z2 | `ntm_r1m − fy1_r1m` 期限差 | −0.18 | −0.04 | −0.02 | 0.1908 |
| 58EYo0v1 | `float_to − lottery` | −0.35 | −0.09 | −0.32 | 0.3355 |

### 1.2 MODEL264-B（`44kQhGalN4WNcMm4aZC1CLb`）：新颖几何，10/10 REJECT

天花板 **S 0.66**。★ 首派批次 `4vN9pv1g14qr9f2KeEeAo32` 因把 `_class` 直接当 group 轴整批连坐（见 §四），修正后重派。

| alpha | 结构 | S | F | 2Y | TO |
|---|---|---:|---:|---:|---:|
| JjerZXdn | `_class` 作 `bucket(rank(_class), 0,1,0.34)` 分组轴 | **0.66** | 0.31 | 0.59 | 0.1745 |
| P0oKdlp7 | `trade_when(_class>2, group_rank(l3,sector), −1)` 上行门控 | **0.64** | 0.37 | 0.62 | 0.0985 |
| gJeLEPMM | `(l3−l1) × sale_l3` 交互 | 0.49 | 0.25 | 0.59 | 0.0999 |
| RREPna80 | `signed_power(l3−l1, 2)` 二次 | 0.46 | 0.23 | 0.50 | 0.1046 |
| vR1P3zL3 | 三指标 `_class` 枚举值 add | 0.38 | 0.17 | 0.34 | 0.1258 |
| 78LlEXn8 | `(l3−l1)` @bucket(_class) 中性化 | 0.38 | 0.13 | 0.24 | 0.1973 |
| 1YN0Qm7m | 三腿 rank add @bucket(l3) | 0.29 | 0.07 | 0.19 | 0.2648 |
| GrW9p8w5 | `trade_when(_class<2, −group_rank(l3), −1)` 下行门控 | 0.19 | 0.06 | −0.27 | 0.1369 |
| E56xXaKP | `group_rank(_class, sector)` 裸枚举 | 0.16 | 0.04 | 0.26 | 0.1646 |
| N1N8vjrL | `ts_rank(l3, 252)` 时序分位 | −0.02 | 0.00 | 0.31 | 0.2687 |

**判死结论**：model264 的 `_l1/_l2/_l3` 概率三元组与 `_class` 枚举，在 **20 个结构互异几何**下天花板 **S 0.66**。四族（预期修正 REV / 估值质量 VALUE / 风险流动性 RISK / 新闻情绪 NEWS）无一例外。
**佐证**：备用池 `wpQYNvZp`(S1.68) / `Vkx3MjW8`(S1.75) 的 S 实际来自 predictive_starmine 两腿，model264 腿仅贡献分散化，非信号源。

### 1.3 SHORTINT-A（`4qpqEGfWo5g3bv7zfOdfXky`）：loan rate 族，10/10 REJECT

天花板 **S 0.68**。全部 `vec_avg` 包裹、`_p5_d1` 变体（cov 0.7833）。

| alpha | 结构 | S | F | 2Y | sub_u | TO |
|---|---|---:|---:|---:|---:|---:|
| mLoQM5e9 | `−group_rank(ts_mean(vec_avg(max_loan_rate), 22))` 峰值费率 | **0.68** | 0.41 | 0.88 | **0.69** | 0.0601 |
| 9qxkLpgx | `−group_rank(ts_mean(vec_avg(loan_rate_volatility), 22))` 费率波动 | **0.68** | 0.40 | **1.12** | 0.46 | 0.0653 |
| 1YN0Qp6J | `−(...max−min 离散度, 22)` | 0.65 | 0.39 | 0.88 | 0.69 | 0.0610 |
| gJeLE8vQ | `−(...mean_loan_rate, 22)` 费率水平 | 0.57 | 0.31 | 0.99 | 0.30 | 0.0620 |
| E56xXG0G | 账龄 rank − 费率 rank 背离 | 0.34 | 0.13 | 0.89 | 0.07 | 0.0659 |
| j2YOb6lW | `−(...average_loan_duration_days, 22)` 账龄 | 0.32 | 0.12 | 0.07 | 0.51 | 0.0593 |
| pwd3AN0b | `−ts_av_diff(mean_loan_rate, 66)` 费率动量 | 0.16 | 0.03 | 0.13 | −0.08 | 0.3499 |
| WjOJ6AKZ | `−ts_av_diff(loaned_share_count, 66)` 供给动量 | −0.05 | −0.01 | 0.01 | −0.64 | 0.2449 |
| KPJZjGYp | 费率 rank − 供给 rank 挤出 | −0.34 | −0.15 | −0.76 | 0.09 | 0.0539 |
| pwd3ANog | `−ts_rank(loaned_market_value_usd, 252)` 市值分位 | −0.35 | −0.11 | −0.07 | −0.75 | 0.2021 |

**判死结论**：shortinterest3 的 8 个 loan-rate/供给度量族天花板 **S 0.68**。已交付 `MPY9VNY9`(S1.59) 的威力**全部来自 `shrt3_bar` 借券需求评级 + 双视界 delta 乘积 + `ts_target_tvr_decay`**，与 loan rate 族无关。
**副产物**：本批 TO 普遍 0.06 左右（`_p5_d1` 是慢变量），`mLoQM5e9` 的 sub_u 0.69 是全段唯一健康子宇宙项。

### 1.4 MODEL28-A（`1nl9I45WQ4gPc0o34J50AWe`）：Merton 结构式信用，10/10 REJECT

天花板 **S 0.74**，但 **F 0.56 / margin 0.00423 / returns 0.0708 是本段质地最好的件**。

| alpha | 结构 | S | F | 2Y | sub_u | TO |
|---|---|---:|---:|---:|---:|---:|
| vR1P3jKr | `rank(DD) × rank(drift)` 双 rank multiply | **0.74** | **0.56** | 0.36 | 0.41 | 0.0335 |
| 78LlEjkO | `−ts_av_diff(pd_pct, 66)` PD 改善 | 0.46 | 0.26 | 0.43 | 0.25 | 0.1165 |
| YP1YG7Pq | `ts_av_diff(distance_to_default, 66)` DD 动量 | 0.41 | 0.21 | 0.36 | 0.18 | 0.1168 |
| KPJZjGWg | `ts_av_diff(asset_drift_pct, 66)` 资产漂移动量 | 0.40 | 0.19 | 0.07 | 0.32 | 0.1338 |
| vR1P3jRr | `−divide(rank(leverage), rank(vol)+1)` 风险构成 | 0.30 | 0.13 | −0.59 | 0.37 | 0.0248 |
| e75Eo3XE | `ts_mean(distance_to_default, 22)` DD 水平 | 0.10 | 0.03 | 0.09 | 0.20 | 0.0243 |
| kqN92Pzz | `−ts_mean(leverage, 22)` 杠杆 | 0.05 | 0.01 | −0.90 | 0.22 | 0.0201 |
| E56xXlZr | `sector_rank − global_rank` | −0.10 | −0.02 | 0.12 | −0.21 | 0.0977 |
| rKR8vj18 | `−ts_rank(asset_volatility_pct, 252)` 波动分位 | −0.13 | −0.03 | −0.83 | −0.13 | 0.1047 |
| 9qxkLpNr | `−ts_mean(asset_volatility_pct, 22)` 低波异常 | −0.30 | −0.14 | 0.46 | −0.15 | 0.0236 |

**判死结论**：model28 与 model36 同属信用风险主题，同归判死。**「低资产波动异常」在 DEU 反向失效**（S −0.30、2Y 0.46、drawdown 0.51）。
**关键副产物**：单腿 DD 水平 S 0.10 → 双 rank multiply S 0.74（**7.4×**）；F 0.03 → 0.56（**18×**）。复合几何的增益是真实的。

---

## 二、★ 本段最重要的方法论拐点：简单几何系统性低估数据集潜力

### 2.1 已交付的 3 颗严格 ATOM 全部使用复合几何

| alpha | 数据集 | 复合几何 | S |
|---|---|---|---:|
| QPvzNNGG | predictive_starmine | **3 腿 rank add** + `bucket(…, 0,1,0.05)` 中性化 | 1.70 |
| LLMzYrZe | predictive_starmine | **2 腿 rank add** + sector 中性化 | 1.61 |
| MPY9VNY9 | shortinterest3 | **双视界 (240d,176d) delta 乘积** + `ts_target_tvr_decay(0.03)` | 1.59 |

### 2.2 本段 4 批简单几何的天花板全部卡在 0.53–0.74

model264 0.66 / shortint-rates 0.68 / model28 0.74 / MODEL264-A 0.53。
**没有任何一条 `group_rank(ts_mean(x, 22), sector)` 型单腿几何超过 0.75。**

### 2.3 三条可行的复合几何配方（从已交付件反推）

1. **同机制多腿 rank add**：`group_rank(add(rank(A), rank(B), rank(C)), sector)` —— 要求 A/B/C 是**同一机制的不同度量**（不是异机制混信号）。
2. **双视界 delta 乘积**：`ts_target_tvr_decay(multiply(rank(ts_delta(x, 240)), rank(ts_delta(x, 176))), target_tvr=0.03)` —— 长短两个视界同向确认才持仓。
3. **两腿 rank multiply**：`group_rank(multiply(rank(A), rank(B)), sector)` —— 双条件同时满足才强信号。

### 2.4 待验：PS-VAL-A → PS-VAL-B 的 A/B

PS-VAL-A（`1DJDST7Uo5009GersBmwQC0`）用**简单几何**打 predictive_starmine 的 `iv_*` / `forward_pe_*` / `rel_val_*` 族。
若单腿落在 0.5–0.9 区间，则立即派 **PS-VAL-B：同族多腿 rank add + bucket 中性化**，直接复刻 QPvzNNGG 结构。
这将是「同数据集第 3 颗 ATOM」且与已交付 2 颗**零共腿**（iv/rel_val 族 vs mean_estimate_change/predicted_surprise 族）。

---

## 三、新数据集字段画像存档

### 3.1 model28（Structural Credit Risk）—— 25 MATRIX，已判死

Merton 结构式模型五维：`distance_to_default`(DD) / `asset_drift_pct` / `asset_volatility_pct` / `leverage` / `pd_pct`。
两套命名：`mdl28_sm_structural_credit_structural_*`（含双下划线的 `__credit_structural_leverage` 特例）与 `mdl28_sm_structural_multiple_credit_structural_*`。
5 个 `_rank` 变体（country/global/industry/region/sector）coverage = **1.0**，其余 0.684。
拥挤度极低：userCount 0–23 / alphaCount 0–35。

### 3.2 insider_agg_matrix —— 34 MATRIX，在飞

三族：
- **买卖股数**（16）：`avg_*` / `total_*` × {buy, sell} × {all, secondary, top}，cov 0.5344
- **重要交易金额**（12）：`significant_value_1..4` / `directional_significant_value_1..4` / `top_*`，cov 0.5342
- **方向指标**（2）：`directional_indicator` / `directional_indicator_2`，**coverage = 1.0**，拥挤度最高（uc34/ac48 与 uc15/ac23）

稀疏披露型数据，`ts_zscore` 会放大跳变，一律先 `ts_backfill(_, 22)`。

### 3.3 predictive_starmine 剩余族（631 字段中已用 4，剩 ~12 族）

| 族 | 字段数 | 是否已用 |
|---|---:|---|
| `mean_estimate_change_pct_*` | 34 | ✅ 已交付 2 颗 |
| `predicted_surprise_*` | — | ✅ 已交付 2 颗 |
| `arm_*` 推荐评分 | — | ❌ 已判死（S≤0.50）|
| `analyst_*_count_*` 升降级计数 | — | ❌ 已判死（S≤0.79）|
| **`iv_*` 内在价值（DCF）** | 56 | 🔄 PS-VAL-A 在飞 |
| **`rel_val_*_component_score`** | 22 | 🔄 PS-VAL-A 在飞 |
| **`forward_pe_*`** | 12 | 🔄 PS-VAL-A 在飞 |
| `ep_yield_pct_smest_*` | 6 | 🔄 PS-VAL-A 在飞 |
| `recommendation_mean_change_*d_*` | 10 | 🔄 PS-VAL-A 在飞 |
| `actual_last_*` | 12 | ⏸ 未测 |
| `eq_vr_dlra*_*` | — | ⏸ 未测 |
| `days_since_last_report_*` | — | ⏸ 未测 |

**★ 核心可交易机制（PS-VAL-A 已实测的两条）**：
- **预期差**：`iv_market_implied_10yr_eps_cagr − iv_forward_10yr_eps_cagr` = 市场隐含增速 − 分析师预测增速，市场预期过高→看跌。
- **估值安全边际**：`forward_pe_smest_fy1 / iv_warranted_f12m_pe` = 市价 PE / 合理 PE，>1 即高估。

---

## 四、★ 新踩的坑：`_class` 枚举字段不能直接当 group 轴（整批连坐）

```text
✗ group_neutralize(x, mdl264_es_ebit_fy1_r1m_class)
  → Incompatible unit for input of "group_neutralize" at index 1,
    expected "Unit[Group:1]", found "Unit[]"
  ⇒ 父模拟 status=ERROR，10 个子模拟全部 CANCELLED，整批作废

✓ group_neutralize(x, bucket(rank(mdl264_es_ebit_fy1_r1m_class), range="0,1,0.34"))
  ⇒ bucket 的官方定义就是 bucket(rank(x), range=...)，返回带 Group 单位的桶号
```

**推广**：任何裸数值/枚举字段要作 `group_rank` / `group_neutralize` / `group_scale` 的 group 参数，必须先过 `bucket(rank(_), range=...)`。只有平台内置的 `sector` / `industry` / `subindustry` / `market` / `country` / `exchange` 等本身带 Group 单位。
`bucket(rank(_), range="0,1,0.34")` 把 3 值枚举切成 3 桶，是「枚举作分组轴」的合法写法。

---

## 五、判死累计台账（DEU，全段）

**有数据但已判死（24 个数据集）**：
model264 / model28 / model36 / model106 / model53 / model238 / model216(单用) / predictive_starmine(arm 族、count 族、ep-actual 族推断) / shortinterest3(loan-rate 族) / dl_riskfree_returns / news104 / news50 / news38 / news_sentiment_transfer / analyst44 / analyst48 / institutions1 / other455(仅 GROUP) / other532 / other699 / insider_matrix / insider_trx_matrix / risk60 / starmine(两辅助族)

**cov=0 判死（44 个）**：model 类 22 个 / news 类 11 个 / analyst 类 11 个。

**已出货（5 颗，全闸通过、UNSUBMITTED）**：

| # | alpha | 数据集 | S | F | 2Y | TO | self | prod | ATOM |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | mLox6Mg2 | sentiment7 + sentiment27 | 2.05 | 1.71 | 2.53 | 0.147 | 0.030 | 0.6935 | ✗ |
| 2 | E56pROb9 | model216 + predictive_starmine | 1.79 | 1.70 | 2.03 | 0.067 | 0.600 | 0.6859 | ✗ 且疑违禁混 |
| 3 | QPvzNNGG | predictive_starmine | 1.70 | 1.30 | 2.18 | 0.155 | 0.678 | 0.6777 | ✓ |
| 4 | LLMzYrZe | predictive_starmine | 1.61 | 1.16 | 1.69 | 0.153 | 0.670 | 0.6697 | ✓ |
| 5 | MPY9VNY9 | shortinterest3 | 1.59 | 1.26 | 2.36 | 0.036 | 0.270 | 0.5986 | ✓ |

严格单数据集 ATOM = **3 / 10**，缺口 **7 颗**。

---

## 六、下一步队列

| 优先 | 批次 | 状态 | 说明 |
|---|---|---|---|
| 1 | PS-VAL-A `1DJDST7Uo5009GersBmwQC0` | 在飞 | iv/forward_pe/rel_val 族简单几何，测单腿强度 |
| 2 | INSIDER-A `3cueYzcqh4wk9fRCTSUx48Y` | 在飞 | insider_agg_matrix 10 模板 |
| 3 | **PS-VAL-B** | 待设计 | 若 PS-VAL-A 单腿 0.5–0.9 → 同族多腿 rank add + bucket（复刻 QPvzNNGG）|
| 4 | SHORTINT-B | 待设计 | `shrt3_bar` 不同视界组合（会与 MPY9VNY9 共腿，需测 self-corr）|
| 5 | news17 / news20 | 待画像 | cov 0.7906(48V) / 0.7729(46V) |

---

## 七、环境与工具备注（本段新增/确认）

- `bucket(rank(x), range=...)` 返回 Group 单位；裸枚举字段不行。
- `mdl28_sm_structural_credit_structural_leverage` 不存在，真实 id 是 `mdl28_sm_structural__credit_structural_leverage`（双下划线）或 `mdl28_sm_structural_multiple_credit_structural_leverage`。
- `recommendation_mean_change_60d` 不存在，必须带后缀：`_60d_2` / `_60d_7`。
- `preflight_expressions` 的 `warning: "… failed after 6 attempts"` 是预检自身超时故障，此时 `unknown_fields` 里的真实字段名不可信，需重跑。
- multisim 父 `status=ERROR` 时**全部子模拟 CANCELLED**（不是只有出错那条），单条语法错即整批作废。派发前必须预检。
