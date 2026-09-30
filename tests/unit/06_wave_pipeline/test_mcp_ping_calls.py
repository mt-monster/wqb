"""Explicit MCP calls preserve tool payloads and fail visibly."""
import importlib.util
import json
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("mcp_ping_calls", Path(__file__).parents[3] / "tools" / "mcp_ping.py")
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


def test_call_payload_and_failure_exit(monkeypatch, capsys):
    class Client:
        closed = False
        def __init__(self, *args):
            pass
        def initialize(self):
            pass
        def list_tools(self):
            return [{"name": "query"}]
        def _send(self, method, params):
            assert params["arguments"] == {"region": "EUR"}
            return {"result": {"isError": True, "content": [{"type": "text", "text": "完整错误"}]}}
        def close(self):
            Client.closed = True
    monkeypatch.setattr(mod, "McpStdioClient", Client)
    assert mod.run_calls({"command": "python"}, [{"tool": "query", "args": {"region": "EUR"}}]) == 1
    assert json.loads(capsys.readouterr().out)["result"]["content"][0]["text"] == "完整错误"
    assert Client.closed
