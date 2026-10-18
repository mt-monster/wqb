# -*- coding: utf-8 -*-
"""potential_scan.py — 区域数据集潜力扫描（零成本，探针 SOP 第 0 步 + 历史闸）

用法：
    python scripts/potential_scan.py --region DEU
    python scripts/potential_scan.py --region DEU --out cache/deu_scan.json

产出：每个数据集的
  - avail  : cov>=0.6 的字段数（可用面）
  - fams   : 概念族数（字段名首词聚类）→ 族多 = 跨族探针空间大
  - zero   : α=0 字段占比（真空白）
  - tested : 已实测字段占比（精确匹配 code 分词 vs 字段名）
  - bestS / best1field / maxfields : 历史读数与合规性判定
分档：
  ★★ 多腿强信号（bestS>=1.58 且 历史行最多字段>=2）—— 信号存在但需合规重表达
  ★  单信号历史已过闸（需复核 code，可能是 R## 标签行）
  ☆  单信号近失带 1.0–1.58（结构升级候选，SOP 的「不判死」带）
  ○  弱信号  × 低产
⚠ 必须过滤 R## 标签行（code 形如 R83 / R102），否则标签会把「合规」判定污染成假阳性。
"""
import argparse, collections, json, os, re, sqlite3, sys

AXIS = {'sector','industry','subindustry','market','country','exchange','sector_country',
        'industry_country','sector_exchange','bucket','rank','cap','close','open','high','low',
        'vwap','volume','returns','adv20','adv60','sharesout','date','range','std','hump','target_tvr'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--region', required=True)
    ap.add_argument('--db', default='data/wqb.db')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    con = sqlite3.connect(a.db); cur = con.cursor()
    cur.execute("SELECT id FROM regions WHERE name=?", (a.region,))
    row = cur.fetchone()
    if not row:
        sys.exit(f"region {a.region} 不在 regions 表")
    rid = row[0]

    allf = {r[0] for r in cur.execute(
        "SELECT DISTINCT field_name FROM fields WHERE dataset_id IN (SELECT id FROM datasets WHERE region_id=?)", (rid,))}
    cat = {n: (c or '?') for n, c in cur.execute("SELECT name, category FROM datasets WHERE region_id=?", (rid,))}

    def is_tag(code):
        c = (code or '').strip()
        return bool(re.fullmatch(r'R\d+[a-z_]*', c)) or len(c) < 12

    def biz(code):
        return {t for t in re.findall(r'[A-Za-z_][A-Za-z0-9_]{4,}', code or '')
                if t in allf and t not in AXIS
                and not t.startswith(('oth455_', 'pv29', 'pv30'))}

    agg, n_tag, n_real = {}, 0, 0
    for ds, s, code in cur.execute(
            "SELECT dataset, sharpe, code FROM backtest_results WHERE region=? AND dataset IS NOT NULL AND sharpe IS NOT NULL", (a.region,)):
        if is_tag(code):
            n_tag += 1; continue
        n_real += 1
        n = len(biz(code))
        d = agg.setdefault(ds, dict(bestS=-9.0, comp=-9.0, nf=0, n=0))
        d['n'] += 1; d['bestS'] = max(d['bestS'], s); d['nf'] = max(d['nf'], n)
        if n <= 1:
            d['comp'] = max(d['comp'], s)

    tested = set()
    for (code,) in cur.execute("SELECT code FROM backtest_results WHERE region=? AND code IS NOT NULL", (a.region,)):
        for tok in re.findall(r'[A-Za-z_][A-Za-z0-9_]{4,}', code or ''):
            if tok in allf:
                tested.add(tok)

    stats = {}
    for did, name in cur.execute("SELECT id, name FROM datasets WHERE region_id=?", (rid,)).fetchall():
        cur.execute("SELECT field_name, coverage, alpha_count FROM fields WHERE dataset_id=?", (did,))
        fs = cur.fetchall()
        av = [f for f in fs if (f[1] or 0) >= 0.6]
        sig = [f for f in av if not any(k in f[0] for k in ('_cluster_', 'grouping', 'group_'))]
        fams = len({re.split(r'[_0-9]', f[0])[0] for f in sig})
        zero = sum(1 for f in sig if (f[2] or 0) == 0)
        nt = sum(1 for f in sig if f[0] in tested)
        stats[name] = dict(avail=len(sig), fams=fams,
                           zero_ratio=(zero / len(sig) if sig else 0),
                           tested_ratio=(nt / len(sig) if sig else 1.0))

    res = []
    for ds, d in agg.items():
        c = None if d['comp'] <= -9 else d['comp']
        st = stats.get(ds, {})
        if d['bestS'] >= 1.58 and d['nf'] >= 2:
            v = '★★ 多腿强信号（可合规重表达）'
        elif d['bestS'] >= 1.58:
            v = '★ 单信号历史已过闸（需复核 code，可能是标签行）'
        elif c is not None and c >= 1.0:
            v = '☆ 单信号近失带 1.0–1.58'
        elif d['bestS'] >= 1.0:
            v = '○ 弱信号'
        else:
            v = '× 低产'
        res.append(dict(ds=ds, cat=cat.get(ds) or '?', rows=d['n'], maxfields=d['nf'],
                        bestS=round(d['bestS'], 2), best1field=(round(c, 2) if c is not None else None),
                        verdict=v, **st))
    order = {'★★': 0, '★': 1, '☆': 2, '○': 3, '×': 4}
    res.sort(key=lambda r: (order[r['verdict'][0]], -r['bestS']))

    print(f"[{a.region}] 台账行：标签行 {n_tag} 剔除 / 真实表达式行 {n_real}")
    print(f"{'数据集':<24}{'类别':<13}{'行':>4}{'字段':>5}{'最优S':>7}{'单字段S':>8}{'可用':>5}{'族':>4}{'空自比':>7}{'探测':>6}  判读")
    for r in res:
        c2 = f"{r['best1field']:.2f}" if r['best1field'] is not None else "  --"
        print(f"{r['ds']:<24}{r['cat']:<13}{r['rows']:>4}{r['maxfields']:>5}{r['bestS']:>7.2f}{c2:>8}"
              f"{r.get('avail',0):>5}{r.get('fams',0):>4}{r.get('zero_ratio',0):>7.0%}{r.get('tested_ratio',0):>6.0%}  {r['verdict']}")
    if a.out:
        os.makedirs(os.path.dirname(a.out), exist_ok=True)
        json.dump(res, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"\n已写出 {a.out}")


if __name__ == '__main__':
    main()
