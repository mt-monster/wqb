# -*- coding: utf-8 -*-
"""论坛取证（forum_recon）证据契约：ledger 键名、记录分类、判死闸的纯判定函数。

单一实现——写入方 `tools/forum_recon.py`、波级节点 `forum_recon_wave`、MCP `seal_dead_end`（判死闸）、`tools/step_funnel.py`（统计）
都从这里取，不再各拼各的键名、各判各的 `found`。此前「工具故障 ≡ 论坛无解」就是因为写入方与读取方对 `found=false` 的理解不一致：
鉴权失败被记成 `found=false` 落 `forum_recon_negative_*`，再被当作判死证据。

三种结局（`status`）——**故障不是无解**：

  ok         found=True   查到有效文章（配方可用，不得直接判死）
  no_result  found=False  检索**可靠地**完成且没有有效文章（可作「论坛无解」判死证据）
  error      found=None   工具故障 / 检索不可信（鉴权失败、依赖缺失、检索全失败、对照检索失败……）——**不是取证**，不入缓存

判死闸（fail-closed，两层）：
  * `evaluate_forum_recon`：只看**声明**（`payload.forum_recon`）——只有 `found=False`、`status` 不是 `error`、带 `question_key` 才放行；
  * `verify_evidence`：再按 `question_key` **回 ledger 核对**（`resolve_outcome`）——声明必须能追溯到真实记录，且不能被更新的可靠记录推翻
    （声明 found=false，但 ledger 里最新的可靠结局是「有货」→ 拒绝）。声明可以抄错、可以编，ledger 记录是工具写的。
"""
from __future__ import annotations

import hashlib
from typing import Any, Callable, Dict, Iterable, Optional

STATUS_OK = "ok"
STATUS_NO_RESULT = "no_result"
STATUS_ERROR = "error"

#: ledger 键前缀（region 作用域；`GLOBAL` 兜底）。`forum_recon_<qkey>` 是有货记录，前缀最短，所以分类不能只看前缀（见 `key_kind`）。
KEY_FOUND_PREFIX = "forum_recon_"
KEY_NEGATIVE_PREFIX = "forum_recon_negative_"
KEY_ERROR_PREFIX = "forum_recon_error_"
KEY_WAVE_PREFIX = "forum_recon_wave_"

#: 判死闸的拒绝码（seal_dead_end 的 error 里带上，agent 据此选下一步）
CODE_ALLOWED = "ok_no_result"
CODE_MISSING = "recon_missing"
CODE_NOT_A_RECORD = "recon_not_a_record"
CODE_NO_KEY = "recon_no_question_key"
CODE_FOUND = "recon_found"
CODE_ERROR = "recon_error"
CODE_UNKNOWN = "recon_unknown"
CODE_NOT_IN_LEDGER = "recon_not_in_ledger"        # 声明的 question_key 在 ledger（region / GLOBAL）里找不到任何记录
CODE_LEDGER_FOUND = "recon_ledger_found"          # ledger 里该问题最新的可靠结局是「有货」，与声明的 found=false 矛盾
CODE_LEDGER_ERROR = "recon_ledger_error"          # ledger 里该问题只有故障记录——从未有过可靠的取证


def question_key(question: str) -> str:
    """同一问题 → 同一键（sha1 前 10 位）；`tools/forum_recon.py` 的 `_qkey` 就是它。"""
    return hashlib.sha1(str(question).strip().encode("utf-8")).hexdigest()[:10]


def key_found(qkey: str) -> str:
    return f"{KEY_FOUND_PREFIX}{qkey}"


def key_negative(qkey: str) -> str:
    return f"{KEY_NEGATIVE_PREFIX}{qkey}"


def key_error(qkey: str) -> str:
    return f"{KEY_ERROR_PREFIX}{qkey}"


def key_wave(wave: Any) -> str:
    """波级取证的完成标记键（每波 ≤ 1 次）；波号可以是整数或字符串（`97` / `s2_<ds>_d1`）。"""
    return f"{KEY_WAVE_PREFIX}{wave}"


def key_kind(key: str) -> Optional[str]:
    """ledger 键 → 记录类别：`found` / `negative` / `error` / `wave`；不是 forum_recon 键返回 None。

    `forum_recon_<qkey>` 的 qkey 恒为 10 位十六进制，所以能与 `forum_recon_negative_…` 等更长的前缀区分开。
    """
    k = str(key or "")
    if k.startswith(KEY_NEGATIVE_PREFIX):
        return "negative"
    if k.startswith(KEY_ERROR_PREFIX):
        return "error"
    if k.startswith(KEY_WAVE_PREFIX):
        return "wave"
    if k.startswith(KEY_FOUND_PREFIX):
        tail = k[len(KEY_FOUND_PREFIX):]
        if len(tail) == 10 and all(c in "0123456789abcdef" for c in tail):
            return "found"
    return None


def classify_record(rec: Any) -> str:
    """一条 recon 记录（ledger 值 / 缓存条目 / `payload.forum_recon`）→ `found` / `negative` / `error` / `unknown`。

    兼容旧记录：旧版把鉴权失败记成 `{"found": false, "error": "forum auth failed: …"}`——带 `error` 且 found 不是 True 的一律算故障，
    **不算负结果**。
    """
    if not isinstance(rec, dict):
        return "unknown"
    if rec.get("status") == STATUS_ERROR:
        return "error"
    if rec.get("error") and rec.get("found") is not True:
        return "error"
    if rec.get("found") is True:
        return "found"
    if rec.get("found") is False:
        return "negative"
    return "unknown"


def status_of(found: Optional[bool]) -> str:
    return STATUS_OK if found is True else STATUS_NO_RESULT if found is False else STATUS_ERROR


def evaluate_forum_recon(evidence: Any) -> Dict[str, Any]:
    """判死闸的纯判定：`{"allowed": bool, "code": str, "message": str}`。

    | evidence（`payload.forum_recon`）        | 判死 |
    |---|---|
    | `found=false`（且无 `error`、带 `question_key`） | 允许 |
    | `found=true`                              | 拒绝——配方转 salvage / Mode B 武器，不得直接判死 |
    | `found=null` / `status=error` / 带 `error` | 拒绝——**工具故障 = 未取证，故障 ≠ 论坛无解** |
    | 缺失                                       | 拒绝——未取证 |
    """
    if evidence is None or evidence == {}:
        return {"allowed": False, "code": CODE_MISSING,
                "message": "缺 forum_recon 取证：判死前必须先跑 tools/forum_recon.py（--out negative），再把结果（question_key / found / status）传进 forum_recon 参数"}
    if not isinstance(evidence, dict):
        return {"allowed": False, "code": CODE_NOT_A_RECORD, "message": "forum_recon 必须是对象（question_key / found / status）"}
    kind = classify_record(evidence)
    if kind == "found":
        return {"allowed": False, "code": CODE_FOUND,
                "message": "论坛有解（found=true）：该帖配方转 salvage / Mode B 武器，不得直接判死"}
    if kind == "error":
        return {"allowed": False, "code": CODE_ERROR,
                "message": "取证记录是工具故障（found=null / status=error / 带 error 字段）：故障 ≠ 论坛无解，不能当判死证据；解决后重跑 forum_recon"}
    if kind != "negative":
        return {"allowed": False, "code": CODE_UNKNOWN, "message": "forum_recon 缺 found（必须是 true / false）"}
    if not str(evidence.get("question_key") or "").strip():
        return {"allowed": False, "code": CODE_NO_KEY,
                "message": "forum_recon 缺 question_key：取证必须可追溯到 ledger 里的 forum_recon_negative_<qkey> 记录"}
    return {"allowed": True, "code": CODE_ALLOWED, "message": "论坛无解（found=false）——取证成立"}


def resolve_outcome(get_record: Callable[[str, str], Optional[Dict[str, Any]]], region: str, qkey: str
                    ) -> Optional[Dict[str, Any]]:
    """按 qkey 在 ledger 里找这个问题的结局。`get_record(region, key)` 返回解析后的 dict 或 None（不存在）。

    查找范围：`region` 再 `GLOBAL`（`tools/forum_recon.py` 缺 region 语境时落 GLOBAL）。
    **可靠结局优先于故障**：有货 / 无解记录里取 `searched_at` 最新的一条；只有故障记录时才返回 error。
    返回 `{"kind", "record", "key", "region"}`；什么都没有返回 None。
    """
    reliable: list = []
    errors: list = []
    for reg in dict.fromkeys([region, "GLOBAL"]):
        for kind, key in (("found", key_found(qkey)), ("negative", key_negative(qkey)), ("error", key_error(qkey))):
            rec = get_record(reg, key)
            if not isinstance(rec, dict):
                continue
            actual = classify_record(rec)
            item = {"kind": actual if actual != "unknown" else kind, "record": rec, "key": key, "region": reg}
            (errors if item["kind"] == "error" else reliable).append(item)
    pool = reliable or errors
    if not pool:
        return None
    order = {"found": 0, "negative": 1, "error": 2}
    return sorted(pool, key=lambda i: (str(i["record"].get("searched_at") or ""), -order.get(i["kind"], 3)), reverse=True)[0]


def verify_evidence(evidence: Any, get_record: Callable[[str, str], Optional[Dict[str, Any]]], region: str
                    ) -> Dict[str, Any]:
    """判死闸的完整判定 = 声明层（`evaluate_forum_recon`）+ ledger 核对（`resolve_outcome`）。

    返回 `{"allowed", "code", "message", ...}`；放行时另带 `question_key` / `ledger_key` / `ledger_region` / `searched_at` / `question`
    （审计用：判死当时依据的是哪条记录、问的是什么、多久以前查的）。**不给证据龄设上限**——「故障 ≠ 无解」才是这道闸要防的失败模式；
    `searched_at` 留痕，要不要重查由人看。**也不核对相关性**：闸认的是证据可靠（不是故障、能追溯、没被推翻），
    问的问题是否对得上要判死的那个族，看留痕里的 `question` 由人判断。
    """
    v = evaluate_forum_recon(evidence)
    if not v["allowed"]:
        return v
    qkey = str(evidence["question_key"]).strip()
    out = resolve_outcome(get_record, region, qkey)
    if out is None:
        return {"allowed": False, "code": CODE_NOT_IN_LEDGER, "question_key": qkey,
                "message": (f"ledger（{region} / GLOBAL）里没有 question_key={qkey} 的取证记录：声明无法核对。"
                            "先跑 tools/forum_recon.py（它会落库），并核对 question_key 有没有抄错")}
    if out["kind"] == "found":
        return {"allowed": False, "code": CODE_LEDGER_FOUND, "question_key": qkey, "ledger_key": out["key"],
                "message": (f"ledger 里该问题最新的可靠结局是「有货」（{out['region']}/{out['key']}），与声明的 found=false 矛盾："
                            "论坛有解，配方转 salvage / Mode B 武器，不得直接判死")}
    if out["kind"] == "error":
        return {"allowed": False, "code": CODE_LEDGER_ERROR, "question_key": qkey, "ledger_key": out["key"],
                "message": (f"ledger 里该问题只有故障记录（{out['region']}/{out['key']}）：从未有过可靠的取证，"
                            "故障 ≠ 论坛无解。修好工具后重跑 forum_recon")}
    return {"allowed": True, "code": CODE_ALLOWED, "message": "论坛无解（声明与 ledger 记录一致）——取证成立",
            "question_key": qkey, "ledger_key": out["key"], "ledger_region": out["region"],
            "searched_at": out["record"].get("searched_at"), "question": out["record"].get("question")}


def summarize_keys(keys: Iterable[str]) -> Dict[str, int]:
    """一组 ledger 键 → 各类记录条数（`tools/step_funnel.py` 用：命中率 = found / (found + negative)，故障与波标记不计入）。"""
    out = {"found": 0, "negative": 0, "error": 0, "wave": 0}
    for k in keys:
        kind = key_kind(k)
        if kind:
            out[kind] += 1
    return out
