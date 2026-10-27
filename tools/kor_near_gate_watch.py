# -*- coding: utf-8 -*-
"""十年探针哨兵：近闸候选即时告警。

按用户 2026-10-25 指令：「当出现近闸候选时就汇报」。
tail `results/kor_year_probe.jsonl`，每条新记录都按 KOR 闸线判一次：

  ALERT  : sharpe >= s_min（默认 1.25 = KOR Mode B 主闸）
           或 n_years == 10 且 sharpe >= near_min（默认 1.0）
  WATCH  : 其余有 sharpe 的记录（仅存档，不告警）

命中即追加写 `logs/kor_near_gate_alerts.log` 并打印，**不缓冲、不等扫完**。
输出文件 mtime 静默超过 --idle-sec 后退出（= 上游扫完了），
退出时打印汇总，便于上层收到任务通知后直接汇报。

用法：
  python tools/kor_near_gate_watch.py --file results/kor_year_probe.jsonl
  python tools/kor_near_gate_watch.py --s-min 1.4 --near-min 1.1 --idle-sec 900
"""
import argparse
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALERT = os.path.join(ROOT, "logs", "kor_near_gate_alerts.log")


def tail_jsonl(path, start_end):
    """从文件末尾开始增量读；文件不存在则等。"""
    while not os.path.exists(path):
        time.sleep(2)
    with open(path, encoding="utf-8") as f:
        if start_end:
            f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                yield None  # 无新行
                continue
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default=os.path.join(ROOT, "results", "kor_year_probe.jsonl"))
    ap.add_argument("--s-min", type=float, default=1.25)
    ap.add_argument("--near-min", type=float, default=1.0)
    ap.add_argument("--idle-sec", type=int, default=600, help="文件静默多久判定扫完并退出")
    ap.add_argument("--poll", type=float, default=5.0)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(ALERT), exist_ok=True)
    print(f"[watch] 哨兵启动｜file={args.file}｜ALERT S>={args.s_min}｜"
          f"近闸 S>={args.near_min} 且 10Y｜idle>{args.idle_sec}s 退出", flush=True)

    seen = 0
    alerts = []
    last_mtime = os.path.getmtime(args.file) if os.path.exists(args.file) else time.time()
    last_active = time.time()
    stream = tail_jsonl(args.file, start_end=False)

    for rec in stream:
        if rec is None:
            time.sleep(args.poll)
            if os.path.exists(args.file):
                m = os.path.getmtime(args.file)
                if m != last_mtime:
                    last_mtime = m
                    last_active = time.time()
            if time.time() - last_active > args.idle_sec:
                print(f"[watch] 文件静默 {args.idle_sec}s ⇒ 判定上游扫完，退出", flush=True)
                break
            continue

        seen += 1
        ds = rec.get("dataset")
        s = rec.get("sharpe")
        n_years = rec.get("n_years")
        verdict = rec.get("verdict")

        if s is None:
            continue
        if s >= args.s_min or (n_years == 10 and s >= args.near_min):
            tag = "ALERT" if s >= args.s_min else "NEAR"
            line = (f"[{time.strftime('%H:%M:%S')}] {tag:5s} {ds:26s} "
                    f"S={s} F={rec.get('fitness')} TO={rec.get('turnover')} "
                    f"n_years={n_years} verdict={verdict}")
            with open(ALERT, "a", encoding="utf-8") as f:
                f.write(line + "\n")
            print(line, flush=True)
            alerts.append((tag, ds, s, n_years))

    print(f"\n[watch] 汇总：读过 {seen} 条｜ALERT {sum(1 for a in alerts if a[0]=='ALERT')} 条｜"
          f"NEAR {sum(1 for a in alerts if a[0]=='NEAR')} 条", flush=True)
    for tag, ds, s, ny in sorted(alerts, key=lambda x: -(x[2] or 0)):
        print(f"  {tag:5s} {ds:26s} S={s} n_years={ny}", flush=True)
    print(f"告警明细见 {ALERT}", flush=True)


if __name__ == "__main__":
    main()
