"""KOR D1 wave4 (price_signal_dl) 证据评审"""
import json

SRC = r"C:\Users\MENGTAO\.qoder-cn\cache\projects\wqb-a40170ec\agent-tools\task-4d7\ae1dbe2d.txt"
OUT = r"D:\coding\traeCN_project\wqb\tracking\KOR\reviews\kor_wave4_review.json"

WAVE3_IDS = {
    "pwNGoV9v", "d5Zzgn2g", "JjGzYnVW", "RRmzqNRa", "N1bzqn18", "QPGzqnZQ", "XgozPkG5", "RRmzqNMb",
}

data = json.load(open(SRC, encoding="utf-8"))
rows = []
for a in data["results"]:
    if a["id"] not in WAVE3_IDS:
        continue
    m = a.get("metrics", {})
    ra = a.get("ra", {})
    rows.append({
        "id": a["id"],
        "code": a["code"],
        "neutralization": a.get("settings", {}).get("neutralization"),
        "sharpe": m.get("sharpe"),
        "fitness": m.get("fitness"),
        "two_year_sharpe": m.get("two_year_sharpe"),
        "margin": m.get("margin"),
        "turnover": m.get("turnover"),
        "risk_neutralized_sharpe": m.get("risk_neutralized_sharpe"),
        "ra_failed": ra.get("ra_failed"),
        "failed_ra_count": ra.get("failed_ra_count"),
        "ra_failed_checks": ra.get("ra_failed_checks", []),
    })

print(f"wave3 alphas found: {len(rows)}/{len(WAVE3_IDS)}")
rows.sort(key=lambda r: (r["sharpe"] is None, -(r["sharpe"] or -99)))

print(f"\n{'id':9s} {'neut':11s} {'sharpe':>7s} {'fit':>6s} {'2y':>6s} {'margin':>10s} {'tvr':>7s} {'rn_sh':>6s} ra_failed_checks")
for r in rows:
    mg = f"{r['margin']*10000:.1f}bp" if r["margin"] is not None else "NA"
    tv = f"{r['turnover']*100:.1f}%" if r["turnover"] is not None else "NA"
    sh = f"{r['sharpe']:.2f}" if r["sharpe"] is not None else "NA"
    ft = f"{r['fitness']:.2f}" if r["fitness"] is not None else "NA"
    ty = f"{r['two_year_sharpe']:.2f}" if r["two_year_sharpe"] is not None else "NA"
    rn = f"{r['risk_neutralized_sharpe']:.2f}" if r["risk_neutralized_sharpe"] is not None else "NA"
    print(f"{r['id']:9s} {r['neutralization']:11s} {sh:>7s} {ft:>6s} {ty:>6s} {mg:>10s} {tv:>7s} {rn:>6s} {','.join(r['ra_failed_checks'])}")

cands = []
for r in rows:
    ok = (
        r["sharpe"] is not None and r["sharpe"] > 1.58
        and r["fitness"] is not None and r["fitness"] > 1.0
        and r["two_year_sharpe"] is not None and r["two_year_sharpe"] > 1.6
        and r["margin"] is not None and r["margin"] > 0.0005
        and r["turnover"] is not None and 0.05 < r["turnover"] < 0.30
        and r["failed_ra_count"] == 0
    )
    if ok:
        cands.append(r)

print("\n=== 通过用户全门槛 ===")
for r in cands:
    print(r["id"], r["code"])
print(f"count={len(cands)}")

near = [r for r in rows if r["sharpe"] and r["sharpe"] > 1.0 and r not in cands]
print("\n=== 近门槛(sharpe>1.0, 未过全门槛) ===")
for r in near:
    print(r["id"], f"sh={r['sharpe']:.2f}", f"fit={r['fitness']:.2f}", f"2y={r['two_year_sharpe']:.2f}", f"tvr={r['turnover']*100:.1f}%", r["code"][:90])

json.dump({"all": rows, "candidates": cands, "near": near}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\nsaved -> {OUT}")
