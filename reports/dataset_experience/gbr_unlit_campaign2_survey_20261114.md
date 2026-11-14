# GBR 未点亮塔第二轮战役选集 survey（campaign2）

生成：2026-11-14　范围：GBR / TOP700 / D1（region 锁定）　前置：`gbr_delivery_manifest_20261114.md`（8 颗在篮）、`gbr_unlit_tower_survey_20261108.md`（第一轮普查）

## 0. 排除口径（用户三口径）

1. **只挖 D1 未点亮塔类别**：已亮 = model 6 / pv 4 / shortinterest 4 / news 3 / analyst 3 / fundamental 3；other=2（<3 阈值）算未点亮。已亮塔数据集**不作主攻**。
2. **已亮塔可作辅助腿**（借券腿=本区已证唯一 prod 通行证，11-13/14 实证）。
3. **挖到六维证伪为止**，不放宽约束凑数。

## 1. 覆盖审计门（skill 3b，成对跑，2026-11-14 实拉）

- 全量审计：`data/dataset_assets/GBR_coverage_audit_d1.json` + `gbr_coverage_audit_20261114.md` —— 177 集平台全拉，可开采池 65，**池内真未探（有字段、零证据）= 0**，65/65 TESTED（注意：`db:expressions` 通道对 MCP 直连仿真盲视，波次档案是补证）。
- 类别审计（`--field-audit`）：
  | category | 平台/已测 | 判定 |
  |---|---|---|
  | earnings | 2/2 | EXHAUSTED |
  | insiders / option / macro | 各全测 | EXHAUSTED |
  | other | 41/8 | **NOT_EXHAUSTED**（差集 33 集，但多为 MCP 直连已探——波次档案补证；唯一大缺口 = order_book_imbalance 226/240 字段） |
  | institutions/sentiment/risk/socialmedia/imbalance | 名义差集 | 均已被 11-08/11-13/14 波次实测收口（判死/判弱证据在 waves 档案） |

## 2. 候选清单与选定理由

| 序 | 数据集 | 塔 | 选定理由 | 主要风险 |
|---|---|---|---|---|
| **P1** | **earnings6** | earnings(0) | SUE 主腿 `2rAo7mm8` S1.74/F1.10/2Y2.78/fails=[]（平台复核）。**10 年逐年全正无空窗**（2026-11-14 实测逐年：最弱年 2020 S0.34 pnl+128k）⇒ **推翻 11-04 报告「五年空窗」数据集级否决**——那是 `P0gbMLz7` 特定表达式（divide 分母近零塌持仓）的缺陷，不是数据集缺陷 | prod 0.8595（DB 记录）+ self 0.7745（撞 3qoGxkqZ 共享借券腿）⇒ 双墙但归因清楚：破墙路径=纯 ATOM 化（去共享腿解 self）+ 中性化档扫（prod 杠杆，本区实证 SLOW/INDUSTRY 极差 0.11） |
| **P2** | **order_book_imbalance** | other(2) | 240 字段只测过 14（6%），11-11 明确「不判死」；覆盖三档分明（trade 分类组 cov 0.4294 全场最高）；字段画像已存档 `tracking/GBR/reference/gbr_order_book_imbalance_fields.json` | 已测 14 字段最强 0.56 且翻符号对称（真噪声特征）；深度组 cov 0.164 可能持仓面窄（先探针再开采） |
| P3 | macro27 | macro(0) | num_jobs_active S1.45/2Y3.62，Belo-Lin-Bazdresch 雇佣溢价 | F 墙 0.66；sub 0.17 覆盖弱；11-13 X1 波 4 臂全弱 ⇒ 降级备胎 |
| P4 | event_ml_signals / stock_search_trends / insiders12 / option1 | other/other/insiders/option | 次级备胎 | 0.52 / TO 墙 / 顶 1.04 / 顶 1.40 |

## 3. 不再投入清单（已证伪，沿用第一轮+11-13/14 波次证据）

sentiment27（2019 起数据，五年空窗一票否决）/ sentiment33（负年 4-6）/ sentiment7 / socialmedia5/12/39 / institutions 全家 5 集 / insider_matrix/trx/agg/insiders1 / risk 残差面（prod 0.85 机制层深墙）+ risk60/68/71/72 / imbalance5（prod 0.74-0.84 拥挤墙）/ other169 CDS（2Y 墙+STAT 摧毁信号）/ event_sentiment_signals / dl_riskfree / analyst7 / pattern_scores（S↔2Y 剪刀差封顶）/ model53/238/264/36 / news50/104 / option1 单集（S 死）/ earnings_sent_matrix（语气面全灭+覆盖 14 只）。

## 4. 执行顺序

Wave1 = ern6 纯 ATOM 破墙（中性化档扫 × SUE 结构变体，目标 prod<0.7+self<0.7 的 earnings 塔首亮）→ Wave2 = order_book trade 分类组（cov 0.43）字段族开采 → 视读数回补 macro27 或备胎。每集挖到证伪才换，换时在波次档案说明剩余未扫维度。
