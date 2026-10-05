# -*- coding: utf-8 -*-
"""os_decay_benchmark.py — IS→OS 衰减基准与选品定标。

目的：把"IS Sharpe 到 OS 只剩多少"从口头经验变成**可计算的定标参数**，
供选品门槛与提交余量使用。

口径：`retention = os.sharpe / is.sharpe`（仅统计两者均非空且 IS>0 的样本）；
同时给出 **ACTIVE 队列**（在跑的）与 **DECOMMISSIONED 队列**（被退役的）两套基准
——后者是"失败下限"，选品时应按更保守的一套留余量。

产出：
  - 控制台表格（分位 + IS→期望 OS 映射 + 目标 OS 反推所需 IS）
  - `data/os_decay_benchmark.json`（机读，供其他工具/提示词引用）
  - `--for <IS>`：给定候选 IS Sharpe，打印期望 OS 区间（选品时直接用）

⚠ 覆盖面限制（2026-09-19 实测）：本账号**只有 USA 有 OS 数值**（其余 9 区
`os.sharpe` 全为 null）→ 当前基准是 **USA 校准**，用于其他区属外推，须标注。

用法（需 MCP venv 的 Python）：
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/os_decay_benchmark.py
  ... --for 1.58        # 选品咨询：IS=1.58 的期望 OS
"""
import argparse
import json
import os
import statistics as S
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(REPO, "logs", "_os_metrics_cache.json")
OUT_JSON = os.path.join(REPO, "data", "os_decay_benchmark.json")


def pct(vals, p):
    if not vals:
        return None
    v = sorted(vals)
    k = (len(v) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def retention_of(rows):
    out = []
    for r in rows:
        isd, osd = r.get("is_sharpe"), r.get("os_sharpe")
        if isd and osd is not None and isd > 0:
            out.append(osd / isd)
    return out


def load():
    with open(CACHE, encoding="utf-8") as f:
        return list(json.load(f).values())


def summarize(rows, label):
    ret = retention_of(rows)
    d = {"n": len(ret)}
    if not ret:
        return d
    for p, name in ((0.10, "p10"), (0.25, "p25"), (0.50, "p50"), (0.75, "p75"), (0.90, "p90")):
        d[name] = round(pct(ret, p), 3)
    d["mean"] = round(S.mean(ret), 3)
    return d


def main():
    ap = argparse.ArgumentParser(description="IS→OS 衰减基准与选品定标")
    ap.add_argument("--region", default="USA", help="当前只有 USA 有 OS 数值")
    ap.add_argument("--for", dest="for_is", type=float, default=None,
                    help="给定候选 IS Sharpe，打印期望 OS 区间")
    a = ap.parse_args()

    rows = [r for r in load() if (r.get("region") or "") == a.region.upper()]
    act = [r for r in rows if (r.get("status") or "").upper() == "ACTIVE"]
    dec = [r for r in rows if (r.get("status") or "").upper() == "DECOMMISSIONED"]

    act_s, dec_s = summarize(act, "ACTIVE"), summarize(dec, "DECOMMISSIONED")

    if not act_s.get("n") and not dec_s.get("n"):
        print(f"{a.region} 无 OS 数值样本")
        return

    print(f"=== IS→OS 衰减基准（{a.region}，{datetime.now():%Y-%m-%d}）===")
    print(f"{'队列':<16}{'n':>5}{'p10':>8}{'p25':>8}{'p50':>8}{'p75':>8}{'p90':>8}{'mean':>8}")
    for name, d in (("ACTIVE（在跑）", act_s), ("DECOMMISSIONED（退役）", dec_s)):
        if not d.get("n"):
            continue
        print(f"{name:<16}{d['n']:>5}" + "".join(
            f"{d.get(k, float('nan')):>8.3f}" for k in ("p10", "p25", "p50", "p75", "p90", "mean")))

    # 更保守的一套（取两队列中较低者）作为选品基准
    base = {k: min(act_s.get(k, 9), dec_s.get(k, 9)) for k in ("p25", "p50") if
            act_s.get(k) is not None or dec_s.get(k) is not None}
    print(f"\n选品用保守基准（两队列取低）：p25={base.get('p25')}  p50={base.get('p50')}")

    print("\n=== IS → 期望 OS（用保守基准）===")
    print(f"{'IS Sharpe':>10}{'OS@p25':>10}{'OS@p50':>10}")
    mapping = {}
    for isv in (1.0, 1.58, 2.0, 2.5, 3.0):
        r_p25 = isv * (base.get("p25") or 0)
        r_p50 = isv * (base.get("p50") or 0)
        mapping[isv] = {"os_p25": round(r_p25, 3), "os_p50": round(r_p50, 3)}
        print(f"{isv:>10.2f}{r_p25:>10.3f}{r_p50:>10.3f}")

    print("\n=== 目标 OS → 所需 IS（反推）===")
    need = {}
    for tgt in (0.3, 0.5, 0.7, 1.0):
        i_p25 = tgt / base["p25"] if base.get("p25") else None
        i_p50 = tgt / base["p50"] if base.get("p50") else None
        need[tgt] = {"is_for_p25": round(i_p25, 3) if i_p25 else None,
                     "is_for_p50": round(i_p50, 3) if i_p50 else None}
        print(f"  目标 OS ≥ {tgt:.2f}：IS ≥ {i_p25:.2f}（80% 把握, p25）／IS ≥ {i_p50:.2f}（中位, p50）"
              if i_p25 and i_p50 else f"  目标 OS ≥ {tgt:.2f}：样本不足")

    # ---- 决定性检验：IS 能否预测 OS？（2026-09-19，n=124）----
    # 结论：不能。corr(IS, retention)=+0.001、corr(IS,OS)=+0.092，且 OS<0 比例恒 ~22%。
    # → 选品门槛不应以"抬 IS"作为降低 OS 风险的手段。
    pairs = [(r["is_sharpe"], r["os_sharpe"]) for r in rows
             if r.get("is_sharpe") and r.get("os_sharpe") is not None and r["is_sharpe"] > 0]
    predictivity = {}
    if len(pairs) >= 10:
        xs = [p[0] for p in pairs]
        rets = [p[1] / p[0] for p in pairs]
        osv = [p[1] for p in pairs]

        def corr(a, b):
            ma, mb = S.mean(a), S.mean(b)
            num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
            den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
            return num / den if den else 0.0

        predictivity = {
            "n": len(pairs),
            "corr_is_retention": round(corr(xs, rets), 3),
            "corr_is_os": round(corr(xs, osv), 3),
            "os_negative_ratio": round(len([v for v in osv if v < 0]) / len(osv), 3),
        }
        print("\n=== IS 能否预测 OS？（决定性检验）===")
        print(f"  n={predictivity['n']}  corr(IS,保留率)={predictivity['corr_is_retention']:+.3f}  "
              f"corr(IS,OS)={predictivity['corr_is_os']:+.3f}  OS<0 比例={predictivity['os_negative_ratio']:.0%}")
        print("  → **IS 对 OS 无预测力**：抬 IS 门槛既不够提升期望 OS，也不会降低负 OS 概率。")
        print("     降低 OS 风险应靠：分散（数量×跨区）＋ 事后监控（os.sharpe60）＋ 族去相关。")
        buckets = [(0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 9)]
        print(f"\n  {'IS 区间':<12}{'n':>4}{'OS均值':>9}{'保留率中位':>11}{'OS<0':>7}")
        bl = {}
        for lo, hi in buckets:
            sub = [(i, o) for i, o in pairs if lo <= i < hi]
            if not sub:
                continue
            bl[f"{lo}~{hi}"] = {
                "n": len(sub),
                "os_mean": round(S.mean([o for _, o in sub]), 3),
                "retention_median": round(S.median([o / i for i, o in sub]), 3),
                "neg_ratio": round(len([o for _, o in sub if o < 0]) / len(sub), 3),
            }
            b = bl[f"{lo}~{hi}"]
            print(f"  {f'{lo}~{hi}':<12}{b['n']:>4}{b['os_mean']:>9.3f}"
                  f"{b['retention_median']:>11.3f}{b['neg_ratio']:>7.0%}")
        predictivity["buckets"] = bl

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "region": a.region.upper(),
        "coverage_caveat": "仅 USA 有 OS 数值（其余区 os.sharpe 为 null），本基准为 USA 校准",
        "cohorts": {"active": act_s, "decommissioned": dec_s},
        "conservative_base": base,
        "is_to_os": mapping,
        "os_target_to_is": need,
        "is_predictivity": predictivity,
        "selection_standard": {
            "expected_os_formula": f"OS ≈ {base.get('p50')} × IS（中位）；区间 p25≈{base.get('p25')}×IS ～ p75≈{act_s.get('p75') or dec_s.get('p75')}×IS",
            "negative_risk": f"负 OS 概率约 {predictivity.get('os_negative_ratio', 0):.0%}，**与 IS 高低无关**（corr={predictivity.get('corr_is_retention')}）",
            "implication": ("抬高 IS 门槛不能降低 OS 风险，只能提升期望值；"
                            "降风险靠分散（数量×跨区）+ os.sharpe60 事后监控 + 族去相关"),
            "submit_bar_check": ("IS 1.58（USA 提交门槛）→ 期望 OS ≈ 0.50（中位），"
                                 "约 1/4 概率 OS ≥ 0.65，约 22% 概率 OS < 0"),
        },
        "sample_note": f"ACTIVE {act_s.get('n')} 颗 + DECOMMISSIONED {dec_s.get('n')} 颗（retention 仅计 IS>0 且有 OS 值者）",
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"\n机读基准 → {OUT_JSON}")

    if a.for_is:
        print(f"\n=== 选品咨询：IS = {a.for_is} ===")
        lo = a.for_is * (base.get("p25") or 0)
        mid = a.for_is * (base.get("p50") or 0)
        hi = a.for_is * (act_s.get("p75") or base.get("p50") or 0)
        print(f"  期望 OS Sharpe ≈ {lo:.2f}（保守, p25）～ {mid:.2f}（中位）～ {hi:.2f}（乐观, p75）")
        print(f"  低于 0 的风险参考：负 OS 在 ACTIVE 中占 "
              f"{len([r for r in act if (r.get('os_sharpe') or 0) < 0])}/{act_s.get('n')}")


if __name__ == "__main__":
    main()
