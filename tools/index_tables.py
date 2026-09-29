# -*- coding: utf-8 -*-
"""index_tables.py — INDEX.md / docs/env_and_switches.md 里「可由代码导出的表」的生成器。

背景（skills 审查 IX-05 / IX-10 / IX-13，2026-09-29）：INDEX 里的区域表是人写的，与 profile / 目录不符两处
（DEU 写 active 而 profile 是 probe-only；AMR 写「无战役目录」而 `tracking/AMR/config/` 存在）；「平台硬线 Sharpe > 1.58」
一个词对应三个数；环境变量与开关只散落在变更日志里，没有目录。通则（报告 X-7）：**能由代码导出的表，由代码生成并嵌入文档，
测试比对生成物与已提交文档**。

    python tools/index_tables.py regions          # 区域清单表（config.REGIONS × profile × tracking 目录）
    python tools/index_tables.py ladder           # 闸门阶梯表（按检查名：平台线 / 内部线 / 来源常量）
    python tools/index_tables.py env              # 环境变量目录表（代码扫描 + docs/env_registry.json 的用途）
    python tools/index_tables.py --check          # 三块与文档里的嵌入块逐字比对（退出码 1 = 漂移）
    python tools/index_tables.py --apply          # 用生成结果覆盖文档里的嵌入块

嵌入块用 `<!-- NAME:start -->` / `<!-- NAME:end -->` 包起来（NAME = region-table / gate-ladder / env-table）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

INDEX = REPO / "Claude" / "skills" / "INDEX.md"
ENV_DOC = REPO / "docs" / "env_and_switches.md"
ENV_REGISTRY = REPO / "docs" / "env_registry.json"
PROFILES = REPO / "Claude" / "skills" / "wq-brain-ra-pipeline" / "references" / "regions"
TRACKING = REPO / "tracking"

#: 块名 → (承载文档, 生成函数名)
BLOCKS = {
    "region-table": INDEX,
    "gate-ladder": INDEX,
    "env-table": ENV_DOC,
}


# ----------------------------------------------------------------------------- 区域表

def _front_matter_value(path: Path, key: str) -> Optional[str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    mm = re.search(rf"^{re.escape(key)}:\s*(\S+)", m.group(1), re.M)
    return mm.group(1).strip("\"'") if mm else None


def region_rows() -> List[dict]:
    from wqb.config import REGIONS
    rows = []
    for r in sorted(REGIONS):
        prof = PROFILES / f"{r}.md"
        cfg = TRACKING / r / "config"
        rows.append({
            "region": r,
            "profile": prof.is_file(),
            "tracking": (cfg / "settings.json").is_file() and (cfg / "thresholds.json").is_file(),
            "entry_verdict": (_front_matter_value(prof, "entry_verdict") or "?") if prof.is_file() else "—",
        })
    return rows


def _region_behaviour(row: dict) -> str:
    if not row["profile"]:
        return "无 profile：走通用处女地模板（参照 ASI），**先补 profile** 再开波"
    ev = row["entry_verdict"]
    parts = []
    if ev == "frozen":
        parts.append("步 1 即拒，不进步 2（后门见 RA `scenarios.md` 情景 RA-08）")
    elif ev == "probe-only":
        parts.append("只许探针批，不开常规波（探针上限见 profile）")
    if not row["tracking"]:
        parts.append("无战役目录：开波前先补 `tracking/%s/config/{settings,thresholds}.json`" % row["region"])
    return "；".join(parts) or "—"


def render_regions() -> str:
    lines = ["| region | profile | `tracking/<R>/config/` | `entry_verdict` | 步 1 的行为 |", "|---|---|---|---|---|"]
    for row in region_rows():
        lines.append("| %s | %s | %s | %s | %s |" % (
            row["region"], "✓" if row["profile"] else "✗ 未建", "✓" if row["tracking"] else "✗",
            f"`{row['entry_verdict']}`" if row["profile"] else "—", _region_behaviour(row)))
    return "\n".join(lines)


# ----------------------------------------------------------------------------- 闸门阶梯

def _pct(x: float) -> str:
    return f"{x * 100:g}%"


def render_ladder() -> str:
    from wqb import config as C
    i, p, pl = C.GATES_INTERNAL, C.GATES_PLATFORM, C.PLATFORM_CHECK_LINES
    lo, hi = i["turnover_range"]
    plo, phi = pl["turnover_range"]
    rows = [
        ("IS Sharpe（`LOW_SHARPE`）",
         f"Delay-1 > {pl['low_sharpe_min']['delay1']:g} / Delay-0 > {pl['low_sharpe_min']['delay0']:g}",
         f"> {i['sharpe_min']:g}", "`PLATFORM_CHECK_LINES.low_sharpe_min` / `GATES_INTERNAL.sharpe_min`"),
        ("2Y Sharpe（`LOW_2Y_SHARPE` / `IS_LADDER_SHARPE`）",
         f"> {pl['low_2y_sharpe_min']:g}", "—（内部线已取 1.58）",
         "`PLATFORM_CHECK_LINES.low_2y_sharpe_min`；提交准入线 `GATES_PLATFORM.sharpe_min` 取的就是它"),
        ("Fitness（`LOW_FITNESS`）",
         f"Delay-1 > {pl['low_fitness_min']['delay1']:g} / Delay-0 > {pl['low_fitness_min']['delay0']:g}",
         f"> {i['fitness_min']:g}", "`PLATFORM_CHECK_LINES.low_fitness_min` / `GATES_INTERNAL.fitness_min`"),
        ("换手（`LOW_TURNOVER` / `HIGH_TURNOVER`）",
         f"∈ [{_pct(plo)}, {_pct(phi)}]", f"∈ [{_pct(lo)}, {_pct(hi)}]",
         "`PLATFORM_CHECK_LINES.turnover_range` / `GATES_INTERNAL.turnover_range`"),
        ("Margin", "平台不检", f"> {i['margin_bp_min']:g} bp", "`GATES_INTERNAL.margin_bp_min`"),
        ("Returns", "平台不检", f"> {_pct(i['returns_min'])}", "`GATES_INTERNAL.returns_min`"),
        ("SELF 相关性", f"< {p['self_corr_max']:g}", f"< {i['self_corr_max']:g}",
         "`GATES_PLATFORM.self_corr_max` / `GATES_INTERNAL.self_corr_max`"),
        ("PROD 相关性", f"< {p['prod_corr_max']:g}", "—", "`GATES_PLATFORM.prod_corr_max`（= `PRODCORR_CEILING`）"),
    ]
    lines = ["| 检查 | 平台线（提交必须） | 内部线（研究阶段，省配额） | 来源常量（`src/wqb/config.py`） |", "|---|---|---|---|"]
    for name, plat, internal, const in rows:
        lines.append(f"| {name} | {plat} | {internal} | {const} |")
    return "\n".join(lines)


# ----------------------------------------------------------------------------- 环境变量

#: 不扫描的目录 / 文件（归档、测试、第三方）
_SKIP_PARTS = {".venv", "attic", "__pycache__", "tests", "legacy", "node_modules", ".git"}
_SCAN_ROOTS = ("src", "tools", "world-quant-brain-mcp", "Claude/skills", "wqb_db_mcp.py")
_ENV_CALL = re.compile(
    r"""(?:os\.environ\.get|os\.environ\.setdefault|os\.getenv|environ\.get|getenv)\(\s*['"]([A-Z][A-Z0-9_]{3,})['"]\s*(?:,\s*([^)\n]+?))?\s*\)""")
#: 传进函数的 `env` 字典（`env.get("WQB_WAIVER_MODE")`）——只认本项目前缀，避免把任意字典键当环境变量
_PREFIXES = "WQB|WQ|BRAIN|CREDENTIALS|MOONSHOT|GEM|FORUM|LABS|MCP|REDIS|CAMPAIGN|OPENAI|FE|API|BACKFILL"
_ENV_DICT = re.compile(
    rf"""\b(?:env|environ|_env|environment)\.get\(\s*['"]((?:{_PREFIXES})_[A-Z0-9_]+)['"]\s*(?:,\s*([^)\n]+?))?\s*\)""")
_ENV_SUB = re.compile(r"""os\.environ\[\s*['"]([A-Z][A-Z0-9_]{3,})['"]\s*\]""")
_LITERAL = re.compile(r"""^(?:['"]([^'"]*)['"]|(-?\d+(?:\.\d+)?))$""")


def _iter_py() -> List[Path]:
    out = []
    for root in _SCAN_ROOTS:
        p = REPO / root
        cands = [p] if p.is_file() else sorted(p.rglob("*.py"))
        for f in cands:
            rel = f.relative_to(REPO)
            if any(part in _SKIP_PARTS for part in rel.parts) or f.name.startswith("test_"):
                continue
            out.append(f)
    return out


def scan_env() -> Dict[str, dict]:
    """代码里读取 / 设置的环境变量：名 → {readers: [相对路径…], default: 字面量默认值或 None}。"""
    found: Dict[str, dict] = {}
    for f in _iter_py():
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = f.relative_to(REPO).as_posix()
        for m in list(_ENV_CALL.finditer(text)) + list(_ENV_DICT.finditer(text)):
            e = found.setdefault(m.group(1), {"readers": set(), "default": None})
            e["readers"].add(rel)
            if m.group(2) and e["default"] is None:
                lit = _LITERAL.match(m.group(2).strip())
                if lit:
                    e["default"] = lit.group(1) if lit.group(1) is not None else lit.group(2)
        for m in _ENV_SUB.finditer(text):
            found.setdefault(m.group(1), {"readers": set(), "default": None})["readers"].add(rel)
    for e in found.values():
        e["readers"] = sorted(e["readers"])
    return found


def load_registry() -> dict:
    return json.loads(ENV_REGISTRY.read_text(encoding="utf-8"))


def _short_path(rel: str) -> str:
    return rel.replace("Claude/skills/", "").replace("world-quant-brain-mcp/", "mcp/")


def render_env() -> str:
    reg = load_registry()
    scanned = scan_env()
    lines: List[str] = []
    for cat, title in reg["categories"].items():
        names = [n for n, v in reg["vars"].items() if v["cat"] == cat and n in scanned]
        if not names:
            continue
        lines += [f"#### {title}", "", "| 变量 | 缺省 | 作用 | 读取方（代码扫描） | 起效 |", "|---|---|---|---|---|"]
        for n in names:
            info, meta = scanned[n], reg["vars"][n]
            default = f"`{info['default']}`" if info["default"] not in (None, "") else "—"
            readers = [f"`{_short_path(r)}`" for r in info["readers"][:2]]
            if len(info["readers"]) > 2:
                readers.append(f"+{len(info['readers']) - 2}")
            lines.append(f"| `{n}` | {default} | {meta['what']} | {' · '.join(readers)} | {meta.get('since', '—')} |")
        lines.append("")
    return "\n".join(lines).rstrip()


# ----------------------------------------------------------------------------- 嵌入

_RENDER = {"region-table": render_regions, "gate-ladder": render_ladder, "env-table": render_env}


def _block_re(name: str) -> "re.Pattern[str]":
    return re.compile(rf"(<!-- {re.escape(name)}:start -->)(.*?)(<!-- {re.escape(name)}:end -->)", re.S)


def embedded(name: str) -> Optional[str]:
    m = _block_re(name).search(BLOCKS[name].read_text(encoding="utf-8"))
    return m.group(2).strip("\n") if m else None


def drifted() -> List[Tuple[str, str]]:
    bad = []
    for name in BLOCKS:
        cur = embedded(name)
        if cur is None:
            bad.append((name, "文档里没有嵌入块"))
        elif cur.strip() != _RENDER[name]().strip():
            bad.append((name, "嵌入块与生成结果不一致"))
    return bad


def apply() -> List[str]:
    changed = []
    for name, doc in BLOCKS.items():
        text = doc.read_text(encoding="utf-8")
        rx = _block_re(name)
        m = rx.search(text)
        if not m:
            print(f"[ERROR] {doc.relative_to(REPO)} 缺 <!-- {name}:start/end --> 标记", file=sys.stderr)
            continue
        new = rx.sub(lambda mm: mm.group(1) + "\n" + _RENDER[name]() + "\n" + mm.group(3), text, count=1)
        if new != text:
            doc.write_text(new, encoding="utf-8")
            changed.append(name)
    return changed


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("what", nargs="?", choices=["regions", "ladder", "env"], help="打印某一块")
    ap.add_argument("--check", action="store_true", help="嵌入块与生成结果逐字比对（退出码 1 = 漂移）")
    ap.add_argument("--apply", action="store_true", help="用生成结果覆盖文档里的嵌入块")
    a = ap.parse_args(argv)
    if a.check:
        bad = drifted()
        for name, why in bad:
            print(f"[DRIFT] {name}: {why}\n        修复：python tools/index_tables.py --apply", file=sys.stderr)
        if not bad:
            print("[OK] 三个嵌入块与生成结果一致")
        return 1 if bad else 0
    if a.apply:
        for name in apply():
            print(f"[APPLIED] {name}")
        return 0
    if a.what:
        print({"regions": render_regions, "ladder": render_ladder, "env": render_env}[a.what]())
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
