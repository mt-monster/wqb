"""
数据库初始化脚本
创建数据库表结构并迁移现有数据
"""

import logging
import os
from pathlib import Path
from typing import Optional

from db_manager import init_database
from migrate import DataMigrator

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


def init_wqb_database(workspace_root: Optional[str] = None,
                      db_path: str = "data/wqb.db",
                      migrate_data: bool = True):
    """初始化 WQB 数据库

    Args:
        workspace_root: 工作区根目录（可配；缺省读 WQ_PROJECT_ROOT，再回退项目根）
        db_path: 数据库文件路径（相对路径时锚定在 workspace_root 下）
        migrate_data: 是否迁移现有数据
    """
    root = resolve_workspace_root(workspace_root)
    db_p = Path(db_path)
    if not db_p.is_absolute():
        db_p = root / db_p

    logger.info("初始化 WQB 数据库...")

    # 1. 初始化数据库
    db_manager = init_database(str(db_p))
    logger.info(f"数据库初始化完成: {db_p}")

    # 2. 迁移现有数据
    if migrate_data:
        migrator = DataMigrator(str(root))
        migrator.migrate_all()
        logger.info("数据迁移完成")

    return db_manager

def main():
    """主函数"""
    logging.basicConfig(level=logging.INFO)
    
    # 初始化数据库
    db_manager = init_wqb_database()
    
    # 打印统计信息
    print("\n=== 数据库统计 ===")
    tables = db_manager.get_tables()
    for table in tables:
        count = db_manager.fetchone(f"SELECT COUNT(*) as count FROM {table}")
        print(f"{table}: {count['count']} 条记录")

if __name__ == "__main__":
    main()
