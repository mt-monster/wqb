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
  - found=false → 落 `forum_recon_negative_<qkey>`（**负结果也是判死证据**，
                 7 天内重复调用直接回放缓存，不重复 live 查）；
                 ⚠ 仅限**真实检索过**（rounds ≥1 且无 error）的无解结论；
  - found=null  → 落 `forum_recon_error_<qkey>`（**工具故障 = 未取证，不是判死证据**；
                 2026-09-29 修复：此前故障被记成 found=False，导致「工具坏了 ≡ 论坛无解」
                 的假阴性误判死；故障结论不进 TTL 缓存，须修复后重试）；
  - 每条有效文章带：post_id / 标题 / 赞数 / 摘录 / 适用边界(context) / 幽灵算子标注。

退出码：0=有产出（有效文章≥1）；2=确认无解（负结果已入库，可作 D2 判死取证）；
        3=未取证（工具故障/零轮检索，**不得**据此处判死）；1=工具异常。
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

#: 中文领域词典（滑窗候选 ∩ 本表）——论坛真实用语。
#: 2026-09-29：旧派生用 `[\u4e00-\u9fff]{2,6}` 机械切窗口，把完整词从中间劈开
#: （实证："表达式骨架设计灵感" → "表达式骨架设" + "计灵感"），搜这种碎片必然 0 命中。
CJK_DOMAIN = (
    "中性化", "换手", "因子", "表达式", "骨架", "模板", "算子", "公式", "权重", "相关性",
    "子宇宙", "实盘", "经验", "配方", "破墙", "卡墙", "判死", "覆盖", "衰减", "窗口",
    "分组", "排序", "中性", "组合", "数据集", "字段", "区域", "回测", "提交", "门槛",
    "指标", "降噪", "正交", "多样", "结构", "时序", "横截面", "事件", "门控", "价差",
    "卖空", "情绪", "新闻", "财报", "分析师", "机构", "宏观", "风险", "波动", "流动性",
)
#: 墙码 → 论坛领域词（子串匹配，覆盖平台墙码命名惯例）
_WALL_MAP = (
    ("SUB_UNIVERSE", ("子宇宙", "sub-universe")),
    ("SUBUNIVERSE", ("子宇宙", "sub-universe")),
    ("SHARPE", ("sharpe",)),
    ("FITNESS", ("fitness",)),
    ("TURNOVER", ("换手", "turnover")),
    ("WEIGHT", ("权重", "weight")),
    ("CONCENTRAT", ("权重集中", "concentrated")),
    ("CORRELATION", ("相关性", "correlation")),
    ("PROD", ("prod",)),
    ("SELF", ("自相关", "self correlation")),
    ("POWER_POOL", ("power pool",)),
    ("THEME", ("主题",)),
    ("COVERAGE", ("覆盖", "coverage")),
    ("RETURNS", ("returns",)),
    ("DIVERSITY", ("多样性", "diversity")),
)


def _wall_terms(wall: str) -> List[str]:
    """墙码 → 论坛领域词（大小写无关的子串匹配）。"""
    w = str(wall or "").upper()
    out: List[str] = []
    for key, vals in _WALL_MAP:
        if key in w:
            for v in vals:
                if v not in out:
                    out.append(v)
    return out


def _cjk_domain_terms(question: str) -> List[str]:
    """从连续中文串里拣出领域词：滑窗 2–4 字 ∩ CJK_DOMAIN（长词优先）。

    避免机械切碎完整词，同时不依赖分词库（本工具须保持零第三方依赖）。
    """
    out: List[str] = []
    for seg in re.findall(r"[\u4e00-\u9fff]{2,}", question):
        n = len(seg)
        for size in (4, 3, 2):            # 长词优先：先试 4 字，避免 "表达式" 被 "表达" 抢先
            for i in range(0, n - size + 1):
                w = seg[i:i + size]
                if w in CJK_DOMAIN and w not in out:
                    out.append(w)
    return out


def plan_queries(question: str, context: Dict[str, str], explicit: Optional[str]) -> List[str]:
    """派生关键词包（**领域实体优先**，2026-09-29 重写）。

    旧实现按「CJK 碎片 + ASCII + context」顺序取 tokens，导致：
      - 中文问句被 2–6 字机械窗口劈碎（"表达式骨架设 计灵感"）；
      - context 里最有检索价值的英文实体（dataset / 墙码 / 算子名）被排到末尾，
        只在 `tokens[1:3]` 里偶然露脸，主包全围绕中文碎片 → 论坛 0 命中。

    新包序（具体→宽泛）：
      ① 实体 × 实体（dataset/family × 墙词 / 算子名 × 墙词）
      ② 实体 × 领域后缀（实盘/经验/配方/破墙）
      ③ 单实体（dataset、墙词、算子名、字段名）
      ④ 中文领域词（滑窗 ∩ CJK_DOMAIN）× region
    """
    if explicit:
        return [q.strip() for q in explicit.split(",") if q.strip()]

    region = str(context.get("region") or "").strip()
    # ① context 里的高价值英文实体
    entities: List[str] = []
    for k in ("dataset", "family"):
        v = str(context.get(k) or "").strip()
        if v and v.lower() not in _STOP:
            entities.append(v)
    entities.extend(_wall_terms(context.get("wall", "")))

    # ② question 里的 ASCII 实体：含下划线/数字的多为算子名或字段名，优先级最高
    asc = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", question)]
    asc = [w for w in asc if w.lower() not in _STOP and w.lower() != region.lower()]
    ent_like = [w for w in asc if ("_" in w) or any(c.isdigit() for c in w)]
    plain_asc = [w for w in asc if w not in ent_like]

    prim: List[str] = []
    for w in entities + ent_like + plain_asc:
        if w and w not in prim:
            prim.append(w)

    # ③ 中文领域词（不再用机械窗口）
    cjk_terms = _cjk_domain_terms(question)
    # 问题自身术语优先：问句才是检索意图的载体，context 实体（dataset/墙词）次之。
    # 若让 context 独占前排，会把 "short interest" 这类问题核心词挤到截断层之外。
    q_terms = ent_like + plain_asc
    c_terms = entities

    packs: List[str] = []
    for i in range(min(len(q_terms), 3)):            # ① 问题术语两两组合（最贴意图）
        for j in range(i + 1, min(len(q_terms), 3)):
            packs.append(f"{q_terms[i]} {q_terms[j]}")
    for a in q_terms[:2]:                            # ② 问题术语 × context 实体
        for b in c_terms[:2]:
            packs.append(f"{a} {b}")
    packs.extend(q_terms[:4])                        # ③ 单术语（问题优先）
    packs.extend(c_terms[:4])
    for e in (q_terms[:1] + c_terms[:1]):            # ④ 实体 × 领域后缀
        for suf in ("实盘", "经验", "配方", "破墙"):
            packs.append(f"{e} {suf}")
    for w in cjk_terms[:4]:                          # ⑤ 中文领域词（带 region 变体）
        packs.append(w)
        if region and region.upper() not in ("GLOBAL", "GLOBAL_ALL"):
            packs.append(f"{region} {w}")
    if not packs:                                    # 兜底：绝不返回空包（空包 = 零轮 = 未取证）
        packs = [region or "worldquant", "alpha"]

    out: List[str] = []
    for p in packs:
        if p and p not in out:
            out.append(p)
    return out


# ---------------------------------------------------------------- 有效文章判据
def is_useful(post: Dict[str, Any]) -> bool:
    """有效文章 = 正文足量 且 含可操作标记，标题非公告/闲聊。

    2026-09-29：正文读不到时**降级用搜索摘要**（snippet）。此前 read_post 失败即判废，
    把「读不了」和「没内容」混为一谈；摘要虽短，仍可回收标题+关键词级线索。
    """
    title = str(post.get("title") or "")
    if any(n in title for n in TITLE_NOISE):
        return False
    body = str(post.get("body") or post.get("text") or "")
    snippet = str(post.get("snippet") or "")
    if len(body) >= 200:
        basis, need = body, 200
    else:
        basis, need = snippet, 80          # 摘要天然短，门槛相应下调
    if len(basis) < need:
        return False
    low = (title + "\n" + basis[:2000]).lower()
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
    # 2026-09-28 修复：此前 fr.load_creds(None) 路径为 None 直接 TypeError，
    # 且把返回的 dict 直接解包成两个变量（得到的是键名不是凭据）——论坛 live 路径从未可用。
    env_path = os.environ.get("WQ_FORUM_ENV") or os.path.join(
        REPO_ROOT, "world-quant-brain-mcp", ".env"
    )
    creds = fr.load_creds(env_path)
    email = creds.get("CREDENTIALS_EMAIL")
    password = creds.get("CREDENTIALS_PASSWORD")
    if not email or not password:
        raise RuntimeError(f"forum credentials missing in {env_path} (CREDENTIALS_EMAIL/PASSWORD)")
    fr.authenticate(s, email, password)
    fr.sso_handshake(s)
    return s, fr


def live_search_round(session, fr, query: str, max_pages: int, read_top: int,
                      seen: set, stats: Optional[Dict[str, int]] = None) -> List[Dict[str, Any]]:
    """一轮：搜 → 解析候选 → 读帖 → 返回新读到的结构化文章（跳过已读）。

    `stats` 由调用方传入并累积四级计数（hits / resolved / read_ok / read_failed /
    resolve_failed / resolve_not_community），用于把「无有效文章」拆开归因——
    2026-09-29：n_useful=0 曾同时掩盖「搜不到 / 搜到但解析不了 / 读到但不合格」三种失败。
    """
    out: List[Dict[str, Any]] = []
    st = stats if stats is not None else {}

    def _bump(key: str) -> None:
        st[key] = st.get(key, 0) + 1

    try:
        hits = fr.search_html(session, query, max_pages=max_pages) or []
    except Exception as e:
        print(f"[forum_recon] 搜索失败（{query}）：{e}", file=sys.stderr)
        return out
    st["hits"] = st.get("hits", 0) + len(hits)
    for hit in hits[:read_top]:
        pid = hit.get("post_id") or hit.get("id")
        is_comm = True
        if not pid and hit.get("click_href"):
            try:
                # 2026-09-29 修复（命中率 0 的决定性根因）：
                # fr.resolve_id() 返回 **3-tuple** (post_id, is_community, url)，
                # 旧代码 `pid = fr.resolve_id(...)` 未解包 → pid 是 tuple →
                # read_post 拼出 ".../posts/(123, True, 'http://...').json" → 请求恒失败
                # → body 恒空 → is_useful 恒 False。搜到了也读不出来，n_useful 结构性为 0。
                rid = fr.resolve_id(session, hit["click_href"])
                if isinstance(rid, (tuple, list)):
                    seq = list(rid) + [None] * (3 - len(rid))
                    pid, is_comm = seq[0], bool(seq[1])
                else:                      # 防御：未来若改为返回单值
                    pid, is_comm = rid, True
                if pid:
                    _bump("resolved")
                else:
                    _bump("resolve_failed")
                if pid and not is_comm:
                    # 帮助中心文章不是社区帖，社区 JSON API 读不到，直接跳过
                    _bump("resolve_not_community")
                    pid = None
            except Exception as e:
                print(f"[forum_recon] 解析失败（{str(hit.get('title', ''))[:30]}）：{e}",
                      file=sys.stderr)
                _bump("resolve_failed")
                pid = None
        if not pid or pid in seen:
            continue
        seen.add(pid)
        try:
            post = fr.read_post(session, pid) or {}
        except Exception as e:
            print(f"[forum_recon] 读帖失败（{pid}）：{e}", file=sys.stderr)
            _bump("read_failed")
            continue
        body = post.get("body") or post.get("text") or ""
        if body:
            _bump("read_ok")
        else:
            _bump("read_failed")
        out.append({
            "post_id": pid,
            "title": post.get("title") or hit.get("title") or "",
            "votes": post.get("votes") or hit.get("votes"),
            "body": body,
            # 搜索摘要兜底：read_post 失败时 snippet 仍可回收（Zendesk 搜索结果自带）
            "snippet": hit.get("snippet") or "",
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
    stats: Dict[str, int] = {}
    # 自适应额度：以查出 limit 篇有效文章为标准；关键词包用尽后继续扩后缀变体，
    # 直到命中或触到安全上限（防失控）。
    ext_packs = [f"{p} {s}" for p in packs[:3] for s in ("问题", "解决", "技巧", "坑")]
    queue = list(packs) + [p for p in ext_packs if p not in packs]
    while len(useful) < limit and round_no < max_rounds and queue:
        query = queue.pop(0)
        tried.append(query)
        round_no += 1
        if session is None:
            try:
                session, fr = _live_session()
            except Exception as e:
                # 2026-09-29 修复：认证/环境故障 ≠ 论坛无解。
                # 旧行为把故障写成 found=False 并落 forum_recon_negative_*，
                # 而 SOP 把 found=false 当作 decision-table D2「论坛无解」的判死取证
                # → 工具坏了被当成论坛确实无解（假阴性），会误判死。
                # 现改为：found=None（未取证）+ 落 forum_recon_error_* + 不进 TTL 缓存。
                result = {"question": question, "question_key": qkey, "found": None,
                          "status": "error", "error": f"forum auth failed: {e}",
                          "searched_at": _now_iso(), "queries_tried": tried}
                _record_error(qkey, result, db_path, context)
                return result
        print(f"[forum_recon] 第 {round_no} 轮检索：{query!r}（已有 {len(useful)} 篇有效）")
        for post in live_search_round(session, fr, query, max_pages=2, read_top=6,
                                      seen=seen, stats=stats):
            if is_useful(post):
                raw = str(post.get("body") or "")
                if len(raw) < 200:                      # 走的是 snippet 降级通道
                    raw = str(post.get("snippet") or "")
                    stats["useful_from_snippet"] = stats.get("useful_from_snippet", 0) + 1
                excerpt = re.sub(r"\s+", " ", raw)[:400]
                useful.append({
                    "post_id": post["post_id"], "title": post["title"],
                    "votes": post.get("votes"), "excerpt": excerpt,
                    "applicable_context": dict(context), "source_query": query,
                    "ghost_operators": scan_ghosts(excerpt, ghost_names),
                })
        # 2026-09-29：逐轮归因输出，让「0 有效」能区分 搜不到 / 解析不了 / 读到但不合格
        print(f"[forum_recon]   本轮累计 hits={stats.get('hits', 0)} "
              f"resolved={stats.get('resolved', 0)} "
              f"read_ok={stats.get('read_ok', 0)} "
              f"read_failed={stats.get('read_failed', 0)} "
              f"resolve_failed={stats.get('resolve_failed', 0)} "
              f"not_community={stats.get('resolve_not_community', 0)}")

    found = len(useful) > 0
    result: Dict[str, Any] = {
        "question": question, "question_key": qkey, "found": found,
        "n_useful": len(useful), "articles": useful, "queries_tried": tried,
        "rounds": round_no, "searched_at": _now_iso(),
        # 归因台账：零命中时据此定位「搜不到 vs 读不了 vs 判不上」
        "stats": dict(stats),
        "note": ("以有效文章为标准自适应扩展；命中即收束" if found else
                 f"关键词空间已扩至 {len(queue) + round_no} 变体/触安全上限 {max_rounds}，仍无有效文章"),
    }
    if not found and stats.get("hits", 0) > 0 and stats.get("read_ok", 0) == 0:
        # 搜到了但一篇都没读出来 → 这是抓取链路故障的信号，不是「论坛无解」
        result["note"] += (
            f"；⚠ 搜到 {stats['hits']} 条但 read_ok=0，属抓取链路故障（非论坛无解），"
            "应排查 resolve/read 后再判"
        )
    # 一轮都没跑（关键词包为空 / 安全上限为 0）也算「未取证」，不得记成论坛无解
    if not found and round_no == 0:
        result = {"question": question, "question_key": qkey, "found": None,
                  "status": "error", "error": "no search round executed（关键词包为空或安全上限为 0）",
                  "searched_at": _now_iso(), "queries_tried": tried}
        _record_error(qkey, result, db_path, context)
        return result

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
    """负结果落库：判死证据链的一环（decision-table D2「论坛无解」），7 天负缓存。

    ⚠ 仅限**真实检索过**（rounds ≥1 且无 error）的无解结论。
    工具故障走 `_record_error`，不得走这里——否则故障会被误当「论坛无解」判死证据。
    """
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


def _record_error(qkey: str, result: Dict[str, Any],
                  db_path: str, context: Dict[str, str]) -> None:
    """工具故障落库：**不是**判死证据（2026-09-29 新增）。

    背景：此前认证/环境故障（如 `load_creds` TypeError、`No module named 'requests'`）
    被 `_record_negative` 记成 `found=False`，而 SOP 集成点把 `found=false` 当作
    decision-table D2「论坛无解」的判死取证 —— **工具坏了 ≡ 论坛无解**，属假阴性，
    实证 5 条里 2 条中招，后果是误把活路判死。

    现行为三件事：
      1. `found=None`（未知/未取证），区别于 `found=False`（确认无解）；
      2. 落独立的 `forum_recon_error_<qkey>`，**不占用** negative 键名，
         使 D2 取证判定可以靠「有无 error 字段」干净区分；
      3. **刻意不写入 TTL 缓存** —— 故障应当重试，不该被回放 7 天。
    """
    region = str(context.get("region") or "GLOBAL")
    sink = f"{region}/forum_recon_error_{qkey}"
    try:
        _ledger_upsert(db_path, region, f"forum_recon_error_{qkey}",
                       {**result, "ttl_note": "工具故障：非判死证据，不缓存，须重试取证"})
        result["sink"] = sink
    except Exception as e:
        result["sink_error"] = str(e)
    # 刻意不写 cache：故障结论不得被 TTL 回放
    print(f"[forum_recon] 工具故障（未取证，已入库：{sink}）"
          f"——**不得**作「论坛无解」判死证据，修复后重试")


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
    found = result.get("found")
    if found is None:
        # 未取证（工具故障）：区别于「确认无解」，调用方不得据此处判死
        return 3
    return 0 if found else 2


if __name__ == "__main__":
    sys.exit(main())
