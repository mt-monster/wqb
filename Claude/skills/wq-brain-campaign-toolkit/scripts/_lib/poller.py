# -*- coding: utf-8 -*-
"""_lib/poller.py - 轮询器：退避 + 挂起熔断（参数化，thresholds.json "poll" 节可覆盖）。

挂起熔断参数组（KOR waveT 卡 24h 教训）：
  init_interval=20s / backoff_factor=1.5 / max_interval=120s /
  stall_minutes=60（progress 无变化判 STALLED）/ timeout_minutes=360
"""
import json
import sys
import time

TERMINAL = {"COMPLETE", "ERROR", "CANCELLED"}

DEFAULT_POLL = {
    "init_interval": 20,
    "backoff_factor": 1.5,
    "max_interval": 120,
    "stall_minutes": 60,
    "timeout_minutes": 360,
}


def poll_config(ctx=None):
    """thresholds.json 的 "poll" 节覆盖默认值。"""
    cfg = dict(DEFAULT_POLL)
    if ctx is not None:
        cfg.update(ctx.thresh("poll", {}))
    return cfg


def poll_until_terminal(api, msid, cfg=None, get_json=None):
    """轮询至 terminal / STALLED / TIMEOUT。返回 (status, detail_dict)。"""
    cfg = cfg or dict(DEFAULT_POLL)
    get_json = get_json or (lambda p: json.load(api.get(p)))
    interval = cfg["init_interval"]
    waited = 0
    last_prog, last_change = None, time.time()
    while waited < cfg["timeout_minutes"] * 60:
        try:
            d = get_json("/simulations/" + msid)
        except Exception as e:
            print(f"  [poll] {msid} err {e}", file=sys.stderr)
            time.sleep(interval)
            waited += interval
            continue
        status, prog = d.get("status"), d.get("progress")
        if status in TERMINAL:
            return status, d
        if prog != last_prog:
            last_prog, last_change = prog, time.time()
        if time.time() - last_change > cfg["stall_minutes"] * 60:
            print(f"  [poll] {msid} 挂起熔断：progress {prog} 超过 {cfg['stall_minutes']}min 无变化")
            return "STALLED", d
        time.sleep(interval)
        waited += interval
        interval = min(interval * cfg["backoff_factor"], cfg["max_interval"])
    return "TIMEOUT", {}
