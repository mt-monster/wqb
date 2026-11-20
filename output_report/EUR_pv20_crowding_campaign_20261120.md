# EUR pv20 拥挤度族专项挖掘与归因（2026-11-20）

> 用户指令「还有哪些数据集可以跑」→ 零配额盘点 EUR 127 数据集 → 选 pv20（PV 塔 2/3，DB 0 臂，aC 3–15 极冷门）。
> 三路证据齐：官方文档（F/S/sub 公式）+ 论坛（crowding/specific-return/2Y 救援/降 TO 反例）+ 论文 24 篇/21 作者（Crowding and Factor Returns 等）。
> 全程 EUR/D1，MCP 只用 `create_multi_simulation`（用户硬约束 2026-11-20）；**未提交任何 alpha**。

## 1. 字段与机制

平台字段（search `specific_return`/`adj`，aC 0–15 极冷门）：`specific_return_eu_top400`(cov0.31) / `eu_top1200`(cov1.0) / `eu_top800`(cov0.65) / `crowding_notliquim`(cov0.83) / `crowding_top800`(cov0.65) / `crowding_top1200`(cov1.0) / `crowding_top2500`(cov1.0) / `adj_specific_return_nonliquid_eu`(cov0.90) / **`adj_specific_return_crowding_top400`(cov0.34，最优)**。

机制：拥挤子集中的特异收益短期反转——`group_rank(ts_rank(subtract(0, F), W), industry)`，decay 驱动 TO/F，窗口驱动 S/2Y，分组轴（country/exchange/market）作 2Y 救援尝试。

**前置复核**：本族 `pyramids.effective=1`（EUR/D1/PV，纯单集）；**未触发 REVERSION_COMPONENT**；逐年 2014–2023 全满仓（2022 弱年 S0.96/DD10.2%，2023 回 1.83）⇒ 满足近十年约束；**RN_sharpe 2.46 ≫ S 1.84** ⇒ 信号被风险暴露拖累（流动性残差前提成立，但 PV+PV 被组合红线禁 ⇒ 改用 PV 分组字段救 ladder）。

## 2. 回测全表（40 臂，6 批 multisim）

| 类别 | 代表 | S | F | TO | 2Y | 判定 |
|---|---|---:|---:|---:|---:|---|
| 基线（字段最优） | VkNaWMnV `adj_top400` w630 d8 | 1.84 | 0.75 | 68.1% | 1.16 | S 过 |
| **decay16 最优** | 9qlWYAj1 双重中性化(industry×country) w125 | **2.05** | **0.95** | 50.2% | 1.08 | S 过、F 差 0.05 |
| decay16 对照 | blaOXWbr w125 industry | 2.04 | 0.95 | 49.7% | 1.11 | 同上 |
| **F 双过闸** | **1YWZevJJ** `ts_decay_linear(...,12)` w125 d8 | **1.74** | **1.05** | 23.4% | **0.66** | **S/F 过、2Y 崩** |
| 平滑 6 | YPaM6ZNJ | 1.59 | 0.87 | 31.9% | 0.68 | 2Y 崩 |
| 平滑 12（原版 d8） | mLa6pOZ9 | 1.48 | 0.88 | 23.4% | 0.60 | 2Y 崩 |
| 短窗 22 | leaKeV0l | 1.32 | 0.44 | 68.1% | 0.96 | 全灭 |
| 短窗 88 | 9qlWqwRq | 1.72 | 0.68 | 67.8% | 1.24 | 2Y 最高档 |
| 窗口 250 | Jj8N6eZW | 1.82 | 0.75 | 67.9% | 1.16 | S 过 |
| 换轴 country | 9qlWYAj1 / YPaM6Wbv | 2.05 | 0.95 | 50.2% | 1.08 | 救 S 不救 2Y |
| 换轴 exchange | blaOXWbr / E5QR1rp9 | 2.04 | 0.95 | 49.7% | 1.11 | 同上 |
| tvr_decay(0.1) | LLKNQV0v | 0.39 | 0.18 | 5.1% | 0.03 | **TO 降但 S/2Y 全崩** |
| hump(0.005) | LLKZLRrn | 0.29 | 0.07 | 0.9% | 1.17 | TO 破下限、死 |
| 其他字段族（eu_* / nonliquid / top2500） | — | 1.7–1.8 | 0.6–0.7 | ~68–90% | 0.9–1.3 | 同质、无增益 |
| ts_delta5 / ts_zscore / ts_quantile | — | ≤1.0 | — | — | — | 无效 |

## 3. 归因（三条硬结论）

1. **F 与 S 线性绑定但不共时**：`F = S·√(ret/max(TO,0.125))` —— F≥1 要求 S≥√(TO/ret)：decay16 需 S≈2.10（实测 2.05 差 0.05）；decay8 平滑12 把 TO 23% 换 F1.05 但 2Y 掉到 0.66。**S/F/2Y 三闸从不同时成立**。
2. **2Y 天花板 = 1.26**（w88–125），限 1.58，且**所有改变（decay/窗口/分组轴/平滑/换字段）都只是拿 2Y 换 S/F，从不抬 2Y**——刷到 2Y≥1.58 的唯一通道（论坛帖）：跨数据集加近期强字段腿 / 找历史仅 2–5 年的数据集，本族均不可用（PV 单集红线）。
3. **降 TO 算子有反效果**：`ts_target_tvr_decay(target=0.1)` 把 TO 68%→5% 但 S 1.76→0.39；`hump(0.005)` 把 TO 压到 0.9% 且 S 0.29；只有 `decay16/24` 与 `ts_decay_linear(12)` 保住 S——与论坛「cut Sharpe faster than turnover」一致。

## 4. 判定

**pv20 拥挤度族不可交付**（2Y 天花板 1.26 < 1.58），PROVISIONAL/族级（论坛证据：反转腿有 REVERSION_COMPONENT 战略风险；prod 未测）。11 字段中只有 `adj_specific_return_crowding_top400` 值得保留作 PK 起点；其余同质/无效。
**流程合规**：MCP 仅 `create_multi_simulation`；三路证据先于回测；每条近闸候选均做归因（逐年+PnL+公式）；全部未提交。

## 5. 经验（已入册）

- 手册实践：F=S·√(ret/TO) 在「高 TO 高 ret」族上的可行域算术——F≥1 需 S≥√(TO/ret)，比固定 S≥1.66 更精确。
- tvr_decay/hump 对高 TO 排序型信号是负杠杆（S 崩快过 TO）；decay 阶梯 8→16 抬 S/F 但压 2Y。
- 论坛「分组字段救 ladder」在 EUR PV 拥挤族上无效（2Y 1.16→1.08~1.11）。
