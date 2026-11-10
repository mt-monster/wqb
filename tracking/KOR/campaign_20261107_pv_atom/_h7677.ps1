$ErrorActionPreference='Stop'
foreach($k in @('P76','P77')){
  $f = Join-Path 'D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom' ('_harv_' + $k + '.json')
  $o = Join-Path 'D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom' ('_msout_' + $k + '.json')
  & python 'D:/coding/traeCN_project/wqb/tools/mcp_http_caller.py' --service wq-brain-http --timeout 600 harvest_multisim_alphas ('@' + $f) 2>&1 | Out-File -FilePath $o -Encoding utf8
  Write-Output ('done ' + $k)
}