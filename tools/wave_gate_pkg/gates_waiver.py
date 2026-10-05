# -*- coding: utf-8 -*-
"""闸 waiver：逃生口 → waiver 检查（2026-09-29 落地，skills 审查 X-8；2026-09-30 包化移植）。

开了哪个逃生口（`--skip-diversity-gate` / `--skip-semantic-gate` / `--semantic-gate off` /
`--inspect-mode off` / `--no-prod-family-gate` / 区域闸显式降级），就查台账里有没有对应闸的
有效 waiver（键 `waiver_<gate>_<region>_<wave|all>`，协议与校验在 `wqb.waiver`）。
缺省 warn：无 waiver 只在**首屏**打醒目告警并进报告 `waivers`；`--waiver-mode enforce`
（或 `WQB_WAIVER_MODE=enforce`）下无 waiver 即 exit 2。逃生口本身不变，只是不再能静默使用。

移植说明：函数体与拆分前单体内的 `_waiver_phase` 逐字一致；机械差异仅两处——
`_wqb_root` / `_wqb_db_path` 改走 `_compat` 晚绑定（保住 `monkeypatch.setattr(wave_gate, ...)`
的测试契约，见 `_compat.py` docstring）。
"""
import os
import sys

from . import _compat
from ._paths import REPO_ROOT


def _waiver_phase(a, campaign, region, inspect_mode, rg):
    """逃生口 → waiver 检查（2026-09-29，skills 审查 X-8）。

    开了哪个逃生口（`--skip-diversity-gate` / `--skip-semantic-gate` / `--semantic-gate off` /
    `--inspect-mode off` / `--no-prod-family-gate` / 区域闸显式降级），就查台账里有没有对应闸的
    有效 waiver（键 `waiver_<gate>_<region>_<wave|all>`，协议与校验在 `wqb.waiver`）。
    缺省 warn：无 waiver 只在**首屏**打醒目告警并进报告 `waivers`；`--waiver-mode enforce`
    （或 `WQB_WAIVER_MODE=enforce`）下无 waiver 即 exit 2。逃生口本身不变，只是不再能静默使用。
    返回 SkipDecision 列表（供写进报告）。
    """
    for root in (_compat.wqb_root(campaign), REPO_ROOT):
        src = os.path.join(root, "src")
        if os.path.isdir(os.path.join(src, "wqb")):
            if src not in sys.path:
                sys.path.insert(0, src)
            break
    try:
        from wqb import waiver as W
    except Exception as e:  # 无 wqb 包时本闸其余部分也跑不起来；不因检查本身崩溃
        print(f"[waiver] wqb.waiver 不可导入（{type(e).__name__}: {e}）：逃生口未做 waiver 检查", file=sys.stderr)
        return []

    rg_mode = rg_default = None
    if rg is not None and getattr(rg, "resolve_mode", None):
        rg_mode, _ = rg.resolve_mode(a.gate_mode)
        _dm = getattr(rg, "default_mode", None)      # 旧安装位的 toolkit 可能没有
        rg_default = _dm() if _dm else None
    sem_env = (os.environ.get("WQB_SEM_MODE") or "").strip().lower()
    esc = []
    if a.skip_diversity_gate:
        esc.append(("diversity", "--skip-diversity-gate"))
    if a.skip_semantic_gate:
        esc.append(("semantic", "--skip-semantic-gate"))
    elif a.semantic_gate == "off":
        esc.append(("semantic", "--semantic-gate off"))
    elif a.semantic_gate is None and sem_env == "off":
        esc.append(("semantic", "WQB_SEM_MODE=off"))
    if inspect_mode == "off":
        esc.append(("inspect", "--inspect-mode off"))
    if not a.prod_family_gate:
        esc.append(("prod_family", "--no-prod-family-gate"))
    # 区域闸：显式 off，或灰度期结束后显式回退 warn 才算逃生口（灰度期缺省 warn 不是逃生）
    if rg_mode == "off" or (rg_mode == "warn" and rg_default == "enforce"):
        esc.append(("region_gates", f"--gate-mode {rg_mode}"))
    if not esc:
        return []

    mode = W.resolve_mode(a.waiver_mode)
    conn = None
    if mode != "off":
        try:
            from wqb.db_conn import connect as _dbconn
            conn = _dbconn(_compat.wqb_db_path(campaign), readonly=True)
        except Exception as e:  # 库不可达：check_skip 按「无 waiver」处理（enforce 下 fail closed）
            print(f"[waiver] 台账不可读（{e}）：按无 waiver 处理", file=sys.stderr)
    decisions = []
    try:
        for gate, flag in esc:
            decisions.append(W.check_skip(conn, gate, region, a.wave, flag, mode=mode))
    finally:
        if conn is not None:
            conn.close()
    for d in decisions:
        for line in d.lines:
            print(line, file=sys.stdout if d.ok else sys.stderr)
    blocked = [d for d in decisions if not d.ok]
    if blocked:
        print(f"[waiver] ★★ waiver-mode=enforce：{', '.join(d.gate for d in blocked)} 被跳过但没有有效 waiver"
              "→ 拒绝开波（exit 2）。先写 waiver，或去掉对应逃生口。", file=sys.stderr)
        sys.exit(2)
    return decisions
