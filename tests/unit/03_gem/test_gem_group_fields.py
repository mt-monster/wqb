"""GROUP axes must survive the CLI chain without becoming numeric signals."""
import argparse
import ast
import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[3]


def _implementation():
    path = ROOT / 'Claude/skills/brain-feature-implementation/scripts/implement_idea.py'
    spec = importlib.util.spec_from_file_location('group_binding_regression', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('relative', [
    'brain-make-some-gem/scripts/headless_runner/run.py',
    'brain-make-some-gem/scripts/trailSomeAlphas/run_pipeline.py',
    'brain-feature-implementation/scripts/fetch_dataset.py',
])
def test_each_cli_boundary_accepts_group_without_network_or_credentials(relative):
    path = ROOT / 'Claude/skills' / relative
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    argument = next(n for n in ast.walk(tree)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr == 'add_argument' and n.args
                    and isinstance(n.args[0], ast.Constant) and n.args[0].value == '--data-type')
    parser = argparse.ArgumentParser()
    statement = ast.fix_missing_locations(ast.Module(body=[ast.Expr(value=argument)], type_ignores=[]))
    exec(compile(statement, str(path), 'exec'), {'parser': parser})
    assert parser.parse_args(['--data-type', 'GROUP']).data_type == 'GROUP'
    assert parser.parse_args([]).data_type == 'MATRIX'
    with pytest.raises(SystemExit):
        parser.parse_args(['--data-type', 'NOT_A_TYPE'])


@pytest.mark.parametrize('type_column', ['type', 'dataType', 'data_type'])
def test_group_concept_keeps_only_original_expression(type_column):
    impl = _implementation()
    frame = pd.DataFrame({'id': ['customer_cluster'], type_column: ['GROUP']})
    template = 'rank(group_mean(ts_sum(returns,22),1,densify({customer_cluster})))'
    assert impl.match_single_horizon_auto(frame, template) == [
        ('flex', 'rank(group_mean(ts_sum(returns,22),1,densify(customer_cluster)))')
    ]
