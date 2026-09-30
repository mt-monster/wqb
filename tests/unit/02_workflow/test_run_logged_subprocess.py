# -*- coding: utf-8 -*-
"""回归测试：workflow 同步节点的子进程运行器（2026-09-20）。

事故：workflow_execute(node="wave_gate") 用 subprocess.run(capture_output=True,
timeout=1800) 在 MCP 服务内卡满 1800s 才回"超时"，同一命令终端 <1s；超时后
子进程输出全丢、孤儿进程不杀。run_logged_subprocess 三点一起治：
  ① 输出直写日志文件（无管道，后代持有句柄也拖不住父进程）；
  ② 超时杀整棵进程树；
  ③ 超时也返回 log_path + 已落盘的输出尾部。
"""
from __future__ import annotations

import os
import sys
import time

import pytest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))

from wqb.workflow._common import run_logged_subprocess  # noqa: E402
from wqb.workflow.nodes import wave_gate as wave_gate_node  # noqa: E402


def test_normal_run_returns_rc_and_tail():
    info = run_logged_subprocess(
        [sys.executable, "-c", "print('hello-gate'); import sys; sys.exit(3)"],
        log_name="ut_normal", timeout_sec=30,
    )
    assert info["timed_out"] is False
    assert info["returncode"] == 3
    assert "hello-gate" in info["tail"]
    assert os.path.isfile(info["log_path"])


def test_timeout_kills_tree_and_keeps_partial_output():
    # 子进程再 spawn 一个孙进程（持有继承的 stdout 句柄），父进程和孙进程都 sleep 很久。
    # 旧实现 capture_output=True 会因孙进程握着管道而卡到超时；新实现直写文件不受影响，
    # 且超时后整棵树被杀。
    code = (
        "import subprocess, sys, time\n"
        "print('partial-before-hang', flush=True)\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])\n"
        "print('CHILD_PID=%d' % child.pid, flush=True)\n"
        "time.sleep(120)\n"
    )
    t0 = time.time()
    info = run_logged_subprocess([sys.executable, "-c", code], log_name="ut_timeout", timeout_sec=3)
    elapsed = time.time() - t0
    assert info["timed_out"] is True
    assert info["returncode"] is None
    assert elapsed < 60, f"超时后应立即返回，实测 {elapsed:.1f}s"
    assert "partial-before-hang" in info["tail"]
    # 孙进程也应被杀：从日志里取 PID 后确认不存活
    import re
    m = re.search(r"CHILD_PID=(\d+)", info["tail"])
    assert m, "日志里应有孙进程 PID"
    child_pid = int(m.group(1))
    time.sleep(1.0)
    alive = _pid_alive(child_pid)
    assert not alive, f"孙进程 {child_pid} 超时后仍存活（进程树未杀干净）"


def _pid_alive(pid: int) -> bool:
    if os.name == "nt":
        import subprocess
        # tasklist 输出走控制台代码页（中文环境 GBK），按 bytes 收再宽松解码
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True).stdout or b""
        return str(pid).encode() in out
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    # 僵尸进程（已被杀、等父进程 wait）也能通过 kill(pid, 0)：容器里 PID 1 常不回收孤儿，会被误判为「仍存活」。
    # 读 /proc/<pid>/stat 的状态位：Z = 已死。（2026-09-29，容器环境耦合）
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            state = f.read().rsplit(b")", 1)[1].split()[0]
        return state != b"Z"
    except (OSError, IndexError):
        return True


def test_wave_gate_node_timeout_surfaces_log(monkeypatch, tmp_path):
    """节点层：超时返回 error + log_path + timed_out，且不再是静默的 1800s。"""
    calls = {}

    def fake_run(cmd, **kw):
        calls["timeout_sec"] = kw.get("timeout_sec")
        return {"returncode": None, "timed_out": True, "elapsed_sec": 1.0,
                "log_path": str(tmp_path / "x.log"), "tail": "[syntax] 1: PASS\n"}

    monkeypatch.setattr(wave_gate_node, "run_logged_subprocess", fake_run)
    monkeypatch.setattr(wave_gate_node, "validate_argv", lambda cmd: (True, None))
    monkeypatch.setattr(wave_gate_node, "resolve_campaign_dir", lambda r: str(tmp_path))
    monkeypatch.setattr(wave_gate_node.os.path, "isfile", lambda p: True)
    monkeypatch.setenv("WQB_WAVE_GATE_TIMEOUT_SEC", "42")
    res = wave_gate_node.run(region="GLB", dataset="ds", wave="w1")
    assert res["success"] is False
    assert res["timed_out"] is True
    assert calls["timeout_sec"] == 42.0
    assert "x.log" in res["error"] and "等价 CLI" in res["error"]
    assert res["stdout_tail"].startswith("[syntax]")


def test_wave_gate_node_default_timeout_is_short():
    assert wave_gate_node.DEFAULT_TIMEOUT_SEC <= 900


def test_wave_gate_node_passes_extra_datasets(monkeypatch, tmp_path):
    """跨金字塔门控波：datasets 必须透传成 --datasets，否则闸2 误判条件腿字段未验证。

    2026-09-27 事故：GLB dl20d × risk70/fundamental44 门控 8 条被闸2 拦下 7 条
    （'[FIELD] 未验证字段: rsk70_mfm2_gemtrd_btop' 等）——CLI 早有 --datasets，
    节点没暴露，MCP 侧无法合并白名单。
    """
    seen = {}

    def fake_run(cmd, **kw):
        seen["cmd"] = list(cmd)
        return {"returncode": 0, "timed_out": False, "elapsed_sec": 0.1,
                "log_path": str(tmp_path / "g.log"), "tail": "[done ] => PASS\n"}

    monkeypatch.setattr(wave_gate_node, "run_logged_subprocess", fake_run)
    monkeypatch.setattr(wave_gate_node, "validate_argv", lambda cmd: (True, None))
    monkeypatch.setattr(wave_gate_node, "resolve_campaign_dir", lambda r: str(tmp_path))
    monkeypatch.setattr(wave_gate_node.os.path, "isfile", lambda p: True)
    res = wave_gate_node.run(region="GLB", dataset="dl_riskfree_returns", wave="w1",
                             datasets="risk70,fundamental44")
    assert res["success"] is True
    cmd = seen["cmd"]
    assert "--datasets" in cmd
    assert cmd[cmd.index("--datasets") + 1] == "risk70,fundamental44"
    # 不传时不得出现空 --datasets（gate.py 会把 "" 当额外集合解析）
    res2 = wave_gate_node.run(region="GLB", dataset="dl_riskfree_returns", wave="w1")
    assert "--datasets" not in seen["cmd"]
    assert res2["success"] is True
