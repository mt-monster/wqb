"""
数据库集成接口
提供与现有流程兼容的数据库操作接口
"""

import json
import logging
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from db_manager import get_db_manager
from dao import (
    get_region_dao, get_dataset_dao, get_field_dao, 
    get_alpha_dao, get_wave_dao, get_expression_dao,
    get_diversity_potential_dao, get_campaign_state_dao,
    get_backtest_result_dao
)

logger = logging.getLogger(__name__)

# 项目根目录：database/ 的上一级，不依赖当前工作目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_workspace_root(workspace_root: Optional[str] = None) -> Path:
    """解析工作区根目录。

    优先级：显式参数 > 环境变量 WQ_PROJECT_ROOT > 项目根（__file__ 推导）。
    消除硬编码绝对路径 D:\\coding\\traeCN_project\\wqb 对 cwd/账号的耦合。
    """
    if workspace_root:
        return Path(workspace_root)
    env_root = os.environ.get("WQ_PROJECT_ROOT")
    if env_root:
        return Path(env_root)
    return PROJECT_ROOT


class DatabaseIntegration:
    """数据库集成类"""

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = resolve_workspace_root(workspace_root)
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
        self.backtest_dao = get_backtest_result_dao()
    
    def save_diversity_potential(self, region: str, dataset: str, data: Dict[str, Any]):
        """保存多样性潜力报告（替代 diversity_potential.json）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            logger.error(f"区域不存在: {region}")
            return
        
        dataset_obj = self.dataset_dao.get_by_name_and_region(dataset, region_obj['id'])
        if not dataset_obj:
            logger.error(f"数据集不存在: {region}/{dataset}")
            return
        
        self.diversity_dao.create_or_update(region_obj['id'], dataset_obj['id'], data)
        logger.info(f"保存多样性潜力: {region}/{dataset}")
    
    def load_diversity_potential(self, region: str, dataset: str) -> Optional[Dict[str, Any]]:
        """加载多样性潜力报告（替代 diversity_potential.json）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            return None
        
        dataset_obj = self.dataset_dao.get_by_name_and_region(dataset, region_obj['id'])
        if not dataset_obj:
            return None
        
        result = self.diversity_dao.get_by_region_and_dataset(region_obj['id'], dataset_obj['id'])
        if result:
            # 解析 JSON 字段
            result['field_categories'] = json.loads(result.get('field_categories', '{}'))
            result['operator_buckets'] = json.loads(result.get('operator_buckets', '{}'))
            result['parameter_space'] = json.loads(result.get('parameter_space', '{}'))
        
        return result
    
    def save_wave_expressions(self, region: str, wave: str, expressions: List[Dict[str, Any]]):
        """保存 wave 表达式（替代 wave<TAG>_exprs.json）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            logger.error(f"区域不存在: {region}")
            return
        
        # 创建或更新 wave
        wave_data = {
            'expression_count': len(expressions),
            'status': 'completed',
            'created_at': datetime.now().isoformat()
        }
        
        wave_obj = self.wave_dao.get_by_region_and_wave(region_obj['id'], wave)
        if wave_obj:
            wave_id = wave_obj['id']
            self.wave_dao.update(wave_id, wave_data)
        else:
            wave_id = self.wave_dao.create_or_update(region_obj['id'], wave, wave_data)
        
        # 保存表达式（兼容 str 和 dict 两种格式）
        for expr in expressions:
            if isinstance(expr, str):
                expr_str = expr
                expr_data = {
                    'fingerprint': None,
                    'status': 'pending',
                    'alpha_id': None,
                    'sharpe': None,
                    'fitness': None,
                    'margin': None,
                    'turnover': None,
                    'created_at': datetime.now().isoformat()
                }
            else:
                expr_str = expr.get('expression', expr.get('expr', ''))
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
            
            if expr_str:
                self.expression_dao.create_or_update(wave_id, expr_str, expr_data)
        
        logger.info(f"保存 wave 表达式: {region}/{wave} ({len(expressions)} 个表达式)")
    
    def load_wave_expressions(self, region: str, wave: str) -> List[Dict[str, Any]]:
        """加载 wave 表达式（替代 wave<TAG>_exprs.json）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            return []
        
        wave_obj = self.wave_dao.get_by_region_and_wave(region_obj['id'], wave)
        if not wave_obj:
            return []
        
        expressions = self.expression_dao.get_by_wave(wave_obj['id'])
        return expressions
    
    def save_alpha_result(self, alpha_id: str, region: str, dataset: str, 
                         expression: str, settings: Dict[str, Any], 
                         metrics: Dict[str, Any]):
        """保存 alpha 结果（替代结果 CSV）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            logger.error(f"区域不存在: {region}")
            return
        
        dataset_obj = self.dataset_dao.get_by_name_and_region(dataset, region_obj['id'])
        if not dataset_obj:
            logger.error(f"数据集不存在: {region}/{dataset}")
            return
        
        alpha_data = {
            'expression': expression,
            'region_id': region_obj['id'],
            'dataset_id': dataset_obj['id'],
            'universe': settings.get('universe'),
            'delay': settings.get('delay'),
            'neutralization': settings.get('neutralization'),
            'sharpe': metrics.get('sharpe'),
            'fitness': metrics.get('fitness'),
            'margin': metrics.get('margin'),
            'turnover': metrics.get('turnover'),
            'two_year_sharpe': metrics.get('two_year_sharpe'),
            'status': metrics.get('status', 'UNSUBMITTED'),
            'prod_correlation': metrics.get('prod_correlation'),
            'self_correlation': metrics.get('self_correlation'),
            'created_at': datetime.now().isoformat()
        }
        
        self.alpha_dao.create_or_update(alpha_id, alpha_data)
        logger.info(f"保存 alpha 结果: {alpha_id}")
    
    def save_backtest_results(self, region: str, wave: str, rows: List[Dict[str, Any]]) -> int:
        """批量保存回测结果到 backtest_results 表（pipeline stage_review 调用）
        
        rows 来自 metrics_cache.fetch_rows，字段：
        {id, code, neut, sharpe, fitness, two_year_sharpe, margin_bp, turnover_pct,
         rn_sharpe, rn_fitness, failed_checks, cached_at}
        注意单位换算：margin_bp -> margin（/10000），turnover_pct -> turnover（/100）
        """
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            logger.error(f"区域不存在: {region}")
            return 0
        
        # 找 wave 下表达式，建立 expression -> expression_id 映射
        wave_obj = self.wave_dao.get_by_region_and_wave(region_obj['id'], wave)
        expr_map = {}
        if wave_obj:
            for e in self.expression_dao.get_by_wave(wave_obj['id']):
                # code 截断 110 字符对齐 metrics_cache.row_from_alpha
                expr_map[(e.get('expression') or '')[:110]] = e.get('id')
        
        saved = 0
        skipped = 0
        for r in rows:
            alpha_id = r.get('id')
            if not alpha_id or r.get('error'):
                continue
            margin_bp = r.get('margin_bp')
            turnover_pct = r.get('turnover_pct')
            data = {
                'status': 'COMPLETE',
                'sharpe': r.get('sharpe'),
                'fitness': r.get('fitness'),
                'two_year_sharpe': r.get('two_year_sharpe'),
                'margin': (margin_bp / 10000.0) if margin_bp is not None else None,
                'turnover': (turnover_pct / 100.0) if turnover_pct is not None else None,
                'ra_failed_count': len(r.get('failed_checks') or []),
                'ra_failed_checks': r.get('failed_checks') or [],
            }
            # expression_id 为 NOT NULL：先按 wave 内映射，再全局按表达式文本兜底，仍无则跳过
            expression_id = expr_map.get((r.get('code') or '')[:110])
            if expression_id is None:
                expression_id = self._find_expression_id_by_text((r.get('code') or '')[:110])
            if expression_id is None:
                logger.warning(f"回测结果跳过 {alpha_id}: 找不到对应 expression（wave={wave}）")
                skipped += 1
                continue
            try:
                self.backtest_dao.create_or_update(alpha_id, expression_id, data)
                saved += 1
            except Exception as e:
                logger.warning(f"回测结果入库失败 {alpha_id}: {e}")
        
        logger.info(f"保存回测结果: {region}/{wave} ({saved} 入 backtest_results, {skipped} 跳过)")
        return saved
    
    def _find_expression_id_by_text(self, expr_text: str) -> Optional[int]:
        """按表达式文本在 expressions 表全局查找 id（兜底）"""
        if not expr_text:
            return None
        row = self.db.fetchone(
            "SELECT id FROM expressions WHERE substr(expression, 1, 110) = ? LIMIT 1",
            (expr_text,)
        )
        return row['id'] if row else None
    
    def get_submit_ready_alphas(self, region: str) -> List[Dict[str, Any]]:
        """获取可提交的 alpha（替代手动筛选）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            return []
        
        return self.alpha_dao.get_submit_ready(region_obj['id'])
    
    def get_campaign_progress(self, region: str) -> Dict[str, Any]:
        """获取战役进度（替代手动统计）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            return {}
        
        # 获取战役状态
        campaign_state = self.campaign_dao.get_by_region(region_obj['id'])
        
        # 获取统计信息
        total_waves = len(self.wave_dao.get_by_region(region_obj['id']))
        total_alphas = len(self.alpha_dao.get_by_region_and_dataset(region_obj['id'], None))
        submit_ready = len(self.get_submit_ready_alphas(region))
        
        return {
            'region': region,
            'total_waves': total_waves,
            'total_alphas': total_alphas,
            'submit_ready': submit_ready,
            'target_count': campaign_state.get('target_count', 10) if campaign_state else 10,
            'status': campaign_state.get('status', 'active') if campaign_state else 'active',
            'last_updated': campaign_state.get('last_updated') if campaign_state else None
        }
    
    def get_dataset_whitelist(self, region: str) -> List[Dict[str, Any]]:
        """获取数据集白名单（替代 score_datasets.py 输出）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            return []
        
        return self.dataset_dao.get_whitelist(region_obj['id'])
    
    def get_field_catalog(self, region: str, dataset: str) -> List[Dict[str, Any]]:
        """获取字段目录（替代 scan_fields.py 输出）"""
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            return []
        
        dataset_obj = self.dataset_dao.get_by_name_and_region(dataset, region_obj['id'])
        if not dataset_obj:
            return []
        
        return self.field_dao.get_by_dataset(dataset_obj['id'])
    
    def export_to_json(self, region: str, output_dir: str):
        """导出数据到 JSON 文件（兼容性接口）"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            logger.error(f"区域不存在: {region}")
            return
        
        # 导出多样性潜力
        datasets = self.dataset_dao.get_by_region(region_obj['id'])
        for dataset in datasets:
            diversity = self.diversity_dao.get_by_region_and_dataset(region_obj['id'], dataset['id'])
            if diversity:
                diversity_file = output_path / f"{region}_{dataset['name']}_diversity_potential.json"
                with open(diversity_file, 'w', encoding='utf-8') as f:
                    json.dump(diversity, f, indent=2, ensure_ascii=False)
        
        # 导出 wave 表达式
        waves = self.wave_dao.get_by_region(region_obj['id'])
        for wave in waves:
            expressions = self.expression_dao.get_by_wave(wave['id'])
            if expressions:
                wave_file = output_path / f"{region}_wave{wave['wave_number']}_exprs.json"
                with open(wave_file, 'w', encoding='utf-8') as f:
                    json.dump({'expressions': expressions}, f, indent=2, ensure_ascii=False)
        
        logger.info(f"导出数据到 JSON: {output_dir}")
    
    def import_from_json(self, region: str, input_dir: str):
        """从 JSON 文件导入数据（兼容性接口）"""
        input_path = Path(input_dir)
        if not input_path.exists():
            logger.error(f"输入目录不存在: {input_dir}")
            return
        
        region_obj = self.region_dao.get_by_name(region)
        if not region_obj:
            logger.error(f"区域不存在: {region}")
            return
        
        # 导入多样性潜力
        for diversity_file in input_path.glob(f"{region}_*_diversity_potential.json"):
            dataset_name = diversity_file.stem.replace(f"{region}_", "").replace("_diversity_potential", "")
            
            with open(diversity_file, 'r', encoding='utf-8') as f:
                diversity_data = json.load(f)
            
            self.save_diversity_potential(region, dataset_name, diversity_data)
        
        # 导入 wave 表达式
        for wave_file in input_path.glob(f"{region}_wave*_exprs.json"):
            wave_number = wave_file.stem.replace(f"{region}_wave", "").replace("_exprs", "")
            
            with open(wave_file, 'r', encoding='utf-8') as f:
                wave_data = json.load(f)
            
            expressions = wave_data.get('expressions', [])
            self.save_wave_expressions(region, wave_number, expressions)
        
        logger.info(f"从 JSON 导入数据: {input_dir}")

# 便捷函数
def get_database_integration() -> DatabaseIntegration:
    """获取数据库集成实例"""
    return DatabaseIntegration()

def save_diversity_potential(region: str, dataset: str, data: Dict[str, Any]):
    """保存多样性潜力报告"""
    integration = get_database_integration()
    integration.save_diversity_potential(region, dataset, data)

def load_diversity_potential(region: str, dataset: str) -> Optional[Dict[str, Any]]:
    """加载多样性潜力报告"""
    integration = get_database_integration()
    return integration.load_diversity_potential(region, dataset)

def save_wave_expressions(region: str, wave: str, expressions: List[Dict[str, Any]]):
    """保存 wave 表达式"""
    integration = get_database_integration()
    integration.save_wave_expressions(region, wave, expressions)

def load_wave_expressions(region: str, wave: str) -> List[Dict[str, Any]]:
    """加载 wave 表达式"""
    integration = get_database_integration()
    return integration.load_wave_expressions(region, wave)

def save_alpha_result(alpha_id: str, region: str, dataset: str, 
                     expression: str, settings: Dict[str, Any], 
                     metrics: Dict[str, Any]):
    """保存 alpha 结果"""
    integration = get_database_integration()
    integration.save_alpha_result(alpha_id, region, dataset, expression, settings, metrics)

def save_backtest_results(region: str, wave: str, rows: List[Dict[str, Any]]) -> int:
    """批量保存回测结果到 backtest_results 表"""
    integration = get_database_integration()
    return integration.save_backtest_results(region, wave, rows)

def get_submit_ready_alphas(region: str) -> List[Dict[str, Any]]:
    """获取可提交的 alpha"""
    integration = get_database_integration()
    return integration.get_submit_ready_alphas(region)

def get_campaign_progress(region: str) -> Dict[str, Any]:
    """获取战役进度"""
    integration = get_database_integration()
    return integration.get_campaign_progress(region)
