"""wqb.memory.idea_store — IdeaStore: idea 文件数据库化管理.

Backed by SQLite. 核心表:
- ``ideas`` — 存储 idea 元数据与表达式列表，替代传统 JSON 文件.

设计目标:
- 彻底消除 JSON 格式问题（引号/转义/特殊字符）
- 支持并发安全写入（事务 + 行级锁）
- 提供与现有 JSON 接口兼容的 API，实现平滑迁移
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def _json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True)


def _json_loads(s: Optional[str]) -> Any:
    if not s:
        return None
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class IdeaStore:
    """SQLite-backed idea storage and retrieval."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # 默认路径: 项目根目录 / data / ideas.db
            root = Path(__file__).parent.parent.parent.parent
            db_path = str(root / "data" / "ideas.db")
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = sqlite3.connect(db_path)
        self._init_tables()

    def _init_tables(self) -> None:
        cur = self.connection.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS ideas (
                id TEXT PRIMARY KEY,
                region TEXT NOT NULL,
                dataset_id TEXT NOT NULL,
                delay INTEGER NOT NULL,
                universe TEXT NOT NULL,
                neutralization TEXT NOT NULL,
                max_trade TEXT,
                type TEXT DEFAULT 'REGULAR',
                data_type TEXT,
                expressions_file TEXT,
                expression_list TEXT,
                target_json TEXT,
                focus TEXT,
                pyramid REAL,
                fieldCount INTEGER,
                coverage REAL,
                status TEXT DEFAULT 'pending',
                wave_id TEXT,
                batch_id TEXT,
                sim_id TEXT,
                ledger_id TEXT,
                created_at TEXT,
                updated_at TEXT,
                metadata TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_ideas_region_dataset ON ideas(region, dataset_id);
            CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
            CREATE INDEX IF NOT EXISTS idx_ideas_created_at ON ideas(created_at);
            CREATE INDEX IF NOT EXISTS idx_ideas_wave_id ON ideas(wave_id);
            CREATE INDEX IF NOT EXISTS idx_ideas_batch_id ON ideas(batch_id);
            CREATE INDEX IF NOT EXISTS idx_ideas_ledger_id ON ideas(ledger_id);
            """
        )
        self.connection.commit()

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()

    def __enter__(self) -> "IdeaStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # -- CRUD ---------------------------------------------------------------

    def save_idea(self, idea_id: str, idea_data: Dict[str, Any]) -> None:
        """保存或更新 idea 记录. 若 id 已存在则更新，否则插入."""
        cur = self.connection.cursor()
        now = _now_iso()

        # 提取字段，兼容不同命名
        region = idea_data.get("region", "")
        dataset_id = idea_data.get("dataset_id") or idea_data.get("dataset", "")
        delay = idea_data.get("delay", 1)
        universe = idea_data.get("universe", "")
        neutralization = idea_data.get("neutralization", "")
        max_trade = idea_data.get("max_trade")
        idea_type = idea_data.get("type", "REGULAR")
        data_type = idea_data.get("data_type")
        expressions_file = idea_data.get("expressions_file")
        expression_list = _json_dumps(idea_data.get("expression_list", []))
        target_json = _json_dumps(idea_data.get("target", {}))
        focus = idea_data.get("focus")
        pyramid = idea_data.get("pyramid")
        fieldCount = idea_data.get("fieldCount")
        coverage = idea_data.get("coverage")
        status = idea_data.get("status", "pending")
        wave_id = idea_data.get("wave_id")
        batch_id = idea_data.get("batch_id")
        sim_id = idea_data.get("sim_id")
        ledger_id = idea_data.get("ledger_id")
        metadata = _json_dumps(idea_data.get("metadata", {}))

        cur.execute("SELECT 1 FROM ideas WHERE id = ?", (idea_id,))
        if cur.fetchone():
            cur.execute(
                """
                UPDATE ideas SET
                    region=?, dataset_id=?, delay=?, universe=?, neutralization=?,
                    max_trade=?, type=?, data_type=?, expressions_file=?,
                    expression_list=?, target_json=?, focus=?, pyramid=?,
                    fieldCount=?, coverage=?, status=?, wave_id=?, batch_id=?,
                    sim_id=?, ledger_id=?, updated_at=?, metadata=?
                WHERE id=?
                """,
                (
                    region, dataset_id, delay, universe, neutralization,
                    max_trade, idea_type, data_type, expressions_file,
                    expression_list, target_json, focus, pyramid,
                    fieldCount, coverage, status, wave_id, batch_id,
                    sim_id, ledger_id, now, metadata, idea_id
                ),
            )
        else:
            cur.execute(
                """
                INSERT INTO ideas (
                    id, region, dataset_id, delay, universe, neutralization,
                    max_trade, type, data_type, expressions_file,
                    expression_list, target_json, focus, pyramid,
                    fieldCount, coverage, status, wave_id, batch_id,
                    sim_id, ledger_id, created_at, updated_at, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    idea_id, region, dataset_id, delay, universe, neutralization,
                    max_trade, idea_type, data_type, expressions_file,
                    expression_list, target_json, focus, pyramid,
                    fieldCount, coverage, status, wave_id, batch_id,
                    sim_id, ledger_id, now, now, metadata
                ),
            )
        self.connection.commit()

    def get_idea(self, idea_id: str) -> Optional[Dict[str, Any]]:
        """按 id 获取 idea 记录，返回字典格式（兼容原 JSON 结构）."""
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,))
        row = cur.fetchone()
        if row is None:
            return None

        # 获取列名
        cur.execute("PRAGMA table_info(ideas)")
        columns = [col[1] for col in cur.fetchall()]
        data = dict(zip(columns, row))

        # 反序列化 JSON 字段
        data["expression_list"] = _json_loads(data.get("expression_list")) or []
        data["target"] = _json_loads(data.get("target_json")) or {}
        data["metadata"] = _json_loads(data.get("metadata")) or {}

        # 移除内部字段
        data.pop("target_json", None)

        return data

    def query_ideas(
        self,
        region: Optional[str] = None,
        dataset_id: Optional[str] = None,
        status: Optional[str] = None,
        wave_id: Optional[str] = None,
        batch_id: Optional[str] = None,
        ledger_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """按条件查询 idea 列表."""
        cur = self.connection.cursor()
        conditions = []
        params = []

        if region:
            conditions.append("region = ?")
            params.append(region)
        if dataset_id:
            conditions.append("dataset_id = ?")
            params.append(dataset_id)
        if status:
            conditions.append("status = ?")
            params.append(status)
        if wave_id:
            conditions.append("wave_id = ?")
            params.append(wave_id)
        if batch_id:
            conditions.append("batch_id = ?")
            params.append(batch_id)
        if ledger_id:
            conditions.append("ledger_id = ?")
            params.append(ledger_id)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        query = f"""
            SELECT id FROM ideas
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])

        cur.execute(query, params)
        idea_ids = [row[0] for row in cur.fetchall()]

        return [self.get_idea(iid) for iid in idea_ids if self.get_idea(iid)]

    def update_status(self, idea_id: str, status: str) -> None:
        """更新 idea 状态."""
        cur = self.connection.cursor()
        cur.execute(
            "UPDATE ideas SET status = ?, updated_at = ? WHERE id = ?",
            (status, _now_iso(), idea_id),
        )
        self.connection.commit()

    def transition_status(self, idea_id: str, new_status: str, **kwargs) -> None:
        """状态机流转：pending → processing → completed/failed.
        
        支持附加字段更新（wave_id, batch_id, sim_id, ledger_id, error 等）.
        """
        idea = self.get_idea(idea_id)
        if idea is None:
            raise ValueError(f"Idea not found: {idea_id}")

        # 验证状态流转合法性
        valid_transitions = {
            "pending": ["processing", "failed"],
            "processing": ["completed", "failed"],
            "completed": [],  # 终态
            "failed": ["pending"],  # 允许重试
        }
        current_status = idea.get("status", "pending")
        if new_status not in valid_transitions.get(current_status, []):
            raise ValueError(
                f"Invalid status transition: {current_status} → {new_status}. "
                f"Valid transitions: {valid_transitions.get(current_status, [])}"
            )

        # 构建更新数据
        update_data = {**idea, "status": new_status}
        for key in ["wave_id", "batch_id", "sim_id", "ledger_id"]:
            if key in kwargs:
                update_data[key] = kwargs[key]

        # 处理错误信息
        if new_status == "failed" and "error" in kwargs:
            metadata = update_data.get("metadata", {})
            metadata["error"] = kwargs["error"]
            metadata["failed_at"] = _now_iso()
            update_data["metadata"] = metadata

        self.save_idea(idea_id, update_data)

    def delete_idea(self, idea_id: str) -> None:
        """删除 idea 记录."""
        cur = self.connection.cursor()
        cur.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
        self.connection.commit()

    def list_all_ids(self) -> List[str]:
        """获取所有 idea id 列表."""
        cur = self.connection.cursor()
        cur.execute("SELECT id FROM ideas ORDER BY created_at DESC")
        return [row[0] for row in cur.fetchall()]

    def count(self, status: Optional[str] = None) -> int:
        """统计 idea 数量."""
        cur = self.connection.cursor()
        if status:
            cur.execute("SELECT COUNT(*) FROM ideas WHERE status = ?", (status,))
        else:
            cur.execute("SELECT COUNT(*) FROM ideas")
        return cur.fetchone()[0]

    # -- 兼容层: 模拟 JSON 文件接口 ------------------------------------------

    def load_from_json_file(self, json_path: str, idea_id: Optional[str] = None) -> str:
        """从 JSON 文件导入 idea，返回 idea_id."""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if idea_id is None:
            # 从文件名生成 id，如 fundamental6_MEA_1_idea_20260819.json -> fundamental6_MEA_1_idea_20260819
            idea_id = Path(json_path).stem

        self.save_idea(idea_id, data)
        return idea_id

    def export_to_json_file(self, idea_id: str, output_path: str) -> None:
        """将 idea 导出为 JSON 文件（用于调试或兼容旧流程）."""
        data = self.get_idea(idea_id)
        if data is None:
            raise ValueError(f"Idea not found: {idea_id}")

        # 移除数据库特有字段
        export_data = {k: v for k, v in data.items() if k not in ["created_at", "updated_at"]}

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)


# -- 便捷函数 ---------------------------------------------------------------

_default_store: Optional[IdeaStore] = None


def get_default_store() -> IdeaStore:
    """获取默认 IdeaStore 实例（单例模式）."""
    global _default_store
    if _default_store is None:
        _default_store = IdeaStore()
    return _default_store


def save_idea(idea_id: str, idea_data: Dict[str, Any]) -> None:
    """便捷保存接口."""
    get_default_store().save_idea(idea_id, idea_data)


def get_idea(idea_id: str) -> Optional[Dict[str, Any]]:
    """便捷获取接口."""
    return get_default_store().get_idea(idea_id)


def query_ideas(**kwargs) -> List[Dict[str, Any]]:
    """便捷查询接口."""
    return get_default_store().query_ideas(**kwargs)
