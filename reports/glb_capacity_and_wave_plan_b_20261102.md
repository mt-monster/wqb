# GLB 容量上限裁定 + 三波填席计划（2026-11-01 二）

> 配套文档：`reports/glb_basket_20261101.md`（篮子 5 颗的成分、互相关、覆盖核验）
> 台账：`glb_quota_ruling_and_tower_plan_20261101`

---

## 一、配额口径裁定：按「组合名」计

用户 2026-10-28 原话：

> **允许**：trio 塔 × 其它 category 数据集（如 `PV+NEWS`），但**这类组合总量 ≤5 个**。
> **应用**：派发前逐字段映射 category → 先判是否 trio 内部互组 → 再数已用几个（≤4 才可加）。

三条依据：

1. 「**组合**总量」字面指组合，不是 alpha 条数。
2. 同一批规则已另有「**每个两塔组合的候选上限 = 3**」专管每个组合里的 alpha 条数；若 R2 也按条数计，两条规则重叠冲突。
3. 操作口径「再数已用几个」——数的是「组合用了几个」。

**裁定 ⇒ 口径 A：按不同组合名计。**

当前 R2 已用 **4** 个组合名：`FUND+OTHER` / `RISK+OTHER` / `OTHER+SENT` / `INST+OTHER`（见下表）。
⇒ 篮子 **5 颗全合法**，且仍剩 **1 个新组合席**。

---

## 二、容量算术：20 颗不可达，上限 15 颗

```
总上限 = R2 组合上限 × R3 每组合上限 = 5 × 3 = 15 颗
```

| 占位 | 组合 | 已提交 | 本批 | 合计 | R3 限 | 剩余席 |
|---|---|---|---|---|---|---|
| RISK+OTHER | trio 内部禁 → 否，合法 | `LLMWkXp6` | `QPvJ6KVw`+`npv9WLVE` | 3 | 3 | **0 满** |
| FUND+OTHER | 合法 | 0 | `d5WqeQbx`+`RRE3O8r1` | 2 | 3 | **1** |
| OTHER+SENT | 合法 | 0 | `Xg9rMdvl` | 1 | 3 | **2** |
| INST+OTHER | 合法 | `e75pvoNz` | 0 | 1 | 3 | **2** |
| *（第 5 组合，待开）* | 合法 | 0 | 0 | 0 | 3 | **3** |

**免配额路线（单塔 / 非trio×非trio）已四次实测封闭：**

| 路线 | 判据 | 结果 |
|---|---|---|
| trio 单塔裸信号 | prod 实测 | 0.7607–0.9660，**9/9 全灭** |
| 非 trio 单塔 | 字段画像 best_s | ≤ 1.34（RISK 借券费族 prod 0.80–0.94 已饱和） |
| 非trio × 非trio | 13 个组合 | 最好 S **0.64** |
| 504 黄金骨架套非 trio 字段 | w161 探针 | **6/6 全灭**（最高 S 0.28），仅对前向收益预测字段有效 |

⇒ **唯一出路是放宽 R2 组合上限或下调目标：**
- 要 20 颗 ⇒ R2 上限需 **≥ 7**（7×3 = 21）
- 若「20 颗」不含已提交的 2 颗 ⇒ 需 **≥ 8**（8×3 = 24）
- 保持上限 5 ⇒ 本轮做到 **15 颗** 即为精确打满

---

## 三、三波填席 = 三座塔同时点亮

GLB D1 现状（平台 `pyramids` 权威）：`pv 2 / model 3 / other 3 / risk 1 / institutions 1`，其余 8 座为 0。
点亮门槛 = **3 颗**。

| 波 | 组合 | 席 | 点亮目标（0→3 或 1→3） |
|---|---|---|---|
| 篮子 5 颗 | RISK+OTHER ×2 / FUND+OTHER ×2 / OTHER+SENT ×1 | 5 | RISK **1→3 点亮**；FUND 0→2；SENT 0→1 |
| **w162**（在飞） | OTHER+SENT | ≤2 | SENTIMENT **0→3 点亮** |
| **w163**（已校验） | INST+OTHER ×2 + FUND+OTHER ×1 | ≤3 | INSTITUTIONS **1→3 点亮**；FUNDAMENTAL **2→3 点亮** |
| **w164**（已校验） | OTHER+ANALYST | ≤3 | ANALYST **0→3 点亮**（倍率 1.4，全 GLB 最高） |

**总账：已提交 2 + 篮子 5 + w162 2 + w163 3 + w164 3 = 15 颗 = 上限精确打满；组合名恰好 5 个 = 配额精确打满。**

---

## 四、三波的门控选型依据

破 prod 墙的唯一有效杠杆 = `trade_when` 加**非 trio 门控腿**。
已验证 prod 干净（<0.70）的门控读数：

| 门控字段 | 塔 | prod | 状态 |
|---|---|---|---|
| `fnd44_jones_cf_accruals` W22 | FUND | **0.5846** | ✅ 已用（`d5WqeQbx`） |
| `fnd44_perc_accruals` W22 | FUND | **0.6479** | ✅ 已用（`RRE3O8r1`） |
| `vec_avg(rsk60_crowding)` W22/W5 | RISK | 0.6385 / 0.6638 / 0.6867 | ✅ 已满 3 席 |
| `snt21_2neg_conf_low_394` W22 | SENT | **0.6512** | ✅ 已用（`Xg9rMdvl`）→ w162 复用 |
| `market_value_institutional_shares_disposed` W22 | INST | **0.6796** | ✅ 已用（`e75pvoNz`） |

失败的门控（勿再用）：`snt21_2neg_conf_up` 0.754 / `scl12_sentiment` 0.719 / `ern3_pre_interval` 0.7599 / `nws73_headlines` 0.8124 / `rsk60_offer` 0.7954。
**成功率 5/10。**

### w162（OTHER+SENT，复用已验证门控，只换 OTHER 信号腿）
```
trade_when(rank(ts_mean(snt21_2neg_conf_low_394, W)) > 0.7,
           signed_power(subtract(group_rank(<OTHER_SIG>, country), 0.5), 0.5),
           rank(ts_mean(snt21_2neg_conf_low_394, W)) < 0.6)
SIG ∈ {probability_label1_2quantile_20day_ohlcv_img,
       single_bucket_60day_return_estimate_ohlcv_img,
       quantile_label_4bucket_20day_ohlcv_img}      W ∈ {22, 66}   ⇒ 6 条
```

### w163（INST+OTHER 2 席 + FUND+OTHER 1 席，全新门控）
`institutions18` 是 INST 里最优的字段面：**best_s 1.67、历史仅 38 条 alpha**（`institutions6` best_s 只有 0.39、已 251 条）⇒ 新席位走 inst18。

- INST 门控：`inst18_fundownershipv2_pct_held` W22（基金持股占比）/ `inst18_fundownershipv2_num_held` W66（持仓家数=广度）
- FUND 门控：`fnd44_factor_benford` W22（Benford 数字取证分）/ `fnd44_probability_restatement` W22（ML 财报重述概率）——刻意避开已用的两个 accruals 族以降互相关
- 信号：`single_bucket_20day_return_estimate_ohlcv_img_2`(country) / `probability_label1_2quantile_20day_ohlcv_img`(market) / `quantile_label_4bucket_20day_ohlcv_img`(country)

### w164（第 5 组合席 · OTHER+ANALYST）
`analyst10` 174 字段，**大量 cov 1.0 且 alphaCount = 0**（真正未挖）。选型刻意落在 `pred_surps`（= (smart_ests − consensus) / consensus，即预测盈余意外，PEAD 经典门控）与估计陈旧度：

- `anl10_cpsfy1_pred_surps_v1_6285`（cov 1.0，ac 65）
- `anl10_cpsfq1_pred_surps_v2_6306`（cov 0.973，ac 42）
- `vec_avg(anl10_bpspast_det_estage_6399)`（估计天数陈旧度，cov 1.0，ac 136）

为什么选 ANALYST：三选一里 ANALYST 胜出 —— 塔倍率 **1.4**（GLB 最高）、GLB 塔位 **0（未点亮）**、字段面 174 且大面积零使用；MACRO `macro27`（ac 0–4）次之但倍率只有 1.1 且全 VECTOR；INSIDERS 无 cov ≥0.6 字段。

---

## 五、本轮关闭的两颗（勿再投入）

| alpha | 表面指标 | 真实情况 |
|---|---|---|
| `GrbkvJjZ` | S2.74 / **F2.94** / TO12.4% / 2Y4.67 | 塔位实为 **PV+RISK**（submit_ready 标成 RISK 单塔 = 错）；`failed_ra_count=1` 卡 **CONCENTRATED_WEIGHT** —— `rsk60_offer` VECTOR 结构性缺陷，六种改法已全败 |
| `gJbxzpNQ` | S2.51 / **F3.23** / TO10.8% / 2Y4.02 | 同族同病，`failed_ra_count=1` 卡 CW |

⇒ **再次证实 `submit_ready.towers` 与 `gate` 标签不可信**，塔位一律以 `get_alpha_details` 的 `pyramids.list` 为准。

---

## 六、篮子 5 颗终验现状（2026-11-01 23:30）

`batch_get_alpha_metrics` 复读：**5/5 `failed_ra_count = 0`** ✅

| # | alpha | 组合 | S | F | TO | 2Y | sub | prod | prod 时刻 | self | 覆盖 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `QPvJ6KVw` | RISK+OTHER | 3.19 | 1.59 | 28.97% | 3.43 | 1.84 | 0.6385 | 11-01 15:15 | 0.6120 | 2014 空 / 2015 363 |
| 2 | `npv9WLVE` | RISK+OTHER | 3.08 | 1.42 | **60.83%** | 3.19 | 2.38 | 0.6638 | 11-01 15:14 | **0.6644** | 2014 空 / 2015 **50** |
| 3 | `RRE3O8r1` | FUND+OTHER | 2.89 | 1.73 | 16.0% | 2.13 | 1.71 | 0.6479 | 11-01 23:06 | 0.4955 | **10Y 全覆盖** |
| 4 | `d5WqeQbx` | FUND+OTHER | 2.71 | 1.43 | 7.55% | 2.68 | 1.64 | 0.5846 | 11-01 15:12 | 0.4597 | 10Y（2020 −1.36） |
| 5 | `Xg9rMdvl` | OTHER+SENT | 2.44 | 1.47 | 19.06% | 2.69 | 2.22 | 0.6512 | 11-01 15:14 | 0.5515 | **10Y 全覆盖** |

- 篮内互相关最大 `d5WqeQbx`↔`RRE3O8r1` = **0.6741**（余量 0.0259，比 prod 48h 漂移还薄 ⇒ 必须相邻提交并立即读回平台 self）
- `max_subset_exact = true`、尺寸 **5** ⇒ 这是阈值 0.7 下的数学最大篮
- `npv9WLVE` 双重薄：TO 60.83% 距 70% 仅 9.2 点；self 0.6644 距 0.7 仅 0.036
- 提交前仍须逐颗 `check_correlation(refresh=True)` 当场终验（prod 48h 保鲜，上述 4 颗已 8 小时）

**日配额**：ET 2026-11-01，REGULAR 0/4 已用 ⇒ 今天最多只能提 **4 颗**（篮子 5 颗需跨两天）。

---

## 七、待用户裁定（三件）

1. **提交授权** —— 提几颗？（5 颗全提 / 今天先提 4 颗 / 按更严覆盖口径提 3 颗）
2. **R2 组合上限是否放宽到 ≥7** —— 不放宽则本轮封顶 15 颗，20 颗不可达
3. **`leading gap` 是否除名** —— `QPvJ6KVw`（2014 空/2015 仅 363）、`npv9WLVE`（2014 空/2015 仅 50）按「连续多年空窗」判据不除名；若采用更严口径，篮子降为 3 颗（`RRE3O8r1` + `d5WqeQbx` + `Xg9rMdvl`）
