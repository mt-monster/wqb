# -*- coding: utf-8 -*-
"""逃生口 → waiver 检查（skills 审查 X-8；抽取自拆分前 `tools/wave_gate.py` 的 main() 内联段）。

契约（AGENTS.md §8.1.2「放行 / 豁免协议」）：用了 `--skip-*` 等逃生口就必须有 waiver，
缺省只告警（warn）、`enforce` 下无 waiver 即 exit 2；用了逃生口的事实必须进首屏，不能静默放行。

为什么单独成文件：本仓真实踩过「放行是静默的」——17 处文档写过「可显式降级，但要在台账记因」，
却没有键名 / 字段 / 有效期 / 批准人，于是放行不留痕。判定逻辑**不在此实现**，
统一走 `wqb.waiver`（唯一事实源），本模块只负责「哪些 CLI 开关算逃生口」与「怎么呈现」。

本文件不新增判定口径：闸 → waiver 键映射、批准人、最长天数、legacy 键全在 `GATE_POLICIES`。
"""
import os
import sys

from ._paths import REPO_ROOT


def _escape_hatches(a, inspect_mode, region_gates):
    """本波用到的逃生口 → ``(gate, flag)`` 列表（顺序即首屏呈现顺序）。

    每个逃生口都对应 `GATE_POLICIES` 里的一个闸；新增逃生口必须同时在 `GATE_POLICIES`
    登记（否则 `wqb.waiver.check_skip` 取不到策略），这是 AGENTS.md §8.1.2 的硬要求。
    """
    out = []
    if getattr(a, "skip_diversity_gate", False):
        out.append(("diversity", "--skip-diversity-gate"))
    # SEM 逃生口有三个等价写法：--semantic-gate off / WQB_SEM_MODE=off / --skip-semantic-gate。
    # 优先级 CLI > env（与 §8.1.1 gate-mode 同口径）；显式给了非 off 的模式就不是逃生口。
    _sem = getattr(a, "semantic_gate", None)
    if getattr(a, "skip_semantic_gate", False):
        _sem = "off"
    if _sem is None:
        _sem = (os.environ.get("WQB_SEM_MODE") or "").strip().lower() or None
    if _sem == "off":
        out.append(("semantic", "--semantic-gate off / WQB_SEM_MODE=off"))
    if getattr(a, "prod_family_gate", True) is False:
        out.append(("prod_family", "--no-prod-family-gate"))
    if inspect_mode == "off":
        out.append(("inspect", "--inspect-mode off"))
    # 区域闸降级只在灰度期结束后才算逃生口：此前缺省就是 warn，显式写 warn 是无操作。
    # 故拿 resolve_mode(cli) 与 default_mode() 比，不同才说明「主动降级」。
    try:
        _resolved, _note = region_gates.resolve_mode(getattr(a, "gate_mode", None))
        _default = region_gates.default_mode()
    except Exception:
        _resolved = _default = None
    _cli_mode = (getattr(a, "gate_mode", None) or "").strip().lower() or None
    if _cli_mode in ("warn", "off") and _cli_mode != _default:
        out.append(("region_gates", f"--gate-mode {_cli_mode}"))
    return out


def _waiver_phase(a, campaign, region, inspect_mode, region_gates):
    """检查本波用到的每个逃生口是否有生效 waiver；返回 ``[SkipDecision]``（无逃生口则空）。

    * warn（缺省）：缺 waiver 只告警并继续开波，但首屏点名「无 waiver 记录」+ 台账键名；
    * enforce：无 waiver / 已过期 / 台账不可读一律 exit 2（fail-closed，退出码与「门禁环境缺失」同码，
      含义都是「本波没有门禁结论」，不是「表达式有问题」）；
    * off：不查台账（仅测试隔离），横幅仍如实写「未检查」，不得假装查过。

    `check_skip` 已处理库不可读（按「无 waiver」，enforce 下 fail closed），此处不再重复判断。
    """
    sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
    from wqb import waiver as _waiver
    from wqb.db_conn import connect as _dbconn  # 禁裸 sqlite3.connect（同包规范）

    hatches = _escape_hatches(a, inspect_mode, region_gates)
    if not hatches:
        return []

    _mode = _waiver.resolve_mode(getattr(a, "waiver_mode", None))
    read_err_ids = set()
    if _mode == "off":
        decisions = [_waiver.check_skip(None, gate, region, None, flag, mode="off")
                     for gate, flag in hatches]
    else:
        # 库打不开（文件缺失 / 权限）不能当成「有 waiver」也不能直接崩：按「台账不可读」处理，
        # 横幅里点名，enforce 下照常 fail closed。
        try:
            conn = _dbconn(readonly=True)
        except Exception as e:  # noqa: BLE001 — 任何连接失败都归为「台账不可读」
            conn = None
            _conn_err = f"{type(e).__name__}: {e}"
        else:
            _conn_err = ""
        try:
            decisions = []
            for gate, flag in hatches:
                d = _waiver.check_skip(conn, gate, region, getattr(a, "wave", None),
                                       flag, mode=_mode)
                if conn is None and _conn_err:
                    # 台账不可读属「环境异常」不是「本波结论」：进 stderr，并从 stdout 那行摘掉
                    # 「无 waiver 记录」（否则会出现其实没查成功的误导措辞）。
                    d.lines = [ln.replace("，无 waiver 记录", "")
                               .replace("（无 waiver 记录）", "")
                               for ln in d.lines]
                    d.lines = [f"{ln}（台账不可读：{_conn_err}，未能核对 waiver）" for ln in d.lines]
                    read_err_ids.add(id(d))
                decisions.append(d)
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    # 首屏呈现：有 waiver / 已放行的横幅进 stdout；缺 waiver、被拦、以及「台账不可读」这类
    # 环境异常进 stderr —— 与「本波能否开波」无关的告警不污染正常输出，但绝不能不出现
    # （§8.1.2：不得静默放行）。
    out_lines, err_lines, blocked = [], [], []
    for d in decisions:
        if id(d) in read_err_ids:
            # 台账不可读 ⇒ 无法确认有没有 waiver。enforce 下必须 fail closed：不能因为
            # 「查不到」就当「已放行」（这正是 §8.1.2 要消除的静默放行）。
            err_lines.extend(d.lines)
            if _mode == "enforce":
                d.ok = False
                blocked.append(d)
        elif d.ok:
            out_lines.extend(d.lines)
        else:
            err_lines.extend(d.lines)
            blocked.append(d)

    for line in out_lines:
        print(line)
    for line in err_lines:
        print(line, file=sys.stderr)

    if blocked:
        gates = "/".join(d.gate for d in blocked)
        # 区分拒绝原因：全部因台账不可读 vs 确无 waiver —— 后者要给用户「去登记 waiver」的指引。
        _all_read_err = all(id(d) in read_err_ids for d in blocked)
        _why = "台账不可读，未能核对 waiver" if _all_read_err else "无生效 waiver"
        _hint = ("先修库可读性（检查 WQB_DB_PATH / 文件权限）" if _all_read_err
                 else "放行须在台账登记并注明批准人")
        print(f"[waiver] ⛔ 拒绝开波：逃生口 {gates} {_why}"
              f"（--waiver-mode enforce）。{_hint}；"
              f"见 AGENTS.md §8.1.2 或 `python tools/waiver.py gates`。", file=sys.stderr)
        raise SystemExit(2)
    return decisions
