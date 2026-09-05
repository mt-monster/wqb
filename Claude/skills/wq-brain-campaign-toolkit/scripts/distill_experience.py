# -*- coding: utf-8 -*-
"""distill_experience.py - 经验蒸馏器（2026-09-01 落地，G1 学习闭环）。

对 registry_empirical 全量 win/dead_end 做模式归纳，产出三类可执行规则：
  1. 跨区死路铁律：同一 family 在 >=2 个区域判死 → 自动写入 cross_region_lessons
     （需 --apply 才落库；默认只报告）。
  2. 区域红灯族：同区同 family 死 >=3 次（或跨区铁律命中本区）→ 输出建议红灯族清单
     （写入 ledger_kv `distilled_red_families`，供 S0a 白名单筛选消费）。
  3. win 配方晋升建议：同一 family 在 >=2 区有 win，或单区 >=3 次 win →
     输出晋升为通用模板的候选（写入 ledger_kv `distilled_win_promotions`）。

设计原则：
  - 只归纳、不自动改 profile 文件（profile 是人工确认层，蒸馏器提建议）；
  - 幂等：cross_region_lessons 以 lesson_id 去重，重复跑无副作用；
  - 输出机器可读 JSON（--json）供 agent 消费，人读报告默认。
"""
import argparse
import json
import sqlite3
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import add_campaign_arg, CampaignContext

MIN_REGIONS_FOR_LESSON = 2   # 跨区铁律门槛
MIN_DEAD_FOR_RED = 3         # 区域红灯族门槛
MIN_WIN_FOR_PROMOTION = 3    # 晋升门槛（单区次数）或跨区 >=2 区


def _db_path(ctx):
    for root in _workspace_roots(ctx):
        p = os.path.join(root, "data", "wqb.db")
        if os.path.isfile(p):
            return p
    raise SystemExit("未找到 data/wqb.db（WQB_ROOT）")


def _workspace_roots(ctx):
    cdir = getattr(ctx, "dir", None)
    here = os.path.dirname(os.path.abspath(__file__))
    roots = []
    if cdir:
        roots.append(os.path.abspath(os.path.join(cdir, "..", "..")))
    roots.append(os.path.abspath(os.path.join(here, "..", "..", "..", "..", "..")))
    env = os.environ.get("WQB_ROOT")
    if env:
        roots.insert(0, env)
    return [r for r in roots if os.path.isfile(os.path.join(r, "data", "wqb.db"))]


def _norm_family(f):
    f = (f or "").strip().lower()
    if len(f) < 3:
        return None
    return f


def load_registry(db):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    wins, deads = [], []
    for r in con.execute(
        "SELECT region, entry_id, family, payload, dead_at FROM registry_empirical WHERE layer='win'"
    ):
        try:
            payload = json.loads(r["payload"]) if r["payload"] else {}
        except Exception:
            payload = {}
        wins.append({"region": r["region"], "family": _norm_family(r["family"]),
                     "entry_id": r["entry_id"], "payload": payload})
    for r in con.execute(
        "SELECT region, entry_id, family, payload, dead_at FROM registry_empirical WHERE layer='dead_end'"
    ):
        try:
            payload = json.loads(r["payload"]) if r["payload"] else {}
        except Exception:
            payload = {}
        deads.append({"region": r["region"], "family": _norm_family(r["family"]),
                      "entry_id": r["entry_id"], "payload": payload, "dead_at": r["dead_at"]})
    con.close()
    return wins, deads


def distill(wins, deads):
    """归纳三类规则。返回 dict：lessons / red_families / win_promotions。"""
    # ---- 1. 跨区死路铁律 ----
    dead_by_family = {}
    for d in deads:
        if d["family"]:
            dead_by_family.setdefault(d["family"], {}).setdefault(d["region"], []).append(d)
    lessons = []
    for fam, by_region in sorted(dead_by_family.items()):
        regions = sorted(by_region)
        if len(regions) >= MIN_REGIONS_FOR_LESSON:
            # 该 family 有没有任何 win（有 win 的不算死路铁律，只算风险族）
            win_regions = {w["region"] for w in wins if w["family"] == fam}
            severity = "hard" if not win_regions else "soft"
            lessons.append({
                "lesson_id": f"XREGION-DEAD-{fam.upper().replace(' ', '-')[:60]}",
                "family": fam,
                "regions": regions,
                "dead_count": sum(len(v) for v in by_region.values()),
                "win_regions": sorted(win_regions),
                "severity": severity,
                "finding": f"family '{fam}' 在 {len(regions)} 个区域判死（{', '.join(regions)}），"
                           f"共 {sum(len(v) for v in by_region.values())} 条死路"
                           + (f"；但 {sorted(win_regions)} 有 win" if win_regions else "，无任何区域 win"),
                "rule": f"新战役白名单排除 '{fam}' 族" if severity == "hard"
                        else f"'{fam}' 族仅在 win 区域复用配方，其他区避免首探",
            })

    # ---- 2. 区域红灯族 ----
    red_families = {}
    for fam, by_region in dead_by_family.items():
        for region, items in by_region.items():
            if len(items) >= MIN_DEAD_FOR_RED:
                red_families.setdefault(region, []).append({
                    "family": fam, "dead_count": len(items),
                    "dead_entries": [i["entry_id"] for i in items],
                    "cross_region_lesson": any(l["family"] == fam for l in lessons),
                })
    # 跨区铁律 hard 命中的区域也标红（未在本区死过也预防性标红）
    for l in lessons:
        if l["severity"] == "hard":
            for region in ALL_REGIONS:
                if region in l["regions"]:
                    continue
                lst = red_families.setdefault(region, [])
                if not any(x["family"] == l["family"] for x in lst):
                    lst.append({"family": l["family"], "dead_count": 0,
                                "dead_entries": [], "cross_region_lesson": True,
                                "note": "跨区铁律预防性标红（本区未实证）"})

    # ---- 3. win 配方晋升 ----
    win_by_family = {}
    for w in wins:
        if w["family"]:
            win_by_family.setdefault(w["family"], []).append(w)
    promotions = []
    for fam, items in sorted(win_by_family.items()):
        regions = sorted({w["region"] for w in items})
        if len(regions) >= MIN_REGIONS_FOR_LESSON or len(items) >= MIN_WIN_FOR_PROMOTION:
            # 提取共性 recipe 载荷
            keys = items[0]["payload"].keys() if items and isinstance(items[0]["payload"], dict) else []
            promotions.append({
                "family": fam, "win_count": len(items), "regions": regions,
                "entry_ids": [w["entry_id"] for w in items],
                "suggested_action": "晋升通用模板（template_kb）" if len(regions) >= 2
                                    else "区域强配方（region_kb win_recipes 置顶）",
                "common_payload_keys": sorted(keys),
            })
    return {"lessons": lessons, "red_families": red_families, "win_promotions": promotions}


ALL_REGIONS = ["USA", "EUR", "KOR", "IND", "ASI", "GBR", "HKG", "GLB", "CHN", "TWN", "MEA", "DEU"]


def apply_lessons(db, lessons):
    """写 cross_region_lessons（幂等，lesson_id 去重）。"""
    con = sqlite3.connect(db)
    n_new = 0
    for l in lessons:
        existing = con.execute(
            "SELECT id FROM cross_region_lessons WHERE lesson_id=?", (l["lesson_id"],)
        ).fetchone()
        if existing:
            con.execute(
                "UPDATE cross_region_lessons SET family=?, finding=?, rule=?, updated_at=? WHERE lesson_id=?",
                (l["family"], l["finding"], l["rule"], datetime.now().isoformat(timespec="seconds"),
                 l["lesson_id"]),
            )
            continue
        con.execute(
            "INSERT INTO cross_region_lessons (lesson_id, family, finding, rule, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?)",
            (l["lesson_id"], l["family"], l["finding"], l["rule"],
             datetime.now().isoformat(timespec="seconds"),
             datetime.now().isoformat(timespec="seconds")),
        )
        n_new += 1
    con.commit()
    con.close()
    return n_new


def write_ledger(ctx, db, key, value):
    """写入 ledger_kv（蒸馏结论的机器可读缓存，S0a/选波消费）。"""
    con = sqlite3.connect(db)
    now = datetime.now().isoformat(timespec="seconds")
    con.execute(
        "INSERT OR REPLACE INTO ledger_kv (region, key, value, updated_at) VALUES (?,?,?,?)",
        ("GLOBAL", key, json.dumps(value, ensure_ascii=False), now),
    )
    con.commit()
    con.close()


def main():
    ap = argparse.ArgumentParser(description="经验蒸馏器：registry win/dead 模式归纳 → 跨区铁律/红灯族/模板晋升")
    add_campaign_arg(ap)
    ap.add_argument("--apply", action="store_true",
                    help="落库（cross_region_lessons + ledger_kv 蒸馏缓存）；缺省只报告")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    db = _db_path(ctx)

    wins, deads = load_registry(db)
    out = distill(wins, deads)
    out["stats"] = {"wins_total": len(wins), "deads_total": len(deads),
                    "lessons": len(out["lessons"]),
                    "red_regions": {k: len(v) for k, v in out["red_families"].items()},
                    "promotions": len(out["win_promotions"])}

    if a.apply:
        n_new = apply_lessons(db, out["lessons"])
        write_ledger(ctx, db, "distilled_red_families", out["red_families"])
        write_ledger(ctx, db, "distilled_win_promotions", out["win_promotions"])
        write_ledger(ctx, db, "distilled_at", {"at": datetime.now().isoformat(timespec="seconds"),
                                               "new_lessons": n_new})
        out["applied"] = {"new_lessons": n_new}

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return
    print(f"[distill] wins={len(wins)} deads={len(deads)}")
    print(f"[distill] 跨区死路铁律 {len(out['lessons'])} 条:")
    for l in out["lessons"]:
        print(f"  {l['lesson_id']} [{l['severity']}] {l['finding']}")
    print(f"[distill] 区域红灯族（供 S0a 白名单排除参考）:")
    for region, fams in sorted(out["red_families"].items()):
        print(f"  {region}: " + ", ".join(f"{x['family']}({x['dead_count']}死)" for x in fams))
    print(f"[distill] win 晋升候选 {len(out['win_promotions'])} 个:")
    for p in out["win_promotions"]:
        print(f"  {p['family']}: {p['win_count']} win in {p['regions']} → {p['suggested_action']}")
    if a.apply:
        print(f"[distill] 已落库：新铁律 {out['applied']['new_lessons']} 条 + 蒸馏缓存 3 键（GLOBAL 桶）")
    else:
        print("[distill] dry 模式：加 --apply 落库（cross_region_lessons 幂等 + ledger_kv GLOBAL 桶）")


if __name__ == "__main__":
    main()
