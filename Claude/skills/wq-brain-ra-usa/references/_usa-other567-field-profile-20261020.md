# other567（Employee Review 员工评价）字段画像与回测档案（USA / D1 / TOP3000）

> 快照日：2026-10-20。来源：`get_datafields(region="USA", delay=1, universe="TOP3000", dataset_id="other567")`。
> 结构：§1 字段画像 · §2 适用模板与机制 · §3 回测结果及指标 · §4 归因 · §5 决策。
> 设置：USA / TOP3000 / D1 / SUBINDUSTRY / decay 5 / trunc 0.08 / VERIFY / nan ON / pasteurization ON / maxTrade OFF。

## §1 字段画像

数据集元数据：193 个字段（`get_datafields` 去噪后实得；平台原始返回含 30 个被过滤项），**全部 VECTOR**，位于未点亮 `other` 塔，数据集 aC 544 / cov 0.5088；无 `dead_end` 记录。

字段按用途分五层，只有前两层可作信号：

| 层 | 代表字段 | cov | uC / aC | 语义 | 可用性判断 |
|---|---|---:|---|---|---|
| **A. 公司月度均分（1–5）** | `avg_overall_company_score` / `avg_business_outlook_score` / `avg_ceo_approval_score` / `avg_culture_values_score` / `avg_diversity_inclusion_score` / `avg_pay_and_benefits_score` / `avg_recommend_to_peer_score` / `avg_senior_management_score` / `avg_work_life_balance_score` / `avg_career_growth_score` | ≈0.62 | uC 1–9 / aC 0–12 | 员工月度评价均分（Glassdoor 风格） | **主信号池**；uC/aC 极低 ⇒ 拥挤度低 |
| **B. 文本衍生情绪** | `career_advancement_sentiment_score` 等 | 0.6246 | 低 | 评价文本的情绪分 | 次信号；与 A 层同源，警惕近重复 |
| **C. 年度趋势评级** | `oth567_trendrating_*`（rolling yearly avg） | 0.4780 | 低 | 12 个月滚动均分 | 慢测量面；覆盖明显更低 |
| **D. 年度趋势变化** | `oth567_trend_deltarating_*` | 0.5079 | 低 | 趋势变化量 | 变化量口径；覆盖更低 |
| **E. 个体评分** | `oth567_individualrating_*` | 0.44–0.55 | 低 | 单条评价级 | 需聚合，噪声大 |
| **F. 标识符 / 分类码** | SEDOL / ticker / CUSIP / LEI / CIK / NAICS / SIC / MSA / country / city / state、role codes、review text | — | — | 元数据 | **不可作信号**（名义量 / 文本） |

**VECTOR 处理**：`avg_*` 是「该公司当月全部评价的均分」按评价维度展开的向量（每条评价一个元素），`vec_avg` 才是「评分的评分」；亦可用 `vec_max` / `vec_sum` 但语义退化为「最高分评价」/「总分」，不作为首选。批 1 只测 `vec_avg`（与 A 层语义一致），聚合对照留给补批。
**覆盖**：0.62 属中等覆盖，`ts_backfill(...,252)` 后有效覆盖进一步上升；C/D/E 层（0.44–0.51）需更长回填。
**更新频率**：月度级（company-month），属慢变量；TO 预期 1–3%，须盯 LOW_TURNOVER。

## §2 适用模板与机制

| 机制 | 经济陈述 | 构造 | 预期符号 |
|---|---|---|---|
| M1 员工满意度溢价 | 高员工评价 = 人力资本质量/管理效率，市场定价不足 | `rank(avg_overall)` | 待测 |
| M2 前瞻维度 | 对业务前景的评价领先于财务报表（员工最先感知订单/裁员） | `rank(avg_business_outlook)` | 待测 |
| M3 管理层维度 | CEO 认可度 = 治理质量代理 | `rank(avg_ceo_approval)` | 待测 |
| M4 维度价差 | 总体评价 − 薪酬评价 = 非货币满意度倾斜；薪酬不满但总体高 = 文化补偿 | `rank(overall − pay)` | 待测 |
| M5 评价变化 | 月度评价的滚动变化 = 情绪转折（领先于评级下修） | `Δ63(overall)` | 待测 |
| M6 长窗时序位置 | 慢变量最优测量面（board_gov / cre / other327 三次实证） | `ts_rank(overall, 504)` | — |
| M7 文本情绪 | 文本分与评分独立的情绪通道 | `rank(career_advancement_sentiment)` | 待测 |
| M8 年度趋势 | 12 个月滚动均分平滑掉月度噪声 | `rank(trendrating_overall)` | 待测 |

**通用壳**：`quantile(group_rank(winsorize(ts_backfill(<SIG>, 252), std=4), industry))`。
**ATOM 合规**：A/B/C 层同属 other567；M4 价差为同数据集内两字段；F 层不入信号。
**文献锚**：Edmans (2011) *Does the Stock Market Fully Value Intangibles? Employee Satisfaction and Equity Prices*；Green–Huang–Wen–Zhou (2019) 员工满意度与股票收益。只取机制，不取参数。
**预注册止损**：
1. 8 条全 `|S| < 1.0` ⇒ 判弱封存 `USA-OTHER567-EMPLOYEE-REVIEW-WEAK`，不补批；
2. M1/M2/M3 三条水平同号且两两差 < 0.10 ⇒ 维度无独立信息，只保留最强一条；
3. 任一 `|S| ∈ [1.25,1.58)` 且 rns ≥ 0.5 ⇒ Mode A，**先测 prod**；
4. 任一全闸 ⇒ `check_correlation(refresh=True)`，按 D0-P 判交付。

## §3 回测结果及指标

**批 1（multisim `Gbt0W4Fg4n5afPTaPixc1u`，8 条，2026-10-20）**：8/8 COMPLETE，0 ERROR。设置见文首；区间 2014-01-01 → 2023-12-31。

| # | 机制 | alpha | S | F | 2Y | SUB（限） | TO | ret | DD | rns | 失败闸 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | M1 overall 水平 | `78on6WkZ` | 1.77 | 1.24 | 1.49 | 0.75（0.77） | 1.48% | 6.15% | 7.62% | 1.91 | SUB / 2Y |
| 2 | M2 business_outlook | `Vkd30VvA` | 1.52 | 1.05 | 1.36 | 0.59（0.66） | 1.47% | 6.02% | 10.10% | 1.74 | S / F / SUB / 2Y |
| 3 | M3 ceo_approval | `JjPvQqjl` | 1.59 | 1.11 | 1.49 | 0.65（0.69） | 1.39% | 6.13% | 9.33% | 1.63 | SUB / 2Y |
| 4 | M4 overall − pay | `j2er8v2Z` | 1.71 | 1.20 | 1.34 | 0.54（0.74） | 1.70% | 6.16% | 4.95% | 1.84 | SUB / 2Y |
| 5 | M5 Δ63(overall) | `9qE7WYq2` | 1.30 | 0.89 | 1.11 | 0.44（0.56） | 1.36% | 5.82% | 8.50% | 0.85 | S / F / SUB / 2Y |
| 6 | M6 ts_rank504(overall) | `RRA16Mjj` | 1.74 | 1.27 | 1.40 | 0.62（0.75） | 1.82% | 6.65% | 5.40% | 1.85 | SUB / 2Y |
| 7 | M7 career_advancement_sentiment | `58jkgxnM` | 1.82 | 1.30 | 1.82 | 0.63（0.79） | 11.48% | 6.38% | 4.96% | 1.62 | **仅 SUB** |
| 8 | M8 trendrating_overall | `leM3Kdp8` | 1.85 | 1.38 | 1.56 | **1.12 PASS** | 1.24% | 6.94% | 9.79% | 1.94 | 无硬失败（2Y 为 warning） |

**prod 实测（`check_correlation(refresh=True)`，D0-P 权威）**：`leM3Kdp8` = **0.8846**（落在 [0.8,0.9)，该桶 n=571）；`58jkgxnM` = **0.8641**（[0.8,0.9)，n=131）。

## §4 归因

1. **信号是真的，不是风格代理**：8/8 的 `risk_neutralized_sharpe` 落在 **0.85–1.94**，其中 7 条 ≥1.62 —— 员工评价截面在扣除风格后仍有独立信息。这也是本族与 event_relation（rns 0.29）最本质的区别。
2. **家族的统一短板是「小盘依赖」而非信号弱**：7/8 挂 `LOW_SUB_UNIVERSE_SHARPE`、6/8 挂 `LOW_2Y_SHARPE`，而 `LOW_SHARPE` 只有 3/8 挂。即信号在大票池里衰减、且近年才变强。它没死在 IS，死在**容量与时段**。
3. **M1/M2/M3 三维度差 > 0.10（1.77 / 1.52 / 1.59）** ⇒ 维度携带独立信息，预注册止损 2 未触发；但同号，说明是同一个「员工满意度溢价」的不同切面，不宜当三条独立 alpha 交付。
4. **M4 价差（overall − pay）S 1.71 且 DD 仅 4.95%，是本族最干净的一条**：非货币满意度与总体评价的背离，比任何单维水平都稳（回撤最低）。可惜 SUB 0.54 / 2Y 1.34 更差。
5. **M6 长窗时序位置（ts_rank504）S 1.74 且 DD 5.40%** —— 与 board_gov / cre / other327 的「慢变量用长窗」结论一致，是本族对既有规则的又一次复证（对比 event_relation 的反例）。
6. **M8 trendrating（12 个月滚动均分）是本族最优**：S1.85 / F1.38 / SUB 1.12 PASS / TO 1.24% / rns 1.94，2Y 1.56 只是 warning 差 0.02。平滑掉月度噪声后信号最强 —— 与「员工评价是慢变量」的结构判断吻合。
7. **M7 文本情绪是唯一 TO 破 11% 的**（11.48%，其余 1.24–1.82%）：文本分月度跳变大、稳定性差；但也正因此 2Y 达 1.82 PASS。
8. **转折点 = prod 0.8846 / 0.8641**。两条最强候选在 prod 上都落进 [0.8,0.9) 且该桶已有数百条历史 alpha ⇒ 按 D0-P 这是**结构性饱和**，不是「再调一档就能过」。员工满意度是美股上被反复挖掘的经典因子（Edmans 2011 之后），平台已有大量同源 alpha，与我们的 rns 高、IS 强同时成立 —— 即「真的有效，所以已经拥挤」。

## §5 决策

- **封存 `USA-OTHER567-EMPLOYEE-REVIEW-PROD-WALL`**（D0-P：prod ∈ [0.8,0.9)，n=571 / n=131）。
- **不做 Mode A**：D0-P 明令 prod 达线后禁止同族磨参数/换壳变体 —— 换 decay / 窗口 / 中性化只会换一个 prod 仍 ~0.85 的 alpha。
- **不补批**：聚合对照（vec_max / vec_sum）、维度价差扩展、C/D/E 层扫描都只会产出同一 prod 桶内的更多候选。
- **salvage 5 条转入 SUPER 组合腿候选池**（各条 TO 低、rns 高、彼此同源但截面上有细分差异）：`leM3Kdp8`（trendrating，S1.85/SUB1.12）、`58jkgxnM`（career sentiment，2Y1.82）、`78on6WkZ`（overall）、`j2er8v2Z`（overall−pay，DD4.95%）、`RRA16Mjj`（ts_rank504，DD5.40%）。
- **可复用结论**：① 员工评价族在 USA 的 prod 地板约 0.86–0.88，IS 全闸也救不回来 —— 下一轮遇到「员工/雇主评价」类数据集先查 prod 桶再决定是否投仿真；② 该族 `rns` 高是常态（1.6–1.9），rns 高 ≠ 可提交，prod 才是墙；③ 文本情绪腿 TO 是水平腿的 9 倍（11.48% vs 1.24%），做组合时注意换手贡献。
