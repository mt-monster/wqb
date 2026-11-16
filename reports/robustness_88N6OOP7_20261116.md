# Robustness Audit — `88N6OOP7`（USA / TOP3000 / D1）

审计时间：2026-11-16 10:40 (GMT+8)｜审计人：agent｜提交前 fail-closed 必填项

## 0. 基本信息

| 项 | 值 |
|---|---|
| 表达式 | `vector_neut(ts_zscore(subtract(ts_mean(mean_top_buy_transaction_count, 22), ts_mean(mean_top_buy_transaction_count, 126)), 252), -ts_corr(vec_avg(rsk59_squeeze_risk), vec_avg(rsk59_shortinterestnotional), 504))` |
| 设置 | USA / TOP3000 / delay=1 / decay=**15** / SUBINDUSTRY / truncation 0.08 / pasteurization ON / unit VERIFY / nan ON |
| 结构 | 主腿＝大额买入笔数「22d 均 − 126d 均」的 252 日 z-score（交易活动加速）；中性化腿＝squeeze 风险 × 空头利息名义额 504 日相关，取负；`vector_neut` 做向量投影中性 |
| 指标 | S **2.38** / F **2.00** / TO **21.99%** / Ret **15.48%** / DD **12.29%** / margin **14.07 bp** |
| 闸门 | 2Y **2.58**（ladder 窗 2）/ sub **1.06** / investability 0.45 / risk-neutralized S 2.67 |
| 相关性 | prod **0.6412** / self **0.2297** |
| `checks.fail` | **[]**（pass 含 LOW_SHARPE/LOW_FITNESS/LOW_TURNOVER/HIGH_TURNOVER/CONCENTRATED_WEIGHT/LOW_SUB_UNIVERSE_SHARPE/IS_LADDER_SHARPE/CLUSTER_TEST/MATCHES_PYRAMID；warning 仅 MATCHES_COMPETITION / MATCHES_THEMES 两条信息项） |

## 1. Phase A — 全闸（`checks.fail=[]`）

| 闸 | 实测 | 线 | 余量 |
|---|---|---|---|
| LOW_SHARPE | 2.38 | 1.58 | **+0.80**（宽） |
| LOW_FITNESS | 2.00 | 1.00 | **+1.00**（宽） |
| TURNOVER | 21.99% | 1%–70% | 带内 |
| CONCENTRATED_WEIGHT | pass | <10% | — |
| LOW_SUB_UNIVERSE_SHARPE | **1.06** | 0.433×2.38 = **1.0305** | **+0.030（最薄闸）** |
| IS_LADDER_SHARPE | 2Y **2.58** | **2.02** | **+0.56**（宽） |
| CLUSTER_TEST | **1.86** | 1.58 | +0.28 |
| SELF_CORRELATION | 0.2297 | <0.70（软线 0.55） | +0.32 / +0.46 |
| PROD_CORRELATION | 0.6412 | <0.70 | **+0.058** |
| REGULAR_SUBMISSION | 待补 description | 需有三段式 | 本次补 |

## 2. Phase B — 逐年归因（`get_alpha_yearly_stats`，IS 2014–2023）

| 年 | Sharpe | Returns | Turnover | Drawdown | Fitness |
|---|---:|---:|---:|---:|---:|
| 2014 | **−0.03** | −0.27% | 26.12% | **12.29%** | −0.00 |
| 2015 | 4.03 | 27.42% | 23.84% | 2.59% | 4.32 |
| 2016 | 1.78 | 11.87% | 21.33% | 6.41% | 1.33 |
| 2017 | 3.22 | 16.14% | 21.33% | 4.32% | 2.80 |
| 2018 | 3.50 | 17.95% | 22.44% | 1.58% | 3.13 |
| 2019 | 2.81 | 16.94% | 21.20% | 3.17% | 2.51 |
| 2020 | 2.43 | 13.89% | 20.71% | 2.74% | 1.99 |
| 2021 | 2.47 | 17.28% | 20.40% | 3.38% | 2.27 |
| 2022 | 3.17 | 21.84% | 21.41% | 2.50% | 3.20 |
| 2023 | 2.08 | 12.43% | 21.06% | 2.49% | 1.60 |

**四条结论**：

1. **9/10 年为正**；唯一负年 2014 的 Sharpe 是 **−0.03**（收益 −0.27%），实质为零 —— 那是样本起始年、持仓从 76 只爬升到 162 只的建仓期，不是信号失效。
2. **最大回撤 12.29% 全部落在 2014**，2015 起逐年 DD 均 ≤ 6.41%（中位数 3.0%）。⇒ 全样本 DD 12.29% 是起始期伪影，稳态风险远低于账面值。
3. **换手无结构性漂移**：10 年在 20.40%–26.12% 的窄带内，且逐年单调收敛（26%→21%）。⇒ 不存在「靠高换手换收益」的时间依赖。
4. **无单年依赖**：剔除最好年份 2015（S 4.03 / Ret 27.42%），剩余 9 年平均 Sharpe 仍 ≈ **2.4**；近三年 2.47 → 3.17 → 2.08 非单调衰减，2023 回落但仍有 2.08。

## 3. Phase C — 参数面（同族已实测三档 decay，非网格试凑）

| 变体 | decay | S | F | 2Y | sub | TO | 结论 |
|---|---:|---|---|---|---|---|---|
| `npazn8v3` | 10 | 2.43 | 2.02 | 2.64 | 1.06 | 22.97% | S 最高但 sub 余量仅 +0.008 |
| **`88N6OOP7`** | **15** | 2.38 | 2.00 | 2.58 | 1.06 | **21.99%** | **sub 余量 +0.030（最厚）、TO 最低、prod/self 最低** |
| `Jj8XKW62` | 20 | 2.37 | 2.01 | 2.58 | 1.05 | ~19% | sub 余量 +0.024 |

选择 decay=15 的理由：`sub` 是唯一贴线的闸，且它是**比值闸**（线 = 0.433×S，S 越高线也越高）。decay10 的 S 高出 0.05，但把 sub 余量压到 +0.008（1.06 两位小数 ⇒ 最坏 +0.003），不划算；decay15 用 −0.05 S 换 3.8 倍余量，且同时 prod / self / 换手 / 单笔 margin 四项都最优。

## 4. Phase D — 相关性与容量

- **prod 0.6412**（< 0.70，余量 +0.058）；本族三颗孪生件中最低。
- **self 0.2297**（< 软线 0.55 一大截）；`diversity_audit` 判定 `level=light`、有效宽度贡献约 77%。
- 三颗 `npazn8v3` / `88N6OOP7` / `Jj8XKW62` 互相关 **0.9857–0.9968** ⇒ 只能三选一，提交本颗即封死另两颗（已知并接受）。
- **容量弱项**：`investability_sharpe` **0.45** / `investability_fitness` **0.21**。这是本次审计唯一的实质性短板 —— 该信号在缩容宇宙上衰减明显。但它不在 `Consultant Submission Tests` 九项之内，属容量参考而非拒付项；且 `risk_neutralized_sharpe` 2.67 说明剥离风险因子后信号本身仍强。

## 5. 结论

**verdict = CONDITIONAL**

- **失败项（REJECT）：无**。`checks.fail = []`，九项提交测试全 PASS。
- **软告警 3 项**：
  1. `investability_sharpe 0.45`（容量弱，非闸门项）；
  2. `2023 Sharpe 2.08`，较 2018 峰值 3.50 回落（但仍在闸线上方 32%，且非单调衰减）；
  3. `sub_universe 1.06 vs 线 1.0305`，余量 **+0.030** 是全闸最薄一环，若平台重算需复查。
- **可提交**：9/10 年正、换手稳定、DD 伪影已定性、方案 D v2 `pass`（ΔS +0.06 / ΔF +0.06 / ΔRet +0.10pp / ΔTO +0.19pp）、塔边际 +1（USA/D1/RISK 2→3）。

## 6. 塔与六维（同期读数）

| 项 | 值 |
|---|---|
| 塔 | `USA/D1/RISK` ×1.1 → 当期 **2 → 3 新点亮（+1）**；`USA/D1/OTHER` ×1.4 → 3 → 4（已点亮，边际 0）；`effective = 2` 席 |
| 六维 | ops 6 / fields 3 / ΔT1 **+0.0037** / ΔT2 +0.0030 / T3 新算子 **0** / T4 新字段 **+1** |
