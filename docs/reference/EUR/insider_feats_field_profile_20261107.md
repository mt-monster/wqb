# EUR / insider_feats 字段画像（118 MATRIX 字段全量梳理）· TOPCS1600 / D1

- 采集时间：2026-11-07｜口径：`get_datafields(dataset_id=insider_feats, region=EUR, universe=TOPCS1600, delay=1, filter_sharpe=false, max_fields=200)` → **118 字段全量返回**（`platform_count=118`，无截断）
- 平台类别：**other**（不是 insiders 类）。EUR 的 insiders 类别只有 3 个集且已全部穷尽，本集与 `insider_matrix`/`insider_trx_matrix` 是 EUR 仅有的 insider 交易数据里**唯一曾出现 S>1.0 读数**的（历史 `top5_buy_tx_count_250d` 双窗 add → S 1.11）
- 全部 118 字段均为 **MATRIX** ⇒ 无 VECTOR/event-input 语义障碍；不需要 `vec_*` 降维

## 1. 两种覆盖率制度（决定一切）

| 制度 | 字段族 | 覆盖率 | 含义与后果 |
|---|---|---|---|
| **A. 平台预聚合比率（`_filled`）** | `buy_sell_ratio_*`、`buy_sell_tx_count_ratio_*`、`*_buy_to_sell_*_ratio_*_filled` | **0.9157 恒定** | 平台已把无交易股票填成中性值 ⇒ **没有 0/0 风险**，可直接当横截面水平用；`nanHandling ON/OFF` 几乎无差别 |
| **B. 原始事件计数（无 filled）** | `top5_buy_tx_count_*`、`total_buy_tx_count_*`、`top20_sale_tx_count_*`、`total_sale_tx_count_*`、`total_insider_*_count_*`、`*_volume_*` | **0.15 – 0.72，且随窗口单调上升**（5d≈0.15-0.34 → 60d≈0.27-0.48 → 250d≈0.46-0.72） | 属**自然零事件**：无交易=0 是真实值而非缺失 ⇒ `nanHandling ON` 填空=0 在语义上正确；窗口越长覆盖越广（250d 才把 72% 股票纳入） |

> ⚠ 关键推论：**B 族必须配 `nanHandling ON`**（把「无内部人交易」正确编码为 0），而 **A 族用 ON/OFF 均可**。这与 analyst45（稀疏 VECTOR，必须 OFF）的结论相反——因为 A/B 两族都有「真实的零/中性值」。

## 2. 字段族谱（族 × 角色 × 窗口）

| 族 | 规模 | 角色档 | 窗口 | 代表字段（a=alphaCount, u=userCount） |
|---|---|---|---|---|
| `buy_sell_ratio_{all,top20,top5}_Wd_filled` | 12 | all(全体) / top20 / top5 | 5/10/20/60/250 | `buy_sell_ratio_all_60d_filled`(a6,u2)｜`buy_sell_ratio_top20_60d_filled`(**a20,u9 最拥挤**) |
| `buy_sell_tx_count_ratio_{all,top20,top5}_Wd[_filled]` | 23 | all / top20 / top5 | 5/10/20/60/250 | `buy_sell_tx_count_ratio_all_60d_filled`(**a0,u0**)｜`..._top5_250d_filled`(a0,u0) |
| `buy_to_sell_ratio_*` / `*_buy_to_sell_txn_ratio_*` / `*_volume_ratio_*` | 18 | all/top20/top5 | 5/10/20/60/250 | 多为 a0,u0；多为无 filled 版（cov 0.34–0.75） |
| `total_buy_tx_count_Wd` | 7 | 全体 | 5/10/20/60/250 | `total_buy_tx_count_250d`(**a0,u0**, cov 0.72) |
| `total_sale_tx_count_Wd` | 5 | 全体 | 5/10/60/250 | `total_sale_tx_count_250d`(a0,u0, cov 0.69) |
| `top5_buy_tx_count_Wd[_2]` | 9 | top5 | 5/10/20/60/250 | `top5_buy_tx_count_250d`(a1,u1, cov 0.46) ← **历史 EUR 最强读数载体** |
| `top20_buy_tx_count_Wd[_2]` | 10 | top20 | 5/10/20/60/250 | `top20_buy_tx_count_250d`(a1,u1, cov 0.52) |
| `top20/top5_sale_tx_count_Wd[_2]` | 15 | top20/top5 卖出 | 5/10/20/60/250 | `top20_sale_tx_count_250d`(a0,u0, cov 0.60) |
| `total_insider_{purchase,buy,sale}_count_*` / `*_volume_lookback_N` | 8 | 全体 | 5/10/20/60/250 | `total_insider_purchase_count_lookback_10`(a1,u1, cov 0.34) |

**拥挤度结论**：118 字段里 **约 95% 的 `alphaCount=0 / userCount=0`**，唯一较拥挤的是 `buy_sell_ratio_top20_60d_filled`（a20/u9）与 `buy_sell_ratio_all_60d_filled`（a6/u2）。⇒ 本集整体 prod 相关性的先验很低，选字段应优先 a0/u0。

## 3. F 闸的闭式约束（本战役最关键的一条数学）

平台 fitness 闭式：`F = S × sqrt( returns / max(turnover, 0.125) )`。
⇒ 本集 TO 只有 1.9–3.9%（远低于 0.125），公式退化为 `F = S × sqrt(returns / 0.125)`。

| 目标 S | 过 F=1.0 所需最小 returns | 说明 |
|---|---|---|
| 1.58（REGULAR 提交线） | **5.01%** | 当前实测 returns 2.3–2.6%，**缺口约 2 倍** |
| 1.70 | 4.33% | |
| 1.80 | 3.86% | 历史判死依据（returns 3.9% ⇒ 需 S≥1.84） |
| 2.00 | 3.13% | |

⇒ **本集的胜负手不是 S，是 returns**。而 `returns ≈ 换手 × 单笔超额`，当前换手只有 3.3% ⇒ 提换手（短窗 / 降 decay）是把 returns 拉进 5% 区间的唯一杠杆。
⇒ 这也解释了历史判死记录 `EUR-INSIDER-FEATS-WEAK` 的真实成因：不是信号无效（S 已到 1.11），而是 **returns 天花板 3.9% 让 F 结构性不可达**。

## 4. 实测记录（2026-11-07，本战役）

| alpha | 表达式 | S | F | TO | returns | 2Y | margin | 多/空 | 失败闸 |
|---|---|---|---|---|---|---|---|---|---|
| `bl6x8LdM` | `group_rank(multiply(rank(buy_sell_tx_count_ratio_all_60d_filled), rank(buy_sell_ratio_top20_250d_filled)), industry)` | **0.80** | 0.37 | 3.26% | 2.61% | 1.25 | 16.0bp | 621/763 | S / F / 2Y |
| `RRE5ARAj` | `group_rank(buy_sell_tx_count_ratio_all_60d_filled, industry)` | 0.74 | 0.33 | 3.84% | 2.45% | 1.20 | 12.8bp | 637/734 | S / F / 2Y |
| `mLoKYL6W` | `group_rank(buy_sell_ratio_all_60d_filled, industry)` | 0.71 | 0.30 | 3.86% | 2.28% | **1.27** | 11.8bp | 637/735 | S / F / 2Y |
| `Jje3Ppvj` | `group_rank(buy_sell_tx_count_ratio_top5_250d_filled, industry)` | 0.66 | 0.27 | 1.93% | 2.11% | 0.81 | 21.9bp | 613/760 | S / F / 2Y |

- **三条共有的好现象**：① 持仓广度 613–763（insider_agg_matrix 只有 210–350）；② **完全没有 rob / sub 闸失败**（insider_agg_matrix 每条都崩在这两闸）；③ 2Y 1.20–1.27，是全战役最接近 1.58 的读数。
- **60d 优于 top5/250d**：`top5_250d` 比值虽然 margin 更高（21.9bp）但 TO 只有 1.93%，returns 反被压低 ⇒ 与 §3 的结论一致。
- **两腿乘积结构有效**：`bl6x8LdM` 相对单腿 `RRE5ARAj` S +0.06、margin 12.8→16.0bp、TO 降 0.58pp ⇒ 与项目记载的「双窗秩乘积一石四鸟」同向。

## 5. 文献映射

| # | 机制 | 来源 | 对应字段族 |
|---|---|---|---|
| 1 | **只统计买入方向的人数/笔数**（不做买卖比）预测收益最强 | Jeng, Metrick & Zeckhauser (2003), REStat；项目实证「buy-only 计数 > buy/sell ratio」 | `total_buy_tx_count_*` / `top5_buy_tx_count_*` |
| 2 | 净买入人数比净买入金额更稳健；金额受少数大额交易支配 | Lakonishok & Lee (2001), RFS | `buy_sell_tx_count_ratio_*`（笔数比） |
| 3 | 交易规模越大越有信息量 | Seyhun (1986) | `*_volume_*` 族（本集尚未测） |
| 4 | 常规 vs 机会型内部人；只有机会型预测收益 | Cohen, Malloy & Pomorski (2012) | 需`ts_delta`/`ts_av_diff` 二阶结构（未测） |
| 5 | 内部人买入的**持续性**（连续同向交易次数） | 项目 EUR insiders 类别卡原语 | `*_count_*` 长窗（250d） |
| 6 | 「÷自身波动」在事件型计数上无效 | 项目实证（`ts_ir`/`÷ts_std_dev` 在本集 S→0、2Y 转负） | ⇒ **禁用** `ts_ir` / `divide(x, ts_std_dev(x,d))` |

## 6. 已知与未知

- **已知**：118 字段全量命名与类型；两套覆盖制度；拥挤度分布（95% 为 a0/u0）；F 闸闭式与所需 returns；4 条实测读数与结构排序（两腿乘积 > 单腿笔数比 > 单腿金额比 > top5/250d）。
- **未知**：① B 族计数在 `nanHandling ON` 下的真实持仓广度与 S（第 11 波在测）；② 短窗（5d/10d）能把 TO 抬到多少、returns 是否同步跟上；③ `*_volume_*` 族（Seyhun 规模轴）是否有信号；④ `_2` 后缀字段（如 `top20_buy_tx_count_250d_2`）与无后缀版的差异语义；⑤ 本集在 EUR/D1/OTHER 塔的 multiplier（`get_alpha_details` 未回传，需补读）。
