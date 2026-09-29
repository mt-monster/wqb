# -*- coding: utf-8 -*-
"""skills 机械核查（2026-09-29）：给「按 skill、按阶段的文字审查」提供可复现的事实依据。

只读：不改任何 skill。用 MCP venv 的 python 跑：
    world-quant-brain-mcp/.venv/bin/python reports/skills_review_20260929/check_skills.py [--section A,B,...]

覆盖 tests/unit/test_skill_integrity.py 没覆盖的面：references/ 下的文档、反引号里的路径、命令行 --flag、
MCP 调用的参数名、字面阈值与 wqb.config 的一致性、跨文件重复段落、结构信号、触发词重叠、孤儿文件、互引对称性。
每一节的输出都是"待人工判读的线索"，不是结论——报告里逐条核对过再引用。
"""
from __future__ import annotations

import ast
import argparse
import difflib
import hashlib
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SK = REPO / "Claude" / "skills"
TOOLKIT = SK / "wq-brain-campaign-toolkit"
MCP_DIR = REPO / "world-quant-brain-mcp"
sys.path.insert(0, str(REPO / "src"))

#: 外部论坛语料 / 内嵌的重复 skill 副本：不参与"文字质量"类检查（重复检查单独处理）
CORPUS = ("brain-alpha-judge/data/forum_corpus/",)
NESTED = ("brain-make-some-gem/scripts/trailSomeAlphas/skills/",)


def rel(p: Path) -> str:
    return str(p.relative_to(REPO)).replace("\\", "/")


def all_md(include_nested: bool = False):
    out = []
    for p in sorted(SK.rglob("*.md")):
        r = rel(p)
        if any(c in r for c in CORPUS):
            continue
        if not include_nested and any(n in r for n in NESTED):
            continue
        out.append(p)
    return out


def skill_of(p: Path) -> str:
    return p.relative_to(SK).parts[0]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def frontmatter(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm, cur = {}, None
    if not m:
        return fm
    for ln in m.group(1).splitlines():
        mm = re.match(r"^([A-Za-z_\-]+):\s*(.*)$", ln)
        if mm:
            cur = mm.group(1)
            fm[cur] = mm.group(2).strip().strip('"')
        elif cur and ln.startswith((" ", "\t", "-")):
            fm[cur] = (fm[cur] + " " + ln.strip()).strip()
    return fm


def fenced_spans(text: str):
    """[(start_line, end_line)]（1-based，含围栏行），用来区分代码块与正文。"""
    spans, start = [], None
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.lstrip().startswith("```"):
            if start is None:
                start = i
            else:
                spans.append((start, i))
                start = None
    return spans


def in_fence(spans, line_no: int) -> bool:
    return any(a <= line_no <= b for a, b in spans)


def git_files():
    out = subprocess.run(["git", "-C", str(REPO), "ls-files"], capture_output=True, text=True).stdout.splitlines()
    return out


# ------------------------------------------------------------------ A. 元数据
def sec_A():
    print("== A. frontmatter / 元数据 ==")
    dates, layers = Counter(), Counter()
    rows = []
    for d in sorted(SK.iterdir()):
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        fm = frontmatter(read(f))
        dates[fm.get("last_verified")] += 1
        layers[fm.get("layer")] += 1
        desc = fm.get("description", "")
        rows.append((d.name, fm.get("layer"), len(desc), len(read(f).splitlines()),
                     bool(re.search(r"触发词|Triggers?|当用户|when the user|Use when|使用", desc, re.I)),
                     bool(fm.get("allowed-tools") or "allowed-tools" in read(f)[:600]),
                     "user-invocable" in read(f)[:800]))
    print("last_verified 取值分布：", dict(dates))
    print("layer 取值分布：", dict(layers))
    print(f"{'skill':46} {'layer':7} {'desc_len':>8} {'lines':>6} trig  allowed-tools  user-invocable")
    for r in sorted(rows, key=lambda x: -x[2]):
        print(f"{r[0]:46} {str(r[1]):7} {r[2]:8} {r[3]:6} {str(r[4]):5} {str(r[5]):14} {r[6]}")


# ------------------------------------------------------------------ B/C. 链接与路径
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_PATH_TOKEN = re.compile(r"(?<![\w/.\\-])((?:[A-Za-z0-9_.\-]+[/\\])*[A-Za-z0-9_\-]+\.(?:py|md|json|sh|ps1|yaml|yml|csv|txt|bin))(?![\w])")
_RUNTIME = re.compile(
    r"(^|/)(tracking|cache|logs|output|output_report|attic|results|candidates|priors|reviews|checkpoint|batches|"
    r"config|reference|deepexplore|forum_notes|workspace|memory)/|^data/|wqb\.db|settings\.json|"
    r"final_expressions|simulation_status|checkpoint|_results?\.(json|csv)|wave\w*\.(json|csv)|"
    r"\.mcp\.json|mcp_config\.json|forum_findings|forum_stroll|run_contract|session_plan|"
    r"task_plan|findings\.md|progress\.md|personal_experience|SKILL\.md|README\.md|INDEX\.md|"
    r"_ledger\.json|ledger_snapshot|gate_results|ranking\.json|selection_plan|\bs\d_walls",
    re.I)


def build_index():
    files = git_files()
    by_base = defaultdict(list)
    for f in files:
        by_base[f.rsplit("/", 1)[-1]].append(f)
    return files, by_base


#: 文档里当作目录变量/别名用的前缀 → 实际目录（别名是否在文中定义过，另在报告里人工核对）
_ALIASES = {"TK/": TOOLKIT / "scripts", "$TK/": TOOLKIT / "scripts", "WQ_TOOLKIT_DIR/": TOOLKIT / "scripts",
            "$WQ_TOOLKIT_DIR/": TOOLKIT / "scripts", "WQ_VALIDATOR_DIR/": TOOLKIT / "scripts",
            "$WQ_VALIDATOR_DIR/": TOOLKIT / "scripts"}
#: 通用占位名 / 示例产物名：不是仓库文件，不参与"文件是否存在"
_GENERIC = re.compile(r"^(_[\w.\-]+|config\.json|file\.json|out\.json|meta\.json|notes\.json|dead\.json|win\.json|"
                      r"spec\.json|exprs\.json|ideas\.md|todo\.md|draft\.md|todos\.json|script\.py|todo\.py|main\.py|"
                      r"utils\.py|priors\.json|notes\.md|instructions\.md|MEMORY\.md|user_config\.json|new_exprs\.json|"
                      r"path_to_ideas\.md|.*_ideas\.md|.*_fields\.json|.*_exprs\.json|.*_batches\.json|.*_raw\.json|"
                      r"generation_constraints\.json|gate_cache\.json|.*_results?\.(?:json|txt))$")


def resolve(token: str, md: Path):
    t = token.replace("\\", "/")
    for a, d in _ALIASES.items():
        if t.startswith(a):
            cand = d / t[len(a):]
            return cand if cand.exists() else None
    t = t.lstrip("./") if not t.startswith("../") else t
    skill_dir = SK / skill_of(md)
    roots = [md.parent, skill_dir, skill_dir / "scripts", skill_dir / "references", REPO, REPO / "tools",
             REPO / "src", REPO / "docs", SK, TOOLKIT / "scripts", TOOLKIT / "scripts" / "_lib", TOOLKIT,
             MCP_DIR, REPO / "src" / "wqb", REPO / "src" / "wqb" / "workflow"]
    for r in roots:
        cand = (r / t).resolve()
        if cand.exists():
            return cand
    return None


def sec_B():
    print("== B. markdown 链接（全部 md，含 references/）==")
    n = bad = 0
    for md in all_md():
        text = read(md)
        for m in _LINK.finditer(text):
            t = m.group(1)
            if t.startswith(("http://", "https://", "#", "mailto:")) or "<" in t or "{" in t:
                continue
            n += 1
            tt = t.split("#")[0]
            if not tt:
                continue
            if not resolve(tt, md):
                bad += 1
                line = text[:m.start()].count("\n") + 1
                print(f"  BROKEN  {rel(md)}:{line}  → {t}")
    print(f"  共 {n} 条相对链接，断 {bad}")


def sec_C():
    print("== C. 反引号 / 正文里的路径（脚本、文档、模块）——解析不到的 ==")
    files, by_base = build_index()
    seen = set()
    miss = []
    elsewhere = []
    for md in all_md():
        text = read(md)
        for i, ln in enumerate(text.splitlines(), 1):
            for m in _PATH_TOKEN.finditer(ln):
                tok = m.group(1)
                if any(c in tok for c in "<>{}*$%") or tok.startswith("http") or "..." in tok:
                    continue
                if _RUNTIME.search(tok) or _GENERIC.match(tok.rsplit("/", 1)[-1]):
                    continue
                key = (rel(md), tok)
                if key in seen:
                    continue
                seen.add(key)
                if resolve(tok, md):
                    continue
                base = tok.rsplit("/", 1)[-1]
                if "/" not in tok.replace("\\", "/") and base in by_base:
                    elsewhere.append((rel(md), i, tok, by_base[base][:3]))
                else:
                    miss.append((rel(md), i, tok))
    print(f"  不存在（仓库里任何常见根下都解析不到）：{len(miss)} 处")
    for r in miss:
        print(f"    MISSING  {r[0]}:{r[1]}  {r[2]}")
    print(f"  只写了文件名、要靠仓库全局同名文件才能落地：{len(elsewhere)} 处（歧义位置）")
    for r in elsewhere[:80]:
        print(f"    AMBIG    {r[0]}:{r[1]}  {r[2]}  → {r[3]}")


# ------------------------------------------------------------------ D. 命令行 flag
_FLAG = re.compile(r"(?<![\w-])(--[A-Za-z][\w-]*)")
_PYTOK = re.compile(r"([A-Za-z0-9_./\\-]+\.py)\b")


def command_candidates(text: str):
    """(line_no, 命令文本)：围栏代码块按续行合并；行内 `code` 各自一条。"""
    lines = text.splitlines()
    spans = fenced_spans(text)
    out = []
    for a, b in spans:
        buf, start = "", None
        for i in range(a + 1, b):
            ln = lines[i - 1]
            if start is None:
                start = i
            buf += " " + ln.strip()
            if not (ln.rstrip().endswith(("\\", "`", "^", ",")) or (i < b - 1 and lines[i].lstrip().startswith("--"))):
                out.append((start, buf.strip()))
                buf, start = "", None
        if buf:
            out.append((start or a, buf.strip()))
    for i, ln in enumerate(lines, 1):
        if in_fence(spans, i):
            continue
        for m in re.finditer(r"`([^`\n]*\.py[^`\n]*)`", ln):
            out.append((i, m.group(1)))
    return out


def script_texts(script: Path):
    d = script.parent
    txt = read(script)
    if script.name in ("campaign.py", "main.py", "pipeline.py") or True:
        for f in sorted(d.glob("*.py")):
            txt += "\n" + read(f)
        lib = d / "_lib"
        if lib.is_dir():
            for f in sorted(lib.glob("*.py")):
                txt += "\n" + read(f)
    return txt


def sec_D():
    print("== D. 命令行里的 --flag 在目标脚本（及同目录）里根本没出现 ==")
    n = bad = 0
    seen = set()
    for md in all_md():
        for line_no, cmd in command_candidates(read(md)):
            pm = _PYTOK.search(cmd)
            if not pm:
                continue
            tok = pm.group(1)
            if any(c in tok for c in "<>{}*$%"):
                continue
            script = resolve(tok, md)
            flags = [f for f in _FLAG.findall(cmd)]
            if not script or not flags:
                continue
            txt = script_texts(script)
            for f in flags:
                n += 1
                if f in ("--help", "--version"):
                    continue
                if f not in txt:
                    key = (rel(md), tok, f)
                    if key in seen:
                        continue
                    seen.add(key)
                    bad += 1
                    print(f"  NOFLAG  {rel(md)}:{line_no}  {tok} {f}   （{rel(script)} 及同目录都没有这个 flag）")
    print(f"  共核对 {n} 个 flag，缺失 {bad}")


# ------------------------------------------------------------------ E. MCP 工具与参数
def load_tools():
    tools = {}
    pat = re.compile(r"@mcp\.tool\([^)]*\)\s*\n\s*(?:async\s+)?def\s+([A-Za-z0-9_]+)")
    srcs = [(f, "wq-brain-http") for f in sorted(MCP_DIR.glob("tools_*.py")) + [MCP_DIR / "main.py", MCP_DIR / "mcp_core.py"]
            if f.exists()] + [(REPO / "wqb_db_mcp.py", "wqb-db")]
    for f, server in srcs:
        text = read(f)
        names = set(m.group(1) for m in pat.finditer(text))
        try:
            tree = ast.parse(text)
        except SyntaxError:
            tree = None
        sig = {}
        if tree:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names:
                    a = node.args
                    params = [x.arg for x in a.args + a.kwonlyargs]
                    ndef = len(a.defaults)
                    req = params[:len(a.args) - ndef] if ndef else params[:len(a.args)]
                    sig[node.name] = (params, [r for r in req])
        for nm in names:
            tools[f"mcp__{server}__{nm}"] = sig.get(nm, (None, None))
    return tools


def match_paren(text: str, i: int, limit: int = 2500):
    """text[i] == '('；返回配对 ')' 的位置（找不到返回 -1）。"""
    depth = 0
    for j in range(i, min(len(text), i + limit)):
        c = text[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return j
    return -1


def sec_E():
    print("== E. MCP 工具引用：未注册的工具名 / 调用里不存在的参数名（含 references/）==")
    tools = load_tools()
    short = {k.split("__", 2)[2]: k for k in tools}
    pat_full = re.compile(r"mcp__(?:wq-brain-http|wqb-db)__[A-Za-z0-9_]*\*?")
    unknown, badparam = [], []
    for md in all_md():
        text = read(md)
        for m in pat_full.finditer(text):
            name = m.group(0)
            if name.endswith("*") or re.match(r"^mcp__[a-z-]+__$", name):
                continue
            line = text[:m.start()].count("\n") + 1
            if name not in tools:
                unknown.append((rel(md), line, name))
                continue
            # 调用形态：name( ... )
            j = m.end()
            if j < len(text) and text[j] == "(":
                e = match_paren(text, j)
                if e > 0:
                    body = text[j + 1:e]
                    params, _req = tools[name]
                    if params:
                        for kw in re.findall(r"(?<![\w.\"'])([A-Za-z_]\w*)\s*=(?!=)", body):
                            if kw not in params and kw not in ("True", "False", "None"):
                                badparam.append((rel(md), line, name.split("__", 2)[2], kw, params))
    print(f"  未注册（工具表里没有）：{len(unknown)} 处")
    seen = set()
    for r in unknown:
        if (r[0], r[2]) in seen:
            continue
        seen.add((r[0], r[2]))
        print(f"    UNKNOWN-TOOL  {r[0]}:{r[1]}  {r[2]}")
    print(f"  调用里的参数名不在函数签名里：{len(badparam)} 处")
    seen = set()
    for r in badparam:
        if (r[0], r[2], r[3]) in seen:
            continue
        seen.add((r[0], r[2], r[3]))
        print(f"    BAD-PARAM  {r[0]}:{r[1]}  {r[2]}({r[3]}=…)   签名={r[4]}")


# ------------------------------------------------------------------ F. 阈值字面值
_NUM = r"([0-9]+(?:\.[0-9]+)?)"
_THR = {
    "Sharpe": re.compile(r"(?<![A-Za-z_])(?:Sharpe|sharpe)(?![A-Za-z_])[^\n|]{0,12}?(?:>=|≥|>|＞|不低于|至少)\s*" + _NUM),
    "Fitness": re.compile(r"(?<![A-Za-z_])(?:Fitness|fitness)(?![A-Za-z_])[^\n|]{0,12}?(?:>=|≥|>|＞|不低于|至少)\s*" + _NUM),
    "PROD相关": re.compile(r"(?:prod|PROD)[_ ]?(?:corr(?:elation)?|相关)?[^\n|]{0,8}?(?:<=|<|≤|＜)\s*" + _NUM),
    "SELF相关": re.compile(r"(?:self|SELF)[_ ]?(?:corr(?:elation)?|相关)?[^\n|]{0,8}?(?:<=|<|≤|＜)\s*" + _NUM),
    "槽位数": re.compile(r"(?:并发|槽位?|slots?|在飞|填槽)[^\n|]{0,10}?[=≈:：]?\s*([3-9]|1[0-9])\s*(?:槽|批|个槽|slots?)"),
}


def sec_F():
    print("== F. 字面阈值（对照 wqb.config：internal sharpe 1.58 / fitness 1.0 / self 0.50；platform self·prod 0.70；槽位 7）==")
    try:
        from wqb import config as C
        print("  config：internal", C.GATES_INTERNAL, "\n          platform", C.GATES_PLATFORM,
              "\n          slots", C.CONCURRENCY["slots"], " STANDARD_WINDOWS", C.STANDARD_WINDOWS)
    except Exception as e:  # noqa: BLE001
        print("  (读 config 失败)", e)
    agg = defaultdict(lambda: defaultdict(list))
    for md in all_md():
        text = read(md)
        for i, ln in enumerate(text.splitlines(), 1):
            for metric, rx in _THR.items():
                for m in rx.finditer(ln):
                    agg[metric][m.group(1)].append((rel(md), i))
    cfg_ok = {"Sharpe": {"1.58"}, "Fitness": {"1.0", "1.00", "1"}, "PROD相关": {"0.7", "0.70"},
              "SELF相关": {"0.7", "0.70", "0.5", "0.50"}, "槽位数": {"7"}}
    for metric, vals in agg.items():
        print(f"  [{metric}] 取值 → 出现次数（涉及文件数）；与 config 一致的只计数，不一致的逐条列出位置")
        for v, locs in sorted(vals.items(), key=lambda kv: -len(kv[1])):
            files = sorted({l[0] for l in locs})
            print(f"     {v:>6}: {len(locs):3d} 次 / {len(files):2d} 文件" + ("" if v in cfg_ok.get(metric, set()) else "   ← 与 config 不同"))
            if v not in cfg_ok.get(metric, set()):
                for f, ln in locs[:8]:
                    line = read(REPO / f).splitlines()[ln - 1].strip()
                    print(f"          {f.replace('Claude/skills/', '')}:{ln}  {line[:150]}")


# ------------------------------------------------------------------ G. 重复
def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def sec_G():
    print("== G. 跨文件重复的段落（≥100 字符；按文件对汇总）；近似重复的文件对 ==")
    groups = defaultdict(set)
    for md in all_md(include_nested=True):
        text = read(md)
        text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
        for para in re.split(r"\n\s*\n", text):
            p_ = norm(para)
            if len(p_) >= 100:
                groups[hashlib.md5(p_.encode()).hexdigest()].add((rel(md), p_[:100]))
    pair = defaultdict(int)
    detail = defaultdict(list)
    for k, v in groups.items():
        files = sorted({x[0] for x in v})
        if len(files) < 2:
            continue
        for a in range(len(files)):
            for b in range(a + 1, len(files)):
                pair[(files[a], files[b])] += 1
                detail[(files[a], files[b])].append(next(iter(v))[1])
    print(f"  共 {len(pair)} 个文件对有重复段落；按重复段数排序（前 30）：")
    for (a, b), n in sorted(pair.items(), key=lambda kv: -kv[1])[:30]:
        print(f"    {n:3d} 段  {a.replace('Claude/skills/', '')}  ↔  {b.replace('Claude/skills/', '')}")
    print("  --- 非「嵌套副本」的重复段落样例（每对最多 2 段）")
    for (a, b), n in sorted(pair.items(), key=lambda kv: -kv[1]):
        if any(x in a or x in b for x in NESTED):
            continue
        print(f"    {a.replace('Claude/skills/', '')} ↔ {b.replace('Claude/skills/', '')}  ({n} 段)")
        for d in detail[(a, b)][:2]:
            print(f"        · {d!r}")
    print("  --- 近似重复文件对（3 行滑窗 Jaccard ≥ 0.45）")
    mds = all_md(include_nested=True)
    sh = {}
    for md in mds:
        ls = [norm(l) for l in read(md).splitlines() if norm(l)]
        sh[md] = {" ".join(ls[i_:i_ + 3]) for i_ in range(max(1, len(ls) - 2))}
    for a in range(len(mds)):
        for b in range(a + 1, len(mds)):
            A, B = sh[mds[a]], sh[mds[b]]
            if len(A) < 8 or len(B) < 8:
                continue
            j_ = len(A & B) / len(A | B)
            if j_ >= 0.45:
                print(f"    {j_:.2f}  {rel(mds[a]).replace('Claude/skills/', '')}  ↔  {rel(mds[b]).replace('Claude/skills/', '')}")


# ------------------------------------------------------------------ H. 结构信号
_HIST = re.compile(r"此前|原先|曾经|曾[^a-zA-Z]|已废弃|已废止|已移除|已并入|已合并|不再|旧版|历史|起已|起改|落地")
_DATEP = re.compile(r"[（(]\s*(?:20\d\d-\d\d-\d\d|\d\d-\d\d)[^）)]*[）)]")
_IMPER = re.compile(r"禁止|不得|严禁|必须|铁律|不要")


def sec_H():
    print("== H. SKILL.md 结构信号（每 100 行的历史叙述 / 日期括号；有无显式 边界·失败·示例·验收 节）==")
    rows = []
    for d in sorted(SK.iterdir()):
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        text = read(f)
        lines = text.splitlines()
        n = len(lines)
        heads = [l for l in lines if l.startswith("#")]
        h_all = "\n".join(heads)
        sig = {
            "when": bool(re.search(r"何时|触发|适用|使用场景|When|Trigger", h_all, re.I)),
            "nogo": bool(re.search(r"不适用|不要|禁止|反模式|不做|Anti|Non-?goal|红线", h_all, re.I)),
            "fail": bool(re.search(r"失败|回退|故障|排障|错误|异常|Troubleshoot|Failure|Error", h_all, re.I)),
            "example": bool(re.search(r"示例|例子|场景|战例|案例|Example|Scenario|实证", h_all, re.I)),
            "check": bool(re.search(r"检查清单|自检|验收|Checklist|完成定义|验证", h_all, re.I)),
            "output": bool(re.search(r"产物|输出|Output|交付|Artifact", h_all, re.I)),
        }
        rows.append((d.name, n, len(heads), len(_HIST.findall(text)) * 100 / max(n, 1),
                     len(_DATEP.findall(text)) * 100 / max(n, 1), len(_IMPER.findall(text)),
                     max((len(l) for l in lines), default=0), sum(1 for l in lines if len(l) > 220), sig))
    print(f"{'skill':46}{'lines':>6}{'heads':>6}{'hist/100':>9}{'date/100':>9}{'imper':>6}{'maxline':>8}{'>220':>5}  when nogo fail ex chk out")
    for r in sorted(rows, key=lambda x: -x[3]):
        s = r[8]
        flags = " ".join("Y" if s[k] else "." for k in ("when", "nogo", "fail", "example", "check", "output"))
        print(f"{r[0]:46}{r[1]:6}{r[2]:6}{r[3]:9.1f}{r[4]:9.1f}{r[5]:6}{r[6]:8}{r[7]:5}   {flags}")


# ------------------------------------------------------------------ I. 触发词重叠
def sec_I():
    print("== I. description 里的触发词在多个 skill 间重叠（会让路由靠运气）==")
    toks = defaultdict(set)
    for d in sorted(SK.iterdir()):
        f = d / "SKILL.md"
        if not f.is_file():
            continue
        desc = frontmatter(read(f)).get("description", "")
        for t in re.split(r"[/、,，;；：:。()（）「」\"“”\s]+", desc):
            t = t.strip()
            if len(t) >= 3 and not re.fullmatch(r"[A-Za-z]{1,4}", t):
                toks[t].add(d.name)
    shared = {t: s for t, s in toks.items() if len(s) >= 2}
    for t, s in sorted(shared.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"    {t!r}: {sorted(s)}")


# ------------------------------------------------------------------ J. 孤儿
def sec_J():
    print("== J. 孤儿文档：没有任何其他文件提到它的 md（skill 目录内）==")
    mds = all_md(include_nested=True)
    texts = {md: read(md) for md in mds}
    pytexts = {p: read(p) for p in SK.rglob("*.py")}
    for md in mds:
        if md.name == "SKILL.md":
            continue
        base = md.name
        stem = md.stem
        hits = 0
        for other, t in list(texts.items()) + list(pytexts.items()):
            if other == md:
                continue
            if base in t:
                hits += 1
        if hits == 0:
            print(f"    ORPHAN  {rel(md)}")


# ------------------------------------------------------------------ K. 互引
def sec_K():
    print("== K. 互引对称性：A 的 SKILL.md 提到 B，B 的 SKILL.md（含其 references）一次都没提到 A ==")
    names = [d.name for d in sorted(SK.iterdir()) if (d / "SKILL.md").is_file()]
    body = {}
    for n in names:
        t = read(SK / n / "SKILL.md")
        for r in (SK / n).rglob("*.md"):
            if r.name != "SKILL.md" and not any(c in rel(r) for c in CORPUS + NESTED):
                t += "\n" + read(r)
        body[n] = t
    own = {n: read(SK / n / "SKILL.md") for n in names}
    for a in names:
        for b in names:
            if a == b:
                continue
            if re.search(r"(?<![\w-])" + re.escape(b) + r"(?![\w-])", own[a]) and not re.search(
                    r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", body[b]):
                print(f"    {a}  →  {b}   （{b} 里没有任何回指）")


SECTIONS = {"A": sec_A, "B": sec_B, "C": sec_C, "D": sec_D, "E": sec_E, "F": sec_F, "G": sec_G, "H": sec_H,
            "I": sec_I, "J": sec_J, "K": sec_K}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", default=",".join(SECTIONS))
    args = ap.parse_args()
    for s in args.section.split(","):
        SECTIONS[s.strip().upper()]()
        print()
