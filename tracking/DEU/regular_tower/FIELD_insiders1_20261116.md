# DEU / D1 / TOP500 — `insiders1` 字段档案（S1）

> 生成：2026-11-16｜口径：`region=DEU, universe=TOP500, delay=1, instrumentType=EQUITY`
> 数据源：**平台实读**——`get_datafields`(×7：全量 / `MATRIX` / dataset 级 `GROUP` / 默认 `filter_sharpe` /
> 全区 `GROUP` 列表 / `GROUP`+`search=subindustry` / `GROUP`+`search=sector`)、
> `get_datasets`、`get_operators`、`get_documentation_page(vector-datafields)`、`preflight_expressions`(×2)，
> 以及**本轮 20 条探针仿真的真实指标**（2 个 multisim，各 10 臂）。本地 `get_field_catalog` 只作对照，不作依据。
> 塔位：`get_datasets` 与 `harvest` 双读 `DEU/D1/INSIDERS`（`pyramidMultiplier=1.6`，`effective=1`）。

---

## 0. 一句话结论

`insiders1` 在 DEU/TOP500/D1 实读 **8 个字段、全部 VECTOR、coverage 全为 0.5343**（8 个值逐位相同 ⇒ 该列在本集
**不携带字段级信息**）。它是**逐笔申报的事件流**：同日只有 **12/500（2.4%）** 的股票有记录，
但**有记录时向量宽度普遍 ≥2**（12 只里有 8 只 ≥2 条、6 只 ≥2 个不同金额）——
所以塌缩发生在**截面**而不是向量内部。**数值本身不带买卖方向**（20 条探针的 `shortCount` 全为 0，
连同 `vec_min(valueeur)` / `vec_min(value)` 也是 0，实证无负值）。裸 `vec_*` 的换手 **1.62–1.79**
（硬线 0.7），而加 250 日回填后降到 **0.011–0.034** ⇒ **时间平滑是本集的入场条件，不是优化项**。

---

## 1. 平台字段全表（平台实读，8/8 无截断）

`get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false)`
→ `count=8, platform_count=8, complete=true, pages_fetched=1`。
默认口径（`filter_sharpe` 缺省）再读一次：同样 8 条，且返回 **`sharpe_filter_applied=false, sharpe_filter_removed=0`**
⇒ 本区**没有做 Sharpe 预筛**，平台不为这 8 个字段的 IS 表现背书（不是"筛过都合格"）。

| # | 字段 | type | coverage | userCount | alphaCount | description（语义唯一依据） |
|---|---|---|---|---|---:|---:|---|
| 1 | `insd1_holdings` | VECTOR | 0.5343 | 11 | 13 | Total equity share holdings of the insider **after the transaction** |
| 2 | `insd1_valueeur` | VECTOR | 0.5343 | 10 | 12 | Total value of the transaction **in Euro** |
| 3 | `insd1_tradesignificance` | VECTOR | 0.5343 | 7 | 9 | Significance score of the trade (**1 = low significance, 3 = high significance**) |
| 4 | `insd1_shares` | VECTOR | 0.5343 | 4 | 5 | **Number of shares** (or units) traded in the transaction |
| 5 | `insd1_price` | VECTOR | 0.5343 | 3 | 4 | Transaction **price per share**; 若报区间则取**最小值** |
| 6 | `insd1_value` | VECTOR | 0.5343 | 2 | 2 | Total value of the transaction **in original currency** |
| 7 | `insd1_gvkey` | VECTOR | 0.5343 | 1 | 1 | Compustat Global Company Identifier（**标识符**） |
| 8 | `transaction_currency_code` | VECTOR | 0.5343 | 1 | 1 | Three-letter **ISO currency code**（**分类标签**） |

**幽灵字段 = 0。** 本地 `get_field_catalog("DEU","insiders1")` 也返回 8 条、id 集合与平台**逐 id 相同**
（唯一失真：本地把数据集 `data_type` 标成 `MATRIX`，而 8/8 实为 VECTOR；且本地 `userCount/alphaCount`
全部记成 ≤1，已过期）。⇒ 本集**没有本地画像幽灵字段问题**，本条已按平台实返回核对，不依赖本地。

**数据集级元数据两处不可信（实读证据）**：
1. `get_datasets(search="insider")` 给 `insiders1` 的 description 是「**RIC ↔ BBID 标识符交叉映射**」，
   与「Global Insider Trading Data」的字段语义完全无关 ⇒ **平台侧元数据串台**，语义只认字段 description
   （同类错配在 EUR/IND 各有一份独立记述：`docs/reference/EUR/insiders_field_profile_20261107.md:40`、
   `docs/reference/field_profile_ind_inst_fund_20261019.md:228`）。
2. 同一调用的拥挤度今日读作 **userCount=23 / alphaCount=38**，而 `FIELD_insiders1_20261115.md:239-240` 前一日记
   20/29 ⇒ 一天内 +3 人/+9 颗，属**低拥挤但在动**（本地 catalog 的 1/1 更不能当准）。

---

## 2. 类型与降维要求

- **8/8 VECTOR，无 MATRIX / EVENT / GROUP。** 实读：同入参加 `data_type="MATRIX"` → `count=0, platform_count=0,
  complete=true`；加 `data_type="GROUP"` → 同样 `0/0`。⇒ 本档**不涉及** EVENT 的 `ts_event_*` 支撑问题，
  也不存在 GROUP 轴字段；`insd1_gvkey` 虽像分组键但类型是 VECTOR，**不能**直接当 group 用。
- **VECTOR 的语义（平台文档实读，`vector-datafields`）**：向量字段「每天每标的不定长，记录**当天**发生的事件条数」，
  所有矩阵算子必须先过 `vec_*` 聚合。⇒ 本集一个格 = 某股某日的**全部申报记录**，不是滚动窗口。
- **可用的 `vec_*` 只有 7 个**（`get_operators` 实读、共 103 算子）：
  `vec_avg / vec_sum / vec_max / vec_min / vec_stddev / vec_range / vec_count`。
  ⚠ 平台**文档页**还列了 `vec_ir / vec_kurtosis / vec_skewness / vec_norm / vec_percentage / vec_powersum / vec_choose`，
  但这些**不在 `get_operators` 返回里** ⇒ 以平台算子表为准，**别照抄文档页写**（本仓 `tools/lib/vector_wrap.py:26`
  的 `VEC_WRAP_OPS` 也含 `vec_ir` 等，属同一类"文档集"口径，实际派发前须过 `preflight`/平台校验）。
- **空向量语义（本轮实证，独立复现前一日结论）**：裸 `vec_sum(insd1_valueeur)` 的 `longCount=11`（不是 500），
  `vec_avg(insd1_holdings)` 的 `lc=9` ⇒ **当日无交易时聚合返回 NaN，不是 0**。因此
  `ts_backfill(vec_*(x), 250)` 是必需项，否则截面只剩个位数股票。
- **降维基线**：`vec_*` → `ts_backfill` → 时序/截面算子，**禁止裸用字段**（
  `tools/probe/dataset_data_probe.py:127` 的 VECTOR 口径）。

---

## 3. 语义维度（按 description 归纳；字段名不作依据）

| 维度 | 代表字段 | 经济含义（据 description） |
|---|---|---|
| **内部人持股存量（状态量）** | `insd1_holdings` | 交易后内部人持股总数 = **stock**，不是流量。跨笔求和 = 公司层面内部人合计持股。 |
| **交易金额（规模，可跨市场比）** | `insd1_valueeur` | 每笔交易总价值（欧元计价）。 |
| **交易金额（规模，原币）** | `insd1_value` | 与 `valueeur` **语义同一、仅计价币种不同** ⇒ **互替而非互补**，同用即重复计规模。 |
| **交易股数（规模，另一口径）** | `insd1_shares` | 本次成交股数；金额 ≈ 股数×价 ⇒ 与金额高度共线。 |
| **成交价快照** | `insd1_price` | 每股成交价（区间取下限）；**不是收盘价**，只有与收盘价比才有"内部人成交折溢价"含义。 |
| **交易重要性（序数）** | `insd1_tradesignificance` | 平台自评 1–3 序数。**序数≠基数**：可作加权，不可解释成"重要性金额"。 |
| **事件条数（派生，无原生字段）** | `vec_count(任一字段)` | 当日该股的申报记录条数 = 广度/事件强度。**5 个字段的 `vec_count` 指标逐位相同**（见 §4.2）⇒ 是**一条**轴。 |
| **日内金额离散（派生）** | `vec_max - vec_min` / `vec_stddev` / `vec_range` | 同日多笔交易的规模离散度/集中度；只在宽度≥2 时有定义。 |
| **标识符（元数据）** | `insd1_gvkey` | Compustat 公司码 ⇒ **非信号**（同股常数，无截面排序含义）。 |
| **分类标签（元数据）** | `transaction_currency_code` | ISO 币种码 ⇒ **非信号**（求均值/求和无经济含义）。 |

**★ 结构性缺口（本集最重要的一条，本轮已实证而非推断）**：8 个字段里**没有任何买卖方向字段**，
且**数值符号也不携带方向**——`vec_min(valueeur)`、`vec_min(value)`、`vec_sum(valueeur)` 三条探针
在 2014–2023 全期 **`shortCount` 全为 0**（详见 §4.5）。
⇒ 方向只能由 `insd1_holdings` 的**时间差分**推断（同期增持=正、减持=负），或做**双向对照臂**定号。

---

## 4. 字段级覆盖实读

### 4.1 `coverage` 在本集不携带字段级信息

8 个字段的 `coverage` **全部 0.5343**，且与数据集级 `coverage`（`get_datasets` 的 0.5343）逐位相同
⇒ 这一列在本集是**数据集级值复制到每个字段**，无法区分字段。**不得用它判字段可用性、更不得用它判数据集可用性**。
反证：同区 `subindustry` / `sector` 两个 GROUP 字段 `coverage=0.0`，却有 692 / 961 个用户、
5327 / 6629 颗 alpha（本轮 `get_datafields(data_type="GROUP", search=...)` 实读）
⇒ **coverage=0 不代表没数据**，只是这个投影字段没填。

### 4.2 20 条探针总表（平台真读数）

统一设置：`DEU/TOP500/D1`、`neutralization=NONE`、`decay=0`、`truncation=0.0`、`nanHandling=OFF`、
`pasteurization=ON`，样本 `2014-01-01 ~ 2023-12-31`。`rank()` 恒正 ⇒ `longCount` = 该口径下有值的股票数
（读法出处 `tools/probe/dataset_data_probe.py:17-20`）。**全部 20 条 `shortCount=0`。**

| # | 表达式 | alpha | longCount | turnover | S | F | 2Y | sub |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `vec_count(insd1_valueeur)` | `P05wnQRW` | 12 | 1.6711 | 0.70 | 0.31 | −0.53 | −0.30 |
| 2 | `vec_count(insd1_value)` | `kqa1nEwL` | 12 | 1.6711 | 0.70 | 0.31 | −0.53 | −0.30 |
| 3 | `vec_count(insd1_price)` | `zqdP5Kx8` | 12 | 1.6711 | 0.70 | 0.31 | −0.53 | −0.30 |
| 4 | `vec_count(insd1_shares)` | `RRe2NjOz` | 12 | 1.6711 | 0.70 | 0.31 | −0.53 | −0.30 |
| 5 | `vec_count(insd1_holdings)` | `ZYa2jP88` | **9** | 1.6345 | 0.68 | 0.32 | −0.54 | −0.26 |
| 6 | `vec_count(insd1_tradesignificance)` | `P05wnQVW` | 12 | 1.6711 | 0.70 | 0.31 | −0.53 | −0.30 |
| 7 | `vec_count(transaction_currency_code)` | `leaQ7pm2` | 12 | 1.6721 | 0.68 | 0.30 | −0.53 | −0.30 |
| 8 | `greater(vec_count(insd1_valueeur),1)` | `blaoNGwq` | **8** | 1.6610 | 0.88 | 0.43 | −0.48 | −0.06 |
| 9 | `rank(ts_backfill(vec_sum(insd1_valueeur),250))` | `A1xgnjAQ` | **294** | **0.0299** | 0.75 | 1.01 | −0.07 | −0.91 |
| 10 | `rank(vec_stddev(insd1_valueeur))` | `vRAe5wQQ` | **7** | 1.6800 | 0.72 | 0.34 | −0.56 | −0.05 |
| 11 | `vec_min(insd1_valueeur)` | `YPa2N57l` | 10 | 1.7875 | 0.25 | 0.08 | −0.68 | 0.03 |
| 12 | `vec_max(insd1_valueeur)` | `zqdP5YYK` | 11 | 1.7161 | 0.31 | 0.11 | −0.57 | −0.27 |
| 13 | `vec_min(insd1_value)` | `1YWaoxxm` | 10 | 1.7893 | 0.21 | 0.07 | −0.65 | −0.03 |
| 14 | `vec_sum(insd1_valueeur)` | `WjlaNPPP` | 11 | 1.7183 | 0.29 | 0.10 | −0.72 | −0.23 |
| 15 | `subtract(vec_max(insd1_valueeur),vec_min(insd1_valueeur))` | `leaQ7885` | **6** | 1.7016 | 0.39 | 0.16 | −0.63 | −0.13 |
| 16 | `vec_avg(insd1_tradesignificance)` | `qM7PnWxK` | 12 | 1.6240 | **0.91** | 0.43 | **−0.03** | **0.24** |
| 17 | `vec_avg(insd1_holdings)` | `9qla9VjK` | 9 | 1.6224 | 0.58 | 0.27 | **+0.62** | 0.20 |
| 18 | `rank(ts_backfill(vec_count(insd1_shares),250))` | `RRe2NVb1` | **294** | 0.0337 | 0.76 | 1.04 | −0.01 | −0.19 |
| 19 | `rank(ts_count_nans(vec_avg(insd1_valueeur),250))` | `88NaO3jV` | **382** | 0.0107 | 0.74 | 0.99 | −0.23 | −0.07 |
| 20 | `rank(days_from_last_change(ts_backfill(vec_sum(insd1_valueeur),250)))` | `Jj8gnxNA` | **383** | 0.0296 | 0.74 | 0.98 | −0.21 | 0.02 |

（#1–10 来自 multisim `4kBt8k45F4YZacG18Glz3gZm`；#11–20 来自 `ec3kSdW54EIc0eGE7BdkHt`。两批均
`child_count=10 / terminal=10 / errors=0`，`harvest_multisim_alphas` 回读 `complete=10, error_count=0`。）

**三条由 #1–#7 直接读出的结构事实**：
1. **`vec_count` 对 5 个字段给出逐位相同的指标**（`12 / 1.6711 / 0.70 / 0.31`）⇒ 这些字段在**同一批申报记录上逐行对齐**，
   "条数"是**一条**轴，不是 5 条；用哪一列做 `vec_count` 都不产生新信息。
2. **`insd1_holdings` 是唯一有缺口的一列**：`vec_count(holdings)` 的 lc=**9** vs 其余 **12**
   ⇒ 约 **25% 的申报记录没有交易后持股**（与 §4.4 的 250 日宽度更低同向）。
3. **`transaction_currency_code` 可以被 `vec_count` 正常归约**（lc=12、无报错；TO 1.6721 / S 0.68 与其余字段
   几乎同值但不逐位相同）—— 它**不是**"技术上不可用"，只是作为分类标签**无信号语义**（见 §7）。

### 4.3 宽度塌缩：**截面塌缩 ≠ 向量宽度塌缩**（本轮新增的关键区分）

| 口径 | 读数 | 占 TOP500 |
|---|---:|---:|
| 同一天**有任一申报**的股票数（#1–#4、#6、#7） | **12** | **2.4%** |
| 同一天**宽度 ≥2**（`greater(vec_count,1)`，#8） | **8** | 1.6%（占事件股 **8/12 = 67%**） |
| 同一天**宽度 ≥2 且金额不同**（`vec_range`，#15） | **6** | 1.2%（占事件股 50%） |
| 同日标准差可算（`vec_stddev`，#10） | **7** | 1.4% |
| 250 日回填后有值（`vec_sum`，#9 / `vec_count`，#18） | **294** | **58.8%** |
| 样本期内**曾**有值（`ts_count_nans`，#19 / `days_from_last_change`，#20） | **382 / 383** | **76.6%** |

结论三条：
1. **截面塌缩到 2.4%**：任何不做时间平滑的 insiders1 表达式，截面只有 10–12 只股票 ⇒ 那不是"弱信号"，
   是**没有截面**。**≥60 日平滑 + ≥250 日回填是入场条件**。
2. **向量内部并未塌缩到 1**：有申报的股票里 **2/3 当天有 ≥2 条记录**、一半有 ≥2 个不同金额
   ⇒ `vec_max ÷ vec_sum` / `vec_range` / `vec_stddev` 这类"日内结构"机制**在本集是有原料的**
   （与"VECTOR 退化成 MATRIX"的担心相反）。但它们的**截面只有 6–8 只**，是全表最窄的一族。
3. **约 1/4 的 TOP500 十年内一次申报都没有**（383/500 曾覆盖）⇒ 任何依赖 `nanHandling ON` 把缺失填 0 的用法，
   都会把 117 只股票变成**长期空头**，alpha 内容被替换成"有没有内部人"这个规模/流动性代理
   （同一机理在 EUR 侧已有记述：`docs/reference/EUR/insiders_field_profile_20261107.md:49-51`）。

### 4.4 更新频率

- **平台 MCP 面不暴露"声明频率"**：`get_datafields` 的投影只留 `id / type / coverage / userCount / alphaCount /
  description` 六键（`world-quant-brain-mcp/mcp_core.py:341-343`，且 description 截断 160 字符——
  本集最长 78 字符，**未被截断**，可全信）⇒ 频率属性 **NOT_MEASURED**，本档不猜。
- **从 description 可定性为事件驱动**：每条记录是"该笔交易"的股数/金额/价格/重要性，不是日/周/月预聚合快照。
- **本轮新增的量级读数**（三档，全是平台实读，见 §4.2）：
  - 日频触达 **2.4%**（12/500）；
  - 滚动 250 日触达 **58.8%**（294/500）；
  - 十年内曾触达 **76.6%**（383/500）。
  - 由前两条可做**算术派生**（标注为派生，非平台读数）：12 只/日 × 250 交易日 ÷ 383 只曾覆盖 ≈ **7.8 个申报日/股/年**
    ⇒ 中位覆盖股大约 **每 32 个交易日一次申报**。
- **未测**：每股更新的**实际间隔分布**。`ts_count_nans` / `days_from_last_change` 的取值本身不在平台指标里，
  只能读到"有多少只股票有值"（#19/#20），读不到间隔数值 ⇒ 本档不给分布，只给上面三档触达率。

### 4.5 方向：**数值不带符号**（本轮实证，替代此前的"据文档推断"）

`vec_min(insd1_valueeur)`(#11)、`vec_min(insd1_value)`(#13)、`vec_sum(insd1_valueeur)`(#14)
三条探针的 alpha 值**就是交易金额本身**；若存在负值（把卖出记成负数），这些股票的权重会是负的、
`shortCount` 必然 >0。实读 **`shortCount=0`（20/20 条臂全为 0）** ⇒
**2014–2023 全样本内 `value` / `valueeur` 没有出现过负值**，`shares` 同理（#4 的计数与方向无关）。
同时 `vec_avg(insd1_tradesignificance)`(#16) 也只有多头，与"1–3 正序数"一致。

⇒ 结论：**买卖方向既不在字段里，也不在数值符号里**。设计上只有三条路：
① 用 `insd1_holdings` 的差分定号；② 同波强制带**反号对照臂**；③ 干脆做**无方向**的强度/集中度/新鲜度机制。
（这条实证回答了 `docs/reference/EUR/insiders_field_profile_20261107.md:53,:69` 留的两个未知项 ③⑤。）

### 4.6 换手：平滑不是优化，是入场

裸 `vec_*` 族换手 **1.62–1.79**（#1–#7、#11–#17），全部超 0.7 硬线 2 倍以上；
同一字段加 250 日回填后 **0.0107–0.0337**（#9、#18、#19、#20）——**相差两个数量级（48–167 倍）**。
⇒ 任何"裸 `vec_*` + 短窗"的写法在 DEU 都会被 `HIGH_TURNOVER` 直接拒（EUR 侧同形实证：
`Claude/skills/wq-brain-ra-eur/references/insiders.md:50` 记 wave496 八条 `vec_avg` 探针 S≤0.50 且
TO=1.52–1.61；`docs/reference/EUR/analyst_campaign_20261013.md:177` 同数）。
⚠ 但注意：#9/#19/#20 的低换手来自**几乎不动的长窗回填**（TO≈1%，S≈0.74、sub≈−0.9~0.0），
属"低换手 = 低信息"的另一端，不是好结果——**换手达标不等于信号有效**。

---

## 5. 结构性约束（写模板前必须知道）

- **ATOM 口径**：本集所有字段同属一个 dataset ⇒ 单集表达式即 ATOM，免 IS_LADDER（
  `Claude/skills/wq-brain-ra-deu/references/_basket-and-atom.md:44-53`）。`insiders1` 与
  `insider_agg_matrix` / `insider_matrix` / `insider_trx_matrix` 是**不同** dataset，混用即掉出 ATOM。
- **闸5（等权腿相加）**：判定器 `_find_equal_weight_leg_add` / `_detect_equal_weight_leg_add`
  （`Claude/skills/wq-brain-campaign-toolkit/scripts/_gate_expr_checks.py:803,:826`）。
  ⚠ **口径已变（2026-11-12 同源豁免）**：命中的 `add()` 若所有腿引用**同一数据集**，不再判 POISON，
  降为 warning `[SAME_DATASET_LEG_ADD]`（`:469-479`）。但 DEU 区域 skill 仍写"跨字段 `add(A,B)` = POISON"
  （`_basket-and-atom.md:81-89`）⇒ **两处口径不一致**，本档**全部模板只用单腿**，不依赖任一方。
- **合法空间（闸5 明确放行）**：同形态不同窗 `add(ts_mean(x,22), ts_mean(x,66))`；单腿 + 标量；
  `subtract(rank(A), rank(B))` 仅限同源且有单一经济含义。
- **中性化**：DEU S0 记录「主腿必须 FAST，SUBINDUSTRY 已三波证死」（`S0_TOWER_SCAN_20261115.md:237`）。
  模板里的 `group_rank(x, subindustry)` 是**信号内分组轴**，与中性化设置两件事，不冲突。
  `subindustry` / `sector` 在 DEU/TOP500 **实读存在**（GROUP，userCount 692/961），可放心用。
- **方向**：无方向字段 ⇒ 任何"增持/减持"语义的模板必须同波带**反号对照臂**。
- **缺失处理**：`nanHandling=OFF` 是探针口径；实盘骨架若要 ON，须先按 §4.3 第 3 条评估"把 117 只无申报股票
  做成空头"的后果。

---

## 6. 模板骨架（10 个不同机制，非换窗口）

统一约定：全部**单表达式、单数据集（ATOM）、单腿**；先 `vec_*` 降维；需要跨日延续的先 `ts_backfill`，
再进时序/截面算子（M3/M4/M10 这类 `ts_sum`/`ts_rank` 聚合天然只加有事件的日子，可不回填）。
「先验」分级：**A** = DEU 已有实测支持；**B** = 跨区/文献先验、DEU 未测；**C** = 构成件在 DEU 已判死，只有新几何才值得一试；
**N** = 本轮新提出的几何（无任何回测）。
**本表 10 条全部未回测**，S/F/2Y/sub 均未知。

| # | 机制（差在哪） | 骨架 | 预期符号 | 先验 |
|---|---|---|---|---|
| **M1** | **存量水平**（状态量高低，不是变化） | `group_rank(ts_backfill(vec_sum(insd1_holdings),250), subindustry)` | **双向**：alignment 给正、entrenchment 给负 ⇒ 必须成对跑 | B（DEU 未单测"水平+组内秩"） |
| **M2** | **净增持流**（一阶差分） | `group_rank(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66), subindustry)` | **正**（净增持；Lakonishok-Lee 2001，变化 > 水平） | **A**：DEU「A 单腿 Δ66」S 1.72（`deu-insiders-evidence.md:31`）；holdings 为该战役唯一强腿（`:51`） |
| **M3** | **事件广度**（申报条数强度，与规模正交） | `group_rank(ts_sum(vec_count(insd1_shares),66), subindustry)` | **双向**：条数多=信息多（正）但也可能是坏消息集中申报（负） | **N**：本轮 #18 证 250 日 count 有截面（lc=294、TO 3.4%）⇒ 轴存在；方向未定 |
| **M4** | **单笔均额的位置**（规模在自身一年历史中的秩） | `group_rank(ts_rank(divide(ts_sum(vec_sum(insd1_valueeur),66), ts_sum(vec_count(insd1_valueeur),66)),252), subindustry)` | **正**（Seyhun 1986：单笔越大越可能是信息交易者） | C（`valueeur` 单腿 1.14 已判死；比值+时序位置是新几何） |
| **M5** | **日内集中度**（最大单笔占当日总额） | `group_rank(ts_mean(divide(vec_max(insd1_valueeur), vec_sum(insd1_valueeur)),66), subindustry)` | **正**（单笔支配=信念集中） | **C/N**：机制在姊妹集最强（HHI 集中度 S 1.74–2.20，`deu-insiders-evidence.md:28-32`）；但本集原生版本的截面只有 **6–8 只/日**（§4.2 #15），宽度风险最高 |
| **M6** | **增持的信噪比**（持续增持 vs 一次性脉冲） | `group_rank(ts_ir(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),22),252), subindustry)` | **正**（持续买入=更强信念；Cohen-Malloy-Pomorski 2012 的 routine/opportunistic） | **A**：DEU「B 单腿 ts_ir」S 1.81（`deu-insiders-evidence.md:29`） |
| **M7** | **事件新鲜度**（距上次申报的天数） | `group_rank(subtract(250, days_from_last_change(ts_backfill(vec_sum(insd1_valueeur),250))), subindustry)` | **正**（越近的事件信息越未衰减） | **N**：本轮 #20 证该轴有 383 只宽截面、TO 3.0% ⇒ 可测；符号是假设、未验证 |
| **M8** | **规模正交化**（剥离"交易活跃度"后的增持残差） | `vector_neut(group_rank(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66), subindustry), rank(ts_backfill(vec_sum(insd1_valueeur),250)))` | **正**（残差=与规模无关的增持信息） | **N**（DEU 未做过 insiders1 侧的正交化） |
| **M9** | **条件持有**（只在净增持期暴露，否则退出） | `trade_when(greater(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66),0), group_rank(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66), subindustry), -1)` | **正偏态**（事件门控 ⇒ 收益右偏、换手下降） | B（DEU 未测 trade_when） |
| **M10** | **序数显著性加权**（金额 × 平台自评重要性 1–3） | `group_rank(ts_sum(multiply(ts_backfill(vec_sum(insd1_valueeur),250), ts_backfill(vec_avg(insd1_tradesignificance),250)),66), subindustry)` | **正**（大且"重要"的交易更有信息） | C（两构成件单独均判死：`valueeur` 1.14、`tradesignificance` 1.21；只有交互几何未测） |

**为什么这 10 条算不同机制**：M1 水平 / M2 一阶差分 / M3 条数（广度）/ M4 单笔规模的位置 / M5 日内集中度 /
M6 差分序列的信噪比 / M7 时间距离 / M8 正交化残差 / M9 条件门控（状态机）/ M10 序数加权。
M1/M2/M6/M8/M9 都基于 holdings，但分别读**水平 / 变化 / 变化的稳定性 / 变化的残差 / 变化的条件暴露**——五种不同的量。
**M3 只写一条**：因 §4.2 证 5 个字段的 `vec_count` 逐位相同，写多条只是换字段名，不是换机制。

**已判死、不要重跑的（DEU 实测，`deu-insiders-evidence.md:54-61`）**：
`insd1_valueeur` / `insd1_value` 单腿（1.14）、`insd1_shares ÷ insd1_holdings`（1.29）、
`insd1_tradesignificance` 单腿（1.21）、`insd1_price`（1.13）；GBR 侧独立复现显著性零信号
（`Claude/skills/wq-brain-ra-gbr/references/insiders.md:101-112`：S 0.06 / 2Y −0.32）。
本轮 #16 给 `vec_avg(tradesignificance)` 裸基线 S 0.91（全表最高），但 **S 0.91 < 1.58 且 2Y −0.03**，
**不构成对该判死的反驳**——它仍是不过闸的裸基线，只是"同族里最不差"。

**⚠ 跨区结论冲突，必须按"几何"分层读（否则会误用 EUR 的判死）**：
EUR 侧对 `insiders1` 有**整集判死**记录（`Claude/skills/wq-brain-ra-eur/references/insiders.md:50`：
wave496 八条 `vec_avg` 探针 S≤0.50、TO 1.52–1.61 ⇒ 判死），而 DEU 侧「Δ66 holdings」单腿实测 S 1.72
（`deu-insiders-evidence.md:31`）。两者**不矛盾**：EUR 判死的是**裸 `vec_avg` 短窗几何**（与本档 #1–#16 的
TO 1.62–1.79 完全同形），DEU 存活的是**长窗回填 + 66 日差分**几何（本档 #9/#18/#19/#20 的 TO 1–3% 同形）。
⇒ **不得**用"EUR 判死 insiders1"去否决 DEU 的长窗 holdings 族；反过来也**不得**用 DEU 的 1.72 去复活
"裸 vec_avg 探针"那条路。判死必须写明是**哪套几何**在哪个区（`AGENTS.md` §7.6 D6 配置维）。

---

## 7. 不可用 / 非信号字段清单

| 字段 | 状态 | 依据 |
|---|---|---|
| `insd1_gvkey` | **非信号（标识符）** | description 为 Compustat 公司码；同股常数，无截面排序含义。⚠ 本轮**未探** `vec_count(gvkey)`（不测就不写"可归约"），但作为标识符它不构成信号代数的一部分。 |
| `transaction_currency_code` | **非信号（分类标签）** | ISO 币种码；本轮实证可被 `vec_count` 归约（lc=12、无报错），但求均值/求和无经济含义。做"币种条数"只会复刻 §4.2 的同一根 count 轴。 |
| `insd1_value` | **语义重复（非阻塞）** | 与 `insd1_valueeur` 同为"交易总额"，仅币种不同 ⇒ 同用即重复计规模；DEU 内建议统一用 `valueeur`（跨市场可比）。 |

**幽灵字段：0 条**（平台 8 条 = 本地 catalog 8 条，逐 id 一致）。**EVENT 字段：0 条**（无需 `ts_event_*` 探针）。

---

## 8. 与既有 DEU 工作的重叠矩阵（避免把旧机制记成新机制）

对照 `tracking/DEU/atom_orthogonal/waveBA6_insiders1_pool_design_20261110.md:18-29` 与
`FIELD_insiders1_20261115.md:197-215`（前一日档案的 BA6 重叠矩阵）：

| 已知设计 | 与本档关系 |
|---|---|
| BA6 I1（Δ66 holdings，`vec_avg`+132 回填） | ≈ **M2**（本档 `vec_sum`+250 回填）⇒ 同机制、不同聚合口径，**不是新模板** |
| BA6 I2（I1 反号） | 本档未单列，但 M1/M3 明确要求成对反号臂 |
| BA6 I3 / I4（valueeur 强度 / significance 水平） | 本档不单列（均已判死） |
| BA6 I5（增持 × 显著性） | ≈ **M10** 的变体（本档是金额 × 显著性） |
| BA6 I6（平均单笔金额 ts_mean 22） | ≈ **M4**（本档改成"比值 + 252 日时序秩"，形状不同） |
| BA6 I7（holdings ts_rank 252） | 与 **M1** 同用水平信息，但 M1 是组内秩、I7 是时序秩 ⇒ 可并存 |
| BA6 I8（`vec_count(shares)` 条数/广度） | **= M3**。前一日档案记为"本档缺"，本轮 #18 已补测（lc=294、TO 3.4%、S 0.76）⇒ **M3 不再是空白，但也不是新机制** |
| BA6 I9（显著性门控增持） | ≈ M9 的变体（M9 用"净增持>0"门控） |
| BA6 I10（holdings ts_std_dev 252，反向） | 本档不单列，可作 M1 的反向对照 |
| 前一日 M5（日内集中度）/ M8（正交化） | 与本档 **M5 / M8** 同源，本轮补了它们的**宽度证据**（6–8 只/日） |

⇒ 相对 BA6，真正**未被覆盖**的只有：**M7（事件新鲜度）**，以及 **M3 的方向未定**这件事本身。

---

## 9. 未做 / 未验证（诚实边界）

1. **10 条模板全部未回测**：只过了 `preflight_expressions`（两批共 20 条 `valid=true`、`unknown_fields=[]`；
   两批合计引用 **8 个字段全覆盖**：gvkey/holdings/price/shares/tradesignificance/valueeur/value/currency_code）
   与人工结构核对，**S/F/2Y/sub/逐年一律未知**。本档只给"可设计的产品面"，不给收益承诺。
2. **`longCount` 的精确口径未证**：本档按本仓 probe SOP 当作"该口径下有值股票数"用（
   `tools/probe/dataset_data_probe.py:13-20`）；#19(382)/#20(383)/#9(294) 三个读数与"日均持仓数"解释自洽，
   但**没有**用逐日数据验证它到底是日均还是末日。
3. **更新间隔分布未测**：只有三档触达率（§4.4），没有每股间隔分布；平台指标里读不到间隔数值本身。
4. **`vec_*` 对分类字段的行为只测了 `vec_count`**：`vec_avg(transaction_currency_code)` 未探（无经济含义，故意不测，
   但这与"测过确认无值"不是一回事）。
5. **`insd1_price` 的语义未被独立验证**：description 说区间取下限，本轮未做"成交价 vs 收盘价"的折溢价探针。
6. **本轮未核 `filter_sharpe` 的 OS 口径**：返回 `sharpe_filter_applied=false` ⇒ 本区根本没做预筛，
   但这不等于"所有字段 OS Sharpe 为负"，只等于"平台没给这个判定"。
7. **`trade_when` 第三参语义未验证**：M9 的 `trade_when(cond, signal, -1)` 写法只过语法预检；
   "常数值 = 平仓" 还是 "常数 = 目标权重" 必须先单臂探针确认（本仓对此无 DEU 实证），
   否则派发后会出现"始终满仓空头"这类静默错误。

---

## 10. 证据索引

**平台读数（2026-11-16 本会话实读）**
- `get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false)`
  → 8 字段全 VECTOR、cov 0.5343、`complete=true / platform_count=8 / pages_fetched=1`（§1 表）
- `get_datafields(...)`（缺省 `filter_sharpe`）→ 同样 8 条 + `sharpe_filter_applied=false / sharpe_filter_removed=0`
- `get_datafields(..., data_type="MATRIX")` → `count=0 / platform_count=0 / complete=true`；`data_type="GROUP"` 同
- `get_datafields(region="DEU", universe="TOP500", data_type="GROUP", dataset_id=null)`
  → `platform_count=1515`（首 40 条截断）；`search="subindustry"` → `subindustry`（userCount 692 / alphaCount 5327）；
  `search="sector"` → `sector`（961 / 6629）——三者 `coverage` 均为 **0.0**
- `get_datasets(search="insider", region="DEU", delay=1, universe="TOP500")`
  → `insiders1 / Global Insider Trading Data / category=insiders / coverage 0.5343 / fieldCount 8 /
  userCount 23 / alphaCount 38 / valueScore 5 / pyramidMultiplier 1.6`；description 为「RIC↔BBID 映射」（串台）
- `get_operators()` → 103 算子；Vector 类仅 `vec_avg/vec_sum/vec_max/vec_min/vec_stddev/vec_range/vec_count`
- `get_documentation_page("vector-datafields")` → VECTOR = 每日每标的不定长事件数，须先 `vec_*` 转矩阵
- `preflight_expressions(10 条, dataset_id="insiders1", DEU/TOP500/D1)` ×2 批 → 均 `valid=true, unknown_fields=[]`
- 探针 multisim `4kBt8k45F4YZacG18Glz3gZm`（#1–10）与 `ec3kSdW54EIc0eGE7BdkHt`（#11–20）：
  均 `10/10 COMPLETE, errors=0`；`harvest_multisim_alphas` 回读 `complete=10, error_count=0`（§4.2 表）
- `get_field_catalog("DEU","insiders1")`（本地，仅对照）→ 8 字段同 id、`data_type=MATRIX`（失真）、拥挤度过期

**代码 / 文档**
- `world-quant-brain-mcp/mcp_core.py:341-343` — datafields 投影只留 6 键、description 截断 160 字符
- `tools/probe/dataset_data_probe.py:13-20` — `NONE` 中性化下 `longCount` 的读法；`:127` — VECTOR 探针 `vec_avg` 降维口径
- `Claude/skills/wq-brain-campaign-toolkit/scripts/_gate_expr_checks.py:803,:826` — 闸5 判定器；
  `:469-479` — 同源豁免降为 `[SAME_DATASET_LEG_ADD]` warning
- `Claude/skills/wq-brain-ra-deu/references/_basket-and-atom.md:44-53`（ATOM 免 IS_LADDER）、`:81-89`（闸5 合法空间）
- `Claude/skills/wq-basket-composition/references/deu-insiders-evidence.md:28-32`（HHI 集中度）、
  `:31`（Δ66 单腿 S 1.72）、`:47-64`（DEU insiders 判死清单）
- `docs/reference/EUR/insiders_field_profile_20261107.md:40-41`（9 字段/无方向字段）、`:49-51`（nanHandling 空头风险）、
  `:53,:69`（留待实测的方向未知项）
- `Claude/skills/wq-brain-ra-gbr/references/insiders.md:101-112` — GBR 侧 significance / value 零信号
- `docs/reference/field_profile_ind_inst_fund_20261019.md:228` — IND 侧同集「标识符映射、cov 0.388」独立记述
- `tracking/DEU/regular_tower/FIELD_insiders1_20261115.md` — 前一日档案（本档在其基础上补：方向实证、
  向量宽度、`vec_count` 语义、currency 可归约、更新频率三档）
- `tracking/DEU/atom_orthogonal/waveBA6_insiders1_pool_design_20261110.md:18-29` — BA6 十模板
- `tracking/DEU/regular_tower/S0_TOWER_SCAN_20261115.md:237` — DEU 主腿 FAST / SUBINDUSTRY 证死

---

## 11. 独立复核（2026-11-16 第二会话；只复读，未回测）

> 本节由**第二个会话追加**，**未覆写** §0–§10 —— 那 20 条探针读数不可重建，覆写即销毁证据。
> 目的只有两个：用一轮**独立平台实读**核对本档字段面结论能否复现；补 3 条上文当时未记的平台侧证据。
> **引用探针指标时仍请引 §4.2 原文，不要引本节**（本节没有重跑任何仿真）。

### 11.1 复读清单（本轮实读，逐项比对）

| # | 调用 | 本轮实返回 | 与上文比对 |
|---|---|---|---|
| R1 | `get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false)` | `count=8, platform_count=8, complete=true, pages_fetched=1`；8 条全 **VECTOR**、coverage 全 **0.5343**；逐字段 `userCount/alphaCount` 与 §1 表**逐位相同**（holdings 11/13、valueeur 10/12、tradesignificance 7/9、shares 4/5、price 3/4、value 2/2、gvkey 1/1、currency 1/1） | ✅ 一致（§1） |
| R2 | 同上，**缺省** `filter_sharpe` | 同样 8 条；`sharpe_filter_applied=false, sharpe_filter_removed=0` | ✅ 一致（§1） |
| R3 | 同上 + `data_type="MATRIX"` | `count=0, platform_count=0, complete=true` | ✅ 一致（§2） |
| R4 | 同上 + `data_type="GROUP"` | `count=0, platform_count=0, complete=true` | ✅ 一致（§2） |
| R5 | `get_datasets(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500")` | `Global Insider Trading Data / category=insiders / coverage=0.5343 / fieldCount=8 / userCount=23 / alphaCount=38 / valueScore=5 / pyramidMultiplier=1.6`；description 仍是「RIC↔BBID 映射」 | ✅ 一致（§1 两处不可信元数据） |
| R6 | `get_operators()` | `count=103`；Vector 类**只有** `vec_avg / vec_count / vec_max / vec_min / vec_range / vec_stddev / vec_sum` | ✅ 一致（§2 的 7 个） |
| R7 | `get_field_catalog("DEU","insiders1")`（本地，仅对照） | 8 条，id 集合与平台**逐 id 相同**；表头 `data_type="MATRIX"`；`userCount/alphaCount` 全是 0/1 | ✅ **幽灵字段 = 0**，并确认本地 `data_type` 与拥挤度两处失真（§1、§7） |
| R8 | `query_field_profile(region="DEU", dataset="insiders1")` | `count=0, rows=[]` | 新增：**本地字段画像表对本集是空的** ⇒ 本集没有任何本地先验可引用，结论只能建在平台实读 + 探针上（与本档做法一致） |
| R9 | `get_datafields(region="DEU", universe="TOP500", delay=1, data_type="GROUP", dataset_id=null, search="subindustry")` | `subindustry` / GROUP / coverage **0.0** / userCount **692** / alphaCount **5327**；`platform_count=1515, complete=false, pagination_truncated=true, truncated_reason="search_window_capped"` | ✅ 一致（§2 地基）：**§6 全部模板依赖的 `subindustry` 分组轴真实存在**，并再次印证「coverage=0 ≠ 没数据」 |

R9 附注：`complete=false / truncated_reason="search_window_capped"` 是**搜索窗被平台截断**的显式标记，与 §2
「GROUP 目录不能用来建全表」的口径一致；`platform_count=1515` 是 DEU/TOP500 的 **GROUP 全量**，**不是**本集字段数。

### 11.2 新增证据 A：VECTOR 文档页给 14 个归约算子，注册表只认 7 个（且 `vec_median` 是纯文字幽灵）

`get_documentation_page("vector-datafields")`（`lastModified=2026-10-16T05:56:37`）实读：

- 正文原文：平台**所有算子都是为矩阵输入设计**的 ⇒「use the matrix operator **only after using the `vec_` operators**」
  —— 这是 §2 降维要求的**平台原文依据**（此前只有本仓经验口径）。
- 文档表格列 **14** 个：`vec_avg, vec_choose, vec_count, vec_ir, vec_kurtosis, vec_max, vec_min, vec_norm,
  vec_percentage, vec_powersum, vec_range, vec_skewness, vec_stddev, vec_sum`；
  而 `get_operators()` 只返回 **7** 个（R6）⇒ 差集 7 个：`vec_choose / vec_ir / vec_kurtosis / vec_norm /
  vec_percentage / vec_powersum / vec_skewness`。
- **本轮新发现（上文未记）**：文档正文第二个例子里写有 **`vec_median(...)`**，但它**既不在该文档自己的表格中，
  也不在 `get_operators` 里** ⇒ 纯文字幽灵，比 §2 记的「文档页多列 7 个」更隐蔽一层。
  **不要照抄文档页写 `vec_median`**；§6 的 10 条模板只用 7 个实名算子，无此风险（§11.4 已机器验证）。

### 11.3 新增证据 B：平台自家文档独立支持「裸 `vec_*` 换手必须衰减」

同一文档页正文两处：① 裸 `vec_count` 的换手「**sometimes touching 200%**」；②「It tends to be **necessary** to reduce
its turnover **using decay operators**」；第二个例子的 `vec_avg` 换手「**around 130%**」，并建议
「reduce turnover by using **`ts_rank` or `ts_decay`**」。

⇒ §4.6 的「裸 `vec_*` TO 1.62–1.79 必须平滑」**不只来自 DEU 探针**，也与平台对 VECTOR 类的一般性陈述同向。
两者是**互相印证**关系（一个按类别、一个按本区实测），不能互相替代：文档不证明 DEU 的数值，探针不证明别的区。

### 11.4 新增证据 C：§6 的 10 条模板本轮全部复过预检（机器实测）

`preflight_expressions(alpha_expressions = §6 全部 10 条, region="DEU", universe="TOP500", delay=1,
dataset_id="insiders1", **auto_fix_vector=false**)` →

```
valid=true, expressions=10, unknown_fields=[], unknown_soft=[], builtin_fields=[],
fields_checked=["insd1_holdings","insd1_shares","insd1_tradesignificance","insd1_valueeur"],
platform_field_count=4, vector_fields=[], any_changed=false
```

三点读法：

1. `valid=true` + `unknown_fields=[]` ⇒ 10 条骨架的字段与算子全部被平台识别。
2. **`auto_fix_vector=false` 下仍 `vector_fields=[]` / `any_changed=false`** ⇒ preflight 的 VECTOR 自动修复器
   **没找到任何未包裹的向量字段** ⇒「先 `vec_*` 再矩阵算子」这条纪律在 10 条模板里是**真做到了**，
   不是靠 auto_fix 兜住的（这一条是 §9 第 1 条此前只有「人工结构核对」的部分，本轮升级为平台预检实测）。
3. `fields_checked` 只有 **4** 个字段，因为 10 条骨架**只用到这 4 个**；`gvkey` / `transaction_currency_code` /
   `value` / `price` 未被任何模板引用（与 §7 把前两个列非信号、§6 不用后两个判死件一致）。
   ⚠ 这不等于「另外 4 个字段不可用」，只等于「本档模板没用到」。

### 11.5 本轮**没有**复核的部分（不得当作已复现）

- **20 条探针的全部指标**（§4.2 表、§4.3 宽度塌缩、§4.5 方向、§4.6 换手）：**一条都没重跑**
  （不重复烧配额，`AGENTS.md` §7.5「收割优先于重挖」）。证据身份仍是**前一会话的平台读数**，
  引用位置见 `FIELD_insiders1_20261116.md:107-137`、`:147-166`、`:183-193`、`:195-203`。
- 拥挤度的**日环比**（§1 第 2 条：20/29 → 23/38）：本轮只复读当日绝对值 23/38，**没有**复核 11-15 的 20/29。
- 跨区判死/证据链：只核了 `Claude/skills/wq-basket-composition/references/deu-insiders-evidence.md:28-32`（Δ66=1.72、
  HHI 1.74–2.20、ts_ir 1.81、freshness 2.04）与 `:47-64`（判死清单：valueeur 1.14 / shares÷holdings 1.29、
  tradesignificance 1.21 / price 1.13），**其余 EUR/GBR 记述未逐条核**。
- §6 全部模板的 **S/F/2Y/sub 仍未回测**（§9 第 1 条继续成立）；本轮只往上加「语法+降维过闸」一层。

### 11.6 复核结论

**§1（8 字段全 VECTOR / coverage 全 0.5343 / 幽灵字段 0）、§2（无 MATRIX·GROUP·EVENT，可用 `vec_*` 仅 7 个）、
§4.1（coverage 不携带字段级信息）、§7（两个非信号字段）四节逐项复现，零更正。**

新增 3 条上文未记的平台侧证据（VECTOR 文档 14 vs 注册表 7 且 `vec_median` 为文字幽灵、平台文档对裸换手的陈述、
10 条模板预检实测），以及 1 条负面信息（本地 `query_field_profile` 对本集为空）。
**字段面（fieldCount=8）与降维要求（7 个 `vec_*`）不需要修订；待补的仍是 §9 那 7 项，其中探针类读数本轮刻意未重跑。**
