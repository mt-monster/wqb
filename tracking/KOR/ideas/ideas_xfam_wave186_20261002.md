# KOR / cross-family slow×fast / D1 — s2_xfam_d1

**Region**: KOR (TOP600, delay1, STATISTICAL, decay4, truncation 0.08)
**Pyramids**: other（慢腿 other466）+ shortinterest（快腿 shortinterest38）
**Generated**: 2026-10-02

## 为什么是 bucket 分组轴，而不是 add(multiply())

用户硬约束原文：「组合信号明确区分**主信号 vs 辅助信号**，辅助信号可考虑 **bucket 自定义分组**，
**禁止 add(A,B) 裸混信号**」。

`win_replay_slow_fast_v1` 写的「0.40 慢残差 × 0.60 正交金字塔快腿」是**加权相加**，直接违反
`mixed_signal_leg_ban_v1`。两者调和点在于**辅助信号的角色**：

| | 违规 | 合规（本波） |
|---|---|---|
| 快腿做什么 | 贡献一半持仓权重 | **只切分主信号的比较范围** |
| 形态 | `add(multiply(0.4,慢), multiply(0.6,快))` | `group_rank(主信号, bucket(快腿, ...))` |
| 语义 | 两个信号各投一半 | 一个信号，**按快腿状态分组比较** |

⇒ 快腿不产生持仓，只改变横截面比较域。**这是"条件化"不是"叠加"。**

## ★ 正交性已实测（不是假设）

`compute_mutual_correlation(['A1NXddRw','rKOadrRj'], threshold=0.4, years=4)`：

```
matrix: A1NXddRw ↔ rKOadrRj = **-0.0843**
num_points: 1023
all_below_threshold: true
```

- `A1NXddRw` = other466 慢腿代表（S2.11/F1.81/2Y1.95，prod 0.6547，已 ACTIVE）
- `rKOadrRj` = shortinterest38 快腿代表（S2.02/F1.12）

**1023 个日收益点的实测相关 −0.084 ≈ 完全正交**。满足硬约束「不同数据集策略间相关性 < 0.4」。

## 两族骨架（均已在本区验证）

**慢腿 other466（other 塔，倍率 1.6×）** — 财务比率慢变量，长窗 504：
```
signed_power(ts_rank(group_rank(divide(分子, 分母), market), 504), 0.5)
```
已测 28 个组合，**分母 18 次集中在 `bs_assets_tot_q` ⇒ 分母维度是最大的未测空间**。

**快腿 shortinterest38（shortinterest 塔，倍率 1.4×）** — 卖空活动买卖比，短窗 5：
```
group_rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt),
                                     vec_sum(shrt38_stk_invactbuy_amt)), 504), 5), sector)
```

---

## Concept 1 — ROE 慢腿 × 卖空活跃度分桶（主推）

**经济机制**：净资产收益率是慢变量（季度更新、长窗定价）。但 ROE 的**市场解读**随卖空活动状态而变：
卖空活跃期，市场更关注"盈利质量是否被质疑"，高 ROE 的信号含义被放大/反转。
用卖空活跃度做分组轴，等于**让 ROE 在"不同卖空压力状态"内各自排序**——
经济上是条件化比较，不是两条信号相加。

**Implementation Example**:
```
group_rank(signed_power(ts_rank(group_rank(divide(oth466_is_net_profit_12m_q, oth466_bs_eq_tot_q), market), 504), 0.5), bucket(rank(group_rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 504), 5), sector)), range="0,1,0.25"))
```
**未测点**: `is_net_profit_12m_q / bs_eq_tot_q`（ROE）分母维度未测（已测分母全是 bs_assets_tot_q）
**算子数**: 11 ⚠ 超 10 上限 → 见下方"复杂度"说明
**形态**: 主信号 + bucket 分组轴，合规

---

## Concept 2 — 现金流回报慢腿 × 卖空分桶（降复杂度版）

**Implementation Example**:
```
group_rank(signed_power(ts_rank(group_rank(divide(oth466_cf_oper_q, oth466_bs_eq_tot_q), market), 504), 0.5), bucket(rank(group_rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 504), 5), sector)), 5))
```
**未测点**: `cf_oper_q / bs_eq_tot_q`（经营现金流/权益 = 现金流回报率）
**算子数**: 11
**bucket 变体**: 本槽用等分 5 档（与 C1 的 range 步进档形成多样性）

---

## Concept 3 — 简化版（≤10 算子，优先）

**降复杂度思路**：主信号去掉外层 `signed_power`（它只是压尾，`group_rank` 本身已秩化），
快腿去掉内层 `group_rank(·,sector)`（bucket 只需序数）。

**Implementation Example**:
```
group_rank(ts_rank(group_rank(divide(oth466_is_net_profit_12m_q, oth466_bs_eq_tot_q), market), 504), bucket(rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 504), 5)), 5))
```
**算子数**: 10（ts_zscore, vec_sum×2, divide, ts_mean, ts_rank, rank, bucket, group_rank×2）
**风险**: 少了 signed_power 压尾，极端值敏感性上升 → 看 CONCENTRATED_WEIGHT

---

## Concept 4 — EV 类慢腿（换分母 = 换经济量）

**Implementation Example**:
```
group_rank(ts_rank(group_rank(divide(oth466_is_ebitda_oper_q, oth466_des_mkt_cap_q), market), 504), bucket(rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 504), 5)), 5))
```
**未测点**: `is_ebitda_oper_q / des_mkt_cap_q`（EBITDA/市值，EV 收益率类，全新经济量）
**算子数**: 10

---

## Concept 5 — 资产周转慢腿（流动资产分母）

**Implementation Example**:
```
group_rank(ts_rank(group_rank(divide(oth466_is_oper_inc_q, oth466_bs_assets_curr_q), market), 504), bucket(rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 504), 5)), 5))
```
**未测点**: `is_oper_inc_q / bs_assets_curr_q`（营业利润/流动资产 = 流动资产回报）
**算子数**: 10
**注意**: `oth466_is_oper_inc_q` 被 prod-sat 标为历史饱和字段，但 A1NXddRw（同分子）prod 0.6547 仍过
⇒ 换分母可能绕开饱和（同分子不同分母 = 不同经济量）

---

## Concept 6 — 快腿换几何（ts_corr 版本作分组轴）

**经济机制**：C1–C5 用"买卖比"作分组轴。本槽改用 **`ts_corr(卖方, 买方, 42)` 的反向** ——
这衡量的是买卖**同步性**而非**比值**。卖买高度同步 = 无信息噪声；背离 = 单边压力。
`reverse(ts_corr(...))` 是 kor_w201 实证过的形态（rKOadrRj S2.02）。

**Implementation Example**:
```
group_rank(ts_rank(group_rank(divide(oth466_is_consol_net_inc_q, oth466_bs_assets_curr_q), market), 504), bucket(rank(reverse(ts_corr(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt), 42))), 5))
```
**未测点**: 分子分母组合 + 快腿几何双重变化
**算子数**: 10

---

## Concept 7 — 短窗慢腿 × 分组轴（周期错配对照）

**经济机制**：C1–C6 慢腿全是 504 长窗。本槽把慢腿降到 **252**，测"周期错配度"对混合的影响。
`win_replay_slow_fast_v1` 强调跨周期；本槽是对照组，验证 504 是否真的是最优错配点。

**Implementation Example**:
```
group_rank(ts_rank(group_rank(divide(oth466_is_net_profit_12m_q, oth466_bs_eq_tot_q), market), 252), bucket(rank(ts_mean(ts_zscore(divide(vec_sum(shrt38_stk_invactsell_amt), vec_sum(shrt38_stk_invactbuy_amt)), 504), 5)), 5))
```
**算子数**: 10
**作用**: 与 C3 形成唯一变量对照（仅慢腿窗口 504→252）

---

## 槽位分配（7 槽 + 1 补）

| 槽 | Concept | 慢腿(分子/分母) | 慢腿窗 | 快腿几何 | bucket 档 |
|---|---|---|---|---|---|
| A1 | C1 | is_net_profit_12m_q / **bs_eq_tot_q** | 504 | 买卖比 | range 0.25 |
| A2 | C3（简化） | is_net_profit_12m_q / **bs_eq_tot_q** | 504 | 买卖比 | 等分 5 |
| A3 | C4 | is_ebitda_oper_q / **des_mkt_cap_q** | 504 | 买卖比 | 等分 5 |
| A4 | C5 | is_oper_inc_q / **bs_assets_curr_q** | 504 | 买卖比 | 等分 5 |
| A5 | C2 | cf_oper_q / **bs_eq_tot_q** | 504 | 买卖比 | 等分 5 |
| B1 | C6 | is_consol_net_inc_q / **bs_assets_curr_q** | 504 | **ts_corr 反向** | 等分 5 |
| B2 | C7 | is_net_profit_12m_q / **bs_eq_tot_q** | **252** | 买卖比 | 等分 5 |

**注**：C1/C2（11 算子）超复杂度上限，本波**先发 10 算子版本**（A1 改用 C3 简化骨架），
若 10 算子版表现优异再单独破例上 11 算子版。

## 多样性自检（六维）

- **算子**: ts_rank / group_rank / divide / ts_mean / ts_zscore / vec_sum / bucket / rank / ts_corr / reverse → 10 类 ✅
- **字段**: other466 分子 5 种、分母 3 种；shortinterest38 字段 4 个（sell/buy amt + ts_corr 版）✅
- **骨架**: 7 条同构（group_rank(主, bucket(快))）⚠ **骨架单一** —— 这是本波的**有意设计**：
  本波是"验证 bucket 分组轴这一混合形态是否成立"的**单变量实验**，
  多样性由"分子分母经济量"承担，跨波多样性由后续波承担。
  若门禁多样性闸 FAIL，按 SOP 用 PROBE_BATCH waiver（曾用于 ASI pattern_scores 批）。
- **预处理**: ts_zscore / ts_rank / group_rank / signed_power(C1/C2) ✅
- **收益来源**: ROE / 现金流回报 / EV 收益率 / 流动资产回报 / 净利润/流动资产 ✅ 5 个不同经济量
- **失败风险**: prod 饱和（oth466_is_oper_inc_q 已标饱和）/ CW（无 signed_power 时）/ prod 墙 ✅ 已识别

## 硬约束核对

- [x] 每条只用 1–2 个 catalog 字段族（other466 + shortinterest38 = 2 个数据集，跨族）✅
- [x] 两腿实测相关 −0.0843 < 0.4 ✅
- [x] 无 `add(multiply(w,A), multiply(1-w,B))` 混信号 ✅
- [x] 辅助信号仅作 bucket 分组轴，不产生独立持仓 ✅
- [x] 窗口只用标准窗（5/42/252/504）✅
- [x] 不同数据集策略间相关性 < 0.4 ✅
- [x] 跨金字塔（other 塔 1.6× + shortinterest 塔 1.4×）✅
