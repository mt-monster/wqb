---
region: HKG
entry_verdict: probe-only
one_liner: "半空白小宇宙：处理类 KOR（CW/longCount 严闸），注意与 CHN 联动信号"
static:
  universe: [TOP800, TOP500]  # 2026-09-29 从 config.REGIONS 回填（2026-08-05 平台实测同，见 ppa-mining §9.1）
  universe_default: TOP800
  delay: [1]
  delay_default: 1
  neutralization_default: STATISTICAL
  notes: "小宇宙预案：继承 KOR 严闸；与 A 股相关性高"
datasets:
  red: []
  green: []
  yellow: []
priors:
  signal_families_include: [analyst, pv]
  signal_families_exclude: [glb_emotion]
  syntax_patterns: []
  win_recipes:
    - "（借用）KOR 分析师预期变化面可作先验，本地验证后回写"
gate_overrides:
  cw_gate: FAIL
  longcount_verdict: FAIL
loop_policy:
  max_probes_per_wave: 2
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死（类 KOR 小宇宙纪律）"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(HKG)"
  last_verified: 2026-08-25
---

# HKG — 小宇宙类 KOR 区

## 定位与实证依据

HKG 半空白，宇宙规模预期与 KOR 同级（小宇宙）。小宇宙的结构性问题（CW/longCount 放大、事件类 CW 通病）在 KOR 已被实证，HKG **预防性继承** KOR 严闸，不等踩坑再补。与 A 股（CHN）联动强：信号生成时需注意含 A 股敞口的字段可能有跨区相关性。

## 流程变体（相对九步骨架）

### 步 1 注入：档位实测

`get_platform_setting_options(HKG)` 复核合法档（当前 `config.REGIONS` = TOP800 / TOP500，默认 TOP800），禁止外推 KOR TOP600。
front-matter 的 `universe` 已于 2026-09-29 从 `config.REGIONS` 回填（此前是 `[]`，与决策表 D5 的 TOP500 / 800 不一致）；以后以 `config.REGIONS` 为准，见 [`../region-profile-contract.md`](../region-profile-contract.md) §4。

### 步 5 注入：继承 KOR 严闸

- 闸 7 longCount<80 → **FAIL**（同 KOR）；
- 步 7 评审 CW>0.5 → **FAIL**（同 KOR）。

### 步 4 注入：KOR 有效面作先验

KOR 实证有效的分析师预期变化面（评级修正 × SH 混合）作为首波先验之一，本地验证后回写；GLB emotion 跨区铁律直接排除。

### 步 7 注入：CHN 联动检查

近闸候选提交前加查：与同账户 CHN 区 ACTIVE 的相关性（若 CHN 区已有 ACTIVE）。显著相关（>0.5）时向用户说明，由用户决定是否接受跨区暴露。

## 避坑清单

- 小宇宙配额纪律同 KOR：8 探针快判死，不扩批。
- 不因"香港市场国际化"假设外推 USA/EUR 配方——无本地实证前一律探针待遇。

## priors
- 拥挤数据集 TOP3（避免重复挖）：pv1(alphaCount=3572, cov=1); pv30(alphaCount=1608, cov=0.93); risk70(alphaCount=732, cov=0.93)
- 白空间候选（未测 + 覆盖≥60% + 低 alphaCount）：analyst_earnings_ibes(cov=1, alphaCount=0); news_sentiment_transfer(cov=1, alphaCount=0); pattern_scores(cov=1, alphaCount=0); pv149(cov=1, alphaCount=0); shortinterest5(cov=1, alphaCount=0)
- 已判死（勿重试）：HKG-FUND-HOLDINGS-PANEL-WEAK-SIGNAL, HKG-MDL238-SCREEN-OWNER-CEILING-139, HKG-MMP-NLP-SENTIMENT-NO-SIGNAL
- 实证笔记：HKG-DUALGATE-EXP-20260909: 流动性门×拥挤度门嵌套，主闸 PENDING——明日提交探测候选 | HKG-QMWLONOE-MODEC2-ZFIX-20260909: 双制度确认（sign+zfix 均值化），sharpe 全场最高 | HKG-QMWLONOE-MODEC-ROUND1-20260909: 全指标反号→修正方向后 +1.72/+1.15/+1.50
