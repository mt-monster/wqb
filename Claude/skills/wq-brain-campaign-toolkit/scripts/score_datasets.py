# -*- coding: utf-8 -*-
"""score_datasets.py - 数据集自动评分 + 探针电池接线（三模式）。

1) 评分（默认）:
   python score_datasets.py --campaign-dir <DIR>
     直连 get_datasets 全量评分（自动排除台账 *_dead），写 reference/<region>_dataset_ranking.json
2) 探针计划（生成不提交）:
   python score_datasets.py --campaign-dir <DIR> --probe-plan behavioral_signals [--fields 6]
     读 typed catalog（缺则自动 scan_fields），按 8 探针模板两段式生成批次，落 candidates/probe_<ds>_exprs.json
3) 探针评分（评审回测结果）:
   python score_datasets.py --campaign-dir <DIR> --probe-score <multisim_id> [--dataset <ds>] [--stage A] [--mark-dead]
   python score_datasets.py --campaign-dir <DIR> --probe-score x --from-json <指标JSON lines文件>  # 离线校准
     按 v2 三灯公式判定 绿灯/黄灯/红灯，红灯可一键记 *_dead 台账
"""
import argparse
import datetime
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, atomic_write, load_credentials,
                         load_json, load_platform_constraints)
from _lib.api import Api
from _lib.ledger import LedgerStore, make_ledger_store, today
from _lib.wqb_store import load_ranking, save_ranking, load_catalog, save_catalog
import metrics_cache
import scan_fields

PAGE = 50


# ---------------- 数据集自动评分 ----------------

def fetch_all_datasets(api, settings):
    base = ("/data-sets?instrumentType={instrumentType}&region={region}"
            "&delay={delay}&universe={universe}&limit={pg}").format(pg=PAGE, **settings)
    out, offset = [], 0
    while True:
        j = json.load(api.get(f"{base}&offset={offset}"))
        rs = j.get("results", [])
        out.extend(rs)
        offset += len(rs)
        if not rs or offset >= j.get("count", 0):
            return out


def usable_fields(ctx, dataset_id, raw_fc):
    """P3 可用字段精修：已建 typed catalog 的数据集，用目录内 coverage>=0.85 的字段数
    代替原始 fieldCount（原始值把稀疏字段也算进广度，高估可挖空间）；无目录则回退原始值。"""
    cat = ctx.catalog_path(dataset_id)
    if os.path.exists(cat):
        try:
            d = load_json(cat)
            n = sum(1 for f in d.get("fields", []) if (f.get("coverage") or 0) >= 0.85)
            if n:
                return n, "catalog"
        except Exception:
            pass
    return raw_fc, "raw"


def crowd_penalty(ac, h=None):
    """P5 拥挤分段罚：ac<=50 满分 0.30；50→500 线性降至 0.15；500→5000 线性降至 0.02；>5000 恒 0.02。
    替代 1/(1+log10(1+ac))：原式 ac=0→ac=1e4 仅降 0.25 分，被 0.4*cov 权重淹没，
    超拥挤集（USA 实测 analyst15 ac=102072 靠 cov≈1 进 tier1）挤占白名单，2026-08-16 走查修订。

    O7 甜区反转（opt-in，h.crowd_sweet_spot_enable=True 时生效，EUR+GBR 双战役实证）：
      默认假设"零竞争=高价值"被证伪——ac<50 的零竞争集几乎全是伪白空间（无信号），
      真正强信号集中在 ac 50-1000 甜区（EUR mha91/si6_151/aea183→2.5/2.0/2.0；GBR starmine686→1.84）。
      甜区模式：ac<50→0.15（零竞争降权）；50<=ac<=1000→0.30（甜区满分）；ac>1000→0.02（红海）。
    """
    h = h or {}
    if h.get("crowd_sweet_spot_enable", False):
        lo = h.get("sweet_spot_ac_min", 50)
        hi = h.get("sweet_spot_ac_max", 1000)
        if ac < lo:
            return h.get("sweet_spot_low_penalty", 0.15)   # 零竞争降权（伪白空间）
        if ac <= hi:
            return h.get("sweet_spot_full", 0.30)          # 甜区满分
        return 0.02                                        # 红海
    # 默认（向后兼容）：原分段罚
    if ac <= 50:
        return 0.30
    if ac <= 500:
        return 0.30 - 0.15 * (ac - 50) / 450.0
    if ac <= 5000:
        return 0.15 - 0.13 * (ac - 500) / 4500.0
    return 0.02


def category_weight(ds, h):
    """O8 category 信号含量加权（opt-in，h.category_weight_enable=True 时生效，EUR+GBR 实证）。

    双战役一致实证：category=model（预训练模型因子）是强信号富矿——
      EUR 4 个强信号集全在 model 类（max2.54/avg1.46）；GBR 唯一强信号 starmine 也在 model 类。
    原始字段类（news/pv/analyst/sentiment/other）几乎全弱。
    权重由 h.category_weights dict 提供（按 region 实测校准），缺省类别乘 1.0（中性）。
    返回乘性因子（叠加在 score 上）。
    """
    if not h.get("category_weight_enable", False):
        return 1.0
    weights = h.get("category_weights", {})
    cat = ds.get("category")
    if isinstance(cat, dict):
        cat = cat.get("id")
    raw = float(weights.get(cat, 1.0))
    lo = float(h.get("category_weight_floor") or 0.9)
    hi = float(h.get("category_weight_cap") or 1.15)
    raw = max(raw, lo)
    raw = min(raw, hi)
    return raw


def score(ds, fc, h=None):
    """连续评分：cov 0.4 + 低拥挤 0.3（P5 分段罚）+ 广度 0.2 + valueScore 0.1，再乘 category 加权（O8）。
    alphaCount 拥挤度只在 score 里软罚（P1）；tier 硬闸见 tier_threshold/assign_quantile_tiers。
    h 为 dataset_health 配置（None 时全默认，行为与旧版一致）。"""
    h = h or {}
    cov = ds.get("coverage") or 0
    ac = ds.get("alphaCount") or 0
    vs = ds.get("valueScore")
    breadth = min(math.log1p(fc) / math.log1p(1000), 1.0)  # clamp：fc>1000 时原式会 >1
    base = (0.40 * cov
            + crowd_penalty(ac, h)
            + 0.20 * breadth
            + 0.10 * (min(vs, 10) / 10.0 if vs is not None else 0.5))  # 缺失取中性 0.5
    return base * category_weight(ds, h)


def backfill_band(r, h):
    """O2 中覆盖回填带：0.65<=cov<0.85 & ac<=50 & vs>=6 → 保底 tier2。
    KOR/USA 双战役两次踩中的盲区（中覆盖带藏低竞争高价值集）；分位制仍会漏
    （USA 实测 event_sentiment_signals cov0.719/ac39/vs6 被分位线挤出）。
    生成侧必须 ts_backfill(66/120) 包裹字段补偿覆盖缺口。"""
    return (h.get("backfill_band_enable", True)
            and h.get("backfill_band_cov_min", 0.65) <= (r["coverage"] or 0) < h.get("backfill_band_cov_max", 0.85)
            and (r["alphaCount"] or 0) <= h.get("backfill_band_alpha_count_max", 50)
            and (r["valueScore"] or 0) >= h.get("backfill_band_value_score_min", 6))


def micro_probe_exception(r, h):
    """O4 微型集探针例外：cov>=0.9 & ac==0 & vs>=6 但字段数<硬地板 → 不硬杀，保底 tier2。
    仅允许走 Stage A 探针早停（成本 1 批）；探针非 EARLY RED 才可转正式挖掘。"""
    return (h.get("probe_exception_enable", True)
            and (r["coverage"] or 0) >= h.get("probe_exception_cov_min", 0.9)
            and (r["alphaCount"] or 0) == 0
            and (r["valueScore"] or 0) >= h.get("probe_exception_value_score_min", 6))


def crowd_veto(ac, h):
    """O5 拥挤一票否决（opt-in）：alphaCount > alpha_count_max → 直接 excluded。
    GBR 2026-08-17：原 alphaCount<=100 硬闸过保守（把 predictive_starmine ac=686 实测 Sh1.80 族挡在池外），
    放宽为 <=alpha_count_max(1000) 准入，>1000 的绝对红线不变。默认关闭，其它战役不受影响。"""
    return (h.get("crowd_veto_enable", False)
            and (ac or 0) > h.get("alpha_count_max", 1000))


def crowd_band(r, h):
    """O6 强信号拥挤带（opt-in）：alphaCount 超原 100 硬闸但 <=alpha_count_max 的强信号集保底 tier2。
    GBR 2026-08-17 放宽门闩引入：predictive_starmine(ac=686)/shortinterest3(ac=294) 等被分位线挤出。
    生成侧义务：cov<crowd_band_cov_max(0.85) 时字段必须 ts_backfill(66/120) 包裹（tier_note=crowd_band）。"""
    return (h.get("crowd_band_enable", False)
            and h.get("crowd_band_alpha_count_min", 100) < (r["alphaCount"] or 0) <= h.get("alpha_count_max", 1000)
            and (r["coverage"] or 0) >= h.get("crowd_band_cov_min", 0.7)
            and (r["valueScore"] or 0) >= h.get("crowd_band_value_score_min", 4)
            and (r.get("usableFieldCount") or 0) >= h.get("crowd_band_field_count_min", 10))


def apply_floor_tiers(rows, h):
    """O2/O4/O6 保底带统一接线（quantile/threshold 两法共用）：只升不降，附 tier_note 溯源。"""
    for r in rows:
        if r.get("tier") != "excluded":
            continue
        if not r.get("hard_excluded") and backfill_band(r, h):
            r["tier"], r["tier_note"] = "tier2", "backfill_band"
        elif not r.get("hard_excluded") and crowd_band(r, h):
            r["tier"], r["tier_note"] = "tier2", "crowd_band"
        elif r.get("hard_excluded") and micro_probe_exception(r, h):
            r["tier"], r["tier_note"] = "tier2", "probe_exception"


def apply_pyramid_quota(rows, h):
    """Keep at least N non-MODEL datasets in tier1 so category_weight cannot wipe PV/NEWS/ANALYST.

    Opt-in: h.pyramid_quota_enable. Promotes highest-score non-model rows that are
    not hard_excluded / dead. Tags tier_note=pyramid_quota (or appends).
    """
    if not h.get("pyramid_quota_enable", True):
        return 0
    need = int(h.get("pyramid_quota_non_model_min", 2))

    def cat(r):
        return str(r.get("category") or "").lower()

    def is_non_model(r):
        c = cat(r)
        return bool(c) and c != "model" and not r.get("hard_excluded") and not r.get("dead")

    have = sum(1 for r in rows if r.get("tier") == "tier1" and is_non_model(r))
    if have >= need:
        return 0
    pool = [r for r in rows if is_non_model(r) and r.get("tier") != "tier1"]
    pool.sort(key=lambda r: -(r.get("score") or 0))
    promoted = 0
    for r in pool:
        if have >= need:
            break
        r["tier"] = "tier1"
        note = r.get("tier_note")
        r["tier_note"] = (str(note) + "+pyramid_quota") if note else "pyramid_quota"
        have += 1
        promoted += 1
    return promoted


def hard_excluded(cov, fc, h):
    """excluded 硬地板（与模式无关）：数据可用性绝对底线。P0：coverage_hard_min/field_count_hard_min 真正接线。"""
    return cov < h.get("coverage_hard_min", 0.7) or fc < h.get("field_count_hard_min", 5)


def tier_threshold(cov, ac, fc, h, mode):
    """固定阈值法（回退路径，tier_method=threshold）。
    P1：mode=general 时 alphaCount 不进硬闸（拥挤度交给 score 软罚）；mode=ppa 保留白空间硬闸。
    O5：crowd_veto 一票否决两模式通用（opt-in）。"""
    if hard_excluded(cov, fc, h) or crowd_veto(ac, h):
        return "excluded"
    ppa = mode == "ppa"
    if (cov >= h["coverage_min"] and fc >= h["field_count_min"]
            and (not ppa or ac <= h["alpha_count_max"])):
        return "tier1"
    if (cov >= h.get("tier2_coverage_min", 0.85) and fc >= h.get("tier2_field_count_min", 5)
            and (not ppa or ac <= h.get("tier2_alpha_count_max", 200))):
        return "tier2"
    return "excluded"


def assign_quantile_tiers(rows, h, mode):
    """P2+P4：非硬排除者按 score 分位分带（分位在本区域数据集分布内计算 → 天然区域自适应，
    消固定阈值悬崖；排名与分层同源）。mode=ppa 额外：tier1 中拥挤超标者降 tier2。"""
    alive = [r for r in rows if not r["hard_excluded"]]
    scores = sorted(r["score"] for r in alive)
    if not scores:
        for r in rows:
            r["tier"] = "excluded"
        return
    n = len(scores)
    t1_bar = scores[min(n - 1, int(h.get("tier1_score_pct", 0.6) * n))]
    t2_bar = scores[min(n - 1, int(h.get("tier2_score_pct", 0.3) * n))]
    ac_max = h.get("alpha_count_max", 50)
    for r in rows:
        if r["hard_excluded"] or crowd_veto(r["alphaCount"], h):
            r["tier"] = "excluded"
            continue
        t = "tier1" if r["score"] >= t1_bar else ("tier2" if r["score"] >= t2_bar else "excluded")
        if mode == "ppa" and t == "tier1" and (r["alphaCount"] or 0) > ac_max:
            t = "tier2"  # PPA 白空间硬规则仅在 ppa 模式生效
        r["tier"] = t


def apply_pyramid_exclusion(rows, h, region, delay):
    """O9 指定 pyramid/catalog 排除（2026-09-01）：excluded_pyramids 列表命中者降 excluded。
    pyramid 命名 = {REGION}_D{delay}_{category}（如 IND_D1_other），也接受裸 category（如 "risk"，
    全 delay 生效）。须在 assign_quantile_tiers/tier_threshold 之后、apply_floor_tiers 之前执行，
    防止被排除项被保底带复活。"""
    excl = [str(x).lower() for x in (h.get("excluded_pyramids") or [])]
    if not excl:
        return 0
    region_lc, delay_s = str(region).lower(), str(delay)
    n = 0
    for r in rows:
        cat = (r.get("category") or "").lower()
        pyramid = f"{region_lc}_d{delay_s}_{cat}"
        hit = pyramid in excl or cat in excl
        if hit and r.get("tier") != "excluded":
            r["tier"] = "excluded"
            r["tier_note"] = "excluded_pyramid"
            n += 1
    return n


def cmd_score(ctx):
    e, pw = load_credentials()
    api = Api(); api.login(e, pw)
    dss = fetch_all_datasets(api, ctx.settings)
    ledger = make_ledger_store(ctx).load()
    dead = {k[:-5] for k in ledger if k.endswith("_dead")}
    h = ctx.thresh("dataset_health")
    mode = h.get("mode", "general")            # P1：general|ppa
    method = h.get("tier_method", "quantile")  # P2：quantile|threshold
    _region_lc = str(ctx.region).lower()
    _delay = str(ctx.settings.get("delay", 1))
    rows = []
    for ds in dss:
        did = ds.get("id")
        cov = ds.get("coverage") or 0
        fc, fc_src = usable_fields(ctx, did, ds.get("fieldCount") or 0)  # P3
        rows.append({
            "id": did, "score": round(score(ds, fc, h), 4),
            "coverage": ds.get("coverage"), "fieldCount": ds.get("fieldCount"),
            "usableFieldCount": fc, "fieldCount_src": fc_src,
            "alphaCount": ds.get("alphaCount"), "userCount": ds.get("userCount"),
            "valueScore": ds.get("valueScore"),
            "pyramidMultiplier": (ds.get("pyramidMultiplier") or {}).get("multiplier")
                if isinstance(ds.get("pyramidMultiplier"), dict) else ds.get("pyramidMultiplier"),
            "category": (ds.get("category") or {}).get("id") if isinstance(ds.get("category"), dict) else ds.get("category"),
            "dead": did in dead,
            "hard_excluded": hard_excluded(cov, fc, h),
        })
        rows[-1]["pyramid"] = f"{_region_lc}_d{_delay}_{(rows[-1].get('category') or '').lower()}"
    if method == "quantile":
        assign_quantile_tiers(rows, h, mode)
        tier_rule = (f"quantile: 非硬排除者按 score 分位分带 tier1>=P{int(h.get('tier1_score_pct',0.6)*100)} / "
                     f"tier2>=P{int(h.get('tier2_score_pct',0.3)*100)}（区域内自适应）；硬地板 cov<{h.get('coverage_hard_min',0.7)} "
                     f"或 usableFields<{h.get('field_count_hard_min',5)} → excluded；mode={mode}"
                     + ("（alphaCount<=alpha_count_max 硬闸）" if mode == "ppa" else "（alphaCount 仅 score 软罚）")
                     + (f"；crowd_veto: alphaCount>{h.get('alpha_count_max',1000)} 一票否决" if h.get("crowd_veto_enable") else ""))
    else:
        for r in rows:
            r["tier"] = tier_threshold(r["coverage"] or 0, r["alphaCount"] or 0,
                                       r["usableFieldCount"], h, mode)
        tier_rule = (f"threshold: tier1 cov>={h['coverage_min']} & fields>={h['field_count_min']}"
                     + (f" & alphaCount<={h['alpha_count_max']}" if mode == "ppa" else "")
                     + f"; tier2 cov>={h.get('tier2_coverage_min',0.85)} & fields>={h.get('tier2_field_count_min',5)}"
                     + (f" & alphaCount<={h.get('tier2_alpha_count_max',200)}" if mode == "ppa" else "")
                     + f"；mode={mode}")
    apply_pyramid_exclusion(rows, h, ctx.region, ctx.settings.get("delay", 1))  # O9：指定 pyramid 排除（保底带前执行防复活）
    apply_floor_tiers(rows, h)  # O2/O4 保底带（两法共用，只升不降）——须在写盘/统计前
    n_quota = apply_pyramid_quota(rows, h)
    n_pyx = sum(1 for r in rows if r.get("tier_note") == "excluded_pyramid")
    rows.sort(key=lambda r: -r["score"])
    alive = [r for r in rows if not r["dead"] and r["tier"] != "excluded"]
    # ---- 点塔视角排序（2026-09-01 优化A）：score 按信号强度优化，
    #      点塔战略按"未点亮类别优先"优化，两者错位是 S0a 手工筛选的根因。
    #      此视图不改 score/tier（信号分层语义保持），只附 pyramid_view：
    #      按 (类别点塔价值, score) 排序的候选清单，S0a 白名单实例化直接消费。
    pyr = pyramid_view(alive, h, ctx.region)
    payload = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "region": ctx.region, "universe": ctx.settings["universe"],
        "total": len(rows), "dead_excluded": len(dead),
        "mode": mode, "tier_method": method,
        "excluded_pyramids": h.get("excluded_pyramids") or [],
        "score_formula": ("0.4*cov + crowd_penalty(alphaCount)[分段: <=50→0.30, 500→0.15, >=5000→0.02] "
                          "+ 0.2*min(log1p(fc)/log1p(1000),1) + 0.1*valueScore/10"),
        "tier_rule": tier_rule + ("；保底带（O2/O4/O6，tier_note 溯源）：backfill_band(0.65<=cov<0.85 "
                                   "& alphaCount<=50 & valueScore>=6)→tier2[生成须 ts_backfill(66/120)]；"
                                   "probe_exception(cov>=0.9 & alphaCount==0 & valueScore>=6 & 字段<硬地板)→"
                                   "tier2[仅限 Stage A 探针早停]"
                                   + ("; crowd_band(alphaCount>100 & <=alpha_count_max & cov>=0.7 "
                                      "& valueScore>=4)→tier2[cov<0.85 生成须 ts_backfill]" if h.get("crowd_band_enable") else "")),
        "pyramid_view": pyr,
        "ranking": rows,
    }
    save_ranking(ctx, payload)
    n1 = sum(1 for r in rows if r["tier"] == "tier1")
    n2 = sum(1 for r in rows if r["tier"] == "tier2")
    n_band = sum(1 for r in rows if r.get("tier_note"))
    print(f"datasets={len(rows)} alive_ranked={len(alive)} (tier1={n1} tier2={n2} floor_band={n_band}"
          f"{f' pyramid_quota={n_quota}' if n_quota else ''}"
          f"{f' pyramid_excluded={n_pyx}' if n_pyx else ''}) "
          f"dead_skipped={len(dead)} mode={mode} method={method}")
    print(f"{'rank':>4} {'score':>7} {'tier':>5}  {'id':28s} cov/fields/alphas")
    for i, r in enumerate(alive[:20], 1):
        print(f"{i:>4} {r['score']:>7} {r['tier']:>5}  {r['id']:28s} "
              f"{r['coverage']}/{r['usableFieldCount']}/{r['alphaCount']}")
    print(f"ranking -> db ledger_kv/{ctx.region}/s0_ranking")

    # pyramid_view 已随 payload 落库；此处只打 stdout 视图
    if pyr:
        print(f"[pyramid-view] 点塔视角 top10（战略排序 ≠ 信号分榜，S0a 白名单从此列表取）:")
        for i, r in enumerate(pyr[:10], 1):
            print(f"  {i:>2} {r['id']:28s} cat={r.get('category','?'):13s} score={r['score']:.3f} "
                  f"pm={r.get('pyramidMultiplier','-')} reason={r.get('pyr_reason','')}")


def pyramid_view(alive_rows, h, region):
    """点塔视角排序：未点亮/低竞争类别优先 + score 平手决胜。

    数据源：datasets 表该 region 的 category 分布（饱和类别=alphaCount 高）+
    h.focus_categories（战役目标类别，如 KOR_REGULAR_20 的 Other/PV/Risk/ShortInterest）。
    只排序 alive_rows（已过死路/硬排除），不重复过滤逻辑。
    """
    focus = {c.strip().upper() for c in str(h.get("focus_categories", "") or "").split(",") if c.strip()}
    exclude = {c.strip().upper() for c in str(h.get("exclude_categories", "") or "").split(",") if c.strip()}
    out = []
    for r in alive_rows:
        cat = (r.get("category") or "").upper()
        if cat in exclude:
            continue
        # 点塔价值：目标类别 2 分（战略直指未点亮塔）；非 MODEL 非目标 1 分；MODEL 0 分（饱和方向）
        if cat in focus:
            v, reason = 2, "focus（战略目标类别）"
        elif cat and cat != "MODEL":
            v, reason = 1, "non-model（多样性加分）"
        else:
            v, reason = 0, "model（饱和方向，点塔价值低）"
        # 低拥挤加分（alphaCount<=200 的白空间）
        if (r.get("alphaCount") or 0) <= 200:
            v += 1
            reason += "+lowcrowd"
        out.append({**r, "pyr_value": v, "pyr_reason": reason})
    out.sort(key=lambda r: (-r["pyr_value"], -r["score"]))
    return out


# ---------------- 通用自学习校准：从实测回测自动校准筛选权重 ----------------

def _infer_ds_from_fname(fname, ds_field):
    """从 results 文件名/字段推断 dataset id（兼容 5slot_xxx_probe / waveN_xxx_results 命名）。"""
    if ds_field and ds_field != "?":
        return ds_field
    base = fname[:-5] if fname.endswith(".json") else fname
    for pat in (r"5slot_([a-z0-9_]+?)_(?:repair\d+_)?probe", r"5slot_([a-z0-9_]+?)_repair",
                r"wave\d+[a-z]?_([a-z0-9_]+?)_(?:results|probe)", r"([a-z0-9_]+?)_probe_results"):
        m = re.match(pat, base)
        if m:
            return m.group(1)
    return ds_field


def _build_field2ds(ctx, valid_ds):
    """从本战役 typed catalog 建 field -> set(dataset) 反查表（仅纳入 ranking 内合法 dataset）。
    用于校准器兜底识别无 dataset 键的 ad-hoc 结果文件。catalog 缺失的 dataset 自动跳过。"""
    field2ds = {}
    for ds in valid_ds:
        try:
            cat = load_catalog(ctx, ds)
        except Exception:
            cat = None
        if not cat:
            continue
        for f in cat.get("fields", []):
            fid = f.get("id")
            if fid:
                field2ds.setdefault(fid, set()).add(ds)
    return field2ds


# 校准用：表达式里的算子集合（字段反查时剔除）
_OPS_TOKENS = {
    "rank", "ts_rank", "ts_delta", "ts_zscore", "ts_backfill", "winsorize",
    "add", "multiply", "subtract", "divide", "group_rank", "ts_decay_linear",
    "signed_power", "vec_avg", "vec_sum", "vec_count", "ts_mean", "ts_std_dev",
    "ts_av_diff", "scale_down", "power", "log", "abs", "max", "min", "quantile",
    "ts_quantile", "clamp", "group_neutralize", "if_else", "greater", "less",
    "and", "or", "not", "ts_arg_max", "hump", "last_diff_value",
}


def _expr_fields(expr):
    """从 alpha 表达式提取字段 token（剔除算子与纯数字）。"""
    return [t for t in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expr or "")
            if t not in _OPS_TOKENS and not t.replace("_", "").isdigit()]


def _infer_alpha_dataset(expr, field2ds, valid_ds):
    """给单条 alpha 反推 dataset：①字段前缀特例(anl15_→analyst15) ②catalog 唯一字段反查多数票。"""
    fs = _expr_fields(expr)
    if any(f.startswith("anl15_") for f in fs):
        return "analyst15" if "analyst15" in valid_ds else None
    votes = {}
    for f in fs:
        hit = field2ds.get(f)
        if hit and len(hit) == 1:  # 字段唯一属于某 dataset 才算票（跨集共享字段不投票）
            d0 = next(iter(hit))
            votes[d0] = votes.get(d0, 0) + 1
    if votes:
        ds = max(votes.items(), key=lambda kv: kv[1])[0]
        return ds if ds in valid_ds else None
    return None


def _collect_from_alpha_store(ctx, valid_ds, field2ds):
    """从 DB alpha 存储采集实测回测（校准主源）。

    背景（USA 2026-08-27 实证）：results/*.json 扫描只命中 4 个数据集——
    ① pipeline checkpoint 的 results 嵌在 batches[].alphas 且文件名含 'checkpoint' 被跳过；
    ② expressions 表 sharpe 列全 NULL（指标从未回写，只在 metrics 缓存）；
    ③ 部分 alpha 的 dataset 是历史恢复假名 recovered_ds_*（同一标号混多数据集）。
    而 alphas 表（list_alphas_by_region）直接带 sharpe/fitness/expression 且 sharpe 非空，
    是唯一可靠的实测源。dataset 用字段反查重归类（不信假名/excluded 状态——excluded 只代表拥挤，不代表没信号）。
    返回 dataset -> [sharpe,...]；采集失败/无数据返回 {}（调用方回退 results/ 扫描）。
    """
    from _lib.wqb_store import get_store
    try:
        store = get_store(ctx)
        try:
            rows = store.list_alphas_by_region(ctx.region)
        finally:
            try:
                store.close()
            except Exception:
                pass
    except Exception:
        return {}
    ds_sh = {}
    for r in rows:
        sh = r.get("sharpe")
        if not isinstance(sh, (int, float)):
            continue
        ds = _infer_alpha_dataset(r.get("expression"), field2ds, valid_ds)
        if ds:
            ds_sh.setdefault(ds, []).append(sh)
    return ds_sh


def calibrate_dataset_health(ctx, strong_bar=1.5, weak_bar=1.0, dry_run=False):
    """通用能力：扫描本战役 results/ 实测回测，自动校准 dataset_health 的筛选权重。

    任何 region 跑过回测后即可用——从"哪个 category / 哪个拥挤度区间真出强信号"反向学习，
    替代凭先验假设写死的权重。EUR+GBR 实证：model 类是富矿、ac<50 零竞争多是伪白空间。

    产出（写回 thresholds.json 的 dataset_health 节，幂等）：
      category_weight_enable=True + category_weights（按 category 实测表现映射到 [0.9,1.15]）
      category_weight_floor/cap 与 pyramid_quota_enable（防 MODEL 权重抹掉 PV/NEWS）
      crowd_sweet_spot_enable=True + sweet_spot_ac_min/max（按强信号集 ac 分布学习甜区）
    返回校准报告 dict。
    """
    import glob
    rdir = ctx.path("results")
    # dataset -> (category, ac) 映射（来自现有 ranking；无 ranking 则无法可靠校准，退化为空）
    cat_map = {}
    ac_map = {}
    valid_ds = set()
    valid_cats = set()
    rk = load_ranking(ctx)
    if not rk and os.path.exists(ctx.ranking_path()):
        rk = load_json(ctx.ranking_path())
    if rk:
        for r in rk.get("ranking", []):
            did = r.get("id")
            valid_ds.add(did)
            cat_map[did] = r.get("category")
            ac_map[did] = r.get("alphaCount")
            if r.get("category"):
                valid_cats.add(r.get("category"))
    # field -> dataset 反查表（从本战役 typed catalog 建；USA 实测 17097 字段零歧义）。
    # 用于兜底识别无 dataset 键的 ad-hoc 结果（USA 早期 results 命名不规范、结构非标准契约）。
    field2ds = _build_field2ds(ctx, valid_ds)

    # 主源：从 DB alpha 存储采集实测（list_alphas_by_region 直接带 sharpe，USA 214 条全可靠）。
    # results/ 扫描只命中 4 个数据集（checkpoint 跳过/expressions sharpe NULL/recovered_ds 假名），
    # alpha 存储才是唯一够到真实回测的源。
    alpha_store_sh = _collect_from_alpha_store(ctx, valid_ds, field2ds)

    def _resolve_ds(fn, ds_field, rows):
        """三级定位 dataset：①显式 dataset 键 ②文件名正则 ③field 反查 catalog。"""
        ds = _infer_ds_from_fname(fn, ds_field)
        if ds in valid_ds:
            return ds
        # ③兜底：多数行的 field 反查命中同一 dataset 即采纳
        votes = {}
        for r in rows:
            if isinstance(r, dict):
                fid = r.get("field") or r.get("field_id") or r.get("id")
                hit = field2ds.get(fid)
                if hit and len(hit) == 1:
                    d0 = next(iter(hit))
                    votes[d0] = votes.get(d0, 0) + 1
        if votes:
            best_ds, n = max(votes.items(), key=lambda kv: kv[1])
            if n >= max(1, len(votes) // 1) and best_ds in valid_ds:
                return best_ds
        return ds

    def _rows_from(d):
        """统一从三种格式提取 (rows, sharpe键名)。返回含 sharpe 的 dict 行列表。
        格式A {dataset,results:[...]}；格式B 顶层 list[{field,sharpe,...}]；
        格式C dict 以 alpha_id/expr 为 key、值为含 sharpe 的 dict（USA ad-hoc）。"""
        if isinstance(d, list):
            return [r for r in d if isinstance(r, dict)]
        if isinstance(d, dict):
            res = d.get("results") or d.get("all")
            if isinstance(res, list):
                return [r for r in res if isinstance(r, dict)]
            # 格式C：值是含 sharpe 的 dict
            out = []
            for k, v in d.items():
                if isinstance(v, dict) and isinstance(v.get("sharpe"), (int, float)):
                    vv = dict(v); vv.setdefault("field", v.get("field") or v.get("field_id"))
                    out.append(vv)
            return out
        return []

    # 聚合 dataset -> best_sh（只采纳 ranking 里真实存在的 dataset，过滤复合名/文件名误推断）
    ds_best = {}
    for fp in sorted(glob.glob(os.path.join(rdir, "*.json"))):
        fn = os.path.basename(fp)
        if "checkpoint" in fn or fn.startswith("_"):
            continue
        try:
            d = load_json(fp)
        except Exception:
            continue
        if not isinstance(d, (dict, list)):
            continue
        rows = _rows_from(d)
        if not rows:
            continue
        ds = _resolve_ds(fn, d.get("dataset") if isinstance(d, dict) else None, rows)
        # 只采纳 ranking 里真实存在的 dataset id（复合 dataset 名/缩写/误推断一律跳过）
        if not ds or ds not in valid_ds:
            continue
        shs = [r.get("sharpe") for r in rows
               if isinstance(r, dict) and isinstance(r.get("sharpe"), (int, float))]
        if not shs:
            continue
        cur = ds_best.setdefault(ds, {"best_sh": 0.0})
        cur["best_sh"] = max(cur["best_sh"], max(shs))
    # 合并 alpha 存储主源（与 results/ 扫描取并集，同一 dataset 取更大 best_sh）
    for ds, shs in alpha_store_sh.items():
        if not shs:
            continue
        cur = ds_best.setdefault(ds, {"best_sh": 0.0})
        cur["best_sh"] = max(cur["best_sh"], max(shs))
    # 补 ac / category（仅用 ranking 合法值）
    for ds, cur in ds_best.items():
        cur["ac"] = ac_map.get(ds)
        c = cat_map.get(ds)
        cur["category"] = c if c in valid_cats else None

    # 按 category 聚合实测表现（category 缺失/不合法的 dataset 不参与 category 权重，但仍计入甜区）
    cat_perf = {}
    for ds, cur in ds_best.items():
        c = cur.get("category")
        if not c:
            continue
        cat_perf.setdefault(c, []).append(cur["best_sh"])
    # category -> 权重：封顶 1.15 / 地板 0.9（src/wqb.config.MINING）。
    # 禁止再映射到 1.3 vs 0.7：EUR Wave35–40 实证这会把 PV/NEWS 整座金字塔挤出 tier1。
    weights = {}
    for c, shs in cat_perf.items():
        mx = max(shs)
        if mx >= strong_bar:
            weights[c] = 1.15
        elif mx >= weak_bar:
            weights[c] = 1.0
        else:
            weights[c] = 0.9
    # 甜区：强信号集(best_sh>=strong_bar)的 ac 分布
    strong_acs = sorted(c["ac"] for c in ds_best.values()
                        if c["best_sh"] >= strong_bar and isinstance(c.get("ac"), int))
    if strong_acs:
        sp_min, sp_max = max(1, min(strong_acs)), max(strong_acs)
    else:
        sp_min, sp_max = 50, 1000  # 无强信号证据时用默认甜区

    report = {
        "region": ctx.region,
        "datasets_observed": len(ds_best),
        "alpha_store_datasets": len(alpha_store_sh),
        "alpha_store_alphas": sum(len(v) for v in alpha_store_sh.values()),
        "category_perf": {c: {"n": len(s), "max": round(max(s), 2),
                              "avg": round(sum(s) / len(s), 2)} for c, s in cat_perf.items()},
        "category_weights": weights,
        "sweet_spot": {"ac_min": sp_min, "ac_max": sp_max,
                       "strong_signal_acs": strong_acs},
        "strong_bar": strong_bar, "weak_bar": weak_bar,
    }
    # 通用能力护栏：实测数据集为 0（results 非标准契约/无匹配）时不写回 thresholds，
    # 避免空的 category_weights/默认甜区污染该区域配置（USA 早期 results 命名不规范曾触发）。
    if not ds_best:
        report["calibrated"] = False
        report["skip_reason"] = ("results/ 无可匹配的标准契约文件（需 {dataset, results:[...]} 或 "
                                 "文件名可推断出 ranking 内的 dataset id）；请先按 campaign toolkit 标准跑回测")
        return report
    report["calibrated"] = True
    if dry_run:
        report["dry_run"] = True
        return report  # 只采集+计算，不写 thresholds
    # 写回 thresholds.json dataset_health（幂等：只更新校准相关键）
    th_path = ctx.path("config", "thresholds.json")
    th = load_json(th_path) if os.path.exists(th_path) else {}
    dh = th.setdefault("dataset_health", {})
    dh["category_weight_enable"] = True
    dh["category_weight_floor"] = 0.9
    dh["category_weight_cap"] = 1.15
    dh["pyramid_quota_enable"] = True
    dh.setdefault("pyramid_quota_non_model_min", 2)
    dh["category_weights"] = weights
    dh["crowd_sweet_spot_enable"] = True
    dh["sweet_spot_ac_min"] = sp_min
    dh["sweet_spot_ac_max"] = sp_max
    dh["_calibrated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    dh["_calibrated_from"] = (f"alpha_store {sum(len(v) for v in alpha_store_sh.values())} alphas/"
                              f"{len(alpha_store_sh)} ds + results/ 扫描 → 共 {len(ds_best)} datasets 实测")
    atomic_write(th_path, th)
    return report


def cmd_calibrate(ctx, dry_run=False):
    r = calibrate_dataset_health(ctx, dry_run=dry_run)
    tag = "[dry-run] " if dry_run else ""
    print(f"{tag}[calibrate] region={r['region']} 实测数据集={r['datasets_observed']} "
          f"(alpha_store: {r.get('alpha_store_alphas', 0)} alphas/{r.get('alpha_store_datasets', 0)} ds)")
    if not r.get("calibrated"):
        print(f"  [跳过] {r.get('skip_reason')}")
        return
    print("  category 实测表现 -> 权重:")
    for c, p in sorted(r["category_perf"].items(), key=lambda x: -x[1]["max"]):
        w = r["category_weights"].get(c, 1.0)
        print(f"    {c:16s} n={p['n']} max={p['max']:.2f} avg={p['avg']:.2f} -> weight={w}")
    sp = r["sweet_spot"]
    print(f"  拥挤甜区: ac {sp['ac_min']}-{sp['ac_max']}（强信号集 ac={sp['strong_signal_acs']}）")
    if dry_run:
        print(f"  {tag}未写回 thresholds.json（dry-run，仅预览校准结果）")
    else:
        print(f"  已写回 thresholds.json dataset_health（category_weight + sweet_spot 开启）")


# ---------------- 探针电池接线 ----------------

def pick_fields(cat, n, family_kw):
    """按 变化/水平/质量 三族各选代表（coverage 优先，零竞争优先）。"""
    def fam(f):
        txt = (f["id"] + " " + (f.get("description") or "")).lower()
        for name, kws in family_kw.items():
            if any(k in txt for k in kws):
                return name
        return "level"
    buckets = {"change": [], "level": [], "quality": []}
    for f in sorted(cat["fields"], key=lambda x: (-(x.get("coverage") or 0),
                                                  (x.get("userCount") or 0))):
        buckets[fam(f)].append(f)
    per = max(1, n // 3)
    picked = buckets["change"][:per] + buckets["level"][:per] + buckets["quality"][:per]
    rest = [f for b in buckets.values() for f in b if f not in picked]
    return (picked + rest)[:n]


def render_probes(cat, fields, battery, stage_a_probes):
    is_vector = cat.get("data_type") == "VECTOR"
    stage_a, stage_b = [], []
    for f in fields:
        fid = f["id"]
        F = f"vec_avg({fid})" if is_vector else fid  # VECTOR 先聚合（含 P8 ts_backfill）
        for p in battery:
            item = {"probe": p["probe"], "field": fid, "expr": p["expr"].replace("F", F)}
            (stage_a if p["probe"] in stage_a_probes else stage_b).append(item)
    return stage_a, stage_b


def cmd_probe_plan(ctx, a):
    pc = load_platform_constraints()
    battery = pc["probe_battery"]
    stage_a_probes = set(pc["stage_a_probes"])
    family_kw = pc["field_family_keywords"]
    cat = load_catalog(ctx, a.probe_plan)
    if not cat:
        print(f"catalog 缺失，先自动 scan_fields --dataset {a.probe_plan}", file=sys.stderr)
        e, pw = load_credentials()
        api = Api(); api.login(e, pw)
        raw = scan_fields.fetch_fields(api, ctx.settings, a.probe_plan)
        cat = scan_fields.build_catalog(ctx.settings, a.probe_plan, raw)
        save_catalog(ctx, cat)
    fields = pick_fields(cat, a.fields, family_kw)
    stage_a, stage_b = render_probes(cat, fields, battery, stage_a_probes)
    bs = ctx.batch_size()

    def batches_of(lst):
        return [[x["expr"] for x in lst[i:i + bs]] for i in range(0, len(lst), bs)]

    all_exprs = stage_a + stage_b
    early_sh = ctx.thresh("probe_scoring_v2").get("early_red_sh", 0.3)
    # 探针计划入 ledger（战役产物不落 candidates/*.json）
    payload = {
        "dataset": a.probe_plan, "data_type": cat.get("data_type"), "region": ctx.region,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "settings": ctx.settings, "fields": [f["id"] for f in fields],
        "stageA": {"probes": sorted(stage_a_probes), "batches": batches_of(stage_a),
                   "early_stop_rule": f"Stage A 完成即 --probe-score --stage A 评分：max|sh|<{early_sh} 且无镜像 -> EARLY RED，不跑 Stage B（省 {len(batches_of(stage_b))} 批）"},
        "stageB": {"probes": sorted(set(p['probe'] for p in stage_b)), "batches": batches_of(stage_b)},
        "expressions": [x["expr"] for x in all_exprs],
        "batches": batches_of(all_exprs),
        "note": "两段式探针：先提 Stage A 批，评分非 EARLY RED 再提 Stage B；multisim id 交给 --probe-score",
    }
    from _lib.wqb_store import get_store
    st = get_store(ctx)
    try:
        st.upsert_ledger(ctx.region, f"probe_plan_{a.probe_plan}", payload)
        st.upsert_expressions(
            ctx.region, f"probe_{a.probe_plan}",
            payload["expressions"], dataset=a.probe_plan, status="probe")
    finally:
        st.close()
    print(f"dataset={a.probe_plan} data_type={cat.get('data_type')} fields={len(fields)} "
          f"stageA={len(stage_a)}式/{len(batches_of(stage_a))}批 "
          f"stageB={len(stage_b)}式/{len(batches_of(stage_b))}批")
    print(f"probe plan(v2 两段式) -> db probe_plan_{a.probe_plan} + expressions")


# ---------------- 三灯 ----------------

def score_v1(rows, thresh):
    """原公式（保留对照；修复 2y None 误判）。"""
    valid = [r for r in rows if r.get("sharpe") is not None]
    max_sh = max((abs(r["sharpe"]) for r in valid), default=0)
    mirror = any(r["sharpe"] < -0.5 for r in valid)
    margin_ok = any((r.get("margin_bp") or 0) > 5 for r in valid)
    tvr_ok = any(5 <= (r.get("turnover_pct") or 0) <= 30 for r in valid)
    potential = max_sh * 2 + (0.5 if mirror else 0) + (0.3 if margin_ok else 0) + (0.2 if tvr_ok else 0)
    g = thresh.get("probe_scoring", {}).get("green_min", 2.0)
    y = thresh.get("probe_scoring", {}).get("yellow_min", 1.0)
    return potential, ("GREEN" if potential >= g else ("YELLOW" if potential >= y else "RED"))


def score_v2(rows, cfg, stage="all"):
    """联合评估 + 广度 + CW 罚分 + tvr 结构性墙 + Stage A 早停。返回结构化判定。"""
    valid = [r for r in rows if r.get("sharpe") is not None]
    if not valid:
        return {"light": "RED", "potential": 0, "action": "无有效指标，判死", "components": {}}
    best = max(valid, key=lambda r: abs(r["sharpe"]))
    abs_sh = abs(best["sharpe"])
    mirror = any(r["sharpe"] < -0.5 for r in valid)
    breadth = sum(1 for r in valid if abs(r["sharpe"]) >= cfg["breadth_bar"])
    mg, tv, rn, fit = best.get("margin_bp"), best.get("turnover_pct"), best.get("rn_sharpe"), best.get("fitness")
    cw_fail = any("CONCENTRATED" in c for c in best.get("failed_checks") or [])
    comps = {
        "sharpe": round(cfg["w_sharpe"] * abs_sh, 3),
        "fitness": round(cfg["w_fitness"] * (fit or 0), 3),
        "mirror": cfg["w_mirror"] if mirror else 0,
        "margin": cfg["w_margin"] if (mg is not None and mg > 5) else 0,
        "tvr": cfg["w_tvr"] if (tv is not None and cfg["tvr_low"] <= tv <= cfg["tvr_high"]) else 0,
        "rn": cfg["w_rn"] if (rn is not None and rn >= cfg["rn_bar"]) else 0,
        "breadth": round(cfg["w_breadth"] * min(breadth, 4) / 4, 3),
        "cw_penalty": -cfg["cw_penalty"] if cw_fail else 0,
    }
    potential = round(sum(comps.values()), 3)
    light = "GREEN" if potential >= cfg["green_min"] else ("YELLOW" if potential >= cfg["yellow_min"] else "RED")

    # Stage A 早停
    if stage == "A" and abs_sh < cfg["early_red_sh"] and not mirror:
        return {"light": "EARLY_RED", "potential": potential, "best": best["id"],
                "action": f"Stage A 无信号(max|sh|={abs_sh:.2f}<{cfg['early_red_sh']}且无镜像)，不跑 Stage B，判死",
                "components": comps}

    # 2Y 红灯（仅当平台返回值；None 不判——v1 把 None 当 0 会误判）
    two_y = best.get("two_year_sharpe")
    red_2y = (two_y is not None and abs_sh >= cfg["red_2y_sh_abs_min"] and two_y < cfg["red_2y_max"])

    # tvr 结构性墙：全部探针同侧出界
    tvrs = [r["turnover_pct"] for r in valid if r.get("turnover_pct") is not None]
    tvr_struct = None
    if tvrs and all(t < cfg["tvr_low"] for t in tvrs):
        tvr_struct = "LOW"
    elif tvrs and all(t > cfg["tvr_high"] for t in tvrs):
        tvr_struct = "HIGH"

    if red_2y:
        light, action = "RED", f"2Y红灯：最强式2y={two_y:.2f}<{cfg['red_2y_max']}（近2年衰减），判死不深挖"
    elif tvr_struct and light == "GREEN":
        light = "YELLOW"
        action = ("结构性低tvr（全族<5%，multi_source_model 教训）：先 trade_when/decay 拉 tvr 再评，限2批"
                  if tvr_struct == "LOW" else
                  "结构性高tvr（全族>30%，news_sentiment_transfer 教训）：拉长窗口/加大 decay 压 tvr，限2批")
    elif light == "GREEN" and cw_fail:
        action = "绿灯(带CW修复)：深挖，骨架直接上跨Category rank加法（CW手册类型三）"
    elif light == "GREEN":
        action = "绿灯：深度挖掘（骨架融合/FE假设族/参数精磨）"
    elif light == "YELLOW":
        action = "黄灯：只做镜像腿与两两融合，限2批"
    else:
        action = "红灯：判死入台账，不回头" + ("（镜像偏强，可选留1批镜像验证）" if mirror else "")
    return {"light": light, "potential": potential, "best": best["id"],
            "best_metrics": {"sharpe": best["sharpe"], "fitness": fit, "2y": two_y,
                             "margin_bp": mg, "tvr_pct": tv, "rn": rn, "cw_fail": cw_fail},
            "breadth": breadth, "tvr_struct": tvr_struct, "red_2y": red_2y,
            "action": action, "components": comps}


def cmd_probe_score(ctx, a):
    if a.from_json:
        rows = [json.loads(l) for l in open(a.from_json, encoding="utf-8") if l.strip()]
    else:
        f = metrics_cache.MetricsFetcher(ctx)  # 单登录复用
        ids = f.multisim_alpha_ids(a.probe_score)
        rows = [f.fetch(aid) for aid in ids]
        rows.sort(key=lambda r: -(r.get("sharpe") if r.get("sharpe") is not None else -99))
    v2 = score_v2(rows, ctx.thresh("probe_scoring_v2"), stage=a.stage)
    v1p, v1l = score_v1(rows, ctx.thresholds)
    src = a.from_json or a.probe_score
    print(f"src={src} stage={a.stage}")
    print(f"[v2] {v2['light']}  potential={v2['potential']}  (v1 对照: {v1l} {v1p:.2f})")
    print(f"  components: {json.dumps(v2['components'], ensure_ascii=False)}")
    if v2.get("best_metrics"):
        print(f"  best={v2['best']} {json.dumps(v2['best_metrics'], ensure_ascii=False)} "
              f"breadth={v2['breadth']} tvr_struct={v2['tvr_struct']}")
    print(f"  action: {v2['action']}")
    if v2["light"] in ("RED", "EARLY_RED") and a.mark_dead and a.dataset:
        make_ledger_store(ctx).set_key(f"{a.dataset}_dead", {
            "dataset": a.dataset,
            "reason": f"探针三灯v2判死 potential={v2['potential']} light={v2['light']}",
            "dead_at": today()})
        print(f"ledger: {a.dataset}_dead written")


def main():
    ap = argparse.ArgumentParser(description="数据集评分 + 探针电池（三模式）")
    add_campaign_arg(ap)
    ap.add_argument("--probe-plan", metavar="DATASET")
    ap.add_argument("--probe-score", metavar="MULTISIM_ID")
    ap.add_argument("--from-json", metavar="FILE", help="从本地 JSON lines 指标文件评分（离线/校准用）")
    ap.add_argument("--stage", choices=["A", "B", "all"], default="all",
                    help="Stage A 评分启用早停判定")
    ap.add_argument("--dataset", help="--probe-score 时指定数据集（用于 --mark-dead）")
    ap.add_argument("--fields", type=int, default=6)
    ap.add_argument("--mark-dead", action="store_true")
    ap.add_argument("--calibrate", action="store_true",
                    help="从本战役实测回测（alpha 存储主源 + results/）自动校准筛选权重（category 加权 + 拥挤甜区），写回 thresholds")
    ap.add_argument("--dry-run", action="store_true",
                    help="配合 --calibrate：只采集+计算+打印校准结果，不写 thresholds.json")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)
    if a.calibrate:
        cmd_calibrate(ctx, dry_run=a.dry_run)
    elif a.probe_plan:
        cmd_probe_plan(ctx, a)
    elif a.probe_score or a.from_json:
        cmd_probe_score(ctx, a)
    else:
        cmd_score(ctx)


if __name__ == "__main__":
    main()
