#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""近闸算子平替实验回测驱动（断点续跑 + 429 令牌桶纪律）。

纪律来源：
- wqb-concurrency §4：429 频繁短退避 wait=min(20+attempt*8,45)s，绝不因限流丢弃候选
- 用户记忆：checkpoint 原子写；只把确定结果算完成；重启跳过已完成
- 在飞上限 INFLIGHT_MAX=5（保守，给并行会话留余量）

用法：
  python reports/opswap_driver.py            # 续跑（读 cache/opswap_state.json）
  OPSWAP_FRESH=1 python reports/opswap_driver.py  # 全新（丢弃状态，含已提交 sim！慎用）
"""
from __future__ import annotations

import json
import os
import sys
import time

import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, "world-quant-brain-mcp", ".env")
PLAN_PATH = os.path.join(ROOT, "cache", "opswap_plan.json")
STATE_PATH = os.path.join(ROOT, "cache", "opswap_state.json")
RESULT_PATH = os.path.join(ROOT, "cache", "opswap_results.json")

API = "https://api.worldquantbrain.com"
INFLIGHT_MAX = 5
POLL_SEC = 25
MAX_429_RETRY_PER_CYCLE = 1  # 每周期最多新投 1 条（令牌桶慢补充，贪心会全撞 429）

# 首批已提交的 7 条（来自 MCP batch_create_simulations 的确认返回）
SEED_INFLIGHT = {
    "d5bERLmX|ts_mean->ts_decay_linear": "1yzakleUh4mf8R7OaANVB5g",
    "d5bERLmX|ts_decay_linear->ts_mean": "dAJmPfst4XtaOViZmkp2RE",
    "omL3gKEb|group_rank->group_zscore": "14GUWu49p4CJ9vg8uZx3SIt",
    "58zarnp5|ts_mean->ts_decay_linear": "S133za4YIawirUs7TSK0",
    "9qja8ZXr|ts_mean->ts_decay_linear": "2dAlSWelk4zF94uFbFYEFR6",
    "9qja8ZXr|group_rank->group_zscore": "3NtGppgfP4vfcDTQlsoytjx",
    "O0Ndjl2v|group_rank->group_zscore": "1CB9eG7vQ54n9TANlX4UiNM",
}


def load_env():
    # .env 值带引号（dotenv 语义），手写解析必须剥引号——否则认证 401（2026-09-30 实证）
    from dotenv import dotenv_values
    return dict(dotenv_values(ENV_PATH))


def atomic_save(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def new_session():
    import base64
    env = load_env()
    email = env.get("BRAIN_EMAIL") or env.get("CREDENTIALS_EMAIL")
    password = env.get("BRAIN_PASSWORD") or env.get("CREDENTIALS_PASSWORD")
    if not email or not password:
        raise RuntimeError("缺少凭据（BRAIN_EMAIL/CREDENTIALS_EMAIL 均未找到）")
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    cred = base64.b64encode(f"{email}:{password}".encode()).decode()
    r = s.post(API + "/authentication",
               headers={"Authorization": f"Basic {cred}"}, timeout=60)
    if r.status_code != 201:
        raise RuntimeError(f"认证失败 HTTP {r.status_code}")
    return s


def build_payload(item):
    st = item["settings"]
    return {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": st["region"],
            "universe": st["universe"],
            "delay": st["delay"],
            "decay": st["decay"],
            "neutralization": st["neutralization"],
            "truncation": st["truncation"],
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": st["nan"],
            "language": "FASTEXPR",
            "visualization": False,
            "maxTrade": st["mt"],
        },
        "regular": item["expression"],
    }


def sim_terminal(sim_json):
    """返回 (terminal: bool, alpha_id|None, status_str)"""
    status = sim_json.get("status") or ""
    alpha = sim_json.get("alpha")
    if alpha:
        return True, alpha, status or "COMPLETE"
    if status in ("ERROR", "FAIL", "CANCELLED"):
        return True, None, status
    # 有些完成态只给 message
    msg = str(sim_json.get("message") or "")
    if "complete" in msg.lower() and alpha:
        return True, alpha, status
    return False, None, status


def main():
    plan = json.load(open(PLAN_PATH, encoding="utf-8"))
    items = {}
    for v in plan["variants"]:
        tag = v["parent"] + "|" + v["swap"]
        items[tag] = v

    # ---- state 初始化/载入（断点续跑） ----
    if os.environ.get("OPSWAP_FRESH") == "1" and os.path.exists(STATE_PATH):
        os.remove(STATE_PATH)
    if os.path.exists(STATE_PATH):
        state = json.load(open(STATE_PATH, encoding="utf-8"))
        print(f"[resume] 载入状态: {sum(1 for x in state['items'].values() if x['status'] == 'done')} done, "
              f"{sum(1 for x in state['items'].values() if x['status'] == 'inflight')} inflight")
    else:
        state = {"items": {}}
        for tag, v in items.items():
            state["items"][tag] = {"status": "pending", "sim_id": None, "alpha_id": None,
                                   "attempts_429": 0, "error": None}
        for tag, sim_id in SEED_INFLIGHT.items():
            if tag in state["items"]:
                state["items"][tag] = {"status": "inflight", "sim_id": sim_id,
                                       "alpha_id": None, "attempts_429": 0, "error": None}
        atomic_save(state, STATE_PATH)

    sess = new_session()
    print("[auth] ok")

    t0 = time.time()
    while True:
        pend = [t for t, x in state["items"].items() if x["status"] == "pending"]
        infl = {t: x["sim_id"] for t, x in state["items"].items() if x["status"] == "inflight"}
        done = sum(1 for x in state["items"].values() if x["status"] == "done")
        errs = sum(1 for x in state["items"].values() if x["status"] == "error")
        print(f"[{time.strftime('%H:%M:%S')}] +{int(time.time()-t0)}s pending={len(pend)} "
              f"inflight={len(infl)} done={done} error={errs}", flush=True)
        if not pend and not infl:
            break

        # 1) 轮询在飞
        for tag, sim_id in list(infl.items()):
            try:
                r = sess.get(f"{API}/simulations/{sim_id}", timeout=60)
                if r.status_code == 401:  # 会话过期重登
                    sess = new_session()
                    continue
                sj = r.json()
                terminal, alpha_id, st = sim_terminal(sj)
                if terminal:
                    rec = state["items"][tag]
                    if alpha_id:
                        rec["status"] = "done"
                        rec["alpha_id"] = alpha_id
                    else:
                        rec["status"] = "error"
                        rec["error"] = f"sim {st}: {str(sj)[:200]}"
                    atomic_save(state, STATE_PATH)
                    print(f"  [terminal] {tag} -> {st} alpha={alpha_id}", flush=True)
            except Exception as e:
                print(f"  [poll-err] {tag}: {e}", flush=True)

        # 2) 补投（每周期最多 MAX 条，429 短退避不丢候选）
        infl_n = sum(1 for x in state["items"].values() if x["status"] == "inflight")
        budget = max(0, min(INFLIGHT_MAX - infl_n, MAX_429_RETRY_PER_CYCLE))
        for tag in pend:
            if budget <= 0:
                break
            rec = state["items"][tag]
            wait = min(20 + rec["attempts_429"] * 8, 45)
            try:
                r = sess.post(API + "/simulations", json=build_payload(items[tag]), timeout=60)
                if r.status_code == 401:
                    sess = new_session()
                    continue
                if r.status_code == 429:
                    rec["attempts_429"] += 1
                    print(f"  [429] {tag} attempt={rec['attempts_429']} wait={wait}s", flush=True)
                    atomic_save(state, STATE_PATH)
                    time.sleep(wait)
                    continue
                if r.status_code in (400, 422):
                    rec["status"] = "error"
                    rec["error"] = f"{r.status_code}: {r.text[:300]}"
                    atomic_save(state, STATE_PATH)
                    print(f"  [BAD] {tag}: {r.text[:150]}", flush=True)
                    budget -= 1
                    continue
                r.raise_for_status()
                loc = r.headers.get("Location") or ""
                sim_id = loc.rstrip("/").split("/")[-1]
                rec["status"] = "inflight"
                rec["sim_id"] = sim_id
                rec["attempts_429"] = 0
                atomic_save(state, STATE_PATH)
                print(f"  [submit] {tag} -> {sim_id}", flush=True)
                budget -= 1
                time.sleep(3)  # 限流缓冲
            except Exception as e:
                print(f"  [submit-err] {tag}: {e}", flush=True)
                time.sleep(wait)

        if pend or infl:
            time.sleep(POLL_SEC)

    # ---- 收尾：harvest 指标 ----
    results = {}
    for tag, rec in state["items"].items():
        entry = {"tag": tag, "status": rec["status"], "alpha_id": rec.get("alpha_id"),
                 "error": rec.get("error")}
        if rec["status"] == "done" and rec.get("alpha_id"):
            try:
                r = sess.get(f"{API}/alphas/{rec['alpha_id']}", timeout=60)
                if r.status_code == 200:
                    aj = r.json()
                    isd = aj.get("is", {})
                    entry["metrics"] = {k: isd.get(k) for k in
                                        ("sharpe", "fitness", "turnover", "returns", "drawdown", "margin")}
                    entry["checks"] = [
                        {"name": c.get("name"), "result": c.get("result"),
                         "value": c.get("value"), "limit": c.get("limit")}
                        for c in (isd.get("checks") or [])
                    ]
            except Exception as e:
                entry["harvest_error"] = str(e)
        results[tag] = entry
        time.sleep(0.3)
    atomic_save(results, RESULT_PATH)
    ok = sum(1 for x in results.values() if x["status"] == "done")
    print(f"[finish] done={ok}/{len(results)} -> {RESULT_PATH}")


if __name__ == "__main__":
    main()
