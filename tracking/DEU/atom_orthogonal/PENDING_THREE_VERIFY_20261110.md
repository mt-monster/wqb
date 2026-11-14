# 三件待授权件 · 平台状态核验（2026-11-10 19:4x）

> 目的：授权前确认三件未被占用/提交、指标未漂移，并修正台账与平台的不一致。

| alpha | status | stage | S | F | 2Y | TO | 备注 |
|---|---|---|---:|---:|---:|---:|---|
| RREPm361 | UNSUBMITTED | IS | 2.02 | 1.25 | 1.82 | 0.2508 | 首选；prod 0.6881（余量 0.012，**提交前必须 refresh**） |
| 1YNMAA8M | UNSUBMITTED | IS | 1.58 | 1.36 | 2.13 | 0.1337 | prod 0.6951（余量 0.005，**提交前必须 refresh**）；self 0.6946 |
| E569ZE7L | UNSUBMITTED | IS | 1.68 | 1.21 | 2.27 | 0.1128 | prod/self 0.5444；稳健性 CONDITIONAL（3y CV 0.626） |

## ⚠ 台账更正：RREPm361 的真实表达式

**平台实际（权威）**：
```
group_rank(add(ts_zscore(est_12m_ebi_median, 240), ts_zscore(subtract(est_12m_ebt_mean, est_12m_ebt_mean_4wks_ago), 44)), sector)
```
- 5 算子；数据集 analyst7；字段：est_12m_ebi_median（EBIT 中位数预期）+ est_12m_ebt_mean 的 4 周变化。

**此前台账记录（已过时，勿再引用）**：ebt_mean 240 窗 + pre_mean 66 窗版本。
⇒ 教训：台账中的表达式必须与平台 get_alpha_details 对齐后再写入交付文档；跨天引用前先重读平台。

## 授权前动作清单（不可省）

1. **prod refresh**：RREPm361（0.6881）与 1YNMAA8M（0.6951）余量极薄，提交前一刻必须 `check_correlation(correlation_type="production", refresh=true)` 取权威值。
2. **self refresh**：1YNMAA8M self 0.6946 贴线，OS 池若有新增件需重算。
3. **逐年覆盖**：三件均有历史台账记录零空窗；提交前用 get_alpha_yearly_stats 复核一次（近十年 longCount>0 且 pnl≠0）。
4. **互相关**：三件之间及与 OS 池 19 件的全对 <0.7（2026-11-09 全局标准）；1YNMAA8M ~ rKRx2Alj 0.6946 为最高对。
5. 用户文字授权后，逐颗 `workflow_submit_alpha(confirm_submit=True)`；**授权前不得提交**。
---

## 已 ACTIVE 两件的逐年健康度复核（2026-11-10 19:4x）

**zq3eb7No（analyst7 / ANALYST 塔 / S2.01）逐年 Sharpe**：
2014 3.59 / 2015 1.90 / 2016 2.06 / 2017 3.30 / 2018 1.60 / 2019 0.52 / 2020 2.32 / 2021 2.21 / 2022 2.33 / 2023 0.81
- 十年零空窗；longCount 155→211 单调递增；**10 年全正**（最低 0.52）。

**bl6AvMkN（analyst_factor_signals + predictive_starmine / S1.61）逐年 Sharpe**：
2014 2.22 / 2015 2.86 / 2016 0.85 / 2017 1.03 / 2018 0.87 / 2019 1.61 / 2020 0.36 / 2021 2.70 / 2022 2.03 / 2023 1.78
- 十年零空窗；longCount 93→175；**10 年全正**（最低 0.36）。

⇒ 两颗已交付件覆盖与年度稳健性均达标（无连续空窗、无负年）。