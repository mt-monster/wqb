# pv37 字段画像（KOR / TOP600 / D1）

- 画像员：字段画像员-pv37 ｜ 画像日期：2026-11-19 ｜ 区域：KOR ｜ 宇宙：TOP600 ｜ 延迟：D1
- 数据集：pv37（Equity Interval Data，category=pv）｜ 平台元数据：coverage=0.734、fieldCount=873、alphaCount=2528、userCount=645、valueScore=2.0、pyramidMultiplier=1.4、dateCreated=2023-11-01
- 拉取方式：`get_datafields(region=KOR, universe=TOP600, delay=1, dataset_id=pv37, filter_sharpe=False, 不传 max_fields)`，全量分页拉取
- 对账：count=873 == platform_count=873 == complete=True，returned=873，无截断（与平台声明一致）
- 说明：描述是唯一语义依据；本集为异构杂烩（PV 类目下混入模板化评估语句、基本面、量价、分析师预期等多族），描述与 id 命名常失配，逐字段按描述归类

## 字段全表（873 字段）

| 字段 id | type | coverage | userCount | alphaCount | 语义（描述摘要） | 角色 |
|---|---|---|---|---|---|---|
| `pv37_001vda` | MATRIX | 0.9999 | 18 | 20 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_01vda` | MATRIX | 0.9999 | 19 | 23 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_03vda` | MATRIX | 0.9999 | 11 | 15 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_06vda` | MATRIX | 0.9999 | 10 | 12 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_081vda` | MATRIX | 0.9999 | 16 | 16 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_0d_tpds` | MATRIX | 0.996 | 6 | 6 | 量价/量能：0-Day Trade Price Downside | 主信号 |
| `pv37_1lcs` | MATRIX | 0.2714 | 5 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_1vda` | MATRIX | 0.9999 | 11 | 14 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_2lcs` | MATRIX | 0.2612 | 3 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_32lcs` | MATRIX | 0.2612 | 3 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_36vda` | MATRIX | 0.9999 | 8 | 8 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_3dls` | MATRIX | 0.5025 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_4dls` | MATRIX | 0.4383 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_4vda` | MATRIX | 0.9999 | 3 | 6 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_54dls` | MATRIX | 0.4389 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_5dls` | MATRIX | 0.3679 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_5vda` | MATRIX | 0.9999 | 6 | 6 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_6vda` | MATRIX | 0.9999 | 4 | 4 | 成交量前瞻预测（vda 族） | 主信号 |
| `pv37_acfn` | MATRIX | 0.3832 | 4 | 4 | 基本面慢变量（裸水平撞规模代理）：Net finance company assets | 主信号 |
| `pv37_adr_ticker` | MATRIX | 0.6452 | 2 | 2 | 分类标识：ADR Ticker | 分组轴 |
| `pv37_adr_ticker_di` | MATRIX | 1.0 | 5 | 8 | 母字段直接指示器（同义标准化版）：ADR Ticker Direct Indicator | 对照 |
| `pv37_algv` | MATRIX | 0.3488 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_1dls` | MATRIX | 0.5768 | 5 | 7 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_1nstq` | MATRIX | 0.7468 | 8 | 8 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_1oscq` | MATRIX | 0.7541 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Quality cash pledge spread | 主信号 |
| `pv37_all_2dls` | MATRIX | 0.5356 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_32dls` | MATRIX | 0.5422 | 5 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_adbs` | MATRIX | 0.7337 | 39 | 79 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_agss` | MATRIX | 0.7379 | 9 | 10 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_aieo` | MATRIX | 0.5943 | 7 | 8 | 基本面慢变量（裸水平撞规模代理）：Operating deposit pledge liabilities | 主信号 |
| `pv37_all_algn` | MATRIX | 0.6942 | 4 | 5 | 基本面慢变量（裸水平撞规模代理）：Net Gain Loss Assets | 主信号 |
| `pv37_all_atcq` | MATRIX | 0.4839 | 4 | 7 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_bcns` | MATRIX | 0.7549 | 9 | 11 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ccns` | MATRIX | 0.7546 | 12 | 20 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_cdav` | MATRIX | 0.7162 | 22 | 73 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_cinx` | MATRIX | 0.7554 | 89 | 178 | 量价/量能：Total x-non-incorporated certificate traded volume | 主信号 |
| `pv37_all_cstq` | MATRIX | 0.5715 | 10 | 12 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ctcv` | MATRIX | 0.5162 | 5 | 6 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_dlts` | MATRIX | 0.7555 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_dltv` | MATRIX | 0.5806 | 4 | 5 | 量价/量能：Total long-term debt volume | 主信号 |
| `pv37_all_dtns` | MATRIX | 0.7267 | 3 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ecns` | MATRIX | 0.7549 | 5 | 8 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_eiuo` | MATRIX | 0.7439 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Operating transaction expense | 主信号 |
| `pv37_all_eoos` | MATRIX | 0.5743 | 3 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_etoq` | MATRIX | 0.6713 | 3 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_fbbs` | MATRIX | 0.7546 | 7 | 14 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_fbds` | MATRIX | 0.7471 | 10 | 11 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_fcfs` | MATRIX | 0.6892 | 6 | 7 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_fcoo` | MATRIX | 0.6971 | 4 | 8 | 基本面慢变量（裸水平撞规模代理）：Operating open asset spread | 主信号 |
| `pv37_all_iabs` | MATRIX | 0.7554 | 14 | 43 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_iads` | MATRIX | 0.7551 | 5 | 9 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_icno` | MATRIX | 0.7521 | 1 | 7 | 基本面慢变量（裸水平撞规模代理）：Operating loan spread | 主信号 |
| `pv37_all_icns` | MATRIX | 0.7447 | 4 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ifpv` | MATRIX | 0.36 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ists` | MATRIX | 0.7131 | 1 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_itpv` | MATRIX | 0.7544 | 6 | 8 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_iucs` | MATRIX | 0.7169 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ixts` | MATRIX | 0.4199 | 3 | 3 | 分类标识：Total assessment of Sale of Transaction Security Exchange | 分组轴 |
| `pv37_all_jads` | MATRIX | 0.6877 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_kcqs` | MATRIX | 0.7168 | 4 | 6 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_laoo` | MATRIX | 0.4824 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating net engagement trend | 主信号 |
| `pv37_all_letq` | MATRIX | 0.7554 | 1 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_lltq` | MATRIX | 0.6849 | 6 | 6 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ltls` | MATRIX | 0.7512 | 2 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_mocq` | MATRIX | 0.4675 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Quality cash management spread | 主信号 |
| `pv37_all_mpns` | MATRIX | 0.7532 | 23 | 33 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_mtps` | MATRIX | 0.7548 | 67 | 151 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_nein` | MATRIX | 0.7014 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Net income earnings | 主信号 |
| `pv37_all_nibx` | MATRIX | 0.755 | 12 | 13 | 基本面慢变量（裸水平撞规模代理）：Net income before extra | 主信号 |
| `pv37_all_nicn` | MATRIX | 0.3879 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Net capital income | 主信号 |
| `pv37_all_niin` | MATRIX | 0.7113 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Net income interest | 主信号 |
| `pv37_all_niis` | MATRIX | 0.7415 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ninn` | MATRIX | 0.5821 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Net income non-operating | 主信号 |
| `pv37_all_nins` | MATRIX | 0.7368 | 4 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_nont` | MATRIX | 0.733 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Net operating expense | 主信号 |
| `pv37_all_ntiv` | MATRIX | 0.7542 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_oiis` | MATRIX | 0.4197 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_pbts` | MATRIX | 0.7542 | 9 | 9 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_pedv` | MATRIX | 0.7537 | 2 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_pics` | MATRIX | 0.7333 | 2 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ppgs` | MATRIX | 0.7134 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_prgs` | MATRIX | 0.7214 | 6 | 7 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ptcs` | MATRIX | 0.6812 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_pxrv` | MATRIX | 0.7233 | 2 | 2 | 分类标识：Total assessment of Value in Revenue Exchange with Payment | 分组轴 |
| `pv37_all_pxto` | MATRIX | 0.4301 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：Operating trade asset | 主信号 |
| `pv37_all_qpic` | MATRIX | 0.7477 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_qred` | MATRIX | 0.748 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_rore` | MATRIX | 0.411 | 3 | 7 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_rpds` | MATRIX | 0.7116 | 3 | 7 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_rrev` | MATRIX | 0.3437 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_rtcv` | MATRIX | 0.5171 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_samt` | MATRIX | 0.7161 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sani` | MATRIX | 0.4447 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sbas` | MATRIX | 0.7544 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sbit` | MATRIX | 0.734 | 28 | 48 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_scur` | MATRIX | 0.7168 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sedv` | MATRIX | 0.7544 | 5 | 9 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_setr` | MATRIX | 0.7406 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sfee` | MATRIX | 0.7264 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sicf` | MATRIX | 0.7465 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sien` | MATRIX | 0.7014 | 3 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sieo` | MATRIX | 0.349 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sinn` | MATRIX | 0.4288 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sinv` | MATRIX | 0.7492 | 1 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_smcq` | MATRIX | 0.7554 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Quality asset management liquidity | 主信号 |
| `pv37_all_smcs` | MATRIX | 0.7554 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_soca` | MATRIX | 0.7071 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_socl` | MATRIX | 0.7553 | 3 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sola` | MATRIX | 0.7511 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sont` | MATRIX | 0.7336 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sopi` | MATRIX | 0.7444 | 12 | 19 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sopp` | MATRIX | 0.725 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sore` | MATRIX | 0.4217 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_sote` | MATRIX | 0.697 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_srev` | MATRIX | 0.7356 | 14 | 17 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_stec` | MATRIX | 0.7131 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_stnr` | MATRIX | 0.7304 | 8 | 9 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_suie` | MATRIX | 0.6076 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_swds` | MATRIX | 0.7544 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_tait` | MATRIX | 0.7476 | 14 | 16 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_tdbs` | MATRIX | 0.5769 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_trsr` | MATRIX | 0.345 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ttax` | MATRIX | 0.7547 | 10 | 14 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_ttiv` | MATRIX | 0.5306 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_vaia` | MATRIX | 0.5666 | 3 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_vbes` | MATRIX | 0.7544 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_vbts` | MATRIX | 0.7542 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_vcap` | MATRIX | 0.4163 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_vdav` | MATRIX | 0.7117 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_veev` | MATRIX | 0.36 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_veia` | MATRIX | 0.6377 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_viac` | MATRIX | 0.7544 | 8 | 9 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_viat` | MATRIX | 0.7544 | 17 | 20 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_viex` | MATRIX | 0.7338 | 1 | 1 | 分类标识：Total assessment of Value in Exchange Transactions | 分组轴 |
| `pv37_all_vmin` | MATRIX | 0.6073 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_vnin` | MATRIX | 0.7399 | 2 | 3 | 基本面慢变量（裸水平撞规模代理）：Net income notifications | 主信号 |
| `pv37_all_vrad` | MATRIX | 0.6794 | 5 | 8 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_all_xeao` | MATRIX | 0.5159 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating asset cash return | 主信号 |
| `pv37_all_xido` | MATRIX | 0.4198 | 0 | 0 | 量价/量能：Total x-identification operations traded volume | 主信号 |
| `pv37_all_xtra` | MATRIX | 0.3493 | 0 | 0 | 量价/量能：Total x-transaction agreement traded volume | 主信号 |
| `pv37_all_yppo` | MATRIX | 0.5369 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating pledge bid asset | 主信号 |
| `pv37_analyst_revisn` | MATRIX | 0.6452 | 2 | 6 | 分析师预期/修正：Analyst Revision | 主信号 |
| `pv37_analyst_revisn_di` | MATRIX | 1.0 | 3 | 4 | 分析师预期/修正：Analyst Revision Direct Indicator | 主信号 |
| `pv37_analyst_uncertainty` | MATRIX | 0.6452 | 1 | 1 | 分析师预期/修正：Analyst Uncertainty | 主信号 |
| `pv37_analyst_uncertainty_di` | MATRIX | 1.0 | 7 | 7 | 分析师预期/修正：Analyst Uncertainty Direct Indicator | 主信号 |
| `pv37_annfv_mfm2_acta` | MATRIX | 0.8345 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_atot` | MATRIX | 0.8726 | 2 | 2 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_bloo` | MATRIX | 0.8659 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_bpao` | MATRIX | 0.8466 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_cnin` | MATRIX | 0.8701 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_deds` | MATRIX | 0.8673 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_dlcl` | MATRIX | 0.7547 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_dtsl` | MATRIX | 0.8561 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_dttl` | MATRIX | 0.8701 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_eltq` | MATRIX | 0.8723 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_inds` | MATRIX | 0.87 | 3 | 3 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_iscs` | MATRIX | 0.8448 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_lctl` | MATRIX | 0.8331 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_lltl` | MATRIX | 0.873 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_ltio` | MATRIX | 0.8077 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_oami` | MATRIX | 0.8379 | 2 | 2 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_octq` | MATRIX | 0.8703 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_olto` | MATRIX | 0.87 | 2 | 2 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_onet` | MATRIX | 0.8668 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_peds` | MATRIX | 0.8673 | 1 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_rcao` | MATRIX | 0.8489 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_rltr` | MATRIX | 0.8601 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_saoo` | MATRIX | 0.7237 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_scor` | MATRIX | 0.834 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_socf` | MATRIX | 0.8699 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_tdbo` | MATRIX | 0.6586 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_vama` | MATRIX | 0.3755 | 0 | 0 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_vami` | MATRIX | 0.8553 | 1 | 1 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_annfv_mfm2_xecs` | MATRIX | 0.8677 | 4 | 5 | MFM2 年化指标，语义不明 | 排除 |
| `pv37_apts` | MATRIX | 0.9516 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_apxv` | MATRIX | 0.3435 | 2 | 3 | 量价/量能：Total x-partnership agreement traded volume | 主信号 |
| `pv37_average_daily_trading_volume` | MATRIX | 0.6783 | 2 | 4 | 量价/量能：Average Daily Trading Volume | 主信号 |
| `pv37_average_daily_trading_volume_di` | MATRIX | 1.0 | 3 | 5 | 母字段直接指示器（同义标准化版）：Average Daily Trading Volume Direct Indicator | 对照 |
| `pv37_b6dls` | MATRIX | 0.5806 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_best_cps` | VECTOR | 0.6555 | 4 | 7 | 分析师一致预期（best 族）：Best CPS estimate | 主信号 |
| `pv37_best_cps_4wk_chg` | VECTOR | 0.6481 | 6 | 12 | 分析师一致预期（best 族）：Best CPS 4-week change | 主信号 |
| `pv37_best_cps_4wk_dn` | VECTOR | 0.6555 | 13 | 24 | 分析师一致预期（best 族）：Best CPS 4-week downgrades | 主信号 |
| `pv37_best_cps_4wk_up` | VECTOR | 0.6555 | 15 | 21 | 分析师一致预期（best 族）：Best CPS 4-week upgrades | 主信号 |
| `pv37_best_cps_chg_pct` | VECTOR | 0.6555 | 3 | 4 | 分析师一致预期（best 族）：Best CPS change percentage | 主信号 |
| `pv37_best_cps_hi` | VECTOR | 0.6555 | 1 | 1 | 分析师一致预期（best 族）：Best CPS high estimate | 主信号 |
| `pv37_best_cps_lo` | VECTOR | 0.6555 | 3 | 9 | 分析师一致预期（best 族）：Best CPS low estimate | 主信号 |
| `pv37_best_cps_median` | VECTOR | 0.6555 | 6 | 9 | 分析师一致预期（best 族）：Best CPS median estimate | 主信号 |
| `pv37_best_cps_numest` | VECTOR | 0.6555 | 3 | 7 | 分析师一致预期（best 族）：Best CPS number of estimates | 主信号 |
| `pv37_best_cps_stddev` | VECTOR | 0.5298 | 1 | 1 | 分析师一致预期（best 族）：Best CPS standard deviation | 主信号 |
| `pv37_best_ebitda` | VECTOR | 0.7311 | 2 | 2 | 分析师一致预期（best 族）：Best EBITDA estimate | 主信号 |
| `pv37_best_ebitda_4wk_chg` | VECTOR | 0.7244 | 16 | 40 | 分析师一致预期（best 族）：Best EBITDA 4-week change | 主信号 |
| `pv37_best_ebitda_4wk_dn` | VECTOR | 0.7311 | 6 | 8 | 分析师一致预期（best 族）：Best EBITDA 4-week downgrades | 主信号 |
| `pv37_best_ebitda_4wk_up` | VECTOR | 0.7311 | 5 | 11 | 分析师一致预期（best 族）：Best EBITDA 4-week upgrades | 主信号 |
| `pv37_best_ebitda_chg_pct` | VECTOR | 0.7311 | 2 | 2 | 分析师一致预期（best 族）：Best EBITDA change percentage | 主信号 |
| `pv37_best_ebitda_hi` | VECTOR | 0.7311 | 0 | 0 | 分析师一致预期（best 族）：Best EBITDA high estimate | 主信号 |
| `pv37_best_ebitda_lo` | VECTOR | 0.7311 | 3 | 4 | 分析师一致预期（best 族）：Best EBITDA low estimate | 主信号 |
| `pv37_best_ebitda_median` | VECTOR | 0.7311 | 8 | 10 | 分析师一致预期（best 族）：Best EBITDA median estimate | 主信号 |
| `pv37_best_ebitda_numest` | VECTOR | 0.7311 | 4 | 5 | 分析师一致预期（best 族）：Best EBITDA number of estimates | 主信号 |
| `pv37_best_ebitda_stddev` | VECTOR | 0.6254 | 0 | 0 | 分析师一致预期（best 族）：Best EBITDA standard deviation | 主信号 |
| `pv37_best_nav` | VECTOR | 0.716 | 3 | 4 | 分析师一致预期（best 族）：Best NAV estimate | 主信号 |
| `pv37_best_nav_4wk_chg` | VECTOR | 0.7084 | 1 | 3 | 分析师一致预期（best 族）：Best NAV 4-week change | 主信号 |
| `pv37_best_nav_4wk_dn` | VECTOR | 0.716 | 3 | 3 | 分析师一致预期（best 族）：Best NAV 4-week downgrades | 主信号 |
| `pv37_best_nav_4wk_up` | VECTOR | 0.716 | 3 | 3 | 分析师一致预期（best 族）：Best NAV 4-week upgrades | 主信号 |
| `pv37_best_nav_chg_pct` | VECTOR | 0.716 | 4 | 12 | 分析师一致预期（best 族）：Best NAV change percentage | 主信号 |
| `pv37_best_nav_hi` | VECTOR | 0.716 | 2 | 3 | 分析师一致预期（best 族）：Best NAV high estimate | 主信号 |
| `pv37_best_nav_lo` | VECTOR | 0.716 | 2 | 2 | 分析师一致预期（best 族）：Best NAV low estimate | 主信号 |
| `pv37_best_nav_median` | VECTOR | 0.716 | 1 | 1 | 分析师一致预期（best 族）：Best NAV median estimate | 主信号 |
| `pv37_best_nav_numest` | VECTOR | 0.716 | 1 | 2 | 分析师一致预期（best 族）：Best NAV Number of Estimates | 主信号 |
| `pv37_best_nav_stddev` | VECTOR | 0.591 | 2 | 2 | 分析师一致预期（best 族）：Best NAV standard deviation | 主信号 |
| `pv37_best_net` | VECTOR | 0.7872 | 3 | 3 | 分析师一致预期（best 族）：Best net profit estimate | 主信号 |
| `pv37_best_net_4wk_chg` | VECTOR | 0.7812 | 29 | 51 | 分析师一致预期（best 族）：Best net profit 4-week change | 主信号 |
| `pv37_best_net_4wk_dn` | VECTOR | 0.7872 | 102 | 238 | 分析师一致预期（best 族）：Best net profit 4-week downgrades | 主信号 |
| `pv37_best_net_4wk_up` | VECTOR | 0.7872 | 44 | 105 | 分析师一致预期（best 族）：Best net profit 4-week upgrades | 主信号 |
| `pv37_best_net_chg_pct` | VECTOR | 0.7872 | 3 | 3 | 分析师一致预期（best 族）：Best net profit change percentage | 主信号 |
| `pv37_best_net_gaap` | VECTOR | 0.8449 | 5 | 8 | 分析师一致预期（best 族）：Best net profit GAAP estimate | 主信号 |
| `pv37_best_net_gaap_4wk_chg` | VECTOR | 0.8389 | 17 | 40 | 分析师一致预期（best 族）：Best net profit GAAP 4-week change | 主信号 |
| `pv37_best_net_gaap_4wk_dn` | VECTOR | 0.7872 | 88 | 144 | 分析师一致预期（best 族）：Best net profit GAAP 4-week downgrades | 主信号 |
| `pv37_best_net_gaap_4wk_up` | VECTOR | 0.7872 | 21 | 58 | 分析师一致预期（best 族）：Best net profit GAAP 4-week upgrades | 主信号 |
| `pv37_best_net_gaap_hi` | VECTOR | 0.845 | 2 | 2 | 分析师一致预期（best 族）：Best net profit GAAP high estimate | 主信号 |
| `pv37_best_net_gaap_lo` | VECTOR | 0.845 | 2 | 2 | 分析师一致预期（best 族）：Best net profit GAAP low estimate | 主信号 |
| `pv37_best_net_gaap_median` | VECTOR | 0.845 | 5 | 10 | 分析师一致预期（best 族）：Best net profit GAAP median estimate | 主信号 |
| `pv37_best_net_gaap_numest` | VECTOR | 0.8449 | 1 | 0 | 分析师一致预期（best 族）：Best net profit GAAP number of estimates | 主信号 |
| `pv37_best_net_gaap_stddev` | VECTOR | 0.7116 | 1 | 0 | 分析师一致预期（best 族）：Best net profit GAAP standard deviation | 主信号 |
| `pv37_best_net_hi` | VECTOR | 0.7872 | 8 | 15 | 分析师一致预期（best 族）：Best Net Profit High Estimate | 主信号 |
| `pv37_best_net_lo` | VECTOR | 0.7872 | 1 | 5 | 分析师一致预期（best 族）：Best net profit low estimate | 主信号 |
| `pv37_best_net_median` | VECTOR | 0.7872 | 4 | 4 | 分析师一致预期（best 族）：Best net profit median estimate | 主信号 |
| `pv37_best_net_numest` | VECTOR | 0.7872 | 2 | 2 | 分析师一致预期（best 族）：Best net profit number of estimates | 主信号 |
| `pv37_best_net_stddev` | VECTOR | 0.6962 | 3 | 4 | 分析师一致预期（best 族）：Best net profit standard deviation | 主信号 |
| `pv37_best_opp_4wk_chg` | VECTOR | 0.316 | 0 | 0 | 分析师一致预期（best 族）：Best Operating Profit 4-Week Change | 主信号 |
| `pv37_best_opp_4wk_dn` | VECTOR | 0.3229 | 0 | 0 | 分析师一致预期（best 族）：Best Operating Profit 4-Week Downgrades | 主信号 |
| `pv37_best_opp_4wk_up` | VECTOR | 0.3229 | 0 | 0 | 分析师一致预期（best 族）：Best operating profit 4-week upgrades | 主信号 |
| `pv37_best_opp_chg_pct` | VECTOR | 0.3229 | 0 | 0 | 分析师一致预期（best 族）：Best operating profit change percentage | 主信号 |
| `pv37_best_opp_hi` | VECTOR | 0.3229 | 0 | 0 | 分析师一致预期（best 族）：Best operating profit high estimate | 主信号 |
| `pv37_best_opp_lo` | VECTOR | 0.3229 | 0 | 0 | 分析师一致预期（best 族）：Best operating profit low estimate | 主信号 |
| `pv37_best_opp_median` | VECTOR | 0.3229 | 1 | 1 | 分析师一致预期（best 族）：Best operating profit median estimate | 主信号 |
| `pv37_best_opp_numest` | VECTOR | 0.3229 | 1 | 1 | 分析师一致预期（best 族）：Best operating profit number of estimates | 主信号 |
| `pv37_best_opp_to_sales` | VECTOR | 0.3208 | 0 | 0 | 分析师一致预期（best 族）：Best operating profit to sales ratio | 主信号 |
| `pv37_best_roa` | VECTOR | 0.7166 | 4 | 5 | 分析师一致预期（best 族）：Best ROA | 主信号 |
| `pv37_best_roa_4wk_chg` | VECTOR | 0.7088 | 18 | 52 | 分析师一致预期（best 族）：Best ROA 4-week change | 主信号 |
| `pv37_best_roa_4wk_dn` | VECTOR | 0.7166 | 1 | 2 | 分析师一致预期（best 族）：Best ROA 4-week down | 主信号 |
| `pv37_best_roa_4wk_up` | VECTOR | 0.7166 | 2 | 4 | 分析师一致预期（best 族）：Best ROA 4-week up | 主信号 |
| `pv37_best_roa_chg_pct` | VECTOR | 0.7166 | 5 | 6 | 分析师一致预期（best 族）：Best ROA change percentage | 主信号 |
| `pv37_best_roa_hi` | VECTOR | 0.7166 | 5 | 10 | 分析师一致预期（best 族）：Best ROA high | 主信号 |
| `pv37_best_roa_lo` | VECTOR | 0.7166 | 3 | 10 | 分析师一致预期（best 族）：Best ROA low | 主信号 |
| `pv37_best_roa_median` | VECTOR | 0.7166 | 2 | 4 | 分析师一致预期（best 族）：Best ROA median | 主信号 |
| `pv37_best_roa_numest` | VECTOR | 0.7166 | 2 | 3 | 分析师一致预期（best 族）：Best ROA number of estimates | 主信号 |
| `pv37_best_roa_stddev` | VECTOR | 0.589 | 1 | 6 | 分析师一致预期（best 族）：Best ROA standard deviation | 主信号 |
| `pv37_beta_vs_acwi_ex_us` | MATRIX | 0.6783 | 20 | 37 | 基本面慢变量（裸水平撞规模代理）：Beta versus ACWI ex US | 主信号 |
| `pv37_beta_vs_acwi_ex_us_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Beta versus ACWI ex US Direct Indicator | 对照 |
| `pv37_beta_vs_country` | MATRIX | 0.6783 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Beta versus Country | 主信号 |
| `pv37_beta_vs_country_di` | MATRIX | 1.0 | 1 | 2 | 母字段直接指示器（同义标准化版）：Beta versus Country Direct Indicator | 对照 |
| `pv37_bs_accrual` | MATRIX | 0.9183 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Accruals on the Balance Sheet | 主信号 |
| `pv37_bs_accrued_income_taxes` | MATRIX | 0.8584 | 8 | 10 | 基本面慢变量（裸水平撞规模代理）：Accrued Income Taxes on the Balance Sheet | 主信号 |
| `pv37_bs_acct_note_rcv` | MATRIX | 0.9805 | 4 | 4 | 基本面慢变量（裸水平撞规模代理）：Account Notes Receivable on the Balance Sheet | 主信号 |
| `pv37_bs_acct_payable` | MATRIX | 0.9025 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：Accounts Payable on the Balance Sheet | 主信号 |
| `pv37_bs_accts_rec_excl_notes_rec` | MATRIX | 1.0 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Accounts Receivable Excluding Notes Receivable on the Balance Sheet | 主信号 |
| `pv37_bs_accum_depr` | MATRIX | 0.8331 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Accumulated Depreciation on the Balance Sheet | 主信号 |
| `pv37_bs_add_paid_in_cap` | MATRIX | 0.9494 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Additional Paid-In Capital on the Balance Sheet | 主信号 |
| `pv37_bs_allow_doubtful_acc_rec` | MATRIX | 0.8704 | 0 | 0 | 量价/量能：Allowance for Doubtful Accounts Receivable on the Balance Sheet | 主信号 |
| `pv37_bs_amt_of_tsy_stock` | MATRIX | 0.8775 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Amount of Treasury Stock on the Balance Sheet | 主信号 |
| `pv37_bs_auth_capital` | MATRIX | 0.9407 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Authorized Capital on the Balance Sheet | 主信号 |
| `pv37_bs_capital_reserve` | MATRIX | 1.0 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Capital Reserve on the Balance Sheet | 主信号 |
| `pv37_bs_cash_near_cash_item` | MATRIX | 0.9944 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Cash and Near Cash Items on the Balance Sheet | 主信号 |
| `pv37_bs_collaterals_cash_mkt_st_inv` | MATRIX | 0.5324 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Collaterals Cash Market Short-Term Investments on the Balance Sheet | 主信号 |
| `pv37_bs_common_stock` | MATRIX | 1.0 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Common Stock on the Balance Sheet | 主信号 |
| `pv37_bs_cur_asset_report` | MATRIX | 0.9243 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Current Asset Report on the Balance Sheet | 主信号 |
| `pv37_bs_cur_liab` | MATRIX | 0.9245 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Current Liabilities on the Balance Sheet | 主信号 |
| `pv37_bs_debt_in_foreign_curr` | MATRIX | 0.4284 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Debt in Foreign Currency on the Balance Sheet | 主信号 |
| `pv37_bs_def_tax_liab` | MATRIX | 0.9686 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Deferred Tax Liability on the Balance Sheet | 主信号 |
| `pv37_bs_disclosed_intangibles` | MATRIX | 0.9872 | 5 | 5 | 基本面慢变量（裸水平撞规模代理）：Disclosed Intangibles on the Balance Sheet | 主信号 |
| `pv37_bs_future_min_oper_lease_oblig` | MATRIX | 0.2578 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Future Minimum Operating Lease Obligation on the Balance Sheet | 主信号 |
| `pv37_bs_goodwill` | MATRIX | 0.6388 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Goodwill on the Balance Sheet | 主信号 |
| `pv37_bs_goodwill_write_off` | MATRIX | 0.4862 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Goodwill write-off on the balance sheet | 主信号 |
| `pv37_bs_gross_fix_asset` | MATRIX | 0.8161 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Gross Fixed Assets on the Balance Sheet | 主信号 |
| `pv37_bs_inventories` | MATRIX | 0.9242 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Inventories on the Balance Sheet | 主信号 |
| `pv37_bs_invest_in_assoc_co` | MATRIX | 0.8483 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Investment in Associate Company on the Balance Sheet | 主信号 |
| `pv37_bs_lt_borrow` | MATRIX | 0.991 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Long-Term Borrowings on the Balance Sheet | 主信号 |
| `pv37_bs_lt_invest` | MATRIX | 0.9907 | 6 | 8 | 基本面慢变量（裸水平撞规模代理）：Long-Term Investments on the Balance Sheet | 主信号 |
| `pv37_bs_mkt_sec_other_st_invest` | MATRIX | 0.9794 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Market securities and other short-term investments | 主信号 |
| `pv37_bs_net_fix_asset` | MATRIX | 0.9944 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Net value of fixed assets after depreciation | 主信号 |
| `pv37_bs_non_depr_decomm_fund` | MATRIX | 0.7629 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Non-depreciable decommissioning fund assets | 主信号 |
| `pv37_bs_non_eqy_rsrv` | MATRIX | 0.5305 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Non-equity reserves | 主信号 |
| `pv37_bs_num_of_shareholders` | MATRIX | 0.6395 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Number of shareholders | 主信号 |
| `pv37_bs_options_outstanding` | MATRIX | 0.444 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Number of outstanding stock options | 主信号 |
| `pv37_bs_other_cur_asset` | MATRIX | 0.9242 | 1 | 4 | 基本面慢变量（裸水平撞规模代理）：Total other current assets | 主信号 |
| `pv37_bs_other_cur_asset_less_prepay` | MATRIX | 1.0 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Other current assets less prepayments | 主信号 |
| `pv37_bs_other_cur_liab` | MATRIX | 0.9616 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Total other current liabilities | 主信号 |
| `pv37_bs_other_inv` | MATRIX | 0.9056 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Other investments | 主信号 |
| `pv37_bs_other_lt_liabilities` | MATRIX | 0.9938 | 2 | 5 | 基本面慢变量（裸水平撞规模代理）：Other long-term liabilities | 主信号 |
| `pv37_bs_other_st_liab` | MATRIX | 0.9937 | 8 | 8 | 基本面慢变量（裸水平撞规模代理）：Other short-term liabilities | 主信号 |
| `pv37_bs_par_val` | MATRIX | 0.9938 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Par value of shares | 主信号 |
| `pv37_bs_pension_rsrv` | MATRIX | 0.9812 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Pension reserves | 主信号 |
| `pv37_bs_plant_const_in_prog` | MATRIX | 0.6959 | 14 | 14 | 基本面慢变量（裸水平撞规模代理）：Plant construction projects in progress | 主信号 |
| `pv37_bs_prepay` | MATRIX | 0.866 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Prepayments | 主信号 |
| `pv37_bs_pure_retained_earnings` | MATRIX | 0.9938 | 5 | 5 | 基本面慢变量（裸水平撞规模代理）：Pure retained earnings | 主信号 |
| `pv37_bs_q_announcement_dt` | MATRIX | 0.9945 | 9 | 14 | 时点/状态标识：The announcement date for quarterly balance sheet data | 排除 |
| `pv37_bs_q_fundamental_entry_dt` | MATRIX | 0.9945 | 7 | 12 | 时点/状态标识：Fundamental entry date | 排除 |
| `pv37_bs_q_latest_period_end_dt_full_record` | MATRIX | 0.9945 | 0 | 0 | 时点/状态标识：Latest period end date full record | 排除 |
| `pv37_bs_re_invest` | MATRIX | 0.8697 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Reinvestments | 主信号 |
| `pv37_bs_retain_earn` | MATRIX | 0.9944 | 2 | 3 | 基本面慢变量（裸水平撞规模代理）：Retained earnings | 主信号 |
| `pv37_bs_sh_cap_and_apic` | MATRIX | 0.9944 | 1 | 1 | 量价/量能：Share capital and additional paid-in capital | 主信号 |
| `pv37_bs_sh_out` | MATRIX | 0.9941 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Shares outstanding | 主信号 |
| `pv37_bs_st_borrow` | MATRIX | 0.993 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Short-term borrowings | 主信号 |
| `pv37_bs_st_debt` | MATRIX | 0.9942 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Short-term debt | 主信号 |
| `pv37_bs_st_portion_of_lt_debt` | MATRIX | 0.8596 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Short-term portion of long-term debt | 主信号 |
| `pv37_bs_tot_asset` | MATRIX | 0.9944 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Total assets | 主信号 |
| `pv37_bs_tot_eqy` | MATRIX | 0.4438 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Total equity | 主信号 |
| `pv37_bs_tot_liab_eqy` | MATRIX | 0.4438 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Total liabilities and equity | 主信号 |
| `pv37_bs_total_avail_line_of_credit` | MATRIX | 0.3717 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Total available line of credit | 主信号 |
| `pv37_bs_total_line_of_credit` | MATRIX | 0.7824 | 3 | 9 | 基本面慢变量（裸水平撞规模代理）：Total line of credit | 主信号 |
| `pv37_cap_10` | MATRIX | 1.0 | 1 | 1 | 量价/量能：10-Day Market Capitalization | 主信号 |
| `pv37_cap_110000` | MATRIX | 1.0 | 1 | 1 | 量价/量能：Capital at 11:00 | 主信号 |
| `pv37_cap_12` | MATRIX | 1.0 | 5 | 8 | 量价/量能：Market cap | 主信号 |
| `pv37_cap_130000` | MATRIX | 1.0 | 2 | 2 | 量价/量能：Capital at 13:00 | 主信号 |
| `pv37_cap_14` | MATRIX | 1.0 | 10 | 11 | 量价/量能：14-Day Market Capitalization | 主信号 |
| `pv37_cap_140000` | MATRIX | 1.0 | 0 | 0 | 量价/量能：Capital at 14:00 | 主信号 |
| `pv37_cap_1430` | MATRIX | 1.0 | 3 | 4 | 量价/量能：Capital at 14:30 | 主信号 |
| `pv37_cap_163000` | MATRIX | 1.0 | 3 | 5 | 量价/量能：Market capitalization at 16:30 | 主信号 |
| `pv37_capital_inv` | MATRIX | 0.6452 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：Capital Investment | 主信号 |
| `pv37_capital_inv_di` | MATRIX | 1.0 | 2 | 3 | 母字段直接指示器（同义标准化版）：Capital Investment Direct Indicator | 对照 |
| `pv37_cashflow_delay1_nugget` | MATRIX | 0.8428 | 1 | 1 | 量价/量能：Cash Flow Delay 1 Nugget | 主信号 |
| `pv37_cfps_best_crncy_iso` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best Currency ISO for CFPS | 主信号 |
| `pv37_cfps_best_cur_fiscal_qtr_period` | MATRIX | 0.8515 | 0 | 0 | 分析师一致预期（best 族）：Best current fiscal quarter period for CFPS | 主信号 |
| `pv37_cfps_best_cur_fiscal_semi_year_period` | MATRIX | 1.0 | 2 | 2 | 分析师一致预期（best 族）：Best current fiscal semi-year period for CFPS | 主信号 |
| `pv37_cfps_best_cur_fiscal_year_period` | MATRIX | 0.8515 | 2 | 2 | 分析师一致预期（best 族）：Best current fiscal year period for CFPS (Cash Flow Per Share) | 主信号 |
| `pv37_cfps_best_eeps_cur_yr` | MATRIX | 0.7756 | 4 | 5 | 分析师一致预期（best 族）：Best estimated EPS current year for CFPS (Cash Flow Per Share) | 主信号 |
| `pv37_cfps_best_eeps_nxt_yr` | MATRIX | 0.768 | 3 | 5 | 分析师一致预期（best 族）：Best estimated EPS next year for CFPS | 主信号 |
| `pv37_cfps_best_fiscal_period_dt` | VECTOR | 0.6555 | 3 | 3 | 分析师一致预期（best 族）：Best fiscal period date for CFPS | 主信号 |
| `pv37_cfps_best_fperiod_override` | VECTOR | 0.5786 | 3 | 4 | 分析师一致预期（best 族）：Best fiscal period override for CFPS (Cash Flow Per Share) | 主信号 |
| `pv37_cfps_expected_report_period` | VECTOR | 0.6555 | 1 | 0 | 时点/状态标识：Expected Report Period for CFPS | 排除 |
| `pv37_cfps_market_status` | VECTOR | 0.6555 | 2 | 2 | 时点/状态标识：Market status for CFPS | 排除 |
| `pv37_cfps_most_recent_period_end_dt` | VECTOR | 0.2781 | 0 | 0 | 时点/状态标识：Most recent period end date for CFPS | 排除 |
| `pv37_close_10` | MATRIX | 1.0 | 3 | 3 | 量价/量能：10-Day Closing Price | 主信号 |
| `pv37_close_110000` | MATRIX | 1.0 | 6 | 7 | 量价/量能：Close price at 11:00 | 主信号 |
| `pv37_close_12` | MATRIX | 1.0 | 9 | 9 | 量价/量能：Close price | 主信号 |
| `pv37_close_130000` | MATRIX | 1.0 | 4 | 4 | 量价/量能：Close price at 13:00 | 主信号 |
| `pv37_close_14` | MATRIX | 1.0 | 9 | 12 | 量价/量能：14-Day Closing Price | 主信号 |
| `pv37_close_140000` | MATRIX | 1.0 | 4 | 7 | 量价/量能：Close price at 14:00 | 主信号 |
| `pv37_close_1430` | MATRIX | 1.0 | 14 | 26 | 量价/量能：Close price at 14:30 | 主信号 |
| `pv37_close_163000` | MATRIX | 1.0 | 12 | 13 | 量价/量能：Closing price at 16:30 | 主信号 |
| `pv37_cn_analyst_revisn` | MATRIX | 0.6452 | 1 | 1 | 分析师预期/修正：CN Analyst Revision | 主信号 |
| `pv37_cn_analyst_revisn_di` | MATRIX | 1.0 | 2 | 6 | 分析师预期/修正：CN Analyst Revision Direct Indicator | 主信号 |
| `pv37_cn_analyst_uncertainty` | MATRIX | 0.6452 | 0 | 0 | 分析师预期/修正：CN Analyst Uncertainty | 主信号 |
| `pv37_cn_analyst_uncertainty_di` | MATRIX | 1.0 | 2 | 2 | 分析师预期/修正：CN Analyst Uncertainty Direct Indicator | 主信号 |
| `pv37_cn_capital_inv` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：CN Capital Investment | 主信号 |
| `pv37_cn_capital_inv_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Capital Investment Direct Indicator | 对照 |
| `pv37_cn_earn_qual` | MATRIX | 0.6452 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：CN Earnings Quality | 主信号 |
| `pv37_cn_earn_qual_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Earnings Quality Direct Indicator | 对照 |
| `pv37_cn_earn_valu` | MATRIX | 0.6452 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：CN Earnings Value | 主信号 |
| `pv37_cn_earn_valu_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Earnings Value Direct Indicator | 对照 |
| `pv37_cn_entrpris_valu` | MATRIX | 0.6452 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：CN Enterprise Value | 主信号 |
| `pv37_cn_entrpris_valu_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：CN Enterprise Value Direct Indicator | 对照 |
| `pv37_cn_ext_finance` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：CN External Finance | 主信号 |
| `pv37_cn_ext_finance_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN External Finance Direct Indicator | 对照 |
| `pv37_cn_fcf_valu` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：CN FCF Value | 主信号 |
| `pv37_cn_fcf_valu_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN FCF Value Direct Indicator | 对照 |
| `pv37_cn_fund_gth` | MATRIX | 0.6452 | 1 | 0 | 基本面慢变量（裸水平撞规模代理）：CN Fundamental Growth | 主信号 |
| `pv37_cn_fund_gth_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Fundamental Growth Direct Indicator | 对照 |
| `pv37_cn_fund_stab` | MATRIX | 0.6452 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：CN Fundamental Stability | 主信号 |
| `pv37_cn_fund_stab_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Fundamental Stability Direct Indicator | 对照 |
| `pv37_cn_leverage` | MATRIX | 0.6452 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：CN Leverage | 主信号 |
| `pv37_cn_leverage_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Leverage Direct Indicator | 对照 |
| `pv37_cn_profitabil_cons` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：CN Profitability Consensus | 主信号 |
| `pv37_cn_profitabil_cons_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：CN Profitability Consensus Direct Indicator | 对照 |
| `pv37_cn_profitability` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：CN Profitability | 主信号 |
| `pv37_cn_profitability_di` | MATRIX | 1.0 | 1 | 2 | 母字段直接指示器（同义标准化版）：CN Profitability Direct Indicator | 对照 |
| `pv37_cn_stk_pric_mom` | MATRIX | 0.6452 | 0 | 0 | 量价/量能：CN Stock Price Momentum | 主信号 |
| `pv37_cn_stk_pric_mom_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Stock Price Momentum Direct Indicator | 对照 |
| `pv37_cn_stk_pric_volatil` | MATRIX | 0.6452 | 1 | 1 | 量价/量能：CN Stock Price Volatility | 主信号 |
| `pv37_cn_stk_pric_volatil_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：CN Stock Price Volatility Direct Indicator | 对照 |
| `pv37_cni_tni_si` | MATRIX | 0.9379 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Consolidated net interest income special items | 主信号 |
| `pv37_company_name` | MATRIX | 0.6452 | 0 | 0 | 分类标识：Company Name | 分组轴 |
| `pv37_company_name_di` | MATRIX | 1.0 | 2 | 2 | 母字段直接指示器（同义标准化版）：Company Name Direct Indicator | 对照 |
| `pv37_contingent_liabilities` | MATRIX | 0.5575 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Contingent liabilities | 主信号 |
| `pv37_ctdv` | MATRIX | 0.5183 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dcdv` | MATRIX | 0.4264 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dcrv` | MATRIX | 0.8547 | 2 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dcsv` | MATRIX | 0.5836 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_ddrv` | MATRIX | 0.3592 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_debt_to_equity` | MATRIX | 0.6783 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Debt to Equity | 主信号 |
| `pv37_debt_to_equity_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Debt to Equity Direct Indicator | 对照 |
| `pv37_dividend_yield` | MATRIX | 0.6452 | 2 | 4 | 基本面慢变量（裸水平撞规模代理）：Dividend Yield | 主信号 |
| `pv37_dividend_yield_di` | MATRIX | 1.0 | 2 | 15 | 母字段直接指示器（同义标准化版）：Dividend Yield Direct Indicator | 对照 |
| `pv37_dividend_yield_f` | MATRIX | 0.6783 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Dividend Yield Forecast | 主信号 |
| `pv37_dividend_yield_f_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Dividend Yield Forecast Direct Indicator | 对照 |
| `pv37_dixv` | MATRIX | 0.6382 | 1 | 1 | 量价/量能：Total x-identification traded volume | 主信号 |
| `pv37_dly_rdlhrhs` | MATRIX | 0.6452 | 0 | 0 | 量价/量能：Direct indicator for the momentum of the company's stock price | 主信号 |
| `pv37_dly_rdlhrhs_nc` | MATRIX | 0.6452 | 0 | 0 | 量价/量能：Daily RDLHRHS NC | 主信号 |
| `pv37_dpav` | MATRIX | 0.9554 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dppv` | MATRIX | 0.9554 | 1 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dpxv` | MATRIX | 0.4941 | 1 | 6 | 量价/量能：Total x-partnership debt traded volume | 主信号 |
| `pv37_drai_decile` | MATRIX | 0.6452 | 0 | 0 | DRAI 评级因子：DRAI Decile | 主信号 |
| `pv37_drai_decile_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：DRAI Decile Direct Indicator | 对照 |
| `pv37_drai_decile_within_country` | MATRIX | 0.6452 | 0 | 0 | DRAI 评级因子：DRAI Decile Within Country | 主信号 |
| `pv37_drai_decile_within_country_di` | MATRIX | 1.0 | 1 | 0 | 母字段直接指示器（同义标准化版）：DRAI Decile Within Country Direct Indicator | 对照 |
| `pv37_drai_decile_within_sector` | MATRIX | 0.6452 | 0 | 0 | DRAI 评级因子：DRAI Decile Within Sector | 主信号 |
| `pv37_drai_decile_within_sector_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：DRAI Decile Within Sector Direct Indicator | 对照 |
| `pv37_drai_score` | MATRIX | 0.6452 | 0 | 0 | DRAI 评级因子：DRAI Score | 主信号 |
| `pv37_drai_score_chg_13w` | MATRIX | 0.6783 | 1 | 1 | DRAI 评级因子：DRAI Score Change 13W | 主信号 |
| `pv37_drai_score_chg_13w_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：DRAI Score Change 13W Direct Indicator | 对照 |
| `pv37_drai_score_chg_1w` | MATRIX | 0.6783 | 1 | 1 | DRAI 评级因子：DRAI Score Change 1W | 主信号 |
| `pv37_drai_score_chg_1w_di` | MATRIX | 1.0 | 3 | 3 | 母字段直接指示器（同义标准化版）：DRAI Score Change 1W Direct Indicator | 对照 |
| `pv37_drai_score_di` | MATRIX | 1.0 | 1 | 0 | 母字段直接指示器（同义标准化版）：DRAI Score Direct Indicator | 对照 |
| `pv37_drdv` | MATRIX | 0.8799 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dtcv` | MATRIX | 0.3429 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dtdv` | MATRIX | 0.4403 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_dtrv` | MATRIX | 0.3531 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_earn_for_common` | MATRIX | 0.9642 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Earnings for common | 主信号 |
| `pv37_earn_qual` | MATRIX | 0.6452 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Earnings Quality | 主信号 |
| `pv37_earn_qual_di` | MATRIX | 1.0 | 3 | 10 | 母字段直接指示器（同义标准化版）：Earnings Quality Direct Indicator | 对照 |
| `pv37_earn_valu` | MATRIX | 0.6452 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Earnings Value | 主信号 |
| `pv37_earn_valu_di` | MATRIX | 1.0 | 1 | 0 | 母字段直接指示器（同义标准化版）：Earnings Value Direct Indicator | 对照 |
| `pv37_ebit` | MATRIX | 0.9118 | 6 | 6 | 基本面慢变量（裸水平撞规模代理）：EBIT | 主信号 |
| `pv37_ebitda` | MATRIX | 0.9349 | 4 | 5 | 基本面慢变量（裸水平撞规模代理）：EBITDA | 主信号 |
| `pv37_ebitda_best_crncy_iso` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best currency ISO for EBITDA | 主信号 |
| `pv37_ebitda_best_cur_fiscal_qtr_period` | MATRIX | 0.8515 | 0 | 0 | 分析师一致预期（best 族）：Best current fiscal quarter period for EBITDA | 主信号 |
| `pv37_ebitda_best_cur_fiscal_semi_year_period` | MATRIX | 1.0 | 1 | 1 | 分析师一致预期（best 族）：Best current fiscal semi-year period for EBITDA | 主信号 |
| `pv37_ebitda_best_cur_fiscal_year_period` | MATRIX | 0.8515 | 1 | 2 | 分析师一致预期（best 族）：Best current fiscal year period for EBITDA | 主信号 |
| `pv37_ebitda_best_eeps_cur_yr` | MATRIX | 0.7756 | 5 | 5 | 分析师一致预期（best 族）：Best estimated EBITDA current year | 主信号 |
| `pv37_ebitda_best_eeps_nxt_yr` | MATRIX | 0.768 | 3 | 3 | 分析师一致预期（best 族）：Best estimated EBITDA next year | 主信号 |
| `pv37_ebitda_best_fiscal_period_dt` | VECTOR | 0.7311 | 2 | 2 | 分析师一致预期（best 族）：Best fiscal period date for EBITDA | 主信号 |
| `pv37_ebitda_best_fperiod_override` | VECTOR | 0.6511 | 1 | 9 | 分析师一致预期（best 族）：Best fiscal period override for EBITDA | 主信号 |
| `pv37_ebitda_expected_report_period` | VECTOR | 0.7311 | 3 | 3 | 时点/状态标识：Expected report period for EBITDA | 排除 |
| `pv37_ebitda_latest_ann_dt_qtrly` | VECTOR | 0.3241 | 1 | 1 | 时点/状态标识：Latest annual date quarterly for EBITDA | 排除 |
| `pv37_ebitda_market_status` | VECTOR | 0.7311 | 1 | 2 | 时点/状态标识：Market status for EBITDA | 排除 |
| `pv37_ebitda_most_recent_period_end_dt` | VECTOR | 0.3714 | 1 | 1 | 时点/状态标识：Most recent period end date for EBITDA | 排除 |
| `pv37_ebitdar` | MATRIX | 0.2518 | 5 | 18 | 基本面慢变量（裸水平撞规模代理）：EBITDAR | 主信号 |
| `pv37_eff_int_rate` | MATRIX | 0.7931 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Effective interest rate | 主信号 |
| `pv37_eiuv` | MATRIX | 0.3492 | 4 | 4 | 量价/量能：Total Unincorporated Enterprise Income Volume | 主信号 |
| `pv37_entrpris_valu` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Enterprise Value | 主信号 |
| `pv37_entrpris_valu_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：Enterprise Value Direct Indicator | 对照 |
| `pv37_eprv` | MATRIX | 0.3499 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_eps_growth_forecast_5year` | MATRIX | 0.6783 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：The expected percentage growth in earnings per share over the coming 5 years | 主信号 |
| `pv37_eps_growth_forecast_5year_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct Indicator for the Forecasted Growth in Earnings per Share Over the Next 5 Years | 对照 |
| `pv37_epts` | MATRIX | 0.495 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_eptv` | MATRIX | 0.6099 | 1 | 2 | 量价/量能：Total private equity traded volume | 主信号 |
| `pv37_exchange_country` | MATRIX | 0.6452 | 0 | 0 | 分类标识：The country where the company's primary stock exchange is located | 分组轴 |
| `pv37_exchange_country_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the country in which the stock exchange is located | 对照 |
| `pv37_ext_finance` | MATRIX | 0.6452 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Funds raised through external sources, such as debt or equity financing | 主信号 |
| `pv37_ext_finance_di` | MATRIX | 1.0 | 2 | 2 | 母字段直接指示器（同义标准化版）：Direct indicator for external financing activities | 对照 |
| `pv37_fcf_valu` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：The valuation of a company based on its free cash flows | 主信号 |
| `pv37_fcf_valu_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the valuation based on free cash flow | 对照 |
| `pv37_ffops_best_crncy_iso` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best currency ISO for FFOPS | 主信号 |
| `pv37_ffops_best_cur_fiscal_qtr_period` | MATRIX | 0.8516 | 0 | 0 | 分析师一致预期（best 族）：Best current fiscal quarter period for FFOPS | 主信号 |
| `pv37_ffops_best_cur_fiscal_semi_year_period` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best current fiscal semi-year period for FFOPS | 主信号 |
| `pv37_ffops_best_cur_fiscal_year_period` | MATRIX | 0.8516 | 1 | 1 | 分析师一致预期（best 族）：Best current fiscal year period for FFOPS | 主信号 |
| `pv37_ffops_best_eeps_cur_yr` | MATRIX | 0.7756 | 4 | 6 | 分析师一致预期（best 族）：Best estimated EPS current year for FFOPS | 主信号 |
| `pv37_ffops_best_eeps_nxt_yr` | MATRIX | 0.768 | 3 | 3 | 分析师一致预期（best 族）：Best estimated EPS next year for FFOPS | 主信号 |
| `pv37_fotv` | MATRIX | 0.3502 | 0 | 0 | 量价/量能：Total other finance traded volume | 主信号 |
| `pv37_ftov` | MATRIX | 0.3481 | 2 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_fttv` | MATRIX | 0.3635 | 0 | 0 | 量价/量能：Total trust fund traded volume | 主信号 |
| `pv37_fund_gth` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：The intrinsic growth of the company based on fundamental analysis | 主信号 |
| `pv37_fund_gth_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：Direct indicator for fundamental growth metrics | 对照 |
| `pv37_fund_stab` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：The consistency and reliability of a company's fundamental financial metrics | 主信号 |
| `pv37_fund_stab_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the stability of the company's fundamentals | 对照 |
| `pv37_fx_conversion` | MATRIX | 0.996 | 0 | 0 | 汇率/汇兑因子：Foreign Exchange Conversion | 主信号 |
| `pv37_fx_conversion_return` | MATRIX | 0.996 | 0 | 0 | 汇率/汇兑因子：Foreign Exchange Conversion Return | 主信号 |
| `pv37_gaxv` | MATRIX | 0.4056 | 1 | 1 | 量价/量能：Total x-agreement traded volume | 主信号 |
| `pv37_gdbs` | MATRIX | 0.3505 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_geographic_region` | MATRIX | 0.6452 | 0 | 0 | 分类标识：The main geographic area where the company operates | 分组轴 |
| `pv37_geographic_region_di` | MATRIX | 1.0 | 1 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the geographic region of operation | 对照 |
| `pv37_ghbs` | MATRIX | 0.3501 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_ghtm` | MATRIX | 0.346 | 2 | 2 | 量价/量能：Market Trend High Gain for All Instruments | 主信号 |
| `pv37_gics_industry_group_name` | MATRIX | 0.6452 | 0 | 0 | 分类标识：The name of the industry group assigned to the company according to the Global Industry Classification Standard | 分组轴 |
| `pv37_gics_industry_group_name_di` | MATRIX | 1.0 | 1 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the name of the industry group according to GICS | 对照 |
| `pv37_gics_industry_group_number` | MATRIX | 0.6783 | 4 | 4 | 分类标识：The number assigned to the industry group of the company according to the Global Industry Classification Standard | 分组轴 |
| `pv37_gics_industry_group_number_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：Direct indicator for the industry group number according to GICS | 对照 |
| `pv37_gics_industry_name` | MATRIX | 0.6452 | 2 | 2 | 分类标识：The name of the industry assigned to the company according to the Global Industry Classification Standard | 分组轴 |
| `pv37_gics_industry_name_di` | MATRIX | 1.0 | 2 | 2 | 母字段直接指示器（同义标准化版）：Direct indicator for the industry name according to GICS | 对照 |
| `pv37_gics_industry_number` | MATRIX | 0.6452 | 1 | 1 | 分类标识：The number assigned to the industry of the company according to the Global Industry Classification Standard | 分组轴 |
| `pv37_gics_industry_number_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the industry number according to GICS | 对照 |
| `pv37_gics_industry_number_i` | MATRIX | 0.6783 | 1 | 1 | 分类标识：The number assigned to the industry of the company according to the Global Industry Classification Standard | 分组轴 |
| `pv37_gics_industry_number_i_di` | MATRIX | 1.0 | 1 | 2 | 母字段直接指示器（同义标准化版）：An alternative industry number assigned to the company according to the Global Industry Classification Standard | 对照 |
| `pv37_gics_sector_name` | MATRIX | 0.6452 | 1 | 1 | 分类标识：The name of the sector assigned to the company according to the Global Industry Classification Standard | 分组轴 |
| `pv37_gics_sector_name_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：Direct indicator for the sector name according to GICS | 对照 |
| `pv37_gics_sector_number` | MATRIX | 0.6783 | 0 | 0 | 分类标识：The number assigned to the sector of the company according to the Global Industry Classification Standard | 分组轴 |
| `pv37_gics_sector_number_di` | MATRIX | 1.0 | 1 | 13 | 母字段直接指示器（同义标准化版）：Direct indicator for the sector number according to GICS | 对照 |
| `pv37_gzps` | MATRIX | 0.3503 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_high_10` | MATRIX | 1.0 | 11 | 24 | 量价/量能：10-Day Highest Price | 主信号 |
| `pv37_high_110000` | MATRIX | 1.0 | 5 | 5 | 量价/量能：High Price at 11:00 | 主信号 |
| `pv37_high_12` | MATRIX | 1.0 | 7 | 15 | 量价/量能：High price | 主信号 |
| `pv37_high_130000` | MATRIX | 1.0 | 2 | 2 | 量价/量能：High price at 13:00 | 主信号 |
| `pv37_high_14` | MATRIX | 1.0 | 3 | 3 | 量价/量能：14-Day Highest Price | 主信号 |
| `pv37_high_140000` | MATRIX | 1.0 | 5 | 10 | 量价/量能：High price at 14:00 | 主信号 |
| `pv37_high_1430` | MATRIX | 1.0 | 6 | 7 | 量价/量能：High price at 14:30 | 主信号 |
| `pv37_high_163000` | MATRIX | 1.0 | 2 | 2 | 量价/量能：Highest price at 16:30 | 主信号 |
| `pv37_id_dly_rdlhrhs` | MATRIX | 1.0 | 0 | 0 | 量价/量能：Daily record of high, low, return, hold, sell, and buy signals | 主信号 |
| `pv37_id_dly_rdlhrhs_nc` | MATRIX | 1.0 | 1 | 1 | 量价/量能：ID Daily RDLHRHS NC | 主信号 |
| `pv37_indv` | MATRIX | 0.7562 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_1spdd` | MATRIX | 0.7531 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted dividends gross cost development | 主信号 |
| `pv37_intfv_all_2spdd` | MATRIX | 0.3547 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted dividends per share 1 | 主信号 |
| `pv37_intfv_all_aaga` | MATRIX | 0.493 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted annual growth average | 主信号 |
| `pv37_intfv_all_aamt` | MATRIX | 0.4788 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted annual maintenance total | 主信号 |
| `pv37_intfv_all_abpl` | MATRIX | 0.2864 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted payable bonds assets data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_acda` | MATRIX | 0.2613 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted cumulative debt annual | 主信号 |
| `pv37_intfv_all_acoa` | MATRIX | 0.6601 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted other asset totals | 主信号 |
| `pv37_intfv_all_acta` | MATRIX | 0.7181 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted total asset accounts | 主信号 |
| `pv37_intfv_all_adep` | MATRIX | 0.7209 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted depreciation expense | 主信号 |
| `pv37_intfv_all_adpa` | MATRIX | 0.6924 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted property building operations | 主信号 |
| `pv37_intfv_all_aemc` | MATRIX | 0.4056 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted cost insurance assets | 主信号 |
| `pv37_intfv_all_afsi` | MATRIX | 0.7365 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment savings direct position, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_agse` | MATRIX | 0.745 | 1 | 4 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings savings gross assets | 主信号 |
| `pv37_intfv_all_aing` | MATRIX | 0.4882 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted net income gains | 主信号 |
| `pv37_intfv_all_aint` | MATRIX | 0.7485 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted net interest | 主信号 |
| `pv37_intfv_all_airm` | MATRIX | 0.6008 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted interest rate margins | 主信号 |
| `pv37_intfv_all_aitl` | MATRIX | 0.7125 | 2 | 8 | 基本面慢变量（裸水平撞规模代理）：Adjusted total interest liabilities | 主信号 |
| `pv37_intfv_all_alge` | MATRIX | 0.3904 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings financial product revenue | 主信号 |
| `pv37_intfv_all_alti` | MATRIX | 0.7389 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted total liabilities | 主信号 |
| `pv37_intfv_all_altr` | MATRIX | 0.6551 | 1 | 4 | 基本面慢变量（裸水平撞规模代理）：Adjusted long-term reserves | 主信号 |
| `pv37_intfv_all_amec` | MATRIX | 0.7084 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities total reserves | 主信号 |
| `pv37_intfv_all_aorc` | MATRIX | 0.7308 | 1 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted other property costs | 主信号 |
| `pv37_intfv_all_aptc` | MATRIX | 0.7281 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted property real estate | 主信号 |
| `pv37_intfv_all_arca` | MATRIX | 0.461 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted property total costs | 主信号 |
| `pv37_intfv_all_arcl` | MATRIX | 0.2563 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted reserve capital assets | 主信号 |
| `pv37_intfv_all_asti` | MATRIX | 0.7097 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted savings home mortgages | 主信号 |
| `pv37_intfv_all_astr` | MATRIX | 0.5153 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted savings total investments | 主信号 |
| `pv37_intfv_all_atda` | MATRIX | 0.6393 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted total assets annual | 主信号 |
| `pv37_intfv_all_atot` | MATRIX | 0.7554 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted total gross liabilities | 主信号 |
| `pv37_intfv_all_bloo` | MATRIX | 0.7491 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Operating open cash flow | 主信号 |
| `pv37_intfv_all_bpao` | MATRIX | 0.7157 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating asset management income | 主信号 |
| `pv37_intfv_all_bpdl` | MATRIX | 0.4356 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities direct operations liabilities, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_caic` | MATRIX | 0.7554 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Adjusted cost gross product development | 主信号 |
| `pv37_intfv_all_cbpa` | MATRIX | 0.6844 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted other total investments | 主信号 |
| `pv37_intfv_all_cfda` | MATRIX | 0.3659 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted cost financing deferred annual | 主信号 |
| `pv37_intfv_all_cila` | MATRIX | 0.6734 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities insurance contracts | 主信号 |
| `pv37_intfv_all_cmin` | MATRIX | 0.5899 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted cost mechanical equipment assets | 主信号 |
| `pv37_intfv_all_cnin` | MATRIX | 0.7557 | 5 | 6 | 基本面慢变量（裸水平撞规模代理）：Net income non-current | 主信号 |
| `pv37_intfv_all_cpca` | MATRIX | 0.6438 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted claims policy cumulative annual | 主信号 |
| `pv37_intfv_all_cpdf` | MATRIX | 0.4529 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial deposit product costs | 主信号 |
| `pv37_intfv_all_cpoa` | MATRIX | 0.6575 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted other earnings assets | 主信号 |
| `pv37_intfv_all_crrf` | MATRIX | 0.508 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial position from savings surplus, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_crta` | MATRIX | 0.7374 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted total other transactions | 主信号 |
| `pv37_intfv_all_deds` | MATRIX | 0.7505 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_dgcd` | MATRIX | 0.7505 | 1 | 1 | 时点/状态标识：Tracking date of adjusted cost gross product development | 排除 |
| `pv37_intfv_all_dlcl` | MATRIX | 0.6584 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities bond direct total, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_drpc` | MATRIX | 0.3921 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted cost property insurance assets | 主信号 |
| `pv37_intfv_all_drpf` | MATRIX | 0.7275 | 3 | 4 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial liabilities from direct reinvestment, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_dtll` | MATRIX | 0.6697 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted Long-Term Liabilities Data, Calculated on an Interim Basis | 主信号 |
| `pv37_intfv_all_dtsl` | MATRIX | 0.7451 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted savings total deposit data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_dttl` | MATRIX | 0.7542 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted long-term total deposit data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_eaca` | MATRIX | 0.7447 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings cumulative annual | 主信号 |
| `pv37_intfv_all_eami` | MATRIX | 0.6763 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings asset management | 主信号 |
| `pv37_intfv_all_ecor` | MATRIX | 0.7245 | 3 | 5 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings capital | 主信号 |
| `pv37_intfv_all_einn` | MATRIX | 0.3449 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings interest income net | 主信号 |
| `pv37_intfv_all_eiue` | MATRIX | 0.4741 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings underwriting insurance expenses | 主信号 |
| `pv37_intfv_all_elar` | MATRIX | 0.7153 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings liabilities asset ratio | 主信号 |
| `pv37_intfv_all_elit` | MATRIX | 0.3535 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings liabilities interest total | 主信号 |
| `pv37_intfv_all_eltq` | MATRIX | 0.7554 | 1 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_eont` | MATRIX | 0.5023 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings other net transactions | 主信号 |
| `pv37_intfv_all_eooe` | MATRIX | 0.5462 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings other operating expenses | 主信号 |
| `pv37_intfv_all_erad` | MATRIX | 0.6228 | 24 | 25 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings reserve asset development | 主信号 |
| `pv37_intfv_all_etoe` | MATRIX | 0.7372 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings total other expenses | 主信号 |
| `pv37_intfv_all_fcff` | MATRIX | 0.6892 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial free cash flow | 主信号 |
| `pv37_intfv_all_fcii` | MATRIX | 0.7403 | 3 | 4 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment income annual net, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_fltf` | MATRIX | 0.7471 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial total direct investments, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_fsic` | MATRIX | 0.5924 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial savings from net direct savings, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_gfia` | MATRIX | 0.6403 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment funding gains | 主信号 |
| `pv37_intfv_all_graa` | MATRIX | 0.684 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted growth revenue annual average | 主信号 |
| `pv37_intfv_all_gwga` | MATRIX | 0.3348 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted gross working gains | 主信号 |
| `pv37_intfv_all_hsca` | MATRIX | 0.4445 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted holdings cash annual | 主信号 |
| `pv37_intfv_all_ibaq` | MATRIX | 0.3305 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial working capital value, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_icex` | MATRIX | 0.7533 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted hedge fund financial operations, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_idlf` | MATRIX | 0.5964 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings from underwriting insurance expenses, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_idsf` | MATRIX | 0.5847 | 6 | 16 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial reserve position, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_ilti` | MATRIX | 0.7538 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment savings total liabilities, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_inds` | MATRIX | 0.7471 | 7 | 9 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_iqea` | MATRIX | 0.6234 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment equity annual | 主信号 |
| `pv37_intfv_all_iscs` | MATRIX | 0.7353 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_isob` | MATRIX | 0.303 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment savings key investment, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_isoi` | MATRIX | 0.5517 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment savings key reserve, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_iwga` | MATRIX | 0.4554 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted gross working investments | 主信号 |
| `pv37_intfv_all_lapb` | MATRIX | 0.72 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities account capital, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_lbpl` | MATRIX | 0.7002 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted Payable Bonds Liabilities Data, Calculated on an Interim Basis | 主信号 |
| `pv37_intfv_all_lcol` | MATRIX | 0.7171 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted other current liabilities data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_lctl` | MATRIX | 0.7181 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted long-term capital liabilities data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_ldbm` | MATRIX | 0.3505 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted Market Bond Deposit Liabilities Data, Calculated on an Interim Basis | 主信号 |
| `pv37_intfv_all_lgue` | MATRIX | 0.3352 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings underwriting gross liabilities | 主信号 |
| `pv37_intfv_all_lltl` | MATRIX | 0.7554 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted long-term liabilities total data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_lmin` | MATRIX | 0.5492 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted mining investments data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_lopb` | MATRIX | 0.7096 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted other payable bonds data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_ltio` | MATRIX | 0.6984 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating income value | 主信号 |
| `pv37_intfv_all_ltll` | MATRIX | 0.6652 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted long-term liabilities to assets ratio, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_metl` | MATRIX | 0.6875 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted market hedge assets data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_mibf` | MATRIX | 0.3519 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted market investment bond liabilities data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_mibh` | MATRIX | 0.3518 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted market investment bond product data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_mibl` | MATRIX | 0.3455 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted market investment bond reserve data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_mibz` | MATRIX | 0.3508 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted market investment gains key data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_mnit` | MATRIX | 0.3502 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Minimum interest trend for all instruments | 主信号 |
| `pv37_intfv_all_mobe` | MATRIX | 0.3502 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Mobile engagement for all instruments | 主信号 |
| `pv37_intfv_all_mobk` | MATRIX | 0.3507 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Mobile kick for all instruments | 主信号 |
| `pv37_intfv_all_mogg` | MATRIX | 0.3442 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Maximum Open Gain for All Instruments | 主信号 |
| `pv37_intfv_all_ndlf` | MATRIX | 0.6701 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial cost for holding deposit positions, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_ndsf` | MATRIX | 0.6273 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial savings capital position, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_niie` | MATRIX | 0.3377 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings interest external | 主信号 |
| `pv37_intfv_all_nppa` | MATRIX | 0.7538 | 3 | 14 | 基本面慢变量（裸水平撞规模代理）：Adjusted property lease contracts | 主信号 |
| `pv37_intfv_all_nscf` | MATRIX | 0.6678 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial cost savings net | 主信号 |
| `pv37_intfv_all_nvii` | MATRIX | 0.4565 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment income savings direct, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_oami` | MATRIX | 0.716 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Operating asset management activity | 主信号 |
| `pv37_intfv_all_octq` | MATRIX | 0.7542 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_oinm` | MATRIX | 0.3512 | 1 | 0 | 基本面慢变量（裸水平撞规模代理）：Minimum open interest for all instruments | 主信号 |
| `pv37_intfv_all_olcl` | MATRIX | 0.3148 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities capital asset value, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_olto` | MATRIX | 0.7478 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating sale operating liabilities | 主信号 |
| `pv37_intfv_all_onet` | MATRIX | 0.7445 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Operating net cash income | 主信号 |
| `pv37_intfv_all_pdcf` | MATRIX | 0.587 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial cost deposit position | 主信号 |
| `pv37_intfv_all_pdsl` | MATRIX | 0.4203 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted savings deposit placement data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_pede` | MATRIX | 0.7113 | 1 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings core | 主信号 |
| `pv37_intfv_all_peds` | MATRIX | 0.7505 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_pnii` | MATRIX | 0.7494 | 2 | 3 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment income job level, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_pwia` | MATRIX | 0.525 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Adjusted interest with protection | 主信号 |
| `pv37_intfv_all_pxtl` | MATRIX | 0.7072 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted long-term tax payable data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_qaii` | MATRIX | 0.7328 | 2 | 3 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment financial reserve earnings, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_rcaa` | MATRIX | 0.7321 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted cost annual average | 主信号 |
| `pv37_intfv_all_rcao` | MATRIX | 0.7287 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating asset cash gain | 主信号 |
| `pv37_intfv_all_rdlf` | MATRIX | 0.6403 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial liabilities from direct investments, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_rdsf` | MATRIX | 0.592 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial savings from direct investments, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_rltr` | MATRIX | 0.7468 | 11 | 13 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_saie` | MATRIX | 0.4941 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings gross liabilities assets | 主信号 |
| `pv37_intfv_all_saoa` | MATRIX | 0.712 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted net total liabilities | 主信号 |
| `pv37_intfv_all_saoo` | MATRIX | 0.6431 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating open asset liabilities | 主信号 |
| `pv37_intfv_all_scor` | MATRIX | 0.725 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_snii` | MATRIX | 0.7442 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment income job reserve, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_socf` | MATRIX | 0.7544 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_sonm` | MATRIX | 0.526 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Minimum open spread for all instruments | 主信号 |
| `pv37_intfv_all_sspf` | MATRIX | 0.6853 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted financial product development costs, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_tbie` | MATRIX | 0.7568 | 29 | 41 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings insurance underwriting | 主信号 |
| `pv37_intfv_all_tdbl` | MATRIX | 0.5831 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities account external, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_tdbo` | MATRIX | 0.3743 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating asset pledge bid | 主信号 |
| `pv37_intfv_all_toia` | MATRIX | 0.6837 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted total other income | 主信号 |
| `pv37_intfv_all_txee` | MATRIX | 0.3724 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings direct operating expenses | 主信号 |
| `pv37_intfv_all_uaie` | MATRIX | 0.5373 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings insurance asset savings | 主信号 |
| `pv37_intfv_all_vacl` | MATRIX | 0.7099 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted liabilities account position bond, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_vama` | MATRIX | 0.3794 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_vami` | MATRIX | 0.7413 | 2 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_intfv_all_vdae` | MATRIX | 0.6842 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Adjusted dividends per share special 4 | 主信号 |
| `pv37_intfv_all_vnie` | MATRIX | 0.4197 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings net non-operating | 主信号 |
| `pv37_intfv_all_vsrl` | MATRIX | 0.3951 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted reserve savings value data, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_xeal` | MATRIX | 0.7338 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Adjusted investment work key reserve, calculated on an interim basis | 主信号 |
| `pv37_intfv_all_xecs` | MATRIX | 0.7534 | 1 | 1 | 分类标识：Assessment of Sale of Cash Exchange | 分组轴 |
| `pv37_intfv_all_xeie` | MATRIX | 0.3548 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Adjusted earnings interest before taxes | 主信号 |
| `pv37_intfv_all_yppa` | MATRIX | 0.7264 | 2 | 4 | 基本面慢变量（裸水平撞规模代理）：Adjusted property net position | 主信号 |
| `pv37_intfv_mfm_atot` | MATRIX | 0.7481 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：A metric representing the total assets | 主信号 |
| `pv37_intfv_mfm_dttl` | MATRIX | 0.7469 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：A metric representing the total long-term debt | 主信号 |
| `pv37_intfv_mfm_eltq` | MATRIX | 0.7481 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：A metric that could represent equity or earnings at the end of a quarter | 主信号 |
| `pv37_intfv_mfm_inds` | MATRIX | 0.7471 | 4 | 9 | 基本面慢变量（裸水平撞规模代理）：A metric representing industry standards or an index value | 主信号 |
| `pv37_intfv_mfm_lctl` | MATRIX | 0.711 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：A metric representing long-term liabilities | 主信号 |
| `pv37_intfv_mfm_olto` | MATRIX | 0.7478 | 5 | 6 | 基本面慢变量（裸水平撞规模代理）：A metric representing other long-term obligations | 主信号 |
| `pv37_intfv_mfm_rltr` | MATRIX | 0.7396 | 102 | 264 | 基本面慢变量（裸水平撞规模代理）：A metric that could represent return or a specific ratio over the long term | 主信号 |
| `pv37_invtry_finished_goods` | MATRIX | 0.9064 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Inventory of finished goods | 主信号 |
| `pv37_invtry_in_progress` | MATRIX | 0.9054 | 5 | 7 | 基本面慢变量（裸水平撞规模代理）：Inventory in progress | 主信号 |
| `pv37_invtry_raw_materials` | MATRIX | 0.9064 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：Inventory of raw materials | 主信号 |
| `pv37_ipts` | MATRIX | 0.5589 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_is_a3_announcement_dt` | MATRIX | 0.9669 | 3 | 4 | 时点/状态标识：The announcement date for a specific financial event or metric | 排除 |
| `pv37_is_a3_fundamental_entry_dt` | MATRIX | 0.9685 | 0 | 0 | 时点/状态标识：The entry date for fundamental financial data | 排除 |
| `pv37_is_a3_latest_period_end_dt_full_record` | MATRIX | 0.9685 | 0 | 0 | 时点/状态标识：The full record date for the end of the latest financial period | 排除 |
| `pv37_is_a_announcement_dt` | MATRIX | 0.9669 | 1 | 6 | 时点/状态标识：Announcement date | 排除 |
| `pv37_is_a_fundamental_entry_dt` | MATRIX | 0.9685 | 5 | 6 | 时点/状态标识：Fundamental entry date | 排除 |
| `pv37_is_a_latest_period_end_dt_full_record` | MATRIX | 0.9685 | 1 | 2 | 时点/状态标识：Latest period end date for full record | 排除 |
| `pv37_is_abnormal_item` | MATRIX | 0.9249 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Abnormal item | 主信号 |
| `pv37_is_avg_num_sh_for_eps` | MATRIX | 0.9631 | 5 | 5 | 基本面慢变量（裸水平撞规模代理）：Average Number of Shares for EPS Calculation | 主信号 |
| `pv37_is_basic_eps_cont_ops` | MATRIX | 0.9305 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Basic earnings per share from continuing operations | 主信号 |
| `pv37_is_cogs_to_fe_and_pp_and_g` | MATRIX | 0.8521 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Cost of goods sold to fuel, electricity, and power and gas | 主信号 |
| `pv37_is_comprehensive_income` | MATRIX | 0.9289 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Comprehensive income | 主信号 |
| `pv37_is_dil_eps_cont_ops` | MATRIX | 0.8195 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Diluted earnings per share from continuing operations | 主信号 |
| `pv37_is_diluted_eps` | MATRIX | 0.8847 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Diluted earnings per share | 主信号 |
| `pv37_is_div_per_shr` | MATRIX | 0.96 | 5 | 7 | 基本面慢变量（裸水平撞规模代理）：Dividends per share | 主信号 |
| `pv37_is_earn_bef_xo_items_per_sh` | MATRIX | 0.9629 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Earnings before extraordinary items per share | 主信号 |
| `pv37_is_eqy_earn_from_invest_assoc` | MATRIX | 0.9456 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Equity earnings from investments in associates | 主信号 |
| `pv37_is_export_sales` | MATRIX | 0.5594 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Export sales | 主信号 |
| `pv37_is_foreign_crncy_trans_adj` | MATRIX | 0.6835 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Foreign currency translation adjustments | 主信号 |
| `pv37_is_foreign_exch_loss` | MATRIX | 0.8883 | 0 | 0 | 汇率/汇兑因子：Foreign exchange loss | 主信号 |
| `pv37_is_gnrl_and_admin_exp` | MATRIX | 0.381 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：General and administrative expenses | 主信号 |
| `pv37_is_inc_bef_xo_item` | MATRIX | 0.964 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Income before extraordinary items | 主信号 |
| `pv37_is_inc_tax_exp` | MATRIX | 0.9639 | 1 | 3 | 基本面慢变量（裸水平撞规模代理）：Income tax expense | 主信号 |
| `pv37_is_int_expense` | MATRIX | 0.9062 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Interest expense | 主信号 |
| `pv37_is_invest_income` | MATRIX | 0.9578 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Investment income | 主信号 |
| `pv37_is_net_inc_avail_com_shrhldrs` | MATRIX | 0.514 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Net income available to common shareholders | 主信号 |
| `pv37_is_net_non_oper_loss` | MATRIX | 0.9637 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Net non-operating loss | 主信号 |
| `pv37_is_oper_inc` | MATRIX | 0.9652 | 4 | 4 | 基本面慢变量（裸水平撞规模代理）：Operating income | 主信号 |
| `pv37_is_other_oper_inc` | MATRIX | 0.3405 | 2 | 5 | 基本面慢变量（裸水平撞规模代理）：Other operating income | 主信号 |
| `pv37_is_other_rev` | MATRIX | 0.4403 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Other revenue | 主信号 |
| `pv37_is_personnel_exp` | MATRIX | 0.9281 | 2 | 3 | 基本面慢变量（裸水平撞规模代理）：Personnel expenses | 主信号 |
| `pv37_is_rd_expend` | MATRIX | 0.6549 | 32 | 64 | 基本面慢变量（裸水平撞规模代理）：Research and development expenditures | 主信号 |
| `pv37_is_sh_for_diluted_eps` | MATRIX | 0.8386 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Shares for diluted EPS calculation | 主信号 |
| `pv37_is_stock_option_expense_bef_tax` | MATRIX | 0.4377 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Stock option expense before tax | 主信号 |
| `pv37_is_tax_eff_on_abnormal_item` | MATRIX | 0.9219 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Tax effect on abnormal items | 主信号 |
| `pv37_is_tax_eff_on_xo_item` | MATRIX | 0.9614 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Tax effect on extraordinary items | 主信号 |
| `pv37_is_tot_cash_com_dvd` | MATRIX | 0.961 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Total cash dividends for common stock | 主信号 |
| `pv37_is_tot_cash_pfd_dvd` | MATRIX | 0.9608 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Total cash dividends for preferred stock | 主信号 |
| `pv37_is_trading_acct_prof` | MATRIX | 0.8659 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Trading account profit | 主信号 |
| `pv37_is_unrealized_gain_loss_comp_inc` | MATRIX | 0.669 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Unrealized gain or loss on comprehensive income | 主信号 |
| `pv37_is_xo_loss_bef_tax_eff` | MATRIX | 0.9619 | 3 | 3 | 基本面慢变量（裸水平撞规模代理）：Extraordinary loss before tax effect | 主信号 |
| `pv37_iwgv` | MATRIX | 0.3844 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_kgps` | MATRIX | 0.3502 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_koreahalftradingtax_nugget` | MATRIX | 0.996 | 1 | 0 | 时点/状态标识：Korea half trading tax nugget | 排除 |
| `pv37_ksps` | MATRIX | 0.3502 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_laxv` | MATRIX | 0.3427 | 3 | 4 | 量价/量能：Total x-allocation traded volume | 主信号 |
| `pv37_lctv` | MATRIX | 0.2847 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_leverage` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：The use of debt to acquire additional assets | 主信号 |
| `pv37_leverage_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：Direct indicator for the company's financial leverage | 对照 |
| `pv37_lgun` | MATRIX | 0.4114 | 1 | 2 | 量价/量能：Net under gain gain | 主信号 |
| `pv37_lguq` | MATRIX | 0.6385 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_low_10` | MATRIX | 1.0 | 6 | 8 | 量价/量能：10-Day Lowest Price | 主信号 |
| `pv37_low_110000` | MATRIX | 1.0 | 1 | 1 | 量价/量能：Low price at 11:00 | 主信号 |
| `pv37_low_12` | MATRIX | 1.0 | 3 | 3 | 量价/量能：Low price | 主信号 |
| `pv37_low_130000` | MATRIX | 1.0 | 8 | 8 | 量价/量能：Low price at 13:00 | 主信号 |
| `pv37_low_14` | MATRIX | 1.0 | 4 | 4 | 量价/量能：14-Day Lowest Price | 主信号 |
| `pv37_low_140000` | MATRIX | 1.0 | 3 | 3 | 量价/量能：Low price at 14:00 | 主信号 |
| `pv37_low_1430` | MATRIX | 1.0 | 2 | 2 | 量价/量能：Low price at 14:30 | 主信号 |
| `pv37_low_163000` | MATRIX | 1.0 | 3 | 3 | 量价/量能：Lowest price at 16:30 | 主信号 |
| `pv37_ltov` | MATRIX | 0.3482 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_lvdv` | MATRIX | 0.3651 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_market_cap` | MATRIX | 0.6783 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：The total value of all a company's shares of stock | 主信号 |
| `pv37_market_cap_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the total market value of a company's outstanding shares | 对照 |
| `pv37_min_noncontrol_interest_credits` | MATRIX | 0.9633 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Minimum noncontrolling interest credits | 主信号 |
| `pv37_minority_noncontrolling_interest` | MATRIX | 0.9935 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Minority non-controlling interest | 主信号 |
| `pv37_most_recent_qrt_eps_surprise` | MATRIX | 0.6783 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：The difference between expected and actual earnings per share for the most recent quarter | 主信号 |
| `pv37_most_recent_qrt_eps_surprise_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：Direct indicator for the most recent quarterly earnings per share surprise | 对照 |
| `pv37_msci_acwi_member` | MATRIX | 0.6783 | 2 | 2 | 分类标识：Indicates whether the company is part of the MSCI All Country World Index | 分组轴 |
| `pv37_msci_acwi_member_di` | MATRIX | 1.0 | 2 | 2 | 母字段直接指示器（同义标准化版）：Direct indicator for membership in the MSCI ACWI | 对照 |
| `pv37_msci_eafe_member_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for membership in the MSCI EAFE | 对照 |
| `pv37_mthe` | MATRIX | 0.346 | 1 | 1 | 量价/量能：Market trend high end for all instruments | 主信号 |
| `pv37_nav_best_crncy_iso` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best currency ISO for NAV | 主信号 |
| `pv37_nav_best_cur_fiscal_qtr_period` | MATRIX | 0.8516 | 1 | 1 | 分析师一致预期（best 族）：Best current fiscal quarter period for NAV | 主信号 |
| `pv37_nav_best_cur_fiscal_semi_year_period` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best current fiscal semi-year period for NAV | 主信号 |
| `pv37_nav_best_cur_fiscal_year_period` | MATRIX | 0.8516 | 1 | 1 | 分析师一致预期（best 族）：Best current fiscal year period for NAV | 主信号 |
| `pv37_nav_best_eeps_cur_yr` | MATRIX | 0.7756 | 4 | 4 | 分析师一致预期（best 族）：Best estimated EPS current year for NAV | 主信号 |
| `pv37_nav_best_eeps_nxt_yr` | MATRIX | 0.768 | 7 | 7 | 分析师一致预期（best 族）：Best estimated EPS next year for NAV | 主信号 |
| `pv37_nav_best_fiscal_period_dt` | VECTOR | 0.716 | 0 | 0 | 分析师一致预期（best 族）：Best fiscal period date for NAV | 主信号 |
| `pv37_nav_best_fperiod_override` | VECTOR | 0.6364 | 2 | 3 | 分析师一致预期（best 族）：Best fiscal period override for NAV | 主信号 |
| `pv37_nav_expected_report_period` | VECTOR | 0.716 | 0 | 0 | 时点/状态标识：Expected report period for NAV | 排除 |
| `pv37_nav_market_status` | VECTOR | 0.716 | 1 | 1 | 时点/状态标识：Market status for NAV | 排除 |
| `pv37_net_income` | MATRIX | 0.964 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Net income | 主信号 |
| `pv37_net_income_bef_mi` | MATRIX | 0.9643 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Net income before minority interest | 主信号 |
| `pv37_net_non_oper_loss` | MATRIX | 0.9612 | 2 | 3 | 基本面慢变量（裸水平撞规模代理）：Net non-operating loss | 主信号 |
| `pv37_netprofit_gaap_best_crncy_iso` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best currency ISO for net profit GAAP | 主信号 |
| `pv37_netprofit_gaap_best_cur_fiscal_qtr_period` | MATRIX | 0.8516 | 0 | 0 | 分析师一致预期（best 族）：Best current fiscal quarter period for net profit GAAP | 主信号 |
| `pv37_netprofit_gaap_best_cur_fiscal_semi_year_period` | MATRIX | 1.0 | 1 | 1 | 分析师一致预期（best 族）：Best Current Fiscal Semi-Year Period for Net Profit GAAP | 主信号 |
| `pv37_netprofit_gaap_best_cur_fiscal_year_period` | MATRIX | 0.8517 | 2 | 3 | 分析师一致预期（best 族）：Best current fiscal year period for net profit GAAP | 主信号 |
| `pv37_netprofit_gaap_best_eeps_cur_yr` | MATRIX | 0.7756 | 9 | 9 | 分析师一致预期（best 族）：Best estimated EPS current year for net profit GAAP | 主信号 |
| `pv37_netprofit_gaap_best_eeps_nxt_yr` | MATRIX | 0.768 | 3 | 3 | 分析师一致预期（best 族）：Best estimated EPS next year for net profit GAAP | 主信号 |
| `pv37_netprofit_gaap_best_fiscal_period_dt` | VECTOR | 0.7872 | 0 | 0 | 分析师一致预期（best 族）：Best fiscal period date for net profit GAAP | 主信号 |
| `pv37_netprofit_gaap_best_fperiod_override` | VECTOR | 0.6975 | 1 | 0 | 分析师一致预期（best 族）：Best fiscal period override for net profit GAAP | 主信号 |
| `pv37_netprofit_gaap_expected_report_period` | VECTOR | 0.7872 | 2 | 2 | 时点/状态标识：Expected report period for net profit GAAP | 排除 |
| `pv37_netprofit_gaap_latest_ann_dt_qtrly` | VECTOR | 0.6049 | 7 | 14 | 时点/状态标识：Latest annual date quarterly for net profit GAAP | 排除 |
| `pv37_netprofit_gaap_market_status` | VECTOR | 0.7872 | 1 | 1 | 时点/状态标识：Market status for net profit GAAP | 排除 |
| `pv37_netprofit_gaap_most_recent_period_end_dt` | VECTOR | 0.6277 | 1 | 1 | 时点/状态标识：Most recent period end date for net profit GAAP | 排除 |
| `pv37_nicv` | MATRIX | 0.4886 | 1 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_nirv` | MATRIX | 0.4855 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_notes_receivable` | MATRIX | 1.0 | 2 | 5 | 基本面慢变量（裸水平撞规模代理）：Notes receivable | 主信号 |
| `pv37_nppv` | MATRIX | 0.7323 | 1 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_num_of_analysts_fy1_forecasts` | MATRIX | 0.6783 | 2 | 2 | 分析师预期/修正：The number of financial analysts providing earnings forecasts for the company's fiscal year 1 | 主信号 |
| `pv37_num_of_analysts_fy1_forecasts_di` | MATRIX | 1.0 | 1 | 1 | 分析师预期/修正：Direct indicator for the number of analysts providing forecasts for fiscal year 1 | 主信号 |
| `pv37_odrv` | MATRIX | 0.3552 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_ohbs` | MATRIX | 0.344 | 2 | 2 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_open_10` | MATRIX | 1.0 | 3 | 3 | 量价/量能：10-Day Opening Price | 主信号 |
| `pv37_open_110000` | MATRIX | 1.0 | 3 | 9 | 量价/量能：Open price at 11:00 | 主信号 |
| `pv37_open_12` | MATRIX | 1.0 | 2 | 2 | 量价/量能：Open price | 主信号 |
| `pv37_open_130000` | MATRIX | 1.0 | 4 | 4 | 量价/量能：Open price at 13:00 | 主信号 |
| `pv37_open_14` | MATRIX | 1.0 | 3 | 3 | 量价/量能：14-Day Opening Price | 主信号 |
| `pv37_open_140000` | MATRIX | 1.0 | 2 | 2 | 量价/量能：Open Price at 14:00 | 主信号 |
| `pv37_open_1430` | MATRIX | 1.0 | 3 | 4 | 量价/量能：Open Price at 14:30 | 主信号 |
| `pv37_open_163000` | MATRIX | 1.0 | 2 | 2 | 量价/量能：Opening price at 16:30 | 主信号 |
| `pv37_operatingprofit_best_crncy_iso` | MATRIX | 1.0 | 0 | 0 | 分析师一致预期（best 族）：Best currency ISO for operating profit | 主信号 |
| `pv37_operatingprofit_best_cur_fiscal_qtr_period` | MATRIX | 0.8516 | 1 | 1 | 分析师一致预期（best 族）：Best current fiscal quarter period for operating profit | 主信号 |
| `pv37_operatingprofit_best_cur_fiscal_semi_year_period` | MATRIX | 0.9999 | 0 | 0 | 分析师一致预期（best 族）：Best current fiscal semi-year period for operating profit | 主信号 |
| `pv37_operatingprofit_best_cur_fiscal_year_period` | MATRIX | 0.8516 | 1 | 1 | 分析师一致预期（best 族）：Best current fiscal year period for operating profit | 主信号 |
| `pv37_operatingprofit_best_eeps_cur_yr` | MATRIX | 0.7756 | 6 | 7 | 分析师一致预期（best 族）：Best estimated EPS current year for operating profit | 主信号 |
| `pv37_operatingprofit_best_eeps_nxt_yr` | MATRIX | 0.768 | 26 | 39 | 分析师一致预期（best 族）：Best estimated EPS next year for operating profit | 主信号 |
| `pv37_operatingprofit_best_fiscal_period_dt` | VECTOR | 0.3229 | 1 | 2 | 分析师一致预期（best 族）：Best fiscal period date for operating profit | 主信号 |
| `pv37_operatingprofit_expected_report_period` | VECTOR | 0.3229 | 0 | 0 | 时点/状态标识：Expected report period for operating profit | 排除 |
| `pv37_operatingprofit_market_status` | VECTOR | 0.3229 | 0 | 0 | 时点/状态标识：Market status for operating profit | 排除 |
| `pv37_opts` | MATRIX | 0.958 | 4 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_opxv` | MATRIX | 0.3949 | 0 | 0 | 量价/量能：Total x-partnership operations traded volume | 主信号 |
| `pv37_ox_feb_spe_lid_si` | MATRIX | 0.8706 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Operating expense for February special items | 主信号 |
| `pv37_pcsv` | MATRIX | 0.4841 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_periods` | MATRIX | 0.6452 | 1 | 0 | 时点/状态标识：The specific periods for which financial reports are prepared | 排除 |
| `pv37_periods_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the financial reporting periods | 对照 |
| `pv37_ppdv` | MATRIX | 0.5938 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_ppfv` | MATRIX | 0.349 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_pretax_inc` | MATRIX | 0.9651 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Pre-tax income | 主信号 |
| `pv37_pric_volatil` | MATRIX | 0.6783 | 3 | 4 | 量价/量能：The degree of variation in the price of the company's stock over time | 主信号 |
| `pv37_pric_volatil_di` | MATRIX | 1.0 | 3 | 3 | 母字段直接指示器（同义标准化版）：Direct indicator for the volatility of the company's stock price | 对照 |
| `pv37_profitabil_cons` | MATRIX | 0.6452 | 3 | 6 | 分析师预期/修正：The general agreement among financial analysts regarding the profitability of the company | 主信号 |
| `pv37_profitabil_cons_di` | MATRIX | 1.0 | 1 | 1 | 分析师预期/修正：Direct indicator for the consensus among analysts on the company's profitability | 主信号 |
| `pv37_profitability` | MATRIX | 0.6452 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：The ability of the company to generate earnings as compared to its expenses and other relevant costs | 主信号 |
| `pv37_profitability_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：Direct indicator for the company's profitability metrics | 对照 |
| `pv37_pxe_rped_si` | MATRIX | 0.9506 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Expense related to research and development special items | 主信号 |
| `pv37_qbbs` | MATRIX | 0.3444 | 2 | 3 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_qdbs` | MATRIX | 0.3441 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_qftm` | MATRIX | 0.358 | 1 | 2 | 量价/量能：Market trend fill quality for all instruments | 主信号 |
| `pv37_return_on_equity` | MATRIX | 0.6783 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：A measure of the profitability of a business in relation to the equity | 主信号 |
| `pv37_return_on_equity_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：A measure of the profitability of a business | 对照 |
| `pv37_returns15` | MATRIX | 0.9955 | 5 | 5 | 量价/量能：Returns over 15 days | 主信号 |
| `pv37_returns180` | MATRIX | 0.9567 | 1 | 3 | 量价/量能：Returns over 180 days | 主信号 |
| `pv37_returns200` | MATRIX | 0.9527 | 3 | 4 | 量价/量能：200-day returns | 主信号 |
| `pv37_returns25` | MATRIX | 0.9933 | 5 | 7 | 量价/量能：Returns over 25 days | 主信号 |
| `pv37_returns30` | MATRIX | 0.9922 | 2 | 3 | 量价/量能：30-Day Returns | 主信号 |
| `pv37_returns40` | MATRIX | 0.9898 | 5 | 5 | 量价/量能：Returns over 40 days | 主信号 |
| `pv37_returns5` | MATRIX | 0.996 | 44 | 178 | 量价/量能：Returns over 5 days | 主信号 |
| `pv37_returns50` | MATRIX | 0.9876 | 4 | 4 | 量价/量能：50-day returns | 主信号 |
| `pv37_returns70` | MATRIX | 0.983 | 4 | 5 | 量价/量能：Returns over 70 days | 主信号 |
| `pv37_returns75` | MATRIX | 0.9816 | 3 | 3 | 量价/量能：Returns over 75 days | 主信号 |
| `pv37_returns90` | MATRIX | 0.9777 | 2 | 3 | 量价/量能：Returns over 90 days | 主信号 |
| `pv37_rnmv` | MATRIX | 0.6212 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_roa_best_crncy_iso` | MATRIX | 1.0 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：ROA best currency ISO | 主信号 |
| `pv37_roa_best_cur_fiscal_qtr_period` | MATRIX | 0.8516 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：ROA best current fiscal quarter period | 主信号 |
| `pv37_roa_best_cur_fiscal_semi_year_period` | MATRIX | 1.0 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：ROA best current fiscal semi-year period | 主信号 |
| `pv37_roa_best_cur_fiscal_year_period` | MATRIX | 0.8516 | 5 | 8 | 基本面慢变量（裸水平撞规模代理）：ROA best current fiscal year period | 主信号 |
| `pv37_roa_best_eeps_cur_yr` | MATRIX | 0.7756 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：ROA best estimate EPS current year | 主信号 |
| `pv37_roa_best_eeps_nxt_yr` | MATRIX | 0.768 | 6 | 8 | 基本面慢变量（裸水平撞规模代理）：ROA best estimate EPS next year | 主信号 |
| `pv37_roa_best_fiscal_period_dt` | VECTOR | 0.7166 | 1 | 6 | 时点/状态标识：ROA best fiscal period date | 排除 |
| `pv37_roa_best_fperiod_override` | VECTOR | 0.6332 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：ROA best fiscal period override | 主信号 |
| `pv37_roa_expected_report_period` | VECTOR | 0.7166 | 2 | 2 | 时点/状态标识：ROA expected report period | 排除 |
| `pv37_roa_market_status` | VECTOR | 0.7166 | 0 | 0 | 时点/状态标识：ROA market status | 排除 |
| `pv37_rpts` | MATRIX | 0.395 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_rtdv` | MATRIX | 0.5251 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_rxfv` | MATRIX | 0.349 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_sales_rev_turn` | MATRIX | 0.9637 | 8 | 11 | 基本面慢变量（裸水平撞规模代理）：Sales revenue turnover | 主信号 |
| `pv37_sedol` | MATRIX | 0.6452 | 1 | 1 | 分类标识：A unique identifier assigned to securities in the United Kingdom | 分组轴 |
| `pv37_sedol_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：Direct indicator for the SEDOL code | 对照 |
| `pv37_spe_si` | MATRIX | 0.9627 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Special items | 主信号 |
| `pv37_spts` | MATRIX | 0.5916 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_sptv` | MATRIX | 0.3778 | 0 | 0 | 量价/量能：Total private securities traded volume | 主信号 |
| `pv37_ssfv` | MATRIX | 0.958 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_stk_pric_mom` | MATRIX | 0.6452 | 0 | 0 | 量价/量能：Direct indicator for the volatility of the stock price | 主信号 |
| `pv37_stk_pric_mom_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：The rate of acceleration of a security's price or volume | 对照 |
| `pv37_stk_pric_volatil` | MATRIX | 0.6452 | 0 | 0 | 量价/量能：Direct indicator for the change in stock price over the last 6 months | 主信号 |
| `pv37_stk_pric_volatil_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：The rate at which the price of the stock increases or decreases for a given set of returns | 对照 |
| `pv37_stock_price` | MATRIX | 0.6783 | 1 | 1 | 分类标识：Direct indicator for the company's ticker symbol | 分组轴 |
| `pv37_stock_price_change_6month` | MATRIX | 0.6783 | 1 | 1 | 量价/量能：Direct indicator for the current stock price | 主信号 |
| `pv37_stock_price_change_6month_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：The percentage change in the company's stock price over the past 6 months | 对照 |
| `pv37_stock_price_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：The current price at which a particular stock can be bought or sold | 对照 |
| `pv37_suit` | MATRIX | 0.3509 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_tcxv` | MATRIX | 0.3557 | 1 | 1 | 量价/量能：Total x-certificate traded volume | 主信号 |
| `pv37_ticker` | MATRIX | 0.6452 | 0 | 0 | 基本面慢变量（裸水平撞规模代理）：Direct indicator for the trailing price-to-earnings ratio | 主信号 |
| `pv37_ticker_di` | MATRIX | 1.0 | 3 | 6 | 母字段直接指示器（同义标准化版）：The unique series of letters assigned to a security for trading purposes | 对照 |
| `pv37_tot_int_exp` | MATRIX | 0.9236 | 1 | 2 | 基本面慢变量（裸水平撞规模代理）：Total interest expense | 主信号 |
| `pv37_tpds` | MATRIX | 0.996 | 1 | 1 | 量价/量能：Trade Price Downside | 主信号 |
| `pv37_trailing_price_to_earnings` | MATRIX | 0.6452 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：A specific financial metric or calculation | 主信号 |
| `pv37_trailing_price_to_earnings_di` | MATRIX | 1.0 | 1 | 1 | 母字段直接指示器（同义标准化版）：The price-to-earnings ratio based on the previous 12 months of earnings | 对照 |
| `pv37_trailing_price_to_earnings_f` | MATRIX | 0.6783 | 0 | 0 | 时点/状态标识：The data date for the specific financial metric or calculation | 排除 |
| `pv37_trailing_price_to_earnings_f_di` | MATRIX | 1.0 | 0 | 0 | 母字段直接指示器（同义标准化版）：The estimated price-to-earnings ratio based on forecasted earnings | 对照 |
| `pv37_vaga` | MATRIX | 0.3368 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vdcv` | MATRIX | 0.5091 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_verd` | MATRIX | 0.3732 | 2 | 5 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vicd` | MATRIX | 0.5587 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vint` | MATRIX | 0.6902 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vlar` | MATRIX | 1.0 | 4 | 4 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_volume_10` | MATRIX | 1.0 | 10 | 11 | 量价/量能：10-Day Trading Volume | 主信号 |
| `pv37_volume_110000` | MATRIX | 1.0 | 2 | 2 | 量价/量能：Volume at 11:00 | 主信号 |
| `pv37_volume_12` | MATRIX | 1.0 | 8 | 8 | 量价/量能：Trading volume | 主信号 |
| `pv37_volume_130000` | MATRIX | 1.0 | 5 | 6 | 量价/量能：Volume at 13:00 | 主信号 |
| `pv37_volume_14` | MATRIX | 1.0 | 1 | 1 | 量价/量能：14-Day Trading Volume | 主信号 |
| `pv37_volume_140000` | MATRIX | 1.0 | 6 | 8 | 量价/量能：Volume at 14:00 | 主信号 |
| `pv37_volume_1430` | MATRIX | 1.0 | 3 | 3 | 量价/量能：Volume at 14:30 | 主信号 |
| `pv37_volume_163000` | MATRIX | 1.0 | 7 | 7 | 量价/量能：Trading volume at 16:30 | 主信号 |
| `pv37_voto` | MATRIX | 0.5196 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vpad` | MATRIX | 0.9516 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vpic` | MATRIX | 0.3425 | 1 | 1 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vtar` | MATRIX | 0.361 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vtau` | MATRIX | 0.4192 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |
| `pv37_vwap_10` | MATRIX | 1.0 | 3 | 4 | 量价/量能：10-Day VWAP | 主信号 |
| `pv37_vwap_110000` | MATRIX | 1.0 | 2 | 2 | 量价/量能：VWAP at 11:00 | 主信号 |
| `pv37_vwap_12` | MATRIX | 1.0 | 7 | 7 | 量价/量能：VWAP | 主信号 |
| `pv37_vwap_130000` | MATRIX | 1.0 | 3 | 3 | 量价/量能：VWAP at 13:00 | 主信号 |
| `pv37_vwap_14` | MATRIX | 1.0 | 3 | 3 | 量价/量能：14-Day VWAP | 主信号 |
| `pv37_vwap_140000` | MATRIX | 1.0 | 1 | 0 | 量价/量能：VWAP at 14:00 | 主信号 |
| `pv37_vwap_1430` | MATRIX | 1.0 | 4 | 5 | 量价/量能：VWAP at 14:30 | 主信号 |
| `pv37_vwap_163000` | MATRIX | 1.0 | 11 | 14 | 量价/量能：Volume-weighted average price at 16:30 | 主信号 |
| `pv37_xo_gl_net_of_tax` | MATRIX | 0.9642 | 2 | 2 | 基本面慢变量（裸水平撞规模代理）：Extraordinary items, gains, and losses, net of tax | 主信号 |
| `pv37_xsit` | MATRIX | 0.358 | 0 | 0 | 量价/量能：Total x-security interest traded volume | 主信号 |
| `pv37_yqe_dfp_sb` | MATRIX | 0.9931 | 1 | 1 | 基本面慢变量（裸水平撞规模代理）：Yearly quarter-end deferred payment service balance | 主信号 |
| `pv37_zhbs` | MATRIX | 0.3505 | 0 | 0 | 模板化评估语句，经济语义失真 | 排除 |

## 结构总览（由全量拉取统计）

- 类型分布：MATRIX 777 / VECTOR 96（VECTOR 元数据 coverage 仅供排序，实测有效覆盖需 Long Count 核验，见风险节）
- coverage 分档：1.0 共 145；0.9–1.0 共 109；0.7–0.9 共 279；0.4–0.7 共 237；0.05–0.4 共 103；无 <0.05 字段
- alphaCount 分档：0 共 275；1–5 共 451；6–20 共 120；21–50 共 14；50+ 共 13
- 角色分布：主信号 563，排除 230，对照 62，分组轴 18
- 家族分布：fundamental 315，template_noise 170，best_consensus 113，price_volume 104，di_variant 62，timestamp 31，mfm2 29，classification 18，analyst 12，vda 10，drai 6，fx 3
- vda 族（10 字段）：`pv37_001vda`、`pv37_01vda`、`pv37_03vda`、`pv37_06vda`、`pv37_081vda`、`pv37_1vda`、`pv37_36vda`、`pv37_4vda`、`pv37_5vda`、`pv37_6vda`
- alphaCount 最高字段（拥挤度风险）：`pv37_all_cinx`(178)、`pv37_intfv_mfm_rltr`(177)、`pv37_all_mtps`(151)、`pv37_all_adbs`(79)、`pv37_all_cdav`(73)、`pv37_all_sbit`(48)、`pv37_all_iabs`(43)
- alphaCount=0 字段 275 个，多为模板评估族与未被使用的慢变量，仅作储备，不进候选

## 机制假设（5 条）

1. **vda 前瞻偏离机制**｜**流量型**｜vda 族是成交量日间前瞻预测，其预测值与实现成交量的偏离刻画订单流知情程度与预期兑现：预测上修而实现未兑现时存在短期价格漂移｜适用统计族：ts_delta（预测-实现差）、ts_rank/ts_zscore（相对自身历史偏离）、divide（预测÷实现）｜证伪条件：若 ts_delta(vda) 的 ts_rank 信号在 KOR/TOP600 全期 S<1.0 且 2Y<0，且与 pv1 等既有量能族字段横截面相关性>0.9（被既有量能信号吸收），则机制证伪。
2. **分析师预期修正扩散机制**｜**流量型**｜best_cps/NAV/EBITDA 等一致预期族的 4 周上调/下调净扩散与修正幅度反映预期动量，预期修正后存在漂移｜适用统计族：横截面 rank、ts_zscore、净扩散=up-dn 的差值构造｜证伪条件：净扩散信号与修正幅度自身相关性>0.95（无增量信息），或全期 S<1.0、2Y<0。
3. **慢变量水平撞规模代理机制（负向）**｜**存量型**｜bs_*/is_*/intfv_* 等基本面慢变量（股本结构、资本结构、市值余额、治理类）的横截面水平值在 KOR/TOP600 小宇宙基本是规模/行业代理，裸水平信号易撞 self 与规模因子｜适用统计族：ts_delta（季频变化量）、ts_rank/ts_zscore（相对自身历史分位）、group_std（行业间离散度）替代裸水平｜证伪条件：若 ts_rank(bs_x) 变换后信号仍与市值 rank 相关性>0.9 且 S<1.0，则规模代理假说成立，该族不可作主信号。
4. **日内量能切片结构机制**｜**流量型**｜volume_110000/140000、cap_130000 等日内时点量能切片反映日内订单流时点结构，切片间比值刻画盘中/尾盘资金偏好｜适用统计族：divide（切片÷全天量能）、ts_zscore｜证伪条件：各切片与全天量能/avg_daily_trading_volume 相关性>0.95 且增量 S<0.5，则切片无增量信息。
5. **模板评估族伪变量机制（负向）**｜**存量型**｜all_* 等「Assessment of Sale of…/Quality assessment of…」模板字段描述为模板化生成、无一致经济含义，横截面水平是伪变量；其中 alphaCount 高者（cinx 178、mtps 151）反映历史使用拥挤而非信号价值｜适用统计族：不作信号，仅作相关性对照与排除表｜证伪条件：若任一模板字段 rank 信号在 2Y 检验中 S>1.25 且跨配置可复现，则其存在隐藏真实语义，须重估并移出排除表。

## 推荐回测档

- **universe**：TOP600（KOR 战役配置，`tracking/KOR/config/settings.json:5`）
- **中性化**：SECTOR（KOR 实证主流档，`tracking/KOR/config/cells.json` 多处 KOR/SECTOR/TOP600 结论基于此档）
- **decay**：5（量能与预期修正类信号的标准平滑档，抑制单日噪声）
- **truncation**：0.08（KOR 小宇宙常规截断）
- **backfill**：需要。96 个 VECTOR 字段（best_* 一致预期族为主）元数据 coverage 存在高估风险，CW FAIL 时用 ts_backfill 补覆盖，而不是调 decay/truncation
- **NaN handling**：ON；**maxTrade**：OFF
- 理由：KOR TOP600 小宇宙放大 CW/longCount 问题（`tracking/KOR/config/thresholds.json:96`），量能族信号需 trade_when 流动性门或双层平滑；本集塔位倍率 1.4，PV 塔 2/3 为近闸未亮塔，本集仅作后续波储备，不挪用已亮塔存量

## 风险与备注

- 三条前置未验（承接候选理由）：vda 的 N 是提前天数还是模型编号未验；十年覆盖未验；与 pv1 量能字段的相关性未验——三者任一不成立则 M1 机制需重估
- 集内 5 族已 4 死（PV 类历史结论），本集描述失配（异构杂烩），画像如实呈现，不按「PV 量能集」整体乐观预设
- VECTOR 字段（96 个）coverage 元数据仅供排序，实测有效覆盖可能远低于标称，投入前必须先做 Long Count 实测；<0.05 直接数据层排除，0.05–0.4 只作门控条件
- 本档案为字段画像与归档，不含仿真；机制假设的证伪条件供后续波次预注册使用
