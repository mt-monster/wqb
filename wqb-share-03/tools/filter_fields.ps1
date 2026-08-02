param([string]$Path, [int]$Top = 60)
$f = Get-Content $Path -Raw | ConvertFrom-Json
# 关键字：核心分析师预估信号
$kw = 'eps|earnings|revenue|ebitda|target|recommend|surprise|revision|forecast|consensus|estimate|mean|median|count|up|down|upgrade|downgrade'
$rows = $f.results | Where-Object { $_.id -match $kw } |
    Sort-Object coverage -Descending |
    Select-Object id, coverage, userCount, alphaCount, description -First $Top
Write-Host "Matched: $($rows.Count)"
$rows | ForEach-Object { "{0,-55} cov={1,-6} u={2,-4} a={3,-5} | {4}" -f $_.id, $_.coverage, $_.userCount, $_.alphaCount, $_.description } | Write-Host