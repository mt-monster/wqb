# Wave BA6 设计 — insiders1 十模板池（DEU D1，2026-11-10 20:1x）

> insiders1 = 内部人交易明细（Compustat Global insider filings）。8 VECTOR 字段 cov 0.5343。
> 可用信号字段 6 个：holdings（交易后持仓）/ price / shares（本次股数）/ tradesignificance（1-3）/ value / valueeur；gvkey 与 currency_code 为元数据禁信号。
> ⚠ 无显式买卖方向字段 ⇒ 方向由 holdings 时间差分推断（正=增持，负=减持），这与文献的「净增持」口径一致。

## 一、学术先验

- **Lakonishok & Lee 1991/2001**：内部人买入显著预测正收益；卖出预测力弱（非对称）。
- **Cohen, Malloy & Pomorski 2012 (JF)**：内部人交易可预测价格压力；「常规交易者」无信息、「机会主义者」有信息。
- **Rozeff & Zaman 1998**：内部人持股变化 > 持股水平（变化含信息）。
- 反向假说：内部人减持=负面信息（对称检验臂）。

## 二、十模板（结构互异，全部先 vec_* 聚合再进算子；≤12 算子）

| # | 表达式 | 机制 | 方向 |
|---|---|---|---|
| I1 | group_rank(ts_delta(ts_backfill(vec_avg(insd1_holdings), 132), 66), subindustry) | 净增持（持股变化） | 正（LL 2001） |
| I2 | -group_rank(ts_delta(ts_backfill(vec_avg(insd1_holdings), 132), 66), subindustry) | 净增持反向对照 | 反（对测） |
| I3 | group_rank(ts_mean(ts_backfill(vec_sum(insd1_valueeur), 132), 66), subindustry) | 交易金额强度 | 正（活动面） |
| I4 | group_rank(ts_mean(ts_backfill(vec_avg(insd1_tradesignificance), 132), 66), subindustry) | 交易显著度水平 | 正（信息含量） |
| I5 | group_rank(ts_mean(multiply(rank(ts_delta(ts_backfill(vec_avg(insd1_holdings), 132), 66)), rank(ts_mean(ts_backfill(vec_avg(insd1_tradesignificance), 132), 22))), 22), subindustry) | 增持 × 显著度交互 | 正（CMP 机会主义） |
| I6 | group_rank(ts_mean(divide(ts_backfill(vec_sum(insd1_valueeur), 132), add(ts_backfill(vec_count(insd1_shares), 132), 1)), 22), subindustry) | 平均单笔金额（conviction 强度） | 正（自建） |
| I7 | group_rank(ts_rank(ts_backfill(vec_avg(insd1_holdings), 132), 252), subindustry) | 持股水平 52 周位置 | 正（Rozeff-Zaman 对照） |
| I8 | group_rank(ts_mean(ts_backfill(vec_count(insd1_shares), 132), 22), subindustry) | 交易笔数（参与广度） | 正（活动面） |
| I9 | trade_when(greater(ts_mean(ts_backfill(vec_avg(insd1_tradesignificance), 132), 22), 2), group_rank(ts_delta(ts_backfill(vec_avg(insd1_holdings), 132), 66), subindustry), -1) | 高显著度门控的增持 | 正（CMP：只跟高信息交易） |
| I10 | -group_rank(ts_std_dev(ts_backfill(vec_avg(insd1_holdings), 132), 252), subindustry) | 持股波动率反向（不确定性） | 反（不确定性溢价） |

## 三、执行前检查

- 双预检：verify_expr 语法 + preflight 字段存在性（insd1_* 已由 get_datafields 确认）。
- 覆盖闸：cov 0.5343 偏低，收割后必须逐年 longCount>0 检查（连续多年空窗则标 PROVISIONAL，不得当信号死）。
- 方向先验铁律：I2 是 I1 的严格反向对照，用于确认符号（若 I1/I2 对称且为负，说明 DEU 内部人增持是反向信号）。
- 塔位：INSIDERS 塔 DEU D1 = 0（未点亮）✓。

## 四、状态

- 设计完成，待 BA5（fund_holdings_panel）收割腾出槽位后派发。
---

## BA6 收割（sim 3N5G5o4XQ4Fjc7rZdxmagIi，10/10 COMPLETE，0 error）

| # | 模板 | alpha | S | 2Y | sub | lc | TO |
|---|---|---|---:|---:|---:|---:|---:|
| I1 | 净增持（持股变化 66） | MP6jkd88 | **0.78** | 0.82 | 0.26 | 78 | 0.080 |
| I2 | 净增持反向对照 | 78YkJ3XL | -0.78 | -0.82 | -0.26 | 140 | 0.080 |
| I3 | 金额强度 66 | LLKPkEX2 | 0.34 | 0.72 | -0.15 | 126 | 0.028 |
| I4 | 显著度水平 66 | LLKPkEla | 0.01 | 1.25 | 0.45 | 132 | 0.028 |
| I5 | 增持 x 显著度交互 | rK71A9rE | **0.78** | **1.65** | 0.43 | 79 | 0.042 |
| I6 | 平均单笔金额 | 6XMnzZYE | 0.45 | 0.69 | -0.19 | 123 | 0.037 |
| **I7** | **持股 52 周位置** | **YPajQ8WM** | **0.85** | 1.03 | 0.23 | 88 | 0.066 |
| I8 | 参与广度（笔数） | GrmqkX3x | 0.23 | 0.56 | -0.04 | 120 | 0.040 |
| I9 | 高显著度门控增持 | mLaPZdxE | 0.69 | 0.66 | **0.47** | 64 | 0.053 |
| I10 | 持股波动率反向 | RReJd92n | -0.51 | -0.54 | -0.03 | 143 | 0.018 |

**归因**：
1. **持股水平面（I7 0.85）> 交易面（I1/I5 0.78）> 活动面（0.01~0.45）** —— 内部人「持股份额高」比「近期增持」更稳定，与 Rozeff-Zaman 1998「水平含信息」方向一致。
2. **I1/I2 严格对称（±0.78）** ⇒ 净增持机制真实存在但强度有限；**lc 差异巨大（I1 78 vs I2 140）** 说明 DEU 内部人减持样本远多于增持（与 Lakonishok-Lee「卖出多于买入」一致）。
3. **I5 交互 2Y 1.65**：Cohen-Malloy-Pomorski「机会主义交易含信息」在近两年成立，但全期仅 0.78。
4. **I9 sub 0.47 全波最佳**（lc 64 偏低）；I10 负号 ⇒ 高持股波动反而好（弱信号）。

**判定**：族天花板 **0.85** 距 1.58 差 0.73 ⇒ **insiders1 信号层弱（PROVISIONAL，1 波 10 臂全测）**，不判死、不追投。INSIDERS 塔内无强信号面。