# analyst46（TipRanks 分析师洞察）波 1 模板池 — 两读取证 + Loudis 方向先验

> 状态：设计定稿（2026-11-03 10:3x），待 oth699w1 收批腾槽后派发。纯单数据集 ANALYST 塔 ATOM（非 trio）。
> 字段：anl46_indicator(1-10 多空分) / sentiment(复合) / experts(贡献者可信度) / alphadecay(想法新鲜度)；**performancepercentile=look-ahead 禁信号**。
> ⚠️ 塔合规：全部表达式只引 anl46_* 字段——**禁用 returns/close 等 PV 内建字段**（trio×非trio 配额已满 5/5，PV+ANALYST 即违规）。

## 一、论坛三读（2026-11-03，extract_ids.py 已参数化修复）
- **《分析师建议和回报率》21 赞**（Paper 16 配方）：短期建议相对长期建议的变化（ts_av_diff）+ ts_regression(returns, rating, d) 历史预测准确度条件化 → 对高准确度股票按近期评级反转。⚠️ 离散评级换手高（1-5 级跳变大调仓）。
- **《analyst10 预期差构建》52 赞**：「同口径差一维」提取预期结构差。**避坑清单**：双版本陷阱（v1/v2 混用混入修订噪声）、已差分字段勿重复差分、先截面标准化再相减防尺度失真（group_zscore(FY2)−group_zscore(FY1)）、覆盖差异放大伪信号、CHN 八腿全灭=region 特异性强。analyst46 无 FY1/FY2 双期字段，此模板不直接套，但「先标准化再组合」与覆盖纪律适用。
- **《分析师预期 × 极端最近性反转》**：Loudis 论文配方——「刚刚创新低」时间位置反转：ts_arg_min(x, 252) 越近越新 → group_rank。⚠️ 照抄臂（唯一）。

## 二、文献方向先验（Loudis 2019 UChicago 实证）
- **偏差成分**：市场过度反应，**3-6 个月（66-126d）后反转** ⇒ 高 indicator 但不可信（experts 低）→ 反转。
- **信息成分**：反应不足，**持续漂移** ⇒ 高 indicator 且可信（experts 高）→ 动量/持有。
- **⇒ experts 字段 = 信息/偏差分离器**，本波核心机制：用 experts 条件化把 indicator 拆成两条腿。

## 三、模板清单（12 互异 · 家族 5 · 照抄臂 1 · 开放臂 ≥4）
- T1 indicator 水平 ts_mean22 正向｜T2 indicator 反向（Loudis bias 反转）｜T3 sentiment 水平｜T4 sentiment 反向。
- T5 ts_arg_min(ts_mean(indicator,22), 252) 刚刚悲观反转（**照抄臂**·recency 帖）｜T6 ts_arg_max 同构 刚刚乐观。
- T7 trade_when(experts 高>ts_quantile(·,252), indicator 正向, -1) **信息成分**（可信背书→漂移）｜T8 trade_when(experts 低, indicator 反向, -1) **偏差成分**（反转）。
- T9 trade_when(alphadecay 新鲜条件, sentiment, -1) 新鲜想法条件化（开放臂）｜T10 ts_av_diff(indicator, 22) 建议边际变化（Paper 16 算子）。
- T11 ts_av_diff(sentiment, 5) 短期情绪突变（开放臂）｜T12 group_rank(indicator 水平, country) 分组轴对照（si3 心得①）。
- 窗口白名单映射：22/66/252/504；recency 帖原 240→252、Paper16 原 120→252（非标窗口弃用）。

## 四、算子硬闸（2026-11-03 get_operators 实证在册）
ts_zscore(x,d) / ts_arg_min(x,d) / ts_arg_max(x,d) / ts_av_diff(x,d) / ts_regression(y,x,d,lag,rettype) / group_zscore(x,group) / winsorize(x,std) 全部在册 ✓。ts_arg_min 语义=最小值时间位置（距今天数，越小越新）。

## 五、覆盖闸
- 待收批后逐颗 get_alpha_yearly_stats 按「连续多年双零」口径验（覆盖口径=连续空窗才排除）。

## 六、待补
- 派发实录 + 收批归因（按模板编号）。
## 八、波 1 收批归因（12/12 全收 · 2026-11-03）

| 臂 | 面 | S | 结论 |
|---|---|---|---|
| T1/T2 | indicator 水平 ± | 0.10 / -0.10 | 对称=噪声 |
| T3/T4 | sentiment 水平 ± | 0.13 / -0.13 | 对称=噪声 |
| T5/T6 | 新近度(ts_arg_min/max) ± | 0.16 / -0.08 | 弱 |
| **T7** | **信息腿（experts 高×indicator）** | **0.11** | **Loudis 信息漂移假说未兑现** |
| **T8** | **偏差腿（experts 低×indicator 反向）** | **-0.40** | **偏差反转假说反向失效（轻微动量）** |
| T9 | alphadecay 条件化 | 0.23 | 弱 |
| T10/T11 | ts_av_diff(indicator 22 / sentiment 5) | -0.09 / -0.05 | 死 |
| T12 | indicator country 轴 | 0.08 | 死 |

**判弱封组合**：max |S|=0.40 << 1.58。Loudis (2019) 信息/偏差分离机制在 DEU/TOP500 的 anl46 字段上**整体未兑现**——indicator/sentiment/experts/alphadecay 四面全弱。analyst46 封盘不再追投。归因要点：DEU 分析师数据的 alpha 已被 anl8/anl10/anl16 等拥挤集榨干，冷集 anl46 的 insight 字段无残余信息。
