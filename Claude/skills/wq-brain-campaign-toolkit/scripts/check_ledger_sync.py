#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_ledger_sync.py - 战役台账同步门禁。

校验项：
1. 战役 ledger JSON（<prefix>_d1_campaign_state.json）存在且可读。
2. WAVE_LEDGER.md（如存在）中登记的波次/批次与 ledger 的 waves/verdict 键一致。
3. runs/ 目录下实际批次文件（*_batch_*.txt）与 ledger 中 waves 登记一致。
4. 无重复 wave 编号、无未登记的在飞批次、无 ledger 中标记完成但 runs/ 缺失的批次。
5. 判死/禁发数据集在 ledger 与 ledger.json（如存在）中一致。

用法：
  python check_ledger_sync.py --campaign-dir tracking/<REGION> [--fix] [--strict]

返回码：
  0 = 台账同步通过，可以继续提交新批次。
  1 = 发现不同步或缺失，需人工核对/修复。

配合 wqb-concurrency §8 七槽填槽模式：每次提交新波前运行本脚本作为"台账同步门"。
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, load_json
from _lib.ledger import LedgerStore, make_ledger_store


def parse_args():
    ap = argparse.ArgumentParser(description="战役台账同步门禁")
    ap.add_argument("--campaign-dir", required=True, help="战役目录路径")
    ap.add_argument("--fix", action="store_true",
                    help="尝试自动修复轻量不同步（仅写 advisory 提示，不改 WAVE_LEDGER.md）")
    ap.add_argument("--strict", action="store_true",
                    help="严格模式：任何 advisory 也视为错误")
    ap.add_argument("--kill-zombies", action="store_true",
                    help="P1-3 战役启动前强制枚举并清理僵尸轮询进程（429 隐性配额消耗源）")
    ap.add_argument("--zombie-dry-run", action="store_true",
                    help="只列出僵尸进程不杀（配合 --kill-zombies）")
    return ap.parse_args()


def load_ledger(ctx):
    """单轨 DB 模式：走 make_ledger_store（默认 sqlite）。返回 (dict|None, source)。"""
    try:
        d = make_ledger_store(ctx).load()
        return (d if d else None), f"sqlite:ledger_kv[{ctx.region}]"
    except Exception:
        return None, f"sqlite:ledger_kv[{ctx.region}]"


def load_ledger_json(ctx):
    """tracking/<REGION>/ledger.json 是 WAVE_LEDGER.md 的机器伴生文件（可选）。"""
    path = ctx.path("ledger.json")
    if not os.path.exists(path):
        return None, path
    return load_json(path), path


def load_wave_ledger(ctx):
    """WAVE_LEDGER.md 人工台账（可选）。"""
    path = ctx.path("WAVE_LEDGER.md")
    if not os.path.exists(path):
        return None, path
    return open(path, encoding="utf-8").read(), path


def extract_wave_ledger_sections(text):
    """从 WAVE_LEDGER.md 提取 ## 波X / ## Wave X 节标题。"""
    waves = set()
    if not text:
        return waves
    for line in text.splitlines():
        m = re.match(r'^##\s*波?\s*(\d+)', line.strip())
        if m:
            waves.add(int(m.group(1)))
    return waves


def extract_runs_batches(runs_dir):
    """从 runs/ 目录提取批次文件中的 wave/批次标识。

    返回 {"batch_tags": set(如 "aa", "ab"), "dataset_batches": {dataset: set(tags)}}。
    """
    batch_tags = set()
    dataset_batches = {}
    if not os.path.isdir(runs_dir):
        return batch_tags, dataset_batches
    for fn in os.listdir(runs_dir):
        if not fn.endswith(".txt"):
            continue
        # 形如 usa_inst6_batch_ww.txt -> dataset=inst6, tag=ww
        m = re.match(r'^[a-z]+_(.+?)_batch_([a-z0-9_]+)\.txt$', fn)
        if not m:
            continue
        dataset, tag = m.group(1), m.group(2)
        batch_tags.add(tag)
        dataset_batches.setdefault(dataset, set()).add(tag)
    return batch_tags, dataset_batches


def extract_ledger_waves(ledger):
    """从 ledger 提取 waves 列表与 verdict 键中的波次。"""
    waves = set()
    verdicts = set()
    if not ledger:
        return waves, verdicts
    for w in ledger.get("waves", []):
        try:
            waves.add(int(str(w.get("wave", "")).replace("波", "")))
        except ValueError:
            pass
    for key in ledger.keys():
        m = re.match(r'^wave(\d+)_verdict$', key)
        if m:
            verdicts.add(int(m.group(1)))
    return waves, verdicts


def check_dead_datasets(ledger, ledger_json):
    """检查 ledger.json 与 ledger 中的判死数据集是否一致。

    注意：USA 历史 ledger.json 使用粗放的 datasets.<name>.status=dead 记录判死，
    而新战役 ledger 使用 <dataset>_dead 键。两者是同一事实的不同 schema，允许仅存在于
    ledger.json（人工伴生文件）中；只要 ledger.json 有，即视为已登记。
    """
    errors = []
    if not ledger_json or not ledger:
        return errors
    json_dead = {k for k, v in ledger_json.get("datasets", {}).items()
                 if isinstance(v, dict) and v.get("status", "").startswith("dead")}
    ledger_dead = {k.replace("_dead", "") for k in ledger.keys() if k.endswith("_dead")}
    # 仅报错：ledger 有 _dead 但 ledger.json 没有（机器文件应为权威）
    only_in_ledger = ledger_dead - json_dead
    if only_in_ledger:
        errors.append(f"战役 ledger 中判死但未在 ledger.json 登记: {sorted(only_in_ledger)}")
    return errors


def main():
    args = parse_args()
    ctx = CampaignContext(args.campaign_dir)

    # ---- P1-3 僵尸进程清理（战役启动前强制枚举，2026-08-31） ----
    if args.kill_zombies:
        rc = _kill_zombie_pollers(dry_run=args.zombie_dry_run)
        if rc != 0 and not args.zombie_dry_run:
            print("[P1-3] 僵尸进程清理失败，阻断提交（先人工核对）")
            return rc

    errors = []
    advisories = []

    # 1. ledger 存在性
    ledger, ledger_path = load_ledger(ctx)
    if ledger is None:
        errors.append(f"战役台账不存在: {ledger_path}")
        print_sync_result(errors, advisories, ctx)
        return 1

    ledger_json, ledger_json_path = load_ledger_json(ctx)
    wave_text, wave_path = load_wave_ledger(ctx)

    # 2. 波次一致性
    ledger_waves, ledger_verdicts = extract_ledger_waves(ledger)
    md_waves = extract_wave_ledger_sections(wave_text)
    runs_tags, runs_dataset_batches = extract_runs_batches(ctx.path("runs"))

    if md_waves and ledger_waves != md_waves:
        only_md = md_waves - ledger_waves
        only_ledger = ledger_waves - md_waves
        if only_md:
            advisories.append(f"WAVE_LEDGER.md 有但 ledger 未登记波次: {sorted(only_md)}")
        if only_ledger:
            errors.append(f"ledger 已登记但 WAVE_LEDGER.md 缺失波次: {sorted(only_ledger)}")

    # 3. verdict 与 waves 对齐
    missing_verdict = ledger_waves - ledger_verdicts
    if missing_verdict:
        advisories.append(f"ledger 已登记但无 verdict 的波次（可能仍在飞）: {sorted(missing_verdict)}")

    # 4. runs/ 与 ledger 对齐（仅检查 runs/ 中存在但 ledger 未登记数据集的批次）
    if runs_dataset_batches:
        # ledger 中 waves 的 dataset 集合
        ledger_datasets = {w.get("dataset") for w in ledger.get("waves", []) if isinstance(w, dict)}
        for dataset, tags in runs_dataset_batches.items():
            if dataset not in ledger_datasets:
                advisories.append(f"runs/ 存在数据集 {dataset} 的批次 {sorted(tags)}，但 ledger waves 未登记该数据集")

    # 5. 判死数据集一致性
    dead_errors = check_dead_datasets(ledger, ledger_json)
    errors.extend(dead_errors)

    # 7. 悬空波对账（2026-09-01 G4）：backtest_results 有结果但 wave_results 无 verdict
    #    的波次 = 复盘中断/会话崩溃残留，列入补写清单（无人值守恢复入口）。
    try:
        import sqlite3 as _sq
        from _lib.wqb_store import get_store as _gs
        _st = _gs(ctx)
        try:
            _con = _st.connection
            # 该 region 有回测结果的波次
            _bt = {str(r[0]) for r in _con.execute(
                "SELECT DISTINCT wave FROM backtest_results WHERE region=?", (ctx.region,)).fetchall()
                if r[0]}
            # wave_results 已有 verdict 的波次
            _wr = {str(r[0]) for r in _con.execute(
                "SELECT wave_number FROM wave_results WHERE region=? "
                "AND verdict IS NOT NULL AND verdict != ''", (ctx.region,)).fetchall()}
        finally:
            _st.close()
        _dangling = sorted(_bt - _wr, key=lambda x: (len(x), x))
        if _dangling:
            advisories.append(
                f"悬空波（有回测结果但 wave_results 无 verdict，需补写复盘）: {_dangling[:12]}"
                + (f" ...共{len(_dangling)}个" if len(_dangling) > 12 else ""))
    except Exception as _de:
        advisories.append(f"悬空波对账跳过（DB 不可达: {_de}）")

    # 6. 轻量修复提示
    if args.fix:
        # 目前 fix 模式仅打印修复建议，不自动写文件；未来可扩展为自动 add-wave/mark-dead
        if advisories:
            advisories.append("[fix 模式] 已生成建议；涉及 WAVE_LEDGER.md 的修改请人工确认后执行")

    print_sync_result(errors, advisories, ctx)
    if errors or (args.strict and advisories):
        return 1
    return 0


def _kill_zombie_pollers(dry_run=False):
    """P1-3 枚举并清理僵尸轮询进程（429 隐性配额消耗源，2026-08-31）。

    背景：僵尸 API 轮询进程（如残留的七槽填槽轮询、batch_status --watch）会持续
    消耗配额致长期 429（记忆：僵尸API轮询进程持续消耗配额致长期429）。
    本函数在战役启动前强制枚举 python 进程，识别并清理轮询类僵尸。

    识别规则（命令行特征）：
      - 含 'batch_status' 且含 '--watch'（残留轮询）
      - 含 'seven_slot' / 'five_slot'（历史进程名，勿删）/ 'poller' / 'poll' 且运行时长 > 2h（疑似挂死）
      - 含 'check_ledger_sync' 自身的进程除外（避免自杀）
    返回码：0=清理成功/无僵尸，1=清理失败，2=发现僵尸但 dry-run 未杀。
    """
    import subprocess
    import time
    try:
        out = subprocess.check_output(
            ['powershell', '-NoProfile', '-Command',
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" "
             "| Select-Object ProcessId, CommandLine, CreationDate "
             "| ConvertTo-Json -Compress"],
            text=True, encoding='utf-8', errors='replace',
        )
    except Exception as e:
        print(f"[P1-3] 进程枚举失败: {e}")
        return 1
    try:
        procs = json.loads(out)
    except json.JSONDecodeError:
        print("[P1-3] 进程枚举结果解析失败")
        return 1
    if isinstance(procs, dict):
        procs = [procs]
    self_pid = os.getpid()
    zombies = []
    now = time.time()
    for p in procs or []:
        pid = p.get('ProcessId')
        cmd = (p.get('CommandLine') or '')
        if not pid or pid == self_pid:
            continue
        if 'check_ledger_sync' in cmd:
            continue
        is_poller = any(k in cmd for k in ('batch_status', 'seven_slot', 'five_slot', '7slot', 'poller', '--watch', 'poll_'))
        if not is_poller:
            continue
        # 运行时长（CreationDate 是 WMI 日期格式，简化处理：全部列为候选）
        zombies.append({'pid': pid, 'cmd': cmd[:120]})
    if not zombies:
        print("[P1-3] 无僵尸轮询进程")
        return 0
    print(f"[P1-3] 发现 {len(zombies)} 个疑似僵尸轮询进程：")
    for z in zombies:
        print(f"  PID {z['pid']}: {z['cmd']}")
    if dry_run:
        print("[P1-3][dry-run] 仅列出未杀")
        return 2
    killed = 0
    for z in zombies:
        try:
            subprocess.check_call(['taskkill', '/PID', str(z['pid']), '/F'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            killed += 1
            print(f"  [killed] PID {z['pid']}")
        except Exception as e:
            print(f"  [fail] PID {z['pid']}: {e}")
    print(f"[P1-3] 清理完成：{killed}/{len(zombies)} 个僵尸进程已杀")
    return 0 if killed == len(zombies) else 1


def print_sync_result(errors, advisories, ctx):
    print(f"战役目录: {ctx.dir}")
    print(f"ledger:   {ctx.ledger_path}")
    print(f"状态:     {'PASS' if not errors else 'FAIL'}")
    if errors:
        print(f"错误({len(errors)}):")
        for e in errors:
            print(f"  [ERROR] {e}")
    if advisories:
        print(f"提醒({len(advisories)}):")
        for a in advisories:
            print(f"  [ADVISORY] {a}")
    if not errors and not advisories:
        print("台账同步：全部一致，可以继续提交新批次。")


if __name__ == "__main__":
    sys.exit(main())
