#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""basket_diversity_gate.py — 篮子簇识别 + 结构多样性审查（防同源充数）。

背景：篮子两两互相关阈值由 0.5 放宽到 config.BASKET_MUTUAL_CORR_MAX(0.7) 后，
仅靠「两两 < 阈值」不足以防止同一收益源重复充数——两颗 alpha 可能 0.65 相关
（同数据集/同机制）仍过阈。本闸做两层审查：

  D1 簇识别：把 |corr| > 阈值 的 alpha 连成连通分量(cluster)，点名「近亲簇」。
     放宽阈值后允许近亲共存，但必须显式报告，供人工判断是否真独立。
  D2 结构多样性：统计篮内数据集/机制族分布，同数据集超过
     config.BASKET_DATASET_CONCENTRATION_WARN 颗 → WARN（同源风险）。

阈值默认读 config.BASKET_MUTUAL_CORR_MAX（单一事实源），--threshold 可覆盖。
默认只报告(WARN 不阻断)；--strict 时结构多样性违规升为 FAIL(exit 1)。

用法：
    python tools/gates/basket_diversity_gate.py --matrix corr.json --meta meta.json
    python tools/gates/basket_diversity_gate.py --matrix corr.json --meta meta.json --threshold 0.6 --strict
输入：
    matrix = {id: {other_id: corr}}（对称，含自身=1 亦可）
    meta   = {id: {"dataset": "...", "family": "...", ...}}
退出码：0 通过/仅报告；1 --strict 且结构多样性硬违规；2 输入/配置错。
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

try:
    from wqb import config as wqb_config
    from wqb.paths import find_repo_root
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    from wqb import config as wqb_config
    from wqb.paths import find_repo_root

ROOT = find_repo_root()


def _corr(matrix, x, y):
    v = (matrix.get(x) or {}).get(y)
    if not isinstance(v, (int, float)):
        v = (matrix.get(y) or {}).get(x)
    return abs(v) if isinstance(v, (int, float)) else 0.0


def identify_clusters(ids, matrix, threshold):
    """|corr| > threshold 连边，求连通分量；只返回 size>=2 的近亲簇。"""
    ids = list(ids)
    adj = {i: set() for i in ids}
    for a_idx, x in enumerate(ids):
        for y in ids[a_idx + 1:]:
            if _corr(matrix, x, y) > threshold:
                adj[x].add(y)
                adj[y].add(x)
    seen, clusters = set(), []
    for x in ids:
        if x in seen or not adj[x]:
            continue
        stack, comp = [x], []
        seen.add(x)
        while stack:
            cur = stack.pop()
            comp.append(cur)
            for nb in adj[cur]:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        if len(comp) >= 2:
            clusters.append(sorted(comp))
    return clusters


def structural_diversity(ids, meta, warn_per_dataset):
    """统计数据集/机制族分布，标记同数据集过度集中。"""
    ds_count, fam_count = {}, {}
    for i in ids:
        m = meta.get(i) or {}
        ds = m.get("dataset") or m.get("dataset_id") or "unknown"
        fam = m.get("family") or m.get("mechanism_family") or "unknown"
        ds_count[ds] = ds_count.get(ds, 0) + 1
        fam_count[fam] = fam_count.get(fam, 0) + 1
    over = [{"dataset": d, "count": n} for d, n in sorted(ds_count.items(), key=lambda kv: -kv[1])
            if d != "unknown" and n > warn_per_dataset]
    return {"dataset_counts": ds_count, "family_counts": fam_count,
            "over_concentrated": over, "n_datasets": len([d for d in ds_count if d != "unknown"]),
            "n_families": len([f for f in fam_count if f != "unknown"])}


def review_basket(ids, matrix, meta, threshold=None, warn_per_dataset=None, strict=False):
    threshold = wqb_config.BASKET_MUTUAL_CORR_MAX if threshold is None else threshold
    warn_per_dataset = (wqb_config.BASKET_DATASET_CONCENTRATION_WARN
                        if warn_per_dataset is None else warn_per_dataset)
    ids = list(ids)
    clusters = identify_clusters(ids, matrix, threshold)
    div = structural_diversity(ids, meta, warn_per_dataset)
    warnings, errors = [], []
    for cl in clusters:
        warnings.append(f"[D1 近亲簇] {cl} 两两|corr|>{threshold}（放宽阈值后允许共存，须人工确认真独立）")
    for oc in div["over_concentrated"]:
        msg = f"[D2 同源集中] 数据集 {oc['dataset']} 占 {oc['count']} 颗 > 警戒 {warn_per_dataset}"
        (errors if strict else warnings).append(msg)
    return {"ok": not errors, "threshold": threshold, "n": len(ids),
            "clusters": clusters, "diversity": div,
            "warnings": warnings, "errors": errors, "strict": strict}


def main():
    ap = argparse.ArgumentParser(description="篮子簇识别 + 结构多样性审查（防同源充数）")
    ap.add_argument("--matrix", required=True, help="相关性矩阵 JSON {id:{id:corr}}")
    ap.add_argument("--meta", required=True, help="alpha 元信息 JSON {id:{dataset,family}}")
    ap.add_argument("--ids", help="逗号分隔的篮子 id（缺省=meta 全部键）")
    ap.add_argument("--threshold", type=float, default=None, help="互相关阈值（缺省读 config）")
    ap.add_argument("--warn-per-dataset", type=int, default=None, help="同数据集警戒颗数（缺省读 config）")
    ap.add_argument("--strict", action="store_true", help="结构多样性违规升为 FAIL")
    args = ap.parse_args()
    try:
        matrix = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
        meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"输入读取失败: {e}", file=sys.stderr)
        return 2
    ids = args.ids.split(",") if args.ids else list(meta.keys())
    r = review_basket(ids, matrix, meta, args.threshold, args.warn_per_dataset, args.strict)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
