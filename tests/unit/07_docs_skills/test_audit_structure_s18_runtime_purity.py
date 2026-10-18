# -*- coding: utf-8 -*-
"""test_audit_structure_s18_runtime_purity.py — S18「tracking/ 入库面不得含运行期产物」的守护。

为什么要这道闸（2026-10-14 布局审计 §2.B-2 / §7）
--------------------------------------------------
`tools/verdict/perf_max.py` 的缺省 `plan_dir` 曾是 `tracking/<region>/perfmax/<alpha_id>_<时间戳>/`。
那个目录里只有 `plan.json`、`dispatch_spec*.json`、`score.json`、`all_exprs.txt`、`variants_*.txt`
——**续跑断点，不是结论**。旧缺省写了几天，实测把 **89 件**（30 `.json` + 59 `.txt`，
9 个时间戳目录）送进版本控制，位置还在业务目录 `tracking/USA/` 下。

同日处置三件：① 缺省输出位改 `results/perfmax/<region>/`（已 gitignore，源头用例见
`tests/unit/10_toolkit_scripts/test_perf_max.py::test_plan_default_output_lands_in_results_not_tracking`）；
② 存量 `git rm -r --cached`（**保盘不删**，磁盘 98 件一件不少）；③ 本闸拦复发。

本文件测五件事，按重要性排序：
  1. **不误伤**（最难的一条）：签名只按**目录形态**。若改按 `plan.json`/`score.json` 这类文件名判，
     实测会把 4 个合法业务件判成运行产物（`candidates/EUR_matrix_plan.json`、
     `candidates/kor_wave2_plan.json`、`candidates/kor_wave3_plan.json`、
     `mining/field_inspect_hkg_continuation_score.json`）——一次误红就没人再信这道闸。
  2. **可红**：事故形态（时间戳目录 / `.log` / `tracking/` 顶层报告）确实 FAIL，且报错给得出修法。
  3. **fail-closed**：取不到索引清单不当作通过。
  4. **对真实仓库不空过**：本轮 89 件已出库 ⇒ 真仓库必须过闸，且磁盘件仍在（证明「出库 ≠ 删除」）。
  5. **生成方已止血**：闸只拦提交，不拦「文档还在教人往错地方写」。
     `brain-alpha-robustness` 的输出位必须已改 `reports/`（同 `test_perf_max.py` 对缺省 `plan_dir` 的守）。
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "audit_structure.py"


@pytest.fixture(scope="module")
def az():
    if not TOOL.is_file():
        pytest.skip("audit_structure.py 不存在")
    spec = importlib.util.spec_from_file_location("wqb_audit_s18", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["wqb_audit_s18"] = mod
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
    """伪造 `git ls-files -z -- tracking` 的输出。"""
    return lambda *a, **k: _Completed(stdout="\x00".join(paths) + "\x00")


# ── 注册（写了函数没挂进 CHECKS = 永不被执行）────────────────────────────
def test_s18_registered_in_checks(az):
    assert "s18" in az.CHECKS, "S18 未注册到 CHECKS"
    assert az.CHECKS["s18"][1] is az.check_s18_tracking_runtime_purity


# ── 1. 不误伤：业务件同名不同位 ────────────────────────────────────────
def test_s18_does_not_flag_business_artifacts_by_filename(az, monkeypatch):
    """4 个真实存在的合法件，名字全命中「派发套件文件名」，但不在时间戳目录里 ⇒ 必须过。

    这条用例是**先写失败再改设计**留下的：初版签名按文件名判，
    `tracking/EUR/candidates/EUR_matrix_plan.json` 立刻被误判。
    """
    legit = [
        "tracking/EUR/candidates/EUR_matrix_plan.json",
        "tracking/KOR/candidates/kor_wave2_plan.json",
        "tracking/KOR/candidates/kor_wave3_plan.json",
        "tracking/mining/field_inspect_hkg_continuation_score.json",
        "tracking/USA/config/settings.json",
    ]
    monkeypatch.setattr(az.subprocess, "run", _face(*legit))
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["OK"], rows.rows


# ── 2. 可红：事故形态 ──────────────────────────────────────────────────
def test_s18_flags_timestamped_runtime_dirs(az, monkeypatch):
    """2026-10-14 实测形态原样复现：perfmax/<alpha_id>_<YYYYMMDD>_<HHMMSS>/ 里的派发断点。"""
    bad = [
        "tracking/USA/perfmax/RR6bv6rz_20261008_092253/plan.json",
        "tracking/USA/perfmax/RR6bv6rz_20261008_092253/dispatch_spec.json",
        "tracking/USA/perfmax/RR6bv6rz_20261008_092253/variants_EQ_SP05.txt",
        "tracking/USA/robustness/NEU_IND_20261008_1525/score.json",
    ]
    monkeypatch.setattr(az.subprocess, "run", _face(*bad))
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["FAIL"]
    detail = rows.details("S18 tracking 产物纯度")[0]
    assert "4 件落在" in detail, detail
    assert "git rm -r --cached" in detail, "报错必须给得出修法（保盘出库，不是删除）"
    assert "results/" in detail, "报错必须指出正确去处"


def test_s18_flags_tracked_logs(az, monkeypatch):
    """.log 单独成条：它不需要时间戳目录也能判定是运行噪声。"""
    monkeypatch.setattr(az.subprocess, "run",
                        _face("tracking/KOR/results/harvest.log"))
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["FAIL"]
    assert "1 件是 `.log`" in rows.details("S18 tracking 产物纯度")[0]


def test_s18_run_dir_signature_accepts_minute_and_second(az):
    """签名同时认 `<名>_<YYYYMMDD>` 与 `<名>_<YYYYMMDD>_<HHMM[SS]>`（实测两种都在用）。"""
    for name in ("NEU_IND_20261008_1525", "RR6bv6rz_20261008_092253", "x_20261008"):
        assert az.S18_RUN_DIR_RE.match(name), name
    for name in ("candidates", "config", "20261008", "wave_2026", "reference"):
        assert not az.S18_RUN_DIR_RE.match(name), f"{name} 不该被判成运行目录"


# ── 2b. 规则③：`tracking/` 顶层不得放报告（名字合规 ≠ 归属合规）─────────
def test_s18_flags_report_at_tracking_top_level(az, monkeypatch):
    """2026-10-14 实测形态：`brain-alpha-robustness` 把归因报告追加到 `tracking/robustness_<日期>.md`。

    这七件**命名四条全过**（纯 ASCII、日期不带杠、日期作后缀），S16 结构性看不见；
    但 §8.13 规定人工审计在 `reports/<主题>_<YYYYMMDD>.md`，业务目录顶层不是它的去处。
    """
    monkeypatch.setattr(az.subprocess, "run",
                        _face("tracking/robustness_20261013.md", "tracking/README.md"))
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["FAIL"], rows.rows
    detail = rows.details("S18 tracking 产物纯度")[0]
    assert "tracking/robustness_20261013.md" in detail, detail
    assert "reports/" in detail, "报错必须点名正确归属"
    assert "git mv" in detail, "修法必须是不损历史的移动"


def test_s18_allows_infrastructure_files_at_tracking_top_level(az, monkeypatch):
    """白名单四件：目录自身配置 + 归属说明 + §4 既定的数据湖索引落点。

    `MANIFEST.json` 现在还不存在（生成有 zip 副作用，待用户裁决），留位是为了
    它落地时不必回头改闸 —— 白名单里允许一个尚未生成的件，比生成时被误红便宜。
    """
    legit = ["tracking/.gitignore", "tracking/README.md",
             "tracking/region_config.json", "tracking/MANIFEST.json"]
    monkeypatch.setattr(az.subprocess, "run", _face(*legit))
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["OK"], rows.rows


def test_s18_top_level_rule_is_depth_two_only(az, monkeypatch):
    """规则③只管 `tracking/` **顶层**：区域层以下同名报告（如 USA/robustness_x.md）不属本条，
    否则会把「区域目录里放区域结论」这类既有形态一并误伤。"""
    monkeypatch.setattr(az.subprocess, "run",
                        _face("tracking/KOR/reports/robustness_20261013.md"))
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["OK"], rows.rows


# ── 3. fail-closed ────────────────────────────────────────────────────
def test_s18_fails_closed_when_git_unavailable(az, monkeypatch):
    """取不到索引清单**不得**当作通过：静默空集 = 闸形同虚设（与 S14/S16/S20 同口径）。"""
    monkeypatch.setattr(az.subprocess, "run",
                        lambda *a, **k: _Completed(stderr="not a git repo", rc=128))
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["FAIL"], rows.rows


def test_s18_scope_is_the_tracking_pathspec(az, monkeypatch):
    """取面必须限定 `tracking`，否则 reports/ 的日期目录（合法）会被判成运行产物。"""
    seen = {}

    def spy(cmd, *a, **k):
        seen["cmd"] = list(cmd)
        return _Completed(stdout="")

    monkeypatch.setattr(az.subprocess, "run", spy)
    az.check_s18_tracking_runtime_purity(_Rows())
    assert "tracking" in seen["cmd"], seen["cmd"]


# ── 4. 对真实仓库：不空过 + 证明「出库 ≠ 删除」─────────────────────────
def test_s18_passes_on_this_repo(az):
    """本轮已把 89 件出库 ⇒ 真仓库必须过闸。不过 = 有人又把断点 commit 回来了。"""
    rows = _Rows()
    az.check_s18_tracking_runtime_purity(rows)
    assert rows.levels("S18 tracking 产物纯度") == ["OK"], (
        f"tracking/ 索引面又出现运行产物：{rows.details('S18 tracking 产物纯度')}")


def test_s18_untracking_kept_files_on_disk(az):
    """非空过：出库用的是 `git rm --cached`，磁盘件必须仍在。

    若这条红而上一条绿，说明断点被**删除**了（违反 AGENTS.md §7「归档而非删除」），
    而不是被出库 —— 两种形态在索引面上读数相同，只有磁盘能区分。
    """
    out = subprocess.run(["git", "ls-files", "-z", "--", "tracking"],
                         capture_output=True, text=True, cwd=str(REPO)).stdout
    assert out, "取不到 tracking/ 索引清单"
    disk = list((REPO / "tracking" / "USA" / "perfmax").rglob("dispatch_spec.json"))
    assert disk, (
        "tracking/USA/perfmax/ 下已无派发件：本仓约定是 `git rm --cached` 保盘出库，"
        "不是删除（§7）；若确要清理请进 attic/ 并在此登记")
    face = [x for x in filter(None, out.split("\0"))]
    assert not any("/perfmax/" in p or "/robustness/" in p for p in face), \
        "这些件仍在索引里，说明出库未生效"


# ── 5. 生成方止血：闸拦提交，拦不了「文档还指着旧位置」────────────────────
def test_robustness_skill_writes_reports_not_tracking():
    """`brain-alpha-robustness` 的报告输出位必须已改 `reports/`。

    与 `test_perf_max.py::test_plan_default_output_lands_in_results_not_tracking` 同一取舍：
    只清症状（把已入库的件搬走）而生成方还写着旧路径，下一轮稳健性审完就又长回来 ——
    本仓这类「搬完又长」已有 S12/S17 两个战例。历史说明行（带「布局审计」字样）允许提到旧路径。
    """
    skill = REPO / "Claude" / "skills" / "brain-alpha-robustness" / "SKILL.md"
    if not skill.is_file():
        pytest.skip("brain-alpha-robustness 不存在")
    text = skill.read_text(encoding="utf-8", errors="replace")
    assert "reports/robustness_" in text, "稳健性报告输出位未改到 reports/"
    bad = [ln.strip()[:90] for ln in text.splitlines()
           if "tracking/robustness" in ln and "布局审计" not in ln]
    assert not bad, f"skill 正文仍指示往 tracking/ 写报告：{bad}"


def test_robustness_skill_forbids_unwritten_report_path():
    """`report_path` 必须是**已落盘**件路径 —— 台账里 3 条死指针全是「先填路径后没写报告」。

    实测成因两种（2026-10-14 台账核对）：① EUR `mL617YPx` 填了 `robustness_20261011.md`，
    那份报告从未生成；② KOR `zq87zzqO` 自创逐 alpha 命名 `robustness_<alpha_id>_<日期>.md`，
    与 skill 现行的每日一份口径不一致，全盘无件。所以本条同时校「只写已落盘」与「别自创命名」。
    """
    skill = REPO / "Claude" / "skills" / "brain-alpha-robustness" / "SKILL.md"
    if not skill.is_file():
        pytest.skip("brain-alpha-robustness 不存在")
    text = skill.read_text(encoding="utf-8", errors="replace")
    assert "只写已落盘" in text, "skill 未约束 report_path 必须指向已落盘的报告"
    assert "MISSING" in text, "skill 未给出「报告确实没写」的替代写法（report_status）"

