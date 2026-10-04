# -*- coding: utf-8 -*-
"""`$WQ_PY -m wqb.profiles <子命令>` —— 区域 × 类别控制层的命令行（2026-10-04）。

  explain     --region R [--category C | --dataset D] [--json]   生效画像（每个值带来源）
  check       [--region R ...]                                    校验 cells.json / 类别卡 / 渲染是否最新
  sync-cells  --region R [--apply] [--min-backtests N]            只读汇总库里证据 → 写 cells.json 的 evidence 块
  render      [--region R ...] [--apply]                          重渲区域 skill 与组合分支文件（缺省只列出差异）
  audit       {sources,dead-keys,literals,modeb,split,matrix} [--region R ...] [--json]

只有 sync-cells --apply / render --apply 会写**文件**；任何子命令都不写数据库、不发平台请求。
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional


def _regions(a) -> Optional[List[str]]:
    return [r.upper() for r in a.region] if getattr(a, "region", None) else None


def cmd_explain(a) -> int:
    from .resolver import explain_text, resolve
    p = resolve(a.region, category=a.category, dataset=a.dataset)
    if a.json:
        print(json.dumps(p, ensure_ascii=False, indent=1, default=str))
    else:
        print(explain_text(p))
    return 0


def cmd_check(a) -> int:
    from wqb.config import REGIONS
    from .cards import load_cards, validate_cards
    from .render import check as render_check
    from .resolver import check_region
    problems: List[str] = [f"类别卡：{e}" for e in validate_cards(load_cards())]
    regions = _regions(a) or sorted(REGIONS)
    for r in regions:
        problems += [f"{r} cells.json：{e}" for e in check_region(r)]
    problems += render_check(regions)
    for p in problems:
        print(p)
    print(f"[check] {len(problems)} 个问题（{', '.join(regions)}）")
    return 1 if problems else 0


def cmd_sync(a) -> int:
    from .evidence import sync_cells
    s = sync_cells(a.region, apply=a.apply, min_backtests=a.min_backtests)
    data = s.pop("data")
    for cat in s["cells"]:
        ev = (data["cells"][cat].get("evidence") or {})
        print(f"  {cat:<14} 回测 {ev.get('backtests', 0):>5}  RA 全过 {ev.get('ra_clean', 0):>4}  "
              f"判死 {len(ev.get('dead_ends') or []):>3}  胜绩 {len(ev.get('wins') or []):>3}"
              f"{'  ← 新建组合' if cat in s['added'] else ''}")
    print(f"[sync-cells] {a.region.upper()}：{len(s['cells'])} 个组合（新建 {len(s['added'])}）；"
          f"无法归类的判死 / 胜绩 {s['unbound_registry_entries']} 条；没写数据集的回测行 {s['unattributed_backtests']} 条；"
          + (f"已写 {s['path']}" if s["applied"] else "干跑（加 --apply 写 cells.json）"))
    return 0


def cmd_render(a) -> int:
    from .render import apply, plan
    items = plan(_regions(a))
    changed = [(p, old, new) for p, old, new in items if old != new]
    for p, old, _ in changed:
        print(f"  {'新建' if old is None else '更新'} {p}")
    if a.apply:
        apply(items)
        print(f"[render] 写了 {len(changed)} 个文件")
    else:
        print(f"[render] {len(changed)} 个文件需要更新（加 --apply 写入）")
    return 0


def cmd_audit(a) -> int:
    from . import audit
    if a.what == "sources":
        rows = audit.param_sources(_regions(a))
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            for r in rows:
                flag = []
                if r["neutralization_conflict"]:
                    flag.append("中性化矛盾")
                if r["universe_conflict"]:
                    flag.append("universe 矛盾")
                if r["db_universe_legal_drift"]:
                    flag.append(f"regions 表档位漂移 {r['db_universe_legal_drift']}")
                print(f"{r['region']}: {'；'.join(flag) or '一致'}\n   中性化 {r['neutralization']}\n   universe {r['universe']}")
    elif a.what == "dead-keys":
        keys = audit.unread_threshold_keys()
        print("\n".join(keys) if not a.json else json.dumps(keys, ensure_ascii=False, indent=1))
        print(f"[dead-keys] {len(keys)} 个阈值键找不到读取方（粗口径）")
    elif a.what == "literals":
        hits = audit.region_literal_branches()
        print("\n".join(hits) if not a.json else json.dumps(hits, ensure_ascii=False, indent=1))
        print(f"[literals] {len(hits)} 处区域字面量分支 / 查表")
    elif a.what == "modeb":
        from wqb.config import REGIONS
        from wqb.workflow.mode_b_config import load_mode_b_config
        from .resolver import _ReadonlyLedger
        for r in _regions(a) or sorted(REGIONS):
            cfg = load_mode_b_config(_ReadonlyLedger(), region=r)
            mg = cfg["main_gate"]
            print(f"{r}: sharpe {mg['sharpe_min']} / fitness {mg['fitness_min']}  [{cfg['_source']}]"
                  + (f"  钳掉 {cfg['_clamped_from']}" if cfg.get("_clamped_from") else ""))
    elif a.what == "split":
        from wqb.config import REGIONS
        rows = [row for r in (_regions(a) or sorted(REGIONS)) for row in audit.split_ratio(r)]
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        for row in rows:
            if not a.json:
                print(f"{row['region']}×{row['category']:<14} S2 {row['s2_ratio']:.0%}  S4 {row['s4_ratio']:.0%}  "
                      f"证据线 {'✓' if row['evidence_ok'] else '×'}  控制流 {'✓' if row['control_flow'] else '×'}  "
                      f"{row['entry_verdict']}  {'→ 够格拆成独立 skill' if row['split_eligible'] else ''}")
        print(f"[split] 够格拆分的组合：{sum(1 for r in rows if r['split_eligible'])} / {len(rows)}")
    elif a.what == "matrix":
        from .evidence import matrix
        rows = matrix(_regions(a))
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=1))
        else:
            for row in sorted(rows, key=lambda x: -x["backtests"]):
                print(f"{row['region']}×{row['category']:<14} 回测 {row['backtests']:>5} RA 全过 {row['ra_clean']:>4} "
                      f"prod 低于上限 {row['prod_clean']:>3} 判死 {row['dead']:>3} 胜绩 {row['win']:>2}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m wqb.profiles", description="区域 × 类别控制层（只读，除 --apply 写文件）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("explain", help="生效画像（每个值带来源）")
    p.add_argument("--region", required=True)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--category")
    g.add_argument("--dataset")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_explain)
    p = sub.add_parser("check", help="校验组合文件 / 类别卡 / 渲染是否最新")
    p.add_argument("--region", action="append")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("sync-cells", help="只读汇总证据写进 cells.json 的 evidence 块")
    p.add_argument("--region", required=True)
    p.add_argument("--apply", action="store_true")
    p.add_argument("--min-backtests", type=int, default=20)
    p.set_defaults(fn=cmd_sync)
    p = sub.add_parser("render", help="重渲区域 skill 与组合分支文件")
    p.add_argument("--region", action="append")
    p.add_argument("--apply", action="store_true")
    p.set_defaults(fn=cmd_render)
    p = sub.add_parser("audit", help="只读审计")
    p.add_argument("what", choices=["sources", "dead-keys", "literals", "modeb", "split", "matrix"])
    p.add_argument("--region", action="append")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_audit)
    return ap


def main(argv: Optional[List[str]] = None) -> int:
    a = build_parser().parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass
    if getattr(a, "region", None) and isinstance(a.region, str):
        a.region = a.region.upper()
    return int(a.fn(a) or 0)


if __name__ == "__main__":
    sys.exit(main())
