# EUR pv20 同类别算子逐层梯度替换（2026-11-20）

> 用户规则澄清后的首个**逐层梯度下降**完整实践：不是扫一层就停，而是「Δ表 → 归因 → 无改善则保持 → 推进下一层 → 全层扫完才停」。
> 基线：`9qlWYAj1`（pv20 拥挤度双重中性化核，本会话 S 最高的潜力候选）
> `group_neutralize(group_rank(ts_rank(subtract(0, adj_specific_return_crowding_top400), 125), industry), country)`
> S2.05 / F0.95 / TO50.2% / 2Y1.08，TOP2500×INDUSTRY×decay4×trunc0.08×nanHandling ON。
> 破闸目标：F 0.95→1.0（差 0.05）、2Y 1.08→1.58。TO 50% 是 F 的主拖累。

## 梯度路径总览（3 层 × 32 臂）

| 层 | 替换轴 | 类别 | 条数 | 结论 |
|---|---|---|---:|---|
| L1 | 内层时序 `ts_rank` | Time Series 窗口类 | 16 | **无改善，保持 ts_rank** |
| L2 | 截面秩 `group_rank` | Group | 8 | **无改善，保持 group_rank** |
| L3 | 外层中性化 `group_neutralize` | Group | 8 | **无改善，保持 group_neutralize** |

三层全扫完，**每一层的基线算子都是该层最优** —— 表达式骨架已到算子层的局部最优，梯度下降收敛。

## L1 Δ 表（替换内层 ts_rank，16 条，前 8 名）

| 算子 | alpha | S | F | TO% | 2Y | ΔS | 类别 |
|---|---|---:|---:|---:|---:|---:|---|
| **ts_rank（基线）** | 9qlWYAj1 | **2.05** | **0.95** | 50.2 | 1.08 | — | 时序秩 |
| ts_av_diff | leaKVwJe | 2.01 | 0.70 | 88.2 | 1.23 | −0.04 | 等价族（距均值） |
| ts_zscore | 2r5m72rZ | 1.96 | 0.67 | 88.5 | 1.13 | −0.09 | 等价族（时序 z） |
| ts_quantile | xAvbxEKb | 1.89 | 0.63 | 88.9 | 1.21 | −0.16 | 等价族（时序分位） |
| ts_scale | P05gpAJL | 1.67 | 0.64 | 41.2 | 0.47 | −0.38 | 语义（时序 0-1） |
| ts_delta | VkN0pQKM | 1.65 | 0.50 | 79.0 | 1.20 | −0.40 | 语义（一阶差） |
| ts_max_diff | 9qlWw5PV | 1.43 | 0.70 | 27.4 | 1.24 | −0.62 | 语义（距峰值） |
| ts_arg_min | e7aQOMAM | 0.64 | 0.21 | 6.7 | 0.57 | −1.41 | 语义（事件时点） |
| （余 8 条 S ≤0.23） | | | | | | | |

**L1 归因**：等价族（ts_av_diff/zscore/quantile）S 聚在 1.89–2.05 验证「相关≈1」；语义族清晰分层——
「距参照物偏离」类（av_diff/max_diff/delta）保 S≥1.4，「水平/离散」类（ts_sum −0.25 / ts_mean −0.25 / ts_std_dev −0.34 / ts_kurtosis −0.58）全崩。
**与 insiders1 互为镜像**：insiders1 内核=水平（ts_sum 最优），pv20 内核=相对偏离（rank/zscore 族最优）。

## L2 Δ 表（替换 group_rank，8 条）

| 算子 | alpha | S | F | TO% | 2Y | ΔS |
|---|---|---:|---:|---:|---:|---:|
| **group_rank（基线）** | 9qlWYAj1 | **2.05** | **0.95** | 50.2 | 1.08 | — |
| group_backfill(+125d) | 1YWZdZQM | 1.97 | 0.69 | 88.0 | 1.20 | −0.08 |
| group_neutralize(嵌 industry) | O0W8Z8ad | 1.96 | 0.69 | 88.1 | 1.23 | −0.09 |
| group_scale | E5QREmJL | 1.93 | 0.66 | 88.3 | 1.21 | −0.12 |
| group_zscore | Jj8QO3Lx | 1.93 | 0.66 | 88.4 | 1.28 | −0.12 |
| group_count | Jj8QOQKm | −0.01 | — | 2.6 | −0.42 | −2.06 |
| group_sum | ZYaAnXLx | −0.13 | −0.03 | 16.4 | −0.71 | −2.18 |
| group_std_dev | vRA2lYVw | −0.47 | −0.10 | 59.7 | −0.33 | −2.52 |
| group_mean(双参) | j2a808mj | −0.50 | −0.10 | 78.2 | −1.21 | −2.55 |

**L2 归因**：保序/归一族（backfill、嵌 neutralize、scale、zscore）S 1.9+（与 group_rank 保序等价，数值路径差异）；
**聚合族全崩**——group_sum/count/std_dev/mean 把秩变成组统计量，alpha 信息在「组内相对位置」不在「组的水平」。
⚠ 有趣线索：group_zscore 2Y 1.28（基线 1.08，+0.20），2Y 上 zscore 化有正贡献，但 S −0.12 不足以换基线。

## L3 Δ 表（替换外层 group_neutralize(country)，8 条）

| 算子 | alpha | S | F | TO% | 2Y | RN |
|---|---|---:|---:|---:|---:|---:|
| **group_neutralize（基线）** | 9qlWYAj1 | **2.05** | **0.95** | 50.2 | 1.08 | 2.46 |
| group_zscore | mLa6V18K | 1.87 | 0.62 | 88.8 | 1.19 | 2.34 |
| group_rank(嵌 country) | RRe61rwz | 1.88 | 0.62 | 89.1 | 1.17 | 2.41 |
| group_backfill(+125d) | 3q0VeAON | 1.78 | 0.61 | 89.4 | **1.42** | 2.34 |
| group_scale | j2a8rxgj | 1.78 | 0.61 | 89.4 | 1.40 | 2.31 |
| group_mean(双参) | 2r5mNKoN | 0.47 | 0.10 | 82.6 | **1.59** | −0.11 |
| group_std_dev | O0W8xV9d | −0.21 | −0.03 | 53.9 | −0.13 | −0.04 |
| group_sum | MP63LZp8 | −0.29 | −0.10 | 3.8 | −0.32 | 0.04 |
| group_count | Jj8QvdJl | −0.32 | −0.12 | 1.1 | −0.49 | 0.02 |

**L3 归因**：外层保持 group_neutralize 最优；**group_backfill(country,125) 把 2Y 抬到 1.42（+0.34，全部 32 臂最高）**
——按国家组回填把「无国家数据日」造成的 2Y 弱年补平了，但 F 0.61 反而退（TO 89% 更高）。
group_mean 的 2Y 1.59 是统计假象（RN −0.11，风险拖累极大，不可用）。

## 收敛判定与破闸方向

三层扫描后**算子层收敛**：基线骨架 `group_neutralize(group_rank(ts_rank(...)))` 三层各自最优。
剩余缺口 F（−0.05）与 2Y（−0.50）**不是算子选择问题**：
- **TO 50% 是 F 的主拖累**：F=S·√(ret/max(TO,.125))，TO 降到 30% F 即可过 1.0——但 L1 已证 ts_decay_linear/hump 类平滑
  在此族是负杠杆（S 崩）；L2 的 group_backfill 88% TO 更差。**降 TO 只剩设置轴（decay 阶梯）或窗口轴（ts_rank 125→250/630）**，
  而这两条在 pv20 战役报告里已实测（decay16 S2.05/2Y1.08 即当前基线族；窗 630 S1.93）。
- **2Y 1.42 线索**（L3 backfill 变体）：值得单独追——`group_backfill(层, country, 125)` 外包装与 decay16 组合的 2Y 待验证，
  但它 TO 89% 先撞 HIGH_TURNOVER，须先解 TO。

**结论**：梯度下降在本骨架收敛于原基线；「逐层全替换」的价值不在翻新基线，而在**三层归因证明该骨架是算子层的局部最优**，
并产出一个 2Y 线索（country backfill 包装 +0.34）。后续若再攻 pv20，应从「窗口轴×backfill 包装」组合进，不再扫算子。

## 追 2Y 线索：country-backfill × 窗口 × decay 组合（2026-11-20 晚，5 臂）

L3 线索 `group_backfill(·, country, 125)` 外包装 2Y 1.08→1.42，但 TO 89% 撞 HIGH_TURNOVER。
组合矩阵：包装固定，单变量扫窗口 {125,250,630} × decay {4,16}（decay16 是 pv20 战役已证的降 TO 杠杆）。

| alpha | 窗口 | decay | S | F | TO% | 2Y | 备注 |
|---|---|---:|---:|---:|---:|---:|---|
| 3q0VeAON（L3 原臂） | 125 | 4 | 1.78 | 0.61 | 89.4 | **1.42** | 2Y 最高但 TO 89% |
| wpobaoVp | 250 | 4 | 1.79 | 0.62 | 89.5 | 1.36 | 窗口加长 2Y 略降 |
| gJaZ8aze | 630 | 4 | 1.81 | 0.63 | 89.6 | 1.40 | 窗口不敏感 |
| 6XMKpM3P | 125 | 16 | **1.93** | **0.92** | **50.6** | 1.14 | decay16 修 TO：F 0.61→0.92 |
| blaOQaV6 | 250 | 16 | 1.93 | 0.93 | 50.7 | 1.00 | F 最高但 2Y 掉到 1.00 |
| d5a1ZagJ | 630 | 16 | 1.93 | 0.92 | 50.8 | 0.94 | 同上 |

**归因：2Y 增益与 decay16 不可兼得**。decay16 把 TO 89%→50.6%、F 0.61→0.92（几乎到闸），但 2Y 从 1.42 压回 1.14；
且 decay16 下窗口越长 2Y 越差（125→1.14 / 250→1.00 / 630→0.94）。decay4 下窗口反而对 2Y 不敏感（1.36–1.42）。
**这是 pv20 族「2Y↔S/F 跷跷板」的第三次独立复现**（此前：ts_decay_linear12 F1.05 但 2Y0.66；decay16 基线族 2Y1.08）。

**结论**：该族 2Y 天花板约束确认稳固——所有「提升近端质量」（decay/平滑/降 TO）的杠杆都会吃掉 2Y，
而「提升 2Y」的杠杆（backfill 包装）都会抬高 TO 毁 F。五臂均在 REVIEW 档（无 READY），
**最优组合点 = 6XMKpM3P（窗125×decay16：S1.93/F0.92/2Y1.14/TO50.6%）**，F 差 0.08、2Y 差 0.44——
比原基线（F0.95/2Y1.08）是「F 略降换 2Y 略升」的横移，未突破。2Y 线索闭合：backfill 包装的 +0.34 在修 TO 后不保留。

## 论坛取证：2Y 无直接解法，流动性残差被双重排除（2026-11-20）

按用户纪律「每步查论坛」，针对 2Y 缺口检索 4 组关键词（2 year sharpe / regime shift / crowding / investability），扫描全库：

| 帖子 | 结论 | 适用性 |
|---|---|---|
| post 44888868944023（invest 0.7 倍线→流动性残差，S 0.99→2.17） | invest_S/S<0.70 时 vector_neut(signal, sqrt(adv20)) 是强杠杆；诊断信号 = RN≫S | **双重排除**：①最优臂 invest 比例 1.41/1.93=0.73>0.70 未卡线（帖明言"高于 0.70 不是它的问题"）；②pv20 为 PV 集，volume/close 第二腿触 PV+PV 红线 |
| post 44687266076823（Momentum Crashes 2016） | 反转族在下跌后反弹+高波动期崩；先分多空腿逐年审计再加 regime 过滤 | 可解释 2Y 弱年形态（2022 反弹年），但 regime 过滤=新信息源组合，超出本骨架；只是归因工具 |
| post 44678103399575（高 prod 处理） | 「换数据源/经济逻辑是唯一可靠修法，调窗口/权重/中性化造不出真改变」 | 与本役双收敛结论一致（侧证） |

**论坛侧证完成**：pv20 的 2Y 墙是信息源级（crowding 反转近端拥挤衰减），非实现级。三条破闸路全部排除（算子层 32 臂收敛 / 设置组合 2Y↔F 跷跷板 / 流动性残差双重不可用）。**维持 PROVISIONAL 停止投入；唯一入口 = 跨类组腿换信息源（消耗跨类配额）**。
