import asyncio,json,sys,os
sys.path.insert(0,r"D:\coding\traeCN_project\wqb\world-quant-brain-mcp")
async def main():
    from brain_api import brain_client
    from tools_data import validate_expressions
    await brain_client.ensure_authenticated()
    exprs=[
      # shortinterest5（涨跌停/交易机制）
      "group_rank(multiply(-1, max_price_decrease_ratio), market)",
      "group_rank(divide(max_price_decrease_ratio, add(max_price_decrease_ratio, max_price_increase_ratio)), market)",
      "group_rank(price_limit_condition, market)",
      "group_rank(ts_mean(max_price_decrease_ratio, 22), market)",
      # shrt38 z_sec_rel MATRIX（行业关系）
      "group_rank(vec_avg(shrt38_z_sec_relsec_cd), market)",
      # shrt38 频率/窗口维度
      "group_rank(vec_avg(shrt38_pyt_qrf), market)",
      "group_rank(vec_avg(shrt38_stk_agg_invactcalc_prd_typ), market)",
      "group_rank(vec_avg(shrt38_stk_agg_short_sellcalc_prd_typ), market)",
      "group_rank(vec_avg(shrt38_finacc_typ_22), market)",
      "group_rank(vec_avg(shrt38_issue_typ), market)",
      # 单位卖空金额（帖3 比值）
      "group_rank(divide(vec_avg(shrt38_tot_amt_wgt), add(vec_avg(shrt38_tot_qty_wgt), 0.0001)), market)",
    ]
    r=await validate_expressions(exprs, region="KOR", universe="TOP600", delay=1)
    print("valid:", r.get("valid"), "unknown:", r.get("unknown_fields"))
    print("checked:", r.get("fields_checked"), "n_platform:", r.get("platform_field_count"))
asyncio.run(main())
