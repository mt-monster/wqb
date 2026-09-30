import asyncio,json,sys,os
sys.path.insert(0,r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
async def main():
    from brain_api import brain_client
    from tools_data import validate_expressions
    await brain_client.ensure_authenticated()
    exprs=[
      "group_rank(vec_avg(loan_utilization_ratio_twn), market)",
      "group_rank(vec_avg(shrt3_utilizationpercent_units), market)",
      "group_rank(vec_avg(mean_loan_rate), market)",
      "group_rank(vec_avg(borrow_activity_score), market)",
      "group_rank(vec_avg(loan_rate_volatility), market)",
      "group_rank(vec_avg(average_loan_duration_days), market)",
      "group_rank(vec_avg(shrt3_bar), market)",
      "group_rank(vec_avg(loan_utilization_ratio), market)",
      "group_rank(vec_avg(loan_utilization_ratio_d1), market)",
      "group_rank(vec_avg(average_loan_duration_days_main), market)",
      "group_rank(vec_avg(new_loaned_share_count), market)",
      "group_rank(vec_avg(-1*ts_delta(vec_avg(max_loan_rate),5)), market)",
    ]
    r=await validate_expressions(exprs, region="KOR", universe="TOP600", delay=1)
    print(json.dumps(r,ensure_ascii=False,indent=1)[:3000])
asyncio.run(main())
