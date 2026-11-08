
## qML0EAo1 — DEU/TOP500/D1/SUBINDUSTRY/decay16 — 判定 CONDITIONAL

- 表达式：`a = ts_backfill(vec_avg(snt7_all_languages_views), 22); b = ts_backfill(vec_avg(snl27_relpopularity08), 22); vector_neut(quantile(ts_ir(ts_mean(max(a, ts_delay(a,1), ts_delay(a,2)), 10), 22), driver="uniform"), b)`
- 算子 11（软标记，>5）；金字塔 DEU/D1/SENTIMENT ×1.8，effective=1
- 顶层：S 2.05 / F 1.92 / TO 0.0898 / Ret 10.93% / DD 4.67% / margin 24.35bp / sub 1.34 / 2Y 2.40
- RA：failed_ra_count=0，checks FAIL=0（仅 MATCHES_THEMES WARNING）

### Phase B 归因
- 逐年（有效窗口 2019–2023，**2014–2018 五年 longCount=0 空仓**）：
  | 年 | S | Ret | DD | margin |
  |---|---|---|---|---|
  | 2019 | 1.63 | 6.72% | 2.27% | 17.4bp |
  | 2020 | 0.59 | 3.28% | 3.02% | 7.8bp |
  | 2021 | 3.00 | 15.41% | 2.56% | 35.6bp |
  | 2022 | 3.45 | 19.14% | 2.65% | 45.1bp |
  | 2023 | 1.41 | 8.09% | 2.83% | 15.5bp |
- 回撤日历：各年 DD 2.27/3.02/2.56/2.65/2.83% 高度均匀，最高 3.02% < 2×均值 5.33% ⇒ 不标警
- PnL 形态：2019-03 起单调上行，2020 年横盘，2021–2022 陡升，2023 年横盘蓄势；无单年崩塌
- Top-5 个股集中度：逐股 PnL 不可得（平台未提供分解），未评

### Phase C 判定
| 检查项 | 实测 | 判定 |
|---|---|---|
| WebDataScope failed | 0，无 PENDING | PASS |
| Recent-3yr Sharpe | 2.40 ≥ 1.58，三年全 > 0.3 | PASS |
| Recent-3yr CV_Sharpe | 0.409（std 1.072 / mean 2.62） | **CONDITIONAL** |
| 衰减比 | 1.41/2.05 = 0.688 | PASS |
| 平年 | 0 | PASS |
| Recent-3yr max/min | 3.45/1.41 = 2.45 | PASS |
| Sub-universe | 平台 PASS，1.34 | PASS |
| 算子数 | 11 | 软标记 |
| Margin @ TO | 24.35bp @ 8.98% | PASS |
| 经济可解释性 | 社媒关注度水平 + 相对流行度正交化，一句话可写 | PASS |

**结论：CONDITIONAL** — 唯一条件项是 CV_Sharpe 0.409 刚踩 0.40 上界（来自 2021/2022 两年超强、2023 回落到 1.41 的正常波动，非噪声拟合）。辅以两条软标记：算子 11 个、2014–2018 五年空仓。

空仓说明（与收入无关）：CPA 组合窗口 2023–2025、Daily Osmosis Rank 用 OS 近期 PnL，2014–2018 空仓不在任何计费窗口内；IS_LADDER_SHARPE 已 PASS 说明平台 ladder 检查按有效窗口计算。
