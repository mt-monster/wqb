#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""daily_select.py — 每日最优候选选择器（配额约束 + 塔多样性 + 全指标合格）。

⛔ 铁律：本脚本**只读、只选不提交**——绝不 POST /alphas/{id}/submit。
   选定结果需用户逐次确认后手动提交。

选择流程
--------
1. **候选池** = submit_ready(READY) ∪ proposal JSON（L1 通过但尚未入队）
2. **全指标合格过滤**：S≥1.58, F≥1.0, 2Y≥1.58（若已知）, TO≤0.70,
   prod<0.7, self<0.7, 无 RA 硬闸 FAIL, 非 add_mix
3. **塔优先排序**：① 未点亮塔优先（lit=False）
   ② 未点亮内缺口小者优先（差1 > 差2 > 0/3）
   ③ 同档按 priority（fitness × 塔倍率 + 相关性余量 × 0.5）
4. **配额约束选择**（贪心 + 塔多样性）：
   a) 第一轮：每个 (region, tower) 只取最优者 → 最大化塔多样性
   b) 第二轮：若第一轮不足配额，从剩余候选补位
5. 输出每颗的选定理由（塔增益、余量、主题）

用法:
  python tools/verdict/daily_select.py                                      # 默认: submit_ready, REGULAR=4
  python tools/verdict/daily_select.py --regular-quota 4 --super-quota 1    # 指定配额
  python tools/verdict/daily_select.py --proposal results/enqueue_proposal_20261007.json
  python tools/verdict/daily_select.py --json results/daily_select_20261007.json
  python tools/verdict/daily_select.py --region GBR                          # 限单区
  python tools/verdict/daily_select.py --min-margin 0.03                     # 最低余量

退出码: 0=正常  2=参数错误  3=DB 不可用
"""
import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src"))

from wqb.store import submit_queue as sq  # noqa: E402
from wqb.expression.skeleton import extract_fields as _extract_fields  # noqa: E402

_CST = timezone(timedelta(hours=8))
DEF_REGULAR_QUOTA = 4
DEF_SUPER_QUOTA = 1
DEF_MIN_MARGIN = 0.0
LIT_THRESHOLD = 3

#: 终态/已退役：绝不复活
_SKIP_STATUS = {"SUBMITTED", "DEAD", "EXPIRED", "SUPERSEDED"}


def _root(p: str) -> str:
    if os.path.isabs(p):
        return p
    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(repo, p)


# ---------------- 塔位解析 ----------------

def _load_pyramid(path: str = "results/pyramid_latest.json") -> dict:
    """读金字塔快照 → {'USA': {'D1': {'MODEL': 4, ...}, ...}, ...}"""
    try:
        with open(_root(path), encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("pyramids") or {}
    except Exception:
        return {}


def _resolve_tower(row: dict, pyramid: dict, field_idx_cache: dict = None) -> dict:
    """解析一颗候选的塔位。

    优先级：① 台账 towers 列 → ② 表达式反推
    返回 {'tower', 'category', 'delay', 'multiplier', 'count', 'lit', 'gap'}
    """
    blank = {"tower": None, "category": None, "delay": None,
             "multiplier": None, "count": None, "lit": None, "gap": None}
    region = row.get("region")
    if not region:
        return blank

    # ① 台账 towers 列
    tower_name = None
    mult = None
    try:
        tw = json.loads(row.get("towers") or "[]")
        if tw:
            tower_name = tw[0].get("name")
            mult = tw[0].get("multiplier")
    except Exception:
        pass

    # ② 表达式反推（平台 UNSUBMITTED alpha 无 pyramids）
    if not tower_name:
        try:
            from wqb.towers import infer_tower, field_index
            if field_idx_cache is None:
                field_idx_cache = {}
            idx = field_idx_cache.get(region, "_missing_")
            if idx == "_missing_":
                idx = field_index(region) or None
                field_idx_cache[region] = idx or "_missing_"
            inf = infer_tower(row.get("expr"), region, field_idx=idx) if idx else None
            if inf:
                tower_name = inf.get("tower")
                if mult is None:
                    mult = inf.get("dataset_multiplier")
        except Exception:
            pass

    if not tower_name:
        return blank

    # 解析塔名 → (region, delay, category)
    parts = tower_name.split("/")
    if len(parts) < 3:
        return blank
    cat = parts[2].lower()
    try:
        delay = int(parts[1].replace("D", ""))
    except (ValueError, IndexError):
        delay = 1
    cnt = ((pyramid.get(region) or {}).get(f"D{delay}") or {}).get(cat)
    lit = None if cnt is None else (cnt >= LIT_THRESHOLD)
    gap = None
    if cnt is not None:
        gap = {2: 0, 1: 1, 0: 2}.get(cnt, 3)

    return {"tower": tower_name, "category": cat, "delay": delay,
            "multiplier": mult, "count": cnt, "lit": lit, "gap": gap}


# ---------------- 指标过滤 ----------------

def _pass_indicators(row: dict, min_sharpe: float, min_fitness: float,
                     min_2y: float, max_corr: float, min_margin: float) -> tuple:
    """全指标合格判定。返回 (通过?, 原因列表)。"""
    reasons = []

    s = row.get("sharpe")
    f = row.get("fitness")
    s2y = row.get("two_year")
    to = row.get("turnover")
    prod = row.get("prod")
    selfc = row.get("self")
    gate = (row.get("gate") or "")
    ra_failed = (row.get("ra_failed") or "").strip()

    # 硬闸
    if gate.startswith("FAIL"):
        reasons.append(f"GATE_FAIL:{gate}")
        return False, reasons

    # RA 硬闸
    if ra_failed and ra_failed not in ("[]", "null", "None"):
        reasons.append(f"RA_FAIL:{ra_failed.strip('[]')[:60]}")
        return False, reasons

    # 指标
    if s is None or s < min_sharpe:
        reasons.append(f"LOW_SHARPE({s or 'unknown'})")
        return False, reasons
    if f is None or f < min_fitness:
        reasons.append(f"LOW_FITNESS({f or 'unknown'})")
        return False, reasons
    if s2y is not None and s2y < min_2y:
        reasons.append(f"LOW_2Y({s2y})")
        return False, reasons
    if to is not None and to > sq.LIM["turnover_hi"]:
        reasons.append(f"HIGH_TURNOVER({to})")
        return False, reasons

    # 相关性
    if prod is not None and prod >= max_corr:
        reasons.append(f"PROD_WALL({prod})")
        return False, reasons
    if selfc is not None and selfc >= max_corr:
        reasons.append(f"SELF_WALL({selfc})")
        return False, reasons

    # 余量
    if prod is not None and selfc is not None:
        margin = min(sq.LIM["prod"] - prod, sq.LIM["self"] - selfc)
        if margin < min_margin:
            reasons.append(f"THIN_MARGIN({margin:.4f})")
            return False, reasons

    return True, reasons


# ---------------- 塔优先排序 ----------------

def _prio(row: dict) -> float:
    """priority()：fitness × 塔倍率 + 相关性余量 × 0.5。"""
    tw = "[]"
    if row.get("tower"):
        rec = {"name": row["tower"]}
        if row.get("multiplier") is not None:
            rec["multiplier"] = row["multiplier"]
        tw = json.dumps([rec], ensure_ascii=False)
    return sq.priority({"fitness": row.get("fitness"), "prod": row.get("prod"),
                        "self": row.get("self"), "towers": tw})


def _sort_key(row: dict):
    """塔优先排序键：① 未点亮优先 ② 缺口小者优先 ③ 同档按 priority。"""
    lit = row.get("lit")
    lit_flag = 0 if lit is False else 1   # 未知按已点亮处理（保守）
    gap = row.get("gap")
    gap_rank = gap if (lit is False and gap is not None) else 3
    return (lit_flag, gap_rank, -_prio(row))


# ---------------- 配额约束选择 ----------------

def _select_with_diversity(qualified: list, quota: int) -> list:
    """贪心选择：最大化塔多样性 + 配额约束。

    第一轮：每个 (region, tower) 只取最优者
    第二轮：若不足配额，从剩余候选补位
    """
    if not qualified or quota <= 0:
        return []
    if len(qualified) <= quota:
        return qualified[:quota]

    sorted_pool = sorted(qualified, key=_sort_key)
    selected = []
    used_combos = set()

    # 第一轮：每个 (region, tower) 只取最优
    for r in sorted_pool:
        if len(selected) >= quota:
            break
        combo = (r.get("region"), r.get("tower"))
        if combo not in used_combos:
            selected.append(r)
            used_combos.add(combo)

    # 第二轮：补位（允许塔位重复）
    if len(selected) < quota:
        selected_ids = {r["alpha_id"] for r in selected}
        for r in sorted_pool:
            if len(selected) >= quota:
                break
            if r["alpha_id"] not in selected_ids:
                selected.append(r)
                selected_ids.add(r["alpha_id"])

    return selected[:quota]


# ---------------- 理由生成 ----------------

def _reason_for(row: dict) -> str:
    """为选定候选生成人类可读的选定理由。"""
    parts = []

    # 塔
    tw = row.get("tower")
    if tw:
        lit = row.get("lit")
        gap = row.get("gap")
        act = row.get("count")
        if lit is False:
            gap_label = {0: "差1", 1: "差2", 2: "差3"}.get(gap, "已满")
            parts.append(f"未点亮 {tw} ({gap_label})")
        elif act is not None:
            parts.append(f"已点亮 {tw} (ACT={act})")
        else:
            parts.append(f"塔位 {tw}")

    # 塔倍率
    mult = row.get("multiplier")
    if mult is not None and mult > 1.0:
        parts.append(f"×{mult:g}倍率")

    # 相关性验证状态
    prod = row.get("prod")
    selfc = row.get("self")
    gate = (row.get("gate") or "")
    is_only = (prod is None and selfc is None) or ("IS_ONLY" in gate)
    if is_only:
        parts.append("⚠ 相关性未验证(IS_ONLY)")
    elif prod is not None and selfc is not None:
        margin = min(sq.LIM["prod"] - prod, sq.LIM["self"] - selfc)
        if margin < 0.03:
            parts.append(f"⚠ 余量仅{margin:.4f}(prod={prod:.4f},self={selfc:.4f})")
        else:
            parts.append(f"余量{margin:.4f}(prod={prod:.4f},self={selfc:.4f})")

    # 指标摘要
    s = row.get("sharpe")
    f = row.get("fitness")
    s2y = row.get("two_year")
    to = row.get("turnover")
    metrics = []
    if s:
        metrics.append(f"S={s:.2f}")
    if f:
        metrics.append(f"F={f:.2f}")
    if s2y and s2y > 0:
        metrics.append(f"2Y={s2y:.2f}")
    if to:
        metrics.append(f"TO={to:.3f}")
    if metrics:
        parts.append(",".join(metrics))

    # 主题/数据集
    family = row.get("family")
    if family:
        parts.append(f"主题:{family}")

    # 字段
    fields = row.get("fields")
    if fields:
        parts.append(f"字段:{','.join(fields[:3])}{'...' if len(fields) > 3 else ''}")

    return "; ".join(parts) if parts else "无额外信息"


# ---------------- 加载候选 ----------------

def _load_from_submit_ready(region=None) -> list:
    """从 submit_ready 加载 READY 行，join alphas 补充 expr 和 ra_failed。"""
    con = sq.connect()
    try:
        sq.ensure_table(con)
        con.row_factory = sqlite3.Row
        q = """SELECT sr.*, a.expression AS expr_full,
               (SELECT b.ra_failed_checks FROM backtest_results b
                WHERE b.alpha_id = sr.alpha_id ORDER BY b.id DESC LIMIT 1) AS ra_failed
               FROM submit_ready sr
               LEFT JOIN alphas a ON sr.alpha_id = a.alpha_id
               WHERE sr.status = 'READY'"""
        ps = []
        if region:
            q += " AND sr.region = ?"
            ps.append(region)
        rows = []
        for r in con.execute(q, ps).fetchall():
            row = dict(r)
            # 用 expr_full 覆盖 expr（submit_ready 的 expr 可能被截断）
            if row.get("expr_full"):
                row["expr"] = row.pop("expr_full")
            else:
                row.pop("expr_full", None)
            rows.append(row)
        return rows
    finally:
        con.close()


def _load_from_proposal(path: str) -> list:
    """从 enqueue_proposal JSON 加载 L1 通过的候选。"""
    try:
        with open(_root(path), encoding="utf-8") as fh:
            prop = json.load(fh)
        cands = []
        for c in prop.get("candidates") or []:
            row = {
                "alpha_id": c["alpha_id"],
                "region": c.get("region"),
                "sharpe": c.get("sharpe"),
                "fitness": c.get("fitness"),
                "two_year": c.get("two_year"),
                "turnover": c.get("turnover"),
                "prod": c.get("prod"),
                "self": c.get("self"),
                "tower": c.get("tower"),
                "lit": c.get("tower_lit"),
                "multiplier": c.get("multiplier"),
                "count": c.get("tower_count"),
                "skeleton": c.get("skeleton"),
                "fields": c.get("fields"),
                "expr": c.get("expr", ""),
                "ra_failed": None,
                "gate": "PROPOSAL",
                "source": "proposal",
            }
            cands.append(row)
        return cands
    except Exception as e:
        print(f"[WARN] 无法读取提案文件 {path}: {e}", file=sys.stderr)
        return []


# ---------------- 主流程 ----------------

def _fmt(v, n=2, dash="—"):
    return dash if v is None else f"{v:.{n}f}"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="每日最优候选选择器（配额约束 + 塔多样性 + 全指标合格）",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--region", help="限单区（默认全库）")
    ap.add_argument("--regular-quota", type=int, default=DEF_REGULAR_QUOTA,
                    help=f"REGULAR 日配额（默认 {DEF_REGULAR_QUOTA}）")
    ap.add_argument("--super-quota", type=int, default=DEF_SUPER_QUOTA,
                    help=f"SUPER 日配额（默认 {DEF_SUPER_QUOTA}）")
    ap.add_argument("--proposal", help="可选：合并提案 JSON 的候选")
    ap.add_argument("--min-sharpe", type=float, default=sq.LIM["sharpe"])
    ap.add_argument("--min-fitness", type=float, default=sq.LIM["fitness"])
    ap.add_argument("--min-2y", type=float, default=sq.LIM["two_year"])
    ap.add_argument("--max-corr", type=float, default=sq.LIM["prod"])
    ap.add_argument("--min-margin", type=float, default=DEF_MIN_MARGIN,
                    help="最低余量（prod/self 与线之间的距离；0=不限，默认 0）")
    ap.add_argument("--require-verified", action="store_true",
                    help="只选相关性已验证的候选（排除 IS_ONLY）")
    ap.add_argument("--pyramid", default="results/pyramid_latest.json",
                    help="塔快照 JSON")
    ap.add_argument("--json", dest="json_out",
                    help="输出 JSON 路径（默认自动带时间戳）")
    ap.add_argument("--no-csv", dest="no_csv", action="store_true",
                    help="只输出 JSON，不生成 CSV")
    a = ap.parse_args()

    stamp = datetime.now(_CST)
    print("=" * 90)
    print(f"每日最优候选选择器   {stamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"REGULAR配额={a.regular_quota}  SUPER配额={a.super_quota}  "
          f"最低余量={a.min_margin}  区域={a.region or '全库'}")
    print("⛔ 只读不提交：选定结果需用户确认后手动提交")
    print("=" * 90)

    # ---------- 加载候选 ----------
    print(f"\n[1/4] 加载候选...")
    candidates = []

    # 来源 1：submit_ready(READY)
    try:
        sr_candidates = _load_from_submit_ready(a.region)
        candidates.extend(sr_candidates)
        print(f"  submit_ready(READY): {len(sr_candidates)} 条")
    except sqlite3.Error as e:
        print(f"  [ERROR] DB 不可用: {e}", file=sys.stderr)
        return 3

    # 来源 2：proposal JSON（可选）
    if a.proposal:
        prop_candidates = _load_from_proposal(a.proposal)
        # 去重：已在 submit_ready 中的不重复加入
        existing_ids = {c["alpha_id"] for c in candidates}
        for c in prop_candidates:
            if c["alpha_id"] not in existing_ids:
                candidates.append(c)
                existing_ids.add(c["alpha_id"])
        if prop_candidates:
            print(f"  proposal: {len(prop_candidates)} 条（新增 {len(prop_candidates) - max(0, len(prop_candidates) - len(existing_ids))} 条）")

    total_pool = len(candidates)
    print(f"  合计候选池: {total_pool} 条")

    if not candidates:
        print("\n候选池为空，退出。")
        return 0

    # ---------- 过滤 + 塔解析 ----------
    print(f"\n[2/4] 全指标合格过滤 + 塔位解析...")
    pyramid = _load_pyramid(a.pyramid)
    field_idx_cache = {}
    qualified = []
    filtered = []

    for r in candidates:
        # 塔解析
        if not r.get("tower"):
            tw = _resolve_tower(r, pyramid, field_idx_cache)
            r.update(tw)

        # 指标过滤
        ok, reasons = _pass_indicators(r, a.min_sharpe, a.min_fitness,
                                       a.min_2y, a.max_corr, a.min_margin)
        # require_verified: 排除 IS_ONLY（prod/self 未验证）
        if ok and a.require_verified:
            prod = r.get("prod")
            selfc = r.get("self")
            gate_val = (r.get("gate") or "")
            if (prod is None and selfc is None) or ("IS_ONLY" in gate_val):
                ok = False
                reasons.append("IS_ONLY(相关性未验证)")
        if ok:
            qualified.append(r)
        else:
            filtered.append((r, reasons))

    print(f"  合格: {len(qualified)} 条 / 过滤: {len(filtered)} 条")

    if filtered:
        by_reason = defaultdict(int)
        for _, reasons in filtered:
            for reason in reasons:
                by_reason[reason.split(":")[0]] += 1
        if by_reason:
            print(f"  过滤理由: {dict(by_reason)}")

    if not qualified:
        print("\n无合格候选，退出。")
        return 0

    # ---------- 排序 + 选择 ----------
    print(f"\n[3/4] 塔优先排序 + 配额选择...")
    sorted_pool = sorted(qualified, key=_sort_key)

    regular_sel = _select_with_diversity(sorted_pool, a.regular_quota)
    # SUPER：从合格池中选与 REGULAR 不同的候选（不同塔更好）
    reg_ids = {r["alpha_id"] for r in regular_sel}
    sa_candidates = [r for r in sorted_pool if r["alpha_id"] not in reg_ids]
    super_sel = _select_with_diversity(sa_candidates, a.super_quota)

    print(f"  REGULAR 选定: {len(regular_sel)} / {a.regular_quota}")
    print(f"  SUPER 选定: {len(super_sel)} / {a.super_quota}")

    # ---------- 报告 ----------
    print(f"\n[4/4] 选定结果\n{'=' * 90}")

    for label, sel, quota in [("REGULAR", regular_sel, a.regular_quota),
                              ("SUPER", super_sel, a.super_quota)]:
        if not sel:
            print(f"\n【{label}】配额 {quota}，无合格候选")
            continue
        print(f"\n【{label}】{len(sel)} / {quota}")
        print(f"  {'#':>2} {'alpha_id':11s}{'reg':5s}{'S':>6s}{'F':>6s}"
              f"{'2Y':>6s}{'TO':>7s}{'prod':>8s}{'self':>8s}  塔位")
        print(f"  {'-'*80}")
        for i, r in enumerate(sel, 1):
            tw = (r.get("tower") or "—")[:20]
            lit = r.get("lit")
            flag = "未" if lit is False else ("亮" if lit is True else "?")
            print(f"  {i:>2} {r['alpha_id']:11s}{r.get('region',''):5s}"
                  f"{r.get('sharpe') or 0:6.2f}{r.get('fitness') or 0:6.2f}"
                  f"{r.get('two_year') or 0:6.2f}{r.get('turnover') or 0:7.3f}"
                  f"{r.get('prod') or 0:8.4f}{r.get('self') or 0:8.4f}  "
                  f"{tw}({flag})")
            print(f"      理由: {_reason_for(r)}")

    # 落盘
    all_sel = regular_sel + super_sel
    if all_sel:
        sel_data = []
        for r in all_sel:
            sel_data.append({
                "alpha_id": r["alpha_id"],
                "region": r.get("region"),
                "sharpe": r.get("sharpe"),
                "fitness": r.get("fitness"),
                "two_year": r.get("two_year"),
                "turnover": r.get("turnover"),
                "prod": r.get("prod"),
                "self": r.get("self"),
                "tower": r.get("tower"),
                "tower_lit": r.get("lit"),
                "tower_count": r.get("count"),
                "tower_gap": r.get("gap"),
                "multiplier": r.get("multiplier"),
                "skeleton": r.get("skeleton"),
                "fields": r.get("fields"),
                "priority": _prio(r),
                "reason": _reason_for(r),
                "source": r.get("source", "submit_ready"),
            })
        payload = {
            "generated_at": stamp.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "regular_quota": a.regular_quota,
            "super_quota": a.super_quota,
            "pool_size": total_pool,
            "qualified_count": len(qualified),
            "filtered_count": len(filtered),
            "regular_selected": len(regular_sel),
            "super_selected": len(super_sel),
            "params": {
                "min_sharpe": a.min_sharpe,
                "min_fitness": a.min_fitness,
                "min_2y": a.min_2y,
                "max_corr": a.max_corr,
                "min_margin": a.min_margin,
                "region": a.region,
            },
            "selected": sel_data,
            "discipline": "read-only: no alpha was submitted; user confirmation required",
        }
        out = a.json_out or _root(os.path.join(
            "results", f"daily_select_{stamp.strftime('%Y%m%d-%H%M%S')}.json"))
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        print(f"\n[JSON] {out}")

    print(f"\n{'=' * 90}")
    print("选定后流程：用户确认 → check_correlation(refresh=True) 终验 → 手动提交")
    print(f"⛔ REGULAR {DEF_REGULAR_QUOTA}/天  SUPER {DEF_SUPER_QUOTA}/天  00:00 ET 重置")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    sys.exit(main())
