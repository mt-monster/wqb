#!/usr/bin/env python3
"""Generate a Markdown summary report from stage results.

Usage:
    python generate_md_report.py glb_second [--output REPORT_glb_second.md]

Reads:
    cache/results_<tag>.jsonl
    analysis/top_tracker_<tag>.json (if exists)

Writes:
    analysis/REPORT_<tag>.md
"""

import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE_DIR, "cache")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# ============================================================
# Helpers
# ============================================================
def read_results(tag):
    path = os.path.join(CACHE, f"results_{tag}.jsonl")
    if not os.path.exists(path):
        return []
    results = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def load_tracker(tag):
    path = os.path.join(ANALYSIS_DIR, f"top_tracker_{tag}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def extract_field(expr):
    """Extract the innermost data field name from a nested expression.
    
    e.g. group_neutralize(winsorize(ts_backfill(anl15_s_cal_fy2_6m_chg, 120), std=4), densify(market))
         → 'anl15_s_cal_fy2_6m_chg'
    """
    known_ops = {
        'group_neutralize', 'group_zscore', 'group_rank',
        'winsorize', 'ts_backfill', 'densify', 'industry_neutralize',
        'sector_neutralize', 'market_neutralize', 'zscore', 'rank',
        'normalize', 'scale', 'ts_delay', 'ts_mean', 'ts_std', 'ts_min',
        'ts_max', 'ts_cov', 'ts_corr', 'truediv', 'log', 'sign', 'abs',
        'cap', 'sign', 'sqrt', 'pow', 'rank', 'neutralize',
        'trade_when', 'condition', 'max', 'min', 'if', 'else',
        'ts_sum', 'ts_regslope', 'ts_regress', 'ts_delta', 'ts_arg_max',
        'ts_arg_min', 'group_mean', 'group_std', 'group_zscore',
        'group_rank', 'group_neutralize', 'group_median', 'group_sum',
        'group_min', 'group_max', 'group_first', 'group_last',
        'group_ts', 'group_lag', 'group_delta', 'group_cov', 'group_corr',
        'industry_zscore', 'industry_rank', 'industry_neutralize',
        'sector_zscore', 'sector_rank', 'sector_neutralize',
        'market_zscore', 'market_rank', 'market_neutralize',
        'country_zscore', 'country_rank', 'country_neutralize',
        'bottom_n', 'top_n', 'quantile', 'bucket', 'sigtype',
        'market', 'sector', 'industry', 'country', 'std', 'half_life',
        'lookback', 'period', 'window', 'days',
    }
    import re
    tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expr)
    for t in tokens:
        if t not in known_ops and not t.startswith('is_') and not t.startswith('sharpe'):
            # Check if it looks like a field (contains underscore and digits)
            if '_' in t and any(c.isdigit() for c in t):
                return t
    return expr.split('(')[0].strip()


def bar(pct, width=12):
    return '█' * max(1, int(pct / 100 * width)) + '░' * max(0, width - int(pct / 100 * width))


def detect_op(expr):
    if 'group_neutralize' in expr:
        return 'group_neutralize'
    elif 'group_zscore' in expr:
        return 'group_zscore'
    elif 'group_rank' in expr:
        return 'group_rank'
    return '?'


def detect_group(expr):
    if 'densify(market)' in expr or 'market_neutralize' in expr:
        return 'market'
    if 'densify(sector)' in expr or 'sector_neutralize' in expr:
        return 'sector'
    if 'densify(industry)' in expr or 'industry_neutralize' in expr:
        return 'industry'
    return '?'


# ============================================================
# Report generation
# ============================================================
def generate_md(tag, output=None):
    results = read_results(tag)
    valid = [r for r in results if r.get("is", {}).get("sharpe") is not None]
    tracker = load_tracker(tag)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    if not valid:
        with open(output or os.path.join(ANALYSIS_DIR, f"REPORT_{tag}.md"), "w", encoding="utf-8") as f:
            f.write(f"# {tag} — 无有效数据\n")
        return

    valid.sort(key=lambda r: abs(r["is"]["sharpe"]), reverse=True)
    sharpes = [abs(r["is"]["sharpe"]) for r in valid]
    n = len(valid)
    mean_s = sum(sharpes) / n
    max_s = max(sharpes)
    p50_s = sorted(sharpes)[n // 2]
    min_s = min(sharpes)

    turnovers = [r["is"].get("turnover", 0) for r in valid]
    mean_tur = sum(turnovers) / n if turnovers else 0

    # ---- Top 5 unique by expression ----
    seen = set()
    top5 = []
    for r in valid:
        expr = r["expression"]
        if expr not in seen:
            seen.add(expr)
            top5.append(r)
            if len(top5) >= 5:
                break

    # ---- Tracker stats ----
    report_count = tracker["report_count"] if tracker else 0
    field_counts = tracker["field_counts"] if tracker else {}
    op_counts = tracker["op_counts"] if tracker else {}
    combo_counts = tracker.get("combo_counts", {}) if tracker else {}

    # ---- Region stats from latest valid ----
    def region_mean(key):
        vals = [r["is"].get(key, 0) for r in valid if r["is"].get(key) is not None]
        return sum(vals) / len(vals) if vals else 0

    amer_m = region_mean("sharpe_glbAmer")
    apac_m = region_mean("sharpe_glbApac")
    emea_m = region_mean("sharpe_glbEmea")

    # ---- Region sign consistency ----
    def is_consistent(r):
        a = r["is"].get("sharpe_glbAmer", 0)
        p = r["is"].get("sharpe_glbApac", 0)
        e = r["is"].get("sharpe_glbEmea", 0)
        if a is None or p is None or e is None:
            return False
        return (a > 0 and p > 0 and e > 0) or (a < 0 and p < 0 and e < 0)

    consistent_count = sum(1 for r in valid if is_consistent(r))

    # ---- Histogram ----
    bins = []
    if n > 0:
        lo, hi = min_s, max_s
        bw = (hi - lo) / 10
        for i in range(10):
            bl = lo + i * bw
            br = lo + (i + 1) * bw
            cnt = sum(1 for s in sharpes if bl <= s < br)
            if i == 9:
                cnt = sum(1 for s in sharpes if bl <= s <= br)
            bins.append((bl, br, cnt))

    # ---- Robustness ----
    submittable = sum(1 for r in valid if abs(r["is"]["sharpe"]) >= 1.58 and r["is"].get("fitness", 0) >= 1.0)

    # =============== BUILD MARKDOWN ===============
    lines = []
    a = lines.append

    a(f"# {tag.upper()} Stage 因子归因分析报告 (Markdown)")
    a(f"")
    a(f"> **生成时间**: {now}")
    a(f"> **文件来源**: `cache/results_{tag}.jsonl`")
    a(f"> **报告路径**: `analysis/REPORT_{tag}.md`")
    a(f"")
    a(f"---")
    a(f"")
    a(f"## 1. 数据概览")
    a(f"")
    a(f"| 指标 | 值 |")
    a(f"|------|-----|")
    a(f"| 有效候选 | **{n}** |")
    a(f"| Mean\\|S\\| | {mean_s:.3f} |")
    a(f"| Max\\|S\\| | **{max_s:.3f}** |")
    a(f"| P50\\|S\\| | {p50_s:.3f} |")
    a(f"| Min\\|S\\| | {min_s:.3f} |")
    a(f"| Mean Turnover | {mean_tur:.4f} ({mean_tur*100:.1f}%) |")
    a(f"| 三区同号 | {consistent_count}/{n} ({consistent_count/n*100:.1f}%) |")
    a(f"")
    a(f"### Sharpe 分布直方图")
    a(f"")
    a(f"```")
    a(f"|S| 范围          数量")
    for bl, br, cnt in bins:
        bar_str = '█' * cnt if cnt > 0 else ''
        a(f"[{bl:+.3f}, {br:+.3f}) {bar_str} ({cnt})")
    a(f"```")
    a(f"")
    a(f"---")
    a(f"")
    a(f"## 2. 累计 Top 5 候选")
    a(f"")
    a(f"| # | \\|S\\| | 算子 | 分组 | Fit | Margin | Field |")
    a(f"|---|------|------|------|-----|--------|-------|")
    for i, r in enumerate(top5, 1):
        expr = r["expression"]
        ism = r["is"]
        op = detect_op(expr)
        grp = detect_group(expr)
        fit = ism.get("fitness", 0)
        marg = ism.get("margin", 0)
        fld = extract_field(expr)
        a(f"| {i} | {abs(ism['sharpe']):.3f} | {op} | {grp} | {fit:+.2f} | {marg*10000:+.1f}bp | `{fld}` |")

    # Region details for top5
    a(f"")
    a(f"**区域分布 (Top 5):**")
    a(f"")
    a(f"| # | Amer | Apac | Emea | 一致? |")
    a(f"|---|------|------|------|-------|")
    for i, r in enumerate(top5, 1):
        amer = r["is"].get("sharpe_glbAmer", "?")
        apac = r["is"].get("sharpe_glbApac", "?")
        emea = r["is"].get("sharpe_glbEmea", "?")
        cons = "✅" if is_consistent(r) else "❌"
        a(f"| {i} | {amer:+.2f} | {apac:+.2f} | {emea:+.2f} | {cons} |")
    a(f"")
    a(f"---")
    a(f"")
    a(f"## 3. 持续 Top 追踪 ({report_count} 份报告)")
    a(f"")

    if field_counts:
        a(f"### 字段出现率")
        a(f"")
        a(f"| 字段 | 出现率 | 趋势 |")
        a(f"|------|--------|------|")
        for fld, cnt in sorted(field_counts.items(), key=lambda x: -x[1]):
            pct = cnt / report_count * 100
            a(f"| `{fld}` | **{cnt}/{report_count} ({pct:.0f}%)** | {bar(pct)} |")
        a(f"")

        a(f"### 算子出现率")
        a(f"")
        a(f"| 算子 | 出现率 |")
        a(f"|------|--------|")
        for op, cnt in sorted(op_counts.items(), key=lambda x: -x[1]):
            pct = cnt / report_count * 100
            a(f"| `{op}` | {cnt}/{report_count} ({pct:.0f}%) |")
        a(f"")

        a(f"### 组合 (field+op) 出现率")
        a(f"")
        a(f"| 组合 | 出现率 |")
        a(f"|------|--------|")
        for combo, cnt in sorted(combo_counts.items(), key=lambda x: -x[1]):
            pct = cnt / report_count * 100
            if pct >= 50:
                a(f"| `{combo}` | {cnt}/{report_count} ({pct:.0f}%) |")
        a(f"")

    a(f"---")
    a(f"")
    a(f"## 4. 区域归因分析")
    a(f"")
    a(f"| 区域 | MeanSharpe | 评价 |")
    a(f"|------|-----------|------|")
    amer_label = "🟢 最强" if amer_m > 0.3 else "🟡 一般" if amer_m > 0 else "🔴 反向"
    apac_label = "🟢 最强" if apac_m > 0.3 else "🟡 一般" if apac_m > 0 else "🔴 反向"
    emea_label = "🟢 最强" if emea_m > 0.3 else "🟡 一般" if emea_m > 0 else "🔴 反向"
    a(f"| **Amer** | {amer_m:+.3f} | {amer_label} |")
    a(f"| **Apac** | {apac_m:+.3f} | {apac_label} |")
    a(f"| **Emea** | {emea_m:+.3f} | {emea_label} |")
    a(f"")
    a(f"---")
    a(f"")
    a(f"## 5. 稳健性检查")
    a(f"")
    a(f"| 检查项 | 结果 | 阈值 |")
    a(f"|--------|------|------|")
    s1 = sum(1 for r in valid if abs(r["is"]["sharpe"]) >= 1.58)
    s2 = sum(1 for r in valid if r["is"].get("fitness", 0) >= 1.0)
    s3 = sum(1 for r in valid if 0.01 <= r["is"].get("turnover", 0) <= 0.7)
    s4 = sum(1 for r in valid if r["is"].get("margin", 0) >= 0.0005)
    a(f"| \\|Sharpe\\| ≥ 1.58 | {s1}/{n} ({s1/n*100:.0f}%) | {'✅' if s1>0 else '❌'} |")
    a(f"| Fitness ≥ 1.0 | {s2}/{n} ({s2/n*100:.0f}%) | {'✅' if s2>0 else '❌'} |")
    a(f"| Turnover ∈ [1%, 70%] | {s3}/{n} ({s3/n*100:.0f}%) | {'✅' if s3==n else '⚠️'} |")
    a(f"| Margin ≥ 5bp | {s4}/{n} ({s4/n*100:.0f}%) | {'✅' if s4/n>0.8 else '⚠️'} |")
    a(f"| 三区域同号 | {consistent_count}/{n} ({consistent_count/n*100:.0f}%) | {'✅' if consistent_count/n>0.5 else '⚠️'} |")
    a(f"")
    a(f"---")
    a(f"")
    a(f"## 6. 关键发现与建议")
    a(f"")
    a(f"### 🔑 核心发现")
    a(f"")

    if field_counts:
        top_fld = max(field_counts, key=field_counts.get)
        top_cnt = field_counts[top_fld]
        a(f"1. **`{top_fld}` 持续霸榜** — {top_cnt}/{report_count} 报告 Top10")
        a(f"2. **Apac 区域**: MeanSharpe={apac_m:+.3f}, {'正向有效' if apac_m > 0 else '系统性反向 — 信号在亚太不成立'}")
        a(f"3. **三区一致候选**: {consistent_count}/{n} ({consistent_count/n*100:.1f}%) — {'需更多区域分散的信号' if consistent_count/n < 0.5 else '区域分散性良好'}")

    if consistent_count > 0:
        # find best consistent candidate
        best_cons = None
        for r in valid:
            if is_consistent(r):
                best_cons = r
                break
        if best_cons:
            a(f"")
            a(f"### 🏆 最佳三区一致候选")
            a(f"")
            a(f"```")
            a(f"表达式: {best_cons['expression']}")
            a(f"|S\\| = {abs(best_cons['is']['sharpe']):.3f}")
            a(f"Fit  = {best_cons['is']['fitness']:+.2f}")
            a(f"Marg = {best_cons['is']['margin']*10000:+.1f}bp")
            a(f"Turn = {best_cons['is']['turnover']*100:.1f}%")
            a(f"Amer = {best_cons['is'].get('sharpe_glbAmer', '?'):+.2f}")
            a(f"Apac = {best_cons['is'].get('sharpe_glbApac', '?'):+.2f}")
            a(f"Emea = {best_cons['is'].get('sharpe_glbEmea', '?'):+.2f}")
            a(f"```")

    a(f"")
    a(f"### 📋 建议")
    a(f"")
    if submittable > 0:
        a(f"| 优先级 | 行动 |")
        a(f"|--------|------|")
        a(f"| P0 | **有 {submittable} 个可提交候选，立即检查相关性并提交** |")
    else:
        a(f"| 优先级 | 行动 |")
        a(f"|--------|------|")
        a(f"| P0 | 深挖三区一致候选，进入 stage3 尝试 basic_ops 增强 |")
        a(f"| P1 | 如果仍不达 1.58，考虑切换 dataset 或区域 |")
        a(f"| P2 | 等待更多批次完成后重新评估 |")
    a(f"")

    out_path = output or os.path.join(ANALYSIS_DIR, f"REPORT_{tag}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ MD 报告已生成: {out_path}", flush=True)
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成 MD 归因报告")
    parser.add_argument("tag", help="标签, 如 glb_second")
    parser.add_argument("--output", help="输出路径 (可选)")
    args = parser.parse_args()
    generate_md(args.tag, args.output)