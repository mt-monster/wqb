. 'd:\coding\traeCN_project\wqb\wqb-share-03\wqb_mcp_core.ps1'
$session = Get-McpSession
if (-not $session) { Write-Output 'SESSION_FAIL'; exit 1 }
Write-Output "SESSION_OK:$session"
# 测试调用 get_user_alphas
$result = Invoke-McpTool -ToolName 'get_user_alphas' -Arguments @{limit=3; offset=0; sort='dateCreated'; order='desc'} -TimeoutSec 60
if ($result -and $result.result -and $result.result.structuredContent) {
    $alphas = $result.result.structuredContent.result.alphas
    if ($alphas) {
        Write-Output "ALPHAS_FOUND:$($alphas.Count)"
        foreach ($a in $alphas) {
            Write-Output "  $($a.id): Sharpe=$($a.is_sharpe) Status=$($a.status)"
        }
    } else { Write-Output 'NO_ALPHAS' }
} elseif ($result -and $result.error) {
    Write-Output "ERROR:$($result.error)"
} else {
    Write-Output 'PARSE_FAIL'
    $result | ConvertTo-Json -Depth 10 | Select-Object -First 5
}
