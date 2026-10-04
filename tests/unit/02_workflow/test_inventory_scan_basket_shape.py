# -*- coding: utf-8 -*-
"""inventory_scan 节点读 basket.json 的形态护栏（2026-10-03 修复）。

原缺陷：``tools/select_ra_basket.py`` 写出的 ``cache/basket.json`` 是**候选列表**，而节点按
``{"candidates": [...]}`` 取值（``basket.get("candidates")``）——对 list 抛 AttributeError，
被外层 ``except Exception`` 吞成 ``Inventory scan failed``，整个盘点跑完后节点仍报失败。
节点除 dry-run 外此前没有任何测试，所以一直没被发现。

用 monkeypatch 把 REPO_ROOT 指到 tmp、把 subprocess.run 换成假的，不碰真实 cache/、不发任何请求。
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
for _p in (REPO, REPO / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.workflow.nodes import inventory_scan as inv  # noqa: E402


@pytest.fixture
def run_node(monkeypatch, tmp_path):
    """返回 f(basket_payload) -> 节点 result；basket_payload 会被写成假 select_ra_basket 的产物。"""
    (tmp_path / "cache").mkdir()
    monkeypatch.setattr(inv, "REPO_ROOT", str(tmp_path))

    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="ok", stderr="")

    monkeypatch.setattr(inv.subprocess, "run", fake_run)
    # 数据集对矩阵分析会读真实库：与本测试无关，换成空。该模块随并行会话的改动出现，不存在时节点也不会调用它
    try:
        import wqb.dataset_pair_matrix as dpm
    except ImportError:
        dpm = None
    if dpm is not None:
        monkeypatch.setattr(dpm, "get_dataset_pair_recommendations", lambda *a, **k: [])

    def _run(payload):
        (tmp_path / "cache" / "basket.json").write_text(json.dumps(payload), encoding="utf-8")
        return inv.run(region="TST", target=3)

    return _run


def test_list_shaped_basket_is_the_real_output_format(run_node):
    """select_ra_basket 的真实产物形态：候选列表。"""
    basket = [
        {"id": "A1", "region": "TST", "prod_status": "fresh_ok"},
        {"id": "A2", "region": "TST", "prod_status": "stale_ok"},
        {"id": "A3", "region": "TST", "prod_status": "unmeasured"},
    ]
    r = run_node(basket)
    assert r["success"] is True, r.get("error")
    assert r["candidate_count"] == 3
    assert r["prod_checked_count"] == 1          # 只有 fresh_ok 算「prod 已核」
    assert r["basket"] == basket


def test_legacy_dict_shaped_basket_still_works(run_node):
    r = run_node({"candidates": [{"id": "A1", "prod_status": "fresh_ok"}, {"id": "A2"}]})
    assert r["success"] is True, r.get("error")
    assert r["candidate_count"] == 2 and r["prod_checked_count"] == 1


def test_empty_basket_is_success_with_zero_counts(run_node):
    r = run_node([])
    assert r["success"] is True, r.get("error")
    assert r["candidate_count"] == 0 and r["prod_checked_count"] == 0
