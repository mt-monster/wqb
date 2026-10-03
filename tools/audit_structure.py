# -*- coding: utf-8 -*-
"""audit_structure.py - 仓库结构守护（2026-09-30 结构审计 P1 新增）

查什么
------
`src/wqb` 已成为可安装包（`pip install -e .`），因此这些约定现在可以被机器
检查了，不再只靠 AGENTS.md 的文字纪律：

- **S1 sys.path 注入冻结**：`src/` 下禁止 `sys.path.insert`（包已可导入）。
  `tools/` 允许存量（脚本靠 `python tools/x.py` 直接跑），但报告增量，
  用于判断是否还在恶化。
- **S2 依赖方向**：`src/` 不得 import `tools`（README 的四层「依赖只允许
  向下」）。反向 tools → src 是设计允许的。
- **S3 同名模块冲突**：`tools/` 与 `src/wqb/` 不应存在同名 .py（import
  解析与静态检查会撞名）。
- **S4 硬编码绝对路径**：`src/` 与 `tools/` 不应出现 `C:\\` / `D:\\` 之类
  本机路径。
- **S5 一次性脚本纪律**：脚本应落在 `tools/`，不应出现在 `reports/`。
- **S6 skills 脚本漂移**：`Claude/skills/` 下按内容去重，报告被 vendoring
  复制多份的脚本。

退出码
------
0 = 全部通过（或仅 WARN）
1 = 有 FAIL，必须修
2 = 工具故障

只读：本工具不改任何文件。S1/S3/S6 的存量问题以 WARN 呈现（清理是独立
任务，不在守护里阻塞日常提交）；新增违规一律 FAIL。
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import io
import re
import sys
import tokenize
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"
TOOLS = REPO_ROOT / "tools"
REPORTS = REPO_ROOT / "reports"
SKILLS = REPO_ROOT / "Claude" / "skills"

#: 扫 Python 文件时跳过的目录名
SKIP_DIRS = {"__pycache__", ".venv", "venv", "node_modules", ".git", "attic",
             "cache", "logs", "research-data", ".pytest_cache"}

#: 硬编码本机盘符路径。注意不能写成 r"[A-Za-z]:[\\/]"——那会把 URL scheme
#: 里的 "s://" 误判成盘符（https://、http:// 全部中招）。要求盘符前不是
#: 单词字符（排除 URL 与命名空间），且斜杠后不是 "/"（排除 scheme）。
ABS_PATH_RE = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/](?!/)")


def py_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return [p for p in root.rglob("*.py")
            if not any(part in SKIP_DIRS for part in p.parts)]


def _strip_comments_and_docstrings(src: str) -> str:
    """去掉 # 注释与 docstring，避免「文档里举的反例」被当成违规。

    用 tokenize 而非正则：docstring 里的盘符路径（本仓存在“`C:\\Users\\x` 是
    错误写法”这类反例说明）不应报违规。tokenize 还能正确处理多行字符串。
    """
    out: list = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
        # 先标记出所有 docstring token 的位置
        doc_positions = _docstring_token_starts(toks)
        for tok in toks:
            if tok.type == tokenize.COMMENT:
                continue
            if tok.type == tokenize.STRING and tok.start in doc_positions:
                # 保留换行，否则行号会偏移
                out.append(tokenize.TokenInfo(
                    tok.type, "\n" * tok.string.count("\n"), tok.start, tok.end, tok.line))
                continue
            out.append(tok)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return src  # 解析不了就回退全文，宁可多报不漏报
    return tokenize.untokenize(out)


def _docstring_token_starts(toks: list) -> set:
    """返回所有模块/类/函数 docstring 的 STRING token 起始位置集合。

    判据：STRING 之前（忽略 NL/NEWLINE/INDENT/DEDENT/COMMENT）没有其他
    有效 token，或之前紧跟的是 def/class/装饰器/赋值开头。
    """
    positions: set = set()
    # 每个逻辑行的首个有效 token
    line_first: dict[int, object] = {}
    for tok in toks:
        if tok.type in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
                        tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING):
            continue
        line_first.setdefault(tok.start[0], tok)
    for tok in toks:
        if tok.type != tokenize.STRING:
            continue
        first = line_first.get(tok.start[0])
        if first is None or first.start == tok.start:
            positions.add(tok.start)
            continue
        # 同一行前面只有 def / class / 装饰器（以 @ 开头）时仍是 docstring
        prefix = " ".join(
            t.string for t in toks
            if t.start[0] == tok.start[0] and t.end[1] <= tok.start[1]
            and t.type not in (tokenize.NL, tokenize.NEWLINE,
                               tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT)
        ).strip()
        if prefix.startswith(("def ", "async def ", "class ", "@")):
            positions.add(tok.start)
    return positions


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []  # (level, check, detail)

    def fail(self, check: str, detail: str) -> None:
        self.rows.append(("FAIL", check, detail))

    def warn(self, check: str, detail: str) -> None:
        self.rows.append(("WARN", check, detail))

    def ok(self, check: str, detail: str) -> None:
        self.rows.append(("OK", check, detail))

    def emit(self) -> int:
        order = {"FAIL": 0, "WARN": 1, "OK": 2}
        for lvl, check, detail in sorted(self.rows, key=lambda r: order[r[0]]):
            print(f"  [{lvl}] {check}: {detail}")
        n_fail = sum(1 for r in self.rows if r[0] == "FAIL")
        n_warn = sum(1 for r in self.rows if r[0] == "WARN")
        print(f"\n[audit_structure] FAIL={n_fail}  WARN={n_warn}")
        return 1 if n_fail else 0


def check_s1_syspath(rep: Report) -> None:
    """sys.path 注入分类。

    关键区分（2026-09-30 审计修正）：`src/wqb` 里的 sys.path 注入分两类，
    语义完全不同，不能一并删：

    - **自举注入**（把 `src/` 自己的父目录挂上去好 `import wqb`）——这类在
      `pip install -e .` 之后纯属多余，应删。
    - **外部挂载**（把 `world-quant-brain-mcp/`、`tools/` 挂上去好 import
      `brain_api` / `sa_probe`）——这两个目录不是 pip 包，**删了直接坏**。
      本仓的 MCP 客户端包刻意不入库安装（见 AGENTS.md 8.2 双 MCP 分工），
      所以这类注入是设计内的一部分，不是技术债。

    因此本检查只盯自举注入：把指向 src/ 自身或其父目录的插入判为 FAIL。
    """
    src_root = SRC.resolve()

    def _is_self_bootstrap(path_str: str) -> bool:
        try:
            p = Path(path_str).resolve()
        except (OSError, ValueError):
            return False
        return p == src_root or p == src_root.parent

    self_bootstrap = []
    external_mounts = 0
    for p in py_files(SRC):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            is_insert = (
                isinstance(f, ast.Attribute)
                and f.attr == "insert"
                and isinstance(f.value, ast.Attribute)
                and f.value.attr == "path"
            )
            if not (is_insert or (isinstance(f, ast.Attribute) and f.attr == "append")):
                continue
            if not node.args:
                continue
            arg = node.args[0]
            txt = None
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                txt = arg.value
            elif isinstance(arg, ast.Name):
                txt = arg.id
            if txt is None:
                continue
            if isinstance(arg, ast.Name):
                # 变量名启发式：含 src / wqb 根的视作自举
                if re.search(r"\b(src|repo_root|wqb_root|project_root)\b", txt, re.I):
                    self_bootstrap.append(
                        f"{p.relative_to(REPO_ROOT).as_posix()}:{node.lineno} ({txt})")
                else:
                    external_mounts += 1
            elif _is_self_bootstrap(txt):
                self_bootstrap.append(
                    f"{p.relative_to(REPO_ROOT).as_posix()}:{node.lineno} ({txt})")
            else:
                external_mounts += 1

    if self_bootstrap:
        for h in self_bootstrap:
            rep.fail("S1 sys.path 自举", f"{h} — 包已可 pip install -e .，请删自举注入")
    else:
        rep.ok("S1 sys.path 自举", "src/ 无自举注入")

    if external_mounts:
        rep.ok("S1 sys.path 外挂",
               f"{external_mounts} 处挂 world-quant-brain-mcp/ 与 tools/ — "
               "设计内行为（非 pip 包），保留")

    tools_hits = sum(
        1 for p in py_files(TOOLS)
        if "sys.path" in _strip_comments_and_docstrings(
            p.read_text(encoding="utf-8", errors="replace")
        )
    )
    rep.warn("S1 sys.path@tools",
             f"{tools_hits} 处存量（脚本直跑需要，属已知技术债，不阻塞）")


def check_s2_dep_direction(rep: Report) -> None:
    """src/ 不得 import tools。"""
    bad = []
    for p in py_files(SRC):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            mods: list[str] = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                mods = [node.module]
            for m in mods:
                if m == "tools" or m.startswith("tools."):
                    bad.append(f"{p.relative_to(REPO_ROOT).as_posix()}: import {m}")
    if bad:
        for b in bad:
            rep.fail("S2 依赖方向", f"{b} — 违反「依赖只允许向下」")
    else:
        rep.ok("S2 依赖方向", "src/ 未引用 tools/")


def check_s3_name_collision(rep: Report) -> None:
    """tools/ 与 src/wqb/ 的文件名重叠（2026-09-30 审计修正：不是缺陷）。

    原设计把「同层同名」判为 import 冲突，**判错了**。实测 7 组重叠
    （wave_gate / submit_queue / waiver / forum_recon / forum_recon_wave /
    alpha_properties / dataset_experience）分属两套互不重叠的命名空间：

    - `tools/*.py` 是**脚本**，靠 `python tools/x.py` 直跑；它 import 包时
      写的是 `from wqb.store import …`（绝对包路径）。
    - `src/wqb/**.py` 是**包内模块**，只能以 `wqb.workflow.nodes.wave_gate`
      这种带包前缀的形式到达。

    证据：`import wave_gate` 报 ModuleNotFoundError（它不存在于顶层），
    `wave_gate.py` 只作为 `wqb.workflow.nodes.wave_gate` 存在。两边不进入
    同一 sys.path 解析优先级竞争，改名只会波及 90+ 处引用而收益为零。

    因此本检查改为**只报告、不判 FAIL**，供人判断是否为有意命名。
    真正会撞名的是同一目录内的重复（如两个 tools/x.py），那不可能存在。
    """
    src_names = {p.name for p in py_files(SRC) if p.name != "__init__.py"}
    collide = sorted(
        p.name for p in py_files(TOOLS)
        if p.name in src_names and p.name != "__init__.py"
    )
    if collide:
        rep.ok("S3 跨层同名",
               f"{len(collide)} 个文件名在 tools/ 与 src/wqb/ 重叠"
               f"（{', '.join(collide)}）——分属脚本与包两套命名空间，"
               "import 不会撞，非缺陷，勿改名")
    else:
        rep.ok("S3 跨层同名", "无重叠")


def check_s4_abs_path(rep: Report) -> None:
    """硬编码本机盘符。

    排除 tools/legacy/（已归档的历史代码，不再维护）与本工具自身
    （它的 docstring 就要举盘符路径作反例）。
    """
    hits = []
    targets = list(py_files(SRC))
    targets += [p for p in py_files(TOOLS)
                if "legacy" not in p.parts and p.resolve() != Path(__file__).resolve()]
    for p in targets:
        txt = _strip_comments_and_docstrings(p.read_text(encoding="utf-8", errors="replace"))
        for i, line in enumerate(txt.splitlines(), 1):
            if ABS_PATH_RE.search(line):
                hits.append(f"{p.relative_to(REPO_ROOT).as_posix()}:{i}")
    if hits:
        for h in hits:
            rep.fail("S4 硬编码路径", f"{h} — 换成本机盘符，不可移植")
    else:
        rep.ok("S4 硬编码路径", "无本机绝对路径（已排除 tools/legacy/ 归档区）")


#: reports/ 下的豁免前缀（2026-09-30）。这些 .py 不是散落垃圾，而是审计结论的
#: **可重跑证据**——与同目录的审计报告 md/json 配对，拆开会让报告里的
#: 「可复现：python reports/xxx.py」指引失效。用 `git grep -w` 核过 refs ≥ 1。
#: 详见 tools/legacy/README.md 的「明确不归档的」表。
S5_EXEMPT_PREFIXES = (
    "reports/ra_pipeline_stage_review_20260927/",
    "reports/skills_review_20260929/",
    "reports/forum_alpha_research/",
    # 文件级：这两份有审查报告写明「可复现：python reports/xxx.py」
    "reports/skills_pipeline_stage_review_20260927",
    "reports/skills_stage_review_v2_20260927",
    "reports/dryrun_chain_runner_20260927",
    "reports/dryrun_chain_runner_v2_20260927",
)


def check_s5_report_scripts(rep: Report) -> None:
    """reports/ 下不该有 .py（产物目录，不是代码目录）。

    豁免 S5_EXEMPT_PREFIXES：审计证据脚本与报告配对，不是违规。
    """
    hits = []
    for p in py_files(REPORTS):
        rel = p.relative_to(REPO_ROOT).as_posix()
        if any(rel.startswith(pfx) for pfx in S5_EXEMPT_PREFIXES):
            continue
        hits.append(rel)
    if hits:
        for h in hits:
            rep.warn("S5 reports/脚本", f"{h} — 应迁到 tools/（AGENTS.md §6 一次性脚本纪律）")
    else:
        rep.ok("S5 reports/脚本", "reports/ 纯产物（审计证据前缀已豁免）")


def check_s6_skill_drift(rep: Report) -> None:
    """skills 副本漂移 —— 委托给专用工具。

    2026-09-30 审计修正：本检查原用裸 md5 分组，把 GEM 内嵌快照（A 类，设计内
    保留）与真跨 skill 复制（B 类，待治理）混在一起报 7 组噪声。分类逻辑已挪到
    `tools/audit_skill_drift.py`，此处只转调，避免两个工具对同一件事各说一套。

    2026-10-03 升级为 **FAIL + 基线棘轮**：B 类（跨 skill 复制）此前是 WARN，
    而 pre-commit 只拦 FAIL → 存量 3 组永远不红，"改一处漏三处"可无声复发
    （历史上 `validator.py` 三份各自演化、缺 hump/bucket/densify 修复就是这么
    发生的）。实测现状：4 份 `validator.py` 哈希全同（**尚未分叉**），
    正是升 FAIL 的最佳时机——此刻登记基线不产生任何存量债。

    棘轮语义（与 `skill_lint.py` 的 baseline 模式一致）：
      - 基线内的已知存量组 → WARN（可见但不阻塞）
      - **基线外的新增组 → FAIL**（阻断提交）
      - 同名但哈希变了 = 有人改过其中一份且未同步其余 → 按新增处理（最危险）
      - 修掉一组后应收窄基线，否则它将来重新出现会被误判为"新增"
    """
    import json
    import subprocess

    script = REPO_ROOT / "tools" / "audit_skill_drift.py"
    if not script.exists():
        rep.warn("S6 skills 漂移", "audit_skill_drift.py 缺失，跳过")
        return

    r = subprocess.run([sys.executable, str(script), "--json"],
                       capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode not in (0, 1):
        rep.warn("S6 skills 漂移",
                 f"audit_skill_drift.py 异常退出（rc={r.returncode}），跳过")
        return
    try:
        payload = json.loads(r.stdout)
        cross = payload.get("cross_skill") or []
        diverged = payload.get("diverged") or []
    except (json.JSONDecodeError, KeyError, TypeError):
        rep.warn("S6 skills 漂移", "audit_skill_drift.py 输出不可解析，跳过")
        return

    # ★ 分叉副本 = 同名脚本在不同 skill 下内容已不同 = "改一处漏三处"已经发生。
    #   这正是本检查存在的意义，故**无条件 FAIL、不进基线**（基线只豁免"仍然
    #   相同"的存量副本；分叉不存在"合法存量"形态）。
    for e in diverged:
        rep.fail("S6 skills 漂移",
                 f"★ {e['name']} 已分叉：{e['copies']} 份 / {e['variants']} 种内容"
                 f"（{', '.join(e['skills'])}）——改一处漏三处已发生，"
                 f"必须四处一致；分叉明细 {e.get('per_skill_hash')}")

    baseline = _s6_baseline()
    baseline_names = {b.split("@")[0] for b in baseline}
    seen, new_groups = set(), []
    for e in cross:
        key = f"{e['name']}@{e['hash']}"
        seen.add(key)
        if key in baseline:
            continue
        why = ("同名脚本哈希已变（改动未同步到全部副本）"
               if e["name"] in baseline_names else "新增跨 skill 复制")
        new_groups.append((e, why))

    for e, why in new_groups:
        rep.fail("S6 skills 漂移",
                 f"{e['name']} ({len(e['paths'])} 份: {', '.join(e['skills'])}) — {why}；"
                 f"多处副本需一起覆盖，详见 `python tools/audit_skill_drift.py`")

    fixed = [b for b in baseline if b not in seen]
    if fixed:
        rep.warn("S6 skills 漂移",
                 f"基线中的 {len(fixed)} 组已消失，可从 "
                 f"tools/audit_structure_baseline.json 移出：{fixed}")

    known = [e for e in cross if f"{e['name']}@{e['hash']}" in baseline]
    if new_groups:
        pass  # 已由 FAIL 行呈现，不再刷 WARN 噪声
    elif known:
        rep.warn("S6 skills 漂移",
                 f"{len(known)} 组已知跨 skill 复制（已登记基线，待治理）："
                 + ", ".join(sorted(e["name"] for e in known)))
    elif not cross:
        rep.ok("S6 skills 漂移", "无跨 skill 复制")


def _s6_baseline() -> set:
    """读取 S6 基线（已登记的存量 B 类组，键 = `文件名@哈希前12位`）。

    文件缺失 → 空基线（此时任何 B 类都算新增 → FAIL），这是保守方向。
    """
    import json

    p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
    if not p.is_file():
        return set()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return set(data.get("s6_skill_drift") or [])
    except (json.JSONDecodeError, OSError):
        return set()


CHECKS = {
    "s1": ("S1 sys.path 注入", check_s1_syspath),
    "s2": ("S2 依赖方向", check_s2_dep_direction),
    "s3": ("S3 同名模块", check_s3_name_collision),
    "s4": ("S4 硬编码路径", check_s4_abs_path),
    "s5": ("S5 reports/脚本", check_s5_report_scripts),
    "s6": ("S6 skills 漂移", check_s6_skill_drift),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="仓库结构守护（只读）")
    ap.add_argument("--only", choices=sorted(CHECKS), action="append",
                    help="只跑指定检查（可重复）")
    args = ap.parse_args(argv)

    selected = args.only or sorted(CHECKS)
    rep = Report()
    for key in selected:
        _name, fn = CHECKS[key]
        try:
            fn(rep)
        except Exception as e:  # 单个检查炸了不该拖垮整轮
            rep.warn(key.upper(), f"检查自身故障（跳过）: {e}")
    return rep.emit()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)
