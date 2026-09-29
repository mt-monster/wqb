# -*- coding: utf-8 -*-
"""mode_b_qualify.py — Mode B 资格判定的 CLI 入口（skills 审查 OP-18 / HP-15 / X-16）。

`wqb.workflow.mode_b_config.evaluate_mode_b` 是资格判定（主闸 + 旁路 A–E + 判死线）的唯一实现。
`workflow_judge` 节点只喂 6 个指标（sharpe / fitness / 2Y / margin / turnover / returns），因此旁路 A（robust_sharpe）、
B（prod_corr + 其余全达标）、D（returns 中位数）在该入口**恒不命中**。本工具让 agent 把全部指标喂给**同一个函数**，
得到与代码一致的判定，而不是照文档表格在脑子里手算。判定表与优先级见
`Claude/skills/wq-brain-alpha-optimization-v1/references/mode-b-qualification.md`。

只读：读 ledger_kv（GLOBAL / 区域）与 tracking/<REGION>/config/thresholds.json，不写任何东西。

子命令：
  show      --region KOR                     打印本区生效的主闸 / 旁路 / 判死线及主闸来源
  evaluate  --region KOR --sharpe 1.1 --fitness 0.7 [--two-year-sharpe 1.3] [--robust-sharpe ..]
            [--margin ..] [--margin-bp ..] [--turnover ..] [--returns ..] [--returns-median ..]
            [--prod-corr ..] [--other-dims-pass]                                判定单个候选

单位（与平台 `is` 指标同口径，写错会直接判错，所以做了范围检查）：
  turnover / returns / margin 都是**小数**：turnover 0.35 = 35%；margin 0.0005 = 5bp（也可用 --margin-bp 5）。
  未给的指标 = 该维度无数据 → 依赖它的旁路不命中（不是「通过」）。

用法:
  $WQ_PY tools/mode_b_qualify.py show --region KOR
  $WQ_PY tools/mode_b_qualify.py evaluate --region KOR --sharpe 0.9 --fitness 0.5 --two-year-sharpe 1.3

退出码: 0=判定完成（含不合格；结论看 JSON 的 result.verdict），2=参数错误。
运行环境: MCP venv（$WQ_PY）。
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器/路径解析（tools/_pyenv.py）：裸 python 也能落到 MCP venv

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(_REPO, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_REPO, "src"))

from wqb.workflow.mode_b_config import evaluate_mode_b, load_mode_b_config  # noqa: E402


class _ReadonlyLedger:
    """只读 ledger 适配器：满足 mode_b_config 需要的 ``get_ledger(region, key)``，不建表、不写库。"""

    def __init__(self, db_path=None):
        self._db_path = db_path

    def get_ledger(self, region, key):
        try:
            from wqb.db_conn import connect
            from wqb.store._common import _loads, default_db_path
            conn = connect(self._db_path or default_db_path(), readonly=True)
            try:
                row = conn.execute("SELECT value FROM ledger_kv WHERE region=? AND key=?", (region, key)).fetchone()
            finally:
                conn.close()
            return _loads(row[0]) if row else None
        except Exception:                # noqa: BLE001 —— 读不到就回落默认，判定不能因此崩溃
            return None


def _effective_config(region: str):
    return load_mode_b_config(_ReadonlyLedger(), region=region)


def _check_units(a) -> None:
    """单位守卫：turnover/returns/margin 是小数；把「70」「5」这类百分数/bp 直接喂进来会静默判错。"""
    if a.margin is not None and abs(a.margin) > 0.05:
        raise SystemExit(f"--margin={a.margin} 超出小数范围（0.0005 = 5bp）；bp 请用 --margin-bp")
    if a.turnover is not None and not (0 <= a.turnover <= 5):
        raise SystemExit(f"--turnover={a.turnover} 超出小数范围（0.35 = 35%）；不要传百分数")
    if a.returns is not None and abs(a.returns) > 5:
        raise SystemExit(f"--returns={a.returns} 超出小数范围（0.06 = 6%）；不要传百分数")


def cmd_show(a) -> int:
    cfg = _effective_config(a.region.upper())
    print(json.dumps({"region": a.region.upper(), "config": cfg}, ensure_ascii=False, indent=2))
    return 0


def cmd_evaluate(a) -> int:
    _check_units(a)
    margin = a.margin if a.margin is not None else (a.margin_bp / 1e4 if a.margin_bp is not None else None)
    cfg = _effective_config(a.region.upper())
    inputs = {
        "sharpe": a.sharpe, "fitness": a.fitness, "two_year_sharpe": a.two_year_sharpe,
        "robust_sharpe": a.robust_sharpe, "margin": margin, "turnover": a.turnover, "returns": a.returns,
        "prod_corr": a.prod_corr, "returns_median": a.returns_median,
        "other_dims_all_pass": True if a.other_dims_pass else None,
    }
    result = evaluate_mode_b(cfg, **inputs)
    print(json.dumps({
        "region": a.region.upper(),
        "main_gate": cfg["main_gate"], "main_gate_source": cfg["_source"],
        "inputs": inputs, "result": result,
    }, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Mode B 资格判定（只读；与 workflow_judge 同一判定函数）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("show", help="打印本区生效的资格配置")
    sp.add_argument("--region", required=True)
    sp.set_defaults(fn=cmd_show)

    ev = sub.add_parser("evaluate", help="判定单个候选")
    ev.add_argument("--region", required=True)
    ev.add_argument("--sharpe", type=float)
    ev.add_argument("--fitness", type=float)
    ev.add_argument("--two-year-sharpe", dest="two_year_sharpe", type=float)
    ev.add_argument("--robust-sharpe", dest="robust_sharpe", type=float, help="旁路 A：稳健 Sharpe（子宇宙/鲁棒宇宙口径）")
    ev.add_argument("--margin", type=float, help="小数；0.0005 = 5bp")
    ev.add_argument("--margin-bp", dest="margin_bp", type=float, help="bp 口径；与 --margin 二选一")
    ev.add_argument("--turnover", type=float, help="小数；0.7 = 70%%")
    ev.add_argument("--returns", type=float, help="小数")
    ev.add_argument("--returns-median", dest="returns_median", type=float, help="旁路 D：本数据集已测候选 returns 中位数")
    ev.add_argument("--prod-corr", dest="prod_corr", type=float, help="旁路 B：PROD 相关性")
    ev.add_argument("--other-dims-pass", dest="other_dims_pass", action="store_true",
                    help="旁路 B：除 prod_corr 外其余检查项全部达标（不给 = 未知，B 不命中）")
    ev.set_defaults(fn=cmd_evaluate)
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    _pyenv.reexec_under_venv()
    sys.exit(main())
