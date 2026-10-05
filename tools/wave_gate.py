# -*- coding: utf-8 -*-
"""wave_gate.py — 每波门禁编排器（CLI 入口 shim）。

## 本文件保留三样东西（其余全在 `tools/wave_gate_pkg/`）

1. **argparse 契约字面**（全部 --flag，见 `parser_factory()`）——
   `wqb.workflow._common.validate_argv` 对本文件做**静态解析**（正则读 add_argument，
   位置敏感）。契约若挪进包内，静态解析会 fail-open：`--prod-family-gate` 这类
   透传参数不再被闸住（2026-09-27 自动注入参数事故的守护面）。
2. `parser_factory()` —— 把契约注入包内编排器。
3. **历史符号全量重导出**（含私有名）—— `import wave_gate` 的测试与
   `tools/` 消费方零改动。

完整拆分说明见 `tools/wave_gate_pkg/__init__.py`。

## 用法（与拆分前一致）

  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219 --wave 97
  python tools/wave_gate.py --campaign-dir tracking/USA --dataset fund28 --wave 31
  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219 \
      --exprs-file candidates.txt --inspect-mode enforce
"""
import argparse
import os
import sys

import sys as _sys_pe, os as _os_pe
_sys_pe.path.insert(0, _os_pe.path.dirname(_os_pe.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器解析（tools/_pyenv.py）；作为脚本运行时自动切到 MCP venv，故文档里可写裸 python

# ---- 历史符号全量重导出（含私有名；改名前先 grep 全仓引用面）----------------
# 显式列名而非 `import *`：① 多个测试直接读本文件做文本断言（如
# test_wave_gate_waiver_phase / test_inspect_mode_failclosed_p1p1），列名让符号可见；
# ② 新增/删除符号必须动这行，强制过一遍引用面检查。
from wave_gate_pkg import (  # noqa: E402,F401
    REPO_ROOT, find_script, _wqb_root, _wqb_db_path, _campaign_store_cls,
    _settings_region, _load_region_gates, _load_template_families_for_gate,
    _TOOLKIT_CANDIDATES, _VALIDATOR_CANDIDATES,
    parse_candidates, _write_back_gate_status,
    parse_gate_payload, gate_error_exit, gate_fail_reasons, env_error_exit,
    load_validator, load_arity_checker,
    resolve_inspect_mode, run_inspect_gate, run_prod_saturation_gate,
    INSPECT_MODES, DEFAULT_INSPECT_MODE,
    check_prod_family_gate, format_prod_family_report, _pf_family,
    _extract_ops, _load_prod_wall_families,
    _semantic_gate, run_syntax_gate,
    _family_shape_gate, _match_premise, _extract_fields_from_expr,
    _field_profile_map_for_gate,
    run_quality_stage, run_variant_clustering, OP_CATEGORIES,
    _extract_all_operators,
    _waiver_phase,
    _main_impl,
)


def parser_factory():
    """argparse 契约（全部 --flag；位置敏感，勿挪进包内——见本文件 module docstring）。"""
    ap = argparse.ArgumentParser(description="每波门禁编排器：语法 + 5 闸 + 多样性")
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/KOR)")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--datasets", default="",
                    help="逗号分隔额外数据集，与 --dataset 合并白名单（跨金字塔 mix）")
    ap.add_argument("--wave", default="0",
                    help="波号（字符串，支持 '97' / 's2_pattern_scores_d1' 等；"
                         "与 toolkit pipeline/gate 及 waves.wave_number 同型。"
                         "2026-09-07 P0-3：原 type=int 导致字符串波号无法进门禁——"
                         "ws2_* 波 gate_rows=0 断链的根因）")
    ap.add_argument("--from-db", action="store_true", help="从 expressions 表读候选（推荐）")
    ap.add_argument("--region", default=None, help="区域（缺省读 settings.json）")
    ap.add_argument("--gate-mode", default=None, choices=("off", "warn", "enforce"),
                    help="开波前区域闸模式（2026-09-17 P0-1）：off / warn(只告警) / "
                         "enforce(命中即退出码 2）。缺省先看 WQB_GATE_MODE，再按日期："
                         "灰度期（至 toolkit _lib/region_gates.WARN_SUNSET）warn，之后 enforce")
    ap.add_argument("--candidates", help="兼容：候选 JSON")
    ap.add_argument("--exprs-file", help="每行一条表达式的 txt")
    ap.add_argument("--expr", help="单条表达式")
    ap.add_argument("--skip-diversity-gate", action="store_true", help="透传 toolkit gate.py（repair 批等）")
    ap.add_argument("--skip-semantic-gate", action="store_true",
                    help="跳过闸 SEM（字段语义归类硬门）。默认**强制开启**：缺 s1_semantic_<dataset> "
                         "台账即 exit 2，命中非信号字段（货币代码/汇率/标识符/分类码）的表达式直接剔出候选。"
                         "仅在已确认该数据集无需语义归类时显式使用（会打印醒目告警）。")
    ap.add_argument("--semantic-gate", dest="semantic_gate", default=None,
                    choices=("off", "warn", "enforce"),
                    help="闸 SEM 模式（缺省读环境变量 WQB_SEM_MODE，兜底 enforce）："
                         "off=跳过（= --skip-semantic-gate）/ warn=缺台账仅告警 / "
                         "enforce=缺台账 exit 2 + 黑名单字段剔出候选。")
    ap.add_argument("--batch-type", default="explore", choices=("explore", "repair", "probe"),
                    help="repair/probe 批不做 qp 质量预估标注（2026-09-19：修复批实测 S2.1 却被预估 0.65 BLOCK，纯噪音）")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--fix", action="store_true", help="透传：VECTOR 数据集自动裹 vec_* 后检测")
    ap.add_argument("--inspect-mode", default=None, choices=("off", "warn", "enforce"),
                    help="体检硬门「缺包」时的行为（缺省读环境变量 WQB_INSPECT_MODE，兜底 warn）："
                         "off=跳过不报 / warn=告警但放行（灰度默认）/ "
                         "enforce=fail-closed，缺包即整波拦截（开新数据集前建议 enforce）")
    ap.add_argument("--waiver-mode", default=None, choices=("off", "warn", "enforce"),
                    help="逃生口 waiver 检查（缺省读环境变量 WQB_WAIVER_MODE，兜底 warn）："
                         "warn=用了 --skip-* / --inspect-mode off 等逃生口而台账无有效 waiver 时首屏告警 / "
                         "enforce=无 waiver 即 exit 2 / off=不查（仅测试隔离）。协议见 wqb.waiver、tools/waiver.py")
    ap.add_argument("--prod-family-gate", dest="prod_family_gate", action="store_true",
                    default=True,
                    help="闸 PF：信号族死路预检（2026-09-25，零配额，纯静态）。命中已死路信号族拦截，"
                         "新信号族 WARN 建议 prod-first 探针；--no-prod-family-gate 可关闭")
    ap.add_argument("--no-prod-family-gate", dest="prod_family_gate", action="store_false",
                    help="关闭闸 PF（默认开；enforced 态违规仍会拦截）")
    ap.add_argument("--pf-unknown-mode", default=None, choices=("warn", "enforce"),
                    help="闸 PF 对「未探明骨架（新骨架/低置信度/证据混合）」的处置"
                         "（缺省读环境变量 WQB_PF_UNKNOWN_MODE，兜底 warn）："
                         "warn=只告警不拦波（历史默认）/ enforce=未探明骨架也拦截整波"
                         "（饱和区「先 prod-first 探针后扩批」的强制档）。"
                         "注：已确认死路骨架（prod_corr ≥0.7，n≥3）无论本档为何恒拦截。")
    ap.add_argument("--skip-quality", action="store_true", help="跳过质量预估+六维多样性阶段")
    ap.add_argument("--quality-block", action="store_true",
                    help="EXPECTED_BLOCK 候选计入 FAIL（默认仅标注；回测配额闸门建议开启）")
    ap.add_argument("--probe-mode", action="store_true",
                    help="启用 2+6 探针批模式（早期判死）")
    ap.add_argument("--gem-validate", action="store_true",
                    help="启用 GEM 候选池强制校验")
    ap.add_argument("--min-gem-ratio", type=float, default=0.8,
                    help="GEM 候选最小占比（默认 0.8）")
    ap.add_argument("--s2-field-validate", action="store_true",
                    help="启用 S1 字段候选池强制校验（防止跳过特征工程推荐）")
    ap.add_argument("--s2-field-block", action="store_true",
                    help="S1 字段校验失败时计入 FAIL（默认仅标注）")
    ap.add_argument("--template-family", default=None,
                    help="模板族 family_id（template_families.json）。指定时启用机制-形状一致性软闸："
                         "校验候选字段形状+语义是否满足该族 mechanism_premise，不满足标 WARN（不阻断）")
    return ap


def main(argv=None):
    """CLI 入口：注入 argparse 契约后委托包内编排器。

    与拆分前 `main()` 行为一致（含 `sys.exit(0/1)` 终态；`argv=None` 时读 `sys.argv`）。
    """
    return _main_impl(argv, parser_factory=parser_factory)


if __name__ == "__main__":
    _pyenv.reexec_under_venv()
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    # L3 写库互斥（2026-09-20）：门禁写 gate_results/expressions，与 build_wave/pipeline/harvest 排队
    _src = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
    if _src not in sys.path:
        sys.path.insert(0, _src)
    from wqb.db_write_lock import write_lock as _wlock
    with _wlock(tag="dbwrite_wave_gate", ttl_sec=1200, wait_timeout=120):
        main()
