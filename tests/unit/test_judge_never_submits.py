# -*- coding: utf-8 -*-
"""brain-alpha-judge 是参考层：**不提交、不默认外发**（skills 审查 T0-5 / T0-15 / X-9，2026-09-29）。

事故背景：vendored AceClient.get_submit_verdict 曾先 `POST /alphas/{id}/submit` 再 GET，而
judge_alpha.baseline_from_platform 每跑一次就调用它——评审一次就真的提交一次候选（通过的 POST 不可撤销），
其后的 NameError 还被外层 try/except 吞掉，事故无痕。另：LLM 层缺省开启且载荷含表达式原文。
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
JUDGE = ROOT / "Claude" / "skills" / "brain-alpha-judge"
SCRIPTS = JUDGE / "scripts"
VENDOR = SCRIPTS / "vendor"


def _load(name, path):
    for p in (str(VENDOR), str(SCRIPTS)):
        if p not in sys.path:
            sys.path.insert(0, p)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod            # dataclass（from __future__ import annotations）解析注解时要在 sys.modules 里找到本模块
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def ace():
    return _load("ace_client_under_test", VENDOR / "ace_client.py")


@pytest.fixture(scope="module")
def judge():
    return _load("judge_alpha_under_test", SCRIPTS / "judge_alpha.py")


class _Resp:
    def __init__(self, status=404, text=""):
        self.status_code, self.text, self.headers = status, text, {}

    def json(self):
        return json.loads(self.text) if self.text else {}


class _Session:
    def __init__(self):
        self.calls = []

    def _rec(self, method, url, **kw):
        self.calls.append((method, url))
        return _Resp()

    def get(self, url, **kw):
        return self._rec("GET", url, **kw)

    def post(self, url, **kw):
        return self._rec("POST", url, **kw)

    def request(self, method, url, **kw):
        return self._rec(method.upper(), url, **kw)


def _client(ace):
    c = ace.AceClient.__new__(ace.AceClient)       # 不走认证（无网络）
    c.base_url = "https://api.example.invalid"
    c.session = _Session()
    return c


# ── 不提交 ────────────────────────────────────────────────────────────────────
def test_get_submit_verdict_is_read_only(ace):
    c = _client(ace)
    out = c.get_submit_verdict("ABC123")
    methods = [m for m, _ in c.session.calls]
    assert methods == ["GET"], f"get_submit_verdict 只允许 GET，实际 {c.session.calls}"
    assert out["post_status"] is None and out["final_success"] is False


def test_submit_alpha_removed_and_sends_nothing(ace):
    c = _client(ace)
    with pytest.raises(RuntimeError, match="已移除"):
        c.submit_alpha("ABC123")
    assert c.session.calls == []


def test_confirm_submit_flag_fails_loudly_before_any_network(judge, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["judge_alpha.py", "--alpha-id", "ABC123", "--confirm-submit"])
    assert judge.main() == 2
    err = capsys.readouterr().err
    assert "已移除" in err and "workflow_submit_alpha" in err


@pytest.mark.parametrize("path", sorted(SCRIPTS.rglob("*.py")), ids=lambda p: str(p.relative_to(SCRIPTS)))
def test_no_script_posts_to_submit(path):
    """静态守护：judge 目录下任何脚本都不得出现对 /submit 的 POST，或 submit_alpha( 的调用点。"""
    text = path.read_text(encoding="utf-8")
    code = "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("#"))
    assert not re.search(r"\.post\([^)]*/submit", code), f"{path.name} 含 POST …/submit"
    for m in re.finditer(r"\bsubmit_alpha\s*\(", code):
        line = code[: m.start()].count("\n")
        ctx = code.splitlines()[line]
        assert "def submit_alpha" in ctx, f"{path.name} 调用了 submit_alpha：{ctx.strip()}"


# ── PPA 口径 ──────────────────────────────────────────────────────────────────
def _alpha(sharpe, fitness=1.2, two_year=None, **kw):
    checks = [] if two_year is None else [{"name": "LOW_2Y_SHARPE", "result": "PASS", "value": two_year}]
    d = {"type": "REGULAR", "is": {"sharpe": sharpe, "fitness": fitness, "checks": checks}}
    d.update(kw)
    return d


def test_regular_uses_internal_line(judge):
    names = [f["name"] for f in judge.internal_hard_gate_failures(_alpha(1.4, fitness=0.9))]
    assert names == ["LOW_SHARPE", "LOW_FITNESS"]


def test_ppa_is_not_judged_by_the_regular_line(judge):
    # PPA：Sharpe∈[1.0,1.58) 合法；此前被 1.58 判 BLOCK
    assert judge.internal_hard_gate_failures(_alpha(1.2, fitness=0.4, type="PPA")) == []
    assert judge.internal_hard_gate_failures(_alpha(1.2, tags=["PowerPoolSelected"])) == []
    bad = judge.internal_hard_gate_failures(_alpha(0.9, type="PPA"))
    assert [f["name"] for f in bad] == ["LOW_SHARPE"] and bad[0]["limit"] == 1.0


def test_thresholds_match_config():
    """judge 的数值必须等于 wqb.config / submit_queue（X-11：阈值字面量不得漂移）。"""
    if str(ROOT / "src") not in sys.path:
        sys.path.insert(0, str(ROOT / "src"))
    from wqb.config import GATES_INTERNAL
    from wqb.store.submit_queue import LIM
    j = _load("judge_alpha_cfg", SCRIPTS / "judge_alpha.py").INTERNAL_HARD_GATES
    assert j["sharpe_min"] == GATES_INTERNAL["sharpe_min"]
    assert j["fitness_min"] == GATES_INTERNAL["fitness_min"]
    assert j["two_year_min"] == LIM["two_year"]
    # PPA 线 = compute_webdata_failed_counts 里 LOW_SHARPE 的 value<1
    from wqb.config import compute_webdata_failed_counts
    just_ok = [{"name": "LOW_SHARPE", "result": "PASS", "value": j["ppa_sharpe_min"]}]
    just_bad = [{"name": "LOW_SHARPE", "result": "PASS", "value": j["ppa_sharpe_min"] - 0.01}]
    assert compute_webdata_failed_counts(just_ok)["failed_ppa"] == 0
    assert compute_webdata_failed_counts(just_bad)["failed_ppa"] == 1


# ── 外发缺省关闭 ──────────────────────────────────────────────────────────────
def test_llm_is_off_by_default_and_ignores_generic_openai_key(monkeypatch):
    llm = _load("llm_judge_under_test", VENDOR / "llm_judge.py")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-should-not-be-used")
    monkeypatch.delenv("BRAIN_JUDGE_LLM_API_KEY", raising=False)
    j = llm.LlmJudge({})
    assert j.enabled is False and j.api_key == ""
    assert j.decide({"candidate": {}}) == {"available": False, "reason": "disabled_by_config"}
    j2 = llm.LlmJudge({"enabled": True})
    assert j2.api_key == ""                       # 通用 OPENAI_API_KEY 不再被隐式使用
    assert j2.decide({"candidate": {}})["reason"] == "missing_api_key"


def test_llm_payload_withholds_expression_by_default(judge):
    kw = dict(alpha_id="A1", platform={"expression": "rank(ts_delta(close, 5))", "checks": [], "failed_checks": []},
              extra={}, heuristics={"operator_count": 2}, trend_block={}, projection_block={},
              corpus_materials=[], deterministic="REVIEW")
    default = judge.build_llm_payload(**kw)
    assert "ts_delta" not in json.dumps(default, ensure_ascii=False)
    opted_in = judge.build_llm_payload(send_expression=True, **kw)
    assert opted_in["candidate"]["expression"] == "rank(ts_delta(close, 5))"


def test_example_config_ships_egress_off():
    cfg = json.loads((JUDGE / "configs" / "config.example.json").read_text(encoding="utf-8"))
    llm = cfg["judge"]["llm"]
    assert llm["enabled"] is False and llm["send_expression"] is False
    assert not llm.get("api_key")


# ---------------------------------------------------------------------------
# 2026-09-29（JD-07 / JD-10）：凭据只读进程环境变量；LLM 只能收紧判定；降级运行有标记
# ---------------------------------------------------------------------------

@pytest.fixture()
def creds():
    return _load("judge_load_credentials_under_test", VENDOR / "load_credentials.py")


def _clear_cred_env(monkeypatch):
    for k in ("CREDENTIALS_EMAIL", "CREDENTIALS_PASSWORD", "BRAIN_USERNAME", "BRAIN_EMAIL", "BRAIN_PASSWORD"):
        monkeypatch.delenv(k, raising=False)


def test_credentials_come_from_process_env_only(creds, monkeypatch, tmp_path):
    _clear_cred_env(monkeypatch)
    monkeypatch.setenv("CREDENTIALS_EMAIL", "a@example.invalid")
    monkeypatch.setenv("CREDENTIALS_PASSWORD", "pw-from-env")
    got = creds.load_credentials(skill_dir=tmp_path)
    assert (got.username, got.password) == ("a@example.invalid", "pw-from-env")


def test_legacy_env_aliases_still_work(creds, monkeypatch, tmp_path):
    _clear_cred_env(monkeypatch)
    monkeypatch.setenv("BRAIN_USERNAME", "b@example.invalid")
    monkeypatch.setenv("BRAIN_PASSWORD", "pw2")
    assert creds.load_credentials(skill_dir=tmp_path).username == "b@example.invalid"


def test_plaintext_credentials_in_config_file_are_not_used_and_not_printed(creds, monkeypatch, tmp_path, capsys):
    _clear_cred_env(monkeypatch)
    monkeypatch.setenv("HOME", str(tmp_path))            # 隔离 ~/secrets
    (tmp_path / "configs").mkdir()
    (tmp_path / "configs" / "config.json").write_text(
        json.dumps({"username": "leak@example.invalid", "password": "SECRET-IN-FILE"}), encoding="utf-8")
    with pytest.raises(RuntimeError, match="CREDENTIALS_EMAIL"):
        creds.load_credentials(skill_dir=tmp_path)
    err = capsys.readouterr().err
    assert "configs/config.json" in err and "SECRET-IN-FILE" not in err and "leak@example.invalid" not in err


def test_home_secrets_file_is_no_longer_a_credential_source(creds, monkeypatch, tmp_path):
    _clear_cred_env(monkeypatch)
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / "secrets").mkdir()
    (tmp_path / "secrets" / "platform-brain.json").write_text(
        json.dumps({"email": "x@example.invalid", "password": "pw"}), encoding="utf-8")
    with pytest.raises(RuntimeError):
        creds.load_credentials(skill_dir=tmp_path / "nowhere", allow_home_secrets=True)


def test_example_config_carries_no_credential_fields():
    cfg = json.loads((JUDGE / "configs" / "config.example.json").read_text(encoding="utf-8"))
    assert "username" not in cfg and "password" not in cfg
    assert cfg["judge"]["llm"]["enabled"] is False and cfg["judge"]["llm"]["api_key"] == ""


def test_llm_key_only_from_dedicated_env_var(monkeypatch):
    lj = _load("llm_judge_under_test", VENDOR / "llm_judge.py")
    monkeypatch.delenv("BRAIN_JUDGE_LLM_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "should-not-be-used")
    j = lj.LlmJudge({"enabled": True, "api_key": "key-in-config-file"})
    assert j.api_key == "" and j.config_key_ignored is True
    out = j.decide({"candidate": {}})
    assert out["available"] is False and "BRAIN_JUDGE_LLM_API_KEY" in out["reason"]


def test_llm_can_only_tighten_the_deterministic_verdict(judge):
    s = judge.stricter_verdict
    assert s("READY", "REVIEW") == "REVIEW"      # 乐观的 LLM 不能把平台数据缺失的 REVIEW 抬成 READY
    assert s("READY", "BLOCK") == "BLOCK"
    assert s("BLOCK", "READY") == "BLOCK"        # LLM 更严则采纳
    assert s("REVIEW", "REVIEW") == "REVIEW"


def test_degraded_report_is_flagged_in_markdown(judge):
    result = {"candidate_label": "x", "alpha_id": "", "platform": {"available": False, "failed_checks": []},
              "extra": {"overall": "review", "rules": []}, "degraded": {"is_degraded": True, "reasons": ["no_credentials_or_client"]},
              "value_factor_trend": {}, "value_factor_projection": {}, "expression_analysis": {}, "suggestions": []}
    md = judge.render_markdown(result)
    assert "降级运行" in md.splitlines()[2] and "不得作为提交依据" in md


def test_notes_from_three_section_description(judge):
    desc = ("Idea: Buy stocks whose analyst revisions accelerate.\n\n"
            "Rationale for data used: Revisions lead price.\n\n"
            "Rationale for operators used: ts_rank smooths noise.")
    got = judge.notes_from_description(desc)
    assert got["idea_summary"] == "Buy stocks whose analyst revisions accelerate."
    assert got["rationale"] == "Revisions lead price. ts_rank smooths noise."


@pytest.mark.parametrize("bad", [None, "", "no headers at all", 123])
def test_notes_from_description_tolerates_missing_or_odd_input(judge, bad):
    assert judge.notes_from_description(bad) == {}


def test_alpha_id_mode_rubric_is_no_longer_doomed_when_platform_has_a_description(judge):
    """economic_foundation 的必填字段由平台 description 补上，不再恒失败。"""
    rubric = json.loads((JUDGE / "data" / "extra_submission_rubric.json").read_text(encoding="utf-8"))
    cand = {"alpha_id": "A1"}
    for k, v in judge.notes_from_description("Idea: x y.\n\nRationale for data used: a.\n\nRationale for operators used: b.").items():
        cand[k] = v
    ok, missing = judge.evaluate_required_fields(cand, ["idea_summary", "rationale"])
    assert ok and not missing
    assert rubric[0]["id"] == "economic_foundation"
