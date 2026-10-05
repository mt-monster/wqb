# -*- coding: utf-8 -*-
"""preflight_wave.py - 波次前置条件预检与自动修复（区域无关，通用）。

解决的问题：
  后续阶段（S2 门禁 / S3 回测）默认前置产物（S0/S1：字段 catalog、白名单）一定存在，
  但该前提无机制校验。续战/旧战役遗留/手工时代探索过的数据集常静默缺失，
  直到发批时才以 ERROR 连坐整批 CANCELLED 的形式爆炸。

检查项（每项输出 {check, status(PASS/WARN/FAIL), detail, remediation}）：
  settings      config/settings.json 可读且含 region
  catalog_db    wqb.db 字段 catalog 存在（DB 为单一事实源，2026-10-01 起取消 reference 文件面）
  freshness     fetched_at 在 --ttl-days 内（过期仅 WARN，建议重扫）
  dead_end      数据集在 registry_empirical 判死清单中（续战需翻案证据，仅 WARN）

修复模式（--repair，幂等）：
  DB 缺 / 过期   → 直连平台 fetch + upsert_field_catalog 入库（不再经 reference JSON 中转）

用法:
  python tools/preflight_wave.py --campaign-dir tracking/IND --dataset behavioral_signals
  python tools/preflight_wave.py --campaign-dir tracking/IND --dataset behavioral_signals --repair
  python tools/preflight_wave.py --campaign-dir tracking/KOR --dataset model219 --wave 99 --ttl-days 30

退出码: 0=全 PASS（允许 WARN）, 1=存在 FAIL
"""
import argparse
import datetime
import json
import os
import sys

import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
DEFAULT_TTL_DAYS = 14

# toolkit 脚本目录（复用其标准 scan_fields 直连 DB 实现，避免本文件重复 fetch 逻辑）
_TOOLKIT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")


def _wqb_root():
    return (os.environ.get("WQB_ROOT") or os.environ.get("WQ_PROJECT_ROOT")
            or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_settings(campaign_dir):
    p = os.path.join(campaign_dir, "config", "settings.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def _open_store():
    root = _wqb_root()
    src = os.path.join(root, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from wqb.store import CampaignStore
    return CampaignStore(os.path.join(root, "data", "wqb.db"))


def _parse_ts(s):
    if not s or not isinstance(s, str):
        return None
    try:
        return datetime.datetime.fromisoformat(s)
    except Exception:
        return None


def check_dead_end(dataset, region):
    """查 registry_empirical dead_end 层，命中返回死路条目摘要；未命中/查不到返回 None。"""
    try:
        import sqlite3
        conn = db_connect(os.path.join(_wqb_root(), "data", "wqb.db"))
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT entry_id, family, payload, dead_at FROM registry_empirical "
            "WHERE layer='dead_end' AND region=?", (region,))
        hits = []
        for r in cur.fetchall():
            hay = " ".join(str(r[k]) for k in r.keys() if r[k] is not None)
            if dataset.lower() in hay.lower():
                hits.append({"entry_id": r["entry_id"], "family": r["family"],
                             "dead_at": r["dead_at"]})
        conn.close()
        return hits or None
    except Exception:
        return None


def repair_db_rescan(campaign_dir, dataset):
    """DB 缺 / 过期：直连平台 fetch 字段后直接 upsert_field_catalog（不经 JSON 中转）。

    复用 toolkit 标准 scan_fields 的 fetch_fields / build_catalog（platform API），
    再走 store.upsert_field_catalog 落库 —— 单进程、无 subprocess、无 reference 文件。
    """
    if _TOOLKIT not in sys.path:
        sys.path.insert(0, _TOOLKIT)
    import scan_fields  # toolkit 版（直连 GET /data-fields）
    from _lib.common import CampaignContext, load_credentials
    from _lib.api import Api

    ctx = CampaignContext(campaign_dir)
    email, pw = load_credentials()
    api = Api()
    api.login(email, pw)
    raw = scan_fields.fetch_fields(api, ctx.settings, dataset)
    cat = scan_fields.build_catalog(ctx.settings, dataset, raw)
    if not cat.get("fields"):
        raise RuntimeError(f"平台返回 0 字段：{ctx.region}/{dataset}")
    store = _open_store()
    try:
        return store.upsert_field_catalog(ctx.region, cat)
    finally:
        store.close()


def run_preflight(campaign_dir, dataset, repair=False, ttl_days=DEFAULT_TTL_DAYS):
    checks = []

    def add(name, status, detail, remediation=None):
        checks.append({"check": name, "status": status, "detail": detail,
                       "remediation": remediation})

    # ---- 1) settings ----
    settings = _load_settings(campaign_dir)
    if not settings or not settings.get("region"):
        add("settings", "FAIL", f"settings.json 缺失或无 region: {campaign_dir}",
            f"创建 {campaign_dir}/config/settings.json（region/universe/delay）")
        return checks  # 无 region 无法继续
    region = settings["region"]
    add("settings", "PASS", f"region={region} universe={settings.get('universe')} "
                            f"delay={settings.get('delay')}")

    preflight_repair = (f"python tools/preflight_wave.py --campaign-dir {campaign_dir} "
                        f"--dataset {dataset} --repair")

    # ---- 2) catalog（DB 为单一事实源；2026-10-01 起取消 reference 文件面）----
    db_cat = None
    db_err = None
    try:
        st = _open_store()
        try:
            db_cat = st.get_field_catalog(region, dataset)
        finally:
            st.close()
    except Exception as e:
        db_err = e

    # ---- 3) 修复：DB 缺失即直连重扫（在判定 catalog_db 之前，判定反映修复后状态）----
    if repair and not (isinstance(db_cat, dict) and db_cat.get("fields")):
        try:
            r = repair_db_rescan(campaign_dir, dataset)
            add("repair_rescan", "PASS", f"直连重扫 + 入 DB 完成: n={r.get('n')}")
            st = _open_store()
            try:
                db_cat = st.get_field_catalog(region, dataset)
            finally:
                st.close()
        except Exception as e:
            add("repair_rescan", "FAIL", str(e), preflight_repair)

    # ---- 4) catalog_db 判定（修复后状态）----
    if db_err is not None:
        add("catalog_db", "WARN", f"DB 查询失败（不阻断）: {db_err}")
    elif isinstance(db_cat, dict) and db_cat.get("fields"):
        add("catalog_db", "PASS", f"DB catalog {len(db_cat['fields'])} 字段")
    elif db_cat is None:
        add("catalog_db", "FAIL", "DB 字段 catalog 缺失（续战/历史数据集需补录）",
            preflight_repair)
    else:
        add("catalog_db", "FAIL", "DB 字段 catalog 为空（0 字段）", preflight_repair)

    # ---- 4) freshness ----
    ts = None
    if isinstance(db_cat, dict) and db_cat.get("fetched_at"):
        ts = _parse_ts(db_cat.get("fetched_at"))
    if ts is None:
        add("freshness", "WARN", "无 fetched_at 时间戳，无法判断新鲜度")
    else:
        age = (datetime.datetime.now() - ts).days
        if age > ttl_days:
            add("freshness", "WARN", f"catalog 已 {age} 天（TTL={ttl_days}），平台字段/竞争可能漂移",
                preflight_repair)
            if repair:
                try:
                    r = repair_db_rescan(campaign_dir, dataset)
                    add("repair_refresh", "PASS", f"过期重扫 + 入 DB 完成: n={r.get('n')}")
                except Exception as e:
                    add("repair_refresh", "FAIL", str(e), preflight_repair)
        else:
            add("freshness", "PASS", f"catalog 新近（{age} 天 ≤ TTL {ttl_days}）")

    # ---- 5) dead_end（续战翻案提示，仅 WARN）----
    hits = check_dead_end(dataset, region)
    if hits:
        ids = ", ".join(h.get("entry_id") or str(h.get("family")) for h in hits[:3])
        add("dead_end", "WARN",
            f"数据集在判死清单中（{ids}），续战需在台账登记翻案证据（新杠杆/新组合方向）")
    else:
        add("dead_end", "PASS", "未命中判死清单")

    return checks


def main():
    ap = argparse.ArgumentParser(description="波次前置条件预检与自动修复（S0/S1 产物门禁）")
    ap.add_argument("--campaign-dir", required=True, help="战役根目录 (如 tracking/IND)")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--wave", help="波号（仅记录用）")
    ap.add_argument("--repair", action="store_true",
                    help="自动修复：DB 缺/过期则直连重扫入库（幂等）")
    ap.add_argument("--ttl-days", type=int, default=DEFAULT_TTL_DAYS,
                    help=f"catalog 新鲜度 TTL（默认 {DEFAULT_TTL_DAYS} 天）")
    ap.add_argument("--quiet", action="store_true", help="只输出 JSON")
    a = ap.parse_args()

    checks = run_preflight(a.campaign_dir, a.dataset, repair=a.repair, ttl_days=a.ttl_days)
    fail = [c for c in checks if c["status"] == "FAIL"]
    warn = [c for c in checks if c["status"] == "WARN"]
    report = {
        "campaign_dir": a.campaign_dir, "dataset": a.dataset, "wave": a.wave,
        "repair": a.repair,
        "verdict": "FAIL" if fail else ("WARN" if warn else "PASS"),
        "checks": checks,
    }
    if not a.quiet:
        for c in checks:
            icon = {"PASS": "ok  ", "WARN": "warn", "FAIL": "FAIL"}[c["status"]]
            print(f"[{icon}] {c['check']:<20} {c['detail']}")
            if c["status"] != "PASS" and c.get("remediation"):
                print(f"       修复: {c['remediation']}")
        print(f"[done] verdict={report['verdict']} "
              f"({len(checks) - len(fail) - len(warn)} PASS / {len(warn)} WARN / {len(fail)} FAIL)")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
