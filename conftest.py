# -*- coding: utf-8 -*-
"""仓库根 conftest：环境耦合测试的显式标记（skills 审查 X-17 #13 / IX-21，2026-09-29）。

问题：一批测试依赖**被 .gitignore 排除的本机产物**（`data/operators_verified.json` 由 get_operators 实测生成；
`data/wqb.db` 的真实台账；`attic/` 下的归档说明），干净克隆里必然失败——CI 上永远红着，真实回归被淹没
（本仓库在云端容器基线里有 21 个这类失败，其中不乏与代码无关的）。

约定：这类测试打 `@pytest.mark.needs_<资源>`，资源缺失时**跳过并写明原因**，而不是失败；
测试逻辑本身（一致性判据）不变，作者本机（资源齐全）仍然全跑。
作用域是整个仓库（testpaths = tests + world-quant-brain-mcp/tests），故放根目录。
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent

#: marker → (资源路径, 为什么缺)
_FILE_MARKERS = {
    "needs_operators_verified": (ROOT / "data" / "operators_verified.json",
                                 "由平台 get_operators 实测生成，被 .gitignore 排除"),
    "needs_attic_step_metrics": (ROOT / "attic" / "step_metrics_20260917" / "README.md",
                                 "attic/ 被 .gitignore 排除，归档说明只在作者本机"),
}


def pytest_configure(config):
    for name, (path, why) in _FILE_MARKERS.items():
        config.addinivalue_line("markers", f"{name}: 需要 {path.relative_to(ROOT)}（{why}）；缺失则跳过")


def pytest_collection_modifyitems(config, items):
    for item in items:
        for name, (path, why) in _FILE_MARKERS.items():
            if item.get_closest_marker(name) and not path.exists():
                item.add_marker(pytest.mark.skip(
                    reason=f"{path.relative_to(ROOT)} 缺失（{why}）——干净克隆下跳过而非失败"))
