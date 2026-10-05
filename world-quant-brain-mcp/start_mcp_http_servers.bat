@echo off
REM =====================================================================
REM 启动 wq-brain-http (8000) 与 wqb-db (8001) 两个 MCP HTTP 常驻服务。
REM
REM 背景：WorkBuddy 的 wq-brain-http / wqb-db 连接器已改为 HTTP 连接
REM (type=http，连 http://127.0.0.1:8000/mcp 与 :8001/mcp)。HTTP 模式下
REM 客户端只连 URL、不起进程，因此这两个 Python 服务必须由本机常驻启动。
REM
REM 本文件只是个薄包装：用 Python 启动器（start_mcp_http_servers.py）直接
REM 以 subprocess 拉起两个服务（DETACHED_PROCESS，脱离本窗口常驻），
REM 不再依赖 cmd 的 start（本机双击环境下 start 拉子进程不可靠）。
REM
REM 用法：
REM   双击本文件            -> 启动两服务，自检后等待回车（回车关窗，服务继续）
REM   登录自启(Startup)     -> WQB_MCP_HTTP_Servers.bat 以 "auto" 调用，不阻塞
REM   关闭服务              -> 运行 stop_mcp_http_servers.bat，或任务管理器结束 python
REM =====================================================================

"D:\coding\traeCN_project\wqb\world-quant-brain-mcp\.venv\Scripts\python.exe" "D:\coding\traeCN_project\wqb\world-quant-brain-mcp\start_mcp_http_servers.py" %1
