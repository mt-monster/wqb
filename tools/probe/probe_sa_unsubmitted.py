#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_sa_unsubmitted.py — 对 SA 探针列出的「未提交候选」逐颗取真实双闸（SELF+PROD）。

目的（呼应整合报告 §6 澄清）：
  SA 探针 `probe_sa_candidates.py` 不取 SA 的 prod/self（JSON 里全是 None）。
  「UNSUBMITTED(已建未提交)」≠「待提交(已验证可交)」。本脚本逐颗用平台
  `check_self_correlation` + `check_correlation(production)` 取真实值，
  判定是否双双 < 0.7（平台提交闸），算出真正可进「待提交」清单的颗数。

★ 处理范围铁律（2026-10-05 用户定，勿回退）
  **只处理「增量数据」与「没有 prod 值但业绩已明确记录的对象」**：
    1) 增量：自上次持久化以来**新出现**的候选（缓存里没有的 alpha_id）；
    2) 无 prod 但业绩已记录：缓存里 `prod_max` 为 None，
       且源数据里 IS sharpe/fitness 均非 None（业绩明确）的对象。
  已经有实测 prod 值的条目**不重复消耗平台单并发队列**，
  直接复用缓存并在报告里标 `source=cache`。
  ⇒ 结果持久化在 `results/sa_unsubmitted_probe_cache.json`，每颗落盘，可断点续跑。

★ 关于 --refresh
  全量验证结果已持久化，日常**不再执行全量 `--refresh`**（翻平台 ~14min 且占队列）。
  仅在候选集合真正变化（新建/提交 SA）后按增量跑即可；确需重扫才用 `--all`。

纯读取（GET），不涉及任何 submit / POST；遵守「只盘点不提交」铁律。
复用 super_build.py cmd_probe 的同两套调用。

用法:
  python tools/probe/probe_sa_unsubmitted.py                  # 增量（默认）
  python tools/probe/probe_sa_unsubmitted.py --all            # 强制全量重扫（慎用）
  python tools/probe/probe_sa_unsubmitted.py --id LLZnG5ZM    # 单颗（忽略缓存）
  python tools/probe/probe_sa_unsubmitted.py --src results/sa_candidates_20261005-214003.json
退出码: 0=正常  3=平台/鉴权失败
"""
import argparse
import asyncio
import glob
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # 同主题目录的兄弟脚本
sys.path.insert(0, os.path.dirname(_HERE))       # tools/（_pyenv 在此；2026-10-06 下沉到主题目录后必需）
import _pyenv  # noqa: E402

REPO = _pyenv.REPO_ROOT
RESULTS_DIR = REPO / "results"
GATE = 0.7
# ★ 持久化主缓存：全量验证结果存放处，日常只读它 + 增量补测
CACHE_PATH = RESULTS_DIR / "sa_unsubmitted_probe_cache.json"


def _latest_sa_json():
    files = sorted(glob.glob(str(RESULTS_DIR / "sa_candidates_*.json")))
    return files[-1] if files else None


def _load_ids(src):
    if src:
        path = src
    else:
        path = _latest_sa_json()
    if not path or not os.path.exists(path):
        print(f"[ERROR] 找不到 SA 探针 JSON（src={src}）", file=sys.stderr)
        sys.exit(3)
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    cands = [a for a in (d.get("super_alphas", {}).get("unsubmitted_candidates") or [])
             if isinstance(a, dict)]
    return path, cands


def _load_cache():
    if not CACHE_PATH.exists():
        return {"updated_at": None, "items": {}}
    try:
        d = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        if not isinstance(d.get("items"), dict):
            d["items"] = {}
        return d
    except Exception:  # noqa: BLE001
        return {"updated_at": None, "items": {}}


def _save_cache(cache):
    """原子写，防中断损坏（每颗探完即落盘，保证断点续跑）。"""
    cache["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CACHE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, CACHE_PATH)


def _perf_recorded(c):
    """业绩是否已明确记录（IS sharpe/fitness 均非 None）。"""
    return (c is not None
            and c.get("sharpe") is not None
            and c.get("fitness") is not None)


def _needs_probe(aid, cand, cache, force_all=False):
    """返回 (是否需探, 原因)。

    铁律：只处理 ①增量（缓存无此 id） ②无 prod 值但业绩已明确记录。
    """
    if force_all:
        return True, "force-all"
    ent = (cache.get("items") or {}).get(aid)
    if ent is None:
        return True, "incremental(新候选)"
    if ent.get("prod_max") is None and _perf_recorded(cand):
        return True, "prod缺失且业绩已记录"
    if ent.get("prod_max") is None and ent.get("error"):
        return True, "上次出错重试"
    return False, "cached"


async def _probe_one(brain, c):
    aid = c.get("id")
    out = {
        "alpha_id": aid,
        "region": c.get("region"),
        "is_sharpe": c.get("sharpe"),
        "is_fitness": c.get("fitness"),
        "name": c.get("name"),
        "self_max": None,
        "self_pass": None,
        "prod_checks": {},
        "prod_max": None,
        "prod_pass": None,
        "passes_both": None,
        "error": None,
        "probed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    try:
        selfr = await brain.check_self_correlation(aid, correlation_type="self")
        out["self_max"] = selfr.get("max_correlation")
        out["self_pass"] = selfr.get("passes_check")
    except Exception as e:
        out["error"] = f"self: {str(e)[:160]}"
    try:
        prodr = await brain.check_correlation(aid, correlation_type="production")
        checks = prodr.get("checks") or {}
        pmax = None
        ppass = True
        for name, cc in checks.items():
            m = cc.get("max_correlation")
            p = cc.get("passes_check")
            out["prod_checks"][name] = {"max": m, "pass": p}
            if m is not None:
                pmax = m if pmax is None else max(pmax, m)
            if p is False:
                ppass = False
        out["prod_max"] = pmax
        out["prod_pass"] = ppass
    except Exception as e:
        out["error"] = (out["error"] or "") + f" | prod: {str(e)[:160]}"
        out["prod_pass"] = False
    s_ok = (out["self_max"] is not None and float(out["self_max"]) < GATE)
    p_ok = (out["prod_max"] is not None and out["prod_pass"] is True
            and float(out["prod_max"]) < GATE)
    out["passes_both"] = bool(s_ok and p_ok)
    return out


async def run(todo, by_id, cache):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    total = len(todo)
    for i, (aid, why) in enumerate(todo, 1):
        c = by_id.get(aid, {"id": aid})
        print(f"[{i:2}/{total}] probe {aid} ({c.get('region')}) [{why}] ...", flush=True)
        r = await _probe_one(brain, c)
        r["source"] = "fresh"
        cache["items"][aid] = r
        _save_cache(cache)  # ★ 每颗落盘，中断可续
        verdict = "PASS(待提交)" if r["passes_both"] else "BLOCKED"
        print(f"      SELF={r['self_max']} PROD={r['prod_max']} -> {verdict}"
              + (f"  err={r['error']}" if r["error"] else ""), flush=True)
        await asyncio.sleep(0.5)
    return cache


def main():
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=None, help="指定 sa_candidates_*.json 源（默认取最新）")
    ap.add_argument("--id", action="append", default=None,
                    help="只探指定 alpha_id（可多次，忽略缓存）；缺省按增量规则处理全部未提交候选")
    ap.add_argument("--all", action="store_true",
                    help="★ 强制全量重扫（日常禁用：占平台单并发队列 ~14min+）")
    args = ap.parse_args()

    src, cands = _load_ids(args.src)
    by_id = {c.get("id"): c for c in cands if c.get("id")}
    if args.id:
        for aid in args.id:
            by_id.setdefault(aid.strip(), {"id": aid.strip()})
    if not by_id:
        print("[ERROR] 无候选可探", file=sys.stderr)
        sys.exit(3)

    cache = _load_cache()
    if args.id:
        todo = [(x.strip(), "--id 指定") for x in args.id if x.strip()]
    else:
        todo = []
        for aid, c in by_id.items():
            need, why = _needs_probe(aid, c, cache, force_all=args.all)
            if need:
                todo.append((aid, why))

    print(f"源: {src}")
    print(f"候选 {len(by_id)} 颗 | 缓存已存 {len(cache.get('items') or {})} 颗 "
          f"(更新于 {cache.get('updated_at')})")
    print(f"本次待探（增量/无prod且业绩已记录）：{len(todo)} 颗")
    if not todo:
        print("  → 无新增、无 prod 缺口，跳过平台调用（不占队列）。")
        print("    如需强制重扫加 --all；确要提交前请对目标颗单独 --id 复测 prod。")
    else:
        print("=" * 74)
        try:
            cache = asyncio.run(run(todo, by_id, cache))
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            _save_cache(cache)  # 中断也保住已探到的
            sys.exit(3)

    # 汇总：缓存全量（含本次命中与历史）
    items = cache.get("items") or {}
    results = []
    for aid, c in by_id.items():
        ent = items.get(aid)
        if ent:
            r = dict(ent)
            r["source"] = "fresh" if any(aid == t[0] for t in todo) else "cache"
        else:
            r = {"alpha_id": aid, "region": c.get("region"), "source": "unprobed",
                 "prod_max": None, "self_max": None, "passes_both": None}
        results.append(r)

    n_pass = sum(1 for r in results if r.get("passes_both"))
    n_block = sum(1 for r in results if r.get("passes_both") is False)
    n_unknown = sum(1 for r in results if r.get("passes_both") is None)
    n_err = sum(1 for r in results if r.get("error"))
    print("\n" + "=" * 74)
    print(f"汇总（缓存全量 {len(results)} 颗）："
          f"PASS(双闸<{GATE}) = {n_pass} | BLOCKED = {n_block} | "
          f"未测 = {n_unknown} | 出错 = {n_err}")
    print("注意：PASS 仅表示平台双闸过；提交仍须用户逐次明示 + SUPER 配额 1/天/区。")
    print("★ >48h 的 prod 视为不可信：正式提交前须对目标颗 `--id` 单独复测。")

    out = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": src,
        "gate": GATE,
        "mode": "all" if args.all else "incremental",
        "probed_this_run": len(todo),
        "total": len(results),
        "pass_count": n_pass,
        "blocked_count": n_block,
        "unknown_count": n_unknown,
        "error_count": n_err,
        "results": results,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = RESULTS_DIR / f"sa_unsubmitted_probe_{stamp}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n报告已写：{path}")
    print(f"持久化缓存：{CACHE_PATH}")


if __name__ == "__main__":
    main()
