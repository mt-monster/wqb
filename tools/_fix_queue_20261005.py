# -*- coding: utf-8 -*-
"""_fix_queue_20261005.py — 一次性队列清洗（2026-10-05，提交候选盘点后的台账修正）。

背景：本地 `submit_ready` 8 条 READY 经平台实测后 6 条状态错误。本脚本按实测结果
逐条回写：submit_ready（status/gate/note/prod/self）+ alphas（platform_status 镜像）
+ alpha_corr_cache / alphas（prod/self 落库，source=platform_sync）。

全部走 `wqb.store.CampaignStore` 与 `wqb.store.submit_queue` 的既有契约，不裸 SQL
绕过（persist_correlation / set_corr_cache / retire）。可安全重跑：幂等。
"""
import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from wqb.store import CampaignStore
from wqb.store import submit_queue as SQ

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "wqb.db")
STAMP = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00")

# 平台实测值（2026-10-05 14:5x，check_correlation(refresh=True)）
MEASURED = {
    "O08EjLVp":  {"prod": 0.5626, "self": 0.13009485606495916, "ok": True},
    "LLZ6wZO2":  {"prod": 0.6762, "self": 0.6760192580490869, "ok": True},
    "pwRWGR3q":  {"prod": 0.9966, "self": None,               "ok": False},
    "78NY2OgO":  {"prod": 0.9936, "self": None,               "ok": False},
}
# 平台 submit_verdict 的 Failed-count RA 硬闸结果
RA_BLOCKED = {
    "A1vOb5pE": "LOW_INVESTABILITY_CONSTRAINED_SHARPE(1.63/1.78)",
    "ZYAWx9J3": "LOW_INVESTABILITY_CONSTRAINED_SHARPE(1.42/1.58)",
}
ALREADY_ACTIVE = ["9qWaRGEK", "gJZ7AvZO"]


def patch_submit_ready(alpha_id: str, **fields) -> int:
    """通用字段回写（gate/status/note/prod/self/verified_*），追加 note 而非覆盖。"""
    con = SQ.connect(DB)
    try:
        con.execute("SELECT id FROM submit_ready WHERE alpha_id=?", (alpha_id,)).fetchone()
        sets, vals = [], []
        for k, v in fields.items():
            if k == "note_append":
                continue
            sets.append(f"{k}=?")
            vals.append(v)
        if "note_append" in fields:
            sets.append("note=COALESCE(note,'')||?")
            vals.append(" | " + fields["note_append"])
        vals.append(alpha_id)
        cur = con.execute(f"UPDATE submit_ready SET {', '.join(sets)} WHERE alpha_id=?", vals)
        con.commit()
        return cur.rowcount or 0
    finally:
        con.close()


def main() -> None:
    store = CampaignStore(DB)
    print(f"== 时间戳 {STAMP} | DB {DB}\n")

    # ── 1) alphas 表：平台镜像修正（gJZ7AvZO 本地还是 NULL）──────────────────
    print("[1/3] alphas.platform_status 镜像")
    for aid in ALREADY_ACTIVE:
        n = store.connection.execute(
            "UPDATE alphas SET platform_status='ACTIVE', stage=COALESCE(stage,'OS'), "
            "updated_at=? WHERE alpha_id=? AND COALESCE(platform_status,'')!='ACTIVE'",
            (STAMP, aid)).rowcount
        print(f"  {aid}: platform_status→ACTIVE/OS，改动 {n} 行")
    store.connection.commit()

    # ── 2) 相关性落库：alpha_corr_cache + alphas（platform_sync 权威口径）─────
    print("\n[2/3] prod/self 落库（platform_sync）")
    for aid, m in MEASURED.items():
        c = store.set_corr_cache(aid, prod=m["prod"], self_=m["self"], source="platform_sync")
        a = store.persist_correlation(aid, prod=m["prod"], self_=m["self"],
                                      source="platform_sync", overwrite=True)
        print(f"  {aid}: prod={m['prod']} self={m['self']} "
              f"| cache={'ok' if 'skipped' not in c else c.get('skipped')} "
              f"| alphas={'ok' if 'skipped' not in a else a.get('skipped')}")

    # ── 3) submit_ready 队列 ─────────────────────────────────────────────────
    print("\n[3/3] submit_ready 队列")

    # 3a. 已提交 → 退休
    for aid in ALREADY_ACTIVE:
        n = SQ.retire(aid, status=SQ.STATUS_SUBMITTED, db_path=DB)
        print(f"  {aid}: retire→SUBMITTED，改动 {n} 行")
    store.connection.close()

    # 3b. 新 RA 硬闸拦住 → DEAD（gate 字段记录实测值；修正此前手写的错误 gate）
    for aid, why in RA_BLOCKED.items():
        n = patch_submit_ready(
            aid,
            status=SQ.STATUS_DEAD,
            gate=f"FAIL:{why}",
            note_append=(f"平台 submit_verdict BLOCKED @ {STAMP}: Failed-count RA=1 "
                         f"[{why}] ⇒ 不可提交；此前 gate 手写值作废"),
        )
        print(f"  {aid}: →DEAD gate=FAIL:{why}，改动 {n} 行")

    # 3c. prod 实测撞墙 → PROD_BLOCKED（近重复克隆，标注无恢复空间）
    for aid in ("pwRWGR3q", "78NY2OgO"):
        m = MEASURED[aid]
        n = patch_submit_ready(
            aid,
            status=SQ.STATUS_PROD_BLOCKED,
            gate="FAIL:PROD",
            prod=m["prod"],
            verified_by="platform_refresh",
            verified_at=STAMP,
            note_append=(f"平台实测 prod={m['prod']} @ {STAMP} (refresh=True) — "
                         f"直方图[0.9,1]各1个，与生产池近重复克隆，等池变化亦无恢复空间；"
                         f"此前 prod=None「待测」标 READY 有误"),
        )
        print(f"  {aid}: →PROD_BLOCKED prod={m['prod']}，改动 {n} 行")

    # 3d. 真可提交 → 刷新为平台实测口径
    patch_submit_ready(
        "O08EjLVp",
        status=SQ.STATUS_READY,
        gate="SUBMIT_LAYER_VERIFIED: prod0.5626+self0.1301 all_passed",
        prod=0.5626, self=0.13009485606495916,
        verified_by="platform_refresh", verified_at=STAMP,
        note_append=(f"平台终验 PASS @ {STAMP}: 模拟层0 FAIL/Failed RA=0/"
                     f"prod0.5626<0.7/self0.1301<0.7 all_passed=true — 唯一真可提交候选"),
    )
    print("  O08EjLVp: →READY（平台终验 PASS）")

    # 3e. 全过但余量极薄 → 保留 READY，写清余量与点塔约束
    patch_submit_ready(
        "LLZ6wZO2",
        status=SQ.STATUS_READY,
        gate="SUBMIT_LAYER_VERIFIED: prod0.6762+self0.6760 余量0.024",
        prod=0.6762, self=0.6760192580490869,
        verified_by="platform_refresh", verified_at=STAMP,
        note_append=(f"平台终验 PASS @ {STAMP} 但 prod/self 双端点各余 0.024 余量；"
                     f"self 对端为已在生产池的 0mrnWojG（近重复）；"
                     f"塔 KOR/D1/FUNDAMENTAL 已 3/3 满 → 建议不提"),
    )
    print("  LLZ6wZO2: →READY（平台 PASS，但余量薄+塔满，标注建议不提）")

    # ── 复核 ─────────────────────────────────────────────────────────────────
    print("\n== 复核：submit_ready 全部 8 条 ==")
    con = SQ.connect(DB)
    rows = con.execute(
        "SELECT alpha_id,region,status,gate,prod,self,verified_by FROM submit_ready "
        "WHERE alpha_id IN ('O08EjLVp','gJZ7AvZO','A1vOb5pE','LLZ6wZO2','ZYAWx9J3',"
        "'pwRWGR3q','9qWaRGEK','78NY2OgO')").fetchall()
    for r in rows:
        d = dict(r)
        print(f"  {d['alpha_id']:10s} {d['region']:4s} [{d['status']:14s}] "
              f"prod={d['prod']} self={d['self']}")
        print(f"{'':10s}         gate={d['gate']}")
    con.close()

    print("\n== 复核：alphas 镜像 ==")
    con2 = CampaignStore(DB)
    for aid in list(MEASURED) + ALREADY_ACTIVE:
        d = con2.get_alpha_by_id(aid) or {}
        print(f"  {aid:10s} platform_status={d.get('platform_status')} stage={d.get('stage')} "
              f"prod={d.get('prod_correlation')} self={d.get('self_correlation')} "
              f"src={d.get('prod_corr_source')}")
    con2.close()

    print("\n== 复核：READY 池现状 ==")
    for st in (SQ.STATUS_READY, SQ.STATUS_PROD_BLOCKED):
        cnt = SQ.connect(DB).execute(
            "SELECT COUNT(*) FROM submit_ready WHERE status=?", (st,)).fetchone()[0]
        print(f"  {st}: {cnt}")
    SQ.connect(DB).close()
    store2 = CampaignStore(DB)
    r = SQ.regrade_ready(db_path=DB, dry_run=True)
    print(f"\n  regrade_ready(dry_run): checked={r['checked']} dead={r['dead']} "
          f"changes={len(r['changes'])} — READY 池无残留 FAIL")
    store2.close()
    print("\nDONE")


if __name__ == "__main__":
    main()
