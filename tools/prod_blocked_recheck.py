# -*- coding: utf-8 -*-
"""prod_blocked_recheck.py — PROD_BLOCKED 候选的**平台实时**复核器。

为什么需要它
------------
PROD_BLOCKED = 「模拟层全过、仅 prod/self 撞 0.7 墙」。它不是废品：生产池会变，
池子松动后应能复活。但两拨数据的**恢复路径完全不同**：

  A 路径（自家撞墙）: 自己实测 prod>=0.7 → 只需重测自己的 prod，跌破 0.7 即复活。
  B 路径（兄弟带累）: prod 列是 None，被 `FAIL:PROD_SIBLING(<id>=<val>)` 顶死——
     判据是**同骨架兄弟的 prod**。而 `store._prod_wall_sibling` 判定兄弟时读的是
     **库内存量 prod**，项目铁律明确「库内 prod 会过期 → 提交前必实测」。
     故必须打平台取兄弟的实时 prod：兄弟松动才解锁。

不重构 `_prod_wall_sibling`（它服务离线零配额的 regrade），本工具在它之上补实时口径。

用法
----
  python tools/prod_blocked_recheck.py [--region KOR] [--dry-run] [--limit N]
      [--fresh]  # 忽略断点续跑

断点续跑：已完成的 alpha_id 记在 results/prod_blocked_recheck_ckpt.json，
重跑自动跳过（网络调用宝贵，且平台 prod 计算受单并发队列限制）。

退出码: 0=成功, 1=失败
运行环境: 网络子命令，走 MCP venv（复用 submit_queue.py 的 bootstrap）
"""
import argparse
import asyncio
import json
import os
import re
import sqlite3
import sys
import time

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RESULTS = os.path.join(_REPO, "results")
_CKPT = os.path.join(_RESULTS, "prod_blocked_recheck_ckpt.json")

_SIB_RE = re.compile(r"^FAIL:PROD_SIBLING\(([^=)]+)=([0-9.]+)\)")


def _mcp_venv_python():
    env = os.environ.get("WQ_PY")
    cands = [env, os.path.join(_REPO, "world-quant-brain-mcp", ".venv", "Scripts", "python.exe")]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return sys.executable


def _add_paths():
    for p in (os.path.join(_REPO, "src"),
              os.path.join(_REPO, "tools"),
              os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))):
        if p and p not in sys.path:
            sys.path.insert(0, p)


def _bootstrap_venv():
    """同 submit_queue.py：切到 MCP venv 并同步等待（Windows 上 os.execv 不是真替换）。"""
    if os.environ.get("WQB_PBR_BOOTSTRAPPED") == "1":
        return
    py = _mcp_venv_python()
    norm = lambda x: os.path.normcase(os.path.abspath(x))  # noqa: E731
    if py and norm(py) != norm(sys.executable):
        import subprocess
        env = dict(os.environ, WQB_PBR_BOOTSTRAPPED="1")
        sys.exit(subprocess.call([py] + sys.argv, env=env))


def _load_ckpt(fresh):
    if fresh or not os.path.isfile(_CKPT):
        return {}
    try:
        with open(_CKPT, "r", encoding="utf-8") as f:
            return json.load(f).get("done") or {}
    except Exception:
        return {}


def _save_ckpt(done):
    os.makedirs(_RESULTS, exist_ok=True)
    tmp = _CKPT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"done": done, "updated_at": time.time()}, f, ensure_ascii=False, indent=1)
    os.replace(tmp, _CKPT)


def _short(x, n=4):
    """把可能为 None 的平台数值截断成定长串（日志对齐用，不参与判定）。"""
    return "None" if x is None else f"{x:.{n}f}"


async def _live_prod(brain, aid):
    """平台实时相关性三元组 (prod_max, self_max, err)。失败/未算出 → None 而非 0。

    注意：不可用 0 兜底 —— 0 会被误判成「与生产池完全无关」而放行（虚假复活）。
    """
    prod = selfc = None
    err = ""
    try:
        p = await brain.get_production_correlation(aid)
        prod = p.get("max") if isinstance(p, dict) else None
    except Exception as e:  # noqa: BLE001
        err = f"prod:{str(e)[:80]}"
    try:
        r = await brain.check_self_correlation(aid, correlation_type="self")
        selfc = r.get("max_correlation") if isinstance(r, dict) else None
    except Exception as e:  # noqa: BLE001
        err = (err + " " if err else "") + f"self:{str(e)[:80]}"
    return prod, selfc, err


async def _sib_prod(brain, sib_id, cache):
    """取兄弟的实时 prod，带进程内缓存。

    多个兄弟受害者共享同一兄弟（实测 9qjPxmre 被 3 行点名、mLm2xG1K 被 2 行），
    而每次 PC 都要占平台单并发队列约 30s —— 不缓存等于同一笔相关性连测三遍。
    """
    if sib_id in cache:
        return cache[sib_id], "(缓存)"
    prod, _, err = await _live_prod(brain, sib_id)
    if prod is not None or not err:
        cache[sib_id] = prod
    return prod, err


async def _run(a):
    _bootstrap_venv()
    _add_paths()
    from brain_api import BrainApiClient
    from wqb.store import submit_queue as sq
    import submit_queue as sqcli

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    con = sq.connect()
    try:
        sq.ensure_table(con)
        rows = [r for r in sq.list_prod_blocked(region=a.region)]
        if a.limit:
            rows = rows[:a.limit]
    finally:
        con.close()

    if not rows:
        print("[recheck] 无 PROD_BLOCKED 候选" + (f"（region={a.region}）" if a.region else ""))
        return 0

    lim = sq.LIM.get("prod", 0.7)
    done = _load_ckpt(a.fresh)
    print(f"[recheck] 待复核 {len(rows)} 条 | 阈值 prod<{lim} 才复活"
          f" | 断点已完成 {len(done)} 条" + ("（dry-run 不写库）" if a.dry_run else ""))

    revived, still, skipped, errs = [], [], [], []
    sib_cache = {}  # 兄弟 id -> 实时 prod（平台 PC 单并发且慢，同兄弟必须复用）

    con = sq.connect()
    try:
        sq.ensure_table(con)
        for i, row in enumerate(rows, 1):
            aid = row.get("alpha_id")
            region = row.get("region")
            gate = row.get("gate") or ""
            m = _SIB_RE.match(gate)
            sib_id = m.group(1) if m else None
            path = "B/sibling" if sib_id else "A/own"

            if aid in done and not a.fresh:
                skipped.append(aid)
                continue

            # 1) 自身：平台拉取全量 IS 指标（含 two_year / sub_universe / cluster_test）+ 相关性
            try:
                rec = await sqcli._fetch(brain, aid)
            except Exception as e:  # noqa: BLE001
                errs.append((aid, f"fetch:{str(e)[:80]}"))
                continue

            own_prod, own_self, e = rec.get("prod"), rec.get("self"), ""
            if own_prod is None:
                own_prod, own_self, e = await _live_prod(brain, aid)

            # 2) B 路径：读兄弟的**实时** prod（同一兄弟常阻塞多行，认 _sib_prod 缓存）
            sib_live = None
            sib_note = ""
            if sib_id:
                sib_live, sib_note = await _sib_prod(brain, sib_id, sib_cache)

            rec["prod"] = own_prod
            rec["self"] = own_self
            rec["region"] = rec.get("region") or region

            # 3) 裁决
            if sib_id and sib_live is not None and sib_live >= lim:
                # 兄弟仍顶墙 → 显式保持 PROD_BLOCKED，刷新实测值但不得升 READY
                # （store._upsert 只看本条 prod，不知道兄弟实时状态，故本工具显式兜）
                note = f"recheck:{sib_id} 实测 prod={sib_live:.4f} 仍≥{lim}"
                if not a.dry_run:
                    con.execute(
                        "UPDATE submit_ready SET prod=?, self=?, gate=?, verified_at=?, note=? "
                        "WHERE alpha_id=? AND region=?",
                        (own_prod, own_self, f"FAIL:PROD_SIBLING({sib_id}={sib_live:.2f})",
                         sq._now(), note, aid, region))
                still.append((aid, f"兄弟 {sib_id} prod={sib_live:.4f} 未松动"))
                outcome = f"仍 PROD_BLOCKED（兄弟 {sib_id}={_short(sib_live)} 顶墙）"
            else:
                g = sq.enqueue(con, rec, note=f"prod_blocked recheck ({path})")
                newst_r = con.execute(
                    "SELECT status FROM submit_ready WHERE alpha_id=? AND region=?",
                    (aid, region)).fetchone()
                newst = newst_r[0] if newst_r else "?"
                if newst == "READY":
                    revived.append((aid, g))
                    outcome = f"★复活 READY（{g}）"
                else:
                    still.append((aid, f"仍 {newst}（{g}）"))
                    outcome = f"仍 {newst}（{g}）"

            done[aid] = {"path": path, "own_prod": own_prod, "sib": sib_id, "sib_prod": sib_live}
            if not a.dry_run:
                # 关键：dry-run 不得写断点 —— 否则正式跑会把「没真正落库」的行当已完成跳过
                _save_ckpt(done)
            print(f"  {i:2d}. [{path}] {aid:12s} {str(region):5s} "
                  f"自有prod={_short(own_prod)} 兄弟prod={_short(sib_live)} → {outcome}"
                  + (f" {sib_note}" if sib_note else "")
                  + (f" ERR={e}" if e else ""))
            if a.sleep:
                await asyncio.sleep(a.sleep)

        if a.dry_run:
            con.rollback()
        else:
            con.commit()
    finally:
        con.close()

    print("\n=== 汇总 ===")
    print(f"  复活 READY : {len(revived)}")
    for aid, g in revived:
        print(f"      {aid:12s} {g}")
    print(f"  仍阻塞     : {len(still)}")
    for aid, why in still:
        print(f"      {aid:12s} {why}")
    if skipped:
        print(f"  断点跳过   : {len(skipped)}")
    if errs:
        print(f"  取数失败   : {len(errs)}")
        for aid, e in errs:
            print(f"      {aid:12s} {e}")
    print("  （dry-run 未写入）" if a.dry_run else "  已写入")
    return 0


def main():
    p = argparse.ArgumentParser(description="PROD_BLOCKED 候选的平台实时复核（含兄弟实时 prod）")
    p.add_argument("--region", help="限定区域（不传=全部）")
    p.add_argument("--limit", type=int, help="只处理前 N 条")
    p.add_argument("--dry-run", action="store_true", help="不写库")
    p.add_argument("--fresh", action="store_true", help="忽略断点续跑，全部重跑")
    p.add_argument("--sleep", type=float, default=0.0, help="每条之间等待秒数（避开平台限流）")
    a = p.parse_args()
    return asyncio.run(_run(a))


if __name__ == "__main__":
    sys.exit(main())
