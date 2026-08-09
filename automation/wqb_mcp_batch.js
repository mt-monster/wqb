// ===========================================================================
// WQB MCP Batch Runner (JavaScript)
// 在 MCP Exec 沙箱中调用，通过 run_command 执行优化后的 PowerShell 脚本
// ===========================================================================
//
// 用法 (在 Exec 中):
//   const { runBatch, checkStatus, submitAlpha, checkCorr } = await import('./wqb_mcp_batch.js');
//   // 或者直接内联代码:
//   const result = await tools.run_command({ ... });
//
// 核心函数:
//   - submitBatch(expressions, settings, batchId): 提交一批回测
//   - checkBatchStatus(commandId): 检查批次状态
//   - getResults(resultFile): 读取结果文件
//   - submitAlphaForCorr(alphaId): 提交alpha触发ProdCorr
//   - checkProdCorr(alphaId): 检查ProdCorr
//   - getAlphaDetails(alphaId): 获取alpha详情
// ===========================================================================

const POWERSHELL = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe';
const MCP_URL = 'http://127.0.0.1:8876/mcp';
const SESSION_FILE = 'd:\\coding\\traeCN_project\\wqb\\wqb-share-03\\tracking\\.mcp_session';
const TRACKING_DIR = 'd:\\coding\\traeCN_project\\wqb\\wqb-share-03\\tracking';
const BATCH_SIZE = 7;
const CORE_MODULE = 'd:\\coding\\traeCN_project\\wqb\\wqb-share-03\\wqb_mcp_core.ps1';

// ---- 默认回测设置 ----
const DEFAULT_SETTINGS = {
    instrument_type: "EQUITY",
    region: "USA",
    universe: "TOP3000",
    delay: 1,
    decay: 10,
    neutralization: "REVERSION_AND_MOMENTUM",
    truncation: 0.08,
    test_period: "P0Y0M",
    unit_handling: "VERIFY",
    nan_handling: "ON",
    language: "FASTEXPR",
    pasteurization: "ON",
    max_trade: "ON"
};

/**
 * 生成 PowerShell 脚本: 初始化 MCP 会话
 */
function genInitSessionScript() {
    return `
. '${CORE_MODULE}'
$session = Initialize-McpSession
if ($session) { text "SESSION_OK:$session" } else { text "SESSION_FAIL" }
`.trim();
}

/**
 * 生成 PowerShell 脚本: 提交一批回测
 * @param {string[]} expressions - Alpha 表达式数组
 * @param {object} settings - 回测设置
 * @param {string} batchId - 批次 ID
 */
function genSubmitBatchScript(expressions, settings, batchId) {
    const exprArray = expressions.map(e => `'${e.replace(/'/g, "''")}'`).join(', ');
    const settingsObj = Object.entries(settings).map(([k, v]) => `'${k}' = '${v}'`).join('; ');

    return `
. '${CORE_MODULE}'
$expressions = @(${exprArray})
$settings = @{ ${settingsObj} }
$results = Submit-SimulationBatch -Expressions $expressions -Settings $settings -BatchId '${batchId}'
$results | ConvertTo-Json -Depth 20
`.trim();
}

/**
 * 生成 PowerShell 脚本: 提交 alpha 触发 ProdCorr
 */
function genSubmitAlphaScript(alphaId) {
    return `
. '${CORE_MODULE}'
$result = Submit-AlphaForProdCorr -AlphaId '${alphaId}'
$result | ConvertTo-Json -Depth 20
`.trim();
}

/**
 * 生成 PowerShell 脚本: 检查 ProdCorr
 */
function genCheckCorrScript(alphaId) {
    return `
. '${CORE_MODULE}'
$result = Check-Correlation -AlphaId '${alphaId}'
$result | ConvertTo-Json -Depth 20
`.trim();
}

/**
 * 生成 PowerShell 脚本: 获取 alpha 详情
 */
function genGetAlphaScript(alphaId) {
    return `
. '${CORE_MODULE}'
$result = Get-AlphaDetails -AlphaId '${alphaId}'
$result | ConvertTo-Json -Depth 20
`.trim();
}

/**
 * 生成 PowerShell 脚本: 直接调用 MCP HTTP (轻量级，不加载模块)
 * 用于简单的单次调用
 */
function genDirectMcpCallScript(toolName, argsObj) {
    const argsJson = JSON.stringify(argsObj);
    return `
$ErrorActionPreference = "Stop"
$BaseUrl = "${MCP_URL}"
$SessionFile = "${SESSION_FILE}"

$sessionId = $null
if (Test-Path $SessionFile) { $sessionId = (Get-Content $SessionFile -Raw).Trim() }

if (-not $sessionId) {
    $initBody = @{jsonrpc="2.0";method="initialize";params=@{protocolVersion="2024-11-05";capabilities=@{};clientInfo=@{name="wqb-exec";version="1.0"}};id=0} | ConvertTo-Json -Depth 5 -Compress
    $headers = @{'Content-Type'='application/json';'Accept'='application/json, text/event-stream'}
    try {
        $resp = Invoke-WebRequest -Uri $BaseUrl -Method POST -Headers $headers -Body $initBody -UseBasicParsing -TimeoutSec 30
        $sessionId = $resp.Headers["Mcp-Session-Id"]
    } catch [System.Net.WebException] {
        if ($_.Exception.Response) { $sessionId = $_.Exception.Response.Headers["Mcp-Session-Id"] }
    }
    if ($sessionId) {
        $sessionId | Out-File -FilePath $SessionFile -NoNewline -Encoding UTF8
        $notifBody = @{jsonrpc="2.0";method="notifications/initialized"} | ConvertTo-Json -Depth 5 -Compress
        $notifHeaders = @{'Content-Type'='application/json';'Accept'='application/json, text/event-stream';'Mcp-Session-Id'=$sessionId}
        try { Invoke-WebRequest -Uri $BaseUrl -Method POST -Headers $notifHeaders -Body $notifBody -UseBasicParsing -TimeoutSec 10 | Out-Null } catch {}
    }
}

$headers = @{'Content-Type'='application/json';'Accept'='application/json, text/event-stream';'Mcp-Session-Id'=$sessionId}
$reqBody = @{jsonrpc="2.0";method="tools/call";params=@{name="${toolName}";arguments=${argsJson} | ConvertFrom-Json};id=99} | ConvertTo-Json -Depth 20 -Compress

try {
    $resp = Invoke-WebRequest -Uri $BaseUrl -Method POST -Headers $headers -Body $reqBody -UseBasicParsing -TimeoutSec 600
    if ($resp.Content -match '(?s)data: (.+?)(\\n\\n|\\z)') {
        $jsonStr = $matches[1].Trim()
        $json = $jsonStr | ConvertFrom-Json
        $json | ConvertTo-Json -Depth 30
    } else {
        try { $resp.Content | ConvertFrom-Json | ConvertTo-Json -Depth 30 } catch { $resp.Content }
    }
} catch [System.Net.WebException] {
    if ($_.Exception.Response) {
        $statusCode = [int]$_.Exception.Response.StatusCode
        if ($statusCode -eq 401 -or $statusCode -eq 403) {
            Remove-Item $SessionFile -Force -ErrorAction SilentlyContinue
            "SESSION_EXPIRED"
        } else {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $errBody = $reader.ReadToEnd()
            "ERROR:$statusCode:$errBody"
        }
    } else {
        "ERROR:$($_.Exception.Message)"
    }
}
`.trim();
}

// ===========================================================================
// 导出 API (供 Exec 中使用)
// ===========================================================================

/**
 * 提交一批回测 (通过 run_command 执行 PowerShell)
 * @param {string[]} expressions - 最多 7 个表达式
 * @param {object} settings - 回测设置 (可选，使用默认值)
 * @param {string} batchId - 批次 ID
 * @returns {Promise<object>} run_command 的结果
 */
async function submitBatch(expressions, settings = {}, batchId = 'auto') {
    // 确保不超过 batch_size
    if (expressions.length > BATCH_SIZE) {
        text(`WARNING: Truncating ${expressions.length} to ${BATCH_SIZE}`);
        expressions = expressions.slice(0, BATCH_SIZE);
    }

    const mergedSettings = { ...DEFAULT_SETTINGS, ...settings };
    const script = genSubmitBatchScript(expressions, mergedSettings, batchId);

    // 写入临时文件并执行
    const tempScript = `${TRACKING_DIR}\\temp_batch_${Date.now()}.ps1`;
    await tools.run_command({
        command: `Set-Content -Path '${tempScript}' -Value @'\n${script}\n'@ -Encoding UTF8`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    const result = await tools.run_command({
        command: `& '${POWERSHELL}' -NoProfile -ExecutionPolicy Bypass -File '${tempScript}'`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    // 清理临时文件
    await tools.run_command({
        command: `Remove-Item '${tempScript}' -Force -ErrorAction SilentlyContinue`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process'
    });

    return result;
}

/**
 * 自动分批提交 (超过 7 个表达式自动分批)
 * @param {string[]} expressions - 所有表达式
 * @param {object} settings - 回测设置
 * @param {string} prefix - 批次前缀
 * @returns {Promise<array>} 所有批次结果
 */
async function submitBatchAutoSplit(expressions, settings = {}, prefix = 'batch') {
    const allResults = [];
    const batchCount = Math.ceil(expressions.length / BATCH_SIZE);

    text(`Splitting ${expressions.length} expressions into ${batchCount} batch(es) of max ${BATCH_SIZE}`);

    for (let i = 0; i < expressions.length; i += BATCH_SIZE) {
        const batchNum = Math.floor(i / BATCH_SIZE) + 1;
        const batchExprs = expressions.slice(i, i + BATCH_SIZE);
        const batchId = `${prefix}_${batchNum}`;

        text(`\n--- Batch ${batchNum}/${batchCount}: ${batchId} (${batchExprs.length} exprs) ---`);

        const result = await submitBatch(batchExprs, settings, batchId);
        allResults.push({ batchId, result });

        // 批次间间隔
        if (i + BATCH_SIZE < expressions.length) {
            text('Waiting 2s before next batch...');
            await new Promise(r => setTimeout(r, 2000));
        }
    }

    return allResults;
}

/**
 * 提交 alpha 触发 ProdCorr 检查
 */
async function submitAlphaForCorr(alphaId) {
    const script = genSubmitAlphaScript(alphaId);
    const tempScript = `${TRACKING_DIR}\\temp_submit_${alphaId}_${Date.now()}.ps1`;

    await tools.run_command({
        command: `Set-Content -Path '${tempScript}' -Value @'\n${script}\n'@ -Encoding UTF8`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    const result = await tools.run_command({
        command: `& '${POWERSHELL}' -NoProfile -ExecutionPolicy Bypass -File '${tempScript}'`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    await tools.run_command({
        command: `Remove-Item '${tempScript}' -Force -ErrorAction SilentlyContinue`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process'
    });

    return result;
}

/**
 * 检查 ProdCorr
 */
async function checkProdCorr(alphaId) {
    const script = genCheckCorrScript(alphaId);
    const tempScript = `${TRACKING_DIR}\\temp_corr_${alphaId}_${Date.now()}.ps1`;

    await tools.run_command({
        command: `Set-Content -Path '${tempScript}' -Value @'\n${script}\n'@ -Encoding UTF8`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    const result = await tools.run_command({
        command: `& '${POWERSHELL}' -NoProfile -ExecutionPolicy Bypass -File '${tempScript}'`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    await tools.run_command({
        command: `Remove-Item '${tempScript}' -Force -ErrorAction SilentlyContinue`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process'
    });

    return result;
}

/**
 * 获取 alpha 详情
 */
async function getAlphaDetails(alphaId) {
    const script = genGetAlphaScript(alphaId);
    const tempScript = `${TRACKING_DIR}\\temp_details_${alphaId}_${Date.now()}.ps1`;

    await tools.run_command({
        command: `Set-Content -Path '${tempScript}' -Value @'\n${script}\n'@ -Encoding UTF8`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    const result = await tools.run_command({
        command: `& '${POWERSHELL}' -NoProfile -ExecutionPolicy Bypass -File '${tempScript}'`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    await tools.run_command({
        command: `Remove-Item '${tempScript}' -Force -ErrorAction SilentlyContinue`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process'
    });

    return result;
}

/**
 * 直接调用 MCP 工具 (轻量级，不加载完整模块)
 * 用于简单的单次查询
 */
async function callMcpTool(toolName, argsObj) {
    const script = genDirectMcpCallScript(toolName, argsObj);
    const tempScript = `${TRACKING_DIR}\\temp_mcp_${Date.now()}.ps1`;

    await tools.run_command({
        command: `Set-Content -Path '${tempScript}' -Value @'\n${script}\n'@ -Encoding UTF8`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    const result = await tools.run_command({
        command: `& '${POWERSHELL}' -NoProfile -ExecutionPolicy Bypass -File '${tempScript}'`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING_DIR
    });

    await tools.run_command({
        command: `Remove-Item '${tempScript}' -Force -ErrorAction SilentlyContinue`,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process'
    });

    return result;
}

// 导出所有函数
text('WQB MCP Batch module loaded. Available functions: submitBatch, submitBatchAutoSplit, submitAlphaForCorr, checkProdCorr, getAlphaDetails, callMcpTool');
