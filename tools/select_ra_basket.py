#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""select_ra_basket.py — 从过闸候选池选出 N 条互不相关、可提交的 RA 篮子。

输入 = build_gate_prior_from_inventory.py --emit-candidates 的产物。

四道处理，顺序是刻意的（2026-09-08 实证）：

  1. **去参数网格**：按 (region, delay, 字段集合) 归并同族变体，每族只留最强一条。
     实测 859 条候选归并后只剩 277 条独立信号（GLB 9.0× / CHN 9.0× / GBR 4.4×）——
     名义库存被 add(A,B) 权重网格与 decay 刷值严重虚高。
     把调参变体送进限流的相关性队列纯属浪费。

  2. **OS 撞车预筛**：生产池包含自己已提交的 alpha，所以「未提交的孪生兄弟」
     必然被自己的已提交版本挡死，且同样卡 SELF_CORRELATION。
     `get_mutual_correlation` 本地算 PnL、**不占平台相关性配额**，可零成本预测这类失败。
     实测证据：O0GWvzbp ~ 已提交 6XpMb0aG 本地互相关 0.9524，
     其平台实测 prod max = 0.9522 —— 四位小数吻合。

  3. **篮内正交 + 金字塔轮转**：贪心选取两两 < 阈值的子集，优先未点亮的金字塔
     （CLAUDE.md：一塔需 3 颗点亮，尽可能多点且均匀）。
     注意 SELF_CORRELATION 是会收紧的约束——每提交一条 OS 池就大一格，
     所以必须按互不相关子集**整体**选取，不能逐条贪心。

  4. **平台复核**：逐条 GET /alphas/{id}，以 detail 端点 `is.checks` 无 result==FAIL 为准。
     list 端点的 checks ≠ detail 端点的 checks；且 submit_verdict 在
     submit_status=404 + prepost_unverifiable 时会报假 SUBMITTABLE，不可依赖。

用法:
    python tools/select_ra_basket.py candidates.json --target 20 --out basket.json
    python tools/select_ra_basket.py candidates.json --pool 150 --threshold 0.7

运行环境: MCP venv（$WQ_PY / world-quant-brain-mcp/.venv）。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
import sys as _sys_pe, os as _os_pe
_sys_pe.path.insert(0, _os_pe.path.dirname(_os_pe.path.abspath(__file__)))
import _pyenv  # noqa: E402  跨平台解释器解析（tools/_pyenv.py）；作为脚本运行时自动切到 MCP venv，故文档里可写裸 python

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "world-quant-brain-mcp"))
sys.path.insert(0, str(REPO_ROOT / "src"))

BANNED_REGIONS = {"MEA"}

FIELD_TOKEN_RE = re.compile(r"\b([a-z][a-z0-9_]{3,})\b")
_KNOWN_OPS = set("""
rank add multiply subtract divide group_rank group_zscore group_neutralize group_mean group_sum
group_count group_scale group_std_dev group_backfill ts_mean ts_delta ts_zscore ts_rank ts_backfill
ts_decay_linear ts_std_dev ts_sum ts_max ts_min ts_corr ts_covariance ts_regression ts_av_diff
ts_arg_max ts_arg_min ts_product ts_quantile ts_count_nans ts_scale ts_step ts_returns ts_ir
ts_delay ts_kurtosis ts_max_diff vec_avg vec_sum vec_max vec_min vec_stddev vec_count vec_range
winsorize scale normalize signed_power quantile power reverse zscore abs log sign sqrt inverse
densify pasteurize hump kth_element trade_when if_else bucket greater less equal and or not is_nan
not_equal less_equal greater_equal max min days_from_last_change last_diff_value
industry sector subindustry market country exchange std range rettype driver
returns close open high low volume vwap cap adv20 sharesout
""".split())


def fields_of(code: str) -> frozenset:
    return frozenset(t for t in FIELD_TOKEN_RE.findall(code or "")
                     if t not in _KNOWN_OPS and not t.isdigit())


def pyr_key(c: dict) -> str:
    return "+".join(sorted((c.get("pyramids") or {}).get("list") or ["?"]))


def dedup_and_rotate(cands: list) -> list:
    """去参数网格 + 按 (region, 金字塔) 轮转排序，让前若干条覆盖尽量多的塔。"""
    cands = [c for c in cands if c.get("region") not in BANNED_REGIONS]
    groups = defaultdict(list)
    for c in cands:
        groups[(c["region"], c["delay"], fields_of(c["code"]))].append(c)
    reps = []
    for g in groups.values():
        g.sort(key=lambda x: (-(x.get("fitness") or 0), -(x.get("sharpe") or 0)))
        reps.append({**g[0], "_dupes": len(g) - 1})

    buckets = defaultdict(list)
    for r in reps:
        buckets[(r["region"], pyr_key(r))].append(r)
    for b in buckets.values():
        b.sort(key=lambda x: -(x.get("fitness") or 0))

    order, guard = [], 0
    while any(buckets.values()) and guard < 500:
        for k in sorted(buckets, key=lambda k: (-len(buckets[k]), str(k))):
            if buckets[k]:
                order.append(buckets[k].pop(0))
        guard += 1
    return order


async def fetch_os_ids(brain) -> list:
    ids, off = [], 0
    while True:
        r = await brain._request("GET", f"{brain.base_url}/users/self/alphas",
                                 params={"limit": 100, "offset": off, "stage": "OS"})
        j = r.json()
        if not isinstance(j, dict):
            break
        arr = j.get("results") or []
        ids += [a["id"] for a in arr if a.get("id")]
        if len(arr) < 100:
            break
        off += 100
    return ids


async def platform_recheck(brain, alpha_id: str):
    """detail 端点复核：返回 FAIL 项列表（空 = 干净）。None 表示取详情失败。"""
    r = await brain._request("GET", f"{brain.base_url}/alphas/{alpha_id}")
    j = r.json()
    if not isinstance(j, dict):
        return None
    checks = ((j.get("is") or {}).get("checks")) or []
    return [{"name": x.get("name"), "value": x.get("value"), "limit": x.get("limit"),
             "ratio": x.get("ratio")}
            for x in checks if isinstance(x, dict) and x.get("result") == "FAIL"]


def _candidate_datasets(conn, region: str, fields) -> set:
    """经 fields 表把表达式用到的字段回填到数据集名（region 作用域）。

    查不到归属 → 空集（不归因；调用方 fail-open 保留候选，宁可漏剔不可误杀）。
    """
    if not fields:
        return set()
    marks = ",".join("?" for _ in fields)
    cur = conn.execute(
        "SELECT DISTINCT ds.name FROM fields f "
        "JOIN datasets ds ON f.dataset_id=ds.id JOIN regions r ON ds.region_id=r.id "
        f"WHERE r.name=? AND f.field_name IN ({marks})",
        (region, *sorted(fields)),
    )
    return {str(r[0]).strip().lower() for r in cur.fetchall() if r[0]}


def apply_dead_exclusions(conn, cands: list):
    """判死/饱和数据集剔除（2026-10-01 P1 断流修复；**默认开启**，`--no-exclude-dead` 才关）。

    动机：本工具四道处理此前不消费判死/饱和台账，「IS 过闸但所属族已撞 prod 墙判死」的候选
    会被带进篮子，烧完步 7 诊断链到步 8 才被 prod 实测挡掉。

    规则（两档与 wqb.profile_drift 同源）：
      - 候选任一字段归属 ∈ dataset_dead ∪ saturated → **剔除**
      - 命中 family_dead（族级死，未必整集死）→ 保留但计数告警
      - 字段查不到归属（fields 表未覆盖该区/集）→ 保留并计数（fail-open）
    返回 (kept, dropped, stats)；dropped 元素 = {"id", "region", "datasets"}。
    """
    from wqb.profile_drift import dead_dataset_index

    by_region: dict = {}
    stats = {"unattributed": 0, "family_dead_hits": 0}
    kept, dropped = [], []
    for c in cands:
        region = c.get("region") or ""
        if region not in by_region:
            by_region[region] = dead_dataset_index(conn, region)
        idx = by_region[region]
        dss = _candidate_datasets(conn, region, fields_of(c.get("code") or ""))
        if not dss:
            stats["unattributed"] += 1
            kept.append(c)
            continue
        hard = sorted(dss & (idx["dataset_dead"] | idx["saturated"]))
        if hard:
            dropped.append({"id": c.get("id"), "region": region, "datasets": hard})
            continue
        if dss & idx["family_dead"]:
            stats["family_dead_hits"] += 1
        kept.append(c)
    return kept, dropped, stats


#: prod 值的新鲜度缺省（天）。2026-10-03：IND 旧候选 09-19~23 实测 prod 0.51–0.67，10-02 复测**全部** 0.83–0.99
#: （社区同族 alpha 持续进 book，WorkBuddy 记忆 MEMORY §1.3「陈旧 prod 值一律作废」）。
PROD_FRESH_DAYS = 2


def classify_prod(prod, checked_at, max_age_days=PROD_FRESH_DAYS, now=None, ceiling=None):
    """把一条候选在 `alphas` 表里记录的 prod 值分类。返回 (status, age_days)。

    status：
      - ``unmeasured``   prod 为空，从未测过
      - ``fresh_ok``     ≤ max_age_days 天内测的，且 < ceiling —— **只有它算「prod 已核」**
      - ``fresh_blocked``≤ max_age_days 天内测的，且 ≥ ceiling —— 已知必撞铁律线
      - ``stale_ok``     更早测的（或没有测量时间）且 < ceiling —— 值作废，须重测
      - ``stale_blocked``更早测的且 ≥ ceiling —— prod 漂移方向是社区同族持续进 book（只升不降），
                         旧高值不会自己变低，按已知必撞处理
    ``age_days`` 为 None 表示没有可解析的测量时间（一律按陈旧算）。
    """
    import datetime as _dt

    if ceiling is None:
        try:
            from wqb.config import PRODCORR_CEILING as ceiling
        except Exception:  # noqa: BLE001  config 不可导入时用与 config 相同的缺省
            ceiling = 0.70
    if prod is None:
        return "unmeasured", None
    age = None
    if checked_at:
        try:
            ts = _dt.datetime.fromisoformat(str(checked_at).strip().replace("Z", "+00:00"))
            if ts.tzinfo is not None:
                ts = ts.astimezone().replace(tzinfo=None)
            ref = now or _dt.datetime.now()
            age = max((ref - ts).total_seconds() / 86400.0, 0.0)
        except (ValueError, TypeError):
            age = None
    fresh = age is not None and age <= max_age_days
    blocked = float(prod) >= float(ceiling)
    return (("fresh_" if fresh else "stale_") + ("blocked" if blocked else "ok")), age


def prod_freshness_index(conn, ids, max_age_days=PROD_FRESH_DAYS, now=None):
    """只读 `alphas` 表，返回 {alpha_id: {prod, checked_at, age_days, status}}（查不到的 id 不在结果里）。"""
    ids = [i for i in dict.fromkeys(ids) if i]
    out = {}
    for start in range(0, len(ids), 500):  # 分块：避开 SQLite 变量个数上限
        chunk = ids[start:start + 500]
        marks = ",".join("?" for _ in chunk)
        rows = conn.execute(
            "SELECT alpha_id, prod_correlation, corr_checked_at FROM alphas "
            f"WHERE alpha_id IN ({marks})", chunk,
        ).fetchall()
        for aid, prod, checked in rows:
            status, age = classify_prod(prod, checked, max_age_days, now)
            out[aid] = {"prod": prod, "checked_at": checked,
                        "age_days": None if age is None else round(age, 2), "status": status}
    return out


async def main_async(a):
    from brain_api import BrainApiClient

    raw = json.loads(Path(a.candidates).read_text(encoding="utf-8"))
    if getattr(a, "exclude_dead", False):
        try:
            from wqb.db_conn import connect as db_connect, default_db_path
            conn = db_connect(a.db or default_db_path(), readonly=True)
            try:
                raw, dropped, ex_stats = apply_dead_exclusions(conn, raw)
            finally:
                conn.close()
            print(f"[剔死] 剔除 {len(dropped)} 条命中判死/饱和数据集"
                  f"（族级死保留 {ex_stats['family_dead_hits']} 条，未归因 {ex_stats['unattributed']} 条）")
            for d in dropped[:10]:
                print(f"      - {d['id']} ({d['region']}): {', '.join(d['datasets'])}")
        except Exception as e:  # fail-open：DB 不可用不阻断选篮
            print(f"[剔死] 跳过（{type(e).__name__}: {e}）")
    ranked = dedup_and_rotate(raw)
    print(f"[去重] 候选 {len(raw)} -> 独立信号 {len(ranked)} "
          f"（压缩 {len(raw) / max(len(ranked), 1):.1f}x）")
    print(f"[分布] {dict(Counter(c['region'] for c in ranked).most_common())}")

    # prod 新鲜度（2026-10-03）：只读库里已记录的 prod 值——已知 ≥ 上限的不再送进限流的相关性队列，
    # 篮子里只有「近 N 天内测过且 < 上限」的才算 prod 已核（步 1 的「库存足够」判据只数这类）。
    prod_info = {}
    try:
        from wqb.db_conn import connect as db_connect, default_db_path
        conn = db_connect(a.db or default_db_path(), readonly=True)
        try:
            prod_info = prod_freshness_index(conn, [c.get("id") for c in ranked], a.prod_max_age_days)
        finally:
            conn.close()
    except Exception as e:  # fail-open：DB 不可用不阻断选篮（全部按 unmeasured 处理，不剔除）
        print(f"[prod 新鲜度] 跳过（{type(e).__name__}: {e}）")
    if prod_info and not a.keep_prod_blocked:
        bad_ids = {i for i, v in prod_info.items() if v["status"] in ("fresh_blocked", "stale_blocked")}
        if bad_ids:
            ranked = [c for c in ranked if c.get("id") not in bad_ids]
            print(f"[prod 已知撞墙] 剔除 {len(bad_ids)} 条（库内记录的 prod ≥ 上限；"
                  f"prod 只会被社区同族挤高，旧高值不会自己变低；--keep-prod-blocked 可保留）")

    pool = ranked[:a.pool]
    meta = {c["id"]: c for c in pool}
    ids = [c["id"] for c in pool]

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    os_ids = [i for i in await fetch_os_ids(brain) if i not in meta]
    print(f"[OS 池] 已提交 {len(os_ids)} 条")

    allids = ids + os_ids
    print(f"[互相关] {len(ids)} 候选 + {len(os_ids)} OS，抓 PnL 中（本地计算，不占平台配额）…",
          flush=True)
    m = await brain.get_mutual_correlation(allids, threshold=a.threshold, years=a.years)
    mat = m.get("matrix") or {}
    missing = set(m.get("missing_pnl") or [])
    if missing:
        print(f"[警告] {len(missing)} 条无 PnL（多为过旧模拟），已排除")

    def corr(x, y):
        v = (mat.get(x) or {}).get(y)
        return abs(v) if isinstance(v, (int, float)) else 0.0

    osset = set(os_ids)
    blocked = {}
    for cid in ids:
        hits = [(o, corr(cid, o)) for o in osset if corr(cid, o) > a.threshold]
        if hits:
            hits.sort(key=lambda t: -t[1])
            blocked[cid] = hits[0]
    survivors = [i for i in ids if i not in blocked and i not in missing]
    print(f"[OS 撞车] 剔除 {len(blocked)}/{len(ids)} 条（与自己已提交的 alpha 超阈，必卡 self）")
    for cid, (o, v) in list(blocked.items())[:8]:
        print(f"    {cid} ~ OS {o} = {v:.4f}")

    chosen, pyr_cnt = [], Counter()
    remaining = list(survivors)
    while remaining and len(chosen) < a.target:
        remaining.sort(key=lambda cid: (pyr_cnt[pyr_key(meta[cid])],
                                        -(meta[cid].get("fitness") or 0)))
        pick = None
        for cid in remaining:
            if all(corr(cid, k) <= a.threshold for k in chosen):
                fails = await platform_recheck(brain, cid)
                if fails is None:
                    continue
                if fails:
                    print(f"    平台复核拒绝 {cid} {meta[cid]['region']:4s} "
                          f"<- {[f['name'] for f in fails]}")
                    remaining.remove(cid)
                    continue
                pick = cid
                break
        if pick is None:
            break
        chosen.append(pick)
        pyr_cnt[pyr_key(meta[pick])] += 1
        remaining.remove(pick)
        await asyncio.sleep(0.3)

    print(f"\n[篮子] {len(chosen)}/{a.target} 条，两两 < {a.threshold}\n")
    hdr = (f"{'#':>3} {'alpha':10s} {'reg':4s} {'universe':18s} {'neut':14s} "
           f"{'sh':>5} {'fit':>5} {'2y':>5} {'maxCorr':>7} {'prod':>14s}  pyramid")
    print(hdr)
    out = []
    for n, cid in enumerate(chosen, 1):
        c = meta[cid]
        mc = max([corr(cid, k) for k in chosen if k != cid]
                 + [corr(cid, o) for o in osset] + [0.0])
        pi = prod_info.get(cid) or {}
        pst = pi.get("status", "unmeasured")
        print(f"{n:>3} {cid:10s} {c['region']:4s} {str(c['universe']):18s} "
              f"{str(c['neut'])[:14]:14s} {(c.get('sharpe') or 0):5.2f} "
              f"{(c.get('fitness') or 0):5.2f} {(c.get('two_year_sharpe') or 0):5.2f} "
              f"{mc:7.4f} {pst:>14s}  {pyr_key(c)}")
        out.append({**c, "max_corr": round(mc, 4), "prod_status": pst,
                    "prod_correlation": pi.get("prod"), "prod_checked_at": pi.get("checked_at"),
                    "prod_age_days": pi.get("age_days")})
    print(f"\n[点塔] {len(set(pyr_key(meta[c]) for c in chosen))} 个互不相同的金字塔")
    n_ok = sum(1 for r in out if r["prod_status"] == "fresh_ok")
    print(f"[prod 新鲜度] 篮内 {len(out)} 条：已核（近 {a.prod_max_age_days} 天内测过且 < 上限）{n_ok} 条 / "
          f"需重测 {len(out) - n_ok} 条（stale / 未测）")
    print("      步 1 的「库存足够」只数已核条数；其余须在步 8 前 check_correlation(refresh=True) 重测。")
    if a.out:
        Path(a.out).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[写出] {a.out}")
    print("\n提醒：本工具只做筛选与报告。按 SOP 步 8，提交必须经用户确认后")
    print("      再调 workflow_submit_alpha —— 禁止自动提交。")


def main():
    ap = argparse.ArgumentParser(description="从过闸候选池选出互不相关的 RA 篮子")
    ap.add_argument("candidates", help="build_gate_prior_from_inventory.py --emit-candidates 的产物")
    ap.add_argument("--target", type=int, default=20, help="篮子大小（默认 20）")
    ap.add_argument("--pool", type=int, default=120, help="送进互相关计算的候选数（默认 120）")
    ap.add_argument("--threshold", type=float, default=0.7, help="相关性阈值（默认 0.7）")
    ap.add_argument("--years", type=int, default=4, help="相关性计算的回看年数（默认 4）")
    ap.add_argument("--out", default=None, help="篮子 JSON 输出路径")
    ap.add_argument("--exclude-dead", dest="exclude_dead", action="store_true", default=True,
                    help="剔除判死/饱和数据集的候选（**默认开启**，workflow 节点不传标志也会走到；"
                         "2026-10-01 P1 断流修复）")
    ap.add_argument("--no-exclude-dead", dest="exclude_dead", action="store_false",
                    help="显式关闭剔除（仅调试；把死族带进篮子的风险自行承担）")
    ap.add_argument("--db", default=None, help="wqb.db 路径（缺省自动探测仓库根）")
    ap.add_argument("--prod-max-age-days", dest="prod_max_age_days", type=float, default=PROD_FRESH_DAYS,
                    help=f"库内 prod 值算「新鲜」的天数（缺省 {PROD_FRESH_DAYS}）；更早测的值作废、须重测")
    ap.add_argument("--keep-prod-blocked", dest="keep_prod_blocked", action="store_true", default=False,
                    help="保留库内记录 prod ≥ 上限的候选（缺省剔除；仅调试）")
    a = ap.parse_args()
    asyncio.run(main_async(a))


if __name__ == "__main__":
    _pyenv.reexec_under_venv()
    main()
