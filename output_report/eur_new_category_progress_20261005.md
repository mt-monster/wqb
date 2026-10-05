# EUR 换 category 挖掘进度报告（2026-10-05）

> 用户指示：**锁定 EUR 不换 region，继续推进 RA 挖掘，换数据集 category**
> 本报告覆盖 INSIDERS / INSTITUTIONS / MODEL(quant_factor_lib) 三个新 category 的首次探矿

## 一、已记录的范围约束

已写入项目长期记忆 `MEMORY.md §0.2`：
- **锁定 EUR，不换 region**；允许在 EUR 内换 dataset / category。
- 遵守既有纪律：**提交需用户当轮明确指示**（此前有自行提交被纠正的先例）。

## 二、选新族的判据（我定的）

优先「**机制与生产池不同源** + **低拥挤**」，避开经典异象（修订/动量/价值）。
用系统筛法一次性拿到候选池：

```sql
SELECT name,category,field_count,alpha_count,value_score FROM datasets
WHERE region_id=6 AND field_count>=20 AND alpha_count<800
ORDER BY value_score DESC, alpha_count ASC LIMIT 30
```

## 三、三个新 category 的实测结果

| category | 数据集 | 字段 | alphaCount | 最佳 S | 最佳 2Y | 结论 |
|---|---|---|---|---|---|---|
| **INSIDERS** | `insider_agg_matrix` | 34 | 46 | **0.98** | 1.81 | 弱 |
| **INSTITUTIONS** | `fund_holdings_panel` | 30（全 VECTOR） | 24 | **0.87** | **1.69** | 弱 |
| **MODEL** | `quant_factor_lib` | 126（全 VECTOR） | **1** | **1.20** | 0.60 | 弱 |

### 3.1 INSIDERS —— 机制方向对，强度不足
- `total_top_buy_shares`（高管买入）正向但弱（S 0.48–0.67）；
  **`reverse(卖出)` 只有 0.12 ⇒"内部人卖出→下跌"在 EUR 不成立**（卖出多为分散化）。
- 换手偏高（0.06–0.25）⇒ 属快信号，与前面 risk/analyst 族的慢信号规律不同。

### 3.2 INSTITUTIONS —— 2Y 最好，但 S 太低
- **J1 `rank(vec_avg(boundary_transaction_total))`（机构建仓/清仓笔数）= S0.87 / 2Y 1.69**
  —— 2Y 是所有新族里最好的，机制方向（机构建仓→正向）正确，但整体强度不足。

### 3.3 MODEL/quant_factor_lib —— ★ 最重要的负面发现
- 该集 **alphaCount = 1**（平台只有 1 人用过），拥挤度最低，且含一个描述为
  **"Implied alpha or expected excess return"** 的字段 `qfl_cassie_qes_cassie_impliedalpha`。
- **实测：该字段直用是 S −0.30，`reverse` 后仍 −0.16。**
- ⇒ **教训（新）：字段描述里写 "implied alpha / expected return" 的，不要指望它直接可用。**
- 困境异象（Altman Z / Ohlson O / Merton DD）**在 EUR 全不成立**（三族 S 全在 ±0.15 内）。
- 财报电话会 NLP 族换手爆炸（0.51–0.66），不适合直接 rank。

## 四、★ 元结论

**"低拥挤" ≠ "有信号"。** `quant_factor_lib` 的 alphaCount=1（最低），却几乎毫无信号。

**EUR 高信号密度数据集极少**：本会话累计探过 **9 个数据集 / 约 230 条表达式**，
只有 **`risk70`（S2.09）与 `analyst_factor_signals`（S1.66 全闸过）** 出过 ≥1.58 的 IS。

## 五、待探清单（已排序）

| 数据集 | category | 字段 | alphaCount | vs |
|---|---|---|---|---|
| `news_sentiment_nlp` | OTHER | 23 | 6 | 6 |
| `workforce_flow_skills` | OTHER | 33 | 6 | 6 |
| `option_chart_model` | MODEL | 39 | 7 | 6 |
| `news_sentiment_dl` | OTHER | 66 | 12 | 6 |
| `multi_source_model` | MODEL | 60 | 27 | 6 |
| `model193` | MODEL | 173 | 85 | 6 |
| `order_book_imbalance` | OTHER | 256 | 154 | 5 |

## 六、本轮工程记录

- 全部波次已回填 `alphas` 表（wave314/315/316 共 45 条）。
- wave315 曾因 `WinError 10061 连接被拒`（平台网络故障）中断，**checkpoint 续跑机制正常工作**，恢复后补完。
- 工具已放 `tracking/EUR/scripts/`（`backfill_alphas_from_ckpt.py` / `fetch_prod.py`），避免 `tools/` 被外部清理删除。
