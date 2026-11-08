# EUR/risk62 暴露字段画像（EUR/D1/TOP2500）2026-11-06

> 用途：EUR/RISK 塔 2/3（差 1 颗点亮），risk62 是 233 字段 MATRIX 风险模型支持集。本文件只做字段画像，未派发。

## 三套字段族（实测 cov / aC）

| 族 | 字段 | cov | aC 区间 | 语义 |
|---|---|---:|---:|---|
| 具名暴露 | `rsk62_risk_{volatility,growth,logcap,pb,mtl,mts,qe2d,spe,logadv20}` | 0.9348 | 48–100 | 风格暴露水平（最不拥挤的一族） |
| 具名 beta 1 | `rsk62_beta1_1_100_{同上}` | 1.0 | 20–367 | 对具名因子的 beta |
| 具名 beta 2 | `rsk62_beta_1_100_{同上}+averagereturn` | 1.0 | 25–280 | 第二套 beta 估计 |
| 残差收益 | `rsk62_return` | 1.0 | 788 | **禁直接用**（等同 returns 墙） |
| 匿名载荷 | `rsk62_1_100_val1..100` + intercept + ksrs | 1.0 | 18–593 | 语义不明，不盲挖 |

## 用法与禁区
- 正确入口 = 具名暴露族的**时序变化**（`ts_delta(暴露,W)`）或**相对自身历史**（`ts_zscore`），承载 BAB(volatility)/价值(pb)/规模(logcap)/动量(mtl) 经典异象。
- 直接用暴露**水平**做信号有两重风险：①暴露是慢变量，vol 低 ⇒ 按 F = S^1.5×sqrt(vol/0.125)，vol≈2% 时需 S≥1.72 才够 F=1；②水平值在横截面上的排序接近风格因子本身，prod 相关性会高。
- `rsk62_return` / 任何 returns 型字段直接使用 = returns 墙，禁止。
- 塔混：RISK 属禁混集合**之外**，可与 NEWS/SENTIMENT/ANALYST/INSTITUTIONS 等任意集合外类别自由组合（不限量）；但与 PV/MODEL/OTHER/FUNDAMENTAL 互组受限。

## 状态
未派发。优先级低于 EUR/PV intraday_pv_feats 波（后者塔位缺口同为 1 颗，但字段拥挤度低两个数量级、且有 HKG 同数据集 S 2.4 的实测先例）。