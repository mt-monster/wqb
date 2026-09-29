# 提交链：可达状态机 · 权力分层 · 不可逆动作块

> 本文是「一颗 alpha 从模拟结果走到平台 ACTIVE」的**唯一叙述**。其他 skill / 文档写「提交判定」时只许引用本文，不再自述一套。
> 词汇（否决权威 / 放行权威、dispatch / submit、FAIL / PENDING / WARNING）见 [`GLOSSARY.md`](../../GLOSSARY.md)。
> 来源：`reports/skills_review_20260929.md` X-2、X-9、SB-03 / SB-13 / SB-14。

## 0. 不可逆动作块（本链唯一的不可逆一步）

> ⚠ **不可逆：`POST /alphas/{id}/submit`——通过即提交，无撤回。** 平台把它同时当「提交」和「提交前检查」，所以**没有零成本的 POST 探测**：
> 任何一次「试探性 POST」只要全过，就是一次真提交。
> **前置（缺一不得执行）**：① `submit_verdict` 不是 `BLOCKED`（§2 步 2）；② 资格门 Failed RA / PPA = 0（步 1）；③ `check_correlation(alpha_id, refresh=True)`
> 实测 prod < 0.7（步 3）；④ **用户明确确认**（步 5）；⑤ 本 ET 日 REGULAR 配额未满（`python tools/quota_status.py`）。
> **默认形态（预检 / 干跑）**：`workflow_submit_alpha(alpha_id=…, confirm_submit=False)`——只做本地预检并查状态，不 POST。
> **需要用户明确确认**：是（`confirm_submit=True`、`super_build.py submit`、PPA 走 web UI 都一样）。
> **执行后必须核验**：`get_alpha_details` → `status == ACTIVE` 且 `dateSubmitted` 非空。**异常**：见 §4；不盲重试，仅「异步受理未翻转」可补发一次。

## 1. 权力分层：否决权威 ≠ 放行权威

| 权力 | 谁 | 能做什么 |
|---|---|---|
| **否决权威** | 资格门、`submit_verdict`、prod 实测、稳健性闸 | **只能拦，不能放**。任何一个说「不」就停 |
| **放行权威** | **用户明确确认** + `workflow_submit_alpha(confirm_submit=True)` | 唯一能让 POST 发生的路径；不可逆 |

因此「`submit_verdict` 说了算」只对否决成立：它说 `BLOCKED` 就不提交；它说 `UNVERIFIABLE`（现实中最好的结果）**不是放行**，后面还有 prod 实测和用户确认。

## 2. 可达状态机

| 步 | 判定 | 权力 | 入口 | 结果 | 可逆 |
|---|---|---|---|---|---|
| 1 | **资格门**：`Failed RA == 0`（PPA 看 `Failed PPA`）；名单内若仍有 `PENDING`，`Failed=0` 只表示「暂无失败」，**待其算完再判** | 否决 | `wqb.config.compute_webdata_failed_counts`（`submit_verdict` 已内含；输出里的 `pending_ra` / `pending_ppa`） | 非零 → 回 ra-pipeline 步 7 修 | 是 |
| 2 | **模拟层 + 硬闸类 WARNING**：`is.checks` 无 FAIL；`LOW_FITNESS` / `LOW_SHARPE` / `LOW_2Y_SHARPE` 的 WARNING 视同 FAIL | 否决 | `python tools/submit_verdict.py --alpha-id <ID>`（或 MCP `submit_verdict`；同一份实现 `wqb.submit_verdict_core`） | 见 §2.1 退出码 | 是 |
| 3 | **prod 实测 < 0.7**（`GET correlations/prod`，账号级单并发；忙时立即返回 `correlation_busy`，阻塞轮询窗口见 `WAIT_THRESHOLDS`） | 否决 | `mcp__wq-brain-http__check_correlation(alpha_id, refresh=True)`；SUPER 用 `super_build.py probe` | ≥ 0.7 → prod 墙决策表（ra-pipeline `decision-table.md` D0） | 是 |
| 4 | **稳健性闸** | 否决（**有代码读取**：结论落台账 `robustness_<alpha_id>`，`submit_verdict` 三入口读它——`REJECT` → `BLOCKED`；`CONDITIONAL` / 无记录只在 `next_step` 提示，不拦） | brain-alpha-robustness | `REJECT` → 停 | 是 |
| 5 | **用户明确确认** | 放行的必要条件 | 人 | 未确认 → 停在这里，列出候选与证据交用户 | 是 |
| 6 | **提交** `workflow_submit_alpha(confirm_submit=True)` | **放行（不可逆）** | 本 skill §4 四态表 | 200 = 已提交；201 / 202 / 空体 200 = 异步受理 | **否** |
| 7 | **轮询与补发**：等状态离开 `UNSUBMITTED`；窗口内未翻 → 补发一次 → 再等一个窗口 → 仍未翻记 `ASYNC_STUCK` 并知会用户 | — | 窗口取 `WAIT_THRESHOLDS`（`submit_flip_wait_s` / `submit_flip_poll_s` / `submit_repost_max`） | `ACTIVE` = 完成 | — |
| 分支 | **PPA**：MCP 预检线不满足的合法 PPA 走 web UI 人工通道，agent 停下并交接（`ppa-handoff.md`）；**SUPER**：`super_build.py submit` 默认带 prod 闸（`--allow-prod-above-07` 才豁免），且**第一次通过的 POST 就是真提交**，不是「预检」 | | | | |

### 2.1 `submit_verdict` 状态与退出码

| verdict | 含义 | 退出码 | 下一步 |
|---|---|---|---|
| `BLOCKED` | 模拟层 FAIL / 硬闸类 WARNING / Failed-count 非零 / 提交层 403 / 未知响应 | **1**（未捕获异常同样 1：fail closed） | 修复并重新回测；**不绕过**（`force`、直接 POST 探测都不可取） |
| `UNVERIFIABLE` | 模拟层干净，但提交层没有信息（`GET /submit` 恒 404） | **10** | 走步 3；**不是放行** |
| `ALREADY_SUBMITTED` | 已 `ACTIVE` / `SUBMITTED` | **11** | 不要再 POST；如需回写走 S6 |
| `SUBMITTABLE` | 模拟层干净且 `GET /submit`=200 | 0 | **现实中不会出现**（GET 恒 404），仅防御分支；文档与上游条件不得写「等 SUBMITTABLE」 |

以 `$?==0` 放行的脚本是错的：UNVERIFIABLE 曾经也是 0（2026-09-29 前）。路由请读退出码，且**只把 1 / 10 / 11 当作有信息的结果**。

## 3. 提交层信息来源：各能回答什么、会不会真提交

| 来源 | 能回答 | 会真提交吗 |
|---|---|---|
| `GET /alphas/{id}/submit` | **什么都回答不了**：本平台恒 `404` + 空体（2026-09-26 实测：未提交与已 ACTIVE 的同样 404）。不要用它做任何判定 | 否 |
| `POST /alphas/{id}/submit` | 提交层真相：200 / 201·202 / 403（带全量 `is.checks` 与真因） | **是——通过即提交** |
| `get_alpha_details(alpha_id).is.checks` | 模拟层各检查的 `PASS` / `FAIL` / `WARNING` / `PENDING`；`status` / `dateSubmitted` | 否 |
| `submit_verdict` 输出 | 上面两类模拟层信息 + 资格门 + 硬闸类 WARNING 的合成判定（**否决**用） | 否 |
| `check_correlation(refresh=True)` | prod / self 相关性实测（异步排队，已决结果缓存 7 天；终验用 `refresh=True`） | 否 |

> 「提交层视图」一词只指第一行那个死端点；其余都直接说来源名。

## 4. 与本链相关的必读细节（不重复正文）

- **POST 四态表 / 补发护栏 / 配额 403** → [`../SKILL.md`](../SKILL.md)「响应处置」与 [`scenarios.md`](scenarios.md)。
- **配额模型（ET 日历日、来源、复检）与点塔优选** → [`quota-and-tower.md`](quota-and-tower.md)。
- **PPA 人工交接单** → [`ppa-handoff.md`](ppa-handoff.md)。
- **MCP 不可用时的 REST 兜底** → [`fallback-rest.md`](fallback-rest.md)（凭据只读进程环境变量，不读 `.env`）。
