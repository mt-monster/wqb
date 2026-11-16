# DEU / D1 / TOP500 — `insiders1` 字段档案（S1）

> 生成：2026-11-15｜口径：`region=DEU, universe=TOP500, delay=1, instrumentType=EQUITY`
> 数据源：**平台实读**（`mcp__wq-brain-http__get_datafields` / `get_datasets` / `get_operators` /
> `preflight_expressions` + 本轮 12 条单发探针仿真）。**本地画像只作对照，不作依据**。
> 塔位：`DEU/D1/INSIDERS`（`get_datasets` 实读 `pyramidMultiplier=1.6`）。

---

## 0. 一句话结论

`insiders1` 在 DEU/TOP500/D1 只有 **8 个字段，全部 VECTOR，全部 0.5343 覆盖**；它是一个
**事件驱动的稀疏脉冲集**（同日仅 8–11/500 只有值），**没有买卖方向字段**，
唯一强信号是 `insd1_holdings`（DEU 既有 30 波实测的口径，本档 §6 M2 沿用），而它恰好是**宽度最窄**的字段（193/500，比同类低 34%）。
先把 `vec_*` 降维、再上 ≥60 日时间平滑，是这个集的硬性入场条件。

---

## 1. 平台字段全表（平台实读，8/8）

`get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false)`
返回 `count=8, platform_count=8, complete=true, pages_fetched=1` ⇒ **全量拉取，无截断**。

| # | 字段 | type | coverage | userCount | alphaCount | description（语义唯一依据） |
|---|---|---|---|---|---:|---:|---|
| 1 | `insd1_holdings` | VECTOR | 0.5343 | 11 | 13 | Total equity share holdings of the insider **after the transaction**（交易后内部人持股存量） |
| 2 | `insd1_valueeur` | VECTOR | 0.5343 | 10 | 12 | Total value of the transaction **in Euro**（欧元计交易总额） |
| 3 | `insd1_tradesignificance` | VECTOR | 0.5343 | 7 | 9 | Significance score of the trade (**1 = low, 3 = high**)（交易重要性序数评分） |
| 4 | `insd1_shares` | VECTOR | 0.5343 | 4 | 5 | **Number of shares (or units) traded** in the transaction（本次成交股数） |
| 5 | `insd1_price` | VECTOR | 0.5343 | 3 | 4 | Transaction **price per share**; 区间报则取**最小值** |
| 6 | `insd1_value` | VECTOR | 0.5343 | 2 | 2 | Total value of the transaction **in original currency**（原币交易总额） |
| 7 | `insd1_gvkey` | VECTOR | 0.5343 | 1 | 1 | Compustat Global Company Identifier（**标识符**） |
| 8 | `transaction_currency_code` | VECTOR | 0.5343 | 1 | 1 | Three-letter **ISO currency code**（**分类标签**） |

**幽灵字段 = 0。** `preflight_expressions` 对全部 8 个字段返回
`unknown_fields=[] / unknown_soft=[] / platform_field_count=8`，与 `get_datafields` 的 8 条逐 id 一致
⇒ 本数据集在 DEU/TOP500/D1 上**没有本地画像幽灵字段问题**。

⚠ **但本地 `field_catalog` 的拥挤度已过期**（`get_field_catalog("DEU","insiders1")` 实读）：
本地记 `holdings 1/1、valueeur 1/1、tradesignificance 1/1、shares 1/1、price 0/0、value 0/0`，
平台实读是 `11/13、10/12、7/9、4/5、3/4、2/2`。
⇒ `S0_TOWER_SCAN_20261115.md:224` 的「几乎无人用过（userCount=1/alphaCount=1）」是**本地 catalog 读数**，
真实拥挤度更高一档（但仍属低拥挤，`alphaCount` 最多 13）。本地 catalog 还把 `data_type` 标成 `MATRIX`
（8 字段实为全 VECTOR），同一处失真。

⚠ **数据集级 description 不可信**：`get_datasets(search="insiders1")` 返回的 description 是
「RIC ↔ BBID 标识符交叉映射」——与内部人交易无关，是平台侧的元数据串台。
**语义只认字段 description**（这也是本档案全部维度归纳的依据）。

---

## 2. 类型与降维要求

- **全 VECTOR，无 MATRIX / GROUP / EVENT**。实读：同一入参加 `data_type="MATRIX"` → `count=0, platform_count=0, complete=true`；
  加 `data_type="GROUP"` → 同样 `0/0`。⇒ 本档案**不涉及** EVENT 的 `ts_event_*` 问题，也不涉及 GROUP 轴字段。
- **平台 Vector 类算子只有 7 个**（`get_operators` 实读，共 103 个算子）：
  `vec_avg(x)` / `vec_sum(x)` / `vec_max(x)` / `vec_min(x)` / `vec_stddev(x)` / `vec_range(x)` / `vec_count(x)`。
  ⚠ **没有** `vec_ir` / `vec_skewness` / `vec_kurtosis` / `vec_choose` ⇒ 「内部人之间的离散度」只能靠
  `vec_stddev` / `vec_range` 表达，别照抄别区写法。
- **★ 空向量语义实测（本轮探针，决定本档 6 个模板的写法：5 条用 `vec_sum`、1 条用 `vec_max`）**：
  `rank(vec_sum(insd1_holdings))` 同日 `longCount=8`（与 `rank(vec_avg(...))` 的 8 完全相同）、
  `rank(vec_max(insd1_valueeur))` 同日 `lc=11`（与 `vec_avg` 的 11 相同）
  ⇒ **当日无交易时 `vec_sum` / `vec_max` 返回 NaN，不是 0**（否则会跑成满 500 个持仓）。
  结论：`vec_sum` 之类的聚合**不会**把「没有交易」变成 0，因此
  `ts_backfill(vec_sum(x),250)` 是必需的，否则整个截面只剩个位数股票。
- **降维写法基线**（本仓 probe SOP 的 VECTOR 口径，见 `tools/probe/dataset_data_probe.py:125-128`）：
  `vec_avg(<field>)` → 再进时序/截面算子。所有模板一律先 `vec_*` 后进算子，**禁止裸用字段**。

---

## 3. 语义维度（按 description 归纳，字段名不作依据）

| 维度 | 代表字段 | 经济含义（据 description 推导） |
|---|---|---|
| **内部人持仓存量（水平）** | `insd1_holdings` | 「交易后内部人持有的总股数」= 交易完成后的**状态量**（stock），不是流量。跨笔相加得「公司层面的内部人合计持股」。 |
| **交易金额（价值/规模）** | `insd1_valueeur`（欧元，跨市场可比）／`insd1_value`（原币） | 「交易总价值」= 每笔交易的**规模**。两字段语义相同、仅计价币种不同 ⇒ **互为替换而非互补**，同用会重复计规模。 |
| **交易数量（规模/广度）** | `insd1_shares` | 「本次成交股数」= 规模口径之一，与金额口径高度共线（金额≈股数×价）。 |
| **交易价格** | `insd1_price` | 「每股成交价，区间报则取下限」= 成交价快照，**不是**市场收盘价；与收盘价做比才有「内部人成交折溢价」含义。 |
| **交易重要性（序数）** | `insd1_tradesignificance` | 平台自评的 1–3 序数显著性。**序数不是基数**：取 mean/sum 只能当加权用，不能解释成「重要性金额」。 |
| **交易强度（派生，无原生字段）** | `shares` × `price` ÷ `value` / `value` ÷ `holdings` / `vec_max` ÷ `vec_sum` | 本集**没有**方向、没有笔数、没有股本字段 ⇒ 强度类指标只能由上述基数派生（每笔均额、集中度、成交额占持股比）。 |
| **标识符（元数据）** | `insd1_gvkey` | Compustat 公司码 ⇒ **非信号**；实测 `vector_neut` 之类可用它做对齐，但不得进信号代数。 |
| **分类标签（元数据）** | `transaction_currency_code` | ISO 币种码 ⇒ **非信号**（分类标签，取均值/求和无经济含义）。 |

**★ 结构性缺口（本集最重要的一条）**：8 个字段里**没有任何买卖方向字段**
——`value`/`valueeur`/`shares` 都是「交易规模」，正负号不携带方向。
⇒ **方向只能由 `insd1_holdings` 的时间差分推断**（同期增持=正、减持=负）。
该缺口在 EUR（`docs/reference/EUR/insiders_field_profile_20261107.md:41`）、
DEU BA6 设计（`tracking/DEU/atom_orthogonal/waveBA6_insiders1_pool_design_20261110.md:3`）两处独立记述，口径一致。

---

## 4. 字段级覆盖实读（coverage / 更新频率 / 宽度塌缩）

### 4.1 `coverage` 在本集**不携带字段级信息**

平台 8 个字段的 `coverage` **全为 0.5343，且与数据集级 coverage（`get_datasets` 的 0.5343）逐位相同**
⇒ 这个读数在本集上是**数据集级值的复制**，无法区分字段。**不得用它判字段可用性**
（也正是本档不用覆盖率排序的原因）。

### 4.2 宽度实测（本轮 12 条单发探针，平台真读数）

口径：`rank(<vec_减维>)`，`neutralization=NONE`、`decay=0`、`truncation=0.01`、`nanHandling=OFF`。
`rank` 恒正 ⇒ `is.longCount` 直接等于**该口径下有值的股票数**
（读法出处 `tools/probe/dataset_data_probe.py:17-19`；`lc` 为平台终态单值，非日均序列）。

| 字段 | 同日宽度 `rank(vec_avg/F)` | 250 日宽度 `rank(ts_backfill(vec_avg(F),250))` | 同日/宇宙 | 250d/宇宙 |
|---|---:|---:|---:|---:|
| `insd1_holdings` | **8** | **193** | 1.6% | **38.6%** |
| `insd1_valueeur` | 11 | 294 | 2.2% | 58.8% |
| `insd1_gvkey` | 11 | 293 | 2.2% | 58.6% |
| `insd1_price` | — | 294 | — | 58.8% |
| `insd1_shares` | — | 293 | — | 58.6% |
| `insd1_tradesignificance` | — | 294 | — | 58.8% |
| `insd1_value` | — | 294 | — | 58.8% |
| `transaction_currency_code` | — | 未探（分类标签，非信号） | — | — |

（同日三行来自 `logs/_tmp_insd1_sameday.py`；250 日七行来自 `logs/_tmp_insd1_deu_probe.py`；
逐条 alpha id：`VkNlp3NV / N1PjpRrq / O0Wmpk21 / omazKAQn / A1xawbel / zqdo9WM8 / d5a7x07Y`（250d），
`kqam3vA8 / Jj8XpWx2 / Jj8Xp2rl`（同日）。）

### 4.3 三条宽度塌缩结论

1. **同日宽度塌缩到个位数**：任何**不做时间平滑**的 insiders1 表达式，截面只有 **8–11 只股票**（TOP500 的 1.6–2.2%）。
   ⇒ 裸 `vec_*` / 短窗 `ts_delta` 出来的东西不是「弱信号」，是**没有截面**。**≥60 日回填/平滑是入场条件**。
2. **`insd1_holdings` 是宽度最窄的字段**：250 日只触及 **193/500（38.6%）**，比同类（293–294，≈58.7%）**低 34%**。
   含义：约 **1/3** 的有内部人交易的股票（293 → 193，缺 34%）**没有**交易后持股申报。
   这解释了为什么基于 holdings 的构造必须长窗（DEU 已验证的那条是 Δ66 且先 132 日回填）。
3. **7 个数值字段的「纯 rank 基线」S 全部落在 0.69–0.79 的窄带内**（`VkNlp3NV 0.77 / omazKAQn 0.79 /
   d5a7x07Y 0.75 / N1PjpRrq 0.75 / A1xawbel 0.73 / zqdo9WM8 0.73 / O0Wmpk21 0.72`，换手 0.9%–2.9%）
   ⇒ 这些字段的截面区分主要来自**同一个共同因子（「有没有内部人交易 / 交易规模」）**，
   而不是各自的经济含义。**叠加它们不会得到独立信息**（也旁证了「同集多字段相加不产生新信息」）。
   ⚠ 口径提醒：`NONE` 中性化的 `rank` 基线是**全多头不可交易件**，S 值只用于比较「有没有截面/是否同源」，不是 alpha 质量。

### 4.4 更新频率

- **平台 MCP 面不暴露频率属性**：`get_datafields` 的投影只保留
  `id / type / coverage / userCount / alphaCount / description` 六个键
  （`world-quant-brain-mcp/mcp_core.py:341-343`）⇒ 「声明更新频率」**读不到**，本档记为 **NOT_MEASURED**，不猜。
- **从 description 可确定它是事件驱动而非周期**：每条记录是「该笔交易」的股数/金额/价格/重要性，
  不是日/周/月的预聚合快照 ⇒ 更新节奏 = 内部人申报节奏（逐笔、不规则）。
- **可测的量级代理（已测）**：同日触达 1.6–2.2% 的股票、250 日触达 38.6–58.8% ⇒
  **约 6 成股票一年内至少有一次申报，但日频只有 2%**。
- **未测（如需再补一条）**：`rank(days_from_last_change(vec_avg(F)))` 或
  `rank(ts_count_nans(vec_avg(F),250))` 单发探针可给出每股更新间隔；本轮未跑，不填数。

---

## 5. 结构性约束（写模板前必须知道）

- **ATOM 口径**：本集所有字段同属一个 dataset ⇒ 单集表达式即 ATOM，**免 IS_LADDER**（`_basket-and-atom.md:35-61`）。
  ⚠ `insiders1` 与 `insider_agg_matrix` 是**两个** dataset，混用即掉出 ATOM（同文件 `:73-76`）。
- **闸5（等权腿相加）**：允许「单字段 × 单形态 × 多窗平滑」，禁止 `add(腿A, 腿B)`
  （`_basket-and-atom.md:79-92`）。本档 8 个骨架已用判定器静态核验：
  `_find_equal_weight_leg_add` 全部 **0 命中**（脚本 `logs/_tmp_gate5_insd1.py`；
  阳性对照 `add(ts_delta(holdings), ts_zscore(valueeur))` 正确命中 2 腿）。
- **中性化**：S0 档记「主腿必须 FAST，SUBINDUSTRY 已三波证死」（`S0_TOWER_SCAN_20261115.md:237`）
  ⇒ 派发时 `neutralization` 取 FAST。注意：模板里的 `group_rank(x, subindustry)` 是**信号内分组轴**，
  与中性化设置是两回事，不冲突。
- **方向**：无方向字段 ⇒ 每个含「增持/减持」语义的模板都必须在同波带一条**反号对照臂**，
  用实测定向（BA6 的 I1/I2 就是这么做的，见 `waveBA6_...:22-23`）。

---

## 6. 模板骨架（8 个不同机制，非换窗口）

统一约定：`F` = 字段；全部先 `vec_*` 降维；全部单表达式（无跨腿 add）；全部只用 insiders1 字段（ATOM）。
「算子数」= 本仓 `wq-alpha-gate-push-op-min/scripts/op_count.py --file logs/_tmp_insd1_templates.txt` 实计：
**M1=3 / M2=4 / M3=7 / M4=7 / M5=5 / M6=5 / M7=9 / M8=8**，全部 ≤12。
「先验」列的分级：
**A** = DEU 已有单腿实测支持；**B** = 跨区/文献先验，DEU 未测；**C** = 构成件在 DEU 已判死，属新几何/低先验。

| # | 机制（与别的模板差在哪） | 骨架表达式 | 预期符号 | 先验 |
|---|---|---|---|---|
| **M1** | **存量水平**（状态量，不是变化）：内部人合计持股的相对高低 | `group_rank(ts_backfill(vec_sum(insd1_holdings),250), subindustry)` | **正**（alignment：持股越高利益绑定越强；反向假说 entrenchment 给负 ⇒ 须定向） | B（DEU 未测水平腿） |
| **M2** | **净增持流**（一阶差分）：66 日内的合计持股变化 | `group_rank(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66), subindustry)` | **正**（Lakonishok-Lee 2001；Rozeff-Zaman：变化 > 水平） | **A**：DEU「A 单腿 Δ66」S 1.72（`deu-insiders-evidence.md:31`）；`insd1_holdings` 单集最好 S 2.36（`:51`） |
| **M3** | **单笔规模的位置**（每笔均额在自身 1 年历史中的秩）：大单 = 信息交易者 | `group_rank(ts_rank(divide(ts_backfill(vec_sum(insd1_valueeur),250), ts_backfill(vec_count(insd1_valueeur),250)),252), subindustry)` | **正**（Seyhun 1986：单笔越大越有信息） | C/B（DEU 未测此形状） |
| **M4** | **序数显著性加权**（金额 × 重要性 1–3）：大且重要 | `group_rank(ts_sum(multiply(ts_backfill(vec_sum(insd1_valueeur),250), ts_backfill(vec_avg(insd1_tradesignificance),250)),66), subindustry)` | **正** | C：`valueeur` 单腿 1.14、`tradesignificance` 单腿 1.21 均已判死（`:55,:57`）⇒ 只有「加权后新几何」才值得一试 |
| **M5** | **日内集中度**（最大单笔 ÷ 当日总额）：单笔支配 = 信念集中 | `group_rank(ts_mean(divide(vec_max(insd1_valueeur), vec_sum(insd1_valueeur)),66), subindustry)` | **正**（集中度越高，信息越可能来自少数知情者） | B/A：DEU 最强机制是「集中度」(S 1.74–2.20)，但它来自**姊妹集** `insider_agg_matrix` 的 SV1..4（`:28-32`）⇒ 本模板是**用 insiders1 原生向量重建**，不是重跑 |
| **M6** | **流动的持续性/信噪比**（增持均值 ÷ 其波动）：持续增持 vs 一次性脉冲 | `group_rank(ts_ir(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),22),252), subindustry)` | **正**（持续买入 = 更强信念；一次大买可能只是流动性事件） | **A**：DEU「B 单腿 ts_ir」S 1.81（`deu-insiders-evidence.md:29`） |
| **M7** | **条件门控状态机**（只在净增持时持仓，否则维持/不建仓）：事件驱动持有 | `trade_when(greater(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66),0), group_rank(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66), subindustry), -1)` | **正偏态**（只在信号触发时暴露 ⇒ 收益分布右偏、换手下降） | B（CMP 2012 机会主义；DEU 未测 trade_when 形态） |
| **M8** | **规模正交化**（把增持信号对「交易活动规模」做残差）：剥离规模后的净信息 | `vector_neut(group_rank(ts_delta(ts_backfill(vec_sum(insd1_holdings),250),66), subindustry), rank(ts_backfill(vec_sum(insd1_valueeur),250)))` | **正**（残差部分 = 与规模无关的增持信息） | B（DEU 未测正交化） |

**为什么这 8 个算「不同机制」而不是换窗口**：M1 是水平、M2 是一阶差分、M3 是单笔规模位置、
M4 是序数加权、M5 是日内集中度、M6 是流的信噪比、M7 是条件持有（状态机）、M8 是正交化残差。
其中 M1/M2/M6 都基于 holdings，但分别读**水平 / 变化 / 变化的稳定性**三种不同的量。

**已死机制（DEU 实测，别重跑）**：`insd1_valueeur` / `insd1_value` 单腿（1.14）、
`insd1_shares ÷ holdings`（1.29）、`insd1_tradesignificance` 单腿（1.21）、`insd1_price`（1.13）
（`Claude/skills/wq-basket-composition/references/deu-insiders-evidence.md:54-61`）。
⚠ 该表的「✅ 唯一强信号 `insd1_holdings` S 2.36」与本档 M2 同族；**M2 不是新机制，是已知最强腿**。
**真正新增的几何只有 2 条：M5（日内集中度）与 M8（规模正交化）**——BA6 十模板里没有任何一条用
`vec_max ÷ vec_sum` 或用 `vector_neut` 剥离规模。M1/M3/M6/M7 与 BA6 的 I7/I6/（B 腿 ts_ir）/I9 是**同族不同参数化**，
派发前必须先查 BA6 是否已跑过（见 §7 逐条映射），别把它们记成新机制。

---

## 7. 与既有 DEU 设计（BA6 十模板）的重叠矩阵

`tracking/DEU/atom_orthogonal/waveBA6_insiders1_pool_design_20261110.md:18-29` 已有 10 条设计，重叠如下：

| BA6 | 与本档关系 |
|---|---|
| I1（Δ66 holdings，`vec_avg` + 132 回填） | ≈ **M2**（本档用 `vec_sum` + 250 回填）⇒ 同机制，不同聚合口径，**不是新模板** |
| I2（I1 反号） | 本档要求每波带反号对照臂，未单列 |
| I3（valueeur 均值的强度） | 本档不单列（已判死单腿 1.14） |
| I4（tradesignificance 水平） | 本档不单列（已判死 1.21） |
| I5（增持 × 显著性 交互） | ≈ **M4** 的变体（本档是金额 × 显著性） |
| I6（平均单笔金额，`ts_mean` 22） | ≈ **M3**（本档改成 `ts_rank` 252 位置，形状不同） |
| I7（holdings `ts_rank` 252） | 与 **M1** 同用水平信息，但 M1 是组内秩、I7 是时序秩 ⇒ 可并存 |
| I8（`vec_count(shares)` 交易笔数/广度） | **本档缺**：见 §6 说明——`vec_count` 可做「参与广度」，是第 9 条可用机制，本档未纳入（未验证空向量语义对 `vec_count` 的影响） |
| I9（显著性门控的增持） | ≈ **M7**（本档用「净增持>0」门控，不用显著性门控） |
| I10（holdings `ts_std_dev` 252，反向） | 本档不单列，可作 M1 的反向对照 |

⇒ 真正**新增**（BA6 未覆盖）：**M5（日内集中度）**、**M8（规模正交化）**、
**M6 的 holdings 版 `ts_ir`**（BA6 的 ts_ir 来自 B 腿，口径未记）、以及 **M1 的组内秩水平版**。

---

## 8. 本档的未做 / 未验证（诚实边界）

1. **没有任何模板被回测**：8 条骨架只过了 `preflight_expressions`（19/19 valid）与闸5 静态判定，
   **S/F/2Y/sub/逐年 全部未知**。本档只给「可设计的产品面」，不给收益承诺。
2. **`transaction_currency_code` 未探针**：作为分类标签不进信号，未跑仿真（不用「没数据」冒充「不该用」——
   它的 250 日宽度未知）。
3. **更新频率只有量级代理**，没有每股更新间隔（§4.4 给了补测写法，本轮未跑）。
4. **`is.longCount` 是平台终态单值**：本档按本仓 probe SOP 的读法把它当「该口径下有值股票数」，
   未验证平台是否按末日还是日均计算（两种解释下「个位数 vs 293」的结论不变）。
5. **`vec_count` 的空向量语义未验证**：M8 之外若要用「交易笔数」类机制（BA6 I8），需先补一条
   `rank(ts_backfill(vec_count(insd1_shares),250))` 探针。

---

## 9. 证据索引

**平台读数（本会话实读）**
- `get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false)`
  → 8 字段全 VECTOR、cov 0.5343、`complete=true`、`platform_count=8`（§1 表）
- `get_datasets(search="insiders1", region="DEU", delay=1, universe="TOP500")`
  → `insiders1` / Global Insider Trading Data / category=insiders / coverage 0.5343 / fieldCount 8 /
  userCount 20 / alphaCount 29 / valueScore 5.0 / pyramidMultiplier 1.6
- `get_datafields(dataset_id="insiders1", region="DEU", delay=1, universe="TOP500", filter_sharpe=false, data_type="MATRIX")` → `count=0 / platform_count=0 / complete=true`
- `get_datafields(..., data_type="GROUP")` → `count=0 / platform_count=0 / complete=true`
- `get_operators()` → 103 算子；Vector 类恰为 `vec_avg/vec_sum/vec_max/vec_min/vec_stddev/vec_range/vec_count`
- `preflight_expressions(19 条, auto_fix_vector=false, dataset_id="insiders1")`
  → `valid=true, unknown_fields=[], platform_field_count=8, any_changed=false`
- `get_field_catalog("DEU","insiders1")`（本地，仅对照）→ 8 字段、`data_type=MATRIX`（失真）、拥挤度过期
- 探针（DEU/TOP500/D1，`NONE`+`decay 0`+`truncation 0.01`+`nanHandling OFF`）：
  `logs/_tmp_insd1_deu_probe.json`（7 条 250d）、`logs/_tmp_insd1_deu_sameday.json`（3 条同日）、
  `logs/_tmp_insd1_deu_vecsum.json`（2 条空向量语义）

**代码 / 文档**
- `world-quant-brain-mcp/mcp_core.py:341-343` — datafields 投影只留 6 键（频率属性不可见）
- `tools/probe/dataset_data_probe.py:17-19` — `NONE` 中性化下 `longCount` 的读法
- `tools/probe/dataset_data_probe.py:125-128` — VECTOR 探针的 `vec_avg` 降维写法
- `Claude/skills/wq-brain-campaign-toolkit/scripts/_gate_expr_checks.py:826-845` — 闸5 判定器文档
- `Claude/skills/wq-brain-campaign-toolkit/scripts/_gate_expr_checks.py:469-476` — 同数据集腿相加的豁免口径
- `Claude/skills/wq-basket-composition/references/deu-insiders-evidence.md:47-64` — DEU insiders 判死清单（S 读数来源）
- `Claude/skills/wq-brain-ra-deu/references/_basket-and-atom.md:35-92` — ATOM 免 IS_LADDER、闸5 合法空间
- `tracking/DEU/atom_orthogonal/waveBA6_insiders1_pool_design_20261110.md:18-29` — BA6 十模板
- `docs/reference/EUR/insiders_field_profile_20261107.md:40-41` — EUR 侧同集（9 字段）与「无方向字段」记述
- `docs/reference/USA/insiders1_field_profile_20261031.md:52-73` — USA 侧同集（45 字段）逐笔族实测
- `tracking/DEU/regular_tower/S0_TOWER_SCAN_20261115.md:224,:237` — 本地 catalog 拥挤度（已过期）与中性化口径

**本轮自建脚本（一次性，`logs/` 下，gitignore）**
- `logs/_tmp_insd1_deu_probe.py` / `logs/_tmp_insd1_sameday.py` / `logs/_tmp_insd1_vecsum.py`
- `logs/_tmp_gate5_insd1.py`（闸5 静态判定，含阳性对照）
- `logs/_tmp_insd1_templates.txt`（供 `op_count.py --file` 统计算子数）
