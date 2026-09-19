# -*- coding: utf-8 -*-
"""带指数退避的批量写入重试封装（MCP 调用端）。

用法：
    from tools.mcp_batch_writer import MCPBatchWriter

    writer = MCPBatchWriter()
    writer.upsert_ledger_key("KOR", "submit_ready", [...])
    writer.upsert_wave_result("KOR", 100, focus="...", candidates=[...])
    writer.flush()  # 可选：强制 flush 本地队列
"""
from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def _normalize_wave(wave: Any, *, dataset: Optional[str] = None,
                    region: Optional[str] = None) -> str:
    """写入前把裸时间戳波号归一（2026-09-17 P2-6）。

    实测 DEU 有 20 行 `expressions.wave` 实为 `time.time()` 的裸 epoch 秒
    （调用方未给波号时用时间戳顶替）。本函数是**根因侧**护栏：
    写入路径统一过 `wqb.wave_id.normalize_wave_id`，使裸时间戳不再进入波号空间。

    契约模块不可达时**原样放行**（不阻断写入）——本护栏治的是口径漂移，
    不该因为 `src/` 不在 sys.path 就让整个写批失败。
    """
    try:
        from wqb.wave_id import normalize_wave_id
    except ImportError:  # pragma: no cover - 依赖环境
        return str(wave)
    return normalize_wave_id(wave, dataset=dataset, region=region)

# 默认重试策略
_DEFAULT_MAX_RETRIES = 3
_DEFAULT_BASE_DELAY = 1.0  # 秒
_DEFAULT_MAX_DELAY = 30.0


class MCPBatchWriter:
    """MCP 批量写入封装：本地队列 + 指数退避重试 + 失败落盘。"""

    def __init__(
        self,
        max_retries: int = _DEFAULT_MAX_RETRIES,
        base_delay: float = _DEFAULT_BASE_DELAY,
        max_delay: float = _DEFAULT_MAX_DELAY,
        queue_file: Optional[str] = None,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.queue_file = queue_file
        self._queue: List[Dict[str, Any]] = []
        self._load_queue()

    def _load_queue(self) -> None:
        """启动时加载未完成的队列（崩溃恢复）。"""
        if not self.queue_file:
            return
        try:
            with open(self.queue_file, "r", encoding="utf-8") as f:
                self._queue = json.load(f)
            if self._queue:
                logger.info(f"[MCPBatchWriter] 恢复 {len(self._queue)} 条未完成任务")
        except FileNotFoundError:
            self._queue = []
        except Exception as e:
            logger.warning(f"[MCPBatchWriter] 队列加载失败: {e}")
            self._queue = []

    def _save_queue(self) -> None:
        """持久化队列到本地文件。"""
        if not self.queue_file:
            return
        try:
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(self._queue, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[MCPBatchWriter] 队列保存失败: {e}")

    def _call_mcp(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """调用 MCP 工具（由子类或调用方注入具体实现）。"""
        raise NotImplementedError("子类须实现 _call_mcp")

    def _execute_with_retry(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """带指数退避的 MCP 调用。"""
        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                return self._call_mcp(tool_name, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    logger.warning(
                        f"[MCPBatchWriter] {tool_name} 第 {attempt + 1} 次失败: {e}, "
                        f"{delay:.1f}s 后重试"
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"[MCPBatchWriter] {tool_name} 重试 {self.max_retries} 次后仍失败: {e}")
        return {"error": str(last_error), "tool": tool_name, "kwargs": kwargs}

    def _enqueue(self, tool_name: str, **kwargs) -> None:
        """任务入队。"""
        self._queue.append({"tool": tool_name, "kwargs": kwargs, "enqueued_at": time.time()})
        self._save_queue()

    def _dequeue(self) -> Optional[Dict[str, Any]]:
        """任务出队。"""
        if not self._queue:
            return None
        task = self._queue.pop(0)
        self._save_queue()
        return task

    # ---------------- 公共 API ----------------

    def upsert_ledger_key(self, region: str, key: str, value: Any) -> Dict[str, Any]:
        """写台账 key（带重试）。"""
        return self._execute_with_retry("upsert_ledger_key", region=region, key=key, value=value)

    def upsert_wave_result(
        self,
        region: str,
        wave_number: int,
        focus: Optional[str] = None,
        context: Optional[str] = None,
        key_findings: Optional[Any] = None,
        candidates: Optional[Any] = None,
        batches: Optional[Any] = None,
        verdict: Optional[str] = None,
        status: str = "closed",
        source_file: Optional[str] = None,
        full_payload: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """写 wave 结果（带重试）。"""
        return self._execute_with_retry(
            "upsert_wave_result",
            region=region,
            wave_number=wave_number,
            focus=focus,
            context=context,
            key_findings=key_findings,
            candidates=candidates,
            batches=batches,
            verdict=verdict,
            status=status,
            source_file=source_file,
            full_payload=full_payload,
        )

    def upsert_backtest_rows(
        self, region: str, wave: str, rows: Any, dataset: Optional[str] = None
    ) -> Dict[str, Any]:
        """写回测行（带重试）。"""
        return self._execute_with_retry(
            "upsert_backtest_rows", region=region, wave=wave, rows=rows, dataset=dataset
        )

    def upsert_expressions(
        self, region: str, wave: str, expressions: Any, dataset: Optional[str] = None, status: str = "pending"
    ) -> Dict[str, Any]:
        """写表达式（带重试）。"""
        return self._execute_with_retry(
            "upsert_expressions", region=region, wave=wave, expressions=expressions, dataset=dataset, status=status
        )

    def flush(self) -> int:
        """flush 本地队列（同步执行所有待处理任务）。"""
        processed = 0
        while True:
            task = self._dequeue()
            if task is None:
                break
            result = self._execute_with_retry(task["tool"], **task["kwargs"])
            if "error" in result:
                logger.error(f"[MCPBatchWriter] flush 失败: {result}")
                # 失败重新入队
                self._enqueue(task["tool"], **task["kwargs"])
                break
            processed += 1
        return processed

    def queue_size(self) -> int:
        """当前队列长度。"""
        return len(self._queue)


# ---------------- 直连 SQLite 实现（绕过 MCP，用于高频批量场景） ----------------

class DirectDBWriter(MCPBatchWriter):
    """直连 SQLite 的批量写入器（绕过 MCP，用于高频批量场景）。

    与 MCPBatchWriter 接口一致，但直接操作 SQLite，避免 MCP 序列化/网络开销。
    适用于：wave 结果回写、批量回测行导入等本地高频场景。
    """

    def __init__(self, db_path: str, **kwargs):
        super().__init__(**kwargs)
        self.db_path = db_path
        self._conn = None
        self._store = None

    def _get_store(self):
        """惰性构造 CampaignStore（唯一写入口，2026-09-18）。

        `src/` 必须在 sys.path 上；缺失时抛 RuntimeError（不静默降级——
        降级回简化实现会重新丢指标，正是本次修复要消灭的故障模式）。
        """
        if self._store is None:
            from pathlib import Path
            import sys
            root = Path(__file__).resolve().parents[1]
            if str(root / "src") not in sys.path:
                sys.path.insert(0, str(root / "src"))
            try:
                from wqb.store import CampaignStore
            except ImportError as e:  # pragma: no cover - 依赖环境
                raise RuntimeError(
                    "CampaignStore 不可达（src/wqb/store）。"
                    "该写入路径不允许降级为简化实现，否则回测指标会静默丢失。"
                ) from e
            self._store = CampaignStore(self.db_path)
        return self._store

    def _get_conn(self):
        if self._conn is None:
            import sqlite3
            self._conn = sqlite3.connect(self.db_path, timeout=30.0)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
        return self._conn

    def _call_mcp(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """直连 SQLite 实现（与 MCP 工具同名同参数）。"""
        conn = self._get_conn()
        cur = conn.cursor()
        now = time.strftime("%Y-%m-%dT%H:%M:%S")

        if tool_name == "upsert_ledger_key":
            region, key, value = kwargs["region"], kwargs["key"], kwargs["value"]
            payload = json.dumps(value, ensure_ascii=False)
            cur.execute(
                "INSERT INTO ledger_kv (region, key, value, created_at, updated_at) "
                "VALUES (?,?,?,?,?) "
                "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at",
                (region, key, payload, now, now),
            )
            conn.commit()
            return {"action": "upserted", "region": region, "key": key}

        elif tool_name == "upsert_wave_result":
            region = kwargs["region"]
            wave_number = kwargs["wave_number"]
            kf = json.dumps(kwargs.get("key_findings"), ensure_ascii=False) if kwargs.get("key_findings") is not None else None
            cand = json.dumps(kwargs.get("candidates"), ensure_ascii=False) if kwargs.get("candidates") is not None else None
            bat = json.dumps(kwargs.get("batches"), ensure_ascii=False) if kwargs.get("batches") is not None else None
            fp = json.dumps(kwargs.get("full_payload"), ensure_ascii=False) if kwargs.get("full_payload") is not None else None
            cur.execute(
                "INSERT INTO wave_results "
                "(region, wave_number, focus, context, key_findings, candidates, batches, verdict, status, source_file, archived, created_at, updated_at, full_payload) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,0,?,?,?) "
                "ON CONFLICT(region, wave_number) DO UPDATE SET "
                "focus=excluded.focus, context=excluded.context, key_findings=excluded.key_findings, "
                "candidates=excluded.candidates, batches=excluded.batches, verdict=excluded.verdict, "
                "status=excluded.status, source_file=excluded.source_file, updated_at=excluded.updated_at, "
                "full_payload=excluded.full_payload",
                (
                    region, str(wave_number), kwargs.get("focus"), kwargs.get("context"),
                    kf, cand, bat, kwargs.get("verdict"), kwargs.get("status", "closed"),
                    kwargs.get("source_file"), now, now, fp,
                ),
            )
            conn.commit()
            return {"action": "upserted", "region": region, "wave_number": wave_number}

        elif tool_name == "upsert_backtest_rows":
            # 2026-09-18 修复（设计文档 §2.2 改动#4）：
            # 原为简化实现，只写 backtest_results 的 9 列且**不写 alphas 表**，
            # 导致 margin / 2Y / sub_universe / prod_corr / self_corr 全部丢失。
            # 现统一委托 CampaignStore.upsert_backtest_rows（唯一写入口，全列 + 同步 alphas）。
            region, wave, rows = kwargs["region"], kwargs["wave"], kwargs["rows"]
            dataset = kwargs.get("dataset")
            wave = _normalize_wave(wave, dataset=dataset, region=region)
            store = self._get_store()
            n = store.upsert_backtest_rows(region, str(wave), rows, dataset=dataset)
            return {"n": n, "region": region, "wave": str(wave)}

        elif tool_name == "persist_correlation":
            # 2026-09-18 新增：相关性检查结果直落 alphas 表。
            store = self._get_store()
            return store.persist_correlation(
                alpha_id=kwargs["alpha_id"],
                prod=kwargs.get("prod"),
                self_=kwargs.get("self_"),
                source=kwargs.get("source", "triage_local"),
                overwrite=bool(kwargs.get("overwrite", False)),
            )

        elif tool_name == "upsert_expressions":
            region, wave, expressions = kwargs["region"], kwargs["wave"], kwargs["expressions"]
            dataset = kwargs.get("dataset")
            status = kwargs.get("status", "pending")
            wave = _normalize_wave(wave, dataset=dataset, region=region)
            n = 0
            for expr in expressions:
                code = expr.get("expression") or expr.get("expr") or expr.get("code") or ""
                if not code:
                    continue
                cur.execute(
                    "INSERT OR REPLACE INTO expressions "
                    "(region, wave, dataset, expression, status, created_at, updated_at) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (region, str(wave), dataset, code, status, now, now),
                )
                n += 1
            conn.commit()
            return {"n": n, "region": region, "wave": str(wave)}

        else:
            raise ValueError(f"DirectDBWriter 不支持的工具: {tool_name}")

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
