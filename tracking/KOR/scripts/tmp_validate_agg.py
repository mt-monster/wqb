import asyncio,json,sys,os
sys.path.insert(0,r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
async def main():
    from brain_api import brain_client
    from tools_data import validate_expressions
    await brain_client.ensure_authenticated()
    exprs=[
      # 换 vec 聚合算子（此前只用 vec_avg）
      "group_rank(vec_sum(shrt38_accum_net_buy_amt), market)",
      "group_rank(vec_max(shrt38_accum_net_buy_amt), market)",
      "group_rank(vec_stddev(shrt38_accum_net_buy_amt), market)",
      "group_rank(vec_range(shrt38_accum_net_buy_amt), market)",
      "group_rank(vec_count(shrt38_accum_net_buy_amt), market)",
      # 投资净买量（qty 版，此前用 amt 版）
      "group_rank(vec_avg(shrt38_stk_invactnet_buy_qty), market)",
      "group_rank(vec_avg(shrt38_accum_net_buy_qty), market)",
      # 买卖不对称（帖3 比值精神，用 invact 系列）
      "group_rank(divide(vec_avg(shrt38_stk_invactsell_amt), add(vec_avg(shrt38_stk_invactbuy_amt), 0.0001)), market)",
      # 短卖量权重（卖空股数权重）
      "group_rank(vec_avg(shrt38_stk_short_sellshort_sell_qty_wgt), market)",
      # 总卖空额水平
      "group_rank(vec_avg(shrt38_amt), market)",
    ]
    r=await validate_expressions(exprs, region="KOR", universe="TOP600", delay=1)
    print("valid:", r.get("valid"), "unknown:", r.get("unknown_fields"))
asyncio.run(main())
