# Reusable MCP-over-HTTP caller for the local wqb-mcp server (brain-platform-mcp).
# Usage: powershell -File tools/mcp_call.ps1 -Tool <toolName> [-ArgsJson '<json>'] [-Raw]
#   -Tool       : MCP tool name (e.g. authenticate, get_datasets, create_multi_simulation)
#   -ArgsJson   : JSON string of the tool's arguments (default "{}")
#   -Raw        : switch; if set, print the inner content text WITHOUT re-parsing as JSON
# Persists the MCP session-id in tracking/.mcp_session and reuses it across calls.
param(
  [Parameter(Mandatory=$true)][string]$Tool,
  [string]$ArgsJson = "{}",
  [string]$ArgsFile = "",
  [string]$OutFile = "",
  [switch]$Raw
)
if ($ArgsFile -and (Test-Path $ArgsFile)) { $ArgsJson = Get-Content $ArgsFile -Raw -Encoding UTF8 }
$ErrorActionPreference = 'Stop'
$uri = "http://127.0.0.1:8876/mcp"
$proj = "D:\coding\traeCN_project\wqb\wqb-share-03"
$sessFile = Join-Path $proj "tracking\.mcp_session"
$acceptH = "application/json, text/event-stream"

function New-Session {
  $init = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"cli","version":"1.0"}}}'
  $r = Invoke-WebRequest -Uri $uri -Method POST -Body $init -ContentType "application/json" -Headers @{Accept=$acceptH} -UseBasicParsing -TimeoutSec 1800
  $sid = $r.Headers["mcp-session-id"]
  if (-not $sid) { throw "initialize: no mcp-session-id header" }
  $h = @{Accept=$acceptH; "mcp-session-id"=$sid}
  $notif = '{"jsonrpc":"2.0","method":"notifications/initialized"}'
  try { Invoke-WebRequest -Uri $uri -Method POST -Body $notif -ContentType "application/json" -Headers $h -UseBasicParsing -TimeoutSec 1800 | Out-Null } catch {}
  Set-Content -Path $sessFile -Value $sid -NoNewline -Encoding UTF8
  return $sid
}

function Invoke-ToolCall($sid, $tool, $argsJson) {
  $id = Get-Random -Minimum 1000 -Maximum 999999
  $payload = "{`"jsonrpc`":`"2.0`",`"id`":$id,`"method`":`"tools/call`",`"params`":{`"name`":`"$tool`",`"arguments`":$argsJson}}"
  $h = @{Accept=$acceptH; "mcp-session-id"=$sid}
  $r = Invoke-WebRequest -Uri $uri -Method POST -Body $payload -ContentType "application/json" -Headers $h -UseBasicParsing -TimeoutSec 1800
  # parse SSE: collect all "data: " lines, join
  $lines = $r.Content -split "`n"
  $dataLines = $lines | Where-Object { $_ -match '^data: ' } | ForEach-Object { $_ -replace '^data: ','' }
  if (-not $dataLines) { throw "no data line in response. status=$($r.StatusCode) body=$($r.Content)" }
  $json = ($dataLines -join "`n")
  return $json
}

# load or create session
$sid = $null
if (Test-Path $sessFile) { $sid = Get-Content $sessFile -Raw -ErrorAction SilentlyContinue }
if (-not $sid) { $sid = New-Session }

try {
  $json = Invoke-ToolCall $sid $Tool $ArgsJson
} catch {
  # session may be stale -> re-init once and retry
  $sid = New-Session
  $json = Invoke-ToolCall $sid $Tool $ArgsJson
}

# parse outer envelope
$obj = $json | ConvertFrom-Json
if ($obj.error) {
  [Console]::Error.WriteLine("MCP_ERROR: " + ($obj.error | ConvertTo-Json -Depth 10))
  exit 2
}
$result = $obj.result
if (-not $result) { $outText = $json }
elseif ($result.content) {
  $text = ($result.content | Where-Object { $_.type -eq 'text' } | ForEach-Object { $_.text }) -join "`n"
  if ($result.isError) {
    [Console]::Error.WriteLine("TOOL_ERROR: " + $text)
    exit 3
  }
  if ($Raw) { $outText = $text }
  else {
    try { $inner = $text | ConvertFrom-Json; $outText = ($inner | ConvertTo-Json -Depth 20) }
    catch { $outText = $text }
  }
} else {
  $outText = ($result | ConvertTo-Json -Depth 20)
}
if ($OutFile) { [IO.File]::WriteAllText($OutFile, $outText, [Text.Encoding]::UTF8) }
else { Write-Output $outText }
