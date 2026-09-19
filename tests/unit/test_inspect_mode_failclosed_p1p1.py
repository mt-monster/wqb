# -*- coding: utf-8 -*-
"""回归测试：体检硬门「缺包」策略（ra-pipeline 步 2 开区硬前置 + 步 5 fail-closed）。

背景（2026-09-17 P1-1 审计结论）：
`tools/wave_gate.py` 的体检硬门（`field_inspect_gate.py`）此前**只在有体检包时才生效**，
缺包一律静默放行，只在 stdout 打一行 `[inspect] 体检硬门未生效`。后果是
「本数据集没有体检包」与「本实测通过体检」在最终 PASS/FAIL 上**无法区分** ——
低覆盖 / 厚尾 / 稀疏事件的预处理约束可以一路裸奔到仿真（历史三连复发的根因）。

本次修复把缺包行为显式化为三档 `off|warn|enforce`，其中：
  - `warn`    = 灰度默认：告警但放行（保持全池不停摆）；
  - `enforce` = fail-closed：缺包即整波拦截，`all_pass=False`、退出码 1。

本测试锁定：
1. `resolve_inspect_mode` 的优先级（CLI > env > 默认）与非法值回落；
2. 无体检包时 `field_inspect_gate.check_expressions` 确实返回 `unavailable`
   （enforce 档赖以触发的判据）；
3. 端到端：同一无包数据集，`warn` 放行而 `enforce` 拦截。
"""

import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))

import wave_gate  # noqa: E402


# ---- 1. 策略解析（纯函数）------------------------------------------------

def test_resolve_defaults_to_warn():
    """无 CLI、无环境变量 → 灰度默认 warn（不改变现网行为）。"""
    assert wave_gate.resolve_inspect_mode(None, env={}) == "warn"
    assert wave_gate.DEFAULT_INSPECT_MODE == "warn"


def test_resolve_cli_beats_env():
    """CLI 高于环境变量 —— 单波临时收紧/放宽不必改全局环境。"""
    assert wave_gate.resolve_inspect_mode("enforce", env={"WQB_INSPECT_MODE": "off"}) == "enforce"
    assert wave_gate.resolve_inspect_mode("off", env={"WQB_INSPECT_MODE": "enforce"}) == "off"


def test_resolve_falls_back_to_env_then_default():
    """无 CLI 时读环境变量；环境变量缺失/为空白则回落默认。"""
    assert wave_gate.resolve_inspect_mode(None, env={"WQB_INSPECT_MODE": "enforce"}) == "enforce"
    assert wave_gate.resolve_inspect_mode(None, env={"WQB_INSPECT_MODE": "  ENFORCE  "}) == "enforce"
    assert wave_gate.resolve_inspect_mode(None, env={"WQB_INSPECT_MODE": ""}) == "warn"
    assert wave_gate.resolve_inspect_mode(None, env={"WQB_INSPECT_MODE": None}) == "warn"


def test_resolve_rejects_illegal_mode():
    """拼错的 mode 不得意外关掉把关 —— 一律回落 warn，绝不静默变 off。"""
    for bad in ("0ff", "false", "no", "blocking", "ENFORCED!", "strict"):
        assert wave_gate.resolve_inspect_mode(bad, env={}) == "warn", bad


def test_inspect_mode_flag_is_declared_and_validated():
    """`--inspect-mode` 必须真在 argparse 里声明（否则子进程 exit=2 被吞成 success）。"""
    src = open(os.path.join(REPO, "tools", "wave_gate.py"), encoding="utf-8").read()
    assert '"--inspect-mode"' in src
    assert "resolve_inspect_mode" in src


# ---- 2. 触发判据：无包 → unavailable -------------------------------------

def test_missing_pack_reports_unavailable():
    """无体检包时 status 必须是 unavailable —— enforce 档的拦截判据。"""
    sys.path.insert(0, os.path.join(REPO, "tools"))
    import field_inspect_gate as fig

    rep = fig.check_expressions(
        ["rank(close)"], region="KOR", dataset="__no_such_pack_dataset__"
    )
    assert rep.get("status") == "unavailable", rep
    # 报告必须给出可自愈的信息，而不是只报"未生效"
    assert rep.get("hint") or rep.get("pack_path")


# ---- 3. 端到端：warn 放行 vs enforce 拦截 ---------------------------------

def _run_wave_gate(mode, dataset="model109", region="KOR", campaign="tracking/KOR"):
    """跑一次单表达式 wave_gate（零平台请求、零配额）。"""
    cmd = [
        sys.executable, os.path.join(REPO, "tools", "wave_gate.py"),
        "--campaign-dir", campaign,
        "--region", region,
        "--dataset", dataset,
        "--wave", "s2_pytest_inspect",
        "--expr", "rank(close)",
        "--skip-diversity-gate",
        "--skip-quality",
        "--inspect-mode", mode,
    ]
    return subprocess.run(
        cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", timeout=300
    )


@pytest.fixture(scope="module")
def kor_no_pack_ready():
    """前置：KOR/model109 有 field whitelist（gate.py 能跑通）但无体检包。"""
    has_wl = os.path.isfile(
        os.path.join(REPO, "tracking", "KOR", "reference", "kor_model109_field_whitelist.json")
    )
    has_pack = os.path.isfile(
        os.path.join(REPO, "tracking", "mining", "field_inspect_kor_model109.json")
    )
    if not has_wl or has_pack:
        pytest.skip("KOR/model109 前置不满足（需有白名单且无体检包）")
    return True


def test_enforce_blocks_when_pack_missing(kor_no_pack_ready):
    """enforce：缺体检包 → 退出码非 0，且输出点名 fail-closed。"""
    r = _run_wave_gate("enforce")
    blob = (r.stdout or "") + (r.stderr or "")
    assert r.returncode != 0, blob[-2000:]
    assert "fail-closed" in blob
    assert "缺体检包" in blob


def test_warn_passes_when_pack_missing(kor_no_pack_ready):
    """warn（灰度默认）：缺包放行 —— 但必须留下可检索的告警，不得静默。"""
    r = _run_wave_gate("warn")
    blob = (r.stdout or "") + (r.stderr or "")
    assert "体检硬门未生效" in blob, blob[-2000:]
    assert "fail-closed" not in blob
