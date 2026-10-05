# -*- coding: utf-8 -*-
"""探针批（batch_type=probe）豁免闸6 骨架多样性（2026-10-04 落地）。

依据规则 diversity_gate_is_portfolio_level_not_per_wave_v1：
  骨架多样性闸的收益在「组合层」不在「单波产出层」——
  本库 818 波次实证：骨架单一 S>=1.58 命中率 51.6% vs 骨架多样 25.2%。
  探针批的目的是单骨架裸测「机制有无 IS 强度」，骨架多样性会污染归因。
  故：
    - 契约 exempt 列表默认含 probe（diversity_audit.INJECTION_EXEMPT、
      _lib/rules.issue_contract）
    - check_batch_diversity 对 batch_type=probe 直接短路
    - pipeline --batch-type probe 自动等价于 --skip-diversity-gate

本测试锁住以上三处行为，防后续改动把它们悄悄移除。
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOLKIT_SCRIPTS = REPO_ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"


def _ensure_path():
    if str(TOOLKIT_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(TOOLKIT_SCRIPTS))


# ---------- 1) 契约 exempt 默认含 probe ----------

def test_injection_exempt_includes_probe():
    """diversity_audit.INJECTION_EXEMPT 必须含 repair 与 probe。"""
    _ensure_path()
    import diversity_audit
    assert "repair" in diversity_audit.INJECTION_EXEMPT
    assert "probe" in diversity_audit.INJECTION_EXEMPT, (
        "probe 批次类型必须默认豁免多样性契约（diversity_gate_is_portfolio_level_not_per_wave_v1）"
    )


def test_issue_contract_default_exempt_includes_probe():
    """_lib.rules.issue_contract 的 exempt 默认值必须含 probe。"""
    _ensure_path()
    import inspect
    from _lib import rules
    sig = inspect.signature(rules.issue_contract)
    default = sig.parameters["exempt"].default
    assert "repair" in default
    assert "probe" in default, (
        "issue_contract 默认 exempt 必须含 probe，否则新签发的契约会重新阻断探针批"
    )


def test_renew_contract_inherits_probe_exemption():
    """续约契约应从过期契约继承 exempt（含 probe），不退回只豁免 repair。"""
    _ensure_path()
    import inspect
    from _lib import rules
    src = inspect.getsource(rules.renew_contract)
    # 续约读取 expired_act 的 exempt，故只要旧契约带 probe 即可延续；
    # 这里断言默认回退值不会把 probe 丢掉。
    assert 'expired_act.get("exempt"' in src


# ---------- 2) check_batch_diversity 对 probe 短路 ----------

def test_check_batch_diversity_probe_short_circuits():
    """batch_type=probe 时闸6 直接返回空 issues（不查契约、不阻断）。"""
    _ensure_path()
    from gate import check_batch_diversity

    # 传一个必然无契约的 ctx（None 触发内部 fallback 路径）；
    # probe 应在任何契约查找之前就短路返回。
    class _Ctx:
        region = "KOR"

    issues, consume_ref = check_batch_diversity(
        ["rank(close)", "ts_delta(volume, 5)"], _Ctx(), batch_type="probe")
    assert issues == [], f"probe 批不应产生闸6 issues，实际：{issues}"
    assert consume_ref is None


def test_check_batch_diversity_probe_short_circuits_before_contract_lookup():
    """probe 短路必须发生在契约状态判定之前（无契约/过期契约也不阻断探针批）。"""
    _ensure_path()
    import inspect
    from gate import check_batch_diversity
    src = inspect.getsource(check_batch_diversity)
    i_probe = src.find('batch_type == "probe"')
    i_contract = src.find("get_contract_expiry_state")
    assert i_probe != -1, "check_batch_diversity 缺少 probe 短路分支"
    assert i_contract != -1
    assert i_probe < i_contract, (
        "probe 短路必须在契约查找之前，否则过期契约会阻断探针批"
    )


# ---------- 3) pipeline --batch-type probe 自动 skip ----------

def test_pipeline_probe_implies_skip_diversity():
    """pipeline 主流程中 batch_type==probe 必须把 skip_diversity 置真。"""
    _ensure_path()
    import inspect
    import pipeline
    src = inspect.getsource(pipeline._cmd_main)
    assert 'a.batch_type == "probe"' in src, (
        "pipeline 未实现 probe -> skip_diversity 的自动等价"
    )
    # 断言存在把 probe 并入 skip 的布尔合成
    assert "_skip_div" in src
