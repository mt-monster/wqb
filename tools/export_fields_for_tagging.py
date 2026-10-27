"""export_fields_for_tagging.py — 导出待 LLM 打标的字段清单（2026-10-23）

背景：正则分类器（field_form）只能抓强模式，遇到语义含糊的字段会退回 other（全交叉）。
LLM 读 description 能判断「这个字段本质是变化量还是水平量」，但流水线是离线常驻进程，不能调 API。
方案：**离线打标 + 文件集成**
  1) 本脚本导出待打标字段（默认只导正则判为 other 的「含糊字段」，LLM 的边际价值最高）；
  2) LLM（会话内）读清单，产出 cache/field_form_llm.json；
  3) 流水线 field_form() 按 overrides > LLM(conf≥0.7) > 正则 > other 取值，按 mtime 热加载。

用法：
    python tools/export_fields_for_tagging.py --priority-cats SENTIMENT,NEWS,EARNINGS --min-cov 0.5
    python tools/export_fields_for_tagging.py --datasets news20,macro27 --all   # 不筛含糊，全导
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "wqb.db")
OUT = os.path.join(ROOT, "cache", "fields_to_tag.json")
TAGFILE = os.path.join(ROOT, "cache", "field_form_llm.json")

sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from wqb.db_conn import connect as db_connect  # noqa: E402
import full_template_campaign as F  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--datasets", default=None, help="逗号分隔；默认全部")
    ap.add_argument("--priority-cats", default=None)
    ap.add_argument("--min-cov", type=float, default=0.5)
    ap.add_argument("--all", action="store_true", help="导出全部字段（默认只导正则判含糊的）")
    ap.add_argument("--hide-done", action="store_true", help="跳过已完成的集（checkpoint）")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    con = db_connect(DB, readonly=True)
    con.row_factory = sqlite3.Row
    cats = [c.strip().upper() for c in (args.priority_cats or "").split(",") if c.strip()]
    want_ds = [d.strip() for d in (args.datasets or "").split(",") if d.strip()]

    done = set()
    if args.hide_done:
        try:
            done = set(json.load(open(os.path.join(ROOT, "results",
                                                   "full_template_campaign_checkpoint.json"),
                                      encoding="utf-8")).get("done") or [])
        except Exception:
            pass

    q = """SELECT d.name ds, COALESCE(d.category,'') cat, f.field_name, f.field_type,
                  f.coverage, COALESCE(f.description,'') descr
           FROM fields f JOIN datasets d ON f.dataset_id=d.id
           JOIN regions r ON d.region_id=r.id
           WHERE r.name=? AND f.coverage>=? AND f.field_type!='GROUP'
           ORDER BY d.name, f.coverage DESC"""
    rows = [dict(x) for x in con.execute(q, (args.region, args.min_cov))]

    try:
        tagged = set(json.load(open(TAGFILE, encoding="utf-8")).keys())
    except Exception:
        tagged = set()

    out = []
    for r in rows:
        if want_ds and r["ds"] not in want_ds:
            continue
        if cats and (r["cat"] or "").upper() not in cats:
            continue
        if args.hide_done and r["ds"] in done:
            continue
        key = f"{r['ds']}.{r['field_name']}"
        if key in tagged:
            continue
        form = F.field_form(r, r["ds"])
        if not args.all and form != "other":
            continue                       # 正则已能判的，不再麻烦 LLM
        out.append({"key": key, "dataset": r["ds"], "category": r["cat"],
                    "field": r["field_name"], "type": r["field_type"],
                    "coverage": round(r["coverage"] or 0, 3),
                    "regex_form": form, "desc": re.sub(r"\s+", " ", r["descr"])[:300]})

    if args.limit:
        out = out[: args.limit]
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"导出 {len(out)} 个待打标字段 → {OUT}")
    print(f"（已打标 {len(tagged)} 个，其中本批跳过；覆盖 {len({o['dataset'] for o in out})} 个数据集）")
    for o in out[:8]:
        print(f"  {o['key']:52s} [{o['category']:12s}] {o['desc'][:70]}")


if __name__ == "__main__":
    main()
