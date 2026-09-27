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


#: verdict 判定表（2026-09-27 R20）——与 toolkit `_lib/wave_results.auto_upsert_from_review`
#: 及 `pipeline.py` 波后自动判定是同一条规则（GREEN / YELLOW / RED 三灯即由此而来）。
VERDICT_TABLE = ("PASS = 本波 ≥1 条候选达标（过全部评审闸 / GREEN；已提交的必然达标）；"
                 "PARTIAL = 0 条达标但 ≥1 条进 near 池（YELLOW）；"
                 "FAIL = 0 达标且 0 near（RED / 全灭）")


def verdict_from_counts(n_pass: int, n_near: int = 0) -> str:
    """按判定表由逐条事实定 verdict——批量导入 / 事后补记用它，而不是从自由文本猜。"""
    if int(n_pass or 0) > 0:
        return "PASS"
    if int(n_near or 0) > 0:
        return "PARTIAL"
    return "FAIL"


def suggest_verdict(verdict: Any) -> Optional[Dict[str, str]]:
    """normalize_verdict 认不出的自由文本 → 按判定表给出**建议**（只进拒绝信息，绝不自动写入）。

    写入路径保持保守，但拒绝时告诉写入方"按判定表这条大概率是什么、依据是哪几个字"，
    省掉一轮来回。KOR 真实历史 30 条 verdict 原文里有 24 条被拒（no_submit / 无提交(…) /
    FULL_RED / 8/8 RED / 2 GREEN + 6 RED / ✅ 2 RA 提交成功），每条都能得到建议（2026-09-27 R20）。
    返回 {"verdict", "confidence": high|medium|low, "rule"}；认不出返回 None。
    """
    v = str(verdict or "").strip()
    if not v:
        return None
    up = v.upper()

    def hit(enum, confidence, rule):
        return {"verdict": enum, "confidence": confidence, "rule": rule}

    if re.search(r"提交成功|✅", v) or re.search(r"(?<!\d)[1-9]\d*\s*GREEN", up):
        return hit("PASS", "high", "提交成功 / ✅ / N GREEN（≥1 条达标）")
    all_red = re.search(r"(\d+)\s*/\s*(\d+)\s*RED", up)
    if "FULL_RED" in up or "全灭" in v or (all_red and all_red.group(1) == all_red.group(2)):
        return hit("FAIL", "high", "全灭 / FULL_RED / N/N RED（0 达标且 0 near）")
    if re.search(r"NEAR|YELLOW", up) or re.search(r"近闸|基线|突破|破闸|黄灯", v):
        return hit("PARTIAL", "medium", "NEAR / 近闸 / 新基线 / 突破 / 黄灯（0 达标但有 near）")
    if re.search(r"判死|天花板|无法破|结构性上限|无挖掘价值", v) or "FAIL" in up:
        return hit("FAIL", "medium", "判死 / 天花板 / FAIL")
    if re.search(r"无提交|0\s*可提交", v) or "NO_SUBMIT" in up:
        return hit("FAIL", "low", "无提交 / no_submit——若本波有 near 候选应为 PARTIAL")
    return None


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
            msg = (f"verdict 必须是 PASS/FAIL/PARTIAL（或带该前缀），收到 {provided['verdict']!r}；"
                   f"描述性结论请放 key_findings。判定表：{VERDICT_TABLE}")
            suggestion = suggest_verdict(provided["verdict"])
            if suggestion is None:
                return {"error": msg, **base}
            return {"error": msg + (f"。按判定表建议 verdict='{suggestion['verdict']}'"
                                    f"（依据：{suggestion['rule']}；置信 {suggestion['confidence']}）"
                                    "，未自动采用——确认后显式传入"),
                    "suggestion": suggestion, **base}
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


def adopt_legacy_row(conn, region: str, wave_number: Any) -> Optional[str]:
    """把旧版按数字入库、`full_payload.wave` 记着原字符串的那一行改回原字符串键（2026-09-27 N30）。

    旧版 toolkit 评审写入按"波号里第一个数字"入库（`s2_<ds>_d1` → 2，冲突顺延 max+1），原字符串
    只留在 full_payload.wave。本波还没有以原字符串为键的行时，把那一行改名（id / created_at /
    全部内容保留），返回旧键；没有可认领的行返回 None。两行并存（旧数字行 + 原字符串行）时不动，
    留给人工处理。写入方在同一事务里、写之前调用。
    """
    wave = "" if wave_number is None else str(wave_number).strip()
    if not wave or conn.execute("SELECT 1 FROM wave_results WHERE region=? AND wave_number=?",
                                (region, wave)).fetchone():
        return None
    for rid, old_key, payload in conn.execute(
            "SELECT id, wave_number, full_payload FROM wave_results WHERE region=?", (region,)).fetchall():
        try:
            old_wave = json.loads(payload).get("wave") if payload else None
        except (TypeError, ValueError, AttributeError):
            continue
        if old_wave is not None and str(old_wave).strip() == wave and str(old_key) != wave:
            conn.execute("UPDATE wave_results SET wave_number=? WHERE id=?", (wave, rid))
            return str(old_key)
    return None
