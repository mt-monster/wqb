# -*- coding: utf-8 -*-
"""ledger_keys.py — 台账（ledger_kv）键目录：扫描器 + 目录读取 + 文档表生成（库 + CLI）。

背景（skills 审查 X-1 / IX-20 / TR-17 / RA-129，2026-09-29）：全库实际使用的 ledger 键远多于任何一份文档登记的，
且出现过「有读取方无写入方」（`saturated_datasets`）、「有写入方无读取方」、「文档教的键已被代码废止」
（`wave<N>_verdict`）。没有一处能回答「这个键谁写、谁读、缺了怎么办、谁负责刷新」。

单一真相源：`docs/ledger_keys.json`（人写：用途 / 写入方 / 读取方 / 缺失行为 / 刷新责任 / 状态）。
本工具从**代码与文档**里机械抽取实际出现的键，tests/unit/01_store_db/test_ledger_key_catalog.py 用它守：
  ① 代码里出现的键必须在目录里；② 被读取的键必须有写入方（已知缺口须显式登记 orphan 并指向审查条目，
  且登记必须仍然为真——缺口被补上后必须删掉登记）；③ 目录里登记的代码引用真实存在；
  ④ 文档里教的键必须在目录里，已废止的键只能出现在带「废止 / 历史」字样的行。

检测范围（静态，宁缺毋滥）：
  * Python AST：get_ledger / upsert_ledger / get_ledger_key / upsert_ledger_key / _get_ledger_raw /
    _upsert_ledger_raw 的 key 实参（字面量、f-string、`%` 格式化、`+` 拼接；`{x}` / `%s` → `<x>`）；
  * 含 ``ledger_kv`` 的 SQL 字面量：`key='…'`、`key LIKE '…'`、`VALUES (?, '…', …)`（INSERT/UPDATE/REPLACE/DELETE 记写）；
  * 文档：`get/upsert_ledger_key(region, "key")`、含 ledger 的行里的 `key='…'`、``ledger `key` ``。
  变量键（`key=pool_key` 这类）无法静态还原，列在 `dynamic` 里供人核对目录是否覆盖。

用法：
  python tools/ledger_keys.py                 # 扫描 + 与目录对账，打印差异
  python tools/ledger_keys.py --print-table   # 输出可嵌入文档的 Markdown 表
  python tools/ledger_keys.py --json          # 机器可读扫描结果
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "docs" / "ledger_keys.json"
SK = REPO / "Claude" / "skills"

READ_FUNCS = {"get_ledger", "get_ledger_key", "_get_ledger_raw"}
WRITE_FUNCS = {"upsert_ledger", "upsert_ledger_key", "_upsert_ledger_raw", "set_key"}
#: key 实参不在第 2 位的接口：LedgerStore.set_key(key, val)
KEY_ARG_INDEX = {"set_key": 0}

CODE_ROOTS = ("src", "tools", "world-quant-brain-mcp", "wqb_db_mcp.py", "Claude/skills")
CODE_SKIP = (".venv", "/tests/", "/tests.py", "forum_corpus", "trailSomeAlphas", "__pycache__",
             "site-packages", "/vendor/", "tools/ledger_keys.py",
             "tools/_kor_")          # 一次性临时脚本（下划线前缀惯例，见 AGENTS.md）
DOC_SKIP = ("brain-alpha-judge/data/forum_corpus/", "brain-make-some-gem/scripts/trailSomeAlphas/skills/")

_PH = re.compile(r"\{([^{}]*)\}|%s|%d")
_DEPRECATED_MARK = re.compile(r"废止|已废|历史|deprecated|不再|旧键|legacy", re.I)


# ----------------------------------------------------------------------------- 归一 / 匹配
def _ph_name(raw: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_]+", "_", raw.split("(")[0].split("[")[0].split(".")[-1]).strip("_")
    return name[:12] or "x"


def norm_key(raw: str) -> str:
    """`{dataset}` / `%s` / `<ds>` / `<W-1>` → 统一 `<x>` 占位；`%`（SQL LIKE 通配）→ `<any>`。"""
    s = _PH.sub(lambda m: "<%s>" % (_ph_name(m.group(1)) if m.group(1) is not None else "x"), raw)
    s = re.sub(r"<[^<>]*>", "<x>", s)
    s = s.replace("%", "<x>").replace("*", "<x>")
    return re.sub(r"(<x>)+", "<x>", s)


def key_regex(pattern: str) -> "re.Pattern[str]":
    """目录里的键模式（`s1_<ds>_d<delay>`）→ 正则；`<x>` 匹配任意非空串。"""
    parts = re.split(r"<[^<>]*>", pattern)
    return re.compile("^" + ".+".join(re.escape(p) for p in parts) + "$")


def is_generic(catalog_key: str) -> bool:
    """键里没有任何字面量（如 `<prefix>_<alpha_id>`）——这种条目只说明形态，不能当通配去「覆盖」别的键。"""
    return not re.sub(r"<[^<>]*>|[_:]", "", catalog_key)


def matches(catalog_key: str, detected: str) -> bool:
    """检测到的键（已 norm）是否被目录条目覆盖：目录里的占位符匹配任意非空串。

    泛型条目（无字面量）只覆盖与自己归一后完全相同的检测键，否则一个 `<x>_<x>` 就能让覆盖检查形同虚设。
    """
    d = norm_key(detected)
    if is_generic(catalog_key):
        return norm_key(catalog_key) == d
    return key_regex(catalog_key).match(d.replace("<x>", "x")) is not None


def head(catalog_key: str) -> str:
    """键的字面量前缀（第一个占位符之前）；用来在引用文件里验证「这个键确实出现」。"""
    return re.split(r"<", catalog_key, maxsplit=1)[0]


# ----------------------------------------------------------------------------- 代码扫描
def _render(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        out = ""
        for v in node.values:
            if isinstance(v, ast.Constant):
                out += str(v.value)
            elif isinstance(v, ast.FormattedValue):
                out += "{%s}" % _ph_name(ast.unparse(v.value))
        return out
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):       # "xr_probe_%s" % tag
        return _render(node.left)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):       # "prefix_" + name
        left, right = _render(node.left), _render(node.right)
        if left is not None and right is not None:
            return left + right
        if left is not None:
            return left + "{x}"
        return None
    return None


def _iter_py() -> Iterable[Path]:
    for r in CODE_ROOTS:
        p = REPO / r
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*.py")):
                s = f.as_posix()
                if any(k in s for k in CODE_SKIP):
                    continue
                yield f


def scan_code() -> Dict[str, Any]:
    """→ {"keys": {norm_key: {"read": [files], "write": [files]}}, "dynamic": [(file, line, callee, "R"|"W")]}"""
    keys: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: {"read": set(), "write": set()})
    dynamic: List[Tuple[str, int, str, str]] = []
    for p in _iter_py():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        rel = p.relative_to(REPO).as_posix()
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                f = n.func
                name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
                if name in READ_FUNCS or name in WRITE_FUNCS:
                    kw = {k.arg: k.value for k in n.keywords}
                    idx = KEY_ARG_INDEX.get(name, 1)
                    node = kw.get("key") or (n.args[idx] if len(n.args) > idx else None)
                    if node is None:
                        continue
                    raw = _render(node)
                    side = "read" if name in READ_FUNCS else "write"
                    if raw is None or not raw.strip("{x}<>"):
                        dynamic.append((rel, getattr(n, "lineno", 0), name, "R" if side == "read" else "W"))
                    else:
                        keys[norm_key(raw)][side].add(rel)
            elif isinstance(n, ast.Constant) and isinstance(n.value, str) and "ledger_kv" in n.value:
                sql = n.value
                is_write = bool(re.search(r"\b(INSERT|UPDATE|REPLACE|DELETE)\b", sql, re.I))
                side = "write" if is_write else "read"
                for m in re.finditer(r"key\s*=\s*'([^']+)'", sql):
                    keys[norm_key(m.group(1))][side].add(rel)
                for m in re.finditer(r"key\s+LIKE\s+'([^']+)'", sql, re.I):
                    keys[norm_key(m.group(1))]["read"].add(rel)
                # VALUES (?, 'key', …) 与 VALUES ('REGION', 'key', …) 两种：第一个值是 region（占位或字面量），第二个才是键
                for m in re.finditer(r"VALUES\s*\(\s*(?:\?|'[^']*')\s*,\s*'([^'?]+)'", sql, re.I):
                    keys[norm_key(m.group(1))]["write"].add(rel)
    return {"keys": {k: {s: sorted(v) for s, v in d.items()} for k, d in keys.items()},
            "dynamic": sorted(set(dynamic))}


# ----------------------------------------------------------------------------- 文档扫描
_DOC_CALL = re.compile(
    r"(?:get|upsert)_ledger_key\(\s*(?:region\s*=\s*)?[^,()\n]*,\s*(?:key\s*=\s*)?['\"]([A-Za-z0-9_<>{}%*.\-]+)['\"]")
_DOC_KEYEQ = re.compile(r"key\s*=\s*['\"]([A-Za-z0-9_<>{}%*.\-]+)['\"]")
_DOC_LEDGER_TICK = re.compile(r"ledger[ _]?(?:key)?\s*[`'\"]([a-z][A-Za-z0-9_<>{}*.\-]*)[`'\"]")


def _doc_files() -> List[Path]:
    files = [REPO / "AGENTS.md", REPO / "CLAUDE.md", REPO / "README.md", SK / "INDEX.md"]
    for p in sorted(SK.rglob("*.md")):
        rel = p.relative_to(SK).as_posix()
        if not any(rel.startswith(x) for x in DOC_SKIP):
            files.append(p)
    return [f for f in dict.fromkeys(files) if f.is_file()]


def scan_docs() -> Dict[str, List[Tuple[str, int, str]]]:
    """→ {norm_key: [(file, line, line_text)]}（只收看起来像键的 token：小写、含下划线或占位符）。"""
    out: Dict[str, List[Tuple[str, int, str]]] = defaultdict(list)
    for f in _doc_files():
        rel = f.relative_to(REPO).as_posix()
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            toks: List[str] = []
            toks += _DOC_CALL.findall(line)
            if "ledger" in line.lower():
                toks += _DOC_KEYEQ.findall(line)
            toks += _DOC_LEDGER_TICK.findall(line)
            for t in toks:
                if not re.search(r"[_<>]", t) or t.isupper():
                    continue
                out[norm_key(t)].append((rel, i, line.strip()))
    return dict(out)


# ----------------------------------------------------------------------------- 目录
def load_catalog() -> List[Dict[str, Any]]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))["entries"]


def covering(entries: List[Dict[str, Any]], detected: str) -> List[Dict[str, Any]]:
    return [e for e in entries if matches(e["key"], detected)]


def reconcile() -> Dict[str, Any]:
    """扫描 ↔ 目录对账，返回各类差异（供 CLI 打印与测试断言）。"""
    entries = load_catalog()
    code = scan_code()
    docs = scan_docs()
    uncovered_code = sorted(k for k in code["keys"] if not covering(entries, k))
    uncovered_docs = sorted(k for k in docs if not covering(entries, k))
    reads_no_writer = []
    for e in entries:
        if e.get("status") == "deprecated":
            continue
        has_reader = bool(e.get("readers"))
        if has_reader and not e.get("writers") and not e.get("orphan"):
            reads_no_writer.append(e["key"])
    return {"uncovered_code": uncovered_code, "uncovered_docs": uncovered_docs,
            "reads_no_writer": reads_no_writer, "dynamic": code["dynamic"]}


# ----------------------------------------------------------------------------- 文档表
def render_table(entries: Optional[List[Dict[str, Any]]] = None) -> str:
    entries = entries if entries is not None else load_catalog()
    rows = ["| 键（`<x>` = 占位） | 用途 | 写入方 | 读取方 | 缺失时 | 刷新 / 状态 |", "|---|---|---|---|---|---|"]

    def refs(items: List[Any]) -> str:
        out = []
        for it in items or []:
            if isinstance(it, str):
                out.append(f"`{it}`")
            else:
                out.append(f"{it.get('kind', '?')}: `{it.get('ref', '')}`")
        return "<br>".join(out) or "—"

    for e in sorted(entries, key=lambda x: x["key"]):
        status = e.get("status", "active")
        tail = e.get("refresh", "")
        if status != "active":
            tail = f"**{status}**；{tail}".rstrip("；")
        if e.get("orphan"):
            tail += f"<br>⚠ {e['orphan']['kind']}（{e['orphan'].get('tracked_by', '')}）"
        rows.append("| `{k}` | {p} | {w} | {r} | {m} | {t} |".format(
            k=e["key"], p=e.get("purpose", ""), w=refs(e.get("writers")), r=refs(e.get("readers")),
            m=e.get("missing", ""), t=tail or "—"))
    return "\n".join(rows)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="ledger 键目录：扫描 / 对账 / 生成文档表")
    ap.add_argument("--print-table", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.print_table:
        print(render_table())
        return 0
    if a.json:
        print(json.dumps({"code": scan_code(), "docs": {k: v[:1] for k, v in scan_docs().items()}},
                         ensure_ascii=False, indent=1))
        return 0
    r = reconcile()
    for title, k in (("代码里出现但目录没有", "uncovered_code"), ("文档里教但目录没有", "uncovered_docs"),
                     ("目录里有读取方却没有写入方（也没登记 orphan）", "reads_no_writer")):
        print(f"[{title}] {len(r[k])}")
        for x in r[k]:
            print("   ", x)
    print(f"[变量键，需人工核对目录是否覆盖] {len(r['dynamic'])}")
    for f, ln, fn, side in r["dynamic"]:
        print(f"    {f}:{ln} {fn} ({side})")
    return 1 if (r["uncovered_code"] or r["uncovered_docs"] or r["reads_no_writer"]) else 0


if __name__ == "__main__":
    sys.exit(main())
