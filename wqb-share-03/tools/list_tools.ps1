$uri = "http://127.0.0.1:8876/mcp"
$proj = "D:\coding\traeCN_project\wqb\wqb-share-03"
$sessFile = Join-Path $proj "tracking\.mcp_session"
$sid = Get-Content $sessFile -Raw
$acceptH = "application/json, text/event-stream"
$id = Get-Random -Minimum 1000 -Maximum 999999
$payload = "{`"jsonrpc`":`"2.0`",`"id`":$id,`"method`":`"tools/list`",`"params`":{}}"
$h = @{Accept=$acceptH; "mcp-session-id"=$sid}
$r = Invoke-WebRequest -Uri $uri -Method POST -Body $payload -ContentType "application/json" -Headers $h -UseBasicParsing -TimeoutSec 1800
$lines = $r.Content -split "`n"
$dataLines = $lines | Where-Object { $_ -match '^data: ' } | ForEach-Object { $_ -replace '^data: ','' }
$json = ($dataLines -join "`n")
$obj = $json | ConvertFrom-Json
$obj.result.tools | ForEach-Object { $_.name } | Sort-Object