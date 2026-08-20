"""
数据库功能测试脚本
"""

import sys
import logging
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from db_manager import init_database
from integration import get_database_integration
from dao import get_region_dao, get_dataset_dao

def test_database():
    """测试数据库功能"""
    logging.basicConfig(level=logging.INFO)
    
    print("=== 测试 WQB 数据库 ===")
    
    # 1. 初始化数据库
    print("\n1. 初始化数据库...")
    db_manager = init_database("data/test_wqb.db")
    print("[OK] 数据库初始化完成")
    
    # 2. 测试集成接口
    print("\n2. 测试集成接口...")
    integration = get_database_integration()
    
    # 测试保存多样性潜力
    test_data = {
        'diversity_score': 0.875,
        'recommended_rounds': 5,
        'field_categories': {'roe': ['mdl31_roe_pct_t4q'], 'gm': ['mdl31_gm_pct_t4q']},
        'operator_buckets': {'ts_zscore': ['ts_zscore'], 'rank': ['rank']},
        'parameter_space': {'windows': [60, 120, 180], 'operators': ['ts_zscore', 'rank']}
    }
    
    # 先创建区域和数据集
    region_dao = get_region_dao()
    dataset_dao = get_dataset_dao()
    
    # 创建测试区域
    region_dao.create_or_update("TEST", {
        'universe_legal': ['TOP400'],
        'delay_legal': [1],
        'neutralization_default': 'SECTOR'
    })
    
    # 创建测试数据集
    region = region_dao.get_by_name("TEST")
    dataset_dao.create_or_update("test_dataset", region['id'], {
        'category': 'model',
        'field_count': 74,
        'coverage': 0.9518,
        'alpha_count': 100,
        'value_score': 8.5,
        'pyramid_multiplier': 1.5,
        'tier': 'tier1',
        'status': 'untried'
    })
    
    # 测试保存多样性潜力
    integration.save_diversity_potential("TEST", "test_dataset", test_data)
    print("[OK] 保存多样性潜力完成")
    
    # 测试加载多样性潜力
    loaded_data = integration.load_diversity_potential("TEST", "test_dataset")
    if loaded_data:
        print(f"[OK] 加载多样性潜力完成: score={loaded_data['diversity_score']}")
    else:
        print("[FAIL] 加载多样性潜力失败")
    
    # 测试保存 wave 表达式
    test_expressions = [
        {
            'expression': 'rank(ts_zscore(mdl31_roe_pct_t4q, 120))',
            'fingerprint': 'test123',
            'status': 'completed',
            'alpha_id': 'TEST001',
            'sharpe': 1.39,
            'fitness': 0.96,
            'margin': 9.47,
            'turnover': 23.58
        }
    ]
    
    integration.save_wave_expressions("TEST", "test_wave", test_expressions)
    print("[OK] 保存 wave 表达式完成")
    
    # 测试加载 wave 表达式
    loaded_expressions = integration.load_wave_expressions("TEST", "test_wave")
    if loaded_expressions:
        print(f"[OK] 加载 wave 表达式完成: {len(loaded_expressions)} 个表达式")
    else:
        print("[FAIL] 加载 wave 表达式失败")
    
    # 测试保存 alpha 结果
    integration.save_alpha_result(
        alpha_id="TEST001",
        region="TEST",
        dataset="test_dataset",
        expression="rank(ts_zscore(mdl31_roe_pct_t4q, 120))",
        settings={
            'universe': 'TOP400',
            'delay': 1,
            'neutralization': 'SECTOR'
        },
        metrics={
            'sharpe': 1.39,
            'fitness': 0.96,
            'margin': 9.47,
            'turnover': 23.58,
            'status': 'UNSUBMITTED'
        }
    )
    print("[OK] 保存 alpha 结果完成")
    
    # 测试获取可提交的 alpha
    submit_ready = integration.get_submit_ready_alphas("TEST")
    print(f"[OK] 获取可提交 alpha 完成: {len(submit_ready)} 个")
    
    # 测试获取战役进度
    progress = integration.get_campaign_progress("TEST")
    print(f"[OK] 获取战役进度完成: {progress}")
    
    # 3. 测试数据库统计
    print("\n3. 数据库统计...")
    tables = db_manager.get_tables()
    for table in tables:
        count = db_manager.fetchone(f"SELECT COUNT(*) as count FROM {table}")
        print(f"  {table}: {count['count']} 条记录")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_database()
