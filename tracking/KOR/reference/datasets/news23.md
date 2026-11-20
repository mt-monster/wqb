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

（待本战役波次写入：alpha id / 表达式 / S/F/2Y/failed_ra/prod / 淘汰原因）
