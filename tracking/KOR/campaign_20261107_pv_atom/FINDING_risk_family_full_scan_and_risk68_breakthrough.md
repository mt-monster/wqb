# RISK 族全量扫描 + risk68 突破（2026-11-07 P49-P54）

## 1. 工具坑：get_datasets 的 category 过滤在 KOR 失效

- `get_datasets(category="RISK")` / `"risk"` / 加 `theme="true"` 全部返回 `{"results":[],"count":0}`；
- 可行做法：**不传 category 拉全量**（KOR/TOP600/D1 = 185 集，81KB），再在本地按返回体 `category` 字段过滤；
- 这条解释了此前「RISK 全景清单从未落盘」的原因：不是没跑，是跑了拿 0 条。

## 2. KOR RISK 类 7 集：本轮全部实测完毕

| dataset | fields | aC | cov | 波次 | 最强读数 | 判定 |
|---|---:|---:|---:|---|---|---|
| risk70 | 96 | 8018 | 0.9798 | 历史多波 | S1.62（omERn83n 已交付） | 已出 1 颗 |
| risk88 | 64 | 1418 | 0.9727 | P49/P53/P54 | dsrt 反转 5d S1.32 / TO0.853；22d S1.06 | 反转有信号但换手致死；载荷族全灭 |
| risk68 | 5 | 770 | 0.9914 | P52/P54 | **权重变化价差 S1.82** | **出货 1 颗** |
| risk59 | 16 | 564 | 0.9806 | P50 | DTC30 S0.84 / bid_rate S0.71 | 无信号（借券水平族全灭） |
| risk72 | 5 | 402 | 0.6246 | P52/P53 | top2000 dsrt 5d S1.06；22d S0.95 | 弱 |
| risk71 | 7 | 349 | 0.6658 | P52/P53 | dsrt 5d S0.69 | 弱（且 2Y 为负） |
| risk60 | 5 | 211 | 1.0 | **P51 重测** | offer/last 水平 S0.49-0.55 | **真弱，非语法误判** |

## 3. risk60 平反检查结论（重要）

旧记录把它判死的原因是 8/8 报 `Operator ts_mean does not support event inputs`——属**语法性失败**。
本轮全部改用 `vec_avg` / `vec_sum` 包装后重跑 10 条（P51），结果：
S 最高 0.55（rsk60_last 水平，2Y1.62）、crowding 正反两臂 0.28/-0.44、fee 动量 -0.18、fee 相对 1 年 0.07。
⇒ **risk60 是真的没信号**，此前的「判死」结论正确但理由错误，现已有实测证据。

## 4. 突破：risk68（Forecast Data）权重变化价差

```
d5Wvpmbx  subtract(group_rank(ts_delta(rsk68_weight_volatility_short, 22), sector),
                  group_rank(ts_delta(rsk68_weight_dadv, 22), sector))
settings: KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay4 · trunc0.08 · nanON · 2014-2023
```

| 闸 | 读数 | 线 | 结论 |
|---|---:|---:|---|
| Sharpe | 1.82 | ≥1.58 | 过 |
| Fitness | 1.25 | ≥1.0 | 过 |
| 2Y Sharpe | 4.10 | ≥1.58 | 过 |
| Turnover | 0.2461 | - | 健康 |
| RA failed | 0 | 0 | 全过 |
| self corr | 0.2023 | <0.70 | 过（pool 30） |
| prod corr | 0.6906 | <0.70 | 过（直方图 [0.6,0.7)=1、[0.5,0.6)=1，非深钉） |

逐年（year|sharpe|pnl|longCount）：
2014|1.25|564221|290 · 2015|1.68|983550|307 · 2016|1.35|726448|309 · 2017|1.15|652008|314 · 2018|1.53|1237933|329
2019|0.50|287910|326 · 2020|0.44|281136|333 · 2021|0.94|618501|349 · 2022|3.46|2577469|328 · 2023|4.69|4024757|336
⇒ 十年逐年 pnl 全正、longCount 全>0，无空窗；2019-2020 弱但不断档。

机制解读：`weight_volatility_short` 是空头侧的波动率权重、`weight_dadv` 是空头侧的流动性权重。
两者**变化量之差**刻画空头仓位的「波动↑而流动性↓」这一挤压前置形态 → 正向前瞻收益。
单腿各自无效（wt_vol delta 0.30 / wt_dadv delta -0.90），**价差才有效**，说明是相对结构而非水平。

## 5. risk88 归因（唯一有信号的另一族）

`rsk88_mfm_ase1_dsrt`（工具特有收益，cov 0.967）是反转信号：
- 5d 反转 S1.32 / TO0.853 / F0.44（decay4）；decay8 下掉到 0.62；
- 22d 反转 S1.06 / TO0.36（decay4）、S1.04 / TO0.32（decay8）；
- 降换手杠杆全部失败：`ts_decay_linear(...,10)` → S0.03、`ts_mean(ts_sum(...),4)` → -0.10；
- `winsorize(std=4)` 与裸式完全相同（0.62/0.16，同 id 指标）；
- subindustry 轴 S0.02、industry 轴 0.55 ⇒ sector 是最优轴。
⇒ 反转族在 KOR 的 S 天花板 ≈1.32，且与换手率强绑，判死。

风格载荷族（`ri_*`，10 个）全部 S -0.56~0.81、2Y -1.2~1.37 ⇒ 载荷是静态暴露，无时序 alpha。

## 6. 仍未测（本轮已画像，见 FIELD_PROFILE_risk_insiders_20261107.md）

| dataset | category | fields | aC | cov | 备注 |
|---|---|---:|---:|---:|---|
| model244 | model | 30 | **17** | 0.459 | Insider Transaction Analytics，aC 极低 |
| other83 | model | 15 | 171 | 0.375 | 同上（另一版本） |
| insiders1 | insiders | 9 | 549 | 0.3526 | Global Insider Trading |
| model68 | model | 4 | 27 | 0.8499 | Risk-Alleviated Momentum（VECTOR） |

## 7. 本轮总账

派发 6 波 60 条（P49 risk88 / P50 risk59 / P51 risk60 / P52 risk71+72+68 / P53 risk88+72 反转降换手 / P54 risk68+88 补几何），
**新增交付候选 1 颗（d5Wvpmbx，risk68）**，使 KOR 交付推进到 4/10。
KOR RISK 类 7 集至此**全部有实测读数**，无遗漏。