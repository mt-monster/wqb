# -*- coding: utf-8 -*-
"""本地零成本预检（直接复用 MCP 的 tools_data 逻辑，不占并发槽）。
用法: python tools/tmp_preflight.py <exprs_file.json> <region> <delay> [dataset_id]
"""
import asyncio, json, os, sys

REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp", ".."))


async def main():
    fp = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else "USA"
    delay = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    ds = sys.argv[4] if len(sys.argv) > 4 else None
    items = json.load(open(fp, encoding="utf-8"))
    labels = [l for l, _ in items]
    exprs = [e for _, e in items]

    import tools_data as td
    from brain_api import brain_client
    await brain_client.ensure_authenticated()

    res = await td.preflight_expressions(
        alpha_expressions=exprs, region=region, universe="TOP3000",
        delay=delay, dataset_id=ds, auto_fix_vector=True)

    print("valid:", res.get("valid"))
    print("unknown_hard:", res.get("unknown_fields"))
    print("unknown_soft:", json.dumps(res.get("unknown_soft"), ensure_ascii=False))
    print("vector_fields:", res.get("vector_fields"))
    print("any_changed:", res.get("any_changed"))
    fex = res.get("fixed_expressions") or exprs
    for i, lab in enumerate(labels):
        chg = " *FIXED*" if fex[i] != exprs[i] else ""
        print(f"[{lab}]{chg} {fex[i]}")
    # 落盘修复后的表达式
    out = [[labels[i], fex[i]] for i in range(len(labels))]
    outp = fp.replace(".json", "_fixed.json")
    json.dump(out, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved:", outp)


asyncio.run(main())
