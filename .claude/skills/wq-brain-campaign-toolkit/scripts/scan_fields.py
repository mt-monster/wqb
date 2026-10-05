# -*- coding: utf-8 -*-
"""scan_fields.py - 统一字段扫描器：直连 GET /data-fields 落 typed catalog。

typed catalog = gate 闸2/3 的数据源：每条字段带 {id, type, coverage, userCount,
alphaCount, description}；数据集级带 data_type（由字段类型众数推断）/region/universe/delay/fetched_at。

⚠️ 过滤参数必须是 dataset.id=<id>；裸 dataset=<id> 会被平台静默忽略
（返回全宇宙 10000 条上限，KOR 2026-08-15 实测）。

用法:
  python scan_fields.py --campaign-dir <DIR> --dataset model219                 # 全量落 catalog
  python scan_fields.py --campaign-dir <DIR> --dataset model219 --limit 5       # 快速冒烟
  python scan_fields.py --campaign-dir <DIR> --dataset model219 --zero-comp     # 只保留 userCount==0 字段

闸 TRI（2026-09-30，步 3/S1 入口 fail-closed）：扫描前先查 ledger `s1_triage_<region>`
（由 `tools/category_field_triage.py --all --write-ledger` 产出），判级非「★可开波」
（判死 / 族连坐 / 拥挤 / 无甜点字段 / 仅条件腿）**一律 exit 2**；台账缺失或数据集不在
台账内同样阻断（无法判定 = 阻断）。逃生口：`--skip-triage-gate` / `--triage-gate off`
/ `WQB_TRI_MODE=off`（会打印醒目告警）。
"""
import argparse
import collections
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import (CampaignContext, add_campaign_arg, load_credentials)
from _lib.api import Api
from _lib.wqb_store import save_catalog
from _lib.field_catalog_cache import get_cache_manager

PAGE = 50

# 可开波判级（与 tools/category_field_triage.py 的 order 表同源；改一处必须改另一处）
TRI_PASS_VERDICT = "★可开波"


def _triage_gate(region, dataset, conn=None):
    """闸 TRI：分类级字段分诊硬门（2026-09-30，步 3/S1 入口）。

    读 ledger `s1_triage_<region>`（由 tools/category_field_triage.py --write-ledger 产出），
    非「★可开波」的数据集**禁止进入字段扫描**。

    为什么要这道闸（实测，不是理论）：
      · 全局 9125 条回测 → 646 条 ra_clean，仅 7.1%；**49% 的回测（4475 条）打在后来
        被证伪的数据集上**，平均 22.8 条/死集。这些浪费发生在**选集之后、回测之中**，
        而选集那一刻本地已有足够信息判定「这个集不值得开」。
      · 判死记录的是**族**不是集：KOR risk88 判死「Barra 风格载荷 ri_* 族」，同族的
        risk70（字段名 mfm2_asetrd_*，只差模型版本号）数据集级判死抓不到，96 字段 /
        3 甜点 / 跨区 GLB maxS 2.16，会被 s0-select 当优质候选推出去 —— 靠**族签名
        包含度**才连坐得到。这一步人做必漏，故工具化后再上闸。

    fail-closed 契约（与闸 SEM 同构，§6 铁律：无法判定 = 阻断）：
      台账不可读 / 台账缺失 / 数据集不在台账内 / 判级非★可开波  →  一律 ok=False。
      唯一逃生口是显式 --skip-triage-gate / --triage-gate off / WQB_TRI_MODE=off。

    返回 dict：{region, dataset, ok, verdict, tags, reason,
                ledger_missing, unknown_dataset}
    conn 可注入（测试用内存库）；缺省走 _lib.db 规范工厂。
    """
    def _res(**kw):
        base = {"region": region, "dataset": dataset, "ok": False, "verdict": None,
                "tags": "", "reason": "", "ledger_missing": False,
                "unknown_dataset": False}
        base.update(kw)
        return base

    key = f"s1_triage_{(region or '').lower()}"
    own = conn is None
    if own:
        from _lib.db import connect as _connect  # toolkit 规范工厂（同 src/wqb/db_conn 口径）
        conn = _connect()
    try:
        try:
            row = conn.execute(
                "SELECT value FROM ledger_kv WHERE region=? AND key=?",
                (region, key)).fetchone()
        except Exception as e:
            # 库不可达 / 缺表 / 库被换 —— **等同于没做分诊**，按缺台账 fail-closed。
            # 这里若吞成「异常不阻断」，等于给了「换个空库就能绕过」的口子。
            return _res(ledger_missing=True, reason=f"分诊台账不可读（按缺台账处理）: {e}")
        if row is None:
            return _res(ledger_missing=True, reason=f"缺分诊台账 {key}")
        try:
            payload = json.loads(row[0])
        except Exception as e:
            return _res(ledger_missing=True, reason=f"{key} 解析失败（按缺台账处理）: {e}")
        verdicts = payload.get("verdicts")
        if not isinstance(verdicts, dict):
            # 旧版台账只存了 survivors，缺全量判级表 —— 无法判定该集的等级，同样阻断
            return _res(ledger_missing=True,
                        reason=f"{key} 无 verdicts 全量判级表（旧版台账，需重跑分诊）")
        ent = verdicts.get(dataset)
        if not isinstance(ent, dict):
            return _res(unknown_dataset=True,
                        reason=f"数据集不在分诊台账内（{key} 共 {len(verdicts)} 集；"
                               f"若为新同步进库的集需重跑分诊）")
        verdict = ent.get("verdict")
        tags = ent.get("tags") or ""
        # 判定依据是 block，不是 verdict —— 「判死但有实证产出」的集不阻断
        # （判死是族级的，同集其他族仍可能活；KOR 实证 3/3 高产集都是判死，
        #   按 verdict 硬拦会 100% 误杀历史产出）。
        block = ent.get("block")
        if block is None:
            # ⚠ 缺 block 键的旧版台账：此时 .get() 返回 None 会让判断放行 ——
            # 那是 fail-open 漏洞，必须按无法判定阻断。
            return _res(ledger_missing=True,
                        reason=f"{key} 的该集条目缺 block 字段（旧版台账，需重跑分诊）")
        if not block:
            return _res(ok=True, verdict=verdict, tags=tags)
        return _res(verdict=verdict, tags=tags,
                    reason=f"分诊判级={verdict}" + (f"（{tags}）" if tags else ""))
    finally:
        if own:
            try:
                conn.close()
            except Exception:
                pass


def fetch_fields(api, settings, dataset, limit=None):
    """分页拉取指定 dataset 的全部字段。过滤必须 dataset.id=<id>（裸 dataset= 被静默忽略）。"""
    base = ("/data-fields?instrumentType={instrumentType}&region={region}"
            "&delay={delay}&universe={universe}&dataset.id={ds}&limit={pg}").format(
                pg=PAGE, ds=dataset, **settings)
    out, offset = [], 0
    while True:
        j = json.load(api.get(f"{base}&offset={offset}"))
        results = j.get("results", [])
        out.extend(results)
        if limit and len(out) >= limit:
            return out[:limit]
        offset += len(results)
        if not results or offset >= j.get("count", 0):
            return out


# 2026-09-04 新增：字段类型自动标注 + 算子类别推荐
# 与 field_operator_pattern.md 适配矩阵对齐，S1 扫描时自动标注字段类型并推荐算子

_FIELD_TYPE_KEYWORDS = {
    "signal": ["score", "rank", "rating", "estimate", "surprise", "prediction", "signal", "alpha"],
    "scale": ["shares", "market cap", "market value", "enterprise value", "total assets", "total equity", "volume", "turnover"],
    "metadata": ["periodend", "periodtype", "fyearend", "periodnum", "analyststart", "curfperiod", "curperiod", "_date", "_dt", "fiscalend", "reportdate"],
    "date": ["date", "period end", "fiscal year end", "announcement", "timestamp"],
}

_FIELD_TYPE_OP_RECOMMEND = {
    "signal": ["rank", "ts_delta", "ts_mean", "ts_zscore", "group_zscore"],
    "scale": ["rank", "ts_mean", "group_scale"],
    "metadata": [],  # 禁用
    "date": [],      # 禁用
}


def _classify_field(field_id, description=""):
    """按字段名/描述推断字段类型（signal/scale/metadata/date）。"""
    fid_lower = field_id.lower()
    desc_lower = description.lower()
    
    # metadata 优先（永不应入表达式）
    for kw in _FIELD_TYPE_KEYWORDS["metadata"]:
        if kw in fid_lower or kw in desc_lower:
            return "metadata"
    
    # date 次之
    for kw in _FIELD_TYPE_KEYWORDS["date"]:
        if kw in fid_lower or kw in desc_lower:
            return "date"
    
    # scale 再次
    for kw in _FIELD_TYPE_KEYWORDS["scale"]:
        if kw in fid_lower or kw in desc_lower:
            return "scale"
    
    # signal 兜底
    return "signal"


def _recommend_operators(field_type, data_type="MATRIX"):
    """按字段类型推荐算子类别。"""
    base_ops = _FIELD_TYPE_OP_RECOMMEND.get(field_type, [])
    if data_type == "VECTOR":
        # VECTOR 字段必须先聚合
        return ["vec_avg", "vec_stddev", "vec_count"] + base_ops
    return base_ops


def build_catalog(settings, dataset, raw):
    types = collections.Counter((f.get("type") or "UNKNOWN") for f in raw)
    data_type = types.most_common(1)[0][0] if types else "UNKNOWN"
    fields = [{
        "id": f.get("id"),
        "type": f.get("type"),
        "coverage": f.get("coverage"),
        "userCount": f.get("userCount"),
        "alphaCount": f.get("alphaCount"),
        "description": (f.get("description") or "")[:120],
        # 2026-09-04 新增：字段类型标注 + 算子推荐
        "field_type": _classify_field(f.get("id", ""), f.get("description", "")),
        "recommended_operators": _recommend_operators(
            _classify_field(f.get("id", ""), f.get("description", "")),
            data_type
        ),
    } for f in raw]
    
    # 字段类型分布统计
    field_type_dist = collections.Counter(f["field_type"] for f in fields)
    
    return {
        "dataset": dataset,
        "region": settings["region"],
        "universe": settings["universe"],
        "delay": settings["delay"],
        "data_type": data_type,
        "type_distribution": dict(types),
        "field_type_distribution": dict(field_type_dist),  # 2026-09-04 新增
        "field_count": len(fields),
        "fetched_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "fields": fields,
    }


def main():
    ap = argparse.ArgumentParser(description="typed catalog 字段扫描")
    add_campaign_arg(ap)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--zero-comp", action="store_true", help="只保留 userCount==0 的零竞争字段")
    ap.add_argument("--stdout", action="store_true", help="只打印不落盘")
    ap.add_argument("--force-refresh", action="store_true", help="强制刷新缓存")
    ap.add_argument("--cache-ttl", type=int, default=86400, help="缓存有效期（秒），默认 24 小时")
    # 闸 TRI（2026-09-30）：步 3/S1 入口分诊硬门。模式解析同 WQB_SEM_MODE / WQB_GATE_MODE。
    ap.add_argument("--triage-gate", dest="triage_gate", default=None,
                    choices=["off", "warn", "enforce"],
                    help="闸 TRI 模式（缺省读环境变量 WQB_TRI_MODE，兜底 enforce）")
    ap.add_argument("--skip-triage-gate", action="store_true",
                    help="闸 TRI 唯一逃生口：跳过分诊硬门（会打印醒目告警）")
    a = ap.parse_args()
    ctx = CampaignContext(a.campaign_dir)

    # ── 闸 TRI：进字段扫描前先问「这个集还值不值得开」 ──────────────────────
    # 产物来源：python tools/category_field_triage.py --region <R> --all --write-ledger
    # 契约：非★可开波（判死/族连坐/拥挤/无甜点字段/仅条件腿）一律阻断，缺台账同样阻断。
    # 模式解析：CLI > 环境变量 WQB_TRI_MODE > 缺省 enforce
    _tri_mode = (os.environ.get("WQB_TRI_MODE") or "enforce").strip().lower()
    if a.skip_triage_gate or a.triage_gate == "off":
        _tri_mode = "off"
    elif a.triage_gate in ("warn", "enforce"):
        _tri_mode = a.triage_gate
    if _tri_mode == "off":
        print("[tri  ] ⚠ 闸 TRI 已关闭（--skip-triage-gate / WQB_TRI_MODE=off）：判死、族连坐、"
              "拥挤、无甜点字段的数据集也会被扫描，回测预算可能再打进已证伪的池子。")
    if _tri_mode != "off":
        try:
            _tri = _triage_gate(ctx.region, a.dataset)
        except Exception as e:  # 闸自身炸了也按「无法判定」处理，不放行
            _tri = {"ok": False, "region": ctx.region, "dataset": a.dataset, "tags": "",
                    "reason": f"闸 TRI 自身异常（按无法判定=阻断处理）: {e}"}
        if not _tri.get("ok"):
            print("[tri  ] %s%s —— %s" % (
                "★★ 闸 TRI 阻断：" if _tri_mode == "enforce" else "[warn] 闸 TRI 告警：",
                a.dataset, _tri.get("reason")), file=sys.stderr)
            if _tri.get("tags"):
                print("[tri  ]    分诊标签: %s" % _tri["tags"], file=sys.stderr)
            print("[tri  ]    修复：python tools/category_field_triage.py --region %s "
                  "--all --write-ledger" % (_tri.get("region") or ctx.region), file=sys.stderr)
            if _tri_mode == "enforce":
                print("[tri  ]    确需放行加 --skip-triage-gate / --triage-gate warn "
                      "（会打印醒目告警）。", file=sys.stderr)
                sys.exit(2)

    # 初始化缓存管理器
    cache_manager = get_cache_manager(ctx, a.cache_ttl)
    
    # 1. 检查缓存（除非强制刷新）
    if not a.force_refresh:
        cached = cache_manager.get_cached_catalog(a.dataset)
        if cached:
            print(f"[cache] 使用缓存的字段目录（{len(cached.get('fields', []))} 个字段，"
                  f"缓存时间: {cached.get('cache_metadata', {}).get('cached_at', 'unknown')})")
            if a.stdout:
                print(json.dumps(cached, ensure_ascii=False, indent=1))
            else:
                save_catalog(ctx, cached)  # 确保 DB 同步
                print(f"catalog -> db fields/{ctx.region}/{a.dataset} ({cached['field_count']}) [cached]")
            return

    # 2. 缓存未命中或强制刷新，执行平台扫描
    print(f"[cache] 缓存未命中或强制刷新，从平台扫描 {a.dataset}...")
    e, pw = load_credentials()
    api = Api()
    api.login(e, pw)
    raw = fetch_fields(api, ctx.settings, a.dataset, limit=a.limit)
    if a.zero_comp:
        raw = [f for f in raw if (f.get("userCount") or 0) == 0]
    cat = build_catalog(ctx.settings, a.dataset, raw)
    
    print(f"dataset={a.dataset} fields={cat['field_count']} data_type={cat['data_type']} "
          f"types={cat['type_distribution']}", file=sys.stderr)
    
    if a.stdout:
        print(json.dumps(cat, ensure_ascii=False, indent=1))
        return
    
    # 3. 保存到缓存和 DB
    save_catalog(ctx, cat)
    cache_manager.save_catalog_cache(a.dataset, cat)
    print(f"catalog -> db fields/{ctx.region}/{a.dataset} ({cat['field_count']}) [fresh]")


if __name__ == "__main__":
    import os as _os_sc; _os_sc.environ.setdefault("WQB_STARTUP_CHECKS", "once")  # 启动校验每进程只打一次（2026-09-19）
    main()
