# BE86 判决：PV 三字段组合族内最佳 1.14（簇轴），BE87 补课波在飞（2026-11-12）

## 一、BE86 四臂结果（sim 1b503D8Ps4xMa2VQ2to8dbg，decay2/SUBINDUSTRY/nan ON，TOP500/D1）

| id | 构造 | S | F | TO | sub | 2Y | RA fails |
|---|---|---:|---:|---:|---:|---:|---|
| pwaYovex | 动量(close,504) − 形态(wedge,252) + 量能(ts_product vol/adv20,5)，sector 内层 × factor1_group50 外层 | **1.14** | 0.59 | 0.267 | 0.58✓ | −0.39 | LOW_SHARPE/LOW_FITNESS/IS_LADDER |
| LLKVq5w2 | 同上，外层 market | 0.91 | 0.44 | 0.259 | 0.40✗ | −0.58 | +sub |
| 0mPO9j2p | tail 带通(winsorize, 0.25-0.75) 三分量 | 0.54 | 0.18 | 0.312 | 0.02✗ | 0.67 | 4 项 |
| O0WQqJXv | 动量腿换 close/vwap,252 | 0.16 | 0.02 | 0.576 | 0.11 | −1.85 | 3 项 |

结论：
1. **簇轴外层（factor1_group50）+0.23 vs market 外层**——pv30 簇标签作分组轴第 2 次有效（BE46 之后）；
2. tail 带通在本族伤害信号（tail 对 rank 型有害的第 5 次复现）；
3. 4 臂全部 REVERSION_COMPONENT warning——即使破 S 闸，平台侧仍有接受风险；
4. **2Y 全弱（−1.85 ~ +0.67）**：近两年 regime 与该结构相反，IS_LADDER 1.58 闸当前无解；
5. pwaYovex S 1.14 落协议 v2 L2 的 1.0-1.2 带 ⇒ 补定向 10 臂（BE87）。

## 二、BE87 补课波（在飞：14C7qM2a04Wkb7XILizxyG6，decay2/SUBINDUSTRY/nan ON）

| 臂 | 假设 |
|---|---|
| 1-3 | 动量窗 252 / 756 / 1008（慢动量 horizon） |
| 4 | 形态窗 504 |
| 5 | 去形态双腿（形态腿必要性检验） |
| 6-7 | 量能窗 3 / 10 |
| 8 | 簇轴内层 × market 外层（轴几何互换） |
| 9 | ts_scale 替换 ts_zscore（矩形式） |
| 10 | 动量腿翻号（方向检验） |

全部 10 臂 ≤10 算子（≤12 预算内）、预检 valid、operator_audit safe。
**收口判据：best <1.2 或较 1.14 无改善 ⇒ PV 三字段组合关闭（覆盖证书并入 TOWER_CLOSURE_MASTER），未点亮塔路径穷尽。**
