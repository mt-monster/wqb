# -*- coding: utf-8 -*-
"""近十天候选因子全量盘点 + 当前可提交性重判（只读，绝不提交）。

池定义：2026-11-05 00:00 ~ 2026-11-15 13:20 GMT+8 期间进入过「提交评估链路」的 alpha：
  ledger_kv submit_* / robustness_*（近十天） + 47 颗全量评估 + 可靠清单 + 全篮子 +
  IND candidate_basket_20261114 + 11-14/15 交付报告与日志点名的 RA 候选。
不含：纯回测扫描件（近十天约 1.7 万条）、SA/SUPER 配方候选（单列 SX 档）。
判序：台账 REJECT/DEAD → 硬闸（ACTIVE / prod>=0.7 / self>=0.7 / ops>8 / 方案D / 稳健REJECT / prod 缓存>48h）→ 指标 → 塔边际 → 排序分。
"""
import json
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def _bootstrap():
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return parent
    raise RuntimeError("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


REPO_ROOT = _bootstrap()

from wqb.db_conn import connect  # noqa: E402

ROOT = REPO_ROOT
NOW = datetime(2026, 11, 15, 13, 20)  # GMT+8
WINDOW_START = "2026-11-05"
DB = os.path.join(ROOT, "data", "wqb.db")
OUT_JSON = os.path.join(ROOT, "results", "candidate_inventory_20261115.json")
OUT_TABLE = os.path.join(ROOT, "results", "candidate_inventory_table_20261115.md")
BENCH = 0.6396  # board meanProdCorrelation, REGULAR, 2026-11-14 快照

REGION_MAP = {1: "USA", 2: "KOR", 3: "ASI", 4: "MEA", 5: "IND", 6: "EUR",
              7: "GBR", 8: "GLB", 9: "HKG", 10: "DEU", 12: "CHN", 13: "JPN", 17: "AMR"}

# 11-14/15 新增候选与结论（日志 / 交付报告，权威于更早台账）
MANUAL = {
    "bla2k0Jq": dict(region="USA", S=1.80, F=1.25, TO=0.1444, ops=4,
                     rob="NO_RECORD", dstatus="放行", mix="none",
                     towers="USA/D1/OTHER 2→3 点亮", tower_gain=1,
                     note="11-15 四颗评估唯一值得提交；与 58J72oQN 互相关 −0.0561 正交", src="USA交付+11-15日志"),
    "58J72oQN": dict(region="USA", S=2.20, F=1.28, TO=0.0642, ops=6,
                     rob="NO_RECORD", dstatus="放行(offset)", mix="none",
                     towers="USA/D1/OTHER 2→3 点亮", tower_gain=1,
                     note="MP6l68aa 零损失压缩 8→6 ops；prod 贴线余量 .0103", src="11-15日志"),
    "MP6l68aa": dict(region="USA", dead="DONE(被 58J72oQN 零损失压缩取代)", src="11-15日志"),
    "vRAn3xkG": dict(region="USA", dead="DEAD：self 0.9961 撞已提交孪生 A1xJdOmg；方案D 硬拦", src="11-15日志"),
    "A1xJdOmg": dict(region="USA", active=True, note="11-14 ET 07:27 提交 ACTIVE", src="台账"),
    "pwaQ0bx3": dict(region="DEU", active=True, note="11-14 ET 01:03 提交 ACTIVE", src="台账"),
    "wpo8olA6": dict(region="DEU", active=True, note="11-13 ET 22:59 提交 ACTIVE", src="台账"),
    "P059RmzM": dict(region="EUR", active=True, note="11-13 ET 04:43 提交 ACTIVE", src="台账"),
    "zqrgna91": dict(region="USA", dstatus="阻断",
                     reason="方案D：ΔF −0.01 ∧ (ΔRet −0.0007 ∧ ΔTO +0.0095) 配对双恶化；prod .6877 贴线", src="11-15日志"),
    "N1eLE1de": dict(region="USA", dstatus="阻断", rob="CONDITIONAL",
                     reason="方案D：ΔRet −0.0026 ∧ ΔTO +0.0071；稳健 CONDITIONAL；prod 余量 .0084 全池最薄", src="11-15日志"),
    "YPMvZZvv": dict(region="USA", reason="陈旧 prod .6958 → refresh .9499 撞墙（14 天漂移 +0.25）", src="USA交付"),
    "E5Q0On6m": dict(region="USA", reason="prod 0.72 超线（差 0.02），被 STATISTICAL 换档件取代", src="USA交付"),
    "e7aeJoEd": dict(region="IND", S=2.38, F=1.72, TO=0.223, ops=8, rob="robust 1.91",
                     dstatus="放行", towers="IND/D1/EARNINGS 2→3 点亮", tower_gain=1,
                     note="IND 交付唯一新点亮载体；EARNINGS 塔差 1 颗", src="IND交付"),
    "qM7eZoVO": dict(region="IND", S=1.90, F=1.42, TO=0.171, ops=7, rob="robust 1.62",
                     dstatus="放行", towers="IND/D1/EARNINGS 2→3（与 e7aeJoEd 同席）", tower_gain=1,
                     note="与 e7aeJoEd 互相关 .6965，可同篮但只点一座", src="IND交付"),
    "rK7Qm6ld": dict(region="IND", S=2.15, F=1.20, TO=0.257, ops=7, rob="robust 1.04",
                     dstatus="放行", towers="IND/D1/SENTIMENT 1→2 否 / PV 11→12 已亮", tower_gain=0, src="IND交付"),
    "MP69RYAk": dict(region="IND", S=2.98, F=2.25, TO=0.244, ops=7, rob="robust 1.70",
                     dstatus="放行", towers="IND/D1/INSTITUTIONS 1→2 否 / PV 11→12 已亮", tower_gain=0,
                     note="self .6585 / prod .6699 双贴线", src="IND交付"),
    "LL5Edbee": dict(region="IND", S=2.53, F=1.78, TO=0.237, ops=7, rob="robust 1.28",
                     dstatus="放行", towers="IND/D1/INSTITUTIONS 1→2 否 / PV 11→12 已亮", tower_gain=0,
                     note="self .6338 余量 .066", src="IND交付"),
    "3qj1eYdz": dict(region="IND", S=2.76, F=1.97, ops=7, rob="robust 1.43",
                     dstatus="放行", towers="IND/D1/INSTITUTIONS 1→2 否", tower_gain=0,
                     note="备选第 6 颗：self .6976 / prod .6962 双贴线，prod 池膨胀高危", src="IND交付"),
    # 11-10/11-14 报告已实证判死件（DB 无 corr 行，必须手工带回）
    "xAvK6b0q": dict(dead="DEAD：self 实测 0.9330 撞 E5QZ1NgJ（11-10 旧表误记 PASS）", src="full_ranking_20261110"),
    "0mY5EZJv": dict(dead="DEAD：self 实测 0.9954 撞 ACTIVE bl6AvMkN", src="full_ranking_20261110"),
    "YP1zY8EM": dict(dead="DEAD：prod 0.729 超线 + CLUSTER_TEST WARNING", src="full_ranking_20261110"),
    "mLovqRV6": dict(dead="DEAD：2Y 1.27 硬闸 WARNING，该族 46 变体全判死", src="full_ranking_20261110"),
    "P05JM61x": dict(dead="DEAD：平台 4 项 FAIL（S1.46/F.79/ladder1.36/sub.61）", src="full_ranking_20261110"),
    "pwdAPALb": dict(dead="DEAD：prod 0.7541（risk70 三重 bucket 族全灭）", src="USA交付"),
    "E56XvX90": dict(dead="DEAD：prod 0.7519（risk70 族）", src="USA交付"),
    "akKqLq56": dict(dead="DEAD：prod 0.7034（risk70 族）", src="USA交付"),
    "P0od2pOp": dict(dead="DEAD：prod 0.8192（earningscall 情绪族地板）", src="USA交付"),
    "6Xd7A5V7": dict(dead="DEAD：prod 0.7672（earningscall 情绪族）", src="USA交付"),
}

# 本轮 MCP check_self_correlation 实测（2026-11-15 13:2x，本地 OS PnL 池，覆盖旧缓存）
SELF_LIVE = {
    "bla2k0Jq": 0.2094, "58J72oQN": 0.2966, "omEdka3v": 0.4164, "6XdkW08J": 0.3393,
    "pwdd7Za6": 0.4158, "RREPm361": 0.3275, "e7aeJoEd": 0.5074, "qM7eZoVO": 0.5017,
    "rK7Qm6ld": 0.2514, "MP69RYAk": 0.6585, "LL5Edbee": 0.6338, "3qj1eYdz": 0.6976,
}

# SA / SUPER 线（RA 唯一可接受通道 ⇒ 不进排序，单列）
SA_ONLY = {
    "kqabOm7g": "GBR/TOP700 SECTOR d3 l14；S4.53/F5.41/prod .6428/self .5291，11-15 跨区质量攻坚排序第一",
    "RReX6k6a": "DEU/TOP500 R&M；S2.92/F2.91/prod .5514/self .5516，11-15 SA 全域扫描排序第一",
    "GrWjwp8Q": "GBR/TOP700 INDUSTRY d1 trunc .02；S3.07/F3.08/prod .6705/self .6092",
    "N1N2WRXo": "GBR SUBIND d1 trunc .08；prod .6867 超本方案余量闸",
    "1YNl3p5R": "USA/TOP1000 CROWDING；prod .6011",
    "xAvMbRll": "EUR/TOP2500 R&M；11-15 SA 扫描三顺",
    "78Y01lrZ": "EUR/TOPCS1600 CROWDING；prod .6605 贴线",
    "Wjl6JJQO": "EUR/TOP2500 SUBIND SUPER，11-13 ET 20:48 已提交",
    "LLKq1dKL": "ASI/MINVOL1M R&M；U .6549/Eff 3.572 最高但 prod=self .6921 被余量闸拒",
}


def jload(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def parse_dt(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s)[:19])
    except Exception:
        return None


def age_h(s):
    d = parse_dt(s)
    return round((NOW - d).total_seconds() / 3600, 1) if d else None


def main():
    con = connect(DB, readonly=True)
    con.row_factory = sqlite3.Row
    pool = defaultdict(set)

    def add(i, src):
        if i and re.fullmatch(r"[A-Za-z0-9]{8}", str(i)):
            pool[str(i)].add(src)

    # --- 1. 台账（近十天提交预检 / 稳健审计） ---
    for r in con.execute("SELECT key, updated_at FROM ledger_kv WHERE updated_at >= ?", (WINDOW_START,)):
        m = re.match(r"^(submit|robustness)_([A-Za-z0-9]{8})$", r["key"])
        if m:
            add(m.group(2), "ledger_" + m.group(1))

    # --- 2. 全量评估 / 可靠清单 / 全篮子 ---
    assess = jload(os.path.join(ROOT, "results/full_candidate_assessment_20261113.json"))
    reliable = jload(os.path.join(ROOT, "results/reliable_submit_list_20261113.json"))
    ranking = jload(os.path.join(ROOT, "results/full_basket_ranking_20261113.json"))
    amap = {x["id"]: x for x in assess["all"]}
    for i in amap:
        add(i, "full_assessment_47")
    for key in ("rows", "seat_rows", "other_rows"):
        for x in reliable.get(key, []) or []:
            if isinstance(x, dict):
                add(x.get("alpha_id") or x.get("alpha") or x.get("id"), "reliable_list")
            else:
                add(x, "reliable_list")
    for key in ("ranked", "excluded"):
        for x in ranking.get(key, []) or []:
            if isinstance(x, dict):
                add(x.get("alpha_id") or x.get("alpha") or x.get("id"), "full_basket")
            else:
                add(x, "full_basket")
    for f in ("final_verify_prod_20261113.json", "final_verify_self_20261113.json",
              "final_verify_meta_20261113.json"):
        for i in jload(os.path.join(ROOT, "results", f)):
            add(i, "final_verify")

    # --- 3. IND 候选篮子 / 手工新增 / SA 线 ---
    row = con.execute("SELECT value FROM ledger_kv WHERE key='candidate_basket_20261114'").fetchone()
    if row:
        b = json.loads(row["value"])
        for sec in ("verified", "backup"):
            for x in b.get(sec, []):
                add(x.get("alpha_id"), "basket_IND_20261114")
    for i in MANUAL:
        add(i, "manual_1114_1115")
    for i in SA_ONLY:
        add(i, "SA_line")

    # --- 4. DB 当前状态 ---
    ledger_region = {}
    for r in con.execute("SELECT key,region FROM ledger_kv WHERE key LIKE 'robustness_%'"):
        _id = r["key"].split("_", 1)[1]
        if r["region"] != "WORKFLOW":
            ledger_region[_id] = r["region"]

    alpha_rows, corr_rows = {}, {}
    for i in pool:
        r = con.execute("SELECT * FROM alphas WHERE alpha_id=?", (i,)).fetchone()
        if r:
            alpha_rows[i] = dict(r)
        q = con.execute("SELECT prod_correlation,self_correlation,source,checked_at FROM alpha_corr_cache WHERE alpha_id=?", (i,)).fetchone()
        if q:
            corr_rows[i] = dict(q)

    # --- 5. 台账判据 ---
    submits, robusts = {}, {}
    for i in pool:
        r = con.execute("SELECT value,updated_at FROM ledger_kv WHERE key=?", ("submit_" + i,)).fetchone()
        if r:
            try:
                v = json.loads(r["value"])
                st = {s.get("step"): s for s in v.get("steps", []) if isinstance(s, dict)}
                mc = st.get("marginal_contribution", {})
                submits[i] = dict(submitted=bool(v.get("submitted")), final=v.get("final_status"),
                                 blocked=bool(st.get("submit_gate", {}).get("blocked")),
                                 hard_blocked=bool(mc.get("hard_blocked")),
                                 hard_failures=mc.get("hard_failures", []),
                                 delta=mc.get("delta", {}), at=r["updated_at"])
            except Exception:
                pass
        q = con.execute("SELECT value FROM ledger_kv WHERE key=?", ("robustness_" + i,)).fetchone()
        if q:
            try:
                robusts[i] = json.loads(q["value"]).get("verdict")
            except Exception:
                robusts[i] = None

    verify_prod = jload(os.path.join(ROOT, "results/final_verify_prod_20261113.json"))
    verify_meta = jload(os.path.join(ROOT, "results/final_verify_meta_20261113.json"))

    out = []
    for i, sources in pool.items():
        a = alpha_rows.get(i, {})
        cr = corr_rows.get(i, {})
        m = amap.get(i, {})
        man = MANUAL.get(i, {})
        sm = submits.get(i, {})
        vp = verify_prod.get(i, {})
        vm = verify_meta.get(i, {})
        active = bool(man.get("active")) or a.get("platform_status") == "ACTIVE" or sm.get("submitted")
        dead = man.get("dead")

        region = (man.get("region") or REGION_MAP.get(a.get("region_id")) or m.get("region")
                  or vm.get("region") or ledger_region.get(i) or "?")
        S = man.get("S", a.get("sharpe", m.get("S")))
        F = man.get("F", a.get("fitness", m.get("F")))
        TO = man.get("TO", a.get("turnover", m.get("TO")))
        ops = man.get("ops", m.get("ops", vm.get("ops")))

        # prod：DB corr cache 优先（最新值 + 时刻），其余退回 11-13 终验 / 全量评估
        prod, prod_at = cr.get("prod_correlation"), cr.get("checked_at")
        if prod is None and vp.get("prod") is not None:
            prod, prod_at = vp.get("prod"), vp.get("at")
        if prod is None:
            prod = m.get("prod_new") if m.get("prod_new") is not None else m.get("prod_old")
            prod_at = None
        if man.get("prod") is not None:
            prod = man["prod"]
        ph = age_h(prod_at) if prod_at else None
        if prod is not None and not prod_at:
            ph = 999.0  # 无时间戳 = 视同过期，fail-closed

        selfc = SELF_LIVE.get(i, man.get("self", cr.get("self_correlation")))
        if selfc is None:
            selfc = m.get("self_new") if m.get("self_new") is not None else m.get("self_old")
        rob = man.get("rob") or robusts.get(i) or m.get("rob") or "NO_RECORD"
        dstatus = man.get("dstatus") or m.get("dstatus") or ("阻断" if sm.get("hard_blocked") else "未测")
        dfails = man.get("reason") or ", ".join(sm.get("hard_failures") or m.get("dfails") or []) or ""
        towers = man.get("towers", m.get("towers", ""))
        tgain = man.get("tower_gain", m.get("tower_gain", 0)) or 0

        # 判序：硬闸（不可豁免）优先于软缺口（待动作/待回源）
        hard, soft = [], []
        if active:
            hard.append("已提交 ACTIVE")
        if dead:
            hard.append(dead)
        if rob == "REJECT":
            hard.append("稳健台账 REJECT")
        if prod is not None and prod >= 0.7:
            hard.append("prod≥0.7")
        if selfc is not None and selfc >= 0.7:
            hard.append("self≥0.7")
        if ops is not None and ops > 8:
            hard.append(f"ops {ops}>8")
        if dstatus == "阻断":
            hard.append("方案D 硬拦")
        if man.get("reason") and not man.get("dead"):
            hard.append(man["reason"])
        if prod is not None and ph is not None and ph > 48:
            soft.append(f"prod 缓存 {ph}h>48h 作废，须回源")
        blockers = hard + soft

        todos = []
        if i in SA_ONLY:
            tier = "SX"
        elif active:
            tier = "S0"
        elif hard:
            tier = "S3"
        else:
            complete = (prod is not None and ph is not None and ph <= 48
                        and selfc is not None and ops is not None and ops <= 8
                        and dstatus != "未测")
            if complete:
                tier = "S1"
            elif prod is None and selfc is None and ops is None and not m:
                tier = "S4"  # 仅台账有记录，无完整评估链路
            else:
                tier = "S2"
            if rob in ("NO_RECORD", "CONDITIONAL"):
                todos.append("稳健审计/显式声明")
            if m.get("narr"):
                todos.append("混腿三问答复核")
            if prod is not None and prod >= 0.68:
                todos.append("prod 贴线，提交前当刻 refresh=True")
            if selfc is None:
                todos.append("self 缺实测")
            if ops is None:
                todos.append("operatorCount 未取")
            if ph is None or ph > 48:
                todos.append("prod 回源终验")
            if dstatus == "未测":
                todos.append("方案D 边际未测")

        # 排序分（沿用 11-14 v3 十维口径 + 本轮两项修正；只做同一 tier 内排序）
        # 修正 A「贴线惩罚」：ZYa6x531 / YPMvZZvv 缓存漂移前例 ⇒ prod≥.68 重罚
        # 修正 B「塔结构纯度」：ATOM 单塔倍率高于混类别双塔（木桶短板铁律）
        score = 0.0
        if prod is not None:
            score += 30 if (ph is not None and ph <= 48) else 0
            score += max(0.0, min(20.0, (0.7 - prod) / 0.2 * 20))
            if prod >= 0.68:
                score -= 12
            if prod >= 0.69:
                score -= 8
        if selfc is not None:
            score += max(0.0, min(15.0, (0.7 - selfc) / 0.4 * 15))
            if selfc >= 0.65:
                score -= 8
        if rob == "PASS" or str(rob).startswith("robust"):
            score += 10
        if not m.get("narr"):
            score += 5  # 免混腿三问
        score += 10 if tgain else 0
        atom = man.get("atom")
        if atom is None:
            # IND 交付 5+1 颗全部 returns 残差化 ⇒ 必为 PV+X 双塔（倍率按短板）
            if i in ("e7aeJoEd", "qM7eZoVO", "rK7Qm6ld", "MP69RYAk", "LL5Edbee", "3qj1eYdz"):
                atom = False
            elif i in ("bla2k0Jq", "58J72oQN", "vRAn3xkG"):
                atom = True  # USA 交付全为单集 ATOM
        score += 8 if atom is True else (0 if atom is False else 2)
        if S is not None and F is not None:
            score += min(5.0, (S / 3.0 + F / 2.0) * 1.5)
        if ops is not None:
            score += 5 if ops <= 3 else (4 if ops <= 5 else (2 if ops <= 8 else 0))
        if prod is not None and prod < BENCH:
            score += 5
        if tier in ("S0", "S3", "S4", "SX"):
            score = min(score, 45) if tier == "S3" else 0

        out.append(dict(id=i, tier=tier, region=region, S=S, F=F, TO=TO, ops=ops,
                        prod=prod, prod_at=prod_at, prod_age_h=ph, self=selfc, rob=rob,
                        dstatus=dstatus, dfails=dfails, towers=towers, tower_gain=tgain,
                        active=active, dead=dead, blockers=blockers, todos=todos,
                        score=round(score, 1), sources=sorted(sources),
                        note=man.get("note", ""), sa_note=SA_ONLY.get(i, ""),
                        platform_status=a.get("platform_status"),
                        created_at=a.get("created_at")))

    tier_order = {"S1": 0, "S2": 1, "S3": 2, "S4": 3, "S0": 4, "SX": 5}
    out.sort(key=lambda x: (tier_order[x["tier"]], -x["score"], x["id"]))
    counts = Counter(x["tier"] for x in out)
    payload = dict(as_of="2026-11-15 13:20 GMT+8", window="2026-11-05 ~ 2026-11-15",
                   pool=len(out), tiers=dict(counts), bench=BENCH,
                   pyramid=dict(USA_OTHER=2, USA_EARNINGS=2, IND_EARNINGS=2,
                                IND_INSTITUTIONS=1, IND_SENTIMENT=1, GBR_OTHER=2,
                                DEU_OTHER=3, EUR_RISK=3),
                   rows=out)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    # 全量排序表（附录）
    lines = ["| # | alpha | 档 | 区 | S/F | ops | prod（缓存龄） | self | 稳健 | 方案D | 塔边际 | 分 | 结论 |",
             "|---:|---|---|---|---:|---:|---|---:|---|---|:---:|---:|---|"]
    for n, x in enumerate(out, 1):
        col = lambda v, f="{:.4f}": (f.format(v) if isinstance(v, (int, float)) else (v or "—"))
        prod_s = (f"{x['prod']:.4f}" + (f" ({x['prod_age_h']}h)" if x["prod_age_h"] is not None and x["prod_age_h"] < 900 else " (旧/无时刻)")) if x["prod"] is not None else "—"
        concl = " / ".join(x["blockers"][:2]) or (" / ".join(x["todos"][:2]) if x["todos"] else ("SA 线，不进 RA 排序" if x["tier"] == "SX" else "可提交"))
        concl = concl.replace("|", "/")[:110]
        lines.append(f"| {n} | `{x['id']}` | {x['tier']} | {x['region']} | "
                     f"{col(x['S'],'{:.2f}')}/{col(x['F'],'{:.2f}')} | {col(x['ops'],'{}')} | "
                     f"{prod_s} | {col(x['self'],'{:.4f}')} | {x['rob'] or '—'} | {x['dstatus']} | "
                     f"{'+1' if x['tower_gain'] else '0'} | {x['score']} | {concl} |")
    with open(OUT_TABLE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("pool", len(out), "tiers", dict(counts))
    for t in ("S1", "S2"):
        print("--", t)
        for x in out:
            if x["tier"] == t:
                print(f"   {x['id']:9s} {x['region']:4s} score={x['score']:5.1f} "
                      f"prod={x['prod']} age={x['prod_age_h']} self={x['self']} ops={x['ops']} "
                      f"rob={x['rob']} D={x['dstatus']} tower=+{x['tower_gain']} todo={x['todos']}")
    print("OUT", OUT_JSON, OUT_TABLE)


if __name__ == "__main__":
    main()
