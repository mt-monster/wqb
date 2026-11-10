# -*- coding: utf-8 -*-
r"""PP 池标签治理执行器（默认 dry-run，需 ``--confirm`` 才写平台）。

配套 ``ppa_readiness.py``：只消费它产出的 ``results/ppa_readiness_20261110.json``，
默认只执行 ``CONSIDER_REMOVE``（摘）或 ``--add`` 时的 ``CONSIDER_ADD``（补）。

★ 安全阀（对应 2026-11-10 实证与论坛纪律）
  1. ``NO_LEVERAGE`` 一律不处理 —— 未命中当期 themes，改标签对当期 CPPAP 无作用；
     要强行处理需显式 ``--allow-no-leverage``（会打印警告）。
  2. ``HOLD_LOW_COUNT`` 一律不处理 —— 当期池<5 条评奖线时摘货会清零参赛资格；
     要强行处理需显式 ``--force-low-count``。
  3. ``ANCHOR`` / ``OK`` / ``EDGE`` 永不摘（论坛：低换手边缘货摘了 BC 反掉 .053）。
  4. 默认 ``--limit 1``（论坛：一次只动一条，等约 6h 读 BC/AC 再决定留/回滚）。
  5. PATCH 载荷只发 ``tags`` + ``regular.description`` 原样回显，
     避免 2026-09-20「MCP set_alpha_properties 清空 name/description」事故；
     每条回读验证 tags/desc/name/color，任一不符自动回滚。
  6. 所有动作写 append-only 台账 ``results/ppa_tag_governance_log.jsonl``。

用法
----
    python tools/gates/ppa_tag_apply.py                      # 干跑，打印将执行的计划
    python tools/gates/ppa_tag_apply.py --add               # 干跑补标签计划
    python tools/gates/ppa_tag_apply.py --confirm --limit 1 # 真正执行 1 条
    python tools/gates/ppa_tag_apply.py --allow-no-leverage --force-low-count  # 仅演示，仍须 --confirm

注意：本脚本**不提交 alpha**，不触碰挖掘闸与 ``config.py``。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "results" / "ppa_readiness_20261110.json"
LEDGER = ROOT / "results" / "ppa_tag_governance_log.jsonl"
PP_TAG = "PowerPoolSelected"
MAX_TAGS = 5


def load_plan() -> dict:
    if not PLAN.exists():
        raise SystemExit("缺少计划文件，请先跑：python tools/gates/ppa_readiness.py")
    return json.loads(PLAN.read_text(encoding="utf-8"))


def next_seq() -> int:
    if not LEDGER.exists():
        return 1
    n = 0
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                n = max(n, int(json.loads(line).get("seq") or 0))
            except json.JSONDecodeError:
                continue
    return n + 1


def select(items: list[dict], a) -> list[dict]:
    wanted = "CONSIDER_ADD" if a.add else "CONSIDER_REMOVE"
    out = []
    for x in items:
        act = x["action"]
        if act == wanted:
            out.append(x)
        elif (a.allow_no_leverage and act == "NO_LEVERAGE" and x["has_pp_tag"]
              and not a.add and x["quality_band"] == "WEAK"):
            # 强制模式也只认论坛双判据交集（margin<10bp 且 TO>0.15），
            # 不把 WATCH（margin 达标但高换手）误纳入原清单的 18 颗。
            out.append(dict(x, action="FORCED_NO_LEVERAGE",
                            reason="用户显式 --allow-no-leverage：该货无当期主题，改标签无效"))
        elif (a.force_low_count and act == "HOLD_LOW_COUNT" and not a.add
              and x["quality_band"] == "WEAK"):
            out.append(dict(x, action="FORCED_LOW_COUNT",
                            reason="用户显式 --force-low-count：会清零当期唯一参赛货"))
    # 永不摘高质量锚/达标/边缘货
    if not a.add:
        out = [x for x in out if x["quality_band"] not in ("ANCHOR", "OK", "EDGE")]
    else:
        out = [x for x in out if len(x["tags"]) < MAX_TAGS]
    return out[: a.limit]


def build_tags(x: dict, add: bool) -> list[str]:
    tags = list(x["tags"])
    if add:
        return tags + [PP_TAG] if PP_TAG not in tags else tags
    return [t for t in tags if t != PP_TAG]


async def get_detail(client, aid: str) -> dict | None:
    for _ in range(4):
        try:
            r = await client._request("GET", f"{client.base_url}/alphas/{aid}")
            return r.json()
        except Exception:  # noqa: BLE001 —— 平台限流返回非 JSON
            await asyncio.sleep(2)
    return None


async def apply_one(client, x: dict, add: bool, seq: int) -> dict:
    aid = x["id"]
    before = await get_detail(client, aid)
    if before is None:
        return {"alpha_id": aid, "ok": False, "error": "GET 详情失败（平台限流），未改动"}
    desc = ((before.get("regular") or {}).get("description")) or ""
    cur_tags = list(before.get("tags") or [])
    target = build_tags(x, add)
    payload = {"tags": target, "regular": {"description": desc}}
    status = None
    for _ in range(4):
        try:
            resp = await client._request("PATCH", f"{client.base_url}/alphas/{aid}", json=payload)
            status = resp.status_code
            if status < 400:
                break
        except Exception:  # noqa: BLE001
            status = -1
        await asyncio.sleep(2)
    after = await get_detail(client, aid)
    if after is None:
        # 无法确认 → 按原 tags 回滚，避免留下未知状态
        await client._request("PATCH", f"{client.base_url}/alphas/{aid}",
                              json={"tags": cur_tags, "regular": {"description": desc}})
        return {"alpha_id": aid, "ok": False, "error": "PATCH 后回读失败，已自动回滚"}
    a_tags = list(after.get("tags") or [])
    a_desc = ((after.get("regular") or {}).get("description")) or ""
    ok = (status is not None and status < 400 and a_tags == target
          and len(a_desc) == len(desc)
          and after.get("name") == before.get("name")
          and after.get("color") == before.get("color"))
    if not ok:
        await client._request("PATCH", f"{client.base_url}/alphas/{aid}",
                              json={"tags": cur_tags, "regular": {"description": desc}})
    rec = {
        "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "seq": seq,
        "action": ("add_power_pool_selected" if add else "remove_power_pool_selected"),
        "alpha_id": aid, "region": x.get("region"),
        "before_tags": cur_tags, "after_tags": a_tags,
        "desc_len_before": len(desc), "desc_len_after": len(a_desc),
        "quality_band": x.get("quality_band"), "readiness_action": x.get("action"),
        "reason": x.get("reason"), "http_status": status,
        "verification": ok,
        "rollback_payload": {"tags": cur_tags, "regular": {"description": "<echo>"}},
        "note": "由 tools/gates/ppa_tag_apply.py 执行；失败自动回滚",
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description="PP 池标签治理执行器（默认 dry-run）")
    ap.add_argument("--confirm", action="store_true", help="真正 PATCH（默认只打印计划）")
    ap.add_argument("--add", action="store_true", help="处理补标签队列而非摘标签队列")
    ap.add_argument("--limit", type=int, default=1, help="本次最多处理几条（默认 1）")
    ap.add_argument("--allow-no-leverage", action="store_true",
                    help="允许处理无当期主题货（明示无效，仅用户强制时）")
    ap.add_argument("--force-low-count", action="store_true",
                    help="允许在当期池<5 条时摘货（会清零参赛资格）")
    a = ap.parse_args()

    plan = load_plan()
    items = select(plan.get("items") or [], a)
    print(f"计划源 {PLAN.relative_to(ROOT)}｜当期主题 {plan.get('current_theme')}"
          f"｜命中 {plan.get('current_theme_entries')} 颗"
          f"｜评奖线 {plan.get('prize_line')} 条"
          f"｜{'达标' if plan.get('prize_eligible') else '未达标'}")
    print(f"模式 {'补标签' if a.add else '摘标签'}｜{'执行' if a.confirm else 'DRY-RUN'}｜上限 {a.limit} 条")
    if not items:
        print("\n[结论] 0 条可执行 —— 当前账户对当期 CPPAP 没有标签治理杠杆：")
        print("  · 300 颗 NO_LEVERAGE（未命中当期 themes，PATCH 不改 themes）")
        print("  · 1 颗 HOLD_LOW_COUNT（当期唯一参赛货，摘了清零池子）")
        print("  ⇒ 正道是新提交命中当期主题的高质量 alpha，而不是改标签。")
        print("  若仍要强行执行，需同时给 --allow-no-leverage --force-low-count --confirm。")
        return 0
    for x in items:
        target = build_tags(x, a.add)
        print(f"  {x['id']:10s} {x['action']:20s} {x['quality_band']:7s} "
              f"margin={x['margin_bp']}bp TO={x['turnover']} "
              f"tags {x['tags']} → {target}")
        print(f"      {x['reason']}")
    if not a.confirm:
        print("\n[DRY-RUN] 未改动平台。加 --confirm 才执行。")
        return 0

    sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))
    from brain_api import brain_client

    async def run():
        await brain_client.ensure_authenticated()
        seq = next_seq()
        for x in items:
            rec = await apply_one(brain_client, x, a.add, seq)
            print(f"  [seq {seq}] {rec['alpha_id']} ok={rec.get('verification', False)} "
                  f"tags={rec.get('after_tags')} {rec.get('error', '')}")
            seq += 1
    asyncio.run(run())
    print(f"台账 → {LEDGER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
