# GBR / insiders1（Global Insider Trading Data，全球内幕交易）

> 塔：**insiders**（GBR/D1，当前 **0/3 未点亮**；乘数 1.4）
> 画像日期 2026-11-24 · 数据源 `get_datafields(GBR, insiders1, TOP700, D1, filter_sharpe=false)`
> 平台实拉：`count=9 / platform_count=9 / returned=9 / complete=true`
> ⚠ 9/9 字段 `coverage=0.5937`（**真实覆盖，非盲区**）；全部 VECTOR ⇒ 必须 `vec_avg`/`vec_sum` 折叠。
> ⚠ 本集 GBR 历史仅 15 条回测 / 0 过闸，**从未做过全字段画像**；同塔 `insiders12` 已做到反向 ~0.70。

---

## 字段全表（平台实拉 9/9）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `insd1_gvkey` | VECTOR | 0.5937 | 13 | 6 | 发行人的 Compustat Global 公司 ID（元数据） |
| `insd1_holdings` | VECTOR | 0.5937 | 22 | 11 | 交易后内部人持有的总股权 |
| `insd1_price` | VECTOR | 0.5937 | 11 | 8 | 每股交易价（区间披露取最低价） |
| `insd1_shares` | VECTOR | 0.5937 | 28 | 23 | 本次交易股数（或单位） |
| `insd1_tradesignificance` | VECTOR | 0.5937 | 19 | 14 | 交易重要性评分（1 低 – 3 高） |
| `insd1_value` | VECTOR | 0.5937 | 13 | 7 | 交易总价值（原币） |
| `insd1_valueeur` | VECTOR | 0.5937 | 17 | 13 | 交易总价值（欧元） |
| `max_trade_price` | VECTOR | 0.5937 | 3 | 2 | 区间披露的最高价 |
| `transaction_currency_code` | VECTOR | 0.5937 | 3 | 2 | 交易币种 ISO 三字母码（元数据） |

---

## 聚合统计

| 指标 | 值 |
|---|---|
| 字段总数 | 9（全部 VECTOR） |
| coverage 分布 | 9/9 = 0.5937（真实覆盖） |
| alphaCount 合计 / 均值 | 129 / **14.3** |
| alphaCount 最大 / 最小 | 28（`insd1_shares`）/ 3（`max_trade_price`、`transaction_currency_code`） |
| userCount 合计 / 均值 | 86 / **9.6** |
| dateCreated | 9/9 = `2026-07-01` |
| 数据集级 | `name=Global Insider Trading Data` / `category=insiders` / `coverage=0.5937` / `userCount=56` / `alphaCount=103` / `valueScore=4.0` / `pyramidMultiplier=1.4` |

---

## 字段族拆解

| 族 | 字段 | 机制 |
|---|---|---|
| **A 交易规模/方向** | `insd1_shares`、`insd1_value`、`insd1_valueeur` | 交易股数/金额；无内置符号 ⇒ 需用 `insd1_tradesignificance` 或买卖分列（本集无分列）构造方向 |
| **B 存量/持仓** | `insd1_holdings` | 交易后持股（规模基准/分母） |
| **C 价格门控** | `insd1_price`、`max_trade_price` | 内幕人成交价（择时/参照），非独立信号 |
| **D 重要性调制** | `insd1_tradesignificance` | 1–3 分，作门控/权重 |
| **E 元数据** | `insd1_gvkey`、`transaction_currency_code` | 不可作信号 |

---

## 可用性三分

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可做信号** | `insd1_shares`、`insd1_value`、`insd1_valueeur`、`insd1_holdings` | 规模量，需 `rank`/`group_rank` 去量纲；无方向符号是本集最大短板 |
| **② 门控/分母** | `insd1_tradesignificance`（门控）、`insd1_holdings`（分母）、`insd1_price`（参照） | 与 insiders12 的 `positionchangetransactionamount`（天然双边）不同 |
| **③ 元数据** | `insd1_gvkey`、`transaction_currency_code` | 标识符/币种，不作信号 |

### 10.1 全字段实测（insiders1，`rank(ts_backfill(vec_avg(F),250))` @NONE/decay0/trunc0/nanOFF）

> 探针批次：`待发`（与 insiders12 共用 10 臂批）。

| 字段 | 类型 | longCount | shortCount | 有数据 | 备注 |
|---|---|---:|---:|---|---|
| `insd1_gvkey` | VECTOR | 待填 | 待填 | 待填 | 元数据，仅测存在性 |
| `insd1_holdings` | VECTOR | 待填 | 待填 | 待填 | |
| `insd1_price` | VECTOR | 待填 | 待填 | 待填 | |
| `insd1_shares` | VECTOR | 待填 | 待填 | 待填 | |
| `insd1_tradesignificance` | VECTOR | 待填 | 待填 | 待填 | |
| `insd1_value` | VECTOR | 待填 | 待填 | 待填 | |
| `insd1_valueeur` | VECTOR | 待填 | 待填 | 待填 | |
| `max_trade_price` | VECTOR | 待填 | 待填 | 待填 | |
| `transaction_currency_code` | VECTOR | 待填 | 待填 | 待填 | |

---

## 历史与先验

- **同塔 `insiders12`（UK，VECTOR 7 字段，cov 0）**：文献模板 10 臂全负（S −0.13 ~ −0.70），反向天花板 ≈0.70；TO 1.7–2.6% 极低（季度/事件稀疏）。
- **`insiders12` 六法**：`percent` 524/700（74.9%）、`positionchangetransactionamount` 516/700；日更 85%；天然双边 275/241。
- **`insider_agg_matrix`**：34 字段但实测仅 14–24 只/32+36 持仓，历史 45 臂最好 0.81 ⇒ 无 ATOM 主腿资格（不投入）。
- **论坛/论文**：insiders12.md §9 已有 Fidrmuc 2006 / Lakonishok-Lee 2001 / Cohen-Malloy-Pomorski 2012 等 6 篇与 3 帖；本集沿用同一机制证据。

## 适用性结论

- **insiders1 与 insiders12 的差别**：insiders1 无天然买卖符号（insiders12 有 `positionchangetransactionamount`），需自行用 `tradesignificance` 或金额带符号构造方向 ⇒ **机制上劣于 insiders12**。
- **优先级**：insiders12 先做（已有反向 0.70 的读数），insiders1 只作补充（同塔第 3 席候选）。
