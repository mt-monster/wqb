# -*- coding: utf-8 -*-
"""test_audit_structure_s1.py — S1「sys.path 自举」的反向负例守护。

背景（2026-10-04 实事故）
------------------------
S1 长期误报 14 处，**阻塞 pre-commit 十余小时**。根因是检查器自身两个 bug 叠加：

  Bug A：`append` 分支只验 `f.attr == "append"`，**完全不验接收者是不是 sys.path**
         ⇒ 任何 `X.append(...)`（如 Markdown 文本拼装常见的 `L.append("")`）
            都会进入自举判定。实测 src/wqb/profiles/render.py 有 89 处命中。
  Bug B：`_is_self_bootstrap("")` 里 `Path("").resolve()` 返回 **CWD**，
         而审计在仓库根运行 ⇒ 空串被解析成仓库根，恰好 == `src_root.parent`
         ⇒ 被判为「自举注入」。

pre-commit 自己的提示语写着「如确认是存量误报请修检查器而非绕过」，
故本文件锁定「修检查器」这个方向，且**必须证明是收紧而非放宽**：
误报形态不得再出现，真违规形态必须仍被报出。

⚠ 性能：`check_s1_syspath` 每次调用全量扫 `src/`（102 文件 + AST，单次约 3 秒）。
故断言合并在**一次**调用内完成（沙箱内同时构造全部形态），另配一个不跑全量
的纯 AST 守卫用例——把本文件控制在数秒级，而不是每个用例各扫一遍。
"""
import ast
import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s1", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s1"] = mod
    spec.loader.exec_module(mod)
    return mod


class _Rep:
    def __init__(self):
        self.rows = []

    def ok(self, c, d): self.rows.append(("OK", c, d))
    def warn(self, c, d): self.rows.append(("WARN", c, d))
    def fail(self, c, d): self.rows.append(("FAIL", c, d))


def _write(root: Path, rel: str, body: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_s1_separates_real_bootstrap_from_false_positives(az, tmp_path, monkeypatch):
    """★ 一次调用覆盖全部形态——这是「修误报」与「放宽标准」的分水岭。

    沙箱 src/ 内同时放：误报形态、真违规形态、应放行的外部挂载与 sys 别名。
    若真违规那两条没被报出，本用例即红（说明标准被一起放宽了）。

    注：变量名启发式是 `\\b(src|repo_root|wqb_root|project_root)\\b`，而正则 `\\b`
    把下划线视作单词字符，故 `src_root` / `SRC_ROOT` 命名**不匹配**
    （`\\bsrc\\b` 要求 src 两侧是非单词字符）——这是启发式的既有局限，本次未改动，
    故正例改用能命中的 `repo_root`。
    """
    src = tmp_path / "src"
    parent_literal = str(src.resolve().parent)

    # 误报形态：非 sys.path 的 .append / 空串
    _write(tmp_path, "src/wqb/render_like.py",
           "def render():\n"
           "    L = []\n"
           "    L.append('')          # Bug A+B：曾被误判为自举\n"
           "    L.append('| a | b |')\n"
           "    lines = []\n"
           "    lines.append('x')\n"
           "    return L, lines\n")
    _write(tmp_path, "src/wqb/empty_arg.py", "import sys\nsys.path.insert(0, '')\n")

    # 真违规：把 src/ 的父目录挂上去
    _write(tmp_path, "src/wqb/bootstrap_literal.py",
           "import sys\n"
           f"sys.path.insert(0, {parent_literal!r})\n")
    _write(tmp_path, "src/wqb/bootstrap_varname.py",
           "import sys\n"
           "from pathlib import Path\n"
           "repo_root = Path(__file__).resolve().parents[1]\n"
           "sys.path.insert(0, str(repo_root))\n")

    # 应放行：外部挂载 + import sys as _sys 别名
    _write(tmp_path, "src/wqb/external_mount.py",
           "import sys\n"
           "from pathlib import Path\n"
           "tools_dir = Path(__file__).resolve().parents[2] / 'tools'\n"
           "sys.path.insert(0, str(tools_dir))\n")
    _write(tmp_path, "src/wqb/sys_alias.py",
           "import sys as _sys\n"
           "from pathlib import Path\n"
           "scripts_dir = Path(__file__).resolve().parents[2] / 'scripts'\n"
           "_sys.path.insert(0, str(scripts_dir))\n")

    monkeypatch.setattr(az, "SRC", src)
    # 报错文案用 `p.relative_to(REPO_ROOT)`，沙箱在仓库外会抛 ValueError，
    # 故一并把 REPO_ROOT 指到沙箱根（只影响报错文案，不影响判定）。
    monkeypatch.setattr(az, "REPO_ROOT", tmp_path)
    rep = _Rep()
    az.check_s1_syspath(rep)
    detail = [r[2] for r in rep.rows if r[0] == "FAIL" and "自举" in r[1]]

    assert any("bootstrap_literal" in d for d in detail), \
        f"路径字面量自举未被报出——标准被放宽了：{detail}"
    assert any("bootstrap_varname" in d for d in detail), \
        f"变量名自举未被报出——标准被放宽了：{detail}"
    for fp in ("render_like", "empty_arg"):
        assert not any(fp in d for d in detail), \
            f"{fp} 被误判为自举（Bug A/B 未修净）：{detail}"
    for okf in ("external_mount", "sys_alias"):
        assert not any(okf in d for d in detail), \
            f"{okf} 被误判为自举（外部挂载删了会直接坏）：{detail}"


def test_real_repo_has_no_false_positives(az):
    """★ 真实仓库：S1 自举必须为 0（这 14 处误报曾长期阻塞 pre-commit）。"""
    if not (REPO / "src" / "wqb").is_dir():
        pytest.skip("无 src/wqb")
    rep = _Rep()
    az.check_s1_syspath(rep)
    fails = [r for r in rep.rows if r[0] == "FAIL" and "自举" in r[1]]
    assert not fails, (
        f"S1 误报回归：{fails}（Bug A：未验接收者；Bug B：空串 Path('')==CWD）")


def test_bootstrap_guard_requires_sys_path_receiver():
    """★ 纯 AST 守卫（不跑全量扫描，秒级）——锁定 Bug A 的修复判据本身。"""
    def matches(src: str) -> bool:
        for node in ast.walk(ast.parse(src)):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            if (isinstance(f, ast.Attribute)
                    and f.attr in ("insert", "append")
                    and isinstance(f.value, ast.Attribute)
                    and f.value.attr == "path"
                    and isinstance(f.value.value, ast.Name)
                    and f.value.value.id.lstrip("_") == "sys"):
                return True
        return False

    for src in ("L.append('')", "lines.append('x')", "buf.path.insert(0, p)",
                "obj.path.append('a')"):
        assert not matches(src), f"{src} 不该进入自举判定（Bug A 未修净）"
    for src in ("sys.path.insert(0, p)", "sys.path.append(p)",
                "_sys.path.insert(0, p)", "_sys.path.append(p)"):
        assert matches(src), f"{src} 是真 sys.path 调用，被守卫漏掉了"