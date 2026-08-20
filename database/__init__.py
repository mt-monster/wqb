"""
WQB 数据库模块
提供数据库存储和访问功能
"""

from .db_manager import DatabaseManager, get_db_manager, init_database
from .dao import (
    RegionDAO, DatasetDAO, FieldDAO, AlphaDAO, WaveDAO, 
    ExpressionDAO, DiversityPotentialDAO, CampaignStateDAO, BacktestResultDAO,
    get_region_dao, get_dataset_dao, get_field_dao, 
    get_alpha_dao, get_wave_dao, get_expression_dao,
    get_diversity_potential_dao, get_campaign_state_dao, get_backtest_result_dao
)
from .integration import (
    DatabaseIntegration, get_database_integration,
    save_diversity_potential, load_diversity_potential,
    save_wave_expressions, load_wave_expressions,
    save_alpha_result, save_backtest_results, get_submit_ready_alphas, get_campaign_progress
)
from .adapter import (
    DatabaseAdapter, get_database_adapter,
    enable_database_mode, disable_database_mode
)
from .migrate import DataMigrator
from .init_db import init_wqb_database

__version__ = "1.0.0"
__all__ = [
    "DatabaseManager", "get_db_manager", "init_database",
    "RegionDAO", "DatasetDAO", "FieldDAO", "AlphaDAO", "WaveDAO",
    "ExpressionDAO", "DiversityPotentialDAO", "CampaignStateDAO", "BacktestResultDAO",
    "get_region_dao", "get_dataset_dao", "get_field_dao",
    "get_alpha_dao", "get_wave_dao", "get_expression_dao",
    "get_diversity_potential_dao", "get_campaign_state_dao", "get_backtest_result_dao",
    "DatabaseIntegration", "get_database_integration",
    "save_diversity_potential", "load_diversity_potential",
    "save_wave_expressions", "load_wave_expressions",
    "save_alpha_result", "save_backtest_results", "get_submit_ready_alphas", "get_campaign_progress",
    "DatabaseAdapter", "get_database_adapter",
    "enable_database_mode", "disable_database_mode",
    "DataMigrator", "init_wqb_database"
]
