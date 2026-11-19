# -*- coding: utf-8 -*-
"""gate.py - 战役统一提交前闸门（8 闸 + 可选闸0 + sha1 缓存；另有子闸 1b/2b/2b-2 与附加闸 9，见 GATE_REGISTRY）。

闸0 语义反模式（可选，--gate0，默认关闭保持兼容）：恒等式（subtract/divide 同参恒零/恒1、
    add(x,0)/multiply(x,1)/power(x,1) 等恒等或恒常量形式）、裸字段表达式（整式单一字段 ID）、
    元数据字段（periodend/periodtype/fyearend/periodnum/analyststart/curfperiod/curperiod）作信号腿
闸1 语法：import alpha-expression-verifier 直调（WQ_VALIDATOR_DIR 优先；缺失标 SYNTAX_UNKNOWN 报警）
    + 算子元数/命名参数（wqb.expression.op_arity，catalog 驱动；缺失标 ARITY_UNKNOWN 报警）。
    2026-09-07 事故：hump(x, 0.005) 以"语法 8/8 PASS"过闸，平台回 "Invalid number of
    inputs : 2, should be exactly 1 input(s)." 并 CANCEL 整批 8 条 multisim——PLY verifier
    只查括号与字段，查不出"命名参数被当位置参数传"（hump(x, hump=0.01) 的 = 即命名标记）。
闸2 字段白名单：--dataset 自动派生 reference/<region>_<ds>_fields.json（typed catalog 优先）
    或 <region>_<ds>_field_whitelist.json（legacy 兼容）
闸3 类型：catalog 有字段级 type 时数据驱动判定 VECTOR 包裹（fn_spans 解析，不再正则猜）；
    legacy 白名单退 strip 启发式；MATRIX 禁 vec_*
闸4 平台不可访问算子（ts_min/ts_max，必须对 idents 判定而非 ops_used——历史死代码教训）
    + quantile 仅 1 参（本层加严，不改 verifier 签名表）+ 白名单 banned_patterns（scope 感知）
闸5 毒模式：平台级（toolkit config/platform_constraints.json）+ 区域级（reference 生成约束）正则拦截
闸6 批级多样性：diversity_audit 的 next_round_injections 契约强制（每批至少 N 条用注入算子
    + 骨架配额；repair 批豁免，--skip-diversity-gate 逃生；P0-2 过期契约转 FAIL-CLOSED 并自动续约）
闸7 longCount 真实性校验（--sanity-longcount）：对 VECTOR 字段从 typed catalog 读取实际 longCount，
    低于 80 标记 WARN（platform cov 在小宇宙区域系统性误导，见 MEA f72-CF/model25-cb/model31-auditor）
闸8 EVENT 类型自动检测（--sanity-event-type）：表达式引用 typed catalog 中 type==EVENT 的字段即 FAIL
    （fundamental6 整集报废教训）。2026-09-29 更正：旧口径要求「必须用 ts_event_*」，而该系列在平台不存在
    （KOR wave16 实测 8/8 ERROR），修复建议照做必挂；现改为「引用即拦，先单条探针」。

子闸/附加闸（2026-09-29 补登记；此前只在代码注释里，INDEX/文档的闸表漏了它们）：
闸1b 算子元数 + 命名参数；闸2b 区域非法 group 字段；闸2b-2 区域不可用字段 + VECTOR 上套 ts_*；
闸9 非标准窗口（默认 warn，window_whitelist_enforce=true 升 block）。
闸5 判定含：正则毒模式 + 结构判定（add 加权 / add 等权 / 中缀 `+` / 跨数据集价差），覆盖矩阵见
tests/unit/04_gates/test_gate5_coverage_matrix.py。
闸编号的**唯一注册表**是本文件的 GATE_REGISTRY；`python gate.py --print-gate-table` 输出 Markdown 闸表，
文档里的闸表由测试（test_gate_registry_docs）与之比对。

缓存 cache/gate_cache.json，key=sha1(dataset+换行+expr)，幂等跳过。

用法:
  python gate.py --campaign-dir <DIR> --dataset model219 --file candidates/xxx_exprs.json
  python gate.py --campaign-dir <DIR> --dataset model219 --expr "rank(close)"
  python gate.py --campaign-dir <DIR> --dataset model219 --file candidates/xxx.json --batch-type repair
  python gate.py --campaign-dir <DIR> --file candidates/xxx.json --dataset <ds> --sanity-all
退出码: 0=全 PASS, 1=存在 FAIL
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, atomic_write, load_json,
                         load_platform_constraints, read_exprs_any, skeleton, expr_fields)
from _lib.ledger import make_ledger_store
from _lib.skill_roots import skill_roots as _skill_roots
from _lib import rules as rules_mod

# 知识闸（KB-aware）：复用 assemble_priors 的读取能力，保证 gate 永远对照结构化 KB。
try:
    from assemble_priors import load_priors_file, assemble_priors_dict, priors_sha
except Exception:  # 模块缺失时降级为"无 KB 可用"
    load_priors_file = None
    assemble_priors_dict = None
    priors_sha = None

# 机制证据闸（2026-11-15 落地）：实现拆至 _gate_knowledge.py——新机制首次派波前
# 论坛/论文检索留痕核对（详见该模块 docstring 与触发表触发点 0）。
from _gate_knowledge import check_evidence_gate, check_priors  # noqa: F401

# —— 闸实现四模块拆分（2026-11-15 充分拆分，业务功能分界）——
#   _gate_expr_checks.py  表达式检查核心（六闸 + op_arity + 签名/缓存 + ghost 算子）
#   _gate_diversity.py    批级多样性（闸6：骨架/字段族/算子分布 + 暴露持久化）
#   _gate_sanity.py       体检硬门（longcount/event_type）+ 语义闸0
#   _gate_knowledge.py    知识闸（priors KB 对照）+ 机制证据闸（论坛/论文留痕）
# 本文件降为 facade：CLI main + 公有名再导出 + 下划线名读转发。
# ⚠ monkeypatch 写路径必须落在实现模块（tests 已同步）；读路径经 __getattr__ 透明。
from _gate_expr_checks import *  # noqa: F401,F403
from _gate_diversity import *  # noqa: F401,F403
from _gate_sanity import *  # noqa: F401,F403
from _gate_expr_checks import _ghost_ops, _resolve_workspace_deps  # main 直接调用

_IMPL_MODULES = None


def __getattr__(name):
    """PEP 562：下划线名（及一切未再导出名）读转发到实现模块。

    仅读路径透明——monkeypatch 写路径 setattr 到本模块会遮蔽转发，
    被 check_one 等实现函数读不到，必须 patch 实现模块（tests 已同步）。
    """
    global _IMPL_MODULES
    if _IMPL_MODULES is None:
        import _gate_diversity
        import _gate_expr_checks
        import _gate_knowledge
        import _gate_sanity
        _IMPL_MODULES = (_gate_expr_checks, _gate_diversity, _gate_sanity, _gate_knowledge)
    _miss = object()
    for m in _IMPL_MODULES:
        v = m.__dict__.get(name, _miss)
        if v is not _miss:
            return v
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")



def main():
    if "--print-gate-table" in sys.argv[1:]:
        print(render_gate_table())
        return
    ap = argparse.ArgumentParser(description="战役提交前 8 闸预检（+可选闸0 语义反模式；--print-gate-table 输出闸表）")
    add_campaign_arg(ap)
    ap.add_argument("--file")
    ap.add_argument("--expr")
    ap.add_argument("--from-db", action="store_true", help="从 expressions 表读本波候选")
    ap.add_argument("--wave", default=None, help="波号（--from-db 必填；写入 gate_results）")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--datasets", default="",
                    help="逗号分隔额外数据集，与 --dataset 合并白名单（跨金字塔 mix）")
    ap.add_argument("--declared-cross-spreads", default="",
                    help="跨集价差经济含义声明，格式 '集A,集B;集C,集D'（2026-10-01 用户修正）")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--cache-file", default=None,
                    help="缓存文件重定向（默认 <campaign>/cache/gate_cache.json；干跑验证用临时路径）")
    ap.add_argument("--batch-type", default="explore",
                    help="批次类型：explore=探索批（默认，受闸6 约束）；repair=修复/设置变体批（豁免）")
    ap.add_argument("--skip-diversity-gate", action="store_true",
                    help="跳过闸6 批级多样性强制（逃生阀，需在台账记录原因）")
    ap.add_argument("--fix", action="store_true",
                    help="自动修复：VECTOR 数据集下裸用的 VECTOR 字段裹上 vec_* 后再检测（幂等，输出 fixed_expr）")
    ap.add_argument("--sanity-longcount", action="store_true",
                    help="闸7：longCount 真实性校验（VECTOR 字段实际 longCount < 80 标记 WARN）")
    ap.add_argument("--sanity-event-type", action="store_true",
                    help="闸8：EVENT 类型自动检测（引用 type==EVENT 的字段即 FAIL；平台无 ts_event_*，先单条探针）")
    ap.add_argument("--sanity-all", action="store_true",
                    help="一次性跑闸 7+8（--sanity-longcount + --sanity-event-type）")
    ap.add_argument("--gate0", action="store_true",
                    help="闸0：语义反模式检查（恒等式/裸字段/元数据字段腿；默认关闭，命中即 FAIL）")
    ap.add_argument("--require-priors", action="store_true",
                    help="知识闸硬约束：priors 缺失或波命中 dead_end family 时 FAIL（默认仅 WARN）")
    ap.add_argument("--require-evidence", action="store_true",
                    help="机制证据闸硬约束（2026-11-15）：新机制首次派波前论坛/论文检索留痕缺失时 FAIL"
                         "（默认仅 WARN；repair/probe 批自动豁免；waiver --gate evidence 3 天期）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    _resolve_workspace_deps(a.campaign_dir)

    if a.from_db:
        if not a.wave:
            ap.error("--from-db 需要 --wave")
        from _lib.wqb_store import get_store
        st = get_store(ctx)
        try:
            rows = st.list_expressions(ctx.region, str(a.wave), dataset=a.dataset)
            if not rows:
                rows = st.list_expressions(ctx.region, str(a.wave))
            # 2026-09-09 D12：同时排除 dropped（纪律废弃终态），与 superseded 同级。
            # 此前只排 superseded，Agent dropped 的 vec_* 类型不兼容骨架（11637）
            # 仍进 gate，一条 [TYPE] FAIL 拖垮整波 all_pass。
            exprs = [r["expression"] for r in rows
                     if r.get("expression") and r.get("status") not in ("superseded", "dropped")]
        finally:
            st.close()
        if not exprs:
            ap.error(f"db 无表达式: {ctx.region} wave={a.wave} dataset={a.dataset}")
    elif a.file:
        exprs = read_exprs_any(a.file)
    elif a.expr:
        exprs = [a.expr]
    else:
        ap.error("need --from-db / --file / --expr")

    extra = [x.strip() for x in (a.datasets or "").split(",") if x.strip()]
    ds_all = [a.dataset] + [x for x in extra if x != a.dataset]
    wl = merge_whitelists(ctx, ds_all) if len(ds_all) > 1 else load_whitelist(ctx, a.dataset)
    pc = load_platform_constraints()
    pc["_region"] = ctx.region  # 闸2b 区域非法 group 字段判定用（2026-09-19）
    pc["_ghost_all"] = sorted(_ghost_ops(pc))   # 入签名：幽灵名单变了缓存必须失效
    if len(ds_all) > 1:
        # 多数据集 mix 批：给价差规则（spread_cross_dataset）提供 field→dataset 映射；
        # 多个数据集共有的字段歧义，不参与同源判定。单数据集批所有字段同源，无须映射。
        _fd = {}
        for _ds in ds_all:
            try:
                for _f in load_whitelist(ctx, _ds)[0]:
                    _fd[_f] = _ds if _f not in _fd else None
            except Exception:
                pass
        pc["_field_dataset"] = {f: d for f, d in _fd.items() if d}
        # 2026-10-01：跨集价差经济含义声明（平台级 pairs + 区域 reference 覆盖 + CLI 追加）
        _declared = []
        _declared += (pc.get("declared_cross_spreads") or {}).get("pairs") or []
        if os.path.exists(ctx.constraints_path()):
            _declared += (load_json(ctx.constraints_path()).get("declared_cross_spreads") or {}).get("pairs") or []
        if a.declared_cross_spreads:
            for _p in a.declared_cross_spreads.split(";"):
                _ab = [x.strip() for x in _p.split(",") if x.strip()]
                if len(_ab) >= 2:
                    _declared.append(_ab)
        pc["_declared_spread_pairs"] = _declared
    poison = list(pc.get("poison_patterns", []))
    cons_path = ctx.constraints_path()
    if os.path.exists(cons_path):  # 区域特有 poison 追加（平台级勿复制进区域文件）
        poison += load_json(cons_path).get("poison_patterns", [])

    sig = gate_signature(ds_all, wl, poison, pc)

    # --fix 会改写表达式，缓存键与原始表达式不一致，禁用缓存以免污染
    use_cache = not a.no_cache and not a.fix
    cache = {}
    cache_path = a.cache_file
    if use_cache and cache_path:
        cache = load_json(cache_path) if os.path.exists(cache_path) else {}
    elif use_cache:
        try:
            from _lib.wqb_store import get_store
            st = get_store(ctx)
            cache = st.get_ledger(ctx.region, f"gate_cache_{a.dataset}") or {}
            if not isinstance(cache, dict):
                cache = {}
            st.close()
        except Exception:
            cache = {}
    dirty = False
    report, all_pass = [], True
    for i, e in enumerate(exprs, 1):
        ck = cache_key(a.dataset, e, sig)
        if use_cache and ck in cache and not env_unknown(cache[ck].get("issues")):
            item = dict(cache[ck])
            item["index"] = i
            item["cached"] = True
        else:
            item = check_one(e, wl, a.dataset, poison, pc, fix=a.fix)
            item["index"] = i
            # 闸门环境缺失时的结论（[*_UNKNOWN]）不入缓存：环境修好后必须重判，而不是继续拿缓存的 FAIL
            if use_cache and not env_unknown(item["issues"]):
                cache[ck] = {k: item[k] for k in ("fields", "issues", "pass")}
                dirty = True
        item["expr"] = e  # 原式（入库口径）：调用方据此按式回写逐条结论，不依赖 index 顺序
        all_pass = all_pass and item["pass"]
        report.append(item)
    if dirty and use_cache:
        if cache_path:
            atomic_write(cache_path, cache)
        else:
            try:
                from _lib.wqb_store import get_store
                st = get_store(ctx)
                st.upsert_ledger(ctx.region, f"gate_cache_{a.dataset}", cache)
                st.close()
            except Exception:
                pass
    # 闸 7/8：数据质量预检（--sanity-* / --sanity-all）
    sanity_issues = []
    run_longcount = a.sanity_all or a.sanity_longcount
    run_event = a.sanity_all or a.sanity_event_type
    if run_longcount or run_event:
        _, data_type, field_types, _ = wl
        if run_longcount:
            sanity_issues.extend(check_sanity_longcount(ctx, a.dataset, exprs, field_types))
        if run_event:
            sanity_issues.extend(check_sanity_event_type(ctx, a.dataset, exprs, field_types))
        if sanity_issues:
            all_pass = False
    # 闸0 语义反模式（可选，--gate0；与闸 1-5 并列，不计入 check_one 的 issues）
    gate0_blocked = []
    if a.gate0:
        known_ops0 = set(pc["known_ops"])
        for e in exprs:
            g0 = check_semantic_gate0(e, known_ops=known_ops0)
            if g0:
                gate0_blocked.append({"expr": e, "issues": g0})
        if gate0_blocked:
            all_pass = False
    # 闸6 批级多样性（仅批量模式；契约存在且生效时强制）
    # --fix 时用修复后的表达式统计骨架/算子，与最终提交一致
    # 2026-09-01 单表达式豁免：单条调试（--expr）凑不齐批级配额（≥2 shapes/骨架配比），
    # 多样性闸自动跳过并注明；批级多样性约束仍由 build_wave/wave_gate 在批量场景强制。
    exprs_for_diversity = [r.get("fixed_expr", exprs[r["index"] - 1]) for r in report]
    if len(exprs_for_diversity) <= 1 and not a.skip_diversity_gate:
        dissues, consume_ref = [], None
        print("[DIVERSITY-SKIP] 单表达式模式：批级多样性闸不适用（≥2 表达式才评估），仅静态闸结果生效")
    else:
        dissues, consume_ref = check_batch_diversity(exprs_for_diversity, ctx, batch_type=a.batch_type,
                                                     skip=a.skip_diversity_gate, dataset=a.dataset)
    if dissues:
        all_pass = False
    if consume_ref is not None and all_pass:
        consume_diversity(ctx, consume_ref)
    # 知识闸（KB-aware）：对照结构化 KB，避免重探已知死路 / 收不到胜方配方
    priors_gate = check_priors(ctx, exprs, a.dataset, require_priors=a.require_priors)
    if not priors_gate["pass"]:
        all_pass = False
    # 机制证据闸（2026-11-15 落地，2026-11-19 加严）：新机制首次派波前须有论坛留痕 + 论文实证查到。
    # ★用户 2026-11-19 明令：EVID-PAPER 不再「留痕就算过」——闸调 tools/research/paper_search.py
    #   （Crossref→arXiv→本地库三层冗余）真查论文，found=false 即 fail（默认硬拦，所有 wave_gate）。
    #   弃用 WebSearch/WebFetch/Semantic Scholar。repair/probe 批自动豁免。
    evidence_gate = check_evidence_gate(ctx, a.dataset, require_evidence=a.require_evidence,
                                        batch_type=a.batch_type)
    if not evidence_gate["pass"]:
        all_pass = False
    payload = {"all_pass": all_pass, "dataset": a.dataset, "total": len(exprs),
                      "passed": sum(r["pass"] for r in report),
                      "cached": sum(1 for r in report if r.get("cached")),
                      "sanity_gates": {
                          "applied": bool(sanity_issues) or run_longcount or run_event,
                          "pass": not sanity_issues,
                          "issues": sanity_issues},
                      "diversity_gate": {
                          "applied": consume_ref is not None or bool(dissues),
                          "pass": not dissues,
                          "issues": dissues,
                          "consumed": consume_ref is not None},
                      "priors_gate": priors_gate,
                      "evidence_gate": evidence_gate,
                      "report": report}
    if a.gate0:  # 仅在开启时附加，缺省输出结构与历史完全一致
        payload["gate0"] = {"checked": len(exprs), "blocked": gate0_blocked}
    if a.wave:
        try:
            from _lib.wqb_store import get_store
            st = get_store(ctx)
            st.upsert_gate_result(ctx.region, str(a.wave), a.dataset, payload)
            st.close()
        except Exception as e:
            print(f"[gate] 入库异常: {e}", file=sys.stderr)
    print(json.dumps(payload, ensure_ascii=False, indent=1))
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    main()


