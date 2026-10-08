# 可提交因子挖掘优化方案（资深 Quant 视角，2026-09-26）

> 前提：本方案基于对九步流水线 19 个 workflow 节点的真实 dry-run 演练 +
> `data/wqb.db` 全库勘察。目标唯一：**在平台挖出可提交（全闸通过）的因子**。
> 所有数据均为实测值，非估计。

---

## 一、诊断：为什么现在挖不出足够的可提交因子

一个因子要在 BRAIN 平台"可提交"，必须**同时**通过七道判定：

| # | 判定 | 当前系统覆盖 | 致命度 |
|---|------|-------------|--------|
| 1 | IS 硬闸：sharpe≥1.58, fitness≥1.0, turnover, margin, weight | ✅ 系统性覆盖（backtest_results） | 高 |
| 2 | **self_correlation < 0.5**（不与自有 alpha 重复） | ❌ **未入库** | 致命 |
| 3 | **prod_correlation < 0.7**（不与生产池重复） | ❌ **未入库** | 致命 |
| 4 | sub_universe_sharpe 稳健（不靠少数票） | ⚠️ 有字段未全测 | 高 |
| 5 | two_year_sharpe（近两年不衰减） | ⚠️ 有字段未全测 | 中 |
| 6 | risk_neutralized_sharpe > 0（非纯因子暴露） | ⚠️ 有字段未全测 | 高 |
| 7 | OS 表现（提交后真实表现不衰减） | ❌ 无回流 | 中 |

**核心病灶**：系统只把第 1 道硬闸做成了流水线，第 2/3 道"相关性双墙"完全没入库，
第 7 道无回流。这导致**候选池虚胖**——1050 条 IS 过硬闸的候选，其中相当比例
（按 EUR/ASI 库存全撞 prod 墙的先验）是废品。`get_salvage_pool` / `submit_ready`
台账里躺着的"可提交"，多数卡在相关性墙上。

---

## 二、实测证据

### 2.1 转化率灾难（S2→S3 断链量化）

| 区域 | 积压 | 已回测 | 总计 | 转化率 | IS过硬闸 | 历史过闸率 |
|------|------|--------|------|--------|---------|-----------|
| GBR | 7,518 | 102 | 8,529 | 1.2% | 21 | 4.0% |
| ASI | 4,169 | 19 | 4,476 | 0.4% | 145 | 25.0% |
| EUR | 3,862 | 52 | 12,752 | 0.4% | 27 | 4.7% |
| GLB | 3,486 | 0 | 8,263 | 0.0% | 161 | 7.6% |
| IND | 1,017 | 160 | 2,748 | 5.8% | 231 | **29.5%** |
| JPN | 848 | 8 | 14,374 | 0.1% | 0 | **0%** |
| DEU | 362 | 173 | 2,271 | 7.6% | 319 | 22.8% |
| MEA | 244 | 322 | 657 | **49.0%** | 99 | 19.9% |

**读法**：
- **产出率**（IS过硬闸/已回测）= 标的质量，低则换区/换集。
- **转化率**（已回测/总生成）= 流水线效率，低则先消化积压。
- IND 产出率 29.5% 但转化率仅 5.8%，475 条 selected+gated 积压是最该优先回测的资产。
- JPN 产出率 0%（max_sharpe 仅 1.24）却生成 14,374 条——**纯浪费，应冻结**。

### 2.2 潜在可提交池 vs 真实可提交池

IS 过硬闸共约 1,050 条（DEU 319 / IND 231 / GLB 161 / ASI 145 / MEA 99 /
USA 34 / EUR 27 / GBR 21 / KOR 13）。**但其中多少能过 prod_corr<0.7 未知**——
`backtest_results` 无此列。历史先验（EUR 47/47、ASI 19/19 全 prod≥0.70）
警示：这 1050 条可能大部分是废品，真实可提交数需体检才能定。

### 2.3 可疑高 sharpe 信号（指标虚高陷阱）

| 区域 | 数据集 | n | avg_sharpe | avg_fitness | 风险判定 |
|------|--------|---|-----------|------------|---------|
| IND | intraday_pv_feats | 15 | 4.89 | 3.31 | too-good-to-true，需 look-ahead/OS 校验 |
| GLB | dl_riskfree_returns | 8 | 4.16 | 2.95 | **伪 alpha**：无风险利率信号，sharpe 虚高 |
| IND | pv103 | 4 | 4.03 | 2.67 | 需稳健性复核 |

`dl_riskfree_returns`（无风险收益率）做信号本质是做多/做空无风险利率——
Sharpe 再高也不是 alpha，prod_corr 必爆，属"指标虚高陷阱"。

### 2.4 工程缺陷

- **假自动化节点**（dry-run 0.000s 空壳，不构建任何命令）：
  `field_understanding` / `auto_review` / `auto_pyramid` / `alpha_booster` / `modeb_improve`。
  违反仓库 dry-run 契约（应"走完零成本前置→构建出命令→到此为止"）。
- **门禁断链**：17 个活跃波（105 条表达式）无 `gate_results`，绕过门禁
  （GLB probe_glb_w1~w5 各 8 条）。
- **提交未回填指标**：`submission_ledger` 的 sharpe/fitness 全 None，
  无法回溯提交质量、无法校准 IS→OS 衰减。
- **hypothesis_round 缺假设目录**：`data/hypothesis_catalog/<ds>_hypotheses.json` 不存在。

---

## 三、优化方案（按 ROI 排序）

### P0 — 把虚胖候选池变成真可提交池（最高 ROI，直接产出）

**P0.1 相关性双墙批量体检**（新增 `corr_screen` workflow 节点 / MCP 工具）
- 对 1,050 条 IS 过硬闸候选，批量跑 `check_self_correlation` + `check_correlation(production)`。
- 结果**入库**：`backtest_results` 加 `self_corr` / `prod_corr` / `corr_checked_at` 列，
  或新建 `correlation_results` 表（`alpha_id` 为主键）。
- 产出"真可提交子集"（双墙全过）→ 直接送 `submit_verdict` 终验。
- 预期：把 1050 虚胖候选收敛到真实可提交集，这是**唯一能把 IS 硬闸池变成提交池的动作**。
- 注意：`get_alpha_corr_metrics` 已有 `corr_age_hours/corr_stale`（>48h 判 stale），
  stale 值只作排序参考，**提交前必须 `check_correlation(refresh=True)` 当日终验当日提交**。

**P0.2 消化积压优先于生成**（改 backlog_gate 语义）
- 当前 backlog_gate 拦 S3 开新波是对的，但应**同时给出消化路径**：
  IND 475 / EUR 347 / GBR 224 / GLB 186 / ASI 87 / USA 65 / DEU 58 条
  selected+gated 积压，按区域产出率加权排批回测。
- IND 29.5% 产出率 × 475 积压 ≈ **140 潜在过闸**——这是最快出货路径。

### P1 — 止血：堵住浪费与伪信号

**P1.1 冻结死区**
- JPN / CHN / HKG 产出率 0%（max_sharpe 1.24 / 0.78 / 1.24），JPN 已浪费 13,499 条。
- 把 `yield=0 stop_rule` 真正接到**生成侧**（现只拦 S3，GEM 仍可无限生成）。
- JPN/CHN/HKG 设 `entry_verdict: frozen`，GEM 生成前查此闸。

**P1.2 伪 alpha 字段黑名单**
- `dl_riskfree_returns` 等无风险收益/基准/beta 类字段进黑名单，生成侧拒用。
- 高 sharpe（>4）候选**强制**走 `brain-alpha-robustness`（OS/look-ahead/sub-universe）
  校验后才信任，否则视为指标虚高。

### P2 — 系统性质量：修工程缺陷

**P2.1 修假自动化节点**：5 个空壳节点二选一——
  (a) 接真实 toolkit 脚本（复用 `score_datasets/scan_fields/gate.py/review_wave.py`）；
  (b) 删除。**禁止假 dry-run**（不构建命令却报 success）。

**P2.2 补相关性入库**：见 P0.1。同时回填 `submission_ledger.sharpe/fitness`。

**P2.3 补门禁断链**：105 条无 gate_results 的表达式，跑 `tools/wave_gate.py --wave <w>`
  补门禁，或标 dropped。

### P3 — 度量对齐（修正已建的"质量效能增益"体系）

⚠️ **重要**：当前 `step_quality/efficiency/gain_metrics` 5 张表**根本不在真实
`data/wqb.db` 中**（实测 `no such table`），且其指标（accuracy/duration/token_count/
avoided_backtests）与"可提交"几乎无关。建议：

1. 先跑 `python tools/migrate_step_metrics.py` 建表（如仍要这套度量）。
2. **重定义指标**对齐"可提交"目标：
   - 质量：`yield_rate`（IS过硬闸率）、`prod_corr_pass_rate`、`self_corr_pass_rate`、
     `sub_universe_pass_rate`、`risk_neutral_pass_rate`
   - 效能：`backtests_per_pass`（每过闸消耗的回测数，越低越好）、`conversion_rate`
   - 增益：`submit_ready_count`（真可提交数）、`os_decay_ratio`（IS→OS 衰减）、
     `submission_success_rate`
3. ROI / net_gain 公式改为基于"真可提交数 / 回测配额消耗"。

---

## 四、落地清单（具体改法）

| 优先级 | 动作 | 涉及文件 | 预期产出 |
|--------|------|---------|---------|
| P0.1 | 新增 `corr_screen` 节点批量跑双墙入库 | `src/wqb/workflow/nodes/corr_screen.py` + `wqb_db_mcp.py` + `registry.py` | 1050 虚胖→真可提交集 | <!-- lint:counterexample: 本表 P0.1 是**待实施项**：corr_screen 节点尚未创建，此处引用的是拟新增的目标路径 -->
| P0.2 | backlog_gate 输出消化排批计划 | `src/wqb/workflow/nodes/campaign.py` `_run_backlog_gate` | IND ~140 潜在过闸 |
| P1.1 | yield=0 闸接生成侧 | `gem.py` / `gem_wave.py` 前置查询 | 阻断 JPN/CHN/HKG 浪费 |
| P1.2 | 伪 alpha 字段黑名单 | `src/wqb/config.py` + GEM 生成约束 | 剔除 riskfree/beta 陷阱 |
| P2.1 | 修/删 5 个假自动化节点 | `src/wqb/workflow/nodes/{field_understanding,auto_review,auto_pyramid,alpha_booster,modeb_improve}.py` | 真自动化或删冗余 |
| P2.2 | 相关性入库 + 提交回填 | `backtest_results` schema / `submission_ledger` | 可回溯提交质量 |
| P2.3 | 补门禁断链 105 条 | `tools/wave_gate.py --wave` | 堵住门禁旁路 |
| P3 | 重定义质量效能增益指标 | `tools/{step_metrics_collector,wave_summary_computer}.py` | 度量对齐可提交目标 |

---

## 五、预期效果

- **P0 落地后**：从 1050 条虚胖候选中筛出真实可提交子集（按 prod 墙先验估计 5%-20%，
  即 50-200 条），并从 IND/DEU 积压再产出 ~140+ 潜在过闸。**这是最快出货路径**。
- **P1 落地后**：止住 JPN/CHN/HKG 的持续浪费，剔除伪 alpha 陷阱。
- **P2/P3 落地后**：流水线从"生成导向"转为"可提交导向"，度量真实反映产出。

**一句话结论**：当前系统"会生成"但不会"筛出可提交"。最高 ROI 的单一动作是
**P0.1 相关性双墙批量体检**——它把虚胖的 IS 硬闸池第一次变成真实的提交池。
