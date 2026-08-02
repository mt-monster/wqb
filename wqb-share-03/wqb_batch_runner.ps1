# ===========================================================================
# WQB Parallel Batch Runner
# 流水线并行提交 + 自动分批 + 结果聚合
# ===========================================================================
# 用法:
#   1. 从文件加载表达式:
#      . .\wqb_batch_runner.ps1 -ExpressionFile .\expressions.json -BatchPrefix "b205"
#
#   2. 内联表达式:
#      . .\wqb_batch_runner.ps1 -Expressions @("rank(close)", "rank(open)") -BatchPrefix "b206"
#
#   3. 交互模式 (读取 stdin):
#      Get-Content .\exprs.txt | .\wqb_batch_runner.ps1 -BatchPrefix "b207"
# ===========================================================================

param(
    # 表达式数组 (内联模式)
    [string[]]$Expressions,

    # 表达式文件 (JSON 数组或每行一个表达式)
    [string]$ExpressionFile,

    # 批次前缀 (如 b205, b206)
    [string]$BatchPrefix = "auto",

    # 回测设置 (JSON 文件路径或内联 hashtable)
    [string]$SettingsFile,

    # 每批大小 (默认 7, 平台最大 8 留 1 给查询)
    [int]$BatchSize = 7,

    # 是否自动提交 RA 通过的 alpha (触发 ProdCorr)
    [switch]$AutoSubmit,

    # 是否自动检查 ProdCorr
    [switch]$AutoCheckCorr,

    # 结果输出目录
    [string]$OutputDir = "d:\coding\traeCN_project\wqb\wqb-share-03\tracking",

    # 是否使用后台作业并行提交多批 (流水线模式)
    [switch]$Pipeline,

    # 流水线深度 (同时运行的最大批次数, 默认 1 = 串行)
    [int]$PipelineDepth = 1
)

$ErrorActionPreference = "Stop"

# ---- 加载核心模块 ----
$coreModule = "d:\coding\traeCN_project\wqb\wqb-share-03\wqb_mcp_core.ps1"
if (-not (Test-Path $coreModule)) {
    Write-Error "Core module not found: $coreModule"
    exit 1
}
. $coreModule

# ---- 默认回测设置 ----
$defaultSettings = @{
    instrument_type  = "EQUITY"
    region           = "USA"
    universe         = "TOP3000"
    delay            = 1
    decay            = 10
    neutralization   = "REVERSION_AND_MOMENTUM"
    truncation       = 0.08
    test_period      = "P0Y0M"
    unit_handling    = "VERIFY"
    nan_handling     = "ON"
    language         = "FASTEXPR"
    pasteurization   = "ON"
    max_trade        = "ON"
}

# 从文件加载设置
if ($SettingsFile -and (Test-Path $SettingsFile)) {
    $loadedSettings = Get-Content $SettingsFile -Raw | ConvertFrom-Json
    foreach ($prop in $loadedSettings.PSObject.Properties) {
        $defaultSettings[$prop.Name] = $prop.Value
    }
}

# ---- 加载表达式 ----
$allExpressions = @()

if ($ExpressionFile -and (Test-Path $ExpressionFile)) {
    $content = Get-Content $ExpressionFile -Raw
    try {
        $parsed = $content | ConvertFrom-Json
        if ($parsed -is [array]) {
            $allExpressions = $parsed
        } else {
            $allExpressions = @($parsed)
        }
    } catch {
        # 非JSON, 按行读取
        $allExpressions = (Get-Content $ExpressionFile) | Where-Object { $_.Trim() -ne "" }
    }
} elseif ($Expressions -and $Expressions.Count -gt 0) {
    $allExpressions = $Expressions
}

if ($allExpressions.Count -eq 0) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\wqb_batch_runner.ps1 -Expressions @('expr1','expr2') -BatchPrefix 'b205'"
    Write-Host "  .\wqb_batch_runner.ps1 -ExpressionFile .\exprs.json -BatchPrefix 'b206'"
    Write-Host "  Get-Content exprs.txt | .\wqb_batch_runner.ps1 -BatchPrefix 'b207'"
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  WQB Batch Runner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Total expressions: $($allExpressions.Count)" -ForegroundColor White
Write-Host "  Batch size: $BatchSize (platform max: 8, using: $BatchSize)" -ForegroundColor White
Write-Host "  Pipeline depth: $PipelineDepth" -ForegroundColor White
Write-Host "  Auto-submit RA pass: $AutoSubmit" -ForegroundColor White
Write-Host "  Auto-check ProdCorr: $AutoCheckCorr" -ForegroundColor White
Write-Host "  Settings: $($defaultSettings.region)/$($defaultSettings.universe)/D$($defaultSettings.delay) | neut=$($defaultSettings.neutralization) | decay=$($defaultSettings.decay) | trunc=$($defaultSettings.truncation)" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# ---- 分批 ----
$batches = @()
for ($i = 0; $i -lt $allExpressions.Count; $i += $BatchSize) {
    $end = [Math]::Min($i + $BatchSize - 1, $allExpressions.Count - 1)
    $batchExprs = $allExpressions[$i..$end]
    $batchNum = [math]::Floor($i / $BatchSize) + 1
    $batchId = if ($BatchPrefix -ne "auto") { "${BatchPrefix}_${batchNum}" } else { "batch_$($i)_$timestamp" }
    $batches += @{
        id     = $batchId
        number = $batchNum
        exprs  = $batchExprs
        start  = $i
        end    = $end
    }
}

Write-Host "Split into $($batches.Count) batch(es):`n" -ForegroundColor Yellow
foreach ($b in $batches) {
    Write-Host "  $($b.id): expressions $($b.start + 1)-$($b.end + 1) ($($b.exprs.Count) items)" -ForegroundColor Gray
}
Write-Host ""

# ---- 初始化会话 ----
Write-Host "Initializing MCP session..." -ForegroundColor Cyan
$session = Get-McpSession
if (-not $session) {
    Write-Error "Failed to initialize MCP session"
    exit 1
}

# ---- 执行批次 ----
$allResults = @()
$raPassedAlphas = @()
$startTime = Get-Date

if ($Pipeline -and $PipelineDepth -gt 1 -and $batches.Count -gt 1) {
    # ---- 流水线模式: 使用后台作业并行提交 ----
    Write-Host "[PIPELINE] Running in pipeline mode (depth=$PipelineDepth)`n" -ForegroundColor Magenta

    $activeJobs = @{}
    $batchIndex = 0
    $completedBatches = 0

    while ($completedBatches -lt $batches.Count) {
        # 启动新批次 (直到达到流水线深度或所有批次已启动)
        while ($activeJobs.Count -lt $PipelineDepth -and $batchIndex -lt $batches.Count) {
            $batch = $batches[$batchIndex]
            $jobScript = {
                param($BatchObj, $Settings, $CoreModule, $OutputDir)

                . $CoreModule

                $result = Submit-SimulationBatch -Expressions $BatchObj.exprs -Settings $Settings -BatchId $BatchObj.id
                return $result
            }

            Write-Host "[PIPELINE] Starting batch $($batch.id)..." -ForegroundColor Cyan
            $job = Start-Job -ScriptBlock $jobScript -ArgumentList $batch, $defaultSettings, $coreModule, $OutputDir
            $activeJobs[$batch.id] = @{ job = $job; batch = $batch; startTime = Get-Date }
            $batchIndex++
        }

        # 检查完成的作业
        $completed = @()
        foreach ($key in $activeJobs.Keys) {
            $jobInfo = $activeJobs[$key]
            if ($jobInfo.job.State -eq "Completed" -or $jobInfo.job.State -eq "Failed") {
                $completed += $key
            }
        }

        foreach ($key in $completed) {
            $jobInfo = $activeJobs[$key]
            $batch = $jobInfo.batch
            $elapsed = ((Get-Date) - $jobInfo.startTime).TotalSeconds

            if ($jobInfo.job.State -eq "Completed") {
                $batchResults = Receive-Job -Job $jobInfo.job
                Write-Host "[PIPELINE] Batch $($batch.id) completed in ${elapsed}s" -ForegroundColor Green

                if ($batchResults) {
                    $allResults += $batchResults
                    foreach ($r in $batchResults) {
                        if ($r.ra_passed) { $raPassedAlphas += $r }
                    }
                    Print-BatchResults -Results $batchResults
                }
            } else {
                Write-Host "[PIPELINE] Batch $($batch.id) FAILED after ${elapsed}s" -ForegroundColor Red
                $err = Receive-Job -Job $jobInfo.job -Keep
                Write-Host "  Error: $($err | Out-String)" -ForegroundColor Red
            }

            Remove-Job -Job $jobInfo.job -Force
            $activeJobs.Remove($key)
            $completedBatches++
        }

        # 短暂等待
        if ($activeJobs.Count -gt 0) {
            Start-Sleep -Seconds 2
        }
    }

} else {
    # ---- 串行模式: 逐批提交 ----
    Write-Host "[SERIAL] Running in serial mode`n" -ForegroundColor Magenta

    for ($i = 0; $i -lt $batches.Count; $i++) {
        $batch = $batches[$i]
        $batchStart = Get-Date

        Write-Host "`n--- Batch $($i + 1)/$($batches.Count): $($batch.id) ---" -ForegroundColor Cyan
        Write-Host "  Expressions:" -ForegroundColor Gray
        for ($j = 0; $j -lt $batch.exprs.Count; $j++) {
            Write-Host "    $($j + 1). $($batch.exprs[$j].Substring(0, [Math]::Min(80, $batch.exprs[$j].Length)))..." -ForegroundColor DarkGray
        }

        $batchResults = Submit-SimulationBatch -Expressions $batch.exprs -Settings $defaultSettings -BatchId $batch.id
        $elapsed = ((Get-Date) - $batchStart).TotalSeconds

        if ($batchResults) {
            $allResults += $batchResults
            foreach ($r in $batchResults) {
                if ($r.ra_passed) { $raPassedAlphas += $r }
            }
            Write-Host "  Batch completed in ${elapsed}s | RA passed: $($batchResults | Where-Object { $_.ra_passed }).Count/$($batchResults.Count)" -ForegroundColor Green
        } else {
            Write-Host "  Batch FAILED after ${elapsed}s" -ForegroundColor Red
        }

        # 批次间短暂间隔 (避免请求过快)
        if ($i -lt $batches.Count - 1) {
            Write-Host "  Waiting 2s before next batch..." -ForegroundColor DarkGray
            Start-Sleep -Seconds 2
        }
    }
}

# ---- 汇总结果 ----
$totalElapsed = ((Get-Date) - $startTime).TotalSeconds

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  BATCH RUN SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Total expressions: $($allExpressions.Count)" -ForegroundColor White
Write-Host "  Total batches: $($batches.Count)" -ForegroundColor White
Write-Host "  Total results: $($allResults.Count)" -ForegroundColor White
Write-Host "  RA passed: $($raPassedAlphas.Count)" -ForegroundColor $(if($raPassedAlphas.Count -gt 0){"Green"}else{"Yellow"})
Write-Host "  Total time: $([math]::Round($totalElapsed, 1))s" -ForegroundColor White
Write-Host "  Avg per expression: $([math]::Round($totalElapsed / $allExpressions.Count, 1))s" -ForegroundColor White
Write-Host "========================================`n" -ForegroundColor Cyan

# ---- 打印 RA 通过的 alpha ----
if ($raPassedAlphas.Count -gt 0) {
    Write-Host "RA-PASSED ALPHAS:" -ForegroundColor Green
    foreach ($r in $raPassedAlphas) {
        Write-Host ("  {0} | Sharpe={1} Fit={2} SubUniv={3} 2Y={4} tvr={5}" -f `
            $r.alpha_id, $r.metrics.sharpe, $r.metrics.fitness, `
            $r.metrics.sub_universe_sharpe, $r.metrics.two_year_sharpe, `
            $r.metrics.turnover) -ForegroundColor Green
        Write-Host "    expr: $($r.expression.Substring(0, [Math]::Min(100, $r.expression.Length)))" -ForegroundColor DarkGray
    }
    Write-Host ""
}

# ---- 保存聚合结果 ----
$summaryFile = Join-Path $OutputDir "batch_summary_${BatchPrefix}_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$summary = @{
    batch_prefix    = $BatchPrefix
    timestamp       = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    total_exprs     = $allExpressions.Count
    total_batches   = $batches.Count
    total_results   = $allResults.Count
    ra_passed_count = $raPassedAlphas.Count
    elapsed_sec     = [math]::Round($totalElapsed, 1)
    settings        = $defaultSettings
    all_results     = $allResults
    ra_passed       = $raPassedAlphas
}
$summary | ConvertTo-Json -Depth 20 | Out-File -FilePath $summaryFile -Encoding UTF8
Write-Host "Summary saved to: $summaryFile" -ForegroundColor Gray

# ---- 自动提交 RA 通过的 alpha ----
if ($AutoSubmit -and $raPassedAlphas.Count -gt 0) {
    Write-Host "`n[AUTO-SUBMIT] Submitting $($raPassedAlphas.Count) RA-passed alphas..." -ForegroundColor Magenta

    foreach ($alpha in $raPassedAlphas) {
        Write-Host "`n  Submitting $($alpha.alpha_id)..." -ForegroundColor Cyan
        $submitResult = Submit-AlphaForProdCorr -AlphaId $alpha.alpha_id

        if ($submitResult -and $submitResult.success) {
            Write-Host "  SUCCESS: $($alpha.alpha_id) submitted!" -ForegroundColor Green
        } else {
            Write-Host "  BLOCKED: $($alpha.alpha_id) - $($submitResult.blocked)" -ForegroundColor Yellow
        }

        Start-Sleep -Seconds 2
    }
}

# ---- 自动检查 ProdCorr ----
if ($AutoCheckCorr -and $raPassedAlphas.Count -gt 0) {
    Write-Host "`n[AUTO-CORR] Checking ProdCorr for $($raPassedAlphas.Count) alphas..." -ForegroundColor Magenta

    foreach ($alpha in $raPassedAlphas) {
        $corrResult = Check-Correlation -AlphaId $alpha.alpha_id
        if ($corrResult) {
            $prodCorr = $corrResult.prod_corr
            $color = if ($prodCorr -lt 0.7) { "Green" } else { "Yellow" }
            Write-Host "  $($alpha.alpha_id): ProdCorr=$prodCorr" -ForegroundColor $color
        }
        Start-Sleep -Seconds 2
    }
}

Write-Host "`nDone!`n" -ForegroundColor Green

# ---- 辅助函数 ----
function Print-BatchResults {
    param($Results)
    if (-not $Results) { return }
    foreach ($r in $Results) {
        $status = if ($r.ra_passed) { "PASS" } else { "FAIL" }
        $color = if ($r.ra_passed) { "Green" } else { "Red" }
        Write-Host ("  {0}: Sharpe={1} [{2}]" -f $r.alpha_id, $r.metrics.sharpe, $status) -ForegroundColor $color
    }
}
