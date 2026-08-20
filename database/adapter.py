"""
数据库适配器层
让现有脚本无缝切换到数据库存储
"""

import json
import csv
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime

try:
    from .integration import get_database_integration
except ImportError:
    from integration import get_database_integration

logger = logging.getLogger(__name__)

class DatabaseAdapter:
    """数据库适配器 - 替换文件操作"""
    
    def __init__(self, workspace_root: str = "D:\\coding\\traeCN_project\\wqb"):
        self.workspace_root = Path(workspace_root)
        self.db_integration = get_database_integration()
        self.use_database = True  # 是否使用数据库
    
    def save_diversity_potential(self, region: str, dataset: str, data: Dict[str, Any], 
                                file_path: Optional[str] = None):
        """保存多样性潜力报告（替换 diversity_potential.json）"""
        if self.use_database:
            # 使用数据库
            self.db_integration.save_diversity_potential(region, dataset, data)
            logger.info(f"保存多样性潜力到数据库: {region}/{dataset}")
        else:
            # 兼容文件保存
            if file_path:
                self._save_json_file(file_path, data)
    
    def load_diversity_potential(self, region: str, dataset: str, 
                                file_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """加载多样性潜力报告（替换 diversity_potential.json）"""
        if self.use_database:
            # 使用数据库
            return self.db_integration.load_diversity_potential(region, dataset)
        else:
            # 兼容文件加载
            if file_path and Path(file_path).exists():
                return self._load_json_file(file_path)
            return None
    
    def save_wave_expressions(self, region: str, wave: str, expressions: List[Dict[str, Any]], 
                            file_path: Optional[str] = None):
        """保存 wave 表达式（替换 wave<TAG>_exprs.json）"""
        if self.use_database:
            # 使用数据库
            self.db_integration.save_wave_expressions(region, wave, expressions)
            logger.info(f"保存 wave 表达式到数据库: {region}/{wave} ({len(expressions)} 个表达式)")
        else:
            # 兼容文件保存
            if file_path:
                self._save_json_file(file_path, {'expressions': expressions})
    
    def load_wave_expressions(self, region: str, wave: str, 
                            file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """加载 wave 表达式（替换 wave<TAG>_exprs.json）"""
        if self.use_database:
            # 使用数据库
            return self.db_integration.load_wave_expressions(region, wave)
        else:
            # 兼容文件加载
            if file_path and Path(file_path).exists():
                data = self._load_json_file(file_path)
                return data.get('expressions', [])
            return []
    
    def save_alpha_result(self, alpha_id: str, region: str, dataset: str, 
                         expression: str, settings: Dict[str, Any], 
                         metrics: Dict[str, Any], csv_path: Optional[str] = None):
        """保存 alpha 结果（替换结果 CSV）"""
        if self.use_database:
            # 使用数据库
            self.db_integration.save_alpha_result(alpha_id, region, dataset, expression, settings, metrics)
            logger.info(f"保存 alpha 结果到数据库: {alpha_id}")
        else:
            # 兼容 CSV 保存
            if csv_path:
                self._append_csv_row(csv_path, {
                    'alpha_id': alpha_id,
                    'expression': expression,
                    'region': region,
                    'dataset': dataset,
                    'universe': settings.get('universe'),
                    'delay': settings.get('delay'),
                    'neutralization': settings.get('neutralization'),
                    'sharpe': metrics.get('sharpe'),
                    'fitness': metrics.get('fitness'),
                    'margin': metrics.get('margin'),
                    'turnover': metrics.get('turnover'),
                    'status': metrics.get('status', 'UNSUBMITTED'),
                    'created_at': datetime.now().isoformat()
                })
    
    def get_submit_ready_alphas(self, region: str, 
                               csv_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取可提交的 alpha（替换手动筛选）"""
        if self.use_database:
            # 使用数据库
            return self.db_integration.get_submit_ready_alphas(region)
        else:
            # 兼容 CSV 筛选
            if csv_path and Path(csv_path).exists():
                return self._filter_submit_ready_from_csv(csv_path)
            return []
    
    def get_campaign_progress(self, region: str, 
                             csv_path: Optional[str] = None) -> Dict[str, Any]:
        """获取战役进度（替换手动统计）"""
        if self.use_database:
            # 使用数据库
            return self.db_integration.get_campaign_progress(region)
        else:
            # 兼容 CSV 统计
            if csv_path and Path(csv_path).exists():
                return self._calculate_progress_from_csv(csv_path)
            return {}
    
    def save_field_catalog(self, region: str, dataset: str, fields: List[Dict[str, Any]], 
                          file_path: Optional[str] = None):
        """保存字段目录（替换 scan_fields.py 输出）"""
        if self.use_database:
            # 使用数据库
            region_obj = self.db_integration.region_dao.get_by_name(region)
            if region_obj:
                dataset_obj = self.db_integration.dataset_dao.get_by_name_and_region(dataset, region_obj['id'])
                if dataset_obj:
                    for field in fields:
                        field_data = {
                            'type': field.get('type'),
                            'description': field.get('description'),
                            'coverage': field.get('coverage'),
                            'category': field.get('category')
                        }
                        self.db_integration.field_dao.create_or_update(dataset_obj['id'], field['name'], field_data)
                    logger.info(f"保存字段目录到数据库: {region}/{dataset} ({len(fields)} 个字段)")
        else:
            # 兼容文件保存
            if file_path:
                self._save_json_file(file_path, {'fields': fields})
    
    def load_field_catalog(self, region: str, dataset: str, 
                          file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """加载字段目录（替换 scan_fields.py 输出）"""
        if self.use_database:
            # 使用数据库
            return self.db_integration.get_field_catalog(region, dataset)
        else:
            # 兼容文件加载
            if file_path and Path(file_path).exists():
                data = self._load_json_file(file_path)
                return data.get('fields', [])
            return []
    
    def save_dataset_ranking(self, region: str, datasets: List[Dict[str, Any]], 
                            file_path: Optional[str] = None):
        """保存数据集排名（替换 score_datasets.py 输出）"""
        if self.use_database:
            # 使用数据库
            region_obj = self.db_integration.region_dao.get_by_name(region)
            if region_obj:
                for dataset in datasets:
                    dataset_data = {
                        'category': dataset.get('category'),
                        'field_count': dataset.get('field_count'),
                        'coverage': dataset.get('coverage'),
                        'alpha_count': dataset.get('alpha_count'),
                        'value_score': dataset.get('value_score'),
                        'pyramid_multiplier': dataset.get('pyramid_multiplier'),
                        'tier': dataset.get('tier'),
                        'status': dataset.get('status', 'untried')
                    }
                    self.db_integration.dataset_dao.create_or_update(dataset['name'], region_obj['id'], dataset_data)
                logger.info(f"保存数据集排名到数据库: {region} ({len(datasets)} 个数据集)")
        else:
            # 兼容文件保存
            if file_path:
                self._save_json_file(file_path, {'datasets': datasets})
    
    def load_dataset_ranking(self, region: str, 
                            file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """加载数据集排名（替换 score_datasets.py 输出）"""
        if self.use_database:
            # 使用数据库
            return self.db_integration.get_dataset_whitelist(region)
        else:
            # 兼容文件加载
            if file_path and Path(file_path).exists():
                data = self._load_json_file(file_path)
                return data.get('datasets', [])
            return []
    
    # 私有辅助方法
    def _save_json_file(self, file_path: str, data: Dict[str, Any]):
        """保存 JSON 文件"""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_json_file(self, file_path: str) -> Dict[str, Any]:
        """加载 JSON 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _append_csv_row(self, csv_path: str, row: Dict[str, Any]):
        """追加 CSV 行"""
        Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 检查文件是否存在
        file_exists = Path(csv_path).exists()
        
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
    
    def _filter_submit_ready_from_csv(self, csv_path: str) -> List[Dict[str, Any]]:
        """从 CSV 筛选可提交的 alpha"""
        submit_ready = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if (row.get('status') == 'UNSUBMITTED' and 
                    float(row.get('sharpe', 0)) > 1.58 and 
                    float(row.get('fitness', 0)) >= 1.0 and
                    float(row.get('margin', 0)) > 0.0005 and
                    0.05 <= float(row.get('turnover', 0)) <= 0.3):
                    submit_ready.append(row)
        return submit_ready
    
    def _calculate_progress_from_csv(self, csv_path: str) -> Dict[str, Any]:
        """从 CSV 计算战役进度"""
        total_alphas = 0
        submit_ready = 0
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_alphas += 1
                if (row.get('status') == 'UNSUBMITTED' and 
                    float(row.get('sharpe', 0)) > 1.58 and 
                    float(row.get('fitness', 0)) >= 1.0):
                    submit_ready += 1
        
        return {
            'total_alphas': total_alphas,
            'submit_ready': submit_ready,
            'target_count': 10,
            'status': 'active'
        }

# 全局适配器实例
_adapter: Optional[DatabaseAdapter] = None

def get_database_adapter() -> DatabaseAdapter:
    """获取全局数据库适配器实例"""
    global _adapter
    if _adapter is None:
        _adapter = DatabaseAdapter()
    return _adapter

def enable_database_mode():
    """启用数据库模式"""
    global _adapter
    if _adapter:
        _adapter.use_database = True

def disable_database_mode():
    """禁用数据库模式（使用文件模式）"""
    global _adapter
    if _adapter:
        _adapter.use_database = False

# 便捷函数
def save_diversity_potential(region: str, dataset: str, data: Dict[str, Any], 
                            file_path: Optional[str] = None):
    """保存多样性潜力报告"""
    adapter = get_database_adapter()
    adapter.save_diversity_potential(region, dataset, data, file_path)

def load_diversity_potential(region: str, dataset: str, 
                            file_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """加载多样性潜力报告"""
    adapter = get_database_adapter()
    return adapter.load_diversity_potential(region, dataset, file_path)

def save_wave_expressions(region: str, wave: str, expressions: List[Dict[str, Any]], 
                        file_path: Optional[str] = None):
    """保存 wave 表达式"""
    adapter = get_database_adapter()
    adapter.save_wave_expressions(region, wave, expressions, file_path)

def load_wave_expressions(region: str, wave: str, 
                        file_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """加载 wave 表达式"""
    adapter = get_database_adapter()
    return adapter.load_wave_expressions(region, wave, file_path)

def save_alpha_result(alpha_id: str, region: str, dataset: str, 
                     expression: str, settings: Dict[str, Any], 
                     metrics: Dict[str, Any], csv_path: Optional[str] = None):
    """保存 alpha 结果"""
    adapter = get_database_adapter()
    adapter.save_alpha_result(alpha_id, region, dataset, expression, settings, metrics, csv_path)

def get_submit_ready_alphas(region: str, 
                           csv_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """获取可提交的 alpha"""
    adapter = get_database_adapter()
    return adapter.get_submit_ready_alphas(region, csv_path)

def get_campaign_progress(region: str, 
                         csv_path: Optional[str] = None) -> Dict[str, Any]:
    """获取战役进度"""
    adapter = get_database_adapter()
    return adapter.get_campaign_progress(region, csv_path)
