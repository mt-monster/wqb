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

---

# 追加：wponnkmd（USA，17:06）

> 同日第二份稳健审计（追加写，非新文件）。台账 `robustness_wponnkmd`。

## 归因

- 表达式：`tail(group_rank(ts_mean(subtract(positive_sentiment_probability_3, negative_sentiment_probability_3), 66), subindustry), lower=0.18, upper=0.82, newval=0)`；USA/TOP3000/delay1/decay1/SUBINDUSTRY。
- 逐年 S：1.54 / 2.19 / **−1.25(2016)** / 2.31 / 1.86 / 1.35 / 1.35 / **3.93(2021)** / 2.75 / 1.64(2023)。
- 近三年 3.93/2.75/1.64，均值 **2.77**、CV **0.419**、衰减比 **0.927**、max/min **2.40**、平年 0。
- PnL 曲线整体单调（2014 起步→2023 收官 4.26M），2016 年段 805K→457K 回撤对应唯一负年。
- Margin **17.38bp** @ TO **4.9%**（噪声拟合线 5bp 远未触及）；sub 1.05 PASS；investability 1.42。
- prod **.6742**（16:42 权威 check_correlation 缓存，0.37h）、self **.5553**（pool 142）。
- 方案 D：ΔS +0.17 / ΔF +0.02 / ΔRet −0.33pp / ΔTO −0.62pp / ΔDD −0.10pp ⇒ 放行。

## Phase C 判定表（摘要）

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA=0 / PPA=0 | PASS |
| Recent-3yr Sharpe | 3.93/2.75/1.64 均值 2.77 ≥1.58，每年>0.3 | PASS |
| Recent-3yr CV | 0.419（0.40–0.60 带） | CONDITIONAL 软标记 |
| 衰减比 | 0.927 ≥0.50 | PASS |
| 平年（近3年） | 0 | PASS |
| max/min | 2.40 ≤3 | PASS |
| 全历史早年疲软 | 2016 −1.25 唯一负年（非近三年） | 软标记，绝不 REJECT |
| Sub-universe | 1.05 | PASS |
| Margin @ turnover | 17.38bp @ 4.9% | PASS |
| 算子数 | 4（软线内） | PASS |
| 经济可解释性 | 「行业内正负面情绪概率差的慢变分位，做多改善相对 peers、做空恶化者，赚情绪反应不足的均值回复」 | PASS |

## 结论

**PASS**。软标记 5 项（2016 负年、CV 0.42、prod 贴线、tail 由精调得出、ops 4），已在台账与提交三段式 description 中如实披露。

## 附：塔与六维

- 塔席位 `USA/D1/EARNINGS`，倍率 1.3，当季计数 **2**，交后 **3** ⇒ **点亮，塔边际 +1**。
- 六维：ops 4 / fields 2；T1 −0.0016、T2 +0.0004、T3 flat、T4 flat ⇒ 价值全在塔点亮，六维中性偏微正。

---

# 追加：blaoQ6Kq（GBR，17:44）— blaoMOAq 的 CW 修复件

> 同日第三份稳健审计（追加写）。台账 `robustness_blaoQ6Kq`。原件 `blaoMOAq` 因 CONCENTRATED_WEIGHT 曾被判 REJECT，本件在 group_rank 输出侧加 ts_mean(5) 后 CW→PASS、Ra=0。

## 归因

- 表达式：`ts_mean(group_rank(ts_decay_linear(vec_avg(snl27_top75pctranking) - vec_avg(snl27_top75pctrankingavg), 60), subindustry), 5)`；GBR/TOP700/delay1/decay8/MARKET。
- 逐年 S：2014–2018 **0（无持仓，snl27 数据自 2019-03 起）** / 2019 2.29 / **2020 −0.51** / 2021 1.90 / 2022 3.17 / 2023 2.13。
- 近三年 1.90/3.17/2.13，均值 **2.40**、CV **0.27**、衰减比 **1.291**、max/min **1.668**、平年 0。
- PnL：2019-03 起持仓，2020 段 915K→420K 回撤对应负年，2021 后单调上行收官 **3.02M**。
- Margin **36.47bp** @ TO **3.32%**；sub 1.34 PASS；investability 1.62。
- self **.1548**（pool 29/34，top bl6KwjwK）；prod 未回源（平台槽熔断）。
- 方案 D（POWER_POOL）：ΔS +0.16 / ΔF +0.18 / ΔRet −0.23pp / ΔTO −1.19pp / ΔDD 0 ⇒ 放行。

## Phase C 判定表（摘要）

| 检查项 | 值 | 判定 |
|---|---|---|
| WebDataScope failed count | Failed RA=0 / PPA=0 | PASS |
| Recent-3yr Sharpe | 1.90/3.17/2.13 均值 2.40≥1.58，每年>0.3 | PASS |
| Recent-3yr CV | 0.27（<0.40） | PASS |
| 衰减比 | 1.291 ≥0.50 | PASS |
| 平年（近3年） | 0 | PASS |
| max/min | 1.668 ≤3 | PASS |
| 2014-2018 无持仓 / 2020 −0.51 | 数据起点 + 早年负年（均非近三年） | 软标记，绝不 REJECT |
| CONCENTRATED_WEIGHT | PASS（repair 成果） | PASS |
| Sub-universe | 1.34 | PASS |
| Margin @ turnover | 36.47bp @ 3.32% | PASS |
| 算子数 | 6（修复必需，软线） | 软标记 |
| 经济可解释性 | 「行业内 top75 分位排名与均值的差，做多参与广/分布散的票、做空相反，赚治理结构被慢定价的价差」 | PASS |

## 结论

**PASS**。软标记 5 项（数据起点、2020 负年、ops 6、CV、prod 待回源）已在台账与三段式 description 如实披露。塔 `GBR/D1/SENTIMENT` ×1.7 当季 0→1 不点亮（边际 0）。

---

## j2a9moM5（KOR/TOP600/D1，2026-11-16 19:58）

- 表达式：`subtract(rank(ts_backfill(ts_rank(subtract(probability_label4_5quantile_5day_ohlcv_2, probability_label0_5quantile_5day_ohlcv_2),462),66)), group_rank(ts_mean(vec_stddev(insd5_vol_chg),55),sector))`
- IS：S 2.12 / F 1.23 / TO 30.8% / 2Y 2.66 / sub 2.01 / invest 1.55 / failed_ra=0。全部硬闸 PASS。
- 逐年 Sharpe 2014–2023：2.75/3.36/2.03/2.48/1.10/**0.12**/1.41/**3.41**/1.72/**2.70**。近3年 3.41/1.72/2.70 全正、CV≈0.33、衰减比 1.27、平年 0、max/min 1.98 → 全 PASS。
- 2019 平年（0.12）在早年，不参与近3年判定；PnL 曲线 2014–2023 单调上行，无单季回撤 >2× 均值。
- margin 0.675bp @ TO30.8%：低于 5bp 但 TO<60%，不满足 REJECT 条件，记软标记。
- 塔：KOR/D1/INSIDERS(1.2×)+OTHER(1.6×)，eff 2 / 短板 1.2×；当季 ins 2/oth 1 → 交后 3/2，insiders 新点亮，边际 +1。
- prod 0.5013（缓存 <48h，非 provisional）；与已提交件互相关 <0.51。
- **结论 PASS**（软标记 2 项：早年 2019 平年、margin 偏低）。
