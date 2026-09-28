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
REVIEW_FINDING_PREFIXES = ("GREEN:", "YELLOW:", "RED:", "best sharpe=", "best 2y sharpe=", "主墙:", "[harvest]")


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

    def auto_upsert_from_review(self, wave_str, rows, candidates, near,
                                settings=None, multisim_ids=None, dry_run=False):
        """pipeline stage_review 自动入库：从评审 rows 生成 wave_results 记录。

        自动生成 focus/verdict/key_findings/candidates/batches，无需手写 wave<N>_results.json。
        幂等：以原波号字符串为键合并写入（2026-09-27 N30；此前取波号里第一个数字、冲突顺延 max+1、
        INSERT OR REPLACE 整行重建）。评审是结论的权威来源，会覆盖收批级联写的暂定 verdict。
        """
        wave_id = "" if wave_str is None else str(wave_str).strip()
        if not wave_id:
            return {"skipped": True, "reason": f"wave 为空: {wave_str!r}"}

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
                "alpha": c.get("id"),
                "sharpe": c.get("sharpe"),
                "fitness": c.get("fitness"),
                "two_year": c.get("two_year_sharpe"),
                "submitted": False,
            })

        # ---- key_findings: 从 rows 自动提取 ----
        findings = []
        sharpes = [r.get("sharpe") for r in (rows or []) if isinstance(r.get("sharpe"), (int, float))]
        if sharpes:
            best = max(sharpes)
            findings.append(f"best sharpe={best:.2f} ({len(cand_list)}/{len(rows)} 达标)")
        two_years = [r.get("two_year_sharpe") for r in (rows or [])
                     if isinstance(r.get("two_year_sharpe"), (int, float))]
        if two_years:
            best_2y = max(two_years)
            findings.append(f"best 2y sharpe={best_2y:.2f}")
        # near 池 walls 聚合
        wall_count = {}
        for n in (near or []):
            for w in (n.get("walls") or []):
                if not w.endswith("_UNKNOWN") and w not in ("NO_DATA", "RA_OTHER"):
                    wall_count[w] = wall_count.get(w, 0) + 1
        if wall_count:
            dom = max(wall_count, key=wall_count.get)
            findings.append(f"主墙: {dom} ({wall_count[dom]}/{len(near or [])} near)")

        # ---- verdict: 自动生成（严格三态枚举，同 upsert 的 VERDICT_OK）----
        # 2026-09-08 修复：此前这里生成 "GREEN: N 候选达标" 式描述性文字，被 upsert
        # 的三态校验 raise SystemExit 打死；SystemExit 不继承 Exception，调用方那句
        # 「不阻断」的 except Exception 抓不住，于是每次回测成功后整条 pipeline 当场
        # 退出（[review]/[ledger]/[done] 全不打印，review checkpoint 也不落）。
        # 现改为写枚举值，原描述性文字降为 key_findings 首条——这正是 upsert 报错
        # 信息自己给的建议。
        n_cand = len(cand_list)
        n_near = len(near or [])
        n_total = len(rows or [])
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

        return self.upsert(
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
