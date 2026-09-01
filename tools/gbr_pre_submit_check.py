#!/usr/bin/env python3
"""
GBR 区域提交前检查脚本
集成字段验证和批次隔离测试，确保安全提交
"""

import asyncio
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict

# Windows 终端 GBK 兜底：强制 stdout/stderr 走 UTF-8
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class GBRPreSubmitChecker:
    """GBR 区域提交前检查器"""
    
    def __init__(self):
        self.tools_dir = Path(__file__).parent
        self.field_validator = self.tools_dir / "validate_gbr_fields.py"
        self.batch_tester = self.tools_dir / "test_gbr_batch_isolation.py"
        
    async def run_field_validation(self, expressions_file: str) -> bool:
        """
        运行字段验证
        
        Args:
            expressions_file: 表达式文件路径
            
        Returns:
            bool: 验证是否通过
        """
        print("=" * 50)
        print("步骤 1: 字段验证")
        print("=" * 50)
        
        try:
            # 运行字段验证脚本
            result = subprocess.run([
                sys.executable, str(self.field_validator),
                "--expressions-file", expressions_file,
                "--output", "gbr_field_validation_report.json"
            ], capture_output=True, text=True, cwd=self.tools_dir)
            
            print(result.stdout)
            if result.stderr:
                print("错误输出:", result.stderr)
            
            # 检查返回码
            if result.returncode == 0:
                print("✅ 字段验证通过")
                return True
            else:
                print("❌ 字段验证失败")
                return False
                
        except Exception as e:
            print(f"运行字段验证时出错: {e}")
            return False
    
    async def run_batch_isolation_test(self, expressions_file: str, batch_size: int = 2) -> bool:
        """
        运行批次隔离测试
        
        Args:
            expressions_file: 表达式文件路径
            batch_size: 批次大小
            
        Returns:
            bool: 测试是否通过
        """
        print("=" * 50)
        print("步骤 2: 批次隔离测试")
        print("=" * 50)
        
        try:
            # 运行批次隔离测试脚本
            result = subprocess.run([
                sys.executable, str(self.batch_tester),
                "--expressions-file", expressions_file,
                "--batch-size", str(batch_size),
                "--output", "gbr_batch_isolation_report.json"
            ], capture_output=True, text=True, cwd=self.tools_dir)
            
            print(result.stdout)
            if result.stderr:
                print("错误输出:", result.stderr)
            
            # 检查返回码
            if result.returncode == 0:
                print("✅ 批次隔离测试通过")
                return True
            else:
                print("❌ 批次隔离测试失败")
                return False
                
        except Exception as e:
            print(f"运行批次隔离测试时出错: {e}")
            return False
    
    def check_validation_report(self, report_file: str = "gbr_field_validation_report.json") -> Dict:
        """
        检查字段验证报告
        
        Args:
            report_file: 报告文件路径
            
        Returns:
            Dict: 报告内容
        """
        report_path = self.tools_dir / report_file
        if report_path.exists():
            with open(report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def check_isolation_report(self, report_file: str = "gbr_batch_isolation_report.json") -> Dict:
        """
        检查批次隔离测试报告
        
        Args:
            report_file: 报告文件路径
            
        Returns:
            Dict: 报告内容
        """
        report_path = self.tools_dir / report_file
        if report_path.exists():
            with open(report_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    async def run_full_check(self, expressions_file: str, batch_size: int = 2) -> bool:
        """
        运行完整的提交前检查
        
        Args:
            expressions_file: 表达式文件路径
            batch_size: 批次大小
            
        Returns:
            bool: 检查是否通过
        """
        print("开始 GBR 区域提交前检查...")
        print(f"表达式文件: {expressions_file}")
        print(f"批次大小: {batch_size}")
        
        # 步骤 1: 字段验证
        field_validation_passed = await self.run_field_validation(expressions_file)
        
        if not field_validation_passed:
            print("\n❌ 字段验证失败，请修复无效字段后重试")
            return False
        
        # 步骤 2: 批次隔离测试
        isolation_test_passed = await self.run_batch_isolation_test(expressions_file, batch_size)
        
        if not isolation_test_passed:
            print("\n❌ 批次隔离测试失败，请检查表达式后重试")
            return False
        
        # 生成最终报告
        await self.generate_final_report(expressions_file)
        
        print("\n" + "=" * 50)
        print("✅ 所有检查通过！可以安全提交到 GBR 区域")
        print("=" * 50)
        
        return True
    
    async def generate_final_report(self, expressions_file: str):
        """
        生成最终检查报告
        
        Args:
            expressions_file: 表达式文件路径
        """
        field_report = self.check_validation_report()
        isolation_report = self.check_isolation_report()
        
        final_report = {
            "check_summary": {
                "expressions_file": expressions_file,
                "field_validation_passed": field_report.get("invalid_fields", 1) == 0,
                "isolation_test_passed": isolation_report.get("test_summary", {}).get("failed", 1) == 0,
                "overall_passed": False
            },
            "field_validation": field_report,
            "batch_isolation": isolation_report,
            "recommendations": [],
            "generated_at": "2026-08-17 10:00:00"
        }
        
        # 计算总体通过状态
        field_ok = final_report["check_summary"]["field_validation_passed"]
        isolation_ok = final_report["check_summary"]["isolation_test_passed"]
        final_report["check_summary"]["overall_passed"] = field_ok and isolation_ok
        
        # 生成建议
        if not field_ok:
            final_report["recommendations"].append("移除或替换无效字段")
        
        if not isolation_ok:
            final_report["recommendations"].append("检查表达式语法和字段组合")
        
        if field_ok and isolation_ok:
            final_report["recommendations"].append("可以安全提交到 GBR 区域")
        
        # 保存最终报告
        with open("gbr_pre_submit_check_report.json", 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n最终检查报告已保存到: gbr_pre_submit_check_report.json")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GBR 区域提交前检查")
    parser.add_argument("--expressions-file", required=True, help="包含 alpha 表达式的文件路径")
    parser.add_argument("--batch-size", type=int, default=2, help="批次隔离测试的批次大小")
    parser.add_argument("--skip-field-validation", action="store_true", help="跳过字段验证")
    parser.add_argument("--skip-isolation-test", action="store_true", help="跳过批次隔离测试")
    
    args = parser.parse_args()
    
    # 检查表达式文件是否存在
    expressions_file = Path(args.expressions_file)
    if not expressions_file.exists():
        print(f"错误: 文件 {expressions_file} 不存在")
        return 1
    
    # 创建检查器
    checker = GBRPreSubmitChecker()
    
    # 运行检查
    if args.skip_field_validation and args.skip_isolation_test:
        print("错误: 不能同时跳过字段验证和批次隔离测试")
        return 1
    
    if args.skip_field_validation:
        print("跳过字段验证，只运行批次隔离测试...")
        success = await checker.run_batch_isolation_test(str(expressions_file), args.batch_size)
    elif args.skip_isolation_test:
        print("跳过批次隔离测试，只运行字段验证...")
        success = await checker.run_field_validation(str(expressions_file))
    else:
        # 运行完整检查
        success = await checker.run_full_check(str(expressions_file), args.batch_size)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
