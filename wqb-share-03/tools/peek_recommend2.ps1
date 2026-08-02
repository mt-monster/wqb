$j = Get-Content tracking/result_recommend_datasets.json -Raw | ConvertFrom-Json
Write-Host "=== Top 30 recommendations (sorted by total_score) ==="
$j.recommendations | Select-Object dataset_id, dataset_name, category, total_score, pyramid_score, quality_score, category_lit, category_alpha_count, category_need_to_light, pyramid_multiplier, dataset_user_count, dataset_alpha_count, os_is_sharpe | Format-Table -AutoSize -Wrap
Write-Host ""
Write-Host "=== Pyramid summary (categories that need lighting) ==="
if ($j.pyramid_summary) {
    $j.pyramid_summary | Where-Object { $_.need_to_light -gt 0 -or $_.lit -eq $false } | Format-Table -AutoSize
}
