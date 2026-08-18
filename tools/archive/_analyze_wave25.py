# -*- coding: utf-8 -*-
"""wave25 候选详情分析：candidates 列表 + decay/truncation 还原 + 与 wave24 对照"""
import json

d = json.load(open(
    r"D:\coding\traeCN_project\wqb\tracking\GBR\results\wave25_starmine_refine_results.json",
    encoding="utf-8"))
cands = d.get("candidates", [])
print("candidates:", len(cands))
print()

# items 的 code -> meta 映射（decay/truncation 依据 items 文件还原）
items = json.load(open(
    r"D:\coding\traeCN_project\wqb\tracking\GBR\candidates\gbr_wave25_starmine_refine_items.json",
    encoding="utf-8"))
meta_map = {}
for it in items:
    key = it["code"].strip()
    if key not in meta_map:
        meta_map[key] = (it.get("decay"), it.get("truncation"))
    else:
        # 同 code 多 settings，追加
        pass

for c in cands:
    code = (c.get("code") or "").strip()
    dec = c.get("decay")
    tru = c.get("truncation")
    # 若结果行 decay 缺失，尝试用 code 还原
    if dec is None and code in meta_map:
        dec, tru = meta_map[code]
    print(
        f"{c.get('id')} d={dec} t={tru} sh={c.get('sharpe')} fit={c.get('fitness')} "
        f"2y={c.get('two_year_sharpe')} mg={c.get('margin_bp')} tvr={c.get('turnover_pct')} "
        f"rn={c.get('rn_sharpe')} rnf={c.get('rn_fitness')} fc={c.get('failed_checks')}"
    )
    print(f"   {code[:140]}")
    print()

# 全 24 行中 failed_checks 非空的
print("=== 非候选行（24 总数中的其他行）===")
rows = d.get("results", [])
print("total rows:", len(rows))
ids_cand = {c["id"] for c in cands}
for r in rows:
    if r.get("id") not in ids_cand:
        fc = r.get("failed_checks")
        code = (r.get("code") or "").strip()
        dec = r.get("decay")
        if dec is None and code in meta_map:
            dec, _ = meta_map[code]
        print(
            f"{r.get('id')} d={dec} sh={r.get('sharpe')} 2y={r.get('two_year_sharpe')} "
            f"rnf={r.get('rn_fitness')} fc={fc} {code[:100]}"
        )
