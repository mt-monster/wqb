# -*- coding: utf-8 -*-
"""并行提交执行器模板 — 五槽填槽模式硬门控（方案 A）。

用法:
    python tools/_submit_parallel.py --batches A B C D E [--max-parallel 5]

硬门控:
    - 必须同时指定 >=2 个批次（推荐 5 批）
    - 禁止单批提交（违反五槽填槽模式）
    - 自动检查台账同步门禁（check_ledger_sync.py）
"""
import argparse
import asyncio
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

MCP_DIR = r'd:\coding\traeCN_project\wqb\world-quant-brain-mcp'
ROOT = r'd:\coding\traeCN_project\wqb'


def run_submit_script(tag):
    """运行单个提交脚本，返回 (tag, success, output)。"""
    script = os.path.join(ROOT, 'tools', f'_submit_{tag.lower()}.py')
    if not os.path.isfile(script):
        return tag, False, f'脚本不存在: {script}'
    
    try:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=ROOT
        )
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return tag, success, output
    except subprocess.TimeoutExpired:
        return tag, False, '超时（300s）'
    except Exception as e:
        return tag, False, f'异常: {e}'


def check_ledger_sync(region='USA'):
    """台账同步门禁 — 第 0 道硬门。"""
    checker = os.path.join(ROOT, 'tools', 'check_ledger_sync.py')
    result = subprocess.run(
        [sys.executable, checker, '--region', region],
        capture_output=True,
        text=True,
        cwd=ROOT
    )
    if result.returncode != 0:
        print('[BLOCKED] 台账同步门禁未通过：')
        print(result.stdout)
        print(result.stderr)
        return False
    print('[PASS] 台账同步门禁通过')
    return True


def main():
    ap = argparse.ArgumentParser(description='并行提交执行器（五槽填槽模式）')
    ap.add_argument('--batches', nargs='+', required=True,
                    help='批次标签列表（如 A B C D E），必须 >=2 个')
    ap.add_argument('--max-parallel', type=int, default=5,
                    help='最大并行数（默认 5，对应平台 5 槽）')
    ap.add_argument('--region', default='USA', help='区域代号（默认 USA）')
    ap.add_argument('--skip-ledger-check', action='store_true',
                    help='跳过台账同步门禁（紧急调试用，不推荐）')
    args = ap.parse_args()

    # 硬门控 1：必须 >=2 批
    if len(args.batches) < 2:
        print('[BLOCKED] 五槽填槽模式违规：必须同时提交 >=2 批（推荐 5 批）')
        print(f'          当前只指定了 {len(args.batches)} 批: {args.batches}')
        sys.exit(1)

    # 硬门控 2：台账同步检查
    if not args.skip_ledger_check:
        if not check_ledger_sync(args.region):
            sys.exit(1)

    # 硬门控 3：并行数限制
    n_parallel = min(len(args.batches), args.max_parallel)
    if n_parallel > 5:
        print(f'[WARN] 并行数 {n_parallel} 超过平台槽位 5，可能触发 429')

    print(f'[START] 并行提交 {len(args.batches)} 批（并行度={n_parallel}）: {args.batches}')

    # 并行执行
    with ThreadPoolExecutor(max_workers=n_parallel) as pool:
        results = list(pool.map(run_submit_script, args.batches))

    # 汇总
    success = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]
    
    print(f'\n[DONE] 成功 {len(success)}/{len(results)} 批')
    for tag, ok, output in results:
        status = 'OK' if ok else 'FAIL'
        print(f'  [{status}] {tag}: {output[:200]}...')
    
    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
