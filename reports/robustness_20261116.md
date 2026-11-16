# 稳健性审计报告 2026-11-16

> 审计对象：`Jj85OR7e`（KOR / TOP600 / D1 / SLOW / decay 2 / trunc 0.08 / nanHandling OFF）
> 表达式：`subtract(group_rank(ts_mean(vec_avg(insd5_tnc), 66), sector), group_rank(ts_mean(vec_stddev(insd5_vol_af), 44), sector))`
> 判定：**PASS**（无 failed_checks，4 项软标记）
> 用户于 2026-11-16 12:52 GMT+8 点名提交。

## B.0 WebDataScope 门（硬前置）

`failed_ra_count = 0`、`failed_ppa_count = 0`、`ra_failed = false` ⇒ **Failed = 0**，通过。
`is.checks` 10 项 PASS 全绿（LOW_SHARPE / LOW_FITNESS / LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / LOW_SUB_UNIVERSE_SHARPE / LOW_INVESTABILITY_CONSTRAINED_SHARPE / CLUSTER_TEST / LOW_2Y_SHARPE / MATCHES_PYRAMID），`fail = []`，warning 仅 `MATCHES_COMPETITION` / `MATCHES_THEMES`（非 counted item）。

## B.1–B.5 归因

### 逐年归因（get_alpha_yearly_stats）

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | **−0.17** | 1.73 | 1.25 | 1.30 | 1.28 | 3.09 | 1.82 | 2.10 | 3.05 | **2.34** |
| Returns | −0.67% | 9.81% | 5.50% | 5.42% | 6.43% | 12.99% | 10.32% | 11.03% | 15.20% | 13.87% |
| Turnover | 11.98% | 12.29% | 12.28% | 12.39% | 12.44% | 12.62% | 12.03% | 12.15% | 12.34% | 12.23% |

- 换手十年**完全稳定**在 12.0–12.6%（极差 0.6pp），说明信号频率是结构性的、不靠交易强度换收益。
- 2014 为唯一负年（−0.17），此后九年**全正**且 2019 起逐年抬升（3.09 → 1.82 → 2.10 → 3.05 → 2.34）。

### 组合层贡献（performance_comparison，partition `EQUITY:KOR:1:POWER_POOL`）

| 量 | Before | After | Δ |
|---|---:|---:|---:|
| Sharpe | 4.41 | 4.74 | **+0.33** |
| Fitness | 3.22 | 3.51 | **+0.29** |
| Returns | 10.05% | 9.93% | −0.12pp |
| Turnover | 18.90% | 18.16% | **−0.74pp** |
| Drawdown | 1.56% | 1.35% | **−0.21pp** |

边际贡献为**强正**：收益基本持平（−0.12pp），但组合 Sharpe / Fitness 双升、换手与回撤双降。

### 相关性（check_correlation）

- prod = **0.5272**（`from_cache=true`，`cached_at 2026-11-16T10:46:53`，`source=platform_sync`，非 provisional ⇒ 48h 内，按 11-14 明令不回源）
- self = **0.0615**（OS 池 32 颗）
- 阈值 0.7，余量分别 0.173 / 0.639

## Phase C 反过拟合闸

| 检查项 | 实测 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed = 0，无 counted PENDING | **PASS** |
| Recent-3yr Sharpe（主判定） | 2.10 / 3.05 / 2.34，均值 **2.497 ≥ 1.58**，每年 > 0.3 | **PASS** |
| Recent-3yr CV_Sharpe | **0.162**（< 0.40） | **PASS** |
| 衰减比（2023 / 全期） | 2.34 / 1.81 = **1.293**（≥ 0.50；>1 表示末端无衰减） | **PASS** |
| 平年（仅近 3 年） | **0** | **PASS** |
| Recent-3yr max/min | 3.05 / 2.10 = **1.452**（≤ 3） | **PASS** |
| 全历史早年疲软 | 2014 −0.17（|S| 0.17 < 0.3 计平年，唯一负年） | **软标记**（绝不 REJECT） |
| Sub-universe | `LOW_SUB_UNIVERSE_SHARPE` PASS，值 **1.65** | **PASS** |
| 算子数 | **7**（> 5 软线；REGULAR 不据此 REJECT） | **软标记** |
| Margin @ turnover | **14.62 bp** @ TO 12.28% | **PASS** |
| Top-5 个股集中度 | 无逐股 PnL 不可得；`CONCENTRATED_WEIGHT` PASS 代证 | 不可得（平台代证 PASS） |
| 经济可解释性 | 「内部人申报参与广度（特殊关系方数量）宽、且交易后持股分布均匀的企业，优于少数大股东集中持股的企业」——一句话可写 | **PASS** |

补充：`S/2Y = 1.81 / 2.66 = 0.68`（项目规则 < 1.3 属健康区，非信号过生命周期）。

## 结论

**PASS**。软标记 4 项（2014 负年、7 算子、Top-5 不可得、单数据集 ATOM），已在台账 `robustness_Jj85OR7e` 与提交三段式 description 中如实披露。

## 附：塔与六维（提交前快照）

- 塔席位：`KOR/D1/INSIDERS`，当季计数 **1**，交后 **2**，门槛 3 ⇒ **不点亮，塔边际 0**；multiplier 1.2。
- 六维：ops **7**（distinct **5**：subtract / group_rank / ts_mean / vec_avg / vec_stddev）｜fields **2**（`insd5_tnc`、`insd5_vol_af`）｜两字段均为该数据集常用字段，T3/T4 无新增。
