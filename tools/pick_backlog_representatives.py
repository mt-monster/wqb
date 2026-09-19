# -*- coding: utf-8 -*-
"""pick_backlog_representatives.py — 从积压里按骨架去重挑代表（只读）。

背景（2026-09-17 实测）：EUR 有 2,235 条 `gated` 从未回测（消化率 2%），
其中 1,891 条是 8/24-25 的陈货；而同族兄弟变体的 SELF 相关 0.9+，
**全量回测既浪费槽位又会产生自相残杀的候选**。骨架签名（`expressions.skeleton`，
2026-09-17 已全库回填）给出机械去重的依据。

本工具只读挑代表，产出可直接喂 `tools/mcp_7slot_batch.py --alpha-json` 的 JSON：

  python tools/pick_backlog_representatives.py --region EUR --out logs/eur_backlog_reps.json
  # 消费（示例，需人工确认后执行）：
  python tools/mcp_7slot_batch.py --alpha-json logs/eur_backlog_reps.json \
      --settings-json tracking/EUR/config/settings.json \
      --output-csv tracking/EUR/results/eur_backlog_reps.csv

策略：每个骨架取 `--per-skeleton` 条（默认 1，即每骨架只留一颗，避免自残）；
按骨架簇大小降序输出（大簇优先，因为大簇意味着重复投入最多）。
"""
import argparse
import collections
import json
import os
import sqlite3

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TK = os.path.join(REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "scripts")


def _apply_gate_filter(rows, region):
    """用当前门禁全量筛（catalog 感知）。返回 (通过行, 失败 id 列表, 统计)。

    2026-09-17 实测背景：EUR 2,235 条 gated 里 1,667 条（75%）会被加固后的闸拦下
    ——其中 1,430 条命中新增的结构判定（禁加权混合），即用户 09-13/09-16 定案的
    纪律从未在这批存量上生效过。**先筛再回测**可省 75% 槽位并避免产出违规形态。
    """
    import contextlib
    import io
    import sys
    sys.path.insert(0, TK)
    import gate
    from _lib.common import CampaignContext

    pc = json.load(open(os.path.join(TK, "..", "config", "platform_constraints.json"),
                        encoding="utf-8"))
    poison = [p for p in pc.get("poison_patterns", []) if p.get("severity", "block") == "block"]
    cdir = os.path.join(REPO, "tracking", region)
    with contextlib.redirect_stdout(io.StringIO()):
        ctx = CampaignContext(cdir)
    wl_cache = {}

    def wl(ds):
        if ds not in wl_cache:
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    wl_cache[ds] = gate.load_whitelist(ctx, ds)
            except Exception:
                wl_cache[ds] = None
        return wl_cache[ds]

    passed, failed, reasons = [], [], collections.Counter()
    for row in rows:
        rid, expr, ds = row[0], row[1], row[2]
        w = wl(ds)
        if w is None:
            failed.append(rid)          # 无 catalog 无法门禁 → 不得回测
            reasons["NO_CATALOG"] += 1
            continue
        o = gate.check_one(expr, w, ds, poison, pc)
        if o["pass"]:
            passed.append(row)
        else:
            failed.append(rid)
            for i in o["issues"]:
                reasons[i.split("]")[0].replace("[", "")] += 1
    return passed, failed, {"reasons": dict(reasons.most_common(6)),
                            "failed": len(failed)}


def _apply_drop(a, failed_ids):
    """把门禁失败者标 status='dropped'（纪律废弃终态）。

    三重守卫（对齐本仓迁移工具惯例 `normalize_wave_ids.py` 等）：
      ① 只动本 run 门禁实测失败的行；② 必须 `--db-backup`；
      ③ 保护态校验：仅 `alpha_id IS NULL` 且当前状态 == `--status` 的行可动
         （有 alpha 的行一旦被改状态会被重选/重烧配额）。
    外加：分批提交 + 每批 `rowcount` 校验 + ledger 台账留痕 + 前后分布核对。
    """
    import datetime
    import shutil

    if os.path.exists(a.db_backup):
        raise SystemExit(f"[拒绝] 备份目标已存在，避免覆盖历史备份：{a.db_backup}")
    shutil.copy2(a.db, a.db_backup)
    print(f"\n[备份] {a.db} → {a.db_backup}")

    conn = sqlite3.connect(a.db)
    conn.row_factory = sqlite3.Row
    before = dict(conn.execute(
        "SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status",
        (a.region,)).fetchall())

    # ② 保护态校验
    protected, candidates = [], []
    ids = list(dict.fromkeys(failed_ids))
    for i in range(0, len(ids), 500):
        chunk = ids[i:i + 500]
        q = "SELECT id, status, alpha_id FROM expressions WHERE id IN (%s)" % \
            ",".join("?" * len(chunk))
        for r in conn.execute(q, chunk):
            if r["alpha_id"]:
                protected.append((r["id"], "有 alpha_id"))
            elif r["status"] != a.status:
                protected.append((r["id"], f"状态已非 {a.status}（{r['status']}）"))
            else:
                candidates.append(r["id"])

    print(f"[裁决] 待标 dropped = {len(candidates)} 条；保护态跳过 = {len(protected)} 条")
    for pid, why in protected[:5]:
        print(f"   跳过 {pid}: {why}")
    if not candidates:
        print("[裁决] 无需变更（幂等：已全部 dropped 或全部受保护）")
        conn.close()
        return

    now = datetime.datetime.now().isoformat(timespec="seconds")
    done = 0
    for i in range(0, len(candidates), a.drop_batch_size):
        batch = candidates[i:i + a.drop_batch_size]
        q = ("UPDATE expressions SET status='dropped', updated_at=? "
             "WHERE status=? AND alpha_id IS NULL AND id IN (%s)" % ",".join("?" * len(batch)))
        conn.execute("BEGIN")
        cur = conn.execute(q, [now, a.status] + batch)
        n = cur.rowcount
        conn.commit()
        if n != len(batch):
            raise SystemExit(f"[中止] 批次 {i} rowcount={n} ≠ {len(batch)}（并发写入？已提交部分，请复查）")
        done += n
        print(f"  [batch] {i + len(batch)}/{len(candidates)} 已标 dropped")

    # 台账留痕（审计：什么时间、依据什么、多少条）
    conn.execute(
        "INSERT OR REPLACE INTO ledger_kv (region, key, value, created_at, updated_at) "
        "VALUES (?,?,?,?,?)",
        (a.region, "drop_batch_backlog_gate_filter",
         json.dumps({"count": done, "from_status": a.status, "to_status": "dropped",
                     "reason": "门禁实测失败（含加固后的结构加权混合判定）",
                     "tool": "tools/pick_backlog_representatives.py --apply-drop",
                     "at": now}, ensure_ascii=False), now, now))
    conn.commit()

    after = dict(conn.execute(
        "SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status",
        (a.region,)).fetchall())
    conn.close()
    print(f"[完成] 已标 dropped {done} 条")
    print(f"  状态分布 {a.region}: {before} → {after}")
    untouched = conn_alpha_check(a.db, candidates)
    print(f"  复核：本批中带 alpha_id 的行 = {untouched}（必须为 0）")


def conn_alpha_check(db_path, ids):
    """复核：本批被改的 id 里是否有 alpha_id 非空（必须 0）。"""
    conn = sqlite3.connect(db_path)
    n = 0
    for i in range(0, len(ids), 500):
        chunk = ids[i:i + 500]
        q = "SELECT COUNT(*) FROM expressions WHERE alpha_id IS NOT NULL AND id IN (%s)" % \
            ",".join("?" * len(chunk))
        n += conn.execute(q, chunk).fetchone()[0]
    conn.close()
    return n


def main():
    ap = argparse.ArgumentParser(description="积压按骨架去重挑代表（只读）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--status", default="gated", help="默认 gated（过闸未回测）")
    ap.add_argument("--per-skeleton", type=int, default=1)
    ap.add_argument("--max", type=int, default=0, help="总量上限（0=不限）")
    ap.add_argument("--gate-filter", action="store_true",
                    help="先用当前门禁全量筛：失败者不进挑选（2026-09-17 启用加固后的闸5）")
    ap.add_argument("--drop-list", default=None,
                    help="把门禁失败者 id 写入该文件（供裁决废弃，需人工确认后执行）")
    ap.add_argument("--apply-drop", action="store_true",
                    help="把门禁失败者标 status='dropped'（纪律废弃终态）。"
                         "必须同时给 --gate-filter 与 --db-backup；本run重算门禁，不信任旧 id 文件")
    ap.add_argument("--db-backup", default=None,
                    help="--apply-drop 必填：写库前把 DB 复制到该路径（不可逆操作的硬守卫）")
    ap.add_argument("--drop-batch-size", type=int, default=200)
    ap.add_argument("--db", default=os.path.join(REPO, "data", "wqb.db"))
    ap.add_argument("--out", required=True, help="输出 JSON（--alpha-json 可直接消费）")
    a = ap.parse_args()

    if a.apply_drop and not a.gate_filter:
        raise SystemExit("[拒绝] --apply-drop 必须与 --gate-filter 同用"
                         "（只能废弃本 run 门禁实测失败的行，不得凭旧 id 文件批量改状态）")
    if a.apply_drop and not a.db_backup:
        raise SystemExit("[拒绝] --apply-drop 必须给 --db-backup <路径>（不可逆写入的硬守卫）")

    conn = sqlite3.connect(a.db)
    rows = conn.execute(
        "SELECT id, expression, dataset, wave, skeleton FROM expressions "
        "WHERE region=? AND status=? AND expression IS NOT NULL AND expression<>'' "
        "ORDER BY id", (a.region, a.status)).fetchall()
    before_dist = dict(conn.execute(
        "SELECT status, COUNT(*) FROM expressions WHERE region=? GROUP BY status",
        (a.region,)).fetchall())
    conn.close()

    failed_ids, gate_stats = [], {}
    if a.gate_filter:
        rows, failed_ids, gate_stats = _apply_gate_filter(rows, a.region)
        print(f"门禁筛选：通过 {len(rows)} / 失败 {len(failed_ids)}"
              f"  失败原因={gate_stats.get('reasons', {})}")
        if a.drop_list:
            with open(a.drop_list, "w", encoding="utf-8") as f:
                json.dump(failed_ids, f)
            print(f"失败者 id 已写入 {a.drop_list}（{len(failed_ids)} 条，裁决需人工确认）")

    if a.apply_drop:
        _apply_drop(a, failed_ids)

    by_sk = collections.defaultdict(list)
    no_sk = 0
    for rid, expr, ds, wave, sk in rows:
        if not sk:
            no_sk += 1
            continue
        by_sk[sk].append({"expression": expr, "dataset": ds or "", "wave": wave or ""})

    print(f"{a.region}/{a.status} 积压 = {len(rows)} 条（无骨架 {no_sk} 条被跳过）")
    print(f"唯一骨架 = {len(by_sk)}  复用率 = {len(rows)/max(len(by_sk),1):.1f}")

    picked = []
    for sk, members in sorted(by_sk.items(), key=lambda kv: -len(kv[1])):
        picked.extend(members[:a.per_skeleton])
    if a.max:
        picked = picked[:a.max]

    top = sorted(by_sk.items(), key=lambda kv: -len(kv[1]))[:5]
    print("最大簇（簇大小 → 骨架）：")
    for sk, members in top:
        print(f"  {len(members):>5}  {sk[:86]}")
    print(f"\n挑选代表 = {len(picked)} 条（每骨架 {a.per_skeleton} 条）"
          f" → 相比全量省 {(1 - len(picked)/max(len(rows),1))*100:.0f}% 回测")

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(picked, f, ensure_ascii=False, indent=1)
    print(f"已写入 {a.out}")


if __name__ == "__main__":
    main()
