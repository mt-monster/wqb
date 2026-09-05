---
region: GBR
entry_verdict: active
one_liner: "达成区扩挖：4 ACTIVE（全闸过 2 + rn 弱 2）+ 白名单 10 数据集（8-26 建），目标累计 10 → 再挖 6"
static:
  universe: [TOP700]  # 8-26 实测确认合法，settings_proven 同源
  universe_default: TOP700
  delay: [1, 0]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "TOP700/delay1/SUBINDUSTRY 为 region_kb settings_proven 实测；delay0 可探"
datasets:
  red: [predictive_starmine, analyst_earnings_ibes, pattern_scores, other455, model264, news104, model53, fund_holdings_panel, news17, analyst9, news20]
  red_reason: "s0_whitelist_2026-08-26 excluded：PROD 饱和 4 族 + 简单结构判死 3 + dead 标记 5（registry dead_end 层 10 条实证）"
  yellow: []
  green: [model238, model106, dl_riskfree_returns, institutions6, news18, sentiment27, shortinterest3, model28, model36, pv29]
priors:
  signal_families_include: [model, institutions, news, sentiment, shortinterest, pv]
  signal_families_exclude: [starmine, analyst_estimate, pattern_scores, other455, model264, dl_riskfree_label, model238_rank]
  syntax_patterns: []
  win_recipes:
    - "starmine 四向价值结构（PROD 饱和，机制换腿复用）"
    - "delta66 双时序差分家族（PROD 饱和，机制换腿复用）"
    - "other455×model264 跨数据集混合（PROD 饱和，机制换腿复用）"
    - "（机制）EUR 0.4 慢 MODEL 残差 + 0.6 快 PV（T-KB-01 验证中）"
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 2
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(GBR) registry dead_end 层 10 条（8-26 回写）"
  last_verified: 2026-08-26
---

# GBR — 达成区扩挖（4 ACTIVE → 目标累计 10）

## 定位与实证依据

GBR 已从"半空白探针态"升级为**达成区**：region_kb 4 ACTIVE（GrlqxwKx/vRNk56mz 全闸过，A1G7o1EE/WjAV89jG rn 偏弱但仍 OS ACTIVE）+ 3 条 win_recipes（全部 PROD 饱和，仅机制换腿复用）+ registry dead_end 10 条（8-26 回写）+ s0_whitelist 10 数据集（8-26 建）。市场结构与 EUR 相近，EUR 机制（0.4 慢 MODEL × 0.6 快 PV）可作换腿先验，但**借用≠验证**：本地回测确认后才能回写 win 层。

## 流程变体（相对九步骨架）

### 步 1 注入：查表即白名单

registry dead_end 10 条 + s0_whitelist_2026-08-26 10 数据集 + wave29/30 FAIL 结论（model238 天花板 0.68 / dl_riskfree label 2Y 崩）已在 DB，步 1 直接消费，不再从零探。

### 步 2 注入：白名单即候选

10 数据集白名单（model238/model106/dl_riskfree_returns/institutions6/news18/sentiment27/shortinterest3/model28/model36/pv29）已锁；S1/S2 已完成 6 数据集（s2_*_d1_idea），剩余 4 个（sentiment27/shortinterest3/model28/model36）步 3 补扫。

### 步 4 注入：win 机制换腿优先

本波至少 2 槽按 win 机制（T-KB-01 慢×快跨周期混合 / T-KB-05 长窗强 2Y / T-KB-07 四向价值）换白名单字段腿；禁用 PROD 饱和族字段。priors 走 `campaign.py assemble-priors`（DB KB 组装）。

### 步 9 注入：判死回写闭环

每波 FAIL 后必须 registry add-dead-end + 可精确定义的族加 methodology_rules dead_end 规则（L3 拦截），不得只写 findings 了事；win 过闸即回写 region_kb win_recipes（时机前置）。

## priors

wins:
- T-KB-01 慢×快跨周期混合：rank(add(multiply(w_s, rank(SLOW_FIELD)), multiply(w_f, rank(FAST_FIELD))))，权重 0.4/0.6 起步，必须跨周期/跨数据源（EUR Wj71Q12o ACTIVE 先例）
- T-KB-05 长窗结构强 2Y：rank(ts_rank(ts_backfill(F, 66), 250)) + decay 6-8（IND 三颗 ACTIVE 先例）
- T-KB-07 四向价值结构：ep_yield fy2 av_diff + fwdPE 反转 + fy1 水平 + delta66/22 双差分（GBR 4 ACTIVE，PROD 饱和仅换腿）
- T-KB-02 镜像反转翻案：探针批 |sh|≥1.0 强负 → 下一批必做镜像反转，不是判死

dead_ends:
- GBR-PROD-SATURATED：starmine 四向 + delta66 + pattern_scores + other455×model264 已 4 ACTIVE 禁同族变体（机制可换腿）
- GBR-DLRISKFREE-LABEL-DEAD：quantile_label/probability_label 族 2Y 崩（wave30 max sh 1.09 / 2Y -0.05）
- GBR-MDL238-RANK-CEILING：model238 排名类天花板 0.68（wave29 9/9 FAIL），仅可作复合从腿
- GBR-SIMPLE-STRUCTURE-DEAD：news104/pattern_scores/model264 简单结构判死（wave26-28）
- GBR-TIER1-EXHAUSTED：tier1 挖穿（8-18），聚焦白名单 tier2/3

settings:
- SUBINDUSTRY + decay4 跟 win（EUR 实证）；可另探 ILLIQUID_MINVOL1M / TOPCS1600 / delay0
- TOP700 / delay1 为主（region_kb settings_proven）

## 避坑清单

- 禁止把 EUR win 当 GBR win 直接引用（跨区配方必须本地验证）。
- PROD 饱和族（starmine/ibes/pattern_scores/other455×model264）不生成新变体，机制换腿除外。
- 白名单外禁止 generate / simulate；model238 只允许复合从腿。
