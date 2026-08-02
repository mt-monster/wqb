$id = 'Vk3rkLo5'
$f = "D:\coding\traeCN_project\wqb\wqb-share-03\tracking\result_get_alpha_details_$id.json"
$j = Get-Content $f -Raw | ConvertFrom-Json
Write-Host ("code: " + $j.code)
Write-Host ("settings: neut=" + $j.settings.neutralization + " trunc=" + $j.settings.truncation + " decay=" + $j.settings.decay + " universe=" + $j.settings.universe + " maxTrade=" + $j.settings.maxTrade)
Write-Host ("metrics: sh=" + $j.metrics.sharpe + " fit=" + $j.metrics.fitness + " tvr=" + $j.metrics.turnover + " margin=" + $j.metrics.margin + " subU=" + $j.metrics.sub_universe_sharpe + " 2Y=" + $j.metrics.two_year_sharpe + " riskNeutSh=" + $j.metrics.risk_neutralized_sharpe)
Write-Host ("ra_failed: " + $j.ra.ra_failed + " count=" + $j.ra.failed_ra_count + " checks=" + ($j.ra.ra_failed_checks -join ','))
Write-Host "checks.fail:"
foreach ($c in $j.checks.fail) { Write-Host ("  " + $c.name + " value=" + $c.value + " limit=" + $c.limit) }
Write-Host "checks.warning:"
foreach ($c in $j.checks.warning) {
    $line = "  " + $c.name
    if ($c.value -ne $null) { $line += " value=" + $c.value }
    if ($c.limit -ne $null) { $line += " limit=" + $c.limit }
    Write-Host $line
}
