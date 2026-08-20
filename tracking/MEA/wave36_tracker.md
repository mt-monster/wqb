# MEA Wave 36 挖掘追踪

## 战役配置
- **区域**: MEA
- **宇宙**: TOP400
- **延迟**: D1 (MEA 仅支持 D1)
- **中性化**: SECTOR
- **Max Trade**: ON
- **类型**: REGULAR

## 修复说明
Wave 35 跳过 S1（数据集审计）+ S2-D（多样性榨取）+ S2（makeSomeGem），直接手写模板导致：
1. analyst7 表达式使用 VECTOR 字段但未用 `vec_*` 包裹
2. 无字段白名单校验，gate.py 无法拦截
3. 无多样性审计，表达式风格单一

Wave 36 修复：
1. ✅ S1: scan_fields → 字段写库（fundamental72 408 + analyst7 715）
2. ✅ S2-D: diversity_extract.py → 多样性潜力入库（fnd72 score=0.625, analyst7 score=0.565）
3. ✅ S2: 基于 S1+S2-D 构建 16 个有经济学意义的表达式
4. ✅ S2': 设置展开 + 数据库承接（waves/expressions 表）
5. ✅ Gate: 5 闸预检全过（fnd72 9/9 + analyst7 7/7）

## 数据集策略
1. **fundamental72** (主攻): 408 VECTOR 字段，未点亮金字塔（fundamental=0），pyramid=1.5x
2. **analyst7** (辅助): 715 字段（707 VECTOR + 8 MATRIX），未点亮金字塔（analyst=1），pyramid=1.4x

## 已提交回测 (Wave 36)

### Batch 1: fundamental72 (8 alphas)
**Multisim ID**: `4DhHKs42p4Ubb5kr7eBRv5K`

| ID | 表达式 | 类别 |
|---|---|---|
| w36_01 | `rank(ts_rank(vec_avg(fnd72_pit_or_is_q_is_eps), 126))` | EPS_momentum |
| w36_02 | `rank(ts_delta(vec_avg(fnd72_pit_or_is_q_is_eps), 66))` | EPS_growth |
| w36_03 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_is_q_is_oper_inc), vec_avg(fnd72_pit_or_is_q_sales_rev_turn)), 252))` | Profitability |
| w36_04 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper), vec_avg(fnd72_pit_or_is_q_earn_for_common)), 252))` | CashFlow_quality |
| w36_05 | `rank(ts_zscore(divide(subtract(vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper), vec_avg(fnd72_pit_or_cf_q_cf_cap_expend_prpty_add)), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252))` | FCF_yield |
| w36_06 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_is_q_earn_for_common), add(vec_avg(fnd72_pit_or_bs_q_bs_sh_cap_and_apic), vec_avg(fnd72_pit_or_bs_q_bs_retain_earn))), 252))` | ROE |
| w36_07 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_bs_q_bs_lt_borrow), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252)) * -1` | Leverage_low |
| w36_08 | `rank(ts_zscore(divide(subtract(vec_avg(fnd72_pit_or_is_q_earn_for_common), vec_avg(fnd72_pit_or_cf_q_cf_cash_from_oper)), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252)) * -1` | Accruals_low |

### Batch 2: fundamental72 + analyst7 (8 alphas)
**Multisim ID**: `XDoTJ9hE5h89xqIPEoxkVV`

| ID | 表达式 | 类别 |
|---|---|---|
| w36_09 | `rank(ts_zscore(divide(vec_avg(fnd72_pit_or_bs_q_bs_cash_near_cash_item), vec_avg(fnd72_pit_or_bs_q_bs_tot_asset)), 252))` | Cash_strength |
| w36_10 | `rank(ts_zscore(vec_avg(analyst_eps_upward_revisions_4weeks), 60))` | Analyst_EPS_rev_up |
| w36_11 | `rank(ts_zscore(vec_avg(analyst_eps_downward_revisions_last_four_weeks_count), 60)) * -1` | Analyst_EPS_rev_down |
| w36_12 | `rank(ts_zscore(subtract(vec_avg(analyst_net_income_upward_revisions_4_weeks_count), vec_avg(analyst_net_income_downward_revision_count_4wks)), 60))` | Analyst_NI_rev |
| w36_13 | `rank(ts_zscore(subtract(vec_avg(analyst_num_sales_estimates_raised_last_4_weeks), vec_avg(analyst_lowered_revenue_estimates_count_4wks)), 60))` | Analyst_sales_rev |
| w36_14 | `rank(ts_zscore(divide(analyst_price_target_mean, close), 60))` | Analyst_PT_upside |
| w36_15 | `rank(ts_delta(analyst_price_target_mean, 20))` | Analyst_PT_momentum |
| w36_16 | `rank(ts_zscore(divide(subtract(analyst_price_target_high, analyst_price_target_low), analyst_price_target_mean), 60)) * -1` | Analyst_PT_dispersion |

## 筛选条件
- sharpe > 1.58
- fitness > 1
- 2ysharpe > 1.6
- margin > 5bp
- turnover 5%-30%
- risk neutralization: sharpe>1, fitness>0.7, margin>5bp, ra_failed_count=0

## 目标
找到 10 个满足提交要求、彼此相关性 < 0.5、策略风格完全不同的 REGULAR alpha

## 数据库承接
- waves 表: wave_number=36, status=running, expression_count=16
- expressions 表: 16 条记录, status=pending
- fields 表: fundamental72 408 + analyst7 715 字段
- diversity_potential 表: fundamental72(0.625) + analyst7(0.565)
- campaign_state 表: current_wave=36, target_count=10

## 当前状态
- ✅ S1: 字段扫描 + 数据库写入
- ✅ S2-D: 多样性榨取 + 数据库写入
- ✅ S2: 表达式生成（基于 S1+S2-D）
- ✅ S2': 设置展开 + 数据库写入
- ✅ Gate: 5 闸预检全过
- ✅ S3: 2 批×8 已提交（multisim ID 已记录）
- ⏳ 等待平台回测完成

## 下一步
1. 轮询回测结果
2. 筛选达标 alpha（廉价闸）
3. 进行 robust test（不同 universe/neutralization）
4. 进行过拟合测试（2y sharpe）
5. 计算 alpha 间相关性矩阵
6. 选择 10 个相关性 < 0.5 的 alpha
7. 设置 alpha 属性并提交
