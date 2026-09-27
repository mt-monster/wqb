#!/usr/bin/env bash
# N30 · 真实环境探针复现（2026-09-27 第五轮）：wave_results 两个自动写入方修复前后对照
#
# 同一份真实历史（tracking/KOR 经 wqb-db MCP 写工具导入）上，N30 修复前的代码树（BASE_DIR）与本工作树各跑一遍：
# 收批 GEM 标签波 → 补收已结案 / open 的真实波 → 评审（toolkit review_wave.py 真跑）→ 重评 → 停止规则 B →
# 只补 focus → 停止规则 B；再把两个 verdict 归一器放在全部区域的真实 verdict 原文上对照。末尾打印验证清单。
#
# 前提：同 reproduce_realenv.sh（MCP venv；无需 BRAIN 凭据，脚本从不读取 world-quant-brain-mcp/.env）
# 副作用与保护（run_realenv_n30.py 内实现）：
#   * 两棵树的 data/wqb.db（wqb-db server 写死该路径，N26）演练期间换成导入快照的副本，结束（含异常）后移回；
#     库 > 5MB（像生产库）时拒跑，除非显式 REALENV_ALLOW_DB_SWAP=1
#   * 战役目录用 $REALENV_SCRATCH/n30/<tree>/tracking/KOR（config 拷自原件），不写 tracking/KOR
set -euo pipefail
REPO=$(git rev-parse --show-toplevel)
PY="$REPO/world-quant-brain-mcp/.venv/bin/python"
[ -x "$PY" ] || PY="$REPO/world-quant-brain-mcp/.venv/Scripts/python.exe"   # Windows（Git Bash）venv 布局
REALENV_SCRATCH=${REALENV_SCRATCH:-$(mktemp -d)/realenv}
mkdir -p "$REALENV_SCRATCH"

# 修复前对照副本：N30 修复之前的提交
PRE_FIX_REV=${PRE_FIX_REV:-3ea1931}
BASE_DIR=${BASE_DIR:-$REALENV_SCRATCH/base_n30}
if [ ! -d "$BASE_DIR/src" ]; then
  mkdir -p "$BASE_DIR"
  git -C "$REPO" archive "$PRE_FIX_REV" | tar -x -C "$BASE_DIR"
fi

cd "$REPO"
REALENV_SCRATCH="$REALENV_SCRATCH" BASE_DIR="$BASE_DIR" PYTHONIOENCODING=utf-8 \
  "$PY" -u reports/ra_pipeline_stage_review_20260927/realenv/run_realenv_n30.py | tee "$REALENV_SCRATCH/realenv_transcript_n30.txt"
echo "transcript: $REALENV_SCRATCH/realenv_transcript_n30.txt"
