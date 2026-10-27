# USA / D1 `pv149`（分析师评级动作计数）字段画像与波 1 设计（2026-10-23）

> **定位**：USA 未点亮塔补挖的第 4 个数据集（`risk60` / `pv106` / `chart_return_model` 之后）。
> 平台类别 **PV（×1.1，0 颗 ACTIVE ⇒ 未点亮）**，满足「已点亮塔不作主数据集」用户规则（2026-09-19 定案）。
> 数据集级事实来自本地台账 `data/wqb.db`（`datasets` / `fields`）与平台 `get_datafields`；
> 标「未实测」的项不得当作已知。

## 1. 为什么选它（S0 选集理由）

`risk60`（prod 0.9917 结构性墙）与 `chart_return_model`（S 上限 1.22）判死后，
对 USA 全库 345 个数据集做五层排除（已亮塔 MODEL/ANALYST/EARNINGS、并行会话优先族、
历史判死记录、覆盖 <0.65、字段 <5），**存活仅 10 个**。其中：

| 候选 | 判读 | 结论 |
|---|---|---|
| `pv149` | PV 塔未点亮、6 字段、aC 1–20、**全库零回测零表达式** | **入选** |
| `us_equity_news` | OTHER；SPRE 明示「情绪域已饱和 prod 0.72–0.82 死」 | 不投 |
| `risk65` | RISK；与已判死的 `risk60` 同一借券费供应商，prod 先验 0.99 | 不投 |
| `other696` | OTHER；GBR 先验波 8 臂 `max |S| 0.57` | 不投 |
| `short_interest_pred` | 在 `settings.json._spre_20260917.excluded_families` | 排除 |

`pv149` 的独特处是**数据源与已交付机制不共享分子**：

| 判据 | 事实 | 为什么重要 |
|---|---|---|
| 塔位 | `datasets.category = PV`，该塔 0 颗 ACTIVE | 用户硬规则：已亮塔只作组腿 |
| 容量 | 6 字段、覆盖 0.98–1.00、全 MATRIX | 无 VECTOR 聚合前置；横截面可直接比较 |
| 拥挤度 | 字段级 aC **1–20**（initiations 9 / upgrades 7 / downgrades 20 / volume 5） | 对照 pv 主流数据集动辄数千条，几乎无人使用 |
| 历史 | 全区域 `backtest_results` 0 行、`expressions` 0 条、registry/ledger 零命中 | 不是「换个壳重跑」，是全新面 |
| 机制 | 分析师**评级动作计数**（上调/下调/首次覆盖） | 与已交付的 estimate-revision（EPS/营收预期）不同源；与 pv63 订单流、pv106 成本无关 |

⚠ **数据集名与内容不符**：平台数据集名是 "Holidays and Trading Hours Calendar"，
但 6 个字段全部是 `dld`（daily last data）评级动作计数。以**字段描述为准**，
名称疑为供应商沿用了历史包名（平台侧如此，无需处理）。

## 2. 字段画像总表（6 字段，全 MATRIX）

| 字段 | 含义（平台原文） | 类型 | 覆盖 | users | aC | 角色 |
|---|---|---|---:|---:|---:|---|
| `pv149_dld_1a` | Number of ratings that were initiated | MATRIX | 0.9836 | 7 | 9 | **信号**：首次覆盖/新增覆盖关注度 |
| `pv149_dld_2a` | Number of upgrades | MATRIX | 0.9799 | 3 | 7 | **信号**：上调计数 |
| `pv149_dld_3a` | Number of downgrades | MATRIX | 0.9801 | 12 | 20 | **信号**：下调计数 |
| `pv149_dld_volume` | Total volume | MATRIX | 1.0000 | 5 | 5 | **信号/分母**：评级动作总量（口径待实测确认） |
| `pv149_dld_week` | Number of the week | MATRIX | 1.0000 | 2 | 2 | **非信号**：日历序数（已入黑名单） |
| `pv149_status_5` | Status code ... valid / missing / suspended | MATRIX | 1.0000 | 1 | 1 | **非信号**：数据质量码（已入黑名单） |

### 2.1 数据类型、分布与可用性

- **计数型整数**，右偏、零膨胀：TOP3000 中大多数股票在单日没有评级动作，`1a/2a/3a`
  预期大量 0（结构判读，非抽样统计）。⇒ 横截面直接用裸值会**大量并列**，
  必须 `ts_decay_linear` / `ts_sum` 累积后再 `group_rank`。
- **覆盖率 0.98** 表示字段有定义；缺的 1.7–2% 由 `nanHandling=ON` 承接成 NaN，不参与排序。
  不需要 `ts_backfill`（回填会把「无评级动作」伪造成「有」）。
- **量纲差异**：`2a/3a` 是 0–个位数的日计数；`volume` 口径未知（可能是评级动作总数，
  也可能是数据记录量）。因此 `volume` 只作比值分母，不单独当水平信号。
- **更新频率**：日频；评级动作是**事件型**更新（无动作日不变或归零，需波 1 去壳臂实测）。
- **可用性**：`validate_expressions` 实测 6/6 字段存在（`unknown_fields=[]`）。

## 3. 机制假设（发批前写定，不得事后改判据）

| 假设 | 机制 | 代表构造 | 方向先验 |
|---|---|---|---|
| **H-lvl 净修正水平** | 上调 − 下调 = 分析师共识的方向性修正；经典 revision momentum | `ts_decay_linear(2a − 3a, 22)` | 高净上调 → 多 |
| **H-ratio 修正平衡** | `(上调−下调)/(上调+下调+1)`，剔除覆盖基数差异（大票天然动作多） | 63 日窗口比值 | 高平衡 → 多 |
| **H-asym 降级不对称** | 分析师「不愿下调」⇒ 真下调的信息含量高于上调 | 仅 `3a` 的反向 | 高下调 → 空 |
| **H-init 首次覆盖** | 新增覆盖 = 新的卖方关注/资金流，事件后漂移 | `ts_decay_linear(1a, 63)` | 高首次覆盖 → 多 |
| **H-act 修正活动强度** | 上调+下调总量 = 分歧/关注度；高活动 → 拥挤反转 | `ts_decay_linear(add(2a, 3a), 22)` | 高活动 → 空（双向都测） |
| **H-srps 修正意外** | 当前 22 日净修正相对自身 252 日历史的 z 分 = 意外修正 | `ts_zscore(ts_decay_linear(2a−3a,22), 252)` | 意外向上 → 多 |
| **H-volnorm 活动归一** | `(2a−3a)/(volume+1)` = 单位评级动作中的净方向 | 22 日比值 | 高净占比 → 多 |

**预登记判据**（波 1 收批时逐条执行，不临时加码）：

1. 任一臂 RA 全过（`S ≥ 1.58`、`F ≥ 1.0`、`SUB/S ≥ 0.435`、2Y 达标）⇒ 立即做 prod 探针，
   不先做同族扩展（`risk60` 教训：16 臂全过 RA 才测 prod，白烧一轮）。
2. **方向纪律**：只把「机制上说得通」的方向当候选。某臂反向 S 更高**不构成**反号理由，
   除非能写出经济机制（pv106 教训：成本水平稳定为负，反号无机制支撑 ⇒ 停投）。
3. **去壳臂 D0 是必读项**：若 D0 的 turnover < 2% 且 9 条重壳臂也 < 2% ⇒ 字段准静态，
   本集判停；若 D0 turnover 很高（> 50%）而重壳臂 < 2% ⇒ 是壳压平，下批换中档壳。
4. 若 `2a`/`3a`/`1a` 全部臂 `|S| < 0.6` ⇒ 本集信号幅度不足，停投（forum_sentiment 同构）。
5. 若仅 `volume` 归一臂有信号而三个动作计数全部无 ⇒ 说明信号来自 `volume` 口径本身，
   先查清 `volume` 语义再决定，不直接扩批。

## 4. 波 1 十臂设计（`pv149_w1`）

设置（除 D0 外全部一致）：USA / TOP3000 / D1 / **SUBINDUSTRY** / decay 8 / truncation 0.08 /
`nanHandling=ON` / `maxTrade=OFF` / `pasteurization=ON` / `unitHandling=VERIFY` /
2014-01-01 → 2023-12-31 / REGULAR。

| # | 假设 | 表达式核心 | 角色 |
|---:|---|---|---|
| N1 | H-lvl | `group_rank(ts_decay_linear(2a−3a, 22), subindustry)` | 经典基线 |
| N2 | H-lvl | N1 反向 | 方向裁决 |
| N3 | H-ratio | `group_rank((ts_decay_linear(subtract(2a, 3a), 63)) / (add(ts_decay_linear(add(2a, 3a), 63), 1)), subindustry)` | 覆盖基数归一 |
| N4 | H-asym | `reverse(group_rank(ts_decay_linear(3a, 22), subindustry))` | 降级压力单独测 |
| N5 | H-init | `group_rank(ts_decay_linear(1a, 63), subindustry)` | 首次覆盖 |
| N6 | H-act | `reverse(group_rank(ts_decay_linear(add(2a, 3a), 22), subindustry))` | 活动强度（负） |
| N7 | H-act | N6 反向 | 方向裁决 |
| N8 | H-srps | `group_rank(ts_zscore(ts_decay_linear(2a−3a,22), 252), subindustry)` | 意外修正 |
| N9 | H-volnorm | `group_rank(ts_decay_linear(2a−3a,22) / (ts_decay_linear(volume,22)+1), subindustry)` | 口径探针 |
| D0 | 去壳诊断 | `group_neutralize(ts_sum(2a,22)−ts_sum(3a,22), industry)`，**decay 0 / 中性化 NONE** | 原生换手 + 裸信号 |

（`2a` = `pv149_dld_2a`，`3a` = `pv149_dld_3a`，`1a` = `pv149_dld_1a`。）

## 5. 波 1 结果与裁决

**派发（2026-10-23 12:23）**：两个 multisim（同批设置一致 ⇒ 一次 POST 收 9 臂 + 1 臂）
- `usa_pv149_w1_batch_a`（N1–N9，SUBINDUSTRY / decay 8）→ multisim `1AURxN2dt4E08Q76ygQEN9A`
- `usa_pv149_w1_batch_d0`（D0 去壳，NONE / decay 0）→ multisim `wgE9G9O854i8Lz6BuOB9DF`

门禁：`wave_gate` all_pass=true 10/10（region 四闸放行；SEM 黑名单 2 字段、剔除 0；
inspect 降级包 enforced、违规 0；prod-sat 零命中）。

**结果表**（2026-10-23 12:38 收批，9 臂 multisim + 单发 D0；全部 `USA/D1/PV ×1.1`）：

| # | alpha id | S | F | TO | RET | 2Y | SUB | SUB/S | RN | RA 失败 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| N1 | `N1eJj0jL` | **0.74** | 0.30 | 8.85% | 2.09% | 0.67 | 0.59 | 0.80 | 0.68 | S/F/2Y |
| N2 | `d5K37plw` | −0.74 | −0.30 | 8.85% | −2.09% | −0.67 | −0.59 | — | −0.68 | S/F/SUB/2Y |
| N3 | `0mjNQqKr` | 0.42 | 0.13 | 7.02% | 1.29% | 0.12 | 0.26 | 0.62 | −0.05 | S/F/2Y |
| N4 | `2rjXZMnY` | −0.07 | −0.01 | 3.93% | −0.20% | −0.18 | 0.30 | — | −0.15 | S/F/2Y |
| N5 | `vROpz8ed` | 0.22 | 0.05 | 4.57% | 0.77% | −0.34 | −0.01 | — | 0.71 | S/F/SUB/2Y |
| N6 | `6XAoq7aJ` | −0.16 | −0.03 | 4.07% | −0.47% | −0.30 | 0.15 | — | −0.36 | S/F/2Y |
| N7 | `78ovXWxQ` | 0.16 | 0.03 | 4.07% | 0.47% | 0.30 | −0.15 | — | 0.36 | S/F/SUB/2Y |
| N8 | `VkdmlVXM` | 0.57 | 0.21 | 8.37% | 1.68% | 0.42 | 0.49 | 0.86 | 0.68 | S/F/2Y |
| N9 | `leM5zdre` | 0.68 | 0.29 | 7.95% | 2.26% | 0.58 | **0.69** | **1.01** | 0.76 | S/F/2Y |
| D0 | `9qEdK5Ko` | 0.30 | 0.18 | **19.44%** | 7.34% | 1.25 | 0.21 | 0.70 | −0.07 | S/F/2Y |

**归因（逐条对照 §3 预登记判据）**：

1. **判据 1（任一臂 RA 全过）未触发**：10/10 全部 0 过闸，无一臂进入 prod 探针。
2. **判据 2（方向纪律）**：N1 +0.74 / N2 −0.74 完全镜像 ⇒ 「净上调 → 多」方向与经典 revision momentum 同号，
   方向本身没有错；N4（单独看降级）−0.07 说明**降级单独无信息**，信息全在 2a−3a 的净差里。
3. **判据 3（去壳臂 D0）**：D0 TO **19.44%**，既不是 <2%（准静态证伪）、也不是 >50%（壳压平证伪）。
   ⇒ 字段有真实日频变动，重壳把 TO 压到 4–8.9% 是**正常平滑**，不是把静态列压平。此条通过。
   D0 的 2Y 1.25 反而高于重壳臂（0.12–0.67），但 S 只有 0.30 ⇒ 裸信号幅度弱，壳抬 S 的代价是压 2Y。
4. **判据 4（信号幅度）**：`2a/3a/1a` 全部臂最好 **0.74**（N1），**只到平台线 1.58 的 47%**；
   次优 N9 0.68（分母归一）、N8 0.57（自有史 z）。要够线需 S 提升 **2.1×**，
   而本项目历史里单靠壳/设置最多提升 20–40%（board_gov_stats 波 87 实证），2.1× 不可能。
5. **判据 5（volume 口径）**：N9（volume 归一）0.68 略低于 N1 0.74 ⇒ 信号**不来自** `volume` 口径，
   `volume` 语义无需再查。N9 的 SUB/S=1.01 是唯一亮点（大票/小票一致），但绝对值同样不足。

**裁决：停投（`USA-PV149-SIGNAL-SHORT`）**。三条独立理由：

1. **幅度结构性不足**：3 个信号字段 × 7 机制 = 10 臂，最好 0.74 / F 0.30 / 2Y 0.67，对 1.58 / 1.0 / 1.58
   三条线分别差 **2.1× / 3.3× / 2.4×**。不是「差一点」，是量级不够。
2. **没有未测的机制轴**：初值(`1a`) 0.22、活动强度(`add(2a, 3a)`) ±0.16、降级单独 −0.07、比值 0.42、
   自有史 z 0.57 ⇒ 六个方向全部试过，唯一有幅度的是净差（0.74），已用最好壳（SUBINDUSTRY + decay 8）。
3. **提幅的唯一路径 = 加强同一机制，而该机制已在 prod 池里**：净评级修正与已交付的 6 颗 analyst
   revision 家族（EPS/营收修正）同属「分析师共识方向」，把 pv149 的 S 从 0.74 抬到 1.58 只能靠更尖锐的
   revision 构造 ⇒ prod 相关性先验只会更高。按 2026-10-23 报告 §9.1 的教训（「冷门数据集 + 经典异象
   不提供相关性优势」），不值得再烧一轮。

**未做 universe 试探的理由（留痕，防日后追问）**：TOP1000/TOP500 对被分析师覆盖长尾更干净，理论上可抬
S 20–40%，但即使 40% 也只到 1.04，仍差 0.54；且 universe 换档会把「PV 塔 ×1.1」的塔位保持不变、
不改变上述第 3 条的相关性结论。故一次 6 臂的 universe 探针**预期不改变裁决**，不做。

**可复用结论**：
- **计数型稀疏事件字段的 S 上限由「事件发生率」决定**：6 个字段里 3 个是低频评级动作，
  重壳后横截面已把 3000 只票全部分开（long/short 1479/1532），不存在「排序并列」问题，
  S 仍只有 0.74 ⇒ 并列不是瓶颈，**事件本身的经济含量**才是。
- **D0 的 2Y 可以显著高于重壳臂**（1.25 vs 0.67）：去壳诊断不能只看 TO，还要看 2Y——若 D0 的 2Y 好而 S 差，
  说明信号集中在近年但幅度低，平滑壳会把近年信息抹平。本集属此型。
- **aC 1–20 + 覆盖 0.98 + 全库零回测** 仍可能是一个**弱信号**数据集；「没人用」不等于「有用」，
  与 pv106 的「aC 104 仍全负」是同一枚硬币的两面。

## 6. 档案索引

| 内容 | 位置 |
|---|---|
| 波 1 逐臂表达式 | `tracking/USA/runs/usa_pv149_w1_n{1..9}.txt` / `_d0.txt` |
| 波 1 设置（逐臂） | `tracking/USA/runs/usa_pv149_w1_spec.json` |
| 波 1 派发件（2 个 multisim） | `tracking/USA/runs/usa_pv149_w1_dispatch.json` |
| 波 1 结果（平台） | multisim `1AURxN2dt4E08Q76ygQEN9A` / `wgE9G9O854i8Lz6BuOB9DF` |
| 语义台账 | `ledger_kv`: `USA/s1_semantic_pv149` |
| 体检包（降级 coverage-only） | `tracking/mining/field_inspect_usa_pv149.json` |
| 同轮前序画像 | `_usa-risk60-field-profile-20261023.md`、`_usa-pv106-field-profile-20261023.md`、`_usa-chart-return-model-field-profile-20261023.md` |
