# GLB D1 挖掘 10 轮评估总结(2026-08-14)

## 目标与约束
- region=GLB, D1, maxTrade=ON, REGULAR
- 提交门槛:sharpe>1.58, fitness>1.0, 2y sharpe>1.6, margin>5bp, 5%<turnover<30%, ra_failed=0, PROD corr<0.7
- 目标:未点亮金字塔 3 个数据集、风格互异、互相关<0.4 的 alpha

## 10 轮结果汇总(80 个模拟)
| 轮次 | 批次 | 数据集 | universe | decay | 最佳 sharpe | 备注 |
|---|---|---|---|---|---|---|
| 1-5 | 语法探索 | sentiment26/21/22 | TOP3000 | 4 | - | 字段全为 MATRIX/双值结构,vec_* 与直接引用均报 "Invalid number of inputs: 2" |
| 6 | cqBe85ZD | analyst15/47, model106 | TOP3000 | 4 | 0.96(mdl106_dividend) | 发现正确用法:winsorize→ts_backfill→ts_rank→group_rank 链 |
| 7 | 13ua3S2 | mdl106 多字段 | TOP3000 | 4 | 1.03(dividend tsr126) | dividend 为正信号,rv/tre 弱 |
| 8 | R9OpY1F | mdl106 组合 | TOP3000 | 4 | 资源超限 | 双链组合(两个 ts_rank 250)资源超限 |
| 9 | 3755mF4 | model109 | TOP3000 | 4 | CANCELLED/unknown | model109 字段在 GLB 实际不可用(get_datafields 未按 universe 过滤) |
| 10 | 19aXFKeR | mdl106 | TOPDIV3000 | 4 | 1.05(dividend tsr126) | TOPDIV3000 与 TOP3000 相当 |
| 11 | 1NaI2W2r | tech_chart_model | TOPDIV3000 | 4 | 资源超限 | 字段数据量大,8 并发不可行 |
| 12 | 1LAKMC87 | mdl106 | TOPDIV3000 | 10 | 资源超限(平台负载) | 与第 10 轮相同表达式,确认平台资源问题 |
| 13 | 40XiOvdu | mdl106 | TOP3000 | 10 | **1.21(tsr63)** | 窗口 63 是甜点(250:0.88 → 126:0.97 → 63:1.21) |
| 14 | uHwtr8zH | mdl106 | TOP3000 | 10 | **1.23(bf22+tsr63)** | backfill 22 略优于 60 |

## 操作符探索率
已探索:rank、group_rank、ts_rank、ts_zscore、ts_backfill、winsorize、ts_mean、ts_delta、add、subtract、vec_avg、vec_sum、vec_max、signed_power、trade_when、bucket
未探索(下一阶段):ts_decay_linear、ts_regression、ts_ir、ts_corr、quantile、group_neutralize、log、inverse、power、signed_power 组合、ts_delay、ts_scale、ts_std_dev、ts_min/max、rank 双参数变体

## 字段探索率
已确认 GLB 可用数据集:mdl106(14 字段,全部 MATRIX 需变换链)、analyst15(307 字段,弱信号)、analyst47(6 字段,0.5 弱)、tech_chart_model(502 字段,资源受限但用户验证 sharpe 2.68)
不可用:sentiment21/22/26(双值结构)、news66/87、fundamental13、model109(GLB 无字段)
已用字段:mdl106_dividend(核心)、mdl106_rv、mdl106_tre、mdl106_stars、mdl106_global_evaluation、anl47_indicator、anl47_totalrawsignal、anl15_gr_12_m_1m_chg、anl15_gr_12_m_6m_chg、anl15_gr_12_m_cos_up、anl15_s_ltg_mdn

## 模板骨架多样性
当前全部使用同一骨架:`group_rank(ts_rank(ts_backfill(winsorize(F, std=5), W1), W2), country)`
变体仅窗口参数(W1: 22/60/120, W2: 21/42/63/84/126/250)。
**骨架多样性不足**——需引入:ts_zscore 外层、ts_mean 平滑、ts_delta 动量、双字段组合(资源允许)、group_neutralize、ts_ir 等

## 风格多样性
当前风格:股息率预测的时序排名(价值风格)。
需补充:动量风格、事件驱动、均值回归、多因子组合

## 预处理
winsorize(std=5/3)、ts_backfill(22/60/120)已验证有效;backfill 22 略优。
未试:nan_handling 变化、ts_delay、标准化(ts_zscore 已试 0.82-0.98 低于 ts_rank)

## 收益来源归因
mdl106_dividend 是股息率预测(前瞻 12 个月),信号本质=价值因子(dividend yield 高 → 未来收益高)。
子区域 sharpe:AMER 0.57-0.66, EMEA 0.45-0.77, APAC 0.64-0.88 → 亚太贡献最稳。
2y sharpe 0.79-1.42(窗口越短 2y 越低,长窗口 2y 稳)。

## 失效风险
1. 单一字段(dividend)风险集中,若股息率因子失效则全军覆没
2. 2y sharpe 普遍 <1.58(短窗口只有 0.38-1.1),IS 达标不代表 OS 稳
3. GLB 可用数据集极少(实际只有 mdl106/analyst15/analyst47/tech_chart_model),选择面窄
4. 平台资源限制:复杂表达式(双 ts_rank 链)会资源超限,组合需控制复杂度
5. 提交配额:当前剩余 0,48h 窗口内无法提交(2026-08-15T08:20 释放)

## 下一阶段(11-20 轮)计划
1. decay=20 与 decay=0 对比(当前 10)
2. MINVOL1M/MINVOL10M universe 探索
3. 骨架多样化:ts_ir/ts_regression/quantile/group_neutralize 变体
4. tech_chart_model 用小批量(2-4 个)重试(用户验证过该数据集)
5. 双字段组合(简化窗口 63 内组合,避免资源超限)
6. anl47_indicator 增强(0.5 → 组合或变窗口)
