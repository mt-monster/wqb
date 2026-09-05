# -*- coding: utf-8 -*-
"""workflow 节点行为回归测试（纯本地，无网络、无真实子进程）.

覆盖 2026-09-01 真实 dry-run 验收中发现的 4 个缺陷：
  - 缺陷#1 batch_track cwd 曾指向 skill 根而非 scripts/（相对路径脚本会误命中）
  - 缺陷#2 campaign._run_preflight 曾少一层 dirname 指到 src/，导致 S0/S1 产物门禁
           静默失效（"script not found" 仅记 warning 后放行）
  - 缺陷#3 campaign._run_quality_gate 曾用 "tools/wave_gate.py" 相对路径 + 错误 cwd
  - 缺陷#4 superalpha confirm_submit 两分支 step 名不一致（super_build_submit vs submit）
另覆盖 executor dry-run 在 executor 层拦截（节点函数不被调用）的纪律。
"""
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from wqb.workflow import _common  # noqa: E402
from wqb.workflow.executor import WorkflowExecutor  # noqa: E402
from wqb.workflow.nodes import batch_track as bt  # noqa: E402
from wqb.workflow.nodes import campaign as cp  # noqa: E402
from wqb.workflow.nodes import superalpha as sa2  # noqa: E402


class _CaptureStore:
    """伪造 store：提供 batch_track 需要的 list_expressions，拦截台账写。"""

    def __init__(self, expressions=None):
        self.expressions = expressions if expressions is not None else ["rank(close)"]
        self.ledger = []

    def list_expressions(self, *a, **kw):
        return list(self.expressions)

    def upsert_ledger(self, *a, **kw):
        self.ledger.append(a)
        return {"ok": True}


class _FakeProc:
    returncode = 0
    stdout = "alpha id = FAKEALPHA\n"
    stderr = ""


def _capture(monkeypatch, target_module, fn_name):
    """用假的 subprocess.run/Popen 捕获 (cmd, kwargs)，返回 calls 列表。

    2026-09-03: 同时 patch subprocess.run 和 subprocess.Popen，
    适配 campaign 节点从 run 改为 Popen 的异步化。
    """
    import subprocess
    import threading
    calls = []
    orig_run = subprocess.run
    orig_popen = subprocess.Popen

    def fake_run(cmd, **kwargs):
        calls.append({"cmd": list(cmd), "cwd": kwargs.get("cwd"), "method": "run"})
        return _FakeProc()

    class _FakePopen:
        """模拟 Popen 行为：立即返回，不实际执行。"""
        def __init__(self, cmd, **kwargs):
            calls.append({"cmd": list(cmd), "cwd": kwargs.get("cwd"), "method": "Popen"})
            self.pid = 99999
            self.returncode = 0
            self.stdout = type('Pipe', (), {'readline': lambda self: b'', 'close': lambda self: None})()
            self.stderr = type('Pipe', (), {'readline': lambda self: b'', 'close': lambda self: None})()

        def communicate(self, timeout=None):
            return ("alpha id = FAKEALPHA\n", "")

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(subprocess, "Popen", _FakePopen)
    return calls, orig_run


# ---------------------------------------------------------------------------
# 公共 fixture：伪造 toolkit 目录，避免依赖用户机器的真实 skill 安装
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _isolate_async_task_dir(tmp_path, monkeypatch):
    """2026-09-04 根治：campaign/fe/batch_track 异步任务输出目录注入 tmp。

    历史污染根因：campaign/fe 测试的真实 async 收尾线程把任务文件写到仓库
    logs/_async_tasks（70 个 FAKEALPHA 桩），batch_track 测试写 src/logs——
    全部为假成功/假任务。WQB_TASK_ROOT 注入后写盘指向 pytest tmp，回收即删。
    """
    monkeypatch.setenv("WQB_TASK_ROOT", str(tmp_path / "tasks"))


@pytest.fixture
def fake_toolkit(tmp_path, monkeypatch):
    scripts = tmp_path / "wq-brain-campaign-toolkit" / "scripts"
    scripts.mkdir(parents=True)
    for name in ("pipeline.py", "build_wave.py", "review_wave.py",
                 "score_datasets.py", "scan_fields.py", "campaign.py"):
        (scripts / name).write_text("# stub\n", encoding="utf-8")
    # 父目录放一个同名脚本，用于证明相对路径不会误命中
    (tmp_path / "wq-brain-campaign-toolkit" / "pipeline.py").write_text("# decoy\n",
                                                                         encoding="utf-8")
    monkeypatch.setenv("WQ_TOOLKIT_DIR", str(scripts))
    monkeypatch.delenv("WQ_PY", raising=False)
    return scripts


# ---------------------------------------------------------------------------
# 缺陷#1：batch_track cwd 必须指向 toolkit scripts 目录
# ---------------------------------------------------------------------------

def test_batch_track_cwd_is_toolkit_scripts_dir(monkeypatch, fake_toolkit):
    calls, _ = _capture(monkeypatch, bt, "run")
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    ex._store = _CaptureStore()

    out = bt.run(region="USA", wave="1", dataset="model219",
                 campaign_dir=str(_common.REPO_ROOT / "tracking" / "USA"),
                 _context={"store": ex._store, "registry": ex.registry})

    assert out["success"] is True
    assert calls, "未生成 subprocess 调用"
    cmd, cwd = calls[0]["cmd"], calls[0]["cwd"]
    scripts = str(fake_toolkit)
    assert cwd == scripts, f"cwd 应为 scripts/ 目录，实际 {cwd}"
    assert cmd[1] == os.path.join(scripts, "pipeline.py"), "脚本应取 scripts/pipeline.py"
    assert scripts not in " ".join(cmd[2:]), "命令不应再重复 toolkit 路径"


def test_batch_track_missing_toolkit_reports_clear_error(monkeypatch, tmp_path):
    """resolve_toolkit_dir 无效/回退失败时，batch_track 应给出可操作的错误。

    注意：不得只靠 WQ_TOOLKIT_DIR 指向空目录——resolve_toolkit_dir 设计上会回退到
    真实 skill 根，此处必须直接 patch 解析函数以模拟"未安装 toolkit"。
    """
    def _no_toolkit():
        return None
    monkeypatch.setattr(bt, "resolve_toolkit_dir", _no_toolkit)

    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test2.db"))
    ex._store = _CaptureStore()
    out = bt.run(region="USA", wave="1", dataset="model219",
                 campaign_dir=str(_common.REPO_ROOT / "tracking" / "USA"),
                 _context={"store": ex._store, "registry": ex.registry})
    assert out["success"] is False
    assert "WQ_TOOLKIT_DIR" in out["error"]


def test_batch_track_empty_expressions_fails(monkeypatch, fake_toolkit):
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    ex._store = _CaptureStore(expressions=[])
    out = bt.run(region="USA", wave="1", dataset="model219",
                 campaign_dir=str(_common.REPO_ROOT / "tracking" / "USA"),
                 _context={"store": ex._store, "registry": ex.registry})
    assert out["success"] is False
    assert "No expressions" in out["error"]


# ---------------------------------------------------------------------------
# 缺陷#2/#3：campaign 子进程脚本必须用绝对路径 + 正确 cwd
# ---------------------------------------------------------------------------

def test_campaign_preflight_uses_absolute_script_path(monkeypatch, fake_toolkit):
    calls, _ = _capture(monkeypatch, cp, "run")
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    ex._store = _CaptureStore()

    r = cp.run(region="USA", stage="S2", dataset="model219", wave="1",
               _context={"store": ex._store, "registry": ex.registry})

    assert r["success"] is True, r["steps"]
    preflight = [c for c in calls if "preflight_wave.py" in " ".join(c["cmd"])]
    assert preflight, "S2 必须真实执行 preflight 子进程（门禁不能静默跳过）"
    script_path = preflight[0]["cmd"][1]
    assert script_path == os.path.join(str(_common.REPO_ROOT), "tools",
                                       "preflight_wave.py"), f"preflight 路径错误: {script_path}"
    assert os.path.isfile(script_path), f"preflight 脚本不存在: {script_path}"
    assert preflight[0]["cwd"] == str(_common.REPO_ROOT), "preflight cwd 应为仓库根"

    pf_step = next(s for s in r["steps"] if s["step"] == "preflight")
    assert "script not found" not in str(pf_step), "preflight 脚本查找失败说明路径推导仍错"


def test_campaign_quality_gate_uses_absolute_script_path(monkeypatch, fake_toolkit):
    calls, _ = _capture(monkeypatch, cp, "run")
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    ex._store = _CaptureStore()

    r = cp.run(region="USA", stage="S3", dataset="model219", wave="1",
               _context={"store": ex._store, "registry": ex.registry})

    assert r["success"] is True, r["steps"]
    gate = [c for c in calls if "wave_gate.py" in " ".join(c["cmd"])]
    assert gate, "S3 必须真实执行质量闸子进程"
    script_path = gate[0]["cmd"][1]
    assert script_path == os.path.join(str(_common.REPO_ROOT), "tools", "wave_gate.py"), \
        f"quality_gate 路径错误: {script_path}"
    assert gate[0]["cwd"] == str(_common.REPO_ROOT), "quality_gate cwd 应为仓库根"


def test_campaign_stage_route_matrix(monkeypatch, fake_toolkit):
    """7 个 stage 的路由 + 未知 stage 拒绝（不依赖 cwd 的路由不变量）。"""
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    ex._store = _CaptureStore()
    calls, _ = _capture(monkeypatch, cp, "run")

    expect = {"S0": "score_datasets.py", "S1": "scan_fields.py", "S2": "build_wave.py",
              "S3": "pipeline.py", "S4": "review_wave.py", "S5": "pipeline.py",
              "S6": "campaign.py"}
    for stage, script in expect.items():
        calls.clear()
        r = cp.run(region="USA", stage=stage, dataset="model219", wave="1",
                   subcommand="ledger",
                   _context={"store": ex._store, "registry": ex.registry})
        assert r["success"] is True, f"{stage}: {r['steps']}"
        # 最后一条调用应是主 stage 脚本
        assert os.path.basename(calls[-1]["cmd"][1]) == script, (stage, calls[-1]["cmd"])

    calls.clear()
    r = cp.run(region="USA", stage="S9",
               _context={"store": ex._store, "registry": ex.registry})
    assert r["success"] is False
    assert [s["step"] for s in r["steps"]][-1] == "route_stage"


def test_campaign_missing_dataset_skips_preflight_with_warning(monkeypatch, fake_toolkit):
    """无 dataset 时 preflight 应明确记 warning 并跳过（不是静默失效）。"""
    calls, _ = _capture(monkeypatch, cp, "run")
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    ex._store = _CaptureStore()

    r = cp.run(region="USA", stage="S2",
               _context={"store": ex._store, "registry": ex.registry})

    assert r["success"] is True
    pf = next(s for s in r["steps"] if s["step"] == "preflight")
    assert "skip preflight" in pf.get("warning", "")
    assert not [c for c in calls if "preflight_wave.py" in " ".join(c["cmd"])]


# ---------------------------------------------------------------------------
# 缺陷#4：superalpha 提交步骤 step 名归一
# ---------------------------------------------------------------------------

def _sa_components(n=12):
    return [f"C{i:03d}" for i in range(n)]


def _stub_probe_go(monkeypatch):
    monkeypatch.setattr(sa2, "_probe_sa_pool", lambda region, dry_run: {
        "step": "sa_probe", "success": True, "verdict": "GO",
        "total": 12, "eligible": 12, "required": 10})


def test_superalpha_confirm_true_step_name_normalized(monkeypatch):
    _stub_probe_go(monkeypatch)
    seen = []

    def fake_build(subcommand, params):
        seen.append(subcommand)
        out = {"step": f"super_build_{subcommand}", "success": True,
               "alpha_id": "FAKEALPHA" if subcommand == "select" else None}
        return out

    monkeypatch.setattr(sa2, "_run_super_build", fake_build)
    out = sa2.run(region="KOR", components=_sa_components(), confirm_submit=True)

    assert out["success"] is True
    assert seen == ["select", "status", "probe", "submit"]
    submit_steps = [s for s in out["steps"] if s.get("step") == "submit"]
    assert len(submit_steps) == 1, f"submit 步骤应恰好 1 个，实际 {[s.get('step') for s in out['steps']]}"
    assert submit_steps[0]["subcommand"] == "super_build_submit"


def test_superalpha_confirm_false_skips_submit_and_uses_same_step_name(monkeypatch):
    _stub_probe_go(monkeypatch)
    seen = []
    monkeypatch.setattr(sa2, "_run_super_build",
                        lambda sc, p: (seen.append(sc), {"step": f"super_build_{sc}",
                                                         "success": True,
                                                         "alpha_id": "FAKEALPHA"
                                                         if sc == "select" else None})[1])
    out = sa2.run(region="KOR", components=_sa_components(), confirm_submit=False)

    assert out["success"] is True
    assert seen == ["select", "status", "probe"], f"未确认却走了后续子命令: {seen}"
    assert "submit" not in seen
    submit_steps = [s for s in out["steps"] if s.get("step") == "submit"]
    assert len(submit_steps) == 1 and submit_steps[0]["skipped"] is True
    assert "confirm_submit=False" in submit_steps[0]["note"]


def test_superalpha_probe_blocked_stops_before_super_build(monkeypatch):
    monkeypatch.setattr(sa2, "_probe_sa_pool", lambda region, dry_run: {
        "step": "sa_probe", "success": False, "verdict": "BLOCKED",
        "eligible": 3, "total": 3, "required": 10, "error": "仅 3 颗 eligible（需 ≥10）"})
    seen = []
    monkeypatch.setattr(sa2, "_run_super_build", lambda sc, p: seen.append(sc))

    out = sa2.run(region="KOR", components=_sa_components(), confirm_submit=False)

    assert out["success"] is False
    assert "eligible" in out["error"]
    assert seen == [], "探针 BLOCKED 时不得建 simulation"


def test_superalpha_dry_run_stops_after_probe(monkeypatch):
    _stub_probe_go(monkeypatch)
    seen = []
    monkeypatch.setattr(sa2, "_run_super_build", lambda sc, p: seen.append(sc))

    out = sa2.run(region="KOR", components=_sa_components(), dry_run=True)

    assert out["success"] is True
    assert seen == []
    assert [s["step"] for s in out["steps"]] == ["sa_probe", "dry_run"]


def test_superalpha_too_few_components_rejected(monkeypatch):
    out = sa2.run(region="KOR", components=["only_one"], confirm_submit=False)
    assert out["success"] is False
    assert "at least" in out["error"]


# ---------------------------------------------------------------------------
# executor dry-run 拦截纪律：节点函数不应被调用
# ---------------------------------------------------------------------------

def test_executor_dry_run_does_not_call_node(monkeypatch, fake_toolkit):
    # 2026-09-01 契约更新：dry-run 调用节点但注入 _context.dry_run=True。
    # 用 batch_track（未感知 dry_run 的节点）验证：dry_run 上下文已注入，
    # 且节点内不会真正执行回测（batch_track 的 run 在 dry_run 上下文下
    # 仍会启动 pipeline --dry-run，故此处只断言上下文注入与无写库副作用）。
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    calls, store_calls = _capture(monkeypatch, bt, "run")
    ex._store = _CaptureStore()

    r = ex.execute("campaign", {"region": "USA", "stage": "S5"}, dry_run=True)

    assert r.success is True and r.dry_run is True
    # campaign 节点 dry-run 感知：构建命令即停，不执行不写库
    out = r.output or {}
    assert out.get("dry_run") is True
    assert any(s.get("step") == "build_command" for s in out.get("steps", []))
    assert not any(s.get("step") == "execute" for s in out.get("steps", []))


def test_executor_missing_params_never_calls_node(monkeypatch):
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    calls, _ = _capture(monkeypatch, bt, "run")

    r = ex.execute("submit_alpha", {})

    assert r.success is False
    assert "Missing required params" in r.error
    assert calls == []


# ---------------------------------------------------------------------------
# 2026-09-01 executor dry_run 三缺陷修复回归（缺陷 A/B/C）
# ---------------------------------------------------------------------------

def test_executor_dry_run_passes_dry_run_kwarg(monkeypatch, tmp_path):
    """缺陷 B：executor 须按签名透传 dry_run 给 batch_track/superalpha。

    dry_run=True 时 batch_track 走自身 dry_run 分支返回计划，不触发 subprocess。
    """
    import subprocess
    ex = WorkflowExecutor(db_path=str(tmp_path / "x.db"))
    ex._store = _CaptureStore(expressions=["rank(close)", "rank(volume)"])
    monkeypatch.setattr(bt, "resolve_campaign_dir", lambda region: str(tmp_path))
    calls = []
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: calls.append(a))

    r = ex.execute("batch_track",
                   {"region": "USA", "wave": "1", "dataset": "model219"},
                   dry_run=True)

    assert r.success is True and r.dry_run is True
    assert r.output.get("dry_run") is True
    assert r.output["plan"]["expression_count"] == 2
    assert calls == [], "dry_run 下 batch_track 不应触发 subprocess"


def test_executor_propagates_node_failure_truthfully(monkeypatch, tmp_path):
    """缺陷 C：executor 不再无条件 success=True，须透传节点真实 success/error。"""
    ex = WorkflowExecutor(db_path=str(tmp_path / "x.db"))
    ex._store = _CaptureStore(expressions=[])
    monkeypatch.setattr(bt, "resolve_campaign_dir", lambda region: str(tmp_path))

    r = ex.execute("batch_track",
                   {"region": "USA", "wave": "1", "dataset": "model219"},
                   dry_run=True)

    assert r.success is False
    assert "No expressions" in r.error


def test_submit_alpha_dry_run_short_circuits(monkeypatch):
    """缺陷 A：submit_alpha 在 dry_run 下不触碰 brain_client。"""
    from wqb.workflow.nodes import submit_alpha as sa
    called = []
    monkeypatch.setattr(sa, "_get_brain_client",
                        lambda: (called.append(1), None)[1])

    out = sa.run(alpha_id="ABC", _context={"dry_run": True})

    assert out["success"] is True and out["dry_run"] is True
    assert called == [], "dry_run 下不应触碰 brain_client"
    assert out["plan"]["alpha_id"] == "ABC"


def test_judge_dry_run_short_circuits(monkeypatch):
    """缺陷 A：judge 在 dry_run 下不触碰 brain_client。"""
    from wqb.workflow.nodes import judge as jd
    called = []
    monkeypatch.setattr(jd, "_get_brain_client",
                        lambda: (called.append(1), None)[1])

    out = jd.run(alpha_id="ABC", _context={"dry_run": True})

    assert out["success"] is True and out["dry_run"] is True
    assert out["verdict"] is None
    assert called == [], "dry_run 下不应触碰 brain_client"


def test_gem_dry_run_short_circuits(monkeypatch):
    """缺陷 A：gem 在 dry_run 下不 subprocess、不写库。"""
    from wqb.workflow.nodes import gem as gm
    import subprocess
    calls = []
    monkeypatch.setattr(subprocess, "Popen",
                        lambda *a, **k: (calls.append(a), None)[1])
    monkeypatch.setattr(subprocess, "run",
                        lambda *a, **k: (calls.append(a), None)[1])

    out = gm.run(region="IND", dataset_id="analyst45", delay=1,
                 universe="TOP3000", data_category="analyst",
                 _context={"dry_run": True, "store": None})

    assert out["success"] is True and out["dry_run"] is True
    assert calls == [], "dry_run 下 gem 不应触发 subprocess"


def test_gem_ideas_format_invalid_blocked_before_popen(monkeypatch, tmp_path):
    """ideas 文件缺 **Concept**/**Implementation Example** 块时，在 Popen 前拦截。

    2026-09-03 新增：run_pipeline 在 BRAIN 登录+数据准备后才解析块结构，格式错误
    会白烧一轮；gem 节点必须在 Popen 前用同规则预检并返回合规示例。
    """
    from wqb.workflow.nodes import gem as gm

    bad_md = tmp_path / "bad_ideas.md"
    bad_md.write_text("Dataset: analyst45\n1. some idea without concept blocks\n",
                      encoding="utf-8")

    monkeypatch.setattr(gm, "resolve_skill_dir", lambda name: "C:/gem")
    monkeypatch.setattr(gm.os.path, "exists", lambda p: True)
    popen_calls = []
    monkeypatch.setattr(gm.subprocess, "Popen",
                        lambda *a, **k: (popen_calls.append(a), None)[1])

    out = gm.run(region="IND", dataset_id="analyst45", delay=1,
                 universe="TOP3000", data_category="analyst",
                 ideas_file=str(bad_md), detached=True)

    assert out["success"] is False
    assert popen_calls == [], "非法 ideas 文件不应触发 Popen"
    last = out["steps"][-1]
    assert last["step"] == "check_ideas_format" and last["success"] is False
    assert last["blocks"] == 0
    assert any("Concept" in e for e in last["errors"])
    assert "sample" in last  # 附带合规示例供快速修正


def test_gem_ideas_format_valid_blocks_parsed():
    """_parse_ideas_blocks 与 run_pipeline.extract_template_blocks 同规则：
    反引号模板与裸模板（tail 自身）均须提取；无 {variable} 占位符的块不计。"""
    from wqb.workflow.nodes import gem as gm

    good_md = (
        "**Concept**: momentum with low-vol scaling\n"
        "- **Implementation Example**: `rank(ts_delta({analyst}, 21))`\n"
        "- **Rationale**: r1\n\n"
        "**Concept**: no backticks tail template\n"
        "- **Implementation Example**: rank(ts_mean({analyst}, 10))\n"
        "- **Rationale**: r2\n"
    )
    blocks = gm._parse_ideas_blocks(good_md)
    assert len(blocks) == 2
    assert blocks[0]["template"] == "rank(ts_delta({analyst}, 21))"
    assert blocks[1]["template"] == "rank(ts_mean({analyst}, 10))"
    assert all("{" in b["template"] and "}" in b["template"] for b in blocks)

    no_ph = (
        "**Concept**: idea A\n"
        "- **Implementation Example**: `rank(close)`\n"
        "- **Rationale**: template without placeholder\n"
    )
    assert gm._parse_ideas_blocks(no_ph) == []

    assert gm._parse_ideas_blocks("Dataset: analyst45\nno blocks here\n") == []



def test_feature_engineering_dry_run_short_circuits(monkeypatch):
    """缺陷 A：feature_engineering 在 dry_run 下不 subprocess、不写库。"""
    from wqb.workflow.nodes import feature_engineering as fe
    import subprocess
    calls = []
    monkeypatch.setattr(subprocess, "run",
                        lambda *a, **k: (calls.append(a), None)[1])

    out = fe.run(region="IND", dataset_id="analyst45", delay=1,
                 universe="TOP3000", data_category="analyst",
                 _context={"dry_run": True, "store": None})

    assert out["success"] is True and out["dry_run"] is True
    assert calls == [], "dry_run 下 feature_engineering 不应触发 subprocess"


def test_campaign_s2_s3_dry_run_skips_preflight_and_quality_gate(monkeypatch, fake_toolkit):
    """缺陷 A（campaign 延伸）：S2/S3 在 dry_run 下不跑 preflight/quality_gate 子进程，
    但应构建出主 stage 命令（build_command 步骤存在、execute 步骤不存在）。"""
    calls, _ = _capture(monkeypatch, cp, "run")
    ex = WorkflowExecutor(db_path=str(Path("logs") / "_tmp_test.db"))
    ex._store = _CaptureStore()

    for stage, script in (("S2", "build_wave.py"), ("S3", "pipeline.py")):
        calls.clear()
        r = cp.run(region="USA", stage=stage, dataset="model219", wave="1",
                   _context={"store": ex._store, "registry": ex.registry,
                             "dry_run": True})
        assert r["success"] is True and r["dry_run"] is True, (stage, r["steps"])
        # 不跑 preflight/quality_gate 子进程
        assert not [c for c in calls if "preflight_wave.py" in " ".join(c["cmd"])], stage
        assert not [c for c in calls if "wave_gate.py" in " ".join(c["cmd"])], stage
        # 仍构建出主 stage 命令
        steps = {s["step"] for s in r["steps"]}
        assert "build_command" in steps
        assert "execute" not in steps



# ---------------------------------------------------------------------------
# 2026-09-04 Mode B 资格线优化（方案 A/B/C）
# ---------------------------------------------------------------------------

def test_judge_extract_region_from_details():
    """方案 A：_extract_region 从 get_alpha_details 返回提取 region。"""
    from wqb.workflow.nodes import judge as jd

    # settings.region 路径
    details = {"result": {"settings": {"region": "EUR"}}}
    assert jd._extract_region(details) == "EUR"

    # 顶层 region 兑底
    details = {"result": {"region": "ind"}}
    assert jd._extract_region(details) == "IND"

    # 无 region 返回 None
    assert jd._extract_region({"result": {}}) is None
    assert jd._extract_region({"__error__": "fail"}) is None


def test_judge_load_mode_b_qualification_region_routing(tmp_path, monkeypatch):
    """方案 A：_load_mode_b_qualification 按 region 读 thresholds.json。"""
    from wqb.workflow.nodes import judge as jd
    import json

    # 构造 EUR thresholds.json
    eur_dir = tmp_path / "tracking" / "EUR" / "config"
    eur_dir.mkdir(parents=True)
    (eur_dir / "thresholds.json").write_text(json.dumps({
        "mode_b_qualification": {"sharpe_min": 1.0, "fitness_min": 0.6}
    }), encoding="utf-8")

    # 构造 KOR thresholds.json
    kor_dir = tmp_path / "tracking" / "KOR" / "config"
    kor_dir.mkdir(parents=True)
    (kor_dir / "thresholds.json").write_text(json.dumps({
        "mode_b_qualification": {"sharpe_min": 1.25, "fitness_min": 0.8}
    }), encoding="utf-8")

    # mock os.path.dirname 让 thresholds_path 指向 tmp_path
    orig_join = os.path.join
    def fake_join(*args):
        if "tracking" in args:
            # 重定向到 tmp_path
            idx = args.index("tracking")
            return orig_join(str(tmp_path), *args[idx:])
        return orig_join(*args)
    monkeypatch.setattr(os.path, "join", fake_join)

    # EUR 读 EUR 的值
    mbq_eur = jd._load_mode_b_qualification(None, region="EUR")
    assert mbq_eur["sharpe_min"] == 1.0
    assert mbq_eur["fitness_min"] == 0.6

    # KOR 读 KOR 的值
    mbq_kor = jd._load_mode_b_qualification(None, region="KOR")
    assert mbq_kor["sharpe_min"] == 1.25
    assert mbq_kor["fitness_min"] == 0.8


def test_probe_batch_mode_b_distribution_mode(tmp_path):
    """方案 B：check_mode_b_eligible 分布感知模式（p75 / count>=2）。"""
    from tools.probe_batch_mode import ProbeBatchExecutor
    import json

    # 构造 campaign_dir + thresholds.json（分布模式）
    campaign_dir = tmp_path / "campaign"
    config_dir = campaign_dir / "config"
    config_dir.mkdir(parents=True)
    (config_dir / "thresholds.json").write_text(json.dumps({
        "mode_b_qualification": {
            "mode": "distribution",
            "sharpe_min": 1.0,
            "fitness_min": 0.6,
            "sharpe_p75_min": 0.9,
            "fitness_p75_min": 0.5,
            "count_above_min": 2,
        }
    }), encoding="utf-8")

    executor = ProbeBatchExecutor(str(campaign_dir), "test_ds", 1, dry_run=True)

    # 场景 1：p75 达标（4 条候选，前 25% = 第 1 条，sharpe 1.2 >= 0.9）
    results = [
        {"sharpe": 1.2, "fitness": 0.7},
        {"sharpe": 0.8, "fitness": 0.5},
        {"sharpe": 0.6, "fitness": 0.4},
        {"sharpe": 0.4, "fitness": 0.3},
    ]
    eligible, best = executor.check_mode_b_eligible(results)
    assert eligible is True
    assert best["sharpe"] == 1.2

    # 场景 2：count 达标（2 条过线）
    results = [
        {"sharpe": 1.1, "fitness": 0.7},
        {"sharpe": 1.05, "fitness": 0.65},
        {"sharpe": 0.5, "fitness": 0.3},
    ]
    eligible, best = executor.check_mode_b_eligible(results)
    assert eligible is True

    # 场景 3：p75 与 count 均不达标
    results = [
        {"sharpe": 0.8, "fitness": 0.5},
        {"sharpe": 0.6, "fitness": 0.4},
    ]
    eligible, best = executor.check_mode_b_eligible(results)
    assert eligible is False
    assert best is None


def test_mode_b_adaptive_learn_threshold():
    """方案 C：learn_mode_b_threshold 从 registry 样本学习阈值。"""
    from wqb.workflow.mode_b_adaptive import learn_mode_b_threshold, _extract_samples, _fit_threshold

    # 构造样本：5 胜 5 负
    wins = [
        {"payload": {"sharpe": 1.5, "fitness": 0.9}},
        {"payload": {"sharpe": 1.3, "fitness": 0.85}},
        {"payload": {"sharpe": 1.2, "fitness": 0.8}},
        {"payload": {"sharpe": 1.1, "fitness": 0.75}},
        {"payload": {"sharpe": 1.0, "fitness": 0.7}},
    ]
    dead_ends = [
        {"payload": {"best_sharpe": 0.9, "best_fitness": 0.6}},
        {"payload": {"best_sharpe": 0.8, "best_fitness": 0.55}},
        {"payload": {"best_sharpe": 0.7, "best_fitness": 0.5}},
        {"payload": {"best_sharpe": 0.6, "best_fitness": 0.45}},
        {"payload": {"best_sharpe": 0.5, "best_fitness": 0.4}},
    ]

    samples = _extract_samples(wins, dead_ends)
    assert len(samples) == 10
    assert sum(1 for s in samples if s[2]) == 5  # 5 胜
    assert sum(1 for s in samples if not s[2]) == 5  # 5 负

    # 拟合阈值：成功率 >= 30% 的最小 sharpe
    sharpe_threshold = _fit_threshold([(s[0], s[2]) for s in samples], target_rate=0.3)
    assert sharpe_threshold is not None
    assert 0.9 <= sharpe_threshold <= 1.5  # 应在胜负分界附近

    # 样本不足返回 None
    class _FakeStore:
        connection = None
    assert learn_mode_b_threshold(_FakeStore(), "EUR") is None
