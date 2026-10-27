# -*- coding: utf-8 -*-
"""webdata_scan.py — 离线扫描 WebData 包的字段年鉴，筛「有信号苗子」的字段。

## 数据格式（已逆向）
``research-data/WebData_<date>_<ver>/data/<dataset>_<REGION>_<universe>_Delay<N>.bin``
= **zlib 压缩的 msgpack dict**：
```
{ "<field>": {"year":[...], "LongCount":[...], "ShortCount":[...], "Coverage":[...],
              "CoverageRatio":[...], "PositiveValues":[...], "NegativeValues":[...],
              "IndicativePositiveRatio":[...], "IndicativeNegativeRatio":[...],
              "IntegerStatus":[...], "absValueBetween1and0ratio":[...],
              "skenewss":[...], "kurtosis":[...], "frequency":[...],
              "yearly_distribution":[...]} }
```
⚠ **不含 Sharpe/returns** —— 这是字段统计画像，不是业绩。真正的强度必须上平台跑裸强度探针
（SOP：`|S| < 0.5 ⇒ kill`）。本工具只做**上平台前的字段质量初筛**，替你把 2.4 万字段砍到几百。

## 两类候选（已按实测分布设计，2026-10-27）
- **A 类「直接可用」**：`posratio ∈ (0.45, 0.95)`（有正有负 ⇒ 有方向信息）
  + `abs01 ≥ 0.3`（已归一化）+ `covRatio ≥ 0.7` + 覆盖稳定
  ⇒ 直接 `rank(F)` / `zscore(F)` 就有方向，探针首选。
- **B 类「需 transform」**：`posratio > 0.95`（全正，多为价格/存量/规模）
  + `covRatio ≥ 0.7`
  ⇒ 必须差分/比率/残差化（`ts_delta`、`divide`、`ts_regression`）才出信号。

## 实测分布（23,811 字段，USA Delay1，供参考）
| 指标 | mean | p10 | p50 | p90 |
|---|---|---|---|---|
| CoverageRatio | 0.713 | 0.297 | 0.805 | 0.970 |
| IndicativePositiveRatio | 0.833 | 0.463 | **1.000** | 1.000 |
| absValueBetween1and0ratio | 2116 | 0.000 | **0.084** | 0.997 |
| frequency=daily 占比 | **28.3%** | | | |

## 用法
```bash
python tools/webdata_scan.py --region USA --out output_report/webdata_usa.csv
python tools/webdata_scan.py --region USA --class A --top 60      # 只看 A 类前 60
python tools/webdata_scan.py --list-files                          # 列出包内全部数据集
```
"""

from __future__ import annotations

import argparse
import csv
import glob
import os
import statistics as st
import sys
import zlib
from typing import Any, Dict, List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PKG = os.path.join(ROOT, "research-data", "WebData_20260219_V0.10.9", "data")


def _mean(vals) -> float:
    v = [x for x in vals or [] if isinstance(x, (int, float))]
    return float(st.mean(v)) if v else 0.0


def _min(vals) -> float:
    v = [x for x in vals or [] if isinstance(x, (int, float))]
    return float(min(v)) if v else 0.0


def load_bin(path: str) -> Dict[str, Any]:
    try:
        import msgpack
    except ImportError:
        raise SystemExit("需要 msgpack：pip install msgpack")
    with open(path, "rb") as f:
        raw = f.read()
    return msgpack.unpackb(zlib.decompress(raw), raw=False, strict_map_key=False)


def profile_field(d: Dict[str, Any]) -> Dict[str, Any]:
    """把一个字段的年鉴压成一行画像。"""
    covr = d.get("CoverageRatio") or []
    posr = d.get("IndicativePositiveRatio") or []
    negr = d.get("IndicativeNegativeRatio") or []
    abs01 = d.get("absValueBetween1and0ratio") or []
    ints = d.get("IntegerStatus") or []
    cov = d.get("Coverage") or []
    freq = d.get("frequency") or []
    yrs = d.get("year") or []

    covr_m, covr_min = _mean(covr), _min(covr)
    posr_m = _mean(posr)
    abs01_m = _mean(abs01)
    ints_m = _mean(ints)
    cov_m = _mean(cov)

    is_daily = bool(freq) and str(freq[0]).lower() == "daily"
    freq_val = str(freq[0]).lower() if freq else "unknown"

    # ---- 分类 ----
    # A：有正有负 + 已归一化 ⇒ 直接 rank/zscore 有方向
    cls = "reject"
    if covr_m >= 0.7 and covr_min >= 0.5 and len(yrs) >= 8:
        if 0.45 < posr_m < 0.95 and abs01_m >= 0.3 and ints_m < 0.5:
            cls = "A"
        elif posr_m >= 0.95 and ints_m < 0.5:
            cls = "B"
        elif posr_m <= 0.45 and abs01_m >= 0.3 and ints_m < 0.5:
            cls = "A"          # 以负值为主，同样有方向（方向取负即可）
        else:
            cls = "C"          # 覆盖够但尺度/形态需额外处理

    # ---- 苗子分（0-100，只用于排序，不代表信号强度）----
    score = 0.0
    score += 40 * min(1.0, covr_m)                       # 覆盖
    score += 20 * min(1.0, max(0.0, covr_min) / 0.7)     # 覆盖稳定性
    # 方向性：|pos-0.5|*2 越接近 1 越有方向，但 全正(≈1) 需 transform ⇒ 给 0.7 折
    direct = abs(posr_m - 0.5) * 2
    score += 20 * (direct * (1.0 if cls == "A" else 0.7))
    score += 10 * min(1.0, abs01_m)                      # 归一化程度
    score += 10 * (1.0 if is_daily else 0.5)             # 频次（日频更易挖）
    if ints_m >= 0.5:
        score *= 0.6                                     # 整数型大幅折价
    if len(yrs) < 8:
        score *= 0.5                                     # 历史短折价

    return {
        "field": None,      # 由调用方填
        "class": cls,
        "score": round(score, 2),
        "cov_ratio": round(covr_m, 3),
        "cov_ratio_min": round(covr_min, 3),
        "coverage": int(cov_m),
        "pos_ratio": round(posr_m, 3),
        "abs01": round(abs01_m, 3),
        "int_status": round(ints_m, 3),
        "freq": freq_val,
        "years": len(yrs),
    }


def scan(pkg: str, region: str, delay: int = 1) -> List[Dict[str, Any]]:
    pat = os.path.join(pkg, f"*_{region}_*_Delay{delay}.bin")
    files = sorted(glob.glob(pat))
    if not files:
        raise SystemExit(f"未找到匹配文件：{pat}")
    rows: List[Dict[str, Any]] = []
    for f in files:
        fn = os.path.basename(f)
        ds = fn.split(f"_{region}_")[0]
        try:
            obj = load_bin(f)
        except Exception as e:  # noqa: BLE001
            print(f"[skip] {fn}: {type(e).__name__} {e}", file=sys.stderr)
            continue
        for fname, d in obj.items():
            if not isinstance(d, dict):
                continue
            r = profile_field(d)
            r["field"] = fname
            r["dataset"] = ds
            r["file"] = fn
            rows.append(r)
    return rows


def summarize(rows: List[Dict[str, Any]]) -> str:
    by_ds: Dict[str, Dict[str, int]] = {}
    for r in rows:
        s = by_ds.setdefault(r["dataset"], {"n": 0, "A": 0, "B": 0, "C": 0, "reject": 0,
                                            "best": 0.0})
        s["n"] += 1
        s[r["class"]] += 1
        s["best"] = max(s["best"], r["score"])
    out = [f"{'dataset':16s} {'fields':>7s} {'A':>5s} {'B':>5s} {'C':>5s} {'rej':>6s} {'best':>6s}",
           "-" * 60]
    for ds in sorted(by_ds, key=lambda k: -by_ds[k]["A"]):
        s = by_ds[ds]
        out.append(f"{ds:16s} {s['n']:>7} {s['A']:>5} {s['B']:>5} {s['C']:>5} "
                   f"{s['reject']:>6} {s['best']:>6.1f}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkg", default=DEFAULT_PKG)
    ap.add_argument("--region", default="USA")
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--out", default="")
    ap.add_argument("--class", dest="cls", default="", choices=["A", "B", "C", "reject", ""])
    ap.add_argument("--top", type=int, default=0, help="只打印前 N 条（0=全部汇总）")
    ap.add_argument("--min-score", type=float, default=0.0)
    ap.add_argument("--list-files", action="store_true")
    a = ap.parse_args()

    if a.list_files:
        for f in sorted(glob.glob(os.path.join(a.pkg, "*.bin"))):
            print(os.path.basename(f))
        return 0

    rows = scan(a.pkg, a.region, a.delay)
    print(f"[scan] {a.region} Delay{a.delay} 字段 {len(rows)} 个")
    print(summarize(rows))
    n_a = sum(1 for r in rows if r["class"] == "A")
    n_b = sum(1 for r in rows if r["class"] == "B")
    print(f"\n[A 类·直接可用] {n_a} 个    [B 类·需 transform] {n_b} 个")

    sel = [r for r in rows if (not a.cls or r["class"] == a.cls)
           and r["score"] >= a.min_score]
    sel.sort(key=lambda r: -r["score"])
    if a.top:
        print(f"\n{'field':44s} {'ds':12s} {'cls':4s} {'score':>6s} {'cov':>5s} {'covmin':>6s} "
              f"{'pos':>5s} {'abs01':>6s} {'freq':>8s}")
        for r in sel[:a.top]:
            print(f"{r['field'][:44]:44s} {r['dataset'][:12]:12s} {r['class']:4s} "
                  f"{r['score']:>6.1f} {r['cov_ratio']:>5.2f} {r['cov_ratio_min']:>6.2f} "
                  f"{r['pos_ratio']:>5.2f} {r['abs01']:>6.3f} {r['freq']:>8s}")

    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        cols = ["field", "dataset", "class", "score", "cov_ratio", "cov_ratio_min", "coverage",
                "pos_ratio", "abs01", "int_status", "freq", "years", "file"]
        with open(a.out, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in sorted(rows, key=lambda x: -x["score"]):
                w.writerow({k: r.get(k) for k in cols})
        print(f"\n[write] {a.out} ({len(rows)} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
