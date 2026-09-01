# -*- coding: utf-8 -*-
"""field_axis.py - 字段信息轴自动识别（P0-B，2026-08-31）。

背景：field-quality 先验说"数据集 top 字段按 alphaCount 排序后，前缀聚类揭示
数据集的主导经济轴"（如 analyst14 的 top 字段是债务/资产轴而非 EPS 轴），
但该识别过去靠人工看。本工具把识别自动化：
  get_datafields 输出 -> alphaCount 降序取 top N -> 字段名词根聚类 -> 输出 2-3 个主导信息轴。

用法:
  # 从 get_datafields 保存的 JSON 识别单个数据集的轴
  python tools/field_axis.py --input data_ref/all_fields.json --dataset analyst14

  # 不指定 dataset：扫描全部数据集，输出每个数据集的 top 轴（--all）
  python tools/field_axis.py --input data_ref/all_fields.json --all

  # 自定义 top 数与最少轴占比
  python tools/field_axis.py --input xxx.json --dataset fnd94 --top-n 40 --min-axis-share 0.15

输入格式兼容两种:
  1. {field_key: {dataset: "...", alphaCount: N, userCount: N, ...}}   # get_datafields 原始输出
  2. {dataset_id: [field_name, ...]}                                   # 简单清单
"""
import argparse
import collections
import json
import os
import re
import sys

# 常见词根 -> 中文经济语义（未命中原样输出英文）
_ROOT_CN = {
    "debt": "债务", "ndebt": "净债务", "ebitda": "息税折旧摊销前利润",
    "nav": "资产净值", "asset": "资产", "book": "账面价值", "equity": "权益",
    "earn": "盈利", "eps": "每股盈利", "profit": "利润", "income": "收益",
    "rev": "营收", "revenue": "营收", "sales": "销售", "gross": "毛利",
    "margin": "利润率", "cash": "现金流", "cf": "现金流", "freecash": "自由现金流",
    "growth": "增长", "growthrate": "增速", "yield": "收益率", "dividend": "股息",
    "est": "预期", "estimate": "预期", "target": "目标价", "rec": "评级",
    "score": "评分", "rank": "排名", "ratio": "比率", "percentile": "分位",
    "mean": "均值", "median": "中位数", "stdev": "标准差", "std": "标准差",
    "beta": "贝塔", "vol": "波动", "volatility": "波动", "momentum": "动量",
    "price": "价格", "return": "收益", "ret": "收益", "close": "收盘价",
    "volume": "成交量", "turnover": "换手", "amihud": "非流动性", "liquidity": "流动性",
    "short": "卖空", "insider": "内部人", "buy": "买入", "sell": "卖出",
    "sentiment": "情绪", "news": "新闻", "count": "计数", "num": "数量",
    "q": "分位", "quantile": "分位", "value": "价值", "mkt": "市值",
    "size": "规模", "cap": "市值", "pe": "市盈率", "pb": "市净率",
    "ps": "市销率", "roa": "资产回报率", "roe": "净资产回报率", "roic": "投入资本回报率",
    "margin_op": "营业利润率", "op": "营业", "accrual": "应计", "lev": "杠杆",
    "analyst": "分析师", "coverage": "覆盖", "revision": "修正", "delta": "变动",
}

_GENERIC_ROOTS = {
    "value", "mean", "median", "count", "num", "ratio", "score", "rank",
    "delta", "diff", "change", "percent", "pct", "ind", "indicator", "metric",
}


def _iter_dataset_fields(data):
    """从输入 JSON 解析 (dataset, field_name) 迭代器。

    兼容两种格式：
      1. {field_key: {dataset:..., alphaCount:..., userCount:...}}
      2. {dataset_id: [field_name, ...]}
    """
    for key, val in data.items():
        if isinstance(val, dict):
            ds = val.get("dataset", val.get("dataset_id", ""))
            if ds:
                yield ds, key, val
        elif isinstance(val, list):
            for f in val:
                if isinstance(f, str):
                    yield key, f, {}


def _field_tokens(field_name: str, dataset_id: str) -> list:
    """字段名词根提取：去数据集前缀、去数字、按 _ 分段，滤通用词。"""
    name = field_name.lower()
    # 去数据集前缀：WQ 字段标准命名是 <缩写><版本>_<语义>（如 anl14_mean_ndebt_fy1）。
    # 不依赖 dataset_id 精确匹配（anl14 vs analyst14 是常见对应），
    # 只要首 token 形如 <1-6字母><数字>_ 就剥离。
    m = re.match(r"^[a-z]{1,6}\d+_(.+)", name)
    if m:
        name = m.group(1)
    parts = re.split(r"[\d_\.]+", name)
    tokens = []
    for p in parts:
        if len(p) < 3:
            continue
        if p in _GENERIC_ROOTS:
            continue
        tokens.append(p)
    return tokens


def identify_axes(fields_meta, top_n=30, min_axis_share=0.2, max_axes=3):
    """识别数据集主导信息轴。

    fields_meta: list of dict {name, alpha_count, user_count, ...}（按 alphaCount 降序）
    返回 list of dict:
      {root, root_cn, field_count, total_alpha, share,
       fields: [(field, alpha_count), ...]}
    """
    if not fields_meta:
        return []
    ranked = sorted(fields_meta, key=lambda f: -f.get("alpha_count", 0))
    top = ranked[:top_n]
    if not top:
        return []
    total_alpha = sum(f.get("alpha_count", 0) for f in top)

    root_buckets = collections.defaultdict(list)  # root -> [(field, alpha), ...]
    for f in top:
        name = f.get("name", "")
        toks = _field_tokens(name, f.get("dataset", ""))
        if not toks:
            root_buckets["other"].append((name, f.get("alpha_count", 0)))
            continue
        # 字段的轴 = 最有信息量的词根（非通用）优先取第一个有意义的 token
        root_buckets[toks[0]].append((name, f.get("alpha_count", 0)))

    axes = []
    for root, items in root_buckets.items():
        field_cnt = len(items)
        ax_alpha = sum(a for _, a in items)
        share = ax_alpha / total_alpha if total_alpha else 0
        if share < min_axis_share:
            continue
        axes.append({
            "root": root,
            "root_cn": _ROOT_CN.get(root, ""),
            "field_count": field_cnt,
            "total_alpha": ax_alpha,
            "share": round(share, 3),
            "fields": sorted(items, key=lambda x: -x[1])[:6],
        })
    axes.sort(key=lambda x: -x["share"])
    return axes[:max_axes]


def _alpha_of(field_key, val):
    for k in ("alphaCount", "alpha_count", "count"):
        if k in val:
            try:
                return int(val[k])
            except (TypeError, ValueError):
                return 0
    return 0


def main():
    ap = argparse.ArgumentParser(description="字段信息轴自动识别（P0-B）")
    ap.add_argument("--input", required=True, help="get_datafields 输出 JSON 或字段清单 JSON")
    ap.add_argument("--dataset", default=None, help="只分析该数据集（缺省打印全部）")
    ap.add_argument("--all", action="store_true", help="打印所有数据集的 top 轴")
    ap.add_argument("--top-n", type=int, default=30, help="按 alphaCount 取 top N 字段（默认 30）")
    ap.add_argument("--min-axis-share", type=float, default=0.2,
                    help="轴最小占比（默认 0.2 = 轴字段 alphaCount 合计占 top N 的 20%%）")
    a = ap.parse_args()

    if not os.path.isfile(a.input):
        print(f"[field_axis] 输入文件不存在: {a.input}", file=sys.stderr)
        sys.exit(1)
    data = json.load(open(a.input, encoding="utf-8"))

    # 按数据集聚合
    ds_map = collections.defaultdict(list)  # dataset -> [field_meta, ...]
    for ds, fname, val in _iter_dataset_fields(data):
        ds_map[ds].append({
            "name": fname, "alpha_count": _alpha_of(fname, val),
            "user_count": val.get("userCount", val.get("user_count", 0)) if isinstance(val, dict) else 0,
            "dataset": ds,
        })

    targets = [a.dataset] if a.dataset else sorted(ds_map)
    printed = 0
    for ds in targets:
        metas = ds_map.get(ds)
        if not metas:
            print(f"[field_axis] 数据集 {ds} 无字段记录")
            continue
        axes = identify_axes(metas, top_n=a.top_n, min_axis_share=a.min_axis_share)
        n_f = len(metas)
        print(f"\n=== {ds}（共 {n_f} 字段，按 alphaCount top {a.top_n} 聚类）===")
        if not axes:
            print("  未能识别主导信息轴（字段词根分散或均低于占比阈值）")
        for i, ax in enumerate(axes, 1):
            cn = f"（{ax['root_cn']}）" if ax["root_cn"] else ""
            print(f"  轴{i}: {ax['root']}{cn} — {ax['field_count']} 字段, "
                  f"alphaCount 合计 {ax['total_alpha']} ({ax['share']:.0%})")
            for fn, ac in ax["fields"]:
                print(f"      {fn} (α={ac})")
        printed += 1
        if not a.all and printed >= 1:
            break


if __name__ == "__main__":
    main()