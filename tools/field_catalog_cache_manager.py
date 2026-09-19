# -*- coding: utf-8 -*-
"""field_catalog_cache_manager.py - S1 字段扫描缓存管理工具。

提供缓存的批量管理功能：
- 批量预热缓存
- 清除指定数据集缓存
- 查看缓存状态
- 强制刷新缓存

用法:
  # 批量预热缓存
  python field_catalog_cache_manager.py --campaign-dir tracking/EUR --preload ai_equity_alpha,model219,news_sentiment
  
  # 清除缓存
  python field_catalog_cache_manager.py --campaign-dir tracking/EUR --clear ai_equity_alpha
  
  # 查看缓存状态
  python field_catalog_cache_manager.py --campaign-dir tracking/EUR --status ai_equity_alpha,model219
  
  # 强制刷新缓存
  python field_catalog_cache_manager.py --campaign-dir tracking/EUR --refresh ai_equity_alpha
"""

import argparse
import datetime
import os
import sys

# 添加 tools/lib 到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

# 添加 toolkit 脚本目录到路径
toolkit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")
if os.path.exists(toolkit_dir):
    sys.path.insert(0, toolkit_dir)
    from _lib.common import CampaignContext
    from _lib.field_catalog_cache import get_cache_manager
else:
    print(f"错误：找不到 toolkit 目录: {toolkit_dir}", file=sys.stderr)
    sys.exit(1)


def preload_caches(ctx, datasets, cache_ttl=86400):
    """批量预热缓存"""
    cache_manager = get_cache_manager(ctx, cache_ttl)
    results = {}
    
    for dataset in datasets:
        print(f"预热 {dataset} 缓存...")
        try:
            # 检查是否需要刷新
            if not cache_manager.should_refresh_cache(dataset):
                print(f"  ✓ {dataset} 缓存有效，跳过")
                results[dataset] = {"status": "skipped", "reason": "cache_valid"}
                continue
            
            # 执行扫描（这里需要调用 scan_fields.py）
            # 由于循环依赖，我们在这里只标记需要刷新
            # 实际的扫描由调用方执行
            print(f"  → {dataset} 需要刷新，请运行 scan_fields.py --dataset {dataset}")
            results[dataset] = {"status": "needs_refresh", "reason": "cache_expired"}
            
        except Exception as e:
            print(f"  ✗ {dataset} 预热失败: {e}")
            results[dataset] = {"status": "error", "error": str(e)}
    
    return results


def clear_cache(ctx, dataset):
    """清除指定数据集缓存"""
    cache_manager = get_cache_manager(ctx)
    try:
        cache_manager.clear_cache(dataset)
        print(f"✓ 已清除 {dataset} 的缓存")
        return True
    except Exception as e:
        print(f"✗ 清除 {dataset} 缓存失败: {e}")
        return False


def get_cache_status(ctx, datasets):
    """获取缓存状态"""
    cache_manager = get_cache_manager(ctx)
    status = {}
    
    for dataset in datasets:
        try:
            cached = cache_manager.get_cached_catalog(dataset)
            if cached:
                cached_at = cached.get("cache_metadata", {}).get("cached_at", "unknown")
                field_count = len(cached.get("fields", []))
                status[dataset] = {
                    "cached": True,
                    "cached_at": cached_at,
                    "field_count": field_count,
                    "ttl_seconds": cached.get("cache_metadata", {}).get("ttl_seconds", 86400),
                }
            else:
                status[dataset] = {"cached": False}
        except Exception as e:
            status[dataset] = {"cached": False, "error": str(e)}
    
    return status


def force_refresh(ctx, datasets):
    """强制刷新缓存"""
    cache_manager = get_cache_manager(ctx)
    results = {}
    
    for dataset in datasets:
        try:
            # 设置强制刷新标记
            from _lib.wqb_store import get_store
            store = get_store(ctx)
            try:
                store.upsert_ledger(ctx.region, f"force_refresh_{dataset}", {"refresh": True, "timestamp": datetime.datetime.now().isoformat()})
            finally:
                store.close()
            
            print(f"✓ 已标记 {dataset} 强制刷新")
            results[dataset] = {"status": "marked_for_refresh"}
        except Exception as e:
            print(f"✗ 标记 {dataset} 强制刷新失败: {e}")
            results[dataset] = {"status": "error", "error": str(e)}
    
    return results


def main():
    ap = argparse.ArgumentParser(description="S1 字段扫描缓存管理工具")
    ap.add_argument("--campaign-dir", required=True, help="战役目录")
    ap.add_argument("--preload", help="批量预热缓存（逗号分隔的数据集列表）")
    ap.add_argument("--clear", help="清除缓存（逗号分隔的数据集列表）")
    ap.add_argument("--status", help="查看缓存状态（逗号分隔的数据集列表）")
    ap.add_argument("--refresh", help="强制刷新缓存（逗号分隔的数据集列表）")
    ap.add_argument("--cache-ttl", type=int, default=86400, help="缓存有效期（秒），默认 24 小时")
    args = ap.parse_args()
    
    ctx = CampaignContext(args.campaign_dir)
    
    if args.preload:
        datasets = [d.strip() for d in args.preload.split(",")]
        print(f"批量预热 {len(datasets)} 个数据集的缓存...")
        results = preload_caches(ctx, datasets, args.cache_ttl)
        print("\n预热结果:")
        for dataset, result in results.items():
            status = result.get("status", "unknown")
            if status == "skipped":
                print(f"  ✓ {dataset}: 缓存有效，跳过")
            elif status == "needs_refresh":
                print(f"  → {dataset}: 需要刷新")
            elif status == "error":
                print(f"  ✗ {dataset}: 错误 - {result.get('error', 'unknown')}")
            else:
                print(f"  ? {dataset}: {status}")
    
    elif args.clear:
        datasets = [d.strip() for d in args.clear.split(",")]
        print(f"清除 {len(datasets)} 个数据集的缓存...")
        for dataset in datasets:
            clear_cache(ctx, dataset)
    
    elif args.status:
        datasets = [d.strip() for d in args.status.split(",")]
        print(f"查看 {len(datasets)} 个数据集的缓存状态...")
        status = get_cache_status(ctx, datasets)
        print("\n缓存状态:")
        for dataset, info in status.items():
            if info.get("cached"):
                print(f"  ✓ {dataset}: {info['field_count']} 个字段，缓存时间: {info['cached_at']}")
            else:
                print(f"  ✗ {dataset}: 无缓存")
                if "error" in info:
                    print(f"    错误: {info['error']}")
    
    elif args.refresh:
        datasets = [d.strip() for d in args.refresh.split(",")]
        print(f"强制刷新 {len(datasets)} 个数据集的缓存...")
        results = force_refresh(ctx, datasets)
        print("\n刷新结果:")
        for dataset, result in results.items():
            status = result.get("status", "unknown")
            if status == "marked_for_refresh":
                print(f"  ✓ {dataset}: 已标记强制刷新")
            elif status == "error":
                print(f"  ✗ {dataset}: 错误 - {result.get('error', 'unknown')}")
            else:
                print(f"  ? {dataset}: {status}")
    
    else:
        print("请指定操作: --preload, --clear, --status, 或 --refresh")
        sys.exit(1)


if __name__ == "__main__":
    main()
