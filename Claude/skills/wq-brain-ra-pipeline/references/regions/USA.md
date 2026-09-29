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
loop_policy:
  max_probes_per_wave: 1
  fast_kill: "缺省（决策表 D15：新数据集 8 探针无 |S|≥0.5 即判死）；本区无额外规则"
  stop_conditions: ["白名单被 dead_end 全覆盖"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(USA)"
  last_verified: 2026-09-29
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

GEM 的 priors（DB 快照 `priors_snapshot_<region>`；缺失时才显式传 `--priors-file`）必须包含 `signal_families_exclude`；生成结果若仍命中饱和族，build-wave 阶段直接剔除，不进本波。

### 步 6 注入：prod-first（**并入 D0-P，不另设预警线**）

USA 的 prod 墙很硬：0.6 → 0.7 区间几乎必然继续恶化（同族 145 颗 ACTIVE 同质）。**处置只按决策表 D0-P**：首探 < 0.60 才扩变体；**0.60–0.70 不扩变体、当天进步 8**（提交前 `check_correlation(refresh=True)` 终验）；≥ 0.75 或踩线尝试失败 → dead_end。
（旧版这里写「预警线 0.6：≥ 0.6 即**停扩换腿**」——那与 D0-P 的 0.60–0.70 行直接相反，会让已成型的候选被放着不提交，正是 IND pv103 事故 0.6997 → 1.0000 的反面教训；`prod_corr_early_warn` 键也已从 front-matter 删除。
若要表达「USA 更严」，含义是**扩批之前**就按族查 prod-first，而不是改阈值。）

### 步 7 注入：Mode B 强制正交

诊断改进阶段，`wq-brain-alpha-optimization-v1` Mode B 必须启用**正交方向推荐**（联动 P2-1 增强）：同族出现 prod ≥ 0.6 → 按 D0-P 处置（0.60–0.70 当天进步 8；≥ 0.75 判 dead_end 并换正交概念），**禁止同族继续磨参数**。

### 步 7 注入：修复用 universe 约定（自 `brain-alpha-repair` 迁入，skills 审查 RE-09）

USA REGULAR 的修复保持 `TOP3000` 默认 universe（`config.REGIONS['USA']['default_universe']`）。改用其它 USA universe 时，在本波 `wave_result.key_findings` 里写明：① TOP3000 下失败的原因；② 换的这个 universe 要回答的诊断问题。**不新造台账键。**

## 避坑清单

- 禁止生成 book/PE/ROE 等经典基本面单因子及其线性变体（必死）。
- 禁止"先摊满 8 条再查 prod"（全局反模式，USA 代价翻倍）。
- delay0 探针单独成批，不与 delay1 混批，避免设置噪声误判信号族。
