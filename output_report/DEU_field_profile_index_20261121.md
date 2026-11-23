# DEU 字段画像存档索引（2026-11-21）

> 归档路径与命名规则见 §1；本轮新增/增量见 §3；全量清单见 §2。

## 1. 归档路径与命名规则

```
tracking/DEU/reference/datasets/<dataset_id>.md
```

| 项 | 规则 |
|---|---|
| **路径** | `tracking/DEU/reference/datasets/` —— DEU 战役的规范字段画像目录（区域级，不是仓库根 `docs/`） |
| **命名** | `<dataset_id>.md`，小写数据集名，与平台 `/data-sets` 的 `id` **逐字一致**（`sentiment27.md` ↔ `sentiment27`）。不写中文别名、不加日期后缀 |
| **必含章节** | `## 字段全表`（逐字段真实 id + 类型 + coverage + userCount + alphaCount + dateCreated + 描述）＋ `## 实测`（逐字段带数字读数的实测行） |
| **完整性硬闸** | `python tools/gates/field_profile_completeness_gate.py --profile tracking/DEU/reference/datasets/<dataset_id>.md` ⇒ **exit 0** 才可作为选区 / 建族依据。三判据：① 全表逐字段真实 id、无通配占位（`*_active` / 「8 个同构孪生」等一律不接受）；② 全表每个字段在档案内有带数字读数的实测行；③ 实测行数 == 全表行数 |
| **零配额静态画像** | `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=<id>, filter_sharpe=false)` 全量拉取；分母对账用 `get_datasets(category=…)` 的 `fieldCount` |
| **实测形态** | 每个字段**一条独立臂**，统一最小形态 + 生产档回测设置；读数取 `get_alpha_details` / `backtest_results` 实读 |

## 2. DEU 字段画像全量清单

| 数据集 | 档案 | 字段数 | 完整性闸 | 状态 |
|---|---|---:|---|---|
| `sentiment27` | [sentiment27.md](../../../tracking/DEU/reference/datasets/sentiment27.md) | 18 | **PASS** | 2026-11-19 建档（六法 66 臂）；**2026-11-21 追加 §8**（残差化族增量读数 + 克隆终判） |
| `sentiment7` | [sentiment7.md](../../../tracking/DEU/reference/datasets/sentiment7.md) | 3 | **PASS** | 2026-11-18 建档 |
| `sentiment33` | [sentiment33.md](../../../tracking/DEU/reference/datasets/sentiment33.md) | 255 | **PASS** | 2026-11-18 建档 |
| `insider_agg_matrix` | [insider_agg_matrix.md](../../../tracking/DEU/reference/datasets/insider_agg_matrix.md) | 34 | **PASS** | **2026-11-21 新建**（全字段 34/34 单发体检） |
| `risk71` | [risk71.md](../../../tracking/DEU/reference/datasets/risk71.md) | 10 | 待补（2/10 已实测） | **2026-11-23 新建**：★★★ 纠正「cov=0.0 ⇒ 无数据」——10 字段全报 cov 0.0 但探针证明有数据；`residualized_return_top2500` 裸 zscore **S −1.12 / TO 90.5%**（强反转，换手是硬敌）；10 字段只 3 条机制 |

**未建档的数据集及原因**（不是遗漏，是有据不建）：

| 数据集 | 原因 |
|---|---|
| `institutions25` / `institutions6` / `fund_holdings_panel` / `institutions4` / `institutions1` | **数据集级/族级判死**（本轮复核确认，见战役报告 §5.4）。判死集不做「选区级」画像；其历史读数在 `tracking/DEU/s1_institutions25_wave1_template_pool.md` 与 `tracking/DEU/reference/dataset_landscape_2026-11-03.md` |
| `insiders1` | 既有档案在 `tracking/DEU/regular_tower/FIELD_insiders1_20261115.md` / `_20261116.md` / `_20261117.md`（波次制，非 `reference/datasets/` 制）。**本轮未把它作为选区**（单集天花板 1.30–1.37 < 1.58，且 2018 年起才有有效样本） |
| `pv20` / `intraday_pv_feats` / `news29` | 本轮只做**定向探测**（IBES 面 2 臂、skew 兄弟字段 2 臂、news29 未派发），**未作选区** ⇒ 不建「选区级」档案；681/585 字段的逐字段探测规模与本轮预算不匹配 |
| `news17` / `news18` / `news20` / `news38` / `news50` / `news104` | 数据集级判死或已被前轮战役逐字段覆盖（见战役报告 §5.4） |
| `risk60` / `risk68` / `risk71` / `risk72` / `risk88` | 数据集级判死 |
| `earnings6` / `earnings_sent_matrix` / `macro27` / `option1` / `socialmedia12` / `imbalance5` | **字段覆盖率全 0.0 ⇒ 数据层排除**（151 个字段无一条有数据），不开波、不建档 |

## 3. 本轮（2026-11-21）新增与增量

| 档案 | 动作 | 内容 |
|---|---|---|
| [insider_agg_matrix.md](../../../tracking/DEU/reference/datasets/insider_agg_matrix.md) | **新建** | 34 字段全表 + **34/34 逐字段实测**（生产档单发体检）；5 条读数结论：① 买正卖负复现（买 +0.15~+0.28 / 卖 −0.28~−0.02）；② 族内分档符号翻转（SV1/SV2 正 vs SV3/SV4 强负）；③ `directional_significant_value_1..4` **平台 ERROR 毒字段**（`"No alpha_id in sim response"`，论坛 `43837157183895` 在 DEU 复现且更彻底）；④ **覆盖是强度物理上限**（LC 37–69 / 500）；⑤ `directional_indicator` 单腿为负但多腿可用 |
| [sentiment27.md](../../../tracking/DEU/reference/datasets/sentiment27.md) | **追加 §8** | 10 个臂的逐字段读数 + 2 条负杠杆（`snt7_views` ΔS −1.11；`ts_quantile` 窗 504 Δ2Y −0.37）+ **族级克隆终判**（6 颗 RA-clean 变体互相关 0.77–0.999、对已提交件 `bl6OWZ2M` 0.932–0.976 ⇒ 全撞 self-corr）+ 对原档案 4 条结论的修正表 |

## 4. 本轮为画像档新增的两条平台级纪律

1. **静默失败字段**：平台对某些字段**不报错、不回滚、只是不产生 alpha**（子任务 status = COMPLETE，但 `"No alpha_id in sim response"`）。
   ⇒ 只盯 `batch_status`（`all_terminal: true` + `child_count: 2`）会把它误读成「成功但没读数」；**必须用 `harvest_multisim_alphas` / `lookINTO_SimError_message` 才能看到该错误**。
2. **VECTOR 字段的 `vec_*` 聚合是搜索维度**：同一 VECTOR 字段用 `vec_avg` / `vec_max` 读数不同 ⇒ 画像档的实测形态必须写明用的哪个聚合算子。

## 5. 相关闸与索引

| 工具 | 用途 |
|---|---|
| `tools/gates/field_profile_completeness_gate.py` | 字段全表 vs 实测覆盖（管「集内字段是否探全」） |
| `tools/gates/audit_dataset_coverage.py` | 数据集是否验过（管「数据集是否探过」）—— 两者分工见 AGENTS.md §4 |
| `tools/fields/profile_dataset_fields.py` | `get_datafields` 落盘 JSON → 画像报告（静态部分） |
| `mcp__wq-brain-http__get_datafields` | 平台字段目录（全量拉取时必须 `filter_sharpe=false`） |
| `mcp__wq-brain-http__get_datasets` | 数据集目录（分母对账；**不带 `category` 会截断**，必须按 category 逐类枚举或用 dataset 级 `fieldCount`） |
