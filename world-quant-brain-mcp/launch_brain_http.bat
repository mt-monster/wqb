@echo off
REM =====================================================================
REM 子启动脚本：wq-brain-http (MCP HTTP, 端口 8000)
REM 由 start_mcp_http_servers.bat 以 start /min 方式拉起，独立窗口、脱离父进程。
REM 所有输出（含崩溃堆栈）重定向到 logs\brain_http_8000.log，便于排查。
REM =====================================================================
cd /d "D:\coding\traeCN_project\wqb\world-quant-brain-mcp"

set MCP_TRANSPORT=streamable-http
set MCP_HOST=127.0.0.1
set MCP_PORT=8000
set WQB_ALLOW_ALPHA_SUBMIT=1
set WQB_ASI_UNIVERSE_FIX=20260916
set WQ_TOOLKIT_DIR=D:\coding\traeCN_project\wqb\Claude\skills\wq-brain-campaign-toolkit\scripts
set WQ_VALIDATOR_DIR=D:\coding\traeCN_project\wqb\Claude\skills\alpha-expression-verifier\scripts

set LOGDIR=D:\coding\traeCN_project\wqb\world-quant-brain-mcp\logs
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe" "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\main.py" >> "%LOGDIR%\brain_http_8000.log" 2>&1
