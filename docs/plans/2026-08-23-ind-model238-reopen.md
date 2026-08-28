# IND model238 判死翻案计划（跨族反腿组合稀释）

> 状态：**已执行 → 升级判死封存**（wave89 跨族反腿 + wave91 残差差分模板两波翻案均失败，2026-08-24；结论见 §9/§10）
> 目标：验证"model238 主腿 × 跨数据集反腿"能否把 prod 从 0.85 压到 <0.7
> 止损线：1 波 8 条；若最优 prod ≥ 0.75 → 升级判死"跨族稀释也无效"，彻底封存

## 1. 背景与质疑点

registry 已判死 `IND-MODEL238-PROD-SATURATED`（family=model238 SmartHoldings）：

- wave86 单因子 8 条：prod 0.88-0.92 全撞（信号真实，S=1.86/1.86/1.73）
- wave87 内部组合 8 条：`add(multiply(rank(mdl238_global_rank),w), multiply(rank(mdl238_global_change_rank),1-w))`
  - robust 0.87→1.01 破墙 ✓，2 候选 QP7narVg（S=1.83/F=1.53/2Y=1.77）、3qlE7YeZ（S=1.75）
  - 但 prod 仅 0.92→0.847/0.86，双撞

**判死质疑（用户提出，经分析成立）**：wave87 只试了 **mdl238 内部两腿**稀释。两条腿都在平台 prod 池里（r_A≈0.92、r_B≈0.85），内部加权的 prod 数学下限 = 最弱腿 ≈0.85——0.847 实证吻合。**跨数据集反腿（换信号构成）从未试过**，而这是 KOR 强 DL 判死记忆的"唯一有效手段"、且 IND 已有成功先例：vRje2ZGd = score_5d（prod 0.8238）× reverse(upgrades) → **0.6908 PASS**。

## 2. 数学可行性

`prod_new ≈ w×0.85 + (1-w)×r_腿3`（线性近似，KOR/IND 实证吻合）：

| 反腿 prod（r_腿3） | w=0.65 | w=0.6 | w=0.55 |
|---|---|---|---|
| 0.3（与池低相关，期望值） | 0.66 ✓ | 0.63 ✓ | 0.60 ✓ |
| 0.5（半拥挤） | 0.73 ✗ | 0.71 ✗ | 0.69 ✓ |
| 0.6+（拥挤） | ✗ | ✗ | ✗ |

结论：**成败完全取决于反腿自身 prod 足够低**，必须预筛。

## 3. 反腿候选短名单（初筛后 4 个）

全部来自 analyst_revision_horizons（wave46 实证的 IND 超调反转负信号族，取反后为正贡献腿）：

| 反腿 | wave46 实证 | 与 vRje2ZGd 冲突风险 | 备注 |
|---|---|---|---|
| `analyst_revision_percentile_score_medium_4` | S=-1.19~-2.40 强负 | **低**（与 score_5d 不同源） | 首选 |
| `analyst_recommendation_downgrades_30d_medium_31` | 负信号 | **中**（与 upgrades 同族） | 备选 |
| `analyst_count_increasing_current_year_earnings_14d_medium_3` | 负信号 | 低 | 备选 |
| `analyst_opinion_avg_shift_30d_short` | 弱负 | 低 | 备选 |

**禁用**：`analyst_recommendation_upgrades_*`（vRje2ZGd 已占用，self 撞墙风险）；qfl/model216 字段（自身 prod 0.79-0.92 太高，做反腿无效）。

## 4. 预筛（回测前，MCP 直调，不烧回测配额）

1. `compute_mutual_correlation`：4 个反腿 vs **vRje2ZGd**（self 先验）——|corr|≥0.3 的反腿剔除换备选
2. `compute_mutual_correlation`：反腿 vs **mdl238_global_rank 单腿**（正交性验证）——期望 |corr|<0.5
3. 通过预筛的反腿才入批；若 4 个全被剔，追加候选（percentile 其他窗口/ts_rank 包裹版）再筛一轮

## 5. 8 条表达式草案（骨架=wave87 原生 add(multiply) 形式，方向为正）

主腿 `rank(mdl238_global_rank)`（wave87 破 robust 关键），反腿 `-rank(L)`（取反后正贡献，无需外层取反）：

1. `add(multiply(rank(mdl238_global_rank), 0.65), multiply(-rank(analyst_revision_percentile_score_medium_4), 0.35))`
2. `add(multiply(rank(mdl238_global_rank), 0.6), multiply(-rank(analyst_revision_percentile_score_medium_4), 0.4))`
3. `add(multiply(rank(mdl238_global_rank), 0.55), multiply(-rank(analyst_revision_percentile_score_medium_4), 0.45))`
4. `add(multiply(rank(mdl238_global_rank), 0.65), multiply(-rank(analyst_recommendation_downgrades_30d_medium_31), 0.35))`
5. `add(multiply(rank(mdl238_global_rank), 0.6), multiply(-rank(analyst_recommendation_downgrades_30d_medium_31), 0.4))`
6. `add(multiply(rank(mdl238_global_rank), 0.65), multiply(-rank(analyst_count_increasing_current_year_earnings_14d_medium_3), 0.35))`
7. `add(multiply(rank(mdl238_global_rank), 0.6), multiply(-rank(analyst_opinion_avg_shift_30d_short), 0.4))`
8. `add(multiply(rank(mdl238_global_screening_rank), 0.6), multiply(-rank(analyst_revision_percentile_score_medium_4), 0.4))`（备选主腿变体）

- 若 CW 墙出现 → 全批套 `ts_mean(..., 21)` 平滑变体（qfl 判死 salvage 配方）
- 设置：IND/TOP500/delay1/**SECTOR**/decay4/truncation 0.08（与 wave87 同轨可对比；prod 与中性化无关已被 KOR 记忆证实）

## 6. 执行步骤（主线程）

1. MCP `compute_mutual_correlation` 预筛（§4）
2. 表达式过 gate（**注意：跨数据集组合需合并 model238 + analyst_revision_horizons 两份 catalog 的字段白名单**，gate 闸 2 按单 dataset 派生——执行前先确认白名单覆盖两数据集字段）
3. pipeline 批量回测 8 条（五槽填槽）
4. 核验 prod/self（MCP check_correlation 直调）
5. 按 §7 裁决

## 7. 裁决规则

| 结果 | 动作 |
|---|---|
| 任一 prod<0.7 且 self<0.7 且 S≥1.58 | **翻案成功**：走 S4/S5 评审链提交；registry 更新 salvage="跨族反腿组合有效（percentile/downgrades 反腿）" |
| 最优 prod∈[0.7, 0.75) 但接近 | 回 S4 优化（w 梯度微调 + 反腿替换）再给 1 波 |
| 最优 prod ≥ 0.75 | **升级判死**：registry salvage 从"无"改为"内部组合+跨族反腿均无效，prod 地板结构性 0.75+"，rule 追加限定，彻底封存不再争议 |

## 8. 风险清单

1. **self 撞 vRje2ZGd**：预筛兜底（|corr|<0.3 才入批）
2. **robust 墙回归**：wave87 robust=1.01 靠内部组合抬出；跨族腿可能拖低——若 robust 回落，回退"内部组合 + 轻量跨族反腿（w 反腿≤0.3）"变体
3. **sharpe 稀释**：SECTOR 轨基底 S=1.83，反腿权重 0.35-0.45 后要保 1.58+
4. **配额成本**：1 波 8 条回测；daily_remaining 提交配额不受影响（本波只回测不提交）
5. **优先级**：若 wave48/49 analyst 主线仍在产粮，本翻案波可排后

## 9. 执行结果（2026-08-24）

wave89 跨族反腿波（8 条，SECTOR/TOP500/delay1/decay4/trunc0.08，multisim 3XL8sk8bg4qxcouH9OR9CN6）回测 + prod/self 核验完毕，**翻案失败，升级封存**。

| alpha | 反腿（权重） | S | fitness | prod | self |
|---|---|---|---|---|---|
| 3qlEeN8N | earnings_30d (0.5) | 1.35 | 1.08 | **0.7034** | — |
| qMjn6RQj | earnings_14d (0.4) | 1.51 | 1.25 | 0.7509 | — |
| 3qlEeNNN | opinion_shift (0.4) | 1.27 | 0.94 | 0.7562 | — |
| Xg7k8djl | ebitda_14d (0.4) | 1.49 | 1.20 | 0.7600 | — |
| 3qlEe8Qg | downgrades (0.4) | 2.03 | 1.89 | 0.7664 | 0.3823 ✓ |
| 2rlvN3r6 | downgrades (0.3) | 1.98 | 1.83 | 0.7997 | 0.3861 ✓ |
| 1YwozrYQ | percentile (0.4) | 2.37 | 2.53 | 0.8243 | 0.5639 ✓ |
| xAjedJKW | percentile (0.3) | 2.24 | 2.30 | 0.8326 | 0.5236 ✓ |

- 无一条同时满足 prod<0.7 且 self<0.7 且 S≥1.58 → 翻案失败。
- 关键发现：跨族反腿**确实能把 prod 压到 0.70 边缘**（earnings_30d w0.5 → 0.7034，打破原 0.85 地板预判），但代价是 S 稀释至 1.35；而保 S 的强腿（percentile/downgrades，S 1.98-2.37）prod 0.77-0.83 全撞。S 与 prod 在权重轴上互斥，双闸无交集，§7 中间分支"再给 1 波"结构性无解。
- self 全部 0.38-0.56 通过，不是障碍。
- registry：`IND-MODEL238-PROD-SATURATED` 已升级（reason/rule 追加 wave89 证据链，salvage 改为"内部组合+跨族反腿均无效"，dead_at 补 2026-08-24）；wave_results wave89 已闭账 RED。
- 可迁移配方沉淀：组合梯度稀释破 robust + 反腿选 earnings/count 族（r≈0.56 远低于 percentile/downgrades 族 r≈0.79）压 prod，仅适用于主腿 S 余量充足的族。

## 10. 残差差分模板翻案波（wave91，2026-08-24）

wave89 判死后用户选定开一次性翻案批（例外条款 `wavewave91_verdict`，理由：残差差分模板 `rank(ts_zscore(A,w) - ts_zscore(group_neutralize(A,sector),w))` 是唯一未实测的降 prod 武器——剥行业暴露属换信号构成）。8 条：3 纯残差（w63/21/10）+ 3 残差×earnings + 2 残差×强S腿。multisim `3FAkMZceh4I6bWGaflY3G2Q`，SECTOR/TOP500/delay1/decay4/trunc0.08。

| alpha | 组合 | S | fitness | prod | self |
|---|---|---|---|---|---|
| wpj59PW5 | 纯残差 63 | 0.11 | 0.02 | **0.2009** ✓ | 0.0205 ✓ |
| mLjqY1Q6 | 纯残差 21 | -0.47 | -0.17 | — | — |
| RR7NAKPz | 纯残差 10 | -0.20 | -0.04 | — | — |
| A1lnQmEX | 残差63×earnings30d 0.6/0.4 | 0.25 | 0.08 | — | — |
| O07nJV2Y | 残差63×earnings30d 0.5/0.5 | 0.29 | 0.10 | — | — |
| ZY7jmM1Z | 残差21×earnings14d 0.6/0.4 | -0.11 | -0.02 | — | — |
| P07nM8Aw | 残差63×downgrades 0.7/0.3 | 0.69 | 0.35 | 0.3458 ✓ | 0.0022 ✓ |
| MP7b0Z2L | 残差21×percentile 0.7/0.3 | **1.40** | 1.01 | **0.6341** ✓ | 0.4535 ✓ |

- **prod 墙首次被破**：纯残差 0.2009（几乎归零）、downgrades 组合 0.3458、percentile 组合 0.6341——残差差分模板确实是 prod 解耦器。
- **但 S 全灭**：max 1.40（MP7b0Z2L）< 1.58 闸，纯残差 S 仅 0.11。残差化剥掉行业暴露的同时剥掉了信号本身——**model238 的 alpha 信号与被饱和的生产暴露同源**。
- 三闸（prod<0.7 / self<0.7 / S≥1.58）仍无交集 → 按用户二进制指令**翻案失败，升级封存**；例外条款已消费（结果回写 registry 后失效，禁止重发）。
- registry `IND-MODEL238-PROD-SATURATED`：reason 追加四波证据链；rule 升级为"prod 墙可破（残差差分），真墙是 S"；salvage 新增配方 2（可复用）：残差差分模板作 prod 解耦器（0.75→0.20 纯 / 0.63 配 0.3 权重信号腿），适用于任何生产饱和但信号可由非饱和腿重建的 alpha。
- wave_results wave91 已闭账 RED；台账键 `wavewave91_verdict` 终态 resolved。
