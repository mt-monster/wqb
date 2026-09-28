# -*- coding: utf-8 -*-
"""name_missing.py - 给仍缺 name 的 ACTIVE alpha 补规范名。

背景（2026-09-20 事故复原）：MCP set_alpha_properties 曾清空全部 name；
`tools/restore_alpha_props.py` 已恢复 47 颗原 name，本脚本补剩下的 47 颗（原 dump 无 name）。

详见 --dry-run 输出的推断（可直接改后补名）。
"""
import argparse
import os
import re
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _add_paths():
    for p in (os.path.join(_REPO, "src"),
              os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))):
        if p and p not in sys.path:
            sys.path.insert(0, p)


def infer_name(region, alpha_type, expr, alpha_id, db_path, ap):
    """推断规范名 `{REGION}_{R|S}_{family}_{短id}`。

    ★ `_seq` 不能固定为 _01：同区域同族会有多颗，会撞名（平台虽不报错，但无法区分）。
      改为用 alpha_id 末尾 4 位做唯一后缀 —— 保证唯一且可反查。
    """
    from wqb.store._common import default_db_path
    ds = ap.resolve_source_dataset(expr, db_path or default_db_path())
    fam = re.sub(r"[^a-z0-9]", "_", (ds or "alpha")).lower()[:18] or "alpha"
    tag = "S" if alpha_type == "SUPER" else "R"
    suffix = str(alpha_id)[-6:]          # 6 位：唯一 + 可反查
    return f"{region}_{tag}_{fam}_{suffix}"


def main():
    _add_paths()
    import asyncio
    import json
    from brain_api import BrainApiClient
    from wqb import alpha_properties as ap
    _bootstrap = os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    a = p.parse_args()

    async def run():
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
        todo = []
        for it in items:
            d = (await c._request("GET", f"{c.base_url}/alphas/{it['id']}")).json()
            s = d.get("settings") or {}
            if d.get("name"):
                continue
            reg = d.get("regular")
            expr = reg.get("code") if isinstance(reg, dict) else None
            nm = infer_name(s.get("region"), d.get("type"), expr, it["id"], None, ap)
            todo.append((it["id"], nm))
        print(f"待补名：{len(todo)} 颗（--apply 才写）")
        seen = set()
        for aid, nm in todo:
            dup = "  <-- 撞名!" if nm in seen else ""
            seen.add(nm)
            print(f"  {aid:9s} -> {nm}{dup}")
            if a.apply:
                r = await c._request("PATCH", f"{c.base_url}/alphas/{aid}", json={"name": nm})
                if r.status_code >= 400:
                    print(f"     !! http {r.status_code} {str(r.text)[:100]}")
        return 0

    asyncio.run(run())
    return 0


if __name__ == "__main__":
    sys.exit(main())
