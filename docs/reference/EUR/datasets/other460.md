# other460 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `other460` |
| 名称 | Predictive data using Deep Learning models |
| 类别 | MODEL |
| 数据字段数(平台) | 1393 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 122 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | MATRIX |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

Time series data prediction using deep learning techniques

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
| UNTESTED | 1386 | 99.5% |
| DEAD | 5 | 0.4% |
| WEAK | 1 | 0.1% |
| DEAD_STATIC | 1 | 0.1% |

- 已实测字段：**7** 个（1%），best_sharpe 最高 **1.22**，中位 -0.36

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 833 | 1.00 | oth460_sopi_l3、oth460_viac_l3、oth460_1l_1nstq |
| 盈利与财务 | 311 | 1.00 | oth460_divyld_bb_l3、oth460_1l_dlts、oth460_fincf_l1 |
| 价量与波动 | 96 | 1.00 | oth460_float_to_l3、oth460_1l_d0252ntr、oth460_1l_d12ntr |
| 修正与预期 | 96 | 1.00 | oth460_es_sale_ntm_r1m_l3、oth460_1l_m1d_cer_se、oth460_1l_m1d_pt_se |
| 持仓与资金流 | 24 | 1.00 | oth460_1l_boie、oth460_1l_btsl、oth460_1l_fmc |
| 宏观与行业 | 20 | 1.00 | oth460_1l_icc、oth460_2l_icc、oth460_3l_icc |
| 情绪与新闻 | 8 | 1.00 | oth460_news_abno_sent_1d_class、oth460_news_abno_sent_1d_l1、oth460_news_abno_sent_1d_l2 |
| 元数据与非信号 | 4 | 1.00 | oth460_1l_vdav、oth460_2l_vdav、oth460_3l_vdav |
| 搜索与替代数据 | 1 | 1.00 | oth460_appy_class |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `oth460_float_to_l3` | MATRIX | 1.000 | 价量与波动 | 3 | 1.22 | 0.91 | 0.63 | WEAK | The probability that the future trend of Float Turnover, 12M" will be move-up" |
| 2 | `oth460_es_sale_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 2 | 0.07 | -0.07 | -0.14 | DEAD | The probability that the future trend of NTM Revenue Revision, 1M" will be move-up" |
| 3 | `oth460_divyld_bb_l3` | MATRIX | 1.000 | 盈利与财务 | 1 | 0.01 | -0.45 | 0.00 | DEAD | The probability that the future trend of Total Yield (Dividend + Share Change)" will be move-up" |
| 4 | `oth460_1l_dlts` | MATRIX | 1.000 | 盈利与财务 | 2 | -0.36 | -0.44 | -0.12 | DEAD | The probability that the future trend of 'Total Debt' will fall |
| 5 | `oth460_fincf_l1` | MATRIX | 1.000 | 盈利与财务 | 2 | -0.39 | -0.89 | -0.11 | DEAD_STATIC | The probability that the future trend of Financing Activities Net Cash Flow" will be fall" |
| 6 | `oth460_sopi_l3` | MATRIX | 1.000 | 其他 | 2 | -0.50 | -0.62 | -0.31 | DEAD | The probability that the future trend of Operating Income" will be move-up" |
| 7 | `oth460_viac_l3` | MATRIX | 1.000 | 其他 | 1 | -0.53 | -0.02 | -0.46 | DEAD | The probability that the future trend of Normalized Inc. Avail to Com." will move up" |
| 8 | `oth460_1l_01dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 10' will fall |
| 9 | `oth460_1l_1dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing Within 1 Year" will be fall" |
| 10 | `oth460_1l_1nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treas Shares - Common Stock Primary Issue" will fall" |
| 11 | `oth460_1l_1ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Shares Outstanding - Preferred Primary Issue' will fall |
| 12 | `oth460_1l_1ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Phase I' will fall |
| 13 | `oth460_1l_1spdd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of DPS - Common Stock Primary Issue" will fall" |
| 14 | `oth460_1l_1spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Special DPS - Common Stock Primary Issue' will fall |
| 15 | `oth460_1l_2dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 2" will fall" |
| 16 | `oth460_1l_2lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 2" will fall" |
| 17 | `oth460_1l_2nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Shares - Common Issue 2" will fall" |
| 18 | `oth460_1l_2ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Shares Outstanding - Preferred Issue 2" will be fall" |
| 19 | `oth460_1l_2ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Phase II' will fall |
| 20 | `oth460_1l_2spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Dividends per Share - Com Stock Issue 2" will be fall" |
| 21 | `oth460_1l_2spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special DPS - Common Stock Issue 2" will fall" |
| 22 | `oth460_1l_32lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in 2-3 Years' will fall |
| 23 | `oth460_1l_3dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-Term Debt Maturing in Year 3" will be fall" |
| 24 | `oth460_1l_3lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 3" will fall" |
| 25 | `oth460_1l_3ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Phase III' will fall |
| 26 | `oth460_1l_3spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Dividends per Share - Com Stock Issue 3" will fall" |
| 27 | `oth460_1l_4lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 4' will be fall |
| 28 | `oth460_1l_54dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-Term Debt Maturing in 4-5 Years" will be fall" |
| 29 | `oth460_1l_54lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in 4-5 Years' will fall |
| 30 | `oth460_1l_57_03_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Moving Average Crossover, 30W-75W" will be fall" |
| 31 | `oth460_1l_5dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 5" will be fall" |
| 32 | `oth460_1l_5lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 5" will fall" |
| 33 | `oth460_1l_63_51_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Moving Average Crossover, 15W-36W" will be fall" |
| 34 | `oth460_1l_7dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 7' will fall |
| 35 | `oth460_1l_8dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 8" will be fall" |
| 36 | `oth460_1l_abpo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Payable/Accrued' will fall |
| 37 | `oth460_1l_acda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Current Asset" will fall" |
| 38 | `oth460_1l_acf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Foreign Exchange Income (Loss)' will fall |
| 39 | `oth460_1l_acoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets' will fall |
| 40 | `oth460_1l_adbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized EBITDA" will be fall" |
| 41 | `oth460_1l_aemc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Miscellaneous Earnings Adjustment" will be fall" |
| 42 | `oth460_1l_aiec` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Equity in Affiliates' will fall |
| 43 | `oth460_1l_alge` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Loss(Gain) on Sale of Assets - Operating' will fall |
| 44 | `oth460_1l_algn` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Gain (Loss) on Sale of Assets" will fall" |
| 45 | `oth460_1l_algv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of (Gain) Loss on Sale of Assets, Suppl." will be a fall" |
| 46 | `oth460_1l_b6dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Matur. in Year 6 & Beyond" will be fall" |
| 47 | `oth460_1l_bb` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Bollinger Bands" will fall" |
| 48 | `oth460_1l_biis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Income, Bank" will fall" |
| 49 | `oth460_1l_bloo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Liabilities" will fall" |
| 50 | `oth460_1l_boie` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest on Other Borrowings" will be fall" |
| 51 | `oth460_1l_bpao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Accounts Payable' will fall |
| 52 | `oth460_1l_btsl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Short Term Borrowings' will fall |
| 53 | `oth460_1l_caic` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Available to Com Excl ExtraOrd" will fall" |
| 54 | `oth460_1l_cbbm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of EBITDAR" will fall" |
| 55 | `oth460_1l_ccns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Change in Cash" will fall" |
| 56 | `oth460_1l_cfda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Charges" will fall" |
| 57 | `oth460_1l_cifv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Interest Cost - Foreign' will fall |
| 58 | `oth460_1l_cinx` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Available to Com Incl ExtraOrd" will fall" |
| 59 | `oth460_1l_cniv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Costs" will fall" |
| 60 | `oth460_1l_csfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Service Cost - Foreign" will fall" |
| 61 | `oth460_1l_cspv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Service Cost - Post-Retirement" will fall" |
| 62 | `oth460_1l_ctcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Total" will be fall" |
| 63 | `oth460_1l_ctda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Income Tax - Current Asset" will fall" |
| 64 | `oth460_1l_ctdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Income Tax - Current Liability" will fall" |
| 65 | `oth460_1l_ctdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Total" will be fall" |
| 66 | `oth460_1l_d0252ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total return, past 120M" will fall" |
| 67 | `oth460_1l_d12ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total return, past 1M" will fall" |
| 68 | `oth460_1l_d36ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 3-month total return" will be fall" |
| 69 | `oth460_1l_dbtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Comp. Store Sales, Retail, Total - %' will fall |
| 70 | `oth460_1l_dcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Service Cost - Domestic' will fall |
| 71 | `oth460_1l_dlyspe_rh` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical relative earnings yield" will fall" |
| 72 | `oth460_1l_drpc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Preferred Dividends" will be fall" |
| 73 | `oth460_1l_drpf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Issuance (Retirement) of Debt, Net' will fall |
| 74 | `oth460_1l_dtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Domestic" will be fall" |
| 75 | `oth460_1l_dtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Domestic" will fall" |
| 76 | `oth460_1l_dtov` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Domestic Tax - Other' will fall |
| 77 | `oth460_1l_dtsl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Notes Payable/Short Term Debt" will be fall" |
| 78 | `oth460_1l_eaca` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Cash & Equivalents" will be fall" |
| 79 | `oth460_1l_ebbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Passengers, Total" will fall" |
| 80 | `oth460_1l_ecns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Cash - Ending Balance" will be fall" |
| 81 | `oth460_1l_eins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Non-Interest Expense, Bank" will fall" |
| 82 | `oth460_1l_eiue` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income)' will fall |
| 83 | `oth460_1l_eiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Expense" will be fall" |
| 84 | `oth460_1l_eiuo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unusual Items" will be fall" |
| 85 | `oth460_1l_eiuv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income), Suppl.' will fall |
| 86 | `oth460_1l_ejtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Value of Bookings" will fall" |
| 87 | `oth460_1l_eoos` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Operating Expenses, Total" will fall" |
| 88 | `oth460_1l_eprv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Post-Retirement Plan Expense" will be fall" |
| 89 | `oth460_1l_epts` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Expected Return" will be fall" |
| 90 | `oth460_1l_eptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Pension Expense" will fall" |
| 91 | `oth460_1l_epxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Post-Retirement, Net' will fall |
| 92 | `oth460_1l_erpm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products in Pre-Registration' will fall |
| 93 | `oth460_1l_etoq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Equity" will fall" |
| 94 | `oth460_1l_fmc` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Chaikin Money Flow' will fall |
| 95 | `oth460_1l_fotv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of All Other Fees" will be fall" |
| 96 | `oth460_1l_ftcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Foreign" will fall" |
| 97 | `oth460_1l_ftdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Foreign" will be fall" |
| 98 | `oth460_1l_fttv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Tax Fees" will fall" |
| 99 | `oth460_1l_gaxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Actuarial Gains and Losses - Domestic" will be fall" |
| 100 | `oth460_1l_gdbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Available Seat Kilometers (ASK)" will be fall" |
| 101 | `oth460_1l_ghc_qe_td_tl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of YoY change in long-term debt/common equity" will fall" |
| 102 | `oth460_1l_gjbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Expense per ASK" will fall" |
| 103 | `oth460_1l_htrm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Rent Growth (Sequential), Total -%" will fall" |
| 104 | `oth460_1l_iabs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Basic EPS Including Extraordinary Items" will be fall" |
| 105 | `oth460_1l_iads` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Diluted EPS Including ExtraOrd Items" will fall" |
| 106 | `oth460_1l_icc` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Commodity Channel Index" will be fall" |
| 107 | `oth460_1l_ifm` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Money Flow Index" will fall" |
| 108 | `oth460_1l_iins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Maturity of Investment" will be fall" |
| 109 | `oth460_1l_iirr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Reinsurance - Income' will fall |
| 110 | `oth460_1l_iiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Income" will fall" |
| 111 | `oth460_1l_im` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Mass Index" will fall" |
| 112 | `oth460_1l_inds` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Diluted Net Income" will be fall" |
| 113 | `oth460_1l_ips` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special Items" will fall" |
| 114 | `oth460_1l_ipts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Interest Cost" will be fall" |
| 115 | `oth460_1l_iscs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Cash and Short-Term Investments" will be fall" |
| 116 | `oth460_1l_isir` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest & Dividends on Investment Secs." will fall" |
| 117 | `oth460_1l_ist` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'True Strength Index' will fall |
| 118 | `oth460_1l_ists` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Special Items" will be fall" |
| 119 | `oth460_1l_itpv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized Income Before Taxes' will fall |
| 120 | `oth460_1l_iv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Vortex Indicator" will fall" |
| 121 | `oth460_1l_ivn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Negative Volume Index' will fall |
| 122 | `oth460_1l_ixts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Extraordinary Items' will fall |
| 123 | `oth460_1l_kcqs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Quick Ratio" will fall" |
| 124 | `oth460_1l_khtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Stores Opened' will fall |
| 125 | `oth460_1l_laoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Assets & Liabilities, Net" will fall" |
| 126 | `oth460_1l_lbtm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Merchandise Margins, Total -%" will fall" |
| 127 | `oth460_1l_lcdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Curr Liability" will be a fall" |
| 128 | `oth460_1l_lctv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Capital Leases, Supplemental" will fall" |
| 129 | `oth460_1l_lda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accumulation Distribution Line" will be fall" |
| 130 | `oth460_1l_ldav` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Revenue - Long Term" will be fall" |
| 131 | `oth460_1l_ldbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Load Factor, Total -%" will fall" |
| 132 | `oth460_1l_lgrr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Realized & Unrealized Gains (Losses)" will be fall" |
| 133 | `oth460_1l_lgsn` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Investment Securities Gains" will fall" |
| 134 | `oth460_1l_lguq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unrealized Gain (Loss)" will fall" |
| 135 | `oth460_1l_lppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Products Launched' will fall |
| 136 | `oth460_1l_ltcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Local" will fall" |
| 137 | `oth460_1l_ltdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Local" will be fall" |
| 138 | `oth460_1l_ltio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inventories" will fall" |
| 139 | `oth460_1l_ltll` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Liabilities' will fall |
| 140 | `oth460_1l_m1d_1yf_spb_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 BPS Diffusion (up/down ratio), 1M' will fall |
| 141 | `oth460_1l_m1d_1yf_spd_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 DPS Diffusion (up/down ratio), 1M" will be fall" |
| 142 | `oth460_1l_m1d_1yf_spe_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 EPS diffusion (up/down ratio), 1M' will fall |
| 143 | `oth460_1l_m1d_1yf_spfc_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 CFPS diffusion (up/down ratio), 1M' will fall |
| 144 | `oth460_1l_m1d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 NAV diffusion (up/down ratio), 1M" will be fall" |
| 145 | `oth460_1l_m1d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation diffusion (up/down ratio), 1M" will be fall" |
| 146 | `oth460_1l_m1d_gtl_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-term growth diffusion (up/down ratio), 1M" will be fall" |
| 147 | `oth460_1l_m1d_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Target price diffusion (up/down ratio), 1M' will fall |
| 148 | `oth460_1l_m1m21_ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Price Momentum, 12M-1M' will fall |
| 149 | `oth460_1l_m1r_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 BPS revision, 1M' will fall |
| 150 | `oth460_1l_m1r_1yf_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 DPS Revision, 1M" will fall" |
| 151 | `oth460_1l_m1r_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 EPS Revision, 1M' will be fall |
| 152 | `oth460_1l_m1r_1yf_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 CFPS Revision, 1M' will fall |
| 153 | `oth460_1l_m1r_1yf_van_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 NAV revision, 1M' will fall |
| 154 | `oth460_1l_m1r_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation Revision, 1M" will be fall" |
| 155 | `oth460_1l_m1r_gtl_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long-term Growth Revision, 1M' will be fall |
| 156 | `oth460_1l_m1r_mtn_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'NTM DPS revision, 1M' will fall |
| 157 | `oth460_1l_m1r_mtn_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EPS Revision, 1M" will fall" |
| 158 | `oth460_1l_m1r_mtn_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM CFPS Revision, 1M" will fall" |
| 159 | `oth460_1l_m1r_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Target Price Revision, 1M" will be fall" |
| 160 | `oth460_1l_m3d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 NAV Diffusion (Up/Down Ratio), 3M" will be fall" |
| 161 | `oth460_1l_m3d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation Diffusion (up/down ratio), 3M" will be fall" |
| 162 | `oth460_1l_m3r_mtn_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM BPS revision, 3M" will fall" |
| 163 | `oth460_1l_mocq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Comprehensive Income" will fall" |
| 164 | `oth460_1l_mpns` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Profit Margin' will fall |
| 165 | `oth460_1l_mtps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Pretax Margin" will be fall" |
| 166 | `oth460_1l_ndsf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Short Term Debt, Net" will fall" |
| 167 | `oth460_1l_niis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest/Invest Income - Non-Operating" will be fall" |
| 168 | `oth460_1l_nins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Inc.(Exp.),Net-Non-Op., Total" will fall" |
| 169 | `oth460_1l_nscf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Common Stock, Net' will fall |
| 170 | `oth460_1l_ntiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inc Tax Ex Impact of Sp Items" will fall" |
| 171 | `oth460_1l_nvii` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Investment, Net' will fall |
| 172 | `oth460_1l_oc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Chaikin Oscillator' will fall |
| 173 | `oth460_1l_ocl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Liabilities Other Total" will fall" |
| 174 | `oth460_1l_od` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations" will be fall" |
| 175 | `oth460_1l_oiis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest/Investment Income - Operating" will fall" |
| 176 | `oth460_1l_oinm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Interest Margin, Total -%" will be fall" |
| 177 | `oth460_1l_olcl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Obligations' will fall |
| 178 | `oth460_1l_ompd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'DecisionPoint Price Momentum Oscillator' will fall |
| 179 | `oth460_1l_opd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Detrended Price Oscillator' will fall |
| 180 | `oth460_1l_opp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Percentage Price Oscillator' will fall |
| 181 | `oth460_1l_optq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Preferred Shares Outstanding" will be fall" |
| 182 | `oth460_1l_opxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Pension, Net - Domestic' will fall |
| 183 | `oth460_1l_os` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Stochastic Oscillator" will be fall" |
| 184 | `oth460_1l_otcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Other" will be fall" |
| 185 | `oth460_1l_otdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Other" will fall" |
| 186 | `oth460_1l_ovp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Percentage Volume Oscillator" will be fall" |
| 187 | `oth460_1l_pcrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Repurch./Retirement of Common/Preferred" will be fall" |
| 188 | `oth460_1l_pcsf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Common/Preferred" will fall" |
| 189 | `oth460_1l_pcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Stock-Based Compensation, Supplemental' will fall |
| 190 | `oth460_1l_pffl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of FedFundsPurch/ScrtySoldUnderRepurchAgrmt" will be fall" |
| 191 | `oth460_1l_poer` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Electric Operations" will be fall" |
| 192 | `oth460_1l_ppdf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Cash Dividends Paid - Preferred" will be fall" |
| 193 | `oth460_1l_ppdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Domestic Pension Plan Expense" will be fall" |
| 194 | `oth460_1l_ppfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Foreign Pension Plan Expense' will fall |
| 195 | `oth460_1l_ppgs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Gross Margin" will fall" |
| 196 | `oth460_1l_prrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Repurchase/Retirement of Preferred" will fall" |
| 197 | `oth460_1l_pxtl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Taxes Payable" will fall" |
| 198 | `oth460_1l_qbbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Revenue Passenger Kilometers (RPK)" will be fall" |
| 199 | `oth460_1l_rcao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accounts Receivable" will be fall" |
| 200 | `oth460_1l_rinr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Non-Insurance Revenue" will fall" |
| 201 | `oth460_1l_rltr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Revenue" will be fall" |
| 202 | `oth460_1l_rpts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Other Expense" will fall" |
| 203 | `oth460_1l_rpul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unearned Premium/Unearned Revenue" will fall" |
| 204 | `oth460_1l_rta` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Average True Range" will fall" |
| 205 | `oth460_1l_rtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Current Tax - Total' will fall |
| 206 | `oth460_1l_rtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Total" will fall" |
| 207 | `oth460_1l_rw` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Williams %R' will fall |
| 208 | `oth460_1l_rxfv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Expected Return on Assets - Foreign" will be fall" |
| 209 | `oth460_1l_saie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Impairment-Assets Held for Sale' will fall |
| 210 | `oth460_1l_saoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Assets" will fall" |
| 211 | `oth460_1l_sern` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge' will fall |
| 212 | `oth460_1l_serv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge, Supplemental' will fall |
| 213 | `oth460_1l_spe_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical 5Y EPS Growth Trend" will be fall" |
| 214 | `oth460_1l_speo_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical 5Y Operating EPS Growth Trend" will fall" |
| 215 | `oth460_1l_spfc_rtnie_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of YoY expected interim CFPS growth" will fall" |
| 216 | `oth460_1l_spfc_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical 5Y CFPS growth trend" will fall" |
| 217 | `oth460_1l_spts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Service Cost" will fall" |
| 218 | `oth460_1l_sptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prior Service Cost - Domestic' will fall |
| 219 | `oth460_1l_sspf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Issuance (Retirement) of Stock, Net' will fall |
| 220 | `oth460_1l_stnr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Sales" will fall" |
| 221 | `oth460_1l_tait` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Income After Taxes" will be fall" |
| 222 | `oth460_1l_tbie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Income Before Taxes" will fall" |
| 223 | `oth460_1l_tcxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Curtailments & Settlements - Domestic" will fall" |
| 224 | `oth460_1l_tdbo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Taxes" will be fall" |
| 225 | `oth460_1l_tdtv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Domestic Tax' will fall |
| 226 | `oth460_1l_tftv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Tax" will fall" |
| 227 | `oth460_1l_toia` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inventories - Other" will be fall" |
| 228 | `oth460_1l_tpda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest-Earning Deposits" will fall" |
| 229 | `oth460_1l_tpv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Volume Price Trend' will fall |
| 230 | `oth460_1l_ttiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Tax - Total" will be fall" |
| 231 | `oth460_1l_uaie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Use" will be fall" |
| 232 | `oth460_1l_vbo` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of On Balance Volume" will fall" |
| 233 | `oth460_1l_vcwf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Warrants Converted" will be fall" |
| 234 | `oth460_1l_vdav` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The probability that the future trend of Advertising Expense, Supplemental" will be fall" |
| 235 | `oth460_1l_vlc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Close Location Value" will be fall" |
| 236 | `oth460_1l_vme` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Ease of Movement" will fall" |
| 237 | `oth460_1l_vnie` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Investment Income - Operating" will fall" |
| 238 | `oth460_1l_xeao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Accrued Expenses' will fall |
| 239 | `oth460_1l_xefe` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Fuel Expense' will fall |
| 240 | `oth460_1l_xeon` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Expense" will fall" |
| 241 | `oth460_1l_yppa` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prepaid Expenses' will fall |
| 242 | `oth460_1l_yppo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prepaid Expenses' will fall |
| 243 | `oth460_1l_zahm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Rooms" will fall" |
| 244 | `oth460_2l_01dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 10" will be neutral" |
| 245 | `oth460_2l_1dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing Within 1 Year" will be neutral" |
| 246 | `oth460_2l_1nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treas Shares - Common Stock Primary Issue" will be neutral" |
| 247 | `oth460_2l_1ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Shares Outstanding - Preferred Primary Issue" will be neutral" |
| 248 | `oth460_2l_1spdd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of DPS - Common Stock Primary Issue" will be neutral" |
| 249 | `oth460_2l_1spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special DPS - Common Stock Primary Issue" will be neutral" |
| 250 | `oth460_2l_2dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 2" will be neutral" |
| 251 | `oth460_2l_2lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 2" will be neutral" |
| 252 | `oth460_2l_2nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Shares - Common Issue 2" will be neutral" |
| 253 | `oth460_2l_2ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Shares Outstanding - Preferred Issue 2" will be neutral" |
| 254 | `oth460_2l_2ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Products in Phase II" will be neutral" |
| 255 | `oth460_2l_2spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Dividends per Share - Com Stock Issue 2" will be neutral" |
| 256 | `oth460_2l_2spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special DPS - Common Stock Issue 2" will be neutral" |
| 257 | `oth460_2l_32lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in 2-3 Years" will be neutral" |
| 258 | `oth460_2l_3dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-Term Debt Maturing in Year 3" will be neutral" |
| 259 | `oth460_2l_3lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 3' will be neutral |
| 260 | `oth460_2l_4lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 4" will be neutral" |
| 261 | `oth460_2l_54dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in 4-5 Years" will be neutral" |
| 262 | `oth460_2l_54lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in 4-5 Years" will be neutral" |
| 263 | `oth460_2l_57_03_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Moving Average Crossover, 30W-75W" will be neutral" |
| 264 | `oth460_2l_5dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 5" will be neutral" |
| 265 | `oth460_2l_5lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 5" will be neutral" |
| 266 | `oth460_2l_63_51_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Moving average crossover, 15W-36W" will be neutral" |
| 267 | `oth460_2l_7dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 7" will be neutral" |
| 268 | `oth460_2l_8dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 8" will be neutral" |
| 269 | `oth460_2l_abpo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Payable/Accrued" will be neutral" |
| 270 | `oth460_2l_acda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Current Asset" will be neutral" |
| 271 | `oth460_2l_acf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Exchange Income (Loss)" will be neutral" |
| 272 | `oth460_2l_acoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Current Assets" will be neutral" |
| 273 | `oth460_2l_adbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized EBITDA" will be neutral" |
| 274 | `oth460_2l_aemc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Miscellaneous Earnings Adjustment" will be neutral" |
| 275 | `oth460_2l_aiec` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Equity in Affiliates" will be neutral" |
| 276 | `oth460_2l_alge` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Loss(Gain) on Sale of Assets - Operating" will be neutral" |
| 277 | `oth460_2l_algn` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Gain (Loss) on Sale of Assets" will be neutral" |
| 278 | `oth460_2l_algv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of (Gain) Loss on Sale of Assets, Suppl." will be neutral" |
| 279 | `oth460_2l_b6dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Matur. in Year 6 & Beyond" will be neutral" |
| 280 | `oth460_2l_bb` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Bollinger Bands" will be neutral" |
| 281 | `oth460_2l_biis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Income, Bank" will be neutral" |
| 282 | `oth460_2l_bloo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Liabilities" will be neutral" |
| 283 | `oth460_2l_boie` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest on Other Borrowings" will be neutral" |
| 284 | `oth460_2l_bpao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accounts Payable" will be neutral" |
| 285 | `oth460_2l_btsl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Short Term Borrowings" will be neutral" |
| 286 | `oth460_2l_caic` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Available to Com Excl ExtraOrd" will be neutral" |
| 287 | `oth460_2l_ccns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Change in Cash" will be neutral" |
| 288 | `oth460_2l_cfda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Charges" will be neutral" |
| 289 | `oth460_2l_cifv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Cost - Foreign" will be neutral" |
| 290 | `oth460_2l_cinx` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Available to Com Incl ExtraOrd" will be neutral" |
| 291 | `oth460_2l_cspv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Service Cost - Post-Retirement" will be neutral" |
| 292 | `oth460_2l_ctcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Total" will be neutral" |
| 293 | `oth460_2l_ctda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Income Tax - Current Asset" will be neutral" |
| 294 | `oth460_2l_ctdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Income Tax - Current Liability" will be neutral" |
| 295 | `oth460_2l_ctdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Total" will be neutral" |
| 296 | `oth460_2l_d0252ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total return, past 120M" will be neutral" |
| 297 | `oth460_2l_d12ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Return, Past 1M" will be neutral" |
| 298 | `oth460_2l_d36ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 3-month total return" will be neutral" |
| 299 | `oth460_2l_dbtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Comp. Store Sales, Retail, Total - %" will be neutral" |
| 300 | `oth460_2l_dcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Service Cost - Domestic" will be neutral" |
| 301 | `oth460_2l_dlts` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Debt" will be neutral" |
| 302 | `oth460_2l_dlyspe_rh` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical relative earnings yield" will be neutral" |
| 303 | `oth460_2l_drpc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Preferred Dividends" will be neutral" |
| 304 | `oth460_2l_drpf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Issuance (Retirement) of Debt, Net" will be neutral" |
| 305 | `oth460_2l_dtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Domestic" will be neutral" |
| 306 | `oth460_2l_dtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Domestic" will be neutral" |
| 307 | `oth460_2l_dtov` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Domestic Tax - Other" will be neutral" |
| 308 | `oth460_2l_dtsl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Notes Payable/Short Term Debt" will be neutral" |
| 309 | `oth460_2l_eaca` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Cash & Equivalents" will be neutral" |
| 310 | `oth460_2l_ebbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Passengers, Total" will be neutral" |
| 311 | `oth460_2l_ecns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Cash - Ending Balance" will be neutral" |
| 312 | `oth460_2l_eins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Non-Interest Expense, Bank" will be neutral" |
| 313 | `oth460_2l_eiue` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Expense (Income)" will be neutral" |
| 314 | `oth460_2l_eiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Expense" will be neutral" |
| 315 | `oth460_2l_eiuo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unusual Items" will be neutral" |
| 316 | `oth460_2l_eiuv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Expense (Income), Suppl." will be neutral" |
| 317 | `oth460_2l_ejtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Value of Bookings" will be neutral" |
| 318 | `oth460_2l_eoos` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Operating Expenses, Total" will be neutral" |
| 319 | `oth460_2l_eprv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Post-Retirement Plan Expense" will be neutral" |
| 320 | `oth460_2l_epts` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Expected Return" will be neutral" |
| 321 | `oth460_2l_eptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Pension Expense" will be neutral" |
| 322 | `oth460_2l_epxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Post-Retirement, Net" will be neutral" |
| 323 | `oth460_2l_erpm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Products in Pre-Registration" will be neutral" |
| 324 | `oth460_2l_etoq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Equity" will be neutral" |
| 325 | `oth460_2l_fmc` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Chaikin Money Flow" will be neutral" |
| 326 | `oth460_2l_fotv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of All Other Fees" will be neutral" |
| 327 | `oth460_2l_ftcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Foreign" will be neutral" |
| 328 | `oth460_2l_ftdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Foreign" will be neutral" |
| 329 | `oth460_2l_gaxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Actuarial Gains and Losses - Domestic" will be neutral" |
| 330 | `oth460_2l_gdbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Available Seat Kilometers (ASK)" will be neutral" |
| 331 | `oth460_2l_ghc_qe_td_tl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of YoY change in long-term debt/common equity" will be neutral" |
| 332 | `oth460_2l_gjbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Expense per ASK" will be neutral" |
| 333 | `oth460_2l_iabs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Basic EPS Including Extraordinary Items" will be neutral" |
| 334 | `oth460_2l_iads` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Diluted EPS Including Extraordinary Items' will be neutral |
| 335 | `oth460_2l_icc` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Commodity Channel Index" will be neutral" |
| 336 | `oth460_2l_ifm` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Money Flow Index" will be neutral" |
| 337 | `oth460_2l_iins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Maturity of Investment" will be neutral" |
| 338 | `oth460_2l_iirr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Reinsurance - Income" will be neutral" |
| 339 | `oth460_2l_iiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Income" will be neutral" |
| 340 | `oth460_2l_im` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Mass Index" will be neutral" |
| 341 | `oth460_2l_inds` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Diluted Net Income" will be neutral" |
| 342 | `oth460_2l_ips` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special Items" will be neutral" |
| 343 | `oth460_2l_ipts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Interest Cost" will be neutral" |
| 344 | `oth460_2l_iscs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Cash and Short Term Investments" will be neutral" |
| 345 | `oth460_2l_isir` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest & Dividends on Investment Secs." will be neutral" |
| 346 | `oth460_2l_ist` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of True Strength Index" will be neutral" |
| 347 | `oth460_2l_ists` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Special Items" will be neutral" |
| 348 | `oth460_2l_itpv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized Income Before Taxes" will be neutral" |
| 349 | `oth460_2l_iv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Vortex Indicator" will be neutral" |
| 350 | `oth460_2l_ivn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Negative Volume Index" will be neutral" |
| 351 | `oth460_2l_ixts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Extraordinary Items" will be neutral" |
| 352 | `oth460_2l_kcqs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Quick Ratio" will be neutral" |
| 353 | `oth460_2l_khtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Stores Opened" will be neutral" |
| 354 | `oth460_2l_laoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Assets & Liabilities, Net" will be neutral" |
| 355 | `oth460_2l_lbtm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Merchandise Margins, Total -%" will be neutral" |
| 356 | `oth460_2l_lcdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Curr Liability" will be neutral" |
| 357 | `oth460_2l_lctv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Capital Leases, Supplemental" will be neutral" |
| 358 | `oth460_2l_lda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accumulation Distribution Line" will be neutral" |
| 359 | `oth460_2l_ldav` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Revenue - Long Term" will be neutral" |
| 360 | `oth460_2l_lgrr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Realized & Unrealized Gains (Losses)" will be neutral" |
| 361 | `oth460_2l_lgsn` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Investment Securities Gains" will be neutral" |
| 362 | `oth460_2l_lguq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unrealized Gain (Loss)" will be neutral" |
| 363 | `oth460_2l_ltio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inventories" will be neutral" |
| 364 | `oth460_2l_ltll` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Liabilities" will be neutral" |
| 365 | `oth460_2l_m1d_1yf_spb_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 BPS diffusion (up/down ratio), 1M" will be neutral" |
| 366 | `oth460_2l_m1d_1yf_spd_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 DPS diffusion (up/down ratio), 1M" will be neutral" |
| 367 | `oth460_2l_m1d_1yf_spe_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EPS diffusion (up/down ratio), 1M" will be neutral" |
| 368 | `oth460_2l_m1d_1yf_spfc_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 CFPS diffusion (up/down ratio), 1M" will be neutral" |
| 369 | `oth460_2l_m1d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 NAV diffusion (up/down ratio), 1M" will be neutral" |
| 370 | `oth460_2l_m1d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation diffusion (up/down ratio), 1M" will be neutral" |
| 371 | `oth460_2l_m1d_gtl_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-term Growth Diffusion (up/down ratio), 1M" will be neutral" |
| 372 | `oth460_2l_m1d_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Target Price Diffusion (Up/Down Ratio), 1M" will be neutral" |
| 373 | `oth460_2l_m1m21_ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Price Momentum, 12M-1M" will be neutral" |
| 374 | `oth460_2l_m1r_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 BPS revision, 1M" will be neutral" |
| 375 | `oth460_2l_m1r_1yf_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 DPS revision, 1M" will be neutral" |
| 376 | `oth460_2l_m1r_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EPS Revision, 1M" will be neutral" |
| 377 | `oth460_2l_m1r_1yf_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 CFPS revision, 1M" will be neutral" |
| 378 | `oth460_2l_m1r_1yf_van_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 NAV revision, 1M" will be neutral" |
| 379 | `oth460_2l_m1r_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation revision, 1M" will be neutral" |
| 380 | `oth460_2l_m1r_gtl_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-term growth revision, 1M" will be neutral" |
| 381 | `oth460_2l_m1r_mtn_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM DPS Revision, 1M" will be neutral" |
| 382 | `oth460_2l_m1r_mtn_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EPS Revision, 1M" will be neutral" |
| 383 | `oth460_2l_m1r_mtn_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM CFPS revision, 1M" will be neutral" |
| 384 | `oth460_2l_m1r_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Target Price Revision, 1M" will be neutral" |
| 385 | `oth460_2l_m3d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 NAV diffusion (up/down ratio), 3M" will be neutral" |
| 386 | `oth460_2l_m3d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation Diffusion (Up/Down Ratio), 3M" will be neutral" |
| 387 | `oth460_2l_m3r_mtn_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM BPS Revision, 3M" will be neutral" |
| 388 | `oth460_2l_mocq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Comprehensive Income" will be neutral" |
| 389 | `oth460_2l_mpns` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Profit Margin" will be neutral" |
| 390 | `oth460_2l_mtps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Pretax Margin" will be neutral" |
| 391 | `oth460_2l_ndsf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Short-term Debt, Net" will be neutral" |
| 392 | `oth460_2l_niis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest/Invest Income - Non-Operating" will be neutral" |
| 393 | `oth460_2l_nins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Inc.(Exp.), Net-Non-Op., Total" will be neutral" |
| 394 | `oth460_2l_nscf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Common Stock, Net" will be neutral" |
| 395 | `oth460_2l_ntiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inc Tax Ex Impact of Sp Items" will be neutral" |
| 396 | `oth460_2l_nvii` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Investment, Net" will be neutral" |
| 397 | `oth460_2l_oc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Chaikin Oscillator" will be neutral" |
| 398 | `oth460_2l_ocl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Liabilities Other Total" will be neutral" |
| 399 | `oth460_2l_od` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations" will be neutral" |
| 400 | `oth460_2l_oiis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest/Investment Income - Operating" will be neutral" |
| 401 | `oth460_2l_oinm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Interest Margin, Total -%" will be neutral" |
| 402 | `oth460_2l_olcl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Obligations" will be neutral" |
| 403 | `oth460_2l_ompd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of DecisionPoint Price Momentum Oscillator" will be neutral" |
| 404 | `oth460_2l_opd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Detrended Price Oscillator" will be neutral" |
| 405 | `oth460_2l_opp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Percentage Price Oscillator" will be neutral" |
| 406 | `oth460_2l_optq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Preferred Shares Outstanding" will be neutral" |
| 407 | `oth460_2l_opxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Pension, Net - Domestic" will be neutral" |
| 408 | `oth460_2l_os` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Stochastic Oscillator" will be neutral" |
| 409 | `oth460_2l_otcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Other" will be neutral" |
| 410 | `oth460_2l_otdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Other" will be neutral" |
| 411 | `oth460_2l_ovp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Percentage Volume Oscillator" will be neutral" |
| 412 | `oth460_2l_pcrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Repurch./Retirement of Common/Preferred" will be neutral" |
| 413 | `oth460_2l_pcsf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Common/Preferred" will be neutral" |
| 414 | `oth460_2l_pcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Stock-Based Compensation, Supplemental" will be neutral" |
| 415 | `oth460_2l_pffl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of FedFundsPurch/ScrtySoldUnderRepurchAgrmt" will be neutral" |
| 416 | `oth460_2l_poer` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Electric Operations" will be neutral" |
| 417 | `oth460_2l_ppdf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Cash Dividends Paid - Preferred" will be neutral" |
| 418 | `oth460_2l_ppdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Domestic Pension Plan Expense" will be neutral" |
| 419 | `oth460_2l_ppfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Pension Plan Expense" will be neutral" |
| 420 | `oth460_2l_ppgs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Gross Margin" will be neutral" |
| 421 | `oth460_2l_prrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Repurchase/Retirement of Preferred" will be neutral" |
| 422 | `oth460_2l_pxtl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Taxes Payable" will be neutral" |
| 423 | `oth460_2l_rcao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accounts Receivable" will be neutral" |
| 424 | `oth460_2l_rinr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Non-Insurance Revenue" will be neutral" |
| 425 | `oth460_2l_rltr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Revenue" will be neutral" |
| 426 | `oth460_2l_rpts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Other Expense" will be neutral" |
| 427 | `oth460_2l_rpul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unearned Premium/Unearned Revenue" will be neutral" |
| 428 | `oth460_2l_rta` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Average True Range" will be neutral" |
| 429 | `oth460_2l_rtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Total" will be neutral" |
| 430 | `oth460_2l_rtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Total" will be neutral" |
| 431 | `oth460_2l_rw` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Williams %R" will be neutral" |
| 432 | `oth460_2l_saie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Sale" will be neutral" |
| 433 | `oth460_2l_saoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Assets" will be neutral" |
| 434 | `oth460_2l_sern` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Restructuring Charge" will be neutral" |
| 435 | `oth460_2l_serv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Restructuring Charge, Supplemental" will be neutral" |
| 436 | `oth460_2l_spe_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Historical 5Y EPS Growth Trend' will be neutral |
| 437 | `oth460_2l_speo_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical 5Y Operating EPS Growth Trend" will be neutral" |
| 438 | `oth460_2l_spfc_rtnie_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of YoY expected interim CFPS growth" will be neutral" |
| 439 | `oth460_2l_spfc_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical 5Y CFPS Growth Trend" will be neutral" |
| 440 | `oth460_2l_spts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Service Cost" will be neutral" |
| 441 | `oth460_2l_sspf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Issuance (Retirement) of Stock, Net" will be neutral" |
| 442 | `oth460_2l_stnr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Sales" will be neutral" |
| 443 | `oth460_2l_tait` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Income After Taxes" will be neutral" |
| 444 | `oth460_2l_tbie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Income Before Taxes" will be neutral" |
| 445 | `oth460_2l_tdbo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Taxes" will be neutral" |
| 446 | `oth460_2l_tdtv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Domestic Tax" will be neutral" |
| 447 | `oth460_2l_tftv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Tax" will be neutral" |
| 448 | `oth460_2l_toia` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inventories - Other" will be neutral" |
| 449 | `oth460_2l_tpda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest-Earning Deposits" will be neutral" |
| 450 | `oth460_2l_tpv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Volume Price Trend" will be neutral" |
| 451 | `oth460_2l_ttiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Tax - Total" will be neutral" |
| 452 | `oth460_2l_uaie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Use" will be neutral" |
| 453 | `oth460_2l_vbo` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'On-Balance Volume' will be neutral |
| 454 | `oth460_2l_vcwf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Warrants Converted" will be neutral" |
| 455 | `oth460_2l_vdav` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The probability that the future trend of Advertising Expense, Supplemental" will be neutral" |
| 456 | `oth460_2l_vlc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Close Location Value" will be neutral" |
| 457 | `oth460_2l_vme` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Ease of Movement" will be neutral" |
| 458 | `oth460_2l_vnie` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Investment Income - Operating" will be neutral" |
| 459 | `oth460_2l_xeao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accrued Expenses" will be neutral" |
| 460 | `oth460_2l_xefe` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Fuel Expense" will be neutral" |
| 461 | `oth460_2l_xeon` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Expense" will be neutral" |
| 462 | `oth460_2l_yppa` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Prepaid Expenses" will be neutral" |
| 463 | `oth460_2l_yppo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Prepaid Expenses" will be neutral" |
| 464 | `oth460_2l_zahm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Rooms" will be neutral" |
| 465 | `oth460_3l_01dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 10' will move up |
| 466 | `oth460_3l_1dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing within 1 Year" will be move-up" |
| 467 | `oth460_3l_1nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treas Shares - Common Stock Prmry Issue" will move up" |
| 468 | `oth460_3l_1ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Shares Outstanding - Preferred Primary Issue' will move up |
| 469 | `oth460_3l_1ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Products in Phase I" will be move-up" |
| 470 | `oth460_3l_1spdd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'DPS - Common Stock Primary Issue' will move up |
| 471 | `oth460_3l_1spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special DPS - Common Stock Primary Issue" will move up" |
| 472 | `oth460_3l_2dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Maturing in Year 2" will be move-up" |
| 473 | `oth460_3l_2lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 2" will be move-up" |
| 474 | `oth460_3l_2nstq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Shares - Common Issue 2" will move up" |
| 475 | `oth460_3l_2ospq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Shares Outstanding - Preferred Issue 2" will be move-up" |
| 476 | `oth460_3l_2ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Products in Phase II" will move up" |
| 477 | `oth460_3l_2spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Dividends per Share - Com Stock Issue 2' will move up |
| 478 | `oth460_3l_2spsd` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special DPS - Common Stock Issue 2" will be move-up" |
| 479 | `oth460_3l_32lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in 2-3 Years" will be move-up" |
| 480 | `oth460_3l_3dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 3' will be move-up |
| 481 | `oth460_3l_3lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 3' will move up |
| 482 | `oth460_3l_3ppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Products in Phase III" will be move-up" |
| 483 | `oth460_3l_3spdd` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Dividends per Share - Com Stock Issue 3' will move up |
| 484 | `oth460_3l_4lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in Year 4" will be move-up" |
| 485 | `oth460_3l_54dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in 4-5 Years' will move up |
| 486 | `oth460_3l_54lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Payments Due in 4-5 Years" will be move-up" |
| 487 | `oth460_3l_57_03_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Moving Average Crossover, 30W-75W' will be move-up |
| 488 | `oth460_3l_5dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 5' will move up |
| 489 | `oth460_3l_5lcs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Capital Lease Payments Due in Year 5' will move up |
| 490 | `oth460_3l_63_51_am` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Moving average crossover, 15W-36W' will move up |
| 491 | `oth460_3l_7dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 7' will move up |
| 492 | `oth460_3l_8dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Long Term Debt Maturing in Year 8' will move up |
| 493 | `oth460_3l_abpo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Payable/Accrued' will move up |
| 494 | `oth460_3l_acda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Current Asset" will move up" |
| 495 | `oth460_3l_acf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Foreign Exchange Income (Loss)' will move up |
| 496 | `oth460_3l_acoa` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets' will move up |
| 497 | `oth460_3l_adbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized EBITDA' will move up |
| 498 | `oth460_3l_aemc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Miscellaneous Earnings Adjustment" will be move-up" |
| 499 | `oth460_3l_aiec` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Equity in Affiliates' will move up |
| 500 | `oth460_3l_alge` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Loss (Gain) on Sale of Assets - Operating" will be move-up" |
| 501 | `oth460_3l_algn` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Gain (Loss) on Sale of Assets" will move up" |
| 502 | `oth460_3l_algv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of (Gain) Loss on Sale of Assets, Suppl." will move up" |
| 503 | `oth460_3l_b6dls` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long Term Debt Matur. in Year 6 & Beyond" will be move-up" |
| 504 | `oth460_3l_bb` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Bollinger Bands' will move up |
| 505 | `oth460_3l_biis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Income, Bank" will be move-up" |
| 506 | `oth460_3l_bloo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Liabilities" will be move-up" |
| 507 | `oth460_3l_boie` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest on Other Borrowings" will be move-up" |
| 508 | `oth460_3l_bpao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accounts Payable" will be move-up" |
| 509 | `oth460_3l_btsl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Short Term Borrowings" will be move-up" |
| 510 | `oth460_3l_caic` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Available to Com Excl ExtraOrd" will move up" |
| 511 | `oth460_3l_cbbm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of EBITDAR" will move up" |
| 512 | `oth460_3l_ccns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Change in Cash" will move up" |
| 513 | `oth460_3l_cfda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Charges" will be move-up" |
| 514 | `oth460_3l_cifv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Cost - Foreign" will move up" |
| 515 | `oth460_3l_cinx` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Available to Com Incl ExtraOrd" will move up" |
| 516 | `oth460_3l_cniv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Costs" will be move-up" |
| 517 | `oth460_3l_csfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Service Cost - Foreign' will move up |
| 518 | `oth460_3l_cspv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Service Cost - Post-Retirement" will be move-up" |
| 519 | `oth460_3l_ctcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Total" will be move-up" |
| 520 | `oth460_3l_ctda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Income Tax - Current Asset" will be move-up" |
| 521 | `oth460_3l_ctdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Deferred Income Tax - Current Liability' will move up |
| 522 | `oth460_3l_ctdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Total" will be move-up" |
| 523 | `oth460_3l_d0252ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total return, past 120M" will move up" |
| 524 | `oth460_3l_d12ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Return, Past 1M" will be move-up" |
| 525 | `oth460_3l_d36ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 3-month total return" will move up" |
| 526 | `oth460_3l_dbtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Comp. Store Sales, Retail, Total - %" will move up" |
| 527 | `oth460_3l_dcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Service Cost - Domestic" will move up" |
| 528 | `oth460_3l_dlts` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Debt' will move up |
| 529 | `oth460_3l_dlyspe_rh` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Historical relative earnings yield' will move up |
| 530 | `oth460_3l_drpc` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Preferred Dividends" will be move-up" |
| 531 | `oth460_3l_drpf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Issuance (Retirement) of Debt, Net" will move up" |
| 532 | `oth460_3l_dtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Domestic" will move up" |
| 533 | `oth460_3l_dtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Domestic" will be move-up" |
| 534 | `oth460_3l_dtov` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Domestic Tax - Other' will move up |
| 535 | `oth460_3l_dtsl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Notes Payable/Short Term Debt' will move up |
| 536 | `oth460_3l_eaca` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Cash & Equivalents" will move up" |
| 537 | `oth460_3l_ebbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Passengers, Total" will move up" |
| 538 | `oth460_3l_ecns` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Cash - Ending Balance' will move up |
| 539 | `oth460_3l_eins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Non-Interest Expense, Bank" will be move-up" |
| 540 | `oth460_3l_eiue` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income)' will move up |
| 541 | `oth460_3l_eiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Expense" will move up" |
| 542 | `oth460_3l_eiuo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unusual Items" will move up" |
| 543 | `oth460_3l_eiuv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Unusual Expense (Income), Suppl.' will move up |
| 544 | `oth460_3l_ejtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Value of Bookings" will move up" |
| 545 | `oth460_3l_eoos` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Operating Expenses, Total" will be move-up" |
| 546 | `oth460_3l_eprv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Post-Retirement Plan Expense' will move up |
| 547 | `oth460_3l_epts` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Expected Return" will be move-up" |
| 548 | `oth460_3l_eptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Pension Expense" will move up" |
| 549 | `oth460_3l_epxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Post-Retirement, Net" will be move-up" |
| 550 | `oth460_3l_erpm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Products in Pre-Registration" will move up" |
| 551 | `oth460_3l_etoq` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Equity" will move up" |
| 552 | `oth460_3l_fmc` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Chaikin Money Flow" will be move-up" |
| 553 | `oth460_3l_fotv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of All Other Fees" will be move-up" |
| 554 | `oth460_3l_ftcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Foreign" will move up" |
| 555 | `oth460_3l_ftdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Deferred Tax - Foreign' will move up |
| 556 | `oth460_3l_fttv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Tax Fees' will move up |
| 557 | `oth460_3l_gaxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Actuarial Gains and Losses - Domestic" will be move-up" |
| 558 | `oth460_3l_gdbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Available Seat Kilometers (ASK)" will be move-up" |
| 559 | `oth460_3l_ghc_qe_td_tl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of YoY Change in Long-Term Debt/Common Equity" will move up" |
| 560 | `oth460_3l_gjbs` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Expense per ASK" will move up" |
| 561 | `oth460_3l_htrm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Rent Growth (Sequential), Total -%" will move up" |
| 562 | `oth460_3l_iabs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Basic EPS Including Extraordinary Items" will move up" |
| 563 | `oth460_3l_iads` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Diluted EPS Including Extraordinary Items" will move up" |
| 564 | `oth460_3l_icc` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Commodity Channel Index" will be move-up" |
| 565 | `oth460_3l_ifm` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Money Flow Index" will be move-up" |
| 566 | `oth460_3l_iins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Maturity of Investment" will move up" |
| 567 | `oth460_3l_iirr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Reinsurance - Income' will move up |
| 568 | `oth460_3l_iiun` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Unusual Income" will move up" |
| 569 | `oth460_3l_im` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Mass Index" will move up" |
| 570 | `oth460_3l_inds` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Diluted Net Income" will move up" |
| 571 | `oth460_3l_ips` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Special Items" will be move-up" |
| 572 | `oth460_3l_ipts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Interest Cost" will move up" |
| 573 | `oth460_3l_iscs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Cash and Short-Term Investments' will be move-up |
| 574 | `oth460_3l_isir` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest & Dividends on Investment Secs." will be move-up" |
| 575 | `oth460_3l_ist` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of True Strength Index" will be move-up" |
| 576 | `oth460_3l_ists` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Special Items" will be move-up" |
| 577 | `oth460_3l_itpv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized Income Before Taxes" will move up" |
| 578 | `oth460_3l_iv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Vortex Indicator' will move up |
| 579 | `oth460_3l_ivn` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Negative Volume Index' will move up |
| 580 | `oth460_3l_ixts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Extraordinary Items" will be move-up" |
| 581 | `oth460_3l_kcqs` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Quick Ratio' will move up |
| 582 | `oth460_3l_khtm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Stores Opened" will be move-up" |
| 583 | `oth460_3l_laoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Assets & Liabilities, Net' will move up |
| 584 | `oth460_3l_lbtm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Merchandise Margins, Total -%" will be move-up" |
| 585 | `oth460_3l_lcdl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Curr Liability" will be move-up" |
| 586 | `oth460_3l_lctv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Capital Leases, Supplemental" will move up" |
| 587 | `oth460_3l_lda` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accumulation Distribution Line" will be move-up" |
| 588 | `oth460_3l_ldav` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Revenue - Long Term" will be move-up" |
| 589 | `oth460_3l_ldbm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Load Factor, Total -%" will move up" |
| 590 | `oth460_3l_lgrr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Realized & Unrealized Gains (Losses)" will move up" |
| 591 | `oth460_3l_lgsn` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Investment Securities Gains" will be move-up" |
| 592 | `oth460_3l_lguq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unrealized Gain (Loss)" will be move-up" |
| 593 | `oth460_3l_lppm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Products Launched" will be move-up" |
| 594 | `oth460_3l_ltcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Local" will be move-up" |
| 595 | `oth460_3l_ltdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Local" will move up" |
| 596 | `oth460_3l_ltio` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Inventories' will move up |
| 597 | `oth460_3l_ltll` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Liabilities" will move up" |
| 598 | `oth460_3l_m1d_1yf_spb_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 BPS diffusion (up/down ratio), 1M' will move up |
| 599 | `oth460_3l_m1d_1yf_spd_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 DPS diffusion (up/down ratio), 1M' will be move-up |
| 600 | `oth460_3l_m1d_1yf_spe_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EPS diffusion (up/down ratio), 1M" will move up" |
| 601 | `oth460_3l_m1d_1yf_spfc_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 CFPS diffusion (up/down ratio), 1M" will be move-up" |
| 602 | `oth460_3l_m1d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 NAV Diffusion (up/down ratio), 1M" will move up" |
| 603 | `oth460_3l_m1d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation diffusion (up/down ratio), 1M" will be move-up" |
| 604 | `oth460_3l_m1d_gtl_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-Term Growth Diffusion (Up/Down Ratio), 1M" will be move-up" |
| 605 | `oth460_3l_m1d_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Target price diffusion (up/down ratio), 1M" will be move-up" |
| 606 | `oth460_3l_m1m21_ntr` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Price Momentum, 12M-1M" will be move-up" |
| 607 | `oth460_3l_m1r_1yf_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 BPS Revision, 1M" will be move up" |
| 608 | `oth460_3l_m1r_1yf_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 DPS revision, 1M" will move up" |
| 609 | `oth460_3l_m1r_1yf_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EPS Revision, 1M" will be move-up" |
| 610 | `oth460_3l_m1r_1yf_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 CFPS revision, 1M' will move up |
| 611 | `oth460_3l_m1r_1yf_van_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 NAV revision, 1M' will move up |
| 612 | `oth460_3l_m1r_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation Revision, 1M" will be move-up" |
| 613 | `oth460_3l_m1r_gtl_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Long-Term Growth Revision, 1M" will be move-up" |
| 614 | `oth460_3l_m1r_mtn_spd_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM DPS revision, 1M" will move up" |
| 615 | `oth460_3l_m1r_mtn_spe_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EPS revision, 1M" will move up" |
| 616 | `oth460_3l_m1r_mtn_spfc_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM CFPS revision, 1M" will move up" |
| 617 | `oth460_3l_m1r_pt_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Target price revision, 1M" will move up" |
| 618 | `oth460_3l_m3d_1yf_van_se` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 NAV diffusion (up/down ratio), 3M' will move up |
| 619 | `oth460_3l_m3d_cer_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Recommendation diffusion (up/down ratio), 3M" will move up" |
| 620 | `oth460_3l_m3r_mtn_spb_se` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM BPS Revision, 3M" will move up" |
| 621 | `oth460_3l_mocq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Comprehensive Income" will be move-up" |
| 622 | `oth460_3l_mpns` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Profit Margin" will move up" |
| 623 | `oth460_3l_mtps` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Pretax Margin' will move up |
| 624 | `oth460_3l_ndsf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Short Term Debt, Net" will be move-up" |
| 625 | `oth460_3l_niis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest/Invest Income - Non-Operating" will move up" |
| 626 | `oth460_3l_nins` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Inc. (Exp.), Net-Non-Op., Total" will be move-up" |
| 627 | `oth460_3l_nscf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Common Stock, Net" will move up" |
| 628 | `oth460_3l_ntiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inc Tax Ex Impact of Sp Items" will be move-up" |
| 629 | `oth460_3l_nvii` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Investment, Net' will move up |
| 630 | `oth460_3l_oc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Chaikin Oscillator" will move up" |
| 631 | `oth460_3l_ocl` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Liabilities Other Total" will move up" |
| 632 | `oth460_3l_od` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Discontinued Operations' will move up |
| 633 | `oth460_3l_oiis` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest/Investment Income - Operating" will be move-up" |
| 634 | `oth460_3l_oinm` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Interest Margin, Total -%" will be move-up" |
| 635 | `oth460_3l_olcl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Capital Lease Obligations" will be move-up" |
| 636 | `oth460_3l_ompd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of DecisionPoint Price Momentum Oscillator" will move up" |
| 637 | `oth460_3l_opd` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Detrended Price Oscillator' will move up |
| 638 | `oth460_3l_opp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Percentage Price Oscillator" will be move-up" |
| 639 | `oth460_3l_optq` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Preferred Shares Outstanding' will move up |
| 640 | `oth460_3l_opxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Pension, Net - Domestic' will move up |
| 641 | `oth460_3l_os` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Stochastic Oscillator" will move up" |
| 642 | `oth460_3l_otcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Other" will move up" |
| 643 | `oth460_3l_otdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Other" will be move-up" |
| 644 | `oth460_3l_ovp` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Percentage Volume Oscillator" will move up" |
| 645 | `oth460_3l_pcrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Repurch./Retirement of Common/Preferred" will move up" |
| 646 | `oth460_3l_pcsf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Common/Preferred" will be move-up" |
| 647 | `oth460_3l_pcsv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Stock-Based Compensation, Supplemental" will move up" |
| 648 | `oth460_3l_pffl` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of FedFundsPurch/ScrtySoldUnderRepurchAgrmt" will be move-up" |
| 649 | `oth460_3l_poer` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Electric Operations" will be move-up" |
| 650 | `oth460_3l_ppdf` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Cash Dividends Paid - Preferred' will move up |
| 651 | `oth460_3l_ppdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Domestic Pension Plan Expense" will move up" |
| 652 | `oth460_3l_ppfv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Pension Plan Expense" will move up" |
| 653 | `oth460_3l_ppgs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Gross Margin" will move up" |
| 654 | `oth460_3l_prrf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Repurchase/Retirement of Preferred' will move up |
| 655 | `oth460_3l_pxtl` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Taxes Payable" will move up" |
| 656 | `oth460_3l_qbbs` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Revenue Passenger Kilometers (RPK)" will be move-up" |
| 657 | `oth460_3l_rcao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accounts Receivable" will move up" |
| 658 | `oth460_3l_rinr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Non-Insurance Revenue" will be move-up" |
| 659 | `oth460_3l_rltr` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Revenue" will be move-up" |
| 660 | `oth460_3l_rpts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Other Expense" will move up" |
| 661 | `oth460_3l_rpul` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Unearned Premium/Unearned Revenue' will move up |
| 662 | `oth460_3l_rta` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Average True Range" will move up" |
| 663 | `oth460_3l_rtcv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Tax - Total" will move up" |
| 664 | `oth460_3l_rtdv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Tax - Total" will be move-up" |
| 665 | `oth460_3l_rw` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Williams %R" will move up" |
| 666 | `oth460_3l_rxfv` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Expected Return on Assets - Foreign' will move up |
| 667 | `oth460_3l_saie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Sale" will be move-up" |
| 668 | `oth460_3l_saoo` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Assets" will be move-up" |
| 669 | `oth460_3l_sern` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge' will move up |
| 670 | `oth460_3l_serv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Restructuring Charge, Supplemental" will move up" |
| 671 | `oth460_3l_spe_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical 5Y EPS growth trend" will move up" |
| 672 | `oth460_3l_speo_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Historical 5Y operating EPS growth trend' will move up |
| 673 | `oth460_3l_spfc_rtnie_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of YoY expected interim CFPS growth" will move up" |
| 674 | `oth460_3l_spfc_y5_rg` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Historical 5Y CFPS growth trend" will be move up" |
| 675 | `oth460_3l_spts` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Plan Service Cost" will be move-up" |
| 676 | `oth460_3l_sptv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Prior Service Cost - Domestic" will move up" |
| 677 | `oth460_3l_sspf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Issuance (Retirement) of Stock, Net" will move up" |
| 678 | `oth460_3l_stnr` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Sales' will move up |
| 679 | `oth460_3l_tait` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net Income After Taxes" will move up" |
| 680 | `oth460_3l_tbie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Net Income Before Taxes' will move up |
| 681 | `oth460_3l_tcxv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Curtailments & Settlements - Domestic" will move up" |
| 682 | `oth460_3l_tdbo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Deferred Taxes" will move up" |
| 683 | `oth460_3l_tdtv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Domestic Tax" will move up" |
| 684 | `oth460_3l_tftv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Tax" will move up" |
| 685 | `oth460_3l_toia` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Inventories - Other" will be move-up" |
| 686 | `oth460_3l_tpda` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest-Earning Deposits" will move up" |
| 687 | `oth460_3l_tpv` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Volume Price Trend" will move up" |
| 688 | `oth460_3l_ttiv` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Tax - Total" will move up" |
| 689 | `oth460_3l_uaie` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Impairment-Assets Held for Use' will move up |
| 690 | `oth460_3l_vbo` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of On Balance Volume" will move up" |
| 691 | `oth460_3l_vcwf` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Warrants Converted" will move up" |
| 692 | `oth460_3l_vdav` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Advertising Expense, Supplemental' will move up |
| 693 | `oth460_3l_vlc` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Close Location Value" will be move-up" |
| 694 | `oth460_3l_vme` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Ease of Movement" will be move-up" |
| 695 | `oth460_3l_vnie` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Investment Income - Operating" will move up" |
| 696 | `oth460_3l_xeao` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accrued Expenses" will move up" |
| 697 | `oth460_3l_xefe` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Fuel Expense' will move up |
| 698 | `oth460_3l_xeon` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Expense' will move up |
| 699 | `oth460_3l_yppa` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Prepaid Expenses" will be move-up" |
| 700 | `oth460_3l_yppo` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Prepaid Expenses' will move up |
| 701 | `oth460_3l_zahm` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Rooms" will move up" |
| 702 | `oth460_abn_volm_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Abnormal Volume" (1: fall, 2: neutral, 3: move up)" |
| 703 | `oth460_abn_volm_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal Volume" will fall" |
| 704 | `oth460_abn_volm_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal Volume" will be neutral" |
| 705 | `oth460_abn_volm_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Abnormal Volume' will move up |
| 706 | `oth460_acae_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Cash & Equivalents" (1: fall, 2: neutral, 3: move-up)" |
| 707 | `oth460_adca_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Discontinued Operations - Current Asset" (1: fall, 2: neutral, 3: move-up)" |
| 708 | `oth460_adfc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Charges" (1: fall, 2: neutral, 3: move up)" |
| 709 | `oth460_adl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Accumulation Distribution Line" (1: fall, 2: neutral, 3: move-up)" |
| 710 | `oth460_adoa_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Discontinued Operations - LT Asset' (1: fall, 2: neutral, 3: move up) |
| 711 | `oth460_adoa_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - LT Asset" will fall" |
| 712 | `oth460_adoa_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - LT Asset" will be neutral" |
| 713 | `oth460_adoa_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - LT Asset" will move up" |
| 714 | `oth460_adpt_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Interest-Earning Deposits" (1: fall, 2: neutral, 3: move-up)" |
| 715 | `oth460_adtc_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Income Tax - Current Asset" (1: fall, 2: neutral, 3: move up)" |
| 716 | `oth460_aiot_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Inventories - Other" (1: fall, 2: neutral, 3: move up)" |
| 717 | `oth460_amihud_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Amihud illiquidity" (1: fall, 2: neutral, 3: move-up)" |
| 718 | `oth460_amihud_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amihud illiquidity" will be fall" |
| 719 | `oth460_amihud_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amihud Illiquidity" will be neutral" |
| 720 | `oth460_amihud_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amihud illiquidity" will be move-up" |
| 721 | `oth460_aoca_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Current Assets" (1: fall, 2: neutral, 3: move-up)" |
| 722 | `oth460_aorc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Receivables - Other' (1: fall, 2: neutral, 3: move up) |
| 723 | `oth460_aorc_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Receivables - Other" will fall" |
| 724 | `oth460_aorc_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Receivables - Other" will be neutral" |
| 725 | `oth460_aorc_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Receivables - Other' will move up |
| 726 | `oth460_appy_class` | MATRIX | 1.000 | 搜索与替代数据 | 0 | — | — | — | UNTESTED | Predicted trend of Prepaid Expenses" (1: fall, 2: neutral, 3: move up)" |
| 727 | `oth460_asti_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Short Term Investments" (1: fall, 2: neutral, 3: move-up)" |
| 728 | `oth460_asti_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Short Term Investments' will fall |
| 729 | `oth460_asti_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Short Term Investments" will be neutral" |
| 730 | `oth460_asti_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Short Term Investments" will be move-up" |
| 731 | `oth460_atr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Average True Range' (1: fall, 2: neutral, 3: move-up) |
| 732 | `oth460_bb_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Bollinger Bands" (1: fall, 2: neutral, 3: move up)" |
| 733 | `oth460_bookp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Book-to-market' (1: fall, 2: neutral, 3: move up) |
| 734 | `oth460_bookp_fy1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Book-to-market, FY1" (1: fall, 2: neutral, 3: move-up)" |
| 735 | `oth460_bookp_fy1_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Book-to-Market, FY1" will fall" |
| 736 | `oth460_bookp_fy1_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Book-to-Market, FY1" will be neutral" |
| 737 | `oth460_bookp_fy1_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Book-to-market, FY1" will be move-up" |
| 738 | `oth460_bookp_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Book-to-market" will fall" |
| 739 | `oth460_bookp_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Book-to-Market" will be neutral" |
| 740 | `oth460_bookp_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Book-to-Market" will move up" |
| 741 | `oth460_cci_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of Commodity Channel Index" (1: fall, 2: neutral, 3: move-up)" |
| 742 | `oth460_ceia_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Equity In Affiliates' (1: fall, 2: neutral, 3: move-up) |
| 743 | `oth460_ciac_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Income Available to Com Excl ExtraOrd" (1: fall, 2: neutral, 3: move-up)" |
| 744 | `oth460_clv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Close Location Value" (1: fall, 2: neutral, 3: move-up)" |
| 745 | `oth460_cmea_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Miscellaneous Earnings Adjustment' (1: fall, 2: neutral, 3: move up) |
| 746 | `oth460_cmf_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of Chaikin Money Flow" (1: fall, 2: neutral, 3: move-up)" |
| 747 | `oth460_cmin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Minority Interest" (1: fall, 2: neutral, 3: move up)" |
| 748 | `oth460_cmin_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Minority Interest' will fall |
| 749 | `oth460_cmin_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Minority Interest" will be neutral" |
| 750 | `oth460_cmin_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Minority Interest" will move up" |
| 751 | `oth460_co_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Chaikin Oscillator" (1: fall, 2: neutral, 3: move-up)" |
| 752 | `oth460_compustat_a2_xgb_dl8_d1_xido_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Extraordinary Items and Discontinued Operations" (1: fall, 2: neutral, 3: move up)" |
| 753 | `oth460_compustat_a2_xgb_dl8_d1_xido_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Extraordinary Items and Discontinued Operations" will be fall" |
| 754 | `oth460_compustat_a2_xgb_dl8_d1_xido_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Extraordinary Items and Discontinued Operations" will be neutral" |
| 755 | `oth460_compustat_a2_xgb_dl8_d1_xido_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Extraordinary Items and Discontinued Operations" will be move-up" |
| 756 | `oth460_cprd_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Preferred Dividends" (1: fall, 2: neutral, 3: move-up)" |
| 757 | `oth460_ddps1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of DPS - Common Stock Primary Issue" (1: fall, 2: neutral, 3: move-up)" |
| 758 | `oth460_ddps2_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Dividends per Share - Com Stock Issue 2" (1: fall, 2: neutral, 3: move up)" |
| 759 | `oth460_ddps3_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Dividends per Share - Com Stock Issue 3" (1: fall, 2: neutral, 3: move-up)" |
| 760 | `oth460_div_payout_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Dividend payout ratio, trailing' (1: fall, 2: neutral, 3: move up) |
| 761 | `oth460_div_payout_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Dividend payout ratio, trailing" will be fall" |
| 762 | `oth460_div_payout_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Dividend Payout Ratio, Trailing" will be neutral" |
| 763 | `oth460_div_payout_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Dividend payout ratio, trailing' will move up |
| 764 | `oth460_divyld_bb_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Total yield (dividend + share change)" (1: fall, 2: neutral, 3: move-up)" |
| 765 | `oth460_divyld_bb_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Yield (Dividend + Share Change)' will fall |
| 766 | `oth460_divyld_bb_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Yield (Dividend + Share Change)" will be neutral" |
| 767 | `oth460_do_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Discontinued Operations" (1: fall, 2: neutral, 3: move-up)" |
| 768 | `oth460_dpmo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of DecisionPoint Price Momentum Oscillator" (1: fall, 2: neutral, 3: move-up)" |
| 769 | `oth460_dpo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Detrended Price Oscillator" (1: fall, 2: neutral, 3: move-up)" |
| 770 | `oth460_dsps1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Special DPS - Common Stock Primary Issue' (1: fall, 2: neutral, 3: move-up) |
| 771 | `oth460_dsps2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Special DPS - Common Stock Issue 2" (1: fall, 2: neutral, 3: move-up)" |
| 772 | `oth460_eama_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Amortization of Acquisition Costs" (1: fall, 2: neutral, 3: move up)" |
| 773 | `oth460_eama_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization of Acquisition Costs" will fall" |
| 774 | `oth460_eama_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization of Acquisition Costs" will be neutral" |
| 775 | `oth460_eama_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization of Acquisition Costs" will move up" |
| 776 | `oth460_efex_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Fuel Expense" (1: fall, 2: neutral, 3: move-up)" |
| 777 | `oth460_egla_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Loss (Gain) on Sale of Assets - Operating' (1: fall, 2: neutral, 3: move-up) |
| 778 | `oth460_eias_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Impairment-Assets Held for Sale' (1: fall, 2: neutral, 3: move up) |
| 779 | `oth460_eiau_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Impairment-Assets Held for Use" (1: fall, 2: neutral, 3: move up)" |
| 780 | `oth460_eibt_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Net Income Before Taxes" (1: fall, 2: neutral, 3: move-up)" |
| 781 | `oth460_einv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Investment Income - Operating" (1: fall, 2: neutral, 3: move up)" |
| 782 | `oth460_eiob_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of 'Interest on Other Borrowings' (1: fall, 2: neutral, 3: move up) |
| 783 | `oth460_elit_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Litigation" (1: fall, 2: neutral, 3: move up)" |
| 784 | `oth460_elit_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Litigation' will fall |
| 785 | `oth460_elit_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Litigation" will be neutral" |
| 786 | `oth460_elit_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Litigation' will move up |
| 787 | `oth460_ellp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Loan Loss Provision" (1: fall, 2: neutral, 3: move-up)" |
| 788 | `oth460_ellp_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Loan Loss Provision' will fall |
| 789 | `oth460_ellp_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Loan Loss Provision" will be neutral" |
| 790 | `oth460_ellp_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Loan Loss Provision' will move up |
| 791 | `oth460_emv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Ease of Movement' (1: fall, 2: neutral, 3: move up) |
| 792 | `oth460_eont_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other, Net" (1: fall, 2: neutral, 3: move up)" |
| 793 | `oth460_eont_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other, Net" will be fall" |
| 794 | `oth460_eont_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other, Net" will be neutral" |
| 795 | `oth460_eont_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other, Net" will move up" |
| 796 | `oth460_eps_disp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 EPS dispersion" (1: fall, 2: neutral, 3: move-up)" |
| 797 | `oth460_eps_disp_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EPS dispersion" will fall" |
| 798 | `oth460_eps_disp_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EPS dispersion" will be neutral" |
| 799 | `oth460_eps_disp_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EPS dispersion" will be move-up" |
| 800 | `oth460_eps_sur_decay_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of EPS Surprise with Decay" (1: fall, 2: neutral, 3: move-up)" |
| 801 | `oth460_eps_sur_decay_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of EPS Surprise with Decay" will fall" |
| 802 | `oth460_eps_sur_decay_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of EPS Surprise with Decay" will be neutral" |
| 803 | `oth460_eps_sur_decay_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of EPS Surprise with Decay" will be move-up" |
| 804 | `oth460_eres_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Restructuring Charge" (1: fall, 2: neutral, 3: move-up)" |
| 805 | `oth460_eres_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Restructuring Charge' will fall |
| 806 | `oth460_eres_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Restructuring Charge" will be neutral" |
| 807 | `oth460_eres_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Restructuring Charge" will be move-up" |
| 808 | `oth460_es_bps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'FY1 BPS diffusion (up/down ratio), 1M' (1: fall, 2: neutral, 3: move up) |
| 809 | `oth460_es_bps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of 'FY1 BPS revision, 1M' (1: fall, 2: neutral, 3: move up) |
| 810 | `oth460_es_bps_ntm_r3m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM BPS revision, 3M" (1: fall, 2: neutral, 3: move up)" |
| 811 | `oth460_es_cfps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 CFPS diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move up)" |
| 812 | `oth460_es_cfps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 CFPS Revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 813 | `oth460_es_cfps_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM CFPS Revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 814 | `oth460_es_dps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 DPS Diffusion (Up/Down Ratio), 1M" (1: fall, 2: neutral, 3: move-up)" |
| 815 | `oth460_es_dps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 DPS revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 816 | `oth460_es_dps_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM DPS revision, 1M" (1: fall, 2: neutral, 3: move up)" |
| 817 | `oth460_es_ebit_fy1_d1m_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 EBIT diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up)" |
| 818 | `oth460_es_ebit_fy1_d1m_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBIT diffusion (up/down ratio), 1M" will fall" |
| 819 | `oth460_es_ebit_fy1_d1m_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBIT diffusion (up/down ratio), 1M" will be neutral" |
| 820 | `oth460_es_ebit_fy1_d1m_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 EBIT diffusion (up/down ratio), 1M' will move up |
| 821 | `oth460_es_ebit_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 EBIT revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 822 | `oth460_es_ebit_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 EBIT revision, 1M' will fall |
| 823 | `oth460_es_ebit_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBIT Revision, 1M" will be neutral" |
| 824 | `oth460_es_ebit_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 EBIT revision, 1M' will be move-up |
| 825 | `oth460_es_ebit_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM EBIT revision, 1M" (1: fall, 2: neutral, 3: move up)" |
| 826 | `oth460_es_ebit_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'NTM EBIT revision, 1M' will fall |
| 827 | `oth460_es_ebit_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EBIT revision, 1M" will be neutral" |
| 828 | `oth460_es_ebit_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EBIT revision, 1M" will be move-up" |
| 829 | `oth460_es_ebitda_fy1_d1m_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 EBITDA Diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up)" |
| 830 | `oth460_es_ebitda_fy1_d1m_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 EBITDA diffusion (up/down ratio), 1M' will fall |
| 831 | `oth460_es_ebitda_fy1_d1m_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBITDA diffusion (up/down ratio), 1M" will be neutral" |
| 832 | `oth460_es_ebitda_fy1_d1m_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBITDA diffusion (up/down ratio), 1M" will move up" |
| 833 | `oth460_es_ebitda_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 EBITDA revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 834 | `oth460_es_ebitda_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBITDA revision, 1M" will fall" |
| 835 | `oth460_es_ebitda_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBITDA Revision, 1M" will be neutral" |
| 836 | `oth460_es_ebitda_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 EBITDA revision, 1M" will move up" |
| 837 | `oth460_es_ebitda_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM EBITDA revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 838 | `oth460_es_ebitda_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EBITDA Revision, 1M" will fall" |
| 839 | `oth460_es_ebitda_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM EBITDA revision, 1M" will be neutral" |
| 840 | `oth460_es_ebitda_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'NTM EBITDA revision, 1M' will move up |
| 841 | `oth460_es_eps_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'FY1 EPS diffusion (up/down ratio), 1M' (1: fall, 2: neutral, 3: move up) |
| 842 | `oth460_es_eps_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of 'FY1 EPS revision, 1M' (1: fall, 2: neutral, 3: move up) |
| 843 | `oth460_es_eps_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of 'NTM EPS Revision, 1M' (1: fall, 2: neutral, 3: move up) |
| 844 | `oth460_es_ltg_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Long-term growth diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up)" |
| 845 | `oth460_es_ltg_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of Long-term Growth Revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 846 | `oth460_es_nav_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'FY1 NAV diffusion (up/down ratio), 1M' (1: fall, 2: neutral, 3: move up) |
| 847 | `oth460_es_nav_fy1_d3m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 NAV diffusion (up/down ratio), 3M" (1: fall, 2: neutral, 3: move up)" |
| 848 | `oth460_es_nav_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 NAV revision, 1M" (1: fall, 2: neutral, 3: move up)" |
| 849 | `oth460_es_rec_d1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of Recommendation diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move up)" |
| 850 | `oth460_es_rec_d3m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of Recommendation diffusion (up/down ratio), 3M" (1: fall, 2: neutral, 3: move-up)" |
| 851 | `oth460_es_rec_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of Recommendation Revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 852 | `oth460_es_roe_fy1_d1m_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 ROE diffusion (up/down ratio), 1M" (1: fall, 2: neutral, 3: move-up)" |
| 853 | `oth460_es_roe_fy1_d1m_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 ROE diffusion (up/down ratio), 1M" will be a fall" |
| 854 | `oth460_es_roe_fy1_d1m_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 ROE Diffusion (up/down ratio), 1M" will be neutral" |
| 855 | `oth460_es_roe_fy1_d1m_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 ROE diffusion (up/down ratio), 1M' will move up |
| 856 | `oth460_es_roe_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 ROE revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 857 | `oth460_es_roe_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 ROE revision, 1M' will fall |
| 858 | `oth460_es_roe_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 ROE revision, 1M" will be neutral" |
| 859 | `oth460_es_roe_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 ROE Revision, 1M' will be move-up |
| 860 | `oth460_es_roe_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM ROE revision, 1M" (1: fall, 2: neutral, 3: move up)" |
| 861 | `oth460_es_roe_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM ROE Revision, 1M" will fall" |
| 862 | `oth460_es_roe_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM ROE revision, 1M" will be neutral" |
| 863 | `oth460_es_roe_ntm_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM ROE revision, 1M" will be move-up" |
| 864 | `oth460_es_sale_fy1_d1m_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 Revenue Diffusion (Up/Down Ratio), 1M" (1: fall, 2: neutral, 3: move-up)" |
| 865 | `oth460_es_sale_fy1_d1m_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 revenue diffusion (up/down ratio), 1M' will fall |
| 866 | `oth460_es_sale_fy1_d1m_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 revenue diffusion (up/down ratio), 1M" will be neutral" |
| 867 | `oth460_es_sale_fy1_d1m_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 Revenue Diffusion (up/down ratio), 1M' will be move-up |
| 868 | `oth460_es_sale_fy1_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of FY1 revenue revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 869 | `oth460_es_sale_fy1_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 revenue revision, 1M' will fall |
| 870 | `oth460_es_sale_fy1_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of FY1 revenue revision, 1M" will be neutral" |
| 871 | `oth460_es_sale_fy1_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'FY1 revenue revision, 1M' will move up |
| 872 | `oth460_es_sale_ntm_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of NTM Revenue Revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 873 | `oth460_es_sale_ntm_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'NTM revenue revision, 1M' will fall |
| 874 | `oth460_es_sale_ntm_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of NTM revenue revision, 1M" will be neutral" |
| 875 | `oth460_es_tp_d1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of 'Target price diffusion (up/down ratio), 1M' (1: fall, 2: neutral, 3: move up) |
| 876 | `oth460_es_tp_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of Target price revision, 1M" (1: fall, 2: neutral, 3: move-up)" |
| 877 | `oth460_es_vol_r1m_class` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Predicted trend of Analyst estimated vol revision, 1M" (1: fall, 2: neutral, 3: move up)" |
| 878 | `oth460_es_vol_r1m_l1` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Analyst estimated vol revision, 1M' will fall |
| 879 | `oth460_es_vol_r1m_l2` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Analyst Estimated Vol Revision, 1M" will be neutral" |
| 880 | `oth460_es_vol_r1m_l3` | MATRIX | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | The probability that the future trend of Analyst estimated vol revision, 1M" will move up" |
| 881 | `oth460_euie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Unusual Expense (Income)" (1: fall, 2: neutral, 3: move-up)" |
| 882 | `oth460_ext_fin_noa_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Net External Financing/Net Operating Assets" (1: fall, 2: neutral, 3: move-up)" |
| 883 | `oth460_ext_fin_noa_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net external financing/net operating assets" will be fall" |
| 884 | `oth460_ext_fin_noa_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net External Financing/Net Operating Assets" will be neutral" |
| 885 | `oth460_ext_fin_noa_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Net external financing/net operating assets" will move up" |
| 886 | `oth460_fca_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Foreign Exchange Income (Loss)" (1: fall, 2: neutral, 3: move-up)" |
| 887 | `oth460_fcsn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Common Stock, Net" (1: fall, 2: neutral, 3: move-up)" |
| 888 | `oth460_fdpp_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Cash Dividends Paid - Preferred" (1: fall, 2: neutral, 3: move-up)" |
| 889 | `oth460_fincf_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Financing Activities Net Cash Flow" (1: fall, 2: neutral, 3: move up)" |
| 890 | `oth460_fincf_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Financing Activities Net Cash Flow" will be neutral" |
| 891 | `oth460_fincf_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Financing Activities Net Cash Flow" will be move-up" |
| 892 | `oth460_float_to_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Float turnover, 12M" (1: fall, 2: neutral, 3: move up)" |
| 893 | `oth460_float_to_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Float turnover, 12M" will fall" |
| 894 | `oth460_float_to_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Float turnover, 12M" will be neutral" |
| 895 | `oth460_fprd_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Issuance (Retirement) of Debt, Net" (1: fall, 2: neutral, 3: move-up)" |
| 896 | `oth460_fpss_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Issuance (Retirement) of Stock, Net' (1: fall, 2: neutral, 3: move up) |
| 897 | `oth460_frcp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Repurch./Retirement of Common/Preferred" (1: fall, 2: neutral, 3: move-up)" |
| 898 | `oth460_frrp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Repurchase/Retirement of Preferred" (1: fall, 2: neutral, 3: move-up)" |
| 899 | `oth460_fscp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Sale/Issuance of Common/Preferred" (1: fall, 2: neutral, 3: move-up)" |
| 900 | `oth460_fsdn_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Short Term Debt, Net' (1: fall, 2: neutral, 3: move-up) |
| 901 | `oth460_fsic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Sale/Issuance of Common" (1: fall, 2: neutral, 3: move up)" |
| 902 | `oth460_fsic_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Common" will fall" |
| 903 | `oth460_fsic_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Common" will be neutral" |
| 904 | `oth460_fsic_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Common" will be move-up" |
| 905 | `oth460_fsip_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Sale/Issuance of Preferred' (1: fall, 2: neutral, 3: move up) |
| 906 | `oth460_fsip_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Preferred" will be fall" |
| 907 | `oth460_fsip_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Preferred" will be neutral" |
| 908 | `oth460_fsip_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale/Issuance of Preferred" will move up" |
| 909 | `oth460_fwcv_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Warrants Converted" (1: fall, 2: neutral, 3: move-up)" |
| 910 | `oth460_gr_5y_cfps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Historical 5Y CFPS Growth Trend" (1: fall, 2: neutral, 3: move-up)" |
| 911 | `oth460_gr_5y_eps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Historical 5Y EPS Growth Trend" (1: fall, 2: neutral, 3: move-up)" |
| 912 | `oth460_gr_5y_oeps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Historical 5Y Operating EPS Growth Trend" (1: fall, 2: neutral, 3: move up)" |
| 913 | `oth460_gr_eintr_cfps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of YoY Expected Interim CFPS Growth" (1: fall, 2: neutral, 3: move-up)" |
| 914 | `oth460_hilomid_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of High Low Mid Point" (1: fall, 2: neutral, 3: move-up)" |
| 915 | `oth460_hilomid_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of High Low Mid Point" will be fall" |
| 916 | `oth460_hilomid_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of High Low Mid Point" will be neutral" |
| 917 | `oth460_hilomid_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of High Low Mid Point" will move up" |
| 918 | `oth460_hr_epsyld_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Historical Relative Earnings Yield" (1: fall, 2: neutral, 3: move-up)" |
| 919 | `oth460_ibaq_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Acquisition of Business" (1: fall, 2: neutral, 3: move-up)" |
| 920 | `oth460_ibaq_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Acquisition of Business" will be fall" |
| 921 | `oth460_ibaq_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Acquisition of Business" will be neutral" |
| 922 | `oth460_ibaq_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Acquisition of Business" will be move-up" |
| 923 | `oth460_iivn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Investment, Net" (1: fall, 2: neutral, 3: move-up)" |
| 924 | `oth460_isoi_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Sale of Intangible Assets" (1: fall, 2: neutral, 3: move-up)" |
| 925 | `oth460_isoi_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale of Intangible Assets" will fall" |
| 926 | `oth460_isoi_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale of Intangible Assets" will be neutral" |
| 927 | `oth460_isoi_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Sale of Intangible Assets" will move up" |
| 928 | `oth460_lclo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Capital Lease Obligations" (1: fall, 2: neutral, 3: move-up)" |
| 929 | `oth460_lco_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Current Liabilities Other Total" (1: fall, 2: neutral, 3: move-up)" |
| 930 | `oth460_ldcl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Discontinued Operations - Curr Liability" (1: fall, 2: neutral, 3: move up)" |
| 931 | `oth460_ldol_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Discontinued Operations - Liabilities" (1: fall, 2: neutral, 3: move-up)" |
| 932 | `oth460_ldol_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Liabilities" will be fall" |
| 933 | `oth460_ldol_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Liabilities" will be neutral" |
| 934 | `oth460_ldol_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations - Liabilities" will be move-up" |
| 935 | `oth460_ldtc_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Income Tax - Current Liability" (1: fall, 2: neutral, 3: move-up)" |
| 936 | `oth460_lffp_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of FedFundsPurch/ScrtySoldUnderRepurchAgrmt" (1: fall, 2: neutral, 3: move-up)" |
| 937 | `oth460_lltl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Long Term Liabilities' (1: fall, 2: neutral, 3: move up) |
| 938 | `oth460_lobl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Bearing Liabilities' (1: fall, 2: neutral, 3: move up) |
| 939 | `oth460_lobl_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Bearing Liabilities" will be fall" |
| 940 | `oth460_lobl_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Bearing Liabilities" will be neutral" |
| 941 | `oth460_lobl_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Bearing Liabilities' will move up |
| 942 | `oth460_lotb_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Short Term Borrowings' (1: fall, 2: neutral, 3: move up) |
| 943 | `oth460_lotb_l1` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Short Term Borrowings" will fall" |
| 944 | `oth460_lotb_l2` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Short Term Borrowings" will be neutral" |
| 945 | `oth460_lotb_l3` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Short Term Borrowings" will be move-up" |
| 946 | `oth460_lottery_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Maximum daily return in the last 1M (lottery factor)" (1: fall, 2: neutral, 3: move-up)" |
| 947 | `oth460_lottery_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Maximum Daily Return in the Last 1M (Lottery Factor)' will be fall |
| 948 | `oth460_lottery_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Maximum daily return in the last 1M (lottery factor)" will be neutral" |
| 949 | `oth460_lottery_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Maximum daily return in the last 1M (lottery factor)" will move up" |
| 950 | `oth460_lstb_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of Total Short Term Borrowings" (1: fall, 2: neutral, 3: move up)" |
| 951 | `oth460_lstd_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Notes Payable/Short Term Debt" (1: fall, 2: neutral, 3: move-up)" |
| 952 | `oth460_lt_dt_eq_chg_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of YoY Change in Long-Term Debt/Common Equity" (1: fall, 2: neutral, 3: move-up)" |
| 953 | `oth460_ltxp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Income Taxes Payable" (1: fall, 2: neutral, 3: move-up)" |
| 954 | `oth460_lupr_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Unearned Premium/Unearned Revenue" (1: fall, 2: neutral, 3: move-up)" |
| 955 | `oth460_ma_15_36_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Moving average crossover, 15W-36W" (1: fall, 2: neutral, 3: move-up)" |
| 956 | `oth460_ma_30_75_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Moving Average Crossover, 30W-75W" (1: fall, 2: neutral, 3: move-up)" |
| 957 | `oth460_macd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Moving Average Convergence/Divergence Oscillator (MACD)" (1: fall, 2: neutral, 3: move-up)" |
| 958 | `oth460_macd_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Moving Average Convergence/Divergence Oscillator (MACD)' will fall |
| 959 | `oth460_macd_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Moving Average Convergence/Divergence Oscillator (MACD)" will be neutral" |
| 960 | `oth460_macd_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Moving Average Convergence/Divergence Oscillator (MACD)' will move-up |
| 961 | `oth460_mbbc_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of EBITDAR" (1: fall, 2: neutral, 3: move-up)" |
| 962 | `oth460_mbbe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Passengers, Total" (1: fall, 2: neutral, 3: move-up)" |
| 963 | `oth460_mbdl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Load Factor, Total -%" (1: fall, 2: neutral, 3: move-up)" |
| 964 | `oth460_mfi_class` | MATRIX | 1.000 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Predicted trend of Money Flow Index" (1: fall, 2: neutral, 3: move-up)" |
| 965 | `oth460_mhak_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Revenue per Avail. Room (REVPAR), Total" (1: fall, 2: neutral, 3: move-up)" |
| 966 | `oth460_mhak_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Revenue per Avail. Room (REVPAR), Total' will fall |
| 967 | `oth460_mhak_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Revenue per Avail. Room (REVPAR), Total" will be neutral" |
| 968 | `oth460_mhak_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Revenue per Avail. Room (REVPAR), Total' will move up |
| 969 | `oth460_mhaz_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Rooms" (1: fall, 2: neutral, 3: move-up)" |
| 970 | `oth460_mi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Mass Index" (1: fall, 2: neutral, 3: move-up)" |
| 971 | `oth460_mibh_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Loss Ratio, Total -%" (1: fall, 2: neutral, 3: move-up)" |
| 972 | `oth460_mibh_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Loss Ratio, Total -%" will fall" |
| 973 | `oth460_mibh_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Loss Ratio, Total -%" will be neutral" |
| 974 | `oth460_mibh_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Loss Ratio, Total -%" will move up" |
| 975 | `oth460_mibl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Combined Ratio, Total -%" (1: fall, 2: neutral, 3: move-up)" |
| 976 | `oth460_mibl_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Combined Ratio, Total -%" will fall" |
| 977 | `oth460_mibl_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Combined Ratio, Total -%" will be neutral" |
| 978 | `oth460_mibl_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Combined Ratio, Total -%" will move up" |
| 979 | `oth460_mibz_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Underwriting Profit or Loss" (1: fall, 2: neutral, 3: move-up)" |
| 980 | `oth460_mibz_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Underwriting Profit or Loss" will fall" |
| 981 | `oth460_mibz_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Underwriting Profit or Loss" will move up" |
| 982 | `oth460_migo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of New Business Annual Premium Equiv. (APE)" (1: fall, 2: neutral, 3: move up)" |
| 983 | `oth460_migo_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'New Business Annual Premium Equiv. (APE)' will fall |
| 984 | `oth460_migo_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of New Business Annual Premium Equiv. (APE)" will be neutral" |
| 985 | `oth460_migo_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of New Business Annual Premium Equiv. (APE)" will move up" |
| 986 | `oth460_mnio_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Net Interest Margin, Total -%" (1: fall, 2: neutral, 3: move up)" |
| 987 | `oth460_mobh_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of 'Crude Oil, Avg. Sales pp. Barrel, Total' (1: fall, 2: neutral, 3: move up) |
| 988 | `oth460_mobh_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Crude Oil, Avg. Sales pp. Barrel, Total" will fall" |
| 989 | `oth460_mobh_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Crude Oil, Avg. Sales pp. Barrel, Total" will be neutral" |
| 990 | `oth460_mobh_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Crude Oil, Avg. Sales pp. Barrel, Total" will move up" |
| 991 | `oth460_mobk_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of 'Crude Oil Production (Barrels)' (1: fall, 2: neutral, 3: move up) |
| 992 | `oth460_mobk_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Crude Oil Production (Barrels)' will fall |
| 993 | `oth460_mobk_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Crude Oil Production (Barrels)" will be neutral" |
| 994 | `oth460_mobk_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Crude Oil Production (Barrels)' will move up |
| 995 | `oth460_mogo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Exploration and Development Costs' (1: fall, 2: neutral, 3: move up) |
| 996 | `oth460_mogo_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Exploration and Development Costs" will fall" |
| 997 | `oth460_mogo_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Exploration and Development Costs" will be neutral" |
| 998 | `oth460_mogo_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Exploration and Development Costs' will move up |
| 999 | `oth460_moio_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Wells, New" (1: fall, 2: neutral, 3: move-up)" |
| 1000 | `oth460_moio_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Wells, New" will be fall" |
| 1001 | `oth460_moio_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Wells, New' will move up |
| 1002 | `oth460_mpp1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Products in Phase I" (1: fall, 2: neutral, 3: move-up)" |
| 1003 | `oth460_mpp2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Products in Phase II" (1: fall, 2: neutral, 3: move-up)" |
| 1004 | `oth460_mpp3_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Products in Phase III" (1: fall, 2: neutral, 3: move up)" |
| 1005 | `oth460_mppl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Products Launched" (1: fall, 2: neutral, 3: move up)" |
| 1006 | `oth460_mpre_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Products in Pre-Registration" (1: fall, 2: neutral, 3: move-up)" |
| 1007 | `oth460_mrth_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Rent Growth (Sequential), Total -%" (1: fall, 2: neutral, 3: move-up)" |
| 1008 | `oth460_mtbd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Comp. Store Sales, Retail, Total - %" (1: fall, 2: neutral, 3: move-up)" |
| 1009 | `oth460_mtbl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Merchandise Margins, Total -%" (1: fall, 2: neutral, 3: move-up)" |
| 1010 | `oth460_mthk_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Stores Opened" (1: fall, 2: neutral, 3: move-up)" |
| 1011 | `oth460_mtho_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Number of Stores Closed" (1: fall, 2: neutral, 3: move-up)" |
| 1012 | `oth460_mtho_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Number of Stores Closed' will fall |
| 1013 | `oth460_mtho_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number of Stores Closed" will be move-up" |
| 1014 | `oth460_mtje_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Value of Bookings" (1: fall, 2: neutral, 3: move up)" |
| 1015 | `oth460_news_abno_sent_1d_class` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Predicted trend of Abnormal Sentiment of Novel/Relevant/Non-Neutral News 1D/365D" (1: fall, 2: neutral, 3: move-up)" |
| 1016 | `oth460_news_abno_sent_1d_l1` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal sentiment of novel/relevant/non-neutral news 1D/365D" will be a fall" |
| 1017 | `oth460_news_abno_sent_1d_l2` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal sentiment of novel/relevant/non-neutral news 1D/365D" will be neutral" |
| 1018 | `oth460_news_abno_sent_1d_l3` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal sentiment of novel/relevant/non-neutral news 1D/365D" will move up" |
| 1019 | `oth460_news_abno_vol_1d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Abnormal volume (z-score) of novel/relevant/non-neutral news, 1D/365D" (1: fall, 2: neutral, 3: move- |
| 1020 | `oth460_news_abno_vol_1d_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal volume (z-score) of novel/relevant/non-neutral news, 1D/365D" will fal |
| 1021 | `oth460_news_abno_vol_1d_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal Volume (z-score) of Novel/Relevant/Non-Neutral News, 1D/365D" will be |
| 1022 | `oth460_news_abno_vol_1d_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Abnormal volume (z-score) of novel/relevant/non-neutral news, 1D/365D" will be |
| 1023 | `oth460_news_sentvol_1d_class` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | Predicted trend of # of novel/relevant/non-neutral news, 1D" (1: fall, 2: neutral, 3: move-up)" |
| 1024 | `oth460_news_sentvol_1d_l1` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of Number ofnovel/relevant/non-neutral news, 1D" will fall" |
| 1025 | `oth460_news_sentvol_1d_l2` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of # of novel/relevant/non-neutral news, 1D" will be neutral" |
| 1026 | `oth460_news_sentvol_1d_l3` | MATRIX | 1.000 | 情绪与新闻 | 0 | — | — | — | UNTESTED | The probability that the future trend of # of novel/relevant/non-neutral news, 1D" will be move-up" |
| 1027 | `oth460_ngla_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Gain (Loss) on Sale of Assets' (1: fall, 2: neutral, 3: move up) |
| 1028 | `oth460_nlar_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Labor & Related Expenses" (1: fall, 2: neutral, 3: move-up)" |
| 1029 | `oth460_nlar_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Labor & Related Expenses" will be fall" |
| 1030 | `oth460_nlar_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Labor & Related Expenses" will be neutral" |
| 1031 | `oth460_nlar_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Labor & Related Expenses" will move up" |
| 1032 | `oth460_noex_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Expense" (1: fall, 2: neutral, 3: move up)" |
| 1033 | `oth460_nont_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Non-Operating Income (Expense)" (1: fall, 2: neutral, 3: move-up)" |
| 1034 | `oth460_nont_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Non-Operating Income (Expense)" will be fall" |
| 1035 | `oth460_nont_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Non-Operating Income (Expense)" will be neutral" |
| 1036 | `oth460_nont_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Non-Operating Income (Expense)" will be move-up" |
| 1037 | `oth460_noru_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Revenue" (1: fall, 2: neutral, 3: move-up)" |
| 1038 | `oth460_noru_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Revenue' will fall |
| 1039 | `oth460_noru_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Revenue" will be neutral" |
| 1040 | `oth460_noru_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Revenue" will move up" |
| 1041 | `oth460_nres_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Restructuring Charge" (1: fall, 2: neutral, 3: move-up)" |
| 1042 | `oth460_nsgl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Investment Securities Gains" (1: fall, 2: neutral, 3: move-up)" |
| 1043 | `oth460_nuie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Unusual Expense" (1: fall, 2: neutral, 3: move-up)" |
| 1044 | `oth460_nuii_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Unusual Income" (1: fall, 2: neutral, 3: move up)" |
| 1045 | `oth460_nvi_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Negative Volume Index" (1: fall, 2: neutral, 3: move-up)" |
| 1046 | `oth460_oacr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Accounts Receivable" (1: fall, 2: neutral, 3: move-up)" |
| 1047 | `oth460_oaex_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Accrued Expenses" (1: fall, 2: neutral, 3: move-up)" |
| 1048 | `oth460_oama_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Amortization of Acquisition Costs" (1: fall, 2: neutral, 3: move up)" |
| 1049 | `oth460_oama_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization of Acquisition Costs" will be fall" |
| 1050 | `oth460_oama_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization of Acquisition Costs" will be neutral" |
| 1051 | `oth460_oama_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Amortization of Acquisition Costs' will move up |
| 1052 | `oth460_oami_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Amortization of Intangibles" (1: fall, 2: neutral, 3: move-up)" |
| 1053 | `oth460_oami_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Amortization of Intangibles' will fall |
| 1054 | `oth460_oami_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization of Intangibles" will be neutral" |
| 1055 | `oth460_oami_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization of Intangibles" will move up" |
| 1056 | `oth460_oapb_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Accounts Payable" (1: fall, 2: neutral, 3: move-up)" |
| 1057 | `oth460_obdt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Taxes" (1: fall, 2: neutral, 3: move-up)" |
| 1058 | `oth460_obv_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of On Balance Volume" (1: fall, 2: neutral, 3: move up)" |
| 1059 | `oth460_oido_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Discontinued Operations" (1: fall, 2: neutral, 3: move up)" |
| 1060 | `oth460_oido_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations" will be fall" |
| 1061 | `oth460_oido_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations" will be neutral" |
| 1062 | `oth460_oido_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Discontinued Operations' will move-up |
| 1063 | `oth460_oitl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Inventories' (1: fall, 2: neutral, 3: move up) |
| 1064 | `oth460_ooal_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Other Assets & Liabilities, Net' (1: fall, 2: neutral, 3: move up) |
| 1065 | `oth460_ooas_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Assets" (1: fall, 2: neutral, 3: move up)" |
| 1066 | `oth460_oolb_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Liabilities" (1: fall, 2: neutral, 3: move up)" |
| 1067 | `oth460_opba_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Payable/Accrued" (1: fall, 2: neutral, 3: move-up)" |
| 1068 | `oth460_oppy_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Prepaid Expenses" (1: fall, 2: neutral, 3: move-up)" |
| 1069 | `oth460_orer_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Reinsurance Receivable' (1: fall, 2: neutral, 3: move up) |
| 1070 | `oth460_orer_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Reinsurance Receivable" will fall" |
| 1071 | `oth460_orer_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Reinsurance Receivable" will be neutral" |
| 1072 | `oth460_orer_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Reinsurance Receivable' will move up |
| 1073 | `oth460_ouie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Unusual Items' (1: fall, 2: neutral, 3: move up) |
| 1074 | `oth460_payable_to_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Accounts Payable Turnover" (1: fall, 2: neutral, 3: move-up)" |
| 1075 | `oth460_payable_to_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Accounts Payable Turnover' will fall |
| 1076 | `oth460_payable_to_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accounts Payable Turnover" will be neutral" |
| 1077 | `oth460_payable_to_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Accounts Payable Turnover" will be move-up" |
| 1078 | `oth460_ppo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of percentage price oscillator" (1: fall, 2: neutral, 3: move up)" |
| 1079 | `oth460_psale_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Price-to-sales" (1: fall, 2: neutral, 3: move-up)" |
| 1080 | `oth460_psale_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Price-to-sales" will be fall" |
| 1081 | `oth460_psale_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Price-to-sales" will be neutral" |
| 1082 | `oth460_psale_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Price-to-sales" will be move-up" |
| 1083 | `oth460_pvo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Percentage Volume Oscillator" (1: fall, 2: neutral, 3: move-up)" |
| 1084 | `oth460_qcom_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Comprehensive Income" (1: fall, 2: neutral, 3: move up)" |
| 1085 | `oth460_qote_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Equity" (1: fall, 2: neutral, 3: move up)" |
| 1086 | `oth460_qpso1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Shares Outstanding - Preferred Primary Issue" (1: fall, 2: neutral, 3: move-up)" |
| 1087 | `oth460_qpso2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Shares Outstanding - Preferred Issue 2" (1: fall, 2: neutral, 3: move-up)" |
| 1088 | `oth460_qtpo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Total Preferred Shares Outstanding" (1: fall, 2: neutral, 3: move-up)" |
| 1089 | `oth460_qtsn1_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Treas Shares - Common Stock Primary Issue" (1: fall, 2: neutral, 3: move-up)" |
| 1090 | `oth460_qtsn2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Treasury Shares - Common Issue 2' (1: fall, 2: neutral, 3: move up) |
| 1091 | `oth460_qugl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Unrealized Gain (Loss)" (1: fall, 2: neutral, 3: move-up)" |
| 1092 | `oth460_reop_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Electric Operations" (1: fall, 2: neutral, 3: move-up)" |
| 1093 | `oth460_rext_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Excise Tax Payments" (1: fall, 2: neutral, 3: move-up)" |
| 1094 | `oth460_rext_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Excise Tax Payments" will be fall" |
| 1095 | `oth460_rext_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Excise Tax Payments" will be neutral" |
| 1096 | `oth460_rext_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Excise Tax Payments' will move up |
| 1097 | `oth460_risi_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Interest & Dividends on Investment Secs." (1: fall, 2: neutral, 3: move-up)" |
| 1098 | `oth460_rnir_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Non-Insurance Revenue" (1: fall, 2: neutral, 3: move-up)" |
| 1099 | `oth460_rnts_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Net Sales" (1: fall, 2: neutral, 3: move up)" |
| 1100 | `oth460_rrgl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Realized & Unrealized Gains (Losses)" (1: fall, 2: neutral, 3: move-up)" |
| 1101 | `oth460_rrii_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Reinsurance - Income" (1: fall, 2: neutral, 3: move up)" |
| 1102 | `oth460_rtlr_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Total Revenue" (1: fall, 2: neutral, 3: move up)" |
| 1103 | `oth460_rtn21d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Total Return, past 1M" (1: fall, 2: neutral, 3: move up)" |
| 1104 | `oth460_rtn2520d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Total return, past 120M" (1: fall, 2: neutral, 3: move-up)" |
| 1105 | `oth460_rtn63d_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 3-Month Total Return" (1: fall, 2: neutral, 3: move-up)" |
| 1106 | `oth460_rtn_12m1m_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Price Momentum, 12M-1M" (1: fall, 2: neutral, 3: move-up)" |
| 1107 | `oth460_sadg_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 'Copper, Average Price per Metric Ton' (1: fall, 2: neutral, 3: move up) |
| 1108 | `oth460_sadg_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Copper, Average Price per Metric Ton" will be a fall" |
| 1109 | `oth460_sadg_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Copper, Average Price per Metric Ton" will be neutral" |
| 1110 | `oth460_sadg_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Copper, Average Price per Metric Ton" will be move-up" |
| 1111 | `oth460_samt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Amortization" (1: fall, 2: neutral, 3: move up)" |
| 1112 | `oth460_samt_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization" will fall" |
| 1113 | `oth460_samt_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization" will be neutral" |
| 1114 | `oth460_samt_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amortization" will move up" |
| 1115 | `oth460_sani_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Total Adjustments to Net Income" (1: fall, 2: neutral, 3: move-up)" |
| 1116 | `oth460_sani_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Adjustments to Net Income" will be fall" |
| 1117 | `oth460_sani_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Adjustments to Net Income" will be neutral" |
| 1118 | `oth460_sani_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Total Adjustments to Net Income' will move up |
| 1119 | `oth460_sbai_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Basic EPS Including Extraordinary Items" (1: fall, 2: neutral, 3: move up)" |
| 1120 | `oth460_sbbq_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Revenue Passenger Kilometers (RPK)" (1: fall, 2: neutral, 3: move-up)" |
| 1121 | `oth460_sbda_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Normalized EBITDA" (1: fall, 2: neutral, 3: move-up)" |
| 1122 | `oth460_sbdg_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 'Available Seat Kilometers (ASK)' (1: fall, 2: neutral, 3: move up) |
| 1123 | `oth460_sbit_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Normalized EBIT" (1: fall, 2: neutral, 3: move-up)" |
| 1124 | `oth460_sbit_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized EBIT" will be fall" |
| 1125 | `oth460_sbit_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized EBIT" will be neutral" |
| 1126 | `oth460_sbit_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized EBIT' will move up |
| 1127 | `oth460_sbjg_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Operating Expense per ASK" (1: fall, 2: neutral, 3: move-up)" |
| 1128 | `oth460_scl23_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Capital Lease Payments Due in 2-3 Years" (1: fall, 2: neutral, 3: move up)" |
| 1129 | `oth460_scl2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Capital Lease Payments Due in Year 2" (1: fall, 2: neutral, 3: move-up)" |
| 1130 | `oth460_scl3_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Capital Lease Payments Due in Year 3" (1: fall, 2: neutral, 3: move-up)" |
| 1131 | `oth460_scl45_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Capital Lease Payments Due in 4-5 Years" (1: fall, 2: neutral, 3: move-up)" |
| 1132 | `oth460_scl4_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Capital Lease Payments Due in Year 4' (1: fall, 2: neutral, 3: move up) |
| 1133 | `oth460_scl5_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Capital Lease Payments Due in Year 5" (1: fall, 2: neutral, 3: move-up)" |
| 1134 | `oth460_scsi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Cash and Short Term Investments" (1: fall, 2: neutral, 3: move-up)" |
| 1135 | `oth460_scur_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Current Ratio" (1: fall, 2: neutral, 3: move up)" |
| 1136 | `oth460_scur_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Current Ratio' will fall |
| 1137 | `oth460_scur_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Ratio" will be neutral" |
| 1138 | `oth460_scur_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Current Ratio" will be move-up" |
| 1139 | `oth460_sdai_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Diluted EPS Including Extraordinary Items" (1: fall, 2: neutral, 3: move-up)" |
| 1140 | `oth460_sdni_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Diluted Net Income' (1: fall, 2: neutral, 3: move up) |
| 1141 | `oth460_setr_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of Effective Tax Rate" (1: fall, 2: neutral, 3: move-up)" |
| 1142 | `oth460_setr_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Effective Tax Rate" will be fall" |
| 1143 | `oth460_setr_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Effective Tax Rate" will be neutral" |
| 1144 | `oth460_setr_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Effective Tax Rate" will be move-up" |
| 1145 | `oth460_sfee_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Foreign Exchange Effects' (1: fall, 2: neutral, 3: move up) |
| 1146 | `oth460_sfee_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Exchange Effects" will fall" |
| 1147 | `oth460_sfee_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Exchange Effects" will be neutral" |
| 1148 | `oth460_sfee_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Foreign Exchange Effects" will move up" |
| 1149 | `oth460_sgpp_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Gross Margin" (1: fall, 2: neutral, 3: move-up)" |
| 1150 | `oth460_sicf_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Investing Cash Flow Items, Total" (1: fall, 2: neutral, 3: move-up)" |
| 1151 | `oth460_sicf_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Investing Cash Flow Items, Total" will be a fall" |
| 1152 | `oth460_sicf_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Investing Cash Flow Items, Total" will be neutral" |
| 1153 | `oth460_sicf_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Investing Cash Flow Items, Total" will be move-up" |
| 1154 | `oth460_siib_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest Income, Bank" (1: fall, 2: neutral, 3: move up)" |
| 1155 | `oth460_siin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest/Invest Income - Non-Operating" (1: fall, 2: neutral, 3: move-up)" |
| 1156 | `oth460_siio_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest/Investment Income - Operating" (1: fall, 2: neutral, 3: move-up)" |
| 1157 | `oth460_sinn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest Exp.(Inc.),Net-Operating, Total" (1: fall, 2: neutral, 3: move-up)" |
| 1158 | `oth460_sinn_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Exp.(Inc.), Net-Operating, Total" will fall" |
| 1159 | `oth460_sinn_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Exp.(Inc.), Net-Operating, Total" will be neutral" |
| 1160 | `oth460_sinn_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Exp.(Inc.), Net-Operating, Total" will be move-up" |
| 1161 | `oth460_sld10_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Long Term Debt Maturing in Year 10' (1: fall, 2: neutral, 3: move up) |
| 1162 | `oth460_sld1_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Long Term Debt Maturing within 1 Year" (1: fall, 2: neutral, 3: move-up)" |
| 1163 | `oth460_sld2_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Long-Term Debt Maturing in Year 2' (1: fall, 2: neutral, 3: move-up) |
| 1164 | `oth460_sld3_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Long Term Debt Maturing in Year 3" (1: fall, 2: neutral, 3: move-up)" |
| 1165 | `oth460_sld45_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Long Term Debt Maturing in 4-5 Years" (1: fall, 2: neutral, 3: move-up)" |
| 1166 | `oth460_sld5_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Long Term Debt Maturing in Year 5" (1: fall, 2: neutral, 3: move up)" |
| 1167 | `oth460_sld6b_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Long Term Debt Matur. in Year 6 & Beyond" (1: fall, 2: neutral, 3: move-up)" |
| 1168 | `oth460_sld7_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of 'Long Term Debt Maturing in Year 7' (1: fall, 2: neutral, 3: move-up) |
| 1169 | `oth460_sld8_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Long Term Debt Maturing in Year 8" (1: fall, 2: neutral, 3: move-up)" |
| 1170 | `oth460_sncc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Net Change in Cash" (1: fall, 2: neutral, 3: move-up)" |
| 1171 | `oth460_snce_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Net Cash - Ending Balance" (1: fall, 2: neutral, 3: move up)" |
| 1172 | `oth460_snie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Non-Interest Expense, Bank" (1: fall, 2: neutral, 3: move-up)" |
| 1173 | `oth460_snii_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Non-Interest Income, Bank" (1: fall, 2: neutral, 3: move-up)" |
| 1174 | `oth460_snin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest Inc.(Exp.), Net-Non-Op., Total" (1: fall, 2: neutral, 3: move up)" |
| 1175 | `oth460_snpm_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Net Profit Margin" (1: fall, 2: neutral, 3: move-up)" |
| 1176 | `oth460_so_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Stochastic Oscillator' (1: fall, 2: neutral, 3: move up) |
| 1177 | `oth460_soca_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Current Assets, Total" (1: fall, 2: neutral, 3: move-up)" |
| 1178 | `oth460_soca_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets, Total' will fall |
| 1179 | `oth460_soca_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Current Assets, Total" will be neutral" |
| 1180 | `oth460_soca_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Assets, Total' will move up |
| 1181 | `oth460_socf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Changes in Working Capital" (1: fall, 2: neutral, 3: move-up)" |
| 1182 | `oth460_socf_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Changes in Working Capital" will be fall" |
| 1183 | `oth460_socf_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Changes in Working Capital" will be neutral" |
| 1184 | `oth460_socf_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Changes in Working Capital" will move up" |
| 1185 | `oth460_socl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Other Current Liabilities, Total" (1: fall, 2: neutral, 3: move-up)" |
| 1186 | `oth460_socl_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Current Liabilities, Total' will fall |
| 1187 | `oth460_socl_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Current Liabilities, Total" will be neutral" |
| 1188 | `oth460_socl_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Current Liabilities, Total" will be move-up" |
| 1189 | `oth460_sodo_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 'Natural Gas, Avg. Sales Price per Cu.Mt.' (1: fall, 2: neutral, 3: move up) |
| 1190 | `oth460_sodo_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Natural Gas, Avg. Sales Price per Cu.Mt." will be fall" |
| 1191 | `oth460_sodo_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Natural Gas, Avg. Sales Price per Cu.Mt." will be neutral" |
| 1192 | `oth460_sodo_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of Natural Gas, Avg. Sales Price per Cu.Mt." will be move-up" |
| 1193 | `oth460_sol23_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Operating Lease Pymts. Due in 2-3 Years" (1: fall, 2: neutral, 3: move up)" |
| 1194 | `oth460_sol23_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Pymts. Due in 2-3 Years" will fall" |
| 1195 | `oth460_sol23_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in 2-3 Years' will be neutral |
| 1196 | `oth460_sol23_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in 2-3 Years' will move up |
| 1197 | `oth460_sol2_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Operating Lease Payments Due in Year 2" (1: fall, 2: neutral, 3: move-up)" |
| 1198 | `oth460_sol2_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 2" will be fall" |
| 1199 | `oth460_sol2_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in Year 2' will be neutral |
| 1200 | `oth460_sol2_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 2" will be move-up" |
| 1201 | `oth460_sol3_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Operating Lease Payments Due in Year 3' (1: fall, 2: neutral, 3: move up) |
| 1202 | `oth460_sol3_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 3" will be fall" |
| 1203 | `oth460_sol3_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 3" will be neutral" |
| 1204 | `oth460_sol3_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 3" will be move-up" |
| 1205 | `oth460_sol45_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Operating Lease Pymts. Due in 4-5 Years" (1: fall, 2: neutral, 3: move-up)" |
| 1206 | `oth460_sol45_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Pymts. Due in 4-5 Years" will be fall" |
| 1207 | `oth460_sol45_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in 4-5 Years" will be neutral" |
| 1208 | `oth460_sol45_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in 4-5 Years" will move up" |
| 1209 | `oth460_sol4_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Operating Lease Payments Due in Year 4" (1: fall, 2: neutral, 3: move-up)" |
| 1210 | `oth460_sol4_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in Year 4' will fall |
| 1211 | `oth460_sol4_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 4" will be neutral" |
| 1212 | `oth460_sol4_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Operating Lease Payments Due in Year 4' will move up |
| 1213 | `oth460_sol5_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Operating Lease Payments Due in Year 5" (1: fall, 2: neutral, 3: move-up)" |
| 1214 | `oth460_sol5_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 5" will fall" |
| 1215 | `oth460_sol5_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 5" will be neutral" |
| 1216 | `oth460_sol5_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Lease Payments Due in Year 5" will be move-up" |
| 1217 | `oth460_sol6b_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Oper. Lse. Pymts. Due in Year 6 & Beyond" (1: fall, 2: neutral, 3: move-up)" |
| 1218 | `oth460_sol6b_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Oper. Lse. Pymts. Due in Year 6 & Beyond" will fall" |
| 1219 | `oth460_sol6b_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Oper. Lse. Pymts. Due in Year 6 & Beyond" will be neutral" |
| 1220 | `oth460_sol6b_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Oper. Lse. Pymts. Due in Year 6 & Beyond" will be move-up" |
| 1221 | `oth460_sont_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other, Net" (1: fall, 2: neutral, 3: move-up)" |
| 1222 | `oth460_sont_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other, Net' will fall |
| 1223 | `oth460_sont_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other, Net" will be neutral" |
| 1224 | `oth460_sont_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other, Net' will move up |
| 1225 | `oth460_sooe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Operating Expenses, Total" (1: fall, 2: neutral, 3: move-up)" |
| 1226 | `oth460_sopi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Operating Income' (1: fall, 2: neutral, 3: move up) |
| 1227 | `oth460_sopi_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Income" will fall" |
| 1228 | `oth460_sopi_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Income" will be neutral" |
| 1229 | `oth460_sopp_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Operating Margin" (1: fall, 2: neutral, 3: move-up)" |
| 1230 | `oth460_sopp_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Margin" will be fall" |
| 1231 | `oth460_sopp_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Margin" will be neutral" |
| 1232 | `oth460_sopp_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Operating Margin" will move up" |
| 1233 | `oth460_spi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Special Items" (1: fall, 2: neutral, 3: move-up)" |
| 1234 | `oth460_spig_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Iron Ore Production (Metric Tonnes)" (1: fall, 2: neutral, 3: move-up)" |
| 1235 | `oth460_spig_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Iron Ore Production (Metric Tonnes)" will be a fall" |
| 1236 | `oth460_spig_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Iron Ore Production (Metric Tonnes)" will be neutral" |
| 1237 | `oth460_spig_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Iron Ore Production (Metric Tonnes)" will be move-up" |
| 1238 | `oth460_sptm_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Pretax Margin" (1: fall, 2: neutral, 3: move-up)" |
| 1239 | `oth460_sqck_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Quick Ratio" (1: fall, 2: neutral, 3: move-up)" |
| 1240 | `oth460_srev_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Revenue" (1: fall, 2: neutral, 3: move-up)" |
| 1241 | `oth460_srev_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Revenue" will fall" |
| 1242 | `oth460_srev_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Revenue" will be neutral" |
| 1243 | `oth460_srev_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Revenue" will move up" |
| 1244 | `oth460_stld_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Total Debt" (1: fall, 2: neutral, 3: move up)" |
| 1245 | `oth460_stpe_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Total Plan Expected Return" (1: fall, 2: neutral, 3: move-up)" |
| 1246 | `oth460_stpi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Total Plan Interest Cost' (1: fall, 2: neutral, 3: move up) |
| 1247 | `oth460_stpr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Total Plan Other Expense" (1: fall, 2: neutral, 3: move-up)" |
| 1248 | `oth460_stps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Total Plan Service Cost' (1: fall, 2: neutral, 3: move up) |
| 1249 | `oth460_stsi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Total Special Items" (1: fall, 2: neutral, 3: move-up)" |
| 1250 | `oth460_stxi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Total Extraordinary Items" (1: fall, 2: neutral, 3: move up)" |
| 1251 | `oth460_suie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Unusual Expense (Income)' (1: fall, 2: neutral, 3: move up) |
| 1252 | `oth460_suie_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unusual Expense (Income)" will fall" |
| 1253 | `oth460_suie_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unusual Expense (Income)" will be neutral" |
| 1254 | `oth460_suie_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Unusual Expense (Income)" will be move-up" |
| 1255 | `oth460_suit_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Non-Recurring Items, Total" (1: fall, 2: neutral, 3: move up)" |
| 1256 | `oth460_suit_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Non-Recurring Items, Total" will fall" |
| 1257 | `oth460_suit_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Non-Recurring Items, Total" will be neutral" |
| 1258 | `oth460_suit_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Non-Recurring Items, Total' will move up |
| 1259 | `oth460_tiat_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Net Income After Taxes" (1: fall, 2: neutral, 3: move-up)" |
| 1260 | `oth460_trix_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of TRIX" (1: fall, 2: neutral, 3: move-up)" |
| 1261 | `oth460_trix_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'TRIX' will fall |
| 1262 | `oth460_trix_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of TRIX" will be neutral" |
| 1263 | `oth460_trix_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of TRIX" will move up" |
| 1264 | `oth460_trkdpit_intfv_xgb_dl8_d1_xido_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Discontinued Operations" (1: fall, 2: neutral, 3: move-up)" |
| 1265 | `oth460_trkdpit_intfv_xgb_dl8_d1_xido_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Discontinued Operations' will fall |
| 1266 | `oth460_trkdpit_intfv_xgb_dl8_d1_xido_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations" will be neutral" |
| 1267 | `oth460_trkdpit_intfv_xgb_dl8_d1_xido_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Discontinued Operations" will be move-up" |
| 1268 | `oth460_tsi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of True Strength Index" (1: fall, 2: neutral, 3: move-up)" |
| 1269 | `oth460_tstk_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Treasury Stock - Total (All Capital)" (1: fall, 2: neutral, 3: move-up)" |
| 1270 | `oth460_tstk_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Stock - Total (All Capital)" will fall" |
| 1271 | `oth460_tstk_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Stock - Total (All Capital)" will be neutral" |
| 1272 | `oth460_tstk_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Treasury Stock - Total (All Capital)" will move up" |
| 1273 | `oth460_ttax_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Provision for Income Taxes" (1: fall, 2: neutral, 3: move-up)" |
| 1274 | `oth460_ttax_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Provision for Income Taxes" will fall" |
| 1275 | `oth460_ttax_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Provision for Income Taxes" will be neutral" |
| 1276 | `oth460_ttax_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Provision for Income Taxes" will be move-up" |
| 1277 | `oth460_vadl_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Revenue - Long Term" (1: fall, 2: neutral, 3: move-up)" |
| 1278 | `oth460_vadv_class` | MATRIX | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Predicted trend of Advertising Expense, Supplemental" (1: fall, 2: neutral, 3: move-up)" |
| 1279 | `oth460_vama_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Amort of Acquisition Costs, Supplemental" (1: fall, 2: neutral, 3: move up)" |
| 1280 | `oth460_vama_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amort of Acquisition Costs, Supplemental" will fall" |
| 1281 | `oth460_vama_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amort of Acquisition Costs, Supplemental" will be neutral" |
| 1282 | `oth460_vama_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Amort of Acquisition Costs, Supplemental" will move up" |
| 1283 | `oth460_vctc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Current Tax - Total" (1: fall, 2: neutral, 3: move-up)" |
| 1284 | `oth460_vctd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Current Tax - Domestic" (1: fall, 2: neutral, 3: move-up)" |
| 1285 | `oth460_vctf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Current Tax - Foreign" (1: fall, 2: neutral, 3: move-up)" |
| 1286 | `oth460_vctl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Current Tax - Local' (1: fall, 2: neutral, 3: move up) |
| 1287 | `oth460_vcto_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Current Tax - Other" (1: fall, 2: neutral, 3: move-up)" |
| 1288 | `oth460_vctr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Current Tax - Total' (1: fall, 2: neutral, 3: move up) |
| 1289 | `oth460_vdpp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Domestic Pension Plan Expense" (1: fall, 2: neutral, 3: move up)" |
| 1290 | `oth460_vdtc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Tax - Total" (1: fall, 2: neutral, 3: move-up)" |
| 1291 | `oth460_vdtd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Tax - Domestic" (1: fall, 2: neutral, 3: move-up)" |
| 1292 | `oth460_vdtf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Tax - Foreign" (1: fall, 2: neutral, 3: move-up)" |
| 1293 | `oth460_vdtl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Tax - Local" (1: fall, 2: neutral, 3: move-up)" |
| 1294 | `oth460_vdto_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Deferred Tax - Other' (1: fall, 2: neutral, 3: move up) |
| 1295 | `oth460_vdtr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Deferred Tax - Total" (1: fall, 2: neutral, 3: move-up)" |
| 1296 | `oth460_veia_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Equity in Affiliates, Supplemental" (1: fall, 2: neutral, 3: move-up)" |
| 1297 | `oth460_veia_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Equity in Affiliates, Supplemental" will fall" |
| 1298 | `oth460_veia_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Equity in Affiliates, Supplemental" will be neutral" |
| 1299 | `oth460_veia_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Equity in Affiliates, Supplemental' will move up |
| 1300 | `oth460_veps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'EPS, Supplemental' (1: fall, 2: neutral, 3: move up) |
| 1301 | `oth460_veps_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of EPS, Supplemental" will be fall" |
| 1302 | `oth460_veps_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of EPS, Supplemental" will be neutral" |
| 1303 | `oth460_veps_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of EPS, Supplemental" will be move-up" |
| 1304 | `oth460_vfic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest Cost - Foreign" (1: fall, 2: neutral, 3: move-up)" |
| 1305 | `oth460_vfpp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Foreign Pension Plan Expense" (1: fall, 2: neutral, 3: move-up)" |
| 1306 | `oth460_vfsc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Service Cost - Foreign" (1: fall, 2: neutral, 3: move up)" |
| 1307 | `oth460_vfxr_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Expected Return on Assets - Foreign" (1: fall, 2: neutral, 3: move up)" |
| 1308 | `oth460_vgla_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of (Gain) Loss on Sale of Assets, Suppl." (1: fall, 2: neutral, 3: move up)" |
| 1309 | `oth460_vi_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Vortex Indicator" (1: fall, 2: neutral, 3: move-up)" |
| 1310 | `oth460_viac_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Normalized Inc. Avail to Com." (1: fall, 2: neutral, 3: move-up)" |
| 1311 | `oth460_viac_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized Inc. Avail to Com." will fall" |
| 1312 | `oth460_viac_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized Inc. Avail to Com." will be neutral" |
| 1313 | `oth460_vias_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Impairment-Assets Held for Sale, Suppl." (1: fall, 2: neutral, 3: move-up)" |
| 1314 | `oth460_vias_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Impairment-Assets Held for Sale, Suppl.' will fall |
| 1315 | `oth460_vias_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Sale, Suppl." will be neutral" |
| 1316 | `oth460_vias_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Sale, Suppl." will be move-up" |
| 1317 | `oth460_viat_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Normalized Income After Taxes" (1: fall, 2: neutral, 3: move-up)" |
| 1318 | `oth460_viat_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Normalized Income After Taxes' will fall |
| 1319 | `oth460_viat_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized Income After Taxes" will be neutral" |
| 1320 | `oth460_viat_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Normalized Income After Taxes" will move up" |
| 1321 | `oth460_viau_class` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Predicted trend of Impairment-Assets Held for Use, Suppl." (1: fall, 2: neutral, 3: move-up)" |
| 1322 | `oth460_viau_l1` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Use, Suppl." will be fall" |
| 1323 | `oth460_viau_l2` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Use, Suppl." will be neutral" |
| 1324 | `oth460_viau_l3` | MATRIX | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | The probability that the future trend of Impairment-Assets Held for Use, Suppl." will move up" |
| 1325 | `oth460_vicd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Interest Cost - Domestic' (1: fall, 2: neutral, 3: move up) |
| 1326 | `oth460_vicd_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Cost - Domestic" will fall" |
| 1327 | `oth460_vicd_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Cost - Domestic" will be neutral" |
| 1328 | `oth460_vicd_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Interest Cost - Domestic' will move up |
| 1329 | `oth460_vinc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest Costs" (1: fall, 2: neutral, 3: move up)" |
| 1330 | `oth460_vint_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Intangibles - Net' (1: fall, 2: neutral, 3: move up) |
| 1331 | `oth460_vint_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Intangibles - Net' will fall |
| 1332 | `oth460_vint_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Intangibles - Net" will be neutral" |
| 1333 | `oth460_vint_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Intangibles - Net" will be move-up" |
| 1334 | `oth460_vitn_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Inc Tax Ex Impact of Sp Items' (1: fall, 2: neutral, 3: move-up) |
| 1335 | `oth460_vitt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Income Tax - Total" (1: fall, 2: neutral, 3: move up)" |
| 1336 | `oth460_vmin_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Minority Interest, Supplemental" (1: fall, 2: neutral, 3: move-up)" |
| 1337 | `oth460_vmin_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Minority Interest, Supplemental" will fall" |
| 1338 | `oth460_vmin_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Minority Interest, Supplemental" will be neutral" |
| 1339 | `oth460_vmin_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Minority Interest, Supplemental" will be move-up" |
| 1340 | `oth460_vol_vo_p_1m_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of 'Volatility of Volume/Price, 1M' (1: fall, 2: neutral, 3: move up) |
| 1341 | `oth460_vol_vo_p_1m_l1` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Volatility of Volume/Price, 1M' will fall |
| 1342 | `oth460_vol_vo_p_1m_l2` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Volatility of Volume/Price, 1M' will be neutral |
| 1343 | `oth460_vol_vo_p_1m_l3` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Volatility of volume/price, 1M' will move up |
| 1344 | `oth460_votd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Domestic Tax - Other" (1: fall, 2: neutral, 3: move-up)" |
| 1345 | `oth460_voto_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Tax" (1: fall, 2: neutral, 3: move-up)" |
| 1346 | `oth460_voto_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Tax" will be fall" |
| 1347 | `oth460_voto_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Other Tax" will be neutral" |
| 1348 | `oth460_voto_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Other Tax' will move up |
| 1349 | `oth460_vpic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Interest Cost - Post-Retirement" (1: fall, 2: neutral, 3: move-up)" |
| 1350 | `oth460_vpic_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Cost - Post-Retirement" will be fall" |
| 1351 | `oth460_vpic_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Interest Cost - Post-Retirement" will be neutral" |
| 1352 | `oth460_vpic_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Interest Cost - Post-Retirement' will move up |
| 1353 | `oth460_vpsc_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Service Cost - Post-Retirement" (1: fall, 2: neutral, 3: move up)" |
| 1354 | `oth460_vpt_class` | MATRIX | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Predicted trend of Volume Price Trend" (1: fall, 2: neutral, 3: move-up)" |
| 1355 | `oth460_vpti_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Normalized Income Before Taxes" (1: fall, 2: neutral, 3: move-up)" |
| 1356 | `oth460_vres_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Restructuring Charge, Supplemental" (1: fall, 2: neutral, 3: move-up)" |
| 1357 | `oth460_vrpe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Post-Retirement Plan Expense" (1: fall, 2: neutral, 3: move-up)" |
| 1358 | `oth460_vscd_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Service Cost - Domestic" (1: fall, 2: neutral, 3: move-up)" |
| 1359 | `oth460_vscp_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Stock-Based Compensation, Supplemental" (1: fall, 2: neutral, 3: move-up)" |
| 1360 | `oth460_vtar_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Audit-Related Fees" (1: fall, 2: neutral, 3: move up)" |
| 1361 | `oth460_vtar_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Audit-Related Fees" will be fall" |
| 1362 | `oth460_vtar_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Audit-Related Fees" will be neutral" |
| 1363 | `oth460_vtar_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of 'Audit-Related Fees' will move up |
| 1364 | `oth460_vtau_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Audit Fees' (1: fall, 2: neutral, 3: move up) |
| 1365 | `oth460_vtau_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Audit Fees" will be fall" |
| 1366 | `oth460_vtau_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Audit Fees" will be neutral" |
| 1367 | `oth460_vtau_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Audit Fees" will move up" |
| 1368 | `oth460_vtcl_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Total Capital Leases, Supplemental" (1: fall, 2: neutral, 3: move-up)" |
| 1369 | `oth460_vtdt_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Domestic Tax' (1: fall, 2: neutral, 3: move up) |
| 1370 | `oth460_vtft_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Foreign Tax" (1: fall, 2: neutral, 3: move-up)" |
| 1371 | `oth460_vtit_class` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Predicted trend of 'Income Tax by Region - Total' (1: fall, 2: neutral, 3: move up) |
| 1372 | `oth460_vtit_l1` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Tax by Region - Total" will fall" |
| 1373 | `oth460_vtit_l2` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Tax by Region - Total" will be neutral" |
| 1374 | `oth460_vtit_l3` | MATRIX | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | The probability that the future trend of Income Tax by Region - Total" will be move-up" |
| 1375 | `oth460_vtof_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of All Other Fees" (1: fall, 2: neutral, 3: move-up)" |
| 1376 | `oth460_vtol_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Total Operating Leases, Supplemental" (1: fall, 2: neutral, 3: move-up)" |
| 1377 | `oth460_vtol_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Operating Leases, Supplemental" will fall" |
| 1378 | `oth460_vtol_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Operating Leases, Supplemental" will be neutral" |
| 1379 | `oth460_vtol_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Total Operating Leases, Supplemental" will move up" |
| 1380 | `oth460_vtpe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Total Pension Expense" (1: fall, 2: neutral, 3: move-up)" |
| 1381 | `oth460_vtps_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of 'Prior Service Cost - Domestic' (1: fall, 2: neutral, 3: move up) |
| 1382 | `oth460_vttf_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Tax Fees" (1: fall, 2: neutral, 3: move-up)" |
| 1383 | `oth460_vuie_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Unusual Expense (Income), Suppl." (1: fall, 2: neutral, 3: move-up)" |
| 1384 | `oth460_vxag_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Actuarial Gains and Losses - Domestic" (1: fall, 2: neutral, 3: move up)" |
| 1385 | `oth460_vxct_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Curtailments & Settlements - Domestic" (1: fall, 2: neutral, 3: move-up)" |
| 1386 | `oth460_vxpe_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Post-Retirement, Net" (1: fall, 2: neutral, 3: move-up)" |
| 1387 | `oth460_vxpo_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Other Pension, Net - Domestic" (1: fall, 2: neutral, 3: move up)" |
| 1388 | `oth460_wr_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Williams %R" (1: fall, 2: neutral, 3: move up)" |
| 1389 | `oth460_xnic_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Income Available to Com Incl ExtraOrd" (1: fall, 2: neutral, 3: move-up)" |
| 1390 | `oth460_xtra_class` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Predicted trend of Extraordinary Item" (1: fall, 2: neutral, 3: move-up)" |
| 1391 | `oth460_xtra_l1` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Extraordinary Item" will fall" |
| 1392 | `oth460_xtra_l2` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Extraordinary Item" will be neutral" |
| 1393 | `oth460_xtra_l3` | MATRIX | 1.000 | 其他 | 0 | — | — | — | UNTESTED | The probability that the future trend of Extraordinary Item" will move up" |

## 六、本地回测证据

- 本地累计回测 **13** 条；其中 `ra_failed_checks` 为空的 **5** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `P0gdMOzJ` | 1.22 | 0.37 | 0.91 | 0.46 | 0.39 | 0 | l4_probe1 | `group_rank(signed_power(subtract(ts_zscore(oth460_float_to_l3,250), ts_zscore(oth460_float` |
| `LLZA5dmn` | 0.53 | 0.13 | -0.09 | 0.55 | 0.36 | 0 | l4_probe1 | `signed_power(subtract(ts_zscore(ts_backfill(oth460_float_to_l3,60),250), ts_zscore(ts_back` |
| `RR6nA1le` | 0.44 | 0.10 | 0.04 | 0.63 | 0.38 | 0 | l4_probe1 | `signed_power(subtract(ts_zscore(oth460_float_to_l3,250), ts_zscore(oth460_float_to_l1,250)` |
| `npdAPkk3` | 0.07 | 0.01 | -0.10 | -0.14 | 0.04 | ["LOW_SHARPE | 254 | `group_rank(oth460_es_sale_ntm_r1m_l3,subindustry)` |
| `vRrO2nxQ` | 0.05 | 0.01 | -0.07 | -0.17 | 0.04 | ["LOW_SHARPE | 254 | `group_rank(subtract(oth460_es_sale_ntm_r1m_l3,oth460_es_sale_ntm_r1m_l1),subindustry)` |
| `wpbM9EG1` | 0.01 | 0.00 | -0.45 | 0.00 | 0.33 | 0 | l4_probe1 | `signed_power(subtract(ts_zscore(oth460_divyld_bb_l3,250), ts_zscore(oth460_divyld_bb_l1,25` |
| `E5pVR0om` | -0.36 | -0.11 | -0.44 | -0.12 | 0.03 | ["LOW_SHARPE | 254 | `group_rank(oth460_1l_dlts,subindustry)` |
| `JjNPQ0Yl` | -0.37 | -0.11 | -0.44 | -0.13 | 0.03 | ["LOW_SHARPE | 254 | `group_rank(subtract(oth460_1l_dlts,oth460_3l_dlts),subindustry)` |
| `P02MgrrW` | -0.39 | -0.12 | -0.89 | -0.11 | 0.02 | ["LOW_SHARPE | 254 | `group_rank(oth460_fincf_l1,subindustry)` |
| `akbVx2M1` | -0.45 | -0.15 | -0.91 | -0.15 | 0.02 | ["LOW_SHARPE | 254 | `group_rank(subtract(oth460_fincf_l1,oth460_fincf_l3),subindustry)` |
| `akbVx2X2` | -0.50 | -0.17 | -0.62 | -0.31 | 0.04 | ["LOW_SHARPE | 254 | `group_rank(oth460_sopi_l3,subindustry)` |
| `9qjEWPP2` | -0.50 | -0.17 | -0.63 | -0.32 | 0.04 | ["LOW_SHARPE | 254 | `group_rank(subtract(oth460_sopi_l3,oth460_sopi_l1),subindustry)` |
| `786Eonm1` | -0.53 | -0.23 | -0.02 | -0.46 | 0.22 | 0 | l4_probe1 | `signed_power(subtract(ts_zscore(oth460_viac_l3,250), ts_zscore(oth460_viac_l1,250)), 3)` |

## 七、判死记录（sealed dead_end）

- `EUR-W254-OTHER460-FORWARD-PROBABILITY-PAIRS`（2026-09-25）family=other460 four target probability directions SUBINDUSTRY decay4：{"dataset": "other460", "wave": "254", "scope": "exact_structures", "whole_dataset_dead": false, "expressions": ["group_rank(oth460_sopi_l3,subindustry)", "group_rank(oth460_1l_dlts,subindustry)", "group_rank(oth460_fincf_l1,subindustry)", "group_rank(oth460_es_sale_ntm_r1m_l3,subindustry)", "group_rank(subtract(oth460_sopi_l3,oth460_sopi_l1),subindustry)", "group_rank(subtract(oth460_1l_dlts,oth4

