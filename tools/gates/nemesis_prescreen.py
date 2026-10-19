# -*- coding: utf-8 -*-
"""照妖镜预筛：用 vector_neut 对「因子代理」正交化，判断信号是不是因子换皮。

背景（2026-10-18 实测）：`eps_q1_estimate_qoq_growth` 腿做到 S 1.89 后 prod 卡 0.7094，
用同数据集代理 `vector_neut(signal, eps_y1_cagr_2yr)` 正交化后 **S 从 1.89 崩到 0.62（−67%）**
⇒ 该信号的 60%+ PnL 就是增长因子，prod 0.75 不是"字段拥挤"而是"因子拥挤"，
任何参数/中性化微调都无效。据此确立纪律：

    S 掉幅  < 30%  → PASS：信号有独立 alpha，值得投入仿真/提交
    30%–50%        → WEAK：一半是因子，先做别的方向
    > 50%          → KILL：信号本体=该因子，**别再微调，直接换信息源**

用法（仓库根，必须用 $WQ_PY）：

    # ① 生成变体（不花仿真）：每条 signal × 每个 proxy 产一条 vector_neut
    $WQ_PY tools/gates/nemesis_prescreen.py --gen \
        --signals tracking/USA/candidates/nemesis_input.json \
        --proxies "eps_y1_cagr_2yr,eps_estimate_trend_slope_1yr" --json

    # ② 判定（输入 MCP harvest_multisim_alphas 的结果 JSON）
    $WQ_PY tools/gates/nemesis_prescreen.py --judge harvest.json

为什么用「同数据集代理」：跨数据集的 vector_neut 会让 alpha 变成 combined（破 ATOM），
同数据集代理既满足正交化又保持单一数据集。

⚠ 代理选择：代理必须是**已知因子**在该数据集里的投影（如增长用 CAGR / trend_slope、
规模用 consensus_value、动量用 trailing 估计）。选错代理会把真 alpha 误杀。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PASS_MAX = 0.30
WEAK_MAX = 0.50


def _split_neut(expr: str) -> tuple[str, str] | None:
    """`vector_neut(BASE, PROXY)` → (BASE, PROXY)；不是该形态返回 None。"""
    s = expr.strip()
    if not s.startswith("vector_neut(") or not s.endswith(")"):
        return None
    inner = s[len("vector_neut("): -1]
    depth, cut = 0, -1
    for i, ch in enumerate(inner):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            cut = i                      # 取最后一个顶层逗号：BASE 自身可能含逗号
    if cut < 0:
        return None
    base, proxy = inner[:cut].strip(), inner[cut + 1:].strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", proxy):
        return None
    return base, proxy


def cmd_gen(args) -> int:
    if not args.proxies:
        raise SystemExit("--gen 需要 --proxies（逗号分隔的同数据集因子代理字段）")
    proxies = [p.strip() for p in args.proxies.split(",") if p.strip()]
    if args.signals:
        raw = Path(args.signals).read_text(encoding="utf-8")
        signals = json.loads(raw) if raw.lstrip().startswith("[") else [l.strip() for l in raw.splitlines() if l.strip()]
    else:
        if not args.signal:
            raise SystemExit("--gen 需要 --signals 文件或 --signal 表达式")
        signals = [args.signal]

    exprs = [f"vector_neut({s.strip()}, {p})" for s in signals for p in proxies]
    if args.json:
        print(json.dumps({"expressions": exprs, "count": len(exprs), "proxies": proxies},
                         ensure_ascii=False, indent=2))
    else:
        print(f"# {len(exprs)} 条变体（{len(signals)} signal × {len(proxies)} proxy）")
        for e in exprs:
            print(e)
    return 0


def cmd_judge(args) -> int:
    data = json.loads(Path(args.judge).read_text(encoding="utf-8"))
    alphas = data.get("alphas") if isinstance(data, dict) else data
    if not isinstance(alphas, list):
        raise SystemExit("--judge 输入应为 harvest 输出（含 alphas 数组）")

    raw: dict[str, float] = {}
    neut: list[dict] = []
    for a in alphas:
        expr = str(a.get("expression") or a.get("code") or "")
        s = ((a.get("metrics") or {}).get("sharpe"))
        if not expr or s is None:
            continue
        pair = _split_neut(expr)
        if pair is None:
            raw[expr.strip()] = float(s)
        else:
            base, proxy = pair
            neut.append({"base": base, "proxy": proxy, "s": float(s),
                         "id": a.get("alpha_id") or a.get("id"), "expr": expr})

    if not neut:
        print("[nemesis] 没找到 vector_neut 变体；用 --gen 先生成再派发", file=sys.stderr)
        return 1

    rows = []
    for n in neut:
        s_raw = raw.get(n["base"])
        if s_raw is None or s_raw <= 0:
            continue
        drop = 1.0 - n["s"] / s_raw
        verdict = "PASS" if drop < PASS_MAX else ("WEAK" if drop < WEAK_MAX else "KILL")
        rows.append({**n, "s_raw": s_raw, "drop": drop, "verdict": verdict, "kept": n["s"] / s_raw})

    rows.sort(key=lambda r: (r["verdict"] != "PASS", r["drop"]))
    if args.json:
        print(json.dumps({"rows": rows, "thresholds": {"pass": PASS_MAX, "weak": WEAK_MAX}},
                         ensure_ascii=False, indent=2))
        return 0

    print(f"\n=== 照妖镜判定（掉幅 <{PASS_MAX:.0%} PASS / <{WEAK_MAX:.0%} WEAK / ≥{WEAK_MAX:.0%} KILL）===\n")
    print(f"{'代理':34} {'S_raw':>7} {'S_neut':>7} {'保留':>7} {'掉幅':>7}  {'判定':6} alpha")
    print("-" * 92)
    for r in rows:
        print(f"{r['proxy'][:34]:34} {r['s_raw']:>7.2f} {r['s']:>7.2f} "
              f"{r['kept']:>6.0%} {r['drop']:>6.0%}  {r['verdict']:6} {r['id'] or ''}")
    print()
    kills = [r for r in rows if r["verdict"] == "KILL"]
    if kills:
        print(f"⛔ {len(kills)} 条判定 KILL：信号本体就是该因子 ⇒ 停止微调，换信息源。")
    passed = [r for r in rows if r["verdict"] == "PASS"]
    if passed:
        print(f"✅ {len(passed)} 条 PASS：残差仍有 alpha，可投入仿真/提交。")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="照妖镜预筛（vector_neut 正交化判定）")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--gen", action="store_true", help="生成 vector_neut 变体表达式")
    g.add_argument("--judge", metavar="HARVEST_JSON", help="判定 harvest 结果 JSON")
    ap.add_argument("--signals", help="信号表达式文件（JSON 数组或每行一条）")
    ap.add_argument("--signal", help="单条信号表达式")
    ap.add_argument("--proxies", help="同数据集因子代理字段，逗号分隔")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    args = ap.parse_args()
    return cmd_gen(args) if args.gen else cmd_judge(args)


if __name__ == "__main__":
    sys.exit(main())
