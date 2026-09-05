---
region: USA
entry_verdict: active
one_liner: "最深最饱和市场：value/quality 种子全死，靠 option/analyst 新集 + 强制正交"
static:
  universe: [TOP3000, TOP1000, TOP500]
  universe_default: TOP3000
  delay: [1, 0]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "档位实证充分，delay0 可探"
datasets:
  red: [pv1, mdl177]
  red_reason: "exhausted；seed basics 全族（value/quality 种子）死"
  yellow: []
  green: [option9, analyst 细分集, news 高级情绪集, event/earnings 集]
priors:
  signal_families_include: [option, analyst_revision, event_driven, news_advanced]
  signal_families_exclude: [classic_value, classic_quality, book_ratio, seed_basics]
  syntax_patterns: []
  win_recipes: []
gate_overrides:
  cw_gate: WARN
  longcount_min: 80
  prod_corr_early_warn: 0.6
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "新数据集 8 探针无 |S|≥0.5 即判死"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(USA)"
  last_verified: 2026-08-25
---

# USA — 饱和市场正交战

## 定位与实证依据

USA 是挖得最深的市场：`search_alphas_by_sharpe(USA, 1.58)` 命中大量已达标 alpha，其中 book/value 系单族 145 颗 ACTIVE 同族。后果：**任何经典 value/quality/momentum 变体的 prod_corr 必然贴死 0.7 红线**。pv1 / mdl177 已 exhausted，seed basics 全族判死。有效方向只剩：option9（进行中）、analyst 细分、event-driven、news 高级情绪。

## 流程变体（相对九步骨架）

### 步 1 注入：PROD 饱和强制拦截

1. 查 `get_dead_ends(USA)`，把 PROD_CORRELATION 类死路的信号族并入 `signal_families_exclude`；
2. 查 `search_alphas_by_sharpe(USA, min_sharpe=1.58)`：某族已达标 alpha ≥10 且风格同质 → 标 `prod_saturation: likely`，该族硬排除出本波 priors；
3. 配置包输出时必须带 `prod_risk` / `prod_saturation` 标注（与 campaign-matrix §输出契约一致）。

### 步 4 注入：priors 硬排除饱和族

GEM `--priors-file` 必须包含 `signal_families_exclude`；生成结果若仍命中饱和族，build-wave 阶段直接剔除，不进七槽。

### 步 6 注入：prod-first 加严

每槽先 1–2 条骨架查 `prod_corr`，**预警线 0.6**（全局默认 0.7）：≥0.6 即停扩换腿，不再等 0.7。USA 的 0.6→0.7 区间几乎必然继续恶化。

### 步 7 注入：Mode B 强制正交

诊断改进阶段，`wq-brain-alpha-optimization-v1` Mode B 必须启用**正交方向推荐**（联动 P2-1 增强）：同族变体 >3 次仍 prod_corr ≥0.6 → 判该族死刑，写 dead_end，换正交概念，禁止同族继续磨参数。

## 避坑清单

- 禁止生成 book/PE/ROE 等经典基本面单因子及其线性变体（必死）。
- 禁止"先摊满 8 条再查 prod"（全局反模式，USA 代价翻倍）。
- delay0 探针单独成批，不与 delay1 混批，避免设置噪声误判信号族。
