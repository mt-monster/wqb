"""Concept binding must retain a field reused in a condition and its signal."""
import importlib.util
from pathlib import Path

import pandas as pd


def _implementation():
    root = Path(__file__).resolve().parents[3]
    path = root / "Claude/skills/brain-feature-implementation/scripts/implement_idea.py"
    spec = importlib.util.spec_from_file_location("concept_binding_regression", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_conditional_financing_concept_keeps_repeated_cashflow_binding():
    impl = _implementation()
    template = "if_else(greater({operating_cashflow},0),-rank(divide({total_financing_cash_flow},abs({operating_cashflow}))),0)"
    frame = pd.DataFrame({"id": ["operating_cashflow", "total_financing_cash_flow"]})
    result = impl.match_single_horizon_auto(frame, template)
    assert [expr for _, expr in result] == [
        "if_else(greater(operating_cashflow,0),-rank(divide(total_financing_cash_flow,abs(operating_cashflow))),0)"
    ]


def test_distinct_placeholders_cannot_create_a_same_field_identity():
    impl = _implementation()
    frame = pd.DataFrame({"id": ["operating_cashflow"]})
    assert impl.match_single_horizon_auto(
        frame, "rank(divide({operating_cashflow},{cashflow}))"
    ) == []
