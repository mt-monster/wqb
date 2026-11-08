# -*- coding: utf-8 -*-
"""datasets 伪数据集行修复器 datasets_phantom_repair（2026-11-06）。

守四件事：
1. dry-run 只出报告、不改库，且发现脏行时 exit 1；
2. --apply 归档 + 重指向本区 _unknown 哨兵 + 删除活表行（含 ILLIQUID 那种
   「本区还没有哨兵」的情形 —— 哨兵要被补建出来）；
3. expressions.dataset 洗白（--keep-expression-dataset 可关）；
4. 生产库上禁止 --no-backup（备份是唯一回滚路径），缺库 exit 2，二次跑幂等。
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.db_conn import connect as db_connect  # noqa: E402
from wqb.store import CampaignStore            # noqa: E402


def _load_tool():
    path = REPO_ROOT / "tools" / "db" / "datasets_phantom_repair.py"
    spec = importlib.util.spec_from_file_location("datasets_phantom_repair", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


repair = _load_tool()

SENTINEL = "_unknown"
PHANTOM = "pv/model/other"


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """临时「仓库根」：WQB_ROOT 指过去，脚本/守卫的路径探测都落在 tmp 内。"""
    root = tmp_path / "repo"
    (root / "src" / "wqb").mkdir(parents=True)
    (root / "data").mkdir()
    (root / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    monkeypatch.setenv("WQB_ROOT", str(root))
    return root


def _seed(repo):
    """建库 + 一个真数据集 + 一个伪数据集行 + 三张表的引用 + 一条脏 expressions。"""
    path = repo / "data" / "wqb.db"
    store = CampaignStore(str(path))
    good = store._ensure_dataset("KOR", "pv106")
    store.close()

    conn = db_connect(str(path))
    try:
        cur = conn.cursor()
        cur.execute("SELECT region_id FROM datasets WHERE id=?", (good,))
        rid = int(cur.fetchone()[0])

        cur.execute("INSERT INTO datasets (name, region_id) VALUES (?,?)", (PHANTOM, rid))
        phantom = int(cur.lastrowid)

        cur.execute(
            "INSERT INTO alphas (alpha_id, expression, region_id, dataset_id) VALUES (?,?,?,?)",
            ("A1", "rank(close)", rid, phantom),
        )
        cur.execute(
            "INSERT INTO waves (region_id, wave_number, dataset_id) VALUES (?,?,?)",
            (rid, "W1", phantom),
        )
        cur.execute(
            "INSERT INTO field_profile (dataset_id, field_name) VALUES (?,?)",
            (phantom, "f1"),
        )
        # expressions 走「先写对、再改脏」—— 历史脏行就是这么来的
        cur.execute(
            "INSERT INTO waves (region_id, wave_number, dataset_id) VALUES (?,?,?)",
            (rid, "W2", good),
        )
        w2 = int(cur.lastrowid)
        cur.execute(
            "INSERT INTO expressions (wave_id, expression, dataset) VALUES (?,?,?)",
            (w2, "rank(close)", PHANTOM),
        )
        conn.commit()
    finally:
        conn.close()
    return path, phantom, good, rid


def _sentinel_id(path, rid):
    conn = db_connect(str(path), readonly=True)
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM datasets WHERE region_id=? AND name=?", (rid, SENTINEL)
        )
        row = cur.fetchone()
        return int(row[0]) if row else None
    finally:
        conn.close()


def test_dry_run_reports_without_mutating(repo, capsys):
    path, phantom, _good, rid = _seed(repo)
    assert repair.main(["--db", str(path), "--json"]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["phantom_rows"] == 1
    assert out["phantom_by_region"] == {"KOR": 1}
    assert out["refs"]["alphas.dataset_id"] == 1
    assert out["regions_missing_sentinel"] == ["KOR"]
    assert out["expression_hits"] == {PHANTOM: 1}
    # 一点没动
    conn = db_connect(str(path), readonly=True)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM datasets WHERE name=?", (PHANTOM,))
        assert cur.fetchone()[0] == 1
        cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='datasets_phantom_archive'")
        assert cur.fetchone()[0] == 0
    finally:
        conn.close()


def test_apply_archives_repoints_and_deletes(repo):
    path, phantom, good, rid = _seed(repo)
    assert repair.main(["--db", str(path), "--apply"]) == 0

    sentinel = _sentinel_id(path, rid)
    assert sentinel is not None

    conn = db_connect(str(path), readonly=True)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM datasets WHERE name=?", (PHANTOM,))
        assert cur.fetchone()[0] == 0

        # 三张表的引用全部改指哨兵，旧 id 一条不留
        for table in ("alphas", "waves", "field_profile"):
            cur.execute(f"SELECT COUNT(*) FROM {table} WHERE dataset_id=?", (sentinel,))
            assert cur.fetchone()[0] == 1, table
            cur.execute(f"SELECT COUNT(*) FROM {table} WHERE dataset_id=?", (phantom,))
            assert cur.fetchone()[0] == 0, table

        # 归档留痕
        cur.execute(
            "SELECT name, region, repointed_to, repointed_to_name, refs_json "
            "FROM datasets_phantom_archive"
        )
        rows = cur.fetchall()
        assert len(rows) == 1
        name, region, repointed, repointed_name, refs_json = rows[0]
        assert (name, region) == (PHANTOM, "KOR")
        assert (repointed, repointed_name) == (sentinel, SENTINEL)
        assert json.loads(refs_json)["alphas.dataset_id"] == 1

        # expressions.dataset 洗白为 NULL
        cur.execute("SELECT dataset FROM expressions")
        assert [r[0] for r in cur.fetchall()] == [None]

        # 真数据集不受影响
        cur.execute("SELECT name FROM datasets WHERE id=?", (good,))
        assert cur.fetchone()[0] == "pv106"
    finally:
        conn.close()


def test_apply_creates_backup_file(repo):
    path, _phantom, _good, _rid = _seed(repo)
    assert repair.main(["--db", str(path), "--apply"]) == 0
    baks = list((repo / "data").glob("wqb.db.bak_phantom_*"))
    assert len(baks) == 1


def test_keep_expression_dataset_flag(repo):
    path, _phantom, _good, _rid = _seed(repo)
    assert repair.main(["--db", str(path), "--apply", "--keep-expression-dataset"]) == 0
    conn = db_connect(str(path), readonly=True)
    try:
        cur = conn.cursor()
        cur.execute("SELECT dataset FROM expressions")
        assert [r[0] for r in cur.fetchall()] == [PHANTOM]
    finally:
        conn.close()


def test_no_backup_refused_on_production_path(repo):
    path, phantom, _good, _rid = _seed(repo)
    assert repair.main(["--db", str(path), "--apply", "--no-backup"]) == 2
    conn = db_connect(str(path), readonly=True)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM datasets WHERE name=?", (PHANTOM,))
        assert cur.fetchone()[0] == 1, "拒绝执行时必须零改动"
    finally:
        conn.close()


def test_second_apply_is_noop(repo):
    path, _phantom, _good, rid = _seed(repo)
    assert repair.main(["--db", str(path), "--apply"]) == 0
    sentinel = _sentinel_id(path, rid)
    assert repair.main(["--db", str(path), "--apply"]) == 0
    assert _sentinel_id(path, rid) == sentinel
    conn = db_connect(str(path), readonly=True)
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM datasets_phantom_archive")
        assert cur.fetchone()[0] == 1, "归档不应重复写"
    finally:
        conn.close()


def test_missing_db_exit_2(repo):
    assert repair.main(["--db", str(repo / "data" / "nope.db")]) == 2
