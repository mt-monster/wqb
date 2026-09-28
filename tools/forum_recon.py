#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""forum_recon.py — 问题驱动的论坛只读检索（recon），回测流水线按需调用（2026-09-28）。

定位（与既有论坛工具的分工）：
  - `forum_research.py`：批量关键词清扫 → JSON dump（抓取核心的**唯一 HTTP 实现**，本工具 import 复用）；
  - `forum_cache_builder.py`：稳健性 Phase A 的关键词包缓存（7 天 TTL）；
  - **本工具**：**单问题 → 结构化答案 → 入库（含负结果）**，供 GEM/build_wave/Mode B/seal_dead_end 消费。

额度口径（用户定案 2026-09-28）：**以能查出有效文章为标准** —— 不设小硬顶，
搜不到有效文章就继续扩展关键词变体（扩到安全上限为止）；达到目标有效篇数即提前收束。
`--limit` = 目标有效文章数（默认 3）；`--max-search-rounds` 仅是防失控的安全上限（默认 8）。

产出契约：
  - found=true  → `--out kb`（合入 KB/community_tpl_kb 的 `forum_recon_entries[]`）
                 或 `--out ledger`（ledger_kv 键 `forum_recon_<qkey>`）；
  - found=false → 一律落 `forum_recon_negative_<qkey>`（**负结果也是判死证据**，
                 7 天内重复调用直接回放缓存，不重复 live 查）；
  - 每条有效文章带：post_id / 标题 / 赞数 / 摘录 / 适用边界(context) / 幽灵算子标注。

退出码：0=有产出（有效文章≥1）；2=无解（负结果已入库）；1=工具异常。
干跑：`--dry-run` 只输出检索计划（关键词包 + 缓存状态），零网络、零写库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECON_CACHE = os.path.join(REPO_ROOT, "tracking", "FORUM", "forum_recon_cache.json")
TTL_DAYS = 7
#: 有效文章判据里的"可操作性"标记（命中任一即认为含可回收内容，非闲聊/公告）
ACTION_MARKERS = (
    "实测", "指标", "sharpe", "fitness", "表达式", "字段", "算子", "配方", "换手",
    "turnover", "稳健", "prod", "相关性", "中性化", "破墙", "回测", "表达", "因子",
)
TITLE_NOISE = ("公告", "直播", "签到", "问卷", "获奖", "名单公示")


# ---------------------------------------------------------------- 小工具
def _qkey(question: str) -> str:
    return hashlib.sha1(question.strip().encode("utf-8")).hexdigest()[:10]


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _load_recon_cache() -> Dict[str, Any]:
    try:
        with open(RECON_CACHE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"entries": {}}


def _save_recon_cache(cache: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(RECON_CACHE), exist_ok=True)
    tmp = RECON_CACHE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    os.replace(tmp, RECON_CACHE)


def _cache_fresh(entry: Dict[str, Any]) -> bool:
    try:
        t = time.mktime(time.strptime(str(entry.get("searched_at", ""))[:19], "%Y-%m-%dT%H:%M:%S"))
        return (time.time() - t) < TTL_DAYS * 86400
    except (ValueError, OverflowError):
        return False


def _db_path(cli_db: Optional[str]) -> str:
    return (cli_db or os.environ.get("WQB_DB_PATH")
            or os.path.join(REPO_ROOT, "data", "wqb.db"))


# ---------------------------------------------------------------- 检索计划（机械、无 LLM）
_STOP = {"的", "了", "有", "无", "和", "与", "在", "是", "在吗", "怎么", "什么", "如何", "为什么",
         "the", "and", "for", "with", "how", "what"}


def plan_queries(question: str, context: Dict[str, str], explicit: Optional[str]) -> List[str]:
    """从问题文本机械派生关键词包（自适应扩展的初始段）。

    包序 = 具体→宽泛：① 问题里最具体的 2 个词；② 单个主题词 + 墙/场景区词；
    ③ 广义主题词；④ 主题词 × 实证后缀变体（"实盘/经验/配方/破墙"）。显式 --queries 覆盖全部。
    """
    if explicit:
        return [q.strip() for q in explicit.split(",") if q.strip()]
    cjk = [w for w in re.findall(r"[\u4e00-\u9fff]{2,6}", question)]
    asc = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", question)]
    ctx_words = [str(v) for k, v in context.items()
                 if k in ("dataset", "region", "wall", "family") and v]
    tokens: List[str] = []
    for w in cjk + asc + ctx_words:
        if w.lower() not in _STOP and w not in tokens:
            tokens.append(w)
    if not tokens:
        tokens = ["worldquant", "alpha"]
    packs: List[str] = []
    if len(tokens) >= 2:
        packs.append(f"{tokens[0]} {tokens[1]}")
    packs.append(f"{tokens[0]} {context.get('wall', '')}".strip())
    packs.append(tokens[0])
    for suf in ("实盘", "经验", "配方", "破墙"):
        packs.append(f"{tokens[0]} {suf}")
    for extra in tokens[1:3]:
        packs.append(extra)
    out: List[str] = []
    for p in packs:
        if p and p not in out:
            out.append(p)
    return out


# ---------------------------------------------------------------- 有效文章判据
def is_useful(post: Dict[str, Any]) -> bool:
    """有效文章 = 正文足量 且 含可操作标记，标题非公告/闲聊。"""
    title = str(post.get("title") or "")
    if any(n in title for n in TITLE_NOISE):
        return False
    body = str(post.get("body") or post.get("text") or "")
    if len(body) < 200:
        return False
    low = (title + "\n" + body[:2000]).lower()
    return any(m.lower() in low for m in ACTION_MARKERS)


def scan_ghosts(text: str, ghost_names: List[str]) -> List[str]:
    """摘录里出现的幽灵算子（入批前须按 ghost_operator_advisory 替换）。"""
    low = text.lower()
    return [g for g in ghost_names if g and g.lower() in low]


def _load_ghost_names(db_path: str) -> List[str]:
    try:
        sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
        from lib.wqb_db import get_conn  # noqa: WPS433
        conn = get_conn(db_path)
        try:
            row = conn.execute(
                "SELECT value FROM ledger_kv WHERE region='KB' AND key='community_tpl_kb'"
            ).fetchone()
        finally:
            conn.close()
        if not row or not row[0]:
            return []
        kb = json.loads(row[0]) if isinstance(row[0], (str, bytes)) else row[0]
        adv = (kb or {}).get("ghost_operator_advisory") or {}
        return sorted(adv.keys()) if isinstance(adv, dict) else []
    except Exception:
        return []


# ---------------------------------------------------------------- 入库
def _ledger_upsert(db_path: str, region: str, key: str, value: Dict[str, Any]) -> None:
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
    from lib.wqb_db import get_conn  # noqa: WPS433
    conn = get_conn(db_path)
    try:
        conn.execute(
            "INSERT INTO ledger_kv (region, key, value) VALUES (?,?,?) "
            "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, "
            "updated_at=CURRENT_TIMESTAMP",
            (region, key, json.dumps(value, ensure_ascii=False)),
        )
        conn.commit()
    finally:
        conn.close()


def _kb_merge_entries(db_path: str, entries: List[Dict[str, Any]]) -> str:
    """把 recon 条目并入 KB/community_tpl_kb.forum_recon_entries[]（幂等 by post_id）。"""
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
    from lib.wqb_db import get_conn  # noqa: WPS433
    conn = get_conn(db_path)
    try:
        row = conn.execute(
            "SELECT value FROM ledger_kv WHERE region='KB' AND key='community_tpl_kb'"
        ).fetchone()
        kb = json.loads(row[0]) if row and isinstance(row[0], (str, bytes)) else (row[0] if row else {})
        kb = kb or {}
        existing = {e.get("post_id"): e for e in kb.get("forum_recon_entries", []) if e.get("post_id")}
        for e in entries:
            existing[e["post_id"]] = e
        kb["forum_recon_entries"] = list(existing.values())
        conn.execute(
            "INSERT INTO ledger_kv (region, key, value) VALUES ('KB','community_tpl_kb',?) "
            "ON CONFLICT(region, key) DO UPDATE SET value=excluded.value, "
            "updated_at=CURRENT_TIMESTAMP",
            (json.dumps(kb, ensure_ascii=False),),
        )
        conn.commit()
    finally:
        conn.close()
    return "KB/community_tpl_kb"


# ---------------------------------------------------------------- live 抓取（复用 forum_research 核心）
def _live_session():
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
    import forum_research as fr  # noqa: WPS433（唯一 HTTP 实现）
    import requests  # noqa: WPS433
    s = requests.Session()
    email, password = fr.load_creds(None)
    fr.authenticate(s, email, password)
    fr.sso_handshake(s)
    return s, fr


def live_search_round(session, fr, query: str, max_pages: int, read_top: int,
                      seen: set) -> List[Dict[str, Any]]:
    """一轮：搜 → 解析候选 → 读帖 → 返回新读到的结构化文章（跳过已读）。"""
    out: List[Dict[str, Any]] = []
    try:
        hits = fr.search_html(session, query, max_pages=max_pages) or []
    except Exception as e:
        print(f"[forum_recon] 搜索失败（{query}）：{e}", file=sys.stderr)
        return out
    for hit in hits[:read_top]:
        pid = hit.get("post_id") or hit.get("id")
        if not pid and hit.get("click_href"):
            try:
                pid = fr.resolve_id(session, hit["click_href"])
            except Exception:
                pid = None
        if not pid or pid in seen:
            continue
        seen.add(pid)
        try:
            post = fr.read_post(session, pid) or {}
        except Exception as e:
            print(f"[forum_recon] 读帖失败（{pid}）：{e}", file=sys.stderr)
            continue
        out.append({
            "post_id": pid,
            "title": post.get("title") or hit.get("title") or "",
            "votes": post.get("votes") or hit.get("votes"),
            "body": post.get("body") or post.get("text") or "",
            "query": query,
        })
        time.sleep(2.5)          # 限速：与 forum_research 的 page_delay 同一包络
    return out


# ---------------------------------------------------------------- 主流程
def recon(question: str, context: Dict[str, str], out_mode: str, limit: int,
          max_rounds: int, queries: Optional[str], dry_run: bool,
          db_path: str) -> Dict[str, Any]:
    qkey = _qkey(question)
    cache = _load_recon_cache()
    cached = cache.get("entries", {}).get(qkey)
    if cached and _cache_fresh(cached):
        print(f"[forum_recon] 缓存命中（{TTL_DAYS}d TTL）：question sha1={qkey}，"
              f"found={cached.get('found')}，不重复 live 查")
        cached["from_cache"] = True
        return cached

    packs = plan_queries(question, context, queries)
    plan = {"question": question, "question_key": qkey, "context": context,
            "queries": packs, "limit": limit, "max_search_rounds": max_rounds,
            "out": out_mode, "cache_state": "hit" if cached else "miss"}
    if dry_run:
        print("[forum_recon][dry-run] 检索计划（零网络、零写库）：")
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return {"dry_run": True, "plan": plan}

    ghost_names = _load_ghost_names(db_path)
    seen: set = set()
    useful: List[Dict[str, Any]] = []
    tried: List[str] = []
    session = fr = None
    round_no = 0
    # 自适应额度：以查出 limit 篇有效文章为标准；关键词包用尽后继续扩后缀变体，
    # 直到命中或触到安全上限（防失控）。
    ext_packs = [f"{p} {s}" for p in packs[:3] for s in ("实盘", "经验", "问题", "解决")]
    queue = list(packs) + [p for p in ext_packs if p not in packs]
    while len(useful) < limit and round_no < max_rounds and queue:
        query = queue.pop(0)
        tried.append(query)
        round_no += 1
        if session is None:
            try:
                session, fr = _live_session()
            except Exception as e:
                result = {"question": question, "question_key": qkey, "found": False,
                          "error": f"forum auth failed: {e}", "searched_at": _now_iso(),
                          "queries_tried": tried}
                _record_negative(cache, qkey, result, db_path, context)
                return result
        print(f"[forum_recon] 第 {round_no} 轮检索：{query!r}（已有 {len(useful)} 篇有效）")
        for post in live_search_round(session, fr, query, max_pages=2, read_top=6, seen=seen):
            if is_useful(post):
                excerpt = re.sub(r"\s+", " ", str(post.get("body") or ""))[:400]
                useful.append({
                    "post_id": post["post_id"], "title": post["title"],
                    "votes": post.get("votes"), "excerpt": excerpt,
                    "applicable_context": dict(context), "source_query": query,
                    "ghost_operators": scan_ghosts(excerpt, ghost_names),
                })

    found = len(useful) > 0
    result: Dict[str, Any] = {
        "question": question, "question_key": qkey, "found": found,
        "n_useful": len(useful), "articles": useful, "queries_tried": tried,
        "rounds": round_no, "searched_at": _now_iso(),
        "note": ("以有效文章为标准自适应扩展；命中即收束" if found else
                 f"关键词空间已扩至 {len(queue) + round_no} 变体/触安全上限 {max_rounds}，仍无有效文章"),
    }
    if not found:
        _record_negative(cache, qkey, result, db_path, context)
        return result

    if out_mode == "kb":
        where = _kb_merge_entries(db_path, useful)
    else:
        region = str(context.get("region") or "GLOBAL")
        where = f"{region}/forum_recon_{qkey}"
        _ledger_upsert(db_path, region, f"forum_recon_{qkey}",
                       {**result, "ttl_note": "同问题 7 天内复用，勿重复 live 查"})
    cache.setdefault("entries", {})[qkey] = {k: v for k, v in result.items() if k != "articles"} | {
        "articles": useful, "sink": where}
    _save_recon_cache(cache)
    print(f"[forum_recon] 有效文章 {len(useful)} 篇 → {where}")
    return result


def _record_negative(cache: Dict[str, Any], qkey: str, result: Dict[str, Any],
                     db_path: str, context: Dict[str, str]) -> None:
    """负结果落库：判死证据链的一环（decision-table D2「论坛无解」），7 天负缓存。"""
    region = str(context.get("region") or "GLOBAL")
    sink = f"{region}/forum_recon_negative_{qkey}"
    try:
        _ledger_upsert(db_path, region, f"forum_recon_negative_{qkey}",
                       {**result, "ttl_note": "负结果 7 天内勿重复 live 查（缓存回放）"})
        result["sink"] = sink
    except Exception as e:
        result["sink_error"] = str(e)
    cache.setdefault("entries", {})[qkey] = result
    _save_recon_cache(cache)
    print(f"[forum_recon] 无解（负结果已入库：{sink}）——可作「论坛无解」判死证据")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="问题驱动论坛只读检索（recon）：以查出有效文章为标准，产出必入库（含负结果）")
    ap.add_argument("--question", required=True, help="具体决策问题（如：GLB model264 慢基本面强度墙有无破墙配方）")
    ap.add_argument("--context", default="", help="k=v,k=v 附加语境（region/dataset/wall/family）")
    ap.add_argument("--out", default="ledger", choices=("kb", "ledger", "negative"),
                    help="产出落点：kb=并入 KB/community_tpl_kb.forum_recon_entries；"
                         "ledger=region/forum_recon_<qkey>；negative（found=false 时强制）")
    ap.add_argument("--limit", type=int, default=3, help="目标有效文章数（默认 3；以查出有效文章为标准）")
    ap.add_argument("--max-search-rounds", type=int, default=8,
                    help="防失控安全上限（默认 8）；额度实际由有效文章数决定，不设小硬顶")
    ap.add_argument("--queries", default=None, help="显式关键词包（逗号分隔），覆盖机械派生")
    ap.add_argument("--db", default=None, help="DB 路径（缺省 WQB_DB_PATH / <repo>/data/wqb.db）")
    ap.add_argument("--dry-run", action="store_true", help="只输出检索计划，零网络零写库")
    a = ap.parse_args()

    context: Dict[str, str] = {}
    for kv in (a.context.split(",") if a.context else []):
        if "=" in kv:
            k, v = kv.split("=", 1)
            context[k.strip()] = v.strip()
    try:
        result = recon(a.question, context, a.out, max(1, a.limit),
                       max(1, a.max_search_rounds), a.queries, a.dry_run, _db_path(a.db))
    except Exception as e:
        print(f"[forum_recon] 工具异常：{e}", file=sys.stderr)
        return 1
    print(json.dumps({k: v for k, v in result.items() if k != "articles"},
                     ensure_ascii=False, indent=2))
    if a.dry_run:
        return 0
    return 0 if result.get("found") else 2


if __name__ == "__main__":
    sys.exit(main())
