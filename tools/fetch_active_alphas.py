#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_active_alphas.py — 拉取区域 ACTIVE alpha 列表并缓存到本地

用法:
  python tools/fetch_active_alphas.py --region KOR
  python tools/fetch_active_alphas.py --region USA --force
"""
import argparse
import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def fetch_active_alphas(region, force=False):
    """从平台拉取 ACTIVE alpha 列表"""
    cache_dir = os.path.join(PROJECT_ROOT, 'tracking', region, 'reference')
    cache_path = os.path.join(cache_dir, f'{region.lower()}_active_alphas.json')
    
    if os.path.exists(cache_path) and not force:
        print(f"[CACHE] 已存在: {cache_path}")
        with open(cache_path, encoding='utf-8') as f:
            data = json.load(f)
        print(f"[CACHE] 共 {len(data)} 个 ACTIVE alpha")
        return data
    
    # 从平台拉取 (需要 MCP 集成, 这里用占位实现)
    print(f"[FETCH] 从平台拉取 {region} ACTIVE alpha...")
    print(f"[WARN] 平台拉取功能需要 MCP 集成, 当前为占位实现")
    print(f"[WARN] 请手动从平台导出 ACTIVE alpha 列表到: {cache_path}")
    
    # 占位: 返回空列表
    return []


def main():
    ap = argparse.ArgumentParser(description='拉取区域 ACTIVE alpha 列表')
    ap.add_argument('--region', required=True, help='区域代码 (KOR/USA/EUR...)')
    ap.add_argument('--force', action='store_true', help='强制重新拉取')
    args = ap.parse_args()
    
    fetch_active_alphas(args.region, args.force)


if __name__ == '__main__':
    main()
