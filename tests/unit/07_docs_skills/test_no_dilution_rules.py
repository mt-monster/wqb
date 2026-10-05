# -*- coding: utf-8 -*-
"""机器规则层不得再推荐「加权稀释」（2026-10-04）。

背景：`methodology_rules.json` 里 4 条 active 规则（`prod_wall_dilution_v1` 梯度稀释、`rnf_dilution_tradeoff_v1`、
`win_replay_slow_fast_v1` 的 0.40 × 0.60、`model_category_rich_v1`）仍在推荐「把两条独立信号腿加权相加」；
`recommend_next_wave` 在「IS 强 + prod > 0.7」（S4 评审最常见的场景）输出 priority 90 的「梯度稀释步长 0.1」建议；
`extract_signals` 还会从权重扫描波里自动学出新的 active 稀释规则。与同文件的 `mixed_signal_leg_ban_v1`、
决策表 D3 / D14（镜像稀释已撤回）、CLAUDE.md「禁止混信号调参」直接矛盾——文档撤回了、机器层还在推，且会自我再生。

守四件事：
  1. 没有 active 规则的 op 是 `gradient_dilute`，也没有 active 规则的 params 带 `slow_weight` / `fast_weight` / `weight_step`；
  2. active 规则的 message 若出现「0.40 … 0.60」配比，必须同时带「禁止」字样（只作为被禁形态被提及）；
  3. `extract_signals` 面对「权重 ↔ prod 单调」的曲线也不再产出稀释规则（反向负例：曲线确实单调）；
  4. `recommend_next_wave` 面对「IS 强 + prod > 0.7」不再给出稀释建议（反向负例：同一输入下仍有其它建议，不是整体哑掉）。
"""
import importlib
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
RULES_JSON = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "config" / "methodology_rules.json"

BANNED_PARAM_KEYS = {"slow_weight", "fast_weight", "weight_step"}


@pytest.fixture(scope="module")
def active_rules():
    data = json.loads(RULES_JSON.read_text(encoding="utf-8-sig"))
    return [r for r in data["rules"] if r.get("status") == "active"]


@pytest.fixture(scope="module")
def rules_mod():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    return importlib.import_module("_lib.rules")


def test_no_active_rule_prescribes_gradient_dilution(active_rules):
    bad = [r["rule_id"] for r in active_rules
           if (r.get("action") or {}).get("op") == "gradient_dilute"
           or BANNED_PARAM_KEYS & set(((r.get("action") or {}).get("params") or {}).keys())]
    assert not bad, f"active 规则仍在推荐加权稀释（违反 mixed_signal_leg_ban_v1）：{bad}"


def test_weight_mix_ratio_only_appears_as_a_prohibition(active_rules):
    offenders = []
    for r in active_rules:
        msg = str((r.get("action") or {}).get("message") or "")
        if "0.40" in msg and "0.60" in msg and "禁止" not in msg:
            offenders.append(r["rule_id"])
    assert not offenders, f"message 里出现 0.40/0.60 配比却没有「禁止」字样：{offenders}"


def test_known_dilution_rules_are_deprecated_not_deleted():
    """退役而非删除：证据留档（deprecated_reason 写明原因），query(status=active) 自然滤掉。"""
    data = json.loads(RULES_JSON.read_text(encoding="utf-8-sig"))
    by_id = {r["rule_id"]: r for r in data["rules"]}
    for rid in ("prod_wall_dilution_v1", "rnf_dilution_tradeoff_v1"):
        assert rid in by_id, f"{rid} 被删了——应 deprecated 留档"
        assert by_id[rid]["status"] == "deprecated"
        assert by_id[rid].get("deprecated_reason"), f"{rid} 缺 deprecated_reason"


def test_extract_signals_no_longer_learns_a_dilution_rule(rules_mod):
    # 反向负例的前提：这条曲线确实是「权重越低 prod 越低」的单调曲线——旧实现会据此产出 gradient_dilute 规则
    rows = [{"weight": w, "prod_corr": p, "sharpe": 2.0}
            for w, p in [(1.0, 0.90), (0.8, 0.87), (0.7, 0.82), (0.5, 0.76), (0.42, 0.70), (0.4, 0.68)]]
    assert rules_mod._detect_dilution(rows) is not None, "前提不成立：_detect_dilution 本应识别这条单调曲线"
    signals = rules_mod.extract_signals(rows, {"region": "TST", "universe": "TOP600", "wave": "1"})
    assert not [s for s in signals if (s.get("action") or {}).get("op") == "gradient_dilute"]


class _Ctx:
    """最小 ctx 桩：recommend_next_wave 只用 dir / region。"""

    def __init__(self, tmp):
        self.dir = str(tmp)
        self.region = "KOR"


def test_recommend_next_wave_no_dilution_advice_when_is_strong_and_prod_walled(rules_mod, tmp_path, monkeypatch):
    monkeypatch.setenv("WQB_RULES_FILE_ONLY", "1")      # 区域规则走文件（不存在 → 空），不读真实 data/wqb.db
    rows = [{"sharpe": 1.8, "fitness": 1.2, "prod_corr": 0.78, "walls": ["PROD"]},
            {"sharpe": 1.6, "fitness": 1.1, "prod_corr": 0.81, "walls": ["PROD"]}]
    recs = rules_mod.recommend_next_wave(_Ctx(tmp_path), rows, near=[], wave_meta={"region": "KOR"})
    text = json.dumps(recs, ensure_ascii=False)
    assert "稀释" not in text and "gradient_dilute" not in text, f"仍在推荐稀释：{text[:300]}"
    assert recs, "同一输入下应仍有其它建议（诊断 / 通用注入），不能整体哑掉"
