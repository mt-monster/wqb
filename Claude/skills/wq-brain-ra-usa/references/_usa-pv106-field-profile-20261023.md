# USA / pv106（交易成本 / 市场冲击）字段画像与首波裁决

> 快照：2026-10-23（`get_field_catalog` region=USA dataset=pv106，6/6 字段实测 + 波 1 十臂）
> 状态：**停投**（不是永久判死：`seal_dead_end` 的 forum-recon 闸 fail-closed，需用户确认 waiver，故此处只记停投）
> 上游选集：与 `risk60` 同批（fundamental 塔耗尽后的未点亮塔补挖），见 `_usa-risk60-field-profile-20261023.md` §1

## 1. 身份与拥挤度

| 项 | 值 |
|---|---|
| 数据集 | `pv106`，平台类别 **PV**（塔未点亮，×1.1） |
| 字段数 | 6（全部 MATRIX） |
| 覆盖 | 1.000 |
| 数据集级 aC | **104**（极低）；userCount 低 |
| USA 历史表达式 | **0**（`alphas.expression LIKE '%transaction_cost%'` = 0）；跨区 RA 干净（IND 2 条） |

六个字段（全部覆盖 1.000，MATRIX）：

| 字段 | 语义 | 波 1 实测 |
|---|---|---|
| `bid_ask_price_gap` | 买卖价差估计 | **未测**（波 1 漏臂，见 §4） |
| `transaction_cost_estimate` | 综合交易成本估计 | **零持仓**（空列） |
| `transaction_cost_median` | 交易成本中位数 | S −0.38 |
| `transaction_cost_maximum` | 交易成本最大值 | S −0.30 |
| `transaction_cost_percentile_10` | 成本 10 分位 | 仅作分子/分母 |
| `transaction_cost_percentile_25` | 成本 25 分位 | 仅作分子/分母 |

## 2. 机制与方向假设（发批前）

- **M1 非流动性溢价**（Amihud 2002）：交易成本高 = 流动性差 ⇒ 应有正溢价 ⇒ 做多高成本。
- **M2 成本尾部风险**：`max − p10` 的离散度 = 尾部冲击 ⇒ 高离散度应折价。
- **M3 成本结构形状**：`p25/median`、`p10/max` 比值衡量成本分布陡峭度。

## 3. 波 1 十臂结果（`1shYDqfBo4Ch90916n4uaixu`，wave=`pv106_w1`）

设置：USA/TOP3000/D1/SUBINDUSTRY/decay 8/trunc 0.08/nanHandling ON/2014–2023。

| 臂 | S | F | TO | 2Y | SUB | 备注 |
|---|---:|---:|---:|---:|---:|---|
| `N1eJxYJo` 成本水平 | 0 | — | 0 | — | — | **零持仓**（`LOW_TURNOVER`+CW） |
| `e76VkXGd` 成本水平@subindustry | 0 | — | 0 | — | — | 零持仓 |
| `GrgK1ZzO` 63 日均值 | 0 | — | 0 | — | — | 零持仓 |
| `ZYmdPOz3` 自有史 zscore | 0 | — | 0 | — | — | 零持仓 |
| `d5K3kN3J` 22 日变化 | 0 | — | 0 | — | — | 零持仓 |
| `akVQj5QO` 中位数 | −0.38 | −0.18 | 3.8% | −0.32 | −0.09 | |
| `vROpwWpr` 最大值 | −0.30 | −0.12 | 3.5% | −0.25 | −0.07 | |
| `xA12OJ2l` `max − p10` | −0.18 | −0.06 | 3.6% | 0.03 | 0.05 | |
| `A1QrjozE` `p25/median` | −0.40 | −0.20 | 6.2% | −0.17 | −0.23 | |
| `ZYmdPOM3` `p10/max` | −0.66 | −0.53 | 11.2% | −0.73 | −0.14 | 本波最差 |

**0/10 过硬闸**；`wave_results` 暂定 verdict=FAIL。

## 4. 归因与裁决

1. **`transaction_cost_estimate` 在 TOP3000/D1 是空列**：五臂 TO=0、`longCount=shortCount=0`、
   直接 `CONCENTRATED_WEIGHT`。⇒ 该字段不可用，**不是构造问题**；后续任何引用它的表达式都会零持仓。
2. **水平项方向与理论相反且稳定为负**：`median` −0.38、`maximum` −0.30
   ⇒ 2014–2023 美股 TOP3000 里「交易成本高」的股票**跑输**，非流动性溢价在本样本中不存在
   （成本高的多半是高波动/高换手/被散户拥挤的票）。按方向纪律，**不能反号当信号用**
   （反号 = 赌高成本跑赢，无机制支撑）。
3. **形状项更差**：`p25/median` −0.40、`p10/max` −0.66 ⇒ 成本分布越陡越差，与 M3 假设反向。
4. **`bid_ask_price_gap` 是唯一未测字段**（波 1 漏臂）。它是本数据集里最接近「瞬时价差」的字段，
   与已证伪的「成本水平」机制不同（价差是微观结构，不是成本负担）。
   **但不为此单独开波**：本数据集 aC 104 极低、6 字段里 5 个已给出负面证据，
   按「数据集级判断优先于单字段补测」纪律停投；若日后需要低相关补充，这一臂是唯一入口。

**裁决：停投**。可复用结论：
- **VECTOR/空列静默零持仓是多字段数据集的常见陷阱**：先看 long/short 计数，再看 Sharpe。
  零持仓臂的「S=0」不是「信号为零」，是「没有建仓」。
- 「aC 极低 + 覆盖 1.0」不足以保证有信号：本数据集 6 字段中 1 个空列、4 个方向稳定为负。

## 5. 存档索引

- 本文件：`Claude/skills/wq-brain-ra-usa/references/_usa-pv106-field-profile-20261023.md`
- 波 1：`tracking/USA/runs/usa_pv106_w1.txt`，multisim `1shYDqfBo4Ch90916n4uaixu`，结果 wave=`pv106_w1`
