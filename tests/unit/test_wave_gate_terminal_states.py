# -*- coding: utf-8 -*-
"""回归测试：wave_gate 对 gate.py 子进程的三分终态（PASS / FAIL / ERROR）。

背景（2026-09-08 实测）：`--datasets pv30` 里的 pv30 未跑过 scan_fields 时，
gate.py 在 merge_whitelists 抛 FileNotFoundError 崩溃，wave_gate 解析不到结论 JSON，
把它记成 `all_pass=None` 再一路落到 FAIL 分支。使用者看到的是"表达式不合格"，
真实原因（缺 typed catalog）只有单独手跑 gate.py 才看得到，且与真多样性 FAIL
在输出上完全无法区分。

本测试锁定三件事：
1. gate.py 崩溃 → ERROR 终态，退出码 2，stderr 原文（含自愈命令）透传到输出；
2. gate.py 正常返回 all_pass=false → FAIL 终态，退出码 1，措辞明确是"闸门不过"；
3. `all_pass=None` 不再是可能的终态 —— 任何解析不到结论的情况都走 ERROR。
"""

import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))

import wave_gate  # noqa: E402

NL = chr(10)


# ---- 纯函数层：结论解析 / 失败原因归纳 ----

def test_parse_gate_payload_ignores_leading_noise():
    """gate.py 在 payload 前会打日志（[DIVERSITY-SKIP]、入库 WARN…），不应干扰解析。"""
    payload = {"all_pass": True, "total": 2, "passed": 2}
    out = "[DIVERSITY-SKIP] 单表达式模式" + NL + json.dumps(payload, indent=1)
    got = wave_gate.parse_gate_payload(out)
    assert got is not None and got["all_pass"] is True


def test_parse_gate_payload_returns_none_on_crash():
    """崩溃时 stdout 只有日志、没有结论 —— 必须返回 None（调用方按 ERROR 处理）。"""
    assert wave_gate.parse_gate_payload("[warn] 断链提示" + NL) is None
    assert wave_gate.parse_gate_payload("") is None
    assert wave_gate.parse_gate_payload(None) is None


def test_parse_gate_payload_rejects_json_without_all_pass():
    """结构像 JSON 但没有 bool all_pass 的输出不算结论，避免 all_pass=None 复活。"""
    assert wave_gate.parse_gate_payload(json.dumps({"total": 3})) is None
    assert wave_gate.parse_gate_payload(json.dumps({"all_pass": None})) is None


def test_gate_fail_reasons_names_the_failing_subgate():
    """FAIL 行要能说清是哪一道闸不过，而不是只给一个 all_pass=false。"""
    reasons = wave_gate.gate_fail_reasons({
        "total": 8, "passed": 8,
        "diversity_gate": {"applied": True, "pass": False, "issues": ["骨架同质"]},
        "priors_gate": {"pass": True},
    })
    assert any("多样性" in x for x in reasons)
    assert not any("静态闸" in x for x in reasons)  # 8/8 过闸，不该报静态闸

    reasons2 = wave_gate.gate_fail_reasons({"total": 3, "passed": 1})
    assert reasons2 == ["静态闸 1-5 拦截 2/3 条"]


# ---- 端到端：桩 gate.py 驱动三种终态 ----
# 桩复刻 gate.py 的真实契约：payload 前先打日志、payload 最后打印、exit 0 <=> all_pass。

_STUB_GATE = NL.join([
    "import json, os, sys",
    "",
    'mode = os.environ["WAVE_GATE_STUB_MODE"]',
    'print("[stub] gate.py 前置日志（payload 之前的噪声行）")',
    'if mode == "crash":',
    "    raise FileNotFoundError(",
    '        "无白名单/catalog：先跑 scan_fields.py --campaign-dir /tmp/c --dataset pv30")',
    'ok = mode == "pass"',
    'payload = {"all_pass": ok, "dataset": "stubds", "total": 2, "passed": 2, "cached": 0,',
    '           "diversity_gate": {"applied": True, "pass": ok,',
    '                              "issues": [] if ok else ["骨架同质：2/2 条同骨架"]},',
    '           "priors_gate": {"pass": True}, "report": []}',
    "print(json.dumps(payload, ensure_ascii=False, indent=1))",
    'sys.exit(0 if payload["all_pass"] else 1)',
])


@pytest.fixture()
def stub_env(tmp_path):
    """隔离工作区：桩 toolkit + 临时 wqb.db + 最小战役目录，绝不碰真库。"""
    if not any(d and os.path.isfile(os.path.join(d, "validator.py"))
               for d in wave_gate._VALIDATOR_CANDIDATES):
        pytest.skip("alpha-expression-verifier 未安装（wave_gate 语法闸前置依赖）")

    toolkit = tmp_path / "toolkit"
    toolkit.mkdir()
    (toolkit / "gate.py").write_text(_STUB_GATE, encoding="utf-8")

    campaign = tmp_path / "campaign"
    (campaign / "config").mkdir(parents=True)
    (campaign / "config" / "settings.json").write_text(
        json.dumps({"region": "TST"}), encoding="utf-8")

    sys.path.insert(0, os.path.join(REPO, "src"))
    from wqb.store import CampaignStore
    db = str(tmp_path / "data" / "wqb.db")
    st = CampaignStore(db)
    try:
        st.upsert_expressions("TST", "w_stub", ["rank(close)", "rank(open)"],
                              dataset="stubds", status="pending")
    finally:
        st.close()

    env = dict(os.environ)
    env.update({
        "WQ_TOOLKIT_DIR": str(toolkit),
        "WQB_ROOT": str(tmp_path),
        "WQB_DB_PATH": db,
        "PYTHONPATH": os.path.join(REPO, "src") + os.pathsep + os.path.join(REPO, "tools"),
        "PYTHONIOENCODING": "utf-8",
    })
    return env, str(campaign)


def _run(env_campaign, mode):
    env, campaign = env_campaign
    env = dict(env, WAVE_GATE_STUB_MODE=mode)
    return subprocess.run(
        [sys.executable, os.path.join(REPO, "tools", "wave_gate.py"),
         "--campaign-dir", campaign, "--dataset", "stubds",
         "--wave", "w_stub", "--from-db", "--region", "TST"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=env, timeout=600)


def test_gate_crash_is_error_not_fail(stub_env):
    """gate.py 崩溃 → ERROR（退出码 2）+ stderr 原文透传，且不与 FAIL 混同。"""
    r = _run(stub_env, "crash")
    out = r.stdout + r.stderr
    assert r.returncode == 2, out
    assert "[gate ] ERROR:" in out
    assert "[done ] ERROR:" in out
    # 自愈命令来自 gate.py 的异常消息，透传即可，无需 wave_gate 自己拼
    assert "scan_fields.py --campaign-dir" in out
    assert "FileNotFoundError" in out
    # ERROR 不得伪装成"闸门不过"，也不得再出现 all_pass=None
    # （ERROR 文案本身含"不是闸门不过"，所以比对的是 FAIL 路径那一行）
    assert "[gate ] FAIL: 闸门不过" not in out
    assert "all_pass=None" not in out
    assert "=> FAIL" not in out


def test_gate_diversity_fail_is_fail_not_error(stub_env):
    """真多样性 FAIL → FAIL（退出码 1），措辞与 ERROR 路径可区分。"""
    r = _run(stub_env, "fail")
    out = r.stdout + r.stderr
    assert r.returncode == 1, out
    assert "[gate ] FAIL: 闸门不过" in out
    assert "多样性" in out
    assert "=> FAIL" in out
    assert "all_pass=false" in out
    assert "ERROR" not in out


def test_gate_pass(stub_env):
    """gate.py all_pass=true → PASS（退出码 0），且不出现 None 终态。"""
    r = _run(stub_env, "pass")
    out = r.stdout + r.stderr
    assert r.returncode == 0, out
    assert "=> PASS" in out
    assert "all_pass=true" in out
    assert "all_pass=None" not in out
    assert "ERROR" not in out
