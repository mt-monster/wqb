#!/usr/bin/env bash
# N35 · 真实环境探针复现（2026-09-28 第八轮）：同一 alpha 再次入库时 alphas / backtest_results 按合并写，修复前后对照
#
# 修复前的代码树（BASE_DIR）与本工作树各起一个 wqb-db server（stdio，.mcp.json 原样），各用一个空库走同一条 alpha 生命周期：
# 收批入库 → 相关性落库 → 提交后平台同步（tools/sync_platform_alphas 的真实转换）→ toolkit 重评审 → 事后补收，
# 再读提交队列、区域 ACTIVE 计数、sync 的本地已提交台账与 get_mining_yield。载荷是 tracking/mining/result_submit_*
# 的真实平台 checks 与真实载荷裁剪件；提交时间、OS 段与相关性数值是构造值。
#
# 前提：同 reproduce_realenv.sh（MCP venv；无需 BRAIN 凭据，脚本从不读取 world-quant-brain-mcp/.env）
# 副作用与保护（run_realenv_n35.py 内实现）：两棵树的 data/wqb.db 演练期间换成空库，结束（含异常）后移回；
# 库 > 5MB（像生产库）时拒跑，除非显式 REALENV_ALLOW_DB_SWAP=1
set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
PY="$REPO/world-quant-brain-mcp/.venv/bin/python"
[ -x "$PY" ] || PY="$REPO/world-quant-brain-mcp/.venv/Scripts/python.exe"   # Windows（Git Bash）venv 布局
REALENV_SCRATCH=${REALENV_SCRATCH:-$(mktemp -d)/realenv}
mkdir -p "$REALENV_SCRATCH"

# 修复前对照副本：N35 修复之前的提交（main 的 023bdb9）
PRE_FIX_REV=${PRE_FIX_REV:-023bdb9}
BASE_DIR=${BASE_DIR:-$REALENV_SCRATCH/base_n35}
if [ ! -d "$BASE_DIR/src" ]; then
  mkdir -p "$BASE_DIR"
  git -C "$REPO" archive "$PRE_FIX_REV" | tar -x -C "$BASE_DIR"
fi

cd "$REPO"
REALENV_SCRATCH="$REALENV_SCRATCH" BASE_DIR="$BASE_DIR" PYTHONIOENCODING=utf-8 \
  "$PY" -u reports/ra_pipeline_stage_review_20260927/realenv/run_realenv_n35.py | tee "$REALENV_SCRATCH/realenv_transcript_n35.txt"
echo "transcript: $REALENV_SCRATCH/realenv_transcript_n35.txt"
