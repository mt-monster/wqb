# -*- coding: utf-8 -*-
"""test_audit_structure_s13.py — S13「tracking 非区域目录登记」的守护测试。

为什么要有 S13
--------------
`tracking/` 下混着区域目录与非区域目录。2026-10-14 实测：磁盘上 13 个区域目录 +
6 个非区域目录（`reference/`、`mining/`、`FORUM`、`prod_probe`、`hypotheses`、`_scratch`），
登记表里 7 项 —— 多出的 `PPA_USA` 是 PPA 战役的运行期产物目录，当前没开战役所以不在磁盘上
（见 `NON_REGION_DIRS_ALLOW_ABSENT`）。S10 靠 `^[A-Z]{3}$`
识别区域，于是 `FORUM`（5 字母）**恰好不匹配**才没被当成区域——这是隐式约定。
任何人新增一个 `FORUM2` / `TASK` / `TEMP` 之类的目录，只要字母数不对就永远
不会被 S10 提示，而 AGENTS.md §8.13 早已把「新 Agent 极易当成区域读」列为风险。

S13 把约定变成可执行：未登记的非区域目录 = FAIL。

⚠ 只读：全部用 tmp_path 沙箱，不动真实 tracking/。
"""
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
    spec = importlib.util.spec_from_file_location("wqb_audit_s13", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s13"] = mod
    spec.loader.exec_module(mod)
    return mod


class _Rep:
    """最小 Report 替身（只需 ok/warn/fail）。"""

    def __init__(self):
        self.rows = []

    def ok(self, check, detail): self.rows.append(("OK", check, detail))
    def warn(self, check, detail): self.rows.append(("WARN", check, detail))
    def fail(self, check, detail): self.rows.append(("FAIL", check, detail))


def _run(az, monkeypatch, tracking_dir: Path):
    monkeypatch.setattr(az, "REPO_ROOT", tracking_dir.parent)
    rep = _Rep()
    az.check_s13_tracking_nonregion_registry(rep)
    return rep.rows


def _mk(tmp_path: Path, names) -> Path:
    tr = tmp_path / "tracking"
    tr.mkdir()
    for n in names:
        (tr / n).mkdir()
    return tr


def test_real_repo_nonregion_dirs_are_all_registered(az):
    """★ 真实仓库的 tracking/ 下不得有未登记的非区域目录（现状须全绿）。"""
    if not (REPO / "tracking").is_dir():
        pytest.skip("无 tracking/")
    import re
    on_disk = {d.name for d in (REPO / "tracking").iterdir() if d.is_dir()}
    regions = {n for n in on_disk if re.match(r"^[A-Z]{3}$", n)}
    undeclared = sorted((on_disk - regions) - set(az.NON_REGION_DIRS))
    assert not undeclared, (
        f"tracking/ 下有未登记的非区域目录：{undeclared}——"
        f"必须登记到 audit_structure.NON_REGION_DIRS（AGENTS.md §8.13："
        f"再增非区域目录一律加 `_` 前缀），否则 S10 识别不到它")


def test_undeclared_nonregion_dir_fails(az, tmp_path, monkeypatch):
    """★ 核心负例：造一个未登记的 tracking/FORUM2 → 必须 FAIL。

    这是 S13 的全部价值所在，删掉登记项等于让检查失效，故必须有反向用例。
    """
    tr = _mk(tmp_path, ["EUR", "USA", "FORUM2"])
    rows = _run(az, monkeypatch, tr)
    fails = [r for r in rows if r[0] == "FAIL"]
    assert fails, f"未登记目录未被拦下：{rows}"
    assert any("FORUM2" in r[2] for r in fails)


def test_declared_dirs_pass(az, tmp_path, monkeypatch):
    """已登记的非区域目录不得报错。"""
    tr = _mk(tmp_path, ["EUR", "reference", "mining", "_scratch"])
    rows = _run(az, monkeypatch, tr)
    assert not [r for r in rows if r[0] == "FAIL"], rows


def test_stale_registry_entry_is_warn_not_fail(az, tmp_path, monkeypatch):
    """登记表里多一项磁盘上不存在的目录 → 只 WARN，不阻断（可清理，不阻塞）。"""
    tr = _mk(tmp_path, ["EUR"])
    monkeypatch.setitem(az.NON_REGION_DIRS, "__probe_missing__", "负例")
    try:
        rows = _run(az, monkeypatch, tr)
        assert not [r for r in rows if r[0] == "FAIL"], rows
        assert [r for r in rows if r[0] == "WARN"], rows
    finally:
        az.NON_REGION_DIRS.pop("__probe_missing__", None)


def test_region_code_named_nonregion_entry_fails(az, tmp_path, monkeypatch):
    """★ 自相矛盾登记：用三字母区域码命名却登记为非区域 → 必须 FAIL。"""
    tr = _mk(tmp_path, ["EUR", "XXX"])
    monkeypatch.setitem(az.NON_REGION_DIRS, "XXX", "负例：区域码形状的非区域")
    try:
        rows = _run(az, monkeypatch, tr)
        fails = [r for r in rows if r[0] == "FAIL"]
        assert fails, f"矛盾登记未被拦下：{rows}"
        assert any("XXX" in r[2] for r in fails)
    finally:
        az.NON_REGION_DIRS.pop("XXX", None)


def test_allow_absent_must_be_subset_of_registry(az):
    """`NON_REGION_DIRS_ALLOW_ABSENT` 里的名字必须同时在登记表里 —— 否则是个静默洞。

    这个集合的语义是「允许磁盘暂缺」，若有人往里加了个**未登记**的名字，
    S13 既不会 WARN 也不会 FAIL，而那正是「未登记目录」本该 FAIL 的形态。
    """
    holes = sorted(set(az.NON_REGION_DIRS_ALLOW_ABSENT) - set(az.NON_REGION_DIRS))
    assert not holes, f"ALLOW_ABSENT 里有未登记的名字（等于给它开了免检）：{holes}"


def test_allow_absent_entry_absent_from_disk_does_not_warn(az, tmp_path, monkeypatch):
    """按 WARN 提示去删登记表会把闸变陷阱：运行期目录暂缺必须**静音**。

    实测动因（2026-10-14）：S13 打的是「`PPA_USA` 磁盘已不存在，可从 NON_REGION_DIRS 清理」。
    但它只是 PPA 战役没开，产物已归档 `attic/ppa_mining_*`；谁真按提示删了登记，
    下次复跑 PPA 就长出 `tracking/PPA_USA/` ⇒ **FAIL 阻断提交**。
    """
    tr = _mk(tmp_path, ["EUR"])
    assert "PPA_USA" not in {p.name for p in tr.iterdir()}
    rows = _run(az, monkeypatch, tr)
    assert not [r for r in rows if r[0] == "WARN" and "PPA_USA" in r[2]], rows
    ok = [r for r in rows if r[0] == "OK"]
    assert ok and "PPA_USA" in ok[0][2], f"OK 读数必须说明为什么它不算 stale：{rows}"


def test_other_stale_entries_still_warn(az, tmp_path, monkeypatch):
    """静音只给白名单：其它登记项暂缺照旧 WARN（棘轮不能被整体放宽）。"""
    tr = _mk(tmp_path, ["EUR"])
    monkeypatch.setitem(az.NON_REGION_DIRS, "__probe_missing__", "负例：登记了但磁盘没有")
    try:
        rows = _run(az, monkeypatch, tr)
        assert [r for r in rows if r[0] == "WARN" and "__probe_missing__" in r[2]], rows
    finally:
        az.NON_REGION_DIRS.pop("__probe_missing__", None)


def test_s13_is_registered_in_checks(az):
    """S13 必须挂进 CHECKS，否则写了检查函数也没人跑。"""
    assert "s13" in az.CHECKS, "S13 未注册到 CHECKS"
    assert az.CHECKS["s13"][1] is az.check_s13_tracking_nonregion_registry


def test_registry_has_reason_for_each_entry(az):
    """每条登记都必须写明「为什么保留在这里」，否则登记表退化成黑名单。"""
    for name, why in az.NON_REGION_DIRS.items():
        assert why and len(why) >= 8, f"{name} 缺少保留理由"