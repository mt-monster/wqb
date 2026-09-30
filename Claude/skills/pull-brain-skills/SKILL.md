---
last_verified: 2026-10-01
name: pull-brain-skills
description: "把外部 skill（ZIP URL / Git 仓库 / 本地目录）拉进**隔离暂存区**并出具静态审查报告（hooks / allowed-tools / scripts / 符号链接 / 风险模式 / 同名碰撞）；不安装、不执行被导入内容。包含 SKILL.md / skill.md（不区分大小写）的文件夹视为候选 skill。"
layer: L7
allowed-tools:
  - Bash
---

# Pull BRAIN Skill

## 职责边界

- **本 skill 负责**：把外部 skill 拉到**隔离暂存目录**（缺省 `attic/import_staging/`，已 gitignore），并对每个候选出具**静态审查报告**（`risk = low / review / high`）。
- **本 skill 不做**：**不安装**（缺省不写任何活跃 skill 根）；**不执行**被导入内容里的任何脚本 / 钩子；**不校验** layer / 命名 / frontmatter 语义（那是「导入后清单」与测试的事）；不做 skill 内容创作。
- **上游 / 下游**：上游 = 外部 skill 源；下游 = 人工审查 → 移入仓库 `Claude/skills/` →（`tools/sync_skills.py` 推送到各安装位）。

**为什么这么严**：导入外部 skill = 向运行时注入**指令 + 可执行物**——SKILL.md 会被当作指令执行，`scripts/` 会被 agent 运行，`allowed-tools: Bash` 授予命令执行，frontmatter 的 `hooks:` 会在工具调用 / 停止事件里执行任意 shell。所以默认只暂存、只审查，装不装由人在读完审查报告后决定。

## 使用方法

脚本：`Claude/skills/pull-brain-skills/scripts/pull_skills.py`（用 `$WQ_PY` 运行；本仓库真相源是 `Claude/skills/`，各宿主安装位由 `tools/sync_skills.py` 同步，见 `INDEX.md`）。

### 示例 1：通过 ZIP 拉取（首选）

在受限网络里最稳。**用固定 commit 的 ZIP，不要用分支头**：`.../archive/refs/heads/main.zip` 是可变引用（同一 URL 前后两次内容不同，你审查过的不一定是装进去的；默认分支也可能不叫 `main`）。

```bash
$WQ_PY Claude/skills/pull-brain-skills/scripts/pull_skills.py "https://github.com/<Owner>/<Repo>/archive/<commit-sha>.zip"
```

### 示例 2：通过 Git 拉取

需要特定分支或已配好 git 时用（`--branch` 只对 Git 源生效）：

```bash
$WQ_PY Claude/skills/pull-brain-skills/scripts/pull_skills.py "https://github.com/<Owner>/<Repo>.git" --branch <branch>
```

### 示例 3：从本地目录导入

```bash
$WQ_PY Claude/skills/pull-brain-skills/scripts/pull_skills.py "/path/to/my-skills-repo"
```

### 选项

| 选项 | 含义 |
|---|---|
| `--dest <dir>` | 目的地。缺省 = 暂存目录（仓库内 `attic/import_staging/`；不在仓库里则 `<cwd>/import_staging`）。指向活跃 skill 根需 `--allow-live-dest` |
| `--branch <b>` | 只对 Git URL 生效（ZIP / 本地目录忽略并提示） |
| `--subdir <rel>` | 从获取到的仓库里的这个子目录扫描（很多仓库把 skill 放在 `skills/<name>/`，此时必须 `--subdir skills`）；路径不得越出仓库 |
| `--overwrite` | 目的地已有同名文件夹时替换——**不删除**：旧的被挪到 `<dest>/.backup/<name>_<时间戳>`，可恢复 |
| `--allow-live-dest` | 允许写进活跃 skill 根（`Claude/skills/`、`~/.claude/skills/` 等）；风险非 `low` 的候选仍被跳过 |
| `--accept-risk` | 与上一项同用，才会写入 `review` / `high` 的候选 |

**退出码**：`0` 至少导入 / 暂存了一个 skill；`1` 用法错误；`2` 拉取 / 克隆 / 子目录失败；`3` 目的地是活跃根但没给 `--allow-live-dest`；`4` 拉取成功但**一个都没导入**（顶层没有含 SKILL.md 的文件夹，或全被跳过）——这不是成功。

ZIP 下载有超时（60 s）与大小上限（50 MB），解压有 zip-slip 防护；本工具从不执行被导入内容，唯一的删除是它自己的临时目录。

## 读审查报告

每个候选的 `audit` 含：

- `hooks`：frontmatter 有 `hooks:` → `risk = high`（必须逐行审）；
- `allowed_tools`：含 `Bash` → `high`；
- `scripts`：`scripts/` 与各类脚本文件清单 → 至少 `review`；
- `symlinks`：有符号链接 → `high`；
- `findings`：风险模式命中（读 `.env` / credentials / `~/.ssh`；`curl` / `requests.post` 等外发；`rm -rf` / `shutil.rmtree` 等删除；`eval` / `subprocess` 等动态执行）；
- `name_collision_with_live`：与现有 skill 同名（想「更新」的场景，见情景 PB-2）。

## 导入后清单（审查通过后，人工执行）

1. **看报告**：`hooks` / `allowed-tools: Bash` / `scripts/` / `findings` 逐条读完，读不懂就拒绝；拒绝理由记一行（见情景 PB-3）。
2. **归层**：按 [`INDEX.md`](../INDEX.md)「分层架构」与 `AGENTS.md`「Skill layer 取值表」选 `layer`。
3. **补 frontmatter**：`name` = 目录名（kebab-case）、`layer`、`last_verified`（今天）、`description`。
4. **补「职责边界」段**（紧跟 H1，含 负责 / 不做 / 上游·下游）——缺它测试不予通过。
5. **命名**：目录名若为 camelCase / 下划线 / 混合大小写，对照 [`CONTRACT.md`](../CONTRACT.md) §3「命名规范」给出 kebab-case 迁移名；不自动重命名（防断引用），由人决定。
6. **移入并同步**：把审查过的文件夹移入 `Claude/skills/`，然后 `$WQ_PY tools/sync_skills.py`（+ `--check`），再跑 `pytest tests/unit/07_docs_skills/test_skill_integrity.py tests/unit/07_docs_skills/test_skill_boundaries.py -q`。
7. **回滚**：还没提交 → 删除新目录并再跑一次 sync；已提交 → `git revert`；`--overwrite` 覆盖过 → 从 `<dest>/.backup/` 挪回。

## 情景卡

### 情景 PB-1　从 GitHub 仓库导入一个 skill 到审查区

- **前置状态**：要导入 `<Owner>/<Repo>` 里的一个 skill，仓库把 skill 放在 `skills/<name>/`。
- **步骤**：① 取固定 commit 的 ZIP；② `$WQ_PY Claude/skills/pull-brain-skills/scripts/pull_skills.py "<...>/archive/<sha>.zip" --subdir skills`；③ 读输出 JSON 的 `copied[].audit`（hooks / allowed_tools / scripts / findings）。
- **分支**：没加 `--subdir` → 退出码 4，提示改用 `--subdir skills`；`risk = low` → 进「导入后清单」；`high` → 逐行审 hooks / Bash，或拒绝。
- **完成定义**：暂存目录里有该文件夹，且已读完并留存审查报告。
- **反例**：用 `refs/heads/main.zip`（审查与安装的内容可能不同）；在没读报告前就移入 `Claude/skills/`。

### 情景 PB-2　导入的 skill 与现有同名（想更新）

- **前置状态**：审查输出 `name_collision_with_live: true`。
- **步骤**：暂存后 `diff -ru Claude/skills/<name> attic/import_staging/<name>`（或 `git diff --no-index`）；逐块判断保留 / 采纳；合并结果放进 `Claude/skills/<name>`，走「导入后清单」。
- **分支**：想整体替换 → 目的地用 `--overwrite`，旧目录会被挪进 `.backup/`，可恢复。
- **完成定义**：`Claude/skills/<name>` 的改动是一次有意的、可 `git diff` 审阅的合并。
- **反例**：对活跃根直接 `--allow-live-dest --overwrite --accept-risk`。

### 情景 PB-3　导入后发现带 `hooks` 或读取 `.env`

- **前置状态**：审查报告里 `hooks: true`，或 `findings` 含 `credential/secret access`。
- **步骤**：**不移入**活跃根；把拒绝理由（哪个文件、哪条命中）记在本轮日志 / 对用户的回复里；需要其中的功能就手工重写一份不含钩子、不碰凭据的版本。
- **完成定义**：暂存区里的该文件夹被删除或留作证据，活跃根没有被写入。
- **反例**：因为「看起来有用」而加 `--accept-risk`。

## 注意事项

- 路径使用正斜杠以保证兼容性；只有 Git 源需要 `git` 在 PATH 中。
- 只检查 `SKILL.md` / `skill.md` 是否存在（不区分大小写），不校验内容有效性——内容有效性靠上面的清单与测试。
