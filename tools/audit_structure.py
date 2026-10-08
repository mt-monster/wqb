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
- **S7 根目录白名单**：仓库根只允许入口 / 配置 / 三份文档 / 会话草稿。
  新增顶层 `.py`/`.log`/无扩展名件一律 FAIL（根目录污染在本仓已复发 5 次，
  靠 `.gitignore` 逐条追赶不能治本）。
- **S8 根↔子目录同名分叉**：仓库根的 `.py` 与子目录同名 `.py` 内容不一致 → FAIL。
  2026-10-04 实事故：论坛工作台脚本在根与 `tools/forum_workbench/` 各存一份且
  **互为超集**（根版有测试中心内嵌、tools 版有 `prune_old_files` 与仓库根上溯修正），
  两侧各自演化无人发现，每晚自动化连日失败。**分叉没有「合法存量」形态，不进基线**。
- **S9 声明目录存在性**：AGENTS.md §1 职责表与 `docs/README.md` 目录树里声明的目录
  必须磁盘存在。FAIL —— 「文档写了但目录不存在」会直接误导下一个动手的 Agent。
- **S10 区域子目录完整性**：`tracking/<REGION>/` 缺五个核心子目录 → FAIL（2026-10-04 P2-3
  已把 13 区补齐，不再容忍差异）；存在非占位空子目录 → WARN。
- **S11 tools/ 顶层冻结**：`tools/*.py` 与基线比对，**只减不增**。新增顶层脚本 = FAIL，
  必须落 `tools/THEMES.json` 里的主题子目录。背景：顶层平铺 171 个，一次性下沉不安全
  （全仓 80 处 `sys.path.insert(...'tools')`、多处把 tools 脚本当模块 import、仓库根推导
  层数硬编码共 5 种写法），故先止血、再按主题逐批迁移。
- **S12 已下架路径不得复活**：基线 `retired_paths` 里的路径若重新出现在工作区 → FAIL。
  2026-10-04 实测：论坛工作台（缺 UI 模板、每晚自动化因它连日失败）整端归档后，
  **同一会话内又被恢复**——靠搬文件完不成下架，必须机械记账。
- **S13 tracking/ 非区域目录登记**：13 个区域码之外的目录（`reference/`、`mining/`、
  `FORUM`、`PPA_USA`、`prod_probe`、`hypotheses`、`_scratch`）必须显式登记在
  `NON_REGION_DIRS`，未登记 → FAIL；登记了但磁盘已无 → WARN（可清理，不阻塞）。
  背景：S10 靠 `^[A-Z]{3}$` 识别区域，`FORUM`（5 字母）**恰好不匹配**才没被当成
  区域——隐式约定无法自动执行；AGENTS.md §8.13 已把「新 Agent 极易当成区域读」
  列为风险，但约定不会自动执行。**本检查只登记不搬**：`reference/` 有 88 处引用、
  `mining/` 有 46 处引用且 AGENTS.md §1 明令勿动，物理搬迁风险远大于收益。
- **S14 tools/README 登记**：`tools/` 下的**受控**脚本必须在 `tools/README.md` 占一行
  （2026-10-06 治理评审 P2-8 新增）。**棘轮**：存量欠债登记在基线 `s14_unregistered_tools`
  → WARN，**新增未登记 → FAIL**。背景：AGENTS.md §8.13「并在 tools/README.md 登记一行」
  长期纯靠自觉（S7/S8/S9/S11 都看不上这件事），实测顶层 159 个里 8 个从未登记。
- **S15 skills 副本同步**：`.claude/skills/`（Agent 宿主读取的副本）必须与源
  `Claude/skills/` 逐文件一致。2026-10-06 第二轮治理复核 P1-3 新增。背景：该副本被
  `.gitignore` 整目录排除，**既不入库也无人比对**，改了源不同步时宿主会静默读旧版。
  加闸当日实测基线 0 差异（`diff -rq` 全绿），属"基线干净时加闸最便宜"。

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
import subprocess
import sys
import tokenize
from collections import defaultdict
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO_ROOT = find_repo_root(__file__)
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
        # 2026-10-04 修 Bug B：空串不得参与判定。
        # `Path("").resolve()` 返回 **CWD**，而测试/审计通常在仓库根运行
        # ⇒ 空串会被解析成仓库根，恰好等于 `src_root.parent`，从而被误判为
        # 「自举注入」。实测 `L.append("")`（纯文本拼接的常见写法）正是这样
        # 在 src/wqb/profiles/render.py 造成 14 处误报，长期阻塞 pre-commit。
        # 空串的语义不是路径，直接排除。
        if not path_str or not path_str.strip():
            return False
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
            # 2026-10-04 修 Bug A：接收者必须是 `sys.path`（或其别名）。
            # 原实现对 insert 只验 `f.value.attr == "path"`、对 append **完全不验接收者**
            # ⇒ 任何 `X.append(...)`（如 Markdown 文本拼装常见的 `L.append("")`）
            # 都会进入自举判定。实测 render.py 有 89 处 `L.append(...)` 命中。
            #
            # 接收者判据用「名字像 sys」而非硬编码 `id == "sys"`：本仓真实代码存在
            # `import sys as _sys` 后写 `_sys.path.insert(...)` 的写法
            # （见 workflow/nodes/{auto_review,campaign}.py），硬判 sys 会漏掉它们。
            if not (
                isinstance(f, ast.Attribute)
                and f.attr in ("insert", "append")
                and isinstance(f.value, ast.Attribute)
                and f.value.attr == "path"
                and isinstance(f.value.value, ast.Name)
                and f.value.value.id.lstrip("_") == "sys"
            ):
                continue
            if not node.args:
                continue
            # ★ 2026-10-04 修 Bug C：按方法语义取「被插入的值」。
            # `sys.path.insert(0, PATH)` 的路径在 **args[1]**（第一个参数是插入
            # 索引），`sys.path.append(PATH)` 才在 args[0]。原实现一律取 args[0]，
            # 于是 insert 形态永远拿到常量 0 —— 路径字面量自举**从未被检出过**
            # （此前没有真实自举样本，故该 bug 一直潜伏）。
            value_idx = 0 if f.attr == "append" else 1
            if len(node.args) <= value_idx:
                continue
            arg = node.args[value_idx]
            # 参数常被包在 str()/Path() 里（str(REPO_ROOT)），剥掉这层壳再判，
            # 否则真实自举（如 sys.path.insert(0, str(REPO_ROOT))）会漏检。
            probe = arg
            for _ in range(2):
                if (isinstance(probe, ast.Call)
                        and isinstance(probe.func, ast.Name)
                        and probe.func.id in ("str", "Path", "PurePath")
                        and probe.args):
                    probe = probe.args[0]
            txt = None
            if isinstance(probe, ast.Constant) and isinstance(probe.value, str):
                txt = probe.value
            elif isinstance(probe, ast.Name):
                txt = probe.id
            if txt is None:
                continue
            if isinstance(probe, ast.Name):
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
        # 2026-10-06 治理评审：原先这里是 warn（跳过）。但本闸 2026-10-03 已升为 FAIL，
        # 而 pre-commit 只拦 FAIL ⇒ 「被委托脚本不见了」这个**最可能**的故障模式会让 S6
        # 静默消失（历史上 `audit_skill_drift.py` 这类文件确实被清理过）。工具自身不可用
        # 必须响亮失败，不能把已登记的闸装成自毁开关。
        rep.fail("S6 skills 漂移",
                 "audit_skill_drift.py 缺失 —— S6 无法执行，按结构性 FAIL 处理："
                 "请从 attic/ 或抢救点取回该文件，不要留空转")
        return

    r = subprocess.run([sys.executable, str(script), "--json"],
                       capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode not in (0, 1):
        # 0/1 是「跑通了，只是有无违规」；其余 = 工具自身坏了（缺依赖 / 崩了）。
        rep.fail("S6 skills 漂移",
                 f"audit_skill_drift.py 异常退出（rc={r.returncode}）—— 工具故障不等于无违规，"
                 f"按 FAIL 处理。stderr 前 200 字：{(r.stderr or '').strip()[:200]}")
        return
    try:
        payload = json.loads(r.stdout)
        cross = payload.get("cross_skill") or []
        diverged = payload.get("diverged") or []
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        rep.fail("S6 skills 漂移",
                 f"audit_skill_drift.py 输出不可解析（{e}）—— 按 FAIL 处理，"
                 f"stdout 前 200 字：{(r.stdout or '').strip()[:200]}")
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


def _sha12(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


#: S7：仓库根允许的文件名（入口 / 配置 / 三份文档 / 会话草稿）。
#: 要新增请先回到 AGENTS.md §8.13 确认归属目录，再决定要不要往这里加一行。
ROOT_ALLOWLIST = {
    # 入口与工具链配置（约定必须住根：MCP 客户端直接指到这里）
    ".mcp.json", "mcp_config.json", "pyproject.toml", "pytest.ini",
    "requirements.txt", "conftest.py", "wqb_db_mcp.py",
    # VCS
    ".gitignore", ".gitattributes", ".mailmap",
    # 文档三件套（定位分工见 AGENTS.md §8.4 第 3 条）
    "AGENTS.md", "CLAUDE.md", "README.md",
    # 会话草稿（planning-with-files 三件套，已 gitignore，不入仓库）
    "findings.md", "progress.md", "task_plan.md",
}

#: S7 里当目录跳过的顶层目录名（目录归属由 S9/S10 管）
ROOT_SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache"}


def check_s7_root_allowlist(rep: Report) -> None:
    """S7：仓库根不允许未知散件。

    只扫顶层文件：目录交给 S9（声明存在性）与 S10（区域子目录）。
    """
    offenders = []
    for p in sorted(REPO_ROOT.iterdir()):
        if p.is_dir() or p.name in ROOT_SKIP_DIRS:
            continue
        if p.name in ROOT_ALLOWLIST:
            continue
        offenders.append(p.name)
    if offenders:
        rep.fail(
            "S7 根目录白名单",
            f"{len(offenders)} 个根级散件不在白名单：{offenders}；"
            "归属判据：脚本→`tools/`，报告→`output_report/`，运行产物→`logs/` 或 `cache/`，"
            "外部数据→`research-data/`，归档→`attic/<主题>_<YYYYMMDD>/`",
        )
    else:
        rep.ok("S7 根目录白名单", "仓库根无额外散件")


#: S8 只拿这些子树比对（全仓 rglob 会顺扫 tracking 上万个数据文件，没信号且慢）
S8_SCOPE = (TOOLS, SRC, REPO_ROOT / "world-quant-brain-mcp", SKILLS,
            REPO_ROOT / "tests", REPO_ROOT / "tracking")


def check_s8_root_subdir_divergence(rep: Report) -> None:
    """S8：仓库根 `.py` 与子目录同名 `.py` 分叉。

    只管「根 ↔ 子目录」这一形态（论坛工作台事故的形状：根上又多出一份同名脚本）。
    子目录之间的同名问题已由 S3（tools vs src）与 S6（skills 副本）覆盖，不在此重报。
    内容一致→WARN（重复文件）；内容不一致→FAIL（分叉）。FAIL 不进基线豁免。
    """
    root_pys = [p for p in sorted(REPO_ROOT.glob("*.py")) if p.name != "conftest.py"]
    if not root_pys:
        rep.ok("S8 根↔子目录分叉", "仓库根无 .py")
        return
    index: dict[str, list[Path]] = defaultdict(list)
    for scope in S8_SCOPE:
        for p in py_files(scope):
            if p.parent != REPO_ROOT:
                index[p.name].append(p)
    diverged: list[str] = []
    identical: list[str] = []
    for rp in root_pys:
        for sub in index.get(rp.name, []):
            rel = sub.relative_to(REPO_ROOT).as_posix()
            try:
                if _sha12(sub) == _sha12(rp):
                    identical.append(f"{rp.name} == {rel}")
                else:
                    diverged.append(f"{rp.name} ≠ {rel}")
            except OSError as e:  # 读不了不等于分叉，诚实报出
                rep.warn("S8 根↔子目录分叉", f"{rp.name} vs {rel} 读取失败：{e}")
    if diverged:
        rep.fail("S8 根↔子目录分叉",
                 f"同名且内容不一致（互为超集，放着不管就继续漂）：{'；'.join(diverged)}")
    if identical:
        rep.warn("S8 根↔子目录分叉",
                 f"同名逐字节副本（建议只留一份）：{'；'.join(identical)}")
    if not diverged and not identical:
        rep.ok("S8 根↔子目录分叉", "根 .py 与子目录无同名冲突")


#: S9：从文档里抽出的目录形状（带通配/占位的一律跳过，不硬判）
_BACKTICK_DIR_RE = re.compile(r"`([A-Za-z0-9_.\-/]+/)`")
_DOCS_TREE_DIR_RE = re.compile(r"^[\u2502\u251c\u2514\u2500\s]*[\u251c\u2514]\u2500+\s+([A-Za-z0-9_.\-/]+)/")


def _looks_like_glob(tok: str) -> bool:
    return any(c in tok for c in ("*", "<", "\u2026", " "))


def check_s9_declared_dirs_exist(rep: Report) -> None:
    """S9：文档声明的目录必须真实存在。

    两个声明源：
    1. AGENTS.md §1「项目概述与模块职责」表的反引号目录 token；
    2. docs/README.md 的目录树（相对 docs/ 的子节点）。
    带 `*` / `<REGION>` / `…` 的占位写法跳过（不是可解引用的具体路径）。
    """
    missing: list[str] = []

    agents = REPO_ROOT / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8", errors="replace")
        sec = re.search(r"^## 1\..*?(?=^## 2\.)", text, re.S | re.M)
        body = sec.group(0) if sec else ""
        for tok in set(_BACKTICK_DIR_RE.findall(body)):
            if _looks_like_glob(tok):
                continue
            if not (REPO_ROOT / tok).is_dir():
                missing.append(f"AGENTS.md \u00a71: {tok}")
    else:
        rep.warn("S9 声明目录存在", "AGENTS.md 不存在，本轮未校 §1")

    docs_idx = REPO_ROOT / "docs" / "README.md"
    if docs_idx.is_file():
        for line in docs_idx.read_text(encoding="utf-8", errors="replace").splitlines():
            m = _DOCS_TREE_DIR_RE.match(line)
            if not m:
                continue
            tok = m.group(1)
            if _looks_like_glob(tok) or tok == "docs":
                continue
            if not (REPO_ROOT / "docs" / tok).is_dir():
                missing.append(f"docs/README.md 目录树: docs/{tok}/")

    if missing:
        rep.fail("S9 声明目录存在",
                 f"文档声明但磁盘不存在：{'；'.join(sorted(missing))}"
                 "（要么把目录建出来，要么删掉这一行——留着就是误导）")
    else:
        rep.ok("S9 声明目录存在", "AGENTS.md \u00a71 与 docs/README.md 声明的目录均存在")


#: S10：每个区域应有的核心子目录（2026-10-04 按 14 区实测最大公约数定）
REGION_CORE_DIRS = {"config", "candidates", "results", "priors", "reference"}
#: 区域目录统一结构（五个核心子目录）——2026-10-04 P2-3 已把 13 区补齐到这一套。
#: 差异已消除，故缺目录从 WARN 升级为 FAIL；仅含 .gitkeep 的空目录不算空壳。
REGION_NAME_RE = re.compile(r"^[A-Z]{3}$")   # 只认三字母区域码；FORUM/PPA_USA/mining 等不当区域算


def _dir_is_skeleton_placeholder(d: Path) -> bool:
    """只含 .gitkeep 的目录 = 有意保留的区域结构占位，不算空壳。

    `tracking/.gitignore` 把 `results/`、`**/candidates/` 整体排除，所以这些占位
    只存在于本机磁盘（不可入库）——S10 本身就是磁盘级检查，因此认它。
    """
    try:
        names = {p.name for p in d.iterdir()}
    except OSError:
        return False
    return names and names <= {".gitkeep"}


def check_s10_region_skeleton(rep: Report) -> None:
    """S10：`tracking/<REGION>/` 五个核心子目录齐全（缺 = FAIL），空壳目录 = WARN。

    2026-10-04 P2-3 已把 13 个区域补齐到同一套结构，因此不再容忍差异：
    缺核心子目录直接 FAIL（新区域建齐五个目录即可，占位用 `.gitkeep`）。
    区域名靠 `^[A-Z]{3}$` 识别，因此 `FORUM`/`PPA_USA`/`prod_probe`/`_scratch`
    这类非区域目录不会被当成区域报（它们的归位约定见 AGENTS.md §8.13）。
    """
    tracking = REPO_ROOT / "tracking"
    if not tracking.is_dir():
        rep.ok("S10 区域子目录", "无 tracking/，跳过")
        return
    regions = [d for d in sorted(tracking.iterdir())
               if d.is_dir() and REGION_NAME_RE.match(d.name)]
    incomplete: list[str] = []
    empties: list[str] = []
    for r in regions:
        subs = [d for d in r.iterdir() if d.is_dir()]
        names = {d.name for d in subs}
        miss = REGION_CORE_DIRS - names
        if miss:
            incomplete.append(f"{r.name}:\u7f3a{sorted(miss)}")
        for d in subs:
            if not any(d.iterdir()):
                empties.append(f"{r.name}/{d.name}/")
            elif _dir_is_skeleton_placeholder(d):
                continue          # 有意占位，不报
    if incomplete:
        rep.fail("S10 区域子目录",
                 f"{len(incomplete)}/{len(regions)} 个区域缺核心子目录：{'；'.join(incomplete)}"
                 "（P2-3 已将 13 区统一为 config/candidates/results/priors/reference；"
                 "新建区域按这套补全即可）")
    if empties:
        rep.warn("S10 区域子目录",
                 f"空子目录（非 .gitkeep 占位）：{'；'.join(sorted(empties))}")
    if not incomplete and not empties:
        rep.ok("S10 区域子目录", f"{len(regions)} 个区域五个核心子目录齐整")


def _s11_baseline() -> set:
    """S11 存量基线：tools/ 顶层允许存在的 .py 文件名集合。

    文件缺失 = 基线过时（提示移出）；新增 = FAIL。基线文件缺失 = 空集→顶层任何脚本都算新增。
    """
    import json

    p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
    if not p.is_file():
        return set()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return set(data.get("s11_tools_top_level") or [])
    except (json.JSONDecodeError, OSError):
        return set()


def _themes_assigned() -> set:
    """`tools/THEMES.json` 里已归属的**顶层脚本名**集合（含已下沉的 moved_files）。

    读不到文件 / 解析失败 = 空集 —— 宁可把现有顶层脚本全判为「未归属」，
    也不要因为登记表本身坏掉而让 S11 静默不生效（2026-10-06 治理评审的 fail-open 主题）。
    """
    import json

    p = REPO_ROOT / "tools" / "THEMES.json"
    if not p.is_file():
        return set()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()
    names: set = set()
    for th in (data.get("themes") or {}).values():
        names |= {Path(f).name for f in (th.get("files") or [])}
        names |= {Path(f).name for f in (th.get("moved_files") or [])}
    return names


def check_s11_tools_top_frozen(rep: Report) -> None:
    """S11：tools/ 顶层只减不增（2026-10-04 P2-1）+ 可度量去冻结（2026-10-06）。

    背景：tools/ 顶层平铺 171 个脚本，而 tools/README.md 早已写好 14 个主题分类（磁盘上
    却没分）。一次性下沉并不安全：实测全仓 80 处 `sys.path.insert(... 'tools')`，
    `index_tables` / `migrate_wave_verdict_enum` 等还被当模块 import，且仓库根推导写法
    同主题内就有 5 种（层数硬编码）。目标结构与逐文件归属已写进 `tools/THEMES.json`，
    迁移按主题分批走；在那之前先把顶层**冻住**，避免上帝目录继续长。

    2026-10-06 治理评审补的两条（原缺）：
      1. `ac2cf35` 号称「10 个 CLI 下沉」实测是在子目录**新建**（10 条 create mode、
         0 条 rename/delete，顶层数 159→159）——「下沉」这个表述让迁移进度看起来推进了
         10 步而实际顶层规模未变。故这里把**读数**摆到台面上：顶层现数 / 基线 / 已下沉数。
      2. 「冻结」只防新增，不防「永不迁移」。新增必须同时在 THEMES.json 登记归属，
         存量也必须逐条有归属 —— 未归属数就是可度量的迁移债，不得靠默认塞进已有目录。
    """
    now = {p.name for p in TOOLS.glob("*.py")}
    baseline = _s11_baseline()
    if not baseline:
        rep.warn("S11 tools 顶层冻结",
                 "基线为空或未登记 s11_tools_top_level —— 未生效，先跑 "
                 "`python tools/audit_structure.py --freeze-tools-top` 写入存量清单")
        return
    added = sorted(now - baseline)
    gone = sorted(baseline - now)
    if added:
        rep.fail("S11 tools 顶层冻结",
                 f"tools/ 顶层新增 {len(added)} 个脚本：{added}；新 CLI 必须落在主题子目录"
                 "（归属查 tools/THEMES.json 的 themes，目录名 kebab-case），并在 "
                 "tools/README.md 登记；不得继续往顶层堆")
    if gone:
        rep.warn("S11 tools 顶层冻结",
                 f"{len(gone)} 个已不在顶层（迁移成功或已删），请同步从 "
                 f"tools/audit_structure_baseline.json 移出：{gone}")

    # 归属棘轮：磁盘上的顶层脚本必须在 THEMES.json 里有主题归属（2026-10-06 实测已 0 条欠债）
    unassigned = sorted(now - _themes_assigned())
    if unassigned:
        rep.fail("S11 tools 顶层冻结",
                 f"{len(unassigned)} 个顶层脚本在 tools/THEMES.json 里**无主题归属**：{unassigned}；"
                 "要么给它加 themes.<主题>.files 条目，要么迁进 tracking/<REGION>/scripts/ "
                 "或归档 —— 不允许默认塞进已有目录（THEMES.json._source 明文禁止）")

    moved = len(baseline) - len(now & baseline)
    if not added and not gone and not unassigned:
        rep.ok("S11 tools 顶层冻结",
               f"顶层 {len(now)} 个与基线一致（只减不增；基线 {len(baseline)}、"
               f"已下沉 {moved} 个、未归属 0 个）")


def _s14_baseline() -> set:
    """S14 存量基线：允许「未在 tools/README.md 登记」的脚本名集合（只减不增）。"""
    import json

    p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
    if not p.is_file():
        return set()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return set(data.get("s14_unregistered_tools") or [])
    except (json.JSONDecodeError, OSError):
        return set()


def _tools_tracked_scripts(recursive: bool = False) -> list:
    """`tools/` 下的**受控**脚本（相对 `tools/` 的 posix 路径）。

    只看 git 跟踪的：并行会话的在途未跟踪文件不该拦住本次提交（AGENTS.md §7）。
    缺省只看**顶层**：AGENTS.md §8.13 的登记义务针对「可复用 CLI」，
    子目录里的包实现模块（`wave_gate_pkg/gates_semantic.py`、`_lib/prescreen.py`）
    不是 CLI，逼它们逐个登记只会逼出无意义的表格灌水。

    ⚠ 不能拿 `tools/*.py` 当 pathspec：git 缺省把 `*` 当跨 `/` 匹配（无 FNM_PATHNAME），
    实测它会连着吐 `legacy/opswap_driver.py` 这类子目录件——目录过滤必须在 Python 侧做。
    """
    r = subprocess.run(["git", "ls-files", "-z", "--", "tools/*.py"],
                       capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        # 拿不到清单就报错：静默给空集 = S14 看似在跑实则永不过（fail-open）。
        raise RuntimeError(f"git ls-files 失败（rc={r.returncode}）：{r.stderr.strip()[:200]}")
    out = []
    for x in filter(None, r.stdout.split("\0")):
        rel = Path(x).relative_to(Path("tools")).as_posix()
        if not recursive and "/" in rel:
            continue
        out.append(rel)
    return sorted(out)


def _looks_like_cli(rel: str) -> bool:
    """是否为对用户跑的 CLI：有 argparse，或带 `if __name__ == "__main__"` 守卫。

    读不了文件（编码/权限）时**当它是 CLI**（保守：宁可多要求登记，不要把真 CLI 漏成
    「免登记」—— 那正是本检查要防的「靠猜」）。
    """
    p = TOOLS / rel
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return True
    return "argparse" in text or '__name__ == "__main__"' in text or "__name__ == '__main__'" in text


def _readme_mentions() -> set:
    """`tools/README.md` 里提到过的脚本路径（归一为相对 `tools/` 的 posix）。

    README 里同时存在三种写法：`code-audit/repo_governance_check.py`（下沉后）、
    `tools/sync_skills.py`（带顶层前缀）、`wave_gate.py`（裸名，存量写法）。
    只比裸名会把 `legacy/gate.py` 与 `gate.py` 当成同一个，故**保留目录段**归一。
    """
    p = TOOLS / "README.md"
    if not p.is_file():
        return set()
    text = p.read_text(encoding="utf-8", errors="replace")
    toks = set(re.findall(r"[A-Za-z0-9_\-./]+\.(?:py|sh|ps1)\b", text))
    norm = set()
    for t in toks:
        t = t.strip("./")
        if t.startswith("tools/"):
            t = t[len("tools/"):]
        norm.add(t)
    return norm


def check_s14_tools_readme_registry(rep: Report) -> None:
    """S14：`tools/` 顶层的 **CLI** 必须在 `tools/README.md` 登记（棘轮：未登记数只减不增）。

    为什么单独立一条（2026-10-06 治理评审）：AGENTS.md §8.13 写「可复用 CLI → `tools/`
    并在 tools/README.md 登记一行」，但 S7/S8/S9/S11 都不看这件事，登记纯靠自觉 ——
    实测顶层 159 个里有 8 个从未登记，而其中 `fetch_all_universes.py` 正是 HEAD 唯一
    动过的生产脚本（改了却没补登记）。本检查把「登记」从文字纪律变成读数。

    范围口径：只盯**顶层 + 像 CLI 的**（有 argparse 或 `__main__` 守卫）。
    子目录里的包实现模块（`wave_gate_pkg/gates_*.py`、`_lib/*.py`）不是 CLI，不逼登记；
    否则只会灌水表格、把真正的缺口淹没。

    棘轮语义：存量欠债登记在基线 `s14_unregistered_tools`（WARN 可见不阻塞），
    新增未登记 → FAIL。补登记后应从基线移出（收紧）。
    """
    if not (TOOLS / "README.md").is_file():
        rep.fail("S14 tools/README 登记", "tools/README.md 不存在 —— 登记面消失，按 FAIL 处理")
        return
    try:
        tracked = _tools_tracked_scripts()
    except RuntimeError as e:
        rep.fail("S14 tools/README 登记", f"无法取受控清单（{e}）—— 不当作「全部已登记」放过")
        return
    tracked = [n for n in tracked if _looks_like_cli(n)]
    mentioned = _readme_mentions()
    # 受控但磁盘已无的件 = **删除事件**，不是「新脚本没登记」（那是 S11/git status 的事）。
    # 不先筛存在性会得到假阳性：实测 2026-10-06 有会话从工作树删了 26 个顶层脚本，
    # 而 `_looks_like_cli()` 对读不到文件的默认保守（当它是 CLI）⇒ 6 个根本没 argparse
    # 的一次性脚本被报成「新增未登记」，把 S14 顶红并混淆两类问题。
    missing = [n for n in tracked if not (TOOLS / n).is_file()]
    tracked = [n for n in tracked if (TOOLS / n).is_file()]
    unreg = sorted(n for n in tracked if n not in mentioned)
    baseline = _s14_baseline()
    new_ones = [n for n in unreg if n not in baseline]
    if new_ones:
        rep.fail("S14 tools/README 登记",
                 f"新增 {len(new_ones)} 个脚本未在 tools/README.md 登记：{new_ones}；"
                 "每个 CLI 都必须在 README 的主题表里占一行（干什么用 / 用法），"
                 "否则后来者只能靠猜（AGENTS.md §8.13）")
    if missing:
        rep.warn("S14 tools/README 登记",
                 f"{len(missing)} 个受控脚本在磁盘上已不存在（属删除/迁移事件，S14 不判它）："
                 f"{missing[:8]}{' …' if len(missing) > 8 else ''}；"
                 "若确是迁移就同步基线与 README，若是误删就从 HEAD 取回")
    carried = [n for n in unreg if n in baseline]
    if carried:
        rep.warn("S14 tools/README 登记",
                 f"基线内存量欠债 {len(carried)} 个：{carried[:12]}"
                 f"{'' if len(carried) <= 12 else ' …共 ' + str(len(carried))}；补登记后请从 "
                 f"tools/audit_structure_baseline.json 的 s14_unregistered_tools 移出")
    if not new_ones and not carried and not missing:
        rep.ok("S14 tools/README 登记",
               f"受控 CLI 脚本 {len(tracked)} 个全部已在 tools/README.md 登记")


#: S12：已下架路径清单（读基线 retired_paths；出现即 FAIL）。
#
# 为什么需要这一条：2026-10-04 把论坛工作台（缺 UI 模板、每晚自动化因此连日 exit≠0）
# 整端归档后，**同一会话内它又被恢复了一次**（3 个 .py 回来了、模板依旧不在），
# 并把已下架的 4 个环境变量重新带入代码扫描 → `test_index_tables` 双向覆盖闸变红。
# 教训：靠“搬走文件”完成的下架扳不住另一个会话的还原，必须机械记账。
def _s12_retired() -> list:
    import json

    p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
    if not p.is_file():
        return []
    try:
        return list(json.loads(p.read_text(encoding="utf-8")).get("retired_paths") or [])
    except (json.JSONDecodeError, OSError):
        return []


def check_s12_no_resurrection(rep: Report) -> None:
    """S12：已归档/已下架的路径不得回到活跃目录树。"""
    hits = []
    for rel in _s12_retired():
        p = REPO_ROOT / rel
        if p.exists():
            hits.append(rel)
    if hits:
        rep.fail("S12 已下架路径复活",
                 f"这些路径已归档却又出现在工作区：{hits}；"
                 "若确需恢复，请先到 attic/ 取回完整内容（含模板与数据）并在 "
                 "tools/audit_structure_baseline.json 的 retired_paths 里移除，"
                 "否则就是拿着坏副本复活一条已证实不可运行的链路")
    else:
        rep.ok("S12 已下架路径复活", "无复活")


#: `tracking/` 下**非区域**目录的显式登记表（2026-10-04 结构审计新增）。
#:
#: 为什么需要它：S10 靠 `^[A-Z]{3}$` 识别区域，于是 `FORUM`（5 字母）恰好不匹配
#: 才没被当成区域——**这是隐式约定**，任何人新增一个 `FORUM2` / `TASK` 之类的目录，
#: 只要字母数不对就永远不会被 S10 提示。AGENTS.md §8.13 已把"再增非区域目录一律加
#: `_` 前缀"写成约定，但约定无法自动执行。
#:
#: 代价：登记了 88 处引用的 `reference/`、46 处的 `mining/` 物理搬迁风险远大于收益，
#: 故**只登记不搬**——本检查的职责是「让这些目录的存在被显式承认，且新增的必须
#: 显式登记」，而不是强推目录改名。
NON_REGION_DIRS = {
    "reference": "跨区参考文档（88 处引用；受控 17 文件；物理搬迁需同步 88 处，故保留）",
    "mining": "共享数据湖（46 处引用、受控 1052 文件；AGENTS.md §1 明令勿动/勿改）",
    "FORUM": "论坛语料与取证产物（受控 8 文件；活跃写入中）",
    "PPA_USA": "PPA 专项产物（运行期，未受控）",
    "prod_probe": "prod 探针 dump（运行期，tracking/.gitignore 已排除）",
    "hypotheses": "hypothesis_round 账本（运行期追加写，.gitignore 已排除）",
    "_scratch": "临时区（§6 第 3 条：用完清空）",
}


def check_s13_tracking_nonregion_registry(rep: Report) -> None:
    """S13：`tracking/` 下的非区域目录必须**显式登记**在 NON_REGION_DIRS。

    棘轮语义：
      - 存在但未登记 → **FAIL**（新增目录必须显式承认，防止继续积累"像区域的目录"）
      - 已登记但磁盘上不存在 → WARN（可从登记表清理，不阻塞）
      - 已登记且形如区域码（^[A-Z]{3}$）→ FAIL（登记了却用区域码命名，自相矛盾）
    """
    import re as _re

    tracking = REPO_ROOT / "tracking"
    if not tracking.is_dir():
        rep.ok("S13 tracking 非区域目录", "无 tracking/，跳过")
        return

    on_disk = {d.name for d in tracking.iterdir() if d.is_dir()}
    regions = {n for n in on_disk if _re.match(r"^[A-Z]{3}$", n)}
    actual_nonregion = on_disk - regions

    undeclared = sorted(actual_nonregion - set(NON_REGION_DIRS))
    for name in undeclared:
        rep.fail("S13 tracking 非区域目录",
                 f"tracking/{name} 既不是三字母区域码，也未登记在 "
                 f"audit_structure.NON_REGION_DIRS——新增非区域目录必须显式登记"
                 f"（AGENTS.md §8.13：再增非区域目录一律加 `_` 前缀），"
                 f"否则 S10 永远识别不到它，新 Agent 极易当成区域读")

    stale = sorted(set(NON_REGION_DIRS) - on_disk)
    if stale:
        rep.warn("S13 tracking 非区域目录",
                 f"登记表里有 {len(stale)} 项磁盘上已不存在，可从 "
                 f"NON_REGION_DIRS 清理：{stale}")

    misnamed = sorted(n for n in (regions & set(NON_REGION_DIRS))
                      if _re.match(r"^[A-Z]{3}$", n))
    for name in misnamed:
        rep.fail("S13 tracking 非区域目录",
                 f"tracking/{name} 用三字母区域码命名却登记为非区域目录，自相矛盾")

    if not undeclared and not misnamed:
        rep.ok("S13 tracking 非区域目录",
               f"{len(actual_nonregion)} 个非区域目录全部已登记"
               + (f"（另有 {len(stale)} 项登记项磁盘已不存在，仅 WARN）" if stale else ""))


def check_s15_agent_skill_copy_drift(rep: Report) -> None:
    """S15：Agent 宿主的 skills 副本必须与源逐文件一致。

    为什么需要这条闸
    ----------------
    `.claude/skills/` 是给 Cursor 等 Agent 宿主读取的**副本**，源是 `Claude/skills/`。
    根 `.gitignore` 把 `.claude/` 整目录排除（注释自承「改动源后需手动同步或重建」），
    因此副本**永不被扫描**：既不入库、也无人比对。一旦改了源而忘了手动同步，
    宿主读到的是旧 skills，且**不会有任何报错** —— 一种纯粹的静默不一致。

    2026-10-06 第二轮治理复核时实测两侧的 `diff -rq` 为 0 差异……但这个观测有陷阱，
    实测结论后来被**推翻**：见下方「硬链接」。

    ★★ 第三次实测（同一天，推翻前两次）：它其实是**目录联接**
    --------------------------------------------------------
    加闸当天做正反向验证：① 往副本追加内容后重跑 → 仍 OK；② 往副本放一个孤儿文件
    → 两边文件数**同时**从 505 变 506。追下去才是真相：

        os.path.realpath('.claude/skills') == os.path.realpath('Claude/skills')
        # => True，两边解析到同一个目录 D:\\...\\Claude\\skills

    即 `.claude/skills` 是 `Claude/skills` 的 **junction（联接）**——不存在两份文件，
    所以 content-based 比对**永远不可能报警**（那是在拿一个目录和它自己比）。
    顺带澄清：本机 `os.path.samefile` 是可信的（对内容不同的独立文件返回 False、
    对真硬链接返回 True），这次失效的原因在junction本身，不在 samefile。

    这个结论同时否掉了根 `.gitignore` 里那句注释的**误导**：那里写
    「由 Cursor 等宿主读取……**不受版本控制也不自动同步**，改动源后需手动同步或重建」
    ——读作"有一份独立副本需要人工维护"，实际是"同一个目录的第二个入口，无需维护"。
    后来的人照注释去"手动同步"，会把 racing 精力花在一个不存在的问题上。
    注释已于 2026-10-07 更正（详见 `.gitignore` 该处）。

    ⇒ 本闸因此先判 realpath：**解析到同一目录就明确报 junction**，不做无效的内容比对；
      只有两侧真正分离（有人用 `xcopy`/`robocopy`/重克隆把它换成真拷贝）时，
      才落到内容比对 + 孤儿检测。形态一变，闸在同一瞬间接手。

    语义
    ----
      - 两侧 realpath 相同 → OK，**明确写明是 junction**（无副本，无可比对象）
      - 真拷贝下有内容差异 / 单侧独有 → FAIL（宿主会读到过期 skills）
    """
    src_root = REPO_ROOT / "Claude" / "skills"
    copy_root = REPO_ROOT / ".claude" / "skills"

    if not copy_root.is_dir() or not any(copy_root.rglob("*")):
        rep.ok("S15 skills 副本同步",
               "无 .claude/skills/ 副本（干净克隆常态），跳过")
        return
    if not src_root.is_dir():
        rep.fail("S15 skills 副本同步",
                 f"副本 {copy_root.relative_to(REPO_ROOT)} 存在，但源 "
                 f"Claude/skills/ 不存在——副本成了唯一归档，请先恢复源")
        return

    import os as _os

    # 第一段：先判两侧是不是**同一个目录**。junction（联接）会让下面的内容比对
    # 变成"一个目录和它自己比"，那是 100% 恒等的无效检查，必须前置识别并说清楚。
    if copy_root.exists() and _os.path.realpath(copy_root) == _os.path.realpath(src_root):
        rep.ok("S15 skills 副本同步",
               f".claude/skills 是 Claude/skills 的联接（realpath 同址）——"
               f"不存在第二份拷贝，无漂移概念，内容比对在此形态下无效故跳过"
               f"（一旦被换成真拷贝，本闸自动转为内容比对 + 孤儿检测）")
        return

    def _rel(root: Path) -> set[str]:
        return {str(p.relative_to(root)).replace("\\", "/")
                for p in root.rglob("*") if p.is_file()}

    src_files, copy_files = _rel(src_root), _rel(copy_root)
    shared = sorted(src_files & copy_files)

    # 第二段：真拷贝形态。逐个 inode 比对（同一 inode 的两个目录项是硬链接，
    # 写了这一个等于写了那一个，不算漂移）。
    linked = {n for n in shared
              if _os.path.samefile(str(src_root / n), str(copy_root / n))}
    only_src = sorted(src_files - copy_files)
    only_copy = sorted(copy_files - src_files)
    changed = sorted(n for n in shared if n not in linked
                     and _sha12(src_root / n) != _sha12(copy_root / n))

    for name in changed:
        rep.fail("S15 skills 副本同步",
                 f"{name}：副本与源内容不一致（改了 Claude/skills/ "
                 f"却没同步 .claude/skills/——宿主会静默读旧版）"
                 f"（修法：重拷该目录，或重建副本）")
    for name in only_src:
        rep.fail("S15 skills 副本同步",
                 f"{name}：源有、副本缺（新增 skill 后需同步到 .claude/skills/）")
    for name in only_copy:
        rep.fail("S15 skills 副本同步",
                 f"{name}：副本有、源无（孤儿文件，宿主可能读到不在库中未归档的内容）")

    if not (only_src or only_copy or changed):
        rep.ok("S15 skills 副本同步",
               f"副本与源逐文件一致（{len(shared)} 个文件；同一 inode 者 {len(linked)} 个）")


CHECKS = {
    "s1": ("S1 sys.path 注入", check_s1_syspath),
    "s2": ("S2 依赖方向", check_s2_dep_direction),
    "s3": ("S3 同名模块", check_s3_name_collision),
    "s4": ("S4 硬编码路径", check_s4_abs_path),
    "s5": ("S5 reports/脚本", check_s5_report_scripts),
    "s6": ("S6 skills 漂移", check_s6_skill_drift),
    "s7": ("S7 根目录白名单", check_s7_root_allowlist),
    "s8": ("S8 根↔子目录分叉", check_s8_root_subdir_divergence),
    "s9": ("S9 声明目录存在", check_s9_declared_dirs_exist),
    "s10": ("S10 区域子目录", check_s10_region_skeleton),
    "s11": ("S11 tools 顶层冻结", check_s11_tools_top_frozen),
    "s12": ("S12 已下架路径复活", check_s12_no_resurrection),
    "s13": ("S13 tracking 非区域目录登记", check_s13_tracking_nonregion_registry),
    "s14": ("S14 tools/README 登记", check_s14_tools_readme_registry),
    "s15": ("S15 skills 副本同步", check_s15_agent_skill_copy_drift),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="仓库结构守护（只读）")
    ap.add_argument("--only", choices=sorted(CHECKS), action="append",
                    help="只跑指定检查（可重复）")
    ap.add_argument("--freeze-tools-top", action="store_true",
                    help="把当前 tools/ 顶层 .py 清单写进 S11 基线（建立/重置存量用）")
    ap.add_argument("--freeze-unregistered", action="store_true",
                    help="把当前「未在 tools/README.md 登记」的脚本清单写进 S14 基线（只登记存量欠债）")
    args = ap.parse_args(argv)

    if args.freeze_unregistered:
        import json

        p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
        data = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
        mentioned = _readme_mentions()
        names = sorted(n for n in _tools_tracked_scripts() if _looks_like_cli(n) and n not in mentioned)
        data["s14_unregistered_tools"] = names
        data["_s14_note"] = (
            "S14 存量欠债：这些 tools/ 脚本未在 tools/README.md 登记（2026-10-06 冻结）。"
            "WARN 不阻塞；补登记后请从本表**移出**（移出即棘轮收紧），新增未登记即 FAIL。"
        )
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[audit_structure] S14 基线已写入 {len(names)} 个未登记脚本 → {p.name}")
        return 0

    if args.freeze_tools_top:
        import json

        p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
        data = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
        names = sorted(x.name for x in TOOLS.glob("*.py"))
        data["s11_tools_top_level"] = names
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")
        print(f"[audit_structure] S11 基线已写入 {len(names)} 个 tools/ 顶层脚本 → {p.name}")
        return 0

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
