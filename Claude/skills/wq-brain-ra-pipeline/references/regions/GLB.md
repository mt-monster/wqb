---
region: GLB
entry_verdict: active
one_liner: "跨区铁律发源地：emotion 死路 + anl15 精确表达式封禁，铁律必读升强制"
static:
  universe: [TOP3000]
  universe_default: TOP3000
  delay: [1]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "大宇宙，跨区组合 delay 受跨区影响需实测"
datasets:
  red: [emotion 系, anl15]
  red_reason: "emotion 跨区死路铁律；anl15 精确表达式平台封禁"
  yellow: []
  green: [pv 系, fundamental 系, analyst 系]
priors:
  signal_families_include: [pv, fundamental, analyst]
  signal_families_exclude: [glb_emotion, anl15_exact]
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.7
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(GLB)"
  last_verified: 2026-08-25
---

# GLB — 跨区铁律区

## 定位与实证依据

GLB 是跨区铁律的主要发源地：emotion 系死路（GLB 判死后推广为跨区铁律，KOR/HKG 等区间接受益）、anl15 精确表达式平台封禁。大宇宙（TOP3000+），跨区组合 delay 设置受各市场开盘时间影响，需实测。GLB 的死路记录有**跨区外溢价值**——本区判死的族要主动评估是否升为跨区铁律。

## 流程变体（相对九步骨架）

### 步 1 注入：铁律必读升强制

骨架中 `get_cross_region_lessons` 为常规查询，GLB 升为**强制逐条核对**：每条铁律在配置包中标注"本波是否触碰"，触碰项必须给出规避方案。

### 步 4 注入：封禁表达式静态拦截

anl15 封禁的**精确表达式文本**进生成黑名单：GEM 产出若含封禁文本（sha1 比对），build-wave 阶段剔除。emotion 系字段全排除。

### 步 9 注入：死路外溢评估（GLB 核心变体）

每波判死回写时加评一条：该死路是否跨区普适？是 → 同步写 `registry_empirical`（`mcp__wqb-db__upsert_registry_empirical(region="GLOBAL", layer="cross_region", entry_id=<lesson_id>, family=<family>, payload={"finding":..., "rule":...})`），其他区 S-PRE 自动读到。

### 步 6 注入：delay 实测

跨区组合 delay0/delay1 表现差异大，新信号族首波 delay1，次波可探 delay0 对照，设置差异单独成批。

## 避坑清单

- anl15 精确表达式：不是"别提交"，是**生成即剔除**（平台级封禁，回测都浪费）。
- emotion 系：包括 sentiment/emotion/mood 命名的所有变体，铁律无例外。
- GLB 大宇宙不等于随便烧：TOP3000 回测成本高，prod-first 纪律照执行。

## stage1 封禁字段实证（orchestrator 4.2 迁移）

- **analyst15 零算子验证**：|sharpe| max=0.520、fitness max=0.300、turnover 0.011-0.125（全 <0.3 必触 LOW_TURNOVER）——anl15 系裸字段在 GLB 无预测力。
- **8 个 `anl15_*` 字段永久触发 "took too much resource"**（封禁清单 `glb_alpha_machine/cache/blocked_fields.txt`，8 条精确表达式，**不能按前缀通配**）。
- **idx80-87 同前缀但 COMPLETE**——同前缀字段并非都封禁，必须按精确表达式比对，勿误伤。
- **真增强路径**：stage2 group 残差 / stage3 `trade_when(delta)`，不是对 anl15 裸字段做算子包装。

## prod-corr 规避要点（orchestrator prod-corr-avoidance 迁移）

- **techindi_model `predicted_first_quantile_ten_day_return_*` 系已判穷尽**：热门字段（users≥50）prod_corr 必超 0.7（qMNZX1o1 实测 0.7686）；中间地带（users 18-40）fit/AMER/2Y 结构性缺口不可修；冷门（users 0-9）信号弱（0.9-1.65）。
- **结论**：GLB pred 系信号族在 prod_corr<0.7 约束下**无候选来源**（信号强度/可打磨性/prod_corr 三者不可兼得，平台结构性 trade-off，同 USA other566/risk65）。
- **算力分配**：该族标记"已穷尽-规避"，不再投入任何 decay/窗口/分组变体；转向新 PPA 主题窗口、新灌入冷门数据集、或其他区域 PPA 主题匹配。
- 完整画像见 [../prod-corr-avoidance.md](../prod-corr-avoidance.md)。
