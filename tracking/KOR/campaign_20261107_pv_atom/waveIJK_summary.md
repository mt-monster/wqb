# Wave I / I2 / J / K 汇总（2026-11-07）— insiders5 余字段 + institutions 持仓轴

## Wave I / I2：insiders5 其余快照字段（10/10 COMPLETE）

| 字段 / 几何 | alpha | S | F | 2Y | raFail |
|---|---|---:|---:|---:|---:|
| vec_avg(grp_td_drt) W22（交易方向水平） | 3qokvWxQ | 0.00 | 0.00 | 0.14 | 5 |
| vec_stddev(grp_td_drt) W22 | 0mYN2Wdk | 0.14 | 0.03 | -0.46 | 4 |
| vec_avg(recent_dt) W22（新鲜度水平） | 0mYN2Mjq | -0.37 | -0.14 | -1.49 | 5 |
| vec_stddev(recent_dt) W22 | npve58Az | 0.65 | 0.33 | 1.24 | 3 |
| vec_stddev(rpst_grp_typ) W22（关联方类型离散度） | RRElx00a | -0.03 | 0.00 | 0.95 | 5 |
| vec_avg(source_real_data) W22 | LLMmoOO9 | -1.09 | -0.73 | -1.13 | 5 |
| vec_stddev(source_data) W22 | 9qxd5WxV | 0.07 | 0.01 | 0.28 | 5 |
| vec_avg(qes) W22 | MPYev3Yr | -0.33 | -0.09 | -0.58 | 5 |
| vec_stddev(grp_source_td_drt) W22 | YP1EVzJR | 0.39 | 0.16 | 0.21 | 3 |
| vec_avg(unt_val) W22 | Xg9v3zMm | 0.82 | 0.51 | 0.88 | 3 |

**判死**：insiders5 全 53 字段扫完，唯一有信号的是 tnc（已被 prod 0.9686 钉死）。
最强的非 tnc 字段 unt_val 只有 S 0.82。

## Wave J：fund_holdings_panel 裸水平/变化/比值（10/10 COMPLETE）

| 模板 | alpha | S | 2Y | raFail |
|---|---|---:|---:|---:|
| holder_account_total 水平（持有人数） | Vkxmb92Y | 0.47 | 1.27 | 3 |
| ts_delta(holder_account_total,66) | kqNW6718 | -0.13 | -0.82 | 4 |
| herfindahl_index_holdings 水平（集中度） | 3qokvVpP | -0.61 | -1.50 | 5 |
| top_weighted / holder 比值（信念占比） | MPYeN37M | 0.51 | 0.51 | 3 |
| mean_security_weight 水平 | vR1p7mgA | 0.54 | 1.11 | 3 |
| vec_sum(boundary_transaction_total) W22 | QPvNRQXp | -0.52 | -0.76 | 4 |
| vec_avg(stable_boundary_trade_count_21d) W22 | 78Lv5Ag2 | -0.35 | -0.44 | 4 |
| vec_avg(large_trade_count_50bps) W22 | LLMmvjbL | 0.17 | 0.63 | 4 |
| vec_stddev(security_transaction_usd_value) W22 | d5W3Mn8Y | -0.09 | -0.06 | 3 |
| ts_delta(security_holding_usd_value,66) | LLMmvnqL | -0.69 | -1.69 | 5 |

**判死**：机构持仓数据集的裸水平几何在 KOR 无信号（|S| 上限 0.61）。

## Wave K / K2：fund_holdings_panel 交互几何

K 首批整批 ERROR，根因（平台原话）：
> Operator divide does not support event inputs. If fields is vector type should use vec_* operator with event input

**教训（写死）**：`preflight_expressions` 只校验字段**存在性**，不校验**向量/事件语义**；
VECTOR 字段参与任何标量算子（divide/multiply/add/ts_*）前必须先 `vec_*` 聚合，否则整批 ERROR。
K2 为全部 VECTOR 字段补 `vec_sum`/`vec_avg` 聚合后的修正版。

## 本轮对 KOR 的总体判断

1. insiders5 塔：**关闭**。tnc 水平族被 prod 0.9686 钉死；离散度族 S 天花板 1.30；其余 51 字段 |S| <= 0.82。
2. institutions 塔：裸水平轴**关闭**；交互几何（K2）待收。
3. 规律：**裸水平类信号已被 prod 池占满**，三颗在库件全部是二阶/交互/意外几何。