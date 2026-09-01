#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quality_predict.py — 候选池质量预估模型（建议3落地，2026-08-27）

回测前对候选表达式做三维质量预估，避免烧配额 + 提前拦截高相关候选：

  1. Sharpe/Fitness 预估：三层先验从历史回测学习（Bayes 收缩）
     - 字段族先验：含该字段族的历史样本 Sharpe/Fitness 分布
     - 骨架先验：同骨架类型历史均值
     - 数据集先验：同数据集历史均值
     预估 = 加权合成（样本数越多权重越高），样本不足时回退全局先验
  2. SELF_CORRELATION 风险预估（本地结构代理，不烧平台配额）：
     - 字段重叠：与存量 alpha（ACTIVE/UNSUBMITTED）的字段交集占比
     - 结构相似度：算子多重集 Jaccard × 骨架匹配
     - 字段族饱和度：该字段族存量 alpha 数
  3. 综合判定：EXPECTED_PASS / REVIEW / EXPECTED_BLOCK

输入源：--file > --exprs > --status（存量 alpha 按状态，如 UNSUBMITTED 候选池） > DB（--region --wave [--dataset]）
用法:
  python tools/quality_predict.py --region USA --wave 28
  python tools/quality_predict.py --region USA --status UNSUBMITTED
  python tools/quality_predict.py --file candidates.txt --json out.json
退出码: 0=无 EXPECTED_BLOCK, 1=存在 EXPECTED_BLOCK
"""
import argparse
import collections
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pool_diversity import (  # noqa: E402  复用建议2工具的解析层
    extract_ops, extract_fields, classify_skeleton, field_family,
    jaccard_multiset,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 原阈值（平台提交标准）
SHARPE_GATE = 1.58
FITNESS_GATE = 1.0
SELF_CORR_GATE = 0.7

# 新增：分层阈值（Wave 1 单字段候选池）
SHARPE_COMBO_GATE = 1.0      # 组合候选池 Sharpe 下限
FITNESS_COMBO_GATE = 0.8     # 组合候选池 Fitness 下限
TURNOVER_COMBO_GATE = 0.4    # 组合候选池 Turnover 上限

# 新增：硬拒绝线（直接丢弃）
SHARPE_HARD_REJECT = 0.5
FITNESS_HARD_REJECT = 0.3
TURNOVER_HARD_REJECT = 0.6


# ---------------- 先验学习 ----------------

def _dataset_id_to_name(conn):
    """alphas.dataset_id (INTEGER) -> datasets.name (TEXT) 映射。"""
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name FROM datasets")
        return {row[0]: row[1] for row in cur.fetchall()}
    except sqlite3.OperationalError:
        return {}


def load_history(conn, region=None):
    """从 alphas + backtest_results 加载历史回测样本。"""
    cur = conn.cursor()
    id2name = _dataset_id_to_name(conn)
    cur.execute(
        "SELECT expression, dataset_id, sharpe, fitness, self_correlation "
        "FROM alphas WHERE sharpe IS NOT NULL AND fitness IS NOT NULL"
    )
    samples = []
    for expr, ds, sh, fit, sc in cur.fetchall():
        if not expr:
            continue
        ds_name = id2name.get(ds, str(ds) if ds else None)
        samples.append({
            'expr': expr, 'dataset': ds_name,
            'sharpe': sh, 'fitness': fit, 'self_corr': sc,
            'ops': extract_ops(expr), 'fields': extract_fields(expr),
            'skeleton': classify_skeleton(expr),
        })
    return samples


def bayes_mean(values, global_mean, k=5):
    """Bayes 收缩均值：样本少时向全局均值收缩。"""
    n = len(values)
    if n == 0:
        return global_mean, 0
    return (sum(values) + k * global_mean) / (n + k), n


def build_priors(samples):
    """构建三层先验：字段族 / 骨架 / 数据集。"""
    g_sh = [s['sharpe'] for s in samples]
    g_fit = [s['fitness'] for s in samples]
    global_sh = sum(g_sh) / len(g_sh) if g_sh else 0.0
    global_fit = sum(g_fit) / len(g_fit) if g_fit else 0.0

    fam_sh, fam_fit = collections.defaultdict(list), collections.defaultdict(list)
    skel_sh, skel_fit = collections.defaultdict(list), collections.defaultdict(list)
    ds_sh, ds_fit = collections.defaultdict(list), collections.defaultdict(list)
    for s in samples:
        for f in set(field_family(x) for x in s['fields']):
            fam_sh[f].append(s['sharpe'])
            fam_fit[f].append(s['fitness'])
        skel_sh[s['skeleton']].append(s['sharpe'])
        skel_fit[s['skeleton']].append(s['fitness'])
        if s['dataset']:
            ds_sh[s['dataset']].append(s['sharpe'])
            ds_fit[s['dataset']].append(s['fitness'])
    return {
        'global': (global_sh, global_fit, len(samples)),
        'family_sharpe': {k: bayes_mean(v, global_sh) for k, v in fam_sh.items()},
        'family_fitness': {k: bayes_mean(v, global_fit) for k, v in fam_fit.items()},
        'skeleton_sharpe': {k: bayes_mean(v, global_sh) for k, v in skel_sh.items()},
        'skeleton_fitness': {k: bayes_mean(v, global_fit) for k, v in skel_fit.items()},
        'dataset_sharpe': {k: bayes_mean(v, global_sh) for k, v in ds_sh.items()},
        'dataset_fitness': {k: bayes_mean(v, global_fit) for k, v in ds_fit.items()},
    }


def predict_metrics(fields, skeleton, dataset, priors):
    """三层先验加权合成（按各层样本数归一化）。"""
    g_sh, g_fit, _ = priors['global']
    sh_terms, fit_terms, weights = [], [], []

    # 数据集层（最具体，权重基础 3）
    if dataset and dataset in priors['dataset_sharpe']:
        m, n = priors['dataset_sharpe'][dataset]
        m_f, _ = priors['dataset_fitness'][dataset]
        w = min(n, 20) / 20 * 3
        sh_terms.append(m * w); fit_terms.append(m_f * w); weights.append(w)
    # 骨架层（权重基础 2）
    if skeleton in priors['skeleton_sharpe']:
        m, n = priors['skeleton_sharpe'][skeleton]
        m_f, _ = priors['skeleton_fitness'][skeleton]
        w = min(n, 30) / 30 * 2
        sh_terms.append(m * w); fit_terms.append(m_f * w); weights.append(w)
    # 字段族层（权重基础 2，多字段族取均值）
    fams = sorted({field_family(f) for f in fields})
    fam_sh_vals, fam_fit_vals = [], []
    for f in fams:
        if f in priors['family_sharpe']:
            fam_sh_vals.append(priors['family_sharpe'][f][0])
            fam_fit_vals.append(priors['family_fitness'][f][0])
    if fam_sh_vals:
        w = 2
        sh_terms.append(sum(fam_sh_vals) / len(fam_sh_vals) * w)
        fit_terms.append(sum(fam_fit_vals) / len(fam_fit_vals) * w)
        weights.append(w)

    total_w = sum(weights)
    if total_w == 0:
        return g_sh, g_fit, 'global_fallback'
    return (sum(sh_terms) / total_w, sum(fit_terms) / total_w,
            '+'.join(['ds', 'skel', 'fam'][:len(weights)]) or 'mix')


# ---------------- SELF_CORRELATION 风险预估 ----------------

def predict_self_corr_risk(expr_info, stock):
    """本地结构代理预估：字段重叠 × 结构相似度 × 字段族饱和度。
    跳过与候选表达式完全相同的存量记录（避免自撞分=1.0 误报）。"""
    fields_set = set(expr_info['fields'])
    best = {'score': 0.0, 'against': None, 'field_overlap': 0.0, 'struct_sim': 0.0}
    for s in stock:
        if s.get('expr') == expr_info.get('expr'):
            continue
        s_fields = set(s['fields'])
        union_f = fields_set | s_fields
        overlap = len(fields_set & s_fields) / len(union_f) if union_f else 0.0
        struct = jaccard_multiset(expr_info['ops'], s['ops'])
        if s['skeleton'] == expr_info['skeleton']:
            struct = min(struct + 0.1, 1.0)
        # 综合分：字段重叠 60% + 结构相似 40%（字段相同结构不同也会高相关）
        score = 0.6 * overlap + 0.4 * struct
        if score > best['score']:
            best = {'score': round(score, 3), 'against': s.get('alpha_id', '?'),
                    'field_overlap': round(overlap, 3), 'struct_sim': round(struct, 3)}
    fams = {field_family(f) for f in expr_info['fields']}
    sat = max((s['family_counts'].get(f, 0) for f in fams), default=0) \
        if expr_info['fields'] and 'family_counts' in s else 0
    return best, sat


def load_stock(conn, region):
    """存量 alpha（用于相关性代理预估）。alphas 存 region_id，经 regions 表映射。"""
    cur = conn.cursor()
    cur.execute(
        "SELECT a.alpha_id, a.expression, a.status FROM alphas a "
        "JOIN regions r ON a.region_id = r.id "
        "WHERE r.name=? AND a.status IN ('ACTIVE', 'UNSUBMITTED')", (region,)
    )
    stock = []
    fam_counts = collections.Counter()
    for aid, expr, status in cur.fetchall():
        if not expr:
            continue
        fields = extract_fields(expr)
        stock.append({
            'alpha_id': aid, 'status': status, 'expr': expr,
            'ops': extract_ops(expr), 'fields': fields,
            'skeleton': classify_skeleton(expr),
        })
        for f in set(field_family(x) for x in fields):
            fam_counts[f] += 1
    for s in stock:
        s['family_counts'] = fam_counts
    return stock


# ---------------- 主流程 ----------------

def load_from_db(region, wave, dataset=None):
    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'data', 'wqb.db'))
    cur = conn.cursor()
    sql = "SELECT expression, dataset FROM expressions WHERE region=? AND wave=?"
    params = [region, str(wave)]
    if dataset:
        sql += " AND dataset=?"
        params.append(dataset)
    cur.execute(sql, params)
    rows = [(r[0], r[1]) for r in cur.fetchall() if r[0]]
    conn.close()
    return rows


def load_candidates_by_status(conn, region, status):
    """从 alphas 表按状态拉候选（如 UNSUBMITTED 存量池），dataset_id 映射为名称。"""
    cur = conn.cursor()
    id2name = _dataset_id_to_name(conn)
    cur.execute(
        "SELECT a.expression, a.dataset_id FROM alphas a "
        "JOIN regions r ON a.region_id = r.id WHERE r.name=? AND a.status=?",
        (region, status))
    return [(expr, id2name.get(ds)) for expr, ds in cur.fetchall() if expr]


def predict_all(candidates, region, conn):
    """candidates: [(expr, dataset_or_None), ...]"""
    samples = load_history(conn, region)
    priors = build_priors(samples)
    stock = load_stock(conn, region)

    results = []
    for expr, ds in candidates:
        info = {
            'expr': expr,
            'ops': extract_ops(expr),
            'fields': extract_fields(expr),
            'skeleton': classify_skeleton(expr),
        }
        p_sh, p_fit, basis = predict_metrics(info['fields'], info['skeleton'], ds, priors)
        corr_best, fam_sat = predict_self_corr_risk(info, stock) if stock else (
            {'score': 0.0, 'against': None, 'field_overlap': 0.0, 'struct_sim': 0.0}, 0)

        reasons = []
        # 硬拒绝线检查（仅 Sharpe/Fitness 过低时直接丢弃；Turnover 高可通过优化降低，不作为硬拒绝）
        if p_sh < SHARPE_HARD_REJECT:
            reasons.append(f"预估Sharpe {p_sh:.2f} < {SHARPE_HARD_REJECT}（硬拒绝）")
        if p_fit < FITNESS_HARD_REJECT:
            reasons.append(f"预估Fitness {p_fit:.2f} < {FITNESS_HARD_REJECT}（硬拒绝）")
        
        # 优选线检查（平台提交标准）
        if p_sh < SHARPE_GATE:
            reasons.append(f"预估Sharpe {p_sh:.2f} < {SHARPE_GATE}")
        if p_fit < FITNESS_GATE:
            reasons.append(f"预估Fitness {p_fit:.2f} < {FITNESS_GATE}")
        
        # 相关性检查
        if corr_best['score'] >= SELF_CORR_GATE:
            reasons.append(f"相关性代理分 {corr_best['score']:.2f} >= {SELF_CORR_GATE}（疑似撞 {corr_best['against']}）")
        if fam_sat >= 30:
            reasons.append(f"字段族饱和：存量同族 alpha {fam_sat} 个")

        # 分层判定逻辑（注意判定顺序：相关性优先，避免高 Sharpe 信号被 Turnover 误杀）
        if reasons and any('相关性' in r or '饱和' in r for r in reasons):
            verdict = 'EXPECTED_BLOCK'  # 相关性/饱和度超标（最高优先级）
        elif reasons and any('硬拒绝' in r for r in reasons):
            verdict = 'HARD_REJECT'  # 直接丢弃（Sharpe/Fitness 过低）
        elif p_sh >= SHARPE_GATE and p_fit >= FITNESS_GATE:
            verdict = 'DIRECT_SUBMIT'  # 优选线：单字段已达标
        elif p_sh >= SHARPE_COMBO_GATE and p_fit >= FITNESS_COMBO_GATE:
            verdict = 'COMBO_CANDIDATE'  # 候选池线：可作为组合腿
        else:
            verdict = 'WEAK_SIGNAL'  # 弱信号，仅当组合池不足时考虑

        results.append({
            'expr': expr[:120],
            'skeleton': info['skeleton'],
            'fields': info['fields'],
            'pred_sharpe': round(p_sh, 2),
            'pred_fitness': round(p_fit, 2),
            'pred_basis': basis,
            'corr_risk': corr_best,
            'family_saturation': fam_sat,
            'verdict': verdict,
            'reasons': reasons,
        })
    return results, priors


def main():
    ap = argparse.ArgumentParser(description='候选池质量预估模型')
    ap.add_argument('--region', default='USA', help='区域（默认 USA）')
    ap.add_argument('--wave', help='波次（DB 模式）')
    ap.add_argument('--dataset', help='数据集（DB 模式可选）')
    ap.add_argument('--status', help='从 alphas 表按状态拉候选（如 UNSUBMITTED）')
    ap.add_argument('--file', help='候选表达式文件（每行一条）')
    ap.add_argument('--exprs', nargs='+', help='直接传表达式')
    ap.add_argument('--json', help='结构化报告落盘路径')
    a = ap.parse_args()

    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, 'data', 'wqb.db'))
    if a.file:
        with open(a.file, encoding='utf-8') as fh:
            candidates = [(ln.strip(), None) for ln in fh
                          if ln.strip() and not ln.startswith('#')]
    elif a.exprs:
        candidates = [(e, None) for e in a.exprs]
    elif a.status:
        candidates = load_candidates_by_status(conn, a.region, a.status)
    elif a.wave:
        candidates = load_from_db(a.region, a.wave, a.dataset)
    else:
        ap.error('需要 --file / --exprs / --status / --wave')

    if not candidates:
        print('[error] 无候选表达式')
        sys.exit(1)

    results, priors = predict_all(candidates, a.region, conn)
    conn.close()

    n_direct = sum(1 for r in results if r['verdict'] == 'DIRECT_SUBMIT')
    n_combo = sum(1 for r in results if r['verdict'] == 'COMBO_CANDIDATE')
    n_weak = sum(1 for r in results if r['verdict'] == 'WEAK_SIGNAL')
    n_blk = sum(1 for r in results if r['verdict'] == 'EXPECTED_BLOCK')
    n_hard = sum(1 for r in results if r['verdict'] == 'HARD_REJECT')
    g = priors['global']
    print(f"[质量预估] 候选 {len(results)} 条 | 先验样本 {g[2]} 条（全局均值 "
          f"Sharpe={g[0]:.2f}, Fitness={g[1]:.2f}）")
    print(f"[分层判定] DIRECT_SUBMIT={n_direct} COMBO_CANDIDATE={n_combo} "
          f"WEAK_SIGNAL={n_weak} EXPECTED_BLOCK={n_blk} HARD_REJECT={n_hard}")
    print(f"[阈值] 优选线 S≥{SHARPE_GATE}/F≥{FITNESS_GATE} | "
          f"候选池 S≥{SHARPE_COMBO_GATE}/F≥{FITNESS_COMBO_GATE} | "
          f"硬拒绝 S<{SHARPE_HARD_REJECT}/F<{FITNESS_HARD_REJECT}")
    for i, r in enumerate(results, 1):
        print(f"\n{i}. [{r['verdict']}] {r['expr']}")
        print(f"   骨架={r['skeleton']} 字段={r['fields']}")
        print(f"   预估 Sharpe={r['pred_sharpe']} Fitness={r['pred_fitness']}（依据: {r['pred_basis']}）")
        c = r['corr_risk']
        print(f"   相关性代理分={c['score']}（字段重叠={c['field_overlap']}, 结构相似={c['struct_sim']}, "
              f"疑似撞 {c['against']}）字段族饱和度={r['family_saturation']}")
        if r['reasons']:
            for reason in r['reasons']:
                print(f"   - {reason}")

    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump({'summary': {
                           'direct_submit': n_direct,
                           'combo_candidate': n_combo,
                           'weak_signal': n_weak,
                           'expected_block': n_blk,
                           'hard_reject': n_hard
                       },
                       'thresholds': {
                           'sharpe_gate': SHARPE_GATE,
                           'fitness_gate': FITNESS_GATE,
                           'sharpe_combo_gate': SHARPE_COMBO_GATE,
                           'fitness_combo_gate': FITNESS_COMBO_GATE,
                           'sharpe_hard_reject': SHARPE_HARD_REJECT,
                           'fitness_hard_reject': FITNESS_HARD_REJECT
                       },
                       'candidates': results}, fh, ensure_ascii=False, indent=2)
        print(f"\n[done] 报告已落盘: {a.json}")
    # 退出码：存在 EXPECTED_BLOCK 或 HARD_REJECT 时返回 1
    sys.exit(1 if (n_blk or n_hard) else 0)


if __name__ == '__main__':
    main()
