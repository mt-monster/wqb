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

产出契约（三种结局，键名与判定的单一实现在 `src/wqb/recon_evidence.py`）：
  - found=true  / status=ok        → `--out kb`（合入 KB/community_tpl_kb 的 `forum_recon_entries[]`）
                                     或 `--out ledger`（ledger_kv 键 `forum_recon_<qkey>`）；
  - found=false / status=no_result → 落 `forum_recon_negative_<qkey>`（**可靠**的负结果 = 判死证据，7 天内重复调用直接回放缓存）；
  - found=null  / status=error     → **工具故障**（凭据缺失 / 依赖缺失 / 鉴权失败 / 检索全失败 / 对照检索失败）：
                                     落 `forum_recon_error_<qkey>`，**不是**取证、**不入缓存**（修好后同问题重新 live 查）。
  - 每条有效文章带：post_id / 标题 / 赞数 / 摘录 / 适用边界(context) / 幽灵算子标注。

**故障 ≠ 无解**（2026-09-29 事故）：旧版把鉴权失败记成 `found=false` 落 `forum_recon_negative_*`，等于「工具坏了 ≡ 论坛无解」→ 误把活路判死。
现在「无解」只在检索**可靠完成**时才成立：鉴权成功；每轮检索都没抛异常；搜到的帖子至少读成功一篇；
且末尾用固定对照词（`CONTROL_QUERY`）再搜一次确认检索通道仍有结果（会话过期 / 被拦 / 页面改版时搜索页会安静地返回 0 条）。

凭据：进程环境 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（标准名）优先；缺则读 MCP `.env`（与 `forum_research.py` 主流程同一路径）。
本工具**不打印、不记录**凭据值。

退出码：0=有产出（有效文章≥1）；2=无解（可靠的负结果已入库）；1=工具故障（含未捕获异常；故障记录见 `forum_recon_error_<qkey>`）。
⚠ 判断「无解」看退出码 2 且输出里**没有** `error` 字段；退出码 1 永远不是取证。
干跑：`--dry-run` 只输出检索计划（关键词包 + 缓存状态），零网络、零写库。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC = os.path.join(REPO_ROOT, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
from wqb import recon_evidence as RE  # noqa: E402

RECON_CACHE = os.path.join(REPO_ROOT, "tracking", "FORUM", "forum_recon_cache.json")
TTL_DAYS = 7
#: 有效文章判据里的"可操作性"标记（命中任一即认为含可回收内容，非闲聊/公告）
ACTION_MARKERS = (
    "实测", "指标", "sharpe", "fitness", "表达式", "字段", "算子", "配方", "换手",
    "turnover", "稳健", "prod", "相关性", "中性化", "破墙", "回测", "表达", "因子",
)
TITLE_NOISE = ("公告", "直播", "签到", "问卷", "获奖", "名单公示")
#: 「无解」成立前的对照检索词：论坛以 alpha 为主题，这个词搜不到任何结果 = 检索通道失效，不是「论坛没有答案」
CONTROL_QUERY = "alpha"


class ReconToolError(Exception):
    """工具故障（不是「论坛无解」）。`code` 供故障记录分类：credentials_missing / deps_missing / auth_failed /
    search_failed / read_failed / control_probe_failed / unexpected。"""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


# ---------------------------------------------------------------- 小工具
def _qkey(question: str) -> str:
    return RE.question_key(question)


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


def _cache_reusable(entry: Optional[Dict[str, Any]]) -> bool:
    """缓存回放只认**新鲜的可靠结局**（有货 / 无解）。旧版把鉴权失败写成 `found=false` + `error` 的条目一律不回放——
    否则那次故障会被当作「论坛无解」重放整整 7 天。"""
    return bool(entry) and _cache_fresh(entry) and RE.classify_record(entry) in ("found", "negative")


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
    cjk = [w for w in re.findall(r"[一-鿿]{2,6}", question)]
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
def _load_credentials(fr) -> Tuple[str, str]:
    """标准名 `CREDENTIALS_EMAIL` / `CREDENTIALS_PASSWORD`（进程环境）优先；缺则读 MCP `.env`（`forum_research.load_creds` 的路径约定）。

    旧版给 `load_creds` 传的是 None 并按元组解包：它要的是 `.env` 路径、返回的是 dict，
    传 None 直接 TypeError——live 路径因此**从未跑通过**，所有真实调用都落进「鉴权失败 → 记成无解」。
    """
    email = os.environ.get("CREDENTIALS_EMAIL")
    password = os.environ.get("CREDENTIALS_PASSWORD")
    if not (email and password):
        env_path = os.path.join(REPO_ROOT, "world-quant-brain-mcp", ".env")
        creds = fr.load_creds(env_path)
        email = email or creds.get("CREDENTIALS_EMAIL")
        password = password or creds.get("CREDENTIALS_PASSWORD")
    if not (email and password):
        raise ReconToolError(
            "credentials_missing",
            "缺凭据：请设置环境变量 CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD（或在 MCP .env 里配置）")
    return email, password


def _live_session():
    sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
    try:
        import forum_research as fr  # noqa: WPS433（唯一 HTTP 实现；顶层 import requests / bs4）
        import requests  # noqa: WPS433
    except ImportError as e:
        raise ReconToolError("deps_missing", f"缺依赖（{e}）——请用 MCP venv 的解释器（$WQ_PY）运行") from e
    email, password = _load_credentials(fr)
    s = requests.Session()
    s.headers.update({"User-Agent": fr.UA})
    try:
        fr.authenticate(s, email, password)
        fr.sso_handshake(s)
    except Exception as e:
        raise ReconToolError("auth_failed", f"forum auth failed: {type(e).__name__}: {e}") from e
    return s, fr


def _resolve_post_id(session, fr, click_href: str) -> Optional[str]:
    """把搜索命中的 click_href 解析成**标量** post_id；拿不到返回 None。

    ★ 为什么要这层适配（2026-10-01 实测根因）：
    `forum_research.resolve_id` 返回的是 **三元组** `(post_id, is_community_post, url)`，
    不是标量。此前这里直接 `pid = fr.resolve_id(...)` 把整个元组当 id 拼进
    `/community/posts/{pid}.json`，URL 变成 `.../posts/('33036460396567', True, 'https://...').json`
    → 平台恒定 404 `InvalidEndpoint` → **读帖 100% 失败**（30 hits / 17 read_errors）。
    而 `get_with_retry` 对 404 不重试、直接返回响应，`read_post` 见非 200 返回 None，
    于是整条链路静默退化成 `read_failed`，看起来和「论坛无解」一模一样。

    第二个元素 `is_community_post` 同样必须校验：非社区帖（帮助中心文章）没有
    `/community/posts/{id}.json` 端点，硬读必然 404，应当直接跳过而不是计入 read_errors。

    兼容标量返回（契约若再变回标量也不会炸）。
    """
    try:
        got = fr.resolve_id(session, click_href)
    except Exception as e:
        print(f"[forum_recon] resolve_id 异常（{str(click_href)[:60]}）：{e}", file=sys.stderr)
        return None
    if isinstance(got, (tuple, list)):
        if len(got) < 2:
            return None
        pid, is_community = got[0], got[1]
        if not pid or not is_community:
            return None
        return str(pid)
    return str(got) if got else None


def live_search_round(session, fr, query: str, max_pages: int, read_top: int,
                      seen: set, stats: Optional[Dict[str, int]] = None) -> List[Dict[str, Any]]:
    """一轮：搜 → 解析候选 → 读帖 → 返回新读到的结构化文章（跳过已读）。

    `stats` 累计这一轮的可靠性信号（`recon` 据此判断「没搜到」是真无解还是检索坏了）：
    searches_ok / search_errors / hits / reads_ok / read_errors。
    """
    st = stats if stats is not None else {}
    for k in ("searches_ok", "search_errors", "hits", "reads_ok", "read_errors"):
        st.setdefault(k, 0)
    out: List[Dict[str, Any]] = []
    try:
        hits = fr.search_html(session, query, max_pages=max_pages) or []
    except Exception as e:
        st["search_errors"] += 1
        print(f"[forum_recon] 搜索失败（{query}）：{e}", file=sys.stderr)
        return out
    st["searches_ok"] += 1
    candidates = hits[:read_top]
    st["hits"] += len(candidates)
    for hit in candidates:
        pid = hit.get("post_id") or hit.get("id")
        if not pid and hit.get("click_href"):
            pid = _resolve_post_id(session, fr, hit["click_href"])
        if not pid or pid in seen:
            continue
        seen.add(pid)
        try:
            post = fr.read_post(session, pid) or {}
        except Exception as e:
            st["read_errors"] += 1
            print(f"[forum_recon] 读帖失败（{pid}）：{e}", file=sys.stderr)
            continue
        if not post:
            st["read_errors"] += 1
            continue
        st["reads_ok"] += 1
        out.append({
            "post_id": pid,
            "title": post.get("title") or hit.get("title") or "",
            "votes": post.get("votes") or hit.get("votes"),
            "body": post.get("body") or post.get("text") or "",
            "query": query,
        })
        time.sleep(2.5)          # 限速：与 forum_research 的 page_delay 同一包络
    return out


def _control_probe(session, fr) -> Optional[Tuple[str, str]]:
    """「无解」成立前的对照检索：`CONTROL_QUERY` 必须有结果。`forum_research.search_html` 遇到非 200 只 log 一行、返回空列表——
    会话过期 / 被拦 / 页面改版时，任何检索都会安静地得到 0 条，看起来和「论坛没有答案」一模一样。
    通过返回 None；失败返回 (code, message)。"""
    try:
        hits = fr.search_html(session, CONTROL_QUERY, max_pages=1) or []
    except Exception as e:
        return ("control_probe_failed", f"对照检索异常：{e}")
    if not hits:
        return ("control_probe_failed",
                f"对照检索（{CONTROL_QUERY!r}）0 结果——检索通道疑似失效（会话过期 / 被拦 / 页面改版），不能把「没搜到」当作「论坛无解」")
    return None


def _unreliable_reason(stats: Dict[str, int]) -> Optional[Tuple[str, str]]:
    """没找到有效文章时，先看这次检索本身可不可信；可信返回 None。"""
    if stats.get("searches_ok", 0) == 0:
        return ("search_failed", f"所有检索均失败（{stats.get('search_errors', 0)} 次），没有任何一轮真正搜成")
    if stats.get("search_errors", 0) > 0:
        return ("search_failed",
                f"{stats['search_errors']} 轮检索异常（另 {stats['searches_ok']} 轮成功）——结论不可信，重跑")
    if stats.get("hits", 0) > 0 and stats.get("reads_ok", 0) == 0:
        return ("read_failed", f"搜到 {stats['hits']} 条候选但读帖全部失败——没有读到任何正文，不能据此说「无有效文章」")
    return None


# ---------------------------------------------------------------- 主流程
def _record_error(qkey: str, question: str, context: Dict[str, str], db_path: str, code: str, message: str,
                  stats: Dict[str, int], tried: List[str]) -> Dict[str, Any]:
    """工具故障落库：`forum_recon_error_<qkey>`（region 作用域）。**不写负结果、不入缓存**——故障应当重试，不该被回放一周。"""
    region = str(context.get("region") or "GLOBAL")
    result: Dict[str, Any] = {
        "question": question, "question_key": qkey, "found": None, "status": RE.STATUS_ERROR,
        "reason_code": code, "error": message, "searched_at": _now_iso(),
        "queries_tried": list(tried), "search_stats": dict(stats),
        "note": "工具故障 ≠ 论坛无解：不作判死证据、不入缓存；修好后重跑同一问题",
    }
    key = RE.key_error(qkey)
    try:
        _ledger_upsert(db_path, region, key, {**result, "ttl_note": "故障记录不入缓存；同问题下次调用会重新 live 查"})
        result["sink"] = f"{region}/{key}"
    except Exception as e:
        result["sink_error"] = str(e)
    print(f"[forum_recon] 工具故障（{code}）：{message}\n"
          f"[forum_recon] 这不是「论坛无解」：不作判死证据、不入缓存；已记 {region}/{key}", file=sys.stderr)
    return result


def _mirror_cached(db_path: str, context: Dict[str, str], qkey: str, cached: Dict[str, Any], out_mode: str) -> None:
    """缓存回放时，保证**本 region** 的 ledger 里有这条记录。

    缓存文件按问题键（不分 region）存；同一问题在别的 region 查过、或 ledger 被重置后，回放的结果在本 region 的 ledger 里没有记录——
    判死闸（`seal_dead_end`）按 `question_key` 回 ledger 核对取证，找不到就会拒绝，而调用方又无从「重查」（缓存会一直命中）。
    尽力而为：写不进去不影响回放本身（`sink_error` 记在结果里）。
    """
    kind = RE.classify_record(cached)
    if kind == "found" and out_mode == "kb":
        return                                              # 有货且落点是 KB（合并入 community_tpl_kb），不是 ledger 键
    key = RE.key_negative(qkey) if kind == "negative" else RE.key_found(qkey) if kind == "found" else None
    if key is None:
        return
    region = str(context.get("region") or "GLOBAL")
    try:
        sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
        from lib.wqb_db import get_conn  # noqa: WPS433
        conn = get_conn(db_path)
        try:
            exists = conn.execute("SELECT 1 FROM ledger_kv WHERE region=? AND key=?", (region, key)).fetchone()
        finally:
            conn.close()
        if not exists:
            _ledger_upsert(db_path, region, key, {**{k: v for k, v in cached.items() if k != "from_cache"},
                                                  "ttl_note": "缓存回放补写（本 region 的 ledger 原先没有这条记录）"})
            cached["sink"] = f"{region}/{key}"
    except Exception as e:
        cached["sink_error"] = str(e)


def recon(question: str, context: Dict[str, str], out_mode: str, limit: int,
          max_rounds: int, queries: Optional[str], dry_run: bool,
          db_path: str) -> Dict[str, Any]:
    qkey = _qkey(question)
    cache = _load_recon_cache()
    cached = cache.get("entries", {}).get(qkey)
    if _cache_reusable(cached):
        print(f"[forum_recon] 缓存命中（{TTL_DAYS}d TTL）：question sha1={qkey}，"
              f"found={cached.get('found')}，不重复 live 查")
        cached["from_cache"] = True
        if not dry_run:
            _mirror_cached(db_path, context, qkey, cached, out_mode)
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
    stats: Dict[str, int] = {"searches_ok": 0, "search_errors": 0, "hits": 0, "reads_ok": 0, "read_errors": 0}
    try:
        session, fr = _live_session()
    except Exception as e:                                   # 鉴权 / 凭据 / 依赖——都是故障，不是无解
        code = e.code if isinstance(e, ReconToolError) else ("deps_missing" if isinstance(e, ImportError) else "unexpected")
        return _record_error(qkey, question, context, db_path, code, str(e), stats, tried)

    round_no = 0
    # 自适应额度：以查出 limit 篇有效文章为标准；关键词包用尽后继续扩后缀变体，
    # 直到命中或触到安全上限（防失控）。
    ext_packs = [f"{p} {s}" for p in packs[:3] for s in ("实盘", "经验", "问题", "解决")]
    queue = list(packs) + [p for p in ext_packs if p not in packs]
    while len(useful) < limit and round_no < max_rounds and queue:
        query = queue.pop(0)
        tried.append(query)
        round_no += 1
        print(f"[forum_recon] 第 {round_no} 轮检索：{query!r}（已有 {len(useful)} 篇有效）")
        for post in live_search_round(session, fr, query, max_pages=2, read_top=6, seen=seen, stats=stats):
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
        "status": RE.status_of(found),
        "n_useful": len(useful), "articles": useful, "queries_tried": tried,
        "rounds": round_no, "searched_at": _now_iso(),
        "note": ("以有效文章为标准自适应扩展；命中即收束" if found else
                 f"关键词空间已扩至 {len(queue) + round_no} 变体/触安全上限 {max_rounds}，仍无有效文章"),
    }
    if stats.get("search_errors"):
        result["search_errors"] = stats["search_errors"]         # 有货但中途有轮次失败：如实记，不影响「有货」
    if not found:
        problem = _unreliable_reason(stats) or _control_probe(session, fr)
        if problem:                                              # 没搜到 ≠ 无解：检索本身不可信 → 故障，不落负结果
            return _record_error(qkey, question, context, db_path, problem[0], problem[1], stats, tried)
        result["search_stats"] = dict(stats)
        _record_negative(cache, qkey, result, db_path, context)
        return result

    if out_mode == "kb":
        where = _kb_merge_entries(db_path, useful)
    else:
        region = str(context.get("region") or "GLOBAL")
        where = f"{region}/{RE.key_found(qkey)}"
        _ledger_upsert(db_path, region, RE.key_found(qkey),
                       {**result, "ttl_note": "同问题 7 天内复用，勿重复 live 查"})
    cache.setdefault("entries", {})[qkey] = {k: v for k, v in result.items() if k != "articles"} | {
        "articles": useful, "sink": where}
    _save_recon_cache(cache)
    print(f"[forum_recon] 有效文章 {len(useful)} 篇 → {where}")
    return result


def _record_negative(cache: Dict[str, Any], qkey: str, result: Dict[str, Any],
                     db_path: str, context: Dict[str, str]) -> None:
    """负结果落库：判死证据链的一环（decision-table D2「论坛无解」），7 天负缓存。
    **只在检索可靠完成时调用**（见 `recon`）——故障走 `_record_error`。"""
    region = str(context.get("region") or "GLOBAL")
    sink = f"{region}/{RE.key_negative(qkey)}"
    try:
        _ledger_upsert(db_path, region, RE.key_negative(qkey),
                       {**result, "ttl_note": "负结果 7 天内勿重复 live 查（缓存回放）"})
        result["sink"] = sink
    except Exception as e:
        result["sink_error"] = str(e)
    cache.setdefault("entries", {})[qkey] = result
    _save_recon_cache(cache)
    print(f"[forum_recon] 无解（检索可靠完成；负结果已入库：{sink}）——可作「论坛无解」判死证据")


def exit_code(result: Dict[str, Any]) -> int:
    """0=有货；2=无解（可靠的负结果）；1=工具故障。干跑恒 0。"""
    if result.get("dry_run"):
        return 0
    found = result.get("found")
    return 0 if found is True else 2 if found is False else 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="问题驱动论坛只读检索（recon）：以查出有效文章为标准，产出必入库（含可靠的负结果；工具故障单独记 error，不算无解）")
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
    return exit_code(result)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _pyenv  # noqa: E402  文档里写的是 `python tools/forum_recon.py`——系统解释器缺 requests / bs4 时自动切到 MCP venv
    _pyenv.reexec_under_venv()
    sys.exit(main())
