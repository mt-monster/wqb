# -*- coding: utf-8 -*-
"""composition_validator.py - 组合验证器：回测后验证辅助信号的增量贡献。

诊断背景：组合表达式回测后，需要回答"辅助信号是否有增量贡献"。
如果组合 Sharpe 不如主信号单独 Sharpe，说明辅助信号在稀释而非增强。

验证三问：
  1. 组合 Sharpe > 主信号单独 Sharpe？（增量检验）
  2. 组合 turnover < 1.5 × 主信号单独 turnover？（噪音检验）
  3. 辅助信号腿单独 Sharpe > 0？（辅助信号自身有效性）

用法:
  from composition_validator import CompositionValidator
  cv = CompositionValidator(ctx)
  verdict = cv.validate(combo_result, primary_result, secondary_result)
  # -> {"verdict": "KEEP"|"DROP_SECONDARY"|"DROP_COMBO", "reason": "..."}
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, load_json


class CompositionValidator:
    """组合验证器：回测后审计辅助信号的增量贡献。"""

    # 增量贡献最低门槛
    MIN_INCREMENTAL_SHARPE = 0.05
    # turnover 放大上限
    MAX_TURNOVER_RATIO = 1.5
    # 辅助信号自身最低 Sharpe
    MIN_SECONDARY_SHARPE = 0.0

    def validate(self, combo_result, primary_result, secondary_result=None):
        """验证组合信号的有效性。

        Args:
            combo_result: 组合信号回测结果 {"sharpe": float, "turnover": float, ...}
            primary_result: 主信号单独回测结果
            secondary_result: 辅助信号单独回测结果（可选）

        Returns:
            {"verdict": "KEEP"|"DROP_SECONDARY"|"DROP_COMBO"|"INSUFFICIENT_DATA",
             "incremental_sharpe": float,
             "turnover_ratio": float,
             "secondary_sharpe": float|None,
             "reason": str}
        """
        combo_sh = combo_result.get("sharpe", 0)
        combo_tvr = combo_result.get("turnover", combo_result.get("turnover_pct", 0))
        prim_sh = primary_result.get("sharpe", 0)
        prim_tvr = primary_result.get("turnover", primary_result.get("turnover_pct", 0))

        if combo_sh is None or prim_sh is None:
            return {
                "verdict": "INSUFFICIENT_DATA",
                "incremental_sharpe": 0,
                "turnover_ratio": 0,
                "secondary_sharpe": None,
                "reason": "缺少必要的回测数据",
            }

        incremental = combo_sh - prim_sh
        tvr_ratio = (combo_tvr / prim_tvr) if prim_tvr > 0 else 1.0
        sec_sh = secondary_result.get("sharpe") if secondary_result else None

        # 三问判定
        issues = []

        # Q1: 增量检验
        if incremental < self.MIN_INCREMENTAL_SHARPE:
            issues.append(
                f"增量 Sharpe={incremental:.3f} < {self.MIN_INCREMENTAL_SHARPE}，"
                f"辅助信号无增量贡献"
            )

        # Q2: 噪音检验
        if tvr_ratio > self.MAX_TURNOVER_RATIO:
            issues.append(
                f"turnover 放大 {tvr_ratio:.1f}x > {self.MAX_TURNOVER_RATIO}x，"
                f"辅助信号引入过多噪音"
            )

        # Q3: 辅助信号自身有效性
        if sec_sh is not None and sec_sh < self.MIN_SECONDARY_SHARPE:
            issues.append(
                f"辅助信号自身 Sharpe={sec_sh:.2f} < {self.MIN_SECONDARY_SHARPE}，"
                f"辅助信号本身无 alpha"
            )

        if not issues:
            verdict = "KEEP"
            reason = (
                f"组合 Sharpe={combo_sh:.2f} vs 主信号={prim_sh:.2f} "
                f"(+{incremental:.3f})，turnover 比={tvr_ratio:.1f}x，"
                f"辅助信号有增量贡献"
            )
        elif incremental < 0:
            verdict = "DROP_COMBO"
            reason = "; ".join(issues) + "。组合不如单信号，应放弃组合"
        else:
            verdict = "DROP_SECONDARY"
            reason = "; ".join(issues) + "。建议去掉辅助信号或换辅助信号"

        return {
            "verdict": verdict,
            "incremental_sharpe": round(incremental, 3),
            "turnover_ratio": round(tvr_ratio, 2),
            "secondary_sharpe": sec_sh,
            "combo_sharpe": combo_sh,
            "primary_sharpe": prim_sh,
            "reason": reason,
        }

    def batch_validate(self, results_csv, combo_patterns=None):
        """批量验证：从回测结果 CSV 中识别组合信号并验证。

        Args:
            results_csv: 回测结果 CSV 路径
            combo_patterns: 组合模式列表 [{"combo_code": str, "primary_code": str, "secondary_code": str}]

        Returns:
            验证报告 dict
        """
        rows = {}
        with open(results_csv, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                code = row.get("code", "")
                if code:
                    rows[code] = {
                        "sharpe": _safe_float(row.get("sharpe")),
                        "turnover": _safe_float(row.get("turnover")),
                        "turnover_pct": _safe_float(row.get("turnover_pct")),
                        "fitness": _safe_float(row.get("fitness")),
                    }

        if not combo_patterns:
            return {"error": "需要提供 combo_patterns 来识别组合信号"}

        verdicts = []
        for pat in combo_patterns:
            combo = rows.get(pat["combo_code"])
            primary = rows.get(pat["primary_code"])
            secondary = rows.get(pat.get("secondary_code", ""), None)
            if not combo or not primary:
                verdicts.append({
                    "combo_code": pat["combo_code"][:60],
                    "verdict": "INSUFFICIENT_DATA",
                    "reason": "组合或主信号回测结果缺失",
                })
                continue
            v = self.validate(combo, primary, secondary)
            v["combo_code"] = pat["combo_code"][:60]
            verdicts.append(v)

        n_keep = sum(1 for v in verdicts if v["verdict"] == "KEEP")
        n_drop_sec = sum(1 for v in verdicts if v["verdict"] == "DROP_SECONDARY")
        n_drop_combo = sum(1 for v in verdicts if v["verdict"] == "DROP_COMBO")

        return {
            "total": len(verdicts),
            "keep": n_keep,
            "drop_secondary": n_drop_sec,
            "drop_combo": n_drop_combo,
            "verdicts": verdicts,
        }


def _safe_float(val):
    if val in (None, "", "None"):
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None
