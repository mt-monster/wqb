@echo off
REM Start WorldQuant BRAIN MCP Server
REM 启动 WorldQuant BRAIN MCP 服务器

setlocal enabledelayedexpansion

echo.
echo ========================================
echo WorldQuant BRAIN MCP Server
echo ========================================
echo.

set MCP_DIR=D:\coding\traeCN_project\wqb\world-quant-brain-mcp
set PYTHON_VENV=!MCP_DIR!\\.venv\Scripts\python.exe

echo 检查环境...
if not exist "!MCP_DIR!" (
    echo 错误: MCP 目录不存在
    echo !MCP_DIR!
    pause
    exit /b 1
)

if not exist "!MCP_DIR!\main.py" (
    echo 错误: main.py 不存在
    pause
    exit /b 1
)

echo ✓ MCP 目录: !MCP_DIR!
echo.

echo 检查依赖...
if exist "!PYTHON_VENV!" (
    echo ✓ 虚拟环境: !PYTHON_VENV!
    set PYTHON_CMD=!PYTHON_VENV!
) else (
    echo ⚠ 虚拟环境不存在，使用系统 Python
    set PYTHON_CMD=python
)

echo.
echo 启动 MCP 服务器...
echo (服务器运行在 http://localhost:8876)
echo.
echo 按 Ctrl+C 停止服务器
echo.

cd /d "!MCP_DIR!"
!PYTHON_CMD! main.py

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo 错误: MCP 服务器启动失败
    echo ========================================
    echo.
    echo 请检查:
    echo   1. .env 文件中的 BRAIN 凭证是否正确
    echo   2. Redis 是否正在运行 (redis-server)
    echo   3. Python 依赖是否已安装 (pip install -r requirements.txt)
    echo.
    pause
    exit /b 1
)
