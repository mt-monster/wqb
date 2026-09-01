# -*- coding: utf-8 -*-
"""neut_cache.py - 中性化×数据集缓存表（P1-1，2026-08-31）。

背景：同一数据集在不同中性化下的表现差异大（model135 REVERSION_AND_MOMENTUM 下 0.876
vs 均值 0.437）。每次新区域战役强制先跑 webdata_quality.py 读区域级中性化排名后，
把 (数据集×中性化) → 历史最佳 sharpe 沉淀到本地 SQLite 缓存，发批前查表选最优 2-3 个，
而非每波重新扫全 11 种。

数据源：WebDataScope 数据包 neutralization.dataset[<ds>][<NEUT>] = {count, sharpe_ratio, ...}
缓存：data/wqb.db 的 neut_cache 表（单轨 DB 模式，与 registry_empirical 同库）。

用法:
  # 从 WebDataScope 数据包回填缓存（每区域战役启动时跑一次）
  python tools/neut_cache.py --rebuild --region USA --delay 1 \
      --zip WebData_20260219_V0.10.9.zip

  # 发批前查表：某数据集最优 3 个中性化
  python tools/neut_cache.py --region USA --delay 1 --dataset model135 --top 3

  # dry-run：只打印不写库
  python tools/neut_cache.py --rebuild --region USA --delay 1 --zip <zip> --dry-run
"""
import argparse
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "wqb.db")

_DDL = """
CREATE TABLE IF NOT EXISTS neut_cache (
    region TEXT NOT NULL,
    delay INTEGER NOT NULL,
    dataset TEXT NOT NULL,
    neutralization TEXT NOT NULL,
    sharpe_ratio REAL,
    count INTEGER,
    osis_count INTEGER,
    fitness_ratio REAL,
    source TEXT,
    updated_at TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (region, delay, dataset, neutralization)
);
"""


def _conn(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(_DDL)
    return conn


def rebuild(region, delay, zip_path, dry_run=False, db_path=DB_PATH):
    """从 WebDataScope 数据包回填 (region, delay) 全量 数据集×中性化 缓存。"""
    import zipfile
    from webdata_quality import load_bin  # 复用现有 msgpack 解压
    with zipfile.ZipFile(zip_path) as zf:
        info = load_bin(zf, 'data/oth/info_data.bin')
    key = f"{region}_{delay}"
    if key not in info:
        print(f"[neut_cache] 数据包中无 {key} 区域数据，可用键: {sorted(info.keys())[:10]}")
        return 0
    neut = info[key].get("neutralization", {})
    ds_table = neut.get("dataset", {})
    rows = []
    for ds, neut_map in ds_table.items():
        for neut_name, stats in neut_map.items():
            rows.append((
                region, delay, ds, neut_name,
                stats.get("sharpe_ratio"), stats.get("count"),
                stats.get("osis_count"), stats.get("fitness_ratio"),
                os.path.basename(zip_path),
            ))
    if dry_run:
        print(f"[neut_cache][dry-run] {key} 将写入 {len(rows)} 行（{len(ds_table)} 数据集）")
        # 打印每个数据集最优中性化预览
        best = {}
        for r in rows:
            ds = r[2]
            if ds not in best or (r[4] or 0) > (best[ds][4] or 0):
                best[ds] = r
        for ds, r in sorted(best.items())[:10]:
            print(f"  {ds}: 最优 {r[3]} sharpe={r[4]}")
        return len(rows)
    conn = _conn(db_path)
    try:
        conn.executemany(
            "INSERT OR REPLACE INTO neut_cache "
            "(region, delay, dataset, neutralization, sharpe_ratio, count, osis_count, fitness_ratio, source) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            rows,
        )
        conn.commit()
        print(f"[neut_cache] {key} 写入 {len(rows)} 行（{len(ds_table)} 数据集）-> {db_path}")
    finally:
        conn.close()
    return len(rows)


def query_top(region, delay, dataset, top=3, db_path=DB_PATH):
    """发批前查表：某数据集最优 top 个中性化（按 sharpe_ratio 降序）。"""
    conn = _conn(db_path)
    try:
        cur = conn.execute(
            "SELECT neutralization, sharpe_ratio, count, osis_count, fitness_ratio "
            "FROM neut_cache WHERE region=? AND delay=? AND dataset=? "
            "ORDER BY COALESCE(sharpe_ratio, -999) DESC LIMIT ?",
            (region, delay, dataset, top),
        )
        rows = cur.fetchall()
    finally:
        conn.close()
    if not rows:
        print(f"[neut_cache] 无缓存：{region}_{delay}/{dataset}（先 --rebuild 回填）")
        return []
    print(f"[neut_cache] {region}_{delay}/{dataset} 最优 {len(rows)} 个中性化：")
    out = []
    for i, (neut, sh, cnt, osis, fit) in enumerate(rows, 1):
        print(f"  {i}. {neut}: sharpe={sh} count={cnt} osis={osis} fitness={fit}")
        out.append({"neutralization": neut, "sharpe_ratio": sh, "count": cnt,
                    "osis_count": osis, "fitness_ratio": fit})
    return out


def main():
    ap = argparse.ArgumentParser(description="中性化×数据集缓存表（P1-1）")
    ap.add_argument("--rebuild", action="store_true", help="从 WebDataScope 数据包回填缓存")
    ap.add_argument("--region", required=True, help="区域（如 USA）")
    ap.add_argument("--delay", type=int, default=1, help="延迟（默认 1）")
    ap.add_argument("--zip", dest="zip_path", default=None, help="WebDataScope 数据包路径（--rebuild 必需）")
    ap.add_argument("--dataset", default=None, help="查表：数据集 id")
    ap.add_argument("--top", type=int, default=3, help="查表：返回最优 top 个（默认 3）")
    ap.add_argument("--db", default=DB_PATH, help=f"SQLite 路径（默认 {DB_PATH}）")
    ap.add_argument("--dry-run", action="store_true", help="只打印不写库")
    a = ap.parse_args()

    if a.rebuild:
        if not a.zip_path:
            ap.error("--rebuild 需要 --zip 指定 WebDataScope 数据包路径")
        rebuild(a.region, a.delay, a.zip_path, dry_run=a.dry_run, db_path=a.db)
    elif a.dataset:
        query_top(a.region, a.delay, a.dataset, top=a.top, db_path=a.db)
    else:
        ap.error("需要 --rebuild（回填）或 --dataset（查表）")


if __name__ == "__main__":
    main()
