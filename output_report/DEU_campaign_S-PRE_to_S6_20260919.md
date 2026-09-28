# DEU 战役执行报告（S-PRE → S6）

- **日期**：2026-09-19（GMT+8）
- **战役**：DEU REGULAR Alpha 挖掘战役（依据 `docs/reference/campaign_kickoff_prompt.md`，编排 `wq-brain-ra-pipeline` 九步骨架）
- **核心目标**：DEU 累计 10 颗 REGULAR alpha
- **用户附加铁律**：已点亮塔对应的数据集**不得优先选用**；优先未点亮塔或更低成本数据源
- **区域配置**：`universe=TOP500` / `delay=1` / `neutralization=SUBINDUSTRY` / `decay=4` / `truncation=0.08`（`tracking/DEU/config/settings.json`）
- **结论（先行）**：本波 S3 全灭（best|S|=0.29）；**DEU 当前累计 6 颗 ACTIVE（+4 未达成）**，未点亮塔可选集已枯竭；新增一颗“库存存活候选”可供用户决策提交。

---

## 0. 目标基线与平台真值

| 项 | 值 | 来源 |
|---|---|---|
| DEU 现有 ACTIVE REGULAR | **6**（`blRnKEk6` / `883Y3bAW` / `Vk65zLzG` / `vRk6og8b` / `2rOe10qY` / `JjxrYjre`） | `get_user_alphas(stage=OS, region=DEU)` = 212 扫描 / 6 命中 |
| 还差 | **+4** | 目标 10 − 现有 6 |
| 塔状态（平台权威） | 16 类中仅 **MODEL 已点亮（6/3）**；OTHER 2/3、SHORTINTEREST 2/3、INSIDERS 1/3；其余 12 类 0/3 | `recommend_datasets` → `category_summary` |
| 关键结构墙 | 精确最大互斥集 size=6，**6 颗已全部 ACTIVE**（`max_clique_proof`，`compute_mutual_correlation` 精确搜索） | ledger `submit_ready.max_clique_proof` |
| 停止闸状态 | 最近 3 个 closed 波 verdict = `PARTIAL / FAIL / FAIL`（再 1 个 FAIL 触发规则 B 全区暂停） | `stop_rules_gate`evidence |

---

## 1. 步 1（S-PRE）查表

**触发条件**：战役启动，`entry_verdict: probe-only`（DEU profile 2026-09-11 审计补建）。

**输入（MCP / CLI）**
- `get_campaign_summary` / `get_dead_ends` / `get_dead_datasets` / `get_cross_region_lessons` / `get_mining_yield(by_dataset)` / `get_ledger_key(region_kb, s0_whitelist, submit_ready)`
- `get_user_alphas(region=DEU, stage=OS)`、`recommend_datasets(DEU, D1, TOP500)`
- 库存盘点（SOP 强制前置）：`tools/build_gate_prior_from_inventory.py --regions DEU --emit-candidates --write-priors`

**输出**
| 项 | 结果 |
|---|---|
| 战役规模 | 114 波全 closed；dead_end **30** 条 |
| 判死数据集（12） | analyst35/44/48、model141/16/262、news50、other128/532/546、risk88、workforce_flow_skills |
| 本区产出率（严格口径） | 回测 1294 行 → ra_clean 164 → **prod_clean 4 / prod_blocked 42**（已测 prod 者 91% 撞墙）；conversion 仅 10.3% |
| 库存盘点 | 扫 1000 条 IS → 过闸 **79** 条候选（7.9%），全部未提交 |
| 篮内正交（`select_ra_basket`） | 265 条互相关计算；**OS 撞车剔除 42/44** → 最终篮 **1 条：`6XrJ5OvE`**（S 1.80 / F 1.93 / 2Y 2.27 / maxCorr 0.6732 / **挂 MODEL 塔**） |
| 跨区铁律命中 | `GLOBAL-CROSS-DATASET-SAME-DOMAIN-LOCK`、`GLOBAL-INSIDER-DOMAIN-SUPERFAMILY`、`PRODCORR-SATURATION-UNIVERSAL`、`SHARPE-HAS-ZERO-PROD-DISCRIMINATION` |

**异常 / 风险**
- `build_gate_prior_from_inventory` 中途 1 次代理层断连（offset=100 页），脚本自身重试成功（`[DEU] 取回 1000 条`）。
- `select_ra_basket` 首跑 SSL EOF 失败 → 重跑成功（瞬态）。
- **判定**：库存 79→1，且唯一存活者落在已点亮塔 → 用户铁律下不可作为主路径；→ 进 S0 开新挖。

---

## 2. 步 2（S0）数据集体检 + 金字塔配置

**触发条件**：库存清空后候选不足以覆盖目标座位（`est_seats` 缺口）。

**输入**
- `tools/campaign_intel.py s0-select --region DEU --delay 1 --universe TOP500 --top-n 15 --target 4`
- `workflow_campaign(stage="S0", calibrate=true)` → `workflow_campaign(stage="S0")`

**输出**
| 项 | 结果 |
|---|---|
| calibrate | 995 alphas / 25 ds 实测；权重：model 1.15、institutions/analyst/other 1.0、insiders/shortinterest/pv/news 0.9；**拥挤甜区 ac 79–374** |
| s0-select（平台推荐 45 集） | 剔除判死 12 → 存活 **33**；`lit=Y` 剔除 **0**（平台推荐本身已限未点亮塔） |
| top5 | news81(63.97) / option1(63.49) / fundamental17(61.75) / risk60(61.72，yield 0.733@15bt) / pv20(61.33) |
| 座位可达性 | Σest_seats=30 ≥ target 4 → 预算充足 |
| 锁定白名单 | 5 集：`option1` / `pv20` / `fundamental17` / `other699` / `risk60`（**全部未点亮塔，MODEL 系全部剔除**） |
| 排除清单（记因） | news81/news17/news104/earnings_sent_matrix（DEU 新闻情绪族全域判死）、macro27（residual dead）、fundamental6（cov 0.49 越档）、intraday_pv_feats（跨区弱+死名单）、pv30/pv29（分类集非信号本体）、pattern_scores/institutions6/fund_holdings_panel/insider_agg_matrix/sentiment27（已判死/弱） |

**异常 / 风险**
- `[WARN] s0_whitelist 未记录 universe`（P3 守卫失效）→ 本次已把 `universe=TOP500` 写进白名单台账修正。
- `[WARN] other545 override-gap`：自动判 hard_excluded 却手工纳入且无 override 理由 → 已从白名单剔除。
- 选出的 top3 **当时未经字段级覆盖校验**（→ 由 S1 兜住，见步 3）。

---

## 3. 步 3（S1）字段扫描 + 覆盖审计

**触发条件**：白名单锁定后（SOP 硬前置：体检包/字段目录必须先落地）。

**输入**：`workflow_campaign(stage="S1", dataset=$DS)` × 4（option1 / pv20 / fundamental17 / risk60）

**输出（字段级 coverage 为核心判据）**

| 数据集 | 字段数 | data_type | max coverage | 判定 |
|---|---|---|---|---|
| option1 | 22 | VECTOR | **0.0** | **EMPTY_IN_DEU**（22/22 全 0） |
| pv20 | 681 | MATRIX | **0.0** | **EMPTY_IN_DEU**（681/681 全 0） |
| fundamental17 | 135 | MATRIX | **0.0** | **EMPTY_IN_DEU**（135/135 全 0） |
| **risk60** | 5 | VECTOR | **0.835** | **COVERAGE_OK — 唯一可挖** |
| 对照组（同区他集） | — | — | 0.63–0.98 | news18 0.69–0.98 / shortinterest3 0.65–0.78 / analyst93 0.63–0.65 / other455 0.72–0.84 |

**异常 / 关键系统性问题**
1. `pv20` 首跑 **HTTP 429** 失败 → 重跑成功（并发 + 另一会话 GBR 战役同时启动，触发平台限流）。
2. ★ **平台 `recommend_datasets` 链路不校验区域字段覆盖率**：本次 top3 全为 DEU 空集。对照组证明 0.0 是真实缺数而非上报口径问题（DEU D0 曾有同型事故 `DEU-W104-D0-DATASET-EMPTY-DEAD`）。
3. DEU 全域 `field_inspect_deu_*` 体检包 = 0，本地 `WebData_20260219_V0.10.9.zip` 不含 DEU → 步 5 体检硬门只能 `warn` 降级，已按要求在台账 `inspect_mode_degradation_20260919` 记因。

**回写**：ledger `catalog_option1/pv20/fundamental17/risk60`、`s1_coverage_audit_20260919`、`s1_risk60_d1`。

---

## 4. 步 4（S2）概念优先选波

**触发条件**：S1 收敛到唯一可行数据集 `risk60`（未点亮塔 RISK 0/3）。

**输入**
- `workflow_campaign(stage="S2", subcommand="assemble-priors")` → `tracking/DEU/priors/deu_priors.json`（wins=6 / dead_ends=12 / sha256 `f0eb4ed4…`）
- `workflow_gem(region=DEU, dataset_id=risk60, delay=1, universe=TOP500, data_type=VECTOR)`

**输出**
- GEM 概念优先产出 **7 条**表达式 → `expressions/DEU/s2_risk60_d1`（status=`gem`）、idea ledger `s2_risk60_d1_idea`
- 机制族：① 放量时段（`rsk60_datatime` 订单流时钟）+ crowding 方向；② 净卖空失衡 `ts_sum(crowding)/ts_sum(|crowding|)` vs 借券费率均值回复的 `ts_corr` 残差式应力读数；③ `vector_neut` 剔除 crowding 后的费率变化残差。

**异常 / 风险**
- ★ MCP `workflow_gem` **detached 存活握手失败**（“still running but no meta.json within 90s”），实测前台同命令 **<240s 正常完成**并落库 → 判定为握手窗口/并发扰动导致的假失败，非 GEM 本体故障（已记录，建议后续对该节点用 `launch_only=true` 或放宽握手窗口）。
- priors 组装前置闸：`signal_floor` 放行（max|S|=0.72 / 2 批）、`stop_rules` 放行（PARTIAL/FAIL/FAIL）、`backlog` WARN（未消化 1320/1671 = 79%）。

---

## 5. 步 5（S2→S3）门禁

**触发条件**：GEM 落库后、发批前。

**输入**：`tools/wave_gate.py --campaign-dir tracking/DEU --dataset risk60 --wave s2_risk60_d1 --from-db`

**输出**
| 闸 | 结果 |
|---|---|
| 区域四道前置闸 | catalog / signal_floor / stop_rules / backlog **全放行** |
| 语法闸 | **7/7 PASS** |
| gate.py 闸 1–5 + 7/8 | `all_pass=true`，passed 7/7 |
| prod 饱和闸 | enforced PASS（10 个历史饱和字段，当前波零命中） |
| 体检硬门 | ⚠ **未生效**（缺 `field_inspect_deu_risk60.json`，快照无 DEU 数据）→ 已记因 |
| 六维多样性 | ⚠ WARN：结构熵 0.86<1.5、机制熵 1.84<2.0、`structure.single_aggregated` 超配 **71%**、缺 Group 类别 |
| 家族天花板预警 | ⚠ 主导腿 `lending_fee_bid_rate` 占 **71%**（≥67%）→ 预测 SELF≥0.9 |
| 质量预估 | DIRECT 0 / COMBO 0 / **WEAK 7** / BLOCK 0 |

**产物**：`gate_results/DEU/s2_risk60_d1/risk60`

---

## 6. 步 6（S3）+ 步 7（S4）回测与诊断

**触发条件**：门禁 all_pass。

**输入**：`workflow_batch_track(region=DEU, wave=s2_risk60_d1, dataset=risk60, concurrency=7, submit=true)`

**输出**
- multisim `2GBhm6xT4vualK1cT71Y0TP`，n=7 → **COMPLETE 7/7**（0 隔离、0 重发）
- `backtest_results +7/7`；`region_kb` 刷新（recent_waves+1，`gate_priors_local` n=1301）
- 配额：`used=0 remaining=4`（回测通道 enabled=False，不占 REGULAR 提交额度）
- **诊断（S4）**：`candidates=0 near=0`（全灭快速通道）

| alpha | sharpe | fitness | 2Y | sub | ra_failed_checks |
|---|---|---|---|---|---|
| O0NqMam7 | **0.29** | 0.12 | 1.28 | 0.07 | L_S/L_F/L_SUB/L_2Y |
| 9qjbd062 | 0.26 | 0.07 | -0.22 | 0.28 | L_S/L_F/CW/L_2Y |
| Wjbno8dx | 0.07 | 0.02 | -0.30 | 0.16 | L_S/L_F/CW/L_2Y |
| j2AWPmdZ | -0.12 | -0.02 | 0.09 | 0.35 | L_S/L_F/CW/L_2Y |
| e7bgVRqJ | -0.18 | -0.04 | 0.11 | 0.28 | L_S/L_F/CW/L_2Y |
| d5bg3LlY | -0.63 | -0.46 | -0.67 | -0.85 | L_S/L_F/CW/L_SUB/L_2Y |
| j2AWPmwQ | -0.65 | -0.20 | -1.86 | -0.42 | L_S/L_F/HT/CW/L_SUB/L_2Y |

**墙定位**：主墙 = `LOW_SHARPE`（信号天花板，best 0.29 距 Mode B 资格线 1.25 差 0.96）；次墙 = `CONCENTRATED_WEIGHT`（4/7）+ `LOW_SUB_UNIVERSE_SHARPE`。**非 prod 墙**（未到该环节）。

---

## 7. 步 8（S5）提交判定

**状态：未执行（无合格候选）**

- Failed-count 资格门：0 条候选通过，无对象可判。
- 唯一可提交对象来自步 1 库存扫描：`6XrJ5OvE`（S 1.80 / F 1.93 / 2Y 2.27 / maxCorr 0.6732）——**但挂 DEU/D1/MODEL（已点亮塔）**，按用户铁律属“浪费配额”，**未提交，等用户裁决**。
- 今日 REGULAR 配额：remaining **4**（00:00 ET 重置，即 GMT+8 次日 12:00）。

---

## 8. 步 9（S6）复盘回写

| 回写对象 | 内容 |
|---|---|
| `wave_results` | wave_number 1789832547，verdict **FAIL**，best|S|=0.29，candidates=0，7 条 key_findings |
| `registry_empirical/dead_end` | `DEU-RISK60-FEE-CROWDING-DEAD-20260919`、`DEU-EMPTY-COVERAGE-S0-PICKS-20260919` |
| `ledger_kv` | `risk60_dead` / `option1_dead` / `pv20_dead` / `fundamental17_dead` / `s6_verdict_s2_risk60_d1` / `s1_coverage_audit_20260919` / `inspect_mode_degradation_20260919` / `s0_whitelist`(重建) |
| `region_kb` | 由 pipeline 自动刷新 recent_waves + gate_priors_local |

**漏斗（全区，只读推导）**：S2 生成 1671 → 门禁放行 1272 → 回测 1301 → 过廉价闸 315 → 提交就绪 72（保留率 22.9%，瓶颈跳 = 过闸→就绪）。

---

## 9. 结论与下一步（决策点）

### 9.1 硬结论

1. **DEU +4 在本轮不可达**。三条独立证据链收敛：
   - 库存侧：79 条过闸候选 → OS 撞车剔 42/44 → 仅 1 条存活，且落在已点亮塔；
   - 结构侧：精确最大互斥集 = 6（已全部 ACTIVE），新增必须对 6 颗全部 <0.7；
   - 选区侧：未点亮塔中唯一覆盖有效的数据集 `risk60` 已探完并判死（信号天花板 0.29）。
2. **用户铁律有效但当前无可行域**：已点亮塔（MODEL）支撑了唯一库存存活候选；未点亮 15 类中，12 类已有判死证据、OTHER/SI/INSIDERS 的近点亮位置被既有 ACTIVE 的 SELF 墙占死（OTHER 由 `2rOe10qY`+`JjxrYjre` 占、SI 由 `blRnKEk6`+`vRk6og8b` 占）。
3. **发现一个系统性缺陷**（值得修）：`recommend_datasets → campaign_intel s0-select` 不校验区域字段覆盖率，本次把 3 个 DEU 空集推到 top3；选区必须回落到 S1 字段级覆盖审计。已在 dead_end 沉淀，避免复用。

### 9.2 可选下一步（需用户裁决）

| 选项 | 动作 | 代价 / 判断 |
|---|---|---|
| A | 提交 `6XrJ5OvE`（MODEL 塔） | 直接 +1 → 累计 7；**违反“不优先已点亮塔”铁律**，但该颗已在库、零额外成本（仅 1 次配额） |
| B | 扩大 data source 后重开 DEU | 需先更新 WebDataScope 导出包（补 DEU）→ 才能生成体检包并覆盖审计未试点集（other545/other699/insider_matrix 等） |
| C | 转区域决策 | DEU 命中停止规则 B 风险高（PARTIAL/FAIL/FAIL + 本波 FAIL）；可转 `brain-next-move-analysis` 或 `wq-brain-campaign-matrix` 换区 |
| D | 换塔策略 | 先补 OTHER（差 1 颗点亮）——但须先找到 <0.7 于 `2rOe10qY` 与 `JjxrYjre` 的新机制集；下一轮白名单可用 `other699`（7 字段，零竞争）做小批探针 |

> 提交任何 alpha 前必须经用户确认（SOP 步 8）；本报告未执行任何提交。
