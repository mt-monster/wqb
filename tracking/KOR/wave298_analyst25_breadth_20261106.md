# wave298 · analyst25 十二模板（KOR / TOP600 / D1）· 2026-11-06

> 区域固定 KOR｜universe TOP600｜delay 1｜目标：ATOM（单数据集）REGULAR alpha
> 数据集：`analyst25`（197 字段，**全部 VECTOR**，cov 全 0.500，白空间 24/197）

## 一、为什么开这一波

| # | 依据 |
|---|---|
| 1 | `analyst25` **不在任何判死表**；此前排除理由只有「alphaCount 3231 高竞争」，不是信号死 |
| 2 | 论坛帖 `43250301270295`（36 赞）报告「分析师盈利预期修正广度」**IS S 3.0–4.5 / TO 0.15–0.35**，并直接指向本集 13 个「家数/估计者数量」字段 |
| 3 | 本集是 KOR **唯一有离线体检包**的数据集（`field_profile/kor_analyst25_profile.json`）⇒ 字段画像最完整 |
| 4 | `kor_priors.json:21` 存有 `mLgknM1p`（KOR analyst25，ra_failed=0 全 checks PASS），仅卡 prod 墙 ⇒ 该集**历史到过提交级** |
| 5 | 已点亮塔不含 ANALYST；analyst 塔 2/3 仍可挖 |

## 二、模板库（12 个结构互异模板，满足 ≥10 硬约束）

差异维度：**字段族 × vec 降维算子 × 时序算子 × 分组轴 × 非线性变换**。
全部 ATOM：表达式中**只出现 `anl25_*` 字段**，不引 `close`/成交量等 PV 字段（避免跨塔与破 ATOM）。

| # | 批 | 机制面 | 表达式 | 算子树 |
|---|---|---|---|---:|
| A1 | A | 修正广度净占比（水平态）·论坛首推 | `group_rank(divide(subtract(vec_sum(anl25_tnc_pu_spe), vec_sum(anl25_eps_down_cnt)), vec_sum(anl25_tot_eps_ests_num)), sector)` | 6 |
| A2 | A | 同一广度的**一阶差分**（信息增量，非水平） | `group_rank(ts_delta(<breadth_net>, 22), sector)` | 7 |
| A3 | A | 换数据腿：**目标价**修正广度净占比 | `group_rank(divide(subtract(vec_sum(anl25_recom_val_up_cnt), vec_sum(anl25_recom_val_down_cnt)), vec_sum(anl25_tot_recomm_num)), sector)` | 6 |
| A4 | A | 目标价溢价 · **时序标准化** + industry 轴（`mLgknM1p` 的 ATOM 化改写） | `group_rank(ts_zscore(vec_avg(anl25_target_prc_med), 66), industry)` | 3 |
| A5 | A | 目标价**分歧度变异系数**（不确定性溢价，取负） | `subtract(0.5, group_rank(divide(vec_stddev(anl25_target_prc_stddev), vec_avg(anl25_target_prc_med)), sector))` | 5 |
| A6 | A | 目标价 1 月修正额的 **22 日累积**（修正速度，非瞬时） | `group_rank(ts_sum(vec_avg(anl25_target_prc_chg_1m), 22), sector)` | 3 |
| B1 | B | 经营利润预测**离散度形状**（极差/中位，取负） | `subtract(0.5, group_rank(divide(subtract(vec_avg(anl25_adj_oper_p_max), vec_avg(anl25_adj_oper_p_min)), vec_avg(anl25_adj_oper_p_med)), sector))` | 7 |
| B2 | B | 盈利**期限结构**（12f / 12t 口径熵） | `group_rank(divide(vec_avg(anl25_revert_net_profit_12f), vec_avg(anl25_revert_net_profit_12t)), sector)` | 4 |
| B3 | B | **利润率剪刀差**（EBIT margin − OperProfit margin，同源两腿相减） | `group_rank(subtract(vec_avg(anl25_ebit_margin), vec_avg(anl25_oper_profit_margin)), sector)` | 4 |
| B4 | B | **新覆盖进场**的 66 日变化（覆盖广度动量） | `group_rank(ts_delta(vec_sum(anl25_eps_new_cnt), 66), sector)` | 3 |
| B5 | B | 广度的**时序分位**（截面秩 → 时序秩） | `group_rank(ts_rank(<breadth_net>, 66), sector)` | 7 |
| B6 | B | EPS 增长率的 22 日均值（平滑水平，非广度为量） | `group_rank(ts_mean(vec_avg(anl25_eps_growth), 22), sector)` | 3 |

`<breadth_net>` = `divide(subtract(vec_sum(anl25_tnc_pu_spe), vec_sum(anl25_eps_down_cnt)), vec_sum(anl25_tot_eps_ests_num))`

**算子数全部 ≤ 7**，远低于上限 12。无 `add` 等权混腿；B3 的两腿为**同源同集 + 单一经济含义**（利润率口径差），属放行形态。

## 三、设置（两批完全一致，保证模板间可归因）

| 项 | 值 |
|---|---|
| region / universe / delay | KOR / TOP600 / D1 |
| neutralization | `REVERSION_AND_MOMENTUM` |
| decay | 4 |
| truncation | 0.08 |
| nanHandling | ON（VECTOR cov 全 0.5，缺失需补） |
| pasteurization / maxTrade | ON / **OFF** |
| unitHandling | VERIFY |

⚠ 论坛推荐 `STATISTICAL` + 短 decay，本波刻意用 R&M/decay4：① 与已出货的 `qMLOooX1`（analyst10）同设置便于横向比较；② 若 12 模板**全灭**，先按论坛口径换 STATISTICAL/decay2 复测**最强的 2 个模板**，再判死。

## 四、预检

`preflight_expressions` 12/12 通过：`valid: true`、`unknown_fields: []`、`unknown_soft: []`。

## 五、派发

| 批 | multisim | 条数 | 派出时刻 |
|---|---|---:|---|
| A（A1–A6） | `4wPkQ7gti5cPb31jBBR45Wl` | 6 | 2026-11-06 19:12 左右 |
| B（B1–B6） | `3HnxEd4FM4xVaOf1dnsni5vR` | 6 | 2026-11-06 19:12 左右 |

## 六、实测结果

> 待回填（回测完成后按模板编号归因，不按单条 alpha 归因）。

## 七、已知风险

| 风险 | 说明 |
|---|---|
| **CW 结构性风险** | 本集 cov **恰 0.500**（197/197）⇒ 落在集中度危险区边缘；若命中 `CONCENTRATED_WEIGHT` 则该条判死 |
| **prod 墙** | `kor_priors.json` 的 `KOR-VALUE-QUALITY-SEEDS` 条记录：含 analyst25 旧快照族的族因 `PROD_CORRELATION` 全败（0.759–0.782）。本波若 S 达标，须优先查 prod |
| **单位连坐** | `divide` 两腿单位不一致可能 `Incompatible unit`；B3/B1 的比值构造风险最高 |
| **alphaCount 拥挤** | 头部字段 `anl25_f21_spe` αC 397、`anl25_adj_oper_profit_12f` αC 374 ⇒ 若命中头部字段，prod 风险更高（本波刻意规避这两个最拥挤字段） |
