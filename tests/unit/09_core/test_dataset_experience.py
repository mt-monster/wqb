import hashlib
from pathlib import Path
import subprocess
import sys

import pytest

from wqb.research.dataset_experience import (
    BEGIN, END, expression_fields, load_evidence, main, render_dataset, write_report,
)
from wqb.store.campaign import CampaignStore

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def db(tmp_path):
    path = tmp_path / 'wqb.db'
    with CampaignStore(str(path)) as store:
        store.upsert_field_catalog('EUR', {'dataset':'sample', 'fields': [
            {'id': 'cash', 'type': 'MATRIX', 'coverage': .8, 'userCount': 0, 'description': 'cash'},
            {'id': 'assets', 'type': 'MATRIX', 'coverage': .9, 'userCount': 1, 'description': 'assets'}]})
        for wave, aid, delay, status in [('1','A',1,'COMPLETE'),('2','B',0,'COMPLETE'),('3','C',1,'ERROR')]:
            store.upsert_backtest_rows('EUR', wave, [{
                'id': aid, 'code': 'reverse(rank(divide(cash,assets)))', 'status': status,
                'sharpe': 1.5, 'fitness': .9, 'two_year_sharpe': 2.,
                'turnover': .02, 'delay': delay, 'universe': 'TOPCS1600',
                'neutralization': 'SUBINDUSTRY', 'prod_corr': .75 if aid=='A' else None,
            }], dataset='sample')
        store.upsert_ledger('EUR', 'review_1', {'all':[{'id':'A','robust_sharpe':.65}]})
    return path


def test_scope_uses_actual_wave_and_delay_without_writing_db(db):
    before = hashlib.sha256(db.read_bytes()).hexdigest()
    evidence = load_evidence(db, 'EUR', 'sample', ['1','2','3'], 1)
    assert [r['alpha_id'] for r in evidence['rows']] == ['A']
    assert evidence['rows'][0]['prod_correlation'] == .75
    assert evidence['rows'][0]['self_correlation'] is None
    assert hashlib.sha256(db.read_bytes()).hexdigest() == before
    rendered = render_dataset(evidence, 'sample')
    assert '未核实' in rendered and '不能当作样本外收益或可提交判定' in rendered
    assert '| 1 | `A` |' in rendered and '`B`' not in rendered and '`C`' not in rendered


def test_missing_delay_is_not_assumed_to_be_d1(db):
    with CampaignStore(str(db)) as store:
        store.upsert_backtest_rows('EUR','4',[{'id':'D','code':'rank(cash)','sharpe':2,'fitness':1}],dataset='sample')
    evidence = load_evidence(db,'EUR',delay=1)
    assert [r['alpha_id'] for r in evidence['rows']] == ['A']
    assert any('D delay 未知' in w for w in evidence['warnings'])


def test_unary_and_repeated_fields_are_extracted():
    assert expression_fields('if_else(greater(cash,0),-rank(divide(financing,abs(cash))),0)') == ['cash','financing']


def test_refresh_preserves_human_analysis_and_is_idempotent(tmp_path):
    path = tmp_path / 'eur_sample_campain.md'
    block = f'{BEGIN}\nfirst\n{END}\n'
    assert write_report(path,block,'title')
    path.write_text(path.read_text(encoding='utf-8')+'\n人工判断：A的Prod超标，不能提交。\n',encoding='utf-8')
    newer = block.replace('first','second')
    assert write_report(path,newer,'title')
    assert '人工判断：A的Prod超标' in path.read_text(encoding='utf-8')
    assert not write_report(path,newer,'title')
    path.write_text(BEGIN+' broken',encoding='utf-8')
    with pytest.raises(ValueError):
        write_report(path,newer,'title')
    assert path.read_text(encoding='utf-8') == BEGIN+' broken'


def test_dry_run_has_no_output_side_effects(db,tmp_path):
    out = tmp_path / 'never-created'
    assert main(['--region','EUR','--db',str(db),'--delay','1','--out-dir',str(out),'--dry-run']) == 0
    assert not out.exists()


def test_toolkit_dispatch_reaches_real_reporter(db,tmp_path):
    out = tmp_path / 'reports'
    proc = subprocess.run([
        sys.executable, '-X','utf8',
        str(ROOT/'Claude/skills/wq-brain-campaign-toolkit/scripts/campaign.py'),
        '--campaign-dir',str(ROOT/'tracking/EUR'),'dataset-experience','--dataset','sample',
        '--db',str(db),'--delay','1','--out-dir',str(out)],
        cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=30)
    assert proc.returncode == 0, proc.stderr
    assert (out/'eur_sample_campain.md').exists()
    assert '`A`' in (out/'eur_sample_campain.md').read_text(encoding='utf-8')


def test_campaign_route_has_dataset_and_only_one_subcommand(monkeypatch):
    from wqb.workflow.nodes import campaign
    monkeypatch.setattr(campaign,'resolve_toolkit_dir',lambda: str(ROOT/'Claude/skills/wq-brain-campaign-toolkit/scripts'))
    result = campaign.run(region='EUR',stage='S6',subcommand='dataset-experience',dataset='news46',
        extra_args=['--delay','1'],_context={'dry_run':True})
    assert result['success'], result
    command = next(s['command'] for s in result['steps'] if s['step']=='build_command')
    assert command.count(' dataset-experience') == 1
    assert '--dataset news46' in command and '--delay 1' in command


def test_default_output_targets_repository_from_foreign_cwd(db, tmp_path):
    proc = subprocess.run([
        sys.executable, '-X', 'utf8', str(ROOT/'tools/dataset_experience.py'),
        '--region', 'EUR', '--db', str(db), '--delay', '1', '--dry-run'],
        cwd=tmp_path, capture_output=True, text=True, encoding='utf-8', timeout=30)
    assert proc.returncode == 0, proc.stderr
    assert str(ROOT/'reports/dataset_experience/eur_sample_campain.md') in proc.stdout
    assert not (tmp_path/'reports').exists()
