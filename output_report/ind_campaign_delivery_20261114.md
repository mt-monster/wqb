# IND REGULAR Alpha 战役交付报告 · 2026-11-14

> 战役产物 → `output_report/`。执行期 2026-11-14 11:47–15:2x GMT+8，全程 IND/TOP500/D1 固定档（STATISTICAL/decay4 或 126/trunc0.08/P0Y0M0D/nanHandling OFF/maxTrade OFF），MCP 全链路，**未提交任何 alpha**（只挖不提交，提交权归用户）。

## 0. 结论

| 指标 | 目标 | 实际 |
|---|---|---|
| 新挖候选（回测+归因） | ≥20 | **53 条**（8 波 multisim，全部新表达式，无历史篮子复用） |
| IS 层 RA 全闸（failed_ra_count=0） | — | **13 颗** |
| 交付（全闸+self<0.7+prod<0.7 refresh+互相关<0.7+组腿≤5） | 10 | **5 颗**（配额 5/5 用满）+ 1 颗备选（3qj1eYdz，双贴线） |
| ATOM（effective=1） | 优先 | **0 颗**（21 条 ATOM 形态全灭，见 §4） |

10 颗未达成的结构原因（证据链见 §4–§5）：IND 的有效信号只存在于「`returns` 残差化」形态（必为 PV+X 双塔），单集 ATOM 全部强度不足；双塔候选受互相关（G1 同骨架 0.72–0.95）与跨 trio 组腿配额 ≤5（`locked.py TOWER_TRIO_CROSS_QUOTA`，用户 10-27/28 定案，未授权放宽）双重约束，合规面上限 = 5–6 颗。

## 1. 交付清单：5 颗验证通过的 Regular Alpha

全部满足：S≥1.58 / F≥1.0 / 2Y≥1.58 / SUB 比值过 / robust≥1.0 / TO≤0.40 / self<0.7 / **prod<0.7（refresh=True 当刻重测）** / 2014–2023 逐年 PnL 有数据 / 两两互相关<0.7 / 跨 trio 组腿 5/5。

| # | alpha_id | dataset | 核心字段 | 算子逻辑 | S | F | 2Y | robust | TO | self | prod(refresh) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `MP69RYAk` | institutions6 | quantity_institutional_shares_disposed | G1 残差：`rank(-ts_regression(ts_zscore(returns,252), ts_zscore(<F>,252),252,rettype=0))` decay126 | 2.98 | 2.25 | 2.79 | 1.70 | 0.244 | 0.658 | **0.6699** |
| 2 | `LL5Edbee` | institutions6 | aggregate_share_count_all_owners | 同 G1 骨架（筹码数锚） | 2.53 | 1.78 | 2.79 | 1.28 | 0.237 | 0.634 | **0.6327** |
| 3 | `rK7Qm6ld` | sentiment21 | snt21_neg_std | G1 残差 decay8（角点：robust 0.99→1.04） | 2.15 | 1.20 | 3.45 | 1.04 | 0.257 | 0.251 | **0.5634** |
| 4 | `e7aeJoEd` | earnings3 | ern3_pre_interval | G1 残差 decay126（判死复开件，ts_backfill(20) 补洞） | 2.38 | 1.72 | 2.13 | 1.91 | 0.223 | 0.507 | **0.5124** |
| 5 | `qM7eZoVO` | earnings3 | ern3_next_interval | 同 G1 骨架（下次财报间隔锚） | 1.90 | 1.42 | 2.02 | 1.62 | 0.171 | 0.502 | **0.5018** |

**塔归属 5 列**（每颗：归属 → 当季计数 → 交后计数 → 是否新点亮 → 边际增量）：

| alpha_id | 塔归属 | 当季计数 | 交后计数 | 是否新点亮 | 边际增量 |
|---|---|---|---|---|---|
| MP69RYAk | INSTITUTIONS(1.0)+PV(1.1) | 1 / 11 | 2 / 12 | INSTITUTIONS 仍差 1 | 倍率 1.0（短板） |
| LL5Edbee | INSTITUTIONS+PV | 1 / 11 | 2 / 12 | 同上 | 倍率 1.0 |
| rK7Qm6ld | SENTIMENT(1.2)+PV(1.1) | 1 / 11 | 2 / 12 | SENTIMENT 仍差 2 | 倍率 1.1 |
| e7aeJoEd | EARNINGS(1.1)+PV(1.1) | 2 / 11 | 3 / 12 | **EARNINGS 点亮（2→3）** | 新点亮 1 座塔 |
| qM7eZoVO | EARNINGS+PV | 同上 | 同上 | 若与 #4 同季同提，第 2 颗不再产生点亮 | 第 1 颗已点亮 |

⚠ `e7aeJoEd` 是本轮唯一的新点亮载体（EARNINGS 差 1 颗）；若用户只提交一颗，优先它可点亮 EARNINGS 塔。`submit_verdict` 7/7 = UNVERIFIABLE_404（平台死端点，模拟层 `failed_ra=0`、零硬闸 WARNING），非 BLOCKED；**放行需用户点名确认**。

互相关矩阵（篮内最大对）：`MP69RYAk`↔`LL5Edbee` 0.6095、`e7aeJoEd`↔`qM7eZoVO` 0.6965，全部 <0.7。近十年逐年 sharpe 全部为正年份 ≥9/10（`rK7Qm6ld` 2015 弱年 0.67 仍为正）。

备选第 6 颗：`3qj1eYdz`（inst6 aggregate_equity_value_all_owners 残差，S 2.76/F 1.97/robust 1.43，self **0.6976** / prod **0.6962** 双贴线）——按 prod 池膨胀铁律（每次提交整族上移）判为高危，不进主篮；若用户接受贴线风险可替换 #2 或 #5。

## 2. 候选清单与选定理由

见 `reports/ind_dataset_selection_20261114.md`（逐集理由 + 数据集级排除算法）与 `output_report/ind_dataset_scan_20261114.md`（144 集全量明细）。主攻 5 集：institutions6（P0 未亮塔×全 ALIVE）、sentiment21（P0 验证性）、earnings11（P0 动态覆盖门）、model77 / other323（P1 未占用，后证实为 WEAK_MECHANISM）。白名单 `s0_whitelist.campaign_20261114` 已 merge 写入。

## 3. 字段画像存档索引

| 产物 | 路径 | 说明 |
|---|---|---|
| 逐集 typed catalog ×5 | `tracking/IND/reference/ind_{institutions6,sentiment21,earnings11,model77,other323}_fields.json` | MCP 实读 185 字段 100% 覆盖（complete=true） |
| 逐集 8 列画像 ×5 | `reports/dataset_experience/ind_<ds>_field_profile_20261114.md` | type/coverage/userCount/alphaCount/更新频率/分布特征/可用性/alpha 适用性 |
| 逐 category 总表 | `reports/dataset_experience/ind_field_profiles_survey_20261114.md` | 三条须知 + 画像表 + 关键字段 + 判死通道 |
| 索引 | `tracking/IND/reference/ind_field_profile_index_20261114.json` + `reports/ind_field_profile_index_20261114.md` | 命名规则 + 对账记录 |

命名规则：人工报告 `snake_case_YYYYMMDD` 后缀；`tracking/IND/reference/ind_<ds>_fields.json` 沿用既有名；**未占用 `*_campain.md`**（生成器既定名，AGENTS.md:1177）。

## 4. 调优经验摘要（归因杠杆 + 对比实验）

| 实验（只动 1 变量） | Δ 读数 | 结论 |
|---|---|---|
| G1 decay 4 → 126（inst6 残差 3 锚） | TO 0.83→0.24，S 4.79→2.98，F 2.51→2.25，**failed_ra 1→0** | HIGH_TURNOVER 0.40 墙的唯一破法 = 大 decay；S 损失可接受（仍 2.5+） |
| snt21 残差 decay 4 → 8（角点搜索） | robust 0.99→1.04 / TO 0.418→0.257，failed_ra 3→0 | decay8 是 robust/TO 的 knife-edge 角点；winsorize/quantile 外壳不改读数（残差已 rank 化） |
| snt21 残差 decay 63/126 | robust 0.64/0.55，S 1.54/1.43 | decay 过大 → 强度塌陷；角点区间 [8, 63) |
| G6 持仓广度 ATOM（ts_delta 66） vs G1 残差 | 0.53 vs 2.98 | 同字段，信号只活在残差形态 |
| G5 winsorize vs quantile（sent21） | 逐位等价（rank 后再截尾无增量） | 截尾算子对已 rank 化信号是空转 |
| ern3 interval 裸水平/短变换 vs 残差化 | −0.75~0.74 vs 2.38 | 10-18 画像 S4.49 无法复现（当时为 IS 全期口径），残差化才过闸 |

淘汰记录全量：53 条候选的 S/F/TO/败闸/归因见 §6 台账文件。

## 5. 可复用结论（带证据）

1. **IND ATOM–强度铁证**：21 条单集 ATOM（inst6 广度/共动/比率/慢变量、ern3 裸水平/内部残差、snt21 长窗/差分）max S = 0.74，全部 <1.58；同一字段的残差形态 S 2.0–3.1。**IND 可交面 = 残差化双塔，ATOM 需新数据维度**（alpha id：E5Qo765m/WjlKqO1N/d5aeQELY/gJa77Q20 等 21 颗全灭件）。
2. **残差化 decay 阶梯**：TO 超标 → decay126（TO 0.24）；robust 贴线 → decay8 角点；两头贴线（如 1YW6Qz6X robust 0.99 + 后测 prod 0.7214）无解。
3. **prod 池膨胀实证**：`1YW6Qz6X` W3 互测时未测 prod，终验 refresh=True 得 **0.7214 越线**（同族 9 颗里唯一）；同骨架锚间 self 0.72–0.95，G1 族合规篮上限 3 颗。
4. **工具陷阱（沉淀进 skill）**：`get_datafields(max_fields=null)` 显式传 null 触发 `max_fields_cap` 只返 1 条（5/5 集复现）；必须不传或传 ≥platform_count。`quantile(..., driver="gaussian")` 的 `gaussian` 会被 preflight 误判为 unknown_field（假阳性，可放行）。
5. **DB 画像会过期**：`model77` DB 记 348 字段/cov 0.85，平台实读 23 字段/cov 0.4001（ESG 治理分）——选集必须 MCP 实读复核，DB 只作预筛。
6. **塔快照漂移**：11-14 当季实读（已亮 7 座，institutions/sentiment/earnings/macro/insiders/imbalance/option/shortinterest 未亮）与 11-05/11-06 快照均不同；每轮战役必须现查 `get_pyramid_alphas()`。
7. **sent21 跨 4 区判死告警应验**：`dead_intersection` high 告警 → 裸字段/长窗 ATOM 全灭；唯一活路 = 对 returns 残差化（`rK7Qm6ld` 已交付）。「跨区判死」禁的是机制不是数据集本身。

## 6. 更换 dataset 与淘汰原因

无换集（用户「不频繁换」）。四个 WEAK_MECHANISM 集按配额用完即止，未触发 switch 报告条件：`sentiment21`（跨区告警验证性 2+2 条）、`earnings11`（35 全 VECTOR 元数据，2 条全灭）、`model77`（ESG 治理 2 条 + 残差 2 条全灭）、`other323`（静态 VECTOR，2 条全灭）。ern3 复开成功属 earnings3（红榜内 interval 特例，10-18 已标）。

## 7. 台账与回写

- 全量候选台账：`tracking/IND/results/ind_candidate_ledger_20261114.md`（53 条：expr/锚/decay/S/F/TO/败闸/verdict/归因）
- 判死回写：`seal_dead_end` ×5（IND-SENT21-BARE-DEAD / IND-EARN11-VECTOR-META-DEAD / IND-MDL77-ESG-WEAK-DEAD / IND-OTHER323-STATIC-DEAD / IND-ATOM-BARE-STRUCT-DEAD）
- 波次结论：`upsert_wave_result` W1–W8
- 台账 key：`candidate_basket_20261114`（5+1 颗终验值）
- 人工复盘：`reports/ind_atom_delivery_review_20261114.md`；调优经验：`reports/ind_tuning_experience_20261114.md`
