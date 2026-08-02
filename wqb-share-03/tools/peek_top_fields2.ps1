param([string]$Dataset = 'ai_equity_alpha', [int]$Skip = 0, [int]$Top = 50)
$path = "D:\coding\traeCN_project\wqb\wqb-share-03\tracking\$Dataset`_fields.json"
$j = Get-Content $path -Raw | ConvertFrom-Json
$f = $j.results
if (-not $f) { $f = $j.result.datafields }
# MATRIX fields sorted by coverage
Write-Host "=== MATRIX fields top $Top (skip $Skip) by coverage ==="
$f | Where-Object { $_.type -eq 'MATRIX' } |
    Sort-Object coverage -Descending |
    Select-Object -Skip $Skip -First $Top |
    Select-Object id, coverage, userCount, alphaCount, description |
    Format-Table -AutoSize -Wrap
