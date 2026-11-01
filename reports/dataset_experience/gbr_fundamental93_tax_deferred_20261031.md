# GBR fundamental93（Earnings Tax Data / 递延税费用）判死档案

- **区域 / 宇宙 / 延迟**：GBR / TOP700 / D1（GBR 只有 TOP700 一个 universe，无退路）
- **测试设置**：`INDUSTRY` + `decay 10` + `truncation 0.05` + `maxTrade OFF` + `nanHandling OFF` + `unitHandling VERIFY`（FUND 族标准档）
- **消耗预算**：2 批 / 4 条 sim
- **结论**：**判死**。4 条最大 |S| = 0.38，且两条触发 `CONCENTRATED_WEIGHT` 硬闸。
- **判死主因不是信号弱，是覆盖率**：持仓只有 118–142 只（TOP700 的 **17%–20%**）。

---

## 1. 数据集事实（17 字段，全 MATRIX，全 `coverage: 0.0`）

`get_datafields(dataset_id="fundamental93", filter_sharpe=False)` → `platform_count=17 / complete=true`。

| 组 | 字段 | 语义 | u / a |
|---|---|---|---|
| **递延税费用比率（7 分母版）** | `fnd93_deferred_tax_expense_{11,12,21,22,31,41,51}` | 分子 = 「净递延税负债 − 净递延税资产」；**XX 是分母索引**（7 种尺度归一化） | `_21` u3/a3 · `_22` u2/a2 · `_41` u2/a2 · `_11` u1/a1 · 其余 u0/a0 |
| **LTM 统计量** | `fnd93_expense_d1_mean` / `_dts`（**LTM 标准差**） / `_max` / `_min` / `_length` | 水平 / 不确定性 / 极值 / 观测数 | 0–1 |
| 负债侧 | `fnd93_liability_d1_length` | 仅观测数 | 0/0 |
| 资产增长别名 | `fnd93_accrualsratio_d1_asset_change` (u2/a3) / `fnd93_expense_d1_asset_change` / `fnd93_liability_d1_asset_change` | 「最新总资产 ÷ asset_ltm」YoY | 0–2 |
| 噪声 | `fnd93_accruals_d1_length` | 仅观测数 | 0/0 |

**字段描述被平台截断**：`_deferred_tax_expense_XX` 的 description 只到
`"There are 7 ratio fields with naming pattern \"DEFERRED_TAX_EXPENSE_XX\", where XX denotes the index of denominator. We use (Net deferred tax liability - Net defe…"`，
**无法从描述反查 11/12/21/22/31/41/51 各对应哪个会计分母**。只能按拥挤度选（`_21` 最常用）。

---

## 2. 四条实测全表

| alpha | 表达式 | S | F | TO | 2Y | SUB | margin | 持仓 | 失败闸 |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `xArXWM0w` | `rank(ts_backfill(fnd93_expense_d1_mean, 66))` | −0.03 | −0.00 | 5.13% | 0.55 | 0.14 | −0.095bp | 73+69=**142** | S / F / 2Y |
| `ZYQkMZej` | `rank(ts_backfill(fnd93_expense_d1_dts, 66))` | −0.27 | −0.11 | 5.02% | −0.44 | −0.25 | −0.814bp | 65+68=**133** | S / F / SUB / 2Y |
| `vR1a62lQ` | `rank(ts_backfill(fnd93_deferred_tax_expense_11, 66))` | 0.17 | 0.06 | 6.15% | −0.03 | −0.30 | +0.507bp | 65+69=**134** | S / F / **CW 0.1317** / SUB / 2Y |
| `QPvmgK9X` | `rank(ts_backfill(fnd93_deferred_tax_expense_21, 66))` | 0.38 | 0.22 | 6.18% | 0.14 | −0.12 | +1.330bp | 58+60=**118** | S / F / **CW 0.1509** / SUB / 2Y |

批次：批 48 = `2aFyFWgLS4RQ8Ych6IQgZ9d`（前两条）、批 49 = `3A1gonasz4Zzc14VQvZhmOn`（后两条）。
`pyramids.list` 全部 `GBR/D1/FUNDAMENTAL`（multiplier 1.6）。

---

## 3. 三条结构性判死理由

### 3.1 覆盖率只有 17%–20%，且换字段形态救不回来

最初假设是「`_mean` 需要多次观测才能算，单点比率 `_XX` 只需一期观测 ⇒ 覆盖会好很多」。
**实测否证**：`_XX` 反而更差（134 / 118 vs 142）。说明 GBR 里递延税科目本身就是稀疏的，
不是「LTM 统计量把样本削掉了」。

对照 `fundamental86`（同为 `coverage: 0.0` 但实测 579 只 = TOP700 的 83%），
⇒ **`coverage: 0.0` 只能判「有没有数据」，判「数据够不够」必须看 `longCount + shortCount`**。
83% 够用，20% 不够。这是本次最有价值的可复用判据。

### 3.2 `CONCENTRATED_WEIGHT` 是覆盖率不足的连带硬闸

700 只宇宙里只有约 120 只有值 ⇒ 单票权重必然冲破 10% 上限
（实测 0.1317 / 0.1509，limit 0.1，触发日期都在 2015 年 3 月）。
**这个闸无法靠换算子 / 换窗口 / 换中性化修**，只能靠提高覆盖率。
⇒ **覆盖率 < 30% 的候选，`CONCENTRATED_WEIGHT` 几乎必然挂**，应当在派发前就预判为死路，别浪费 sim。

### 3.3 TO 5%–6% ⇒ 年更数据，信号一年只动一次

四条 TO 全部落在 5.0%–6.2%。年更基本面 + 低换手组合下，Sharpe 无法靠交易频率补。
`xArXWM0w` 还暴露了**时间不稳定性**：全期 S −0.03 但 2Y 0.55 ⇒ 近两年才有微弱信号，全期没有。
这种形态即便方向反转也拿不到可用 Sharpe。

---

## 4. 机制先验与本区实测的分歧

先验来自 **Desai-Dharmapala 2006（BTD，book-tax difference 作为税务规避代理）** 与
Wilson 2009（tax shelter 惩罚）——预期「递延税费用比率越高（越激进）⇒ 未来收益越差」，
即 `reverse(rank(...))` 方向。

**GBR 实测不支持**：`_mean` 原始方向 S −0.03（反转后 +0.03）、`_dts` 原始 −0.27（反转后 +0.27）、
`_11` 原始 +0.17（反转后 −0.17）、`_21` 原始 +0.38（反转后 −0.38）。
四个方向的绝对值都 ≤ 0.38，且正负不统一 ⇒ **不是方向问题，是信号不存在**。

**另一个机制在本集不可实现**：Dyreng-Graham-Long 2008 的 **cash ETR** 需要
cash tax paid / pretax income，本集**无此二字段**；R/E/A 口径需要的 revenue / invested_capital / equity
也都不在 17 字段里。⇒ 税务激进性这条线在 GBR × fundamental93 上**无可用载体**。

---

## 5. 下次怎么办

1. **GBR 的 12 个 FUND 数据集自此全部测完**（`fundamental22` 只有 1 字段，可忽略）。
   新的 FUND alpha 不要再从「新数据集」找，只能从**已验证数据集的未用几何**找。
2. **`fundamental17` 是唯一还有厚度的 FUND 集**（135 字段，`current_enterprise_value` 是集内市场量）。
   `rKRQbPPE` 证明了 `divide(<会计量>, current_enterprise_value)` 是**单数据集**骨架，不占 PV+FUND 配额。
   后续 FUND 候选一律走这条路换分子，不要再碰 `coverage 0.0` 的小集。
3. **派发前加一道覆盖率预判**：任何 FUND 候选，若无法确认 `longCount + shortCount > 0.35 × 700 ≈ 245`，
   先派单条探针而不是直接上模板批，避免整批撞 `CONCENTRATED_WEIGHT`。
4. 本集字段可留作**辅助腿**：`_dts`（L2 不确定性）在 2Y 上 −0.44、全期 −0.27，
   方向稳定为负，可作为「风险越高越差」的正交腿备选，但覆盖面太小，优先级最低。
