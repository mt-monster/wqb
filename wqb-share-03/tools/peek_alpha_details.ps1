param([string]$File = 'tracking/result_alpha_details_QP9xgkmW.json')
$j = Get-Content $File -Raw | ConvertFrom-Json
$a = $j
if ($j.result) { $a = $j.result }
if ($j.alpha) { $a = $j.alpha }
Write-Host "=== File: $File ==="
Write-Host ("id: " + $a.id)
Write-Host ("code: " + $a.code)
Write-Host ("status: " + $a.status)
Write-Host ("grade: " + $a.grade)
Write-Host ("sharpe: " + $a.is.sharpe)
Write-Host ("fitness: " + $a.is.fitness)
Write-Host ("turnover: " + $a.is.turnover)
Write-Host ("margin: " + $a.is.margin)
Write-Host ("2Y sharpe: " + $a.is.longerHorizons2Y)
Write-Host ("subUniverse sharpe: " + $a.is.subUniverseSharpe)
Write-Host ("selfCorrelation: " + $a.is.selfCorrelation)
Write-Host ("prodCorrelation: " + $a.is.prodCorrelation)
Write-Host ("--- checks ---"
)
if ($a.is.checks) {
    $a.is.checks | Format-Table name, value, limit, result -AutoSize
}
if ($a.is.riskAttributes) {
    Write-Host "--- risk attributes ---"
    $a.is.riskAttributes | Format-Table name, result, value, limit -AutoSize
}
