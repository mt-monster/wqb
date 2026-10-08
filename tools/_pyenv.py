# -*- coding: utf-8 -*-
"""tools/_pyenv.py — 工具脚本共用的解释器 / MCP 目录解析（跨平台）。

背景（skills 审查 T0-9 / X-14，2026-09-29）：7 个工具脚本各抄一份
``cands = [env, r"d:\\coding\\traeCN_project\\wqb\\...\\Scripts\\python.exe"]``，
非 Windows 环境（含云端容器）里 venv 解释器永远找不到、MCP 目录指向不存在的盘符。
现统一到这里：

    venv_python():  $WQ_PY（须是存在的文件**且不串仓**）→ <MCP_DIR>/.venv/Scripts/python.exe（Windows）
                    → <MCP_DIR>/.venv/bin/python（POSIX）→ sys.executable
                    「串仓」= $WQ_PY 挂在别的 wqb 工作区的 world-quant-brain-mcp 下（见 is_foreign_wqb_python）
    mcp_dir():      $WQ_MCP_DIR → <repo>/world-quant-brain-mcp

用法（脚本头部）::

    import _pyenv                      # tools/ 在 sys.path[0]（python tools/x.py 时成立）
    _pyenv.reexec_under_venv()         # 解释器不是 venv 的就 execv 过去
    _pyenv.bootstrap_paths()           # MCP 目录 + src 入 sys.path

命令行 ``python tools/_pyenv.py`` 打印 venv 解释器路径，供文档里的 ``$WQ_PY`` 一行式使用。
"""
import os
import re
import sys
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测双标记，**与文件层数无关**
    （AGENTS.md §8 禁止新增 `parents[N]` / `dirname(dirname())` 这类层数硬编码）。
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()
from wqb.paths import find_repo_root  # noqa: E402
REPO_ROOT = find_repo_root(__file__)


def mcp_dir() -> Path:
    env = os.environ.get("WQ_MCP_DIR")
    return Path(env) if env else REPO_ROOT / "world-quant-brain-mcp"


_MCP_MARKER = "world-quant-brain-mcp"


def is_foreign_wqb_python(candidate: str) -> bool:
    """``$WQ_PY`` 是否指向**另一个 wqb 工作区**的 venv（串仓）。

    判据：候选路径的祖先里含 ``world-quant-brain-mcp``（即它挂在某个 wqb 工作区下），
    但那个目录不是本仓的 MCP 目录。

    事故背景（2026-10-06）：环境里残留 ``WQ_PY=D:/coding/hw_project/wqb/world-quant-brain-mcp/
    .venv/Scripts/python.exe``（另一份仓库副本）。它是**存在的文件**，旧实现只看
    ``os.path.isfile`` 于是放行，``tools/submit_queue.py`` 被 re-exec 到那个解释器，
    三层进程互相等待、13 分钟无输出。
    """
    if not candidate:
        return False
    try:
        p = Path(candidate).resolve()
    except OSError:
        return False
    own = os.path.normcase(str(Path(mcp_dir()).resolve()))
    for parent in p.parents:
        if parent.name == _MCP_MARKER:
            return os.path.normcase(str(parent)) != own
    return False


def venv_python() -> str:
    """MCP venv 的解释器；都不存在时退回当前解释器（不抛错，交给后续 import 报缺依赖）。

    顺序：``$WQ_PY``（存在的文件，**且不串仓**）→ <MCP_DIR>/.venv/Scripts/python.exe（Windows）
    → <MCP_DIR>/.venv/bin/python（POSIX）→ sys.executable。
    """
    v = mcp_dir() / ".venv"
    explicit = os.environ.get("WQ_PY")
    if explicit and os.path.isfile(explicit):
        if is_foreign_wqb_python(explicit):
            print(f"[WARN] $WQ_PY 指向另一个 wqb 工作区的 venv（串仓）：{explicit}\n"
                  f"       已忽略，改用本仓 venv {v / 'Scripts' / 'python.exe'}。"
                  f"彻底修复请在 shell 里 unset WQ_PY。", file=sys.stderr)
        else:
            return explicit
    for c in (str(v / "Scripts" / "python.exe"), str(v / "bin" / "python")):
        if os.path.isfile(c):
            return c
    return sys.executable


_ENV_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")


def expand_env(value, environ=None):
    """展开 ``${VAR}`` / ``${VAR:-default}``（与 Claude Code 对 .mcp.json 的展开语法一致）。

    变量未设置且无默认值时保留字面量 ``${VAR}``（让错误显形，而不是悄悄变空串）。
    非字符串原样返回；列表 / 字典递归展开。
    """
    env = os.environ if environ is None else environ
    if isinstance(value, str):
        def _sub(m):
            got = env.get(m.group(1))
            if got not in (None, ""):
                return got
            return m.group(2) if m.group(2) is not None else m.group(0)
        return _ENV_RE.sub(_sub, value)
    if isinstance(value, list):
        return [expand_env(v, environ) for v in value]
    if isinstance(value, dict):
        return {k: expand_env(v, environ) for k, v in value.items()}
    return value


def _same_exe(a: str, b: str) -> bool:
    # Windows 的 abspath 保留盘符大小写（D:\\ vs d:\\），不 normcase 会误判「不是同一个解释器」而 re-exec
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def reexec_under_venv() -> None:
    """当前解释器不是 MCP venv 的就切过去（保持 argv 与退出码语义）。

    POSIX：``os.execv`` 原地替换进程。
    Windows：``os.execv`` 实为「起子进程后父进程立即退出（返回码 0）」——上层会把它当成已完成
    （wave31 false-complete 事故），故改为等待子进程并透传其退出码。
    ``WQB_PYENV_REEXEC`` 防止 venv 路径经符号链接解析后与 sys.executable 不等价时死循环。
    """
    py = venv_python()
    if _same_exe(py, sys.executable) or os.environ.get("WQB_PYENV_REEXEC"):
        return
    os.environ["WQB_PYENV_REEXEC"] = "1"
    if os.name == "nt":
        import subprocess
        sys.exit(subprocess.call([py] + sys.argv))
    os.execv(py, [py] + sys.argv)


def bootstrap_paths() -> None:
    for p in (str(REPO_ROOT / "src"), str(mcp_dir())):
        if p not in sys.path:
            sys.path.insert(0, p)


if __name__ == "__main__":
    print(venv_python())
