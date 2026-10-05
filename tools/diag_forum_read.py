# -*- coding: utf-8 -*-
"""forum_recon 读帖链路最小诊断（只读、零回测配额）。

分步打印每一跳的真实 HTTP 状态，定位「搜到 N 条但读帖全失败」的根因：
  1) 凭据加载    2) BRAIN auth    3) SSO handshake
  4) 搜索（control probe）  5) 逐帖 read_post（含原始 status / body 片段）

用法：
    <WQ_PY> -u tools/diag_forum_read.py [--probe-n 3]
退出码：0 = 至少读到 1 帖正文；3 = 全部读帖失败（即 read_failed 复现）；4 = 更上游故障。
"""
from __future__ import annotations

import argparse
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

try:
    import forum_research as fr
    import forum_recon
    import requests
except ImportError as e:
    print(f"[diag] 缺依赖：{e} —— 请用 MCP venv 解释器（$WQ_PY）运行", file=sys.stderr)
    sys.exit(4)

CONTROL_QUERY = fr.CONTROL_QUERY if hasattr(fr, "CONTROL_QUERY") else "alpha"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe-n", type=int, default=3, help="最多实测读几帖")
    ap.add_argument("--query", default=CONTROL_QUERY)
    args = ap.parse_args()

    # 1) 凭据
    email = os.environ.get("CREDENTIALS_EMAIL")
    password = os.environ.get("CREDENTIALS_PASSWORD")
    if not (email and password):
        env_path = os.path.join(REPO_ROOT, "world-quant-brain-mcp", ".env")
        creds = fr.load_creds(env_path)
        email = email or creds.get("CREDENTIALS_EMAIL")
        password = password or creds.get("CREDENTIALS_PASSWORD")
    print(f"[1] creds: email={'set' if email else 'MISSING'} pw={'set' if password else 'MISSING'}")
    if not (email and password):
        print("[diag] 凭据缺失，无从诊断", file=sys.stderr)
        return 4

    s = requests.Session()
    s.headers.update({"User-Agent": fr.UA})

    # 2) BRAIN auth
    try:
        fr.authenticate(s, email, password)
        print(f"[2] BRAIN auth: OK (cookie t={'yes' if s.cookies.get('t') else 'no'})")
    except Exception as e:
        print(f"[2] BRAIN auth FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        return 4

    # 3) SSO
    try:
        fr.sso_handshake(s)
        print("[3] SSO handshake: OK")
    except Exception as e:
        print(f"[3] SSO handshake FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        return 4

    # 4) 搜索
    try:
        hits = fr.search_html(s, args.query, max_pages=1) or []
    except Exception as e:
        print(f"[4] search FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        return 4
    print(f"[4] search {args.query!r}: {len(hits)} hits")
    if not hits:
        print("[diag] 对照检索 0 结果 —— 检索通道失效（会话/被拦/改版）", file=sys.stderr)
        return 4
    for h in hits[:5]:
        print(f"      hit: id={h.get('post_id') or h.get('id')} click_href={str(h.get('click_href'))[:60]}")

    # 5) 逐帖 read_post（含原始 HTTP 状态，绕开 get_with_retry 的静默 None）
    ok = 0
    for hit in hits[: args.probe_n]:
        pid = hit.get("post_id") or hit.get("id")
        if not pid and hit.get("click_href"):
            # 走修复后的适配层（forum_recon._resolve_post_id），而非裸 resolve_id
            pid = forum_recon._resolve_post_id(s, fr, hit["click_href"])
            print(f"      _resolve_post_id -> {pid!r}")
        if not pid:
            print("      [skip] 取不到 post_id（非社区帖或解析失败）")
            continue

        url = f"{fr.API}/community/posts/{pid}.json?include=users"
        try:
            raw = s.get(url, headers=fr.JSON_HEADERS, timeout=60, allow_redirects=True)
            status = raw.status_code
            ctype = raw.headers.get("Content-Type", "")
            snippet = (raw.text or "")[:180].replace("\n", " ")
        except Exception as e:
            print(f"[5] pid={pid} 请求异常: {type(e).__name__}: {e}")
            continue
        print(f"[5] pid={pid} -> HTTP {status} ct={ctype}")
        print(f"       body[:180] = {snippet}")
        if status != 200:
            continue
        try:
            post = fr.read_post(s, pid) or {}
        except Exception as e:
            print(f"       read_post 抛异常: {type(e).__name__}: {e}")
            continue
        if post:
            ok += 1
            print(f"       read_post OK: title={str(post.get('title'))[:50]} body_len={len(post.get('body') or '')}")
        else:
            print("       read_post 返回空（200 但解析为空）")

    print(f"\n[结论] 读到正文 {ok}/{min(len(hits), args.probe_n)} 帖")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
