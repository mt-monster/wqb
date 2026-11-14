# INSIDERS 深挖 · Step 1 结果（BE113 已收 / BE114 整批 FAIL 待隔离）

## BE113 insiders1 未测机制（4wwcACdf64HIaDQdQKx88Z3，10 臂 0 错误）

| # | 臂 | 构造 | S | F | 2Y | TO | lc/sc | 归因 |
|---|---|---|---:|---:|---:|---:|---|---|
| 1 | WjlM6X8Z | **真实仓位占比** Σ66 shares/(H+shares) | **0.85** | 0.59 | 0.94 | 3.6% | **96/125** | 与旧 conviction 同强但**持仓更健康**（旧 81/133）|
| 2 | oma7Mzel | valueeur/adv20 Σ66 | 0.69 | 0.40 | 0.66 | 4.1% | 127/145 | 规模中性化价值流弱于仓位口径 |
| 3 | 0mPq0QW1 | sig==3 门控 × 仓位占比 | 0.33 | 0.14 | **1.34** | 4.0% | 64/122 | 硬门控杀 S 但 2Y 最高——**高重要性交易是近端信号** |
| 4 | aka6qPJW | ts_rank(H,252) | 0.73 | 0.30 | 0.05 | **59.4%** | 18/67 | ❌ 空心（TO 60%）|
| 5 | vRA83z0G | ts_zscore(H,252) | 0.86 | 0.39 | 0.16 | **58.7%** | 17/64 | ❌ 空心 |
| 6 | WjlM6XKk | Δ66 平滑 · **subindustry 轴** | 0.86 | 0.61 | 0.38 | 6.1% | 58/135 | 轴下沉不如 sector |
| 7 | **pwamAzQ6** | **decay22(Δ66 平滑)** | **0.94** | **0.74** | 0.81 | 6.1% | 63/124 | F 0.74 优于原臂 0.88→0.74? 持平；S 略降 |
| 8 | zqdZ1oXd | ts_rank(price,66) | 0.93 | 0.36 | −0.09 | **62.1%** | 23/83 | ❌ 空心（价格分位无稳定持仓）|
| 9 | QP0MLlmw | tail 去并列 on 仓位占比 | 0.36 | 0.20 | 0.35 | 14.1% | 25/86 | ❌ tail 反噬（sub −0.30）|
| 10 | **MP6Oo8l8** | Δ66 平滑 · **market 轴** | **1.04** | 0.86 | 0.89 | 6.2% | 66/127 | 与 sector 轴 1.06 等价 |

**归因结论**：
1. **持仓水平类时序化（ts_rank/ts_zscore）在稀疏事件字段上必然空心**（TO 58-62%、lc 17-18）——与「先聚合再差分」纪律一致：水平分位放大了申报日跳变。
2. **分组轴不敏感**（sector 1.06 / market 1.04 / subindustry 0.86）⇒ 该族信号是**个股级**，行业中性化只贡献轻微。
3. **decay22 平滑不增益**（0.94 < 1.06）⇒ 换手已低（6%），无需再平滑。
4. **真实仓位占比（0.85，lc 96/125）** 是广度最好的腿，可作组合第二腿（与 Δ66 的 66/127 互补）。
5. **sig==3 门控的 2Y 1.34** 提示：高重要性交易子集是「近端强」信号，可与 Δ66 组合。

## BE114 insider_agg_matrix（4ggMhRamn4Dt9gqT765ypm2，10 臂全 FAIL）

**根因判定**：BE114 引入 4 个从未跑过的字段（top_significant_value_1 / directional_significant_value_1 / directional_indicator_2 / top_directional_significant_value_1），触发整批连坐（batch-kill）。BE104 用过的字段（significant_value_1-4 / total_* / avg_* / directional_indicator）全部正常。
**下一步**：4 臂探针单独验证这 4 个字段是否平台可访问；BE114b 用已验证字段重建。

## 下一步（Step 2）

1. **BE115**：4 字段可访问性探针（top_significant_value_1 / directional_significant_value_1 / directional_indicator_2 / top_directional_significant_value_1）
2. **BE116**：insiders1 Δ66 腿 **nan OFF** 设置档（该族 nan 方向从未测；pv20×insd 族 nan OFF 崩到 0.16，但 analyst 族 nan OFF 是 2.02——必须实测）
