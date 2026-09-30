"""A wave query must not relabel every alpha from the same dataset."""
import importlib.util
from pathlib import Path
import sqlite3


def test_wave_membership_is_backtest_provenance(tmp_path, monkeypatch):
    path = tmp_path / "waves.db"
    with sqlite3.connect(path) as conn:
        conn.executescript("""
            CREATE TABLE regions (id INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE waves (id INTEGER, region_id INTEGER, dataset_id INTEGER, wave_number TEXT);
            CREATE TABLE alphas (alpha_id TEXT, region_id INTEGER, dataset_id INTEGER, sharpe REAL);
            CREATE TABLE backtest_results (region TEXT, wave TEXT, alpha_id TEXT);
            INSERT INTO regions VALUES (1, 'EUR'), (2, 'USA');
            INSERT INTO waves VALUES (1,1,17,'251'), (2,1,17,'252'), (3,1,17,'253'), (4,2,17,'252');
            INSERT INTO alphas VALUES ('OLD',1,17,1.18), ('NEW',1,17,.8), ('OTHER',2,17,2.1);
            INSERT INTO backtest_results VALUES ('EUR','251','OLD'), ('EUR','252','NEW'),
                ('USA','252','OTHER'), ('EUR','252','NEW'), ('USA','252','OLD');
        """)
    spec = importlib.util.spec_from_file_location(
        "db_wave_membership_test", Path(__file__).resolve().parents[3] / "wqb_db_mcp.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "DB_PATH", path)
    assert [x["alpha_id"] for x in module.list_alphas_by_wave("EUR", 251)] == ["OLD"]
    rows = module.list_alphas_by_wave("EUR", 252)
    assert [(x["alpha_id"], x["region"], x["wave_number"]) for x in rows] == [("NEW", "EUR", "252")]
    assert module.list_alphas_by_wave("EUR", 253) == []
    assert [x["alpha_id"] for x in module.list_alphas_by_wave("USA", 252)] == ["OTHER"]
