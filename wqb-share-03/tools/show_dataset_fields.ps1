param([string]$Dataset = 'sentiment22', [int]$Top = 30)
$path = "D:\coding\traeCN_project\wqb\wqb-share-03\tracking\$Dataset`_fields.json"
$f = Get-Content $path -Raw | ConvertFrom-Json
$fields = $f.results
if (-not $fields) { $fields = $f.result.datafields }
Write-Host "===== $Dataset ====="
Write-Host ("Total fields: " + $fields.Count)
# Filter MATRIX type only (most usable), sort by coverage
$rows = $fields | Where-Object { $_.type -eq 'MATRIX' } |
    Sort-Object coverage -Descending |
    Select-Object id, coverage, valueScore, userCount, alphaCount, description -First $Top
Write-Host ("MATRIX fields (top " + $Top + " by coverage):")
foreach ($r in $rows) {
    $line = "{0,-50} cov={1,-6} val={2,-5} u={3,-4} a={4,-5}" -f $r.id, $r.coverage, $r.valueScore, $r.userCount, $r.alphaCount
    if ($r.description) { $line += " | " + $r.description }
    Write-Host $line
}
Write-Host ""
# Also list valueScore leaders
Write-Host "Top 15 by valueScore:"
$rows2 = $fields | Where-Object { $_.type -eq 'MATRIX' -and $_.valueScore -ne $null } |
    Sort-Object valueScore -Descending |
    Select-Object id, coverage, valueScore, userCount, alphaCount, description -First 15
foreach ($r in $rows2) {
    $line = "{0,-50} cov={1,-6} val={2,-5} u={3,-4} a={4,-5}" -f $r.id, $r.coverage, $r.valueScore, $r.userCount, $r.alphaCount
    if ($r.description) { $line += " | " + $r.description }
    Write-Host $line
}
