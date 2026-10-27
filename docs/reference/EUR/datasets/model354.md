# model354 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `model354` |
| 名称 | Comprehensive Factor Analytics Data |
| 类别 | MODEL |
| 数据字段数(平台) | 236 |
| 覆盖率 | 1.0 |
| 平台已有 alpha | 77 |
| valueScore | 4.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | VECTOR |
| delay | 1 |
| 状态 | scanned |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset provides a mapping between Refinitiv Instrument Codes (RICs) and Bloomberg IDs, enabling seamless cross-referencing of securities between the two major financial data platforms. The mapping is maintained and updated by the security master team, with historical and current files available to support legacy and new systems. While not intended for general research or alpha generation, this mapping is crucial for data integration, ensuring consistency and accuracy when combining datasets from different vendors or when aligning security identifiers across research, trading, and risk management systems.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **236** |
| 类型分布 | VECTOR×236 |
| 平均覆盖率 | **1.000** |
| 覆盖率区间 | 1.00 ~ 1.00 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 优（覆盖 ≥90%，可直接做尽） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 236 | 100.0% |
| 中 (0.70–0.90) | 0 | 0.0% |
| 低 (0.50–0.70) | 0 | 0.0% |
| 稀疏 (<0.50) | 0 | 0.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNTESTED | 236 | 100.0% |

- 该数据集全部字段**尚未实测**（UNTESTED）⇒ 优先做尽

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 修正与预期 | 134 | 1.00 | mdl354_group_pt1divyld_exp、mdl354_group_pt1es_ebitda_fy1_d1m、mdl354_group_pt1es_ebitda_fy1_d3m |
| 盈利与财务 | 74 | 1.00 | mdl354_group_pt11yf_dlyspe、mdl354_group_pt11yf_ep、mdl354_group_pt12yf_dlyspe |
| 宏观与行业 | 17 | 1.00 | mdl354_group_pt1ac_5y_sale、mdl354_group_pt1country、mdl354_group_pt1gr_5y_sale |
| 价量与波动 | 6 | 1.00 | mdl354_group_pt1d1ntr、mdl354_group_pt1psale、mdl354_group_pt1psale_fy1 |
| 其他 | 4 | 1.00 | mdl354_group_pt1bookp、mdl354_group_pt1bookp_fy1、mdl354_group_pt1pbt |
| 元数据与非信号 | 1 | 1.00 | mdl354_group_pt1item |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `mdl354_group_pt11yf_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking earnings yield for the next fiscal year. |
| 2 | `mdl354_group_pt11yf_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on forward-looking earnings for the next fiscal year. |
| 3 | `mdl354_group_pt12yf_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking earnings yield for the second fiscal year ahead. |
| 4 | `mdl354_group_pt12yf_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on forward-looking earnings for the second fiscal year ahead. |
| 5 | `mdl354_group_pt1ac_5y_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of sales over the past 5 years. |
| 6 | `mdl354_group_pt1b_mtl_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backward-looking earnings yield based on the last twelve months. |
| 7 | `mdl354_group_pt1b_mtl_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on backward-looking earnings for the last twelve months. |
| 8 | `mdl354_group_pt1bookp` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Book value per share of the company. |
| 9 | `mdl354_group_pt1bookp_fy1` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Forward-looking book value per share for the next fiscal year. |
| 10 | `mdl354_group_pt1cfoyld` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow yield based on operating cash flows. |
| 11 | `mdl354_group_pt1cfoyld_fy1` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking cash flow yield for the next fiscal year. |
| 12 | `mdl354_group_pt1country` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country of domicile for the company. |
| 13 | `mdl354_group_pt1d1ntr` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily return of the stock. |
| 14 | `mdl354_group_pt1d_mtl_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backward-looking earnings yield based on the last twelve months (diluted). |
| 15 | `mdl354_group_pt1d_mtl_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on backward-looking diluted earnings for the last twelve months. |
| 16 | `mdl354_group_pt1divyld_exp` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Expected dividend yield based on analyst forecasts. |
| 17 | `mdl354_group_pt1divyld_fy1` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking dividend yield for the next fiscal year. |
| 18 | `mdl354_group_pt1divyld_sh` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholder dividend yield based on trailing dividends. |
| 19 | `mdl354_group_pt1divyld_trl` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing dividend yield based on historical dividends. |
| 20 | `mdl354_group_pt1dly_lf_org` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth-adjusted free cash flow yield. |
| 21 | `mdl354_group_pt1dlyfcf` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow yield based on trailing free cash flows. |
| 22 | `mdl354_group_pt1ebit_ev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes (EBIT) divided by enterprise value. |
| 23 | `mdl354_group_pt1ebitda_ev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation, and amortization (EBITDA) divided by enterprise value. |
| 24 | `mdl354_group_pt1es_ebitda_fy1_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, updated daily. |
| 25 | `mdl354_group_pt1es_ebitda_fy1_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, updated monthly. |
| 26 | `mdl354_group_pt1es_ebitda_fy1_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, rolling monthly. |
| 27 | `mdl354_group_pt1es_ebitda_fy1_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, rolling quarterly. |
| 28 | `mdl354_group_pt1es_ebitda_ntm_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, updated daily. |
| 29 | `mdl354_group_pt1es_ebitda_ntm_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, updated monthly. |
| 30 | `mdl354_group_pt1es_ebitda_ntm_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, rolling monthly. |
| 31 | `mdl354_group_pt1es_ebitda_ntm_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, rolling quarterly. |
| 32 | `mdl354_group_pt1es_roe_fy1_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, updated daily. |
| 33 | `mdl354_group_pt1es_roe_fy1_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, updated monthly. |
| 34 | `mdl354_group_pt1es_roe_fy1_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, rolling monthly. |
| 35 | `mdl354_group_pt1es_roe_fy1_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, rolling quarterly. |
| 36 | `mdl354_group_pt1es_roe_ntm_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, updated daily. |
| 37 | `mdl354_group_pt1es_roe_ntm_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, updated monthly. |
| 38 | `mdl354_group_pt1es_roe_ntm_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, rolling monthly. |
| 39 | `mdl354_group_pt1es_roe_ntm_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, rolling quarterly. |
| 40 | `mdl354_group_pt1es_sale_fy1_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, updated daily. |
| 41 | `mdl354_group_pt1es_sale_fy1_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, updated monthly. |
| 42 | `mdl354_group_pt1es_sale_fy1_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, rolling monthly. |
| 43 | `mdl354_group_pt1es_sale_fy1_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, rolling quarterly. |
| 44 | `mdl354_group_pt1es_sale_ntm_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, updated daily. |
| 45 | `mdl354_group_pt1es_sale_ntm_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, updated monthly. |
| 46 | `mdl354_group_pt1es_sale_ntm_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, rolling monthly. |
| 47 | `mdl354_group_pt1es_sale_ntm_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, rolling quarterly. |
| 48 | `mdl354_group_pt1gr_5y_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of sales over the past 5 years. |
| 49 | `mdl354_group_pt1gr_fy1_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Expected growth rate of sales for the next fiscal year. |
| 50 | `mdl354_group_pt1gr_fy2_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Expected growth rate of sales for the second fiscal year ahead. |
| 51 | `mdl354_group_pt1gr_intr_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of sales based on historical trends. |
| 52 | `mdl354_group_pt1gva_mmocer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation average for the stock. |
| 53 | `mdl354_group_pt1item` | VECTOR | 1.000 | 元数据与非信号 | 0 | — | — | — | UNTESTED | Identifier for the specific data item. |
| 54 | `mdl354_group_pt1m1d_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, updated daily. |
| 55 | `mdl354_group_pt1m1d_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, updated daily. |
| 56 | `mdl354_group_pt1m1d_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, updated daily. |
| 57 | `mdl354_group_pt1m1d_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, updated daily. |
| 58 | `mdl354_group_pt1m1d_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, updated daily. |
| 59 | `mdl354_group_pt1m1d_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, updated daily. |
| 60 | `mdl354_group_pt1m1d_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, updated daily. |
| 61 | `mdl354_group_pt1m1d_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, updated daily. |
| 62 | `mdl354_group_pt1m1d_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, updated daily. |
| 63 | `mdl354_group_pt1m1d_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, updated daily. |
| 64 | `mdl354_group_pt1m1r_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, rolling monthly. |
| 65 | `mdl354_group_pt1m1r_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, rolling monthly. |
| 66 | `mdl354_group_pt1m1r_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, rolling monthly. |
| 67 | `mdl354_group_pt1m1r_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, rolling monthly. |
| 68 | `mdl354_group_pt1m1r_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, rolling monthly. |
| 69 | `mdl354_group_pt1m1r_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, rolling monthly. |
| 70 | `mdl354_group_pt1m1r_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, rolling monthly. |
| 71 | `mdl354_group_pt1m1r_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, rolling monthly. |
| 72 | `mdl354_group_pt1m1r_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, rolling monthly. |
| 73 | `mdl354_group_pt1m1r_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, rolling monthly. |
| 74 | `mdl354_group_pt1m21yf_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on forward-looking earnings for the next twelve months. |
| 75 | `mdl354_group_pt1m3d_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, updated monthly. |
| 76 | `mdl354_group_pt1m3d_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, updated monthly. |
| 77 | `mdl354_group_pt1m3d_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, updated monthly. |
| 78 | `mdl354_group_pt1m3d_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, updated monthly. |
| 79 | `mdl354_group_pt1m3d_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, updated monthly. |
| 80 | `mdl354_group_pt1m3d_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, updated monthly. |
| 81 | `mdl354_group_pt1m3d_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, updated monthly. |
| 82 | `mdl354_group_pt1m3d_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, updated monthly. |
| 83 | `mdl354_group_pt1m3d_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, updated monthly. |
| 84 | `mdl354_group_pt1m3d_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, updated monthly. |
| 85 | `mdl354_group_pt1m3r_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, rolling quarterly. |
| 86 | `mdl354_group_pt1m3r_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, rolling quarterly. |
| 87 | `mdl354_group_pt1m3r_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, rolling quarterly. |
| 88 | `mdl354_group_pt1m3r_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, rolling quarterly. |
| 89 | `mdl354_group_pt1m3r_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, rolling quarterly. |
| 90 | `mdl354_group_pt1m3r_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, rolling quarterly. |
| 91 | `mdl354_group_pt1m3r_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, rolling quarterly. |
| 92 | `mdl354_group_pt1m3r_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, rolling quarterly. |
| 93 | `mdl354_group_pt1m3r_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, rolling quarterly. |
| 94 | `mdl354_group_pt1m3r_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, rolling quarterly. |
| 95 | `mdl354_group_pt1mtn_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking earnings yield for the next twelve months. |
| 96 | `mdl354_group_pt1ntr_pt` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Return based on the target price relative to the current price. |
| 97 | `mdl354_group_pt1pbt` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Tangible book value per share of the company. |
| 98 | `mdl354_group_pt1psale` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-sales ratio based on trailing sales. |
| 99 | `mdl354_group_pt1psale_fy1` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-sales ratio based on forward-looking sales for the next fiscal year. |
| 100 | `mdl354_group_pt1sale_ev` | VECTOR | 1.000 | 其他 | 0 | — | — | — | UNTESTED | Sales divided by enterprise value. |
| 101 | `mdl354_group_pt1spd_1yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of dividends per share for the next fiscal year. |
| 102 | `mdl354_group_pt1spd_2yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of dividends per share for the second fiscal year ahead. |
| 103 | `mdl354_group_pt1spd_rtni_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of dividends per share based on historical trends. |
| 104 | `mdl354_group_pt1spd_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of dividends per share over the past 5 years. |
| 105 | `mdl354_group_pt1spd_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of dividends per share over the past 5 years. |
| 106 | `mdl354_group_pt1spe_1yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of earnings per share for the next fiscal year. |
| 107 | `mdl354_group_pt1spe_2yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of earnings per share for the second fiscal year ahead. |
| 108 | `mdl354_group_pt1spe_rtni_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of earnings per share based on historical trends. |
| 109 | `mdl354_group_pt1spe_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of earnings per share over the past 5 years. |
| 110 | `mdl354_group_pt1spe_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of earnings per share over the past 5 years. |
| 111 | `mdl354_group_pt1speo_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of operating earnings per share over the past 5 years. |
| 112 | `mdl354_group_pt1speo_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of operating earnings per share over the past 5 years. |
| 113 | `mdl354_group_pt1spfc_1yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of cash flow per share for the next fiscal year. |
| 114 | `mdl354_group_pt1spfc_2yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of cash flow per share for the second fiscal year ahead. |
| 115 | `mdl354_group_pt1spfc_rtni_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of cash flow per share based on historical trends. |
| 116 | `mdl354_group_pt1spfc_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of cash flow per share over the past 5 years. |
| 117 | `mdl354_group_pt1spfc_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of cash flow per share over the past 5 years. |
| 118 | `mdl354_group_pt1ve_fcf` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow divided by enterprise value. |
| 119 | `mdl354_sector_pt11yf_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking earnings yield for the next fiscal year. |
| 120 | `mdl354_sector_pt11yf_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on forward-looking earnings for the next fiscal year. |
| 121 | `mdl354_sector_pt12yf_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking earnings yield for the second fiscal year ahead. |
| 122 | `mdl354_sector_pt12yf_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on forward-looking earnings for the second fiscal year ahead. |
| 123 | `mdl354_sector_pt1ac_5y_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of sales over the past 5 years. |
| 124 | `mdl354_sector_pt1b_mtl_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backward-looking earnings yield based on the last twelve months. |
| 125 | `mdl354_sector_pt1b_mtl_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on backward-looking earnings for the last twelve months. |
| 126 | `mdl354_sector_pt1bookp` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Book value per share of the company. |
| 127 | `mdl354_sector_pt1bookp_fy1` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Forward-looking book value per share for the next fiscal year. |
| 128 | `mdl354_sector_pt1cfoyld` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Cash flow yield based on operating cash flows. |
| 129 | `mdl354_sector_pt1cfoyld_fy1` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking cash flow yield for the next fiscal year. |
| 130 | `mdl354_sector_pt1country` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Country of domicile for the company. |
| 131 | `mdl354_sector_pt1d1ntr` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Daily return of the stock. |
| 132 | `mdl354_sector_pt1d_mtl_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Backward-looking earnings yield based on the last twelve months (diluted). |
| 133 | `mdl354_sector_pt1d_mtl_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on backward-looking diluted earnings for the last twelve months. |
| 134 | `mdl354_sector_pt1divyld_exp` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Expected dividend yield based on analyst forecasts. |
| 135 | `mdl354_sector_pt1divyld_fy1` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking dividend yield for the next fiscal year. |
| 136 | `mdl354_sector_pt1divyld_sh` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Shareholder dividend yield based on trailing dividends. |
| 137 | `mdl354_sector_pt1divyld_trl` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Trailing dividend yield based on historical dividends. |
| 138 | `mdl354_sector_pt1dly_lf_org` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Growth-adjusted free cash flow yield. |
| 139 | `mdl354_sector_pt1dlyfcf` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow yield based on trailing free cash flows. |
| 140 | `mdl354_sector_pt1ebit_ev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest and taxes (EBIT) divided by enterprise value. |
| 141 | `mdl354_sector_pt1ebitda_ev` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Earnings before interest, taxes, depreciation, and amortization (EBITDA) divided by enterprise value. |
| 142 | `mdl354_sector_pt1es_ebitda_fy1_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, updated daily. |
| 143 | `mdl354_sector_pt1es_ebitda_fy1_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, updated monthly. |
| 144 | `mdl354_sector_pt1es_ebitda_fy1_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, rolling monthly. |
| 145 | `mdl354_sector_pt1es_ebitda_fy1_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next fiscal year, rolling quarterly. |
| 146 | `mdl354_sector_pt1es_ebitda_ntm_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, updated daily. |
| 147 | `mdl354_sector_pt1es_ebitda_ntm_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, updated monthly. |
| 148 | `mdl354_sector_pt1es_ebitda_ntm_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, rolling monthly. |
| 149 | `mdl354_sector_pt1es_ebitda_ntm_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for EBITDA for the next twelve months, rolling quarterly. |
| 150 | `mdl354_sector_pt1es_roe_fy1_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, updated daily. |
| 151 | `mdl354_sector_pt1es_roe_fy1_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, updated monthly. |
| 152 | `mdl354_sector_pt1es_roe_fy1_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, rolling monthly. |
| 153 | `mdl354_sector_pt1es_roe_fy1_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next fiscal year, rolling quarterly. |
| 154 | `mdl354_sector_pt1es_roe_ntm_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, updated daily. |
| 155 | `mdl354_sector_pt1es_roe_ntm_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, updated monthly. |
| 156 | `mdl354_sector_pt1es_roe_ntm_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, rolling monthly. |
| 157 | `mdl354_sector_pt1es_roe_ntm_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for return on equity (ROE) for the next twelve months, rolling quarterly. |
| 158 | `mdl354_sector_pt1es_sale_fy1_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, updated daily. |
| 159 | `mdl354_sector_pt1es_sale_fy1_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, updated monthly. |
| 160 | `mdl354_sector_pt1es_sale_fy1_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, rolling monthly. |
| 161 | `mdl354_sector_pt1es_sale_fy1_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next fiscal year, rolling quarterly. |
| 162 | `mdl354_sector_pt1es_sale_ntm_d1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, updated daily. |
| 163 | `mdl354_sector_pt1es_sale_ntm_d3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, updated monthly. |
| 164 | `mdl354_sector_pt1es_sale_ntm_r1m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, rolling monthly. |
| 165 | `mdl354_sector_pt1es_sale_ntm_r3m` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for sales for the next twelve months, rolling quarterly. |
| 166 | `mdl354_sector_pt1gr_5y_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of sales over the past 5 years. |
| 167 | `mdl354_sector_pt1gr_fy1_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Expected growth rate of sales for the next fiscal year. |
| 168 | `mdl354_sector_pt1gr_fy2_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Expected growth rate of sales for the second fiscal year ahead. |
| 169 | `mdl354_sector_pt1gr_intr_sale` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of sales based on historical trends. |
| 170 | `mdl354_sector_pt1gva_mmocer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation average for the stock. |
| 171 | `mdl354_sector_pt1item` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Identifier for the specific data item. |
| 172 | `mdl354_sector_pt1m1d_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, updated daily. |
| 173 | `mdl354_sector_pt1m1d_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, updated daily. |
| 174 | `mdl354_sector_pt1m1d_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, updated daily. |
| 175 | `mdl354_sector_pt1m1d_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, updated daily. |
| 176 | `mdl354_sector_pt1m1d_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, updated daily. |
| 177 | `mdl354_sector_pt1m1d_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, updated daily. |
| 178 | `mdl354_sector_pt1m1d_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, updated daily. |
| 179 | `mdl354_sector_pt1m1d_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, updated daily. |
| 180 | `mdl354_sector_pt1m1d_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, updated daily. |
| 181 | `mdl354_sector_pt1m1d_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, updated daily. |
| 182 | `mdl354_sector_pt1m1r_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, rolling monthly. |
| 183 | `mdl354_sector_pt1m1r_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, rolling monthly. |
| 184 | `mdl354_sector_pt1m1r_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, rolling monthly. |
| 185 | `mdl354_sector_pt1m1r_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, rolling monthly. |
| 186 | `mdl354_sector_pt1m1r_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, rolling monthly. |
| 187 | `mdl354_sector_pt1m1r_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, rolling monthly. |
| 188 | `mdl354_sector_pt1m1r_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, rolling monthly. |
| 189 | `mdl354_sector_pt1m1r_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, rolling monthly. |
| 190 | `mdl354_sector_pt1m1r_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, rolling monthly. |
| 191 | `mdl354_sector_pt1m1r_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, rolling monthly. |
| 192 | `mdl354_sector_pt1m21yf_ep` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Price-to-earnings ratio based on forward-looking earnings for the next twelve months. |
| 193 | `mdl354_sector_pt1m3d_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, updated monthly. |
| 194 | `mdl354_sector_pt1m3d_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, updated monthly. |
| 195 | `mdl354_sector_pt1m3d_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, updated monthly. |
| 196 | `mdl354_sector_pt1m3d_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, updated monthly. |
| 197 | `mdl354_sector_pt1m3d_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, updated monthly. |
| 198 | `mdl354_sector_pt1m3d_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, updated monthly. |
| 199 | `mdl354_sector_pt1m3d_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, updated monthly. |
| 200 | `mdl354_sector_pt1m3d_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, updated monthly. |
| 201 | `mdl354_sector_pt1m3d_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, updated monthly. |
| 202 | `mdl354_sector_pt1m3d_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, updated monthly. |
| 203 | `mdl354_sector_pt1m3r_1yf_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next fiscal year, rolling quarterly. |
| 204 | `mdl354_sector_pt1m3r_1yf_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next fiscal year, rolling quarterly. |
| 205 | `mdl354_sector_pt1m3r_1yf_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next fiscal year, rolling quarterly. |
| 206 | `mdl354_sector_pt1m3r_1yf_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next fiscal year, rolling quarterly. |
| 207 | `mdl354_sector_pt1m3r_cer_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus recommendation for the stock, rolling quarterly. |
| 208 | `mdl354_sector_pt1m3r_mtn_spb_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for book value per share for the next twelve months, rolling quarterly. |
| 209 | `mdl354_sector_pt1m3r_mtn_spd_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for dividends per share for the next twelve months, rolling quarterly. |
| 210 | `mdl354_sector_pt1m3r_mtn_spe_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for earnings per share for the next twelve months, rolling quarterly. |
| 211 | `mdl354_sector_pt1m3r_mtn_spfc_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus estimate for cash flow per share for the next twelve months, rolling quarterly. |
| 212 | `mdl354_sector_pt1m3r_pt_se` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Analyst consensus target price for the stock, rolling quarterly. |
| 213 | `mdl354_sector_pt1mtn_dlyspe` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Forward-looking earnings yield for the next twelve months. |
| 214 | `mdl354_sector_pt1ntr_pt` | VECTOR | 1.000 | 修正与预期 | 0 | — | — | — | UNTESTED | Return based on the target price relative to the current price. |
| 215 | `mdl354_sector_pt1pbt` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Tangible book value per share of the company. |
| 216 | `mdl354_sector_pt1psale` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-sales ratio based on trailing sales. |
| 217 | `mdl354_sector_pt1psale_fy1` | VECTOR | 1.000 | 价量与波动 | 0 | — | — | — | UNTESTED | Price-to-sales ratio based on forward-looking sales for the next fiscal year. |
| 218 | `mdl354_sector_pt1sale_ev` | VECTOR | 1.000 | 宏观与行业 | 0 | — | — | — | UNTESTED | Sales divided by enterprise value. |
| 219 | `mdl354_sector_pt1spd_1yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of dividends per share for the next fiscal year. |
| 220 | `mdl354_sector_pt1spd_2yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of dividends per share for the second fiscal year ahead. |
| 221 | `mdl354_sector_pt1spd_rtni_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of dividends per share based on historical trends. |
| 222 | `mdl354_sector_pt1spd_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of dividends per share over the past 5 years. |
| 223 | `mdl354_sector_pt1spd_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of dividends per share over the past 5 years. |
| 224 | `mdl354_sector_pt1spe_1yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of earnings per share for the next fiscal year. |
| 225 | `mdl354_sector_pt1spe_2yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of earnings per share for the second fiscal year ahead. |
| 226 | `mdl354_sector_pt1spe_rtni_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of earnings per share based on historical trends. |
| 227 | `mdl354_sector_pt1spe_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of earnings per share over the past 5 years. |
| 228 | `mdl354_sector_pt1spe_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of earnings per share over the past 5 years. |
| 229 | `mdl354_sector_pt1speo_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of operating earnings per share over the past 5 years. |
| 230 | `mdl354_sector_pt1speo_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of operating earnings per share over the past 5 years. |
| 231 | `mdl354_sector_pt1spfc_1yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of cash flow per share for the next fiscal year. |
| 232 | `mdl354_sector_pt1spfc_2yf_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Expected growth rate of cash flow per share for the second fiscal year ahead. |
| 233 | `mdl354_sector_pt1spfc_rtni_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Intrinsic growth rate of cash flow per share based on historical trends. |
| 234 | `mdl354_sector_pt1spfc_y5_ca` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of cash flow per share over the past 5 years. |
| 235 | `mdl354_sector_pt1spfc_y5_rg` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Annualized compound growth rate of cash flow per share over the past 5 years. |
| 236 | `mdl354_sector_pt1ve_fcf` | VECTOR | 1.000 | 盈利与财务 | 0 | — | — | — | UNTESTED | Free cash flow divided by enterprise value. |

## 六、本地回测证据

- 本地累计回测 **10** 条；其中 `ra_failed_checks` 为空的 **10** 条（⚠ 空不等于过关，2Y 为 NULL 者需复检）

| alpha | S | F | 2Y | sub | TO | RA失败数 | wave | 表达式（截断） |
|---|---:|---:|---:|---:|---:|---|---:|---|
| `pwv7ap73` | 0.27 | 0.04 | -0.67 | 0.00 | 0.40 | 0 | w636a | `signed_power(group_rank(ts_backfill(subtract(vec_avg(mdl354_group_pt1es_roe_fy1_d1m), vec_` |
| `88vLN2zV` | 0.19 | 0.03 | -0.63 | 0.16 | 0.28 | 0 | w636a | `signed_power(group_rank(ts_backfill(vec_avg(mdl354_group_pt1spe_1yf_rg), 22), sector), 3.0` |
| `9qERl2wV` | 0.10 | 0.01 | -0.72 | 0.10 | 0.26 | 0 | w636a | `signed_power(group_rank(ts_backfill(vec_avg(mdl354_group_pt1gr_fy1_sale), 22), sector), 3.` |
| `0mj8Pa72` | 0.07 | 0.01 | -1.19 | 0.06 | 0.22 | 0 | w636a | `group_rank(ts_backfill(vec_avg(mdl354_group_pt1divyld_exp), 22), sector)` |
| `O0J9W2pq` | 0.04 | 0.00 | -1.18 | 0.06 | 0.31 | 0 | w636a | `signed_power(group_rank(ts_backfill(vec_avg(mdl354_group_pt1ntr_pt), 22), sector), 3.0)` |
| `0mj8Pa8r` | 0.00 | 0.00 | -1.41 | 0.18 | 0.33 | 0 | w636a | `signed_power(group_rank(ts_backfill(subtract(vec_avg(mdl354_group_pt1es_ebitda_fy1_d1m), v` |
| `2rjK52KY` | 0.00 | 0.00 | -0.60 | 0.20 | 0.33 | 0 | w636a | `signed_power(group_rank(ts_backfill(subtract(vec_avg(mdl354_group_pt1es_sale_fy1_d1m), vec` |
| `N1eOP2rX` | -0.08 | -0.01 | -1.18 | 0.06 | 0.31 | 0 | w636a | `signed_power(group_rank(ts_backfill(vec_avg(mdl354_group_pt1m1d_mtn_spe_se), 22), sector),` |
| `omoYakKn` | -0.16 | -0.03 | -1.19 | -0.12 | 0.18 | 0 | w636a | `signed_power(group_rank(ts_backfill(vec_avg(mdl354_sector_pt1ntr_pt), 22), sector), 3.0)` |
| `vROmAoL3` | -0.21 | -0.03 | -1.41 | -0.03 | 0.34 | 0 | w636a | `signed_power(group_rank(ts_backfill(subtract(vec_avg(mdl354_group_pt1m1d_1yf_spe_se), vec_` |

## 七、判死记录（sealed dead_end）

- `EUR-NEWS36-NOVELTY-SENT-WEAK`（2026-08-25）family=news36 novelty/phrase/word/confidence concepts：{"dataset": "news36", "id": "EUR-NEWS36-NOVELTY-SENT-WEAK", "reason": "Wave65 56 exprs / 7 slots. Max S0.60 F0.19 (rKjodQr9 relevance-gated inverted neg phrases). Confidence S0.54, phrase S0.51. No cheap-gate. Slow /S/<1 so do not mix PV.", "rule": "Leave news36 standalone novelty/sentiment densify. NEWS whitelist concept track exhausted (news38/36/84/85). Skip news54 timestamps. Next unused non-N
- `EUR-M354-VALUATION-YIELD-WEAK`（2026-08-25）family=model354 group valuation yield concepts：{"dataset": "model354", "id": "EUR-M354-VALUATION-YIELD-WEAK", "reason": "Wave66 56 exprs / 7 slots (FY2/NTM EY, FCF/CFO/div yield, sales/EV, FY1-LTM disagreement). Max S0.26 F0.07 (KP7bgexN). Many TVR 2-4%. No cheap-gate. Do not mix PV.", "rule": "Leave model354 standalone valuation densify. Next unused whitelist: ml_factor_proj low-competition non-return MATRIX concepts (not NEWS, not news54, no

