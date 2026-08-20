"""
数据访问对象（DAO）层
提供高级数据操作接口
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from db_manager import DatabaseManager, get_db_manager

logger = logging.getLogger(__name__)

class BaseDAO:
    """基础 DAO 类"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or get_db_manager()
        self.table_name = ""
    
    def create(self, data: Dict[str, Any]) -> int:
        """创建记录"""
        return self.db.insert(self.table_name, data)
    
    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """根据 ID 获取记录"""
        return self.db.fetchone(f"SELECT * FROM {self.table_name} WHERE id = ?", (id,))
    
    def get_all(self) -> List[Dict[str, Any]]:
        """获取所有记录"""
        return self.db.fetchall(f"SELECT * FROM {self.table_name}")
    
    def update(self, id: int, data: Dict[str, Any]) -> int:
        """更新记录"""
        data['updated_at'] = datetime.now().isoformat()
        return self.db.update(self.table_name, data, "id = ?", (id,))
    
    def delete(self, id: int) -> int:
        """删除记录"""
        return self.db.delete(self.table_name, "id = ?", (id,))

class RegionDAO(BaseDAO):
    """区域 DAO"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "regions"
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取区域"""
        return self.db.fetchone("SELECT * FROM regions WHERE name = ?", (name,))
    
    def create_or_update(self, name: str, config: Dict[str, Any]) -> int:
        """创建或更新区域配置"""
        data = {
            'name': name,
            'universe_legal': json.dumps(config.get('universe_legal', [])),
            'delay_legal': json.dumps(config.get('delay_legal', [])),
            'neutralization_default': config.get('neutralization_default'),
            'updated_at': datetime.now().isoformat()
        }
        
        existing = self.get_by_name(name)
        if existing:
            return self.db.update(self.table_name, data, "name = ?", (name,))
        else:
            data['created_at'] = datetime.now().isoformat()
            return self.create(data)

class DatasetDAO(BaseDAO):
    """数据集 DAO"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "datasets"
    
    def get_by_name_and_region(self, name: str, region_id: int) -> Optional[Dict[str, Any]]:
        """根据名称和区域获取数据集"""
        return self.db.fetchone(
            "SELECT * FROM datasets WHERE name = ? AND region_id = ?", 
            (name, region_id)
        )
    
    def get_by_region(self, region_id: int) -> List[Dict[str, Any]]:
        """获取区域的所有数据集"""
        return self.db.fetchall(
            "SELECT * FROM datasets WHERE region_id = ? ORDER BY name", 
            (region_id,)
        )
    
    def get_whitelist(self, region_id: int) -> List[Dict[str, Any]]:
        """获取白名单数据集"""
        return self.db.fetchall(
            "SELECT * FROM datasets WHERE region_id = ? AND tier = 'tier1' ORDER BY value_score DESC", 
            (region_id,)
        )
    
    def create_or_update(self, name: str, region_id: int, data: Dict[str, Any]) -> int:
        """创建或更新数据集"""
        dataset_data = {
            'name': name,
            'region_id': region_id,
            'category': data.get('category'),
            'field_count': data.get('field_count'),
            'coverage': data.get('coverage'),
            'alpha_count': data.get('alpha_count'),
            'value_score': data.get('value_score'),
            'pyramid_multiplier': data.get('pyramid_multiplier'),
            'tier': data.get('tier'),
            'status': data.get('status', 'untried'),
            'updated_at': datetime.now().isoformat()
        }
        
        existing = self.get_by_name_and_region(name, region_id)
        if existing:
            return self.db.update(self.table_name, dataset_data, "id = ?", (existing['id'],))
        else:
            dataset_data['created_at'] = datetime.now().isoformat()
            return self.create(dataset_data)

class FieldDAO(BaseDAO):
    """字段 DAO（表 fields：列 field_name / field_type / field_group）

    注意：callers（migrate.py / adapter.py）传入的字段名参数命名为
    ``name``、类型参数命名为 ``type``、分组参数命名为 ``category``，
    此处统一映射到真实表列，读取时再做别名回映射，调用方零改动。
    """
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "fields"
    
    _SELECT = (
        "SELECT id, dataset_id, field_name AS name, field_type AS type, "
        "coverage, user_count, alpha_count, description, field_group AS category, "
        "created_at FROM fields"
    )
    
    def get_by_dataset(self, dataset_id: int) -> List[Dict[str, Any]]:
        """获取数据集的所有字段"""
        return self.db.fetchall(
            f"{self._SELECT} WHERE dataset_id = ? ORDER BY field_name", 
            (dataset_id,)
        )
    
    def get_by_type(self, dataset_id: int, field_type: str) -> List[Dict[str, Any]]:
        """根据类型获取字段"""
        return self.db.fetchall(
            f"{self._SELECT} WHERE dataset_id = ? AND field_type = ? ORDER BY field_name", 
            (dataset_id, field_type)
        )
    
    def create_or_update(self, dataset_id: int, name: str, data: Dict[str, Any]) -> int:
        """创建或更新字段（name→field_name, type→field_type, category→field_group）"""
        field_data = {
            'dataset_id': dataset_id,
            'field_name': name,
            'field_type': data.get('type'),
            'description': data.get('description'),
            'coverage': data.get('coverage'),
            'field_group': data.get('category'),
            'user_count': data.get('user_count'),
            'alpha_count': data.get('alpha_count'),
        }
        if existing := self.db.fetchone(
            "SELECT * FROM fields WHERE dataset_id = ? AND field_name = ?", 
            (dataset_id, name)
        ):
            return self.db.update(self.table_name, field_data, "id = ?", (existing['id'],))
        else:
            field_data['created_at'] = datetime.now().isoformat()
            return self.create(field_data)

class AlphaDAO(BaseDAO):
    """Alpha DAO"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "alphas"
    
    def get_by_alpha_id(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """根据 alpha_id 获取记录"""
        return self.db.fetchone("SELECT * FROM alphas WHERE alpha_id = ?", (alpha_id,))
    
    def get_by_region_and_dataset(self, region_id: int, dataset_id: int) -> List[Dict[str, Any]]:
        """获取区域和数据集的所有 alpha"""
        return self.db.fetchall(
            "SELECT * FROM alphas WHERE region_id = ? AND dataset_id = ? ORDER BY created_at DESC", 
            (region_id, dataset_id)
        )
    
    def get_submit_ready(self, region_id: int) -> List[Dict[str, Any]]:
        """获取可提交的 alpha"""
        return self.db.fetchall(
            """SELECT * FROM alphas 
               WHERE region_id = ? AND status = 'UNSUBMITTED' 
               AND sharpe > 1.58 AND fitness >= 1.0 AND margin > 0.0005
               AND turnover BETWEEN 0.05 AND 0.3
               ORDER BY sharpe DESC""", 
            (region_id,)
        )
    
    def create_or_update(self, alpha_id: str, data: Dict[str, Any]) -> int:
        """创建或更新 alpha"""
        alpha_data = {
            'alpha_id': alpha_id,
            'expression': data.get('expression'),
            'region_id': data.get('region_id'),
            'dataset_id': data.get('dataset_id'),
            'universe': data.get('universe'),
            'delay': data.get('delay'),
            'neutralization': data.get('neutralization'),
            'sharpe': data.get('sharpe'),
            'fitness': data.get('fitness'),
            'margin': data.get('margin'),
            'turnover': data.get('turnover'),
            'two_year_sharpe': data.get('two_year_sharpe'),
            'status': data.get('status', 'UNSUBMITTED'),
            'prod_correlation': data.get('prod_correlation'),
            'self_correlation': data.get('self_correlation'),
            'created_at': data.get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }
        
        existing = self.get_by_alpha_id(alpha_id)
        if existing:
            return self.db.update(self.table_name, alpha_data, "alpha_id = ?", (alpha_id,))
        else:
            return self.create(alpha_data)

class WaveDAO(BaseDAO):
    """Wave DAO"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "waves"
    
    def get_by_region_and_wave(self, region_id: int, wave_number: str) -> Optional[Dict[str, Any]]:
        """根据区域和波次获取记录"""
        return self.db.fetchone(
            "SELECT * FROM waves WHERE region_id = ? AND wave_number = ?", 
            (region_id, wave_number)
        )
    
    def get_by_region(self, region_id: int) -> List[Dict[str, Any]]:
        """获取区域的所有 wave"""
        return self.db.fetchall(
            "SELECT * FROM waves WHERE region_id = ? ORDER BY created_at DESC", 
            (region_id,)
        )
    
    def create_or_update(self, region_id: int, wave_number: str, data: Dict[str, Any]) -> int:
        """创建或更新 wave"""
        wave_data = {
            'region_id': region_id,
            'wave_number': wave_number,
            'dataset_id': data.get('dataset_id'),
            'expression_count': data.get('expression_count', 0),
            'status': data.get('status', 'pending'),
            'created_at': data.get('created_at', datetime.now().isoformat()),
            'completed_at': data.get('completed_at'),
            'updated_at': datetime.now().isoformat()
        }
        
        existing = self.get_by_region_and_wave(region_id, wave_number)
        if existing:
            return self.db.update(self.table_name, wave_data, "id = ?", (existing['id'],))
        else:
            return self.create(wave_data)

class ExpressionDAO(BaseDAO):
    """表达式 DAO"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "expressions"
    
    def get_by_wave(self, wave_id: int) -> List[Dict[str, Any]]:
        """获取 wave 的所有表达式"""
        return self.db.fetchall(
            "SELECT * FROM expressions WHERE wave_id = ? ORDER BY created_at", 
            (wave_id,)
        )
    
    def get_by_status(self, wave_id: int, status: str) -> List[Dict[str, Any]]:
        """根据状态获取表达式"""
        return self.db.fetchall(
            "SELECT * FROM expressions WHERE wave_id = ? AND status = ? ORDER BY created_at", 
            (wave_id, status)
        )
    
    def create_or_update(self, wave_id: int, expression: str, data: Dict[str, Any]) -> int:
        """创建或更新表达式"""
        expr_data = {
            'wave_id': wave_id,
            'expression': expression,
            'fingerprint': data.get('fingerprint'),
            'status': data.get('status', 'pending'),
            'alpha_id': data.get('alpha_id'),
            'sharpe': data.get('sharpe'),
            'fitness': data.get('fitness'),
            'margin': data.get('margin'),
            'turnover': data.get('turnover'),
            'created_at': data.get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }
        
        existing = self.db.fetchone(
            "SELECT * FROM expressions WHERE wave_id = ? AND expression = ?", 
            (wave_id, expression)
        )
        
        if existing:
            return self.db.update(self.table_name, expr_data, "id = ?", (existing['id'],))
        else:
            return self.create(expr_data)

class DiversityPotentialDAO(BaseDAO):
    """多样性潜力 DAO"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "diversity_potential"
    
    def get_by_region_and_dataset(self, region_id: int, dataset_id: int) -> Optional[Dict[str, Any]]:
        """根据区域和数据集获取多样性潜力"""
        return self.db.fetchone(
            "SELECT * FROM diversity_potential WHERE region_id = ? AND dataset_id = ?", 
            (region_id, dataset_id)
        )
    
    def create_or_update(self, region_id: int, dataset_id: int, data: Dict[str, Any]) -> int:
        """创建或更新多样性潜力"""
        potential_data = {
            'region_id': region_id,
            'dataset_id': dataset_id,
            'diversity_score': data.get('diversity_score'),
            'recommended_rounds': data.get('recommended_rounds'),
            'field_categories': json.dumps(data.get('field_categories', {})),
            'operator_buckets': json.dumps(data.get('operator_buckets', {})),
            'parameter_space': json.dumps(data.get('parameter_space', {})),
            'created_at': data.get('created_at', datetime.now().isoformat()),
            'updated_at': datetime.now().isoformat()
        }
        
        existing = self.get_by_region_and_dataset(region_id, dataset_id)
        if existing:
            return self.db.update(self.table_name, potential_data, "id = ?", (existing['id'],))
        else:
            return self.create(potential_data)

class BacktestResultDAO(BaseDAO):
    """回测结果 DAO（backtest_results 表）"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "backtest_results"
    
    def get_by_alpha_id(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """根据 alpha_id 获取最新一条回测结果"""
        return self.db.fetchone(
            "SELECT * FROM backtest_results WHERE alpha_id = ? ORDER BY created_at DESC LIMIT 1",
            (alpha_id,)
        )
    
    def get_by_expression(self, expression_id: int) -> List[Dict[str, Any]]:
        """获取某表达式的全部回测结果"""
        return self.db.fetchall(
            "SELECT * FROM backtest_results WHERE expression_id = ? ORDER BY created_at DESC",
            (expression_id,)
        )
    
    def get_passing(self, sharpe_min: float = 1.58, fitness_min: float = 1.0,
                    margin_min: float = 0.0005, turnover_lo: float = 0.05,
                    turnover_hi: float = 0.30) -> List[Dict[str, Any]]:
        """获取过廉价闸的回测结果（决策表 D0 直查）"""
        return self.db.fetchall(
            """SELECT * FROM backtest_results
               WHERE status = 'COMPLETE' AND sharpe > ? AND fitness >= ?
               AND margin > ? AND turnover BETWEEN ? AND ?
               ORDER BY sharpe DESC""",
            (sharpe_min, fitness_min, margin_min, turnover_lo, turnover_hi)
        )
    
    def create_or_update(self, alpha_id: str, expression_id: Optional[int],
                         data: Dict[str, Any]) -> int:
        """创建或更新回测结果（按 alpha_id 幂等）"""
        result_data = {
            'expression_id': expression_id,
            'alpha_id': alpha_id,
            'status': data.get('status', 'COMPLETE'),
            'sharpe': data.get('sharpe'),
            'fitness': data.get('fitness'),
            'turnover': data.get('turnover'),
            'margin': data.get('margin'),
            'returns': data.get('returns'),
            'drawdown': data.get('drawdown'),
            'two_year_sharpe': data.get('two_year_sharpe'),
            'sub_universe_sharpe': data.get('sub_universe_sharpe'),
            'long_count': data.get('long_count'),
            'short_count': data.get('short_count'),
            'pnl': data.get('pnl'),
            'book_size': data.get('book_size'),
            'concentrated_weight': data.get('concentrated_weight'),
            'ra_failed_count': data.get('ra_failed_count'),
            'ra_failed_checks': json.dumps(data.get('ra_failed_checks', [])),
            'ppa_failed_count': data.get('ppa_failed_count'),
            'ppa_failed_checks': json.dumps(data.get('ppa_failed_checks', [])),
        }
        
        existing = self.get_by_alpha_id(alpha_id) if alpha_id else None
        if existing:
            return self.db.update(self.table_name, result_data, "id = ?", (existing['id'],))
        else:
            result_data['created_at'] = datetime.now().isoformat()
            return self.create(result_data)

class CampaignStateDAO(BaseDAO):
    """战役状态 DAO"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)
        self.table_name = "campaign_state"
    
    def get_by_region(self, region_id: int) -> Optional[Dict[str, Any]]:
        """根据区域获取战役状态"""
        return self.db.fetchone(
            "SELECT * FROM campaign_state WHERE region_id = ?", 
            (region_id,)
        )
    
    def create_or_update(self, region_id: int, data: Dict[str, Any]) -> int:
        """创建或更新战役状态"""
        state_data = {
            'region_id': region_id,
            'current_wave': data.get('current_wave'),
            'submit_ready_count': data.get('submit_ready_count', 0),
            'target_count': data.get('target_count', 10),
            'status': data.get('status', 'active'),
            'last_updated': datetime.now().isoformat()
        }
        
        existing = self.get_by_region(region_id)
        if existing:
            return self.db.update(self.table_name, state_data, "region_id = ?", (region_id,))
        else:
            return self.create(state_data)

# 便捷函数
def get_region_dao() -> RegionDAO:
    """获取区域 DAO"""
    return RegionDAO()

def get_dataset_dao() -> DatasetDAO:
    """获取数据集 DAO"""
    return DatasetDAO()

def get_field_dao() -> FieldDAO:
    """获取字段 DAO"""
    return FieldDAO()

def get_alpha_dao() -> AlphaDAO:
    """获取 Alpha DAO"""
    return AlphaDAO()

def get_wave_dao() -> WaveDAO:
    """获取 Wave DAO"""
    return WaveDAO()

def get_expression_dao() -> ExpressionDAO:
    """获取表达式 DAO"""
    return ExpressionDAO()

def get_diversity_potential_dao() -> DiversityPotentialDAO:
    """获取多样性潜力 DAO"""
    return DiversityPotentialDAO()

def get_campaign_state_dao() -> CampaignStateDAO:
    """获取战役状态 DAO"""
    return CampaignStateDAO()

def get_backtest_result_dao() -> BacktestResultDAO:
    """获取回测结果 DAO"""
    return BacktestResultDAO()
