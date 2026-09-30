import asyncio,json,sys,os
sys.path.insert(0,r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
async def main():
    from brain_api import brain_client
    from tools_data import validate_expressions
    await brain_client.ensure_authenticated()
    exprs=[
      # rsk59 内部比值（借券费率结构，与 shrt38 不同数据源）
      "group_rank(divide(vec_avg(rsk59_offer_rate), add(vec_avg(rsk59_last_rate), 0.0001)), market)",
      "group_rank(divide(vec_avg(rsk59_short_interest), add(vec_avg(rsk59_indicativeavailability), 0.0001)), market)",
      "group_rank(divide(vec_avg(rsk59_s3utilization), market)",
      # shrt38 其他比值结构
      "group_rank(divide(vec_avg(shrt38_tot_amt_wgt), add(vec_avg(shrt38_ytq), 0.0001)), market)",
      # rsk59 DTC 比值
      "group_rank(divide(vec_avg(rsk59_daystocover10day), add(vec_avg(rsk59_daystocover90day), 0.0001)), market)",
      # squeeze/crowded 比
      "group_rank(divide(vec_avg(rsk59_squeeze_risk), add(vec_avg(rsk59_crowded_score), 1)), market)",
    ]
    r=await validate_expressions(exprs, region="KOR", universe="TOP600", delay=1)
    print("valid:", r.get("valid"), "unknown:", r.get("unknown_fields"))
asyncio.run(main())
