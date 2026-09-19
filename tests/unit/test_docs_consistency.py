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
    # 2026-09-17 #8：语义由"整节缺失→静默放行"改为 fail-closed（回落默认+告警）。
    assert "fail-closed" in contract, "contract 未说明 signal_floor 缺配置时的 fail-closed 语义"
    assert "enabled:false" in contract, "contract 未说明唯一的放行开关（显式 enabled:false）"


def test_signal_floor_docs_state_authoritative_location_and_real_region_count():
    """2026-09-17 P2-12：文档须写明①权威位置 ②真实的 13/13 覆盖数。

    起因：正文曾记「11 区已配」（漏计 AMR/GLB），并把 `thresholds.json` 与
    references/regions/*.md 的 profile 混为一谈。数目必须与磁盘实况一致。
    """
    import glob as _glob
    import json as _json

    # ① 磁盘实况：从配置反推，而不是在测试里硬写数字
    paths = sorted(
        _glob.glob(str(REPO_ROOT / "tracking" / "*" / "config" / "thresholds.json"))
    )
    configured = []
    for p in paths:
        try:
            d = _json.loads(open(p, encoding="utf-8").read())
        except Exception:
            continue
        if (d.get("diversity") or {}).get("signal_floor") is not None:
            configured.append(Path(p).parts[-3])
    assert len(configured) == len(paths) > 0, (
        f"signal_floor 覆盖不完整：{len(configured)}/{len(paths)}"
    )

    # ② 文档口径须与实况一致
    skill = _read(RA_PIPELINE / "SKILL.md")
    assert "diversity.signal_floor" in skill
    assert "唯一权威位置" in skill, "未写明 signal_floor 的权威位置"
    assert f"{len(configured)}/{len(configured)} 区域均已配该节" in skill, (
        f"文档未记录真实的区域覆盖数 {len(configured)}/{len(configured)}"
    )
    assert "11 个区域" not in skill, "仍残留过期的「11 个区域」表述"


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
# 2026-09-13 更新：run_pipeline.py 于 09-12 模块化拆分时把解析逻辑下沉到
# pipeline_paths.py（run_pipeline 本体已无内联搜索链），锚点随之迁移。
ROOT_RESOLVERS = [
    SKILLS_DIR / "brain-make-some-gem/scripts/trailSomeAlphas/pipeline_paths.py",
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


# ---------------------------------------------------------------------------
# 10. last_verified 新鲜度（2026-09-12 新增：内容改了元数据没改 = 漂移）
# ---------------------------------------------------------------------------

#: 容差：last_verified 允许落后最后一次提交至多 2 天（同日多轮编辑不计漂移）
LV_GRACE_DAYS = 2


def _skill_md_files() -> list[Path]:
    return sorted(p for p in SKILLS_DIR.glob("*/SKILL.md"))


def _last_commit_date(path: Path) -> str | None:
    import subprocess
    r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path.as_posix()],
                       capture_output=True, text=True)
    return r.stdout.strip() or None


@pytest.mark.parametrize("path", _skill_md_files(), ids=lambda p: p.parent.name)
def test_last_verified_not_older_than_last_commit(path: Path):
    text = _read(path)
    m = re.search(r"^last_verified:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    assert m, f"{path.parent.name} 缺 last_verified"
    lv = m.group(1)
    cd = _last_commit_date(path)
    if not cd:
        pytest.skip("无 git 提交历史")
    assert lv >= cd, (
        f"{path.parent.name}: last_verified={lv} 落后最后一次内容提交（{cd}）——"
        f"内容已变而元数据未复核。修法：复核内容后更新 frontmatter last_verified，不要放宽本断言")


# ---------------------------------------------------------------------------
# 11. 工具/节点计数只能引用 INDEX 基准段（2026-09-12 新增：根治 66/68/7 节点口径分裂）
# ---------------------------------------------------------------------------

#: 命中即检查的计数写法（工具数 / 节点数）；行内必须同时引用 INDEX 基准段才放行
BARE_COUNT = re.compile(
    r"\b(?:66|68)\s*(?:个)?\s*工具|\b(?:3[2-9])\s*(?:个)?\s*工具|[7７]\s*个节点|七个节点|7 个 workflow 节点")
COUNT_REF_MARKS = ("INDEX", "唯一基准", "测试守护", "计数基准段")


def test_no_bare_tool_or_node_counts_outside_index():
    bad = []
    for p in SKILLS_DIR.rglob("*.md"):
        if "_unpacked" in p.as_posix() or p == INDEX_MD:
            continue
        for i, line in enumerate(_read(p).splitlines(), 1):
            if BARE_COUNT.search(line) and not any(k in line for k in COUNT_REF_MARKS):
                bad.append(f"{p.relative_to(REPO_ROOT).as_posix()}:{i}: {line.strip()[:90]}")
    assert not bad, (
        "skill 文档裸写工具/节点计数（口径唯一基准 = INDEX.md「MCP 工具/节点计数基准段」）：\n"
        + "\n".join(bad[:8]))


def test_mcp_tool_counts_match_index():
    """INDEX 基准段的 68 必须等于 tools_*.py 装饰器实数——注册变了测试即红。"""
    tools_dir = REPO_ROOT / "world-quant-brain-mcp"
    per_module = {}
    for p in sorted(tools_dir.glob("tools_*.py")):
        n = len(re.findall(r"^@mcp\.tool", _read(p), re.M))
        per_module[p.stem] = n
    total = sum(per_module.values())
    idx = _read(INDEX_MD)
    assert f"**{total} 个工具**" in idx, (
        f"INDEX 基准段写 {total} 个工具？实测装饰器合计 {total}（{per_module}）——同步 INDEX")
    for mod, n in per_module.items():
        assert f"`{mod}` {n}" in idx, f"INDEX 基准段缺 {mod} 的计数 {n}"
    # workflow 节点数：改为**从 registry 实算**（2026-09-17）。
    # 此前写死 `assert "**18 个**" in idx` —— 那只是在断言"INDEX 里出现过 18 这个串"，
    # 节点增删时 INDEX 不改也照样通过（裸数字不守护必漂，与本函数下方 wqb-db 的那条教训同源）。
    # 现在和 wqb-db 一样机械对齐实数。
    sys.path.insert(0, str(REPO_ROOT / "src"))
    from wqb.workflow.registry import get_registry
    _reg = get_registry()
    n_nodes = len(_reg.list_nodes()) if hasattr(_reg, "list_nodes") else len(_reg._nodes)
    assert f"- workflow 节点：**{n_nodes} 个**" in idx, (
        f"INDEX 基准段 workflow 节点数与 registry 实数 {n_nodes} 不符——同步 INDEX")
    # wqb-db 同样机械守护（2026-09-15：此前只靠人工改数，region_rotation/seal_dead_end
    # 落地后基准仍写 33、实数已是 35——裸数字不守护必漂）
    n_db = len(re.findall(r"^@mcp\.tool", _read(REPO_ROOT / "wqb_db_mcp.py"), re.M))
    assert f"`wqb-db` 服务器：**{n_db} 个工具**" in idx, (
        f"INDEX 基准段 wqb-db 计数与 wqb_db_mcp.py 装饰器实数 {n_db} 不符——同步 INDEX")


def test_node_registration_audit_is_clean():
    """workflow 节点「四处同步」审计必须干净（2026-09-18 固化）。

    背景：`alpha_booster` 只注册了 registry，另三处漏同步 → 3 个测试红；
    `gem` 的 NodeMeta 漏 `batch_size` 也属同一类漂移。四个位置本身各有测试守护，
    但它们**分散在三个文件**，失败时看到的是零散的红，不是"你漏了哪几处"。

    本测试直接调 `tools/audit_node_registration.py` 的审计逻辑，把四处做成一张对照表：
    registry / test_workflow 期望集合 / _DRY_RUN_CASES / INDEX 计数。
    这样"加节点漏同步"会在这里一次性暴露，而不是在三个文件里各红一条。

    失败时跑：`python tools/audit_node_registration.py`（会列出全部缺口与修复方向）。
    """
    import importlib.util

    tool = REPO_ROOT / "tools" / "audit_node_registration.py"
    assert tool.exists(), "审计工具缺失：tools/audit_node_registration.py"
    spec = importlib.util.spec_from_file_location("_audit_node_reg", tool)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    reg = mod._load_registry()
    nodes = set(reg.list_nodes())
    problems = []

    tw = mod._parse_test_workflow_nodes()
    if nodes - tw:
        problems.append(f"test_workflow 期望集合缺 {sorted(nodes - tw)}")
    if tw - nodes:
        problems.append(f"test_workflow 期望集合多 {sorted(tw - nodes)}（registry 已无此节点）")

    dr = mod._parse_dry_run_cases()
    if nodes - dr:
        problems.append(f"_DRY_RUN_CASES 缺 {sorted(nodes - dr)}")
    if dr - nodes:
        problems.append(f"_DRY_RUN_CASES 多 {sorted(dr - nodes)}")

    drift = mod._signature_drift(reg)
    if drift:
        problems.append(f"NodeMeta 与 run() 签名漂移：{drift}")

    idx_count = mod._parse_index_node_count()
    if idx_count != len(nodes):
        problems.append(f"INDEX 记 {idx_count} 个，registry 实为 {len(nodes)} 个")

    assert not problems, (
        "workflow 节点四处不同步（跑 `python tools/audit_node_registration.py` 看修复方向）：\n  - "
        + "\n  - ".join(problems)
    )


def test_ppa_mining_and_ra_pipeline_reference_count_baseline():
    """曾经的 66/32 与 68/33 分裂点，必须已改为引用基准段。"""
    for f in (SKILLS_DIR / "wq-brain-ppa-mining" / "SKILL.md", RA_PIPELINE / "SKILL.md"):
        t = _read(f)
        assert "INDEX.md" in t and "计数基准" in t, f"{f.parent.name} 未引用计数基准段"
        assert "66 工具" not in t and "32 工具" not in t


# ---------------------------------------------------------------------------
# 12. 禁止工作区绝对路径（2026-09-12 新增：换机即断）
# ---------------------------------------------------------------------------

def test_no_workspace_absolute_path_in_skills_and_docs():
    bad = []
    pat = re.compile(r"[A-Za-z]:[\\/]+coding[\\/]+traeCN_project")
    for base in (SKILLS_DIR, REPO_ROOT / "docs"):
        for p in base.rglob("*.md"):
            if "_unpacked" in p.as_posix():
                continue
            if "docs/plans" in p.as_posix().replace("\\", "/"):
                continue  # docs/plans/ 是历史计划归档（只读记录，记载当时的绝对路径属正常）
            for i, line in enumerate(_read(p).splitlines(), 1):
                if pat.search(line):
                    bad.append(f"{p.relative_to(REPO_ROOT).as_posix()}:{i}: {line.strip()[:90]}")
    assert not bad, "出现工作区绝对路径（应改仓库根相对路径）：\n" + "\n".join(bad[:8])

# ---------------------------------------------------------------------------
# 13. 算子三表一致性 + feature-implementation 正本/副本 parity（2026-09-12 全量精读 P0）
# ---------------------------------------------------------------------------

def _load_json(path: Path):
    return json.loads(_read(path))


def test_operator_configs_consistent():
    """known_ops 唯一真值 = operators_verified.verified；semantics 未验证项必须显式标注。"""
    ov = _load_json(REPO_ROOT / "data" / "operators_verified.json")
    verified = set(ov["verified"])
    pc = _load_json(SKILLS_DIR / "wq-brain-campaign-toolkit" / "config" / "platform_constraints.json")
    sem = _load_json(SKILLS_DIR / "wq-brain-campaign-toolkit" / "config" / "operator_semantics.json")
    assert set(pc["known_ops"]) == verified, (
        "platform_constraints.known_ops 与 operators_verified.verified 不一致——"
        "known_ops 唯一真值是 verified（平台 get_operators 实测），先对账再改")
    unverified = {k for k, v in sem["operators"].items()
                  if isinstance(v, dict) and str(v.get("_status", "")).startswith("unverified")}
    assert set(sem["operators"]) - unverified == verified, (
        f"operator_semantics 与 verified 漂移："
        f"多={sorted(set(sem['operators']) - verified - unverified)} "
        f"少={sorted(verified - set(sem['operators']))}")
    ghosts = pc.get("ghost_ops")
    assert isinstance(ghosts, list) and len(ghosts) >= 10, (
        "platform_constraints 缺 ghost_ops（权威=ledger KB/community_tpl_kb.ghost_operator_advisory）")


def test_feature_impl_vendored_matches_canonical():
    """gem 内嵌副本与正本必须逐文件一致（2026-09-12 已回灌同步；分叉即红）。"""
    import hashlib
    vend = SKILLS_DIR / "brain-make-some-gem" / "scripts" / "trailSomeAlphas" / "skills" / "brain-feature-implementation" / "scripts"
    canon = SKILLS_DIR / "brain-feature-implementation" / "scripts"
    assert vend.is_dir() and canon.is_dir()
    vfiles = {p.name for p in vend.glob("*.py")}
    cfiles = {p.name for p in canon.glob("*.py")}
    assert vfiles == cfiles, f"两侧文件集合不一致：仅副本={sorted(vfiles-cfiles)} 仅正本={sorted(cfiles-vfiles)}"
    bad = []
    for name in sorted(vfiles):
        hv = hashlib.md5((vend / name).read_bytes()).hexdigest()
        hc = hashlib.md5((canon / name).read_bytes()).hexdigest()
        if hv != hc:
            bad.append(name)
    assert not bad, f"gem 内嵌副本与正本分叉（禁止第二实现）：{bad}——以 gem 运行版为准回灌正本后提交"

# ---------------------------------------------------------------------------
# 14. 模板族的算子合法性（2026-09-13 落地论坛「一阶变换族」）
# ---------------------------------------------------------------------------

_OP_CALL = re.compile(r"([a-z_][a-z_0-9]*)\s*\(")


def test_template_families_only_use_verified_operators():
    """每个族的 skeleton / skeleton_variants 只能用 verified 算子。

    动机：论坛高赞模板帖常引用幽灵算子（ts_entropy / ts_decay_exp_window 等），
    直接抄进族里会让整批回测静默失败。本测试把「算子真值」焊死在族的定义上。
    """
    ov = _load_json(REPO_ROOT / "data" / "operators_verified.json")
    verified = set(ov["verified"])
    pc = _load_json(SKILLS_DIR / "wq-brain-campaign-toolkit" / "config" / "platform_constraints.json")
    banned = set(pc.get("ghost_ops") or []) | set(pc.get("inaccessible_ops") or [])

    cfg = _load_json(SKILLS_DIR / "wq-brain-campaign-toolkit" / "config" / "template_families.json")
    offenders = {}
    for fam in cfg["families"]:
        exprs = [str(fam.get("skeleton") or "")]
        exprs += [v.get("expr", "") for v in (fam.get("skeleton_variants") or []) if isinstance(v, dict)]
        bad = set()
        for e in exprs:
            for op in _OP_CALL.findall(e):
                if op not in verified or op in banned:
                    bad.add(op)
        if bad:
            offenders[fam.get("family_id")] = sorted(bad)
    assert not offenders, (
        f"模板族使用了非 verified 算子（幽灵/不可访问或未登记）：{offenders}——"
        f"算子真值 = data/operators_verified.json 的 verified")


def test_first_order_transform_family_landed():
    """论坛「一阶变换族」必须存在且 9 条变体齐全（原帖称 10 条但正文实列 9 条）。"""
    cfg = _load_json(SKILLS_DIR / "wq-brain-campaign-toolkit" / "config" / "template_families.json")
    fam = next((f for f in cfg["families"] if f.get("family_id") == "first_order_transform"), None)
    assert fam is not None, "first_order_transform 族缺失"
    variants = fam.get("skeleton_variants") or []
    assert len(variants) == 9, f"变体数应为 9，实际 {len(variants)}"
    names = [v["name"] for v in variants]
    assert names == ["slope", "growth_rate", "ar_slope", "squared_momentum", "decay_momentum",
                     "rank_reversal", "log_smooth", "signed_power", "delta_stack"]
    assert fam["status"] == "candidate_unverified"
    assert set(fam["forbidden_operators"]) >= {"ts_entropy", "ts_decay_exp_window", "ts_skewness"}

