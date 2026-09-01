#!/usr/bin/env python3
"""
GBR 区域批次隔离测试脚本
用于小批次测试新字段，确认无误后再加入大批次
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import List, Dict

# Windows 终端 GBK 兜底：强制 stdout/stderr 走 UTF-8
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 添加 MCP 目录到路径
MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))

from main import brain_client as bc


class GBRBatchIsolationTester:
    """GBR 区域批次隔离测试器"""
    
    def __init__(self):
        self.region = "GBR"
        self.universe = "TOP700"
        self.delay = 1
        self.instrument_type = "EQUITY"
        self.neutralization = "SUBINDUSTRY"
        self.test_results = []
        
    async def test_single_expression(self, expression: str, test_name: str = "") -> Dict:
        """
        测试单个表达式
        
        Args:
            expression: alpha 表达式
            test_name: 测试名称
            
        Returns:
            Dict: 测试结果
        """
        print(f"测试表达式: {expression}")
        
        try:
            # 创建单个模拟
            payload = {
                "type": "REGULAR",
                "settings": {
                    "instrumentType": self.instrument_type,
                    "region": self.region,
                    "universe": self.universe,
                    "delay": self.delay,
                    "decay": 4.0,
                    "truncation": 0.08,
                    "neutralization": self.neutralization,
                    "pasteurization": "ON",
                    "unitHandling": "VERIFY",
                    "nanHandling": "ON",
                    "language": "FASTEXPR",
                    "testPeriod": "P0Y0M",
                    "visualization": False,
                },
                "regular": expression
            }
            
            # 提交模拟
            response = await bc._request("POST", f"{bc.base_url}/simulations", json=payload)
            data = response.json()
            
            sim_id = data.get("id", "") or data.get("location", "")
            alpha_id = data.get("alpha", "") or data.get("alphaId", "")
            
            result = {
                "test_name": test_name,
                "expression": expression,
                "sim_id": sim_id,
                "alpha_id": alpha_id,
                "status": "SUBMITTED",
                "error": None,
                "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print(f"  → 提交成功: sim_id={sim_id}, alpha_id={alpha_id}")
            
            # 等待一段时间让模拟开始运行
            await asyncio.sleep(5)
            
            # 检查模拟状态
            if sim_id:
                status_result = await self._check_simulation_status(sim_id)
                result.update(status_result)
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"  → 提交失败: {error_msg}")
            
            return {
                "test_name": test_name,
                "expression": expression,
                "sim_id": None,
                "alpha_id": None,
                "status": "ERROR",
                "error": error_msg,
                "submitted_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    async def _check_simulation_status(self, sim_id: str) -> Dict:
        """
        检查模拟状态
        
        Args:
            sim_id: 模拟ID
            
        Returns:
            Dict: 状态信息
        """
        try:
            response = await bc._request("GET", f"{bc.base_url}/simulations/{sim_id}")
            data = response.json()
            
            status = data.get("status", "UNKNOWN")
            progress = data.get("progress", 0)
            
            return {
                "simulation_status": status,
                "progress": progress,
                "status_checked_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {
                "simulation_status": "CHECK_ERROR",
                "status_error": str(e),
                "status_checked_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    async def test_batch_isolation(self, expressions: List[str], batch_size: int = 2) -> List[Dict]:
        """
        批次隔离测试
        
        Args:
            expressions: 表达式列表
            batch_size: 每批测试的表达式数量
            
        Returns:
            List[Dict]: 测试结果列表
        """
        print(f"开始批次隔离测试，每批 {batch_size} 个表达式")
        
        all_results = []
        
        # 按批次分组
        for i in range(0, len(expressions), batch_size):
            batch = expressions[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            print(f"\n=== 测试批次 {batch_num} ===")
            
            # 测试当前批次
            batch_results = []
            for j, expr in enumerate(batch):
                test_name = f"batch_{batch_num}_expr_{j+1}"
                result = await self.test_single_expression(expr, test_name)
                batch_results.append(result)
                
                # 添加延迟避免请求过快
                await asyncio.sleep(2)
            
            all_results.extend(batch_results)
            
            # 检查批次结果
            successful = sum(1 for r in batch_results if r["status"] == "SUBMITTED")
            failed = len(batch_results) - successful
            
            print(f"批次 {batch_num} 结果: {successful} 成功, {failed} 失败")
            
            # 如果批次中有失败的，记录详细信息
            if failed > 0:
                print("失败的表达式:")
                for result in batch_results:
                    if result["status"] != "SUBMITTED":
                        print(f"  - {result['expression']}: {result.get('error', 'Unknown error')}")
            
            # 批次间延迟
            if i + batch_size < len(expressions):
                print("等待 10 秒后进行下一批次...")
                await asyncio.sleep(10)
        
        self.test_results = all_results
        return all_results
    
    def generate_isolation_report(self, output_file: str):
        """
        生成隔离测试报告
        
        Args:
            output_file: 输出文件路径
        """
        if not self.test_results:
            print("没有测试结果可报告")
            return
        
        # 统计结果
        total_tests = len(self.test_results)
        successful = sum(1 for r in self.test_results if r["status"] == "SUBMITTED")
        failed = total_tests - successful
        
        # 按状态分组
        status_groups = {}
        for result in self.test_results:
            status = result.get("simulation_status", "UNKNOWN")
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(result)
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "successful": successful,
                "failed": failed,
                "success_rate": successful / total_tests if total_tests > 0 else 0
            },
            "status_distribution": {
                status: len(results) for status, results in status_groups.items()
            },
            "detailed_results": self.test_results,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== 隔离测试报告 ===")
        print(f"总测试数: {total_tests}")
        print(f"成功: {successful}")
        print(f"失败: {failed}")
        print(f"成功率: {successful/total_tests*100:.1f}%")
        print(f"\n状态分布:")
        for status, count in report["status_distribution"].items():
            print(f"  {status}: {count}")
        
        print(f"\n详细报告已保存到: {output_file}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GBR 区域批次隔离测试")
    parser.add_argument("--expressions-file", required=True, help="包含 alpha 表达式的文件路径")
    parser.add_argument("--batch-size", type=int, default=2, help="每批测试的表达式数量")
    parser.add_argument("--output", default="gbr_batch_isolation_report.json", help="输出报告文件路径")
    parser.add_argument("--test-mode", choices=["single", "batch"], default="batch", help="测试模式")
    
    args = parser.parse_args()
    
    # 读取表达式文件
    expressions_file = Path(args.expressions_file)
    if not expressions_file.exists():
        print(f"错误: 文件 {expressions_file} 不存在")
        return
    
    expressions = []
    with open(expressions_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                expressions.append(line)
    
    if not expressions:
        print("错误: 文件中没有找到有效的表达式")
        return
    
    print(f"开始批次隔离测试 {len(expressions)} 个表达式...")
    
    # 创建测试器
    tester = GBRBatchIsolationTester()
    
    if args.test_mode == "single":
        # 单个测试模式
        results = []
        for i, expr in enumerate(expressions):
            result = await tester.test_single_expression(expr, f"single_test_{i+1}")
            results.append(result)
            await asyncio.sleep(3)  # 延迟
        
        tester.test_results = results
    else:
        # 批次测试模式
        await tester.test_batch_isolation(expressions, args.batch_size)
    
    # 生成报告
    tester.generate_isolation_report(args.output)
    
    # 返回退出码
    failed_count = sum(1 for r in tester.test_results if r["status"] != "SUBMITTED")
    if failed_count > 0:
        print(f"\n⚠️  有 {failed_count} 个表达式测试失败，建议检查后再提交")
        return 1
    else:
        print(f"\n✅ 所有表达式测试通过！可以安全提交大批次")
        return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
