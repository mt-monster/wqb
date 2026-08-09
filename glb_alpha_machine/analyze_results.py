# -*- coding: utf-8 -*-
"""
因子归因分析脚本
用法:
  python analyze_results.py <tag>              # e.g. "glb_first"
  python analyze_results.py glb_first --top 20  # 自定义 top N
  python analyze_results.py glb_first --save   # 同时保存 HTML 报告

输出:
  1. 终端打印完整归因报告
  2. (可选) 保存 analysis_{tag}.html
"""
import os
import sys
import json
import re
import argparse
from collections import defaultdict
from datetime import datetime

# ==================== 配置 ====================
ANALYSIS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis")
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# 提交门槛
SHARPE_THRESHOLD = 1.58
FITNESS_THRESHOLD = 1.0
TURNOVER_MIN = 0.01
TURNOVER_MAX = 0.7
MARGIN_THRESHOLD = 0.0005  # 5bp (GLB)

# 因子族分类
def classify_factor(field_name):
    """根据字段名归类到因子族"""
    if field_name.startswith("anl15_gr_"):
        return "分析师评级 (Rating)"
    elif field_name.startswith("anl15_s_"):
        return "行业 (Sector)"
    elif field_name.startswith("anl15_ind_"):
        return "个股 (Individual)"
    elif field_name.startswith("sector_"):
        return "板块聚合 (SectorAgg)"
    elif field_name.startswith("group_"):
        return "分组 (Group)"
    else:
        return "其他"


def extract_field(expression):
    """从表达式中提取原始字段名"""
    m = re.search(r'ts_backfill\((\w+),', expression)
    if m:
        return m.group(1)
    # Fallback: 返回表达式前60字符
    return expression[:60]


def extract_operator(expression):
    """从表达式中提取使用的算子链 (可处理多层嵌套)"""
    ops = []
    # raw = 仅 winsorize(ts_backfill(...)) 无其他算子
    if re.match(r'^winsorize\(ts_backfill\(', expression):
        return "raw"
    # 提取所有嵌套算子(从外到内)
    op_pattern = re.compile(
        r'(rank|reverse|inverse|zscore|quantile|normalize|log|sqrt|'
        r'ts_rank|ts_zscore|ts_delta|ts_sum|ts_product|ts_ir|ts_std_dev|'
        r'ts_mean|ts_arg_min|ts_arg_max|ts_max_diff|ts_returns|ts_scale|'
        r'ts_kurtosis|ts_quantile|signed_power|group_rank|neutralize|'
        r'winsorize|trade_when|group_zscore|group_rank|group_scale|'
        r'decay_linear|decay_fast_linear|decay_sqr|clip|abs|sign)'
    )
    matches = op_pattern.findall(expression)
    # 去重保留顺序
    seen = set()
    for m in matches:
        if m not in seen:
            ops.append(m)
            seen.add(m)
    return "+".join(ops) if ops else "raw"


def extract_field(expression):
    """从表达式中提取原始字段名"""
    m = re.search(r'ts_backfill\((\w+),', expression)
    if m:
        return m.group(1)
    m2 = re.search(r'\((\w+_[\w_]+)\)', expression)
    if m2:
        return m2.group(1)
    return expression[:60]


def extract_window(expression):
    """提取 ts_backfill 窗口参数"""
    m = re.search(r'ts_backfill\([^,]+,(\d+)\)', expression)
    if m:
        return int(m.group(1))
    return None


def read_results(tag):
    """读取 JSONL 结果文件"""
    results_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "cache", f"results_{tag}.jsonl"
    )
    if not os.path.exists(results_file):
        print(f"[ERROR] 未找到结果文件: {results_file}")
        sys.exit(1)

    results = []
    with open(results_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    results.append(json.loads(line))
                except Exception:
                    pass
    return results


def compute_stats(values):
    """计算基础统计量"""
    if not values:
        return {}
    n = len(values)
    values_sorted = sorted(values)
    return {
        "count": n,
        "mean": sum(values) / n,
        "std": (sum((v - sum(values)/n)**2 for v in values) / n) ** 0.5 if n > 1 else 0,
        "min": values_sorted[0],
        "p25": values_sorted[int(n * 0.25)],
        "p50": values_sorted[int(n * 0.5)],
        "p75": values_sorted[int(n * 0.75)],
        "max": values_sorted[-1],
    }


def histogram_bar(values, label_min, label_max, bins=10):
    """生成 ASCII 直方图"""
    if not values:
        return "  (无数据)"
    v_min = min(values)
    v_max = max(values)
    if v_min == v_max:
        return f"  {v_min:.4f}"
    bin_width = (v_max - v_min) / bins
    counts = [0] * bins
    for v in values:
        idx = min(int((v - v_min) / bin_width), bins - 1)
        counts[idx] += 1
    max_count = max(counts) if counts else 1
    lines = []
    for i in range(bins):
        lo = v_min + i * bin_width
        hi = lo + bin_width
        bar_len = int(counts[i] / max_count * 40) if max_count > 0 else 0
        bar = "█" * bar_len
        lines.append(f"  [{lo:+7.3f}, {hi:+7.3f}) {bar} ({counts[i]})")
    return "\n".join(lines)


def fmt_pct(v):
    if v is None:
        return "N/A"
    return f"{v*100:.2f}%"


def fmt_bp(v):
    if v is None:
        return "N/A"
    return f"{v*10000:.2f}bp"


def fmt_sharpe(v):
    if v is None:
        return "N/A"
    return f"{v:+.3f}"


def fmt_fitness(v):
    if v is None:
        return "N/A"
    return f"{v:+.3f}"


# ==================== 归因分析引擎 ====================
def analyze(tag, top_n=15, save_html=False):
    results = read_results(tag)
    stage = tag.replace("glb_", "")

    # 分离有效/无效
    valid = [r for r in results if r.get("is", {}).get("sharpe") is not None]
    errors = [r for r in results if r.get("is", {}).get("sharpe") is None]

    # 提取各指标
    sharpes = [r["is"]["sharpe"] for r in valid]
    turnovers = [r["is"]["turnover"] for r in valid if r["is"].get("turnover") is not None]
    fitnesses = [r["is"]["fitness"] for r in valid if r["is"].get("fitness") is not None]
    margins = [r["is"]["margin"] for r in valid if r["is"].get("margin") is not None]
    returns = [r["is"]["return"] for r in valid if r["is"].get("return") is not None]
    drawdowns = [r["is"]["drawdown"] for r in valid if r["is"].get("drawdown") is not None]

    # 按 |sharpe| 排序
    valid.sort(key=lambda r: abs(r["is"]["sharpe"]), reverse=True)

    # 提交门槛检查
    submittable = []
    for r in valid:
        ism = r["is"]
        if abs(ism.get("sharpe", 0)) >= SHARPE_THRESHOLD and \
           ism.get("fitness", 0) >= FITNESS_THRESHOLD and \
           TURNOVER_MIN <= ism.get("turnover", 0) <= TURNOVER_MAX:
            submittable.append(r)

    # 因子族分析
    family_stats = defaultdict(list)
    for r in valid:
        field = extract_field(r["expression"])
        family = classify_factor(field)
        family_stats[family].append(abs(r["is"]["sharpe"]))

    # 算子分析
    op_stats = defaultdict(list)
    for r in valid:
        op = extract_operator(r["expression"])
        op_stats[op].append(abs(r["is"]["sharpe"]))

    # 区域归因
    regions = ["glbAmer", "glbApac", "glbEmea"]
    region_sharpe = {reg: [r["is"].get(f"sharpe_{reg}") for r in valid
                            if r["is"].get(f"sharpe_{reg}") is not None]
                     for reg in regions}

    # ==================== 输出报告 ====================
    report_lines = []

    def out(s=""):
        report_lines.append(s)
        print(s)

    out()
    out("═" * 70)
    out(f"  GLB Analyst15 — Stage {stage.upper()} 因子归因分析")
    out(f"  分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    out("═" * 70)

    # 1. 总览
    out()
    out("【1】总览")
    out("─" * 50)
    out(f"  总候选数:          {len(results)}")
    out(f"  成功 (有IS指标):   {len(valid)}  ({len(valid)/max(len(results),1)*100:.1f}%)")
    out(f"  失败 (无IS指标):   {len(errors)}  ({len(errors)/max(len(results),1)*100:.1f}%)")
    out(f"  可提交候选:        {len(submittable)}")
    if submittable:
        out(f"    → 可提交 alpha_id: {', '.join(r['alpha_platform_id'] for r in submittable[:10])}")

    # 2. Sharpe 分布
    out()
    out("【2】Sharpe 分布")
    out("─" * 50)
    s_stats = compute_stats(sharpes)
    if s_stats:
        out(f"  Count: {s_stats['count']}  Mean: {s_stats['mean']:+.4f}  Std: {s_stats['std']:.4f}")
        out(f"  Min: {s_stats['min']:+.4f}  P25: {s_stats['p25']:+.4f}  "
            f"P50: {s_stats['p50']:+.4f}  P75: {s_stats['p75']:+.4f}  Max: {s_stats['max']:+.4f}")
        out(f"  |Sharpe| stats:")
        abs_sharpes = [abs(s) for s in sharpes]
        abs_stats = compute_stats(abs_sharpes)
        out(f"    Mean: {abs_stats['mean']:.4f}  P50: {abs_stats['p50']:.4f}  "
            f"Max: {abs_stats['max']:.4f}")
        out()
        out("  |Sharpe| 直方图:")
        out(histogram_bar(abs_sharpes, 0, abs_stats['max'], bins=10))

    # 3. 其他指标
    out()
    out("【3】其他 IS 指标分布")
    out("─" * 50)
    for label, vals in [("Turnover", turnovers), ("Fitness", fitnesses),
                         ("Margin(bp)", [m*10000 for m in margins]),
                         ("Return(%)", [r*100 for r in returns]),
                         ("Drawdown(%)", [d*100 for d in drawdowns])]:
        st = compute_stats(vals)
        if st:
            out(f"  {label:15s}: Mean={st['mean']:+.4f}  P50={st['p50']:+.4f}  "
                f"Min={st['min']:+.4f}  Max={st['max']:+.4f}")

    # 4. Top N 候选
    out()
    out(f"【4】Top {top_n} 候选 (按 |Sharpe| 排序)")
    out("─" * 50)
    header = f"  {'#':>3} {'|Shr|':>6} {'Shr':>7} {'Fit':>6} {'Tur':>6} {'Marg':>8} {'Ret':>7} {'DD':>7}  Field"
    out(header)
    out(f"  {'─'*len(header)}")
    for i, r in enumerate(valid[:top_n]):
        ism = r["is"]
        field = extract_field(r["expression"])
        out(f"  {i+1:>3} {abs(ism['sharpe']):6.3f} {ism['sharpe']:+7.3f} "
            f"{ism['fitness']:+6.3f} {ism['turnover']:6.3f} {ism['margin']*10000:+8.2f}bp "
            f"{ism['return']*100:+6.2f}% {ism['drawdown']*100:6.2f}%  {field}")

    # 5. 因子族归因
    out()
    out("【5】因子族归因 (Factor Family Attribution)")
    out("─" * 50)
    if family_stats:
        fam_sorted = sorted(family_stats.items(), key=lambda x: x[1][0] if x[1] else 0, reverse=True)
        fam_header = f"  {'因子族':<20} {'N':>5} {'Mean|S|':>8} {'P50|S|':>8} {'Max|S|':>8} {'AvgTurn':>8} {'占比':>6}"
        out(fam_header)
        out(f"  {'─'*len(fam_header)}")
        for fam, s_vals in fam_sorted:
            s_stats_f = compute_stats(s_vals)
            # 该族平均 turnover
            fam_turn = [r["is"]["turnover"] for r in valid
                        if classify_factor(extract_field(r["expression"])) == fam
                        and r["is"].get("turnover") is not None]
            avg_turn = sum(fam_turn) / len(fam_turn) if fam_turn else 0
            pct = len(s_vals) / len(valid) * 100
            out(f"  {fam:<20} {len(s_vals):>5} {s_stats_f['mean']:>8.3f} "
                f"{s_stats_f['p50']:>8.3f} {s_stats_f['max']:>8.3f} "
                f"{avg_turn:>8.4f} {pct:>5.1f}%")

    # 6. 算子归因
    out()
    out("【6】算子归因 (Operator Attribution)")
    out("─" * 50)
    if op_stats:
        op_sorted = sorted(op_stats.items(), key=lambda x: x[1][0] if x[1] else 0, reverse=True)
        op_header = f"  {'算子':<16} {'N':>5} {'Mean|S|':>8} {'P50|S|':>8} {'Max|S|':>8}"
        out(op_header)
        out(f"  {'─'*len(op_header)}")
        for op, s_vals in op_sorted:
            s_stats_o = compute_stats(s_vals)
            out(f"  {op:<16} {len(s_vals):>5} {s_stats_o['mean']:>8.3f} "
                f"{s_stats_o['p50']:>8.3f} {s_stats_o['max']:>8.3f}")

    # 7. 区域归因
    out()
    out("【7】区域归因 (Regional Attribution)")
    out("─" * 50)
    region_header = f"  {'区域':<12} {'N':>5} {'MeanShr':>8} {'P50Shr':>8} {'MaxShr':>8} {'Avg|Fit|':>10}"
    out(region_header)
    out(f"  {'─'*len(region_header)}")
    for reg in regions:
        reg_vals = region_sharpe[reg]
        if reg_vals:
            r_stats = compute_stats(reg_vals)
            # 平均 |fitness|
            reg_fit = [abs(r["is"].get(f"fitness_{reg}", 0) or 0) for r in valid
                       if r["is"].get(f"fitness_{reg}") is not None]
            avg_fit = sum(reg_fit) / len(reg_fit) if reg_fit else 0
            out(f"  {reg:<12} {len(reg_vals):>5} {r_stats['mean']:>+8.3f} "
                f"{r_stats['p50']:>+8.3f} {r_stats['max']:>+8.3f} {avg_fit:>10.4f}")

    # 8. 稳健性检查
    out()
    out("【8】稳健性检查 (Robustness Check)")
    out("─" * 50)
    if valid:
        pass_shr = sum(1 for s in sharpes if abs(s) >= SHARPE_THRESHOLD)
        pass_fit = sum(1 for f in fitnesses if f >= FITNESS_THRESHOLD)
        pass_turn = sum(1 for t in turnovers if TURNOVER_MIN <= t <= TURNOVER_MAX)
        out(f"  |Sharpe| ≥ {SHARPE_THRESHOLD}:  {pass_shr}/{len(valid)} ({pass_shr/len(valid)*100:.1f}%)")
        out(f"  Fitness ≥ {FITNESS_THRESHOLD}:    {pass_fit}/{len(valid)} ({pass_fit/len(valid)*100:.1f}%)")
        out(f"  Turnover ∈ [{TURNOVER_MIN},{TURNOVER_MAX}]: {pass_turn}/{len(valid)} ({pass_turn/len(valid)*100:.1f}%)")
        out(f"  Margin ≥ {MARGIN_THRESHOLD*10000:.1f}bp: {sum(1 for m in margins if m >= MARGIN_THRESHOLD)}/{len(valid)}")
        # 三区域一致性: 三区域 sharpe 同号
        consistent = 0
        for r in valid:
            ism = r["is"]
            signs = [ism.get(f"sharpe_{reg}") for reg in regions]
            if all(s is not None for s in signs):
                if all(s > 0 for s in signs) or all(s < 0 for s in signs):
                    consistent += 1
        out(f"  三区域同号:        {consistent}/{len(valid)} ({consistent/len(valid)*100:.1f}%)")
        # 区域 sharpe 衰减
        decay_ratio = []
        for r in valid:
            ism = r["is"]
            global_shr = abs(ism.get("sharpe", 0) or 0)
            sub_shrs = [abs(ism.get(f"sharpe_{reg}", 0) or 0) for reg in regions]
            if global_shr > 0 and sub_shrs:
                avg_sub = sum(sub_shrs) / len(sub_shrs)
                decay_ratio.append(avg_sub / global_shr)
        if decay_ratio:
            avg_decay = sum(decay_ratio) / len(decay_ratio)
            out(f"  区域衰减率(子域/全局): {avg_decay:.3f} (越接近1越稳健)")

    # 9. Decay & 窗口分析
    out()
    out("【9】Decay & 窗口分析 (Decay & Window Attribution)")
    out("─" * 50)
    # Decay 分布
    decay_stats = defaultdict(list)
    window_stats = defaultdict(list)
    for r in valid:
        d = r.get("decay", "?")
        decay_stats[d].append(abs(r["is"]["sharpe"]))
        w = extract_window(r["expression"])
        if w is not None:
            window_stats[w].append(abs(r["is"]["sharpe"]))

    if decay_stats:
        out("  Decay 分布:")
        dec_header = f"    {'Decay':>6} {'N':>5} {'Mean|S|':>8} {'P50|S|':>8} {'Max|S|':>8}"
        out(dec_header)
        out(f"    {'─'*len(dec_header)}")
        for d in sorted(decay_stats.keys(), key=lambda x: (isinstance(x, str), x)):
            s_vals = decay_stats[d]
            s_s = compute_stats(s_vals)
            out(f"    {str(d):>6} {len(s_vals):>5} {s_s['mean']:>8.3f} "
                f"{s_s['p50']:>8.3f} {s_s['max']:>8.3f}")

    if window_stats:
        out("  窗口长度分布:")
        win_header = f"    {'窗口':>6} {'N':>5} {'Mean|S|':>8} {'P50|S|':>8} {'Max|S|':>8}"
        out(win_header)
        out(f"    {'─'*len(win_header)}")
        for w in sorted(window_stats.keys()):
            s_vals = window_stats[w]
            s_s = compute_stats(s_vals)
            out(f"    {w:>6} {len(s_vals):>5} {s_s['mean']:>8.3f} "
                f"{s_s['p50']:>8.3f} {s_s['max']:>8.3f}")

    # 10. 失败分析
    if errors:
        out()
        out("【10】失败分析 (Error Analysis)")
        out("─" * 50)
        err_types = defaultdict(int)
        for e in errors:
            st = e.get("status", "UNKNOWN")
            err_types[st] += 1
        for st, cnt in sorted(err_types.items(), key=lambda x: -x[1]):
            out(f"  {st}: {cnt}")
        task_errs = defaultdict(int)
        for e in errors:
            task_errs[e.get("task_no", "?")] += 1
        if task_errs:
            out("  失败 task 分布:")
            for t, cnt in sorted(task_errs.items()):
                out(f"    task {t}: {cnt} errors")

    # 11. 总结与建议
    out()
    out("【11】总结与建议")
    out("─" * 50)
    if not valid:
        out("  ⚠ 无有效结果, 检查任务是否全部完成")
    elif not submittable:
        out(f"  • 当前 {len(valid)} 个有效结果, 最高 |Sharpe|={max(abs(s) for s in sharpes):.3f}")
        if len(valid) < len(results) * 0.9:
            out("  • 错误率偏高, 建议降低批次大小(SIMS_PER_BATCH=2)或增加间隔")
        if stage == "first":
            out("  • 建议: 进入 stage2 对 top 300 做 group_ops 变换")
            out("  • 或: 考虑加入 basic_ops (rank/reverse/zscore) 提升信号强度")
        elif stage == "second":
            out("  • 建议: 进入 stage3 对 top 300 做 trade_when 变换")
            out("  • 或: 考虑加入 basic_ops 增强二阶信号")
        elif stage == "third":
            out("  • 建议: 检查是否满足提交条件 (Sharpe>1.58, Fitness>1.0)")
            out("  • 或: 回到 stage1 更换 ops_set 重新探索")
        # Top 3 建议
        out(f"  • 最高 |Sharpe| 的3个字段: {', '.join(extract_field(r['expression']) for r in valid[:3])}")
    else:
        out(f"  ✓ {len(submittable)} 个可提交候选:")
        for r in submittable:
            ism = r["is"]
            out(f"    alpha={r['alpha_platform_id']} sharpe={ism['sharpe']:+.3f} "
                f"fitness={ism['fitness']:+.3f} margin={ism['margin']*10000:.2f}bp")
        out("  • 建议: 进入 stage4 做提交前检查")

    out()
    out("═" * 70)

    # 跨报告持续 Top 追踪
    _print_persistent_top(tag, valid, top_n, out)

    # 保存 HTML
    if save_html:
        html_path = os.path.join(ANALYSIS_DIR, f"analysis_{tag}.html")
        html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>GLB {stage.upper()} Analysis</title>
<style>
body {{ font-family: monospace; white-space: pre-wrap; padding: 20px; }}
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid #ddd; padding: 4px 8px; text-align: right; }}
th {{ background: #f5f5f5; }}
</style></head><body><pre>{'\n'.join(report_lines)}</pre></body></html>"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        out(f"  HTML 报告已保存: {html_path}")

    return valid, submittable


# ==================== 跨报告持续 Top 追踪 ====================
def _tracker_path(tag):
    return os.path.join(ANALYSIS_DIR, f"top_tracker_{tag}.json")


def _load_tracker(tag):
    path = _tracker_path(tag)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"field_counts": {}, "op_counts": {}, "report_count": 0}


def _save_tracker(tag, tracker):
    path = _tracker_path(tag)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tracker, f, ensure_ascii=False, indent=2)


def _print_persistent_top(tag, valid, top_n, out):
    """打印跨报告持续 Top 追踪: 哪些字段/算子在多份报告中反复出现"""
    # 提取 Top N
    top = valid[:top_n]
    top_fields = [extract_field(r["expression"]) for r in top]
    top_ops = [extract_operator(r["expression"]) for r in top]
    top_field_op_pairs = [(extract_field(r["expression"]), extract_operator(r["expression"])) for r in top]

    tracker = _load_tracker(tag)
    tracker["report_count"] += 1

    # 更新字段计数
    for f in set(top_fields):
        tracker["field_counts"][f] = tracker["field_counts"].get(f, 0) + 1
    # 更新算子计数
    for o in set(top_ops):
        tracker["op_counts"][o] = tracker["op_counts"].get(o, 0) + 1
    # 更新 field+op 组合计数
    if "combo_counts" not in tracker:
        tracker["combo_counts"] = {}
    for (f, o) in set(top_field_op_pairs):
        key = f"{o}({f})"
        tracker["combo_counts"][key] = tracker["combo_counts"].get(key, 0) + 1

    # 记录 Top1 变化
    if top:
        t1 = extract_field(top[0]["expression"])
        if "top1_history" not in tracker:
            tracker["top1_history"] = []
        tracker["top1_history"].append({"field": t1, "sharpe": top[0]["is"]["sharpe"],
                                        "report": tracker["report_count"]})

    _save_tracker(tag, tracker)

    # 输出追踪结果
    if tracker["report_count"] <= 1:
        out()
        out("【12】持续 Top 追踪 (Persistent Top Tracker)")
        out("─" * 50)
        out("  (首次报告, 尚无历史对比)")
        return

    out()
    out("【12】持续 Top 追踪 (Persistent Top Tracker)")
    out("─" * 50)
    out(f"  累计报告数: {tracker['report_count']}")

    # 持续入榜字段
    total_reports = tracker["report_count"]
    persistent_fields = {k: v for k, v in tracker["field_counts"].items()
                         if v >= total_reports * 0.5}  # 至少50%报告中出现
    if persistent_fields:
        out("  持续入榜字段 (出现率≥50%):")
        sorted_pf = sorted(persistent_fields.items(), key=lambda x: -x[1])
        for f, cnt in sorted_pf[:8]:
            pct = cnt / total_reports * 100
            bar = "█" * int(pct / 10)
            out(f"    {f:<40} {cnt}/{total_reports} ({pct:.0f}%) {bar}")

    # 持续入榜算子
    persistent_ops = {k: v for k, v in tracker["op_counts"].items()
                      if v >= total_reports * 0.5}
    if persistent_ops:
        out("  持续入榜算子 (出现率≥50%):")
        for o, cnt in sorted(persistent_ops.items(), key=lambda x: -x[1]):
            pct = cnt / total_reports * 100
            out(f"    {o:<20} {cnt}/{total_reports} ({pct:.0f}%)")

    # 持续入榜组合 (field+op)
    persistent_combos = {k: v for k, v in tracker.get("combo_counts", {}).items()
                         if v >= total_reports * 0.5}
    if persistent_combos:
        out("  持续入榜组合 (field+op, 出现率≥50%):")
        for c, cnt in sorted(persistent_combos.items(), key=lambda x: -x[1])[:8]:
            pct = cnt / total_reports * 100
            out(f"    {c:<55} {cnt}/{total_reports} ({pct:.0f}%)")

    # Top1 变化趋势
    if "top1_history" in tracker and len(tracker["top1_history"]) > 1:
        out("  Top1 变化:")
        for h in tracker["top1_history"][-5:]:
            out(f"    报告#{h['report']}: {h['field']} (sharpe={h['sharpe']:+.3f})")


# ==================== 跨阶段对比 ====================
def compare_stages(tags, top_n=10):
    """对比多个阶段的结果"""
    print()
    print("═" * 70)
    print("  跨阶段对比分析 (Cross-Stage Comparison)")
    print(f"  分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 70)

    stage_data = {}
    for tag in tags:
        results = read_results(tag)
        valid = [r for r in results if r.get("is", {}).get("sharpe") is not None]
        errors = [r for r in results if r.get("is", {}).get("sharpe") is None]
        sharpes = [abs(r["is"]["sharpe"]) for r in valid]
        mean_shr = sum(sharpes) / len(sharpes) if sharpes else 0
        max_shr = max(sharpes) if sharpes else 0
        median_shr = sorted(sharpes)[len(sharpes)//2] if sharpes else 0
        stage_data[tag] = {
            "total": len(results),
            "valid": len(valid),
            "errors": len(errors),
            "mean_abs_shr": mean_shr,
            "max_abs_shr": max_shr,
            "median_abs_shr": median_shr,
            "submittable": sum(1 for r in valid
                               if abs(r["is"]["sharpe"]) >= SHARPE_THRESHOLD
                               and r["is"].get("fitness", 0) >= FITNESS_THRESHOLD),
            "top3_fields": [extract_field(r["expression"]) for r in
                            sorted(valid, key=lambda x: abs(x["is"]["sharpe"]), reverse=True)[:3]]
        }

    # 对比表
    print(f"\n{'阶段':<16} {'总数':>5} {'有效':>5} {'错误':>5} {'Mean|S|':>8} {'Median|S|':>10} {'Max|S|':>7} {'可提交':>6}")
    print(f"{'─'*80}")
    for tag in tags:
        d = stage_data[tag]
        print(f"{tag:<16} {d['total']:>5} {d['valid']:>5} {d['errors']:>5} "
              f"{d['mean_abs_shr']:>8.3f} {d['median_abs_shr']:>10.3f} "
              f"{d['max_abs_shr']:>7.3f} {d['submittable']:>6}")

    # 进步分析
    print(f"\n  进步分析:")
    for i in range(1, len(tags)):
        prev = stage_data[tags[i-1]]
        curr = stage_data[tags[i]]
        if prev["max_abs_shr"] > 0:
            improvement = (curr["max_abs_shr"] - prev["max_abs_shr"]) / prev["max_abs_shr"] * 100
            mean_improvement = (curr["mean_abs_shr"] - prev["mean_abs_shr"]) / prev["mean_abs_shr"] * 100
            print(f"  {tags[i-1]} → {tags[i]}:")
            print(f"    Max|S| 变化: {prev['max_abs_shr']:.3f} → {curr['max_abs_shr']:.3f} ({improvement:+.1f}%)")
            print(f"    Mean|S| 变化: {prev['mean_abs_shr']:.3f} → {curr['mean_abs_shr']:.3f} ({mean_improvement:+.1f}%)")
            print(f"    可提交数: {prev['submittable']} → {curr['submittable']}")

    # Top 3 字段对比
    print(f"\n  Top 3 字段对比:")
    for tag in tags:
        d = stage_data[tag]
        print(f"  {tag}: {', '.join(d['top3_fields'])}")

    print("═" * 70)


# ==================== Main ====================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GLB Alpha 因子归因分析")
    parser.add_argument("tag", help="结果标签, 如 glb_first")
    parser.add_argument("--top", type=int, default=15, help="Top N 候选数")
    parser.add_argument("--save", action="store_true", help="保存 HTML 报告")
    parser.add_argument("--compare", nargs="+", help="额外标签用于跨阶段对比, 如 glb_second glb_third")
    args = parser.parse_args()

    analyze(args.tag, top_n=args.top, save_html=args.save)

    if args.compare:
        compare_stages([args.tag] + args.compare)