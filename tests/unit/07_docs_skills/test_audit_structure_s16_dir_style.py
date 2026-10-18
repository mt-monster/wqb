# -*- coding: utf-8 -*-
"""test_audit_structure_s16_dir_style.py — S16 规则⑦：报告子目录名必须 kebab-case（存量只登记不回改）。

为什么补这一条（2026-10-14 布局审计批次G，`reports/project_layout_audit_20261014.md` §6 规则⑦）
----------------------------------------------------------------------------------------------
`reports/` 同一层里 5 个 kebab（`forum-experience`）与 4 个 snake（`dataset_experience`）并存。
「这份报告在哪个目录」本该是**一次确定**的事，风格混用把它变成两套猜。§8.13 早就定了
「目录 = 小写 kebab-case」，但**没有任何闸看过目录名** —— S16 此前的取面全是文件
（`_s16_targets()` 按扩展名筛 `.md/.json/...`），目录名对它结构性失明（同批次F 的 S11 数据件失明）。

⚠ 两个方向问题都在这轮撞上了，所以本文件既有**行为**用例也有**口径**用例：
  · 口径：`test_gate_direction_matches_agents_md` —— 本报告 §5 第 10 条建议「统一为 snake_case」，
    与 §8.13「目录 kebab」**相反**。裁决以 §8.13 为权威（§8.4 明写它是治理规约的权威源）。
    这条测试钉的是**方向**：下一个人若照报告那句建议把目录批量改成 snake，
    本闸会把他全部拦下 —— 于是必须先来改这条测试，改的时候就必然读到这段理由。
  · 行为：`test_toplevel_files_are_not_dirs` —— 本闸**首跑判红 255 条**的根因就是
    取面把顶层 `.md` 文件当成了子目录（`len(parts) < 2` 应为 `< 3`）。
    这条是那条事故的回归，不是装饰。

⚠ 只读：全部 monkeypatch，不动真实 `reports/`。
"""
import importlib.util
import re
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"
TITLE = "S16 报告命名规范"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s16_dir", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s16_dir"] = mod
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

    def levels(self, check=None):
        return [r[0] for r in self.rows if check is None or r[1] == check]

    def details(self, check=None):
        return [r[2] for r in self.rows if check is None or r[1] == check]


def _only_dir_face(az, monkeypatch, tracked, pending, *, targets=(), docs=(), gone=()):
    """把 S16 其余各面清空，只留规则⑦ 的目录面 —— 让 FAIL 归因唯一。

    `gone` = 假装**盘上已不存在**的存量登记项（缺省空 = 4 条伞都还在）。
    ⚠ 必须显式替换 `_s16_dir_on_disk`：它读真实磁盘，沙箱用例若不接管它，
    结果就随本机 `reports/` 的实际内容漂（第一版就是这么误把「真实盘上有没有」
    当成被测事实，三条用例一起红，而闸本身没错）。
    """
    monkeypatch.setattr(az, "_s16_targets", lambda: list(targets))
    monkeypatch.setattr(az, "_s16_untracked", lambda: [])
    monkeypatch.setattr(az, "_s16_script_hits", lambda: ([], []))
    monkeypatch.setattr(az, "_s16_docs_targets", lambda others=False: list(docs))
    monkeypatch.setattr(az, "_s16_baseline", lambda: set())
    monkeypatch.setattr(az, "_s16_dir_on_disk", lambda rel: rel not in set(gone))

    def names(others=False):
        return list(pending if others else tracked)

    monkeypatch.setattr(az, "_s16_dir_names", names)
    rows = _Rows()
    az.check_s16_output_naming(rows)
    return rows


# ---------------------------------------------------------------- 方向与存量
def test_gate_direction_matches_agents_md(az):
    """闸的判定方向必须与 §8.13 一致（kebab），而不是报告 §5 第 10 条那句「统一为 snake_case」。"""
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\*\*目录\*\*：小写 ([a-z-]+)", agents)
    assert m, "AGENTS.md §8.13 的目录命名规范条目被改写了对不上 —— 本测试的前提没了，先去修文档/本测试"
    declared = m.group(1).strip()
    assert declared == "kebab-case", f"§8.13 声明的目录风格是 {declared}，与闸假设为 kebab 不符"
    for name in ("forum_alpha_research", "dataset_experience"):
        assert not az._KEBAB_DIR_RE.match(name), f"{name} 应当被判为**不合规**（snake）"
    for name in ("forum-experience", "eur-mining", "gbr-campaign-final"):
        assert az._KEBAB_DIR_RE.match(name), f"{name} 应当合规"


def test_real_repo_dirs_are_all_kebab_or_registered(az):
    """真实仓库：一层子目录要么 kebab，要么在 `S16_DIR_LEGACY` 里带理由登记 —— 不得有第三种。"""
    tracked = az._s16_dir_names()
    assert tracked, "取面为空 = 本闸静默消失（fail-open），比没有闸更糟"
    stray = [d for d in tracked
             if not az._KEBAB_DIR_RE.match(d.split("/", 1)[1]) and d not in az.S16_DIR_LEGACY]
    assert not stray, f"未登记的不合规子目录：{stray}"
    legacy_on_disk = [d for d in az.S16_DIR_LEGACY if az._s16_dir_on_disk(d)]
    assert len(legacy_on_disk) == len(az.S16_DIR_LEGACY), (
        f"存量登记 {len(az.S16_DIR_LEGACY)} 条但盘上只有 {len(legacy_on_disk)} 条；"
        "条目留在表里就是一条永久豁免通道（同 S13/S11 的坑）")


def test_legacy_entries_carry_real_reasons(az):
    """每条存量登记都要写清「为什么单独改它会造事故」，不是「可以不改」。"""
    assert az.S16_DIR_LEGACY, "存量登记表被清空 —— 那 4 个目录还在盘上"
    for key, reason in az.S16_DIR_LEGACY.items():
        assert key.startswith(("reports/", "output_report/")), key
        assert len(reason) >= 20, f"{key} 的理由太短，写不出引用面就别登记：{reason}"
        assert re.search(r"refs|引用|死指针|生成器|校验|消歧|_refs", reason), \
            f"{key} 的理由没有给出**代价证据**（引用面 / 生成器 / 死指针）：{reason}"


# ---------------------------------------------------------------- 行为（非空过）
def test_new_snake_dir_fails(az, monkeypatch):
    rows = _only_dir_face(az, monkeypatch, ["reports/forum-experience", "reports/new_debt_dir"], [])
    assert rows.levels(TITLE) == ["FAIL"], rows.details(TITLE)
    detail = rows.details(TITLE)[0]
    assert "reports/new_debt_dir" in detail, detail
    assert "new-debt-dir" in detail, f"报错要点名合规写法：{detail}"
    assert "S16_DIR_LEGACY" in detail, f"必须警告「别拿存量表当豁免通道」：{detail}"


def test_toplevel_files_are_not_dirs(az, monkeypatch):
    """回归：顶层 .md 曾被当成子目录，本闸首跑因此判红 255 条。"""
    seen = {}

    def fake_run(cmd, *a, **k):
        seen["cmd"] = cmd

        class _R:
            returncode = 0
            stdout = ("reports/skills_review_20260929_closure.md\x00"
                      "reports/submit_report_20261006.md\x00"
                      "output_report/DEU_campaign_20261013.md\x00"
                      "reports/forum-experience/post_12345.md\x00")
            stderr = ""

        return _R()

    monkeypatch.setattr(az.subprocess, "run", fake_run)
    assert az._s16_dir_names() == ["reports/forum-experience"], "顶层文件被误判成目录（`< 3` 判据失效）"


def test_ghost_legacy_entry_is_warn_not_fail(az, monkeypatch):
    """登记项对应的目录已不在盘上 ⇒ WARN 提示移出，不 FAIL（存量表不能变成永久伞）。

    判据取**磁盘**而非 git 跟踪面（`_s16_dir_on_disk`）：用跟踪面会把「目录还在、
    只是里面暂时没跟踪件」误报成伞已失效，而这条 WARN 让人做的动作恰恰是**删条目**。
    """
    ghost = "reports/forum_alpha_research"
    rows = _only_dir_face(az, monkeypatch, ["reports/forum-experience"], [], gone=(ghost,))
    assert rows.levels(TITLE) == ["WARN"], rows.details(TITLE)
    warns = rows.details(TITLE)
    assert any("S16_DIR_LEGACY" in w for w in warns), warns
    assert any(ghost in w for w in warns), f"WARN 必须点名是哪条伞失效：{warns}"


def test_untracked_snake_dir_is_warn_only(az, monkeypatch):
    """并行会话刚 mkdir、还没 `git add` 的不合规目录：只提示不阻断（§7 不互相拦截）。"""
    rows = _only_dir_face(az, monkeypatch, ["reports/forum-experience"], ["reports/tmp_notes"])
    assert rows.levels(TITLE) == ["WARN"], rows.details(TITLE)
    assert "tmp_notes" in rows.details(TITLE)[0]


def test_fail_closed_on_git_error(az, monkeypatch):
    """取不到清单**不得**当作「目录风格全部合规」（与 S14/S16/S18/S20 同口径）。"""
    monkeypatch.setattr(az, "_s16_targets", lambda: [])
    monkeypatch.setattr(az, "_s16_untracked", lambda: [])
    monkeypatch.setattr(az, "_s16_script_hits", lambda: ([], []))
    monkeypatch.setattr(az, "_s16_docs_targets", lambda others=False: [])
    monkeypatch.setattr(az, "_s16_baseline", lambda: set())
    monkeypatch.setattr(az, "_s16_dir_on_disk", lambda rel: True)

    def boom(others=False):
        raise RuntimeError("git ls-files 失败（rc=128）：not a git repo")

    monkeypatch.setattr(az, "_s16_dir_names", boom)
    rows = _Rows()
    az.check_s16_output_naming(rows)
    assert rows.levels(TITLE)[:1] == ["FAIL"], rows.details(TITLE)
    assert any("不当作" in d for d in rows.details(TITLE)), rows.details(TITLE)


def test_ok_reading_names_the_dir_face(az, monkeypatch):
    """全合规时 OK 读数必须把目录面报出来 —— 只报文件面会让人以为目录根本没被看过。"""
    rows = _only_dir_face(az, monkeypatch, ["reports/forum-experience"], [])
    assert rows.levels(TITLE) == ["OK"], rows.details(TITLE)
    assert "子目录" in rows.details(TITLE)[0], rows.details(TITLE)
