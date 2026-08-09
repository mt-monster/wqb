#!/usr/bin/env python3
"""
Multi-stage comparison report generator.
Reads all stage results (glb_first, glb_second, glb_third) and produces
a unified markdown report showing stage-by-stage progression, attribution,
and future mining recommendations.

Usage:
    python generate_multi_stage_report.py [--output REPORT_multi_stage.md]
"""

import json
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(BASE_DIR, "cache")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)

STAGES = [
    ("glb_first", "Stage1 — 一阶原始"),
    ("glb_second", "Stage2 — 二阶 group_ops"),
    ("glb_third", "Stage3 — 三阶 trade_when"),
]


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
                try:
                    results.append(json.loads(line))
                except Exception:
                    pass
    return results


def load_tracker(tag):
    path = os.path.join(ANALYSIS_DIR, f"top_tracker_{tag}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def load_progress(tag):
    pkl = os.path.join(CACHE, f"progress_{tag}.pkl")
    if os.path.exists(pkl):
        import pickle
        with open(pkl, "rb") as f:
            try:
                return pickle.load(f)
            except Exception:
                return None
    return None


def bar(pct, width=12):
    filled = int(pct / 100 * width)
    return "█" * max(1, filled) + "░" * max(0, width - filled)


# --- Field extraction for stage1: just the raw field name ---
# Stage2+: extract innermost field (anl15_*)
# For stage1, expression may be a full alpha like "zscore(ts_backfill(anl15_x, 120))"
def extract_field(expr):
    known_ops = {
        'group_neutralize', 'group_zscore', 'group_rank', 'group_scale',
        'winsorize', 'ts_backfill', 'densify', 'industry_neutralize',
        'sector_neutralize', 'market_neutralize', 'zscore', 'rank',
        'normalize', 'scale', 'ts_delay', 'ts_mean', 'ts_std', 'ts_min',
        'ts_max', 'ts_cov', 'ts_corr', 'truediv', 'log', 'sign', 'abs',
        'cap', 'sqrt', 'pow', 'neutralize', 'trade_when', 'condition',
        'max', 'min', 'if', 'else', 'ts_sum', 'ts_regslope', 'ts_regress',
        'ts_delta', 'ts_arg_max', 'ts_arg_min', 'ts_zscore', 'ts_rank',
        'ts_std_dev', 'ts_skewness', 'ts_kurtosis', 'ts_product',
        'ts_quantile', 'ts_ir', 'ts_scale', 'ts_returns', 'ts_max_diff',
        'signed_power', 'reverse', 'inverse', 'quantile',
        'industry_zscore', 'industry_rank', 'sector_zscore', 'sector_rank',
        'market_zscore', 'market_rank', 'country_zscore', 'country_rank',
        'bottom_n', 'top_n', 'bucket', 'sigtype',
        'ts_mean', 'ts_std', 'ts_arg_max', 'ts_arg_min',
        'market', 'sector', 'industry', 'country', 'std', 'half_life',
        'lookback', 'period', 'window', 'days', 'close', 'volume', 'returns',
        'ts_skewness', 'ts_entropy', 'inst_tvr', 'sigmoid', 'ts_decay_exp_window',
        'ts_percentage', 'vector_neut', 'vector_proj', 'ts_moment',
        'ts_min_max_cps', 'ts_min_diff', 'ts_max',
        'log_diff', 's_log_1p', 'fraction', 'scale_down',
    }
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr)
    for t in tokens:
        if t not in known_ops and not t.startswith("is_") and not t.startswith("sharpe"):
            if "_" in t and any(c.isdigit() for c in t):
                return t
    return expr.split("(")[0].strip()


def detect_stage_type(expr):
    """Detect the operation type for a given stage's expression"""
    if 'trade_when' in expr:
        # Extract the open event
        m = re.search(r'trade_when\(([^,]+),', expr)
        if m:
            event = m.group(1).strip()
            # Truncate long events
            return f"open: {event[:50]}"
        return "trade_when"
    if 'group_neutralize' in expr:
        return 'group_neutralize'
    if 'group_zscore' in expr:
        return 'group_zscore'
    if 'group_rank' in expr:
        return 'group_rank'
    if 'group_scale' in expr:
        return 'group_scale'
    # Stage1: try to identify the primary operator
    if expr.startswith('zscore'):
        return 'zscore'
    if expr.startswith('rank'):
        return 'rank'
    if 'signed_power' in expr:
        return 'signed_power'
    if 'ts_zscore' in expr:
        return 'ts_zscore'
    if 'ts_rank' in expr:
        return 'ts_rank'
    if 'ts_delta' in expr:
        return 'ts_delta'
    if 'ts_std_dev' in expr:
        return 'ts_std_dev'
    return expr.split("(")[0].strip() if "(" in expr else expr


def detect_group(expr):
    if 'densify(market)' in expr:
        return 'market'
    if 'densify(sector)' in expr:
        return 'sector'
    if 'densify(industry)' in expr:
        return 'industry'
    return '-'


def extract_open_event(expr):
    """Extract the open event from trade_when expressions"""
    m = re.search(r'trade_when\(([^,]+),', expr)
    if m:
        return m.group(1).strip()
    return '-'


# ============================================================
# Stage stats
# ============================================================
def compute_stage_stats(tag, label):
    results = read_results(tag)
    valid = [r for r in results if r.get("is", {}).get("sharpe") is not None]
    tracker = load_tracker(tag)
    progress = load_progress(tag)

    if not valid:
        return None

    valid.sort(key=lambda r: abs(r["is"]["sharpe"]), reverse=True)
    sharpes = [abs(r["is"]["sharpe"]) for r in valid]
    n = len(valid)

    mean_s = sum(sharpes) / n
    max_s = max(sharpes)
    min_s = min(sharpes)
    p50_s = sorted(sharpes)[n // 2]
    p75_s = sorted(sharpes)[int(n * 0.75)]
    p25_s = sorted(sharpes)[int(n * 0.25)]

    # Field attribution
    field_counts = {}
    for r in valid:
        fld = extract_field(r["expression"])
        field_counts[fld] = field_counts.get(fld, 0) + 1

    top_fields = sorted(field_counts.items(), key=lambda x: -x[1])[:10]

    # Operator attribution
    op_counts = {}
    for r in valid:
        op = detect_stage_type(r["expression"])
        op_counts[op] = op_counts.get(op, 0) + 1
    top_ops = sorted(op_counts.items(), key=lambda x: -x[1])[:10]

    # Region stats
    def region_mean(key):
        vals = [r["is"].get(key, 0) for r in valid if r["is"].get(key) is not None]
        return sum(vals) / len(vals) if vals else 0

    amer_m = region_mean("sharpe_glbAmer")
    apac_m = region_mean("sharpe_glbApac")
    emea_m = region_mean("sharpe_glbEmea")

    # Region sign consistency
    def is_consistent(r):
        a = r["is"].get("sharpe_glbAmer", 0)
        p = r["is"].get("sharpe_glbApac", 0)
        e = r["is"].get("sharpe_glbEmea", 0)
        if a is None or p is None or e is None:
            return False
        return (a > 0 and p > 0 and e > 0) or (a < 0 and p < 0 and e < 0)

    consistent = sum(1 for r in valid if is_consistent(r))

    # Turnover
    turnovers = [r["is"].get("turnover", 0) for r in valid]
    mean_tur = sum(turnovers) / n if turnovers else 0

    # Top 10 unique
    seen = set()
    top10 = []
    for r in valid:
        if r["expression"] not in seen:
            seen.add(r["expression"])
            top10.append(r)
            if len(top10) >= 10:
                break

    # Tracker info
    report_count = tracker["report_count"] if tracker else 0
    tracker_fields = tracker["field_counts"] if tracker else {}
    tracker_ops = tracker["op_counts"] if tracker else {}

    # Progress info
    progress_info = ""
    if progress and progress.get("done", 0) < 1000:
        # Only show progress for stage3 (active)
        done = progress.get("done", 0)
        total = 120 if "third" in tag else 45 if "second" in tag else 0
        if total > 0:
            progress_info = f"{done}/{total} ({done/total*100:.0f}%)"

    return {
        "tag": tag,
        "label": label,
        "n": n,
        "mean_s": mean_s,
        "max_s": max_s,
        "min_s": min_s,
        "p50_s": p50_s,
        "p25_s": p25_s,
        "p75_s": p75_s,
        "mean_tur": mean_tur,
        "consistent": consistent,
        "consistent_pct": consistent / n * 100,
        "amer_m": amer_m,
        "apac_m": apac_m,
        "emea_m": emea_m,
        "top_fields": top_fields,
        "top_ops": top_ops,
        "top10": top10,
        "report_count": report_count,
        "tracker_fields": tracker_fields,
        "tracker_ops": tracker_ops,
        "progress": progress_info,
    }


# ============================================================
# Generate report
# ============================================================
def generate(output=None):
    stats_list = []
    for tag, label in STAGES:
        s = compute_stage_stats(tag, label)
        if s:
            stats_list.append(s)

    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    lines = []
    a = lines.append

    a(f"# GLB Alpha Machine — 全阶段对比归因报告")
    a(f"")
    a(f"> **生成时间**: {now}")
    a(f"> **数据来源**: `cache/results_*.jsonl`")
    a(f"")
    a(f"---")
    a(f"")

    # ============================================================
    # Section 1: Cross-stage progression
    # ============================================================
    a(f"## 1. 阶段演进总览 (Cross-Stage Progression)")
    a(f"")
    a(f"| 指标 | Stage1 (一阶) | Stage2 (二阶) | Stage3 (三阶) | 演进趋势 |")
    a(f"|------|:---:|:---:|:---:|:---:|")

    if len(stats_list) >= 3:
        s1, s2, s3 = stats_list[0], stats_list[1], stats_list[2]
        n1, n2, n3 = s1["n"], s2["n"], s3["n"]
        ms1, ms2, ms3 = s1["mean_s"], s2["mean_s"], s3["mean_s"]
        mx1, mx2, mx3 = s1["max_s"], s2["max_s"], s3["max_s"]
        p50_1, p50_2, p50_3 = s1["p50_s"], s2["p50_s"], s3["p50_s"]
        tur1, tur2, tur3 = s1["mean_tur"], s2["mean_tur"], s3["mean_tur"]
        cons1, cons2, cons3 = s1["consistent_pct"], s2["consistent_pct"], s3["consistent_pct"]

        # Progression indicators
        def trend(v1, v2, v3):
            if v3 > v2 > v1:
                return "📈 持续提升"
            elif v3 > v1:
                return "📈 最终上升"
            elif v3 < v2 < v1:
                return "📉 持续下降"
            elif v3 < v1:
                return "📉 最终下降"
            return "➡️ 持平"

        a(f"| 有效候选数 | {n1} | {n2} | {n3} | — |")
        a(f"| Mean\\|S\\| | {ms1:.3f} | {ms2:.3f} | {ms3:.3f} | {trend(ms1, ms2, ms3)} |")
        a(f"| Max\\|S\\| | {mx1:.3f} | {mx2:.3f} | {mx3:.3f} | {trend(mx1, mx2, mx3)} |")
        a(f"| P50\\|S\\| | {p50_1:.3f} | {p50_2:.3f} | {p50_3:.3f} | {trend(p50_1, p50_2, p50_3)} |")
        a(f"| Mean Turnover | {tur1*100:.1f}% | {tur2*100:.1f}% | {tur3*100:.1f}% | {trend(tur1, tur2, tur3)} |")
        a(f"| 三区一致率 | {cons1:.0f}% | {cons2:.0f}% | {cons3:.0f}% | {trend(cons1, cons2, cons3)} |")

        # Progression arrows
        a(f"")
        a(f"**Sharpe 演进路径:**")
        a(f"")
        a(f"```")
        a(f"Max|S|:  {mx1:.3f} ──Stage2──▶ {mx2:.3f} ({(mx2-mx1)/mx1*100:+.0f}%) ──Stage3──▶ {mx3:.3f} ({(mx3-mx2)/mx2*100:+.0f}%)")
        a(f"Mean|S|: {ms1:.3f} ──Stage2──▶ {ms2:.3f} ({(ms2-ms1)/ms1*100:+.0f}%) ──Stage3──▶ {ms3:.3f} ({(ms3-ms2)/ms2*100:+.0f}%)")
        a(f"P50|S|:  {p50_1:.3f} ──Stage2──▶ {p50_2:.3f} ({(p50_2-p50_1)/p50_1*100:+.0f}%) ──Stage3──▶ {p50_3:.3f} ({(p50_3-p50_2)/p50_2*100:+.0f}%)")
        a(f"```")
        a(f"")

        # Distribution comparison
        a(f"**分布对比 (IQR/P50/Max):**")
        a(f"")
        a(f"| 阶段 | P25 | P50 | P75 | 分布特征 |")
        a(f"|------|:---:|:---:|:---:|----------|")
        for s in [s1, s2, s3]:
            iqr = s["p75_s"] - s["p25_s"]
            feature = "集中" if iqr < 0.1 else "分散" if iqr > 0.2 else "适中"
            a(f"| {s['label']} | {s['p25_s']:.3f} | {s['p50_s']:.3f} | {s['p75_s']:.3f} | IQR={iqr:.3f} ({feature}) |")
        a(f"")
    elif len(stats_list) >= 2:
        s1, s2 = stats_list[0], stats_list[1]
        a(f"| 指标 | Stage1 | Stage2 |")
        a(f"|------|:---:|:---:|")
        a(f"| 有效候选 | {s1['n']} | {s2['n']} |")
        a(f"| Mean\\|S\\| | {s1['mean_s']:.3f} | {s2['mean_s']:.3f} |")
        a(f"| Max\\|S\\| | {s1['max_s']:.3f} | {s2['max_s']:.3f} |")
        a(f"| 三区一致 | {s1['consistent_pct']:.0f}% | {s2['consistent_pct']:.0f}% |")
    a(f"")

    # ============================================================
    # Section 2: Region evolution
    # ============================================================
    a(f"## 2. 区域归因演进 (Regional Evolution)")
    a(f"")
    a(f"| 阶段 | Amer | Apac | Emea | 最强区域 | 最弱区域 |")
    a(f"|------|:----:|:----:|:----:|:--------:|:--------:|")
    for s in stats_list:
        regions = {"Amer": s["amer_m"], "Apac": s["apac_m"], "Emea": s["emea_m"]}
        best = max(regions, key=lambda k: regions[k])
        worst = min(regions, key=lambda k: regions[k])
        a(f"| {s['label']} | {s['amer_m']:+.3f} | {s['apac_m']:+.3f} | {s['emea_m']:+.3f} | **{best}** | ⚠️ {worst} |")
    a(f"")
    a(f"**区域一致性分析:**")
    a(f"")
    for s in stats_list:
        if s["apac_m"] < -0.1:
            a(f"- **{s['label']}**: Apac 系统性反向 ({s['apac_m']:+.3f}), 信号主要由 Amer 驱动")
        elif s["apac_m"] > 0.2:
            a(f"- **{s['label']}**: Apac 正向有效 ({s['apac_m']:+.3f}), 区域分散性改善")
        else:
            a(f"- **{s['label']}**: Apac 中性 ({s['apac_m']:+.3f}), 需进一步验证")
    a(f"")

    # ============================================================
    # Section 3: Top candidates per stage
    # ============================================================
    a(f"## 3. 各阶段 Top 候选对比")
    a(f"")
    for s in stats_list:
        a(f"### {s['label']} (Top 5)")
        a(f"")
        a(f"| # | \\|S\\| | 核心操作 | 字段 | Fit | Margin | Turnover |")
        a(f"|---|:---:|:--------:|:----:|:---:|:------:|:--------:|")
        for i, r in enumerate(s["top10"][:5], 1):
            ism = r["is"]
            op = detect_stage_type(r["expression"])
            fld = extract_field(r["expression"])
            a(f"| {i} | {abs(ism['sharpe']):.3f} | `{op}` | `{fld}` | {ism['fitness']:+.2f} | {ism['margin']*10000:+.1f}bp | {ism['turnover']*100:.1f}% |")
        a(f"")

    # ============================================================
    # Section 4: Field attribution across stages
    # ============================================================
    a(f"## 4. 字段归因 (跨阶段字段稳定性)")
    a(f"")
    # Collect all fields
    all_fields = set()
    field_stats = {}
    for s in stats_list:
        for fld, cnt in s["top_fields"]:
            all_fields.add(fld)
            if fld not in field_stats:
                field_stats[fld] = {}
            field_stats[fld][s["tag"]] = cnt

    a(f"| 字段 | Stage1 | Stage2 | Stage3 | 出现阶段数 | 评价 |")
    a(f"|------|:------:|:------:|:------:|:----------:|:----:|")
    for fld in sorted(all_fields):
        s1c = field_stats[fld].get("glb_first", 0)
        s2c = field_stats[fld].get("glb_second", 0)
        s3c = field_stats[fld].get("glb_third", 0)
        stages_present = sum(1 for v in [s1c, s2c, s3c] if v > 0)
        if stages_present == 3:
            rating = "🔥 全阶段稳定"
        elif stages_present == 2:
            rating = "📊 多数阶段"
        else:
            rating = "📄 单阶段"
        a(f"| `{fld}` | {s1c} | {s2c} | {s3c} | {stages_present} | {rating} |")
    a(f"")

    # ============================================================
    # Section 5: Operator/Event attribution
    # ============================================================
    a(f"## 5. 算子/事件归因")
    a(f"")
    for s in stats_list:
        a(f"### {s['label']}")
        a(f"")
        a(f"| 算子/操作 | 数量 | 占比 |")
        a(f"|----------|:----:|:----:|")
        total = s["n"]
        for op, cnt in s["top_ops"][:10]:
            a(f"| `{op}` | {cnt} | {cnt/total*100:.0f}% |")
        a(f"")

    # ============================================================
    # Section 6: Persistence tracker summary
    # ============================================================
    a(f"## 6. 持续入榜字段 (Persistent Top Tracker)")
    a(f"")
    for s in stats_list:
        if s["tracker_fields"]:
            a(f"### {s['label']} ({s['report_count']} 份报告)")
            a(f"")
            a(f"| 字段 | 出现率 | 趋势 |")
            a(f"|------|:------:|:----:|")
            for fld, cnt in sorted(s["tracker_fields"].items(), key=lambda x: -x[1]):
                pct = cnt / s["report_count"] * 100
                a(f"| `{fld}` | {cnt}/{s['report_count']} ({pct:.0f}%) | {bar(pct)} |")
            a(f"")

    # ============================================================
    # Section 7: Key findings & future mining strategy
    # ============================================================
    a(f"## 7. 关键发现与未来挖掘策略")
    a(f"")

    # Findings
    a(f"### 🔑 核心发现")
    a(f"")

    if len(stats_list) >= 3:
        s1, s2, s3 = stats_list[0], stats_list[1], stats_list[2]

        # 1. Sharpe improvement
        total_imp = (s3["max_s"] - s1["max_s"]) / s1["max_s"] * 100
        a(f"1. **Sharpe 提升路径**: Stage1 Max={s1['max_s']:.3f} → Stage2={s2['max_s']:.3f} → Stage3={s3['max_s']:.3f} (总提升 {total_imp:+.0f}%)")
        a(f"   - group_ops (二阶) 提升: {(s2['max_s']-s1['max_s'])/s1['max_s']*100:+.0f}%")
        a(f"   - trade_when (三阶) 提升: {(s3['max_s']-s2['max_s'])/s2['max_s']*100:+.0f}%")

        # 2. Field stability
        if s2["tracker_fields"]:
            top_fld = max(s2["tracker_fields"], key=s2["tracker_fields"].get)
            top_cnt = s2["tracker_fields"][top_fld]
            pct = top_cnt / s2["report_count"] * 100
            a(f"2. **最稳定字段**: `{top_fld}` — 在 {s2['report_count']} 份报告中 {pct:.0f}% 入 Top10")

        # 3. Region analysis
        a(f"3. **区域诊断**:")
        a(f"   - Amer: Stage3 MeanSharpe={s3['amer_m']:+.3f} — {'✅ 有效' if s3['amer_m'] > 0.2 else '⚠️ 一般' if s3['amer_m'] > 0 else '❌ 反向'}")
        a(f"   - Apac: Stage3 MeanSharpe={s3['apac_m']:+.3f} — {'✅ 有效' if s3['apac_m'] > 0.2 else '⚠️ 一般' if s3['apac_m'] > 0 else '❌ 系统性反向'}")
        a(f"   - Emea: Stage3 MeanSharpe={s3['emea_m']:+.3f} — {'✅ 有效' if s3['emea_m'] > 0.2 else '⚠️ 一般' if s3['emea_m'] > 0 else '❌ 反向'}")

        # 4. Gap analysis
        gap = 1.58 - s3["max_s"]
        if gap > 0:
            a(f"4. **提交差距**: 当前 Max|S|={s3['max_s']:.3f}, 距 1.58 差 **{gap:.2f}** ({gap/s3['max_s']*100:.0f}%)")
        else:
            a(f"4. **🎉 已达提交阈值**: Max|S|={s3['max_s']:.3f} ≥ 1.58")

    a(f"")

    # ============================================================
    # Future mining strategy
    # ============================================================
    a(f"### 📋 未来挖掘策略 (Future Mining Strategy)")
    a(f"")
    a(f"#### 策略 A: 深化当前信号链 (当前最优)")
    a(f"")
    a(f"```")
    a(f"当前最优信号链:")
    a(f"  字段: anl15_s_cal_fy2_6m_chg")
    a(f"  一阶: winsorize(ts_backfill(field, 120), std=4)")
    a(f"  二阶: group_neutralize(...) / group_zscore(...)")
    a(f"  三阶: trade_when(ts_corr(close, volume, 20) > 0.3, ...)")
    a(f"")
    a(f"可扩展方向:")
    a(f"  1. 测试不同 ts_backfill 窗口: 60/90/180/250 (当前=120)")
    a(f"  2. 测试不同 winsorize std: 2/3/5/6 (当前=4)")
    a(f"  3. 组合二阶+三阶: trade_when() 内嵌套 group_rank()")
    a(f"  4. 叠加 basic_ops: signed_power(zscore(rank(...)), 3)")
    a(f"```")
    a(f"")
    a(f"#### 策略 B: 拓展字段池")
    a(f"")
    a(f"```")
    a(f"当前仅使用 analyst15 (1个 dataset):")
    a(f"  - 已验证: anl15_s_cal_fy2_6m_chg (100%入Top)")
    a(f"  - 次优: anl15_gr_12_m_6m_chg (71%入Top)")
    a(f"")
    a(f"推荐尝试的 dataset:")
    a(f"  1. analyst16 — 分析师评级 (与 anl15 互补)")
    a(f"  2. options — 期权隐含波动率/偏度")
    a(f"  3. fundamentals — 财务基本面")
    a(f"  4. price_volume — 量价信号")
    a(f"  5. short_interest — 做空数据")
    a(f"  6. institutional — 机构持仓变化")
    a(f"```")
    a(f"")
    a(f"#### 策略 C: 拓展算子空间")
    a(f"")
    a(f"```")
    a(f"当前算子:")
    a(f"  Stage1: zscore/rank/ts_zscore/ts_rank/...")
    a(f"  Stage2: group_neutralize/group_rank/group_zscore")
    a(f"  Stage3: trade_when (12 open events)")
    a(f"")
    a(f"可拓展算子:")
    a(f"  - basic_ops: signed_power, quantile, normalize")
    a(f"  - ts_ops: ts_product, ts_quantile, ts_ir")
    a(f"  - 新增 trade_when open events:")
    a(f"    · ts_regression(volume, price, 20)")
    a(f"    · group_zscore(field, market) > 1.5")
    a(f"    · ts_delta(volume, 1) > 0 (放量)")
    a(f"    · ts_momentum(close, 20) > 0 (趋势)")
    a(f"```")
    a(f"")
    a(f"#### 策略 D: 区域突破")
    a(f"")
    a(f"```")
    a(f"当前 Apac 系统性反向 — 这是核心瓶颈:")
    a(f"")
    a(f"方案1: 寻找 Apac 正向的 dataset")
    a(f"  - options/derivatives 在亚太可能更有效")
    a(f"  - fundamentals 在新兴市场有独特信号")
    a(f"")
    a(f"方案2: 使用 country 级别分组代替 market")
    a(f"  - group_neutralize(field, country) 可能捕捉区域性信号")
    a(f"")
    a(f"方案3: 分区域独立挖掘")
    a(f"  - 先做 Amer-only 提交 (如果允许)")
    a(f"  - 再独立探索 Apac/Emea 专属信号")
    a(f"```")
    a(f"")
    a(f"#### 策略 E: 高阶组合")
    a(f"")
    a(f"```")
    a(f"当 Max|S| 卡在 0.5~0.7 区间时, 考虑:")
    a(f"")
    a(f"1. 双信号 blend:")
    a(f"   0.5 * trade_when(event1, field_A) + 0.5 * trade_when(event2, field_B)")
    a(f"")
    a(f"2. 条件嵌套:")
    a(f"   trade_when(event1, trade_when(event2, field))")
    a(f"")
    a(f"3. 时间窗口缩放:")
    a(f"   用 ts_backfill 的不同窗口做差分:")
    a(f"   ts_backfill(field, 60) - ts_backfill(field, 120)")
    a(f"")
    a(f"4. 算子叠加:")
    a(f"   signed_power(zscore(rank(ts_zscore(field))), 3)")
    a(f"```")
    a(f"")

    # ============================================================
    # Section 8: Submission checklist
    # ============================================================
    a(f"## 8. 提交检查清单 (Submission Readiness)")
    a(f"")
    a(f"| 检查项 | 阈值 | Stage3 状态 | 通过? |")
    a(f"|--------|:----:|:-----------:|:-----:|")

    if len(stats_list) >= 3:
        s3 = stats_list[2]
        mx = s3["max_s"]
        top_r = s3["top10"][0] if s3["top10"] else None
        if top_r:
            ism = top_r["is"]
            fit = ism.get("fitness", 0)
            tur = ism.get("turnover", 0)
            marg = ism.get("margin", 0)
            ret = ism.get("return", 0)
            dd = ism.get("drawdown", 0)

            a(f"| |Sharpe| | ≥1.58 | {mx:.3f} | {'✅' if mx >= 1.58 else '❌'} |")
            a(f"| Fitness | ≥1.0 | {fit:.2f} | {'✅' if fit >= 1.0 else '❌'} |")
            a(f"| Turnover | [5%, 20%] | {tur*100:.1f}% | {'✅' if 0.05 <= tur <= 0.20 else '⚠️'} |")
            a(f"| Margin | >5bp | {marg*10000:.1f}bp | {'✅' if marg > 0.0005 else '❌'} |")
            a(f"| Return | >5% | {ret*100:.1f}% | {'✅' if ret > 0.05 else '❌'} |")
            a(f"| Drawdown | <Return | {dd*100:.1f}% | {'⚠️' if dd > ret else '✅'} |")

    a(f"")

    # ============================================================
    # Section 9: Running status
    # ============================================================
    a(f"## 9. 运行状态")
    a(f"")
    a(f"| 阶段 | 进度 | 有效结果 | Mean\\|S\\| | Max\\|S\\| |")
    a(f"|------|:----:|:--------:|:-------:|:------:|")
    for s in stats_list:
        prog = s["progress"] or "✅ 完成"
        a(f"| {s['label']} | {prog} | {s['n']} | {s['mean_s']:.3f} | {s['max_s']:.3f} |")
    a(f"")

    out_path = output or os.path.join(ANALYSIS_DIR, "REPORT_multi_stage.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 全阶段对比报告已生成: {out_path}", flush=True)
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成全阶段对比归因报告")
    parser.add_argument("--output", help="输出路径")
    args = parser.parse_args()
    generate(args.output)