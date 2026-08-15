# -*- coding: utf-8 -*-
"""kor_pipeline.py - KOR 战役端到端编排器（跨层 B + M13/M14）。

把 gate -> submit -> poll -> review -> ledger 串成一条带 checkpoint/resume 的流水线
（落实项目"断点续跑"纪律；此前 8 层人工串跑、无 driver）。

用法:
  python kor_pipeline.py quota                          # M14：48h 滚动提交配额（修正算法）
  python kor_pipeline.py run --file candidates/x.json --dataset model219 --wave 36A
      默认只跑 gate 并打印提交计划（不烧配额）
  python kor_pipeline.py run ... --submit [--max-batches 2] [--force]
      过闸后按批提交（单批在飞规则）+ 轮询到 terminal（挂起熔断）
  python kor_pipeline.py run ... --submit --review --write-ledger
      全链路：评审 + 回写台账
  恢复：重跑同一 --wave 自动从 checkpoint 续跑；--fresh 强制全新。
"""
import argparse, datetime, json, os, sys, time
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gate as gate_mod
import kor_ledger
import metrics_cache
import review_wave as review_mod
from kor_fetch_metrics import Api, load_creds

SETTINGS = json.load(open(os.path.join(ROOT, "config", "settings.json"), encoding="utf-8"))
BATCH = SETTINGS.get("_multi_sim_batch_size", 8)
SUBMIT_LIMIT = 4          # REGULAR_SUBMISSION 48h 滚动上限
SUBMIT_WINDOW_H = 48

TERMINAL = {"COMPLETE", "ERROR", "CANCELLED"}


def ckpt_path(wave):
    return os.path.join(ROOT, "results", f"pipeline_{wave}_checkpoint.json")


def ckpt_load(wave, fresh=False):
    p = ckpt_path(wave)
    if fresh or not os.path.exists(p):
        return {"wave": wave, "stages": {}, "batches": []}
    return json.load(open(p, encoding="utf-8"))


def ckpt_save(ck):
    p = ckpt_path(ck["wave"])
    tmp = p + ".tmp"
    json.dump(ck, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, p)


# ---------------- M14: 配额闸（修正 earliest_release 算法） ----------------

def submission_quota(api):
    j = json.load(api.get("/users/self/alphas?stage=OS&limit=100&order=-dateSubmitted"))
    now = datetime.datetime.now(datetime.timezone.utc)
    win = []
    for a in j.get("results", []):
        ds = a.get("dateSubmitted")
        if not ds:
            continue
        t = datetime.datetime.fromisoformat(ds.replace("Z", "+00:00"))
        if (now - t).total_seconds() < SUBMIT_WINDOW_H * 3600:
            win.append((t, a.get("id")))
    win.sort()
    used = len(win)
    remaining = max(0, SUBMIT_LIMIT - used)
    release = None
    if used >= SUBMIT_LIMIT:
        release = (win[used - SUBMIT_LIMIT][0]
                   + datetime.timedelta(hours=SUBMIT_WINDOW_H)).isoformat()
    return {"used": used, "remaining": remaining, "earliest_release_utc": release,
            "window_ids": [w[1] for w in win],
            "_note": "release 为窗口内最早一笔滑出 48h 的时间（已修正旧版 max() 语义）；"
                     "SUPER 是否独立配额池未验证"}


def api_call(api, method, path, payload=None, retries=5):
    """429 指数退避包装。"""
    delay = 5
    for i in range(retries):
        try:
            return (api.post(path, payload) if method == "post" else api.get(path))
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise


# ---------------- 各阶段 ----------------

def stage_gate(ck, exprs, dataset):
    if ck["stages"].get("gate", {}).get("done"):
        print(f"[gate] 已完成（checkpoint），跳过。passed={len(ck['stages']['gate']['passed'])}")
        return ck["stages"]["gate"]["passed"]
    wl = gate_mod.load_whitelist(dataset)
    cons = json.load(open(os.path.join(ROOT, "reference", "kor_generation_constraints.json"),
                          encoding="utf-8"))
    poison = cons.get("poison_patterns", [])
    passed, failed = [], []
    for e in exprs:
        r = gate_mod.check_one(e, wl, dataset, poison)
        (passed if r["pass"] else failed).append({"expr": e, **({} if r["pass"] else {"issues": r["issues"]})})
    ck["stages"]["gate"] = {"done": True, "total": len(exprs),
                            "passed": passed, "failed": failed,
                            "at": datetime.datetime.now().isoformat(timespec="seconds")}
    ckpt_save(ck)
    print(f"[gate] total={len(exprs)} passed={len(passed)} failed={len(failed)}")
    for f in failed[:5]:
        print(f"  FAIL: {f['expr'][:70]} -> {f['issues'][0][:90]}")
    return passed


def submit_batch(api, exprs):
    payloads = [{"type": "REGULAR", "settings": {k: v for k, v in SETTINGS.items()
                                                 if not k.startswith("_")},
                 "regular": e} for e in exprs]
    body = payloads[0] if len(payloads) == 1 else payloads
    r = api_call(api, "post", "/simulations", body)
    loc = r.headers.get("Location") or ""
    return loc.rstrip("/").split("/")[-1]


def poll_until_terminal(api, msid, hang_min=60, timeout_min=360):
    """M13：轮询循环 + 退避 + 挂起熔断（waveT 卡 24h 教训）。"""
    interval, waited = 20, 0
    last_prog, last_change = None, time.time()
    while waited < timeout_min * 60:
        try:
            d = json.load(api_call(api, "get", "/simulations/" + msid))
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
        if time.time() - last_change > hang_min * 60:
            print(f"  [poll] {msid} 挂起熔断：progress {prog} 超过 {hang_min}min 无变化")
            return "STALLED", d
        time.sleep(interval)
        waited += interval
        interval = min(interval * 1.5, 120)
    return "TIMEOUT", {}


def stage_submit_poll(ck, passed, max_batches, force):
    api = Api(); api.login(*load_creds())  # 单进程单登录（M17）
    q = submission_quota(api)
    print(f"[quota] used={q['used']} remaining={q['remaining']} release={q['earliest_release_utc']}")
    if q["remaining"] <= 0 and not force:
        print("[quota] 提交配额耗尽，中止（--force 强行继续）")
        return
    exprs = [p["expr"] for p in passed]
    done_exprs = {e for b in ck["batches"] if b.get("status") in TERMINAL
                  for e in b.get("exprs", [])}
    todo = [e for e in exprs if e not in done_exprs]
    if not todo:
        print("[submit] 全部批次已 terminal（checkpoint），跳过")
        return
    batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)]
    for bi, batch in enumerate(batches[:max_batches], 1):
        # 单批在飞规则：确认上一批已 terminal（本循环串行天然满足）
        try:
            msid = submit_batch(api, batch)
        except Exception as e:
            print(f"[submit] batch{bi} 提交失败: {e}")
            ck["batches"].append({"exprs": batch, "status": "SUBMIT_FAIL", "error": str(e)[:200]})
            ckpt_save(ck)
            continue
        rec = {"exprs": batch, "multisim": msid, "status": "RUNNING",
               "submitted_at": datetime.datetime.now().isoformat(timespec="seconds")}
        ck["batches"].append(rec)
        ckpt_save(ck)
        print(f"[submit] batch{bi}/{len(batches)} multisim={msid} n={len(batch)}")
        status, detail = poll_until_terminal(api, msid)
        rec["status"] = status
        if status == "COMPLETE":
            children = detail.get("children", [])  # 全量 child（M13 修正 [:8] 截断）
            alphas = []
            for c in children:
                try:
                    sim = json.load(api_call(api, "get", "/simulations/" + c))
                    if sim.get("alpha"):
                        alphas.append(sim["alpha"])
                except Exception:
                    pass
            rec["alphas"] = alphas
            print(f"[poll] {msid} COMPLETE alphas={len(alphas)}")
        elif status == "ERROR":
            errs = []
            for c in detail.get("children", []):
                try:
                    sim = json.load(api_call(api, "get", "/simulations/" + c))
                    if sim.get("error"):
                        errs.append({"child": c, "error": str(sim["error"])[:120]})
                except Exception:
                    pass
            rec["errors"] = errs
            print(f"[poll] {msid} ERROR（{len(errs)} 个子模拟错误，见 checkpoint）")
        else:
            print(f"[poll] {msid} -> {status}")
        ckpt_save(ck)


def stage_review(ck, write_ledger):
    if ck["stages"].get("review", {}).get("done"):
        print("[review] 已完成（checkpoint），跳过")
        return
    alphas = [a for b in ck["batches"] for a in b.get("alphas", [])]
    if not alphas:
        print("[review] 无 alpha 可评审")
        return
    t = review_mod.THRESH["review"]
    rows = metrics_cache.fetch_rows(alphas)
    candidates = [r for r in rows if review_mod.passes(r, t)]
    near = []
    for r in rows:
        if r not in candidates and r.get("sharpe") and r["sharpe"] > review_mod.THRESH["near"]["sharpe_min"]:
            r["walls"] = review_mod.walls(r, t)
            near.append(r)
    out = os.path.join(ROOT, "reviews", f"kor_review_{ck['wave']}.json")
    tmp = out + ".tmp"
    json.dump({"tag": ck["wave"], "all": rows, "candidates": candidates, "near": near},
              open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, out)
    print(f"[review] total={len(rows)} candidates={len(candidates)} near={len(near)} -> {out}")
    if write_ledger:
        def mut(d):
            sr = d.setdefault("submit_ready", [])
            for c in candidates:
                if not any((x.get("id") if isinstance(x, dict) else x) == c["id"] for x in sr):
                    sr.append({"id": c["id"], "note": f"pipeline {ck['wave']} 全门槛过",
                               "queued_at": datetime.date.today().isoformat()})
        kor_ledger.update(mut)
        print(f"[ledger] submit_ready +{len(candidates)}")
    ck["stages"]["review"] = {"done": True, "candidates": len(candidates), "near": len(near)}
    ckpt_save(ck)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("quota")
    p = sub.add_parser("run")
    p.add_argument("--file", required=True)
    p.add_argument("--dataset", required=True)
    p.add_argument("--wave", required=True)
    p.add_argument("--submit", action="store_true")
    p.add_argument("--review", action="store_true")
    p.add_argument("--write-ledger", action="store_true")
    p.add_argument("--max-batches", type=int, default=99)
    p.add_argument("--force", action="store_true")
    p.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    if a.cmd == "quota":
        api = Api(); api.login(*load_creds())
        print(json.dumps(submission_quota(api), ensure_ascii=False, indent=1))
        return

    ck = ckpt_load(a.wave, fresh=a.fresh)
    d = json.load(open(a.file, encoding="utf-8"))
    exprs = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    exprs = [e for e in exprs if isinstance(e, str)]
    passed = stage_gate(ck, exprs, a.dataset)
    if not a.submit:
        print(f"[plan] gate 过 {len(passed)} 式；加 --submit 提交（单批在飞 + 配额闸）")
        return
    stage_submit_poll(ck, passed, a.max_batches, a.force)
    if a.review:
        stage_review(ck, a.write_ledger)
    print(f"[done] checkpoint: {ckpt_path(a.wave)}")


if __name__ == "__main__":
    main()
