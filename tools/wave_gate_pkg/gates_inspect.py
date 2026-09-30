# -*- coding: utf-8 -*-
"""体检硬门（缺包策略 off|warn|enforce）+ PROD 饱和闸 + 新数据集首波自动升 enforce。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。

ra-pipeline 步 5 把体检硬门写成"回测前必过"，但 2026-09-06 之前整条可执行路径上
零调用方。有体检包就逐条校验并计入 FAIL；没有体检包按 --inspect-mode 处理：
  warn（灰度默认）= 告警但放行；enforce = 缺包即整波拦截（fail-closed）。
静默通过才是最坏的结果（低覆盖/厚尾/稀疏事件的预处理约束会一路裸奔到仿真）。
"""
import os
import sys

from ._paths import _settings_region, _wqb_db_path

#: 体检硬门缺包时的合法行为。warn = 灰度默认（告警放行），enforce = fail-closed 整波拦截。
INSPECT_MODES = ("off", "warn", "enforce")
DEFAULT_INSPECT_MODE = "warn"


def resolve_inspect_mode(cli_value=None, env=None):
    """解析体检硬门缺包策略，优先级：CLI > 环境变量 `WQB_INSPECT_MODE` > 默认 warn。

    2026-09-17 P1-1：此前缺包**恒静默放行**，导致「无体检包」与「体检通过」在输出上
    无法区分（历史三连复发）。抽出本函数使策略可单测，并支持 CLI 强制 fail-closed。
    非法取值一律回落默认（不让拼错的 mode 意外关掉把关）。
    """
    env = os.environ if env is None else env
    raw = cli_value or env.get("WQB_INSPECT_MODE") or DEFAULT_INSPECT_MODE
    mode = str(raw).strip().lower()
    return mode if mode in INSPECT_MODES else DEFAULT_INSPECT_MODE


def run_inspect_gate(a, campaign, items, syntax, _inspect_mode):
    """执行体检硬门。返回 (report_patch, inspect_report, inspect_unavailable)。

    2026-09-28 默认闸定调（新数据集首波 fail-closed）：用户未显式给 --inspect-mode、
    也无 WQB_INSPECT_MODE 时，缺包行为自适应——新数据集首波（本区该集 0 回测）缺包
    → 升为 enforce（预处理约束不能裸奔到仿真）；熟集缺包 → 维持灰度 warn。

    返回的 `_inspect_mode` 可能被就地升级为 "enforce"，调用方须使用返回的第三项。
    """
    inspect_report = None
    inspect_unavailable = False
    patch = {}
    if _inspect_mode == "off":
        print("[inspect] 体检硬门已按 --inspect-mode=off 显式跳过（无把关）")
        patch["field_inspect"] = {"status": "skipped", "reason": "inspect-mode=off"}
        return patch, None, False
    try:
        tools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import field_inspect_gate as fig_mod
        passed_exprs = [e for (cid, e), s in zip(items, syntax) if s["valid"]]
        if passed_exprs:
            # region 必须走 settings.json 兜底：--region 默认 None（见其 help
            # "缺省读 settings.json"），直接用 a.region 会传空串进来，
            # 于是体检包路径拼成 field_inspect__<ds>.json，明明有包也报"未生效"。
            _region = a.region or _settings_region(campaign) or ""
            inspect_report = fig_mod.check_expressions(
                passed_exprs, region=_region, dataset=a.dataset
            )
            print("\n" + fig_mod.format_report(inspect_report))
            patch["field_inspect"] = inspect_report
            inspect_unavailable = inspect_report.get("status") == "unavailable"
        else:
            # 无有效候选 → 本闸无从校验，按"未生效"处理（enforce 下会拦截，合理）
            inspect_unavailable = True
    except Exception as e:
        print(f"[inspect] 体检硬门执行异常（不阻断）: {e}")
        patch["field_inspect"] = {"status": "error", "error": str(e)}
        inspect_unavailable = True

    # 新数据集首波缺包 → 自动升 enforce（仅在用户未显式指定策略时）
    if inspect_unavailable and _inspect_mode != "off" and a.inspect_mode is None \
            and not os.environ.get("WQB_INSPECT_MODE"):
        try:
            import sqlite3 as _sq9
            _region9 = a.region or _settings_region(campaign) or ""
            _c9 = _sq9.connect(_wqb_db_path(campaign))
            try:
                _n9 = _c9.execute(
                    "SELECT COUNT(*) FROM backtest_results WHERE region=? AND dataset=?",
                    (_region9, a.dataset)).fetchone()[0]
            finally:
                _c9.close()
            if int(_n9 or 0) == 0:
                _inspect_mode = "enforce"
                print("[inspect] 新数据集首波缺体检包（本区该集 0 回测）→ 自动升为 enforce（fail-closed）")
        except Exception:
            pass  # 查不到库时维持灰度，不因环境问题拦波

    if inspect_unavailable and _inspect_mode == "enforce":
        print(
            "[inspect] ★★ fail-closed：本数据集无可用体检包（或体检执行异常），"
            "按 --inspect-mode=enforce 拦截整波，候选未回测。\n"
            "          生成体检包：python tools/gen_field_inspect_packs.py "
            "--region <REGION> --delay <D>\n"
            "          确认无包可生成时临时降级：--inspect-mode warn",
            file=sys.stderr,
        )
    return patch, inspect_report, inspect_unavailable, _inspect_mode


def run_prod_saturation_gate(a, campaign, items):
    """PROD 饱和闸（2026-09-07 P1-1 前移接线）。

    审计实证：全库可提交库存仅 MEA 3 颗，prod 饱和是全局第一瓶颈。
    此闸在 S3 回测前拦截饱和字段/饱和数据集（enforced 态违规计入 FAIL；
    无历史数据区域不阻断，但报告"未生效"）。
    返回 report_patch dict。
    """
    patch = {}
    try:
        tools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import prod_saturation_gate as psg
        _region = a.region or _settings_region(campaign) or ""
        if _region:
            prod_sat_report = psg.check_wave(
                [e for _, e in items], region=_region, dataset=a.dataset
            )
            print("\n" + psg.format_report(prod_sat_report))
            patch["prod_saturation"] = prod_sat_report
    except Exception as e:
        print(f"[prod-sat] PROD 饱和闸执行异常（不阻断）: {e}")
        patch["prod_saturation"] = {"status": "error", "error": str(e)}
    return patch
