# -*- coding: utf-8 -*-
"""SubmissionsMixin: submission ledger CRUD for CampaignStore."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from ._common import _dumps, _loads, _now


class SubmissionsMixin:
    """Submission ledger read/write methods."""

    def upsert_submission(self, alpha_id: str, region: Optional[str] = None,
                          submission_type: str = "REGULAR", status: str = "PENDING",
                          quota_used: int = 0,
                          verdict: Optional[Dict] = None, submitted_at: Optional[str] = None,
                          verified_at: Optional[str] = None) -> Dict[str, Any]:
        """Upsert submission record.

        verified_at 默认 now()（提交即验证），消除旧版 None 不填的遗漏。
        quota_remaining 已废弃（从未写入），不再接受。
        """
        cur = self.connection.cursor()
        now = _now()
        submitted_at = submitted_at or now
        verified_at = verified_at or now
        verdict_json = _dumps(verdict) if verdict else None

        cur.execute(
            "SELECT id FROM submission_ledger WHERE alpha_id=? AND submitted_at=?",
            (alpha_id, submitted_at),
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                """UPDATE submission_ledger SET region=?, submission_type=?, status=?,
                   quota_used=?, verdict=?, verified_at=?, updated_at=?
                   WHERE alpha_id=? AND submitted_at=?""",
                (region, submission_type, status, quota_used,
                 verdict_json, verified_at, now, alpha_id, submitted_at),
            )
            action = "updated"
        else:
            cur.execute(
                """INSERT INTO submission_ledger
                   (alpha_id, region, submission_type, status, quota_used,
                    verdict, submitted_at, verified_at, created_at, updated_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (alpha_id, region, submission_type, status, quota_used,
                 verdict_json, submitted_at, verified_at, now, now),
            )
            action = "inserted"
        self.connection.commit()
        return {"action": action, "alpha_id": alpha_id, "submitted_at": submitted_at}

    def get_submission(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """Get latest submission record for alpha."""
        cur = self.connection.cursor()
        cur.execute(
            """SELECT * FROM submission_ledger WHERE alpha_id=?
               ORDER BY submitted_at DESC LIMIT 1""",
            (alpha_id,),
        )
        row = cur.fetchone()
        if not row:
            return None
        return dict(row)

    def list_submissions(self, region: Optional[str] = None, status: Optional[str] = None,
                         limit: int = 100) -> List[Dict[str, Any]]:
        """List submission records."""
        cur = self.connection.cursor()
        sql = "SELECT * FROM submission_ledger WHERE 1=1"
        params: List[Any] = []
        if region:
            sql += " AND region=?"
            params.append(region)
        if status:
            sql += " AND status=?"
            params.append(status)
        sql += " ORDER BY submitted_at DESC LIMIT ?"
        params.append(limit)
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def get_quota_status(self, region: Optional[str] = None, window_hours: int = 48) -> Dict[str, Any]:
        """Get submission quota status for the rolling window."""
        cur = self.connection.cursor()
        # 计算窗口内的提交数
        cutoff = datetime.now().timestamp() - (window_hours * 3600)
        cutoff_str = datetime.fromtimestamp(cutoff).isoformat()

        sql = """SELECT COUNT(*) as used FROM submission_ledger
                 WHERE submitted_at > ? AND status IN ('SUBMITTED', 'ACTIVE')"""
        params: List[Any] = [cutoff_str]
        if region:
            sql += " AND region=?"
            params.append(region)

        cur.execute(sql, params)
        used = cur.fetchone()[0]

        # 默认配额限制（可从 platform_constraints.json 读取）
        quota_limit = 4  # 48h 滚动配额

        return {
            "used": used,
            "limit": quota_limit,
            "remaining": max(0, quota_limit - used),
            "window_hours": window_hours,
            "region": region,
        }
