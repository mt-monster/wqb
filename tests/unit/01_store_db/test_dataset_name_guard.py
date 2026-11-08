# -*- coding: utf-8 -*-
"""datasets.name 形状守卫（2026-11-06）。

背景：_ensure_dataset(region, name) 会按传入的**任意字符串**现建 datasets 行，
而 _ensure_wave / _backtest 把塔位组合标签、表达式描述、region 名原样透传
=> 实测 82 行从来不是数据集的行落进表里，污染任何按 datasets 表的统计。

本测试守三件事：
1. config.is_phantom_dataset_name 的形状口径（含 _unknown 白名单）；
2. 写入口被拒时**回落本区 _unknown 哨兵**，不新建污染行；
3. 被拒名字留审计行，且审计写失败不得阻断写库。
"""
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
for _p in (REPO_ROOT, REPO_ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from wqb.config import DATASET_SENTINEL, is_phantom_dataset_name  # noqa: E402
from wqb.store import CampaignStore  # noqa: E402


@pytest.fixture
def store(tmp_path, monkeypatch):
    # 审计日志要落到 tmp（守卫按 wqb.paths 向上探测取根），别污染真 logs/
    root = tmp_path / "repo"
    (root / "src" / "wqb").mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    monkeypatch.setenv("WQB_ROOT", str(root))
    db = CampaignStore(str(tmp_path / "camp.db"))
    yield db
    db.close()


@pytest.mark.parametrize("name", [
    "risk/model",
    "pv/model/other",
    "analyst/fundamental",
    "fundamental44|institutions6",
    "insiders1,sentiment21",
    "KOR",                                  # region 名被当成 dataset
    "earnings3_ASI",                        # 大写后缀
    "analyst+imbalance5+risk68 (CORE+风险尾部门控, 三塔effective0)",
    "__sem_gate_no_ledger__",
    "",
    None,
])
def test_phantom_names_rejected(name):
    assert is_phantom_dataset_name(name) is True


@pytest.mark.parametrize("name", [
    "fnd6", "anl4", "other455", "pv106", "sentiment21", "fundamental6", "a",
    DATASET_SENTINEL,                        # store 刻意哨兵，必须放行
])
def test_real_dataset_ids_accepted(name):
    assert is_phantom_dataset_name(name) is False


def test_guard_falls_back_to_sentinel(store):
    did = store._ensure_dataset("KOR", "pv/model/other")
    cur = store.connection.cursor()
    cur.execute("SELECT name FROM datasets WHERE id=?", (did,))
    assert cur.fetchone()[0] == DATASET_SENTINEL
    cur.execute("SELECT COUNT(*) FROM datasets WHERE name=?", ("pv/model/other",))
    assert cur.fetchone()[0] == 0


def test_guard_is_idempotent_and_shares_one_sentinel(store):
    a = store._ensure_dataset("KOR", DATASET_SENTINEL)
    b = store._ensure_dataset("KOR", "risk/model")
    c = store._ensure_dataset("KOR", "fundamental44|institutions6")
    assert a == b == c
    cur = store.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM datasets WHERE name=?", (DATASET_SENTINEL,))
    assert cur.fetchone()[0] == 1


def test_guard_does_not_touch_real_dataset(store):
    did = store._ensure_dataset("KOR", "pv106")
    cur = store.connection.cursor()
    cur.execute("SELECT name FROM datasets WHERE id=?", (did,))
    assert cur.fetchone()[0] == "pv106"


def test_ensure_wave_junk_dataset_lands_on_sentinel(store):
    """_ensure_wave 是历史脏名的**主要透传口**（82 行多数从这儿进来）。"""
    wid = store._ensure_wave("KOR", "W1", "pv/model/other")
    cur = store.connection.cursor()
    cur.execute(
        "SELECT d.name FROM waves w JOIN datasets d ON d.id = w.dataset_id WHERE w.id=?",
        (wid,),
    )
    assert cur.fetchone()[0] == DATASET_SENTINEL


def test_guard_writes_audit_line(store, tmp_path):
    store._ensure_dataset("KOR", "risk/model")
    log = tmp_path / "repo" / "logs" / "datasets_phantom_names.jsonl"
    assert log.is_file()
    lines = log.read_text(encoding="utf-8").strip().splitlines()
    rec = json.loads(lines[-1])
    assert rec["region"] == "KOR"
    assert rec["rejected_name"] == "risk/model"


def test_audit_failure_does_not_break_write(store, monkeypatch):
    """磁盘满 / 只读挂载不该把回测流水线打挂 —— 守卫只负责不新建污染行。"""
    import wqb.store._schema as schema_mod

    def _boom(*_a, **_kw):
        raise OSError("disk full")

    monkeypatch.setattr(schema_mod, "find_repo_root", _boom)
    did = store._ensure_dataset("KOR", "risk/model")
    cur = store.connection.cursor()
    cur.execute("SELECT name FROM datasets WHERE id=?", (did,))
    assert cur.fetchone()[0] == DATASET_SENTINEL
