#!/usr/bin/env python3
"""WebDataScope 数据包 → 数据集/字段/中性化/预处理全景分析。

用法:
    python3 tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region USA --delay 1
    python3 tools/webdata_quality.py --zip WebData_20260219_V0.10.9.zip --region USA --delay 1 \
        --fields analyst11 --json-out tracking/quality_analyst11.json

功能:
    1. 数据集质量排名 (count/sharpe/fitness) + 甜点区 (100≤count≤3000 且 sharpe≥1.1×均值)
    2. 每数据集最优中性化 (count≥20 且 osis_count≥20 可信)
    3. 字段使用先验 (count/sharpe/fitness) + 每字段最优中性化
    4. 字段级数据体检 (仅当该组合在 dataSetList.json 中):
       - CoverageRatio 均值/趋势 / 单边性 / 离散性 / 偏度峰度 / 更新频率 / 值域
       - 从 yearly_distribution 解析值域分布形状 → 预处理算子建议
    5. OS 退化检测: osis_data.bin（OS-only） vs info_data.bin（IS+OS）数据集/类别级对照
    6. 类别级统计: isos.category + neutralization.category

依赖: pip install msgpack
"""
import argparse, json, re, zipfile, zlib

import msgpack

# 中位数分位段 → 分布形状判定
DIST_SHAPE_RULES = [
    # (描述, 匹配函数)
]


def load_bin(zf: zipfile.ZipFile, name: str):
    return msgpack.unpackb(zlib.decompress(zf.read(name)), strict_map_key=False)


def parse_yearly_distribution(dist_str: str):
    """解析 '{(0, 0.05): 0.6499, ...}' 字符串 → [(lo, hi, freq), ...]"""
    try:
        pairs = re.findall(r'\((\d+\.?\d*), (\d+\.?\d*)\):\s*([\d.]+)', dist_str or '')
        return [(float(lo), float(hi), float(f)) for lo, hi, f in pairs]
    except Exception:
        return []


def classify_distribution(dist):
    """从分位直方图推导分布形状与预处理建议。
    dist: [(lo, hi, freq), ...] 单年分位分布
    返回 (shape_label, advice)
    """
    if not dist:
        return ('unknown', '无分布数据')
    # 排除最后一档 (0.95, 1] 后看主体集中度
    vals = [f for _, _, f in dist]
    total = sum(vals)
    if total <= 0:
        return ('unknown', '分布总频次为 0')
    # 主体(90%)所在区间
    sorted_by_freq = sorted(dist, key=lambda x: -x[2])
    top_share = sorted_by_freq[0][2] / total
    # 看 [0,0.1) 或 [0.9,1] 频次 → 截尾/单峰
    low_tail = sum(f for lo, hi, f in dist if hi <= 0.1) / total
    high_tail = sum(f for lo, hi, f in dist if lo >= 0.9) / total
    # 前 3 档占比
    top3_share = sum(f for _, _, f in sorted_by_freq[:3]) / total

    if top_share > 0.9:
        return ('point_mass', '值域集中单一档位（近似常量/离散哑变量）→ rank/变化率无效，检查是否事件/哑变量')
    if low_tail > 0.5:
        return ('zero_inflated', '大量 0 值（>50% 落在 [0,0.1)）→ 事件/稀疏字段，配合 ts_backfill 或事件门控')
    if high_tail > 0.5:
        return ('ceiling', '大量值接近上界（截尾）→ winsorize/rank/densify 抑制')
    if top3_share > 0.7:
        return ('concentrated', '分布高度集中前 3 档 → 有效信息少，慎作主信号')
    return ('spread', '分布较分散 → 可直接使用或轻度预处理')


def mean_year(arr):
    return sum(arr) / len(arr) if arr else 0


def field_inspect(field_name, fdata):
    """对单字段体检数据生成预处理建议。"""
    cr = fdata.get('CoverageRatio', [])
    pos_r = fdata.get('IndicativePositiveRatio', [])
    neg_r = fdata.get('IndicativeNegativeRatio', [])
    int_s = fdata.get('IntegerStatus', [])
    freq = fdata.get('frequency', [])
    skew = fdata.get('skenewss', [])
    kurt = fdata.get('kurtosis', [])
    long_c = fdata.get('LongCount', [])
    short_c = fdata.get('ShortCount', [])

    cr_mean = mean_year(cr)
    pos_mean = mean_year(pos_r)
    neg_mean = mean_year(neg_r)
    int_has_one = any(int_s)
    skew_abs_mean = abs(mean_year(skew))
    kurt_mean = mean_year(kurt)

    advices = []
    if cr_mean < 0.4:
        advices.append('覆盖率<0.4 → 必须 ts_backfill/group_backfill，否则 CONCENTRATED_WEIGHT')
    # 覆盖趋势: 早年低近年高
    if len(cr) >= 5:
        early = mean_year(cr[:3])
        late = mean_year(cr[-3:])
        if late > early * 1.3:
            advices.append(f'覆盖厂字形 (早{early:.2f}→近{late:.2f}) → 数据商中途扩容，回测注意早年失真')
    if pos_mean > 0.95:
        advices.append(f'单边恒正(正值{pos_mean:.2f}) → 勿用原始水平做多空，先变化率/排名/与基准差')
    if neg_mean > 0.95:
        advices.append(f'单边恒负(负值{neg_mean:.2f}) → 同上，先变化率/排名')
    if int_has_one and cr_mean > 0.3:
        advices.append('含整数值(离散/评分/计数) → 优先 rank/bucket/group_rank，慎用平滑算子与 ts_delta')
    if skew_abs_mean > 2:
        advices.append(f'偏度|{mean_year(skew):.2f}|高 → 外层 rank/signed_power(x,<1)/winsorize 抑制极值')
    if kurt_mean > 8:
        advices.append(f'峰度{kurt_mean:.1f}高(厚尾) → 外层 rank/winsorize')
    if freq:
        f0 = freq[0] if isinstance(freq[0], str) else str(freq[0])
        if f0 in ('monthly', 'quarterly'):
            advices.append(f'更新频率{f0}低 → 时序窗口≥更新周期(月度≥21d季度≥63d)，短窗只采样噪声')
        elif f0 == 'weekly':
            advices.append(f'更新频率weekly → 时序窗口≥5d')
    if long_c and short_c:
        lm, sm = mean_year(long_c), mean_year(short_c)
        if sm > 0 and lm > 0 and (lm / sm > 3 or sm / lm > 3):
            advices.append(f'多空样本失衡(Long{lm:.0f}/Short{sm:.0f}) → 检查 signed_power/双 rank 平衡')
        elif sm == 0 and lm > 0:
            advices.append(f'纯多头样本(Long{lm:.0f}/Short0) → 必须对称化(减均值/双序 rank)')
    # 分布形状
    yd = fdata.get('yearly_distribution', '')
    if isinstance(yd, str) and (yd.startswith('{') or yd.startswith('[')):
        dist = parse_yearly_distribution(yd)
        if dist:
            shape, da = classify_distribution(dist)
            if shape in ('zero_inflated', 'point_mass', 'ceiling', 'concentrated'):
                advices.append(da)
    return advices


def universe_coverage(dsl):
    """从 dataSetList.json 统计每个 region_universe 的体检覆盖数。"""
    cov = {}
    for entry in dsl:
        # 格式: <dataset>_<REGION>_<UNIVERSE>_Delay<N>
        try:
            parts = entry.rsplit('_Delay', 1)[0].split('_')
            # 数据集名可能含下划线，所以从右往左取：universe 倒数第1，region 倒数第2
            universe = parts[-1]
            region = parts[-2]
            ru = f'{region}_{universe}'
            cov[ru] = cov.get(ru, 0) + 1
        except Exception:
            continue
    return cov


def cross_region_diff(info, osis, target_region, delay, top_n=20):
    """对比同数据集在多个 region 的 sharpe，识别 region-specific alpha 潜力。"""
    target_key = f'{target_region}_{delay}'
    if target_key not in info:
        return []
    target_ds = info[target_key]['isos'].get('dataset', {})
    rows = []
    for other_key, other_rd in info.items():
        if not other_key.endswith(f'_{delay}') or other_key == target_key:
            continue
        other_region = other_key.rsplit('_', 1)[0]
        other_ds = other_rd['isos'].get('dataset', {})
        for ds, ts in target_ds.items():
            if ds not in other_ds:
                continue
            t_sharpe = ts.get('sharpe_ratio', 0)
            o_sharpe = other_ds[ds].get('sharpe_ratio', 0)
            t_count = ts.get('count', 0)
            o_count = other_ds[ds].get('count', 0)
            if t_count < 100 and o_count < 100:
                continue
            rows.append({
                'dataset': ds,
                'target': target_region, 't_sharpe': round(t_sharpe, 3), 't_count': t_count,
                'other': other_region, 'o_sharpe': round(o_sharpe, 3), 'o_count': o_count,
                'diff': round(t_sharpe - o_sharpe, 3),
            })
    # 按 |diff| 降序
    rows.sort(key=lambda r: -abs(r['diff']))
    return rows[:top_n]


def field_combine_hints(field_shapes):
    """根据字段分布形状提出 2-field 组合建议。"""
    # 按形状分桶
    buckets = {'point_mass': [], 'zero_inflated': [], 'ceiling': [],
               'concentrated': [], 'spread': [], 'unknown': []}
    for fname, shape in field_shapes:
        buckets.setdefault(shape, []).append(fname)
    hints = []
    # 事件门控：point_mass / zero_inflated 作门控，spread 作主信号
    gating_fields = buckets['point_mass'] + buckets['zero_inflated']
    signal_fields = buckets['spread']
    if gating_fields and signal_fields:
        hints.append(f'事件门控候选: trade_when({gating_fields[0]}_cond, {signal_fields[0]}_expr, -1) — '
                     f'用 {gating_fields[0]} (稀疏事件) 作门控，{signal_fields[0]} (连续) 作主信号')
    # 截尾+稀疏：ceiling + zero_inflated 互补
    if buckets['ceiling'] and buckets['zero_inflated']:
        hints.append(f'互补组合候选: {buckets["ceiling"][0]} (截尾) × {buckets["zero_inflated"][0]} (稀疏) — '
                     f'不同分布形状降低结构相关性')
    # 多个 spread：双 rank 平衡
    if len(buckets['spread']) >= 2:
        hints.append(f'双信号候选: rank({buckets["spread"][0]}) - rank({buckets["spread"][1]}) — '
                     f'两个连续字段双 rank 去相关')
    # 多个 concentrated：慎作主信号
    if len(buckets['concentrated']) >= 2:
        hints.append(f'⚠ 多个 concentrated 字段 ({", ".join(buckets["concentrated"][:3])}) 有效信息少，'
                     f'优先作辅助/门控而非主信号')
    return hints


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', required=True)
    ap.add_argument('--region', default='USA')
    ap.add_argument('--delay', type=int, default=1)
    ap.add_argument('--top', type=int, default=30)
    ap.add_argument('--fields', default=None, help='逗号分隔的数据集列表, 输出字段级体检')
    ap.add_argument('--json-out', default=None)
    ap.add_argument('--cross-region', action='store_true',
                    help='输出同数据集在多 region 的 sharpe 对比 (识别 region-specific 机会)')
    args = ap.parse_args()

    key = f"{args.region}_{args.delay}"
    with zipfile.ZipFile(args.zip) as zf:
        info = load_bin(zf, 'data/oth/info_data.bin')
        try:
            osis = load_bin(zf, 'data/oth/osis_data.bin')
        except KeyError:
            osis = None
        dsl = json.loads(zf.read('data/dataSetList.json'))

    if key not in info:
        raise SystemExit(f"{key} 不在数据包中, 可用: {sorted(info)}")
    rd = info[key]
    isos = rd['isos']
    neut = rd['neutralization']
    mean_sharpe = isos['mean']['sharpe_ratio']
    mean_fitness = isos['mean']['fitness_ratio']
    window = f"{rd['sub_beg_time']} → {rd['sub_end_time']}"
    sweet_threshold = mean_sharpe * 1.1

    print(f'# {key} 社区提交统计  窗口 {window}')
    print(f'总量 {isos["total_count"]}  平均 sharpe {mean_sharpe:.3f} / fitness {mean_fitness:.3f}')
    print(f'甜点区阈值: sharpe ≥ {sweet_threshold:.3f} (区域均值×1.1) 且 100≤count≤3000\n')
    if osis and key in osis:
        os_mean = osis[key]['mean']['sharpe_ratio']
        print(f'OS-only 快照 (窗口 {osis[key]["sub_beg_time"]} → {osis[key]["sub_end_time"]}) 平均 sharpe {os_mean:.3f}')
        print(f'IS+OS 平均 {mean_sharpe:.3f} vs OS-only {os_mean:.3f} → 差 {mean_sharpe - os_mean:.3f}')
        if os_mean > mean_sharpe:
            print(f'  注: OS 高于 IS+OS 是选择性偏差 (只有通过筛选的 alpha 进 OS), 非退化信号')
        print()

    # ============ 0. Universe 体检覆盖矩阵 ============
    print(f'## Universe 体检覆盖 (dataSetList.json, 共 {len(dsl)} 组合)\n')
    ucov = universe_coverage(dsl)
    print('| region_universe | 体检数据集数 | 说明 |\n|---|---|---|')
    notes_map = {
        'USA_TOP3000': '主流, 竞争最激烈',
        'EUR_TOP1200': '欧洲, 中等覆盖',
        'CHN_TOP3000': '中国, 较少覆盖',
        'ASI_MINVOL1M': '亚洲低波动, 较少覆盖',
        'GLB_TOP3000': '全球, 较少覆盖',
        'GLB_MINVOL1M': '全球低波动',
        'JPN_TOP1600': '日本, 极少覆盖',
        'KOR_TOP600': '韩国, 极少覆盖',
    }
    for ru in sorted(ucov, key=lambda k: -ucov[k]):
        print(f"| {ru} | {ucov[ru]} | {notes_map.get(ru, '')} |")
    print(f'\n提示: 低覆盖 universe (KOR/JPN/CHN/GLB) 竞争小 → ProdCorr 风险低, 但需在 get_datafields coverage 上复核\n')

    # ============ 0b. 跨区域数据集对比 ============
    if args.cross_region:
        cr_rows = cross_region_diff(info, osis, args.region, args.delay, top_n=args.top)
        if cr_rows:
            print(f'## 跨区域数据集对比 (同数据集在多 region 的 sharpe 差异, |diff| Top{args.top})\n')
            print('| dataset | target | t_sharpe | t_count | other | o_sharpe | o_count | diff |\n|---|---|---|---|---|---|---|---|')
            for r in cr_rows:
                print(f"| {r['dataset']} | {r['target']} | {r['t_sharpe']} | {r['t_count']} | "
                      f"{r['other']} | {r['o_sharpe']} | {r['o_count']} | {r['diff']:+.3f} |")
            print(f'\n提示: |diff|>0.3 表示该数据集在两个 region 表现差异大, 可考虑 region-specific alpha\n')

    # ============ 1. 数据集质量排名 ============
    def best_neuts(nstats, min_n):
        rows = [(k, v['sharpe_ratio'], v['count'], v.get('osis_count', 0))
                for k, v in nstats.items()
                if v.get('count', 0) >= min_n and v.get('osis_count', 0) >= 5]
        return sorted(rows, key=lambda x: -x[1])[:3]

    ds_rows = []
    for ds, s in isos['dataset'].items():
        os_sharpe = None
        if osis and key in osis:
            os_sharpe = osis[key]['dataset'].get(ds, {}).get('sharpe_ratio')
        bn = best_neuts(neut['dataset'].get(ds, {}), 20)
        ds_rows.append({
            'dataset': ds, 'count': s.get('count', 0),
            'sharpe': round(s.get('sharpe_ratio', 0), 3),
            'fitness': round(s.get('fitness_ratio', 0), 3),
            'os_sharpe': round(os_sharpe, 3) if os_sharpe is not None else None,
            'best_neuts': [{'neut': n, 'sharpe': round(sh, 3), 'count': c, 'osis': int(os_c)}
                           for n, sh, c, os_c in bn]})
    ds_rows.sort(key=lambda r: -r['count'])
    sweet = sorted([r for r in ds_rows if 100 <= r['count'] <= 3000 and r['sharpe'] >= mean_sharpe * 1.1],
                   key=lambda r: -r['sharpe'])

    print(f'## 数据集 Top{args.top} (按提交数)\n')
    print('| dataset | count | sharpe | fitness | OS sharpe | best neuts |\n|---|---|---|---|---|---|')
    for r in ds_rows[:args.top]:
        os_txt = f"{r['os_sharpe']}" if r['os_sharpe'] is not None else '--'
        bn = ', '.join(f"{b['neut']}({b['sharpe']},n={b['count']},os={b['osis']})" for b in r['best_neuts'])
        print(f"| {r['dataset']} | {r['count']} | {r['sharpe']} | {r['fitness']} | {os_txt} | {bn} |")

    print(f'\n## 甜点区 (100≤count≤3000 且 sharpe≥1.1×均值)\n')
    print('| dataset | count | sharpe | fitness | OS sharpe |\n|---|---|---|---|---|')
    for r in sweet[:args.top]:
        os_txt = f"{r['os_sharpe']}" if r['os_sharpe'] is not None else '--'
        print(f"| {r['dataset']} | {r['count']} | {r['sharpe']} | {r['fitness']} | {os_txt} |")

    # ============ 2. OS 退化检测 ============
    print(f'\n## OS 退化检测 (IS+OS sharpe vs OS-only sharpe, 差>0.15 标记退化)\n')
    print('| dataset | count | IS+OS sharpe | OS sharpe | 差 | 判定 |\n|---|---|---|---|---|---|')
    degraded = []
    if osis and key in osis:
        os_ds = osis[key]['dataset']
        for r in ds_rows:
            if r['os_sharpe'] is None:
                continue
            diff = r['sharpe'] - r['os_sharpe']
            verdict = '⚠ 退化' if diff > 0.15 else ('🟢 稳健' if abs(diff) <= 0.15 else '✓ OS更优')
            if diff > 0.15:
                degraded.append(r['dataset'])
            print(f"| {r['dataset']} | {r['count']} | {r['sharpe']} | {r['os_sharpe']} | {diff:.3f} | {verdict} |")
        if degraded:
            print(f'\n⚠ 退化数据集: {", ".join(degraded)} → 降低优先级或要求更强鲁棒性证据')

    # ============ 3. 类别级统计 ============
    print(f'\n## 类别级统计 (isos.category + osis.category)\n')
    print('| category | count | sharpe | fitness | OS sharpe |\n|---|---|---|---|---|')
    for cat, s in sorted(isos['category'].items(), key=lambda x: -x[1]['count']):
        os_cat = None
        if osis and key in osis:
            os_cat = osis[key]['category'].get(cat, {}).get('sharpe_ratio')
        os_txt = f"{os_cat:.3f}" if os_cat is not None else '--'
        print(f"| {cat} | {s['count']} | {s['sharpe_ratio']:.3f} | {s['fitness_ratio']:.3f} | {os_txt} |")

    # ============ 4. 字段级体检 ============
    if args.fields:
        targets = [d.strip() for d in args.fields.split(',')]
        print(f'\n## 字段级体检 ({", ".join(targets)})\n')
        for ds_name in targets:
            # 匹配 dataSetList.json
            candidates = [n for n in dsl if n.startswith(f'{ds_name}_{args.region}_') and f'_Delay{args.delay}' in n]
            if not candidates:
                print(f'### {ds_name}: 不在数据包覆盖矩阵中 (dataSetList.json 无 {ds_name}_{args.region}_*_Delay{args.delay})')
                continue
            fname = candidates[0]
            try:
                with zipfile.ZipFile(args.zip) as zf:
                    ds_data = load_bin(zf, f'data/{fname}.bin')
            except KeyError:
                print(f'### {ds_name}: {fname}.bin 不存在 (仅 dataSetList 列出但缺 bin)')
                continue
            print(f'### {ds_name} ({fname}, {len(ds_data)} 字段)\n')
            field_shapes = []
            for field, fdata in sorted(ds_data.items()):
                adv = field_inspect(field, fdata)
                # 解析分布形状用于组合建议
                yd = fdata.get('yearly_distribution', '')
                shape = 'unknown'
                if isinstance(yd, str) and (yd.startswith('{') or yd.startswith('[')):
                    dist = parse_yearly_distribution(yd)
                    if dist:
                        shape, _ = classify_distribution(dist)
                field_shapes.append((field, shape))
                if adv:
                    cr = mean_year(fdata.get('CoverageRatio', []))
                    freq = fdata.get('frequency', ['?'])[0]
                    print(f'- `{field}` [cov={cr:.2f}, freq={freq}, shape={shape}] → {"; ".join(adv)}')
            # 字段组合建议
            hints = field_combine_hints(field_shapes)
            if hints:
                print(f'\n**字段组合建议** (基于分布形状互补):')
                for h in hints:
                    print(f'- {h}')

    # ============ 5. JSON 导出 ============
    if args.json_out:
        f_rows = []
        for f, s in isos['datafield'].items():
            bn = best_neuts(neut['datafield'].get(f, {}), 5)
            f_rows.append({'field': f, 'count': s.get('count', 0),
                           'sharpe': round(s.get('sharpe_ratio', 0), 3),
                           'fitness': round(s.get('fitness_ratio', 0), 3),
                           'best_neuts': [{'neut': n, 'sharpe': round(sh, 3), 'count': c, 'osis': int(os_c)}
                                          for n, sh, c, os_c in bn]})
        f_rows.sort(key=lambda r: -r['count'])
        with open(args.json_out, 'w') as fh:
            json.dump({'region_delay': key, 'mean_sharpe': mean_sharpe,
                       'window': window, 'datasets': ds_rows, 'sweet_spot': sweet,
                       'degraded': degraded, 'fields': f_rows},
                      fh, ensure_ascii=False, indent=1)
        print(f'\nJSON 已写入 {args.json_out}')


if __name__ == '__main__':
    main()