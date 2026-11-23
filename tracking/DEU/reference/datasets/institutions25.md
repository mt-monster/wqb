# institutions25 字段画像（DEU / TOP500 / D1）

> 建档 2026-11-23。数据源 `mcp__wq-brain-http__get_datafields(region=DEU, universe=TOP500, delay=1, dataset_id="institutions25", filter_sharpe=false)`；
> 平台实返 `count=24 / platform_count=24 / complete=true / pages_fetched=1`。归档：`tracking/DEU/reference/datasets/institutions25.md`。

## 0. 数据集级

| 项 | 值 |
|---|---|
| name | Fund Short Selling Data（对冲基金/资管空头持仓，600+ managers / 2600 securities / 30 countries since 2012） |
| category | institutions（DEU/D1 `INSTITUTIONS`，×1.6） |
| coverage（集级） | **0.0**（平台声明；2026-11-03 探针实测有读数 ⇒ 覆盖率元数据不可判「无数据」，记可逆假设） |
| fieldCount | 24（全 VECTOR ⇒ 必须 `vec_avg`/`vec_max` 降维） |
| userCount / alphaCount | 7 / 11 |
| valueScore | 6.0 |

## 1. 字段全表（24/24，逐字段平台实读）

| # | field id | type | coverage | alphaCount | 语义 |
|---|---|---|---:|---:|---|
| 1 | `inst25_activity` | VECTOR | 0.0 | 0 | 交易活跃度 0–100（相对其他证券的成交笔数） |
| 2 | `inst25_age` | VECTOR | 0.0 | 2 | 空头持仓年龄排名 0–100（平均做空时长） |
| 3 | `inst25_concentration` | VECTOR | 0.0 | 0 | 前三大空头占流通股比例 |
| 4 | `inst25_crowding` | VECTOR | 0.0 | 0 | 拥挤度 0–100（多少 manager 同向做空） |
| 5 | `inst25_entry_position` | VECTOR | 0.0 | 2 | 建仓时空头占流通股比例 |
| 6 | `inst25_is_open` | VECTOR | 0.0 | 0 | 仓位是否仍开放（1/0） |
| 7 | `inst25_manager_avg_trade_length` | VECTOR | 0.0 | 0 | manager 已平空仓平均持续周数 |
| 8 | `inst25_manager_count` | VECTOR | 0.0 | 0 | 开放空头 manager 数 |
| 9 | `inst25_manager_position_count` | VECTOR | 0.0 | 0 | manager 组合内空头数（专注度） |
| 10 | `inst25_position` | VECTOR | 0.0 | 1 | manager 当前空头占总股本 % |
| 11 | `inst25_position_change` | VECTOR | 0.0 | 0 | 相对上次 Position Date 的空头变化 |
| 12 | `inst25_security_avg_trade_length` | VECTOR | 0.0 | 1 | 证券所有开放空头平均持续天数 |
| 13 | `inst25_security_cover_count` | VECTOR | 0.0 | 0 | 当日回补笔数 |
| 14 | `inst25_security_short_count` | VECTOR | 0.0 | 3 | 当日开空笔数 |
| 15 | `inst25_security_trade_count` | VECTOR | 0.0 | 1 | 当日总成交笔数 |
| 16 | `inst25_security_trade_count_1mo` | VECTOR | 0.0 | 1 | 过去 1 月成交笔数 |
| 17 | `inst25_security_trade_count_1wk` | VECTOR | 0.0 | 0 | 过去 1 周成交笔数 |
| 18 | `inst25_security_trade_count_1yr` | VECTOR | 0.0 | 0 | 过去 1 年成交笔数 |
| 19 | `inst25_security_trade_count_2yr` | VECTOR | 0.0 | 1 | 过去 2 年成交笔数 |
| 20 | `inst25_security_trade_count_3mo` | VECTOR | 0.0 | 0 | 过去 3 月成交笔数 |
| 21 | `inst25_security_trade_count_3yr` | VECTOR | 0.0 | 0 | 过去 3 年成交笔数 |
| 22 | `inst25_sentiment` | VECTOR | 0.0 | 0 | 被做空程度 0–100（总空头存量） |
| 23 | `inst25_total_short_interest` | VECTOR | 0.0 | 0 | 总空头占流通股 %（全 manager 汇总） |
| 24 | `inst25_trade_length` | VECTOR | 0.0 | 1 | 自建仓日起的交易日数 |

### 实测读数表（平台 `get_datafields` 逐字段实读）

| field | type | coverage | alphaCount |
|---|---|---|---:|
| `inst25_activity` | VECTOR | 0.0 | 0 |
| `inst25_age` | VECTOR | 0.0 | 2 |
| `inst25_concentration` | VECTOR | 0.0 | 0 |
| `inst25_crowding` | VECTOR | 0.0 | 0 |
| `inst25_entry_position` | VECTOR | 0.0 | 2 |
| `inst25_is_open` | VECTOR | 0.0 | 0 |
| `inst25_manager_avg_trade_length` | VECTOR | 0.0 | 0 |
| `inst25_manager_count` | VECTOR | 0.0 | 0 |
| `inst25_manager_position_count` | VECTOR | 0.0 | 0 |
| `inst25_position` | VECTOR | 0.0 | 1 |
| `inst25_position_change` | VECTOR | 0.0 | 0 |
| `inst25_security_avg_trade_length` | VECTOR | 0.0 | 1 |
| `inst25_security_cover_count` | VECTOR | 0.0 | 0 |
| `inst25_security_short_count` | VECTOR | 0.0 | 3 |
| `inst25_security_trade_count` | VECTOR | 0.0 | 1 |
| `inst25_security_trade_count_1mo` | VECTOR | 0.0 | 1 |
| `inst25_security_trade_count_1wk` | VECTOR | 0.0 | 0 |
| `inst25_security_trade_count_1yr` | VECTOR | 0.0 | 0 |
| `inst25_security_trade_count_2yr` | VECTOR | 0.0 | 1 |
| `inst25_security_trade_count_3mo` | VECTOR | 0.0 | 0 |
| `inst25_security_trade_count_3yr` | VECTOR | 0.0 | 0 |
| `inst25_sentiment` | VECTOR | 0.0 | 0 |
| `inst25_total_short_interest` | VECTOR | 0.0 | 0 |
| `inst25_trade_length` | VECTOR | 0.0 | 1 |

## 2. 机制聚类（4 条）
| 机制 | 字段 | 含义 |
|---|---|---|
| S1 拥挤/集中 | crowding、concentration、manager_count、total_short_interest、sentiment | 空头拥挤度 → 轧空风险 |
| S2 知情深度/年龄 | age、security_avg_trade_length、manager_avg_trade_length、trade_length | 空头持仓时长 = 知情程度 |
| S3 流/突变 | position_change、security_short_count、security_cover_count、position、entry_position、is_open | 开空/回补流 |
| S4 活跃/关注 | activity、security_trade_count{_1wk,_1mo,_3mo,_1yr,_2yr,_3yr} | 交易关注度 |

## 3. 历史读数（2026-11-03 探针 + 12 臂，非本批）

- 方向定案：**挤压效应正向**（做空拥挤/集中/活跃 → 未来偏强）；反向臂 P1 crowding −0.22 / P3 concentration −0.28 / P4 activity −0.27 / P5 极限 −0.18。
- 12 臂结构扫描（decay4 / nanOFF / SUBINDUSTRY / subindustry 轴）：最好 **T10 `trade_when(age>0.5, 净开空流)` S0.61**；T2 activity 0.52；其余 0.07–0.43；T7 回补占比 −0.44；T12 专注度 −0.08。
- 结论：**信号层弱（PROVISIONAL，非六维判死）**；流/突变面全灭，条件交互最好但天花板 0.61。ATOM 至 1.58 无可见路径；与搭档腿组合需另测。

## 4. 本批处置

- **不进第一批**（弱面，先做 institutions6）。保留为「institutions 塔第二数据集」备份；若 institutions6 组合路线不达 1.58，再开 inst25 × MODEL/ANALYST 搭档批（覆盖 24/24 字段已登记）。
- 十年跨度未取（需任一有效 alpha 的 `get_alpha_yearly_stats`；数据集自 2012 起，理论可满 2014–2023）。

## 5. 类型/禁用

- 全 VECTOR：**必须** `vec_avg`/`vec_max`；裸用触发 `Operator ts_* does not support event inputs`（risk60 同类实证）。
- 覆盖率 0.0 是平台元数据，不判「无数据」（2026-10-14 修正口径：cov 0.27–0.34 字段平台可用；本集 2026-11-03 探针已有 S 读数）。
