import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    out = {}
    for ds in ["shortinterest38","shortinterest5","shortinterest3","shortinterest4","shortinterest6","shortinterest1","shortinterest2"]:
        try:
            r = await brain_client.get_datafields(region="KOR", universe="TOP600", delay=1, dataset_id=ds, filter_sharpe=False)
            res = r.get("results", r) if isinstance(r, dict) else r
            if res:
                out[ds] = [(f.get("id"), str(f.get("type")), str(f.get("description",""))[:80]) for f in res]
                print(f"\n===== KOR/{ds}  n={len(res)} =====")
                for i,t,d in out[ds]:
                    print(f"  {i:52s} {t:10s} {d}")
            else:
                print(f"\n===== KOR/{ds}  EMPTY =====")
        except Exception as e:
            print(f"[{ds}] ERR {type(e).__name__}: {e}")
    with open(os.path.join(REPO,"tracking/KOR/candidates/kor_si_all_fields.json"),"w",encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
asyncio.run(main())
