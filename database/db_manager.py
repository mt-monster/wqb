"""
数据库连接管理器
支持 SQLite 和 PostgreSQL
"""

import sqlite3
import json
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseManager:
    """数据库连接管理器"""
    
    def __init__(self, db_path: str = "data/wqb.db"):
        """初始化数据库管理器
        
        Args:
            db_path: 数据库文件路径（SQLite）
        """
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """确保数据库目录存在"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """初始化数据库"""
        with self.get_connection() as conn:
            # 读取 schema 文件
            schema_path = Path(__file__).parent / "schema.sql"
            if schema_path.exists():
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_sql = f.read()
                
                # 检查表是否已存在
                existing_tables = self.get_tables()
                if not existing_tables:
                    # 如果没有表，则执行 schema
                    conn.executescript(schema_sql)
                    conn.commit()
                    logger.info(f"数据库初始化完成: {self.db_path}")
                else:
                    logger.info(f"数据库已存在，跳过初始化: {self.db_path}")
            else:
                logger.warning(f"Schema 文件不存在: {schema_path}")
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接（上下文管理器）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 返回字典式结果
        try:
            yield conn
        finally:
            conn.close()
    
    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """执行 SQL 语句"""
        with self.get_connection() as conn:
            cursor = conn.execute(sql, params)
            conn.commit()
            return cursor
    
    def executemany(self, sql: str, params_list: List[tuple]) -> sqlite3.Cursor:
        """批量执行 SQL 语句"""
        with self.get_connection() as conn:
            cursor = conn.executemany(sql, params_list)
            conn.commit()
            return cursor
    
    def fetchone(self, sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """查询单条记录"""
        with self.get_connection() as conn:
            cursor = conn.execute(sql, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def fetchall(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """查询多条记录"""
        with self.get_connection() as conn:
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """插入记录"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, tuple(data.values()))
            conn.commit()
            return cursor.lastrowid
    
    def update(self, table: str, data: Dict[str, Any], where: str, where_params: tuple = ()) -> int:
        """更新记录"""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, tuple(data.values()) + where_params)
            conn.commit()
            return cursor.rowcount
    
    def delete(self, table: str, where: str, where_params: tuple = ()) -> int:
        """删除记录"""
        sql = f"DELETE FROM {table} WHERE {where}"
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, where_params)
            conn.commit()
            return cursor.rowcount
    
    def upsert(self, table: str, data: Dict[str, Any], unique_keys: List[str]) -> int:
        """插入或更新记录（UPSERT）"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        update_clause = ', '.join([f"{k} = excluded.{k}" for k in data.keys() if k not in unique_keys])
        
        sql = f"""
            INSERT INTO {table} ({columns}) 
            VALUES ({placeholders})
            ON CONFLICT ({', '.join(unique_keys)}) 
            DO UPDATE SET {update_clause}
        """
        
        with self.get_connection() as conn:
            cursor = conn.execute(sql, tuple(data.values()))
            conn.commit()
            return cursor.lastrowid
    
    def transaction(self):
        """事务上下文管理器"""
        return self.get_connection()
    
    def backup(self, backup_path: str):
        """备份数据库"""
        with self.get_connection() as conn:
            backup_conn = sqlite3.connect(backup_path)
            conn.backup(backup_conn)
            backup_conn.close()
            logger.info(f"数据库备份完成: {backup_path}")
    
    def get_table_info(self, table: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        return self.fetchall(f"PRAGMA table_info({table})")
    
    def get_tables(self) -> List[str]:
        """获取所有表名"""
        rows = self.fetchall("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        return [row['name'] for row in rows]

# 全局数据库管理器实例
_db_manager: Optional[DatabaseManager] = None

def get_db_manager(db_path: str = "data/wqb.db") -> DatabaseManager:
    """获取全局数据库管理器实例"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(db_path)
    return _db_manager

def init_database(db_path: str = "data/wqb.db") -> DatabaseManager:
    """初始化数据库"""
    global _db_manager
    _db_manager = DatabaseManager(db_path)
    return _db_manager
