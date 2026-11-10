# -*- coding: utf-8 -*-
"""dataset_data_probe.py - 数据集「有没有持仓」探针执行器（coverage 元数据不可信时的唯一答案）。

## 为什么有这只工具

`coverage` 三层都不可信（GBR 2026-11-09 实测）：
- 数据集级：`techindi_model` = 0.0，却有 399 字段、贡献该战役 10 席中的 2 席；
- field 级：177 个集里 109 个集「所有字段 coverage 全 0」；
- 只有「字段目录非空」是真的 —— 但那只证明**字段存在**，不证明**数据有值**。

`audit_dataset_coverage.py` 会把「有字段 + coverage 全 0 + 零回测证据」的集标成
`UNTESTED_BLIND` 并要求探针，本工具就是那个探针的执行器：每个集跑**一条最小仿真**，
读 `is.longCount + is.shortCount`（真实持仓只数）当作「本区有没有数据」的唯一实测答案。

## ★ 探针设计（这里的每个选择都是为了不被误判）

- **`neutralization=NONE` 是刻意的**：`rank()` 输出恒为正，不过中性化 ⇒ `longCount` 直接等于
  「该字段在本区有值的股票数」。若用 SUBINDUSTRY，一个常数型字段会被中性化成 0 持仓，
  从而被误判成「没数据」——那正是本工具要消灭的那类假证据。
- **`ts_backfill(...,250)`**：稀疏/年度字段（多数 other*/event* 集就是这类）在短回填窗口下
  会被判成 NaN。250 交易日 ≈ 一年，足以让「一年至少更新一次」的字段留下痕迹。
- **VECTOR 字段先 `vec_avg`**：否则 FASTEXPR 直接报类型错。
- **一条集一条单发仿真**，不走 multi-sim children：children 语法错会 CANCELLED 整批（本仓已踩 3 次），
  单发互不连坐。
- **fail-closed**：终态里读不到 `longCount/shortCount` ⇒ `data_present = null` +
  `PROBE_FAILED`。**绝不允许**把「没读到」写成「没数据」——那是本工具存在的理由，
  2026-11-09 首版就在这里踩过（`lc=None` 被算成 `data=False`）。

## 用法

    # 1) 按审计产出的探针清单批量探针
    python tools/probe/dataset_data_probe.py --region GBR --universe TOP700 --delay 1 \\
        --plan data/dataset_assets/GBR_probe_plan_d1.json \\
        --out data/dataset_assets/GBR_probe_results_d1.json --jobs 4

    # 2) 只探指定的集
    python tools/probe/dataset_data_probe.py --region GBR --universe TOP700 \\
        --datasets other571,event_relation --out data/dataset_assets/GBR_probe_results_d1.json

    # 3) 回灌给审计门（状态从 UNTESTED_BLIND 变成 TESTED / NO_DATA）
    python tools/gates/audit_dataset_coverage.py --region GBR --universe TOP700 --delay 1 \\
        --reuse-cache data/dataset_assets/GBR_coverage_audit_d1.json \\
        --probe-results data/dataset_assets/GBR_probe_results_d1.json --gate closure

输出 JSON 结构（`results` 以 dataset id 为键，审计门直接吃这一层）：

    {"generated_at": "...", "region": "GBR", "universe": "TOP700", "delay": 1,
     "settings": {...},
     "results": {"other571": {"status": "COMPLETE", "field": "x", "ftype": "MATRIX",
                              "expr": "...", "alpha_id": "...", "long_count": 412,
                              "short_count": 0, "pnl": 1234.5, "sharpe": 0.31,
                              "data_present": true}}}

判据：`data_present = (long_count + short_count) > 0`。**只有探针跑通且持仓为 0 才算「没数据」**；
仿真失败（ERROR / 超时 / 语法错 / 读不到 is 段）只记 `PROBE_FAILED`，不得当成「没数据」。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime


def _find_repo_root() -> str:
    """向上探测 pyproject.toml + src/wqb 双标记（AGENTS.md §8 禁层数硬编码）。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if (os.path.isfile(os.path.join(cur, "pyproject.toml"))
                and os.path.isdir(os.path.join(cur, "src", "wqb"))):
            return cur
        cur = os.path.dirname(cur)
    raise SystemExit("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


REPO_ROOT = _find_repo_root()
for _extra in (os.path.join(REPO_ROOT, "src"),
               os.path.join(REPO_ROOT, "tools", "lib"),
               os.path.join(REPO_ROOT, "tools"),
               os.path.join(REPO_ROOT, "world-quant-brain-mcp")):
    if os.path.isdir(_extra) and _extra not in sys.path:
        sys.path.insert(0, _extra)

# 网络工具统一在 MCP venv 下跑（tools/README.md 约定）；缺 venv 时原地继续
try:                                                               # pragma: no cover
    import _pyenv
    _pyenv.reexec_under_venv()
except Exception:                                                  # noqa: BLE001
    pass

from brain_api import BrainApiClient, SimulationData, SimulationSettings  # noqa: E402

USABLE_TYPES = {"MATRIX", "VECTOR"}


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ----------------------------------------------------------------------------- fields
async def pick_field(client, region, universe, delay, dataset):
    """挑一个可仿真字段：只用 MATRIX/VECTOR，按 alphaCount→coverage 降序（最可能是主信号）。

    `get_datafields` 自己按 dataset.id 分页拉全量且 all-or-error（MCP 侧契约），
    所以这里**不要**再传 limit/offset（实测 TypeError: unexpected keyword）。
    """
    try:
        resp = await client.get_datafields(
            region=region, universe=universe, delay=delay,
            dataset_id=dataset, filter_sharpe=False,
        )
    except Exception as e:                                         # noqa: BLE001
        return None, 0, "%s: %s" % (type(e).__name__, e)
    items = (resp or {}).get("results") or []
    usable = [f for f in items
              if str(f.get("type") or "").upper() in USABLE_TYPES and f.get("id")]
    if not usable:
        return None, len(items), "no MATRIX/VECTOR field in first %d rows" % len(items)
    usable.sort(key=lambda f: (-(f.get("alphaCount") or 0), -(f.get("coverage") or 0)))
    return usable[0], len(items), None


def build_expr(field_id, ftype, backfill):
    if str(ftype or "").upper() == "VECTOR":
        return "rank(ts_backfill(vec_avg(%s),%d))" % (field_id, backfill)
    return "rank(ts_backfill(%s,%d))" % (field_id, backfill)


# ----------------------------------------------------------------------------- sim
async def probe_one(client, dataset, args):
    field, n_seen, err = await pick_field(client, args.region, args.universe, args.delay,
                                          dataset)
    if field is None:
        return {"dataset": dataset, "status": "PROBE_FAILED", "stage": "pick_field",
                "data_present": None, "error": err, "fields_seen": n_seen}
    expr = build_expr(field["id"], field.get("type"), args.backfill)
    settings = SimulationSettings(
        region=args.region, universe=args.universe, delay=args.delay,
        decay=args.decay, neutralization=args.neutralization,
        truncation=args.truncation, nanHandling="OFF", visualization=False,
    )
    rec = {"dataset": dataset, "datasource_fields_seen": n_seen,
           "field": field["id"], "ftype": field.get("type"), "expr": expr,
           "field_alpha_count": field.get("alphaCount"),
           "field_coverage": field.get("coverage")}
    try:
        alpha = await client.create_simulation(
            SimulationData(type="REGULAR", settings=settings, regular=expr))
    except Exception as e:                                         # noqa: BLE001
        rec.update({"status": "PROBE_FAILED", "stage": "simulate", "data_present": None,
                    "error": "%s: %s" % (type(e).__name__, e)})
        return rec
    if not isinstance(alpha, dict) or not alpha.get("id"):
        rec.update({"status": "PROBE_FAILED", "stage": "simulate", "data_present": None,
                    "error": ("sim returned no alpha id: %s" % str(alpha)[:300])})
        return rec

    is_ = alpha.get("is") or {}
    rec.update({
        "alpha_id": alpha.get("id"),
        "sim_status": alpha.get("status"),
        "long_count": is_.get("longCount"),
        "short_count": is_.get("shortCount"),
        "pnl": is_.get("pnl"),
        "sharpe": is_.get("sharpe"),
        "fitness": is_.get("fitness"),
        "turnover": is_.get("turnover"),
        "is_keys": sorted(is_.keys())[:40],
    })
    lc, sc = rec["long_count"], rec["short_count"]
    if lc is None and sc is None:
        # ★ fail-closed：读不到持仓 ≠ 没有持仓
        rec.update({"status": "PROBE_FAILED", "stage": "metrics", "data_present": None,
                    "error": "terminal payload has no longCount/shortCount (is_keys=%s)"
                             % ",".join(rec["is_keys"][:12])})
        return rec
    rec["data_present"] = bool((lc or 0) + (sc or 0) > 0)
    rec["status"] = str(alpha.get("status") or "COMPLETE").upper()
    return rec


def _result(out, args):
    """把逐集记录打包成落盘 JSON（增量写与终态写共用同一形状）。"""
    counts = {}
    for v in out.values():
        counts[v.get("status")] = counts.get(v.get("status"), 0) + 1
    counts["data_present_true"] = sum(1 for v in out.values() if v.get("data_present"))
    counts["data_present_false"] = sum(1 for v in out.values()
                                       if v.get("data_present") is False)
    counts["data_present_null"] = sum(1 for v in out.values()
                                      if v.get("data_present") is None)
    return {
        "generated_at": _now(),
        "region": args.region, "universe": args.universe, "delay": args.delay,
        "settings": {"decay": args.decay, "neutralization": args.neutralization,
                     "truncation": args.truncation, "backfill": args.backfill},
        "criterion": "data_present = (longCount + shortCount) > 0；"
                     "读不到读数或仿真失败 => PROBE_FAILED(data_present=null)，不算没数据",
        "counts": counts,
        "results": out,
    }


async def run_async(args):
    client = BrainApiClient()
    await client.ensure_authenticated()

    targets = []
    if args.datasets:
        targets = [d.strip() for d in args.datasets.split(",") if d.strip()]
    elif args.plan:
        plan = json.load(open(args.plan, encoding="utf-8"))
        rows = plan.get("probe_needed") or plan.get("results") or []
        targets = [r.get("dataset") for r in rows if r.get("dataset")]
    if not targets:
        print(json.dumps({"ok": False, "error": "no --datasets / --plan targets"},
                         ensure_ascii=False))
        return 2

    done = {}
    if args.reuse_out and args.out and os.path.isfile(args.out):
        try:
            prev = json.load(open(args.out, encoding="utf-8"))
            done = {k: v for k, v in (prev.get("results") or {}).items()
                    if v.get("data_present") is not None}
        except Exception:                                          # noqa: BLE001
            done = {}
    todo = [d for d in targets if d not in done]

    sem = asyncio.Semaphore(max(1, args.jobs))
    out = dict(done)

    def dump():
        """★ 逐条落盘：16 集探针是小时级任务，只在全部结束后写盘等于「一次崩溃全丢」。"""
        if not args.out:
            return
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(_result(out, args), f, ensure_ascii=False, indent=1)

    async def worker(ds):
        async with sem:
            rec = await probe_one(client, ds, args)
        out[ds] = rec
        print("[probe] %-26s %-13s lc=%s sc=%s data=%s %s" % (
            ds, rec.get("status"), rec.get("long_count"), rec.get("short_count"),
            rec.get("data_present"), (rec.get("error") or "")[:70]), flush=True)
        dump()

    if todo:
        await asyncio.gather(*(worker(d) for d in todo))

    res = _result(out, args)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
    print(json.dumps({"ok": True, "counts": res["counts"], "out": args.out},
                     ensure_ascii=False, indent=1))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="dataset data-presence probe (longCount)")
    ap.add_argument("--region", required=True)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--plan", default=None, help="audit --probe-plan 产物")
    ap.add_argument("--datasets", default=None, help="逗号分隔，覆盖 --plan")
    ap.add_argument("--out", default=None, help="结果 JSON（供 audit --probe-results 消费）")
    ap.add_argument("--reuse-out", action="store_true", help="复用 out 里已有读数的条目")
    ap.add_argument("--jobs", type=int, default=4, help="并发的单发仿真数")
    ap.add_argument("--backfill", type=int, default=250)
    ap.add_argument("--decay", type=float, default=0.0)
    ap.add_argument("--neutralization", default="NONE",
                    help="★ 探针刻意用 NONE：rank 全正，longCount 直接等于有数据的股票数")
    ap.add_argument("--truncation", type=float, default=0.01)
    args = ap.parse_args(argv)
    return asyncio.run(run_async(args))


if __name__ == "__main__":
    sys.exit(main())
