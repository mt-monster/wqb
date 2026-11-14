# ★★突破：ANALYST 单塔 ATOM `6XM87Zb7`（S 1.87，全闸通过）

日期：2026-11-12　背景：insiders 双集 ATOM 卡在 S 1.37 后，转向其他塔复用「同塔多数据集=ATOM」规则

## 一、数据集全集盘点（DEU 共 172 个）

按塔（category）分组，可用于「同塔多数据集组合」的塔：

| 塔 | 数据集数 | 高覆盖代表 | 倍数 |
|---|---:|---|---:|
| **analyst** | **18** | analyst7(0.72)、analyst9(0.58)、analyst44(0.58)、analyst93(0.64)、analyst47(0.62)、analyst48(0.79)、analyst_factor_signals(0.60) | 1.8 |
| news | 17 | news104(0.963)、news18(0.805)、news17(0.791)、news20(0.773)、news50(0.764) | 1.8 |
| model | 45 | predictive_starmine(0.79)、model264(0.997)、analyst_earnings_ibes(0.998) | 1.8 |
| fundamental | 12 | fundamental6(0.49) | 1.8 |
| institutions | 5 | **institutions6(1.0)**、fund_holdings_panel(0.90) | 1.6 |
| risk | 5 | **risk88(1.0)**、risk60(0.835) | 1.5 |
| sentiment | 3 | sentiment27(0.904)、sentiment7(0.742) | 1.8 |
| earnings | 2 | earnings6、earnings_sent_matrix | 1.5 |
| insiders | 2 | insiders1(0.534)、insider_agg_matrix(0.562) | 1.6 |
| pv | 16 | pv29(1.0)、pattern_scores(0.989) | 1.6 |
| shortinterest | 1 | shortinterest3(0.71) | 1.3 |

## 二、关键：ANALYST 塔已有两颗 S>2 的存量 ATOM，机制可复刻

| alpha | 表达式 | S | Y2 | sub | TO |
|---|---|---:|---:|---:|---:|
| `RREPm361` | `group_rank(add(ts_zscore(est_12m_ebi_median,240), ts_zscore(est_12m_ebt_mean − est_12m_ebt_mean_4wks_ago,44)), sector)` | **2.02** | 1.82 | **1.24** | 25.1% |
| `zq3eb7No` | `group_rank(add(ts_zscore(est_12m_ebt_mean,240), ts_zscore(est_12m_pre_mean − est_12m_pre_mean_4wks_ago,66)), sector)` | **2.01** | 1.64 | 1.00 | 22.6% |

**共同机制：`ts_zscore(长期水平, 240) + ts_zscore(短期修正Δ4周, 44/66)`**
**共同设置：decay=0 / FAST / nan=OFF / truncation=0.08**

⇒ 我在 BE211 用这两条表达式做对照臂，平台**去重返回原 alpha id**，证明机制复刻精确。

## 三、突破：三腿 ANALYST ATOM `6XM87Zb7`

```
group_rank(add(
  ts_zscore(est_12m_ebi_median, 240),                                  # EBIT 水平（长期）
  ts_zscore(est_12m_ebt_mean - est_12m_ebt_mean_4wks_ago, 44),          # EBT 修正（短期）
  ts_zscore(est_12m_pre_mean - est_12m_pre_mean_4wks_ago, 66)           # 税前利润修正（中期）
), sector)
```

| 指标 | 值 | 闸 | 判定 |
|---|---:|---:|---|
| Sharpe | **1.87** | 1.58 | ✅ |
| Fitness | **1.06** | 1.00 | ✅ |
| 2Y Sharpe | **1.91** | 1.58 | ✅ |
| Sub-Universe | **1.08** | 0.70 | ✅ |
| Turnover | 26.6% | <70% | ✅ |
| **pyramids.effective** | **1** | — | **ATOM ✅** |
| **checks.fail** | **[]** | — | **9 项全过 ✅** |

checks.pass 全 9 项：LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST / **LOW_2Y_SHARPE** / MATCHES_PYRAMID

**这是本战役第一颗新挖的、S 过闸的 ATOM。**

注：`submit_verdict` 返回 `UNVERIFIABLE_404` —— 平台提交端点已下线（dead endpoint），与 `vR1oxZA3` 同类。非未通过。

## 四、加腿递减规律（再次确认，BE211）

| 腿数 | 构造 | S | F | Y2 | sub |
|---:|---|---:|---:|---:|---:|
| 2 | ebi水平 + ebtΔ44 | 2.02 | 1.25 | 1.82 | 1.24 |
| 2 | ebt水平 + preΔ66 | 2.01 | 1.28 | 1.64 | 1.00 |
| **3** | **ebi水平 + ebtΔ44 + preΔ66** | **1.87** | 1.06 | **1.91** | 1.08 |
| 4 | + promoΔ44 | 1.78 | 1.02 | 1.25 | 0.86 |
| 6 | + sal/cps/dps/bpsΔ44 | 1.07 | 0.43 | 1.01 | 0.75 |

**与 insiders 完全一致的规律：腿数越多 S 越低。**

## 五、第三腿的指标族选择（BE212，全部 < 冠军）

| 第三腿 | alpha | S | F | Y2 | sub | fails |
|---|---|---:|---:|---:|---:|---:|
| **pre 66** | **6XM87Zb7** | **1.87** | **1.06** | 1.91 | 1.08 | **0** |
| pre66+sal66（四腿）| 78YAAVP5 | 1.65 | 0.87 | 1.69 | 1.05 | 1 |
| cps 66 | vRAqqV7w | 1.62 | 0.84 | **1.97** | 0.92 | 1 |
| bps 66 | ZYa55Lvx | 1.58 | 0.83 | 1.30 | 1.04 | 2 |
| dps 66 | MP6WWAva | 1.42 | 0.68 | 0.78 | 0.86 | 3 |
| sal 66 | leaqqZPA | 1.41 | 0.68 | 1.94 | 0.82 | 2 |

⇒ **`pre`（税前利润）是最优第三腿**，与 ebt（税前利润）机制同族但窗口不同（44 vs 66）。
⇒ 与「analyst 双窗口搭档最强」的历史规律吻合。

## 六、因子画像（analyst7 的 383 个 est_12m_* 字段）

- analyst7 共 **608 字段**，其中 `est_12m_*` **383 个**，**覆盖率全部 1.0**
- 族划分：按指标（ebi/ebt/pre/sal/cps/csh/dps/bps/ner/net/prr…）× 按形态（mean/median/4wks_ago/raisednum/lowerednum/num…）
- 主力可用族（覆盖率 0.68-0.74，MATRIX 类型）：**sal / pre / cps / dps / bps**
- **字段类型全部为 MATRIX**（不是 VECTOR），可直接进 `ts_zscore`，无需 `vec_avg`

## 七、工程陷阱（本轮 3 次整批作废的教训）

| 错误写法 | 平台报错 | 正确写法 |
|---|---|---|
| `subtract(anl9_s_numup, anl9_s_numdn)` | `Operator subtract does not support event inputs` | 先 `vec_avg` 各自聚合 |
| `ts_mean(anl93_...relative_profitability1,66)` | `Operator ts_mean does not support event inputs` | 先 `vec_avg` |
| `ts_mean(vec_avg(anl47_rawsentiment),66)` | 整批 CANCELLED | MATRIX 字段**不可** vec_avg，直接 `ts_mean` |

**纪律：派发前必须查字段 type。VECTOR → 先 vec_avg 再时序算子；MATRIX → 直接时序算子。**

## 八、ANALYST 四数据集探针（BE210，全部 eff=1 但信号弱）

用 analyst9/44/93/47 四个数据集各建一腿组合，**塔归属确认 `eff=1, DEU/D1/ANALYST`**，
但 S 仅 0.07-0.67 —— 说明这四个数据集的机制（修正广度/预测偏离/质量权重/原始信号）本身弱，
**analyst7 的 est_12m_* 族才是强度来源。**
