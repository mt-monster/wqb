# -*- coding: utf-8 -*-
"""把 prod 探测产物（peek / 带锁实测）落进权威缓存 ``alpha_corr_cache``。

2026-11-10 审查 P0-1 的修复：此前 ``results/prod_peek_<id>.json`` /
``results/prod_wait_<id>.json`` **全仓没有任何读取方**，「免查 prod 提交」靠一次手工
SQL 把值塞进权威表；正规写入口又用「写库时刻」而非平台测量时刻，于是一个几天前算出的
值今天写库就被当成「48h 内新鲜实测」，直接过 0.7 闸。

本工具是那条手工步骤的唯一替代：
  * 以产物里的 ``at``（**探测时刻**）作为 ``checked_at``，保鲜判据据此成立；
  * ``source`` 统一登记为 ``prod_peek``（``wqb.store.CORR_SOURCES``）；
  * 值域 / 时间戳 / alpha_id 三重校验，任一不过即拒绝落库；
  * 走 ``CampaignStore.set_corr_cache``（联动 ``alphas`` 镜像），不再裸 SQL。

用法：
    python tools/prod_peek_ingest.py GrW9OxmG                 # 单颗
    python tools/prod_peek_ingest.py AAA111 BBB222 --dry-run  # 批量预演
    python tools/prod_peek_ingest.py --dir results --all      # 目录下全部产物

退出码：0 全部成功（或 dry-run）；1 有任一失败。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from wqb.store import CampaignStore, corr_age_hours  # noqa: E402
from wqb.store._corr_cache import CORR_FRESH_HOURS  # noqa: E402

PEEK_SOURCE = "prod_peek"


def _candidate_paths(alpha_id: str, directory: str) -> List[str]:
    return [
        os.path.join(directory, f"prod_peek_{alpha_id}.json"),
        os.path.join(directory, f"prod_wait_{alpha_id}.json"),
    ]


def load_payload(alpha_id: str, directory: str) -> Optional[Dict[str, Any]]:
    """优先读 peek 产物，其次带锁产物；都不存在返回 None。"""
    for p in _candidate_paths(alpha_id, directory):
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    data = json.load(f)
            except (OSError, ValueError):
                continue
            if isinstance(data, dict):
                data["_path"] = p
                return data
    return None


def validate(payload: Dict[str, Any], alpha_id: str) -> Dict[str, Any]:
    """三重校验：alpha_id 一致 / prod ∈ [0,1] / at 可解析。返回 {ok, reason, ...}。"""
    out: Dict[str, Any] = {"ok": False, "alpha_id": alpha_id}
    if not isinstance(payload, dict):
        out["reason"] = "产物不是 JSON 对象"
        return out
    if payload.get("alpha_id") and str(payload["alpha_id"]) != alpha_id:
        out["reason"] = f"产物 alpha_id={payload['alpha_id']!r} 与请求 {alpha_id!r} 不一致"
        return out
    raw = payload.get("prod", payload.get("max"))
    try:
        val = float(raw)
    except (TypeError, ValueError):
        out["reason"] = f"prod 非数值：{raw!r}"
        return out
    if not (0.0 <= val <= 1.0):
        out["reason"] = f"prod 越界 [0,1]：{val}"
        return out
    at = payload.get("at") or payload.get("checked_at")
    age = corr_age_hours(at) if at else None
    if age is None:
        out["reason"] = f"缺少可解析的测量时刻 at={at!r}（拒绝用写库时刻冒充）"
        return out
    out.update({"ok": True, "prod": val, "checked_at": at, "age_hours": age,
                "stale": age > CORR_FRESH_HOURS,
                "histogram": payload.get("histogram") or payload.get("records")})
    return out


def ingest_one(store, alpha_id: str, directory: str, *, dry_run: bool = False) -> Dict[str, Any]:
    payload = load_payload(alpha_id, directory)
    if payload is None:
        return {"alpha_id": alpha_id, "ok": False,
                "reason": f"未找到产物（{directory}/prod_peek_{alpha_id}.json 或 prod_wait_*）"}
    chk = validate(payload, alpha_id)
    if not chk["ok"]:
        return {"alpha_id": alpha_id, "ok": False, "reason": chk["reason"],
                "path": payload.get("_path")}
    res = {"alpha_id": alpha_id, "ok": True, "prod": chk["prod"],
           "checked_at": chk["checked_at"], "age_hours": chk["age_hours"],
           "stale": chk["stale"], "source": PEEK_SOURCE, "path": payload.get("_path")}
    if chk["stale"]:
        res["warning"] = (f"测量时刻距今 {chk['age_hours']}h > {CORR_FRESH_HOURS}h，"
                          "落库后读侧会判 stale（只可排序参考，不可判闸）")
    if dry_run:
        res["dry_run"] = True
        return res
    wrote = store.set_corr_cache(
        alpha_id, prod=chk["prod"], records=chk.get("histogram"),
        source=PEEK_SOURCE, checked_at=chk["checked_at"])
    res["store"] = wrote
    if wrote.get("skipped"):
        res["ok"] = False
        res["reason"] = f"set_corr_cache 跳过：{wrote['skipped']}"
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("alphas", nargs="*", help="alpha id（可多个）")
    ap.add_argument("--dir", default=os.path.join(ROOT, "results"), help="产物目录")
    ap.add_argument("--all", action="store_true", help="处理目录下全部 prod_peek_*/prod_wait_* 产物")
    ap.add_argument("--dry-run", action="store_true", help="只校验与预演，不写库")
    ap.add_argument("--db", default=None, help="数据库路径（缺省走 CampaignStore 默认）")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    args = ap.parse_args(argv)

    ids: List[str] = list(args.alphas)
    if args.all:
        seen = set()
        for pat in ("prod_peek_*.json", "prod_wait_*.json"):
            for p in sorted(glob.glob(os.path.join(args.dir, pat))):
                base = os.path.basename(p)
                aid = base[len("prod_peek_"):-len(".json")] if base.startswith("prod_peek_") \
                    else base[len("prod_wait_"):-len(".json")]
                if aid and aid not in seen:
                    seen.add(aid)
                    ids.append(aid)
    if not ids:
        ap.error("至少给一个 alpha id，或用 --all")

    store = CampaignStore(args.db) if args.db else CampaignStore()
    results = []
    try:
        for aid in ids:
            results.append(ingest_one(store, aid, args.dir, dry_run=args.dry_run))
    finally:
        store.close()

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for r in results:
            if r["ok"]:
                tag = "DRY" if r.get("dry_run") else "OK "
                extra = f" ⚠ {r['warning']}" if r.get("warning") else ""
                print(f"[{tag}] {r['alpha_id']} prod={r['prod']} at={r['checked_at']} "
                      f"age={r['age_hours']}h source={r['source']}{extra}")
            else:
                print(f"[FAIL] {r['alpha_id']} {r.get('reason')}")
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
