# -*- coding: utf-8 -*-
"""l1_ladder.py — L1 时间导数层梯度读数（治「形态≠导数层」的系统性盲区）

背景（2026-10-24）：字段「形态」（是什么）与信号所在的「时间导数层」（在水平/速度/加速度
哪层）是两个正交维度。acquisition_model 的 global_company_size_percentile_rank：
  水平 lvl −0.24 → 一阶 d1 −0.94 → 二阶 d2 +0.83（符号翻转，信号只在加速度层）
若预筛只测水平层，会得到 −0.24 就判死，永远看不到 +0.83。

本工具把一个数据集的已回测 alpha 按「字段 × L1 层」排成矩阵，让符号翻转一眼可见。

用法：
    python tools/l1_ladder.py --multisim 40neIqz4kvahXrun4UrmI t0rKki14yS8Xs1h1GRfW1a
    python tools/l1_ladder.py --json cache/x.json     # [{"code":..,"metrics":{...}}]
"""
import argparse
import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

L1_ORDER = ["lvl", "d1", "d2", "ed", "ir", "dsp"]
L1_ZH = {"lvl": "水平", "d1": "一阶差分(速度)", "d2": "二阶差分(加速度)",
         "ed": "事件衰减", "ir": "信噪比", "dsp": "组内离散"}

# 已知字段名集合（用于从表达式里反提字段）
_OP_WORDS = {"rank", "add", "multiply", "divide", "subtract", "greater", "less", "and",
             "or", "not", "abs", "log", "exp", "sign", "min", "max", "sum", "std", "mean",
             "count", "scale", "power", "backfill", "delta", "decay", "ir", "zscore",
             "quantile", "winsorize", "hump", "reverse", "tail", "bucket", "trade_when",
             "if_else", "group_rank", "group_neutralize", "group_zscore", "group_mean",
             "vec_avg", "vec_sum", "vec_max", "vec_stddev", "ts_mean", "ts_delta",
             "ts_rank", "ts_quantile", "ts_zscore", "ts_scale", "ts_std_dev", "ts_sum",
             "ts_decay_linear", "ts_ir", "ts_corr", "ts_delay", "ts_av_diff", "pasteurize",
             "inverse", "days_from_last_change", "signed_power", "vector_neut",
             "regression_neut", "ts_regression", "ts_backfill", "ts_backfill"}


def l1_of(code):
    """表达式 → L1 层。按最外层的差分/事件结构判。"""
    c = code
    if re.search(r"ts_delta\s*\(\s*ts_delta", c):
        return "d2"
    if "ts_delta(" in c:
        return "d1"
    if "ts_decay_linear(" in c:
        return "ed"
    if "ts_ir(" in c:
        return "ir"
    if "vec_stddev(" in c or "ts_std_dev(" in c and "ts_delta" not in c:
        return "dsp"
    return "lvl"


def field_of(code):
    """粗提表达式里的字段名（取最长的小写标识符，排除算子名）。"""
    ids = re.findall(r"[a-z][a-z0-9_]{5,}", code)
    ids = [i for i in ids if i not in _OP_WORDS and not i.startswith("ts_")]
    if not ids:
        return "?"
    return max(ids, key=len)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--multisim", nargs="*", default=None, help="multisim id 列表")
    ap.add_argument("--json", dest="jf", default=None, help="alpha JSON 文件")
    ap.add_argument("--min-abs", type=float, default=0.0, help="只显示 |S|>=此值的格子")
    a = ap.parse_args()

    alphas = []
    if a.jf:
        alphas = json.load(open(a.jf, encoding="utf-8"))
    elif a.multisim:
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
        import _pyenv
        _pyenv.bootstrap_paths()
        from brain_api import brain_client
        import asyncio

        async def pull():
            await brain_client.ensure_authenticated()
            base = brain_client.base_url
            out = []
            for mid in a.multisim:
                r = await brain_client._request("GET", f"{base}/simulations/{mid}")
                for sid in (r.json().get("children") or []):
                    rr = await brain_client._request("GET", f"{base}/simulations/{sid}")
                    jj = rr.json()
                    al = jj.get("alpha")
                    aid = al.get("id") if isinstance(al, dict) else al
                    if not aid:
                        continue
                    da = await brain_client._request("GET", f"{base}/alphas/{aid}")
                    out.append(da.json())
            return out

        alphas = asyncio.run(pull())
    else:
        ap.error("需要 --multisim 或 --json")

    # 字段 × L1 → max S
    cell = collections.defaultdict(list)
    for al in alphas:
        code = al.get("regular") or {}
        code = code.get("code") if isinstance(code, dict) else (al.get("code") or "")
        m = al.get("is") or {}
        s = m.get("sharpe")
        if s is None or not code:
            continue
        cell[(field_of(code), l1_of(code))].append(s)

    if not cell:
        print("没有可用读数")
        return
    fields = sorted({f for f, _ in cell},
                     key=lambda f: -max(abs(x) for (ff, _), v in cell.items()
                                        if ff == f for x in v))
    print(f'{"字段":<44}' + "".join(f"{L1_ZH.get(l, l):>16}" for l in L1_ORDER))
    print("-" * (44 + 16 * len(L1_ORDER)))
    for f in fields:
        row = f"{f[:42]:<44}"
        for l in L1_ORDER:
            v = cell.get((f, l))
            if not v:
                row += f"{'—':>16}"
            else:
                mx = max(v, key=abs)
                mark = "" if abs(mx) >= a.min_abs else ""
                row += f"{mx:>15.2f}{mark}"
        print(row)
    print()
    # 符号翻转提示
    flips = []
    for f in fields:
        vals = {l: max(cell[(f, l)], key=abs) for l in L1_ORDER if (f, l) in cell}
        if len(vals) >= 2 and len({(v > 0) for v in vals.values()}) > 1:
            flips.append((f, vals))
    if flips:
        print("⚠ 符号翻转（同字段跨 L1 层正负相反 ⇒ 信号只在特定导数层，勿用单层判死）：")
        for f, vals in flips:
            print(f"   {f[:40]:42s} " +
                  " ".join(f"{l}={v:+.2f}" for l, v in sorted(vals.items())))
    else:
        print("未检出符号翻转。")


if __name__ == "__main__":
    main()
