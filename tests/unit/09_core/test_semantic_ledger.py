# -*- coding: utf-8 -*-
"""wqb.semantic_ledger —— `s1_semantic_*` 台账的 L3.5 判定唯一口径（2026-10-05 补测试）。

守两件事（都是实测踩过的坑）：
1. **判定用「键存在」而非「族非空」**：原生集（fundamental*/pv*/news*）字段名不带角色后缀，
   `families` 为空是正确结果；若按「族为空」判待补做，每次 S1 都会重跑，永不幂等。
2. **两个消费点同源**：`campaign._semantic_coverage_check`（补做触发）与
   `field_semantic_classify --all`（跳过条件）必须给同一个答案，否则同一数据集
   被反复重跑或永远漏补 L3.5 族。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from wqb.semantic_ledger import family_count, ledger_has_l35, parse_ledger  # noqa: E402


def _val(**extra):
    return json.dumps({"region": "KOR", "dataset": "model109", "total_fields": 120,
                       "blocked_field_count": 40, **extra}, ensure_ascii=False)


def test_parse_ledger_accepts_str_dict_bytes_and_refuses_garbage():
    d = {"a": 1}
    assert parse_ledger(json.dumps(d)) == d
    assert parse_ledger(d) is d                      # 已是 dict 原样返回
    assert parse_ledger(json.dumps(d).encode("utf-8")) == d
    assert parse_ledger("") is None                  # 空台账
    assert parse_ledger(None) is None
    assert parse_ledger("not json") is None          # 脏值不抛，交调用方判缺
    assert parse_ledger("[1,2]") is None             # 合法 JSON 但非 dict
    assert parse_ledger(123) is None


def test_has_l35_is_key_presence_not_family_emptiness():
    """★ 幂等性核心：空 families 仍算「已含 L3.5」，不得判成待补做。"""
    assert ledger_has_l35(_val(families={}, family_stats={"n_families": 0})) is True
    assert family_count(_val(families={}, family_stats={})) == 0
    # 旧版台账（families 功能之前生成）：两键都不存在 → 待补做
    assert ledger_has_l35(_val(signal_field_count=80)) is False
    # 任一键存在即可（历史上出现过只写 family_stats 的中间版本）
    assert ledger_has_l35(_val(family_stats={"n_families": 3})) is True
    assert ledger_has_l35(_val(families={"rev_q": {"n": 4}})) is True
    assert family_count(_val(families={"rev_q": {"n": 4}, "eps_q": {"n": 2}})) == 2


def test_has_l35_never_raises_on_broken_rows():
    """读真库时脏 value 不可避免；判定必须 fail 到 False（=待补做），不能抛断 S1。"""
    for bad in ("", "   ", "{oops", "null", '"a string"', 42, None):
        assert ledger_has_l35(bad) is False


def test_two_consumers_share_the_single_source():
    """两个消费点必须从本模块取判定，不得各自再写一份（漂移即分叉）。"""
    for rel in (ROOT / "src" / "wqb" / "workflow" / "nodes" / "campaign.py",
                ROOT / "tools" / "field_semantic_classify.py"):
        src = rel.read_text(encoding="utf-8")
        assert "from wqb.semantic_ledger import" in src, rel.name
        assert "ledger_has_l35(" in src, rel.name
        # 口径只能来自本模块：不得就地重做 JSON 解析 + 键判定
        assert '"family_stats" in' not in src and "'family_stats' in" not in src, rel.name
