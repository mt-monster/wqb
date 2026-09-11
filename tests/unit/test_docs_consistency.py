# -*- coding: utf-8 -*-
"""文档 ↔ 代码 一致性守护测试（2026-09-11 新增）。

背景：2026-09-11 的"RA 流水线自洽性审计"共修了 24 项，其中**至少 5 项**
（技能根硬编码、闸编号三种口径、阈值 schema 两版、`.bak_` 残留、旧 skill 名残留）
本可由一条测试提前拦下 —— 它们全是"文档/配置 vs 代码/事实"的漂移，不需要跑平台。

本文件把这些审计结论固化为回归，覆盖 7 类：

  1. thresholds.json schema（六节规范版 vs KOR/IND/DEU 扁平版，两者都必须被 contract 记录）
  2. gate.py 闸编号只有一种口径（权威 = gate.py 模块头：8 闸 + 可选闸0）
  3. 区域三表互含（`src/wqb/config.py::REGIONS` / ra-pipeline profiles / INDEX.md 区域表）
  4. 每个 region profile 的 frontmatter 契约（9 个键 + entry_verdict 取值 + region == 文件名）
  5. 无硬编码技能根（`C:\\Users\\...` 绝对路径；四处技能根解析必须含 `.claude` 主位）
  6. skills 目录内所有 markdown 的相对链接可解析（不止 SKILL.md）
  7. skills 树内无 `.bak_*` 残留（sync 忽略 `.bak_` → 残留永不被发现）

维护约定：新增/修改 skill 或 profile 后若本文件失败，**先修内容**，不要放宽断言；
确实需要放宽的（如新的允许上下文），把理由写进注释。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "Claude" / "skills"
RA_PIPELINE = SKILLS_DIR / "wq-brain-ra-pipeline"
PROFILES_DIR = RA_PIPELINE / "references" / "regions"
INDEX_MD = SKILLS_DIR / "INDEX.md"
TOOLKIT_SKILL = SKILLS_DIR / "wq-brain-campaign-toolkit" / "SKILL.md"
GATE_RULES = SKILLS_DIR / "wq-brain-campaign-toolkit" / "references" / "gate-rules.md"
GATE_PY = SKILLS_DIR / "wq-brain-campaign-toolkit" / "scripts" / "gate.py"
SYNC_TOOL = REPO_ROOT / "tools" / "sync_skills.py"

sys.path.insert(0, str(REPO_ROOT / "src"))


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# 1. thresholds.json schema 两版并存，且都被 contract 记录
# ---------------------------------------------------------------------------

SIX_SECTIONS = {"review", "near", "quick_scan", "probe_scoring_v2", "hard_gates", "dataset_health"}
#: 扁平版的等价键（KOR / IND / DEU：把闸值写在顶层）
FLAT_KEYS = {"review", "near", "sharpe_min", "fitness_min", "prod_corr_max",
             "self_corr_max", "turnover_min", "turnover_max"}


def _thresholds_files() -> list[Path]:
    return sorted((REPO_ROOT / "tracking").glob("*/config/thresholds.json"))


def test_thresholds_files_exist():
    files = _thresholds_files()
    assert files, "tracking/*/config/thresholds.json 一个都没有 —— 路径或布局变了？"


@pytest.mark.parametrize("path", _thresholds_files(), ids=lambda p: p.parent.parent.name)
def test_thresholds_json_parses_and_has_common_sections(path: Path):
    data = json.loads(_read(path))
    common = {"review", "near", "dataset_health"}
    missing = common - set(data)
    assert not missing, f"{path.parent.parent.name} 缺公共节 {sorted(missing)}"


@pytest.mark.parametrize("path", _thresholds_files(), ids=lambda p: p.parent.parent.name)
def test_thresholds_is_six_section_or_flat_form(path: Path):
    """每份 thresholds 必须能判入两种 schema 之一，不允许"第三种形态"。"""
    keys = set(json.loads(_read(path)))
    six = SIX_SECTIONS <= keys
    flat = FLAT_KEYS <= keys
    assert six or flat, (
        f"{path.parent.parent.name} 既非六节规范版（缺 {sorted(SIX_SECTIONS - keys)}）"
        f"也非扁平版（缺 {sorted(FLAT_KEYS - keys)}）—— 新增了第三种 schema，"
        f"请同步 references/campaign-dir-contract.md 与本测试"
    )


def test_contract_documents_both_thresholds_schemas():
    contract = _read(TOOLKIT_SKILL.parent / "references" / "campaign-dir-contract.md")
    assert "两版 schema 并存" in contract, "contract 未记录两版 schema 并存"
    assert "| diversity |" in contract, "contract 未记录 diversity 节"


def test_contract_has_diversity_signal_floor_semantics():
    contract = _read(TOOLKIT_SKILL.parent / "references" / "campaign-dir-contract.md")
    assert "静默放行" in contract, "contract 未说明 signal_floor 缺配置时的放行语义"


# ---------------------------------------------------------------------------
# 2. gate.py 闸编号（唯一基准 = gate.py 模块头）
# ---------------------------------------------------------------------------

def test_gate_py_header_declares_eight_gates():
    """权威来源：gate.py 自己的模块 docstring。"""
    src = _read(GATE_PY)
    head = src[:2000]
    assert "8 闸" in head, "gate.py 模块头未声明 8 闸 —— 权威变了，同步文档"
    assert "闸0" in head, "gate.py 模块头未提及可选闸0"


def test_gate_numbering_has_single_authoritative_table():
    idx = _read(INDEX_MD)
    assert "## gate.py 闸编号" in idx, "INDEX.md 缺闸编号权威表"
    assert "8 闸 + 可选闸0" in idx


def test_no_competing_gate_counts_in_docs():
    """禁止出现与权威表冲突的第三/第四种口径。"""
    idx = _read(INDEX_MD)
    toolkit = _read(TOOLKIT_SKILL)
    rules = _read(GATE_RULES)
    assert "**8 闸 + 可选闸0**" in toolkit, "toolkit §6 未用权威口径"
    assert "闸编号唯一基准" in rules, "gate-rules 未标注闸编号基准"
    assert "gate 6 闸判定细则" not in rules, "gate-rules 标题仍是旧的『6 闸』口径"


def test_agents_md_references_authoritative_gate_count():
    agents = _read(REPO_ROOT / "AGENTS.md")
    assert "gate.py 8 闸" in agents, "AGENTS.md §6 未对齐权威闸数"


# ---------------------------------------------------------------------------
# 3. 区域三表互含
# ---------------------------------------------------------------------------

def _code_regions() -> set[str]:
    from wqb.config import REGIONS
    return set(REGIONS)


def _profile_names() -> set[str]:
    return {p.stem for p in PROFILES_DIR.glob("*.md")}


def test_profiles_subset_of_code_regions():
    extra = _profile_names() - _code_regions()
    assert not extra, f"profile 里有 config.REGIONS 未定义的区域：{sorted(extra)}"


def test_index_region_table_covers_all_code_regions():
    idx = _read(INDEX_MD)
    missing = sorted(r for r in _code_regions() if r not in idx)
    assert not missing, f"INDEX.md 区域表缺：{missing}"


def test_index_has_region_table_section():
    assert "## 区域清单" in _read(INDEX_MD)


# ---------------------------------------------------------------------------
# 4. region profile frontmatter 契约
# ---------------------------------------------------------------------------

PROFILE_KEYS = ["region", "entry_verdict", "one_liner", "static", "datasets",
                "priors", "gate_overrides", "loop_policy", "empirical_anchor"]
VALID_VERDICTS = {"active", "probe-only", "frozen"}


@pytest.mark.parametrize("path", sorted(PROFILES_DIR.glob("*.md")), ids=lambda p: p.stem)
def test_profile_frontmatter_contract(path: Path):
    text = _read(path)
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    assert m, f"{path.name} 无 YAML frontmatter"
    block = m.group(1)
    keys = re.findall(r"^([a-z_]+):", block, re.M)
    missing = [k for k in PROFILE_KEYS if k not in keys]
    assert not missing, f"{path.name} profile 缺键：{missing}"

    region = re.search(r"^region:\s*(\S+)", block, re.M)
    assert region, f"{path.name} 无 region 字段"
    assert region.group(1) == path.stem, f"{path.name} 的 region={region.group(1)} 与文件名不符"

    verdict = re.search(r"^entry_verdict:\s*(\S+)", block, re.M)
    assert verdict, f"{path.name} 无 entry_verdict"
    assert verdict.group(1) in VALID_VERDICTS, (
        f"{path.name} entry_verdict={verdict.group(1)} 不在 {sorted(VALID_VERDICTS)}")


# ---------------------------------------------------------------------------
# 5. 无硬编码技能根
# ---------------------------------------------------------------------------

#: 允许出现"历史路径/反例"的上下文（行级白名单）
ALLOW_HARDCODE = ("历史", "禁止", "此前", "顺序", "→", ".claude", "自动搜索", "硬编码", "废弃",
                  "已归档", "旧名", "禁用", "迁移")
#: 只判"把安装位当**路径前缀**用"（即 `.../.<host>/skills/<skill>/...`），
#: 单纯列出安装位根目录（如 INDEX.md 的权威副本表）是合法文档，不算违规。
HARDCODE_PATTERNS = (
    r"C:[\\/]Users[\\/]",
    r"\.(?:qoder-cn|trae-cn|workbuddy|cursor|codex|claude)[\\/]skills[\\/]",
)


def _hardcode_violations(path: Path) -> list[str]:
    out = []
    for i, line in enumerate(_read(path).splitlines(), 1):
        if not any(re.search(p, line) for p in HARDCODE_PATTERNS):
            continue
        if any(a in line for a in ALLOW_HARDCODE):
            continue
        out.append(f"{path.relative_to(REPO_ROOT).as_posix()}:{i}: {line.strip()[:90]}")
    return out


def test_no_hardcoded_skill_root_in_skills_markdown():
    bad = []
    for p in SKILLS_DIR.rglob("*.md"):
        if "_unpacked" in p.as_posix():
            continue
        bad += _hardcode_violations(p)
    assert not bad, "skills 文档出现硬编码技能根主路径：\n" + "\n".join(bad[:8])


def test_no_hardcoded_skill_root_in_docs():
    bad = []
    for p in (REPO_ROOT / "docs").rglob("*.md"):
        bad += _hardcode_violations(p)
    assert not bad, "docs 出现硬编码技能根主路径：\n" + "\n".join(bad[:8])


def test_no_hardcoded_user_path_in_skills_python():
    bad = []
    for p in SKILLS_DIR.rglob("*.py"):
        if "_unpacked" in p.as_posix() or "__pycache__" in p.as_posix():
            continue
        for i, line in enumerate(_read(p).splitlines(), 1):
            if re.search(r"C:[\\/]Users[\\/]", line) and not line.strip().startswith("#"):
                bad.append(f"{p.relative_to(REPO_ROOT).as_posix()}:{i}: {line.strip()[:90]}")
    assert not bad, "skills 脚本出现硬编码用户绝对路径：\n" + "\n".join(bad[:8])


#: 四处"技能根解析"调用点（N1 回归锚点）：必须走单源 helper，不得再内联搜索链
ROOT_RESOLVERS = [
    SKILLS_DIR / "brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py",
    SKILLS_DIR / "brain-make-some-gem/scripts/trailSomeAlphas/skeletons.py",
    SKILLS_DIR / "wq-brain-campaign-toolkit/scripts/assemble_priors.py",
    SKILLS_DIR / "wq-brain-campaign-toolkit/scripts/gate.py",
]

SKILL_ROOT_MIRRORS = {
    "brain-make-some-gem": SKILLS_DIR / "brain-make-some-gem/scripts/trailSomeAlphas/skill_roots.py",
    "wq-brain-campaign-toolkit": SKILLS_DIR / "wq-brain-campaign-toolkit/scripts/_lib/skill_roots.py",
}


@pytest.mark.parametrize("path", ROOT_RESOLVERS, ids=lambda p: p.name)
def test_root_resolvers_use_single_source_helper(path: Path):
    """2026-09-11 收敛：四处调用点统一走 skill_roots helper（顺序只此一份）。"""
    assert path.is_file(), f"技能根解析脚本不存在：{path}"
    src = _read(path)
    assert "skill_roots" in src, (
        f"{path.name} 未引用 skill_roots helper —— 内联搜索链会与主安装位/仓库副本脱节")


def _load_module_from_file(path: Path, name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, f"无法加载 {path}"
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_skill_root_mirrors_declare_same_host_order():
    """两份镜像（gem / toolkit）的宿主顺序必须一致，且主安装位在最前。"""
    mods = {k: _load_module_from_file(v, f"mirror_{k.replace('-', '_')}")
            for k, v in SKILL_ROOT_MIRRORS.items()}
    orders = {k: tuple(getattr(m, "HOST_DIRS")) for k, m in mods.items()}
    assert len(set(orders.values())) == 1, f"两份镜像宿主顺序不一致：{orders}"
    first_two = list(orders.values())[0][:2]
    assert first_two == (".claude", ".codex"), (
        f"技能根解析必须优先主安装位 ~/.claude/skills 与 ~/.codex/skills，实际：{first_two}")


def test_skill_root_mirrors_agree_with_common_resolver():
    """镜像顺序必须与 `wqb.workflow._common._skill_roots()` 的宿主相对顺序一致。"""
    from wqb.workflow._common import _skill_roots
    common = [Path(p) for p in _skill_roots() if p]
    common_hosts = [p.parent.name for p in common if p.parent.name.startswith(".")]
    mirror = _load_module_from_file(
        SKILL_ROOT_MIRRORS["wq-brain-campaign-toolkit"], "mirror_order_check")
    mirror_hosts = [h for h in mirror.HOST_DIRS if h in common_hosts]
    # 共同出现的宿主，其相对顺序必须与 _common 一致
    assert mirror_hosts == [h for h in common_hosts if h in mirror.HOST_DIRS], (
        f"镜像与 _common 顺序不一致：mirror={mirror_hosts} common={common_hosts}")


def test_skill_root_mirrors_end_with_repo_skills():
    """两份镜像最后兜底必须是仓库自带 Claude/skills（保证 clone 即可用）。"""
    for name, path in SKILL_ROOT_MIRRORS.items():
        mod = _load_module_from_file(path, f"mirror_repo_{name.replace('-', '_')}")
        assert mod.skill_roots()[-1].replace("\\", "/").endswith("Claude/skills"), (
            f"{name} 的 skill_roots() 未以仓库副本兜底：{mod.skill_roots()[-1]}")


# ---------------------------------------------------------------------------
# 6. skills 目录内所有 markdown 的相对链接可解析
# ---------------------------------------------------------------------------

_MD_LINK = re.compile(r"\]\(([^)]+)\)")


@pytest.mark.parametrize("path", sorted(SKILLS_DIR.rglob("*.md")), ids=lambda p: p.name)
def test_relative_links_resolve_in_all_skills_markdown(path: Path):
    if "_unpacked" in path.as_posix():
        pytest.skip("vendored 副本不校验")
    broken = []
    for target in _MD_LINK.findall(_read(path)):
        if target.startswith(("http://", "https://", "#", "mailto:")) or "<" in target:
            continue
        base = target.split("#", 1)[0].strip()
        # 排除占位符/非路径文本（如模板里的 `](url)`、`](a, b, c)`）
        if not base or " " in base or "," in base:
            continue
        if "." not in base and "/" not in base:
            continue
        if (path.parent / base).exists() or (REPO_ROOT / base).exists():
            continue
        broken.append(target)
    assert not broken, f"{path.relative_to(REPO_ROOT).as_posix()} 链接指向不存在的路径：{broken}"


# ---------------------------------------------------------------------------
# 7. skills 树内无 .bak_ 残留
# ---------------------------------------------------------------------------

def test_no_bak_files_inside_skills_tree():
    leftovers = [p.relative_to(REPO_ROOT).as_posix()
                 for p in SKILLS_DIR.rglob("*") if ".bak_" in p.name]
    assert not leftovers, (
        "skills 树内残留 .bak_ 文件（sync 忽略 .bak_ → 永不被发现）：\n" + "\n".join(leftovers[:8]))


# ---------------------------------------------------------------------------
# 8. 旧 skill 名不得回潮（2026-09-10 已全量改成 kebab-case）
# ---------------------------------------------------------------------------

OLD_SKILL_NAMES = ["brain-makeSomeGem", "brain-nextMove-analysis",
                   "brain-simAlphasinBatch-and-track", "brain-how-to-pass-AlphaTest",
                   "brain-calculate-alpha-selfcorrQuick",
                   "brain-inspectRawTemplate-create-Setting", "pull_BRAINSkill"]
ALLOW_OLD = ("旧名", "禁用", "已统一", "此前", "禁止", "迁移", "已归档", "已删除", "不存在的 MCP 名")
_MAPPING_ROW = re.compile(r"^\|\s*`(?:" + "|".join(map(re.escape, OLD_SKILL_NAMES)) + r")`\s*\|\s*`")


def test_no_legacy_skill_names_outside_deprecation_tables():
    bad = []
    for p in SKILLS_DIR.rglob("*.md"):
        if "_unpacked" in p.as_posix():
            continue
        for i, line in enumerate(_read(p).splitlines(), 1):
            for old in OLD_SKILL_NAMES:
                if old in line and not any(a in line for a in ALLOW_OLD) and not _MAPPING_ROW.match(line):
                    bad.append(f"{p.relative_to(REPO_ROOT).as_posix()}:{i}: {old}")
    assert not bad, "旧 skill 名回潮：\n" + "\n".join(bad[:8])


# ---------------------------------------------------------------------------
# 9. sync 工具保留"只增不删"默认，且提供显式 prune 入口
# ---------------------------------------------------------------------------

def test_sync_tool_keeps_safe_default_and_exposes_prune():
    src = _read(SYNC_TOOL)
    assert "--prune-orphans" in src, "sync_skills.py 未提供 --prune-orphans（孤儿清理入口）"
    assert "--apply" in src, "sync_skills.py 的 prune 应默认 dry-run、--apply 才写盘"
