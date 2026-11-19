# -*- coding: utf-8 -*-
"""_gate_knowledge.py - gate.py 拆分·知识闸（check_priors，KB-aware）与机制证据闸
(check_evidence_gate，2026-11-15：新机制首次派波前论坛/论文检索留痕核对)。

依赖：assemble_priors（priors 读取）、_lib.ledger（evidence 闸查 forum_recon_* /
forum_paper_recon_* 留痕——只查留痕不做检索，live 检索是 S2 设计动作）。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import expr_fields, load_platform_constraints
from _lib.ledger import make_ledger_store

# 知识闸（KB-aware）：复用 assemble_priors 的读取能力，保证 gate 永远对照结构化 KB。
try:
    from assemble_priors import load_priors_file, assemble_priors_dict, priors_sha
except Exception:  # 模块缺失时降级为"无 KB 可用"
    load_priors_file = None
    assemble_priors_dict = None
    priors_sha = None

def check_evidence_gate(ctx, dataset, require_evidence=False, batch_type="explore"):
    """机制证据闸（2026-11-15 用户三次质询漏检论坛模板后落地）：

    新机制首次派波前，必须已有论坛/论文检索留痕（forum_recon_* / forum_paper_recon_*），
    否则 FAIL（--require-evidence 时）/ WARN（默认）。闸只查留痕、不做检索——
    live 检索是 Agent 在 S2 设计模板时的动作（tools/forum_recon.py，故障≠无解），
    闸在发批前核对「做没做」。豁免通道：--batch-type repair/probe（参数变体批不重查），
    或 waiver 协议（§8.1.2，evidence 闸 3 天期）。

    返回 dict: {applied, pass, source, issues:[{code,severity,detail}]}

    行为：
      [EVID-FORUM]  7 天内该 dataset 的论坛检索留痕缺失（ok/no_result/error 均算留痕）
          severity = fail（若 --require-evidence 且非豁免批）否则 warn
      [EVID-PAPER]  论文检索留痕缺失（forum_paper_recon_<qkey>，手写摘要键）
          severity 同上
      [EVID-TERMS]  留痕 payload 里检索词未覆盖三维矩阵（机制措辞/算子×字段/数据集名）
          severity = warn（留痕在案但词维不全——提示下轮补齐，不阻断）

    判据来源（三次漏检实证）：
      1) campaign7/8 情绪塔两轮未查论坛，漏 FF65210「情绪-收益相关性错位」帖（IND S2.46）；
      2) GB-Z3 earningscall_sentiment 按论文先验直设计，漏 WL58980 横向点塔模板（39 赞）；
      3) 根因是措辞维度错配——帖子按机制命名（错位/联动失效），旧检索按数据集名。
    """
    issues = []
    # 豁免批：repair/probe 批不重查（7 天缓存语义内的参数变体，SOP 触发表口径）
    if batch_type in ("repair", "probe"):
        return {"applied": False, "pass": True, "source": "exempt", "issues": []}

    try:
        from _lib.ledger import make_ledger_store
        _store = make_ledger_store(ctx)
        kv = _store.load()
    except Exception as e:
        # ledger 不可达不阻断（闸是检查器不是检索器），WARN 留痕供人核
        issues.append({"code": "EVID-LEDGER-UNREACHABLE", "severity": "warn",
                       "detail": f"ledger 不可读（{e}），证据闸降级为放行——发批前请人工核对论坛/论文留痕"})
        return {"applied": False, "pass": True, "source": "unreachable", "issues": issues}

    import datetime as _dt
    _now = _dt.datetime.now()
    cutoff = _now - _dt.timedelta(days=7)

    def _recent(prefix, ds):
        """7 天内的留痕（ok/no_result/error 均算留痕）。

        ⚠ forum_recon_<qkey> 的 qkey 是**内容哈希**（10 位十六进制），键名不含数据集名——
        数据集匹配必须读 payload：question 模板含数据集/族名（"<REGION> <数据集> 有无解法"），
        queries_tried 含实际用过的检索词。键名匹配在本区 7 条真实留痕上实测全失配。
        """
        hits = []
        ds_token = (ds or "").split("_")[0].lower()
        for key, payload in kv.items():
            if not key.startswith(prefix):
                continue
            blob = payload if isinstance(payload, dict) else {}
            question = str(blob.get("question") or "")
            queries = " ".join(str(q) for q in (blob.get("queries_tried") or []))
            searchable = f"{question} {queries} {key}".lower()
            if ds_token and ds_token not in searchable:
                continue
            ts = blob.get("searched_at") or blob.get("updated_at") or blob.get("created_at")
            if ts is None:
                hits.append((key, blob))
                continue
            try:
                t = _dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                if t.tzinfo is None:
                    t = t.replace(tzinfo=None)
                if t >= cutoff:
                    hits.append((key, blob))
            except Exception:
                hits.append((key, blob))
        return hits

    forum_hits = _recent("forum_recon", dataset)
    paper_hits = _recent("forum_paper_recon", dataset)

    # ★2026-11-19 用户明令：EVID-PAPER 不要「留痕就算过」，要「一定能查到论文」。
    # 从留痕 payload 取实际检索词，调用稳定的 paper_search（Crossref→arXiv→本地库）实证：
    #   found=true  → pass（真的查到了，附 DOI/标题）
    #   found=false → fail（留痕在案但查不到论文，按用户要求不通过）—— 不再只看留痕键存在
    # 无留痕时，用 dataset 机制词直接实查一次；查到也算过（省去单独补留痕）。
    paper_verified = None  # {found, papers, source}
    try:
        _repo = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             os.pardir, os.pardir, os.pardir, os.pardir))
        # scripts -> wq-brain-campaign-toolkit -> skills -> Claude -> repo root
        if _repo not in sys.path:
            sys.path.insert(0, _repo)
        from tools.research.paper_search import verify_diverse as _verify_diverse

        queries: List[str] = []
        # ★优先用留痕里已声明的真实论文 cite（作者+年份）去 Crossref 精确核验——
        # 这是「查到论文」的强证据；dataset 名不是论文检索词，拿它搜只会命中噪声行。
        for _k, _b in paper_hits:
            _blob = _b if isinstance(_b, dict) else {}
            for p in (_blob.get("papers") or []):
                cite = (p.get("cite") if isinstance(p, dict) else str(p)) or ""
                m = re.match(r"\s*([A-Z][A-Za-z\-]+(?:\s*&\s*[A-Z][A-Za-z\-]+)?)\s*\((\d{4})", str(cite))
                if m:
                    authors = re.sub(r"\s*&\s*", " ", m.group(1))
                    queries.append(f"{authors} {m.group(2)}")
            if _blob.get("paperPrior"):
                queries.append(str(_blob["paperPrior"])[:120])
        # 去重保序，最多 3 条（避免多次 HTTP）
        seen = set()
        queries = [q for q in queries if not (q in seen or seen.add(q))][:3]
        if not queries:
            # 无 cite 留痕：用 question 里的机制措辞（不含数据集 id 数字后缀）
            for _k, _b in paper_hits:
                _blob = _b if isinstance(_b, dict) else {}
                if _blob.get("question"):
                    queries.append(str(_blob["question"])[:120])
        # ★不允许用 dataset 名兜底：Crossref 对 "institutions" 这类泛词会返回同名无关论文
        #   （实测 "Institutions, institutions, institutions" 被算成 5 篇 4 作者 = 假阳性）。
        #   无 cite / 无 paperPrior / 无 question 留痕 ⇒ queries 为空 ⇒ 多样证核验直接 fail-closed，
        #   逼迫上游（S2 设计期）写真实机制检索词并落留痕，而不是靠数据集名蒙混过关。
        #   （dataset 名只用于日志标注，不进 queries。）
        # ★用户 2026-11-19 加严：多样证——跨查询累积 ≥5 篇不同论文 ∧ ≥3 个不同第一作者。
        _r = _verify_diverse(queries, min_papers=5, min_authors=3, limit_per_query=5)
        paper_verified = {
            "diverse_ok": _r["diverse_ok"], "found": _r["found"],
            "n_papers": _r["n_papers"], "n_authors": _r["n_authors"],
            "papers": _r["papers"][:5], "queries": _r["queries"], "errors": _r.get("errors"),
        }
    except Exception as _pe:
        paper_verified = {"found": None, "error": f"{type(_pe).__name__}: {str(_pe)[:100]}"}

    sev = "fail" if require_evidence else "warn"
    if not forum_hits:
        issues.append({"code": "EVID-FORUM", "severity": sev,
                       "detail": f"数据集 {dataset} 无 7 天内论坛检索留痕（forum_recon_*）——"
                                 f"新机制首次派波前必须先跑 tools/forum_recon.py，"
                                 f"检索词按三维矩阵（机制措辞/算子×字段/数据集名）各至少 1 个。"
                                 f"豁免：repair/probe 批自动放行，或 tools/waiver.py new --gate evidence（3 天期）"})
    else:
        issues.append({"code": "EVID-FORUM", "severity": "pass",
                       "detail": f"论坛留痕在案：{', '.join(k for k, _ in forum_hits[:3])}"})
    # ★用户 2026-11-19 加严：论文必须「多样证」才算过——≥5 篇不同论文 ∧ ≥3 个不同第一作者。
    if paper_verified and paper_verified.get("diverse_ok") is True:
        _titles = "; ".join(
            (p.get("title") or p.get("path") or "")[:70] for p in paper_verified["papers"][:5]
        )
        issues.append({"code": "EVID-PAPER", "severity": "pass",
                       "detail": f"论文多样证达标：{paper_verified['n_papers']} 篇 / "
                                 f"{paper_verified['n_authors']} 作者（≥5 篇 ∧ ≥3 作者）｜{_titles}"})
    else:
        # 孤证/查不到（含工具故障）一律 FAIL——fail-closed，留痕不算通过。
        if paper_verified and paper_verified.get("diverse_ok") is False:
            _why = (f"多样证不足：{paper_verified.get('n_papers', 0)} 篇 / "
                    f"{paper_verified.get('n_authors', 0)} 作者，需 ≥5 篇 ∧ ≥3 作者"
                    f"（query {len(paper_verified.get('queries', []))} 条）")
        elif paper_verified and paper_verified.get("found") is False:
            _why = "论文检索未命中（found=false）"
        else:
            _why = (f"论文核验工具故障：{paper_verified.get('error')}" if paper_verified else "无检索词可查")
        issues.append({"code": "EVID-PAPER", "severity": "fail",
                       "detail": f"数据集 {dataset} {_why}——用户硬闸：EVID-PAPER 必须多样证"
                                 f"（≥5 篇不同论文 ∧ ≥3 不同第一作者），留痕/单篇不算通过。"
                                 f"用 tools/research/paper_search.py --diverse（Crossref→arXiv→本地库三层冗余）"
                                 f"实查并确认 diverse_ok=true；不足须补机制检索词或换机制，不得伪造。"})
    # 三维检索词覆盖（EVID-TERMS，仅 WARN）：最新留痕的 queries_tried 若连数据集名都没查，
    # 提示措辞维度缺失——campaign7/8 两次漏检的根因即「只按数据集名检索，未按机制措辞检索」。
    if forum_hits:
        newest = max(forum_hits, key=lambda hb: str(hb[1].get("searched_at") or ""))
        queries = [str(q) for q in (newest[1].get("queries_tried") or [])]
        ds_token = (dataset or "").split("_")[0].lower()
        if queries and not any(ds_token in q.lower() for q in queries):
            issues.append({"code": "EVID-TERMS", "severity": "warn",
                           "detail": f"最新论坛留痕 {newest[0]} 的检索词 {queries} 未含数据集名维度——"
                                     f"按三维矩阵（机制措辞/算子×字段/数据集名）补一轮检索再设计臂"})

    # ★2026-11-19：EVID-PAPER 实证核验一旦执行，闸即 applied（不再取决于留痕存在）。
    applied = require_evidence or bool(forum_hits) or bool(paper_hits) or paper_verified is not None
    gate_pass = not any(i["severity"] == "fail" for i in issues)
    return {"applied": applied, "pass": gate_pass, "source": "ledger",
            "issues": issues}


def check_priors(ctx, exprs, dataset, require_priors=False):
    """知识闸（KB-aware）：提交前波必须对照结构化 KB，否则静默漏掉已知死路。

    返回 dict: {applied, pass, sha, source, issues:[{code,severity,detail}]}

    行为：
      [PRIORS-MISSING]       priors 文件与 DB 兜底均无可用 KB
          severity = fail（若 --require-priors）否则 warn
      [PRIORS-DEADEND-HIT]   波数据集或表达式字段命中某 dead_end family
          severity = fail（若 --require-priors）否则 warn

    取数优先级：落盘 priors 文件 -> DB 兜底 assemble_priors_dict（保证闸永远 KB-aware，
    不依赖 assemble-priors 先跑过）。WARN 默认仅提示；--require-priors 上升为 FAIL。
    """
    issues = []

    # 1) 取 priors：优先落盘文件，缺失则 DB 兜底
    priors, source = None, "none"
    if load_priors_file is not None:
        try:
            priors = load_priors_file(ctx)
            if priors is not None:
                source = "file"
        except Exception:
            priors = None
    if not isinstance(priors, dict) or not (priors.get("wins") or priors.get("dead_ends")):
        if assemble_priors_dict is not None:
            try:
                priors = assemble_priors_dict(ctx)
                source = "db_fallback"
            except Exception:
                priors = None
    if not isinstance(priors, dict) or not (priors.get("wins") or priors.get("dead_ends")):
        sev = "fail" if require_priors else "warn"
        issues.append({"code": "PRIORS-MISSING", "severity": sev,
                       "detail": "无可用 KB（文件缺失且 DB 兜底为空）；GEM 可能重探已知死路"})
        return {"applied": False, "pass": sev != "fail", "sha": None,
                "source": source, "issues": issues}

    sha = None
    if priors_sha is not None:
        try:
            sha = priors_sha(ctx)
        except Exception:
            sha = None

    # 2) dead_end 命中检测（波数据集 + 表达式字段 vs dead_end family）
    # 2026-10-30：取 `dead_ends`（注入 prompt 的 12 条名额）∪ `_dead_ends_all`（全量）。
    # 只读前者会让闸对名额外的死路失明——KOR 实有 99 条，wave187/200 两次打已判死的
    # fund_holdings_panel 都是这么漏的（死条目被 MAX_DEADENDS 截断，闸根本没看见）。
    dead = [d for d in (priors.get("dead_ends") or []) if isinstance(d, dict)]
    _extra = [d for d in (priors.get("_dead_ends_all") or []) if isinstance(d, dict)]
    if _extra:
        _seen = {(d.get("family") or "").lower() for d in dead}
        dead += [d for d in _extra if (d.get("family") or "").lower() not in _seen]
    if dead and dataset:
        known_ops = set()
        try:
            known_ops = set(load_platform_constraints().get("known_ops", []))
        except Exception:
            pass
        fields = set()
        for e in exprs:
            fields |= expr_fields(e, known_ops)
        ds_l = dataset.lower()
        for d in dead:
            fam = (d.get("family") or "").lower()
            if not fam:
                continue
            hit = (ds_l in fam) or fam.startswith(ds_l) or any(f.lower() in fam for f in fields)
            if hit:
                sev = "fail" if require_priors else "warn"
                issues.append({
                    "code": "PRIORS-DEADEND-HIT", "severity": sev,
                    "detail": f"波数据集/字段命中 dead_end family='{d.get('family')}' "
                              f"reason={(d.get('reason') or '')[:120]}",
                })

    applied_pass = not any(i["severity"] == "fail" for i in issues)
    return {"applied": True, "pass": applied_pass, "sha": sha,
            "source": source, "issues": issues}
