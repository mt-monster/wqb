#!/usr/bin/env python3
"""EUR / ml_factor_proj PPA 挖掘批次提交与取回。

用法:
  python tools/mine_eur_mlfactor.py submit  <batch_tag>
  python tools/mine_eur_mlfactor.py fetch   <batch_tag>
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util
import importlib.machinery

_spec = importlib.util.spec_from_loader(
    "mcp_py", importlib.machinery.SourceFileLoader("mcp_py", str(Path(__file__).resolve().parent / "mcp_py"))
)
mcp_py = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mcp_py)
call_tool = mcp_py.call_tool

WORKSPACE = Path(__file__).resolve().parent.parent
OUT = WORKSPACE / "tracking" / "mining"
OUT.mkdir(parents=True, exist_ok=True)

REGION = "EUR"
UNIVERSE = "TOP1200"
DELAY = 1

# ---- V9 范式: reversed spread + returns 反转 ----
V9 = ("scale(rank(ts_zscore(subtract(ts_mean(ts_backfill({a},66),22),"
      "ts_mean(ts_backfill({b},66),22),filter=true),189)))"
      "+scale(-rank(ts_zscore(returns,42)))*{w}")

# 单字段版 (无 spread), 用于对照
V9S = ("scale(rank(ts_zscore(ts_mean(ts_backfill({a},66),22),189)))"
       "+scale(-rank(ts_zscore(returns,42)))*{w}")


def build(pairs, w=0.35):
    out = []
    for label, a, b in pairs:
        expr = V9.format(a=a, b=b, w=w) if b else V9S.format(a=a, w=w)
        out.append((label, expr))
    return out


BATCHES = {
    # 批次 e1: 三方向探测, 统一 SUBINDUSTRY / decay=4
    "e1": dict(
        neutralization="SUBINDUSTRY", decay=4, truncation=0.08,
        pairs=[
            ("A1_ar60_3",   "change_60m_active_return", "change_3m_active_return"),
            ("A2_ar24_6",   "change_24m_active_return", "change_6m_active_return"),
            ("A3_ar12_1",   "change_twelve_month_active_return", "change_1m_active_return"),
            ("B1_eps_1y3y", "change_1y_eps_to_price", "change_3y_eps_to_price"),
            ("B2_cf_1y3y",  "change_1y_cashflow_to_price", "change_3y_cashflow_to_price"),
            ("B3_relE_eps", "change_5y_relative_earnings_to_price", "change_1y_eps_to_price"),
            ("C1_alpha12_60", "change_12m_alpha", "change_60m_alpha"),
            ("C2_ar36_9",   "change_36m_active_return", "change_9m_active_return"),
        ]),
    # 批次 e2: COUNTRY 中性化对照 (EUR 多国市场)
    "e2": dict(
        neutralization="COUNTRY", decay=4, truncation=0.08,
        pairs=[
            ("A1_ar60_3",   "change_60m_active_return", "change_3m_active_return"),
            ("A2_ar24_6",   "change_24m_active_return", "change_6m_active_return"),
            ("A3_ar12_1",   "change_twelve_month_active_return", "change_1m_active_return"),
            ("B1_eps_1y3y", "change_1y_eps_to_price", "change_3y_eps_to_price"),
            ("B2_cf_1y3y",  "change_1y_cashflow_to_price", "change_3y_cashflow_to_price"),
            ("B3_relE_eps", "change_5y_relative_earnings_to_price", "change_1y_eps_to_price"),
            ("C1_alpha12_60", "change_12m_alpha", "change_60m_alpha"),
            ("C2_ar36_9",   "change_36m_active_return", "change_9m_active_return"),
        ]),
}


# ---- 第二轮: 围绕胜出方向 A3 换结构 (raw 表达式直给) ----
A = "change_twelve_month_active_return"
B = "change_1m_active_return"
SPREAD120 = f"subtract(ts_backfill({A},120),ts_backfill({B},120))"
RET = "scale(-rank(ts_zscore(returns,42)))"

RAW_BATCHES = {
    "e3": dict(
        neutralization="SUBINDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
        unit_handling="VERIFY",
        exprs=[
            ("T1_pure",   f"rank({SPREAD120})"),
            ("T2_grp",    f"group_rank({SPREAD120},subindustry)"),
            ("T3_tsrank", f"ts_rank(subtract(ts_backfill({A},250),ts_backfill({B},250)),250)"),
            ("T4_wins",   f"normalize(winsorize({SPREAD120},std=4))"),
            ("T5_zs60",   f"rank(ts_zscore({SPREAD120},60))"),
            ("T6_nore",   f"scale(rank(ts_zscore(subtract(ts_mean(ts_backfill({A},66),22),"
                          f"ts_mean(ts_backfill({B},66),22),filter=true),189)))"),
            ("T7_re07",   f"scale(rank(ts_zscore(subtract(ts_mean(ts_backfill({A},66),22),"
                          f"ts_mean(ts_backfill({B},66),22),filter=true),189)))+{RET}*0.7"),
            ("T8_trio",   "rank(subtract(add(ts_backfill(change_twelve_month_active_return,120),"
                          "ts_backfill(change_24m_active_return,120)),"
                          "add(ts_backfill(change_1m_active_return,120),"
                          "ts_backfill(change_3m_active_return,120))))"),
        ]),
    # e4: 换字段族 —— 经典 alpha 来源单字段净信号强度扫描 (无 returns 项)
    "e4": dict(
        neutralization="SUBINDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
        exprs=[(f"F_{f.replace('change_','')[:18]}",
                f"rank(ts_zscore(ts_backfill({f},120),250))") for f in [
            "change_52w_high_price_ratio",
            "change_50_200d_price_ratio",
            "change_30_75w_price_ratio",
            "change_analyst_consensus_rating",
            "change_3m_revision_fy2_eps",
            "change_6m_rating_revision",
            "change_dispersion_fy2_eps_estimates",
            "change_20d_volume_to_price_volatility",
        ]]),
    # e5: 多因子合成 —— 把前三轮所有正 sharpe 方向按权重组合
    "e5": dict(
        neutralization="SUBINDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
        exprs=[
            ("M1_core3",
             f"scale(rank(ts_zscore({SPREAD120},189)))*0.4"
             "+scale(rank(ts_zscore(ts_backfill(change_52w_high_price_ratio,120),250)))*0.2"
             "+scale(rank(ts_zscore(ts_backfill(change_20d_volume_to_price_volatility,120),250)))*0.2"
             f"+{RET}*0.2"),
            ("M2_core5",
             f"scale(rank(ts_zscore({SPREAD120},189)))*0.3"
             "+scale(rank(ts_zscore(subtract(ts_backfill(change_5y_relative_earnings_to_price,120),"
             "ts_backfill(change_1y_eps_to_price,120)),189)))*0.2"
             "+scale(rank(ts_zscore(subtract(ts_backfill(change_12m_alpha,120),"
             "ts_backfill(change_60m_alpha,120)),189)))*0.15"
             "+scale(rank(ts_zscore(ts_backfill(change_52w_high_price_ratio,120),250)))*0.15"
             f"+{RET}*0.2"),
            ("M3_core3_re05",
             f"scale(rank(ts_zscore({SPREAD120},189)))*0.35"
             "+scale(rank(ts_zscore(ts_backfill(change_52w_high_price_ratio,120),250)))*0.15"
             f"+{RET}*0.5"),
            ("M4_core3_big",
             f"scale(rank(ts_zscore({SPREAD120},189)))*0.4"
             "+scale(rank(ts_zscore(ts_backfill(change_52w_high_price_ratio,120),250)))*0.2"
             "+scale(rank(ts_zscore(ts_backfill(change_20d_volume_to_price_volatility,120),250)))*0.2"
             f"+{RET}*0.2"),
            ("M5_grp_core3",
             f"scale(group_rank({SPREAD120},subindustry))*0.4"
             "+scale(group_rank(ts_backfill(change_52w_high_price_ratio,120),subindustry))*0.2"
             "+scale(group_rank(ts_backfill(change_20d_volume_to_price_volatility,120),subindustry))*0.2"
             f"+{RET}*0.2"),
            ("M6_ts_core3",
             f"scale(ts_rank({SPREAD120},250))*0.4"
             "+scale(ts_rank(ts_backfill(change_52w_high_price_ratio,120),250))*0.2"
             "+scale(ts_rank(ts_backfill(change_20d_volume_to_price_volatility,120),250))*0.2"
             f"+{RET}*0.2"),
            ("M7_neg_short",
             f"scale(rank(ts_zscore({SPREAD120},189)))*0.4"
             "+scale(-rank(ts_zscore(ts_backfill(change_analyst_consensus_rating,120),250)))*0.2"
             "+scale(-rank(ts_zscore(ts_backfill(change_30_75w_price_ratio,120),250)))*0.2"
             f"+{RET}*0.2"),
            ("M8_full_mix",
             f"scale(rank(ts_zscore({SPREAD120},189)))*0.3"
             "+scale(rank(ts_zscore(ts_backfill(change_52w_high_price_ratio,120),250)))*0.15"
             "+scale(rank(ts_zscore(ts_backfill(change_20d_volume_to_price_volatility,120),250)))*0.15"
             "+scale(-rank(ts_zscore(ts_backfill(change_analyst_consensus_rating,120),250)))*0.1"
             "+scale(-rank(ts_zscore(ts_backfill(change_dispersion_fy2_eps_estimates,120),250)))*0.1"
             f"+{RET}*0.2"),
        ]),
}
RAW_BATCHES["e5"]["universe"] = "TOP1200"

# ============ e8: 论坛全模板验证 (映射到 ml_factor_proj; 排除不可访问的 ts_entropy) ============
# 关键教训: 一个 fatal operator 会级联 CANCEL 整个 multisimulation,
# 故把风险算子 (if_else/greater/abs/ts_scale) 隔离到单独批次 e9, 其余用标准算子。
# e8a: 标准算子模板族代表 (10) —— T1/T2/T5/T6/T7/T10/T11/T15/T3/T14
RAW_BATCHES["e8a"] = dict(
    neutralization="INDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
    exprs=[
        ("T1_drev",    "-ts_delta(change_1y_eps_growth, 66)"),
        ("T2_small",   "-change_1y_eps_growth * ts_std_dev(change_1y_eps_growth, 30)"),
        ("T5_base",    "group_rank(ts_rank(change_1y_eps_growth, 252), industry)"),
        ("T6_eymom",   "group_rank(ts_rank(change_1y_eps_to_price, 60), industry)"),
        ("T7_peg",     "-group_zscore(subtract(change_1y_eps_to_price, change_1y_eps_growth), industry)"),
        ("T10_term",   "group_zscore(subtract(group_zscore(change_60m_active_return, industry), "
                       "group_zscore(change_1m_active_return, industry)), industry)"),
        ("T11_dupont", "group_zscore(subtract(ts_zscore(change_1y_eps_growth, 250), "
                       "ts_zscore(change_3y_cashflow_to_price, 250)), industry)"),
        ("T15_vol",    "-ts_std_dev(change_20d_volume_to_price_volatility, 10)"),
        ("T3_opearn",  "ts_rank(change_1y_eps_growth, 252)"),
        ("T14_semivar","-ts_std_dev(change_1m_active_return, 30)"),
    ])
# e8b: 期限结构窗口对扫描 + 反转/PEG 变体 (7) —— T10 多变体 + T1v/T2v/T7v
RAW_BATCHES["e8b"] = dict(
    neutralization="INDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
    exprs=[
        ("T10v_36_6",  "group_zscore(subtract(group_zscore(change_36m_active_return, industry), "
                       "group_zscore(change_6m_active_return, industry)), industry)"),
        ("T10v_24_9",  "group_zscore(subtract(group_zscore(change_24m_active_return, industry), "
                       "group_zscore(change_9m_active_return, industry)), industry)"),
        ("T10v_12_1",  "group_zscore(subtract(group_zscore(change_twelve_month_active_return, industry), "
                       "group_zscore(change_1m_active_return, industry)), industry)"),
        ("T10v_60_3",  "group_zscore(subtract(group_zscore(change_60m_active_return, industry), "
                       "group_zscore(change_3m_active_return, industry)), industry)"),
        ("T1v_cf",     "-ts_delta(change_3y_cashflow_to_price, 66)"),
        ("T2v_mom",    "-change_fama_french_momentum * ts_std_dev(change_fama_french_momentum, 30)"),
        ("T7v_divpeg", "-group_zscore(divide(change_1y_eps_to_price, change_1y_eps_growth), industry)"),
    ])
# e9: 条件算子模板单独隔离 (if_else/greater/abs/ts_scale) —— 避免级联取消好模板
RAW_BATCHES["e9"] = dict(
    neutralization="INDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
    exprs=[
        ("T12_qual",   "if_else(greater(abs(change_dispersion_fy2_eps_estimates), 0.001), "
                       "ts_scale(change_3m_revision_fy2_eps, 60), 0)"),
        ("T12_qual2",  "if_else(greater(change_3m_revision_fy2_eps, 0), "
                       "ts_rank(change_dispersion_fy2_eps_estimates, 60), 0)"),
    ])
# e10a/e10b/e11: e8a/e9 整批瞬态失败后, 拆小批次重跑 (规避整批 CANCEL/ERROR)
RAW_BATCHES["e10a"] = dict(
    neutralization="INDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
    exprs=[
        ("T1_drev",  "-ts_delta(change_1y_eps_growth, 66)"),
        ("T2_small", "-change_1y_eps_growth * ts_std_dev(change_1y_eps_growth, 30)"),
        ("T5_base",  "group_rank(ts_rank(change_1y_eps_growth, 252), industry)"),
        ("T6_eymom", "group_rank(ts_rank(change_1y_eps_to_price, 60), industry)"),
        ("T7_peg",   "-group_zscore(subtract(change_1y_eps_to_price, change_1y_eps_growth), industry)"),
    ])
RAW_BATCHES["e10b"] = dict(
    neutralization="INDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
    exprs=[
        ("T10_term",   "group_zscore(subtract(group_zscore(change_60m_active_return, industry), "
                       "group_zscore(change_1m_active_return, industry)), industry)"),
        ("T11_dupont", "group_zscore(subtract(ts_zscore(change_1y_eps_growth, 250), "
                       "ts_zscore(change_3y_cashflow_to_price, 250)), industry)"),
        ("T15_vol",    "-ts_std_dev(change_20d_volume_to_price_volatility, 10)"),
        ("T3_opearn",  "ts_rank(change_1y_eps_growth, 252)"),
        ("T14_semivar","-ts_std_dev(change_1m_active_return, 30)"),
    ])
RAW_BATCHES["e11"] = dict(
    neutralization="INDUSTRY", decay=4, truncation=0.08, universe="TOP1200",
    exprs=[
        ("T12_qual",   "if_else(greater(abs(change_dispersion_fy2_eps_estimates), 0.001), "
                       "ts_scale(change_3m_revision_fy2_eps, 60), 0)"),
        ("T12_qual2",  "if_else(greater(change_3m_revision_fy2_eps, 0), "
                       "ts_rank(change_dispersion_fy2_eps_estimates, 60), 0)"),
    ])
# e6 = e5 的 TOP2500 大池版本 (延后按需启用)


def submit_raw(tag):
    cfg = RAW_BATCHES[tag]
    built = cfg["exprs"]
    exprs = [e for _, e in built]
    args = dict(
        alpha_expressions=exprs,
        instrument_type="EQUITY", region=REGION,
        universe=cfg.get("universe", UNIVERSE), delay=DELAY,
        decay=cfg["decay"], neutralization=cfg["neutralization"],
        truncation=cfg["truncation"], test_period="P0Y0M",
        unit_handling=cfg.get("unit_handling", "VERIFY"), nan_handling="OFF",
        language="FASTEXPR", visualization=False, pasteurization="ON",
    )
    meta = {"tag": tag, "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            "labels": [l for l, _ in built], "args": args}
    (OUT / f"args_mlfp_{tag}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[submit] {tag}: {len(exprs)} exprs, neut={cfg['neutralization']}, "
          f"univ={args['universe']}, decay={cfg['decay']}")
    res = call_tool("create_multi_simulation", args, timeout=1800)
    (OUT / f"res_mlfp_{tag}.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items() if k != "submitted_expressions"},
                     ensure_ascii=False, indent=1, default=str)[:1200])


def submit(tag):
    if tag in RAW_BATCHES:
        return submit_raw(tag)
    cfg = BATCHES[tag]
    built = build(cfg["pairs"])
    exprs = [e for _, e in built]
    args = dict(
        alpha_expressions=exprs,
        instrument_type="EQUITY", region=REGION, universe=UNIVERSE, delay=DELAY,
        decay=cfg["decay"], neutralization=cfg["neutralization"],
        truncation=cfg["truncation"], test_period="P0Y0M",
        unit_handling="VERIFY", nan_handling="OFF", language="FASTEXPR",
        visualization=False, pasteurization="ON",
    )
    meta = {"tag": tag, "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            "labels": [l for l, _ in built], "args": args}
    (OUT / f"args_mlfp_{tag}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[submit] {tag}: {len(exprs)} exprs, neut={cfg['neutralization']}, decay={cfg['decay']}")
    res = call_tool("create_multi_simulation", args, timeout=1800)
    (OUT / f"res_mlfp_{tag}.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str)[:3000])


def _retry(tool, args, n=4, wait=8, timeout=900):
    last = None
    for i in range(n):
        r = call_tool(tool, args, timeout=timeout)
        if not (isinstance(r, dict) and r.get("error")):
            return r
        last = r
        time.sleep(wait)
    return last


def fetch(tag):
    res = json.loads((OUT / f"res_mlfp_{tag}.json").read_text(encoding="utf-8"))
    meta = json.loads((OUT / f"args_mlfp_{tag}.json").read_text(encoding="utf-8"))
    mid = res.get("multisimulation_id")
    loc = res.get("multisimulation_location") or f"https://api.worldquantbrain.com/simulations/{mid}"
    labels = meta["labels"]
    ch = _retry("get_multisimulation_children", {"multisimulation_location": loc})
    (OUT / f"children_mlfp_{tag}.json").write_text(
        json.dumps(ch, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    kids = ch.get("children") or ch.get("results") or []
    print(f"[fetch] {tag} mid={mid} children={len(kids)}")
    if not kids:
        return
    locs = [k.get("location_url") or k.get("location") if isinstance(k, dict) else k for k in kids]
    info = _retry("lookINTO_SimError_message", {"locations": locs})
    (OUT / f"simstat_mlfp_{tag}.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    items = info.get("results") or info.get("simulations") or info.get("items") or []
    rows = []
    for i, k in enumerate(kids):
        it = items[i] if i < len(items) else {}
        if not isinstance(it, dict):
            it = {}
        aid = it.get("alpha") or it.get("alpha_id")
        lbl = labels[i] if i < len(labels) else f"#{i}"
        rows.append({"label": lbl, "sim": locs[i], "status": it.get("status"),
                     "alpha": aid, "message": it.get("message") or it.get("error")})
    for r in rows:
        if not r["alpha"]:
            continue
        d = _retry("get_alpha_details", {"alpha_id": r["alpha"]}, n=3)
        m = (d or {}).get("is") or (d or {}).get("metrics") or {}
        r["sharpe"] = m.get("sharpe")
        r["fitness"] = m.get("fitness")
        r["turnover"] = m.get("turnover")
        r["returns"] = m.get("returns")
        r["drawdown"] = m.get("drawdown")
        r["margin"] = m.get("margin")
        checks = (d or {}).get("is", {}).get("checks") or []
        r["fail"] = [c.get("name") for c in checks if c.get("result") == "FAIL"]
    (OUT / f"rows_mlfp_{tag}.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    hdr = f"{'label':16} {'status':10} {'alpha':10} {'sharpe':>7} {'fit':>6} {'tvr':>6} {'ret':>7}"
    print(hdr); print("-" * len(hdr))
    for r in sorted(rows, key=lambda x: -(x.get("sharpe") or -9)):
        print(f"{r['label']:16} {str(r['status'])[:10]:10} {str(r.get('alpha'))[:10]:10} "
              f"{(r.get('sharpe') if r.get('sharpe') is not None else float('nan')):7.2f} "
              f"{(r.get('fitness') if r.get('fitness') is not None else float('nan')):6.2f} "
              f"{(r.get('turnover') if r.get('turnover') is not None else float('nan')):6.3f} "
              f"{(r.get('returns') if r.get('returns') is not None else float('nan')):7.4f}"
              + ("  FAIL=" + ",".join(r.get("fail") or []) if r.get("fail") else ""))


if __name__ == "__main__":
    cmd, tag = sys.argv[1], sys.argv[2]
    if cmd == "submit":
        submit(tag)
    elif cmd == "fetch":
        fetch(tag)
    else:
        raise SystemExit("unknown cmd")
