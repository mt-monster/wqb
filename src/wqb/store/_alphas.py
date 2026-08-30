# -*- coding: utf-8 -*-
"""AlphasMixin: alpha query methods for CampaignStore."""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class AlphasMixin:
    """Alpha query methods."""

    def get_alpha_by_id(self, alpha_id: str) -> Optional[Dict[str, Any]]:
        """根据 alpha_id 查询 alpha 详情（含 region 名）。"""
        cur = self.connection.cursor()
        cur.execute(
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE a.alpha_id=?",
            (alpha_id,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def list_alphas_by_region(self, region: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出某 region 的全部 alpha（可选 status 过滤）。"""
        cur = self.connection.cursor()
        sql = (
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE r.name=?"
        )
        params: List[Any] = [region]
        if status:
            sql += " AND a.status=?"
            params.append(status)
        sql += " ORDER BY a.updated_at DESC"
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]

    def search_alphas_by_sharpe(
        self,
        region: Optional[str] = None,
        min_sharpe: float = 1.0,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """按 sharpe 搜索 alpha（sharpe >= min_sharpe）。"""
        cur = self.connection.cursor()
        sql = (
            "SELECT a.*, r.name AS region FROM alphas a "
            "JOIN regions r ON a.region_id = r.id "
            "WHERE a.sharpe >= ?"
        )
        params: List[Any] = [min_sharpe]
        if region:
            sql += " AND r.name=?"
            params.append(region)
        sql += " ORDER BY a.sharpe DESC LIMIT ?"
        params.append(limit)
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]
