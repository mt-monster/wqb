---
region: EUR
entry_verdict: full-coverage
one_liner: "⛔ 2026-10-20 起废止探针式派发，数据集必须做尽（字段全量覆盖 / 模板族 ≥3 / 边界算子档穷举）；2026-10-02 的『结构性穷尽』只在探针式派发口径下成立，重开前必须重跑全量覆盖闸。已验证机制两条：① analyst7 四件套修订 surprise（14 颗 RA 全过 / 6 个 metric 族，TOP2500 + FAST + decay 40–80，最大互不相关团 7）；② 慢 MODEL 残差 × 快 PV（加权写法已被闸 5 禁止，只许条件 / 分组 / 残差三式，SUBINDUSTRY + decay4）"
static:
  universe: [TOP2500, TOPCS1600, TOP1200, TOP800, TOP400]
  universe_default: TOP2500
  delay: [1, 0]
  delay_default: 1
  neutralization_default: SUBINDUSTRY
  notes: "SUBINDUSTRY + decay4 为慢 MODEL × 快 PV 的 win 实证设置；档位以 src/wqb/config.py::REGIONS['EUR'] 为准（2026-09-22 实测：ILLIQUID_MINVOL1M 已不可用、TOP1600 不在档位表；IS 强度集中在 TOP2500，窄档易塔陷）。analyst7 修订族是例外配方：TOP2500 / FAST / decay 40–80 / nanHandling ON / maxTrade ON，见 wq-brain-ra-eur/references/_atom-revision-playbook.md"
datasets:
  red: []
  red_reason: ""
  yellow: []
  green: [model 系（慢残差腿）, pv 系（快腿）, analyst 系]
priors:
  signal_families_include: [slow_model_residual, fast_pv, analyst]
  signal_families_exclude: []
  syntax_patterns: []
  win_recipes:
    - "（机制）慢 MODEL 残差 × 快 PV 的跨周期 / 跨数据源结构；neutralization=SUBINDUSTRY；decay=4。历史落地写法是 0.40/0.60 加权相加，2026-09-13 起被路线 A 与闸 5 禁止——只许以条件 / 分组 / 残差入场，不记录混合比例"
    - "（机制）analyst7 四件套修订 surprise：group_neutralize(signed_power(group_zscore(divide(subtract(metric_mean, metric_mean_4wks_ago), metric_std), subindustry), p), market)。设置 TOP2500 / FAST / decay 40（幅度）或 80（广度、门控、gps）/ nanHandling ON / maxTrade ON，与区域缺省不同。14 颗 RA 全过 / 6 个 metric 族（dps/ebt/ebi/gps/pre/cps）；同族 p 变体互相关 0.97–0.99 ⇒ 每族 1 席，最大互不相关团 7。2Y 修复：trade_when(abs(ts_zscore(单字段水平值或原信号, 66)) > 1.0, CORE, 0)。完整配方见 wq-brain-ra-eur/references/_atom-revision-playbook.md"
gate_overrides:
  cw_gate: WARN
loop_policy:
  fast_kill: "缺省（决策表 D15：新数据集 8 探针无 |S|≥0.5 即判死）仅适用于单字段级——数据集级判死必须先通过三道覆盖闸，任何一闸未过都不允许判死该数据集"
  stop_conditions: ["白名单被 dead_end 全覆盖", "EUR/D1 结构性穷尽（2026-10-02 历史结论，2026-10-20 起冻结）——升 active 须出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源，或全量覆盖闸三闸均过但候选 |S| 全 <0.5"]
empirical_anchor:
  dead_ends_ref: "get_dead_ends(EUR)"
  last_verified: 2026-10-20
---

# EUR — 全量覆盖区（2026-10-20 起 full-coverage）

## ★ 2026-10-20 现状：`full-coverage`（废止探针式派发）

- **口径**：锁定数据集后必须枚举**全部字段语义维度 × ≥3 个模板族 × 边界算子全部合法档**才算测完，不允许「跑 10 条就换集」。数据集级判死必须先过三道覆盖闸（字段覆盖 100% / 模板族 ≥3 / 边界算子档穷举），任一未过 = 未做尽，不得 `seal_dead_end`。判定入口 `tools/full_coverage_gate.py --gate-mode enforce`，操作细则见 `wq-brain-ra-eur`「全量覆盖操作纪律」。
- **2026-10-02 的「结构性穷尽」已冻结**（见下方历史快照）：该结论只在探针式派发口径下成立（47/47 族 prod ≥ 0.70、7 个战役 exhausted），**不等于全量覆盖已做尽**；重开必须重跑三闸。
- **升 active 的条件**：出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源（决策表 D0-P「诊断前置」）；**或**三闸全过但候选 |S| 全 <0.5。

## ★ 2026-10-20 新增胜绩：analyst7 修订族（14 颗 RA 全过 / 6 个 metric 族）

与下方慢 MODEL × 快 PV 并列的**第二条独立机制**，也是本区「同数据集换 metric 族扩席」的样板：

- **骨架**：幅度版 `group_neutralize(signed_power(group_zscore(divide(subtract(<metric>_mean, <metric>_mean_4wks_ago), <metric>_std), subindustry), p), market)`；广度版分子换 `raisednum - lowerednum`、分母换 `raisednum + lowerednum`。
- **设置必须显式传**：`TOP2500 / FAST / decay 40（幅度）或 80（广度、门控、gps）/ nanHandling ON / maxTrade ON`。`wqb.profiles explain` 只回区域缺省（TOPCS1600 / SUBINDUSTRY / decay 4），照抄会跑成另一条信号。
- **席位**：14 颗全过覆盖 dps / ebt / ebi / gps / pre / cps；同族 p 变体互相关 0.97–0.99 ⇒ 每族 1 席，**最大互不相关团 = 7**（14 颗全过 ≠ 14 颗可同时提交）。
- **2Y/CV 修复**：`trade_when(abs(ts_zscore(<单字段水平值或原信号>, 66)) > 1.0, CORE, 0)`（`Grge2lN3` 2Y 2.02、Recent-3yr CV .436→.366；计数门控反向，2Y 0.51–0.66）。
- **完整配方 / 否证清单 / 提交协议**：[`_atom-revision-playbook.md`](../../../wq-brain-ra-eur/references/_atom-revision-playbook.md)；证据主档 `docs/reference/EUR/eur_analyst_field_profile_20261018.md` §52–§56。

## 历史快照：2026-10-02 结构性穷尽（probe-only 口径，已冻结）

来源：WorkBuddy 记忆 2026-10-02（用户要求转 EUR 后的调查；全部是项目内既有证据，不是新猜测）。以下结论保留作历史证据，**2026-10-20 起不再作为派发或判死依据**。

- **未点亮塔路径数学上封闭**（09-09）：`Fitness_upper = Sharpe_max × sqrt(returns_max / 0.125)`，要同时过平台的 Fitness 线与 Sharpe 线（`config.PLATFORM_CHECK_LINES`）需 returns ≥ 0.05，而 EUR 数据集 returns 天花板普遍 < 0.03；唯一 returns 达标的 ohlcv 族（0.061）撞字段级 prod 墙 0.80–0.82（四种算子几何全撞）。
- **库存 47/47 族 prod ≥ 0.70**（最低 0.7068），零竞争新轴三塔全灭，universe 换档否证（TOP2500 2.19 → TOP1200 0.33 → TOP400 0.50）；当前未提交候选 prod 全部 ≥ 0.7411，已 ACTIVE 的最低 0.5463。
- 过闸率 4.9%（259 波 / 594 回测，29 条 ≥ 1.58，137 条 dead_end，7 个 campaign 全 exhausted）；185 个数据集只测过 47 个，但大量「未测」是被 S0 硬地板排除的假机会（cov < 0.6 / usableFields < 10 / alphaCount > 1500）。
- 处女地 4 波新挖 max sharpe 0.22–0.93；10-02 仍有探针 `other460` best S 1.22 / 2Y 0.91，远低于 EUR 的 2Y 硬闸 1.6。
- ⚠ 设置口径三处不一致，动手前先定：`tracking/EUR/config/settings.json` = TOPCS1600 / SUBINDUSTRY / decay4 / trunc0.08 / maxTrade ON / nanHandling ON；WAVE_LEDGER 记 TOP2500 / COUNTRY / decay6；wave261 的 settings_json 是 TOP2500 / SUBINDUSTRY / decay4。
- **（当时的）升档条件**：出现 returns ≥ 0.05 且 prod 直方图不是密墙的新信号源（决策表 D0-P「诊断前置」）；否则只许探针。**该判据已被 2026-10-20 的 full-coverage 口径取代**，仅作历史留档；下面的「win 换腿」章节仍作机制参考。

## 定位与实证依据（2026-10-02 之前的历史画像）

EUR 已有平台级验证的**机制**：慢 MODEL 残差（低相关底座）× 快 PV（弹性），中性化 SUBINDUSTRY，decay 4（registry win 层）。历史落地写法是 `0.40 × 慢 + 0.60 × 快` 的加权相加——**该写法自 2026-09-13 起被路线 A 与闸 5 禁止，不得照抄**；现只许改写成条件 / 分组 / 残差三式（见 optimization-v1 `structural-interaction-forms.md`）。价值在机制，不在具体字段，也不在比例。策略不是找新配方，而是**按该机制换腿扩配**：换慢腿字段、换快腿字段、换数据集组合。

## 流程变体（相对九步骨架）

### 步 4 注入：win 换腿升为强制（full-coverage 下在本数据集内完成）

骨架约束"每波至少 `win_replay_slots_min` 槽按 win 机制换腿"在 EUR **升为硬约束 ≥2 槽**：

- **不许为凑换腿槽跨数据集跳集**：数据集锁定后，换腿 = 换 metric 族 / 换字段 / 换形态（analyst7 的 6 族 14 颗是样板）；跨数据集的「慢 MODEL × 快 PV」须单独立项，并同样按全量覆盖闸做尽。
- 慢腿候选：model 系数据集未用过的残差字段；
- 快腿候选：pv 系未用过的量价字段；
- 中性化 / decay 跟 win 配方，不重新扫参数（那是 Mode A 的事，不在生成阶段）；结构性组合里没有「混合比例」这个参数可调。

### 步 6 注入：设置探索默认开启

骨架列为"可另探"的两项在 EUR 默认排入探索队列（每波最多占 1 槽，不挤占 win 换腿槽）：

1. `TOPCS1600`；
2. `delay 0`。

- **配方自带设置时先按配方设置跑基线**：analyst7 修订族要求 TOP2500 / FAST / decay 40–80（与 `settings.json` 缺省不同）。拿区域缺省当基线等于换了信号，不能用来判该配方死活。

> `ILLIQUID_MINVOL1M` 已从平台档位表移除（2026-09-22 实测，且对 EUR 已被永久停提），不得再排入；`TOP1200` / `TOP800` / `TOP400` 等窄档实测易塔陷（`config.REGIONS['EUR']['_note']`），只作单点对照探针，不作探索主线。

### 步 9 注入：win 配方版本化回写

每次 win 换腿产出新 ACTIVE，回写 win 层时必须记录**换的是哪条腿 + 新字段 id**（analyst 族还要记 metric 族），形成配方族谱，避免下一波重复换同一条腿。analyst7 已占用 dps / ebt / ebi / gps / pre / cps 六族；同族 p 变体互相关 0.97–0.99，只算 1 席。

## 避坑清单

- 禁止只穷举同金字塔换字段（骨架反模式，EUR 最容易犯）。
- **不调混合比例**：加权 / 等权相加已被闸 5 禁止（路线 A，2026-09-13 起），也违背「禁止混信号调参」；换腿时每波只动一个变量（慢腿字段 / 快腿字段 / 条件分位阈值）。
- **新数据集不再走 8 探针快判死**：8 探针只适用于单字段级初筛。数据集级判死必须先过三道覆盖闸（字段 100% / 模板族 ≥3 / 边界算子档穷举）+ 全波次 |S|<0.5；任一未过 = 未做尽，不得 `seal_dead_end`。
- **设置档必须显式传**：MCP `create_multi_simulation` 只认 snake_case（`nan_handling` / `max_trade` / `instrument_type` / `unit_handling` / `test_period`），camelCase 被静默丢弃；派发后读回一个子项 `settings` 断言 `nanHandling` / `maxTrade` 为 ON，否则读数只能作方向性证据。
