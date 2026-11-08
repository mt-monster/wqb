# -*- coding: utf-8 -*-
"""Step 1.8（分散度审查）在 `run()` 里的接线守护。

背景：2026-11-08 用 **124 颗已提交 USA alpha 的真实 OS 数据**检验「哪种提交标准真的影响
Combined Alpha Performance」，结论推翻了两条当时的直觉提案：

  · 所有 IS 读数对 OS 的秩相关都接近 0：Sharpe +0.007、Fitness +0.003、margin +0.068、
    sub_universe −0.057、**two_year −0.146（反向）** ⇒ 拿 IS 指标排序等于随机；
  · margin 对 −Turnover 的 ρ = **+0.922**，且 margin ≈ Returns/(504×Turnover)（逐颗误差 <1%）
    ⇒ 它只是「低换手」的代理，不是独立信息。

`CAP ≈ (μ̄/σ̄)·sqrt(N/(1+(N-1)ρ̄))`，有效宽度饱和于 `1/ρ̄` ⇒ **降 ρ 比增 N 有效**。
所以本步只锁两件事：self 软线 0.55，以及「高相关候选必须用 ΔS ≥ +0.02 补偿」。
`force=True` **可豁免**（自设纪律，非平台红线）。

本文件锁的是**接线行为**：分级正确、阻断早于副作用、豁免留痕、不可判定时 fail-open。
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT / "src",):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.workflow.nodes import submit_alpha as SA  # noqa: E402


CODE = "group_rank(ts_zscore(pv103_ivam_sum, 66), sector)"


def _detail(self_corr, *, checks=None):
    d = {
        "id": "TESTALPHA1",
        "status": "UNSUBMITTED",
        "type": "REGULAR",
        "settings": {"region": "GBR", "universe": "TOP700", "delay": 1},
        "regular": {"operatorCount": 3, "code": CODE},
        "is": {
            "sharpe": 2.0, "fitness": 1.5, "turnover": 0.15,
            "checks": checks if checks is not None else [
                {"name": "LOW_SHARPE", "result": "PASS"},
                {"name": "LOW_2Y_SHARPE", "result": "PASS"},
            ],
        },
    }
    if self_corr is not None:
        d["is"]["selfCorrelation"] = self_corr
    return d


class _FakeClient:
    def __init__(self, detail, before=2.0, after=2.3, self_probe=None):
        self._detail = detail
        self._before = before
        self._after = after
        self._self_probe = self_probe   # 主动 self 检查的返回值（None ⇒ 返回空体）
        self.self_probe_calls = 0

    async def get_alpha_details(self, alpha_id):
        return self._detail

    async def submit_alpha(self, alpha_id):
        return {"success": True, "status_code": 200,
                "message": "Alpha submitted; IS checks passed"}

    async def check_correlation(self, alpha_id, correlation_type="both", **kw):
        if correlation_type == "self":
            self.self_probe_calls += 1
            if self._self_probe is None:
                return {}
            return {"checks": {"self": {"max_correlation": self._self_probe}}}
        return {}

    async def performance_comparison(self, alpha_id):
        if self._before is None:
            return {}
        return {"partitionName": "EQUITY:GBR:1",
                "stats": {"before": {"sharpe": self._before, "fitness": 1.2,
                                     "turnover": 0.15, "returns": 0.08, "drawdown": 0.05},
                          "after": {"sharpe": self._after, "fitness": 1.3,
                                    "turnover": 0.15, "returns": 0.09, "drawdown": 0.04}}}

    def __getattr__(self, name):
        async def _noop(*a, **k):
            return {}
        return _noop


def _run(monkeypatch, self_corr, *, confirm_submit=False, force=False,
         before=2.0, after=2.3, local_cache=None):
    client = _FakeClient(_detail(self_corr), before=before, after=after)
    monkeypatch.setattr(SA, "_get_brain_client", lambda: client)
    monkeypatch.setattr(SA, "ALLOW_ALPHA_SUBMIT", True)
    # 本地库兜底：默认无缓存；传 local_cache 即模拟库里有历史读数
    monkeypatch.setattr(SA, "_local_self_corr", lambda aid: local_cache)
    monkeypatch.setattr(SA, "_submit_gate", lambda *a, **k: {
        "step": "submit_gate", "passed": True, "blocked": False,
        "robustness": {"recorded": True, "verdict": "PASS"}})
    monkeypatch.setattr(SA, "_quota_gate", lambda *a, **k: {
        "allowed": True, "used": 1, "limit": 4, "remaining": 3})
    monkeypatch.setattr(SA, "_prod_gate", lambda *a, **k: {
        "allowed": True, "prod_max": 0.5, "threshold": 0.7})
    monkeypatch.setattr(SA, "_poll_status", lambda *a, **k: "ACTIVE")
    monkeypatch.setattr(SA, "_finalize", lambda r, s, a, **k: r)
    return SA.run(alpha_id="TESTALPHA1", confirm_submit=confirm_submit, force=force,
                  _context={})


def _div(result):
    for s in result.get("steps") or []:
        if s.get("step") == "diversity_audit":
            return s
    return None


# ---------------- 分级判定 ----------------

def test_low_self_is_light_and_passes(monkeypatch):
    """self < 0.55 ⇒ light，免检放行（ΔS 只有 0 也不触发软闸）。

    注意不能把 ΔS 设成负数 —— 那会先被 Step 1.7 的硬闸拦下，Step 1.8 根本跑不到
    （`test_step17_runs_before_step18` 专门锁这个顺序）。
    """
    r = _run(monkeypatch, 0.20, confirm_submit=True, before=2.0, after=2.0)
    s = _div(r)
    assert s is not None, "未产出 diversity_audit"
    assert s["level"] == "light" and s["available"] is True
    assert s.get("blocked") is None
    assert s["width_share"] == 0.8
    assert r.get("blocked") is not True


def test_step17_runs_before_step18(monkeypatch):
    """ΔS<0 时由 Step 1.7 先拦，Step 1.8 不执行（顺序即优先级）。"""
    r = _run(monkeypatch, 0.20, confirm_submit=True, before=3.0, after=2.9)
    assert r.get("blocked") is True
    assert r.get("reason", "").startswith("marginal_contribution blocked")
    assert _div(r) is None, "Step 1.7 已返回，Step 1.8 不该执行"


def test_high_self_with_weak_delta_blocks(monkeypatch):
    """self ≥ 0.55 且 ΔS < +0.02 ⇒ blocked（真提交时）。"""
    r = _run(monkeypatch, 0.62, confirm_submit=True, before=2.0, after=2.005)  # ΔS=+0.005
    s = _div(r)
    assert s["level"] == "blocked" and s["blocked"] is True
    assert "self=0.6200" in s["block_reason"] and "0.0050" in s["block_reason"]
    assert r.get("blocked") is True
    assert r.get("reason", "").startswith("diversity_gate blocked")


def test_high_self_with_strong_delta_passes(monkeypatch):
    """self ≥ 0.55 但 ΔS ≥ +0.02 ⇒ dense_justified，放行（用边际贡献补偿相关预算）。"""
    r = _run(monkeypatch, 0.62, confirm_submit=True, before=2.0, after=2.10)  # ΔS=+0.10
    s = _div(r)
    assert s["level"] == "dense_justified", s
    assert s.get("blocked") is None
    assert r.get("blocked") is not True


def test_delta_boundary_exactly_at_threshold_passes(monkeypatch):
    """ΔS 恰为 +0.02（阈值）⇒ 放行，不是「小于等于才拦」以外的边界错判。"""
    r = _run(monkeypatch, 0.60, confirm_submit=True, before=2.00, after=2.02)
    s = _div(r)
    assert s["level"] == "dense_justified", s


# ---------------- 阻断时机与豁免 ----------------

def test_block_happens_before_side_effects(monkeypatch):
    r = _run(monkeypatch, 0.70, confirm_submit=True, before=2.0, after=2.0)
    assert r.get("blocked") is True
    names = [x.get("step") for x in (r.get("steps") or [])]
    assert "set_properties" not in names, "阻断必须早于 set_properties"
    assert "submit" not in names, "阻断必须早于 POST"
    assert r.get("submitted") is not True


def test_force_exempts_soft_gate(monkeypatch):
    """force=True ⇒ 豁免（自设纪律，与 prod 闸的「无豁免」语义不同）。"""
    r = _run(monkeypatch, 0.70, confirm_submit=True, force=True, before=2.0, after=2.0)
    assert r.get("blocked") is not True
    assert r.get("diversity_warning"), "豁免也必须留痕"
    assert r.get("diversity_warning")["level"] == "blocked"


def test_preflight_only_warns_never_blocks(monkeypatch):
    """预检（confirm_submit=False）只产出判定 + 预告，绝不置 blocked。"""
    r = _run(monkeypatch, 0.70, confirm_submit=False, before=2.0, after=2.0)
    assert r.get("blocked") is not True
    assert r.get("success") is True
    assert r.get("diversity_warning"), "预检必须预告真提交会被拦"


# ---------------- fail-open 边界 ----------------

def test_missing_self_is_unknown_fail_open(monkeypatch):
    """平台不回填 selfCorrelation 且本地库也无缓存 ⇒ unknown + fail-open（不可判 ≠ 不合格）。"""
    r = _run(monkeypatch, None, confirm_submit=True, before=2.0, after=2.0)
    s = _div(r)
    assert s["level"] == "unknown" and s["available"] is False
    assert s.get("blocked") is None
    assert r.get("blocked") is not True


def test_missing_self_falls_back_to_local_cache(monkeypatch):
    """未提交 alpha 的 is.selfCorrelation 常为空 ⇒ 回落本地库缓存并用它判定。

    2026-11-08 端到端验证的补丁：实测 IND `786wl6b8` 预检时该字段为 null，
    若不回落，本步对绝大多数候选等于不存在（永远 fail-open）。
    **刻意不现算** —— self 检查要列全池 + 下载 PnL，实测拖长 12s+ 会把 MCP 进程拖崩。
    """
    r = _run(monkeypatch, None, confirm_submit=True, before=2.0, after=2.0,
             local_cache=0.62)
    s = _div(r)
    assert s["self_source"] == "local_cache"
    assert s["self_corr"] == 0.62
    assert s["level"] == "blocked", s
    assert r.get("blocked") is True


def test_present_self_skips_local_lookup(monkeypatch):
    """平台已有读数 ⇒ 不查本地库（平台值优先）。"""
    called = []
    monkeypatch.setattr(SA, "_local_self_corr", lambda aid: called.append(aid) or 0.99)
    r = _run(monkeypatch, 0.30)
    s = _div(r)
    assert s["self_source"] == "platform"
    assert s["self_corr"] == 0.30
    assert called == [], "平台已有读数时不该再查本地库"


def test_local_cache_is_lower_bound_only(monkeypatch):
    """缓存值偏保守（池只增 ⇒ 真实值只会更高）⇒ 用它判定不会误伤，最坏漏拦。"""
    r = _run(monkeypatch, None, confirm_submit=True, before=2.0, after=2.5,
             local_cache=0.58)
    s = _div(r)
    assert s["level"] == "dense_justified", s   # 0.58 ≥ 0.55，但 ΔS=+0.5 足以豁免


def test_missing_delta_with_high_self_still_fail_open(monkeypatch):
    """高 self 但 ΔS 不可得 ⇒ 仍 fail-open（与 Step 1.7 的可用性口径一致）。"""
    r = _run(monkeypatch, 0.68, confirm_submit=True, before=None)
    s = _div(r)
    assert s["level"] == "unknown"
    assert s["self_corr"] == 0.68 and s["delta_sharpe"] is None
    assert r.get("blocked") is not True


def test_soft_line_constants_are_below_platform_line(monkeypatch):
    """软线必须严于平台线 0.7，否则这道闸没有增量意义。"""
    assert SA._DENSITY_SELF_SOFT < 0.7
    assert SA._DENSITY_DELTA_MIN > 0
    r = _run(monkeypatch, 0.65, confirm_submit=False)
    assert _div(r)["platform_line"] == 0.7
