#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wave269 EUR fundamental23 融资现金流族 × 残差化破 prod 墙 runner.

背景（2026-10-03 实测）：
  rKOdkZX9 = reverse(rank(ts_mean(fin/assets,252)))                       prod 0.9073
  78NoOeVx = vector_neut(reverse(rank(fin/assets)), rank(ocf/assets))     prod 0.7432
  => 用经营现金流做 vector_neut 正交轴的一次残差化，把 prod 削了 0.164。
  本波沿 残差轴 / 分母 / 分子兄弟 / 等价算子 四轴展开，找 <0.7 的结构。

用法：
  python tracking/EUR/scripts/run_wave269_fincf_residual.py            # 续跑（默认）
  W269_FRESH=1 python tracking/EUR/scripts/run_wave269_fincf_residual.py  # 强制全新
"""
import csv
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # .../tracking/EUR/scripts/x.py -> 仓库根
sys.path.insert(0, str(ROOT))

TOOLKIT = Path(
    os.environ.get(
        "WQ_TOOLKIT",
        ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts",
    )
)
sys.path.insert(0, str(TOOLKIT))

from _lib.common import CampaignContext, atomic_write, load_credentials  # noqa: E402
from _lib.api import Api, api_call  # noqa: E402
from _lib.poller import TERMINAL  # noqa: E402
import metrics_cache  # noqa: E402

DATASET = "fundamental23"
# 波次代号：改 W269_TAG 即复用同一 runner 跑下一波，不必复制脚本
TAG = os.environ.get("W269_TAG", "wave269_fincf_residual")
INPUT = ROOT / "tracking" / "EUR" / "candidates" / f"eur_{TAG}_items.json"
OUT_DIR = ROOT / "tracking" / "EUR" / "results"
OUT_JSON = OUT_DIR / f"{TAG}_results.json"
OUT_CSV = OUT_DIR / f"{TAG}_results.csv"
CKPT = OUT_DIR / f"{TAG}_checkpoint.json"

# 槽位按"在飞作业数"动态定：平台总并发 7 槽，本机常有其他 _serial_v*.py 作业占槽。
# 开工前先数进程，SLOTS = 7 - 已占用 - 1（留 1 槽余量），否则必撞
# CONCURRENT_SIMULATION_LIMIT_EXCEEDED（2026-10-03 实测踩过）。
SLOTS = int(os.environ.get("W269_SLOTS", "1"))
BATCH_SIZE = 8
POLL_INTERVAL = 15
STALL_MINUTES = 10  # 记忆：progress .1 停滞 >10min 且 child=0 判卡住

FRESH = os.environ.get("W269_FRESH") == "1"


def settings_fingerprint(s):
    keys = ["region", "universe", "delay", "neutralization", "decay", "truncation"]
    payload = {k: s.get(k) for k in keys}
    return hashlib.sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]


def load_checkpoint():
    """返回 (done_codes, carried_results)。settings_hash 不匹配即判 fresh。"""
    if FRESH or not CKPT.exists():
        return set(), []
    try:
        ck = json.load(open(CKPT, encoding="utf-8"))
    except Exception as e:
        print(f"[ckpt] 读取失败({e})，按 fresh 处理", file=sys.stderr)
        return set(), []
    carried = [r for r in ck.get("results", []) if r.get("id") not in (None, "", "STALLED")]
    done = {r["code"] for r in carried if r.get("code")}
    return done, carried


def save_checkpoint(results, settings_hash=None):
    payload = {"ran_at": time.strftime("%Y-%m-%d %H:%M:%S"), "results": results}
    if settings_hash:
        payload["settings_hash"] = settings_hash
    atomic_write(str(CKPT), payload)


def save_progress(results, candidates):
    results_sorted = sorted(
        results, key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99)
    )
    payload = {
        "ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset": DATASET,
        "slots": SLOTS,
        "batch_size": BATCH_SIZE,
        "total_alphas": len(results_sorted),
        "candidates": candidates,
        "results": results_sorted,
    }
    atomic_write(str(OUT_JSON), payload)
    fieldnames = [
        "id", "dataset", "code", "note", "decay", "truncation", "sharpe", "fitness",
        "two_year_sharpe", "margin_bp", "turnover_pct", "rn_sharpe", "rn_fitness",
        "failed_checks", "multisim", "batch_idx",
    ]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in results_sorted:
            w.writerow(r)
    print(f"[save] rows={len(results_sorted)} candidates={len(candidates)}")


def submit_batch(api, settings, batch_idx, batch):
    payloads = []
    for it in batch:
        s = {k: v for k, v in settings.items() if not k.startswith("_")}
        if it.get("decay") is not None:
            s["decay"] = it["decay"]
        if it.get("truncation") is not None:
            s["truncation"] = it["truncation"]
        if it.get("neut") is not None:
            s["neutralization"] = it["neut"]
        payloads.append({"type": "REGULAR", "settings": s, "regular": it["code"]})
    body = payloads[0] if len(payloads) == 1 else payloads
    r = api_call(api, "post", "/simulations", body)
    loc = r.headers.get("Location") or ""
    msid = loc.rstrip("/").split("/")[-1]
    if not msid:
        # 429 / 并发超限会走到这里：必须可见，否则静默空转
        print(f"[submit][FAIL] batch{batch_idx + 1} 无 Location；"
              f"status={getattr(r, 'status_code', '?')} body={str(getattr(r, 'text', ''))[:300]}",
              file=sys.stderr, flush=True)
    print(f"[submit] batch{batch_idx + 1} multisim={msid} n={len(batch)}", flush=True)
    return msid


def fetch_rows_for_multisim(api, fetcher, msid):
    ms = json.load(api.get(f"/simulations/{msid}"))
    ids = []
    for c in ms.get("children", []):
        try:
            sim = json.load(api.get(f"/simulations/{c}"))
            if sim.get("alpha"):
                ids.append(sim["alpha"])
        except Exception as e:
            print(f"[child] {c} err {e}", file=sys.stderr)
    if not ids and ms.get("alpha"):
        ids.append(ms["alpha"])
    rows = []
    for aid in ids:
        # 2026-10-03 事故：此处原无 try/except，一次网络异常即整脚本崩溃，
        # 已完成的批次结果因未落盘而丢失。单条取数失败必须隔离。
        try:
            r = fetcher.fetch(aid)
        except Exception as e:
            print(f"[child] alpha {aid} fetch exception: {e}", file=sys.stderr, flush=True)
            continue
        if isinstance(r, dict) and "error" not in r:
            rows.append(r)
        else:
            print(f"[child] alpha {aid} fetch err: {r}", file=sys.stderr, flush=True)
    return rows


def main():
    ctx = CampaignContext("tracking/EUR")
    settings = ctx.settings
    fp = settings_fingerprint(settings)
    print(f"[settings] {fp} universe={settings.get('universe')} "
          f"neut={settings.get('neutralization')} decay={settings.get('decay')} "
          f"trunc={settings.get('truncation')}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    done_codes, results = load_checkpoint()
    # settings_hash 守卫：档位变了就当全新，避免不同设置混进同一 checkpoint
    if done_codes and CKPT.exists():
        try:
            ck = json.load(open(CKPT, encoding="utf-8"))
            if ck.get("settings_hash") and ck.get("settings_hash") != fp:
                print("[ckpt] settings 已变更，丢弃旧 checkpoint 按 fresh 跑")
                done_codes, results = set(), []
        except Exception:
            pass

    items = json.load(open(INPUT, encoding="utf-8"))
    todo = [it for it in items if it["code"] not in done_codes]
    print(f"[resume] 总 {len(items)} 条，已完成 {len(done_codes)} 条，本轮待跑 {len(todo)} 条")
    if not todo:
        save_progress(results, [])
        print("[done] 全部已完成，无待跑项")
        return

    api = Api()
    api.login(*load_credentials())
    fetcher = metrics_cache.MetricsFetcher(ctx)

    pending = [todo[i:i + BATCH_SIZE] for i in range(0, len(todo), BATCH_SIZE)]
    inflight = {}
    candidates = []
    last_seen = {}
    attempts = {}          # code -> 已尝试次数
    MAX_ATTEMPTS = 2       # 超过即判该表达式不可用并丢弃，避免死循环

    def _retry(code):
        n = attempts.get(code, 0) + 1
        attempts[code] = n
        return n <= MAX_ATTEMPTS

    start = 0

    def _fill():
        """填槽；提交失败(如 429)则整批退回 pending，等下一轮再试。"""
        nonlocal start
        while len(inflight) < SLOTS and pending:
            batch = pending.pop(0)
            msid = submit_batch(api, settings, start, batch)
            if not msid:
                pending.insert(0, batch)
                return False
            inflight[msid] = {"batch_idx": start, "batch": batch}
            last_seen[msid] = (None, time.time())
            start += 1
            time.sleep(0.3)
        return True

    if not _fill() and not inflight:
        print("[abort] 首轮提交即失败且无在飞作业，退出（多为并发超限）", file=sys.stderr)
        return

    fill_fail_streak = 0
    while inflight or pending:
        if not inflight and pending:
            # 上一轮填槽被 429 打回：退避后重试，连续失败超限才放弃
            time.sleep(POLL_INTERVAL)
            if _fill():
                fill_fail_streak = 0
                continue
            fill_fail_streak += 1
            if fill_fail_streak > 10:
                print("[abort] 连续 10 次填槽失败（多为并发超限），剩余 "
                      f"{sum(len(b) for b in pending)} 条未跑", file=sys.stderr)
                break
            continue
        fill_fail_streak = 0
        done = []
        now = time.time()
        for msid in list(inflight.keys()):
            rec = inflight[msid]
            try:
                d = json.load(api.get(f"/simulations/{msid}"))
            except Exception as e:
                print(f"[poll] {msid} check err {e}", file=sys.stderr)
                continue
            status = d.get("status")
            progress = d.get("progress")

            if status not in TERMINAL:
                prev_prog, prev_ts = last_seen.get(msid, (None, now))
                if progress != prev_prog:
                    last_seen[msid] = (progress, now)
                elif now - prev_ts > STALL_MINUTES * 60:
                    print(f"[stall] {msid} progress={progress} 停滞 {STALL_MINUTES}min，判卡住并补发")
                    done.append(msid)
                    # 卡住 ≠ 表达式错：整批重新入队（受重试上限保护）
                    retry_batch = [it for it in rec["batch"] if _retry(it["code"])]
                    if retry_batch:
                        pending.insert(0, retry_batch)
                else:
                    print(f"[poll] {msid} status={status} progress={progress}")
                continue

            print(f"[poll] {msid} -> {status}")
            done.append(msid)
            if msid in last_seen:
                del last_seen[msid]
            # 2026-10-04 修复：批次内可能出现「同一表达式 + 不同档位(neut/decay/trunc)」，
            # 原先用 code 做 key 会被最后一条覆盖，导致 note/档位全部串成同一个。
            # 改用 (code, neut, decay, truncation) 复合键。
            meta_map = {
                (
                    it["code"],
                    it.get("neut"),
                    it.get("decay"),
                    it.get("truncation"),
                ): it
                for it in rec["batch"]
            }
            try:
                rows = fetch_rows_for_multisim(api, fetcher, msid)
            except Exception as e:
                print(f"[poll] {msid} 取数异常: {e}", file=sys.stderr, flush=True)
                rows = []
                bkey = rec["batch"][0]["code"]
                n = attempts.get(bkey, 0) + 1
                attempts[bkey] = n
                if n <= MAX_ATTEMPTS:
                    print(f"[retry] 整批退回重排(第{n}次)", flush=True)
                    pending.insert(0, rec["batch"])
            for r in rows:
                # 档位扫描批里同一 code 出现多次，需带上本次 settings 才能命中正确的 note
                mkey = (
                    r.get("code"),
                    r.get("neut"),
                    r.get("decay"),
                    r.get("truncation"),
                )
                meta = meta_map.get(mkey) or meta_map.get((r.get("code"), None, None, None)) or {}
                r["dataset"] = meta.get("dataset", DATASET)
                r["note"] = meta.get("note", "")
                if meta.get("neut"):
                    r["neut"] = meta["neut"]
                r["multisim"] = msid
                r["batch_idx"] = rec["batch_idx"]
                results.append(r)
            # 只把拿到 alpha_id 的算完成
            got = {r.get("code") for r in rows if r.get("id")}
            for it in rec["batch"]:
                if it["code"] not in got:
                    if _retry(it["code"]):
                        print(f"[miss] 未取到 alpha_id，重排(第{attempts[it['code']]}次): "
                              f"{it.get('note', it['code'][:60])}")
                        pending.insert(0, [it])
                    else:
                        print(f"[drop] 连续 {MAX_ATTEMPTS} 次无 alpha_id，判不可用: "
                              f"{it.get('note', it['code'][:60])}")
                        results.append({
                            "id": "DROPPED", "dataset": DATASET, "code": it["code"],
                            "note": it.get("note", ""), "multisim": msid,
                            "batch_idx": rec["batch_idx"], "error": "NO_ALPHA_ID",
                        })
            if pending:
                new_batch = pending.pop(0)
                new_msid = submit_batch(api, settings, start, new_batch)
                if not new_msid:
                    pending.insert(0, new_batch)   # 提交失败，退回等下轮
                else:
                    inflight[new_msid] = {"batch_idx": start, "batch": new_batch}
                    last_seen[new_msid] = (None, time.time())
                    start += 1
                    time.sleep(0.3)

        for msid in done:
            if msid in inflight:
                del inflight[msid]

        save_checkpoint(results, fp)
        if results or candidates:
            save_progress(results, candidates)

        if inflight:
            time.sleep(POLL_INTERVAL)

    results.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    save_checkpoint(results, fp)
    save_progress(results, candidates)
    print(f"[final] rows={len(results)}")


if __name__ == "__main__":
    main()
