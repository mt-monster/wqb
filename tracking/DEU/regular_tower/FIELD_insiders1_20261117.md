# DEU / D1 / TOP500 — `insiders1` 字段档案（S1）· 2026-11-17

> 生成：2026-11-17｜口径：`region=DEU, universe=TOP500, delay=1`
> 数据源：**本轮平台实读**（详见 §9 证据索引）：
> `get_datafields`（全量 / `data_type=MATRIX` / `data_type=GROUP`）、`get_datasets`、`get_operators`（103 算子）、
> `batch_get_alpha_metrics`（既有 20 条探针臂 **20/20 success**，零配额重读）、`get_alpha_details`（**11 臂**，含 longCount/shortCount/CW/RA）、
> `preflight_expressions`（8 条模板全过）。
> 本地对照（只读 sqlite，`logs/_tmp_ins1_catalog*.py`，**wqb-db MCP 本轮故障见 §8**）：`field_profile_perf` 8 行 / `fields` 表 0 行。
> 前序档案：`FIELD_insiders1_20261115.md` / `FIELD_insiders1_20261116.md`（本文在其基础上**新增「字段新鲜度」节**，
> 并把宽度/换手读数升级为**本轮直接平台重读**，前序的 20 条探针指标不再只是转录）。

---

## 0. 一句话结论

平台实读 **8 字段、8/8 VECTOR、coverage 逐字段全 0.5343**（= 数据集级值复制，**该列在本集不携带字段级信息**）。
全部字段 **2026-07-01 同日 onboard（单一批次）**，**近 3 个月零新增**；平台无任何字段级「最后更新」属性。
按「老 + alphaCount 极低」判据（onboard ≥90 天且 alphaCount ≤2）圈出 **3 个疑似死字段**：
`insd1_gvkey`(1)、`transaction_currency_code`(1)、`insd1_value`(2)——前两者同时是语义上的标识符/标签（§7）。
字段级宽度（本轮 `get_alpha_details` 实读）：裸 `vec_*` 截面 **6–12 只/日（1.2%–2.4% 的 TOP500）** 且 **8/8 裸臂 CW 满值挂闸
（value=1.0 vs limit 0.1）**；250 日回填后 **294 只（58.8%）**、十年内曾覆盖 **383 只（76.6%）**。
**时间平滑是本集的入场条件**：裸臂换手 1.62–1.79（硬线 0.7），回填后 0.011–0.034（§5.4）。

---

## 1. 平台字段全表（平台实读，8/8 无截断）

`get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false)`
→ `count=8, platform_count=8, complete=true, pages_fetched=1`（本轮实读）。
⚠ 请求中 ask 拟用的 `sort_by="dateCreated"` / `min_coverage=0.0` **不是本 MCP 工具的入参**（schema 无这两键），
响应回显 `sorted_by=null, min_coverage=null` ⇒ 排序/覆盖过滤**未被执行**；「新鲜度」改由返回的逐字段 `dateCreated` 手工归纳（§2）。

| # | 字段 | type | coverage | userCount | alphaCount | dateCreated | pyramidMultiplier | description（语义唯一依据） |
|---|---|---|---|---|---:|---:|---|---|
| 1 | `insd1_holdings` | VECTOR | 0.5343 | 11 | 13 | 2026-07-01 | 1.6 | Total equity share holdings of the insider **after the transaction** |
| 2 | `insd1_valueeur` | VECTOR | 0.5343 | 10 | 12 | 2026-07-01 | 1.6 | Total value of the transaction **in Euro** |
| 3 | `insd1_tradesignificance` | VECTOR | 0.5343 | 7 | 9 | 2026-07-01 | 1.6 | Significance score of the trade (**1 = low significance, 3 = high significance**) |
| 4 | `insd1_shares` | VECTOR | 0.5343 | 4 | 5 | 2026-07-01 | 1.6 | **Number of shares** (or units) traded in the transaction |
| 5 | `insd1_price` | VECTOR | 0.5343 | 3 | 4 | 2026-07-01 | 1.6 | Transaction **price per share**; 若报区间则取**最小值** |
| 6 | `insd1_value` | VECTOR | 0.5343 | 2 | 2 | 2026-07-01 | 1.6 | Total value of the transaction **in original currency** |
| 7 | `insd1_gvkey` | VECTOR | 0.5343 | 1 | 1 | 2026-07-01 | 1.6 | Compustat Global Company Identifier（**标识符**） |
| 8 | `transaction_currency_code` | VECTOR | 0.5343 | 1 | 1 | 2026-07-01 | 1.6 | Three-letter **ISO currency code**（**分类标签**） |

**幽灵字段 = 0。** 本地对照（只读 sqlite，`data/wqb.db`）：
- `field_profile_perf` 表 DEU/insiders1 恰 **8 行、id 集合与平台逐 id 相同**；
- `fields` 表（原始 catalog）`dataset_id='insiders1'` **0 行**（本地原始 catalog 对本集为空，无多出的幽灵 id）；
- `datasets` 表 `id LIKE '%insider%'` **0 行**（本地数据集表缺本集行）。
⇒ 平台 8 条 = 本地 8 条，**不存在本地幽灵字段问题**，本条按平台实返回核对。
⚠ 本地 `field_profile_perf` 给 8 字段**全部标 `verdict='UNUSABLE'` 且 `n_tests=0`** ⇒ 零测试支撑的本地标签，
按 AGENTS §8.11 口径（`n_tests` 不含 MCP 直连仿真）**不作可用性依据**。

**数据集级元数据（`get_datasets` 本轮实读，两处不可信）**：
1. `insiders1` 的 description 是「RIC↔BBID 标识符交叉映射」，与字段语义（Global Insider Trading Data）无关 ⇒ **平台元数据串台**，语义只认字段 description。
2. 拥挤度：`userCount=23 / alphaCount=38 / valueScore=5.0 / pyramidMultiplier=1.6 / coverage=0.5343 / fieldCount=8`。
   前序档（`FIELD_insiders1_20261116.md:50-51`）记 11-16 为 23/38 ⇒ 与昨日持平（11-15 为 20/29）。
3. 派生（算术，非平台声明）：8 字段 `alphaCount` 求和 = **47 ≠ 数据集级 38** ⇒ 字段级 alphaCount 是「引用该字段的 alpha 数」，
   同一 alpha 引用多字段会重复计；**不是**「8 条独立字段信号各有 47 个 alpha」。

---

## 2. 字段新鲜度（ask 指定节；全部为平台 `dateCreated` 实读）

| 项 | 读数 | 依据 |
|---|---|---|
| 最新 `dateCreated` | **2026-07-01**（8/8 字段同一日期） | §1 表逐字段实读 |
| 近 3 个月 onboard 字段数 | **0 / 8**（2026-08-17 之后零新增） | 8/8 `dateCreated=2026-07-01` |
| 距今天龄 | **139 天**（2026-07-01 → 2026-11-17；派生算术） | 同上 |
| 平台「最后更新」属性 | **NOT_MEASURED**（`get_datafields` 投影无此键，`world-quant-brain-mcp/mcp_core.py:333-349`） | 本轮返回的 8 条字段无任何更新时点 |
| onboard 形态 | **单一批次**（8 字段同日上线，此后无增量/无替换） | §1 表 |

**「老且 alphaCount 极低」= 疑似死字段**（判据：onboard ≥ 90 天 且 平台 `alphaCount ≤ 2`；本集 8/8 满足年龄侧，判别力全在 alphaCount）：

| 字段 | dateCreated | alphaCount | 判定 | 依据 |
|---|---|---|---|---|
| `insd1_gvkey` | 2026-07-01 | **1**（最低档） | **疑似死字段 → §7** | 老（139 天）+ 全表最低引用；且 description 为 Compustat 标识符 ⇒ 双重理由 |
| `transaction_currency_code` | 2026-07-01 | **1**（最低档） | **疑似死字段 → §7** | 老 + 全表最低引用；且 description 为 ISO 币种标签 ⇒ 双重理由 |
| `insd1_value` | 2026-07-01 | **2** | **疑似死字段 → §7** | 老 + 次低引用；且与 `insd1_valueeur` 语义重复（仅币种不同）⇒ 低引用可能因为「被 valueeur 替代」 |

⚠ 诚实边界（不猜不补）：
1. **alphaCount 低 ≠ 信号死**——低引用也可能是「低拥挤 = 机会」；本档只按 ask 判据登记「疑似」，**不据此判死**
   （AGENTS §7.6 D2：未测字段不得凭族先验封禁；`gvkey`/`currency_code` 另有语义层面的非信号理由，`value` 另有语义重复理由）。
2. 全集 8 字段共享同一 `dateCreated` ⇒ **「老」在本集内没有任何区分度**，本档不把「老」单独当作字段级特征。
3. 平台字段 `alphaCount` 分布（13/12/9/5/4/2/1/1）显示本集整体低拥挤，头部集中在 `holdings`/`valueeur`——与 DEU 战役「holdings 为唯一强信号、valueeur 为已判死单腿」的实测一致（§6 先验列）。

---

## 3. 类型与降维要求

- **8/8 VECTOR，无 MATRIX / EVENT / GROUP。** 本轮实读：同入参加 `data_type="MATRIX"` → `count=0, platform_count=0, complete=true`；
  `data_type="GROUP"` → 同样 0/0。⇒ 本档**不涉及** EVENT 的 `ts_event_*` 支撑问题（无 EVENT 字段可探）；
  `insd1_gvkey` 虽像分组键但类型是 VECTOR，**不能**直接当 group 用。
- **可用 `vec_*` 只有 7 个**（`get_operators` 本轮实读、共 103 算子）：`vec_avg / vec_sum / vec_max / vec_min / vec_stddev / vec_range / vec_count`。
- **空向量语义（本轮实证）**：`vec_count(insd1_valueeur)` 的 `longCount=12`（不是 500）⇒ 当日无申报时聚合**没有值**（不是 0）。
  因此 **`ts_backfill(vec_*(x), 250)` 是本集入场件**，否则截面只剩个位数股票（§5.2）。
- **降维纪律**：`vec_*` →（需要跨日延续时）`ts_backfill` → 时序/截面算子，**禁止裸用字段**
  （`tools/probe/dataset_data_probe.py:127` 的 VECTOR 探针口径 `rank(ts_backfill(vec_avg(f),250))`）。
  ⚠ 逐字段聚合口径影响宽度：`vec_sum(valueeur)` 单日 11 只、`vec_count` 12 只、`vec_min` 10 只、`subtract(vec_max,vec_min)`（≡ `vec_range` 语义）6 只（§5.2）——
  **不同聚合算子读出不同截面**，选聚合本身是设计决策。

---

## 4. 语义维度（按 description 归纳；字段名不作依据）

| 维度 | 代表字段 | 经济含义（据 description） |
|---|---|---|
| **内部人持股存量（状态量）** | `insd1_holdings` | 交易后内部人持股总数 = **stock**；跨笔/跨人求和 ≈ 公司层面内部人合计持股。**本集唯一的方向代理**（时间差分定增持/减持）。 |
| **交易规模（欧元）** | `insd1_valueeur` | 每笔交易总价值（EUR），跨市场可比。 |
| **交易规模（原币）** | `insd1_value` | 与 `valueeur` **语义同一、仅计价币种不同** ⇒ 互替而非互补，同用即重复计规模。 |
| **成交股数** | `insd1_shares` | 本次成交股数；金额 ≈ 股数×价 ⇒ 与金额高度共线。 |
| **成交价快照** | `insd1_price` | 每股成交价（区间取下限）；**不是收盘价**，只有与自身历史比才有"内部人成交价位"含义。 |
| **交易重要性（序数）** | `insd1_tradesignificance` | 平台自评 1–3 序数。**序数≠基数**：可作加权，不可解释成"重要性金额"。 |
| **事件条数（派生）** | `vec_count(任一字段)` | 当日该股申报记录条数 = 事件强度/广度轴。**本轮实证**：`vec_count(valueeur)` 与 `vec_count(tradesignificance)` 的全部指标逐位相同（S 0.70 / F 0.31 / TO 1.6711 / lc 12 / pnl 34,832,751，两个 alpha id 平台实读逐键一致，§5.2）⇒ 条数是**一条**轴，换字段不产生新信息。 |
| **日内规模离散（派生）** | `vec_range` / `vec_stddev` / `subtract(vec_max,vec_min)` | 同日多笔交易的规模分歧度/集中度；只在当日宽度 ≥2 时有定义（lc 6–7）。 |
| **标识符（元数据）** | `insd1_gvkey` | Compustat 公司码 ⇒ 非信号（同股常数，无截面排序含义）。 |
| **分类标签（元数据）** | `transaction_currency_code` | ISO 币种码 ⇒ 非信号（均值/求和无经济含义；`vec_count` 可归约但只是重复 §7 的 count 轴）。 |

**★ 结构性缺口（2026-11-16 探针实证，本轮 11 臂重读再次确认）**：8 个字段里**没有任何买卖方向字段**，
且本轮重开的 **11 条**探针臂平台 `shortCount=0`（§5.2；其中 `vec_min(valueeur)` / `vec_min(value)` / `vec_sum(valueeur)` 三条正是「若卖出被记成负数则必然出现空头」的判别臂）⇒ 数值符号也不携带方向。
⇒ 方向只能由 `insd1_holdings` 的**时间差分**推断（§6 M1/M5），或同波带反号对照臂。

---

## 5. 字段级覆盖实读

### 5.1 `coverage` 在本集不携带字段级信息（且数据集级 coverage 不可作可用性判据）

8 字段 coverage **全部 0.5343**，与 `get_datasets` 返回的数据集级 `coverage=0.5343` **逐位相同**
⇒ 该列是把数据集级值复制到每个字段，**无法区分字段**。不得用它判字段可用性、更不得用它判数据集可用性
（AGENTS §8.11 ①：数据集级 coverage 是"宽面已入场的标签"不是数据存在性判据；本档同口径执行）。

### 5.2 宽度塌缩（本轮平台实读 `get_alpha_details`，11 臂；及 `batch_get_alpha_metrics` 20/20）

统一探针口径：`neutralization=NONE / decay=0 / truncation=0.0 / nanHandling=OFF / 2014-01-01~2023-12-31`。
`rank()` 恒正 ⇒ `longCount` = 该口径下有值的股票数（读法出处 `tools/probe/dataset_data_probe.py:13-22`）。

| # | 表达式（alpha id） | lc | TO | S | F | sub | shortCount | CW | 备注 |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---|
| 1 | `vec_count(insd1_valueeur)`（`P05wnQRW`） | **12** | 1.6711 | 0.70 | 0.31 | −0.30 | 0 | **fail 1.0** | 同日有申报的股票数 = 2.4% |
| 2 | `vec_count(insd1_tradesignificance)`（`P05wnQVW`） | **12** | 1.6711 | 0.70 | 0.31 | −0.30 | 0 | **fail 1.0** | 与 #1 **逐键相同**（含 pnl 34,832,751） |
| 3 | `vec_count(insd1_holdings)`（`ZYa2jP88`） | **9** | 1.6345 | 0.68 | 0.32 | −0.26 | 0 | **fail 1.0** | 唯一有缺口的列（约 25% 申报记录无交易后持股） |
| 4 | `greater(vec_count(insd1_valueeur),1)`（`blaoNGwq`） | **8** | 1.6610 | 0.88 | 0.43 | −0.06 | 0 | **fail 1.0** | 当日宽度 ≥2 = 1.6%（占事件股 8/12=67%） |
| 5 | `subtract(vec_max(insd1_valueeur),vec_min(insd1_valueeur))`（`leaQ7885`） | **6** | 1.7016 | 0.39 | 0.16 | −0.13 | 0 | **fail 1.0** | 当日 ≥2 个不同金额 = 1.2%（占事件股 50%） |
| 6 | `vec_min(insd1_valueeur)`（`YPa2N57l`） | **10** | 1.7875 | 0.25 | 0.08 | 0.03 | 0 | **fail 1.0** | **方向判别臂**：若有负值权重必为负 |
| 7 | `vec_sum(insd1_valueeur)`（`WjlaNPPP`） | **11** | 1.7183 | 0.29 | 0.10 | −0.23 | 0 | **fail 1.0** | 同上（金额直通权重） |
| 8 | `vec_min(insd1_value)`（`1YWaoxxm`） | **10** | 1.7893 | 0.21 | 0.07 | −0.03 | 0 | **fail 1.0** | 同上（原币口径） |
| 9 | `rank(ts_backfill(vec_sum(insd1_valueeur),250))`（`A1xgnjAQ`） | **294** | 0.0299 | 0.75 | 1.01 | −0.91 | 0 | **pass** | 250 日回填后 = 58.8% |
| 10 | `rank(ts_count_nans(vec_avg(insd1_valueeur),250))`（`88NaO3jV`） | **382** | 0.0107 | 0.74 | 0.99 | −0.07 | 0 | **pass** | 十年内曾覆盖 = 76.4% |
| 11 | `rank(days_from_last_change(ts_backfill(vec_sum(insd1_valueeur),250)))`（`Jj8gnxNA`） | **383** | 0.0296 | 0.74 | 0.98 | 0.02 | 0 | **pass** | 十年内曾覆盖 = 76.6% |

（另 9 臂的 S/F/TO/2Y/sub/margin 本轮 `batch_get_alpha_metrics` 20/20 实读，与前序档 §4.2 逐值一致；
`vec_stddev` lc=7、`vec_max` lc=11、`vec_avg(holdings)` lc=9、`vec_avg(tradesignificance)` S 0.91 等为前序档读数
`FIELD_insiders1_20261116.md:115-134`，本轮未重开。）

**塌缩形态 = 截面塌缩，不是向量宽度塌缩**：
- 同日事件股 **12/500（2.4%）**；其中有记录股里 **8/12（67%）宽度 ≥2、6/12（50%）有 ≥2 个不同金额**（#4/#5 直接读数）
  ⇒ 「日内结构」（集中度/离散度）在本集**有原料**，但全表最窄（6–8 只/日）。
- 250 日回填后 **294/500（58.8%）**；十年内曾覆盖 **382–383/500（76.6%）**。
- **约 117 只 TOP500 股票十年内一次申报都没有** ⇒ 依赖 `nanHandling ON` 把缺失填 0 的写法会把它们变成长期空头，
  alpha 内容被替换成「有没有内部人」这一规模/流动性代理（与 EUR 侧记述同机理：`docs/reference/EUR/insiders_field_profile_20261107.md:49-51`）。
- **宽度塌缩的直接后果 = CW 满值挂闸（本轮新登记）**：**8/8 实读裸臂** `CONCENTRATED_WEIGHT` 全部 `fail`，value 恰为 **1.0** vs limit 0.1
  （单名权重 100%），日期各异（2019-10-10 / 2021-07-05 / 2021-09-06×3 / 2023-01-16 / 2023-10-20）；回填臂 #9/#10/#11 则 CW **pass**。

### 5.3 更新频率

- **平台 MCP 面不暴露声明频率**：`get_datafields` 投影只有 `id/type/coverage/userCount/alphaCount/dateCreated/pyramidMultiplier/description` 八键
  （`world-quant-brain-mcp/mcp_core.py:333-349`；description 截断 160 字符，本集最长 78 字符未截断）⇒ 频率属性 **NOT_MEASURED**，本档不猜。
- 从 description 定性：逐笔交易申报（事件驱动），非日/周/月预聚合快照。
- 触达率三档（全为平台读数，§5.2）：日频 **2.4%**；滚动 250 日 **58.8%**；十年内 **76.6%**。
- 派生（算术，标注非平台读数）：12 只/日 × 250 交易日 ÷ 383 只曾覆盖 ≈ **7.8 个申报日/股/年** ⇒ 中位覆盖股约**每 32 个交易日一次申报**。
- **未测**：每股更新的实际间隔分布（平台指标读不到间隔数值本身，本档不给分布）。

### 5.4 换手：平滑是入场，不是优化

裸 `vec_*` 族换手 **1.62–1.79**（§5.2 表 #1–#8 裸臂，本轮 `get_alpha_details` 实读；20 臂全体的 TO 区间 1.6224–1.7893 由 batch 实读确认），全部超 0.7 硬线 2 倍以上；
同一字段加 250 日回填后 **0.0107–0.0337**（#9–#11）——相差 **48–167 倍**。
⚠ 低换手 ≠ 好信号：#9–#11 的 S≈0.74–0.75 但 sub −0.91~0.02、2Y −0.23~−0.07，属「低换手 = 低信息」另一端（DEU 判读基准 S≥1.58 全未达）。

### 5.5 方向：数值不带符号（本轮 11 臂 `get_alpha_details` 实读 `shortCount` 全 0）

11/11 条实读臂 `shortCount=0`（§5.2 表，取 `metrics.shortCount`）⇒ 2014–2023 全样本内 `value/valueeur/shares` 未出现负值；
其中 `vec_min(insd1_valueeur)`（lc 10）、`vec_min(insd1_value)`（lc 10）、`vec_sum(insd1_valueeur)`（lc 11）三条**正是**判别臂——
若卖出被记为负数，这三条的权重会变负、`shortCount` 必然 >0，实测均为 0。
`vec_avg(tradesignificance)`（S 0.91，前序档）也全多头，与「1–3 正序数」一致。⇒ **买卖方向不在字段里、也不在数值符号里**。
（未重开的 9 臂 shortCount 未在本轮复读，前序档记同为 0：`FIELD_insiders1_20261116.md:183-193`。）
设计上只有三条路：① `insd1_holdings` 差分定号（M1/M5）；② 同波反号对照臂；③ 无方向强度/集中度/新鲜度机制。

---

## 6. 模板骨架（8 个不同机制，非换窗口；本轮 `preflight_expressions` 全过）

统一约定：单表达式、单数据集（ATOM）、单腿；先 `vec_*` 降维；跨日延续先 `ts_backfill`；
`ts_sum/ts_mean` 只加有事件的日子（天然平滑，可不回填）。
**全部 8 条本轮过 `preflight_expressions`（`valid=true, unknown_fields=[], vector_fields=[], any_changed=false`，
`auto_fix_vector=false` 下无未包裹向量字段）——语法/字段/降维三关已证，但 S/F/2Y/sub 全未回测。**
先验分级：**A** = DEU 战役已有实测支持；**T** = 本族 w1–w4 已实测（强度有限）；**C** = 构成件已判死、交互几何未测；**N** = 本轮新提出。

| # | 机制（差在哪） | 骨架 | 预期符号 | 经济机制 | 先验 |
|---|---|---|---|---|---|
| **M1** | **存量变化的信噪比**（持续增持 vs 一次性脉冲） | `rank(ts_ir(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66),252))` | **+** | 持续买入比一次性买入更可能是信息交易（Cohen-Malloy-Pomorski 的 routine/opportunistic 区分）；Δ66 单腿 DEU 已证 1.72 | **A**（`deu-insiders-evidence.md:31` 的「A 单腿 Δ66 = 1.72」+ `:51` holdings 为唯一强信号 S 2.36；该文件未逐字写明 A 的底字段，本档并列引用、不作二次归因）；`ts_ir` 壳未在本族测过 holdings 差分 |
| **M2** | **日内单笔支配度**（最大单笔占当日总额） | `rank(ts_sum(divide(vec_max(insd1_valueeur), add(vec_sum(insd1_valueeur),0.0001)),66))` | **+** | 单笔支配 = 信念集中；姊妹集 HHI 几何 DEU 最强（S 1.74–2.20），但那是 `significant_value_1`（**不在本集 8 字段**，见下注） | **T**（w4 已测 `ts_sum(max÷sum,66)` 族：S 0.20–0.89，无分组 ts_ir 252 最高 0.89，`WAVE_rt-insiders-w4_20261116.md:21,26`）；裸核弱 |
| **M3** | **事件广度**（申报条数强度，与规模正交） | `rank(ts_sum(vec_count(insd1_shares),66))` | **+（待双向验证）** | 申报到达强度 = 信息量；但也可能是坏消息集中申报 ⇒ 建议同波带反号臂 | **T**（w4 臂8 分组版 S 0.62 / sub 0.01，`WAVE_rt-insiders-w4_20261116.md:28`；条数是单一轴，只写一条） |
| **M4** | **事件新鲜度**（距最近申报的天数） | `rank(subtract(250, days_from_last_change(ts_backfill(vec_sum(insd1_valueeur),250))))` | **+** | 越近的申报信息越未衰减 | **T**（w4 金额时钟 S 0.43 / w3 条数时钟 0.27，`WAVE_rt-insiders-w4_20261116.md:86-89`：金额 > 条数，两者都弱） |
| **M5** | **净增持日占比**（符号频率，非幅度） | `rank(ts_sum(sign(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),1)),66))` | **+** | 66 日里持仓净上升的天数占比 = 增持 regime 的频率；与 M1 的幅度信噪比正交（频 vs 幅） | **N**（无回测；方向为推断，因无方向字段，必须反号对照） |
| **M6** | **同日金额分歧度（反向）**（低离散 = 意图一致） | `rank(ts_mean(reverse(divide(vec_stddev(insd1_valueeur), add(vec_avg(insd1_valueeur),0.0001))),66))` | **+（=低分歧）** | 同日多笔金额集中 vs 分歧：分歧大 = 多名内部人/混合意图 = 噪声；离散度反向加权 | **C/N**（`vec_stddev` 裸基线 S 0.72 但 lc 仅 7；比值+反向+ts_mean 平滑为新几何） |
| **M7** | **重要性加权规模**（金额 × 平台自评 1–3） | `rank(ts_sum(multiply(ts_backfill(vec_sum(insd1_valueeur),250), ts_backfill(vec_avg(insd1_tradesignificance),250)),66))` | **+** | 大额且"重要"的交易更有信息；单腿均死、交互未测 | **C**（`valueeur` 1.14 / `tradesignificance` 1.21 判死，`deu-insiders-evidence.md:54,56`） |
| **M8** | **成交价相对自身历史位置**（估值位置） | `rank(divide(vec_avg(insd1_price), ts_mean(vec_avg(insd1_price),250)))` | **双向** | 内部人成交价相对过去一年自身水平的折溢价；无方向字段 ⇒ 高位=卖出价/低位=买入价无法区分，必须成对跑 | **C/N**（`insd1_price` 单腿 1.13 判死 `deu-insiders-evidence.md:57`；比值+时序位置为新几何；**同时补 D2 缺口：price 族从未被 w1–w4 探过**，`WAVE_rt-insiders-w4_20261116.md:187`） |

**为什么算 8 个不同机制**：M1 幅度信噪比 / M2 日内集中度 / M3 条数广度 / M4 时间距离 / M5 符号频率 /
M6 日内分歧度 / M7 序数交互 / M8 价格位置——8 种不同的量。M1 与 M5 同用 holdings 但分别读**幅度稳定性**与**方向频率**；
M2 与 M6 同用 valueeur 但分别读**最大单笔占比**与**全向量离散**。不做纯换窗变体。
**注（重要）**：`deu-insiders-evidence.md:28,52` 的 HHI 2.20 出自 `significant_value_1`（姊妹集 `insider_agg_matrix`/`insider_matrix` 的字段），
**不在 insiders1 的 8 字段名单里**（本轮平台实读）⇒ 该先验只能作为「集中度机制在姊妹集有效」的跨集佐证，
不能直接背书本集 M2 的期望强度（w4 实测本集原生集中度最高 0.89）。

---

## 7. 不可用 / 疑似死字段清单（blockedFields）

| 字段 | 状态 | 依据 |
|---|---|---|
| `insd1_gvkey` | **疑似死字段（双理由）** | ① 新鲜度判据：`dateCreated=2026-07-01`（139 天）且 `alphaCount=1`（全表最低档，§2）；② description 为 Compustat 标识符 ⇒ 同股常数、无截面排序含义，非信号。 |
| `transaction_currency_code` | **疑似死字段（双理由）** | ① 新鲜度判据：`alphaCount=1`（全表最低档，§2）；② description 为 ISO 币种标签 ⇒ 均值/求和无经济含义（`vec_count` 可归约但只是重复 count 轴）。 |
| `insd1_value` | **疑似死字段（双理由）** | ① 新鲜度判据：`alphaCount=2`（次低档，§2）；② description 与 `insd1_valueeur` 语义重复（仅币种不同）⇒ 低引用疑似被 valueeur 替代，同用即重复计规模。 |
| 幽灵字段 | **0 条** | 平台 8 条 = 本地 `field_profile_perf` 8 条，逐 id 一致（§1）。 |

⚠ 边界声明：以上按 ask 判据记为**疑似**，**不构成判死**（AGENTS §7.6：D2 未测字段不得凭先验封禁；`gvkey`/`currency_code` 的非信号判定来自 description 语义，与 alphaCount 低互为印证而非互相推导）。
本地 `field_profile_perf` 的 8/8 `UNUSABLE`（`n_tests=0`）**不作依据**（§1）。

---

## 8. 未做 / 未验证（诚实边界）

1. **8 条模板全部未回测**：只过 `preflight_expressions`（8/8 `valid=true, unknown_fields=[]`）——**S/F/2Y/sub/逐年全未知**，本档只给可设计的产品面。
2. **本轮未发起任何新仿真**（收割优先于重挖，AGENTS §7.5）：宽度/换手读数来自**既有 20 臂的平台重读**
   （`batch_get_alpha_metrics` 20/20 + `get_alpha_details` **11 臂**），不是新回测；`vec_stddev`（lc 7）、`vec_max`（lc 11）、
   `vec_avg(holdings)`（lc 9）、`vec_avg(tradesignificance)`（S 0.91）为前序档读数 `FIELD_insiders1_20261116.md:115-134`，本轮未重开。
3. **`sort_by` / `min_coverage` 不可用**：MCP 工具 schema 无这两参（本轮回显 `sorted_by=null, min_coverage=null`）⇒ 「按 dateCreated 排序拉取」未执行，新鲜度由返回的逐字段 `dateCreated` 手工归纳（§2）。
4. **wqb-db MCP 本轮故障**：`get_field_catalog` / `query_field_profile` 三次调用均返回 `Session not found`（-32600）⇒ 本地对照改走只读 sqlite（`logs/_tmp_ins1_catalog*.py`，`mode=ro`，零写入），**不把工具故障当无解证据**。
5. **更新间隔分布未测**（§5.3）；**平台「最后更新」无属性**（§2）——新鲜度只有 onboard 时点，没有刷新轨迹。
6. **方向推断（M5/M8）未经验证**：无方向字段是结构事实，M5 的正号、M8 的双向都必须在波次里带反号对照臂实证。
7. **拥挤度在动**：`userCount=23/alphaCount=38`（本轮）与 11-15 的 20/29（`FIELD_insiders1_20261116.md:50-51`）变化已记录；本轮只读当日绝对值。
8. **探针档 vs 生产档**：§5 读数全在 `NONE/decay0/nanOFF` 探针档；区域生产档 `decay4/nanON/SUBINDUSTRY`（`tracking/DEU/config/settings.json`）四波未扫（D6 未达，`WAVE_rt-insiders-w4_20261116.md:191`）。

---

## 9. 证据索引（全部为本会话 2026-11-17 平台实读）

**平台调用**
- `get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false)`
  → `count=8, platform_count=8, complete=true, pages_fetched=1`；8 字段全 VECTOR、coverage 全 0.5343、
  逐字段 `dateCreated=2026-07-01`、`pyramidMultiplier=1.6`、`userCount/alphaCount` 见 §1 表（§1）
- 同上 + `data_type="MATRIX"` → `count=0, platform_count=0, complete=true`；`data_type="GROUP"` 同（§3）
- `get_datasets(search="insider", region="DEU", delay=1, universe="TOP500")`（返回全量 catalog 中含）
  → `insiders1 / Global Insider Trading Data / category=insiders / coverage=0.5343 / fieldCount=8 /
  userCount=23 / alphaCount=38 / valueScore=5.0 / pyramidMultiplier=1.6`；description 串台为「RIC↔BBID 映射」（§1）
- `get_operators()` → `count=103`；Vector 类仅 `vec_avg / vec_count / vec_max / vec_min / vec_range / vec_stddev / vec_sum`（§3）
- `batch_get_alpha_metrics([20 条既有探针臂])` → `total=20, success=20, failed=0`；
  S/F/TO/2Y/sub/margin/DD/`failed_ra_count` 与前序档 §4.2 逐值一致（§5.2/§5.4）。
  ⚠ 该工具**不返回** `longCount`/`shortCount`（入参只有 `alpha_ids`，返回体见 schema）⇒ 宽度与方向结论一律取自 `get_alpha_details`，不从 batch 面推断。
- `get_alpha_details` ×11：`P05wnQRW`（`vec_count(valueeur)`，lc=12，CW fail 1.0@2019-10-10）、
  `P05wnQVW`（`vec_count(tradesignificance)`，与前者逐键相同）、`ZYa2jP88`（`vec_count(holdings)`，lc=9，CW fail@2021-07-05）、
  `blaoNGwq`（`greater(vec_count(valueeur),1)`，lc=8，CW fail@2023-01-16）、`leaQ7885`（`subtract(vec_max,vec_min)`，lc=6，CW fail@2023-10-20）、
  `YPa2N57l`（`vec_min(valueeur)`，lc=10，shortCount=0，CW fail@2021-09-06）、`WjlaNPPP`（`vec_sum(valueeur)`，lc=11，shortCount=0，CW fail@2021-09-06）、
  `1YWaoxxm`（`vec_min(value)`，lc=10，shortCount=0，CW fail@2021-09-06）、
  `A1xgnjAQ`（`rank(ts_backfill(vec_sum(valueeur),250))`，lc=294，CW pass）、`88NaO3jV`（lc=382）、`Jj8gnxNA`（lc=383）（§5.2）
- `preflight_expressions`（8 条 §6 模板，`auto_fix_vector=false`）→ `valid=true, expressions=8, unknown_fields=[],
  vector_fields=[], any_changed=false, fields_checked=[holdings,price,shares,tradesignificance,valueeur]`（§6）

**本地只读（wqb-db MCP 故障时的替代通道，零写入）**
- `logs/_tmp_ins1_catalog.py` / `logs/_tmp_ins1_catalog2.py`（`data/wqb.db`，`mode=ro`）：
  `field_profile_perf` 8 行同 id / `fields` 表 0 行 / `datasets` 表无 insider 行 / 8/8 `verdict=UNUSABLE, n_tests=0`（§1）

**代码 / 文档**
- `world-quant-brain-mcp/mcp_core.py:333-349` — `_slim_datafields` 投影 8 键（`dateCreated`/`pyramidMultiplier` 2026-11-17 恢复，
  见 `:343-345` 注释）、description `_truncate(160)`
- `tools/probe/dataset_data_probe.py:13-22` — `NONE` 中性化下 `longCount` 读法；`:127` — VECTOR 探针 `rank(ts_backfill(vec_avg(f),250))`
- `Claude/skills/wq-basket-composition/references/deu-insiders-evidence.md:28-31`（Δ66 1.72 / ts_ir 1.81 / 新鲜度 2.04）、
  `:51-57`（insd1_holdings 2.36 唯一强信号；valueeur 1.14 / shares÷holdings 1.29 / tradesignificance 1.21 / price 1.13 判死）、
  `:52`（HHI 2.20 出自 `significant_value_1`，**非本集字段**，§6 注）
- `tracking/DEU/regular_tower/WAVE_rt-insiders-w4_20261116.md:21-30`（w4 十臂实读：集中度 0.20–0.89、事件频率 0.62、
  金额时钟 0.43）、`:64`（`group_rank(subindustry)` 对集中度核 = S −0.22 / F −0.33）、`:187`（D2：price/value/tradesignificance 未测）、`:191`（D6 未达）
- `tracking/DEU/regular_tower/FIELD_insiders1_20261116.md:107-137`（前序 20 条探针表）、`:50-51`（11-15→11-16 拥挤度 20/29→23/38）
- `docs/reference/EUR/insiders_field_profile_20261107.md:49-51`（nanHandling 空头风险机理，EUR 侧同形）

**前序档案对比**：本文对 `FIELD_insiders1_20261116.md` 的**新增** = ①「字段新鲜度」节（§2，dateCreated 单一批次/近 3 个月零新增）；
② 8 条模板过 `preflight`（§6）；③ CW 满值挂闸实证（§5.2）；④ 本地 `fields` 表 0 行 / `field_profile_perf` UNUSABLE 无测试支撑（§1）；
⑤ 字段级 alphaCount 求和 ≠ 数据集级 alphaCount 的重复计说明（§1）。**复核一致**：8 字段全 VECTOR、coverage 全 0.5343、
幽灵字段 0、可用 `vec_*` 仅 7 个、无 MATRIX/GROUP/EVENT、数值无方向（11/11 实读臂 `shortCount=0`）。
