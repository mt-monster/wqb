# -*- coding: utf-8 -*-
"""wave_results_writer.py - wave 结果台账入库工具（单轨 DB 模式）。

替代手写 wave<N>_results.json，直接写入 wave_results 表。

用法：
  from tools.wave_results_writer import write_wave_result
  write_wave_result(
      region="MEA",
      wave_number=49,
      focus="fundamental72 is_q zscore252 参数扫描",
      context="wave48 发现 is_q zscore252 唯一有效族，wave49 参数优化",
      key_findings=["EBITDA z252 limit0.3 sharpe 1.72 全 PASS", ...],
      candidates=[{"id": "xxx", "variant": "EBITDA z252 limit0.3", "sharpe": 1.72, ...}],
      batches=[{"id": "1UJOYrdA44Eta0lPag2ESdk", "n": 10, ...}],
      verdict="QP7er8qp 变体全 PASS，提交前自查 SELF_CORR",
      status="closed",
      full_payload={...}  # 完整 wave JSON（可选，MD 快照导出用）
  )
"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "wqb.db"


def write_wave_result(
    region,
    wave_number,
    focus=None,
    context=None,
    key_findings=None,
    candidates=None,
    batches=None,
    verdict=None,
    status="open",
    source_file=None,
    archived=0,
    full_payload=None,
):
    """写入 wave 结果台账到 wave_results 表（幂等，INSERT OR REPLACE）。

    参数：
        region: 区域（MEA/USA/KOR/ASI/EUR/GBR/HKG/IND/GLB/DEU）
        wave_number: 波次编号（整数）
        focus: wave 主题
        context: 背景
        key_findings: 关键结论数组（list of str）
        candidates: 候选 alpha 摘要（list of dict）
        batches: 批次信息（list of dict）
        verdict: 最终裁决
        status: open / closed
        source_file: 原 JSON 文件路径（追溯，可选）
        archived: 是否已归档（0/1）
        full_payload: 完整 wave JSON（dict，可选，MD 快照导出用）
    """
    conn = sqlite3.connect(str(DB))
    c = conn.cursor()
    c.execute(
        """
        INSERT OR REPLACE INTO wave_results
        (region, wave_number, focus, context, key_findings, candidates, batches, verdict, status, source_file, archived, full_payload, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (
            region,
            wave_number,
            focus,
            context,
            json.dumps(key_findings or [], ensure_ascii=False),
            json.dumps(candidates or [], ensure_ascii=False),
            json.dumps(batches or [], ensure_ascii=False),
            verdict,
            status,
            source_file,
            archived,
            json.dumps(full_payload, ensure_ascii=False) if full_payload else None,
        ),
    )
    conn.commit()
    conn.close()
    print(f"[OK] wave_results: {region} wave{wave_number} status={status}")


def list_wave_results(region=None, status=None, archived=None):
    """列出 wave 结果（可按 region/status/archived 过滤）。"""
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    sql = "SELECT * FROM wave_results WHERE 1=1"
    params = []
    if region:
        sql += " AND region=?"
        params.append(region)
    if status:
        sql += " AND status=?"
        params.append(status)
    if archived is not None:
        sql += " AND archived=?"
        params.append(archived)
    sql += " ORDER BY region, CAST(wave_number AS INTEGER)"
    c.execute(sql, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    # CLI 测试
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        region = sys.argv[2] if len(sys.argv) > 2 else None
        rows = list_wave_results(region=region)
        for r in rows:
            print(f"{r['region']} wave{r['wave_number']}: {r['status']} - {r['focus']}")
    else:
        print("Usage: python wave_results_writer.py list [REGION]")
