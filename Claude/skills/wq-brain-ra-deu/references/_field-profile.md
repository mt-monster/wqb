# 字段画像（开批前判断的硬依据）· DEU 视图

> 回到 [DEU 区域流程](../SKILL.md)
> 工具：**`tools/fields/field_profile.py`（多区域通用）**｜主表：`data/wqb.db::field_profile_perf`｜本区视图：`field_profile_deu`

## 这张表解决什么问题

**把「该不该测这个字段」从一条回测降级成一条 SQL。**

DEU 有 **22494 个字段 / 178 个数据集**，但一批只测 10 个 ⇒ 全扫要 **2249 批**。
画像用**已有的回测副产品**（换手 / S / 2Y / sub）把字段预先判成 9 类，**开批前先过滤**。

## ★ 多区域隔离设计（2026-10-08 重构，勿再串号）

**旧版缺陷**：表名硬编码 `field_profile_deu` + build 首行 `DROP TABLE IF EXISTS`
⇒ **跑第二个区域会清掉已建区域的画像**。已修复。

| 层 | 名称 | 说明 |
|---|---|---|
| **主表** | `field_profile_perf` | **复合主键 `(region, dataset, field)`** —— 所有区共存于一张表，一份 schema |
| **每区视图** | `field_profile_deu` / `field_profile_eur` / … | 只读视图，各自 `WHERE region='<R>'` ⇒ **查询体验 = 每区一张独立表** |
| 写入语义 | `DELETE WHERE region=?` | build 只清**本区**（不再 DROP 整表） |

**⇒ 建 EUR 画像不影响 DEU；两区查询互不串号（已实测验证：perf 表 61103 行 = DEU 22494 + EUR 38609，各视图 region 纯度 100%）。**

## 与仓库既有 `field_profile` 表的分工（勿混淆）

| 表 | 来源 | 内容 | 用途 |
|---|---|---|---|
| `field_profile`（既有） | **WebDataScope 数据包** | `shape` / `skew` / `kurt` / `freq` / `near_zero_ratio` | 「字段→模板族」匹配，供 GEM 过滤绑定字段 |
| **`field_profile_perf`**（本工具建） | **回测副产品** | `to_med`（换手）/ `best_s_sg` / `best_2y_sg` / `verdict` | **开批前的可用性判断** |

**★ DEU 不在 WebDataScope 数据包覆盖内** ⇒ 既有的 `field_profile` 表**对本区无数据**（实测：`field_profile` 30705 行全为 USA/CHN/EUR/ASI/GLB/JPN/KOR，**DEU 0 行**）。
**⇒ 本工具是 DEU 唯一的字段画像来源**；对 EUR 等有数据包的区，两者互补（数据包给统计形状，本工具给实测性能）。

## 九类 verdict

| verdict | 判据 | 处置 |
|---|---|---|
| `UNUSABLE` | `coverage < 0.6` | **永久剔除**（占全量 77.6%） |
| `AXIS_ONLY` | `ftype == GROUP` | **只能当分组轴**，不进信号白名单 |
| `UNTESTED` | 通过上两关但 `n_tests == 0` | 可探（仍需按机制族排优先级） |
| `ALIVE` | 单信号 S ≥ **1.58** | 过闸线 |
| `WEAK` | 单信号 S ≥ 1.10 | 有信号但不够强 ⇒ 优先深挖 |
| `DEAD` | 已测 S < 1.10 | 不再投入 |
| **`DEAD_STATIC`** | `to_med < 0.03` | **静态属性，任何骨架都无用** |
| **`DEAD_TURNOVER`** | `to_med > 0.70` | **被 `HIGH_TURNOVER` 闸直接拒** |
| **`DEAD_COUNT`** | 名字含 `num/count` 且 2Y≥1.3 且 S≤0.7 | **「2Y 有 S 无」判死形态** |

`best_*_sg` 三列是**单信号记录**的最好值（已剔多腿 `add` 污染）；`n_sg` = 单信号记录数。

## 用法（跨区域通用）

```bash
# 建表 / 更新（先回填平台，再建）—— 只影响指定区域
$WQ_PY tools/data-repair/backfill_deu_from_platform.py --region DEU --stage IS
$WQ_PY tools/fields/field_profile.py --build --region DEU
$WQ_PY tools/fields/field_profile.py --build --region EUR          # 任意区域

# 一次建全部有实测数据的区域（互不影响）
$WQ_PY tools/fields/field_profile.py --all-regions

# 盘点所有已建画像的区域
$WQ_PY tools/fields/field_profile.py --list

# 查询（查主表并按 region 过滤；也可直接查每区视图）
$WQ_PY tools/fields/field_profile.py --query --region DEU --verdict WEAK
$WQ_PY tools/fields/field_profile.py --query --region EUR --category analyst --min-s 1.1
# 等价：SELECT * FROM field_profile_eur WHERE verdict='ALIVE';
```

> 旧命令 `tools/fields/field_profile_deu.py ...` 仍可用（已改为**兼容转发壳**，行为完全一致并提示迁移）。

## ★ 开批前的三步零成本检查（必做）

```bash
# ① 查画像：目标字段（或同族字段）的 to_med
$WQ_PY tools/fields/field_profile_deu.py --query --region DEU --verdict UNTESTED --limit 40
#    to_med < 0.03 或 > 0.70 ⇒ 直接跳过，不要开批
# ② 校验字段名与类型（MCP，零成本）
#    preflight_expressions(alpha_expressions=[...], region="DEU", universe=TOP500, delay=1)
#    看 unknown_fields 是否为空；VECTOR 字段会被提示需 vec_*
# ③ 校验算子元数
#    $WQ_PY -c "from wqb.expression import op_arity; op_arity.ensure_safe_for_dispatch(exprs)"
```

**②③ 缺失的代价都是"整批 CANCELLED"（一次 10 条全废），已在 DEU 各踩过一次。**

## ★ 换手外推法（对未测字段也有效）

未测字段本身没有换手记录，但**同一 `family` 的字段换手高度相似**，可外推：

| 命名族 | 实测换手 | 结论 |
|---|---|---|
| `count_institutional_*` / `aggregate_share_count_*` | **0.0146 ~ 0.0204** | 机构家数类 ⇒ 静态 |
| `mdl28_*_credit_structural_*_rank` | **0.0245 ~ 0.0277** | 信用排位类 ⇒ 静态 |
| `star_sr_*_d1` / `credit_risk_*_score_d1` | **0.0221 ~ 0.0229** | 信用分类 ⇒ 静态 |
| `anl93_{accuracy,consistency,correv,estimator}_*` | **0.019 ~ 0.029** | 分析师技能元数据 ⇒ 静态 |
| `est_12m_*_estimate_change_*` | **0.045 ~ 0.19** | 预期变化率 ⇒ **可用** |

**⇒ 开新批次前，先查该族**已有代表字段的 `to_med`，**就能预判整族值不值得探**。

## DEU 画像现状（2026-10-08 重建，实测口径）

| verdict | 数量 | 占比 |
|---|---:|---:|
| `UNUSABLE` | 17460 | 77.62% |
| `UNTESTED` | **3196** | 14.21% |
| `AXIS_ONLY` | 1390 | 6.18% |
| `DEAD` | 358 | 1.59% |
| `DEAD_STATIC` | 34 | 0.15% |
| `WEAK` | **29** | 0.13% |
| `DEAD_TURNOVER` | 19 | 0.08% |
| `DEAD_COUNT` | 6 | 0.03% |
| **`ALIVE`** | **2** | 0.01% |

- **已测 448 个**（31 活/弱 + 417 判死）＝全量 1.99%；**可寻址池 = 3,644**（已测 448 + 未测 3,196）。
- **两个 ALIVE**：`eps_y1_estimate_change_3mo`（S1.67/2Y2.14）、`netprofit_y1_estimate_change_3mo`（S1.70/2Y1.66）。
- 按语义归族后，31 个活/弱只来自 **5 个机制族**：分析师修正 16、收益预测概率 6、ML/评级合成分 7、分析师跟随收益 2。
- 完整语义画像报告：`output_report/DEU_field_profile_by_description_20261008.md`。

## ★★ 未测池的真实结构（2026-10-08 新增，勿再误读「3,196 个没试过的普通字段」）

**100% 是非标量类型**：`MATRIX 2,775` + `VECTOR 410` + `SYMBOL 11`。

| 类型 | 能否直接用 | 证据 |
|---|---|---|
| MATRIX | **能裸用**（DEU 实证） | `group_rank(ts_scale(pattern_field,66),sector)`、`rank(mdl264_*_class)` 都跑出真实 sharpe（组合腿最高 S1.94）|
| VECTOR | **不能裸用**，需 `vec_*` | `vec_avg(mean_loan_rate_main)` 成功（analyst93，组合 S2.02）|
| SYMBOL | **不是信号** | 日期/时间戳/ISO 国家码/序号 ⇒ 11 个应从「潜在空间」里扣除 ⇒ **有效未测 3,185** |

> ⚠ **USA 的「MATRIX 禁套」结论不可外推到 DEU** —— 同一周内两区实测结论相反。类型处置必须**逐区实测**。

未测池的其余关键结构：
- **496 个（16%）来自「零测试兄弟」的 dataset**：`other455` 300（**供应链图谱 Node2Vec 嵌入的 PCA 分量**，数据源是 USA 图谱）、`news17` 48、`pv29` 40（行业聚类，可当轴）、`news50` 37、`sentiment27` 18（**SYMBOL 毒药**）。
- **含毒药字段的未测池**：ANALYST/estimate 379 里大量是「覆盖标识 / ISO 币种代码」（如 `anl44_2_dps_coveredby`、`..._lastactccy`）⇒ 探测前必须读 description。
- **PV/score 415** ＝ 图表形态相似度（`pattern_scores` 两代命名：`*_simscore_lookback*` 已测 17 个，`dynamic_similarity*` 未测）。

## 已知局限（别把 `UNTESTED` 当"从未测过"）

- 只覆盖**平台上仍存在的 IS alpha**；"alpha 被删 / 未持久化 / `field_of()` 提取失败"都会误判为 UNTESTED；
- 回填只做了 `DEU / stage=IS`，OS 未做；
- 平台列表接口**分页上限 ~1100**（HTTP 400 后停止），可能有遗漏；
- 画像**只判"有没有信号"**，不判"配什么机制" ⇒ 需配合 `field_characteristic_to_mechanism.md`。

## ★ 跨区对照（2026-10-08 · 含 W199 实测验证）

**建了 EUR 画像后看到一个强对照，随后用 W199 实测验证 —— 结论与初见时的直觉相反。**

| 字段（同名同框架） | EUR | **DEU（W199 实测）** |
|---|---:|---:|
| `predicted_surprise_pct_f12m_earnings_5` | **S2.06 ALIVE** | **S0.82~0.90 DEAD** |
| `predicted_surprise_pct_f12m_revenue_4` | **S2.09 ALIVE** | **S0.69~0.76 DEAD** |
| `predicted_surprise_pct_fy1_revenue_4` | 未测 | S0.95 DEAD |
| `predicted_surprise_pct_fy2_ebitda_4` | 未测 | S1.04 DEAD |

**W199 批次**：10 条，用本会话已验证框架（行业内相对 + `ts_decay_linear` d3 + gran 0.02 + 窗 1/120）+ 简化框架对照。
**结果：全部失败（S −0.12~1.04），无一条接近 1.58。**

### ★★★ 由此确立的结论（修正此前假说）

1. **不是「形式选错」** —— 我原推测「DEU 只测了绝对版，补测 `_pct_` 版就有戏」；**实测证否**：DEU 的 pct 版同样无效。
   **⇒ 真实原因是跨区机制差异，不是形式差异。**
2. **同字段 + 同框架，跨区效果可以差 1.2~1.3 个 Sharpe** ⇒ **「机制有效」是区域属性，不是字段属性。**
3. **跨区对照是「提出假设」的工具，不是结论** —— 它能高效指出值得一试的候选，但**必须实测验证**。
   （本次对照成功提出了一个好假设，但假设被实测推翻 —— 这本身就是对照的价值：**用低成本实验排除了一个方向**。）

**★ 用法**（仍然有效，只是预期要现实）：
```bash
# 别区的 ALIVE/WEAK，在本区什么状态？
$WQ_PY tools/fields/field_profile.py --query --region EUR --min-s 1.5
$WQ_PY tools/fields/field_profile.py --query --region DEU --verdict UNTESTED --limit 60
```

## 全链路方法论（跨区域通用）

画像只是链路的第一层。**从画像到产出 alpha 的完整七层思路**（选区域 → 选字段族 → 开批前三闸 → 信号构造 → 结构维度 → 参数微调 → 闸门判定 → 闭环回填），
含五条铁律与本会话 DEU 完整实战轨迹，见 [`docs/reference/field_profile_to_alpha_playbook.md`](../../../../docs/reference/field_profile_to_alpha_playbook.md)。

## ★ 画像的使用判断流程（跨区域通用）

本页讲"DEU 的画像是什么"；**「怎么用画像判断有无信号」的 7 步否决漏斗 + 三层证据等级**，
以及 13 区完整画像汇总，见 [`docs/reference/field_profile_usage_guide.md`](../../../../docs/reference/field_profile_usage_guide.md)。

## ★★ 按 description 机制选字段（2026-10-08 新增，替代"按名字族"）

**★ 字段名会骗人，数据集名也会。** 实测（DEU 22,494 字段，description 覆盖率 100%）：
名字机制与 description 机制的不一致比例**视规则宽严在 10% ~ 75% 之间** ⇒ 结论只有一个：**名字不可作为选字段依据**。
已实证 10 类硬误判，其中两类连数据集名都是错的：

| 字段 / 数据集 | 名字暗示 | description 真实语义 |
|---|---|---|
| `liquidity_money_flow_alignment` | 流动性-资金流对齐 | **Relative Turnover (RTN63D)** |
| `volume_anomaly_price_positioning_2` | 量价异常定位 | **Detrended Price Oscillator (DPO)** |
| `iv_projected_dividends_fy11_3` | 隐含波动率 | **内在价值模型 DPS 预测** |
| `dl_riskfree_returns`（数据集）| 无风险收益率 | **前瞻市场中性收益的分位桶/概率/回归预测** |
| `probability_label3_5quantile_*` | 概率标签 | 前瞻收益落入第 3 桶的 log 概率 |
| `est_12m_*_raisednum_*` | 预期上调 | **上调家数**（count_breadth）|
| `act_q_cpx_surprisenum` | 惊喜值 | **计算 surprise 所用的估计数**（参与量）|
| `anl93_profitabilityprev_estimator_*` | 盈利能力 | **正确预测概率 / 跟单日收益** |
| `mdl238_industry_rank` | 行业排名 | **Smart Holdings 分的行业百分位（机构持股概率）** |
| `news17`（数据集）| 新闻 | 内含**分析师荐股变化分**（`analyst_recommendation_change_score`）|

```bash
# ① 先看该区的「真实机制」分布（选字段的第一步）—— 26 族
$WQ_PY tools/fields/field_profile.py --list-tags --region DEU

# ② 按机制筛选（逗号分隔 = OR）；mech_all 列显示**全部**命中标签
$WQ_PY tools/fields/field_profile.py --query --region DEU --desc-tag count_breadth --verdict UNTESTED
$WQ_PY tools/fields/field_profile.py --query --region DEU --desc-tag surprise,revision

# ③ coverage 边界人口（0.6 刀切线两侧；DEU 有 1593 个字段落在 [0.5,0.6) 被整体弃用）
$WQ_PY tools/fields/field_profile.py --query --region DEU --min-cov 0.5 --max-cov 0.6
```

**26 个机制标签**：`volatility` `probability` `percentile_rank` `regression_pred` `surprise` `revision` `estimate`
`forecast` `dividend` `valuation` `quantile_bucket` `count_breadth` `growth` `liquidity` **`cluster_label`** `score`
`return` `risk` `ratio` **`level_amount`** **`intraday`** **`technical`** **`sentiment`** **`uncertainty`** **`event`**

**★ 三个必须知道的读数口径**（都是实测踩出来的）：
1. **`mech_all` 与筛选不同源**：`--desc-tag` 是 LIKE 过滤，单标签只显示优先级首个命中 ⇒ 用 `mech_all` 列确认「为什么命中」。
   例：`act_q_cpx_surprisenum` 的 `mech_all = surprise/estimate/count_breadth` —— 名义 surprise 实为「参与家数」。
2. **标签优先级把「家数」藏在「预期」里**：`estimate`(#7) 先于 `count_breadth`(#12) ⇒ "Number of raised analyst estimates…" 单标签显示 `estimate`。
   刻意不改（会改写 9,051 个字段标签且误伤真均值），**查广度语义请用 `--desc-tag count_breadth`**。
3. **关键词匹配带词边界**（已修）：裸子串会让 `"Operating Activities - Net Cash Flow"` 命中 `rating` → `score`。

**★ 立刻可见的价值**：DEU 按机制看，`probability` 732 个（含 5 活/弱、**316 未测**）、`count_breadth` 1,023 个（106 未测）、
`forecast` 743 个（5 活/弱）、**`cluster_label` 1,799 个（341 未测，纯图谱嵌入）** —— 后三个大机制都曾被我按名字误判。
