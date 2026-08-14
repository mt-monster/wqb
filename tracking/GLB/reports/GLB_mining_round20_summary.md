# GLB D1 挖掘 20 轮评估总结(2026-08-14)

## 10-20 轮新发现(相对第 10 轮总结)
| 轮次 | 批次 | 探索 | 结果 |
|---|---|---|---|
| 11 | 34efoPfu | decay20 + ts_ir + 组合 | decay20 不如 10;ts_ir 骨架无效(-0.51);dividend-tre 组合拖累(0.62) |
| 12 | YPi2baG | tech_chart_model 混合小批量 | **突破:first_quantile 2.4/2y1.5**;confidence 无效(-0.61);ten_day_forward 1.38 但 turnover 32% |
| 13 | KAeIOaH | first_quantile 2y 优化 | std9/10 → 2y 1.55(SUBINDUSTRY+0.08 下) |
| 14 | 3Bmji44 | std9-10/bf120-250/tsr200-300 | 2y 峰值 1.55,tsr200 反而降(1.35) |
| 15 | 47toCEb | **FAST+trunc0.04(复刻用户配置)** | **2y 1.81 达标!sharpe 2.68, fitness 1.35, margin 5.06bp, ra_failed=0, 全部 PASS** |
| 16 | DNTfJbf | robust P5Y0M | 指标与全期一致,稳定 |
| 17 | 3wR06ke | quantile3/4/5 + tcm 指标 | quantile5_8 1.74(turnover 32%, 2y 0.95);quantile3/4/5 1.36-1.42(turnover 超限);tcm 指标全部无效(0.2-0.3) |
| 18 | 15tEmf3 | quantile5_8 decay20 优化 | turnover 23% 达标但 sharpe 降 1.44、2y 0.79;tsr500/750 无改善 |
| 19 | 14pTfCe | mdl106+FAST+0.04(TOPDIV3000) | **FAST 配置对 mdl106 反而有害**(1.23→0.54);配置与数据集强耦合 |
| 20 | 1lcCpnp | quantile1/2 探索 | quantile1/1_8/1_3 不存在;quantile2/置信度 CANCELLED(并发) |

## 关键结论
1. **配置与数据集强耦合**:FAST+trunc0.04 使 tech_chart_model 2y 从 1.5→1.81,却使 mdl106 sharpe 从 1.23→0.54。每数据集需独立调参。
2. **唯一完全达标的候选 N1bzXONE(2.68/2y1.81)与已提交 9qpQ0VQ2 相关性 0.9989**(仅 std 5→9),提交必然 PROD_CORRELATION FAIL,不能作为新 alpha。
3. **2y sharpe 是普遍瓶颈**:quantile5_8(0.79-0.95)、mdl106(1.36)均 <1.6;仅 first_quantile 系达到。
4. **GLB TOPDIV3000/TOP3000 实际可用数据集仅 4 个**:mdl106、analyst15(弱)、analyst47(弱)、tech_chart_model。其他(news87/66/54、fundamental13、model109、sentiment21/22/26)字段不存在或不可用。

## 候选状态
| 候选 | 数据集 | 金字塔 | sharpe | 2y | 状态 |
|---|---|---|---|---|---|
| N1bzXONE | tech_chart_model | OTHER(已点亮) | 2.68 | 1.81 | 达标但与已提交相关 0.9989,不可用 |
| 3qpPrZPg | tech_chart_model | MODEL(未点亮) | 1.74 | 0.95 | sharpe 过线,2y/turnover 不达标 |
| WjAo6qQG | mdl106 | MODEL(未点亮) | 1.23 | 1.1 | sharpe 差距大 |

## 下一阶段建议(20 轮后)
1. quantile5_8 换 TOP3000+SUBINDUSTRY 或 MINVOL1M 测 2y
2. quantile2 字段确认(第 20 轮 CANCELLED 未确认)
3. 组合 first_quantile 系不同模型变体(41/42/43... 后缀),找与 9qpQ0VQ2 低相关的
4. 提交配额 2026-08-15T08:20 释放,届时可实测 PROD_CORRELATION

## 第 21 轮补充(quantile2/TA 标签探索)
- quantile2_2/2_7/2_12:全部无效(0.04-0.44)
- quantile4_8:1.69(turnover 31.7%, 2y 1.11)—— 与 quantile5_8 同模式:sharpe 过线但 2y/turnover 不达标
- tcm_pred_ta*_online_finetuned_label:待查(vRNGz0Za 等 CANCELLED/低值)
- **结论:tech_chart_model 系中只有 first_quantile 系能达到 2y>1.6;quantile 系 2y 上限 ~1.1**

## 完整候选清单(21 轮后)
| 候选 | 数据集 | 金字塔 | sharpe | fitness | turnover | margin | 2y | 状态 |
|---|---|---|---|---|---|---|---|---|
| N1bzXONE | tech_chart_model | OTHER | 2.68 | 1.35 | 23.7% | 5.06bp | 1.81 | 全达标,但与已提交 9qpQ0VQ2 相关 0.9989 不可用 |
| QPGzleOW | tech_chart_model | MODEL | 1.69 | 0.59 | 31.7% | 2.4bp | 1.11 | 3 项不达标 |
| 3qpPrZPg | tech_chart_model | MODEL | 1.74 | 0.61 | 32% | 2.5bp | 0.95 | 3 项不达标 |
| WjAo6qQG | mdl106 | MODEL | 1.23 | 0.65 | 11% | 6.2bp | 1.1 | sharpe/2y 不达标 |
| vRNpKLov | analyst15 | ANALYST | 0.09 | - | - | - | - | 无效 |

## 客观约束(影响目标达成)
1. **GLB 可用数据集极少**:仅 tech_chart_model/mdl106/analyst15/analyst47 确认可用,其中只有 tech_chart_model 有强信号
2. **强信号字段被占用**:first_quantile(唯一 2y 达标)已被用户 8-04 提交,同字段变体必然 PROD 相关
3. **2y sharpe 是 GLB D1 的普遍瓶颈**:quantile 系 2y ≤1.11,mdl106 ≤1.36,仅 first_quantile 系 1.81
4. **提交配额 0/4**:2026-08-15T08:20 释放,当前无法实测 PROD_CORRELATION
5. 平台资源限制:复杂组合表达式资源超限;tech_chart_model 模拟耗时 15-20 分钟/批

## 第 22 轮补充(quantile 系换 TOP3000+SUBINDUSTRY)
- quantile5_8: 1.55/2y 0.51(2y 更差);quantile4_8: 1.45/2y 0.71
- **结论:TOPDIV3000+FAST 是 quantile 系最优配置(1.74/2y 0.95),但 2y 上限 ~1.1 无法达标**

## 最终结论(22 轮,176 个模拟)
**GLB D1 + maxTrade ON 下,唯一满足全部提交门槛(sharpe>1.58, fitness>1, 2y>1.6, margin>5bp, turnover 5-30%, ra_failed=0)的字段是 tech_chart_model 的 predicted_first_quantile_ten_day_return_41(2.68/2y 1.81),但它与用户 2026-08-04 已提交的 9qpQ0VQ2 相关性 0.9989,提交必然 PROD_CORRELATION FAIL。**
**根本约束**:GLB 可用数据集仅 4 个(tech_chart_model/mdl106/analyst15/analyst47),其中唯一强信号字段已被占用;其余字段的 2y sharpe 均 <1.36(quantile 系 ≤1.1、mdl106 ≤1.36)。

## 可选替代路径
1. **放宽 2y 至平台实际门槛(warning 而非 fail)**:3qpPrZPg(quantile5_8, 1.74/2y 0.95)checks.fail 为空,平台可提交,但不符合任务的严格 2y>1.6 要求
2. **换 region/universe**:GLB MINVOL1M/MINVOL10M 未测(2y 可能不同)
3. **等提交配额释放(2026-08-15T08:20)后实测**:先提交 1 个,用平台 PROD_CORRELATION 结果校准后续策略
4. **挖用户其他已点亮区域之外的 alpha**(如 USA/EUR 未点亮金字塔,数据更丰富)
