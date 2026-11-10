$ErrorActionPreference = 'Stop'; Set-Location 'D:/coding/traeCN_project/wqb'
$py = 'D:/coding/traeCN_project/wqb/tools/mcp_http_caller.py'; $cd = 'D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom'
$jobs = @(@('P100A','https://api.worldquantbrain.com/simulations/RRFcPd1c4X5bbxwWAIqvr'), @('P100B','https://api.worldquantbrain.com/simulations/2io1PAgRe4BybKKUwxCggj8'))
foreach($j in $jobs){
  $k=$j[0]; $loc=$j[1]; $ap=Join-Path $cd ('_harv_'+$k+'.json')
  [System.IO.File]::WriteAllText($ap, ('{"multisimulation_location":"'+$loc+'"}'), (New-Object System.Text.UTF8Encoding($false)))
  for($i=1;$i -le 25;$i++){
    Start-Sleep -Seconds 35
    $out = (& python $py --service wq-brain-http --timeout 500 harvest_multisim_alphas ('@'+$ap) 2>&1 | Out-String)
    if($out -match 'No children found' -or $out -match 'HTTP 401' -or $out -match '"error"'){ Write-Output ($k+' try '+$i); continue }
    [System.IO.File]::WriteAllText((Join-Path $cd ('_msout_'+$k+'.json')), $out, (New-Object System.Text.UTF8Encoding($false)))
    Write-Output ($k+' harvested try '+$i+' bytes='+$out.Length); break
  }
}