import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
async def main():
    from brain_api import brain_client
    from tools_sim import create_multi_simulation
    from tools_ops import batch_status
    await brain_client.ensure_authenticated()
    # 三条最小复现：单字段裸用（不做 group_rank），看哪条能活
    tests = [
      ("A_bare_dec", "vec_avg(max_price_decrease_ratio)"),
      ("B_bare_plc", "vec_avg(price_limit_condition)"),
      ("C_bare_inc", "vec_avg(max_price_increase_ratio)"),
    ]
    r = await create_multi_simulation([t[1] for t in tests], region="KOR", universe="TOP600", delay=1,
            decay=4, neutralization="STATISTICAL", truncation=0.08, nan_handling="ON", test_period="P0Y0M")
    pid = r.get("multisimulation_id")
    print("PID:", pid)
    await asyncio.sleep(45)
    st = await batch_status([pid])
    for b in st.get("batches",[]):
        print("all_terminal:", b.get("all_terminal"))
        for c in b.get("children",[]):
            print(" ", c.get("status"), c.get("error"), "S=",c.get("sharpe"))
asyncio.run(main())
