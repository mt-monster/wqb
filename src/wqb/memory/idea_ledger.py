"""wqb.memory.idea_ledger — IdeaLedger: idea + wave + sim 全链路集成管理.

整合 IdeaStore 与 SimulationDB，实现：
- idea 生成 → wave 构建 → batch 回测 → sim 结果 的全链路追踪
- 状态机驱动：pending → processing → completed/failed
- 与 ledger.json / WAVE_LEDGER.md 双向同步
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .idea_store import IdeaStore
from .db import SimulationDB


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class IdeaLedger:
    """Idea + Wave + Sim 全链路集成管理器."""

    def __init__(
        self,
        idea_db_path: Optional[str] = None,
        sim_db_path: Optional[str] = None,
        ledger_root: Optional[str] = None,
    ):
        self.idea_store = IdeaStore(idea_db_path)
        self.sim_db = SimulationDB(sim_db_path) if sim_db_path else None
        self.ledger_root = Path(ledger_root) if ledger_root else Path("tracking")

    def close(self) -> None:
        self.idea_store.close()
        if self.sim_db:
            self.sim_db.close()

    def __enter__(self) -> "IdeaLedger":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # -- Idea 生命周期 ------------------------------------------------------

    def create_idea(
        self,
        idea_id: str,
        region: str,
        dataset_id: str,
        delay: int,
        universe: str,
        neutralization: str,
        expression_list: List[str],
        **kwargs,
    ) -> str:
        """创建新 idea，状态为 pending."""
        idea_data = {
            "region": region,
            "dataset_id": dataset_id,
            "delay": delay,
            "universe": universe,
            "neutralization": neutralization,
            "expression_list": expression_list,
            "status": "pending",
            **kwargs,
        }
        self.idea_store.save_idea(idea_id, idea_data)
        return idea_id

    def start_processing(self, idea_id: str, wave_id: Optional[str] = None) -> None:
        """标记 idea 进入处理中，关联 wave."""
        idea = self.idea_store.get_idea(idea_id)
        if idea is None:
            raise ValueError(f"Idea not found: {idea_id}")

        update_data = {"status": "processing"}
        if wave_id:
            update_data["wave_id"] = wave_id

        self.idea_store.save_idea(idea_id, {**idea, **update_data})

    def complete_idea(
        self,
        idea_id: str,
        batch_id: Optional[str] = None,
        sim_id: Optional[str] = None,
        ledger_id: Optional[str] = None,
    ) -> None:
        """标记 idea 完成，关联 batch/sim/ledger."""
        idea = self.idea_store.get_idea(idea_id)
        if idea is None:
            raise ValueError(f"Idea not found: {idea_id}")

        update_data = {"status": "completed"}
        if batch_id:
            update_data["batch_id"] = batch_id
        if sim_id:
            update_data["sim_id"] = sim_id
        if ledger_id:
            update_data["ledger_id"] = ledger_id

        self.idea_store.save_idea(idea_id, {**idea, **update_data})

    def fail_idea(self, idea_id: str, error: str, **kwargs) -> None:
        """标记 idea 失败，记录错误信息."""
        idea = self.idea_store.get_idea(idea_id)
        if idea is None:
            raise ValueError(f"Idea not found: {idea_id}")

        metadata = idea.get("metadata", {})
        metadata["error"] = error
        metadata["failed_at"] = _now_iso()
        metadata.update(kwargs)

        update_data = {
            "status": "failed",
            "metadata": metadata,
        }

        self.idea_store.save_idea(idea_id, {**idea, **update_data})

    # -- Wave 集成 ----------------------------------------------------------

    def create_wave(
        self,
        wave_id: str,
        region: str,
        dataset_id: str,
        idea_ids: List[str],
        strategy: str,
        **kwargs,
    ) -> str:
        """创建 wave，关联多个 idea."""
        # 更新所有关联 idea 的 wave_id 和状态
        for idea_id in idea_ids:
            idea = self.idea_store.get_idea(idea_id)
            if idea:
                self.idea_store.save_idea(idea_id, {
                    **idea,
                    "wave_id": wave_id,
                    "status": "processing",
                })

        # 记录 wave 元数据到 ledger
        wave_meta = {
            "wave_id": wave_id,
            "region": region,
            "dataset_id": dataset_id,
            "idea_ids": idea_ids,
            "strategy": strategy,
            "created_at": _now_iso(),
            **kwargs,
        }

        wave_dir = self.ledger_root / region / "waves"
        wave_dir.mkdir(parents=True, exist_ok=True)
        wave_file = wave_dir / f"{wave_id}.json"
        with open(wave_file, "w", encoding="utf-8") as f:
            json.dump(wave_meta, f, ensure_ascii=False, indent=2)

        return wave_id

    def get_wave_ideas(self, wave_id: str) -> List[Dict[str, Any]]:
        """获取 wave 关联的所有 idea."""
        return self.idea_store.query_ideas(wave_id=wave_id)

    # -- Batch/Sim 集成 -----------------------------------------------------

    def record_batch(
        self,
        batch_id: str,
        wave_id: str,
        expressions: List[str],
        results: List[Any],
        session_id: Optional[str] = None,
    ) -> str:
        """记录 batch 回测结果，更新关联 idea."""
        # 更新 wave 下所有 idea 的 batch_id
        ideas = self.get_wave_ideas(wave_id)
        for idea in ideas:
            self.idea_store.save_idea(idea["id"], {
                **idea,
                "batch_id": batch_id,
            })

        # 记录到 SimulationDB
        if self.sim_db and session_id:
            self.sim_db.record_batch(session_id, batch_id, expressions, results)

        return batch_id

    def record_sim_result(
        self,
        sim_id: str,
        idea_id: str,
        expression: str,
        settings: Dict[str, Any],
        result: Dict[str, Any],
    ) -> str:
        """记录单个 sim 结果，更新 idea 状态."""
        idea = self.idea_store.get_idea(idea_id)
        if idea is None:
            raise ValueError(f"Idea not found: {idea_id}")

        # 更新 idea 的 sim_id
        self.idea_store.save_idea(idea_id, {
            **idea,
            "sim_id": sim_id,
        })

        # 缓存到 SimulationDB
        if self.sim_db:
            h = self.sim_db.compute_hash(expression, settings)
            self.sim_db.put_cached(h, expression, json.dumps(settings), result)

        return sim_id

    # -- 查询与统计 ----------------------------------------------------------

    def get_idea_full_context(self, idea_id: str) -> Optional[Dict[str, Any]]:
        """获取 idea 的完整上下文（含 wave/batch/sim 信息）."""
        idea = self.idea_store.get_idea(idea_id)
        if idea is None:
            return None

        context = {
            "idea": idea,
            "wave": None,
            "batch": None,
            "sim": None,
        }

        # 加载 wave 信息
        if idea.get("wave_id"):
            wave_file = self.ledger_root / idea["region"] / "waves" / f"{idea['wave_id']}.json"
            if wave_file.exists():
                with open(wave_file, "r", encoding="utf-8") as f:
                    context["wave"] = json.load(f)

        # 加载 batch/sim 信息（从 SimulationDB）
        if self.sim_db and idea.get("batch_id"):
            # 查询 batch_log
            cur = self.sim_db.connection.cursor()
            cur.execute(
                "SELECT * FROM batch_log WHERE batch_id = ?",
                (idea["batch_id"],),
            )
            row = cur.fetchone()
            if row:
                context["batch"] = {
                    "batch_id": row[2],
                    "expressions": json.loads(row[3]) if row[3] else [],
                    "results": json.loads(row[4]) if row[4] else [],
                    "created_at": row[5],
                }

        return context

    def get_region_stats(self, region: str) -> Dict[str, Any]:
        """获取区域统计信息."""
        all_ideas = self.idea_store.query_ideas(region=region, limit=10000)

        stats = {
            "region": region,
            "total": len(all_ideas),
            "by_status": {},
            "by_dataset": {},
            "waves": set(),
        }

        for idea in all_ideas:
            status = idea.get("status", "unknown")
            dataset = idea.get("dataset_id", "unknown")
            wave_id = idea.get("wave_id")

            stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
            stats["by_dataset"][dataset] = stats["by_dataset"].get(dataset, 0) + 1
            if wave_id:
                stats["waves"].add(wave_id)

        stats["waves"] = list(stats["waves"])
        return stats

    # -- 状态机查询 ----------------------------------------------------------

    def get_pending_ideas(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取待处理 idea."""
        return self.idea_store.query_ideas(region=region, status="pending")

    def get_processing_ideas(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取处理中 idea."""
        return self.idea_store.query_ideas(region=region, status="processing")

    def get_completed_ideas(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取已完成 idea."""
        return self.idea_store.query_ideas(region=region, status="completed")

    def get_failed_ideas(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取失败 idea."""
        return self.idea_store.query_ideas(region=region, status="failed")


# -- 便捷函数 ---------------------------------------------------------------

_default_ledger: Optional[IdeaLedger] = None


def get_default_ledger() -> IdeaLedger:
    """获取默认 IdeaLedger 实例（单例模式）."""
    global _default_ledger
    if _default_ledger is None:
        _default_ledger = IdeaLedger()
    return _default_ledger
