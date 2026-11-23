# news23 — MnA Deals Data（KOR / TOP600 / D1）

> 画像日期：2026-11-17 · 数据源：平台 `get_datafields(dataset_id=news23, region=KOR, universe=TOP600, delay=1, filter_sharpe=false, 不传 max_fields)`。
> 三重对账：`count=93 == platform_count=93`，`complete=true`，pages_fetched=2。字段全量 93/93，**无抽样**。
> 归属类别：NEWS（KOR D1 **未点亮塔**）。归档规则：`tracking/KOR/reference/datasets/<platform dataset_id>.md`（每集一份，手工维护）。

## 1. 数据集体征

| 项 | 值 |
|---|---|
| 数据集 | `news23` — M&A Deals Data |
| 字段数 / 类型 | **93 / 93 全 VECTOR**（最内层必须先 `vec_*` 聚合）|
| 整体覆盖 | 数据集级 0.3288（field 级 0.015–0.795；数据集级 coverage 不作存在性判据，SOP §2.4）|
| aC / userCount | 极低：多数字段 aC 0–2；最高 `nws23_target_asalesltm` aC 12、`nws23_target_niltm` aC 9 ⇒ **冷门集，prod 白空间候选** |
| 更新频率 | 事件驱动（M&A 公告），估计事件型稀疏 ⇒ 窗口 ≥63d（inferred，在线六法待验）|
| 经济轴 | 收购溢价（offer premium）× 目标方估值/盈利 × 收购方对价 |

## 2. 字段族（按 description 分类，不按字段名；名 vs description 差异逐条记）

### 族 A — 报价溢价（机制核心，aC 0–3）
| 字段 | cov | aC | description 要点 |
|---|---:|---:|---|
| `offer_premium_one_day_prior` | 0.149 | 1 | 报价相对公告前 1 日收盘价的溢价 % |
| `offer_premium_one_day_prior_2` | 0.086 | 0 | 同上（名 vs desc 差异：同机制两份字段，需验是否同源）|
| `offer_premium_one_week_prior` | 0.149 | 0 | 公告前 1 周溢价 % |
| `offer_premium_four_weeks_prior` | 0.149 | 3 | 公告前 4 周溢价 %（aC 最高）|
| `offer_premium_*_2` 变体 | 0.086 | 0 | 同族另一版本，cov 更低 |

→ 预处理：cov<0.4 且事件稀疏 ⇒ **必须 `ts_backfill` + `trade_when` 门控，禁裸 rank**。

### 族 B — 目标方估值/盈利（第二腿候选，aC 2–12）
| 字段 | cov | aC | description 要点 |
|---|---:|---:|---|
| `nws23_target_niltm` | 0.313 | 9 | 目标方上一财年净利润 |
| `nws23_target_asalesltm` | 0.312 | 12 | 目标方 LTM 净销售（**全表 aC 最高 = 头部字段 ⇒ 最强经济轴指向"目标方规模"**）|
| `nws23_target_mtlspe` | 0.313 | 2 | 目标方 EPS |
| `nws23_target_pricebook` | 0.207 | 1 | 报价/账面价值比 |
| `nws23_target_value` | 0.313 | 2 | 对价总额 |

### 族 C — 收购方（事件结果字段，D1 未来函数风险）
`nws23_acquiror_apr1daya`（公告后 1 日股价，cov 0.212/aC0）、`nws23_acquiror_akw1rpa`（公告后 1 周，0.202/aC0）、`nws23_acquiror_spea`（收购方 EPS，0.256/aC1）、`nws23_acquiror_value`（对价，0.256/aC1）。
⚠ description 明写 "one day after deal announcement" ⇒ **D1 入场时该信息已发生，禁作信号**（防未来函数）。

### 族 D — 私有市场/PE/VC（与上市公司 alpha 无关，排除）
`investment_detail_disclosed_valuation` 0.795/aC2、`fund_total_size_2` 0.677/aC0、`company_employee_count` 0.396/aC0、`actual_investment_round_total` 0.396/aC5 等约 45 字段 → 非上市标的投资轮数据。

### 族 E — 编码/分类字段（只作分组轴或门控，禁算术）
`company_industry_code` 0.438/aC0、`investment_detail_stage_*` 0.795/aC0–1、`individual_job_title*` 0.396/0.643 aC0、`company_veic6_category` 0.795/aC1。

## 3. 头部字段质量先验（铁律 0.1：aC 降序 TOP）

1. `nws23_target_asalesltm` aC **12** — 目标方销售 ⇒ 头部轴 = **目标方规模/基本面**，不是"溢价"本身。
   **方向纠偏**：机制以目标方基本面为主腿、溢价为辅腿（或溢价作门控），否则方向从第一波就偏。
2. `nws23_target_niltm` aC 9 — 目标方净利润（印证规模/盈利轴）。
3. `actual_investment_round_total` aC 5、`offer_premium_four_weeks_prior` aC 3、`nws23_target_mtlspe/value` aC 2。

## 4. 可用性 / 分布 / 频率（静态推定 [inferred]）

- 类型：**全 VECTOR** → 每字段内 `vec_avg`（计数类 `vec_sum`）后再进 `rank`/`ts_*`。
- 覆盖：族 A 0.086–0.149（稀疏事件）、族 B 0.207–0.313、族 D 0.396–0.795。
- 分布：`point_mass` / `zero_inflated` [inferred]（事件型 + 低 aC）⇒ 门控而非裸 rank。
- 频率：事件驱动 [inferred]，窗口下限 63d（季度），门控用 252d 更稳。
- 近十年：须用 `get_alpha_yearly_stats` 逐年验证，不用数据集级 coverage 替代（SOP §2 / AGENTS §8.11）。

## 5. 已试记录（追加，不覆盖）

> 2026-11-22「每集 ≥5 模板 + 每模板完整梯度」补齐战役。达标标准见记忆
> `imbalance-news-template-gradient-compliance-20261122`。全部 KOR/TOP600/D1/INDUSTRY/decay4/trunc0.08。

### 5.1 五模板定义（互异经济机制，非换窗/常数）
| 模板 | 机制 | 主字段族 |
|---|---|---|
| T1 目标方规模 | 目标方销售/净值水平（aC 头部轴） | 族 B `nws23_target_*` |
| T2 报价溢价 | offer premium 相对公告前价 | 族 A `offer_premium_*` |
| T3 交易估值 | 报价/估值比 rankval、pricebook | 族 B `nws23_target_rank*` |
| T4 目标方盈利 | EPS / 净利润 | 族 B `nws23_target_mtlspe/niltm` |
| T5 收购方规模 | 收购方销售/对价（事件结果，非未来函数字段） | 族 C `nws23_acquiror_asalesltm/value` |

### 5.2 L1 外层截面全类别替换（已完成，5 wave 全 FAIL）
| 模板 | wave | 最优 alpha | 表达式 | S | F | 2Y | failed_RA | 判 |
|---|---|---|---|---:|---:|---:|---:|---|
| T1 | `s2_news23_T1_targetsize_L1_d1` | `MP6VOR06` | `rank(ts_mean(ts_backfill(vec_avg(nws23_target_niltm),22),22))` | 0.23 | 0.11 | −0.01 | — | S 差 1.35，20–60 持仓/年 |
| T2 | `s2_news23_T2_premium_L1_d1` | `1YW0eWjm` | premium 族 backfill+rank | 0.22 | 0.14 | 0.36 | — | CW FAIL，事件极稀疏（lc≈20） |
| T3 | `s2_news23_T3_valuation_L1_d1` | `akaGYdv5` | `zscore(...target_rank_rankval...)` | 0.30 | 0.17 | −0.18 | — | 全族最弱 |
| T4 | `s2_news23_T4_earnings_L1_d1` | `vRAPMerA` | EPS/niltm backfill+rank | 0.20 | 0.09 | 0.10 | — | 无信号 |
| T5 | `s2_news23_T5_acquiror_L1_d1` | `58JYo0zo` | `group_zscore(ts_mean(ts_backfill(vec_avg(nws23_acquiror_asalesltm),22),22),sector)` | **0.63** | **0.51** | **1.79** | 3（S/F/CW） | ★本集最强，2Y 已过闸、S 差 0.95、CW 0.1127 |

**L1 结论**：T5 收购方规模唯一有读数（S0.63/2Y1.79），T1–T4 全部 S≤0.30。M&A 事件极稀疏（longCount 20–61），截面排序几乎无定价力；2Y 偶高是事件窗效应非稳定信号。

### 5.3 L2 内层时序全类别替换（逐模板推进）
| 模板 | wave | 内层全类别替换 8 臂最优 | S | 2Y | L1→L2 Δ | 结论 |
|---|---|---|---:|---:|---|---|
| T1 | `s2_news23_T1_targetsize_L2_d1` | `xAv5a0jn` `ts_mean(252)` | 0.54 | 0.13 | 0.23→**0.54 (Δ+0.31)** | 长窗抬 S 但 2Y 崩，距闸 1.04；内层收敛 |
| T3 | `s2_news23_T3_valuation_L2_d1` | `0mP5nGwp` `ts_backfill(22)` | 0.64 | 0.27 | 0.30→**0.64 (Δ+0.34)** | 本集 L2 最高 S；另 `xAv5XlYn` 2Y1.85 过闸但 S0.51/CW0.1215 微超；CW 主墙（7/8）|
| T4 | `s2_news23_T4_earnings_L2_d1` | `wpoWOgl5` `ts_mean(66)` | 0.38 | 0.17 | 0.20→**0.38 (Δ+0.18)** | EPS 族无定价力，CW 主墙（5/8）；内层收敛 |
| T2 | `s2_news23_T2_premium_L2_d1` | `wpoW6bGl` `ts_zscore(252)` | 0.29 | 0.51 | 0.22→**0.29 (Δ+0.07)** | 最优臂 longCount=3/CW=1.0，`ts_delta` 臂 lc=sc=0 零持仓异常；CW 是主墙（6/8）；内层收敛 |
| T5 | `s2_news23_T5_acquiror_L2_d1` | `akaGvrd9` `ts_mean(66)` / `RRePWJ1n` `ts_mean(66,66)` | 0.31 | 0.69/0.58 | 0.63→**0.31 (Δ−0.32)** | **内层替换全灭**，L1 的 `ts_mean(ts_backfill(...,22),22)` 确认为最优；CW 是主墙（5/8） |

T5 L2 内层替换明细（外层 `group_zscore(...,sector)` 冻结）：`ts_backfill(22)` S0.22 / `ts_mean(66)` **S0.31** / `ts_decay_linear` S0.27 / `ts_av_diff` −0.33 / `ts_delta` 0.04 / `ts_backfill(66)` 0.31 / `ts_backfill(252)` 0.28 / `ts_zscore(252)` −0.02。**全类别内层替换无一超过 L1 基线 S0.63 ⇒ T5 内层收敛**。

T1 L2 内层替换明细（外层 `rank(...)` 冻结）：`ts_backfill(22)` S0.11 / `ts_mean(66)` 0.37 / `ts_decay_linear` 0.07 / `ts_av_diff` −0.19 / `ts_delta` 0.37 / `ts_mean(66,66)` 0.38 / `ts_mean(252)` **0.54** / `ts_zscore(252)` −0.26。**长窗 252 抬 S 到 0.54 但 2Y 崩到 0.13，距全闸 1.04 ⇒ T1 内层收敛**。
### 5.4 收口判定（2026-11-22）
**news23 已满足「≥5 模板 + 每模板完整梯度」**：T1–T5 五个互异经济机制模板 × 每模板 (L1 外层截面全类别替换 8 臂 + L2 内层时序全类别替换 8 臂) = 10 wave / 80 臂，全部入库。
- **0 全闸**：全集最高 S0.64（T3 L2 `0mP5nGwp`）距闸 0.94；T5 L1 `58JYo0zo` S0.63/2Y1.79 是唯一 2Y 过闸臂但 S 差 0.95。
- **主墙 = CW/CONCENTRATED_WEIGHT**（M&A 事件极稀疏，longCount 20–60，极端权重集中）+ S 全线塌（目标方规模/溢价/EPS 族无截面定价力）。
- **跨族不外推**：族 A 溢价、族 B 估值/盈利、族 C 收购方规模三族各自收敛，2Y 偶高（T3 `xAv5XlYn` 1.85）是事件窗效应，非稳定信号。
- **不判死**：按红线「轻易不要把数据集判死」，本集记作「梯度证据完整、信号层弱（0 全闸）」；如需新线只能引外部新信息源，不得用本结论外推其它 news 集。
- 证据闸：论坛 MCP 检索无 M&A 特异模板帖；论文多样证 PASS（16 篇/13 作者，含 JFE《Premium for heightened uncertainty》）。
