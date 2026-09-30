"""核实指定 alpha 的 classifications / /check 原始返回 / theme 匹配情况"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    for aid in sys.argv[1:]:
        print(f"\n{'='*20} {aid} {'='*20}")
        r = await brain_client._request("GET", f"https://api.worldquantbrain.com/alphas/{aid}")
        if r.status_code != 200:
            print(f"HTTP {r.status_code}")
            continue
        d = r.json()
        print("name:", d.get("name"))
        print("status:", d.get("status"))
        print("classifications:", json.dumps([c.get("id") for c in d.get("classifications", [])], ensure_ascii=False))
        print("settings:", json.dumps(d.get("settings", {}), ensure_ascii=False))
        _pyr = d.get("pyramids")
        _plist = _pyr if isinstance(_pyr, list) else (_pyr or {}).get("list", [])
        print("pyramids:", json.dumps([p.get("name") if isinstance(p, dict) else p for p in _plist], ensure_ascii=False))
        print("desc_len:", len(d.get("description") or ""))
        is_ = d.get("is") or {}
        checks = is_.get("checks", [])
        for c in checks:
            print(f"  {c.get('name'):>34} | {c.get('result'):>8} | {c.get('value')} | limit={c.get('limit')}")

asyncio.run(main())
