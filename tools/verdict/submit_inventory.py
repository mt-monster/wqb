#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""submit_inventory.py — 一跑即出「当前可提交候选清单」的盘点工具。

⛔ 铁律：本脚本**只读平台、只判不提交**——绝不 POST /alphas/{id}/submit。
   任何提交动作都须用户在当轮明确指示，并走 worldquant-submit-alpha（含配额 1 次/天/区）。

判定口径（与 tools/submit_verdict.py 共用 wqb.submit_verdict_core.decide，不另起一套）：
  1) 模拟层  get_alpha_details().is.checks 的 FAIL / 硬闸 WARNING
  2) 资格门  WebDataScope Failed-count（REGULAR 看 RA / PPA 看 PPA）——唯一权威；
             本地 submit_ready.gate 字段不可信（实测 A1vOb5pE/ZYAWx9J3 本地记 PASS
             而平台 LOW_INVESTABILITY_CONSTRAINED_SHARPE FAIL）
  3) 相关性  check_correlation(refresh=True)。**>48h 的 prod 视为过期必须重测**
             （实证：.68→.98 漂移；E5pbM7Nm 静态 0.6678 → 刷新 0.981 FAIL）

输出七分类（优先级从上到下）：
  SUBMIT_NOW         模拟层干净 + Failed-count=0 + prod/self<0.7 + 余量≥thin_margin
                     + 相关性在新鲜窗口内 ⇒ 可提交（仍需用户逐次明示 + 平台配额）
  THIN_MARGIN        同上但 min(prod,self) 余量 < thin_margin（默认 0.03）
                     ⇒ 全过但一碰就撞墙，建议不提
  PROD_WALL          模拟层全过，仅 prod/self ≥ 0.7（随生产池变化可恢复；不 POST，
                     POST 会污染池子废掉同族兄弟）
  HARD_BLOCKED      模拟层 FAIL / 硬闸 WARNING / Failed-count 非零（须修复重测）
  ALREADY_SUBMITTED 平台已 ACTIVE/SUBMITTED（勿重复 POST）
  CORR_UNKNOWN      prod/self 缺失或超新鲜窗口且本轮未取得（含平台 busy/pending）
  ERROR             平台请求失败

用法：
  python tools/verdict/submit_inventory.py                            # 盘点 READY + 拉新 corr + 同步台账
  python tools/verdict/submit_inventory.py --no-sync-queue             # 只读，完全不动 submit_ready
  python tools/verdict/submit_inventory.py --skip-corr                 # 只用库里已存相关性（最快）
  python tools/verdict/submit_inventory.py --include-prod-blocked --skip-corr
  python tools/verdict/submit_inventory.py --refresh-all               # 全部强制 refresh=True
  python tools/verdict/submit_inventory.py --region GBR --limit 10

产物：控制台报告 + results/submit_inventory_<时间戳>.json + .csv
checkpoint：logs/_submit_inventory.json（corr 结果缓存，48h 内重跑不重打平台单并发队列）

退出码：0=正常出报告  2=参数错误  3=平台/鉴权失败
运行环境：MCP venv（`WQ_PY` 或 world-quant-brain-mcp/.venv，自动 re-exec）
"""
import argparse
import asyncio
import csv
import json
import os
import sys
from datetime import datetime, timedelta, timezone

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # 同主题目录的兄弟脚本
sys.path.insert(0, os.path.dirname(_HERE))       # tools/（_pyenv 在此；2026-10-06 下沉到主题目录后必需）
import _pyenv  # noqa: E402

REPO = _pyenv.REPO_ROOT
LOGS_DIR = REPO / "logs"
RESULTS_DIR = REPO / "results"
CKPT_PATH = LOGS_DIR / "_submit_inventory.json"
PYRAMID_CACHE = LOGS_DIR / "_pyramid_multipliers.json"
PYRAMID_TTL_H = 24.0

LOCAL_TZ = datetime.now().astimezone().tzinfo
BUCKETS = ("SUBMIT_NOW", "THIN_MARGIN", "PROD_WALL", "HARD_BLOCKED",
           "ALREADY_SUBMITTED", "CORR_UNKNOWN", "ERROR")


def _bootstrap():
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()


def _now():
    return datetime.now().astimezone()


def _now_iso():
    return _now().isoformat(timespec="seconds")


def _parse_iso(s):
    """容错解析 ISO 时间戳（无时区按本机时区）；失败返回 None。"""
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=LOCAL_TZ)
    return dt


def _age_hours(iso):
    dt = _parse_iso(iso)
    if dt is None:
        return None
    return round((_now() - dt).total_seconds() / 3600.0, 1)


# ---------------- checkpoint（corr 结果缓存） ----------------

def load_ckpt():
    try:
        return json.loads(CKPT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"corr": {}}


def save_ckpt(ckpt):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = CKPT_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(ckpt, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, CKPT_PATH)


# ---------------- 读库 ----------------

def load_queue(region=None, include_prod_blocked=False, include_dead=False, db_path=None):
    from wqb.store import submit_queue as sq
    con = sq.connect(db_path)
    try:
        sq.ensure_table(con)
        statuses = ["READY"]
        if include_prod_blocked:
            statuses.append(sq.STATUS_PROD_BLOCKED)
        if include_dead:
            statuses.append(sq.STATUS_DEAD)
        ph = ",".join("?" * len(statuses))
        q = f"SELECT * FROM submit_ready WHERE status IN ({ph})"
        ps = list(statuses)
        if region:
            q += " AND region=?"
            ps.append(region)
        rows = [dict(r) for r in con.execute(q, ps).fetchall()]
        rows.sort(key=lambda r: (r.get("region") or "", r.get("alpha_id") or ""))
        return rows
    finally:
        con.close()


def queue_snapshot(db_path=None):
    """各状态计数，供报告对照（确认同步没有误伤）。"""
    from wqb.store import submit_queue as sq
    con = sq.connect(db_path)
    try:
        return {r["s"]: r["n"] for r in con.execute(
            "SELECT status AS s, COUNT(*) AS n FROM submit_ready GROUP BY status")}
    finally:
        con.close()


def alpha_corr_meta(alpha_id, db_path=None):
    """相关性实测时间戳（新鲜度判据来源；无记录返回 None）。

    2026-10-05 单源化：改走 ``store.get_corr_authoritative``——权威表
    ``alpha_corr_cache`` 优先，缺条目回落 ``alphas``。此前本函数只查
    ``alphas.corr_checked_at``，于是「实测值只写在权威表」的候选（实测 6 颗 GBR）
    被判「无新鲜度依据」→ 强制重打平台单并发队列 → 撞 ``correlation_busy`` → 降级
    ``CORR_UNKNOWN``，尽管本地就躺着当天的平台实测值。
    """
    try:
        from wqb.store import CampaignStore
        st = CampaignStore(db_path) if db_path else CampaignStore.from_workspace()
        try:
            rec = st.get_corr_authoritative(alpha_id)
        finally:
            st.close()
        if not rec or rec.get("checked_at") is None:
            return None
        return {"corr_checked_at": rec.get("checked_at"),
                "source": rec.get("source"),
                "age_hours": rec.get("age_hours"),
                "stale": rec.get("stale")}
    except Exception:  # noqa: BLE001 - 库不可用时按「无新鲜度依据」处理
        return None


def alpha_corr_cache_row(alpha_id, db_path=None):
    """相关性实测值（第二级复用源）；无该表或无此 alpha 返回 None。

    2026-10-05：与 :func:`alpha_corr_meta` 一样改走**单源读**
    ``get_corr_authoritative``，权威表缺条目时回落 ``alphas``（返回里
    ``from_alphas=True``），不再只查 ``alpha_corr_cache`` 一张表。
    """
    try:
        from wqb.store import CampaignStore
        st = CampaignStore(db_path) if db_path else CampaignStore.from_workspace()
        try:
            rec = st.get_corr_authoritative(alpha_id)
        finally:
            st.close()
        if not rec or rec.get("prod_correlation") is None:
            return None
        return {"prod": rec.get("prod_correlation"),
                "self": rec.get("self_correlation"),
                "checked_at": rec.get("checked_at"),
                "source": rec.get("source"),
                "age_hours": rec.get("age_hours"),
                "stale": rec.get("stale"),
                "from_alphas": rec.get("from_alphas", False)}
    except Exception:  # noqa: BLE001 - 权威表可能不存在
        return None


# ---------------- 塔位（region/D{delay}/{category} + 倍率） ----------------

def _read_pyramid_cache():
    """读 24h 内的本地塔倍率缓存；过期/缺失/损坏返回 None。"""
    try:
        obj = json.loads(PYRAMID_CACHE.read_text(encoding="utf-8"))
        age = _age_hours(obj.get("checked_at"))
        if age is not None and age <= PYRAMID_TTL_H:
            return obj.get("table", {})
    except (OSError, ValueError):
        pass
    return None


def _write_pyramid_cache(table):
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = PYRAMID_CACHE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"checked_at": _now_iso(),
                               "count": len(table), "table": table},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, PYRAMID_CACHE)


def _parse_pyramid_payload(payload):
    """平台返回 → ``{"USA/D1/model": 1.3, ...}``（键小写，供 lookup_multiplier 查）。"""
    from wqb.towers import category_key
    table = {}
    for p in (payload.get("pyramids") if isinstance(payload, dict) else None) or []:
        if not isinstance(p, dict):
            continue
        rg = str(p.get("region") or "").strip().upper()
        try:
            dl = int(p.get("delay"))
        except (TypeError, ValueError):
            continue
        cat = p.get("category")
        cid = cat.get("id") if isinstance(cat, dict) else cat
        m = p.get("multiplier")
        if not rg or not cid or not isinstance(m, (int, float)):
            continue
        table[f"{rg}/D{dl}/{category_key(str(cid))}"] = float(m)
    return table


async def load_pyramid_multipliers(brain, force=False):
    """平台塔倍率表 → ``{"USA/D1/model": 1.3, ...}``，本地缓存 24h。

    结算倍率以平台塔表为准（``get_pyramid_multipliers``）；本地
    ``datasets.pyramid_multiplier`` 是 S0 catalog 抓的数据集级值，与塔表不一致
    （实测 EUR/D1/MODEL：dataset 1.6 vs 塔表 1.3），仅作兜底。
    失败静默返回空表——盘点绝不能因塔倍率取不到而中断。
    """
    cached = _read_pyramid_cache()
    if cached and not force:
        return cached
    try:
        payload = await brain.get_pyramid_multipliers()
    except Exception:  # noqa: BLE001 - 网络/端点失败
        return cached or {}
    table = _parse_pyramid_payload(payload)
    if table:
        _write_pyramid_cache(table)
        return table
    return cached or {}


def resolve_tower(row, pyr_table, field_idx_cache):
    """解析一颗候选的塔位。

    优先级：① 台账 ``towers`` 列（归一化后非空）→ ② 表达式反推
    （平台对 UNSUBMITTED alpha 的 pyramids/category 均为 null，见 wqb.towers）。
    倍率：① 平台塔表 → ② 数据集级 pyramid_multiplier。

    Returns: ``{"tower", "multiplier", "source", "dataset"}``
    """
    from wqb.store.submit_queue import normalize_towers
    from wqb.towers import infer_tower, lookup_multiplier, parse_tower

    region = row.get("region")
    parsed_tws = normalize_towers(row.get("towers"))
    mult = None
    dataset = None
    source = ""
    names = [n for n, _m in parsed_tws if n]
    if names:
        nm = names[0]
        mult = next((m for _n, m in parsed_tws if m is not None), None)
        parsed = parse_tower(nm)
        if parsed:
            m = lookup_multiplier(pyr_table, parsed[0], parsed[1], parsed[2])
            if m is not None:
                mult = m
        source = "台账"
    else:
        idx = field_idx_cache.get(region, "_missing_")
        if idx == "_missing_":
            from wqb.towers import field_index
            idx = field_index(region) or None
            field_idx_cache[region] = idx or "_missing_"
        inf = infer_tower(row.get("expr"), region, field_idx=idx) if idx else None
        if not inf:
            return {"tower": None, "multiplier": None, "source": "未知", "dataset": None}
        nm = inf["tower"]
        dataset = inf.get("dataset")
        mult = inf.get("dataset_multiplier")
        parsed = parse_tower(nm)
        if parsed:
            m = lookup_multiplier(pyr_table, parsed[0], parsed[1], parsed[2])
            if m is not None:
                mult = m
        source = "表达式反推"
    return {"tower": nm, "multiplier": mult, "source": source, "dataset": dataset}


def backfill_towers(aid, region, tower_name, multiplier, db_path=None):
    """把解析出的塔位写回 ``submit_ready.towers``（规范 JSON 形态，priority 可读倍率）。

    幂等：塔名已一致则不动；仅原值为空/无有效塔名时回填，不覆盖已有台账信息。
    """
    if not tower_name:
        return False
    from wqb.store import submit_queue as sq
    con = sq.connect(db_path)
    try:
        r = con.execute("SELECT towers FROM submit_ready WHERE alpha_id=? AND region=? LIMIT 1",
                        (aid, region)).fetchone()
        if not r:
            return False
        have = [n for n, _m in sq.normalize_towers(r[0]) if n]
        if have and have[0] == tower_name:
            return False
        rec = [{"name": tower_name}]
        if multiplier is not None:
            rec[0]["multiplier"] = multiplier
        cur = con.execute("UPDATE submit_ready SET towers=? WHERE alpha_id=? AND region=?",
                          (json.dumps(rec, ensure_ascii=False), aid, region))
        con.commit()
        return bool(cur.rowcount)
    finally:
        con.close()


# ---------------- 平台判定 ----------------

async def judge(brain, alpha_id):
    """模拟层 + Failed-count + 提交层（GET，平台恒 404）判定。永不 POST。"""
    from wqb.submit_verdict_core import decide, is_already_submitted, normalize_submit_layer
    detail = await brain.get_alpha_details(alpha_id)
    if is_already_submitted(detail):
        return {"detail": detail, "res": decide(alpha_id, detail)}
    resp = await brain._request("GET", f"{brain.base_url}/alphas/{alpha_id}/submit")
    body = resp.json() if (resp.status_code in (200, 403) and resp.text) else {}
    return {"detail": detail, "res": decide(
        alpha_id, detail, resp.status_code, normalize_submit_layer(resp.status_code, body))}


async def fetch_corr(brain, alpha_id, refresh, max_wait, retries=1):
    """拉 prod + self 相关性。busy 时按 retry_after 退避重试一次。

    返回 {'prod','self','from_cache','checked_at','status','source'}；失败 {'status': str(err)}。
    """
    try:
        pc = await brain.check_correlation(alpha_id, "both", 0.7, refresh=refresh)
    except Exception as e:  # noqa: BLE001
        return {"status": f"{type(e).__name__}:{str(e)[:120]}"}
    if pc.get("status") in ("pending", "correlation_busy", "data_unavailable"):
        ra = int(pc.get("retry_after") or 0)
        if pc.get("status") == "correlation_busy" and ra and ra <= max_wait and retries > 0:
            await asyncio.sleep(min(ra, max_wait))
            return await fetch_corr(brain, alpha_id, refresh, 0, retries - 1)
        return {"status": pc.get("status")}
    chk = pc.get("checks") or {}
    prod = (chk.get("production") or {}).get("max_correlation")
    selfc = (chk.get("self") or {}).get("max_correlation")
    # ★ self 回退（2026-10-05 修）：组合端点 check_correlation(...,"both") 对
    #   **未提交（UNSUBMITTED）** 的 alpha，self 腿恒返回空 —— 实测 `WjegEmQO`
    #   prod=0.5012 拿得到、self 却是 None，于是被误判 CORR_UNKNOWN（不可提交），
    #   而独立端点 check_self_correlation 明明给出 0.1616（与会话实测一致）。
    #   该端点走本地 OS PnL 池计算，几乎不占平台单并发队列，可安全回退。
    src = "platform_live"
    if selfc is None:
        try:
            sr = await brain.check_self_correlation(alpha_id, correlation_type="self")
            m = sr.get("max_correlation")
            if m is not None:
                selfc = m
                src = "platform_live+self_local_pool"
        except Exception:  # noqa: BLE001 - 回退失败不阻断，保持原 None
            pass
    return {"prod": prod, "self": selfc,
            "from_cache": bool((chk.get("production") or {}).get("from_cache")),
            "all_passed": pc.get("all_passed"), "status": "ok", "source": src}


def persist_live_corr(alpha_id, prod, selfc, db_path=None):
    """平台实测值回填 alphas 表（权威值，overwrite=True）。失败静默，不影响盘点。

    alpha_corr_cache 已由 check_correlation 内部写入，这里只补 alphas 表。
    """
    from wqb.store import CampaignStore
    store = None
    try:
        store = CampaignStore(db_path)
        return store.persist_correlation(
            alpha_id, prod, selfc, source="platform_sync", overwrite=True)
    except Exception:  # noqa: BLE001
        return {"skipped": "persist_error"}
    finally:
        if store is not None:
            try:
                store.close()
            except Exception:  # noqa: BLE001
                pass


# ---------------- 分类 ----------------

def corr_fresh(prod_age_h, self_age_h, stale_hours):
    """返回 (是否新鲜, 缺失/过期原因)。prod 与 self 都实测且在窗口内才算新鲜。"""
    if prod_age_h is None:
        return False, "prod 未实测"
    if self_age_h is None:
        return False, "self 未实测"
    bad = []
    if prod_age_h > stale_hours:
        bad.append(f"prod 已 {prod_age_h}h（>{stale_hours}h）")
    if self_age_h > stale_hours:
        bad.append(f"self 已 {self_age_h}h（>{stale_hours}h）")
    return (not bad), "；".join(bad)


def classify(res, prod, selfc, fresh, thin, lim_prod, lim_self):
    """七分类。返回 (bucket, reason_code, note)。"""
    verdict = res.get("verdict")
    if verdict == "ALREADY_SUBMITTED":
        return "ALREADY_SUBMITTED", "ALREADY_SUBMITTED", "平台已 ACTIVE/SUBMITTED，勿重复 POST"
    if verdict == "BLOCKED":
        return "HARD_BLOCKED", res.get("reason_code") or "BLOCKED", res.get("verdict_note") or ""
    # 模拟层 + Failed-count 干净，落到相关性维度
    p_bad = prod is not None and prod >= lim_prod
    s_bad = selfc is not None and selfc >= lim_self
    if p_bad or s_bad:
        return ("PROD_WALL", "FAIL:PROD" if p_bad else "FAIL:SELF",
                f"prod={prod} self={selfc}（线 {lim_prod}/{lim_self}）")
    # prod 或 self 缺失 = 无法确认通过（平台 SELF_CORRELATION 是真实闸）→ 只能判 CORR_UNKNOWN
    if prod is None or selfc is None:
        miss = "prod" if prod is None else "self"
        return ("CORR_UNKNOWN", "CORR_MISSING",
                f"{miss} 未实测（prod={prod} self={selfc}），不可判可提交")
    if not fresh:
        return "CORR_UNKNOWN", "CORR_STALE_OR_MISSING", "相关性已过期，须重测"
    p_margin = round(lim_prod - prod, 4)
    s_margin = round(lim_self - selfc, 4)
    margin = min(p_margin, s_margin)
    if margin < thin:
        return ("THIN_MARGIN", "THIN_MARGIN",
                f"全闸通过但余量 {margin} < {thin}（prod={prod} self={selfc}）")
    return "SUBMIT_NOW", "SUBMIT_NOW", f"prod={prod} self={selfc} 余量 {margin}"


# ---------------- 队列同步（幂等） ----------------

def sync_row(row, bucket, res, prod, selfc, do_sync, db_path=None, thin=0.03):
    """把盘点结论写回 submit_ready。状态已一致则跳过，避免 note 无限累加。"""
    out = {"alpha_id": row["alpha_id"], "bucket": bucket, "synced": False, "why": ""}
    if not do_sync:
        out["why"] = "no_sync_queue"
        return out
    from wqb.store import submit_queue as sq
    aid, region = row["alpha_id"], row.get("region")
    cur_status, cur_gate = row.get("status"), row.get("gate") or ""
    try:
        if bucket == "ALREADY_SUBMITTED":
            if cur_status == sq.STATUS_SUBMITTED:
                out["why"] = "already_SUBMITTED"
                return out
            r = sq.mark_blocked(aid, reason="ALREADY_SUBMITTED", region=region)
        elif bucket == "HARD_BLOCKED":
            reason = res.get("reason_code") or "BLOCKED"
            if cur_status == sq.STATUS_DEAD and cur_gate == reason:
                out["why"] = "already_DEAD_same_reason"
                return out
            r = sq.mark_blocked(aid, reason=reason, region=region,
                                note=res.get("verdict_note") or "")
        elif bucket == "PROD_WALL":
            reason = "FAIL:PROD" if (prod is not None and prod >= sq.LIM["prod"]) else "FAIL:SELF"
            if cur_status == sq.STATUS_PROD_BLOCKED and cur_gate == reason:
                out["why"] = "already_PROD_BLOCKED_same_reason"
                return out
            r = sq.mark_blocked(aid, reason=reason, status=sq.STATUS_PROD_BLOCKED, region=region,
                                note=f"盘点 prod={prod} self={selfc}")
        elif bucket == "CORR_UNKNOWN":
            # 相关性未取得不是新判据：不能把行降级成 READY 再刷个 UNVERIFIED 盖住原判据
            # （如 FAIL:PROD_SIBLING）。保留原 status/gate，只在 note 留痕（幂等：同 tag 不重复追加）
            tag = f"corr_未实测@{_now_iso()[:10]}"
            con = sq.connect(db_path)
            try:
                cur = con.execute(
                    "UPDATE submit_ready SET note=COALESCE(note,'')||? WHERE alpha_id=? "
                    "AND COALESCE(note,'') NOT LIKE '%'||?||'%'",
                    (f" | {tag}", aid, tag))
                con.commit()
                out["synced"] = bool(cur.rowcount)
                out["why"] = "noted_keep_original"
            finally:
                con.close()
            return out
        elif bucket in ("SUBMIT_NOW", "THIN_MARGIN"):
            # gate 保留 SUBMIT_LAYER_VERIFIED 前缀（供 LIKE 过滤），后附实测值与结论，
            # 避免下一轮把「余量 0.024」这类关键信息刷成裸标记
            base_margin = min(sq.LIM["prod"] - prod, sq.LIM["self"] - selfc)
            gate = ("SUBMIT_LAYER_VERIFIED: prod{:.4f}+self{:.4f} 余量{:.4f}".format(
                prod, selfc, base_margin))
            if bucket == "THIN_MARGIN":
                gate += f" 余量<{thin} 建议不提"
            n = sq.mark_verified(aid, region=region, gate=gate, source="submit_inventory",
                                 rec={"sharpe": res.get("sharpe"), "fitness": res.get("fitness"),
                                      "turnover": res.get("turnover"),
                                      "two_year": res.get("two_year"),
                                      "prod": prod, "self": selfc})
            out["synced"] = bool(n)
            out["why"] = "upgraded" if n else "unchanged_or_absent"
            return out
        else:
            out["why"] = "bucket_not_synced"
            return out
        out["synced"] = bool(r.get("changed"))
        out["why"] = r.get("why") or "downgraded"
        return out
    except Exception as e:  # noqa: BLE001 - 同步失败绝不影响盘点结果
        out["why"] = f"db_error:{type(e).__name__}"
        return out


# ---------------- 报告 ----------------

def print_report(rows, snapshot_before, snapshot_after, args, started_at, done_at):
    counts = {b: 0 for b in BUCKETS}
    for r in rows:
        counts[r["bucket"]] += 1
    bar = "=" * 100
    print(bar)
    print(f"候选 alpha 可提交性盘点   {started_at} → {done_at}   (stale={args.stale_hours}h"
          f", thin_margin={args.thin_margin})")
    print("⛔ 本脚本只读不提交：任何提交须用户逐次明示 + 平台配额 1 次/天/区")
    print(bar)
    print("分类                 数量")
    for b in BUCKETS:
        if counts[b]:
            print(f"  {b:<20}{counts[b]}")
    print(f"  {'TOTAL':<20}{sum(counts.values())}")

    print(bar)
    for b in BUCKETS:
        sub = [r for r in rows if r["bucket"] == b]
        if not sub:
            continue
        print(f"\n【{b}】{len(sub)} 颗")
        for r in sub:
            pm = f"{r['prod_margin']}" if r["prod_margin"] is not None else "n/a"
            sm = f"{r['self_margin']}" if r["self_margin"] is not None else "n/a"
            age = f"{r['corr_age_h']}h" if r["corr_age_h"] is not None else "never"
            tw = r.get("tower") or "塔位未知"
            tm = f" ×{r['tower_multiplier']:g}" if r.get("tower_multiplier") else ""
            print(f"  {r['alpha_id']:<10} {r['region']:<4} S={r['sharpe']} F={r['fitness']} "
                  f"2Y={r['two_year']} TO={r['turnover']} | prod={r['prod']} self={r['self']}"
                  f" 余量 P/S={pm}/{sm} | 相关性 {age}"
                  f"{' 新鲜' if r['fresh'] else ' 过期/缺失'}")
            print(f"      塔位: {tw}{tm}（{r.get('tower_source') or '-'}）"
                  f"{(' / ' + r['tower_dataset']) if r.get('tower_dataset') else ''}")
            if r["note"]:
                print(f"      └─ {str(r['note'])[:150]}")
            if r["verdict_note"]:
                print(f"      └─ 平台: {str(r['verdict_note'])[:150]}")

    if counts["SUBMIT_NOW"]:
        print("\n" + bar)
        print("▶ 需要用户决策（可提交候选）：")
        for r in rows:
            if r["bucket"] == "SUBMIT_NOW":
                tm = f" ×{r['tower_multiplier']:g}" if r.get("tower_multiplier") else ""
                print(f"   · {r['alpha_id']} ({r['region']})  塔={r.get('tower') or '未知'}{tm}  "
                      f"prod={r['prod']} self={r['self']}  S={r['sharpe']} F={r['fitness']}")
        print("  提交流程：用户明示 → 稳健性台账 → check_correlation(refresh=True) 终验"
              " → workflow_submit_alpha(confirm_submit=True)")
    else:
        print("\n" + bar)
        print("▶ 当前无「全闸通过 + 相关性新鲜 + 余量充足」的可提交候选。")

    print(bar)
    print(f"submit_ready 台账  盘前 {snapshot_before}")
    if args.sync_queue:
        print(f"submit_ready 台账  盘后 {snapshot_after}")
    else:
        print("submit_ready 台账  （--no-sync-queue，未改动）")
    print(bar)


def write_outputs(rows, counts, args, started_at):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    jpath = RESULTS_DIR / f"submit_inventory_{stamp}.json"
    payload = {"generated_at": _now_iso(), "started_at": started_at,
               "stale_hours": args.stale_hours, "thin_margin": args.thin_margin,
               "sync_queue": args.sync_queue, "counts": counts,
               "row_count": len(rows),
               "discipline": "read-only: no alpha was submitted; quota is 1/day/region",
               "rows": rows}
    jpath.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    if getattr(args, "no_csv", False):
        print(f"\n报告：{jpath.name}（{RESULTS_DIR}，按 --no-csv 仅输出 JSON，未生成 CSV）")
        return jpath, None
    cpath = RESULTS_DIR / f"submit_inventory_{stamp}.csv"
    cols = ["bucket", "alpha_id", "region", "tower", "tower_multiplier", "tower_source",
            "tower_dataset", "sharpe", "fitness", "two_year", "turnover",
            "prod", "self", "prod_margin", "self_margin", "corr_age_h", "fresh", "stale_reason",
            "verdict", "reason_code", "status_old", "synced", "sync_why", "note"]
    with cpath.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in cols})
    print(f"\n报告：{jpath.name} / {cpath.name}（{RESULTS_DIR}）")
    return jpath, cpath


# ---------------- 主流程 ----------------

async def run(args):
    _bootstrap()
    from brain_api import BrainApiClient
    from wqb.store import submit_queue as sq
    started_at = _now_iso()
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    rows_in = load_queue(region=args.region, include_prod_blocked=args.include_prod_blocked,
                         include_dead=args.include_dead, db_path=args.db)
    if args.limit:
        rows_in = rows_in[:args.limit]
    snapshot_before = queue_snapshot(args.db)
    print(f"读取 submit_ready：{len(rows_in)} 条待盘点"
          f"（region={args.region or 'ALL'}，sync_queue={args.sync_queue}）")

    ckpt = load_ckpt() if (not args.skip_corr and not args.no_ckpt) else {"corr": {}}
    ckpt["corr"] = ckpt.get("corr") or {}
    lim_prod, lim_self = sq.LIM["prod"], sq.LIM["self"]
    out_rows = []
    n_corr_called = 0
    # 塔倍率表（24h 本地缓存；取不到也不影响盘点）+ 字段索引缓存
    pyr_table = {} if args.skip_tower else await load_pyramid_multipliers(brain)
    field_idx_cache = {}
    if pyr_table:
        print(f"塔倍率表：{len(pyr_table)} 条（平台 get_pyramid_multipliers）")
    elif not args.skip_tower:
        print("塔倍率表：未取得（塔名仍可标，倍率回退数据集级值）")

    for i, row in enumerate(rows_in, 1):
        aid = row["alpha_id"]
        base = {"alpha_id": aid, "region": row.get("region"), "status_old": row.get("status"),
                "gate_old": row.get("gate"), "bucket": "ERROR", "verdict": None,
                "reason_code": None, "note": "", "verdict_note": "",
                "prod": row.get("prod"), "self": row.get("self"),
                "prod_margin": None, "self_margin": None,
                "corr_age_h": None, "fresh": False, "stale_reason": "",
                "sharpe": row.get("sharpe"), "fitness": row.get("fitness"),
                "two_year": row.get("two_year"), "turnover": row.get("turnover")}
        try:
            got = await judge(brain, aid)
        except Exception as e:  # noqa: BLE001
            base["note"] = f"get_alpha_details 失败：{type(e).__name__}: {str(e)[:120]}"
            out_rows.append(base)
            print(f"[{i}/{len(rows_in)}] {aid} ERROR {base['note'][:80]}")
            continue
        res, detail = got["res"], got["detail"]
        is_ = detail.get("is") or {}
        base.update({
            "verdict": res.get("verdict"), "reason_code": res.get("reason_code"),
            "verdict_note": res.get("verdict_note") or "",
            "platform_status": detail.get("status"), "is_ppa": res.get("is_ppa"),
            "failed_ra": res.get("failed_ra"), "failed_ppa": res.get("failed_ppa"),
            "sharpe": is_.get("sharpe", row.get("sharpe")),
            "fitness": is_.get("fitness", row.get("fitness")),
            "turnover": is_.get("turnover", row.get("turnover")),
            "two_year": is_.get("two_year_sharpe", row.get("two_year")),
        })

        # 塔位：台账 towers 列 → 表达式反推（平台 UNSUBMITTED alpha 无 pyramids/category）
        tw = resolve_tower(row, pyr_table, field_idx_cache) if not args.skip_tower else {}
        base.update({
            "tower": tw.get("tower"), "tower_multiplier": tw.get("multiplier"),
            "tower_source": tw.get("source") or "", "tower_dataset": tw.get("dataset"),
        })
        if args.sync_queue and tw.get("tower"):
            # 幂等：塔名已一致 / 已有非空台账值时不改动
            if backfill_towers(aid, row.get("region"), tw["tower"], tw["multiplier"], args.db):
                base["towers_backfilled"] = True
                _m = f" ×{tw['multiplier']:g}" if tw["multiplier"] else ""
                print(f"      [塔位回填] {aid} → {tw['tower']}{_m}（原台账 towers 为空/无有效塔名）")

        prod, selfc = base["prod"], base["self"]
        checked_at = None
        need_corr = (args.skip_corr is False) and base["verdict"] not in (
            "ALREADY_SUBMITTED", "BLOCKED")
        at_quota = args.max_corr > 0 and n_corr_called >= args.max_corr
        if need_corr and not at_quota:
            resolved = None  # (prod, selfc, checked_at, source)
            cached = ckpt["corr"].get(aid) or {}
            cache_age = _age_hours(cached.get("checked_at"))
            if (cached.get("prod") is not None and cache_age is not None
                    and cache_age <= args.stale_hours):
                # 一级复用源：checkpoint 里 48h 内有实测值 → 直接复用，不打平台
                resolved = (cached.get("prod"), cached.get("self"),
                            cached.get("checked_at"), "checkpoint")
            elif not args.refresh_all:
                # 二级复用源：alpha_corr_cache 的实测值（check_correlation 内部落库）。
                # 命中同样免打平台单并发队列。
                cc = alpha_corr_cache_row(aid, args.db) or {}
                cc_age = _age_hours(cc.get("checked_at"))
                if (cc.get("prod") is not None and cc_age is not None
                        and cc_age <= args.stale_hours):
                    prod_c = cc.get("prod")
                    # cache 里 self 缺失时保留 submit_ready 行的值（可能来自本轮实测）
                    self_c = cc.get("self") if cc.get("self") is not None else selfc
                    resolved = (prod_c, self_c, cc.get("checked_at"), "alpha_corr_cache")
                    ckpt["corr"][aid] = {"prod": prod_c, "self": self_c,
                                         "checked_at": cc.get("checked_at"),
                                         "all_passed": None,
                                         "source": "alpha_corr_cache"}
                    save_ckpt(ckpt)
            if resolved is not None:
                prod, selfc, checked_at = resolved[:3]
                base["corr_source"] = resolved[3]
                # ★ self 补齐（2026-10-05 修）：复用源常常只有 prod、没有 self
                #   （组合端点对 UNSUBMITTED alpha 的 self 腿恒空，实测 WjegEmQO）。
                #   此前直接沿用 None → 整颗被判 CORR_UNKNOWN、从「可提交」里消失。
                #   这里用本地 OS PnL 池端点补齐（不占平台单并发队列）。
                if prod is not None and selfc is None:
                    try:
                        sr = await brain.check_self_correlation(
                            aid, correlation_type="self")
                        m = sr.get("max_correlation")
                        if m is not None:
                            selfc = m
                            base["corr_source"] = resolved[3] + "+self_local_pool"
                            ckpt["corr"][aid] = {
                                **(ckpt["corr"].get(aid) or {}),
                                "prod": prod, "self": selfc,
                                "checked_at": checked_at}
                            save_ckpt(ckpt)
                            persist_live_corr(aid, prod, selfc, args.db)
                    except Exception:  # noqa: BLE001 - 补齐失败不阻断
                        pass
            else:
                n_corr_called += 1
                base["corr_source"] = "live"
                r = await fetch_corr(brain, aid, refresh=True, max_wait=args.busy_wait)
                if r.get("status") == "ok":
                    prod, selfc = r.get("prod"), r.get("self")
                    checked_at = _now_iso()
                    ckpt["corr"][aid] = {"prod": prod, "self": selfc,
                                         "checked_at": checked_at,
                                         "all_passed": r.get("all_passed")}
                    save_ckpt(ckpt)
                    if not r.get("from_cache"):
                        persist_live_corr(aid, prod, selfc, args.db)
                else:
                    base["note"] = f"相关性未取得：平台 {r.get('status')}"
                if args.sleep_sec > 0:
                    await asyncio.sleep(args.sleep_sec)
        elif need_corr:
            base["note"] = base["note"] or (
                f"跳过相关性：已达 --max-corr {args.max_corr}（--max-corr 0 表示不限）")

        meta = alpha_corr_meta(aid, args.db)
        db_checked_at = (meta or {}).get("corr_checked_at")
        checked_at = checked_at or db_checked_at or row.get("verified_at")
        age = _age_hours(checked_at)
        fresh, reason = corr_fresh(age if age is not None else None,
                                   age if age is not None else None, args.stale_hours)
        # prod / self 的实测时间同源（同一次 check_correlation），故共用 age
        bucket, reason_code, note = classify(res, prod, selfc, fresh, args.thin_margin,
                                             lim_prod, lim_self)
        base.update({
            "prod": prod, "self": selfc, "corr_checked_at": checked_at, "corr_age_h": age,
            "fresh": fresh, "stale_reason": reason or "", "bucket": bucket,
            "reason_code": reason_code,
            "note": (str(note) + ("；" + base["note"] if base["note"] else "")),
        })
        base["prod_margin"] = (round(lim_prod - prod, 4) if prod is not None else None)
        base["self_margin"] = (round(lim_self - selfc, 4) if selfc is not None else None)
        base["sync"] = sync_row(row, bucket, res, prod, selfc, args.sync_queue, args.db,
                                thin=args.thin_margin)
        base["synced"] = base["sync"]["synced"]
        base["sync_why"] = base["sync"]["why"]
        out_rows.append(base)
        print(f"[{i}/{len(rows_in)}] {aid:<10} {row.get('region','?'):<4} "
              f"{bucket:<16} prod={prod} self={selfc} {('fresh' if fresh else 'stale:' + reason)}")

    snapshot_after = queue_snapshot(args.db) if args.sync_queue else snapshot_before
    counts = {b: sum(1 for r in out_rows if r["bucket"] == b) for b in BUCKETS}
    print_report(out_rows, snapshot_before, snapshot_after, args, started_at, _now_iso())
    write_outputs(out_rows, counts, args, started_at)
    return 0


def build_parser():
    ap = argparse.ArgumentParser(
        description="候选 alpha 可提交性盘点（只读平台、只判不提交）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--region", help="只盘点该区域（如 GBR / IND / KOR）")
    ap.add_argument("--include-prod-blocked", action="store_true",
                    help="同时盘点 PROD_BLOCKED 行（默认只看 READY）")
    ap.add_argument("--include-dead", action="store_true",
                    help="同时复查 DEAD 行（成本高；用于发现平台闸变化）")
    ap.add_argument("--skip-corr", action="store_true",
                    help="不调用 check_correlation，只用库里已存值（最快，但相关性可能已过期）")
    ap.add_argument("--refresh-all", action="store_true",
                    help="忽略 checkpoint，全部强制 refresh=True 回源")
    ap.add_argument("--no-ckpt", action="store_true", help="忽略 checkpoint 缓存")
    ap.add_argument("--skip-tower", action="store_true",
                    help="不解析塔位（不调用 get_pyramid_multipliers；报告塔位列留空）")
    ap.add_argument("--sync-queue", dest="sync_queue", action="store_true", default=True,
                    help="把判定结果写回 submit_ready（默认开）")
    ap.add_argument("--no-sync-queue", dest="sync_queue", action="store_false",
                    help="只读，完全不动 submit_ready")
    # 保鲜窗口默认值来自 store 侧唯一事实源，避免 48h 数字在此硬编码漂移
    # （Redis 7 天 TTL 教训，见 docs/design/prod_corr_persistence_design_20260918.md §6.6）。
    from wqb.store._corr_cache import CORR_FRESH_HOURS
    ap.add_argument("--stale-hours", type=float, default=float(CORR_FRESH_HOURS),
                    help=f"相关性新鲜窗口（默认 {CORR_FRESH_HOURS:g}h；>该窗口视为过期）")
    ap.add_argument("--thin-margin", type=float, default=0.03,
                    help="余量低于该值判 THIN_MARGIN（默认 0.03）")
    ap.add_argument("--max-corr", type=int, default=0,
                    help="本轮最多调用几次 check_correlation（0=不限；该端点单并发，较慢）")
    ap.add_argument("--sleep-sec", type=float, default=2.0, help="两次相关性调用间隔（默认 2s）")
    ap.add_argument("--busy-wait", type=int, default=90,
                    help="correlation_busy 时最多等待多少秒后重试一次（默认 90）")
    ap.add_argument("--limit", type=int, default=0, help="只盘点前 N 条（调试用）")
    ap.add_argument("--db", help="指定 sqlite 路径（默认走 wqb 默认库）")
    ap.add_argument("--no-csv", dest="no_csv", action="store_true",
                    help="只输出 JSON，不生成 CSV（用于自动化 deliverable 只含 md+json）")
    return ap


def main():
    args = build_parser().parse_args()
    if args.stale_hours <= 0 or args.thin_margin < 0:
        print("参数错误：stale-hours 须 >0，thin-margin 须 >=0")
        return 2
    try:
        return asyncio.run(run(args))
    except KeyboardInterrupt:
        print("\n用户中断")
        return 130
    except Exception as e:  # noqa: BLE001 - 平台/鉴权失败归 3
        print(f"盘点失败：{type(e).__name__}: {e}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
