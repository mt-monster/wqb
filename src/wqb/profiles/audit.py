# -*- coding: utf-8 -*-
"""区域 / 组合控制层的只读审计（2026-10-04）。

- `param_sources`：同一区域参数（中性化 / universe）在各处的取值，标出互相矛盾的区；
- `unread_threshold_keys`：thresholds.json 里在代码中找不到读取方的键（棘轮测试的数据源）；
- `region_literal_branches`：代码里按区域代码字面量做的分支 / 查表（区域差异应该在数据层）；
- `split_ratio`：拆分判据——组合的差异化内容占主流程该步正文的比例 + 证据线 + 控制流 + 区域状态。
全部只读：不写库、不改文件。
"""
from __future__ import annotations

import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _root() -> Path:
    from wqb.config import REPO_ROOT
    return REPO_ROOT


# ---------------------------------------------------------------- 参数多源

def _ast_dict_literal(path: Path, var: str) -> Dict[str, Any]:
    """读某个 .py 里名为 var 的字典字面量（找不到返回空）。"""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == var for t in n.targets):
            try:
                return ast.literal_eval(n.value)
            except ValueError:
                return {}
    return {}


def _ast_region_dict_in_call(path: Path, marker: str) -> Dict[str, Any]:
    """读 `{...}.get(region, ...)` 形态的区域字典字面量（以源码里出现 marker 的那一个为准）。"""
    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
    except (OSError, SyntaxError):
        return {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Dict) and n.keys and all(isinstance(k, ast.Constant) for k in n.keys):
            seg = ast.get_source_segment(src, n) or ""
            if marker in seg:
                try:
                    return ast.literal_eval(n)
                except ValueError:
                    continue
    return {}


def param_sources(regions: Optional[List[str]] = None, db: Optional[str] = None) -> List[Dict[str, Any]]:
    """每区一行：中性化 / universe 在各来源的取值与是否矛盾。"""
    from wqb.config import REGIONS
    root = _root()
    rows: List[Dict[str, Any]] = []
    neut_fallback = _ast_dict_literal(root / "src" / "wqb" / "workflow" / "nodes" / "campaign.py", "neut_map")
    uni_fallback = _ast_region_dict_in_call(root / "tools" / "campaign_intel.py", '"TOP2000U"')
    db_rows: Dict[str, Tuple[Any, Any]] = {}
    try:
        from wqb.db_conn import connect, default_db_path
        path = db or default_db_path()
        if os.path.isfile(path):
            conn = connect(path, readonly=True, timeout=5.0)
            try:
                for name, nd, ul in conn.execute("SELECT name, neutralization_default, universe_legal FROM regions"):
                    db_rows[str(name)] = (nd, json.loads(ul) if ul else None)
            finally:
                conn.close()
    except Exception:  # noqa: BLE001
        pass
    from wqb.region_profile import load_profile
    for r in (regions or sorted(REGIONS)):
        r = r.upper()
        st = {}
        sp = root / "tracking" / r / "config" / "settings.json"
        if sp.exists():
            st = json.loads(sp.read_text(encoding="utf-8-sig"))
        prof = load_profile(r)
        static = ((prof.raw if prof else {}) or {}).get("static") or {}
        neut = {
            "settings.json": st.get("neutralization"),
            "profile.static": static.get("neutralization_default"),
            # config.REGIONS[r]["neutralizations"] 是扫描顺序，不是缺省值，不进对照
            "db.regions": (db_rows.get(r) or (None, None))[0],
            "campaign.py 兜底": neut_fallback.get(r, "SUBINDUSTRY" if neut_fallback else None),
        }
        uni = {
            "settings.json": st.get("universe"),
            "profile.static": static.get("universe_default"),
            "config.REGIONS": REGIONS.get(r, {}).get("default_universe"),
            "campaign_intel 兜底": uni_fallback.get(r),
        }
        legal = REGIONS.get(r, {}).get("universes") or []
        db_legal = (db_rows.get(r) or (None, None))[1]
        neut_vals = {str(v).upper() for v in neut.values() if v not in (None, "", "null", "None")}
        uni_vals = {str(v).upper() for v in uni.values() if v not in (None, "", "null", "None")}
        rows.append({
            "region": r, "neutralization": neut, "universe": uni,
            "neutralization_conflict": len(neut_vals) > 1, "universe_conflict": len(uni_vals) > 1,
            "db_universe_legal_drift": sorted(set(db_legal or []) ^ set(legal)) if db_legal else [],
        })
    return rows


# ---------------------------------------------------------------- 未读阈值键

#: **代码扫描的目录口径（单源，2026-10-06 治理评审 P1-6）**。
#: 动因：`tools/code-audit/audit_destructive_default.py` 自己抄了一份扫描范围，
#: 既只覆盖 324/980 个 `.py`（把 `Claude/skills/`、`world-quant-brain-mcp/` 这两堆
#: 执行频率最高的代码留在闸外），又漏了 `.venv` / `site-packages` —— 按文档建议一扩范围
#: 就抱出几千条第三方误报（实测 `pytz/__init__.py` 的时区列表被当成 `subprocess rm`）。
#: 全仓静态扫描类工具一律从本处取，不要再抄第四份。
CODE_DIRS = ("src", "tools", "Claude/skills", "world-quant-brain-mcp")

#: 扫描时必须排除的路径片段（测试 / 归档 / 第三方依赖）。
#: 口径与 `region_literal_branches` 原内置表一致，只补上第三方那几项：
#: 对缺省扫描集（src / tools / Claude/skills/...）行为不变，因为那些目录里
#: 本来就没有 `site-packages` / `node_modules`。
CODE_SKIP_PARTS = (
    "/tests/", "/legacy/", "/attic/", "/vendor/",
    "/.venv/", "/site-packages/", "/node_modules/", "/__pycache__/",
)

_CODE_DIRS = CODE_DIRS  # 历史名，保留已有引用点


def _code_blob(root: Path) -> str:
    parts: List[str] = []
    for base in _CODE_DIRS:
        for f in (root / base).rglob("*.py"):
            n = f.as_posix()
            if "/tests/" in n or f.name.startswith("test_") or "/legacy/" in n or "/attic/" in n or "/.venv/" in n:
                continue
            try:
                parts.append(f.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                pass
    mcp = root / "wqb_db_mcp.py"
    if mcp.exists():
        parts.append(mcp.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts)


def _leaves(d: Any, path: Tuple[str, ...] = ()) -> Iterable[Tuple[str, ...]]:
    if isinstance(d, dict):
        for k, v in d.items():
            yield from _leaves(v, path + (str(k),))
    else:
        yield path


def unread_threshold_keys(root: Optional[Path] = None) -> List[str]:
    """`<区>:<点分键>` 形式：代码里既找不到叶子键字面量（或所在节字面量）的阈值键。粗口径（漏动态拼接的键）。"""
    root = root or _root()
    blob = _code_blob(root)
    out: List[str] = []
    for p in sorted((root / "tracking").glob("*/config/thresholds.json")):
        region = p.parent.parent.name
        data = json.loads(p.read_text(encoding="utf-8-sig"))
        for leaf in _leaves(data):
            if not leaf or any(x.startswith("_") or x.startswith("$") for x in leaf):
                continue
            key, sec = leaf[-1], leaf[0]
            ok = (f'"{key}"' in blob or f"'{key}'" in blob) and (
                len(leaf) == 1 or f'"{sec}"' in blob or f"'{sec}'" in blob)
            if not ok:
                out.append(f"{region}:{'.'.join(leaf)}")
    return out


# ---------------------------------------------------------------- 区域字面量分支

def _region_codes() -> set:
    from wqb.config import REGIONS
    return set(REGIONS)


def region_literal_branches(paths: Optional[List[Path]] = None, root: Optional[Path] = None) -> List[str]:
    """`<相对路径>:<种类>:<涉及区域>` —— 比较 / in 判断里的区域字面量，以及 ≥3 个区域码作键的字典字面量。

    不报：config.py（区域常量的家）、测试、legacy / attic、本模块与 taxonomy 自身。按「路径 + 种类 + 区域集合」去重，
    与行号无关（文件挪行不会让棘轮误报）。
    """
    root = root or _root()
    codes = _region_codes()
    files = paths or [f for base in ("src", "tools", "Claude/skills/wq-brain-campaign-toolkit/scripts")
                      for f in (root / base).rglob("*.py")]
    skip_parts = CODE_SKIP_PARTS  # 单源（原内置表与本处同序，2026-10-06 收敛到 CODE_SKIP_PARTS）
    skip_files = {"src/wqb/config.py", "src/wqb/profiles/audit.py", "src/wqb/profiles/taxonomy.py"}
    found: set = set()
    for f in files:
        rel = f.resolve().relative_to(root.resolve()).as_posix()
        if any(s in "/" + rel for s in skip_parts) or rel in skip_files or f.name.startswith("test_"):
            continue
        try:
            tree = ast.parse(f.read_text(encoding="utf-8", errors="ignore"))
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Compare):
                lits = []
                for node in [n.left, *n.comparators]:
                    if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in codes:
                        lits.append(node.value)
                    elif isinstance(node, (ast.Tuple, ast.List, ast.Set)):
                        lits += [e.value for e in node.elts if isinstance(e, ast.Constant) and e.value in codes]
                if lits:
                    found.add(f"{rel}:compare:{','.join(sorted(set(lits)))}")
            elif isinstance(n, ast.Dict):
                keys = [k.value for k in n.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
                hit = sorted(set(keys) & codes)
                if len(hit) >= 3:
                    found.add(f"{rel}:dict:{','.join(hit)}")
    return sorted(found)


# ---------------------------------------------------------------- 拆分判据

def _chars(text: str) -> int:
    text = re.sub(r"```.*?```", "", text or "", flags=re.S)
    return len(re.sub(r"\s+", "", text))


def _main_step_body(step: int, root: Path) -> int:
    ra = root / "Claude" / "skills" / "wq-brain-ra-pipeline"
    skill = (ra / "SKILL.md").read_text(encoding="utf-8")
    sec = 0
    for part in re.split(r"(?m)^### ", skill)[1:]:
        if part.startswith(f"步 {step}"):
            sec = _chars(part)
    ref = {3: "step3-s1-semantic.md", 4: "step4-generation.md", 7: "step7-diagnose.md"}.get(step)
    return sec + (_chars((ra / "references" / ref).read_text(encoding="utf-8")) if ref else 0)


def split_ratio(region: str, root: Optional[Path] = None, min_wins: int = 2, min_dead: int = 5) -> List[Dict[str, Any]]:
    """每个组合一行：S2 / S4 差异化内容占比、证据线、控制流差异、区域状态 → 是否够格拆成独立 skill。

    差异化内容只算组合**自己的**知识（cells.json 的 generation / s4 / 覆盖值 + 分支文件手写块），
    不算自动汇总的证据清单与从类别卡 / 全局带进来的通用内容。四条同时满足才 eligible：
      ① 占比 > 30%（用户判据）② 控制流不同（组合声明了 `flow` 级差异：新步骤 / 新工具 / 新停止规则）
      ③ 证据线：≥ min_wins 条胜绩，或 ≥ min_dead 条判死 ④ 区域 entry_verdict = active
    """
    from .cells import load_cells
    from .render import get_block, skill_dir
    root = root or _root()
    data = load_cells(region)
    try:
        from wqb.region_profile import load_profile
        prof = load_profile(region.upper())
        verdict = (prof.entry_verdict if prof else "") or "unknown"
    except Exception:  # noqa: BLE001
        verdict = "unknown"
    body = {s: _main_step_body(s, root) for s in (4, 7)}
    rows = []
    for cat, c in sorted((data.get("cells") or {}).items()):
        gen = c.get("generation") or {}
        s4 = c.get("s4") or {}
        own2 = json.dumps({k: gen.get(k) for k in ("use", "avoid", "skeletons", "notes")}, ensure_ascii=False)
        own4 = json.dumps({"s4": s4, "bt": c.get("backtest"), "th": c.get("thresholds")}, ensure_ascii=False)
        doc = skill_dir(region) / "references" / f"{cat}.md"
        manual = get_block(doc.read_text(encoding="utf-8"), "manual") if doc.exists() else ""
        r2 = _chars(own2) / body[4] if body[4] else 0.0
        r4 = (_chars(own4) + _chars(manual or "")) / body[7] if body[7] else 0.0
        ev = c.get("evidence") or {}
        evidence_ok = len(ev.get("wins") or []) >= min_wins or len(ev.get("dead_ends") or []) >= min_dead
        flow = bool(c.get("flow"))
        eligible = max(r2, r4) > 0.30 and flow and evidence_ok and verdict == "active"
        rows.append({"region": region.upper(), "category": cat, "s2_ratio": round(r2, 3), "s4_ratio": round(r4, 3),
                     "evidence_ok": evidence_ok, "control_flow": flow, "entry_verdict": verdict,
                     "split_eligible": eligible})
    return rows
