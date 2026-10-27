# -*- coding: utf-8 -*-
"""2026-10-20：/data-fields 全量分页契约（all-or-error）。

背景：2026-10-18 的 analyst7 字段画像只记到 299/1111 —— 客户端把 dataset 级拉取
截在 300 条并缓存 7 天。实测平台契约（EUR/D1/TOP2500）：
- 每页上限 50（limit=100 直接 HTTP 400）；
- ``dataset.id=`` 可翻到任意深度，必须拉到平台声明的 count；
- ``search=`` 只能在 offset+limit<=100 的窗口内取前 100 个匹配，且 count 是**未过滤**总数。

本文件同时守护两份实现：``tools/lib/api_client.paginate_all`` 与
toolkit ``_lib/api.paginate_all``（语义必须一致）。
"""
import importlib.util
import io
import json
import re
import sys
import urllib.error
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]

# tools/lib 的模块名很通用，按路径加载成唯一名字，避免与其他测试的同名模块互踩。
_SPEC = importlib.util.spec_from_file_location(
    "wqb_tools_lib_api_client", REPO_ROOT / "tools" / "lib" / "api_client.py")
tools_api = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(tools_api)

TK = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"
if str(TK) not in sys.path:
    sys.path.insert(0, str(TK))
from _lib import api as tk_api  # noqa: E402

IMPLS = [
    pytest.param(tools_api, id="tools_lib"),
    pytest.param(tk_api, id="toolkit_lib"),
]


def _pages(fields, count=None, page=50):
    total = len(fields) if count is None else count
    out = {}
    for off in range(0, total, page):
        out[off] = {"results": fields[off:off + page], "count": total}
    return out


class FakeApi:
    """Minimal Api stand-in: ``get(path)`` returns a JSON file-like object."""

    def __init__(self, pages, fail_offsets=(), fail_code=400):
        self.pages = pages
        self.fail_offsets = set(fail_offsets)
        self.fail_code = fail_code
        self.calls = []
        self.paths = []

    def get(self, path):
        self.paths.append(path)
        offset = int(re.search(r"[?&]offset=(\d+)", path).group(1))
        self.calls.append(offset)
        if offset in self.fail_offsets:
            raise urllib.error.HTTPError(
                "https://x", self.fail_code, "err", {}, io.BytesIO(b""))
        return io.StringIO(json.dumps(self.pages[offset]))


def test_full_scoped_pull_fetches_all_pages():
    fields = [{"id": "f%d" % i} for i in range(1111)]
    for mod in (tools_api, tk_api):
        api = FakeApi(_pages(fields))
        res = mod.paginate_all(api, "/data-fields?dataset.id=analyst7", sleep=0)
        assert len(res["items"]) == 1111
        assert res["platform_count"] == 1111
        assert res["complete"] is True
        assert res["pages"] == 23
        assert res["truncated_reason"] is None
        assert api.calls == list(range(0, 1111, 50))
        # page size is always 50 and the caller's base must not carry limit.
        assert "limit=50&offset=0" in api.paths[0]


@pytest.mark.parametrize("mod", IMPLS)
def test_short_pull_raises_pagination_error(mod):
    fields = [{"id": "f%d" % i} for i in range(57)]
    api = FakeApi(_pages(fields, count=1111))
    with pytest.raises(mod.PaginationError, match="incomplete pull"):
        mod.paginate_all(api, "/data-fields?dataset.id=analyst7", sleep=0)
    assert api.calls == [0, 50]


@pytest.mark.parametrize("mod", IMPLS)
def test_search_window_caps_at_100(mod):
    fields = [{"id": "x%d" % i} for i in range(150)]
    api = FakeApi(_pages(fields, count=4757))
    res = mod.paginate_all(api, "/data-fields?dataset.id=ds&search=x", sleep=0)
    assert api.calls == [0, 50]
    assert len(res["items"]) == 100
    assert res["platform_count"] == 4757
    assert res["complete"] is False
    assert res["truncated_reason"] == "search_window_capped"


@pytest.mark.parametrize("mod", IMPLS)
def test_search_400_beyond_first_page_is_a_window_cap(mod):
    fields = [{"id": "x%d" % i} for i in range(150)]
    api = FakeApi(_pages(fields, count=4757), fail_offsets={50})
    res = mod.paginate_all(api, "/data-fields?dataset.id=ds&search=x", sleep=0)
    assert api.calls == [0, 50]
    assert len(res["items"]) == 50
    assert res["truncated_reason"] == "search_window_capped"
    assert res["complete"] is False


@pytest.mark.parametrize("mod", IMPLS)
def test_non_search_http_error_raises(mod):
    fields = [{"id": "f%d" % i} for i in range(1111)]
    api = FakeApi(_pages(fields), fail_offsets={50}, fail_code=403)
    with pytest.raises(urllib.error.HTTPError):
        mod.paginate_all(api, "/data-fields?dataset.id=analyst7", sleep=0)
    assert api.calls == [0, 50]


@pytest.mark.parametrize("mod", IMPLS)
def test_max_items_cap_is_declared_not_silent(mod):
    fields = [{"id": "f%d" % i} for i in range(1111)]
    api = FakeApi(_pages(fields))
    res = mod.paginate_all(api, "/data-fields?dataset.id=analyst7",
                           max_items=120, sleep=0)
    assert len(res["items"]) == 120
    assert res["pages"] == 3
    assert res["complete"] is False
    assert res["truncated_reason"] == "max_items_cap"
    assert api.calls == [0, 50, 100]


@pytest.mark.parametrize("mod", IMPLS)
def test_no_progress_raises(mod):
    page = [{"id": "f%d" % i} for i in range(50)]
    api = FakeApi({0: {"results": page, "count": 1111},
                   50: {"results": page, "count": 1111}})
    with pytest.raises(mod.PaginationError, match="no progress"):
        mod.paginate_all(api, "/data-fields?dataset.id=analyst7", sleep=0)
    assert api.calls == [0, 50]
