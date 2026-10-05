# -*- coding: utf-8 -*-
"""wave_gate 包：每波门禁编排器（原单文件 `tools/wave_gate.py`，2026-09-30 拆分）。

## 为什么拆

原单文件 1631 行，其中 `main()` 独占 725 行、内联 8 个独立闸位。拆分把"编排"
与"各闸实现"分离，使每个闸位可独立单测；**不改变任何对外行为**。

## 模块布局

| 模块 | 职责 |
|---|---|
| `cli.py` | **编排**：按序调用各闸位（argparse 契约在入口 shim `tools/wave_gate.py`） |
| `_paths.py` | 工作区根 / 战役库路径 / skill 目录解析（包内唯一路径事实源） |
| `payload.py` | gate.py 子进程输出解析 + 三分终态（PASS/FAIL/ERROR）+ verifier 装载 |
| `candidates.py` | 候选解析（DB/JSON/txt/单条）+ 逐条状态回写 |
| `gates_semantic.py` | 闸 SEM：字段语义归类硬门 |
| `gates_syntax.py` | 闸 1：PLY 语法 + op_arity |
| `gates_pf.py` | 闸 PF：信号族死路预检 |
| `gates_inspect.py` | 体检硬门 + PROD 饱和闸 |
| `gates_familyshape.py` | 机制-形状一致性软闸 |
| `gates_quality.py` | 六维多样性 + 算子类别覆盖 + 质量预估 + 变体聚类 |
| `gates_waiver.py` | 逃生口 → waiver 检查（09-29 X-8；缺省 warn，enforce 下无 waiver 即 exit 2） |

## 兼容契约（勿破坏）

`tools/wave_gate.py` 保留为**薄 shim**，转发到本包并重导出全部历史符号，
因此下列三类消费者**零改动**：

1. `import wave_gate` / `from wave_gate import parse_candidates`（18 个测试文件）；
2. `subprocess.run([python, "tools/wave_gate.py", ...])`（workflow 节点 / 测试）；
3. `wqb.workflow._common.validate_argv` 对脚本的**静态 argparse 解析**
   （它沿 import 链读 add_argument，链为 shim → 本包 `__init__` → `cli`）。

⚠ `__all__` 之外的符号也一律重导出 —— 测试直接用了多个私有函数
（`_wqb_db_path` / `_load_prod_wall_families` / `_VALIDATOR_CANDIDATES` /
`_settings_region` 等）。**新增/删除符号前先 grep 全仓引用面。**
"""
# ---- 路径 ----
from ._paths import (REPO_ROOT, _TOOLKIT_CANDIDATES, _VALIDATOR_CANDIDATES,
                     _campaign_store_cls, _load_region_gates,
                     _load_template_families_for_gate, _settings_region,
                     _wqb_db_path, _wqb_root, find_script)
# ---- 候选解析 / 状态回写 ----
from .candidates import _write_back_gate_status, parse_candidates
# ---- 机制-形状软闸 ----
from .gates_familyshape import (_extract_fields_from_expr, _family_shape_gate,
                                _field_profile_map_for_gate, _match_premise)
# ---- 体检 / PROD 饱和 ----
from .gates_inspect import (DEFAULT_INSPECT_MODE, INSPECT_MODES,
                            resolve_inspect_mode, run_inspect_gate,
                            run_prod_saturation_gate)
# ---- 闸 PF ----
from .gates_pf import (_extract_ops, _load_prod_wall_families, _pf_family,
                       check_prod_family_gate, format_prod_family_report)
# ---- 质量 / 多样性 ----
from .gates_quality import (OP_CATEGORIES, _extract_all_operators,
                            run_quality_stage, run_variant_clustering)
# ---- 闸 SEM ----
from .gates_semantic import _semantic_gate
# ---- 语法闸 ----
from .gates_syntax import run_syntax_gate
# ---- 逃生口 waiver 检查（09-29 X-8；抽取自原 main() 内联函数）----
from .gates_waiver import _waiver_phase
# ---- gate.py 输出解析 / 终态 ----
from .payload import (env_error_exit, gate_error_exit, gate_fail_reasons,
                      load_arity_checker, load_validator, parse_gate_payload)
# ---- CLI 编排 ----
# 注意：`cli.main` 需要显式注入 `parser_factory`（argparse 契约字面保留在
# 入口脚本 `tools/wave_gate.py` 内，见该文件 module docstring）。包层不提供
# 可直接调用的 `main()` —— 直接调用请走 `_main_impl(argv, parser_factory=...)`，
# 或按 `import wave_gate`（shim 路径）取得已注入的 `main`。
from .cli import main as _main_impl

__all__ = [
    "REPO_ROOT", "find_script", "_wqb_root", "_wqb_db_path", "_campaign_store_cls",
    "_settings_region", "_load_region_gates", "_load_template_families_for_gate",
    "_TOOLKIT_CANDIDATES", "_VALIDATOR_CANDIDATES",
    "parse_candidates", "_write_back_gate_status",
    "parse_gate_payload", "gate_error_exit", "gate_fail_reasons", "env_error_exit",
    "load_validator", "load_arity_checker",
    "resolve_inspect_mode", "run_inspect_gate", "run_prod_saturation_gate",
    "INSPECT_MODES", "DEFAULT_INSPECT_MODE",
    "check_prod_family_gate", "format_prod_family_report", "_pf_family",
    "_extract_ops", "_load_prod_wall_families",
    "_semantic_gate", "run_syntax_gate",
    "_family_shape_gate", "_match_premise", "_extract_fields_from_expr",
    "_field_profile_map_for_gate",
    "run_quality_stage", "run_variant_clustering", "OP_CATEGORIES",
    "_extract_all_operators",
    "_waiver_phase",
    "_main_impl",
]
