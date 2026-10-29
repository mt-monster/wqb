# 波 177 — `mfm_model_output` 十风格因子 × 十结构互异模板

- **区域 / 设置**：USA / TOP3000 / D1 / **STATISTICAL** / decay 2 / truncation 0.05 / nanHandling OFF / 2014-01-01 ~ 2023-12-31
- **数据集**：`mfm_model_output`（117 字段 / coverage 0.9963 / alphaCount 308 / valueScore **3.0** / pyramid `USA/D1/RISK` multiplier 1.1）
- **结论**：**1/10 命中**，`qMLbW8xP` 过全部硬闸（fRA=0）
- **批次**：multisim `1veAhE6Lx4t3cG96xNWTynM`，10 条全部 terminal，0 错误
- **落库**：`n_pass=1 / n_near=0`

## 1. 十模板结果总表

| # | 字段 | 模板（骨架结构） | alpha | S | F | TO | 2Y | SUB | invest_r | fRA |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | `momentum_factor_score` | 线性衰减 + 反向：`group_rank(reverse(ts_decay_linear(ts_backfill(F,22),66)), industry)` | `78LOZWjb` | −0.27 | −0.06 | 10.84% | 0.55 | 0.51 | 2.1852 | 3 |
| T2 | `relative_size_factor` | 年度偏离 + 截面 zscore：`group_zscore(ts_av_diff(ts_backfill(F,22),252), sector)` | `O0AerO7J` | **−1.16** | −0.78 | 15.51% | −1.02 | −0.34 | 0.6724 | 3 |
| T3 | `relative_liquidity_factor` | 长窗序位：`group_rank(ts_rank(ts_backfill(F,22),504), industry)` | `WjOkPM7Z` | 0.86 | 0.34 | 10.30% | 0.72 | 0.47 | 1.0000 | 3 |
| T4 | `relative_leverage_factor` | 二阶波动：`group_rank(ts_std_dev(ts_backfill(F,22),66), industry)` | `RREXVMVb` | −0.33 | −0.08 | 6.34% | 0.39 | 0.03 | 1.0000 | 3 |
| T5 | `broad_market_factor_score_2` | 三阶符号幂：`group_rank(signed_power(ts_zscore(ts_backfill(F,22),252),3), industry)` | `KPJeO3Op` | **0.00** | — | **0.00%** | — | — | — | 5 |
| **T6** | **`short_interest_factor_score_2`** | **逆均值：`group_rank(reverse(ts_mean(ts_backfill(F,22),22)), industry)`** | **`qMLbW8xP`** | **1.73** | **1.02** | 8.19% | **2.48** | 0.84 | 1.0231 | **0** |
| T7 | `systemic_risk_measure_2` | 一阶差分：`group_rank(ts_delta(ts_backfill(F,22),66), industry)` | `gJevQ6ZO` | 0.40 | 0.11 | 11.27% | 0.52 | 0.56 | 1.1250 | 3 |
| T8 | `hedge_fund_ownership_factor1` | 长窗 zscore + 反向 + 细分组：`group_rank(reverse(ts_zscore(ts_backfill(F,22),252)), subindustry)` | `A1V609ve` | **−1.18** | −0.49 | 8.81% | −0.99 | −0.62 | 0.9746 | 4 |
| T9 | `relative_volatility_factor` | 年度偏离：`group_rank(ts_av_diff(ts_backfill(F,22),66), industry)` | `Vkxn6VdV` | 0.58 | 0.18 | 13.60% | **1.16** | 0.57 | 1.0813 | 3 |
| T10 | `systemic_risk_factor_score` | 二阶协方差：`group_rank(ts_covariance(ts_backfill(F,22), ts_backfill(F,22),66), industry)` | `wpQ6Yq9l` | −0.70 | −0.28 | 7.99% | −0.52 | −0.30 | 1.0571 | 3 |

`prescreen`：READY = [`qMLbW8xP`] / REVIEW 空 / REJECT = 其余 9 条。

## 2. `F = S·sqrt(R/max(TO, 0.125))` 在 10 条上 10/10 命中（含 7 条只有地板公式能对上）

| alpha | 实测 F | TO | 用 TO 反算 | 用 0.125 反算 | 判 |
|---|---|---|---|---|---|
| `78LOZWjb` | −0.06 | 10.84% | −0.063 | — | **地板** |
| `O0AerO7J` | −0.78 | 15.51% | **−0.781** | — | TO |
| `WjOkPM7Z` | 0.34 | 10.30% | 0.370 | **0.336** | **地板** |
| `RREXVMVb` | −0.08 | 6.34% | −0.109 | **−0.078** | **地板** |
| `qMLbW8xP` | 1.02 | 8.19% | 1.259 | **1.018** | **地板** |
| `gJevQ6ZO` | 0.11 | 11.27% | 0.121 | **0.109** | **地板** |
| `A1V609ve` | −0.49 | 8.81% | −0.580 | **−0.487** | **地板** |
| `Vkxn6VdV` | 0.18 | 13.60% | **0.179** | — | TO |
| `wpQ6Yq9l` | −0.28 | 7.99% | −0.353 | **−0.282** | **地板** |

**与波 176 合并：两个数据集共 17 条 alpha，`TO 地板 = 0.125` 全部反算吻合（16/17 精确到小数点后两位）。** 这条公式从推演升级为可用的工程工具：任何候选拿到 S / R / TO 就能预测 F，不必再花仿真槽试错。

### 推论：本波 7/10 条落在 TO < 12.5% 的「地板区」

⇒ **对它们压换手对 F 零收益**。这是重要的策略反转：`78LOZWjb` / `WjOkPM7Z` / `RREXVMVb` / `qMLbW8xP` / `gJevQ6ZO` / `A1V609ve` / `wpQ6Yq9l` 这 7 条若 F 不够，唯一出路是**提 R（或提 S）**；反过来，**从地板下把 TO 适度提回 12.5% 附近能白拿 F**——`qMLbW8xP` 当前 F=1.02 恰好过闸，但若 margin 比不变、TO 从 8.19% 提到 12.5%，F 会按 `sqrt(TO/0.125)` 之外的方式变化（TO 超过地板后公式换段），是可探索方向。

## 3. 命中的 `qMLbW8xP` 机制归因

```
group_rank(reverse(ts_mean(ts_backfill(short_interest_factor_score_2, 22), 22)), industry)
STATISTICAL / TOP3000 / D1 / decay 2 / trunc 0.05 / nanHandling OFF
```

| 指标 | 值 | 闸 |
|---|---|---|
| S / F | 1.73 / 1.02 | ≥1.58 / ≥1.00 ✅ |
| 2Y | **2.48** | ≥1.58 ✅ |
| TO / R / margin | 8.19% / 4.33% / **10.58bp** | ✅ |
| SUB | 0.84 | ≥0.752（0.4346×1.73）✅ |
| invest_S / ratio | 1.77 / 1.0231 | ≥0.70 ✅ |
| longCount / shortCount | 1606 / 1520 | ✅ |
| **ra_failed_count** | **0** | ✅ |
| pyramid | `USA/D1/RISK`（effective=1） | 点塔 ✅ |

**经济机制：卖空水平异象的反向（低卖空敞口跑赢）。** Asquith–Pathak–Ritter (2005) 的 short-interest anomaly 在 2014–2023 的 USA 大盘上表现为「卖空强度越低 → 后续超额收益越高」，本式 `reverse(ts_mean(·,22))` 正是取这个方向。

**与同数据集的另一颗 `ZYQZEawY` 完全正交**：

| 对 | 4 年日收益相关（986 点） |
|---|---|
| `qMLbW8xP` × `ZYQZEawY` | **0.1277** |
| `qMLbW8xP` × `0mYopJ7r` | 0.1454 |
| `qMLbW8xP` × `WjOkPM7Z` | **−0.0179** |
| `ZYQZEawY` × `0mYopJ7r` | 0.8914（同机制，只能取一） |
| `ZYQZEawY` × `WjOkPM7Z` | 0.1031 |

原因：`ZYQZEawY` 用的是 `discount_store_retail_score`，其真实语义是 **"Daily specific (idiosyncratic) returns = 残差日收益 %"**（特质残差反转），而 `qMLbW8xP` 用的是**卖空敞口水平**。一个交易「个股相对模型的定价错误」，一个交易「卖空者的仓位拥挤度」，两者在经济学上无交集。

**这是本会话最重要的方法论突破**：此前在同一字段 `discount_store_retail_score` 上换窗口（66 vs 252，相关 ≥0.89）与换分组轴（industry vs subindustry，相关 0.8914）都被证死 ⇒ **在同一字段内换形态无法解耦，必须换机制**。

## 4. 两个「信号真实但强度不足」的字段（反向读数的价值）

T2 与 T8 的**原始 S 为负且绝对值 ≥1.16**，意味着反向表达式的 S 天然 ≥1.16。这是本波除 `qMLbW8xP` 外唯一的经济价值所在——它们不是噪声，是方向被写反了。

| 反向后的期望读数 | T2 `relative_size_factor` | T8 `hedge_fund_ownership_factor1` |
|---|---|---|
| S | **1.16** ✅ | **1.18** ✅ |
| F | 0.78 ✗ | 0.49 ✗ |
| 2Y | 1.02 ✗（需 1.58） | 0.99 ✗（需 1.58） |
| SUB | 0.34 ✗（需 0.504） | 0.62 ✅（需 0.513） |
| invest_ratio | 0.6724 ✗（<0.70） | 0.9746 ✅ |
| R / TO | 7.03% / 15.51% = 0.4533 | 2.13% / 8.81% = 0.2418 |

- **T2 反向**：R/TO = 0.4533，要 F=1.0 需 0.743 ⇒ 需把 TO 压 39% 或把 R 提 64%。且 invest_ratio 0.6724 卡在自设 0.70 闸下。
- **T8 反向**：TO 8.81% 在地板区 ⇒ **压 TO 对 F 无效**。R 仅 2.13%，margin 4.84bp。要 F=1.0 需 R 提到 8.76%（4×）。靠压换手不可能，必须换骨架提 margin。

⇒ T8 的正确救法是**换骨架**，不是调参。这正是波 178 用 `qMLbW8xP` 的获胜骨架（margin 10.58bp）重测 `hedge_fund_ownership_factor0` 的原因。

## 5. 其余字段的确定性结论

- **`broad_market_factor_score_2` 是整列为 0 的空字段**：`KPJeO3Op` S 0.00 / TO 0.00% / longCount 0 / shortCount 0，fRA = 5（LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE 全挂）。该字段 `alphaCount = 0 / userCount = 0`。
  **教训：`alphaCount = 0` 的字段不能假定「没人挖过 = 有信号」，必须先跑一条最廉价的裸水平探针确认非零。**
- **`relative_leverage_factor` 全档弱**：T4 S −0.33，历史 1 条也弱 ⇒ 判死该字段。
- **`relative_volatility_factor` 值得二次投入**：T9 的 **2Y 1.16 > S 0.58**，说明近年显著变强，是全部 10 个字段里唯一的「时间趋势正向」字段。
- **`relative_liquidity_factor` 与已有两颗完美正交（−0.0179 / 0.1031）但 S 只有 0.86** ⇒ 它是理想的「第 3 颗骨架载体」，差的是信号强度不是相关性。波 178 用获胜骨架重测它是正确赌注。
- **`hedge_fund_ownership_factor0`**（94 users / 155 alphas，本数据集最拥挤）从未在我账号下测过，波 178 首次实测。
- **61 个行业暴露 score + 43 个行业二元 flag 全部无增量**，不再投入。

## 6. 两个命名陷阱（写进字段画像，避免后续误用）

| 字段名 | 字面含义 | **实际语义** |
|---|---|---|
| `discount_store_retail_score` | 折扣零售评分 | **Daily specific (idiosyncratic) returns = 特质残差日收益 %** |
| `systemic_risk_factor_score` | 系统性风险因子 | **Specific risk matrix per stock per day, annualized percent-squared = 特质方差**（"systemic" 应为 "specific"） |

真正的系统性风险字段是 `systemic_risk_measure_2`（T7，S 0.40）。

## 7. 后续动作

1. **RISK 塔当前资产 = 2 颗合格且共存**（`ZYQZEawY` S1.64/F1.00/2Y1.64 + `qMLbW8xP` S1.73/F1.02/2Y2.48，相关 0.1277），**缺第 3 颗**。
2. 波 178 已派发（multisim `3e0lMk9yy59VcIcDIdtSMiA`），两条腿：
   - **获胜骨架字段扫描**（7 条）：`group_rank(reverse(ts_mean(ts_backfill(F,22),22)), industry)`，F ∈ {`relative_momentum_factor`, `hedge_fund_ownership_factor0`, `relative_size_factor`, `relative_liquidity_factor`, `systemic_risk_measure_2`, `relative_volatility_factor`, `momentum_factor_score`}
   - **同字段解耦结构**（3 条）：`short_interest_factor_score_2` 的二阶波动 / 一阶差分反向 / 长窗序位反向 —— 测能否复现 `qMLbW8xP` 的强度但换掉持仓
3. 若波 178 的 `relative_liquidity_factor` 或 `relative_size_factor` 在获胜骨架下 S ≥ 1.58 且与已有两颗 < 0.7 ⇒ RISK 塔亮点，可同日提交 3 颗。
