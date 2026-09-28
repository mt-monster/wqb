# -*- coding: utf-8 -*-
"""2026-09-20：densify() 的输入/输出都是分组键（平台语义），本地闸不得把
densify(bucket(...)) 判成 Unit[Group:1] 不兼容（ASI robust 论坛配方 37473718017175 实证可跑）。"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VAL_DIR = REPO_ROOT / "Claude" / "skills" / "alpha-expression-verifier" / "scripts"
if str(VAL_DIR) not in sys.path:
    sys.path.insert(0, str(VAL_DIR))

import validator as v  # noqa: E402


def _check(expr):
    return v.ExpressionValidator().check_expression(expr)


def test_densify_bucket_inside_cartesian_passes():
    exprs = [
        'group_neutralize(rank(close), group_cartesian_product(country, densify(bucket(rank(cap), range="0,1,0.1"))))',
        '-group_zscore(ts_decay_linear(close, 5), group_cartesian_product(country, densify(bucket(rank(cap), range="0,1,0.1"))))',
        'group_rank(close, densify(bucket(rank(volume), range="0,1,0.2")))',
    ]
    for e in exprs:
        r = _check(e)
        assert not [x for x in r.get("errors", []) if "densify" in x or "Incompatible unit" in x], (e, r)


def test_densify_output_is_still_a_group_key():
    # densify 产物是分组键：喂给非 group 参数位仍应报单位不兼容
    r = _check('rank(densify(bucket(rank(cap), range="0,1,0.1")))')
    assert any("Incompatible unit" in x for x in r.get("errors", [])), r


def test_densify_accepts_dataset_group_identifier_syntax():
    # Syntax has no field catalog; native GROUP axes are ordinary identifiers.
    expr = ('rank(group_mean(ts_sum(returns,22),1,'
            'densify(oth455_customer_n2v_p10_q200_w1_kmeans_cluster_5)))')
    result = _check(expr)
    assert result['valid'], result


def test_densify_field_output_cannot_be_used_as_numeric_signal():
    result = _check('rank(densify(customer_cluster))')
    assert not result['valid'], result
    assert any('Incompatible unit' in error for error in result['errors']), result


def test_densify_does_not_accept_scalar_or_arbitrary_numeric_expression():
    for expr in ('densify(5)', 'densify(ts_sum(returns,22))'):
        result = _check(expr)
        assert not result['valid'], (expr, result)
