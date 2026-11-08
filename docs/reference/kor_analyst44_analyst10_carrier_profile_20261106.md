# KOR · analyst44 / analyst10 载体画像与白空间清单（2026-11-06）

> 区域 KOR / universe TOP600 / delay 1（本区唯一合法档）。
> 数据源：MCP `get_datafields`（`filter_sharpe:false`，两集均 `complete:true`）+ 本地 `wqb-db.query_field_profile`。
> 定位：本文档只回答「**哪些字段值得当主信号载体**」，机制与模板见 `tracking/KOR/wave273_274_analyst_kor_20261106.md`。

---

## 一、结论先行：ANALYST 塔在 KOR 只有 3 个「历史到过 1.5」的载体

全 KOR 字段按 `best_s` 排序后，`analyst*` 数据集里能过 1.5 的只有下列几条（其余全是 shortinterest38 / other466 的地盘）：

| 数据集 | 字段 | 类型 | cov | aC | 历史 best S / F / 2Y | 历史测试数 |
|---|---|---|---:|---:|---|---:|
| analyst44 | `eps_estimate_4wk_change` | VECTOR | **1.00** | 5 | **1.78 / 1.64 / 2.23** | 39 |
| analyst10 | `anl10_smartest_sal_fy1_pred_surps_v0` | MATRIX | 0.96 | 39 | 1.62 / 1.27 / null | 28 |
| analyst44 | `eps_gaap_estimate_4wk_change` | VECTOR | **1.00** | 1 | 1.55 / 1.23 / 1.63 | 5 |
| analyst10 | `anl10_smartest_pre_fy1_pred_surps_v1` | MATRIX | 0.95 | 30 | 1.44 / 1.06 / null | 1 |
| analyst10 | `anl10_smartest_sal_fy1_pred_surps_v1` | MATRIX | 0.96 | 25 | 1.41 / 1.04 / null | 60 |

**必须记住的反例**：`analyst_factor_signals`（本轮 wave272 主战场）在该表里**历史 best S 只有 0.20**；
我本轮用 `ts_delta(eps_revision_magnitude,22)` 打到 **1.22 / F0.96 / 2Y2.09** 已是该集历史最好记录
⇒ 该集**不是被漏掉的金矿，而是天花板本来就低**，继续在它身上加模板的边际收益极低。这是本轮换集的硬依据。

---

## 二、analyst44：540 字段，cov=1.0 的白空间极多

### 2.1 类型与语义
- 540 字段 = VECTOR 374 / MATRIX 166。主体是 **Bloomberg BEst 的「估计 + 修正事件」快照**。
- 三套命名体系并存，**同一经济量出现 2–3 次**，务必按 description 取用、不要按名字猜：
  1. `eps_estimate_4wk_change` / `eps_gaap_estimate_4wk_change` —— 通用 4 周修正（**本轮 proven**）
  2. `anl44_best_eps_4wk_chg` / `anl44_best_dps_4wk_chg` —— Bloomberg BEst 专有 4 周修正（实测更弱：`anl44_best_eps_4wk_chg` 仅 S0.56）
  3. `anl44_2_<metric>_value|prevalue|lastactvalue|coveredby` —— **逐事件向量**（事件流，覆盖 0.49–0.65，别当快照用）
- **多空语义方向陷阱**：`net_debt_*_up_revisions` 里「上修」= 分析师上调**负债**预测 = 基本面变差 ⇒ 该族要取反号才能当多头信号。

### 2.2 cov = 1.00 且几乎无人使用的白空间（可直接当主信号）

| 字段 | aC | 经济含义 | 与已 proven 载体的关系 |
|---|---:|---|---|
| `bps_consensus_change_percent` | 0 | 每股账面价值修正（百分比） | **价值锚**，与 EPS 修正不同源 |
| `bps_4week_consensus_change` | 0 | 同上（绝对额） | 同上 |
| `ffops_4week_consensus_change` | 0 | FFOPS 修正（REIT/重资产） | 独立轴 |
| `ffops_consensus_change_percent` | 0 | 同上（百分比） | 独立轴 |
| `sales_estimate_change_percent` | 1 | **营收**修正（顶层数字，最不易被粉饰） | 论坛实证「比 EPS 干净」 |
| `pretaxprofit_change_percent` | 1 | 税前利润修正 | 独立轴 |
| `net_debt_4week_up_revisions` / `_down_revisions` | 0 / 0 | 杠杆修正广度（**方向要取反**） | 独立轴 |
| `eps_estimate_stddev` / `anl44_best_eps_stddev` | 0 / 0 | EPS 分歧度 | 作分母/门控 |
| `anl44_best_dps_stddev` | 0 | DPS 分歧度 | 同上 |
| `anl44_best_dps_hi` / `_lo` | 0 / 1 | DPS 一致预期区间 | 区间位置/偏斜 |
| `roe_4week_consensus_change` / `roe_consensus_change_percent` | 3 / 3 | ROE 修正 | 质量轴 |
| `bps_num_estimates_up_4w` / `bps_num_estimates_down_4w` | 0 / 6 | 账面价值修正广度 | 广度轴 |

### 2.3 明确不要用的字段族
- `*_currency_code` / `*_crncy_iso` / `*_period_end_dt` / `*_update_time` / `*_fiscal_period` / `*_override_flag`：元数据或时间戳，**不是信号**（时间戳禁作信号）。
- `*_coveredby` / `*_market_status` / `*_session_status`：状态位，只配当门控。
- `anl44_2_*` 事件流层：只适合做事件型（创新性修正），不要与快照层混算。

---

## 三、analyst10：640 字段，StarMine「预测惊喜」矩阵

### 3.1 语义分层（description 原文口径）

    anl10_smartest_<metric>_<horizon>_pred_surps_<version>
      metric  ∈ sal(营收) pre(税前) net(净利) ebi(EBIT) gps(毛利) bps(账面) nav(净资产) ndept(净负债)
      horizon ∈ fy1 / fy2 / fq1 / fq2
      version = v0(原始 raw) / v1(稳定化 stabilized overlay) / v2(精修 refined overlay)

- 「预测惊喜」= StarMine 按分析师历史准确度加权后的 smart estimate 相对 D1 共识的偏离 ⇒ 属**创新性修正**机制，与 4 周修正（analyst44）**机制不同源**，可作独立 alpha。
- v2 通常最拥挤（如 `sal_fy1_v2` aC89），v0 最干净（`sal_fy1_v0` aC39，但历史 best S 最高 1.62）。

### 3.2 cov ≥ 0.90 且 aC ≤ 5 的白空间（本轮未测，可直接排波）

| 字段 | cov | aC |
|---|---:|---:|
| `anl10_smartest_bps_fy1_pred_surps_v0` | 0.92 | **0** |
| `anl10_smartest_bps_fy1_pred_surps_v1` | 0.92 | **0** |
| `anl10_smartest_ebi_fy1_pred_surps_v2` | 0.95 | **0** |
| `anl10_smartest_gps_fy1_pred_surps_v0` | 0.94 | **0** |
| `anl10_smartest_bps_fy1_pred_surps_v2` | 0.92 | 1 |
| `anl10_smartest_gps_fy1_pred_surps_v2` | 0.94 | 1 |
| `anl10_smartest_net_fy1_pred_surps_v2` | 0.96 | 1 |
| `anl10_smartest_gps_fy1_pred_surps_v1` | 0.94 | 3 |
| `anl10_smartest_net_fy1_pred_surps_v0` | 0.96 | 5 |
| `anl10_smartest_ebi_fy1_pred_surps_v1` | 0.95 | 7 |

### 3.3 工程注意
- analyst10 是 **MATRIX** 集（640 里 475 MATRIX / 165 VECTOR）⇒ 上表字段**不需要 vec_ 前缀**；误加 `vec_avg` 会因类型不符被平台判错并**连坐取消整批**。
- 判类型一律走 MCP `get_datafields` 的 `type` 字段，不要靠名字或历史配方猜。

---

## 四、索引
- 原始字段快照：`tracking/KOR/reference/field_profile/kor_analyst44_fields_current.json`、`kor_analyst10_fields_current.json`
- 数据集级扫描表：`docs/reference/kor_analyst_dataset_scan_20261106.md`
- 本轮载体登记（可机读）：本地库 ledger key `KOR/analyst_carrier_registry`
