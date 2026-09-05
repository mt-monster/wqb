---
last_verified: 2026-09-01
name: brain-alpha-judge
description: "判断 WorldQuant BRAIN alpha（Regular 或 PPA / Power Pool）当前是否值得提交：综合平台硬检查、PPA 主题/相关性门控，以及内置的高价值中文论坛 Markdown 语料库。当用户想在提交前做额外质量审查、评估 alpha 是否值得提交、核对 PPA 主题匹配，或在明确确认后提交时使用。★2026-09-01 新增「点塔优选排序」：多个 READY 候选时按金字塔点亮价值排序（点亮=该 catalog 近 90 天提交 ≥3 颗；跨 ≥3 catalog 不计；差 ≤2 颗塔优先；0 亮区域单颗不算点亮；MEA 本季度不提交）。Before submitting a Regular or PPA alpha, when doing quality review or deciding if an alpha is worth submitting"
layer: L5
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - mcp__wq-brain-http__*
user-invocable: true
---







# Brain Alpha Judge（Alpha 判定器）

> **⚠️ 弃用声明（2026-08-31）**：提交判定唯一权威已迁移至 `tools/submit_verdict.py`（403 盲区唯一权威，见 `wq-brain-ra-pipeline` 步 8）——**不要再用本 skill 做"是否提交"的最终判定**。本 skill 仅保留两类参考价值：① PPA 主题匹配/相关性门控的**人工核对清单**；② value-factor trend score（防挤同一金字塔）的**参考评分**。需要最终提交判定时直接跑 `& $WQ_PY tools/submit_verdict.py --alpha-id <ID>`。本 skill 的 READY/REVIEW/BLOCK 三态输出仅作评审参考，不构成提交依据。
>
> **⚠️ 处女提交盲区（2026-09-01 实证，RR7OWQKd）**：`tools/submit_verdict.py` 的提交层 GET 视图依赖"POST 之后才存在"的提交记录——**从未 POST 过的 alpha，GET /submit 返 404**，旧版工具会一律误判 BLOCKED（假阴性）。已修复：`UNSUBMITTED + 404` → PREPOST 降级为"模拟层 + 双闸预检"判定。另两个配套实证：① POST 201 = 异步受理，~40s 内翻 OS/ACTIVE（用 get_alpha_details 轮询确认，勿依赖 POST 返回值）；② 受理后再次 POST 得到的 403 是"已提交"拒绝，**不是硬闸失败**。

本 skill 的**活跃职能只有三个**（其余六步评审流程已于 2026-09-01 删除，判定权威归 `tools/submit_verdict.py`）：
1. **点塔优选排序**（多 READY 候选时定提交顺序，见下方专节——用户准则）；
2. **value-factor trend score**（防挤同一金字塔的参考评分，见下方专节）；
3. **PPA 附加闸门人工核对清单**（仅 PPA 提交前查阅，见下方专节）。

## 衔接协议
- **上游**：S4 链末端——`brain-explain-alphas`（归因）→ `brain-alpha-robustness`（过拟合/稳健性必经闸）。
- **本 skill 角色**：S5 **参考评审**（非最终判定权威，2026-08-31 起）——PPA 主题匹配/相关性门控人工核对清单 + value-factor trend score + 点塔优选排序；最终"是否可提交"以 `tools/submit_verdict.py` 为准。
- **下游**：按「提交路由」段——READY→`worldquant-submit-alpha`（REGULAR/PPA）/`wq-brain-superalpha`（SUPER）；BLOCK→回 S4 `wq-brain-alpha-optimization-v1` Mode B。

## 与 brain-alpha-robustness 的职责边界（2026-08-31 明确）

两者同处 S4→S5 交界，但职责**不重叠**。候选必须先过 robustness 闸，再进 judge 评审。

| 维度 | brain-alpha-robustness（S4→S5 必经闸） | brain-alpha-judge（S5 参考） |
|------|--------------------------------------|------------------------------|
| **核心问题** | 这个 alpha *该不该* 提交？（过拟合诊断） | 这个 alpha *现在值不值得* 提交？（参考评审） |
| **判定性质** | 诊断性（PASS/CONDITIONAL/REJECT） | 参考性（READY/REVIEW/BLOCK，不构成提交依据） |
| **关注指标** | 近 3 年强度、衰减比、CV_Sharpe、厂字形、sub-universe、top-5 集中度、参数敏感性 | PPA 主题/标签/硬指标、相关性门控、value-factor trend、点塔价值 |
| **数据源** | `get_alpha_yearly_stats`/`get_alpha_pnl`/`performance_comparison` | 平台 IS checks + `check_correlation` + trend score |
| **是否改表达式** | 否（诊断不改；修复归 `brain-alpha-repair`） | 否（只评审） |
| **输出** | robustness 审计报告 + 三态判定 | 点塔排序 + trend score + PPA 核对结论 |

**执行顺序（硬约束）**：`brain-explain-alphas`（按需）→ **robustness（必经）** → `tools/submit_verdict.py`（判定权威）→ judge（可选参考：点塔/PPA 核对）→ 提交路由。

## 适用范围

- Regular 与 PPA alpha 的**参考评审**（最终判定一律走 `tools/submit_verdict.py`）。
- PPA 主题 / PPAC / 互相关性门控在 agent 会话中使用 BRAIN MCP（`mcp__wq-brain-http__*`）。
- 仅在用户明确确认后提交。

## PPA 附加闸门（Power Pool，人工核对清单）

仅当用户明确说明"仅 Regular（不涉及 Power Pool）"时才可跳过。

- **主题（Theme）**：通过 `mcp__wq-brain-http__get_messages` 获取当前 Power Pool 主题。若区域/数据集不匹配，判定结果不能为 `READY`（应返回 `WAIT_THEME_ROTATION`）。
- **标签（Tags）**：计划提交的标签必须包含 `PowerPoolSelected`；颜色为 GREEN。
- **硬指标**：Sharpe ≥ 1.58、Fitness ≥ 1.0、TVR 5–20%、**LOW_2Y_SHARPE 严格 > 1.58**、CONCENTRATED_WEIGHT 必须通过。`mcp__wq-brain-http__get_alpha_details` 返回 WARNING 不算通过。
- **相关性**：PROD < 0.7，SELF < 0.5。优先在 `mcp__wq-brain-http__*` 上使用本地 `mcp__wq-brain-http__check_self_correlation` / `mcp__wq-brain-http__compute_mutual_correlation`（不占用平台相关性配额）。同数据集同腿兄弟 alpha（corr 0.82–1.0）→ 返回 `BLOCK`，建议更换数据集。
- **CW 配方**：`rank(add(...))` 通常 FAIL；优先 `add(multiply(rank(...), w1), multiply(rank(...), w2))` 并配合 `ts_backfill`。
- **提交语义**：提交统一走 `mcp__wq-brain-http__workflow_submit_alpha`（workflow 引擎，含预检+状态轮询）。HTTP 201 = 异步受理，~40s 内翻 OS/ACTIVE（用 `get_alpha_details` 轮询确认，勿依赖 POST 返回值）。若该 MCP 工具不感知 PPA，不要通过 MCP 自动提交 PPA —— 停下并询问用户。

若 `platform_submit_ok=false` **或**任一 PPA 附加闸门失败，候选不能进入提交确认。

## Value Factor Trend Score 含义

judge 在每次运行时计算 value-factor trend 上下文块。

- 仅使用提交日期（`stage=OS`），窗口可配置。
- 仅使用 Regular alpha。
- `A` 表示窗口内的 ATOM alpha 数量。
- 此处的 ATOM 指单一数据集纯度（`SINGLE_DATA_SET` 分类，含 `atom` 回退）。

返回的字段：

- `N`：窗口内 Regular 提交数量
- `A`：窗口内 ATOM Regular 提交数量
- `P`：已覆盖的金字塔类别数
- `P_max`：平台 multipliers 给出的金字塔类别总数
- `S_A = A / N`
- `S_P = P / P_max`
- `S_H`：各金字塔分布的归一化熵
- `diversity_score = S_A * S_P * S_H`

解读：

- `S_A` 越高：单数据集提交占比越干净
- `S_P` 越高：金字塔覆盖越广
- `S_H` 越高：已覆盖金字塔之间的分布越均衡

该分数作为判断质量与 value-factor 方向的上下文被计算并报告。
本 skill 还会给出当前候选的假设投影，展示该 alpha 若提交进同一窗口，diversity score 的前后变化、delta 与方向。
它不会自动提交，也不会绕过明确确认。

## 确认规则

正常使用下绝不自动提交。本 skill 不执行提交——提交一律走
`tools/submit_verdict.py`（判定 SUBMITTABLE）+ 用户明确确认 + `worldquant-submit-alpha`。

## 提交路由（参考说明；最终提交判定以 `mcp__wq-brain-http__submit_verdict` 为权威，本 skill verdict 仅作评审参考，不构成提交依据）

以下路由由 `wq-brain-ra-pipeline` 步 8 统一决策，本 skill 不输出路由指令：

- 参考 verdict=READY 且 `submit_verdict` 判定 SUBMITTABLE、用户确认后：
  - type=REGULAR / PPA 单颗 → `worldquant-submit-alpha`（真实提交 API；覆盖 description PATCH 与状态翻转坑）。
  - type=SUPER（≥10 个 ACTIVE REGULAR 组件合成）→ `wq-brain-superalpha`（neutralization 逐区扫描 + selection/combo 工作流）。
- 参考 verdict=REVIEW → 列出缺失证据，用户人工确认后按上述路由。
- 参考 verdict=BLOCK（含 prod_corr≥0.7、同数据集同腿兄弟 corr 0.82–1.0）→ 回 `wq-brain-alpha-optimization-v1` Mode B（见其「prod_corr 反馈循环」节），不提交。
- 提交完成（OS 池 `status=ACTIVE`）→ 交 `wq-backtest-monitor`（S6）跟踪与台账回写。

## ★ 点塔优选排序（2026-09-01 用户准则，多个 READY 候选时按此定提交顺序）

**优先点塔：优先提能点亮「未点亮」金字塔塔的 alpha；同档内按绩效（fitness 降序）排序。**
在多个候选都 READY 且配额不足（REGULAR 4/ET 日 + SUPER 1/ET 日）时，按下述顺序挑选：

1. **点亮口径（三层，全实证）**：
   - 点亮 = 该 catalog（区域×延迟×类别，`pyramids[].name`）下**近 90 天提交的 ACTIVE ≥3 颗**（窗口外老 alpha 不计数）；
   - **跨 ≥3 个 catalog 的 alpha 不计点塔**（平台 `pyramidThemes.effective`：1塔→1、2塔→2、3塔→0）；
   - **0 亮区域的单颗提交 ≠ 点亮**（要凑 3 颗同类；单颗只是打地基）。
2. **候选点塔价值分级**（先算每塔当前颗数，用 `tracking/_submit_kit/_tower_map.py` 或 `tools/submit_verdict.py`）：
   - A 档：落「差 ≤2 颗」塔（现状 ≥2/3）→ **一次提交即点亮**，最优先；
   - B 档：落「差 2 颗」塔（现状 1/3）；
   - C 档：落 0/3 塔（0 亮区域打地基，如 GLB/HKG/DEU/ASI/GBR 全域 0 亮时）。
   - 同档内按 fitness 降序，其次 sharpe。
3. **已过度提交区域**（如 MEA 本季度）**不提交**，候选只罗列交用户拍板。
4. **跨 ≥3 catalog 的候选表达式直接降级**（提交后对点塔零贡献，即使指标好）。
5. 候选将点亮哪座塔：未提交 alpha 的 `pyramids` 恒为空 → 用 `alphas.dataset_id → datasets.category`
   拼塔名；缺失时表达式字段反查 `fields` 表（多数票）；仍 UNKNOWN 按该区域未亮类别保守判断。
   权威字段归属用 `GET /data-fields/{field}?region=&universe=&delay=`（列表接口带 search 返回 Invalid query，不可用）。
6. 提交后复核：`_tower_map.py` 重跑确认目标塔颗数 +1 且 ≥3（点亮成立）。

## 提交语义（2026-08-11 GBR 战役已验证）

`mcp__wq-brain-http__get_alpha_details`/`/check` 对 LOW_2Y_SHARPE 和 CONCENTRATED_WEIGHT 只显示 **WARNING** —— 真正的通过/失败在**提交时**才判定：

- `POST /alphas/{id}/submit` → **201** = 已受理（异步检查待执行；只接受 200 的 MCP 客户端会误报 `success:false` —— 工具 bug）。
- `GET /alphas/{id}/submit` → **200** = 最终成功 / **403** = 被拒（body 含失败检查列表）/ **404** = 记录已清除。
- 唯一可靠的成功信号是 alpha 出现在 OS 池中（`status=ACTIVE`）。不要仅凭 POST 状态或详情检查判断成功。
- PENDING 检查（如异步中的 SELF_CORRELATION）是未决，不是失败。

内置的 `ace_client.py` 现在提供 `get_submit_verdict()`（POST+GET 三态判定）与 `classify_check_pass()`（返回 `True/False/None`，None = 未决/警告）。`baseline_from_platform()` 为此包含 `submit_verdict` 与 `pending_checks`。

## 独立原则

将本 skill 视为自包含。

- 仅从本 skill 目录导入。
- 内置运行时辅助代码放在 `scripts/vendor/` 下。
- 不要依赖来自 `untracked/` 或 `untracked/APP/` 的运行时导入。

## 参考

- 附加标准： [references/extra-standard-rubric.md](references/extra-standard-rubric.md)
- 来源政策： [references/source-selection.md](references/source-selection.md)
- 语料清单： [references/corpus-manifest.md](references/corpus-manifest.md)
- 改进路线图： [references/improvement-roadmap.md](references/improvement-roadmap.md)
- 未来改进指南： [references/future-improvement-guide.md](references/future-improvement-guide.md)
- 机器可读标准： `data/extra_submission_rubric.json`
