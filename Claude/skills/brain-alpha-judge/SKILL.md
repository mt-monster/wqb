---
last_verified: 2026-09-29
name: brain-alpha-judge
description: "提交前的参考评审（非提交判定、不提交）：PPA 主题 / 相关性人工核对清单、value-factor trend score、多候选点塔排序。当用户想在提交前做额外质量审查、核对 PPA 主题匹配，或需要给多个过闸候选排提交顺序时使用。Reference-only review before submitting a Regular or PPA alpha: PPA theme checklist, value-factor trend score, pyramid-lighting order. It never judges submittability and never submits."
layer: L5
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - mcp__wq-brain-http__*
user-invocable: true
---

# Brain Alpha Judge（提交前参考评审）

## 职责边界

- **本 skill 负责**：S5 **参考核对层**，三个职能：① PPA 主题 / 相关性**人工核对清单** ② value-factor **trend score** ③ **多候选点塔排序**（口径指向 `worldquant-submit-alpha`）
- **本 skill 不做**：**不作「是否提交」的判定、不执行提交**——否决权威 = `tools/submit_verdict.py`；放行 = 用户明确确认后 `worldquant-submit-alpha`（REGULAR / PPA）/ `wq-brain-superalpha`（SUPER）。代码里**没有提交路径**：`--confirm-submit` 已移除（传入直接报错退出 2），vendor 的 `AceClient.submit_alpha` 只抛错，`get_submit_verdict` 只 GET（`tests/unit/test_judge_never_submits.py` 守）。与 `brain-alpha-robustness` 不重叠（诊断 vs 参考评审）
- **上游 / 下游**：上游 = 已过资格门的候选；下游 = 用户 / 提交链（不经本 skill 路由）

**READY / REVIEW / BLOCK 三态只是评审摘要**（脚本的词汇，`submit_verdict` 没有 READY），不构成提交依据；`worth_submit_now` 也只表示「评审上值得排进提交队列」。

## 在提交链中的位置（一条链，以 [`AGENTS.md`](AGENTS.md) 与 [`submit-chain.md`](../worldquant-submit-alpha/references/submit-chain.md) 为准）

`资格门（Failed RA / PPA = 0）→ brain-alpha-robustness → submit_verdict（只有否决权）→ prod 实测 → 用户明确确认 → workflow_submit_alpha`。
**judge 不在必经链上**：它是可选的参考，用在「要不要 / 先提哪颗」有疑问时。旧文把它写成「必经 / 决策性」并要求「robustness 之后进 judge 做最终提交评审」，与链矛盾，已删。

| | brain-alpha-robustness | brain-alpha-judge |
|---|---|---|
| 问题 | 会不会过拟合？（诊断） | 现在值不值得排进提交队列？（参考） |
| 输出 | PASS / CONDITIONAL / REJECT | READY / REVIEW / BLOCK（仅参考）+ 评语 + 建议 |
| 数据 | 逐年统计 / PnL / `performance_comparison` | 平台 IS checks + 相关性 + 本地静态语料 + trend score |
| 是否改表达式 | 否（修复归 `brain-alpha-repair`） | 否 |

judge **不读取** robustness 的输出（脚本里没有对应字段）；两者互不引用结论，用户 / agent 各自读各自的报告。

## 运行与降级

```
$WQ_PY scripts/judge_alpha.py --alpha-id <ID>                 # 按 ID（需要平台数据）
$WQ_PY scripts/judge_alpha.py --input-json <candidates.json>  # 批量；候选字段见「证据字段」
$WQ_PY scripts/judge_alpha.py --alpha-id <ID> --trend-window-days 365
```

- 工作目录 = 本 skill 目录（`scripts/judge_alpha.py` 相对它解析）；报告写到 `outputs/judge_<UTC 时间戳>.json` 与 `.md`；stdout 打印两个路径与条数。退出码：0 = 已出报告，2 = 传了已移除的 `--confirm-submit`。
- **凭据**：只读**进程环境变量** `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（旧别名 `BRAIN_USERNAME` / `BRAIN_PASSWORD` 仍认）。**不读 `.env`、不读 `configs/config.json` 或 `~/secrets/` 里的明文、不把密码放命令行**（AGENTS.md）；这些文件里若有凭据，脚本在 stderr 提示迁移，不打印值。
- **降级运行**（无凭据 / 平台取不到数）：只剩表达式启发式，**verdict 上限 REVIEW**，报告首行标「降级运行」、JSON 里 `degraded.is_degraded = true`——**不得作为提交依据**。
- **LLM 层默认关闭**（`configs/config.example.json` 的 `judge.llm.enabled=false`）。开启后会把候选的检查指标 / 相关性 / 表达式**结构统计** / 论坛语料摘录发往 `llm.api_url` 指向的**第三方端点**；**表达式原文默认不外发**（`judge.llm.send_expression=true` 才带）；密钥只认环境变量 `BRAIN_JUDGE_LLM_API_KEY`（不读配置里的 `api_key`，也不回落到 `OPENAI_API_KEY`）。外发字段白名单见 `build_llm_payload`。LLM 只能**收紧**确定性判定（取两者中更严的），不能把 REVIEW / BLOCK 抬成 READY——所以 `overall_verdict` 的上界由确定性规则决定，可复现。

## 职能 1：PPA 主题 / 相关性人工核对清单

何时跑：候选 `type == PPA` 或标签含 `PowerPoolSelected`（仅当用户明确说「只做 Regular」才可跳过）。逐项人工核对，**脚本不逐项校验**（下表标明哪些有代码）：

| 项 | 口径 | 来源 / 是否有代码 |
|---|---|---|
| 主题 | region / delay / universe 匹配**当期** Power Pool 主题 | `mcp__wq-brain-http__get_messages(limit=30)` 实时重扫（RA 步 1）；无代码。不匹配 → 候选由 agent 手工标 `YELLOW + WAIT_THEME_ROTATION`（**没有代码实现**，脚本只有三态） |
| 标签与颜色 | tags 含 `PowerPoolSelected`；color = **`PURPLE`**（PPA 通道专用色；GREEN 须由 OS 结果挣得，禁作默认） | `alpha_properties.COLOR_PPA`；脚本**不校验**颜色 |
| 资格线 | `Failed PPA == 0`（`PPA_CHECK_NAMES`）；**`LOW_SHARPE` 只在 value < 1 时计失败**——PPA 不套 REGULAR 的 1.58 严线，Sharpe ∈ [1.0, 1.58) 的合法 PPA 不得判 BLOCK | `judge_alpha.INTERNAL_HARD_GATES["ppa_sharpe_min"]`，与 `wqb.config` 一致（`tests/unit/test_judge_gates_match_config.py` 守）；口径见 [`webdatascope-failed-gates.md`](../wq-brain-ra-pipeline/references/webdatascope-failed-gates.md) |
| 相关性 | PROD < 0.7（平台线）；SELF < 0.5 是**内部严线 / PPAC 口径**，不是平台硬闸；同数据集同腿兄弟（corr 0.82–1.0）→ 建议换数据集 | `check_self_correlation` / `compute_mutual_correlation`（本地，不占平台配额）；prod 用 `check_correlation` |
| CW（`CONCENTRATED_WEIGHT`） | 必须过；`get_alpha_details` 只显示 WARNING，**提交时才判 FAIL**，别当通过 | 修法见 [`brain-how-to-pass-alpha-test` §4](../brain-how-to-pass-alpha-test/SKILL.md)（时间平滑；**不是**换成加权腿相加——那是被禁的混信号形态） |
| 提交渠道 | MCP `workflow_submit_alpha` **不感知 PPA**，本地预检不看 `PowerPoolSelected`：合法但指标较低的 PPA 会被拦 → 停下交接，用户在 web UI 提交 | [`ppa-handoff.md`](../worldquant-submit-alpha/references/ppa-handoff.md) |

若 `platform_submit_ok=false` 或任一 PPA 闸失败，`overall_verdict` 不能为 READY（代码：LLM 只能收紧；内部硬闸失败 → BLOCK，仅配额未释放 → REVIEW）。

## 职能 2：value-factor trend score（防挤同一金字塔）

每次运行计算，**仅信息**：只用 `stage=OS` 的 Regular 提交，窗口可配（缺省 365 天，`--trend-window-days`）。字段：

| 字段 | 含义 |
|---|---|
| `N` / `A` | 窗口内 Regular 提交数 / 其中 ATOM 数 |
| `P` / `P_max` | 已覆盖的金字塔类别数 / 平台给出的类别总数 |
| `S_A = A/N`，`S_P = P/P_max`，`S_H` | ATOM 占比 / 类别覆盖率 / 各金字塔分布的归一化熵 |
| `diversity_score = S_A × S_P × S_H` | 任一因子为 0 则整体为 0 |

同时给出「若该候选提交进同一窗口」的假设投影（前后 diversity score、delta、方向）。

- **ATOM 在这里 = 单一数据集纯度（`SINGLE_DATA_SET` 分类，含 atom 回退）**；`brain-how-to-pass-alpha-test` 里的「ATOM」指提交标准的放宽档（近 2 年 Sharpe），**不是同一个定义**，词表见 GLOSSARY。
- **`S_P`（类别覆盖率，宏观多样性）与「点亮数（近 90 天 ≥ 3 颗 ACTIVE）」是两个不同的金字塔指标**：前者衡量已提交组合的分散度，后者决定**先提哪颗**（职能 3）。两者互不替代。
- **没有决策用途**：delta 为负时不自动拦截也不改判定，只作为「先提别的」的提示；要阻止请走职能 3 的排序或用户判断。

## 职能 3：多候选点塔排序

配额不足、多个候选都过闸时，**口径与排序只在 [`worldquant-submit-alpha/references/quota-and-tower.md` §2](../worldquant-submit-alpha/references/quota-and-tower.md)**（点亮 = 近 90 天 ≥ 3 颗 ACTIVE；跨 ≥ 3 个 catalog 不计；分档「差 1 颗 / 差 2 颗 / 0/3 需凑 3 颗」；同档内轮转再按 fitness）。本 skill 不再自带一份——旧文是 submit-alpha 的逐句拷贝，并共享了两处逻辑错误（A 档「差 ≤ 2 颗」与 B 档「差 2 颗」重叠；「差 2 颗一次提交即点亮」不成立），现已随 submit-alpha 一并更正。

## 证据字段（`--input-json` 候选与 rubric）

rubric（`data/extra_submission_rubric.json` 8 条规则，**机器可读源**；英文说明 [`references/extra-standard-rubric.md`](references/extra-standard-rubric.md) 只作解释）对候选的 notes 字段做「**文本非空即通过**」的检查——所以它能被凑数，只是提醒，不是证据。字段从哪来：

| 字段 | 来源 |
|---|---|
| `idea_summary` / `rationale` | **`--alpha-id` 模式自动取平台三段式 description**（Idea → `idea_summary`；两段 Rationale → `rationale`；此前该模式下 `economic_foundation` 天生不过） |
| `template_notes` / `stability_notes` / `test_period_notes` / `cross_universe_notes` / `cross_region_notes` | `brain-explain-alphas`（概念与模板）与 `brain-alpha-robustness`（稳健性 / 跨 universe 复测）的输出，由调用方摘入 |
| `coverage_notes` / `turnover_notes` / `liquidity_notes` / `capacity_notes` | `get_alpha_details` 的 `is` 指标与字段体检档案 |
| `diversification_notes` / `portfolio_fit_notes` / `submission_priority_notes` / `value_factor_notes` | `check_correlation` / `compute_mutual_correlation`、职能 2 的 trend 投影、职能 3 的档位 |

建议格式建议写 `{动作, 对象, 预期, 验收}`；**证据 id（帖子 / 规则 id）可选**——旧文要求每条建议都引用语料，会逼人凑引用；旧文的「REVIEW / BLOCK 至少 3 条」数量下限同样已删，不为凑数。

## 语料

`data/forum_corpus/` 是**静态快照**（篇数与生成日期见 `data/forum_corpus/index.json`：当前 21 篇，`generated_at` 2026-04-12），judge 不连接实时论坛，也没有自动更新机制。政策与清单：[`references/source-selection.md`](references/source-selection.md)、[`references/corpus-manifest.md`](references/corpus-manifest.md)。引用里的 `TL87739` / `XX42289` 等是论坛用户名缩写，出处见 `index.json`。

## 情景卡

见 [`references/scenarios.md`](references/scenarios.md)：JD-01 PPA 候选（Sharpe 1.2、PPAC 0.42、主题当期匹配）、JD-02 多候选点塔排序、JD-03 降级运行。

## 开发者备忘（不属于 agent 用法）

自包含原则、vendor 目录用途与 `INTERNAL_HARD_GATES` 是内部闸的第 3 份拷贝（`config.GATES_INTERNAL`、`submit_queue.LIM`、此处；一致性由测试守）等，见 [`references/developer-notes.md`](references/developer-notes.md)。规划类文档已移出运行时 references（`attic/judge_planning_docs_20260929/`）。
