# -*- coding: utf-8 -*-
"""_lib/wave_results.py - WaveResultsStore：wave_results 表统一读写（单入口 + 幂等 + 结构校验）。

取代 `from tools.wave_results_writer import write_wave_result` 式 Python 脚本直调
（AI 每次回写 wave 结论被迫写脚本）与散装 SQL。与 _lib/ledger.py / _lib/registry.py 同模式：
  1. 幂等 upsert：INSERT OR REPLACE + UNIQUE(region, wave_number)，可重复跑
  2. import 子命令（已废弃）：解析历史 wave<N>_results.json 入库，仅为兼容保留
  3. 单事务提交，防半写
  4. 读（get/list）与写同入口，便于回写后立即验证
  5. auto_upsert_from_review：pipeline stage_review 自动入库，无需手写 JSON

2026-08-22 起：wave<N>_results.json 文件已淘汰，波次结论一律走 pipeline 自动入库
或 wave upsert 直写数据库。import 子命令仅为导入历史文件保留，新波次禁止再用。

表结构见 database/schema.sql（wave_results：UNIQUE(region, wave_number)）。
CLI 由 campaign.py wave 转发；查表走 wqb-db-mcp（只读），写库走本入口。
"""
import argparse
import datetime
import json
import os
import re
import sys

from .common import load_json
from .ledger import SqliteLedgerStore  # 复用 db 路径单一来源

STATUS_OK = ("open", "closed")


def today():
    return datetime.date.today().isoformat()


class WaveResultsStore:
    def __init__(self, region, db_path=None):
        self.region = region
        self.db_path = db_path or SqliteLedgerStore._default_db_path()
        self._ensure_table()

    def _conn(self):
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_table(self):
        conn = self._conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wave_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region VARCHAR(50) NOT NULL,
                wave_number INTEGER NOT NULL,
                focus TEXT,
                context TEXT,
                key_findings JSON,
                candidates JSON,
                batches JSON,
                verdict TEXT,
                status VARCHAR(20),
                source_file VARCHAR(500),
                archived INTEGER DEFAULT 0,
                full_payload JSON,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region, wave_number)
            )
        """)
        conn.commit()
        conn.close()

    def upsert(self, wave_number, focus=None, context=None, key_findings=None,
               candidates=None, batches=None, verdict=None, status="open",
               source_file=None, full_payload=None, dry_run=False):
        """幂等写入（INSERT OR REPLACE，单事务）。返回规范化摘要 dict。"""
        if not isinstance(wave_number, int) or wave_number <= 0:
            raise SystemExit(f"wave_number 必须是正整数，得到: {wave_number!r}")
        if status not in STATUS_OK:
            raise SystemExit(f"status 非法: {status}（可选: {STATUS_OK}）")
        # S6→S-PRE 闭环硬约束：结案波次必须带结论。2026-08-23 实测 133 条 wave 记录
        # 有 97 条 verdict 为空（EUR/GBR/HKG/ASI 四区全空），下一轮查表读不到任何可复用信息。
        # 波次进行中（status=open）允许留空，结案时补。
        if status == "closed" and not str(verdict or "").strip():
            raise SystemExit(
                f"wave{wave_number} status=closed 必须带 --verdict（结案即须有结论）。"
                f"未定则用 --status open 保持进行中。"
            )
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
        if dry_run:
            return {"dry_run": True, "region": self.region, "wave_number": wave_number,
                    "status": status, "focus": focus,
                    "key_findings_n": len(key_findings or []),
                    "candidates_n": len(candidates or []),
                    "batches_n": len(batches or []),
                    "sql": "INSERT OR REPLACE (未执行)"}
        conn = self._conn()
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO wave_results "
                "(region, wave_number, focus, context, key_findings, candidates, batches, "
                " verdict, status, source_file, archived, full_payload, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
                (self.region, wave_number, focus, context,
                 json.dumps(key_findings or [], ensure_ascii=False),
                 json.dumps(candidates or [], ensure_ascii=False),
                 json.dumps(batches or [], ensure_ascii=False),
                 verdict, status, source_file, 0,
                 json.dumps(full_payload, ensure_ascii=False) if full_payload else None),
            )
        conn.close()
        return {"region": self.region, "wave_number": wave_number, "status": status,
                "focus": focus, "key_findings_n": len(key_findings or []),
                "candidates_n": len(candidates or []), "batches_n": len(batches or [])}

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

    @staticmethod
    def parse_wave_number(wave_str):
        """从 wave 字符串提取数字编号。支持 '94'/'wave94'/'94A'/'01' 等格式。"""
        if isinstance(wave_str, int):
            return wave_str
        s = str(wave_str).strip()
        m = re.search(r"(\d+)", s)
        if not m:
            return None
        return int(m.group(1))

    def auto_upsert_from_review(self, wave_str, rows, candidates, near,
                                settings=None, multisim_ids=None, dry_run=False):
        """pipeline stage_review 自动入库：从评审 rows 生成 wave_results 记录。

        自动生成 focus/verdict/key_findings/candidates/batches，
        无需手写 wave<N>_results.json。幂等（INSERT OR REPLACE）。
        """
        wave_num = self.parse_wave_number(wave_str)
        if wave_num is None:
            return {"skipped": True, "reason": f"无法解析 wave 号: {wave_str!r}"}

        # ---- focus: 从 settings 提取数据集信息 ----
        ds = (settings or {}).get("dataset", "")
        neut = (settings or {}).get("neutralization", "")
        focus = f"{ds}" if ds else f"wave{wave_num}"
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

        # ---- verdict: 自动生成 ----
        n_cand = len(cand_list)
        n_near = len(near or [])
        n_total = len(rows or [])
        if n_cand > 0:
            verdict = f"GREEN: {n_cand} 候选达标"
        elif n_near > 0:
            verdict = f"YELLOW: 0 候选, {n_near} near"
        else:
            verdict = f"RED: {n_total} 全灭"

        # ---- batches: multisim 信息 ----
        batch_list = []
        for msid in (multisim_ids or []):
            batch_list.append({"id": msid, "n": n_total})

        return self.upsert(
            wave_num, focus=focus, context=context,
            key_findings=findings, candidates=cand_list,
            batches=batch_list, verdict=verdict,
            status="closed", source_file="pipeline:auto",
            full_payload={
                "wave": wave_str, "date": today(),
                "total": n_total, "candidates_n": n_cand, "near_n": n_near,
                "settings": settings or {},
                "near": [{"id": n.get("id"), "code": n.get("code"),
                          "sharpe": n.get("sharpe"), "walls": n.get("walls")}
                         for n in (near or [])],
            },
            dry_run=dry_run,
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

    p = sub.add_parser("upsert", help="写/更新 wave 结论（幂等）")
    p.add_argument("--wave", type=int, required=True)
    p.add_argument("--focus")
    p.add_argument("--context")
    p.add_argument("--verdict")
    p.add_argument("--status", choices=STATUS_OK, default="open")
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
    p.add_argument("--wave", type=int, required=True)
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")

    p = sub.add_parser("list", help="列出该区域 wave 记录")
    p.add_argument("--status", choices=STATUS_OK)
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")

    a = ap.parse_args(argv)
    region = a.region or ctx.region

    if a.cmd == "list":
        rows = WaveResultsStore(region).list(a.status)
        print(f"region={region} waves={len(rows)}"
              + (f" status={a.status}" if a.status else ""))
        for r in rows:
            print(f"  wave{r['wave_number']:>3} {r['status']:6s} {r['focus'] or ''}"
                  + (f"  src={os.path.basename(r['source_file'])}" if r["source_file"] else ""))
        return 0

    if a.cmd == "get":
        row = WaveResultsStore(region).get(a.wave)
        if not row:
            print(f"MISSING: {region}/wave{a.wave}", file=sys.stderr)
            return 1
        print(f"wave{a.wave} {row['status']}  verdict={row['verdict']}")
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

    store = WaveResultsStore(region)
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
        tag = "[DRY] " if a.dry_run else ""
        print(f"{tag}wave{a.wave} {'校验通过，未写入' if a.dry_run else 'OK'} -> "
              f"{region}/{out['status']} (findings={out['key_findings_n']} "
              f"candidates={out['candidates_n']} batches={out['batches_n']})")
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
