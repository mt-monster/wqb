# -*- coding: utf-8 -*-
"""prod_first_screen.py — 区域"未提交存量"的 prod 首筛（prod-first 纪律的机械执行）。

背景（2026-09-22 盘点）：全库 370 颗 IS 合格但未提交的存量里，**只有 97 颗测过 prod，
其中仅 6 颗 <0.7** —— 瓶颈是 prod 不是 IS。而 **ASI 95 颗从未测过**（该区已测的 2 颗分别是
0.5093 / 0.5116，明显低于 0.7），是唯一未被开发的大池子。本工具把"先测 prod 再谈打磨"
变成一次性可跑的筛选。

行为：
  - 枚举区域内 IS 合格 & 未提交的 alpha（口径：sharpe≥1.58 & fitness≥1.0 & 2Y≥1.58 & margin 非空 & 未 ACTIVE）
  - 逐条测 **prod（原始 GET 轮询：空体=平台仍在算，非空取 `max`；见 2026-09-22 修正）** 与 **self（本地计算）**
  - **断点续跑**：state 文件记录已测 alpha；网络失败不入 state（下次重试）
  - 测得的值**回写 alphas.prod_correlation / self_correlation / corr_checked_at**（测量落库，幂等）
  - 输出 CSV + JSON；打印「<0.7 可提交清单」

用法（需 MCP venv 的 Python）：
  world-quant-brain-mcp/.venv/Scripts/python.exe tools/prod_first_screen.py --region ASI
  ... --region ASI --limit 20        # 小批试点
  ... --region ASI --dry-run         # 只列待测，不发起请求

★ 平台侧枚举（2026-09-30 EUR 实测修正）：`--region` 口径只认本地 alphas 表，而本地镜像的
  `two_year_sharpe`/`margin` 常缺同步 → 整片平台存量被筛成“0 待测”（EUR 因此连跑 4 轮
  “todo=0”，而平台侧候选文件里实际有 12 条 S>=1.66/2Y>=1.69 从未测过）。扫平台存量请用：
  ... --from-file cache/candidates_eur.json --region EUR --family-cap 2 --early-stop-clean 12
  候选文件 = `tools/build_gate_prior_from_inventory.py --emit-candidates` 产物（键
  id/code/sharpe/fitness/two_year_sharpe/universe/neut/delay/region）。
"""
import argparse
import asyncio
import json
import os
import re
import sqlite3
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))
sys.path.insert(0, os.path.join(REPO, "src"))
sys.path.insert(0, os.path.join(REPO, "src"))
from wqb.db_conn import connect as db_connect  # 规范工厂（裸 sqlite3.connect 被守卫禁止）
DB = os.path.join(REPO, "data", "wqb.db")

#: 闸5 毒模式单一事实源（toolkit config）；本工具只拿它做“扫队列前省钱预筛”，
#: 最终权威仍是 tools/wave_gate.py → toolkit gate.py 闸5。
CONSTRAINTS_JSON = os.path.join(
    REPO, "Claude", "skills", "wq-brain-campaign-toolkit", "config", "platform_constraints.json")

PROD_PASS = 0.7

IS_QUALIFIED = (
    "a.alpha_id IS NOT NULL AND a.sharpe>=1.58 AND a.fitness>=1.0 AND a.two_year_sharpe>=1.58 "
    "AND a.margin IS NOT NULL AND (a.platform_status IS NULL OR a.platform_status='UNSUBMITTED')"
)

#: backtest_results.ra_failed_checks 的这些取值等价于“无失败项”（RA-clean）。
_RA_EMPTY = ("", "null", "none", "[]")


def ra_failed_value(v) -> bool:
    """单个 ra_failed_checks 取值是否含平台失败项（RA-clean 判据取反）。

    NULL/空串/'null'/'[]' 按“无失败”计（与 ra-pipeline 严格口径、get_mining_yield(strict) 同源）。
    """
    if v is None:
        return False
    s = str(v).strip()
    return bool(s) and s.lower() not in _RA_EMPTY


def ra_failed_ids(region="", db=None):
    """「最新一次回测带 RA 失败项」的 alpha_id 集合。

    为什么需要（2026-09-30 ASI 实测）：旧版 `--region` 窗口只筛 sharpe/fitness/2Y/margin，
    不看 ra_failed_checks，于是把一批 `LOW_ROBUST_UNIVERSE_SHARPE / LOW_ASI_JPN_SHARPE`
    已失败的强指标行当成“待测供给”（ASI 103 行），要么白烧相关性队列，
    要么让人误判“还有大量未测供给”。prod 测量只对平台 RA 全过的行有意义。

    取**最新一行**（id 最大）而非任一行：早期波 FAIL、后期重跑 clean 的行仍应可测。
    """
    conn = db_connect(db or DB)
    conn.row_factory = sqlite3.Row
    sql = (
        "SELECT b.alpha_id FROM backtest_results b "
        "WHERE b.id = (SELECT MAX(b2.id) FROM backtest_results b2 WHERE b2.alpha_id = b.alpha_id) "
        "AND b.ra_failed_checks IS NOT NULL "
        "AND LOWER(TRIM(b.ra_failed_checks)) NOT IN ('null','none','[]','')"
    )
    params: list = []
    if region:
        sql += " AND UPPER(COALESCE(b.region,''))=?"
        params.append(region.upper())
    ids = {r[0] for r in conn.execute(sql, params) if r[0]}
    conn.close()
    return ids


def targets(region, limit=0, skip_measured=True, allow_ra_failed=False):
    """本地 alphas 表窗口的待测行（默认只给平台 RA 全过的行测 prod）。"""
    conn = db_connect(DB)
    conn.row_factory = sqlite3.Row
    extra = "AND a.prod_correlation IS NULL" if skip_measured else ""
    if not allow_ra_failed:
        # 相关子查询而非 NOT IN(?,?..)：坏行可达上千，参数个数会顶到 SQLite 变量上限
        extra += (
            " AND NOT EXISTS (SELECT 1 FROM backtest_results b"
            "  WHERE b.alpha_id = a.alpha_id"
            "    AND b.id = (SELECT MAX(b2.id) FROM backtest_results b2"
            "                WHERE b2.alpha_id = b.alpha_id)"
            "    AND b.ra_failed_checks IS NOT NULL"
            "    AND LOWER(TRIM(b.ra_failed_checks)) NOT IN ('null','none','[]',''))"
        )
    sql = (f"SELECT a.alpha_id, a.sharpe, a.fitness, a.two_year_sharpe, r.name AS region "
           f"FROM alphas a JOIN regions r ON r.id=a.region_id "
           f"WHERE r.name=? AND {IS_QUALIFIED} {extra} "
           f"ORDER BY a.sharpe DESC")
    if limit:
        sql += f" LIMIT {int(limit)}"
    rows = [dict(r) for r in conn.execute(sql, (region.upper(),))]
    conn.close()
    return rows


def persist(alpha_id, prod, self_v=None, source="prod_first_screen"):
    """测量落库（走 CampaignStore、不裸 SQL）；行不存在则先登记再写。

    2026-09-30：平台侧候选（--from-file）常常根本不在本地 alphas 表，旧版裸 UPDATE
    影响 0 行且不报错 → 测了等于没测（EUR 前四轮“49 条已测”只存在于丢失的 state JSON、
    库里只余 18 条）。现在先 upsert_alpha_from_platform 登记再 persist_correlation。
    """
    if not isinstance(prod, (int, float)) and not isinstance(self_v, (int, float)):
        return "no_valid_value"
    sys.path.insert(0, os.path.join(REPO, "src"))
    from wqb.store import CampaignStore
    from wqb.db_write_lock import write_lock
    store = CampaignStore(DB)
    with write_lock(tag="dbwrite_prod_screen", ttl_sec=180, wait_timeout=90):
        if not store.connection.execute(
                "SELECT 1 FROM alphas WHERE alpha_id=?", (alpha_id,)).fetchone():
            return "not_found"            # 登记在 enumerate_from_file 阶段已做完
        r = store.persist_correlation(alpha_id, prod=prod, self_=self_v,
                                      source=source, overwrite=False)
    return "ok" if "skipped" not in r else r["skipped"]


# ------------------------- 平台侧候选枚举（--from-file）-------------------------

_FIELD_STOP = {
    "sector", "industry", "subindustry", "market", "country", "exchange", "symbol",
    "null", "true", "false", "date", "range", "high", "low", "std", "mean",
}
_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_]*")
_W_NUM_RE = re.compile(r"^\s*(?:multiply\s*\(\s*)?(\d*\.?\d+)\s*(?:\*|,)")


def known_ops() -> set:
    """算子名单（单一事实源：toolkit platform_constraints.json::known_ops）。

    字段族提取必须先跳算子 token，否则 `group_rank(...)`/`vec_avg(...)` 会被当成字段名，
    把整族归到算子名下、令“族已撞墙”排除完全失效。
    """
    try:
        with open(CONSTRAINTS_JSON, encoding="utf-8") as f:
            cfg = json.load(f)
        ops = {str(o).lower() for o in (cfg.get("known_ops") or [])}
        ops |= {str(o).lower() for o in (cfg.get("inaccessible_ops") or [])}
    except Exception:  # noqa: BLE001
        return set()
    return ops


def field_family(code: str, ops=None) -> str:
    """字段族 = 表达式里第一个非算子/非分组轴字段 token 的前两截（族配给的分组单位）。"""
    ops = ops if ops is not None else known_ops()
    for t in _TOKEN_RE.findall(code or ""):
        tl = t.lower()
        if tl in ops or tl in _FIELD_STOP or tl.isdigit() or len(tl) < 4:
            continue
        parts = tl.split("_")
        return "_".join(parts[:2]) if len(parts) >= 2 else tl
    return "?"


def poison_patterns():
    """读闸5 单一事实源（platform_constraints.json）的 block 级正则；缺文件则空。"""
    try:
        with open(CONSTRAINTS_JSON, encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:  # noqa: BLE001
        return []
    out = []
    for p in cfg.get("poison_patterns") or []:
        if p.get("severity") != "block" or p.get("_structural"):
            continue                      # 结构判定非正则（占位永假），走 structural_weighted_mix
        rx = p.get("regex") or ""
        if not rx or rx == "(?!)":
            continue
        try:
            out.append((p.get("name", "?"), re.compile(rx, re.I)))
        except re.error:
            continue
    return out


def _top_level_args(s: str, open_idx: int) -> list:
    """取 `s[open_idx] == '('` 的顶层实参（括号平衡分割，嵌套逗号不算）。"""
    out, depth, cur = [], 0, ""
    for ch in s[open_idx + 1:]:
        if ch == "(":
            depth += 1
            cur += ch
        elif ch == ")":
            if depth == 0:
                out.append(cur)
                return out
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def _is_weighted_arg(arg: str) -> bool:
    """一个 add() 实参是否“带显式权重”：`0.65 * 腿` / `multiply(0.4, 腿)` / `multiply(腿, 0.5)`。

    只认 (0,1) 开区间的字面量：`multiply(2, 腿)`（放大）与 `subtract(0, rank(x))`（取负）
    都不是混腿权重。
    """
    a = (arg or "").strip()
    m = _W_NUM_RE.match(a)
    if m:
        try:
            return 0 < float(m.group(1)) < 1
        except ValueError:
            return False
    mm = re.match(r"^multiply\s*\(", a, re.I)
    if mm:
        for sub in _top_level_args(a, mm.end() - 1):
            t = sub.strip()
            if re.fullmatch(r"\d*\.?\d+", t):
                try:
                    if 0 < float(t) < 1:
                        return True
                except ValueError:
                    continue
    return False


def structural_weighted_mix(expr: str) -> bool:
    """闸5 结构判定的最小复刻：任一 `add(` 的顶层实参 ≥2 个带显式权重即判“加权混腿”。
    等权 add(A,B) 与单腿缩放不拦（与闸5 同判据）。

    ★ 权威实现是 toolkit gate.py 的括号平衡扫描；这里只作扫队列前的省钱预筛，
      提交前仍以 wave_gate 闸5 为准。
    """
    for m in re.finditer(r"\badd\s*\(", expr or "", re.I):
        if sum(1 for arg in _top_level_args(expr, m.end() - 1) if _is_weighted_arg(arg)) >= 2:
            return True
    return False


def prod_by_family(region):
    """本区已有 prod 测量按族聚合（返回 {family: max_prod}）——“已证撞墙族”的机械判定依据。"""
    conn = db_connect(DB)
    conn.row_factory = sqlite3.Row
    ops = known_ops()
    got = {}
    for r in conn.execute(
            "SELECT a.expression e, a.prod_correlation p FROM alphas a "
            "JOIN regions r ON r.id=a.region_id WHERE r.name=? AND a.prod_correlation IS NOT NULL",
            (region.upper(),)):
        f = field_family(r["e"], ops)
        got[f] = max(got.get(f, 0.0), float(r["p"]))
    conn.close()
    return got


def already_in_table(region):
    conn = db_connect(DB)
    ids = {r[0] for r in conn.execute(
        "SELECT a.alpha_id FROM alphas a JOIN regions r ON r.id=a.region_id WHERE r.name=?",
        (region.upper(),))}
    conn.close()
    return ids


def enumerate_from_file(path, region, family_cap=0, exclude_family="",
                        include_weak=False, drop_poison=True, allow_ra_failed=False):
    """从平台侧候选 JSON 枚举待测行（不看本地表的 2Y/margin），筛四层：
      1) 非本区 2) 毒模式（闸5 正则 + 结构加权腿） 3) 同族已实测 prod>=0.7
      4) 同族配给 --family-cap（按 sharpe 倒序取头）+ 表达式去重。
    返回 (rows, meta)。rows 元素含 alpha_id/sharpe/fitness/two_year_sharpe/expression/region。
    """
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    excl = {k.strip().lower() for k in (exclude_family or "").split(",") if k.strip()}
    pats = poison_patterns() if drop_poison else []
    ops = known_ops()
    walls = prod_by_family(region)
    known = already_in_table(region)
    bad_ra = set() if allow_ra_failed else ra_failed_ids(region)
    fam_rows, meta = {}, {"total": len(items), "skip_region": 0, "skip_poison": 0,
                          "skip_walled_family": 0, "skip_family_cap": 0, "skip_dup": 0,
                          "skip_weak": 0, "skip_ra_failed": 0, "poison_names": [],
                          "walled_fams": dict(walls)}
    seen_codes = set()
    for it in items:
        aid = it.get("id") or it.get("alpha_id")
        code = it.get("code") or it.get("expression") or ""
        reg = (it.get("region") or region or "").upper()
        if reg != (region or "").upper():
            meta["skip_region"] += 1
            continue
        s, ftn = it.get("sharpe"), it.get("fitness")
        ty = it.get("two_year_sharpe")
        if not include_weak and (s is None or ftn is None or s < 1.58 or ftn < 1.0):
            meta["skip_weak"] += 1
            continue
        why = next((n for n, rx in pats if rx.search(code)), None)
        if why is None and drop_poison and structural_weighted_mix(code):
            why = "weighted_leg_mix_structural"
        if aid in bad_ra:
            # 平台 RA 硬闸已有失败项 → 不可提交，测 prod 是烧单并发队列
            meta["skip_ra_failed"] += 1
            continue
        if why:
            meta["skip_poison"] += 1
            meta["poison_names"].append(f"{aid}:{why}")
            continue
        fam = field_family(code, ops)
        if fam in excl or walls.get(fam, 0) >= PROD_PASS:
            meta["skip_walled_family"] += 1
            continue
        key = re.sub(r"\s+", "", code).lower()
        if key in seen_codes:
            meta["skip_dup"] += 1
            continue
        seen_codes.add(key)
        fam_rows.setdefault(fam, []).append({
            "alpha_id": aid, "sharpe": s, "fitness": ftn, "two_year_sharpe": ty,
            "expression": code, "region": reg, "family": fam,
            "universe": it.get("universe"), "delay": it.get("delay"),
            "neutralization": it.get("neut") or it.get("neutralization"),
            "turnover": it.get("turnover"), "in_alphas": aid in known,
        })
    rows = []
    for fam, lst in fam_rows.items():
        lst.sort(key=lambda r: -(r["sharpe"] or 0))
        take = lst if not family_cap else lst[:family_cap]
        meta["skip_family_cap"] += len(lst) - len(take)
        rows.extend(take)
    rows.sort(key=lambda r: -(r["sharpe"] or 0))
    return rows, meta


def register_missing(store, rows):
    """把不在 alphas 表的候选先登记（合并写，不覆盖已有值），否则 prod 测量无处落库。"""
    n = 0
    todo = [r for r in rows if not r.get("in_alphas")]
    if not todo:
        return 0
    from wqb.db_write_lock import write_lock
    with write_lock(tag="dbwrite_prod_register", ttl_sec=300, wait_timeout=120):
        for r in todo:
            try:
                store.upsert_alpha_from_platform({
                    "alpha_id": r["alpha_id"], "region": r["region"],
                    "expression": r["expression"], "sharpe": r["sharpe"],
                    "fitness": r["fitness"], "turnover": r.get("turnover"),
                    "two_year_sharpe": r.get("two_year_sharpe"),
                    "universe": r.get("universe"), "delay": r.get("delay"),
                    "neutralization": r.get("neutralization"),
                    "platform_status": "UNSUBMITTED", "alpha_type": "REGULAR", "stage": "IS",
                })
                n += 1
            except Exception as e:  # noqa: BLE001
                print(f"  [register] {r['alpha_id']} 登记失败（不阻断测量）：{str(e)[:120]}")
    return n


async def main():
    ap = argparse.ArgumentParser(description="区域未提交存量的 prod 首筛（可续跑）")
    ap.add_argument("--region", default="ASI")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--state", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--sleep", type=float, default=0.6)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--window-s", type=int, default=300, help="每颗 prod 轮询窗口（秒）")
    ap.add_argument("--poll-gap", type=int, default=15, help="轮询间隔（秒）")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--all-measured", action="store_true",
                    help="连已测过 prod 的也重测（默认只测 prod 为 NULL 的）")
    ap.add_argument("--from-file", default=None,
                    help="平台侧存量候选 JSON（build_gate_prior_from_inventory --emit-candidates 产物）；"
                         "用它枚举而非本地 alphas 表（本地镜像 2Y/margin 缺同步时会漏掉整片供给）")
    ap.add_argument("--family-cap", type=int, default=0,
                    help="同字段族最多测几条（0=不限；防同族变体刷爆相关性队列）")
    ap.add_argument("--exclude-family", default="",
                    help="逗号分隔的字段族关键字，命中即整族不测（手动补录已证撞墙族；"
                         "族内已有实测 prod>=0.7 的会被自动排除）")
    ap.add_argument("--early-stop-clean", type=int, default=0,
                    help="累计攒到 N 颗 prod<0.7 即停（0=跑完全部）")
    ap.add_argument("--include-weak", action="store_true",
                    help="--from-file 时连 sharpe<1.58/fitness<1.0 的候选也纳入（默认只扫过 IS 硬闸的）")
    ap.add_argument("--keep-poison", action="store_true",
                    help="不剔闸5 毒模式（默认剔：加权混腿永不可提交，测 prod 是烧队列）")
    ap.add_argument("--allow-ra-failed", action="store_true",
                    help="连平台 RA 硬闸已有失败项的行也测 prod（默认剔：这些行不可提交，"
                         "测了只是白占单并发队列。2026-09-30 ASI 教训：旧版不剔导致 103 条"
                         "LOW_ROBUST/LOW_ASI_JPN_SHARPE 已失败行被当成“待测供给”）")
    a = ap.parse_args()

    state_path = a.state or os.path.join(REPO, "logs", f"_prod_screen_{a.region.upper()}_state.json")
    out_path = a.out or os.path.join(REPO, "logs", f"prod_screen_{a.region.upper()}.json")

    meta = {}
    if a.from_file:
        rows, meta = enumerate_from_file(
            a.from_file, a.region, family_cap=a.family_cap, exclude_family=a.exclude_family,
            include_weak=a.include_weak, drop_poison=not a.keep_poison,
            allow_ra_failed=a.allow_ra_failed)
        print(f"{a.region} ← {os.path.basename(a.from_file)}：入篮 {len(rows)}｜"
              f"非本区 {meta['skip_region']} 毒模式 {meta['skip_poison']} "
              f"RA已失败 {meta['skip_ra_failed']} "
              f"族已撞墙/手排 {meta['skip_walled_family']} 族配给 {meta['skip_family_cap']} "
              f"去重 {meta['skip_dup']} 未过闸 {meta['skip_weak']}（共 {meta['total']}）")
        from collections import Counter as _C
        print("  毒模式命中：" + str(dict(_C(x.split(":", 1)[1] for x in meta["poison_names"]))))
        print("  库内实测撞墙族：" + str({k: round(v, 4) for k, v in meta["walled_fams"].items()
                                       if v >= PROD_PASS}))
    else:
        rows = targets(a.region, a.limit, skip_measured=not a.all_measured,
                       allow_ra_failed=a.allow_ra_failed)

    state = {}
    if os.path.isfile(state_path):
        with open(state_path, encoding="utf-8") as f:
            state = json.load(f)
    todo = [r for r in rows if r["alpha_id"] not in state]
    if not a.all_measured:
        conn = db_connect(DB)
        have = {x[0] for x in conn.execute(
            "SELECT alpha_id FROM alphas WHERE prod_correlation IS NOT NULL")}
        conn.close()
        skipped_measured = [r["alpha_id"] for r in todo if r["alpha_id"] in have]
        todo = [r for r in todo if r["alpha_id"] not in have]
        if skipped_measured:
            print(f"  库内已有 prod 值跳过 {len(skipped_measured)} 条：{skipped_measured[:10]}")
    if a.limit and not a.from_file:
        todo = todo[:a.limit]
    print(f"{a.region}: 待测 {len(rows)}（其中未处理 {len(todo)}）｜state={state_path}")
    if a.dry_run:
        for r in todo[:30]:
            ty = r.get("two_year_sharpe")
            print(f"  {r['alpha_id']:<9} S={r['sharpe']:.2f} F={r['fitness']:.2f} "
                  f"2Y={'-' if ty is None else format(ty, '.2f')} fam={r.get('family', '?'):<22} "
                  f"u={r.get('universe')} 在库={'是' if r.get('in_alphas') else '否'}")
        print(f"  …共 {len(todo)} 条")
        return

    from brain_api import brain_client
    bc = brain_client
    await bc.ensure_authenticated()

    if a.from_file and todo:                      # 不在库的候选先登记，否则测量无处落库
        sys.path.insert(0, os.path.join(REPO, "src"))
        from wqb.store import CampaignStore
        n = register_missing(CampaignStore(DB), todo)
        print(f"  登记入 alphas：{n} 条（其余已在库）")

    measured, failed = 0, 0
    for i, row in enumerate(todo, 1):
        aid = row["alpha_id"]
        # 2026-09-22 修正：改用**原始端点轮询**取 prod——
        # 客户端 check_correlation 是同一 GET 的阻塞式轮询，且结果缓存依赖 Redis（本环境不可用）
        # → 每次回源、易「等死」。原始 GET 始终秒回（空体=平台仍在算），自己控节奏更稳。
        # 非空返回体形如 {schema, records(直方图), max, min}，**max 即 0.7 判定值**。
        prod = self_v = None
        for _ in range(int(a.window_s / a.poll_gap) or 1):
            try:
                resp = await asyncio.wait_for(
                    bc._request("GET", f"{bc.base_url}/alphas/{aid}/correlations/prod"),
                    timeout=25)
                txt = (resp.text or "").strip()
                if txt:
                    j = json.loads(txt)
                    if j.get("max") is not None:
                        prod = j["max"]
                        break
            except Exception:
                pass
            await asyncio.sleep(a.poll_gap)
        for _ in range(2):
            try:
                sc = await bc.check_self_correlation(aid, threshold=0.7)
                self_v = (sc or {}).get("max_correlation")
                if self_v is not None:
                    break
            except Exception:
                pass
            await asyncio.sleep(0.8)

        if prod is None:                      # prod 取不到 → 不入 state，下次重试
            failed += 1
            print(f"  [{i}/{len(todo)}] {aid} prod=取不到（下次重试）")
        else:
            measured += 1
            state[aid] = {"prod": prod, "self": self_v, "family": row.get("family"),
                          "sharpe": row.get("sharpe"), "fitness": row.get("fitness"),
                          "at": datetime.now().isoformat(timespec="seconds")}
            with open(state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=1)
            # 测量落库（只填 NULL，保留平台权威值；走 CampaignStore）
            wrote = persist(aid, prod, self_v)
            if wrote == "not_found":
                print(f"  [warn] {aid} 不在 alphas 表，prod 值仅存 state（请查登记步骤是否失败）")
            flag = "✅" if prod < PROD_PASS else "  "
            print(f"  [{i}/{len(todo)}] {aid} prod={prod:.4f} self={self_v} "
                  f"S={row.get('sharpe')} fam={row.get('family', '?')} 落库={wrote} {flag}")
        await asyncio.sleep(a.sleep)
        if a.early_stop_clean:
            clean_now = [k for k, v in state.items() if (v.get("prod") or 9) < PROD_PASS]
            if len(clean_now) >= a.early_stop_clean:
                print(f"\n[early-stop] 已攒到 {len(clean_now)} 颗 prod<{PROD_PASS}，不再占用相关性队列")
                break

    # 汇总
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"region": a.region.upper(), "measured": state, "screen": meta,
                   "updated": datetime.now().isoformat(timespec="seconds")},
                  f, ensure_ascii=False, indent=1)
    passing = {k: v for k, v in state.items() if v["prod"] is not None and v["prod"] < PROD_PASS}
    print(f"\n本次测得 {measured}｜prod 取不到 {failed}（未入 state，重跑即续）")
    print(f"累计已测 {len(state)}｜**prod<0.7 = {len(passing)}**")
    for k, v in sorted(passing.items(), key=lambda kv: kv[1]["prod"]):
        print(f"  ✅ {k}: prod={v['prod']:.4f} self={v['self']}")
    print(f"结果 → {out_path}")


if __name__ == "__main__":
    asyncio.run(main())
