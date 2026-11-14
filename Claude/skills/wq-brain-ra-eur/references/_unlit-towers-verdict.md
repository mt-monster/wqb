# EUR 未点亮塔实测终局（_unlit-towers-verdict.md）

> **as_of**：2026-11-12 ｜ 来源：RJ 系列波，约 152 臂新回测 + 6 批字段诊断
> 定位：EUR 7 个未点亮塔的**判死/判弱证据总表**。机制选型前先看本文，避免重挖。

## 总表

| 塔 | 当前 | 结论 | 数据集 | 最强读数 | 死因 |
|---|---|---|---|---|---|
| risk | 2/3 | **单字段判死、组合出活** | risk68 / risk60 / risk62 | edadv S1.67；residual_return 反转 S1.68；−rsk60_offer×imb5 **S2.60** | edadv SUB/S **0.07**（规模代理）；residual **TO 70%** |
| insiders | 2/3 | 判死 | insider_agg_matrix / insiders1 | 探针 S0.52 / 0.61 | TO 52% / 176%，信号天花板 0.61 |
| pv | 2/3 | 判弱 | pv106 / intraday_pv_feats / pv103 | pv106 spreadbp **−1.01**（负向） | 价差族系统性负向（EUR 价差大→收益低）；intraday 585 字段两法皆灭 |
| earnings | 1/3 | 判死 | earnings6 / earnings_sent_matrix | prelim range width S0.70（SUB/S 1.06） | eps_change_* **实测全零**；真信号强度不足 |
| institutions | 0/3 | **可续（有质量无强度）** | fund_holdings_panel / institutions6 | HHI S0.50 但 **SUB/S 1.28**；stable_boundary_*_active 裸信号 **S1.64** | 强度不足；S1.64 那支 prod 0.8887 FAIL |
| socialmedia | 0/3 | 判死 | socialmedia12 / socialmedia15 | 十臂全部 \|S\|≤0.21 | **SUB 全负**（方向性近零） |
| macro | 0/3 | 不优先 | macro27 / macro10 | — | cov 0.15–0.43 全 VECTOR；macro10 单标量 |

## 三条可复用的字段级教训

### 1. `_active` 后缀变体差异巨大
`stable_boundary_trade_count_21d_active` **S1.64**，同名字段非 active 版 **S0.00**。
⇒ 同机制先查 `_active` / `_filled` / `_2` 等变体，不要假设等价。

### 2. 裸信号外层加 group_rank 会损信号
`zq378ELo` 原式 = `ts_mean(group_zscore(vec_avg(...),country),22)`，**最外层无 group_rank**，S1.64。
我加 `group_rank(...,industry)` 外层后掉到 0.38–0.81。
⇒ 加横截面算子前先测原式读数。

### 3. 单向事件型字段只能做腿，不能做主信号
`rsk60_offer` 单字段 S−0.73（无方向），但**取反后与 imb5 组合**得 S2.60（篮子件 `JjeNJ00O`）。
判据：取反衰减量 >0.40 ⇒ 单向事件型，只有极端段有预测力。

## 与字段画像的关系

字段级六维画像见 `tracking/EUR/reference/profiles/EUR_UNLIT_FIELD_PROFILES_20261112.md`（仓库内路径），
原始字段 JSON 见 `tracking/EUR/reference/fields/<dataset>_eur_d1.json`。
本文只给**结论**，挖新机制前请先查画像的「潜在 alpha 适用性」列。
