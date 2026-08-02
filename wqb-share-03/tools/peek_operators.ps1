$o = Get-Content tracking/operators.json -Raw | ConvertFrom-Json
if ($o.name) {
    Write-Host ($o.name -join ', ')
} else {
    $o | ConvertTo-Json -Depth 3
}
