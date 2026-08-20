"""
数据迁移脚本
从现有 JSON/CSV 文件迁移到数据库
"""

import json
import csv
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

from db_manager import get_db_manager
from dao import (
    get_region_dao, get_dataset_dao, get_field_dao, 
    get_alpha_dao, get_wave_dao, get_expression_dao,
    get_diversity_potential_dao, get_campaign_state_dao
)

logger = logging.getLogger(__name__)


def load_registry(workspace_root: Path) -> Dict[str, Any]:
    """加载战役 registry：优先拆分目录 research-data/registry/，回退旧单文件 campaign_registry.json。

    返回结构与旧单文件一致：{"regions": {<R>: {...}}, ...}。
    """
    registry_dir = workspace_root / "research-data" / "registry"
    index_path = registry_dir / "index.json"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
        regions = {}
        for region in index.get('regions', []):
            rp = registry_dir / f"{region}.json"
            if rp.exists():
                with open(rp, 'r', encoding='utf-8') as f:
                    regions[region] = json.load(f)
        out = dict(index)
        out['regions'] = regions
        return out

    legacy = workspace_root / "research-data" / "campaign_registry.json"
    if legacy.exists():
        with open(legacy, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


class DataMigrator:
    """数据迁移器"""
    
    def __init__(self, workspace_root: str = "D:\\coding\\traeCN_project\\wqb"):
        self.workspace_root = Path(workspace_root)
        self.db = get_db_manager()
        
        # 初始化 DAO
        self.region_dao = get_region_dao()
        self.dataset_dao = get_dataset_dao()
        self.field_dao = get_field_dao()
        self.alpha_dao = get_alpha_dao()
        self.wave_dao = get_wave_dao()
        self.expression_dao = get_expression_dao()
        self.diversity_dao = get_diversity_potential_dao()
        self.campaign_dao = get_campaign_state_dao()
    
    def migrate_all(self):
        """迁移所有数据"""
        logger.info("开始数据迁移...")
        
        # 1. 迁移区域配置
        self.migrate_regions()
        
        # 2. 迁移数据集
        self.migrate_datasets()
        
        # 3. 迁移字段
        self.migrate_fields()
        
        # 4. 迁移 alpha
        self.migrate_alphas()
        
        # 5. 迁移 wave
        self.migrate_waves()
        
        # 6. 迁移表达式
        self.migrate_expressions()
        
        # 7. 迁移多样性潜力
        self.migrate_diversity_potential()
        
        # 8. 迁移战役状态
        self.migrate_campaign_state()
        
        logger.info("数据迁移完成！")
    
    def migrate_regions(self):
        """迁移区域配置"""
        logger.info("迁移区域配置...")
        
        # 从 campaign_registry 读取区域配置（优先拆分目录，回退旧单文件）
        registry = load_registry(self.workspace_root)
        if registry:
            for region_name, region_data in registry.get('regions', {}).items():
                static_config = region_data.get('static', {})
                config = {
                    'universe_legal': static_config.get('universe_legal', []),
                    'delay_legal': static_config.get('delay_legal', []),
                    'neutralization_default': static_config.get('neutralization_default')
                }
                
                self.region_dao.create_or_update(region_name, config)
                logger.info(f"迁移区域: {region_name}")
    
    def migrate_datasets(self):
        """迁移数据集"""
        logger.info("迁移数据集...")
        
        # 从 campaign_registry 读取数据集信息（优先拆分目录，回退旧单文件）
        registry = load_registry(self.workspace_root)
        if registry:
            for region_name, region_data in registry.get('regions', {}).items():
                region = self.region_dao.get_by_name(region_name)
                if not region:
                    continue
                
                region_id = region['id']
                assets = region_data.get('assets', {})
                
                for dataset_name, dataset_info in assets.get('datasets', {}).items():
                    # 处理不同的数据结构
                    if isinstance(dataset_info, dict):
                        data = {
                            'category': dataset_info.get('category'),
                            'field_count': dataset_info.get('field_count'),
                            'coverage': dataset_info.get('coverage'),
                            'alpha_count': dataset_info.get('alpha_count'),
                            'value_score': dataset_info.get('value_score'),
                            'pyramid_multiplier': dataset_info.get('pyramid_multiplier'),
                            'tier': dataset_info.get('tier'),
                            'status': dataset_info.get('status', 'untried')
                        }
                    else:
                        # 如果 dataset_info 不是字典，跳过
                        logger.warning(f"跳过无效数据集信息: {region_name}/{dataset_name}")
                        continue
                    
                    self.dataset_dao.create_or_update(dataset_name, region_id, data)
                    logger.info(f"迁移数据集: {region_name}/{dataset_name}")
                
                # 如果 datasets 为空，从 top_datasets 获取
                if not assets.get('datasets') and assets.get('top_datasets'):
                    for dataset_info in assets.get('top_datasets', []):
                        if isinstance(dataset_info, dict) and 'name' in dataset_info:
                            dataset_name = dataset_info['name']
                            data = {
                                'category': dataset_info.get('category'),
                                'field_count': dataset_info.get('field_count'),
                                'coverage': dataset_info.get('coverage'),
                                'alpha_count': dataset_info.get('alpha_count'),
                                'value_score': dataset_info.get('value_score'),
                                'pyramid_multiplier': dataset_info.get('pyramid_multiplier'),
                                'tier': dataset_info.get('tier'),
                                'status': dataset_info.get('status', 'untried')
                            }
                            
                            self.dataset_dao.create_or_update(dataset_name, region_id, data)
                            logger.info(f"迁移数据集: {region_name}/{dataset_name}")
    
    def migrate_fields(self):
        """迁移字段"""
        logger.info("迁移字段...")
        
        # 从字段扫描结果迁移
        reference_dir = self.workspace_root / "tracking"
        for region_dir in reference_dir.iterdir():
            if not region_dir.is_dir():
                continue
            
            region_name = region_dir.name
            region = self.region_dao.get_by_name(region_name)
            if not region:
                continue
            
            region_id = region['id']
            reference_subdir = region_dir / "reference"
            
            if reference_subdir.exists():
                for fields_file in reference_subdir.glob("*_fields.json"):
                    dataset_name = fields_file.stem.replace(f"{region_name}_", "").replace("_fields", "")
                    
                    dataset = self.dataset_dao.get_by_name_and_region(dataset_name, region_id)
                    if not dataset:
                        continue
                    
                    dataset_id = dataset['id']
                    
                    with open(fields_file, 'r', encoding='utf-8') as f:
                        fields_data = json.load(f)
                    
                    for field in fields_data.get('fields', []):
                        field_data = {
                            'type': field.get('type'),
                            'description': field.get('description'),
                            'coverage': field.get('coverage'),
                            'category': field.get('category')
                        }
                        
                        self.field_dao.create_or_update(dataset_id, field['name'], field_data)
                    
                    logger.info(f"迁移字段: {region_name}/{dataset_name} ({len(fields_data.get('fields', []))} 个字段)")
    
    def migrate_alphas(self):
        """迁移 alpha"""
        logger.info("迁移 alpha...")
        
        # 从结果 CSV 文件迁移
        for region_dir in (self.workspace_root / "tracking").iterdir():
            if not region_dir.is_dir():
                continue
            
            region_name = region_dir.name
            region = self.region_dao.get_by_name(region_name)
            if not region:
                continue
            
            region_id = region['id']
            results_dir = region_dir / "results"
            
            if results_dir.exists():
                for csv_file in results_dir.glob("*_status.csv"):
                    wave_number = csv_file.stem.replace("_status", "")
                    
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            if row.get('alpha_id'):
                                alpha_data = {
                                    'expression': row.get('expression', ''),
                                    'region_id': region_id,
                                    'dataset_id': None,  # 需要从 wave 推断
                                    'universe': row.get('universe'),
                                    'delay': row.get('delay'),
                                    'neutralization': row.get('neutralization'),
                                    'sharpe': float(row.get('sharpe', 0)) if row.get('sharpe') else None,
                                    'fitness': float(row.get('fitness', 0)) if row.get('fitness') else None,
                                    'margin': float(row.get('margin', 0)) if row.get('margin') else None,
                                    'turnover': float(row.get('turnover', 0)) if row.get('turnover') else None,
                                    'status': row.get('status', 'UNSUBMITTED'),
                                    'created_at': row.get('created_at', datetime.now().isoformat())
                                }
                                
                                self.alpha_dao.create_or_update(row['alpha_id'], alpha_data)
                    
                    logger.info(f"迁移 alpha: {region_name}/{wave_number}")
    
    def migrate_waves(self):
        """迁移 wave"""
        logger.info("迁移 wave...")
        
        for region_dir in (self.workspace_root / "tracking").iterdir():
            if not region_dir.is_dir():
                continue
            
            region_name = region_dir.name
            region = self.region_dao.get_by_name(region_name)
            if not region:
                continue
            
            region_id = region['id']
            candidates_dir = region_dir / "candidates"
            
            if candidates_dir.exists():
                for wave_file in candidates_dir.glob("*_wave*_exprs.json"):
                    wave_number = wave_file.stem.replace(f"{region_name}_", "").replace("_exprs", "")
                    
                    with open(wave_file, 'r', encoding='utf-8') as f:
                        wave_data = json.load(f)
                    
                    wave_info = {
                        'dataset_id': None,  # 需要从表达式推断
                        'expression_count': len(wave_data.get('expressions', [])),
                        'status': 'completed',
                        'created_at': datetime.now().isoformat()
                    }
                    
                    self.wave_dao.create_or_update(region_id, wave_number, wave_info)
                    logger.info(f"迁移 wave: {region_name}/{wave_number}")
    
    def migrate_expressions(self):
        """迁移表达式"""
        logger.info("迁移表达式...")
        
        for region_dir in (self.workspace_root / "tracking").iterdir():
            if not region_dir.is_dir():
                continue
            
            region_name = region_dir.name
            region = self.region_dao.get_by_name(region_name)
            if not region:
                continue
            
            region_id = region['id']
            candidates_dir = region_dir / "candidates"
            
            if candidates_dir.exists():
                for wave_file in candidates_dir.glob("*_wave*_exprs.json"):
                    wave_number = wave_file.stem.replace(f"{region_name}_", "").replace("_exprs", "")
                    
                    wave = self.wave_dao.get_by_region_and_wave(region_id, wave_number)
                    if not wave:
                        continue
                    
                    wave_id = wave['id']
                    
                    with open(wave_file, 'r', encoding='utf-8') as f:
                        wave_data = json.load(f)
                    
                    for expr in wave_data.get('expressions', []):
                        expr_data = {
                            'fingerprint': expr.get('fingerprint'),
                            'status': expr.get('status', 'pending'),
                            'alpha_id': expr.get('alpha_id'),
                            'sharpe': expr.get('sharpe'),
                            'fitness': expr.get('fitness'),
                            'margin': expr.get('margin'),
                            'turnover': expr.get('turnover'),
                            'created_at': datetime.now().isoformat()
                        }
                        
                        self.expression_dao.create_or_update(wave_id, expr['expression'], expr_data)
                    
                    logger.info(f"迁移表达式: {region_name}/{wave_number} ({len(wave_data.get('expressions', []))} 个表达式)")
    
    def migrate_diversity_potential(self):
        """迁移多样性潜力"""
        logger.info("迁移多样性潜力...")
        
        for region_dir in (self.workspace_root / "tracking").iterdir():
            if not region_dir.is_dir():
                continue
            
            region_name = region_dir.name
            region = self.region_dao.get_by_name(region_name)
            if not region:
                continue
            
            region_id = region['id']
            reference_dir = region_dir / "reference"
            
            if reference_dir.exists():
                for diversity_file in reference_dir.glob("*_diversity_potential.json"):
                    dataset_name = diversity_file.stem.replace(f"{region_name}_", "").replace("_diversity_potential", "")
                    
                    dataset = self.dataset_dao.get_by_name_and_region(dataset_name, region_id)
                    if not dataset:
                        continue
                    
                    dataset_id = dataset['id']
                    
                    with open(diversity_file, 'r', encoding='utf-8') as f:
                        diversity_data = json.load(f)
                    
                    potential_data = {
                        'diversity_score': diversity_data.get('diversity_score'),
                        'recommended_rounds': diversity_data.get('recommended_rounds'),
                        'field_categories': diversity_data.get('field_categories', {}),
                        'operator_buckets': diversity_data.get('operator_buckets', {}),
                        'parameter_space': diversity_data.get('parameter_space', {}),
                        'created_at': datetime.now().isoformat()
                    }
                    
                    self.diversity_dao.create_or_update(region_id, dataset_id, potential_data)
                    logger.info(f"迁移多样性潜力: {region_name}/{dataset_name}")
    
    def migrate_campaign_state(self):
        """迁移战役状态"""
        logger.info("迁移战役状态...")
        
        for region_dir in (self.workspace_root / "tracking").iterdir():
            if not region_dir.is_dir():
                continue
            
            region_name = region_dir.name
            region = self.region_dao.get_by_name(region_name)
            if not region:
                continue
            
            region_id = region['id']
            
            # 从现有数据推断战役状态
            waves = self.wave_dao.get_by_region(region_id)
            alphas = self.alpha_dao.get_by_region_and_dataset(region_id, None)
            
            submit_ready_count = len([a for a in alphas if a.get('status') == 'UNSUBMITTED' and 
                                    a.get('sharpe', 0) > 1.58 and a.get('fitness', 0) >= 1.0])
            
            state_data = {
                'current_wave': len(waves),
                'submit_ready_count': submit_ready_count,
                'target_count': 10,
                'status': 'active'
            }
            
            self.campaign_dao.create_or_update(region_id, state_data)
            logger.info(f"迁移战役状态: {region_name} (submit_ready: {submit_ready_count})")

def main():
    """主函数"""
    logging.basicConfig(level=logging.INFO)
    
    migrator = DataMigrator()
    migrator.migrate_all()

if __name__ == "__main__":
    main()
