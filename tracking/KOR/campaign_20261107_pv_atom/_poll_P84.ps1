$ErrorActionPreference = 'Stop'
Set-Location 'D:/coding/traeCN_project/wqb'
$py = 'D:/coding/traeCN_project/wqb/tools/mcp_http_caller.py'
$cd = 'D:/coding/traeCN_project/wqb/tracking/KOR/campaign_20261107_pv_atom/'
$jobs = @(@('P84A','https://api.worldquantbrain.com/simulations/JEO8qff54zEcscjjKG1ryt'), @('P84B','https://api.worldquantbrain.com/simulations/3DddQc6kL4QJc9z1fLp6UlUD'))
foreach($j in $jobs){
  $k = $j[0]; $loc = $j[1]
  $ap = Join-Path $cd ('_harv_' + $k + '.json')
  $a = '{"multisimulation_location":"' + $loc + '"}'
  [System.IO.File]::WriteAllText($ap, $a, (New-Object System.Text.UTF8Encoding($false)))
  $ok = $false
  for($i=1; $i -le 22; $i++){
    Start-Sleep -Seconds 40
    $out = (& python $py --service wq-brain-http --timeout 600 harvest_multisim_alphas ('@' + $ap) 2>&1 | Out-String)
    if($out -match 'No children found'){ Write-Output ($k + ' try ' + $i + ' still processing'); continue }
    $of = Join-Path $cd ('_msout_' + $k + '.json')
    [System.IO.File]::WriteAllText($of, $out, (New-Object System.Text.UTF8Encoding($false)))
    Write-Output ($k + ' harvested at try ' + $i + ' bytes=' + $out.Length)
    $ok = $true
    break
  }
  if(-not $ok){ Write-Output ($k + ' TIMEOUT') }
}
Write-Output 'ALLDONE'