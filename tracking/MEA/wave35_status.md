# MEA Wave 35 挖掘状态报告

## 战役配置
- **区域**: MEA
- **宇宙**: TOP400
- **延迟**: D1 (MEA 仅支持 D1)
- **中性化**: SECTOR
- **Max Trade**: ON
- **类型**: REGULAR

## 数据集策略
1. **fundamental72** (主攻): 300 VECTOR 字段，未点亮金字塔
2. **analyst7** (辅助): 300 VECTOR 字段，需正交信号（已有2个 alpha prod_corr>0.8）

## 已提交回测 (Wave 35)

### Batch 1: fundamental72 (8 alphas)
**Multisim ID**: `1NvPlgd5o4vBbxqPEHkoaOx`

| ID | 表达式 | 类别 |
|---|---|---|
| w35_01 | `rank(ts_rank(vec_avg(fnd72_pit_or_is_q_is_eps), 126))` | EPS_momentum |
| w35_02 | `rank(ts_delta(vec_avg(fnd72_pit_or_is_q_is_eps), 66))` | EPS_growth |
| w35_03 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_is_q_is_oper_inc), vec_avg(fnd72_pit_or_is_q_sales_rev_turn)), 252))` | Profitability |
| w35_04 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper), vec_avg(fnd72_pit_or_is_q_earn_for_common)), 252))` | CashFlow_quality |
| w35_05 | `rank(ts_zscore(divide(subtract(vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper), vec_avg(fnd72_pit_or_cf_q_cf_cap_expend_prpty_add)), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252))` | FCF_yield |
| w35_06 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_is_q_earn_for_common), add(vec_avg(fnd72_pit_or_bs_q_bs_sh_cap_and_apic), vec_avg(fnd72_pit_or_bs_q_bs_retain_earn))), 252))` | ROE |
| w35_07 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_bs_q_bs_lt_borrow), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252)) * -1` | Leverage_low |
| w35_08 | `rank(ts_zscore(divide(subtract(vec_avg(fnd72_pit_or_is_q_earn_for_common), vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper)), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252)) * -1` | Accruals_low |

### Batch 2: analyst7 + mixed (8 alphas)
**Multisim ID**: `Zuv59emn4j5cpE1aWFxGAlO`

| ID | 表达式 | 类别 |
|---|---|---|
| w35_09 | `rank(ts_zscore(analyst_eps_upward_revisions_4weeks, 60))` | Analyst_revision_up |
| w35_10 | `rank(ts_zscore(analyst_eps_downward_revisions_last_four_weeks_count, 60)) * -1` | Analyst_revision_down |
| w35_11 | `rank(ts_delta(analyst_eps_mean, 20))` | Analyst_consensus_momentum |
| w35_12 | `rank(ts_zscore(analyst_consensus_mean_roe, 120))` | Analyst_ROE |
| w35_13 | `rank(ts_zscore(subtract(analyst_consensus_high_eps, analyst_consensus_eps_low_estimate), 60)) * -1` | Analyst_dispersion |
| w35_14 | `add(rank(ts_delta(vec_avg(fnd72_pit_or_is_q_is_eps), 66)), rank(ts_zscore(divide(vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper), vec_avg(fnd72_pit_or_is_q_earn_for_common)), 252)))` | Composite_quality |
| w35_15 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_bs_q_bs_cash_near_cash_item), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252))` | Balance_sheet_strength |
| w35_16 | `rank(ts_zscore(divide(analyst_flash_mean_eps, analyst_eps_mean), 60))` | Analyst_surprise |

## 筛选条件
- sharpe > 1.58
- fitness > 1
- 2ysharpe > 1.6
- margin > 5bp
- turnover 5%-30%
- risk neutralization: sharpe>1, fitness>0.7, margin>5bp, ra_failed_count=0

## 目标
找到 10 个满足提交要求、彼此相关性 < 0.4、策略风格完全不同的 REGULAR alpha

## 当前状态
- ✅ 已提交 16 个 alpha 回测
- ⏳ 等待平台回测完成（预计 5-10 分钟）
- ⏳ 待回测完成后进行 robust test 和过拟合测试
- ⏳ 待计算 alpha 间相关性

## 下一步
1. 轮询回测结果
2. 筛选达标 alpha
3. 进行 robust test（不同 universe/neutralization）
4. 进行过拟合测试（2y sharpe）
5. 计算 alpha 间相关性矩阵
6. 选择 10 个相关性 < 0.4 的 alpha
7. 设置 alpha 属性并提交
