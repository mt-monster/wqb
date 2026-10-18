# -*- coding: utf-8 -*-
"""test_audit_structure_s11_moved.py — S11「下沉数」必须是磁盘核验出来的，不是登记表说的。

为什么要改这个读数（2026-10-14 布局审计实施，reports/project_layout_audit_20261014.md §3/§9）
------------------------------------------------------------------------------------------
S11 的 docstring 里躺着一条战例：`ac2cf35` 号称「10 个 CLI 下沉」，实测是在子目录**新建**
（10 条 create mode、0 条 rename/delete），顶层一个没少。当时靠人工读 git log 才发现。
而旧读数写的是 `len(baseline) - len(now & baseline)` —— 它比战例更糟，是**反向失真**的：

  真下沉之后，本闸自己会提示「请同步从 audit_structure_baseline.json 移出」；
  一移出，`baseline - now & baseline` 立刻归零 ⇒ 打印「已下沉 0 个」。
  于是「迁了 23 个并把基线收紧」与「一个没迁」输出**一模一样**，进度不可见。

`_themes_moved_verified()` 把口径换成 **THEMES 登记表 ∩ 磁盘实核**（顶层少一个 且 子目录多一个
才算一个），登记与磁盘不符即 FAIL。2026-10-14 首跑实测：真下沉 23 个、名不副实 0 个。

本文件测三件事：① 核验函数对三种形态（真迁 / 顶层仍在 / 子目录没有）判定正确；
② 判定为不符时 `check_s11` 走 FAIL（不是 WARN——WARN 在 pre-commit 里不阻断，等于没闸）；
③ 对真实仓库不空过。
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s11_moved", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s11_moved"] = mod
    spec.loader.exec_module(mod)
    return mod


class _Rows:
    """收 Report 的行，便于按级别断言（不依赖 stdout 格式）。"""

    def __init__(self):
        self.rows = []

    def fail(self, check, detail):
        self.rows.append(("FAIL", check, detail))

    def warn(self, check, detail):
        self.rows.append(("WARN", check, detail))

    def ok(self, check, detail):
        self.rows.append(("OK", check, detail))


def _fake_tools(tmp_path, monkeypatch, az, *, moved_files, top_names=("a.py",), sub_names=("b.py",)):
    """造一棵假 tools/：顶层 `a.py`、主题目录 `x/<sub_names>`，THEMES 登记 `moved_files`。"""
    tools = tmp_path / "tools"
    (tools / "x").mkdir(parents=True)
    for n in top_names:
        (tools / n).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    for n in sub_names:
        (tools / "x" / n).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    themes = {"themes": {"x": {"dir": "tools/x", "files": ["a.py", "b.py"],
                               "moved_files": list(moved_files)}}}
    (tools / "THEMES.json").write_text(json.dumps(themes, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(az, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(az, "TOOLS", tools)
    return tools


def test_moved_verified_requires_both_halves(az, tmp_path, monkeypatch):
    """★ 真下沉 = 顶层少了 **且** 子目录有了。只满足一半都不算。"""
    _fake_tools(tmp_path, monkeypatch, az, moved_files=["b.py"])
    moved, bogus = az._themes_moved_verified()
    assert moved == 1 and bogus == [], f"真迁的那件没被计数：{moved} {bogus}"


def test_moved_verified_catches_created_not_moved(az, tmp_path, monkeypatch):
    """战例形态（子目录有、顶层**也有**）与登记名写错（两处都没有）都必须点名。"""
    _fake_tools(tmp_path, monkeypatch, az, moved_files=["a.py", "nope.py"])
    moved, bogus = az._themes_moved_verified()
    assert moved == 0
    assert len(bogus) == 2, bogus
    assert any("a.py" in b and "顶层仍在" in b for b in bogus), bogus
    assert any("nope.py" in b and "不存在" in b for b in bogus), bogus


def test_check_s11_fails_when_registration_lies(az, tmp_path, monkeypatch):
    """登记与磁盘不符 ⇒ FAIL。

    必须是 FAIL 不能是 WARN：pre-commit 只阻断 FAIL，WARN 等于把这条闸写成装饰
    （AGENTS.md §8.12 里 S6 的教训同一条：「被委托工具缺失也 FAIL，原先是 warn ⇒ 闸会静默消失」）。
    """
    _fake_tools(tmp_path, monkeypatch, az, moved_files=["a.py"])
    monkeypatch.setattr(az, "_s11_baseline", lambda: {"a.py"})
    rep = _Rows()
    az.check_s11_tools_top_frozen(rep)
    fails = [r for r in rep.rows if r[0] == "FAIL"]
    assert fails and "moved_files" in fails[0][2], rep.rows


def test_real_repo_moved_registration_is_honest(az):
    """真实仓库：登记的全部核验通过，且下沉数不是 0（防本闸被改成空过）。"""
    moved, bogus = az._themes_moved_verified()
    assert bogus == [], f"THEMES 登记了名不副实的下沉：{bogus}"
    assert moved >= 23, f"实测下沉数只增不减，现数 {moved} 低于 2026-10-14 的 23"


def test_db_theme_batch_actually_left_the_top_level(az):
    """2026-10-14 首批主题下沉（db）落地核对：顶层没了、`tools/db/` 有了。

    直接看磁盘而不是只看 `moved` 计数 —— 计数会被 THEMES 登记驱动，本条钉的是文件本身。
    """
    for name in ("db_lock_audit.py", "db_maintenance.py"):
        assert not (REPO / "tools" / name).exists(), f"tools/{name} 仍在顶层（下沉未完成）"
        assert (REPO / "tools" / "db" / name).is_file(), f"tools/db/{name} 不存在"
