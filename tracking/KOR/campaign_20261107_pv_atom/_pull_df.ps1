$ErrorActionPreference='Stop'
$cd='D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom'
$py='D:/coding/traeCN_project/wqb/tools/mcp_http_caller.py'
$sets=@('risk59','risk60','risk68','risk70','risk71','risk72','risk88','insiders1','insiders5')
foreach($s in $sets){
  $out = Join-Path $cd ("_dfout_" + $s + ".json")
  & python $py --service wq-brain-http --timeout 300 get_datafields ("@" + (Join-Path $cd ("_df_" + $s + ".json"))) 2>&1 | Out-File -FilePath $out -Encoding utf8
  Write-Output ("done " + $s)
}