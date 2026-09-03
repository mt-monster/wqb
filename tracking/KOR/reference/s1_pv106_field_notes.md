# S1 字段理解：pv106（KOR/TOP600/D1）

- 数据集类型：MATRIX，29 字段，coverage=1.0
- 主题：流动性微观结构（bid-ask spread / slippage / transaction cost）

## 字段/特征/建议

- 特征：成本类字段正偏（须 rank）；wli_* 变体高拥挤（users 36-58）全避开；冷门主候选：transaction_cost_estimate(users=0)/pv106_lastspreadbp(users=3)/korean_market_slippage(users=3)/group_order_slippage(users=2)
- 建议：流动性溢价方向（低成本=高流动性→跑赢）需实证双向；sector 组内相对化参照 wave140 正面结构；动量 5 日窗口；平滑 22 日窗口
- 风险提示：spread 族 wli_* 已饱和；bp 归一化变体优先；KOR TOP600 流动性溢价方向可能反转

## 初始信号

1. 交易成本水平（transaction_cost_estimate，users=0 冷门，低成本=流动性好→正向）
2. 点差水平（pv106_lastspreadbp，bp 归一化，窄点差=高流动性）
3. KOR 专属滑点模型（korean_market_slippage）

## 进阶信号

- 点差动量：ts_delta(rank(spreadbp), 5)
- 成本-点差背离：rank(cost) − rank(spreadbp)
- sector 组内流动性：group_rank(rank(cost), sector)
- 流动性平滑：ts_mean(rank(cost), 22)

## 预处理决策

- MATRIX 连续 → rank 包裹防偏态/厚尾
- 正值成本字段禁止裸水平直接使用，必须 rank
- sector 相对化走 group_rank/group_zscore
