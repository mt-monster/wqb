# -*- coding: utf-8 -*-
"""2026-09-19：bucket() 缺 range=/buckets= 必须被本地语法闸拦下（JPN wave7 实证：平台 ERROR 整批连坐）。"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VAL_DIR = REPO_ROOT / "Claude" / "skills" / "alpha-expression-verifier" / "scripts"
if str(VAL_DIR) not in sys.path:
    sys.path.insert(0, str(VAL_DIR))

import validator as v  # noqa: E402


def _check(expr):
    return v.ExpressionValidator().check_expression(expr)


def test_bucket_without_range_or_buckets_fails():
    r = _check("group_neutralize(rank(close), bucket(rank(volume)))")
    assert r.get("valid") is False or r.get("errors")
    assert any("bucket" in e and ("range" in e or "buckets" in e) for e in r.get("errors", []))


def test_bucket_with_range_or_buckets_passes():
    for e in ('group_neutralize(rank(close), bucket(rank(volume), range="0,1,0.1"))',
              'group_rank(close, bucket(rank(volume), buckets="0.2,0.4,0.6,0.8"))'):
        r = _check(e)
        assert not [x for x in r.get("errors", []) if "bucket" in x], r
