# Robustness 审计报告 2026-11-14（DEU）

## pwaQ0bx3 — fnd1 CEO 任期治理因子（ATOM）

**表达式**：`tail(winsorize(group_zscore(group_backfill(ts_backfill(vec_avg(fnd1_board_characteristics_filtered_timerole),250),sector,250),sector),std=4),lower=-0.95,upper=0.95,newval=0)`

**设置**：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON/maxTrade OFF
**构造谱系**：BE251 存在性探针（治理三活体）→ BE252 rank+tail → BE253-254 带宽网格 → BE257 zscore 量级形态 → BE258-261 gBF 修 CW + 带宽 ±0.95 + std4（用户 group_backfill 指令）

### 指标

| 项 | 值 | 闸 |
|---|---:|---|
| Sharpe | 1.60 | ≥1.58 ✅ |
| Fitness | 1.40 | ≥1.0 ✅ |
| 2Y Sharpe | 2.01 | ✅ |
| Sub-universe | 1.25 | ✅（平台 LOW_SUB_UNIVERSE_SHARPE PASS）|
| prod | 0.6821 | <0.7 ✅（refresh 实测，直方图健康：尾部 [0.6,0.7) 仅 3 名）|
| 篮内互相关 | max 0.1385 | <0.7 ✅（对 17 颗交付篮全对，18 颗全矩阵 all_below）|
| failed_ra_count | 0 | ✅ |
| TO / DD / margin | 2.6% / 7.6% / 74bp | 远离噪声拟合线 ✅ |
| 算子数 | 6 | 软标记（>5）|

### Phase B 逐年（IS 2014–2023）

| 年 | S | returns | lc/sc |
|---|---:|---:|---|
| 2014 | -0.03 | -0.2% | 81/92 |
| 2015 | 0.94 | 5.6% | 82/78 |
| 2016 | 0.54 | 3.3% | 78/86 |
| 2017 | 2.02 | 11.4% | 94/84 |
| 2018 | 2.50 | 15.4% | 109/86 |
| 2019 | 1.45 | 6.8% | 95/111 |
| 2020 | 0.16 | 1.0% | 122/113 |
| 2021 | 4.07 | 26.3% | 146/145 |
| 2022 | 2.78 | 18.1% | 142/160 |
| 2023 | 1.19 | 7.3% | 120/153 |

- Recent-3yr（2021/22/23）：全正（>0.3）✓，均值 2.68 ≥ 1.58 ✓；平台 2Y 检查 PASS（2.01）
- 衰减比 = 1.19/1.60 = **0.74 ≥ 0.50** ✓
- Recent-3yr CV_Sharpe = 1.18/2.68 = **0.44**（0.40–0.60 标警带，软标记）
- Recent-3yr max/min = 4.07/1.19 = **3.42**（3–5 标警带，软标记）
- 平年（近 3 年 |S|<0.3）：0 ✓
- 早年疲软（2014 平年 / 2020 弱年）：全历史软标记，不参与判定

### Phase C 判定

| 检查项 | 结果 |
|---|---|
| WebDataScope failed count | 0/0 ✅ |
| Recent-3yr Sharpe | PASS |
| CV_Sharpe | 0.44 → 标警（软）|
| 衰减比 | PASS |
| 平年 | 0 ✅ |
| max/min | 3.42 → 标警（软）|
| Sub-universe | 平台 PASS |
| 算子数 | 6 → 软标记 |
| Margin @ TO | 74bp @ 2.6% PASS |
| Top-5 集中度 | 未算（逐股 PnL 未返回，可选）|
| 经济可解释性 | 「CEO 在任时间长 ⇒ 管理层稳定/经验溢价，治理慢变量定价不足」一句话可写 ✅ |

**硬 REJECT 项：0。判定 = PASS（soft_flags: CV_Sharpe=0.44, max_min=3.42, ops=6, 2014_flat_year）**

### 备注

- submit_verdict(pwaQ0bx3) = UNVERIFIABLE（非 BLOCKED，failed_any=0，硬闸 warning 空）
- prod 实测 refresh=True 0.6821 all_passed；家族同核四读数 0.6805/0.656/0.6276/0.6821 全 <0.7
- 篮内互相关对 17 颗交付篮 max 0.1385（Jj8VQwoe），18 颗全矩阵 <0.7
- 近十年闸注记：2014 年 pnl −17.6K（−0.09%，治理数据首年爬坡），严格 pnl>0 不满足但非零持仓缺陷，如实交用户裁量
- ATOM 路径：SINGLE_DATA_SET / ATOM:LAST_2Y（免 IS Ladder）
- 用户已明确确认提交（2026-11-14 会话内原话「确认」）
