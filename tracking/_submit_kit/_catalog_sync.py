# -*- coding: utf-8 -*-
"""本地 datasets 目录修复：从平台 /data-sets 全量同步（权威）。

修复内容：
  1) IND/EUR 等区域 category 全 NULL → 用平台类别回填；
  2) KOR 18/192、ASI 0/163 等数据集缺失 → 补插；
  3) datasets 表加 delay 列（本地原本没有，无法区分 D0/D1 数据集）。
附带：用平台目录 + PV 命名归一，输出修正后的点塔全集。
安全：动手前 sqlite3 backup API 备份。
"""
import asyncio
import json
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

WQ_ROOT = Path(r"D:\coding\traeCN_project\wqb")
sys.path.insert(0, str(WQ_ROOT / "world-quant-brain-mcp"))
DB = WQ_ROOT / "data" / "wqb.db"
OUT_CACHE = WQ_ROOT / "research-data" / "platform_catalog_20260901.json"

UNIVERSE_CANDIDATES = {
    "USA": ["TOP3000"], "KOR": ["TOP600"], "ASI": ["TOP2000", "TOP1000", "TOP500"],
    "MEA": ["TOP400", "TOP300"], "IND": ["TOP500"],
    "EUR": ["TOP2500", "TOP1200", "TOP400"], "GBR": ["TOP700"],
    "GLB": ["TOP3000", "MINVOL1M", "TOP2000"], "HKG": ["TOP500", "TOP800"],
    "DEU": ["TOP500", "TOP300"],
}
REGIONS = list(UNIVERSE_CANDIDATES)
PAGE_SLEEP, COMBO_SLEEP, MAX_PAGES = 1.0, 2.0, 15

# 平台目录类别名 → 金字塔塔名（pyramids[].name 实测口径）
CAT_NORM = {"PRICE VOLUME": "PV", "SHORT INTEREST": "SHORTINTEREST",
            "SOCIAL MEDIA": "SOCIALMEDIA"}


def norm_cat(c):
    c = (c or "").strip().upper()
    return CAT_NORM.get(c, c)


async def fetch_page_all(brain, region, universe, delay):
    """拉该 region+delay(+universe) 的全部数据集（精简字段）。"""
    rows, offset, pages = [], 0, 0
    while pages < MAX_PAGES:
        for attempt in range(4):
            try:
                r = await brain._request(
                    "GET", f"{brain.base_url}/data-sets",
                    params={"region": region, "universe": universe, "delay": delay,
                            "limit": 50, "offset": offset, "theme": "false"})
                if r.status_code == 429:
                    await asyncio.sleep(8)
                    continue
                if r.status_code != 200:
                    return None, f"HTTP {r.status_code}"
                j = r.json()
                break
            except Exception as e:
                if attempt == 3:
                    return None, f"ERR {type(e).__name__}: {str(e)[:60]}"
                await asyncio.sleep(5)
        res = j.get("results") or []
        for d in res:
            cat = d.get("category")
            rows.append({
                "id": d.get("id"), "name": d.get("name"),
                "category": norm_cat(cat.get("name") if isinstance(cat, dict) else cat),
                "subcategory": (d.get("subcategory") or {}).get("name"),
                "field_count": d.get("fieldCount"), "alpha_count": d.get("alphaCount"),
                "coverage": d.get("coverage"), "value_score": d.get("valueScore"),
                "pyramid_multiplier": d.get("pyramidMultiplier"),
                "delay": d.get("delay"), "universe": d.get("universe"),
                "date_updated": d.get("dateUpdated"),
            })
        total = j.get("count")
        if len(res) < 50 or (total is not None and offset + len(res) >= int(total)):
            break
        offset += 50
        pages += 1
        await asyncio.sleep(PAGE_SLEEP)
    return rows, None


def pyr_names(a):
    return [p.get("name") for p in (a.get("pyramids") or []) if p.get("name")]


async def fetch_active(brain):
    out, offset = [], 0
    while True:
        r = await brain._request(
            "GET", f"{brain.base_url}/users/self/alphas",
            params={"status": "ACTIVE", "limit": 100, "offset": offset})
        arr = r.json().get("results") or []
        out.extend(arr)
        if len(arr) < 100 or offset > 5000:
            break
        offset += 100
    return out


def db_backup():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = WQ_ROOT / "data" / f"wqb.db.bak_catalog_{ts}"
    src = sqlite3.connect(str(DB))
    dst = sqlite3.connect(str(bak))
    src.backup(dst)
    dst.close()
    src.close()
    return bak


async def main():
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    # ---------- 1) 拉平台目录 ----------
    catalog = {}
    print("=== 拉取平台数据集目录 ===")
    for rg in REGIONS:
        catalog[rg] = {}
        for delay in (1, 0):
            rows, err, used = None, None, None
            for uni in UNIVERSE_CANDIDATES[rg]:
                rows, err = await fetch_page_all(brain, rg, uni, delay)
                if rows:                 # 非空才算命中；空集换下一个 universe
                    used = uni
                    break
            n = len(rows) if rows else 0
            print(f"  {rg:4s} D{delay}: {n:>4} 个数据集 (uni={used})"
                  + ("" if rows is not None else f"  [失败 {err}]"))
            if rows is not None:
                catalog[rg][str(delay)] = rows
            await asyncio.sleep(COMBO_SLEEP)
    OUT_CACHE.write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
    n_all = sum(len(v) for rg in catalog for v in rg and catalog[rg].values())
    print(f"[cache] {OUT_CACHE}  (数据集 {n_all} 条)")

    # ---------- 2) 修 DB ----------
    con = sqlite3.connect(str(DB))
    cur = con.cursor()
    cur.execute("SELECT id, name FROM regions")
    rid = {n: i for i, n in cur.fetchall()}
    cur.execute("PRAGMA table_info(datasets)")
    cols = [c[1] for c in cur.fetchall()]
    if "delay" not in cols:
        cur.execute("ALTER TABLE datasets ADD COLUMN delay INTEGER")
        print("[schema] datasets 加列 delay")
    cur.execute("SELECT status, COUNT(*) FROM datasets GROUP BY status")
    st = cur.fetchall()
    default_status = max(st, key=lambda x: x[1])[0] if st else "active"

    # 同步前快照
    cur.execute("SELECT r.name, COUNT(*), SUM(CASE WHEN d.category IS NULL THEN 1 ELSE 0 END) "
                "FROM datasets d LEFT JOIN regions r ON r.id=d.region_id GROUP BY r.name")
    before = {a: (b, c) for a, b, c in cur.fetchall()}

    bak = db_backup()
    print(f"[backup] {bak}")

    upd, ins, skip_d0, filled_cat = 0, 0, 0, 0
    for rg, by_delay in catalog.items():
        r_id = rid.get(rg)
        if r_id is None:
            continue
        for delay_key in ("1", "0"):          # 先 D1 后 D0，同名以 D1 为准
            for d in by_delay.get(delay_key, []) or []:
                if not d.get("id"):
                    continue
                cur.execute("SELECT id, category FROM datasets WHERE region_id=? AND name=?",
                            (r_id, d["id"]))
                row = cur.fetchone()
                if row:
                    if row[1] is None and d.get("category"):
                        filled_cat += 1
                    cur.execute(
                        "UPDATE datasets SET category=?, field_count=?, coverage=?, "
                        "alpha_count=?, value_score=?, pyramid_multiplier=?, "
                        "updated_at=?, delay=COALESCE(delay,?) WHERE id=?",
                        (d.get("category"), d.get("field_count"), d.get("coverage"),
                         d.get("alpha_count"), d.get("value_score"),
                         d.get("pyramid_multiplier"),
                         datetime.now().isoformat(timespec="seconds"),
                         int(delay_key), row[0]))
                    upd += 1
                else:
                    if delay_key == "0":
                        skip_d0 += 1     # D0 独有数据集也入库（带 delay=0）
                    cur.execute(
                        "INSERT INTO datasets (name, region_id, category, field_count, "
                        "coverage, alpha_count, value_score, pyramid_multiplier, status, "
                        "created_at, updated_at, delay) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        (d["id"], r_id, d.get("category"), d.get("field_count"),
                         d.get("coverage"), d.get("alpha_count"), d.get("value_score"),
                         d.get("pyramid_multiplier"), default_status,
                         datetime.now().isoformat(timespec="seconds"),
                         datetime.now().isoformat(timespec="seconds"), int(delay_key)))
                    ins += 1
    con.commit()

    # ---------- 3) 校验 ----------
    cur.execute("SELECT r.name, COUNT(*), SUM(CASE WHEN d.category IS NULL THEN 1 ELSE 0 END) "
                "FROM datasets d LEFT JOIN regions r ON r.id=d.region_id GROUP BY r.name")
    after = {a: (b, c) for a, b, c in cur.fetchall()}
    print(f"\n[sync] 更新 {upd} / 插入 {ins} / 回填 NULL 类别 {filled_cat}")
    print(f"{'区域':<6}{'数据集 前→后':>16}{'NULL类别 前→后':>18}")
    for rg in REGIONS:
        b, a = before.get(rg, (0, 0)), after.get(rg, (0, 0))
        print(f"{rg:<6}{b[0]:>7}→{a[0]:<7}{b[1]:>9}→{a[1]:<8}")
    con.close()

    # ---------- 4) 修正后的点塔全集 ----------
    # ★ 点亮口径（用户 2026-09-01 定义）：该 catalog 下 ACTIVE ≥3 颗才算点亮。
    MIN_LIT = 3
    active = await fetch_active(brain)
    lit_cnt = defaultdict(int)
    for x in active:
        for nm in pyr_names(x):
            lit_cnt[nm] += 1
    lit = {nm for nm, n in lit_cnt.items() if n >= MIN_LIT}
    print(f"\n=== 修正后点塔全集（平台目录，类别名已归一；点亮=每塔≥{MIN_LIT} 颗 ACTIVE）===")
    print(f"{'区域':<6}{'全集':>5}{'已亮':>5}{'未亮':>5}")
    tp = tl = tu = 0
    unlit_by = {}
    for rg in REGIONS:
        poss = set()
        for dk, rows in catalog.get(rg, {}).items():
            for d in rows or []:
                if d.get("category"):
                    poss.add(f"{rg}/D{dk}/{d['category']}")
        L = {t for t in poss if t in lit}
        U = sorted(poss - L)
        unlit_by[rg] = U
        tp += len(poss); tl += len(L); tu += len(U)
        print(f"{rg:<6}{len(poss):>5}{len(L):>5}{len(U):>5}   未亮: "
              + ", ".join(t.split('/', 1)[1] for t in U))
    print(f"{'合计':<6}{tp:>5}{tl:>5}{tu:>5}")
    out2 = WQ_ROOT / "research-data" / "tower_universe_corrected_20260901.json"
    out2.write_text(json.dumps({"min_lit": MIN_LIT, "lit_counts": dict(lit_cnt),
                                "lit": sorted(lit), "unlit": unlit_by,
                                "totals": {"possible": tp, "lit": tl, "unlit": tu}},
                               ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[saved] {out2}")


if __name__ == "__main__":
    asyncio.run(main())
