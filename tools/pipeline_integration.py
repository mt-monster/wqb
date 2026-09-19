#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

try:
    from quality_control_engine import QualityControlEngine
    QC_AVAILABLE = True
except ImportError:
    QC_AVAILABLE = False
    print('[warn] quality_control_engine 未安装，质量检查功能不可用')


def integrate_s2_build_wave(file_path, wave, size=48):
    print('=' * 70)
    print('S2 选波阶段：多维标签选波 + 质量检查')
    print('=' * 70)

    with open(file_path, encoding='utf-8') as f:
        d = json.load(f)
    exprs = d if isinstance(d, list) else (d.get('expressions') or d.get('exprs') or [])
    exprs = [e for e in exprs if isinstance(e, str)]

    print()
    print('候选池：', len(exprs), '条表达式')

    print()
    print('[1/3] 多维标签选波...')
    # 使用 skeleton_tags 直接实现多维选波
    from skeleton_tags import batch_extract_tags, summarize_tags, DEFAULT_QUOTA
    import collections

    tags_list = batch_extract_tags(exprs)

    # 按机制族分桶
    mechanism_buckets = collections.defaultdict(list)
    for i, tags in enumerate(tags_list):
        mechanism_buckets[tags['mechanism']].append((i, tags))

    # 按结构分桶
    structure_buckets = collections.defaultdict(list)
    for i, tags in enumerate(tags_list):
        structure_buckets[tags['structure']].append((i, tags))

    # 轮转抽样：优先满足机制多样性
    picked = []
    picked_indices = set()
    picked_tags = []

    # 第一轮：按机制配额抽样
    for mechanism, cap in DEFAULT_QUOTA['mechanism'].items():
        bucket = mechanism_buckets.get(mechanism, [])
        target = max(1, int(size * cap))
        for i, tags in bucket[:target]:
            if len(picked) >= size:
                break
            if i not in picked_indices:
                picked.append(exprs[i])
                picked_indices.add(i)
                picked_tags.append(tags)

    # 第二轮：填充剩余配额（按结构多样性）
    remaining = size - len(picked)
    if remaining > 0:
        for structure, cap in sorted(DEFAULT_QUOTA['structure'].items(), key=lambda x: -x[1]):
            bucket = structure_buckets.get(structure, [])
            for i, tags in bucket:
                if len(picked) >= size:
                    break
                if i not in picked_indices:
                    picked.append(exprs[i])
                    picked_indices.add(i)
                    picked_tags.append(tags)

    # 汇总标签统计
    summary = summarize_tags(picked_tags)

    # 配额校验
    violations = []
    for dim, quotas in DEFAULT_QUOTA.items():
        actual = summary.get(f'{dim}_share', {})
        for tag, cap in quotas.items():
            if actual.get(tag, 0) > cap:
                violations.append(f"{dim}.{tag} 超配 {actual[tag]:.0%} > {cap:.0%}")

    meta = {
        'multidim': True,
        'summary': summary,
        'quota_violations': violations,
        'quota_passed': not violations,
    }

    print('选波结果：', len(picked), '条')
    print('机制覆盖：', len(meta['summary']['mechanism']), '种')
    print('构造链覆盖：', len(meta['summary']['construction_chain']), '种')

    if QC_AVAILABLE:
        print()
        print('[2/3] 质量检查...')
        engine = QualityControlEngine()

        wave_data = {
            'templates': [],
            'fields': [],
            'expressions': picked,
            'field_profiles': None,
        }

        report = engine.run_full_check(wave_data)

        print('表达式质量：', report['summary']['expression_score'])
        print('配额合规：', 'PASS' if meta['quota_passed'] else 'FAIL')
        if meta['quota_violations']:
            print('配额超限：', len(meta['quota_violations']), '项')
            for v in meta['quota_violations'][:3]:
                print('  -', v)

    print()
    print('[3/3] 保存结果...')
    output = {
        'wave': wave,
        'selected': picked,
        'meta': meta,
        'quality_report': report if QC_AVAILABLE else None,
    }

    output_path = 'logs/s2_wave' + wave + '_integrated.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print('结果已保存：', output_path)

    return output


def integrate_s3_wave_gate(campaign_dir, dataset, wave):
    print('=' * 70)
    print('S3 预检阶段：质量检查 + 门禁')
    print('=' * 70)

    print()
    print('[1/3] 运行现有门禁...')
    import subprocess
    cmd = [
        sys.executable, 'tools/wave_gate.py',
        '--campaign-dir', campaign_dir,
        '--dataset', dataset,
        '--wave', str(wave),
        '--from-db',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

    print('门禁结果：', 'PASS' if result.returncode == 0 else 'FAIL')

    if QC_AVAILABLE:
        print()
        print('[2/3] 质量检查...')
        engine = QualityControlEngine()

        gate_result_path = campaign_dir + '/cache/gate_wave' + str(wave) + '_' + dataset + '.json'
        if os.path.exists(gate_result_path):
            with open(gate_result_path, encoding='utf-8') as f:
                gate_result = json.load(f)

            expressions = [item['expr'] for item in gate_result.get('syntax', {}).get('items', [])]

            wave_data = {
                'templates': [],
                'fields': [],
                'expressions': expressions,
                'field_profiles': None,
            }

            report = engine.run_full_check(wave_data)

            print('表达式质量：', report['summary']['expression_score'])
            print('风险标记：高=', report['expression_report']['high_risk'],
                  '中=', report['expression_report']['medium_risk'],
                  '低=', report['expression_report']['low_risk'])

    print()
    print('[3/3] 保存结果...')
    output = {
        'wave': wave,
        'dataset': dataset,
        'gate_result': result.returncode == 0,
        'quality_report': report if QC_AVAILABLE else None,
    }

    output_path = 'logs/s3_wave' + str(wave) + '_' + dataset + '_integrated.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print('结果已保存：', output_path)

    return output


def integrate_s4_review_wave(campaign_dir, dataset, wave):
    print('=' * 70)
    print('S4 评审阶段：回测质量分析 + 信号苗头识别')
    print('=' * 70)

    print()
    print('[1/3] 加载回测结果...')
    backtest_result_path = campaign_dir + '/cache/backtest_wave' + str(wave) + '_' + dataset + '.json'

    if not os.path.exists(backtest_result_path):
        print('[warn] 回测结果不存在：', backtest_result_path)
        print('[info] 使用模拟数据演示')

        backtest_results = [
            {
                'expression': 'group_rank(ts_delta(vec_avg(eps_up_cnt), 22), industry)',
                'sharpe': 1.35,
                'fitness': 0.95,
                'mechanism': 'analyst_revision',
                'fields': ['eps_up_cnt'],
            },
            {
                'expression': 'rank(eps_estimate_4wk_change)',
                'sharpe': 0.85,
                'fitness': 0.65,
                'mechanism': 'momentum',
                'fields': ['eps_estimate_4wk_change'],
            },
        ]
    else:
        with open(backtest_result_path, encoding='utf-8') as f:
            backtest_results = json.load(f)

    print('回测结果：', len(backtest_results), '条')

    if QC_AVAILABLE:
        print()
        print('[2/3] 回测质量分析...')
        engine = QualityControlEngine()

        wave_data = {
            'templates': [],
            'fields': [],
            'expressions': [],
            'backtest_results': backtest_results,
        }

        report = engine.run_full_check(wave_data)

        print('回测达标率：', report['summary']['backtest_pass_rate'])
        print('信号苗头：', len(report['backtest_report']['signal_promising']), '个')

        if report['backtest_report']['signal_promising']:
            print()
            print('信号苗头清单：')
            for item in report['backtest_report']['signal_promising']:
                print('  -', item['expression'][:60], '...')
                print('    sharpe=', item['sharpe'], 'fitness=', item['fitness'], 'mechanism=', item['mechanism'])

    print()
    print('[3/3] 保存结果...')
    output = {
        'wave': wave,
        'dataset': dataset,
        'backtest_results': backtest_results,
        'quality_report': report if QC_AVAILABLE else None,
    }

    output_path = 'logs/s4_wave' + str(wave) + '_' + dataset + '_integrated.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print('结果已保存：', output_path)

    return output


def main():
    ap = argparse.ArgumentParser(description='质量改进控制体系 Pipeline 集成示例')
    ap.add_argument('--stage', required=True, choices=['s2', 's3', 's4'],
                    help='集成阶段：s2=选波, s3=预检, s4=评审')
    ap.add_argument('--file', help='候选表达式 JSON 文件（S2 阶段）')
    ap.add_argument('--wave', required=True, help='波次标签')
    ap.add_argument('--size', type=int, default=48, help='选波大小（S2 阶段）')
    ap.add_argument('--campaign-dir', help='战役根目录（S3/S4 阶段）')
    ap.add_argument('--dataset', help='数据集（S3/S4 阶段）')
    a = ap.parse_args()

    if a.stage == 's2':
        if not a.file:
            print('[error] S2 阶段需要 --file 参数')
            sys.exit(1)
        integrate_s2_build_wave(a.file, a.wave, a.size)

    elif a.stage == 's3':
        if not a.campaign_dir or not a.dataset:
            print('[error] S3 阶段需要 --campaign-dir 和 --dataset 参数')
            sys.exit(1)
        integrate_s3_wave_gate(a.campaign_dir, a.dataset, a.wave)

    elif a.stage == 's4':
        if not a.campaign_dir or not a.dataset:
            print('[error] S4 阶段需要 --campaign-dir 和 --dataset 参数')
            sys.exit(1)
        integrate_s4_review_wave(a.campaign_dir, a.dataset, a.wave)


if __name__ == '__main__':
    main()
