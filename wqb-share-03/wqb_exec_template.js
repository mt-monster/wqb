// ===========================================================================
// WQB MCP Exec Integration (v4)
// 修复: UTF-16LE 编码 + CLIXML 输出清理 + batch_size=8 + pipeline=7
// ===========================================================================
// 用法: 将此文件内容粘贴到 integrated_code_mode Exec 工具的 code 参数
// ===========================================================================
// Exec 沙箱限制: 无 setTimeout, 无 fetch, 无 require, 无 console, 无 btoa
// 可用: tools.run_command(), tools.Read(), tools.LS(), text(), ALL_TOOLS
// ===========================================================================

const PS = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe';
const CORE = 'd:\\coding\\traeCN_project\\wqb\\wqb-share-03\\wqb_mcp_core.ps1';
const TRACKING = 'd:\\coding\\traeCN_project\\wqb\\wqb-share-03\\tracking';
const BATCH_SIZE = 8;

// ---- Base64 编码 (UTF-16LE, PowerShell -EncodedCommand 要求) ----
function base64EncodeUtf16LE(str) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    const bytes = [];
    for (let i = 0; i < str.length; i++) {
        const code = str.charCodeAt(i);
        bytes.push(code & 0xFF);
        bytes.push((code >> 8) & 0xFF);
    }
    let result = '';
    let j = 0;
    while (j < bytes.length) {
        const b1 = bytes[j++];
        const b2 = j < bytes.length ? bytes[j++] : -1;
        const b3 = j < bytes.length ? bytes[j++] : -1;
        result += chars[b1 >> 2];
        result += chars[((b1 & 3) << 4) | (b2 >= 0 ? (b2 >> 4) : 0)];
        result += b2 >= 0 ? chars[((b2 & 15) << 2) | (b3 >= 0 ? (b3 >> 6) : 0)] : '=';
        result += b3 >= 0 ? chars[b3 & 63] : '=';
    }
    return result;
}

// ---- 清理 PowerShell CLIXML 输出 ----
function cleanClixml(stdout) {
    if (!stdout) return '';
    let cleaned = stdout;
    // 移除 CLIXML 前缀
    cleaned = cleaned.replace(/^#<\s*CLIXML\s*/i, '');
    // 移除 CLIXML XML 后缀 (从 <Objs 到结尾)
    const clixmlStart = cleaned.indexOf('<Objs');
    if (clixmlStart > 0) {
        cleaned = cleaned.substring(0, clixmlStart);
    }
    return cleaned.trim();
}

// ---- 核心执行器 ----
async function execPs(psScript) {
    const b64 = base64EncodeUtf16LE(psScript);
    const cmd = `& '${PS}' -NoProfile -ExecutionPolicy Bypass -OutputFormat Text -InputFormat Text -EncodedCommand ${b64}`;
    const result = await tools.run_command({
        command: cmd,
        blocking: true,
        requires_approval: false,
        target_terminal: 'new',
        command_type: 'short_running_process',
        cwd: TRACKING
    });
    // 清理 CLIXML
    if (result.stdout) {
        result.cleanedStdout = cleanClixml(result.stdout);
    }
    return result;
}

// ---- 从清理后的输出中提取 JSON ----
function extractJson(cleanedStdout) {
    if (!cleanedStdout) return null;
    // 尝试整段解析
    try {
        return JSON.parse(cleanedStdout);
    } catch (e) {}
    // 尝试找到 JSON 块
    const lines = cleanedStdout.split('\n');
    let braceCount = 0, inJson = false, jsonLines = [];
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!inJson && (line.startsWith('{') || line.startsWith('['))) {
            inJson = true;
            jsonLines = [];
        }
        if (inJson) {
            jsonLines.push(lines[i]);
            for (let j = 0; j < line.length; j++) {
                if (line[j] === '{' || line[j] === '[') braceCount++;
                if (line[j] === '}' || line[j] === ']') braceCount--;
            }
            if (braceCount <= 0 && jsonLines.length > 0) {
                try {
                    return JSON.parse(jsonLines.join('\n'));
                } catch (e) {
                    inJson = false;
                    jsonLines = [];
                }
            }
        }
    }
    return null;
}

// ===========================================================================
// API 函数
// ===========================================================================

// ---- 1. 提交一批回测 (最多7个, 自动强制) ----
async function submitBatch(expressions, settings, batchId) {
    if (expressions.length > BATCH_SIZE) {
        text(`WARNING: ${expressions.length} > ${BATCH_SIZE}, truncating`);
        expressions = expressions.slice(0, BATCH_SIZE);
    }
    const exprArr = expressions.map(e => `'${e.replace(/'/g, "''")}'`).join(', ');
    const setArr = Object.entries(settings).map(([k, v]) => `'${k}' = '${v}'`).join('; ');

    const psScript = `. '${CORE}'
$ErrorActionPreference = 'Continue'
$expressions = @(${exprArr})
$settings = @{ ${setArr} }
$results = Submit-SimulationBatch -Expressions $expressions -Settings $settings -BatchId '${batchId}'
if ($results) { $results | ConvertTo-Json -Depth 20 } else { Write-Output '{"error":"no_results"}' }`;

    text(`[submitBatch] ${batchId}: ${expressions.length} exprs...`);
    const result = await execPs(psScript);
    const parsed = extractJson(result.cleanedStdout);
    if (parsed) {
        if (Array.isArray(parsed)) {
            const raPassed = parsed.filter(a => a.ra_passed).length;
            text(`[submitBatch] Got ${parsed.length} results, ${raPassed} RA-passed`);
        } else if (parsed.error) {
            text(`[submitBatch] Error: ${parsed.error}`);
        }
    } else {
        text(`[submitBatch] Parse failed. Last 300 chars: ${result.cleanedStdout.slice(-300)}`);
    }
    return { raw: result, parsed: parsed, stdout: result.cleanedStdout };
}

// ---- 2. 自动分批提交 (超过7个自动拆分) ----
async function submitAll(expressions, settings, prefix) {
    const batchCount = Math.ceil(expressions.length / BATCH_SIZE);
    text(`Splitting ${expressions.length} expressions into ${batchCount} batch(es)`);
    const allResults = [];
    for (let i = 0; i < expressions.length; i += BATCH_SIZE) {
        const batchNum = Math.floor(i / BATCH_SIZE) + 1;
        const batchExprs = expressions.slice(i, i + BATCH_SIZE);
        const batchId = `${prefix}_${batchNum}`;
        text(`\n--- Batch ${batchNum}/${batchCount}: ${batchId} ---`);
        const result = await submitBatch(batchExprs, settings, batchId);
        allResults.push({ batchId, result });
    }
    text(`\n=== Complete: ${allResults.length} batches ===`);
    return allResults;
}

// ---- 3. 提交 alpha 触发 ProdCorr ----
async function submitAlpha(alphaId) {
    const psScript = `. '${CORE}'
$ErrorActionPreference = 'Continue'
$result = Submit-AlphaForProdCorr -AlphaId '${alphaId}'
if ($result) { $result | ConvertTo-Json -Depth 20 } else { Write-Output '{"error":"no_result"}' }`;

    text(`[submitAlpha] ${alphaId}...`);
    const result = await execPs(psScript);
    const parsed = extractJson(result.cleanedStdout);
    if (parsed) {
        if (parsed.success) text(`[submitAlpha] SUCCESS: ${alphaId}`);
        else if (parsed.blocked) text(`[submitAlpha] BLOCKED: ${alphaId}`);
    }
    return { raw: result, parsed: parsed };
}

// ---- 4. 检查 ProdCorr ----
async function checkCorr(alphaId) {
    const psScript = `. '${CORE}'
$ErrorActionPreference = 'Continue'
$result = Check-Correlation -AlphaId '${alphaId}'
if ($result) { $result | ConvertTo-Json -Depth 20 } else { Write-Output '{"error":"no_result"}' }`;

    text(`[checkCorr] ${alphaId}...`);
    const result = await execPs(psScript);
    const parsed = extractJson(result.cleanedStdout);
    if (parsed && parsed.prod_corr !== undefined) {
        text(`[checkCorr] ${alphaId}: ProdCorr=${parsed.prod_corr} [${parsed.prod_corr < 0.7 ? 'PASS' : 'HIGH'}]`);
    }
    return { raw: result, parsed: parsed };
}

// ---- 5. 获取 alpha 详情 ----
async function getAlpha(alphaId) {
    const psScript = `. '${CORE}'
$ErrorActionPreference = 'Continue'
$result = Get-AlphaDetails -AlphaId '${alphaId}'
if ($result) { $result | ConvertTo-Json -Depth 20 } else { Write-Output '{"error":"no_result"}' }`;

    text(`[getAlpha] ${alphaId}...`);
    const result = await execPs(psScript);
    return { raw: result, parsed: extractJson(result.cleanedStdout) };
}

// ---- 6. 获取最近 alpha 列表 ----
async function getRecentAlphas(limit) {
    limit = limit || 10;
    const psScript = `. '${CORE}'
$ErrorActionPreference = 'Continue'
$result = Invoke-McpTool -ToolName 'get_user_alphas' -Arguments @{limit=${limit}; offset=0; sort='dateCreated'; order='desc'} -TimeoutSec 60
if ($result -and $result.result -and $result.result.structuredContent) {
    $r = $result.result.structuredContent.result
    if ($r.alphas) { $r.alphas | ConvertTo-Json -Depth 10 }
    elseif ($r.error) { Write-Output ('{"error":"' + $r.error + '"}') }
    else { Write-Output '{"error":"no_alphas"}' }
} else { Write-Output '{"error":"parse_failed"}' }`;

    text(`[getRecentAlphas] limit=${limit}...`);
    const result = await execPs(psScript);
    const parsed = extractJson(result.cleanedStdout);
    if (Array.isArray(parsed)) text(`[getRecentAlphas] Found ${parsed.length}`);
    return { raw: result, parsed: parsed };
}

// ---- 7. 检查 MCP 连通性 ----
async function pingMcp() {
    const psScript = `. '${CORE}'
$ErrorActionPreference = 'Continue'
$session = Get-McpSession
if ($session) { Write-Output ('{"status":"ok","session":"' + $session + '"}') }
else { Write-Output '{"status":"fail"}' }`;
    const result = await execPs(psScript);
    return { raw: result, parsed: extractJson(result.cleanedStdout) };
}

// ---- 8. 完整流程: 回测 -> RA检查 -> ProdCorr提交 ----
async function fullWorkflow(expressions, settings, prefix) {
    text('=== Full Workflow ===\n');
    text('Step 1: Submitting...');
    const batchResults = await submitAll(expressions, settings, prefix);

    const raPassed = [];
    for (const batch of batchResults) {
        if (batch.result.parsed && Array.isArray(batch.result.parsed)) {
            for (const alpha of batch.result.parsed) {
                if (alpha.ra_passed) raPassed.push(alpha);
            }
        }
    }
    text(`\nStep 2: ${raPassed.length} RA-passed`);

    if (raPassed.length > 0) {
        text('\nStep 3: ProdCorr check...');
        for (const alpha of raPassed) {
            text(`\n  ${alpha.alpha_id}...`);
            const submitResult = await submitAlpha(alpha.alpha_id);
            if (submitResult.parsed && submitResult.parsed.success) {
                await checkCorr(alpha.alpha_id);
            }
        }
    }

    text('\n=== Summary ===');
    text(`  Exprs: ${expressions.length} | Batches: ${batchResults.length} | RA-pass: ${raPassed.length}`);
    if (raPassed.length > 0) text(`  Alphas: ${raPassed.map(a => a.alpha_id).join(', ')}`);
    return { batches: batchResults, raPassed };
}

// ---- 默认回测设置 ----
const DEFAULTS = {
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

// ===========================================================================
// 自检
// ===========================================================================
text('=== WQB MCP Exec Integration v4 ===');
text(`Batch size: ${BATCH_SIZE} (platform max: 8, all slots used)`);
text(`Pipeline: 7 batches in parallel`);

text('\n1. MCP connectivity...');
const ping = await pingMcp();
text(`   ${JSON.stringify(ping.parsed)}`);

text('\n2. Functions ready:');
text('   submitBatch(exprs, settings, batchId)  - Max 7 per batch');
text('   submitAll(exprs, settings, prefix)     - Auto-split');
text('   submitAlpha(alphaId)                   - ProdCorr trigger');
text('   checkCorr(alphaId)                     - Check ProdCorr');
text('   getAlpha(alphaId)                      - Alpha details');
text('   getRecentAlphas(limit)                 - Recent list');
text('   pingMcp()                              - Connectivity');
text('   fullWorkflow(exprs, settings, prefix)  - Full pipeline');

text('\n=== Ready ===');
