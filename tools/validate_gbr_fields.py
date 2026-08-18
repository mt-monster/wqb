#!/usr/bin/env python3
"""
GBR 区域字段验证脚本
在提交 alpha 表达式前验证所有字段在 GBR 区域是否存在
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Dict, Set

# 添加 MCP 目录到路径
MCP_DIR = Path(__file__).parent.parent / "world-quant-brain-mcp"
sys.path.insert(0, str(MCP_DIR))

from main import brain_client as bc


class GBRFieldValidator:
    """GBR 区域字段验证器"""
    
    def __init__(self):
        self.region = "GBR"
        self.universe = "TOP700"
        self.delay = 1
        self.instrument_type = "EQUITY"
        self.validated_fields: Set[str] = set()
        self.invalid_fields: Set[str] = set()
        
    async def validate_field(self, field_name: str) -> bool:
        """
        验证单个字段在 GBR 区域是否存在
        
        Args:
            field_name: 字段名称
            
        Returns:
            bool: 字段是否存在
        """
        try:
            # 使用 get_datafields API 搜索字段
            response = await bc.get_datafields(
                instrument_type=self.instrument_type,
                region=self.region,
                universe=self.universe,
                delay=self.delay,
                search_term=field_name,
                limit=10
            )
            
            # 检查是否有匹配的字段
            results = response.get('results', [])
            for field in results:
                if field.get('id') == field_name:
                    self.validated_fields.add(field_name)
                    return True
            
            # 如果没有精确匹配，字段不存在
            self.invalid_fields.add(field_name)
            return False
            
        except Exception as e:
            print(f"验证字段 {field_name} 时出错: {e}")
            self.invalid_fields.add(field_name)
            return False
    
    async def validate_fields_from_expressions(self, expressions: List[str]) -> Dict:
        """
        从表达式列表中提取并验证所有字段
        
        Args:
            expressions: alpha 表达式列表
            
        Returns:
            Dict: 验证结果
        """
        # 提取所有字段名
        all_fields = set()
        for expr in expressions:
            fields = self._extract_fields_from_expression(expr)
            all_fields.update(fields)
        
        print(f"从 {len(expressions)} 个表达式中提取到 {len(all_fields)} 个唯一字段")
        
        # 验证每个字段
        validation_results = {}
        for field in sorted(all_fields):
            print(f"验证字段: {field}")
            is_valid = await self.validate_field(field)
            validation_results[field] = is_valid
            
            # 添加延迟以避免请求过快
            await asyncio.sleep(0.5)
        
        return {
            "total_fields": len(all_fields),
            "valid_fields": len(self.validated_fields),
            "invalid_fields": len(self.invalid_fields),
            "validation_results": validation_results,
            "invalid_field_list": list(self.invalid_fields),
            "valid_field_list": list(self.validated_fields)
        }
    
    def _extract_fields_from_expression(self, expression: str) -> Set[str]:
        """
        从表达式中提取字段名
        
        Args:
            expression: alpha 表达式
            
        Returns:
            Set[str]: 字段名集合
        """
        import re
        
        # 匹配可能的字段名模式
        # 通常字段名包含字母、数字、下划线，可能以特定前缀开头
        field_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        
        # 排除常见的函数名和关键字
        excluded_words = {
            'rank', 'add', 'subtract', 'multiply', 'divide', 'ts_rank', 'ts_delta',
            'ts_zscore', 'ts_decay_linear', 'ts_backfill', 'group_zscore', 'group_rank',
            'normalize', 'scale', 'quantile', 'vec_avg', 'vec_max', 'vec_min',
            'and', 'or', 'not', 'if', 'else', 'true', 'false', 'null',
            'subindustry', 'industry', 'sector', 'country', 'region'
        }
        
        fields = set()
        matches = re.findall(field_pattern, expression)
        
        for match in matches:
            # 过滤掉函数名和关键字
            if match.lower() not in excluded_words:
                # 检查是否像字段名（通常包含数字或特定前缀）
                if any(char.isdigit() for char in match) or match.startswith(('mdl', 'anl', 'nws', 'fnd', 'pv', 'ts_')):
                    fields.add(match)
        
        return fields
    
    def save_validation_report(self, report: Dict, output_file: str):
        """
        保存验证报告到文件
        
        Args:
            report: 验证报告
            output_file: 输出文件路径
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"验证报告已保存到: {output_file}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GBR 区域字段验证")
    parser.add_argument("--expressions-file", required=True, help="包含 alpha 表达式的文件路径")
    parser.add_argument("--output", default="gbr_field_validation_report.json", help="输出报告文件路径")
    parser.add_argument("--batch-size", type=int, default=5, help="每批验证的字段数量")
    
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
    
    print(f"开始验证 {len(expressions)} 个表达式中的字段...")
    
    # 创建验证器
    validator = GBRFieldValidator()
    
    # 验证字段
    report = await validator.validate_fields_from_expressions(expressions)
    
    # 保存报告
    validator.save_validation_report(report, args.output)
    
    # 打印摘要
    print("\n=== 字段验证摘要 ===")
    print(f"总字段数: {report['total_fields']}")
    print(f"有效字段: {report['valid_fields']}")
    print(f"无效字段: {report['invalid_fields']}")
    
    if report['invalid_fields'] > 0:
        print(f"\n无效字段列表:")
        for field in report['invalid_field_list']:
            print(f"  - {field}")
        print(f"\n建议: 请移除或替换这些无效字段后再提交")
        return 1
    else:
        print(f"\n✅ 所有字段验证通过！可以安全提交")
        return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
