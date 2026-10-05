# -*- coding: utf-8 -*-
"""2026-10-02 步 6 P0/P1 回归：提交期失败重发 + 波末完成度闸。

背景（评估实证）：
- P0：`_run_round` Phase 1 提交抛异常（429/网络）时，旧代码只写 `SUBMIT_FAIL` 就丢弃，
  不进 `_retry_queue`，同一次 run 内永不重发。全库 42 批 = 330 条表达式静默丢失；
  GBR s2_institutions6_d1 闸过 93 却只入库 83。
- P1：§6.5「backtest_results 行数 = 波内表达式数」此前无任何代码校验，丢批零告警。

本测试纯本地：api / submit_batch / poll / store 全部打桩，不联网、不写库。
"""
import importlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _pipeline_mod():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))
    for m in ("pipeline", "review_wave", "metrics_cache", "gate", "_lib.rules",
              "_lib.region_kb", "_lib.wqb_store", "_lib.ledger", "_lib.common",
              "_lib.api", "_lib.poller", "_lib"):
        sys.modules.pop(m, None)
    return importlib.import_module("pipeline")


# ---------------------------------------------------------------- 错误可重发判定（纯函数）

def test_is_retryable_submit_error_classification():
    pl = _pipeline_mod()
    assert pl._is_retryable_submit_error("HTTP Error 429: Too Many Requests") is True
    assert pl._is_retryable_submit_error("503 Service Unavailable") is True
    assert pl._is_retryable_submit_error("HTTP Error 502: Bad Gateway") is True
    assert pl._is_retryable_submit_error("<urlopen error timed out>") is True
    assert pl._is_retryable_submit_error("Connection reset by peer") is True
    # 不可重发：4xx 其它（重发只会烧时间）
    assert pl._is_retryable_submit_error("HTTP Error 400: Bad Request") is False
    assert pl._is_retryable_submit_error("HTTP Error 403: Forbidden") is False
    assert pl._is_retryable_submit_error("") is False
    assert pl._is_retryable_submit_error(None) is False


def test_batch_key_is_order_sensitive_and_stable():
    pl = _pipeline_mod()
    assert pl._batch_key(["a", "b"]) == pl._batch_key(["a", "b"])
    assert pl._batch_key(["a", "b"]) != pl._batch_key(["b", "a"])


# ---------------------------------------------------------------- P0：提交期失败进重发队列

class _Ctx:
    region = "GBR"
    settings = {"region": "GBR", "universe": "TOP1200"}

    def thresh(self, k):
        return {"review": {"sharpe": 1.25, "fitness": 1.0, "turnover": [0.01, 0.7]},
                "near": {"sharpe_min": 1.0}}.get(k, {})


def _install_fakes(pl, monkeypatch, plan, fail_plan=None):
    """plan: msid -> (status, detail)。fail_plan: submit 第 N 次（1-based）→ 抛的异常。

    fake_submit 按「成功提交序号」取 msid；fail_plan 命中时抛异常不消耗 msid。
    """
    order = list(plan.keys())
    submitted = []
    call_no = {"n": 0}

    def fake_submit(api, settings, exprs):
        call_no["n"] += 1
        if fail_plan and call_no["n"] in fail_plan:
            raise RuntimeError(fail_plan[call_no["n"]])
        msid = order[len(submitted)]
        submitted.append((msid, [pl.item_expr(e) for e in exprs]))
        return msid

    def fake_poll(api, msid, pcfg, bi):
        st, detail = plan[msid]
        return bi, st, detail

    def fake_update(ck, bi, batch, msid, status, detail, api):
        rec = next((b for b in ck["batches"] if b.get("multisim") == msid), None)
        if not rec:
            rec = {"exprs": batch, "multisim": msid}
            ck["batches"].append(rec)
        rec["status"] = status
        if status == "COMPLETE":
            rec["alphas"] = ["A" + msid]
        return rec

    monkeypatch.setattr(pl, "submit_batch", fake_submit)
    monkeypatch.setattr(pl, "_poll_single_batch", fake_poll)
    monkeypatch.setattr(pl, "_update_ck_batch", fake_update)
    monkeypatch.setattr(pl, "ckpt_save", lambda ctx, ck, d: None)
    monkeypatch.setenv("WQB_GLOBAL_SLOTS", "0")
    return submitted


def test_submit_429_is_retried_and_eventually_completes(monkeypatch):
    """首批提交 429 → 自动重发 → 成功 COMPLETE（不再丢批）。"""
    pl = _pipeline_mod()
    plan = {"ms1": ("COMPLETE", {"children": []})}
    # 第 1 次提交抛 429，第 2 次（重发）成功
    submitted = _install_fakes(pl, monkeypatch, plan,
                               fail_plan={1: "HTTP Error 429: Too Many Requests"})
    ck = {"wave": "w1", "batches": [], "item_overrides": {}}
    completed, failed, _ = pl._run_round(
        api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(a)", "rank(b)"]],
        n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[], max_submit_retry=2)
    assert submitted == [("ms1", ["rank(a)", "rank(b)"])]        # 重发成功
    assert completed == 1 and failed == 0
    assert not [b for b in ck["batches"] if b.get("status") == "SUBMIT_FAIL"]


def test_submit_429_exhausts_retry_then_submit_fail(monkeypatch):
    """持续 429 → 重发至上限后落 SUBMIT_FAIL（可见、可由重跑续命），不无限重发。"""
    pl = _pipeline_mod()
    plan = {}   # 永不成功
    submitted = _install_fakes(pl, monkeypatch, plan,
                               fail_plan={1: "HTTP Error 429: Too Many Requests",
                                          2: "HTTP Error 429: Too Many Requests",
                                          3: "HTTP Error 429: Too Many Requests",
                                          4: "HTTP Error 429: Too Many Requests"})
    ck = {"wave": "w1", "batches": [], "item_overrides": {}}
    completed, failed, _ = pl._run_round(
        api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(a)"]],
        n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[], max_submit_retry=2)
    assert submitted == []                                       # 从未成功
    # 3 次尝试（原始 + 2 次重发）→ 落 1 条 SUBMIT_FAIL
    fails = [b for b in ck["batches"] if b.get("status") == "SUBMIT_FAIL"]
    assert len(fails) == 1 and fails[0]["exprs"] == ["rank(a)"]
    assert completed == 0


def test_non_retryable_submit_error_goes_straight_to_fail(monkeypatch):
    """400（载荷非法）不可重发 → 一次尝试即落 SUBMIT_FAIL，不浪费重发。"""
    pl = _pipeline_mod()
    plan = {}
    submitted = _install_fakes(pl, monkeypatch, plan,
                               fail_plan={1: "HTTP Error 400: Bad Request",
                                          2: "HTTP Error 429: Too Many Requests"})
    ck = {"wave": "w1", "batches": [], "item_overrides": {}}
    pl._run_round(api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(a)"]],
                  n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[],
                  max_submit_retry=2)
    fails = [b for b in ck["batches"] if b.get("status") == "SUBMIT_FAIL"]
    assert len(fails) == 1 and "400" in fails[0]["error"]
    assert submitted == []


def test_all_phase1_failed_bootstrap_refills_from_retry_queue(monkeypatch):
    """Phase 1 全失败（futures 空）但重发队列非空 → 引导补批，不能被 `while futures` 吞掉。"""
    pl = _pipeline_mod()
    plan = {"ms1": ("COMPLETE", {"children": []}), "ms2": ("COMPLETE", {"children": []})}
    # 两批都在首轮 429，重发后都成功
    submitted = _install_fakes(pl, monkeypatch, plan,
                               fail_plan={1: "HTTP Error 429: socket", 2: "HTTP Error 429: socket"})
    ck = {"wave": "w1", "batches": [], "item_overrides": {}}
    completed, failed, _ = pl._run_round(
        api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(a)"], ["rank(b)"]],
        n_slots=2, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[], max_submit_retry=2)
    assert set(m for m, _ in submitted) == {"ms1", "ms2"}
    assert completed == 2 and failed == 0
    assert not [b for b in ck["batches"] if b.get("status") == "SUBMIT_FAIL"]


def test_serial_single_slot_retry_does_not_deadlock(monkeypatch):
    """n_slots=1（--serial）下，重发批占满唯一槽位时循环仍能推进、正常收尾。"""
    pl = _pipeline_mod()
    plan = {"ms1": ("COMPLETE", {"children": []}), "ms2": ("COMPLETE", {"children": []})}
    # 首批 429（重发），第二批即首轮第二槽队列里的（_pending）
    submitted = _install_fakes(pl, monkeypatch, plan,
                               fail_plan={1: "HTTP Error 429: throttle"})
    ck = {"wave": "w1", "batches": [], "item_overrides": {}}
    completed, failed, _ = pl._run_round(
        api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(a)"]],
        n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1,
        pending_batches=[["rank(b)"]], max_submit_retry=2)
    assert set(m for m, _ in submitted) == {"ms1", "ms2"}
    assert completed == 2 and failed == 0


def test_submit_retry_batch_can_still_be_isolated_on_error(monkeypatch):
    """提交期重发批若 ERROR，仍应走连坐隔离（它此前根本没跑起来）——不被 _isolation_retry 挡。"""
    pl = _pipeline_mod()
    errs = [{"child": "x", "status": "ERROR", "error": "Invalid field", "expr": "rank(bad)"},
            {"child": "y", "status": "CANCELLED", "error": "CANCELLED", "expr": "rank(ok)"}]
    plan = {"ms1": ("COMPLETE", {"children": []}),          # 重发后跑起来但 ERROR
            "ms2": ("COMPLETE", {"children": []})}          # 隔离后的无辜兄弟重发
    monkeypatch.setattr(pl, "_isolate_error_batch", lambda b, e: (
        [{"expr": "rank(bad)", "error": "Invalid field"}], ["rank(ok)"]))
    monkeypatch.setattr(pl, "_mark_culprits_in_db", lambda ctx, wave, c: len(c))
    submitted = _install_fakes(pl, monkeypatch, plan,
                               fail_plan={1: "HTTP Error 429: Too Many Requests"})
    # 让 ms1 的 poll 返回 ERROR
    orig_poll = pl._poll_single_batch

    def poll_error(api, msid, pcfg, bi):
        if msid == "ms1":
            return bi, "ERROR", {"children": ["x", "y"]}
        return orig_poll(api, msid, pcfg, bi)
    monkeypatch.setattr(pl, "_poll_single_batch", poll_error)
    monkeypatch.setattr(pl, "_update_ck_batch", lambda ck, bi, batch, msid, status, detail, api: (
        {"exprs": batch, "multisim": msid, "status": status,
         "errors": errs if status == "ERROR" else [], "alphas": ["A"] if status == "COMPLETE" else []}))

    ck = {"wave": "w1", "batches": [], "item_overrides": {}}
    pl._run_round(api=None, ctx=_Ctx(), ck=ck, round_batches=[["rank(bad)", "rank(ok)"]],
                  n_slots=1, pcfg={}, checkpoint_dir=None, round_idx=1, pending_batches=[],
                  max_submit_retry=2)
    # 提交序列：ms1（重发成功）→ ms2（隔离重发）
    assert [m for m, _ in submitted] == ["ms1", "ms2"]
    assert submitted[1] == ("ms2", ["rank(ok)"])


# ---------------------------------------------------------------- P1：完成度闸（纯函数）

def test_completeness_ok_when_saved_equals_planned():
    pl = _pipeline_mod()
    ck = {"stages": {"gate": {"passed": [{"expr": "a"}, {"expr": "b"}, {"expr": "c"}]}},
          "batches": [{"status": "COMPLETE"}]}
    r = pl.check_backtest_completeness(ck, n_saved=3)
    assert r["planned"] == 3 and r["saved"] == 3 and r["missing"] == 0
    assert r["ok"] is True and r["warn"] is False


def test_completeness_warns_on_missing_rows():
    pl = _pipeline_mod()
    ck = {"stages": {"gate": {"passed": [{"expr": str(i)} for i in range(93)]}},
          "batches": [{"status": "SUBMIT_FAIL"}] * 2}
    r = pl.check_backtest_completeness(ck, n_saved=83)
    assert r["planned"] == 93 and r["saved"] == 83 and r["missing"] == 10
    assert r["submit_fail_batches"] == 2
    assert r["warn"] is True and r["ok"] is False


def test_completeness_tolerates_small_gap_when_configured():
    pl = _pipeline_mod()
    ck = {"stages": {"gate": {"passed": [{"expr": str(i)} for i in range(10)]}}, "batches": []}
    r = pl.check_backtest_completeness(ck, n_saved=9, tolerance=1)
    assert r["warn"] is False and r["ok"] is True


def test_completeness_noop_when_no_gate_stage():
    pl = _pipeline_mod()
    r = pl.check_backtest_completeness({"batches": []}, n_saved=0)
    assert r["planned"] == 0 and r["ok"] is True and r["warn"] is False


# ---------------------------------------------------------------- P1：接线（源码契约 + 端到端打桩）

def test_stage_review_calls_completeness_helper():
    """源码契约：stage_review 两处 save_backtest_results 后都要调 _report_completeness。"""
    src = (TOOLKIT_SCRIPTS / "pipeline.py").read_text(encoding="utf-8")
    assert src.count("_report_completeness(ctx, ck, n_saved)") == 2
    # 完成度结果要落 checkpoint
    assert '"completeness": completeness' in src


def test_report_completeness_reads_live_rows(monkeypatch):
    """_report_completeness 以库里本波实际行数为准（非本次 upsert 数）。"""
    pl = _pipeline_mod()
    monkeypatch.setattr(pl, "_count_wave_backtest_rows", lambda ctx, wave: 83)
    ck = {"wave": "w1", "stages": {"gate": {"passed": [{"expr": str(i)} for i in range(93)]}},
          "batches": [{"status": "SUBMIT_FAIL"}]}
    r = pl._report_completeness(_Ctx(), ck, n_saved=83)
    assert r["saved"] == 83 and r["live_rows"] == 83 and r["warn"] is True


def test_report_completeness_degrades_when_db_unreachable(monkeypatch):
    """库不可达（live=None）→ 退回用 upsert 计数，不抛异常。"""
    pl = _pipeline_mod()
    monkeypatch.setattr(pl, "_count_wave_backtest_rows", lambda ctx, wave: None)
    ck = {"wave": "w1", "stages": {"gate": {"passed": [{"expr": "a"}]}}, "batches": []}
    r = pl._report_completeness(_Ctx(), ck, n_saved=1)
    assert r["saved"] == 1 and r["live_rows"] is None and r["warn"] is False
