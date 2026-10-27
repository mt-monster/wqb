#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""把区域全量字段画像写入数据库（两层：数据集级 + 字段级）

表结构：
    dataset_profile     —— 每数据集 1 行（EUR 185 行）
    field_profile_full  —— 每字段 1 行（EUR 38,609 行）

数据源：
    data/wqb.db::datasets / fields / field_profile_perf / backtest_results
    tracking/EUR/reference/eur_dataset_catalog.json（仅 EUR：平台名称与描述）

用法：
    python tools/load_field_profiles_to_db.py            # 全量重建（EUR + EUR catalog）
    python tools/load_field_profiles_to_db.py --region EUR
    python tools/load_field_profiles_to_db.py --region USA --no-catalog
        # ⚠ 非 EUR 区域**必须加 --no-catalog**：CATALOG 是 EUR 的，
        #   USA 有 154/346 个同名数据集会被 EUR 的 coverage/alphaCount/valueScore 覆盖 ⇒ 选池失真。
"""
import os
import sys
import json
import sqlite3          # 仅用于 sqlite3.Row（连接本身一律走 db_connect）
import collections
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gen_eur_field_profiles import classify, infer_frequency, availability, COV_BUCKETS  # noqa: E402
from wqb.db_conn import connect as db_connect  # noqa: E402

DB = os.path.join(ROOT, "data", "wqb.db")
CATALOG = os.path.join(ROOT, "tracking", "EUR", "reference", "eur_dataset_catalog.json")

DDL_DATASET = """
CREATE TABLE IF NOT EXISTS dataset_profile (
    region              TEXT NOT NULL,
    dataset             TEXT NOT NULL,
    name                TEXT,
    category            TEXT,
    description         TEXT,
    coverage            REAL,
    field_count         INTEGER,
    alpha_count         INTEGER,
    value_score         REAL,
    pyramid_multiplier  REAL,
    delay               INTEGER,
    data_type           TEXT,
    n_fields            INTEGER,
    avg_field_coverage  REAL,
    min_field_coverage  REAL,
    max_field_coverage  REAL,
    freq_hint           TEXT,
    availability        TEXT,
    n_untested          INTEGER,
    n_alive             INTEGER,
    n_unusable          INTEGER,
    n_dead              INTEGER,
    n_axis_only         INTEGER,
    best_s_in_dataset   REAL,
    best_2y_in_dataset  REAL,
    n_backtests         INTEGER,
    n_ra_pass           INTEGER,
    n_dims              INTEGER,
    n_dims_bt           INTEGER,
    n_dims_static       INTEGER,
    dim_coverage_bt     REAL,
    dim_coverage_static REAL,
    updated_at          TEXT,
    PRIMARY KEY (region, dataset)
);
CREATE INDEX IF NOT EXISTS idx_dp_cat   ON dataset_profile(region, category);
CREATE INDEX IF NOT EXISTS idx_dp_alive ON dataset_profile(region, n_alive);
CREATE INDEX IF NOT EXISTS idx_dp_cov   ON dataset_profile(region, avg_field_coverage);
"""

DDL_FIELD = """
CREATE TABLE IF NOT EXISTS field_profile_full (
    region           TEXT NOT NULL,
    dataset          TEXT NOT NULL,
    category         TEXT,
    field_name       TEXT NOT NULL,
    field_type       TEXT,
    coverage         REAL,
    description      TEXT,
    semantic_family  TEXT,
    sem_type         TEXT,
    coverage_tier    TEXT,
    freq_hint        TEXT,
    n_tests          INTEGER DEFAULT 0,
    best_s           REAL,
    best_2y          REAL,
    best_sub         REAL,
    best_f           REAL,
    verdict          TEXT,
    skeleton_fams    TEXT,
    is_alive         INTEGER DEFAULT 0,
    is_untested      INTEGER DEFAULT 0,
    updated_at       TEXT,
    PRIMARY KEY (region, dataset, field_name)
);
CREATE INDEX IF NOT EXISTS idx_fpf_ds   ON field_profile_full(region, dataset);
CREATE INDEX IF NOT EXISTS idx_fpf_fam  ON field_profile_full(semantic_family);
CREATE INDEX IF NOT EXISTS idx_fpf_verd ON field_profile_full(verdict);
CREATE INDEX IF NOT EXISTS idx_fpf_bs   ON field_profile_full(best_s);
CREATE INDEX IF NOT EXISTS idx_fpf_cov  ON field_profile_full(coverage);
"""


def cov_tier(c):
    if c is None:
        return "未知"
    for label, lo, hi in COV_BUCKETS:
        if lo <= c < hi:
            return label
    return "未知"


def main():
    region = "EUR"
    catalog_path = CATALOG
    for i, a in enumerate(sys.argv):
        if a == "--region" and i + 1 < len(sys.argv):
            region = sys.argv[i + 1]
        if a == "--catalog" and i + 1 < len(sys.argv):
            catalog_path = sys.argv[i + 1]
        if a == "--no-catalog":
            catalog_path = None

    catalog = {}
    if catalog_path:
        if os.path.exists(catalog_path):
            with open(catalog_path, encoding="utf-8") as fh:
                catalog = json.load(fh)
        else:
            print(f"[catalog] 指定文件不存在，按无 catalog 处理：{catalog_path}")
    else:
        print("[catalog] 已禁用（--no-catalog）：name/description 留空、"
              "coverage/alphaCount/valueScore 取 data/wqb.db::datasets")

    # 写连接必须走规范工厂：WAL + busy_timeout=60s + foreign_keys，且 pytest 下会被
    # 生产库硬闸拦住（AGENTS.md §8.4 第 11 项）。
    con = db_connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(DDL_DATASET)
    con.executescript(DDL_FIELD)

    # 轻量迁移：补齐后加的列（幂等）
    def _ensure_cols(table, cols):
        have = {r[1] for r in con.execute(f"PRAGMA table_info({table})")}
        for cname, ctype in cols.items():
            if cname not in have:
                con.execute(f"ALTER TABLE {table} ADD COLUMN {cname} {ctype}")

    _ensure_cols("field_profile_full", {"sem_type": "TEXT"})
    _ensure_cols("dataset_profile", {
        "n_dims": "INTEGER", "n_dims_bt": "INTEGER", "n_dims_static": "INTEGER",
        "dim_coverage_bt": "REAL", "dim_coverage_static": "REAL",
    })
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ds_rows = list(con.execute(
        """SELECT d.id, d.name, d.category, d.coverage, d.alpha_count, d.value_score,
                  d.pyramid_multiplier, d.data_type, d.delay
           FROM datasets d JOIN regions r ON d.region_id = r.id
           WHERE r.name = ? ORDER BY d.name""", (region,)))

    # 回测聚合
    bt = {}
    for b in con.execute(
            """SELECT dataset,
                      COUNT(*) n,
                      SUM(CASE WHEN ra_failed_checks IS NULL OR ra_failed_checks=''
                                    OR ra_failed_checks='[]' THEN 1 ELSE 0 END) n_ra,
                      MAX(sharpe) best_s
               FROM backtest_results WHERE region=? GROUP BY dataset""", (region,)):
        bt[b["dataset"]] = dict(b)

    n_ds = n_fl = 0
    seen = set()
    for d in ds_rows:
        name = d["name"]
        if name in seen:
            continue
        seen.add(name)
        fields = list(con.execute(
            """SELECT f.field_name, f.field_type, f.coverage, f.description,
                      p.n_tests, p.best_s, p.best_2y, p.best_sub, p.best_f,
                      p.verdict, p.skeleton_fams, st.sem_type
               FROM fields f
               LEFT JOIN field_profile_perf p
                      ON p.region=? AND p.dataset=? AND p.field=f.field_name
               LEFT JOIN field_semantic_type st
                      ON st.region=? AND st.dataset=? AND st.field=f.field_name
               WHERE f.dataset_id=?
                 AND EXISTS (SELECT 1 FROM datasets dd JOIN regions gg ON gg.id = dd.region_id
                              WHERE dd.id = f.dataset_id AND gg.name = ?)""",
            (region, name, region, name, d["id"], region)))
        if not fields:
            continue

        covs = [f["coverage"] for f in fields if f["coverage"] is not None]
        avg_cov = sum(covs) / len(covs) if covs else 0.0
        verd = collections.Counter((f["verdict"] or "UNTESTED") for f in fields)
        bests = [f["best_s"] for f in fields if f["best_s"] is not None]
        best2 = [f["best_2y"] for f in fields if f["best_2y"] is not None]
        btr = bt.get(name, {})
        cat = catalog.get(name) or {}

        # 维度覆盖（族字段数 ≥3 才算一维；小集退回「整集=1维」）
        fams = collections.defaultdict(lambda: [0, 0, 0])  # fam -> [total, tested_bt, tested_static]
        for f in fields:
            fam = classify(f["field_name"], f["description"])
            fams[fam][0] += 1
            if (f["n_tests"] or 0) > 0:
                fams[fam][1] += 1
            if (f["verdict"] or "UNTESTED") != "UNTESTED":
                fams[fam][2] += 1
        big = {k: v for k, v in fams.items() if v[0] >= 3}
        if big:
            n_dims = len(big)
            n_dims_bt = sum(1 for v in big.values() if v[1] > 0)
            n_dims_st = sum(1 for v in big.values() if v[2] > 0)
        else:
            n_dims, n_dims_bt, n_dims_st = 1, (1 if any(v[1] > 0 for v in fams.values()) else 0),                                             (1 if any(v[2] > 0 for v in fams.values()) else 0)

        con.execute(
            """INSERT OR REPLACE INTO dataset_profile
               (region,dataset,name,category,description,coverage,field_count,alpha_count,
                value_score,pyramid_multiplier,delay,data_type,n_fields,avg_field_coverage,
                min_field_coverage,max_field_coverage,freq_hint,availability,n_untested,n_alive,
                n_unusable,n_dead,n_axis_only,best_s_in_dataset,best_2y_in_dataset,
                n_backtests,n_ra_pass,n_dims,n_dims_bt,n_dims_static,
                dim_coverage_bt,dim_coverage_static,updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (region, name, cat.get("name") or "", d["category"], (cat.get("description") or "")[:800],
             cat.get("coverage", d["coverage"]), cat.get("fieldCount", len(fields)),
             cat.get("alphaCount", d["alpha_count"]), cat.get("valueScore", d["value_score"]),
             cat.get("pyramidMultiplier", d["pyramid_multiplier"]), d["delay"], d["data_type"],
             len(fields), avg_cov, min(covs) if covs else None, max(covs) if covs else None,
             infer_frequency(fields[0]["field_type"] or "", fields[0]["description"] or "", fields[0]["field_name"]),
             availability(avg_cov, len(fields)),
             verd.get("UNTESTED", 0), verd.get("ALIVE", 0), verd.get("UNUSABLE", 0),
             verd.get("DEAD", 0) + verd.get("DEAD_STATIC", 0), verd.get("AXIS_ONLY", 0),
             max(bests) if bests else None, max(best2) if best2 else None,
             btr.get("n", 0), btr.get("n_ra", 0), n_dims, n_dims_bt, n_dims_st,
             round(n_dims_bt / n_dims, 4) if n_dims else None,
             round(n_dims_st / n_dims, 4) if n_dims else None, now))

        for f in fields:
            con.execute(
                """INSERT OR REPLACE INTO field_profile_full
                   (region,dataset,category,field_name,field_type,coverage,description,
                    semantic_family,sem_type,coverage_tier,freq_hint,n_tests,best_s,best_2y,best_sub,
                    best_f,verdict,skeleton_fams,is_alive,is_untested,updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (region, name, d["category"], f["field_name"], f["field_type"], f["coverage"],
                 (f["description"] or "")[:600],
                 classify(f["field_name"], f["description"]), f["sem_type"],
                 cov_tier(f["coverage"]), infer_frequency(f["field_type"] or "", f["description"] or "", f["field_name"]),
                 f["n_tests"] or 0, f["best_s"], f["best_2y"], f["best_sub"], f["best_f"],
                 f["verdict"] or "UNTESTED", f["skeleton_fams"],
                 1 if (f["verdict"] or "") == "ALIVE" else 0,
                 1 if (f["verdict"] or "UNTESTED") == "UNTESTED" else 0, now))
            n_fl += 1
        n_ds += 1

    con.commit()
    print(f"[load] region={region} datasets={n_ds} fields={n_fl}")
    for t in ("dataset_profile", "field_profile_full"):
        r = con.execute(f"SELECT COUNT(*) c FROM {t} WHERE region=?", (region,)).fetchone()
        print(f"  {t}: {r['c']} rows")
    con.close()


if __name__ == "__main__":
    main()
