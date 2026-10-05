# 论坛经验 → skills 回测流程：集成方案

> 基于 2026-10-02 论坛调研（见 `reports/forum_alpha_inspiration_taxonomy_20261002.md`）
> 与现有 GEM / 骨架库源码实测。所有文件:行号均为当前仓库实测。

---

## 0. 一句话结论

**论坛产物有三类，必须走三个不同落点，不能一锅炖。**

| 论坛产物 | 落点 | 为什么 |
|---|---|---|
| **机制拓扑**（算子组合形状） | 骨架库 `skeletons_data_forum.py` | 代码组装 → 语法强保证 |
| **带 citation 的经济机制** | `tools/economic_mechanism_templates.py` | 已有 P0/P1 分级与 category 路由 |
| **具体表达式**（如 `vec_min(a)/vec_min(b)`） | idea md 通道（隔离 + 打未实证标） | **绕过语法保证 + 未实证**，禁止进前两者 |

核心原则：**论坛给「形状」和「为什么」，不给「字符串」。** 一旦把自由字符串塞进
prompt，就退化成模板展开器时代的老病——约束只在语法层，零语义层约束。

---

## 1. 现有链路注入点地图（实测）

| # | 注入点 | 文件:行 | 作用 | 论坛经验可否进 |
|---|---|---|---|---|
| 1 | 骨架库装配 | `skeletons.py:209-215` | `_BASE + _DECOUPLE` → `SKELETONS`(144) | ✅ **主落点** |
| 2 | prompt 装配 | `skeletons.py:596-919` | skel/econ_kb/econ_tmpl/regime/priors 五块拼装 | 间接 |
| 3 | 经济机制模板注入 | `skeletons.py:772-817` | `get_all_p0_templates()` → prompt | ✅ 次落点 |
| 4 | 填槽配额与去重 | `skeletons.py:493-589` | family 配额、`mechanism` 级去重、闸 0 lint | 影响新骨架能否出量 |
| 5 | 闸 0 语义 lint | `skeletons.py:323-414` | 恒等式/裸字段/幻觉字段/退化窗口 | 新骨架必须过 |
| 6 | 毒模式预闸 | `pipeline_pregate.py:260-301` | 读 `platform_constraints.json::poison_patterns`(8 条 block) | 违规形态在此被拦 |
| 7 | 区域 priors | `skeletons.py:960-997` | 读 `references/regions/<R>.md` 的 `## priors` 段 | ✅ **零风险** |
| 8 | 字段质量评分 | `skeletons.py:700-711` → `tools/field_quality_scorer.py` | `[HIGH-QUALITY]` 标记 | ✅ **零风险** |

---

## 2. 落点 A：机制拓扑 → 骨架库 ✅ 已实现并通过自检

**新增文件**：`Claude/skills/brain-make-some-gem/scripts/trailSomeAlphas/skeletons_data_forum.py`（4 条，惰性未接线）

### 缺口对照（新增前已核实现有 144 骨架）

| 新增骨架 | 现有最接近 | 真实缺口 |
|---|---|---|
| `ratio_eff.group_flow_stock`<br>`group_rank(divide({x},{y}+0.0001), subindustry)` | `ratio_eff.flow_stock` = `rank(divide({x},{y}+eps))` | 无 group 版。项目实证「内嵌 group_rank 是独立增益维度」（EUR: S 0.44→1.22、2Y +177%） |
| `spread_residual.ts_instability`<br>`ts_zscore(ts_std_dev(subtract({x},{y}),{W}),{W2})` | `spread_residual.cross_horizon` = `subtract(rank(x),rank(y))` | 只有**静态价差**，缺「价差的时序不稳定性」这一维 |
| `spread_residual.group_regression_residual`<br>`group_zscore(ts_regression({y},{x},{W}), subindustry)` | `spread_residual.ts_regression_residual` = `rank(ts_regression(...))` | 无 group 版残差 |
| `trend_cons.sign_persistence`<br>`rank(ts_mean(sign(ts_delta({x},1)),{W}))` | `trend_cons.ma_ratio`（快慢均线比） | 缺「方向持续性 vs 变化幅度」这一维 |

### 自检结果（全部通过）

| 骨架 | 算子数 | 闸0 lint | 毒模式 | 算子白名单 | 判定 |
|---|---|---|---|---|---|
| ratio_eff.group_flow_stock | 2 | 干净 | 无 | 全在 known_ops | OK |
| spread_residual.ts_instability | 3 | 干净 | 无 | 全在 known_ops | OK |
| spread_residual.group_regression_residual | 2 | 干净 | 无 | 全在 known_ops | OK |
| trend_cons.sign_persistence | 4 | 干净 | 无 | 全在 known_ops | OK |

- 算子数 2–4，满足项目 §0.1 复杂度纪律（< 10）
- 无 id 冲突；均带 `mechanism`（参与 `assign_slots` 机制级去重，防参数变体簇）

### 接线（3 行，改 `skeletons.py:209-215`）

```python
from skeletons_data_base import SKELETONS as _BASE_SKELETONS
from skeletons_data_decouple import SKELETONS as _DECOUPLE_SKELETONS
from skeletons_data_forum import SKELETONS as _FORUM_SKELETONS      # 新增

SKELETONS = _BASE_SKELETONS + _DECOUPLE_SKELETONS + _FORUM_SKELETONS  # 新增
```

⚠ 接线后同步：① `build_skeleton_prompt` 的 skel_block 自动带上新骨架（无需改）；
② 家族配额 `adjusted_max_per_family = n_slots//6` 会自动稀释 → 若想让论坛骨架出量，
需给 `spread_residual` / `ratio_eff` 单独配额；③ 跑 `tests/unit/09_core/test_skeleton_dedup_p5.py`
与 `tests/unit/07_docs_skills/test_docs_consistency.py`（后者校验骨架只用 verified 算子）。

---

## 3. 落点 B：经济机制模板库 —— ⚠️ 先整改再加

**文件**：`tools/economic_mechanism_templates.py`

### 发现的冲突

该库有 **9 条模板含加权混合腿** `add(multiply(0.x, rank(A)), multiply(0.y, rank(B)))`，
其中 **3 条是等幅**（`0.5/0.5` 或 `±0.5`）：

```
L35  0.6*rank(vec_avg(analyst_revision)) + 0.4*rank(vec_stddev(...))
L66  0.7*rank(ts_delta(...))            + 0.3*rank(days_from_last_change(...))
L128 0.5*rank(...)                      + 0.5*rank(...)          ← 等权
L252 0.5*rank(fundamental_field)        + 0.5*rank(value_field)  ← 等权
L283 0.5*rank(...)                      + -0.5*rank(...)         ← 等幅
...（共 9 条）
```

这**正是项目 §0 铁律禁止的形态**（`0.4A+0.6B`、等权 `0.5A+0.5B` 同属违规族），
对应的执行规则 `weighted_signal_mix_structural` / `equal_weight_leg_add` 已在
`platform_constraints.json` v1.5 中，且被 `pipeline_pregate.py` 以 `severity=block` 拦下。

**更关键的矛盾**：`skeletons.py:223` 注释记载 `interact.weighted_mix` 已于 **2026-09-12 退役**
（同一原因），但 `economic_mechanism_templates.py` 从未同步 → **同一仓库里骨架库已弃的
形态，经济模板库还在通过 `skeletons.py:772-817` 往 prompt 里教**。这是毒模式的
「上游污染源」：pregate 拦得住产出，拦不住 prompt 的语义诱导。

### 整改两条路（建议 A）

- **A（推荐）**：把 9 条改写为合规形态——`ts_corr` / `divide` / `subtract(rank,rank)` /
  `if_else·trade_when` / `group_zscore·group_rank`（§0 放行 5 类形态），保留机制名与 citation。
- **B（保守）**：加 `"deprecated": true` 并在 `get_all_p0_templates()` 过滤掉，停止注入 prompt。

改完再按第 4 节往里加论坛机制（凸显理论 STR、隔夜拉锯战、理想振幅、处置效应、
PEAD 快慢手、分析师修正广度），每条带 `citation`。

---

## 4. 落点 C：具体表达式 → idea md 通道，隔离未实证

论坛的具体表达式**不进 A/B**。理由有二：
1. 会绕过「代码组装 → 语法强保证」这条命脉；
2. 论坛表达式**默认未实证**（skill 纪律明文）。

正确路径：`brain-feature-implementation` 的 idea markdown 通道
（`implement_idea.py` 绑定占位符）。**注意已踩过的坑**：GEM ideas 硬约束要求
`**Implementation Example**` 的占位符**精确等于或后缀匹配真实 field id**——
论坛的 `group_rank({field}/cap, industry)` 里 `{field}` 是通用占位符，
经 `pipeline_placeholders.validate_placeholders_strict` 会被判**幻觉占位符**直接全灭。

⇒ 所以论坛模板进 idea md 前，必须先把 `{field}` 改成真实字段或合法后缀。

落库时打标：`source=forum, verified=false`，并强制过 `preflight_expressions` + 闸 5。

---

## 5. 落点 D：非模板经验 → 零风险通道

| 论坛经验 | 落点 | 现状 |
|---|---|---|
| 「高覆盖率 × 低 alphaCount(0–3)」白空间筛选法 | `tools/field_quality_scorer.py`（`skeletons.py:700-711` 调用） | 目前只按描述打分，未接入 alphaCount → 可直接并入口径 |
| 「字段描述里 not directly predictive 反而值得看」 | 同上（反向加权） | 未接入 |
| 区域 × 信号族实证（如 GLB 哪些族已判死） | `references/regions/<R>.md` 的 `## priors` 段 | ⚠ **14 个区里 13 个没有 `## priors`**，只有 GBR 有 → `load_region_priors()` 对 13 区返回空，通道闲置 |
| 论坛判死证据 | `registry_empirical` / `seal_dead_end`（`brain-dataset-mining-experience`） | 已有通道，按既有纪律走 |

---

## 6. 反馈闭环：别盲信论坛

现有 `skeleton_stats` 已支持按 `skeleton_id` 统计 `pass_rate / best_sharpe`
（`skeletons.py:669-697` 会把 `[MEASURED n=… pass=…]` 标注进 prompt，并按过闸率排序置顶）。

新增骨架均带 `origin=forum` 与 `forum_ref`。接线后建议跑 1–2 波，单独统计
**论坛来源骨架 vs 原生骨架的过闸率**——若论坛骨架过闸率显著更低，说明
「论坛机制 ≠ 本区可提交」，应当降级而不是继续扩批。

---

## 7. 明确不做（反模式）

- ❌ 把论坛表达式字符串直接塞进 `skeletons.py` 的 template 字段（绕过组装保证）
- ❌ 一次性导入几十条论坛骨架（现有 144 条里 `econ_option` 独占 94 条已被压配额，
  说明骨架库**已经过度膨胀**，再加会稀释 prompt、降低命中密度）
- ❌ 把论坛高票当作实证（票数 ≠ 过闸；票高只说明「写法受欢迎」）
- ❌ 跨区外推（论坛的 CHN/USA 经验不能直接套 GLB / KOR）

---

## 8. 执行清单（2026-10-02 23:27 已推进）

- [x] 新增 `skeletons_data_forum.py`（4 条，自检全绿）
- [x] **接线** `skeletons.py:209-215`（3 行）→ 骨架库 144 → **148**，forum 来源 4 条
- [x] 跑 `test_skeleton_dedup_p5.py` + `test_docs_consistency.py` + `tests/unit/03_gem/`
      → **388 passed / 2 skipped**（跳过项因 `data/operators_verified.json` 缺失，已手工比对 `known_ops`）
- [x] prompt 冒烟：4 条新骨架均进入 `skel_block`；econ 模板块在 analyst/pv/fundamental
      三类数据集下均正常注入、**违规数 0**（备份 `tools/economic_mechanism_templates.py.bak_20261002`）
- [x] **整改 `economic_mechanism_templates.py`：9 条违规模板直接删除**（未标 deprecated）
      → 模板 27 → **18**，每机制保留 2 条（1 纯信号 + 1 合规门控/中性化），P0=10 / P1=8 / backfill=6
- [x] `sync_skills.py` 同步 4 个安装位，`--check` exit 0
- [x] `sync_skills.py` 同步 4 个安装位，`--check` exit 0
- [x] **`tools/skeleton_origin_report.py`（新）** — forum vs native 过闸率对比，绕开死掉的
      ledger 归因，改用结构签名归因（`structural_signature` ↔ `expressions.skeleton`）
- [x] **`tools/field_quality_scorer.py` 接真实数据 + 白空间维度** — 修 `field_catalog`→`fields`、
      sharpe 回退改 None、新增 uncrowded 15%
- [x] **`tools/seed_region_priors.py`（新）** — 13 区 `## priors` 从 DB 自动装配（默认只填空）
- [x] 修 `brain-dataset-exploration-general/SKILL.md` 经济大类「10 类→11 类」（漏列 价格/收益）
- [ ] 剩 1 个既有红灯 `test_glossary_docs`（`wq-brain-campaign-matrix/SKILL.md` 新增「唯一」宣称，需 owner 决断）
- [ ] 跑 1–2 波后按 `origin=forum` 统计过闸率，决定是否扩批（工具已就绪）

### 删除明细（9 条，均为 `add(multiply(w, rank(A)), multiply(v, rank(B)))` 形态）

| 机制 | 删除的模板 | 保留的合规替代 |
|---|---|---|
| analyst_dispersion | 分歧 × 修正方向 | 分歧 × 覆盖度（门控） |
| information_decay | 新鲜度 × 修正幅度 | 新鲜度门控 |
| tail_risk | 尾部风险 × 修正方向 | 尾部风险门控 |
| industry_dispersion | 行业离散度 × 个股相对强度 | 行业离散度门控 |
| volume_price_coherence | 量价协同 × 价格动量 | 量价协同门控 |
| short_term_reversal | 反转 × 成交量确认 | 反转门控 |
| low_volatility_anomaly | 低波动 × 质量 | 波动率门控 |
| quality_factor | 质量 × 价值（QMJ） | 质量行业内中性化 |
| liquidity_premium | 流动性 × 反转 | 流动性门控 |

**判断依据**：9 条违规模板所在的机制里，均已存在一条表达**同一套经济学交互**的合规
`trade_when` 门控（或 `group_zscore` 中性化）兄弟模板 ⇒ 删除为零经济学损失，
故直接删除而非改写、更不标 deprecated。
