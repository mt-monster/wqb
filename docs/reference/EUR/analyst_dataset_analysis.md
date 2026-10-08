# EUR ANALYST 类 · 16 个数据集逐一分析

> 分析时间：2026-10-07 22:08–22:40。
> **数据来源全部为平台实查**（`get_datasets(category=analyst)` + `get_datafields`），本地 catalog 不可信（见 §0）。
> 设置档：`EUR / TOPCS1600 / SUBINDUSTRY / decay4 / maxTrade ON / nanHandling ON`。
> 拥挤度口径：`userCount` / `alphaCount` 为**平台全量**（含他人），非本账号。

---

# 〇 ★ 首要发现：本地 catalog 只记录了 4 个，实际有 16 个

| # | 数据集 | 字段 | user | alpha | 值评分 | 覆盖中位 |类型 | 本轮状态 |
|---:|---|---:|---:|---:|---:|---:|---|---|
| 1 | `model52` | 3 | 1 | 2 | 5.0 | 0.199 | M3 | ❌ 覆盖过低 |
| 2 | `analyst81` | 5 | 5 | 5 | 5.0 | 0.232 | M5 | ❌ 覆盖过低 |
| 3 | `analyst_base_ref` | 17 | 5 | 6 | 3.0 | 混合 | M+V | ⚠ 共识基础量 |
| 4 | `analyst40` | 22 | 10 | 12 | 5.0 | 0.30 | M+V | ❌ **董事变动，覆盖 0.26–0.37** |
| 5 | `analyst_factor_signals` | 108 | 32 | 50 | 2.0 | 0.32 | M108 | ⚠ **今日已挖（130 条）** |
| 6 | `analyst_consensus` | 1929 | 40 | 70 | 3.0 | ≈0.80 | V 为主 | ★ 字段最多，user 低 |
| 7 | `analyst9` | 111 | 47 | 76 | 2.0 | ≈0.59 | V106/M5 | ✅ 今日测过（S1.69） |
| 8 | `analyst11` | 445 | 92 | 138 | 3.0 | ≈0.86 | M | ❌ **实为 ESG 数据集** |
| 9 | `analyst45` | 61 | 147 | 242 | 2.0 | **1.000** | **V61** | ★ **CT 最高（+0.73）** |
| 10 | `analyst14` | 121 | 157 | 265 | 1.0 | 0.500 | M121 | ⚠ coverage 是占位值 |
| 11 | **`analyst39`** | **24** | **263** | **541** | 2.0 | **0.913** | **M24** | ★★ **本类最优落点** |
| 12 | `analyst15` | 1744 | 335 | 889 | 2.0 | 0.500 | M | ❌ **已是 GICS 行业聚合值** |
| 13 | `analyst10` | 961 | 595 | 1369 | 2.0 | ≈0.95 | V+M | ❌ 拥挤 |
| 14 | `analyst7` | 1111 | 671 | 3073 | 1.0 | 0.500 | M | ⚠ 今日测过（S1.97，四项接近） |
| 15 | `analyst4` | 776 | 807 | 3011 | 1.0 | ≈0.86 | M+V | ❌ 拥挤 |
| 16 | `analyst69` | 813 | 1615 | **14081** | 1.0 | ≈0.94 | V 为主 | ❌ **alpha 14081，全类最挤** |

**★★ 两个 catalog 层面的错位**（今日第4、5 次）：
1. **本地只有 4 个**：`analyst_revision_horizons` / `analyst7` / `analyst9` / `analyst_factor_signals`。
2. ★★ **`analyst_revision_horizons` 不在这 16 个里** —— 它是**今日挖了 130 条的主力集**，
   说明「category=analyst」这个过滤条件会漏掉一类数据集，**不能只按 category 选集**。

---

# 1★★ 实测打断：`coverage` 是占位值，不是真实截面宽度

这是本轮最重要的发现，**直接影响 S0 体检的「覆盖 ≥0.35」门槛能否使用**。

| 数据集 | 平台报coverage | **实测 TO**（反映真实截面） | 判读 |
|---|---|---|---|
| **`analyst7`** | **全部精确 0.5**（27 个字段无一例外） | **TO 0.0092** | ❌ 截面极窄 |
| **`analyst39`** | 0.70–0.92（看着很高） | **TO 0.0172 / 0.0206** | ❌ 同样窄 |
| `analyst45` | 全部精确 1.000 | TO 0.1372 | ⚠ 中等 |

⇒ ★★★ **「coverage 精确等于 0.5 或 1.0」是平台默认值**，
   真实截面宽度只能靠**派 1 条仿真看 TO** 或读 `long_count`/`short_count` 来判断。
⇒ ★ **修正后的 S0 体检顺序**：派 1 条探针 → 看 TO → 再决定是否投入挖矿。
   （比先查 coverage 再决定快且准）

**探针实测明细**（`2PhtZK2pU4W3cCM4xThsWCn`；⚠ 这 4 颗的 `dataset_id` 被收割工具统一错标为
`analyst39+pv1`，实际分属三个集，下表的归属由表达式字段名判定）：

| alpha | 数据集 | 字段 | S | F | 2Y | TO | **CLUSTER_TEST** |
|---|---|---|---:|---:|---:|---:|---:|
| `O08rzvWJ` | `analyst7` | `est_12m_eps_median` | 0.17 | 0.06 | −0.87 | **0.0092** | **+0.29** |
| `rKe5Gm01` | `analyst39` | `anl39_qtotd2eq`（本季杠杆） | 0.07 | 0.02 | 0.05 | **0.0172** | **+0.38** |
| `58gQ5VGN` | `analyst39` | `anl39_roxlcxspeq`（EPS 环比） | 0.32 | 0.16 | −0.60 | **0.0206** | **+0.16** |
| `wpbYGVNl` | `analyst45` | `anl45_net_market_exposure` | −0.07 | −0.02 | −0.85 | 0.1372 | **+0.73** |

### ★★ 与 FUNDAMENTAL 的对照：同一区内两类数据的死因完全不同

| | ANALYST | FUNDAMENTAL |
|---|---|---|
| 探针 CT | **全为正**（+0.16 ~ +0.73） | **全为负**（−0.06 ~ −1.63） |
| 主闸 | **prod**（族级拥挤） | **CLUSTER_TEST**（结构性） |
| 可否用 CT 预检筛掉 | ❌ 筛不掉（CT 全正） | ✅ 一筛一个准 |

⇒★ **「CT 预检」这条SOP 只在 CT 为负的数据集上有效**，ANALYST 类不适用。

---

# 2 `analyst39` ★★ 本类最优落点（推荐下一波主攻）

**为何最优**：24 字段可穷尽 · 覆盖 0.70–0.92 · **零使用字段 0 个** · 全 MATRIX（无 VECTOR 归约负担）· user 263 未饱和。

### 2.1 字段构成：4 个财务科目 × 时间阶梯

**★ 它天然带「期限梯度」结构** —— 这是今日在 `analyst_revision_horizons` 上打出S1.68 的同一机制：

| 科目 | 当期 | TTM | 去年 | 更早 |
|---|---|---|---|---|
| **EPS（含特别项）** | `qepsinclxo` 本季 | `ttmepsincx` | `aepsinclxo` 最近财年 | `xlcxspemtp` 上一 TTM |
| **EPS（不含特别项）** | `roxlcxspeq` 本季 | `xlcxspemtt` | `roxlcxspea` 最近财年 | — |
| **账面价值/股** | `qtanbvps` / `spvbq` 本季 | — | `atanbvps` / `spvba` 最近财年 | — |
| **杠杆（负债/权益）** | ★`qtotd2eq` 本季 | — | ★`qtotd2eq2` 去年同期 | ★`rasv2_atotd2eq` 最近财年 |
| **毛利率** | `qgrosmgn` 本季 | `ttmgrosmgn` | `agrosmgn` / `agrosmgn2` | `grosmgn5yr` 5年均 |
| **EPS 变化率** | `ghcspea` 同比 | `ghcspemtt` 环比 TTM | `rygnhcspe` 去年同期 | `epschngin` 上季 |

⇒★★ **杠杆三阶梯最完整**（`qtotd2eq` / `qtotd2eq2` / `rasv2_atotd2eq`），
`qtotd2eq` 已有 122 用户 / 175 alpha（最热），而 `rasv2_atotd2eq` **仅 3 用户 / 3 alpha**（最冷）
⇒ **「杠杆变化」而非「杠杆水平」是本集的白空间**。

### 2.2 拥挤度分层（避免扫万人坑）

| 字段 | user/alpha | 判读 |
|---|---|---|
| ★`anl39_qtotd2eq` | **122 / 175** | ❌ 万人坑，必撞 prod |
| `anl39_qtanbvps` / `spvbq` | 56/66 · 28/34 | ⚠ 中等 |
| `anl39_roxlcxspeq` / `ttmepsincx` | 26/34 · 29/31 | ✅ 可用 |
| ★★`anl39_rasv2_atotd2eq` | **3 / 3** | ★★ **最冷 ⇒ 首选** |
| ★`anl39_qtotd2eq2` | 5 / 6 | ★ 次冷（去年同期杠杆） |
| `anl39_epschngin` | 3 / 3 | ★ 冷（上季 EPS 变化） |

⇒ ★ **同一科目的「不同时间阶梯」userCount 差 40 倍** ⇒ 冷字段是白空间。

---

# 3 逐个数据集判读

## 3.1 `analyst7`（1111 字段 / user 671 / alpha 3073）⚠ 今日已测

- **命名**：`est_12m_<指标>_<统计>` / `est_q_<季度>_<统计>`。指标 ∈ 16 种（dps/sal/roa/opr/ebi/…），
  统计 ∈ {mean, median, high, low, std, num, num_28d, raised_1wk, lowered_1wk, *_4wks_ago, *_3mth_ago, …}。
- **今日实测最佳**：`akxLxjVv` **S1.97 / F1.29 / 2Y1.71 / sub1.06** —— 四项全部接近过线，
  **是本区今日最接近可提交的 alpha**（但 prod 未测）。
- ⚠ **coverage 全部精确 0.5 且实测 TO仅 0.0092** ⇒ 截面极窄，
  **S 高可能来自少数持仓的集中效应**，需读 `long_count` 确认。
- ❌ 拥挤度极高（alpha 3073），做笛卡尔积必撞 prod。

## 3.2 `analyst_factor_signals`（108 字段 / user 32）⚠ 今日已挖（130 条）

- **命名**：`<科目>_<机制>`，科目 ∈ {eps, netprofit, revenue}，机制 7 类。
- **今日实测**：S1.53（`Vk0GoLk8`）/ S1.73（`YPMvkvd6`），**全部撞 prod 0.75–0.85**。
- **★ 关键结构发现**：`eps_y1_estimate_change_3mo`（3 个月共识变化，cover 0.931）是**唯一活字段**；
  同族 8 个 `*_estimate_change_*` 里只有它成立 ⇒ **兄弟字段不迁移**。
- ✅ **大量字段 userCount=0**（本类里零使用比例最高的高覆盖集）：
  `revenue_y1_estimate_skewness`(0)、`netprofit_y1_cagr_4yr`(0)、`eps_y2_estimate_coeff_var`(0) 等。

## 3.3 `analyst9`（111 字段 / user 47）✅ 今日测过

- **命名**：`consensusv2span*`(34) + `s` 版（30），**VECTOR 为主（106/111）⇒ 必须 `vec_avg`**。
- 今日最佳 S1.69 / F1.00 / 2Y1.13 / sub1.04（`58glgGZJ`）。
- ⚠ VECTOR 归约负担重（今日 wave373 实测：`vec_avg` 后接时序算子返回全零）。

## 3.4 `analyst39`（24 字段）★★ 推荐下一波主攻 → 见 §2

## 3.5 `analyst45`（61 字段 / user 147）★ CT 最高（+0.73）

- **全 VECTOR**（61/61）⇒ 必须 `vec_avg`。
- ⚠⚠ **coverage 全部 1.000 但它不是市场数据** —— 字段是**平台用户自己的 idea 组合账本**
  （`anl45_net_market_exposure` = 平台用户 alpha 的多空敞口差）。
  ⇒ **别被 1.0 误导**；且它描述的是「别人做了什么」，与市场基本面无直接因果。
-★ 但 **CT +0.73 是本类最高** ⇒ 若要用，走「跟随平台用户持仓」逻辑，
  与 EUR `analyst` 主题重合度高，**prod 风险大**。

## 3.6 `analyst_consensus`（1929 字段 / user 40 / alpha 70）★ 字段最多而竞争低

- **★ 性价比高**：user 40 但字段 1929 ⇒ **人均字段数最多**。
- **命名**：`{mean,median,max,min,stddev}_estimate_<指标>_<周期>`。
- ⚠ 全量查询超 8 万字符会报错 ⇒ 必须用 `search` 按前缀分批。
- 待测：本类字段数最多的集，可复用今日 `analyst_revision_horizons` 的「期限梯度」机制。

## 3.7 `analyst11`（445 字段）❌ 名不副实：**这是 ESG 数据集**

- 字段是 `anl11_creptcesger*` 等 ESG 指标（CRE/PT/CE/SGER =碳排放相关），
  **不是分析师预期数据** ⇒ 归类错误，**不能按 ANALYST 机制挖**。
- ★ **同一份数据双份暴露**：`anl11_` 缩写 + 可读长名 ⇒ **字段名必须先去重**，
  否则笛卡尔积会自我复制品（self 爆）。
- 94% 零使用，但零使用的原因是**无人意识到归类错误**，不等于白空间。

## 3.8 `analyst15`（1744 字段）❌ 建议跳过

-字段描述明确写「**aggregated within GICS industry grouping**」⇒ **已是行业聚合值**
  ⇒ 横截面排序后组内无差异 ⇒ 信噪比接近 0。
- ⚠ 部分字段描述有**复制粘贴错误**（`anl40_brdcount` 的描述被复制到 `est_12m_eps_lowerednum`）
  ⇒ **按 description 归类会出错**，必须逐字段看。

## 3.9 `analyst14`（121 字段 / user 157）

- 命名：`{high,low,mean,median,stddev,numofests}_<指标>`（99/121 是这6 类）。
- coverage 精确 0.500（占位值）⇒ 真实截面未测。
- ⚠ 机制高度同质（6 个统计量 × 16 指标）⇒ 笛卡尔积收益低。

## 3.10 `analyst4`（776 字段 / user 807）❌ 拥挤

- 主导族`fs_detail_estimates_*` + `_flag`/`_ft`（27）。
- 覆盖 ≈0.86（抽样），但 user 807 / alpha 3011 ⇒ **过度竞争**。

## 3.11 `analyst69`（813 字段 / user 1615 / alpha 14081）❌ 全类最挤

- 主导族 `anl69_best_*`（≈420 字段）。
- ★ **拥挤度分层极不均**：`_rating` 子族 507 用户 / 3865 alpha，
  而 `_4wk_up` 仅 11 用户 ⇒ **差 46 倍** ⇒ 只碰冷子族。
- ⚠ 即使如此，全集 alpha 14081 ⇒ prod 墙极高。

## 3.12 `analyst10`（961 字段 / user 595）❌ 拥挤

- 主导族 `*past_det_*`（≈330）+ `smart_ests`（≈120）。
- 覆盖 ≈0.95（抽样），但 user 595 / alpha 1369 ⇒ 过度竞争。

## 3.13 `analyst40`（22 字段 / user 10）❌ 覆盖过低

- **主题= 董事会变动**：`anl40_addin`(新任) / `moveout`(离任) / `netturnoverrate` / `gender*` / `*timeretirement` / `*stdevage`。
- ★ **与今日 FUNDAMENTAL 的 `fundamental1` 治理族高度重叠**
  ⇒ 该族已在 EUR 判死（S −0.38~0.47）⇒ **不必重试**。
- ⚠ 多个字段描述写着「No record before 20160729」⇒ **样本期只到 2016 年后**，IS 偏短。
- ❌ **覆盖仅 0.26–0.37**，低于 0.35 门槛。

## 3.14 `analyst_base_ref`（17 字段 / user 5）⚠ 共识基础量

- **VECTOR 为主**（共识统计 8 个 + 实际值 2 个）⇒ 须 `vec_avg`。
- ★ **经济含义清晰**：`consensus_high/low/mean/median/stddev_estimate_annual`（离散度）、
  `consensus_surprise_percentage_annual`（预期差）、`consensus_vs_actual_diff_annual`（实际 vs 预期）。
- ⚠ **VECTOR 覆盖仅 0.3158**；MATRIX 部分（`dilution_adjustment_ratio`/`last_close_price`/`number_of_issued_shares`）
  覆盖 0.968 但**是元字段**（≈ pv1 性质 ⇒ prod 高）。
-⇒ 「**预期差的离散度**」是本类唯一未被今日挖过的机制方向，值得小批探针。

## 3.15 `model52`（3 字段）/ `analyst81`（5 字段）❌ 字段太少

- `model52`：`cr_*` 3 字段，覆盖中位 0.199 ⇒ 不可用。
- `analyst81`：`anl81_*` 5 字段，覆盖中位 0.232 ⇒ 不可用。
- ★ 两者值评分 5.0（最高档）但**覆盖否决** ⇒ **值评分高 ≠ 可用**。

---

# 4 结论与下一步

## 4.1 优先级排序

| 优先级 | 数据集 | 理由 | 建议动作 |
|---|---|---|---|
| ★★★ **1** | **`analyst39`** | 24 字段可穷尽 · 零使用 0 · **天然期限梯度** · 冷字段多 | **下一波主攻**（先 8 条探针测 CT 与 S） |
| ★★ 2 | `analyst_consensus` | 1929 字段 / user 仅 40 ⇒ 人均空间最大 | 按 `search` 分批，先测 `*_estimate_change_*` |
| ★★ 3 | `analyst_base_ref` | 「预期差离散度」是未测机制 | 8 条探针（VECTOR 须 `vec_avg`） |
| ★ 4 | `analyst7` 冷子族 | 今日 S1.97 四项接近，**但需先读 long_count** | 先确认截面宽度再决定 |
| ❌ 跳过 | `analyst15` / `analyst11` / `analyst4` / `analyst69` / `analyst10` | GICS 聚合值 / 实为 ESG / 拥挤 | — |
| ❌ 跳过 | `analyst40` / `model52` / `analyst81` | 覆盖过低或治理族已判死 | — |

## 4.2 ★ 三条本轮新增的纪律

1. **★ `coverage` 不可信**（「精确 0.5 / 1.0」是占位值）⇒ **S0 体检必须派 1 条仿真看 TO**，
   不能只查 coverage。这推翻了「覆盖 ≥0.35」门槛在本区的可用性。
2. **★ 「按 category 选集」会漏** —— 今日主力集 `analyst_revision_horizons` 不在
   `category=analyst` 的 16 个里⇒ 选集时必须 `get_datasets` 全量列举，不只按 category 过滤。
3. **★ CT 预检 SOP 只在 CT 为负的数据集上有效** —— ANALYST 类 CT 全为正，
   该 SOP 在此category 筛不出任何东西 ⇒ **需换判据（本类应先测 prod 拥挤度）**。

## 4.3 待续方向（本轮未做完）

- **`analyst39` 的期限梯度**：杠杆三阶梯（`qtotd2eq` / `qtotd2eq2` / `rasv2_atotd2eq`，
  user 122/5/3）⇒ 「杠杆**变化**」是 `analyst39` 的白空间，与今日在
  `analyst_revision_horizons` 上撞 prod 的「修正**水平**」是**不同机制**。
- **`analyst45` 的 CT +0.73** 是本类最高 ⇒ 若 CT 能被推到 1.58，是绕过 ANALYST prod 墙的可能路径
  （今日 FUNDAMENTAL 正是卡在 CT）。
- **`analyst7` 的 `akxLxjVv`（S1.97）** 需补 prod 与 long_count 才知道是否真可用。

---

铁律：本轮**零提交、零入队**，`ALLOW_ALPHA_SUBMIT` 未触碰；全部仅仿真。