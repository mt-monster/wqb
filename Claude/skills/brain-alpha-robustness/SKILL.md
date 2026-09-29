---
name: brain-alpha-robustness
description: "提交前稳健性验证：汇集论坛实证的归因与反过拟合技术，跨年度与子宇宙做 PnL 归因分析，拒绝高 Sharpe 来自噪声拟合、股票集中或单年行情的候选。当任务涉及提交前验证、OS 表现不佳的事后复盘，或用户提到过拟合/稳健性/子宇宙/逐年统计/PnL 归因/衰减比/参数稳定性时使用。"
last_verified: 2026-09-29
layer: L4
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
  - mcp__wqb-db__*
---

# BRAIN Alpha 稳健性（Robustness）

## 职责边界

- **本 skill 负责**：反过拟合 / 稳健性闸：跨年度、子宇宙、逐年 PnL 归因，拒绝「高 Sharpe 来自噪声拟合 / 股票集中 / 单年行情」（S4→S5，**REJECT 由代码执行**：结论落台账 `robustness_<alpha_id>`，`submit_verdict` 读到 REJECT 即 BLOCKED，见下「结论去哪」）
- **本 skill 不做**：不做提交判定（`submit_verdict`）、**不编辑候选使其过闸**（→ `brain-alpha-repair` / `wq-brain-alpha-optimization-v1`）、**不做论坛知识刷新**（那是独立任务，见 Phase A）
- **上游 / 下游**：上游 = S4 达标候选（`brain-explain-alphas` 归因之后）；下游 = `submit_verdict` → prod 实测 → 用户确认；`brain-alpha-judge` 只是**可选参考评审**，不是「唯一提交评审入口」（旧文这样写，与 judge 自己的定位矛盾，已删）

与 `brain-alpha-repair` 的区别：repair 编辑候选使其可过闸；本 skill 依据稳健性与归因证据**诊断**该候选**是否应该**提交。通过相关性预检（`get_alpha_details` 的 `is.checks` + `check_correlation`；**不存在 `get_submission_check` 这个 MCP 工具**）的 alpha 仍可能过拟合在单一年份或 5 只股票上——这正是本 skill 要抓住的情形。

## 结论去哪（RB-03：从「文件态」到台账）

Phase C 的三态判定**必须**写进台账，这样 `submit_verdict` 才读得到：

```
mcp__wqb-db__upsert_ledger_key(region=<alpha 的区域>, key="robustness_<alpha_id>",
    value={"alpha_id": "<id>", "verdict": "PASS|CONDITIONAL|REJECT", "failed_checks": ["…"],
           "soft_flags": ["…"], "checked_at": "<ISO 时间>", "report_path": "tracking/<日期>_robustness.md"})
```

读取方 = `wqb.robustness_record` → `submit_verdict`（CLI / MCP / 批量共用，`src/wqb/submit_verdict_core.py`）：

| 台账里的 verdict | `submit_verdict` 的反应 |
|---|---|
| `REJECT` | **BLOCKED**（`reason_code: ROBUSTNESS_REJECT`，`failed_checks` 进原因）——fail closed |
| `CONDITIONAL` | 不改判；`next_step` 提示「先 repair 并重审（≤ 2 轮）再请用户确认」 |
| `PASS` | 不改判、不加提示 |
| 无记录 | 不改判；`next_step` 提示「稳健性结论未落台账，未跑则先跑」——**fail open**（旧候选与非 RA 链候选不被一刀切挡死；要强制就在 RA 步 8 的清单里把它当必查项） |

同一 alpha 重审后以最新记录为准（覆盖写）。markdown 报告（`report_path`）只给人读，**不是事实源**。

## 工作流

### Phase A — 知识来源（闸门只读 `references/techniques.md`；刷新是独立任务）

旧版把「论坛知识刷新」塞进**每个候选**的闸门流程，并允许「刷新发现新规则则以新规则为准」——闸门阈值可被当日论坛内容改写，同一候选在不同日期可得不同判定，不可复现、无审批（RB-04 / RB-05）。现在拆开：

- **闸门只读** [`references/techniques.md`](references/techniques.md)（2026-04-22 论坛共识台账，每条锚定作者 / 赞数）与本文 Phase C 的表。**Phase C 的阈值不因当日论坛内容改变。**
- **刷新是独立任务**（定时或手动，不在候选流程里）：
  - `$WQ_PY tools/forum_cache_builder.py --status`（缓存 `data/forum_cache.json`，7 天 TTL；路径在仓库内，不再写死某个宿主的安装位）；过期用 `--ensure` / `--plan`（输出 MCP 拉取计划：5 个关键词包、去重、每包留最高赞）。
  - 问题驱动的单点检索用 `tools/forum_recon.py`（统一入口）。
  - **论坛新发现只作「提案」**：追加到 `references/techniques.md` 的「E · 提案区」（带日期 / 来源 / 赞数），经人审后才移入 A–D 并进入 Phase C。认证由服务端完成，失败即停并请用户处理（**不要**在 skill 里走 `authenticate` 要邮箱口令）。

### Phase B — 归因分析（逐候选）

对每个进入提交评审的候选，先产出归因报告再跑反过拟合闸；报告引用具体 MCP 工具输出，不是散文摘要。

**B.0　WebDataScope failed-count 门（硬前置）**：先从 `get_alpha_details` 取 `is.checks`，按 [`webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md) 算 Failed RA / Failed PPA。

| Failed | 名单内 `PENDING` | 处置 |
|---|---|---|
| > 0 | 任意 | **REJECT**（无 CONDITIONAL 通道），**不跑 B / C、不跑 `check_correlation`、不设属性**；逐条枚举 counted item 的 `name` / `result` / `limit` / `value`。REJECT 的含义是「本轮不合格」——按 RA 步 7 转 `brain-alpha-repair` 修复后**重新入闸**，不是永久判死 |
| = 0 | = 0 | 继续 B.0a |
| = 0 | > 0 | **暂无失败，待复查**：等其算完（重取 `get_alpha_details`）再判；**不据此 REJECT，也不据此 PASS** |

满足用户临时给的类型化指标（如 `sharpe > 1.58, fitness > 1, 2Y > 1.6`）但 Failed 非零的候选**不是**合格者，不向用户推荐。

**B.0a　体检硬门前置确认**：表达式应已在 RA 步 5（`tools/wave_gate.py`）或 repair 第 2c 步过体检硬门。来自修复路径而未过者在此补跑：`$WQ_PY tools/field_inspect_gate.py --region <R> --dataset <DS> --exprs-file <txt>`（体检包路径 `tracking/mining/field_inspect_<region 小写>_<dataset>.json`，按**数据集**分包；旧文写的 `tracking/field_inspect_<region>.json` 已过期）；违规 → 直接 REJECT 回 repair。预处理不达标的表达式即使 IS 好看，样本外也会因 CONCENTRATED_WEIGHT、极值未抑制而退化。

**B.1–B.5　归因**

1. `get_alpha_details(alpha_id)`：规范表达式、region / universe / neutralization / decay、顶层指标；确认在 IS（未提交）。
2. `get_alpha_yearly_stats(alpha_id)`：逐年 Sharpe / returns / drawdown / fitness。**近窗制度**（用户指令 2026-06-20；理由：要求 10 年全强过严，会杀死活信号）——按**最近 3 个 IS 年**判稳健性：
   - **Recent-3yr 强度（主判定）**：最近 3 个 IS 年的 Sharpe（≈ 平台 2Y / 3Y sharpe）≥ **用户 2Y 线**（= `PLATFORM_CHECK_LINES["low_2y_sharpe_min"]`，当前 1.58）**且**最近 3 年每年为正（`sharpe > 0.3`；`|sharpe| < 0.3` 计「平年」）。
   - **衰减比** = `last_year_sharpe / full_period_sharpe`，< 0.30 标警。**Recent-3yr CV_Sharpe** = 最近 3 个年度 Sharpe 的 std / mean，≥ 0.60 标警。全历史 CV / 厂字形 / max-min 只作信息软标记，**绝不据此 REJECT**。
3. `get_alpha_pnl(alpha_id)`：回撤日历（任一季 `drawdown > 2 × 全期平均` 标警）；换手 × margin（换手 > 60% 且 margin < 3 bp 标警，噪声拟合，论坛 LJ46725）；Top-5 个股集中度（逐股 PnL 可得时；≥ 50% 标警）。
4. `check_correlation(alpha_id)`：prod / self 相关性（在这里复记使报告自含）。取数规则见下「prod 相关性怎么取」。
5. `performance_comparison(alpha_id)`：相对池贡献；边际贡献为负是软标记，写进报告交用户终审。

### Phase C — 反过拟合闸（归因之后、提交之前）

按序执行；单个硬标记 → REJECT。年度行只在**最近 3 个 IS 年**上计算。

| 检查项 | PASS | CONDITIONAL | REJECT |
|---|---|---|---|
| WebDataScope failed count | Failed = 0 且无 PENDING | 名单内有 PENDING（待复查，不判） | Failed > 0（硬 REJECT） |
| **Recent-3yr Sharpe（主判定）** | ≥ 用户 2Y 线且近 3 年每年为正 | 某近年在 0–0.3 | 某近年 < 0 或 3 年合计 < 线 |
| Recent-3yr CV_Sharpe | < 0.40 | 0.40–0.60 | ≥ 0.60 |
| 衰减比 | ≥ 0.50 | 0.30–0.50 | < 0.30 |
| 平年（仅最近 3 年） | 0 | 1 | ≥ 2 |
| Recent-3yr max/min Sharpe 比 | ≤ 3 | 3–5 | > 5 |
| 全历史早年疲软（CV / 厂字形 / max-min） | — | 记软标记 | **绝不** REJECT |
| Sub-universe | 平台检查 `LOW_SUB_UNIVERSE_SHARPE` = PASS | 检查 WARNING / 贴线 | FAIL |
| 算子数 | 仅**软标记**：> 5 提示过拟合风险；**PPA** 另有硬上限 ≤ 8（Power Pool 规则，文档记载、未复核平台） | — | REGULAR 不因算子数 REJECT |
| Margin @ turnover | ≥ 5 bp | 3–5 bp @ 40%+ TVR | < 3 bp @ > 60% TVR |
| Top-5 个股集中度 | < 30% | 30–50% | ≥ 50% |
| 经济可解释性 | 一句话可写（例：「分析师上调预期修正，市场反应不足」） | 需 2+ 句 | 说不出信号方向（例：`rank(field)` 换窗口换出来的） |

对旧表的更正（RB-10）：① 子宇宙不再固定「TOP1000 / 500 / 200 全部 ≥ 1.0」——平台 `LOW_SUB_UNIVERSE_SHARPE` 是**相对公式**（≥ 0.75 × √(子宇宙规模 / 全宇宙规模) × alpha Sharpe，见 [`brain-how-to-pass-alpha-test` §5](../brain-how-to-pass-alpha-test/SKILL.md)），且 KOR / IND 的全宇宙本身就 ≤ TOP600 / TOP500，固定档位不适用；② 算子数「8 = REJECT」与 GEM 样本矛盾（p90 = 12 个算子仍过平台闸）→ REGULAR 降为软标记；③ Margin 5 / 3 bp 是**论坛经验的噪声拟合线**，与研究阶段的内部严线（`GATES_INTERNAL.margin_bp_min`，10 bp）不是同一条；④ 「经济可解释性」给判例。

**PASS** → 台账 `PASS` → `submit_verdict`（只有否决权）→ prod 实测 → 用户确认。
**CONDITIONAL** → [`brain-alpha-repair`](../brain-alpha-repair/SKILL.md) 第 2 步修复轮换后重跑 Phase B；升级前最多 2 轮。
**REJECT** → 不提交；`failed_checks` 与结构性成因（范式 / 数据集 / universe）记入台账，并按 RA 步 9 判死粒度（家族 → `seal_dead_end`）沉淀。

### Phase D — 回写（永远执行）

1. **台账**：`mcp__wqb-db__upsert_ledger_key` 写 `robustness_<alpha_id>`（格式见「结论去哪」）——这是唯一被代码读取的落点。
2. **报告**：完整归因报告 + 判定追加到 `tracking/YYYY-MM-DD_robustness.md`（给人读；路径填进台账的 `report_path`）。
3. PASS 带 CONDITIONAL 软标记：把存活的软标记写进台账 `soft_flags`，并在用户确认提交前的三段式 description 里如实带上一行（`worldquant-submit-alpha` 设属性时），用户一年后复盘 OS 表现时有可读审计痕迹。
4. 旧版还要求发 `alpha.robustness_audit` 事件（`wqb.memory.events.emit`）、REJECT 时调 `wqb.search.failure_memory.record(...)`（需要写 Python，且要私有函数 `validator._shape_signature`）。**这两条已移出必做项**：两个模块全仓库**没有任何消费方**（只写 `data/events/*.jsonl` 与 `tracking/mining/failure_memory.jsonl`），DB 单轨里没有落点；需要时的入口在 `src/wqb/memory/events.py` / `src/wqb/search/failure_memory.py`。

### Phase E — PPA 提交规则

候选通过审计、进入提交环节前，快速否决用（细则与配额语义的唯一叙述在 [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md)「PPA 通道」与 [`ppa-vs-ra.md`](../wq-brain-ra-pipeline/references/ppa-vs-ra.md)）：

1. **PPA 提交路径**：MCP `workflow_submit_alpha` 非 PPA 感知（内置 REGULAR 预检照拦合法但指标较低的 PPA，打标签重试无效）→ 合法 PPA（Sharpe ≥ 1.0 / 算子 ≤ 8 / 字段 ≤ 3 / PPAC < 0.5，文档记载、未复核平台）**只能走平台 web UI**，且仅在当期 Power Pool 主题窗口内；agent 停下交接（`ppa-handoff.md`）。
2. **RA 常规提交**不受主题限制，但达标 alpha 可能无 RA 通道可选（平台强制走 PPA 通道）。
3. **PPA 描述三段是硬性要求**（Idea / Rationale for data used / Rationale for operators used）。「`set_alpha_properties` 预置描述 + tags `PowerPoolSelected` + color」用于**记账与识别**；在 web UI 流程里标签是否仍被平台要求**未复核**。**颜色不是 GREEN**：PPA 通道专用色是 `PURPLE`（`alpha_properties.COLOR_PPA`），GREEN 须由 OS 结果挣得。
4. **幽灵提交识别**：台账记 ACTIVE 但平台 `GET /alphas/{id}` 返回 404 → 从未真正落地（静默丢弃）。**不要**把 `alphas.status` 写成 `PHANTOM`（不是代码里的状态；且 2026-09-28 起 `alphas` 的合并写入对 `ACTIVE` / `SUBMITTED` / `DECOMMISSIONED` **不回退**，这样写会被静默忽略）——改为在核对报告 / `key_findings` 里留痕并知会用户（不新造台账键）；这属于提交后核对，归 `wq-backtest-monitor` / `worldquant-submit-alpha`，不属于稳健性闸。已实证案例：`pwKvRLqg`。
5. **~~提交探测协议~~（已删除）**：旧版写「选 5 个最大化多样样本，逐个提交 + 轮询 `/check` 读 prodCorr，5 个全 FAIL 则整族不可提交」——**提交即真实动作**，通过就是 ACTIVE、不可撤销（与 RA 的「确认前禁止一切真提交」冲突；同源于 prod-corr-avoidance 旧版的 POST 探针，X-9 / T0-2）。prod 一律用 `check_correlation`（只读）+ 决策表 D0-P。

## prod 相关性怎么取（RB-17：从验证清单提到正文）

- `check_correlation(alpha_id)`（MCP）是**阻塞轮询**：内置 `prod_corr_poll_s`（30 s）轮询、最长 `prod_corr_timeout_s`（3600 s），账号级单并发（忙时立即返回 `correlation_busy`）；已决结果缓存 7 天（`from_cache: true`），提交前终验用 `refresh=True`。Redis **只是可选缓存**（无 Redis 功能不受影响，相关性锁回落为进程内 fail-fast 锁）；「等死」的原因是 30 s × 120 次的阻塞轮询与账号级单并发，不是 Redis。
- 想直接看平台值：`GET /alphas/{id}/correlations/prod` 恒秒回 200，**空体 = 平台仍在算**，非空返回 `{records, max, min}`，**`max` 才是判定值**；不要高频 `refresh=true`（会加长平台队列）。合规入口：`python tools/campaign_intel.py prod-first`（串行、进程锁、单条硬超时；见 [`prod-corr-avoidance.md`](../wq-brain-ra-pipeline/references/prod-corr-avoidance.md)）。任一返回空时重试一次后向用户报错——**不得编造数字**。

## 设计边界

- 判定阈值是 **2026-04-22 的论坛共识**（作者归属见 `references/techniques.md`），刻意保守。**放宽的入口 = 用户明确指令**（留痕：写 `robustness_<alpha_id>.soft_flags` 并在报告里注明「按用户指令放宽某项」）；skill 本身没有「参数」机制，旧文写的「可通过 skill 参数放宽」并不存在。
- Phase B 的检查刻意廉价（全部单次 MCP 调用），使 skill 可在每个候选上运行而不爆预算；更重的逐股归因在 `get_alpha_pnl` 开始返回逐股分解前是可选的。
- 本 skill 无破坏性：绝不修改候选表达式；robustness 诊断、repair 修复、robustness 复审自然串联。

## 验证清单

1. `$WQ_PY tools/forum_cache_builder.py --status` 能读到缓存状态（这是知识刷新的自检，不是候选闸门的前置）。
2. 对样本 alpha 端到端跑 Phase B，确认 `get_alpha_details` / `get_alpha_yearly_stats` / `get_alpha_pnl` / `check_correlation` 返回非空载荷；取相关性的注意事项见上节。
3. 判定后 `mcp__wqb-db__get_ledger_key(region, "robustness_<alpha_id>")` 读得回同一 verdict；对 REJECT 的候选跑 `python tools/submit_verdict.py --alpha-id <ID>` 应得 `BLOCKED`（`ROBUSTNESS_REJECT`）。
4. Phase E 的 PPA 规则在候选通过审计后被读取消费。
