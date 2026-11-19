#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论坛 MCP 读帖链路最小诊断（只读、零回测配额；2026-11-18 改 MCP 唯一入口）。

查论坛唯一方式 = `docs/reference/forum_and_doc_tools_guide.md` 的 `wq-brain-http` MCP 工具
（单一实现 `tools/lib/forum_mcp.py`）。本诊断分步打印每一跳，定位「搜到 N 条但读帖全失败」的根因：
  1) MCP 客户端构造（.mcp.json 解析 / 服务可达）
  2) search_forum_posts（control probe）
  3) 从 results[].link 提取 post_id
  4) 逐帖 read_forum_post（含 success / error / body 片段）

⚠ search 超时/失败是**工具故障**（guide §2.2 传输层错配），不是「论坛无解」；本诊断只报状态，不落负结果。

用法：
    <WQ_PY> -u tools/diag_forum_read.py [--probe-n 3] [--query alpha]
退出码：0 = 至少读到 1 帖正文；3 = 全部读帖失败（read_failed 复现）；4 = 更上游故障（客户端/搜索）。
"""
from __future__ import annotations

import argparse
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

try:
    from lib import forum_mcp as FM
except ImportError as e:
    print(f"[diag] 缺依赖：{e} —— 请用 MCP venv 解释器（$WQ_PY）运行", file=sys.stderr)
    sys.exit(4)

CONTROL_QUERY = "alpha"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe-n", type=int, default=3, help="最多实测读几帖")
    ap.add_argument("--query", default=CONTROL_QUERY)
    args = ap.parse_args()

    # 1) MCP 客户端（凭据由服务端读取，客户端不碰口令）
    try:
        cli = FM.client()
        print(f"[1] MCP client: OK (uri={cli.uri})")
    except (Exception, SystemExit) as e:
        print(f"[1] MCP client FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        print("    服务没起？先 python tools/start_wq_mcp.py --all；地址以 .mcp.json 为准", file=sys.stderr)
        return 4

    # 2) 搜索（control probe）
    try:
        res = FM.search_posts(cli, args.query, max_results=max(args.probe_n, 5))
    except Exception as e:
        print(f"[2] search FAILED: {type(e).__name__}: {e}", file=sys.stderr)
        return 4
    if FM.is_error(res):
        print(f"[2] search {args.query!r} 故障：{res.get('error') or 'success=False'}", file=sys.stderr)
        print("    工具故障 ≠ 论坛无解（guide §2.2）；可试文档两步绕行 get_documentations→get_documentation_page", file=sys.stderr)
        return 4
    hits = FM.search_results(res)
    print(f"[2] search {args.query!r}: {len(hits)} hits")
    if not hits:
        print("[diag] 对照检索 0 结果 —— 检索通道失效（会话/被拦/服务不可达）", file=sys.stderr)
        return 4
    for h in hits[:5]:
        print(f"      hit: id={FM.post_id_from_link(h.get('link'))} title={str(h.get('title'))[:40]}")

    # 3)+4) 逐帖 read_forum_post
    ok = 0
    for hit in hits[: args.probe_n]:
        pid = hit.get("post_id") or FM.post_id_from_link(hit.get("link"))
        if not pid:
            print("      [skip] 取不到 post_id（link 无 /posts/<数字>）")
            continue
        try:
            pres = FM.read_post(cli, pid)
        except Exception as e:
            print(f"[4] pid={pid} read 异常: {type(e).__name__}: {e}")
            continue
        if FM.is_error(pres):
            print(f"[4] pid={pid} -> error: {str(pres.get('error') or 'success=False')[:160]}")
            continue
        body = FM.post_body(pres)
        print(f"[4] pid={pid} -> OK title={FM.post_title(pres)[:50]} body_len={len(body)}")
        print(f"       body[:180] = {body[:180].replace(chr(10), ' ')}")
        if body:
            ok += 1

    print(f"\n[结论] 读到正文 {ok}/{min(len(hits), args.probe_n)} 帖")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
