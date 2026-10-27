# -*- coding: utf-8 -*-
"""编排层：原 main() 逐字搬迁并改名 run()。⚠ P2 待办：534 行内部尚未拆成 stage 函数。"""
import os
import sys
import json
import re
import asyncio
import sqlite3
import subprocess
import collections
import time
from datetime import datetime

from .config import *            # noqa: F401,F403
from .config import _WQB_SCRIPTS_DIR  # noqa: F401

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from campaign_semantics import (  # noqa: E402,F401
    LIT_THRESHOLD, VIRGIN_AC, VIRGIN_VS, VIRGIN_MIN_COV, VIRGIN_COV_FLOOR,
    is_virgin, all_datasets, exposure_profile, lit_set,
    NAME_META, is_name_metadata, classify_desc,
    FORM_FAMILIES, GATED_CATS, GATE_Q, POSTPROC_Q, PER_DIM, MIN_FIELDS_TOTAL,
    FULL_FIELD_CAP, BLACKBOX_FAMILIES, field_tier,
    FAMILY_EXPOSURE, EXPOSURE_VOCAB, EXPR_EXPOSURE, field_exposure_hint,
    CONCEPT_FAMILIES, CONCEPT_ZH, field_concepts, concept_families,
    PP_VOCAB, parse_preprocessing, load_s1_preprocessing, apply_preprocessing,
    _DESC_NOISE, clean_desc, _load_form_overrides, _load_llm_tags, LLM_CONF_MIN,
    FORM_EVIDENCE, field_form, print_form_audit,
)
from .bad_tokens import *  # noqa
from .persist import *  # noqa
from .transport import *  # noqa
from .fields import *  # noqa
from .generate import *  # noqa
from .audit import *  # noqa
from .lit import *  # noqa
from .sweep import *  # noqa
from .mirror import *  # noqa
from .report import *  # noqa
from .fields import _family_key  # noqa
from .transport import _FORCED_RELEASE, row6  # noqa


def _absorb(rows, all_alphas, per_tpl, tpl, batch=None):
    """收割行 → all_alphas / per_tpl（2026-10-26：统一走 6 元组，rob 缺失为 None）。

    五处解包点共用本函数：收割脚本加 `rob=` 后行变成 6 元组，
    旧写法 `for aid, sv, fv, y2, sub in rows` 会直接 ValueError 把整集打断。
    """
    n = 0
    for _row in (rows or []):
        r6 = row6(_row)
        if not r6:
            continue
        aid, sv, fv, y2, sub, rob = r6
        nt = norm_tpl(tpl)
        per_tpl[nt].append((aid, sv, y2, sub))
        all_alphas.append({"alpha": aid, "tpl": nt, "s": sv, "f": fv,
                           "y2": y2, "sub": sub, "rob": rob,
                           "batch": batch or tpl})
        n += 1
    return n


def _val(v):
    """收割哨兵 -99（MISSING）→ None。0.0 是合法值，不能用 `or` 链。"""
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if x <= -90 else x


def pick_prod_target(all_alphas, g2y, gsub=None, grob=None):
    """选 prod 探测目标：**全闸（含 robust）已过**的最高 S > RA 全过的最高 S > 裸 max S。

    2026-10-26：旧实现一律取 max(S)，于是 IND 每集都拿 robust 0.8x 的票去测 prod，
    robust 过线的那颗（往往 S 低 0.05）从未被试过 —— 这是「ATOM 全灭于 robust」
    在流程侧的half：不是没有可救的候选，是候选选择根本不看 robust。
    EUR（grob=None）保持原行为，一行不变。
    """
    cand = [a for a in all_alphas if _val(a.get("s")) is not None]
    if not cand:
        return None
    if grob is None:
        return max(cand, key=lambda a: _val(a["s"]))

    def _full(a):
        return (_val(a.get("s")) >= 1.58 and (_val(a.get("f")) or 0) >= 1.0
                and (_val(a.get("y2")) or 0) >= g2y
                and (gsub is None or (_val(a.get("sub")) or 0) >= gsub))

    def _rob(a):
        v = _val(a.get("rob"))
        return v is not None and v >= grob

    return (max([a for a in cand if _full(a) and _rob(a)],
                key=lambda a: _val(a["s"]), default=None)
            or max([a for a in cand if _full(a)],
                   key=lambda a: _val(a["s"]), default=None)
            or max(cand, key=lambda a: _val(a["s"])))


def decide_verdict(has_alphas, n_fail, err_msgs, ten_failed, joint,
                   neg_live, max_s, n_strong):
    """集级判定（P0-2 抽出成纯函数，只为可测——顺序即优先级，勿调换）。

    两条 P0-2 相关的语义：
      - `ALIVE_NEG`：正向电池没出全闸，但镜像翻出了「指标全过 + 未被换手拦」的候选，
        与 ALIVE 同等可行动（prod 见 `neg.prod_top`；未测逐年画像，故不冒充 deliverable）。
      - `DEAD_NEG`：正负两向都不可交付，但**数据有强反应**（|S|≥1.58 的 ATOM 结构存在）
        ⇒ 与「无信号 DEAD」区分，下一波别把该集当成没信号而永久搁置。
    """
    if not has_alphas:
        return "SIM_FAIL" if n_fail else ("ERROR" if err_msgs else "NO_DATA")
    if ten_failed:
        return "INSUFFICIENT_HISTORY"
    if joint:
        return "ALIVE"
    if neg_live:
        return "ALIVE_NEG"
    if max_s >= 1.3:
        return "BORDERLINE"
    if (n_strong or 0) > 0:
        return "DEAD_NEG"
    return "DEAD"


def run():
    global MAX_INFLIGHT
    only = None
    limit = None
    priority_cats = None
    only_cats = None         # --only-cats OTHER,PV：只跑这些类目（硬锁定，非排序）
    # 2026-10-25 用户改判：0.8 → **0.6**。B 方案（0.5→0.8）实施后审计发现 32 个集被判
    # SKIPPED_LOW_COV，而「已完成 61 个」里有 59% 是这种空转 ⇒ 目标池实际只测了 41%。
    # 0.6 的边界收益：32 个里 11 个（cov 0.60–0.79）会真正开跑，21 个（<0.6）仍跳过。
    # 低覆盖稀释证据仍有效（cov 0.27–0.34→maxS 0.48、cov 0.197→maxS 0.30），故不降到 0.5。
    priority_min_cov = 0.6   # 用户 2026-10-25 定档
    min_cov_global = None    # --min-cov：全局覆盖率门槛（覆盖 priority / 非 priority 两处字面量）
    require_ten_years = False  # --require-ten-years：候选必须 10 年都有持仓数据
    skip_lit = False
    keep_fields = None       # --keep-fields a,b：这些字段跳过「平台字段清单」过滤（清单常漏掉可用字段）
    audit_ds = None          # --audit a,b：只打印字段×族覆盖矩阵，不跑仿真
    sweep_done = False       # --sweep-done：只对已判完的近闸集补扫设置轴，然后退出
    for i, a in enumerate(sys.argv):
        if a == "--datasets":
            only = sys.argv[i + 1].split(",")
        if a == "--limit":
            limit = int(sys.argv[i + 1])
        if a == "--priority-cats":
            priority_cats = sys.argv[i + 1].split(",")
        if a == "--only-cats":
            only_cats = sys.argv[i + 1].split(",")
        if a == "--priority-min-cov":
            priority_min_cov = float(sys.argv[i + 1])
        if a == "--min-cov":
            min_cov_global = float(sys.argv[i + 1])
        if a == "--require-ten-years":
            require_ten_years = True
        if a == "--skip-lit":
            skip_lit = True
        if a == "--keep-fields":
            keep_fields = [x.strip() for x in sys.argv[i + 1].split(",") if x.strip()]
        if a == "--max-inflight":
            MAX_INFLIGHT = max(1, int(sys.argv[i + 1]))
        if a == "--sweep-done":
            sweep_done = True
        if a == "--audit":
            audit_ds = sys.argv[i + 1].split(",")

    # 2026-10-25 修：`--max-inflight` 必须写回 transport 模块。
    # `from .transport import *` 只是把整数**复制**进 pipeline 的命名空间，而
    # `wait_slot()` 在自己的模块里读 transport.MAX_INFLIGHT ⇒ 旧写法下该参数静默无效，
    # 实际并发恒为 7（用户要求 IND 战役并发 = 2，必须真生效）。
    from . import transport as _transport
    _transport.MAX_INFLIGHT = MAX_INFLIGHT

    # 区域闸位（2026-10-25 IND 开波）：IND 的 2Y 闸是 1.0、sub 是**绝对** 1.0，
    # 与 EUR（2Y 1.58、sub 0.53×S 比率闸）不同。照 EUR 判会把 IND 近闸候选
    # 全部误判 BORDERLINE（runbook §3）。EUR 行为保持不变。
    _G2Y = 1.0 if REGION == "IND" else 1.58
    _GSUB = 1.0 if REGION == "IND" else None
    # robust 闸：平台 LOW_ROBUST_UNIVERSE_SHARPE 限值是**固定 1.0**，与区域无关。
    # 但 EUR 旧流程从不取该指标（收割脚本此前根本不读），故只在 IND 启用，EUR 行为不变。
    _GROB = 1.0 if REGION == "IND" else None

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    load_bad_tokens()
    if BAD_TOKENS:
        print(f"[preflight] 已加载平台黑名单 {len(BAD_TOKENS)} 个：{sorted(BAD_TOKENS)}")
    beat(note="start")

    # 已点亮判定（平台当季金字塔：同一 category 满 3 颗即点亮，2026-10-25 用户裁定）
    counts = compute_lit(REGION)
    lit_cats = lit_set(counts)
    cats_all = [r[0] for r in con.execute(
        f"SELECT DISTINCT category FROM dataset_profile WHERE region='{REGION}' AND category IS NOT NULL")]
    unlit = {c: counts.get(c.upper(), 0) for c in cats_all
             if c.upper() not in lit_cats}
    lit_counts = {c: n for c, n in counts.items() if c in lit_cats}
    print(f"[lit] 已点亮(当季 >={LIT_THRESHOLD} 颗，降权): "
          + (", ".join(f"{c}={n}" for c, n in sorted(lit_counts.items(), key=lambda x: -x[1])) or "无"))
    print(f"[lit] 未点亮(可挖): "
          + (", ".join(f"{c}={n}" for c, n in sorted(unlit.items(), key=lambda x: x[1])) or "无"))
    # 打印 transport 模块的**实际生效值**，不再打印本地副本（2026-10-25：免得再次静默失效）
    print(f"[gate] 同时在飞作业上限 = {_transport.MAX_INFLIGHT}（--max-inflight 可调）")
    print(f"[geom] robust 几何族 = {'ON' if ROBUST_GEOM else 'OFF'}"
          + (f"（{len(ROBUST_TPL)} 族 × 全字段，bf={RG_BF} zw={RG_ZW} "
             f"lv_smooth={RG_LV_SMOOTH}，decay 分档="
             f"{sorted(set(ROBUST_DECAY_BY_TPL.values()) | {ROBUST_DECAY})}，按档独立批）"
             if ROBUST_GEOM else "")
          + ("｜ATOM_ONLY=1（残差族已关）" if ATOM_ONLY else ""))

    ds_list = all_datasets(con, only=only, limit=limit, priority_cats=priority_cats,
                           lit_cats=counts, skip_lit=skip_lit)
    if only_cats:
        oc = {c.upper() for c in only_cats}
        before = len(ds_list)
        ds_list = [d for d in ds_list if (d.get("category") or "").upper() in oc]
        print(f"[only-cats] 锁定 {sorted(oc)}：{before} → {len(ds_list)} 个集")
    ck = load_ckpt()
    res = load_results()

    if audit_ds:
        audit_fields(con, ck, res, audit_ds)
        return

    if sweep_done:
        sweep_done_sets(con, ck, res)
        return

    print(f"[campaign] 数据集总数 {len(ds_list)}｜已完成 {len(ck['done'])}")
    for d in ds_list:
        ds = d["dataset"]
        if ds in ck["done"]:
            continue
        cov = d["cov"] or 0
        cat_u = (d.get("category") or "").upper()
        pri = priority_cats and cat_u in {c.upper() for c in priority_cats}
        # 2026-10-25：--min-cov 覆盖「priority / 非 priority」两处字面量（原本只有 pri 分支可调，
        # 非 pri 恒 0.6 ⇒ 手册 §4.2「两处并列，改一处无效」的同一坑）。
        eff_min = (min_cov_global if min_cov_global is not None
                   else (priority_min_cov if pri else 0.6))
        if is_virgin(d):
            eff_min = min(eff_min, VIRGIN_MIN_COV)
        if cov < eff_min:
            print(f"[skip] {ds} coverage {cov:.2f} < {eff_min}"
                  + ("（优先类别放宽门槛）" if pri else ""))
            ck["done"].append(ds)
            res["results"][ds] = {"verdict": "SKIPPED_LOW_COV", "coverage": cov}
            save_ckpt(ck); save_results(res)
            emit_digest(ds, d["category"], res, ck, len(ds_list))
            continue

        print(f"\n=== {ds} ({d['category']}) fields={d['n_fields']} cov={cov:.2f} vs={d['vs']} ===")
        beat(ds, note="dataset-start")
        prev_fields = (ck.get("fields") or {}).get(ds)
        sel = select_fields(con, ds, field_min_cov=eff_min, only_names=prev_fields,
                            keep_fields=keep_fields)
        # 2026-10-24：处女地集字段级门槛也自适应。equity_conc_metrics 实测 18 个 VECTOR 字段
        # 覆盖率清一色 0.197，在 0.35 下取不到任何字段 ⇒ 整集被 SKIPPED_TOO_FEW_FIELDS 挡死，
        # 而它恰恰是处女地里暴露最多样（4 种）的集。
        # ⚠ 但**不能降到 0**：0.197 覆盖率下 vec_avg 对无数据股票返回 0、ts_backfill 前向填充，
        #   ⇒ 1565/1600 全部满仓（longCount 没问题），但 78% 的排名由填充值决定 ⇒ 信号被稀释。
        #   实测剂量-反应：cov 0.27–0.34 → maxS 0.48（DEU WANL43）；cov 0.197 → maxS 0.30（本集）。
        #   ⇒ 下限设为 0.25（略低于 DEU 已验证的 0.27），低于此值判「数据不可用」而非「低覆盖」。
        if len(sel) < 3 and is_virgin(d) and eff_min > VIRGIN_COV_FLOOR:
            for _mc in (0.25, VIRGIN_COV_FLOOR):
                sel = select_fields(con, ds, field_min_cov=_mc, only_names=prev_fields,
                                    keep_fields=keep_fields)
                if len(sel) >= 3:
                    print(f"  [cov] {ds}: 处女地字段级门槛 {eff_min} → {_mc}（原门槛下 0 字段）")
                    if _mc < 0.25:
                        print(f"  [cov] ⚠ {ds}: 字段覆盖率仅 {_mc} ⇒ 约 "
                              f"{1-_mc:.0%} 的排名将由 vec_avg 填充值 + ts_backfill 决定，"
                              f"信号被稀释，预期 maxS 走低（参考：cov 0.197 → 0.30）")
                    break
        if len(sel) < 3:
            print(f"  字段不足（<3，字段级门槛 {eff_min}），跳过")
            ck["done"].append(ds)
            res["results"][ds] = {"verdict": "SKIPPED_TOO_FEW_FIELDS", "coverage": cov}
            save_ckpt(ck); save_results(res)
            emit_digest(ds, d["category"], res, ck, len(ds_list))
            continue

        # 字段选择持久化：同一集续跑必须沿用同一套字段。否则筛选器一改，已派发族用旧字段、
        # 新派发族用新字段，族间不可比（2026-10-22 修筛选器时发现）。
        if not prev_fields:
            ck.setdefault("fields", {})[ds] = [x["field_name"] for x in sel]
            save_ckpt(ck)
            print(f"  [fields] 锁定代表字段 {len(sel)} 个")

        print_form_audit(ds, sel)
        # 2026-10-24 ①：打印透明度分档，肉眼抽查「黑盒集是否还在被形态分类器假装懂」
        _tiers = collections.Counter(r.get("ftier") or field_tier(r, d["category"], ds) for r in sel)
        print(f"  [tier] {ds}: " + " ".join(f"{k}={v}" for k, v in sorted(_tiers.items())))
        # 2026-10-24 ①：机制概念分布（8 问路径）。命中率即「机制驱动选路」的覆盖面
        _cons = collections.Counter()
        _n_hit = 0
        for r in sel:
            cs = field_concepts(r, d["category"], ds)
            if cs:
                _n_hit += 1
            for c in (cs or ["<无概念>"]):
                _cons[c] += 1
        print(f"  [concept] {ds}: 机制命中 {_n_hit}/{len(sel)} 字段 → "
              + " ".join(f"{CONCEPT_ZH.get(k, k)}={v}" for k, v in _cons.most_common()))
        # 2026-10-24 ③：本地读 S1 台账的 preprocessing（受控词表；自由文本不采信）
        pp_map = load_s1_preprocessing(con, ds)
        if pp_map:
            print(f"  [pp] {ds}: S1 预处理命中 {len(pp_map)} 个字段："
                  + ", ".join(f"{k}→{'+'.join(v)}" for k, v in list(pp_map.items())[:5]))
        freq = DS_FREQ.get(ds, "quarterly" if d["category"] in (
            "ANALYST", "FUNDAMENTAL", "INSIDERS", "INSTITUTIONS", "EARNINGS", "MACRO") else "daily")
        exprs = build_exprs(sel, freq, cat=d["category"], ds=ds, pp_map=pp_map)
        print(f"  代表字段 {len(sel)}（维度 {len(set(x['dim'] for x in sel))}）× 模板族 = {len(exprs)} 条")
        # 2026-10-24 ②：Expected Exposure 分布 —— 收益来源多样性是 prod 相关性的结构性解。
        # 单暴露集 = 与既有同源 alpha 高相关的结构性风险，S/2Y 再高也难独立过 prod。
        _exp = collections.Counter(EXPR_EXPOSURE.get(e, "other") for _t, e in exprs)
        print(f"  [expo] {ds}: {len(_exp)} 种暴露 → "
              + " ".join(f"{k}={v}" for k, v in sorted(_exp.items(), key=lambda kv: -kv[1])))
        if len(_exp) <= 2:
            _dom = _exp.most_common(1)[0]
            print(f"  [expo] ⚠ {ds} 仅 {len(_exp)} 种暴露（{_dom[0]} 占 {_dom[1]}/{len(exprs)}）"
                  f"⇒ 低多样性，prod 相关性结构性风险，优先度下调")

        # 续跑：**按模板族**复用已派发批次，缺哪个族就只派哪个族。
        # ⚠ 三坑（2026-10-22 全踩过）：
        #   ① 不能用 tpl != "cs" 判新旧：旧架构还有 d1/ed/d2/dw 等短名族，会误复用；
        #   ② 不能「有复用就整体跳过派发」：sentiment27 只有 dw 族命中旧批 → 144 条只收 2 条就判 DEAD；
        #   ③ 同名的旧族表达式可能与新架构不同 → 逐批校验「批内表达式 ⊆ 本次该族的表达式」才准复用。
        cur_by_tpl = collections.defaultdict(list)
        for tpl, e in exprs:
            cur_by_tpl[tpl].append(e)
        prev_by_tpl = collections.defaultdict(list)
        for x in (ck.get("sims", {}).get(ds) or []):
            if x and x[0] and x[1] in cur_by_tpl:
                prev_by_tpl[x[1]].append(tuple(x))
        sims, need = [], []
        for tpl, elist in cur_by_tpl.items():
            lst = prev_by_tpl.get(tpl) or []
            want = set(elist)
            reuse_ok = bool(lst)
            if reuse_ok:
                for _sid, _t, bi in lst:
                    fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{tpl}_{bi}.txt")
                    if not os.path.exists(fn):
                        reuse_ok = False
                        break
                    got = {l.strip() for l in open(fn, encoding="utf-8") if l.strip()}
                    if not got <= want:      # 旧批内容 ≠ 新架构该族 → 不能复用
                        reuse_ok = False
                        break
            if reuse_ok:
                sims += lst
                # 缺陷3修复：子集判据会静默丢表达式——复用后必须算差集并补派。
                covered = set()
                for _sid, _t, _bi in lst:
                    fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{_t}_{_bi}.txt")
                    try:
                        covered |= {l.strip() for l in open(fn, encoding="utf-8") if l.strip()}
                    except Exception:
                        pass
                missing = [e for e in elist if e not in covered]
                if missing:
                    print(f"  [resume] {tpl}: 旧批只覆盖 {len(covered)}/{len(elist)} 条 → 补派 {len(missing)} 条")
                    need.append((tpl + "_f", missing))
            else:
                need.append((tpl, elist))
        if sims:
            print(f"  [resume] 复用已派发 {len(sims)} 批（覆盖 {len(cur_by_tpl) - len(need)}/{len(cur_by_tpl)} 族）")
        if need:
            print(f"  [dispatch] 派发 {sum(len(e) for _, e in need)} 条（{len(need)} 族未覆盖）")
            _base = list(sims)

            def _persist(partial, _ds=ds, _base=_base):
                ck["sims"][_ds] = _base + list(partial)
                save_ckpt(ck)

            new_sims = dispatch([(tpl, e) for tpl, elist in need for e in elist], ds, "t",
                                on_batch=_persist)
            ck["sims"][ds] = sims + new_sims
            save_ckpt(ck)
            sims += new_sims

        # 单条批修复：历史断点里 n=1 的批次提交后必为 COMPLETE/children=0（2026-10-22 实测），
        # 结果永远收不到。把这些孤儿表达式合并成均分整批（≤10/批）重派一次。
        orphan = []
        for _sid, tpl, bi in sims:
            if tpl == "rep":
                continue
            fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{tpl}_{bi}.txt")
            if not os.path.exists(fn):
                continue
            lines = [l.strip() for l in open(fn, encoding="utf-8") if l.strip()]
            if len(lines) == 1:
                orphan.append(lines[0])
        if orphan:
            rep_key = ds + "@rep"
            prev_rep = [tuple(x) for x in (ck.get("sims", {}).get(rep_key) or []) if x and x[0]]
            if prev_rep:
                print(f"  [repair] 复用已重派 {len(prev_rep)} 批")
                sims = list(sims) + prev_rep
            else:
                print(f"  [repair] 单条批孤儿 {len(orphan)} 条 → 合并重派（均分 ≤10/批）")
                def _persist_rep(partial, _k=rep_key):
                    ck["sims"][_k] = list(partial)
                    save_ckpt(ck)

                rep = dispatch([("rep", e) for e in orphan], ds, "rep", on_batch=_persist_rep)
                ck["sims"][rep_key] = rep
                save_ckpt(ck)
                sims = list(sims) + rep

        # 收割（允许部分未完成）
        per_tpl = collections.defaultdict(list)
        all_alphas = []
        err_msgs = []
        n_fail = 0          # 平台侧 FAIL 的批次数（整批跑不起来，非"没结果"）
        failed_batches = []  # (tpl, bi) 整批 FAIL/ERROR → 剔除黑名单后重派（缺陷2 自愈）
        for sim_id, tpl, bi in sims:
            if not sim_id:
                continue
            rows, errs, state = harvest_until_done(sim_id, ds, tag=f"{tpl}_{bi}")
            if state == "empty":
                print(f"  [harvest] {tpl}_{bi} COMPLETE children=0（结构性空批），放弃")
            elif state == "fail":
                n_fail += 1
                failed_batches.append((tpl, bi))
                note_bad_tokens(errs)
                print(f"  [harvest] {tpl}_{bi} 平台侧 FAIL（整批跑不起来）err={errs[:1]}")
                # 同一数据集所有族共用字段与设置：前两批即 FAIL，后面必然同样 FAIL
                if n_fail >= 2 and not all_alphas:
                    print("  [abort] 前 2 批均 FAIL 且无任何结果 → 跳过本集剩余收割")
                    break
                continue
            elif rows and state != "ok":
                print(f"  [harvest] {tpl}_{bi} 部分收割 {len(rows)} 条（state={state}）")
            if not rows:
                print(f"  [harvest] {tpl}_{bi} 无结果（err={errs[:1]}）")
                for e in errs[:1]:
                    err_msgs.append(e)
                continue
            _absorb(rows, all_alphas, per_tpl, tpl)

        # ---------- 毒化自愈：整批 FAIL 的表达式剔除黑名单后重派一次（缺陷2）----------
        if failed_batches:
            rep = []
            for _t, _bi in failed_batches:
                fn = os.path.join(ROOT, "cache", f"_camp_{ds}_{_t}_{_bi}.txt")
                try:
                    rep += [(f"{_t}_rp", l.strip()) for l in open(fn, encoding="utf-8") if l.strip()]
                except Exception:
                    pass
            rep, _nbad = filter_bad(rep)
            if len(rep) < 2:
                print(f"  [repair] 剔除黑名单后仅 {len(rep)} 条（<2，空批风险），放弃重派")
            else:
                print(f"  [repair] {len(failed_batches)} 批失败 → 剔除 {_nbad} 条后重派 {len(rep)} 条")
                _key = ds + "@rp"
                _prev = [tuple(x) for x in (ck.get("sims", {}).get(_key) or []) if x and x[0]]
                if _prev:
                    _sims = _prev
                    print(f"  [repair] 复用已重派 {len(_sims)} 批")
                else:
                    def _persist_rp(pp, _k=_key):
                        ck["sims"][_k] = list(pp); save_ckpt(ck)
                    _sims = dispatch(rep, ds, "rp", on_batch=_persist_rp)
                    ck["sims"][_key] = _sims
                    save_ckpt(ck)
                for _sid, _t2, _b2 in _sims:
                    if not _sid:
                        continue
                    _rows, _errs, _st = harvest_until_done(_sid, ds, tag=f"rp_{_b2}")
                    note_bad_tokens(_errs)
                    _absorb(_rows, all_alphas, per_tpl, _t2)

        # ---------- 阶段 1.5：残差化族（returns 对字段回归取残差）----------
        # IND 唯一被证实能过 prod 墙的配方（institutions6 wave232 10/10 RA 全过）。
        # ⚠ 必须单独一批、用 decay=RESIDUAL_DECAY 派发：IND 基础 decay=4 复现不了实测。
        try:
            _res = build_residual(sel, cat=d.get("category"))
            if _res:
                _res_key = ds + "@res"
                _prev_res = [tuple(x) for x in (ck.get("sims", {}).get(_res_key) or [])
                             if x and x[0]]
                if _prev_res:
                    _res_sims = _prev_res
                    print(f"  [res] 复用已派发残差化 {len(_res_sims)} 批")
                else:
                    print(f"  [res] 残差化族 {len(_res)} 条（{len({t for t, _ in _res})} 族，"
                          f"decay={RESIDUAL_DECAY}）")

                    def _persist_res(partial, _k=_res_key):
                        ck["sims"][_k] = list(partial)
                        save_ckpt(ck)

                    _res_sims = dispatch(_res, ds, "res", on_batch=_persist_res,
                                         settings={"decay": RESIDUAL_DECAY})
                    ck["sims"][_res_key] = _res_sims
                    save_ckpt(ck)
                for _sid, _t, _b in _res_sims:
                    if not _sid:
                        continue
                    _rr, _re, _rs = harvest_until_done(_sid, ds, tag=f"res_{_b}")
                    note_bad_tokens(_re)
                    if not _rr:
                        print(f"  [res] {_t}_{_b} 无结果（state={_rs}，err={_re[:1]}）")
                        for _e in _re[:1]:
                            err_msgs.append(_e)
                        continue
                    _absorb(_rr, all_alphas, per_tpl, _t)
        except Exception as e:
            print(f"  [res] 异常，跳过：{type(e).__name__}: {e}")

        # ---------- 阶段 1.6：robust 几何族（短 bf + 固定 z + group/凸变换）----------
        # 2026-10-26：IND 的 ATOM 候选全部卡在 LOW_ROBUST_UNIVERSE_SHARPE（限值 1.0），
        # 而旧模板库 13 族的主派发（decay=4 + 季/年 backfill=252）结构上限实测只有 0.87–0.99。
        # 本族实测 robust 1.01–1.12，但 decay **按结构分档**（generate.ROBUST_DECAY_BY_TPL）：
        #   z/rank/dev → 10、居中凸 rg_grdev_p3* → 6、rg_lvvol* → 2
        # 旧实现全局 decay=10 ⇒ 凸族与 lvvol 族跑的是未验证设置（两颗全闸成品复现不出来）。
        # 按档分组派发：同档的族仍合并成同批，**不增加批数**。
        try:
            _rg = build_robust_geom(sel, ds=ds, cat=d.get("category"))
            if _rg:
                _rg_by_dec = collections.defaultdict(list)
                for _t, _e in _rg:
                    _rg_by_dec[robust_decay(_t)].append((_t, _e))
                _rg_sims = []
                for _dec in sorted(_rg_by_dec):
                    _grp = _rg_by_dec[_dec]
                    _rg_key = f"{ds}@rg_d{_dec}"
                    _prev_rg = [tuple(x) for x in (ck.get("sims", {}).get(_rg_key) or [])
                                if x and x[0]]
                    if _prev_rg:
                        print(f"  [rg] decay={_dec}: 复用已派发 {len(_prev_rg)} 批")
                        _rg_sims += _prev_rg
                        continue
                    print(f"  [rg] decay={_dec}: 稳健几何族 {len(_grp)} 条"
                          f"（{len({t for t, _ in _grp})} 族，bf={RG_BF} zw={RG_ZW}）")

                    def _persist_rg(partial, _k=_rg_key):
                        ck["sims"][_k] = list(partial)
                        save_ckpt(ck)

                    _s = dispatch(_grp, ds, f"rg_d{_dec}", on_batch=_persist_rg,
                                  settings={"decay": _dec})
                    ck["sims"][_rg_key] = _s
                    save_ckpt(ck)
                    _rg_sims += _s
                for _sid, _t, _b in _rg_sims:
                    if not _sid:
                        continue
                    _rr, _re, _rs = harvest_until_done(_sid, ds, tag=f"rg_{_t}_{_b}")
                    note_bad_tokens(_re)
                    if not _rr:
                        print(f"  [rg] {_t}_{_b} 无结果（state={_rs}，err={_re[:1]}）")
                        for _e in _re[:1]:
                            err_msgs.append(_e)
                        continue
                    _absorb(_rr, all_alphas, per_tpl, _t)
        except Exception as e:
            print(f"  [rg] 异常，跳过：{type(e).__name__}: {e}")

        best = {}
        max_s = -9
        max_2y = -9
        for tpl, lst in per_tpl.items():
            ms = max((x[1] for x in lst), default=None)
            m2 = max((x[2] for x in lst), default=None)
            best[tpl] = {"max_s": ms, "max_2y": m2}
            if ms is not None:
                max_s = max(max_s, ms)
            if m2 is not None:
                max_2y = max(max_2y, m2)

        # ---------------- 阶段 2：后处理电池（对 S≥0.8 的 top3 构造）----------------
        # ⚠ 排除 robust 几何族：它的验证点是 decay=10，而本电池按区域缺省 decay=4 派发，
        #   跑出来的 pp 变体与 rg 原式不可比（robust 会掉），白占槽位。
        tops = sorted((a for a in all_alphas
                       if a["s"] is not None and a.get("tpl") not in ROBUST_TPL),
                      key=lambda a: -a["s"])[:3]
        tops = [a for a in tops if a["s"] >= 0.8]
        if tops:
            print(f"  [stage2] 后处理电池：top{len(tops)} 构造 × 5 变体")
            codes = fetch_codes([a["alpha"] for a in tops])
            pp = []
            for a in tops:
                c = codes.get(a["alpha"])
                if c:
                    pp += build_postproc(c)
            if pp:
                pp_key = ds + "@pp"
                prev_pp = [tuple(x) for x in (ck.get("sims", {}).get(pp_key) or []) if x and x[0]]
                if prev_pp:
                    sims2 = prev_pp
                    print(f"  [resume] 复用已派发后处理 {len(sims2)} 批")
                else:
                    def _persist_pp(partial, _k=pp_key):
                        ck["sims"][_k] = list(partial)
                        save_ckpt(ck)

                    sims2 = dispatch(pp, ds, "pp", on_batch=_persist_pp)
                    ck["sims"][pp_key] = sims2
                    save_ckpt(ck)
                for sim_id, tpl, bi in sims2:
                    if not sim_id:
                        continue
                    rows, errs, state = harvest_until_done(sim_id, ds, tag=f"pp_{bi}")
                    if state == "empty":
                        print(f"  [harvest] {tpl}_{bi} COMPLETE children=0（结构性空批），放弃")
                    elif rows and state != "ok":
                        print(f"  [harvest] {tpl}_{bi} 部分收割 {len(rows)} 条（state={state}）")
                    if not rows:
                        continue
                    _absorb(rows, all_alphas, per_tpl, tpl)
                # 阶段2后重算 per-template best
                for tpl, lst in per_tpl.items():
                    best[tpl] = {"max_s": max((x[1] for x in lst), default=None),
                                 "max_2y": max((x[2] for x in lst), default=None)}
                max_s = max((b["max_s"] for b in best.values() if b["max_s"] is not None), default=max_s)
                max_2y = max((b["max_2y"] for b in best.values() if b["max_2y"] is not None), default=max_2y)

        # ---------- 载体结构扩散：本集最强族补跑未覆盖的 probe 字段 ----------
        try:
            _cx = carrier_expand(ds, sel, best, freq, ck, len(best))
            for _sid, _tc, _bc in _cx:
                if not _sid:
                    continue
                _rows, _errs, _st = harvest_until_done(_sid, ds, tag=f"cx_{_bc}")
                note_bad_tokens(_errs)
                _absorb(_rows, all_alphas, per_tpl, _tc)
            if _cx:
                for tpl_n, lst in per_tpl.items():
                    best[tpl_n] = {"max_s": max((x[1] for x in lst), default=None),
                                   "max_2y": max((x[2] for x in lst if x[2] is not None), default=None)}
                max_s = max((b["max_s"] for b in best.values() if b["max_s"] is not None), default=max_s)
                max_2y = max((b["max_2y"] for b in best.values() if b["max_2y"] is not None), default=max_2y)
        except Exception as e:
            print(f"  [carrier] 异常，跳过：{type(e).__name__}: {e}")

        # ---------- 字段 × 族 覆盖矩阵（审计：哪些格子从没跑过）----------
        field_cov = {}
        try:
            _names = [r["field_name"] for r in sel]
            _all_tpl = {t for t, _ in FAMILIES} | {"dw", "pp"} | set(RESIDUAL_TPL) | set(ROBUST_TPL)
            _cov = batch_field_coverage(ds, _names)
            field_cov = {f: sorted(v) for f, v in _cov.items()}
            _cells = sum(len(set(v) & _all_tpl) for v in _cov.values())
            _tot = len(_names) * len(_all_tpl)
            _untested = [f for f in _names if len(set(_cov.get(f, set())) & _all_tpl) < 3]
            print(f"  [matrix] 字段 {len(_names)} × 族 {len(_all_tpl)} → 覆盖 {_cells}/{_tot} 格"
                  + (f"；薄覆盖字段 {len(_untested)} 个: {_untested[:5]}" if _untested else ""))
        except Exception as e:
            print(f"  [matrix] 统计失败：{type(e).__name__}: {e}")

        # ---------- 阶段 1.7：负向强信号镜像（P0-2）----------
        # 放在 matrix 之后、joint 之前：① matrix 的逐族覆盖按 `cache/_camp_*` 扫文件，
        # 先跑镜像会让 `*_neg` 混进覆盖统计；② 镜像行只进 `neg` 块，**不进 all_alphas**，
        # 所以下面 joint / near_gate / pick_prod_target / settings_sweep 全自动保持正向口径。
        neg = {}
        try:
            neg = run_neg_mirror(ds, all_alphas, ck, _G2Y, _GSUB, _GROB)
        except Exception as e:
            print(f"  [neg] 异常，跳过：{type(e).__name__}: {e}")
            neg = {}

        # 联合判定：S 与 2Y 必须同时过闸（旧版只看 max_S，会把 2Y=0 的假阳性判 ALIVE）
        # 联合判据含 F（2026-10-21 用户指出）：S≥1.5 且 F≥1.0 且 2Y≥1.58
        joint = [a for a in all_alphas if (a["s"] or 0) >= 1.5
                 and (a.get("f") or 0) >= 1.0 and (a["y2"] or 0) >= _G2Y
                 and (_GSUB is None or (a.get("sub") or 0) >= _GSUB)]
        # 近闸（IND 口径）：S 已过 1.58 + F≥1.0 + 2Y/sub 过线 ⇒ 只差稳健宇宙与相关性
        near_gate = [a for a in all_alphas if (a["s"] or 0) >= 1.58
                     and (a.get("f") or 0) >= 1.0 and (a["y2"] or 0) >= _G2Y
                     and (_GSUB is None or (a.get("sub") or 0) >= _GSUB)]
        n_unknown = sum(1 for e in err_msgs if "unknown variable" in e.lower())

        # ---------- 缺陷1修复：近闸集（1.2<=S<1.58）自动扫设置轴 ----------
        sweep = {}
        try:
            max_s, sweep = settings_sweep(ds, all_alphas, ck, res, max_s,
                                          cat=d.get("category"))
            if sweep:
                ys = [v["max_2y"] for v in sweep.values() if v.get("max_2y") is not None]
                if ys:
                    max_2y = max([max_2y] + ys)
                joint = [a for a in all_alphas if (a["s"] or 0) >= 1.5
                         and (a.get("f") or 0) >= 1.0 and (a["y2"] or 0) >= _G2Y
                         and (_GSUB is None or (a.get("sub") or 0) >= _GSUB)]
                pt = collections.defaultdict(list)
                for a in all_alphas:
                    if a.get("s") is not None:
                        pt[a["tpl"]].append((a["alpha"], a["s"], a.get("y2"), a.get("sub")))
                for tpl_n, lst in pt.items():
                    best[tpl_n] = {"max_s": max((x[1] for x in lst), default=None),
                                   "max_2y": max((x[2] for x in lst if x[2] is not None), default=None)}
        except Exception as e:
            print(f"  [sweep] 异常，跳过：{type(e).__name__}: {e}")

        # 近闸/入闸候选测 prod（死局预警：S 高但 prod 高 = 白挖）。
        # 只对 max_S>=1.2 的集测最优那颗，避免无谓占用 prod 异步队列。
        prod_top = None
        # 2026-10-26：IND 优先选「含 robust 全闸已过」的最高 S（见 pick_prod_target）；
        # 其余区域（_GROB=None）仍是裸 max S，一行不变。
        best_alpha = pick_prod_target(all_alphas, _G2Y, _GSUB, _GROB) if all_alphas else None
        yp = None
        # 2026-10-24 用户指出：阈值 1.4 高于 prod 的 1.2，导致 max_s∈[1.2,1.4) 的近闸集
        # 完全跳过年度画像 ⇒ yp=None ⇒ 下面 `not (yp and yp.get("fragile"))` 恒真，
        # **fragile 一票否决被静默绕过**，digest 里永远是 frag=?。
        # 实例：quant_factor_lib（max_s=1.33）实际 first_year=2020、n_years=4、late_start=True ⇒ fragile，
        #       却在没有画像的情况下被判 BORDERLINE，随后被拿去做定向破闸（整轮无效）。
        # ⇒ 阈值对齐 near.sharpe_min = 1.2（与 prod 检测同档）：凡值得看 prod 的集，就必须看逐年画像。
        if best_alpha is not None and max_s >= 1.2:
            try:
                yp = year_profile(best_alpha["alpha"])
                if yp:
                    print(f"  [year] {best_alpha['alpha']} 首个持仓年 {yp['first_year']}"
                          f"（起点 {yp['start_year']}）｜有效 {yp['n_years']} 年｜"
                          f"单年集中 {yp['top_share']:.0%}（{yp['top_year']}）｜"
                          f"剔除后年均 {yp['ex_top_ret']:+.1%}"
                          + ("  ✗ FRAGILE" if yp["fragile"] else "  ✓"))
            except Exception as e:
                print(f"  [year] 画像失败：{type(e).__name__}: {e}")

        # 2026-10-25 用户要求：**十年都要有数据**。year_profile 只在 max_s>=1.2 时算，
        # 故只否决「本可评 ALIVE/BORDERLINE」的集；DEAD 不受影响。
        ten_ok = None   # None = 未验证（year_profile 缺失）
        if require_ten_years and yp:
            ten_ok = (yp.get("n_years", 0) >= 10
                      and yp.get("first_year", 9999) <= yp.get("start_year", 0))
            if not ten_ok:
                print(f"  [10y] ✗ 不满足十年数据：仅 {yp.get('n_years')} 年有持仓"
                      f"（首年 {yp.get('first_year')}，起点 {yp.get('start_year')}）"
                      f"｜单年集中 {yp.get('top_share', 0):.0%}")
            else:
                print(f"  [10y] ✓ 十年齐备（{yp.get('n_years')} 年，首年 {yp.get('first_year')}）")
        elif require_ten_years and (joint or max_s >= 1.3):
            print("  [10y] ⚠ 年度画像缺失，无法验证十年数据（保留原 verdict，结果里 ten_years=None）")

        # 近闸/入闸候选测 prod（死局预警：S 高但 prod 高 = 白挖）。
        # 十年闸先判：已被十年数据否决的候选 prod 不影响 verdict，不必占用平台
        # 异步相关队列（2026-10-25 事故：gJWlvd0v 被 [10y] 否决，却仍进 check_prod，
        # 卡在 412 轮询上近 1 小时，整个 campaign 停在 option1 不动）。
        if best_alpha is not None and max_s >= 1.2 and not (require_ten_years and ten_ok is False):
            print(f"  [prod] 测最优候选 {best_alpha['alpha']}（S={best_alpha['s']}）的 prod 相关性…")
            prod_top = check_prod(best_alpha["alpha"])
            if prod_top is not None:
                tag = "✗ prod>0.7 死局" if prod_top >= 0.7 else "✓ prod 过线"
                print(f"  [prod] {best_alpha['alpha']} prod={prod_top:.3f} {tag}")
        elif best_alpha is not None and max_s >= 1.2:
            print(f"  [prod] 跳过 {best_alpha['alpha']}：十年数据闸已否决，prod 不再影响 verdict")

        # 镜像的可行动状态：指标全过 + 没被换手拦（TO>0.4 的 ATOM 过不了平台 HIGH_TURNOVER）
        _neg_live = [r for r in (neg.get("mirrors") or [])
                     if r.get("joint") and not r.get("turnover_blocked")]
        if neg:
            neg["actionable"] = [r["alpha"] for r in _neg_live]

        verdict = decide_verdict(
            bool(all_alphas), n_fail, err_msgs,
            bool(require_ten_years and ten_ok is False),
            joint, _neg_live, max_s, neg.get("n_strong"))

        # ---------- 缺陷5修复：verdict 之外给出逐闸距离 + 可交付标记 ----------
        def _gap(v, lim):
            if v is None:
                return None
            return round(max(0.0, lim - float(v)) / lim, 3)

        b_s = best_alpha["s"] if best_alpha else None
        b_f = best_alpha.get("f") if best_alpha else None
        b_y2 = best_alpha.get("y2") if best_alpha else (max_2y if max_2y > -9 else None)
        b_sub = best_alpha.get("sub") if best_alpha else None
        b_rob = _val(best_alpha.get("rob")) if best_alpha else None
        gates = {
            "S":    {"value": b_s, "limit": 1.58, "gap": _gap(b_s, 1.58)},
            "F":    {"value": b_f, "limit": 1.0, "gap": _gap(b_f, 1.0)},
            "2Y":   {"value": b_y2, "limit": _G2Y, "gap": _gap(b_y2, _G2Y)},
            "prod": {"value": prod_top, "limit": 0.7,
                     "gap": (None if prod_top is None else round(max(0.0, prod_top - 0.7), 3))},
        }
        if _GSUB is not None:     # IND：sub 是绝对闸（1.0），必须单列出来
            gates["sub"] = {"value": b_sub, "limit": _GSUB, "gap": _gap(b_sub, _GSUB)}
        if _GROB is not None:     # IND：robust 闸（限值固定 1.0）——ATOM 唯一的结构性墙
            gates["robust"] = {"value": b_rob, "limit": _GROB, "gap": _gap(b_rob, _GROB)}
        deliverable = bool(b_s and b_s >= 1.58 and (b_f or 0) >= 1.0
                           and (b_y2 or 0) >= _G2Y
                           and (_GSUB is None or (b_sub or 0) >= _GSUB)
                           and (_GROB is None or (b_rob or 0) >= _GROB)
                           and prod_top is not None and prod_top < 0.7
                           and not (yp and yp.get("fragile"))    # 年度画像脆弱 ⇒ 一票否决
                           and ten_ok is not False)              # 十年数据不足 ⇒ 不可交付（2026-10-25 用户要求）
        deliv_score = max([g["gap"] for g in gates.values() if g.get("gap") is not None] or [1.0])
        n_rob_clean = (sum(1 for a in all_alphas
                           if (_val(a.get("rob")) or 0) >= _GROB) if _GROB is not None else None)

        res["results"][ds] = {
            "coverage": cov, "n_fields": d["n_fields"], "n_sel": len(sel),
            "n_dims": len(set(x["dim"] for x in sel)), "freq": freq,
            "per_template": best, "max_s": round(max_s, 3) if max_s > -9 else None,
            "max_2y": round(max_2y, 3) if max_2y > -9 else None,
            "n_joint": len(joint), "n_alphas": len(all_alphas),
            "n_unknown_field_err": n_unknown, "n_fail_batches": n_fail,
            "prod_top": prod_top, "settings_sweep": sweep, "field_coverage": field_cov,
            "year_profile": yp,
            "gates": gates, "deliverable": deliverable, "deliv_score": deliv_score,
            # 2026-10-26：robust 口径留痕 —— target 就是 prod 实际测的那颗
            "target": (best_alpha or {}).get("alpha"),
            "n_robust_clean": n_rob_clean,
            "near_gate": near_gate[:10],      # IND 定向挖掘的输入（S/F/2Y/sub 已过，只差 robust+corr）
            "neg": neg,                       # P0-2 镜像块（不含在 alphas / max_s 里）
            "verdict": verdict, "alphas": all_alphas,
        }
        ck["done"].append(ds)
        save_ckpt(ck); save_results(res)
        sw_txt = ("  sweep=" + ",".join(f"{k}:{v['max_s']}" for k, v in (sweep or {}).items())
                  if sweep else "")
        rob_txt = (f"  robust={gates['robust']['value']}（过线 {n_rob_clean} 颗）"
                   if _GROB is not None else "")
        print(f"  → verdict={verdict}  max_S={max_s:.2f}  max_2Y={max_2y:.2f}  "
              f"joint(S>=1.5&2Y>=1.58)={len(joint)}  n_alphas={len(all_alphas)}  "
              f"unknown_field_err={n_unknown}  deliv={deliverable}"
              f"(score={deliv_score}){rob_txt}{sw_txt}")
        if neg and (neg.get("n_strong") or neg.get("mirrors")):
            print(f"     neg: n_strong={neg.get('n_strong')} min_s={neg.get('min_s')} "
                  f"mirrors={len(neg.get('mirrors') or [])} joint={neg.get('joint')} "
                  f"TO_blocked={neg.get('turnover_blocked')} prod={neg.get('prod_top')}"
                  + (f" 行动项={neg.get('actionable')}" if neg.get("actionable") else ""))
        for tpl, b in sorted(best.items(), key=lambda kv: -(kv[1]["max_s"] or -9)):
            print(f"     {tpl:3s}  S={b['max_s'] if b['max_s'] is not None else '—'}  2Y={b['max_2y'] if b['max_2y'] is not None else '—'}")
        beat(ds, note="dataset-done")
        emit_digest(ds, d["category"], res, ck, len(ds_list))

    print(f"\n[campaign] 本轮完成，累计 {len(ck['done'])}/{len(ds_list)}")
