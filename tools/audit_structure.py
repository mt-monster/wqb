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
- **S7 根目录白名单**：仓库根只允许入口 / 配置 / 三份文档 / 会话草稿（**只校文件**，目录归 S17）。
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
- **S16 报告命名规范**：`output_report/**`、`reports/**` 与 `tracking/` **顶层**的报告类文件
  必须守 §8.13：纯 ASCII 无空格、日期**不带杠**、带日期时 `YYYYMMDD` **作后缀**。
  2026-10-08 第二轮输出目录复核新增。**棘轮**：存量违规登记进基线 → WARN，**新增违规 → FAIL**。
  背景：第一轮治理把 `output_report/`+`reports/` 的日期带杠件全部改名后，
  同一个治理动作**漏扫了 `tracking/` 顶层**（4 个 `2026-10-0X_robustness.md` 一直躺着），
  且随后仍有会话把分析报告写进 `cache/`（不入库、会被 `git clean -fd` 带走）
  ——文字纪律守不住持续写入，必须有读数。
- **S17 顶层目录已声明**：仓库根的非点开头目录必须在 `S17_TOP_DIR_ALLOWLIST` 里。
  2026-10-14 结构审计新增，**FAIL 不进基线**。起因：根出现一整棵 skills 树
  `wq-brain-ra-usa/`（455 件，与 `Claude/skills/` 名单 100% 相同），而 S7 对目录是
  `if p.is_dir(): continue` 无条件跳过、S9 只校「声明的在不在」 ⇒ 未声明顶层目录是整套守护的空白。
  点开头目录（宿主配置 / VCS / 解释器缓存）一律放行：逐个登记会随客户端增减反复误红。
- **S18 `tracking/` 产物纯度**：`tracking/` 的**索引面**不得含运行期产物 —— 路径里有
  `<名>_<YYYYMMDD>[_<HHMM>]` 形态的目录段，或是 `.log` → FAIL（**不进基线**）。
  2026-10-14 结构审计新增。起因是 `perf_max` 的缺省 `plan_dir` 指向 `tracking/<region>/perfmax/…_<时间戳>/`，
  实测把 89 件派发断点（`plan/dispatch_spec/score/variants_*.txt`）写进了版本控制。
  ⚠ 签名**只按目录形态**、不按 `plan.json`/`score.json` 这类文件名：实测后者在 tracking/ 索引面
  另有 4 个合法业务件（`candidates/*_plan.json`、`mining/field_inspect_*_score.json`），按名拦会误伤战役台账。
- **S20 索引↔工作树一致**：`git ls-files --deleted` 非空 → FAIL（索引挂着工作树已不存在的幽灵路径）。
  2026-10-14 同轮新增。起因：`reports/<主题>_<日期>/` 改名成 `…_refs/` 时只暂存了新路径，
  旧路径 25 件删除未暂存 ⇒ 按索引取面的 S16 照扫旧路径并 FAIL，而 pre-commit 跑在建提交对象之前
  ⇒ 磁盘上根本不存在的路径卡住整条提交链。
- **S21 跟踪件扩展名**：`git ls-files` 全仓面上，基名不含 `.` 的件 → FAIL（**不进基线**）。
  2026-10-15 批次I 新增，将 §6 规则⑤「文件必须有扩展名」从「只管 `tools/` 顶层」补到全仓。
  背景：S11 只看 `tools/*` 一层，S16/S18 取面先按扩展名筛 ⇒ 三条合起来对其余位置的
  无扩展名件**结构性失明**。活样本 `tools/mcp_py`：一个无扩展名的 Python 脚本，
  因基名无 `.` 同时躲过 S4（盘符）/S11/S14 与全仓 `*.py` 扫描。
  豁免两份：**名字型**（`Makefile`/`Dockerfile`/`LICENSE`… 由工具按全名识别，加扩展名反而认不出）、
  **路径型**（`tools/git-hooks/pre-commit|commit-msg`，git 只执行精确名）——
  两者不可互换，把 hook 名挪进名字型等于给任意目录的 `pre-commit` 开口子。
  路径型条目从索引消失 → WARN 催删（防它变永久豁免通道，同 S13/S11）。

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
OUTPUT_REPORT = REPO_ROOT / "output_report"
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
    "reports/ra_pipeline_stage_review_20260927_refs/",
    "reports/skills_review_20260929_refs/",
    "reports/forum_alpha_research/",
    # 文件级：这两份有审查报告写明「可复现：python reports/xxx.py」
    "reports/skills_pipeline_stage_review_20260927",
    "reports/skills_stage_review_v2_20260927",
    "reports/dryrun_chain_runner_20260927",
    "reports/dryrun_chain_runner_v2_20260927",
    # T4 字段名 diff 证据脚本，与 `output_report/deu_field_name_verification_20261010.md`
    # 配对（该报告点名「diff 脚本」）。2026-10-10 第四轮治理自 output_report/ 迁入
    # （S16 规则⑤：产物目录不得混入脚本）——同 dryrun_chain_runner 的可重跑证据语义。
    "reports/diff_t4_20261010",
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


#: S11 取面扩展（2026-10-14 布局审计批次F）：`tools/` 顶层**允许常驻的非 .py 件**。
#:
#: 为什么要有这张表
#: ----------------
#: S11 的取面一直是 `TOOLS.glob("*.py")`，加上后来补的「无扩展名」一条 —— 于是
#: **带扩展名但非 `.py` 的顶层件对整条闸链结构性失明**（S4 盘符扫 `*.py`、S14 按脚本名登记、
#: S16 只看报告面）。活样本是 `tools/skeleton_quota.json`：一个数据配置文件，
#: 在顶层躺了一个多月，`THEMES.json` 里没有它、`tools/README.md` 里没有它、
#: 没有任何一道闸看过它一眼 —— 报告 §2.C-3 是靠人读目录才发现的。
#: 同一目录出现「一种文件形态永久看不见」就是结构性缺口，与 `mcp_py`（无扩展名）同族。
#:
#: 口径：`tools/` 是 **CLI 层**，顶层只该有脚本 + 闸自己的登记表 + 唯一索引。
#: 判据不是「名字像不像配置」而是「**谁读它**」：
#:   - 数据件 → 区域级进 `tracking/<R>/reference/`，规范级进 `src/wqb/<包>/*.json`
#:     （现成先例：`src/wqb/profiles/category_cards.json`）；
#:   - 工具文档 → `tools/docs/` 或主题目录（2026-10-14 批次1 已把 5 份 `README_*.md` 迁进 `tools/docs/`）；
#:   - 运行期可写产物 → `cache/` / `logs/`（§8.13）。
#: 确实需要常驻顶层 → 在本表登记并**写明理由**（理由缺失=表退化成黑名单，同 S13 的纪律）。
TOOLS_TOP_DATA_ALLOWLIST = {
    "README.md": "tools/ 的唯一索引（S14 的登记面），AGENTS.md §1 指它当入口",
    "THEMES.json": "S11 自己的归属登记表，本闸逐条读它，移走等于拆闸",
    "audit_structure_baseline.json": "S6/S11/S14/S16 的存量基线，本闸自己读",
}


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


def _themes_moved_verified() -> tuple[int, list]:
    """各主题 `moved_files` 的**磁盘核验**：返回 (真下沉数, 名不副实清单)。

    真下沉判据两条都要满足：① 该名字**不在** `tools/` 顶层；② 该名字**在**主题目录里存在。
    起因是本闸 docstring 第 1 条战例（`ac2cf35` 号称下沉 10 个、实为子目录新建，顶层一个没少）——
    当时靠人工读 git log 才发现。旧读数 `len(baseline) - len(now & baseline)` 更是**反的**：
    真下沉后按纪律要把名字移出基线（本闸自己就是这么提示的），于是移出后读数归零，
    「已下沉 0 个」与「从没下沉过」长得一样，进度不可见。改成按登记表 + 磁盘实核，
    2026-10-14 实测真下沉 23 个、名不副实 0 个。
    """
    import json

    p = REPO_ROOT / "tools" / "THEMES.json"
    if not p.is_file():
        return 0, []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0, []
    top = {q.name for q in TOOLS.glob("*.py")}
    ok, bogus = 0, []
    for key, th in (data.get("themes") or {}).items():
        thdir = TOOLS / Path(str(th.get("dir") or "")).name
        for f in th.get("moved_files") or []:
            name = Path(f).name
            still_top = name in top
            in_sub = (thdir / name).is_file()
            if not still_top and in_sub:
                ok += 1
            else:
                why = "顶层仍在（未真迁）" if still_top else "主题目录里不存在（漏 mv / 已回滚 / 登记名写错）"
                bogus.append(f"{key}/{name}：{why}")
    return ok, bogus


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
    # ⚠ 基线缺失**不得**整闸早退（2026-10-14 批次F 改掉）。旧写法 `if not baseline: warn; return`
    # 让「.py 存量清单读不到」连带关掉同闸其余各条 —— 无扩展名件、顶层数据件、主题归属棘轮、
    # moved_files 核验全都不跑，而读数只有一行 WARN，看着像「本闸已评估」。
    # 现在只关掉确实依赖基线的那两条（added / gone），其余各条照校。
    no_baseline = not baseline
    # 无扩展名件单独成条（2026-10-14 布局审计新增）：活样本是原 `tools/mcp_py` ——
    # 一个 UTF-8 Python 脚本，只因名字没有 `.py`，就同时躲过了 S4（硬编码盘符）、
    # S11（顶层冻结）、S14（README 登记）与全仓 `*.py` 扫描，于是它带着 `D:\...` 绝对路径
    # 和已退役的 8876 端点长期躺在顶层、无人知。取面按扩展名筛的闸，对无扩展名文件是**结构性失明**，
    # 所以这里不是补一条命名洁癖，而是把这类件重新拉回所有闸的视野。
    extless = sorted(p.name for p in TOOLS.iterdir()
                     if p.is_file() and not p.suffix and not p.name.startswith("."))
    if extless:
        rep.fail("S11 tools 顶层冻结",
                 f"tools/ 顶层有无扩展名文件 {extless}：脚本必须带 `.py`（否则 S4/S11/S14 与"
                 "一切 `*.py` 取面的闸都看不见它），文档必须带 `.md`；"
                 "活样本 `tools/mcp_py` 已于 2026-10-14 更名为 `mcp_http_caller.py`")

    # 取面扩展的另一半（2026-10-14 批次F）：**带扩展名但不是 `.py`** 的顶层件。
    # 活样本是 `tools/skeleton_quota.json` —— 数据配置在 CLI 层顶层躺了一个多月，
    # THEMES.json 没它、README 没它、S4/S14/S16 也都不看它（报告 §2.C-3 靠人读目录才发现）。
    # `TOOLS_TOP_DATA_ALLOWLIST` 的注释写明判据（看「谁读它」，不看名字像不像配置）。
    others = sorted(p.name for p in TOOLS.iterdir()
                    if p.is_file() and p.suffix and not p.name.startswith(".")
                    and p.suffix != ".py")
    stray = [n for n in others if n not in TOOLS_TOP_DATA_ALLOWLIST]
    for name in stray:
        rep.fail("S11 tools 顶层冻结",
                 f"tools/ 顶层有未登记的非脚本件 `{name}`：`tools/` 是 CLI 层，顶层只允许脚本 + "
                 f"`audit_structure.TOOLS_TOP_DATA_ALLOWLIST` 里的登记表与唯一索引。"
                 f"按 §8.13 归属：数据件 → 区域级 `tracking/<R>/reference/`、"
                 f"规范级 `src/wqb/<包>/`（先例 `profiles/category_cards.json`）；"
                 f"工具文档 → `tools/docs/` 或主题目录；运行期产物 → `cache/`|`logs/`。"
                 f"（活样本 `tools/skeleton_quota.json` 已于 2026-10-14 迁至 "
                 f"`tracking/KOR/reference/`）")
    allow_gone = sorted(n for n in TOOLS_TOP_DATA_ALLOWLIST if n not in others)
    if allow_gone:
        rep.warn("S11 tools 顶层冻结",
                 f"TOOLS_TOP_DATA_ALLOWLIST 有 {len(allow_gone)} 项顶层已不在：{allow_gone}；"
                 "确认它真是「不再需要常驻」再从表里删 —— 参照 S13 的教训："
                 "直接照 WARN 提示删登记项，可能把闸变成陷阱（登记表缺失≠该件不该存在）")

    added = sorted(now - baseline)
    gone = sorted(baseline - now)
    if no_baseline:
        rep.warn("S11 tools 顶层冻结",
                 "基线为空或未登记 s11_tools_top_level —— 仅「新增脚本」与「已移出」两条读数未生效，"
                 "先跑 `python tools/audit_structure.py --freeze-tools-top` 写入存量清单；"
                 "本闸其余各条（无扩展名 / 顶层数据件 / 主题归属 / moved_files）照旧校")
    else:
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

    moved, bogus = _themes_moved_verified()
    if bogus:
        rep.fail("S11 tools 顶层冻结",
                 f"{len(bogus)} 条 `moved_files` 登记与磁盘不符：{bogus}；"
                 "「下沉」必须是 `git mv`（顶层少一个、子目录多一个），"
                 "在子目录**新建**一份不算下沉（战例见本闸 docstring）")
    if not added and not gone and not unassigned and not stray and not extless and not bogus:
        rep.ok("S11 tools 顶层冻结",
               f"顶层 {len(now)} 个脚本与基线一致（只减不增；基线 {len(baseline)}、"
               f"已下沉 {moved} 个（THEMES 登记 ∩ 磁盘核验）、未归属 0 个），"
               f"非脚本件 {len(others)} 个全部在允许清单内（{others}）")



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

#: 登记了、但**允许磁盘上暂时没有**的非区域目录（S13 的 stale WARN 对此静音）。
#: 为什么留而不是按 WARN 提示删掉：`PPA_USA` 是 PPA 战役的运行期产物目录，
#: 2026-10-14 实测磁盘无此目录 = 该区战役当前没开（产物已归档 `attic/ppa_mining_*`），
#: 一旦有人复跑 PPA 战役它就长回来 —— 而那时它不在登记表里就是 **FAIL**。
#: 即「WARN 提示的清理动作会把闸变成陷阱」。守护见
#: `tests/unit/07_docs_skills/test_audit_structure_s13.py`（本集合必须是 NON_REGION_DIRS 的子集）。
NON_REGION_DIRS_ALLOW_ABSENT = frozenset({"PPA_USA"})


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

    stale = sorted(set(NON_REGION_DIRS) - on_disk - NON_REGION_DIRS_ALLOW_ABSENT)
    if stale:
        rep.warn("S13 tracking 非区域目录",
                 f"登记表里有 {len(stale)} 项磁盘上已不存在，可从 "
                 f"NON_REGION_DIRS 清理：{stale}")
    absent_ok = sorted(n for n in NON_REGION_DIRS_ALLOW_ABSENT if n not in on_disk)

    misnamed = sorted(n for n in (regions & set(NON_REGION_DIRS))
                      if _re.match(r"^[A-Z]{3}$", n))
    for name in misnamed:
        rep.fail("S13 tracking 非区域目录",
                 f"tracking/{name} 用三字母区域码命名却登记为非区域目录，自相矛盾")

    if not undeclared and not misnamed:
        rep.ok("S13 tracking 非区域目录",
               f"{len(actual_nonregion)} 个非区域目录全部已登记"
               + (f"（另有 {len(stale)} 项登记项磁盘已不存在，仅 WARN）" if stale else "")
               + (f"（{absent_ok} 属运行期目录，允许暂缺、不按 stale 报：见 "
                  f"NON_REGION_DIRS_ALLOW_ABSENT）" if absent_ok else ""))


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


# ---------------------------------------------------------------- S16 报告/产物命名
#: 扫描面：`output_report/**` + `reports/**` 的报告类文件，外加 `tracking/` **顶层** .md。
#: `tracking/` 之所以只取顶层：`<REGION>/` 下是战役产物（另有区域目录约定），
#: 而 2026-10-08 复核发现的 4 个「日期带杠」件（`tracking/2026-10-0X_robustness.md`）
#: 正躺在顶层 —— 第一轮治理扫了 output_report/reports，**漏的就是这一层**。
S16_SUFFIXES = {".md", ".json", ".txt", ".csv", ".html"}
#: 报告类文件里不算违规的例外名（目录说明等）。
S16_EXEMPT_NAMES = {"README.md", "MANIFEST.md", "CHANGELOG.md"}
_DASH_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
_D8_RE = re.compile(r"(?<!\d)\d{8}(?!\d)")
#: 机器生成产物的命名后缀 —— 豁免「缺日期」规则④。理由：这些名字由生成器模板拼出，
#: 且消费方依赖**同名覆盖**语义（`feature_engineering.py` 的 `stale_ideas_md_path`、
#: `dataset_experience.py` 生成 + `step9_audit.py` 校验的既定文件名，见 §8.13）。
#: 给它们塞日期会让同一数据集每跑一次多出一个新文件，stale 比对随之失效。
#: 其余三条规则（ASCII / 不带杠 / 日期须作后缀）对它们**照样生效**。
S16_MACHINE_SUFFIXES = ("_ideas.md", "_campain.md")

#: S16 规则⑦（2026-10-14 布局审计 §6 规则⑦「同一父目录内风格不混用」）：
#: `reports/` 与 `output_report/` 的**一层子目录名**一律 kebab-case（§8.13「目录：小写 kebab-case」）。
#: ⚠ **布局审计报告 `reports/project_layout_audit_20261014.md` §3 树注释与 §5 第 10 条原写
#: 「`reports/` 子目录命名统一为 snake_case」，与本闸方向相反 —— 按 §8.13 裁决作废（报告内已同步更正）**：
#: §8.13 是全仓目录规范的唯一权威（S11 的 19 个主题目录、S17 的顶层目录都按它建），
#: 若为 reports/ 单开一套 snake，等于给「同仓两套目录风格」再多一个例外面。
#: 改名代价实测（`git grep -o -h -- <路径>` 命中行数 / 文件数，2026-10-14 tracked 面）：
#: `dataset_experience` 40/24、`forum_alpha_research` 20/12、
#: `ra_pipeline_stage_review_20260927_refs` 43/17、`skills_review_20260929_refs` 9/5
#: —— 四个都不合规，也**没有一个**能安全单件改名。故：新目录按 kebab 守，存量 4 个登记不回改。
#: 只扫**一层**：规则⑦ 的观察单位是「同一父目录内的兄弟」；二层实测只有
#: `reports/ra_pipeline_stage_review_20260927_refs/realenv/` 一个目录且已是 kebab，无混用。
S16_DIR_FACE = ("reports", "output_report")
_KEBAB_DIR_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
#: 存量欠债。**移出条件 = 该目录改名后旧路径全库 refs=0**（不是「看着不顺眼」）。
#: 每条理由都是「为什么单独改它会制造事故」，不是「为什么可以不改」。
S16_DIR_LEGACY = {
    "reports/dataset_experience":
        "生成器 `dataset_experience.py` 写名 + `step9_audit.py` 校验 + 实测 40 行/24 文件引用"
        "（含 §8.13 登记的既定文件名 `<region>_<ds>_campain.md`）；"
        "同 §8.13「campain 非笔误，禁止单独改」那条纪律 —— 要改就连生成/校验/测试/存量一起专项处理",
    "reports/forum_alpha_research":
        "目录内脚本自引用自身路径（gather_search_v2.py / make_digest.py 等）+ 实测 20 行/12 文件引用；"
        "改名即 `doc_path_refs.py` 棘轮硬闸的活文档死指针",
    "reports/ra_pipeline_stage_review_20260927_refs":
        "§8.13 已登记的**同名消歧后缀**（输出目录治理第三轮 P2-C：目录加 `_refs`、`.md` 主体不动）；"
        "实测 43 行/17 文件引用（含报告主体自己的复现命令 `…_refs/reproduce.sh`、`realenv/`），"
        "再改一次名就是死指针",
    "reports/skills_review_20260929_refs":
        "同上（P2-C 同批裁决），实测 9 行/5 文件引用，主体指向 `…_refs/check_skills.py`",
}


def _s16_dir_names(others: bool = False) -> list:
    """`reports/` 与 `output_report/` 的一层子目录名（来自 git 的文件清单派生）。

    为什么从**文件清单**派生而不是 `iterdir()`：目录本身不在 git 索引里（git 只跟踪文件），
    `iterdir()` 会把 `__pycache__`、别的会话刚 mkdir 还没落件的空中目录都算进来 ——
    那是「目录存在性」问题，不是「命名风格」问题，混在一起只会造出与内容无关的红。
    fail-closed：取不到清单即抛 `RuntimeError`，由调用方转 FAIL。
    """
    cmd = ["git", "ls-files", "-z"]
    cmd += ["--others", "--exclude-standard"] if others else ["--"]
    cmd += ["--", *S16_DIR_FACE]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        raise RuntimeError(f"git ls-files 失败（rc={r.returncode}）：{r.stderr.strip()[:200]}")
    out = set()
    for x in filter(None, (r.stdout or "").split("\0")):
        parts = Path(x).as_posix().split("/")
        # ⚠ 本闸首跑就是把这条判据写错才判红的：`len(parts) < 2` 时 `parts[1]` 取到的是
        # `reports/skills_review_20260929_closure.md` 这类**顶层文件**，于是 30+ 个 .md 被当成
        # 「不合规的子目录」。子目录的证据是路径里**还有第三段**，不是第二段存在。
        if len(parts) < 3:
            continue  # 面上直接散落的文件，不是子目录
        if "__pycache__" in parts:
            continue
        out.add(f"{parts[0]}/{parts[1]}")
    return sorted(out)


def _s16_dir_on_disk(rel: str) -> bool:
    """存量登记项是否**真的还在盘上**（独立成一个函数就是为了可被测试替换）。

    ⚠ 判据不用 `rel in dirs_tracked`（git 跟踪面）：那会把「目录在盘上、只是里面暂时没有
    跟踪件」误报成「登记已失效」。而这条 WARN 让人做的动作是**删掉条目** —— 误报等于诱导人
    摘掉一把仍然有效的伞，下次那个目录复跑就 FAIL 阻断提交（S13 的 `PPA_USA` 是同一形态，
    AGENTS.md §8.13 专门为它写过「别按 S13 的 WARN 提示把它删掉」）。
    """
    return (REPO_ROOT / rel).is_dir()


def _s16_targets() -> list:
    """S16 扫描件（相对仓库根的 posix 路径）。

    只取 **git 跟踪的**（含已暂存）：与 S14 同口径 —— 未跟踪的在途文件不该拦住别人的提交；
    而一旦 `git add`，新文件即进入 `git ls-files`，正是本闸要拦的时刻（pre-commit 在建
    提交对象**之前**跑，此时新文件已在索引里）。
    """
    r = subprocess.run(["git", "ls-files", "-z", "--", "output_report", "reports", "tracking/*.md"],
                       capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        # 拿不到清单就报错：静默给空清单 = S16 看似在跑实则永不过（fail-open）。
        raise RuntimeError(f"git ls-files 失败（rc={r.returncode}）：{r.stderr.strip()[:200]}")
    out = []
    for x in filter(None, r.stdout.split("\0")):
        rel = Path(x).as_posix()
        if Path(x).name in S16_EXEMPT_NAMES:
            continue
        if Path(x).suffix.lower() not in S16_SUFFIXES:
            continue
        # git 缺省把 `*` 当跨 `/` 匹配（无 FNM_PATHNAME），`tracking/*.md` 会连子目录一起吐
        # ⇒ 目录层级过滤必须在 Python 侧做（同 S14 的 `_tools_tracked_scripts`）。
        if rel.startswith("tracking/") and rel.count("/") > 1:
            continue
        out.append(rel)
    return sorted(out)


def _s16_untracked() -> list:
    """S16 预检面：**未跟踪**的报告类文件（在途，还没进索引）。

    为什么单独取这一面：`_s16_targets()` 只取 git 跟踪的，那是**有意的取舍**
    （在途文件不该拦住别人的提交）。但代价是违规在 `git add` 之前**完全隐形**，
    而 `git add` 的那一刻它就 FAIL —— 恰好撞上 S16 的立项理由「文字纪律守不住
    持续的写入」（2026-10-10 实测复发一次：`tracking/2026-10-09_robustness.md`
    在 `git add` 前静默通过，一 add 即 FAIL，而这已是同类问题第二轮）。

    故本节只做 **WARN 预检**，不动 `_s16_targets()` 的 FAIL 语义：让人在写盘后
    立刻看见命名违规，而不是等到提交被拦。未跟踪件**不进基线**（它们随时会被
    改名或删除），也**不算 FAIL**（并行会话的在途文件不该互相拦截）。
    """
    r = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z", "--",
         "output_report", "reports", "tracking/*.md"],
        capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        return []
    out = []
    for x in filter(None, r.stdout.split("\0")):
        rel = Path(x).as_posix()
        if Path(x).name in S16_EXEMPT_NAMES:
            continue
        if Path(x).suffix.lower() not in S16_SUFFIXES:
            continue
        if rel.startswith("tracking/") and rel.count("/") > 1:
            continue
        machine = _is_machine_name(x)
        if _naming_violations(rel, machine_ok=machine):
            out.append(rel)
    return sorted(out)


def _is_machine_name(rel: str) -> bool:
    """该报告类文件是否机器产物（豁免「缺日期」规则④）。见 `S16_MACHINE_SUFFIXES`。"""
    return any(Path(rel).name.endswith(s) for s in S16_MACHINE_SUFFIXES)


def _naming_violations(rel: str, machine_ok: bool = False) -> list:
    """返回该文件名违反 §8.13 命名规范的理由列表（空 = 合规）。

    四条（AGENTS.md §8.13「命名规范」，新建即守、存量不强制回改）：
      ① 纯 ASCII、无空格；
      ② 日期不带杠（`20261008` 而非 `2026-10-08`）；
      ③ 带日期时 `YYYYMMDD` **必须作后缀**（`skills_review_20261003.md`）；
      ④ **人工撰写的报告必须带日期**（`reports/`/`tracking/` 顶层的报告）。
         机器产物豁免（`machine_ok=True`）：见 `S16_MACHINE_SUFFIXES` 的说明 ——
         它们的名字由生成器拼出，消费方依赖同名覆盖，塞日期会破坏 stale 语义。

    规则④的由来（2026-10-10 P2-D）：§8.13 原文写「产物与报告**一律** `YYYYMMDD`
    作后缀」，而实现此前只在**已含日期**时校验格式位置 —— 无日期的文件名永不过闸、
    也永进不了基线（实测 `output_report/` 有 62 个、`reports/` 子目录 25 个无日期件）。
    文档与实现漂移 ⇒ 下一个人读 §8.13 会以为那 87 个都是违规。故补齐实现，让两边
    对「什么叫合规」有同一个答案；存量的 25 件进 `s16_naming_violations` 基线（WARN）。
    """
    name = Path(rel).name
    stem = name.rsplit(".", 1)[0]
    bad = []
    if any(ord(c) > 127 or c == " " for c in name):
        bad.append("非 ASCII / 含空格")
    if _DASH_DATE_RE.search(stem):
        bad.append("日期带杠（应为 YYYYMMDD 无杠）")
    for m in _D8_RE.finditer(stem):
        if not stem.endswith("_" + m.group(0)):
            bad.append(f"日期 {m.group(0)} 不在末尾（应作后缀）")
            break
    if not bad and not machine_ok and not _D8_RE.search(stem):
        bad.append("缺日期（报告应带 YYYYMMDD）")
    return bad


def _s16_baseline() -> set:
    """S16 存量基线：允许「违反命名规范」的存量件（路径集合，只减不增）。"""
    import json

    p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
    if not p.is_file():
        return set()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return set(data.get("s16_naming_violations") or [])
    except (json.JSONDecodeError, OSError):
        return set()


def _s16_script_hits() -> tuple:
    """S16 规则⑤扫面：`output_report/**/*.py`（脚本不该出现在产物目录）。

    返回 `(已跟踪, 未跟踪在途)` 两个列表。命名规则天然管不到 `.py`
    （`S16_SUFFIXES` 只含报告类扩展名），实测曾有 `output_report/diff_t4.py`
    长期隐形（2026-10-10 第四轮 P1-4 补闸）。取舍与命名预检一致：
    跟踪件 FAIL（进索引就是提交时刻），在途件 WARN（写盘即见、不拦别人）。
    """
    tracked, pend = [], []
    for p in py_files(OUTPUT_REPORT):
        rel = p.relative_to(REPO_ROOT).as_posix()
        r = subprocess.run(["git", "ls-files", "--error-unmatch", "--", rel],
                           capture_output=True, cwd=str(REPO_ROOT))
        (tracked if r.returncode == 0 else pend).append(rel)
    return sorted(tracked), sorted(pend)


#: S16 规则⑥（2026-10-14 布局审计 §4「docs 混结论件」新增）：`docs/**` 的命名与归属面。
#: 取这里而不是新起一道 S：规则①②③与报告面**完全同源**，只差「要不要带日期」这一条，
#: 分成两道闸会让下一个人以为 docs/ 也要求日期（实测 docs/ 有 79 个 .md，其中规范类无日期件占多数）。
#: ⚠ docs/ **不适用规则④（必须带日期）**：`docs/` 是长期规范 / SOP / 速查（§8.13），
#: 一份 `tool_registry.md` 不该为了过闸而编一个日期。
S16_DOCS_FACE = "docs"
#: `docs/plans/` 保持 `YYYY-MM-DD-<主题>.md` **前缀带杠**写法（§8.13 明示的成型例外，实测 8 个）。
#: 该目录内不混用，故整目录豁免规则②③；规则①（ASCII）与⑤（snake_case）照样生效。
S16_DOCS_EXEMPT_DIRS = ("docs/plans/",)


def _s16_docs_targets(others: bool = False) -> list:
    """`docs/**` 的文档面（`others=True` 取未跟踪在途件）。

    fail-closed：`git ls-files` 取不到清单即抛 `RuntimeError`，由调用方转 FAIL ——
    与 S14/S16/S18/S20 同口径（静默空集 = 闸形同虚设）。
    """
    cmd = ["git", "ls-files", "-z"]
    if others:
        cmd += ["--others", "--exclude-standard"]
    cmd += ["--", S16_DOCS_FACE]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        raise RuntimeError(
            f"git ls-files（docs 面{'' if others else ' / 在途'}）失败 rc={r.returncode}："
            f"{r.stderr.strip()[:200]}")
    out = []
    for x in filter(None, r.stdout.split("\0")):
        if Path(x).suffix.lower() not in S16_SUFFIXES:
            continue
        if Path(x).name in S16_EXEMPT_NAMES:
            continue
        out.append(Path(x).as_posix())
    return sorted(out)


def _docs_naming_violations(rel: str) -> list:
    """`docs/` 面适用的 §8.13 命名子集（空 = 合规）。与报告面的四条**不同**，见 `S16_DOCS_FACE` 说明。"""
    name = Path(rel).name
    stem = name.rsplit(".", 1)[0]
    in_plans = rel.startswith(S16_DOCS_EXEMPT_DIRS)
    bad = []
    if any(ord(c) > 127 or c == " " for c in name):
        bad.append("非 ASCII / 含空格")
    if re.search(r"[A-Z]", name):
        bad.append("含大写字母（§8.13 文件一律 snake_case；实测 docs/ 面唯一合法的大写件是 README/CHANGELOG，已在豁免名单）")
    if not in_plans:
        if _DASH_DATE_RE.search(stem):
            bad.append("日期带杠（应为 YYYYMMDD 无杠）")
        for m in _D8_RE.finditer(stem):
            if not stem.endswith("_" + m.group(0)):
                bad.append(f"日期 {m.group(0)} 不在末尾（应作后缀）")
                break
    return bad


def check_s16_output_naming(rep: Report) -> None:
    """S16：`output_report/`+`reports/`+`tracking/` 顶层的报告类文件命名（2026-10-08 新增）。

    背景：§8.13 的命名规范（`YYYYMMDD` 作后缀、纯 ASCII、日期不带杠）此前**只写在文档里**，
    没有机械闸，于是第一轮治理改完 `output_report/`+`reports/` 后：
      ① 同一个治理动作**漏扫了 `tracking/` 顶层**（4 个 `2026-10-0X_robustness.md` 一直躺着）；
      ② 并行会话随后又往 `cache/` 写了一份分析报告（属会丢的位置，见复核报告 §2.B）。
    文字纪律守不住持续的写入，故加棘轮：存量入基线（WARN 可见不阻塞），**新增违规 → FAIL**。

    规则⑤（2026-10-10 第四轮 P1-4）：`output_report/` **不得混入脚本**（`.py`）——
    产物目录不是代码目录（§8.13）。第三轮曾人工核过「0 .py」但没有机械闸守，
    随即又出现 `output_report/diff_t4.py`；脚本按 §8.13 去 `tools/`（可复用）或
    `logs/_tmp_*.py`（一次性），审计证据脚本走 `reports/` + `S5_EXEMPT_PREFIXES` 登记。

    规则⑥（2026-10-14 布局审计 §4）：**`docs/**` 也进命名面**。起因是本轮治理在 `docs/reference/`
    抓到两份结论式报告（`CODE_QUALITY_SUMMARY.md`、`INTEGRATION_COMPLETE.md`，已迁 `reports/`），
    而 S16 此前的取面是 `output_report` + `reports` + `tracking/` 顶层 —— **`docs/` 整个不在扫描面里**，
    于是「大写命名 + 报告混进规范目录」这类问题对本闸结构性失明（同 S11 的扩展名失明、S18 的顶层失明）。
    docs/ 面只校 §8.13 的 ASCII / snake_case / 日期形态三条，**不校「必须带日期」**
    （`docs/` 是长期规范区，一份 `tool_registry.md` 不该为过闸编日期）；`docs/plans/` 整目录豁免日期形态
    （§8.13 明示它保持 `YYYY-MM-DD-<主题>.md` 前缀写法，实测 8 个）。

    规则⑦（2026-10-14 布局审计 §6 规则⑦）：**报告子目录名 = kebab-case**。同一父目录内
    5 个 kebab 与 4 个 snake 并存（`forum-experience` vs `dataset_experience`），存量入
    `S16_DIR_LEGACY`（逐条写明「为什么单独改名会造事故」），**新建即守**。
    ⚠ 与本闸方向相反的旧建议（报告 §5 第 10 条「统一为 snake_case」）已在 `S16_DIR_FACE`
    注释处裁决：以 §8.13 的目录规范（kebab）为唯一权威。
    """
    try:
        targets = _s16_targets()
    except RuntimeError as e:
        rep.fail("S16 报告命名规范", f"无法取受控清单（{e}）—— 不当作「全部合规」放过")
        return
    viol = {rel: _naming_violations(rel, machine_ok=_is_machine_name(rel))
            for rel in targets}
    viol = {k: v for k, v in viol.items() if v}
    baseline = _s16_baseline()
    new_ones = sorted(k for k in viol if k not in baseline)
    if new_ones:
        sample = "；".join(f"{k}（{'、'.join(viol[k])}）" for k in new_ones[:5])
        rep.fail("S16 报告命名规范",
                 f"新增 {len(new_ones)} 个文件名违反 §8.13（日期 YYYYMMDD 作后缀 / 不带杠 / 纯 ASCII 无空格）："
                 f"{sample}{' …' if len(new_ones) > 5 else ''}；"
                 "改名为 `<主题>_<YYYYMMDD>.md` 并同步引用，或确认有意的例外后登记进基线")
    carried = sorted(k for k in viol if k in baseline)
    if carried:
        rep.warn("S16 报告命名规范",
                 f"基线内存量违规 {len(carried)} 个（§8.13 明示存量不强制回改，仅提示）："
                 f"{carried[:6]}{'' if len(carried) <= 6 else ' …共 ' + str(len(carried))}；"
                 "改一个就请从 tools/audit_structure_baseline.json 的 s16_naming_violations 移出（棘轮收紧）")
    # 在途件预检：WARN，不进基线、不算 FAIL。理由见 `_s16_untracked()` 文档字符串 ——
    # 不做这一步的话，命名违规在 `git add` 之前完全隐形（2026-10-10 第二轮复发）。
    pend = _s16_untracked()
    if pend:
        rep.warn("S16 报告命名规范",
                 f"{len(pend)} 个**未跟踪**（在途）报告文件名违反 §8.13，"
                 f"`git add` 后会转为 FAIL：{pend[:6]}{'' if len(pend) <= 6 else ' …' }；"
                 "建议现在就改名为 `<主题>_<YYYYMMDD>.md`"
                 "（本条只提示不阻断：并行会话的在途文件不该互相拦截）")
    # 规则⑤（2026-10-10 第四轮 P1-4）：output_report/ 不得混入脚本。取舍与命名预检一致：
    # 跟踪件 FAIL、在途件 WARN —— 见 `_s16_script_hits()` 文档字符串。
    try:
        py_tracked, py_pend = _s16_script_hits()
    except RuntimeError as e:
        rep.fail("S16 报告命名规范", f"无法扫描 output_report/ 的脚本（{e}）—— 不当作「无脚本」放过")
        return
    for h in py_tracked:
        rep.fail("S16 报告命名规范",
                 f"{h} —— output_report/ 不得混入脚本（§8.13：产物目录不是代码目录）；"
                 "可复用 CLI → tools/，一次性 → logs/_tmp_*.py，审计证据脚本 → reports/（S5 豁免登记）")
    if py_pend:
        rep.warn("S16 报告命名规范",
                 f"{len(py_pend)} 个**未跟踪**（在途）脚本混在 output_report/，`git add` 后会转为 FAIL："
                 f"{py_pend}（本条只提示不阻断：并行会话的在途文件不该互相拦截）")
    # 规则⑥（2026-10-14 布局审计 §4）：docs/ 进命名面。取舍与①⑤一致 ——
    # 跟踪件 FAIL（进索引就是提交时刻）、在途件 WARN（不拦并行会话）。docs/ 无基线：
    # 实测当前跟踪面违规为 0（大写件只剩 3 个 README，已豁免；带杠日期 8 个全在 docs/plans/，已豁免），
    # 建基线等于给一个空债面留永久通道。
    try:
        docs_targets = _s16_docs_targets()
        docs_pend = _s16_docs_targets(others=True)
    except RuntimeError as e:
        rep.fail("S16 报告命名规范", f"无法取 docs/ 受控清单（{e}）—— 不当作「docs 全部合规」放过")
        docs_targets, docs_pend = [], []
    docs_viol = {rel: _docs_naming_violations(rel) for rel in docs_targets}
    docs_viol = {k: v for k, v in docs_viol.items() if v}
    for k, reasons in sorted(docs_viol.items()):
        rep.fail("S16 报告命名规范",
                 f"{k} —— docs/ 文档名违反 §8.13（{'、'.join(reasons)}）；"
                 "规范/SOP 改 snake_case 留在 docs/；**一次性结论报告**按 §8.13 归属迁 "
                 "`reports/<主题>_<YYYYMMDD>.md`（人工审计/复盘桶），别再混进规范目录")
    docs_pend_bad = sorted(rel for rel in docs_pend if _docs_naming_violations(rel))
    if docs_pend_bad:
        rep.warn("S16 报告命名规范",
                 f"{len(docs_pend_bad)} 个**未跟踪**（在途）docs/ 文档名违反 §8.13，"
                 f"`git add` 后会转为 FAIL：{docs_pend_bad[:6]}"
                 f"{'' if len(docs_pend_bad) <= 6 else ' …'}（只提示不阻断）")
    # 规则⑦（2026-10-14 布局审计 §6 规则⑦）：`reports/`+`output_report/` 的**一层子目录名**风格。
    # 起因：同一父目录里 5 个 kebab 与 4 个 snake 并存（`forum-experience` vs `dataset_experience`），
    # 而「找一份报告在哪个目录」本来就该是**一次确定**的事 —— 风格混用把它变成了两套猜。
    # 取舍与前几条一致：跟踪件 FAIL、在途件 WARN；存量 4 条进 `S16_DIR_LEGACY`（只登记不回改，
    # 理由逐条写在常量里，移出条件是「改名后旧路径 refs=0」而不是「看着不顺眼」）。
    try:
        dirs_tracked = _s16_dir_names()
        dirs_pend = [d for d in _s16_dir_names(others=True) if d not in dirs_tracked]
    except RuntimeError as e:
        rep.fail("S16 报告命名规范", f"无法取报告子目录清单（{e}）—— 不当作「目录风格全部合规」放过")
        dirs_tracked, dirs_pend = [], []
    dir_bad = [d for d in dirs_tracked
               if not _KEBAB_DIR_RE.match(d.split("/", 1)[1]) and d not in S16_DIR_LEGACY]
    for d in dir_bad:
        rep.fail("S16 报告命名规范",
                 f"子目录 `{d}/` 违反 §8.13「目录 = 小写 kebab-case」（规则⑦：同一父目录内不混用风格）；"
                 f"新建报告目录请用 kebab（`{d.split('/',1)[1].replace('_','-')}/`）。"
                 f"**别往 `S16_DIR_LEGACY` 里塞**：那 4 条是因为改名会造成活文档死指针才登记的，"
                 "新建目录没有历史包袱，没有登记理由")
    legacy_gone = [d for d in S16_DIR_LEGACY if not _s16_dir_on_disk(d)]
    if legacy_gone:
        rep.warn("S16 报告命名规范",
                 f"{len(legacy_gone)} 条 `S16_DIR_LEGACY` 登记已不在盘上：{legacy_gone}；"
                 "存量目录被改名或清空后请同步删掉条目 —— 留着就是一条**永久豁免通道**（同 S13/S11 的坑）")
    dir_pend_bad = [d for d in dirs_pend if not _KEBAB_DIR_RE.match(d.split("/", 1)[1])]
    if dir_pend_bad:
        rep.warn("S16 报告命名规范",
                 f"{len(dir_pend_bad)} 个**未跟踪**（在途）报告子目录名不是 kebab-case，"
                 f"`git add` 后会转为 FAIL：{dir_pend_bad}（只提示不阻断）")
    if (not new_ones and not carried and not pend and not py_tracked and not py_pend
            and not docs_viol and not docs_pend and not dir_bad and not dir_pend_bad
            # `legacy_gone` 一并入条件：否则同一闸会同时打出 `[OK] …存量登记 4 个` 与
            # `[WARN] 4 条登记已不在盘上` —— 本仓其余 WARN 项（carried/pend/docs_pend）都在此列，
            # 口径一致才有「看到 OK 就等于本闸全部评估且干净」这个读数契约。
            and not legacy_gone):
        rep.ok("S16 报告命名规范",
               f"{len(targets)} 个报告/产物文件名 + {len(docs_targets)} 个 docs/ 文档名全部符合 §8.13，"
               f"output_report/ 无脚本混入，报告子目录 {len(dirs_tracked)} 个风格一致"
               f"（kebab + 存量登记 {len(S16_DIR_LEGACY)} 个）")


#: S17：允许存在的顶层目录（2026-10-14 新增）。
#: 前半 = AGENTS.md §1 职责表声明的活跃目录；后半 = 运行期 / 宿主配置目录（gitignore 区，
#: 由 tools/retention.py 与各项目自身管理，不属结构治理面）。
#: ⚠ 这里刻意**不**用「§1 动态解析 + gitignore 推断」：S9 校的是「声明的在不在」，
#: 与本闸「不在名单的就不该存在」是相反方向，动态化只会让名单随文档措辞漂。
#: 新增顶层目录 = 先在 AGENTS.md §1 立项（写清职责与变更注意），再往这里加一行。
S17_TOP_DIR_ALLOWLIST = {
    # 源码与工具链
    "src", "tools", "tests", "world-quant-brain-mcp", "Claude",
    # 数据与业务
    "tracking", "research-data", "extensions", "data",
    # 文档与产物
    "docs", "reports", "output_report", "attic",
    # 运行期（gitignore）
    "cache", "logs", "results",
}
#: 点开头的目录一律放行：宿主配置（.claude/.clinerules/.qoder-cn/.workbuddy/.mcp 等）
#: 与各客户端自管，逐个登记会随宿主增减反复误红；VCS/解释器缓存也在这一类。
S17_DOT_DIRS_OK = True
#: 机器自生成目录（**非点开头**，但仍不是「模块」）：解释器/虚拟环境/包管理器随手重建，
#: 判 FAIL 只会让钩子永久变红而不指向任何可修的事实。实测反例：本闸首跑就因根 `__pycache__` FAIL
#: —— 任何在仓库根跑 python 的动作（含 pytest）都会把它建回来。
S17_MACHINE_DIRS = {"__pycache__", ".venv", ".venvs", "node_modules", ".cache"}


def check_s17_top_level_dirs(rep: Report) -> None:
    """S17：顶层目录必须已声明。

    起因（2026-10-14 结构审计）：仓库根出现一整棵 skills 树 `wq-brain-ra-usa/`（455 件，
    与 `Claude/skills/` 名单 100% 相同、内容零差异），**16 道闸一道都没报**——因为
    `check_s7_root_allowlist` 里是 `if p.is_dir(): continue`（无条件跳过所有目录，
    `ROOT_SKIP_DIRS` 形同虚设），而 S9 只校「已声明的目录在不在」、S10 只管区域子目录。
    即「未声明的顶层目录」是整套守护的结构性空白。

    危害不是观感：① 455 个文件只以未跟踪形态存在 = §7 禁止 `git clean` 的那类不可恢复债；
    ② 它是第二技能源，任何把 skill 搜索根指到仓库根的误操作（`WQ_SKILLS_DIR=.`）都会让它
    盖过规范源；③ `_skill_roots()` 从不解析 `repo_root/<skill-name>`，它零引用却能被误当在用。

    顶层目录出现名单外项 → FAIL，**不进基线**（同 S8/S11/S16 的取舍：这类问题没有合法存量形态）。

    **复发记录（守卫有效，缺的是执行）**：
    - 2026-10-14 首次：仓库根 `wq-brain-ra-usa/`（455 件）→ 本闸上线。
    - 2026-10-17 22:50 **第 3 次**：同一形态再现 466 件 / 6.1 MB。实跑本闸仍能拦
      （`S17_TOP_DIR_ALLOWLIST` 不含该名、判据取 `REPO_ROOT.iterdir()` **磁盘面**），
      说明**不是守卫缺口而是没人跑**——`tools/sync_skills.py` 只在自己的流程里工作，
      同步完不触发任何结构审计，问题滞留近一天才在布局快照里被发现。
      配套双修：① `sync_skills.py::_is_repo_root_or_ancestor` 扩为 `_is_repo_related`
      （增「子孙」判定，覆盖仓库内子目录这一形态）② `sync_skills.py` 同步成功后
      内联跑一次本闸逻辑，发现未声明顶层目录即顶屏告警。
    - 该副本已按 §7「归档而非删除」移入 `attic/sync_strays_20261018/`。
    """
    offenders = []
    machine_seen = []
    for p in sorted(REPO_ROOT.iterdir()):
        if not p.is_dir():
            continue
        if p.name in S17_MACHINE_DIRS:
            machine_seen.append(p.name)
            continue
        if p.name.startswith("."):
            if S17_DOT_DIRS_OK:
                continue
        if p.name in S17_TOP_DIR_ALLOWLIST:
            continue
        offenders.append(p.name)
    if offenders:
        rep.fail(
            "S17 顶层目录已声明",
            f"{len(offenders)} 个顶层目录不在 S17_TOP_DIR_ALLOWLIST：{offenders}；"
            "归属判据见 AGENTS.md §8.13（脚本→tools/，产物→output_report/，运行期→cache|logs|results/，"
            "归档→attic/<主题>_<YYYYMMDD>/）；确属新模块则先在 §1 职责表立项再登记白名单",
        )
    else:
        n = len([p for p in REPO_ROOT.iterdir()
                 if p.is_dir() and not p.name.startswith(".")
                 and p.name not in S17_MACHINE_DIRS])
        extra = f"（另跳过机器自生成目录 {machine_seen}）" if machine_seen else ""
        rep.ok("S17 顶层目录已声明", f"顶层 {n} 个目录全部已声明{extra}")


#: S18：`tracking/` 入库面的运行产物签名（2026-10-14 布局审计 §2.B-2 / §7 新增）。
#:
#: ⚠ **只按目录形态判，不按文件名判**。曾考虑用 `plan.json` / `score.json` /
#: `dispatch_spec.json` / `all_exprs.txt` / `variants_*.txt` 这套派发文件名做签名，
#: 实测 `tracking/` 索引面命中 93 件，其中 **4 件是合法业务件**：
#: `tracking/EUR/candidates/EUR_matrix_plan.json`、`tracking/KOR/candidates/kor_wave2_plan.json`、
#: `tracking/KOR/candidates/kor_wave3_plan.json`、`tracking/mining/field_inspect_hkg_continuation_score.json`。
#: 按文件名拦会把战役台账判成运行产物 —— 一次误红就没人再信这道闸。
#: 剩下的 89 件全部落在 `<名>_<YYYYMMDD>_<HHMM>` 形态的目录里，所以**目录签名既完备又不误伤**。
S18_RUN_DIR_RE = re.compile(r"^[^/]+_\d{8}(?:_\d{2,6})?$")
#: `.log` 是纯运行噪声（实测 9 个 `dispatch*.log` 早已被 .gitignore 挡住，
#: 这条留着是因为「被忽略」不等于「没入库」——历史上同类件一旦先被 `git add -f` 就永久留在索引）。
S18_LOG_SUFFIXES = (".log",)

#: S18 规则③：`tracking/` **顶层**（深度恰好 2 的跟踪件）允许的件。
#: 起因（2026-10-14 布局审计 §2.B-3 / §5 P1#7）：`brain-alpha-robustness` 让 agent 把
#: 稳健性归因报告**追加**到 `tracking/robustness_<YYYYMMDD>.md`，于是 7 份人工审计报告长期住在
#: 业务目录顶层（其中 5 份已入库）。它们的名字完全合规（S16 四条全过），
#: 但归属错了：§8.13 规定「人工审计与复盘 → `reports/<主题>_<YYYYMMDD>.md`」。
#: ⇒ **命名合规 ≠ 归属合规**，S16 看不见这件事，必须有一道闸校「`tracking/` 顶层是谁的目录」。
#: 白名单只放这一层的**基础设施件**，不放任何报告/产物：
#: `.gitignore` 与 `region_config.json` 是目录自身配置，`README.md` 是归属说明，
#: `MANIFEST.json` 是 §4「数据湖索引」既定落点（`generate_manifest.py` 写死 `tracking/MANIFEST.json`，
#: 本轮因 zip 副作用待用户裁决，先留位，生成时不必改闸）。
S18_TRACKING_TOP_ALLOWLIST = frozenset({
    ".gitignore", "README.md", "region_config.json", "MANIFEST.json",
})


def _s18_tracking_index_face() -> list:
    """`tracking/` 的**索引面**（含已暂存）。取不到就抛 —— 静默空集 = 本闸形同虚设
    （与 S14/S16/S20 同一口径：pre-commit 只拦 FAIL，闸失效必须响）。"""
    r = subprocess.run(["git", "ls-files", "-z", "--", "tracking"],
                       capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        raise RuntimeError(f"git ls-files rc={r.returncode}：{r.stderr.strip()[:200]}")
    return sorted(x for x in filter(None, r.stdout.split("\0")))


def check_s18_tracking_runtime_purity(rep: Report) -> None:
    """S18：`tracking/` 入库面不得含运行期产物（派发断点 / 日志），顶层不得含报告。

    三条判定（同一取面：`git ls-files -- tracking`）：
    ① 路径中间段命中 `<名>_<YYYYMMDD>[_<HHMM>]` ⇒ 时间戳运行目录；
    ② `*.log` ⇒ 运行噪声；
    ③ **深度恰好 2 的件**（`tracking/` 顶层）不在白名单 ⇒ 归属错位。

    起因一（2026-10-14 布局审计 §2.B-2）：`tools/verdict/perf_max.py` 的缺省 `plan_dir` 是
    `tracking/<region>/perfmax/<alpha_id>_<时间戳>/`，里面写的是 `plan.json`、`dispatch_spec*.json`、
    `score.json`、`all_exprs.txt`、`variants_*.txt` —— **续跑断点，不是结论**。旧缺省这样写了几天，
    实测把 **89 件**（30 `.json` + 59 `.txt`，9 个时间戳目录）送进了版本控制，
    位置还在业务目录 `tracking/USA/` 下，违反 AGENTS.md §8.13「运行期产物 → cache|logs|results」
    与 §5 规约 0「战役产物只入库、禁止当持久化目录用」。

    起因二（同日 §2.B-3 / §5 P1#7，规则③）：`brain-alpha-robustness` 把稳健性归因报告写成
    `tracking/robustness_<YYYYMMDD>.md`，7 份（5 份已入库）住业务目录顶层。
    **这七件的名字全都合规**（S16 四条全过）——所以 S16 结构性看不见，
    而 §8.13 的归属表要求人工审计在 `reports/`。本条把「归属」与「命名」拆成两件事来校。

    同日做的处置（本闸是最后一步）：① 缺省输出位改 `results/perfmax/<region>/`（已 gitignore）
    与 skill 的报告输出位改 `reports/`；② 存量 `git rm -r --cached` / `git mv`（**保盘不删**，
    §7「归档而非删除」；磁盘 98 件一件不少）；③ 本闸在**索引面**拦复发。

    判据取索引而非磁盘：违规的定义是「进了版本控制」；磁盘上被 gitignore 的时间戳目录是设计内。
    **FAIL 不进基线**（同 S8/S11/S17 的取舍：运行产物入库没有「合法存量」形态，
    本轮清完后索引面读数就是 0，留基线等于给下一次放行开门）。
    """
    try:
        face = _s18_tracking_index_face()
    except Exception as e:                      # 取不到清单不当作通过
        rep.fail("S18 tracking 产物纯度", f"无法取 `tracking/` 索引清单：{e}")
        return
    bad_dirs, bad_logs = [], []
    bad_top = []
    for rel in face:
        parts = rel.split("/")
        if len(parts) == 2 and parts[1] not in S18_TRACKING_TOP_ALLOWLIST:
            bad_top.append(rel)
        if any(S18_RUN_DIR_RE.match(d) for d in parts[1:-1]):
            bad_dirs.append(rel)
        elif rel.endswith(S18_LOG_SUFFIXES):
            bad_logs.append(rel)
    if bad_dirs or bad_logs or bad_top:
        seg = []
        if bad_dirs:
            dirs = sorted({"/".join(p.split("/")[:-1]) for p in bad_dirs})
            seg.append(f"{len(bad_dirs)} 件落在**时间戳运行目录**里，涉及 {len(dirs)} 个目录：{dirs[:4]}"
                       f"{' …' if len(dirs) > 4 else ''}")
        if bad_logs:
            seg.append(f"{len(bad_logs)} 件是 `.log`：{bad_logs[:4]}{' …' if len(bad_logs) > 4 else ''}")
        if bad_top:
            seg.append(
                f"{len(bad_top)} 件直接躺在 `tracking/` **顶层**：{bad_top[:4]}"
                f"{' …' if len(bad_top) > 4 else ''}"
                f"（该层只允许 {sorted(S18_TRACKING_TOP_ALLOWLIST)}）")
        rep.fail(
            "S18 tracking 产物纯度",
            "；".join(seg) +
            "。派发断点/日志属运行期产物，AGENTS.md §8.13 规定去处是 `results/`（续跑）、"
            "`cache/`（断点）、`logs/`（日志），不是 `tracking/<REGION>/`；"
            "**人工审计/复盘报告去处是 `reports/<主题>_<YYYYMMDD>.md`**，业务目录顶层不放报告"
            "（名字合规不等于归属合规，本条就是为这一区分加的）。"
            "修法：运行产物 `git rm -r --cached <目录>`（保盘，不是删除）+ 把写入方缺省输出位改到 "
            "`results/` 下（本轮已这样处理 `tools/verdict/perf_max.py`，新缺省 "
            "`results/perfmax/<region>/<alpha_id>_<时间戳>/`）；"
            "报告类 `git mv tracking/<名> reports/<名>` 并同步 `report_path` 与生成方 skill",
        )
    else:
        rep.ok("S18 tracking 产物纯度",
               f"tracking/ 索引面 {len(face)} 件，无时间戳运行目录、无 `.log`、"
               f"顶层除 {sorted(S18_TRACKING_TOP_ALLOWLIST)} 外无杂件")


def check_s20_index_worktree_consistency(rep: Report) -> None:
    """S20：索引里不得挂工作树已不存在的文件（未暂存删除）。

    起因（2026-10-14 同一轮审计）：`reports/ra_pipeline_stage_review_20260927/` 改名成
    `…_refs/` 时，新路径已 `git add` 入索引、旧路径的删除**没暂存** —— 索引同时挂着 23 件
    幽灵路径与 23 件新路径。后果不是脏，是**卡闸**：`_s16_targets()` 取面是 `git ls-files`
    （含已暂存），于是 S16 照扫旧路径下 9 个「缺日期」的 `.txt` 并 FAIL，
    而 pre-commit 跑在建提交对象之前 ⇒ 整条提交链被一个磁盘上根本不存在的路径拦住。
    实测本轮全仓未暂存删除恰好 25 件且 100% 落在 `reports/`（两组 23 + 2），
    同形态出现两次 ⇒ 按 §4 第 7 条固化为闸。

    修法一行：`git add -u -- <路径>`（只暂存删除与修改，不动文件内容、不损历史）。
    刻意不叫 `git add -A`：本仓禁止顺带把别人的未跟踪件拖进暂存面（§7 第 1/2 条）。
    """
    r = subprocess.run(["git", "ls-files", "-z", "--deleted"],
                       capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        # 拿不到清单就 FAIL：静默放过 = 本闸形同虚设（与 S16 的「取不到受控清单不当作通过」同口径）
        rep.fail("S20 索引↔工作树一致",
                 f"git ls-files --deleted 失败（rc={r.returncode}）：{r.stderr.strip()[:200]}")
        return
    deleted = sorted(x for x in filter(None, r.stdout.split("\0")))
    if deleted:
        sample = "；".join(deleted[:6])
        rep.fail(
            "S20 索引↔工作树一致",
            f"{len(deleted)} 个文件在索引里但工作树已不存在（删除未暂存，索引挂着幽灵路径）：{sample}"
            f"{' …' if len(deleted) > 6 else ''}；"
            "确认这些删除是有意的之后 `git add -u -- <路径>` 暂存即可（改名场景务必连旧路径一起暂存，"
            "否则 S16 一类按索引取面的闸会持续误红）",
        )
    else:
        rep.ok("S20 索引↔工作树一致", "索引无未暂存删除")


#: S21：约定**按全名识别**、因此本就没有扩展名的件（§6 规则⑤，2026-10-15 批次I 新增）。
#: 这类名字由工具链自己规定（make 找 `Makefile`、docker 找 `Dockerfile`），
#: 加扩展名等于让它们认不出来 —— 所以按**文件名**豁免，不按路径豁免。
S21_EXEMPT_NAMES = {
    "Makefile", "Dockerfile", "Containerfile",
    "LICENSE", "LICENCE", "NOTICE", "Vagrantfile", "Procfile",
}
#: S21：必须**按路径**豁免的件。git 只执行 `hooks/<精确名>`（本仓 `core.hooksPath`
#: = `tools/git-hooks`），改名即不执行。⚠ 这类条目**不能挪进 `S21_EXEMPT_NAMES`**：
#: 按名字豁免 `pre-commit` 等于给任何目录里的 `pre-commit` 开口子，
#: 而本仓要的豁免面只有那一个 hooks 目录（伞的半径必须等于事实的半径）。
S21_EXEMPT_PATHS = {
    "tools/git-hooks/pre-commit",
    "tools/git-hooks/commit-msg",
}


def check_s21_files_have_extension(rep: Report) -> None:
    """S21：全仓跟踪件必须有扩展名（点开头文件与两份白名单除外）。

    为什么单开一道（2026-10-15，同族于 §10.3 的「按扩展名取面的闸结构性失明」）：
    §6 规则⑤「文件必须有扩展名」此前**只在 `tools/` 顶层机械化**（S11 规则①），
    而 S11 取面是 `tools/*` 一层、S16/S18 取面又先按 `S16_SUFFIXES` 筛扩展名 ——
    三条合起来，对「仓库其余位置的无扩展名件」完全失明。

    反例不是假想，是本轮亲手抓到的 `tools/mcp_py`：一个无扩展名的 UTF-8 Python 脚本，
    因为名字里没有 `.`，**同时**躲过 S4（硬编码盘符）、S11、S14 与全仓 `*.py` 扫描，
    带着 `D:\\...` 绝对路径和一个已退役的 8876 端点长期躺在仓库里（2026-10-14 才
    改名 `tools/mcp_http_caller.py` 并修掉硬编码）。⇒ 一条只覆盖 1/N 个位置的命名规则
    不等于有规则；把它补到全跟踪面才是「机械口径」。

    判据形状（吸取 §10.10.6 的教训：**先定身份再写判据**）：
      ① 取面 = `git ls-files`（索引面，与 S16/S18/S20 同口径）；
      ② 「无扩展名」的定义 = **基名里不含 `.`**。这一条看着太简单，但它是对的写法：
         直觉写法 `Path(p).suffix == ""` 会把**每一个点开头文件**判成违规
         （实测 `PurePath(".gitignore").suffix == ""`、`".mcp.json"` 同），
         于是本闸首跑就会在 `.gitignore` 上永久误红 —— 与 S17 首跑被根 `__pycache__`
         纠正是同一类错误（判据拦的是工具约定的既有形态，不指向任何可修事实）。
         点开头件按定义就含 `.`，所以「含点即放过」天然覆盖它们，不需要额外豁免分支；
         它们的「扩展名」由全名承担（`.gitignore` 之于 git），本就不是本条要管的形态。
      ③ **无基线**：与 S16 docs 面、S17、S18 同一取舍 —— 实测当前违规 0 件
         （跟踪面 4107 件里只有 4 件无扩展名，且 4 件全在白名单），
         给空债面建基线 = 留一条永久豁免通道。
    """
    r = subprocess.run(["git", "ls-files", "-z"],
                       capture_output=True, text=True, cwd=str(REPO_ROOT))
    if r.returncode != 0:
        rep.fail("S21 跟踪件扩展名",
                 f"git ls-files 失败（rc={r.returncode}）：{r.stderr.strip()[:200]}")
        return
    face = [x.replace("\\", "/") for x in filter(None, r.stdout.split("\0"))]
    if not face:
        # 空面不当通过：与 S14/S16/S18/S20 同口径（取不到清单 = 闸这一轮根本没跑）
        rep.fail("S21 跟踪件扩展名", "git ls-files 返回空集：取不到跟踪面不等于没问题")
        return

    offenders, name_hits, path_hits = [], set(), set()
    for p in face:
        name = p.rsplit("/", 1)[-1]
        if "." in name:
            continue
        if name in S21_EXEMPT_NAMES:
            name_hits.add(name)
            continue
        if p in S21_EXEMPT_PATHS:
            path_hits.add(p)
            continue
        offenders.append(p)

    if offenders:
        sample = "、".join(offenders[:8])
        rep.fail(
            "S21 跟踪件扩展名",
            f"{len(offenders)} 个跟踪件没有扩展名：{sample}"
            f"{' …' if len(offenders) > 8 else ''}；"
            "无扩展名的脚本对 `file` 判定、语法高亮、全仓 `*.py` 扫描与 S4/S11/S14 一并失明"
            "（战例 `tools/mcp_py`）。修法 = 改名补扩展名并同步引用点"
            "（`tools/README.md` 登记名、S12 下架清单、活文档指针），**不是删除**",
        )
    else:
        rep.ok("S21 跟踪件扩展名",
               f"跟踪面 {len(face)} 件，无扩展名件全部落在白名单内"
               f"（名字豁免命中 {sorted(name_hits)}；路径豁免命中 {sorted(path_hits)}）")

    # 伞失效反查：白名单条目已不在索引 ⇒ 要求同步删除条目。
    # 只校**路径型**白名单：名字型（Makefile/Dockerfile…）是通用约定，
    # 本仓今天没有 `Procfile` 不代表以后不会有，不该据此判红或催删。
    gone = sorted(p for p in S21_EXEMPT_PATHS if p not in set(face))
    if gone:
        rep.warn("S21 跟踪件扩展名",
                 f"S21_EXEMPT_PATHS 有 {len(gone)} 项已不在索引：{gone}；"
                 "条目留着就是一条永久豁免通道（同 S13/S11 的坑），请一并删掉")


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
    "s16": ("S16 报告命名规范", check_s16_output_naming),
    "s17": ("S17 顶层目录已声明", check_s17_top_level_dirs),
    "s18": ("S18 tracking 产物纯度", check_s18_tracking_runtime_purity),
    "s20": ("S20 索引↔工作树一致", check_s20_index_worktree_consistency),
    "s21": ("S21 跟踪件扩展名", check_s21_files_have_extension),
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="仓库结构守护（只读）")
    ap.add_argument("--only", choices=sorted(CHECKS), action="append",
                    help="只跑指定检查（可重复）")
    ap.add_argument("--freeze-tools-top", action="store_true",
                    help="把当前 tools/ 顶层 .py 清单写进 S11 基线（建立/重置存量用）")
    ap.add_argument("--freeze-unregistered", action="store_true",
                    help="把当前「未在 tools/README.md 登记」的脚本清单写进 S14 基线（只登记存量欠债）")
    ap.add_argument("--freeze-naming", action="store_true",
                    help="把当前「违反 §8.13 命名规范」的报告/产物清单写进 S16 基线（存量不回改，只登记欠债）")
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

    if args.freeze_naming:
        import json

        p = REPO_ROOT / "tools" / "audit_structure_baseline.json"
        data = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
        names = sorted(k for k, v in
                       ((rel, _naming_violations(rel)) for rel in _s16_targets()) if v)
        data["s16_naming_violations"] = names
        data["_s16_note"] = (
            "S16 存量欠债：这些报告/产物文件名违反 AGENTS.md §8.13 命名规范"
            "（日期带杠 / 日期未作后缀 / 非 ASCII 或含空格），2026-10-08 冻结，"
            "按 §8.13「存量不强制回改」处理 → WARN 不阻塞。"
            "新件违规即 FAIL；改一个请从本表**移出**（移出即棘轮收紧）。"
        )
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[audit_structure] S16 基线已写入 {len(names)} 个命名违规文件 → {p.name}")
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
