---
last_verified: 2026-09-29
name: brain-next-move-analysis
description: "日报 / 早报 / 状态检查 / 「哪个区更值得挖」「该不该转区」「下一步做什么」时使用：只读汇总平台公告、比赛、事件、多样性分数、alpha 表现（IS/OS）、金字塔缺口与区域态势，按固定模板给出建议。只报告不决策：不选区、不出白名单、不回测、不提交。"
layer: L0
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
  - mcp__wqb-db__*
---

# BRAIN 日报与下一步分析

## 职责边界

- **本 skill 负责**：只读汇总并**报告**——① 平台公告 / 排行榜 / 多样性分数 / 比赛 / 事件；② alpha 表现（OS 已提交 + IS 库存）；③ 金字塔缺口；④ 区域态势（**转述** `tools/region_status.py` 的输出，不自己算）；⑤ 按 §3 的固定模板写出**建议**（建议 ≠ 执行，执行归各自的 skill）。
- **本 skill 不做**：不做选区 / 转区**决策**（决策方 = `wqb.region_rotation`，经 `python tools/region_status.py --rotate` 或 MCP `region_rotation` 取结论；战役配置包归 `wq-brain-campaign-matrix`）；不产出战役白名单、不选字段（S0 = ra-pipeline 步 2 / 决策表 D4）；不回测、不提交、不写 DB / 台账。
- **上游 / 下游**：上游 = 平台（`mcp__wq-brain-http__*`）+ 本地 DB（`tools/region_status.py`、`mcp__wqb-db__*`）；下游 = 用户，以及 ra-pipeline 的两处「转区」出口（步 1 无可挖 / 停止规则命中）和每个 ET 日开工前的一次日报。**它是情报出口，不是流水线前置**：日报失败或跳过，任何一步都不受阻。层名 = L0（并行情报层）。

## 1. 先定时间口径

- 「今天」= 系统日期；提交配额 / 事件过滤 / 「当季」都按**美东（ET）日历日**，用 `wqb.timeutil`（含夏令时，冬夏令时的 GMT+8 换算不同，不要心算）：

```powershell
& $WQ_PY -c "import sys; sys.path.insert(0,'src'); from wqb.timeutil import et_now; print(et_now().isoformat())"   # 在仓库根运行
```

- 日报头写明「取数时间（ET）」。**没有 `get_ny_time.py`**（历史文档提到过的脚本从未存在）。

## 2. 取数（章节 → 工具 → 关键点）

大纲只有这一份；`reference.md` 只写各章怎么取数、字段怎么读。取数互不依赖，可并行。任一章失败只标「本章数据不可用：<原因>」，其余照出。

| 章节 | 取数 | 关键点 |
|---|---|---|
| 0 执行摘要 | —（写在最后） | 3–5 条：关键洞察 / 机会 / 风险，每条带数字与来源 |
| 1 平台公告 | `get_messages(limit=30, offset=0)` | 与 ra-pipeline 同一 `limit`；只摘与挖矿、提交规则、比赛、算子 / 数据更新相关的项 |
| 2 排行榜与多样性 | `get_leaderboard(user_id=…)`；`value_factor_trendScore(start_date, end_date)` | 两个日期必填：起 = 本季度首日 `T00:00:00Z`、止 = 今天 `T23:59:59Z`；**只比较同一区间的前后两次读数**（后一次低于前一次 → 下一波 S0 改攻未点亮塔，判据同 ra-pipeline 步 9，无机检阈值） |
| 3 比赛 | `get_user_competitions()` → 每个**未截止**比赛：`get_competition_details` + `get_competition_agreement` | **必须读协议**，核对 universe / delay / alpha 类型；推荐的 alpha 必须逐项符合（例：全球赛只收 GLOBAL universe，USA 区的 alpha 不算） |
| 4 事件 | `get_events()`（无参数） | 按 §1 的 ET 今日过滤掉已过去的项 |
| 5 Alpha 表现 | 见 §2.1 | |
| 6 金字塔缺口 | `get_pyramid_multipliers()` + `get_pyramid_alphas()`（默认当季） | 当季 ACTIVE ≥ 3 = 已点亮（`category_lit`）；缺口 = 未点亮塔 × 还差几颗 |
| 7 区域态势 | `python tools/region_status.py` | 见 §4 |
| 8 建议 | 见 §3 | |

### 2.1 Alpha 表现的取数范围（不要在 3 万条 IS 库存里随手取 30 条）

| 池 | 范围 | 取法 |
|---|---|---|
| OS（已提交） | 全量（通常 < 数百条）；分析对象 = 自上次日报以来新提交的 + 掉出 ACTIVE 的 | `get_user_alphas(stage="OS", order="-dateSubmitted", limit=30)`，按 `offset` 翻到用尽 |
| IS（未提交库存） | **不枚举**。只看两类：① 自上次日报以来新增；② 可提交队列 | ① `get_user_alphas(stage="IS", start_date=<上次日报日期>, order="-dateCreated", limit=30)`；② `mcp__wqb-db__get_submit_ready(region)`（读 `submit_ready` 表；存储口径见 `docs/skills_review_decisions.md` DEC-33） |
| 单颗深挖 | 只对 ①②里被点名的 alpha | `get_alpha_details` / `get_alpha_yearly_stats` / `get_alpha_pnl`；相关性 `check_correlation(alpha_id, correlation_type="production", threshold=0.7)` |

**IS / OS 的词义**（`get_user_alphas` 文档）：IS = 尚未提交的 alpha；OS = 已提交的 alpha。**不是**「正在回测」和「最近成功提交」——正在回测的仿真在 `wq-backtest-monitor` 的范围。

## 3. 建议：固定格式

每条建议一行，五列缺一不可（缺哪列就不要发这条建议）：

| 动作 | 依据（数据 + 来源工具 / 命令） | 前置检查（三项全要写结果） | 预期成本 | 何时复核 |
|---|---|---|---|---|
| 一个动词短语，如「在 KOR 开 <dataset> 战役」「转 IND」「清 EUR 提交队列」 | 引用第 2 节取到的数字，不写「感觉」 | 见下三项，每项写 是 / 否 / 未查 | 配额 / 波数 / 人工步骤 | 一个可观察的触发点，如「下一次日报」「该波收批后」 |

**前置检查（任何一项为「否」→ 建议改写为对应的替代动作，不能照发）**：

1. **点亮塔**：目标数据集所在 category 当季已点亮（ACTIVE ≥ 3）→ **不得推荐它作战役主数据集**（ra-pipeline 硬约束 0，2026-09-19 用户定案；它的字段只能当未点亮塔主信号的辅助腿）。判据取 `get_pyramid_alphas` 或 `recommend_datasets` 的 `category_lit`，**不用**「金字塔乘数高」当选塔准则。
2. **跨区弱先验**：该数据集 / 信号族在别的区是否已判死或明显偏弱（`get_cross_region_lessons` / `get_dead_datasets`；`campaign_intel.py s0-select` 输出带 `[跨区弱:…]`）。≥ 2 区独立复现的死族**不推荐**；单区偏弱只降权并注明。
3. **停波闸**：目标区的停止规则是否已命中（区级产出 A / 同轴熔断 B1 / 多轴停 B2；口径见 ra-pipeline `references/loop-and-stop.md` L.2，放行记录用 `python tools/waiver.py list --region <R>` 查）。命中 → 只能推荐「换区 / 换轴 / 等用户放行」，**不能推荐「再开一波」**。

选塔与选区**不在本 skill 决定**：建议里写的是「按 ra-pipeline 步 2 的规则，X 是候选」，由用户或流水线确认。

## 4. 区域态势（只转述，不重算）

```powershell
& $WQ_PY tools/region_status.py                      # 默认：DB 里有回测记录的区域；--json 给机器可读
& $WQ_PY tools/region_status.py --regions KOR,EUR   # 指定区域（覆盖 config.REGIONS 里没有回测记录的区，逐个点名）
& $WQ_PY tools/region_status.py --rotate --current <R>   # 转区决策（同源 wqb.region_rotation）；只读，不加 --write-ledger
```

- **区域清单** = `config.REGIONS`（现 14 个，含 DEU / JPN / AMR）；不要在文档里写死名单。DB 里没有回测记录的区不会出现在默认输出里——需要就 `--regions` 点名。
- **数字口径**：输出里的「达标」`pass_ge_158` = 本地 `backtest_results` 中 `sharpe ≥ 1.58` 的条数（**宽口径**：只看 Sharpe，不看 RA 硬闸与 prod 相关性）；ACTIVE 也是本地口径，平台全量以 `tools/sync_platform_alphas.py` 同步后的库为准。RA 选区先验用**严格口径**（`ra_clean`：RA 硬闸全过）——看产出率请用 `mcp__wqb-db__get_mining_yield(region, strict=True)`，两个口径并列写进日报，别互相替代。
- **建议动作的判据**（数值只以 `tools/region_status.py` 顶部常量为准；本表由 `tests/unit/test_se_docs.py` 钉死）：

| 建议动作（`suggested_action`） | 判据（自上而下，命中即停） |
|---|---|
| 继续（注意 PROD 同质风险→正交方向） | `pass_ge_158 ≥ 10`（`PROD_SATURATION_MIN_PASS`）；同时是 campaign-matrix `prod_saturation: likely` 的判据 |
| 冻结/转区（exhausted 占比过高） | 战役 `exhausted` 占比 ≥ 80%（`EXHAUSTED_FREEZE_PCT`）且战役总数 ≥ 5（`EXHAUSTED_MIN_CAMPAIGNS`） |
| 开战役候选（untried 充足、投入不足） | 有 `untried` 战役且回测总量 < 20（`OPEN_CAMPAIGN_MAX_BACKTESTED`） |
| 继续观察 | 以上皆不满足 |

- **`entry_verdict`**（区域 profile 的 front-matter，三态 `active` / `probe-only` / `frozen`）的默认含义与步 1 的动作只有一处定义：ra-pipeline `references/step1-inventory.md` §1.1。日报里 `frozen` 区只报状态；`probe-only` 区只推荐探针批，不推荐常规战役。**本表的「建议动作」是数据侧提示，不覆盖 `entry_verdict`**：`active` 区出现「冻结/转区」→ 写成「建议复核转区」并附 `--rotate` 的结论，而不是直接判冻结。
- 转区**结论**一律引 `--rotate` 的输出（`should_rotate` / `to_region` / `reason`）；本 skill 不复述饱和判据（在 `src/wqb/region_rotation.py`）。

**输出区域状态表**：

| region | entry_verdict | 回测 | 达标（宽口径） | ra_clean 产出率（严格） | exhausted 占比 | 建议动作（数据侧） | `--rotate` 结论 |
|---|---|---|---|---|---|---|---|

## 5. 失败与降级

| 现象 | 含义 | 处置 |
|---|---|---|
| MCP 工具「不存在」/ 连接失败 | 服务没起或没连上（不是工具没实现） | 报「平台数据不可用」并说明哪章缺；**不要**编数字补齐；需要人工重连时请用户在本机处理 |
| 认证失败 | 凭据由 MCP 服务按 `world-quant-brain-mcp/.env` 自动读取 | **不要向用户索要口令、不要读 / 打印 `.env`、不要把口令传给任何工具**；请用户在本机终端完成登录后重试 |
| `region_status.py` 报 DB 不存在 | 本地库未初始化 | 该章标「区域态势不可用」，其余照出；不要回落到手算 |
| `value_factor_trendScore` 无数据 | 该区间没有提交 | 写「本季暂无读数」，不要用 0 |
| 比赛协议读不到 | 平台或权限问题 | 不推荐任何「符合比赛」的 alpha，只标「规则未核对」 |

## 情景卡

### 情景 NM-A　用户说「早报」

- **前置状态**：无。
- **步骤**：① §1 定 ET 时间；② §2 各章并行取数；③ §4 跑 `region_status.py`；④ 按 §3 模板写建议；⑤ 最后写第 0 节摘要。
- **完成定义**：每章要么有数据与来源，要么有「不可用：原因」；每条建议五列齐全。
- **反例**：不查协议就推荐「符合比赛」的 alpha；用金字塔乘数高当理由推荐已点亮塔；把 `pass_ge_158` 当作「可提交数」。

### 情景 NM-B　用户问「哪个区更值得挖」

- **步骤**：`region_status.py` 出全表 → 对候选区各跑一次 `--rotate --current <当前区>` 取 `ranked` → 表里并列写宽口径达标与 `get_mining_yield` 严格口径 → 建议按 §3 三项前置检查。
- **完成定义**：结论引用 `--rotate` 的 `to_region` / `reason`，并写明这是数据侧建议，最终选区由用户 / ra-pipeline 确认。
- **反例**：只按 `suggested_action` 一列排序；对 `frozen` 区推荐开战役。
