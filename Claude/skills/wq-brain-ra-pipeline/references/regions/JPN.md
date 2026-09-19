---
region: JPN
entry_verdict: active
one_liner: "2026-09-15 首度开挖：平台实测 universe 仅 TOP1600/TOP1200；D1 共 7 塔全 0 亮；白名单 10 集（pyramid_view 战略榜重建，6 塔覆盖）"
static:
  universe: [TOP1600, TOP1200]   # 平台 get_platform_setting_options 实测（2026-09-15）
  universe_default: TOP1600
  delay: [1, 0]
  delay_default: 1
  neutralization_default: MARKET
  notes: "旧文档曾错写 TOP3000 / TOP2000 / TOP1000 / TOP500，全部无效——一切以平台实测为准；中性化 SUBINDUSTRY/SECTOR 实测不可用（见硬事实 3）"
datasets:
  red: []
  red_reason: ""
  yellow: []
  green: [intraday_pv_feats, continuation_score, pattern_scores, analyst_consensus, analyst_base_ref, fundamental109, fund_holdings_panel, mmp_nlp_sentiment, acquisition_model, news_sentiment_transfer]
  green_note: "s0_whitelist（2026-09-15 重建，pyramid_view 战略榜口径）：放宽档 coverage≥0.6 / alphaCount≤1500 / fieldCount≥10 + 补偿三件套；10 集均无 WebDataScope 体检包；备选 price_signal_dl / analyst_factor_signals / dl_riskfree_returns（拥挤）"
priors:
  signal_families_include: []
  signal_families_exclude: [emotion]
  syntax_patterns: []
  win_recipes: []
  win_note: "区域 win 层空（新开垦）；GLOBAL region_kb 模板可用；anl15 系按精确表达式（sha1）级封禁，非前缀通配"
gate_overrides:
  cw_gate: FAIL
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 5
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死回写，不扩批不换设置重试"
  stop_conditions: ["白名单被 dead_end 全覆盖", "连续 3 波全 FAIL 且无新 dead_end"]
empirical_anchor:
  pyramid: "JPN/D1 7 塔 0 亮（2026-09-15 平台实测）：analyst/model/other/fundamental/pv/sentiment/institutions 各需 3 颗"
  compensation: "alphaCount 50→1500 放宽 30 倍的三件套：users≥50 仅信号方向验证 / users10-49 进池必实测 / users0-9 优先且冷门字段占批次预算≥50%"
  last_verified: 2026-09-15
---

# JPN — 2026-09-15 首度开挖（active）

## 定位与实证依据

JPN 为 2026-09-15 首度开挖的 active 区：无 win 层、无 dead_end、无任何回测历史（expressions/backtest_results 均空）。目标 = 新挖「过闸待提交」REGULAR alpha，点塔集中在 3–4 座塔（D1 共 7 塔，每塔 3 颗点亮）。

白名单已锁 10 个数据集（`s0_whitelist`，2026-09-15 依 `s0_ranking.pyramid_view` 战略榜重建、旧 6 集名单留档于 `legacy_whitelist_20260915_pre`）：pv×3（intraday_pv_feats / continuation_score / pattern_scores，score 1.07 断层领先）+ analyst×2（analyst_consensus / analyst_base_ref）+ fundamental109 + fund_holdings_panel（institutions）+ other×2（mmp_nlp_sentiment / acquisition_model）+ news_sentiment_transfer（sentiment）。6 塔覆盖，非 MODEL 占比 9/10。备选：price_signal_dl（model ac=4）/ analyst_factor_signals / dl_riskfree_returns（userCount 227，按「users≥50 仅方向验证」级）。

## 平台硬事实（2026-09-15 实测，覆盖一切旧文档）

1. **universe 仅 `TOP1600` / `TOP1200`**。`src/wqb/config.py`、`tracking/JPN/config/settings.json`、`tracking/region_config.json`、`tools_sim.py` 的 `_REGION_UNIVERSE_MAP` 已按实测对齐——历史错值（TOP3000/TOP2000/TOP1000/TOP500）全部作废。
2. delay：1（静态档）+ 0（可探）；delay 切换单独成批。
3. 中性化：**SUBINDUSTRY / SECTOR 实测不可用**（2026-09-15 模拟层实证：报 `Invalid data field subindustry/sector`，POST 可接受但执行必 ERROR；JPN 缺分类字段，平台 options 列表含 ≠ 实际可用）。**可用：NONE / MARKET / STATISTICAL**（三条对照模拟均 COMPLETE）。静态档取 `MARKET`；A/B 对照可用 STATISTICAL。无 COUNTRY。

4. **intraday_pv_feats 目录字段 ≠ 平台可用字段（2026-09-19 w8 实测）**：8/10 批 CANCELLED，平台报 `Invalid data field close`，
   而表达式不含裸 `close`（同集单字段探针 `mean_last_trade_price_return_30m_pre_close_2` / `max_twap_vwap_ratio_daily` 在
   STATISTICAL 与 MARKET 下均 COMPLETE）→ 部分派生字段目录有、平台无。intraday 微观结构在 JPN 与 IND/GBR/USA 同样弱（16 条 max|S| 1.02），
   不再投入；含 `sector/subindustry/industry` 的表达式必须在选波后丢弃（闸 2b / GEM pregate 已自动拦）。
5. **积压闸**：JPN 1728 条 GEM 池 conversion 0.4% 会被 backlog gate 拦住；已按用户指令写 `backlog_gate_override` 至 2026-09-25。
   analyst_revision_horizons 的 GEM 一次渲染 7538 条（1026 字段 × 模板）——pregate 骨架封顶（缺省 12/骨架）已上线，重跑会自动收敛。

## 流程变体（相对九步骨架）

### 步 1 注入：实测优先 + 铁律逐条核对

静态层以实测为准（已固化）。跨区铁律逐条标注「本波是否触碰」。

### 步 2 注入：放宽档 + 补偿三件套（强制）

放宽档（coverage≥0.6 / alphaCount≤1500 / fieldCount≥10）已获本次授权；补偿三件套随行：users≥50 只做信号方向验证、users 10-49 进池提交前必实测、users 0-9 优先且冷门字段占批次预算 ≥50%。选型偏好 Other / Risk / ShortInterest 等未点亮类别；JPN profile green 名单实测不达标则回退 green。

### 步 4 注入：点塔集中 + JPN 黑名单

- 点塔：7 塔 0 亮，优先选 3–4 座塔各打 3–5 颗，避免摊薄。
- 生成黑名单：emotion 系全排除；anl15 系按**精确表达式**匹配封禁（sha1 比对，非前缀通配）。
- 禁止 add(A,B) 混信号；主辅权重显式分配（默认 0.6 主 + 0.4 辅，禁止 50/50 无差别 add）。

### 步 5 注入：体检硬门缺口处置

白名单 6 集在 `research-data/WebData_20260219_V0.10.9.zip`（JPN/D1 仅 2 数据集：analyst14/model25，均不在白名单）**无 WebDataScope 数据** → `wave_gate` 会打印「体检硬门未生效」。此时预处理 5 硬门（低覆盖 ts_backfill / |skew|>2 rank/winsorize/signed_power / kurt>8 rank/winsorize / 单边恒正负禁裸水平 / 稀疏事件 trade_when）由 S1 层 `get_datafields` 画像补齐把关。

### 步 6 注入：fast_kill

新数据集 8 探针无 |S|≥0.5 即判死回写（`thresholds.jpn_specific_adjustments.fast_kill`），不扩批不换设置重试。

### 步 9 注入：死路外溢评估

判死族评估是否跨区普适；是 → `upsert_registry_empirical(region="GLOBAL", layer="cross_region")`。

## 避坑清单

- **禁止照抄他区 universe**：本区实为 TOP1600/TOP1200（曾四处错写为 TOP3000/TOP2000 等，2026-09-15 已全量修正）。
- **禁止用 SECTOR/SUBINDUSTRY 中性化**：必报 `Invalid data field`（POST 可接受但执行全 ERROR，2026-09-15 两次 24 条批实证）。用 MARKET/STATISTICAL/NONE。
- **体检包缺口是已知状态**：不要因「体检硬门未生效」警告而停摆；按步 5 注入用字段画像替代把关，但仍严格执行 5 条预处理规则。
- **anl15 黑名单是精确表达式级**（sha1），不要退化为前缀通配误杀整个 anl15 家族。
- JPN 提交配额与其他区**共享** REGULAR 4 颗 / ET 日历日，提交需用户逐颗确认。

## 硬事实 6（2026-09-19 实证）：JPN/TOP1600/D1 **没有 pv1 基础量价字段**

- `get_datasets(JPN, D1, TOP1600, category=pv)` 只有 continuation_score / intraday_pv_feats / pattern_scores / univ1，**无 pv1**：`close` / `adv20` / `returns` / `volume` 等全部不可用。
- 直接后果：`rank(ts_delta(close, 5))` → 平台 `Invalid data field close`（2Jja8EaWz59v8IfKuZfRmZ2）。
- 连带后果（解释了硬事实 5 的"莫名 close 报错"）：**VECTOR 字段 `vec_avg(f)` 之上再套任何 ts_\* 算子**（ts_delta / ts_delay / ts_zscore / ts_backfill 链）也报同一错误
  （analyst_consensus `mean_flash_estimate_eps_annual12_3`：`rank(vec_avg(f))` COMPLETE=O0NKlYVb S 0.64，而 ts_delta/ts_zscore/subtract+ts_delay 三式全 ERROR；
  w8 intraday_pv_feats 同症）。MATRIX 字段上的 ts_\*（w12 analyst_revision_horizons）正常。
- 规则：JPN 表达式**禁用 pv1 字段、禁用 VECTOR+ts_\* 组合**；VECTOR 只能 `rank(vec_avg(f))`/`group_rank(vec_avg(f), market)` 级别；
  需要"变化/修正"类机制的 VECTOR 数据集（analyst_consensus 等）在 JPN 不可实现 → 分析师塔只能靠 MATRIX 集（analyst_revision_horizons 已实证衰减）。
- GEM 预闸/闸2：JPN 下含 `close|open|high|low|volume|returns|vwap|cap|adv20` 的表达式直接丢弃；含 `ts_*(...vec_*(...))` 的表达式直接丢弃。
