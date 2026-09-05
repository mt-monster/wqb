# 运行模式与 Run Contract（modes & contract）

> 合并自 run-modes.md / run-contract.md / auto-send-e1.md（2026-08-18 精简）。

## 1. 三种模式

「逛一逛论坛」**默认 = explore stroll-with-mandatory-contribution** — 有方向地逛或先逛后定方向，**每轮必须以贡献收尾**。禁止浏览后菜单与零贡献纯 read 会话。

| 模式 | 用户典型说法 | 做什么 | Run Contract? |
|------|--------------|--------|---------------|
| **explore**（默认） | 逛一逛、看看、转转 | MCP 搜读 → **必贡献** → **auto-send E1** 或 7.5+Contract → 6–9 | **单条 E1 write 可免**；否则必做 |
| **contribute** | 贡献、填空白、跟评、发帖、点赞 | 完整 Recon → gap → 更严 write 计划 + **必 curator** → Phase 7.5 → Run Contract → 同意执行 | **必做** |
| **hybrid**（弃用别名） | 逛一逛顺便看看要不要回 | **等同 explore**，行为不变 | 同 explore |

**默认规则：** 用户只说「逛论坛」且未提贡献 → `explore`（仍必须以贡献收尾）。

## 2. 最低贡献条（explore 每轮必达，硬性）

每次「逛一逛论坛」会话必须以 ≥1 个论坛写操作结束。每次写必须含**独特个人价值**（P0–P5，含本机 AI 对话史），不复读楼主/热评。满足至少其一：

1. **≥1 证据支撑的写操作** — 评论或新帖，每条论断追溯到 E1/E2/E3。
2. **明确的用户批准计划**，含评论 + curator 点赞组合。

**若确实无话可说：** 在 stroll notes 记录原因，仍尝试 linker 式最小价值（链接/索引指路/窄问题回复），避免空会话。

**贡献义务决策树：** MCP 有写工具 → 必贡献；无写工具（如 wq-brain-http 仅只读）→ 自动豁免降级只读，须在 session_plan / stroll_notes 注明豁免原因。

## 3. explore 子风格

- **purposeful stroll**：起步即有方向（P5/`get_user_alphas`、`get_messages`/`get_events`、置顶帖、P0–P4、本轮聊天上下文）。
- **emergent-purpose stroll**：起步无 agenda，先逛后定方向，逛出 finds 后记录 emerged contribution plan（必有一项 write）。

**explore vs contribute：** 同必贡献，不同严格度——explore 不要求 upfront formal gap、curator 仅推荐；contribute 完整 gap 评分 + Role Pick + 必 curator。

## 4. Run Contract（标准 write 路径）

**何时需要：** 本轮 MCP write **未**满足 §5 auto-send E1 全部条件时（多条 write、upvote、linker、含 E2/E3、含建议/推断/提问、或对 E1 纯事实复述无把握）。

**Forbidden UX（所有模式）：** 浏览后「你想先做哪一项？」菜单；让用户挑顺序；零 write 直接结束；把不合格草稿强行 auto-send。

**流程：**
```
Block 1 — Context: Phase 0–1 (+ contribute 时 Phase 2–5 Recon)
Block 1.5a — Auto-send E1? A1–A8 全过 → MD→HTML → 聊天贴 HTML 预览 → Phase 9（单条）
Block 1.5b — Draft + Phase 7.5: evidence + adversarial subagent（标准路径）
Block 2 — Run Contract: Phase 1.5 — STOP for 同意执行 / 修改 / 取消 (PASS drafts only)
Block 3 — Execute: Phase 6–9 — auto after 同意执行, no per-item menu
```

**合同必填：** 依据（memory + history + 为何此刻写）；搜/读/评/赞/帖计划 + 完整中文草稿；每条草稿含 `evidence_sources[]` + `adversarial_review_status: pass`；结尾 `同意执行` / `修改：…` / `取消`。

**Gate：** 未通过对抗审查的草稿不得写入合同。Curator：contribute 合同默认含 ≥1 upvote；explore 推荐含 ≥1 upvote when merited。

## 5. Auto-Send E1（单条 write 免 Run Contract）

当且仅当草稿**完全是可核验的一手经验复述**时，可跳过 Run Contract 与 Phase 7.5 subagent，直接 MCP write。任一条件不满足 → 立刻回退标准路径。

**硬性条件（A1–A8 全过）：**
- A1 恰好 1 条 write（comment 或 post，不含 upvote）
- A2 E1-only + 独特（≥1 条 thread 未覆盖的个人细节）
- A3 E1-only sources（本轮 `get_user_alphas` / P1 / P0 ledger / P4 本机 AI 对话）；禁 E2/E3 作正文论据
- A4 零推断（禁建议/推荐/可能/应该/试试/更好等词）
- A5 第一人称过去/现在事实，不评价楼主方案对错
- A6 含 alpha 指标时本轮必须已调 `get_user_alphas`
- A7 不用跟评主文向楼主提问
- A8 新帖额外：saturation ALLOW，标题为「经验记录」非教程

**Upvote 永不 auto-send。**

**自检清单（写前必过）：** A1–A8 全满足；每个数字能在 get_user_alphas 或 P1/ledger 一一对应；删除所有对他人建议句（删后无实质内容则改 Contract）；已 MCP read 目标帖；新帖 saturation ALLOW 已记录；有任何犹豫 → fallback_to_contract。

**执行流程：** 评估资格 → PASS：写 certification → MD→HTML → 聊天贴 HTML 预览 → Phase 9 write（1 条）→ 汇报。FAIL：Phase 7.5 → Run Contract → 同意执行 → Phase 9。同轮若还计划第 2 条 write 或 upvote → 整条按标准 Contract。

**日志必填（session_plan.md）：** `auto_send_e1: {eligible, certification: pass|fallback_to_contract, reason_if_fallback, write_type, post_id, e1_pointers[]}`。`action_ledger.json` 标 `auto_send_e1: true`。

## 6. Config

- `default_run_mode: "explore"`；`consent_mode: "upfront_batch"`（auto-send 为窄例外）
- `auto_send_e1: {enabled: true, max_writes: 1, require_get_user_alphas_this_run: true}`
