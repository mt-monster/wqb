"""submit_batch 设置档守护测试（2026-10-27 修复回归）.

背景：`tools_ops.submit_batch` 曾把 `maxTrade` 硬编码为 `ON`、`nanHandling` 硬编码为
`OFF`，导致对 AMR/CHN/DEU/GLB/IND/JPN/KOR/USA 这 8 个权威值为 OFF 的区域系统性错误，
且 MCP schema 无法覆盖。修复后改为读 `tracking/<REGION>/config/settings.json`。

守护点：
1. GLB → maxTrade OFF / nanHandling OFF（来自区域档案）
2. ASI → maxTrade ON / nanHandling ON（来自区域档案）
3. 显式参数优先于区域档案
4. 无档案区域 → 回落平台安全缺省（maxTrade OFF）
5. universe / decay / neutralization 不被区域档案覆盖（必须由调用参数决定）
"""
import asyncio

import pytest

import tools_ops


def _dry(**kwargs):
    kwargs.setdefault("expressions", ["rank(close)"])
    kwargs.setdefault("dry_run", True)
    return asyncio.run(tools_ops.submit_batch(**kwargs))


def test_glb_uses_region_profile_off():
    r = _dry(region="GLB", universe="MINVOL1M", decay=12, neutralization="STATISTICAL")
    assert r["success"] is True
    assert r["settings_source"] == "region_profile"
    s = r["settings_used"]
    assert s["maxTrade"] == "OFF", "GLB 权威值 maxTrade=OFF，硬编码 ON 是历史 bug"
    assert s["nanHandling"] == "OFF"


def test_asi_uses_region_profile_on():
    r = _dry(region="ASI")
    s = r["settings_used"]
    assert s["maxTrade"] == "ON"
    assert s["nanHandling"] == "ON", "ASI 权威值 nanHandling=ON"


def test_explicit_overrides_region_profile():
    r = _dry(region="GLB", max_trade="ON", nan_handling="ON")
    s = r["settings_used"]
    assert s["maxTrade"] == "ON"
    assert s["nanHandling"] == "ON"
    assert r["settings_source"] == "explicit"
    assert set(r["explicit_overrides"]) == {"maxTrade", "nanHandling"}


def test_unknown_region_falls_back_safe():
    r = _dry(region="ZZZ")
    s = r["settings_used"]
    assert r["settings_source"] == "default"
    assert s["maxTrade"] == "OFF"
    assert s["nanHandling"] == "OFF"


def test_call_params_not_overridden_by_profile():
    """区域档案里的 universe/decay 不得覆盖调用参数。"""
    r = _dry(region="GLB", universe="TOPDIV3000", decay=2, neutralization="MARKET")
    s = r["settings_used"]
    assert s["universe"] == "TOPDIV3000"
    assert s["decay"] == 2
    assert s["neutralization"] == "MARKET"


def test_settings_profile_disabled():
    r = _dry(region="GLB", settings_profile=False)
    s = r["settings_used"]
    assert r["settings_source"] == "default"
    assert s["maxTrade"] == "OFF"
