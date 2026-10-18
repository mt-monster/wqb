# -*- coding: utf-8 -*-
"""test_audit_structure_s21_extension.py — S21「全仓跟踪件必须有扩展名」的守护。

为什么补这道闸（2026-10-15 批次I，接 2026-10-14 布局审计 §6 规则⑤ / §10.3）
--------------------------------------------------------------------------
`§6 规则⑤ 文件必须有扩展名` 此前只在 **`tools/` 顶层**机械化（S11 规则①）。
而三条按扩展名取面的闸合起来对「其余位置的无扩展名件」完全失明：
S11 只看 `tools/*` 一层，S16/S18 先按 `S16_SUFFIXES` 筛。

反例是亲手抓到的 `tools/mcp_py`：一个无扩展名的 UTF-8 Python 脚本，因为基名里没有 `.`，
**同时**躲过 S4（硬编码盘符）/ S11 / S14 与全仓 `*.py` 扫描，带着 `D:\\...` 绝对路径
和一个已退役端点长期躺在仓库里。⇒ 规则只覆盖 1/N 个位置，就等于没有规则。

本文件测六件事，按重要性排序：
  1. **不误伤 dotfile**（最难的一条）：判据是「基名不含 `.`」而不是
     `Path(p).suffix == ""` —— 后者会把 `.gitignore` / `.mcp.json` 全判成违规，
     本闸就会永久误红。变异反查见
     `test_dotfile_names_are_exempt_and_that_line_is_load_bearing`。
  2. **可红**：无扩展名脚本确实 FAIL，且报错给得出「改名 + 同步引用、不是删除」。
  3. **白名单分型**：名字型豁免与路径型豁免不能互换 —— 把 `pre-commit` 放进名字型
     就等于给任何目录里的 `pre-commit` 开口子（伞半径必须等于事实半径）。
  4. **伞失效反查**：路径型白名单条目不在索引 ⇒ WARN 催删（同 S13/S11 的坑）。
  5. **fail-closed**：git 失败或取到空集都不算通过。
  6. **对真实仓库不空过**：真仓库必须过闸，且取面数量级对得上（≥3000），
     并核验白名单四件确实在盘上（防「豁免的是个不存在的幽灵路径」）。
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"
CHECK = "S21 跟踪件扩展名"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s21", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s21"] = mod
    spec.loader.exec_module(mod)
    return mod


class _Rows:
    def __init__(self):
        self.rows = []

    def fail(self, check, detail):
        self.rows.append(("FAIL", check, detail))

    def warn(self, check, detail):
        self.rows.append(("WARN", check, detail))

    def ok(self, check, detail):
        self.rows.append(("OK", check, detail))

    def levels(self, check):
        return [lvl for lvl, name, _ in self.rows if name == check]

    def details(self, check):
        return [d for lvl, name, d in self.rows if name == check]


class _Completed:
    def __init__(self, stdout="", stderr="", rc=0):
        self.stdout, self.stderr, self.returncode = stdout, stderr, rc


def _face(*paths):
    """伪造 `git ls-files -z` 的输出（整仓面，不带 pathspec）。"""
    return lambda *a, **k: _Completed(stdout="\x00".join(paths) + "\x00")


# ── 注册（写了函数没挂进 CHECKS = 永不被执行）────────────────────────────
def test_s21_registered_in_checks(az):
    assert "s21" in az.CHECKS, "S21 未注册到 CHECKS"
    assert az.CHECKS["s21"][1] is az.check_s21_files_have_extension


# ── 1. 不误伤：点开头件 + 两份白名单 ────────────────────────────────────
def test_s21_allows_dotfiles_and_whitelisted_names(az, monkeypatch):
    legit = [
        ".gitignore",
        ".mcp.json",
        "world-quant-brain-mcp/.env.example",
        "world-quant-brain-mcp/Makefile",
        "world-quant-brain-mcp/Dockerfile",
        "tools/git-hooks/pre-commit",
        "tools/git-hooks/commit-msg",
        "docs/README.md",
        "src/wqb/db_conn.py",
    ]
    monkeypatch.setattr(az.subprocess, "run", _face(*legit))
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert rows.levels(CHECK) == ["OK"], rows.rows


def test_s21_face_is_the_whole_index_not_a_pathspec(az, monkeypatch):
    """取面必须是**全仓** `git ls-files`（无 pathspec）。

    若有人把命令改成 `git ls-files -z -- tools`，本闸就退回 S11 的覆盖面，
    而 S11 已经在管 tools/ 顶层 —— 两条闸重复、仓库其余部分照旧失明。
    """
    seen = {}

    def spy(cmd, *a, **k):
        seen["cmd"] = list(cmd)
        return _Completed(stdout="a/b.py\x00")

    monkeypatch.setattr(az.subprocess, "run", spy)
    az.check_s21_files_have_extension(_Rows())
    assert seen["cmd"] == ["git", "ls-files", "-z"], seen["cmd"]


# ── 2. 可红：无扩展名脚本 ──────────────────────────────────────────────
def test_s21_flags_extensionless_tracked_script(az, monkeypatch):
    """`tools/mcp_py` 的真实形态：基名不含 `.`，也不以 `.` 开头 ⇒ FAIL。

    人造面里连上两个 hook 件，伞失效那条 WARN 就不出现，
    断言可以严格到「只有 FAIL 一条」。
    """
    face = ("tools/git-hooks/pre-commit", "tools/git-hooks/commit-msg",
            "docs/README.md", "tools/mcp_py", "tracking/KOR/notes")
    monkeypatch.setattr(az.subprocess, "run", _face(*face))
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert rows.levels(CHECK) == ["FAIL"], rows.rows
    detail = rows.details(CHECK)[0]
    assert "2 个跟踪件没有扩展名" in detail, detail
    assert "tools/mcp_py" in detail and "tracking/KOR/notes" in detail, detail
    assert "改名" in detail and "不是删除" in detail, "报错必须给出不损历史的修法"
    assert "mcp_py" in detail, "战例要点名，否则下一个人还会当它是观感问题"


def test_s21_exemption_kinds_are_not_interchangeable(az, monkeypatch):
    """路径型条目挪进名字型 ⇒ 该红的红不了；这条把「伞半径」写成一测。

    白名单里那两个 hook 件的豁免**只覆盖登记目录**；同一个基名出现在别处必须判红。
    （本用例的 face 故意不含那两个 hook 件，所以除了 FAIL 还会带一条伞失效 WARN，
    这里只断言 FAIL 语义与点名对象。）
    """
    assert "pre-commit" not in az.S21_EXEMPT_NAMES
    assert "tools/git-hooks/pre-commit" in az.S21_EXEMPT_PATHS
    monkeypatch.setattr(az.subprocess, "run",
                        _face("world-quant-brain-mcp/Makefile", "scripts/pre-commit"))
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert "FAIL" in rows.levels(CHECK), rows.rows
    detail = rows.details(CHECK)[0]
    assert "scripts/pre-commit" in detail, detail


# ── 4. 伞失效反查 ─────────────────────────────────────────────────────
def test_s21_warns_when_allowlisted_path_is_gone(az, monkeypatch):
    """白名单路径已从索引消失 ⇒ WARN 催删条目（留着就是永久豁免通道，同 S13/S11）。"""
    monkeypatch.setattr(az.subprocess, "run", _face("docs/README.md"))
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert rows.levels(CHECK) == ["OK", "WARN"], rows.rows
    detail = rows.details(CHECK)[-1]
    assert "S21_EXEMPT_PATHS" in detail and "永久豁免通道" in detail, detail


# ── 5. fail-closed ────────────────────────────────────────────────────
def test_s21_fails_closed_when_git_unavailable(az, monkeypatch):
    monkeypatch.setattr(az.subprocess, "run",
                        lambda *a, **k: _Completed(stderr="not a git repo", rc=128))
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert rows.levels(CHECK) == ["FAIL"], rows.rows


def test_s21_fails_closed_on_empty_face(az, monkeypatch):
    """空面 ≠ 通过：与 S14/S16/S18/S20 同口径。"""
    monkeypatch.setattr(az.subprocess, "run", lambda *a, **k: _Completed(stdout=""))
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert rows.levels(CHECK) == ["FAIL"], rows.rows
    assert "空集" in rows.details(CHECK)[0], rows.details(CHECK)


# ── 6. 对真实仓库：不空过 ─────────────────────────────────────────────
def test_s21_passes_on_this_repo_and_face_is_real_size(az):
    """真仓库必须过闸（违规 0），且取面数量级对得上。

    数量级断言是防「取面退化成半个目录」的那一半 —— 另一半见
    `test_s21_face_is_the_whole_index_not_a_pathspec`。
    """
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert rows.levels(CHECK) == ["OK"], rows.details(CHECK)
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True,
                         text=True, cwd=str(REPO)).stdout
    face = [x for x in filter(None, out.split("\0"))]
    assert len(face) >= 3000, f"跟踪面只有 {len(face)} 件，取面可疑"
    n_bad = [p for p in face
             if "." not in p.rsplit("/", 1)[-1]
             and not p.rsplit("/", 1)[-1].startswith(".")]
    assert set(n_bad) == set(az.S21_EXEMPT_PATHS) | {
        "world-quant-brain-mcp/Makefile", "world-quant-brain-mcp/Dockerfile"}, \
        f"无扩展名件名单变了，白名单要么过期要么漏登记：{sorted(n_bad)}"


def test_s21_allowlisted_paths_exist_on_disk(az):
    """豁免的必须是在用的真件，不是幽灵路径。"""
    for p in az.S21_EXEMPT_PATHS:
        assert (REPO / p).is_file(), f"S21_EXEMPT_PATHS 指向不存在的件：{p}"


# ── 变异反查：证明「含点即放过」那一行是**承重**的 ────────────────────────
def test_dotfile_names_are_exempt_and_that_line_is_load_bearing(az, monkeypatch):
    """同一份 dotfile 面：现状 OK；把 `if "." in name: continue` 改成不跳过即 FAIL。

    这条同时钉住两件容易写错的事（2026-10-15 批次I 亲手踩到，别再写回去）：
      ① 直觉判据 `Path(p).suffix == ""` 会把**每个点开头文件**判成违规
         （`PurePath(".gitignore").suffix` 是空串），本闸首跑就会在 `.gitignore` 上
         永久误红 —— 与 S17 首跑被根 `__pycache__` 纠正同一类错误；
      ② 因此**不需要**再写一条 `name.startswith(".")` 豁免分支：点开头件按定义含 `.`，
         「含点即放过」天然覆盖它们。一条永远走不到的分支不是防御，是给人读错的诱饵
         —— 本文件初版就写了那条，是变异用例把它抓出来的（变异后仍然 OK）。
    """
    dot_only = [".gitignore", ".mcp.json", ".env.example", "docs/.keep"]

    # 现状：dotfile 全放过 ⇒ OK
    monkeypatch.setattr(az.subprocess, "run", _face(*dot_only))
    rows = _Rows()
    az.check_s21_files_have_extension(rows)
    assert rows.levels(CHECK)[0] == "OK", rows.rows
    assert "4 件" in rows.details(CHECK)[0], rows.details(CHECK)

    src = Path(TOOL).read_text(encoding="utf-8")
    assert 'if name.startswith("."):' not in src.split("def check_s21_files_have_extension")[1], \
        "S21 里又出现了多余的 dotfile 豁免分支：含点即放过已覆盖，多余分支只会误导"

    needle = 'if "." in name:\n            continue'
    assert src.count(needle) == 1, f"判据行形态变了或被复制到别处（命中 {src.count(needle)} 次）"
    mutant_src = src.replace(needle, 'if False:\n            continue', 1)
    assert mutant_src != src, "变异没生效"
    # 变异件必须落在**仓库内**：audit_structure 的模块级 `_bootstrap_src()` 向上找
    # `pyproject.toml + src/wqb` 双标记，落在仓库外的 tmp_path 上会在 exec 时直接抛
    # 「仓库根未找到」。取 `logs/_tmp_*.py` —— §8.13 规定的一次性草稿位、gitignored、
    # 且不在 `test_db_write_guards` 的 SCAN_ROOTS（src/tools/4 个 skill 目录）里。
    if not (REPO / "logs").is_dir():
        pytest.skip("logs/ 不存在（本仓运行期目录，正常应在）")
    mutant = REPO / "logs" / "_tmp_s21_mutant_audit_structure.py"
    mutant.write_text(mutant_src, encoding="utf-8")
    spec2 = importlib.util.spec_from_file_location("wqb_audit_s21_mutant", mutant)
    mod2 = importlib.util.module_from_spec(spec2)
    sys.modules["wqb_audit_s21_mutant"] = mod2
    try:
        spec2.loader.exec_module(mod2)
        mod2.subprocess = type(sys)("fake_subprocess_for_mutant")
        mod2.subprocess.run = _face(*dot_only)
        rows2 = _Rows()
        mod2.check_s21_files_have_extension(rows2)
    finally:
        mutant.unlink(missing_ok=True)
        sys.modules.pop("wqb_audit_s21_mutant", None)
    assert rows2.levels(CHECK)[0] == "FAIL", (
        f"变异后仍不红 ⇒ 「含点即放过」不承重，或本用例写空了：{rows2.rows}")
    assert "4 个跟踪件没有扩展名" in rows2.details(CHECK)[0], rows2.details(CHECK)
