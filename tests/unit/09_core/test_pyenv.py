# -*- coding: utf-8 -*-
"""tools/_pyenv.py：工具脚本共用的解释器 / MCP 目录解析（skills 审查 T0-9 / X-14，2026-09-29）。

此前 7 个脚本各抄一份 `cands = [env, r"d:\\coding\\...\\Scripts\\python.exe"]`：非 Windows 环境（含云端容器）
里 venv 解释器永远找不到。且 Windows 下 `os.execv` = 起子进程后父进程立即退出（返回码 0），上层会把它当成已完成
（wave31 false-complete）——故 Windows 分支改为等待子进程并透传退出码。
"""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import _pyenv  # noqa: E402

SOP_CLIS = ["submit_verdict", "batch_submit_verdict", "super_build", "campaign_intel", "harvest_multisim",
            "sa_probe", "submit_batch", "quota_status", "batch_status", "mcp_ping",
            # 2026-09-29：ra-pipeline 各步细则里以裸 `python` 调用的脚本（skill_lint bare-python 只放行接了 _pyenv 的）
            "build_gate_prior_from_inventory", "select_ra_basket", "gen_field_inspect_packs",
            "field_semantic_classify", "wave_gate", "sync_platform_alphas"]


def test_resolution_order(tmp_path, monkeypatch):
    mcp = tmp_path / "mcp"
    monkeypatch.setenv("WQ_MCP_DIR", str(mcp))
    monkeypatch.delenv("WQ_PY", raising=False)
    assert _pyenv.mcp_dir() == mcp
    assert _pyenv.venv_python() == sys.executable                   # 什么都没有 → 当前解释器
    posix = mcp / ".venv" / "bin" / "python"
    posix.parent.mkdir(parents=True)
    posix.write_text("")
    assert _pyenv.venv_python() == str(posix)                       # POSIX venv
    win = mcp / ".venv" / "Scripts" / "python.exe"
    win.parent.mkdir(parents=True)
    win.write_text("")
    assert _pyenv.venv_python() == str(win)                         # Windows venv 优先（同时存在时）
    explicit = tmp_path / "custom_python"
    explicit.write_text("")
    monkeypatch.setenv("WQ_PY", str(explicit))
    assert _pyenv.venv_python() == str(explicit)                    # $WQ_PY 最优先
    monkeypatch.setenv("WQ_PY", str(tmp_path / "nope"))
    assert _pyenv.venv_python() == str(win)                         # $WQ_PY 指向不存在的文件 → 忽略


def test_default_mcp_dir_is_repo_relative(monkeypatch):
    monkeypatch.delenv("WQ_MCP_DIR", raising=False)
    assert _pyenv.mcp_dir() == ROOT / "world-quant-brain-mcp"


def test_reexec_is_skipped_for_the_same_interpreter_even_if_case_differs(monkeypatch):
    monkeypatch.delenv("WQB_PYENV_REEXEC", raising=False)
    monkeypatch.setattr(_pyenv, "venv_python", lambda: sys.executable)
    called = []
    monkeypatch.setattr(os, "execv", lambda *a: called.append(a))
    _pyenv.reexec_under_venv()
    assert called == []
    # Windows：D:\ vs d:\ 视为同一个
    monkeypatch.setattr(os.path, "normcase", lambda p: p.lower())
    assert _pyenv._same_exe(sys.executable.upper(), sys.executable.lower())


def test_reexec_uses_execv_on_posix_and_waits_on_windows(monkeypatch):
    monkeypatch.delenv("WQB_PYENV_REEXEC", raising=False)
    monkeypatch.setattr(_pyenv, "venv_python", lambda: "/some/other/python")
    monkeypatch.setattr(sys, "argv", ["tool.py", "--x"])

    class _Stop(Exception):
        pass

    def fake_execv(py, argv):
        raise _Stop((py, argv))

    monkeypatch.setattr(os, "execv", fake_execv)
    monkeypatch.setattr(os, "name", "posix")
    with pytest.raises(_Stop) as ei:
        _pyenv.reexec_under_venv()
    assert ei.value.args[0] == ("/some/other/python", ["/some/other/python", "tool.py", "--x"])
    assert os.environ.pop("WQB_PYENV_REEXEC") == "1"                # 防死循环标记

    import subprocess
    monkeypatch.setattr(os, "name", "nt")
    monkeypatch.setattr(subprocess, "call", lambda argv: 7)
    with pytest.raises(SystemExit) as se:
        _pyenv.reexec_under_venv()
    assert se.value.code == 7                                       # 等子进程并透传退出码（不是立即 0）
    os.environ.pop("WQB_PYENV_REEXEC", None)


def test_reexec_loop_guard(monkeypatch):
    monkeypatch.setenv("WQB_PYENV_REEXEC", "1")
    monkeypatch.setattr(_pyenv, "venv_python", lambda: "/some/other/python")
    monkeypatch.setattr(os, "execv", lambda *a: pytest.fail("不应再次 exec"))
    _pyenv.reexec_under_venv()


@pytest.mark.parametrize("name", SOP_CLIS)
def test_sop_cited_clis_have_no_hardcoded_drive_letter(name):
    text = (ROOT / "tools" / f"{name}.py").read_text(encoding="utf-8")
    assert "traeCN_project" not in text, f"{name}.py 仍硬编码 Windows 盘符路径（应走 tools/_pyenv.py）"


@pytest.mark.parametrize("name", [n for n in SOP_CLIS if n not in ("mcp_ping", "quota_status", "batch_submit_verdict")])
def test_sop_cited_clis_share_the_same_bootstrap(name):
    text = (ROOT / "tools" / f"{name}.py").read_text(encoding="utf-8")
    assert "import _pyenv" in text
    assert "os.execv" not in text, f"{name}.py 自带 os.execv（Windows 下会 false-complete）；应统一走 _pyenv.reexec_under_venv"


def test_cli_prints_the_interpreter_for_dollar_wq_py():
    import subprocess
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "_pyenv.py")], capture_output=True, text=True, check=True)
    assert Path(out.stdout.strip()).exists()
