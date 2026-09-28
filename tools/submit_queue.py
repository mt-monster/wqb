# -*- coding: utf-8 -*-
"""submit_queue.py - 待提交候选队列 CLI。

解决的问题
----------
每轮回测后找到的可提交 alpha，若不当天提交，之后极易遗忘。本工具把「已通过提交层闸门
的候选」持久化到本地库，并在每个 ET 日开始时可一键列出待提交项。

逻辑核心在 `src/wqb/store/submit_queue.py`（single source of truth），本文件只是 CLI 外壳。
同一份逻辑被三方共用：
  1. 本 CLI（人工取用）
  2. `tools/harvest_multisim.py`（S3 收批后自动入队）
  3. `src/wqb/workflow/nodes/submit_alpha.py`（提交成功后自动退役）

子命令
------
  init                建表（IF NOT EXISTS）
  add                 加入候选（从平台拉指标 + 相关性）
  add-many            从 `alphas` 表批量导入（离线、零配额）
  verify              复检相关性 + RA 硬闸（过期/变差则标记 EXPIRED/DEAD；先退役已 ACTIVE）
  sync                退役已在平台 ACTIVE/已提交的 READY 行（离线 alphas 表 + 平台 OS 列表）
  list                列出候选（默认仅 READY，按优先级）
  pick                输出最优先 1 条（供提交）
  regrade             离线复判 READY 行（RA 硬闸 / add 混腿 / prod 兄弟），零配额
  retire              退役（SUBMITTED / DEAD / EXPIRED）

退出码: 0=成功, 1=失败
运行环境: 网络子命令（add / verify）走 MCP venv
"""
import argparse
import json
import os
import sys

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, os.path.join(_REPO, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _add_paths():
    """把 src/ 与 MCP 目录加入 sys.path。"""
    for p in (os.path.join(_REPO, "src"),
              os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))):
        if p and p not in sys.path:
            sys.path.insert(0, p)


def _bootstrap_venv():
    """网络子命令：切到 MCP venv 重启进程。

    Windows 上 `os.execv` 不是真正的进程替换：父进程立刻退出（rc=0），子进程在后台继续跑，
    调用方用 `&&` 串联的下一条命令会抢在子进程前执行、输出也可能丢失（2026-09-20 实测 sync 后
    regrade 先跑）。故改为 subprocess 同步等待并透传退出码。"""
    if os.environ.get("WQB_SQ_BOOTSTRAPPED") == "1":
        return  # 已在 venv 子进程里（实测路径大小写不同会二次拉起，用环境标记兜底）
    py = _mcp_venv_python()
    norm = lambda x: os.path.normcase(os.path.abspath(x))  # noqa: E731
    if py and norm(py) != norm(sys.executable):
        import subprocess
        env = dict(os.environ, WQB_SQ_BOOTSTRAPPED="1")
        sys.exit(subprocess.call([py] + sys.argv, env=env))


def _sq():
    _add_paths()
    from wqb.store import submit_queue as sq
    return sq


# ---------------- 本地子命令 ----------------

def cmd_init(a):
    sq = _sq()
    con = sq.connect()
    try:
        sq.ensure_table(con)
        n = con.execute("SELECT COUNT(*) FROM submit_ready").fetchone()[0]
        con.commit()
    finally:
        con.close()
    print(f"[init] 表就绪，现有 {n} 条")
    return 0


def cmd_add_many(a):
    sq = _sq()
    n = sq.enqueue_from_alphas(region=a.region, min_sharpe=a.min_sharpe,
                               min_fitness=a.min_fitness, max_prod=a.max_prod,
                               dry_run=a.dry_run, dedup=not a.no_dedup,
                               max_per_skeleton=a.max_per_skeleton)
    print(f"[add-many] 入队 {n} 条" + ("（dry-run 未写入）" if a.dry_run else ""))
    return 0


def cmd_retag(a):
    """按当前规范重算队列所有行的 suggested_tags（规范升级后回填）。"""
    sq = _sq()
    if a.dry_run:
        n = sq.refresh_tags(region=a.region, dry_run=True)
        print(f"[retag] dry-run：{n} 行将更新（未写入）")
        return 0
    n = sq.refresh_tags(region=a.region)
    print(f"[retag] 已刷新 {n} 行的 suggested_tags")
    return 0


def cmd_dedup(a):
    """对现有队列按骨架去重（同骨架只留优先级最高的 N 条）。"""
    sq = _sq()
    d = sq.dedup_siblings(region=a.region, max_per_skeleton=a.max_per_skeleton,
                          dry_run=a.dry_run)
    tag = "dry-run 未写入" if a.dry_run else "已写入"
    print(f"[dedup] 骨架 {d['skeletons']} 个 | 保留 {d['kept']} | "
          f"标 SUPERSEDED {d['superseded']}（{tag}）")
    return 0


def cmd_list(a):
    sq = _sq()
    rows = sq.list_ready(region=a.region, all_status=a.all_status)
    if a.top:
        rows = rows[:a.top]
    scope = "全部状态" if a.all_status else "READY"
    print(f"=== 待提交队列（{scope}）：{len(rows)} 条 ===")
    if not rows:
        print("  （空）")
    for i, r in enumerate(rows, 1):
        tw = ""
        try:
            tl = json.loads(r.get("towers") or "[]")
            if tl:
                tw = ",".join(f"{t.get('name')}x{t.get('multiplier')}" for t in tl)
        except Exception:
            pass
        print(f"  {i:2d}. {str(r.get('alpha_id')):12s} {str(r.get('region')):5s} "
              f"sh={r.get('sharpe')} fit={r.get('fitness')} 2y={r.get('two_year')} "
              f"turn={r.get('turnover')} | prod={r.get('prod')} self={r.get('self')} "
              f"| {r.get('gate')} | prio={sq.priority(r)} | {tw}")
    return 0


def cmd_pick(a):
    sq = _sq()
    rows = sq.list_ready(region=a.region)
    if not rows:
        print("队列为空，无可提交候选")
        return 1
    print(json.dumps(rows[0], ensure_ascii=False, default=str, indent=1))
    return 0


def cmd_regrade(a):
    """离线复判 READY 行（闸门升级后清洗历史队列，零配额）。"""
    sq = _sq()
    d = sq.regrade_ready(region=a.region, dry_run=a.dry_run)
    tag = "dry-run 未写入" if a.dry_run else "已写入"
    print(f"[regrade] 复判 {d['checked']} 条 | 判死 {d['dead']} | 改动 {len(d['changes'])}（{tag}）")
    for aid, old_g, new_g in d["changes"]:
        print(f"  {aid:12s} {old_g} -> {new_g}")
    return 0


def cmd_retire(a):
    sq = _sq()
    if a.dry_run:
        print(f"[retire] dry-run：{a.alpha_id} → {a.status}（未写入）")
        return 0
    n = sq.retire(a.alpha_id, status=a.status, region=a.region)
    print(f"[retire] {a.alpha_id} → {a.status}（影响 {n} 条，已写入）")
    return 0 if n else 1


# ---------------- 网络子命令 ----------------

async def _fetch(brain, aid):
    d = await brain.get_alpha_details(aid)
    s = d.get("settings") or {}
    isv = d.get("is") or {}
    prod = selfc = None
    try:
        p = await brain.get_production_correlation(aid)
        prod = p.get("max") if isinstance(p, dict) else None
    except Exception:
        pass
    try:
        r = await brain.check_self_correlation(aid, correlation_type="self")
        selfc = r.get("max_correlation")
    except Exception:
        pass
    reg = d.get("regular")
    # 坑 1：平台 IS checks 的 FAIL 名单（robust / sub-universe / CW / ladder ...）随记录带入闸门
    ra_fails = [c.get("name") for c in (isv.get("checks") or [])
                if isinstance(c, dict) and c.get("result") == "FAIL"]
    return {
        "ra_failed_checks": ra_fails,
        "alpha_id": aid, "region": s.get("region"), "universe": s.get("universe"),
        "delay": s.get("delay"), "decay": s.get("decay"),
        "neutralization": s.get("neutralization"),
        "expr": reg.get("code") if isinstance(reg, dict) else None,
        "sharpe": isv.get("sharpe"), "fitness": isv.get("fitness"),
        "turnover": isv.get("turnover"), "two_year": isv.get("twoYearSharpe"),
        "sub_universe": isv.get("subUniverseSharpe"), "cluster_test": isv.get("clusterTest"),
        "prod": prod, "self": selfc,
        "towers": json.dumps(d.get("pyramids") or [], ensure_ascii=False),
    }


async def _cmd_add(a):
    _bootstrap_venv()
    _add_paths()
    from brain_api import BrainApiClient
    from wqb.store import submit_queue as sq
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    con = sq.connect()
    try:
        sq.ensure_table(con)
        for aid in a.alpha_id:
            rec = await _fetch(brain, aid)
            if not rec.get("region"):
                print(f"  {aid}: 取不到区域，跳过")
                continue
            gate = sq.enqueue(con, rec, note=a.note or "")
            print(f"  {aid} [{rec['region']}] sh={rec['sharpe']} fit={rec['fitness']} "
                  f"prod={rec['prod']} self={rec['self']} → {gate}")
        if a.dry_run:
            con.rollback()
            print("[add] dry-run，未写入")
        else:
            con.commit()
            print("[add] 已写入")
    finally:
        con.close()
    return 0


async def _platform_active_ids(brain, region=None, max_pages=30):
    """平台 OS 列表里的 alpha id（ACTIVE + DECOMMISSIONED 都算「已占坑」）。分页到空页为止。"""
    ids = []
    for page in range(max_pages):
        try:
            d = await brain.get_user_alphas(stage="OS", limit=100, offset=page * 100)
        except Exception as e:  # noqa: BLE001
            print(f"  [sync] 平台 OS 列表第 {page} 页拉取失败: {str(e)[:120]}")
            break
        rows = (d or {}).get("results") or []
        for r in rows:
            st = (r.get("settings") or {}).get("region")
            if region and st and st != region:
                continue
            if r.get("id"):
                ids.append(r["id"])
        if len(rows) < 100:
            break
    return ids


async def _sync_active(brain, sq, region=None):
    """坑 3：先离线（本地 alphas 表）再在线（平台 OS 列表）把已 ACTIVE 的 READY 行退役。返回 (离线数, 在线数)。"""
    n_local = sq.retire_platform_done(region=region)
    ids = await _platform_active_ids(brain, region=region)
    n_remote = sq.retire_active(ids, region=region) if ids else 0
    return n_local, n_remote


async def _cmd_sync(a):
    if a.offline:  # 纯本地，不切 venv、不访问平台
        sq = _sq()
        n = sq.retire_platform_done(region=a.region)
        print(f"[sync] 离线退役（本地 alphas 表 ACTIVE/已提交）: {n} 条")
        return 0
    _bootstrap_venv()
    _add_paths()
    from brain_api import BrainApiClient
    from wqb.store import submit_queue as sq
    brain = BrainApiClient()
    await brain.ensure_authenticated()
    n_local, n_remote = await _sync_active(brain, sq, region=a.region)
    print(f"[sync] 退役已 ACTIVE：离线 {n_local} 条 + 平台 OS 列表 {n_remote} 条")
    return 0


async def _cmd_verify(a):
    _bootstrap_venv()
    _add_paths()
    from datetime import datetime, timedelta
    from brain_api import BrainApiClient
    from wqb.store import submit_queue as sq

    brain = BrainApiClient()
    await brain.ensure_authenticated()
    if not a.no_sync and not a.dry_run:
        n_local, n_remote = await _sync_active(brain, sq, region=a.region)
        if n_local or n_remote:
            print(f"[verify] 先退役已 ACTIVE：离线 {n_local} + 平台 {n_remote} 条")
    con = sq.connect()
    try:
        sq.ensure_table(con)
        # verified_at 由 store._now() 写入 = **本地 naive** ISO 秒级串；cutoff 必须同口径，
        # 否则 UTC 串（差 8 小时 + 带 +00:00 后缀）做字符串比较会让当天验过的行永远不复检
        # （2026-09-20 实测 --max-age-days 0 → "待复检 0 条"）。
        cutoff = (datetime.now() - timedelta(days=a.max_age_days)).isoformat(timespec="seconds")
        q = "SELECT * FROM submit_ready WHERE status='READY'"
        ps = []
        if a.region:
            q += " AND region = ?"
            ps.append(a.region)
        q += " AND (verified_at IS NULL OR verified_at < ?)"
        ps.append(cutoff)
        rows = con.execute(q, ps).fetchall()
        print(f"[verify] 待复检 {len(rows)} 条（>{a.max_age_days} 天未验）")
        for r in rows:
            try:
                rec = await _fetch(brain, r["alpha_id"])
            except Exception as e:  # noqa: BLE001 —— 单条取数失败不拖垮整轮
                print(f"  {r['alpha_id']} 取数失败，跳过: {str(e)[:120]}")
                continue
            # 相关性接口失败时 _fetch 返回 None：不能拿 None 覆盖已实测值（会把
            # SUBMIT_LAYER_VERIFIED 降级成 IS_ONLY 且丢失 prod），跳过本条留待下轮
            if (rec["prod"] is None and r["prod"] is not None) or                (rec["self"] is None and r["self"] is not None):
                print(f"  {r['alpha_id']} 相关性接口失败（prod={rec['prod']} self={rec['self']}），保留旧值跳过")
                continue
            gate, st = sq.gate_of(rec["sharpe"], rec["fitness"], rec["two_year"],
                                  rec["turnover"], rec["prod"], rec["self"],
                                  rec.get("ra_failed_checks"), rec.get("expr") or r["expr"])
            if gate.startswith("FAIL"):
                # PROD/SELF 撞墙、RA 硬闸 FAIL、add 混腿 → DEAD；其余指标漂移 → EXPIRED
                hard = gate in ("FAIL:PROD", "FAIL:SELF") or gate.startswith(("FAIL:RA:", "FAIL:ADD_MIX"))
                st = sq.STATUS_DEAD if hard else sq.STATUS_EXPIRED
            con.execute(
                """UPDATE submit_ready SET sharpe=?,fitness=?,turnover=?,two_year=?,
                   prod=?,self=?,gate=?,verified_at=?,verified_by='verify',status=?
                   WHERE id=?""",
                (rec["sharpe"], rec["fitness"], rec["turnover"], rec["two_year"],
                 rec["prod"], rec["self"], gate, sq._now(), st, r["id"]))
            flag = "OK" if st == sq.STATUS_READY else f"!! {st}"
            print(f"  {r['alpha_id']} prod {r['prod']}→{rec['prod']} "
                  f"self {r['self']}→{rec['self']} {flag} ({gate})")
            if not a.dry_run:
                con.commit()  # 逐条落盘：网络抖动中途挂掉也不丢已验过的行
        if a.dry_run:
            con.rollback()
            print("[verify] dry-run 未写入")
        else:
            con.commit()
            print("[verify] 已写回")
    finally:
        con.close()
    return 0


def main():
    ap = argparse.ArgumentParser(description="待提交候选队列（回测过闸 → 持久化 → 取用）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="建表").set_defaults(fn=cmd_init)

    p = sub.add_parser("add", help="加入候选（从平台拉指标与相关性）")
    p.add_argument("--alpha-id", nargs="+", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=lambda a: __import__("asyncio").run(_cmd_add(a)))

    p = sub.add_parser("add-many", help="从 alphas 表批量导入（离线零配额）")
    p.add_argument("--region")
    p.add_argument("--min-sharpe", type=float)
    p.add_argument("--min-fitness", type=float)
    p.add_argument("--max-prod", type=float)
    p.add_argument("--no-dedup", action="store_true",
                   help="关闭入队后按骨架去重（默认开启）")
    p.add_argument("--max-per-skeleton", type=int, default=1,
                   help="同区域同骨架保留条数（默认 1）")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_add_many)

    p = sub.add_parser("dedup", help="对现有队列按骨架去重（同骨架留最优 N 条）")
    p.add_argument("--region")
    p.add_argument("--max-per-skeleton", type=int, default=1)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_dedup)

    p = sub.add_parser("retag", help="按当前规范重算队列的 suggested_tags（回填）")
    p.add_argument("--region")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_retag)

    p = sub.add_parser("verify", help="复检相关性 + RA 硬闸（过期/变差则标记；先自动退役已 ACTIVE）")
    p.add_argument("--region")
    p.add_argument("--max-age-days", type=int, default=7)
    p.add_argument("--no-sync", action="store_true", help="跳过「退役已 ACTIVE」预处理")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=lambda a: __import__("asyncio").run(_cmd_verify(a)))

    p = sub.add_parser("sync", help="退役已在平台 ACTIVE/已提交的 READY 行（离线 alphas 表 + 平台 OS 列表）")
    p.add_argument("--region")
    p.add_argument("--offline", action="store_true", help="只用本地 alphas 表，不访问平台")
    p.set_defaults(fn=lambda a: __import__("asyncio").run(_cmd_sync(a)))

    p = sub.add_parser("list", help="列出候选（默认仅 READY，按优先级）")
    p.add_argument("--region")
    p.add_argument("--top", type=int)
    p.add_argument("--all-status", action="store_true", help="含 DEAD/EXPIRED/SUBMITTED")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("pick", help="输出最优先 1 条")
    p.add_argument("--region")
    p.set_defaults(fn=cmd_pick)

    p = sub.add_parser("regrade", help="离线复判 READY 行（RA 硬闸 / add 混腿 / prod 兄弟），零配额")
    p.add_argument("--region")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_regrade)

    p = sub.add_parser("retire", help="退役")
    p.add_argument("--alpha-id", required=True)
    p.add_argument("--status", default="SUBMITTED",
                   choices=["SUBMITTED", "DEAD", "EXPIRED"])
    p.add_argument("--region")
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_retire)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
