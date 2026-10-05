# PPA（Power Pool）提交：路由、人工交接与回写

> PPA 是**独立日配额**（`POWER_POOL_SUBMISSION` limit=1 / ET 日），与 REGULAR 4 / 日、SUPER 1 / 日并行不互占；每天先提 PPA 那颗是既定纪律。
> 但它有一条 agent 走不了的人工通道。本文规定**走哪条路、什么时候停下交接、用户提交后怎么落账**。来源：SB-07 / SB-08 / SB-22 / SB-23。

## 1. 路由：MCP 还是 web UI

MCP 的 `workflow_submit_alpha` / `submit_alpha` **不是 PPA 感知的**：它内置本地预检（`pre_submit_check`）——Sharpe > 1.3、Fitness > 0.75、
Turnover 4%–40%、Returns > 4%、其余 IS checks 无 FAIL；**Margin 只是 warning**（平台不检 margin）。该预检不看 `PowerPoolSelected` 标签，
所以合法但指标较低的 PPA 会被它拦下。这些是刻意放宽的**本地**筛（不是平台线，数字见 `wqb.config.PLATFORM_CHECK_LINES` 与 `pre_submit_check` 文档串）。

| 候选 | 走哪条 |
|---|---|
| 满足上面的本地预检 | 可走 MCP：`workflow_submit_alpha(color="PURPLE", tags=["CH_PPA", "SRC_<数据集>", "PowerPoolSelected"], confirm_submit=…)`，其余规则同 REGULAR（提交链 `submit-chain.md`） |
| 不满足（如合法 PPA 的 Sharpe ∈ [1.0, 1.3)） | **web UI 人工通道**（仅当期活跃 Power Pool 主题窗口内；`MATCHES_THEMES` = PASS 才受理；非活跃区域报 "does not match any Power Pool Theme"）→ **agent 停下并交接**，见 §2 |

> `force=True` 只跳过本地预检，**不放行任何平台检查**。允许场景仅两类：合法 PPA（Sharpe 低于预检线）、SUPER；其余一律不用。

## 2. 交接（agent 在这里停下）

```
python tools/ppa_handoff.py sheet --alpha-id <ALPHA_ID> [--ppac <本地算出的 PPAC>]
```

输出交接单：候选 id / 区域 / 表达式 / IS 指标 / **PPA 资格门（Failed PPA、名单内 PENDING）** / 算子与字段计数，以及**必须由人核对**的项：
PPAC（本地 `brain-calculate-alpha-selfcorr-quick`，≤ 0.5 才走 PPA 通道）、当期主题窗口、已准备好的属性（name / color `PURPLE` / tags / 三段式 description）。
判据数字（Sharpe ≥ 1.0、算子 ≤ 8、字段 ≤ 3、PPAC < 0.5）来自平台 Power Pool 规则的文档记载，**本环境未向平台复核**，以当期平台规则为准。

**用户不在线时的默认动作**：候选留在提交队列（`submit_ready`，status 不变），不重复催，也**不改走 MCP 通道**。

## 3. 回写

用户说「已在 web UI 提交」后：

```
python tools/ppa_handoff.py record --alpha-id <ALPHA_ID>
```

先向平台核验 `status ∈ {ACTIVE, SUBMITTED}` 且 `dateSubmitted` 非空（翻转可能有 2–3 分钟延迟），核验过才写 `submission_ledger`（`submission_type=PPA`）；核验不过 **不写**（exit 1）。
之后照常走 S6（`wq-backtest-monitor` §14）。
