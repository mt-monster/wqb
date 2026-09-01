# -*- coding: utf-8 -*-
"""diversity_audit.py - 多样性审计累积进台账（M18）。

取代 kor_op_exploration_stats.py 的静态一次性扫描：每次运行把算子/字段/骨架分布
追加进台账 diversity_history（累积可看趋势），并更新 diversity_audit_latest。

用法:
  python diversity_audit.py            # 扫描全部 wave 文件 + 写台账
  python diversity_audit.py --no-ledger # 只打印
"""
import argparse, collections, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import kor_ledger

KNOWN_OPS = [
    "rank", "add", "subtract", "multiply", "divide", "signed_power", "sqrt",
    "greater", "less", "if_else", "trade_when", "delay", "delta", "ts_delay",
    "ts_delta", "ts_mean", "ts_sum", "ts_std_dev", "ts_rank", "ts_decay_linear",
    "ts_ir", "ts_av_diff", "ts_scale", "ts_zscore", "ts_backfill", "ts_arg_max",
    "ts_arg_min", "ts_product", "group_rank", "group_neutralize", "group_mean",
    "group_sum", "group_zscore", "quantile", "pasteurize", "normalize", "vec_avg",
    "vec_max", "vec_min", "vec_sum", "vec_count", "vec_norm", "bucket", "range",
    "winsorize", "abs", "log", "sign", "exp", "power",
]


def skeleton(e):
    if "trade_when(" in e or "if_else(" in e:
        return "event_gated"
    if "group_" in e:
        return "group"
    if "divide(" in e:
        return "ratio"
    if "add(" in e or "multiply(" in e:
        return "linear_mix"
    return "single"


def audit():
    ops, fields, skel = collections.Counter(), collections.Counter(), collections.Counter()
    total, uniq = 0, set()
    files = glob.glob(os.path.join(ROOT, "kor_wave*_exprs.json")) + \
        glob.glob(os.path.join(ROOT, "candidates", "*.json"))
    for f in files:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        ex = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
        for e in ex:
            if not isinstance(e, str):
                continue
            total += 1
            uniq.add(re.sub(r"\s+", "", e))
            skel[skeleton(e)] += 1
            for tok in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*\(", e):
                ops[tok[:-1]] += 1
            for t in set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", e)):
                if len(t) > 6 and t not in KNOWN_OPS:
                    fields[t] += 1
    used = {op for op in KNOWN_OPS if ops.get(op, 0) > 0}
    return {
        "audited_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "wave_files": len(files), "total_exprs": total, "unique_exprs": len(uniq),
        "duplicate_exprs": total - len(uniq),
        "operator_exploration_rate": round(len(used) / len(KNOWN_OPS), 3),
        "operators_used": len(used), "operators_known": len(KNOWN_OPS),
        "operators_unused": [op for op in KNOWN_OPS if op not in used],
        "operator_freq_top": dict(ops.most_common(12)),
        "skeleton_distribution": dict(skel),
        "field_count": len(fields),
        "field_freq_top": dict(fields.most_common(12)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-ledger", action="store_true")
    a = ap.parse_args()
    r = audit()
    print(json.dumps(r, ensure_ascii=False, indent=1))
    if not a.no_ledger:
        def mut(d):
            d["diversity_audit_latest"] = r
            hist = d.setdefault("diversity_history", [])
            hist.append({"at": r["audited_at"], "total": r["total_exprs"],
                         "unique": r["unique_exprs"],
                         "exploration_rate": r["operator_exploration_rate"],
                         "skeleton": r["skeleton_distribution"]})
        kor_ledger.update(mut)
        print("ledger: diversity_audit_latest + diversity_history updated", file=sys.stderr)


if __name__ == "__main__":
    main()
