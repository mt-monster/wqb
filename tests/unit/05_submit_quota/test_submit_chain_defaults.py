# -*- coding: utf-8 -*-
"""提交链的默认值守护：不可逆动作默认不执行、颜色缺省不是 GREEN（skills 审查 SB-05/SB-06/X-9）。

只做 AST 静态读取（不 import MCP 包），主 venv 即可跑。
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

#: `ast.FunctionDef` 只覆盖同步函数；`async def` 是 `ast.AsyncFunctionDef`。
#: 2026-10-27：`workflow_submit_alpha` 为了不阻塞 MCP 事件循环改成 `async def`，
#: 只认 FunctionDef 的探针当场「找不到函数」⇒ 本文件 4 条提交安全断言全部停摆。
#: 两种形态都要认，否则一次 sync→async 改造就能把不可逆动作的静态保险打瞎。
_FUNC_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef)


def _defaults(path, func):
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    for n in ast.walk(tree):
        if isinstance(n, _FUNC_DEFS) and n.name == func:
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


def _tool_names(path):
    """该模块里所有 `@mcp.tool()` 装饰的函数名（同步 + 异步）。

    ⚠ 这里**故意不复用** `_FUNC_DEFS`：探针自己写死两种形态，才能在被测的
    `_defaults()` 收窄成只看 `FunctionDef` 时仍然枚举出异步工具并让它红。
    """
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    out = []
    for n in ast.walk(tree):
        if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if any("mcp.tool" in ast.unparse(d) for d in n.decorator_list):
            out.append(n.name)
    return out


def test_workflow_submit_alpha_defaults_are_safe():
    d = _defaults("world-quant-brain-mcp/tools_workflow.py", "workflow_submit_alpha")
    assert d["confirm_submit"] is False, "默认必须只预检不提交"
    assert d["force"] is False
    assert d["color"] is None, "缺省交给节点取 BLUE；GREEN 须由 OS 结果挣得，禁当默认值"
    assert d["dry_run"] is False
    assert d["robustness_audited"] is False, "稳健性声明缺省必须 fail-closed（2026-10-04 起快捷入口暴露该参数）"
    assert "allow_prod_above_07" not in d, "prod 红线豁免已于 2026-10-18 彻底移除（不合规），任何入口都不得出现"


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


def test_probe_sees_every_mcp_tool_in_tools_workflow():
    """不变量：本文件的 AST 探针对 `tools_workflow.py` 里**每个** MCP 工具都取得到。

    防的是「判据按代码形态写死」这一类静默失守：2026-10-27 `workflow_submit_alpha`
    改成 `async def` 后，只认 `ast.FunctionDef` 的探针当场看不到它，
    于是 4 条提交安全断言一条都不跑、只留下一条「找不到函数」的红。
    这里对全部工具逐个过一遍探针，任何形态漏认都会在这条用例上暴露。
    """
    path = "world-quant-brain-mcp/tools_workflow.py"
    names = _tool_names(path)
    assert names, f"{path}: 一个 @mcp.tool() 都没解析到（装饰器形态变了？）"
    unreachable = [n for n in names if not isinstance(_defaults(path, n), dict)]
    assert not unreachable, f"{path}: 探针取不到这些工具：{unreachable}"

