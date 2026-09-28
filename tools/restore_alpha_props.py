# -*- coding: utf-8 -*-
"""restore_alpha_props.py - 恢复被误清的 name / description（事故修复专用）。

事故：2026-09-20 tools/alpha_properties.py 曾用 MCP `set_alpha_properties` 批量打 tags，
该接口 payload **无条件包含** `name` 与 `regular.description`（默认 `None`/"None"）
→ 115 颗 ACTIVE 的 name 被清空、description 被覆写为字符串 'None'。

恢复源：`logs/_os_alphas_raw.json`（事故**之前** 2026-09-19 19:33 的平台原始转储，
221 条 / 51 有 name / 58 有真实 description，SUPER 另含 selection/combo.description）。

安全设计
--------
- **最小字段 PATCH**：payload 只含要恢复的键，物理上不碰 tags/color 等已修好的属性。
- 每条独立重试（指数退避）；失败只跳过该条。
- `--apply` 才写；默认 dry-run。
"""
import asyncio
import json
import os
import sys
import time

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(_REPO, "logs", "_os_alphas_raw.json")


def _add_paths():
    for p in (os.path.join(_REPO, "src"),
              os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))):
        if p and p not in sys.path:
            sys.path.insert(0, p)


async def main(apply: bool, only_missing_ids=None):
    _add_paths()
    from brain_api import BrainApiClient
    dump = {x["id"]: x for x in json.load(open(DUMP, encoding="utf-8")) if isinstance(x, dict)}
    c = BrainApiClient()
    await c.ensure_authenticated()

    items, off = [], 0
    while off < 3000:
        r = await c._request("GET", f"{c.base_url}/users/self/alphas?limit=100&offset={off}&status=ACTIVE")
        if r.status_code != 200:
            break
        res = r.json().get("results", [])
        if not res:
            break
        items.extend(res)
        off += 100
    if only_missing_ids:
        items = [it for it in items if it["id"] in only_missing_ids]

    ok = fail = skip = 0
    for it in items:
        aid = it["id"]
        x = dump.get(aid)
        if not x:
            skip += 1
            continue
        typ = x.get("type")
        payload = {}
        if x.get("name"):
            payload["name"] = x["name"]
        if typ == "REGULAR":
            reg = x.get("regular") or {}
            desc = reg.get("description")
            if desc and desc != "None":
                payload["regular"] = {"description": desc}
        else:
            for k in ("selection", "combo"):
                v = x.get(k) or {}
                dd = v.get("description")
                if dd and dd != "None":
                    payload[k] = {"description": dd}
        if not payload:
            skip += 1
            continue
        if not apply:
            print(f"  [dry] {aid}: name={payload.get('name')!r} keys={list(payload)}")
            ok += 1
            continue
        last = None
        for i in range(4):
            try:
                r = await c._request("PATCH", f"{c.base_url}/alphas/{aid}", json=payload)
                if r.status_code < 400:
                    ok += 1
                    print(f"  [ok] {aid} keys={list(payload)}")
                    break
                last = f"HTTP {r.status_code} {str(r.text)[:100]}"
            except Exception as e:  # noqa: BLE001
                last = f"{type(e).__name__}: {str(e)[:80]}"
            if i < 3:
                await asyncio.sleep(2 * (2 ** i))
        else:
            fail += 1
            print(f"  [FAIL] {aid}: {last}")
        time.sleep(0.25)
    print(f"\n[restore] apply={apply} 恢复 {ok} / 跳过 {skip}" + (f" / 失败 {fail}" if fail else ""))
    return 0


if __name__ == "__main__":
    ap = sys.argv[1:] if len(sys.argv) > 1 else []
    asyncio.run(main(apply="--apply" in ap))
