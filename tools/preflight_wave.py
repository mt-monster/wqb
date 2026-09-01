# -*- coding: utf-8 -*-
"""preflight_wave.py - 波次前置条件预检与自动修复（区域无关，通用）。

解决的问题：
  后续阶段（S2 门禁 / S3 回测）默认前置产物（S0/S1：字段 catalog、白名单）一定存在，
  但该前提无机制校验。续战/旧战役遗留/手工时代探索过的数据集常静默缺失，
  直到发批时才以 ERROR 连坐整批 CANCELLED 的形式爆炸。

检查项（每项输出 {check, status(PASS/WARN/FAIL), detail, remediation}）：
  settings      config/settings.json 可读且含 region
  catalog_file  reference/<region>_<dataset>_fields.json（或 legacy 白名单）存在（gate.py 消费）
  catalog_db    wqb.db 字段 catalog 存在（DB 为单一事实源）
  sync          文件与 DB 字段集一致（分叉即需修复）
  freshness     fetched_at 在 --ttl-days 内（过期仅 WARN，建议重扫）
  dead_end      数据集在 registry_empirical 判死清单中（续战需翻案证据，仅 WARN）

修复模式（--repair，幂等）：
  文件缺 + DB 有 → 从 DB 导出文件（合并文件中遗留的 banned_patterns 等）
  DB 缺 + 文件有 → 文件 upsert 入 DB
  双缺 / 过期    → 子进程跑 scan_fields.py 重扫后再入 DB
  分叉           → 以较新者（fetched_at）覆盖较旧者

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
import subprocess
import sys

DEFAULT_TTL_DAYS = 14


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


def _catalog_file_path(campaign_dir, region, dataset):
    ref = os.path.join(campaign_dir, "reference")
    cat = os.path.join(ref, f"{region.lower()}_{dataset}_fields.json")
    legacy = os.path.join(ref, f"{region.lower()}_{dataset}_field_whitelist.json")
    return cat if os.path.exists(cat) else (legacy if os.path.exists(legacy) else None)


def _read_catalog_file(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return None


def _file_field_set(catalog):
    if not isinstance(catalog, dict):
        return set()
    if "verified_fields" in catalog:  # legacy 白名单格式
        return set(catalog["verified_fields"])
    return {f.get("id") for f in catalog.get("fields", []) if f.get("id")}


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
        conn = sqlite3.connect(os.path.join(_wqb_root(), "data", "wqb.db"))
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


def repair_file_from_db(campaign_dir, region, dataset, db_cat):
    """DB → 文件：导出 catalog JSON（gate.py 消费面）。"""
    path = os.path.join(campaign_dir, "reference", f"{region.lower()}_{dataset}_fields.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    out = dict(db_cat)
    out.setdefault("fetched_at", datetime.datetime.now().isoformat(timespec="seconds"))
    out["exported_from_db_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    tmp = path + ".tmp"
    json.dump(out, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    os.replace(tmp, path)
    return path


def repair_db_from_file(region, file_cat):
    """文件 → DB：upsert_field_catalog（DB 为单一事实源）。"""
    st = _open_store()
    try:
        return st.upsert_field_catalog(region, file_cat)
    finally:
        st.close()


def repair_rescan(campaign_dir, dataset):
    """双缺/过期：重跑 scan_fields.py（需平台凭据），失败抛异常。"""
    scan = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_fields.py")
    r = subprocess.run([sys.executable, scan, "--campaign-dir", campaign_dir,
                        "--dataset", dataset],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"scan_fields 失败 rc={r.returncode}: {(r.stderr or r.stdout)[-400:]}")
    return r.stdout.strip()


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

    scan_cmd = (f"python tools/scan_fields.py --campaign-dir {campaign_dir} "
                f"--dataset {dataset}")
    preflight_repair = (f"python tools/preflight_wave.py --campaign-dir {campaign_dir} "
                        f"--dataset {dataset} --repair")

    # ---- 2/3) catalog 文件 + DB ----
    fpath = _catalog_file_path(campaign_dir, region, dataset)
    file_cat = _read_catalog_file(fpath) if fpath else None
    db_cat = None
    try:
        st = _open_store()
        try:
            db_cat = st.get_field_catalog(region, dataset)
        finally:
            st.close()
    except Exception as e:
        add("catalog_db", "WARN", f"DB 查询失败（不阻断）: {e}")

    if fpath and file_cat is not None:
        add("catalog_file", "PASS", f"{os.path.basename(fpath)} "
                                    f"({len(_file_field_set(file_cat))} 字段)")
    else:
        add("catalog_file", "FAIL", "reference 白名单/catalog 缺失（gate.py 5 闸将无法执行）",
            scan_cmd + f" 或 {preflight_repair}")
    if isinstance(db_cat, dict) and db_cat.get("fields"):
        add("catalog_db", "PASS", f"DB catalog {len(db_cat['fields'])} 字段")
    elif db_cat is None:
        add("catalog_db", "FAIL", "DB 字段 catalog 缺失（续战/历史数据集需补录）",
            preflight_repair)

    # ---- 4) 修复：缺失侧回灌 ----
    if repair:
        if (not fpath or file_cat is None) and isinstance(db_cat, dict) and db_cat.get("fields"):
            out = repair_file_from_db(campaign_dir, region, dataset, db_cat)
            fpath = out
            file_cat = _read_catalog_file(out)
            add("repair_file_from_db", "PASS", f"DB → 文件导出: {os.path.basename(out)}")
        elif fpath and file_cat is not None and not (isinstance(db_cat, dict) and db_cat.get("fields")):
            try:
                r = repair_db_from_file(region, file_cat)
                add("repair_db_from_file", "PASS", f"文件 → DB 入库: n={r.get('n')}")
                st = _open_store()
                try:
                    db_cat = st.get_field_catalog(region, dataset)
                finally:
                    st.close()
            except Exception as e:
                add("repair_db_from_file", "FAIL", f"入库失败: {e}")
        elif (not fpath or file_cat is None) and not (isinstance(db_cat, dict) and db_cat.get("fields")):
            try:
                repair_rescan(campaign_dir, dataset)
                fpath = _catalog_file_path(campaign_dir, region, dataset)
                file_cat = _read_catalog_file(fpath) if fpath else None
                if file_cat is not None:
                    repair_db_from_file(region, file_cat)
                    add("repair_rescan", "PASS", "重扫 + 入 DB 完成")
                else:
                    add("repair_rescan", "FAIL", "重扫后仍未产出 catalog 文件")
            except Exception as e:
                add("repair_rescan", "FAIL", str(e), scan_cmd)

    # ---- 5) sync：文件与 DB 字段集分叉 ----
    if fpath and file_cat is not None and isinstance(db_cat, dict) and db_cat.get("fields"):
        fs, ds = _file_field_set(file_cat), {f.get("id") for f in db_cat["fields"]}
        if fs == ds:
            add("sync", "PASS", f"文件与 DB 字段集一致（{len(fs)}）")
        else:
            add("sync", "WARN",
                f"文件与 DB 分叉：文件多 {len(fs - ds)} / DB 多 {len(ds - fs)}",
                preflight_repair + "（以较新 fetched_at 覆盖）")
            if repair:
                ft = _parse_ts(file_cat.get("fetched_at"))
                dt = _parse_ts(db_cat.get("fetched_at"))
                try:
                    if ft and dt and ft >= dt:
                        repair_db_from_file(region, file_cat)
                        add("repair_sync", "PASS", "文件较新 → 覆盖 DB")
                    else:
                        # 保留文件中独有的字段与附加键（banned_patterns 等）
                        merged = dict(db_cat)
                        for k in ("banned_patterns", "low_stock_coverage",
                                  "estimated_stock_count", "avg_coverage"):
                            if k in file_cat:
                                merged[k] = file_cat[k]
                        repair_file_from_db(campaign_dir, region, dataset, merged)
                        add("repair_sync", "PASS", "DB 较新（或无时间戳）→ 覆盖文件，保留文件附加键")
                except Exception as e:
                    add("repair_sync", "FAIL", str(e))

    # ---- 6) freshness ----
    ts = None
    for src in (file_cat, db_cat):
        if isinstance(src, dict) and src.get("fetched_at"):
            ts = ts or _parse_ts(src.get("fetched_at"))
    if ts is None:
        add("freshness", "WARN", "无 fetched_at 时间戳，无法判断新鲜度")
    else:
        age = (datetime.datetime.now() - ts).days
        if age > ttl_days:
            add("freshness", "WARN", f"catalog 已 {age} 天（TTL={ttl_days}），平台字段/竞争可能漂移",
                scan_cmd + f" 或 {preflight_repair}")
            if repair:
                try:
                    repair_rescan(campaign_dir, dataset)
                    f2 = _catalog_file_path(campaign_dir, region, dataset)
                    fc2 = _read_catalog_file(f2) if f2 else None
                    if fc2 is not None:
                        repair_db_from_file(region, fc2)
                        add("repair_refresh", "PASS", "过期重扫 + 入 DB 完成")
                except Exception as e:
                    add("repair_refresh", "FAIL", str(e), scan_cmd)
        else:
            add("freshness", "PASS", f"catalog 新近（{age} 天 ≤ TTL {ttl_days}）")

    # ---- 7) dead_end（续战翻案提示，仅 WARN）----
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
                    help="自动修复：文件↔DB 互灌 / 双缺重扫 / 过期刷新（幂等）")
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
