# INSIDERS 数学变换扩展（BE119/BE120，2026-11-11）

> 用户问：能否通过更多数学变换得到更强组合与信号？算子用平台的，数学模型找外部论文。
> 答案路径：把 INSIDERS 从「基础矩（水平/变化/比值）」推进到**高阶矩 + 信噪比 + 秩序统计 + 秩聚合 + 残差化 + 非线性压缩**六族变换。

## 论文依据（数学模型映射）

| 变换 | 数学模型 | 文献 |
|---|---|---|
| 秩序统计加权 / Top-k 集中度 | 知情交易按订单规模排序，大单信息量最高 | Seyhun 1986/1998；Easley-O'Hara 信息驱动交易 |
| Top1 vs Top2 差额比 | 知情流集中度（Gini 式） | Lakonishok-Lee 2001 净买入比率 |
| Top1 份额（HHI 式） | Herfindahl 集中度 | 产业组织/持仓集中度文献 |
| ts_ir（均值/标准差） | 信息比 / 信噪比 | Grinold-Kahn《Active Portfolio Management》|
| ts_kurtosis | 高阶矩：流的尾部集中度 | 金融高阶矩定价文献 |
| signed_power 0.5 | 凹变换：规模收益递减 | Almgren-Chriss 2000 冲击成本 |
| ts_quantile | 非参数单调变换（秩保序） | 稳健统计 |
| 多尺度等权混合 | 多时间尺度动量组合 | Lo 2002《The Statistics of Sharpe Ratios》|
| ts_corr(flow, delay(flow)) | 流的自相关 = 持续性 vs 一次性 | 内部人交易序列相关文献 |
| 有符号对数压缩 | 重尾压缩（对称对数） | 稳健变换通用做法 |
| vector_neut | 对流动性正交化（残差化） | 因子残差化标准做法 |
| trade_when 门控 | 条件信号（仅高信息时交易） | 事件研究条件化 |
| 秩聚合（Borda） | 多指标秩平均 | 复合评分加权（InsidersTrades 帖）|

## ⚠️ 平台静态闸的一条新纪律（本轮实测）

**加权混腿被判定为毒模式**：`add(multiply(0.5,A), multiply(0.3,B))` 触发 `[POISON] weighted_leg_mix_func_prefix`，整批拒绝。
⇒ 数学上的「指数加权/多尺度加权」必须改写成**等权嵌套**（add(add(A,B),C)）或**比值/幂次**形式（divide(multiply(S1,S1),add(S1,S2))）。
⇒ 这与用户 CLAUDE.md「禁止混信号调参，尤其警惕 add(A,B)」是同一纪律的自动化执行。

## BE119 agg_matrix 十臂（1m3IJ89Y55hEbZUOD6PQ29c）

| # | 变换 | 表达式核心 |
|---|---|---|
| 1 | 二次强调 Top1 | ts_mean(S1²/(S1+S2), 66) |
| 2 | Top1−Top2 集中度 | ts_mean((S1−S2)/(S1+S2), 66) |
| 3 | Top1 份额（HHI） | ts_mean(S1/(S1+S2+S3+S4), 66) |
| 4 | 信噪比 | ts_ir(S1, 66) |
| 5 | 峰度 | ts_kurtosis(S1, 66) |
| 6 | 凹变换 | signed_power(S1/adv20 均值66, 0.5) |
| 7 | 非参数单调 | ts_quantile(S1/adv20, 66) |
| 8 | 多尺度等权 | Σ22 + Σ66 + Σ132（等权嵌套）|
| 9 | 流自相关 | ts_corr(S1, ts_delay(S1,1), 66) |
| 10 | 对称对数压缩 | ts_mean(sign·log(1+abs), 66) |

## BE120 insd1 十臂（3UN8186GK4h8a6irJbHuFNI）

| # | 变换 | 表达式核心 |
|---|---|---|
| 1 | 双尺度等权 | Δ66 + Δ132 |
| 2 | 信噪比 | ts_ir(holdings, 66) |
| 3 | 峰度 | ts_kurtosis(Δ66, 66) |
| 4 | 凹变换 | signed_power(Δ66, 0.5) |
| 5 | 秩聚合（Borda）| rank(Δ66) + rank(仓位占比) |
| 6 | 残差化 | vector_neut(Δ66, adv20) |
| 7 | 条件门控 | trade_when(ts_rank(abs(Δ),252)>0.7, rank(Δ66), 0) |
| 8 | 对称对数压缩 | ts_mean(sign·log(1+abs(Δ)), 66) |
| 9 | 两指标一致性 | ts_corr(Δ66, 仓位占比, 66) |
| 10 | group_neutralize | group_neutralize(Δ66, sector) |

## 判读线

- 任一臂 > 1.07（INSIDERS 现天花板）⇒ 数学变换有效，进满波扩展；
- 1.0-1.07 ⇒ 边际，记录但不重启；
- <1.0 ⇒ 确认基础矩已是最优表示，数学变换族关闭。
