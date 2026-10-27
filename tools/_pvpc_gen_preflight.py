# -*- coding: utf-8 -*-
"""生成 *_pre_close_2 子族的待校验表达式清单（供 preflight 用）。"""
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINDOWS = (126, 252)


def build():
    con = sqlite3.connect(os.path.join(ROOT, "data", "wqb.db")); con.execute("PRAGMA busy_timeout=30000")
    fs = [r[0] for r in con.execute(
        "select field from field_profile_perf where region='EUR' and dataset='intraday_pv_feats' "
        "and field like '%pre_close_2%' and coverage >= 0.6 order by field")]
    con.close()

    ex = []
    for w in WINDOWS:
        for f in fs:
            ex.append("ts_rank(ts_backfill(%s, 22), %d)" % (f, w))
    return fs, ex


def main():
    fs, ex = build()
    out = os.path.join(ROOT, "cache", "_pvpc_preflight.json")
    json.dump(ex, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    print("字段 %d 个，表达式 %d 条 -> %s" % (len(fs), len(ex), out))


if __name__ == "__main__":
    main()
