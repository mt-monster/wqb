"""Evidence-backed, read-only DB -> per-dataset Markdown experience snapshots."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import re
import sqlite3
import os
import tempfile

from wqb.db_conn import connect, default_db_path
from wqb.expression.grammar import parse_expression
from wqb.expression.validator import _fields_of

BEGIN = '<!-- BEGIN WQB DATASET EVIDENCE -->'
END = '<!-- END WQB DATASET EVIDENCE -->'


def unpack(value, default=None):
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value) if value else default
    except (ValueError, TypeError):
        return default


def cell(value):
    if value is None:
        return '未核实'
    return str(value).replace('|', '\\|').replace('\n', ' ').replace('\r', '')


def expression_fields(code):
    stack = [parse_expression(code)]
    result = set()
    while stack:
        node = stack.pop()
        if node.kind == 'ident':
            result.update(_fields_of(node))
        stack.extend(node.args)
    return sorted(result)


def load_evidence(db, region, dataset=None, waves=None, delay=None):
    """Only completed backtests; never join alphas to waves through dataset_id."""
    with closing(connect(str(Path(db).resolve()), readonly=True, row_factory=sqlite3.Row)) as conn:
        ledger = {r['key']: unpack(r['value'], {}) for r in conn.execute(
            'SELECT key,value FROM ledger_kv WHERE region=?', (region,))}
        wave_info = {str(r['wave_number']): unpack(r['full_payload'], {}) for r in conn.execute(
            'SELECT wave_number,full_payload FROM wave_results WHERE region=?', (region,))}
        sql = '''SELECT b.*, a.delay AS alpha_delay, a.universe AS alpha_universe,
                        a.neutralization AS alpha_neutralization,
                        a.prod_correlation, a.self_correlation
                 FROM backtest_results b LEFT JOIN alphas a ON a.alpha_id=b.alpha_id
                 WHERE b.region=? AND UPPER(b.status)='COMPLETE'
                 AND b.alpha_id IS NOT NULL AND b.alpha_id<>'' '''
        args = [region]
        if dataset:
            sql += ' AND b.dataset=?'
            args.append(dataset)
        if waves:
            sql += ' AND b.wave IN (' + ','.join('?' for _ in waves) + ')'
            args.extend(str(w) for w in waves)
        sql += ' ORDER BY b.id'
        unique = {}
        warnings = []
        for raw in conn.execute(sql, args):
            row = dict(raw)
            if not row.get('dataset') or row['dataset'] == '_unknown':
                warnings.append(f"{row['alpha_id']} 无 dataset 归属，未纳入")
                continue
            settings = wave_info.get(str(row['wave']), {}).get('settings', {})
            row['delay'] = row['alpha_delay'] if row['alpha_delay'] is not None else settings.get('delay')
            row['universe'] = row['alpha_universe'] or settings.get('universe')
            row['neutralization'] = row['alpha_neutralization'] or settings.get('neutralization')
            row['settings'] = settings
            if delay is not None and row['delay'] != delay:
                if row['delay'] is None:
                    warnings.append(f"{row['alpha_id']} delay 未知，不能归入 D{delay}")
                continue
            review = ledger.get(f"review_{row['wave']}", {})
            detail = next((x for x in review.get('all', []) if x.get('id') == row['alpha_id']), {})
            row['review'] = detail
            row['robust'] = detail.get('robust_sharpe')
            row['failed_checks'] = unpack(row.get('ra_failed_checks'), None)
            try:
                row['fields'] = expression_fields(row.get('code') or '')
            except Exception as exc:
                row['fields'] = []
                warnings.append(f"{row['alpha_id']} 字段解析失败：{type(exc).__name__}；需人工核对原式")
            unique[row['alpha_id']] = row
        rows = list(unique.values())
        datasets = sorted({r['dataset'] for r in rows})
        catalogs = {}
        for ds in datasets:
            cat = ledger.get(f'catalog_{ds}', {})
            if not isinstance(cat, dict) or not cat.get('fields'):
                found = conn.execute('''SELECT d.catalog_json FROM datasets d
                    JOIN regions r ON r.id=d.region_id WHERE r.name=? AND d.name=?''', (region, ds)).fetchone()
                cat = unpack(found['catalog_json'], {}) if found else {}
            catalogs[ds] = {f.get('id') or f.get('field_name'): f for f in cat.get('fields', [])}
        return {'region': region, 'rows': rows, 'catalogs': catalogs, 'warnings': warnings,
                'waves_filter': list(waves or []), 'delay_filter': delay}


def render_dataset(evidence, dataset):
    rows = [r for r in evidence['rows'] if r['dataset'] == dataset]
    if not rows:
        raise ValueError(f'没有已完成回测：{dataset}')
    region = evidence['region']
    catalog = evidence['catalogs'].get(dataset, {})
    used = sorted({f for r in rows for f in r['fields']})
    waves = sorted({str(r['wave']) for r in rows}, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x))
    best = max((r for r in rows if r.get('sharpe') is not None), key=lambda r: r['sharpe'], default=None)
    settings = sorted({(cell(r['delay']), cell(r['universe']), cell(r['neutralization']),
        cell(r['settings'].get('decay')), cell(r['settings'].get('truncation')),
        cell(r['settings'].get('startDate')), cell(r['settings'].get('endDate'))) for r in rows})
    lines = [BEGIN, '## 数据库证据快照', '',
        f"- 范围：{region} / {dataset}；波次 {', '.join(waves)}；去重后 {len(rows)} 条已完成回测，{len(used)} 个实用字段。",
        '- 数据源：data/wqb.db 的 backtest_results（真实波次）、alphas（已存相关性）、ledger_kv/catalog_* 与 review_*。',
        '- 生成、选中、待回测和独立数据诊断不计入回测成果。缺失相关性写“未核实”；空失败列表不证明通过完整 Regular 提交链。',
        '- 以下为历史 IS 证据，不能当作样本外收益或可提交判定；字段参与强因子不等于字段独立有效。',
        f"- 筛选：delay={cell(evidence['delay_filter']) if evidence['delay_filter'] is not None else '全部（分设置展示）'}；waves={','.join(map(str,evidence['waves_filter'])) or '该数据集全部已回测波次'}。",
        '', '| Delay | Universe | 中性化 | Decay | Truncation | 开始 | 结束 |', '|---|---|---|---|---|---|---|']
    lines.extend('| ' + ' | '.join(s) + ' |' for s in settings)
    if best:
        lines += ['', f"最高 Sharpe 候选：`{best['alpha_id']}`，Sharpe={best['sharpe']}，同条 Fitness={cell(best['fitness'])}，Prod={cell(best['prod_correlation'])}。"]
    lines += ['', '## 字段证据与使用经验', '',
        '| 字段 | 类型 / 覆盖率 / users | 平台描述 | 已测次数 | 最强参与候选 S / F | 证据边界 |',
        '|---|---|---|---:|---|---|']
    for field in used:
        f = catalog.get(field, {})
        fr = [r for r in rows if field in r['fields']]
        strongest = max((r for r in fr if r.get('sharpe') is not None), key=lambda r:r['sharpe'], default=None)
        meta = f"{cell(f.get('type'))} / {cell(f.get('coverage'))} / {cell(f.get('userCount'))}"
        score = f"{strongest['sharpe']} / {cell(strongest['fitness'])} (`{strongest['alpha_id']}`)" if strongest else '未核实'
        caveat = '仅为所列搭配中的结果；不能推断独立贡献'
        if f.get('type') == 'VECTOR':
            caveat += '；须先聚合为 MATRIX'
        if not f:
            caveat += '；本地目录缺字段元数据'
        lines.append(f"| `{field}` | {meta} | {cell(f.get('description'))} | {len(fr)} | {score} | {caveat} |")
    lines += ['', '## 已完成候选逐条记录', '',
        '| 波次 | Alpha | Sharpe | Fitness | 2Y | 换手率% | Sub | Robust | Prod | Self |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        tv = round(r['turnover'] * 100, 3) if r.get('turnover') is not None else None
        vals = [r['wave'], f"`{r['alpha_id']}`", r['sharpe'], r['fitness'], r['two_year_sharpe'],tv,
                r['sub_universe_sharpe'],r['robust'],r['prod_correlation'],r['self_correlation']]
        lines.append('| ' + ' | '.join(cell(v) for v in vals) + ' |')
    lines += ['', '### 原式与局部失败证据', '']
    for r in rows:
        lines += [f"**{r['alpha_id']}（wave {r['wave']}）**", '', '```text', r.get('code') or '原式缺失', '```', '',
                  f"已存检查失败：{cell(', '.join(r['failed_checks'])) if r['failed_checks'] else '未记录失败项；仍须按完整 Regular 标准核查'}。", '']
    if evidence['warnings']:
        lines += ['### 读取限制', ''] + ['- ' + w for w in evidence['warnings']]
    lines += [END]
    return '\n'.join(lines) + '\n'


def write_report(path, block, title):
    """Replace only our evidence block, retain analyst text; fail on concurrent edits."""
    path = Path(path)
    previous = path.read_text(encoding='utf-8') if path.exists() else None
    if previous is None:
        content = f'# {title}\n\n' + block + '\n## 人工机制复盘\n\n待结合原式、字段语义与平台核查补充；机器统计不自动生成因果结论。\n'
    elif BEGIN in previous and END in previous:
        start, stop = previous.index(BEGIN), previous.index(END) + len(END)
        if stop <= start:
            raise ValueError(f'证据块边界损坏：{path}')
        content = previous[:start] + block.rstrip() + previous[stop:]
    elif BEGIN in previous or END in previous:
        raise ValueError(f'证据块标记不完整，保留原文件：{path}')
    else:
        content = previous.rstrip() + '\n\n' + block
    if content == previous:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, prefix='.'+path.name, suffix='.tmp', delete=False) as fp:
        fp.write(content)
        tmp = Path(fp.name)
    try:
        current = path.read_text(encoding='utf-8') if path.exists() else None
        if current != previous:
            raise RuntimeError(f'文档被另一写入者修改，请重新读取再刷新：{path}')
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description='按数据集导出字段级挖掘经验；只读DB，保留人工复盘段。')
    parser.add_argument('--region')
    parser.add_argument('--campaign-dir')
    parser.add_argument('--dataset', help='省略则覆盖本区域范围内所有已回测数据集')
    parser.add_argument('--wave', '--waves', dest='waves', help='可选逗号分隔波次；省略读取完整历史')
    parser.add_argument('--delay', type=int, choices=[0, 1])
    parser.add_argument('--db')
    parser.add_argument('--out-dir', default=str(Path(__file__).resolve().parents[3] / 'reports/dataset_experience'),
                        help='默认写入仓库 reports/dataset_experience，不随工作目录变化')
    parser.add_argument('--dry-run', action='store_true', help='验证读取并显示计划，不写文件或数据库')
    args = parser.parse_args(argv)
    region = args.region
    if args.campaign_dir:
        settings = json.loads((Path(args.campaign_dir)/'config/settings.json').read_text(encoding='utf-8-sig'))
        if region and region != settings['region']:
            parser.error('--region 与 campaign settings 不一致')
        region = settings['region']
    if not region:
        parser.error('需要 --region 或 --campaign-dir')
    evidence = load_evidence(args.db or default_db_path(), region, args.dataset,
                             args.waves.split(',') if args.waves else None, args.delay)
    datasets = sorted({r['dataset'] for r in evidence['rows']})
    if not datasets:
        parser.error('该范围没有已完成回测；不会生成伪经验文件')
    for ds in datasets:
        if not re.fullmatch(r'[A-Za-z0-9_-]+', ds) or not re.fullmatch(r'[A-Za-z0-9_-]+', region):
            raise ValueError('region/dataset 不能用于安全文件名')
        # 注意：文件名刻意保留历史拼写 `campain`（缺 g），**不是笔误可改**——
        # 该后缀已被既有 reports/dataset_experience/*.md 与消费方（skill 文档、
        # 经验检索）当作稳定契约；改拼写会使旧文件失配、被当成新文件重写。
        # 若要规范化，须一次性迁移所有存量文件 + 同步 skill 文档，勿单点修改。
        path = Path(args.out_dir) / f'{region.lower()}_{ds}_campain.md'
        block = render_dataset(evidence, ds)
        changed = False if args.dry_run else write_report(path, block, f'{region} · {ds} 因子挖掘经验')
        print(f"{'DRY-RUN' if args.dry_run else 'UPDATED' if changed else 'UNCHANGED'} {path} rows={sum(r['dataset']==ds for r in evidence['rows'])}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
