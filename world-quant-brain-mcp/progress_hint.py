# -*- coding: utf-8 -*-
"""任务进度 + 预计剩余时间（ETA）的共享生成器（2026-11-20）。

## 为什么需要它
MCP 服务是 streamable-http + stateless（mcp_core.py），工具内 ``print(..., file=sys.stderr)``
只有服务端日志能看到，**调用方（Agent / 用户）看不到**。要让进度可见，唯一可靠的通道是
把结构化进度对象塞进工具**返回值**（并经 _slim_* 白名单保留）。

两处长耗时操作共用本模块：
  - 查 prod（brain_mixin_spcread._poll_production_correlation）
  - create_multi_simulation（tools_sim.py，派发 + 同步等待）

## ETA 基准（实证，勿拍脑袋改）
  - prod 相关性：平台正常计算 180–200 s，单次轮询窗口 240 s（_PROD_CORR_WAIT_S）。
    窗口内越快收敛越好；超时返回 pending，ETA 语义是「还剩多少等待预算」。
  - 批量回测：data/wqb.db::backtest_results.duration_s (src='batch', 近30天 n=9913)
    中位 302 s / p25 211 s / p75 470 s / p90 672 s。派发时给区间估计。

零依赖（只用标准库），可被 mixin / tools / 独立 CLI 安全 import。任何异常都不得影响主流程。
"""
from __future__ import annotations

from typing import Any, Dict, Optional

# 平台计算 / 轮询窗口基准（秒）
PROD_TYPICAL_S = 190.0       # 正常计算 180–200 s 的中点
PROD_WINDOW_S = 240.0        # 单次轮询窗口上限（与 wqb.config.WAIT_THRESHOLDS 同源）
BATCH_MEDIAN_S = 302.0       # 批量派发→收批端到端周转中位（实证 n=9913）
BATCH_P25_S = 211.0
BATCH_P75_S = 470.0


def fmt_eta(seconds: Optional[float]) -> str:
    """秒 → 人类可读时长。None/负数 → '—'（不可估，绝不臆造 0）。"""
    if seconds is None:
        return "—"
    try:
        s = float(seconds)
    except (TypeError, ValueError):
        return "—"
    if s < 0:
        return "—"
    if s < 60:
        return f"{int(s)}s"
    m, sec = divmod(int(s), 60)
    if m < 60:
        return f"{m}m{sec:02d}s" if sec else f"{m}m"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m" if m else f"{h}h"


def progress_snapshot(
    *,
    elapsed_s: Optional[float],
    stage: str,
    basis_s: float,
    window_s: Optional[float] = None,
    note: str = "",
) -> Dict[str, Any]:
    """生成结构化进度对象。

    Args:
        elapsed_s: 已耗时（秒）。None → percent/eta 均为 None（不可估）。
        stage: 'polling' | 'dispatched' | 'done' | 'pending' 等阶段标签。
        basis_s: ETA 基准总时长（秒）——poll 用窗口 240；派发用中位 302。
        window_s: 硬窗口上限（秒）。给了则 ETA = max(0, window - elapsed)，
            否则 ETA = max(0, basis - elapsed)（典型完成剩余）。
        note: 附加口径说明（如 '批量周转中位·p25=211s p75=470s'）。

    Returns:
        {
          'stage': str,
          'elapsed_s': float|None,
          'eta_s': float|None,          # 预计剩余秒
          'eta_human': str,             # 人类可读
          'percent': float|None,        # 0–100，已耗时/基准
          'basis_s': float,             # ETA 基准，便于消费方判断可信度
          'note': str,
        }
    """
    try:
        e = None if elapsed_s is None else max(0.0, float(elapsed_s))
    except (TypeError, ValueError):
        e = None
    try:
        b = max(1.0, float(basis_s))
    except (TypeError, ValueError):
        b = 1.0

    if e is None:
        eta = None
        pct = None
    else:
        cap = b if window_s is None else max(1.0, float(window_s))
        eta = max(0.0, cap - e)
        # percent 与 eta 必须同一分母，否则出现「63% 却还剩 2m」的自相矛盾。
        # 有硬窗口时按窗口算（prod），无窗口时按基准算（批量派发）。
        pct = round(min(100.0, e / cap * 100.0), 1)

    return {
        "stage": stage,
        "elapsed_s": round(e, 1) if e is not None else None,
        "eta_s": round(eta, 1) if eta is not None else None,
        "eta_human": fmt_eta(eta) if e is not None else "—",
        "percent": pct,
        "basis_s": b,
        "note": note,
    }


def batch_dispatch_progress(elapsed_s: Optional[float], n: int) -> Dict[str, Any]:
    """派发阶段专用：ETA 用批量周转中位 302 s，note 带 p25/p75 区间。"""
    p = progress_snapshot(
        elapsed_s=elapsed_s,
        stage="dispatched",
        basis_s=BATCH_MEDIAN_S,
        note=(f"批量端到端周转中位 {int(BATCH_MEDIAN_S)}s "
              f"(p25={int(BATCH_P25_S)}s p75={int(BATCH_P75_S)}s), n={n}"),
    )
    p["n_expressions"] = n
    return p


def prod_poll_progress(elapsed_s: Optional[float], *, done: bool = False,
                       timed_out: bool = False) -> Dict[str, Any]:
    """prod 轮询专用：窗口 240 s 作 ETA 上限，典型 190 s 作进度基准。

    2026-11-20 实测修正：done/超时是终态，必须强制 eta=0、percent=100，
    否则快速命中（如预读/缓存加速）会出现「stage=done 却显示还需 3m30s」的
    自相矛盾。只有 polling 中间态才按 elapsed 推算剩余。
    """
    stage = "done" if done else ("pending" if timed_out else "polling")
    if done or timed_out:
        p = {
            "stage": stage,
            "elapsed_s": round(max(0.0, float(elapsed_s or 0)), 1),
            "eta_s": 0.0,
            "eta_human": "0s" if done else "—",
            "percent": 100.0,
            "basis_s": PROD_TYPICAL_S,
            "note": ("已完成" if done else "轮询窗口耗尽, 返回 pending (未判死, 可隔时重查)"),
        }
    else:
        p = progress_snapshot(
            elapsed_s=elapsed_s,
            stage=stage,
            basis_s=PROD_TYPICAL_S,
            window_s=PROD_WINDOW_S,
            note="平台计算典型 180–200s, 轮询窗口上限 240s",
        )
    p["window_s"] = PROD_WINDOW_S
    return p


__all__ = [
    "fmt_eta", "progress_snapshot", "batch_dispatch_progress", "prod_poll_progress",
    "PROD_TYPICAL_S", "PROD_WINDOW_S", "BATCH_MEDIAN_S", "BATCH_P25_S", "BATCH_P75_S",
]
