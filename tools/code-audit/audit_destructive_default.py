#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""audit_destructive_default — 找「默认即破坏」的脚本（2026-10-06 新增，P3 后续）。

为什么要有这个工具
------------------
2026-10-06 实测：`tools/code-audit/db_mcp_split.py` 在**模块顶层**直接
`Path.write_text(...)`，而唯一的开关是中途一句 `if "--plan" in sys.argv: sys.exit(0)`。
后果：跑一次 `--help`（甚至打错一个 flag）就把**被跟踪的**根门面 `wqb_db_mcp.py`
从 2808 行截成 91 行，并生成 7 个未跟踪模块。

这类写法的要害不是"没有开关"，而是**开关不在前面**：任何一次误调用都会真的落盘。
本仓的既有红线是「默认只读/dry-run，删除或写盘必须显式 `--apply`」，
但**没有任何机械检查在守护它** —— 本工具补上这条。

判定规则（AST，只看模块级）
---------------------------
在模块级（`def`/`class` 之外）按**语句顺序**走：
  · 遇到「提前退出型开关」= `if <test 提到 apply/dry/plan/force/confirm/yes>` 且 body 含
    `sys.exit()` / `return` / `raise SystemExit` → 记录已设闸，之后不再报
  · 遇到「破坏性调用」而**尚未**设闸 → 报 DRY-RUN-MISSING（高危：任何调用都真落盘）
  · `if __name__ == "__main__":` 块内的破坏性调用单独归类 ADVISORY
    （只在直跑时发生；常见且安全的 argparse `--apply` 形态就在这一档，故不判失败）

**把破坏性动作整个收进 `def main()` 并加 `if __name__ == "__main__"` 守卫** = 已认可的解法：
本工具**不进 `def`/`class` 体**（那里不会在 import 时执行），故不再报——`Python` 直跑才发生。

破坏性调用 = `Path.write_text/write_bytes/unlink/rmdir/touch/mkdir`、`os.remove/rmdir/rename/replace/
truncate`、`shutil.rmtree/move/copytree`、`open(..., 'w'|'a'|'x')`、`json.dump`、`DataFrame.to_csv/
to_parquet/to_excel`、`subprocess.*` 里的 `rm -rf` / `del /s`。

棘轮（ratchet）
---------------
与 `doc_path_refs.py` 同一套语义：**只拦新增，不追存量**。基线存
`tests/fixtures/destructive_default_baseline.json` 的 `hard` 键（`file::kind::detail`，
**不含行号**——行号会随无关改动漂移）。**只有不在基线上的 DRY-RUN-MISSING 才阻断。**

· `PARSE-FAIL`（文件语法错、本工具读不懂）**只告警不阻断**：那多半是编辑中间态，
  拿它卡提交只会训练出 `--no-verify` 的习惯（本仓治理笔记已明写此教训）。
· 基线为空 = 当前全仓零高危，此后任何一条新增都会被拦住。

用法
----
    python tools/code-audit/audit_destructive_default.py                  # 棘轮：只报新增高危
    python tools/code-audit/audit_destructive_default.py --all            # 连 ADVISORY / PARSE-FAIL 一起列
    python tools/code-audit/audit_destructive_default.py --json
    python tools/code-audit/audit_destructive_default.py --path tools
    python tools/code-audit/audit_destructive_default.py --update-baseline  # 复核后登记存量
退出码：0 = 无新增高危 / 1 = 有新增高危 / 2 = 工具故障
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，与文件层数无关（AGENTS.md §8）。"""
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()

from wqb.paths import find_repo_root  # noqa: E402

REPO = find_repo_root(__file__)

BASELINE = REPO / "tests" / "fixtures" / "destructive_default_baseline.json"

DEFAULT_DIRS = ("tools", "src/wqb")
SKIP_PARTS = ("__pycache__", "/attic/", "/legacy/", "/vendor/")

#: 破坏性方法名（按 attr 匹配，不看对象类型 —— 宁可多报，人工复核）
DESTRUCTIVE_ATTRS = {
    "write_text", "write_bytes", "unlink", "rmdir", "touch", "truncate",
    "remove", "removedirs", "rmtree", "move", "copytree", "replace", "rename",
    "to_csv", "to_parquet", "to_excel", "to_json", "dump", "dump_all", "chmod",
}
#: 这些 attr 太常见、歧义大（`df.replace`、`str.replace`、`shutil.move` 都叫 replace）,
#: 只报「对象名像路径/文件」的调用
AMBIGUOUS_ATTRS = {"remove", "replace", "rename", "move", "dump", "chmod", "touch", "truncate"}
AMBIGUOUS_OK_OBJS = {"os", "shutil", "json", "pickle", "df", "frame", "self", "conn", "cur"}

WRITE_MODES = {"w", "a", "x", "wb", "ab", "xb", "w+", "a+"}

#: 「提前退出型开关」的 test 里出现的词（小写子串匹配）
GATE_WORDS = ("apply", "dry", "plan", "force", "confirm", "yes", "__main__")


def _is_exit_call(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
    return name in ("exit", "quit") or name == "SystemExit"


def _body_exits(body: list[ast.stmt]) -> bool:
    for st in body:
        for n in ast.walk(st):
            if _is_exit_call(n) or isinstance(n, (ast.Return, ast.Raise)):
                return True
    return False


def _is_gate(node: ast.stmt) -> bool:
    """`if <提到 apply/dry/plan/…> : … exit` —— 提前退出型开关。"""
    if not isinstance(node, ast.If):
        return False
    src = ast.unparse(node.test).lower()
    if not any(w in src for w in GATE_WORDS):
        return False
    return _body_exits(node.body)


def _destructive_call(node: ast.AST) -> str | None:
    """返回破坏性调用的可读描述，否则 None。"""
    if isinstance(node, ast.Call):
        f = node.func
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
        # open(path, "w")
        if name == "open" and len(node.args) >= 2:
            mode = node.args[1]
            if isinstance(mode, ast.Constant) and isinstance(mode.value, str) and mode.value in WRITE_MODES:
                return f"open(..., {mode.value!r})"
        if name in DESTRUCTIVE_ATTRS and isinstance(f, ast.Attribute):
            obj = f.value
            if name in AMBIGUOUS_ATTRS:
                base = obj.id if isinstance(obj, ast.Name) else (
                    obj.attr if isinstance(obj, ast.Attribute) else ""
                )
                if base and base not in AMBIGUOUS_OK_OBJS:
                    return None
                if not base:
                    return None
            return f".{name}()"
    # subprocess 里的 rm -rf / del /s
    if isinstance(node, ast.List) and node.elts:
        txt = " ".join(e.value for e in node.elts if isinstance(e, ast.Constant) and isinstance(e.value, str))
        low = txt.lower()
        if ("rm" in low and "-rf" in low) or ("del" in low and "/s" in low):
            return f"subprocess {txt[:40]}"
    return None


CONTROL_FLOW = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)


def _own_exprs(st: ast.stmt) -> list[ast.AST]:
    """只取**该语句自身**的表达式节点，不进入它的子语句。

    子语句会作为独立条目出现在扁平表里；若这里再 `ast.walk` 一遍就会重复计数，
    更糟的是会钻进 `def` 体（那正是"函数内的写盘"被误报的原因）。
    """
    if isinstance(st, (ast.If, ast.While)):
        return [st.test]
    if isinstance(st, (ast.For, ast.AsyncFor)):
        return [st.iter]
    if isinstance(st, (ast.With, ast.AsyncWith)):
        return [i.context_expr for i in st.items]
    if isinstance(st, ast.Try):
        return []
    return list(ast.walk(st))


def _flatten_module_stmts(stmts, in_main=False):
    """把模块级语句压成有序扁平表；**不进入 def / class**。

    产出 [(stmt, in_main)]，顺序即执行顺序（模块级 `if`/`for`/`try` 的 body 确实会执行）。
    """
    out = []
    for st in stmts:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        is_main = in_main
        if isinstance(st, ast.If) and "__main__" in ast.unparse(st.test):
            is_main = True
        out.append((st, is_main))
        for attr in ("body", "orelse", "finalbody"):
            sub = getattr(st, attr, None)
            if isinstance(sub, list) and sub:
                out.extend(_flatten_module_stmts(sub, is_main))
    return out


def _walk_module_level(stmts, in_main=False):
    """产出 (行号, 描述, 是否在 __main__ 块内, 是否已在提前退出开关之后)。"""
    gated = False
    for st, is_main in _flatten_module_stmts(stmts, in_main):
        if isinstance(st, ast.If) and _is_gate(st):
            gated = True
            continue
        for n in _own_exprs(st):
            d = _destructive_call(n)
            if d:
                yield getattr(n, "lineno", 0) or getattr(st, "lineno", 0), d, is_main, gated


def scan_file(p: Path) -> list[dict]:
    try:
        tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, OSError) as e:
        return [{"file": str(p.relative_to(REPO)), "line": 0, "kind": "PARSE-FAIL", "detail": str(e)[:80]}]
    out = []
    for line, desc, in_main, gated in _walk_module_level(tree.body):
        if in_main:
            out.append({"file": str(p.relative_to(REPO)), "line": line, "kind": "ADVISORY",
                        "detail": f"__main__ 块内破坏性调用 {desc}"})
        elif not gated:
            out.append({"file": str(p.relative_to(REPO)), "line": line, "kind": "DRY-RUN-MISSING",
                        "detail": f"模块级破坏性调用 {desc}，且此前无提前退出型开关"})
    return out


def iter_files(dirs: list[str]) -> list[Path]:
    files = []
    for d in dirs:
        base = REPO / d
        if not base.exists():
            continue
        for p in base.rglob("*.py"):
            rp = p.as_posix()
            if any(s in rp for s in SKIP_PARTS):
                continue
            files.append(p)
    return sorted(set(files))


def _key(f: dict) -> str:
    """基线键：**不含行号**（行号随无关改动漂移，会让棘轮误判为"新增"）。"""
    return f"{f['file']}::{f['kind']}::{f['detail']}"


def _load_baseline() -> set[str]:
    if not BASELINE.exists():
        return set()
    try:
        d = json.loads(BASELINE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    return set(d.get("hard", []))


def main() -> int:
    ap = argparse.ArgumentParser(description="找「默认即破坏」的脚本（模块级破坏性调用 + 无提前退出开关）")
    ap.add_argument("--path", action="append", help=f"只扫这些目录（默认 {list(DEFAULT_DIRS)}）")
    ap.add_argument("--all", action="store_true", help="连 ADVISORY / PARSE-FAIL 一起列")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--update-baseline", action="store_true",
                    help="把当前全部 DRY-RUN-MISSING 写进基线（复核过、确认是存量债才用）")
    a = ap.parse_args()

    files = iter_files(a.path or list(DEFAULT_DIRS))
    if not files:
        print("[destructive-default] 没扫到文件（路径给错了？）", file=sys.stderr)
        return 2
    findings: list[dict] = []
    for p in files:
        findings.extend(scan_file(p))

    hard = [f for f in findings if f["kind"] == "DRY-RUN-MISSING"]
    parse_fail = [f for f in findings if f["kind"] == "PARSE-FAIL"]
    adv = [f for f in findings if f["kind"] == "ADVISORY"]

    if a.update_baseline:
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps({
            "_doc": "audit_destructive_default.py 的棘轮基线（2026-10-06）。列出的条目是"
                    "『模块级破坏性调用且前置开关在后面』的**存量**违规：不阻断提交，但不得新增。"
                    "键 = file::kind::detail（不含行号，行号漂移不该算新增）。"
                    "修好一条请重跑 --update-baseline 收紧；只在确认合理时才手工放宽。",
            "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "_scanned": len(files),
            "hard": sorted({_key(f) for f in hard}),
        }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"[destructive-default] 基线已更新：{BASELINE.relative_to(REPO)}（存量 {len(hard)} 条）")
        return 0

    base = _load_baseline()
    new_hard = [f for f in hard if _key(f) not in base]
    carried = len(hard) - len(new_hard)

    if a.json:
        print(json.dumps({"scanned": len(files), "new_hard": new_hard,
                          "baseline_carried": carried, "parse_fail": parse_fail,
                          "advisory": adv}, ensure_ascii=False, indent=1))
        return 1 if new_hard else 0

    print(f"[destructive-default] 扫 {len(files)} 个 .py（基线 {len(base)} 条）")
    if new_hard:
        print(f"\n❌ 新增高危：模块级破坏性调用且**开关在后面**"
              f"（任何误调用都会真落盘）——{len(new_hard)} 条")
        for f in new_hard:
            print(f"  {f['file']}:{f['line']}  {f['detail']}")
        print("\n  修法二选一：")
        print('  ① 破坏性调用**之前**放默认干跑闸：')
        print('       APPLY = "--apply" in sys.argv')
        print("       if not APPLY:\n           print('[DRY-RUN] 未写盘; 落盘请加 --apply'); sys.exit(0)")
        print("  ② 把破坏性动作整个收进 `def main()` 并加 `if __name__ == \"__main__\":` 守卫")
        print("     （本工具不进函数体，import 时也就不会有副作用）")
    else:
        print("\n✅ 无新增高危" + (f"（基线内存量 {carried} 条）" if carried else "") + "。")
    if parse_fail:
        print(f"\n⚠ PARSE-FAIL {len(parse_fail)} 条（**不阻断**：编辑中间态居多）")
        for f in parse_fail[:20]:
            print(f"  {f['file']}:{f['line']}  {f['detail']}")
    if a.all and adv:
        print(f"\n— ADVISORY（__main__ 块内，仅在直跑时发生）—{len(adv)} 条")
        for f in adv[:60]:
            print(f"  {f['file']}:{f['line']}  {f['detail']}")
    return 1 if new_hard else 0


if __name__ == "__main__":
    sys.exit(main())
