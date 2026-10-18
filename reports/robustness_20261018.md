# Robustness 归因报告（2026-10-18）— USA × analyst44 提交三候选

判定依据：brain-alpha-robustness Phase B/C（2026-04-22 论坛共识阈值）。区域 USA，数据集 analyst44（单数据集 ATOM）。

## 候选 1：`gJWoaJqv`（背离加速度，504窗/market轴/d20/RAM）

- 表达式：`quantile(group_rank(hump(ts_delta(ts_av_diff(subtract(eps_rev, sales_rev), 504), 252), hump=0.01), market))`
- IS：S 1.74 / F 1.27 / 2Y 2.21 / SUB 0.86 / TO 0.1014 / returns 6.71% / margin 13.2bp
- 相关性：prod 0.6978 ✓ / self 0.5578 ✓（check_correlation refresh 实测）
- WebDataScope：failed_ra=0 / failed_ppa=0，checks.fail=[] ✓
- 逐年 Sharpe：2014 2.51 / 2015 2.38 / 2016 0.91 / 2017 2.27 / 2018 1.19 / 2019 2.35 / 2020 0.29 / 2021 1.86 / 2022 2.27 / 2023 2.19
  - Recent-3yr（2021-23）：1.86/2.27/2.19，全正且均值 2.11 ≥ 1.58 ✓
  - CV_Sharpe = 0.085 < 0.40 ✓；衰减比 2.19/1.74 = 1.26 ≥ 0.50 ✓；max/min 1.22 ≤ 3 ✓；平年 0 ✓
- SUB：平台 LOW_SUB_UNIVERSE_SHARPE PASS ✓
- Margin@TO：13.2bp @ TO 10.1% ≥ 5bp ✓
- 经济可解释：盈利质量（EPS 修正 vs 收入修正背离）的**改善加速度**——分析师盈利上修加速且被收入验证的公司跑赢。
- **判定：PASS**

## 候选 2：`xA1mvAmw`（背离加速度，756窗/sector轴/d10/RAM）

- IS：S 1.75 / F 1.21 / 2Y 2.20 / SUB 0.85 / TO 0.1335 / returns 6.36% / margin 9.5bp
- 相关性：prod 0.6955 ✓ / self 0.5577 ✓
- WebDataScope：0/0，fail=[] ✓
- 逐年 Sharpe：2021 1.87 / 2022 2.28 / 2023 2.16（近3年全正，均值 2.10）；CV 0.085；衰减比 1.23；max/min 1.22
- SUB PASS ✓；Margin 9.5bp @ TO 13.4% ✓
- **判定：PASS**

## 候选 3：`3qjnoddP`（背离加速度，504窗/sector轴/d10/RAM）

- IS：S 1.74 / F 1.20 / 2Y 2.19 / SUB 0.89 / TO 0.1336 / returns 6.33% / margin 9.5bp
- 相关性：prod 0.6891 ✓ / self 0.5541 ✓
- WebDataScope：0/0，fail=[] ✓
- 逐年 Sharpe：2021 1.96 / 2022 2.20 / 2023 2.29（近3年全正且逐年抬升，均值 2.15）；CV 0.063；衰减比 1.32；max/min 1.17
- SUB PASS ✓；Margin 9.5bp ✓
- **判定：PASS**

## 共同软标记（soft flags）

- Top-5 个股集中度：PnL 接口未返回逐股分解，无法计算 ⇒ 软标记「未测」（非 REJECT 项）。
- 三者互为同机制变体（背离加速度，仅窗/轴/decay 不同），互相关预计 0.7-0.9；提交时按用户指令「base 收益前 3」执行。
- 全历史早年（2016/2018/2020）Sharpe 0.29-1.19 偏软：按近窗制度仅作信息软标记，不据此 REJECT。

## 结论

三个候选全部 **PASS**，建议提交（用户已明确授权提交 base 收益前 3）。

---

## 追记（11:40）：按 base payment 标准重选 + mLYxaLxp 拦截

用户澄清「base 收益最大」= 可获得的 **base payment** 最大。论坛实证（4 帖互证）：
高 fitness + 低 PC（prod correlation）是 base payment 的「版本答案」；self-corr < 0.3 时大概率 BP > 1.5；
`returns` 主要影响 OS 特许权使用费而非 base payment 档位（此前按 returns 误选，已废弃，且三次提交均未成功、无浪费）。

### 重选结果（PASS 集合内按 F×(1−PC) 排）

| 排名 | alpha | F | PC | self | 近3年Sharpe | 判定 |
|---|---|---:|---:|---:|---|---|
| 1 | **npAONOVa** | 1.25 | 0.6481 | 0.3861 | 1.19/1.74/2.00（1.64） | **PASS → 提交** |
| 2 | **MP056Plk** | 1.19 | 0.6735 | 0.3998 | 1.14/1.62/2.18（1.65） | **PASS → 提交** |
| 3 | **gJWoaJqv** | **1.27** | 0.6978⚠贴线 | 0.5578 | 1.86/2.27/2.19（2.11） | **PASS → 提交**（F 最高；PC 贴线为已知权衡） |
| — | mLYxaLxp | 1.20 | 0.6420 | 0.3992 | 1.05/1.62/1.79（**1.49 < 1.58**） | **REJECT**（RECENT_3YR_SHARPE，不提交） |

备选（未换上的原因）：`3qjnoddP`（F 1.20/PC 0.6891/self 0.5541，PASS，综合分略低于 gJWoaJqv）。

### mLYxaLxp 拦截依据
brain-alpha-robustness Phase C「Recent-3yr Sharpe（主判定）」：REJECT = 某近年 < 0 或 **3 年合计 < 线**。
mLYxaLxp 2021-23 均值 1.487 < 1.58 ⇒ REJECT。平台 2Y 闸（近 2 年，1.64）已过，
但内部近 3 窗制更严，fail-closed 执行，留档不提交；其低 PC（0.642）优势由 npAONOVa/MP056Plk 覆盖。
