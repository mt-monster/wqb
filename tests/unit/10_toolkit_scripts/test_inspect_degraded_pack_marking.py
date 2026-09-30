# -*- coding: utf-8 -*-
"""守护测试：降级体检包必须可见（不得伪装成完整通过）。

背景（2026-09-27 纠错）：
`--inspect-mode enforce` 是 **fail-closed——缺体检包即整波拦截**（见
`tools/wave_gate.py:473-475/977/1316`）。因此「给 5 区直接开 enforce 补空转」
是错误建议：这 5 区若没有包，每一波都会被拦死（本人上一轮建议已据此纠正）。

实测口径：
  - WebDataScope 数据包只覆盖 7 区（USA 112 / EUR 19 / CHN 13 / ASI 7 / GLB 6 /
    JPN 2 / KOR 1），**不含** DEU / IND / GBR / MEA / TWN / HKG；
  - 无源区只能走**降级包**（`tools/gen_inspect_from_db.py`，只有 coverage 维度）；
  - 降级包会带 `_degraded: true`，但闸原先一律报 `enforced` → 「只查了 1/5 条规则」
    被读成「全部通过」。

本测试锁定：
1. `load_pack_ex` 能区分完整包与降级包（且 `load_pack` 旧签名返回值不变）；
2. 降级包的报告带 `degraded=True` 与 `rules_inert`（4 条未生效规则）；
3. `format_report` 输出里出现「降级包」标记 —— 人读面也看得见；
4. 缺包区仍是 `unavailable`（enforce 的拦截判据未被削弱）。
"""

import json
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, "tools"))

import field_inspect_gate as fig  # noqa: E402

MINING = os.path.join(REPO, "tracking", "mining")


def _find_pack(degraded: bool):
    """在 tracking/mining 找一个降级包 / 完整包（不存在则跳过）。"""
    if not os.path.isdir(MINING):
        return None
    for fn in sorted(os.listdir(MINING)):
        if not fn.startswith("field_inspect_") or not fn.endswith(".json"):
            continue
        path = os.path.join(MINING, fn)
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        flat = {}
        for _ds, ffs in (data.get("fields") or {}).items():
            if isinstance(ffs, dict):
                flat.update(ffs)
        if not flat:
            continue
        is_deg = any(isinstance(v, dict) and v.get("_degraded") for v in flat.values()) \
            or "degraded" in str(data.get("source") or "").lower()
        if is_deg == degraded:
            # field_inspect_<region>_<dataset>.json
            body = fn[len("field_inspect_"):-len(".json")]
            region, _, dataset = body.partition("_")
            return region.upper(), dataset
    return None


# ---- 1. load_pack_ex 区分两类包 ------------------------------------------

def test_degraded_pack_is_detected():
    """降级包必须被识别（degraded=True），否则会伪装成完整通过。"""
    hit = _find_pack(degraded=True)
    if not hit:
        pytest.skip("本机 tracking/mining 无降级体检包")
    region, dataset = hit
    flat, degraded = fig.load_pack_ex(region, dataset)
    assert flat, f"{region}/{dataset} 应为非空包"
    assert degraded is True, f"{region}/{dataset} 应被识别为降级包"


def test_full_pack_is_not_flagged_degraded():
    """完整包（WebDataScope 来源）不得被误标为降级。"""
    hit = _find_pack(degraded=False)
    if not hit:
        pytest.skip("本机 tracking/mining 无完整体检包")
    region, dataset = hit
    flat, degraded = fig.load_pack_ex(region, dataset)
    assert flat
    assert degraded is False


def test_load_pack_signature_unchanged():
    """`load_pack` 旧签名（返回 dict|None）必须保持 —— 已有调用方依赖它。"""
    hit = _find_pack(degraded=True) or _find_pack(degraded=False)
    if not hit:
        pytest.skip("无体检包可比对")
    region, dataset = hit
    legacy = fig.load_pack(region, dataset)
    flat, _ = fig.load_pack_ex(region, dataset)
    assert legacy == flat


# ---- 2. 降级包的报告必须显式标记 ----------------------------------------

def test_degraded_report_marks_rules_inert():
    """降级包报告须带 degraded=True 与 4 条未生效规则。"""
    hit = _find_pack(degraded=True)
    if not hit:
        pytest.skip("本机无降级体检包")
    region, dataset = hit
    rep = fig.check_expressions(["rank(ts_mean(some_field, 22))"],
                                region=region, dataset=dataset)
    assert rep.get("status") != "unavailable", rep
    assert rep.get("degraded") is True, rep
    inert = rep.get("rules_inert") or []
    assert len(inert) == 4, inert
    # 四条未生效规则须点名维度，便于追查
    joined = " ".join(inert)
    for kw in ("skewness", "kurtosis", "distribution_shape", "frequency"):
        assert kw in joined, f"{kw} 未在 rules_inert 中说明"


def test_degraded_hint_is_actionable():
    """降级包报告须给出补齐完整包的命令（可自愈）。"""
    hit = _find_pack(degraded=True)
    if not hit:
        pytest.skip("本机无降级体检包")
    region, dataset = hit
    rep = fig.check_expressions(["rank(ts_mean(some_field, 22))"],
                                region=region, dataset=dataset)
    assert "gen_field_inspect_packs" in (rep.get("hint") or ""), rep.get("hint")


def test_format_report_shows_degraded_marker():
    """人读输出必须出现「降级包」字样 —— 不能只在 JSON 里。"""
    hit = _find_pack(degraded=True)
    if not hit:
        pytest.skip("本机无降级体检包")
    region, dataset = hit
    rep = fig.check_expressions(["rank(ts_mean(some_field, 22))"],
                                region=region, dataset=dataset)
    text = fig.format_report(rep)
    assert "降级包" in text, text


# ---- 3. 完整包不得带降级标记（防误报） ----------------------------------

def test_full_pack_report_has_no_degraded_marker():
    hit = _find_pack(degraded=False)
    if not hit:
        pytest.skip("本机无完整体检包")
    region, dataset = hit
    rep = fig.check_expressions(["rank(ts_mean(some_field, 22))"],
                                region=region, dataset=dataset)
    assert rep.get("status") != "unavailable"
    assert not rep.get("degraded"), rep
    assert "降级包" not in fig.format_report(rep)


# ---- 4. 缺包区仍 unavailable（enforce 判据未被削弱） --------------------

def test_missing_pack_still_unavailable():
    """缺包仍是 unavailable —— 这是 enforce 拦截的依据，不得被改成放行。"""
    rep = fig.check_expressions(["rank(close)"], region="TWN",
                                dataset="__no_such_pack__")
    assert rep.get("status") == "unavailable", rep
    assert rep.get("enforced") is False
