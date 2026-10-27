# model264 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model264` |
| 名称 | Predictive data using Deep Learning models |
| 类别 | MODEL |
| 数据字段数(平台) | 1393 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 68 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

The Wolfe Research Equity Factor Model is a comprehensive quantitative dataset offering over 270 numerical factors for global equities, with history dating back to 1986. It includes a wide array of factor categories such as value, growth, quality, momentum, volatility, analyst sentiment, technical indicators, and alternative data signals. The dataset provides both raw and sector/region-neutralized versions of factors, as well as point-in-time and forward-looking metrics, making it suitable for robust backtesting and live signal generation. With detailed coverage of analyst revisions, earnings surprises, price momentum, liquidity, and risk metrics, this factor library enables systematic investors to construct, test, and optimize multi-factor stock selection models, perform risk attribution,

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **1393** |
| 类型分布 | MATRIX×1393 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 快照（按库表更新，需实测） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 1393 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 1380 | 99.1% |
| DEAD | 12 | 0.9% |
| DEAD_STATIC | 1 | 0.1% |

- 已实测字段：**13** 个（1%），best_sharpe 最高 **0.48**，中位 -0.02

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 816 | 1.00 | mdl264_asti_l3、mdl264_ouie_class、mdl264_mthk_class |
| 盈利与财务 | 311 | 1.00 | mdl264_1l_ppgs、mdl264_1l_rltr、mdl264_2l_mpns |
| 修正与预期 | 114 | 1.00 | mdl264_1l_m1r_cer_se、mdl264_1l_m1r_1yf_spe_se、mdl264_1l_ivn |
| 价量与波动 | 93 | 1.00 | mdl264_1l_m1m21_ntr、mdl264_1l_d0252ntr、mdl264_1l_d12ntr |
| 持仓与资金流 | 24 | 1.00 | mdl264_1l_boie、mdl264_1l_btsl、mdl264_1l_fmc |
| 宏观与行业 | 20 | 1.00 | mdl264_1l_icc、mdl264_2l_icc、mdl264_3l_icc |
| 情绪与新闻 | 8 | 1.00 | mdl264_news_abno_sent_1d_class、mdl264_news_abno_sent_1d_l1、mdl264_news_abno_sent_1d_l2 |
| 元数据与非信号 | 6 | 1.00 | mdl264_1l_vdav、mdl264_2l_vdav、mdl264_3l_vdav |
| 搜索与替代数据 | 1 | 1.00 | mdl264_appy_class |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl264_1l_ppgs` | MATRIX | 1.000 | 盈利与财务 | 1 | 0.48 | — | — | DEAD | The probability that the future trend of "Gross Margin" will fall |
| 2 | `mdl264_asti_l3` | MATRIX | 1.000 | 其他 | 1 | 0.26 | — | — | DEAD | The probability that the future trend of "Short Term Investments" will be move-up |
| 3 | `mdl264_1l_rltr` | MATRIX | 1.000 | 盈利与财务 | 1 | 0.25 | — | — | DEAD | The probability that the future trend of "Total Revenue" will be fall |
| 4 | `mdl264_2l_mpns` | MATRIX | 1.000 | 盈利与财务 | 1 | 0.20 | — | — | DEAD | The probability that the future trend of "Net Profit Margin" will be neutral |
| 5 | `mdl264_1l_m1r_cer_se` | MATRIX | 1.000 | 修正与预期 | 1 | 0.13 | — | — | DEAD | Probability that the future trend of "Recommendation revision, 1M" will be fall |
| 6 | `mdl264_1l_m1r_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 1 | 0.05 | — | — | DEAD | Probability that the future trend of "FY1 EPS revision, 1M" will be fall |
| 7 | `mdl264_1l_m1m21_ntr` | MATRIX | 1.000 | 价量与波动 | 1 | -0.02 | — | — | DEAD | Probability that the future trend of Price momentum, 12M-1M will be fall |
| 8 | `mdl264_ouie_class` | MATRIX | 1.000 | 其他 | 1 | -0.17 | — | — | DEAD | Predicted trend of 'Unusual Items' (1: fall, 2: neutral, 3: move up) |
| 9 | `mdl264_mthk_class` | MATRIX | 1.000 | 其他 | 1 | -0.29 | — | — | DEAD_STATIC | Predicted trend of "Number of Stores Opened" (1: fall, 2: neutral, 3: move-up) |
| 10 | `mdl264_1l_rta` | MATRIX | 1.000 | 其他 | 1 | -0.31 | — | — | DEAD | Probability that the future trend of Average True Range will be fall |
| 11 | `mdl264_macd_class` | MATRIX | 1.000 | 其他 | 1 | -0.52 | — | — | DEAD | Predicted trend of the Moving Average Convergence/Divergence (MACD): 1=fall, 2=neutral, 3=move-up |
| 12 | `mdl264_1l_d0252ntr` | MATRIX | 1.000 | 价量与波动 | 1 | -0.61 | — | — | DEAD | Probability that the future trend of "Total return, past 120M" will be fall |
| 13 | `mdl264_1l_dlts` | MATRIX | 1.000 | 盈利与财务 | 1 | -0.88 | — | — | DEAD | The probability that the future trend of 'Total Debt' will fall |
| 14 | `mdl264_1l_01dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 10' will fall |
| 15 | `mdl264_1l_1dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing Within 1 Year" will be fall |
| 16 | `mdl264_1l_1nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Treas Shares - Common Stock Primary Issue" will fall |
| 17 | `mdl264_1l_1ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Shares Outstanding - Preferred Primary Issue' will fall |
| 18 | `mdl264_1l_1ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Phase I' will fall |
| 19 | `mdl264_1l_1spdd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "DPS - Common Stock Primary Issue" will fall |
| 20 | `mdl264_1l_1spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Special DPS - Common Stock Primary Issue' will fall |
| 21 | `mdl264_1l_2dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 2" will fall |
| 22 | `mdl264_1l_2lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 2" will fall |
| 23 | `mdl264_1l_2nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Treasury Shares - Common Issue 2" will fall |
| 24 | `mdl264_1l_2ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Shares Outstanding - Preferred Issue 2" will be fall |
| 25 | `mdl264_1l_2ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Phase II' will fall |
| 26 | `mdl264_1l_2spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Dividends per Share - Com Stock Issue 2" will be fall |
| 27 | `mdl264_1l_2spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Special DPS - Common Stock Issue 2" will fall |
| 28 | `mdl264_1l_32lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in 2-3 Years' will fall |
| 29 | `mdl264_1l_3dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long-Term Debt Maturing in Year 3" will be fall |
| 30 | `mdl264_1l_3lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 3" will fall |
| 31 | `mdl264_1l_3ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Phase III' will fall |
| 32 | `mdl264_1l_3spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Dividends per Share - Com Stock Issue 3" will fall |
| 33 | `mdl264_1l_4lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 4' will be fall |
| 34 | `mdl264_1l_54dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long-Term Debt Maturing in 4-5 Years" will be fall |
| 35 | `mdl264_1l_54lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in 4-5 Years' will fall |
| 36 | `mdl264_1l_57_03_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Moving average crossover, 30W-75W" will be fall |
| 37 | `mdl264_1l_5dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 5" will be fall |
| 38 | `mdl264_1l_5lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 5" will fall |
| 39 | `mdl264_1l_63_51_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of the 15W-36W moving average crossover will be fall |
| 40 | `mdl264_1l_7dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 7' will fall |
| 41 | `mdl264_1l_8dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 8" will be fall |
| 42 | `mdl264_1l_abpo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Payable/Accrued' will fall |
| 43 | `mdl264_1l_acda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Current Asset" will fall |
| 44 | `mdl264_1l_acf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Exchange Income (Loss)" will be fall |
| 45 | `mdl264_1l_acoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets' will fall |
| 46 | `mdl264_1l_adbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized EBITDA" will be fall |
| 47 | `mdl264_1l_aemc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Miscellaneous Earnings Adjustment" will be fall |
| 48 | `mdl264_1l_aiec` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Equity in Affiliates' will fall |
| 49 | `mdl264_1l_alge` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Loss(Gain) on Sale of Assets - Operating' will fall |
| 50 | `mdl264_1l_algn` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Gain (Loss) on Sale of Assets" will fall |
| 51 | `mdl264_1l_algv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "(Gain) Loss on Sale of Assets, Suppl." will be a fall |
| 52 | `mdl264_1l_b6dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Matur. in Year 6 & Beyond" will be fall |
| 53 | `mdl264_1l_bb` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Bollinger Bands" will be fall |
| 54 | `mdl264_1l_biis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Income, Bank" will fall |
| 55 | `mdl264_1l_bloo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Liabilities" will fall |
| 56 | `mdl264_1l_boie` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest on Other Borrowings" will be fall |
| 57 | `mdl264_1l_bpao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Accounts Payable' will fall |
| 58 | `mdl264_1l_btsl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Short Term Borrowings' will fall |
| 59 | `mdl264_1l_caic` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Available to Com Excl ExtraOrd" will fall |
| 60 | `mdl264_1l_cbbm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "EBITDAR" will fall |
| 61 | `mdl264_1l_ccns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Change in Cash" will fall |
| 62 | `mdl264_1l_cfda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Charges" will fall |
| 63 | `mdl264_1l_cifv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Interest Cost - Foreign' will fall |
| 64 | `mdl264_1l_cinx` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Available to Com Incl ExtraOrd" will fall |
| 65 | `mdl264_1l_cniv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Costs" will fall |
| 66 | `mdl264_1l_csfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Service Cost - Foreign" will fall |
| 67 | `mdl264_1l_cspv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Service Cost - Post-Retirement" will fall |
| 68 | `mdl264_1l_ctcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Total" will be fall |
| 69 | `mdl264_1l_ctda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Income Tax - Current Asset" will fall |
| 70 | `mdl264_1l_ctdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Income Tax - Current Liability" will fall |
| 71 | `mdl264_1l_ctdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Total" will be fall |
| 72 | `mdl264_1l_d12ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total return, past 1M" will be fall |
| 73 | `mdl264_1l_d36ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of 3-month total return will be fall |
| 74 | `mdl264_1l_dbtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Comp. Store Sales, Retail, Total - %' will fall |
| 75 | `mdl264_1l_dcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Service Cost - Domestic' will fall |
| 76 | `mdl264_1l_dlyspe_rh` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of historical relative earnings yield will be fall |
| 77 | `mdl264_1l_drpc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Preferred Dividends" will be fall |
| 78 | `mdl264_1l_drpf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Issuance (Retirement) of Debt, Net' will fall |
| 79 | `mdl264_1l_dtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Domestic" will be fall |
| 80 | `mdl264_1l_dtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Domestic" will fall |
| 81 | `mdl264_1l_dtov` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Domestic Tax - Other' will fall |
| 82 | `mdl264_1l_dtsl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Notes Payable/Short Term Debt" will be fall |
| 83 | `mdl264_1l_eaca` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Cash & Equivalents" will be fall |
| 84 | `mdl264_1l_ebbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Passengers, Total" will fall |
| 85 | `mdl264_1l_ecns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Cash - Ending Balance" will be fall |
| 86 | `mdl264_1l_eins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Non-Interest Expense, Bank" will fall |
| 87 | `mdl264_1l_eiue` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income)' will fall |
| 88 | `mdl264_1l_eiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Expense" will be fall |
| 89 | `mdl264_1l_eiuo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unusual Items" will be fall |
| 90 | `mdl264_1l_eiuv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income), Suppl.' will fall |
| 91 | `mdl264_1l_ejtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Value of Bookings" will fall |
| 92 | `mdl264_1l_eoos` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Operating Expenses, Total" will fall |
| 93 | `mdl264_1l_eprv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Post-Retirement Plan Expense" will be fall |
| 94 | `mdl264_1l_epts` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Expected Return" will be fall |
| 95 | `mdl264_1l_eptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Pension Expense" will fall |
| 96 | `mdl264_1l_epxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Post-Retirement, Net' will fall |
| 97 | `mdl264_1l_erpm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Pre-Registration' will fall |
| 98 | `mdl264_1l_etoq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Equity" will fall |
| 99 | `mdl264_1l_fmc` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Chaikin Money Flow" will be fall |
| 100 | `mdl264_1l_fotv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "All Other Fees" will be fall |
| 101 | `mdl264_1l_ftcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Foreign" will fall |
| 102 | `mdl264_1l_ftdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Foreign" will be fall |
| 103 | `mdl264_1l_fttv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Tax Fees" will fall |
| 104 | `mdl264_1l_gaxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Actuarial Gains and Losses - Domestic" will be fall |
| 105 | `mdl264_1l_gdbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Available Seat Kilometers (ASK)" will be fall |
| 106 | `mdl264_1l_ghc_qe_td_tl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "YoY change in long-term debt/common equity" will be fall |
| 107 | `mdl264_1l_gjbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Expense per ASK" will fall |
| 108 | `mdl264_1l_htrm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Rent Growth (Sequential), Total -%" will fall |
| 109 | `mdl264_1l_iabs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Basic EPS Including Extraordinary Items" will be fall |
| 110 | `mdl264_1l_iads` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Diluted EPS Including ExtraOrd Items" will fall |
| 111 | `mdl264_1l_icc` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Commodity Channel Index" will be fall |
| 112 | `mdl264_1l_ifm` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Money Flow Index will be fall |
| 113 | `mdl264_1l_iins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Maturity of Investment" will be fall |
| 114 | `mdl264_1l_iirr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Reinsurance - Income' will fall |
| 115 | `mdl264_1l_iiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Income" will fall |
| 116 | `mdl264_1l_im` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Mass Index will be fall |
| 117 | `mdl264_1l_inds` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Diluted Net Income" will be fall |
| 118 | `mdl264_1l_ips` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special Items will be fall |
| 119 | `mdl264_1l_ipts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Interest Cost" will be fall |
| 120 | `mdl264_1l_iscs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Cash and Short-Term Investments" will be fall |
| 121 | `mdl264_1l_isir` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest & Dividends on Investment Secs." will fall |
| 122 | `mdl264_1l_ist` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of True Strength Index will be fall |
| 123 | `mdl264_1l_ists` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Special Items" will be fall |
| 124 | `mdl264_1l_itpv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized Income Before Taxes' will fall |
| 125 | `mdl264_1l_iv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Vortex Indicator will be fall |
| 126 | `mdl264_1l_ivn` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of the Negative Volume Index will be fall |
| 127 | `mdl264_1l_ixts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Extraordinary Items' will fall |
| 128 | `mdl264_1l_kcqs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Quick Ratio" will fall |
| 129 | `mdl264_1l_khtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Stores Opened' will fall |
| 130 | `mdl264_1l_laoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Assets & Liabilities, Net" will fall |
| 131 | `mdl264_1l_lbtm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Merchandise Margins, Total -%" will fall |
| 132 | `mdl264_1l_lcdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Curr Liability" will be a fall |
| 133 | `mdl264_1l_lctv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Capital Leases, Supplemental" will fall |
| 134 | `mdl264_1l_lda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Accumulation Distribution Line will be fall |
| 135 | `mdl264_1l_ldav` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Revenue - Long Term" will be fall |
| 136 | `mdl264_1l_ldbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Load Factor, Total -%" will fall |
| 137 | `mdl264_1l_lgrr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Realized & Unrealized Gains (Losses)" will be fall |
| 138 | `mdl264_1l_lgsn` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Investment Securities Gains" will fall |
| 139 | `mdl264_1l_lguq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unrealized Gain (Loss)" will fall |
| 140 | `mdl264_1l_lppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products Launched' will fall |
| 141 | `mdl264_1l_ltcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Local" will fall |
| 142 | `mdl264_1l_ltdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Local" will be fall |
| 143 | `mdl264_1l_ltio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inventories" will fall |
| 144 | `mdl264_1l_ltll` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Liabilities' will fall |
| 145 | `mdl264_1l_m1d_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 BPS diffusion (up/down ratio), 1M will be fall |
| 146 | `mdl264_1l_m1d_1yf_spd_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 DPS diffusion (up/down ratio), 1M" will be fall |
| 147 | `mdl264_1l_m1d_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 EPS diffusion (up/down ratio), 1M will be fall |
| 148 | `mdl264_1l_m1d_1yf_spfc_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 CFPS diffusion (up/down ratio), 1M will be fall |
| 149 | `mdl264_1l_m1d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV diffusion (up/down ratio), 1M will be fall |
| 150 | `mdl264_1l_m1d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of Recommendation diffusion (up/down ratio), 1M will be fall |
| 151 | `mdl264_1l_m1d_gtl_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long-term growth diffusion (up/down ratio), 1M" will be fall |
| 152 | `mdl264_1l_m1d_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Target price diffusion (up/down ratio), 1M" will be fall |
| 153 | `mdl264_1l_m1r_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 BPS revision over 1 month will be fall |
| 154 | `mdl264_1l_m1r_1yf_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 DPS revision, 1M will be fall |
| 155 | `mdl264_1l_m1r_1yf_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 CFPS revision, 1M will be fall |
| 156 | `mdl264_1l_m1r_1yf_van_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV revision, 1M will be fall |
| 157 | `mdl264_1l_m1r_gtl_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of long-term growth revision, 1M will be fall |
| 158 | `mdl264_1l_m1r_mtn_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM DPS revision over 1 month will be fall |
| 159 | `mdl264_1l_m1r_mtn_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "NTM EPS revision, 1M" will be fall |
| 160 | `mdl264_1l_m1r_mtn_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM CFPS revision, 1M will be fall |
| 161 | `mdl264_1l_m1r_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Target price revision, 1M" will be fall |
| 162 | `mdl264_1l_m3d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV diffusion (up/down ratio) over 3 months will be fall |
| 163 | `mdl264_1l_m3d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation diffusion (up/down ratio), 3M will be fall |
| 164 | `mdl264_1l_m3r_mtn_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM BPS revision over 3 months will be fall |
| 165 | `mdl264_1l_mocq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Comprehensive Income" will fall |
| 166 | `mdl264_1l_mpns` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Profit Margin' will fall |
| 167 | `mdl264_1l_mtps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Pretax Margin" will be fall |
| 168 | `mdl264_1l_ndsf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Short Term Debt, Net" will fall |
| 169 | `mdl264_1l_niis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest/Invest Income - Non-Operating" will be fall |
| 170 | `mdl264_1l_nins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Inc.(Exp.),Net-Non-Op., Total" will fall |
| 171 | `mdl264_1l_nscf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Common Stock, Net' will fall |
| 172 | `mdl264_1l_ntiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inc Tax Ex Impact of Sp Items" will fall |
| 173 | `mdl264_1l_nvii` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Investment, Net' will fall |
| 174 | `mdl264_1l_oc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Chaikin Oscillator" will be fall |
| 175 | `mdl264_1l_ocl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of Current Liabilities Other Total will be fall |
| 176 | `mdl264_1l_od` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Discontinued Operations will be a fall |
| 177 | `mdl264_1l_oiis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest/Investment Income - Operating" will fall |
| 178 | `mdl264_1l_oinm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Interest Margin, Total -%" will be fall |
| 179 | `mdl264_1l_olcl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Obligations' will fall |
| 180 | `mdl264_1l_ompd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of DecisionPoint Price Momentum Oscillator will be fall |
| 181 | `mdl264_1l_opd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Detrended Price Oscillator will be fall |
| 182 | `mdl264_1l_opp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of percentage price oscillator will be fall |
| 183 | `mdl264_1l_optq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Preferred Shares Outstanding" will be fall |
| 184 | `mdl264_1l_opxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Pension, Net - Domestic' will fall |
| 185 | `mdl264_1l_os` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of the Stochastic Oscillator will be fall |
| 186 | `mdl264_1l_otcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Other" will be fall |
| 187 | `mdl264_1l_otdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Other" will fall |
| 188 | `mdl264_1l_ovp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Percentage Volume Oscillator" will be fall |
| 189 | `mdl264_1l_pcrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Repurch./Retirement of Common/Preferred" will be fall |
| 190 | `mdl264_1l_pcsf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Common/Preferred" will fall |
| 191 | `mdl264_1l_pcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Stock-Based Compensation, Supplemental' will fall |
| 192 | `mdl264_1l_pffl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FedFundsPurch/ScrtySoldUnderRepurchAgrmt" will be fall |
| 193 | `mdl264_1l_poer` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Electric Operations" will be fall |
| 194 | `mdl264_1l_ppdf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Cash Dividends Paid - Preferred" will be fall |
| 195 | `mdl264_1l_ppdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Domestic Pension Plan Expense" will be fall |
| 196 | `mdl264_1l_ppfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Foreign Pension Plan Expense' will fall |
| 197 | `mdl264_1l_prrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Repurchase/Retirement of Preferred" will fall |
| 198 | `mdl264_1l_pxtl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Taxes Payable" will fall |
| 199 | `mdl264_1l_qbbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Revenue Passenger Kilometers (RPK)" will be fall |
| 200 | `mdl264_1l_rcao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts Receivable" will be fall |
| 201 | `mdl264_1l_rinr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Non-Insurance Revenue" will fall |
| 202 | `mdl264_1l_rpts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Other Expense" will fall |
| 203 | `mdl264_1l_rpul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unearned Premium/Unearned Revenue" will fall |
| 204 | `mdl264_1l_rtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Current Tax - Total' will fall |
| 205 | `mdl264_1l_rtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Total" will fall |
| 206 | `mdl264_1l_rw` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Williams %R" will be fall |
| 207 | `mdl264_1l_rxfv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Expected Return on Assets - Foreign" will be fall |
| 208 | `mdl264_1l_saie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Impairment-Assets Held for Sale' will fall |
| 209 | `mdl264_1l_saoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Assets" will fall |
| 210 | `mdl264_1l_sern` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge' will fall |
| 211 | `mdl264_1l_serv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge, Supplemental' will fall |
| 212 | `mdl264_1l_spe_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Historical 5Y EPS growth trend will be fall |
| 213 | `mdl264_1l_speo_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Historical 5Y operating EPS growth trend" will be fall |
| 214 | `mdl264_1l_spfc_rtnie_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of YoY expected interim CFPS growth will be fall |
| 215 | `mdl264_1l_spfc_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Historical 5Y CFPS growth trend will be fall |
| 216 | `mdl264_1l_spts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Service Cost" will fall |
| 217 | `mdl264_1l_sptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prior Service Cost - Domestic' will fall |
| 218 | `mdl264_1l_sspf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Issuance (Retirement) of Stock, Net' will fall |
| 219 | `mdl264_1l_stnr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Sales" will fall |
| 220 | `mdl264_1l_tait` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Income After Taxes" will be fall |
| 221 | `mdl264_1l_tbie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Income Before Taxes" will fall |
| 222 | `mdl264_1l_tcxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Curtailments & Settlements - Domestic" will fall |
| 223 | `mdl264_1l_tdbo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Taxes" will be fall |
| 224 | `mdl264_1l_tdtv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Domestic Tax' will fall |
| 225 | `mdl264_1l_tftv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Tax" will fall |
| 226 | `mdl264_1l_toia` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inventories - Other" will be fall |
| 227 | `mdl264_1l_tpda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest-Earning Deposits" will fall |
| 228 | `mdl264_1l_tpv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Volume Price Trend will be fall |
| 229 | `mdl264_1l_ttiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Tax - Total" will be fall |
| 230 | `mdl264_1l_uaie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Use" will be fall |
| 231 | `mdl264_1l_vbo` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of On Balance Volume will be fall |
| 232 | `mdl264_1l_vcwf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Warrants Converted" will be fall |
| 233 | `mdl264_1l_vdav` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Advertising Expense, Supplemental" will be fall |
| 234 | `mdl264_1l_vlc` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of Close Location Value will be fall |
| 235 | `mdl264_1l_vme` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Ease of Movement will be fall |
| 236 | `mdl264_1l_vnie` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Investment Income - Operating" will fall |
| 237 | `mdl264_1l_xeao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Accrued Expenses' will fall |
| 238 | `mdl264_1l_xefe` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Fuel Expense' will fall |
| 239 | `mdl264_1l_xeon` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Expense" will fall |
| 240 | `mdl264_1l_yppa` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prepaid Expenses' will fall |
| 241 | `mdl264_1l_yppo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prepaid Expenses' will fall |
| 242 | `mdl264_1l_zahm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Rooms" will fall |
| 243 | `mdl264_2l_01dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 10" will be neutral |
| 244 | `mdl264_2l_1dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing Within 1 Year" will be neutral |
| 245 | `mdl264_2l_1nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Treas Shares - Common Stock Primary Issue" will be neutral |
| 246 | `mdl264_2l_1ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Shares Outstanding - Preferred Primary Issue" will be neutral |
| 247 | `mdl264_2l_1spdd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "DPS - Common Stock Primary Issue" will be neutral |
| 248 | `mdl264_2l_1spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Special DPS - Common Stock Primary Issue" will be neutral |
| 249 | `mdl264_2l_2dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 2" will be neutral |
| 250 | `mdl264_2l_2lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 2" will be neutral |
| 251 | `mdl264_2l_2nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Treasury Shares - Common Issue 2" will be neutral |
| 252 | `mdl264_2l_2ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Shares Outstanding - Preferred Issue 2" will be neutral |
| 253 | `mdl264_2l_2ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Products in Phase II" will be neutral |
| 254 | `mdl264_2l_2spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Dividends per Share - Com Stock Issue 2" will be neutral |
| 255 | `mdl264_2l_2spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Special DPS - Common Stock Issue 2" will be neutral |
| 256 | `mdl264_2l_32lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in 2-3 Years" will be neutral |
| 257 | `mdl264_2l_3dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long-Term Debt Maturing in Year 3" will be neutral |
| 258 | `mdl264_2l_3lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 3' will be neutral |
| 259 | `mdl264_2l_4lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 4" will be neutral |
| 260 | `mdl264_2l_54dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in 4-5 Years" will be neutral |
| 261 | `mdl264_2l_54lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in 4-5 Years" will be neutral |
| 262 | `mdl264_2l_57_03_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Moving average crossover, 30W-75W" will be neutral |
| 263 | `mdl264_2l_5dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 5" will be neutral |
| 264 | `mdl264_2l_5lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 5" will be neutral |
| 265 | `mdl264_2l_63_51_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of the 15W-36W moving average crossover will be neutral |
| 266 | `mdl264_2l_7dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 7" will be neutral |
| 267 | `mdl264_2l_8dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 8" will be neutral |
| 268 | `mdl264_2l_abpo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Payable/Accrued" will be neutral |
| 269 | `mdl264_2l_acda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Current Asset" will be neutral |
| 270 | `mdl264_2l_acf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Foreign Exchange Income (Loss) will be neutral |
| 271 | `mdl264_2l_acoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Current Assets" will be neutral |
| 272 | `mdl264_2l_adbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized EBITDA" will be neutral |
| 273 | `mdl264_2l_aemc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Miscellaneous Earnings Adjustment" will be neutral |
| 274 | `mdl264_2l_aiec` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Equity in Affiliates" will be neutral |
| 275 | `mdl264_2l_alge` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Loss(Gain) on Sale of Assets - Operating" will be neutral |
| 276 | `mdl264_2l_algn` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Gain (Loss) on Sale of Assets" will be neutral |
| 277 | `mdl264_2l_algv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "(Gain) Loss on Sale of Assets, Suppl." will be neutral |
| 278 | `mdl264_2l_b6dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Matur. in Year 6 & Beyond" will be neutral |
| 279 | `mdl264_2l_bb` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Bollinger Bands" will be neutral |
| 280 | `mdl264_2l_biis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Income, Bank" will be neutral |
| 281 | `mdl264_2l_bloo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Liabilities" will be neutral |
| 282 | `mdl264_2l_boie` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest on Other Borrowings" will be neutral |
| 283 | `mdl264_2l_bpao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts Payable" will be neutral |
| 284 | `mdl264_2l_btsl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Short Term Borrowings" will be neutral |
| 285 | `mdl264_2l_caic` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Available to Com Excl ExtraOrd" will be neutral |
| 286 | `mdl264_2l_ccns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Change in Cash" will be neutral |
| 287 | `mdl264_2l_cfda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Charges" will be neutral |
| 288 | `mdl264_2l_cifv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Cost - Foreign" will be neutral |
| 289 | `mdl264_2l_cinx` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Available to Com Incl ExtraOrd" will be neutral |
| 290 | `mdl264_2l_cspv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Service Cost - Post-Retirement" will be neutral |
| 291 | `mdl264_2l_ctcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Total" will be neutral |
| 292 | `mdl264_2l_ctda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Income Tax - Current Asset" will be neutral |
| 293 | `mdl264_2l_ctdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Income Tax - Current Liability" will be neutral |
| 294 | `mdl264_2l_ctdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Total" will be neutral |
| 295 | `mdl264_2l_d0252ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Total return, past 120M" will be neutral |
| 296 | `mdl264_2l_d12ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total return, past 1M" will be neutral |
| 297 | `mdl264_2l_d36ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of 3-month total return will be neutral |
| 298 | `mdl264_2l_dbtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Comp. Store Sales, Retail, Total - %" will be neutral |
| 299 | `mdl264_2l_dcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Service Cost - Domestic" will be neutral |
| 300 | `mdl264_2l_dlts` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Debt" will be neutral |
| 301 | `mdl264_2l_dlyspe_rh` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of historical relative earnings yield will be neutral |
| 302 | `mdl264_2l_drpc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Preferred Dividends" will be neutral |
| 303 | `mdl264_2l_drpf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Issuance (Retirement) of Debt, Net" will be neutral |
| 304 | `mdl264_2l_dtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Domestic" will be neutral |
| 305 | `mdl264_2l_dtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Domestic" will be neutral |
| 306 | `mdl264_2l_dtov` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Domestic Tax - Other" will be neutral |
| 307 | `mdl264_2l_dtsl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Notes Payable/Short Term Debt" will be neutral |
| 308 | `mdl264_2l_eaca` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Cash & Equivalents" will be neutral |
| 309 | `mdl264_2l_ebbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Passengers, Total" will be neutral |
| 310 | `mdl264_2l_ecns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Cash - Ending Balance" will be neutral |
| 311 | `mdl264_2l_eins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Non-Interest Expense, Bank" will be neutral |
| 312 | `mdl264_2l_eiue` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Expense (Income)" will be neutral |
| 313 | `mdl264_2l_eiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Expense" will be neutral |
| 314 | `mdl264_2l_eiuo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unusual Items" will be neutral |
| 315 | `mdl264_2l_eiuv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Expense (Income), Suppl." will be neutral |
| 316 | `mdl264_2l_ejtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Value of Bookings" will be neutral |
| 317 | `mdl264_2l_eoos` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Operating Expenses, Total" will be neutral |
| 318 | `mdl264_2l_eprv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Post-Retirement Plan Expense" will be neutral |
| 319 | `mdl264_2l_epts` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Expected Return" will be neutral |
| 320 | `mdl264_2l_eptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Pension Expense" will be neutral |
| 321 | `mdl264_2l_epxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Post-Retirement, Net" will be neutral |
| 322 | `mdl264_2l_erpm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Products in Pre-Registration" will be neutral |
| 323 | `mdl264_2l_etoq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Equity" will be neutral |
| 324 | `mdl264_2l_fmc` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Chaikin Money Flow" will be neutral |
| 325 | `mdl264_2l_fotv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "All Other Fees" will be neutral |
| 326 | `mdl264_2l_ftcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Foreign" will be neutral |
| 327 | `mdl264_2l_ftdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Foreign" will be neutral |
| 328 | `mdl264_2l_gaxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Actuarial Gains and Losses - Domestic" will be neutral |
| 329 | `mdl264_2l_gdbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Available Seat Kilometers (ASK)" will be neutral |
| 330 | `mdl264_2l_ghc_qe_td_tl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "YoY change in long-term debt/common equity" will be neutral |
| 331 | `mdl264_2l_gjbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Expense per ASK" will be neutral |
| 332 | `mdl264_2l_iabs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Basic EPS Including Extraordinary Items" will be neutral |
| 333 | `mdl264_2l_iads` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Diluted EPS Including Extraordinary Items' will be neutral |
| 334 | `mdl264_2l_icc` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Commodity Channel Index" will be neutral |
| 335 | `mdl264_2l_ifm` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Money Flow Index will be neutral |
| 336 | `mdl264_2l_iins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Maturity of Investment" will be neutral |
| 337 | `mdl264_2l_iirr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Reinsurance - Income" will be neutral |
| 338 | `mdl264_2l_iiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Income" will be neutral |
| 339 | `mdl264_2l_im` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Mass Index will be neutral |
| 340 | `mdl264_2l_inds` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Diluted Net Income" will be neutral |
| 341 | `mdl264_2l_ips` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of Special Items will be neutral |
| 342 | `mdl264_2l_ipts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Interest Cost" will be neutral |
| 343 | `mdl264_2l_iscs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Cash and Short Term Investments" will be neutral |
| 344 | `mdl264_2l_isir` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest & Dividends on Investment Secs." will be neutral |
| 345 | `mdl264_2l_ist` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of True Strength Index will be neutral |
| 346 | `mdl264_2l_ists` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Special Items" will be neutral |
| 347 | `mdl264_2l_itpv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized Income Before Taxes" will be neutral |
| 348 | `mdl264_2l_iv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Vortex Indicator will be neutral |
| 349 | `mdl264_2l_ivn` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of the Negative Volume Index will be neutral |
| 350 | `mdl264_2l_ixts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Extraordinary Items" will be neutral |
| 351 | `mdl264_2l_kcqs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Quick Ratio" will be neutral |
| 352 | `mdl264_2l_khtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Stores Opened" will be neutral |
| 353 | `mdl264_2l_laoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Assets & Liabilities, Net" will be neutral |
| 354 | `mdl264_2l_lbtm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Merchandise Margins, Total -%" will be neutral |
| 355 | `mdl264_2l_lcdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Curr Liability" will be neutral |
| 356 | `mdl264_2l_lctv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Capital Leases, Supplemental" will be neutral |
| 357 | `mdl264_2l_lda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Accumulation Distribution Line will be neutral |
| 358 | `mdl264_2l_ldav` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Revenue - Long Term" will be neutral |
| 359 | `mdl264_2l_lgrr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Realized & Unrealized Gains (Losses)" will be neutral |
| 360 | `mdl264_2l_lgsn` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Investment Securities Gains" will be neutral |
| 361 | `mdl264_2l_lguq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unrealized Gain (Loss)" will be neutral |
| 362 | `mdl264_2l_ltio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inventories" will be neutral |
| 363 | `mdl264_2l_ltll` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Liabilities" will be neutral |
| 364 | `mdl264_2l_m1d_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 BPS diffusion (up/down ratio), 1M will be neutral |
| 365 | `mdl264_2l_m1d_1yf_spd_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 DPS diffusion (up/down ratio), 1M" will be neutral |
| 366 | `mdl264_2l_m1d_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 EPS diffusion (up/down ratio), 1M will be neutral |
| 367 | `mdl264_2l_m1d_1yf_spfc_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 CFPS diffusion (up/down ratio), 1M will be neutral |
| 368 | `mdl264_2l_m1d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV diffusion (up/down ratio), 1M will be neutral |
| 369 | `mdl264_2l_m1d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of Recommendation diffusion (up/down ratio), 1M will be neutral |
| 370 | `mdl264_2l_m1d_gtl_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long-term growth diffusion (up/down ratio), 1M" will be neutral |
| 371 | `mdl264_2l_m1d_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Target price diffusion (up/down ratio), 1M" will be neutral |
| 372 | `mdl264_2l_m1m21_ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Price momentum, 12M-1M will be neutral |
| 373 | `mdl264_2l_m1r_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 BPS revision, 1M" will be neutral |
| 374 | `mdl264_2l_m1r_1yf_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 DPS revision, 1M will be neutral |
| 375 | `mdl264_2l_m1r_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of "FY1 EPS revision, 1M" will be neutral |
| 376 | `mdl264_2l_m1r_1yf_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 CFPS revision, 1M will be neutral |
| 377 | `mdl264_2l_m1r_1yf_van_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV revision, 1M will be neutral |
| 378 | `mdl264_2l_m1r_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Recommendation revision, 1M" will be neutral |
| 379 | `mdl264_2l_m1r_gtl_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Long-term growth revision, 1M" will be neutral |
| 380 | `mdl264_2l_m1r_mtn_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM DPS revision over 1 month will be neutral |
| 381 | `mdl264_2l_m1r_mtn_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "NTM EPS revision, 1M" will be neutral |
| 382 | `mdl264_2l_m1r_mtn_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM CFPS revision, 1M will be neutral |
| 383 | `mdl264_2l_m1r_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Target price revision, 1M" will be neutral |
| 384 | `mdl264_2l_m3d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV diffusion (up/down ratio) over 3 months will be neutral |
| 385 | `mdl264_2l_m3d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation diffusion (up/down ratio), 3M will be neutral |
| 386 | `mdl264_2l_m3r_mtn_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM BPS revision over 3 months will be neutral |
| 387 | `mdl264_2l_mocq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Comprehensive Income" will be neutral |
| 388 | `mdl264_2l_mtps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Pretax Margin" will be neutral |
| 389 | `mdl264_2l_ndsf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Short-term Debt, Net" will be neutral |
| 390 | `mdl264_2l_niis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest/Invest Income - Non-Operating" will be neutral |
| 391 | `mdl264_2l_nins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Inc.(Exp.), Net-Non-Op., Total" will be neutral |
| 392 | `mdl264_2l_nscf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Common Stock, Net" will be neutral |
| 393 | `mdl264_2l_ntiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inc Tax Ex Impact of Sp Items" will be neutral |
| 394 | `mdl264_2l_nvii` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Investment, Net" will be neutral |
| 395 | `mdl264_2l_oc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Chaikin Oscillator" will be neutral |
| 396 | `mdl264_2l_ocl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of Current Liabilities Other Total will be neutral |
| 397 | `mdl264_2l_od` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Discontinued Operations will be neutral |
| 398 | `mdl264_2l_oiis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest/Investment Income - Operating" will be neutral |
| 399 | `mdl264_2l_oinm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Interest Margin, Total -%" will be neutral |
| 400 | `mdl264_2l_olcl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Obligations" will be neutral |
| 401 | `mdl264_2l_ompd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of DecisionPoint Price Momentum Oscillator will be neutral |
| 402 | `mdl264_2l_opd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Detrended Price Oscillator will be neutral |
| 403 | `mdl264_2l_opp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of percentage price oscillator will be neutral |
| 404 | `mdl264_2l_optq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Preferred Shares Outstanding" will be neutral |
| 405 | `mdl264_2l_opxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Pension, Net - Domestic" will be neutral |
| 406 | `mdl264_2l_os` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of the Stochastic Oscillator will be neutral |
| 407 | `mdl264_2l_otcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Other" will be neutral |
| 408 | `mdl264_2l_otdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Other" will be neutral |
| 409 | `mdl264_2l_ovp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Percentage Volume Oscillator" will be neutral |
| 410 | `mdl264_2l_pcrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Repurch./Retirement of Common/Preferred" will be neutral |
| 411 | `mdl264_2l_pcsf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Common/Preferred" will be neutral |
| 412 | `mdl264_2l_pcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Stock-Based Compensation, Supplemental" will be neutral |
| 413 | `mdl264_2l_pffl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FedFundsPurch/ScrtySoldUnderRepurchAgrmt" will be neutral |
| 414 | `mdl264_2l_poer` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Electric Operations" will be neutral |
| 415 | `mdl264_2l_ppdf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Cash Dividends Paid - Preferred" will be neutral |
| 416 | `mdl264_2l_ppdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Domestic Pension Plan Expense" will be neutral |
| 417 | `mdl264_2l_ppfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Pension Plan Expense" will be neutral |
| 418 | `mdl264_2l_ppgs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Gross Margin" will be neutral |
| 419 | `mdl264_2l_prrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Repurchase/Retirement of Preferred" will be neutral |
| 420 | `mdl264_2l_pxtl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Taxes Payable" will be neutral |
| 421 | `mdl264_2l_rcao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts Receivable" will be neutral |
| 422 | `mdl264_2l_rinr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Non-Insurance Revenue" will be neutral |
| 423 | `mdl264_2l_rltr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Revenue" will be neutral |
| 424 | `mdl264_2l_rpts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Other Expense" will be neutral |
| 425 | `mdl264_2l_rpul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unearned Premium/Unearned Revenue" will be neutral |
| 426 | `mdl264_2l_rta` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Average True Range will be neutral |
| 427 | `mdl264_2l_rtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Total" will be neutral |
| 428 | `mdl264_2l_rtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Total" will be neutral |
| 429 | `mdl264_2l_rw` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Williams %R" will be neutral |
| 430 | `mdl264_2l_saie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Sale" will be neutral |
| 431 | `mdl264_2l_saoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Assets" will be neutral |
| 432 | `mdl264_2l_sern` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Restructuring Charge" will be neutral |
| 433 | `mdl264_2l_serv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Restructuring Charge, Supplemental" will be neutral |
| 434 | `mdl264_2l_spe_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Historical 5Y EPS growth trend will be neutral |
| 435 | `mdl264_2l_speo_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Historical 5Y operating EPS growth trend" will be neutral |
| 436 | `mdl264_2l_spfc_rtnie_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of YoY expected interim CFPS growth will be neutral |
| 437 | `mdl264_2l_spfc_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Historical 5Y CFPS growth trend will be neutral |
| 438 | `mdl264_2l_spts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Service Cost" will be neutral |
| 439 | `mdl264_2l_sspf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Issuance (Retirement) of Stock, Net" will be neutral |
| 440 | `mdl264_2l_stnr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Sales" will be neutral |
| 441 | `mdl264_2l_tait` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Income After Taxes" will be neutral |
| 442 | `mdl264_2l_tbie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Income Before Taxes" will be neutral |
| 443 | `mdl264_2l_tdbo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Taxes" will be neutral |
| 444 | `mdl264_2l_tdtv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Domestic Tax" will be neutral |
| 445 | `mdl264_2l_tftv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Tax" will be neutral |
| 446 | `mdl264_2l_toia` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inventories - Other" will be neutral |
| 447 | `mdl264_2l_tpda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest-Earning Deposits" will be neutral |
| 448 | `mdl264_2l_tpv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Volume Price Trend will be neutral |
| 449 | `mdl264_2l_ttiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Tax - Total" will be neutral |
| 450 | `mdl264_2l_uaie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Use" will be neutral |
| 451 | `mdl264_2l_vbo` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of On Balance Volume will be neutral |
| 452 | `mdl264_2l_vcwf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Warrants Converted" will be neutral |
| 453 | `mdl264_2l_vdav` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Advertising Expense, Supplemental" will be neutral |
| 454 | `mdl264_2l_vlc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Close Location Value" will be neutral |
| 455 | `mdl264_2l_vme` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Ease of Movement will be neutral |
| 456 | `mdl264_2l_vnie` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Investment Income - Operating" will be neutral |
| 457 | `mdl264_2l_xeao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accrued Expenses" will be neutral |
| 458 | `mdl264_2l_xefe` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Fuel Expense" will be neutral |
| 459 | `mdl264_2l_xeon` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Expense" will be neutral |
| 460 | `mdl264_2l_yppa` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Prepaid Expenses" will be neutral |
| 461 | `mdl264_2l_yppo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Prepaid Expenses" will be neutral |
| 462 | `mdl264_2l_zahm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Rooms" will be neutral |
| 463 | `mdl264_3l_01dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 10' will move up |
| 464 | `mdl264_3l_1dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing within 1 Year" will be move-up |
| 465 | `mdl264_3l_1nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Treas Shares - Common Stock Prmry Issue" will move up |
| 466 | `mdl264_3l_1ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Shares Outstanding - Preferred Primary Issue' will move up |
| 467 | `mdl264_3l_1ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Products in Phase I" will be move-up |
| 468 | `mdl264_3l_1spdd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'DPS - Common Stock Primary Issue' will move up |
| 469 | `mdl264_3l_1spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Special DPS - Common Stock Primary Issue" will move up |
| 470 | `mdl264_3l_2dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Maturing in Year 2" will be move-up |
| 471 | `mdl264_3l_2lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 2" will be move-up |
| 472 | `mdl264_3l_2nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Treasury Shares - Common Issue 2" will move up |
| 473 | `mdl264_3l_2ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Shares Outstanding - Preferred Issue 2" will be move-up |
| 474 | `mdl264_3l_2ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Products in Phase II" will move up |
| 475 | `mdl264_3l_2spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Dividends per Share - Com Stock Issue 2' will move up |
| 476 | `mdl264_3l_2spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Special DPS - Common Stock Issue 2" will be move-up |
| 477 | `mdl264_3l_32lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in 2-3 Years" will be move-up |
| 478 | `mdl264_3l_3dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 3' will be move-up |
| 479 | `mdl264_3l_3lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 3' will move up |
| 480 | `mdl264_3l_3ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Products in Phase III" will be move-up |
| 481 | `mdl264_3l_3spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Dividends per Share - Com Stock Issue 3' will move up |
| 482 | `mdl264_3l_4lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in Year 4" will be move-up |
| 483 | `mdl264_3l_54dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in 4-5 Years' will move up |
| 484 | `mdl264_3l_54lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Payments Due in 4-5 Years" will be move-up |
| 485 | `mdl264_3l_57_03_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Moving average crossover, 30W-75W" will be move-up |
| 486 | `mdl264_3l_5dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 5' will move up |
| 487 | `mdl264_3l_5lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 5' will move up |
| 488 | `mdl264_3l_63_51_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of the 15W-36W moving average crossover will be move-up |
| 489 | `mdl264_3l_7dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 7' will move up |
| 490 | `mdl264_3l_8dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 8' will move up |
| 491 | `mdl264_3l_abpo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Payable/Accrued' will move up |
| 492 | `mdl264_3l_acda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Current Asset" will move up |
| 493 | `mdl264_3l_acf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Exchange Income (Loss)" will be move-up |
| 494 | `mdl264_3l_acoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets' will move up |
| 495 | `mdl264_3l_adbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized EBITDA' will move up |
| 496 | `mdl264_3l_aemc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Miscellaneous Earnings Adjustment" will be move-up |
| 497 | `mdl264_3l_aiec` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Equity in Affiliates' will move up |
| 498 | `mdl264_3l_alge` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Loss (Gain) on Sale of Assets - Operating" will be move-up |
| 499 | `mdl264_3l_algn` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Gain (Loss) on Sale of Assets" will move up |
| 500 | `mdl264_3l_algv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "(Gain) Loss on Sale of Assets, Suppl." will move up |
| 501 | `mdl264_3l_b6dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long Term Debt Matur. in Year 6 & Beyond" will be move-up |
| 502 | `mdl264_3l_bb` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Bollinger Bands" will be move-up |
| 503 | `mdl264_3l_biis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Income, Bank" will be move-up |
| 504 | `mdl264_3l_bloo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Liabilities" will be move-up |
| 505 | `mdl264_3l_boie` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest on Other Borrowings" will be move-up |
| 506 | `mdl264_3l_bpao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts Payable" will be move-up |
| 507 | `mdl264_3l_btsl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Short Term Borrowings" will be move-up |
| 508 | `mdl264_3l_caic` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Available to Com Excl ExtraOrd" will move up |
| 509 | `mdl264_3l_cbbm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "EBITDAR" will move up |
| 510 | `mdl264_3l_ccns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Change in Cash" will move up |
| 511 | `mdl264_3l_cfda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Charges" will be move-up |
| 512 | `mdl264_3l_cifv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Cost - Foreign" will move up |
| 513 | `mdl264_3l_cinx` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Available to Com Incl ExtraOrd" will move up |
| 514 | `mdl264_3l_cniv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Costs" will be move-up |
| 515 | `mdl264_3l_csfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Service Cost - Foreign' will move up |
| 516 | `mdl264_3l_cspv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Service Cost - Post-Retirement" will be move-up |
| 517 | `mdl264_3l_ctcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Total" will be move-up |
| 518 | `mdl264_3l_ctda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Income Tax - Current Asset" will be move-up |
| 519 | `mdl264_3l_ctdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Deferred Income Tax - Current Liability' will move up |
| 520 | `mdl264_3l_ctdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Total" will be move-up |
| 521 | `mdl264_3l_d0252ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Total return, past 120M" will be move-up |
| 522 | `mdl264_3l_d12ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total return, past 1M" will be move-up |
| 523 | `mdl264_3l_d36ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of 3-month total return will be move-up |
| 524 | `mdl264_3l_dbtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Comp. Store Sales, Retail, Total - %" will move up |
| 525 | `mdl264_3l_dcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Service Cost - Domestic" will move up |
| 526 | `mdl264_3l_dlts` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Debt' will move up |
| 527 | `mdl264_3l_dlyspe_rh` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of historical relative earnings yield will be move-up |
| 528 | `mdl264_3l_drpc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Preferred Dividends" will be move-up |
| 529 | `mdl264_3l_drpf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Issuance (Retirement) of Debt, Net" will move up |
| 530 | `mdl264_3l_dtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Domestic" will move up |
| 531 | `mdl264_3l_dtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Domestic" will be move-up |
| 532 | `mdl264_3l_dtov` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Domestic Tax - Other' will move up |
| 533 | `mdl264_3l_dtsl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Notes Payable/Short Term Debt' will move up |
| 534 | `mdl264_3l_eaca` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Cash & Equivalents" will move up |
| 535 | `mdl264_3l_ebbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Passengers, Total" will move up |
| 536 | `mdl264_3l_ecns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Cash - Ending Balance' will move up |
| 537 | `mdl264_3l_eins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Non-Interest Expense, Bank" will be move-up |
| 538 | `mdl264_3l_eiue` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income)' will move up |
| 539 | `mdl264_3l_eiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Expense" will move up |
| 540 | `mdl264_3l_eiuo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unusual Items" will move up |
| 541 | `mdl264_3l_eiuv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income), Suppl.' will move up |
| 542 | `mdl264_3l_ejtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Value of Bookings" will move up |
| 543 | `mdl264_3l_eoos` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Operating Expenses, Total" will be move-up |
| 544 | `mdl264_3l_eprv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Post-Retirement Plan Expense' will move up |
| 545 | `mdl264_3l_epts` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Expected Return" will be move-up |
| 546 | `mdl264_3l_eptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Pension Expense" will move up |
| 547 | `mdl264_3l_epxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Post-Retirement, Net" will be move-up |
| 548 | `mdl264_3l_erpm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Products in Pre-Registration" will move up |
| 549 | `mdl264_3l_etoq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Equity" will move up |
| 550 | `mdl264_3l_fmc` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Chaikin Money Flow" will be move-up |
| 551 | `mdl264_3l_fotv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "All Other Fees" will be move-up |
| 552 | `mdl264_3l_ftcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Foreign" will move up |
| 553 | `mdl264_3l_ftdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Deferred Tax - Foreign' will move up |
| 554 | `mdl264_3l_fttv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Tax Fees' will move up |
| 555 | `mdl264_3l_gaxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Actuarial Gains and Losses - Domestic" will be move-up |
| 556 | `mdl264_3l_gdbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Available Seat Kilometers (ASK)" will be move-up |
| 557 | `mdl264_3l_ghc_qe_td_tl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "YoY change in long-term debt/common equity" will be move-up |
| 558 | `mdl264_3l_gjbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Expense per ASK" will move up |
| 559 | `mdl264_3l_htrm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Rent Growth (Sequential), Total -%" will move up |
| 560 | `mdl264_3l_iabs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Basic EPS Including Extraordinary Items" will move up |
| 561 | `mdl264_3l_iads` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Diluted EPS Including Extraordinary Items" will move up |
| 562 | `mdl264_3l_icc` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Commodity Channel Index" will be move-up |
| 563 | `mdl264_3l_ifm` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Money Flow Index will be move-up |
| 564 | `mdl264_3l_iins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Maturity of Investment" will move up |
| 565 | `mdl264_3l_iirr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Reinsurance - Income' will move up |
| 566 | `mdl264_3l_iiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Unusual Income" will move up |
| 567 | `mdl264_3l_im` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Mass Index will be move-up |
| 568 | `mdl264_3l_inds` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Diluted Net Income" will move up |
| 569 | `mdl264_3l_ips` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of Special Items will be move-up |
| 570 | `mdl264_3l_ipts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Interest Cost" will move up |
| 571 | `mdl264_3l_iscs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Cash and Short-Term Investments' will be move-up |
| 572 | `mdl264_3l_isir` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest & Dividends on Investment Secs." will be move-up |
| 573 | `mdl264_3l_ist` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of True Strength Index will be move-up |
| 574 | `mdl264_3l_ists` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Special Items" will be move-up |
| 575 | `mdl264_3l_itpv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized Income Before Taxes" will move up |
| 576 | `mdl264_3l_iv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Vortex Indicator will be move-up |
| 577 | `mdl264_3l_ivn` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of the Negative Volume Index will be move-up |
| 578 | `mdl264_3l_ixts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Extraordinary Items" will be move-up |
| 579 | `mdl264_3l_kcqs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Quick Ratio' will move up |
| 580 | `mdl264_3l_khtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Stores Opened" will be move-up |
| 581 | `mdl264_3l_laoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Assets & Liabilities, Net' will move up |
| 582 | `mdl264_3l_lbtm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Merchandise Margins, Total -%" will be move-up |
| 583 | `mdl264_3l_lcdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Curr Liability" will be move-up |
| 584 | `mdl264_3l_lctv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Capital Leases, Supplemental" will move up |
| 585 | `mdl264_3l_lda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Accumulation Distribution Line will be move-up |
| 586 | `mdl264_3l_ldav` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Revenue - Long Term" will be move-up |
| 587 | `mdl264_3l_ldbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Load Factor, Total -%" will move up |
| 588 | `mdl264_3l_lgrr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Realized & Unrealized Gains (Losses)" will move up |
| 589 | `mdl264_3l_lgsn` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Investment Securities Gains" will be move-up |
| 590 | `mdl264_3l_lguq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unrealized Gain (Loss)" will be move-up |
| 591 | `mdl264_3l_lppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Products Launched" will be move-up |
| 592 | `mdl264_3l_ltcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Local" will be move-up |
| 593 | `mdl264_3l_ltdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Local" will move up |
| 594 | `mdl264_3l_ltio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Inventories' will move up |
| 595 | `mdl264_3l_ltll` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Liabilities" will move up |
| 596 | `mdl264_3l_m1d_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 BPS diffusion (up/down ratio), 1M will be move-up |
| 597 | `mdl264_3l_m1d_1yf_spd_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 DPS diffusion (up/down ratio), 1M" will be move-up |
| 598 | `mdl264_3l_m1d_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 EPS diffusion (up/down ratio), 1M will be move-up |
| 599 | `mdl264_3l_m1d_1yf_spfc_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 CFPS diffusion (up/down ratio), 1M will be move-up |
| 600 | `mdl264_3l_m1d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV diffusion (up/down ratio), 1M will be move-up |
| 601 | `mdl264_3l_m1d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of Recommendation diffusion (up/down ratio), 1M will be move-up |
| 602 | `mdl264_3l_m1d_gtl_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Long-term growth diffusion (up/down ratio), 1M" will be move-up |
| 603 | `mdl264_3l_m1d_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Target price diffusion (up/down ratio), 1M" will be move-up |
| 604 | `mdl264_3l_m1m21_ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Price momentum, 12M-1M will be move-up |
| 605 | `mdl264_3l_m1r_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 BPS revision, 1M" will be move-up |
| 606 | `mdl264_3l_m1r_1yf_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 DPS revision, 1M will be move-up |
| 607 | `mdl264_3l_m1r_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of "FY1 EPS revision, 1M" will be move-up |
| 608 | `mdl264_3l_m1r_1yf_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 CFPS revision, 1M will be move-up |
| 609 | `mdl264_3l_m1r_1yf_van_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV revision, 1M will be move-up |
| 610 | `mdl264_3l_m1r_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Recommendation revision, 1M" will be move-up |
| 611 | `mdl264_3l_m1r_gtl_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Long-term growth revision, 1M" will be move-up |
| 612 | `mdl264_3l_m1r_mtn_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM DPS revision over 1 month will be move-up |
| 613 | `mdl264_3l_m1r_mtn_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "NTM EPS revision, 1M" will be move-up |
| 614 | `mdl264_3l_m1r_mtn_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM CFPS revision, 1M will be move-up |
| 615 | `mdl264_3l_m1r_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Target price revision, 1M" will be move-up |
| 616 | `mdl264_3l_m3d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 NAV diffusion (up/down ratio) over 3 months will be move-up |
| 617 | `mdl264_3l_m3d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation diffusion (up/down ratio), 3M will be move-up |
| 618 | `mdl264_3l_m3r_mtn_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM BPS revision over 3 months will be move-up |
| 619 | `mdl264_3l_mocq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Comprehensive Income" will be move-up |
| 620 | `mdl264_3l_mpns` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Profit Margin" will move up |
| 621 | `mdl264_3l_mtps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Pretax Margin' will move up |
| 622 | `mdl264_3l_ndsf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Short Term Debt, Net" will be move-up |
| 623 | `mdl264_3l_niis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest/Invest Income - Non-Operating" will move up |
| 624 | `mdl264_3l_nins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Inc. (Exp.), Net-Non-Op., Total" will be move-up |
| 625 | `mdl264_3l_nscf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Common Stock, Net" will move up |
| 626 | `mdl264_3l_ntiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inc Tax Ex Impact of Sp Items" will be move-up |
| 627 | `mdl264_3l_nvii` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Investment, Net' will move up |
| 628 | `mdl264_3l_oc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Chaikin Oscillator" will be move-up |
| 629 | `mdl264_3l_ocl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of Current Liabilities Other Total will be move-up |
| 630 | `mdl264_3l_od` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Discontinued Operations will be a move-up |
| 631 | `mdl264_3l_oiis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest/Investment Income - Operating" will be move-up |
| 632 | `mdl264_3l_oinm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Interest Margin, Total -%" will be move-up |
| 633 | `mdl264_3l_olcl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Capital Lease Obligations" will be move-up |
| 634 | `mdl264_3l_ompd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of DecisionPoint Price Momentum Oscillator will be move-up |
| 635 | `mdl264_3l_opd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Detrended Price Oscillator will be move-up |
| 636 | `mdl264_3l_opp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of percentage price oscillator will be move-up |
| 637 | `mdl264_3l_optq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Preferred Shares Outstanding' will move up |
| 638 | `mdl264_3l_opxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Pension, Net - Domestic' will move up |
| 639 | `mdl264_3l_os` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of the Stochastic Oscillator will be move-up |
| 640 | `mdl264_3l_otcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Other" will move up |
| 641 | `mdl264_3l_otdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Other" will be move-up |
| 642 | `mdl264_3l_ovp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Percentage Volume Oscillator" will be move-up |
| 643 | `mdl264_3l_pcrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Repurch./Retirement of Common/Preferred" will move up |
| 644 | `mdl264_3l_pcsf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Common/Preferred" will be move-up |
| 645 | `mdl264_3l_pcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Stock-Based Compensation, Supplemental" will move up |
| 646 | `mdl264_3l_pffl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FedFundsPurch/ScrtySoldUnderRepurchAgrmt" will be move-up |
| 647 | `mdl264_3l_poer` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Electric Operations" will be move-up |
| 648 | `mdl264_3l_ppdf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Cash Dividends Paid - Preferred' will move up |
| 649 | `mdl264_3l_ppdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Domestic Pension Plan Expense" will move up |
| 650 | `mdl264_3l_ppfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Pension Plan Expense" will move up |
| 651 | `mdl264_3l_ppgs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Gross Margin" will move up |
| 652 | `mdl264_3l_prrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Repurchase/Retirement of Preferred' will move up |
| 653 | `mdl264_3l_pxtl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Taxes Payable" will move up |
| 654 | `mdl264_3l_qbbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Revenue Passenger Kilometers (RPK)" will be move-up |
| 655 | `mdl264_3l_rcao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts Receivable" will move up |
| 656 | `mdl264_3l_rinr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Non-Insurance Revenue" will be move-up |
| 657 | `mdl264_3l_rltr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Revenue" will be move-up |
| 658 | `mdl264_3l_rpts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Other Expense" will move up |
| 659 | `mdl264_3l_rpul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Unearned Premium/Unearned Revenue' will move up |
| 660 | `mdl264_3l_rta` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Average True Range will be move-up |
| 661 | `mdl264_3l_rtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Tax - Total" will move up |
| 662 | `mdl264_3l_rtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Tax - Total" will be move-up |
| 663 | `mdl264_3l_rw` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Williams %R" will be move-up |
| 664 | `mdl264_3l_rxfv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Expected Return on Assets - Foreign' will move up |
| 665 | `mdl264_3l_saie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Sale" will be move-up |
| 666 | `mdl264_3l_saoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Assets" will be move-up |
| 667 | `mdl264_3l_sern` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge' will move up |
| 668 | `mdl264_3l_serv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Restructuring Charge, Supplemental" will move up |
| 669 | `mdl264_3l_spe_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Historical 5Y EPS growth trend will be move-up |
| 670 | `mdl264_3l_speo_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Historical 5Y operating EPS growth trend" will be move-up |
| 671 | `mdl264_3l_spfc_rtnie_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of YoY expected interim CFPS growth will be move-up |
| 672 | `mdl264_3l_spfc_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of Historical 5Y CFPS growth trend will be move-up |
| 673 | `mdl264_3l_spts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Plan Service Cost" will be move-up |
| 674 | `mdl264_3l_sptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Prior Service Cost - Domestic" will move up |
| 675 | `mdl264_3l_sspf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Issuance (Retirement) of Stock, Net" will move up |
| 676 | `mdl264_3l_stnr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Sales' will move up |
| 677 | `mdl264_3l_tait` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Net Income After Taxes" will move up |
| 678 | `mdl264_3l_tbie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Income Before Taxes' will move up |
| 679 | `mdl264_3l_tcxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Curtailments & Settlements - Domestic" will move up |
| 680 | `mdl264_3l_tdbo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Deferred Taxes" will move up |
| 681 | `mdl264_3l_tdtv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Domestic Tax" will move up |
| 682 | `mdl264_3l_tftv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Tax" will move up |
| 683 | `mdl264_3l_toia` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Inventories - Other" will be move-up |
| 684 | `mdl264_3l_tpda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest-Earning Deposits" will move up |
| 685 | `mdl264_3l_tpv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Volume Price Trend will be move-up |
| 686 | `mdl264_3l_ttiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Tax - Total" will move up |
| 687 | `mdl264_3l_uaie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Impairment-Assets Held for Use' will move up |
| 688 | `mdl264_3l_vbo` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of On Balance Volume will be move-up |
| 689 | `mdl264_3l_vcwf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Warrants Converted" will move up |
| 690 | `mdl264_3l_vdav` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Advertising Expense, Supplemental' will move up |
| 691 | `mdl264_3l_vlc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Close Location Value" will be move-up |
| 692 | `mdl264_3l_vme` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Ease of Movement will be move-up |
| 693 | `mdl264_3l_vnie` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Investment Income - Operating" will move up |
| 694 | `mdl264_3l_xeao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accrued Expenses" will move up |
| 695 | `mdl264_3l_xefe` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Fuel Expense' will move up |
| 696 | `mdl264_3l_xeon` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Expense' will move up |
| 697 | `mdl264_3l_yppa` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Prepaid Expenses" will be move-up |
| 698 | `mdl264_3l_yppo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prepaid Expenses' will move up |
| 699 | `mdl264_3l_zahm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Rooms" will move up |
| 700 | `mdl264_abn_volm_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Modal class of the predicted trend for Abnormal volume (1=fall, 2=neutral, 3=move-up) |
| 701 | `mdl264_abn_volm_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Abnormal volume will be fall |
| 702 | `mdl264_abn_volm_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Abnormal volume will be neutral |
| 703 | `mdl264_abn_volm_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Abnormal volume will be move-up |
| 704 | `mdl264_acae_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Cash & Equivalents" (1: fall, 2: neutral, 3: move-up) |
| 705 | `mdl264_adca_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Discontinued Operations - Current Asset" (1: fall, 2: neutral, 3: move-up) |
| 706 | `mdl264_adfc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Charges" (1: fall, 2: neutral, 3: move up) |
| 707 | `mdl264_adl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of Accumulation Distribution Line |
| 708 | `mdl264_adoa_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Discontinued Operations - LT Asset' (1: fall, 2: neutral, 3: move up) |
| 709 | `mdl264_adoa_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - LT Asset" will fall |
| 710 | `mdl264_adoa_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - LT Asset" will be neutral |
| 711 | `mdl264_adoa_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - LT Asset" will move up |
| 712 | `mdl264_adpt_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest-Earning Deposits" (1: fall, 2: neutral, 3: move-up) |
| 713 | `mdl264_adtc_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Income Tax - Current Asset" (1: fall, 2: neutral, 3: move up) |
| 714 | `mdl264_aiot_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Inventories - Other" (1: fall, 2: neutral, 3: move up) |
| 715 | `mdl264_amihud_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Modal class of the predicted trend for Amihud illiquidity (1=fall, 2=neutral, 3=move-up) |
| 716 | `mdl264_amihud_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Amihud illiquidity will be fall |
| 717 | `mdl264_amihud_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Amihud illiquidity will be neutral |
| 718 | `mdl264_amihud_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of Amihud illiquidity will be move-up |
| 719 | `mdl264_aoca_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Current Assets" (1: fall, 2: neutral, 3: move-up) |
| 720 | `mdl264_aorc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Receivables - Other' (1: fall, 2: neutral, 3: move up) |
| 721 | `mdl264_aorc_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Receivables - Other" will fall |
| 722 | `mdl264_aorc_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Receivables - Other" will be neutral |
| 723 | `mdl264_aorc_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Receivables - Other' will move up |
| 724 | `mdl264_appy_class` | MATRIX | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Predicted trend of "Prepaid Expenses" (1: fall, 2: neutral, 3: move up) |
| 725 | `mdl264_asti_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Short Term Investments" (1: fall, 2: neutral, 3: move-up) |
| 726 | `mdl264_asti_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Short Term Investments' will fall |
| 727 | `mdl264_asti_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Short Term Investments" will be neutral |
| 728 | `mdl264_atr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of Average True Range |
| 729 | `mdl264_bb_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Bollinger Bands" (1: fall, 2: neutral, 3: move-up) |
| 730 | `mdl264_bookp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class for "Book-to-market" where 1=fall, 2=neutral, 3=move-up |
| 731 | `mdl264_bookp_fy1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Book-to-market, FY1" (1: fall, 2: neutral, 3: move-up) |
| 732 | `mdl264_bookp_fy1_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Book-to-market, FY1" will be fall |
| 733 | `mdl264_bookp_fy1_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Book-to-market, FY1" will be neutral |
| 734 | `mdl264_bookp_fy1_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Book-to-market, FY1" will be move-up |
| 735 | `mdl264_bookp_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Book-to-market" will be fall |
| 736 | `mdl264_bookp_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Book-to-market" will be neutral |
| 737 | `mdl264_bookp_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Book-to-market" will be move-up |
| 738 | `mdl264_cci_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of "Commodity Channel Index" (1: fall, 2: neutral, 3: move-up) |
| 739 | `mdl264_ceia_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Equity In Affiliates' (1: fall, 2: neutral, 3: move-up) |
| 740 | `mdl264_ciac_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Income Available to Com Excl ExtraOrd" (1: fall, 2: neutral, 3: move-up) |
| 741 | `mdl264_clv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1=fall, 2=neutral, 3=move-up) for Close Location Value |
| 742 | `mdl264_cmea_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Miscellaneous Earnings Adjustment' (1: fall, 2: neutral, 3: move up) |
| 743 | `mdl264_cmf_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of "Chaikin Money Flow" (1: fall, 2: neutral, 3: move-up) |
| 744 | `mdl264_cmin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Minority Interest" (1: fall, 2: neutral, 3: move up) |
| 745 | `mdl264_cmin_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Minority Interest' will fall |
| 746 | `mdl264_cmin_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Minority Interest" will be neutral |
| 747 | `mdl264_cmin_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Minority Interest" will move up |
| 748 | `mdl264_co_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Chaikin Oscillator" (1: fall, 2: neutral, 3: move-up) |
| 749 | `mdl264_compustat_a2_xgb_dl8_d1_xido_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Extraordinary Items and Discontinued Operations" (1: fall, 2: neutral, 3: move-up) |
| 750 | `mdl264_compustat_a2_xgb_dl8_d1_xido_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Extraordinary Items and Discontinued Operations" will be fall |
| 751 | `mdl264_compustat_a2_xgb_dl8_d1_xido_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Extraordinary Items and Discontinued Operations" will be neutral |
| 752 | `mdl264_compustat_a2_xgb_dl8_d1_xido_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Extraordinary Items and Discontinued Operations" will be move-up |
| 753 | `mdl264_cprd_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Preferred Dividends" (1: fall, 2: neutral, 3: move-up) |
| 754 | `mdl264_ddps1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "DPS - Common Stock Primary Issue" (1: fall, 2: neutral, 3: move-up) |
| 755 | `mdl264_ddps2_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Dividends per Share - Com Stock Issue 2" (1: fall, 2: neutral, 3: move up) |
| 756 | `mdl264_ddps3_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Dividends per Share - Com Stock Issue 3" (1: fall, 2: neutral, 3: move-up) |
| 757 | `mdl264_div_payout_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend class for "Dividend payout ratio, trailing" where 1=fall, 2=neutral, 3=move-up |
| 758 | `mdl264_div_payout_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Dividend payout ratio, trailing" will be fall |
| 759 | `mdl264_div_payout_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Dividend payout ratio, trailing" will be neutral |
| 760 | `mdl264_div_payout_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Dividend payout ratio, trailing" will be move-up |
| 761 | `mdl264_divyld_bb_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend class for Total yield (dividend + share change): 1 fall, 2 neutral, 3 move-up |
| 762 | `mdl264_divyld_bb_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of Total yield (dividend + share change) will be fall |
| 763 | `mdl264_divyld_bb_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total yield (dividend + share change)" will be neutral |
| 764 | `mdl264_divyld_bb_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total yield (dividend + share change)" will be move-up |
| 765 | `mdl264_do_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Discontinued Operations" (1: fall, 2: neutral, 3: move-up) |
| 766 | `mdl264_dpmo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class for DecisionPoint Price Momentum Oscillator: 1 fall, 2 neutral, 3 move-up |
| 767 | `mdl264_dpo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Detrended Price Oscillator (1: fall, 2: neutral, 3: move-up) |
| 768 | `mdl264_dsps1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Special DPS - Common Stock Primary Issue' (1: fall, 2: neutral, 3: move-up) |
| 769 | `mdl264_dsps2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Special DPS - Common Stock Issue 2" (1: fall, 2: neutral, 3: move-up) |
| 770 | `mdl264_eama_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Amortization of Acquisition Costs" (1: fall, 2: neutral, 3: move up) |
| 771 | `mdl264_eama_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization of Acquisition Costs" will fall |
| 772 | `mdl264_eama_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization of Acquisition Costs" will be neutral |
| 773 | `mdl264_eama_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization of Acquisition Costs" will move up |
| 774 | `mdl264_efex_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Fuel Expense" (1: fall, 2: neutral, 3: move-up) |
| 775 | `mdl264_egla_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Loss (Gain) on Sale of Assets - Operating' (1: fall, 2: neutral, 3: move-up) |
| 776 | `mdl264_eias_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Impairment-Assets Held for Sale' (1: fall, 2: neutral, 3: move up) |
| 777 | `mdl264_eiau_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Impairment-Assets Held for Use" (1: fall, 2: neutral, 3: move up) |
| 778 | `mdl264_eibt_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Net Income Before Taxes" (1: fall, 2: neutral, 3: move-up) |
| 779 | `mdl264_einv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Investment Income - Operating" (1: fall, 2: neutral, 3: move up) |
| 780 | `mdl264_eiob_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of 'Interest on Other Borrowings' (1: fall, 2: neutral, 3: move up) |
| 781 | `mdl264_elit_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Litigation" (1: fall, 2: neutral, 3: move up) |
| 782 | `mdl264_elit_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Litigation' will fall |
| 783 | `mdl264_elit_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Litigation" will be neutral |
| 784 | `mdl264_elit_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Litigation' will move up |
| 785 | `mdl264_ellp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Loan Loss Provision" (1: fall, 2: neutral, 3: move-up) |
| 786 | `mdl264_ellp_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Loan Loss Provision' will fall |
| 787 | `mdl264_ellp_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Loan Loss Provision" will be neutral |
| 788 | `mdl264_ellp_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Loan Loss Provision' will move up |
| 789 | `mdl264_emv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Ease of Movement (1: fall, 2: neutral, 3: move-up) |
| 790 | `mdl264_eont_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other, Net" (1: fall, 2: neutral, 3: move up) |
| 791 | `mdl264_eont_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other, Net" will be fall |
| 792 | `mdl264_eont_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other, Net" will be neutral |
| 793 | `mdl264_eont_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other, Net" will move up |
| 794 | `mdl264_eps_disp_class` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Predicted trend class for FY1 EPS dispersion coded as 1 fall 2 neutral 3 move-up |
| 795 | `mdl264_eps_disp_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EPS dispersion will be fall |
| 796 | `mdl264_eps_disp_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EPS dispersion will be neutral |
| 797 | `mdl264_eps_disp_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EPS dispersion will be move-up |
| 798 | `mdl264_eps_sur_decay_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) for predicted trend of EPS Surprise with Decay |
| 799 | `mdl264_eps_sur_decay_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of EPS Surprise with Decay will be fall |
| 800 | `mdl264_eps_sur_decay_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of EPS Surprise with Decay will be neutral |
| 801 | `mdl264_eps_sur_decay_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of EPS Surprise with Decay will be move-up |
| 802 | `mdl264_eres_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Restructuring Charge" (1: fall, 2: neutral, 3: move-up) |
| 803 | `mdl264_eres_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge' will fall |
| 804 | `mdl264_eres_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Restructuring Charge" will be neutral |
| 805 | `mdl264_eres_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Restructuring Charge" will be move-up |
| 806 | `mdl264_es_bps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1=fall, 2=neutral, 3=move-up) for FY1 BPS diffusion (up/down ratio), 1M |
| 807 | `mdl264_es_bps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) of the predicted trend for FY1 BPS revision over 1 month |
| 808 | `mdl264_es_bps_ntm_r3m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) of the predicted trend for NTM BPS revision over 3 months |
| 809 | `mdl264_es_cfps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class for FY1 CFPS diffusion (up/down ratio), 1M: 1 fall, 2 neutral, 3 move-up |
| 810 | `mdl264_es_cfps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of FY1 CFPS revision, 1M |
| 811 | `mdl264_es_cfps_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted modal trend class for NTM CFPS revision, 1M (1=fall, 2=neutral, 3=move-up) |
| 812 | `mdl264_es_dps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "FY1 DPS diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up) |
| 813 | `mdl264_es_dps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 DPS revision, 1M: 1=fall, 2=neutral, 3=move-up |
| 814 | `mdl264_es_dps_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) of the predicted trend for NTM DPS revision over 1 month |
| 815 | `mdl264_es_ebit_fy1_d1m_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 EBIT diffusion (up/down ratio), 1M (1: fall, 2: neutral, 3: move-up) |
| 816 | `mdl264_es_ebit_fy1_d1m_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBIT diffusion (up/down ratio), 1M will be fall |
| 817 | `mdl264_es_ebit_fy1_d1m_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 EBIT diffusion (up/down ratio), 1M" will be neutral |
| 818 | `mdl264_es_ebit_fy1_d1m_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 EBIT diffusion (up/down ratio), 1M" will be move-up |
| 819 | `mdl264_es_ebit_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class (1=fall, 2=neutral, 3=move-up) for FY1 EBIT revision, 1M |
| 820 | `mdl264_es_ebit_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 EBIT revision, 1M will be fall |
| 821 | `mdl264_es_ebit_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 EBIT revision, 1M will be neutral |
| 822 | `mdl264_es_ebit_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of FY1 EBIT revision, 1M will be move-up |
| 823 | `mdl264_es_ebit_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted modal trend class for NTM EBIT revision, 1M (1=fall, 2=neutral, 3=move-up) |
| 824 | `mdl264_es_ebit_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EBIT revision, 1M will be fall |
| 825 | `mdl264_es_ebit_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EBIT revision, 1M will be neutral |
| 826 | `mdl264_es_ebit_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EBIT revision, 1M will be move-up |
| 827 | `mdl264_es_ebitda_fy1_d1m_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) for predicted trend of FY1 EBITDA diffusion (up/down ratio), 1M |
| 828 | `mdl264_es_ebitda_fy1_d1m_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EBITDA diffusion (up/down ratio), 1M will be fall |
| 829 | `mdl264_es_ebitda_fy1_d1m_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EBITDA diffusion (up/down ratio), 1M will be neutral |
| 830 | `mdl264_es_ebitda_fy1_d1m_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EBITDA diffusion (up/down ratio), 1M will be move-up |
| 831 | `mdl264_es_ebitda_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of FY1 EBITDA revision, 1M |
| 832 | `mdl264_es_ebitda_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EBITDA revision, 1M will be fall |
| 833 | `mdl264_es_ebitda_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EBITDA revision, 1M will be neutral |
| 834 | `mdl264_es_ebitda_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 EBITDA revision, 1M will be move-up |
| 835 | `mdl264_es_ebitda_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class for NTM EBITDA revision, 1M: 1 fall, 2 neutral, 3 move-up |
| 836 | `mdl264_es_ebitda_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM EBITDA revision, 1M will be fall |
| 837 | `mdl264_es_ebitda_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM EBITDA revision, 1M will be neutral |
| 838 | `mdl264_es_ebitda_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of NTM EBITDA revision, 1M will be move-up |
| 839 | `mdl264_es_eps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1=fall, 2=neutral, 3=move-up) for FY1 EPS diffusion (up/down ratio), 1M |
| 840 | `mdl264_es_eps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class for "FY1 EPS revision, 1M" where 1=fall, 2=neutral, 3=move-up |
| 841 | `mdl264_es_eps_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of "NTM EPS revision, 1M" (1: fall, 2: neutral, 3: move-up) |
| 842 | `mdl264_es_ltg_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Long-term growth diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up) |
| 843 | `mdl264_es_ltg_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class for long-term growth revision, 1M (1=fall, 2=neutral, 3=move-up) |
| 844 | `mdl264_es_nav_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 NAV diffusion (up/down ratio), 1M: 1=fall, 2=neutral, 3=move-up |
| 845 | `mdl264_es_nav_fy1_d3m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) of the predicted trend for FY1 NAV diffusion (up/down ratio) over 3 months |
| 846 | `mdl264_es_nav_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class for FY1 NAV revision, 1M (1=fall, 2=neutral, 3=move-up) |
| 847 | `mdl264_es_rec_d1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class for Recommendation diffusion (up/down ratio), 1M (1=fall, 2=neutral, 3=move-up) |
| 848 | `mdl264_es_rec_d3m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of Recommendation diffusion (up/down ratio), 3M (1: fall, 2: neutral, 3: move-up) |
| 849 | `mdl264_es_rec_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend class for "Recommendation revision, 1M" where 1=fall, 2=neutral, 3=move-up |
| 850 | `mdl264_es_roe_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "FY1 ROE diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up) |
| 851 | `mdl264_es_roe_fy1_d1m_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 ROE diffusion (up/down ratio), 1M" will be fall |
| 852 | `mdl264_es_roe_fy1_d1m_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 ROE diffusion (up/down ratio), 1M" will be neutral |
| 853 | `mdl264_es_roe_fy1_d1m_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 ROE diffusion (up/down ratio), 1M" will be move-up |
| 854 | `mdl264_es_roe_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) of the predicted trend for FY1 ROE revision over 1 month |
| 855 | `mdl264_es_roe_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 ROE revision over 1 month will be fall |
| 856 | `mdl264_es_roe_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 ROE revision over 1 month will be neutral |
| 857 | `mdl264_es_roe_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Probability that the future trend of FY1 ROE revision over 1 month will be move-up |
| 858 | `mdl264_es_roe_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM ROE revision, 1M (1: fall, 2: neutral, 3: move-up) |
| 859 | `mdl264_es_roe_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM ROE revision, 1M will be fall |
| 860 | `mdl264_es_roe_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM ROE revision, 1M will be neutral |
| 861 | `mdl264_es_roe_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM ROE revision, 1M will be move-up |
| 862 | `mdl264_es_sale_fy1_d1m_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted modal trend class for FY1 revenue diffusion (up/down ratio), 1M (1=fall, 2=neutral, 3=move-up) |
| 863 | `mdl264_es_sale_fy1_d1m_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 revenue diffusion (up/down ratio), 1M will be fall |
| 864 | `mdl264_es_sale_fy1_d1m_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 revenue diffusion (up/down ratio), 1M will be neutral |
| 865 | `mdl264_es_sale_fy1_d1m_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 revenue diffusion (up/down ratio), 1M will be move-up |
| 866 | `mdl264_es_sale_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of "FY1 revenue revision, 1M" (1: fall, 2: neutral, 3: move-up) |
| 867 | `mdl264_es_sale_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 revenue revision, 1M" will be fall |
| 868 | `mdl264_es_sale_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 revenue revision, 1M" will be neutral |
| 869 | `mdl264_es_sale_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "FY1 revenue revision, 1M" will be move-up |
| 870 | `mdl264_es_sale_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of "NTM revenue revision, 1M" (1: fall, 2: neutral, 3: move-up) |
| 871 | `mdl264_es_sale_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "NTM revenue revision, 1M" will be fall |
| 872 | `mdl264_es_sale_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "NTM revenue revision, 1M" will be neutral |
| 873 | `mdl264_es_sale_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "NTM revenue revision, 1M" will be move-up |
| 874 | `mdl264_es_tp_d1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of "Target price diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up) |
| 875 | `mdl264_es_tp_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of "Target price revision, 1M" (1: fall, 2: neutral, 3: move-up) |
| 876 | `mdl264_es_vol_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of "Analyst estimated vol revision, 1M" (1: fall, 2: neutral, 3: move-up) |
| 877 | `mdl264_es_vol_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Analyst estimated vol revision, 1M" will be fall |
| 878 | `mdl264_es_vol_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Analyst estimated vol revision, 1M" will be neutral |
| 879 | `mdl264_es_vol_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Analyst estimated vol revision, 1M" will be move-up |
| 880 | `mdl264_euie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Unusual Expense (Income)" (1: fall, 2: neutral, 3: move-up) |
| 881 | `mdl264_ext_fin_noa_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend class for net external financing over net operating assets coded as 1 fall 2 neutral 3 move-up |
| 882 | `mdl264_ext_fin_noa_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of net external financing over net operating assets will be fall |
| 883 | `mdl264_ext_fin_noa_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of net external financing over net operating assets will be neutral |
| 884 | `mdl264_ext_fin_noa_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of net external financing over net operating assets will be move-up |
| 885 | `mdl264_fca_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) for the predicted future trend of Foreign Exchange Income (Loss) |
| 886 | `mdl264_fcsn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Common Stock, Net" (1: fall, 2: neutral, 3: move-up) |
| 887 | `mdl264_fdpp_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Cash Dividends Paid - Preferred" (1: fall, 2: neutral, 3: move-up) |
| 888 | `mdl264_fincf_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) for the predicted future trend of Financing Activities Net Cash Flow |
| 889 | `mdl264_fincf_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Probability that the future trend of Financing Activities Net Cash Flow will be a fall |
| 890 | `mdl264_fincf_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Financing Activities Net Cash Flow" will be neutral |
| 891 | `mdl264_fincf_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Financing Activities Net Cash Flow" will be move-up |
| 892 | `mdl264_float_to_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of "Float turnover, 12M" (1: fall, 2: neutral, 3: move-up) |
| 893 | `mdl264_float_to_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Float turnover, 12M" will be fall |
| 894 | `mdl264_float_to_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Float turnover, 12M" will be neutral |
| 895 | `mdl264_float_to_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Float turnover, 12M" will be move-up |
| 896 | `mdl264_fprd_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Issuance (Retirement) of Debt, Net" (1: fall, 2: neutral, 3: move-up) |
| 897 | `mdl264_fpss_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Issuance (Retirement) of Stock, Net' (1: fall, 2: neutral, 3: move up) |
| 898 | `mdl264_frcp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Repurch./Retirement of Common/Preferred" (1: fall, 2: neutral, 3: move-up) |
| 899 | `mdl264_frrp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Repurchase/Retirement of Preferred" (1: fall, 2: neutral, 3: move-up) |
| 900 | `mdl264_fscp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Sale/Issuance of Common/Preferred" (1: fall, 2: neutral, 3: move-up) |
| 901 | `mdl264_fsdn_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Short Term Debt, Net' (1: fall, 2: neutral, 3: move-up) |
| 902 | `mdl264_fsic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Sale/Issuance of Common" (1: fall, 2: neutral, 3: move up) |
| 903 | `mdl264_fsic_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Common" will fall |
| 904 | `mdl264_fsic_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Common" will be neutral |
| 905 | `mdl264_fsic_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Common" will be move-up |
| 906 | `mdl264_fsip_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Sale/Issuance of Preferred' (1: fall, 2: neutral, 3: move up) |
| 907 | `mdl264_fsip_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Preferred" will be fall |
| 908 | `mdl264_fsip_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Preferred" will be neutral |
| 909 | `mdl264_fsip_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale/Issuance of Preferred" will move up |
| 910 | `mdl264_fwcv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Warrants Converted" (1: fall, 2: neutral, 3: move-up) |
| 911 | `mdl264_gr_5y_cfps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class for Historical 5Y CFPS growth trend (1=fall, 2=neutral, 3=move-up) |
| 912 | `mdl264_gr_5y_eps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of Historical 5Y EPS growth trend |
| 913 | `mdl264_gr_5y_oeps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Historical 5Y operating EPS growth trend" (1: fall, 2: neutral, 3: move-up) |
| 914 | `mdl264_gr_eintr_cfps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class for YoY expected interim CFPS growth (1=fall, 2=neutral, 3=move-up) |
| 915 | `mdl264_hilomid_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1=fall, 2=neutral, 3=move-up) for the High Low Mid Point factor |
| 916 | `mdl264_hilomid_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of High Low Mid Point will be fall |
| 917 | `mdl264_hilomid_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of High Low Mid Point will be neutral |
| 918 | `mdl264_hilomid_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Model-estimated probability that the future trend of High Low Mid Point will be move-up |
| 919 | `mdl264_hr_epsyld_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend class for historical relative earnings yield coded as 1 fall 2 neutral 3 move-up |
| 920 | `mdl264_ibaq_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Acquisition of Business" (1: fall, 2: neutral, 3: move-up) |
| 921 | `mdl264_ibaq_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Acquisition of Business" will be fall |
| 922 | `mdl264_ibaq_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Acquisition of Business" will be neutral |
| 923 | `mdl264_ibaq_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Acquisition of Business" will be move-up |
| 924 | `mdl264_iivn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Investment, Net" (1: fall, 2: neutral, 3: move-up) |
| 925 | `mdl264_isoi_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Sale of Intangible Assets" (1: fall, 2: neutral, 3: move-up) |
| 926 | `mdl264_isoi_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale of Intangible Assets" will fall |
| 927 | `mdl264_isoi_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale of Intangible Assets" will be neutral |
| 928 | `mdl264_isoi_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Sale of Intangible Assets" will move up |
| 929 | `mdl264_lclo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Capital Lease Obligations" (1: fall, 2: neutral, 3: move-up) |
| 930 | `mdl264_lco_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend class for Current Liabilities Other Total; 1=fall, 2=neutral, 3=move-up (modal class from the L1–L3 probabilities) |
| 931 | `mdl264_ldcl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Discontinued Operations - Curr Liability" (1: fall, 2: neutral, 3: move up) |
| 932 | `mdl264_ldol_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Discontinued Operations - Liabilities" (1: fall, 2: neutral, 3: move-up) |
| 933 | `mdl264_ldol_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Liabilities" will be fall |
| 934 | `mdl264_ldol_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Liabilities" will be neutral |
| 935 | `mdl264_ldol_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations - Liabilities" will be move-up |
| 936 | `mdl264_ldtc_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Income Tax - Current Liability" (1: fall, 2: neutral, 3: move-up) |
| 937 | `mdl264_lffp_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of "FedFundsPurch/ScrtySoldUnderRepurchAgrmt" (1: fall, 2: neutral, 3: move-up) |
| 938 | `mdl264_lltl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Long Term Liabilities' (1: fall, 2: neutral, 3: move up) |
| 939 | `mdl264_lobl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Bearing Liabilities' (1: fall, 2: neutral, 3: move up) |
| 940 | `mdl264_lobl_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Bearing Liabilities" will be fall |
| 941 | `mdl264_lobl_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Bearing Liabilities" will be neutral |
| 942 | `mdl264_lobl_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Bearing Liabilities' will move up |
| 943 | `mdl264_lotb_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Short Term Borrowings' (1: fall, 2: neutral, 3: move up) |
| 944 | `mdl264_lotb_l1` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Short Term Borrowings" will fall |
| 945 | `mdl264_lotb_l2` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Short Term Borrowings" will be neutral |
| 946 | `mdl264_lotb_l3` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Short Term Borrowings" will be move-up |
| 947 | `mdl264_lottery_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class for maximum daily return in the last 1M (lottery factor) (1=fall, 2=neutral, 3=move-up) |
| 948 | `mdl264_lottery_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of maximum daily return in the last 1M (lottery factor) will be fall |
| 949 | `mdl264_lottery_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of maximum daily return in the last 1M (lottery factor) will be neutral |
| 950 | `mdl264_lottery_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of maximum daily return in the last 1M (lottery factor) will be move-up |
| 951 | `mdl264_lstb_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Short Term Borrowings" (1: fall, 2: neutral, 3: move up) |
| 952 | `mdl264_lstd_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Notes Payable/Short Term Debt" (1: fall, 2: neutral, 3: move-up) |
| 953 | `mdl264_lt_dt_eq_chg_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "YoY change in long-term debt/common equity" (1: fall, 2: neutral, 3: move-up) |
| 954 | `mdl264_ltxp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Income Taxes Payable" (1: fall, 2: neutral, 3: move-up) |
| 955 | `mdl264_lupr_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Unearned Premium/Unearned Revenue" (1: fall, 2: neutral, 3: move-up) |
| 956 | `mdl264_ma_15_36_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Modal class (1=fall, 2=neutral, 3=move-up) of the predicted trend for moving average crossover (15-week vs 36-week) |
| 957 | `mdl264_ma_30_75_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Moving average crossover, 30W-75W" (1: fall, 2: neutral, 3: move-up) |
| 958 | `mdl264_macd_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of MACD will be fall |
| 959 | `mdl264_macd_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of MACD will be neutral |
| 960 | `mdl264_macd_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of MACD will be move-up |
| 961 | `mdl264_mbbc_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "EBITDAR" (1: fall, 2: neutral, 3: move-up) |
| 962 | `mdl264_mbbe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Passengers, Total" (1: fall, 2: neutral, 3: move-up) |
| 963 | `mdl264_mbdl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Load Factor, Total -%" (1: fall, 2: neutral, 3: move-up) |
| 964 | `mdl264_mfi_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of Money Flow Index (1: fall, 2: neutral, 3: move-up) |
| 965 | `mdl264_mhak_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Revenue per Avail. Room (REVPAR), Total" (1: fall, 2: neutral, 3: move-up) |
| 966 | `mdl264_mhak_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Revenue per Avail. Room (REVPAR), Total' will fall |
| 967 | `mdl264_mhak_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Revenue per Avail. Room (REVPAR), Total" will be neutral |
| 968 | `mdl264_mhak_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Revenue per Avail. Room (REVPAR), Total' will move up |
| 969 | `mdl264_mhaz_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Rooms" (1: fall, 2: neutral, 3: move-up) |
| 970 | `mdl264_mi_class` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Predicted trend class for Mass Index coded as 1 fall 2 neutral 3 move-up |
| 971 | `mdl264_mibh_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Loss Ratio, Total -%" (1: fall, 2: neutral, 3: move-up) |
| 972 | `mdl264_mibh_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Loss Ratio, Total -%" will fall |
| 973 | `mdl264_mibh_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Loss Ratio, Total -%" will be neutral |
| 974 | `mdl264_mibh_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Loss Ratio, Total -%" will move up |
| 975 | `mdl264_mibl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Combined Ratio, Total -%" (1: fall, 2: neutral, 3: move-up) |
| 976 | `mdl264_mibl_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Combined Ratio, Total -%" will fall |
| 977 | `mdl264_mibl_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Combined Ratio, Total -%" will be neutral |
| 978 | `mdl264_mibl_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Combined Ratio, Total -%" will move up |
| 979 | `mdl264_mibz_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Underwriting Profit or Loss" (1: fall, 2: neutral, 3: move-up) |
| 980 | `mdl264_mibz_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Underwriting Profit or Loss" will fall |
| 981 | `mdl264_mibz_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Underwriting Profit or Loss" will move up |
| 982 | `mdl264_migo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "New Business Annual Premium Equiv. (APE)" (1: fall, 2: neutral, 3: move up) |
| 983 | `mdl264_migo_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'New Business Annual Premium Equiv. (APE)' will fall |
| 984 | `mdl264_migo_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "New Business Annual Premium Equiv. (APE)" will be neutral |
| 985 | `mdl264_migo_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "New Business Annual Premium Equiv. (APE)" will move up |
| 986 | `mdl264_mnio_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Net Interest Margin, Total -%" (1: fall, 2: neutral, 3: move up) |
| 987 | `mdl264_mobh_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of 'Crude Oil, Avg. Sales pp. Barrel, Total' (1: fall, 2: neutral, 3: move up) |
| 988 | `mdl264_mobh_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Crude Oil, Avg. Sales pp. Barrel, Total" will fall |
| 989 | `mdl264_mobh_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Crude Oil, Avg. Sales pp. Barrel, Total" will be neutral |
| 990 | `mdl264_mobh_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Crude Oil, Avg. Sales pp. Barrel, Total" will move up |
| 991 | `mdl264_mobk_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of 'Crude Oil Production (Barrels)' (1: fall, 2: neutral, 3: move up) |
| 992 | `mdl264_mobk_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Crude Oil Production (Barrels)' will fall |
| 993 | `mdl264_mobk_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Crude Oil Production (Barrels)" will be neutral |
| 994 | `mdl264_mobk_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Crude Oil Production (Barrels)' will move up |
| 995 | `mdl264_mogo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Exploration and Development Costs' (1: fall, 2: neutral, 3: move up) |
| 996 | `mdl264_mogo_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Exploration and Development Costs" will fall |
| 997 | `mdl264_mogo_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Exploration and Development Costs" will be neutral |
| 998 | `mdl264_mogo_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Exploration and Development Costs' will move up |
| 999 | `mdl264_moio_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Wells, New" (1: fall, 2: neutral, 3: move-up) |
| 1000 | `mdl264_moio_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Wells, New" will be fall |
| 1001 | `mdl264_moio_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Wells, New' will move up |
| 1002 | `mdl264_mpp1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Products in Phase I" (1: fall, 2: neutral, 3: move-up) |
| 1003 | `mdl264_mpp2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Products in Phase II" (1: fall, 2: neutral, 3: move-up) |
| 1004 | `mdl264_mpp3_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Products in Phase III" (1: fall, 2: neutral, 3: move up) |
| 1005 | `mdl264_mppl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Products Launched" (1: fall, 2: neutral, 3: move up) |
| 1006 | `mdl264_mpre_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Products in Pre-Registration" (1: fall, 2: neutral, 3: move-up) |
| 1007 | `mdl264_mrth_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Rent Growth (Sequential), Total -%" (1: fall, 2: neutral, 3: move-up) |
| 1008 | `mdl264_mtbd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Comp. Store Sales, Retail, Total - %" (1: fall, 2: neutral, 3: move-up) |
| 1009 | `mdl264_mtbl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Merchandise Margins, Total -%" (1: fall, 2: neutral, 3: move-up) |
| 1010 | `mdl264_mtho_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Number of Stores Closed" (1: fall, 2: neutral, 3: move-up) |
| 1011 | `mdl264_mtho_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Stores Closed' will fall |
| 1012 | `mdl264_mtho_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Number of Stores Closed" will be move-up |
| 1013 | `mdl264_mtje_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Value of Bookings" (1: fall, 2: neutral, 3: move up) |
| 1014 | `mdl264_news_abno_sent_1d_class` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Predicted trend of "Abnormal sentiment of novel/relevant/non-neutral news 1D/365D" (1: fall, 2: neutral, 3: move-up) |
| 1015 | `mdl264_news_abno_sent_1d_l1` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Abnormal sentiment of novel/relevant/non-neutral news 1D/365D" will be fall |
| 1016 | `mdl264_news_abno_sent_1d_l2` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Abnormal sentiment of novel/relevant/non-neutral news 1D/365D" will be neutral |
| 1017 | `mdl264_news_abno_sent_1d_l3` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Abnormal sentiment of novel/relevant/non-neutral news 1D/365D" will be move-up |
| 1018 | `mdl264_news_abno_vol_1d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of abnormal volume (z-score) of novel/relevant/non-neutral news, 1D over 365D |
| 1019 | `mdl264_news_abno_vol_1d_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of abnormal volume (z-score) of novel/relevant/non-neutral news, 1D over 365D will be fall |
| 1020 | `mdl264_news_abno_vol_1d_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Abnormal volume (z-score) of novel/relevant/non-neutral news, 1D/365D" will be neutral |
| 1021 | `mdl264_news_abno_vol_1d_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Abnormal volume (z-score) of novel/relevant/non-neutral news, 1D/365D" will be move-up |
| 1022 | `mdl264_news_sentvol_1d_class` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Predicted trend class for number of novel/relevant/non-neutral news, 1D (1=fall, 2=neutral, 3=move-up) |
| 1023 | `mdl264_news_sentvol_1d_l1` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Probability that the future trend of number of novel/relevant/non-neutral news, 1D will be fall |
| 1024 | `mdl264_news_sentvol_1d_l2` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Probability that the future trend of number of novel/relevant/non-neutral news, 1D will be neutral |
| 1025 | `mdl264_news_sentvol_1d_l3` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Probability that the future trend of number of novel/relevant/non-neutral news, 1D will be move-up |
| 1026 | `mdl264_ngla_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Gain (Loss) on Sale of Assets' (1: fall, 2: neutral, 3: move up) |
| 1027 | `mdl264_nlar_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Labor & Related Expenses" (1: fall, 2: neutral, 3: move-up) |
| 1028 | `mdl264_nlar_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Labor & Related Expenses" will be fall |
| 1029 | `mdl264_nlar_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Labor & Related Expenses" will be neutral |
| 1030 | `mdl264_nlar_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Labor & Related Expenses" will move up |
| 1031 | `mdl264_noex_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Expense" (1: fall, 2: neutral, 3: move up) |
| 1032 | `mdl264_nont_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Non-Operating Income (Expense)" (1: fall, 2: neutral, 3: move-up) |
| 1033 | `mdl264_nont_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Non-Operating Income (Expense)" will be fall |
| 1034 | `mdl264_nont_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Non-Operating Income (Expense)" will be neutral |
| 1035 | `mdl264_nont_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Non-Operating Income (Expense)" will be move-up |
| 1036 | `mdl264_noru_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Revenue" (1: fall, 2: neutral, 3: move-up) |
| 1037 | `mdl264_noru_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Revenue' will fall |
| 1038 | `mdl264_noru_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Revenue" will be neutral |
| 1039 | `mdl264_noru_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Revenue" will move up |
| 1040 | `mdl264_nres_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Restructuring Charge" (1: fall, 2: neutral, 3: move-up) |
| 1041 | `mdl264_nsgl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Investment Securities Gains" (1: fall, 2: neutral, 3: move-up) |
| 1042 | `mdl264_nuie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Unusual Expense" (1: fall, 2: neutral, 3: move-up) |
| 1043 | `mdl264_nuii_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Unusual Income" (1: fall, 2: neutral, 3: move up) |
| 1044 | `mdl264_nvi_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class (1=fall, 2=neutral, 3=move-up) for the Negative Volume Index |
| 1045 | `mdl264_oacr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Accounts Receivable" (1: fall, 2: neutral, 3: move-up) |
| 1046 | `mdl264_oaex_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Accrued Expenses" (1: fall, 2: neutral, 3: move-up) |
| 1047 | `mdl264_oama_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Amortization of Acquisition Costs" (1: fall, 2: neutral, 3: move up) |
| 1048 | `mdl264_oama_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization of Acquisition Costs" will be fall |
| 1049 | `mdl264_oama_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization of Acquisition Costs" will be neutral |
| 1050 | `mdl264_oama_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Amortization of Acquisition Costs' will move up |
| 1051 | `mdl264_oami_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Amortization of Intangibles" (1: fall, 2: neutral, 3: move-up) |
| 1052 | `mdl264_oami_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Amortization of Intangibles' will fall |
| 1053 | `mdl264_oami_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization of Intangibles" will be neutral |
| 1054 | `mdl264_oami_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization of Intangibles" will move up |
| 1055 | `mdl264_oapb_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Accounts Payable" (1: fall, 2: neutral, 3: move-up) |
| 1056 | `mdl264_obdt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Taxes" (1: fall, 2: neutral, 3: move-up) |
| 1057 | `mdl264_obv_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of On Balance Volume |
| 1058 | `mdl264_oido_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Discontinued Operations" (1: fall, 2: neutral, 3: move up) |
| 1059 | `mdl264_oido_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations" will be fall |
| 1060 | `mdl264_oido_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations" will be neutral |
| 1061 | `mdl264_oido_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Discontinued Operations' will move-up |
| 1062 | `mdl264_oitl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Inventories' (1: fall, 2: neutral, 3: move up) |
| 1063 | `mdl264_ooal_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Assets & Liabilities, Net' (1: fall, 2: neutral, 3: move up) |
| 1064 | `mdl264_ooas_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Assets" (1: fall, 2: neutral, 3: move up) |
| 1065 | `mdl264_oolb_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Liabilities" (1: fall, 2: neutral, 3: move up) |
| 1066 | `mdl264_opba_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Payable/Accrued" (1: fall, 2: neutral, 3: move-up) |
| 1067 | `mdl264_oppy_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Prepaid Expenses" (1: fall, 2: neutral, 3: move-up) |
| 1068 | `mdl264_orer_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Reinsurance Receivable' (1: fall, 2: neutral, 3: move up) |
| 1069 | `mdl264_orer_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Reinsurance Receivable" will fall |
| 1070 | `mdl264_orer_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Reinsurance Receivable" will be neutral |
| 1071 | `mdl264_orer_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Reinsurance Receivable' will move up |
| 1072 | `mdl264_payable_to_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of "Accounts payable turnover" (1: fall, 2: neutral, 3: move-up) |
| 1073 | `mdl264_payable_to_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts payable turnover" will be fall |
| 1074 | `mdl264_payable_to_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts payable turnover" will be neutral |
| 1075 | `mdl264_payable_to_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Accounts payable turnover" will be move-up |
| 1076 | `mdl264_ppo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class for percentage price oscillator (1=fall, 2=neutral, 3=move-up) |
| 1077 | `mdl264_psale_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class for "Price-to-sales" where 1=fall, 2=neutral, 3=move-up |
| 1078 | `mdl264_psale_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Price-to-sales" will be fall |
| 1079 | `mdl264_psale_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Price-to-sales" will be neutral |
| 1080 | `mdl264_psale_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Probability that the future trend of "Price-to-sales" will be move-up |
| 1081 | `mdl264_pvo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of "Percentage Volume Oscillator" (1: fall, 2: neutral, 3: move-up) |
| 1082 | `mdl264_qcom_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Comprehensive Income" (1: fall, 2: neutral, 3: move up) |
| 1083 | `mdl264_qote_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Equity" (1: fall, 2: neutral, 3: move up) |
| 1084 | `mdl264_qpso1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Shares Outstanding - Preferred Primary Issue" (1: fall, 2: neutral, 3: move-up) |
| 1085 | `mdl264_qpso2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Shares Outstanding - Preferred Issue 2" (1: fall, 2: neutral, 3: move-up) |
| 1086 | `mdl264_qtpo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Preferred Shares Outstanding" (1: fall, 2: neutral, 3: move-up) |
| 1087 | `mdl264_qtsn1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Treas Shares - Common Stock Primary Issue" (1: fall, 2: neutral, 3: move-up) |
| 1088 | `mdl264_qtsn2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Treasury Shares - Common Issue 2' (1: fall, 2: neutral, 3: move up) |
| 1089 | `mdl264_qugl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Unrealized Gain (Loss)" (1: fall, 2: neutral, 3: move-up) |
| 1090 | `mdl264_reop_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Electric Operations" (1: fall, 2: neutral, 3: move-up) |
| 1091 | `mdl264_rext_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Excise Tax Payments" (1: fall, 2: neutral, 3: move-up) |
| 1092 | `mdl264_rext_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Excise Tax Payments" will be fall |
| 1093 | `mdl264_rext_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Excise Tax Payments" will be neutral |
| 1094 | `mdl264_rext_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Excise Tax Payments' will move up |
| 1095 | `mdl264_risi_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest & Dividends on Investment Secs." (1: fall, 2: neutral, 3: move-up) |
| 1096 | `mdl264_rnir_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Non-Insurance Revenue" (1: fall, 2: neutral, 3: move-up) |
| 1097 | `mdl264_rnts_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Net Sales" (1: fall, 2: neutral, 3: move up) |
| 1098 | `mdl264_rrgl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Realized & Unrealized Gains (Losses)" (1: fall, 2: neutral, 3: move-up) |
| 1099 | `mdl264_rrii_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Reinsurance - Income" (1: fall, 2: neutral, 3: move up) |
| 1100 | `mdl264_rtlr_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Revenue" (1: fall, 2: neutral, 3: move up) |
| 1101 | `mdl264_rtn21d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of "Total return, past 1M" (1: fall, 2: neutral, 3: move-up) |
| 1102 | `mdl264_rtn2520d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class for "Total return, past 120M" where 1=fall, 2=neutral, 3=move-up |
| 1103 | `mdl264_rtn63d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class for 3-month total return: 1 fall, 2 neutral, 3 move-up |
| 1104 | `mdl264_rtn_12m1m_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Modal class of the predicted trend for Price momentum, 12M-1M (1=fall, 2=neutral, 3=move-up) |
| 1105 | `mdl264_sadg_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 'Copper, Average Price per Metric Ton' (1: fall, 2: neutral, 3: move up) |
| 1106 | `mdl264_sadg_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Copper, Average Price per Metric Ton" will be a fall |
| 1107 | `mdl264_sadg_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Copper, Average Price per Metric Ton" will be neutral |
| 1108 | `mdl264_sadg_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Copper, Average Price per Metric Ton" will be move-up |
| 1109 | `mdl264_samt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Amortization" (1: fall, 2: neutral, 3: move up) |
| 1110 | `mdl264_samt_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization" will fall |
| 1111 | `mdl264_samt_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization" will be neutral |
| 1112 | `mdl264_samt_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amortization" will move up |
| 1113 | `mdl264_sani_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Adjustments to Net Income" (1: fall, 2: neutral, 3: move-up) |
| 1114 | `mdl264_sani_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Adjustments to Net Income" will be fall |
| 1115 | `mdl264_sani_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Adjustments to Net Income" will be neutral |
| 1116 | `mdl264_sani_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Adjustments to Net Income' will move up |
| 1117 | `mdl264_sbai_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Basic EPS Including Extraordinary Items" (1: fall, 2: neutral, 3: move up) |
| 1118 | `mdl264_sbbq_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Revenue Passenger Kilometers (RPK)" (1: fall, 2: neutral, 3: move-up) |
| 1119 | `mdl264_sbda_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Normalized EBITDA" (1: fall, 2: neutral, 3: move-up) |
| 1120 | `mdl264_sbdg_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 'Available Seat Kilometers (ASK)' (1: fall, 2: neutral, 3: move up) |
| 1121 | `mdl264_sbit_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Normalized EBIT" (1: fall, 2: neutral, 3: move-up) |
| 1122 | `mdl264_sbit_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized EBIT" will be fall |
| 1123 | `mdl264_sbit_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized EBIT" will be neutral |
| 1124 | `mdl264_sbit_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized EBIT' will move up |
| 1125 | `mdl264_sbjg_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of "Operating Expense per ASK" (1: fall, 2: neutral, 3: move-up) |
| 1126 | `mdl264_scl23_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Capital Lease Payments Due in 2-3 Years" (1: fall, 2: neutral, 3: move up) |
| 1127 | `mdl264_scl2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Capital Lease Payments Due in Year 2" (1: fall, 2: neutral, 3: move-up) |
| 1128 | `mdl264_scl3_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Capital Lease Payments Due in Year 3" (1: fall, 2: neutral, 3: move-up) |
| 1129 | `mdl264_scl45_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Capital Lease Payments Due in 4-5 Years" (1: fall, 2: neutral, 3: move-up) |
| 1130 | `mdl264_scl4_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Capital Lease Payments Due in Year 4' (1: fall, 2: neutral, 3: move up) |
| 1131 | `mdl264_scl5_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Capital Lease Payments Due in Year 5" (1: fall, 2: neutral, 3: move-up) |
| 1132 | `mdl264_scsi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Cash and Short Term Investments" (1: fall, 2: neutral, 3: move-up) |
| 1133 | `mdl264_scur_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Current Ratio" (1: fall, 2: neutral, 3: move up) |
| 1134 | `mdl264_scur_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Current Ratio' will fall |
| 1135 | `mdl264_scur_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Ratio" will be neutral |
| 1136 | `mdl264_scur_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Current Ratio" will be move-up |
| 1137 | `mdl264_sdai_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Diluted EPS Including Extraordinary Items" (1: fall, 2: neutral, 3: move-up) |
| 1138 | `mdl264_sdni_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Diluted Net Income' (1: fall, 2: neutral, 3: move up) |
| 1139 | `mdl264_setr_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of "Effective Tax Rate" (1: fall, 2: neutral, 3: move-up) |
| 1140 | `mdl264_setr_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Effective Tax Rate" will be fall |
| 1141 | `mdl264_setr_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Effective Tax Rate" will be neutral |
| 1142 | `mdl264_setr_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Effective Tax Rate" will be move-up |
| 1143 | `mdl264_sfee_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Foreign Exchange Effects' (1: fall, 2: neutral, 3: move up) |
| 1144 | `mdl264_sfee_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Exchange Effects" will fall |
| 1145 | `mdl264_sfee_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Exchange Effects" will be neutral |
| 1146 | `mdl264_sfee_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Foreign Exchange Effects" will move up |
| 1147 | `mdl264_sgpp_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Gross Margin" (1: fall, 2: neutral, 3: move-up) |
| 1148 | `mdl264_sicf_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Investing Cash Flow Items, Total" (1: fall, 2: neutral, 3: move-up) |
| 1149 | `mdl264_sicf_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Investing Cash Flow Items, Total" will be a fall |
| 1150 | `mdl264_sicf_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Investing Cash Flow Items, Total" will be neutral |
| 1151 | `mdl264_sicf_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Investing Cash Flow Items, Total" will be move-up |
| 1152 | `mdl264_siib_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest Income, Bank" (1: fall, 2: neutral, 3: move up) |
| 1153 | `mdl264_siin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest/Invest Income - Non-Operating" (1: fall, 2: neutral, 3: move-up) |
| 1154 | `mdl264_siio_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest/Investment Income - Operating" (1: fall, 2: neutral, 3: move-up) |
| 1155 | `mdl264_sinn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest Exp.(Inc.),Net-Operating, Total" (1: fall, 2: neutral, 3: move-up) |
| 1156 | `mdl264_sinn_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Exp.(Inc.), Net-Operating, Total" will fall |
| 1157 | `mdl264_sinn_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Exp.(Inc.), Net-Operating, Total" will be neutral |
| 1158 | `mdl264_sinn_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Exp.(Inc.), Net-Operating, Total" will be move-up |
| 1159 | `mdl264_sld10_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Long Term Debt Maturing in Year 10' (1: fall, 2: neutral, 3: move up) |
| 1160 | `mdl264_sld1_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Long Term Debt Maturing within 1 Year" (1: fall, 2: neutral, 3: move-up) |
| 1161 | `mdl264_sld2_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Long-Term Debt Maturing in Year 2' (1: fall, 2: neutral, 3: move-up) |
| 1162 | `mdl264_sld3_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Long Term Debt Maturing in Year 3" (1: fall, 2: neutral, 3: move-up) |
| 1163 | `mdl264_sld45_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Long Term Debt Maturing in 4-5 Years" (1: fall, 2: neutral, 3: move-up) |
| 1164 | `mdl264_sld5_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Long Term Debt Maturing in Year 5" (1: fall, 2: neutral, 3: move up) |
| 1165 | `mdl264_sld6b_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Long Term Debt Matur. in Year 6 & Beyond" (1: fall, 2: neutral, 3: move-up) |
| 1166 | `mdl264_sld7_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Long Term Debt Maturing in Year 7' (1: fall, 2: neutral, 3: move-up) |
| 1167 | `mdl264_sld8_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Long Term Debt Maturing in Year 8" (1: fall, 2: neutral, 3: move-up) |
| 1168 | `mdl264_sncc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Net Change in Cash" (1: fall, 2: neutral, 3: move-up) |
| 1169 | `mdl264_snce_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Net Cash - Ending Balance" (1: fall, 2: neutral, 3: move up) |
| 1170 | `mdl264_snie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Non-Interest Expense, Bank" (1: fall, 2: neutral, 3: move-up) |
| 1171 | `mdl264_snii_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Non-Interest Income, Bank" (1: fall, 2: neutral, 3: move-up) |
| 1172 | `mdl264_snin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest Inc.(Exp.), Net-Non-Op., Total" (1: fall, 2: neutral, 3: move up) |
| 1173 | `mdl264_snpm_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Net Profit Margin" (1: fall, 2: neutral, 3: move-up) |
| 1174 | `mdl264_so_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class (1=fall, 2=neutral, 3=move-up) for the Stochastic Oscillator |
| 1175 | `mdl264_soca_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Current Assets, Total" (1: fall, 2: neutral, 3: move-up) |
| 1176 | `mdl264_soca_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets, Total' will fall |
| 1177 | `mdl264_soca_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Current Assets, Total" will be neutral |
| 1178 | `mdl264_soca_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets, Total' will move up |
| 1179 | `mdl264_socf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Changes in Working Capital" (1: fall, 2: neutral, 3: move-up) |
| 1180 | `mdl264_socf_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Changes in Working Capital" will be fall |
| 1181 | `mdl264_socf_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Changes in Working Capital" will be neutral |
| 1182 | `mdl264_socf_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Changes in Working Capital" will move up |
| 1183 | `mdl264_socl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Current Liabilities, Total" (1: fall, 2: neutral, 3: move-up) |
| 1184 | `mdl264_socl_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Liabilities, Total' will fall |
| 1185 | `mdl264_socl_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Current Liabilities, Total" will be neutral |
| 1186 | `mdl264_socl_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Current Liabilities, Total" will be move-up |
| 1187 | `mdl264_sodo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 'Natural Gas, Avg. Sales Price per Cu.Mt.' (1: fall, 2: neutral, 3: move up) |
| 1188 | `mdl264_sodo_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Natural Gas, Avg. Sales Price per Cu.Mt." will be fall |
| 1189 | `mdl264_sodo_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Natural Gas, Avg. Sales Price per Cu.Mt." will be neutral |
| 1190 | `mdl264_sodo_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Natural Gas, Avg. Sales Price per Cu.Mt." will be move-up |
| 1191 | `mdl264_sol23_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Operating Lease Pymts. Due in 2-3 Years" (1: fall, 2: neutral, 3: move up) |
| 1192 | `mdl264_sol23_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Pymts. Due in 2-3 Years" will fall |
| 1193 | `mdl264_sol23_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in 2-3 Years' will be neutral |
| 1194 | `mdl264_sol23_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in 2-3 Years' will move up |
| 1195 | `mdl264_sol2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Operating Lease Payments Due in Year 2" (1: fall, 2: neutral, 3: move-up) |
| 1196 | `mdl264_sol2_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 2" will be fall |
| 1197 | `mdl264_sol2_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in Year 2' will be neutral |
| 1198 | `mdl264_sol2_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 2" will be move-up |
| 1199 | `mdl264_sol3_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Operating Lease Payments Due in Year 3' (1: fall, 2: neutral, 3: move up) |
| 1200 | `mdl264_sol3_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 3" will be fall |
| 1201 | `mdl264_sol3_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 3" will be neutral |
| 1202 | `mdl264_sol3_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 3" will be move-up |
| 1203 | `mdl264_sol45_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Operating Lease Pymts. Due in 4-5 Years" (1: fall, 2: neutral, 3: move-up) |
| 1204 | `mdl264_sol45_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Pymts. Due in 4-5 Years" will be fall |
| 1205 | `mdl264_sol45_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in 4-5 Years" will be neutral |
| 1206 | `mdl264_sol45_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in 4-5 Years" will move up |
| 1207 | `mdl264_sol4_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Operating Lease Payments Due in Year 4" (1: fall, 2: neutral, 3: move-up) |
| 1208 | `mdl264_sol4_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in Year 4' will fall |
| 1209 | `mdl264_sol4_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 4" will be neutral |
| 1210 | `mdl264_sol4_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in Year 4' will move up |
| 1211 | `mdl264_sol5_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Operating Lease Payments Due in Year 5" (1: fall, 2: neutral, 3: move-up) |
| 1212 | `mdl264_sol5_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 5" will fall |
| 1213 | `mdl264_sol5_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 5" will be neutral |
| 1214 | `mdl264_sol5_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Lease Payments Due in Year 5" will be move-up |
| 1215 | `mdl264_sol6b_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Oper. Lse. Pymts. Due in Year 6 & Beyond" (1: fall, 2: neutral, 3: move-up) |
| 1216 | `mdl264_sol6b_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Oper. Lse. Pymts. Due in Year 6 & Beyond" will fall |
| 1217 | `mdl264_sol6b_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Oper. Lse. Pymts. Due in Year 6 & Beyond" will be neutral |
| 1218 | `mdl264_sol6b_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Oper. Lse. Pymts. Due in Year 6 & Beyond" will be move-up |
| 1219 | `mdl264_sont_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other, Net" (1: fall, 2: neutral, 3: move-up) |
| 1220 | `mdl264_sont_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other, Net' will fall |
| 1221 | `mdl264_sont_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other, Net" will be neutral |
| 1222 | `mdl264_sont_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other, Net' will move up |
| 1223 | `mdl264_sooe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Operating Expenses, Total" (1: fall, 2: neutral, 3: move-up) |
| 1224 | `mdl264_sopi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Operating Income' (1: fall, 2: neutral, 3: move up) |
| 1225 | `mdl264_sopi_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Income" will fall |
| 1226 | `mdl264_sopi_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Income" will be neutral |
| 1227 | `mdl264_sopi_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Income" will be move-up |
| 1228 | `mdl264_sopp_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Operating Margin" (1: fall, 2: neutral, 3: move-up) |
| 1229 | `mdl264_sopp_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Margin" will be fall |
| 1230 | `mdl264_sopp_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Margin" will be neutral |
| 1231 | `mdl264_sopp_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Operating Margin" will move up |
| 1232 | `mdl264_spi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class for "Special Items" (1=fall, 2=neutral, 3=move-up) |
| 1233 | `mdl264_spig_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Iron Ore Production (Metric Tonnes)" (1: fall, 2: neutral, 3: move-up) |
| 1234 | `mdl264_spig_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Iron Ore Production (Metric Tonnes)" will be a fall |
| 1235 | `mdl264_spig_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Iron Ore Production (Metric Tonnes)" will be neutral |
| 1236 | `mdl264_spig_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Iron Ore Production (Metric Tonnes)" will be move-up |
| 1237 | `mdl264_sptm_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Pretax Margin" (1: fall, 2: neutral, 3: move-up) |
| 1238 | `mdl264_sqck_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Quick Ratio" (1: fall, 2: neutral, 3: move-up) |
| 1239 | `mdl264_srev_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Revenue" (1: fall, 2: neutral, 3: move-up) |
| 1240 | `mdl264_srev_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Revenue" will fall |
| 1241 | `mdl264_srev_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Revenue" will be neutral |
| 1242 | `mdl264_srev_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Revenue" will move up |
| 1243 | `mdl264_stld_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Debt" (1: fall, 2: neutral, 3: move up) |
| 1244 | `mdl264_stpe_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Plan Expected Return" (1: fall, 2: neutral, 3: move-up) |
| 1245 | `mdl264_stpi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Total Plan Interest Cost' (1: fall, 2: neutral, 3: move up) |
| 1246 | `mdl264_stpr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Plan Other Expense" (1: fall, 2: neutral, 3: move-up) |
| 1247 | `mdl264_stps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Total Plan Service Cost' (1: fall, 2: neutral, 3: move up) |
| 1248 | `mdl264_stsi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Special Items" (1: fall, 2: neutral, 3: move-up) |
| 1249 | `mdl264_stxi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Extraordinary Items" (1: fall, 2: neutral, 3: move up) |
| 1250 | `mdl264_suie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Unusual Expense (Income)' (1: fall, 2: neutral, 3: move up) |
| 1251 | `mdl264_suie_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unusual Expense (Income)" will fall |
| 1252 | `mdl264_suie_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unusual Expense (Income)" will be neutral |
| 1253 | `mdl264_suie_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Unusual Expense (Income)" will be move-up |
| 1254 | `mdl264_suit_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Non-Recurring Items, Total" (1: fall, 2: neutral, 3: move up) |
| 1255 | `mdl264_suit_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Non-Recurring Items, Total" will fall |
| 1256 | `mdl264_suit_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Non-Recurring Items, Total" will be neutral |
| 1257 | `mdl264_suit_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Non-Recurring Items, Total' will move up |
| 1258 | `mdl264_tiat_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Net Income After Taxes" (1: fall, 2: neutral, 3: move-up) |
| 1259 | `mdl264_trix_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Modal class of the predicted trend for TRIX (1=fall, 2=neutral, 3=move-up) |
| 1260 | `mdl264_trix_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of TRIX will be fall |
| 1261 | `mdl264_trix_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of TRIX will be neutral |
| 1262 | `mdl264_trix_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Probability that the future trend of TRIX will be move-up |
| 1263 | `mdl264_trkdpit_intfv_xgb_dl8_d1_xido_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Discontinued Operations" (1: fall, 2: neutral, 3: move-up) |
| 1264 | `mdl264_trkdpit_intfv_xgb_dl8_d1_xido_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Discontinued Operations' will fall |
| 1265 | `mdl264_trkdpit_intfv_xgb_dl8_d1_xido_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations" will be neutral |
| 1266 | `mdl264_trkdpit_intfv_xgb_dl8_d1_xido_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Discontinued Operations" will be move-up |
| 1267 | `mdl264_tsi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class for True Strength Index (1=fall, 2=neutral, 3=move-up) |
| 1268 | `mdl264_tstk_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class of Treasury Stock - Total (All Capital) (1: fall, 2: neutral, 3: move-up) |
| 1269 | `mdl264_tstk_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Stock - Total (All Capital) will be fall |
| 1270 | `mdl264_tstk_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Stock - Total (All Capital) will be neutral |
| 1271 | `mdl264_tstk_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Stock - Total (All Capital) will be move-up |
| 1272 | `mdl264_ttax_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Provision for Income Taxes" (1: fall, 2: neutral, 3: move-up) |
| 1273 | `mdl264_ttax_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Provision for Income Taxes" will fall |
| 1274 | `mdl264_ttax_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Provision for Income Taxes" will be neutral |
| 1275 | `mdl264_ttax_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Provision for Income Taxes" will be move-up |
| 1276 | `mdl264_vadl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Revenue - Long Term" (1: fall, 2: neutral, 3: move-up) |
| 1277 | `mdl264_vadv_class` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Predicted trend of "Advertising Expense, Supplemental" (1: fall, 2: neutral, 3: move-up) |
| 1278 | `mdl264_vama_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Amort of Acquisition Costs, Supplemental" (1: fall, 2: neutral, 3: move up) |
| 1279 | `mdl264_vama_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amort of Acquisition Costs, Supplemental" will fall |
| 1280 | `mdl264_vama_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amort of Acquisition Costs, Supplemental" will be neutral |
| 1281 | `mdl264_vama_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Amort of Acquisition Costs, Supplemental" will move up |
| 1282 | `mdl264_vctc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Current Tax - Total" (1: fall, 2: neutral, 3: move-up) |
| 1283 | `mdl264_vctd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Current Tax - Domestic" (1: fall, 2: neutral, 3: move-up) |
| 1284 | `mdl264_vctf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Current Tax - Foreign" (1: fall, 2: neutral, 3: move-up) |
| 1285 | `mdl264_vctl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Current Tax - Local' (1: fall, 2: neutral, 3: move up) |
| 1286 | `mdl264_vcto_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Current Tax - Other" (1: fall, 2: neutral, 3: move-up) |
| 1287 | `mdl264_vctr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Current Tax - Total' (1: fall, 2: neutral, 3: move up) |
| 1288 | `mdl264_vdpp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Domestic Pension Plan Expense" (1: fall, 2: neutral, 3: move up) |
| 1289 | `mdl264_vdtc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Tax - Total" (1: fall, 2: neutral, 3: move-up) |
| 1290 | `mdl264_vdtd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Tax - Domestic" (1: fall, 2: neutral, 3: move-up) |
| 1291 | `mdl264_vdtf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Tax - Foreign" (1: fall, 2: neutral, 3: move-up) |
| 1292 | `mdl264_vdtl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Tax - Local" (1: fall, 2: neutral, 3: move-up) |
| 1293 | `mdl264_vdto_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Deferred Tax - Other' (1: fall, 2: neutral, 3: move up) |
| 1294 | `mdl264_vdtr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Deferred Tax - Total" (1: fall, 2: neutral, 3: move-up) |
| 1295 | `mdl264_veia_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Equity in Affiliates, Supplemental" (1: fall, 2: neutral, 3: move-up) |
| 1296 | `mdl264_veia_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Equity in Affiliates, Supplemental" will fall |
| 1297 | `mdl264_veia_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Equity in Affiliates, Supplemental" will be neutral |
| 1298 | `mdl264_veia_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Equity in Affiliates, Supplemental' will move up |
| 1299 | `mdl264_veps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'EPS, Supplemental' (1: fall, 2: neutral, 3: move up) |
| 1300 | `mdl264_veps_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "EPS, Supplemental" will be fall |
| 1301 | `mdl264_veps_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "EPS, Supplemental" will be neutral |
| 1302 | `mdl264_veps_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "EPS, Supplemental" will be move-up |
| 1303 | `mdl264_vfic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest Cost - Foreign" (1: fall, 2: neutral, 3: move-up) |
| 1304 | `mdl264_vfpp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Foreign Pension Plan Expense" (1: fall, 2: neutral, 3: move-up) |
| 1305 | `mdl264_vfsc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Service Cost - Foreign" (1: fall, 2: neutral, 3: move up) |
| 1306 | `mdl264_vfxr_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Expected Return on Assets - Foreign" (1: fall, 2: neutral, 3: move up) |
| 1307 | `mdl264_vgla_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "(Gain) Loss on Sale of Assets, Suppl." (1: fall, 2: neutral, 3: move up) |
| 1308 | `mdl264_vi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend class for Vortex Indicator (1=fall, 2=neutral, 3=move-up) |
| 1309 | `mdl264_viac_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Normalized Inc. Avail to Com." (1: fall, 2: neutral, 3: move-up) |
| 1310 | `mdl264_viac_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized Inc. Avail to Com." will fall |
| 1311 | `mdl264_viac_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized Inc. Avail to Com." will be neutral |
| 1312 | `mdl264_viac_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized Inc. Avail to Com." will move up |
| 1313 | `mdl264_vias_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Impairment-Assets Held for Sale, Suppl." (1: fall, 2: neutral, 3: move-up) |
| 1314 | `mdl264_vias_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Impairment-Assets Held for Sale, Suppl.' will fall |
| 1315 | `mdl264_vias_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Sale, Suppl." will be neutral |
| 1316 | `mdl264_vias_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Sale, Suppl." will be move-up |
| 1317 | `mdl264_viat_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Normalized Income After Taxes" (1: fall, 2: neutral, 3: move-up) |
| 1318 | `mdl264_viat_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized Income After Taxes' will fall |
| 1319 | `mdl264_viat_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized Income After Taxes" will be neutral |
| 1320 | `mdl264_viat_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Normalized Income After Taxes" will move up |
| 1321 | `mdl264_viau_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of "Impairment-Assets Held for Use, Suppl." (1: fall, 2: neutral, 3: move-up) |
| 1322 | `mdl264_viau_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Use, Suppl." will be fall |
| 1323 | `mdl264_viau_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Use, Suppl." will be neutral |
| 1324 | `mdl264_viau_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Impairment-Assets Held for Use, Suppl." will move up |
| 1325 | `mdl264_vicd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Interest Cost - Domestic' (1: fall, 2: neutral, 3: move up) |
| 1326 | `mdl264_vicd_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Cost - Domestic" will fall |
| 1327 | `mdl264_vicd_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Cost - Domestic" will be neutral |
| 1328 | `mdl264_vicd_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Interest Cost - Domestic' will move up |
| 1329 | `mdl264_vinc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest Costs" (1: fall, 2: neutral, 3: move up) |
| 1330 | `mdl264_vint_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Intangibles - Net' (1: fall, 2: neutral, 3: move up) |
| 1331 | `mdl264_vint_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Intangibles - Net' will fall |
| 1332 | `mdl264_vint_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Intangibles - Net" will be neutral |
| 1333 | `mdl264_vint_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Intangibles - Net" will be move-up |
| 1334 | `mdl264_vitn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Inc Tax Ex Impact of Sp Items' (1: fall, 2: neutral, 3: move-up) |
| 1335 | `mdl264_vitt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Income Tax - Total" (1: fall, 2: neutral, 3: move up) |
| 1336 | `mdl264_vmin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Minority Interest, Supplemental" (1: fall, 2: neutral, 3: move-up) |
| 1337 | `mdl264_vmin_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Minority Interest, Supplemental" will fall |
| 1338 | `mdl264_vmin_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Minority Interest, Supplemental" will be neutral |
| 1339 | `mdl264_vmin_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Minority Interest, Supplemental" will be move-up |
| 1340 | `mdl264_vol_vo_p_1m_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of "Volatility of volume/price, 1M" (1: fall, 2: neutral, 3: move-up) |
| 1341 | `mdl264_vol_vo_p_1m_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Volatility of volume/price, 1M" will be fall |
| 1342 | `mdl264_vol_vo_p_1m_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Volatility of volume/price, 1M" will be neutral |
| 1343 | `mdl264_vol_vo_p_1m_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Volatility of volume/price, 1M" will be move-up |
| 1344 | `mdl264_votd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Domestic Tax - Other" (1: fall, 2: neutral, 3: move-up) |
| 1345 | `mdl264_voto_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Tax" (1: fall, 2: neutral, 3: move-up) |
| 1346 | `mdl264_voto_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Tax" will be fall |
| 1347 | `mdl264_voto_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Other Tax" will be neutral |
| 1348 | `mdl264_voto_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Tax' will move up |
| 1349 | `mdl264_vpic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Interest Cost - Post-Retirement" (1: fall, 2: neutral, 3: move-up) |
| 1350 | `mdl264_vpic_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Cost - Post-Retirement" will be fall |
| 1351 | `mdl264_vpic_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Interest Cost - Post-Retirement" will be neutral |
| 1352 | `mdl264_vpic_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Interest Cost - Post-Retirement' will move up |
| 1353 | `mdl264_vpsc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Service Cost - Post-Retirement" (1: fall, 2: neutral, 3: move up) |
| 1354 | `mdl264_vpt_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend class (1: fall, 2: neutral, 3: move-up) of Volume Price Trend |
| 1355 | `mdl264_vpti_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Normalized Income Before Taxes" (1: fall, 2: neutral, 3: move-up) |
| 1356 | `mdl264_vres_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Restructuring Charge, Supplemental" (1: fall, 2: neutral, 3: move-up) |
| 1357 | `mdl264_vrpe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Post-Retirement Plan Expense" (1: fall, 2: neutral, 3: move-up) |
| 1358 | `mdl264_vscd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Service Cost - Domestic" (1: fall, 2: neutral, 3: move-up) |
| 1359 | `mdl264_vscp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Stock-Based Compensation, Supplemental" (1: fall, 2: neutral, 3: move-up) |
| 1360 | `mdl264_vtar_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Audit-Related Fees" (1: fall, 2: neutral, 3: move up) |
| 1361 | `mdl264_vtar_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Audit-Related Fees" will be fall |
| 1362 | `mdl264_vtar_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Audit-Related Fees" will be neutral |
| 1363 | `mdl264_vtar_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Audit-Related Fees' will move up |
| 1364 | `mdl264_vtau_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Audit Fees' (1: fall, 2: neutral, 3: move up) |
| 1365 | `mdl264_vtau_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Audit Fees" will be fall |
| 1366 | `mdl264_vtau_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Audit Fees" will be neutral |
| 1367 | `mdl264_vtau_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Audit Fees" will move up |
| 1368 | `mdl264_vtcl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Capital Leases, Supplemental" (1: fall, 2: neutral, 3: move-up) |
| 1369 | `mdl264_vtdt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Domestic Tax' (1: fall, 2: neutral, 3: move up) |
| 1370 | `mdl264_vtft_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Foreign Tax" (1: fall, 2: neutral, 3: move-up) |
| 1371 | `mdl264_vtit_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of 'Income Tax by Region - Total' (1: fall, 2: neutral, 3: move up) |
| 1372 | `mdl264_vtit_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Tax by Region - Total" will fall |
| 1373 | `mdl264_vtit_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Tax by Region - Total" will be neutral |
| 1374 | `mdl264_vtit_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Income Tax by Region - Total" will be move-up |
| 1375 | `mdl264_vtof_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "All Other Fees" (1: fall, 2: neutral, 3: move-up) |
| 1376 | `mdl264_vtol_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Operating Leases, Supplemental" (1: fall, 2: neutral, 3: move-up) |
| 1377 | `mdl264_vtol_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Operating Leases, Supplemental" will fall |
| 1378 | `mdl264_vtol_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Operating Leases, Supplemental" will be neutral |
| 1379 | `mdl264_vtol_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Total Operating Leases, Supplemental" will move up |
| 1380 | `mdl264_vtpe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Total Pension Expense" (1: fall, 2: neutral, 3: move-up) |
| 1381 | `mdl264_vtps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Prior Service Cost - Domestic' (1: fall, 2: neutral, 3: move up) |
| 1382 | `mdl264_vttf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Tax Fees" (1: fall, 2: neutral, 3: move-up) |
| 1383 | `mdl264_vuie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Unusual Expense (Income), Suppl." (1: fall, 2: neutral, 3: move-up) |
| 1384 | `mdl264_vxag_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Actuarial Gains and Losses - Domestic" (1: fall, 2: neutral, 3: move up) |
| 1385 | `mdl264_vxct_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Curtailments & Settlements - Domestic" (1: fall, 2: neutral, 3: move-up) |
| 1386 | `mdl264_vxpe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Post-Retirement, Net" (1: fall, 2: neutral, 3: move-up) |
| 1387 | `mdl264_vxpo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Other Pension, Net - Domestic" (1: fall, 2: neutral, 3: move up) |
| 1388 | `mdl264_wr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Williams %R" (1: fall, 2: neutral, 3: move-up) |
| 1389 | `mdl264_xnic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Income Available to Com Incl ExtraOrd" (1: fall, 2: neutral, 3: move-up) |
| 1390 | `mdl264_xtra_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of "Extraordinary Item" (1: fall, 2: neutral, 3: move-up) |
| 1391 | `mdl264_xtra_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Extraordinary Item" will fall |
| 1392 | `mdl264_xtra_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Extraordinary Item" will be neutral |
| 1393 | `mdl264_xtra_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of "Extraordinary Item" will move up |

## 六、本地回测证据

- 本地累计回测 **14** 条；其中 `ra_failed_checks` 为空的 **14** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `vRrKNKqw` | 0.48 | 0.16 | — | — | 0.08 | 0 | 191 | `ts_zscore(mdl264_1l_ppgs, 66)` |
| `88jmvZ1q` | 0.31 | 0.08 | — | — | 0.07 | 0 | 192 | `vector_neut(rank(ts_backfill(mdl264_1l_m1d_1yf_spd_se,22)), rank(ts_backfill(mdl264_1l_m1d` |
| `LLNP5wAv` | 0.26 | 0.06 | — | — | 0.04 | 0 | 192 | `rank(group_neutralize(subtract(rank(ts_backfill(subtract(mdl264_asti_l3,mdl264_asti_l1),22` |
| `gJbY8Y6m` | 0.25 | 0.06 | — | — | 0.04 | 0 | 191 | `group_rank(mdl264_1l_rltr, subindustry)` |
| `j2A5eJb9` | 0.20 | 0.05 | — | — | 0.12 | 0 | 192 | `group_zscore(divide(ts_delta(ts_backfill(mdl264_2l_mpns,22),5), add(ts_std_dev(ts_backfill` |
| `XgbjojGa` | 0.13 | 0.02 | — | — | 0.09 | 0 | 191 | `rank(ts_delta(mdl264_1l_m1r_cer_se, 22))` |
| `9qjzpzZo` | 0.05 | 0.00 | — | — | 0.08 | 0 | 191 | `rank(ts_delta(mdl264_1l_m1r_1yf_spe_se, 22))` |
| `LLNPGPL2` | -0.02 | 0.00 | — | — | 0.06 | 0 | 191 | `rank(mdl264_1l_m1m21_ntr)` |
| `RRbJAone` | -0.17 | -0.03 | — | — | 0.03 | 0 | 192 | `trade_when(equal(mdl264_ouie_class, 3), subtract(mdl264_rnts_class, vector_neut(mdl264_oid` |
| `JjNVPkKn` | -0.29 | -0.14 | — | — | 0.03 | 0 | 192 | `divide(subtract(ts_backfill(mdl264_mthk_class,22), ts_backfill(mdl264_mtho_class,22)), add` |
| `zq8vNvKV` | -0.31 | -0.11 | — | — | 0.06 | 0 | 191 | `rank(mdl264_1l_rta)` |
| `mLmPYNM5` | -0.52 | -0.39 | — | — | 0.03 | 0 | 192 | `ts_corr(sign(subtract(mdl264_macd_class, 2)), reverse(sign(subtract(mdl264_mibl_class, 2))` |
| `LLNPGPjn` | -0.61 | -0.28 | — | — | 0.04 | 0 | 191 | `rank(mdl264_1l_d0252ntr)` |
| `JjNVGVMx` | -0.88 | -0.40 | — | — | 0.09 | 0 | 191 | `ts_zscore(mdl264_1l_dlts, 66)` |

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

