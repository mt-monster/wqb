$ErrorActionPreference='Stop'
foreach($k in @('P74','P75')){
  & python 'D:/coding/traeCN_project/wqb/tools/mcp_http_caller.py' --service wq-brain-http --timeout 600 harvest_multisim_alphas ('@D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_harv_' + $k + '.json') 2>&1 | Out-File -FilePath ('D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/_msout_' + $k + '.json') -Encoding utf8
  Write-Output ('done ' + $k)
}