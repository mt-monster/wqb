#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GEM `--detached --console`（实时控制台窗口 + 日志双写）与 `--watch`（跟随）契约。

背景：run.py 的 detached 分支写死 `DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP |
CREATE_NO_WINDOW` 且 stdout/stderr 重定向到文件，MCP 服务自身又无控制台 —— 生成
过程在终端里完全不可见，只能事后 tail。2026-09-25 在 skill 侧原生加 `--console`
（子进程把 stdout 交还新窗口 + `_ConsoleFileTee` 双写同一份 stdout.log）与
`--watch`（人肉 tail -f，终态自动收尾）。本测试冻结三件事：

1. argv 契约：child 命令必须剔掉 `--detached/--console/--watch/--task-id` ——
   否则后台进程自己再弹一个窗口，或被当成 detached 启动器递归 spawn。
2. spawn 契约：console=True 用 CREATE_NEW_CONSOLE 且不重定向 stdout、注入
   GEM_LOG_FILE/GEM_ERR_FILE；console=False 行为逐字不变（回归保护）。
3. 观测契约：tee 双写；控制台编码不支持时降级替换而非把生成带崩；watch 在
   meta 进终态后自行退出（不永久挂住）。
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUN_PY = ROOT / "Claude/skills/brain-make-some-gem/scripts/headless_runner/run.py"

win_only = pytest.mark.skipif(os.name != "nt", reason="creationflags 是 Windows 分支")


def _load_run_py():
    spec = importlib.util.spec_from_file_location("gem_run_console", RUN_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# 1. argv 契约
# ---------------------------------------------------------------------------

def test_child_cmd_strips_launcher_only_flags():
    mod = _load_run_py()
    argv = [
        "--config", "config.json", "--region", "GLB", "--dataset-id", "fundamental17",
        "--delay", "1", "--detached", "--console",
        "--task-id", "gem_1_x", "--tasks-dir", "/tmp/tasks",
        "--watch", "gem_1_x", "--from-start", "--batch-size", "100",
    ]
    child = mod._build_detached_child_cmd(Path("run.py"), argv)
    joined = " ".join(child)
    for flag in ("--detached", "--console", "--watch", "--from-start",
                 "--task-id", "--tasks-dir", "gem_1_x", "/tmp/tasks"):
        assert flag not in child, f"{flag} 泄漏进 detached child 命令：{joined}"
    # 真正的生成参数必须原样透传
    assert "--batch-size" in child and "100" in child and "--region" in child


def test_run_py_argparse_accepts_console_and_watch():
    """--console / --watch 必须在 argparse 里注册（否则 gem 节点透传即秒退）。"""
    import ast

    tree = ast.parse(RUN_PY.read_text(encoding="utf-8-sig"))
    flags = {
        node.args[0].value
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and node.args
        and isinstance(getattr(node.func, "attr", None), str)
        and node.func.attr == "add_argument"
        and isinstance(node.args[0], ast.Constant)
    }
    assert {"--console", "--watch", "--from-start"} <= flags


# ---------------------------------------------------------------------------
# 2. spawn 契约
# ---------------------------------------------------------------------------

class _FakePopen:
    def __init__(self):
        self.kwargs = None

    def __call__(self, cmd, **kwargs):
        self.kwargs = kwargs

        class _P:
            pid = 4242
        return _P()


def _launch(monkeypatch, tmp_path, mod, console: bool):
    fake = _FakePopen()
    monkeypatch.setattr(mod.subprocess, "Popen", fake)
    pid, task_dir = mod._launch_detached(
        cmd=[sys.executable, "run.py", "--region", "GLB"],
        cwd=tmp_path,
        task_id="gem_test_1",
        tasks_dir=tmp_path,
        mode="GLB_test_delay1",
        console=console,
    )
    return fake, pid, task_dir


@win_only
def test_console_launch_opens_real_window_and_injects_tee_env(monkeypatch, tmp_path):
    mod = _load_run_py()
    fake, pid, task_dir = _launch(monkeypatch, tmp_path, mod, console=True)
    flags = fake.kwargs.get("creationflags", 0)
    assert flags == subprocess.CREATE_NEW_CONSOLE
    assert not flags & subprocess.CREATE_NO_WINDOW, "console 模式不得带 CREATE_NO_WINDOW"
    assert fake.kwargs.get("stdout") is None, "console 模式 stdout 必须交还控制台窗口"
    env = fake.kwargs["env"]
    assert env["GEM_LOG_FILE"] == str(task_dir / "stdout.log")
    assert env["GEM_ERR_FILE"] == str(task_dir / "stderr.log")
    assert env.get("PYTHONUNBUFFERED") == "1", "管道/控制台下的块缓冲会把实时拖成几十秒"
    assert pid == 4242
    meta = json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))
    assert meta["status"] == "running" and meta["stdout_log"].endswith("stdout.log")


@win_only
def test_default_detached_launch_unchanged(monkeypatch, tmp_path):
    """console=False：逐字保留原 detached 行为（无窗口 + 文件重定向）。"""
    mod = _load_run_py()
    fake, _, _ = _launch(monkeypatch, tmp_path, mod, console=False)
    flags = fake.kwargs.get("creationflags", 0)
    assert flags & subprocess.CREATE_NO_WINDOW and flags & subprocess.DETACHED_PROCESS
    assert fake.kwargs.get("stdout") is not None
    assert "GEM_LOG_FILE" not in fake.kwargs["env"]


# ---------------------------------------------------------------------------
# 3. 观测契约
# ---------------------------------------------------------------------------

class _NaggingConsole:
    """只在 cp936 遇到不可映射字符时抛错，模拟真实 Windows 终端。"""

    def __init__(self, bad: str = "\U0001f680"):
        self.text = ""
        self.bad = bad
        self.encoding = "ascii"

    def write(self, s):
        if self.bad in s:
            raise UnicodeEncodeError("ascii", s, 0, 1, "terminal cannot encode")
        self.text += s
        return len(s)

    def flush(self):
        pass


def test_console_file_tee_writes_both_and_survives_encode_error(tmp_path):
    mod = _load_run_py()
    log = tmp_path / "stdout.log"
    console = _NaggingConsole()
    tee = mod._ConsoleFileTee(console, str(log))
    tee.write("plain line\n")
    tee.write("rocket \U0001f680 line\n")   # 第一次抛错 → 降级替换重试
    tee.flush()
    assert log.read_text(encoding="utf-8") == "plain line\nrocket \U0001f680 line\n"
    assert "plain line" in console.text and "rocket" in console.text
    assert tee.encoding == "ascii" and tee.isatty() is False


def test_watch_exits_on_terminal_meta(capsys):
    mod = _load_run_py()
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        tasks = Path(td)
        task = tasks / "gem_watch_1"
        task.mkdir()
        (task / "stdout.log").write_text("a\nb\n", encoding="utf-8")
        (task / "meta.json").write_text(
            json.dumps({"status": "completed"}), encoding="utf-8")
        assert mod._watch_task(tasks_dir=tasks, task_id="gem_watch_1",
                              from_start=True, poll_s=0.01) == 0
        out = capsys.readouterr().out
        assert "a" in out and "b" in out and "停止跟随" in out


def test_watch_missing_log_returns_error(capsys, tmp_path):
    mod = _load_run_py()
    assert mod._watch_task(tasks_dir=tmp_path, task_id="gem_nope") == 1
    assert "not found" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# 4. 透传契约（节点 / MCP 层 / registry）
# ---------------------------------------------------------------------------

def test_gem_node_signature_and_registry_advertise_console():
    sys.path.insert(0, str(ROOT / "src"))
    import inspect

    from wqb.workflow.nodes import gem as gem_node
    from wqb.workflow.registry import get_registry

    assert "console" in inspect.signature(gem_node.run).parameters
    node_src = (ROOT / "src/wqb/workflow/nodes/gem.py").read_text(encoding="utf-8")
    assert 'cmd.append("--console")' in node_src, "节点未把 console 透传给 run.py"
    meta = get_registry().get_meta("gem")
    assert meta is not None and "console" in meta.optional_params, \
        "registry 未声明 console → workflow_execute(\"gem\", {\"console\": True}) 会被参数校验拦下"

    tool_src = (ROOT / "world-quant-brain-mcp/tools_workflow.py").read_text(encoding="utf-8")
    assert '"console": console' in tool_src, "workflow_gem 未把 console 传进 gem 节点参数"
