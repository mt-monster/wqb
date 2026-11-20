# -*- coding: utf-8 -*-
"""paper_search.py — 稳定的外部金融论文检索（唯一实现，三层冗余 + fail-closed）。

背景（2026-11-19 用户明令）：
  1) 项目中所有查论文的地方必须用「明确稳定可靠」的通道，不稳定的（WebSearch/WebFetch/
     Semantic Scholar 429）一律弃用；
  2) 证据闸（wave_gate 的 EVID-PAPER）不要「留痕就算过」，要「一定能查到论文」。

实测（2026-11-19，项目 venv）：
  - Crossref REST  : 稳定 1.2s，精确命中期刊论文（DOI/作者/年份）—— 主通道
  - arXiv API      : 稳定 1.3s，但纯金融词常返回空（偏物理/CS/量化预印本）—— 补量化/方法类
  - Semantic Scholar: 429 限流 —— 弃用
  - 本地论文库      : docs/reference + docs/experience（19+ 文件）—— 保底，必命中已知论文

三层冗余：crossref → arxiv → 本地库。任一层拿到真实论文即 found=true；
全部失败则 found=false + fail-closed（不编造、不拿"查不到"当通过）。

外发边界：只发通用检索词（经济机制/方法名），不发未公开表达式 / 数据集名 / 字段名 /
alpha id。凭据不需要（三个通道都匿名）。

用法：
  python tools/paper_search.py --query "divergence of opinion short selling" --json out.json
  python tools/paper_search.py --query "反转效应 中国股市" --limit 5
  from tools.paper_search import search_papers; r = search_papers("momentum crash")

退出码：0=found / 2=not found（fail-closed）/ 1=工具故障
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import Any, Dict, List

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_USER_AGENT = "WQB-Research/1.0 (mailto:research@worldquantbrain.local)"
_TIMEOUT = 15

# 本地保底论文库目录（相对仓库根）——这些文件已沉淀了带出处的经典金融论文锚
_LOCAL_CORPUS = [
    "docs/experience",
    "docs/reference",
    "Claude/skills/wq-brain-ra-pipeline/references",
]
# 只在这些"论文痕迹"行里匹配，避免命中普通文本
_LOCAL_PAPER_RE = re.compile(
    r"(Miller|Merton|Fama|French|Carhart|Jegadeesh|Titman|Piotroski|Novy-Marx|"
    r"Sharpe|Asness|Moskowitz|Pedersen|Barber|Odean|Tetlock|Gabaix|Koijen|"
    r"Bernard|Thomas|Price|Matsumoto|Doran|Peterson|Fisher|Statman|Ang|"
    r"Baker|Wurgler|Campbell|Cochrane|Hou|Xue|Zhang|Harvey|Liu|"
    r"divergence of opinion|short.sale|momentum|value premium|"
    r"PEAD|post.earnings|sentiment|overvaluation|arXiv|SSRN|DOI|"
    r"\d{4}\.\d{4,5})",
    re.IGNORECASE,
)


def _crossref(query: str, limit: int) -> List[Dict[str, Any]]:
    import requests
    # 作者+年份查询（闸从留痕 cite 抽的 'Lakonishok Lee 2001'）用 query.author + filter from-pub-date
    author_mode = bool(re.search(r"\b(19|20)\d{2}\b", query))
    params = {"rows": limit, "select": "title,author,published,DOI,container-title"}
    if author_mode:
        author = " ".join(t for t in query.split() if not t.isdigit())
        params["query.author"] = author
    else:
        params["query.title"] = query
    r = requests.get("https://api.crossref.org/works", params=params,
                     headers={"User-Agent": _USER_AGENT}, timeout=_TIMEOUT)
    r.raise_for_status()
    out = []
    for it in r.json().get("message", {}).get("items", []):
        title = (it.get("title") or [""])[0]
        authors = [f"{a.get('family','')} {a.get('given','')}".strip()
                   for a in (it.get("author") or [])[:4]]
        out.append({
            "title": title,
            "authors": authors,
            "year": _year(it.get("published")),
            "venue": (it.get("container-title") or [""])[0],
            "doi": it.get("DOI"),
            "source": "crossref",
        })
    return out


def _arxiv(query: str, limit: int) -> List[Dict[str, Any]]:
    import requests
    import xml.etree.ElementTree as ET
    r = requests.get(
        "https://export.arxiv.org/api/query",
        params={"search_query": f'all:"{query}"', "start": 0, "max_results": limit},
        headers={"User-Agent": _USER_AGENT}, timeout=_TIMEOUT,
    )
    r.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(r.text)
    out = []
    for e in root.findall("a:entry", ns):
        title = (e.findtext("a:title", "", ns) or "").strip()
        if not title:
            continue
        out.append({
            "title": title,
            "authors": [a.findtext("a:name", "", ns) for a in e.findall("a:author", ns)][:4],
            "year": (e.findtext("a:published", "", ns) or "")[:4],
            "venue": "arXiv",
            "doi": (e.findtext("a:id", "", ns) or "").strip(),
            "source": "arxiv",
        })
    return out


def _year(published: Any) -> str:
    try:
        return str(published["date-parts"][0][0])
    except Exception:
        return ""


def _local(query: str, limit: int) -> List[Dict[str, Any]]:
    """本地保底：在已沉淀的论文痕迹文件里按检索词命中行。
    ★必须与 query 实词重叠（不能只靠 _LOCAL_PAPER_RE 关键词表——那会让任何
    含 momentum 的行都命中无关查询，制造假阳性）。
    """
    stop = {"this", "that", "with", "from", "have", "effect", "study", "paper",
            "analysis", "based", "using", "evidence", "market", "markets",
            "股票", "股市", "基于", "研究", "影响", "效应"}
    tokens = [t.lower() for t in re.split(r"[\s，,、]+", query)
              if len(t) >= 4 and t.lower() not in stop]
    hits: List[Dict[str, Any]] = []
    for sub in _LOCAL_CORPUS:
        root = os.path.join(_REPO_ROOT, sub)
        if not os.path.isdir(root):
            continue
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                if not fn.endswith((".md", ".txt")):
                    continue
                path = os.path.join(dirpath, fn)
                try:
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f, 1):
                            if not _LOCAL_PAPER_RE.search(line):
                                continue
                            low = line.lower()
                            # 双重条件：行本身有论文痕迹 AND 含 query 实词
                            matched = sum(1 for t in tokens if t in low or (len(t) >= 5 and t[:5] in low))
                            if matched == 0:
                                continue
                            hits.append({
                                "title": line.strip()[:180],
                                "authors": [],
                                "year": "",
                                "venue": "local-corpus",
                                "doi": "",
                                "source": "local",
                                "path": os.path.relpath(path, _REPO_ROOT),
                                "line": i,
                                "matched_tokens": matched,
                            })
                except OSError:
                    continue
    hits.sort(key=lambda h: -h["matched_tokens"])
    return hits[:limit]


# 中文金融术语 → 英文检索词（Crossref 是英文库，中文查询零命中——2026-11-19 workflow
# 实测：中文 prompt 下模板员写中文 mechanism，paper_search found=false 误杀。此表在查询层自动扩容）。
_CN_EN = {
    "反转": "return reversal", "特质反转": "idiosyncratic return reversal",
    "动量": "momentum", "特质动量": "idiosyncratic momentum",
    "低贝塔": "low beta anomaly betting against beta", "贝塔": "beta anomaly",
    "低波动": "low volatility anomaly", "低波": "low volatility anomaly",
    "异象": "anomaly", "均值回复": "mean reversion",
    "特质收益": "idiosyncratic return residual return",
    "残差": "residual return", "流动性": "liquidity",
    "交易量": "trading volume", "波动率": "volatility",
    "价值": "value premium", "规模": "size premium",
    "应计": "accruals", "盈余": "earnings announcement drift",
    "分析师": "analyst revision", "情绪": "sentiment",
    "做空": "short selling constraints", "卖空": "short sale constraints",
    "拥挤": "crowding", "换手": "turnover",
    "截面": "cross section", "行业": "industry", "分组": "portfolio sort",
    "持有期": "holding period", "信息扩散": "information diffusion",
}


def _expand_cn(query: str) -> List[str]:
    """中文查询扩容为多个英文/中英查询；纯英文原样返回。"""
    if not re.search(r"[一-鿿]", query):
        return [query]
    en_terms: List[str] = []
    for cn, en in _CN_EN.items():
        if cn in query:
            en_terms.append(en)
    out = [query]
    if en_terms:
        # 去重保序，英文同义词合并成一个查询（Crossref 对多词查询 tolerant）
        seen = set()
        en_terms = [e for e in en_terms if not (e in seen or seen.add(e))]
        out.append(" ".join(en_terms[:6]))
    return out


def _relevance(query: str, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Crossref 对任何查询都返回「最接近」结果——必须校验与检索词有实质重叠。
    两种模式：
      - 作者+年份查询（如 'Lakonishok Lee 2001'）：核验 authors 或 year 命中
      - 机制词查询：核验 title 命中
    """
    stop = {"this", "that", "with", "from", "have", "effect", "study", "paper",
            "analysis", "based", "using", "evidence", "market", "markets",
            "股票", "股市", "基于", "研究", "影响", "效应"}
    tokens = [t.lower() for t in re.split(r"[\s，,、]+", query)
              if len(t) >= 3 and t.lower() not in stop]
    if not tokens:
        return []
    # 作者模式：查询含 4 位年份 ⇒ 用作者/年份核验（标题不含作者名）
    years = re.findall(r"\b(19|20)\d{2}\b", query)
    author_mode = bool(years)
    out = []
    for p in papers:
        title = (p.get("title") or "").lower()
        authors = " ".join(a.lower() for a in (p.get("authors") or []))
        if author_mode:
            # 作者姓氏（去年份）至少命中一个作者字段即算真查到
            surnames = [t for t in tokens if not t.isdigit() and len(t) >= 4]
            hit = sum(1 for s in surnames if s in authors)
            if hit >= 1:
                q = dict(p); q["relevance_hits"] = hit; out.append(q)
        else:
            # 机制模式：至少 1 个长实词(≥6)完整命中，或 2 个短实词同时命中。
            # 单个 3-5 字母泛词（xyz/institution）命中不算——Crossref 对任意查询都会返回含常见词的结果。
            long_hit = any(len(t) >= 6 and t in title for t in tokens)
            short_hits = sum(1 for t in tokens if 3 <= len(t) <= 5 and t in title)
            if long_hit or short_hits >= 2:
                q = dict(p); q["relevance_hits"] = int(long_hit) + short_hits; out.append(q)
    return out


def search_papers(query: str, limit: int = 5, layers: str = "crossref,arxiv,local") -> Dict[str, Any]:
    """三层冗余检索。返回 {found, papers, layers_tried, error}。

    found=true 只要任一层返回「与检索词相关」的论文（经 _relevance 校验）；
    全失败或只有无关结果 found=false（fail-closed）。
    """
    papers: List[Dict[str, Any]] = []
    tried: List[Dict[str, Any]] = []
    errors: List[str] = []
    # 中文查询自动扩容为「中文原词 + 英文同义词」，逐个检索后合并（KOR/GBR 中文 mechanism 场景）
    for sub_q in _expand_cn(query):
        _sub = _search_single(sub_q, limit, layers)
        papers.extend(_sub["papers"])
        tried.extend(_sub["layers_tried"])
        errors.extend(_sub.get("errors") or [])
        if _sub["found"]:
            break
    return {
        "query": query,
        "found": bool(papers),
        "papers": _dedup(papers)[:limit],
        "layers_tried": tried,
        "errors": errors,
    }


def _dedup(papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for p in papers:
        k = _identity(p)
        if k not in seen:
            seen.add(k)
            out.append(p)
    return out


def _search_single(query: str, limit: int, layers: str) -> Dict[str, Any]:
    papers: List[Dict[str, Any]] = []
    tried: List[Dict[str, Any]] = []
    errors: List[str] = []
    for layer in layers.split(","):
        layer = layer.strip()
        fn = {"crossref": _crossref, "arxiv": _arxiv, "local": _local}.get(layer)
        if fn is None:
            continue
        t0 = time.time()
        try:
            got = fn(query, limit)
            # 在线层（crossref/arxiv）必须过相关性校验；本地层已按 token 匹配，直接保留
            if layer in ("crossref", "arxiv"):
                got = _relevance(query, got)
            tried.append({"layer": layer, "count": len(got), "seconds": round(time.time() - t0, 2)})
            papers.extend(got)
            if got:
                break  # 首层命中即停，不浪费冗余层
        except Exception as e:
            errors.append(f"{layer}: {type(e).__name__}: {str(e)[:120]}")
            tried.append({"layer": layer, "count": 0, "error": type(e).__name__})
    return {
        "query": query,
        "found": bool(papers),
        "papers": papers[:limit],
        "layers_tried": tried,
        "errors": errors,
    }


def _identity(p: Dict[str, Any]) -> str:
    """论文唯一标识：DOI 优先，否则标题归一化（去空格/标点/小写）。"""
    doi = (p.get("doi") or "").strip().lower()
    if doi:
        return "doi:" + doi
    return "title:" + re.sub(r"[^a-z0-9\u4e00-\u9fff]", "", (p.get("title") or "").lower())


def _first_author(p: Dict[str, Any]) -> str:
    """第一作者姓氏（小写）；本地库无作者则用 path:line 当身份，避免被当成同一作者。"""
    authors = p.get("authors") or []
    if authors:
        name = str(authors[0])
        # "Miller, Edward M." / "Edward M. Miller" / "Edward Miller" → 取末词或首词姓氏
        parts = re.split(r"[\s,]+", name.strip())
        return (parts[0] if "," in name else parts[-1]).lower()
    return f"local:{p.get('path','')}:{p.get('line','')}"


def verify_diverse(queries: List[str], min_papers: int = 5, min_authors: int = 3,
                   limit_per_query: int = 5,
                   layers: str = "crossref,arxiv,local") -> Dict[str, Any]:
    """多样证核验：跨多个查询累积论文，按 DOI/标题去重，要求 ≥min_papers 篇不同论文
    且 ≥min_authors 个不同第一作者。单篇/单作者孤证一律 diverse_ok=false（fail-closed）。

    用户 2026-11-19 加严：「不仅要一定能查到论文，还要保证多样证（≥5 篇不同论文）」。
    """
    all_papers: Dict[str, Dict[str, Any]] = {}
    tried: List[Dict[str, Any]] = []
    errors: List[str] = []
    for q in queries:
        if not isinstance(q, str) or not q.strip():
            continue
        r = search_papers(q, limit_per_query, layers)
        tried.append({"query": q, "found": r["found"], "layers": r["layers_tried"]})
        errors.extend(r.get("errors") or [])
        for p in r["papers"]:
            all_papers.setdefault(_identity(p), p)
    papers = list(all_papers.values())
    authors = {_first_author(p) for p in papers}
    diverse_ok = len(papers) >= min_papers and len(authors) >= min_authors
    return {
        "diverse_ok": diverse_ok,
        "found": bool(papers),
        "n_papers": len(papers),
        "n_authors": len(authors),
        "min_papers": min_papers,
        "min_authors": min_authors,
        "papers": papers,
        "queries": tried,
        "errors": errors,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="稳定的外部金融论文检索（三层冗余，fail-closed，多样证）")
    ap.add_argument("--query", required=True, help="通用检索词（机制/方法名，不含表达式/数据集/字段名）；"
                                                   "多样证模式下用逗号分隔多个查询")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--layers", default="crossref,arxiv,local", help="逗号分隔，默认三层全开")
    ap.add_argument("--diverse", action="store_true", help="多样证模式：跨查询累积，要求 ≥min-papers 篇 ∧ ≥min-authors 作者")
    ap.add_argument("--min-papers", type=int, default=5)
    ap.add_argument("--min-authors", type=int, default=3)
    ap.add_argument("--json", dest="json_path", default=None, help="结果写 JSON 到该路径")
    args = ap.parse_args(argv)

    queries = [q.strip() for q in args.query.split(",") if q.strip()]
    if args.diverse or len(queries) > 1:
        result = verify_diverse(queries, args.min_papers, args.min_authors, args.limit, args.layers)
        ok = result["diverse_ok"]
        print(f"diverse_ok: {ok} | papers={result['n_papers']}/{result['min_papers']} "
              f"authors={result['n_authors']}/{result['min_authors']}")
        for q in result["queries"]:
            print(f"  query '{q['query']}': found={q['found']}")
    else:
        result = search_papers(queries[0], args.limit, args.layers)
        ok = result["found"]
        print(f"query: {result['query']}")
        print(f"found: {result['found']} | layers: {result['layers_tried']}")
    if args.json_path:
        os.makedirs(os.path.dirname(os.path.abspath(args.json_path)), exist_ok=True)
        with open(args.json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=1)
    for p in result["papers"]:
        print(f"  - {(p.get('title') or p.get('path',''))[:100]} [{p.get('year')}] "
              f"{p.get('doi') or p.get('path','')}")
    if result.get("errors"):
        print("  errors: " + " ; ".join(result["errors"][:3]), file=sys.stderr)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
