#!/usr/bin/env python3
"""
MCP 环境验证脚本
验证 WorldQuant BRAIN MCP 是否正确配置
"""

import os
import sys
import json
import subprocess
from pathlib import Path

class MCPVerifier:
    def __init__(self):
        self.mcp_dir = Path("D:/coding/traeCN_project/wqb/world-quant-brain-mcp").absolute()
        self.venv_dir = self.mcp_dir / ".venv"
        self.env_file = self.mcp_dir / ".env"
        self.main_script = self.mcp_dir / "main.py"
        self.claude_config = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"

    def check_mcp_directory(self):
        """Check MCP directory structure"""
        print("\n📂 检查 MCP 目录结构")
        print("-" * 70)

        checks = {
            "MCP 目录": self.mcp_dir,
            "main.py": self.main_script,
            ".env 配置": self.env_file,
            "虚拟环境": self.venv_dir,
            "requirements.txt": self.mcp_dir / "requirements.txt",
        }

        all_ok = True
        for name, path in checks.items():
            if path.exists():
                print(f"✓ {name}: {path}")
            else:
                print(f"✗ {name}: {path} (NOT FOUND)")
                all_ok = False

        return all_ok

    def check_env_config(self):
        """Check .env configuration"""
        print("\n🔐 检查环境配置")
        print("-" * 70)

        if not self.env_file.exists():
            print("✗ .env 文件不存在")
            return False

        try:
            with open(self.env_file, 'r') as f:
                env_content = f.read()

            # Check for credentials
            has_email = "CREDENTIALS_EMAIL" in env_content
            has_password = "CREDENTIALS_PASSWORD" in env_content

            print(f"✓ .env 文件存在")
            print(f"  {'✓' if has_email else '✗'} CREDENTIALS_EMAIL 已配置")
            print(f"  {'✓' if has_password else '✗'} CREDENTIALS_PASSWORD 已配置")

            return has_email and has_password
        except Exception as e:
            print(f"✗ 无法读取 .env: {e}")
            return False

    def check_dependencies(self):
        """Check if Python dependencies are installed"""
        print("\n📦 检查依赖")
        print("-" * 70)

        required_packages = [
            "fastmcp",
            "redis",
            "httpx",
            "pydantic",
        ]

        all_installed = True
        for package in required_packages:
            try:
                __import__(package)
                print(f"✓ {package}")
            except ImportError:
                print(f"✗ {package} (NOT INSTALLED)")
                all_installed = False

        if not all_installed:
            print("\n💡 安装缺失依赖:")
            print(f"   cd {self.mcp_dir}")
            print(f"   pip install -r requirements.txt")

        return all_installed

    def check_redis(self):
        """Check Redis connectivity"""
        print("\n🔄 检查 Redis")
        print("-" * 70)

        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=2)
            r.ping()
            print("✓ Redis 可用 (localhost:6379)")
            return True
        except ImportError:
            print("✗ redis 包未安装")
            return False
        except Exception as e:
            print(f"✗ Redis 不可达: {e}")
            print("\n💡 启动 Redis:")
            print("   redis-server")
            return False

    def check_claude_config(self):
        """Check Claude MCP configuration"""
        print("\n🎨 检查 Claude 配置")
        print("-" * 70)

        if not self.claude_config.exists():
            print(f"✗ Claude 配置文件不存在: {self.claude_config}")
            return False

        try:
            with open(self.claude_config, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if "mcpServers" not in config:
                print("✗ 配置中没有 mcpServers")
                return False

            if "wq-brain-http" not in config["mcpServers"]:
                print("✗ 配置中没有 wq-brain-http")
                return False

            mcp_config = config["mcpServers"]["wq-brain-http"]
            print(f"✓ Claude 配置文件: {self.claude_config}")
            print(f"  ✓ MCP 服务器: wq-brain-http")
            print(f"  ✓ 命令: {mcp_config.get('command')}")
            print(f"  ✓ 脚本: {mcp_config.get('args', [''])[0]}")
            print(f"  ✓ 状态: {'启用' if not mcp_config.get('disabled') else '禁用'}")

            return True
        except Exception as e:
            print(f"✗ 无法读取配置: {e}")
            return False

    def check_port_availability(self):
        """Check if port 8876 is available"""
        print("\n🔌 检查端口")
        print("-" * 70)

        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 8876))
            sock.close()

            if result == 0:
                print("⚠ 端口 8876 已被占用")
                print("  提示: 可能 MCP 已在运行")
                return False
            else:
                print("✓ 端口 8876 可用")
                return True
        except Exception as e:
            print(f"⚠ 无法检查端口: {e}")
            return True

    def show_mcp_tools_summary(self):
        """Show available MCP tools"""
        print("\n🛠️  MCP 工具摘要")
        print("-" * 70)

        tools_summary = {
            "认证与账户": [
                "authenticate",
                "get_user_profile",
                "get_user_activities",
                "get_leaderboard"
            ],
            "Alpha 管理": [
                "get_alpha_details",
                "batch_get_alpha_metrics",
                "set_alpha_properties",
                "get_user_alphas"
            ],
            "数据与字段": [
                "get_datasets",
                "get_datafields",
                "get_operators",
                "run_selection"
            ],
            "仿真": [
                "create_multi_simulation",
                "create_simulation",
                "get_simulation_result",
                "run_diagnostics"
            ],
            "提交与监控": [
                "submit_alpha",
                "get_submission_quota",
                "query_submission_status",
                "check_correlation"
            ],
            "其他": [
                "search_forum_posts",
                "get_glossary_terms",
                "manage_config",
                "operator_audit"
            ]
        }

        total_tools = sum(len(v) for v in tools_summary.values())
        print(f"\n总计: {total_tools} 个工具\n")

        for category, tools in tools_summary.items():
            print(f"{category} ({len(tools)}):")
            for tool in tools:
                print(f"  • {tool}")
            print()

    def run_diagnostics(self):
        """Run complete diagnostics"""
        print("\n" + "="*70)
        print("🔍 WorldQuant BRAIN MCP 环境诊断")
        print("="*70)

        results = {
            "MCP 目录": self.check_mcp_directory(),
            "环境配置": self.check_env_config(),
            "Python 依赖": self.check_dependencies(),
            "Redis": self.check_redis(),
            "Claude 配置": self.check_claude_config(),
            "端口可用性": self.check_port_availability(),
        }

        self.show_mcp_tools_summary()

        # Summary
        print("\n" + "="*70)
        print("📊 诊断总结")
        print("="*70 + "\n")

        passed = sum(1 for v in results.values() if v)
        total = len(results)

        for check, result in results.items():
            status = "✓" if result else "✗"
            print(f"{status} {check}")

        print(f"\n通过: {passed}/{total}\n")

        if passed == total:
            print("✓✓✓ 所有检查通过! 可以启动 MCP 服务器 ✓✓✓\n")
            print("启动命令:")
            print(f"  cd {self.mcp_dir}")
            print(f"  python main.py\n")
            return True
        else:
            print("⚠ 部分检查失败,请按照提示修复\n")
            return False

def main():
    try:
        verifier = MCPVerifier()
        success = verifier.run_diagnostics()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ 诊断出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
