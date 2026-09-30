# -*- coding: utf-8 -*-
"""闸 1：语法校验（PLY 括号/字段 + 算子元数/命名参数）。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。

2026-09-07：hump(x, 0.005) 曾以"语法 8/8 PASS"过闸，平台回
"Invalid number of inputs : 2, should be exactly 1 input(s)." 并 CANCEL 整批
8 条 multisim。PLY verifier 只查括号平衡与字段存在性，查不出"命名参数被当
位置参数传"，故此处并联 op_arity（catalog 驱动，见 src/wqb/expression/op_arity.py）。
"""
from .payload import load_arity_checker, load_validator


def run_syntax_gate(items):
    """逐条语法校验。返回 syntax 记录列表（与原 main() 内联块逐字一致）。

    每条记录：{"id": cid, "valid": bool, "errors": [...]}
    """
    validator = load_validator()
    arity_check = load_arity_checker()
    syntax = []
    for cid, e in items:
        r = validator.check_expression(e)
        errors = list(r.get("errors") or []) if not r.get("valid") else []
        if arity_check is not None:
            errors.extend(arity_check(e))
        else:
            errors.append("[ARITY_UNKNOWN] op_arity 不可达（本仓库 src/wqb/expression/op_arity.py 导入失败，见上方 [arity] 行），"
                          "算子元数/命名参数未校验")
        ok = not errors
        syntax.append({"id": cid, "valid": ok, "errors": errors})
        print(f"[syntax] {cid}: {'PASS' if ok else 'FAIL ' + str(errors)[:240]}")
    return syntax
