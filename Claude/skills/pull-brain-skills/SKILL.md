---
last_verified: 2026-09-12
name: pull-brain-skills
description: "从 ZIP URL（首选）、Git 仓库或本地目录导入有效的 agent skill。包含 SKILL.md / skill.md 文件（不区分大小写）的文件夹视为有效 skill。"
layer: L7
allowed-tools:
  - Bash
---







# Pull BRAIN Skill

本 skill 从远程源或本地目录导入 skill 文件夹。

**校验规则**：若一个文件夹包含 `SKILL.md` 或 `skill.md` 文件（不区分大小写），即视为有效 skill。

## 使用方法

1. **定位脚本**：`<SKILL_ROOT>/pull-brain-skills/scripts/pull_skills.py`
   （`<SKILL_ROOT>` = 技能库根目录；本仓库真相源是 `Claude/skills/`，各宿主安装位由 `tools/sync_skills.py` 同步，见 `INDEX.md`）

2. **运行脚本**：提供 ZIP URL（推荐）、Git URL 或本地路径。

### 示例 1：通过 ZIP 拉取（首选推荐）
该方法更快，且在受限网络环境中表现最好。为此，你需要先把仓库地址解析为 ZIP 文件 URL：在仓库 URL 后追加 `/archive/refs/heads/main.zip`。例如，仓库地址为 `https://github.com/GitRepoAuthorName/RepoName` 时，ZIP URL 即为 `https://github.com/GitRepoAuthorName/RepoName/archive/refs/heads/main.zip`。
```bash
python "<SKILL_ROOT>/pull-brain-skills/scripts/pull_skills.py" "https://github.com/GitRepoAuthorName/RepoName/archive/refs/heads/main.zip" --overwrite
```

### 示例 2：通过 Git 拉取
当你需要特定分支或已配置好 git 时使用。
```bash
python "<SKILL_ROOT>/pull-brain-skills/scripts/pull_skills.py" "https://github.com/GitRepoAuthorName/RepoName.git"
```

### 示例 3：从本地目录导入
```bash
python "<SKILL_ROOT>/pull-brain-skills/scripts/pull_skills.py" "C:/Downloads/my-skills-repo"
```

选项：
- `--dest <path>`：skill 的目标安装目录。默认 = 仓库真相源 `Claude/skills/`（导入后须跑 `tools/sync_skills.py` 推送到各安装位）；也可指定某个安装位根目录。
- `--branch <branch>`：指定要检出的分支。
- `--overwrite`：覆盖同名已存在的 skill 文件夹。

## 行为
- 浅克隆仓库（`--depth 1`）到临时目录。
- 扫描顶层文件夹中的 `SKILL.md` / `skill.md`（不区分大小写）。
- 将有效的 skill 文件夹复制到 `--dest` 指定的目录（默认仓库 `Claude/skills/`）。

## 注意事项
- 路径使用正斜杠以保证兼容性。
- 需要 `git` 位于 PATH 中。
- 仅检查 `SKILL.md` / `skill.md` 是否存在，不校验内容有效性。
- **命名规范警告**：拉取到的 skill 目录名若为 camelCase、下划线或混合大小写（不符合 `INDEX.md` 命名规范的 kebab-case），安装时应向用户**警告**该目录名不规范，并建议规范迁移名（参见 `INDEX.md` 命名规范章节的存量例外表）；不自动重命名（防断引用），由用户决定是否调整后安装。
