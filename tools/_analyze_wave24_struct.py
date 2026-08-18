# -*- coding: utf-8 -*-
"""wave24 全结果：按结构分类（av20 主力 / fwdPE_avdiff 三向 / 门控 / 其他）"""
import json

d = json.load(open(
    r"D:\coding\traeCN_project\wqb\tracking\GBR\results\wave24_starmine_grid_results.json",
    encoding="utf-8"))
rows = d.get("results", [])
print("wave24 rows:", len(rows))
print()
for r in rows:
    code = (r.get("code") or "")
    has_av20 = "ts_av_diff(ep_yield_pct_smest_fy2_3" in code
    has_fwdpe_avdiff = "ts_av_diff(forward_pe_smest_fy1_3" in code
    has_gate = "if_else(" in code or "trade_when(" in code
    n_add = code.count("add(") + code.count("multiply(")
    tag = []
    if has_av20:
        tag.append("AV20")
    if has_fwdpe_avdiff:
        tag.append("FWD_AVD")
    if has_gate:
        tag.append("GATE")
    if not tag:
        tag.append("OTHER")
    fc = r.get("failed_checks") or []
    print(
        f"{r.get('id')} [{'|'.join(tag)}] sh={r.get('sharpe')} fit={r.get('fitness')} "
        f"2y={r.get('two_year_sharpe')} mg={r.get('margin_bp')} tvr={r.get('turnover_pct')} "
        f"rn={r.get('rn_sharpe')} rnf={r.get('rn_fitness')} fc={fc}"
    )
