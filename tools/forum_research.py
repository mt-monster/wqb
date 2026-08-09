#!/usr/bin/env python3
"""
Direct WorldQuant BRAIN forum research (no Playwright), rate-limit aware.

Flow:
  1. BRAIN Basic-Auth -> JWT cookie 't'
  2. Zendesk support SSO handshake -> support cookies
  3. Scrape HTML search pages (/hc/{locale}/search?query=...) with delays + Referer
  4. Resolve post ids by following the Zendesk "search click" redirect
  5. Read full post + comments via the community JSON API
"""
import argparse
import base64
import html
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://support.worldquantbrain.com"
API = f"{BASE}/api/v2"
BRAIN_AUTH = "https://api.worldquantbrain.com/authentication"
SSO_ACCESS = (
    "https://worldquantbrain.zendesk.com/access"
    "?brand_id=1500000894061&locale=zh-cn"
    f"&return_to={BASE}/hc/zh-cn"
)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
HTML_HEADERS = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Referer": f"{BASE}/hc/zh-cn"}
JSON_HEADERS = {"User-Agent": UA, "Accept": "application/json"}


def log(m):
    print(m, file=sys.stderr, flush=True)


def load_creds(env_path):
    creds = {}
    if os.path.exists(env_path):
        for line in open(env_path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip().strip('"').strip("'")
    return creds


def html_to_text(h):
    if not h:
        return ""
    t = re.sub(r"<[^>]+>", "\n", h)
    t = html.unescape(t)
    return "\n".join(ln.strip() for ln in t.splitlines() if ln.strip())


def get_with_retry(session, url, headers, params=None, timeout=60, retries=3, delay=3.0):
    """GET with exponential backoff on 406/429/5xx/connection errors."""
    last = None
    for attempt in range(retries):
        try:
            r = session.get(url, params=params, headers=headers, timeout=timeout, allow_redirects=True)
            if r.status_code in (406, 429) or r.status_code >= 500:
                wait = delay * (attempt + 1) + 2
                log(f"    {r.status_code} on {url[:70]} -> retry in {wait:.0f}s")
                time.sleep(wait)
                last = r
                continue
            return r
        except Exception as e:
            wait = delay * (attempt + 1)
            log(f"    conn error {e} -> retry in {wait:.0f}s")
            time.sleep(wait)
            last = None
    return last


def authenticate(session, email, password, timeout=60):
    enc = base64.b64encode(f"{email}:{password}".encode()).decode()
    r = session.post(BRAIN_AUTH, headers={"Authorization": f"Basic {enc}", "User-Agent": UA}, timeout=timeout)
    if r.status_code != 201:
        raise RuntimeError(f"BRAIN auth failed: {r.status_code} {r.text[:200]}")
    return bool(session.cookies.get("t"))


def sso_handshake(session, timeout=60):
    r = session.get(SSO_ACCESS, headers=HTML_HEADERS, timeout=timeout, allow_redirects=True)
    return r.status_code


def search_html(session, query, locale="zh-cn", max_pages=2, page_delay=2.5):
    out = []
    for page in range(1, max_pages + 1):
        r = get_with_retry(session, f"{BASE}/hc/{locale}/search", HTML_HEADERS, params={"query": query, "page": page})
        if r is None or r.status_code == 404 or r.status_code != 200:
            log(f"  search '{query}' p{page} status {r.status_code if r else 'None'}")
            break
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.select("li.search-result-list-item")
        if not items:
            break
        for it in items:
            a = it.select_one("h2.search-result-title a") or it.select_one("h2 a")
            if not a:
                continue
            href = a.get("href", "")
            if href and not href.startswith("http"):
                href = BASE + href
            snippet_el = it.select_one(".search-results-description")
            snippet = snippet_el.get_text(" ", strip=True) if snippet_el else ""
            votes = 0
            ve = it.select_one('.search-result-votes span[aria-hidden="true"]')
            if ve:
                m = re.search(r"\d+", ve.get_text(strip=True))
                if m:
                    votes = int(m.group())
            comments = 0
            ce = it.select_one('.search-result-meta-count span[aria-hidden="true"]')
            if ce:
                m = re.search(r"\d+", ce.get_text(strip=True))
                if m:
                    comments = int(m.group())
            bc = [b.get_text(strip=True) for b in it.select("ol.search-result-breadcrumbs li")]
            author, date = "Unknown", "Unknown"
            meta = it.select("ul.meta-group li.meta-data")
            if meta:
                author = meta[0].get_text(strip=True)
                if len(meta) > 1:
                    t = meta[1].select_one("time")
                    if t:
                        date = t.get("datetime", t.get_text(strip=True))
            out.append({"title": a.get_text(strip=True), "click_href": href, "snippet": snippet,
                        "votes": votes, "comments": comments, "breadcrumbs": bc, "author": author,
                        "date": date, "query": query})
        time.sleep(page_delay)
    return out


def resolve_id(session, click_href, timeout=30):
    r = get_with_retry(session, click_href, HTML_HEADERS, timeout=timeout, retries=2, delay=4.0)
    if r is not None:
        m = re.search(r"/posts/(\d+)", r.url)
        if m:
            return m.group(1), ("/community/posts/" in r.url), r.url
    return None, False, None


def read_post(session, post_id, timeout=60):
    p = get_with_retry(session, f"{API}/community/posts/{post_id}.json?include=users", JSON_HEADERS, timeout=timeout, retries=2)
    if p is None or p.status_code != 200:
        return None
    pj = p.json()
    rec = pj.get("post", {})
    users = {u.get("id"): u.get("name") for u in pj.get("users", []) if isinstance(u, dict)}
    comments = []
    page = 1
    while True:
        cj = get_with_retry(session, f"{API}/community/posts/{post_id}/comments.json?page={page}&include=users", JSON_HEADERS, timeout=timeout, retries=2)
        if cj is None or cj.status_code != 200:
            break
        cdata = cj.json()
        for c in cdata.get("comments", []):
            comments.append({"author": users.get(c.get("author_id"), "Unknown"), "body": html_to_text(c.get("body", "")), "date": c.get("created_at")})
        if not cdata.get("next_page"):
            break
        page += 1
        if page > 25:
            break
        time.sleep(0.3)
    return {"id": post_id, "title": rec.get("title"), "author": users.get(rec.get("author_id"), "Unknown"),
            "body": html_to_text(rec.get("details", "")), "votes": rec.get("vote_sum", 0),
            "created_at": rec.get("created_at"), "url": rec.get("html_url") or rec.get("url"),
            "comments": comments, "comment_count": len(comments)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=None)
    ap.add_argument("--queries", default="GLB,全球因子,分区域权重,Power Pool,中性化,turnover,点塔,冷门数据集")
    ap.add_argument("--max-pages", type=int, default=2)
    ap.add_argument("--resolve-top", type=int, default=34)
    ap.add_argument("--read-top", type=int, default=22)
    ap.add_argument("--out", default="tracking/forum_glb_search.json")
    ap.add_argument("--posts-out", default="tracking/forum_glb_posts.json")
    args = ap.parse_args()

    env_path = args.env or str(Path(__file__).resolve().parent.parent / "world-quant-brain-mcp" / ".env")
    creds = load_creds(env_path)
    email = creds.get("CREDENTIALS_EMAIL")
    password = creds.get("CREDENTIALS_PASSWORD")
    if not email or not password:
        log("ERROR: missing credentials"); sys.exit(2)

    session = requests.Session()
    session.headers.update({"User-Agent": UA})
    log("Authenticating to BRAIN...")
    authenticate(session, email, password)
    log("SSO handshake...")
    st = sso_handshake(session)
    log(f"SSO status {st}")

    queries = [q.strip() for q in args.queries.split(",") if q.strip()]
    raw = []
    for q in queries:
        res = search_html(session, q, max_pages=args.max_pages)
        log(f"  query '{q}': {len(res)} raw results")
        raw.extend(res)
        time.sleep(2.0)

    seen = {}
    for r in raw:
        key = r["click_href"]
        if key not in seen:
            seen[key] = r
        else:
            if r["query"] not in (seen[key].get("queries") or []):
                seen[key].setdefault("queries", [seen[key]["query"]]).append(r["query"])
    results = list(seen.values())
    for r in results:
        r.setdefault("queries", [r.get("query")])
    results.sort(key=lambda x: (x.get("votes", 0) or 0) + (x.get("comments", 0) or 0), reverse=True)
    log(f"Unique results: {len(results)}")

    top = results[: args.resolve_top]
    resolved = []
    for r in top:
        pid, is_comm, url = resolve_id(session, r["click_href"])
        if pid and is_comm:
            r["id"] = pid
            r["url"] = url
            r["is_community"] = True
            resolved.append(r)
            log(f"  resolved {pid}: {r['title']}")
        else:
            r["is_community"] = False
        time.sleep(1.0)
    log(f"Resolved community posts: {len(resolved)}")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(results, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log(f"Saved {len(results)} search results -> {args.out}")

    to_read = resolved[: args.read_top]
    posts = []
    for r in to_read:
        post = read_post(session, r["id"])
        if post:
            post["query_hits"] = r.get("queries", [])
            post["snippet"] = r.get("snippet")
            posts.append(post)
            log(f"  read {r['id']}: {post['title']} ({post['comment_count']} comments)")
        else:
            log(f"  read {r['id']} failed")
        time.sleep(0.5)
    json.dump(posts, open(args.posts_out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    log(f"Saved {len(posts)} full posts -> {args.posts_out}")


if __name__ == "__main__":
    main()
