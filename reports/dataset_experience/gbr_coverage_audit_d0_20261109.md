# GBR 数据集覆盖度审计（D0 / TOP700）

生成：2026-11-09T10:53:21　工具：`tools/gates/audit_dataset_coverage.py`

## scope（引用本文任何结论前先读这一段）

- 样本来源：平台 `/data-sets` 全量实拉（`instrumentType=EQUITY region=GBR delay=0 universe=TOP700`），平台报 73 / 实拉 73（完整=True）
- 「有没有数据」判据 = **字段目录 `/data-fields` 非空**（fields_seen>0（/data-fields 目录）；coverage 只作辅助标记；持仓有无以探针 longCount+shortCount 为准）；coverage **不作为**存在性判据（见下节实测）
- 「挖过没」证据源：db:expressions, db:text(12677)（证据条数 56 个数据集）；证据通道状态 = OK
- ★ 证据链的第四个洞：`expressions.dataset` 在本区有 **3015 行（23.8%）为 NULL**——只按该列取「已测集」会把真实回测记成「没挖过」。本工具判据是**表达式原文里的字段名**，不是该列。
- ★ 证据盲区：MCP 直连仿真（create_simulation / create_multi_simulation）不写 data/wqb.db::expressions ⇒ 本工具的『挖过没』对这类记录盲视：池内『零挖掘记录』不等于没跑过。判『没挖过』前必须回波次日志/仿真台账核对。
- 截断条件：字段抽查每集最多 2 页（10 集被截断，73 集复用上次探针）；**截断存在 ⇒ 本文结论只覆盖该样本**

## ★ coverage 三层实测（本区最贵的教训）

| 层 | 实测 | 可作判据？ |
|---|---|---|
| 数据集级 `coverage` | `techindi_model` = 0.0，却有 399 字段、贡献 10 席中的 2 席 | ✗ |
| field 级 `coverage` | 本区 **42** 个集「所有字段 coverage 全 0」（42/73） | ✗ |
| 字段目录 `count` | 有字段即为「有数据」 | ✓ |

## 计数

| status | 含义 | 集数 |
|---|---|---|
| `UNTESTED_BLIND` | ★ 有字段 + coverage 元数据全 0 + 零回测证据 ⇒ 必须探针 | 24 |
| `UNTESTED_COV_OK` | 有字段且元数据说有用量，但零回测证据 | 4 |
| `TESTED` | expressions 有回测记录 / code 匹配到该集字段 | 45 |

## 未点亮塔池（可开采池）

| 口径 | 集数 |
|---|---|
| 平台全量（D0 / TOP700） | 73 |
| 已点亮塔（规则性排除，不参与开采） | 0 |
| **可开采池** | **73** |
| 池内已挖掘（**本工具证据通道内**有记录） | 45 |
| 池内**有数据但本通道零记录**（探针已证有数据） | 0 |
| **池内真未探（有字段、零证据）** | **28** |
| 池内无字段（可判死） | 0 |

## ★ 有数据但本通道零记录（探针证明有数据 + 证据通道内无回测记录）

这些集有探针数据背书，但在**本工具的『挖过没』证据源**里找不到任何回测记录。
★ 别直接读成「一次都没跑过」：MCP 直连仿真不进 `expressions` 表，本工具对它盲视；
下结论前先回波次日志核对，否则就是拿「我的台账里没有」冒充「没人跑过」。

若核对后确实未开采，它们属容量未知区，不能与「已开采但没出东西」的集合并列用作「本区上限」的证据。

（空）

## ★ 真未探清单（有字段目录、零回测证据）

| dataset | category | valueScore | alphaCount | 字段数 | maxCov | 元数据盲区 | status |
|---|---|---|---|---|---|---|---|
| `mmp_nlp_sentiment` | other | 7.0 | 20 | 72/72 | 0.0 | 是 | `UNTESTED_BLIND` |
| `model253` | model | 7.0 | 0 | 2/2 | 0.0 | 是 | `UNTESTED_BLIND` |
| `model50` | model | 7.0 | 4 | 51/51 | 0.0 | 是 | `UNTESTED_BLIND` |
| `univ1` | pv | 7.0 | 0 | 1/1 | 0.0 | 是 | `UNTESTED_BLIND` |
| `event_sentiment_signals` | other | 6.0 | 5 | 52/52 | 0.0 | 是 | `UNTESTED_BLIND` |
| `london_sentiment` | model | 6.0 | 1 | 7/7 | 0.0 | 是 | `UNTESTED_BLIND` |
| `model257` | model | 6.0 | 0 | 5/5 | 0.0 | 是 | `UNTESTED_BLIND` |
| `news46` | news | 6.0 | 1 | 19/19 | 0.0 | 是 | `UNTESTED_BLIND` |
| `quant_factor_lib` | model | 6.0 | 0 | 100/190 | 0.0 | 是 | `UNTESTED_BLIND` |
| `search_interest` | other | 6.0 | 2 | 6/6 | 0.0 | 是 | `UNTESTED_BLIND` |
| `analyst10` | analyst | 5.0 | 60 | 100/592 | 0.0 | 是 | `UNTESTED_BLIND` |
| `analyst16` | analyst | 5.0 | 3 | 56/56 | 0.0 | 是 | `UNTESTED_BLIND` |
| `analyst8` | analyst | 5.0 | 6 | 3/3 | 0.0 | 是 | `UNTESTED_BLIND` |
| `chart_return_model` | pv | 5.0 | 36 | 8/8 | 0.0 | 是 | `UNTESTED_BLIND` |
| `model239` | model | 5.0 | 21 | 14/14 | 0.0 | 是 | `UNTESTED_BLIND` |
| `model37` | model | 5.0 | 39 | 29/29 | 0.0 | 是 | `UNTESTED_BLIND` |
| `news29` | news | 5.0 | 0 | 8/8 | 0.0 | 是 | `UNTESTED_BLIND` |
| `news73` | news | 5.0 | 1 | 22/22 | 0.0 | 是 | `UNTESTED_BLIND` |
| `model252` | model | 4.0 | 7 | 3/3 | 0.0 | 是 | `UNTESTED_BLIND` |
| `model27` | model | 4.0 | 2 | 6/6 | 0.0 | 是 | `UNTESTED_BLIND` |
| `news21` | news | 4.0 | 0 | 12/12 | 0.0 | 是 | `UNTESTED_BLIND` |
| `news7` | news | 3.0 | 3 | 1/1 | 0.0 | 是 | `UNTESTED_BLIND` |
| `pv20` | pv | 3.0 | 0 | 100/100 | 0.0 | 是 | `UNTESTED_BLIND` |
| `risk59` | risk | 3.0 | 1344 | 16/16 | 0.0 | 是 | `UNTESTED_BLIND` |
| `analyst45` | analyst | 6.0 | 4 | 38/38 | 0.3952 | 否 | `UNTESTED_COV_OK` |
| `institutions1` | institutions | 5.0 | 6 | 8/8 | 0.4856 | 否 | `UNTESTED_COV_OK` |
| `other532` | other | 5.0 | 55 | 1/1 | 0.7639 | 否 | `UNTESTED_COV_OK` |
| `model242` | model | 3.0 | 2985 | 5/5 | 1.0 | 否 | `UNTESTED_COV_OK` |

