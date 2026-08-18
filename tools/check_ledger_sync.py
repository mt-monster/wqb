#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""台账同步门禁（ledger sync gate）— 提交新波回测前的第 0 道门。

用法:
    python tools/check_ledger_sync.py --region USA
    python tools/check_ledger_sync.py --region USA --allow-lag 2
    python tools/check_ledger_sync.py            # 自动扫描 tracking/*/WAVE_LEDGER.md

原理:
    runs/ 目录最新批次字母 - 台账已登记的批次字母 = 滞后批数
    滞后 > --allow-lag (默认 0, 即最新批必须已入台账) → exit 1 阻断提交。

设计背景: 执行线程习惯性把波结论追加进 runs/ 散件 txt 而不更新 WAVE_LEDGER.md/ledger.json，
导致台账停在旧波次、下一波选波失联（已实际发生两次）。文字 SOP 拦不住，故在执行层设硬门：
台账未跟上回收进度时，禁止提交新波。

例外: 纯探索性批次（无正式波次编号）不受本门约束，可用 --allow-lag 放宽或跳过。
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def batch_files(runs_dir):
    """runs/ 下所有正式批次表达式文件（*_batch_*.txt）。"""
    return glob.glob(os.path.join(runs_dir, '*_batch_*.txt'))


def latest_batches(runs_dir, k=3):
    """按修改时间取最新的 k 个批次文件，返回 [(字母, 文件名)]。"""
    files = [(os.path.getmtime(f), f) for f in batch_files(runs_dir)]
    files.sort(reverse=True)
    out = []
    for _, f in files[:k]:
        m = re.search(r'_batch_([a-z0-9]+)\.txt$', os.path.basename(f), re.I)
        if m:
            out.append((m.group(1).upper(), os.path.basename(f)))
    return out


def check_region(region, allow_lag=0):
    """返回 (ok, messages)。"""
    trk = os.path.join(ROOT, 'tracking', region)
    runs = os.path.join(trk, 'runs')
    ledger_md = os.path.join(trk, 'WAVE_LEDGER.md')
    ledger_json = os.path.join(trk, 'ledger.json')
    msgs = []

    if not os.path.isdir(runs):
        return True, [f'[{region}] runs/ 不存在，跳过（无正式战役）']
    if not os.path.isfile(ledger_md):
        if batch_files(runs):
            return False, [f'[{region}] 有 {len(batch_files(runs))} 个批次文件但 WAVE_LEDGER.md 不存在 → 先建台账再提交']
        return True, [f'[{region}] 无批次文件，跳过']

    text = open(ledger_md, encoding='utf-8').read()
    latest = latest_batches(runs)
    if not latest:
        return True, [f'[{region}] 无批次文件，跳过']

    # 滞后判定：最新 N 个批次字母未出现在台账正文 = 滞后批数
    lagging = [(code, fn) for code, fn in latest
               if not re.search(r'(?<![A-Za-z])' + re.escape(code) + r'(?![A-Za-z])', text)]
    ok = len(lagging) <= allow_lag
    newest_code, newest_fn = latest[0]
    if ok:
        msgs.append(f'[{region}] 最新批次 {newest_code}（{newest_fn}）已入台账，同步 OK')
    else:
        msgs.append(f'[{region}] 台账滞后 {len(lagging)} 批（允许 {allow_lag}）→ 阻断提交：')
        for code, fn in lagging:
            msgs.append(f'    - 批次 {code}（{fn}）未出现在 WAVE_LEDGER.md')
        msgs.append('    处置：先把已回收批次的结论（批次表/闸门结论/判死/下一波决策）'
                    '回填 WAVE_LEDGER.md + ledger.json，再提交新波')

    # 交叉校验：ledger.json waves_completed vs WAVE_LEDGER.md 累计波次
    if os.path.isfile(ledger_json):
        try:
            lj = json.load(open(ledger_json, encoding='utf-8'))
            wj = lj.get('waves_completed')
            m = re.search(r'累计波次\s*\|\s*(\d+)', text)
            if wj is not None and m and int(m.group(1)) < int(wj):
                ok = False
                msgs.append(f'[{region}] WAVE_LEDGER.md 累计波次({m.group(1)}) < ledger.json waves_completed({wj}) → 台账落后，需同步')
        except (ValueError, OSError):
            msgs.append(f'[{region}] ⚠️ ledger.json 解析失败，跳过交叉校验')
    return ok, msgs


def main():
    if hasattr(sys.stdout, 'reconfigure'):  # Windows GBK 控制台乱码防护
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description='台账同步门禁：runs/ 最新批次必须已入 WAVE_LEDGER.md，否则阻断提交')
    ap.add_argument('--region', help='区域代号（如 USA）；缺省自动扫描 tracking/*/WAVE_LEDGER.md')
    ap.add_argument('--allow-lag', type=int, default=0, help='允许滞后的批次数（默认 0=最新批必须已入台账）')
    args = ap.parse_args()

    if args.region:
        regions = [args.region]
    else:
        regions = sorted(d for d in os.listdir(os.path.join(ROOT, 'tracking'))
                         if os.path.isfile(os.path.join(ROOT, 'tracking', d, 'WAVE_LEDGER.md')))
        if not regions:
            print('[ledger-sync] 未找到任何 WAVE_LEDGER.md，跳过')
            sys.exit(0)

    all_ok = True
    for r in regions:
        ok, msgs = check_region(r, args.allow_lag)
        all_ok &= ok
        for m in msgs:
            print(m)
    print('\n[ledger-sync] ' + ('PASS' if all_ok else 'BLOCKED：台账未跟上回收进度，先回填再提交新波'))
    sys.exit(0 if all_ok else 1)


if __name__ == '__main__':
    main()
