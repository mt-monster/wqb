#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""enqueue_propose.py — 入队「三层裁决」网关（L1 策略筛 → L2 择优 → L3 人工确认）。

★ 政策依据（2026-10-06 用户定案）
  **入队必须有人工/策略裁决**，不做「全闸即自动入队」。
  实测为什么要这样（2026-10-06）：`alphas` 里 S≥1.58/F≥1.0/prod<0.7 的未入队候选 393 条，
  直接全量入队的结局是 **251 条（64%）立即判 DEAD**（平台 RA 硬闸已 FAIL：
  LOW_ROBUST_UNIVERSE_RETURNS 87、LOW_ASI_JPN_SHARPE 28、LOW_2Y 13、IS_LADDER 12、ADD_MIX 22…）。
  ⇒ **「S/F≥线」是差前置；真正有效的判据是平台自己的 RA 检查**（`ra_failed_checks` 空）。

★ 三层
  **L1 硬前置（策略，自动筛）**
     a) 平台 RA 检查干净：`backtest_results.ra_failed_checks` 为空
     b) `sharpe ≥ --min-sharpe`（默认 1.58）且 `fitness ≥ --min-fitness`（默认 1.0）
     c) `two_year` 未知→放行（待核）；已知须 `≥ --min-2y`（默认 1.58）
     d) `turnover ≤ LIM['turnover_hi']`
     e) 非 add 混腿（闸5 毒化）
     f) `prod`/`self` 未知→放行（IS_ONLY）；已知须 `< --max-corr`（默认 0.7）
  **L2 择优（策略，控膨胀）**
     g) 同族只留代表：每 `(region, skeleton)` 取排序最高一条
     h) **塔优先**（2026-10-06 用户定案）：排序键 = ① 未点亮塔优先（当季 category ACTIVE < 3）
        ② 未点亮内缺口小者优先（差1 > 差2 > 0/3 打地基）③ 同档按 `priority()`（fitness×塔倍率＋相关余量）
     i) 可选 `--top-per-region N` 每区配额
  **L3 人工确认（本工具强制两段式）**
     - 提案模式（默认）：产出带 `proposal_id` + `content_hash` 的提案 JSON，**不写库**
     - 落库必须同时给 **`--apply --proposal <提案JSON> --approved-by <人>`**；
       校验 content_hash 未被改动、逐条重跑 L1（防陈旧）、可选 `--approve <id,id,...>` 只批子集；
       决策写入 `results/enqueue_decisions.jsonl` 审计台账。

★ 安全闸（防"复活已退役"）
  跳过 `submit_ready.status ∈ {SUBMITTED, DEAD, EXPIRED, SUPERSEDED}` 的行，且只处理尚未入队的 alpha。
  （2026-10-06 事故：`enqueue_from_alphas` 的 protected 不含 EXPIRED/SUPERSEDED，
    全量 upsert 曾复活 115 条 EXPIRED + 25 条 SUPERSEDED，已回滚。本工具不再走那条路径。）

用法:
  python tools/enqueue_propose.py                                  # L1+L2 提案（不写库）
  python tools/enqueue_propose.py --json results/enq.json          # 提案 + 落盘
  python tools/enqueue_propose.py --region GLB --top-per-region 5  # 单区 + 配额
  python tools/enqueue_propose.py --pyramid results/pyramid_latest.json   # 指定塔快照
  # ★ L3：人工确认后落库
  python tools/enqueue_propose.py --apply --proposal results/enq.json --approved-by bysone --reason "点塔优先，批 GLB 前 10"
  python tools/enqueue_propose.py --apply --proposal results/enq.json --approved-by bysone --approve kqonYg0L,e7bLOO2l
退出码: 0=正常  2=参数错误  3=DB 不可用  4=L3 校验失败（缺批准/哈希不符）
"""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from wqb.store import submit_queue as sq  # noqa: E402

DEF_MIN_SHARPE = 1.58
DEF_MIN_FITNESS = 1.0
DEF_MIN_2Y = 1.58
DEF_MAX_CORR = 0.7
DEF_PYRAMID = "results/pyramid_latest.json"
LEDGER = "results/enqueue_decisions.jsonl"
LIT_THRESHOLD = 3          # 当季 category ACTIVE ≥ 3 = 已点亮（仓库 skill 口径）
_CST = timezone(timedelta(hours=8))

#: 终态/已退役：绝不复活
_SKIP_STATUS = {"SUBMITTED", "DEAD", "EXPIRED", "SUPERSEDED"}


# ---------------- 基础设施 ----------------

def _connect(db=None) -> sqlite3.Connection:
    con = sq.connect(db) if db else sq.connect()
    con.row_factory = sqlite3.Row
    return con


def _root(p: str) -> str:
    """相对仓库根解析（脚本可能在任意 cwd 下被调）。"""
    if os.path.isabs(p):
        return p
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(repo, p)


# ---------------- 塔（金字塔） ----------------

class TowerMap:
    """读 `get_pyramid_alphas` 快照 + 表达式反推，给每条候选定塔、查 ACTIVE 数、判是否点亮。"""

    def __init__(self, path: str):
        self.ok = False
        self.table = {}
        self.idx_cache = {}
        try:
            with open(_root(path), encoding="utf-8") as fh:
                data = json.load(fh)
            self.table = data.get("pyramids") or {}
            self.lit_threshold = int(data.get("lit_threshold") or LIT_THRESHOLD)
            self.ok = bool(self.table)
        except Exception:  # noqa: BLE001 —— 快照缺失时降级为「无塔信息」，不阻断提案
            self.lit_threshold = LIT_THRESHOLD

    def _index(self, region):
        if region not in self.idx_cache:
            try:
                from wqb.towers import field_index
                self.idx_cache[region] = field_index(region)
            except Exception:  # noqa: BLE001
                self.idx_cache[region] = None
        return self.idx_cache[region]

    def lookup(self, expr, region):
        """→ dict(tower, category, delay, dataset, multiplier, count, lit, gap)"""
        blank = {"tower": None, "category": None, "delay": None, "dataset": None,
                 "multiplier": None, "count": None, "lit": None, "gap": None}
        if not self.ok or not expr or not region:
            return blank
        idx = self._index(region)
        if not idx:
            return blank
        try:
            from wqb.towers import infer_tower
            inf = infer_tower(expr, region, field_idx=idx)
        except Exception:  # noqa: BLE001
            return blank
        if not inf:
            return blank
        cat = (inf.get("category") or "").lower()
        delay = inf.get("delay") or 1
        cnt = ((self.table.get(region) or {}).get(f"D{delay}") or {}).get(cat)
        lit = None if cnt is None else (cnt >= self.lit_threshold)
        gap = None
        if cnt is not None:
            gap = {2: 0, 1: 1, 0: 2}.get(cnt, 3)   # 差1 > 差2 > 0/3 打地基；已点亮给 3
        return {"tower": inf.get("tower"), "category": inf.get("category"), "delay": delay,
                "dataset": inf.get("dataset"), "multiplier": inf.get("dataset_multiplier"),
                "count": cnt, "lit": lit, "gap": gap}


# ---------------- L1 ----------------

def _fetch_candidates(con, region=None):
    q = """
      SELECT a.alpha_id, r.name AS region, a.expression AS expr,
             a.sharpe, a.fitness, a.turnover,
             a.two_year_sharpe AS two_year, a.sub_universe_sharpe AS sub,
             a.prod_correlation AS prod, a.self_correlation AS selfc,
             (SELECT b.ra_failed_checks FROM backtest_results b
               WHERE b.alpha_id = a.alpha_id ORDER BY b.id DESC LIMIT 1) AS ra_failed,
             (SELECT sr.status FROM submit_ready sr
               WHERE sr.alpha_id = a.alpha_id LIMIT 1) AS q_status
        FROM alphas a LEFT JOIN regions r ON a.region_id = r.id
       WHERE a.alpha_id IS NOT NULL AND a.alpha_id <> ''
         AND COALESCE(a.soft_deleted,0)=0
         AND COALESCE(a.disposition,'') <> 'DEAD'
         AND a.status IN ('UNSUBMITTED','COMPLETE')
         AND COALESCE(a.platform_status,'') NOT IN ('ACTIVE','DECOMMISSIONED')
         AND a.date_submitted IS NULL
    """
    ps = []
    if region:
        q += " AND r.name = ?"
        ps.append(region)
    return [dict(r) for r in con.execute(q, ps).fetchall()]


def l1_check(row, min_sharpe, min_fitness, min_2y, max_corr):
    """L1 硬前置。返回 (通过?, 剔除理由)。"""
    st = (row.get("q_status") or "")
    if st in _SKIP_STATUS:
        return False, "ALREADY_" + st
    if st:
        return False, "ALREADY_IN_QUEUE(" + st + ")"
    if not row.get("region"):
        return False, "NO_REGION"
    rf = (row.get("ra_failed") or "").strip()
    if rf and rf not in ("[]", "null", "None"):
        return False, "RA_FAIL:" + (rf.strip("[]").split(",")[0].strip().strip('"') or "?")
    if sq.is_add_mix(row.get("expr")):
        return False, "ADD_MIX"
    s, f = row.get("sharpe"), row.get("fitness")
    if s is None or s < min_sharpe:
        return False, "LOW_SHARPE"
    if f is None or f < min_fitness:
        return False, "LOW_FITNESS"
    ty = row.get("two_year")
    if ty is not None and ty < min_2y:
        return False, "LOW_2Y"
    to = row.get("turnover")
    if to is not None and to > sq.LIM["turnover_hi"]:
        return False, "HIGH_TURNOVER"
    for k in ("prod", "selfc"):
        v = row.get(k)
        if v is not None and v >= max_corr:
            return False, ("PROD" if k == "prod" else "SELF")
    return True, ""


# ---------------- L2 ----------------

def _prio(r):
    """priority()：fitness × 塔倍率 + 相关余量 × 0.5。"""
    tw = "[]"
    if r.get("tower"):
        rec = {"name": r["tower"]}
        if r.get("multiplier") is not None:
            rec["multiplier"] = r["multiplier"]
        tw = json.dumps([rec], ensure_ascii=False)
    return sq.priority({"fitness": r.get("fitness"), "prod": r.get("prod"),
                        "self": r.get("selfc"), "towers": tw})


def _sort_key(r):
    """塔优先排序键：① 未点亮优先 ② 未点亮内缺口小者优先 ③ 同档按 priority。"""
    lit = r.get("lit")
    lit_flag = 0 if lit is False else (1 if lit is True else 1)   # 未知按已点亮处理（保守）
    gap = r.get("gap")
    gap_rank = gap if (lit is False and gap is not None) else 3
    return (lit_flag, gap_rank, -_prio(r))


def l2_select(rows, top_per_region=0):
    """同族只留代表 → （可选）每区配额。返回 (picked, n_groups)。"""
    groups = defaultdict(list)
    for r in rows:
        groups[(r["region"], sq._sig(r.get("expr")))].append(r)
    picked = []
    for _k, g in groups.items():
        picked.append(sorted(g, key=_sort_key)[0])
    if top_per_region > 0:
        by_reg = defaultdict(list)
        for r in picked:
            by_reg[r["region"]].append(r)
        picked = []
        for _reg, g in by_reg.items():
            picked.extend(sorted(g, key=_sort_key)[:top_per_region])
    picked.sort(key=_sort_key)
    return picked, len(groups)


# ---------------- L3 ----------------

def _content_hash(cands):
    """提案内容指纹：只覆盖「身份 + 关键指标」，保证批的是同一批东西。"""
    h = hashlib.sha256()
    for c in sorted(cands, key=lambda z: z["alpha_id"]):
        h.update(("|".join(str(c.get(k)) for k in
                           ("alpha_id", "region", "sharpe", "fitness", "prod", "self")).encode()))
    return h.hexdigest()[:16]


def _append_ledger(rec):
    path = _root(LEDGER)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------------- 主流程 ----------------

def _fmt(v, n=2, dash="—"):
    return dash if v is None else f"{v:.{n}f}"


def main() -> int:
    ap = argparse.ArgumentParser(description="入队三层裁决：L1 策略筛 → L2 择优 → L3 人工确认")
    ap.add_argument("--region", help="限单区（默认全库）")
    ap.add_argument("--min-sharpe", type=float, default=DEF_MIN_SHARPE)
    ap.add_argument("--min-fitness", type=float, default=DEF_MIN_FITNESS)
    ap.add_argument("--min-2y", type=float, default=DEF_MIN_2Y)
    ap.add_argument("--max-corr", type=float, default=DEF_MAX_CORR)
    ap.add_argument("--top-per-region", type=int, default=0, help="每区最多 N 条（0=不限）")
    ap.add_argument("--no-dedup", action="store_true", help="关掉 L2 同族只留代表")
    ap.add_argument("--pyramid", default=DEF_PYRAMID, help="塔快照 JSON（默认 results/pyramid_latest.json）")
    ap.add_argument("--no-tower", action="store_true", help="不做塔优先排序")
    # L3
    ap.add_argument("--apply", action="store_true", help="★ L3 落库（必须同时给 --proposal 与 --approved-by）")
    ap.add_argument("--proposal", help="L3：待批的提案 JSON 路径（提案模式产出）")
    ap.add_argument("--approved-by", help="L3：批准人（必填，留审计痕迹）")
    ap.add_argument("--reason", default="", help="L3：批准理由")
    ap.add_argument("--approve", default="", help="L3：只批这些 alpha_id（逗号分隔）；缺省=批全部")
    # 产出
    ap.add_argument("--json", dest="json_out", help="提案落盘 JSON 路径（默认自动带时间戳）")
    a = ap.parse_args()

    try:
        con = _connect()
    except sqlite3.Error as e:
        print(f"[ERROR] DB 不可用：{e}", file=sys.stderr)
        return 3

    try:
        sq.ensure_table(con)

        # ---------- L3 落库分支 ----------
        if a.apply:
            if not a.proposal or not a.approved_by:
                print("[L3 拒绝] --apply 必须同时给 --proposal <提案JSON> 与 --approved-by <人>。\n"
                      "         入队需人工裁决：先跑提案模式，审阅后再带这两项落库。", file=sys.stderr)
                return 4
            try:
                with open(_root(a.proposal), encoding="utf-8") as fh:
                    prop = json.load(fh)
            except Exception as e:  # noqa: BLE001
                print(f"[L3 拒绝] 提案文件不可读：{e}", file=sys.stderr)
                return 4
            cands = prop.get("candidates") or []
            stored = prop.get("content_hash")
            if stored != _content_hash(cands):
                print(f"[L3 拒绝] content_hash 不符（提案被改动过？stored={stored} "
                      f"now={_content_hash(cands)}）。请重新生成提案。", file=sys.stderr)
                return 4
            want = {x.strip() for x in a.approve.split(",") if x.strip()}
            if want:
                cands = [c for c in cands if c["alpha_id"] in want]
                print(f"[L3] 子集批准：{len(cands)} / {prop.get('proposal')} 条")
            return _do_apply(con, prop, cands, a)

        # ---------- 提案分支 ----------
        tw = TowerMap(a.pyramid)
        if not tw.ok and not a.no_tower:
            print(f"[WARN] 塔快照不可用（{a.pyramid}）；跳过塔优先排序，仅按 priority。", file=sys.stderr)

        raw = _fetch_candidates(con, a.region)
        l1, killed = [], Counter()
        for r in raw:
            ok, why = l1_check(r, a.min_sharpe, a.min_fitness, a.min_2y, a.max_corr)
            if not ok:
                killed[why.split(":")[0] if why.startswith("RA_FAIL") else why] += 1
                continue
            inf = {"tower": None, "count": None, "lit": None, "gap": None, "multiplier": None,
                   "category": None, "delay": None, "dataset": None, "multiplier": None}
            if not a.no_tower:
                inf = tw.lookup(r.get("expr"), r.get("region"))
            r.update(inf)
            l1.append(r)

        if a.no_dedup:
            picked, n_groups = sorted(l1, key=_sort_key), len(l1)
        else:
            picked, n_groups = l2_select(l1, a.top_per_region)

        cands = [{"alpha_id": r["alpha_id"], "region": r["region"],
                  "sharpe": r.get("sharpe"), "fitness": r.get("fitness"),
                  "two_year": r.get("two_year"), "sub": r.get("sub"),
                  "prod": r.get("prod"), "self": r.get("selfc"),
                  "tower": r.get("tower"), "tower_count": r.get("count"),
                  "tower_lit": r.get("lit"),
                  "skeleton": sq._sig(r.get("expr"))} for r in picked]

        stamp = datetime.now(_CST)
        payload = {"proposal": stamp.strftime("enq-%Y%m%d-%H%M%S"),
                   "generated_at": stamp.strftime("%Y-%m-%dT%H:%M:%S%z"),
                   "applied": False, "scope": a.region or "全库",
                   "s0": len(raw), "l1": len(l1), "proposal_count": len(cands),
                   "killed": dict(killed),
                   "params": {"min_sharpe": a.min_sharpe, "min_fitness": a.min_fitness,
                              "min_2y": a.min_2y, "max_corr": a.max_corr,
                              "top_per_region": a.top_per_region, "dedup": not a.no_dedup,
                              "tower_aware": not a.no_tower, "pyramid": a.pyramid},
                   "content_hash": _content_hash(cands),
                   "candidates": cands}

        scope = a.region or "全库"
        print(f"=== enqueue_propose（{scope}）[L1+L2 提案] ===")
        print(f"S0 未入队候选（全 alphas）        : {len(raw)}")
        print(f"L1 平台RA干净+非毒化+2Y/TO/相关  : {len(l1)}")
        print(f"L2 同族只留代表（{n_groups} 骨架组）  : {len(picked)}")
        lit_n = sum(1 for c in cands if c["tower_lit"] is False)
        print(f"→ 提案 {len(cands)} 条 {dict(Counter(c['region'] for c in cands))}"
              f" | 其中指向未点亮塔 {lit_n} 条")
        if killed:
            print("L1 剔除理由 top10:")
            for k, v in killed.most_common(10):
                print(f"   {k:34} {v}")

        print(f"\n{'alpha_id':11}{'reg':5}{'S':>7}{'F':>7}{'2Y':>7}{'prod':>8}  "
              f"{'tower':16}{'ACT':>4} {'点':3} skeleton")
        print("-" * 118)
        for c in cands:
            ty = _fmt(c["two_year"])
            pd_ = _fmt(c["prod"], 4)
            tws = (c["tower"] or "—")[:16]
            flag = "亮" if c["tower_lit"] else ("未" if c["tower_lit"] is False else "?")
            print(f"{c['alpha_id']:11}{str(c['region']):5}{c['sharpe'] or 0:>7.2f}{c['fitness'] or 0:>7.2f}"
                  f"{ty:>7}{pd_:>8}  {tws:16}{str(c['tower_count'] if c['tower_count'] is not None else '—'):>4} "
                  f"{flag:3} {(c['skeleton'] or '')[:26]}")

        out = a.json_out or _root(os.path.join(
            "results", f"enqueue_proposal_{stamp.strftime('%Y%m%d-%H%M%S')}.json"))
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        print(f"\n[提案 JSON] {out}")
        print(f"[L3 待批] proposal={payload['proposal']} content_hash={payload['content_hash']}")
        print("  落库需：")
        print(f"    python tools/enqueue_propose.py --apply --proposal {os.path.relpath(out, _root('.'))} "
              f"--approved-by <你> [--approve id1,id2]")
        return 0
    finally:
        con.close()


def _do_apply(con, prop, cands, a) -> int:
    """L3：落库（已通过哈希与批准人校验）+ 写审计台账。"""
    print(f"=== enqueue_propose [L3 APPLY] 批准人={a.approved_by} "
          f"proposal={prop.get('proposal')} ===")
    con.execute("BEGIN")
    applied, skipped = [], Counter()
    for c in cands:
        row = con.execute(
            "SELECT a.expression, a.sharpe, a.fitness, a.turnover, a.two_year_sharpe, "
            "a.sub_universe_sharpe, a.prod_correlation, a.self_correlation, r.name AS region, "
            "(SELECT b.ra_failed_checks FROM backtest_results b WHERE b.alpha_id=a.alpha_id "
            " ORDER BY b.id DESC LIMIT 1) AS ra_failed, "
            "(SELECT sr.status FROM submit_ready sr WHERE sr.alpha_id=a.alpha_id LIMIT 1) AS q_status "
            "FROM alphas a LEFT JOIN regions r ON a.region_id=r.id WHERE a.alpha_id=?",
            (c["alpha_id"],)).fetchone()
        if row is None:
            skipped["NOT_IN_ALPHAS"] += 1
            continue
        fresh = dict(row)
        fresh["expr"] = fresh.pop("expression")
        ok, why = l1_check(fresh, a.min_sharpe, a.min_fitness, a.min_2y, a.max_corr)
        if not ok:                      # 防陈旧：落库前逐条重跑 L1
            skipped[why.split(":")[0] if why.startswith("RA_FAIL") else why] += 1
            continue
        sq.enqueue(con, {
            "alpha_id": c["alpha_id"], "region": fresh["region"],
            "universe": None, "delay": None, "decay": None, "neutralization": None,
            "expr": fresh["expr"], "alpha_type": None,
            "sharpe": fresh["sharpe"], "fitness": fresh["fitness"],
            "turnover": fresh["turnover"], "two_year": fresh["two_year_sharpe"],
            "sub_universe": fresh.get("sub_universe_sharpe"),
            "prod": fresh["prod_correlation"], "self": fresh["self_correlation"],
            "ra_failed_checks": fresh["ra_failed"],
            "towers": json.dumps([{"name": c["tower"]}] if c.get("tower") else [],
                                 ensure_ascii=False),
            "verified_by": "alphas",
        }, note=f"enqueue-propose {a.approved_by} {datetime.now(_CST).strftime('%Y-%m-%d %H:%M')}")
        applied.append(c["alpha_id"])
    con.commit()

    rec = {"ts": datetime.now(_CST).strftime("%Y-%m-%dT%H:%M:%S%z"),
           "proposal": prop.get("proposal"), "content_hash": prop.get("content_hash"),
           "approved_by": a.approved_by, "reason": a.reason,
           "requested": len(cands), "applied": len(applied),
           "applied_ids": applied, "skipped": dict(skipped),
           "params": prop.get("params")}
    _append_ledger(rec)

    print(f"已入队 {len(applied)} 条" + (f"，跳过 {dict(skipped)}" if skipped else ""))
    print("台账:", dict(Counter(x[0] for x in con.execute(
        "SELECT status FROM submit_ready").fetchall())))
    print(f"[审计] 已写 {LEDGER}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
