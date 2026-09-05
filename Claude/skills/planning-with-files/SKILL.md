---
name: planning-with-files
layer: L7
version: "2.1.0"
description: 实现 Manus 风格的文件化规划，用于复杂任务。创建 task_plan.md、findings.md 与 progress.md。当开始复杂的多步任务、研究项目或任何需要 >5 次工具调用的任务时使用。
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
          command: "echo '[planning-with-files] Ready. Auto-activates for complex tasks, or invoke manually with /planning-with-files'"
  PreToolUse:
    - matcher: "Write|Edit|Bash"
      hooks:
        - type: command
          command: "cat task_plan.md 2>/dev/null | head -30 || true"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "echo '[planning-with-files] File updated. If this completes a phase, update task_plan.md status.'"
  Stop:
    - hooks:
        - type: command
          command: ".qoder-cn/skills/planning-with-files/scripts/check-complete.sh"
---

# 文件化规划（Planning with Files）

像 Manus 一样工作：使用持久化的 markdown 文件作为你的"磁盘上的工作记忆"。

## 重要：文件放哪里

使用本 skill 时：

- **模板** 存放在 skill 目录 `.qoder-cn/skills/planning-with-files/templates/`
- **你的规划文件**（`task_plan.md`、`findings.md`、`progress.md`）应创建在**你的项目目录**——即你当前工作的文件夹中

| 位置 | 存放内容 |
|----------|-----------------|
| Skill 目录（`.qoder-cn/skills/planning-with-files/`） | 模板、脚本、参考文档 |
| 你的项目目录 | `task_plan.md`、`findings.md`、`progress.md` |

这样可以确保规划文件与你的代码放在一起，而不是埋在 skill 安装目录里。

## 快速上手

在开始任何复杂任务之前：

1. **在项目中创建 `task_plan.md`** —— 参考 [templates/task_plan.md](templates/task_plan.md)
2. **在项目中创建 `findings.md`** —— 参考 [templates/findings.md](templates/findings.md)
3. **在项目中创建 `progress.md`** —— 参考 [templates/progress.md](templates/progress.md)
4. **决策前重读计划** —— 让目标保持在注意力窗口内
5. **每个阶段完成后更新** —— 标记完成、记录错误

> **注意**：三个规划文件都应创建在当前工作目录（你的项目根目录），而不是 skill 的安装目录。

## 核心模式

```
上下文窗口 = 内存（易失、有限）
文件系统 = 磁盘（持久、无限）

→ 任何重要信息都写入磁盘。
```

## 文件用途

| 文件 | 用途 | 何时更新 |
|------|---------|----------------|
| `task_plan.md` | 阶段、进度、决策 | 每个阶段之后 |
| `findings.md` | 研究、发现 | 每次有新发现之后 |
| `progress.md` | 会话日志、测试结果 | 会话期间持续更新 |

## 关键规则

### 1. 先创建计划
没有 `task_plan.md` 绝不开始复杂任务。没有商量余地。

### 2. 两动作规则
> "每执行 2 次查看/浏览/搜索操作后，立即将关键发现保存到文本文件中。"

这可以防止视觉/多模态信息丢失。

### 3. 先读再决定
在重大决策前，先读取计划文件。这能让目标保持在注意力窗口内。

### 4. 行动后更新
完成任何阶段后：
- 标记阶段状态：`in_progress` → `complete`
- 记录遇到的任何错误
- 记录新建/修改的文件

### 5. 记录所有错误
每个错误都要写进计划文件。这能积累知识、避免重蹈覆辙。

```markdown
## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | Created default config |
| API timeout | 2 | Added retry logic |
```

### 6. 永不重复失败
```
if action_failed:
    next_action != same_action
```
记录你尝试过的方法。调整方案。

## 三次失败升级协议（3-Strike）

```
第 1 次：诊断与修复
  → 仔细阅读错误
  → 找出根本原因
  → 应用针对性修复

第 2 次：换一种方法
  → 同样的错误？换不同方法
  → 换工具？换库？
  → 绝不重复完全相同的失败动作

第 3 次：更大范围反思
  → 质疑假设
  → 搜索解决方案
  → 考虑更新计划

3 次失败后：上报给用户
  → 说明你尝试过什么
  → 分享具体错误
  → 请求指导
```

## 读 vs 写决策矩阵

| 场景 | 动作 | 原因 |
|-----------|--------|--------|
| 刚写完文件 | 不要读 | 内容仍在上下文中 |
| 查看了图片/PDF | 立即写入发现 | 多模态 → 在丢失前转成文本 |
| 浏览器返回数据 | 写入文件 | 截图不会持久保存 |
| 开始新阶段 | 读取计划/发现 | 若上下文过期则重新定位 |
| 发生错误 | 读取相关文件 | 需要当前状态才能修复 |
| 间隔后恢复 | 读取所有规划文件 | 恢复状态 |

## 五问重启测试

如果你能回答这些问题，说明你的上下文管理很扎实：

| 问题 | 答案来源 |
|----------|---------------|
| 我在哪里？ | task_plan.md 中的当前阶段 |
| 我要去哪里？ | 剩余阶段 |
| 目标是什么？ | 计划中的目标陈述 |
| 我学到了什么？ | findings.md |
| 我做了什么？ | progress.md |

## 何时使用该模式

**适用场景：**
- 多步任务（3 步以上）
- 研究任务
- 构建/创建项目
- 涉及大量工具调用的任务
- 任何需要组织规划的任务

**跳过场景：**
- 简单问题
- 单文件编辑
- 快速查找

## 模板

复制这些模板即可开始：

- [templates/task_plan.md](templates/task_plan.md) —— 阶段跟踪
- [templates/findings.md](templates/findings.md) —— 研究存储
- [templates/progress.md](templates/progress.md) —— 会话日志

## 脚本

用于自动化的辅助脚本：

- `scripts/init-session.sh` —— 初始化所有规划文件
- `scripts/check-complete.sh` —— 校验所有阶段是否完成

## 高级主题

- **Manus 原则：** 见 [reference.md](reference.md)
- **真实示例：** 见 [examples.md](examples.md)

## 反模式

| 不要这样做 | 应该这样做 |
|-------|------------|
| 用 TodoWrite 做持久化 | 创建 task_plan.md 文件 |
| 目标只陈述一次就忘记 | 决策前重读计划 |
| 隐藏错误并静默重试 | 将错误记录到计划文件 |
| 把所有东西塞进上下文 | 把大段内容存到文件里 |
| 立即开始执行 | 先创建计划文件 |
| 重复失败的动作 | 记录尝试、调整方案 |
| 在 skill 目录创建文件 | 在你的项目中创建文件 |
