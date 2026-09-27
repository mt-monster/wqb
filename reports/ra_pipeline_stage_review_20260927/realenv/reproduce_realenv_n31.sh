#!/usr/bin/env bash
# N31 · 真实环境探针复现（2026-09-27 第六轮）：SOP 步 6 手动补收入口修复前后对照
#
# 同一份真实历史（tracking/KOR 经 wqb-db MCP 写工具导入）上，N31 修复前的代码树（BASE_DIR）与本工作树各起一个
# wqb-db server（stdio，.mcp.json 原样）：工具表 → 照各自 SOP 原文调收批入库 → workflow_auto_harvest 只读报告 →
# workflow_auto_harvest 带 alphas。输入是 harvest_multisim_alphas 的返回形态（KOR 真实 wave94 指标组装）。
#
# 前提：同 reproduce_realenv.sh（MCP venv；无需 BRAIN 凭据，脚本从不读取 world-quant-brain-mcp/.env）
# 副作用与保护（run_realenv_n31.py 内实现）：两棵树的 data/wqb.db 演练期间换成导入快照的副本，结束（含异常）后移回；
# 库 > 5MB（像生产库）时拒跑，除非显式 REALENV_ALLOW_DB_SWAP=1
set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
PY="$REPO/world-quant-brain-mcp/.venv/bin/python"
[ -x "$PY" ] || PY="$REPO/world-quant-brain-mcp/.venv/Scripts/python.exe"   # Windows（Git Bash）venv 布局
REALENV_SCRATCH=${REALENV_SCRATCH:-$(mktemp -d)/realenv}
mkdir -p "$REALENV_SCRATCH"

# 修复前对照副本：N31 修复之前的提交（main 的 9ca1cc8）
PRE_FIX_REV=${PRE_FIX_REV:-9ca1cc8}
BASE_DIR=${BASE_DIR:-$REALENV_SCRATCH/base_n31}
if [ ! -d "$BASE_DIR/src" ]; then
  mkdir -p "$BASE_DIR"
  git -C "$REPO" archive "$PRE_FIX_REV" | tar -x -C "$BASE_DIR"
fi

cd "$REPO"
REALENV_SCRATCH="$REALENV_SCRATCH" BASE_DIR="$BASE_DIR" PYTHONIOENCODING=utf-8 \
  "$PY" -u reports/ra_pipeline_stage_review_20260927/realenv/run_realenv_n31.py | tee "$REALENV_SCRATCH/realenv_transcript_n31.txt"
echo "transcript: $REALENV_SCRATCH/realenv_transcript_n31.txt"
