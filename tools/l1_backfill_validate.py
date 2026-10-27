# -*- coding: utf-8 -*-
"""l1_backfill_validate.py — 补测批字段名校验（本地，零平台调用）

配合 cache/_l1_backfill.json（[{"ds","tpl","e"}]）使用：
过滤掉字段名不存在于本地库的表达式，避免 unknown variable 连坐整批。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = os.path.join(ROOT, "cache", "_l1_backfill.json")
DB = os.path.join(ROOT, "data", "wqb.db")

# 连接一律走规范工厂（WAL + busy_timeout=60s + foreign_keys），见 AGENTS.md §8.4 第 11 项。
# 本脚本只读，readonly=True 可跳过会改写库文件字节的 journal_mode=WAL。
sys.path.insert(0, os.path.join(ROOT, "src"))
from wqb.db_conn import connect as db_connect  # noqa: E402

_SKIP_PREFIX = ("ts_", "vec_", "group_", "if_", "tail", "bucket", "trade_", "signed_",
                "reverse", "quantile", "winsorize", "hump", "vector_", "regression_")
_SKIP_WORDS = {"rank", "add", "multiply", "divide", "subtract", "greater", "less", "and",
               "or", "not", "abs", "log", "exp", "sign", "min", "max", "sum", "std", "mean",
               "count", "scale", "power", "backfill", "delta", "decay", "ir", "zscore"}


def main():
    rows = json.load(open(BATCH, encoding="utf-8"))
    con = db_connect(DB, readonly=True)
    valid = {r[0] for r in con.execute(
        "SELECT f.field_name FROM fields f JOIN datasets d ON f.dataset_id=d.id "
        "JOIN regions g ON d.region_id=g.id WHERE g.name='EUR'")}
    ok, bad = [], []
    for x in rows:
        ids = set(re.findall(r"(?<![a-z_])([a-z][a-z0-9_]*(?:_[a-z0-9]+){1,})(?![a-z0-9_]*\()",
                             x["e"]))
        ids = {i for i in ids
               if not i.startswith(_SKIP_PREFIX) and i not in _SKIP_WORDS}
        miss = [i for i in ids if i not in valid]
        (bad if miss else ok).append((x, miss))
    print(f"字段名校验: 通过 {len(ok)} / 失败 {len(bad)}")
    for x, m in bad[:8]:
        print(f"  x {x['ds']}: 缺 {m[:3]}")
    json.dump([x for x, _ in ok], open(BATCH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"已更新 {BATCH}（{len(ok)} 条）")
    for x, _ in ok[:5]:
        print(f"  [{x['ds']}/{x['tpl']}] {x['e'][:110]}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
