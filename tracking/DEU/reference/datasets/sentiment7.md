# DEU / TOP500 / D1 — sentiment7 字段全画像

> 生成：2026-11-18｜来源：`mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id=sentiment7, filter_sharpe=false)` 全量实读
> 分片情况：**未分片**——单页返回 `complete=true`、`pages_fetched=1`、`platform_count=3`、`returned=3`；去重后 3 = platform_count，无缺口。该集 3 字段远低于平台 search 的 100 条上限，故未按前缀分片。
> 分母对账（四路一致）：`platform_count=3` ｜ `returned=3`（去重后 3） ｜ `get_datasets(region=DEU, universe=TOP500, delay=1, search=sentiment7)` 的 `fieldCount=3` ｜ 本地 `mcp__wqb-db__get_field_catalog(DEU, sentiment7)` 的 `field_count=3`。本文「字段全表」3 行。
> 数据集级（`get_datasets`，DEU/TOP500/D1）：name **Webpage Views  Data**（原样，中间双空格）｜category **sentiment**｜coverage **0.7418**｜userCount **63**｜alphaCount **114**｜valueScore **4.0**｜pyramidMultiplier **1.8**
> ⚠ **语义更正（沿用前稿结论并在本轮复核）**：本集虽归 sentiment 类目，**不是新闻情绪**——它是**维基百科页面浏览量**（`snt7_*`），是 attention / 散户关注度的代理变量。数据集描述原文：「tracks daily Wikipedia page views for a global universe of companies, including both parent entities and their subsidiaries」，且明写跨语言聚合（`across multiple languages and lin…`，平台描述被截断）。

## 0. 聚合统计

### 0.1 总量与类型

| 项 | 值 |
|---|---|
| 字段总数 | **3** |
| VECTOR | **3**（3/3 = 100%） |
| SYMBOL | 0 |
| MATRIX / GROUP / OTHER | 0 / 0 / 0 |
| `pyramidMultiplier` | 全为 **1.8**（3/3） |
| `dateCreated` 取值集合 | **{2026-07-01}**（3/3，同日一次性 onboard） |
| coverage 取值集合 | **{0.7357, 0.7539}**（只有两档，无第三个取值） |
| 全字段共同前缀 | `snt7_`（3/3） |

### 0.2 coverage 分布

| 区间 | 字段数 | 构成 |
|---|---|---|
| ≥ 0.7 | **3** | 全部（0.7539 一个 / 0.7357 两个） |
| 0.5 – 0.7 | 0 | — |
| 0.3 – 0.5 | 0 | — |
| 0.3 以下（>0） | 0 | — |
| = 0 | 0 | — |

- 算术均值 = (0.7539 + 0.7357 + 0.7357) / 3 = 2.2253 / 3 = **0.741767**，四舍五入 **0.7418**，与 `get_datasets` 的 dataset 级 0.7418 **逐位吻合** ⇒ 数据集级 coverage 就是字段 coverage 的简单均值（与本区 `sentiment27.md` 观察到的同一口径）。
- 极差仅 **0.0018**（0.18 个百分点），说明三个字段共用同一套 TOP500 映射；`snt7_all_languages_views` 略高 0.0018，是「全语言合计」比「按 project × access type 拆分」多补到一小批名字。
- 0.7357 ≈ TOP500 的 **368** 名，0.7539 ≈ **377** 名。覆盖 > 0.4，**不强制 backfill**。

### 0.3 alphaCount / userCount 分布

| 区间（alphaCount） | 字段数 | 字段（括号内为 alphaCount） |
|---|---|---|
| = 0 | 0 | —（本集无零 alphaCount 字段） |
| 1 – 20 | 1 | 时间戳字段（6） |
| 21 – 50 | 1 | 单 project 浏览量字段（37） |
| 51 – 100 | 1 | 全语言合计字段（76） |

- VECTOR 字段 alphaCount 中位数 = **37**，均值 = 119 / 3 = **39.67**；最小 6（时间戳），最大 76（全语言合计）。
- **字段行 alphaCount 求和 = 119，userCount 求和 = 75**；数据集级是 **114 / 63**。两者不等属口径差异、不是数据矛盾：一条 alpha 用了多个字段时，会在这几个字段行各计一次，而 `get_datasets` 的 dataset 级计数按 alpha 去重（119 − 114 = 5 次重复计；75 − 63 = 12 次重复计）。⇒ 判断「本集多拥挤」用 **114**；判断「哪个字段被用得最多」用字段行 alphaCount。
- **拥挤度高度集中**：全语言合计字段一个占字段行 alphaCount 的 **76 / 119 = 63.9%**，其余两个合计 36.1%。说明已有人做过这条信号，且集中在聚合度最高的那一档。
- userCount 40 / 6 / 29 也同向（全语言合计最热）。userCount 6 与 alphaCount 6 的时间戳字段值得单独看（见 §3.3）。

### 0.4 本地目录 vs 平台的计数漂移（**本轮新发现，必须按平台口径**）

| 字段 | 平台 userCount / alphaCount | 本地 `field_catalog` userCount / alphaCount |
|---|---|---|
| `snt7_all_languages_views` | **40 / 76** | 1 / 2 |
| `snt7_timestamp` | **6 / 6** | 1 / 1 |
| `snt7_views` | **29 / 37** | 3 / 3 |

- 本地 `data/wqb.db` 的 `field_catalog` **字段 id 与 coverage 与平台完全一致**（3 行、0.7539/0.7357/0.7357），但 **userCount / alphaCount 是陈旧快照**（量级差 20–38 倍）。⇒ 本项目 §8.9 的「本地快照」纪律适用于此：**拥挤度判断一律读平台 `get_datafields`，不得引用本地计数**。
- 本地 `field_catalog` 的 `data_type` 记为 **MATRIX**，而平台字段级 `type` **3/3 都是 VECTOR**（`get_datasets` 不返回 dataType 字段，无法据平台核对数据集级类型）。二者不冲突但**不要据本地 `data_type=MATRIX` 推断字段是标量**——平台字段是向量，进表达式前必须过 `vec_*`。

### 0.5 字段族拆解（按前缀，实读计数）

| 前缀 | 字段数 | 占比 | 语义 | 覆盖档 |
|---|---|---|---|---|
| `snt7_` | **3** | 100% | 维基百科页面浏览量的三个侧面 | 0.7357 / 0.7539 |

本集**只有一个前缀**（不像 `sentiment27` 有 `snl27_` / `snt27_` / `aggregate_` / `ranking_` / `source_` 五族）。`snt7_` 内部按语义再拆两族：

| 子族 | 字段 | 字段数 | 说明 |
|---|---|---|---|
| 浏览量水平（关注度信号主体） | `snt7_all_languages_views`、`snt7_views` | 2 | 同一底层度量的两个聚合度：全语言合计 与 按 project × access type 拆分 |
| 内容时间戳 | `snt7_timestamp` | 1 | 数据记录的内容日期（YYYYMMDD），平台声明为 VECTOR 形态 |

- 两族之间**不是并列的两条腿**，而是**一个度量的两层聚合**：`snt7_all_languages_views` 是 `snt7_views` 在语言维上的合计（数据集描述明写 aggregating across multiple languages）。⇒ 两者**高度同源，只能取一席**；当作两条独立信号腿会重复买同一条信息（另受 AGENTS.md §7.7 混腿禁令约束）。
- 3 个字段全部 `field_group = null`（本地 catalog 实读），平台侧无更细分组。

## 字段全表

|字段 id|type|coverage|userCount|alphaCount|dateCreated|pyramidMultiplier|描述（原文语义；≤120 字）|
|---|---|---:|---:|---:|---:|---:|---|
|`snt7_all_languages_views`|VECTOR|0.7539|40|76|2026-07-01|1.8|公司维基百科页面全语言合计浏览量；本集 coverage 与 alphaCount 双高，已是最拥挤字段|
|`snt7_timestamp`|VECTOR|0.7357|6|6|2026-07-01|1.8|数据记录的内容日期 YYYYMMDD；日期戳，非信号|
|`snt7_views`|VECTOR|0.7357|29|37|2026-07-01|1.8|指定 project 与 access type 下的维基百科日度页面浏览量；向量形态，需 vec_ 算子归约|

## 1. 可用性三分（3 个字段不都能直接进表达式）

### 1.1 信号可用（0 个，0.0%）

**本集没有可直接裸用的标量水平信号。** 两个浏览量字段都是**无界非负计数**（见 §1.2），时间戳是元数据（见 §1.3）。这不是「本集没信号」，而是「本集的信号全部必须先归一化」——归一化之后 §1.2 的两个字段就是本集**全部**的信号主体。

因此任何使用本集的 alpha，**归一化不是可选项而是前置条件**：至少落到 `rank` / `ts_zscore` / 比值 之一，再进入横截面或时序结构。

### 1.2 计数类：需归一化（2 个，66.7%）

两个浏览量字段：`snt7_all_languages_views`（全语言合计）、`snt7_views`（按 project × access type 拆分）。

- **为何必须归一化**：页面浏览量是**无界正计数**，且与公司规模 / 知名度 / 上市年限强相关。裸用等于在做「大公司 vs 小公司」的规模因子，不是「关注度变化」信号。
- **归一化方向（三选一，按假设定）**：
  - 横截面 `group_rank(..., sector|industry|subindustry)` —— 去掉规模与行业维度；
  - 时序 `ts_zscore(..., 22|66)` 或 `ts_delta(..., 5|22)` —— 抓关注度**边际变化**（推荐，因为「关注度水平」的半衰期远短于「关注度变化」）；
  - 比值 `divide(A, ts_mean(A, 252))` —— 相对自身历史基准的关注度，天然消掉公司规模。
- **VECTOR 前置**：两者都是 VECTOR 类型，标量化之前必须过 `vec_avg` / `vec_sum`（`snt7_views` 的向量维是 project × access type；`snt7_all_languages_views` 是语言维聚合）。**不要**把 VECTOR 直接塞进只吃标量的算子。
- ⚠ **同源只取一席**：`snt7_all_languages_views` 与 `snt7_views` 是同一度量的两层聚合，α 高度相关。选一即可；若都要用，只能是「合计 vs 分项一致性」这种结构性差异（如 `divide(vec_avg(snt7_all_languages_views), vec_sum(snt7_views))`，衡量未覆盖语言占比），**不是**两条独立腿。
- ⚠ **零值/稀疏性未知**：本轮为静态画像，未跑回测，平台 coverage 0.7357 只说明「有值覆盖」，**不等于非零覆盖**。若做比值型表达式，分母仍须防零（`trade_when(分母 > 0, ..., -1)` 或先 `ts_backfill`）。

### 1.3 元数据不可用（1 个，33.3%）

| 字段 | 类型 | 为何不可用 |
|---|---|---|
| `snt7_timestamp` | VECTOR | 数据记录的**内容日期**（YYYYMMDD）。平台无「日期字符串 → 可比较量」的通用算子，进表达式只会得到一个近似常数的伪信号；其 `alphaCount=6` / `userCount=6` 说明**已有 6 条 alpha 用过它**——按形态推断多为误用（或仅作 PIT 对齐辅助），**不构成它可用作信号的证据**。 |

用法限于研究期：确定数据的时点对齐（PIT）、估算更新频率与事件去重窗口。**不进候选表达式。**

### 1.4 三分汇总

| 类别 | 字段数 | 占比 | 字段 |
|---|---:|---:|---|
| 信号可用（可裸用） | **0** | 0.0% | — |
| 计数类（归一化后为信号主体） | **2** | 66.7% | `snt7_all_languages_views`、`snt7_views` |
| 元数据不可用 | **1** | 33.3% | `snt7_timestamp` |
| 合计 | **3** | 100% | — |

## 2. 合法模板白名单（静态画像推导，**未回测验证**）

- ✅ `group_rank(ts_zscore(vec_avg(snt7_views), 22|66), sector)` —— 单 project 浏览量的时序标准化再横截面；本项目最标准的关注度形态。
- ✅ `group_rank(ts_delta(vec_avg(snt7_all_languages_views), 5|22), subindustry)` —— 关注度**突变**；浏览量属流量类，**优先差分而非水平**（水平量与公司规模强相关）。
- ✅ `group_rank(divide(vec_avg(snt7_views), ts_mean(vec_avg(snt7_views), 252)), industry)` —— 相对自身年度基准的关注度（前稿「法4 比值>1」曾在 288 个样本上读到 40.3%，但该读数属**单字段抽样实测，本轮未复跑**，只作方向参考，不作容量证据）。
- ✅ `group_rank(divide(vec_avg(snt7_all_languages_views), vec_sum(snt7_views)), sector)` —— 唯一允许两者同用的形态：合计 ÷ 分项 = 未被拆分覆盖的语言份额（**单一经济含义**）。
- ⛔ 排除 `snt7_timestamp`（§1.3）。
- ⛔ 排除裸用水平浏览量（§1.2）。
- ⛔ 排除把两个浏览量字段当两条独立腿（同源同度量，§0.5）。
- ⚠ `pyramidMultiplier=1.8`，按 AGENTS.md §6 木桶倍率律属**中等档**；单集（ATOM）可独立计塔，一旦跨集混入倍率更低的字段，按最低倍率结算。
- ⚠ 与本区 `sentiment27`（Tranco 域名排名）、`sentiment33`（NLP 情绪）**语义正交**，若做跨集只允许 gating / grouping / residual / ratio 四形态（AGENTS.md §7.7），且 PV 类数据集只做单集优先。

## 3. 本任务边界（未做 / 不可在本轮做的部分）

- **本轮零回测、零仿真配额**：全部读数取自平台目录 API（`get_datafields` / `get_datasets`）与本地 `field_catalog` 只读查询，属**静态画像**。
- **未做「六法实测」**（法1 覆盖 / 法2 非零 / 法3 N=5·22·66 / 法4 比值>1）：需要真跑回测，不在本次字段画像任务范围。本档案**不提供逐字段的动态覆盖读数**；`coverage` 列是**平台声明值**，不等于逐日横截面宽度。
- **前稿草稿里的六法读数已移除**：它在 3 个字段里只测了 `snt7_views` 一个（288/500 = 57.6% 等），属**抽样读数**，违反「全字段探测禁止抽样」约束（AGENTS.md §4），且本轮无从复跑，故不保留二手数字。要动态读数须按 3 个字段全量重跑。
- **前稿草稿的「字段全表」表头缺失**（数据行直接顶格、无表头与分隔行），本轮已按标准列序重建，并补齐聚合统计 / 字段族拆解 / 可用性三分三节。
- **未验证**：平台未给出字段的非零率、更新频率与逐日截面宽度；`snt7_views` 的向量维度（project / access type 的实际卡氏积大小）也未实读。这些只能靠回测或 Labs 数据探针取得。

## 4. 平台实况与「第 3 席」目标（2026-11-23 实读，**本节是回测证据，覆盖前 3 节的静态推断**）

### 4.1 SENTIMENT 塔在 DEU = **2/3**，两席机制均 prod-clean

| 席位 | 件 | 机制 | S | F | 2Y | TO | prod | self | 提交日 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `bl6OWZ2M`（`DEU_R_alpha_01`） | **snt7 注意力 IR 水平** | 2.03 | 1.61 | 2.54 | 16.1% | **0.6671** | 0.0306 | 2026-11-04 |
| 2 | `vRAvXvZb`（`DEU_R_snl27kurt_01`） | snl27 kurtosis / totaldomains^2.25 | 1.63 | 1.02 | 2.31 | 20.2% | **0.5614** | 0.3276 | 2026-11-18 |

`bl6OWZ2M` 逐字代码（**这是必须去相关的母件**）：
```
a = ts_backfill(vec_avg(snt7_all_languages_views), 22);
vector_neut(ts_quantile(ts_ir(ts_mean(max(a, ts_delay(a, 5)), 5), 22), 252, driver="gaussian"),
            ts_backfill(vec_avg(snl27_relpopularity08), 22))   @ SUBINDUSTRY / d2 / trunc 0.02
```
**⇒ 3/3 只差 1 颗，且两个已有机制的 prod 余量都很大（0.56 / 0.67）。这是全场最便宜的一席。**

### 4.2 卡点 = self-corr，不是 prod

`kqNRX1ZP`（本地 READY 库存件，S **2.06** / F 1.86 / 2Y 2.37 / sub 1.49 / RN 1.63 / **RA fail 列表为空**、连 `CLUSTER_TEST` 都 pass）
实为 `bl6OWZ2M` 的**近重复变体**（同 snt7→ts_ir→quantile 核，只多一重 `snl27_totaldomains` 正交化 + 窗 120 vs 252）：

**self-corr = 0.7936 FAIL**（对其余 21 颗 OS 件全部 ≤ 0.14）⇒ 单件近重复，非整族同质。

**⇒ 结论：`snt7` 的「水平 + ts_ir + ts_quantile」抽取被 `bl6OWZ2M` 占满，同抽取的任何窗口/正交基/decay 变体都过不了 0.70。
第 3 席必须换抽取或换机制。**

### 4.3 本轮去相关探针（批 `3uM07agUm59GbGM1eS4A4XL5`，3 臂，SUBINDUSTRY / d2 / trunc 0.02，对齐母件）

| 臂 | 机制 | 表达式核心 | 依据 |
|---|---|---|---|
| **S1** | 尾部注意力水平（**换归约**） | `vec_max` 替代 `vec_avg`，其余同母件 | `vec_*` 归约是独立算子类别轴（max > avg > min，sum≡avg）；母件只用过 avg |
| **S2** | 注意力**扩散度**（换机制） | `divide(vec_max(snt7_views), vec_avg(snt7_views))` | 语言/项目维度的注意力集中度 ≠ 水平；Da/Engelberg/Gao 2011 `10.1111/j.1540-6261.2010.01628.x`（注意力配置） |
| **S3** | 注意力**变化率**（换机制） | `ts_delta(vec_avg(all_languages_views), 66)` | Moat et al. 2013 `10.1038/srep01801`（浏览量→交易量，变化而非水平）；本档 §2 也优先差分 |

**验收判据（事前写定）**：S ≥ 1.58 且 self-corr < 0.70（对 `bl6OWZ2M` 与 `vRAvXvZb`）⇒ 即 SENTIMENT 第 3 席 → 塔点亮。
若三臂 S 全 < 1.2，则回到 §2 白名单里**尚未回测**的「语言份额」形态
`group_rank(divide(vec_avg(all_languages_views), vec_sum(snt7_views)), sector)`（单一经济含义，且天然与水平抽取正交）。

### ★ 4.4 探针结果：三臂全灭，且否证「vec_max > vec_avg」（2026-11-23 21:5x）

| 臂 | 机制 | id | S | F | 2Y | TO | sub | RA |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 母件 | level + ts_ir + quantile（`vec_avg`） | `bl6OWZ2M` | **2.03** | **1.61** | **2.54** | 16.1% | 1.20 | 0 |
| S1 | 换 `vec_max` 归约 | `O0WL7jLv` | 1.41 | 0.94 | 1.36 | 16.2% | 0.59 | 4（+`IS_LADDER` 第4年 1.36<1.58） |
| S2 | 扩散度 `vec_max/vec_avg` | `gJalj5lm` | 0.79 | 0.18 | 0.25 | **66.9%** | 0.01 | 4 |
| S3 | 变化率 `ts_delta(·,66)` | `Jj8A7kAx` | 0.31 | 0.05 | −0.68 | **50.5%** | 0.12 | 4 |

**三条结论**

1. **★★ `vec_max` 在 snt7 上比 `vec_avg` 差 0.62**（2.03 → 1.41，且新增 `IS_LADDER_SHARPE` 第 4 年失败）
   ⇒ **「vec_max > vec_avg」不是通用律**，`vec_*` 归约的选择与「杠杆跨核不可移植」同类，必须逐核实测。
   （对照：`vector-fold-is-its-own-operator-category` 的 max>avg 结论来自全 VECTOR 的 KOR 数据集；
   此处 snt7 的向量维度是「语言 × 访问类型」，`max` 取到的是**最热单一语言页**这一噪声最大的分量。）
2. **比值型 TO 66.9% / 差分型 TO 50.5%** ⇒ 两者都是**结构型 TO 死因**（`divide(A,B)` 当 A、B 同源同流量时，
   比值逐日重排；`ts_delta` 在日更计数上是纯噪声）。snt7 是低流量日更计数，任何分子分母同源的重排都会炸换手。
3. **★★ snt7 的信号形态是特定的**：只有「水平 + ts_ir + ts_quantile」能到 2.03，换归约/比值/差分全塌到 0.31–1.41。
   `signal-form-specificity-test` 第 3 次复现（前两次：GBR institutions1、EUR insider）。

**⇒ SENTIMENT 第 3 席在 snt7 上结构性关闭。** 唯一未试的 §2 白名单形态是「语言份额」
`divide(vec_avg(all_languages_views), vec_sum(snt7_views))` —— 但它同样是同源比值，
按本档结论 2 的 TO 死因，预期不高；若要真攻该席，应换数据集（sentiment33 NLP 面）而非继续挤 snt7。
