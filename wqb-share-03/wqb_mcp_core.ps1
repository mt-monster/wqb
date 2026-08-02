# ===========================================================================
# WQB MCP Core Module
# 自动会话管理 + 超时回退 + 重试机制
# ===========================================================================
# 用法: . ./wqb_mcp_core.ps1  (dot-source 加载函数)
# ===========================================================================

# ---- 全局配置 ----
$script:WQB_MCP_URL = "http://127.0.0.1:8876/mcp"
$script:WQB_SESSION_FILE = "d:\coding\traeCN_project\wqb\wqb-share-03\tracking\.mcp_session"
$script:WQB_TRACKING_DIR = "d:\coding\traeCN_project\wqb\wqb-share-03\tracking"
$script:WQB_MAX_CONCURRENT = 7          # 平台最大并发8，留1给查询/提交
$script:WQB_BATCH_SIZE = 7              # 每批提交的表达式数量
$script:WQB_TIMEOUT_SEC = 600           # 单批次超时(秒)
$script:WQB_RETRY_MAX = 3               # 最大重试次数
$script:WQB_SESSION_RETRY_MAX = 2       # 会话过期重试次数

# ---- 会话管理 ----

function Initialize-McpSession {
    <#
    .SYNOPSIS
    初始化新的 MCP 会话，返回 session ID
    #>
    [CmdletBinding()]
    param()

    $initBody = @{
        jsonrpc = "2.0"
        method  = "initialize"
        params  = @{
            protocolVersion = "2024-11-05"
            capabilities    = @{}
            clientInfo      = @{ name = "wqb-batch-runner"; version = "2.0" }
        }
        id      = 0
    } | ConvertTo-Json -Depth 10 -Compress

    $headers = @{
        'Content-Type' = 'application/json'
        'Accept'       = 'application/json, text/event-stream'
    }

    try {
        $resp = Invoke-WebRequest -Uri $script:WQB_MCP_URL -Method POST `
            -Headers $headers -Body $initBody -UseBasicParsing -TimeoutSec 30
        $sessionId = $resp.Headers["Mcp-Session-Id"]
    } catch [System.Net.WebException] {
        if ($_.Exception.Response) {
            $sessionId = $_.Exception.Response.Headers["Mcp-Session-Id"]
            if (-not $sessionId) {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $errBody = $reader.ReadToEnd()
                Write-Warning "Init error body: $errBody"
            }
        }
    } catch {
        Write-Error "MCP init failed: $($_.Exception.Message)"
        return $null
    }

    if (-not $sessionId) {
        Write-Error "Failed to get MCP session ID"
        return $null
    }

    # 保存会话
    $parent = Split-Path $script:WQB_SESSION_FILE -Parent
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    $sessionId | Out-File -FilePath $script:WQB_SESSION_FILE -NoNewline -Encoding UTF8

    # 发送 initialized 通知
    $notifBody = @{ jsonrpc = "2.0"; method = "notifications/initialized" } | ConvertTo-Json -Depth 5 -Compress
    $notifHeaders = @{
        'Content-Type'   = 'application/json'
        'Accept'         = 'application/json, text/event-stream'
        'Mcp-Session-Id' = $sessionId
    }
    try {
        Invoke-WebRequest -Uri $script:WQB_MCP_URL -Method POST `
            -Headers $notifHeaders -Body $notifBody -UseBasicParsing -TimeoutSec 10 | Out-Null
    } catch {}

    Write-Host "[MCP] Session initialized: $sessionId" -ForegroundColor Green
    return $sessionId
}

function Get-McpSession {
    <#
    .SYNOPSIS
    获取当前有效的 MCP 会话，如不存在则自动初始化
    #>
    [CmdletBinding()]
    param()

    $sessionId = $null
    if (Test-Path $script:WQB_SESSION_FILE) {
        $sessionId = (Get-Content $script:WQB_SESSION_FILE -Raw).Trim()
    }

    if (-not $sessionId) {
        $sessionId = Initialize-McpSession
    }

    return $sessionId
}

function Clear-McpSession {
    <#
    .SYNOPSIS
    清除当前会话（用于会话过期后强制重新初始化）
    #>
    Remove-Item $script:WQB_SESSION_FILE -Force -ErrorAction SilentlyContinue
}

# ---- 核心 MCP 调用 ----

function Invoke-McpTool {
    <#
    .SYNOPSIS
    调用 MCP 工具，自动处理会话过期和重试

    .PARAMETER ToolName
    MCP 工具名称 (如 create_multi_simulation, get_user_alphas)

    .PARAMETER Arguments
    工具参数 (hashtable)

    .PARAMETER TimeoutSec
    超时时间（秒），默认 600

    .OUTPUTS
    解析后的 JSON 结果对象
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$ToolName,

        [Parameter(Mandatory)]
        [hashtable]$Arguments,

        [int]$TimeoutSec = $script:WQB_TIMEOUT_SEC,

        [int]$SessionRetryCount = 0
    )

    $sessionId = Get-McpSession
    if (-not $sessionId) {
        Write-Error "No valid MCP session"
        return $null
    }

    $headers = @{
        'Content-Type'   = 'application/json'
        'Accept'         = 'application/json, text/event-stream'
        'Mcp-Session-Id' = $sessionId
    }

    $reqBody = @{
        jsonrpc = "2.0"
        method  = "tools/call"
        params  = @{ name = $ToolName; arguments = $Arguments }
        id      = 99
    } | ConvertTo-Json -Depth 20 -Compress

    try {
        $resp = Invoke-WebRequest -Uri $script:WQB_MCP_URL -Method POST `
            -Headers $headers -Body $reqBody -UseBasicParsing -TimeoutSec $TimeoutSec
        $content = $resp.Content

        # 解析 SSE 格式
        if ($content -match '(?s)data: (.+?)(\n\n|\z)') {
            $jsonStr = $matches[1].Trim()
            return $jsonStr | ConvertFrom-Json
        } else {
            try { return $content | ConvertFrom-Json } catch { return $content }
        }
    } catch [System.Net.WebException] {
        $errResp = $_.Exception.Response
        if ($errResp) {
            $statusCode = [int]$errResp.StatusCode
            $reader = New-Object System.IO.StreamReader($errResp.GetResponseStream())
            $errBody = $reader.ReadToEnd()

            # 401/403 = 会话过期，自动重新初始化
            if ($statusCode -eq 401 -or $statusCode -eq 403 -or $errBody -match "session" -or $errBody -match "unauthorized") {
                if ($SessionRetryCount -lt $script:WQB_SESSION_RETRY_MAX) {
                    Write-Warning "[MCP] Session expired (HTTP $statusCode), re-initializing... (attempt $($SessionRetryCount + 1)/$($script:WQB_SESSION_RETRY_MAX))"
                    Clear-McpSession
                    Start-Sleep -Seconds 1
                    return Invoke-McpTool -ToolName $ToolName -Arguments $Arguments -TimeoutSec $TimeoutSec -SessionRetryCount ($SessionRetryCount + 1)
                } else {
                    Write-Error "[MCP] Max session retries exceeded"
                    return $null
                }
            }

            Write-Error "[MCP] HTTP $statusCode - $errBody"
        } else {
            # 超时或连接错误
            $errMsg = $_.Exception.Message
            if ($errMsg -match "timeout" -or $errMsg -match "timed out") {
                Write-Warning "[MCP] Request timed out for $ToolName"
                return @{ error = "TIMEOUT"; tool = $ToolName }
            }
            Write-Error "[MCP] Connection error: $errMsg"
        }
        return $null
    } catch {
        $errMsg = $_.Exception.Message
        if ($errMsg -match "timeout" -or $errMsg -match "timed out") {
            Write-Warning "[MCP] Request timed out for $ToolName"
            return @{ error = "TIMEOUT"; tool = $ToolName }
        }
        Write-Error "[MCP] Error: $errMsg"
        return $null
    }
}

# ---- 高级 API ----

function Submit-SimulationBatch {
    <#
    .SYNOPSIS
    提交一批 alpha 表达式进行模拟回测

    .DESCRIPTION
    - 自动将表达式按 BATCH_SIZE (7) 分批
    - 超时后自动通过 get_user_alphas 回退获取结果
    - 自动保存原始结果到 tracking 目录

    .PARAMETER Expressions
    Alpha 表达式数组

    .PARAMETER Settings
    回测设置 hashtable (region, universe, neutralization, decay 等)

    .PARAMETER BatchId
    批次 ID (用于文件命名)

    .OUTPUTS
    结果数组: @{ alpha_id, metrics, ra, expression, batch_id }
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string[]]$Expressions,

        [Parameter(Mandatory)]
        [hashtable]$Settings,

        [string]$BatchId = "auto"
    )

    # 限制每批不超过 MAX_CONCURRENT
    if ($Expressions.Count -gt $script:WQB_BATCH_SIZE) {
        Write-Warning "Expressions count ($($Expressions.Count)) > batch size ($($script:WQB_BATCH_SIZE)). Truncating."
        $Expressions = $Expressions[0..($script:WQB_BATCH_SIZE - 1)]
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $resultFile = Join-Path $script:WQB_TRACKING_DIR "result_${BatchId}_${timestamp}_raw.json"
    $argsFile = Join-Path $script:WQB_TRACKING_DIR "args_${BatchId}.json"

    # 构建参数
    $simArgs = @{
        alpha_expressions  = $Expressions
        instrument_type    = $Settings.instrument_type
        region             = $Settings.region
        universe           = $Settings.universe
        delay              = $Settings.delay
        decay              = $Settings.decay
        neutralization     = $Settings.neutralization
        truncation         = $Settings.truncation
        test_period        = $Settings.test_period
        unit_handling      = $Settings.unit_handling
        nan_handling       = $Settings.nan_handling
        language           = $Settings.language
        visualization      = $false
        pasteurization     = $Settings.pasteurization
        max_trade          = $Settings.max_trade
    }

    # 保存参数
    $simArgs | ConvertTo-Json -Depth 10 | Out-File -FilePath $argsFile -Encoding UTF8

    Write-Host "[BATCH $BatchId] Submitting $($Expressions.Count) expressions..." -ForegroundColor Cyan

    $result = Invoke-McpTool -ToolName "create_multi_simulation" -Arguments $simArgs -TimeoutSec $script:WQB_TIMEOUT_SEC

    # 超时回退: 通过 get_user_alphas 获取结果
    if ($result -and $result.error -eq "TIMEOUT") {
        Write-Warning "[BATCH $BatchId] Simulation timed out, falling back to get_user_alphas..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5  # 等待平台处理

        $result = Invoke-FallbackGetAlphas -BatchId $BatchId -Expressions $Expressions
    }

    if (-not $result) {
        Write-Error "[BATCH $BatchId] Failed to get results"
        return $null
    }

    # 保存原始结果
    $result | ConvertTo-Json -Depth 30 | Out-File -FilePath $resultFile -Encoding UTF8

    # 解析结果
    $parsed = Parse-SimulationResult -Result $result -BatchId $BatchId -Expressions $Expressions
    return $parsed
}

function Invoke-FallbackGetAlphas {
    <#
    .SYNOPSIS
    超时回退: 通过 get_user_alphas 获取最近的 alpha 结果
    #>
    [CmdletBinding()]
    param(
        [string]$BatchId,
        [string[]]$Expressions
    )

    $alphaArgs = @{
        limit = $script:WQB_BATCH_SIZE + 2  # 多取几个以防遗漏
        offset = 0
        sort = "dateCreated"
        order = "desc"
    }

    $retryCount = 0
    $maxRetries = 5
    $allAlphas = @()

    while ($retryCount -lt $maxRetries) {
        $result = Invoke-McpTool -ToolName "get_user_alphas" -Arguments $alphaArgs -TimeoutSec 60
        if ($result -and $result.result -and $result.result.structuredContent) {
            $alphas = $result.result.structuredContent.result.alphas
            if ($alphas) {
                $allAlphas = $alphas
                break
            }
        }
        $retryCount++
        Write-Host "  Fallback retry $retryCount/$maxRetries..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
    }

    # 构造兼容的结果格式
    $alphaResults = @()
    foreach ($alpha in $allAlphas) {
        $alphaResults += @{
            alpha_id = $alpha.id
            expression = $alpha.expression
            metrics = @{
                sharpe = $alpha.is_sharpe
                fitness = $alpha.is_fitness
                turnover = $alpha.turnover
                returns = $alpha.is_returns
                sub_universe_sharpe = $alpha.sub_universe_sharpe
                two_year_sharpe = $alpha.two_year_sharpe
            }
            ra = @{
                ra_failed = $alpha.ra_failed
                failed_ra_count = $alpha.failed_ra_count
            }
            status = $alpha.status
        }
    }

    return @{
        result = @{
            structuredContent = @{
                result = @{
                    success = $true
                    total_created = $alphaResults.Count
                    total_requested = $Expressions.Count
                    alpha_results = $alphaResults
                    fallback = $true
                }
            }
        }
    }
}

function Parse-SimulationResult {
    <#
    .SYNOPSIS
    解析 create_multi_simulation 结果，提取关键指标
    #>
    [CmdletBinding()]
    param($Result, [string]$BatchId, [string[]]$Expressions)

    $parsedResults = @()

    # 尝试多种路径提取结果
    $r = $null
    if ($Result.result -and $Result.result.structuredContent) {
        $r = $Result.result.structuredContent.result
    } elseif ($Result.result) {
        $r = $Result.result
    }

    if (-not $r) {
        Write-Warning "[BATCH $BatchId] Could not parse result structure"
        return $parsedResults
    }

    Write-Host "[BATCH $BatchId] Success: $($r.success) | Created: $($r.total_created)/$($r.total_requested)" -ForegroundColor $(if($r.success){"Green"}else{"Red"})

    if ($r.alpha_results) {
        for ($i = 0; $i -lt $r.alpha_results.Count; $i++) {
            $alpha = $r.alpha_results[$i]
            $expr = if ($i -lt $Expressions.Count) { $Expressions[$i] } else { "unknown" }

            $raPassed = -not $alpha.ra.ra_failed
            $status = if ($raPassed) { "ALL RA PASS" } else { "RA_Fail=$($alpha.ra.failed_ra_count)" }
            $color = if ($raPassed) { "Green" } else { "Red" }

            Write-Host ("  {0}: Sharpe={1} Fit={2} SubUniv={3} 2Y={4} tvr={5} [{6}]" -f `
                $alpha.alpha_id, $alpha.metrics.sharpe, $alpha.metrics.fitness, `
                $alpha.metrics.sub_universe_sharpe, $alpha.metrics.two_year_sharpe, `
                $alpha.metrics.turnover, $status) -ForegroundColor $color

            $parsedResults += @{
                alpha_id    = $alpha.alpha_id
                expression  = $expr
                batch_id    = $BatchId
                metrics     = $alpha.metrics
                ra          = $alpha.ra
                ra_passed   = $raPassed
                status      = $alpha.status
            }
        }
    }

    return $parsedResults
}

function Get-AlphaDetails {
    <#
    .SYNOPSIS
    获取单个 alpha 的详细信息
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$AlphaId)

    $result = Invoke-McpTool -ToolName "get_alpha_details" -Arguments @{ alpha_id = $AlphaId } -TimeoutSec 60

    if ($result -and $result.result -and $result.result.structuredContent) {
        return $result.result.structuredContent.result
    }
    return $null
}

function Submit-AlphaForProdCorr {
    <#
    .SYNOPSIS
    提交 alpha 以触发 ProdCorr 检查

    .OUTPUTS
    @{ success, blocked, check_result, prod_corr }
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$AlphaId)

    Write-Host "[SUBMIT] Submitting $AlphaId for ProdCorr check..." -ForegroundColor Cyan

    $result = Invoke-McpTool -ToolName "submit_alpha" -Arguments @{ alpha_id = $AlphaId } -TimeoutSec 300

    if (-not $result) {
        Write-Error "[SUBMIT] Failed to submit $AlphaId"
        return $null
    }

    $r = $null
    if ($result.result -and $result.result.structuredContent) {
        $r = $result.result.structuredContent.result
    } elseif ($result.result) {
        $r = $result.result
    }

    if ($r) {
        Write-Host "  success: $($r.success) | blocked: $($r.blocked)" -ForegroundColor $(if($r.success){"Green"}else{"Yellow"})
        if ($r.check_result -and $r.check_result.is_checks_summary) {
            foreach ($check in $r.check_result.is_checks_summary) {
                $color = if ($check.result -eq "PASS") { "Green" } elseif ($check.result -eq "FAIL") { "Red" } else { "Yellow" }
                Write-Host "  $($check.name): $($check.result) val=$($check.value) limit=$($check.limit)" -ForegroundColor $color
            }
        }
        if ($r.error) { Write-Host "  Error: $($r.error)" -ForegroundColor Red }
    }

    return $r
}

function Check-Correlation {
    <#
    .SYNOPSIS
    检查 alpha 的 ProdCorr
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory)][string]$AlphaId)

    $result = Invoke-McpTool -ToolName "check_correlation" -Arguments @{ alpha_id = $AlphaId } -TimeoutSec 120

    if ($result -and $result.result -and $result.result.structuredContent) {
        return $result.result.structuredContent.result
    }
    return $null
}

# ---- 模块加载完成 ----
# 通过 dot-source 方式加载: . ./wqb_mcp_core.ps1
# 所有函数自动在当前作用域可用
