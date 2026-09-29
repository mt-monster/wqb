---
name: planning-with-files
layer: L7
version: "2.1.0"
description: 文件化规划元技能：把复杂任务的过程状态写进 task_plan.md / findings.md / progress.md（磁盘即工作记忆，压缩后可恢复）。当用户明确要求做计划文件、任务跨多个会话、或没有现成的状态存储且步数很多（研究 / 大重构）时使用；WQ 挖掘任务的结果真相源在 DB 台账，不要用它替代。
last_verified: 2026-09-29
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
hooks:
  SessionStart:
    - hooks:
        - type: command
          command: "echo '[planning-with-files] Ready. Invoke with /planning-with-files when a task needs a plan file.'"
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          # 2026-09-29：只在**改文件前**回显计划头部（原为 Write|Edit|Bash 前 30 行，RA 长流程里每次 Bash 都注入）。
          # 仅当前目录有 task_plan.md 时才有输出；永远 exit 0。
          command: "bash -c 'head -n 20 task_plan.md 2>/dev/null || true'"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "echo '[planning-with-files] File updated. If this completes a phase, update task_plan.md status.'"
  Stop:
    - hooks:
        - type: command
          # 2026-09-29：原命令 `<SKILL_ROOT>/planning-with-files/scripts/check-complete.sh` 的占位符没有任何
          # 工具替换（sync_skills 不替换），Stop 钩子每次都会执行失败；且脚本在没有 task_plan.md 时报 ERROR，
          # 会在无关会话里每次 Stop 都噪声。改为**内联、无占位符、无 plan 时静默**的提醒（永远 exit 0，不阻断停止）。
          command: "bash -c 'f=task_plan.md; [ -f \"$f\" ] || exit 0; t=$(grep -c \"### Phase\" \"$f\"); c=$(grep -cF \"**Status:** complete\" \"$f\"); if [ \"$t\" -gt 0 ] && [ \"$c\" -ne \"$t\" ]; then echo \"[planning-with-files] task_plan.md: $c/$t phases complete - finish or update the plan before stopping\" >&2; fi; exit 0'"
---

# 文件化规划（Planning with Files）

## 职责边界

- **本 skill 负责**：复杂任务的**文件化规划**——`task_plan.md` / `findings.md` / `progress.md` 三件套，记录**过程与决策**，让上下文压缩后能恢复。
- **本 skill 不做**：不涉及任何 WQ 平台调用、不读写 `data/wqb.db`、不改 skill；**不替代 DB 台账**——WQ 挖掘任务的**结果**真相源是 DB 台账（`wave_results` / `registry_empirical` / ledger 键），规划文件只是过程笔记，**不是战役产物**。
- **上游 / 下游**：通用元技能，**与 WQ 技能链没有依赖**（不共用 `$WQ_PY`，也不调用任何 WQ 工具）；优先级见下「与领域协议的关系」。
- **来源**：外部开源「Manus 风格规划」skill 的中文化改编（`version: "2.1.0"` 是其上游版本号，与本库 `last_verified` 无关）。**上游地址与许可未在仓库内登记**——待人补充。

像 Manus 一样工作：使用持久化的 markdown 文件作为你的「磁盘上的工作记忆」。

## 何时使用（一个口径）

- **用**：用户明确要求做计划 / 用文件跟踪；任务**跨多个会话**；**没有现成的状态存储**且步数很多（研究、构建、大重构）。
- **不用**：简单问题、单文件编辑、快速查找；**WQ 流水线任务**（RA 九步等）——它们的状态已在 DB 台账 / 各 skill 的检查点里，再建计划文件是重复记账。
- **用户说「直接改，别写计划」** → 遵从用户，不建计划文件（可只在回复里列步骤）。

## 与领域协议的关系（优先级）

**用户当次指令 > 领域协议（RA / submit-alpha 等各 skill 与 AGENTS.md） > 本 skill。** 具体地：

- 结果、判定、台账写入以领域协议为准，规划文件里只记「做了什么、为什么」；
- 本 skill 的「先建计划」「两动作规则」「3 次失败上报」都是**默认习惯**，与领域协议冲突时让位（见下「失败处理」）。

## 文件放哪里

- **模板**在 skill 目录 `Claude/skills/planning-with-files/templates/`（安装位同名目录）。
- **你的规划文件**建在**仓库根**：`/task_plan.md`、`/findings.md`、`/progress.md`——这三个路径已被 `.gitignore` 忽略（在 `tracking/<REGION>/` 等子目录里工作时也写回仓库根，`git rev-parse --show-toplevel` 取根，避免在子目录产生未忽略的文件污染 `git status`）。云端 / 只读受限的会话改写到会话的 scratchpad 目录。
- 下面的**钩子只看当前目录**的 `task_plan.md`：不在仓库根时钩子静默、不影响使用。

## 钩子（frontmatter `hooks:`）到底做什么

本 skill 是全库**唯一**允许声明 `hooks:` 的 skill（`tests/unit/test_skill_hooks_and_tools_guard.py` 的白名单）。钩子 = 在 agent 生命周期事件上自动执行的命令，所以逐条写明：

| 事件 | 命令做什么 | 成本 / 风险 |
|---|---|---|
| SessionStart | `echo` 一行提示 | 无 |
| PreToolUse（仅 `Write|Edit`） | 有 `task_plan.md` 时回显其前 20 行，否则静默 | 有计划文件时每次改文件前多 20 行上下文；**不再**在 Bash 前触发 |
| PostToolUse（`Write|Edit`） | `echo` 一行提醒更新阶段状态 | 每次改文件多 1 行 |
| Stop | 内联脚本：有计划文件且阶段未全部 `complete` 时向 stderr 提醒 | **永远 `exit 0`**，不阻断停止 |

全部是 POSIX 命令（`bash`、`head`、`grep`）；无 bash 的宿主上钩子会报错但**不阻断**，可以直接删掉 frontmatter 里的 `hooks:` 块。手动校验脚本：`scripts/check-complete.sh`（无计划文件时 `exit 1`，只用于手动检查，不接钩子）。

## 快速上手

1. 在仓库根创建 `task_plan.md`——参考 [templates/task_plan.md](templates/task_plan.md)（一次 WQ 战役的填好示例见 [references/wq-examples.md](references/wq-examples.md)）；
2. 创建 `findings.md`（[模板](templates/findings.md)）与 `progress.md`（[模板](templates/progress.md)）；
3. **决策前重读计划**——让目标保持在注意力窗口内；
4. **每个阶段完成后更新**——标记完成、记录错误。

## 核心模式

```
上下文窗口 = 内存（易失、有限）
文件系统 = 磁盘（持久、无限）

→ 任何重要的过程信息都写入磁盘。
```

| 文件 | 用途 | 何时更新 |
|------|---------|----------------|
| `task_plan.md` | 阶段、进度、决策 | 每个阶段之后 |
| `findings.md` | 研究、发现 | 每次有新发现之后 |
| `progress.md` | 会话日志、测试结果 | 会话期间持续更新 |

## 关键规则

1. **复杂任务先建计划**（满足上面「何时使用」时）；用户明确不要计划则例外。
2. **两动作规则**：每执行 2 次查看 / 浏览 / 搜索操作后，把关键发现存进文本文件——防止视觉 / 多模态信息丢失。
3. **先读再决定**：重大决策前先读计划文件。
4. **行动后更新**：完成阶段后标记 `in_progress` → `complete`，记录遇到的错误与新建 / 修改的文件。
5. **记录所有错误**：每个错误写进计划文件，积累知识、避免重蹈覆辙。

```markdown
## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | Created default config |
| API timeout | 2 | Added retry logic |
```

## 失败处理（区分「确定性失败」与「暂时性失败」）

**「失败」的粒度**：同一目标动作的一次无效尝试（一次工具调用 / 一条命令）。波次级、构造级的失败计数由领域协议管（RA 停止规则、optimization-v1 的止损阶梯等），**不在本 skill 内**。

| 失败类型 | 规则 |
|---|---|
| **确定性失败**（同样的输入必然再败：语法错、参数错、文件不存在、权限拒绝） | **不重复**同一动作：换方案（下面的 3 次协议） |
| **暂时性失败**（429 限流、`GET correlations/prod` 空体轮询、`PENDING` 等待、异步受理后按提交协议的补发） | **按各 skill 的协议重试**（退避 / 轮询间隔 / 补发护栏），不算「重复失败」——例如 429 退避后同一请求重试是规定动作 |

**3 次协议（只用于确定性失败）**

```
第 1 次：诊断与修复 —— 仔细读错误、找根因、针对性修复
第 2 次：换一种方法 —— 同样的错误就换方案 / 换工具，不重复完全相同的失败动作
第 3 次：更大范围反思 —— 质疑假设、搜索解决方案、考虑更新计划
3 次失败后：上报给用户 —— 说明尝试过什么、分享具体错误、请求指导
```

## 读 vs 写决策矩阵

| 场景 | 动作 | 原因 |
|-----------|--------|--------|
| 刚写完文件 | 不要读 | 内容仍在上下文中 |
| 查看了图片 / PDF | 立即写入发现 | 多模态 → 在丢失前转成文本 |
| 浏览器返回数据 | 写入文件 | 截图不会持久保存 |
| 开始新阶段 | 读取计划 / 发现 | 若上下文过期则重新定位 |
| 发生错误 | 读取相关文件 | 需要当前状态才能修复 |
| 间隔后恢复 | 读取所有规划文件 | 恢复状态 |

## 五问重启测试

| 问题 | 答案来源 |
|----------|---------------|
| 我在哪里？ | task_plan.md 中的当前阶段 |
| 我要去哪里？ | 剩余阶段 |
| 目标是什么？ | 计划中的目标陈述 |
| 我学到了什么？ | findings.md |
| 我做了什么？ | progress.md |

**WQ 场景的填好示例**（RA 步 4 GEM 生成被压缩打断后恢复）：「我在哪里」← `task_plan.md` 里 `### Phase 4` 的 `in_progress`；「我要去哪里」← Phase 5–9；「目标」← 计划头部的「KOR fundamental17 开第 190 波」；「学到了什么」← `findings.md` 的闸 SEM 结论与 priors 快照日期；「做了什么」← `progress.md` 的命令与产物路径——**结果**（这波已入库多少条表达式、闸结果）则以台账为准：`mcp__wqb-db__get_wave_result` / `list_expressions`，**不**以规划文件为准。

## 情景卡

### 情景 PW-1　一次 RA 战役的计划

- **前置状态**：用户要求开一次 RA 战役并要求「用计划文件跟踪」。
- **步骤**：仓库根建 `task_plan.md`：阶段 = 九步（S-PRE → S6，参见 [references/wq-examples.md](references/wq-examples.md)），每个阶段写「产物落在 DB 的哪个键 / 表」作为检查点；`findings.md` 只记决策与证据来源；每个阶段完成后更新 `task_plan.md`，并**同时**按 RA 的完成定义写台账。
- **完成定义**：计划里每个阶段的检查点都能在台账里查到对应记录。
- **反例**：把这波的表达式清单、回测指标写进 `progress.md` 当作真相源（会与 `backtest_results` 漂移）。

### 情景 PW-2　长任务被压缩后恢复

- **步骤**：五问 → 读 `task_plan.md` 找当前阶段 → 读 `findings.md` / `progress.md` → 读台账核对**结果**（`get_wave_result` 等）→ 继续。
- **分支**：计划与台账不一致 → 以台账为准，并在 `progress.md` 记一行差异原因。
- **完成定义**：五问都能答，且答案来源写得出。

### 情景 PW-3　用户说「直接改，别写计划」

- **动作**：遵从用户——不建计划文件。需要保留过程记录时，用回复里的简短步骤列表；会话内待办用宿主的 Task 工具。
- **反例**：坚持「没有 `task_plan.md` 就不动手」（用户当次指令优先）。

## 模板与脚本

- 模板：[templates/task_plan.md](templates/task_plan.md)（阶段跟踪）、[templates/findings.md](templates/findings.md)（研究存储）、[templates/progress.md](templates/progress.md)（会话日志）。
- 脚本（**bash**；Windows 需 Git Bash / WSL）：`scripts/init-session.sh` 初始化三个文件；`scripts/check-complete.sh` 校验阶段是否全部完成。`check-complete.sh` 靠 `### Phase` 与 `**Status:** complete` 两个字符串计数，**与模板文本强耦合**——改了模板格式就会失效。
- 高级：Manus 原则见 [reference.md](reference.md)；真实示例见 [examples.md](examples.md)。

## 反模式

| 不要这样做 | 应该这样做 |
|-------|------------|
| 把 WQ 战役的结果记在规划文件里当真相源 | 结果写 DB 台账；规划文件只记过程与决策 |
| 用 TodoWrite / Task 工具做跨会话持久化 | **会话内**用 Task 工具跟踪待办，**跨会话**状态用规划文件（或 DB 台账）——二者互补，不互斥 |
| 目标只陈述一次就忘记 | 决策前重读计划 |
| 隐藏错误并静默重试 | 将错误记录到计划文件 |
| 对暂时性失败（429 / 空体 / PENDING）套「永不重复」 | 按各 skill 的重试协议；只有确定性失败才「换方案」 |
| 把所有东西塞进上下文 | 把大段内容存到文件里 |
| 在 skill 目录 / 子目录创建规划文件 | 建在仓库根（已 gitignore） |
