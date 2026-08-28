#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""convert_alpha_list_to_exprs.py - 将 S2' 的 alpha_list.json 转换为 S3 pipeline 的输入格式

S2' 输出格式（brain-inspectRawTemplate-create-Setting）：
[
  {
    "type": "REGULAR",
    "settings": {"region": "USA", "universe": "TOP3000", ...},
    "regular": "rank(ts_delta(...))"
  },
  ...
]

S3 输入格式（pipeline.py）：
{
  "expressions": ["rank(ts_delta(...))", ...]
}
"""

import json
import sys


def convert_alpha_list_to_exprs(alpha_list_path: str, output_path: str) -> None:
    """将 alpha_list.json 转换为 expressions 格式"""
    
    # 读取 alpha_list.json
    with open(alpha_list_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 支持多种格式：
    # 1. 纯列表：[{...}, {...}]
    # 2. {"alphas": [{...}, {...}]}
    # 3. {"expressions": [...]}
    if isinstance(data, list):
        alpha_list = data
    elif isinstance(data, dict):
        alpha_list = data.get("alphas") or data.get("expressions") or []
    else:
        raise ValueError(f"Expected list or dict in {alpha_list_path}, got {type(data)}")
    
    # 提取表达式
    expressions = []
    for alpha in alpha_list:
        if isinstance(alpha, dict):
            # 优先从 "regular" 字段提取（S2' 标准格式）
            if "regular" in alpha:
                expressions.append(alpha["regular"])
            # 兼容 "expr" 字段（自定义格式）
            elif "expr" in alpha:
                expressions.append(alpha["expr"])
            else:
                print(f"Warning: Skipping alpha entry without 'regular' or 'expr' field: {alpha}")
        elif isinstance(alpha, str):
            # 兼容纯字符串列表
            expressions.append(alpha)
        else:
            print(f"Warning: Skipping invalid alpha entry: {alpha}")
    
    # 写入 expressions 格式
    output = {"expressions": expressions}
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Converted {len(expressions)} expressions from {alpha_list_path} to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_alpha_list_to_exprs.py <alpha_list.json> <output_exprs.json>")
        sys.exit(1)
    
    convert_alpha_list_to_exprs(sys.argv[1], sys.argv[2])
