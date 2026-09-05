---
region: TWN
entry_verdict: probe-only
one_liner: "小宇宙类 KOR：继承严闸 + 先实测档位，半导体权重股结构注意集中度"
static:
  universe: []  # 实测，预期小宇宙档
  universe_default: null
  delay: [1]
  delay_default: 1
  neutralization_default: STATISTICAL
  notes: "半导体/电子权重极高，行业集中度天然大，中性化选择敏感"
datasets:
  red: []
  red_reason: ""
  yellow: []
  green: []
priors:
  signal_families_include: [analyst, pv]
  signal_families_exclude: [glb_emotion]
  syntax_patterns: []
  win_recipes:
    - "（借用）KOR 分析师预期变化面可作先验，本地验证后回写"
gate_overrides:
  cw_gate: FAIL
  longcount_min: 80
  longcount_verdict: FAIL
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 2
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死（类 KOR 小宇宙纪律）"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(TWN)"
  last_verified: 2026-08-25
---

# TWN — 小宇宙类 KOR 区

## 定位与实证依据

TWN 小宇宙，registry 空白。结构上半导体/电子权重极高（单一个股可占指数大比例），**行业集中度天然大**——这使中性化选择比常规市场更敏感：SUBINDUSTRY 可能过度集中到单一行业，STATISTICAL 中性化优先级更高。处理上预防性继承 KOR 小宇宙严闸。

## 流程变体（相对九步骨架）

### 步 1 注入：档位实测

`get_platform_setting_options(TWN)` 实测合法档，禁止外推 KOR TOP600。

### 步 5 注入：继承 KOR 严闸

- 闸 7 longCount<80 → **FAIL**；
- 步 7 评审 CW>0.5 → **FAIL**。

### 步 2 注入：中性化对照默认开启

受行业集中度影响，每个新信号族首波设置做 **STATISTICAL vs SUBINDUSTRY 对照**（各占半槽），确定 dominant 后回写 static 层 `neutralization_default`。

### 步 4 注入：KOR 有效面作先验

KOR 分析师预期变化面作为首波先验之一；GLB emotion 铁律排除。TWN 与 KOR 产业链联动（半导体），KOR win 配方的可移植性值得验证，但同 GBR 规则：本地验证后才回写 win 层。

## 避坑清单

- 中性化不对照就定默认 = 在白噪声上建楼。
- 权重股相关字段（台积电类大单）生成的信号天然高 CW，预审时预期管理：CW FAIL 率高不代表数据集无信号。
- 小宇宙配额纪律同 KOR：8 探针快判死。
