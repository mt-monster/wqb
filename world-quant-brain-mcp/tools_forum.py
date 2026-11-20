"""论坛与消息工具 — MCP 工具层 (2026-08-13 自 main.py 按域拆分)。"""
import os, re
from typing import Dict, List, Optional, Any

from mcp_core import mcp, brain_client, load_config, logger

@mcp.tool()

async def get_messages(limit: Optional[int] = None, offset: int = 0) -> Dict[str, Any]:
    """
    Get messages for the current user with optional pagination.
    
    Args:
        limit: Maximum number of messages to return (e.g., 10 for top 10 messages)
        offset: Number of messages to skip (for pagination)
    
    Returns:
        Messages for the current user, optionally limited by count
    """
    try:
        return await brain_client.get_messages(limit, offset)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def get_glossary_terms() -> List[Dict[str, str]]:
    """
    Get glossary terms from WorldQuant BRAIN forum.
    
    Note: This uses Playwright and is implemented in forum_functions.py
    Credentials come from the server-side config only (CREDENTIALS_EMAIL / CREDENTIALS_PASSWORD);
    the tool takes no credential arguments (skills 审查 FB-10 / X-15：agent 不传口令).
    
    Returns:
        A list of glossary terms with definitions
    """
    try:
        config = load_config()
        credentials = config.get("credentials", {})
        email = credentials.get("email")
        password = credentials.get("password")
        if not email or not password:
            raise ValueError("Authentication credentials not provided or found in config.")
        
        return await brain_client.get_glossary_terms(email, password)
    except Exception as e:
        logger.error(f"Error in get_glossary_terms tool: {e}")
        return [{"error": str(e)}]

@mcp.tool()

async def get_forum_posts(page: int = 1, per_page: int = 100,
                          sort_by: str = "created_at",
                          sort_order: str = "desc") -> Dict[str, Any]:
    """
    List forum posts via the deterministic Zendesk Community list endpoint.

    Plain JSON API (no Playwright), so it is immune to Cloudflare challenge
    pages. Measured 2026-11-19: count=11296,
    page_count=113; each item carries id/title/body/votes/comments/url.

    Args:
        page: 1-based page number
        per_page: Items per page (max 100)
        sort_by: "created_at" | "updated_at" | "vote_sum"
        sort_order: "desc" | "asc"

    Returns:
        Page of posts plus corpus count metadata
    """
    try:
        config = load_config()
        credentials = config.get("credentials", {})
        email = credentials.get("email")
        password = credentials.get("password")
        if not email or not password:
            return {"error": "Authentication credentials not provided or found in config."}
        return await brain_client.list_forum_posts(email, password, page, per_page,
                                                   sort_by, sort_order)
    except Exception as e:
        logger.error(f"Error in get_forum_posts: {e!r}")
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def search_forum_posts_local(keywords: List[str], limit: int = 5,
                                   max_pages: int = 8) -> Dict[str, Any]:
    """
    Deterministic forum search: pull the post corpus via the list endpoint and filter locally.

    **The only forum search channel.** The legacy Playwright-based
    ``search_forum_posts`` tool was **retired on 2026-11-20** (user decision):
    it scraped a Cloudflare-protected search page and returned 0 results for
    every query while the corpus demonstrably contained hundreds of matches
    (sharpe / turnover / correlation), i.e. its "0 results" was a false signal.

    Args:
        keywords: Keywords to match (title hits weigh 3x body hits)
        limit: Max posts to return
        max_pages: How many corpus pages (100 posts each) to scan

    Returns:
        Matching posts with scores, plus how many posts were scanned
    """
    try:
        config = load_config()
        credentials = config.get("credentials", {})
        email = credentials.get("email")
        password = credentials.get("password")
        if not email or not password:
            return {"error": "Authentication credentials not provided or found in config."}
        return await brain_client.search_forum_posts_local(email, password, keywords,
                                                           limit, max_pages)
    except Exception as e:
        logger.error(f"Error in search_forum_posts_local: {e!r}")
        return {"error": f"An unexpected error occurred: {str(e)}"}

@mcp.tool()

async def read_forum_post(article_id: str, include_comments: bool = True) -> Dict[str, Any]:
    """
    Get a specific forum post by article ID.
    
    Note: This uses Zendesk support SSO plus JSON APIs and is implemented in forum_functions.py
    Credentials come from the server-side config only; the tool takes no credential arguments.
    
    Args:
        article_id: The article ID to retrieve (e.g., "32984819083415-新人求模板")
        include_comments: Also return the comment section (default: True)
    
    Returns:
        Forum post content with comments
    """
    try:
        config = load_config()
        credentials = config.get("credentials", {})
        email = credentials.get("email")
        password = credentials.get("password")
        if not email or not password:
            return {"error": "Authentication credentials not provided or found in config."}

        return await brain_client.read_forum_post(email, password, article_id, include_comments)
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
