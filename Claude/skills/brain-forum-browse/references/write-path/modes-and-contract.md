# 运行模式与 Run Contract（modes & contract）

> **休眠**（写路径）：只在 MCP 有论坛写工具时适用，见 [README.md](README.md)。

> **休眠**：只在 MCP 有论坛写工具时适用，见 [README.md](README.md)。当前环境只读，explore 的现役流程见 [../../SKILL.md](../../SKILL.md) §3。

## 1. 四种模式

| 模式 | 用户典型说法 | 做什么 | Run Contract? |
|------|--------------|--------|---------------|
| **explore**（有写工具时的缺省） | 逛一逛、看看、转转 | MCP 搜读 → **必贡献** → Auto-Send E1，或 Phase 7.5 + Run Contract → 执行 | **单条 E1 写可免**；否则必做 |
| **contribute** | 贡献、填空白、跟评、发帖、点赞 | 完整 Recon → gap → 更严的写计划 + **必 curator** → Phase 7.5 → Run Contract → 同意执行 | **必做** |
| **recon** | 流水线卡住要查论坛 | 经 `tools/forum_recon.py` 只读检索，入库（含负结果）——见 [../../SKILL.md](../../SKILL.md) §5 | **免**；也免贡献义务、免工作区记忆 |
| **hybrid**（已弃用别名） | 逛一逛顺便看看要不要回 | 等同 explore | 同 explore |

有写工具且用户只说「逛论坛」、未提贡献 → `explore`（仍须以贡献收尾）。禁止：浏览后「你想先做哪一项？」菜单、零贡献的纯读会话、把不合格草稿硬 auto-send。

## 2. 贡献义务决策树（唯一表述）

```
MCP 是否提供论坛写工具（create_forum_comment / create_forum_post / upvote_forum_comment）？
├─ 是 → 每次 explore / contribute 会话必须以 ≥1 个写操作结束（每轮写操作数 ∈ [1, 3]）。
│        每次写必须含**独特个人价值**（E1 / E2 / E3 支撑），不复读楼主 / 热评。
│        确实无话可说：在 stroll notes 记录原因，仍可发**linker**——但 linker 只有一个条件：
│        本轮有 E2（MCP 读到的帖）**且**有明确的索引理由；不允许「硬发一条链接」。
└─ 否 → 休眠：没有贡献义务。会话降级为只读 explore（SKILL §3），在笔记里注明「无写工具」。
```

最低贡献条（有写工具时）满足其一：**≥1 个有证据支撑的写操作**（评论或新帖，每条论断追溯到 E1 / E2 / E3），或**明确的用户批准计划**（评论 + curator 点赞组合）。

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

**Gate：** 未通过对抗审查的草稿不得写入合同。Curator：contribute 合同默认含 ≥1 upvote；explore 值得时推荐含 ≥1 upvote。

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
