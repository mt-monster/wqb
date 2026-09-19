# -*- coding: utf-8 -*-
"""GEM 管线环境引导与共享依赖（run_pipeline 家族最底层模块）。

职责（单一，2026-09-12 从 run_pipeline.py 拆出）：
  1. 路径常量（BASE_DIR / SKILLS_DIR / FEATURE_*_DIR）
  2. UTF-8 stdout 配置（Windows 防 UnicodeEncodeError）
  3. sys.path 注入：feature-implementation scripts + 工作区 tools/lib
  4. 共享依赖导入：ace_lib / ExpressionValidator / wrap_naked_vectors

依赖方向：pipeline_paths → 其他 pipeline_* 与 run_pipeline。
本模块不得 import 任何 pipeline_* 业务模块（避免循环依赖）。

兼容性：headless_runner/run.py 通过 `rp.ace_lib` 访问 ace_lib 并 patch 其属性，
run_pipeline.py 必须 re-export 本模块的 ace_lib（同一模块对象，属性 patch 全局生效）。
"""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SKILLS_DIR = BASE_DIR / "skills"
FEATURE_ENGINEERING_DIR = SKILLS_DIR / "brain-data-feature-engineering"
FEATURE_IMPLEMENTATION_DIR = SKILLS_DIR / "brain-feature-implementation"
FEATURE_IMPLEMENTATION_SCRIPTS = FEATURE_IMPLEMENTATION_DIR / "scripts"

# Ensure UTF-8 stdout on Windows to avoid UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 技能根解析统一走 skill_roots helper（2026-09-11 审计收敛；09-13 拆分后沿用）：
# 顺序与 toolkit `_lib/skill_roots.py` / `wqb.workflow._common._skill_roots()` 一致，
# 由 tests/unit/test_docs_consistency.py::test_root_resolvers_use_single_source_helper 守护。
from skill_roots import candidate_paths_under_skill as _cand  # noqa: E402

# feature-implementation scripts 优先取主安装位副本，仓库副本兜底
for _p in _cand("brain-feature-implementation", "scripts"):
    if (_p if isinstance(_p, Path) else Path(_p)).is_dir():
        sys.path.insert(0, str(_p))
        FEATURE_IMPLEMENTATION_SCRIPTS = Path(_p)
        # 2026-09-13 修复（GEM 入库静默丢失事故）：DIR 原先不随 SCRIPTS 重解析，
        # 造成 implement/merge 产物写主安装位、而 run_pipeline 的 final_path
        # 检查相对位（B）→ 1015 分支落 else，validate/vector-fix/DB 入库全被
        # 跳过（DEU 三次 GEM 的 merge 产物被静默丢弃，靠手工抢救入库）。
        # DIR 恒 = SCRIPTS.parent，与实际执行位置同源。
        FEATURE_IMPLEMENTATION_DIR = FEATURE_IMPLEMENTATION_SCRIPTS.parent
        break

sys.path.insert(0, str(FEATURE_IMPLEMENTATION_SCRIPTS))
try:
    import ace_lib  # type: ignore
except Exception as exc:  # pragma: no cover - 环境缺失时硬失败（原 run_pipeline 同行为）
    raise SystemExit(f"Failed to import ace_lib from {FEATURE_IMPLEMENTATION_SCRIPTS}: {exc}")
try:
    from validator import ExpressionValidator  # type: ignore
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"Failed to import ExpressionValidator from {FEATURE_IMPLEMENTATION_SCRIPTS}: {exc}")


def _find_tools_lib() -> Path | None:
    """定位工作区 tools/lib（vector_wrap 的单一权威源）。"""
    env = os.environ.get("WQB_TOOLS_LIB")
    if env and (Path(env) / "vector_wrap.py").is_file():
        return Path(env)
    # 从常见工作区根向上/已知位置探测 vector_wrap.py
    candidates = [
        Path(os.environ.get("WQB_ROOT", "")) / "tools" / "lib" if os.environ.get("WQB_ROOT") else None,
        Path("D:/coding/traeCN_project/wqb/tools/lib"),
    ]
    for c in candidates:
        if c and (c / "vector_wrap.py").is_file():
            return c
    return None


_REPO_TOOLS_LIB = _find_tools_lib()
if _REPO_TOOLS_LIB and str(_REPO_TOOLS_LIB) not in sys.path:
    sys.path.insert(0, str(_REPO_TOOLS_LIB))
try:
    from vector_wrap import wrap_naked_vectors  # type: ignore
except Exception:
    # 无 tools/lib 时降级：生成端 VECTOR 兜底修复跳过（MATRIX 路径不受影响）
    wrap_naked_vectors = None
