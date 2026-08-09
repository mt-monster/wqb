# ===========================================================================
# WQB Quick Start - 快速启动示例
# 演示如何使用优化后的回测系统
# ===========================================================================
# 运行方式:
#   .\wqb_quickstart.ps1
# ===========================================================================

$ErrorActionPreference = "Stop"

# 加载核心模块
. "d:\coding\traeCN_project\wqb\wqb-share-03\wqb_mcp_core.ps1"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  WQB Quick Start Demo" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ---- 示例1: 7个表达式一批, 串行提交 ----
Write-Host "=== Example 1: Single batch (7 expressions, serial) ===`n" -ForegroundColor Yellow

$expressions = @(
    # other566 变体 (基于 3qePVw3Z 配方)
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 3), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 2), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 4), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 5), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r5_label, subindustry), 0.5), 3), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, sector), 0.5), 3), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 3), 20)"
)

$settings = @{
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

# 方式A: 直接调用核心函数
$results = Submit-SimulationBatch -Expressions $expressions -Settings $settings -BatchId "demo_b1"

Write-Host "`n--- Results ---" -ForegroundColor Cyan
if ($results) {
    $raPassed = $results | Where-Object { $_.ra_passed }
    Write-Host "RA passed: $($raPassed.Count)/$($results.Count)" -ForegroundColor $(if($raPassed.Count -gt 0){"Green"}else{"Yellow"})
}

# ---- 示例2: 通过 batch runner 脚本运行 (支持更多表达式自动分批) ----
Write-Host "`n`n=== Example 2: Batch runner (14 expressions, auto-split into 2 batches) ===`n" -ForegroundColor Yellow

# 将14个表达式写入文件, runner 自动分2批(每批7)
$moreExpressions = @(
    # shortinterest3 变体
    "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(shrt3_bar), subindustry), 0.5), 3), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(shrt3_bar), subindustry), 0.5), 5), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(shrt3_bar), subindustry), 0.5), 7), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(shrt3_bar), subindustry), 0.5), 3), 20)",
    "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(shrt3_bar), sector), 0.5), 3), 10)",
    "ts_decay_linear(signed_power(subtract(rank(vec_avg(shrt3_bar)), 0.5), 3), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(vec_avg(shrt3_utilizationpercent_units), subindustry), 0.5), 3), 10)",
    # 更多 other566 变体
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 7), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 11), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 3), 5)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r5_label, subindustry), 0.5), 5), 10)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r5_label, subindustry), 0.5), 7), 20)",
    "ts_decay_linear(signed_power(subtract(group_rank(oth566_l2r20_label, subindustry), 0.5), 3), 30)",
    "ts_decay_linear(signed_power(subtract(rank(oth566_l2r20_label), 0.5), 3), 10)"
)

$exprFile = "d:\coding\traeCN_project\wqb\wqb-share-03\tracking\demo_expressions.json"
$moreExpressions | ConvertTo-Json -Depth 5 | Out-File -FilePath $exprFile -Encoding UTF8
Write-Host "Expressions written to: $exprFile"
Write-Host "Run: .\wqb_batch_runner.ps1 -ExpressionFile '$exprFile' -BatchPrefix 'demo_b2'`n"

# ---- 示例3: 流水线模式 (多批并行) ----
Write-Host "=== Example 3: Pipeline mode (2 batches concurrent) ===`n" -ForegroundColor Yellow
Write-Host "Run: .\wqb_batch_runner.ps1 -ExpressionFile '$exprFile' -BatchPrefix 'demo_b3' -Pipeline -PipelineDepth 2`n"

# ---- 示例4: 自动提交 + ProdCorr 检查 ----
Write-Host "=== Example 4: Auto-submit + ProdCorr check ===`n" -ForegroundColor Yellow
Write-Host "Run: .\wqb_batch_runner.ps1 -ExpressionFile '$exprFile' -BatchPrefix 'demo_b4' -AutoSubmit -AutoCheckCorr`n"

# ---- 示例5: 检查已有 alpha 的 ProdCorr ----
Write-Host "=== Example 5: Check ProdCorr for existing alpha ===`n" -ForegroundColor Yellow
Write-Host "# Load core module first:"
Write-Host "# . .\wqb_mcp_core.ps1"
Write-Host "# Submit-AlphaForProdCorr -AlphaId 'A17oXw3g'"
Write-Host "# Check-Correlation -AlphaId 'A17oXw3g'"
Write-Host "# Get-AlphaDetails -AlphaId 'A17oXw3g'`n"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Quick start complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
