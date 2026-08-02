param([string]$File)
$j = Get-Content $File -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($a in $j.alpha_results) {
  $m = $a.metrics; $r = $a.ra
  $checks = ''
  if ($r.ra_failed_checks) { $checks = ($r.ra_failed_checks -join ',') }
  $tvr = [math]::Round($m.turnover * 100, 1)
  $mg = [math]::Round($m.margin * 10000, 1)
  Write-Output ("{0}|{1}|sh={2}|fit={3}|tvr={4}%|margin={5}bp|subU={6}|2Y={7}|riskNeut={8}|RAfail={9}|{10}" -f $a.id, $a.code, $m.sharpe, $m.fitness, $tvr, $mg, $m.sub_universe_sharpe, $m.two_year_sharpe, $m.risk_neutralized_sharpe, $r.failed_ra_count, $checks)
}
