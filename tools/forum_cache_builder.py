"""Forum post cache builder for brain-alpha-robustness Phase A.

构建/刷新论坛帖缓存，避免每次会话重复拉取 ≥30 篇论坛帖。
缓存策略：TTL 7 天 + 按关键词包分组 + 投票数加权排序。

用法（MCP venv）：
    $WQ_PY tools/forum_cache_builder.py --refresh          # 全量刷新
    $WQ_PY tools/forum_cache_builder.py --status           # 查看缓存状态
    $WQ_PY tools/forum_cache_builder.py --ensure           # 过期才刷新（默认）
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# 缓存位置：skill 目录下，随 skill 分发
SKILL_DIR = Path.home() / ".qoder-cn" / "skills" / "brain-alpha-robustness"
CACHE_FILE = SKILL_DIR / "data" / "forum_cache.json"
TTL_DAYS = 7

# Phase A 规定的 5 个关键词包（与 SKILL.md 一致）
KEYWORD_BUNDLES = [
    {"query": "过拟合 overfitting alpha", "limit": 20},
    {"query": "归因分析 yearly stats alpha sharpe", "limit": 20},
    {"query": "sub-universe 参数敏感 稳健性测试", "limit": 15},
    {"query": "robust test 年度 sharpe decay ratio", "limit": 15},
    {"query": "performance_comparison 厂字形 股票集中", "limit": 10},
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _cache_age_days(cache: dict) -> float:
    built = cache.get("built_at")
    if not built:
        return float("inf")
    try:
        dt = datetime.fromisoformat(built)
        return (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
    except Exception:
        return float("inf")


def load_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def cache_status() -> dict:
    cache = load_cache()
    if not cache:
        return {"status": "empty", "age_days": None, "posts": 0}
    age = _cache_age_days(cache)
    posts = len(cache.get("posts", {}))
    return {
        "status": "fresh" if age < TTL_DAYS else "stale",
        "age_days": round(age, 1),
        "posts": posts,
        "built_at": cache.get("built_at"),
        "bundles": {b["query"]: len(b.get("post_ids", [])) for b in cache.get("bundles", [])},
    }


def build_cache_via_mcp() -> dict:
    """通过 MCP 拉取论坛帖构建缓存。需在 Agent 会话中调用 MCP 工具。

    本函数生成一个 MCP 调用计划，由 Agent 执行后回填。
    直接独立运行时仅输出计划，不实际拉取。
    """
    plan = {
        "built_at": _now_iso(),
        "ttl_days": TTL_DAYS,
        "bundles": [],
        "posts": {},
    }
    for bundle in KEYWORD_BUNDLES:
        plan["bundles"].append({
            "query": bundle["query"],
            "limit": bundle["limit"],
            "post_ids": [],  # Agent 回填
        })
    return plan


def main() -> int:
    ap = argparse.ArgumentParser(description="Forum post cache builder for robustness Phase A")
    ap.add_argument("--refresh", action="store_true", help="强制全量刷新")
    ap.add_argument("--status", action="store_true", help="查看缓存状态")
    ap.add_argument("--ensure", action="store_true", help="过期才刷新（默认行为）")
    ap.add_argument("--plan", action="store_true", help="仅输出 MCP 拉取计划（JSON）")
    args = ap.parse_args()

    if args.status:
        st = cache_status()
        print(json.dumps(st, ensure_ascii=False, indent=2))
        return 0

    if args.plan or args.refresh:
        plan = build_cache_via_mcp()
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        if not args.plan:
            print("\n[提示] 这是 MCP 拉取计划。请在 Agent 会话中执行 Phase A 缓存填充，", file=sys.stderr)
            print("或运行 brain-alpha-robustness skill 让其自动使用缓存优先逻辑。", file=sys.stderr)
        return 0

    # 默认 ensure 行为
    st = cache_status()
    if st["status"] == "fresh":
        print(f"[缓存] 新鲜（{st['age_days']} 天前构建，{st['posts']} 篇），无需刷新。")
        return 0
    print(f"[缓存] {st['status']}，需要刷新。运行 --plan 查看拉取计划。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
