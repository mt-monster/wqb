# -*- coding: utf-8 -*-
"""gradient_gate（梯度回测完备性闸）守护测试。

2026-11-21 用户指令「把梯度回测嵌入到回测的流程中必做」的机械守卫。
判据：① 骨架厚度 ≥ min_variants；② 梯度档案 `## Layer N` 成型层数 ≥ min_layers；
③ Δ 表档案存在（可关）；关档案时层数回退为骨架多样性近似。
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "tools" / "gates"))
import gradient_gate as gg  # noqa: E402

_LAYER0 = """## Layer 0（参考）

| 臂 | S | 2Y |
|---|---|---|
| a | 1.0 | 1.0 |
| b | 1.1 | 1.1 |
| c | 1.2 | 1.2 |
| d | 1.3 | 1.3 |
"""

_LAYER1 = """## Layer 1（内核）

| 臂 | S | 2Y |
|---|---|---|
| a | 1.4 | 1.4 |
| b | 1.5 | 1.5 |
| c | 1.6 | 1.6 |
| d | 1.7 | 1.7 |
"""


def _make_db(tmp_path: Path, rows) -> Path:
    db = tmp_path / "wqb.db"
    con = sqlite3.connect(db)
    con.execute(
        "create table expressions (id integer primary key, region text, dataset text,"
        " expression text, skeleton text, sharpe real)"
    )
    con.executemany(
        "insert into expressions (region, dataset, expression, skeleton, sharpe) values (?,?,?,?,?)",
        rows,
    )
    con.commit()
    con.close()
    return db


def _thick_rows(dataset: str = "ds", region: str = "TST"):
    rows = [(region, dataset, f"rank(ts_mean(F,{10+i}))", "rank(ts_mean(F,N))", 1.0) for i in range(5)]
    rows += [(region, dataset, f"group_rank(F, sector{i})", "group_rank(F,F)", 1.0) for i in range(2)]
    return rows


def _wave_archive(root: Path, region: str, dataset: str, body: str) -> None:
    d = root / region / "waves"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"wave1_gradient_{dataset}.md").write_text("# Δ table\n\n" + body, encoding="utf-8")


def test_done_when_thickness_layers_archive_present(tmp_path, capsys):
    db = _make_db(tmp_path, _thick_rows("ds_a"))
    root = tmp_path / "tracking"
    _wave_archive(root, "TST", "ds_a", _LAYER0 + "\n" + _LAYER1)
    rc = gg.main(["--region", "TST", "--dataset", "ds_a", "--db", str(db),
                  "--archive-root", str(root), "--json"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out[0]["verdict"] == "GRADIENT_DONE"
    assert out[0]["dominant_skeleton_variants"] == 5
    assert out[0]["archive_layers"] == 2


def test_partial_when_only_one_layer_filled(tmp_path):
    """Layer 1 只有表头与「待收」占位 ⇒ 未完成层不计。"""
    body = (_LAYER0 + "\n## Layer 1（内核）\n\n| 臂 | S | 2Y |\n|---|---|---|\n"
            "| a | 待收 | |\n| b | 待收 | |\n| c | 待收 | |\n")
    db = _make_db(tmp_path, _thick_rows("ds_e"))
    root = tmp_path / "tracking"
    _wave_archive(root, "TST", "ds_e", body)
    rc = gg.main(["--region", "TST", "--dataset", "ds_e", "--db", str(db),
                  "--archive-root", str(root)])
    assert rc == 2


def test_missing_when_single_point_retries_only(tmp_path):
    # 每个骨架只有 1 条 = 单点试错，不算梯度
    rows = [("TST", "ds_b", f"rank(ts_mean(F,{10+i}))", f"skeleton_{i}", 1.0) for i in range(6)]
    db = _make_db(tmp_path, rows)
    rc = gg.main(["--region", "TST", "--dataset", "ds_b", "--db", str(db),
                  "--archive-root", str(tmp_path / "tracking")])
    assert rc == 2


def test_partial_when_thick_but_no_archive(tmp_path):
    db = _make_db(tmp_path, _thick_rows("ds_c"))
    rc = gg.main(["--region", "TST", "--dataset", "ds_c", "--db", str(db),
                  "--archive-root", str(tmp_path / "no_such_root")])
    assert rc == 2


def test_archive_off_allows_done(tmp_path):
    db = _make_db(tmp_path, _thick_rows("ds_d"))
    rc = gg.main(["--region", "TST", "--dataset", "ds_d", "--db", str(db),
                  "--archive-root", str(tmp_path / "no_such_root"),
                  "--require-archive", "off"])
    assert rc == 0


def test_field_prefix_fallback(tmp_path):
    # dataset 列空、靠 field-prefix 命中
    rows = [("TST", None, f"rank(ts_mean(inst1_price,{10+i}))", "rank(ts_mean(F,N))", 1.0) for i in range(4)]
    rows += [("TST", None, "group_rank(inst1_price, sector)", "group_rank(F,F)", 1.0)] * 2
    db = _make_db(tmp_path, rows)
    root = tmp_path / "tracking"
    _wave_archive(root, "TST", "institutions1", _LAYER0 + "\n" + _LAYER1)
    rc = gg.main(["--region", "TST", "--dataset", "institutions1", "--field-prefix", "inst1_",
                  "--db", str(db), "--archive-root", str(root), "--json"])
    assert rc == 0