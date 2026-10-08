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

## DEU 画像现状（2026-10-08）

| verdict | 数量 |
|---|---:|
| `UNUSABLE` | 17460 |
| `UNTESTED` | 3252 |
| `AXIS_ONLY` | 1390 |
| `DEAD` | 312 |
| `DEAD_STATIC` | 30 |
| `WEAK` | 26 |
| `DEAD_TURNOVER` | 19 |
| `DEAD_COUNT` | 4 |
| **`ALIVE`** | **1** |

**全 DEU 唯一过线字段**：`eps_y1_estimate_change_3mo`（`analyst_factor_signals`，单信号 **S1.66 / 2Y2.14 / sub0.98 / n_sg 60**）。

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

**★ 字段名会骗人** —— 实证：`iv_projected_*`（实为股息预测）、`probability_label*`（实为**收益预测**，EUR S4.65）、
`analyst7` 的 `est_q_dps_raised*`（实为**分析师上调家数**）。DEU 有 **2,845 个（10.5%）字段的名字机制 ≠ description 机制**。

```bash
# ① 先看该区的「真实机制」分布（选字段的第一步）
$WQ_PY tools/fields/field_profile.py --list-tags --region DEU

# ② 按机制筛选（逗号分隔 = OR）
$WQ_PY tools/fields/field_profile.py --query --region DEU --desc-tag count_breadth --verdict UNTESTED
$WQ_PY tools/fields/field_profile.py --query --region DEU --desc-tag surprise,revision
```

**可用标签**：`volatility` `probability` `percentile_rank` `regression_pred` `surprise` `revision` `estimate`
`forecast` `dividend` `valuation` `quantile_bucket` `count_breadth` `growth` `liquidity` `score` `return` `risk` `ratio`

**★ 立刻可见的价值**：DEU 按机制看，`probability` **729 个字段（含 5 个活/弱、316 未测）**、`count_breadth` **1,016 个（106 未测）**、
`forecast` **876 个（5 活/弱）** —— 这三个大机制都曾被我按名字误判。
