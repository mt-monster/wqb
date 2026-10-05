#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单发 fanout 运行器：逐条独立设置档派发 + 断点续跑 + 指标收割。

⚠ 本脚本曾于 2026-10-05 被外部清理进程删除（连同 check_wave_fields.py / fetch_prod.py），
  故按当日日志 §73/ §80 / §83 的踩坑记录**重建并保留全部已验证补丁**。

★ 三个必须同步改的地方（缺一不可，见 §73 / §80）：
  ① ``SETTINGS_KEYS`` 提交映射——漏了则 items 里写了不进 settings（杠杆完全无效）；
  ② ``_key()`` 去重键——漏了则同表达式不同该维度的变体**续跑时被静默跳过**；
  ③ 记录行落盘（成功行 + DROPPED 行**两处**都补）——漏了则每次续跑**重跑全部**。

★ 平台实测（EUR/D1，2026-10-05）：``maxTrade`` **只认 "ON"/"OFF"，数值 0.05/0.1 → HTTP 400**。
  且 `SimulationSettings.maxTrade` 默认值是 **"OFF"** ——
  所以"不设 maxTrade"≡ OFF，而 wave328 的 S2(ON) 与不设拿到同一 alpha_id 是因为
  **平台在 payload 组装时按显式值走**；测该键必须写 **ON vs OFF 显式对照**。

items 文件名约定（硬性）：``tracking/<REGION>/candidates/<region>_<tag>_items.json``
（``--tag wave330_decay_grid`` ⇒ 读 ``eur_wave330_decay_grid_items.json``）

items 每行支持的键::

    {"code": "<表达式>", "note": "说明",              # 必需
     "decay": 10, "truncation": 0.08, "neut": "FAST", "universe": "TOPCS1600",
     "maxTrade": "ON", "nanHandling": "ON", "pasteurization": "ON"}

用法::

    python tracking/EUR/scripts/run_wave_single_fanout.py wave330_decay_grid \
        --dataset multi_source_model --fresh --conc 4
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from wqb.expression.op_arity import check_expressions_strict, format_report  # noqa: E402

# items 键 →平台 settings 键
SETTINGS_KEYS = (
    ("decay", "decay"),
    ("truncation", "truncation"),
    ("neut", "neutralization"),
    ("universe", "universe"),
    ("maxTrade", "maxTrade"),
    ("nanHandling", "nanHandling"),
    ("pasteurization", "pasteurization"),
)
# 去重键用的 item 键（顺序固定，缺一不可）
KEY_ITEMS = ("decay", "truncation", "neut", "universe",
             "maxTrade", "nanHandling", "pasteurization")


def load_ckpt(path):
    path = str(path)  # ★ Path + str 会 TypeError，统一转 str
    if not os.path.exists(path):
        return []
    try:
        return json.load(open(path, encoding="utf-8")).get("results", [])
    except Exception:
        return []


def save_ckpt(path, rows):
    """原子写，防中断损坏。★ path 统一转 str（Path + str 会 TypeError）。"""
    path = str(path)
    tmp = path + ".tmp"
    json.dump({"results": rows}, open(tmp, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def _key(it):
    """★ 去重键必须含全部设置维度（§73/§80）。漏一个 ⇒ 续跑静默跳过该维度变体。"""
    return (it["code"],) + tuple(it.get(k) for k in KEY_ITEMS)


def settings_row(it):
    """★ 记录行落盘设置档（§73/§80）。漏了 ⇒ _key(r) 读记录行得 (code,None,…) ⇒ 每次重跑全部。"""
    row = {"code": it["code"], "note": it.get("note", "")}
    row.update({k: it.get(k) for k in KEY_ITEMS})
    return row


def extract(body, it):
    """从 alpha details 抽指标与闸门。

    ★★★ 平台 `brain_client.get_alpha_details` 的**真实结构**（2026-10-05 实测，勿凭直觉改）：

      指标：`alpha["is"]` 里有 sharpe / fitness / turnover / returns / drawdown / margin / pnl …
            ⚠ **但 2Y / sub / robust 三个不在这里**。

      ★ **`alpha["is"]["checks"]` 才是全指标权威口径**——每个 check 带name/result/value：
            LOW_SHARPE  value=1.75      LOW_FITNESS    value=1.17
            LOW_2Y_SHARPE value=1.76★  LOW_SUB_UNIVERSE_SHARPE value=1.63★
            LOW_ROBUST_UNIVERSE_SHARPE value=1.44★  CLUSTER_TEST value=1.09 (WARNING)
            result ∈ {PASS, FAIL, WARNING, PENDING}
      ⇒ **2Y/sub/robust 只能从 checks 里按 name 取 value**，别去 `is` 里找。

      MCP 工具（`mcp__wq-brain-http__get_alpha_details`）会把它**规范化**成
      `alpha["metrics"]`（snake_case：two_year_sharpe / sub_universe_sharpe / robust_universe_sharpe）
      + `alpha["checks"]`（分 fail/warning/pass/pending 四组）+ `alpha["ra"]`。
      ⇒ 两种格式都认：优先 `metrics`，回退 `is` + `is.checks`。
    """
    row = settings_row(it)
    a = body.get("alpha") if isinstance(body.get("alpha"), dict) else body
    isv = a.get("is") or {}
    m = a.get("metrics")
    if not isinstance(m, dict) or m.get("sharpe") is None:
        m = isv                      # ★ 原始 API 形态

    def pick(*names):
        for n in names:
            v = m.get(n)
            if v is not None:
                return v
        return None

    row["id"] = a.get("id") or body.get("id")
    row["sharpe"] = pick("sharpe")
    row["fitness"] = pick("fitness")
    row["turnover_pct"] = pick("turnover")
    row["returns"] = pick("returns")
    row["drawdown"] = pick("drawdown")
    row["margin"] = pick("margin")
    row["pnl"] = pick("pnl")
    row["long_count"] = pick("longCount", "long_count")
    row["short_count"] = pick("shortCount", "short_count")

    # ★ checks：两种形态（list / dict分组）都要认
    checks = {}
    if isinstance(isv.get("checks"), list):          # 原始 API：[{name,result,value}]
        for c in isv["checks"]:
            if isinstance(c, dict) and c.get("name"):
                checks[c["name"]] = c
    for c in (a.get("checks") or []):                 # 容错：也接受 list
        if isinstance(c, dict) and c.get("name"):
            checks.setdefault(c["name"], c)
    row["sub_universe_sharpe"] = pick("sub_universe_sharpe", "subUniverseSharpe") \
        or (checks.get("LOW_SUB_UNIVERSE_SHARPE") or {}).get("value")
    row["two_year_sharpe"] = pick("two_year_sharpe", "twoYearSharpe") \
        or (checks.get("LOW_2Y_SHARPE") or {}).get("value")
    row["robust_universe_sharpe"] = pick("robust_universe_sharpe", "robustUniverseSharpe") \
        or (checks.get("LOW_ROBUST_UNIVERSE_SHARPE") or {}).get("value")
    row["cluster_test"] = (checks.get("CLUSTER_TEST") or {}).get("value")
    row["prod_corr"] = a.get("prodCorrelation") or (a.get("prod") or {}).get("correlation")

    # 闸门：★ 只有 result==FAIL 才算挂；WARNING 不是失败（记忆 §0：warning≠安全，但≠failed）
    fails, warns, passes, pendings = [], [], [], []
    for name, c in checks.items():
        res = str(c.get("result") or "").upper()
        if res == "FAIL":
            fails.append(name)
        elif res == "WARNING":
            warns.append(f"{name}({c.get('value')})")
        elif res == "PASS":
            passes.append(name)
        elif res == "PENDING":
            pendings.append(name)
    ck = a.get("checks")
    if isinstance(ck, dict):                 # MCP 规范化的分组形态
        fails = ck.get("fail") or fails
        warns = [w.get("name") if isinstance(w, dict) else str(w)
                 for w in (ck.get("warning") or [])] or warns
        passes = ck.get("pass") or passes
        pendings = ck.get("pending") or pendings
    row["fail_reasons"] = ",".join(fails) or None
    row["warn_reasons"] = ",".join(warns) or None
    row["pass_reasons"] = ",".join(passes) or None
    row["pending_reasons"] = ",".join(pendings) or None
    # failed_ra 只数 FAIL
    row["failed_ra_count"] = len(fails)
    row["ra_failed"] = bool(fails)

    py = a.get("pyramids") or {}
    lst = py.get("list") if isinstance(py, dict) else None
    row["pyramid"] = lst[0].get("name") if lst else None
    return row


async def run(args, items, todo, ckpt, carried):
    # ★ _pyenv 在 tools/ 下（不是 src/），本脚本在 tracking/<R>/scripts/ 需显式加路径。
    #   它提供 bootstrap_paths()（把 MCP 目录加进 sys.path）与 reexec_under_venv()。
    sys.path.insert(0, str(ROOT / "tools"))
    import _pyenv
    _pyenv.bootstrap_paths()
    from brain_api import brain_client
    from brain_api_models import SimulationData, SimulationSettings

    reg = args.region
    universe = "TOPCS1600" if reg == "EUR" else "TOP3000"
    # 本地战役基线设置
    base = {
        "instrumentType": "EQUITY", "region": reg, "delay": 1,
        "universe": universe, "decay": 40.0, "neutralization": "FAST",
        "truncation": 0.0, "language": "FASTEXPR", "visualization": True,
        "testPeriod": "P0Y0M", "unitHandling": "VERIFY",
    }

    results = list(carried)
    sem = asyncio.Semaphore(max(1, args.conc))

    async def submit(it):
        """★ `create_simulation` **内部已轮询到终态**并返回 alpha 详情dict
        （brain_mixin_simulation.py：轮询 location → progress_data["alpha"]
          → GET /alphas/{id} → return alpha_response.json()）。
        ⇒ 不需要外层轮询循环；并发由内部 `_create_simulation_semaphore` 限流。

        ⚠ 但**不要信返回 dict 的 metrics 形态**：实测当「表达式+设置」与已有 alpha
        相同时平台直接回既有 id，返回形态与新建不同（metrics 取不到）。
        ⇒ 一律以 `get_alpha_details(aid)` 为准。
        """
        s = dict(base)
        for k, key in SETTINGS_KEYS:
            if it.get(k) is not None:
                s[key] = it[k]
        async with sem:
            try:
                sd = SimulationData(type="REGULAR",
                                    settings=SimulationSettings(**s),
                                    regular=it["code"])
                res = await brain_client.create_simulation(sd)
            except Exception as e:
                msg = f"{type(e).__name__}: {e}"
                if "400" in msg:
                    msg = "HTTP400 " + msg[-160:]
                return it, None, msg, None
        if not isinstance(res, dict):
            return it, None, f"BAD_RESP:{type(res).__name__}", None
        if res.get("error") or not res.get("id"):
            return it, None, f"API_ERR:{str(res.get('error'))[:160]}", None
        aid = res["id"]
        # ★ 两种指标格式都要认：原始 API 在 `is`（驼峰段），MCP 规范化在 `metrics`。
        #   平台刚创建时可能都还没算出来 ⇒ 短退避重试；仍取不到才标 metrics_unavailable。
        body = None
        for attempt in range(4):
            try:
                det = await brain_client.get_alpha_details(aid)
                if isinstance(det, dict):
                    m = det.get("metrics") if isinstance(det.get("metrics"), dict) else (det.get("is") or {})
                    # ★ 就绪判据用sharpe（两个格式都有）；2Y/sub 只在 checks 里，不用来判就绪
                    if isinstance(m, dict) and m.get("sharpe") is not None:
                        body = det
                        break
            except Exception:
                pass
            await asyncio.sleep(4 + attempt * 4)
        return it, aid, None, body


    async def do_submit():
        for fut in [asyncio.create_task(submit(it)) for it in todo]:
            it, aid, err, detail = await fut
            if aid is None:
                print(f"[submit-fail] {err} :: {it.get('note', it['code'])[:40]}", flush=True)
                row = settings_row(it)
                row.update({"id": "DROPPED", "dataset": args.dataset or "", "error": err})
            else:
                if detail is None:
                    #平台回既有 id 且 details 取不到 ⇒ 记录并标警告，不静默丢指标
                    row = settings_row(it)
                    row.update({"id": aid, "dataset": args.dataset or "",
                                "warn_reasons": "metrics_unavailable"})
                else:
                    row = extract(detail, it)
                    row["id"] = aid
                    row["dataset"] = args.dataset or ""
                print(f"  {row['id']}  S={row.get('sharpe')} F={row.get('fitness')} "
                      f"2Y={row.get('two_year_sharpe')} sub={row.get('sub_universe_sharpe')} "
                      f"TO={row.get('turnover_pct')} FAIL={row.get('fail_reasons')} "
                      f"WARN={row.get('warn_reasons')}", flush=True)
            results.append(row)
            save_ckpt(ckpt, results)

    await do_submit()
    save_ckpt(ckpt, results)
    ok = sum(1 for r in results if r.get("id") not in (None, "DROPPED"))
    print(f"[final] rows={len(results)}  成功 {ok}  失败 {len(results) - ok}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tag")
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--dataset", default=None)
    ap.add_argument("--conc", type=int, default=4)
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--no-gate", action="store_true")
    args = ap.parse_args()

    reg = args.region.lower()
    cand_dir = ROOT / "tracking" / args.region / "candidates"
    items_path = cand_dir / f"{reg}_{args.tag}_items.json"
    if not os.path.exists(items_path):
        print(f"[x] 找不到 items: {items_path}")
        near = sorted(cand_dir.glob(f"*{args.tag.split('_')[0]}*.json"))
        if near:
            print(f"    候选: {[c.name for c in near]}")
        return 2
    ckpt = ROOT / "tracking" / args.region / "results" / f"{args.tag}_checkpoint.json"

    items = json.load(open(items_path, encoding="utf-8"))
    print(f"[load] {len(items)} 条 <- {items_path.name}", flush=True)

    if not args.no_gate:
        report = check_expressions_strict([it["code"] for it in items])
        if not report["ok"]:
            print(format_report(report), flush=True)
            print(f"[gate] 硬闸拒绝：{report['total'] - report['passed']} 条，已中止", flush=True)
            return 2
        print(f"[gate] {report['passed']}/{report['total']} PASS", flush=True)

    carried = [] if args.fresh else load_ckpt(ckpt)
    done = {_key(r) for r in carried if r.get("code") and r.get("id") not in (None, "DROPPED")}
    todo = [it for it in items if _key(it) not in done]
    print(f"[resume] 总 {len(items)} 已完成 {len(done)} 待跑 {len(todo)} conc={args.conc}", flush=True)
    if not todo:
        return 0
    return asyncio.run(run(args, items, todo, ckpt, carried))


if __name__ == "__main__":
    raise SystemExit(main())
