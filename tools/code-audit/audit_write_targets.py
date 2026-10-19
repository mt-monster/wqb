#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""audit_write_targets — 断言所有写盘目标命中 §8.13 白名单目录（2026-10-20 新增）。

为什么要有这个工具
------------------
2026-10-20 目录结构审计（`reports/repo_structure_and_write_output_audit_20261020.md`）发现：
`src/wqb/search/scheduler.py` 里 `prepare_session_pack(materialize=True)` 曾用
``pack_dir = os.path.join("tracking", "sessions", date)`` —— **相对 cwd**。
后果实测：跑 `pytest tests/unit/09_core/test_handoff.py` 时，测试直接往真
`tracking/sessions/2026-04-22/` 写了 `agent-brief.md` + `mcp-plan.json`
（.gitignore 未覆盖 tracking/，直接污染版本库未跟踪区）。

同类模式在此前是「顶层游离件」的成因：脚本落到 `tools/` 或根目录的产物，
没人知道该往哪归，最后变成结构治理的存量债。§8.13 目录职责表是**约定**，
没有机械检查在守护它 —— 本工具补上这条。

判定规则
--------
用 AST 定位所有写盘调用点，然后**沿赋值图回溯**（最多 2 层）把路径从变量名
解析成字面量，再对照 §8.13 白名单分类：

  ✅ 允许：`output_report/` · `tracking/<REG>/`（3 字母区域码）· `cache/` ·
           `logs/` · `results/` · `data/` · `tempfile` / `tmp_path` / `mkdtemp` /
           `gettempdir` / `/tmp/` · `WQB_ROOT` / `WQB_TASK_ROOT` env 注入 ·
           `REPO_ROOT` 锚定的等价形式 · `Path(__file__)` 相对 · `.gitignore`
  ⚠️ 违规：裸相对路径（落调用方 cwd）· 落进代码目录 `src/` / `tools/` ·
           落进人工面 `docs/` / `reports/`（除非该工具已登记为生成器）

**只报新增，不追存量**（棘轮，与 `audit_destructive_default.py` 同套语义）：
基线存 `tests/fixtures/write_targets_baseline.json`。行号不入库 ——
无关改动会让行号漂移。

用法
----
    python tools/code-audit/audit_write_targets.py                  # 棘轮：只报新增违规
    python tools/code-audit/audit_write_targets.py --all            # 连白名单命中一起列
    python tools/code-audit/audit_write_targets.py --json
    python tools/code-audit/audit_write_targets.py --update-baseline
退出码：0 = 无新增违规 / 1 = 有新增违规 / 2 = 工具故障
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ------------------------------------------------------------------ 自举
def _bootstrap_src() -> None:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()

from wqb.paths import find_repo_root  # noqa: E402
from wqb.profiles.audit import CODE_DIRS, CODE_SKIP_PARTS  # noqa: E402  扫描口径单源

REPO = find_repo_root(__file__)
BASELINE = REPO / "tests" / "fixtures" / "write_targets_baseline.json"


# ------------------------------------------------------------------ 白名单

#: 违规判定的目录前缀（相对仓库根，或作为裸字面量出现）
_VIOLATE_PREFIXES = (
    "src/", "tools/", "world-quant-brain-mcp/",
    "docs/", "reports/",
    "Claude/skills/",
)
#: 允许的路径片段：字面量或变量值里出现即算命中
#: 注意：目录名不带尾部 "/"，因为 Python 的 `Path(...) / "tracking" / "x"` 语法里目录名不带斜杠
_ALLOW_SUBSTRINGS = (
    "output_report", "tracking", "cache", "logs", "results",
    "data", "attic",
    "tmp_path", "tempfile", "NamedTemporary", "mkdtemp", "gettempdir",
    "/tmp/", "WQB_ROOT", "WQB_TASK_ROOT", "WQB_HOME",
    "REPO_ROOT", "repo_root", "_REPO_ROOT", "find_repo_root",
    "repo_relative", "__file__", "Path(__file__)",
)
#: 写盘 attr
_WRITE_ATTRS = {"write_text", "write_bytes", "to_csv", "to_excel", "to_parquet",
                "to_json", "to_pickle", "to_frame", "savefig", "saveas"}
#: 写盘 module call
_WRITE_MODULE_CALLS = {"json.dump", "json.dumps", "json.dump", "pickle.dump",
                       "np.savetxt", "np.save"}


# ------------------------------------------------------------------ 解析

def _resolve_target_expr(node: ast.AST) -> Tuple[str, str]:
    """提取写盘调用的目标路径表达式：返回 (表达式源代码, 顶层变量名)。"""
    if not isinstance(node, ast.Call):
        return "", ""
    f = node.func
    if isinstance(f, ast.Attribute):
        attr = f.attr
        base = f.value
        if attr in _WRITE_ATTRS:
            # base 是变量；第一个位置参数是内容，不关心
            if isinstance(base, ast.Name):
                return "", base.id
        return "", ""
    if isinstance(f, ast.Name):
        if f.id == "open" and node.args:
            tgt = node.args[0]
            if isinstance(tgt, ast.Name):
                return "", tgt.id
            return (ast.get_source_segment(_src, tgt) or "")[:80], tgt.id if isinstance(tgt, ast.Name) else ""
        if f.id in ("dump", "dumps") and len(node.args) >= 2:
            tgt = node.args[1]
            if isinstance(tgt, ast.Name):
                return "", tgt.id
            return (ast.get_source_segment(_src, tgt) or "")[:80], tgt.id if isinstance(tgt, ast.Name) else ""
    if isinstance(f, ast.Attribute):
        pass  # 上面已处理
    return "", ""


def _build_assignment_map(tree: ast.AST) -> Dict[str, List[ast.AST]]:
    """变量名 → 它的所有赋值右侧 AST 节点。"""
    m: Dict[str, List[ast.AST]] = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    m.setdefault(t.id, []).append(n.value)
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
            if n.value is not None:
                m.setdefault(n.target.id, []).append(n.value)
    return m


def _expr_literals(expr: ast.AST, amap: Dict[str, List[ast.AST]], depth: int = 0,
                   seen: Optional[set] = None) -> str:
    """把一个表达式递归展开成字面量子串集合的字符串（用于白名单匹配）。"""
    seen = seen or set()
    if depth > 3:
        return ""
    parts: List[str] = []

    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        return expr.value
    if isinstance(expr, ast.Name):
        if expr.id in seen:
            return ""
        seen.add(expr.id)
        for rhs in amap.get(expr.id, []):
            parts.append(_expr_literals(rhs, amap, depth + 1, seen))
        return " ".join(parts)
    if isinstance(expr, ast.JoinedStr):
        # f-string：把 fstring 的 parts 都展开
        for v in expr.values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            elif isinstance(v, ast.FormattedValue):
                parts.append(_expr_literals(v.value, amap, depth + 1, seen))
        return " ".join(parts)
    if isinstance(expr, ast.BinOp):
        # a + b（路径拼接）
        return " ".join(_expr_literals(e, amap, depth + 1, seen) for e in (expr.left, expr.right))
    if isinstance(expr, ast.Call):
        # 函数调用：抓参数里的字面量 + 参数变量
        f = expr.func
        fname = ""
        if isinstance(f, ast.Name):
            fname = f.id
        elif isinstance(f, ast.Attribute):
            fname = f.attr
            if isinstance(f.value, ast.Name):
                fname = f.value.id + "." + fname
        parts.append(fname)
        for a in expr.args:
            parts.append(_expr_literals(a, amap, depth + 1, seen))
        # os.path.join("a", "b", "c") 会把 a/b/c 都拼进去
        return " ".join(parts)
    if isinstance(expr, ast.Attribute) and isinstance(expr.value, ast.Name):
        return expr.value.id + "." + expr.attr
    if isinstance(expr, (ast.List, ast.Tuple)):
        return " ".join(_expr_literals(e, amap, depth + 1, seen) for e in expr.elts)
    if isinstance(expr, ast.Subscript):
        return _expr_literals(expr.value, amap, depth + 1, seen)
    return ""


# ------------------------------------------------------------------ 分类

def classify_target(material: str) -> Tuple[str, str]:
    """
    返回 (kind, label)：
      kind ∈ {"ALLOWED", "VIOLATE", "UNKNOWN"}
      label = 白名单命中片段 / 违规片段 / "?"
    """
    if not material.strip():
        return "UNKNOWN", "?"
    # 违规优先（避免 docs/xxx 里恰好含 "tmp" 时被误放行）
    for pre in _VIOLATE_PREFIXES:
        # 违规前缀本身已含 "/", 匹配 "src/" "tools/" 等作为目录开头即可。
        # 不做 lookbehind 约束：`Path("docs/foo.md")` 与 `"docs/foo.md"` 都应算违规。
        if re.search(re.escape(pre), material):
            return "VIOLATE", pre.rstrip("/")
    # 允许
    for tok in _ALLOW_SUBSTRINGS:
        if tok in material:
            return "ALLOWED", tok
    # 裸文件名（无目录前缀，含 . 结尾扩展名）
    # 只有当整个 material 就是一个短字符串且含扩展名 → 判违规
    stripped = material.strip().strip("'\"")
    if re.match(r"^[\w.-]+\.(md|json|txt|csv|log|html|pkl|parquet|jsonl)$", stripped):
        return "VIOLATE", f"裸文件名 '{stripped[:40]}' 落 cwd"
    return "UNKNOWN", "?"


# ------------------------------------------------------------------ 扫描

# 模块级全局：ast 遍历时用于 get_source_segment
_src: Optional[str] = None


def scan_file(path: Path, root: Path) -> List[Dict]:
    """扫描单个 .py，返回违规候选列表。"""
    global _src
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    _src = text
    amap = _build_assignment_map(tree)
    out: List[Dict] = []
    rel = path.relative_to(root).as_posix()

    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        is_write = False
        material_src = ""
        var_hint = ""
        if isinstance(f, ast.Attribute):
            if f.attr in _WRITE_ATTRS:
                is_write = True
                if isinstance(f.value, ast.Name):
                    var_hint = f.value.id
        elif isinstance(f, ast.Name):
            if f.id == "open" and n.args:
                # 检查 mode 参数：无 mode = 默认 "r"，不判写
                mode = None
                if len(n.args) >= 2 and isinstance(n.args[1], ast.Constant):
                    mode = n.args[1].value
                else:
                    for kw in n.keywords:
                        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                            mode = kw.value.value
                if mode is None or not isinstance(mode, str) or mode[0] not in ("w", "a", "x", "+"):
                    is_write = False
                else:
                    tgt = n.args[0]
                    material_src = _expr_literals(tgt, amap)
            elif f.id in ("dump", "dumps") and len(n.args) >= 2:
                is_write = True
                material_src = _expr_literals(n.args[1], amap)
        elif isinstance(f, ast.Attribute):
            # np.savetxt, np.save, df.to_csv 已在 WRITE_ATTRS 覆盖
            pass

        if not is_write:
            continue

        # material = 所有能反映路径的字面量子串：目标表达式 + 接收方变量（`open(x, 'w')` 里
        # x 是路径；`f.write_text(x)` 里 f 是路径）+ 调用名（os.path.join / Path(...)）
        material_parts: List[str] = [material_src or "", var_hint or ""]
        if isinstance(f, ast.Attribute):
            if isinstance(f.value, ast.Name):
                material_parts.append(f.value.id)          # e.g. ROOT, dest_root, pack_dir
            material_parts.append(f.attr)                  # e.g. write_text
            # 若 base 本身是表达式（如 Path(x).write_text），把 base 也展开
            if not isinstance(f.value, ast.Name):
                material_parts.append(_expr_literals(f.value, amap))
        elif isinstance(f, ast.Name):
            material_parts.append(f.id)                    # open / dump / dumps
        material = " ".join(p for p in material_parts if p)

        kind, label = classify_target(material)
        if kind == "ALLOWED":
            continue
        out.append({
            "file": rel,
            "line": n.lineno,
            "kind": kind,
            "label": label,
            "hint": material.strip()[:120],
        })
    return out


def scan(root: Path, dirs=None, skip_parts=None) -> List[Dict]:
    dirs = dirs or CODE_DIRS
    skip_parts = skip_parts or CODE_SKIP_PARTS
    out: List[Dict] = []
    for base in dirs:
        d = root / base
        if not d.exists():
            continue
        for f in d.rglob("*.py"):
            rel = f.as_posix().replace(str(root) + "/", "")
            if any(s in "/" + rel for s in skip_parts):
                continue
            if f.name.startswith("test_") and "/tests/" in "/" + rel:
                continue
            out.extend(scan_file(f, root))
    return out


# ------------------------------------------------------------------ 棘轮

def _fingerprint(item: Dict) -> str:
    """路径::kind::label（不含行号，不随无关改动漂移）"""
    return f"{item['file']}::{item['kind']}::{item['label']}"


def load_baseline() -> set:
    if not BASELINE.exists():
        return set()
    try:
        data = json.loads(BASELINE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return set(data.get("violations", []))


def save_baseline(violations: set) -> None:
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(
        json.dumps({"violations": sorted(violations)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ------------------------------------------------------------------ CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="写盘目标 §8.13 白名单审计（棘轮）")
    ap.add_argument("--all", action="store_true", help="连 UNKNOWN / ALLOWED 也列出")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--update-baseline", action="store_true", help="把当前违规全量写入基线")
    ap.add_argument("--path", help="限定扫描目录（相对仓库根）")
    args = ap.parse_args(argv)

    root = REPO
    if args.path:
        items = scan(root, dirs=(args.path,))
    else:
        items = scan(root)

    violations = [i for i in items if i["kind"] == "VIOLATE"]
    unknowns = [i for i in items if i["kind"] == "UNKNOWN"]

    if args.update_baseline:
        save_baseline({_fingerprint(v) for v in violations})
        print(f"[update-baseline] 已登记 {len(violations)} 条违规到 {BASELINE.relative_to(root)}")
        return 0

    baseline = load_baseline()
    new_viols = [v for v in violations if _fingerprint(v) not in baseline]

    if args.json:
        print(json.dumps({
            "violations": violations,
            "unknowns": unknowns if args.all else [],
            "new_violations": new_viols,
            "baseline_size": len(baseline),
        }, ensure_ascii=False, indent=2))
    else:
        print(f"扫描完成：违规 {len(violations)} 条 | UNKNOWN {len(unknowns)} 条 | 新增违规 {len(new_viols)} 条")
        if new_viols:
            print(f"\n【新增违规】（基线外，阻断提交）：")
            for v in new_viols[:40]:
                print(f"  ❌ {v['file']}:{v['line']}  ← {v['label']}")
                print(f"     解析出：{v['hint'][:100]}")
            if len(new_viols) > 40:
                print(f"  ... 及另 {len(new_viols) - 40} 条")
        if args.all and violations:
            print(f"\n【全部违规】（含基线内）：")
            for v in violations:
                tag = "🔴新增" if v in new_viols else "🟡基线内"
                print(f"  {tag} {v['file']}:{v['line']}  ← {v['label']}")
        if args.all and unknowns:
            print(f"\n【UNKNOWN】（解析不出路径，需人工看）：")
            for u in unknowns[:20]:
                print(f"  ⚪ {u['file']}:{u['line']}  ← {u['hint'][:80]}")

    return 1 if new_viols else 0


if __name__ == "__main__":
    sys.exit(main())
