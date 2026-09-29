# -*- coding: utf-8 -*-
"""提交链的默认值守护：不可逆动作默认不执行、颜色缺省不是 GREEN（skills 审查 SB-05/SB-06/X-9）。

只做 AST 静态读取（不 import MCP 包），主 venv 即可跑。
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _defaults(path, func):
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == func:
            a = n.args
            names = [x.arg for x in a.args]
            vals = [None] * (len(names) - len(a.defaults)) + list(a.defaults)
            def _val(v):
                if v is None:
                    return "<required>"
                try:
                    return ast.literal_eval(v)
                except ValueError:          # 非字面量（如常量名）：返回源码文本
                    return ast.unparse(v)
            return {k: _val(v) for k, v in zip(names, vals)}
    raise AssertionError(f"{path}: 找不到 {func}")


def test_workflow_submit_alpha_defaults_are_safe():
    d = _defaults("world-quant-brain-mcp/tools_workflow.py", "workflow_submit_alpha")
    assert d["confirm_submit"] is False, "默认必须只预检不提交"
    assert d["force"] is False
    assert d["color"] is None, "缺省交给节点取 BLUE；GREEN 须由 OS 结果挣得，禁当默认值"
    assert d["dry_run"] is False


def test_submit_alpha_node_default_color_is_pending_blue():
    d = _defaults("src/wqb/workflow/nodes/submit_alpha.py", "run")
    assert d["color"] is None and d["confirm_submit"] is False
    src = (ROOT / "src/wqb/alpha_properties.py").read_text(encoding="utf-8")
    assert 'COLOR_PENDING = "BLUE"' in src


def test_superalpha_tool_default_does_not_submit():
    d = _defaults("world-quant-brain-mcp/tools_workflow.py", "workflow_superalpha")
    assert d["confirm_submit"] is False


def test_verify_timeout_default_matches_wait_thresholds():
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from wqb.config import WAIT_THRESHOLDS
    d = _defaults("world-quant-brain-mcp/tools_workflow.py", "workflow_submit_alpha")
    assert d["verify_timeout"] == WAIT_THRESHOLDS["submit_flip_wait_s"]
