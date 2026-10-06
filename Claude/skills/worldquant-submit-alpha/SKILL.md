---
last_verified: 2026-10-06
name: worldquant-submit-alpha
description: "把用户已确认的 REGULAR alpha 真实提交到 WorldQuant Brain 平台（POST /alphas/{id}/submit，不可逆）：workflow_submit_alpha 预检 → 用户确认后提交 → 四态响应处置（补发 / ASYNC_STUCK）。用户说“提交 alpha / submit / 上平台 / 落地”时用。不作提交判定（→ submit_verdict）、不处理 SUPER（→ wq-brain-superalpha）；PPA 人工通道与配额、点塔优选见 references/。"
layer: L5
allowed-tools:
  - Read
  - Bash
  - mcp__wq-brain-http__*
---

# WorldQuant Brain — 实际提交 Alpha 到平台

## 职责边界

- **本 skill 负责**：**REGULAR 单颗 alpha 的真实提交**——`workflow_submit_alpha` 预检 → 用户确认后的 `POST /alphas/{id}/submit` → 四态响应处置（补发 / `ASYNC_STUCK`）→ 属性规范；并给出配额口径与点塔优选规则（`references/quota-and-tower.md`）
- **本 skill 不做**：**不处理 SUPER 组套**（→ `wq-brain-superalpha`）；**不作提交判定**（否决判定 = `tools/submit_verdict.py`，权力分层见 `references/submit-chain.md`）；**不替用户确认**；不改表达式；PPA 的人工通道只出交接单（`references/ppa-handoff.md`）
- **上游 / 下游**：上游 = 用户已明确确认的候选（`submit_verdict` 不是 `BLOCKED`、资格门 Failed RA = 0、prod 实测 < 0.7，见提交链 §2）；下游 = `status=ACTIVE` 的 alpha + S6（`wq-backtest-monitor` §14 台账回写）

> ⚠ **不可逆：`POST /alphas/{id}/submit`——通过即提交，无撤回；没有「零成本探测」。** 前置、默认形态、确认、核验的完整块见 [`references/submit-chain.md`](references/submit-chain.md) §0。
> 要点：默认 `confirm_submit=False`（只预检）；**用户明确确认后**才可置 `True`；提交后必须核验 `status == ACTIVE` 且 `dateSubmitted` 非空。

## 何时用

用户要把某个已模拟出的 alpha（已知 `alpha_id`）真正提交到平台。很多脚本里的「submit」只是本地打标或**派发仿真**（`POST /simulations`，见 `GLOSSARY.md`「dispatch」）——本 skill 只管**真正落到平台**的那一步。
凭据由 MCP 服务端加载，agent 不接触（不读 `.env`、不在命令行传口令）。

## 提交流程

**前置**（缺一不得进入步骤 2）：`submit_verdict` 退出码 ≠ 1；prod 实测 < 0.7；用户明确确认；当日 REGULAR 配额未满（`python tools/quota_status.py`）。

**步骤 1 · 预检（默认形态，不 POST）**

```
mcp__wq-brain-http__workflow_submit_alpha(
  alpha_id="<ALPHA_ID>",
  name="IND_R_pvrevgate_01",   # <REGION>_<R|S>_<family>_<seq>；R=REGULAR、S=SUPER；勿放 PROD 数值
  tags=["CH_REG", "SRC_insiders1", "W113"],
  descriptions="Idea: <idea>\n\nRationale for data used: <rationale>\n\nRationale for operators used: <rationale>",
  confirm_submit=False         # 只预检 + 查状态；color 缺省由节点取 BLUE
)
```

**步骤 2 · 提交（仅在用户明确确认后；不可逆）**：同参数把 `confirm_submit` 置 `True`，再按下面的「响应处置」分支。`verify_timeout` 缺省 = `WAIT_THRESHOLDS.submit_flip_wait_s`（240 s），不要自己改小。
**稳健性声明（2026-10-04 起 MCP 入口可直接传）**：`confirm_submit=True` 时，台账 `robustness_<alpha_id>` 无记录就**必须**显式 `robustness_audited=True`（缺省 False，fail-closed）才放行；台账已有记录则该声明降为辅助（`REJECT` 由节点直接拦下）。顺序：先跑 `brain-alpha-robustness` 并把结论落台账，再提交——不要只靠声明过关。`allow_prod_above_07` **不**在快捷入口里：prod 红线豁免须用户明确指令，显式走 `workflow_execute(node="submit_alpha", params={…, "allow_prod_above_07": True})` 留痕。
`force=True` 只跳过**本地预检**（内容与允许场景见 `references/ppa-handoff.md` §1），**不放行任何平台检查**；REGULAR 一般不用。

**步骤 3 · 核验**：`mcp__wq-brain-http__get_alpha_details(alpha_id=…)` → `status == ACTIVE`（或 `SUBMITTED` 后转 `ACTIVE`）且 `dateSubmitted` 非空。

MCP 不可用时的 REST 兜底见 [`references/fallback-rest.md`](references/fallback-rest.md)（同样要用户确认，凭据只读进程环境变量）。

## 响应处置（POST 的 4 种形态）

| # | 响应 | 含义 | 处置 |
|---|---|---|---|
| ① | `200` + `{"success":true,"reason":"IS checks passed","checks":[…]}` | **明确通过** | 轮询至 `status=ACTIVE` |
| ② | `201` / `202`「Accepted (async); IS checks still computing」 | **异步受理**，结果未知 | 等 `submit_flip_wait_s`；仍 `UNSUBMITTED` → **确认 `dateSubmitted` 为空后 re-POST 一次**（`submit_repost_max`）→ 再等一个窗口 → 仍未翻记 `ASYNC_STUCK`，知会用户，不再重试 |
| ③ | `200` + 「Non-JSON submit response」+ **空体** | **异步受理、结果未知** | 同 ②：**不得当成失败** |
| ④ | `403` + JSON `{"is":{"checks":[…]}}` | **失败**，零成本，回带**全量 checks 与真因** | 读唯一的 `FAIL` 项（见下） |

窗口取值（240 s / 5 s / 补发 1 次）唯一来源 = `wqb.config.WAIT_THRESHOLDS`；MCP `submit_alpha` 对 201/202 立即返回，等待与补发由 `submit_alpha` 节点负责。
若工具返回 `False` 或 `success:false` 但 HTTP 是 201/202/空体 200——那是**②③**，不是失败：按上表处置。
实证：2026-09-26 `O0GjWqeY` / `2rpX85Ax` / `np8VGNz3` 走 ②③ 后未补发，悬空 `UNSUBMITTED` > 24 h。**`regular.description` 过短是另一条独立成因**（网关静默丢弃，需补 ≥ 100 字合规嵌套描述），勿与 ②③ 混为一谈。

**403 的真因读法**：`is.checks[].result` 有 `PASS` / `FAIL` / `WARNING` / `PENDING`。**`PENDING` 不挡提交，但也不能据此放行**；真正拦阻的是 `FAIL`：
- `REGULAR_SUBMISSION: FAIL`，`value ≥ limit`（如 4/4）= **ET 日配额用尽，不是候选缺陷**——停、不判死、记待次日（`scenarios.md` S5-03）；`SUPER` / PPA 各自独立通道；
- 任一硬指标 `FAIL` / 硬闸类 `WARNING`（词义见 `GLOSSARY.md` §2.4）= 候选本身的问题，回 ra-pipeline 步 7。
`PASS_CHEAP` / 模拟层干净都**不能替代**平台实测。

## 属性规范（`src/wqb/alpha_properties.py`，规格 `docs/alpha_properties_spec.md`）

- `color`：平台**仅接受** `GREEN / BLUE / RED / YELLOW / PURPLE`（`validate_color` 拒其余）。**提交态默认 `BLUE`（待观察）；`GREEN` 须由 OS 结果挣得，禁当默认值**；`PURPLE` 仅 PPA。MCP 工具与节点的缺省都是 `None → BLUE`。
- `name`：`<REGION>_<R|S>_<family>_<seq>`（`build_name`；PPA 是 REGULAR 型，也用 `R`）。**禁止放 PROD 数值**（提交时快照，会过期骗人）。手写 name 不被强制校验，须自觉遵守。
- `tags`：`CH_<通道>` + `SRC_<数据集>` 必打，可选 `W<波次>` / `EXPRFAM_<族>` / `CORR_<档>`；**上限 5 个**（`MAX_TAGS`）。缺省由节点按规范自动生成，`check_tags` 只告警不强制。**`PowerPoolSelected` 仅真实 PPA 通道**（普通提交用 `CH_REG`）。平台已自带的（塔、类型、区域、作者、`stage`）不要重复打。
- `description`：`set_alpha_properties` 已封装嵌套写法 `{"regular":{"description":…}}`（扁平写法被 `400 Unexpected property.`）；三段式，各段 ≥ 100 词。SUPER 的 description 写法见 `wq-brain-superalpha`。

## 终态与验收

| 状态 | 判据 | 动作 |
|---|---|---|
| **成功** | `status ∈ {ACTIVE, SUBMITTED→ACTIVE}` 且 `dateSubmitted` 非空 | 回写 S6，重跑 `campaign_intel.py pyramid` 看塔 +1 |
| **未决** | 仍 `UNSUBMITTED`、窗口内 | 继续轮询；窗口满走补发（表 ②） |
| **卡住** | 补发后再等一个窗口仍 `UNSUBMITTED` | 记 `ASYNC_STUCK`，**知会用户，不再重试**；> 24 h 仍未翻由用户在平台上查 |
| **失败** | 403 有 `FAIL` | 按真因处置（上节）；配额类不判死 |
| **已提交** | `status` 已是 `ACTIVE` / `SUBMITTED` | **不要再 POST**（`submit_verdict` 退出码 11）；重复 POST 是否扣配额没有实测结论，故不做。提交后再取 `is.checks` 只会看到 `ALREADY_SUBMITTED: FAIL`（表示不可重复提交，属正常，原检查结果已锁定） |

## 失败分支（症状 → 判据 → 处置）

| 症状 | 判据 | 处置 |
|---|---|---|
| 提交后一直 `UNSUBMITTED` | 201 / 202 / 空体 200 | ②③：等窗口 → 确认 `dateSubmitted` 空 → 补发一次 |
| 403 `REGULAR_SUBMISSION` | `value ≥ limit` | 配额用尽：停，不判死，待次日 |
| 403 其他 `FAIL` | `is.checks` 里的 FAIL 名 | 候选问题：回步 7，不要重试 |
| `workflow_submit_alpha` 预检就 `blocked` | `pre_submit_check` 未过（本地放宽筛：Sharpe > 1.3、Fitness > 0.75、Turnover 4%–40%、Returns > 4%、无 FAIL；数字见其文档串） | 合法 PPA 走 `ppa-handoff.md`；其余回修 |
| 400 `Unexpected property` | 扁平 description | 用嵌套写法（`set_alpha_properties` 已封装） |

## 不做什么

- **不用 POST 试探**配额或检查——通过即提交。配额复检用 `quota_status.py`。
- **不用 `GET /alphas/{id}/submit`** 做任何判定：本平台恒 `404` + 空体。
- **不用 `activities/submissions`** 判断当日配额（缺 `today` 字段）。
- **不在 201 后立刻判失败**；**不因配额 403 判死候选**；**不无限补发**。
- **不把「提交」一词用在派发仿真上**：`tools/submit_batch.py` 与 MCP `submit_batch` 是 `POST /simulations` 的**派发**，不是把 alpha 提交上平台。

## 工具

| 要做什么 | 用什么 |
|---|---|
| 否决判定（模拟层 + 资格门 + 硬闸类 WARNING） | `python tools/submit_verdict.py --alpha-id <ID> [--json]`（退出码 1 / 10 / 11，见提交链 §2.1） |
| 当日已提交颗数（ET 日） | `python tools/quota_status.py` |
| 塔现状 / 点塔优选 | `python tools/campaign_intel.py pyramid --region <R> --delay <D>`；规则见 `references/quota-and-tower.md` |
| PPA 交接与回写 | `python tools/ppa_handoff.py sheet\|record --alpha-id <ID>` |
| 提交（MCP） | `mcp__wq-brain-http__workflow_submit_alpha`（步骤 1–2） |

## SUPER 与 PPA（只给指针）

- **SUPER**：完整方法论与提交见 `wq-brain-superalpha`；提交同样受 ET 日配额（SUPER 1 / 日）约束，且**第一次通过的 POST 就是真提交**；SUPER 不点塔。
- **PPA**：独立日配额（1 / ET 日）；MCP 预检线满足者可走 MCP，其余走 web UI 人工通道——**agent 停下并交接**，见 `references/ppa-handoff.md`。

## 参考

`references/submit-chain.md`（提交链状态机、权力分层、信息来源表）· `references/quota-and-tower.md`（配额模型、点塔优选）· `references/ppa-handoff.md`（PPA 路由 / 交接 / 回写）· `references/scenarios.md`（四张情景卡）· `references/fallback-rest.md`（REST 兜底）
