# USA / D1 `chart_return_model` 字段画像与机制台账（2026-10-23）

> **定位**：USA 未点亮塔补挖第 3 个数据集（`other635` 判死后接续）。
> 平台类别 **PV（×1.1，0 颗 ACTIVE ⇒ 未点亮）**，满足「已点亮塔不作主数据集」用户规则（2026-09-19 定案）。
> 数据集级事实全部来自本地台账 `data/wqb.db`（`datasets` / `fields` / `expressions`）与平台
> `validate_expressions`；标「未实测」的项不得当作已知。

## 1. 为什么选它（S0 选集理由）

`other635` 波 1 判死后，在 44 个未点亮候选中按「结构是否可能提供新机制」而非「S 上限」重排。
`chart_return_model` 同时满足：

| 判据 | 事实 | 为什么重要 |
|---|---|---|
| 塔位 | `datasets.category = PV`，该塔 0 颗 ACTIVE（`campaign_intel pyramid --region USA --delay 1`） | 用户硬规则：已亮塔（ANALYST / MODEL）只作组腿 |
| 容量 | 248 字段、覆盖 **1.0**、MATRIX、`value_score = 5` | 满覆盖、无稀疏事件问题，不需要 `ts_backfill` 兜底即可横截面比较 |
| 结构 | **20 个 `predicted_*forward_return` 连续预测** = 6 个期限 × 14 个训练配置；另有 116 个日内快照字段与 112 个分桶/概率/分位字段 | 是 ai_equity「平行模型预测同一目标」结构的**正版宿主** |
| 拥挤度 | 数据集 aC **66**；20 个回归字段里 **17 个 aC = 0**；本地台账 `expressions` 仅 7 条 `backtested`、**0 条 ACTIVE** | 预测类字段在生产池中几乎未被使用 |

⚠ **aC 低不保证 prod 低**（`risk60` 反例，见 `_usa-risk60-field-profile-20261023.md` §7.2）。
本数据集的价值主张在**结构**：同一目标上的多配置预测，天然可造「模型分歧」，而分歧构造在 USA 生产池中稀有
（ai_equity 实测 prod 0.64–0.69）。

## 2. 字段画像总表（248 字段，按语义族）

| 族 | 数量 | 代表字段 | 语义 / 用法 |
|---|---:|---|---|
| **回归预测收益** | **20** | `predicted_forward_return`（1 interval ahead，未截断）、`_t100`、`_g2`、`_g6r1`、`_r10`、`_r20`、`_w2r1`、`_bidaskr10`、`_bidaskr5im`、`_g2r5`、`_r5`、`_r10_2`、`_forward_return_2`、`_3`、`_flr1` | 连续预测，可正可负；期限族 `one/three/five/ten/twenty_day_forward_return` 是 **1/3/5/10/20 交易日**预测 |
| log-softmax 桶概率 | 26 | `likelihood_fifth_return_bucket_bidaskr10` | 预测收益落在第 k 个分位桶的**对数**概率，跨桶可做「看多质量 − 看空质量」 |
| 分位组概率 | 34 | `probability_second_quantile_group_g6r1`、`probability_fifth_return_bucket_t100` | 同上，按训练配置分组 |
| 桶 one-hot 标签 | 24 | `predicted_fifth_return_bucket_g2` | 0/1 硬标签，信息量低于概率，只在需要离散事件时用 |
| 分位组标签 | 20 | `predicted_fifth_quantile_group_r10` | 0-based 组号，序数型 |
| 分位序号 | 8 | `predicted_fifth_return_quantile`、`_2` | 0-based 分位号，**序数**（可当粗粒度分数，但会丢桶内差异） |
| **日内快照** | **116** | `first_bid_price_int60`、`third_ask_price_int120`、`second_trade_volume_top_book` | 当日第 1–6 个 interval 的价 / 量 / 盘口快照，覆盖 `int60`（6 段）/ `int120`（3 段）/ `top_book` / `agg` 四种采样模块 |

**期限族的真实含义**：基字段与 14 个配置变体预测的是 **next interval（1-bar ahead）**；
`predicted_{one,three,five,ten,twenty}_day_forward_return` 才是 **交易日尺度**。
`_r10`/`_r20` 的「r」指 **10/20 intervals** 的前瞻窗口（平台原文 "next 10 intervals"），
不是 10/20 个交易日 —— 这是本数据集最容易读错的一处口径。

## 3. 数据类型、更新频率、分布与可用性

- **全 MATRIX**：可直接进 `ts_*` / `group_*` / `rank`，无 VECTOR 聚合前置（与 `other635` 相反）。
- **更新频率**：D1 快照；预测由日内 interval 模型生成，`delay = 1` 下可执行的最早时点是次日。
- **分布**：回归预测「unbounded continuous」，`_w2r1` 平台明示 **should be winsorized before use**；
  `_t100` 平台标注为 **recommended** 版本。概率族是 log-softmax（负值，越大越可能）。
- **可用性**：USA / TOP3000 / D1 字段存在性实测通过（`validate_expressions` → `unknown_fields = []`；
  `_bidaskr10` 一次 6 轮重试失败但被判为「lookup incomplete」，未列为 unknown，回测实测有值）。
- **历史**：本地台账 7 条 `backtested` + 133 条 `dropped`，**0 条 ACTIVE** —— 整个数据集在 USA 未产出过提交级 alpha。

## 4. 机制假设与波 1 预登记（发批前写定，不得事后改判据）

结构上有三条互不重叠的机制：

| 假设 | 机制 | 代表构造 |
|---|---|---|
| **H-lvl 水平** | 模型预测的**未来收益水平**本身即信号（多头高预测、空头低预测） | `ts_backfill(predicted_*, 66)`，正反向各一条 |
| **H-hzn 期限分歧** | 短期限与长期限预测之差 = 模型的**期限结构**（近端动量 vs 远端均值回归） | `5d − 1d` |
| **H-cfg 配置分歧** | 同一目标的 14 个训练配置（含成本 / 分组 / 秩变换 / 窗口）预测不一致 ⇒ 不确定性 | `gross − bidaskr10`、`g2 − g6r1`、`r10 − r20`、`base − w2r1` |

**预登记判据**：任一臂 RA 全过（`S ≥ 1.58`、`F ≥ 1.0`、`SUB/S ≥ 0.435`、2Y 达标）⇒ 立即做 prod 探针，
不先做同族扩展（`risk60` 教训：16 臂全过 RA 才测 prod，白烧一轮）。

**设置**：MARKET / TOP3000 / decay 8 / truncation 0.08 / `nanHandling=ON` / 2014-01-01..2023-12-31
（`tracking/USA/runs/usa_crm_w1_spec.json`）。

## 5. 波 1 实测（10 臂，multisim `4alaRUbNk54auOyUZ12q7v`）

| # | 构造 | alpha | S | F | TO | RET | 2Y | SUB | SUB/S | RN | RA 失败 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `ts_backfill(predicted_forward_return, 66)` 基字段 | `j2ePEEp5` | 0.69 | 0.19 | 52.74% | 4.0% | 0.84 | 0.17 | 0.246 | 0.93 | S/F/SUB |
| 2 | 同上取反 | `9qEdvve9` | −0.69 | — | — | — | — | — | — | — | — |
| 3 | `_t100`（平台推荐版） | `QPYNJJxW` | **1.22** | 0.37 | 57.12% | 5.1% | **−0.01** | 0.29 | 0.238 | 1.62 | S/F/SUB/2Y |
| 4 | `predicted_twenty_day_forward_return` | `58jAbbmX` | 0.90 | 0.40 | 36.15% | 7.0% | **1.27** | **0.59** | **0.656** | 0.91 | S/F/2Y |
| 5 | `base − bidaskr10`（含成本分歧） | `leM5qqmO` | −0.34 | — | — | — | — | — | — | — | — |
| 6 | 同上取反 | `A1QrWWAw` | 0.34 | — | — | — | — | — | — | — | — |
| 7 | `g2 − g6r1` | `Vkdm99W5` | 0.30 | — | — | — | — | — | — | — | — |
| 8 | `r10 − r20` | `YPxErrR6` | −0.49 | — | — | — | — | — | — | — | — |
| 9 | `5d − 1d`（期限分歧） | `2rjX003Z` | 0.71 | **0.52** | **9.76%** | 6.8% | 1.13 | 0.27 | 0.380 | 0.25 | S/F/SUB/2Y |
| 10 | `base − w2r1` | `d5K3XXNj` | −0.20 | — | — | — | — | — | — | — | — |

（`—` = 该臂远低于判据，未逐项抄录；完整原始行见 multisim 与 `tracking/USA/runs/usa_crm_w1.txt` 的注释头。）

## 6. 裁决与归因（停投）

**预登记判据无一臂满足**（最好 S 1.22，且该臂 2Y = −0.01、SUB/S 0.238、RN 1.62）。逐条归因：

1. **期限错配是主因**：14 个配置变体与基字段预测的是 **next interval（1-bar）**，而 D1 最早次日成交。
   信号主体在可交易时点之前已衰减，于是只剩高换手（52–57%）与近零的 2Y 收益 —— `_t100` 臂
   S 1.22 看起来最高，2Y 却是 **−0.01**，正是「全样本靠早期几年撑起来」的形状。
2. **可执行的日尺度预测强度不足**：`二十日` 臂是本波唯一 2Y > 1（1.27）且 SUB/S > 0.6（0.656）的构造，
   方向正确、衰减比健康，但 S 仅 **0.90**，距 1.58 差 1.75 倍；`5d−1d` 臂换手只有 9.76%（F 0.52 为全波最高），
   但 SUB/S 0.380 说明横截面区分度不够。
3. **配置分歧轴信息量为零**：`gross−bidask`、`g2−g6r1`、`r10−r20`、`base−w2r1` 四组双向 |S| 全部落在
   0.20–0.49，且正负无序 —— 与 `other635` 的分歧轴失败**同构**。
4. **可复用判据（写进选集纪律）**：**分歧腿必须来自「信息源不同」的模型**。ai_equity 的两条腿是两套
   独立模型的预测（分歧 = 真实不确定性）；这里是**同一模型、同一训练数据、只改正则/分组/窗口**的 14 个版本，
   差异主要是**抽样噪声**，差分把公共信号减掉、只剩噪声 ⇒ 无方向信息。
   推论：**同模型多配置字段的 aC 低 ≠ 未被挖掘，而是本身不含新信息**。
5. **未投入的轴与理由**（避免下一轮重复）：116 个日内快照字段（第 1–6 个 interval 的价/量/盘口）本质是
   分钟级微观结构，在 D1 delay 下与第 1 条同病；112 个分桶/概率字段的默认口径也是 1-interval，
   与主因同源。**若将来有人要复用本数据集，唯一值得试的是「20 日预测 + 更慢壳层」的强度提升**，
   而不是换字段。

裁决：`chart_return_model` **停投**。PV 塔仍 0 颗 ACTIVE，未被消耗。

## 7. 档案索引

| 内容 | 位置 |
|---|---|
| 波 1 表达式与注释头 | `tracking/USA/runs/usa_crm_w1.txt` |
| 波 1 设置 | `tracking/USA/runs/usa_crm_w1_spec.json` |
| 波 1 结果（平台） | multisim `4alaRUbNk54auOyUZ12q7v` |
| 交付报告对应节 | `output_report/USA_regular_alpha_delivery_20261021.md` §9.3 |
| 同轮前序画像 | `_usa-risk60-field-profile-20261023.md`、`_usa-other635-field-profile-20261023.md` |
