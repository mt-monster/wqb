# -*- coding: utf-8 -*-
"""skill_lint.py — skill 文档「内容为真」的机械检查（库 + CLI）。

背景（skills 审查 X-17，2026-09-29）：仓库原有守护只查形式（frontmatter、边界段存在、工具计数、链接可达），
不查文档里的命令 / 参数 / 表达式是否为真。本工具补上其中最高频的几类，并与 tests/unit/test_skill_lint.py
配合成**棘轮**：现存违规登记在 tests/fixtures/skill_lint_baseline.json，新增违规必红，已修复的必须从基线移除。

检查项（check id）：
  cmd-subcommand / cmd-flag / cmd-required / cmd-script
        文档里 fenced 命令 → 目标脚本的 argparse（AST 提取，含子命令）：子命令是否存在、flag 是否存在、
        必填 flag 是否缺失。此前机检只核「flag 名是否在同目录任一脚本出现」，BM-14 的 4 条错误命令一条没抓到。
  mcp-tool / mcp-param
        `mcp__<server>__<tool>(k=v, …)`：工具是否注册、参数名是否在签名内（SB-06：示例带不存在的形参）。
  expr-gate
        fenced / 行内表达式过闸（gate.check_one 的 POISON / GHOST / INACCESSIBLE / SYNTAX / ARITY）。
        反例语境（反例/禁止/违规/❌/counterexample…）豁免。
  env-read / cli-password
        文档指示读取 `.env`、命令行传口令（AGENTS：凭据只在 .env，禁止读取、打印、提交）。
  bare-python
        fenced 命令用裸 `python`（跨平台不可解析）。目标脚本已接 tools/_pyenv（自动切 venv）者豁免。

用法：
  python tools/skill_lint.py                 # 全部检查，打印违规（含基线状态）
  python tools/skill_lint.py --check cmd     # 只跑某类（前缀匹配）
  python tools/skill_lint.py --json          # 机器可读
  python tools/skill_lint.py --update-baseline   # 把当前违规写入基线（只在“有意接受”时用，需人审 diff）
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import shlex
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

REPO = Path(__file__).resolve().parents[1]
SK = REPO / "Claude" / "skills"
BASELINE = REPO / "tests" / "fixtures" / "skill_lint_baseline.json"

CORPUS = ("brain-alpha-judge/data/forum_corpus/",)
NESTED = ("brain-make-some-gem/scripts/trailSomeAlphas/skills/",)

#: 文档里常用的路径别名变量 → 仓库路径（用于解析脚本）
ALIASES = {
    "$TK": "Claude/skills/wq-brain-campaign-toolkit/scripts",
    "$TOOLKIT": "Claude/skills/wq-brain-campaign-toolkit/scripts",
    "$WQ_TOOLKIT_DIR": "Claude/skills/wq-brain-campaign-toolkit/scripts",
    "$env:WQ_TOOLKIT_DIR": "Claude/skills/wq-brain-campaign-toolkit/scripts",
}
COUNTER_MARK = re.compile(r"反例|禁止|违规|错误示范|错误写法|不要|勿|不得|❌|✗|counter-?example|历史范式|已废止|已作废|被拦|拦截|会被|不合规|不可用",
                          re.I)
#: 命令块的「反例语境」只认强标记（紧邻前 2 行）：普通的「不要/勿」常出现在命令块附近的规则句里，不代表该块是反例
STRONG_COUNTER = re.compile(r"反例|错误示范|错误写法|不要这样|禁止这样|勿这样|❌|✗|counter-?example|历史范式|已废止的写法", re.I)
PLACEHOLDER = re.compile(r"^(<[^>]*>|\{[^}]*\}|\$[A-Za-z_(][\w()]*|%[^%]+%|\.\.\.|…)$")


# ----------------------------------------------------------------------------- 文档遍历
def iter_docs() -> Iterable[Path]:
    for p in sorted(SK.rglob("*.md")):
        r = p.relative_to(REPO).as_posix()
        if any(c in r for c in CORPUS) or any(n in r for n in NESTED):
            continue
        yield p


def rel(p: Path) -> str:
    return p.relative_to(REPO).as_posix()


def fenced_blocks(text: str) -> List[Tuple[int, int, str, List[str]]]:
    """[(start_line, end_line, lang, lines)]（行号 1 起；不含围栏行本身）。"""
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        m = re.match(r"^\s*(```|~~~)\s*([\w+-]*)", lines[i])
        if m:
            fence, lang, j = m.group(1), m.group(2), i + 1
            body = []
            while j < len(lines) and not lines[j].lstrip().startswith(fence):
                body.append(lines[j])
                j += 1
            out.append((i + 2, j, lang.lower(), body))
            i = j + 1
        else:
            i += 1
    return out


EXEMPT_MARK = "lint:counterexample"      # 显式豁免标记：`<!-- lint:counterexample -->` 写在块前一行，或行内同行


def context_is_counterexample(lines: List[str], start_line: int, look_back: int = 4, strong: bool = False) -> bool:
    lo = max(0, start_line - 1 - look_back)
    ctx = lines[lo:start_line]
    if any(EXEMPT_MARK in ln for ln in ctx):
        return True
    pat = STRONG_COUNTER if strong else COUNTER_MARK
    return any(pat.search(ln) for ln in ctx)


# ----------------------------------------------------------------------------- argparse AST 提取
class Spec:
    def __init__(self) -> None:
        self.top: Dict[str, dict] = {}
        self.subs: Dict[str, Dict[str, dict]] = {}
        self.all_flags: Set[str] = set()
        self.dynamic = False          # 有无法静态解析的 add_argument（helper 传参 / parents 复杂）→ 只做「flag 名出现过」级检查
        self.multi = False            # 脚本里构造了多个 ArgumentParser（预解析器 + 主解析器等）→ 不做必填检查

    def flags_for(self, sub: Optional[str]) -> Dict[str, dict]:
        d = dict(self.top)
        if sub and sub in self.subs:
            d.update(self.subs[sub])
        return d


def _const(node) -> Optional[object]:
    return node.value if isinstance(node, ast.Constant) else None


def _kw(call: ast.Call, name: str):
    for k in call.keywords:
        if k.arg == name:
            return k.value
    return None


@lru_cache(maxsize=None)
def parse_argparse(path: str) -> Optional[Spec]:
    try:
        tree = ast.parse(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, OSError):
        return None
    spec = Spec()
    kind: Dict[str, Tuple[str, Optional[str]]] = {}      # var -> ("top"|"subs"|"sub", name)
    parents: Dict[str, List[str]] = {}
    parser_like = False
    n_parsers = 0
    HELPERS = {"add_campaign_arg": ("--campaign-dir", False)}     # 已知会往 parser 上加 flag 的 helper

    def visit(node):
        nonlocal parser_like, n_parsers
        for n in ast.walk(node):
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) \
                    and isinstance(n.value, ast.Call):
                v, c = n.targets[0].id, n.value
                fn = c.func
                if isinstance(fn, ast.Attribute) and fn.attr == "ArgumentParser":
                    kind[v] = ("top", None)
                    parser_like = True
                    n_parsers += 1
                    pk = _kw(c, "parents")
                    if isinstance(pk, ast.List):
                        parents[v] = [e.id for e in pk.elts if isinstance(e, ast.Name)]
                elif isinstance(fn, ast.Attribute) and fn.attr == "add_subparsers":
                    kind[v] = ("subs", None)
                elif isinstance(fn, ast.Attribute) and fn.attr == "add_parser" and c.args:
                    name = _const(c.args[0])
                    if isinstance(name, str):
                        kind[v] = ("sub", name)
                        spec.subs.setdefault(name, {})
                        pk = _kw(c, "parents")
                        if isinstance(pk, ast.List):
                            parents[v] = [e.id for e in pk.elts if isinstance(e, ast.Name)]
            if isinstance(n, ast.Call):
                fname = n.func.id if isinstance(n.func, ast.Name) else (n.func.attr if isinstance(n.func, ast.Attribute) else "")
                passed = [a.id for a in n.args if isinstance(a, ast.Name) and a.id in kind]
                if passed and fname not in ("add_argument", "add_subparsers", "add_parser", "parse_args", "parse_known_args"):
                    if fname in HELPERS:
                        flag, req_ = HELPERS[fname]
                        spec.all_flags.add(flag)
                        w = kind[passed[0]]
                        (spec.top if w[0] == "top" else spec.subs.setdefault(w[1], {}))[flag] = {"required": req_, "takes_value": True}
                    else:
                        spec.dynamic = True                 # 不认识的 helper 会往 parser 上加东西
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "add_argument" \
                    and isinstance(n.func.value, ast.Call) and isinstance(n.func.value.func, ast.Attribute) \
                    and n.func.value.func.attr == "add_parser" and n.func.value.args:
                sname = _const(n.func.value.args[0])                      # sub.add_parser("get").add_argument(...)
                if isinstance(sname, str):
                    for a in n.args:
                        if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("-"):
                            spec.all_flags.add(a.value)
                            spec.subs.setdefault(sname, {})[a.value] = {
                                "required": _const(_kw(n, "required")) is True,
                                "takes_value": _const(_kw(n, "action")) not in ("store_true", "store_false", "count", "help", "version")}
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "add_argument" \
                    and isinstance(n.func.value, ast.Name):
                v = n.func.value.id
                flags = [a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str)
                         and a.value.startswith("-")]
                req = _const(_kw(n, "required")) is True
                act = _const(_kw(n, "action"))
                takes = act not in ("store_true", "store_false", "count", "help", "version")
                info = {"required": req, "takes_value": takes}
                for f in flags:
                    spec.all_flags.add(f)
                where = kind.get(v)
                if where is None:
                    spec.dynamic = True            # 形参 / 未追踪的 parser：无法定位归属
                    continue
                for f in flags:
                    if where[0] == "top":
                        spec.top[f] = info
                    elif where[0] == "sub":
                        spec.subs.setdefault(where[1], {})[f] = info

    visit(tree)
    spec.multi = n_parsers > 1
    # parents 合并：把被引用 parser 的 flag 并入
    owner = {v: k for v, k in kind.items()}
    for v, plist in parents.items():
        for pv in plist:
            src = kind.get(pv)
            if not src:
                spec.dynamic = True
                continue
    if not parser_like and not spec.all_flags:
        return None
    return spec


@lru_cache(maxsize=None)
def script_index() -> Dict[str, List[Path]]:
    idx: Dict[str, List[Path]] = defaultdict(list)
    for base in (REPO / "tools", SK):
        for p in base.rglob("*.py"):
            r = p.relative_to(REPO).as_posix()
            if "/attic/" in r or "/legacy/" in r or "__pycache__" in r or any(n in r for n in NESTED):
                continue
            idx[p.name].append(p)
    return idx


def resolve_script(token: str, doc: Path) -> Tuple[Optional[Path], str]:
    """返回 (path, status)；status ∈ ok / ambiguous / missing / skip。"""
    t = token.strip("\"'")
    for k, v in ALIASES.items():
        if t.startswith(k):
            t = v + t[len(k):]
    t = t.replace("\\", "/")
    t = re.sub(r"^<SKILL_ROOT>/", "Claude/skills/", t)
    if re.search(r"[<{$%]", t):
        base = Path(t).name
        if "/" not in t and base.endswith(".py"):
            pass
        else:
            cand = script_index().get(Path(t).name, [])
            return (cand[0], "ok") if len(cand) == 1 else (None, "skip")
    try:
        skill_dir = SK / doc.relative_to(SK).parts[0]
    except ValueError:                                   # 文档不在仓库里（单测用临时目录）
        skill_dir = doc.parent
    for base in (REPO, doc.parent, skill_dir):
        p = (base / t)
        if p.is_file():
            return p, "ok"
    cand = script_index().get(Path(t).name, [])
    if len(cand) == 1:
        return cand[0], "ok"
    if len(cand) > 1:
        # 同名多份：优先与路径尾部匹配者
        tail = [c for c in cand if c.as_posix().endswith(t.lstrip("./"))]
        if len(tail) == 1:
            return tail[0], "ok"
        return None, "ambiguous"
    return None, "missing"


# ----------------------------------------------------------------------------- 命令抽取
_CMD_START = re.compile(
    r"^\s*(?:[$>]\s*|PS>\s*|&\s*)?(?:(?:\"?[\w./\\:-]*(?:python3?(?:\.exe)?|\$WQ_PY|\$PY|\$env:WQ_PY|\$\{?WQ_PY\}?)\"?)\s+)"
    r"(?P<rest>.+)$")


def join_continuations(body: List[str]) -> List[Tuple[int, str]]:
    out, cur, first = [], "", 0
    for i, ln in enumerate(body):
        s = ln.rstrip()
        if not cur:
            first = i
        if s.endswith("\\") or s.endswith("`"):
            cur += s[:-1] + " "
            continue
        cur += s
        out.append((first, cur))
        cur = ""
    if cur:
        out.append((first, cur))
    return out


def extract_commands(doc: Path) -> List[dict]:
    text = doc.read_text(encoding="utf-8", errors="replace")
    all_lines = text.split("\n")
    cmds = []
    for start, _end, lang, body in fenced_blocks(text):
        if lang not in ("", "bash", "sh", "shell", "powershell", "ps1", "pwsh", "cmd", "console", "text"):
            continue
        if context_is_counterexample(all_lines, start, 3, strong=True):       # 围栏前 2 行（空行 + 引导句）
            continue
        for off, line in join_continuations(body):
            m = _CMD_START.match(line)
            if not m:
                continue
            cmds.append({"doc": doc, "line": start + off, "raw": line.strip(),
                         "head": line[:m.start("rest")].strip(), "rest": m.group("rest")})
    return cmds


def tokenize(rest: str) -> List[str]:
    rest = re.sub(r"\s#.*$", "", rest)                         # 行内注释
    rest = re.sub(r"\[[^\]]*\]", " ", rest)                    # [可选片段]
    rest = re.sub(r"(?:^|\s)(?:\|\||&&|\||;|>>?|2>&1|2>|<(?=\s)).*$", "", rest)  # 管道 / 重定向之后不看（<DIR> 占位符不算）
    try:
        return shlex.split(rest, posix=True)
    except ValueError:
        return rest.split()


# ----------------------------------------------------------------------------- 检查：命令
TK_SCRIPTS = SK / "wq-brain-campaign-toolkit" / "scripts"


@lru_cache(maxsize=None)
def campaign_dispatch() -> Dict[str, Path]:
    """campaign.py 的分发表：子命令 → 目标脚本（SUBCOMMANDS 字典 + ledger/registry/wave → _lib/*.py）。"""
    table: Dict[str, Path] = {"ledger": TK_SCRIPTS / "_lib" / "ledger.py",
                              "registry": TK_SCRIPTS / "_lib" / "registry.py",
                              "wave": TK_SCRIPTS / "_lib" / "wave_results.py"}
    try:
        tree = ast.parse((TK_SCRIPTS / "campaign.py").read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return table
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SUBCOMMANDS" for t in n.targets) \
                and isinstance(n.value, ast.Dict):
            for k, v in zip(n.value.keys, n.value.values):
                if isinstance(k, ast.Constant) and isinstance(v, ast.Constant):
                    table[str(k.value)] = TK_SCRIPTS / f"{v.value}.py"
    return table


def _split_campaign(args: List[str]) -> Tuple[Optional[str], List[str], bool]:
    """campaign.py 的全局 `--campaign-dir` 位置任意；返回 (子命令, 透传参数, 是否给了 --campaign-dir)。"""
    rest, i, has_cd = [], 0, False
    while i < len(args):
        a = args[i]
        if a == "--campaign-dir":
            has_cd = True
            i += 2
            continue
        if a.startswith("--campaign-dir="):
            has_cd = True
            i += 1
            continue
        rest.append(a)
        i += 1
    return (rest[0] if rest else None), rest[1:], has_cd


def _flag_lookup(flags: Dict[str, dict], tok: str) -> Optional[str]:
    if tok in flags:
        return tok
    cands = [f for f in flags if f.startswith(tok) and f.startswith("--") and tok.startswith("--")]
    return cands[0] if len(cands) == 1 else None            # argparse 允许唯一前缀缩写


def check_commands() -> List[dict]:
    out = []
    for doc in iter_docs():
        for c in extract_commands(doc):
            toks = tokenize(c["rest"])
            script_tok = next((t for t in toks if t.replace("\\", "/").endswith(".py")), None)
            if not script_tok:
                continue
            path, status = resolve_script(script_tok, doc)
            snippet = c["raw"][:110]
            if status == "missing":
                out.append(_v("cmd-script", doc, c["line"], f"脚本不存在: {script_tok}", snippet))
                continue
            if path is None:
                continue
            args = toks[toks.index(script_tok) + 1:]
            extra_present: Set[str] = set()
            if path.name == "campaign.py" and path.parent == TK_SCRIPTS:
                cmd, sub_args, has_cd = _split_campaign(args)
                if cmd is None or PLACEHOLDER.match(cmd) or cmd in ("-h", "--help"):
                    continue
                target = campaign_dispatch().get(cmd)
                if target is None:
                    out.append(_v("cmd-subcommand", doc, c["line"],
                                  f"campaign.py: 无子命令 {cmd!r}（有: {sorted(campaign_dispatch())}）", snippet))
                    continue
                path, args = target, sub_args
                if has_cd:
                    extra_present.add("--campaign-dir")           # 分发器会把它补回 argv（或已在内部消费）
            spec = parse_argparse(str(path))
            if spec is None:
                continue
            sub, present, i, bad_sub = None, set(extra_present), 0, False
            top = spec.top
            while i < len(args):
                t = args[i]
                if t.startswith("-") and not PLACEHOLDER.match(t):
                    name = t.split("=", 1)[0]
                    flags = spec.flags_for(sub)
                    hit = _flag_lookup(flags, name) or (name if name in spec.all_flags else None)
                    if hit is None and not spec.dynamic and name not in ("-h", "--help"):
                        out.append(_v("cmd-flag", doc, c["line"],
                                      f"{path.name}{' ' + sub if sub else ''}: 未知参数 {name}", snippet))
                    else:
                        present.add(hit or name)
                    if hit and flags.get(hit, {}).get("takes_value", True) and "=" not in t:
                        i += 1
                    elif hit is None and i + 1 < len(args) and not args[i + 1].startswith("-"):
                        i += 1
                elif spec.subs and sub is None and not bad_sub:
                    if t in spec.subs:
                        sub = t
                    elif not PLACEHOLDER.match(t):
                        out.append(_v("cmd-subcommand", doc, c["line"],
                                      f"{path.name}: 无子命令 {t!r}（有: {sorted(spec.subs)}）", snippet))
                        bad_sub = True
                i += 1
            elided = any(PLACEHOLDER.match(t) and t in ("...", "…") for t in args)
            if not elided and not spec.dynamic and not spec.multi and not bad_sub:
                need = {f for f, inf in spec.flags_for(sub).items() if inf.get("required")}
                miss = sorted(f for f in need if f not in present)
                if miss:
                    out.append(_v("cmd-required", doc, c["line"],
                                  f"{path.name}{' ' + sub if sub else ''}: 缺必填参数 {miss}", snippet))
    return out


# ----------------------------------------------------------------------------- 检查：MCP 调用
@lru_cache(maxsize=None)
def mcp_registry() -> Dict[str, Dict[str, Set[str]]]:
    """{server: {tool: {param,…}}}（AST：@mcp.tool 装饰的函数签名）。"""
    files = {"wq-brain-http": sorted((REPO / "world-quant-brain-mcp").glob("tools_*.py")),
             "wqb-db": [REPO / "wqb_db_mcp.py"]}
    reg: Dict[str, Dict[str, Set[str]]] = {k: {} for k in files}
    for server, paths in files.items():
        for p in paths:
            try:
                tree = ast.parse(p.read_text(encoding="utf-8"))
            except (OSError, SyntaxError):
                continue
            for n in ast.walk(tree):
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    decos = [ast.unparse(d) for d in n.decorator_list]
                    if any("mcp.tool" in d for d in decos):
                        a = n.args
                        names = {x.arg for x in a.args + a.kwonlyargs + a.posonlyargs}
                        reg[server][n.name] = names
    return reg


_MCP_CALL = re.compile(r"mcp__(wq-brain-http|wqb-db)__(\w+)\s*\(")


def _match_paren(text: str, i: int, limit: int = 2500) -> str:
    depth, j = 1, i
    while j < min(len(text), i + limit) and depth:
        ch = text[j]
        depth += (ch == "(") - (ch == ")")
        j += 1
    return text[i:j - 1] if depth == 0 else text[i:j]


def _top_level_kwargs(argstr: str) -> Set[str]:
    depth, cur, names = 0, [], set()
    parts = []
    for ch in argstr:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    for p in parts:
        m = re.match(r"\s*([A-Za-z_]\w*)\s*=(?!=)", p)
        if m:
            names.add(m.group(1))
    return names


def check_mcp() -> List[dict]:
    out, reg = [], mcp_registry()
    for doc in iter_docs():
        text = doc.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")
        for m in _MCP_CALL.finditer(text):
            server, tool = m.group(1), m.group(2)
            line = text.count("\n", 0, m.start()) + 1
            if context_is_counterexample(lines, line, 2) or COUNTER_MARK.search(lines[line - 1]):
                continue
            snippet = lines[line - 1].strip()[:110]
            if tool not in reg.get(server, {}):
                out.append(_v("mcp-tool", doc, line, f"{server} 无工具 {tool}", snippet))
                continue
            kw = _top_level_kwargs(_match_paren(text, m.end()))
            bad = sorted(k for k in kw if k not in reg[server][tool])
            if bad:
                out.append(_v("mcp-param", doc, line, f"{tool}: 签名里没有参数 {bad}", snippet))
    return out


# ----------------------------------------------------------------------------- 检查：表达式过闸
_OPS_HINT = re.compile(r"\b(rank|ts_[a-z_]+|group_[a-z_]+|add|subtract|multiply|divide|zscore|scale|trade_when|"
                       r"if_else|vec_[a-z_]+|winsorize|quantile|hump|normalize|signed_power|abs|log)\s*\(")
_EXPR_MIN_LEN = 14


@lru_cache(maxsize=None)
def _gate():
    import importlib.util
    for p in (str(REPO / "src"), str(SK / "wq-brain-campaign-toolkit" / "scripts")):
        if p not in sys.path:
            sys.path.insert(0, p)
    gp = SK / "wq-brain-campaign-toolkit" / "scripts" / "gate.py"
    spec = importlib.util.spec_from_file_location("_skill_lint_gate", gp)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_skill_lint_gate"] = mod
    spec.loader.exec_module(mod)
    pc = json.loads((SK / "wq-brain-campaign-toolkit" / "config" / "platform_constraints.json").read_text(encoding="utf-8"))
    pc["_region"] = "USA"
    return mod, pc


#: 只报「策略/平台事实」类违规（加权混合、幽灵算子、不可访问算子）。[SYNTAX]/[ARITY] 不报：文档里的表达式大多是
#: 伪代码/模板（`ts_rank(...)`、`winsorize(x, std=N)`、`{f}`），语法层报警几乎全是噪声。
_GATE_KINDS = ("[POISON:", "[GHOST]", "[INACCESSIBLE]")


def _looks_like_expr(s: str) -> bool:
    s = s.strip()
    if len(s) < _EXPR_MIN_LEN or s.count("(") != s.count(")") or not _OPS_HINT.search(s):
        return False
    if re.search(r"[一-鿿]", s) or s.startswith(("python", "$", "&", "#", "http", "--")) or " = " in s.split("(")[0]:
        return False
    return True


def check_exprs() -> List[dict]:
    try:
        gate, pc = _gate()
    except Exception as e:                                   # noqa: BLE001
        return [{"check": "expr-gate", "file": "-", "line": 0, "msg": f"闸门加载失败: {e}", "snippet": "-", "key": "expr-gate|-|load"}]
    out = []
    for doc in iter_docs():
        text = doc.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")
        cands: List[Tuple[int, str]] = []
        for start, _e, lang, body in fenced_blocks(text):
            if lang not in ("", "text", "fastexpr", "brain", "alpha", "expr", "python", "js"):
                continue
            if context_is_counterexample(lines, start, 4):
                continue
            for k, ln in enumerate(body):
                s = ln.strip().rstrip(";,")
                if _looks_like_expr(s) and not COUNTER_MARK.search(ln) and EXEMPT_MARK not in ln:
                    cands.append((start + k, s))
        for k, ln in enumerate(lines, 1):
            if COUNTER_MARK.search(ln) or EXEMPT_MARK in ln or (k > 1 and EXEMPT_MARK in lines[k - 2]):
                continue
            for m in re.finditer(r"`([^`\n]{%d,})`" % _EXPR_MIN_LEN, ln):
                if _looks_like_expr(m.group(1)):
                    cands.append((k, m.group(1).strip()))
        seen = set()
        for line, expr in cands:
            if (line, expr) in seen:
                continue
            seen.add((line, expr))
            idents = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr))
            ops = set(pc["known_ops"]) | set(pc["group_identifiers"]) | set(pc["price_volume_fields"]) | set(pc["driver_args"])
            fields = {t for t in idents if t not in ops}
            try:
                item = gate.check_one(expr, (fields, "MATRIX", {f: "MATRIX" for f in fields}, []), "D1",
                                      list(pc["poison_patterns"]), pc)
            except Exception:                                # noqa: BLE001
                continue
            bad = [i for i in item["issues"] if i.startswith(_GATE_KINDS) and not i.startswith("[SYNTAX_UNKNOWN]")]
            if bad:
                out.append(_v("expr-gate", doc, line, bad[0][:140], expr[:110]))
    return out


# ----------------------------------------------------------------------------- 检查：凭据 / 裸 python
_ENV_READ = re.compile(r"load_dotenv|(?:cat|type|Get-Content|读取|打开|source)\s+[^\n]{0,40}\.env\b|world-quant-brain-mcp/\.env")
_PWD_CLI = re.compile(r"--(?:password|passwd)\b|--email\s+\S+@|password\s*=\s*[\"'][^\"']+[\"']", re.I)
_PROHIBIT = re.compile(r"禁止|不得|勿|不要|绝不|never|do not|don't|不读取|不接触|不能|严禁")


def check_secrets() -> List[dict]:
    out = []
    for doc in iter_docs():
        lines = doc.read_text(encoding="utf-8", errors="replace").split("\n")
        for i, ln in enumerate(lines, 1):
            prev = " ".join(lines[max(0, i - 3):i - 1])
            # 同行有禁止/反例词，或前 2 行有强反例标记才豁免（相邻的「禁止」规则句不代表下一行也是反例）
            if _PROHIBIT.search(ln) or COUNTER_MARK.search(ln) or STRONG_COUNTER.search(prev) or EXEMPT_MARK in prev:
                continue
            if _ENV_READ.search(ln):
                out.append(_v("env-read", doc, i, "文档指示读取 .env（凭据只由 MCP 服务端加载，agent 不接触）", ln.strip()[:110]))
            if _PWD_CLI.search(ln):
                out.append(_v("cli-password", doc, i, "命令行/示例里传口令或邮箱", ln.strip()[:110]))
    return out


def check_bare_python() -> List[dict]:
    out = []
    for doc in iter_docs():
        for c in extract_commands(doc):
            head = c["head"].lstrip("$>& ").strip().strip('"')
            if not re.fullmatch(r"python3?(\.exe)?", head):
                continue
            toks = tokenize(c["rest"])
            script_tok = next((t for t in toks if t.replace("\\", "/").endswith(".py")), None)
            if script_tok is None or script_tok.endswith("_pyenv.py"):
                continue
            path, _ = resolve_script(script_tok, doc)
            if path is not None and "import _pyenv" in path.read_text(encoding="utf-8", errors="replace"):
                continue                                     # 目标脚本自带 re-exec：裸 python 也能跑
            out.append(_v("bare-python", doc, c["line"], "裸 python（用 $WQ_PY，或目标脚本接入 tools/_pyenv）", c["raw"][:110]))
    return out


# ----------------------------------------------------------------------------- 汇总 / 基线
def _v(check: str, doc: Path, line: int, msg: str, snippet: str) -> dict:
    norm = re.sub(r"\s+", " ", snippet).strip()
    return {"check": check, "file": rel(doc), "line": line, "msg": msg, "snippet": snippet,
            "key": f"{check}|{rel(doc)}|{norm[:80]}|{msg[:60]}"}


CHECKS = {
    "cmd": check_commands,
    "mcp": check_mcp,
    "expr": check_exprs,
    "secret": check_secrets,
    "bare-python": check_bare_python,
}


def run(selected: Optional[List[str]] = None) -> List[dict]:
    out: List[dict] = []
    for name, fn in CHECKS.items():
        if selected and not any(name.startswith(s) for s in selected):
            continue
        out.extend(fn())
    return out


def load_baseline() -> Dict[str, int]:
    if not BASELINE.is_file():
        return {}
    return json.loads(BASELINE.read_text(encoding="utf-8")).get("violations", {})


def counts(vs: List[dict]) -> Dict[str, int]:
    c: Dict[str, int] = defaultdict(int)
    for v in vs:
        c[v["key"]] += 1
    return dict(c)


def diff_against_baseline(vs: List[dict]) -> Tuple[List[str], List[str]]:
    now, base = counts(vs), load_baseline()
    new = sorted(k for k, n in now.items() if n > base.get(k, 0))
    fixed = sorted(k for k, n in base.items() if now.get(k, 0) < n)
    return new, fixed


def main() -> int:
    ap = argparse.ArgumentParser(description="skill 文档内容为真机检（命令 / MCP 调用 / 表达式 / 凭据 / 裸 python）")
    ap.add_argument("--check", action="append", help="只跑某类（前缀匹配，可重复）：cmd/mcp/expr/secret/bare-python")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--update-baseline", action="store_true", help="把当前违规写入基线（需人审 diff）")
    a = ap.parse_args()
    vs = run(a.check)
    if a.update_baseline:
        if a.check:
            print("--update-baseline 需要全量检查（不带 --check）", file=sys.stderr)
            return 2
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps({
            "_doc": "skill_lint 棘轮基线：现存已知违规。新增违规测试必红；修复后必须从这里删除（测试会提示）。"
                    "只在有意接受时用 `python tools/skill_lint.py --update-baseline` 重写，并人审 diff。",
            "violations": dict(sorted(counts(vs).items()))}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"baseline written: {len(vs)} violations / {len(counts(vs))} keys")
        return 0
    new, fixed = diff_against_baseline(vs)
    if a.json:
        print(json.dumps({"violations": vs, "new": new, "fixed": fixed}, ensure_ascii=False, indent=1))
        return 1 if new else 0
    by = defaultdict(list)
    for v in vs:
        by[v["check"]].append(v)
    for chk in sorted(by):
        print(f"\n== {chk}: {len(by[chk])} ==")
        for v in by[chk][:60]:
            mark = "NEW " if v["key"] in new else "    "
            print(f"{mark}{v['file']}:{v['line']}  {v['msg']}\n       {v['snippet']}")
    print(f"\n总计 {len(vs)} 条；相对基线 新增 {len(new)} / 已修复待清基线 {len(fixed)}")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
