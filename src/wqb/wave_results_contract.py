# -*- coding: utf-8 -*-
"""wave_results 写入契约 —— 合并式 upsert + 结案必带 verdict（2026-09-27 P0-1）。

## 问题（2026-09-27 dry-run 全链复现）
`mcp__wqb-db__upsert_wave_result` 在行已存在时对**所有列**赋值，本次没传的列被写成 NULL。
ra-pipeline 步 9 要求把点塔进度"拷进 upsert_wave_result 的 key_findings"——只传
key_findings 的那次调用会把已经写好的 verdict 清空；停止规则 B
（`campaign._run_stop_rules_gate`）把空 verdict 归一为 UNKNOWN、只告警不拦截，
"最近 3 个 closed 波全 FAIL"的区域因此照样被放行开下一波。

同一写法还允许 `status='closed'` + verdict 为空的"空壳"行（toolkit
`_lib/wave_results.WaveResultsStore.upsert` 早已拒绝这种写入，两个入口契约不一致）；
`tools/mcp_batch_writer.DirectDBWriter` 的直写兜底同样是全列覆盖。MCP 签名
`wave_number: int` 还让 `s2_<ds>_d<delay>` 这类字符串波号在参数校验层就被拒，
这些波永远写不进 verdict。

## 契约（本模块是唯一实现：MCP 工具与直写兜底都调用它）
1. **合并**：行已存在时只覆盖本次**显式传入（非 None）**的列，其余列保持原值。
   `key_findings` 等 JSON 列一旦传入即整列替换（不做追加）。
2. **status 缺省**：新行 → `closed`（沿用 MCP 原默认）；已有行 → 本次写了 verdict
   则 `closed`（"写结论即结案"，与原默认一致），否则保持原状态。显式传入的 status 总是生效。
3. **结案必带结论**：写入后的行若 `status='closed'` 且 verdict 为空 → 拒绝、不写库。
4. **verdict 枚举**：PASS / FAIL / PARTIAL；可辨认的前缀 / 计数形态归一，原文作为
   key_findings 首条保留；无法辨认 → 拒绝（2026-09-15 ⑦ 规则）。
5. **wave_number 一律按字符串存取**（表结构为 TEXT；`97` 与 `s2_<ds>_d1` 都合法）。

事务由调用方负责：本模块只执行 SQL，不 commit、不 close。
"""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

VERDICT_OK = ("PASS", "FAIL", "PARTIAL")
STATUS_OK = ("open", "closed")
#: 可写列（region / wave_number 是主键维度；archived 与时间戳由本模块维护）
FIELDS = ("focus", "context", "key_findings", "candidates", "batches",
          "verdict", "status", "source_file", "full_payload")
_JSON_FIELDS = ("key_findings", "candidates", "batches", "full_payload")


def normalize_verdict(verdict: Any) -> Tuple[Optional[str], str]:
    """自由文本 verdict → 枚举（规则原样迁自 wqb_db_mcp._normalize_wave_verdict）。

    返回 (枚举 | None, 命中的规则)；None 表示无法辨认，调用方应拒绝写入。
    注意：原注释称"与 tools/migrate_wave_verdict_enum.classify 同规则"并不成立 ——
    本函数只有前缀 / 过硬闸计数 / 全灭 三类规则；classify 另有 `FAIL` 子串、判死 / 天花板、
    近闸突破等关键词规则（那是带人工复核的一次性迁移工具）。写入路径刻意保持保守：
    无法辨认就拒绝、让写入方显式给枚举，而不是按关键词猜停止规则 B 的输入。
    """
    v = str(verdict or "").strip()
    if not v:
        return None, "空"
    up = v.upper()
    if up in VERDICT_OK:
        return up, "枚举"
    if up.startswith("GREEN") or up.startswith("PASS"):
        return "PASS", "前缀"
    if up.startswith(("YELLOW", "PARTIAL", "CLOSED_ACCEPTED")):
        return "PARTIAL", "前缀"
    if up.startswith(("RED", "FAIL", "CLOSED_DEAD_END", "GATE_BLOCKED", "PROBE_WEAK")):
        return "FAIL", "前缀"
    m = re.search(r"(\d+)\s*/\s*(\d+)\s*过硬闸", v)
    if m:
        return ("PASS" if int(m.group(1)) > 0 else "FAIL"), "过硬闸计数"
    if "全灭" in v or "GATE_FAIL" in up:
        return "FAIL", "关键词"
    return None, "无匹配"


def _as_list(raw: Any) -> List[Any]:
    """库里 JSON 列 → list（非 list 包一层，损坏按原文保留一条）。"""
    if raw is None or raw == "":
        return []
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except (TypeError, ValueError):
            return [raw]
    if isinstance(raw, list):
        return list(raw)
    return [raw]


def upsert_wave_result(conn, region: str, wave_number: Any, now: str,
                       **fields: Any) -> Dict[str, Any]:
    """按本模块契约写一行 wave_results。

    返回 ``{"action": "inserted"|"updated"|"noop", "region", "wave_number",
    "verdict", "status", "updated_fields"}``；违反契约时返回 ``{"error": ...}`` 且不写库。
    """
    unknown = sorted(set(fields) - set(FIELDS))
    if unknown:
        raise TypeError(f"wave_results 不认识的列: {unknown}")
    wave = "" if wave_number is None else str(wave_number).strip()
    base = {"region": region, "wave_number": wave}
    if not str(region or "").strip() or not wave:
        return {"error": "region / wave_number 不能为空", **base}

    provided = {k: v for k, v in fields.items() if v is not None}

    status = provided.get("status")
    if status is not None and status not in STATUS_OK:
        return {"error": f"status 必须是 {list(STATUS_OK)} 之一，收到 {status!r}", **base}

    verdict_note = None
    if "verdict" in provided:
        norm, _rule = normalize_verdict(provided["verdict"])
        if norm is None:
            return {"error": f"verdict 必须是 PASS/FAIL/PARTIAL（或带该前缀），收到 "
                             f"{provided['verdict']!r}；描述性结论请放 key_findings", **base}
        raw = str(provided["verdict"]).strip()
        if norm != raw:
            verdict_note = f"原 verdict（写入时归一）: {raw}"
        provided["verdict"] = norm

    row = conn.execute(
        "SELECT verdict, status, key_findings FROM wave_results WHERE region=? AND wave_number=?",
        (region, wave),
    ).fetchone()
    old_verdict, old_status, old_findings = (row[0], row[1], row[2]) if row else (None, None, None)

    if verdict_note:
        # 归一说明插到 key_findings 首条：本次传了就在传入列表上加，没传就在库里原列表上加
        # （不能像旧实现那样只写 [note]——那会把已有 findings 整列替换掉）。
        findings = _as_list(provided["key_findings"]) if "key_findings" in provided else _as_list(old_findings)
        provided["key_findings"] = [verdict_note] + findings

    if row is None:
        provided.setdefault("status", "closed")
    elif "status" not in provided and "verdict" in provided:
        provided["status"] = "closed"          # 写结论即结案（与原默认一致）

    final_status = provided.get("status", old_status)
    final_verdict = provided.get("verdict", old_verdict)
    if final_status == "closed" and not str(final_verdict or "").strip():
        return {"error": f"wave {wave} 结案（status='closed'）必须带 verdict（PASS/FAIL/PARTIAL）；"
                         f"只补写其它字段时请一并给出 verdict，结论未定请传 status='open'", **base}

    for k in _JSON_FIELDS:
        if k in provided:
            provided[k] = json.dumps(provided[k], ensure_ascii=False)

    if row is None:
        cols = ["region", "wave_number", *provided, "archived", "created_at", "updated_at"]
        vals = [region, wave, *provided.values(), 0, now, now]
        conn.execute(
            f"INSERT INTO wave_results ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
            vals,
        )
        action = "inserted"
    elif provided:
        sets = ", ".join(f"{k}=?" for k in provided)
        conn.execute(
            f"UPDATE wave_results SET {sets}, updated_at=? WHERE region=? AND wave_number=?",
            [*provided.values(), now, region, wave],
        )
        action = "updated"
    else:
        action = "noop"

    return {"action": action, **base, "verdict": final_verdict, "status": final_status,
            "updated_fields": sorted(provided)}
