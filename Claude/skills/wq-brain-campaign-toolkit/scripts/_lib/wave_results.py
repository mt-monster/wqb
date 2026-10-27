# -*- coding: utf-8 -*-
"""_lib/wave_results.py - WaveResultsStore：wave_results 表统一读写（单入口 + 幂等 + 结构校验）。

取代 `from tools.wave_results_writer import write_wave_result` 式 Python 脚本直调
（AI 每次回写 wave 结论被迫写脚本）与散装 SQL。与 _lib/ledger.py / _lib/registry.py 同模式：
  1. 幂等 upsert：写入走工作区的写入契约 `wqb.wave_results_contract`（与 wqb-db MCP、直写兜底
     同一实现：合并式 upsert、结案必带枚举 verdict），波号按**原字符串**存取（2026-09-27 N30）
  2. import 子命令（已废弃）：解析历史 wave<N>_results.json 入库，仅为兼容保留
  3. 单事务提交，防半写
  4. 读（get/list）与写同入口，便于回写后立即验证
  5. auto_upsert_from_review：pipeline stage_review 自动入库，无需手写 JSON

2026-09-27 N30：此前按"波号里第一个数字"入库（`s2_<ds>_d1` → 2，冲突时顺延 max+1）并用
INSERT OR REPLACE 整行重建——与 backtest_results / expressions / waves 的波号对不上，未传的列被清空，
created_at 每次评审都被重置成"现在"，停止规则 B 的窗口（按波的开始时刻）因此把旧 s2 波当成最新波。

2026-08-22 起：wave<N>_results.json 文件已淘汰，波次结论一律走 pipeline 自动入库
或 wave upsert 直写数据库。import 子命令仅为导入历史文件保留，新波次禁止再用。

表结构见 database/schema.sql（wave_results：UNIQUE(region, wave_number)）。
CLI 由 campaign.py wave 转发；查表走 wqb-db-mcp（只读），写库走本入口。
"""
import sys as _sys_m, os as _os_m
_sys_m.path.insert(0, str(_os_m.path.dirname(_os_m.path.abspath(__file__))))  # _lib 可导入
from _lib.db import connect as db_connect  # 规范工厂（2026-09-20 L1 收口）
import argparse
import datetime
import json
import os
import re
import sys

from .common import load_json
from .ledger import SqliteLedgerStore  # 复用 db 路径单一来源

STATUS_OK = ("open", "closed")
#: 评审自动生成的 key_findings 行。重跑评审时整组替换；其它来源的行（步 9 的 [pyramid] 点塔进度、
#: 人工备注、写入契约的归一说明）保留在后面。[harvest] 是收批级联的暂定摘要，评审结论出来后一并替换。
#: 2026-10-24 P1-2：复盘固定四列（强度上限 / 机制方向与证伪条件 / prod 读数 / 闸缺口排序）。
#: 旧的 best sharpe= / 主墙: 前缀保留在替换组里，用于重跑时清掉历史行。
REVIEW_FINDING_PREFIXES = (
    "GREEN:", "YELLOW:", "RED:",
    "① 强度上限:", "② 机制方向与证伪条件:", "③ prod 读数:", "④ 闸缺口排序:",
    "best sharpe=", "best 2y sharpe=", "主墙:", "[harvest]",
)

#: 换手保留区间（P1-5，2026-10-24；与 `docs/experience/01_platform_gates.md` 同源）。
#: 收批后只标注不删行：越界行不值得再进 prod/self 等昂贵队列。
TO_BAND_LO, TO_BAND_HI = 0.03, 0.70


def annotate_turnover_band(rows, lo=TO_BAND_LO, hi=TO_BAND_HI):
    """给每行标注 `to_band`（in / low / high / unknown），返回越界行清单。

    单位：`turnover_pct` 是百分数（`metrics_cache.row_from_alpha` 已 ×100）；
    也接受 `turnover` 比例（≤1）自动换算。区间按比例口径 [lo, hi]。
    """
    bad = []
    for r in rows or []:
        tv = r.get("turnover_pct")
        if not isinstance(tv, (int, float)):
            raw = r.get("turnover")
            tv = raw * 100 if isinstance(raw, (int, float)) else None
        if not isinstance(tv, (int, float)):
            r["to_band"] = "unknown"
            continue
        frac = float(tv) / 100.0
        if frac < lo:
            r["to_band"] = "low"
            bad.append(r)
        elif frac > hi:
            r["to_band"] = "high"
            bad.append(r)
        else:
            r["to_band"] = "in"
    return bad


def _fnum(v):
    """数值转 float；bool / None / 字符串一律 None（不做隐式转换）。"""
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _first_num(r, *keys):
    for k in keys:
        v = _fnum((r or {}).get(k))
        if v is not None:
            return v
    return None


def _rid(r):
    """行/候选的 alpha id（评审行用 `id`，收批行有时用 `alpha_id`）。"""
    return (r or {}).get("id") or (r or {}).get("alpha_id")


#: 墙名 -> (阈值键, 行字段, 阈值缩放)；SUB / ROBUST 用行内 limit（平台给的单条门槛）。
_WALL_METRIC = {
    "SHARPE": ("sharpe_min", "sharpe", 1.0),
    "FITNESS": ("fitness_min", "fitness", 1.0),
    "2Y": ("two_year_sharpe_min", "two_year_sharpe", 1.0),
    "LOW_2Y_SHARPE": ("two_year_sharpe_min", "two_year_sharpe", 1.0),
    "IS_LADDER_SHARPE": ("two_year_sharpe_min", "two_year_sharpe", 1.0),
    "MARGIN": ("margin_min", "margin_bp", 10000.0),
    "SUB": ("__sub_limit__", "sub_universe_sharpe", 1.0),
    "LOW_SUB_UNIVERSE_SHARPE": ("__sub_limit__", "sub_universe_sharpe", 1.0),
    "LOW_ROBUST_UNIVERSE_SHARPE": ("__robust_limit__", "robust_sharpe", 1.0),
}


def wall_gap(r, wall, thresholds):
    """单行单墙「还差多少」= (门槛 − 实测)/|门槛|；正数 = 没到。算不出返回 None。

    复盘 P1-2 要求按差值排序（而不是按「是否 FAIL」计数）——同一堵墙差 5% 和差 60%
    是两种结论，后者基本可判死。
    """
    t = thresholds if isinstance(thresholds, dict) else {}
    if wall == "TVR":
        tv = _fnum(r.get("turnover_pct"))
        lo, hi = _fnum(t.get("turnover_min")), _fnum(t.get("turnover_max"))
        if tv is None or lo is None or hi is None:
            return None
        lo, hi = lo * 100, hi * 100
        if tv < lo:
            return (lo - tv) / max(abs(lo), 1e-9)
        if tv > hi:
            return (tv - hi) / max(abs(hi), 1e-9)
        return None
    spec = _WALL_METRIC.get(wall)
    if not spec:
        return None
    tkey, rkey, scale = spec
    have = _fnum(r.get(rkey))
    if have is None:
        return None
    if tkey == "__sub_limit__":
        need = _fnum(r.get("sub_universe_limit"))
    elif tkey == "__robust_limit__":
        need = _fnum(r.get("robust_limit"))
    else:
        need = _fnum(t.get(tkey))
        need = need * scale if need is not None else None
    if need is None or need == 0:
        return None
    return (need - have) / abs(need)


def wall_gap_ranking(rows, thresholds):
    """按「最坏缺口」给本波各墙排序 → [(wall, n_rows)], {wall: (gap, alpha_id)}。"""
    counts, worst = {}, {}
    for r in rows or []:
        for w in (r.get("walls") or []):
            if w == "NO_DATA":
                continue
            counts[w] = counts.get(w, 0) + 1
            g = wall_gap(r, w, thresholds)
            if g is not None and (w not in worst or g > worst[w][0]):
                worst[w] = (g, r.get("id"))
    ranked = sorted(
        counts.items(),
        key=lambda kv: (1 if kv[0] in worst else 0,
                        worst.get(kv[0], (0.0,))[0],
                        kv[1]),
        reverse=True)
    return ranked, worst


def today():
    return datetime.date.today().isoformat()


def _now():
    """与 CampaignStore / wqb-db MCP 同一口径的本地时间戳（写入契约的 created_at / updated_at）。"""
    return datetime.datetime.now().isoformat(timespec="seconds")


class WaveResultsStore:
    def __init__(self, region, db_path=None, ctx=None):
        self.region = region
        self.ctx = ctx
        self.db_path = db_path or SqliteLedgerStore._default_db_path(ctx)
        self._ensure_table()

    def _conn(self):
        import sqlite3
        conn = db_connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_table(self):
        # 与 src/wqb/store/_schema.py 同一张表（波号 TEXT、带 created_at）。旧版这里建的是
        # INTEGER 波号、没有 created_at 的表；表已存在时只补 created_at 列。
        conn = self._conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wave_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region VARCHAR(50) NOT NULL,
                wave_number TEXT NOT NULL,
                focus TEXT,
                context TEXT,
                key_findings JSON,
                candidates JSON,
                batches JSON,
                verdict TEXT,
                status VARCHAR(20),
                source_file VARCHAR(500),
                archived INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                full_payload JSON,
                UNIQUE(region, wave_number)
            )
        """)
        cols = {r[1] for r in conn.execute("PRAGMA table_info(wave_results)")}
        if "created_at" not in cols:
            conn.execute("ALTER TABLE wave_results ADD COLUMN created_at TIMESTAMP")
        conn.commit()
        conn.close()

    def _contract(self):
        """工作区的写入契约 `wqb.wave_results_contract`；找不到返回 None。"""
        try:
            from wqb import wave_results_contract
            return wave_results_contract
        except ImportError:
            pass
        from .wqb_store import _workspace_roots
        for root in _workspace_roots(getattr(self.ctx, "dir", None)):
            src = os.path.join(root, "src")
            if os.path.isdir(os.path.join(src, "wqb")):
                if src not in sys.path:
                    sys.path.insert(0, src)
                try:
                    from wqb import wave_results_contract
                    return wave_results_contract
                except ImportError:
                    continue
        return None

    def upsert(self, wave_number, focus=None, context=None, key_findings=None,
               candidates=None, batches=None, verdict=None, status=None,
               source_file=None, full_payload=None, dry_run=False,
               replace_findings_prefixes=None):
        """幂等写入（单事务）。返回规范化摘要 dict。

        写入走工作区写入契约（合并式 upsert：只覆盖本次传入的列，created_at 与未传的列保持原值），
        波号按原字符串存取（`97` 与 `s2_<ds>_d1` 都合法）。本方法先做更严的入参校验
        （verdict 只收枚举，描述性文字请放 key_findings）。
        status 不给（None）时：给了 verdict → 结案（契约的"写结论即结案"）；没给 verdict →
        已有行保持原状态、新行 open（新开一波、结论未定）。此前缺省 "open"——合并写入下
        `wave upsert --wave 97 --focus ...` 会把已结案的波改回 open，停止规则 B 从此看不到它。
        replace_findings_prefixes：给出时 key_findings 不整列替换，只替换以这些前缀开头的旧行，
        其余旧行接在本次 findings 之后（评审重跑用）。
        """
        if isinstance(wave_number, bool) or (isinstance(wave_number, int) and wave_number <= 0):
            raise SystemExit(f"wave_number 非法: {wave_number!r}")
        wave = "" if wave_number is None else str(wave_number).strip()
        if not wave:
            raise SystemExit(f"wave_number 不能为空，得到: {wave_number!r}")
        if status is not None and status not in STATUS_OK:
            raise SystemExit(f"status 非法: {status}（可选: {STATUS_OK}）")
        # S6→S-PRE 闭环硬约束"结案波次必须带结论"（2026-08-23 实测 133 条 wave 记录有 97 条
        # verdict 为空）由写入契约按**写入后的行**判定：合并写入下，已有 verdict 的结案波只改
        # focus 等字段是合法的；新结案行或没有 verdict 的结案行仍被拒。
        # 2026-09-01 verdict 三态约束：机械判定（WHERE verdict='FAIL'）要求严格枚举值。
        # PASS=有候选过内部严线 / FAIL=全灭 / PARTIAL=部分近闸。
        # 描述性结论（如"0/8 过硬闸, 新高 0.55"）放 key_findings，不占 verdict。
        VERDICT_OK = {"PASS", "FAIL", "PARTIAL"}
        v = str(verdict or "").strip()
        if v and v not in VERDICT_OK:
            raise SystemExit(
                f"verdict 必须是 {sorted(VERDICT_OK)} 之一，得到: {verdict!r}。"
                f"描述性结论请写入 --finding / key_findings。"
            )
        summary = {"region": self.region, "wave_number": wave,
                   "status": status or ("closed" if v else "保持原状态（新行 open）"),
                   "focus": focus, "key_findings_n": len(key_findings or []),
                   "candidates_n": len(candidates or []), "batches_n": len(batches or [])}
        if dry_run:
            return dict(summary, dry_run=True, sql="wave_results_contract.upsert_wave_result (未执行)")
        contract = self._contract()
        if contract is None:
            raise SystemExit("找不到工作区的写入契约 wqb.wave_results_contract（src/wqb）：设 WQB_WORKSPACE "
                             "指向工作区根后重试。wave_results 只经这一个契约写入，不再退回按数字波号整行覆盖")
        conn = self._conn()
        try:
            with conn:
                # 旧版按数字入库的本波行改回原字符串键（契约里的同一实现，收批级联也调它）
                legacy = getattr(contract, "adopt_legacy_row", lambda *_a: None)(conn, self.region, wave)
                old = conn.execute("SELECT key_findings FROM wave_results WHERE region=? AND wave_number=?",
                                   (self.region, wave)).fetchone()
                if status is None and not v and old is None:
                    status = "open"   # 新行、没给结论（契约对新行缺省 closed，会因缺 verdict 拒写）
                if replace_findings_prefixes and key_findings is not None:
                    try:
                        old = json.loads(old[0]) if old and old[0] else []
                    except (TypeError, ValueError):
                        old = [old[0]]
                    kept = [f for f in (old if isinstance(old, list) else [old])
                            if not str(f).startswith(tuple(replace_findings_prefixes))]
                    key_findings = list(key_findings) + kept
                res = contract.upsert_wave_result(
                    conn, self.region, wave, _now(), focus=focus, context=context,
                    key_findings=key_findings, candidates=candidates, batches=batches,
                    verdict=verdict or None, status=status, source_file=source_file,
                    full_payload=full_payload)
                if "error" in res:
                    raise SystemExit(res["error"])   # with conn：异常即回滚（含旧行改名）
        finally:
            conn.close()
        if legacy is not None:
            print(f"[wave_results] {self.region} 旧行 wave_number={legacy} 改为 {wave!r}"
                  f"（旧版按波号里的第一个数字入库，与 backtest_results / waves 对不上）")
        return dict(summary, action=res["action"], verdict=res.get("verdict"),
                    status=res.get("status", status), legacy_wave_number=legacy,
                    key_findings_n=len(key_findings or []), updated_fields=res.get("updated_fields") or [])

    def get(self, wave_number):
        conn = self._conn()
        row = conn.execute(
            "SELECT region, wave_number, focus, context, key_findings, candidates, batches, "
            "verdict, status, source_file, archived, full_payload "
            "FROM wave_results WHERE region=? AND wave_number=?",
            (self.region, wave_number),
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    def list(self, status=None):
        sql = "SELECT region, wave_number, focus, verdict, status, source_file " \
              "FROM wave_results WHERE region=?"
        args = [self.region]
        if status:
            sql += " AND status=?"
            args.append(status)
        sql += " ORDER BY wave_number DESC"
        conn = self._conn()
        rows = conn.execute(sql, args).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def _prod_from_db(self, ids):
        """从本地 alphas 表取 prod_correlation（零平台请求）→ ({id: value}, 可读?)。

        评审行本身不带 prod（IS 指标缓存只存平台 IS 块）；prod 由
        `check_correlation(refresh=True)` 实测后经收批/同步落 `alphas.prod_correlation`。
        表/列缺失或库不可读时返回可读性 False，调用方把它写成「未测判定不可靠」而非空。
        """
        ids = [x for x in (ids or []) if x]
        if not ids:
            return {}, True
        try:
            conn = self._conn()
            try:
                q = ",".join("?" * len(ids))
                got = {r["alpha_id"]: r["prod_correlation"]
                       for r in conn.execute(
                           f"SELECT alpha_id, prod_correlation FROM alphas "
                           f"WHERE alpha_id IN ({q})", ids)}
            finally:
                conn.close()
            return got, True
        except Exception:  # noqa: BLE001 — 只读降级，不阻断评审
            return {}, False

    def auto_upsert_from_review(self, wave_str, rows, candidates, near,
                                settings=None, multisim_ids=None, dry_run=False,
                                thresholds=None, mechanism=None, falsifier=None):
        """pipeline stage_review 自动入库：从评审 rows 生成 wave_results 记录。

        自动生成 focus/verdict/key_findings/candidates/batches，无需手写 wave<N>_results.json。
        幂等：以原波号字符串为键合并写入（2026-09-27 N30；此前取波号里第一个数字、冲突顺延 max+1、
        INSERT OR REPLACE 整行重建）。评审是结论的权威来源，会覆盖收批级联写的暂定 verdict。

        2026-10-24 P1-2：key_findings 固定四列——
          ① 强度上限（max|S| 及其来源 + 正负向极值 + 2Y）
          ② 机制方向与证伪条件（settings.mechanism / .falsifier 或显式入参；缺则标未登记）
          ③ prod 读数（行内 prod_correlation → 本地 alphas 表；无值显式标「未测」）
          ④ 闸缺口排序（按 (门槛−实测)/|门槛| 排序，不是按 FAIL 行数）+ TO 越界标注（P1-5）
        复盘旧格式（best sharpe= / best 2y sharpe= / 主墙:）保留在替换组里，重跑时清掉。
        """
        wave_id = "" if wave_str is None else str(wave_str).strip()
        if not wave_id:
            return {"skipped": True, "reason": f"wave 为空: {wave_str!r}"}
        rows = list(rows or [])
        near = list(near or [])

        # ---- focus: 从 settings 提取数据集信息 ----
        ds = (settings or {}).get("dataset", "")
        neut = (settings or {}).get("neutralization", "")
        focus = ds or (f"wave{wave_id}" if wave_id[:1].isdigit() else wave_id)   # 97 → wave97；s2_<ds>_d1 原样
        if neut:
            focus += f" ({neut})"

        # ---- context: 设置快照 ----
        uni = (settings or {}).get("universe", "")
        decay = (settings or {}).get("decay", "")
        delay = (settings or {}).get("delay", "")
        context = f"{self.region}/{uni}/delay{delay}/decay{decay}" if uni else None

        # ---- candidates: 达标候选摘要 ----
        cand_list = []
        for c in (candidates or []):
            cand_list.append({
                "alpha": _rid(c),
                "sharpe": c.get("sharpe"),
                "fitness": c.get("fitness"),
                "two_year": c.get("two_year_sharpe"),
                "submitted": False,
            })

        # ---- key_findings: 复盘固定四列（P1-2）----
        findings = []

        scored = [(abs(s), r) for r in rows
                  for s in [_fnum(r.get("sharpe"))] if s is not None]
        best_abs, best_row = (max(scored, key=lambda t: t[0]) if scored else (None, None))
        best_sign = ""
        if best_row is not None:
            best_sign = "负向" if (_fnum(best_row.get("sharpe")) or 0) < 0 else "正向"
        # ① 强度上限：看 |S| 而不是最高正 S——反向臂同样是候选（reverse 必须成对发批）
        if scored:
            bits = [f"max|S|={best_abs:.2f}（#{_rid(best_row)}，{best_sign}）"]
            pos = [_fnum(r.get("sharpe")) for r in rows if (_fnum(r.get("sharpe")) or 0) > 0]
            neg = [_fnum(r.get("sharpe")) for r in rows if (_fnum(r.get("sharpe")) or 0) < 0]
            if pos:
                bits.append(f"正向最高 {max(pos):.2f}")
            if neg:
                bits.append(f"负向最强 {min(neg):.2f}")
            y2 = [_fnum(r.get("two_year_sharpe")) for r in rows
                  if _fnum(r.get("two_year_sharpe")) is not None]
            if y2:
                bits.append(f"2Y 最高 {max(y2):.2f}")
            findings.append("① 强度上限: " + "; ".join(bits))
        else:
            findings.append("① 强度上限: 无可用 sharpe（本批无读数）")

        # ② 机制方向与证伪条件：机制本身无法从读数反推，缺登记就显式标未登记（不编）
        mech = (mechanism or (settings or {}).get("mechanism")
                or (settings or {}).get("hypothesis"))
        fals = (falsifier or (settings or {}).get("falsifier")
                or (settings or {}).get("falsify_if"))
        direction = (best_sign if best_row is not None else "未定（无读数）")
        src = f"（best|S| 臂 #{_rid(best_row)}）" if best_row is not None else ""
        findings.append(
            f"② 机制方向与证伪条件: 方向={direction}{src}; "
            f"机制={mech or '未登记'}; "
            f"证伪={fals or '未登记（回测后必须补：什么读数会推翻本机制）'}")

        # ③ prod 读数：行内值 → 本地 alphas 表（零平台请求）；无值就是「未测」，不许留空
        # 注意用原始 candidates（cand_list 的键是 `alpha`，_rid 认 `id`/`alpha_id`，
        # 若遍历 cand_list 会把全部候选漏出 prod 统计范围）。
        scope_ids = []
        for c in list(candidates or []) + near:
            aid = _rid(c)
            if aid and aid not in scope_ids:
                scope_ids.append(aid)
        if not scope_ids:
            findings.append("③ prod 读数: 无候选 / 无 near ⇒ prod 无对象（未测）")
        else:
            by_id = {_rid(r): r for r in rows if _rid(r)}
            got = {}
            for aid in scope_ids:
                v = _first_num(by_id.get(aid), "prod_correlation", "prod_corr")
                if v is not None:
                    got[aid] = v
            missing = [x for x in scope_ids if x not in got]
            db_readable = True
            if missing:
                dbvals, db_readable = self._prod_from_db(missing)
                for aid, v in dbvals.items():
                    fv = _fnum(v)
                    if fv is not None:
                        got[aid] = fv
                missing = [x for x in scope_ids if x not in got]
            if got:
                top_aid = max(got, key=lambda k: got[k])
                head = (f"已测 {len(got)}/{len(scope_ids)}，"
                        f"max {got[top_aid]:.3f}（#{top_aid}）")
            else:
                head = f"已测 0/{len(scope_ids)}"
            if missing:
                head += (f"; **未测 {len(missing)} 条**"
                         f" [{', '.join('#' + m for m in missing[:4])}"
                         f"{'…' if len(missing) > 4 else ''}]"
                         f"（提交前必须 check_correlation(refresh=True)）")
            if not db_readable:
                head += "；本地 alphas 表不可读（未测判定不可靠）"
            findings.append("③ prod 读数: " + head)

        # ④ 闸缺口排序：按差值排序（同一堵墙差 5% / 差 60% 是两种结论）
        ranking, worst = wall_gap_ranking(rows, thresholds)
        to_bad = annotate_turnover_band(rows)
        to_note = ""
        if to_bad:
            n_low = sum(1 for r in to_bad if r.get("to_band") == "low")
            n_high = sum(1 for r in to_bad if r.get("to_band") == "high")
            parts = ([f"low {n_low} 条"] if n_low else []) + ([f"high {n_high} 条"] if n_high else [])
            to_note = (f" ｜ TO 越界 {'/'.join(parts)}"
                       f"（区间 [{TO_BAND_LO:.2f}, {TO_BAND_HI:.2f}]，只标注不删行；"
                       f"越界行不进 prod/self 队列）")
        if ranking:
            bits = []
            for w, n in ranking[:5]:
                g = worst.get(w)
                if g is not None:
                    bits.append(f"{w} 差 {g[0] * 100:.0f}%×{n}行（#{g[1]}）")
                else:
                    bits.append(f"{w} ×{n}行（差值不可算）")
            findings.append("④ 闸缺口排序: " + " > ".join(bits) + to_note)
        else:
            findings.append("④ 闸缺口排序: 无墙（全过或本波未做 walls 诊断）" + to_note)

        # ---- verdict: 自动生成（严格三态枚举，同 upsert 的 VERDICT_OK）----
        # 2026-09-08 修复：此前这里生成 "GREEN: N 候选达标" 式描述性文字，被 upsert
        # 的三态校验 raise SystemExit 打死；SystemExit 不继承 Exception，调用方那句
        # 「不阻断」的 except Exception 抓不住，于是每次回测成功后整条 pipeline 当场
        # 退出（[review]/[ledger]/[done] 全不打印，review checkpoint 也不落）。
        # 现改为写枚举值，原描述性文字降为 key_findings 首条——这正是 upsert 报错
        # 信息自己给的建议。
        n_cand = len(cand_list)
        n_near = len(near)
        n_total = len(rows)
        if n_cand > 0:
            verdict, verdict_note = "PASS", f"GREEN: {n_cand} 候选达标"
        elif n_near > 0:
            verdict, verdict_note = "PARTIAL", f"YELLOW: 0 候选, {n_near} near"
        else:
            verdict, verdict_note = "FAIL", f"RED: {n_total} 全灭"
        findings.insert(0, verdict_note)

        # ---- batches: multisim 信息 ----
        batch_list = []
        for msid in (multisim_ids or []):
            batch_list.append({"id": msid, "n": n_total})

        out = self.upsert(
            wave_id, focus=focus, context=context,
            key_findings=findings, candidates=cand_list,
            batches=batch_list, verdict=verdict,
            status="closed", source_file="pipeline:auto",
            full_payload={
                "wave": wave_id, "date": today(),
                "total": n_total, "candidates_n": n_cand, "near_n": n_near,
                "settings": settings or {},
                "near": [{"id": n.get("id"), "code": n.get("code"),
                          "sharpe": n.get("sharpe"), "walls": n.get("walls")}
                         for n in (near or [])],
            },
            dry_run=dry_run,
            replace_findings_prefixes=REVIEW_FINDING_PREFIXES,
        )
        out["findings"] = findings     # 首屏打印用；不改变 upsert 的返回契约
        return out


def parse_results_json(path):
    """解析现成 wave<N>_results.json -> (wave, focus, context, key_findings, candidates, batches, full_payload)。"""
    data = load_json(path)
    wave = data.get("wave")
    if wave is None:
        m = re.search(r"wave(\d+)", os.path.basename(path))
        if m:
            wave = int(m.group(1))
    if not wave:
        raise SystemExit(f"无法从 {path} 解析 wave 号（顶层 wave 键或文件名 wave<N> 均缺失）")
    key_findings = data.get("key_findings") or []
    results = data.get("results") or []
    multisim = data.get("multisim")
    batches = []
    if multisim:
        batches.append({"id": multisim, "n": len(results)})
    return (int(wave), data.get("focus"), data.get("context"),
            key_findings, results, batches, data)


def cli_main(ctx, argv):
    """argv = wave 之后的参数。返回退出码。"""
    ap = argparse.ArgumentParser(prog="campaign.py wave",
                                 description="wave_results 台账统一 CLI（幂等写 + 一键导入）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("upsert", help="写/更新 wave 结论（幂等，合并写入：只改本次给出的字段）")
    p.add_argument("--wave", required=True, help="波号原字符串（97 / s2_<ds>_d1 均可）")
    p.add_argument("--focus")
    p.add_argument("--context")
    p.add_argument("--verdict")
    p.add_argument("--status", choices=STATUS_OK,
                   help="不给时：带 --verdict 即结案；否则已有行保持原状态、新行 open")
    p.add_argument("--finding", action="append", help="可重复：key_findings 一条")
    p.add_argument("--candidates", help="候选摘要 JSON 数组（@file.json 或内联）")
    p.add_argument("--batches", help="批次信息 JSON 数组（@file.json 或内联）")
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")
    p.add_argument("--dry-run", action="store_true", help="只校验并打印，不落库")

    p = sub.add_parser("import", help="[已废弃] 导入历史 wave<N>_results.json（新波次请用 pipeline 自动入库或 wave upsert）")
    p.add_argument("--file", required=True, help="results JSON 路径（相对战役目录或绝对）")
    p.add_argument("--status", choices=STATUS_OK, default="closed",
                   help="结果文件已生成即波次结案，默认 closed")
    p.add_argument("--verdict", help="覆盖文件内无的裁决（可选；缺省留空由评审补）")
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")
    p.add_argument("--dry-run", action="store_true", help="只解析并打印，不落库")

    p = sub.add_parser("get", help="取单波完整记录")
    p.add_argument("--wave", required=True, help="波号原字符串（97 / s2_<ds>_d1 均可）")
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")

    p = sub.add_parser("list", help="列出该区域 wave 记录")
    p.add_argument("--status", choices=STATUS_OK)
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")

    a = ap.parse_args(argv)
    region = a.region or ctx.region

    if a.cmd == "list":
        rows = WaveResultsStore(region, ctx=ctx).list(a.status)
        print(f"region={region} waves={len(rows)}"
              + (f" status={a.status}" if a.status else ""))
        for r in rows:
            print(f"  wave={str(r['wave_number']):<6} {r['status'] or '':6s} {r['focus'] or ''}"
                  + (f"  src={os.path.basename(r['source_file'])}" if r["source_file"] else ""))
        return 0

    if a.cmd == "get":
        row = WaveResultsStore(region, ctx=ctx).get(a.wave)
        if not row:
            print(f"MISSING: {region}/wave={a.wave}", file=sys.stderr)
            return 1
        print(f"wave={a.wave} {row['status']}  verdict={row['verdict']}")
        print(f"focus: {row['focus']}")
        if row["context"]:
            print(f"context: {row['context']}")
        kf = json.loads(row["key_findings"] or "[]")
        for i, k in enumerate(kf, 1):
            print(f"  finding{i}: {k}")
        cand = json.loads(row["candidates"] or "[]")
        print(f"candidates={len(cand)}  batches={len(json.loads(row['batches'] or '[]'))}"
              f"  src={row['source_file']}")
        return 0

    store = WaveResultsStore(region, ctx=ctx)
    if a.cmd == "upsert":
        def _arr(v):
            if not v:
                return None
            if v.startswith("@"):
                data = load_json(v[1:], encoding="utf-8")
                return data if isinstance(data, list) else data.get("items", [data])
            return json.loads(v)

        out = store.upsert(
            a.wave, focus=a.focus, context=a.context, verdict=a.verdict,
            status=a.status, key_findings=a.finding,
            candidates=_arr(a.candidates), batches=_arr(a.batches),
            dry_run=a.dry_run,
        )
        if a.dry_run:
            print(f"[DRY] wave={a.wave} 校验通过，未写入 -> {region}/{out['status']} "
                  f"(findings={out['key_findings_n']} candidates={out['candidates_n']} batches={out['batches_n']})")
        else:   # 合并写入：报写入后的行，与本次实际写了哪些列
            print(f"wave={a.wave} OK {out['action']} -> {region}/{out['status']} verdict={out['verdict']} "
                  f"(本次写入: {','.join(out['updated_fields']) or '无'})")
        return 0

    # import
    path = a.file if os.path.isabs(a.file) else os.path.join(ctx.dir, a.file)
    if not os.path.exists(path):
        print(f"文件不存在: {path}", file=sys.stderr)
        return 2
    wave, focus, context, kf, cand, batches, payload = parse_results_json(path)
    if a.verdict:
        payload["verdict"] = a.verdict
    try:
        rel = os.path.relpath(path)
    except ValueError:  # 跨盘符（skill 在 C:，工作区在 D:）回退绝对路径
        rel = os.path.abspath(path)
    out = store.upsert(wave, focus=focus, context=context, verdict=a.verdict,
                       status=a.status, key_findings=kf, candidates=cand,
                       batches=batches, source_file=rel,
                       full_payload=payload, dry_run=a.dry_run)
    tag = "[DRY] " if a.dry_run else ""
    print(f"{tag}wave{wave} {('解析通过，未写入' if a.dry_run else 'imported')} -> "
          f"{region}/{out['status']} (findings={out['key_findings_n']} "
          f"candidates={out['candidates_n']} batches={out['batches_n']} src={os.path.basename(path)})")
    return 0
