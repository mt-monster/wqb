#!/usr/bin/env bash
# 复现 2026-09-27 RA 九步流水线沙箱 dry-run。
# 在一个临时目录里用 `git archive HEAD` 建隔离副本 + 合成种子库，全程不读写真实仓库与生产库 data/wqb.db。
# 用法：bash reports/ra_pipeline_stage_review_20260927/reproduce.sh [工作目录]
# Windows 下在 Git Bash 里运行；若没有 python3 命令，先 `export PY=python`。
set -euo pipefail
PY=${PY:-python3}
REPO=$(git rev-parse --show-toplevel)
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=${1:-$(mktemp -d)}
mkdir -p "$WORK/wqb/data" "$WORK/home" "$WORK/stubs/mcp/server" "$WORK/pylib" "$WORK/out"
git -C "$REPO" archive HEAD | tar -x -C "$WORK/wqb"

# 只为能 import wqb_db_mcp.py：FastMCP.tool() 退化为恒等装饰器
: > "$WORK/stubs/mcp/__init__.py"
: > "$WORK/stubs/mcp/server/__init__.py"
cat > "$WORK/stubs/mcp/server/fastmcp.py" <<'EOF'
class FastMCP:
    def __init__(self, *a, **k): pass
    def tool(self, *a, **k):
        def deco(fn): return fn
        return deco
    resource = prompt = tool
    def run(self, *a, **k): raise RuntimeError("stub FastMCP: run() disabled in sandbox")
EOF

# ply = 验证器硬依赖（requirements 未声明）；msgpack = 体检硬门依赖（已在 MCP requirements 声明）
"$PY" -m pip install --quiet --target "$WORK/pylib" ply "msgpack>=1.0.0,<2.0.0"

cp "$HERE/sbx_guard.py" "$HERE/seed_db.py" "$HERE/run_dryrun.py" "$WORK/"
export SBX="$WORK/wqb" STUBS="$WORK/stubs" HOME="$WORK/home" PYTHONDONTWRITEBYTECODE=1
(cd "$WORK" && "$PY" seed_db.py)
(cd "$WORK" && PYTHONPATH_NOPLY="$WORK" PYTHONPATH="$WORK:$WORK/pylib" "$PY" run_dryrun.py | tee "$WORK/out/transcript_raw.txt")
echo "transcript -> $WORK/out/transcript_raw.txt"
