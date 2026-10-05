# -*- coding: utf-8 -*-
"""wqb.waiver 协议：键、校验、读取顺序、旧键兼容、横幅、跳过检查（skills 审查 X-8）。"""
import datetime as dt
import json
import re
import sqlite3

import pytest

from wqb import waiver as W

T = dt.date(2026, 9, 29)


def _conn(rows=()):
    c = sqlite3.connect(":memory:")
    # 与既有夹具一致：只有 region/key/value 三列（不能依赖 updated_at）
    c.execute("CREATE TABLE ledger_kv (region TEXT, key TEXT, value TEXT)")
    for region, key, value in rows:
        c.execute("INSERT INTO ledger_kv VALUES (?,?,?)", (region, key, json.dumps(value)))
    return c


def _good(**kw):
    v = {"gate": "semantic", "reason_code": "NO_INPUT_AVAILABLE", "reason": "该数据集无描述文",
         "evidence": "ledger:KOR/s1_semantic_x 缺失；classify 报 no description",
         "approved_by": "agent", "created_at": "2026-09-29", "expires_at": "2026-10-03"}
    v.update(kw)
    return v


# ----------------------------------------------------------------------------- 键
def test_key_roundtrip_including_underscored_gate_and_wave():
    assert W.waiver_key("stop_rules", "gbr") == "waiver_stop_rules_GBR_all"
    assert W.waiver_key("semantic", "KOR", "s2_pattern_scores_d1") == "waiver_semantic_KOR_s2_pattern_scores_d1"
    assert W.parse_key("waiver_stop_rules_GBR_all") == ("stop_rules", "GBR", "all")
    assert W.parse_key("waiver_semantic_KOR_s2_pattern_scores_d1") == ("semantic", "KOR", "s2_pattern_scores_d1")
    assert W.parse_key("waiver_region_gates_USA_97") == ("region_gates", "USA", "97")
    assert W.parse_key("stop_rules_override") is None
    assert W.parse_key("waiver_unknowngate_USA_all") is None


def test_wave_zero_and_none_mean_all():
    assert W.waiver_key("diversity", "KOR", 0) == W.waiver_key("diversity", "KOR", None) == "waiver_diversity_KOR_all"


# ----------------------------------------------------------------------------- 校验
def test_valid_new_form_is_active():
    w = W.normalize("semantic", "KOR", "all", _good(), source_key="k", today=T)
    assert w.status == W.ACTIVE and not w.problems and w.active


def test_expired_new_form():
    w = W.normalize("semantic", "KOR", "all", _good(expires_at="2026-09-28", created_at="2026-09-25"),
                    source_key="k", today=T)
    assert w.status == W.EXPIRED


def test_expiry_day_itself_is_still_valid_like_legacy_until():
    w = W.normalize("semantic", "KOR", "all", _good(expires_at="2026-09-29"), source_key="k", today=T)
    assert w.status == W.ACTIVE


@pytest.mark.parametrize("patch,needle", [
    ({"expires_at": None}, "expires_at"),                       # 不允许永久
    ({"created_at": None}, "created_at"),
    ({"reason": " "}, "reason"),
    ({"reason_code": "BECAUSE"}, "reason_code"),
    ({"approved_by": "bot"}, "approved_by"),
    ({"expires_at": "2026-12-31"}, "上限"),                      # semantic 最长 7 天
    ({"expires_at": "2026-09-01"}, "早于"),
    ({"evidence": None}, "evidence"),                           # NO_INPUT_AVAILABLE 必带证据
    ({"gate": "diversity"}, "不一致"),
])
def test_invalid_new_form(patch, needle):
    w = W.normalize("semantic", "KOR", "all", _good(**patch), source_key="k", today=T)
    assert w.status == W.INVALID and any(needle in p for p in w.problems), w.problems


def test_user_only_gate_rejects_agent_approver():
    v = _good(gate="stop_rules", reason_code="USER_INSTRUCTION", approved_by="agent", expires_at="2026-10-05")
    w = W.normalize("stop_rules", "GBR", "all", v, source_key="k", today=T)
    assert w.status == W.INVALID and any("只允许 user" in p for p in w.problems)


def test_user_instruction_requires_user_approver():
    v = _good(reason_code="USER_INSTRUCTION", approved_by="agent")
    w = W.normalize("semantic", "KOR", "all", v, source_key="k", today=T)
    assert w.status == W.INVALID and any("USER_INSTRUCTION" in p for p in w.problems)


def test_unknown_gate_and_red_lines_are_invalid():
    w = W.normalize("nope", "KOR", "all", _good(), source_key="k", today=T)
    assert w.status == W.INVALID and "未在 GATE_POLICIES 登记" in w.problems[0]
    for red in W.RED_LINES:
        r = W.normalize(red, "KOR", "all", _good(gate=red), source_key="k", today=T)
        assert r.status == W.INVALID and r.problems[0].startswith("RED_LINE")
        assert red not in W.GATE_POLICIES, "红线不得同时登记为可豁免闸"


def test_non_object_value_is_invalid():
    for bad in (None, 3, [], "not json"):
        assert W.normalize("semantic", "KOR", "all", bad, source_key="k", today=T).status == W.INVALID


# ----------------------------------------------------------------------------- 旧键
def test_legacy_key_semantics_are_preserved():
    ok = W.normalize("stop_rules", "GBR", "all", {"reason": "用户明示继续", "until": "2099-01-01"},
                     source_key="stop_rules_override", legacy=True, today=T)
    assert ok.active and ok.legacy and ok.expires_at == "2099-01-01" and not ok.warnings
    expired = W.normalize("stop_rules", "GBR", "all", {"reason": "过期", "until": "2000-01-01"},
                          source_key="stop_rules_override", legacy=True, today=T)
    assert expired.status == W.EXPIRED
    no_reason = W.normalize("stop_rules", "GBR", "all", {"until": "2099-01-01"},
                            source_key="stop_rules_override", legacy=True, today=T)
    assert no_reason.status == W.INVALID


def test_legacy_without_until_still_honored_but_flagged():
    w = W.normalize("backlog", "GBR", "all", {"reason": "用户明示"}, source_key="backlog_gate_override",
                    legacy=True, today=T)
    assert w.active and any("NO_EXPIRY" in x for x in w.warnings)
    assert any("NO_EXPIRY" in line for line in W.banner_lines([w]))


def test_legacy_garbage_until_fails_closed():
    w = W.normalize("stop_rules", "GBR", "all", {"reason": "x", "until": "永久"},
                    source_key="stop_rules_override", legacy=True, today=T)
    assert w.status == W.INVALID and any("无法解析" in p for p in w.problems)


# ----------------------------------------------------------------------------- 读取
def test_load_prefers_wave_specific_then_all_then_legacy():
    stop = _good(gate="stop_rules", reason_code="USER_INSTRUCTION", approved_by="user", expires_at="2026-10-10")
    conn = _conn([
        ("GBR", "stop_rules_override", {"reason": "legacy", "until": "2099-01-01"}),
        ("GBR", "waiver_stop_rules_GBR_all", stop),
    ])
    w = W.load(conn, "stop_rules", "GBR", today=T)
    assert w.source_key == "waiver_stop_rules_GBR_all"                 # 新键先于旧键
    conn.execute("DELETE FROM ledger_kv WHERE key='waiver_stop_rules_GBR_all'")
    assert W.load(conn, "stop_rules", "GBR", today=T).source_key == "stop_rules_override"
    assert W.load(conn, "stop_rules", "KOR", today=T) is None         # 别的区不串


def test_load_returns_first_bad_when_no_active_and_active_beats_bad():
    bad = _good(expires_at="2026-09-20", created_at="2026-09-19")
    conn = _conn([("KOR", "waiver_semantic_KOR_all", bad)])
    w = W.load(conn, "semantic", "KOR", today=T)
    assert w is not None and w.status == W.EXPIRED
    conn.execute("INSERT INTO ledger_kv VALUES (?,?,?)",
                 ("KOR", "waiver_semantic_KOR_97", json.dumps(_good())))
    assert W.load(conn, "semantic", "KOR", wave=97, today=T).active


def test_load_propagates_db_errors_instead_of_guessing():
    c = sqlite3.connect(":memory:")            # 没有 ledger_kv 表
    with pytest.raises(sqlite3.OperationalError):
        W.load(c, "semantic", "KOR", today=T)


def test_load_all_lists_new_legacy_and_bad_keys():
    conn = _conn([
        ("GBR", "stop_rules_override", {"reason": "x", "until": "2099-01-01"}),
        ("GBR", "waiver_backlog_GBR_all", _good(gate="backlog", reason_code="USER_INSTRUCTION",
                                                approved_by="user", expires_at="2026-10-10")),
        ("GBR", "waiver_madeup_GBR_all", {"reason": "x"}),
    ])
    got = {w.source_key: w.status for w in W.load_all(conn, "GBR", today=T)}
    assert got == {"stop_rules_override": W.ACTIVE, "waiver_backlog_GBR_all": W.ACTIVE,
                   "waiver_madeup_GBR_all": W.INVALID}


# ----------------------------------------------------------------------------- 写
def test_build_payload_validates_and_renders_mcp_call():
    p = W.build_payload("semantic", "kor", reason_code="NO_INPUT_AVAILABLE", reason="无描述文",
                        approved_by="agent", days=3, evidence="尝试记录", today=T)
    assert p["key"] == "waiver_semantic_KOR_all" and p["region"] == "KOR"
    assert p["value"]["expires_at"] == "2026-10-02"
    assert p["mcp_call"].startswith("mcp__wqb-db__upsert_ledger_key(region='KOR', key='waiver_semantic_KOR_all'")
    with pytest.raises(W.WaiverError):
        W.build_payload("semantic", "KOR", reason_code="NO_INPUT_AVAILABLE", reason="x",
                        approved_by="agent", days=30, evidence="e", today=T)     # 超上限 7 天
    with pytest.raises(W.WaiverError):
        W.build_payload("stop_rules", "GBR", reason_code="USER_INSTRUCTION", reason="x",
                        approved_by="agent", days=3, today=T)                    # 只允许 user


def test_record_writes_through_store():
    class Store:
        def __init__(self):
            self.calls = []

        def upsert_ledger(self, region, key, value):
            self.calls.append((region, key, value))

    s = Store()
    p = W.record(s, "diversity", "KOR", reason_code="REPAIR_BATCH", reason="repair 批复用同骨架",
                 approved_by="agent", days=2, wave="w31", today=T)
    assert s.calls == [("KOR", "waiver_diversity_KOR_w31", p["value"])]


# ----------------------------------------------------------------------------- 跳过检查 / 横幅
def test_check_skip_modes():
    conn = _conn()
    warn = W.check_skip(conn, "semantic", "KOR", 5, "--skip-semantic-gate", mode="warn", today=T)
    assert warn.ok and "无 waiver 记录" in warn.lines[0] and "waiver_semantic_KOR_5" in warn.lines[0]
    enforce = W.check_skip(conn, "semantic", "KOR", 5, "--skip-semantic-gate", mode="enforce", today=T)
    assert not enforce.ok
    off = W.check_skip(conn, "semantic", "KOR", 5, "--skip-semantic-gate", mode="off", today=T)
    assert off.ok and "未检查" in off.lines[0]
    conn.execute("INSERT INTO ledger_kv VALUES (?,?,?)", ("KOR", "waiver_semantic_KOR_all", json.dumps(_good())))
    with_wv = W.check_skip(conn, "semantic", "KOR", 5, "--skip-semantic-gate", mode="enforce", today=T)
    assert with_wv.ok and with_wv.waiver.active and "已有 waiver" in with_wv.lines[0]
    assert with_wv.to_dict()["waiver"]["gate"] == "semantic"


def test_check_skip_unreadable_ledger_fails_closed_under_enforce():
    bare = sqlite3.connect(":memory:")
    d = W.check_skip(bare, "diversity", "KOR", None, "--skip-diversity-gate", mode="enforce", today=T)
    assert not d.ok and "台账不可读" in d.lines[0]
    assert W.check_skip(bare, "diversity", "KOR", None, "--skip-diversity-gate", mode="warn", today=T).ok


def test_resolve_mode_precedence_and_invalid_falls_back():
    assert W.resolve_mode(None, {}) == "warn"
    assert W.resolve_mode(None, {"WQB_WAIVER_MODE": "enforce"}) == "enforce"
    assert W.resolve_mode("off", {"WQB_WAIVER_MODE": "enforce"}) == "off"
    assert W.resolve_mode("bogus", {"WQB_WAIVER_MODE": "bogus"}) == "warn"


def test_gate_report_fields_shape_is_backward_compatible():
    w = W.normalize("stop_rules", "GBR", "all", {"reason": "用户明示继续", "until": "2099-01-01"},
                    source_key="stop_rules_override", legacy=True, today=T)
    f = W.gate_report_fields(w)
    assert f["override"] == {"reason": "用户明示继续", "until": "2099-01-01"}      # 既有测试断言的形状
    assert f["waiver"]["source_key"] == "stop_rules_override"
    expired = W.normalize("stop_rules", "GBR", "all", {"reason": "x", "until": "2000-01-01"},
                          source_key="stop_rules_override", legacy=True, today=T)
    assert "override" not in W.gate_report_fields(expired)                          # 过期不放行
    assert "已过期" in W.rejected_note(expired) or "EXPIRED" in W.rejected_note(expired)
    assert W.gate_report_fields(None) == {} and W.rejected_note(None) == ""


def test_write_hint_names_key_limits_and_legacy():
    h = W.write_hint("stop_rules", "gbr")
    assert "waiver_stop_rules_GBR_all" in h and "≤30 天" in h and "stop_rules_override" in h
    assert "stop_rules_override" not in W.write_hint("semantic", "KOR")


def test_every_flag_maps_to_a_registered_gate_and_policy_is_sane():
    for flag, gate in W.FLAG_TO_GATE.items():
        assert gate in W.GATE_POLICIES, (flag, gate)
    for g, pol in W.GATE_POLICIES.items():
        assert pol.gate == g and pol.max_days > 0 and set(pol.approvers) <= set(W.APPROVERS)
        assert pol.flags, f"{g} 没有登记逃生口（flags）——文档无从引用"


def test_index_switch_table_is_generated_from_gate_policies():
    """INDEX.md 的「闸与逃生口总表」必须等于 render_switch_table()（改政策先改注册表再重生成）。"""
    import re
    from pathlib import Path
    idx = (Path(__file__).resolve().parents[3] / "Claude" / "skills" / "INDEX.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- switch-table:start -->\n(.*?)\n<!-- switch-table:end -->", idx, re.S)
    assert m, "INDEX.md 缺 switch-table 块"
    assert m.group(1).strip() == W.render_switch_table().strip(), \
        "INDEX 的总表与 GATE_POLICIES 不一致：python tools/waiver.py gates --markdown 重新生成后替换"


def test_switch_table_escapes_pipes_and_lists_every_gate():
    t = W.render_switch_table()
    for g in W.GATE_POLICIES:
        assert f"`{g}`" in t
    for line in t.splitlines()[2:]:
        # 7 列 = 8 个未转义竖线（首尾各一）
        assert len(re.split(r"(?<!\\)\|", line)) - 1 == 8, line


def test_policy_defaults_agree_with_code_where_derivable():
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(root / "tools"))
    import wave_gate
    assert wave_gate.DEFAULT_INSPECT_MODE in W.GATE_POLICIES["inspect"].default
    # 包化后 SEM 模式解析在 wave_gate_pkg/cli.py，同时读 shim + pkg
    parts = []
    for rel in ("tools/wave_gate.py", "tools/wave_gate_pkg/cli.py"):
        p = root / rel
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
    src = "\n".join(parts)
    assert 'or "enforce"' in src and "enforce" in W.GATE_POLICIES["semantic"].default   # 闸 SEM 缺省 enforce
    assert W.DEFAULT_MODE == "warn"
