# DEU / TOP500 / D1 — sentiment27 字段全画像

> 生成：2026-11-19｜数据源：本轮实调 `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=sentiment27, filter_sharpe=false)`（未传 `max_fields`）。
> 取数结果：`count=18`、`platform_count=18`、`complete=true`、`pages_fetched=1`、`returned=18` ⇒ **未分片、无缺口**，去重后 18 = `platform_count`。
> 分母对账：`platform_count=18` ＝ 本文「字段全表」18 行 ＝ `get_datasets(DEU/TOP500/D1, category=sentiment)` 里 sentiment27 的 `fieldCount=18`，三处一致。
> 数据集级（`get_datasets`，实读）：name **Website Popularity Rankings**｜category sentiment｜coverage **0.9038**｜userCount **155**｜alphaCount **390**｜valueScore **4.0**｜pyramidMultiplier **1.8**。
> ⚠ **语义定位**：`sentiment27` 属 sentiment 类目，但**不是新闻情绪/NLP 打分**——它是 **Tranco 网站域名排名（网络关注度）**：`snl27_*` 为发行人名下全部映射域名的排名分布统计，`snt27_rank` 为单域名在 Tranco 的日度排名。

## 字段全表

|字段 id|type|coverage|userCount|alphaCount|dateCreated|pyramidMultiplier|描述|
|---|---|---:|---:|---:|---:|---:|---|
|`aggregate_collection_timestamp`|SYMBOL|0.9022|0|0|2026-07-01|1.8|聚合排名数据从源采集的日期；日期戳，非分析指标|
|`aggregate_reference_date`|SYMBOL|0.9022|0|0|2026-07-01|1.8|聚合排名数据的生效期日期；日期戳，非分析指标|
|`ranking_reference_date`|SYMBOL|0.9118|0|0|2026-07-01|1.8|网站排名数据的生效期日期；日期戳，非分析指标|
|`snl27_avgranking`|VECTOR|0.9022|18|21|2026-07-01|1.8|发行人全部映射域名的 Tranco 排名算术均值；越低越热门|
|`snl27_kurtosis`|VECTOR|0.9022|33|48|2026-07-01|1.8|域名排名分布的超额峰度（尾部厚度/极端值）|
|`snl27_relpopularity08`|VECTOR|0.9022|44|67|2026-07-01|1.8|alpha=0.8 的复合相对关注度；越高代表跨域名关注越广（本集 alphaCount 最高）|
|`snl27_relpopularity1`|VECTOR|0.9022|41|61|2026-07-01|1.8|alpha=1 的复合相对关注度；越高代表关注越广|
|`snl27_skewness`|VECTOR|0.9022|25|66|2026-07-01|1.8|域名排名分布的偏度（不对称/集中度）|
|`snl27_top50pctranking`|VECTOR|0.9022|13|16|2026-07-01|1.8|排名分布第 50 百分位（中位数）截断值；越低越好|
|`snl27_top50pctrankingavg`|VECTOR|0.9022|21|34|2026-07-01|1.8|前 50%（较好一半）域名的平均排名；越低越好|
|`snl27_top75pctranking`|VECTOR|0.9022|7|10|2026-07-01|1.8|排名分布第 75 百分位截断值；越低越好（本集 alphaCount 最低）|
|`snl27_top75pctrankingavg`|VECTOR|0.9022|14|43|2026-07-01|1.8|前 75% 域名的平均排名；越低越好|
|`snl27_topranking`|VECTOR|0.9022|18|21|2026-07-01|1.8|当日发行人域名中的最好（最低）排名；越低越好|
|`snl27_totalcountrydomains`|VECTOR|0.9022|11|15|2026-07-01|1.8|带国别码 TLD 或区域标识的关联域名数（无界正计数）|
|`snl27_totaldomains`|VECTOR|0.9022|31|43|2026-07-01|1.8|当日与发行人关联的去重域名总数（无界正计数）|
|`snl27_wq_pit`|VECTOR|0.9022|11|11|2026-07-01|1.8|内部 PIT 对齐标记；平台描述明写 not an analytical metric|
|`snt27_rank`|VECTOR|0.9118|20|28|2026-07-01|1.8|域名在 Tranco 中的日度人气排名，1 = 最热门；越低越好|
|`source_collection_timestamp`|SYMBOL|0.9118|0|0|2026-07-01|1.8|网站排名数据从源采集的日期；日期戳，非分析指标|

行数核对：18 行 = `platform_count` 18，缺口 **0**。上表 `coverage` / `userCount` / `alphaCount` / `dateCreated` / `pyramidMultiplier` 均为本轮平台返回体原值，未做估算或补值。

## 1. 聚合统计

### 1.1 总量与类型

| 项 | 值 |
|---|---|
| 字段总数 | **18** |
| VECTOR | **14** |
| SYMBOL | **4** |
| MATRIX / GROUP / OTHER | 0 / 0 / 0 |
| 去重后字段 id 数 | 18（单页 `returned=18`，无重复） |
| `pyramidMultiplier` | 全为 **1.8**（18/18） |
| `dateCreated` 取值集合 | **{2026-07-01}**（18/18，同日一次性 onboard） |
| coverage 取值集合 | **{0.9022, 0.9118}**（只有两个取值） |

### 1.2 coverage 分布

| 区间 | 字段数 | 构成 |
|---|---:|---|
| ≥ 0.9 | **18** | 全部 |
| 0.5 – 0.9 | 0 | — |
| 0.3 – 0.5 | 0 | — |
| 0 < c < 0.3 | 0 | — |
| = 0 | 0 | — |

- 取值明细（实读计数）：`0.9022` → **15** 个，`0.9118` → **3** 个（`ranking_reference_date` / `snt27_rank` / `source_collection_timestamp`）。
- 加权均值 = (15×0.9022 + 3×0.9118) / 18 = **0.903800**，与 `get_datasets` 的 dataset 级 **0.9038** 逐位吻合 ⇒ 数据集级 coverage 就是字段 coverage 的简单均值，无隐藏权重。
- 0.9118 的三个全部来自「单域名排名源」，0.9022 的十五个全部来自「发行人名下域名聚合源」⇒ **两条源、两档覆盖**，档差 0.0106（1.16%）。两档都不是「高覆盖」：约 9–10% 的 TOP500 标的在任一日没有该集数据。

### 1.3 alphaCount / userCount 分布

| alphaCount 区间 | 字段数 | 字段（括号内为 alphaCount） |
|---|---:|---|
| = 0 | **4** | 4 个 SYMBOL 日期戳（同时 userCount=0） |
| 1 – 20 | 4 | `snl27_top75pctranking`(10) `snl27_wq_pit`(11) `snl27_totalcountrydomains`(15) `snl27_top50pctranking`(16) |
| 21 – 50 | 7 | `snl27_avgranking`(21) `snl27_topranking`(21) `snt27_rank`(28) `snl27_top50pctrankingavg`(34) `snl27_top75pctrankingavg`(43) `snl27_totaldomains`(43) `snl27_kurtosis`(48) |
| 51 – 70 | 3 | `snl27_relpopularity1`(61) `snl27_skewness`(66) `snl27_relpopularity08`(67) |

- 合计校验：4 + 4 + 7 + 3 = **18** ✓
- 14 个 VECTOR 的 alphaCount 排序 = 10, 11, 15, 16, 21, 21, 28, 34, 43, 43, 48, 61, 66, 67 ⇒ **中位数 31**（第 7/8 位为 28 与 34），最小 **10**（`snl27_top75pctranking`），最大 **67**（`snl27_relpopularity08`）。
- **字段行 alphaCount 求和 = 484、userCount 求和 = 307**；数据集级是 **390 / 155**。两者不等是计数口径差异，不是数据矛盾：一条 alpha 用到多个字段时，会在每个字段行各计一次；`get_datasets` 的 dataset 级数字按 alpha 去重。⇒ 判「本集多拥挤」用 **390**；判「哪个字段被用得最多」用字段行 alphaCount。
- 热度集中在 **相对关注度 + 分布形状矩**（`relpopularity08` 67 / `skewness` 66 / `relpopularity1` 61 / `kurtosis` 48），说明既有实践主要在把该集当「关注度水平 + 排名分布形状」用，而不是当单域名排名用。

### 1.4 与数据集级元数据的对账

| 项 | 字段实读 | `get_datasets` | 判定 |
|---|---|---|---|
| 字段数 | 18 | 18 | ✅ 一致 |
| coverage | 0.903800（简单均值） | 0.9038 | ✅ 四舍五入一致 |
| pyramidMultiplier | 1.8（18/18） | 1.8 | ✅ 一致 |
| userCount | 307（字段行求和） | 155 | 口径不同（字段行按 alpha-字段对重复计） |
| alphaCount | 484（字段行求和） | 390 | 口径不同（同上） |
| valueScore | 字段目录无此字段 | 4.0 | 只在 dataset 级提供 |

## 2. 字段族拆解

### 2.1 按命名空间前缀（实读计数）

| 前缀 | 字段数 | 占比 | 语义 | coverage 档 |
|---|---:|---:|---|---|
| `snl27_` | **13** | 72.2% | 发行人名下全部映射域名的 Tranco 排名**分布统计** | 0.9022 |
| `snt27_` | **1** | 5.6% | 单域名在 Tranco 中的日度人气排名 | 0.9118 |
| `aggregate_` | **2** | 11.1% | 聚合源的采集日期 / 生效期日期戳（SYMBOL） | 0.9022 |
| `ranking_` | **1** | 5.6% | 单域名排名源的生效期日期戳（SYMBOL） | 0.9118 |
| `source_` | **1** | 5.6% | 单域名排名源的采集日期戳（SYMBOL） | 0.9118 |
| **合计** | **18** | 100% | — | — |

### 2.2 `snl27_` 内部 6 个语义子族（合计 13）

| 子族 | 字段 | 数 |
|---|---|---:|
| 中心趋势 | `snl27_avgranking`（算术均值）、`snl27_topranking`（最优/最低排名） | 2 |
| 分位截断与分位内均值 | `snl27_top50pctranking`、`snl27_top50pctrankingavg`、`snl27_top75pctranking`、`snl27_top75pctrankingavg` | 4 |
| 分布形状矩 | `snl27_skewness`、`snl27_kurtosis` | 2 |
| 复合关注度得分 | `snl27_relpopularity08`、`snl27_relpopularity1` | 2 |
| 域名规模计数 | `snl27_totaldomains`、`snl27_totalcountrydomains` | 2 |
| 内部 PIT 标记 | `snl27_wq_pit` | 1 |

### 2.3 结构观测

- **两条数据源、一套排名体系**：`snl27_*`（13，聚合源，cov 0.9022）与 `snt27_rank`（1，单域名源，cov 0.9118）度量的是**同一个 Tranco 排名体系**的两个切面，不是两个独立机制。
- **分位族 4 字段互相近似**：`top50pctranking` / `top50pctrankingavg` / `top75pctranking` / `top75pctrankingavg` 都出自同一条排名分布，是同一信息的截断位/均值位差异（分位越低越靠前）。`avgranking` 与 `topranking` 同理是水平量的两个统计量。
- **复合得分只差一个参数**：`relpopularity08` 与 `relpopularity1` 的区别仅是复合参数 alpha（0.8 vs 1），不是不同机制。
- **形状矩是唯一"二阶"信息**：`skewness` / `kurtosis` 描述分布形状而非水平，与上述水平量正交度最高，也因此 alphaCount 高（66 / 48）。
- **冗余率**：13 个 `snl27_` 里，去掉 2 个规模计数、1 个内部标记后，10 个是排名分布的不同统计量；按「同一分布的矩/分位」口径，可压缩到 **3 个语义位**（水平、分位截断、分布形状），冗余度约 70%。

## 3. 可用性三分（18 个不都能进表达式）

### 3.1 信号可用（11 个，61.1%）

`snl27_avgranking`、`snl27_topranking`、`snl27_top50pctranking`、`snl27_top50pctrankingavg`、`snl27_top75pctranking`、`snl27_top75pctrankingavg`、`snl27_skewness`、`snl27_kurtosis`、`snl27_relpopularity08`、`snl27_relpopularity1`、`snt27_rank`。

- **方向：9 个「越低越好」，2 个「越高越好」**。排名类 8 个（`avgranking` / `topranking` / 4 个分位字段）＋ `snt27_rank` 都是「排名数值越小＝越热门」；`relpopularity08` / `relpopularity1` 反向（越高＝关注越广）⇒ **排名族进表达式前必须取负**（`-1 *` 或在 `rank()` 前后翻转），否则符号与「关注度上升 → 未来收益」的假设相反。这是本集**最容易犯的方向错误**。
- **`skewness` / `kurtosis` 无界**（实数域），且是分布形状而非水平，适合做二阶特征，不宜当主信号单独成腿。
- **`kurtosis` 存在符号陷阱**：超额峰度的「高」既可能来自单一超热域名（集中）也可能来自长尾，经济含义不单向，回测前必须自己确认方向（本档案不做方向背书）。
- **同族高度同源**：`relpopularity08` 与 `relpopularity1` 只差参数；`avgranking` / `topranking` / 4 个分位字段同为同一排名分布的统计量 ⇒ **每语义子族只取一席**，避免同一波重复买同一条信息。

### 3.2 计数类：需归一化（2 个，11.1%）

`snl27_totaldomains`（去重域名总数，uC 31 / aC 43）、`snl27_totalcountrydomains`（带 ccTLD 的域名数，uC 11 / aC 15）。

- 两者是**无界正计数**，与公司规模、跨国经营程度强相关：裸用等于在做「大公司 vs 小公司」而不是关注度信号。
- 正确用法：① `divide(totalcountrydomains, totaldomains)` 取**海外域名占比**（单一经济含义）；② 或先 `rank` / `ts_zscore` 去掉规模维度；③ 或 `divide(计数, ts_mean(计数, 66))` 取相对自身历史的扩张速度。
- ⚠ **分母零值**：`snl27_totaldomains` 平台描述未保证 ≥1，`divide` 前建议 `trade_when(snl27_totaldomains > 0, …, -1)` 或先 `ts_backfill`。

### 3.3 元数据不可用（5 个，27.8%）

| 字段 | 类型 | 为何不可用 |
|---|---|---|
| `aggregate_collection_timestamp` | SYMBOL | 采集日期，字符串型日期戳，算子无定义 |
| `aggregate_reference_date` | SYMBOL | 生效期日期戳 |
| `ranking_reference_date` | SYMBOL | 生效期日期戳 |
| `source_collection_timestamp` | SYMBOL | 采集日期戳 |
| `snl27_wq_pit` | VECTOR | 内部 PIT 对齐标记，平台描述明写 *not an analytical metric*；它是 VECTOR 类型，**`filter_sharpe=false` 下照样出现在目录里，极易被误当信号** |

- 4 个 SYMBOL 的 userCount / alphaCount 全为 **0**（无任何历史使用），是干净的元数据。
- `snl27_wq_pit` 例外：**uC=11 / aC=11**，说明历史上确有 11 条 alpha 用到它（大概率作辅助对齐或误用），**不能因为"有 alphaCount"就当作可用信号**。
- 这 5 个仅可用于研究期：语义对齐、时效衰减窗口设定、事件去重、PIT 校验。

### 3.4 三分一致性检查

- 11（信号）+ 2（计数归一化）+ 5（元数据）= **18** ✓，与 `platform_count=18` 相等，无遗漏。
- 18 个字段的 coverage 只在 0.9022 / 0.9118 两档，**没有任何高覆盖字段**：TOP500 里约 9–10% 的标的在任一日没有该集数据，表达式必须能处理「无数据 = NaN」，填充策略要显式写（`ts_backfill` / `trade_when`），不能依赖隐式填充。
- 可作信号的 11 个字段**全部集中在同一条排名体系**（Tranco），本集不提供第二个独立经济机制 ⇒ 单集内不存在「两条独立腿」，跨集只能走 gating / grouping / residual / ratio（AGENTS.md §7.7）。

## 4. 引用本档案前的强制校验

```bash
python tools/gates/field_profile_completeness_gate.py \
    --profile tracking/DEU/reference/datasets/sentiment27.md
```

该闸三判据：① `## 字段全表` 逐字段真实 id、无通配占位；② 全表每个字段在档案内均有带数字读数的行（差集逐条列出）；③ 全表行数 == 实测行数。本档案需 exit 0 才可作为选区 / 建族依据。

## 5. 本任务边界

- 本轮**零回测、零仿真配额**：全部读数取自平台目录 API（`get_datafields` / `get_datasets`），属**静态画像**。
- 六法实测**已于 2026-11-19 补做并核验**（66 条回测实读，见第 7 节）；本档案字段全表的 `coverage` 列仍是**平台声明值**，不等于逐日横截面宽度，逐日宽度以第 7 节实测覆盖为准。
- **本档案前一版本**曾含一节「六法实测」（56 条 `get_alpha_details` 读数，标注 2026-11-19）；该节已转为 **§6bis 历史附录（仅供追溯）**，动态读数以第 7 节实跑为准。

## 6bis 历史附录（已被第 7 节取代）

本节的读数已由第 7 节的实跑结果取代，仅供追溯。

> ⚠ **来源状态：未经本轮核验**。以下数字来自本档案前一版本（该目录当时为未跟踪文件，无 git 历史），标注的生成日期为 2026-11-19，产物是 56 条 `get_alpha_details` 实读。
> 本轮（字段画像任务）只调用了 `get_datafields` / `get_datasets`，**没有复跑这批判定**，因此不能确认这 56 条 alpha 的读数、映射关系与汇总是否与当时一致。
> **引用前必须用 `get_alpha_details` 对同名 alpha 逐条重新实测**，不得把本节当作已核实结论使用。

### 6.1 口径（沿用原记录，仅供追溯）

DEU / TOP500 / Delay 1 / Neutralization **NONE** / Decay **0** / Truncation 0 / Pasteurization ON / NaN Handling OFF / IS 2014-01-01 → 2023-12-31（P0Y0M0D 默认全历史）。
覆盖率 = `(longCount + shortCount) / 500`。六法：法1 = 裸 `vec_avg(F)`｜法2 = `vec_avg(F) != 0`｜法3 = `ts_std_dev(vec_avg(F), N) != 0`，N ∈ {5, 22, 66, 132}。
原记录称样本映射表 **56 个 alpha**（法1 11 + 法2 11 + 法3 N=5 11 + N=22 11 + N=66 11 + N=132 1），56/56 可读；原记录亦注明该批全部为 `stage=IS` / `status=UNSUBMITTED` 的探测件，RA 未过（主因 `LOW_SHARPE`：0.72–0.94 vs 平台限 1.58），只回答「字段覆盖 / 更新频率」，不作候选或提交依据。

### 6.2 按字段汇总（原记录，仅供追溯）

| 字段 | 法1 覆盖 | 法2 非零 | N=5 | N=22 | N=66 | N=5 / 法1 | N=22 / 法1 | N=66 / 法1 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
|`snl27_avgranking`|378（75.6%）|378（75.6%）|381（76.2%）|383（76.6%）|386（77.2%）|100.8%|101.3%|102.1%|
|`snl27_topranking`|378（75.6%）|378（75.6%）|373（74.6%）|379（75.8%）|383（76.6%）|98.7%|100.3%|101.3%|
|`snl27_top50pctranking`|378（75.6%）|378（75.6%）|381（76.2%）|383（76.6%）|386（77.2%）|100.8%|101.3%|102.1%|
|`snl27_top50pctrankingavg`|378（75.6%）|378（75.6%）|381（76.2%）|383（76.6%）|386（77.2%）|100.8%|101.3%|102.1%|
|`snl27_top75pctranking`|378（75.6%）|378（75.6%）|381（76.2%）|383（76.6%）|386（77.2%）|100.8%|101.3%|102.1%|
|`snl27_top75pctrankingavg`|378（75.6%）|378（75.6%）|381（76.2%）|383（76.6%）|386（77.2%）|100.8%|101.3%|102.1%|
|`snl27_skewness`|279（55.8%）[a]|280（56.0%）|283（56.6%）|288（57.6%）|294（58.8%）|101.4%|103.2%|105.4%|
|`snl27_kurtosis`|316（63.2%）[b]|316（63.2%）|264（52.8%）|275（55.0%）|286（57.2%）|83.5%|87.0%|90.5%|
|`snl27_relpopularity08`|378（75.6%）|378（75.6%）|365（73.0%）|381（76.2%）|385（77.0%）|96.6%|100.8%|101.9%|
|`snl27_relpopularity1`|378（75.6%）|378（75.6%）|361（72.2%）|379（75.8%）|384（76.8%）|95.5%|100.3%|101.6%|
|`snt27_rank`|381（76.2%）|381（76.2%）|387（77.4%）|389（77.8%）|392（78.4%）|101.6%|102.1%|102.9%|

原记录注：[a] `snl27_skewness` 法1 = 225 long + 54 short；法2 = 280 long + 0 short。[b] `snl27_kurtosis` 法1 = 31 long + 285 short（净空头）；法2 = 316 long + 0 short。其余 9 个字段在全部方法下 `shortCount` 均为 0。`snt27_rank` 另有 N=132：395（79.0%）。

### 6.3 sharpe / turnover（原记录，仅供追溯）

| 字段 | 法1 | 法2 | N=5 | N=22 | N=66 |
|---|---|---|---|---|---|
|`snl27_avgranking`|0.89 / 3.88%|0.88 / 2.01%|0.87 / 0.67%|0.88 / 0.63%|0.87 / 0.60%|
|`snl27_topranking`|0.72 / 4.46%|0.88 / 2.01%|0.86 / 1.05%|0.87 / 0.71%|0.87 / 0.63%|
|`snl27_top50pctranking`|0.88 / 4.23%|0.88 / 2.01%|0.87 / 0.67%|0.88 / 0.63%|0.87 / 0.60%|
|`snl27_top50pctrankingavg`|0.83 / 4.17%|0.88 / 2.01%|0.87 / 0.67%|0.88 / 0.63%|0.87 / 0.60%|
|`snl27_top75pctranking`|0.90 / 4.23%|0.88 / 2.01%|0.87 / 0.67%|0.88 / 0.63%|0.87 / 0.60%|
|`snl27_top75pctrankingavg`|0.86 / 4.05%|0.88 / 2.01%|0.87 / 0.67%|0.88 / 0.63%|0.87 / 0.60%|
|`snl27_skewness`|0.93 / 8.58%|0.92 / 2.41%|0.91 / 0.97%|0.92 / 0.75%|0.92 / 0.65%|
|`snl27_kurtosis`|−0.86 / 7.22%|0.92 / 2.23%|0.93 / 1.46%|0.93 / 1.01%|0.94 / 0.73%|
|`snl27_relpopularity08`|0.94 / 1.93%|0.88 / 2.01%|0.87 / 3.02%|0.88 / 0.76%|0.87 / 0.66%|
|`snl27_relpopularity1`|0.91 / 1.97%|0.88 / 2.01%|0.87 / 3.10%|0.88 / 0.79%|0.88 / 0.65%|
|`snt27_rank`|0.89 / 5.31%|0.88 / 3.46%|0.85 / 0.69%|0.86 / 0.65%|0.85 / 0.61%|

### 6.4 原记录的结论（仅供追溯，仅作复跑线索）

① **法1 与法2 在场数基本相等** ⇒ 原记录据此判「缺失是 NaN 而非 0」；唯一例外 `snl27_skewness`（279 vs 280）。原记录同时强调「在场数相等 ≠ 信号等价」（`kurtosis` 法1 sharpe −0.86 vs 法2 +0.92，符号翻转）。
② **频率档**：以「N=5 / 法1 ≥ 90%」为日更判据，10 个字段归日更；`snl27_kurtosis` N=5 仅 83.5% → N=66 90.5%，原记录判其按周级或更慢更新。
③ **窗口下限**：日更字段可用 5–22 短窗；`snl27_kurtosis` 需 ≥66。原记录并提示法3 的 turnover 普遍低于平台 `LOW_TURNOVER` 下限 0.01，窗口与 turnover 必须一起算。

### 6.5 与平台声明 coverage 的偏差（原记录，仅供追溯）

| 字段 | 平台声明 coverage | 法1 实测（/500） | 偏差（pp） |
|---|---:|---:|---:|
|`snl27_avgranking`|0.9022|0.7560|−14.62|
|`snl27_topranking`|0.9022|0.7560|−14.62|
|`snl27_top50pctranking`|0.9022|0.7560|−14.62|
|`snl27_top50pctrankingavg`|0.9022|0.7560|−14.62|
|`snl27_top75pctranking`|0.9022|0.7560|−14.62|
|`snl27_top75pctrankingavg`|0.9022|0.7560|−14.62|
|`snl27_skewness`|0.9022|0.5580|−34.42|
|`snl27_kurtosis`|0.9022|0.6320|−27.02|
|`snl27_relpopularity08`|0.9022|0.7560|−14.62|
|`snl27_relpopularity1`|0.9022|0.7560|−14.62|
|`snt27_rank`|0.9118|0.7620|−14.98|

原记录的推断（算术，未向平台核验分母）：若声明值分母是 DEU 实际有数据的标的数 ≈ **419**（378÷0.9022≈419.0、381÷0.9118≈417.9），则排名类与 relpopularity 字段的缺口主要由「500 名义规模 vs 419 实际规模」解释；`skewness`（279÷419≈66.6%）与 `kurtosis`（316÷419≈75.4%）在该分母下仍显著偏低 ⇒ 原记录判这两个形状字段本身更稀疏。
**本轮立场**：该推断未被本轮任何调用证实；`coverage` 列（平台声明）**不可直接当 TOP500 里的可交易比例**使用，做截面覆盖预估前须重跑。

## 7. 六法实测（本轮实跑，已核验）

> 生成：2026-11-19。66 条表达式（11 个信号字段 × 6 法）先经 `mcp__wq-brain-http__preflight_expressions`（region=DEU, universe=TOP500, delay=1, dataset_id=sentiment27）预检：`valid=true`、`unknown_fields=[]`、`vec_avg` 包裹形态无需修正；分 7 批 `mcp__wq-brain-http__create_multi_simulation` 派发（单批 ≤10 条；multisim id：`1UOZyT1FQ5gt9o419VGyONZn` / `1arS0xb356TbvbrYV2kqSN` / `4y2XyJ70z4icct0GUSqFbf3` / `2CkARI6ye4BLaEE7RhBN2jp` / `kHsSs6z84YP9y24T9sFNpg` / `4k3d3T8Jv4GsbGT1dQK4kw7A` / `1BE9KAgcv4HncJ51bWSDjzSV`）；`batch_status` 收批 66/66 COMPLETE、errors=0；逐条 `get_alpha_details` 实读（平台返回 `code` 与 multisim 提交表达式逐条核对一致）。
> 口径：neutralization=**NONE** / decay=**0** / test_period=**P0Y0M0D**（IS 2014-01-01→2023-12-31）/ truncation=**0.0** / region=DEU / universe=**TOP500** / delay=1 / pasteurization=ON / nanHandling=OFF；VECTOR 一律 `vec_avg`。
> 六法：法1 = 裸 `vec_avg(F)`；法2 = `vec_avg(F) != 0`；法3 = `ts_std_dev(vec_avg(F), N) != 0`（N ∈ {5, 22, 66}）；法4 = `divide(vec_avg(F), ts_mean(vec_avg(F), 252)) > 1`。
> 覆盖率 = `(metrics.longCount + metrics.shortCount) / 500`。频率判定：n5 ≥ 0.9×法1 ⇒ daily（窗 5–22）；n5 不足而 n22 ≥ 0.9×法1 ⇒ weekly（窗 22）；否则 slow（窗 66）。零膨胀 = 法2 明显低于法1（本集无）。

| 字段 | 法1 覆盖 | 法2 非零 | N=5 | N=22 | N=66 | 法4 比值(>1 占比) | 频次 | 窗下限 | 零膨胀 | !=0 陷阱 | 备注 |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|---|
| `snl27_avgranking` | 0.756（378L+0S） | 0.756 | 0.762 | 0.766 | 0.772 | 0.362 | daily | 5 | 否 | 否 | 排名类「越低越好」进表达式前须取负；实测 0.756 vs 声明 0.9022（缺口≈500 名义 vs 419 实际分母）；cov=nz ⇒ 非零膨胀 |
| `snl27_topranking` | 0.756（378L+0S） | 0.756 | 0.746 | 0.758 | 0.766 | 0.344 | daily | 5 | 否 | 否 | 排名类须取负；n5/法1=0.987 仍达 daily 线；与 avgranking 同属中心趋势子族，每子族只取一席 |
| `snl27_top50pctranking` | 0.756（378L+0S） | 0.756 | 0.762 | 0.766 | 0.772 | 0.354 | daily | 5 | 否 | 否 | 分位截断族，须取负；读数与 avgranking 同形（378/378/381/383/386），同族同源高冗余 |
| `snl27_top50pctrankingavg` | 0.756（378L+0S） | 0.756 | 0.762 | 0.766 | 0.772 | 0.362 | daily | 5 | 否 | 否 | 分位内均值族，须取负；读数与 top50pctranking 同形 |
| `snl27_top75pctranking` | 0.756（378L+0S） | 0.756 | 0.762 | 0.766 | 0.772 | 0.358 | daily | 5 | 否 | 否 | 分位截断族（本集 alphaCount 最低 10），须取负；法1 sharpe 0.90 为排名族最高 |
| `snl27_top75pctrankingavg` | 0.756（378L+0S） | 0.756 | 0.762 | 0.766 | 0.772 | 0.356 | daily | 5 | 否 | 否 | 分位内均值族，须取负；与 top50pctrankingavg 同族同源 |
| `snl27_skewness` | 0.558（225L+54S） | 0.560（280L+0S） | 0.566 | 0.576 | 0.588 | 0.284 | daily | 5 | 否 | **是** | **禁止用 != 0 变换**：法1(225L/54S)→法2(280L/0S) 多空反号翻转（54 个负偏度样本被翻成多头）；无界矩类须 rank/zscore 后用；实测 0.558 显著低于声明 0.9022（形状字段本身更稀疏） |
| `snl27_kurtosis` | 0.632（31L+285S） | 0.632（316L+0S） | 0.528 | 0.550 | 0.572 | 0.296 | slow | 66 | 否 | **是** | **禁止用 != 0 变换**：法1(31L/285S, sharpe −0.86)→法2(316L/0S, sharpe +0.92) 完全反号翻转；n5=0.835×cov、n22=0.870×cov 均不达 0.9 ⇒ 本集唯一 slow；法3 覆盖随窗变宽单调恢复（264→275→286），符合周级以下更新 |
| `snl27_relpopularity08` | 0.756（378L+0S） | 0.756 | 0.730 | 0.762 | 0.770 | 0.378 | daily | 5 | 否 | 否 | relpopularity「越高越好」不需取负；本集 alphaCount 最高（67）；法1 sharpe 0.94 / fitness 1.79 为全集最优；法4 长边 0.378 全集最高 |
| `snl27_relpopularity1` | 0.756（378L+0S） | 0.756 | 0.722 | 0.758 | 0.768 | 0.374 | daily | 5 | 否 | 否 | relpopularity「越高越好」；与 relpopularity08 只差复合参数 alpha，同源冗余 |
| `snt27_rank` | 0.762（381L+0S） | 0.762 | 0.774 | 0.778 | 0.784 | 0.366 | daily | 5 | 否 | 否 | 单域名源（声明 0.9118 本集最高档），须取负；实测覆盖 0.762 全集最高；法3 各窗覆盖 387/389/392 全集最高 |

**判定**：11 个字段全部有信号形态读数——10 个 daily（短窗 5–22 可用）、`snl27_kurtosis` slow（窗下限 66）；除 kurtosis 外法2 非零 ≈ 法1（缺失是 NaN 而非 0）；`snl27_skewness` / `snl27_kurtosis` 两个无界矩类存在 **!= 0 反号陷阱，禁止用 != 0 变换**；实测覆盖 0.558–0.762 系统性低于平台声明 0.9022/0.9118（−14.6 ～ −34.4pp），缺口与「TOP500 名义规模 vs ≈419 实际有数据标的」的解释一致，且与 §6bis 原记录逐字段吻合（附录已转正）。

## 8. 2026-11-21 增量：sentiment7 × sentiment27「残差化向量中性」族（生产档复跑）

> 口径：DEU / TOP500 / D1 / **生产档**（decay 4 / SUBINDUSTRY / truncation 0.08 / nanHandling OFF / unitHandling VERIFY / pasteurization ON / maxTrade OFF / FASTEXPR / IS 2014-01-01→2023-12-31）。
> 派发：`mcp__wq-brain-http__create_multi_simulation`，**每批 2 臂**（用户「每次回测派批最多 2 个」），在飞批 ≤ 2；臂序＝派发顺序核对。
> 骨架：`vector_neut( <snt7 关注度信号> , <snl27 中性化目标> )`——`snt7` 侧 = `ts_quantile(ts_ir(ts_mean(max(ts_backfill(vec_avg(snt7_all_languages_views),22), ts_delay(…,5)),5),22), 252, driver="gaussian")`；`snl27` 侧 = `ts_backfill(vec_avg(<F>),22)`。

### 8.1 本轮新增读数（逐字段／逐臂）

| 字段（snl27 侧） | 臂（中性化目标） | alpha | S | F | 2Y | sub | TO | RA failed | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `snl27_top50pctrankingavg` | 分位内均值 | `leaE9287` | **1.90** | 1.52 | **2.43** | 1.17 | 0.152 | **0** | §1.3 标注的「零臂未回测」字段，本轮首次成臂 |
| `snl27_top75pctrankingavg` | 分位内均值 | `E5QNLEpr` | 1.89 | 1.51 | 2.42 | 1.17 | 0.152 | 0 | 同族 |
| `snl27_topranking` | 中心趋势 | `omaRkL82` | **1.94** | 1.57 | **2.46** | 1.19 | 0.152 | 0 | 本轮最高 S |
| `snl27_skewness` | 分布形状 | `O0WR2L5Y` | 1.84 | 1.46 | 2.18 | 1.05 | 0.153 | 0 | 唯一非分位/非中心的目标 |
| `snl27_top50pctranking` | 分位截断 | `0mPxawrK` | 1.88 | 1.50 | 2.39 | 1.19 | 0.152 | 0 | — |
| `snl27_avgranking` | 中心趋势 | `akaeg7xR` | 1.88 | 1.50 | 2.39 | 1.18 | 0.152 | 0 | — |
| `snl27_totaldomains` | 裸单字段（无残差化） | `akae8krv` | 0.41 | 0.19 | 1.76 | 0.32 | 0.015 | 2 | 计数类裸用＝规模代理（与 §3.2 一致） |
| `snl27_totalcountrydomains` | 裸单字段 | `A1xe51Rl` | 0.17 | 0.05 | 1.11 | 0.22 | 0.016 | 3 | 同上，更弱 |
| `snl27_avgranking` | 裸单字段 | `O0WR2767` | −0.13 | −0.03 | 0.46 | −0.45 | 0.024 | 4 | 排名类裸用方向为负（§3.1「须取负」成立） |
| `snl27_kurtosis` | 裸单字段 | `Jj8o273A` | 0.16 | 0.04 | 0.01 | −0.12 | 0.027 | 4 | 慢变量、slow 档 |

### 8.2 两条负杠杆（可复用）

| 换法 | Δ | 结果 |
|---|---|---|
| `snt7_all_languages_views` → `snt7_views` | ΔS **−1.11** | `N1PL2ZO7` S 0.79（RA 失败 3 项，含 `IS_LADDER_SHARPE` 1.31）⇒ **多语言合计是必需口径，单 project 覆盖不足** |
| `ts_quantile` 窗 252 → 504 | ΔS −0.11 / Δ2Y **−0.37** | `akaegpOw` S 1.79 / 2Y 2.06（RA 全过）⇒ **252 是上界，504 是负杠杆** |

### 8.3 ★ 终判：本族在 DEU 已被占位（self-corr 闸）

- 族内互相关（本地 `compute_mutual_correlation`，4 年 PnL）：`leaE9287`↔`E5QNLEpr` **0.9996**、↔`0mPxawrK` 0.9987、↔`akaeg7xR` 0.9985；`omaRkL82`↔`akaegpOw` 0.9528、↔`O0WR2L5Y` 0.8029 ⇒ **6 个 RA-clean 变体只有 1 条独立信息**。
- 对已提交件 `bl6OWZ2M`（SENTIMENT 塔在册件，`prod 0.6671 / self 0.0306`）：`omaRkL82` **0.9760**、`akaegpOw` 0.9324、`leaE9287` 0.9755 ⇒ **全部超过 self-corr 0.70 闸**。
- `check_self_correlation`（本地 OS 池，pool_size 22）逐条复测：`omaRkL82` max **0.9760 FAIL**、`akaegpOw` max **0.9324 FAIL**。
- 与既有 17 颗篮子互相关全部 |r| < 0.12（`leaE9287` 对篮中 17 颗最大 0.0468）⇒ **不是篮子冲突，是 OS 池克隆**。

⇒ **结论（PROVISIONAL，族级）**：DEU 的 `sentiment7 × sentiment27` 残差化族已被 `bl6OWZ2M` 占位。**换 `snl27` 中性化目标不产生新信息**（分位/中心/形状三类目标之间 0.77–0.999 高度同源，符合 §2.3「同一分布的矩/分位，冗余度约 70%」的预判）；本轮 6 颗 RA-clean 件**均不可交付**（self-corr 闸），仅作**方向锚**与**机制证据**留档。

### 8.4 对档案既有结论的修正

| 原结论 | 本轮实测 | 修正后 |
|---|---|---|
| §1.3「`snl27_top50pctrankingavg` 零臂未回测」 | 本轮首次成臂，S 1.90 / 2Y 2.43 / RA 全过 | **已回测**；但落入 §8.3 克隆族 ⇒ 记「已测·被 self-corr 拦」 |
| §2.3「分位族 4 字段互相近似、可压缩到 3 个语义位」 | 分位/中心/形状三类目标间互相关 0.77–0.999 | **强化**：连「换语义位」都换不出独立 PnL，冗余度应记为 **≥ 90%（对残差化用法而言）** |
| §3.1「排名类 8 个进表达式前必须取负」 | `snl27_avgranking` 裸用 S **−0.13**（sub −0.45） | **成立**（首次实测确认） |
| §3.2「计数类裸用＝规模代理」 | `totaldomains` 裸用 S 0.41 / TO 0.015 | **成立**（TO 被压到 1.5%＝换手塌缩到不可交易） |
