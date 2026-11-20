# -*- coding: utf-8 -*-
"""_lib/forum_corpus.py — 论坛语料的**确定性**检索通道。

## 为什么弃用 Playwright 搜索（2026-11-19 定性 · 11-20 该工具整体退役）

旧 `search_forum_posts` 走 Playwright 抓取 `https://support.worldquantbrain.com/hc/<locale>/search`，
抓三个查询词（`alpha` / `earnings surprise` / `sharpe` / `post earnings announcement drift`）实测：

| 现象 | 次数 | 含义 |
|---|---:|---|
| 客户端 30s 超时 | 3 | Playwright + Cloudflare 挑战页，握手慢 |
| 秒回 `total_found=0` 且 `navigation_failed=false` | 4 | **假信号** |

最后一行是根因：`forum_functions._search_forum_posts_impl` 里，等不到选择器 `ul.search-results-list` 时
只记 warning 并**显式不设 nav_failed**（代码注释原话：「可能是真的没有结果，也可能是挑战页；不判 nav_failed」）。
⇒ **`total_found=0` 不构成「论坛无此内容」的证据**，任何把它当「可靠无结果」的判断都是错的。

## 本模块走的正路

Zendesk Community **列表端点**（同一 support session，无 Playwright）：

    GET https://support.worldquantbrain.com/api/v2/community/posts.json?per_page=100&page=N

实测（2026-11-19）：`count=11296` / `page_count=113`，列表项**自带**
`id / title / details(正文 HTML) / vote_sum / comment_count / created_at / html_url / topic_id`。

⇒ 论坛检索 = **全量拉取 + 本地关键词过滤**，确定性、可复现、零超时、零误判。
   本地过滤实测（800 帖样本）：sharpe 378 / turnover 225 / correlation 180 / earnings 61 /
   crowding 40 / sentiment 38 / PEAD 5 命中。

## 鉴权

与 `forum_functions.ForumClient._ensure_support_session` 同源：BRAIN 平台登录 → 同 session 访问
`https://worldquantbrain.zendesk.com/access?...` 完成 SSO 握手 → 同 session 取 support JSON。

⚠ **必须用 `requests` 而不是 urllib**（实测 2026-11-19）：urllib 的重定向处理在
`worldquantbrain.zendesk.com/access` → `support.worldquantbrain.com/hc/<locale>` 这一跳上
返回 **406 Not Acceptable**，握手失败；同一流程用 `requests`（allow_redirects=True + 浏览器 UA）
实测 **200 / final_url=support HC / posts count=11296**。
本模块自建 `requests.Session`（不依赖 MCP 包，skill 装到仓库外也能跑）。
"""
from __future__ import annotations

import base64
import html
import json
import re
from typing import Any, Dict, List, Optional, Sequence

try:
    import requests
except ImportError:  # pragma: no cover - 环境缺 requests 时给出明确指引
    requests = None  # type: ignore

SUPPORT_BASE = "https://support.worldquantbrain.com"
ZENDESK_BRAND_ID = "1500000894061"
BRAIN_BASE = "https://api.worldquantbrain.com"
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
_ACCEPT_HTML = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"


def strip_html(raw: Optional[str]) -> str:
    """HTML → 纯文本（论坛正文是 HTML，关键词匹配前必须去标签）。"""
    if not raw:
        return ""
    txt = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    txt = re.sub(r"(?s)<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    return re.sub(r"\s+", " ", txt).strip()


def kw_hit_ratio(text: str, kw: str) -> float:
    """关键词在文本中的**词命中率**（0–1）。

    ⚠ 不能整串子串匹配：查询 "post earnings announcement drift" 在语料里写作
    "post-earnings announcement drift"（带连字符），整串匹配 0 命中。
    ⇒ 按词拆开算命中率，连字符/标点/大小写差异都不影响。
    """
    words = [w for w in re.split(r"\W+", str(kw).lower()) if len(w) > 1]
    if not words:
        return 0.0
    hit = sum(1 for w in words if w in text)
    return hit / len(words)


def score_post(post: Dict[str, Any], kws: Sequence[str]) -> tuple:
    """给一帖打分：标题命中权重 3、正文命中权重 1，按词命中率折算。

    纯函数，便于单测（2026-11-19：评分逻辑曾是 search() 内联，无法验证）。
    """
    title = (post.get("title") or "").lower()
    body = (post.get("body") or "").lower()
    score = 0.0
    matched: List[str] = []
    for kw in kws:
        r_title = kw_hit_ratio(title, kw)
        r_body = kw_hit_ratio(body, kw)
        if r_title <= 0 and r_body <= 0:
            continue
        score += 3.0 * r_title + 1.0 * r_body
        if max(r_title, r_body) >= 0.5:
            matched.append(kw)
    return score, matched


class ForumCorpus:
    """论坛语料的确定性访问器（列表端点 + 本地过滤）。"""

    def __init__(self, email: str = "", password: str = "", locale: str = "en-us"):
        if requests is None:
            raise RuntimeError(
                "forum_corpus 需要 requests（pip install requests）；"
                "实测 urllib 走 Zendesk SSO 会 406")
        self.email = email
        self.password = password
        self.locale = locale
        self._session: Optional[Any] = None
        self._corpus: Optional[List[Dict[str, Any]]] = None

    # ---- 会话 ----
    def _build_session(self) -> Any:
        s = requests.Session()
        s.headers.update({"User-Agent": _UA})
        if self.email and self.password:
            token = base64.b64encode(f"{self.email}:{self.password}".encode()).decode()
            r = s.post(BRAIN_BASE + "/authentication", data=b"",
                       headers={"Authorization": "Basic " + token}, timeout=40)
            r.raise_for_status()
        access = (
            "https://worldquantbrain.zendesk.com/access"
            f"?brand_id={ZENDESK_BRAND_ID}&locale={self.locale}"
            f"&return_to={SUPPORT_BASE}/hc/{self.locale}"
        )
        rr = s.get(access, allow_redirects=True, timeout=45,
                   headers={"Accept": _ACCEPT_HTML})
        rr.raise_for_status()
        return s

    @property
    def session(self) -> Any:
        if self._session is None:
            self._session = self._build_session()
        return self._session

    # ---- 列表 ----
    def posts_page(self, page: int = 1, per_page: int = 100,
                   sort_by: str = "created_at", sort_order: str = "desc") -> Dict[str, Any]:
        url = (f"{SUPPORT_BASE}/api/v2/community/posts.json"
               f"?per_page={per_page}&page={page}&sort_by={sort_by}&sort_order={sort_order}")
        r = self.session.get(url, timeout=45,
                             headers={"Accept": "application/json", "User-Agent": _UA})
        r.raise_for_status()
        return r.json()

    def corpus(self, max_pages: int = 8, per_page: int = 100, refresh: bool = False) -> List[Dict[str, Any]]:
        """拉取语料（前 max_pages 页）。列表项自带正文，无需逐帖再读。"""
        if self._corpus is not None and not refresh:
            return self._corpus
        out: List[Dict[str, Any]] = []
        for page in range(1, max(1, int(max_pages)) + 1):
            try:
                data = self.posts_page(page=page, per_page=per_page)
            except Exception:
                break
            posts = data.get("posts") or []
            if not posts:
                break
            for p in posts:
                out.append({
                    "id": p.get("id"),
                    "title": p.get("title") or "",
                    "body": strip_html(p.get("details")),
                    "votes": p.get("vote_sum") or 0,
                    "comments": p.get("comment_count") or 0,
                    "created_at": p.get("created_at") or "",
                    "url": p.get("html_url") or p.get("url") or "",
                })
        self._corpus = out
        return out

    # ---- 检索（本地过滤）----
    def search(self, keywords: Sequence[str], limit: int = 5,
               max_pages: int = 8, min_votes: int = 0) -> List[Dict[str, Any]]:
        """关键词检索。标题命中权重高于正文命中；同权重按赞数降序。"""
        corpus = self.corpus(max_pages=max_pages)
        kws = [str(k).strip().lower() for k in keywords if str(k).strip()]
        if not kws:
            return []
        hits = []
        for p in corpus:
            if (p.get("votes") or 0) < min_votes:
                continue
            score, matched = score_post(p, kws)
            if score:
                hits.append({**p, "match_score": score, "matched": matched})
        hits.sort(key=lambda x: (-x["match_score"], -(x.get("votes") or 0), x["title"]))
        return hits[:max(1, int(limit))]

    # ---- 单帖评论（需要时才读）----
    def post_comments(self, post_id: Any, page: int = 1) -> List[Dict[str, Any]]:
        url = f"{SUPPORT_BASE}/api/v2/community/posts/{post_id}/comments.json?page={page}&include=users"
        r = self.session.get(url, timeout=45,
                             headers={"Accept": "application/json", "User-Agent": _UA})
        r.raise_for_status()
        data = r.json()
        users = {u.get("id"): u.get("name") for u in (data.get("users") or []) if isinstance(u, dict)}
        out = []
        for c in (data.get("comments") or []):
            out.append({
                "author": users.get(c.get("author_id"), "Unknown"),
                "body": strip_html(c.get("body")),
                "date": c.get("created_at") or "",
            })
        return out
