# 稳健性审计 · 2026-10-25（IND/D1 未点亮塔三颗候选）

依据 `brain-alpha-robustness` Phase B/C（阈值 = 2026-04-22 论坛共识台账，不因当日论坛内容改变）。
IS 区间 2014-01-01 ~ 2023-12-31；「近 3 IS 年」= 2021 / 2022 / 2023。
用户 2Y 线 = `PLATFORM_CHECK_LINES["low_2y_sharpe_min"]` = 1.58。

## 0. 结论

| alpha | 塔归属 | Sharpe | 2Y | sub | robust | prod / self | 判定 |
|---|---|---|---|---|---|---|---|
| `E5VNe67L` | institutions + pv | 3.20 | 3.00 | 1.64 | 1.80 | 0.6459 / 0.3437 | **PASS** |
| `KPmvEYeE` | institutions + pv | 3.07 | 3.14 | 1.65 | 1.49 | 0.6162 / 0.3094 | **PASS** |
| `vRO9nG3w` | macro + pv | 2.90 | 3.14 | 1.69 | 1.78 | 0.6695 / 0.6806 | **CONDITIONAL** |

三者 `is.checks` 全 pass，RA 失败项 0，PENDING 仅相关性 / 配额类（不计 Failed）。
三者 PEP 十年逐年 PnL 全正（2014–2023），无「厂」字形。

## 1. 逐年证据（平台 `get_alpha_yearly_stats`，IS）

| year | E5VNe67L S / dd | KPmvEYeE S / dd | vRO9nG3w S / dd |
|---|---|---|---|
| 2014 | 6.80 / 2.04% | 6.40 / 1.33% | 6.65 / 1.86% |
| 2015 | 1.70 / 2.81% | 1.99 / 3.00% | 1.30 / 4.12% |
| 2016 | 3.33 / 1.84% | 3.21 / 1.56% | 2.64 / 2.60% |
| 2017 | 2.40 / 3.43% | 2.76 / 2.24% | 2.34 / 2.24% |
| 2018 | 3.19 / 2.21% | 4.65 / 2.04% | 3.09 / 2.87% |
| 2019 | 2.60 / 3.39% | 3.15 / 2.97% | 2.57 / 2.20% |
| 2020 | 3.39 / 2.43% | 1.45 / 4.01% | 3.42 / 2.83% |
| 2021 | 2.85 / 1.98% | 1.65 / 2.73% | 1.33 / 3.78% |
| 2022 | 2.57 / 2.43% | 2.88 / 1.78% | 3.36 / 1.55% |
| 2023 | 3.63 / 2.50% | 3.54 / 1.30% | 2.95 / 1.99% |

## 2. Phase C 反过拟合闸（近 3 年）

| 检查项 | E5VNe67L | KPmvEYeE | vRO9nG3w |
|---|---|---|---|
| Recent-3yr Sharpe（主判定） | 2.85 / 2.57 / 3.63 全正 → PASS | 1.65 / 2.88 / 3.54 全正 → PASS | 1.33 / 3.36 / 2.95 全正 → PASS |
| Recent-3yr CV_Sharpe | **0.18** PASS | **0.36** PASS | **0.42** ⚠ CONDITIONAL |
| 衰减比（last / 全期） | 3.63/3.20 = 1.13 PASS | 3.54/3.07 = 1.15 PASS | 2.95/2.90 = 1.02 PASS |
| 平年数（S≤0.3 视为平年） | 0 PASS | 0 PASS | 0 PASS |
| Recent-3yr max/min | 1.41 PASS | 2.15 PASS | 2.53 PASS |
| Sub-universe / robust | 1.64 / 1.80 PASS | 1.65 / 1.49 PASS | 1.69 / 1.78 PASS |
| Margin @ turnover | 6.9–25.9 bp @ TO 22–29% PASS | 7.0–23.1 bp @ TO 22–27% PASS | 5.2–23.1 bp @ TO 23–28% PASS |
| WebDataScope Failed | 0 PASS | 0 PASS | 0 PASS |
| 经济可解释性 | 一句话可写 PASS | 一句话可写 PASS | 一句话可写 PASS |

经济含义（三颗同族）：把 252 日收益对某个基本面 / 机构 / 宏观字段做时序回归取残差，再横截面排序
——捕捉「因子解释不了的个股特异收益」的反转，属残差化反转族（`rank(-ts_regression(returns, F))`）。

## 3. 未完成项与软标记

- **季度回撤日历未逐季核验**：取 `get_alpha_pnl` 时账号认证被 429（同期本区 campaign 与另一 EUR
  campaign 在跑）。可用上界替代：季度回撤 ≤ 所在年度回撤 ≤ 4.12%（三颗最大都在 2015），
  年度平均 2.5%–2.7%，无年度异常。需要逐季结论时在战役空档补跑。
- **Top-5 个股集中度不可得**：`get_alpha_pnl` 只有账户级曲线，无逐股分解；三颗 long/short count
  均 240–260 只，结构性集中风险低（非证据，仅先验）。
- `vRO9nG3w` 的唯一软标记是 Recent-3yr CV = 0.42（2021 年 S=1.33 拖累）。按 skill 的 CONDITIONAL
  处置：先 `brain-alpha-repair` 修复 ≤2 轮再请用户确认；但它不触发 `submit_verdict` 的 BLOCKED。
  ⚠ MACRO 当季 2/3，而 `macro63` 只有 1 字段被 `n_fields>=3` 挡在池外 —— 本区暂无第二条 MACRO 现货。

## 4. 两两相关（2586 个共同交易日 PnL 差分 Pearson）

| 对 | r |
|---|---|
| E5VNe67L ↔ KPmvEYeE | 0.6615 |
| E5VNe67L ↔ vRO9nG3w | 0.6733 |
| KPmvEYeE ↔ vRO9nG3w | 0.6245 |
| E5VNe67L ↔ 9qEPO5K2 | 0.7235（不可配对） |

三者两两均 < 0.7，可依次提交（SELF 互相关应在闸内；最终以提交前 `check_correlation` 为准）。

## 5. 提交前 prod 实测复核（2026-10-26 00:47–00:58，`check_correlation(refresh=True)`）

| alpha | 10-23 缓存值 | 2026-10-26 实测 | < 0.7 |
|---|---|---|---|
| E5VNe67L | 0.6459 | **0.6643**（00:47:29） | ✅ |
| KPmvEYeE | 0.6162 | **0.6162**（00:56:27） | ✅ |
| vRO9nG3w | 0.6695 | **0.6804**（01:05:39） | ✅（余量仅 0.0196） |

- 实测走 `BrainApiClient.check_correlation(..., threshold=0.7, refresh=True)`（持 `logs/_dblock/correlation.lock.json`，账号级单并发），
  不是直连 GET —— 直连 `GET /alphas/{id}/correlations/prod` 当时四颗全返回空体（平台仍在算），**空体不得当数字用**。
- 同批 `ZYmJYx30` = **0.723**（00:41:06）越线，已在台账 `robustness_ZYmJYx30` 的 `soft_flags` 留痕并判该族不可提交。
