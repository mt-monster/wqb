# -*- coding: utf-8 -*-
"""2026-09-21：detached 存活握手必须带「首字节心跳」——子进程存活但长时间 0 字节输出
（batch_track 无控制台标志启动挂死实证：3 小时 0 字节、仅加载 python313.dll）
要判失败并杀进程树，而不是当成"启动成功"。"""
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from wqb.workflow._common import detached_launch_failed  # noqa: E402


def _spawn(code, tmp_path):
    out = tmp_path / "stdout.log"
    err = tmp_path / "stderr.log"
    fo = open(out, "w", encoding="utf-8")
    fe = open(err, "w", encoding="utf-8")
    # 与生产启动点一致：POSIX 上子进程自成会话，killpg 才不会连测试进程一起杀
    extra = {} if sys.platform == "win32" else {"start_new_session": True}
    proc = subprocess.Popen([sys.executable, "-u", "-c", code], stdout=fo, stderr=fe,
                            stdin=subprocess.DEVNULL, **extra)
    return proc, str(out), str(err), fo, fe


def test_silent_alive_child_is_failed_and_killed(tmp_path):
    proc, out, err, fo, fe = _spawn("import time; time.sleep(60)", tmp_path)
    try:
        reason = detached_launch_failed(proc, err, grace_sec=0.3, stdout_log=out, first_output_sec=2)
        assert reason and "0 字节" in reason, reason
        deadline = time.time() + 10
        while proc.poll() is None and time.time() < deadline:
            time.sleep(0.1)
        assert proc.poll() is not None  # 进程树已被杀
    finally:
        fo.close()
        fe.close()
        if proc.poll() is None:
            proc.kill()


def test_child_with_early_output_passes(tmp_path):
    proc, out, err, fo, fe = _spawn(
        "import time,sys; print('hello'); sys.stdout.flush(); time.sleep(5)", tmp_path)
    try:
        reason = detached_launch_failed(proc, err, grace_sec=0.3, stdout_log=out, first_output_sec=5)
        assert reason is None, reason
        assert proc.poll() is None  # 仍在跑，未被误杀
    finally:
        fo.close()
        fe.close()
        if proc.poll() is None:
            proc.kill()


def test_heartbeat_disabled_keeps_old_behaviour(tmp_path):
    proc, out, err, fo, fe = _spawn("import time; time.sleep(3)", tmp_path)
    try:
        reason = detached_launch_failed(proc, err, grace_sec=0.3)
        assert reason is None
    finally:
        fo.close()
        fe.close()
        if proc.poll() is None:
            proc.kill()


def test_live_child_with_benign_stderr_info_line_passes(tmp_path):
    """2026-10-24 实证：toolkit gate.py 把 `[gate] 闸1 verifier = …` 写进 stderr，
    进程仍在跑、gate 已过、表达式已读 —— 不能因这一行判「启动失败」。"""
    code = (
        "import sys,time\n"
        "sys.stderr.write('[gate] 闸1 verifier = D:/x/scripts\\n'); sys.stderr.flush()\n"
        "print('running'); sys.stdout.flush()\n"
        "time.sleep(5)\n"
    )
    proc, out, err, fo, fe = _spawn(code, tmp_path)
    try:
        reason = detached_launch_failed(proc, err, grace_sec=0.5, stdout_log=out, first_output_sec=3)
        assert reason is None, reason
        assert proc.poll() is None  # 仍在跑，未被误杀
    finally:
        fo.close()
        fe.close()
        if proc.poll() is None:
            proc.kill()


def test_live_child_with_traceback_stderr_still_failed(tmp_path):
    """反向：进程存活但 stderr 里是 traceback ⇒ 仍判启动失败（不许把真故障放过）。"""
    code = (
        "import sys,time\n"
        "sys.stderr.write('Traceback (most recent call last):\\n  File \"x.py\"\\nKeyboardInterrupt\\n')\n"
        "sys.stderr.flush()\n"
        "print('running'); sys.stdout.flush()\n"
        "time.sleep(5)\n"
    )
    proc, out, err, fo, fe = _spawn(code, tmp_path)
    try:
        reason = detached_launch_failed(proc, err, grace_sec=0.5, stdout_log=out, first_output_sec=3)
        assert reason and "stderr 非空" in reason, reason
    finally:
        fo.close()
        fe.close()
        if proc.poll() is None:
            proc.kill()


def test_batch_track_launch_flags_match_campaign_node():
    """batch_track 不得再带无控制台创建标志，且必须 stdin=DEVNULL（与 campaign 节点一致）。"""
    src = (REPO_ROOT / "src" / "wqb" / "workflow" / "nodes" / "batch_track.py").read_text(encoding="utf-8")
    start = src.index("popen_kwargs: Dict[str, Any] = {")
    end = src.index("proc = subprocess.Popen(cmd, **popen_kwargs)")
    launch = src[start:end]
    code_lines = [ln for ln in launch.splitlines() if not ln.strip().startswith("#")]
    assert not any("DETACHED_PROCESS" in ln for ln in code_lines)
    assert any('"stdin": subprocess.DEVNULL' in ln for ln in code_lines)


def test_kill_process_tree_never_kills_own_group(tmp_path):
    """子进程与调用方同一进程组（漏了 start_new_session）时，只杀子进程，调用方必须活着。"""
    if sys.platform == "win32":
        return
    from wqb.workflow._common import _kill_process_tree
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"],
                            stdin=subprocess.DEVNULL)   # 故意不新开会话：与本进程同组
    try:
        _kill_process_tree(proc)
        assert proc.poll() is not None      # 子进程已死
    finally:
        if proc.poll() is None:
            proc.kill()
    # 能走到这里就说明本进程没被 killpg 误杀
