# GBR 数据集覆盖度审计（D1 / TOP700）

生成：2026-11-09T10:53:11　工具：`tools/gates/audit_dataset_coverage.py`

## scope（引用本文任何结论前先读这一段）

- 样本来源：平台 `/data-sets` 全量实拉（`instrumentType=EQUITY region=GBR delay=1 universe=TOP700`），平台报 177 / 实拉 177（完整=True）
- 「有没有数据」判据 = **字段目录 `/data-fields` 非空**（fields_seen>0（/data-fields 目录）；coverage 只作辅助标记；持仓有无以探针 longCount+shortCount 为准）；coverage **不作为**存在性判据（见下节实测）
- 「挖过没」证据源：db:expressions, db:text(12677)（证据条数 56 个数据集）；证据通道状态 = OK
- ★ 证据链的第四个洞：`expressions.dataset` 在本区有 **3015 行（23.8%）为 NULL**——只按该列取「已测集」会把真实回测记成「没挖过」。本工具判据是**表达式原文里的字段名**，不是该列。
- ★ 证据盲区：MCP 直连仿真（create_simulation / create_multi_simulation）不写 data/wqb.db::expressions ⇒ 本工具的『挖过没』对这类记录盲视：池内『零挖掘记录』不等于没跑过。判『没挖过』前必须回波次日志/仿真台账核对。
- 探针回灌：`D:/coding/traeCN_project/wqb/data/dataset_assets/GBR_probe_results_d1.json`（16 条；实测有数据 16 / 实测无数据 0 / 失败 0）
- 截断条件：字段抽查每集最多 2 页（52 集被截断，177 集复用上次探针）；**截断存在 ⇒ 本文结论只覆盖该样本**

## ★ coverage 三层实测（本区最贵的教训）

| 层 | 实测 | 可作判据？ |
|---|---|---|
| 数据集级 `coverage` | `techindi_model` = 0.0，却有 399 字段、贡献 10 席中的 2 席 | ✗ |
| field 级 `coverage` | 本区 **109** 个集「所有字段 coverage 全 0」（109/177） | ✗ |
| 字段目录 `count` | 有字段即为「有数据」 | ✓ |

## 计数

| status | 含义 | 集数 |
|---|---|---|
| `TESTED` | expressions 有回测记录 / code 匹配到该集字段 | 65 |
| `LIT_EXCLUDED` | 塔已点亮（规则性排除，与数据无关） | 112 |

## 未点亮塔池（可开采池）

| 口径 | 集数 |
|---|---|
| 平台全量（D1 / TOP700） | 177 |
| 已点亮塔（规则性排除，不参与开采） | 112 |
| **可开采池** | **65** |
| 池内已挖掘（**本工具证据通道内**有记录） | 61 |
| 池内**有数据但本通道零记录**（探针已证有数据） | 4 |
| **池内真未探（有字段、零证据）** | **0** |
| 池内无字段（可判死） | 0 |

## ★ 有数据但本通道零记录（探针证明有数据 + 证据通道内无回测记录）

这些集有探针数据背书，但在**本工具的『挖过没』证据源**里找不到任何回测记录。
★ 别直接读成「一次都没跑过」：MCP 直连仿真不进 `expressions` 表，本工具对它盲视；
下结论前先回波次日志核对，否则就是拿「我的台账里没有」冒充「没人跑过」。

若核对后确实未开采，它们属容量未知区，不能与「已开采但没出东西」的集合并列用作「本区上限」的证据。

| dataset | category | 探针字段 | longCount | 探针 alpha |
|---|---|---|---:|---|
| `event_sentiment_signals` | other | `section_sentiment_score_3` | 343 | `O0Ado8a7` |
| `other78` | other | `entity_recognition_score` | 650 | `A1VXkpzl` |
| `stock_search_trends` | other | `search_interest_1y_equity_symbol` | 210 | `d5WJdGp2` |
| `socialmedia39` | socialmedia | `scl39_top5_people_also_watch_ticker_ii` | 424 | `ZYQVokoQ` |

**共 4 个集属于「有数据、本证据通道内零记录」**（口径见上，勿读成「没跑过」）。

## ★ 真未探清单（有字段目录、零回测证据）

（空）

## 门禁

- `coverage`：PASS
- `closure`：PASS

