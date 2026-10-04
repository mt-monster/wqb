---
last_verified: 2026-10-05
name: brain-how-to-pass-alpha-test
description: "只读地回答 WorldQuant BRAIN alpha 提交测试的问题：每个检查（18 个 RA 检查 + SELF / PROD 相关性）的线、为什么没过、往哪个方向改，并给出失败后的建议路径（不执行）。当用户询问 alpha 提交失败原因、如何提升 alpha 指标或测试要求时使用（submission tests / thresholds / improvement tips / 提交测试 / 通过测试）。"
layer: L4
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# BRAIN Alpha 提交测试：要求与改进建议

## 职责边界

- **本 skill 负责**：**只读**——回答「某项检查的线是什么、为什么没过、先往哪个方向想」，并在 FAIL 后给出**建议路径**（下文「诊断之后」）。
- **本 skill 不做**：不产生新表达式、不回测、不改候选——需要动手改 → `wq-brain-alpha-optimization-v1`（判据：**是否产生新表达式**）；**不执行**分流与判死回写（写台账 / 终止候选归 RA 步 5b / 步 9 的 `seal_dead_end` 流程）；不做提交判定（`tools/submit_verdict.py`）。
- **上游 / 下游**：上游 = 失败的候选指标（S3 `brain-sim-alphas-in-batch-and-track`；结果读 `backtest_results` 表）；下游 = `wq-brain-alpha-optimization-v1` → `brain-calculate-alpha-selfcorr-quick` →（可选）`brain-explain-alphas` → `brain-alpha-robustness` → `tools/submit_verdict.py`。

完整细节与社区背景见 [reference.md](reference.md)；每类失败的「症状 → 根因 → 动作 → 验收」情景卡见 [references/scenarios.md](references/scenarios.md)。

## 0. 检查名 → 线 → 读哪节

提交测试的真实来源是 `is.checks` 里的 **18 个 `RA_CHECK_NAMES`**（`wqb.config`；PPA 另计 7 个 `PPA_CHECK_NAMES`；计数口径见 RA [`webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md)：`result` 既不是 `PASS` 也不是 `PENDING` 即计入失败，**`WARNING` 也算**）。**数值一律以 `wqb.config` 为准，本页只写键名**：

- 平台官方线 = `config.PLATFORM_CHECK_LINES`（LOW_SHARPE / LOW_FITNESS 按 delay 分列）；
- 内部严线 = `config.GATES_INTERNAL`（研究阶段省配额的本地预筛，**比平台线严**——按平台线判「已过」会把会被内部闸拦下的候选当成已过）。

| 检查名 | 它在说什么 | 平台线（config 键） | 内部线（config 键） | 失败时读哪 |
|---|---|---|---|---|
| `LOW_SHARPE` | IS Sharpe 不够（RA 侧只认 `result`） | `PLATFORM_CHECK_LINES['low_sharpe_min']` | `GATES_INTERNAL['sharpe_min']` | §2 |
| `LOW_FITNESS` | Fitness 不够 | `PLATFORM_CHECK_LINES['low_fitness_min']` | `GATES_INTERNAL['fitness_min']` | §1 |
| `LOW_TURNOVER` / `HIGH_TURNOVER` | 换手过低 / 过高 | `PLATFORM_CHECK_LINES['turnover_range']` | `GATES_INTERNAL['turnover_range']` | §3 |
| `CONCENTRATED_WEIGHT` | 单票权重集中；**无 value / limit**，只显示 `PASS` / `WARNING` | — | — | §4 |
| `LOW_SUB_UNIVERSE_SHARPE` | 子宇宙 Sharpe 相对不足（相对公式，见 §5） | 平台相对公式 | — | §5 |
| `LOW_2Y_SHARPE` / `IS_LADDER_SHARPE` | 近两年 Sharpe（同一事实的两个读数位，`RA_2Y_NAMES`） | `PLATFORM_CHECK_LINES['low_2y_sharpe_min']` | 同左（`submit_queue.LIM['two_year']`） | [playbook](references/two-year-sharpe-playbook.md) |
| `LOW_RETURNS` | Returns 不够 | 平台线（读响应里的 value / limit） | `GATES_INTERNAL['returns_min']` | 暂无专项经验：先看 §1（Returns 是 Fitness 的分子） |
| `LOW_ROBUST_UNIVERSE_SHARPE` / `LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO` / `LOW_ROBUST_UNIVERSE_RETURNS` | 稳健宇宙下 Sharpe / Returns 相对不足 | 平台相对线（读响应） | — | 暂无专项经验：见 `brain-alpha-robustness`（子宇宙 / 稳健性）与 §5 的思路 |
| `LOW_INVESTABILITY_CONSTRAINED_SHARPE` | 可投资性约束下的 Sharpe 不足 | 平台线（读响应） | — | **压尾前查持仓对称性**（LC/SC）：`signed_power` 压尾会造成多空不对称而触发本墙；实测 `quantile` 替 `signed_power` 后多空持仓完全对称（LC319/SC319）⇒ **优先换等价的非压尾包装算子**（见 §5b），不是抬 Sharpe |
| `LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE` | 计入成本后非流动宇宙的 Sharpe 不足 | 平台线（读响应） | — | 暂无专项经验：成本敏感 → 先降换手（§3） |
| `LOW_GLB_EMEA_SHARPE` / `LOW_GLB_AMER_SHARPE` / `LOW_GLB_APAC_SHARPE` | GLB 各大区分区 Sharpe（仅 GLB） | 平台线（读响应） | — | 暂无专项经验（GLB 区域 profile 见 RA `regions/GLB.md`） |
| `LOW_ASI_JPN_SHARPE` | ASI 内日本子集 Sharpe（仅 ASI） | 平台线（读响应） | — | 暂无专项经验 |
| *`SELF_CORRELATION`*（不计入 Failed RA，另行核） | 与自己已提交 alpha 太像 | `GATES_PLATFORM['self_corr_max']` | `GATES_INTERNAL['self_corr_max']` | §6a |
| *`PROD_CORRELATION`*（同上） | 与全平台生产池太像（prod 墙） | `GATES_PLATFORM['prod_corr_max']` | — | §6b |

「暂无专项经验」是如实登记，不是漏写：这些检查在本库还没有可复用的修法；遇到时先按表里给的相邻小节思路，并把新经验回写。

## 失败点 → 修法族（速查；RA 提示词 §2.3 与 `brain-alpha-repair` 反向链接到这里）

下表只回答「先往哪个方向想」，**不产生新表达式**（动手改 → `wq-brain-alpha-optimization-v1`，先想法后参数）。

| 失败的检查 | 修法族 | 细则 |
|---|---|---|
| `LOW_SHARPE` / `LOW_FITNESS` | 信号层：换数据 / 换概念 / 换结构；不是磨参数 | §1 §2 |
| `LOW_2Y_SHARPE` / `IS_LADDER_SHARPE` | 先看逐年形态，再按 设置轴 → 表达式轴 → 机制轴 | playbook |
| `LOW_TURNOVER` / `HIGH_TURNOVER` | 平滑与窗口（`ts_decay_linear` / `ts_mean` / `decay`） | §3 |
| `CONCENTRATED_WEIGHT` | 时间平滑；低频字段先 `ts_backfill`；**中性化与参数层无效** | §4 |
| `LOW_SUB_UNIVERSE_SHARPE` | **比值闸，抬 S 无效**（门槛随 S 同比例抬高）→ 动结构：去市值乘数 / 分档 decay / 换分组轴（逐区实测）/ 长窗 | §5 |
| `SELF_CORRELATION` | 换概念 / 换数据源，不是换窗口 | §6a |
| `PROD_CORRELATION` | 只按 RA 决策表 **D0-P** 一张表处置（先做表里的「诊断前置」：单颗钉子 / 密墙 / 可破三型；同族同分母先换分母），**不盲扫参数** | §6b |

## 1. Fitness（`LOW_FITNESS`）

**要求**：至少 "Average"——线见 §0（Delay-0 与 Delay-1 不同；本库战役几乎全是 **Delay-1**，取 `settings.delay` 对应列）。

**公式**：`Fitness = Sharpe × sqrt(|Returns| / max(Turnover, 0.125))`（另一写法 `Sharpe × √(505 × margin)` 见 playbook §1，同一关系）。

**要点**：换手低于 12.5% 后**继续降换手不再抬 Fitness**（分母被 floor）。

| 数值例 | Sharpe | Returns | Turnover | Fitness | 读法 |
|---|---|---|---|---|---|
| ① floor 生效 | 1.6 | 6% | 8% | ≈ **1.11** | 与 Turnover = 12.5% 时**相同**——别再为 Fitness 降换手 |
| ② 高换手 | 1.6 | 6% | 40% | ≈ **0.62** | 其余不变 |
| ③ 降到 25% | 1.6 | 6% | 25% | ≈ **0.78** | ②→③ 把换手从 40% 降到 25% 就抬了 0.16；再往 12.5% 才到 ≈ 1.11 |

**改进**：提高 Sharpe / Returns、降低 Turnover（到 12.5% 为止）；用分组算子（如搭配 pv13）提升 fitness。检查用 `mcp__wq-brain-http__get_alpha_details`（返回 `is.checks`）。

**配额不在本 skill 职责内**：提交配额的读取归 `worldquant-submit-alpha` / `brain-next-move-analysis`。**读配额不得靠 POST submit**——通过即真提交，不可撤销；预检用 `workflow_submit_alpha(confirm_submit=False)`（默认值：本地放宽预检 + 查状态，见 [`submit-chain.md`](../worldquant-submit-alpha/references/submit-chain.md)）。

## 2. Sharpe（`LOW_SHARPE`）

**要求**：线见 §0（Delay-0 与 Delay-1 不同；取 `settings.delay` 对应列）。`Sharpe = sqrt(252) × IR`，`IR = mean(PnL) / stdev(PnL)`。

**改进**：关注低波动下的稳定 PnL；对流动性 / 非流动性股票分档做 decay（写法用 `bucket` / `group_*`，见 optimization-v1 形态库 F4）；Sharpe 为负（如 -1 到 -2）可试翻转符号 `-original_expression`。

## 3. Turnover（`LOW_TURNOVER` / `HIGH_TURNOVER`）

**要求**：区间见 §0（平台线 1%–70%；内部线更窄，别互相顶替）。

**改进**：用 `ts_decay_linear` / `ts_mean` 平滑信号；Fitness 视角下换手低于 12.5% 没有额外收益（§1）。

## 4. Weight Test（`CONCENTRATED_WEIGHT`）

**要求**：任一股票权重上限 < 10%。

**要点（一行读完）**：**中性化对本闸无效**；**有效手段是时间平滑**（`ts_mean` / `ts_decay_linear`，窗口取 5 或 22；原实验用 10，需复验）；低频字段先 `ts_backfill`；事件 / 计数类信号构造时默认加时间平滑，不要直接 rank 瞬时值。⚠ **平滑要作用在补过覆盖的原始字段上**（`ts_backfill` → 平滑 → 再构造信号）：只对**最终信号**套 `ts_decay_linear` 不修 CW——KOR shortinterest38 换手 0.298→0.14（−53%）、S 2.00→2.15，CW 仍 FAIL（CW 由组内分布集中度决定，不由换手决定；GBR starmine 族连外层 `rank()` 均匀化都 403，唯一过的同族结构是 `trade_when` 门控；方法论全文见 `docs/experience/02_signal_patterns.md` §14）。

- **本闸无法预检**：无 value / limit，IS 阶段只显示 `WARNING` / `PASS`。`WARNING` 计入 Failed RA（口径见 §0 的链接）→ Failed RA ≠ 0 就不该提交。实测 4 例里 2 例（IS 阶段 `WARNING` 者）提交后 FAIL；2 例（`PASS` 者）成功。
- **根因在表达式结构，不在参数**：瞬时离散计数 / 事件类信号 → 权重集中；同一信号加时间平滑 → PASS。合规式样：`rank(ts_mean(subtract(U30, D30), 10))`（单信号平滑，已 ACTIVE）。
- **参数层全无效（别再试）**：换 neutralization 四档仍 `WARNING`；truncation 0.08 → 0.02 / 0.01 仍 `WARNING`；末端再套 `rank(...)` 反而变 FAIL；`scale(x, 1)` 语法错。
- **适用范围**：证据只来自 **IND / TOP500 的分析师修正族**（n = 4，2 例 FAIL / 2 例 PASS），置信度低；**未验证范围**：其它区域、其它信号类型。证据表与逐例细节见 [references/concentrated-weight-evidence.md](references/concentrated-weight-evidence.md)（含已被闸 5 禁止的历史加权混合写法，**不得照抄**）。

## 5. Sub-universe（`LOW_SUB_UNIVERSE_SHARPE`）

**要求**：`Sub-universe Sharpe ≥ 0.75 × sqrt(subuniverse_size / alpha_universe_size) × alpha_sharpe`。

**数值例**：TOP3000 → 子集 TOP1000：门槛 = `0.75 × sqrt(1000 / 3000)` = 0.433 倍 alpha Sharpe；alpha Sharpe = 1.6 时子集 Sharpe 需 ≥ **0.69**。按同式，TOP500/TOP3000 类档位系数约 **0.571**；**系数随 universe 档位变，务必按本区实算，别套用别区数值**（SA 的系数另见 `wq-brain-superalpha`，与 REGULAR 不同）。

**⚠ 这是比值闸，「抬整体 Sharpe」破不了（2026-10-03 实证更正）**：
门槛 = `系数 × alpha_sharpe`，**alpha_sharpe 抬高的同时门槛按同比例抬高** ⇒
原地跑步，净效果为零。实测 D0-P：抬 S 后 SUB 仍未过。
所以**不要把"先抬 Sharpe"当修法**，那是本条曾经的方向性错误指引（已删）。

**改进方向（动结构，不是抬 S）**：
1. **去掉与市值相关的乘数**（市值/规模加权会把子集表现绑到大盘股）；
2. 分档 decay：用 `bucket` / `group_*` 表达流动性分层（optimization-v1 形态库 F4），
   **不要**把两份不同 decay 的信号按权重相加（闸 5 block）；
3. 换分组轴（`market` / `exchange`）——但 ⚠ **轴不是通用旋钮**：EUR 有效、
   KOR other466 六种轴向全灭 ⇒ **族相关，逐区实测**，别当万能钥匙；
4. 长窗平滑（`ts_rank` / `ts_decay_linear`）——⚠ 低频季度财报**不该**套日频事件型平滑
   （实测 S 1.80→1.37、F 1.38→0.93，方向为负）。

**常见报错**：`Sub-universe Sharpe NaN is not above cutoff` = 子集覆盖不足（子集里字段大面积缺失）→ 对字段 `ts_backfill` 或 `pasteurize` 后重测。

## 5b. 等价算子替换（判「无解/天花板」之前**必须**先扫）

**为什么单列一节**：`LOW_SUB_UNIVERSE_SHARPE`（§5）与 `LOW_INVESTABILITY_CONSTRAINED_SHARPE`
（§0 表）的常见"修法"都是**改结构**，而**改结构不等于换信号族**——有一类改法只换
包装算子、信号骨架全冻结，却能同时改动多个闸门。跳过这一步会把**「实现路径的约束」
误判成「结构性的约束」**，从而错杀可救的族。

**规则（2026-10-03 补入本 skill）**：**在下结论说「不可能 / 天花板 / 已到顶 / 无解」之前，
必须先扫一遍等价算子替换**。KOR 实证：判「不可能三角」后，仅把 `signed_power(x,0.5)`
换成 `quantile(x)`（骨架其余全冻结）即 2Y 1.51→1.56、prod 0.6544→0.6397；再把外层轴
sector→market ⇒ 2Y 1.62 全闸过。**那个"三角"是 `signed_power` 造成的假性约束。**

**本库最常用的两条**（完整 7 条替换表与三条纪律见
[`02_signal_patterns.md` §12](docs/experience/02_signal_patterns.md)）：

| 替换 | 效果 | 判定 |
|---|---|---|
| `signed_power(x,0.5)` → **`quantile(x)`** | 2Y +0.05~0.11、prod −0.015、持仓变对称 | ★★ 最强破闸；**同时解 §5b 的 INVESTABILITY 墙** |
| 外层轴 sector → **market**（quantile 包装下） | 2Y +0.06 | ★★ **依赖包装算子，不可外推** |

**三条纪律**（照抄会出事）：
1. 记忆里的语法级效应**必须本区实测不可外推**（`SCALE-NEG-RANK` IND 成立 / KOR 反向）；
2. 外层分组轴最优值**依赖内层包装算子**，不能把轴的选择单独外推；
3. **`quantile` 只接受 1 参**（`ts_quantile` 才两参）。

⚠ 本节只给方向，**不生成表达式**；动手改走 `wq-brain-alpha-optimization-v1`。

## 6a. Self-Correlation（`SELF_CORRELATION`）

**要求**：与**自己已提交** alpha 的 PnL 相关 < 线（§0：`GATES_PLATFORM['self_corr_max']`）。**平台还有第二条通过路径**：新 alpha 的 Sharpe 比与之相关的已提交 alpha **高 10%** 也可过——例：新 1.9 vs 旧 1.6 → 1.19× ≥ 1.10 → 过；新 1.7 vs 旧 1.6 → 1.06× < 1.10 → 不过。**本库按单阈值处理，未实现该豁免**（`GATES_PLATFORM` / `submit_queue.LIM` 都是单阈值），所以这条路径在本库是「平台可能放行、本库先拦」的保守偏差。

**取值途径**：本地快筛 `brain-calculate-alpha-selfcorr-quick`（批量）/ MCP `check_self_correlation`（单个）——两者都有**结构性盲区**（近期提交的孪生体不在本地池，见 selfcorr-quick）；平台的 SELF 值目前只在提交响应里（提交即真提交，见 `worldquant-submit-alpha`）。

**失败处置**：**换 idea / 换数据源**，不是换窗口。（PROD 与 SELF 是两个池、两条路，**别混**。）

## 6b. Prod-Correlation（`PROD_CORRELATION`）

**要求**：与**全平台生产池**相关 < 线（§0：`GATES_PLATFORM['prod_corr_max']`）。

**取值**：`check_correlation`（只读 `GET correlations/prod`）——**阻塞轮询 ≤ 60 min、账号级单并发（忙时立即返回 `correlation_busy`）、有 Redis 才缓存**；三种返回的处置与「不要高频 `refresh=true`」的量化见 RA [`prod-corr-avoidance.md`](../wq-brain-ra-pipeline/references/prod-corr-avoidance.md) §1（环境事实只写那一处）。**禁用** `POST /submit` 探测。

**处置**：只按 RA 决策表 [D0-P](../wq-brain-ra-pipeline/references/decision-table.md)（< 0.60 扩；0.60–0.70 不扩、当天进提交步；0.70–0.75 仅 1 次结构性尝试；≥ 0.75 或尝试失败 → 判死）。**不磨参数。**

## 通用建议

- **从简单开始**：先用 `ts_rank` 等基础算子。
- **股票池取本区默认**（`wqb.config.REGIONS` 各区 universe，如 USA=TOP3000、KOR=TOP600、EUR=TOP2500），不要照搬 USA 的选择。
- **ATOM 原则**（单数据集 alpha，享放宽的提交口径，近 2 年 Sharpe 为准）：**判据** = 表达式只用单一数据集的字段（分组字段除外）；**阈值**只引用平台官方表（见 GLOSSARY「ATOM alpha」，不在别处写数字）；**适用对象** = 单数据集 alpha。RA 的跨数据集路线（D3 / D11 / D14）与 ATOM 冲突时：跨集组合**主动放弃 ATOM 放宽**，按常规线（`LOW_2Y_SHARPE` 等）判——这是有意的取舍，不是疏漏。

## 诊断之后：建议路径（本 skill 只建议，不执行）

判定 FAIL 后候选不得直接丢弃或只留 near_pool。先做**资格判定**（[`mode-b-qualification.md`](../wq-brain-alpha-optimization-v1/references/mode-b-qualification.md) 的判定表；命令 `$WQ_PY tools/mode_b_qualify.py evaluate …`），再按结论建议：

| 判定 | 建议路径 | 谁执行 |
|---|---|---|
| `main_gate` / `bypass` | 进 `wq-brain-alpha-optimization-v1` Mode B（`bypass` 带绑定的 `mode_b_action`）；常规 2–3 轮仍卡结构性闸再走「组合腿救援」 | optimization-v1 |
| `no_qualify` | 不进改进；留 near / salvage 或结束；**不写 `dead_end`** | — |
| `dead_end` | **候选级**封存：先 `forum_recon`（`found=true` 不得直接判死），再 `seal_dead_end` | RA 步 9 §9.5 |

- 判死**粒度**：上表是**候选级**（`dead_end(candidate)`，只约束该字段搭配 + 结构 + 设置，见 `brain-dataset-mining-experience`）；**家族 / 波次级**判死按 RA 步 5b / D0-P / D15，本 skill 不做。
- salvage_pool 由 S4 `review_wave.py --write-ledger` 自动幂等写入（combo 候选 + near 补充），**无需人工入池**；入池线 vs 动用线的区别见资格判定表 §5（入池宽、动用严）。

## LOW_2Y_SHARPE / IS_LADDER 破闸

先 `get_alpha_yearly_stats` 诊断逐年形态，再按 设置轴 → 表达式轴 → 机制轴 三级修；末两年符号反转且三轴代表变体都不过 = 该 (区域, 家族) 判死。完整手册（论坛实证 + 文献 + KOR risk71 反例）：[references/two-year-sharpe-playbook.md](references/two-year-sharpe-playbook.md)。
