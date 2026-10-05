#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单条扇出回测 runner —— 小批量的正确姿势（2026-10-04 wave273 实测教训）。

背景：
  wave273 首次以 8 条打包 multisim 提交 → **整批 ERROR**，8 个 child 全 FAIL 且
  `message` 为 None（无原因）；改成逐条单发（并发 4）→ 8 条全部 201 Created、7 条 COMPLETE。
  随后用 2 条打包复现 → COMPLETE 正常。
  ⇒ 判定：**批内只要有一条非法表达式，整批可能被连坐判 ERROR 且不返回原因**。
  小批量排查/探针一律走本脚本（逐条单发 + 逐条记错），不要用 multisim runner。

与 run_wave269_fincf_residual.py 的区别：
  - 那个走 `/simulations` 的 list 载荷（multisim），一错全连坐；
  - 这个逐条 POST 单 simulation，并发受控，**某条挂只影响那一条**；
  - 断点续跑：checkpoint 记已完成 code，重启只跑剩下的；
  - 平台错误信息抓取：批内失败时逐条回读 `/simulations/{id}` 的 message/alpha 字段。

用法：
  python tracking/EUR/scripts/run_wave_single_fanout.py <TAG> [--fresh] [--conc 2]
  环境变量：
    FANOUT_SLOTS   并发单条数（默认 2；平台总槽 7，多会话并存时留余量给其它流水线）
"""
import argparse
import csv
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "Claude" / "skills" / "wq-brain-campaign-toolkit" / "scripts"))

from _lib.common import CampaignContext, atomic_write, load_credentials  # noqa: E402
from _lib.api import Api, api_call  # noqa: E402
from wqb.expression.op_arity import (  # noqa: E402
    check_expressions_strict,
    format_report,
)

DATASET = "risk70"
OUT_DIR = ROOT / "tracking" / "EUR" / "results"
#: 终态集合。``WARNING`` 必须在内——2026-10-04 wave290 实测：B7 的 sim
#: 返回 ``status="WARNING"``（已产出 alpha）却不在原集合里，导致轮询死循环，
#: 进程卡 38 分钟不退出（其余 15 条早已完成）。
TERMINAL = {"COMPLETE", "FAIL", "ERROR", "CANCELLED", "WARNING"}
POLL = 10


def load_ckpt(path):
    if not path.exists():
        return []
    try:
        return json.load(open(path, encoding="utf-8")).get("results", [])
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tag")
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--dataset", default=DATASET,
                    help=f"结果元数据里的数据集标签（默认 {DATASET}）；表达式实际取数由字段决定")
    ap.add_argument("--no-gate", action="store_true",
                    help="跳过算子存在性+元数硬闸（只限已回测过的老波次）")
    ap.add_argument("--conc", type=int, default=int(os.environ.get("FANOUT_SLOTS", "2")))
    args = ap.parse_args()

    tag = args.tag
    _ds = args.dataset
    inp = ROOT / "tracking" / "EUR" / "candidates" / f"eur_{tag}_items.json"
    ckpt = OUT_DIR / f"{tag}_checkpoint.json"
    out_csv = OUT_DIR / f"{tag}_results.csv"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    items = json.load(open(inp, encoding="utf-8"))

    # 发批前硬闸：元数违规 + 未知算子。wave285 教训——`ts_std`（正确是
    # `ts_std_dev`）不在平台算子表里，离线闸放行、发到平台 3 条全 ERROR，
    # 白扔 3 个槽位。任何一条不合法即中止，绝不带着坏表达式上平台。
    if not args.no_gate:
        report = check_expressions_strict(
            [(it.get("note", str(i + 1)), it["code"]) for i, it in enumerate(items)])
        if not report["ok"]:
            print(format_report(report), flush=True)
            print(f"[gate] 硬闸拒绝：{report['total'] - report['passed']} 条不可提交，"
                  f"已中止（--no-gate 可跳过，仅限已确认过的老波次）", flush=True)
            return 2
        print(f"[gate] {report['passed']}/{report['total']} PASS（算子存在性 + 元数）", flush=True)

    carried = [] if args.fresh else load_ckpt(ckpt)
    #去重键必须是 (code, settings) 而不是 code —— 否则同表达式不同设置档的变体
    #（如 wave325 的 A1/A5/A6/A7/A10，同为 rank(analyst_quantile1_60d_pred)但 decay/neut 不同）
    # 在续跑时会被静默跳过，丢掉 4 个设置档。实测确认 submit() 不按 code 去重，
    # 每条独立 POST /simulations，故此处也必须逐条独立判定。
    def _key(it):
        # maxTrade/nanHandling/pasteurization 都在键里 —— 加任何设置维度都必须同步加这里，
        # 否则同表达式不同该维度的变体会在续跑时被静默跳过（wave325 踩过 code-only 的坑）。
        return (it["code"], it.get("decay"), it.get("truncation"),
                it.get("neut"), it.get("universe"), it.get("maxTrade"),
                it.get("nanHandling"), it.get("pasteurization"))

    done = {_key(r) for r in carried
            if r.get("code") and r.get("id") not in (None, "DROPPED")}
    todo = [it for it in items if _key(it) not in done]
    print(f"[resume] 总 {len(items)} 已完成 {len(done)} 待跑 {len(todo)} conc={args.conc}", flush=True)
    if not todo:
        return

    ctx = CampaignContext("tracking/EUR")
    base = {k: v for k, v in ctx.settings.items() if not k.startswith("_")}
    api = Api()
    api.login(*load_credentials())

    def submit(it):
        s = dict(base)
        for k, key in (("decay", "decay"), ("truncation", "truncation"),
                       ("neut", "neutralization"), ("universe", "universe"),
                       # 以下三项为 2026-10-05 新增：maxTrade 由论坛处方（robust 偏离时开），
                       # nanHandling/pasteurization 一并放开以备后续波次，无需再改运行器。
                       ("maxTrade", "maxTrade"),
                       ("nanHandling", "nanHandling"),
                       ("pasteurization", "pasteurization")):
            if it.get(k) is not None:
                s[key] = it[k]
        try:
            r = api_call(api, "post", "/simulations",
                         {"type": "REGULAR", "settings": s, "regular": it["code"]})
        except Exception as e:
            return it, None, f"SUBMIT_EXC:{e}"
        if r.status not in (200, 201):
            return it, None, f"SUBMIT_HTTP{r.status}"
        sid = (r.headers.get("Location") or "").rstrip("/").split("/")[-1]
        return it, sid, None

    results = list(carried)
    pending = list(todo)
    inflight = {}

    with ThreadPoolExecutor(max_workers=args.conc) as ex:
        while pending or inflight:
            while pending and len(inflight) < args.conc:
                it, sid, err = ex.submit(submit, pending.pop(0)).result()
                if err or not sid:
                    print(f"[submit-fail] {err} :: {it.get('note', it['code'][:50])}", flush=True)
                    results.append({"id": "DROPPED", "code": it["code"], "note": it.get("note", ""),
                                    "dataset": _ds, "error": err})
                else:
                    inflight[sid] = it
                    print(f"[submit] {sid} :: {it.get('note', it['code'][:50])}", flush=True)

            time.sleep(POLL)
            for sid in list(inflight):
                try:
                    d = json.load(api.get(f"/simulations/{sid}"))
                except Exception as e:
                    print(f"[poll] {sid} err {e}", file=sys.stderr, flush=True)
                    continue
                st = d.get("status")
                if st not in TERMINAL:
                    continue
                it = inflight.pop(sid)
                aid = d.get("alpha")
                if aid:
                    try:
                        a = json.load(api.get(f"/alphas/{aid}"))
                        # 字段名跨形态兼容：平台 /alphas/{id} 把指标放在 is.*，
                        # 但 2Y / sub_universe / robust 在不同版本里名字不一致（曾长期抓到 None，
                        # 导致回测层看不到 LOW_2Y_SHARPE —— 见记忆 §48.5）。这里多路兜底。
                        srcs = [a.get("is") or {}, a.get("metrics") or {}, a]

                        def pick(*names):
                            for src in srcs:
                                for n in names:
                                    v = src.get(n)
                                    if v is not None:
                                        return v
                            return None

                        # ★ 平台原始 /alphas/{id} 的 is.* 里【没有】twoYearSharpe /
                        # subUniverseSharpe / robustUniverseSharpe —— 它们只存在于
                        # is.checks 各条目的 value（实测 2026-10-04）。旧代码按 is.get(
                        # "twoYearSharpe") 取 ⇒ 长期全 None ⇒ 回测层看不到 LOW_2Y_SHARPE。
                        checks = [c for c in (a.get("is", {}).get("checks") or [])
                                  if isinstance(c, dict)]

                        def chk(name):
                            for c in checks:
                                if c.get("name") == name:
                                    return c.get("value")
                            return None

                        fails = [c["name"] for c in checks if c.get("result") == "FAIL"]
                        top_checks = a.get("checks") or {}
                        for c in (top_checks.get("fail") or []):
                            if isinstance(c, dict) and c.get("name"):
                                fails.append(c["name"])
                        hard_warn = [c["name"] for c in checks
                                     if c.get("result") == "WARNING" and c.get("name") in
                                     ("LOW_2Y_SHARPE", "LOW_SHARPE", "LOW_FITNESS",
                                      "LOW_SUB_UNIVERSE_SHARPE",
                                      "LOW_ROBUST_UNIVERSE_SHARPE", "CLUSTER_TEST")]
                        row = {"id": aid, "code": it["code"], "note": it.get("note", ""),
                               "dataset": _ds,
                               # ★ 设置档必须落盘：resume 的去重键是 (code, decay,
                               # truncation, neut, universe)，记录行缺这几个键就永远
                               # 匹配不上 items ⇒ 续跑会重跑全部变体。见 §73.1。
                               "decay": it.get("decay"),
                               "truncation": it.get("truncation"),
                               "maxTrade": it.get("maxTrade"),
                               "nanHandling": it.get("nanHandling"),
                               "pasteurization": it.get("pasteurization"),
                               "neut": it.get("neut"),
                               "universe": it.get("universe"),
                               "sharpe": pick("sharpe"),
                               "fitness": pick("fitness"),
                               "two_year_sharpe": pick("twoYearSharpe", "two_year_sharpe")
                               or chk("LOW_2Y_SHARPE"),
                               "margin_bp": round((pick("margin") or 0) * 10000, 2),
                               "turnover_pct": pick("turnover"),
                               "sub_universe_sharpe": pick("subUniverseSharpe",
                                                           "sub_universe_sharpe")
                               or chk("LOW_SUB_UNIVERSE_SHARPE"),
                               "robust_universe_sharpe": pick("robustUniverseSharpe",
                                                              "robust_universe_sharpe")
                               or chk("LOW_ROBUST_UNIVERSE_SHARPE"),
                               "cluster_test": chk("CLUSTER_TEST"),
                               "failed_checks": ",".join(dict.fromkeys(fails)),
                               "hard_warns": ",".join(dict.fromkeys(hard_warn)),
                               "sim": sid}
                    except Exception as e:
                        row = {"id": aid, "code": it["code"], "note": it.get("note", ""),
                               "dataset": _ds,
                               # ★ 设置档必须落盘：resume 的去重键是 (code, decay,
                               # truncation, neut, universe)，记录行缺这几个键就永远
                               # 匹配不上 items ⇒ 续跑会重跑全部变体。见 §73.1。
                               "decay": it.get("decay"),
                               "truncation": it.get("truncation"),
                               "maxTrade": it.get("maxTrade"),
                               "nanHandling": it.get("nanHandling"),
                               "pasteurization": it.get("pasteurization"),
                               "neut": it.get("neut"),
                               "universe": it.get("universe"), "error": f"fetch:{e}", "sim": sid}
                else:
                    row = {"id": "DROPPED", "code": it["code"], "note": it.get("note", ""),
                           "dataset": _ds, "error": f"NO_ALPHA_ID status={st}", "sim": sid}
                    print(f"[miss] {sid} status={st} msg={str(d.get('message'))[:200]} :: "
                          f"{it.get('note', it['code'][:50])}", flush=True)
                results.append(row)
                atomic_write(str(ckpt), {"ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                                         "tag": tag, "results": results})

    results.sort(key=lambda r: -(r.get("sharpe") or -99))
    atomic_write(str(ckpt), {"ran_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                             "tag": tag, "results": results})
    cols = ["id", "dataset", "code", "note", "sharpe", "fitness", "two_year_sharpe", "margin_bp",
            "turnover_pct", "sub_universe_sharpe", "robust_universe_sharpe", "failed_checks",
            "hard_warns", "sim"]
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in results:
            w.writerow(r)
    print(f"[final] rows={len(results)}", flush=True)
    for r in results:
        print(f"  {r.get('id'):12} S={r.get('sharpe')} F={r.get('fitness')} "
              f"TO={r.get('turnover_pct')} FAIL={r.get('failed_checks') or r.get('error')}")


if __name__ == "__main__":
    import sys as _sys

    _ret = main()
    if isinstance(_ret, int) and _ret:
        _sys.exit(_ret)
