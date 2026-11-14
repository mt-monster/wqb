# ★判死：insiders 数据集只有 holdings 存量维度有效（BE148 全灭）

日期：2026-11-12
multisim `NIMO5bwg5hu9I117IrN1wEi`（10 臂，非 holdings 核心 + analyst 稳定腿）

## 实测：10 臂全灭（全部 fail=3）

| 臂 | insiders 腿 | alpha | S | F | 2Y | sub | fail |
|---|---|---|---:|---:|---:|---:|---:|
| V2 交易占比 | `insd1_shares/insd1_holdings` | Jj8qPL8j | **1.29** | 0.93 | 0.43 | 1.25 | 3 |
| V9 显著性+占比 | `tradesignif` + 占比 | blaX83JR | 1.21 | 0.82 | 0.93 | 0.91 | 3 |
| V10 显著加权+信噪 | `valueeur×signif` + ts_ir | d5apKwYv | 1.21 | 0.82 | 0.68 | 0.59 | 3 |
| V8 金额+占比 | `valueeur` + 占比 | Jj8qPLom | 1.19 | 0.81 | 0.50 | 0.60 | 3 |
| V5 金额信噪比 | `ts_ir(valueeur)` | leadMZgO | 1.14 | 0.74 | 0.41 | 1.07 | 3 |
| V6 交易价 | `insd1_price` | xAvq1alb | 1.13 | 0.78 | 0.91 | 0.74 | 3 |
| V1 金额水平 | `valueeur` 水平 | RReMALEb | 1.06 | 0.69 | 0.14 | 0.53 | 3 |
| V4 显著加权额 | `valueeur×signif` | 1YWej5WW | 1.06 | 0.69 | 0.21 | 0.56 | 3 |
| V7 金额+显著 | 双流量腿 | 9qlYEQGe | 0.98 | 0.59 | 0.68 | 0.42 | 4 |
| V3 显著度 | `tradesignificance` 水平 | qM78EZ7P | 0.88 | 0.55 | 0.46 | 0.90 | 3 |

## 判死结论（带覆盖证书）

**insiders 数据集的两个可用字段族中，只有「持仓存量（holdings）」有 alpha 信息。**

| 维度 | 字段 | 结论 | 证据 |
|---|---|---|---|
| **持仓存量** | `insd1_holdings` | ✅ **唯一有 alpha** | S7/S3 核心 S 1.54-2.36；已交付 qM7KxkQV 也用 `ts_rank(insd1_holdings,252)` |
| 交易金额（流量） | `insd1_valueeur` / `insd1_value` | ❌ 死 | V1 1.06 / V4 1.06 / V5 1.14 |
| 交易股数占比 | `insd1_shares/insd1_holdings` | ❌ 死 | V2 1.29（最好也只 fail=3）|
| 显著度 | `insd1_tradesignificance` | ❌ 死 | V3 0.88 / 组合 V9 1.21 |
| 交易价 | `insd1_price` | ❌ 死 | V6 1.13 |
| 集中度 | `significant_value_1-4`（HHI）| ✅ 有效但**只作 C 腿** | C 单腿 0.83，挂 S7 上贡献 +0.3 |

**机理**：内部人交易的 alpha 来自**知情者持仓的持续性变化**（存量的一阶变化 Δ + 信噪比 ts_ir），
而不是**单笔交易的规模/显著性**（流量）。后者在 DEU TOP500 上噪声太大（insiders1 cov 仅 53%，单笔事件稀疏）。

这与 CMP 2012 的理论一致：内部人信号需要**聚合到持仓层面**才有横截面区分度；单笔交易的方向/规模不可靠。

## 覆盖证书

| 维度 | 已覆盖 |
|---|---|
| 字段 | insiders1 全 8 字段（holdings/shares/value/valueeur/price/tradesignificance/gvkey/currency）+ insider_agg_matrix 30 个可访问字段 |
| 矩 | 水平、Δ66、ts_ir、ts_mean、ts_sum、ts_rank252、占比、显著加权 |
| 骨架 | 单腿、双腿 add、乘性门控、HHI 比值、cap 桶分档、双搭档叠加 |
| 分组轴 | sector、market、subindustry、bucket(rank(cap)) |
| 非线性 | signed_power(1.0/1.2/1.3/1.4/1.6)、winsorize、tail、trade_when、hump |
| 配置 | SUBINDUSTRY / MARKET / CROWDING / FAST；decay 0/1/2/4；nan ON/OFF；trunc 0.08 |
| 窗口 | 22 / 44 / 66 / 88 / 110 / 132 / 176 / 252 / 504 |

⇒ **无空格**，判死成立（holdings 之外的维度）。

## 对 20 颗目标的影响

insiders 数据集的独立可交付上限已探明：
- **S7/S3 核心 × 搭档族**：最多 3-4 颗独立件（已取 3 颗：npa9PKWw / vRA82ogA / XgaGb3J1，另 KPg3NZX8）
- **非 holdings 维度**：0 颗

⇒ 要补足剩余缺口，**必须转向 DEU 其他数据集**（用户的「锁 insiders」已触及该数据集的结构上限）。
