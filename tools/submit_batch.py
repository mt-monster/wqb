# -*- coding: utf-8 -*-
"""submit_batch.py - 通用 alpha 批量提交，取代 tools/_submit_*.py（共 31 个同构一次性脚本）。

所有被取代脚本的共同结构：
  MCP_DIR + chdir + BrainApiClient + BASE(USA/TOP3000/EQUITY/2014-2023)
  + load(expr 文件) + 组装 payload(type=REGULAR, settings=dict(BASE, decay, neutralization))
  + POST {base_url}/simulations + 打印 Location

用法:
  # 单批次（绝大多数 _submit_* 同构场景）
  python submit_batch.py --path tracking/USA/runs/xxx_batch.txt --decay 4 --neutralization SUBINDUSTRY

  # 多批次（逐批不同 decay / universe，对应 _submit_inst6_t12 / _submit_inst6_z）
  python submit_batch.py --spec spec.json
  # spec.json 例: [{"path":"a.txt","decay":1,"universe":"TOP3000"},
  #                {"path":"b.txt","decay":2,"universe":"TOP1000"}]

  # 试跑（不触网，仅打印将提交的 payload）
  python submit_batch.py --path x.txt --decay 4 --neutralization SUBINDUSTRY --dry-run

可选覆盖 BASE 任意字段: --region/--universe/--delay/--start/--end/--type/--truncation。
"""
import argparse
import asyncio
import json
import os
import sys
import time

MCP_DIR = os.environ.get("WQ_MCP_DIR", r"d:\coding\traeCN_project\wqb\world-quant-brain-mcp")

BASE = {
    "instrumentType": "EQUITY", "region": "USA", "universe": "TOP3000",
    "delay": 1, "truncation": 0.0, "pasteurization": "ON",
    "unitHandling": "VERIFY", "nanHandling": "OFF", "maxTrade": "ON",
    "maxPosition": "OFF", "language": "FASTEXPR", "visualization": False,
    "startDate": "2014-01-01", "endDate": "2023-12-31",
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip() and not l.startswith("#")]


def build_payload(exprs, decay, neutralization, atype, overrides):
    settings = dict(BASE, decay=decay, neutralization=neutralization)
    # type 只在 payload 顶层，不进 settings
    settings.update({k: v for k, v in overrides.items() if k != "type"})
    return [{"type": atype, "settings": settings, "regular": e} for e in exprs]


def batches_from_args(args):
    """返回 list of (tag, path, decay, neutralization, overrides)。"""
    overrides = {}
    for k, v in [
        ("region", args.region), ("universe", args.universe), ("delay", args.delay),
        ("startDate", args.start), ("endDate", args.end), ("truncation", args.truncation),
        ("type", args.type if args.type else None),
    ]:
        if v is not None:
            overrides[k] = v
    n = args.neutralization or "SUBINDUSTRY"
    t = args.type or "REGULAR"
    return [(os.path.basename(p), p, args.decay, n, dict(overrides)) for p in args.path]


async def run(batches, sleep, dry_run):
    for tag, path, decay, neut, overrides in batches:
        exprs = load(path)
        payload = build_payload(exprs, decay, neut, overrides.get("type", "REGULAR"), overrides)
        print(f"[{tag}] n={len(payload)} decay={decay} neut={neut} "
              f"type={overrides.get('type','REGULAR')} overrides={overrides}")
        if dry_run:
            print("  DRY-RUN sample:", payload[0] if payload else None)
            continue
        os.chdir(MCP_DIR)
        from brain_api import BrainApiClient  # noqa: E402
        client = BrainApiClient()
        await client.ensure_authenticated()
        resp = await client._request("POST", f"{client.base_url}/simulations", json=payload)
        loc = resp.headers.get("Location", "")
        print(f"  status={resp.status_code} -> {loc}")
        if resp.status_code != 201:
            print("  BODY:", resp.text[:500])
        time.sleep(sleep)
    print("ALL SUBMITTED" if not dry_run else "DRY-RUN DONE")


def main():
    ap = argparse.ArgumentParser(description="通用 alpha 批量提交（取代 _submit_*.py）")
    ap.add_argument("--path", nargs="+", help="表达式文件路径（可多个，使用相同 decay/neut）")
    ap.add_argument("--decay", type=int, help="decay 值")
    ap.add_argument("--neutralization", default="SUBINDUSTRY")
    ap.add_argument("--type", default="REGULAR")
    ap.add_argument("--spec", help="多批次 JSON 规格文件（list of {path,decay,neutralization?,universe?,type?}）")
    # BASE 覆盖
    ap.add_argument("--region")
    ap.add_argument("--universe")
    ap.add_argument("--delay", type=int)
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--truncation", type=float)
    ap.add_argument("--sleep", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.spec:
        spec = json.load(open(args.spec, encoding="utf-8"))
        batches = []
        for b in spec:
            ov = {}
            for k in ("region", "universe", "delay", "startDate", "endDate", "type"):
                if k in b and b[k] is not None:
                    ov[k] = b[k]
            batches.append((os.path.basename(b["path"]), b["path"],
                            b.get("decay", args.decay), b.get("neutralization", "SUBINDUSTRY"), ov))
    elif args.path and args.decay is not None:
        batches = batches_from_args(args)
    else:
        ap.error("需提供 --spec，或同时提供 --path 与 --decay")
    asyncio.run(run(batches, args.sleep, args.dry_run))


if __name__ == "__main__":
    main()
