# 2026-09-23 Dry-Run 全链审计与可提交因子优化方案

> 视角：资深金融 quant 工程。目标：把「生成量大」转化为「可提交因子产出」。
> 方法：19 个 workflow 节点全量 dry-run + 1320 单测回归 + 只读漏斗/DB 探查，零平台配额消耗。
> **进度（2026-09-25 v2 复盘更新）**：
> - **P0-1 两批已完成**：GLB/ASI 批（O0NoPARJ 提交 ACTIVE，18 撞墙）；KOR/USA 批（**KP78pLWk VERIFIED 待用户确认提交**，6 撞墙，np8VGNz3/VkGJ73eA 终验进行中）。
> - **KOR 20% 历史撞墙率被证伪：实际 4/5=80%** ——「篮子顶层=拥挤信号集中区」跨区成立，两批合计 24 验仅 2 颗过墙（8%）。
> - Phase2 工具 bug 已修复 +7 单测；积压持续恶化（374 波/25,960 条无门禁、519 波/7,338 条超 7 天）。
> - **v2 优先级结论：库存收割暂停扩量，转向 P1 结构修复 + 换筛选条件**（见 §五）。

## 一、Dry-run 审计结果（基础设施健康度：良好）

| 检查项 | 结果 |
|---|---|
| `tools/audit_node_registration.py`（registry/test/dry-run/INDEX 四处同步） | ✅ 19/19 节点无漂移 |
| 全量回归 `pytest tests/` | ✅ 1320 passed, 9 skipped（42.9s） |
| `tools/sync_skills.py --check`（4 个安装位） | ✅ 无漂移 |
| 19 节点逐个 `dry_run=True` | ✅ 18/19 通过；`hypothesis_round` 缺假设目录 fail-closed 拒绝并带因，**符合契约非缺陷** |

**结论：skills/workflow 机械化层无漂移、无静默失败。短板不在代码，在数据流转与执行纪律。**

## 二、实测暴露的四个结构性瓶颈（按严重度排序）

### 瓶颈 1：S2→S3 断链 —「生成失控 + 门禁缺位 + 库存积压」三重叠加

dry-run 启动告警（DB 实况，非推测）：

- **354 个活跃波、20,901 条表达式无任何 gate_results 记录**。Top：JPN `s2_analyst_revision_horizons_d1` 7,564 条、JPN `mmp_nlp_sentiment` 2,514 条、ASI `intraday_pv_feats` 2,089 条——单波 7,564 条即「同骨架换字段」失控渲染（`WQB_GEM_MAX_PER_SKELETON` 封顶 12/骨架是 09-19 才加的，历史存量未清）。
- **439 个 pending/gated 波超 7 天未动（约 4,195 条积压）**，大量 EUR 2 条/波的碎波。
- 漏斗佐证：USA unconsumed 35.5%、IND 70.7%、KOR 78.8%——**七槽回测吞吐远低于生成速度**，且 IND/USA 的 `conversion`（已回测/已生成）分别仅 28%/10% 量级，属于「管道问题」而非「标的问题」。

### 瓶颈 2：736 条过硬闸候选从未测 prod — 最大的零成本机会

`sharpe>1.58 & fitness>1.0 & (ra_failed_checks 为空或未挂)` 且 prod 未测：

| 区域 | 过硬闸未测 prod | 已测 prod 撞墙率(≥0.7) | near-miss 池 |
|---|---|---|---|
| DEU | 267 | 42/48 = 88% | 156 |
| GLB | 150 | 2/8 = 25% | 86 |
| ASI | 120 | 0/4 = 0% | 78 |
| IND | 107 | 98/148 = 66% | 65 |
| MEA | 31 | 57/80 = 71% | 117 |
| USA | 31 | 11/24 = 46% | 87 |
| EUR | 20 | 7/12 = 58% | 17 |
| KOR | 10 | 2/10 = 20% | 53 |

另：真·干净过硬闸（`ra_failed_checks` 为空）：DEU 161 / GLB 146 / IND 114 / MEA 95 / EUR 16 / KOR 11。

**这批库存是 2026-09-07「清库存 20 条 vs 新挖 170 回测 0 条」教训的同型机会，且规模更大。**

### 瓶颈 3：risk_neutralized_sharpe 采集覆盖近乎为零 — RN_EXPOSURE 硬规则在主战场裸奔

| 区域 | backtest 行 | 有 rn_sharpe |
|---|---|---|
| DEU / USA / IND / MEA / EUR | 1402/965/782/498/435 | **0** |
| ASI | 488 | 341 |
| GBR | 432 | 66 |

SOP 的风险中性化硬规则（`rn_sharpe≤0 且 sharpe≥1.58 ⇒ 直接记 dead_end 禁止调参`）在 DEU/IND 等 5 个信号最强区域**无法执行**。HKG w4 式的「整批都是因子暴露裸信号」在这些区可能正被当真信号反复打磨。

### 瓶颈 4：DEU 达标 315 条中 154 条挂在非 prod 闸

- `IS_LADDER_SHARPE` 133 条（子期表现不一致，方向明确可修）
- `CONCENTRATED_WEIGHT` 21 条（权重集中，bucket/分组可修）
- 但 DEU 已测 prod 撞墙率 88% —— **先修闸再测 prod 会浪费工时，顺序应当反转**。

## 三、优化方案

### P0 · 立即执行（零/低配额，预期 1-3 个工作日出可提交）

**P0-1 库存收割流水线（对应瓶颈 2）**

按「已测 prod 撞墙率」排优先级，从低到高：

1. `python tools/build_gate_prior_from_inventory.py --regions GLB,ASI,KOR,USA --emit-candidates cache/candidates.json --write-priors`
2. `python tools/select_ra_basket.py cache/candidates.json --target 20 --out cache/basket.json`（去参数网格 + OS 撞车预筛 + 篮内正交）
3. 篮内逐条 `submit_verdict`（模拟层 checks + `/alphas/{id}/submit` 双视图）；READY 且 prod<0.7 → **当天请用户确认提交**（09-19 血教训：IND pv103 因先做变体被外部抢注，prod 1.0000 整族封死）。
4. prod 队列恒 1 在飞、等待期插本地活（`compute_mutual_correlation` 不占配额）。

预期：GLB 150 + ASI 120 + KOR 10 + USA 31 按撞墙率折算理论可提交 15-30 条量级；即使对折也是当前 submit_ready=0 的直接破零。

#### P0-1 执行结果（2026-09-23/24 已完成，GLB/ASI 部分）

- **枚举**：`--regions GLB,ASI`，每区 1000 条（平台上限）。GLB 309 过闸（30.9%）/ ASI 19（1.9%）→ 候选池 328 条（`cache/candidates_glb_asi.json`）。
- **篮选**：`select_ra_basket --target 20` → 296 颗互相关去冗余（188 对 ≥0.7）+ OS 撞车预筛剔 17/55 → **19 颗正交篮**（两两 <0.7，覆盖 11 金字塔）。
- **判定链**：Phase1 双视图 19/19 UNVERIFIABLE（处女提交 404 盲区，模拟层 0 FAIL）→ Phase2 prod+self 终验：**18 颗撞 prod 墙（0.77–1.00，含 2 颗 1.0 整族复刻）、1 颗 READY**。
- **提交**：**GLB/O0NoPARJ 用户确认后提交成功**（POST 201 → ACTIVE/OS；MINVOL1M+SUBINDUSTRY+decay10；S 2.31 / F 1.35 / prod 0.6193 / self 0.6199）。win 已回写 `registry_empirical`（id=1348）。
- **实证修正预期**：GLB 主流集（TOPDIV3000/MINVOL1M）真实 prod 撞墙率 18/19（95%），**远超历史库存口径的 25%**——篮子顶层候选几乎全是拥挤信号。P2-1 中「GLB 加大投入」需要限定为「冷门字段 + 未点亮塔」，台账已写 `ledger_kv GLB/submit_ready_blocked_p0_1_20260923` 供 S0 降优先级消费。
- **附带发现并已修复**：`batch_submit_verdict.py --phase2-prod` 三处假阴性 bug（self 读 `all_passed` 而非 `passes_check`、prod max 未从 `checks["production"]` 取、未决 `all_passed=None` 被误判 FAIL）——已修复并补 7 条单测（`tests/unit/test_batch_submit_verdict_phase2.py`），全量回归 1356 绿。
- **剩余动作**：KOR/USA 候选池尚未枚举（`--regions KOR,USA`），预期撞墙率 20%/46%，是下一批收割目标。

**P0-2 积压裁决（对应瓶颈 1）**

- 439 个 >7 天 pending/gated 波：逐波二选一——补跑 `python tools/wave_gate.py --wave <wave>`，或标 `status='dropped'`（勿留死库存）。EUR 2 条/波的碎波建议直接 dropped。
- JPN `analyst_revision_horizons` 7,564 条等失控波：**不补门禁、不回测**，按同骨架封顶规则抽样 12 条/骨架后其余 dropped——历史数据已证明该族无 yield。
- **进度（2026-09-24 复测，未开始裁决）**：dry-run 启动告警已增长至 **365 个活跃波（23,460 条表达式）无 gate_results、447 个波积压超 7 天（约 4,842 条）**——较 09-23 的 354 波/20,901 条与 439 波/4,195 条**继续恶化**，裁决优先级应上调。

### P1 · 一周内（结构修复）

**P1-1 rn_sharpe 采集补全（瓶颈 3）**：`review_wave.py` / harvest 路径确认 `risk_neutralized_sharpe` 拉取逻辑（当前仅 ASI/GBR 部分覆盖，疑与 review 入口调用率相关），并补跑一次全库存回填。DEU 161 条干净过硬闸尤其需要先过 RN 墙再谈提交——DEU 是 IS_LADDER 与因子暴露双重高危区。

**P1-2 DEU 修复顺序反转（瓶颈 4）**：133 条 IS_LADDER_SHARPE 不先修，先对 DEU 干净过硬闸做 prod-first 族级探针（每族 1-2 条）；prod<0.7 的族内再修 IS_LADDER（Mode B：decay 拉长 / 窗口标准化的方向性修法）。

**P1-3 每波表达式预算硬顶**：在 `build_wave` / GEM 落库处加 `WQB_MAX_EXPR_PER_WAVE`（建议 200），超顶即拒绝入库。这是把「354 波 2 万条无门禁积压」这类事故机械拦住的唯一手段（AGENTS.md 失败诊断纪律第 7 条：同类漂移第二次出现就写工具拦）。

### P2 · 战略（两周内）

**P2-1 区域预算再分配**（基于严格口径 yield + prod 撞墙率双维）：

| 区域 | 动作 | 依据 |
|---|---|---|
| GLB / ASI / KOR | 加大投入 | 达标率高 + prod 撞墙率低（0-25%），ASI rn_sharpe 覆盖 70% 评审质量最好 |
| DEU | 维持但转向冷门字段（users≤9 占比 ≥50%）+ 未点亮塔 | 信号最强（315 达标）但 prod 88% 撞墙 = 拥挤；冷字段是唯一出路 |
| IND / MEA | 收缩到库存收割 | prod 66%/71% 撞墙，新挖边际收益低 |
| GBR / JPN / CHN / HKG | 停止新挖 | 0 达标（JPN 238 / GBR 432 / CHN 60 / HKG 28 回测零过硬闸） |

**P2-2 OS 期望值入排序**：`expOS = IS sharpe × 0.358`（USA 124 例实测）已有校准，建议在 `select_ra_basket` 排序权重中显式加入 expOS 与 OS 存活率（IS/OS 秩相关仅 +0.086，IS 高分不是 OS 存活的理由）。

**P2-3 prod-first 执行率监控**：步 5b 与步 7 的 prod-first 探针规则已存在（09-19 硬门），但 IND 66% 撞墙率说明「先 IS 后 prod」惯性仍在。建议把「本波是否跑过 prod-first」写进 `wave_results.key_findings`，S6 复盘漏跑即波次记 FAIL_xxx 提示。

## 四、验证与守护

- ~~本方案不改任何运行代码~~ **已按方案推进的代码变更**（截至 2026-09-24）：
  - `tools/batch_submit_verdict.py`：Phase2 字段语义修复（`_phase2_outcome` 四态判定：PROMOTE / BLOCKED_SELF / BLOCKED_PROD / PENDING），配套 `tests/unit/test_batch_submit_verdict_phase2.py` 7 条单测。
  - 其余 P0/P1 动作均用既有工具（`build_gate_prior_from_inventory` / `select_ra_basket` / `wave_gate` / `campaign_intel prod-first` / `submit_verdict`）执行，符合「MCP 应用尽用」铁律。
- P1-3 落地时需同步：registry NodeMeta（如做节点参数）+ `tests/unit/test_workflow.py` 期望集合 + `_DRY_RUN_CASES` + `Claude/skills/INDEX.md` 计数（四处同步契约）。
- 提交动作仍守步 8：`submit_verdict` READY → 用户确认 → `workflow_submit_alpha`，不入自动链（O0NoPARJ 已按此链执行）。

## 附：数据快照（2026-09-23 生成；2026-09-24 部分指标已变，见 P0-1 执行结果）

- 达标（S>1.58 & F>1.0）总量：DEU 315 / IND 228 / GLB 156 / ASI 122 / MEA 95 / USA 31 / EUR 25 / KOR 11 / 其余 0。
- 漏斗最狠一跳：USA/IND = S3 过闸→S5 就绪（0%）；KOR/EUR = S3 回测→过闸（3.7%/6.2%）。
- S6 verdict 分布：USA FAIL39/PARTIAL35/PASS2；IND FAIL72/PARTIAL65/PASS7；KOR FAIL54/PARTIAL23/PASS3；EUR FAIL133/PARTIAL35/PASS14。
- **收割后状态变化**：GLB 篮子 18 颗 PROD_WALL 候选已从 `submit_ready` 队列退役为 DEAD（原因入 note）；`alphas.prod_correlation` 回写 7 行新值（备份 `data/wqb_backup_prodcorr_20260923_192610.db`）；O0NoPARJ 提交后队列行 SUBMITTED。GLB 剩余过硬闸未测 prod 候选约 132 条（150 − 18 已验撞墙）。

---

## 五、v2 复盘（2026-09-25）：两批收割后的方案修订

### 5.1 机械层复检（2026-09-25 重跑）

| 检查项 | 结果 |
|---|---|
| `audit_node_registration.py` 四处同步 | ✅ 19/19 无漂移 |
| 全量回归 `pytest tests/` | ✅ **1411 passed**（较 09-23 的 1320 净增 91，含 Phase2 修复 7 条单测） |
| `sync_skills.py --check` 4 安装位 | ✅ 零漂移 |

### 5.2 两批收割战果与「拥挤集中」实证

| 批次 | 篮子 | VERIFIED | PROD_WALL | 撞墙率 | 状态 |
|---|---|---|---|---|---|
| 批 1 GLB/ASI（09-23） | 19 | **O0NoPARJ**（已提交 ACTIVE） | 18 | 95% | 闭环 |
| 批 2 KOR/USA（09-24） | 10（跳过 1 已知撞墙） | **KP78pLWk**（KOR/MODEL，prod 0.6334） | 6（KOR 4 + USA 2） | 6/7 = 86% | 2 颗 USA 终验进行中 |

**核心实证：历史撞墙率系统性低估篮子顶层拥挤度。** KOR 历史口径 20%（n=10）→ 篮子实测 80%；GLB 历史口径 25% → 95%。两批合计 24 验 2 过（8%）vs 方案原预期 15-30 条。机理：`select_ra_basket` 按 sharpe/fitness 择优，而高分 alpha 恰是全平台用户都能挖出的拥挤信号——**IS 高分与 prod 干净负相关**。

**已固化**：6 颗撞墙退役 DEAD（队列 note 带原因）；战果入 ledger `KOR/submit_ready_blocked_p0_1_batch2_20260924`；队列保护再次生效（A1GmYKJe 历史 DEAD/FAIL:ADD_MIX 未被复活）。

**工具改进待办（新增）**：`select_ra_basket` 应读本地 `alphas.prod_correlation` 预剔除已知撞墙者（本批 P0ZLbM1x 即漏网）；候选收割入库需补 `alphas` 行（平台库存 alpha 多数本地无行，prod 真值无处落）。

### 5.3 积压趋势（持续恶化，裁决优先级上调）

| 日期 | 无门禁活跃波 | 表达式 | 超 7 天积压波 | 积压表达式 |
|---|---|---|---|---|
| 09-23 | 354 | 20,901 | 439 | 4,195 |
| 09-24 | 365 | 23,460 | 447 | 4,842 |
| **09-25** | **374** | **25,960** | **519** | **7,338** |

三天净增 20 波 / 5,059 条无门禁表达式、80 波 / 3,143 条积压——**生成侧仍在以 >1,600 条/天的速度产生未消化库存**。P0-2 裁决与 P1-3 预算硬顶从「一周内」上调为「立即」。

### 5.4 v2 优先级（修订版）

1. **【立即】库存收割暂停扩量**：按旧筛选条件（sharpe/fitness 择优）的第三批预期撞墙率 ≈85%+，每颗消耗平台 prod 队列 1-5 分钟，边际收益为负。
2. **【立即】P0-2 积压裁决 + P1-3 每波预算硬顶**：止损信号源（374 波/25,960 条），阻止恶化。
3. **【当天】KP78pLWk（KOR/MODEL，prod 0.6334 / self 0.2382）用户确认后提交**：0.60-0.70 区间当天提交规则适用。
4. **【本周】换条件重启收割**：冷门字段（users≤9 占比 ≥50%）+ 未点亮塔 + `expOS` 排序权重；先 `prod-first` 族级探针（每族 1-2 条）再扩批。
5. **【本周】P1-1 rn_sharpe 采集补全**（RN 硬规则仍在 5 主力区裸奔）+ P1-2 DEU prod-first 反转。
6. **【持续】np8VGNz3 / VkGJ73eA 终验落定后同样处置**（PASS → 请确认提交；WALL → 退役）。
