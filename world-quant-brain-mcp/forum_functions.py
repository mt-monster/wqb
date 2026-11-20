#!/usr/bin/env python3
"""
WorldQuant BRAIN Forum Functions - Python Version
Comprehensive forum functionality including glossary, search, and post viewing using Playwright.
"""

import asyncio
import logging
import re
import sys
import time
import weakref
from datetime import datetime
from typing import Dict, Any, List

def log(message: str, level: str = "INFO"):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)

try:
    from playwright.async_api import async_playwright
except ImportError:
    log("Playwright not installed. Please install it with: pip install playwright", "ERROR")
    async_playwright = None

from bs4 import BeautifulSoup
import requests
import os


_BROWSER_PATH_CACHE = None
_BROWSER_PATH_CHECKED = False


def _html_to_text(html: str) -> str:
    """Convert forum HTML fragments to readable plain text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator='\n')
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)


def _kw_hit_ratio(text: str, kw: str) -> float:
    """关键词在文本中的词命中率（0–1）。

    ⚠ 不能整串子串匹配：查询 "post earnings announcement drift" 在语料里写作
    "post-earnings announcement drift"（带连字符），整串匹配 0 命中（实测）。
    """
    words = [w for w in re.split(r"\W+", str(kw).lower()) if len(w) > 1]
    if not words:
        return 0.0
    return sum(1 for w in words if w in text) / len(words)


def _extract_post_id(post_url_or_id: str) -> str:
    """Extract numeric forum post id from a raw id, slug, or full URL."""
    if not post_url_or_id:
        raise ValueError("Forum post id is required")
    match = re.search(r'/posts/(\d+)|^(\d+)', str(post_url_or_id))
    post_id = next((group for group in match.groups() if group), None) if match else None
    if not post_id:
        raise ValueError(f"Could not extract forum post id from: {post_url_or_id}")
    return post_id


def _extract_locale(post_url_or_id: str, default: str = "zh-cn") -> str:
    """Extract forum locale from URL when present."""
    if isinstance(post_url_or_id, str):
        match = re.search(r'/hc/([^/]+)/community/posts/', post_url_or_id)
        if match:
            return match.group(1)
    return default

# 导入浏览器设置模块
def get_browser_path():
    """获取可用的浏览器路径"""
    global _BROWSER_PATH_CACHE, _BROWSER_PATH_CHECKED
    if _BROWSER_PATH_CHECKED:
        return _BROWSER_PATH_CACHE
    try:
        # 尝试直接导入
        import browser_setup
        _BROWSER_PATH_CACHE = browser_setup.ensure_browser_available()
        _BROWSER_PATH_CHECKED = True
        return _BROWSER_PATH_CACHE
    except ImportError:
        # 如果直接导入失败，尝试从当前目录导入
        try:
            from pathlib import Path
            current_dir = Path(__file__).parent
            browser_setup_path = current_dir / "browser_setup.py"
            if browser_setup_path.exists():
                import sys
                sys.path.insert(0, str(current_dir))
                import browser_setup
                _BROWSER_PATH_CACHE = browser_setup.ensure_browser_available()
                _BROWSER_PATH_CHECKED = True
                return _BROWSER_PATH_CACHE
        except Exception:
            # Fallback: simple .env parser
            try:
                from pathlib import Path as _Path
                candidate = _Path(__file__).parent / ".env"
                if candidate.exists():
                    for _line in candidate.read_text().splitlines():
                        _line = _line.strip()
                        if not _line or _line.startswith('#') or '=' not in _line:
                            continue
                        _k, _v = _line.split('=', 1)
                        _k = _k.strip()
                        _v = _v.strip().strip('"').strip("'")
                        os.environ.setdefault(_k, _v)
            except Exception:
                logging.getLogger(__name__).debug("swallowed exception", exc_info=True)
        
        # 如果都失败了，返回None使用默认设置
        log("未找到browser_setup模块，将使用默认Playwright浏览器", "WARNING")
        _BROWSER_PATH_CHECKED = True
        _BROWSER_PATH_CACHE = None
        return None

def _resolve_proxy_url():
    """论坛通道的代理地址；WQB_FORUM_BYPASS_PROXY=1 时强制直连（返回 None）。

    2026-11-07：代理关掉后 HTTP(S)_PROXY 仍指向死端口（127.0.0.1:7897），
    这里是一条 or 链，用「设空字符串」绕不过去 —— 必须先判 bypass 开关。
    由 world-quant-brain-mcp/proxy_mode.py 的 mode=off 置位。
    """
    if (os.getenv("WQB_FORUM_BYPASS_PROXY") or "").strip().lower() in ("1", "true", "yes", "on"):
        return None
    return (os.getenv("FORUM_SETTINGS_PROXY") or os.getenv("HTTPS_PROXY")
            or os.getenv("https_proxy") or os.getenv("HTTP_PROXY")
            or os.getenv("http_proxy")) or None

# --- Parsing Helper Functions (from playwright_forum_test.py) ---

def _is_navigation_or_metadata(line: str) -> bool:
    """Check if a line is navigation or metadata."""
    navigation_patterns = [
        r'^\d+ days? ago$',
        r'~\d+ minute read',
        r'^Follow',
        r'^Not yet followed',
        r'^Updated$',
        r'^AS\d+$',
        r'^[A-Z] - [A-Z] - [A-Z]',  # Letter navigation
        r'^A$',
        r'^B$',
        r'^[A-Z]$'  # Single letters
    ]
    return any(re.match(pattern, line.strip()) for pattern in navigation_patterns)

def _looks_like_term(line: str) -> bool:
    """Check if a line looks like a glossary term."""
    if len(line) > 100:
        return False
    if _is_navigation_or_metadata(line):
        return False
    definition_starters = ['the', 'a', 'an', 'this', 'that', 'it', 'is', 'are', 'was', 'were', 'for', 'to', 'in', 'on', 'at', 'by', 'with']
    first_word = line.lower().split(' ')[0] if line else ''
    if first_word and first_word in definition_starters:
        return False
    is_short = len(line) <= 80
    starts_with_capital = bool(re.match(r'^[A-Z]', line))
    has_all_caps = bool(re.match(r'^[A-Z\s\-\/\(\)]+$', line))
    has_reasonable_length = len(line) >= 2
    return is_short and has_reasonable_length and (starts_with_capital or has_all_caps)

def _parse_glossary_terms(content: str) -> List[Dict[str, str]]:
    """Parse glossary terms from HTML content."""
    soup = BeautifulSoup(content, 'html.parser')
    # Get text from the article body, which is more reliable than splitting the whole HTML
    article_body = soup.select_one('.article-body')
    if not article_body:
        return []
    
    # Use .get_text with a separator to preserve line breaks, which is key for the logic below
    lines = article_body.get_text(separator='\n').split('\n')
    
    terms = []
    current_term = None
    current_definition = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if _looks_like_term(line):
            if current_term:
                # Save the previous term
                terms.append({
                    "term": current_term,
                    "definition": " ".join(current_definition).strip()
                })
            # Start a new term
            current_term = line
            current_definition = []
        elif current_term:
            # Add to the current definition
            current_definition.append(line)
            
    # Add the last term
    if current_term:
        terms.append({
            "term": current_term,
            "definition": " ".join(current_definition).strip()
        })
        
    # Filter out invalid terms and improve quality
    return [term for term in terms if 
            len(term["term"]) > 0 and 
            len(term["definition"]) > 10 and
            not _is_navigation_or_metadata(term["term"]) and
            "ago" not in term["definition"] and
            "minute read" not in term["definition"]]

class ForumClient:
    """Forum client for WorldQuant BRAIN support site, using Playwright."""
    
    @staticmethod
    def _needs_proactor() -> bool:
        """Check if current event loop supports subprocess creation on Windows."""
        try:
            import asyncio, sys
            if sys.platform != 'win32':
                return False
            loop = asyncio.get_event_loop()
            loop_name = loop.__class__.__name__
            # ProactorEventLoop supports subprocess; SelectorEventLoop does not
            return 'Proactor' not in loop_name
        except Exception:
            return False

    @staticmethod
    async def _run_in_proactor(coro):
        """Run a coroutine in a thread with ProactorEventLoop (supports subprocess on Windows).

        IMPORTANT: ``join()`` must never block the caller's event loop, otherwise the
        uvicorn loop cannot answer health probes (watchdog initialize has a 4s timeout)
        and the watchdog will taskkill the server mid-operation. Await the join via the
        default executor so the main loop stays responsive for the whole operation.
        """
        import asyncio, threading

        result = [None, None]  # [value, exception]

        def runner():
            try:
                loop = asyncio.ProactorEventLoop()
                asyncio.set_event_loop(loop)
                try:
                    result[0] = loop.run_until_complete(coro)
                finally:
                    loop.close()
            except Exception as e:
                result[1] = e

        t = threading.Thread(target=runner)
        t.start()
        await asyncio.get_running_loop().run_in_executor(None, t.join)
        if result[1]:
            raise result[1]
        return result[0]
    
    def __init__(self):
        # Load .env to allow overrides via environment
        try:
            from dotenv import load_dotenv, find_dotenv
            env_path = find_dotenv(usecwd=True)
            if env_path:
                load_dotenv(env_path, override=False)
            else:
                from pathlib import Path as _Path
                candidate = _Path(__file__).parent / ".env"
                if candidate.exists():
                    load_dotenv(candidate, override=False)
        except Exception:
            logging.getLogger(__name__).debug("swallowed exception", exc_info=True)

        self.base_url = os.getenv("FORUM_SETTINGS_BASE_URL", "https://support.worldquantbrain.com")
        # timeouts: seconds in env -> milliseconds for playwright waits
        try:
            self.selector_timeout_ms = int(float(os.getenv("FORUM_SETTINGS_TIMEOUT", "15")) * 1000)
        except Exception:
            self.selector_timeout_ms = 15000
        # headless setting
        self.headless = str(os.getenv("FORUM_SETTINGS_HEADLESS", "true")).lower() in ("1","true","yes","on")
        try:
            self.max_concurrency = max(1, int(os.getenv("FORUM_MAX_CONCURRENCY", "1")))
        except Exception:
            self.max_concurrency = 1
        # 并发闸门**不能**在这里建：asyncio.Semaphore 会绑定到「首次使用时正在运行的事件循环」。
        # 本类的协程在 Windows 上通常由 _run_in_proactor() 放到**新线程的新 ProactorEventLoop**
        # 里执行（主循环是 SelectorEventLoop，无法 spawn 子进程），与主循环不是同一个 loop，
        # 共享同一个 Semaphore 会在 `async with` 里抛
        #   RuntimeError('<asyncio.locks.Semaphore ...> is bound to a different event loop')
        # 且首次异常后 _value 已被扣到 0 却不归还，闸门永久卡死（表现 locked, waiters:1），
        # 必须重启进程才能复位。故改为按事件循环惰性建，用 WeakKeyDictionary 缓存，
        # 循环 close()+gc 后自动释放，无泄漏（2026-10-26 实测修复）。
        self._forum_sem_by_loop: "weakref.WeakKeyDictionary" = weakref.WeakKeyDictionary()
        # The session is mainly used for the initial authentication via brain_client
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        })

    def _get_post_api_url(self, post_id: str) -> str:
        return f"{self.base_url}/api/v2/community/posts/{post_id}.json?include=users"

    def _get_comments_api_url(self, post_id: str, page: int) -> str:
        return f"{self.base_url}/api/v2/community/posts/{post_id}/comments.json?page={page}&include=users"

    def _get_posts_list_url(self, page: int, per_page: int, sort_by: str, sort_order: str) -> str:
        """Zendesk Community **列表**端点（确定性；实测 count=11296 / page_count=113）。

        与 `/search` 抓取路径的根本区别：这是纯 JSON API，不经 Playwright，
        不受 Cloudflare 挑战页影响，且列表项自带 details 正文 / vote_sum / comment_count，
        因此「检索」可以退化为「拉语料 + 本地过滤」，既确定又不误判。
        """
        return (f"{self.base_url}/api/v2/community/posts.json"
                f"?per_page={per_page}&page={page}&sort_by={sort_by}&sort_order={sort_order}")

    async def list_forum_posts(self, email: str, password: str, page: int = 1,
                                per_page: int = 100, sort_by: str = "created_at",
                                sort_order: str = "desc") -> Dict[str, Any]:
        """列出论坛帖子（确定性 JSON API）。"""
        try:
            async with self._forum_sem():
                session = await self._ensure_support_session(email, password, locale="en-us")
                payload = await self._get_support_json(
                    session, self._get_posts_list_url(page, per_page, sort_by, sort_order))
                posts = payload.get("posts") or []
                out = []
                for p in posts:
                    out.append({
                        "id": p.get("id"),
                        "title": p.get("title"),
                        "votes": p.get("vote_sum") or 0,
                        "comments": p.get("comment_count") or 0,
                        "created_at": p.get("created_at"),
                        "url": p.get("html_url") or p.get("url"),
                        "body": _html_to_text(p.get("details") or "")[:1200],
                    })
                return {
                    "success": True,
                    "count": payload.get("count"),
                    "page_count": payload.get("page_count"),
                    "page": payload.get("page", page),
                    "returned": len(out),
                    "results": out,
                }
        except Exception as e:
            log(f"Failed to list forum posts: {str(e)}", "ERROR")
            return {"success": False, "results": [], "error": str(e)}

    async def search_forum_posts_local(self, email: str, password: str,
                                       keywords: List[str], limit: int = 5,
                                       max_pages: int = 8) -> Dict[str, Any]:
        """确定性论坛检索：拉语料 + 本地关键词过滤（不走 Playwright 抓取）。

        2026-11-20：旧 Playwright 搜索已按用户裁定**整体退役**（对任何查询都倾向返回
        0 结果或超时，「0 结果」是假信号）。本方法是论坛检索的唯一通道：
        用 Zendesk 列表端点拉语料后本地过滤，同一批关键词稳定命中
        （earnings / sharpe / turnover / correlation / crowding / sentiment / PEAD 均数十～数百条）。
        """
        try:
            async with self._forum_sem():
                session = await self._ensure_support_session(email, password, locale="en-us")
                kws = [str(k).strip().lower() for k in (keywords or []) if str(k).strip()]
                hits = []
                scanned = 0
                for page in range(1, max(1, int(max_pages)) + 1):
                    payload = await self._get_support_json(
                        session, self._get_posts_list_url(page, 100, "created_at", "desc"))
                    posts = payload.get("posts") or []
                    if not posts:
                        break
                    for p in posts:
                        scanned += 1
                        title = (p.get("title") or "").lower()
                        body = _html_to_text(p.get("details") or "").lower()
                        score, matched = 0.0, []
                        for kw in kws:
                            r_title = _kw_hit_ratio(title, kw)
                            r_body = _kw_hit_ratio(body, kw)
                            if r_title <= 0 and r_body <= 0:
                                continue
                            score += 3.0 * r_title + 1.0 * r_body
                            if max(r_title, r_body) >= 0.5:
                                matched.append(kw)
                        if score:
                            hits.append({
                                "id": p.get("id"),
                                "title": p.get("title"),
                                "votes": p.get("vote_sum") or 0,
                                "comments": p.get("comment_count") or 0,
                                "created_at": p.get("created_at"),
                                "url": p.get("html_url") or p.get("url"),
                                "body": _html_to_text(p.get("details") or "")[:1200],
                                "match_score": score,
                                "matched": matched,
                            })
                    if len(hits) >= max(1, int(limit)) * 4:
                        break
                hits.sort(key=lambda x: (-x["match_score"], -x["votes"], x["title"] or ""))
                return {
                    "success": True,
                    "keywords": kws,
                    "scanned": scanned,
                    "total_matched": len(hits),
                    "returned": min(len(hits), max(1, int(limit))),
                    "results": hits[:max(1, int(limit))],
                    "search_reliable": True,
                    "channel": "zendesk-community-list+local-filter",
                }
        except Exception as e:
            log(f"Failed to search forum posts locally: {str(e)}", "ERROR")
            return {"success": False, "results": [], "error": str(e)}

    @staticmethod
    def _forum_proxies():
        """代理映射：仅用于论坛（Zendesk）流量，BRAIN API 调用保持直连。"""
        proxy_url = _resolve_proxy_url()
        if not proxy_url:
            return None
        return {"http": proxy_url, "https": proxy_url}

    def _forum_sem(self) -> "asyncio.Semaphore":
        """取「当前事件循环」对应的并发闸门（不存在则新建）。

        每个事件循环各持一把 Semaphore，从根上避免跨循环绑定报错。
        用 WeakKeyDictionary 缓存：_run_in_proactor() 每次调用都新建线程+循环，
        循环关闭并 GC 后条目自动消失，不会随调用次数累积。
        """
        loop = asyncio.get_running_loop()
        sem = self._forum_sem_by_loop.get(loop)
        if sem is None:
            sem = asyncio.Semaphore(self.max_concurrency)
            self._forum_sem_by_loop[loop] = sem
        return sem

    async def _ensure_support_session(self, email: str, password: str, locale: str = "zh-cn", timeout_seconds: int = 30):
        """Establish a Zendesk support session using the authenticated BRAIN session."""
        try:
            from brain_api import brain_client
        except ImportError:
            import sys
            from pathlib import Path
            current_dir = Path(__file__).parent
            sys.path.insert(0, str(current_dir))
            from brain_api import brain_client

        try:
            await asyncio.wait_for(brain_client.ensure_authenticated(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            log(f"Authentication check timed out after {timeout_seconds}s, proceeding anyway.", "WARNING")
        except Exception:
            log("Authenticating with BRAIN platform...", "INFO")
            auth_result = await asyncio.wait_for(
                brain_client.authenticate(email, password),
                timeout=timeout_seconds
            )
            if auth_result.get('status') != 'authenticated':
                raise Exception("BRAIN platform authentication failed.")

        access_url = (
            "https://worldquantbrain.zendesk.com/access"
            f"?brand_id=1500000894061&locale={locale}"
            f"&return_to={self.base_url}/hc/{locale}"
        )

        def establish_session():
            return brain_client.session.get(
                access_url,
                timeout=timeout_seconds,
                allow_redirects=True,
                proxies=self._forum_proxies(),
                headers={
                    'User-Agent': self.session.headers['User-Agent'],
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                },
            )

        response = await asyncio.to_thread(establish_session)
        log(
            f"Support SSO handshake completed with status={response.status_code}, final_url={response.url}",
            "INFO"
        )
        return brain_client.session

    async def _get_support_json(self, session: requests.Session, url: str, timeout_seconds: int = 30) -> Dict[str, Any]:
        """Fetch forum JSON using the Zendesk-authenticated session."""
        def do_request():
            response = session.get(
                url,
                timeout=timeout_seconds,
                proxies=self._forum_proxies(),
                headers={
                    'User-Agent': self.session.headers['User-Agent'],
                    'Accept': 'application/json',
                },
            )
            response.raise_for_status()
            return response.json()

        return await asyncio.to_thread(do_request)

    async def _get_browser_context(self, p: Any, email: str, password: str, timeout_seconds: int = 30):
        """Authenticate and return a browser context with the session."""
        # Import brain_client here to avoid circular dependency
        try:
            from brain_api import brain_client
        except ImportError:
            # 尝试从当前目录导入
            import sys
            from pathlib import Path
            current_dir = Path(__file__).parent
            sys.path.insert(0, str(current_dir))
            from brain_api import brain_client
        
        # Avoid re-authenticating on every forum call: authenticate clears cookies and can
        # disrupt other concurrent tools using the same session.
        try:
            await asyncio.wait_for(brain_client.ensure_authenticated(), timeout=timeout_seconds)
        except asyncio.TimeoutError:
            log(f"Authentication check timed out after {timeout_seconds}s, proceeding anyway.", "WARNING")
        except Exception:
            log("Authenticating with BRAIN platform...", "INFO")
            try:
                auth_result = await asyncio.wait_for(
                    brain_client.authenticate(email, password),
                    timeout=timeout_seconds
                )
                if auth_result.get('status') != 'authenticated':
                    raise Exception("BRAIN platform authentication failed.")
                log("Successfully authenticated with BRAIN platform.", "SUCCESS")
            except asyncio.TimeoutError:
                log(f"Authentication timed out after {timeout_seconds}s, continuing with partial session.", "WARNING")

        # 论坛（Zendesk）是独立 SSO 域：仅带 BRAIN API cookie 会被重定向到
        # platform.worldquantbrain.com/sign-in。先完成 Zendesk SSO 握手，
        # 让 brain_client.session 持有 support/zendesk 域 cookie，再注入浏览器。
        try:
            await self._ensure_support_session(email, password, timeout_seconds=timeout_seconds)
            log("Zendesk 支持会话已建立（SSO）", "SUCCESS")
        except Exception as e:
            log(f"Zendesk SSO 会话建立失败，将沿用现有 cookie: {str(e)[:200]}", "WARNING")

        # 获取可用的浏览器路径
        browser_path = get_browser_path()
        
        # 设置浏览器启动参数 - 增强稳定性
        browser_args = [
            '--headless=new',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-background-networking',
            '--disable-sync',
            '--no-first-run'
        ]

        # 可选代理：support.worldquantbrain.com（Zendesk）在部分网络下需代理才能访问。
        # Playwright 启动的 Chromium 不会自动走系统代理，故显式支持：
        #   FORUM_SETTINGS_PROXY=http://127.0.0.1:7897
        # 未设置任何代理变量时行为不变。
        proxy_url = _resolve_proxy_url()
        launch_kwargs = {}
        if proxy_url:
            launch_kwargs["proxy"] = {"server": proxy_url}
            log(f"论坛浏览器使用代理: {proxy_url}", "INFO")
        
        try:
            if browser_path and os.path.exists(browser_path):
                log(f"使用自定义浏览器路径: {browser_path}", "INFO")
                browser = await asyncio.wait_for(
                    p.chromium.launch(executable_path=browser_path, args=browser_args, timeout=timeout_seconds * 1000, **launch_kwargs),
                    timeout=timeout_seconds + 10
                )
            else:
                log("使用默认Playwright浏览器", "INFO")
                browser = await asyncio.wait_for(
                    p.chromium.launch(headless=self.headless, args=browser_args, timeout=timeout_seconds * 1000, **launch_kwargs),
                    timeout=timeout_seconds + 10
                )
        except asyncio.TimeoutError:
            raise Exception(f"Browser launch timed out after {timeout_seconds + 10}s")
            
        try:
            context = await asyncio.wait_for(
                browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            await browser.close()
            raise Exception("Browser context creation timed out")

        log("Transferring authentication session to browser...", "INFO")
        try:
            cookies = brain_client.session.cookies
            playwright_cookies = []
            for cookie in cookies:
                cookie_dict = {
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain if cookie.domain else '.worldquantbrain.com',
                    'path': cookie.path if cookie.path else '/',
                    'secure': cookie.secure if hasattr(cookie, 'secure') else True,
                    'httpOnly': 'HttpOnly' in cookie._rest if hasattr(cookie, '_rest') else False,
                    'sameSite': 'Lax'
                }
                if hasattr(cookie, 'expires') and cookie.expires:
                    cookie_dict['expires'] = cookie.expires
                playwright_cookies.append(cookie_dict)
            
            await asyncio.wait_for(context.add_cookies(playwright_cookies), timeout=10)
            log("Session transferred.", "SUCCESS")
        except Exception as e:
            log(f"Cookie transfer warning (continuing): {str(e)}", "WARNING")
        
        return browser, context

    async def get_glossary_terms(self, email: str, password: str) -> List[Dict[str, str]]:
        """Extract glossary terms from the forum using Playwright."""
        if async_playwright is None:
            raise ImportError("Playwright not available. Please install it with: pip install playwright")

        if self._needs_proactor():
            return await self._run_in_proactor(self._get_glossary_terms_impl(email, password))
        return await self._get_glossary_terms_impl(email, password)

    async def _get_glossary_terms_impl(self, email: str, password: str) -> List[Dict[str, str]]:
        """Glossary implementation (assumes ProactorEventLoop-compatible context)."""

        async with self._forum_sem():
            async with async_playwright() as p:
                browser = None
                try:
                    log("Starting glossary extraction process with Playwright", "INFO")
                    browser, context = await self._get_browser_context(p, email, password)
                    
                    page = await context.new_page()
                    log("Navigating to BRAIN support forum glossary...", "INFO")
                    await page.goto("https://support.worldquantbrain.com/hc/en-us/articles/4902349883927-Click-here-for-a-list-of-terms-and-their-definitions")
                    
                    log("Extracting glossary content...", "INFO")
                    content = await page.content()
                    
                    terms = _parse_glossary_terms(content)
                    
                    log(f"Extracted {len(terms)} glossary terms", "SUCCESS")
                    return terms

                except Exception as e:
                    log(f"Glossary extraction failed: {str(e)}", "ERROR")
                    # Re-raise to be handled by the MCP server wrapper
                    raise
                finally:
                    if browser:
                        await browser.close()
                        log("Browser closed.", "INFO")

    async def read_full_forum_post(self, email: str, password: str, post_url_or_id: str, include_comments: bool = True) -> Dict[str, Any]:
        """Read a complete forum post and its comments via Zendesk JSON API."""
        try:
            async with self._forum_sem():
                log("Starting forum post reading process via Zendesk API", "INFO")

                post_id = _extract_post_id(post_url_or_id)
                locale = _extract_locale(post_url_or_id)
                session = await self._ensure_support_session(email, password, locale=locale)

                post_payload = await self._get_support_json(session, self._get_post_api_url(post_id))
                post_record = post_payload.get('post') or {}
                user_map = {
                    user.get('id'): user.get('name')
                    for user in post_payload.get('users', [])
                    if isinstance(user, dict)
                }

                post_data = {
                    'title': post_record.get('title', 'Unknown Title'),
                    'author': user_map.get(post_record.get('author_id'), 'Unknown Author'),
                    'body': _html_to_text(post_record.get('details', '')) or 'Body not found',
                    'details': {
                        'votes': str(post_record.get('vote_sum', 0)),
                        'date': post_record.get('created_at', 'Unknown Date') or 'Unknown Date',
                        'url': post_record.get('html_url') or post_record.get('url')
                    }
                }

                comments: List[Dict[str, Any]] = []
                if include_comments:
                    page_num = 1
                    while True:
                        comments_payload = await self._get_support_json(
                            session,
                            self._get_comments_api_url(post_id, page_num)
                        )
                        comment_records = comments_payload.get('comments') or []
                        if not comment_records:
                            break

                        users = comments_payload.get('users') or []
                        user_map.update({
                            user.get('id'): user.get('name')
                            for user in users
                            if isinstance(user, dict)
                        })

                        for comment_record in comment_records:
                            comment_data = {
                                'author': user_map.get(comment_record.get('author_id'), 'Unknown'),
                                'body': _html_to_text(comment_record.get('body', '')),
                                'date': comment_record.get('created_at', 'Unknown Date') or 'Unknown Date'
                            }
                            comments.append(comment_data)

                        if not comments_payload.get('next_page'):
                            break
                        page_num += 1

                log(f"Extracted {len(comments)} comments in total.", "SUCCESS")
                return {
                    'success': True,
                    'post': post_data,
                    'comments': comments,
                    'total_comments': len(comments)
                }

        except Exception as e:
            log(f"Failed to read forum post: {str(e)}", "ERROR")
            raise

# Initialize forum client
forum_client = ForumClient()

# The main block is for testing and won't be run by the MCP server.
if __name__ == "__main__":
    print("📚 WorldQuant BRAIN Forum Functions - This script provides the ForumClient class.", file=sys.stderr)
    # Basic local smoke test if credentials are set via env.
    email = os.getenv("CREDENTIALS_EMAIL")
    password = os.getenv("CREDENTIALS_PASSWORD")
    if email and password:
        # Example article id; adjust if needed
        article_id = "36371597455127-示例文章"
        try:
            result = asyncio.run(forum_client.read_full_forum_post(email, password, article_id))
            print(result)
        except Exception as e:
            log(f"Local test failed: {e}", "ERROR")
    else:
        log("Set CREDENTIALS_EMAIL and CREDENTIALS_PASSWORD in environment to run local test.", "INFO")