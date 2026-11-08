"""margin 的预测力检验（只读分析，不参与提交路径）。

问题：2026-11-08 讨论「要不要给 submit_alpha 加一道 margin 闸」。加闸前必须先回答两件事：
  1. margin 对真实 OS 表现（os_sharpe125）有没有预测力？若有，阈值才有意义。
  2. margin 是不是**独立信息**？官方 Fitness = Sharpe * sqrt(|Returns| / max(Turnover, 0.125))，
     而 glossary 的 Margin = PnL / total dollars traded ≈ Returns / (504 * Turnover)。
     ⇒ 当 Turnover >= 0.125 时 margin ∝ (Fitness/Sharpe)^2，是**冗余字段**；
        只有 Turnover < 0.125（Fitness 分母被封顶）时 margin 才携带增量信息。
     若成立，「margin 闸」等价于「Fitness 闸」，不该重复设闸。

数据来源：`batch_get_alpha_metrics` 实测 80 颗已提交 USA alpha 的 margin（2026-11-08 拉取），
`os_sharpe125` 取自本地库 data/wqb.db。

用法：
    python tools/gates/margin_predictive_power.py
"""
from __future__ import annotations

import math
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from wqb import db_conn  # noqa: E402

DB = Path(__file__).resolve().parents[2] / "data" / "wqb.db"

# 2026-11-08 由 mcp__wq-brain-http__batch_get_alpha_metrics 实测（4 批 x 20 颗），单位 bp
MARGIN_BP = {
    # batch 1
    "ArN8Q8Y": 2.856, "WL5qXEG": 1.079, "nqN0qYx": 6.942, "v62M88a": 5.207,
    "NVYbl1g": 8.438, "eGK9Lvd": 16.055, "EzZbK6G": 11.300, "7vlVbl8": 0.767,
    "RzMOGR0": 2.800, "WZdxPRk": 0.342, "v6P11Nw": 4.067, "35xZxxX": 2.233,
    "6J1P0XL": 4.255, "qLL7zpZ": 9.865, "9m65rXe": 3.556, "zGaGnqK": 11.895,
    "1K9bE3z": 5.628, "rVA721a": 6.369, "AzRmNQw": 13.185, "KmP73gj": 6.873,
    # batch 2
    "0gnPV9p": 13.719, "AzZMAlw": 3.011, "KzE3N2k": 6.332, "Mz963Vk": 17.012,
    "evKdVnl": 3.293, "YJkjgww": 3.206, "xGwV5Jq": 9.345, "rVAOZAo": 6.209,
    "GzZ73Lo": 13.289, "bzWqQo6": 13.623, "9Mgnx8e": 8.960, "x2mv07N": 1.181,
    "do61Ynv": 5.100, "9mJazvr": 8.088, "jxw95NW": 1.895, "7v1bE3v": 2.171,
    "N3jVjzp": 3.356, "XvnkAk0": 1.249, "AmYvjPe": 3.138, "2XmbgGP": 1.665,
    # batch 3
    "l935K2O": 5.495, "GzA0rOx": 4.206, "JWQpA3O": 2.000, "55nP3w5": 2.343,
    "gdx066J": 6.880, "VdKw8Jw": 0.754, "WodgzLO": 1.041, "J19Goe2": 5.035,
    "5Glv3nn": 8.720, "rVLLKZ3": 4.303, "m1JaJz6": 1.959, "K5rmVOx": 2.713,
    "P8pPpaw": 4.429, "m0X79vx": 2.151, "6JMmdrG": 5.739, "KQ6x7El": 5.333,
    "LZmvE16": 9.117, "dodNqlJ": 5.718, "9MvEjwx": 10.458, "7oLgPAL": 3.936,
    # batch 4
    "1PLJxnR": 2.798, "Gze9QEO": 9.894, "5eqrE56": 2.034, "VmdG395": 2.909,
    "do7bLmg": 2.683, "06exgMk": 6.135, "60qLZ17": 16.160, "RzXZ0va": 9.246,
    "bxleg9R": 1.306, "GxL1wjQ": 4.843, "5ALEdk5": 1.149, "x2mMoMJ": 0.901,
    "EzYdjkR": 15.311, "eGKGo3O": 14.948, "azJnjd5": 8.613, "pGPqPXb": 10.956,
    "rGOdX8E": 5.724, "OM2V3r1": 0.707, "2XwomaY": 3.471, "orAkx3k": 2.562,
}


def spearman(x, y):
    pairs = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pairs) < 10:
        return None, len(pairs)
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]

    def rk(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = rk(xs), rk(ys)
    n = len(pairs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return (num / den if den else None), n


def main() -> int:
    conn = db_conn.connect(str(DB))
    conn.row_factory = sqlite3.Row
    ids = list(MARGIN_BP)
    ph = ",".join("?" * len(ids))
    rows = [dict(r) for r in conn.execute(
        f"""SELECT alpha_id, sharpe, fitness, turnover, returns, os_sharpe125, os_sharpe60, os_sharpe
            FROM alphas WHERE alpha_id IN ({ph})""", ids)]

    for r in rows:
        r["margin"] = MARGIN_BP[r["alpha_id"]] / 1e4
    rows = [r for r in rows if r["os_sharpe125"] is not None]
    print(f"样本: {len(rows)} 颗（已提交 USA，margin 实测 + os125 本地）\n")

    # ---- 检验 1：margin 的定义等式 ----
    print("=== 检验 1：margin ≈ Returns / (504 × Turnover)？ ===")
    devs = []
    for r in rows:
        if r["returns"] and r["turnover"]:
            pred = r["returns"] / (504 * r["turnover"])
            if r["margin"]:
                devs.append(abs(pred - r["margin"]) / r["margin"])
    devs.sort()
    print(f"  相对偏差中位 {devs[len(devs)//2]:.1%}｜p90 {devs[int(len(devs)*0.9)]:.1%}（n={len(devs)}）")
    print("  ⇒ 等式成立则 margin 不携带 Returns/Turnover 之外的独立信息\n")

    # ---- 检验 2：margin 与 Fitness 的共线程度 ----
    print("=== 检验 2：margin 是否只是 Fitness/Sharpe 的函数？ ===")
    # 理论上 TO>=0.125: margin ∝ (F/S)^2 / 504 * ... 直接看经验相关
    rho_fs, n_fs = spearman([r["margin"] for r in rows],
                            [(r["fitness"] / r["sharpe"]) ** 2 if r["sharpe"] else None for r in rows])
    rho_f, n_f = spearman([r["margin"] for r in rows], [r["fitness"] for r in rows])
    rho_s, n_s = spearman([r["margin"] for r in rows], [r["sharpe"] for r in rows])
    rho_t, n_t = spearman([r["margin"] for r in rows], [-r["turnover"] for r in rows])
    print(f"  ρ(margin, (F/S)^2) = {rho_fs:+.3f}  n={n_fs}   ← 定义式预测应接近 +1")
    print(f"  ρ(margin, Fitness) = {rho_f:+.3f}  n={n_f}")
    print(f"  ρ(margin, Sharpe)  = {rho_s:+.3f}  n={n_s}")
    print(f"  ρ(margin, -Turnover)={rho_t:+.3f}  n={n_t}\n")

    # ---- 检验 3：margin 对 OS 的预测力（核心） ----
    print("=== 检验 3：margin vs 真实 OS（核心问题） ===")
    print(f"{'指标':16s}{'ρ vs os125':>12s}{'ρ vs os60':>12s}{'ρ vs os全期':>13s}")
    for name, getter in (
        ("margin", lambda r: r["margin"]),
        ("Fitness", lambda r: r["fitness"]),
        ("Sharpe", lambda r: r["sharpe"]),
        ("2Y(缺失)", lambda r: r["two_year_sharpe"] if "two_year_sharpe" in r else None),
    ):
        a, _ = spearman([getter(r) for r in rows], [r["os_sharpe125"] for r in rows])
        b, _ = spearman([getter(r) for r in rows], [r["os_sharpe60"] for r in rows])
        c, _ = spearman([getter(r) for r in rows], [r["os_sharpe"] for r in rows])
        fmt = lambda v: f"{v:+.3f}" if v is not None else "n/a"
        print(f"{name:16s}{fmt(a):>12s}{fmt(b):>12s}{fmt(c):>13s}")

    # ---- 检验 4：分位分层 ----
    print("\n=== 检验 4：margin 四分位 → OS 均值 ===")
    s = sorted(rows, key=lambda r: r["margin"])
    k = max(len(s) // 4, 1)
    print(f"{'分位':22s}{'n':>4s}{'margin中位':>11s}{'os125':>8s}{'os60':>8s}{'IS S':>7s}{'F':>6s}{'负OS':>7s}")
    for i in range(4):
        seg = s[i * k:(i + 1) * k] if i < 3 else s[3 * k:]
        if not seg:
            continue
        m = sorted(r["margin"] for r in seg)[len(seg) // 2]
        print(f"Q{i+1} {seg[0]['margin']*1e4:5.1f}~{seg[-1]['margin']*1e4:5.1f}bp {len(seg):>4d}"
              f"{m*1e4:>10.1f}b"
              f"{sum(r['os_sharpe125'] for r in seg)/len(seg):>8.2f}"
              f"{sum(r['os_sharpe60'] for r in seg)/len(seg):>8.2f}"
              f"{sum(r['sharpe'] for r in seg)/len(seg):>7.2f}"
              f"{sum(r['fitness'] for r in seg)/len(seg):>6.2f}"
              f"{sum(1 for r in seg if r['os_sharpe125'] < 0)/len(seg):>6.0%}")

    # ---- 检验 5：Fitness 的同口径分位（对照组） ----
    print("\n=== 检验 5：Fitness 四分位 → OS 均值（对照） ===")
    s2 = sorted(rows, key=lambda r: r["fitness"])
    print(f"{'分位':22s}{'n':>4s}{'F中位':>8s}{'os125':>8s}{'os60':>8s}{'负OS':>7s}")
    for i in range(4):
        seg = s2[i * k:(i + 1) * k] if i < 3 else s2[3 * k:]
        if not seg:
            continue
        print(f"Q{i+1} {seg[0]['fitness']:5.2f}~{seg[-1]['fitness']:5.2f} {len(seg):>4d}"
              f"{sorted(r['fitness'] for r in seg)[len(seg)//2]:>8.2f}"
              f"{sum(r['os_sharpe125'] for r in seg)/len(seg):>8.2f}"
              f"{sum(r['os_sharpe60'] for r in seg)/len(seg):>8.2f}"
              f"{sum(1 for r in seg if r['os_sharpe125'] < 0)/len(seg):>6.0%}")

    # ---- 检验 6：只在高换手子样本里看 margin 的增量 ----
    print("\n=== 检验 6：TO>=0.125（Fitness 分母未封顶）子样本 ===")
    hi = [r for r in rows if r["turnover"] >= 0.125]
    lo = [r for r in rows if r["turnover"] < 0.125]
    for lab, seg in (("TO>=0.125", hi), ("TO<0.125", lo)):
        if len(seg) < 10:
            print(f"  {lab:12s} n={len(seg)} 样本不足")
            continue
        a, _ = spearman([r["margin"] for r in seg], [r["os_sharpe125"] for r in seg])
        b, _ = spearman([r["fitness"] for r in seg], [r["os_sharpe125"] for r in seg])
        print(f"  {lab:12s} n={len(seg):>3d}  ρ(margin,os125)={a:+.3f}  ρ(F,os125)={b:+.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
