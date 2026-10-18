# DEU × pv（组合分支）

> 回到 [DEU 区域流程](../SKILL.md) · [DEU profile（证据与历史）](../../wq-brain-ra-pipeline/references/regions/DEU.md) · 实时生效画像：`$WQ_PY -m wqb.profiles explain --region DEU --category pv`

<!-- profiles:cell-panel:start -->
**状态**：probe（跟区域入场 probe-only）　**分组**：PV　**类别卡**：pv

**涉及数据集**：intraday_pv_feats、pattern_scores、pv30

### 回测设置（进仿真的值）

| 设置 | 值 | 来源 |
|---|---|---|
| instrumentType | EQUITY | 区域 settings.json |
| region | DEU | 区域 settings.json |
| universe | TOP500 | 区域 settings.json |
| delay | 1 | 区域 settings.json |
| neutralization | SUBINDUSTRY | 区域 settings.json |
| decay | 4 | 区域 settings.json |
| truncation | 0.08 | 区域 settings.json |
| pasteurization | ON | 区域 settings.json |
| unitHandling | VERIFY | 区域 settings.json |
| nanHandling | OFF | 区域 settings.json |
| maxTrade | OFF | 区域 settings.json |
| language | FASTEXPR | 区域 settings.json |
| visualization | false | 区域 settings.json |
| startDate | 2013-01-01 | 区域 settings.json |
| endDate | 2023-12-31 | 区域 settings.json |

### 阈值

- Mode B 主闸 sharpe / fitness：1.25 / 0.8（thresholds_override:DEU；下限锁生效，实时值看 explain）
- 其余阈值跟区域 thresholds.json（本组合无覆盖）

### 证据（2026-10-04 只读汇总）

| 回测 | RA 全过 | prod 已测 | 其中低于上限 | 判死 | 胜绩 |
|---|---|---|---|---|---|
| 24 | 0 | 0 | 0 | 3 | 0 |

主要数据集（回测数）：pattern_scores（15）、intraday_pv_feats（9）

### S1 字段理解

- 各区可用性差异大：先查本区有没有 pv1（JPN TOP1600 没有，close / adv20 / returns 不可用）
- intraday_pv_feats 目录字段 ≠ 平台可用字段：先单字段探针再成批
- 窗口（类别卡，均在白名单内）：daily 1/5/22；monthly 66

### S2 生成

- **类别通用原语**（类别卡，跨区）：
  - continuation vs reversal: short-horizon pattern vs longer mean
  - intraday vs overnight: session-specific pressure
  - volume-conditioned return: price move that happened on unusual volume
  - fast+slow interaction must be ONE coherent signal (ratio / ts_corr / conditional), never a weighted sum of two legs
  - volatility regime: high-vol vs low-vol period signal divergence
  - liquidity shock: volume spike vs historical average (ts_zscore of volume)
  - price efficiency: bid-ask spread or price impact proxy
- **跨区结论**（IND/GLB/ASI；negative）：日内价量相关反转 / 尾盘反转 IS 很强，但裸用 prod 0.79–0.99；只有加门控才可能破墙（见全局杠杆 subset_gate）（证据：IND intraday_pv_feats prod 0.79–0.92、pv103 外部孪生 1.0（IND profile）；GLB / ASI 门控模板（2026-09-21 实证）） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（JPN/IND/GBR/USA；negative）：日内微观结构的非反转机制普遍弱（max ／S／ 约 1.0，或撞 fitness 墙）（证据：JPN w8 16 条 max／S／ 1.02；USA-IPV-CORR-PRECLOSE-FITNESS-WALL-20260921；GBR-INTRADAY-MICRO-WEAK；IND 未点亮塔实证） <!-- lint:const-ok 证据原文 -->
- **跨区结论**（KOR/GBR/DEU/AMR；negative）：图表形态族（pattern_scores / continuation_score / chart_cnn）（证据：KOR 三连死（chart_cnn 1.51 → continuation 0.34 → pattern_scores 0.49）；GBR-SIMPLE-STRUCTURE-DEAD；DEU-PATTERN_SCORES-PROBE-DEAD-20261002；AMR 红榜） <!-- lint:const-ok 证据原文 -->
- **禁止**（类别卡）：禁止使用加权混合（0.4*rank(A) + 0.6*rank(B) / add(multiply(0.4,A),multiply(0.6,B))）
- **禁止**（类别卡）：禁止使用 ts_entropy / ts_skewness（幽灵算子）
- **禁止**（全局锁定）：禁止两条独立信号腿相加：加权（0.4×A + 0.6×B）、等权 add(rank(A), rank(B))、中缀 + 都算；第二个数据集只以条件（trade_when / if_else）、分组（group_rank / bucket）或残差（regression_neut / vector_neut）入场
- **禁止**（全局锁定）：禁止 ts_event_* 系列（平台没有）与幽灵算子；字段名逐一经 get_datafields 验证

### S4 改进（按顺序试：组合 → 类别卡 → 全局）

1. [全局] 判「无解 / 天花板」前先扫等价算子替换：signed_power → quantile、ts_scale → quantile / normalize。数值路径不同，一次动多个闸（含 prod，要读全部闸）（KOR/GLB 复现：KOR other466 signed_power→quantile：2Y 1.51→1.56、prod 0.6544→0.6397；GLB quantile 替 ts_scale：S +0.20、F +0.06、prod 0.475→0.565（DEC-72）） <!-- lint:const-ok 证据原文 -->
   - 注意：效应量逐区实测，禁外推；quantile 只收 1 个参数
2. [全局] 强但撞 prod 墙的快信号：用一个经济子集门控（trade_when 进 >0.5 出 <0.4 的慢变量，或 rank(cap)>0.2 ∩ 子集）只在子集里持仓（GLB/ASI/IND 复现：GLB-DL20D-SUBSET-GATE-FAMILY-20260921（prod 0.82→0.60–0.67）；ASI LLNgdpw2 / 88jaV5lv；IND ZYbqREW1 / levk5JYN（prod 0.54–0.55）） <!-- lint:const-ok 证据原文 -->
   - 前提：未门控的基础信号 IS sharpe 不低于 2.5、fitness 不低于 1.5（GLB 2026-09-27 铁律：门控只修 prod / robust，不造强度）；慢信号门控后换手会升，只用于快信号
- 提醒：prod 与 self 两个端点都取 max、都过线才可提；不改持仓的降 prod 杠杆（hump、加大 decay）会把 self 推爆（EUR wave274） <!-- lint:const-ok 证据原文 -->
- 提醒：设置是强度闸：nanHandling / maxTrade / decay / 中性化换档等于换信号，跨档结果不可比（IND 行为族 S 2.19→0.46） <!-- lint:const-ok 证据原文 -->
- 提醒：decay 匹配信号速度：快信号上 decay 越大越差；decay 0 与 1 逐位相同，只留一个 <!-- lint:const-ok 证据原文 -->
- 提醒：prod 墙先看直方图分单颗钉子 / 密墙 / 可破三型，再决定换分母、换设置档或分组轴（决策表 D0-P 诊断前置） <!-- lint:const-ok 证据原文 -->

### S5 提交前

- 资格判定：`$WQ_PY tools/mode_b_qualify.py evaluate --region DEU --sharpe <S> --fitness <F> --two-year-sharpe <2Y>`（喂全指标，旁路 A–E 才会生效）
- 提交链：`submit_verdict` 只否决；prod 与 self 双端点实测（`check_correlation(refresh=True)`）；用户明确确认后才 `workflow_submit_alpha(confirm_submit=True)`——见 `worldquant-submit-alpha`

### 判死记录（不要重试；「归属」= payload 绑定 / 由条目名推断 / 关键词推断）

| 条目 | 族 | 下次怎么办 / 说明 | 数据集 | 归属 |
|---|---|---|---|---|
| DEU-PATTERN_SCORES-PROBE-DEAD-20261002 | pattern_scores 图表形态相似度 | DEU 不再投 pattern_scores（形态相似度方向不成立，零竞争≠有信号）；此集此前两波已实测却漏写 registry，导致 2026-09-29 被误锁进白名单——教训：锁白名单前必须交叉核 expressions.status | pattern_scores | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-PV30-GROUP-ONLY-NOT-SIGNAL-20261002 | pv30 统计聚类分组标签（GROUP 类，非信号本体） | pv30（含同类 pv29）不得进信号白名单，只能当 group_rank 的自定义分组轴使用。判定口径：凡 catalog.data_type=='GROUP' 的数据集一律降级为分组轴。S0 锁白名单时必须先查 catalog 的 da | pv30 | inferred | <!-- lint:const-ok 证据原文 -->
| DEU-W104-D0-DATASET-EMPTY-DEAD | DEU D0 日内快信号（pattern_scores/pv29/pv30/other455） | DEU D0 快信号路径在数据集层不可行：凡依赖历史计算的字段(形态相似度/行业分类/关系/残差)在 D0 都不可用。D0 仅适合当天到达的稀疏事件/新闻/日内量价原始字段，且需先 get_datafields(delay=0) 实测字段存 | pattern_scores | inferred | <!-- lint:const-ok 证据原文 -->
<!-- profiles:cell-panel:end -->

## 补充说明（手写）

<!-- profiles:manual:start -->
### 字段画像结论（2026-10-08）

`UNUSABLE` 2137｜`UNTESTED` 527｜**`AXIS_ONLY` 190**｜`DEAD` 23（共 2877）—— **0 产出，0 WEAK**

- `pattern_scores`（504 全高覆盖）：**40 条全灭，最高 S0.46** ⇒ 已判死，**未测的 487 个不必再投**。
- `pv30`（180）/ `pv29`（50）：`AXIS_ONLY` ⇒ **只能当轴**。
- `pv1` 元字段（`close`/`vwap`/`volume`/`cap`）：可作分母或轴；**单独作信号 prod 必高**（平台 sector 3749 / industry 3251 alphas）。

**⇒ 本类别在 DEU 无可用信号面。**

---

## ★★★ PV 类别复核（2026-10-14 WANL33–34，按探针 SOP 严格协议）

**已按 SOP 补测「从未探过的概念族」+「文献构造」，结论不变（可信度更高）**：

**资源画像**：`pv29`(50 字段) / `pv30`(180) 全是分组轴（`*_grouping_*` / `factor*_group*_score`）⇒ 规则排除；`pattern_scores`(504) 是唯一信号集；`pv109` cov 0.467 剔除；`pv1` DEU 无数据。

**概念族拆解揭示的真实缺口**：历史探测（40+10 条）只覆盖了「**相似度水平量**」（max/mean/median/min/dynamic_similarity）一个维度；以下三族**从未测过**：`std_similarity_*`（离散度）、`quantile95_similarity_*`（高分位强度）、`symmetry_triangle_*`。

**WANL33（双结构 × 未测族）**：`std_similarity_*` 族**一致负向**（−0.35~−0.65，TO 0.18–0.36）；分位族 +0.23；其余 ≤0.06。
**WANL34（文献构造：门控/时序秩/反向/形状）**：反向·清晰度优先 **0.65**（上限）；`trade_when(ts_rank>0.9)` 门控仅 **0.16**；`ts_delta`/`ts_zscore`/`signed_power` ≤0.29。

**⇒ 20 条双结构 + 跨族 + 文献构造全覆盖后，天花板 = S0.65（需 1.58）。判死确认。**

**★ 根因（有文献支持，非「探针不够」）**：
- Chart Library（16M 图表实盘前瞻）：形态匹配方向准确率仅 **50–55%**；其真正边际在**预测未来波动（高方差匹配 = 高波动）**，不在方向。
- Fuzzy-logic TA（FAJ 2004）：membership 模糊度与后续收益相关，但弱形态甚至方向相反。
- **⇒ 「相似度的离散度」预测的是波动而非截面方向**——与 alpha 目标（方向性 Sharpe）结构性不匹配。**这正是 504 个高覆盖、零竞争字段零产出的原因：不是没人发现，而是可提取信息的类型不对。**

**★ 方法论收获**：① 「探针太少」的正确打开方式是 **补概念族**（不是多跑同族字段——族内 PnL 相关 0.99）；② **文献构造必须实测**（文献说 >90% 门控有效，本平台实测 0.16）。

### ★★★ 轴用法收口（2026-10-14 WANL41）——PV 类别最终封闭

**PV 全类别清点（16 个）**：`pv29`(50) / `pv30`(285，其中 **180 个 GROUP 轴**) 均为**纯分组轴**；`pattern_scores` 三轮判死；**`pv109` 字段级核验 = 0 个 cov≥0.6 字段**（规则排除）；其余 12 个（pv1/pv13/pv17/pv20/pv47/pv71/pv103/pv106/pv132/pv173/continuation_score/intraday_pv_feats）**DEU 平台覆盖 = 0**（无数据）。

**pv30 因子轴 × 四个近失候选**（`factor1-4_group20_top800_513` 等，GROUP 型）：

| 变体 | S | 对照（无 pv30 轴） |
|---|---|---|
| `dlrQ1 + f1轴 + bucket` | 1.18 | 1.18（**无变化**） |
| `m238GSFA + f1轴 + subindustry` | 0.97 / F0.69 | 0.99 / F0.73（**略降**） |
| `rv + f2轴` | 0.66 | 0.90（**降**） |
| `m238Δ66 + f1/f2/f3轴` | 0.44–0.70 | 0.81（**降**） |

**★★ 两条新铁律（可迁移）：**
1. **轴增益是「字段 × 轴」特异的** —— `oth455` 轴曾把 starmine 抬 +0.84，但 `pv30` 因子轴对所有候选 **0 增益或负增益** ⇒ 换轴必须逐字段实测，不能假设「换轴有增益」。
2. **GROUP 轴会把 2Y 检查从宽松 `LOW_2Y_SHARPE` 切换为严格 `IS_LADDER_SHARPE`**（limit≈1.585）——本批 ladder 实测仅 **0.49–0.79**，且 `pwvY0wJ3` **prod 0.7146 > 0.7 失败** ⇒ **用 GROUP 轴换取 S 增益时，必须同时预判严格 ladder 的代价**。

**⇒ PV 类别在 DEU 最终封闭：可提交产出 = 0。**
<!-- profiles:manual:end -->
