$j = Get-Content tracking/result_recommend_datasets.json -Raw | ConvertFrom-Json
if ($j.recommendations) {
    Write-Host "=== Top 30 recommendations ==="
    $j.recommendations | Select-Object -First 30 | Format-Table dataset_id, pyramid, pyramid_alphas, score, valueScore, userCount, alphaCount, coverage -AutoSize
} elseif ($j.result) {
    Write-Host "=== result ==="
    $j.result | ConvertTo-Json -Depth 4
} else {
    $j | ConvertTo-Json -Depth 4
}
Write-Host ""
Write-Host "=== pyramid summary if present ==="
if ($j.pyramid_summary) { $j.pyramid_summary | Format-Table -AutoSize }
if ($j.pyramids) { $j.pyramids | Format-Table -AutoSize }
