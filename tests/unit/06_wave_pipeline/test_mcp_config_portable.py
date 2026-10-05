# -*- coding: utf-8 -*-
"""`.mcp.json` 的 HTTP 形态与跨平台性（2026-10-05 由 stdio 形态改写）。

历史背景
--------
本文件原守护「**${VAR:-default} 跨平台展开**」（skills 审查 T0-9 / X-14）：当时
`.mcp.json` 是 stdio 形态（`command`/`args`/`env`），云端会话因 `D:/coding/...`
ENOENT 起不来，故用 `${VAR:-default}` 并配 Linux 覆盖测试。

2026-10-05 起两个 server 改为 **HTTP 常驻服务**（`type=http` + `url`），
客户端只连 URL、**不再由客户端起进程** ⇒ 盘符路径整体从配置里消失，
`${VAR:-default}` 展开**无处可用**（`_pyenv` 仍是通用工具，语义测试保留）。

所以本文件现在守两件事：
1. **形态**：两个 server 都是 `type=http` + 合法 URL，且**端口不相同**
   —— 端口相同第二个服务起不来，且症状是「客户端连不上」而非报错，极难查；
2. **跨平台**：配置里**不含任何本机盘符**（HTTP 形态天然满足，
   但仍显式断言——防止有人日后又往里塞 `command`）。

旧测试 `test_defaults_expand_to_the_legacy_windows_values` /
`test_env_overrides_make_it_work_on_linux` 依赖 `command` 键，
在 HTTP 形态下**前提已失效**（不是「期望过时」，是「被测对象不存在」），
故替换为本文件下方的新用例；`expand_env` 的通用语义仍由
`test_expand_env_semantics` 覆盖，未删。
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import _pyenv  # noqa: E402

#: HTTP 形态基线（2026-10-05）。**权威源是 .mcp.json 本身**，这里只固化契约。
EXPECTED_URLS = {
    "wq-brain-http": "http://127.0.0.1:8000/mcp",
    "wqb-db": "http://127.0.0.1:8001/mcp",
}


def _servers():
    return json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]


def test_both_servers_are_http_with_expected_urls():
    """两个 server 都是 HTTP 形态，URL 与基线逐字一致。

    URL 变了但没人改这个文件 ⇒ 客户端连不上而服务端自测全绿
    （这正是本文件最初要防的那类静默故障）。
    """
    got = _servers()
    assert set(got) == set(EXPECTED_URLS), f"server 集合变了: {sorted(got)}"
    for name, url in EXPECTED_URLS.items():
        spec = got[name]
        assert spec.get("type") == "http", f"{name} type 应为 http"
        assert spec.get("url") == url, f"{name} url 漂移: {spec.get('url')}"
        # HTTP 形态不应再有 command/args —— 留着会让客户端优先走 stdio
        assert "command" not in spec and "args" not in spec, (
            f"{name} 仍是 command/args 形态，会与 type=http 冲突")


def test_ports_are_distinct():
    """两个 server 端口必须不同 —— 同端口第二个起不来（症状：客户端连不上）。"""
    ports = [urlparse(v).port for v in EXPECTED_URLS.values()]
    assert len(set(ports)) == len(ports), f"端口冲突: {EXPECTED_URLS}"
    for p in ports:
        assert p and 1024 < p < 65536, f"端口非法: {p}"


def test_urls_are_loopback_only():
    """只监听回环地址。

    HTTP 服务无认证；一旦绑 0.0.0.0，等于把「能提交 alpha / 读全部台账」
    的能力暴露到局域网——而 `wq-brain-http` 持平台凭据。
    """
    for name, url in EXPECTED_URLS.items():
        host = urlparse(url).hostname
        assert host in ("127.0.0.1", "localhost"), f"{name} 绑到了 {host}（应为回环）"


def test_mirror_matches_and_has_no_launch_keys():
    """镜像 `mcp_config.json` 与 .mcp.json 一致（AGENTS.md §8.3：镜像漂移不会被发现）。

    HTTP 形态下镜像也不该有 command/args/env —— 它同样是给客户端读的。
    """
    mirror = json.loads((ROOT / "mcp_config.json").read_text(encoding="utf-8"))["mcpServers"]
    got = _servers()
    assert set(mirror) == set(got)
    for name, spec in got.items():
        assert mirror[name].get("url") == spec.get("url"), name
        for k in ("command", "args"):
            assert k not in mirror[name], f"镜像 {name} 仍含 {k}"


def test_no_hardcoded_drive_letter_anywhere():
    """配置里不含任何本机盘符（HTTP 形态天然满足，显式守住防回潮）。"""
    for f in (ROOT / ".mcp.json", ROOT / "mcp_config.json"):
        text = f.read_text(encoding="utf-8")
        stripped = re.sub(r"\$\{[A-Z_]+:-[^}]*\}", "", text)
        assert "D:/" not in stripped and "D:\\" not in stripped, f"{f.name} 含盘符"


def test_expand_env_semantics_still_intact():
    """`_pyenv.expand_env` 是通用工具，语义不因本项目改 HTTP 而变。"""
    e = _pyenv.expand_env
    assert e("${A}/x", {"A": "1"}) == "1/x"
    assert e("${A:-d}/x", {}) == "d/x" and e("${A:-d}/x", {"A": ""}) == "d/x"
    assert e("${A:-d}/x", {"A": "1"}) == "1/x"
    assert e("${MISSING}", {}) == "${MISSING}"                   # 未设且无默认：保留字面量，错误显形
    assert e(["${A:-1}", {"k": "${B:-2}"}, 3], {}) == ["1", {"k": "2"}, 3]
