#!/usr/bin/env bash
# RA 九步流水线 · 真实环境 dry-run 复现（2026-09-27；第三轮 = P0 + P1（R18–R21）修复后）
#
# 两个 MCP server 与所有子进程的 env = .mcp.json 原样（不补任何工作区根变量）；每步打印【阶段小结】，
# 末尾打印 P1 验证清单（对照同目录 realenv_transcript_p0.txt = 第二轮实录）。
#
# 前提：
#   * MCP venv：world-quant-brain-mcp/.venv（Python 3.12），按 world-quant-brain-mcp/requirements.txt 安装，外加 ply
#     （wave_gate 语法闸依赖；requirements 未声明，见报告 N12）
#   * 无需 BRAIN 凭据；脚本从不读取 world-quant-brain-mcp/.env
# 副作用与保护（run_realenv.py 内实现）：
#   * <repo>/data/wqb.db 演练期间临时移到 $REALENV_SCRATCH，结束（含异常）后移回；
#     库 > 5MB（像生产库）时拒跑，除非显式 REALENV_ALLOW_DB_SWAP=1
#   * tracking/KOR/priors/ 有未提交改动时拒跑；真实 assemble-priors 会重写该目录，结束后 git checkout 复原
#   * logs/_async_tasks/ 新增 campaign 异步任务文件（gitignored）
#   * 演练中 wave_gate 在仓库根造出的杂散目录 "D:\coding\traeCN_project\wqb" 会被检测并删除
#     （R19 之后不再出现；检测保留，作为回归护栏）
set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
PY="$REPO/world-quant-brain-mcp/.venv/bin/python"
[ -x "$PY" ] || PY="$REPO/world-quant-brain-mcp/.venv/Scripts/python.exe"   # Windows（Git Bash）venv 布局
REALENV_SCRATCH=${REALENV_SCRATCH:-$(mktemp -d)/realenv}
mkdir -p "$REALENV_SCRATCH"

# 修复前对照副本（附 B）：两个 P0 修复之前的提交
PRE_FIX_REV=${PRE_FIX_REV:-d1c7d78}
BASE_DIR=${BASE_DIR:-$REALENV_SCRATCH/base}
if [ ! -d "$BASE_DIR/src" ]; then
  mkdir -p "$BASE_DIR"
  git -C "$REPO" archive "$PRE_FIX_REV" | tar -x -C "$BASE_DIR"
fi

cd "$REPO"
REALENV_SCRATCH="$REALENV_SCRATCH" BASE_DIR="$BASE_DIR" PYTHONIOENCODING=utf-8 \
  "$PY" -u reports/ra_pipeline_stage_review_20260927/realenv/run_realenv.py | tee "$REALENV_SCRATCH/realenv_transcript.txt"
echo "transcript: $REALENV_SCRATCH/realenv_transcript.txt"
