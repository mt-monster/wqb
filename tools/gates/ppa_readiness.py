# -*- coding: utf-8 -*-
r"""CPPAP 就绪度判据（只读，离线快照优先）。

把「提高 Combined Power Pool Alpha Performance 可执行清单」编码成可执行判据，
并加上 2026-11-10 实证得到的**前置闸**：平台 ``themes`` 才是当期资格，
``PowerPoolSelected`` 只是成分开关；PATCH tags **不改变** themes。
只有「命中当期主题 ∧ 带标签 ∧ 质量」三者齐备，标签才影响当期 CPPAP。

判据来源
--------
- 论坛 ``44230497234839``（LZ90942）：摘「margin<10bp 且 TO>0.15」有用；
  「低换手边缘货」别摘（实测摘 7 条 BC 反掉 .053）；交满 5 条才够评奖；
  条数越多 BC 越高（8→17 条对应 .103→.200）；榜约 6h 刷新。
- 论坛 ``38846510482967``（MZ45384，74 赞）：margin 目标 15bp / 最低 10bp、
  S/F>1、曲线不低头/尾年不差、每月 2 区 + 月底点满塔、tag 管理只是权宜之计。
- 2026-11-10 平台实测：301 颗 ACTIVE 仅 1 颗命中当期 ``GLB/D1 Power Pool Nov'26``；
  其余带标签货命中 Sept/Oct/Aug **往期**主题或 ``themes=[]``。
  ⇒ 本工具对「无当期主题」的 alpha 一律输出 ``NO_LEVERAGE``，不再建议摘/补。

★ 与 MEMORY §8 的边界：margin 只是低换手代理（ρ(margin,−TO)=+0.922），
IS margin 不预测 OS ⇒ 本工具**只产出软标记/排序信息，绝不做提交硬闸**。

用法
----
    python tools/gates/ppa_readiness.py                 # 离线快照，摘要 + 落盘
    python tools/gates/ppa_readiness.py --json          # 机器可读
    python tools/gates/ppa_readiness.py --id JjeMlmXA  # 单颗判定
    python tools/gates/ppa_readiness.py --refresh       # 在线刷新（失败自动回退快照）
    python tools/gates/ppa_readiness.py --theme-match "Dec\`26"   # 指定当期主题

数据源（按优先级）：``--refresh`` 在线 > 快照 ``results/ppa_theme_scan_20261110.json``
> ``results/ppa_all_active_20261110.json``（后者无 themes，仅作兜底并标 unknown）。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "results" / "ppa_theme_scan_20261110.json"
FALLBACK = ROOT / "results" / "ppa_all_active_20261110.json"
LEDGER = ROOT / "results" / "ppa_tag_governance_log.jsonl"
OUT = ROOT / "results" / "ppa_readiness_20261110.json"

PP_TAG = "PowerPoolSelected"
MIN_ENTRIES_FOR_PRIZE = 5          # 论坛：交满 5 条才够评奖
MARGIN_TARGET_BP = 15.0           # MZ45384 目标
MARGIN_FLOOR_BP = 10.0            # MZ45384 最低
TO_EDGE = 0.15                    # 低换手边缘货阈值
MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Sept", "Oct", "Nov", "Dec"])}


# ---------------------------------------------------------------- 当期主题识别

def month_rank(name: str) -> int:
    """从 ``GLB/D1 Power Pool Nov`26`` 之类名字里解析年月，返回可比较整数。"""
    m = re.search(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)`(\d{2})", str(name))
    if not m:
        return -1
    return (2000 + int(m.group(2))) * 12 + MONTHS[m.group(1)]


def detect_current_theme(rows: list[dict], override: str | None = None) -> str | None:
    """取全池里**年月最新**的 Power Pool 主题名作为当期主题。"""
    names = {n for r in rows for n in (r.get("themes") or [])
             if "Power Pool" in str(n)}
    if not names:
        return None
    if override:
        hit = [n for n in names if override in str(n)]
        return hit[0] if hit else override
    return max(names, key=month_rank)


# ---------------------------------------------------------------- 质量档

def quality_band(margin_bp: float | None, turnover: float | None,
                 sharpe: float | None = None, fitness: float | None = None) -> str:
    """四档，对应清单的「该摘 / 别摘 / 必须留」。"""
    mg = margin_bp or 0.0
    to = turnover or 0.0
    if mg >= MARGIN_TARGET_BP and to <= TO_EDGE:
        return "ANCHOR"          # 必须留：高质量锚
    if mg >= MARGIN_FLOOR_BP and to <= TO_EDGE:
        return "OK"              # 达标
    if mg < MARGIN_FLOOR_BP and to > TO_EDGE:
        return "WEAK"            # 论坛双判据交集：该摘候选
    if mg < MARGIN_FLOOR_BP and to <= TO_EDGE:
        return "EDGE"            # 低换手边缘货：别摘
    return "WATCH"               # margin 达标但高换手，无明确实证


def candidate_soft_flag(margin_bp: float | None, sharpe: float | None = None,
                        fitness: float | None = None) -> dict:
    """★ 挖掘候选的**软标记**（只报信息，不拦截，避免与 MEMORY §8 的否决冲突）。"""
    mg = margin_bp or 0.0
    return {
        "margin_bp": round(mg, 2),
        "target_bp": MARGIN_TARGET_BP,
        "floor_bp": MARGIN_FLOOR_BP,
        "meets_target": mg >= MARGIN_TARGET_BP,
        "meets_floor": mg >= MARGIN_FLOOR_BP,
        "s_f_gt_1": bool((sharpe or 0) > 1 and (fitness or 0) > 1),
        "note": ("软标记仅用于 CPPAP 取向的候选排序；不得作为提交硬闸——"
                 "IS margin 不预测 OS，且 margin 只是低换手代理（MEMORY §8）"),
    }


# ---------------------------------------------------------------- 逐颗动作

def classify(r: dict, current_theme: str | None, current_count: int) -> dict:
    themes = [str(t) for t in (r.get("themes") or [])]
    in_current = bool(current_theme and any(current_theme in t for t in themes))
    tagged = bool(r.get("ppa")) or PP_TAG in [str(t) for t in (r.get("tags") or [])]
    band = quality_band(r.get("margin_bp"), r.get("turnover"),
                        r.get("sharpe"), r.get("fitness"))

    if not in_current:
        action, why = "NO_LEVERAGE", "未命中当期主题：标签对当期 CPPAP 无杠杆（PATCH 不改 themes）"
    elif band in ("ANCHOR", "OK", "EDGE"):
        action = "KEEP_TAG" if tagged else "CONSIDER_ADD"
        why = ("高质量锚/达标/低换手边缘货：标签应保留" if tagged
               else "命中当期主题且质量达标：可补标签（总数≤5，仅提交后）")
        if band == "EDGE" and tagged:
            why += "；论坛实测摘此类 BC 反掉 .053"
    elif band == "WEAK":
        if not tagged:
            action, why = "KEEP_UNTAGGED", "命中当期主题但质量弱：不要补标签"
        elif current_count < MIN_ENTRIES_FOR_PRIZE:
            action, why = "HOLD_LOW_COUNT", (
                f"当期池仅 {current_count} 颗（<{MIN_ENTRIES_FOR_PRIZE} 条评奖线）："
                "论坛实证条数越多 BC 越高，此时摘货会清零参赛资格")
        else:
            action, why = "CONSIDER_REMOVE", "论坛双判据交集：摘高换手低 margin 有效（一次一条）"
    else:
        action, why = "WATCH", "margin 达标但高换手，论坛无明确实证，先观察"

    return {
        "id": r.get("id"), "region": r.get("region"),
        "themes": themes, "in_current_theme": in_current,
        "tags": r.get("tags") or [], "has_pp_tag": tagged,
        "margin_bp": r.get("margin_bp"), "turnover": r.get("turnover"),
        "sharpe": r.get("sharpe"), "fitness": r.get("fitness"),
        "quality_band": band, "action": action, "reason": why,
        "soft_flag": candidate_soft_flag(r.get("margin_bp"), r.get("sharpe"), r.get("fitness")),
    }


# ---------------------------------------------------------------- 取数

def load_snapshot() -> tuple[list[dict], str]:
    if SNAPSHOT.exists():
        return json.loads(SNAPSHOT.read_text(encoding="utf-8")), str(SNAPSHOT.relative_to(ROOT))
    if FALLBACK.exists():
        rows = json.loads(FALLBACK.read_text(encoding="utf-8"))
        for r in rows:
            r.setdefault("themes", [])
        return rows, str(FALLBACK.relative_to(ROOT)) + "（无 themes，判据降级）"
    raise SystemExit("缺少快照：请先跑 results/ppa_theme_scan_20261110.json")


def apply_ledger_corrections(rows: list[dict]) -> tuple[list[dict], list[str]]:
    """用治理台账的**最终态**校正快照里的 tags。

    背景：``ppa_theme_scan_20261110.json`` 是在 11-10 两条标签实验（seq1/seq2）
    生效期间采集的；seq3/seq4 已把它们回滚。themes 不受标签影响仍可用，但
    tags/ppa 必须按台账最后一次动作覆盖，否则会把已恢复的标签误判成未带标签。
    """
    if not LEDGER.exists():
        return rows, []
    final: dict[str, list[str]] = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        aid = rec.get("alpha_id")
        if not aid:
            continue
        if "restored_tags" in rec:            # rollback：权威最终态
            final[aid] = list(rec["restored_tags"])
        elif "after_tags" in rec:             # add/remove 的中间态
            final[aid] = list(rec["after_tags"])
    applied = []
    for r in rows:
        if r.get("id") in final:
            r["tags"] = final[r["id"]]
            r["ppa"] = PP_TAG in r["tags"]
            applied.append(r["id"])
    return rows, applied


async def fetch_online() -> list[dict] | None:
    sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))
    try:
        from brain_api import brain_client
    except Exception as e:  # noqa: BLE001
        print(f"[refresh] 无法加载 brain_client：{e}，回退快照", file=sys.stderr)
        return None
    await brain_client.ensure_authenticated()
    rows = []
    for off in range(0, 700, 100):
        got = None
        for _ in range(4):
            try:
                resp = await brain_client._request(
                    "GET", f"{brain_client.base_url}/users/self/alphas"
                           f"?stage=OS&status=ACTIVE&limit=100&offset={off}&order=-dateSubmitted")
                got = resp.json()
                break
            except Exception:  # noqa: BLE001 —— 平台限流返回非 JSON
                await asyncio.sleep(2)
        if got is None:
            print("[refresh] 平台连续非 JSON 响应，回退快照", file=sys.stderr)
            return None
        page = got.get("results") or []
        for a in page:
            s, m = a.get("settings") or {}, a.get("is") or {}
            tags = a.get("tags") or []
            themes = a.get("themes") or []
            rows.append(dict(
                id=a.get("id"), region=s.get("region"), tags=tags,
                ppa=(PP_TAG in tags),
                themes=[t.get("name") if isinstance(t, dict) else str(t) for t in themes],
                sharpe=m.get("sharpe"), fitness=m.get("fitness"),
                margin_bp=round((m.get("margin") or 0) * 10000, 2),
                turnover=m.get("turnover"), dateSubmitted=a.get("dateSubmitted")))
        if len(page) < 100:
            break
    return rows


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="CPPAP 就绪度判据（只读）")
    ap.add_argument("--refresh", action="store_true", help="在线拉平台（失败回退快照）")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    ap.add_argument("--id", help="只看某一颗")
    ap.add_argument("--theme-match", default=None, help="指定当期主题片段，如 Nov`26")
    ap.add_argument("--no-write", action="store_true", help="不落盘结果")
    a = ap.parse_args()

    source = "online"
    rows = asyncio.run(fetch_online()) if a.refresh else None
    corrected: list[str] = []
    if not rows:
        rows, source = load_snapshot()
        rows, corrected = apply_ledger_corrections(rows)

    cur = detect_current_theme(rows, a.theme_match)
    n_current = sum(1 for r in rows
                    if cur and any(cur in str(t) for t in (r.get("themes") or [])))
    items = [classify(r, cur, n_current) for r in rows]
    if a.id:
        items = [x for x in items if x["id"] == a.id]

    counter = Counter(x["quality_band"] for x in items)
    acts = Counter(x["action"] for x in items)
    result = {
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "source": source, "active_scanned": len(rows),
        "ledger_tag_corrections": corrected,
        "current_theme": cur, "current_theme_entries": n_current,
        "prize_line": MIN_ENTRIES_FOR_PRIZE,
        "prize_eligible": n_current >= MIN_ENTRIES_FOR_PRIZE,
        "quality_bands": dict(counter), "actions": dict(acts),
        "rules": {
            "ANCHOR": "margin>=15bp 且 TO<=0.15 → 必须留",
            "OK": "margin>=10bp 且 TO<=0.15 → 留",
            "WEAK": "margin<10bp 且 TO>0.15 → 论坛双判据，该摘候选",
            "EDGE": "margin<10bp 且 TO<=0.15 → 别摘（实测 BC 反掉 .053）",
            "NO_LEVERAGE": "未命中当期 themes → 标签对当期 CPPAP 无杠杆",
            "HOLD_LOW_COUNT": f"当期池<{MIN_ENTRIES_FOR_PRIZE} 条 → 条数越少 BC 越低，暂缓摘货",
        },
        "boundary": ["tag 管理只保护 CPPAP，对 Combined/Selected 无效",
                     "BC−AC 差值固定 .159–.177，只能靠换货",
                     "本地日 PnL 近似不可信（穷举挑 10 条反而 +.023→−.039）",
                     "margin 仅软标记，不得作为提交硬闸（MEMORY §8）"],
        "items": items,
    }

    if not a.no_write and not a.id:
        OUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    if a.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0

    print(f"数据源 {source}｜ACTIVE {len(rows)} 颗｜台账标签校正 {len(corrected)} 颗 {corrected}")
    print(f"当期主题 {cur}｜命中 {n_current} 颗｜评奖线 {MIN_ENTRIES_FOR_PRIZE} 条"
          f"｜{'达标' if result['prize_eligible'] else '未达标（标签治理无杠杆）'}")
    print("质量档", dict(counter))
    print("动作档", dict(acts))
    for x in items:
        if x["action"] in ("CONSIDER_REMOVE", "CONSIDER_ADD", "HOLD_LOW_COUNT") or a.id:
            print(f"  {x['id']:10s} {x['action']:17s} {x['quality_band']:7s} "
                  f"margin={x['margin_bp']}bp TO={x['turnover']} | {x['reason']}")
    if not a.no_write and not a.id:
        print(f"落盘 → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
