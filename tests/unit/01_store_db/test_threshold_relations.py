# -*- coding: utf-8 -*-
"""阈值口径的**关系**守护（skills 审查 X-11，2026-09-29）：同一个词（Sharpe/Fitness/Turnover…）在仓库里
曾有 3–5 个取值（1.25 / 1.3 / 1.58；0.75 / 1.0；4–40% / 5–20% / 1–70%）。它们各有用途，但用途必须写清、
关系必须钉住——本测试把「谁比谁宽、谁等于谁」写成断言，任何一方漂移就红。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for _p in (str(ROOT / "src"), str(ROOT / "world-quant-brain-mcp")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.config import GATES_INTERNAL, GATES_PLATFORM, PLATFORM_CHECK_LINES as PL  # noqa: E402
from wqb.store.submit_queue import LIM  # noqa: E402


def test_platform_lines_are_registered_per_check_name():
    assert PL["low_sharpe_min"] == {"delay1": 1.25, "delay0": 2.0}
    assert PL["low_fitness_min"] == {"delay1": 1.0, "delay0": 1.3}
    assert PL["turnover_range"] == (0.01, 0.70)
    assert PL["low_2y_sharpe_min"] == 1.58


def test_gates_platform_sharpe_is_the_2y_line_not_the_low_sharpe_line():
    """GATES_PLATFORM.sharpe_min（1.58）= 平台 2Y 线，**不是** LOW_SHARPE 线（Delay-1 为 1.25）。"""
    assert GATES_PLATFORM["sharpe_min"] == PL["low_2y_sharpe_min"] > PL["low_sharpe_min"]["delay1"]
    assert GATES_PLATFORM["fitness_min"] == PL["low_fitness_min"]["delay1"]
    assert GATES_PLATFORM["turnover_range"] == PL["turnover_range"]


def test_internal_lines_are_at_least_as_strict_as_platform_lines():
    assert GATES_INTERNAL["sharpe_min"] >= GATES_PLATFORM["sharpe_min"]
    assert GATES_INTERNAL["fitness_min"] >= GATES_PLATFORM["fitness_min"]
    lo_i, hi_i = GATES_INTERNAL["turnover_range"]
    lo_p, hi_p = GATES_PLATFORM["turnover_range"]
    assert lo_p <= lo_i and hi_i <= hi_p                     # 内部换手窗 ⊂ 平台换手窗
    assert GATES_INTERNAL["self_corr_max"] <= GATES_PLATFORM["self_corr_max"]


def test_submit_queue_lines_come_from_config():
    assert LIM["sharpe"] == GATES_PLATFORM["sharpe_min"]
    assert LIM["fitness"] == GATES_PLATFORM["fitness_min"]
    assert LIM["two_year"] == PL["low_2y_sharpe_min"]
    assert LIM["turnover_hi"] == GATES_PLATFORM["turnover_range"][1]


def test_pre_submit_check_is_removed_and_never_reintroduced():
    """`pre_submit_check` 已于 2026-10-02 **物理删除**（定义 + 单测 + GBR 配套脚本簇）。

    该方法是放宽的本地启发式（Sharpe 1.3 / Fitness 0.75 / Turnover 4%–40% / Returns 4%，
    预检异常即放行 = fail-open），2026-09-29 起提交路由已改用 fail-closed 的
    `submit_alpha._submit_gate`，生产调用方为 0。

    本测试守护「不得复活」：
      1. `brain_mixin_simulation.py` 里**不得**再有 `def pre_submit_check` 定义；
      2. `src/` 全树不得出现 `pre_submit_check(` 的方法调用形态
         （允许「已移除」说明性注释，注释里不写调用括号）；
      3. 配套 GBR 脚本簇（`tools/gbr_pre_submit_check.py` 等）不得回流。

    路由的**活机制**由 `test_submit_gate_thresholds_are_pinned` 守护（`_submit_gate` /
    配额 / prod 三闸常量）——这才是提交的唯一本地闸。
    """
    src = (ROOT / "world-quant-brain-mcp" / "brain_mixin_simulation.py").read_text(encoding="utf-8")
    assert "def pre_submit_check" not in src, "pre_submit_check 已删除，不得复活定义"
    assert "pre_submit_check() 已移除" in src, "应保留「已移除」说明注释，指向 _submit_gate"

    call_re = re.compile(r"(?:\.|\b)pre_submit_check\s*\(")
    hits = []
    for p in (ROOT / "src").rglob("*.py"):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in call_re.finditer(text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            line = text[line_start:text.find("\n", m.start())]
            hits.append(f"{p.relative_to(ROOT)}: {line.strip()[:80]}")
    assert hits == [], f"pre_submit_check 已删除，不应再被调用：{hits}"

    for gone in ("tools/gbr_pre_submit_check.py", "tools/validate_gbr_fields.py",
                 "tools/test_gbr_batch_isolation.py"):
        assert not (ROOT / gone).exists(), f"GBR 配套脚本 {gone} 已随 pre_submit_check 一并删除"


def test_submit_gate_thresholds_are_pinned():
    """提交路由本地闸（submit_alpha._submit_gate / 配额闸 / prod 闸）的关键常量钉死。

    这些是「不过闸就提交不出去」的代码承载点；漂移即红：
      - 硬闸 WARNING 集合 = {LOW_FITNESS, LOW_SHARPE, LOW_2Y_SHARPE}（模拟层 WARNING、提交层升级 FAIL）；
      - REGULAR 配额上限 = 4 / ET 日（与 tools/quota_status.py REGULAR_LIMIT 一致）；
      - prod 闸阈值 = 0.7（用户铁律，与 super_build --prod-gate 默认一致）。
    """
    src = (ROOT / "src" / "wqb" / "workflow" / "nodes" / "submit_alpha.py").read_text(encoding="utf-8")
    assert '_SUBMIT_HARD_GATE_WARNINGS = {"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE"}' in src
    assert "_REGULAR_QUOTA_LIMIT = REGULAR_DAILY_LIMIT" in src
    assert "_PROD_THRESHOLD = 0.7" in src
    # 与唯一实现源对比
    from wqb.submit_verdict_core import SUBMIT_HARD_GATE_WARNINGS as CORE_HARD
    assert CORE_HARD == frozenset({"LOW_FITNESS", "LOW_SHARPE", "LOW_2Y_SHARPE"})
    # REGULAR / SUPER 配额上限的唯一实现 = wqb.quota（2026-10-05 起类型化：两条独立配额线）。
    # 值仍钉死；两个消费点必须从该实现取数，不得各自硬编码（漂移即红）。
    from wqb.quota import REGULAR_DAILY_LIMIT, SUPER_DAILY_LIMIT
    assert (REGULAR_DAILY_LIMIT, SUPER_DAILY_LIMIT) == (4, 1)
    quota_src = (ROOT / "tools" / "quota_status.py").read_text(encoding="utf-8")
    assert "wqb.quota" in quota_src


def test_is_ppa_alpha_is_shared_between_gate_and_core():
    """_submit_gate 的 PPA 判定必须与 submit_verdict_core.is_ppa_alpha 同口径（F10b 修复）。

    {type: REGULAR, tags: [PowerPoolSelected]} 两端都必须判 True（否则计数组错位）。
    """
    sys.path.insert(0, str(ROOT / "src"))
    from wqb.submit_verdict_core import is_ppa_alpha as core_is_ppa
    from wqb.workflow.nodes.submit_alpha import _is_ppa_alpha as gate_is_ppa
    tagged = {"type": "REGULAR", "tags": ["PowerPoolSelected", "SRC_x"]}
    assert core_is_ppa(tagged) is True
    assert gate_is_ppa(tagged) is True
    plain = {"type": "REGULAR", "tags": ["CH_REG"]}
    assert core_is_ppa(plain) is False and gate_is_ppa(plain) is False
    assert gate_is_ppa({"type": "PPA"}) is True
