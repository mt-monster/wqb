$ErrorActionPreference='Stop'
$cd='D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom'
$py='D:/coding/traeCN_project/wqb/tools/mcp_http_caller.py'
$sets=@('ml_factor_proj','quant_factor_lib','price_signal_dl','ai_equity_alpha')
foreach($s in $sets){
  & python $py --service wq-brain-http --timeout 300 get_datafields ("@" + (Join-Path $cd ("_df_" + $s + ".json"))) 2>&1 | Out-File -FilePath (Join-Path $cd ("_dfout_" + $s + ".json")) -Encoding utf8
  Write-Output ("done " + $s)
}