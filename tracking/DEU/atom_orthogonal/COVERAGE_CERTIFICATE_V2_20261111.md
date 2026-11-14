# 覆盖证书 · v2 制度产物（2026-11-11）

> 制度：判死档案必须列出（字段 × 矩 × 骨架 × 分组轴）已覆盖格与空格；**有空格 ⇒ provisional 不记死**。

## 一、institutions1（INSTITUTIONS 塔，6 臂 BE48 + 13 条历史）

| 维度 | 已覆盖 | 空格 |
|---|---|---|
| 字段 | inst1_valueeur（流量额）、inst1_holdings（存量）、inst1_shares、inst1_tradesignificance | — |
| 矩 | ts_mean66 水平、ts_rank252、ts_zscore252、Δ66 | **ts_sum66（季度）★**、Δ220、ts_mean5 |
| 骨架 | group_rank 单腿、group_rank+ts_mean、multiply 加权 | **max 归并多窗**（论坛 INS-DEU-01）、双腿 add |
| 分组轴 | industry、subindustry | **sector**、market、group_neutralize |
| 非线性 | winsorize(std2/std4)、multiply 权重 | **tail ★**、trade_when 门控、hump、bucket |
| 配置 | SUBINDUSTRY、INDUSTRY、SLOW_AND_FAST | **FAST、SECTOR、MARKET、STATISTICAL**、decay 3/5、trunc 0.06/0.10 |

⇒ **空格仍在**（tail、ts_sum、max 归并、部分中性化档）⇒ 该数据集此前判定只能是 provisional。
⇒ BE50 正在补 tail + ts_sum + 正确配方；BE51v3 也在飞。

## 二、insider_agg_matrix（INSIDERS 塔，10 臂 BE49 + 69 条历史）

| 维度 | 已覆盖 | 空格 |
|---|---|---|
| 字段 | directional_indicator、directional_indicator_2、total_buy/sell_shares、total_top_buy/sell_shares、avg_secondary_buy/sell_shares、avg_sell_shares | **significant_value_1-4、top_directional_significant_value_1-4、avg_top_buy/sell_shares、avg_secondary_top_*** |
| 矩 | ts_sum66、ts_mean22、ts_delta66、ts_zscore252、ts_rank252 | **ts_sum220、ts_mean5、Δ22** |
| 骨架 | 单腿 group_rank+winsorize、双腿 add、max 三窗归并 | **双腿 max 归并（论坛 INS-DEU-01 全型）、trade_when 门控** |
| 分组轴 | industry、subindustry、sector | **market、group_neutralize** |
| 非线性 | winsorize(std2)、multiply、divide 比值 | **tail ★**、trade_when、hump、bucket |
| 配置 | SUBINDUSTRY、INDUSTRY | **SLOW_AND_FAST、FAST、SECTOR**、decay 3/5 |

⇒ 字段族有 8 个未测（显著值族 8 枚）+ tail + 双腿 max 归并 ⇒ provisional。

## 三、结论

此前对 institutions1（0.41）与 insider_agg_matrix（0.84）的「死」判定**不成立**——
按 v2 覆盖证书，两者均有未覆盖格（尤其 tail / ts_sum / max 归并 / 中性化档），
应记为 **PROVISIONAL（弱证据）** 而非穷尽判死。BE48/BE49 的实测值只证明「已测格内弱」。

后续：BE50/BE51v3 补 tail；BE52 补待授权篮子替换面；BE53/BE54/BE55 补 option1/pattern/risk72。