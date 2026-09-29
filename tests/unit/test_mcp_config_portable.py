# -*- coding: utf-8 -*-
"""`.mcp.json` 跨平台（skills 审查 T0-9 / X-14，2026-09-29）。

实证：云端会话里两个 MCP 服务因 `D:/coding/.../Scripts/python.exe` ENOENT 无法启动，工具全部不可用。
现 `.mcp.json` 用 Claude Code 支持的 `${VAR:-default}`（command/args/env 均可展开）：**未设环境变量时
展开结果与改造前逐字相同（作者 Windows 本机行为不变）**；云端/Linux 只需设 WQB_HOME、WQB_MCP_PY、
WQB_DB_MCP_PY（见 README「云端会话连接 MCP」）。`mcp_config.json`（供 Claude Desktop，不展开变量）
保持字面路径，本测试守护它与 `.mcp.json` 的缺省展开值一致——AGENTS.md 曾写明「镜像漂移不会被测试发现」。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import _pyenv  # noqa: E402

W = "D:/coding/traeCN_project/wqb"
LEGACY = {   # 改造前的字面值（Windows 本机行为的回归基线）
    "wq-brain-http": {
        "command": f"{W}/world-quant-brain-mcp/.venv/Scripts/python.exe",
        "args": [f"{W}/world-quant-brain-mcp/main.py"],
        "env": {"MCP_TRANSPORT": "stdio", "WQB_ASI_UNIVERSE_FIX": "20260916",
                "WQ_TOOLKIT_DIR": f"{W}/Claude/skills/wq-brain-campaign-toolkit/scripts",
                "WQ_VALIDATOR_DIR": f"{W}/Claude/skills/alpha-expression-verifier/scripts"},
    },
    "wqb-db": {
        "command": f"{W}/.venv/Scripts/python.exe",
        "args": [f"{W}/wqb_db_mcp.py"],
        "env": {"MCP_TRANSPORT": "stdio"},
    },
}


def _servers():
    return json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]


def test_defaults_expand_to_the_legacy_windows_values():
    """没设任何环境变量时，与改造前逐字相同（作者本机行为不变）。"""
    assert _pyenv.expand_env(_servers(), environ={}) == LEGACY


def test_env_overrides_make_it_work_on_linux():
    env = {"WQB_HOME": "/home/user/wqb", "WQB_MCP_PY": "/home/user/wqb/world-quant-brain-mcp/.venv/bin/python",
           "WQB_DB_MCP_PY": "/home/user/wqb/world-quant-brain-mcp/.venv/bin/python"}
    got = _pyenv.expand_env(_servers(), environ=env)
    assert got["wq-brain-http"]["command"] == env["WQB_MCP_PY"]
    assert got["wq-brain-http"]["args"] == ["/home/user/wqb/world-quant-brain-mcp/main.py"]
    assert got["wq-brain-http"]["env"]["WQ_TOOLKIT_DIR"] == "/home/user/wqb/Claude/skills/wq-brain-campaign-toolkit/scripts"
    assert got["wqb-db"]["command"] == env["WQB_DB_MCP_PY"]
    assert got["wqb-db"]["args"] == ["/home/user/wqb/wqb_db_mcp.py"]
    assert "D:/" not in json.dumps(got)          # 覆盖后不残留任何盘符


def test_mirror_for_claude_desktop_matches_the_default_expansion():
    mirror = json.loads((ROOT / "mcp_config.json").read_text(encoding="utf-8"))["mcpServers"]
    launch = ("command", "args", "env")          # 镜像另有 Desktop 专用键（description / alwaysAllow），不比较
    expected = _pyenv.expand_env(_servers(), environ={})
    assert set(mirror) == set(expected)
    for name, spec in expected.items():
        assert {k: mirror[name].get(k) for k in launch} == {k: spec.get(k) for k in launch}, name


def test_expand_env_semantics():
    e = _pyenv.expand_env
    assert e("${A}/x", {"A": "1"}) == "1/x"
    assert e("${A:-d}/x", {}) == "d/x" and e("${A:-d}/x", {"A": ""}) == "d/x"
    assert e("${A:-d}/x", {"A": "1"}) == "1/x"
    assert e("${MISSING}", {}) == "${MISSING}"                   # 未设且无默认：保留字面量，错误显形
    assert e(["${A:-1}", {"k": "${B:-2}"}, 3], {}) == ["1", {"k": "2"}, 3]


def test_no_hardcoded_drive_letter_left_outside_defaults():
    text = (ROOT / ".mcp.json").read_text(encoding="utf-8")
    import re
    stripped = re.sub(r"\$\{[A-Z_]+:-[^}]*\}", "", text)          # 去掉全部 ${VAR:-default}
    assert "D:/" not in stripped and "D:\\" not in stripped
