# Wave BE9 备选设计 — 臂1（xAvKY0Ob S1.49）的 S/sub 双缺口修法

> 现状：S 1.49（差 0.09）/ F 1.05 ✅ / 2Y 2.14 ✅ / sub 0.58（差 0.13）/ TO 0.142 ✅
> 两条缺口都很小，但需要同时补。

## 方向 A：设置维度（此前从未在组合上试过）

| # | 手段 | 预期 | 风险 |
|---|---|---|---|
| A1 | decay 4 → 8 | 降换手、提 margin、可能提 S | 可能降 S（平滑过度） |
| A2 | decay 4 → 12 | 同上更强 | 同上 |
| A3 | neutralization SUBINDUSTRY → SECTOR | **可能直接改善 sub**（减少子宇宙内的中性化约束） | 可能降 S |
| A4 | neutralization → INDUSTRY | 同上 | 同上 |

**A3/A4 是关键**：sub_universe_sharpe 衡量子宇宙内的表现；中性化设成比分组轴更粗的层级（sector/industry），主组合在更大池内中性化，子宇宙内的信号保留度更高。

## 方向 B：字段替换

| # | 手段 | 依据 |
|---|---|---|
| B1 | 内部人腿 `insd1_holdings` → `insd1_tradesignificance` | 显著度是信息含量维度（I4 单体 S0.01 但 2Y1.25） |
| B2 | 内部人腿 window 252 → 504 | BE8 已含此臂 |
| B3 | 借券腿 264 → 220 / 308 | 264 是峰值，邻域可能存在更优点 |

## 方向 C：结构

| # | 手段 | 依据 |
|---|---|---|
| C1 | 组合层 `group_rank(add(...))` → `group_zscore(add(...))` | BE8 已含 |
| C2 | 两腿先各自 group_rank，再用 `vector_neut` 正交 | 1YWqzPGQ 的 B3 结构曾有效 |

## 优先级

1. **A3/A4（中性化换粗）** —— 最直接对准 sub 缺口，且是全新维度。
2. **A1/A2（decay）** —— 低风险微调。
3. B3（窗口邻域）—— 264 是峰值，两侧可能更好。

## 派发方式

中性化是 wave 级设置（每次 create_multi_simulation 一套），所以 A3/A4 需要**拆成两个独立 multisim**。
decay 同理。
⇒ 计划：
- M1: [臂1 原式, 变体1, 变体2] @ SECTOR 中性化 / decay 4
- M2: [臂1 原式, 变体1] @ INDUSTRY 中性化 / decay 4
- M3: [臂1 原式, 变体1] @ SUBINDUSTRY / decay 8