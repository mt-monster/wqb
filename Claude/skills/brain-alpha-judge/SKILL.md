---
last_verified: 2026-09-01
name: brain-alpha-judge
description: "（参考层·非提交判定）评估 WorldQuant BRAIN alpha（Regular 或 PPA / Power Pool）的提交参考价值：综合平台硬检查、PPA 主题/相关性门控，以及内置的高价值中文论坛 Markdown 语料库。当用户想在提交前做额外质量审查、评估 alpha 是否值得提交、核对 PPA 主题匹配，或在明确确认后提交时使用。★2026-09-01 新增「点塔优选排序」：多个 READY 候选时按金字塔点亮价值排序（点亮=该 catalog 近 90 天提交 ≥3 颗；跨 ≥3 catalog 不计；差 ≤2 颗塔优先；0 亮区域单颗不算点亮；MEA 本季度不提交）。Before submitting a Regular or PPA alpha, when doing quality review or deciding if an alpha is worth submitting"
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

> **⚠️ 弃用声明（2026-08-31）**：提交判定唯一权威已迁移至 `tools/submit_verdict.py`（403 盲区唯一权威，见 `wq-brain-ra-pipeline` 步 8）——**不要再用本 skill 做"是否提交"的最终判定**。本 skill 仅保留两类参考价值：① PPA 主题匹配/相关性门控的**人工核对清单**；② value-factor trend score（防挤同一金字塔）的**参考评分**。需要最终提交判定时直接跑 `& $WQ_PY tools/submit_verdict.py --alpha-id <ID> --with-quota`。本 skill 的 READY/REVIEW/BLOCK 三态输出仅作评审参考，不构成提交依据。
>
> **⚠️ 处女提交盲区（2026-09-01 实证，RR7OWQKd）**：`tools/submit_verdict.py` 的提交层 GET 视图依赖"POST 之后才存在"的提交记录——**从未 POST 过的 alpha，GET /submit 返 404**，旧版工具会一律误判 BLOCKED（假阴性）。已修复：`UNSUBMITTED + 404` → PREPOST 降级为"模拟层 + 双闸预检"判定。另两个配套实证：① POST 201 = 异步受理，~40s 内翻 OS/ACTIVE（用 get_alpha_details 轮询确认，勿依赖 POST 返回值）；② 受理后再次 POST 得到的 403 是"已提交"拒绝，**不是硬闸失败**。

本 skill 以**两道硬闸**（① 平台基线硬检查 + ② PPA 附加闸门）为骨架、按下方「闸门顺序」六步执行的工作流处理 Regular **与** PPA（Power Pool）alpha。

## 衔接协议（参考层，非提交判定）
- **上游**：S4 链末端——`brain-explain-alphas`（归因）→ `brain-alpha-robustness`（过拟合/稳健性必经闸）。
- **本 skill 角色**：S5 参考核对层（**非最终判定**）——仅提供 ① PPA 主题/相关性门控人工核对清单、② value-factor trend score、③ 点塔优选排序（多 READY 候选时的排序参考）。**最终提交判定唯一权威 = `tools/submit_verdict.py`**，本 skill 的 READY/REVIEW/BLOCK 三态输出不构成提交依据。
- **下游**：`submit_verdict.py` READY + 用户确认后，直接走 `worldquant-submit-alpha`（REGULAR/PPA）或 `wq-brain-superalpha`（SUPER），不再经本 skill 路由。

## 与 brain-alpha-robustness 的职责边界（2026-08-31 明确）

两者同处 S4→S5 交界，但职责**不重叠**。候选必须先过 robustness 闸，再进 judge 评审。

| 维度 | brain-alpha-robustness（S4→S5 必经闸） | brain-alpha-judge（S5 评审） |
|------|--------------------------------------|------------------------------|
| **核心问题** | 这个 alpha *该不该* 提交？（过拟合诊断） | 这个 alpha *现在值不值得* 提交？（综合评审） |
| **判定性质** | 诊断性（PASS/CONDITIONAL/REJECT） | 决策性（READY/REVIEW/BLOCK） |
| **关注指标** | 近 3 年强度、衰减比、CV_Sharpe、厂字形、sub-universe、top-5 集中度、参数敏感性 | 平台硬检查、PPA 主题/标签/硬指标、相关性门控、value-factor trend、多样性投影 |
| **数据源** | `get_alpha_yearly_stats`/`get_alpha_pnl`/`performance_comparison` | 平台 IS checks + `check_correlation` + 本地论坛语料 + trend score |
| **是否改表达式** | 否（诊断不改；修复归 `brain-alpha-repair`） | 否（只评审） |
| **输出** | robustness 审计报告 + 三态判定 | verdict + confidence + 中文评语 + 可执行建议 |

**执行顺序（硬约束）**：`brain-explain-alphas` → **robustness（先）** → **judge（后）** → 提交路由。
- robustness REJECT → 不进 judge，直接回写台账/失败记忆。
- robustness PASS/CONDITIONAL → 进 judge 做最终提交评审。
- judge 不重复 robustness 的归因计算；judge 引用 robustness 的结论作为证据输入。
- 任一 skill 判 BLOCK/REJECT 都必须给出 ≥3 条可执行建议并引用证据。

## 适用范围

- Regular 与 PPA alpha。
- 内置静态本地语料库作为附加判定标准（judge CLI 内不连接实时论坛）。
- PPA 主题 / PPAC / 互相关性门控在 agent 会话中使用 BRAIN MCP（`mcp__wq-brain-http__*`）。
- 仅在用户明确确认后提交。

内置语料位于 `data/forum_corpus/` 及 `data/forum_corpus/index.json`。
V1 当前包含 20 篇打包进本 skill 的已收录中文语料条目：

- 本地保留 20 篇全文 Markdown 帖子。
- 长超时本地恢复扫描后，剩余 0 条内置搜索快照条目。

## 闸门顺序

> **凭据前置**：平台硬检查与 trend score 需要 BRAIN 凭据，读取顺序为
> `configs/config.json`（首次使用需 `cp configs/config.example.json configs/config.json` 后填写）→ 环境变量 `BRAIN_USERNAME`/`BRAIN_PASSWORD` →
> `world-quant-brain-mcp/.env` (`CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`) →
> `~/secrets/platform-brain.json`。无凭据时脚本**自动降级为纯表达式启发式判定**（不崩溃，
> 但平台检查与 trend 数据缺失，判定仅供参考）。LLM 层缺 API key 时同样自动降级。

1. 执行平台硬检查，确认 alpha 在基线上可提交。
2. 若候选为 PPA（或标签含 PowerPoolSelected）：提交前先运行下方 **PPA 附加闸门**。
3. 依据已提交的 Regular alpha（OS 窗口）计算 value-factor trend score 上下文。
4. 应用由本地语料推导出的附加提交标准，判断该 alpha 现在是否值得提交。
5. 视情况运行 LLM 决策层，综合 checks + 表达式 + trend + rubric 证据。
6. 仅在用户明确确认后提交。

## PPA 附加闸门（Power Pool）

仅当用户明确说明"仅 Regular（不涉及 Power Pool）"时才可跳过。

- **主题（Theme）**：通过 `mcp__wq-brain-http__get_messages` 获取当前 Power Pool 主题。若区域/数据集不匹配，判定结果不能为 `READY`（应返回 `WAIT_THEME_ROTATION`）。
- **标签（Tags）**：计划提交的标签必须包含 `PowerPoolSelected`；颜色为 GREEN。
- **硬指标**：Sharpe ≥ 1.58、Fitness ≥ 1.0、TVR 5–20%、**LOW_2Y_SHARPE 严格 > 1.58**、CONCENTRATED_WEIGHT 必须通过。`mcp__wq-brain-http__get_alpha_details` 返回 WARNING 不算通过。
- **相关性**：PROD < 0.7，SELF < 0.5。优先在 `mcp__wq-brain-http__*` 上使用本地 `mcp__wq-brain-http__check_self_correlation` / `mcp__wq-brain-http__compute_mutual_correlation`（不占用平台相关性配额）。同数据集同腿兄弟 alpha（corr 0.82–1.0）→ 返回 `BLOCK`，建议更换数据集。
- **CW 配方**：`rank(add(...))` 通常 FAIL；优先 `add(multiply(rank(...), w1), multiply(rank(...), w2))` 并配合 `ts_backfill`。
- **提交语义**：MCP `mcp__wq-brain-http__submit_alpha` 将 HTTP 201 视为失败是工具 bug。确认 OS 池中 `status=ACTIVE`。若该 MCP 工具不感知 PPA，不要通过 MCP 自动提交 PPA —— 停下并询问用户。

若 `platform_submit_ok=false` **或**任一 PPA 附加闸门失败，LLM 判定结果不能为 `READY`。

## LLM 决策层

收集完全部结构化证据后，judge 可调用 LLM 产出最终判定与评语。

两种执行模式：

- Agent 模式（本 AI 对话中优先）：直接使用当前 AI 会话产出 LLM 判定与评语，无需额外 API key。
- 脚本 API 模式（独立 CLI 可选）：调用外部 OpenAI 兼容端点，需要 API key。

- 输入证据包括：平台检查结果、失败项、表达式、表达式分析、附加标准状态/原因、value-factor trend 块，以及假设提交后的 value-factor 投影块。
- 输出包括：`verdict`、`confidence`、`comment`、`strengths`、`risks`。
- LLM 文本输出（`comment`、`strengths`、`risks`）应为中文（默认简体中文）。
- 最终 `overall_verdict`：有 LLM 判定时用 LLM 结果，否则回退到确定性规则判定。
- 安全护栏：若 `platform_submit_ok=false` 或 PPA 附加闸门失败，LLM 判定不能为 `READY`。

默认开启。在 `configs/config.json` 的 `judge.llm` 下配置（首次使用需 `cp configs/config.example.json configs/config.json` 后填写）。

## 建议要求

判定候选 alpha 时，务必给出基于本地文档/标准证据的可执行建议。

- 建议必须引用语料/标准证据（帖子 ID 或规则 ID）。
- 建议应直接对应失败项与缺失的证据字段。
- 最低目标：当判定为 `REVIEW` 或 `BLOCK` 时给出至少 3 条具体行动。

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

## 检查本地语料库

若想在判定前检查支撑用的 Markdown 语料：

```powershell
Set-Location "<SKILL_ROOT>/brain-alpha-judge"
Get-ChildItem "data/forum_corpus"
Get-Content "data/forum_corpus/index.json"
```

语料政策与当前清单请阅读：

- [references/source-selection.md](references/source-selection.md)
- [references/corpus-manifest.md](references/corpus-manifest.md)

## 判定一个候选 alpha

本地语料与标准就绪后，使用 judge CLI。

按 ID 判定单个 alpha：

```powershell
Set-Location "<SKILL_ROOT>/brain-alpha-judge"
python scripts/judge_alpha.py --alpha-id "<alpha_id>"
```

从 JSON 批量判定候选：

```powershell
Set-Location "<SKILL_ROOT>/brain-alpha-judge"
python scripts/judge_alpha.py --input-json "data/candidates.example.json"
```

judge 默认将 JSON 与 Markdown 报告写入 `outputs/`。

可选 trend-score 窗口控制：

```powershell
Set-Location "<SKILL_ROOT>/brain-alpha-judge"
python scripts/judge_alpha.py --alpha-id "<alpha_id>" --trend-window-days 365
python scripts/judge_alpha.py --alpha-id "<alpha_id>" --trend-start-date "2025-01-01T00:00:00Z" --trend-end-date "2026-01-01T00:00:00Z"
```

LLM 配置示例：

```json
{
  "judge": {
    "llm": {
      "enabled": true,
      "provider": "openai-compatible",
      "model": "gpt-4o-mini",
      "api_url": "https://api.openai.com/v1/chat/completions",
      "api_key": ""
    }
  }
}
```

也可通过环境变量提供 key：

- `BRAIN_JUDGE_LLM_API_KEY`
- `OPENAI_API_KEY`

## 确认规则（已简化：本 skill 不执行提交）

本 skill 是参考层，**不执行提交**。提交由 `tools/submit_verdict.py` 判定 + 用户确认后，走 `worldquant-submit-alpha`（真实提交 API）。

`scripts/judge_alpha.py` 仅作离线评审参考，`--confirm-submit` 已废弃，勿再用它触发真实提交。

## 提交路由（统一由 submit_verdict.py 判定，本 skill 只给参考）

- `submit_verdict.py --with-quota` 返回 READY 且用户确认后：
  - type=REGULAR / PPA 单颗 → `worldquant-submit-alpha`（真实提交 API；覆盖 description PATCH 与状态翻转坑）。
  - type=SUPER（≥10 个 ACTIVE REGULAR 组件合成）→ `wq-brain-superalpha`（neutralization 逐区扫描 + selection/combo 工作流）。
- 参考层 BLOCK 信号（prod_corr≥0.7、同数据集同腿兄弟 corr 0.82–1.0）→ 回 `wq-brain-alpha-optimization-v1` Mode B（见其「prod_corr 反馈循环」节），不提交。
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
