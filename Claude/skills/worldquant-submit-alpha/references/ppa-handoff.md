# PPA（Power Pool）提交：路由、人工交接与回写

> PPA 是**独立日配额**（`POWER_POOL_SUBMISSION` limit=1 / ET 日），与 REGULAR 4 / 日、SUPER 1 / 日并行不互占；每天先提 PPA 那颗是既定纪律。
> 但它有一条 agent 走不了的人工通道。本文规定**走哪条路、什么时候停下交接、用户提交后怎么落账**。来源：SB-07 / SB-08 / SB-22 / SB-23。

## 1. 路由：MCP 还是 web UI

> **2026-10-02 口径更新**：旧的 `pre_submit_check`（Sharpe > 1.3、Fitness > 0.75、Turnover 4%–40%、Returns > 4%、Margin 仅 warning 的**弱启发式**）
> **已于 2026-09-29 退役、2026-10-02 物理删除**（含 client mixin 里的定义、其单测与 GBR 配套检查脚本簇），
> 现在提交路由的本地闸是节点里的 `_submit_gate`（fail-closed，纯平台口径）：
> 模拟层任一 `FAIL` / 硬闸类 `WARNING`（`LOW_FITNESS`/`LOW_SHARPE`/`LOW_2Y_SHARPE`）/ `Failed RA·PPA ≠ 0`（Phase B.0 硬门）/ robustness 台账 `REJECT`
> → blocked；外加步 1.4 配额闸（ET 今日满 4 → blocked）与步 1.6 prod 闸（`check_correlation(production)`，max ≥ 0.7 或未出数 → blocked）。MCP 路径**已 PPA 感知**
> （`_is_ppa_alpha`：`type==PPA` **或** 带 `PowerPoolSelected` 标签，与 `submit_verdict_core` 统一口径），故不会再因标签缺失把合法 PPA 当 REGULAR 判错计数组。

| 候选 | 走哪条 |
|---|---|
| 过 `_submit_gate`（模拟层无 FAIL / 无硬闸 WARNING / Failed PPA = 0 / 无 REJECT）+ prod 低于 `config.GATES_PLATFORM.prod_corr_max` + 配额未满 | 可走 MCP：`workflow_submit_alpha(color="PURPLE", tags=["CH_PPA", "SRC_<数据集>", "PowerPoolSelected"], confirm_submit=…)`，其余规则同 REGULAR（提交链 `submit-chain.md`） |
| 不满足（如合法 PPA 的 IS 指标偏低但平台接受、或主题窗口需人工核对） | **web UI 人工通道**（仅当期活跃 Power Pool 主题窗口内；`MATCHES_THEMES` = PASS 才受理；非活跃区域报 "does not match any Power Pool Theme"）→ **agent 停下并交接**，见 §2 |

> `force=True` 只跳过 `_submit_gate` 本地预检，**不放行 prod 闸与配额闸**（prod 须 `allow_prod_above_07=True` 显式留痕）。允许场景极窄：确需人工覆盖本地预检时；其余一律不用。

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
