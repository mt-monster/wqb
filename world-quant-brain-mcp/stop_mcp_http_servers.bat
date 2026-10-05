@echo off
REM =====================================================================
REM 停止 wq-brain-http (8000) 与 wqb-db (8001) 两个 MCP HTTP 服务。
REM 通过 netstat 找到监听对应端口的 PID 并 taskkill。
REM =====================================================================
echo 正在停止 MCP HTTP 服务（8000 / 8001）...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8000" ^| findstr "LISTENING"') do taskkill /PID %%a /F >nul 2>&1
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":8001" ^| findstr "LISTENING"') do taskkill /PID %%a /F >nul 2>&1
echo 完成。若仍有残留，请到任务管理器结束 python.exe（对应 main.py / wqb_db_mcp.py）。
pause
