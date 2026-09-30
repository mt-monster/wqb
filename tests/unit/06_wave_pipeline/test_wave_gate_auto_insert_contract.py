# -*- coding: utf-8 -*-
"""wave_gate「自动注入参数」调用契约的守护（2026-09-27 新增）。

## 缘起（真实事故，非假想）

`world-quant-brain-mcp/tools_workflow.py:446-466` 会对 `gem → batch_track` 链**自动插入**
wave_gate 节点（2026-09-25 P3 fail-safe，防止 Agent 走自动链时跳过闸 PF），插入参数含
`prod_family_gate=True`；而 `src/wqb/workflow/nodes/wave_gate.py` 的 `run()` 当时**无此形参**
→ 该类链 100% 抛 `TypeError: run() got an unexpected keyword argument 'prod_family_gate'`
（2026-09-27 dry-run 实证，`failed_at=wave_gate`）。

**守护缺口**：`tools/audit_node_registration.py` 校验的是 *registry 元数据 vs run() 签名*，
**不覆盖「自动注入参数」这一调用侧** → 漂移零命中。本模块补上这一层。

## 反向负例原则（RULES.md：豁免式守护必配反向负例）

只断言"参数集 ⊆ 签名"会因为**解析器失效**（正则失配返回空集）而静默假绿 ——
故 `test_auto_insert_guard_is_not_vacuous` 先断言解析器确实抓到了 `prod_family_gate`。
"""
from __future__ import annotations

import inspect
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLS_WORKFLOW = REPO_ROOT / "world-quant-brain-mcp" / "tools_workflow.py"
WAVE_GATE_CLI = REPO_ROOT / "tools" / "wave_gate.py"


def _auto_inserted_params() -> set:
    """从 tools_workflow.py 解析自动插入的 wave_gate 参数名集合。"""
    if not TOOLS_WORKFLOW.is_file():
        return set()
    text = TOOLS_WORKFLOW.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'"node"\s*:\s*"wave_gate".*?"params"\s*:\s*\{(.*?)\}', text, re.S)
    if not m:
        return set()
    return set(re.findall(r'"(\w+)"\s*:', m.group(1)))


def _run_signature_params() -> set:
    from src.wqb.workflow.nodes import wave_gate

    return set(inspect.signature(wave_gate.run).parameters)


def test_auto_insert_guard_is_not_vacuous():
    """反向负例①：解析器必须真的抓到 `prod_family_gate`，否则后续断言会静默空跑（假绿）。"""
    params = _auto_inserted_params()
    assert "prod_family_gate" in params, (
        "未能从 tools_workflow.py 解析出自动注入的 wave_gate 参数（正则失效，或该 fail-safe 被移除）。"
        "若 fail-safe 确实已删除，请同步删除本守护——不要让它退化成永远通过的空断言"
    )


def test_auto_inserted_params_are_accepted_by_run():
    """调用侧自动注入的**每一个**参数都必须被 `wave_gate.run()` 接受。

    这是本次事故的直接判据：`audit_node_registration.py` 管的是 registry 元数据，
    管不到 `tools_workflow.py` 里硬编码的自动插入参数，所以必须单列一条。
    """
    injected = _auto_inserted_params()
    accepted = _run_signature_params()
    missing = sorted(injected - accepted)
    assert not missing, (
        "自动注入的 wave_gate 参数 run() 不接受 —— `gem → batch_track` 链会以 TypeError 整链失败"
        "（2026-09-27 实证：`prod_family_gate`）。缺参：" + ", ".join(missing)
    )


def test_prod_family_gate_has_cli_flag():
    """节点参数必须落在 CLI 已声明的 flag 上，否则 `validate_argv` 会判 argv 契约失败。"""
    assert WAVE_GATE_CLI.is_file(), f"缺少 {WAVE_GATE_CLI}"
    text = WAVE_GATE_CLI.read_text(encoding="utf-8", errors="replace")
    for flag in ("--prod-family-gate", "--no-prod-family-gate"):
        assert flag in text, f"tools/wave_gate.py 未声明 {flag}（节点透传会触发 argv 契约失败）"


def test_wave_gate_dry_run_accepts_auto_inserted_params(tmp_path):
    """反向负例②：端到端——按自动注入的参数集真调一次 dry_run，不得 TypeError。

    dry_run 只构建命令并过 argv 契约校验，不 subprocess、不写库（AGENTS.md 干跑契约）。
    `campaign_dir` 用 tmp_path 以避免依赖 `tracking/<region>` 是否真实存在。
    """
    from src.wqb.workflow.nodes import wave_gate

    res = wave_gate.run(
        region="GBR",
        dataset="starmine",
        wave="auto",
        campaign_dir=str(tmp_path),
        inspect_mode="warn",
        prod_family_gate=True,
        dry_run=True,
    )
    assert res.get("success") is True, f"dry_run 未成功（通常是 TypeError 或 argv 校验失败）：{res}"
    plan = res.get("plan") or ""
    assert "--prod-family-gate" in plan, f"闸 PF 未透传到 CLI：{plan}"
    assert "--no-prod-family-gate" not in plan
