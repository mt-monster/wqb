#!/usr/bin/env python3
"""
MCP 连接验证脚本
验证 MCP 服务器是否正常运行并可被 Claude 访问
"""

import os
import sys
import json
import socket
import subprocess
import time
import requests
from pathlib import Path

class MCPConnectionVerifier:
    def __init__(self):
        self.mcp_dir = Path("D:/coding/traeCN_project/wqb/world-quant-brain-mcp")
        self.mcp_host = "localhost"
        self.mcp_port = 8876
        self.claude_config = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
        self.test_results = {}

    def print_header(self, title):
        """Print section header"""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80 + "\n")

    def check_mcp_config(self):
        """Check if Claude has MCP configuration"""
        self.print_header("1️⃣  检查 Claude MCP 配置")

        if not self.claude_config.exists():
            print(f"✗ Claude 配置文件不存在")
            print(f"  预期位置: {self.claude_config}")
            return False

        try:
            with open(self.claude_config, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if "mcpServers" not in config:
                print("✗ 配置中没有 mcpServers 段")
                return False

            if "wq-brain-http" not in config["mcpServers"]:
                print("✗ 配置中没有 wq-brain-http 服务器")
                return False

            mcp_config = config["mcpServers"]["wq-brain-http"]
            print(f"✓ 找到 MCP 配置")
            print(f"  位置: {self.claude_config}")
            print(f"  服务器: wq-brain-http")
            print(f"  命令: {mcp_config.get('command')}")
            print(f"  脚本: {mcp_config.get('args', [''])[0]}")
            print(f"  启用: {not mcp_config.get('disabled', False)}")

            return True
        except Exception as e:
            print(f"✗ 无法读取配置: {e}")
            return False

    def check_port_available(self):
        """Check if port 8876 is accessible"""
        self.print_header("2️⃣  检查 MCP 端口")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.mcp_host, self.mcp_port))
            sock.close()

            if result == 0:
                print(f"✓ MCP 端口 {self.mcp_port} 已打开")
                print(f"  MCP 服务正在运行!")
                return True
            else:
                print(f"✗ MCP 端口 {self.mcp_port} 未响应")
                print(f"  MCP 服务可能未启动")
                print(f"\n  💡 启动 MCP 服务:")
                print(f"     start_mcp.bat")
                print(f"     或")
                print(f"     cd {self.mcp_dir}")
                print(f"     python main.py")
                return False
        except Exception as e:
            print(f"✗ 端口检查失败: {e}")
            return False

    def test_mcp_connection(self):
        """Test direct connection to MCP server"""
        self.print_header("3️⃣  测试 MCP 服务器连接")

        try:
            url = f"http://{self.mcp_host}:{self.mcp_port}/mcp"
            print(f"连接到: {url}")

            response = requests.get(url, timeout=3)

            if response.status_code == 200:
                print(f"✓ MCP 服务器响应正常 (HTTP {response.status_code})")

                try:
                    data = response.json()
                    print(f"✓ 返回 JSON 数据")
                    print(f"  响应: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"  (响应不是 JSON 格式)")

                return True
            else:
                print(f"⚠ MCP 服务器返回状态码 {response.status_code}")
                return False

        except requests.exceptions.ConnectionError:
            print(f"✗ 无法连接到 MCP 服务器")
            print(f"  {self.mcp_host}:{self.mcp_port}")
            return False
        except Exception as e:
            print(f"✗ 连接测试失败: {e}")
            return False

    def check_mcp_processes(self):
        """Check if MCP processes are running"""
        self.print_header("4️⃣  检查 MCP 进程")

        try:
            # Check for Python processes
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe"],
                capture_output=True,
                text=True
            )

            if "python.exe" in result.stdout:
                print(f"✓ Python 进程正在运行")

                # Try to find main.py
                result2 = subprocess.run(
                    ["tasklist", "/V"],
                    capture_output=True,
                    text=True
                )

                if "main.py" in result2.stdout:
                    print(f"✓ MCP main.py 进程已识别")
                else:
                    print(f"⚠ 找到 Python 进程，但未确认是 MCP")

                return True
            else:
                print(f"✗ 没有 Python 进程运行")
                print(f"  MCP 服务可能未启动")
                return False

        except Exception as e:
            print(f"⚠ 进程检查失败: {e}")
            return False

    def test_redis_connection(self):
        """Check if Redis is accessible"""
        self.print_header("5️⃣  检查 Redis 连接")

        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=2)
            r.ping()
            print(f"✓ Redis 可用 (localhost:6379)")
            return True
        except ImportError:
            print(f"⚠ redis 包未安装")
            print(f"  但这不影响 MCP 服务运行")
            return False
        except Exception as e:
            print(f"✗ Redis 不可达: {e}")
            print(f"  MCP 需要 Redis 来缓存和并发控制")
            return False

    def show_mcp_tools_summary(self):
        """Show MCP tools that should be available"""
        self.print_header("6️⃣  可用的 MCP 工具")

        print("以下工具应该在 Claude 中可用:\n")

        tools_list = {
            "👤 账户与认证": [
                "authenticate",
                "get_user_profile",
                "get_user_activities",
                "get_leaderboard"
            ],
            "🔤 Alpha 管理": [
                "get_alpha_details",
                "batch_get_alpha_metrics",
                "set_alpha_properties",
                "get_user_alphas"
            ],
            "📊 数据与字段": [
                "get_datasets",
                "get_datafields",
                "get_operators",
                "run_selection"
            ],
            "⚡ 仿真引擎": [
                "create_multi_simulation",
                "create_simulation",
                "get_simulation_result",
                "run_diagnostics"
            ],
            "📤 提交与监控": [
                "submit_alpha",
                "get_submission_quota",
                "check_correlation",
                "query_submission_status"
            ]
        }

        total = 0
        for category, tools in tools_list.items():
            print(f"{category} ({len(tools)})")
            for tool in tools:
                print(f"  • {tool}")
            total += len(tools)
            print()

        print(f"总计: {total}+ 个工具")

    def generate_test_script(self):
        """Generate a test script for Claude"""
        self.print_header("7️⃣  Claude 测试脚本")

        test_script = """
在 Claude 中尝试以下操作进行验证:

1. 测试基本连接
   输入: "请调用 authenticate MCP 工具验证身份"
   预期: 返回认证状态和用户信息

2. 获取数据集列表
   输入: "请使用 get_datasets MCP 工具获取可用数据集列表"
   预期: 返回数据集列表

3. 列出所有工具
   输入: "列出所有可用的 WorldQuant BRAIN MCP 工具"
   预期: 显示 50+ 个工具

4. 测试仿真功能
   输入: "使用 create_multi_simulation 工具创建一个测试仿真"
   预期: 返回仿真结果或错误消息

5. 检查工具调用
   输入: "查看最近调用的 MCP 工具有哪些"
   预期: Claude 显示已调用的工具列表
"""
        print(test_script)

    def show_troubleshooting(self):
        """Show troubleshooting guide"""
        self.print_header("❌ 故障排查")

        troubleshooting = """
问题 1: "MCP 端口 8876 未响应"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原因: MCP 服务未启动
解决:
  1. 打开 start_mcp.bat
  2. 或运行: cd world-quant-brain-mcp && python main.py
  3. 等待看到: [INFO] FastMCP server started

问题 2: "MCP 端口占用"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原因: 端口 8876 被其他程序占用
解决:
  1. netstat -ano | findstr :8876
  2. taskkill /PID <PID> /F
  3. 重新启动 MCP

问题 3: "Claude 看不到 MCP 工具"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原因: Claude 缓存或配置未生效
解决:
  1. 完全关闭 Claude (检查任务管理器)
  2. 等待 10 秒
  3. 重新打开 Claude
  4. 等待 15-20 秒让 MCP 连接

问题 4: "Redis connection failed"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原因: Redis 未运行
解决:
  1. redis-server
  2. 或: docker run -d -p 6379:6379 redis

问题 5: "Authentication failed"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
原因: BRAIN 凭证错误或已过期
解决:
  1. 编辑 .env 文件
  2. 检查 CREDENTIALS_EMAIL 和 PASSWORD
  3. 重启 MCP 服务
"""
        print(troubleshooting)

    def run_verification(self):
        """Run complete verification"""
        print("\n" + "🔍 "*40)
        print("WorldQuant BRAIN MCP 连接验证".center(80))
        print("🔍 "*40)

        checks = {
            "Claude MCP 配置": self.check_mcp_config(),
            "MCP 端口可用性": self.check_port_available(),
            "MCP 服务连接": self.test_mcp_connection(),
            "MCP 进程运行": self.check_mcp_processes(),
            "Redis 连接": self.test_redis_connection(),
        }

        self.test_results = checks

        # Show tools summary
        self.show_mcp_tools_summary()

        # Show test script
        self.generate_test_script()

        # Show summary
        self.print_header("📊 验证总结")

        passed = sum(1 for v in checks.values() if v)
        total = len(checks)

        print(f"通过: {passed}/{total}\n")

        for check, result in checks.items():
            status = "✓" if result else "✗"
            print(f"{status} {check}")

        print("\n" + "="*80)

        if passed == total:
            print("✓✓✓ 所有检查通过! MCP 已就绪 ✓✓✓".center(80))
            print("\n你现在可以在 Claude 中使用所有 50+ 个 MCP 工具!")
        elif passed >= 3:
            print("⚠ 部分检查失败,但基本功能应该可用".center(80))
            print("\n请查看上面的故障排查部分")
        else:
            print("✗ 多个检查失败,MCP 可能无法正常工作".center(80))

        print("="*80)

        # Show troubleshooting
        self.show_troubleshooting()

        print("\n" + "="*80)
        print("验证完成".center(80))
        print("="*80 + "\n")

        return passed == total

def main():
    try:
        verifier = MCPConnectionVerifier()
        success = verifier.run_verification()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ 验证出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
