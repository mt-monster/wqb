# 阻塞期检索台账（论坛 + 外部论文）· dl_riskfree 概率场换机制面（2026-11-07）

## 触发
激增族 14 变体 prod 全落 0.7567–0.8468 厚尾 ⇒ 按 SOP「思路阻塞查论坛+论文」补检索，
决定是否在**同一数据集**上改打未试机制面（不换数据集，符合硬约束）。

## 平台论坛（MCP search_forum_posts）
- query `machine learning probability predicted return signal` → 命中《【论文合集】量化研究推荐论文(持续更新中）》
  （109 赞，KJ42842，2024-07-15），snippet 含 *Time-Series and Cross-Sectional Stock Return
  Forecasting: New Machine Learning Methods* ⇒ ML 分布预测作 alpha 信号是平台活跃主题，方向不偏门。
- 命中《使用蒙特卡洛来实现 python alpha 代码》（5 赞）⇒ 论坛侧无直接可抄的概率场模板，
  故骨架需自建（下面 10 模板全部标「自建」）。

## 外部论文 / 文献（web_search）
- **Dispersion anomaly**（Diether/Malloy/Scherbina 系；命中 *The forecast dispersion anomaly revisited:*
  *Time-series forecast dispersion and the cross-section of stock returns*、*What Drives the Dispersion Anomaly?*）：
  预测分歧度高的股票未来收益**更低**（横截面负向）。这给「信念强度 / 分歧度」模板 T1/T3/T9 方向先验。
- *Why do forecasters disagree? Lessons from the term structure of cross-sectional dispersion* ⇒
  分歧有**期限结构**，支撑 T4（5d vs 60d 概率斜率）与 T7（跨期限共识）。
- *Machine Learning Alpha Signals* / *Can Machine Learning Predict Factor Returns?* / *Distributionally Robust
  Forecast Combinations* ⇒ 分布预测信号（非点预测）本身含可挖的截面信息，支撑 T2/T6/T8/T10。

## 结论（可复用）
1. 概率字段族的**换机制面**方向 = 分歧度 / 期限结构 / 二阶矩 / 历史分位 / 桶序数，
   与已被 prod 占据的「激增幅度 × level 门控」在持仓上正交 ⇒ 有绕墙可能。
2. 论坛无现成模板可抄，必须自建 ≥10 个结构互异模板（见 waveP1_exprs.json，全部标「自建」）。
3. 先验方向：分歧度类**取负向**（高分歧 → 低收益），故 P1 若出正向活口需复核经济含义，
   若出 |S| 达标的负向臂，按 KOR 做空约束**必须单独实测正向版**（取负非镜像）。

## 算子存在性核验（MCP get_operators，防 DEU 幽灵算子连坐）
ts_av_diff / ts_std_dev / group_zscore / group_neutralize / signed_power / ts_rank / ts_delta /
ts_mean / abs / subtract / add / group_rank —— **12/12 存在**，preflight valid=true / any_changed=false。
