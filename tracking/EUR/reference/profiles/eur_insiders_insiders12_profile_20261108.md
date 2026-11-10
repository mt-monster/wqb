# EUR × insiders12 字段画像（2026-11-08）

> 平台目录：8/8 字段全量（complete=true，全部 VECTOR）；UK 内部人交易数据

## 判定：覆盖判死，不投槽

| 字段 | cov | 语义 |
|---|---|---|
| insd12_percent | **0.1925** | 交易后内部人持股比例 |
| insd12_positionchangetransactionamount | **0.1925** | 交易股数（买+/卖−） |
| insd12_sharesheld | **0.1925** | 交易后持股数 |
| insd12_mktprice | 0.1925 | 交易市价 |
| insd12_transactioncode | 0.2592 | 交易类型码 |
| option_exercise_price_eur/gbp/reported | 0.1925 | 期权行权价 |

**判死依据（覆盖口径，2026-10-30/31 修正版）**：cov 0.19–0.26 ≪ 0.85 ⇒ sub 闸结构性不可达（fundamental28 同型，cov 0.50 已判）。零星缺年可接受、连续多年空窗不可接受——本数据集 4/5 字段 cov 不足 0.2，属数据源级缺失。
**结论**：EUR INSIDERS 塔(2/3)不可经 insiders12 点亮；如需点亮走 starmine+insiders 复刻 RRAvGrn0 形态（avg_top_buy_shares 字段，待溯源所属数据集）。
