#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""forum_mcp.py — 论坛访问的**唯一实现**（2026-11-18 用户裁定）。

全项目查论坛一律按 `docs/reference/forum_and_doc_tools_guide.md`：只经 `wq-brain-http`
的 6 个 MCP 工具 —— `search_forum_posts_local` / `get_forum_posts`（**确定性检索，唯一检索通道**）/
`read_forum_post` / `get_glossary_terms` /
`get_documentations` / `get_documentation_page`。

**不再** requests 抓 HTML 搜索页、**不再**直连 Zendesk JSON API、**不再**拿 WebSearch 当论坛通道。
（WebSearch/WebFetch 只用于**论文**取证线 EVID-PAPER，与论坛线分开。）

要点（与 guide 对齐）：
  - **检索唯一通道 = `search_forum_posts_local`**：服务端走 Zendesk 列表端点（`/api/v2/community/posts.json`，
    实测 count=11296 / page_count=113，列表项自带正文）拉语料后本地词命中率过滤，**确定性、零超时**。
  - 旧 `search_forum_posts`（Playwright 抓 Cloudflare 页）**已于 2026-11-20 整体退役**
    （用户裁定）：它的「0 结果 + navigation_failed=false」是**假信号**（挑战页与真无结果无法区分），
    实现已从 MCP 删除，本项目不得再引用。
  - 读帖 `read_forum_post`：`article_id` 接受纯数字或含 `/posts/<数字>` 的 URL；标题前缀（如 `LC97552`）会被拒。
  - search 坏时的绕行：`get_documentations` → `get_documentation_page(page_id)` → 从正文
    `<a href=".../posts/<数字>-...">` 提取数字 id → `read_forum_post` 直读。
  - 凭据由**服务端配置**读取；本模块不收、不读、不传口令（skill 审查 FB-10 / X-15）。

传输复用 `tools/mcp_http_caller.py::McpHttpClient`（streamable-HTTP、session 落盘复用、
服务地址从 `.mcp.json` 解析）。客户端超时设得比服务端 search 的 `overall_timeout`(120s) 长，
避免 guide §2.2 说的「客户端 30s 先掐断」错配。

本模块是**库**（无 `__main__` CLI），供 `tools/forum_recon.py` / `tools/diag_forum_read.py` 复用；
论坛检索的额度/缓存/三态结局/入库契约仍在 `forum_recon.py`（单一实现 `src/wqb/recon_evidence.py`）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# 定位同级 tools/ 目录以 import mcp_http_caller（它自带 src 自举）。
_TOOLS = Path(__file__).resolve().parent.parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
import mcp_http_caller as _MHC  # noqa: E402

REPO_ROOT = _MHC.REPO_ROOT

#: guide 规定的论坛/文档工具白名单——本模块只允许调这些（机械闸据此校验）。
ALLOWED_TOOLS = frozenset({
    "read_forum_post",
    "get_glossary_terms",
    "get_documentations",
    "get_documentation_page",
    # 2026-11-19：确定性检索通道（Zendesk 列表端点 + 本地过滤）。
    # 2026-11-20：旧 Playwright `search_forum_posts` 已整体退役，这两个是**唯一**检索通道。
    "get_forum_posts",
    "search_forum_posts_local",
})

#: 客户端超时（秒）：> 服务端 search overall_timeout(120s)，避免传输层先掐断。
CLIENT_TIMEOUT = 180
_SESSION_FILE = REPO_ROOT / "cache" / "_forum_mcp_session"

#: 从 URL/HTML 提取帖子数字 id（与 forum_functions._extract_post_id 同口径）。
_POST_ID_RE = re.compile(r"/posts/(\d+)")


def client(timeout: int = CLIENT_TIMEOUT) -> "_MHC.McpHttpClient":
    """构造指向 wq-brain-http 的 MCP 客户端（地址从 .mcp.json 解析，session 落盘复用）。"""
    uri = _MHC.service_uri("wq-brain-http")
    return _MHC.McpHttpClient(uri, _SESSION_FILE, timeout=timeout)


def _call(cli, tool: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if tool not in ALLOWED_TOOLS:
        raise ValueError(f"forum_mcp 只允许 guide 白名单工具 {sorted(ALLOWED_TOOLS)}，收到 {tool!r}")
    out = cli.call_tool(tool, arguments)
    return out if isinstance(out, dict) else {"raw": out}


# ---------------------------------------------------------------- 工具封装
def read_post(cli, article_id: str, include_comments: bool = True) -> Dict[str, Any]:
    """读单帖全文（含评论）。返回 {success, post:{title,body,details:{votes,...}}, comments} 或 {error}。"""
    return _call(cli, "read_forum_post",
                 {"article_id": str(article_id), "include_comments": bool(include_comments)})


def glossary_terms(cli) -> Any:
    return _call(cli, "get_glossary_terms", {})


def docs_index(cli) -> Any:
    """官方文档集合索引（11 个集合，每集 pages:[{id,title,...}]）。"""
    return _call(cli, "get_documentations", {})


def doc_page(cli, page_id: str) -> Dict[str, Any]:
    """单页文档。content[].value 是 HTML 字符串（链接在 <a href> 里）。"""
    return _call(cli, "get_documentation_page", {"page_id": str(page_id)})


def list_posts(cli, page: int = 1, per_page: int = 100) -> Dict[str, Any]:
    """列出论坛帖（确定性列表端点，实测 count=11296 / page_count=113）。"""
    return _call(cli, "get_forum_posts",
                 {"page": int(page), "per_page": int(per_page)})


def search_posts_local(cli, keywords: List[str], limit: int = 5,
                       max_pages: int = 8) -> Dict[str, Any]:
    """确定性论坛检索（列表端点 + 本地词命中率过滤）。**查得到**的通道。"""
    return _call(cli, "search_forum_posts_local",
                 {"keywords": list(keywords), "limit": int(limit),
                  "max_pages": int(max_pages)})


# ---------------------------------------------------------------- 结果判读 / id 提取
def is_error(res: Any) -> bool:
    """MCP 返回是否为故障（含传输层 error / success=False / 非 dict）。"""
    if not isinstance(res, dict):
        return True
    if "error" in res:
        return True
    if res.get("success") is False:
        return True
    return False


def search_results(res: Dict[str, Any]) -> List[Dict[str, Any]]:
    if is_error(res):
        return []
    return list(res.get("results") or [])


def post_id_from_link(link: Any) -> Optional[str]:
    """从帖子 URL 提取数字 id（MCP search 的 results[].link 含 /posts/<id>-slug）。"""
    m = _POST_ID_RE.search(str(link or ""))
    return m.group(1) if m else None


def post_ids_from_html(html: Any) -> List[str]:
    """从文档页 HTML 提取全部帖子数字 id（去重保序）——guide §2.3 绕行路径的核心。"""
    return list(dict.fromkeys(_POST_ID_RE.findall(str(html or ""))))


def discover_post_ids_via_doc(cli, page_id: str) -> List[str]:
    """绕行：读一个文档页，抽出其中引用的帖子数字 id（供 read_post 直读）。"""
    page = doc_page(cli, page_id)
    if is_error(page):
        return []
    blocks = page.get("content") or []
    html = " ".join(str(b.get("value", "")) for b in blocks if isinstance(b, dict))
    return post_ids_from_html(html)


def post_body(res: Dict[str, Any]) -> str:
    """从 read_post 返回里取正文文本。"""
    if is_error(res):
        return ""
    post = res.get("post") or {}
    return str(post.get("body") or post.get("text") or "")


def post_title(res: Dict[str, Any]) -> str:
    if is_error(res):
        return ""
    return str((res.get("post") or {}).get("title") or "")


def post_votes(res: Dict[str, Any]) -> Any:
    if is_error(res):
        return None
    details = (res.get("post") or {}).get("details") or {}
    return details.get("votes")
