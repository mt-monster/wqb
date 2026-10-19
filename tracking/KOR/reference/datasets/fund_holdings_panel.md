# fund_holdings_panel — Global Institutional Fund Holdings

> **字段画像档案** · KOR / TOP600 / Delay=1 · 生成日期 2026-07-19
> 数据来源：`get_datafields(dataset_id=fund_holdings_panel)` 全量拉取（30/30，无夏普过滤隐藏）
> 关联：[`references/institutions.md`](../../../Claude/skills/wq-brain-ra-kor/references/institutions.md)

## 一、数据集总览

| 指标 | 值 |
|---|---|
| 字段总数 | **30**（MATRIX 15 / VECTOR 15，**严格配对**：每个字段都有一个 `_active` 变体） |
| coverage 分布 | 0.9553 × 9（MATRIX 全量）/ 0.887 × 9（VECTOR）/ 0.6626 × 12（`_active` 档） |
| 白空间（alphaCount ≤ 2） | 6 / 30（`secondary_sentiment_total_2` 类，含 ac=1 的 `transaction_cost` 型字段） |
| 塔 | institutions ×1.4 |
| **更新频率** | **日频**（描述含 `on the date` / `the day's trade value`） |
| 已提交 RA | 0（未点亮） |
| **综合判定** | ❌ **判死（3/30 探针，最高 S 0.53）** —— 但 ATOM 形态成立 |

> ⚠ **`_active` 后缀 = 同一指标的「仅活跃账户」口径**，cov 0.6626 明显低于全量口径 0.887/0.9553。
> 按 skill 铁律「cov<0.4→必 backfill」的精神，`_active` 档（cov 0.66）虽未触发硬阈值，但**多头会被压窄**，
> 本轮实测已见该效应（多头 181 vs 空头 445）。

## 二、字段分类（★ 以 description 为准）

| 类 | 经济学角色 | 条数 | 字段 |
|---|---|---:|---|
| **G1 边界交易** | 基金**新建仓 / 完全清仓**事件数与金额 | 4(+4 active) | `boundary_transaction_total`、`boundary_transaction_usd_value` 及其 `_active` |
| **G2 稳定边界交易** | 21 个工作日内**无同股边界交易**的账户发起的建/清仓（更持久） | 1(+1) | `stable_boundary_trade_count_21d` |
| **G3 大额交易** | 交易额 > 基金 AUM 0.5% 的笔数 | 1(+1) | `large_trade_count_50bps` |
| **G4 集中度 HHI** | 持仓/交易价值的 HHI 集中度 | 2(+2) | `herfindahl_index_holdings`、`herfindahl_index_transactions` |
| **G5 拥挤度** | 自定义 crowding 指标 | 1(+1) | `holding_value_distribution_score` |
| **G6 交易分布** | 当日交易价值在账户间的分布指数 | 1(+1) | `transaction_value_distribution_score` |
| **G7 账户广度** | 持有该股的账户数 / 当日交易账户数 | 2(+2) | `holder_account_total`、`transaction_account_total` |
| **G8 信念持仓** | 该股进入其组合**前 30% 权重**的账户数 | 1(+1) | `top_weighted_account_number` |
| **G9 信念交易** | 交易标的是信念持仓的笔数 | 1(+1) | `top_weighted_transaction_number` |
| **G10 权重/价值** | 平均组合权重、总持仓美元值、总交易美元值 | 3(+3) | `mean_security_weight`、`security_holding_usd_value`、`security_transaction_usd_value` |

## 三、0.1 字段质量先验（★ 头部 = 该集最强经济轴）

按 `alphaCount` 降序（头部即最强经济轴）：

| 序 | 字段 | ac | 角色 | 读数 |
|---:|---|---:|---|---|
| 1 | **`boundary_transaction_total`** | **34** | G1 | **建仓/清仓事件数 = 最强轴** |
| 2 | `herfindahl_index_holdings` | 27 | G4 | 持仓集中度 |
| 3 | `holder_account_total` | 26 | G7 | 持有人广度 |
| 4 | `holding_value_distribution_score` | 18 | G5 | 拥挤度 |
| 5 | `top_weighted_account_number` | 14 | G8 | 信念持仓广度 |
| 6 | `mean_security_weight` | 12 | G10 | 平均权重 |

> ⇒ **头部轴 = 机构建仓/清仓事件（流量）**，与 `institutions6` 头部是「存量水平」正好相反。
> 按 skill ②.b：事件型 ⇒ 必须门控 / 控换手，**禁裸 rank**（本轮统一用 `ts_target_tvr_decay`）。

## 四、字段全表（含实测）

| 字段（`*` = 有 `_active` 变体） | 类型 | cov | uc | ac | 类 | 实测 S | 判定 |
|---|---|---|---:|---:|---|---:|---|
| `boundary_transaction_total`* | VECTOR | 0.887 | 26 | **34** | G1 | **0.10** | ❌ 建仓+清仓加总⇒方向相消 |
| `boundary_transaction_usd_value`* | VECTOR | 0.887 | 6 | 6 | G1 | 未测 | ⚠ 同 #1 预期同命运 |
| `stable_boundary_trade_count_21d`* | VECTOR | 0.887 | 10 | 11 | G2 | 未测 | ⚠ 持久性口径，未测 |
| `large_trade_count_50bps`* | VECTOR | 0.887 | 2 | 3 | G3 | 未测 | ⚠ 白空间但覆盖窄 |
| `herfindahl_index_holdings`* | MATRIX | 0.9553 | 25 | 27 | G4 | 未测 | ⚠ 水平集中度 |
| `herfindahl_index_transactions`* | VECTOR | 0.887 | 2 | 2 | G4 | 未测 | ⚠ |
| `holding_value_distribution_score`* | MATRIX | 0.9553 | 16 | 18 | G5 | 未测 | ⚠ crowding 水平量 |
| `transaction_value_distribution_score`* | VECTOR | 0.887 | 4 | 4 | G6 | 未测 | ⚠ |
| **`holder_account_total`** | MATRIX | 0.9553 | 19 | 26 | G7 | **0.53** | ⚠ 有信号但远不足 |
| `transaction_account_total`* | VECTOR | 0.887 | 6 | 6 | G7 | 未测 | ⚠ |
| **`top_weighted_account_number`** | MATRIX | 0.9553 | 11 | 14 | G8 | **0.53** | ⚠ 信念广度，同上 |
| `top_weighted_transaction_number`* | VECTOR | 0.887 | 8 | 8 | G9 | 未测 | ⚠ |
| `mean_security_weight`* | MATRIX | 0.9553 | 10 | 12 | G10 | 未测 | ⚠ 水平量 |
| `security_holding_usd_value`* | MATRIX | 0.9553 | 6 | 7 | G10 | 未测 | ⚠ |
| `security_transaction_usd_value`* | VECTOR | 0.887 | 3 | 3 | G10 | 未测 | ⚠ |
| 另 15 个 `_active` 变体 | — | 0.6626 | ≤9 | ≤10 | 同上 | 未测 | ⚠ cov 低，多头被压窄 |

## 五、实测记录（ATOM 形态）

模板同 `institutions6`。全部 `pyramid_short="institutions"`、`effective=1` ⇒ **ATOM 形态成立**。

| alpha | 核心结构 | S | F | TO | 2Y |
|---|---|---:|---:|---:|---:|
| `QPYELJ8M` | `vec_sum(boundary_transaction_total)` | **0.10** | 0.02 | 0.264 | −0.46 |
| `bl8vEXap` | `ts_delta(holder_account_total, 66)` | **0.53** | 0.26 | 0.115 | 0.39 |
| `VkdOJwlV` | `ts_delta(top_weighted_account_number, 66)` | **0.53** | 0.25 | 0.214 | −0.03 |

## 六、结论与死因

**判死依据（3/30 探针，快判死阈值为 8 探针无 |S|≥0.5；本轮 2 条已达 0.53，未触发硬阈值但信号明确在 0.5 弱档）**：

1. **头部轴（G1 边界交易）方向相消**：`boundary_transaction_total` 把新建仓与完全清仓**加总**，
   两个相反方向的事件互相抵消 ⇒ S 0.10。数据集**没有提供净买卖字段**，
   而 `institutions6` 有净额对却同样失效（季频摊平）。
2. **广度量（G7/G8）天花板 0.53**：持有人数与信念持有人数的 66 日变动都只到 0.53，
   且 2Y 分别 0.39 / −0.03 ⇒ **ladder 也不可用**。
3. 与 `institutions6`（最高 0.80）合并看，**两个机构持仓数据集 7 字段最高 |S| = 0.80**
   ⇒ 跨数据集规律成立。

> **未测字段的处置建议**：G2（稳定边界交易，持久性口径，机制上比 G1 更干净 —— 它排除了「同股反复交易」
> 的噪声，是**方向未知的净事件**，值得 1 条探针）、G4 变动量（集中度下降 = 机构分散化）各值得 1 条。
> 其余（G3/G6/G9/G10 及全部 `_active`）预期同命运，不建议投入。
## 十、覆盖补测（2026-07-20 回填）

| 字段 | 表达式 | S | F | TO | 2Y | 多空 | 判定 |
|---|---|---:|---:|---:|---:|---|---|
| `herfindahl_index_holdings_active`（cov 0.6626） | `ts_delta(,66)` | **0.52** | 0.26 | 0.1189 | 0.60 | 186/442 | ❌ **`_active` 家族既窄又弱（vs 全量 0.77）** |

**覆盖度终值：7/30 字段实测**（含 `_active` 家族代表）。
`herfindahl_index_holdings_active` 的失败说明：**cov 0.6626 的「仅活跃账户」口径不是 prod 白空间，而是更窄更弱的截面**（多空 186/442，比全量口径 234/400 更失衡）。

**⇒ 本数据集判死结论不变**：最高 |S| = 0.77（HHI 变动），无一字段达到 1.0。
