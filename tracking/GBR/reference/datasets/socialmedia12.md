# GBR / socialmedia12（Sentiment Data for Equity，社媒情绪）

> 塔：**socialmedia**（GBR/D1，当前 **0/3 未点亮**；乘数 1.3）
> 画像日期 2026-11-24 · `get_datafields(GBR, socialmedia12, TOP700, D1, filter_sharpe=false)`
> 平台实拉：`count=6 / platform_count=6 / returned=6 / complete=true`
> ⚠ 本集在 GBR **无任何历史回测记录**（DB `alphas`/`backtest_results` 零命中）⇒ 全新机制面；塔 0/3。
> ⚠ 仅 2 个 MATRIX 信号字段（`scl12_buzz` / `scl12_sentiment`），其余 4 个是公司实体元数据（VECTOR）。

---

## 字段全表（平台实拉 6/6）

| 字段 | 类型 | cov | αC | uC | 经济含义（平台 description） |
|---|---|---:|---:|---:|---|
| `entity_employee_count` | VECTOR | 0.0 | 24 | 15 | 实体（公司/指数/人）员工数 |
| `entity_profile_summary` | VECTOR | 0.0 | 28 | 24 | 公司简介文本 |
| `entity_sector_name` | VECTOR | 0.0 | 25 | 22 | 实体行业分类 |
| `entity_total_revenue` | VECTOR | 0.0 | 21 | 19 | 公司营收 |
| `scl12_buzz` | MATRIX | 0.0 | 167 | 106 | 相对情绪成交/提及量（relative sentiment volume = 注意力） |
| `scl12_sentiment` | MATRIX | 0.0 | 234 | 123 | 情绪分数 |

---

## 聚合统计

| 指标 | 值 |
|---|---|
| 字段总数 | 6（MATRIX 2 / VECTOR 4） |
| coverage 分布 | 6/6 = 0.0（GBR 元数据盲区） |
| alphaCount 合计 / 均值 | 499 / **83.2** |
| alphaCount 最大 / 最小 | 234（`scl12_sentiment`）/ 21（`entity_total_revenue`） |
| userCount 合计 / 均值 | 309 / **51.5** |
| dateCreated | 6/6 = `2026-07-01` |
| 数据集级 | `name=Sentiment Data for Equity` / `category=socialmedia` / `coverage=0.0` / `userCount=202` / `alphaCount=467` / `valueScore=2.0` / `pyramidMultiplier=1.3` |

---

## 字段族拆解

| 族 | 字段 | 机制 |
|---|---|---|
| **A 注意力（量）** | `scl12_buzz` | 相对提及量：关注度突然上升 → 短期动量/反转（依期限） |
| **B 情绪（方向）** | `scl12_sentiment` | 社媒情绪极性：悲观/乐观 |
| **C 实体元数据** | `entity_employee_count`、`entity_profile_summary`、`entity_sector_name`、`entity_total_revenue` | 公司画像/行业/规模，非日频信号；`entity_sector_name` 可作分组轴 |

---

## 可用性三分

| 分类 | 字段 | 依据 |
|---|---|---|
| **① 可做信号** | `scl12_buzz`（注意力）、`scl12_sentiment`（方向） | MATRIX，可直接 `ts_zscore`/`rank` |
| **② 分组轴** | `entity_sector_name` | 字符串分组（AXIS_ONLY），不作信号 |
| **③ 元数据** | `entity_employee_count`、`entity_profile_summary`、`entity_total_revenue` | 非日频，作规模/文本辅助 |

### 10.1 全字段实测（socialmedia12，`rank(ts_backfill(F,250))` @NONE/decay0/trunc0/nanOFF）

> 探针批次：`待发`（与 insiders/socialmedia5 合并 10 臂）。

| 字段 | 类型 | longCount | shortCount | 有数据 | 备注 |
|---|---|---:|---:|---|---|
| `entity_employee_count` | VECTOR | 待填 | 待填 | 待填 | 元数据，仅测存在性 |
| `entity_profile_summary` | VECTOR | 待填 | 待填 | 待填 | 文本，仅测存在性 |
| `entity_sector_name` | VECTOR | 待填 | 待填 | 待填 | 分组轴 |
| `entity_total_revenue` | VECTOR | 待填 | 待填 | 待填 | 规模 |
| `scl12_buzz` | MATRIX | 待填 | 待填 | 待填 | 注意力主信号 |
| `scl12_sentiment` | MATRIX | 待填 | 待填 | 待填 | 情绪主信号 |

---

## 历史与先验

- **GBR sentiment 类别已判死**（sentiment27/7/33：五年空窗 / 7 个负年 / 三机制面全闭合）——但那是 **sentiment 塔**；socialmedia 塔（0/3）是**不同塔**，且本集从未测过。
- **KOR news 经验**：新闻类成功样本用「新闻条数=关注度」而非情绪极性（EUR 2026-10-29 反模式）；`scl12_buzz`（注意力）优先于 `scl12_sentiment`（极性）。
- **论文**：可沿用「注意力 → 短期收益」与「情绪反转」文献（Tetlock 2007 / Da-Engelberg-Gao 2011 等），但须以本区实测为准。

## 适用性结论

- **机制**：注意力（buzz）与情绪（sentiment）两条，**不互异**（同一社媒源），最多算 1–2 个模板。
- **优先级**：先测 `scl12_buzz` 的水平/差分/时序秩三形态；若 |S|<0.5 按 D15 判死本集，不再铺开。
