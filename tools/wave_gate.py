# -*- coding: utf-8 -*-
"""wave_gate.py - 每波门禁编排器（CLI 入口 + 薄 shim，实现在 tools/wave_gate_pkg/ 包内）。

在单次调用内完成：
  1) 候选解析：--candidates JSON（{expressions:[{id,expr}]} / [str] / {exprs:[...]}）
     或 --exprs-file（每行一条）或 --expr（单条）
  2) 语法校验：alpha-expression-verifier（与 gate 闸1 同源，先于 5 闸执行，
     失败即整波拦截——语法错误是整批 CANCELLED 连坐的头号元凶）
  3) 5 闸预检 + 批级多样性：复用 wq-brain-campaign-toolkit 的权威 gate.py
     （路径自动解析 WQ_TOOLKIT_DIR → ~/.claude/... → 仓库自带 Claude/skills，勿硬编码）
  4) 六维结构多样性 + 质量预估；EXPECTED_BLOCK 候选默认仅标注，
     --quality-block 开启硬拦截（回测配额闸门）
  5) 结果落盘：gate_results 表（完整 JSON + 人类摘要）

用法:
  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219 --wave 97       --candidates candidates/wave97_exprs.json
  python tools/wave_gate.py --campaign-dir tracking/USA --dataset fund28 --wave 31       --exprs-file candidates/w31.txt --skip-diversity-gate
  python tools/wave_gate.py --campaign-dir tracking/KOR --dataset model219       --expr "rank(close)" --wave 98

退出码: 0=PASS（语法+5 闸全过）, 1=FAIL（闸门不过，表达式不合格）,
        2=ERROR（gate.py 子进程崩溃/未给出结论 —— 环境问题，不是表达式问题；
          stderr 原文已透传到 [gate ] stderr| 行，自愈命令通常就在里面）
运行环境: 与 gate.py 一致，纯标准库，任意 Python 3.10+ 均可。

------------------------------------------------------------------
2026-09-30 包化：本文件原为 1631 行单文件（`main()` 独占 725 行、内联 8 个闸位）。
现拆为 `tools/wave_gate_pkg/` 包（cli / _paths / payload / candidates / gates_*），
本文件保留**两样东西**，其余一律转发到包：

  A) **argparse 契约**（下文 `build_parser()` 的 25 个 `add_argument`，字面声明）；
  B) `__main__` 入口（启动校验 + L3 写库互斥锁）。

拆分的三类消费者**零改动**：

  1) `import wave_gate` / `from wave_gate import parse_candidates`（18 个测试文件）；
  2) `subprocess.run([python, "tools/wave_gate.py", ...])`（workflow 节点 / 测试）；
  3) `wqb.workflow._common.validate_argv` 的**静态 argparse 解析**。

  ⚠ **A 是本次拆分最脆的契约，勿把 parser 挪进包内**：
  `_common.script_arg_contract` 要求**入口脚本自身**必须出现字面 `add_argument`
  —— 否则直接返回 None = fail-open，argv 校验静默失效（它只放行"脚本压根没声明过
  的 --flag"，读不到声明就无从拦截）。`_common._local_module_files` 又只解析
  **一层** `from X import ...`。2026-09-30 实测三种失效写法，全部 fail-open：
    ① shim 零 add_argument、parser 在包内 → own 为空 → None；
    ② parser 藏在包内二层（`wave_gate.cli.parser`）→ 一层解析够不到 → None；
    ③ 通配式 `ap.add_argument(*flags, **kw)` → 静态正则只认字面串 → None。
  **结论：parser 必须字面留在本文件。** 改动前先跑：
      python -m pytest tests/unit/test_wave_gate_auto_insert_contract.py -q
      python -c "import sys;sys.path.insert(0,'src');from wqb.workflow import _common as c;print(c.script_arg_contract('tools/wave_gate.py') is not None)"

原单文件备份于 `attic/wave_gate_split_20260930/wave_gate_monolith_1631.py`。
"""
import argparse
import os
import sys

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

from wave_gate_pkg import *  # noqa: E402,F401,F403  （包 __init__ 重导出全部历史符号）
from wave_gate_pkg import __all__ as _pkg_all  # noqa: E402

# 显式转发包内被历史消费者引用的符号（测试直接 import 了若干私有名）。
from wave_gate_pkg import (  # noqa: E402,F401
    DEFAULT_INSPECT_MODE, INSPECT_MODES, OP_CATEGORIES, REPO_ROOT,
    _campaign_store_cls, _extract_all_operators, _extract_fields_from_expr,
    _extract_ops, _field_profile_map_for_gate, _family_shape_gate,
    _load_prod_wall_families, _load_region_gates, _load_template_families_for_gate,
    _match_premise, _pf_family, _semantic_gate, _settings_region,
    _TOOLKIT_CANDIDATES, _VALIDATOR_CANDIDATES, _wqb_db_path, _wqb_root,
    _write_back_gate_status, check_prod_family_gate, env_error_exit, find_script,
    format_prod_family_report, gate_error_exit, gate_fail_reasons,
    load_arity_checker, load_validator, parse_candidates,
    parse_gate_payload, resolve_inspect_mode, run_inspect_gate,
    run_prod_saturation_gate, run_quality_stage, run_syntax_gate,
    run_variant_clustering,
)

__all__ = list(_pkg_all)

#: 包内编排入口（要求显式注入 parser_factory，见其 docstring）
from wave_gate_pkg import _main_impl  # noqa: E402


def main(argv=None):
    """CLI 入口：把本文件（字面）的 argparse 契约注入编排层。

    ⚠ 必须传 `build_parser=self.build_parser` —— 契约的唯一字面定义在本文件，
    注入是为了让 `wqb.workflow._common.script_arg_contract` 仍能解析到它。
    """
    return _main_impl(argv, parser_factory=build_parser)


def build_parser():
    """构建 argparse（每波门禁编排器的完整 CLI 契约）。"""
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
    ap.add_argument("--prod-family-gate", dest="prod_family_gate", action="store_true",
                    default=True,
                    help="闸 PF：信号族死路预检（2026-09-25，零配额，纯静态）。命中已死路信号族拦截，"
                         "新信号族 WARN 建议 prod-first 探针；--no-prod-family-gate 可关闭")
    ap.add_argument("--no-prod-family-gate", dest="prod_family_gate", action="store_false",
                    help="关闭闸 PF（默认开；enforced 态违规仍会拦截）")
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


if __name__ == "__main__":
    import os as _os_sc
    _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    # L3 写库互斥（2026-09-20）：门禁写 gate_results/expressions，与 build_wave/pipeline/harvest 排队
    _src = os.path.normpath(os.path.join(_TOOLS_DIR, "..", "src"))
    if _src not in sys.path:
        sys.path.insert(0, _src)
    from wqb.db_write_lock import write_lock as _wlock
    with _wlock(tag="dbwrite_wave_gate", ttl_sec=1200, wait_timeout=120):
        main()
