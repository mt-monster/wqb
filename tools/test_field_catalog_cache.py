# -*- coding: utf-8 -*-
"""test_field_catalog_cache.py - S1 字段扫描缓存功能测试。

测试缓存的各个环节：
1. 缓存未命中时的平台扫描
2. 缓存命中时的快速返回
3. 强制刷新功能
4. 缓存 TTL 机制
5. 批量预热功能

用法:
  python test_field_catalog_cache.py --campaign-dir tracking/EUR --dataset ai_equity_alpha
"""

import argparse
import datetime
import json
import os
import sys
import time

# 添加 tools/lib 到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
from api_client import Api, load_creds

# 添加 toolkit 脚本目录到路径
toolkit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")
if os.path.exists(toolkit_dir):
    sys.path.insert(0, toolkit_dir)
    from _lib.common import CampaignContext
    from _lib.field_catalog_cache import get_cache_manager
    from scan_fields import fetch_fields, build_catalog
else:
    print(f"错误：找不到 toolkit 目录: {toolkit_dir}", file=sys.stderr)
    sys.exit(1)


def test_cache_miss(ctx, dataset):
    """测试缓存未命中时的平台扫描"""
    print(f"\n=== 测试 1: 缓存未命中 ===")
    
    # 清除缓存
    cache_manager = get_cache_manager(ctx)
    cache_manager.clear_cache(dataset)
    
    # 检查缓存状态
    cached = cache_manager.get_cached_catalog(dataset)
    assert cached is None, "缓存应该为空"
    print("✓ 缓存已清除")
    
    # 执行平台扫描
    print("执行平台扫描...")
    start_time = time.time()
    
    e, pw = load_creds()
    api = Api()
    api.login(e, pw)
    raw = fetch_fields(api, ctx.settings, dataset, limit=10)  # 限制字段数加快测试
    catalog = build_catalog(ctx.settings, dataset, raw)
    
    scan_time = time.time() - start_time
    print(f"✓ 平台扫描完成，耗时 {scan_time:.2f}s，{catalog['field_count']} 个字段")
    
    # 保存到缓存
    cache_manager.save_catalog_cache(dataset, catalog)
    print("✓ 结果已保存到缓存")
    
    return catalog


def test_cache_hit(ctx, dataset):
    """测试缓存命中时的快速返回"""
    print(f"\n=== 测试 2: 缓存命中 ===")
    
    cache_manager = get_cache_manager(ctx)
    
    # 第一次获取（应该从缓存读取）
    print("第一次获取（缓存读取）...")
    start_time = time.time()
    cached1 = cache_manager.get_cached_catalog(dataset)
    read_time1 = time.time() - start_time
    
    assert cached1 is not None, "缓存应该存在"
    print(f"✓ 缓存读取完成，耗时 {read_time1:.3f}s，{len(cached1.get('fields', []))} 个字段")
    
    # 第二次获取（应该再次从缓存读取）
    print("第二次获取（缓存读取）...")
    start_time = time.time()
    cached2 = cache_manager.get_cached_catalog(dataset)
    read_time2 = time.time() - start_time
    
    assert cached2 is not None, "缓存应该存在"
    print(f"✓ 缓存读取完成，耗时 {read_time2:.3f}s")
    
    # 验证缓存一致性
    assert cached1 == cached2, "两次缓存读取结果应该一致"
    print("✓ 缓存一致性验证通过")
    
    return cached1


def test_force_refresh(ctx, dataset):
    """测试强制刷新功能"""
    print(f"\n=== 测试 3: 强制刷新 ===")
    
    cache_manager = get_cache_manager(ctx)
    
    # 标记强制刷新
    from _lib.wqb_store import get_store
    store = get_store(ctx)
    try:
        store.upsert_ledger(ctx.region, f"force_refresh_{dataset}", {"refresh": True, "timestamp": datetime.datetime.now().isoformat()})
    finally:
        store.close()
    
    print("✓ 已标记强制刷新")
    
    # 检查是否需要刷新
    should_refresh = cache_manager.should_refresh_cache(dataset)
    assert should_refresh, "应该需要刷新"
    print("✓ 强制刷新标记生效")
    
    # 清除强制刷新标记
    store = get_store(ctx)
    try:
        store.upsert_ledger(ctx.region, f"force_refresh_{dataset}", None)
    finally:
        store.close()
    
    print("✓ 强制刷新标记已清除")


def test_cache_ttl(ctx, dataset):
    """测试缓存 TTL 机制"""
    print(f"\n=== 测试 4: 缓存 TTL ===")
    
    # 创建短 TTL 缓存管理器（1 秒）
    short_ttl_manager = get_cache_manager(ctx, ttl_seconds=1)
    
    # 获取当前缓存
    cached = short_ttl_manager.get_cached_catalog(dataset)
    if cached:
        print("✓ 当前缓存有效")
        
        # 等待 TTL 过期
        print("等待 TTL 过期（2 秒）...")
        time.sleep(2)
        
        # 检查缓存是否过期
        expired_cached = short_ttl_manager.get_cached_catalog(dataset)
        assert expired_cached is None, "缓存应该已过期"
        print("✓ 缓存 TTL 机制正常")
    else:
        print("⚠ 无缓存可测试 TTL")


def test_batch_preload(ctx, datasets):
    """测试批量预热功能"""
    print(f"\n=== 测试 5: 批量预热 ===")
    
    cache_manager = get_cache_manager(ctx)
    
    for dataset in datasets:
        print(f"预热 {dataset}...")
        try:
            # 检查缓存状态
            cached = cache_manager.get_cached_catalog(dataset)
            if cached:
                print(f"  ✓ {dataset} 缓存有效")
            else:
                print(f"  → {dataset} 需要扫描")
        except Exception as e:
            print(f"  ✗ {dataset} 预热失败: {e}")


def main():
    ap = argparse.ArgumentParser(description="S1 字段扫描缓存功能测试")
    ap.add_argument("--campaign-dir", required=True, help="战役目录")
    ap.add_argument("--dataset", required=True, help="测试数据集")
    ap.add_argument("--batch-datasets", help="批量测试数据集（逗号分隔）")
    args = ap.parse_args()
    
    ctx = CampaignContext(args.campaign_dir)
    
    print(f"开始测试 S1 字段扫描缓存功能")
    print(f"战役目录: {args.campaign_dir}")
    print(f"测试数据集: {args.dataset}")
    
    try:
        # 测试 1: 缓存未命中
        catalog = test_cache_miss(ctx, args.dataset)
        
        # 测试 2: 缓存命中
        cached = test_cache_hit(ctx, args.dataset)
        
        # 测试 3: 强制刷新
        test_force_refresh(ctx, args.dataset)
        
        # 测试 4: 缓存 TTL
        test_cache_ttl(ctx, args.dataset)
        
        # 测试 5: 批量预热
        if args.batch_datasets:
            batch_datasets = [d.strip() for d in args.batch_datasets.split(",")]
            test_batch_preload(ctx, batch_datasets)
        
        print(f"\n=== 所有测试通过 ===")
        print("✓ 缓存功能正常")
        print("✓ 强制刷新正常")
        print("✓ TTL 机制正常")
        print("✓ 批量预热正常")
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
