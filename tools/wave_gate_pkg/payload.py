# -*- coding: utf-8 -*-
"""gate.py 子进程输出的解析与终态判定（PASS / FAIL / ERROR 三分）。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。本模块**不含业务闸逻辑**，
只负责"把子进程输出翻译成结论"与"把结论翻译成退出码"。

历史缺陷（2026-09-08 修复）：gate.py 崩溃时 stdout 无 JSON，旧实现把它记成
all_pass=None 再一路落到 FAIL 分支，使用者看到的是"表达式不合格"，而真实原因
（如缺 typed catalog）只有单独手跑 gate.py 才看得到。现在无结论 = ERROR。
"""
import json
import re
import subprocess
import sys

#: stderr 截尾上限：FileNotFoundError 的自愈命令在 traceback 末尾，800 会把它切掉
_GATE_ERR_TAIL = 4000
#: stdout 只做背景，真正的原因在 stderr
_GATE_OUT_TAIL = 800

#: gate.py 的"闸门环境缺失"逐条标记（与 toolkit gate.ENV_UNKNOWN_TAGS 一致）：没校验，不是式子坏
_ENV_UNKNOWN = re.compile(r"^\[(SYNTAX|ARITY)_UNKNOWN\]")


def _env_unknown_only(issues):
    issues = [str(x) for x in (issues or [])]
    return bool(issues) and all(_ENV_UNKNOWN.match(x) for x in issues)


def parse_gate_payload(stdout):
    """从 gate.py 的 stdout 取结论 JSON（payload 恒为最后一次打印，indent=1）。

    返回 dict（含 bool all_pass）或 None。None 表示 gate.py 没有给出结论，
    调用方必须按 ERROR 处理，不得当成 all_pass=False。
    """
    text = stdout or ""
    starts, off = [], 0
    for line in text.splitlines(keepends=True):
        starts.append(off)
        off += len(line)
    for i in reversed(starts):
        if text[i:i + 1] != "{":
            continue
        try:
            obj = json.loads(text[i:].strip())
        except Exception:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("all_pass"), bool):
            return obj
    return None


def _echo_block(text, prefix, limit):
    """把子进程输出原样透传（截尾但不静默丢弃）。"""
    s = (text or "").rstrip()
    if not s:
        return False
    if len(s) > limit:
        print(f"{prefix} ...(前 {len(s) - limit} 字符省略)")
        s = s[-limit:]
    for line in s.splitlines():
        print(f"{prefix} {line}")
    return True


def gate_error_exit(cmd, r, reason):
    """gate.py 未给出结论 -> ERROR 终态，措辞与"闸门不过"的 FAIL 严格区分。

    透传 stderr 原文（gate.py 的异常消息里通常已带自愈命令，如
    `scan_fields.py --campaign-dir <dir> --dataset <ds>`），并以退出码 2 结束
    （FAIL 仍为 1），让上游 pipeline 能区分"环境坏了"与"这批表达式不合格"。
    """
    print()
    print(f"[gate ] ERROR: {reason}")
    # stdout 先打（多是 store 启动 WARN 之类的背景噪声），stderr 后打 ——
    # 真正的原因要紧挨着 [done ] 行，别被噪声挤到上面去。
    _echo_block(r.stdout, "[gate ] stdout|", _GATE_OUT_TAIL)
    if not _echo_block(r.stderr, "[gate ] stderr|", _GATE_ERR_TAIL):
        print("[gate ] stderr| (空)")
    print(f"[gate ] 复现命令: {subprocess.list2cmdline(cmd)}")
    print("[done ] ERROR: 门禁未跑完 —— gate.py 异常退出，不是闸门不过。"
          "本波未产出门禁结论，也未写 gate_results；按上面 stderr 修复环境后重跑。")
    sys.exit(2)


def gate_fail_reasons(payload):
    """从 gate.py 结论里摘出失败的子闸，供 FAIL 行给出可读原因。"""
    reasons = []
    total, passed = payload.get("total"), payload.get("passed")
    if isinstance(total, int) and isinstance(passed, int) and passed < total:
        reasons.append(f"静态闸 1-5 拦截 {total - passed}/{total} 条")
    for key, label in (("diversity_gate", "批级多样性闸"),
                       ("sanity_gates", "数据质量闸"),
                       ("priors_gate", "知识闸")):
        sub = payload.get(key)
        if isinstance(sub, dict) and sub.get("pass") is False:
            n = len(sub.get("issues") or [])
            reasons.append(label + (f"（{n} 项）" if n else ""))
    blocked = (payload.get("gate0") or {}).get("blocked") or []
    if blocked:
        reasons.append(f"闸0 语义反模式（{len(blocked)} 条）")
    env_only = [it for it in (payload.get("report") or [])
                if not it.get("pass") and _env_unknown_only(it.get("issues"))]
    if env_only:
        reasons.append(f"其中 {len(env_only)} 条仅因闸门环境缺失（verifier / op_arity 不可达）判 FAIL、"
                       "不是表达式问题——设 WQB_WORKSPACE 指向工作区根 / WQ_VALIDATOR_DIR 后重跑")
    return reasons


def env_error_exit(reason):
    """门禁环境缺失（verifier / ply / toolkit gate.py）→ ERROR 终态，退出码 2（闸门不过的 FAIL 为 1）。

    2026-09-27 R12（审计 N12）：此前缺 ply 时 verifier 在 import 阶段 sys.exit(1)，缺 verifier /
    gate.py 时 FileNotFoundError 未捕获（Python 同样 exit 1）——上游把"环境坏了"读成"这批表达式不合格"。
    """
    print(f"[done ] ERROR: 门禁环境缺失 —— {reason}。本波未产出门禁结论、也未写 gate_results，"
          "不是表达式问题；修好环境后重跑。")
    sys.exit(2)


def load_validator():
    """动态加载 alpha-expression-verifier 的 ExpressionValidator（直调，免子进程）。"""
    import importlib
    import os
    from ._paths import _VALIDATOR_CANDIDATES, find_script
    try:
        dir_ = os.path.dirname(find_script(_VALIDATOR_CANDIDATES, "validator.py"))
    except FileNotFoundError as e:
        env_error_exit(str(e))
    sys.path.insert(0, dir_)
    try:
        mod = importlib.import_module("validator")
    except (ImportError, SystemExit) as e:  # verifier 缺 ply 时在 import 阶段 sys.exit(1)
        env_error_exit(f"alpha-expression-verifier 加载失败（{dir_}；通常是缺 ply："
                       f"pip install -r world-quant-brain-mcp/requirements.txt）：{e!r}")
    return mod.ExpressionValidator()


def load_arity_checker():
    """加载 wqb.expression.op_arity.check_expression（算子元数 + 命名参数闸）。

    src/ 相对仓库根；取不到即视为 checkout 损坏，调用方标 ARITY_UNKNOWN 并计 FAIL
    ——静默放过才是最坏结果。
    """
    import os
    from ._paths import REPO_ROOT
    src = os.path.join(REPO_ROOT, "src")
    if os.path.isdir(src) and src not in sys.path:
        sys.path.insert(0, src)
    try:
        from wqb.expression.op_arity import check_expression as _chk
    except Exception as exc:  # pragma: no cover - 仅在 checkout 损坏时触发
        print(f"[arity] 模块不可达: {exc}")
        return None
    return _chk
