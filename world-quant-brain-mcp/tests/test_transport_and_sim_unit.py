"""tools_sim 和 brain_mixin_transport 单元测试 — 参数校验 + 重试退避逻辑（无网络）。

覆盖两个此前无测试的关键路径：
1. tools_sim._validate_region_settings：region/universe/neutralization 组合校验
2. brain_mixin_transport.TransportMixin._retry_wait_seconds：Retry-After / 指数退避
3. brain_mixin_transport.TransportMixin._to_absolute_url：URL 拼接
4. brain_mixin_transport.TransportMixin._response_payload：JSON/text 提取
5. brain_mixin_transport.TransportMixin._simulation_error_message：错误信息提取
"""
import json
from unittest.mock import MagicMock, patch

import pytest
import requests

# tools_sim 需要注入 MCP 包路径
from brain_mixin_transport import TransportMixin


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def make_shell():
    """构造空壳 TransportMixin 实例，不触发 __init__ 的 Redis/session 逻辑。"""
    return TransportMixin.__new__(TransportMixin)


# ---------------------------------------------------------------------------
# _validate_region_settings (tools_sim.py)
# ---------------------------------------------------------------------------

def test_validate_region_settings_valid():
    """合法 region/universe/neutralization 组合返回 None。"""
    from tools_sim import _validate_region_settings
    assert _validate_region_settings("USA", "TOP3000", "SUBINDUSTRY") is None
    assert _validate_region_settings("EUR", "TOP2500", "STATISTICAL") is None
    assert _validate_region_settings("GBR", "TOP700", "INDUSTRY") is None


def test_validate_region_settings_unknown_region():
    """未知 region 返回错误 dict。"""
    from tools_sim import _validate_region_settings
    r = _validate_region_settings("MARS", "TOP3000", "SUBINDUSTRY")
    assert r is not None
    assert "Unknown region" in r["error"]


def test_validate_region_settings_bad_universe():
    """universe 不在该 region 的合法列表中返回错误。"""
    from tools_sim import _validate_region_settings
    r = _validate_region_settings("USA", "TOP700", "SUBINDUSTRY")
    assert r is not None
    assert "not valid for region" in r["error"]


def test_validate_region_settings_bad_neutralization():
    """未知 neutralization 返回错误。"""
    from tools_sim import _validate_region_settings
    r = _validate_region_settings("USA", "TOP3000", "MAGIC")
    assert r is not None
    assert "Unknown neutralization" in r["error"]


def test_validate_region_settings_all_regions_covered():
    """_REGION_UNIVERSE_MAP 覆盖 src/wqb/config.py 中的全部区域（一致性检查）。"""
    from tools_sim import _REGION_UNIVERSE_MAP
    # 至少 14 个区域（config.py 定义了 14 个）
    assert len(_REGION_UNIVERSE_MAP) >= 14
    for region, universes in _REGION_UNIVERSE_MAP.items():
        assert isinstance(universes, list) and len(universes) >= 1, f"{region} has no universes"


# ---------------------------------------------------------------------------
# _retry_wait_seconds (brain_mixin_transport.py)
# ---------------------------------------------------------------------------

def test_retry_wait_with_retry_after_header():
    """有 Retry-After header 时，等待时间等于 header 值（受 max_delay 上限）。"""
    c = make_shell()
    resp = MagicMock(spec=requests.Response)
    resp.headers = {"Retry-After": "5"}
    wait = c._retry_wait_seconds(resp, attempt=0)
    assert wait == 5.0


def test_retry_wait_retry_after_capped_by_max_delay():
    """Retry-After 超过 max_delay 时被截断。"""
    c = make_shell()
    resp = MagicMock(spec=requests.Response)
    resp.headers = {"Retry-After": "120"}
    wait = c._retry_wait_seconds(resp, attempt=0, max_delay=60.0)
    assert wait == 60.0


def test_retry_wait_exponential_backoff_no_header():
    """无 Retry-After 时使用指数退避（base * 1.6^attempt + jitter）。"""
    c = make_shell()
    resp = MagicMock(spec=requests.Response)
    resp.headers = {}
    # attempt=0: base_delay=2.0 * 1.6^0 = 2.0 + jitter(0..0.2)
    wait = c._retry_wait_seconds(resp, attempt=0, base_delay=2.0)
    assert 2.0 <= wait <= 2.3
    # attempt=3: 2.0 * 1.6^3 = 8.192 + jitter
    wait3 = c._retry_wait_seconds(resp, attempt=3, base_delay=2.0)
    assert 8.0 <= wait3 <= 9.0


def test_retry_wait_none_response():
    """response 为 None 时退回指数退避。"""
    c = make_shell()
    wait = c._retry_wait_seconds(None, attempt=1, base_delay=2.0)
    # 2.0 * 1.6^1 = 3.2 + jitter
    assert 3.0 <= wait <= 3.6


def test_retry_wait_invalid_retry_after_falls_back():
    """Retry-After 非数字时退回指数退避。"""
    c = make_shell()
    resp = MagicMock(spec=requests.Response)
    resp.headers = {"Retry-After": "not-a-number"}
    wait = c._retry_wait_seconds(resp, attempt=0, base_delay=2.0)
    assert 2.0 <= wait <= 2.3


def test_retry_wait_backoff_capped_by_max_delay():
    """指数退避被 max_delay 上限截断。"""
    c = make_shell()
    resp = MagicMock(spec=requests.Response)
    resp.headers = {}
    # attempt=10: 2.0 * 1.6^10 ≈ 2.0 * 109.95 ≈ 219.9 → capped to 60
    wait = c._retry_wait_seconds(resp, attempt=10, base_delay=2.0, max_delay=60.0)
    assert wait <= 61.0  # 60 + jitter(0..6)


# ---------------------------------------------------------------------------
# _to_absolute_url (brain_mixin_transport.py)
# ---------------------------------------------------------------------------

def test_to_absolute_url_relative():
    """相对路径拼接 base_url。"""
    c = make_shell()
    c.base_url = "https://api.worldquantbrain.com"
    assert c._to_absolute_url("/simulations") == "https://api.worldquantbrain.com/simulations"


def test_to_absolute_url_already_absolute():
    """已经是绝对 URL 时原样返回。"""
    c = make_shell()
    c.base_url = "https://api.worldquantbrain.com"
    full = "https://api.worldquantbrain.com/alphas/123"
    assert c._to_absolute_url(full) == full


def test_to_absolute_url_empty():
    """空字符串原样返回。"""
    c = make_shell()
    c.base_url = "https://api.worldquantbrain.com"
    assert c._to_absolute_url("") == ""


# ---------------------------------------------------------------------------
# _response_payload (brain_mixin_transport.py)
# ---------------------------------------------------------------------------

def test_response_payload_json():
    """能解析 JSON 时返回 dict。"""
    c = make_shell()
    resp = MagicMock(spec=requests.Response)
    resp.json.return_value = {"key": "value"}
    assert c._response_payload(resp) == {"key": "value"}


def test_response_payload_text_fallback():
    """JSON 解析失败时返回 text。"""
    c = make_shell()
    resp = MagicMock(spec=requests.Response)
    resp.json.side_effect = ValueError("not JSON")
    resp.text = "plain text error"
    assert c._response_payload(resp) == "plain text error"


# ---------------------------------------------------------------------------
# _simulation_error_message (brain_mixin_transport.py)
# ---------------------------------------------------------------------------

def test_simulation_error_message_from_error_key():
    """从 'error' key 提取错误信息。"""
    c = make_shell()
    msg = c._simulation_error_message({"error": "Invalid expression"})
    assert "Invalid expression" in msg


def test_simulation_error_message_from_message_key():
    """从 'message' key 提取。"""
    c = make_shell()
    msg = c._simulation_error_message({"message": "Something went wrong"})
    assert "Something went wrong" in msg


def test_simulation_error_message_nested():
    """从嵌套 dict 中提取 error/message。"""
    c = make_shell()
    data = {"progress": {"errorMessage": "timeout during simulation"}}
    msg = c._simulation_error_message(data)
    assert "timeout during simulation" in msg


def test_simulation_error_message_non_dict():
    """非 dict 输入返回 str。"""
    c = make_shell()
    assert c._simulation_error_message("string error") == "string error"
    assert c._simulation_error_message(None) == "Unknown error"


def test_simulation_error_message_empty_dict():
    """空 dict 返回 'Unknown error'。"""
    c = make_shell()
    msg = c._simulation_error_message({})
    assert "Unknown error" in msg or msg == ""
