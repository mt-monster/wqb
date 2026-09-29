# -*- coding: utf-8 -*-
"""wqb.submit_verdict_core：提交层判定的唯一实现（skills 审查 X-2 / T0-1，2026-09-29）。

覆盖：四态可达性、退出码契约（只有 SUBMITTABLE 是 0；UNVERIFIABLE 不再是 0）、Failed-count 资格门
（REGULAR 看 RA / PPA 看 PPA；PENDING 不计）、硬闸类 WARNING、403 / 未知响应 fail-closed，
以及「三个入口不得各抄一份判定」的守护。
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from wqb.submit_verdict_core import (  # noqa: E402
    EXIT_CODES, SUBMIT_HARD_GATE_WARNINGS, VERDICTS, decide, is_already_submitted, is_ppa_alpha,
    normalize_submit_layer)


def _detail(status="UNSUBMITTED", checks=None, **kw):
    d = {"status": status, "type": "REGULAR", "is": {"checks": checks or []}}
    d.update(kw)
    return d


def _chk(name, result, value=None, limit=None):
    return {"name": name, "result": result, "value": value, "limit": limit}


def test_exit_code_contract():
    assert set(EXIT_CODES) == set(VERDICTS)
    assert EXIT_CODES["SUBMITTABLE"] == 0
    # 只有 SUBMITTABLE 是 0：`$?==0` 放行的脚本不能把 UNVERIFIABLE / ALREADY_SUBMITTED 当可提交
    assert [v for v, c in EXIT_CODES.items() if c == 0] == ["SUBMITTABLE"]
    assert len(set(EXIT_CODES.values())) == len(EXIT_CODES)
    assert 2 not in EXIT_CODES.values()          # 2 留给 argparse 参数错误


def test_fresh_alpha_404_is_unverifiable_never_zero():
    r = decide("A1", _detail(), 404, [])
    assert r["verdict"] == "UNVERIFIABLE" and r["exit_code"] == 10 != 0
    assert r["prepost_unverifiable"] is True
    assert r["submit_layer_view"] == "dead_endpoint_404"
    assert "check_correlation" in r["next_step"] and "confirm_submit=True" in r["next_step"]


def test_submittable_only_when_submit_layer_is_200():
    r = decide("A1", _detail(), 200, [])
    assert r["verdict"] == "SUBMITTABLE" and r["exit_code"] == 0
    assert r["submit_layer_view"] == "live"


@pytest.mark.parametrize("detail", [
    _detail("ACTIVE"), _detail("SUBMITTED"), _detail("UNSUBMITTED", dateSubmitted="2026-09-01T00:00:00Z")])
def test_already_submitted(detail):
    assert is_already_submitted(detail)
    r = decide("A1", detail)
    assert r["verdict"] == "ALREADY_SUBMITTED" and r["exit_code"] == 11
    assert r["submit_status"] is None and r["submit_layer_view"] == "not_queried"
    assert "POST" in r["next_step"]


def test_sim_fail_blocks():
    r = decide("A1", _detail(checks=[_chk("LOW_SHARPE", "FAIL", 1.0, 1.58)]), 404, [])
    assert r["verdict"] == "BLOCKED" and r["exit_code"] == 1
    assert r["reason_code"].startswith("SIM_FAIL:LOW_SHARPE")


@pytest.mark.parametrize("name", sorted(SUBMIT_HARD_GATE_WARNINGS))
def test_hard_gate_warning_blocks(name):
    r = decide("A1", _detail(checks=[_chk(name, "WARNING", 0.5, 1.0)]), 404, [])
    assert r["verdict"] == "BLOCKED"
    codes = [x["code"] for x in r["reasons"]]
    assert "SUBMIT_HARD_WARN" in codes and r["hard_gate_warnings"][0]["name"] == name


def test_soft_warning_alone_does_not_block():
    r = decide("A1", _detail(checks=[_chk("CONCENTRATED_WEIGHT", "PASS"), _chk("SOME_INFO", "WARNING")]), 404, [])
    assert r["verdict"] == "UNVERIFIABLE"


def test_failed_count_gate_regular_uses_ra_and_pending_is_not_failed():
    warn = _chk("LOW_SUB_UNIVERSE_SHARPE", "WARNING", 0.3, 0.5)   # 不在硬闸 WARNING 集合，但计入 RA Failed
    r = decide("A1", _detail(checks=[warn]), 404, [])
    assert r["failed_ra"] == 1 and r["verdict"] == "BLOCKED"
    assert r["reason_code"] == "FAILED_COUNT_RA:LOW_SUB_UNIVERSE_SHARPE"
    pend = _chk("LOW_SUB_UNIVERSE_SHARPE", "PENDING")
    r2 = decide("A1", _detail(checks=[pend]), 404, [])
    assert r2["failed_ra"] == 0 and r2["verdict"] == "UNVERIFIABLE"       # PENDING ≠ FAIL（与平台一致）


def test_failed_count_gate_ppa_uses_ppa_and_low_sharpe_value():
    checks = [_chk("LOW_SHARPE", "PASS", 0.9, 1.0)]                       # PPA：LOW_SHARPE value<1 一律计
    ppa = _detail(type="PPA", checks=checks)
    assert is_ppa_alpha(ppa)
    r = decide("P1", ppa, 404, [])
    assert r["is_ppa"] and r["failed_ppa"] == 1 and r["verdict"] == "BLOCKED"
    assert r["reason_code"] == "FAILED_COUNT_PPA:LOW_SHARPE"
    # 同样的 checks 在 REGULAR 上按 RA 口径（PASS 不计）
    assert decide("R1", _detail(checks=checks), 404, [])["verdict"] == "UNVERIFIABLE"


def test_ppa_detected_by_tag_like_mcp_did():
    d = _detail(tags=["CH_PPA", "PowerPoolSelected"])
    assert is_ppa_alpha(d)               # CLI 旧实现只看 type，漏了标签（与 MCP 不一致）


def test_403_blocks_with_names_and_string_details_are_normalised():
    checks = normalize_submit_layer(403, {"detail": ["REGULAR_SUBMISSION", "PROD_CORRELATION"]})
    assert checks == [{"name": "REGULAR_SUBMISSION", "result": "FAIL"},
                      {"name": "PROD_CORRELATION", "result": "FAIL"}]
    r = decide("A1", _detail(), 403, checks)
    assert r["verdict"] == "BLOCKED"
    assert r["reason_code"] == "SUBMIT_403:REGULAR_SUBMISSION,PROD_CORRELATION"


def test_unknown_or_missing_submit_status_fails_closed():
    for st in (None, 500, 429):
        r = decide("A1", _detail(), st, [])
        assert r["verdict"] == "BLOCKED" and r["exit_code"] == 1, st
        assert r["reason_code"].startswith("UNKNOWN_HTTP_")


def test_non_unsubmitted_404_is_blocked_not_unverifiable():
    r = decide("A1", _detail("DECOMMISSIONED"), 404, [])
    assert r["verdict"] == "BLOCKED" and r["reason_code"] == "NOT_UNSUBMITTED:DECOMMISSIONED"


def test_normalize_submit_layer_200_and_garbage():
    assert normalize_submit_layer(200, {"is": {"checks": [{"name": "X", "result": "PASS"}]}}) == [
        {"name": "X", "result": "PASS"}]
    assert normalize_submit_layer(404, {"x": 1}) == []
    assert normalize_submit_layer(200, None) == []
    assert normalize_submit_layer(403, {"detail": "boom"}) == [{"name": "boom", "result": "FAIL"}]


def test_result_keeps_legacy_mcp_keys():
    """MCP 历史返回体的键必须仍在（下游解析不破）。"""
    r = decide("A1", _detail(), 404, [])
    for k in ("verdict", "verdict_note", "alpha_id", "alpha_status", "is_ppa", "sim_fails", "sim_warnings",
              "hard_gate_warnings", "failed_ra", "failed_ppa", "failed_ra_items", "failed_ppa_items",
              "submit_status", "submit_checks", "submit_layer_view", "prepost_unverifiable"):
        assert k in r, k


# ── 守护：三个入口不得再各抄一份判定 ─────────────────────────────────────────────
@pytest.mark.parametrize("rel", [
    "tools/submit_verdict.py",
    "tools/batch_submit_verdict.py",
    "world-quant-brain-mcp/tools_ops.py",
])
def test_entrypoints_use_the_core_and_do_not_duplicate_logic(rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    assert "submit_verdict_core" in text, f"{rel} 未使用 wqb.submit_verdict_core"
    for banned in ("_SUBMIT_HARD_GATE_WARNINGS", "def _count_failed", "LOW_FITNESS\", \"LOW_SHARPE\""):
        assert banned not in text, f"{rel} 又抄了一份判定口径：{banned}"


def test_cli_exit_codes_follow_the_contract():
    """CLI 的 _finish 按契约退出：UNVERIFIABLE 不再是 0（行为级断言，不比对源码文本）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("submit_verdict_cli", ROOT / "tools" / "submit_verdict.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for verdict, code in EXIT_CODES.items():
        with pytest.raises(SystemExit) as ei:
            mod._finish({"verdict": verdict, "exit_code": code}, False, EXIT_CODES)
        assert ei.value.code == code, verdict
    text = (ROOT / "tools" / "submit_verdict.py").read_text(encoding="utf-8")
    assert "sys.exit(0 if ok else 1)" not in text
