# 提交情景卡（S5）

> 每张卡：前置状态 → 步骤（命令 + 预期）→ 分支 → 产物与落点 → 完成定义 → 反例。参数以代码签名为准（`workflow_submit_alpha` 见 `world-quant-brain-mcp/tools_workflow.py`）。
> 链路与词汇见 [`submit-chain.md`](submit-chain.md)；配额见 [`quota-and-tower.md`](quota-and-tower.md)。

## 情景 S5-01　一颗 REGULAR alpha 从「判定通过」到 ACTIVE（正常路径）

- **前置状态**：候选 X（IND，`type=REGULAR`，`status=UNSUBMITTED`）；`submit_verdict` = `UNVERIFIABLE`（退出码 10，`GET /submit` 恒 404，属预期）；`Failed RA == 0` 且名单内无 PENDING；
  `check_correlation(X, refresh=True)` 实测 prod = 0.55（< 0.7）；用户已在本会话**明确确认**；`quota_status.py` 显示当日 REGULAR 未满。
- **步骤**：
  1. 预检：`workflow_submit_alpha(alpha_id=X, name="IND_R_<family>_01", tags=["CH_REG","SRC_<ds>","W<wave>"], descriptions="Idea: …\n\nRationale for data used: …\n\nRationale for operators used: …", confirm_submit=False)`
     → 预期预检通过并返回当前状态（`color` 缺省即 `BLUE`）；不通过则停。
  2. **仅在用户确认后**同参数 `confirm_submit=True`（不可逆）→ 按 HTTP 状态分支（见分支）。
  3. 核验：`get_alpha_details(X)` → `status == ACTIVE` 且 `dateSubmitted` 非空。
  4. 回写 S6（`wq-backtest-monitor` §14），并重跑 `campaign_intel.py pyramid --region IND --delay 1` 确认目标塔 +1。
- **分支**：`200 + success:true` → 直接步骤 3；`201/202` 或 `200` 空体 → 见 S5-02；`403` → 读 `is.checks` 里唯一的 `FAIL`：`REGULAR_SUBMISSION value ≥ limit` → 见 S5-03，其余 FAIL → 回 ra-pipeline 步 7。
- **产物与落点**：`wave_results.verdict`（经 `upsert_wave_result`）；`submit_ready` 表该条状态更新；OS 监控在 S6。
- **完成定义（可机检）**：`status == ACTIVE ∧ dateSubmitted ≠ null ∧ wave_results.verdict ≠ null`。
- **反例**：不要用 POST 试探配额；不要在 `UNVERIFIABLE` 时跳过 prod 实测；不要在 201 后立刻判失败；不要把硬闸类 `WARNING`（`LOW_FITNESS` / `LOW_SHARPE` / `LOW_2Y_SHARPE`）当「不挡」——它们在提交层等价 FAIL。

## 情景 S5-02　异步受理后一直没翻转

- **前置状态**：S5-01 步骤 2 返回 `201`「Accepted (async); IS checks still computing」，或 `200` + 「Non-JSON submit response」空体。二者都是**异步受理、结果未知**，**不是失败**。
- **步骤**：
  1. 每 `submit_flip_poll_s`（5 s）轮询 `get_alpha_details`，最长 `submit_flip_wait_s`（240 s，`wqb.config.WAIT_THRESHOLDS`）。`status` 离开 `UNSUBMITTED`（→ `ACTIVE` / `SUBMITTED`）即成功。
  2. 窗口内仍 `UNSUBMITTED`：**先确认 `dateSubmitted` 为空**，再 **re-POST 一次**，再等一个窗口。
  3. 仍未翻：记 `ASYNC_STUCK`，**知会用户，不再重试**。
- **分支**：补发返回 403 → 读 checks（多半是那一刻才算出的真 FAIL）→ 回 S5-01 的 403 分支；补发前发现 `dateSubmitted` 已有值 → 说明第一次其实成功了，**不要补发**。
- **产物与落点**：`ASYNC_STUCK` 记入本波 `wave_results.key_findings`（写什么见 ra-pipeline 步 9），不改 verdict。
- **完成定义**：`status ∈ {ACTIVE, SUBMITTED}` 或已记 `ASYNC_STUCK` 并通知用户。
- **反例**：不要把 ②③ 误诊成 description 过短（那是另一条独立成因：网关静默丢弃，需补 ≥100 字合规嵌套描述）；不要把 201 当失败去重跑回测；不要无限补发。
- **实证**：2026-09-26 `O0GjWqeY` / `2rpX85Ax` / `np8VGNz3` 走异步受理后未补发，悬空 `UNSUBMITTED` > 24 h。

## 情景 S5-03　403：当日配额用尽

- **前置状态**：S5-01 步骤 2 返回 403，唯一 `FAIL` 项是 `REGULAR_SUBMISSION`，`value ≥ limit`（如 4 / 4）。
- **步骤**：停；**不判死候选**；把候选原样留在提交队列，记「待次日（ET 日重置，见 `quota-and-tower.md` §1）」；告诉用户还剩哪几颗、明天按什么顺序提（点塔排序，`quota-and-tower.md` §2）。
- **分支**：SUPER（1/日）与 PPA（1/日）各自独立，REGULAR 满了不影响它们。
- **完成定义**：候选状态未变（仍 `UNSUBMITTED`），没有任何重试。
- **反例**：不要重试；不要因为 403 就淘汰候选；不要改走别的通道绕配额。

## 情景 S5-04　并行会话用光了配额

- **前置状态**：本会话已备好 3 颗候选并获用户确认，但账号配额被**另一个会话**同日用掉（2026-09-25：4 REGULAR + 1 SUPER 全被另一会话用光，本会话一颗未提）。
- **步骤**：批量提交**前 30 秒内**运行 `python tools/quota_status.py`（零成本，**不要**为复检再发 POST）→ 已满则不提交，同 S5-03；未满则按剩余额度取前 N 颗（点塔排序）。
- **完成定义**：提交前有一次 30 秒内的 `quota_status` 输出作依据。
- **反例**：不要凭会话开始时的余额提交；不要用 `activities/submissions` 判断（缺 `today` 字段）；不要用 POST 复检。
