# -*- coding: utf-8 -*-
"""test_audit_structure_s17_s20.py — S17「顶层目录已声明」与 S20「索引↔工作树一致」的守护测试。

为什么要有这两道闸（2026-10-14 结构审计）
------------------------------------------
**S17**：仓库根出现一整棵 skills 树 `wq-brain-ra-usa/`（455 件，与 `Claude/skills/`
名单 100% 相同、内容零差异），而**当时 16 道闸一道都没报**：

  - `check_s7_root_allowlist` 的循环体是 `if p.is_dir(): continue` —— 无条件跳过**所有**目录，
    连 `ROOT_SKIP_DIRS` 都没轮到判断（那行条件里的目录集合形同虚设）；
  - S9 校的是「文档声明的目录在不在」（反向），S10 只管 `tracking/<REGION>/` 子目录。

⇒ 「未声明的顶层目录」是整套结构守护的空白。危害不是观感：455 个文件只以未跟踪形态存在
= AGENTS.md §7 禁止 `git clean` 的那类不可恢复债；且它是第二技能源，任何把 skill 搜索根
指到仓库根的误操作都会让它盖过规范源（`_skill_roots()` 从不解析 `repo_root/<skill-name>`）。

**S20**：`reports/<主题>_<日期>/` 改名成 `…_refs/` 时只暂存了新路径，旧路径 25 件删除未暂存
⇒ 索引同时挂着幽灵路径与新路径。而 `_s16_targets()` 取面是 `git ls-files`（含已暂存），
S16 照扫旧路径下 9 个「缺日期」文件并 FAIL；pre-commit 跑在**建提交对象之前**扫的正是索引
⇒ 一个磁盘上根本不存在的路径卡住整条提交链。同形态实测出现两次（23 + 2），按 §4 第 7 条固化。

本文件测三件事：① 两闸都挂进 `CHECKS`（否则写了函数也没人跑，S13/S16 的同款守）；
② 判定逻辑正确（含 S17 首跑就暴露的 `__pycache__` 误红回归）；③ 对真实仓库不空过。
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
    spec = importlib.util.spec_from_file_location("wqb_audit_s17_s20", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s17_s20"] = mod
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

    def levels(self, check):
        return [lvl for lvl, name, _ in self.rows if name == check]

    def details(self, check):
        return [d for lvl, name, d in self.rows if name == check]

    @property
    def n_fail(self):
        return sum(1 for r in self.rows if r[0] == "FAIL")


# ── ① 注册（写了函数但没挂进 CHECKS = 永不被执行）────────────────────────
def test_s17_registered_in_checks(az):
    assert "s17" in az.CHECKS, "S17 未注册到 CHECKS"
    assert az.CHECKS["s17"][1] is az.check_s17_top_level_dirs


def test_s20_registered_in_checks(az):
    assert "s20" in az.CHECKS, "S20 未注册到 CHECKS"
    assert az.CHECKS["s20"][1] is az.check_s20_index_worktree_consistency


def test_s17_allowlist_covers_declared_dirs(az):
    """S17 白名单必须覆盖 AGENTS.md §1 声明的全部顶层目录。

    否则本闸会在一个干净仓库上永久变红（白名单与职责表打架 = 比没闸更糟，
    因为它逼人 `--no-verify`）。这里用 §1 的实际声明反查白名单，方向与 S9 相反。
    """
    agents = REPO / "AGENTS.md"
    if not agents.is_file():
        pytest.skip("AGENTS.md 不存在")
    import re
    text = agents.read_text(encoding="utf-8", errors="replace")
    sec = re.search(r"^## 1\..*?(?=^## 2\.)", text, re.S | re.M)
    body = sec.group(0) if sec else ""
    # §1 职责表第一列的反引号目录 token（`tracking/`、`src/wqb/` …）
    declared = {m.split("/")[0] for m in re.findall(r"\|\s*`([A-Za-z_][\w./-]*)/?\s*\|", body)}
    declared = {d for d in declared if d and not d.startswith(".")}
    missing = sorted(d for d in declared if d not in az.S17_TOP_DIR_ALLOWLIST)
    assert not missing, f"AGENTS.md §1 声明但不在 S17 白名单：{missing}（两边必须同步）"


# ── ② S17 判定：沙箱目录树（不碰真实仓库）──────────────────────────────
def _mk_root(tmp_path, names):
    for n in names:
        (tmp_path / n).mkdir()
    (tmp_path / "sentinel.py").write_text("", encoding="utf-8")  # 文件不参与 S17
    return tmp_path


def test_s17_flags_undeclared_top_dir(az, tmp_path, monkeypatch):
    """事故形态复现：根多出一个非点、非机器目录 → FAIL。"""
    monkeypatch.setattr(az, "REPO_ROOT", _mk_root(tmp_path, ["src", "tools", "wq-brain-ra-usa"]))
    rows = _Rows()
    az.check_s17_top_level_dirs(rows)
    assert rows.levels("S17 顶层目录已声明") == ["FAIL"]
    assert "wq-brain-ra-usa" in rows.details("S17 顶层目录已声明")[0]


def test_s17_passes_on_declared_tree(az, tmp_path, monkeypatch):
    monkeypatch.setattr(az, "REPO_ROOT", _mk_root(tmp_path, ["src", "tools", "docs", "attic"]))
    rows = _Rows()
    az.check_s17_top_level_dirs(rows)
    assert rows.n_fail == 0, rows.rows


def test_s17_skips_machine_dirs(az, tmp_path, monkeypatch):
    """回归（本闸首跑就踩的误红）：根 `__pycache__` 由解释器随手重建，不是模块。

    判它 FAIL ⇒ pre-commit 永久红且不指向任何可修的事实。
    """
    monkeypatch.setattr(az, "REPO_ROOT", _mk_root(tmp_path, ["src", "__pycache__", ".venv"]))
    rows = _Rows()
    az.check_s17_top_level_dirs(rows)
    assert rows.n_fail == 0, f"机器目录被误判：{rows.rows}"
    assert "__pycache__" in rows.details("S17 顶层目录已声明")[0]  # 跳过要说出来，不静默


def test_s17_dot_dirs_are_allowed(az, tmp_path, monkeypatch):
    """宿主配置目录（.claude/.clinerules/.qoder-cn…）逐个登记会随客户端增减反复误红。"""
    monkeypatch.setattr(az, "REPO_ROOT", _mk_root(tmp_path, ["src", ".claude", ".qoder-cn", ".git"]))
    rows = _Rows()
    az.check_s17_top_level_dirs(rows)
    assert rows.n_fail == 0, rows.rows


# ── ③ S20 判定：假 subprocess（不依赖沙箱 git）────────────────────────
class _Completed:
    def __init__(self, stdout="", stderr="", rc=0):
        self.stdout, self.stderr, self.returncode = stdout, stderr, rc


def test_s20_flags_unstaged_deletion(az, monkeypatch):
    """事故形态复现：改名只入新路径，旧路径删除未暂存 → 索引挂幽灵路径。"""
    ghost = ("reports/ra_pipeline_stage_review_20260927/dryrun_transcript.txt\x00"
             "reports/ra_pipeline_stage_review_20260927/realenv/realenv_transcript_n30.txt\x00")

    def fake_run(cmd, *a, **k):
        assert "--deleted" in cmd, cmd
        return _Completed(stdout=ghost)

    monkeypatch.setattr(az.subprocess, "run", fake_run)
    rows = _Rows()
    az.check_s20_index_worktree_consistency(rows)
    assert rows.levels("S20 索引↔工作树一致") == ["FAIL"]
    detail = rows.details("S20 索引↔工作树一致")[0]
    assert "2 个文件在索引里但工作树已不存在" in detail, detail
    assert "git add -u" in detail  # 报错必须给得出修法


def test_s20_ok_when_clean(az, monkeypatch):
    monkeypatch.setattr(az.subprocess, "run", lambda *a, **k: _Completed(stdout=""))
    rows = _Rows()
    az.check_s20_index_worktree_consistency(rows)
    assert rows.levels("S20 索引↔工作树一致") == ["OK"]


def test_s20_fails_closed_on_git_error(az, monkeypatch):
    """取不到清单**不得**当作通过（fail-open = 闸静默消失，与 S16 同口径）。"""
    monkeypatch.setattr(az.subprocess, "run", lambda *a, **k: _Completed(stderr="not a git repo", rc=128))
    rows = _Rows()
    az.check_s20_index_worktree_consistency(rows)
    assert rows.levels("S20 索引↔工作树一致") == ["FAIL"]
    assert "失败" in rows.details("S20 索引↔工作树一致")[0]


def test_s20_passes_on_this_repo(az):
    """真实仓库必须过 S20 —— 索引里挂幽灵路径本身就是待修事故。

    非空过时：把某件已跟踪文件从工作树删掉但不暂存，`test_s20_flags_unstaged_deletion`
    那条假 subprocess 用例覆盖不到「真 git 命令 + 真参数」这一层。
    """
    import subprocess
    out = subprocess.run(["git", "ls-files", "-z", "--deleted"],
                         capture_output=True, text=True, cwd=str(REPO)).stdout
    deleted = sorted(x for x in filter(None, out.split("\0")))
    rows = _Rows()
    az.check_s20_index_worktree_consistency(rows)
    if deleted:
        assert rows.levels("S20 索引↔工作树一致") == ["FAIL"], (
            f"索引有 {len(deleted)} 件未暂存删除却判过：{deleted[:5]}")
    else:
        assert rows.levels("S20 索引↔工作树一致") == ["OK"], rows.rows


def test_s17_passes_on_this_repo(az):
    """真实仓库的根必须过 S17（本次审计已把游离 skills 树归档，此处防复发）。"""
    rows = _Rows()
    az.check_s17_top_level_dirs(rows)
    assert rows.levels("S17 顶层目录已声明") == ["OK"], (
        "顶层出现未声明目录 —— 归属判据见 AGENTS.md §8.13")
