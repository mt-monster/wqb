# DEU / TOP500 / D1 — insider_agg_matrix 字段全画像

> 生成：2026-11-21｜来源：`mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=insider_agg_matrix, filter_sharpe=false)` 全量实读
> 取数结果：`count=34`、`platform_count=34`、`complete=true`、`pages_fetched=1`、`returned=34` ⇒ **未分片、无缺口**，去重后 34 = `platform_count`。
> 分母对账：`platform_count=34` ＝ 本文「字段全表」34 行 ＝ `get_datasets(DEU/TOP500/D1, category=insiders)` 里 `insider_agg_matrix` 的 `fieldCount=34`，三处一致。
> 数据集级（`get_datasets`，实读）：name **Smart Insider Transaction Aggregates**｜category insiders｜coverage **0.5617**｜userCount **103**｜alphaCount **196**｜valueScore **4.0**｜pyramidMultiplier **1.6**
> ⚠ **语义定位**：本集是**内部人交易的结构化聚合矩阵**（`insider_agg_matrix`），**不是**「 insider 原始逐笔申报」（那是 `insiders1`）——两者是两个**独立数据集**，跨集使用即 2 数据集（**非 ATOM**）。
> ⚠ **本轮是「全字段 34/34 实测探测」**：每个字段一条独立单发体检臂（生产档），逐条读 `S / F / 2Y / longCount / shortCount`。**无抽样、无「代表字段」**（AGENTS §4 硬约束）。

## 字段全表

|字段 id|type|coverage|userCount|alphaCount|dateCreated|pyramidMultiplier|描述|
|---|---|---:|---:|---:|---:|---:|---|
|`avg_buy_shares`|MATRIX|0.5344|9|13|2026-07-01|1.6|全体董事买入股数的均值|
|`avg_secondary_buy_shares`|MATRIX|0.5344|20|30|2026-07-01|1.6|董事（非高管）直接买入股数均值|
|`avg_secondary_sell_shares`|MATRIX|0.5344|8|9|2026-07-01|1.6|董事（非高管）直接卖出股数均值|
|`avg_secondary_top_buy_shares`|MATRIX|0.5344|4|5|2026-07-01|1.6|高管（非董事）直接买入股数均值|
|`avg_secondary_top_sell_shares`|MATRIX|0.5344|3|3|2026-07-01|1.6|高管（非董事）直接卖出股数均值|
|`avg_sell_shares`|MATRIX|0.5344|6|8|2026-07-01|1.6|全体董事卖出股数的均值|
|`avg_top_buy_shares`|MATRIX|0.5344|5|5|2026-07-01|1.6|全体高管买入股数的均值|
|`avg_top_sell_shares`|MATRIX|0.5344|3|3|2026-07-01|1.6|全体高管卖出股数的均值|
|`directional_indicator`|MATRIX|1.0|36|52|2026-07-01|1.6|内部人活动整体方向/偏向指标|
|`directional_indicator_2`|MATRIX|1.0|15|23|2026-07-01|1.6|增强型内部人活动方向/偏向指标|
|`directional_significant_value_1`|MATRIX|0.5342|0|0|2026-07-01|1.6|带方向的重大内部人交易中的最高值（**本轮实测 ERROR**）|
|`directional_significant_value_2`|MATRIX|0.5342|0|0|2026-07-01|1.6|带方向的重大内部人交易中的次高值（**本轮实测 ERROR**）|
|`directional_significant_value_3`|MATRIX|0.5342|0|0|2026-07-01|1.6|带方向的重大内部人交易中的第三高值（**本轮实测 ERROR**）|
|`directional_significant_value_4`|MATRIX|0.5342|0|0|2026-07-01|1.6|带方向的重大内部人交易中的第四高值（**本轮实测 ERROR**）|
|`significant_value_1`|MATRIX|0.5342|13|16|2026-07-01|1.6|最重大内部人交易的金额|
|`significant_value_2`|MATRIX|0.5342|2|3|2026-07-01|1.6|第二大重要内部人交易的金额|
|`significant_value_3`|MATRIX|0.5342|3|3|2026-07-01|1.6|第三大重要内部人交易的金额|
|`significant_value_4`|MATRIX|0.5342|5|5|2026-07-01|1.6|第四大重要内部人交易的金额|
|`top_directional_significant_value_1`|MATRIX|0.5342|3|4|2026-07-01|1.6|高管带方向重大交易中的最高值|
|`top_directional_significant_value_2`|MATRIX|0.5342|1|1|2026-07-01|1.6|高管带方向重大交易中的次高值|
|`top_directional_significant_value_3`|MATRIX|0.5342|2|2|2026-07-01|1.6|高管带方向重大交易中的第三高值|
|`top_directional_significant_value_4`|MATRIX|0.5342|0|0|2026-07-01|1.6|高管带方向重大交易中的第四高值|
|`top_significant_value_1`|MATRIX|0.5342|5|5|2026-07-01|1.6|高管重大交易中的最高值|
|`top_significant_value_2`|MATRIX|0.5342|1|1|2026-07-01|1.6|高管重大交易中的次高值|
|`top_significant_value_3`|MATRIX|0.5342|2|3|2026-07-01|1.6|高管重大交易中的第三高值|
|`top_significant_value_4`|MATRIX|0.5342|5|5|2026-07-01|1.6|高管重大交易中的第四高值|
|`total_buy_shares`|MATRIX|0.5344|9|10|2026-07-01|1.6|全体董事买入股数之和|
|`total_secondary_buy_shares`|MATRIX|0.5344|10|17|2026-07-01|1.6|董事直接买入股数之和|
|`total_secondary_sell_shares`|MATRIX|0.5344|5|8|2026-07-01|1.6|董事直接卖出股数之和|
|`total_secondary_top_buy_shares`|MATRIX|0.5344|6|9|2026-07-01|1.6|高管直接买入股数之和|
|`total_secondary_top_sell_shares`|MATRIX|0.5344|4|4|2026-07-01|1.6|高管直接卖出股数之和|
|`total_sell_shares`|MATRIX|0.5344|4|4|2026-07-01|1.6|全体董事卖出股数之和|
|`total_top_buy_shares`|MATRIX|0.5344|10|12|2026-07-01|1.6|全体高管买入股数之和|
|`total_top_sell_shares`|MATRIX|0.5344|4|4|2026-07-01|1.6|全体高管卖出股数之和|

行数核对：34 行 = `platform_count` 34，缺口 **0**。

## 实测（全字段 34/34，生产档单发体检）

口径：DEU / TOP500 / D1；`decay=4` / `neutralization=SUBINDUSTRY` / `truncation=0.08` / `unitHandling=VERIFY` / `nanHandling=OFF` / `pasteurization=ON` / `maxTrade=OFF` / FASTEXPR；IS 2014-01-01→2023-12-31。
体检形态（每字段一条臂，统一形态）：`group_rank(ts_mean(<F>, 66), sector)`。读数 = `S / F / 2Y / TO / longCount / shortCount`（平台 `get_alpha_details` 与 `backtest_results` 实读）。

|字段|alpha|S|F|2Y|TO|LC|SC|
|---|---|---:|---:|---:|---:|---:|---:|
|`avg_buy_shares`|`3q01O7vO`|0.27|0.11|0.31|0.065|54|65|
|`avg_secondary_buy_shares`|`e7aNPOMp`|0.28|0.11|0.24|0.0661|51|64|
|`avg_secondary_sell_shares`|`9ql83r6e`|-0.28|-0.11|0.38|0.0657|60|65|
|`avg_secondary_top_buy_shares`|`blaJgqWR`|0.16|0.05|-0.10|0.0666|39|62|
|`avg_secondary_top_sell_shares`|`RRe9wWOb`|-0.17|-0.06|0.43|0.065|58|62|
|`avg_sell_shares`|`58JrdWmX`|-0.15|-0.04|0.30|0.0656|61|66|
|`avg_top_buy_shares`|`gJaX5dOl`|0.24|0.09|-0.16|0.0662|42|63|
|`avg_top_sell_shares`|`A1xe5mME`|-0.10|-0.02|0.40|0.0656|58|63|
|`directional_indicator`|`Wjl32QEN`|-0.11|-0.03|-0.26|0.1312|69|69|
|`directional_indicator_2`|`78Y3Rbk2`|-0.10|-0.02|-0.60|0.1319|69|69|
|`directional_significant_value_1`|（无 alpha）|ERROR|ERROR|ERROR|ERROR|0|0|
|`directional_significant_value_2`|（无 alpha）|ERROR|ERROR|ERROR|ERROR|0|0|
|`directional_significant_value_3`|（无 alpha）|ERROR|ERROR|ERROR|ERROR|0|0|
|`directional_significant_value_4`|（无 alpha）|ERROR|ERROR|ERROR|ERROR|0|0|
|`significant_value_1`|`omaRj15n`|0.36|0.17|0.57|0.0654|52|65|
|`significant_value_2`|`gJaXNYOg`|0.33|0.15|0.59|0.0653|52|65|
|`significant_value_3`|`MP6dvO2a`|-0.65|-0.38|-0.09|0.0634|46|63|
|`significant_value_4`|`akaem6g9`|-0.63|-0.36|0.05|0.0635|46|63|
|`top_directional_significant_value_1`|`QP0ORjPg`|0.17|0.06|0.13|0.0674|37|61|
|`top_directional_significant_value_2`|`blaJ0MGN`|0.16|0.05|0.15|0.0671|37|61|
|`top_directional_significant_value_3`|`mLadnXW1`|-0.70|-0.44|-0.13|0.0614|37|58|
|`top_directional_significant_value_4`|`58JrKvK6`|-0.69|-0.43|-0.05|0.0615|37|58|
|`top_significant_value_1`|`ZYag8LnZ`|0.30|0.13|0.11|0.0667|39|62|
|`top_significant_value_2`|`XgaV3Enb`|0.28|0.12|0.12|0.0663|39|62|
|`top_significant_value_3`|`zqdg72d8`|-0.74|-0.47|-0.20|0.0621|39|60|
|`top_significant_value_4`|`Jj8oaW3l`|-0.72|-0.46|-0.15|0.0622|39|60|
|`total_buy_shares`|`RRe9O2Mn`|0.16|0.05|0.30|0.065|54|65|
|`total_secondary_buy_shares`|`6XMZWa7E`|0.26|0.10|0.20|0.0662|51|64|
|`total_secondary_sell_shares`|`KPgv1aYj`|-0.12|-0.03|0.45|0.0661|60|65|
|`total_secondary_top_buy_shares`|`GrmXRJ0G`|0.15|0.05|-0.10|0.0665|39|62|
|`total_secondary_top_sell_shares`|`1YWO8Z8M`|-0.06|-0.01|0.50|0.0656|58|62|
|`total_sell_shares`|`XgaV3J01`|-0.03|0.00|0.34|0.0663|62|66|
|`total_top_buy_shares`|`Jj8oA9MW`|0.19|0.07|-0.17|0.0659|42|63|
|`total_top_sell_shares`|`78Y35pWb`|-0.02|0.00|0.40|0.0664|59|63|

行数核对：34 行 = 字段全表 34 行，缺口 **0**。

## 1. 读数结论（5 条）

### 1.1 ★ 买入正 / 卖出负：文献方向在 DEU **复现**，但幅度只有 0.1–0.28

| 方向 | 字段 | S 区间 |
|---|---|---|
| 买 | `avg_secondary_buy_shares` +0.28 / `avg_buy_shares` +0.27 / `avg_secondary_top_buy_shares` +0.16 / `avg_top_buy_shares` +0.24 / `total_secondary_buy_shares` +0.26 / `total_buy_shares` +0.16 / `total_secondary_top_buy_shares` +0.15 / `total_top_buy_shares` +0.19 | **+0.15 ~ +0.28** |
| 卖 | `avg_secondary_sell_shares` −0.28 / `avg_sell_shares` −0.15 / `avg_secondary_top_sell_shares` −0.17 / `avg_top_sell_shares` −0.10 / `total_secondary_sell_shares` −0.12 / `total_secondary_top_sell_shares` −0.06 / `total_sell_shares` −0.03 / `total_top_sell_shares` −0.02 | **−0.28 ~ −0.02** |

⇒ 与 JMZ(2003) / 论坛 `43152032301591`「买入类字段 S 1.56–1.59，卖出股数 0.21」**方向一致**（买强卖弱），
但**幅度差一个数量级**（EUR/美股口径 1.5+ vs DEU 0.15–0.28）⇒ **跨区不可外推效应量**（AGENTS 跨区不外推铁律再得一例）。

### 1.2 ★ 同一族内「按排名分档符号翻转」：SV1/SV2 正、SV3/SV4 强负

| 字段 | S |
|---|---:|
| `significant_value_1` / `_2`（最大/次大交易金额） | **+0.36 / +0.33** |
| `significant_value_3` / `_4`（第三/第四大交易金额） | **−0.65 / −0.63** |
| `top_significant_value_1` / `_2` | +0.30 / +0.28 |
| `top_significant_value_3` / `_4` | **−0.74 / −0.72** |
| `top_directional_significant_value_1` / `_2` | +0.17 / +0.16 |
| `top_directional_significant_value_3` / `_4` | **−0.70 / −0.69** |

⇒ **「最大单笔」与「第三/第四单笔」符号相反且强度差 2 倍**。两种解释：(a) 金额轴上有**阈值效应**（只有足够大的交易是知情交易，小额反而是例行买卖）；
(b) SV1/SV2 与 SV3/SV4 在构造上**分属买方与卖方两侧**（SV1/SV2 = 买入侧、SV3/SV4 = 卖出侧）。
⚠ **平台目录未给这 8 个字段的符号约定**，本档案**不替平台背书**；若要用，必须先做**字段级符号探针**（论坛同结论，见 §2）。
⇒ **可直接用的合成口径**（与 EUR 已交付形态同源、但换成本区读数）：`divide(ts_sum(SV1..SV4 合计), 日常净买卖股数)` **不是**本轮读数支持的方向；
本轮读数支持的是**分档取符号**（SV1/SV2 取正、SV3/SV4 取负）。

### 1.3 ★ `directional_significant_value_1..4` = **平台 ERROR 字段**（毒字段，DEU 复现）

- 4 个字段各派 1 臂，**平台不产生 alpha**（无 alpha id、无 longCount/shortCount）⇒ 记 ERROR / lc=sc=0。
- **平台侧确切报错**（本轮 `create_multi_simulation` 回读，multisim `3eJ8lfcnd5aIcgISGuXoSHP` / `1KG8Ng6SR4sC9eFDcmJfqPt` / `2udKoR3qF4qYahjKEmrxyhW`）：子任务 status = COMPLETE，但 **`"error": "No alpha_id in sim response"`**、`error_count: 2` ⇒ **平台静默失败**（批次不报错、不回滚、只是不产生 alpha）。
- **与论坛 `43837157183895`（LW67640）的「毒字段」记录一致**：「`directional_significant_value_1` = 毒字段（一批 8 条表达式全 FAIL 且无任何错误信息，二分法才定位到它）」。
- ⚠ **DEU 侧给得更强**：不是「该字段弱」，而是 **4/4 同族字段全部 ERROR** ⇒ **整族排除**，不要在派发前浪费批次（一条臂即废一条批次）。
- ⚠ **工具侧坑**：这类静默失败**不会**在 `batch_status` 里报 `errors`，而是 `all_terminal: true` + `child_count: 2`；只有 `harvest_multisim_alphas` / `lookINTO_SimError_message` 才吐出 `"No alpha_id in sim response"`。**只盯 `batch_status` 会把它误读成「成功但没读数」**。
- 对比：`top_directional_significant_value_1..4` **全部正常**（ac 0–2 但都有 alpha）⇒ **「带方向的重大交易」只在高管子族上可用**。

### 1.4 ★ 覆盖是本集强度的**物理上限**：longCount / shortCount 仅 **37–69 / 500**

- 34 个字段的持仓宽度实测 **LC 37–69、SC 58–69**（对比：`sentiment27` 同档 LC 126–157 / SC 124–159）。
- 即 **横截面上只有约 8–14% 的 TOP500 标的有内部人交易数据**，且买卖两侧宽度接近 ⇒ 截面样本是本集一切统计强度的约束。
- 这解释了 DEU 既有档案「`insider_agg_matrix` 单集上限 0.92–0.93」的根因：**不是模板选错，是可交易宽度只有 1/8**。
- ⚠ **「宽度塌缩入场」铁律**（`_effective-levers.md` 反模式表）：`lc/sc < 50` 或 0/0 的集不开波。本集 `avg_secondary_top_*` / `top_*_significant_value_*` 的 LC 37–42 **已在塌缩边缘** ⇒ 这几族即使信号方向正确也难成可交付件。

### 1.5 `directional_indicator` / `_2` 单独用**方向为负**（与论坛「零持仓/毒字段」告警部分冲突）

- `directional_indicator` S **−0.11**（TO 0.1312，LC/SC 69/69）、`directional_indicator_2` S **−0.10**（2Y −0.60）。
- 论坛 `43837157183895` 记其在 EUR 为「零持仓（zscore 版 0 多 0 空）」；**DEU 侧不是零持仓（69/69）但单独用方向为负**。
- DEU 已提交件 `Vk65zLzG`（S 1.79 ACTIVE）用的就是 `directional_indicator` **作多腿之一** ⇒ **单腿为负 ≠ 家族为死**；该字段在多腿结构里可用。

## 2. 论坛 / 论文取证（配套）

| 来源 | 与本集直接相关的结论 |
|---|---|
| 论坛 `43837157183895`（LW67640） | EUR 已交付形态：`top_directional_significant_value_1`（1260d）÷ `total_top_buy_shares − total_top_sell_shares`（84d）⇒ S 1.89 / prod 0.5322 / self 0.1268。**窗口悬崖**：分母 84 → S 1.77、63 → 0.77、42 → 0.85。**毒字段**：`directional_significant_value_1`。股数族单独 63 日 S 1.90；金额族单独最高 S 0.49 且 2Y 常年为负。**两族相加＝零** |
| 论坛 `43152032301591` | 买入类字段 S 1.56–1.59 vs 卖出股数 0.21；异常度模板 `ts_zscore(ts_sum(total_top_buy_transaction_count,21),252)` |
| 论坛 `43467688159511` | 买侧心理纯度显著高于卖侧；相对金额 > 绝对金额；多人协同增持置信度倍增 |
| 论文 `10.1093/rfs/6.1.79`（Damodaran & Liu 1993） | 内部人交易作为私人信息信号（EUR 侧转述：年化超额约 11%） |
| 论文 `10.2139/ssrn.3478344`（Beneish & Markarian 2019） | 内部人**买入**的理论模型（与本档案 §1.1 的「买强卖弱」一致） |

## 3. ★ 本轮移植实验：EUR 比值形态在 DEU **不迁移**（但机制正交）

| 臂 | alpha | S | F | 2Y | self |
|---|---|---:|---:|---:|---:|
| `divide(ts_sum(top_directional_significant_value_1,1260), ts_sum(subtract(total_top_buy_shares,total_top_sell_shares),84))` | `2r59xRvw` | 0.37 | 0.17 | **−0.41** | **0.038** |
| 同上，分母窗 84→126 | `d5aY6mdX` | 0.12 | 0.03 | **−0.29** | 0.071 |

⇒ **形态不迁移**（S 0.37 / 2Y 负）；但 **self-corr 仅 0.038** ⇒ **与 OS 池完全正交** ⇒ 是**干净的 DEU INSIDERS 塔新信号位储备**（塔位 2/3，缺 1 颗），缺的是**强度杠杆**。
⇒ 记 **PROVISIONAL（族级）**：本集不判死，但「单集天花板 < 1.0」与「比值形态 self-corr 近零」两条同时成立 ⇒ 下一轮应攻**强度**而非**形态**。

## 4. 引用本档案前的强制校验

```bash
python tools/gates/field_profile_completeness_gate.py \
    --profile tracking/DEU/reference/datasets/insider_agg_matrix.md
```

## 5. 本任务边界

- 本轮**只读档案 + 回测**：全部读数取自平台回测（`create_multi_simulation` → `get_alpha_details` / `backtest_results`），**未做任何平台提交**。
- 体检形态是**统一最小形态**（`group_rank(ts_mean(F,66),sector)`），**不是六法全套**；六法（覆盖/非零/多窗标准差/比值）在本集只做了 1 形态 ⇒ **逐字段覆盖与更新频率未穷尽**（LC/SC 只反映该形态下的持仓宽度）。
- 字段的**符号约定未向平台核实**（§1.2）：SV1/SV2 与 SV3/SV4 的正负含义**不可**从本档案外推。
- `insiders1`（8 字段）是**另一个数据集**，本档不覆盖；两者跨集即 2 数据集 ⇒ 非 ATOM。
