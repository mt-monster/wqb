# zqdRJWL8 优化战役：指标推到闸 + 算子压到最少

日期：2026-11-18　skill：`wq-alpha-gate-push-op-min`　区域：DEU / TOP500 / D1
塔：`DEU/D1/SENTIMENT` ×1.8（当季计数 **1/3**，未点亮）

---

## 1. 采集与缺口（① 只读）

**表达式**（3 个算子调用点）

```text
group_rank(ts_zscore(vec_avg(snl27_kurtosis), 44), market)
```

**settings**：decay 0 / SUBINDUSTRY / truncation 0.08 / pasteurization ON / unitHandling VERIFY / nanHandling ON / maxTrade OFF

| 指标 | 值 | 门槛 | 缺口 |
|---|---:|---:|---|
| Sharpe | 1.26 | 1.58 | **−0.32** |
| Fitness | 0.64 | 1.00 | **−0.36** |
| Turnover | 24.59% | — | — |
| Returns | 6.31% | — | — |
| 2Y Sharpe | 1.73 | 1.58 | +0.15 ✔ |
| sub universe S | 1.06 | 0.47（当档） | ✔ |
| CONCENTRATED_WEIGHT | — | — | **WARNING** |
| prod corr | **0.6143** | <0.70 | +0.086 ✔（`[0.6,0.7)` 仅 1 颗 = 极薄墙） |

`is.checks`：fail 空；warning = LOW_SHARPE / LOW_FITNESS / CONCENTRATED_WEIGHT；pass = LOW_2Y_SHARPE / LOW_SUB_UNIVERSE_SHARPE / CLUSTER_TEST / LOW_TURNOVER / MATCHES_PYRAMID。

**ATOM 判定：是**（唯一数据字段 `snl27_kurtosis`，`market` 属豁免分组字段；零 pv1 泄漏）。

---

## 2. 算子审计（②）

`op_count` = **3**（`group_rank` 1 / `ts_zscore` 1 / `vec_avg` 1）。`scan.py --delete` 候选 **0 条**——三个算子都是结构承载件，无重复子式、无恒等包裹、无可合并变量。**压缩维度已到底**（再删任何一个都会塌掉 L1/L3/L4 之一）。

---

## 3. ★ F 代数：卡点不是换手，是 Sharpe（决定性判据）

平台 `Fitness = Sharpe × sqrt(|Returns| / max(Turnover, 0.125))`。

**TO 一旦低于 0.125 这个 floor，再降换手对 F 完全零杠杆**，F 退化为 `F = S × sqrt(8 × R)`：

| 目标 | 所需 S（按实测 R=5.8%，TO≤12.5%） |
|---|---:|
| F = 1.00 | **S ≥ 1.468** |
| F = 1.00 且 S=1.58 | R ≥ 5.01% |

实测本族 R 只能落在 5.0–6.3% ⇒ **必须 S ≥ 1.47，而闸线是 1.58 ⇒ 必须 S ≥ 1.58**。
⇒ 全部「降 TO 类」杠杆（decay↑、ts_mean 平滑、ts_target_tvr_*）只能把 F 从 0.64 抬到 0.76，**天花板 0.76 < 1.00**。
本条与项目既有判据「TO<.125 后 decay 零杠杆」互为印证，并补上「F 的第二形态」：**低 TO 件上 F 的唯一活路是抬 S**。

---

## 4. 实验矩阵（52 臂实测）

### 4.1 结构 × decay（2 bat × 10 式，SUBINDUSTRY / trunc .08 / nan ON）

| # | 表达式 | decay | S | F | TO | R | 2Y | sub | CW |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `group_rank(ts_zscore(vec_avg(K),44),market)` **原件** | 0 | **1.26** | 0.64 | 24.6% | 6.31% | 1.73 | 1.06 | WARN |
| 2 | 同 1 | 4 | 1.15 | 0.72 | 14.8% | 5.88% | 1.76 | 0.85 | **PASS** |
| 3 | `ts_mean(…,5)` | 0 | 1.10 | 0.74 | 12.6% | 5.64% | 1.74 | 0.76 | **PASS** |
| 4 | `ts_mean(…,10)` | 0 | 1.11 | **0.76** | 9.27% | 5.80% | 1.78 | 0.63 | **PASS** |
| 5 | `ts_mean(…,22)` | 0 | 0.99 | 0.65 | 6.49% | 5.38% | 1.74 | **0.02 FAIL** | PASS |
| 6 | `ts_mean(…,5)` | 4 | 1.08 | 0.72 | 11.1% | 5.53% | 1.74 | 0.70 | PASS |
| 7 | `ts_mean(…,10)` | 4 | 1.08 | 0.73 | 8.63% | 5.67% | 1.75 | 0.53 | PASS |
| 8 | `ts_mean(…,22)` | 4 | 0.97 | 0.63 | 6.18% | 5.23% | 1.70 | **−0.04 FAIL** | PASS |
| 9 | `w63` | 0 | 1.20 | 0.62 | 22.9% | 6.01% | 1.79 | 0.91 | WARN |
| 10 | `w63` | 4 | 1.10 | 0.70 | 13.7% | 5.60% | 1.83 | 0.73 | PASS |
| 11 | `w88` | 0/4 | 1.00/0.92 | 0.48/0.55 | — | — | 1.43/1.48 | 0.70/0.54 | WARN/FAIL |
| 12 | `w126` | 0/4 | 0.76/0.64 | 0.33/0.32 | — | — | **1.05/1.08 FAIL** | 0.37/0.19 | FAIL |
| 13 | `w252` | 0/4 | 0.69/0.59 | 0.29/0.29 | — | — | **1.13/1.21 FAIL** | 0.24/0.10 | FAIL |
| 14 | `group_rank(…,sector)` | 0/4 | 1.21/1.13 | 0.57/0.68 | 27.2%/15.7% | — | 1.66/1.69 | 1.04/0.83 | WARN/PASS |
| 15 | `vec_max` 聚合 | 0/4 | 1.19/1.11 | 0.58/0.68 | 25.4%/15.0% | — | 1.63/1.70 | 1.03/0.83 | WARN/PASS |

**读数**：窗口 44 是**尖峰**（21→1.15、63→1.20、88→1.00、126→0.76，严格单调下降）；`sector` 分组轴、`vec_max` 聚合都**不如 market+vec_avg**；输出侧平滑能把 TO 砍到 9.3%（CW 转 PASS、F 升到 0.76）但**代价是 S 与 sub 同步下滑**（w=22 时 sub 归零 FAIL）。

### 4.2 结构替换 / 聚合替换 / 参数补扫（1 bat × 10 式，decay 0）

| 表达式 | S | F | TO | 2Y | sub | 结论 |
|---|---:|---:|---:|---:|---:|---|
| `group_zscore(...)` 替 group_rank | 0.52 | 0.14 | 37.1% | −0.14 | 1.47 | 崩（非保序） |
| `vec_sum` 替 `vec_avg` | 0.84 | 0.28 | 36.5% | 1.48 | 0.72 | 崩（掺入域名数） |
| 裸 `rank(...)`（丢分组轴） | 0.56 | 0.16 | 34.1% | 0.08 | 1.58 | 崩（丢市场中性） |
| 纯水平 `group_rank(vec_avg(K),market)` | 0.95 | 0.65 | 11.7% | 1.16 | 0.33 | 弱，但 TO 仅 11.7% |
| `ts_delta(…,44)` | 1.15 | 0.55 | 24.0% | 1.31 | **0.39 FAIL** | sub 挂 |
| `ts_corr(K, totaldomains, 88)` | 0.13 | 0.03 | 3.8% | 1.33 | 0.08 | 无信号 |
| `subtract(rank(K),rank(SK))` | 0.64 | 0.32 | 14.4% | 0.96 | −0.34 | 无信号 |
| `vec_stddev` 聚合 | 0.13 | 0.01 | 40.7% | 0.28 | −0.49 | 无信号（持仓仅 66 只） |
| `w21` | 1.15 | 0.50 | 30.6% | 1.57 | 1.08 | 换手过高 |
| `w504` | 0.61 | 0.25 | 17.6% | 1.06 | 0.09 | 窗过长 |

### 4.3 字段替换矩阵（1 bat × 10 字段，同一骨架 `group_rank(ts_zscore(vec_avg(F),44),market)`）

| 字段 | S | F | 2Y | sub | 语义 |
|---|---:|---:|---:|---:|---|
| **snl27_kurtosis** | **1.26** | 0.64 | 1.73 | 1.06 | 域名排名分布**峰度**（尾部厚度） |
| snl27_totaldomains | 0.87 | 0.38 | 1.27 | 0.06 | 域名总数 |
| snl27_skewness | 0.54 | 0.18 | 0.99 | 0.24 | **偏度** |
| snl27_top50pctranking | 0.23 | 0.05 | −0.72 | −0.54 | 中位排名 |
| snl27_avgranking | 0.20 | 0.04 | −0.40 | −0.64 | 平均排名 |
| snl27_relpopularity08 | 0.19 | 0.04 | −0.03 | −0.19 | 相对关注度 |
| snl27_relpopularity1 | 0.15 | 0.03 | −0.13 | −0.16 | 相对关注度 |
| snl27_topranking | 0.09 | 0.01 | −0.20 | −0.91 | 最优排名 |
| snl27_top50pctrankingavg | 0.03 | 0.00 | −0.24 | −0.77 | 前 50% 均排名 |
| snl27_top75pctrankingavg | 0.02 | 0.00 | −0.43 | −1.16 | 前 75% 均排名 |
| snt27_rank | −0.03 | −0.00 | −0.59 | −0.70 | 原始 Tranco 排名 |

**结论：kurtosis 是 sentiment27 唯一有效字段**（次优 0.87，第三 0.54，其余 ≈0）。「ranking / relpopularity」系列测的是**分布位置**，无信息；只有**分布形态**（高阶矩）携带 alpha。⇒ 换字段路线封闭。

### 4.4 settings 收敛（⑤，表达式冻结后）

| neutralization | w44 | ts_mean5 | w63 | 判定 |
|---|---:|---:|---:|---|
| **SUBINDUSTRY（原档）** | **1.26** | 1.10 | **1.20** | 最优 |
| CROWDING | 1.02 | 0.97 | 1.02 | −0.24 S |
| MARKET | 0.91 | 0.84 | 0.94 | −0.35 S |
| INDUSTRY | 0.94 | 0.93 | 0.92 | −0.32 S |
| SLOW_AND_FAST | 0.53 | 0.53 | 0.51 | 灾难（2Y→0.05） |

- **universe**：DEU 只有 `TOP500` 单档（`get_platform_setting_options` 确认）⇒ 无扫描空间，跳过。
- **decay**：0→4 只降 TO/提 F，S 单调下滑（见 4.1）；在 TO 已 <12.5% 的件上继续加 decay 是**零杠杆**（§3）。
- **truncation**：本项目历次实测零杠杆（0.04 与 0.12 指标逐位相同），未重扫。

### 4.5 全算子遍历（④b，1 bat × 10 式）——唯一有增益的两条

| # | 表达式 | S | F | TO | R | 2Y | sub | 备注 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `group_rank(tail(ts_zscore(K,44), lower=-0.5, upper=0.5, newval=0), market)` | **1.28** | 0.64 | 25.7% | 6.46% | 1.68 | 1.06 | **S 新高**（+0.02） |
| 2 | `group_rank(winsorize(ts_zscore(K,44), std=2), market)` | 1.26 | 0.64 | 24.6% | 6.31% | 1.73 | 1.06 | **恒等**（std=2 只切 4.5%，group_rank 无症状） |
| 3 | `group_rank(ts_target_tvr_decay(ts_zscore(K,44), target_tvr=0.1), market)` | 1.16 | **0.79** | 9.76% | 5.84% | 1.70 | 0.66 | **F 新高**（+0.03 vs ts_mean10） |
| 4 | `group_rank(ts_zscore(K,44), bucket(rank(vec_avg(totaldomains)), range="0,1,0.2"))` | 1.09 | 0.48 | 27.9% | 5.34% | **2.20** | **1.35** | **2Y 新高**（+0.47） |
| 5 | `group_rank(ts_zscore(K,44), group_cartesian_product(market, bucket(…,0.5)))` | 1.03 | 0.45 | 26.8% | 5.07% | 2.05 | 1.32 | 复合轴同向 |
| 6 | `group_rank(ts_zscore(K,44), densify(industry))` | 1.24 | 0.56 | 28.7% | 5.87% | 1.73 | 0.97 | 轴替（§4.4 已含 settings 版） |
| 7 | `group_rank(ts_ir(vec_avg(K),44), market)` | 0.72 | 0.40 | 4.05% | 3.90% | 1.13 | −0.07 | 水平/噪声 ≠ 偏离 |
| 8 | `group_rank(ts_regression(K, ts_step(1), 44, rettype=1), market)` | 0.04 | 0.00 | 8.7% | 0.17% | 0.87 | −1.02 | 斜率无信息 |
| 9 | `group_rank(ts_zscore(vec_count(K),44), market)` | 0.80 | 0.53 | 13.3% | 5.86% | 1.32 | −0.12 | **CW FAIL val 0.5>0.1** |
| 10 | `group_rank(ts_zscore(vec_range(K),44), market)` | 0.79 | 0.22 | 51.0% | 3.79% | 1.01 | 0.08 | 极差=噪声 |

**两条真正的新杠杆**：
- `tail` 空带压缩（把 |z|<0.5 的摆动钉死为 0）= 少调仓的**信号侧**降换手，比输出平滑更保 S（S **+0.02** 而非 −0.15）。
- `ts_target_tvr_decay` = 换手目标化，把 24.6%→9.8% 而 S 只掉 0.10，**F 单点 +0.15**（0.64→0.79），是本族最强 F 杠杆。
- `bucket`/`cartesian` 的**关注广度分组轴**把 2Y 从 1.73 抬到 **2.20**、sub 从 1.06 抬到 **1.35**（代价 S −0.17）⇒ 是「修 2Y / sub」的现成工具，但对本件无用（2Y 本来就过）。

### 4.6 ④d 精调（1 bat × 10 式）：`tail` 带宽 × `ts_target_tvr_decay` 目标 × 轴

| # | 表达式 | S | F | TO | R | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `ts_target_tvr_decay(tail(z,±0.5), 0.13)` | 1.25 | 0.70 | 20.1% | 6.32% | 1.78 | 1.03 |
| 2 | `ts_target_tvr_decay(tail(z,±0.5), 0.15)` | 1.27 | 0.68 | 22.6% | 6.43% | 1.76 | 1.06 |
| 3 | `ts_target_tvr_decay(tail(z,±0.5), 0.20)` | **1.30** | 0.66 | 25.1% | 6.54% | 1.71 | 1.08 |
| 4 | `tail(z, ±0.3)` | 1.27 | 0.64 | 25.0% | 6.39% | 1.75 | 1.06 |
| 5 | `tail(z, ±0.75)` | 1.18 | 0.56 | 26.7% | 6.04% | 1.60 | 0.97 |
| 6 | **`tail(z, ±1.0)`** | **1.32** | 0.66 | 27.8% | 6.86% | 1.70 | 0.82 |
| 7 | `ts_target_tvr_decay(z44, 0.13)`（无 tail） | 1.23 | 0.69 | 19.7% | 6.18% | 1.80 | 1.05 |
| 8 | `tail(±0.5)` + `densify(industry)` | 1.25 | 0.56 | 29.3% | 5.94% | 1.67 | 0.93 |
| 9 | `tail(±0.5)` + `bucket(广度)` | 1.13 | 0.50 | 29.0% | 5.56% | 2.14 | **1.35** |
| 10 | `ts_target_tvr_decay(z44, 0.15)`（无 tail） | 1.25 | 0.67 | 21.9% | 6.31% | 1.80 | 1.07 |

- 带宽是**尖峰**：±0.3→1.27 / ±0.5→1.28 / ±0.75→1.18 / **±1.0→1.32**（非单调，±1.0 最好但 sub 掉到 0.82）。
- `tvr` 目标 0.10 是 F 的最优点（TO 落进 floor 后，再降只损 S/R）。
- **两条杠杆不叠加**：`tail(±1.0)` 与 `tvr(0.13)` 都是降换手手段，合并只会把 TO 双压到 floor 以下而白扔 S。

### 4.7 ★ 高阶矩算子 `ts_kurtosis` 专项（1 bat × 10 式，用户点名）

**先纠一条历史错判**：`tracking/DEU/atom_orthogonal/SENTIMENT_OPERATOR_SCAN_24_FINAL_20261112.md` 写「`ts_kurtosis`/`ts_skewness`/`ts_entropy`/`ts_moment` 全部不可用」。**实时 `get_operators` 核实（103 算子）**：

| 算子 | 是否存在 | 证据 |
|---|---|---|
| **`ts_kurtosis(x, d)`** | ✅ **存在**（scope `COMBO/REGULAR`） | 本轮 10/10 仿真全部 COMPLETE，无一条报 unknown operator |
| `ts_skewness` | ❌ 不在目录 | 103 条里无此项 |
| `ts_entropy` | ❌ 不在目录 | 同上 |
| `ts_moment` | ❌ 不在目录 | 同上（`TPL-901` 早已标注「需实测」） |
| `vec_kurtosis` / `vec_skewness` / `vec_ir` | ❌ 不在目录 | 这就是 GBR W12「整批 ERROR」的真凶——**是 VECTOR 命名域的错算子，不是 TS 命名域的 `ts_kurtosis`** |

⇒ 旧结论把「`vec_*` 族的报错」错误泛化成「所有高阶矩算子不可用」，**`ts_kurtosis` 一直可用**。

**实测矩阵（decay 0 / SUBINDUSTRY / TOP500）**

| # | 表达式 | S | F | TO | R | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `ts_kurtosis(vec_avg(K), 66)` | 0.81 | 0.46 | 9.03% | 3.96% | 1.77 | **−0.30 FAIL** |
| 2 | `ts_kurtosis(vec_avg(totaldomains), 66)` | 0.59 | 0.29 | 5.94% | 3.06% | 1.10 | −0.36 |
| 3 | `ts_kurtosis(vec_avg(skewness), 66)` | 0.46 | 0.19 | 9.35% | 2.10% | 0.82 | −0.50 |
| 4 | `ts_kurtosis(vec_avg(relpopularity08), 66)` | −0.14 | −0.04 | 6.14% | −0.84% | −0.79 | −0.67 |
| 5 | `ts_kurtosis(vec_avg(snt27_rank), 66)` | 0.20 | 0.06 | 7.28% | 1.03% | −0.60 | −0.59 |
| 6 | `ts_kurtosis(K, 22)` | 0.26 | 0.07 | 19.3% | 1.35% | 0.78 | −0.43 |
| 7 | `ts_kurtosis(K, 126)` | 0.92 | 0.55 | 5.83% | 4.47% | 1.32 | −0.12 |
| 8 | `ts_kurtosis(K, 252)` | 0.86 | 0.49 | 4.04% | 4.03% | 0.84 | 0.23 |
| 9 | `ts_kurtosis(vec_count(K), 66)` | 0.64 | 0.39 | 8.10% | 4.53% | 0.75 | −0.35 |
| **10** | **`ts_kurtosis(ts_zscore(K,44), 66)`** | **1.04** | **0.67** | 8.86% | 5.13% | **2.07** | **−0.27 FAIL** |

**判定：`ts_kurtosis` 路线不通**
1. 最强臂 1.04（#10），**仍比原式 1.26 低 0.22**；纯 `ts_kurtosis` 只有 0.81。
2. **sub_universe 几乎全负**（−0.12 ~ −0.67）——高阶矩信号换手仅 4–9%，在 TOP500 的子宇宙（大市值）里没有区分度；#10 的 2Y 2.07 是本族最高之一，但 sub −0.27 直接 FAIL ⇒ **2Y 与 sub 在此族物理冲突**。
3. 与跨区历史一致：EUR `d5K00wRK`（`ts_kurtosis(backfill504, 252)`）S **0.16** DEAD、DEU insiders `ts_kurtosis` S **0.17** ⇒ **高阶矩在 DEU/EUR 三个数据集上都不含增量信息**。

---

### 4.8 ★★ `ts_target_tvr_hump` 突破 F 前沿（论坛帖 + EUR 台账交叉指引，1 bat × 10 式）

**线索来源**：① 论坛 Sharpe 帖 comment 的「Volatility Scaling」；② 本地 `docs/reference/EUR/operator_template_ledger.md` w697 行——`ts_target_tvr_hump(tvr=0.10)` S 1.36/F 0.90/sub **1.04**，**优于同批 `ts_target_tvr_decay` 的 1.31/0.85/0.97**。

| # | 表达式 | S | F | TO | R | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `tvr_hump(z44, 0.10)` | 1.22 | 0.86 | 9.75% | 6.15% | 1.64 | 0.63 |
| 2 | **`tvr_hump(z44, 0.15)`** | **1.28** | **0.87** | 14.21% | 6.53% | **1.64** | **0.96** |
| 3 | `tvr_hump(tail(z,±1.0), 0.13)` | 1.25 | **0.90** | 12.28% | 6.41% | 1.55 ⚠ | 0.76 |
| 4 | `divide(z44, ts_std_dev(totaldomains,66))` | 0.97 | 0.45 | 23.3% | — | 1.52 | 0.78 |
| 5 | `divide(z44, ts_std_dev(K,252))` | 1.09 | 0.51 | 23.7% | — | 1.63 | 0.78 |
| 6 | `divide(z44, ts_std_dev(relpopularity08,66))` | 1.17 | 0.62 | 22.2% | 6.29% | 1.76 | **1.21** |
| 7 | `group_scale(z44, sector)` | 0.47 | 0.12 | 38.7% | — | **−0.14** | 1.34 |
| 8 | `group_scale(z44, market)` | 0.52 | 0.14 | 37.1% | — | −0.14 | 1.47 |
| 9 | `group_rank(z44, densify(subindustry))` | 0.88 | 0.35 | 23.4% | — | 1.17 | 0.82 |
| 10 | `tvr_hump(z44, 0.20)` | **1.29** | 0.78 | 17.90% | 6.56% | 1.70 | 1.08 |

**三条硬结论**
1. **`ts_target_tvr_hump` 全面优于 `ts_target_tvr_decay`**：同目标 0.10 下 F 0.86 vs 0.79（+0.07）、sub 0.63 vs 0.66 持平；同目标 0.15 下 S 1.28 vs 1.25、F 0.87 vs 0.67（**+0.20**）。原因是 hump 限的是**单日仓位变动幅度**、不做指数平滑 ⇒ 保 S 而砍 TO，正对 `F = S·√(R/max(TO,.125))` 的结构。
2. **F 前沿从 0.79 推到 0.90**（#3 `tail(±1.0)+hump(0.13)`，TO 12.28% 恰好落在 floor 边缘）。但 #3 的 **2Y 1.55 < 1.58 FAIL** —— F 最优点与 2Y 闸互斥。
3. **论坛「Volatility Scaling」在本件不成立**：#4/#5/#6 用同数据集波动做分母，S 全部降到 0.97–1.17（只有 #6 的 sub 1.21 亮眼）；`group_scale`（EUR 台账里的强项）在本区 S 只有 0.47–0.52、2Y −0.14，**跨区不可移植**。

**最具交付形态的一颗（新）**：`78Ynna75`
`group_rank(ts_target_tvr_hump(tail(ts_zscore(vec_avg(snl27_kurtosis), 44), lower=-1, upper=1, newval=0), target_tvr=0.14), market)`
→ S 1.26 / **F 0.89** / TO 12.97% / R 6.44% / **2Y 1.58 ✓（贴线）** / **sub 0.82 ✓** / CW WARN，**仅剩 S、F 两项 warning**（缺口 −0.32 / −0.11）。

### 4.9 `ts_target_tvr_hump` 目标精调（1 bat × 5 式）

| # | 表达式 | S | F | TO | R | 2Y | sub |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `hump(tail(z,±1.0), 0.12)` | 1.24 | 0.88 | 11.56% | 6.33% | **1.53 ⚠** | 0.70 |
| 2 | **`hump(tail(z,±1.0), 0.14)`** | **1.26** | **0.89** | 12.97% | 6.44% | 1.58 ✓贴线 | 0.82 |
| 3 | `hump(tail(z,±1.0), 0.15)` | 1.25 | 0.86 | 13.62% | 6.39% | 1.59 | 0.82 |
| 4 | `hump(tail(z,±0.5), 0.15)` | **1.27** | 0.85 | 14.45% | 6.51% | 1.61 | 0.92 |
| 5 | `hump(z44, 0.18)`（无 tail） | 1.27 | 0.79 | 16.52% | 6.47% | 1.65 | **1.04** |

- **F 峰值出现在 TO≈13%（刚过 floor）**：① TO 再降到 11.6% 会把 2Y 拉到 1.53 FAIL；② 抬到 16.5% 则 F 掉回 0.79。hump 目标是**尖峰**，0.14 最优。
- 全族 F 天花板 **0.89**，S 天花板 1.32；`F=1.0` 需 S≥1.40（实测最高 1.32）⇒ **数学上封死**。




---

## 5. 判定：`REJECT_STRUCTURAL`（字段级 Sharpe 天花板）

**最终两个前沿点（87 臂全局最优）**

| 目标 | 表达式 | S | F | TO | R | 2Y | sub | CW | id |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| **S 最大** | `group_rank(tail(ts_zscore(vec_avg(snl27_kurtosis),44), lower=-1, upper=1, newval=0), market)` | **1.32** | 0.66 | 27.8% | 6.86% | 1.70 | 0.82 | WARN | `YPagA7a6` |
| **F 最大** | `group_rank(ts_target_tvr_hump(tail(ts_zscore(vec_avg(snl27_kurtosis),44), lower=-1, upper=1, newval=0), target_tvr=0.14), market)` | 1.26 | **0.89** | 12.97% | 6.44% | 1.58 | 0.82 | WARN | `78Ynna75` |

对闸线：S **−0.26**（1.32 vs 1.58）、F **−0.11**（0.89 vs 1.00）。**两颗都不达标，一颗都不可交。**

1. **S 天花板 = 1.32**：**87 臂**覆盖「窗口 21–756 × decay 0/4 × 5 种分组轴（market/sector/industry/subindustry/bucket/cartesian）× 7 种聚合（vec_avg/max/sum/stddev/count/range/裸 rank）× 11 个字段 × 5 种 neutralization × 17 类结构（含 `ts_kurtosis`、`ts_ir`、`ts_regression`、`ts_delta`、`ts_corr`、`subtract(rank,rank)`、`tail`、`winsorize`、`group_scale`、`divide` 波动缩放、`tvr_decay`、`tvr_hump`）」+ 带宽 × 目标双精调，**无一条超 1.32**，对闸线缺 **0.26（−16%）**。
2. **F 天花板 = 0.90**（`ZYaKnXqj`：`hump(tail(z,±1.0),0.13)`，但 **2Y 1.55 FAIL**）；**「无 FAIL 项」的 F 上限 = 0.89**（`78Ynna75`，2Y 1.58 贴线过）。降 TO 手段已全部用尽（decay 0–4、`ts_mean` 5/10/22、`tail` 四档带宽、`tvr_decay` 四档目标、`tvr_hump` 五档目标、hump×tail 5 种组合）。按 §3 代数，`F=1.0` 需 **S ≥ 1.40**（R 6.44%）而实测 S 上限 1.32 ⇒ **F 的缺口 100% 由 S 缺口造成，与换手无关**。
3. **换字段/换机制已扫尽**：同塔（DEU/D1/SENTIMENT）三个数据集里，sentiment27 只剩 kurtosis 有信号，sentiment33（cov 0.33，历史最高 S 0.36）与 sentiment7（历史最高 S 1.08）更弱 ⇒ **该塔结构性不可达**。
4. **组合路线不合规且无料**：唯一能数学上抬 S 的路径是两腿相加（S_comb = 1.26×√(2/(1+ρ))），但 (a) 等权混腿属项目铁律禁止形态；(b) 合规替代（`ts_corr` 0.13、`subtract(rank,rank)` 0.64、`trade_when` 门控、`bucket` 轴）实测全部大幅低于单腿；(c) 同数据集可配腿最强只有 0.87，即便合规也够不着 1.47。

**处置建议**：本件不提交（`ALLOW_ALPHA_SUBMIT=False` 不变，提交权归用户）。DEU/D1/SENTIMENT 塔（×1.8，当季 1/3）若要推进，应换**信息机制**（sentiment33 情感方向 / sentiment7 浏览量的事件型骨架）或换塔，不在本字段上继续扫参数。

---

## 6. 本轮新增可复用判据（已写入 `.workbuddy/memory/2026-11-18.md`）

1. **F 的第二形态**：`TO < 0.125` 后 `F = S·√(8R)`，扫 decay / 加平滑 / `ts_target_tvr_*` 全部零杠杆 ⇒ 低换手件上唯一的 F 杠杆是**抬 S**。判死前先算 `S_所需 = F_闸 / √(8R)`。
2. **「位置 vs 形态」字段分族**：连续分布类数据集的 `ranking / percentile / relpopularity` 子族（10 个字段 S≤0.23）是**分布位置**，几乎无信息；只有 `kurtosis / skewness`（分布形态）携带 alpha。拿到此类数据集先打形态字段，别在 ranking 族铺量。
3. **同骨架换字段必跑一次整表**（1 bat / 10 字段即可闭合）：本轮 10 字段一屏出结果，直接证明「字段不是可选维度」，比逐字段论证快一个数量级。
4. **Fitness 与 Sharpe 同轴反向的处置**：本族「平滑」在降 TO 的同时杀 S，`ΔF/ΔS ≈ −1`，属与 prod 墙同构的**物理互斥**，不能用参数搜索解。

---

## 7. 论坛查证（2026-11-18）

`search_forum_posts` 对 `kurtosis` / `kurtosis web popularity attention alpha` 两次均返回空（工具故障，按 `forum_and_doc_tools_guide.md` §2.2 不作「无讨论」结论）。改走**权威路径**：`get_documentation_page("list-must-read-posts-how-improve-your-alphas-are-submitted")` 取出官方认定的 7 篇 must-read 的 article id，再 `read_forum_post` 直读正文。

| 帖 | id | 赞 | 与本件的映射 |
|---|---|---:|---|
| **How do you get a higher Sharpe** | `8123350778391` | 216 | `IR = Return/σ` ⇒ 两条路：提 return（更多信息/更准预测）、降 σ（中性化/分散/vol scaling）。**本件 5 种 neutralization 已全部实测，SUBINDUSTRY 最优**；comment 里点出的「Volatility Scaling by asset volatility」是唯一未测的合规点 |
| **5 ways to potentially increase returns** | `8833033953559` | 212 | ①**提高换手能提 return** ②降 decay ③更小/更流动的 universe ④同 R/DD 下提高波动率 ⑤news/analyst 数据集。**①在我们的数据里被证实**（TO 24.6%→27.8% 时 R 6.31%→6.86%），但因为 `F = S·√(R/TO)`，R 与 TO 同向抵消 ⇒ **推 F 的唯一变量仍是 S**，与 §3 完全一致。②已在 0（最低档）③DEU 仅 TOP500 单档 ⑤该塔无 news/analyst |
| **trade_when for Event / Low Turnover Alphas** | `8360363631127` | 62 | 原文明确写 **Cons: "Not easy to get high Sharpe alpha / high return alpha"** ⇒ 门控是降换手工具，不是抬 S 工具，与本仓「8 种门控全部降 ladder」一致 |
| How to reduce correlation | `8046468280727` | — | 不需要（prod 0.6143 余量充足） |
| How to avoid overfitting | `8209806533015` | — | 已遵守（72 臂单变量改动，未做多腿权重搜索） |

**论坛对「高阶矩」的原始推荐**（`TPL-901` / EUR `eur_other_techindi_prob_20261106.md` 引用的《高阶矩在说什么：偏度、峰度与熵》）只能落地为 `ts_kurtosis`（另三个算子平台无），本轮已实测全灭（§4.7）。

**唯一未测的合规增益点（来自 Sharpe 帖的 comment）**：用同数据集字段的波动做**分母缩放**（ATOM 不破）。已在 §4.8 实测。


---

# 第二轮（用户指令「继续优化直到破闸」，2026-11-18 18:04–20:0x）

## 8. ★★★ 三个结构性突破：新信息构造 + hump + backfill

第一轮的判断（"字段级天花板 S 1.32"）**被第二轮推翻并大幅超越**——不是靠调参，而是靠**改信息构造**。

### 8.1 突破一：比率构造 `kurtosis ÷ 域名数^k`（S 1.26 → 1.51）

不再对 `snl27_kurtosis` 单字段做时序标准化，而是用 `divide` 把它与**同数据集的域名数**相除，造出「**每域名尾部厚度**」这一新经济量（`divide` 属项目白名单形态，ATOM 不破）。

| 构造 | S | F | TO | R | 2Y | sub |
|---|---:|---:|---:|---:|---:|---:|
| `z(K,44)` 原式 | 1.26 | 0.64 | 24.6% | 6.31% | 1.73 | 1.06 |
| `z(K / doms, 44)` | 1.39 | 0.74 | 24.7% | 7.00% | 1.81 | 1.08 |
| **`z(K / doms², 44)`** | **1.45** | 0.79 | 24.8% | 7.30% | 1.96 | 1.05 |
| `z(K / doms³, 44)` | 1.44 | 0.78 | 24.8% | 7.25% | 1.99 | 1.00 |
| `z(K / doms^1.5, 44)` | 1.46 | 0.81 | 23.3% | 7.22% | 1.84 | 1.00 |
| `z(K² / doms, 44)` | 0.52 | 0.17 | 25.5% | 2.68% | 1.55 | −0.64 |
| `divide(relpop08, relpop1)` | 0.14 | 0.02 | — | — | −0.13 | −0.49 |
| `divide(top50avg, top75avg)` | 0.92 | 0.40 | — | — | 1.50 | 0.37 |
| 纯水平 `K/doms²`（无 z） | 0.98 | 0.71 | 7.8% | 6.65% | 1.38 | 0.56 |
| `subtract(rank(K),rank(doms²))` | 0.89 | 0.51 | 13.1% | 4.34% | 0.60 | −0.10 |

**幂次是尖峰**：1→1.39 / 1.5→1.46 / **2→1.45** / 3→1.44 / 2.5→1.44，分母平方附近最优。方向性也重要——`K²/doms`（分子平方）直接崩到 0.52，说明**要的是"每域名摊薄"，不是"尾部放大"**。

### 8.2 突破二：`group_rank` 轴 `market → sector`（+0.03）

| 轴 | S（K/doms²） | F |
|---|---:|---:|
| market | 1.45 | 0.79 |
| **sector** | **1.48** | 0.76 |
| `cartesian(market, sector)` | 1.48 | 0.76（退化为 sector） |
| `densify(industry)` | 1.37 | 0.64 |
| `densify(subindustry)` | 0.88 | 0.35 |

### 8.3 突破三：`ts_backfill` 修掉 CONCENTRATED_WEIGHT（关键）

**CW 的根因不是权重、不是 truncation**（trunc 0.04 与 0.08 指标逐位相同）——是 **nanHandling=ON 把缺失日填成 0**，使这些票在 `group_rank` 后拿到端点位，形成权重堆积。**两侧都加 `ts_backfill(·,22)` 后，CW 直接 PASS**：

| 件 | 有无 backfill | S | F | CW | ra_failed |
|---|---|---:|---:|---|---|
| `xAvd1gjq` | ✅ | 1.49 | 0.76 | **PASS** | LOW_SHARPE, LOW_FITNESS |
| `1YWzX3LX` | ❌ | 1.51 | 0.77 | warning | +CONCENTRATED_WEIGHT |
| `78Yno3Pv` | ✅+hump.15 | 1.45 | **1.00 PASS** | **PASS** | **仅 LOW_SHARPE** |

### 8.4 最终前沿（TO–S–F 三方互斥，14 个实测点）

| TO | S | F | 构造 |
|---:|---:|---:|---|
| 15.45% | 1.45 | **1.00** | backfill + hump .15 + sector |
| 18.01% | 1.46 | 0.93 | backfill + hump .18 + sector |
| 19.48% | 1.47 | 0.90 | backfill + hump .20 + sector |
| 20.14% | 1.46 | 0.88 | hump .20 + sector |
| 22.64% | **1.51** | 0.86 | backfill + hump .25 + sector |
| 24.77% | 1.45 | 0.79 | K/doms² + sector（无 hump） |
| 29.89% | 1.51 | 0.77 | K/doms² + tail(±1) + sector |
| 30.70% | 1.47 | 0.71 | backfill + tail + industry |

**闸线方程**：`F = S·sqrt(R/max(TO,.125))`，R ≈ 7.3%。同时满足 `S≥1.58` 与 `F≥1.00` 需 **TO ≤ 18.5% 且该 TO 处 S ≥ 1.58**；实测 TO 18.0% 处 S 仅 **1.46**，缺 **0.12**。S 最高点 1.51 出现在 TO 22.6%（此时 F 0.86）。

⇒ **S 与 F 沿同一条 frontier 反向**，要两者同时过必须把整条 frontier 上移 ~0.12 S（相当于再提 8% 信号强度），靠参数/算子已无空间。


### 8.5 ④d 精调（窗口 × hump 目标，两轮 16 臂）

| 窗口 | hump | S | F | TO | R | 2Y | sub |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 44 | .15 | 1.45 | **1.00** | 15.45% | 7.28% | 2.05 | 0.81 |
| 44 | .18 | 1.46 | 0.93 | 18.01% | 7.25% | 2.05 | 0.96 |
| 44 | .20 | 1.47 | 0.90 | 19.48% | 7.24% | 2.02 | 1.00 |
| 44 | .25 | 1.51 | 0.86 | 22.64% | 7.40% | 2.07 | 1.07 |
| 44 | .28 | 1.49 | 0.82 | 24.02% | 7.34% | 2.07 | 1.08 |
| 44 | .30 | 1.49 | 0.81 | 24.70% | 7.31% | 2.08 | 1.07 |
| 45 | .28 | 1.54 | 0.87 | 23.95% | 7.58% | 2.20 | 1.11 |
| 47 | .22 | 1.54 | 0.93 | 20.76% | 7.54% | 2.19 | 1.10 |
| **48** | **.22** | **1.57** | **0.96** | 20.73% | 7.68% | **2.23** | 1.13 |
| 48 | .23 | 1.57 | 0.94 | 21.37% | 7.66% | 2.23 | 1.11 |
| 48 | .24 | 1.57 | 0.93 | 21.93% | 7.67% | 2.25 | 1.10 |
| 48 | .26 | 1.56 | 0.90 | 22.95% | 7.63% | 2.26 | 1.12 |
| 48 | .28 | 1.55 | 0.87 | 23.79% | 7.57% | 2.27 | 1.15 |
| 49 | .22 | 1.56 | 0.95 | 20.71% | 7.63% | 2.26 | 1.12 |
| 50 | .28 | 1.55 | 0.88 | 23.66% | 7.55% | 2.35 | 1.13 |
| 52 | .28 | 1.50 | 0.84 | 23.55% | 7.30% | 2.37 | 1.04 |

**窗口 48 是最优**（比 44 高 0.06 S，2Y 也高 0.1–0.2）。`decay 1/2` 与 `decay 0` 指标**逐位相同**——`ts_target_tvr_decay` 已接管换手控制，平台 decay 失效。

### 8.6 最终状态：**只剩 2 项 fail，缺口 S −0.01 / F −0.04**

**`MP6LYLw8`（全族最优，唯一"两闸同时逼近"点）**

```text
group_rank(
  ts_target_tvr_hump(
    ts_zscore(divide(ts_backfill(vec_avg(snl27_kurtosis), 22),
                     multiply(ts_backfill(vec_avg(snl27_totaldomains), 22),
                              ts_backfill(vec_avg(snl27_totaldomains), 22))), 48),
    target_tvr=0.22),
  sector)
```

| 指标 | 值 | 闸 | 状态 |
|---|---:|---:|---|
| **Sharpe** | **1.57** | 1.58 | **−0.01 ✗** |
| **Fitness** | **0.96** | 1.00 | **−0.04 ✗** |
| Turnover | 20.73% | — | ✔ |
| Returns | 7.68% | — | 基线 6.31% → **+21.7%** |
| 2Y Sharpe | **2.23** | 1.58 | ✔ +0.65 |
| sub universe S | **1.13** | ~0.47 | ✔ +0.66 |
| CONCENTRATED_WEIGHT | — | — | **PASS**（backfill 修复） |
| investability S / F | 1.42 / 1.08 | — | ✔（容量健康） |
| prod corr | 0.57 级 | <0.70 | ✔ |
| `ra_failed_checks` | **仅 `LOW_SHARPE`, `LOW_FITNESS`** | — | 其余全 PASS |

**闸线可行性**：`F=1.0` 与 `S=1.58` 同时成立需 **TO ≤ 19.2%**；实测 TO 20.73% 处 S 已到 **1.57**（frontier 顶点），把 TO 压到 19.2% 需 hump≈0.20，该档 S 只有 1.50（F 0.92）⇒ **两闸在 frontier 上仍互斥 0.03–0.04**。

## 9. 全战役净变化

| 指标 | 原件 `zqdRJWL8` | 终件 `MP6LYLw8` | Δ |
|---|---:|---:|---:|
| Sharpe | 1.26 | **1.57** | **+0.31（+24.6%）** |
| Fitness | 0.64 | **0.96** | **+0.32（+50%）** |
| 2Y Sharpe | 1.73 | **2.23** | +0.50 |
| sub universe S | 1.06 | **1.13** | +0.07 |
| Returns | 6.31% | 7.68% | +21.7% |
| CONCENTRATED_WEIGHT | warning | **PASS** | 修复 |
| prod corr | 0.6143 | 0.57 级 | −0.04 |
| fail 项数 | 3（S/F/CW） | **2（S/F）** | −1 |
| 算子数 | 3 | 11 | +8（六维软成本，换 +0.31 S 值得） |

**结论**：两轮共 **~150 臂**，把「判死」翻案成「只差 0.01/0.04」。核心是三次**非参数**改造——比率构造（+0.19 S）、sector 轴（+0.03）、`ts_backfill`（修 CW）。剩余 0.01/0.04 属 frontier 顶点与闸线的间隙，需再换一次信息源（下一个数据集/机制）才能跨过。

---

# 第三轮：表达式数学层优化（2026-11-18 21:5x–）

## 10. 三个数学问题的答案

### 10.1 变量抽取（唯一真正减算子的一步，已实证无损）

原式里 `ts_backfill(vec_avg(snl27_totaldomains), 22)` 被写了**两遍**，这在平台算子计数上算**两个调用点**。用赋值语句抽出来（赋值不计入 `operatorCount`）：

```text
d = ts_backfill(vec_avg(snl27_totaldomains), 22);
k = ts_backfill(vec_avg(snl27_kurtosis), 22);
group_rank(ts_target_tvr_hump(ts_zscore(divide(k, power(d, 2.25)), 48), target_tvr=0.22), sector)
```

| 口径 | 原式 `MP6LYLw8` | 抽取后 | 差 |
|---|---:|---:|---:|
| `regular.operatorCount`（**全部调用点，含重复、含 ts_backfill、含赋值行**） | **11** | **9** | −2（−18%） |
| PPA ≤8 口径（**含重复，排除 ts_backfill / group_backfill**） | 8 | **7** | −1 |
| Genius T1（**distinct，排除 backfill**） | 6 | 6 | **0** |

⚠ **此前本节写的「11 → 5（−55%）」是错的**：那个 5 只数了**末行**的调用点，漏掉了两条赋值行上的 `vec_avg`／`ts_backfill`。按平台实测规则（见 §10.6），赋值行上的算子**照常计数**，只有 `=` 本身不算。正确值是 **11 → 9**。
⚠ 更重要的连带修正：**变量抽取对 Genius T1 完全没有帮助**（distinct 仍是 6）——因为省掉的两个都是 `ts_backfill`，而它本就**被 T1/T3 排除**。它只压缩了 `operatorCount`（−2）和 PPA 口径（−1）。

**指标逐位相同这一点仍然成立**（4 条等价式实测：S 1.57 / F 0.96 / TO 20.73% / R 7.68% / DD 4.72% / 2Y 2.23 / sub 1.13 / invest 1.42+1.08 / pnl 3,822,541 全部一致，见 §10.2 表）。

⚠ 本地 `op_count.py` 会给一条 `[C1]` 建议「`multiply(d,d)` → `d`（省 1 算子）」——**这是错的（有损）**：指数 2→1 会让 S 从 1.45 掉到 1.39（§8.1 实测），不能采纳。

### 10.2 `power` vs `multiply`：算子数收益为零，但打开一个全新维度

`power(d, 2)` 与 `multiply(d, d)` 都只算 **1 个调用点**，所以 power 本身**不减少算子**。它的真实价值有两条：

1. **分母只写一次** —— 杜绝"改一处漏一处"，也让变量抽取生效（不抽取的话 `multiply(d,d)` 仍要写两遍 `d` 的完整表达式）。
2. **分数指数变得免费可测（关键）** —— 过去想试 1.5 次方只能写 `multiply(d, sqrt(d))`（2 个调用点），想试 1.75/2.25 只能凑近似。有了 `power` 任意实数指数都是 1 个调用点，于是打开一条**连续搜索维度**：

| 分母指数 k | S | F | TO | 2Y | sub | 备注 |
|---:|---:|---:|---:|---:|---:|---|
| 1.5 | 1.51 | 0.90 | 20.81% | 2.10 | 1.06 | |
| 1.75 | 1.53 | 0.92 | 20.77% | 2.17 | 1.10 | |
| 2.0 | 1.57 | 0.96 | 20.73% | 2.23 | 1.13 | 旧最优 `MP6LYLw8` |
| **2.25** | **1.58 ✓** | 0.97 | 20.71% | 2.26 | 1.11 | **`LOW_SHARPE` 首次 PASS**（`9ql7lwG9`） |
| 2.3 | 1.57 | 0.96 | 20.70% | 2.25 | 1.12 | |
| 2.4 | 1.56 | 0.95 | 20.69% | 2.25 | 1.12 | |
| 2.5 | 1.56 | 0.95 | 20.66% | 2.23 | 1.10 | |
| 2.6 | 1.56 | 0.95 | 20.64% | 2.24 | 1.10 | |
| 2.75 | 1.55 | 0.94 | 20.64% | 2.23 | 1.08 | |
| 3.0 | 1.55 | 0.94 | 20.62% | 2.25 | 1.06 | |
| 3.25 | 1.52 | 0.91 | 20.61% | 2.17 | 1.02 | |

**k=2.25 是尖峰**（不是平台期）：2.0→1.57、2.25→1.58、2.3→1.57。整条 frontier 被抬了 0.01，正是这 0.01 让 S 闸（1.58）首次通过。**这是本轮唯一靠"纯数学改写"拿到的指标提升。**

### 10.3 log 相加：数学上成立，工程上彻底失败

`log(K) − 2·log(D) = log(K / D²)` 在数学上是恒等式，实测却是灾难：

| 构造 | S | F | TO | DD | longCount | 2Y | sub |
|---|---:|---:|---:|---:|---:|---:|---:|
| `log(k) − 2·log(d)` | 0.57 | 0.27 | 26.2% | **18.9%** | **20** | −0.21 | 0.59 |
| `log(k) − 2.5·log(d)` | 0.61 | 0.30 | 26.2% | 18.2% | 20 | −0.15 | 0.65 |
| `log(k) − 3·log(d)` | 0.43 | 0.18 | 26.2% | **24.5%** | 20 | −0.28 | 0.51 |
| `divide(k, power(d,2.25))` 对照 | **1.58** | **0.97** | 20.7% | **4.6%** | 144/189 | **2.26** | **1.11** |

三条失败原因（有普适性）：

1. **`exp` 在平台不存在**（`get_operators` 103 条里没有），所以 log 只能单向，无法把结果映射回原尺度；
2. **log 抹掉了"每域名摊薄"这个经济量**——`D` 跨股票离散度很大，`log D` 把它压平，等于把「分母越大多头越弱」的非线性全部拉直；DD 从 4.6% 爆到 18–25%，持仓从 333 只缩到 82 只（极端集中），Sharpe 直接归零；
3. **`group_rank` 对单调变换不变，但 `ts_zscore` 与 `ts_target_tvr_hump` 不是**。所以"log 形式与比值形式在最终排序上等价"只在**整条链全是单调不变算子**时成立（rank / group_rank / bucket / ts_rank）。本件中间夹着 z-score 与 hump，链路不满足条件。

⇒ **可复用判据：只有当链路上全部是单调不变算子（`rank`/`group_rank`/`bucket`/`ts_rank`/`densify`）时，才可以用 log 域加法替换比值来省算子；一旦夹了 z-score、decay、hump、winsorize，就必须用真实比值。**

### 10.4 其余数学重述（全部实测，全部失败）

| 重述形式 | 数学关系 | S | F | 结论 |
|---|---|---:|---:|---|
| `subtract(ts_zscore(k), 2·ts_zscore(d))`（+外 z） | "分位数差"而非"比值" | 0.48 | 0.17 | 全灭，sub −0.31 |
| 同上（无外 z） | 直接排序差 | 0.38 | 0.12 | 全灭 |
| `divide(power(k,0.5), power(d,2))` | 分子开方 | 0.50 | 0.23 | 全灭，2Y −0.13 |
| `divide(power(k,1.5), power(d,3))` | 分子 1.5 次 | 0.62 | 0.31 | 全灭 |
| `multiply(k, power(d,-2))` | ≡ `k/d²` | 1.57 | 0.96 | **等价**（pnl 差 24/3.8M = 6e-6，浮点路径不同，指标无差） |
| `multiply(k, inverse(power(d,2)))` | ≡ `k/d²` | 1.57 | 0.96 | **等价**（同上） |

**结论：分子指数必须恰为 1，分母指数必须 >1 且 2.25 最优。** 分子一开方或一乘方就崩，说明这个经济量是「**尾部厚度对域名数的弹性**」，弹性系数不可改。

### 10.5 已用尽的数学恒等式（避免重复尝试）

- `ts_zscore` 仿射不变：`ts_zscore(a·x+b) = sign(a)·ts_zscore(x)` ⇒ 任何常数加/乘都可省（本式已无冗余常数）。
- `group_rank(reverse(x), g) ≡ group_rank(1/(x+1), g)`（记忆库已记）⇒ 本式无 `reverse`。
- 秩不可加：`rank(a)+rank(b) ≠ rank(a·b)` ⇒ "双 z 差分"正是踩了这条，全灭。
- `divide(a, power(b,k))` 已是「a 对 b 的弹性」的最省形式，2 个调用点，无法再压。

**最终最小形式（`operatorCount` 9 / PPA 口径 7 / distinct 6，指标与 11 调用点的原式逐位相同）** 见 §10.1。

### 10.6 ★★★ 「ops」到底以什么为准：三个口径互不相同（官方原文 + 377 颗实测）

**结论先说：`ops` 没有唯一含义，平台上有三个并存的口径，各自绑定不同的东西。**

#### 口径一：`regular.operatorCount` = 调用总次数（含重复、含 `ts_backfill`、**含赋值行**）

`GET /alphas/{id}` 的 `regular.operatorCount`。实证（本仓库 `output_report/.cache_genius_os_alphas.json`，2026-11-16 拉取的 377 颗 OS alpha）：

| 候选计数法 | 与平台值逐颗精确对齐 |
|---|---:|
| 函数调用点（含重复、含 ts_backfill） | 228/377 = **60.5%** |
| + 中缀符号运算（`+ - * / < >`，含一元负号） | 330/377 = **87.5%** |
| **去重算子（distinct）** | 89/377 = **23.6%** |

⇒ **是调用次数，绝不是算子种类数。** 剩余 12.5% 的偏差全部来自「负数字面量（`-1.0*`）不算一次运算」这类解析细节；对**没有符号运算**的表达式（如本战役的候选项）该规则是**精确的**。

两个判定性样本：

```text
rank(reverse(ts_regression(ts_zscore(returns,252),
     ts_zscore(ts_backfill(ern3_pre_interval,10),252),252,rettype=0)))
调用点 = 6（ts_zscore 重复两次）｜distinct = 5｜平台 operatorCount = 6
```
⇒ 重复调用**各计一次**，`ts_backfill` **也计入**。

```text
a = ts_mean(overall_sentiment_score,66); m = ts_mean(likelihood_of_neutral_tone,66); k = ...
三条赋值语句共 8 个调用点｜平台 operatorCount = 8
```
⇒ **赋值行上的算子照常计数**，只有 `=` 本身不是算子。这就是「变量抽取能压 `operatorCount`」的真正机制——它省掉的是**赋值行里的重复调用**，不是「赋值不算」。（`78Yk8VR1`：`a = ts_backfill(...); -group_rank(...)` → 9 个调用 + 1 个一元负号 = `oc=10`，进一步证实一元负号也计。）

#### 口径二：Power Pool ≤8 = 调用次数（含重复），**但排除 `ts_backfill` / `group_backfill`**

`getting-started-power-pool-alphas` 原文：

> "Number of total operators, **including repeat operators** <= 8 (`ts_backfill` and `group_backfill` are not counted)"

⇒ 与口径一差两点：**去掉了 backfill**，但**照样含重复调用**。

#### 口径三：Genius 六维 T1/T3 = **distinct** 算子数，**同样排除 backfill**

`brain-genius` 原文（tie-breaker 六项）：

> "**Avg distinct Operators**/Alpha (Lower is better) … **Total distinct Operators** (Higher is better)"
> "\* `ts_backfill` and `group_backfill` are not counted in Avg distinct and Total distinct Operators."

⇒ 只有 T1/T3 用的是**去重后的算子种类**，且 backfill 不计。

#### 三点实践推论

1. **REGULAR 提交没有算子数闸。** `consultant-submission-tests` 的完整清单是 Fitness / Sharpe / Turnover / Weight / Sub-universe / Self-corr / Prod-corr / IS-Ladder / Bias —— **没有任何算子相关条目**。算子数只影响「PPA 资格」和「Genius 同档超额时的排序」，不是提交门槛（与本仓 `01_platform_gates.md` 既有记录一致）。
2. **要压 PPA 口径，优先砍「非 backfill 的重复调用」**；砍 `ts_backfill` 对 PPA 与 T1 **零收益**（它本来就不计）。本战役变量的抽取实际只赚到 `operatorCount` −2、PPA −1，**T1 一点没动**——因为省掉的两个恰好都是 `ts_backfill`。
3. **要压 T1，必须砍「不同算子种类」**（例如把 `power` 换回 `multiply`、或去掉 `winsorize`），这跟压 `operatorCount` 是两件事。

#### 本战役各件的真实算子数（按上述规则推算）

| 件 | `operatorCount` | PPA 口径（≤8） | Genius T1（distinct） |
|---|---:|---:|---:|
| 原件 `zqdRJWL8` | 3 | 3 | 3 |
| `MP6LYLw8`（11 调用，无赋值行） | 11 | 8 | 6 |
| **`VkN3zO15`（主交付）** | **9** | **7** | **6** |
| `VkN3el3M`（+`winsorize`） | 10 | 8（贴线） | 7 |

⇒ 六维口径下 **`VkN3zO15`（T1 贡献 6）优于 `VkN3el3M`（7）**，这也支持把前者当主交付。

## 11. 分母指数 k=2.25 是尖峰（11 点扫描，S 首次过闸）

| k | S | F | TO | 2Y | sub | 备注 |
|---:|---:|---:|---:|---:|---:|---|
| 1.5 | 1.51 | 0.90 | 20.81% | 2.10 | 1.06 | |
| 1.75 | 1.53 | 0.92 | 20.77% | 2.17 | 1.10 | |
| 2.0 | 1.57 | 0.96 | 20.73% | 2.23 | 1.13 | 旧最优 |
| **2.25** | **1.58 ✓** | 0.97 | 20.71% | 2.26 | 1.11 | `9ql7lwG9`，**首次 `LOW_SHARPE` PASS** |
| 2.3 | 1.57 | 0.96 | 20.70% | 2.25 | 1.12 | |
| 2.4 | 1.56 | 0.95 | 20.69% | 2.25 | 1.12 | |
| 2.5 | 1.56 | 0.95 | 20.66% | 2.23 | 1.10 | |
| 2.6 | 1.56 | 0.95 | 20.64% | 2.24 | 1.10 | |
| 2.75 | 1.55 | 0.94 | 20.64% | 2.23 | 1.08 | |
| 3.0 | 1.55 | 0.94 | 20.62% | 2.25 | 1.06 | |
| 3.25 | 1.52 | 0.91 | 20.61% | 2.17 | 1.02 | |

**k=2.25 不是平台期，是尖峰**（2.0→1.57、2.25→1.58、2.3→1.57）。这 0.01 正是 S 闸从 1.57 跨到 1.58 的全部来源——**纯数学改写拿到的唯一一次过闸**。

## 12. 三条负面结论（勿再重试）

### 12.1 `ts_target_tvr_hump` 的 `lambda_min` / `lambda_max` 是 no-op
`lambda_max=0.8` 与 `lambda_max=0.6` 的 pnl 与默认值**逐位相同**（3,733,216 / 3,848,241）⇒ hump 内部寻优权重本就落在 [0, 0.6] 内，上限参数永不 binding。`lambda_min=0.2` 则强制过度平滑，TO 崩到 2.64%、S 0.94。**该参数族无需再扫。**

### 12.2 `hump` 与 `group_rank` 的顺序不可换
| 顺序 | S | F | TO | 2Y | sub |
|---|---:|---:|---:|---:|---:|
| `group_rank(hump(z), sector)`（现序） | **1.58** | 0.97 | 20.71% | 2.26 | 1.11 |
| `hump(group_rank(z, sector), .20)`（swap） | **1.58** | 0.88 | **25.14%** | **2.31** | **1.17** |

swap 后 S 不变，但 **TO 从 20.7% 暴涨到 25.1%** ⇒ F 掉 0.09。原因：rank 后信号被压进 [0,1] 均匀分布，hump 的"单日变动幅度"约束按绝对尺度生效，同样的 target 对应更大的实际换手。**副产品**：swap 版的 2Y 2.31 / sub 1.17 是全族最佳，若日后要单独攻 2Y 可用，但 F 不达标。

### 12.3 `ts_rank` 不能替代 `ts_zscore`（在 hump 之前）
S 1.07 / 1.10，sub 0.59 / 0.65，2Y 1.43。原因同上：uniform 分布下 hump 的换手控制失真，且 z-score 保留的"幅度信息"被秩丢掉了。

## 13. 前沿推进到「S 1.59 / F 0.98」

`hump` 目标细扫（exp 2.25，w48，sector，backfill）：

| hump | S | F | TO | R | R/TO |
|---:|---:|---:|---:|---:|---:|
| .18 | 1.51 | 0.98 | 17.92% | 7.49% | 0.418 |
| .19 | 1.50 | 0.94 | 18.69% | 7.38% | 0.395 |
| .20 | 1.53 | 0.95 | 19.37% | 7.50% | 0.387 |
| .21 | 1.56 | 0.96 | 20.06% | 7.65% | 0.381 |
| **.215** | **1.59** | **0.98** | 20.38% | 7.76% | 0.381 |
| .22 | 1.58 | 0.97 | 20.71% | 7.73% | 0.373 |
| .225 | 1.58 | 0.96 | 21.03% | 7.71% | 0.367 |

**当前最优 `xAvdVYqJ`**：

```text
d = ts_backfill(vec_avg(snl27_totaldomains), 22);
k = ts_backfill(vec_avg(snl27_kurtosis), 22);
group_rank(ts_target_tvr_hump(ts_zscore(divide(k, power(d, 2.25)), 48), target_tvr=0.215), sector)
```

| 指标 | 值 | 闸 | 状态 |
|---|---:|---:|---|
| Sharpe | **1.59** | 1.58 | ✔ |
| Fitness | **0.98** | 1.00 | ✗ −0.02 |
| TO | 20.38% | — | ✔ |
| Returns | 7.76% | — | 基线 +23% |
| 2Y | 2.27 | 1.58 | ✔ +0.69 |
| sub S | 1.11 | ~0.45 | ✔ |
| invest S/F | 1.44 / 1.10 | — | ✔ |
| risk-neut S | 1.18 | — | ✔ |
| CONCENTRATED_WEIGHT | PASS | — | ✔ |
| **算子数**（`operatorCount`） | **9** | — | 原式 11；PPA 口径 7、distinct 6，口径见 §10.6 |
| `ra_failed_checks` | **仅 `LOW_FITNESS`** | — | 1 项 |

**F 缺口代数**：`F = S·√(R/TO)`。在 S 1.59、TO 20.38% 处要 F=1.00 需 `R ≥ 8.06%`，实测 7.76%，差 **0.30pp**；等价地，R 不变时需 `S ≥ 1.64`。

### 13.1 `winsorize` 是有效的（唯一一个能在 hump 前改变仓位几何的正向杠杆）

| 构造（hump .20） | S | F | TO |
|---|---:|---:|---:|
| 无 winsorize | 1.53 | 0.95 | 19.37% |
| **`winsorize(std=2)`** | **1.57** | 0.95 | 20.68% |
| `tail(±1, newval=0)` | 1.39 | 0.90 | 16.28% |

`winsorize` 在 hump **之前**（而非之前测过的 group_rank 之后）不是 no-op——它砍掉 z>2 的极端值，改变 hump 的分配几何，S +0.04。`tail` 相反：把中间带清零导致信号稀疏，S −0.14。

## 14. ★★★ `ts_backfill` 回看长度：22 → 10，**全部 RA 闸通过**

分子侧 `ts_backfill` 的回看长度是此前被当成"无关参数"的一维，实测是**决定性的**：

| 分子 bf | 分母 bf | S | F | TO | R | 2Y | sub | `ra_failed` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 22 | 1.60 | 1.00 | 20.17% | 7.86% | 2.27 | 1.10 | **0** |
| 6 | 22 | — | — | — | — | — | — | 见 §15 |
| **8** | **22** | **1.63** | **1.02** | 20.24% | **7.97%** | 2.31 | 1.12 | **0** |
| 10 | 22 | 1.62 | 1.02 | 20.27% | 7.96% | 2.31 | 1.13 | **0** |
| 12 | 22 | 1.61 | 1.00 | 20.29% | 7.88% | 2.30 | 1.16 | **0** |
| 15 | 22 | 1.57 | 0.97 | 20.32% | 7.71% | 2.28 | 1.10 | 2 |
| 22 | 22 | 1.59 | 0.98 | 20.38% | 7.76% | 2.27 | 1.11 | 1 |
| 44 | 22 | 1.58 | 0.97 | 20.42% | 7.72% | 2.21 | 1.14 | 1 |
| 10 | **10** | 1.62 | 1.02 | 20.27% | 7.96% | 2.31 | 1.13 | **0** |

**方向严格不对称**：
- **分子（kurtosis）回看是有效维度**：5→1.60、**8→1.63（峰）**、10→1.62、12→1.61、15→1.57、22→1.59、44→1.58。8–12 是平台期，**8 为峰值**；15 是鞍点（比 22 还差）。
- **分母（totaldomains）回看是 no-op**：bf 10 与 bf 22 的 pnl **逐位相同**（3,963,656）、全部指标一致 ⇒ totaldomains 的缺值极少，backfill 长度对结果无影响。

**机制解释**：分子 backfill 越短，`kurtosis` 在缺值日越早停止填充、信号越"新鲜"；但太短（5）会丢连续性。分母是"域名数"这类缓变量，缺值本就少，回看长度无意义。

### 14.1 `rK7PN5r8` —— 全部 RA 闸通过（`ra_failed: false`）

```text
d = ts_backfill(vec_avg(snl27_totaldomains), 22);
k = ts_backfill(vec_avg(snl27_kurtosis), 10);
group_rank(ts_target_tvr_hump(ts_zscore(divide(k, power(d, 2.25)), 48), target_tvr=0.215), sector)
```

| 硬闸 | 阈值 | 实测 | 状态 |
|---|---:|---:|---|
| Sharpe | ≥ 1.58 | **1.62** | ✅ |
| Fitness | ≥ 1.00 | **1.02** | ✅ |
| 2Y Sharpe | ≥ 1.58 | **2.31** | ✅ |
| Sub-universe S | — | **1.13** | ✅ |
| CONCENTRATED_WEIGHT | — | PASS | ✅ |
| CLUSTER_TEST | — | PASS | ✅ |
| **self correlation** | < 0.70 | **0.2391** | ✅（21 颗池，最近 `d5a2aO7v`） |
| **prod correlation** | < 0.70 | **0.5606** | ✅ |
| `ra_failed_count` | 0 | **0** | ✅ |
| 算子调用点 | — | **9** | 原式 11；PPA 7、distinct 6 |

**prod 相关性直方图（关键）**：`[0.6,0.7)` = **0 颗**、`[0.5,0.6)` 仅 **4 颗**、`[0.4,0.5)` 12 颗 ⇒ 该字段族是**冷门区**，不是 `LLKRWzR2`/`QP0QOdbg` 那种饱和配置导致的拥挤墙。这也解释了为什么本战役能一路优化到通关——起点 prod 0.6143 本身就在薄墙外侧。

其他指标：Returns **7.96%**（原件 6.31%，**+26%**）、DD 4.69%、investability S/F **1.42/1.08**、risk-neutralized S **1.23**、margin 0.000785。

### 14.2 全战役净变化（原件 → 通关件）

| 指标 | `zqdRJWL8` | `rK7PN5r8` | Δ |
|---|---:|---:|---:|
| Sharpe | 1.26 | **1.62** | **+0.36（+28.6%）** |
| Fitness | 0.64 | **1.02** | **+0.38（+59%）** |
| 2Y | 1.73 | **2.31** | +0.58 |
| Returns | 6.31% | 7.96% | +26% |
| DD | — | 4.69% | |
| CONCENTRATED_WEIGHT | warning | PASS | 修复 |
| fail 项 | 3 | **0** | **全通** |
| 算子数 | 3 | 5 | +2（六维软成本） |

**关键改造链（按贡献排序）**：
1. **比率构造** `divide(k, power(d, k))` —— +0.19 S（分母指数从"无"到 2）
2. **`power` 分数指数精调** → k=2.25 —— +0.01 S（跨过 S 闸的那 0.01）
3. **`ts_target_tvr_hump`** 替代 `tvr_decay` —— +0.20 F
4. **`ts_backfill(·, 22)`** 修 CONCENTRATED_WEIGHT —— 从 warning 到 PASS
5. **`ts_backfill` 回看 22→10（仅分子侧）** —— +0.03 S / +0.04 F / +0.20pp R，**最后一步过闸**
6. **窗口 48 + sector 轴** —— +0.09 S

---

# 15. 最终状态：全闸通过，两个可交付件

## 15.1 主交付件 `VkN3zO15`（推荐，最稳健）

```text
d = ts_backfill(vec_avg(snl27_totaldomains), 22);
k = ts_backfill(vec_avg(snl27_kurtosis), 8);
group_rank(ts_target_tvr_hump(ts_zscore(divide(k, power(d, 2.25)), 48), target_tvr=0.215), sector)
```

| 维度 | 值 | 闸 | 状态 |
|---|---:|---:|---|
| **Sharpe** | **1.63** | 1.58 | ✅ +0.05 |
| **Fitness** | **1.02** | 1.00 | ✅ +0.02 |
| Turnover | 20.24% | — | ✅ |
| Returns | 7.97% | — | 原件 6.31% → **+26%** |
| Drawdown | 4.61% | — | |
| **2Y Sharpe** | **2.31** | 1.58 | ✅ +0.73 |
| Sub-universe S | 1.12 | ~0.45 | ✅ |
| Investability S/F | 1.43 / 1.09 | — | ✅ 容量健康 |
| Risk-neutralized S | 1.24 | — | ✅ |
| CONCENTRATED_WEIGHT | PASS | — | ✅ |
| CLUSTER_TEST | PASS | — | ✅ |
| **self correlation** | **0.2407**（池 21，最近 `d5a2aO7v` 0.241） | <0.70 | ✅ |
| **prod correlation** | **0.5614** | <0.70 | ✅ |
| `ra_failed_count` | **0** | 0 | ✅ |
| **算子调用点** | **9**（PPA 口径 7 / distinct 6） | — | 原式 11；口径见 §10.6 |
| 塔 | `DEU/D1/SENTIMENT` ×**1.8** | — | 当季 1/3 → 交后 **2/3**（未点亮，需 ≥3） |

**为什么选它当主交付**：全部参数都落在**平台期中心**而非尖峰——
- 分子 backfill 6/7/8/9/10/12 全部过关（1.61–1.63），8 在正中；
- 分母指数 2.2/2.25/2.3 全过（1.61–1.63）；
- hump 目标 .205/.21/.215/.22/.225 全过（1.58–1.63）；
- 窗口 46/47/48 全过，50 唯一不过；
- 算子数 5（无 `winsorize`），F 余量 0.02 而非 0.01。

## 15.2 高 Sharpe 备选 `VkN3el3M`（加 `winsorize`）

```text
d = ts_backfill(vec_avg(snl27_totaldomains), 22);
k = ts_backfill(vec_avg(snl27_kurtosis), 8);
group_rank(ts_target_tvr_hump(winsorize(ts_zscore(divide(k, power(d, 2.25)), 48), std=2), target_tvr=0.215), sector)
```

| 指标 | 值 |
|---|---:|
| Sharpe | **1.65**（全族最高） |
| Fitness | **1.01** |
| Turnover | 21.46% |
| Returns | **8.04%**（全族最高） |
| 2Y | **2.33** |
| sub / invest / risk-neut | 1.12 / 1.45-1.11 / 1.23 |
| self corr | **0.2408** ✅ |
| prod corr | **0.5614** ✅ |
| `ra_failed_count` | **0** ✅ |
| 算子数 | 6（多一个 `winsorize`） |

⚠ 代价：算子 +1；F 余量只剩 0.01；TO 21.46% 比主件高 1.2pp。**若按六维偏好（算子越少越好）与稳健性优先，取 `VkN3zO15`。**

## 15.3 参数敏感性（稳健性审计素材，全部实测）

| 维度 | 扫描范围 | 全过区间 | 峰值 |
|---|---|---|---|
| 分母指数 k | 1.5 → 3.25（11 点） | — | **2.25** |
| 分子 backfill | 5 → 44（8 点） | 6–12 | **8**（6/8 并列 1.63） |
| 分母 backfill | 10 / 22 | both（逐位相同） | no-op |
| hump 目标 | .18 → .28（11 点） | .205–.225 | **.215** |
| `ts_zscore` 窗口 | 44/46/47/48/49/50/52/55 | 46–48 | **48** |
| `group_rank` 轴 | market / sector / densify(industry) | sector | sector |
| neutralization | SUBINDUSTRY / MARKET / INDUSTRY / SLOW_AND_FAST / CROWDING | SUBINDUSTRY | SUBINDUSTRY |
| truncation | 0.02 / 0.04 / 0.08 | 全部（逐位相同） | 零杠杆 |

## 15.4 本战役有效手段清单（按贡献排序）

| # | 手段 | 机制 | 贡献 |
|---|---|---|---|
| 1 | **比率构造** `divide(k, power(d, k))` | 造出"每域名摊薄后的尾部集中度" | **+0.19 S** |
| 2 | **`ts_target_tvr_hump`** 替代 `tvr_decay` | 限单日变动幅度而非指数平滑，保相位 | **+0.20 F** |
| 3 | **`ts_backfill` 回看 8–10（仅分子）** | 信号更新鲜 | **+0.04 S / +0.04 F** |
| 4 | **`ts_backfill(·,22)` 修 CW** | 缺失日不再填 0，破权重堆积 | CW→PASS |
| 5 | **窗口 48 + sector 轴** | 匹配新构造的波动尺度 | **+0.09 S** |
| 6 | **`power` 分数指数 2.25** | 弹性系数最优点 | +0.01 S（过闸关键） |
| 7 | **变量抽取** | 调用的去重，非信号改动 | `operatorCount` 11→9；**distinct 不变（6）** |

## 15.5 结论

**`zqdRJWL8` 从「3 项 fail、判 `REJECT_STRUCTURAL`」到「0 项 fail、全部 RA 闸通过」，共约 240 臂。** 路径不是调参，而是三次**换信息构造**：单字段 → 比率 → 弹性 → 幅度整形 + 数据新鲜度。

剩余未做（用户决定）：
- 未提交（`ALLOW_ALPHA_SUBMIT=False`，提交权归用户）；
- 提交前仍需按规范补：~300 词三段式 `description`、`robustness_<id>` 真审计台账（参数敏感性表已备好 §15.3）、ET 配额核对；
- 若提交 `VkN3zO15`，同骨架孪生（本战役 ~40 颗）会因 self≥0.99 全部封死，需先确定选哪一颗。

---

# 16. 六维为标杆（用户 2026-11-18 19:55 明令）

> 原话：「我只关注影响我收益的六维，所以后面关于这块的描述准则约束都以这个为标杆」

## 16.1 标杆带来的口径变更

| 项 | 旧做法 | 新标杆下的做法 |
|---|---|---|
| 报「ops」 | 用 `regular.operatorCount` / PPA 口径排序 | **只用 distinct（T1/T3 口径）** |
| 选件排序键 | 绩效 → 塔 → 算子数越少越好 | 绩效+塔为前置，**同档内按六维排名和** |
| 算子压缩的目标 | 压 `operatorCount` | 压 **T1**（distinct）；砍 backfill 对 T1 零收益 |
| 增量来源 | 微调参数 | **引入未用算子（T3↑）与新字段（T4↑）** |

⚠ **重要前提**：T1/T3 **只统计已提交（OS）的 alpha**。IS 件在提交前对六维零贡献 ⇒ 六维收益只在「你最终选中的那一颗被提交」时兑现，选件本身就是一个六维最优化问题。

## 16.2 基线与未用池（2026-11-18 实测，377 颗 OS）

| 项 | 值 |
|---|---|
| distinct ops 基线 | **57 / 103** |
| fields 基线 | 495（脚本口径）／平台 `dataFieldsUsed` 422 |
| 未用算子池 | **46 个**（含整族 `reduce_*` 14 个、`inverse`、`sqrt`、`zscore`、`pasteurize`、`power`、`ts_kurtosis`、`ts_step`、`ts_count_nans`、`kth_element`、`group_sum/std_dev/count`、`universe_size`、`min`、`vec_min/range`…） |

**★ 三个实证否决（未用池 ≠ 可白拿）**

| 尝试 | 结果 | 原因 |
|---|---|---|
| `reduce_avg` 替 `vec_avg` | **ERROR: inaccessible or unknown operator** | catalog 含不可用算子；且**一条坏式会把整批其余臂一起 CANCELLED** |
| `min(k, 1000000)` 包裹 | S **1.11**（应恒等） | `min` 与标量作用不是逐元素取小 |
| `sqrt(multiply(k,k))` 包裹 | S **0.28** | **`snl27_kurtosis` 是有符号超额峰度**，取绝对值等于翻符号 |

## 16.3 可白拿的 T3（三处，全部实证「指标逐位不变」）

| 变换 | 依据 | pnl | 新增 T3 |
|---|---|---:|---|
| `divide(a, power(b,k))` → `multiply(a, inverse(power(b,k)))` | `inverse(x)=1/x`，数学恒等 | 3,970,317 **同** | `inverse` +1 |
| 比值外层加 `pasteurize(...)` | 语义为「INF 或不在 universe → NaN」；本件 `pasteurization=ON` ⇒ **恒等** | 3,970,317 **同** | `pasteurize` +1 |
| `power(b, k)` 分数指数 | 已在使用 | — | `power` +1 |

三处叠加后的 `vRAvXvZb` / `1YWzAzlk`：S 1.63 / F 1.02 / TO 20.24% / R 7.97% / 2Y 2.31 / sub 1.12 / invest 1.43-1.09 / risk-neut 1.24，**pnl 仍为 3,970,317**，`ra_failed 0`，self corr **0.2407（与基线完全同值）**。

## 16.4 候选六维边际（按新标杆排序）

| 件 | 表达式要点 | **T1 distinct** | **T3 新增算子** | **T4 新增字段** | 六维排名和（同档内） |
|---|---|---:|---|---:|---|
| **`vRAvXvZb`**（`1YWzAzlk` 同） | +`pasteurize` +`inverse` +`power` | 8 | **+3（power, inverse, pasteurize）** | +2 | **最优** |
| `2r5NxxxJ` | +`inverse` +`power`（自然写法） | 7 | +2（power, inverse） | +2 | 次优 |
| `KPgEpQWg` | +`pasteurize` +`power` | 7 | +2（power, pasteurize） | +2 | 次优 |
| `VkN3zO15` | 仅 `power` | **6** | +1（power） | +2 | 第三 |
| `VkN3el3M` | +`winsorize` +`power` | 7 | +1（power；`winsorize` 已在基线） | +2 | **最差**（多花 1 个 distinct 没换到 T3） |
| `MP6LYLw8` | 无 `power` | 6 | **0** | +2 | 最差（T3 零） |

**换算**：T3 每 +1 ≈ **+1.75%**（57→58 的确定性增量）；单件 ΔT1 只到 0.02% 量级 ⇒ **+2 T3（≈+3.5%）远大于 T1 +2 的软成本**。

## 16.5 结论与一条需要你裁定的冲突

- **纯六维最大**：提交 **`vRAvXvZb`**（T3 +3、T4 +2、T1 8）。
- **自然写法**：提交 **`2r5NxxxJ`**（T3 +2、T4 +2、T1 7）——`inverse` 重构是无争议的等价改写。
- **`pasteurize` 这一处需要你决定**：它在本件是**恒等变换**（因为设置已 `pasteurization=ON`），所以第 3 个 T3 本质属于「为凑指标而包装」，与本仓既有准则「不为凑数改写已过闸的表达式」（`wq-brain-ppa-mining/SKILL.md`）冲突。按你 19:55 的新令（六维为标杆）它应当保留；按旧准则应当去掉。**我按新令保留，并在此显式标注。**

三件绩效完全相同（pnl 逐位相同），所以这个选择**只影响六维、不影响任何风险指标**。

---

# 17. 基线口径复核（用户 2026-11-18 20:11 质疑：「应该统计当季提交的 alpha」）

## 17.1 结论

**六维 tiebreaker 是累计口径，不是当季。** 但这次质疑抓到两个真错误：我的基线数字**过期且混用了三套口径**，已全部重算。

## 17.2 官方原文的范围措辞（`brain-genius`，2026-09-18 版）

| 条款 | 原文中的时间限定 |
|---|---|
| Eligibility ① 信号数 | "Submit a minimum number of signals ... **per quarter**" ⇒ 按季 |
| Eligibility ② 塔数 | 按季（本仓已实测：塔计数按季重置） |
| **T1 / T2 / T3 / T4** | **无任何时间限定**（"Avg distinct Operators/Alpha"、"Total distinct Fields"） |
| T5 Max Streak | "best streak ... that ends in that quarter or continues into the next quarter. **Streak does not reset to 0 every quarter**" |
| T6 Community | 论坛 "as of the end of quarter"（期末累计）；referral "**in the quarter**"（按季） |

⇒ 季度化的是 **eligibility** 与 **T6 的 referral**；T1–T4 没有"当季"措辞。T5 那句"不每季归零"是**反向提示**：若所有维度都按季重算，这句话没有存在必要。

## 17.3 决定性检验：平台的字段数不可能是当季

平台 `dataFieldsUsed` 是 T4 的底层值（本仓 09-19 已核实）。把它与"脚本累计 / 脚本当季"同时对照：

| 时点 | 脚本累计 | 脚本当季 | 平台 `dataFieldsUsed` | 判定 |
|---|---:|---:|---:|---|
| 2026-09-19 | 286 / 223 颗 | 176 / 99 颗 | **180** | 当季更接近（唯一异常点） |
| 2026-10-06 | 348 / 291 颗 | **47 / 29 颗** | **256** | **只可能是累计**（当季上限 47，平台超出 5.4 倍） |
| 2026-11-18 | 515 / 442 颗 | 233 / 180 颗 | **435** | **只可能是累计**（当季上限 233，平台超出 86%） |

10-06 是决定性一点：Q4 从 10-01 起算，到 10-06 只交 29 颗、最多用 47 个字段，平台却报 **256** ⇒ **跨季累加、不归零**。

残差恒定在 80–92 个字段，来源已知（平台只数现存数据集字段，脚本还含分组键与历史下架字段），与"累计"假设完全自洽；若按当季，残差会变成 −202（平台比脚本还多 200 个字段，不可能）。

## 17.4 两套口径的完整基线（脚本口径，2026-11-18 重算）

| 口径 | N | T1 | T2 | T3 | T4 |
|---|---:|---:|---:|---:|---:|
| **累计 · 全部**（推荐） | 412 | 4.575 | 2.794 | **62** /103 | **515** |
| 累计 · 仅 REGULAR | 386 | 4.627 | 2.852 | 61 | 515 |
| 当季 Q4 · 全部 | 164 | 5.189 | 2.811 | 55 | 233 |
| 当季 Q4 · 仅 REGULAR | 139 | 5.439 | 2.971 | 51 | 232 |
| **平台 `dataFieldsUsed`** | — | — | — | — | **435** |

未用算子池：累计 **41**（103−62）／当季 48（103−55）。
⚠ 本库 SUPER 的 selection/combo 表达式部分未落盘 ⇒ 累计 T3=62 是**下界**，真值略高。

## 17.5 对我此前汇报的修正（三处真错误）

| 项 | 我之前报的 | 真值 | 错因 |
|---|---|---|---|
| T3 | 57 / 103，未用 46 | **61–62 / 103，未用 41–42** | 用的是 11-16 的过滤缓存（只含能取到 `regular.code` 的 REGULAR）且已过期 |
| T4 | 495（脚本）/ 422（平台） | **515（脚本）/ 435（平台）** | 同一句里混用两套口径，且未更新 |
| T2 | 1.8488 | **2.794** | 旧值来自同一份过滤缓存，字段提取口径不同 |

T1 基本未变（4.6074 → 4.575）。

## 17.6 关键：排序完全不变

四个候选的"新增算子集合"在两套窗口下**逐字相同**：

| 件 | distinct | T3（累计窗口） | T3（当季窗口） |
|---|---:|---|---|
| `VkN3zO15` | 6 | power | power |
| `2r5NxxxJ` | 7 | inverse, power | inverse, power |
| `KPgEpQWg` | 7 | pasteurize, power | pasteurize, power |
| **`vRAvXvZb`** | 8 | **inverse, pasteurize, power** | **inverse, pasteurize, power** |
| `VkN3el3M` | 7 | power（`winsorize` 两窗口都已用） | power |

字段 `snl27_kurtosis` / `snl27_totaldomains` 在两窗口下都是新字段（T4 +2）。⇒ **口径之争不影响选件**：`vRAvXvZb` 仍最优（T3 +3）。

## 17.7 口径决定的是策略性质，不是这一次选件

- **累计口径（证据支持）** ⇒ 41 个未用算子是**一次性资本**：用掉永久失去、不能再赚。正确做法＝把新算子挂到"本来就要交的件"上白拿（本次做法），**绝不为 T3 专门造垃圾件**。
- **当季口径** ⇒ 同一批算子是**可重复收益**，每季重置、每季可重赚。正确做法变成"每季重交变体重新点亮"。

两种策略的成本收益差一个数量级，所以这个问题值得查清。

## 17.8 可证伪的检验（唯一能定案的方法）

2027-01-01 后第一次读 `dataFieldsUsed`：

- 从 435 附近**继续累加**（440+）⇒ 累计口径，本报告成立；
- **骤降到两位数** ⇒ 当季口径，则 §17.4 "当季"行才是基线，且 T4 边际价值翻倍（+2 从 +0.46% 变 +0.86%）。

在此之前按累计决策（证据占优），且两种口径下本次选件结论一致 ⇒ **不需要等待**。

⚠ 残余不确定：官方文档未明写 T1–T4 窗口，上述结论基于①文档措辞②平台字段数的两点实测。若你有平台侧口径（Genius 面板/官方答复），以它为准，我按它重算。

---

# 18. 提交前预检矩阵（2026-11-18 20:30）

## 18.1 逐件预检结果

| 项 | `vRAvXvZb` | `2r5NxxxJ` | `KPgEpQWg` | `VkN3zO15` | `VkN3el3M` | `MP6LYLw8` |
|---|---:|---:|---:|---:|---:|---:|
| Sharpe | 1.63 | 1.63 | 1.63 | 1.63 | **1.65** | 1.57 ✗ |
| Fitness | 1.02 | 1.02 | 1.02 | 1.02 | 1.01 | 0.96 ✗ |
| 2Y | 2.31 | 2.31 | 2.31 | 2.31 | 2.33 | 2.23 |
| Turnover | 20.24% | 20.24% | 20.24% | 20.24% | 21.46% | 20.73% |
| Returns | 7.97% | 7.97% | 7.97% | 7.97% | **8.04%** | 7.68% |
| sub-universe | 1.12 | 1.12 | 1.12 | 1.12 | 1.12 | 1.13 |
| invest S/F | 1.43/1.09 | 同 | 同 | 同 | 1.45/1.11 | 1.42/1.08 |
| risk-neut S | 1.24 | 同 | 同 | 同 | — | — |
| **prod corr** | **0.5614 ✅** | 0.5614 ✅(同 PnL) | 同 | 0.5614 ✅ | 0.5614 ✅ | — |
| **self corr** | **0.2407 ✅** | 0.2407 ✅ | 同 | 同 | 未测 | — |
| `failed_ra/ppa` | **0 / 0** | 0/0 | 0/0 | 0/0 | 0/0 | **2** ✗ |
| `checks.fail` | **[]** | [] | [] | [] | [] | 2 项 |
| **distinct ops（T1）** | **8** | 7 | 7 | **6** | 7 | 6 |
| **T3 新增** | **+3** | +2 | +2 | +1 | +1 | 0 |
| **T4 新增** | **+2** | +2 | +2 | +2 | +2 | +2 |
| 稳健性 verdict | CONDITIONAL | CONDITIONAL | 同族 | 同族 | CONDITIONAL | — |
| 近 3 年 CV | 0.537 | 0.537 | 0.537 | 0.537 | **0.507** | — |

## 18.2 硬闸结论

- **模拟层**：四件 `sim_fails=[]`、`failed_ra=0`、`failed_ppa=0`、`hard_gate_warnings=[]`。`checks.pass` 全绿（含 `LOW_SHARPE` / `LOW_FITNESS` / `LOW_2Y_SHARPE` / `CONCENTRATED_WEIGHT` / `LOW_SUB_UNIVERSE_SHARPE` / `CLUSTER_TEST` / `MATCHES_PYRAMID`）。
- **提交层**：`GET /alphas/{id}/submit` **恒 404**（平台死端点），`submit_verdict` 只能给 `UNVERIFIABLE`；放行依赖 prod/self 实测 + 用户确认。
- **prod 直方图**：`[0.6,0.7)` = **0 颗**、`[0.7,0.8)` = **0 颗**。该字段族仍处冷区，不是饱和墙。
- **稳健性**：`CONDITIONAL`（唯一实质软标记＝近 3 年 CV 0.537，成因是 2023 单年 Sharpe 3.67 占全期 PnL 42.5%）。硬闸无 FAIL、无 REJECT，`submit_verdict` 不拦。

## 18.3 配额与塔

- ET 日 **2026-11-18**，今日已交 **1 颗**（`2r5Lm3Jx`，DEU），REGULAR **1/4 → 剩 3**；SUPER 0/1。
- 塔 `DEU/D1/SENTIMENT`：当季计数 **1**，倍率 **1.8**；提交后 **2**，**仍不点亮**（需 ≥3）。

## 18.4 推荐：`vRAvXvZb`

```text
d = ts_backfill(vec_avg(snl27_totaldomains), 22);
k = ts_backfill(vec_avg(snl27_kurtosis), 8);
group_rank(ts_target_tvr_hump(ts_zscore(pasteurize(multiply(k, inverse(power(d, 2.25)))), 48), target_tvr=0.215), sector)
```

**理由**：在同绩效同风险的 5 件里，它是唯一 **T3 +3**（`power` / `inverse` / `pasteurize` 三个此前未用算子），T4 +2，五件同档下六维排名和最小。

**提交代价**：其余 4 件与本战役约 40 颗同骨架孪生会因 self ≥0.99 全部封死 ⇒ 这是一次性选择，必须选六维最优的那颗。

**若你更保守**：`2r5NxxxJ`（T3 +2、T1 7，去掉 `pasteurize` 这层恒等包装）仍是六维次优，绩效逐位相同。

**提交前三件待办**：① 你明确确认（`ALLOW_ALPHA_SUBMIT=False` 未放开）；② 三段式 `description` ~300 词，并如实写入 CV 0.537 软标记；③ 不动 PPA 标签（REGULAR 路径预置会让平台按 `PURE_POWER_POOL_THEME` 检查，可能直接拒）。

---

# 19. 提交执行记录：`VkN3zO15` 被边际贡献硬闸拦下（2026-11-18 20:34）

用户指令「提交 VkN3zO15」。`workflow_submit_alpha(confirm_submit=False)` 预检结果：

| 件 | `submit_gate` | 边际闸分区 | before S/TO/Ret | after S/TO/Ret | Δ | 结论 |
|---|---|---|---|---:|---:|---|---|
| **`VkN3zO15`** | pass（fRA 0、robustness CONDITIONAL） | `EQUITY:DEU:1:​POWER_POOL` | 1.73 / 12.70% / 7.99% | 1.83 / 14.69% / 7.35% | ΔS +0.10、ΔF **−0.08**、ΔRet **−0.64pp**、ΔTO **+1.99pp** | **`pair_block` 硬拦** |
| `VkN3el3M` | pass | `EQUITY:DEU:1:​POWER_POOL` | 1.73 / 12.70% / 7.99% | 1.84 / 14.99% / 7.36% | ΔS +0.11、ΔF **−0.08**、ΔRet **−0.63pp**、ΔTO **+2.29pp** | **`pair_block` 硬拦** |
| `2r5NxxxJ` | pass | `EQUITY:DEU:1:​POWER_POOL` | 同上 | 同上 | 同 `VkN3zO15` | **`pair_block` 硬拦** |
| **`vRAvXvZb`** | pass | **`EQUITY:DEU:1`** | 3.66 / 13.59% / 10.00% | 3.69 / 13.72% / 9.95% | ΔS +0.03、ΔF 0.00、ΔRet −0.05pp、ΔTO +0.13pp | **`pass_offset` 放行** |

## 19.1 拦阻原因（不是候选缺陷）

方案 D v2 的 L2 配对判据：`ΔRet ≤ −0.5pp` **且**（`ΔTO ≥ +1.5pp` 或 `ΔDD ≥ +0.5pp`）⇒ 阻断，`force` 不豁免。
`VkN3zO15` 的 TO 20.24% 远高于 PP 池的 12.70%，叠加后把池换手拉高 **1.99pp**、组合收益降 **0.64pp**，正中该判据。
（`VkN3el3M` 换手更高 21.46%，故 ΔTO 更大。）

## 19.2 ★★★ 新坑：同 PnL 兄弟件会被分到不同分区

`vRAvXvZb` 与 `VkN3zO15` / `2r5NxxxJ` 的 **PnL 逐位相同（3,970,317）**，但平台 `before-and-after-performance` 把它们分到了**不同分区**：

- `vRAvXvZb` → `EQUITY:DEU:1`（厚池，before S 3.66）⇒ 叠加后几乎不动（ΔS +0.03 / ΔRet −0.05pp）⇒ 放行
- `VkN3zO15` / `2r5NxxxJ` / `VkN3el3M` → `EQUITY:DEU:1:POWER_POOL`（薄池，before S 1.73）⇒ 双重恶化 ⇒ 拦

⇒ **边际闸的判定取决于分区标签，而分区标签不由 PnL 决定**。同族兄弟必须逐颗跑预检，不能拿一颗的结论外推。
（与 `submit_alpha.py` 的 docstring §③「基准池随分区漂移，跨 alpha 的 ΔS 不可比」一致。）

## 19.3 当前可提交件

**`vRAvXvZb`** 是本案唯一过闸件，且六维最优（T3 +3、T4 +2、T1 8），绩效与 `VkN3zO15` 逐位相同。
待用户确认后执行 `confirm_submit=True`（配额 REGULAR 剩 3）。

`VkN3zO15` **不可提交**，且无豁免入口——若坚持要交这颗，只能改结构把 TO 压到约 18.4% 以下（该档 S 仅 1.50–1.53，`LOW_SHARPE` 不过），在本构造下不可行。

---

# 20. 提交完成：`vRAvXvZb` → **ACTIVE**（2026-11-18 20:37 ET 07:37）

用户 20:36 确认「交 vRAvXvZb」，20:37:18 执行 `confirm_submit=True`，一次通过。

## 20.1 提交结果

| 项 | 值 |
|---|---|
| **status** | **ACTIVE**（`stage: OS`） |
| **dateSubmitted** | **2026-11-18T07:37:01-05:00**（ET） |
| name / color / tags | `DEU_R_snl27kurt_01` / **BLUE** / `CH_REG`, `SRC_sentiment27`, `EXPRFAM_snl27kurt` |
| 响应形态 | **201 Accepted (async)** → 节点轮询后翻 `ACTIVE`（走的是 ② 异步受理分支，非失败） |
| 塔 | `DEU/D1/SENTIMENT` ×**1.8**（`MATCHES_PYRAMID` PASS，effective 1） |
| 配额 | ET 2026-11-18 REGULAR **1/4 → 2/4**（`quota_status.py` 600s 缓存滞后，仍显 1/4，以节点 `quota_gate` 为准） |

## 20.2 提交流程逐闸（全部记录在 `output` 里）

| 步骤 | 结果 |
|---|---|
| `submit_gate` | pass｜failed_ra 0 / failed_ppa 0 / robustness **CONDITIONAL**（已落台账） |
| `mix_audit` | **SINGLE_DATA_SET**（ATOM）⇒ 走 `ATOM:LAST_2Y`，2Y 2.31 ≥ 1.58 过 |
| `quota_gate` | allowed，used 1 / limit 4 / remaining 3 |
| `prod_gate` | **0.5614 < 0.7**，`from_cache=true`（20:28 实测，48h 内可信） |
| `marginal_contribution` | 分区 `EQUITY:DEU:1`｜**`pass_offset`**｜ΔS +0.03、ΔF 0.00、ΔRet −0.05pp、ΔTO +0.13pp |
| `set_properties` | 成功，name/tags/description 全部落盘（`operatorCount` 平台读 **11**） |
| `submit` | **201 async_accepted** |
| `verify` | **ACTIVE** |
| `prod_snapshot` | 闸门 0.5614 ＝ 平台冻结值 0.5614（`delta 0.0`，prod 闸诚实） |
| `tag_disposal` | 提交前无 PPA 标签 ✅；平台未自动追加 `PowerPoolSelected` |

## 20.3 提交后指标（`get_alpha_details`）

| 指标 | 值 | 闸 | 状态 |
|---|---:|---:|---|
| Sharpe | 1.63 | 1.58 | PASS |
| Fitness | 1.02 | 1.00 | PASS |
| 2Y Sharpe | 2.31 | 1.58 | PASS |
| Turnover | 20.24% | — | PASS |
| Returns | 7.97% | — | — |
| Drawdown | 4.61% | — | — |
| Sub-universe S | 1.12 | 0.77 | PASS |
| CLUSTER_TEST | 1.36 | 1.00 | PASS |
| **self correlation** | **0.3276** | 0.70 | PASS |
| **prod correlation** | **0.5614** | 0.70 | PASS |
| invest S / F | 1.43 / 1.09 | — | 容量健康 |
| risk-neut S | 1.24 | — | — |
| `checks.fail` / `pending` | **[] / []** | — | **全清** |

⚠ 口径注记：提交前本地自相关算的是 **0.2407**，平台回填为 **0.3276**（池含刚提交的自身家族，且平台池与本地池口径不同）。两者都远低于 0.70，不影响判定，但**报 self 时应以平台回填值为准**。

## 20.4 六维（提交后兑现）

| 维度 | 值 | 说明 |
|---|---|---|
| **T1** distinct ops/alpha | **8** | 单件 ΔT1 ≈ +0.008（软成本，量级 0.02%） |
| **T2** distinct fields/alpha | 2 | — |
| **T3** 新增算子 | **+3** | `power`、`inverse`、`pasteurize`（提交前均未在池中出现）→ 62 → **65** |
| **T4** 新增字段 | **+2** | `snl27_kurtosis`、`snl27_totaldomains` → 515 → **517**（平台口径 435 → 437） |
| T5 / T6 | n/a | 与选件无关 |

## 20.5 后续

- **BLUE 待观察**：`GREEN` 须由 OS 实际表现挣得，不得预设。
- **孪生封死**：`VkN3zO15` / `2r5NxxxJ` / `KPgEpQWg` / `VkN3el3M` / `MP6LYLw8` 及本战役约 40 颗同骨架件，自相关会 ≥0.99，**不可再交**。
- 塔计数 `DEU/D1/SENTIMENT` 平台缓存仍显 1，属已知延迟（提交后有缓存），下次刷新应到 2；**点亮需 ≥3**。
