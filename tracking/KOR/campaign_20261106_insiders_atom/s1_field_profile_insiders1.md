# S1 · insiders1 全字段画像（9/9）

> 数据源：`get_datafields(KOR, TOP600, D1, dataset_id=insiders1, filter_sharpe=false)`，2026-11-06。
> 前置画像（更详细）见 [reference/datasets/insiders1.md](../../reference/datasets/insiders1.md)。

## 0. 元信息

| 项 | 值 |
|---|---|
| dataset | `insiders1` · Global Insider Trading Data（Compustat Global 口径） |
| category / 塔 | `insiders`（KOR/D1/INSIDERS **0/3**，乘数 1.2） |
| 字段数 | **9，全 VECTOR**；coverage **.3526**（9 个字段完全一致 ⇒ 同一份报表并列列） |
| aC 分布 | `gvkey` 178 / `shares` 112 / `value` 107 / `holdings` 57 / `price` 45 / `valueeur` 45 / `tradesignificance` 40 / `transaction_currency_code` 15 / `max_trade_price` 5 |

## 1. 字段全表

| # | 字段 | 类型 | cov | uC | aC | 语义 | 更新频率 | 分布特征 | 可用性 |
|---|---|---|---:|---:|---:|---|---|---|---|
| 1 | `insd1_gvkey` | VECTOR | .3526 | 55 | 178 | Compustat Global 公司标识 | 事件 | ID | ⛔ 标识 |
| 2 | `insd1_shares` | VECTOR | .3526 | 72 | 112 | 本笔交易股数（无符号） | 事件 | 重尾、跨 6 数量级 | ✅ 强度腿 |
| 3 | `insd1_value` | VECTOR | .3526 | 59 | 107 | 本笔交易金额（原币 KRW） | 事件 | 重尾 | ✅ 强度腿（与 `valueeur` 同源，只取一） |
| 4 | `insd1_holdings` | VECTOR | .3526 | 32 | 57 | **交易后该内部人持股总数** | 事件 | 单边恒正、重尾 | ⚠ 唯一方向代理：需相邻笔差分 |
| 5 | `insd1_price` | VECTOR | .3526 | 30 | 45 | 每股价（区间取最低） | 事件 | 右偏 | ⚠ 与 `max_trade_price` 构成区间 |
| 6 | `insd1_valueeur` | VECTOR | .3526 | 34 | 45 | 交易金额（欧元） | 事件 | 与 `value` 同源 | ⛔ 同源重复，取 eu 引入汇率噪声 |
| 7 | `insd1_tradesignificance` | VECTOR | .3526 | 27 | 40 | 交易重要性 1/2/3 | 事件 | 离散 3 档 | ⚠ **门控/权重**，非信号 |
| 8 | `transaction_currency_code` | VECTOR | .3526 | 10 | 15 | 币种码 | 事件 | 类别 | ⛔ 编码 |
| 9 | `max_trade_price` | VECTOR | .3526 | 5 | 5 | 区间报价上限 | 事件 | 右偏 | ⚠ 可做 `max/price` 区间宽度，cov .35 太薄 |

## 2. 结构性缺陷（判据）

1. **无买卖方向码**（无 acquired/disposed、无 transaction code）⇒ 无法构造「净买入」；`holdings` 相邻差分是唯一代理，但同一内部人跨笔匹配在平台侧不可控 ⇒ **代理失真风险高**。
2. **cov .3526** ⇒ 只有 1/3 股票有读数。论坛实证：cov<0.7 的字段横截面排序等于在噪声上排序（`buy_sell_ratio` cov .6x ⇒ S 0.7 卡子宇宙闸）。
3. 9 字段中 **4 个是元数据/同源重复**（gvkey / currency / valueeur / max_trade_price 边际）⇒ 真可用 3–4 个。

## 3. 裁定

⛔ **本轮不派主力波**。理由：与 insiders5 同塔同机制但更弱（无方向 + 覆盖 .35），任何在 insiders1 上能成立的机制，在 insiders5 上都有更干净的字段。仅当 insiders5 完全榨干（10 颗交不出）时，才用 1 波 4 条探针（`tradesignificance` 门控 × 金额强度）做最后手段。
