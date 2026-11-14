# DEU D1 战役 · 最终交付报告（2026-11-11 23:21）

## 一、达成结论

| 目标 | 要求 | 达成 | 状态 |
|---|---:|---:|---|
| 正文第 4 条：ATOM 类型 regular alpha | 10 | **11** | ✅ **超额 1 颗** |
| 其中严格 ATOM（单数据集单塔） | — | **5** | 已核实塔构成 |
| 其中 regular（双塔组合） | — | 6 | — |
| 标题：20 个 ATOM | 20 | 5 | ❌ DEU D1 结构上不可达 |

## 二、11 颗交付清单（互相关全对 <0.7，最大独立集 = 11，超阈对 0 个）

| # | alpha | 状态 | 口径 | 塔 | S | F | 2Y | TO | self | prod |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | bl6AvMkN | ✅ ACTIVE 11-07 | regular | MODEL+ANALYST | 1.61 | 1.36 | 2.15 | 0.110 | 0.514 | — |
| 2 | vR1oxZA3 | ✅ ACTIVE 11-07 | regular | （无标记） | **3.27** | **3.09** | **4.39** | 0.183 | 0.599 | 0.599 |
| 3 | GrW9OxmG | ✅ ACTIVE 11-07 | **ATOM** | ANALYST | 1.62 | 1.56 | 1.93 | 0.046 | 0.266 | 0.664 |
| 4 | zq3eb7No | ✅ ACTIVE 11-08 | **ATOM** | ANALYST | 2.01 | 1.28 | 1.64 | 0.226 | 0.364 | 0.617 |
| 5 | rKRx2Alj | ✅ ACTIVE 11-09 | regular | MODEL+ANALYST | 1.95 | 1.80 | 2.23 | 0.140 | 0.563 | 0.656 |
| 6 | 78Yk8VR1 | ✅ ACTIVE 11-10 | **ATOM** | SHORTINTEREST | 1.68 | 1.21 | 2.27 | 0.113 | — | — |
| 7 | qM7KxkQV | 🟡 待授权 | regular | SHORT+INSIDERS | 1.72 | 1.34 | 2.43 | 0.143 | 0.543 | **0.543** |
| 8 | Jj8VQwoe | 🟡 待授权 | regular | SHORT+OTHER | 1.65 | 1.24 | 2.42 | 0.147 | 0.565 | **0.6124** |
| 9 | RREPm361 | 🟡 待授权 | **ATOM** | ANALYST | 2.02 | 1.25 | 1.82 | 0.251 | 0.328 | 0.6881→重算超45min |
| 10 | d5a2vxzY | 🟡 待授权 | **ATOM** | SHORTINTEREST | 1.60 | 1.08 | 2.05 | 0.180 | 0.604 | **0.6039** |
| 11 | 9qlz29Oe | 🟡 待授权 | regular | SHORT+NEWS | 1.86 | 1.34 | 2.02 | 0.173 | 0.455 | **0.47** |

**互相关**：`all_below_threshold = True` / 最大独立集 **11** / 超 0.7 的对 **0 个** / 最紧对 zq3eb7No~RREPm361 = 0.6879。
**逐年**：11 颗全部 2014-2023 十年零空窗（满足 goal 第 6 条）。

## 三、三颗关键新件的算子逻辑

### d5a2vxzY（严格 ATOM，第 10 颗）

```
group_zscore(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(max_loan_rate_p5_d1), 132), 220), sector),
  -group_rank(ts_delta(ts_backfill(vec_avg(mean_loan_rate_p5_d1), 132), 132), sector)
), market)
```

借券**最高成交利率**（做空方最急迫挤兑成本）× **平均借券利率**（常态做空成本），长短窗口对照。单塔 SHORTINTEREST。

### 9qlz29Oe（第 11 颗）

```
group_zscore(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(max_loan_rate_p5_d1), 132), 220), sector),
  group_rank(ts_mean(ts_delta(ts_backfill(vec_avg(nws20_multiple_comp_event_sentiment_score), 132), 66), 11), sector)
), market)
```

借券最高利率（资金面拥挤）× 新闻情绪（基本面改善，66 日变化 + 11 日平滑）。塔 SHORT+NEWS。

### qM7KxkQV（已长驻待授权，最稳的 regular）

```
group_zscore(add(
  -group_rank(ts_delta(ts_backfill(vec_avg(shrt3_bar), 132), 220), sector),
  group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings), 132), 252), sector)
), market)
```

借款需求评分（做空拥挤度）× 内部人持股 52 周位置（知情者信息优势）。塔 SHORT+INSIDERS。

## 四、九条可复用方法论（本战役沉淀）

| # | 结论 | 证据 |
|---:|---|---|
| M1 | **字段版本（覆盖率）选择 > 骨架/窗口调参** | `_p5_d1` 版 S 1.40→1.91，同骨架同机制 |
| M2 | **F = S × sqrt(R/max(TO,0.125))**，TO 甜点=0.125 | 多件反算误差 <0.002 |
| M3 | **设置层不是杠杆**：nanHandling=OFF / decay=0 均让 S 暴跌 1.0+ | BE20 4 臂 + SET1 4 臂 |
| M4 | **天花板是极窄单点**（字段×频率×骨架） | fundamental6 同族 20 字段全负 |
| M5 | **强腿换搭档仍强**才算真强腿 | max_loan_rate × I7=1.91，× oth47=1.92 |
| M6 | **self=1.0 即重复件** | E569ZE7L 撞 78Yk8VR1 |
| M7 | **LOW_SUB 解法：第二腿加 ts_mean 11**，降 S 同时降门槛 | LLKP3pm1 0.88 fail → 9qlz29Oe 0.89 pass |
| M8 | **sub 门槛不可用 0.474×S 估算**，边界件必查平台 checks | 两件千分位边界判出相反结果 |
| M9 | **coverage=0 ≈ 区域无数据**，判据看 longCount<100 | fundamental6 0.49→1.73；f89 →0.69；f72 lc=26→-0.56 |

## 五、档案索引

| 文档 | 内容 |
|---|---|
| ALPHA11_CONFIRMED_9qlz29Oe_20261111.md | 第 11 颗完整档案 + 11 颗汇总 |
| GOAL_ACHIEVED_10TH_ALPHA_20261111.md | 第 10 颗 d5a2vxzY 十一闸验证 |
| WAVE_BE21_P5D1_BREAKTHROUGH_20261111.md | _p5_d1 增量面突破 |
| WAVE_BE22_STRONGLEG_NONI7_20261111.md | 强腿×非I7第二腿（5 颗全闸） |
| WAVE_BE24/25 | shortinterest3 单塔空间穷尽（16 臂） |
| WAVE_F72_DATA_SPARSE_20261111.md | fundamental72 稀疏实证 + 32 个数据集收口 |
| FIELD_PROFILE_CORE_DATASETS_20261111.md | 核心数据集字段画像 |
| DATASET_USABILITY_MASTER_20261111.md | 29 项数据集可用性总表 |
| RECIPE_MATRIX_SHORTINTEREST_20261110.md | 借券族配方矩阵 |
| DEU_OS_INVENTORY_AND_DELTA_20261111.md | DEU 20 颗 ACTIVE 权威清单 |

## 六、唯一未完成项

**5 颗待授权件的提交**（提交不可逆，需用户明确文字授权）。
其中 RREPm361 的 prod 平台重算已超 45 分钟仍未出值（历史读数 0.6881）；其余 4 颗 prod 均已实测通过。