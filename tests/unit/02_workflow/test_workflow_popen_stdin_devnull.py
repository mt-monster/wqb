# -*- coding: utf-8 -*-
"""2026-09-21：workflow 节点从 MCP 服务进程 spawn 的每个 subprocess.Popen 都必须显式
stdin=subprocess.DEVNULL。实证：MCP 宿主的 stdin 是异步管道，继承它的子解释器在启动阶段
永久阻塞（batch_track 3 小时 0 字节；gem "no meta.json within 90s"）；带 DEVNULL 的
campaign 节点与 gem launch_only 分支从不复现。静态守护：逐个 Popen 调用点回溯 60 行内
必须出现 stdin=… 或 "stdin": …。"""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
NODES = REPO_ROOT / "src" / "wqb" / "workflow" / "nodes"


def _popen_sites(text):
    return [m.start() for m in re.finditer(r"subprocess\.Popen\(", text)]


def test_every_node_popen_sets_stdin_devnull():
    offenders = []
    for py in sorted(NODES.glob("*.py")):
        text = py.read_text(encoding="utf-8")
        for pos in _popen_sites(text):
            window_start = max(0, pos - 2500)
            window = text[window_start:pos + 400]
            # 去掉注释行再判定，防止注释里的 stdin 字样误判通过
            code = "\n".join(ln for ln in window.splitlines() if not ln.strip().startswith("#"))
            if not re.search(r'(\"stdin\"\s*:\s*subprocess\.DEVNULL|stdin\s*=\s*subprocess\.DEVNULL)', code):
                line = text[:pos].count("\n") + 1
                offenders.append(f"{py.name}:{line}")
    assert not offenders, f"这些 Popen 未断开 stdin（继承 MCP 宿主管道会启动挂死）：{offenders}"


def test_batch_track_has_no_detached_process_flag():
    src = (NODES / "batch_track.py").read_text(encoding="utf-8")
    code = "\n".join(ln for ln in src.splitlines() if not ln.strip().startswith("#"))
    assert "DETACHED_PROCESS" not in code
