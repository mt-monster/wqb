# Wave BD1 — institutions4（TO 治理重开）+ stock_cluster_dl 首测（2026-11-10 19:5x）

> 触发：按 §7.6 六维闸，institutions4 属**配置层死**（TO 88.7%），必须先测替代几何才能终判；`ts_target_tvr_decay/tvr_hump` 正是换手治理标准工具。
> stock_cluster_dl 从未测；字段实测为 PCA 特征向量（MATRIX，非簇标签）⇒ 可做信号。

## 字段实况（get_datafields 实测）

**institutions4**（6 VECTOR，cov 0.3413）：current/previous market_value、current/previous shares、percent_of_portfolio、percent_of_shares_outstanding —— 标准机构持仓披露，季频慢变量。
**stock_cluster_dl**（5 MATRIX）：principal_component_features_5..9；**只有 pcf_9 cov=1.0**，5-8 覆盖 0.17-0.50 过低 ⇒ 只用 pcf_9。

## 十臂

| # | 表达式要点 | 机制 |
|---|---|---|
| D1 | percent_of_shares_outstanding delta264 x tvr_decay | 机构控盘度变化（tvr 治理） |
| D2 | current_shares delta264 x tvr_decay | 持股股数变化 |
| D3 | current_market_value vec_sum delta264 x tvr_decay | 持仓市值流 |
| D4 | percent_of_portfolio delta264 反向 x industry | 仓位占比变化（防集中） |
| D5 | percent_of_shares_outstanding 水平 132 x tvr_decay | 控盘度水平面 |
| D6 | 双窗加速度（264/132 乘积）x tvr_decay 反向 | 借券族冠军几何迁移 |
| D7 | 市值变化 − 股数变化（净额）x tvr_hump | 价格 vs 数量分解 |
| D8 | percent_of_portfolio delta132 反向 x industry | 季度级仓位变动 |
| D9 | pcf_9 zscore252 x tvr_decay | PCA 特征水平 |
| D10 | pcf_9 delta66 x tvr_decay x industry | PCA 特征变化 |

算子数：8-11；设置 DEU/TOP500/D1/decay4/SUBINDUSTRY/trunc0.08/nanON。
塔合规：INSTITUTIONS 塔 1/3（未点亮）✓；OTHER 塔 2/3（未点亮）✓。

## 出口

- institutions4 若 S≥1.2 且 TO 被 tvr_decay 压到 <0.7 ⇒ 配置层死被推翻，进破闸。
- 若仍 S<1.0 ⇒ 信号层弱，按新闸记 PROVISIONAL（此时配置层已测，死因可升级为信号层）。