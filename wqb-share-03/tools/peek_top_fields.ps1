param([string]$Dataset = 'ai_equity_alpha', [int]$Top = 30)
$path = "D:\coding\traeCN_project\wqb\wqb-share-03\tracking\$Dataset`_fields.json"
$j = Get-Content $path -Raw | ConvertFrom-Json
$f = $j.results
if (-not $f) { $f = $j.result.datafields }
Write-Host ("Total: " + $f.Count)
Write-Host "=== Type distribution ==="
$f | Group-Object type | Select-Object Name, Count | Format-Table -AutoSize
Write-Host "=== Top $Top by userCount ==="
$f | Where-Object { $_.userCount -ne $null -and $_.userCount -gt 0 } |
    Sort-Object userCount -Descending |
    Select-Object id, type, coverage, valueScore, userCount, alphaCount, description -First $Top |
    Format-Table -AutoSize -Wrap
Write-Host "=== Top $Top by alphaCount ==="
$f | Where-Object { $_.alphaCount -ne $null -and $_.alphaCount -gt 0 } |
    Sort-Object alphaCount -Descending |
    Select-Object id, type, coverage, valueScore, userCount, alphaCount, description -First $Top |
    Format-Table -AutoSize -Wrap
Write-Host "=== Top $Top by valueScore ==="
$f | Where-Object { $_.valueScore -ne $null -and $_.valueScore -gt 0 } |
    Sort-Object valueScore -Descending |
    Select-Object id, type, coverage, valueScore, userCount, alphaCount, description -First $Top |
    Format-Table -AutoSize -Wrap
