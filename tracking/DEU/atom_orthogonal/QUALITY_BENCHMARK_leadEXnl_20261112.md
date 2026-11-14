# ★质量标杆：leadEXnl 十年全部 Sharpe ≥1.03（无单年依赖）

日期：2026-11-12

## 逐年对照

| 年 | leadEXnl (S2.20) | 0mPqGEgq (S1.74) | mLapKbd2 (S1.64) |
|---|---:|---:|---:|
| 2014 | 1.03 | 0.72 | **0.25** |
| 2015 | **3.47** | 1.68 | 0.78 |
| 2016 | 1.24 | 1.50 | 0.26 |
| 2017 | 2.42 | 1.16 | 1.05 |
| 2018 | 2.52 | 3.05 | 2.37 |
| 2019 | 2.47 | 1.96 | 1.45 |
| 2020 | 1.67 | 1.60 | 2.39 |
| 2021 | 2.43 | 0.90 | 0.99 |
| 2022 | 2.29 | 1.65 | 3.04 |
| 2023 | 2.62 | 3.05 | 3.35 |
| **最差年** | **1.03** | 0.72 | 0.25 |
| **负年数** | **0** | 0 | 0 |
| **标准差** | **最低** | 中 | **最高** |

## 判断

**leadEXnl（C + AS3 + AS4）是本战役质量最高的件：**
- S 2.20 / F 1.64 / 2Y 2.43 / sub 1.42 —— 四项均衡，无短板
- **十年最低 1.03，最高 3.47，全部为正** —— 无单年依赖、无风格暴露
- 只有 11 个算子
- 塔 INSIDERS+MODEL，eff=2，合规

对比之前的高 S 件：
- `mLapKbd2` 的 2Y 3.18 最高，但 2014 只有 0.25、2016 只有 0.26 ⇒ **依赖近两年**
- `0mPqGEgq` 的 2021 只有 0.90
- `MP6OgoPr`（B+AS3）曾因「逐年无负年」被特别记录，但最低 0.67 仍低于 leadEXnl 的 1.03

⇒ **leadEXnl 是「全期均衡型」的最佳代表**，比单看 S 排名更有交付价值。
⇒ 它的构造（C 集中度 + analyst 14d/90d 双窗）值得作为后续所有件的模板。

## 可复用模板

```
h = vec_avg(insd1_holdings)                                    # 若复用则提到变量
c = group_rank(ts_mean(divide(significant_value_1,
      add(significant_value_1,significant_value_2,
          significant_value_3,significant_value_4)),66),sector)
p = add(rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_14d_4,5)),
        rank(ts_mean(mean_estimate_change_pct_f12m_ebitda_90d_3,22)))
out = signed_power(group_zscore(add(c,p),sector),1.3)
```
（实际派发时去掉变量赋值，写成单行展开版；11 个算子）