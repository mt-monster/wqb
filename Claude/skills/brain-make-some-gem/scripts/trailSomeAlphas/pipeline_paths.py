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
#: 内嵌 legacy 兜底位（`scripts/trailSomeAlphas/skills/`）。**仅在脱离仓库且各安装位都缺失时才会用到**，
#: 其内容是历史快照、可能过期 —— 2026-09-26 审计核实的真实解析顺序见下方 `_resolve_skill_dir()`。
#: ⚠ 这两个常量只是"最后兜底"，**不是**运行时首选；下游应改用下面的解析结果。
_EMBEDDED_FEATURE_ENGINEERING_DIR = SKILLS_DIR / "brain-data-feature-engineering"
_EMBEDDED_FEATURE_IMPLEMENTATION_DIR = SKILLS_DIR / "brain-feature-implementation"


# ---------------------------------------------------------------------------
# GEM 数据产物根（2026-09-25 结构优化目标 A）
# ---------------------------------------------------------------------------
# 背景：final_expressions / 数据集 csv / whitelist / orphan_field_profile 此前落在
# FEATURE_IMPLEMENTATION_DIR/data/（skill 安装位内部、深 7 层），随 skill_roots 解析到的
# 安装位漂移（Claude 安装位 vs 历史 Agent 位 vs 仓库副本），同一 dataset 在不同时间写到
# 不同物理位置，gem.py 的 _find_final_expressions 需硬编码两段候选路径去猜。
# 现迁出到仓库稳定路径 data/gem_runs/（与 skill 安装位解耦），WQB_GEM_DATA_ROOT 可覆盖。


def _find_repo_root() -> Path | None:
    """从 BASE_DIR 向上找含 src/wqb 的祖先（仓库根判定，不硬编码盘符）。"""
    for anc in [BASE_DIR, *BASE_DIR.parents]:
        if (anc / "src" / "wqb" / "workflow" / "_common.py").is_file():
            return anc
    return None


def _resolve_gem_data_root() -> Path:
    """GEM 数据根：WQB_GEM_DATA_ROOT env > 仓库 data/gem_runs > 回退旧位（脱离仓库运行时兜底）。"""
    env = os.environ.get("WQB_GEM_DATA_ROOT")
    if env:
        return Path(env)
    repo = _find_repo_root()
    if repo is not None:
        return repo / "data" / "gem_runs"
    # 脱离仓库运行（如 skill 被单独拷走）：回退旧行为，保证可用。
    # ⚠ 这里用**内嵌 legacy 常量**而非 FEATURE_IMPLEMENTATION_DIR —— 后者在下方才解析，
    # 若在此引用会在"找不到仓库"这条分支上抛 NameError（2026-09-26 修正）。
    return _EMBEDDED_FEATURE_IMPLEMENTATION_DIR / "data"


GEM_DATA_ROOT = _resolve_gem_data_root()

#: GEM 自生成 ideas 报告根（2026-09-26）。原先写进 `FEATURE_ENGINEERING_DIR/output_report`，
#: 即**仓库 skill 树内部**（实证已有 16 个 `*_ideas.md` 混入 `Claude/skills/.../skills/`，
#: 且会随解析漂移落到不同安装位）。现与 `data/` 同源移出到 GEM_DATA_ROOT 下。
GEM_REPORT_ROOT = GEM_DATA_ROOT / "output_report"

# Ensure UTF-8 stdout on Windows to avoid UnicodeEncodeError
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 技能根解析统一走 skill_roots helper（2026-09-11 审计收敛；09-13 拆分后沿用）：
# 顺序与 toolkit `_lib/skill_roots.py` / `wqb.workflow._common._skill_roots()` 一致，
# 由 tests/unit/test_docs_consistency.py::test_root_resolvers_use_single_source_helper 守护。
from skill_roots import candidate_paths_under_skill as _cand  # noqa: E402

# ---------------------------------------------------------------------------
# skill 目录解析（2026-09-26 审计重写：两个目录统一走同一套解析，消除静默降级）
# ---------------------------------------------------------------------------
# 背景：`FEATURE_IMPLEMENTATION_DIR` 曾在默认位写死为内嵌 legacy 副本（09-13 才改为跟随 SCRIPTS）；
# 而 `FEATURE_ENGINEERING_DIR` **一直没改**，仍恒指向内嵌的 `skills/brain-data-feature-engineering`。
# 实测后果（2026-09-26）：那个内嵌目录**连 SKILL.md 都没有** → `read_text_optional()` 失败返回 `""`
# → 顶层 322 行的字段工程文档**从未进入 LLM prompt**，且完全静默。
# 现统一为：env 覆盖 > skill_roots 候选（主安装位优先，仓库副本兜底） > 内嵌 legacy 兜底。


def _resolve_skill_dir(env_var: str, skill_name: str, probe: str) -> "tuple[Path, str]":
    """解析 skill 目录。返回 (skill_dir, source)。

    probe 为相对 skill 根的**单段**探针（目录或文件），例如 "scripts" / "SKILL.md"——
    用单段是为了让 `candidate_paths_under_skill` 的返回值恰好是 `<skill_dir>/<probe>`，
    取 `.parent` 即得 skill 根。source ∈ {env:<VAR>, root:<安装位>, embedded:legacy}。
    """
    env = os.environ.get(env_var)
    if env:
        p = Path(env)
        if (p / probe).exists():
            return p, f"env:{env_var}"
    for _p in _cand(skill_name, probe):
        pp = _p if isinstance(_p, Path) else Path(_p)
        if pp.exists():
            return pp.parent, f"root:{pp.parent}"
    # 脱离仓库、且所有安装位都缺失 → 用内嵌 legacy 副本保证可用（调用方须据 source 告警）
    return SKILLS_DIR / skill_name, "embedded:legacy"


FEATURE_IMPLEMENTATION_DIR, _FI_SOURCE = _resolve_skill_dir(
    "WQB_FI_SKILL_DIR", "brain-feature-implementation", "scripts")
FEATURE_IMPLEMENTATION_SCRIPTS = FEATURE_IMPLEMENTATION_DIR / "scripts"
# 2026-09-13 修复（GEM 入库静默丢失事故）：DIR 必须与 SCRIPTS 同源，否则 implement/merge 产物写
# 主安装位、而 run_pipeline 的 final_path 检查相对位（B）→ 1015 分支落 else，
# validate/vector-fix/DB 入库全被跳过（DEU 三次 GEM 的 merge 产物被静默丢弃）。
# 2026-09-26：上句由"恒 = SCRIPTS.parent"升级为统一解析，语义不变、且新增 env 覆盖与来源留痕。
# 探针用 SKILL.md：内嵌 legacy 的 dfe 副本**没有** SKILL.md，因此它必然被跳过 → 自动选中
# 带完整 SKILL.md 的权威副本（这正是此前静默降级的根因）。
FEATURE_ENGINEERING_DIR, _DFE_SOURCE = _resolve_skill_dir(
    "WQB_DFE_SKILL_DIR", "brain-data-feature-engineering", "SKILL.md")

#: 供 run_pipeline 起跑时一次性打印/告警（谁胜出、哪个文档缺失）。
SKILL_DIR_SOURCES = {
    "feature_implementation": (FEATURE_IMPLEMENTATION_DIR, _FI_SOURCE),
    "feature_engineering": (FEATURE_ENGINEERING_DIR, _DFE_SOURCE),
}


def missing_skill_docs() -> "list[str]":
    """返回缺失的 skill 文档说明列表（**空列表 = 正常**）。

    GEM 会把两份 SKILL.md 拼进 LLM prompt；`read_text_optional` 失败返回空串，
    此前是**完全静默**的。此函数把"文档缺失"变成可断言的事实，由调用方告警。
    """
    out = []
    for label, d in (("brain-feature-implementation", FEATURE_IMPLEMENTATION_DIR),
                     ("brain-data-feature-engineering", FEATURE_ENGINEERING_DIR)):
        if not (d / "SKILL.md").is_file():
            out.append(f"{label}/SKILL.md 缺失（解析到 {d}）")
    return out


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
    """定位工作区 tools/lib（vector_wrap 的单一权威源）。

    2026-09-25 清理：移除硬编码盘符 D:/coding/...，改用 _find_repo_root() 推导
    （向上找含 src/wqb 的祖先），与 GEM_DATA_ROOT 同口径。
    """
    env = os.environ.get("WQB_TOOLS_LIB")
    if env and (Path(env) / "vector_wrap.py").is_file():
        return Path(env)
    # 从仓库根推导（_find_repo_root 向上找含 src/wqb 的祖先，不硬编码盘符）
    repo = _find_repo_root()
    if repo is not None:
        candidate = repo / "tools" / "lib"
        if (candidate / "vector_wrap.py").is_file():
            return candidate
    # WQB_ROOT env 显式覆盖（非常规部署）
    wqb_root = os.environ.get("WQB_ROOT")
    if wqb_root:
        candidate = Path(wqb_root) / "tools" / "lib"
        if (candidate / "vector_wrap.py").is_file():
            return candidate
    return None


_REPO_TOOLS_LIB = _find_tools_lib()
if _REPO_TOOLS_LIB and str(_REPO_TOOLS_LIB) not in sys.path:
    sys.path.insert(0, str(_REPO_TOOLS_LIB))
try:
    from vector_wrap import wrap_naked_vectors  # type: ignore
except Exception:
    # 无 tools/lib 时降级：生成端 VECTOR 兜底修复跳过（MATRIX 路径不受影响）
    wrap_naked_vectors = None
