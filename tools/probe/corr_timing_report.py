#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""corr_timing_report.py — 从 MCP 日志统计「查 prod 的时间到底花在哪」（2026-10-28 P2-8）。

数据源 = ``[corr-t] {...}`` 结构化打点（写入方
``world-quant-brain-mcp/brain_mixin_spcread._corr_log_timing``），解析与汇总在
``wqb.corr_timing``（本脚本只做 IO 与排版，不重复实现判定）。

回答三件事：
  1. 拿到值 vs 没拿到值各多少次、结果率多少；
  2. 时间去向：平台真算 / 轮询超时空转 / 同 alpha 等待 / busy 拒绝；
  3. 哪些 alpha 在反复触发（同族超时后立刻重来的信号）。

用法:
  python tools/probe/corr_timing_report.py                       # 读 logs/wq-brain-http.log
  python tools/probe/corr_timing_report.py --log logs/xxx.log
  python tools/probe/corr_timing_report.py --since 2026-10-28T00:00:00
  python tools/probe/corr_timing_report.py --json results/corr_timing.json
  python tools/probe/corr_timing_report.py --events              # 附原始打点明细

退出码: 0=正常  2=日志不存在/参数错误
"""
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(_HERE))
import _pyenv  # noqa: E402

REPO = _pyenv.REPO_ROOT


def _fmt_row(cols, widths):
    return "  ".join(str(c)[:w].ljust(w) for c, w in zip(cols, widths))


def print_summary(s, log_path):
    w = s["window"] or {}
    print(f"日志：{log_path}")
    if not s["records"]:
        print("未找到 [corr-t] 打点。")
        print("提示：打点是 2026-10-28 起新增的；旧日志没有，先让 wq-brain-http 重启并跑一次相关性查询。")
        return
    span = f"{w.get('span_h')}h" if w.get("span_h") is not None else "?"
    print(f"打点：{s['records']} 条 / {s['alphas']} 个 alpha / 窗口 {span}"
          f"（{w.get('first') or '?'} → {w.get('last') or '?'}）")

    print("\n▶ 事件分布（按事件名）")
    widths = (24, 7, 10, 9, 8, 8)
    print(_fmt_row(("event", "count", "合计s", "中位s", "p90s", "最大s"), widths))
    by_event = s["by_event"]
    for ev in sorted(by_event, key=lambda k: (-by_event[k]["count"], k)):
        r = by_event[ev]
        print(_fmt_row((ev, r["count"], r["sum_s"], r["median_s"], r["p90_s"], r["max_s"]),
                       widths))

    o = s["outcomes"]
    rate = "—" if o["value_rate"] is None else f"{o['value_rate'] * 100:.1f}%"
    print("\n▶ 结果构成")
    print(f"拿到值 {o['got_value']} / 终局 {o['got_value'] + o['no_value']}（{rate}）"
          f"；缓存命中 {o['cache_hits']} · 预读命中 {o['pre_read_hits']} · "
          f"等待合流 {o['joins']}（省 {o['joins']} 次平台计算）")
    print(f"平台轮询 {o['platform_polls']} 次（真算 {o['computed']} / 成功 {o['computed_of_success']}"
          f"）；4xx 终态 {by_event.get('terminal', {}).get('count', 0)}；busy 拒绝 "
          f"{by_event.get('busy', {}).get('count', 0) + by_event.get('inflight_busy', {}).get('count', 0)}")

    t = s["time_s"]
    total = t["platform_success"] + t["platform_pending"] + t["join_wait"]
    pend_share = (t["platform_pending"] / total * 100) if total else 0.0
    print("\n▶ 时间去向（打点覆盖的等待时间）")
    n_ok = by_event.get("success", {}).get("count", 0)
    avg_ok = (t["platform_success"] / n_ok) if n_ok else 0.0
    print(f"平台计算  {t['platform_success']:>9.1f}s（{n_ok} 次，均 {avg_ok:.1f}s）")
    print(f"超时空转  {t['platform_pending']:>9.1f}s（占 {pend_share:.1f}%；"
          f"{by_event.get('pending', {}).get('count', 0)} 次轮询窗口耗尽）")
    print(f"合流等待  {t['join_wait']:>9.1f}s（同 alpha 等到的，未额外触发计算）")
    print(f"等待超时  {t['same_alpha_wait_timeout']:>9.1f}s（随后转 busy，未重触发）")
    ra = s["retry_after"]
    if ra["count"]:
        print(f"busy/pending 的 retry_after：{ra['count']} 条，中位 {ra['median_s']}s / "
              f"最大 {ra['max_s']}s")

    if s["sources"]:
        print("\n▶ 数值来源")
        for src, n in s["sources"].items():
            print(f"  {src:<28} {n}")

    if s["repeat_alphas"]:
        print("\n▶ 重复触发最多的 alpha（同族超时后立刻重来的信号）")
        for p in s["repeat_alphas"]:
            print(f"  {p['alpha']:<12} {p['events']:>3} 条  {','.join(p['kinds'])}")

    if s["top_alphas"]:
        print("\n▶ 耗时最长的 alpha")
        for p in s["top_alphas"]:
            print(f"  {p['alpha']:<12} {p['elapsed_s']:>9.1f}s  {p['events']:>3} 条  "
                  f"{','.join(p['kinds'])}")


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="统计 [corr-t] 打点：查 prod 的时间与结果构成（只读本地日志）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", default=None,
                    help="日志路径（缺省 logs/wq-brain-http.log）")
    ap.add_argument("--since", default=None,
                    help="只统计 ts >= 该时刻（ISO，如 2026-10-28T00:00:00）")
    ap.add_argument("--until", default=None,
                    help="只统计 ts <= 该时刻（ISO）")
    ap.add_argument("--top", type=int, default=5, help="耗时榜条数（默认 5）")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="把汇总写成 JSON 文件")
    ap.add_argument("--events", action="store_true", help="附原始打点明细")
    a = ap.parse_args(argv)

    from wqb import corr_timing

    log_path = a.log or corr_timing.default_log_path()
    if not os.path.exists(log_path):
        print(f"日志不存在：{log_path}", file=sys.stderr)
        return 2
    records = corr_timing.parse_file(log_path)
    if a.since:
        records = [r for r in records if str(r.get("ts") or "") >= a.since]
    if a.until:
        records = [r for r in records if str(r.get("ts") or "") <= a.until]
    summary = corr_timing.summarize(records, top=a.top)
    print_summary(summary, log_path)

    if a.events:
        print("\n▶ 原始打点")
        for r in records:
            print(json.dumps(r, ensure_ascii=False, sort_keys=True))

    if a.json_out:
        out = os.path.join(str(REPO), a.json_out) if not os.path.isabs(a.json_out) else a.json_out
        os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
        payload = {"log": log_path, "since": a.since, "until": a.until,
                   "summary": summary}
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print(f"\nJSON：{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
