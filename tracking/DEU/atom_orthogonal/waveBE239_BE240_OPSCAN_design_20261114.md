# fnd45 全算子场景扫描设计（BE239/BE240，2026-11-14）

> 用户指令：「根据模板组 alpha 的时候，一定要记住，先把平台允许我用的所有算子场景吃透，都要深度尝试并对结果归因分析和对照分析」。
> 基线 = A1xdpqAW（fnd45 QA 情绪 杠杆A w378，S 0.96 / 2Y 1.73 / sub 0.72 / **prod 0.4527 过**）——当前唯一 prod 干净的核心。

## 一、平台 REGULAR 可用算子盘点（get_operators 103 个，REGULAR scope 剔除 COMBO/SELECTION 专用后约 84 个）

对照 DEU 战役已验证结论（references/_operator-inventory.md 68 用/16 未用 + 本轮新证），按「对 fnd45 QA 情绪信号的应用场景」分类：

### 已吃透（本轮已测有归因）
- group_rank / group_zscore / group_neutralize / rank / zscore / ts_backfill / ts_mean / ts_delta / ts_zscore / signed_power / winsorize / add / multiply / subtract / ts_sum / trade_when / vec_avg（news17/18 用）/ industry/sector/subindustry 三轴实测
### 本轮要深度尝试的未测场景（按机制分组，每臂带对照）

| # | 算子 | 场景设计 | 假设 |
|---|---|---|---|
| 1 | **ts_decay_linear** | 线性衰减窗 63/126 替代 ts_mean 平滑（近端权重高——电话会时效性先验） | 衰减均值优于等权均值（rsk68 weight_edadv 同构） |
| 2 | **ts_ir** | `ts_ir(bf(qa,378), 252)` 信息比率化（累加÷同窗波动） | risk72 死档证 IR 化是弱信号放大器（+0.40→+0.76） |
| 3 | **ts_regression** | qa 对 pr 回归残差（rettype=0 残差）：剔除台面话成分的真话残差 | 巴西论文 tone-gap 的回归版 |
| 4 | **ts_corr** | `ts_corr(qa, pr, 252)` 两段情绪一致性（低相关=分歧大→负） | SSRN 分歧负向预测 |
| 5 | **ts_arg_max/min** | `ts_arg_max(bf(qa,378), 252)` 情绪峰值新鲜度（最近越近越有效） | 时效性机制（risk60 last>offer 同构） |
| 6 | **hump** | 基线外套 hump(0.01) 压 TO | TO 4.8% 已低，预期无效（tvr_decay 无效条件判据） |
| 7 | **ts_quantile** | `ts_quantile(qa, 378, driver="gaussian")` 高斯分位变换替代 rank | 厚尾压缩 |
| 8 | **quantile** | 截面 `quantile(qa, driver="gaussian", sigma=1.0)` | 同上截面版 |
| 9 | **ts_scale** | `ts_scale(bf(qa,378), 252)` 自身历史 0-1 位置 | 52 周位置（BE176 conviction 同构） |
| 10 | **normalize** | 截面去市场均值 | 简单对照 |
| 11 | **vector_neut** | `vector_neut(qa信号, rank(fnd45_mktcap))` 规模正交 | mktcap 剥离（cov 0.32 窄宇宙的宽度补偿） |
| 12 | **group_backfill** | `group_backfill(qa, subindustry, 66)` 组内回填替代 ts_backfill | CW 手册双解药之一 |
| 13 | **last_diff_value / days_from_last_change** | 电话会间隔天数（事件节律） | 财报节奏异常检测 |
| 14 | **ts_av_diff** | `ts_av_diff(bf(qa,378), 252)` 偏离自身均值 | 简写对照（= 组内 zscore 时序版） |
| 15 | **kth_element** | k=2 具名（第二近值）| 边界用法验证（DEU 教训：k 必须具名） |
| 16 | **if_else / tail** | `tail(基线, lower=-0.5, upper=0.5, newval=0)` 中性带压缩 | 双向带通（BE80 冠军语义） |
| 17 | **ts_covariance / ts_std_dev / ts_kurtosis** | 情绪波动/峰度二阶矩 | sentiment27 判词：二阶矩>一阶矩 |
| 18 | **ts_product / ts_returns** | 情绪几何累积/变化率 | 低优先 |
| 19 | **log / sqrt / power** | 非线性族 | signed_power 已最优，预期无增益 |
| 20 | **scale / group_scale / group_count / group_sum / group_mean / group_std_dev / densify / pasteurize** | 输出整形族 | 权重分布修正，不改变排序——低优先对照 |

## 二、派发计划

两波并发（≤10 臂/波）：
- **BE239**（时序变换族）：1/2/5/7/9/14/16/17（含对照基线复刻）
- **BE240**（截面/组/结构族）：3/4/11/12/13/8/10 + 基线变体
- 设置：DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nan ON/maxTrade OFF
- 判读：每臂与基线（S 0.96/2Y 1.73/sub 0.72）逐项对照归因，正增益者进入组合池，负增益者记归因入档

## 三、预检纪律
- fnd45 全 MATRIX 免 vec_
- `fnd45_mktcap` 价格量纲参与算术前必须 rank/group_rank 归一（本项目 4 次踩坑记录）
- 每波过 preflight（dataset_id=fundamental45）
