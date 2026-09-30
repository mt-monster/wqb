import asyncio,json,sys,os
sys.path.insert(0,r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
async def main():
    from brain_api import brain_client
    from tools_data import validate_expressions
    await brain_client.ensure_authenticated()
    B="divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001))"
    exprs=[
      f"group_rank(signed_power(subtract({B},0.5),0.5), market)",
      f"group_rank(ts_rank({B},126), exchange)",
      f"group_rank(ts_decay_linear({B}, 10), market)",
      f"group_rank(ts_zscore({B}, 252), market)",
      f"group_rank(ts_mean({B}, 3), market)",
      f"group_rank(ts_median({B}, 5), market)",
      f"group_rank(rank({B}), market)",
      f"group_rank(ts_rank({B}, 378), market)",
    ]
    r=await validate_expressions(exprs, region="KOR", universe="TOP600", delay=1)
    print("valid:", r.get("valid"), "unknown:", r.get("unknown_fields"))
asyncio.run(main())
