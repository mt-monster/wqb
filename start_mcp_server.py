#!/usr/bin/env python3
"""
WorldQuant BRAIN MCP Server Launcher
启动 MCP 服务并自动配置 Claude
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class MCPServerLauncher:
    def __init__(self):
        # 2026-09-05：路径改为基于本文件推导，不再硬编码盘符
        self.repo_root = Path(__file__).resolve().parent
        self.mcp_dir = self.repo_root / "world-quant-brain-mcp"
        self.venv_python = self.mcp_dir / ".venv" / "Scripts" / "python.exe"
        self.main_script = self.mcp_dir / "main.py"
        self.db_mcp_python = self.repo_root / ".venv" / "Scripts" / "python.exe"
        self.db_mcp_script = self.repo_root / "wqb_db_mcp.py"
        self.config_dir = Path.home() / "AppData" / "Roaming" / "Claude"

    def check_environment(self):
        """Check if MCP environment is properly set up"""
        print("\n" + "="*70)
        print("🔍 检查环境 (Checking environment)")
        print("="*70 + "\n")

        # Check MCP directory
        if not self.mcp_dir.exists():
            print(f"✗ MCP 目录不存在: {self.mcp_dir}")
            return False
        print(f"✓ MCP 目录: {self.mcp_dir}")

        # Check main.py
        if not self.main_script.exists():
            print(f"✗ main.py 不存在: {self.main_script}")
            return False
        print(f"✓ 启动脚本: {self.main_script}")

        # Check Python
        if not self.venv_python.exists():
            print(f"⚠ 虚拟环境不存在: {self.venv_python}")
            print("  使用系统 Python...")
            self.venv_python = Path(sys.executable)
        else:
            print(f"✓ Python 环境: {self.venv_python}")

        # Check .env
        env_file = self.mcp_dir / ".env"
        if not env_file.exists():
            print(f"✗ .env 不存在: {env_file}")
            print("  请创建 .env 文件并配置凭证")
            return False
        print(f"✓ 配置文件: {env_file}")

        # Check requirements
        req_file = self.mcp_dir / "requirements.txt"
        if not req_file.exists():
            print(f"✗ requirements.txt 不存在")
            return False
        print(f"✓ 依赖文件: {req_file}")

        return True

    def check_redis(self):
        """Check if Redis is available"""
        print("\n检查 Redis...")
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=2)
            r.ping()
            print("✓ Redis 可用")
            return True
        except Exception as e:
            print(f"✗ Redis 不可用: {e}")
            print("  提示: 请启动 Redis (redis-server)")
            return False

    def generate_claude_config(self):
        """Generate Claude configuration"""
        print("\n生成 Claude 配置...")

        config_file = self.config_dir / "claude_desktop_config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # 服务器名必须是 wq-brain-http / wqb-db：所有 skill 调用的工具前缀是
        # mcp__wq-brain-http__* 与 mcp__wqb-db__*（2026-09-05 修复，此前写的
        # "wq-brain-mcp" 会让全部 skill 工具引用失配，且完全没装 wqb-db）。
        servers = {
            "wq-brain-http": {
                "command": str(self.venv_python),
                "args": [str(self.main_script)],
                "env": {"MCP_TRANSPORT": "stdio"},
                "disabled": False,
                "alwaysAllow": [
                    "authenticate",
                    "get_user_profile",
                    "get_datasets",
                    "create_multi_simulation",
                    "check_correlation",
                    "submit_verdict"
                ]
            }
        }
        if self.db_mcp_script.exists():
            db_python = self.db_mcp_python if self.db_mcp_python.exists() else Path(sys.executable)
            servers["wqb-db"] = {
                "command": str(db_python),
                "args": [str(self.db_mcp_script)],
                "env": {"MCP_TRANSPORT": "stdio"},
                "disabled": False,
            }
        else:
            print(f"⚠ 未找到 {self.db_mcp_script}，跳过 wqb-db 注册（台账类 skill 将不可用）")

        mcp_config = {"mcpServers": servers}

        # Try to merge with existing config
        if config_file.exists():
            with open(config_file, 'r') as f:
                existing = json.load(f)
                existing.setdefault("mcpServers", {})
                # 清理历史错误命名，避免同一服务器留两份
                existing["mcpServers"].pop("wq-brain-mcp", None)
                existing["mcpServers"].update(servers)
            mcp_config = existing
            print(f"✓ 更新现有配置: {config_file}")
        else:
            print(f"✓ 创建新配置: {config_file}")

        # Write config
        with open(config_file, 'w') as f:
            json.dump(mcp_config, f, indent=2, ensure_ascii=False)

        print(f"✓ Claude 配置已保存")
        print(f"  配置文件: {config_file}")

        return config_file

    def show_startup_instructions(self):
        """Show instructions to start the server"""
        print("\n" + "="*70)
        print("🚀 启动 MCP 服务器")
        print("="*70 + "\n")

        print("选择启动方式:\n")

        print("方案 1: 直接运行 (开发用)")
        print("-" * 70)
        print(f"cd {self.mcp_dir}")
        print(f"{self.venv_python} main.py")
        print("")

        print("方案 2: 后台运行 (生产用)")
        print("-" * 70)
        print(f"cd {self.mcp_dir}")
        print(f"pythonw.exe {self.venv_python} main.py")
        print("")

        print("方案 3: 作为 Windows 服务")
        print("-" * 70)
        print(f"nssm install WQBrainMCP {self.venv_python} {self.main_script}")
        print("nssm start WQBrainMCP")
        print("")

    def show_verification_steps(self):
        """Show how to verify installation"""
        print("\n" + "="*70)
        print("✅ 验证安装")
        print("="*70 + "\n")

        print("1. 启动 MCP 服务器")
        print("   python main.py")
        print("")

        print("2. 完全关闭 Claude 应用")
        print("   (检查任务管理器确保完全退出)")
        print("")

        print("3. 重新打开 Claude")
        print("   应该能看到 MCP 工具已连接")
        print("")

        print("4. 在 Claude 中测试工具")
        print('   输入: "使用 authenticate 工具进行身份验证"')
        print("")

        print("5. 验证工具列表")
        print('   输入: "列出我可用的 MCP 工具"')
        print("")

        print("预期输出示例:")
        print("-" * 70)
        print("""
{
  "authenticated": true,
  "user_id": "your_user_id",
  "email": "mthyzx@126.com",
  "available_tools": 52
}
""")

    def save_startup_script(self):
        """Save a batch script for easy startup"""
        startup_script = self.mcp_dir / "start_mcp.bat"

        script_content = f"""@echo off
REM Start WorldQuant BRAIN MCP Server

cd /d "{self.mcp_dir}"

echo Starting MCP Server...
echo.

python main.py

if %errorlevel% neq 0 (
    echo.
    echo Error: MCP server failed to start
    echo Check:
    echo   1. .env file has valid BRAIN credentials
    echo   2. Redis is running (redis-server)
    echo   3. Python dependencies are installed
    pause
)
"""

        with open(startup_script, 'w') as f:
            f.write(script_content)

        print(f"\n✓ 启动脚本已保存: {startup_script}")
        print(f"  可直接双击运行!")

    def run(self):
        """Run the launcher"""
        print("\n" + "🚀 "*20)
        print("WorldQuant BRAIN MCP 服务器安装助手")
        print("WorldQuant BRAIN MCP Server Installer")
        print("🚀 "*20 + "\n")

        # Check environment
        if not self.check_environment():
            print("\n✗ 环境检查失败")
            return False

        # Check Redis
        redis_ok = self.check_redis()

        # Generate Claude config
        config_file = self.generate_claude_config()

        # Show instructions
        self.show_startup_instructions()

        # Save startup script
        self.save_startup_script()

        # Show verification
        self.show_verification_steps()

        print("\n" + "="*70)
        print("📋 总结 (Summary)")
        print("="*70)
        print(f"✓ MCP 目录: {self.mcp_dir}")
        print(f"✓ Claude 配置: {config_file}")
        print(f"{'✓' if redis_ok else '⚠'} Redis: {'就绪' if redis_ok else '需要启动'}")
        print("\n✓ 安装完成! 可以启动 MCP 服务器了")
        print("="*70 + "\n")

        return True

def main():
    try:
        launcher = MCPServerLauncher()
        success = launcher.run()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
