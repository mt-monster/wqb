# -*- coding: utf-8 -*-
"""批次派发时刻登记 —— 支撑「派发→收批」端到端周转（2026-11-04 #112）。

批量回测是 fire-and-forget：``POST /simulations`` 立刻返回 multisim location，
平台侧并行计算，本地随后用 ``harvest_multisim_alphas`` 收批落库。平台
**不暴露单颗 alpha 的计算耗时**（``/alphas/{id}`` 与 ``payload_json`` 均无
时间字段），因此批量路径唯一可观测的端到端量是
「派发时刻 → 收批落库时刻」的墙钟周转。

本模块把派发时刻写进 ``data/wave_dispatch.json``（跨进程 / 跨重启存活，
原子写 tmp+replace），key = multisim id（URL 最后一段，统一相对/绝对
Location 格式差异）。收批时读回并算差值，由调用方附加到 alpha detail 的
``duration_s`` 键走既有落库链路。

★ 口径（面板必须标注，切勿当单颗计算耗时）：
  - 批量行 ``duration_s`` = **整批端到端周转**，同批多行共享同一个值；
  - 单条 ``create_simulation`` 行 ``duration_s`` = 单颗阻塞墙钟。
  两者不同源，不可混算中位数当「单颗耗时」。

零依赖（只用标准库），便于 ``tools/submit_batch.py`` 这类独立 CLI 进程
也能安全 import（它不具备 mcp_core / CampaignStore 运行环境）。
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

#: 与 wqb.db 同目录，跨会话存活；不在任何临时目录。
_DATA = Path(__file__).resolve().parents[1] / "data" / "wave_dispatch.json"

#: 超过 48h 的派发记录自动清理（收批不会隔这么久，防文件无限增长）。
_TTL_S = 48 * 3600


def _key(location) -> str:
    """Location → multisim id。 '/simulations/abc' 与完整 URL 都归到 'abc'。"""
    if not location:
        return ""
    s = str(location).rstrip("/").split("?")[0]
    return s.split("/")[-1]


def _load() -> dict:
    try:
        with open(_DATA, "r", encoding="utf-8") as f:
            d = json.load(f)
            return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _save(d: dict) -> None:
    try:
        _DATA.parent.mkdir(parents=True, exist_ok=True)
        tmp = str(_DATA) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        os.replace(tmp, _DATA)
    except Exception:
        pass  # 旁路能力：登记失败绝不能影响仿真


def mark(location, n: int = 0, region: str = "") -> None:
    """登记一次派发。POST /simulations 成功后调用；失败静默。

    派发在 MCP 内是串行的（RLock + 单 stdio 通道），读-改-写冲突概率可忽略；
    独立 CLI 并发派发时若偶发覆盖，只影响该批耗时样本，不影响回测本身。
    """
    k = _key(location)
    if not k:
        return
    try:
        now = time.time()
        d = {kk: vv for kk, vv in _load().items()
             if isinstance(vv, dict) and 0 <= now - float(vv.get("ts", 0)) < _TTL_S}
        d[k] = {"ts": now,
                "iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)),
                "n": int(n or 0), "region": region or ""}
        _save(d)
    except Exception:
        pass


def elapsed(location):
    """派发 → 此刻的墙钟秒（round 1）。无记录 / 超 TTL / 异常返回 ``None``。"""
    k = _key(location)
    if not k:
        return None
    try:
        v = _load().get(k)
        if not isinstance(v, dict) or v.get("ts") is None:
            return None
        dt = time.time() - float(v["ts"])
        return round(dt, 1) if 0 <= dt < _TTL_S else None
    except Exception:
        return None


__all__ = ["mark", "elapsed"]
