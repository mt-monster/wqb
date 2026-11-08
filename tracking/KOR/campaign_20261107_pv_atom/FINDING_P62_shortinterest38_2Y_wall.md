# P62 收割：shortinterest38 全族卡 2Y（2026-11-07）

派发 10 条（KOR/TOP600/D1 · REVERSION_AND_MOMENTUM · decay 4 · trunc 0.08 · nanHandling OFF），complete 10 / error 0。

| alpha | 表达式（简） | S | F | TO | 2Y | raF | 唯一失败项 |
|---|---|---:|---:|---:|---:|---:|---|
| Vkxeoz88 | sell/buy 22d 求和比 · industry | **2.04** | **1.84** | 0.109 | **1.04** | 1 | LOW_2Y_SHARPE |
| 6XdNb0zp | sell/buy 22d 均值比 · sector | 1.92 | 1.76 | 0.104 | 0.96 | 1 | LOW_2Y_SHARPE |
| LLM3xznv | sell/buy 22d 求和比 · sector | 1.89 | 1.73 | 0.106 | 0.84 | 1 | LOW_2Y_SHARPE |
| 78LlVmd8 | −净买入股数 22d 均值 | 1.78 | 1.59 | 0.105 | 0.26 | 1 | LOW_2Y_SHARPE |
| JjerLzde | sell/buy 22d · subindustry | 1.74 | 1.40 | 0.107 | 0.82 | 1 | LOW_2Y_SHARPE |
| N1N8ozAL | sell/buy 数量比（无平滑） | 1.55 | 0.65 | 0.411 | **1.95** | 3 | S / F / CONCENTRATED_WEIGHT |
| N1N8oznp | sell/buy 金额比（无平滑） | 1.52 | 0.64 | 0.410 | **1.98** | 3 | S / F / CONCENTRATED_WEIGHT |
| qMLVZGAK | 卖/(买+卖) 归一 | 1.52 | 0.64 | 0.410 | 1.98 | 3 | S / F / CONCENTRATED_WEIGHT |
| j2YOmJ1j | −净买入金额 22d 均值 | 1.53 | 1.29 | 0.107 | 0.14 | 2 | S / LOW_2Y |
| O0Agvzoq | sell/buy 66d 求和比 | 1.49 | 1.21 | 0.068 | 0.83 | 2 | S / LOW_2Y |

## 结论：结构性互斥曲线，不是调参能解决

按平滑强度排序，S/F 与 2Y 严格反向：

- 无平滑（TO 0.41）：2Y 1.95–1.98 过线，但 S 1.52–1.55、F 0.64–0.65 双卡。
- 22d 平滑（TO 0.105）：S 1.74–2.04、F 1.40–1.84 过线，但 2Y 0.14–1.04 全卡。
- 22d→66d 平滑加剧：S 掉到 1.49、2Y 0.83 ⇒ 平滑不是单调改善。

⇒ 该族不存在同时满足 S≥1.58 ∧ F≥1.0 ∧ 2Y≥1.58 的窗口。
与既有记忆「平滑算子压死 2Y」第三次独立复现（ts_mean / ts_sum / ts_target_tvr_decay 在 KOR 的共性副作用）。

## 判定

**shortinterest38 判死（容量 0）**。

## 副产品

N1N8oznp 与 qMLVZGAK（卖/(买+卖) 归一）读数逐位相同（S1.52 / F0.64 / TO0.4104 / 2Y1.98）
⇒ 归一化改写在比值型信号上完全等价，后续不必再测同分母归一这类换写法。