param([string]$Path, [int]$Count = 5)
$f = Get-Content $Path -Raw | ConvertFrom-Json
Write-Host "TotalCount: $($f.results.Count)"
$f.results | Select-Object -First $Count | ConvertTo-Json -Depth 5