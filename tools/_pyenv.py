# -*- coding: utf-8 -*-
"""tools/_pyenv.py — 工具脚本共用的解释器 / MCP 目录解析（跨平台）。

背景（skills 审查 T0-9 / X-14，2026-09-29）：7 个工具脚本各抄一份
``cands = [env, r"d:\\coding\\traeCN_project\\wqb\\...\\Scripts\\python.exe"]``，
非 Windows 环境（含云端容器）里 venv 解释器永远找不到、MCP 目录指向不存在的盘符。
现统一到这里：

    venv_python():  $WQ_PY（须是存在的文件）→ <MCP_DIR>/.venv/Scripts/python.exe（Windows）
                    → <MCP_DIR>/.venv/bin/python（POSIX）→ sys.executable
    mcp_dir():      $WQ_MCP_DIR → <repo>/world-quant-brain-mcp

用法（脚本头部）::

    import _pyenv                      # tools/ 在 sys.path[0]（python tools/x.py 时成立）
    _pyenv.reexec_under_venv()         # 解释器不是 venv 的就 execv 过去
    _pyenv.bootstrap_paths()           # MCP 目录 + src 入 sys.path

命令行 ``python tools/_pyenv.py`` 打印 venv 解释器路径，供文档里的 ``$WQ_PY`` 一行式使用。
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def mcp_dir() -> Path:
    env = os.environ.get("WQ_MCP_DIR")
    return Path(env) if env else REPO_ROOT / "world-quant-brain-mcp"


def venv_python() -> str:
    """MCP venv 的解释器；都不存在时退回当前解释器（不抛错，交给后续 import 报缺依赖）。"""
    v = mcp_dir() / ".venv"
    cands = [os.environ.get("WQ_PY"), str(v / "Scripts" / "python.exe"), str(v / "bin" / "python")]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def reexec_under_venv() -> None:
    py = venv_python()
    if os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)


def bootstrap_paths() -> None:
    for p in (str(REPO_ROOT / "src"), str(mcp_dir())):
        if p not in sys.path:
            sys.path.insert(0, p)


if __name__ == "__main__":
    print(venv_python())
