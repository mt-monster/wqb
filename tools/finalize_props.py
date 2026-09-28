# -*- coding: utf-8 -*-
"""finalize_props.py - alpha 属性收尾：SUPER 命名优化 + 超 5 标签瘦身。

背景（2026-09-20）：规范化全部 ACTIVE(115) 后仍有两类**可接受但不理想**项：
1. **SUPER 命名**：几条仍用 PROD 数值（`0.6483`）或 fallback `alpha`（`IND_S_alpha_x`）。
   SUPER 由 selection/combo 聚合，可用组件数命名 `IND_S_20comp_<id6>`（组件数来自 settings.selectionLimit）。
2. **超 5 标签**：历史留下了 `PowerPoolSelected`/区域码/`BLEND`/数据集名 等与
   `CH_*`/`SRC_*` 重复的标签 → 收紧到 ≤5，保留 `RETIRE_*` 等留痕。

安全：
- **精确 PATCH**：只发要改的键（name 或 tags），不碰其它。
- 每颗在变更前列入想干跑核对；`--apply` 才写；写前已有 `logs/_props_snapshot_*.json` 兜底。
"""
import argparse
import os
import re
import sys
import time

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _add_paths():
    for p in (os.path.join(_REPO, "src"),
              os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))):
        if p and p not in sys.path:
            sys.path.insert(0, p)


# name 保留白名单：SUPER 已有规范的就不动；需重写的有三类：
#   ① 纯 PROD 数值（如 "0.6498"）          ② 'alpha' fallback（如 "XXX_S_alpha_1"）
#   ③ super_build.py 旧 bug 的固定尾码 SEQ（如 "GLB_S_10comp_01"，同区多颗必然重名）
_BAD_SUPER_NAME = re.compile(
    r"^(\d+(\.\d+)?|[A-Z]{3}_S_alpha_|[A-Z]{3}_S_(?:N|\d+)comp_\d{2}$)"
)


def _super_name(region, ncomp, alpha_id):
    return f"{region}_S_{ncomp if ncomp else 'N'}comp_{str(alpha_id)[-6:]}"


def _trim_tags(tags):
    """把标签收紧到 ≤5。

    - 必保：`CH_*` / `SRC_*`（规范）与 `RETIRE_*` / `WAIT_*`（运维/留痕标记，删了丢语义）
    - 其余人工额外标签按序补满到 5
    - 去与已保留前缀重复的（如 `X数据集` + `SRC_X` 重复）
    """
    MANDATORY = ("CH_", "SRC_", "RETIRE_", "WAIT_")
    keep, extras = [], []
    for t in (tags or []):
        if not t:
            continue
        if t.startswith(MANDATORY):
            keep.append(t)
        else:
            extras.append(t)
    seen_val = {re.sub(r"^[A-Za-z0-9]+_", "", t).lower() for t in keep}
    dedup_extra = [t for t in extras if re.sub(r"^[A-Za-z0-9]+_", "", t).lower() not in seen_val]
    return (keep + dedup_extra)[:5]


async def main(apply):
    _add_paths()
    from brain_api import BrainApiClient
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

    plan = []  # (aid, payload, reason)
    for it in items:
        d = (await c._request("GET", f"{c.base_url}/alphas/{it['id']}")).json()
        s = d.get("settings") or {}
        typ = d.get("type")
        payload = {}
        # SUPER 命名
        if typ == "SUPER" and (d.get("name") or "") and _BAD_SUPER_NAME.match(d.get("name") or ""):
            ncomp = (s or {}).get("selectionLimit")
            nm = _super_name((s or {}).get("region"), ncomp, it["id"])
            payload["name"] = nm
        # tags >5 瘦身（仅当有明显可收缩项）
        tags = d.get("tags") or []
        if len(tags) > 5:
            trimmed = _trim_tags(tags)
            if trimmed != tags:
                payload["tags"] = trimmed
        if payload:
            reason = f"name={payload.get('name')!r}" if "name" in payload else ""
            reason += ((" / " if reason else "") + f"tags {len(tags)}→{len(payload.get('tags', tags))}")
            plan.append((it["id"], payload, reason))

    print(f"计划改 {len(plan)} 颗（--apply 才写）")
    for aid, pl, why in plan:
        print(f"  {aid:9s} {why}\n      payload={pl}")
        if apply:
            try:
                r = await c._request("PATCH", f"{c.base_url}/alphas/{aid}", json=pl)
                if r.status_code >= 400:
                    print(f"      !! http {r.status_code} {str(r.text)[:100]}")
                time.sleep(0.3)
            except Exception as e:  # noqa: BLE001
                print(f"      !! {str(e)[:100]}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    import asyncio
    asyncio.run(main(a.apply))
