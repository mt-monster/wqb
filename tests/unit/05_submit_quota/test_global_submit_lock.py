# -*- coding: utf-8 -*-
"""全局禁提交闸（2026-10-05 用户指令）：「只挖不提交」——挖到的 alpha 一律积攒，提交由用户决定。

本文件守护三条不变量（防回归）：
  1. `wqb.config.ALLOW_ALPHA_SUBMIT` 默认 False（唯一事实源，env 才可覆盖）；
  2. `submit_alpha.run(confirm_submit=True)` 在锁定时 fail-closed 拒绝、且**零网络副作用**
     （覆盖 MCP `workflow_submit_alpha` 与 `workflow_execute(node="submit_alpha")` 两条路径）；
  3. `tools/super_build.py` 的 POST 站点同样受锁保护（SUPER 路径）。
"""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT / "src", REPO_ROOT / "tools"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb import config as C  # noqa: E402
from wqb.workflow.nodes import submit_alpha as SA  # noqa: E402


def test_config_default_is_locked():
    """默认锁定；仅当用户显式设 WQB_ALLOW_ALPHA_SUBMIT 时才可能为 True。"""
    if not os.getenv("WQB_ALLOW_ALPHA_SUBMIT"):
        assert C.ALLOW_ALPHA_SUBMIT is False
    else:  # pragma: no cover - 仅显式放行时走到
        assert C.ALLOW_ALPHA_SUBMIT is True


def test_confirm_submit_blocked_and_no_side_effect(monkeypatch):
    """锁定态下 confirm_submit=True 必须被拒，且不进入任何网络/属性步骤。"""
    monkeypatch.setattr(SA, "ALLOW_ALPHA_SUBMIT", False, raising=True)
    res = SA.run(alpha_id="LOCKEDTEST", confirm_submit=True)
    assert res["submitted"] is False
    assert res["success"] is False
    assert res.get("blocked") is True
    assert "global_submit_lock" in str(res.get("reason"))
    # 零副作用：唯一 step 就是锁闸本身，未出现 precheck / prod_gate / quota_gate
    steps = [s.get("step") for s in (res.get("steps") or [])]
    assert steps == ["global_submit_lock"], steps


def test_force_does_not_bypass_lock(monkeypatch):
    """force=True 不豁免全局禁提交闸。"""
    monkeypatch.setattr(SA, "ALLOW_ALPHA_SUBMIT", False, raising=True)
    res = SA.run(alpha_id="LOCKEDTEST", confirm_submit=True, force=True)
    assert res.get("blocked") is True
    assert "global_submit_lock" in str(res.get("reason"))


def test_super_build_submit_site_guarded():
    """SUPER 路径的 POST 站点（tools/super_build.py::cmd_submit）也引用同一开关。"""
    src = (REPO_ROOT / "tools" / "super_build.py").read_text(encoding="utf-8")
    assert "ALLOW_ALPHA_SUBMIT" in src
