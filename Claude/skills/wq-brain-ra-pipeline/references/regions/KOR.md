---
region: KOR
entry_verdict: active
one_liner: "TOP600 小宇宙：有效面=分析师预期变化，图表/新闻/AI/信用四大红灯，CW 闸升级 FAIL"
static:
  universe: [TOP600]
  universe_default: TOP600
  delay: [1]
  delay_default: 1
  neutralization_default: STATISTICAL
  notes: "小宇宙放大 CW/longCount 问题；档位禁止外推"
datasets:
  red: [chart_patterns, news_sentiment, ai_ml, credit_risk]
  red_reason: "图表形态 3 连死 / 新闻情绪 3 连死 / AI-ML 3 连死 / 信用风险双死；GLB emotion 跨区铁律同禁"
  yellow: []
  green: [analyst 系（评级/预期）, insiders, pv]
priors:
  signal_families_include: [analyst_revision, analyst_x_sh_mix, insider, pv]
  signal_families_exclude: [chart_pattern, news_emotion, ai_ml, credit_risk, glb_emotion]
  syntax_patterns: []
  win_recipes:
    - "分析师评级修正 × SH（shortinterest/holders）混合（2 颗 ACTIVE 实证）"
gate_overrides:
  cw_gate: FAIL
  longcount_min: 80
  longcount_verdict: FAIL
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死回写，不扩批（小宇宙烧不起配额）"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(KOR)"
  last_verified: 2026-08-25
---

# KOR — 小宇宙红灯区

## 定位与实证依据

KOR 是 TOP600 小宇宙，挖得最深（wave 95+），20 数据集 exhausted。死路图谱极清晰：**图表形态 3 连死、新闻情绪 3 连死、AI/ML 3 连死、信用风险双死**，外加 GLB emotion 跨区铁律。活路同样清晰：**分析师预期变化面**——评级修正 × SH 混合已产 2 颗 ACTIVE。小宇宙的结构性问题：CW（持仓集中度）与 longCount（VECTOR 字段有效长度）问题被放大，事件类数据集 CW>0.5 是通病。

## 流程变体（相对九步骨架）

### 步 2 注入：白名单极窄

- 白名单只留：绿榜（analyst/insiders/pv）+ status=untried 新集；
- 金字塔配额冲突时**优先 analyst 族上提**（实证有效面），tier_note 标 `pyramid_quota_kor`；
- 红榜数据集一律不进白名单，即使用户点名——先提示死路 rule 出处（matrix 硬规则 2）。

### 步 3 注入：typed catalog 双查

扫描字段时强制输出每字段 `longCount` 与 `type`：`longCount < 80` 的 VECTOR 字段进观察名单，步 5 闸 7 按 FAIL 处理（见下）。

### 步 5 注入：闸门加严（KOR 核心变体）

| 闸 | 全局默认 | KOR |
|---|---|---|
| 闸 7 longCount<80 | WARN | **FAIL** |
| CW>0.5（步 7 评审） | WARN | **FAIL**（事件类通病实证） |

CW 为动态指标不进静态闸，在步 7 review 时检查：CW>0.5 的 alpha 直接判死不回炉。

### 步 2/6 注入：8 探针快判死

新数据集只给 8 条探针预算：无 |S|≥0.5 即写 dead_end 回写 registry，**不扩批、不换设置重试**。小宇宙配额稀缺，慢判死 = 慢性自杀。

## 避坑清单

- 四大红灯族 + GLB emotion：生成阶段直接排除，不抱"换参数复活"幻想。
- 事件类数据集（earnings 等）：优先生成 `ts_event_*` 裸 rank 表达式，且预设 CW 必查。
- 禁止 delay0 外推（KOR 实证仅 delay1）。
