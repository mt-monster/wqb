# news23 — EUR 字段画像

> 自动生成于 2026-10-20 17:55　|　[← 返回索引](README.md)

## 一、数据集元信息

| 项 | 值 |
|---|---|
| 数据集 ID | `news23` |
| 名称 | MnA Deals Data |
| 类别 | NEWS |
| 数据字段数(平台) | 136 |
| 覆盖率 | 0.4462 |
| 平台已有 alpha | 104 |
| valueScore | 3.0 |
| 金字塔倍率 | 1.3 |
| 数据类型 | — |
| delay | 1 |
| 状态 | — |

## 二、数据集描述（平台原文）

> ⚠️ 平台目录描述存在**错配**（已实测：insiders1 / imbalance5 的描述指向无关数据集）。以「五、全字段明细」的真实字段语义为准。

This dataset offers detailed information on mergers and acquisitions (M&A), new equity issues, and debt offerings, including deal structure, participants, financial terms, and status. It covers transaction attributes such as deal value, premiums, payment methods, industry classifications, and advisor involvement. By tracking deal flow, market trends, and competitive dynamics, the dataset enables users to analyze market share, identify comparable transactions, and assess the impact of corporate actions on stock prices. It is highly valuable for predicting price movements around deal announcements, understanding industry consolidation, and constructing event-driven trading strategies.

## 三、字段画像汇总

| 维度 | 结果 |
|---|---|
| 字段总数 | **136** |
| 类型分布 | VECTOR×136 |
| 平均覆盖率 | **0.446** |
| 覆盖率区间 | 0.19 ~ 0.77 |
| 更新频率（推断） | 事件/逐笔型（VECTOR） |
| 可用性评级 | 低（覆盖 <50%，仅作条件/分组或放弃） |

**覆盖率分档**

| 档 | 字段数 | 占比 |
|---|---:|---:|
| 高 (≥0.90) | 0 | 0.0% |
| 中 (0.70–0.90) | 23 | 16.9% |
| 低 (0.50–0.70) | 30 | 22.1% |
| 稀疏 (<0.50) | 83 | 61.0% |

**历史实测分布（field_profile_perf）**

| 判定 | 字段数 | 占比 |
|---|---:|---:|
| UNUSABLE | 83 | 61.0% |
| UNTESTED | 53 | 39.0% |

- 无带 `n_tests>0` 的有效实测记录；但历史判定已存在（UNTESTED 53 / UNUSABLE 83 等）。⚠ 历史判定可能**过时**（如 analyst7 的旧判死已作废），做尽前须重跑。

## 四、语义维度地图（自动归类）

| 语义族 | 字段数 | 平均覆盖 | 代表字段 |
|---|---:|---:|---|
| 其他 | 58 | 0.43 | company_employee_count_2、company_veic6_category、firm_capital_under_management_2 |
| 价量与波动 | 31 | 0.35 | company_offer_unit_price、company_purchase_price_2、company_offered_price |
| 盈利与财务 | 23 | 0.41 | company_offer_total_size、company_sales_amount_2、fund_total_size_2 |
| 持仓与资金流 | 12 | 0.73 | fund_raising_quarter_amount_2、fund_total_target_amount_2、fundraising_commitment_amount_2 |
| 宏观与行业 | 6 | 0.46 | company_sic_code、company_industry_code、company_industry_sic_code |
| 修正与预期 | 6 | 0.73 | individual_job_title_2、investment_detail_estimated_fund_total、investment_detail_estimated_round_total |

## 五、全字段明细

> 按 `best_sharpe` 降序（未测者置后）。`判定` 来自 `field_profile_perf`：ALIVE=历史测出过 S≥闸线（**不代表可提交**）；UNTESTED=未测；UNUSABLE/DEAD/AXIS_ONLY=已证否或仅可作轴。

| # | 字段名 | 类型 | 覆盖 | 语义族 | 测次 | best_S | best_2Y | best_sub | 判定 | 描述 |
|---:|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | `company_employee_count_2` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Number of employees for the invested company (possibly at time of deal) |
| 2 | `company_offer_total_size` | VECTOR | 0.770 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total size of the offer for company shares or assets. |
| 3 | `company_offer_unit_price` | VECTOR | 0.770 | 价量与波动 | 0 | — | — | — | UNTESTED | Offer price in a related funding/deal event for the investee company |
| 4 | `company_purchase_price_2` | VECTOR | 0.770 | 价量与波动 | 0 | — | — | — | UNTESTED | Purchase price paid for the company. |
| 5 | `company_sales_amount_2` | VECTOR | 0.770 | 盈利与财务 | 0 | — | — | — | UNTESTED | Reported sales/revenue figure for the company receiving VC investment; usually last reported or most recent value |
| 6 | `company_sic_code` | VECTOR | 0.770 | 宏观与行业 | 0 | — | — | — | UNTESTED | Standard Industry Classification code for the investee company |
| 7 | `company_veic6_category` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | VEIC6 category classification for the company. |
| 8 | `firm_capital_under_management_2` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Total capital managed by the firm. |
| 9 | `fund_raising_quarter_amount_2` | VECTOR | 0.770 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total capital raised by the fund in a specific quarter |
| 10 | `fund_total_size_2` | VECTOR | 0.770 | 盈利与财务 | 0 | — | — | — | UNTESTED | Total committed or raised capital of a private equity/venture capital fund |
| 11 | `fund_total_target_amount_2` | VECTOR | 0.770 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total target amount the fund aims to raise |
| 12 | `fundraising_commitment_amount_2` | VECTOR | 0.770 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total amount of committed capital raised for the venture capital fund in the fundraising round |
| 13 | `individual_job_title_2` | VECTOR | 0.770 | 修正与预期 | 0 | — | — | — | UNTESTED | Professional title/role of the individual (e.g., Partner, CEO, Analyst) |
| 14 | `investment_detail_age_months` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Age of the investment detail in months. |
| 15 | `investment_detail_age_years_2` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Age of the investment detail in years. |
| 16 | `investment_detail_deal_value` | VECTOR | 0.770 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Investment amount or deal value for the funding round |
| 17 | `investment_detail_disclosed_valuation` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Disclosed valuation amount for the investee company at the time of the VC investment round |
| 18 | `investment_detail_estimated_fund_total` | VECTOR | 0.770 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated total funding amount involved in the investment deal details for the VC round |
| 19 | `investment_detail_estimated_round_total` | VECTOR | 0.770 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated total investment amount for the funding round |
| 20 | `investment_detail_stage_one` | VECTOR | 0.770 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Primary investment stage (e.g., seed, early, growth) for the funding round |
| 21 | `investment_detail_stage_three` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Stage three classification for the investment detail. |
| 22 | `investment_detail_stage_two` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Stage two classification for the investment detail. |
| 23 | `investment_round_total_amount` | VECTOR | 0.770 | 其他 | 0 | — | — | — | UNTESTED | Total amount invested in the round for the company/deal |
| 24 | `actual_investment_round_total` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Total amount invested in a particular investment round |
| 25 | `company_employee_count` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Number of employees at the company. |
| 26 | `company_inception_year` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Year the company was founded or established |
| 27 | `company_industry_code` | VECTOR | 0.696 | 宏观与行业 | 0 | — | — | — | UNTESTED | Industry classification code for the company. |
| 28 | `company_industry_sic_code` | VECTOR | 0.696 | 宏观与行业 | 0 | — | — | — | UNTESTED | Standard Industry Classification code for the portfolio company’s primary industry |
| 29 | `company_offer_size_value` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Size of the offer made to the company, typically in monetary terms. |
| 30 | `company_offered_price` | VECTOR | 0.696 | 价量与波动 | 0 | — | — | — | UNTESTED | Offer price per share for the company in an IPO or similar transaction |
| 31 | `company_purchase_price` | VECTOR | 0.696 | 价量与波动 | 0 | — | — | — | UNTESTED | Purchase price paid for the company in the buyout transaction |
| 32 | `company_sales_amount` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Reported sales amount for the company. |
| 33 | `estimated_investment_round_total` | VECTOR | 0.696 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated total amount for the investment round. |
| 34 | `firm_capital_under_management` | VECTOR | 0.696 | 盈利与财务 | 0 | — | — | — | UNTESTED | Amount of capital managed by the private equity firm (AUM or similar metric) |
| 35 | `firm_establishment_year` | VECTOR | 0.696 | 盈利与财务 | 0 | — | — | — | UNTESTED | Year when the private equity firm was founded |
| 36 | `firm_inception_year` | VECTOR | 0.696 | 盈利与财务 | 0 | — | — | — | UNTESTED | Date when the private equity firm was founded |
| 37 | `fund_establishment_year` | VECTOR | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Year the fund was founded or established |
| 38 | `fund_inception_year` | VECTOR | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Year the fund was established/founded |
| 39 | `fund_raising_quarter_amount` | VECTOR | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Fundraising amount (capital raised or committed) during a specific quarter |
| 40 | `fund_raising_year` | VECTOR | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Calendar year in which fundraising activity or report occurred |
| 41 | `fund_total_size` | VECTOR | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Size of the fund, typically measured in monetary terms such as total committed capital |
| 42 | `fund_total_target_amount` | VECTOR | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Total capital target for fundraising for the fund (goal amount to be raised) |
| 43 | `fundraising_commitment_amount` | VECTOR | 0.696 | 持仓与资金流 | 0 | — | — | — | UNTESTED | Amount of committed capital in the fund’s fundraising round |
| 44 | `individual_job_title` | VECTOR | 0.696 | 修正与预期 | 0 | — | — | — | UNTESTED | Job title of the individual (e.g., Managing Director, Partner, Analyst) |
| 45 | `investment_age_months` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Age of the investment in months since inception. |
| 46 | `investment_deal_value` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | The total monetary value of the investment/deal disclosed for this buyout transaction |
| 47 | `investment_detail_age_years` | VECTOR | 0.696 | 盈利与财务 | 0 | — | — | — | UNTESTED | Age (in years) of the company or asset involved, typically since founding or incorporation |
| 48 | `investment_disclosed_valuation` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Amount of the company's valuation disclosed at the time of the deal |
| 49 | `investment_estimated_total_funding` | VECTOR | 0.696 | 修正与预期 | 0 | — | — | — | UNTESTED | Estimated total funding amount for the investment. |
| 50 | `investment_round_number` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | The numeric sequence or designation of the investment round for a company or deal |
| 51 | `investment_stage_category` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Category describing the stage of the investment (e.g., seed, growth, exit). |
| 52 | `investment_stage_primary` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Primary stage of the investment (e.g., seed, growth). |
| 53 | `investment_stage_secondary` | VECTOR | 0.696 | 其他 | 0 | — | — | — | UNTESTED | Secondary stage of the investment (e.g., expansion, late). |
| 54 | `nws23_acquiror_akw1rpa` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Acquiror's stock price one week after deal announcement |
| 55 | `nws23_acquiror_apr1daya` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Acquiror's stock price one day after the deal announcement |
| 56 | `nws23_acquiror_apr1dayb` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Acquiror's stock price one day before deal announcement |
| 57 | `nws23_acquiror_asalesltm` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Acquiror Net Sales in Last 12 Months |
| 58 | `nws23_acquiror_emu_hostvalue` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Deal value in million Euros |
| 59 | `nws23_acquiror_laitni_rp` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Initial price per common share or partnership unit offered by the acquiror |
| 60 | `nws23_acquiror_mtlspe` | VECTOR | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share of the target for the last financial year prior to deal announcement |
| 61 | `nws23_acquiror_niltm` | VECTOR | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income of target in last financial year prior to deal announcement |
| 62 | `nws23_acquiror_pctown` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of shares owned by acquiror after the transaction, including previously owned shares |
| 63 | `nws23_acquiror_pricebook` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Offering price in the deal divided by target's book value per share as of most current prior financials |
| 64 | `nws23_acquiror_psought` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of common, or common equivalent, shares outstanding sought by the acquiror in this transaction |
| 65 | `nws23_acquiror_qcatcp` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of shares acquired by the acquirer in the transaction (acquired shares over total outstanding) |
| 66 | `nws23_acquiror_rank_rankval` | VECTOR | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Rank value calculated by subtracting liabilities assumed from transaction value and adding target's net debt |
| 67 | `nws23_acquiror_rp` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price per common shares or partnership unit paid by the acquiror in the transaction |
| 68 | `nws23_acquiror_saleslltm` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Net sales of the target company in the last 12 months |
| 69 | `nws23_acquiror_spea` | VECTOR | 0.359 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Acquiror’s earnings per share for last fiscal year before deal announcement |
| 70 | `nws23_acquiror_value` | VECTOR | 0.359 | 其他 | 0 | — | — | — | UNUSABLE | Total value of consideration paid by the acquiror |
| 71 | `offer_premium_four_weeks_prior_2` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Premium of offer price to target closing stock price 4 weeks prior to original announcement, percentage |
| 72 | `offer_premium_one_day_prior_2` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Premium of offer price vs. target closing price 1 day before announcement (% value) |
| 73 | `offer_premium_one_week_prior_2` | VECTOR | 0.359 | 价量与波动 | 0 | — | — | — | UNUSABLE | Premium of offer price to the target's closing stock price 1 week prior to announcement, expressed as a percentage |
| 74 | `nws23_target_akw1rpa` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Acquiror stock price 1 week after announcement |
| 75 | `nws23_target_apr1daya` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Acquiror stock price one day after deal announcement |
| 76 | `nws23_target_apr1dayb` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Acquiror's stock price 1 day prior to announcement of the deal |
| 77 | `nws23_target_asalesltm` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Acquiror net sales in the last 12 months |
| 78 | `nws23_target_emu_hostvalue` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Deal value converted to million Euros |
| 79 | `nws23_target_laitni_rp` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Initial price per common shares or partnership units offered by the acquiror in the transaction |
| 80 | `nws23_target_mtlspe` | VECTOR | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share of the target in the last financial year prior to announcement |
| 81 | `nws23_target_niltm` | VECTOR | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Net income of the target in the last financial year prior to announcement |
| 82 | `nws23_target_pctown` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of shares owned after the transaction (shares acquired plus previously owned divided by total outstanding) |
| 83 | `nws23_target_pricebook` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Offering price divided by target's book value per share prior to deal announcement |
| 84 | `nws23_target_psought` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of shares outstanding sought by acquiror in the transaction |
| 85 | `nws23_target_qcatcp` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of shares acquired: shares acquired divided by total shares outstanding |
| 86 | `nws23_target_rank_rankval` | VECTOR | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Rank value: transaction value minus any liabilities assumed, plus target’s net debt |
| 87 | `nws23_target_rp` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price per common share or partnership unit paid by the acquiror in the transaction |
| 88 | `nws23_target_saleslltm` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Net sales of the target in the last 12 months |
| 89 | `nws23_target_spea` | VECTOR | 0.313 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Earnings per share of acquiror in last financial year prior to deal announcement |
| 90 | `nws23_target_value` | VECTOR | 0.313 | 其他 | 0 | — | — | — | UNUSABLE | Total value of consideration paid by the acquiror |
| 91 | `offer_premium_four_weeks_prior` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Premium of offer price to target closing stock price 4 weeks prior to the original announcement date, expressed as a percentage |
| 92 | `offer_premium_one_day_prior` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Premium of offer price to target closing stock price 1 day prior to original announcement date, as a percentage |
| 93 | `offer_premium_one_week_prior` | VECTOR | 0.313 | 价量与波动 | 0 | — | — | — | UNUSABLE | Premium of offer price to target closing stock price 1 week prior to original announcement date, as a percentage |
| 94 | `aggregate_dollar_amount` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total principal amount of the entire syndicated loan transaction, in millions of dollars |
| 95 | `euro_total_proceeds_amount` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total proceeds amount for the syndicated loan transaction, expressed in Euros |
| 96 | `euro_total_proceeds_with_overallotment_2` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total proceeds amount for the transaction, denominated in euros |
| 97 | `loan_amount_host_currency` | VECTOR | 0.211 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Amount of the loan tranche in millions of host (local) currency |
| 98 | `loan_amount_usd` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Amount of the loan tranche in millions of US dollars |
| 99 | `loan_principal_amount` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Amount of the loan tranche in millions of US dollars |
| 100 | `loan_tranche_count` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total number of tranches (distinct loan portions/facilities) in the syndicated loan package |
| 101 | `principal_amount_host_currency` | VECTOR | 0.211 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Amount of the loan tranche in millions of host (original) currency |
| 102 | `total_tranche_count` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total number of tranches (distinct parts/loans) within the loan package |
| 103 | `total_transaction_amount_usd` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total principal amount for the entire syndicated loan transaction, denominated in millions of dollars |
| 104 | `total_transaction_value` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total syndicated loan package amount in US dollars, summing all tranches across markets |
| 105 | `transaction_total_amount_usd` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Total size of the loan package for the deal, summed across all tranches, in US dollars |
| 106 | `years_to_final_maturity` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Number of years from offer date to final maturity |
| 107 | `years_to_final_maturity_2` | VECTOR | 0.211 | 其他 | 0 | — | — | — | UNUSABLE | Number of years from loan offer date to the final maturity date of the loan tranche |
| 108 | `bond_to_equity_exchange_ratio` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Ratio specifying how many shares of common stock are received for each exchangeable bond or preferred share upon conversion |
| 109 | `equity_bookrunner_proceeds_amount` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Proceeds amount per book runner in the market for the issue |
| 110 | `equity_highest_filing_price` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Highest price, in the original filing price range, at which the issuer expects securities to be offered |
| 111 | `equity_lowest_filing_price` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Lowest price, in the original filing price range, at which the issuer expects securities to be offered |
| 112 | `equity_total_proceeds_with_overallotment` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total proceeds from the issue in this market including overallotment sold |
| 113 | `equity_total_proceeds_with_overallotment_all_markets` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total proceeds from the transaction plus overallotment amount sold, in millions of dollars |
| 114 | `equity_years_to_final_maturity` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Number of years from the offer date until the final maturity date of the security |
| 115 | `global_equity_overallotment_amount` | VECTOR | 0.204 | 盈利与财务 | 0 | — | — | — | UNUSABLE | Total overallotment amount option for the equity new issue, expressed in millions of dollars |
| 116 | `global_shares_filed_initial` | VECTOR | 0.204 | 其他 | 0 | — | — | — | UNUSABLE | Total number of shares worldwide filed for the offering at the time of the original filing |
| 117 | `gross_spread_percent_of_principal` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total managers' fee as a percent of issue's domestic principal amount |
| 118 | `lockup_period_duration_days` | VECTOR | 0.204 | 其他 | 0 | — | — | — | UNUSABLE | Minimum number of days shares must be held before lock-up restrictions expire |
| 119 | `non_buyback_years_post_issue` | VECTOR | 0.204 | 其他 | 0 | — | — | — | UNUSABLE | Number of years from the offer date during which the security cannot be called or bought back by the issuer |
| 120 | `preferred_to_common_conversion_ratio` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Offer price of preferred stock divided by conversion price, representing conversion ratio |
| 121 | `primary_shares_filed_pct_of_total` | VECTOR | 0.204 | 其他 | 0 | — | — | — | UNUSABLE | Percentage of total globally filed shares that are primary shares (newly issued) at original filing |
| 122 | `security_offering_unit_price` | VECTOR | 0.204 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price per share or bond offered to the public |
| 123 | `shares_eligible_post_lockup` | VECTOR | 0.204 | 其他 | 0 | — | — | — | UNUSABLE | Number of shares eligible for sale after lockup agreement or restriction period expires |
| 124 | `shares_sold_by_existing_shareholders` | VECTOR | 0.204 | 其他 | 0 | — | — | — | UNUSABLE | Actual number of shares sold by selling shareholders or the company in the offering |
| 125 | `aggregate_transaction_proceeds` | VECTOR | 0.186 | 其他 | 0 | — | — | — | UNUSABLE | Total proceeds amount for the entire transaction, representing all tranches |
| 126 | `basis_point_spread_to_benchmark` | VECTOR | 0.186 | 价量与波动 | 0 | — | — | — | UNUSABLE | Basis point spread to benchmark; the yield difference, expressed in basis points, between the new issue and a specified benchmark instrument |
| 127 | `bookrunner_proceeds_amount` | VECTOR | 0.186 | 其他 | 0 | — | — | — | UNUSABLE | Proceeds amount of the issue in this market per book runner for this market |
| 128 | `deal_amount_in_issue_currency` | VECTOR | 0.186 | 宏观与行业 | 0 | — | — | — | UNUSABLE | Amount of the transaction/deal in the currency of issuance (host currency) |
| 129 | `euro_total_proceeds_with_overallotment` | VECTOR | 0.186 | 其他 | 0 | — | — | — | UNUSABLE | Proceeds amount plus overallotment sold in all markets, expressed in million Euros |
| 130 | `floating_rate_spread_to_index` | VECTOR | 0.186 | 价量与波动 | 0 | — | — | — | UNUSABLE | Basis point spread of issue relative to a specified floating-rate index |
| 131 | `lead_manager_fee_amount` | VECTOR | 0.186 | 价量与波动 | 0 | — | — | — | UNUSABLE | Portion of the gross spread paid specifically to the lead manager(s), expressed in dollars per share or bond |
| 132 | `security_offering_price` | VECTOR | 0.186 | 价量与波动 | 0 | — | — | — | UNUSABLE | Price per share or bond at which the security is offered to the public |
| 133 | `selling_concession_amount` | VECTOR | 0.186 | 价量与波动 | 0 | — | — | — | UNUSABLE | Portion of the gross spread allocated to the selling group, expressed in dollars per share or bond |
| 134 | `total_manager_fee_amount` | VECTOR | 0.186 | 价量与波动 | 0 | — | — | — | UNUSABLE | Total manager's fee (gross spread), expressed in dollars per share or bond |
| 135 | `total_proceeds_with_overallotment` | VECTOR | 0.186 | 其他 | 0 | — | — | — | UNUSABLE | Proceeds amount of the issue in this market plus the overallotment amount sold in this market |
| 136 | `underwriting_fee_amount` | VECTOR | 0.186 | 其他 | 0 | — | — | — | UNUSABLE | Portion of underwriting fee paid to lead/co-managers, expressed in dollars per share or bond |

## 六、本地回测证据

本地库无该数据集的回测记录。

> 说明：`backtest_results` 只收录已持久化的波次（当前 EUR 共 1157 行）；本次会话的直接派发未写库，故此处为空**不代表未做尽**，实测结论见配套战役档案。

## 七、判死记录（sealed dead_end）

无针对本数据集的 `dead_end` 记录。

