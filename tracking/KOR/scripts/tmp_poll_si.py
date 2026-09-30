# -*- coding: utf-8 -*-
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
WAVES = {
 "SI3a":"3ba5em6Ej4sTb2UGAn7PlDw",
 "SI3b":"2Pbb1HdxR594bLSkwsBnxqw",
 "SI5":"2ZXB50e9P4C9bWMe5y2hJZT",
 "SI3M":"3BUj3Ytc4Z8aUSMpe5tNcC",
}
async def main():
    from brain_api import brain_client
    from tools_ops import batch_status
    await brain_client.ensure_authenticated()
    r = await batch_status(list(WAVES.values()))
    for b in r.get("batches", []):
        print(f"\n== {b.get('batch_id')} kind={b.get('kind')} child={b.get('child_count')} all_terminal={b.get('all_terminal')} err={b.get('errors')}")
        for c in b.get("children",[]):
            print(f"   {str(c.get('status')):12s} {c.get('id')}  S={c.get('sharpe')} F={c.get('fitness')} T={c.get('turnover')} alpha={c.get('alpha')} err={str(c.get('error'))[:80]}")
asyncio.run(main())
