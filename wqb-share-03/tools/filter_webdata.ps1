# Filter analyst/news/risk datasets from webdata_usa1.json, sorted by sharpe
$j = Get-Content 'D:\coding\traeCN_project\wqb\wqb-share-03\tracking\webdata_usa1.json' -Raw | ConvertFrom-Json
$j.datasets |
  Where-Object { $_.dataset -match '^(analyst|news|risk)' } |
  Sort-Object sharpe -Descending |
  Select-Object -First 30 dataset, count, sharpe, fitness,
    @{N='topNeut';E={$_.best_neuts[0].neut}},
    @{N='topNeutSh';E={$_.best_neuts[0].sharpe}},
    @{N='topNeutN';E={$_.best_neuts[0].count}} |
  Format-Table -AutoSize | Out-String -Width 200
