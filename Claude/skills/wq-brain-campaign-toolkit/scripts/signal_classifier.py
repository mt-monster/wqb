# -*- coding: utf-8 -*-
"""signal_classifier.py - 信号分级器：把候选字段/信号分为主信号/辅助信号/禁止组合。

诊断背景：LLM 生成组合表达式时缺乏信号角色区分，导致等权线性混合泛滥、
同族信号重复叠加、辅助信号稀释主信号。本模块在生成前用台账历史数据
给每个候选信号定级，输出角色标签供组合模板消费。

分级依据（优先级从高到低）：
  1. 台账历史回测 Sharpe（同字段/同族）
  2. 数据集探针三灯判定结果
  3. 字段覆盖率/数据质量元数据
  4. 与历史波次的去重距离

用法:
  from signal_classifier import SignalClassifier
  sc = SignalClassifier(ctx)  # CampaignContext
  roles = sc.classify(["mws85_sentiment", "nws18_ber", "mdl41_numericvalue"])
  # -> {"mws85_sentiment": {"role": "primary", "sharpe_hist": 0.72, ...}, ...}
  pairs = sc.valid_pairs(["mws85_sentiment", "nws18_ber", "mdl41_numericvalue"])
  # -> [("mws85_sentiment", "mdl41_numericvalue"), ...]  # 排除同族对
"""
import csv
import glob
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, expr_fields, load_json, load_platform_constraints


# 同族信号映射：字段名前缀 -> 信号族
# 同族信号之间不应该等权叠加（实质是单信号）
SIGNAL_FAMILIES = {
    "news_sentiment": ["mws85_", "nws18_", "news20_"],
    "analyst_consensus": ["analyst44_", "est_"],
    "insider": ["insider_", "insider_feats"],
    "institutional": ["institutions6_", "inst_"],
    "short_interest": ["shortinterest3_", "si_"],
    "model_fsi": ["mdl41_", "model53_", "model238_"],
    "starmine": ["ep_yield", "forward_pe", "arm_score", "rel_val_"],
    "securities_lending": ["loaned_", "lend_"],
    "web_traffic": ["tranco_", "web_"],
    "option_iv": ["option8_", "option40_", "iv_"],
    "fundamental": ["fundamental28_", "fnd28_"],
    "earnings": ["earnings_", "earn_"],
    "price_volume": ["open", "high", "low", "close", "volume", "returns", "vwap"],
    "dl_riskfree": ["dl_riskfree"],
}


def _field_family(field_name):
    """判断字段属于哪个信号族。"""
    for family, prefixes in SIGNAL_FAMILIES.items():
        for p in prefixes:
            if field_name.startswith(p) or p in field_name:
                return family
    return "other"


class SignalClassifier:
    """信号分级器：基于台账历史 + 探针结果给信号定角色。"""

    def __init__(self, ctx):
        """
        Args:
            ctx: CampaignContext 实例
        """
        self.ctx = ctx
        self._history = None  # 惰性加载
        self._probe_results = None

    # ---------- 数据加载 ----------

    def _load_history(self):
        """从 results/*.csv 加载历史回测记录，按字段聚合最佳 Sharpe。"""
        if self._history is not None:
            return self._history
        self._history = {}  # field -> {"best_sharpe": float, "n_tests": int, "sharpes": [float]}
        results_dir = self.ctx.path("results")
        if not os.path.isdir(results_dir):
            return self._history
        pc = load_platform_constraints()
        known_ops = set(pc.get("known_ops") or [])
        for name in sorted(os.listdir(results_dir)):
            if not name.endswith(".csv"):
                continue
            try:
                with open(os.path.join(results_dir, name), encoding="utf-8-sig", newline="") as f:
                    for row in csv.DictReader(f):
                        code = row.get("code", "")
                        sh_str = row.get("sharpe")
                        if not code or not sh_str or sh_str in ("", "None"):
                            continue
                        try:
                            sh = float(sh_str)
                        except (TypeError, ValueError):
                            continue
                        fields = expr_fields(code, known_ops)
                        for fld in fields:
                            entry = self._history.setdefault(fld, {
                                "best_sharpe": -999, "n_tests": 0, "sharpes": []
                            })
                            entry["best_sharpe"] = max(entry["best_sharpe"], sh)
                            entry["n_tests"] += 1
                            entry["sharpes"].append(sh)
            except Exception:
                continue
        return self._history

    def _load_probe_results(self):
        """从 ledger 加载数据集探针三灯判定结果。"""
        if self._probe_results is not None:
            return self._probe_results
        self._probe_results = {}
        try:
            ledger = load_json(self.ctx.ledger_path)
            for key, val in ledger.items():
                if isinstance(val, dict) and "probe_verdict" in val:
                    self._probe_results[key] = val["probe_verdict"]
                elif isinstance(val, dict) and "verdict" in val:
                    self._probe_results[key] = val["verdict"]
        except Exception:
            pass
        return self._probe_results

    # ---------- 分级逻辑 ----------

    def classify(self, field_names):
        """给一组字段分级。

        Args:
            field_names: 字段名列表

        Returns:
            {field_name: {"role": "primary"|"secondary"|"banned",
                          "family": str,
                          "best_sharpe": float|None,
                          "n_tests": int,
                          "reason": str}}
        """
        history = self._load_history()
        result = {}
        for fld in field_names:
            family = _field_family(fld)
            hist = history.get(fld)
            entry = {
                "family": family,
                "best_sharpe": hist["best_sharpe"] if hist else None,
                "n_tests": hist["n_tests"] if hist else 0,
                "role": None,
                "reason": "",
            }

            if hist:
                avg_sh = sum(hist["sharpes"]) / len(hist["sharpes"]) if hist["sharpes"] else 0
                if hist["best_sharpe"] >= 0.5:
                    entry["role"] = "primary"
                    entry["reason"] = f"历史最佳 Sharpe={hist['best_sharpe']:.2f} >= 0.5"
                elif hist["best_sharpe"] >= 0.2:
                    entry["role"] = "secondary"
                    entry["reason"] = f"历史最佳 Sharpe={hist['best_sharpe']:.2f} in [0.2, 0.5)"
                elif hist["n_tests"] >= 10 and avg_sh < 0.1:
                    entry["role"] = "banned"
                    entry["reason"] = f"已测试 {hist['n_tests']} 次，均值 Sharpe={avg_sh:.2f} < 0.1，判死"
                else:
                    entry["role"] = "secondary"
                    entry["reason"] = f"历史 Sharpe={hist['best_sharpe']:.2f}，信号较弱"
            else:
                # 无历史记录：默认 secondary（未验证），让回测来定
                entry["role"] = "secondary"
                entry["reason"] = "无历史回测记录，待验证"

            result[fld] = entry
        return result

    def valid_pairs(self, field_names, max_corr=0.7):
        """生成合法的主辅信号对。

        规则：
          - 同族信号不组合（实质是单信号叠加）
          - banned 信号不参与组合
          - primary + secondary 组合优先
          - 两个 secondary 可以组合（探索性）
          - 两个 primary 可以组合（强强联合）

        Args:
            field_names: 字段名列表
            max_corr: 最大允许相关性（暂用族级别代理）

        Returns:
            [(primary_field, secondary_field), ...] 按优先级排序
        """
        classified = self.classify(field_names)
        pairs = []
        fields = [f for f in field_names if classified[f]["role"] != "banned"]

        for i, f1 in enumerate(fields):
            for f2 in fields[i + 1:]:
                # 同族不组合
                if classified[f1]["family"] == classified[f2]["family"]:
                    continue
                # 确定主辅
                r1 = classified[f1]["role"]
                r2 = classified[f2]["role"]
                if r1 == "primary" and r2 != "primary":
                    pairs.append((f1, f2))
                elif r2 == "primary" and r1 != "primary":
                    pairs.append((f2, f1))
                elif r1 == "primary" and r2 == "primary":
                    # 双主信号：Sharpe 高的为主
                    s1 = classified[f1].get("best_sharpe") or 0
                    s2 = classified[f2].get("best_sharpe") or 0
                    pairs.append((f1, f2) if s1 >= s2 else (f2, f1))
                else:
                    # 双辅助：按 Sharpe 排序
                    s1 = classified[f1].get("best_sharpe") or 0
                    s2 = classified[f2].get("best_sharpe") or 0
                    pairs.append((f1, f2) if s1 >= s2 else (f2, f1))

        # 按主信号 Sharpe 降序排列
        def pair_score(p):
            s = classified[p[0]].get("best_sharpe")
            return -(s if s is not None else 0)

        pairs.sort(key=pair_score)
        return pairs

    def suggest_weight(self, primary_field, secondary_field):
        """建议主辅权重。

        规则：
          - 主信号 Sharpe >= 1.0: 主 0.8, 辅 0.2
          - 主信号 Sharpe >= 0.5: 主 0.7, 辅 0.3
          - 主信号 Sharpe < 0.5 或无历史: 主 0.6, 辅 0.4
          - 辅助信号权重永不超过 0.4

        Returns:
            (primary_weight, secondary_weight)
        """
        classified = self.classify([primary_field, secondary_field])
        p_sharpe = classified[primary_field].get("best_sharpe") or 0
        if p_sharpe >= 1.0:
            return (0.8, 0.2)
        elif p_sharpe >= 0.5:
            return (0.7, 0.3)
        else:
            return (0.6, 0.4)

    def family_of(self, field_name):
        """公开接口：查询字段所属信号族。"""
        return _field_family(field_name)

    def report(self, field_names):
        """生成分级报告（人类可读）。"""
        classified = self.classify(field_names)
        pairs = self.valid_pairs(field_names)
        lines = ["# 信号分级报告", ""]
        lines.append("## 字段分级")
        for fld, info in sorted(classified.items(), key=lambda x: -(x[1].get("best_sharpe") or 0)):
            role_tag = {"primary": "[主]", "secondary": "[辅]", "banned": "[禁]"}[info["role"]]
            sh = f"{info['best_sharpe']:.2f}" if info["best_sharpe"] is not None else "N/A"
            lines.append(f"  {role_tag} {fld} | 族={info['family']} | 最佳Sharpe={sh} | {info['reason']}")
        lines.append("")
        lines.append("## 合法组合对")
        for p, s in pairs:
            w = self.suggest_weight(p, s)
            lines.append(f"  {p} (主, w={w[0]}) + {s} (辅, w={w[1]})")
        lines.append("")
        lines.append("## 禁止组合")
        banned = [f for f, info in classified.items() if info["role"] == "banned"]
        if banned:
            lines.append(f"  判死字段: {', '.join(banned)}")
        same_family = []
        fields = list(classified.keys())
        for i, f1 in enumerate(fields):
            for f2 in fields[i + 1:]:
                if classified[f1]["family"] == classified[f2]["family"]:
                    same_family.append(f"{f1} + {f2} (同族={classified[f1]['family']})")
        if same_family:
            lines.append(f"  同族禁配: {'; '.join(same_family)}")
        return "\n".join(lines)
