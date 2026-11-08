# HKG 模板库（2026-11-03）— 每个数据集 ≥10 个结构互异模板

> 纪律：模板差异必须落在**骨架结构 / 算子几何 / 矩（水平·一阶差分·二阶方差）/ 分组轴 / 非线性变换**上，不是换参数。
> 来源标注：`forum` = 平台论坛实证帖；`paper` = 金融文献机制（本轮 web_search 因额度不可用，文献为既有知识，未在线核验）；`self` = 结构自建。
> 区域设置固定：HKG / TOP800 / D1 / SECTOR / decay4 / trunc 0.08 / VERIFY / nanHandling ON / pasteurization ON / maxTrade OFF。
> 闸线（平台实测，取自 `2rApJ67b` 的 checks）：**LOW_SHARPE 1.58 / LOW_FITNESS 1.0 / LOW_2Y_SHARPE 1.58**；self<0.7、prod<0.7。

---

## A. intraday_pv_feats（PV，579 字段全 MATRIX，cov 0.928–0.98；塔 HKG/D1/PV ×1.5 未点亮）

机制：收盘前 30 分钟是全天流动性需求最集中时段（指数化/被动执行），主动买单推动 `high` 上沿；
反复被追高的名字 = 向流动性提供者持续付溢价 ⇒ 反转。
- `forum`: 《GLB 尾盘高点反转因子》43624289553815（S 2.34 / RA 全过）
- `paper`: Cushing & Madhavan (2000) 收盘前价格由被动执行驱动；Nagel (2012) 短期反转=流动性提供报酬；Bogousslavsky (2021) 日内各时段收益横截面独立定价

| # | 模板 | 结构轴 | 来源 |
|---|---|---|---|
| A1 | `reverse(group_zscore(ts_mean(mean_high_price_return_30m_pre_close_2,126),industry))` | 水平 + 长窗 + 分组 zscore | forum 主配方 |
| A2 | `reverse(group_zscore(ts_mean(subtract(high_ret,low_ret),126),industry))` | 高低价差（上沿 vs 下沿） | forum 对照 |
| A3 | `reverse(group_zscore(ts_mean(subtract(ask_ret,bid_ret),126),industry))` | 买卖报价差 = 尾部流动性成本 | self |
| A4 | `reverse(group_zscore(ts_mean(mean_vwap_return_30m_pre_close_2,126),industry))` | VWAP 口径（成交量加权价） | self |
| A5 | `reverse(group_zscore(ts_mean(high_ret,126),subindustry))` | 分组轴粒度（subindustry） | forum 粒度轴 |
| A6 | `reverse(group_zscore(ts_std_dev(high_ret,126),industry))` | **二阶矩**（追高的不稳定性） | self |
| A7 | `reverse(group_zscore(ts_mean(high_ret,22),industry))` | 短窗（信号时效） | self |
| A8 | `reverse(group_zscore(ts_mean(high_ret,252),industry))` | 长窗（结构持续性） | self |
| A9 | `reverse(group_zscore(ts_mean(subtract(last_trade_ret,vwap_ret),126),industry))` | 主动成交 vs VWAP 溢价 | self |
| A10 | `reverse(group_zscore(ts_corr(high_ret,volume_30m,126),industry))` | 价量耦合（追高是否有量支撑） | self |

## B. risk59（RISK，16 字段全 VECTOR，cov 0.8843；塔 HKG/D1/RISK ×1.3 未点亮）

机制：借券费率 = 做空的价格。费率高 ⇒ 做空需求旺 ⇒ 或定价过高（未来负收益），或空头拥挤（轧空正收益）。
- `forum`: 《融券借贷的隐形成本：risk59 融券数据随笔》43607257389207（费率高 + 补库天数长 = 做空白热化）
- `paper`: D'Avolio (2002) 借券市场费率由供需决定；Asquith-Pathak-Ritter (2005) 高做空兴趣预测负收益；Engelberg-Reed-Ringgenberg (2018) 借券费含做空风险溢价

| # | 模板 | 结构轴 | 来源 |
|---|---|---|---|
| B1 | `group_rank(ts_mean(subtract(offer_rate,bid_rate),66),sector)` | 借贷买卖价差（费率的横截面结构） | self |
| B2 | `-group_rank(ts_mean(last_rate,66),sector)` | 费率水平（负向 = 定价过高） | paper |
| B3 | `-group_rank(ts_delta(last_rate,22),sector)` | **一阶差分**（新空头流入） | paper |
| B4 | `-group_rank(ts_mean(s3utilization,66),sector)` | 利用率（借出/可借）拥挤度 | forum |
| B5 | `group_rank(ts_mean(daystocover10day,66),sector)` | 补库天数（正向 = 轧空） | forum |
| B6 | `group_rank(ts_mean(crowded_score,66),sector)` | 厂商拥挤度评分 | self |
| B7 | `group_rank(ts_mean(squeeze_risk,66),sector)` | 轧空风险评分 | self |
| B8 | `-group_rank(ts_mean(short_momentum,22),sector)` | 空头动量（日频做空/回补） | self |
| B9 | `-group_rank(ts_mean(multiply(last_rate,s3utilization),66),sector)` | **交互项**（贵 × 满） | forum |
| B10 | `-group_zscore(ts_zscore(last_rate,252),sector)` | 相对自身历史的极端度 | self |

## C. sentiment21（SENTIMENT，138 字段全 MATRIX，cov 0.966–1.0；塔 HKG/D1/SENTIMENT ×1.6 未点亮）

机制：情绪**水平**（pos−neg）之外，情绪**离散**（`*dts_*`= 情绪标准差）= 意见分歧；置信区间宽度 = 不确定性。
- `forum`: 《拷打AI：机构情绪分歧因子》37137602566679；《【Alpha灵感】情绪类因子》34435098185751
- `paper`: Diether-Malloy-Scherbina (2002) 分歧度高 ⇒ 未来收益低；Baker-Wurgler (2006) 情绪水平反向

| # | 模板 | 结构轴 | 来源 |
|---|---|---|---|
| C1 | `group_rank(ts_mean(subtract(pos_mean,neg_mean),22),sector)` | 极性差水平（短窗） | forum |
| C2 | `-group_rank(ts_mean(dts_sop,66),sector)` | **二阶矩**（正向情绪分歧） | paper |
| C3 | `-group_rank(ts_mean(subtract(pos_conf_up,pos_conf_low),66),sector)` | 置信区间宽度（不确定性） | self |
| C4 | `group_rank(ts_delta(subtract(pos_mean,neg_mean),22),sector)` | **一阶差分**（情绪改善） | self |
| C5 | `group_rank(ts_mean(subtract(pos_max,neg_max),66),sector)` | 极值不对称 | self |
| C6 | `-group_rank(ts_mean(neut_mean,66),sector)` | 中性占比（信息含量倒数） | self |
| C7 | `-group_rank(ts_std_dev(neg_mean,126),sector)` | 负向情绪波动 | self |
| C8 | `group_rank(ts_mean(subtract(4pos_mean,4neg_mean),22),sector)` | 单通道（TRNA）极性差 | self |
| C9 | `group_rank(ts_mean(subtract(subtract(2pos,2neg),subtract(4pos,4neg)),66),sector)` | **多源通道分歧**（模块2−模块4） | self |
| C10 | `group_zscore(ts_zscore(subtract(pos_mean,neg_mean),252),sector)` | 长窗 zscore 极端度 | self |

## D. institutions6（INSTITUTIONS，11 字段全 MATRIX，cov 0.994–0.999；塔 ×1.4 未点亮）

机制：机构持股变动 = 聪明钱流向；持有人数与买方数的变化 = 广度。
- `paper`: Nofsinger & Sias (1999) 机构持股变动预测收益；Gompers & Metrick (2001) 机构持股与股票特征

| # | 模板 | 结构轴 |
|---|---|---|
| D1 | `group_rank(ts_delta(count_institutional_holders_security,66),sector)` | 持有人数一阶差分（广度） |
| D2 | `group_rank(ts_delta(count_institutional_buyers_security,22),sector)` | 买方机构数变化 |
| D3 | `group_rank(ts_mean(divide(aggregate_equity_value_institutions,aggregate_equity_value_all_owners),66),sector)` | 机构持股市值占比 |
| D4 | `-group_rank(ts_std_dev(count_institutional_holders_security,126),sector)` | 持有人数波动（不稳定） |
| D5 | `group_rank(ts_zscore(count_institutional_holders_security,252),sector)` | 相对自身历史极端度 |

## E. other532（OTHER，2 字段全 VECTOR，cov 1.0；塔 ×1.7 未点亮）

机制：**特异收益**（剔除风格后的残差收益）= 纯个股信息，反转/延续在其上更干净。

| # | 模板 | 结构轴 |
|---|---|---|
| E1 | `-group_rank(ts_mean(vec_avg(oth532_spret),22),sector)` | 残差收益短期反转 |
| E2 | `group_rank(ts_mean(vec_avg(oth532_spret),126),sector)` | 残差收益中期延续 |
| E3 | `-group_rank(ts_std_dev(vec_avg(oth532_spret),126),sector)` | 残差波动（特质风险） |

## F. other543（OTHER，4 字段 VECTOR，cov 0.784–0.892；港交所 CCASS 披露）

机制：**中央结算系统参与者持股** = 港股独有的持仓穿透披露（含港股通南下资金）。持股集中度与变动是港股本地的强信号。
- 注意：cov 0.78–0.89，需 ts_backfill 或 if_else 兜底才能满足「近十年都有数据」。

| # | 模板 | 结构轴 |
|---|---|---|
| F1 | `group_rank(ts_delta(vec_avg(oth543_disclosures_hk_shareholding),66),sector)` | 港资持股变动 |
| F2 | `group_rank(ts_mean(divide(vec_avg(oth543_disclosures_hk_shareholding),add(vec_avg(oth543_hk_total_issued_share),1)),66),sector)` | 持股占比水平 |
| F3 | `group_rank(ts_mean(divide(vec_avg(oth543_disclosures_ashares_shareholding),add(vec_avg(oth543_ashares_total_issued_share),1)),66),sector)` | A 股通道占比（南北向对照） |

## G. macro63（MACRO，1 字段 MATRIX，cov 1.0；塔 ×1.2 未点亮）

`mcr63_membership` = 指数成分归属。机制：指数调整（纳入/剔除）带来的被动资金流。
| # | 模板 | 结构轴 |
|---|---|---|
| G1 | `group_rank(ts_delta(mcr63_membership,22),sector)` | 成分变更事件（纳入=正流） |
| G2 | `ts_sum(mcr63_membership,252)` | 成分稳定性（长期在指数内） |

---

## H. intraday_pv_feats（PV，579 字段；**HKG 唯一能稳定过 LOW_SHARPE 1.58 的族**）

> 全部结果来自 HKG / TOP800 / D1 / SECTOR / decay 4 / truncation 0.08 / 2014-01-01~2023-12-31 实测。
> 统一外层骨架：`group_zscore(divide(ts_mean(D,126), ts_std_dev(D,126)), industry)`（6 算子）。
> 字段命名规律：`mean_<价格类型>_price_return_<30m|60m>_<post_open|pre_close_2>`；**vwap 例外，不带 price**（`mean_vwap_return_...`）；`high` 的 60m–pre_close 段是 `mean_high_price_return_60m_pre_close`（无 `_2`）。

### H1. 价格类型 − vwap（pre_close 段）：度量「收盘前 30/60 分钟的价格偏移」

| # | D | 号 | S | 2Y | 说明 |
|---|---|---|---:|---:|---|
| H1a | `low − vwap` 30m | + | **1.77** | 1.70 | 下影偏移（0 fail） |
| H1b | `high − vwap` 60m | + | **1.69** | 2.29 | 上影偏移（0 fail） |
| H1c | `last_trade − vwap` 60m | − | 1.75 | 1.42 | 收盘价溢价→反转 |
| H1d | `bid − vwap` 30m | + | 1.41 | 1.46 | 买价偏移（弱一半） |
| H1e | `ask − vwap` 30m | + | 1.26 | 1.35 | 卖价偏移（最弱） |
| H1f | `high − vwap` 30m | + | 1.80 | 1.74 | = `RRE7vM2e` |
| H1g | `last_trade − vwap` 30m | − | 1.97 | 2.10 | = `2rAlGNk6`（本族最强） |

**符号规律（重要）**：`low`、`high`、`bid`、`ask` 对 vwap 的偏移**同号为正**（偏移越大越好）；唯独 `last_trade − vwap` **必须取负**（收盘价高于 vwap → 次日反转）。

### H2. 时段价差（post_open − pre_close_2）：度量「尾盘相对开盘的定价抬升」

| # | 价格类型 / 窗 | S | 2Y | 换手 | 说明 |
|---|---|---:|---:|---:|---|
| H2a | `vwap` 60m | **2.42** | 2.30 | 5.28% | `QPv3lZ6K`，全族最高 |
| H2b | `last_trade` 30m | **2.40** | 1.97 | 5.25% | `xArYzO5w` |
| H2c | `last_trade` 60m | **2.34** | 2.30 | 5.15% | `MPY18MVr` |
| H2d | `bid` 60m | 1.76 | 1.40 | 4.51% | 弱一档 |
| H2e | `high` 60m | 1.17 | 0.80 | 4.52% | |
| H2f | `ask` 30m / 60m | 1.17 / 1.13 | 0.53 / 0.67 | 4.2% | |
| H2g | `low` 60m / 30m | 0.90 / 0.25 | 0.34 / 0.84 | 4.5% | 弱 |
| H2h | `high` 30m | 0.20 | 0.79 | 4.46% | 最弱 |

**结构规律**：时段价差的强载体是 **vwap 与 last_trade**（2.34–2.42），high/low 反而弱；与 H1 正好互补——**pre_close 段看 high/low，post_open 段看 vwap/last_trade**。

### H3. 已判死（勿重投）

- **量价/流动性/相关性族全灭**：`corr_*_with_volume`、`avg_*_size_to_volume_ratio`、`kurtosis_trade_volume_interval`、`corr_{ask,bid}_price_with_slippage`、`mean_slippage_30m_*` 共 10 个结构，最好 S 0.49，多数为负。
  ⇒ **同一数据集内部机制分层：信号只住在价格路径，不住在成交量/订单簿/滑点。**
- `ts_rank(·,252)` 几何：S 2.27 但换手 77%、F 0.92，需 `hump` 才能用（`hump` 第二参数必须写 `hump=`）。
- `num_intervals_*`（换手 73%）、`vwap/last` 偏离（换手 58%）均失效。

### H4. 族内共线（决定提交篮子）

13 颗全闸通过的**最大互不相关篮子只有 4 颗**：`MPY18MVr` / `qMLjw8nA` / `2rAlGNk6` / `RRE7vM2e`。
高共线对：`qMLjw8nA~YP1796Nq` 0.923、`RRE75dKj~pwdPzXJ6` 0.9225、`xArYzO5w~MPY18MVr` 0.9208、`QPv3lZ6K~MPY18MVr` 0.8789。
⇒ 新的 2.4 档三颗只能取 1 颗；PV 塔 3 颗的正解 = `2rAlGNk6` + `RRE7vM2e` + (`MPY18MVr` 或 `qMLjw8nA`)。

