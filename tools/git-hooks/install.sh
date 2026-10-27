#!/bin/sh
# install.sh — 把本目录挂成 git hooksPath（一次性，每台机器 / 每次克隆都要跑一次）。
#
# 为什么需要它
# ------------
# `core.hooksPath` 是**本机 git config，不入库**。所以干净克隆下来钩子是**不生效**的：
# pre-commit（audit_structure / doc_path_refs / destructive_default / pytest）与
# commit-msg（零信息提交消息）全都静默不跑，结构违规会一路攒到 CI 才发现——
# 而本仓直到 2026-10-24 才有 CI。这就是 2026-10-24 审计里 27 项违规（14 结构 + 13 测试）
# 能长期存在的根因。**新克隆第一件事就是跑本脚本。**
#
# 用法
# ----
#   sh tools/git-hooks/install.sh          # 安装（幂等，重复跑无副作用）
#   sh tools/git-hooks/install.sh --check  # 只校验是否挂好，不改配置（CI / 自检用）
#   sh tools/git-hooks/install.sh --unset  # 摘掉（回到 .git/hooks）
#
# Windows（PowerShell）用同目录的 install.ps1。
set -eu

# 本脚本在 tools/git-hooks/ 下 → 上两级是仓库根
_HOOKS_DIR=$(cd "$(dirname "$0")" && pwd)
_REPO_ROOT=$(cd "$_HOOKS_DIR/../.." && pwd)

# 相对路径形式，避免把绝对路径写进 config（这样拷走仓库也能用）
_REL_HOOKS="tools/git-hooks"

_mode=${1:---install}

_is_git_repo() {
    git -C "$_REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1
}

if ! _is_git_repo; then
    echo "[install-hooks] 不是 git 仓库：$_REPO_ROOT" >&2
    exit 1
fi

_current=$(git -C "$_REPO_ROOT" config core.hooksPath 2>/dev/null || echo "")

case "$_mode" in
    --check)
        if [ "$_current" = "$_REL_HOOKS" ]; then
            echo "[install-hooks] OK: core.hooksPath=$_REL_HOOKS"
            exit 0
        fi
        echo "[install-hooks] MISSING: core.hooksPath=[${_current:-<未设置>}]，期望 [$_REL_HOOKS]" >&2
        echo "[install-hooks] 修法：sh $_REL_HOOKS/install.sh" >&2
        exit 1
        ;;
    --unset)
        git -C "$_REPO_ROOT" config --unset core.hooksPath 2>/dev/null || true
        echo "[install-hooks] 已摘除 core.hooksPath（回到 .git/hooks）"
        exit 0
        ;;
    --install|"")
        ;;
    *)
        echo "[install-hooks] 未知参数：$_mode" >&2
        exit 1
        ;;
esac

# POSIX 下 git hook 必须可执行；Windows 上 git 不看执行位，但 chmod 无害
for _h in "$_HOOKS_DIR"/*; do
    [ -f "$_h" ] || continue
    case "$(basename "$_h")" in
        install.sh|install.ps1|README.md) continue ;;
    esac
    chmod +x "$_h" 2>/dev/null || true
done

git -C "$_REPO_ROOT" config core.hooksPath "$_REL_HOOKS"

echo "[install-hooks] 已挂上：core.hooksPath=$_REL_HOOKS"
echo "[install-hooks] 生效的钩子：$(ls "$_HOOKS_DIR" | grep -vE '^(install\.sh|install\.ps1|README\.md)$' | tr '\n' ' ')"
echo "[install-hooks] 自检：sh $_REL_HOOKS/install.sh --check"
