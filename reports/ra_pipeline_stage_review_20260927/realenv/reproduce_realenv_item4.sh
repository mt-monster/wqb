#!/usr/bin/env bash
# 第 4 项 · 真实环境探针复现（2026-09-28 第七轮）：backtest_results.ra_failed_checks 按 RA 唯一定义写，修复前后对照
#
# 修复前的代码树（BASE_DIR）与本工作树各起一个 wqb-db server（stdio，.mcp.json 原样），各用一个空库跑同一序列：
# 真实评审行（tracking/*/reviews）→ upsert_backtest_rows；真实平台载荷（tracking/mining/result_submit_*）与真实载荷
# 裁剪件上的四种情形，各走 toolkit 评审 / 收批·原始形态 / 收批·精简形态三条写入路径；再读 get_mining_yield 与提交队列。
#
# 前提：同 reproduce_realenv.sh（MCP venv；无需 BRAIN 凭据，脚本从不读取 world-quant-brain-mcp/.env）
# 副作用与保护（run_realenv_item4.py 内实现）：两棵树的 data/wqb.db 演练期间换成空库，结束（含异常）后移回；
# 库 > 5MB（像生产库）时拒跑，除非显式 REALENV_ALLOW_DB_SWAP=1
set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
PY="$REPO/world-quant-brain-mcp/.venv/bin/python"
[ -x "$PY" ] || PY="$REPO/world-quant-brain-mcp/.venv/Scripts/python.exe"   # Windows（Git Bash）venv 布局
REALENV_SCRATCH=${REALENV_SCRATCH:-$(mktemp -d)/realenv}
mkdir -p "$REALENV_SCRATCH"

# 修复前对照副本：第 4 项修复之前的提交（main 的 baf6f19）
PRE_FIX_REV=${PRE_FIX_REV:-baf6f19}
BASE_DIR=${BASE_DIR:-$REALENV_SCRATCH/base_item4}
if [ ! -d "$BASE_DIR/src" ]; then
  mkdir -p "$BASE_DIR"
  git -C "$REPO" archive "$PRE_FIX_REV" | tar -x -C "$BASE_DIR"
fi

cd "$REPO"
REALENV_SCRATCH="$REALENV_SCRATCH" BASE_DIR="$BASE_DIR" PYTHONIOENCODING=utf-8 \
  "$PY" -u reports/ra_pipeline_stage_review_20260927/realenv/run_realenv_item4.py | tee "$REALENV_SCRATCH/realenv_transcript_item4.txt"
echo "transcript: $REALENV_SCRATCH/realenv_transcript_item4.txt"
