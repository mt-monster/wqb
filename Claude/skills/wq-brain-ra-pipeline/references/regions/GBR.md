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
  red: [predictive_starmine, analyst_earnings_ibes, pattern_scores, other455, model264, news104, model53, fund_holdings_panel, news17, analyst9, news20, earnings6, shortinterest3]
  red_reason: "s0_whitelist_2026-08-26 excluded：PROD 饱和 4 族 + 简单结构判死 3 + dead 标记 5（registry dead_end 层 10 条实证）。**2026-10-28 追加 2 条**：earnings6（平台 meta coverage=0.0 是 meta 造假，字段真实可回测，但 get_alpha_yearly_stats 实测 2014-2018 五年 pnl=0/持仓 0、2019 仅 24 多头 ⇒ 数据自 2019-12 起，**不满足『近十年都有数据』**；其 SUB 闸全灭根因是样本期短导致子宇宙统计退化，不是轴粒度）；shortinterest3（wave12 补测 6 条关闭死路留的口子，最好 S0.80，距硬闸 49%）"
  yellow: []
  green: [model238, model106, dl_riskfree_returns, institutions6, news18, sentiment27, model28, model36, pv29, news50]
priors:
  signal_families_include: [model, institutions, news, sentiment, shortinterest, pv]
  signal_families_exclude: [starmine, analyst_estimate, pattern_scores, other455, model264, dl_riskfree_label, model238_rank]
  syntax_patterns: []
  win_recipes:
    - "starmine 四向价值结构（PROD 饱和，机制换腿复用）"
    - "delta66 双时序差分家族（PROD 饱和，机制换腿复用）"
    - "other455×model264 跨数据集混合（PROD 饱和，机制换腿复用）"
    - "（机制）慢 MODEL 残差 × 快 PV 的跨周期 / 跨数据源结构（T-KB-01；只许以条件 / 分组 / 残差入场，**禁**加权 / 等权相加——2026-09-13 起闸 5 拦）"
gate_overrides:
  cw_gate: WARN
loop_policy:
  max_probes_per_wave: 2
  fast_kill: "缺省（决策表 D15：新数据集 8 探针无 |S|≥0.5 即判死）；本区无额外规则"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(GBR) registry dead_end 层 10 条（8-26 回写）"
  last_verified: 2026-08-26
---

# GBR — 达成区扩挖（4 ACTIVE → 目标累计 10）

## 定位与实证依据

### 2026-10-28 · 未点亮塔开波结论（s2_news50_d1 / s2_shortinterest3_d1，74 颗全 ATOM）

**塔位现状（当前季度 D1）**：model=5、analyst=3（已点亮）；pv=1、other=1（未满 3）；**NEWS=0、SHORTINTEREST=0、EARNINGS=0**（本轮主攻对象）。

**本轮实测**：74 颗 regular alpha 全部落在 NEWS（62）与 SHORTINTEREST（6）两座未点亮塔，**全部单数据集 ATOM**、零 PV/MODEL/OTHER 腿、窗口全在白名单、十年数据覆盖已用 `get_alpha_yearly_stats` 逐���核验。

**两条可复用的结论**：
1. **`news50` 的 `mws50_vea`（Aggregate Event Volume 91 日）均值回复是 GBR 未点亮塔唯一存活的横截面信号**，最佳 `1YNEqJbQ` S1.26 / F0.80 / 2Y1.79 / SUB0.89 / TO0.088（`failed_ra_count=2`，只差 LOW_SHARPE 与 LOW_FITNESS）。**等价算子替换（`ts_decay_linear(·,22)`）是决定性杠杆**：+0.21 S / +0.26 F / +0.62 2Y / −0.07 TO，且让 LOW_2Y_SHARPE 由 FAIL 转 PASS。详见 `references/news.md` 与 registry `GBR-NEWS50-VEA-MEANREV-WIN` / `GBR-NEWS50-VEA-S-CEILING-20261028`。
2. **本区信号含行业层面成分 ⇒ 用 `group_neutralize` 不用 `group_rank`**：vea 的 group_rank 版 S 从 1.03 腰斩到 0.52，group_neutralize 版 1.04/2Y1.20；ess 极性族同样（裸 0.67 → group_rank 后 −0.22）。

**★ 选集铁律（本区新增）**：带时间跨度要求时，**唯一权威是 `get_alpha_yearly_stats` 的逐年持仓数/pnl，不是平台 `coverage`**——`coverage=0` 可能是 meta 造假（earnings6 / news48 / option1 / analyst45 / macro27 同款）也可能是真空集。

**★ 塔位铁律**：本地 `backtest_results.dataset` 是**本地分组标签、不是平台塔位**。`KPrmWlwN`（S1.62 / 2Y1.89 / failed_ra_count=0）虽挂在 `shortinterest3` 分组下，表达式实际只用 `pv47_spret` 单字段、平台 `pyramid_short=pv` ⇒ **属 PV 塔**，别记成 SHORTINTEREST 产出。塔位判定唯一权威 = alpha 详情的 `ra.pyramid_short` / `pyramids.list`。

**★ 待办**：`KPrmWlwN` 是本区现成的 REGULAR 全闸通过候选（单字段 ATOM / 塔位 pv / PV 塔 1/3 未满），prod 实测受平台账号级单并发槽占用而未完成（inflight），prod<0.7 后走 `submit_verdict` → 用户确认 → `workflow_submit_alpha(confirm_submit=True)`。 <!-- from config.prod_corr_max -->

GBR 已从"半空白探针态"升级为**达成区**：region_kb 4 ACTIVE（GrlqxwKx/vRNk56mz 全闸过，A1G7o1EE/WjAV89jG rn 偏弱但仍 OS ACTIVE）+ 3 条 win_recipes（全部 PROD 饱和，仅机制换腿复用）+ registry dead_end 10 条（8-26 回写）+ s0_whitelist 10 数据集（8-26 建）。市场结构与 EUR 相近，EUR 的「慢 MODEL × 快 PV」跨周期结构可作换腿先验（其原配方是 0.4 / 0.6 加权相加，**已被 2026-09-13 起的路线 A 与闸 5 禁止**，只能改写成条件 / 分组 / 残差形态，见 optimization-v1 `structural-interaction-forms.md`），但**借用≠验证**：本地回测确认后才能回写 win 层。

## 流程变体（相对九步骨架）

### 步 1 注入：查表即白名单

registry dead_end 10 条 + s0_whitelist_2026-08-26 10 数据集 + wave29/30 FAIL 结论（model238 天花板 0.68 / dl_riskfree label 2Y 崩）已在 DB，步 1 直接消费，不再从零探。

### 步 2 注入：白名单即候选

10 数据集白名单（model238/model106/dl_riskfree_returns/institutions6/news18/sentiment27/shortinterest3/model28/model36/pv29）已锁；S1/S2 已完成 6 数据集（s2_*_d1_idea），剩余 4 个（sentiment27/shortinterest3/model28/model36）步 3 补扫。

### 步 4 注入：win 机制换腿优先

本波至少 2 槽按 win 机制（T-KB-01 慢×快跨周期结构（不加权） / T-KB-05 长窗强 2Y / T-KB-07 四向价值）换白名单字段腿；禁用 PROD 饱和族字段。priors 走 `campaign.py assemble-priors`（DB KB 组装）。

### 步 9 注入：判死回写闭环

每波 FAIL 后必须 registry add-dead-end + 可精确定义的族加 methodology_rules dead_end 规则（L3 拦截），不得只写 findings 了事；win 过闸即回写 region_kb win_recipes（时机前置）。

## priors

wins:
- T-KB-01 慢×快跨周期结构：**旧配方**是 `rank(add(multiply(w_s, rank(慢)), multiply(w_f, rank(快))))` 权重 0.4 / 0.6 起步（EUR Wj71Q12o ACTIVE 先例）——**该加权相加写法已被闸 5 禁止（路线 A，2026-09-13 起）**，不得照抄；可迁移的只有「必须跨周期 / 跨数据源」这条铁律，落地形态限条件 / 分组 / 残差三式（`structural-interaction-forms.md`）
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
- SUBINDUSTRY + decay4 跟 win（EUR 实证）；可另探本区合法档（以 `config.REGIONS['GBR']` 为准，当前仅 TOP700）/ delay0。ILLIQUID_MINVOL1M 已从平台档位表移除，不得再探
- TOP700 / delay1 为主（region_kb settings_proven）

## 避坑清单

- 禁止把 EUR win 当 GBR win 直接引用（跨区配方必须本地验证）。
- PROD 饱和族（starmine/ibes/pattern_scores/other455×model264）不生成新变体，机制换腿除外。
- 白名单外禁止 generate / simulate；model238 只允许复合从腿。
