# -*- coding: utf-8 -*-
"""_lib/registry.py - RegistryStore：registry_empirical 表统一读写（单入口 + 幂等 + 结构校验）。

取代散装 INSERT OR REPLACE 直改（无校验/无单事务/payload 结构漂移风险）。
与 _lib/ledger.py 同模式：
  1. 幂等 upsert：INSERT OR REPLACE + UNIQUE(region, layer, entry_id)，可重复跑
  2. payload 结构校验：按 layer 必填字段；dead_end/win 缺省自动补 dead_at/date
  3. 单事务提交，防半写
  4. 读（list/get）与写同入口，便于回写后立即验证

layer 约定：dead_end / win / campaign / orphan（schema.sql §17 registry_empirical）。
CLI 由 campaign.py registry 转发；查表走 wqb-db-mcp（只读），写库走本入口。
"""
import argparse
import datetime
import json
import os
import sys

from .common import load_json
from .ledger import SqliteLedgerStore  # 复用 db 路径单一来源

REQUIRED = {
    "dead_end": ["id", "family", "reason", "rule"],
    "win": ["id", "what", "key"],
    "campaign": ["dataset", "status"],
    "orphan": ["id"],
}
STATUS_OK = ("untried", "in_progress", "exhausted")


def today():
    return datetime.date.today().isoformat()


class RegistryStore:
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
            CREATE TABLE IF NOT EXISTS registry_empirical (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region VARCHAR(50) NOT NULL,
                layer VARCHAR(20) NOT NULL,
                entry_id VARCHAR(100),
                family VARCHAR(200),
                payload JSON NOT NULL,
                dead_at VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region, layer, entry_id)
            )
        """)
        conn.commit()
        conn.close()

    def upsert(self, layer, payload, dry_run=False):
        """幂等写入（INSERT OR REPLACE，单事务）。返回规范化后的条目 dict。"""
        p = validate(layer, payload)
        entry_id = p["id"] if layer != "campaign" else p["dataset"]
        if layer == "dead_end":
            family = p.get("family")
        elif layer == "win":
            family = p.get("what")
        elif layer == "campaign":
            family = p.get("dataset")
        else:
            family = None
        dead_at = p.get("dead_at") or p.get("date")
        if dry_run:
            return {"dry_run": True, "region": self.region, "layer": layer,
                    "entry_id": entry_id, "family": family, "dead_at": dead_at,
                    "payload": p, "sql": "INSERT OR REPLACE (未执行)"}
        conn = self._conn()
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO registry_empirical "
                "(region, layer, entry_id, family, payload, dead_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, datetime('now'))",
                (self.region, layer, entry_id, family,
                 json.dumps(p, ensure_ascii=False), dead_at),
            )
        conn.close()
        return {"region": self.region, "layer": layer, "entry_id": entry_id,
                "family": family, "dead_at": dead_at, "payload": p}

    def list(self, layer=None):
        sql = ("SELECT region, layer, entry_id, family, dead_at, payload "
               "FROM registry_empirical WHERE region=?")
        args = [self.region]
        if layer:
            sql += " AND layer=?"
            args.append(layer)
        sql += " ORDER BY layer, entry_id"
        conn = self._conn()
        rows = conn.execute(sql, args).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get(self, layer, entry_id):
        conn = self._conn()
        row = conn.execute(
            "SELECT region, layer, entry_id, family, dead_at, payload "
            "FROM registry_empirical WHERE region=? AND layer=? AND entry_id=?",
            (self.region, layer, entry_id),
        ).fetchone()
        conn.close()
        return dict(row) if row else None


def validate(layer, payload):
    """按 layer 校验必填字段；缺省自动补 dead_at/date。返回规范化 payload。"""
    if layer not in REQUIRED:
        raise SystemExit(f"非法 layer: {layer}（可选: {sorted(REQUIRED)}）")
    missing = [k for k in REQUIRED[layer] if not payload.get(k)]
    if missing:
        raise SystemExit(f"{layer} payload 缺必填字段: {missing}")
    if layer == "campaign" and payload["status"] not in STATUS_OK:
        raise SystemExit(f"campaign.status 非法: {payload['status']}（可选: {STATUS_OK}）")
    p = dict(payload)
    if layer == "dead_end" and not p.get("dead_at"):
        p["dead_at"] = today()
    if layer == "win" and not p.get("date"):
        p["date"] = today()
    return p


def merge_payload(raw, named):
    """合并 --extra/--payload 与命名参数（命名参数优先）。@前缀 = 读 UTF-8 JSON 文件（中文安全通道）。"""
    p = {}
    if raw:
        if raw.startswith("@"):
            p.update(load_json(raw[1:], encoding="utf-8"))
        else:
            p.update(json.loads(raw))
    p.update(named)
    return p


def cli_main(ctx, argv):
    """argv = registry 之后的参数。返回退出码。"""
    ap = argparse.ArgumentParser(prog="campaign.py registry",
                                 description="registry 实证层统一 CLI（幂等写 + 结构校验）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # 写子命令公共选项
    def add_write_common(p):
        p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")
        p.add_argument("--extra", help="额外字段 JSON（@file.json 或内联；命名参数优先）")
        p.add_argument("--dry-run", action="store_true", help="只校验并打印，不落库")

    p = sub.add_parser("add-dead-end", help="新死路 -> layer=dead_end")
    p.add_argument("--id", required=True)
    p.add_argument("--family", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--rule", required=True)
    p.add_argument("--salvage")
    p.add_argument("--dead-at")
    add_write_common(p)

    p = sub.add_parser("add-win", help="胜绩 -> layer=win")
    p.add_argument("--id", required=True)
    p.add_argument("--what", required=True)
    p.add_argument("--key", required=True)
    p.add_argument("--date")
    add_write_common(p)

    p = sub.add_parser("upsert-campaign", help="数据集进度 -> layer=campaign")
    p.add_argument("--dataset", required=True)
    p.add_argument("--status", required=True, choices=STATUS_OK)
    p.add_argument("--note")
    add_write_common(p)

    p = sub.add_parser("add-orphan", help="UNSUBMITTED 孤儿 -> layer=orphan")
    p.add_argument("--ids", required=True, help="逗号分隔 alpha_id 列表")
    add_write_common(p)

    p = sub.add_parser("list", help="列出该区域 registry 条目")
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")
    p.add_argument("--layer", choices=sorted(REQUIRED))

    p = sub.add_parser("get", help="取单条完整 payload")
    p.add_argument("--region", help=f"覆盖区域（默认 ctx.region={ctx.region}）")
    p.add_argument("--layer", required=True, choices=sorted(REQUIRED))
    p.add_argument("--id", required=True)

    a = ap.parse_args(argv)
    region = a.region or ctx.region

    if a.cmd == "list":
        store = RegistryStore(region)
        rows = store.list(a.layer)
        print(f"region={region} entries={len(rows)}"
              + (f" layer={a.layer}" if a.layer else ""))
        for r in rows:
            print(f"  {r['layer']:9s} {r['entry_id']:42s} {r['family'] or ''}  dead_at={r['dead_at']}")
        return 0

    if a.cmd == "get":
        store = RegistryStore(region)
        row = store.get(a.layer, a.id)
        if not row:
            print(f"MISSING: {region}/{a.layer}/{a.id}", file=sys.stderr)
            return 1
        print(f"region={row['region']} layer={row['layer']} entry_id={row['entry_id']} "
              f"dead_at={row['dead_at']}")
        print(json.dumps(json.loads(row["payload"]), ensure_ascii=False, indent=1))
        return 0

    store = RegistryStore(region)
    if a.cmd == "add-dead-end":
        named = {"id": a.id, "family": a.family, "reason": a.reason, "rule": a.rule}
        if a.salvage:
            named["salvage"] = a.salvage
        if a.dead_at:
            named["dead_at"] = a.dead_at
        out = store.upsert("dead_end", merge_payload(a.extra, named), a.dry_run)
    elif a.cmd == "add-win":
        named = {"id": a.id, "what": a.what, "key": a.key}
        if a.date:
            named["date"] = a.date
        out = store.upsert("win", merge_payload(a.extra, named), a.dry_run)
    elif a.cmd == "upsert-campaign":
        named = {"dataset": a.dataset, "status": a.status}
        if a.note:
            named["note"] = a.note
        out = store.upsert("campaign", merge_payload(a.extra, named), a.dry_run)
    elif a.cmd == "add-orphan":
        ids = [x.strip() for x in a.ids.split(",") if x.strip()]
        for oid in ids:
            out = store.upsert("orphan", merge_payload(a.extra, {"id": oid}), a.dry_run)
            print(f"{'[DRY] ' if a.dry_run else ''}orphan {oid} -> "
                  f"{'OK' if a.dry_run else 'written'} (region={region})")
        return 0
    print(f"{'[DRY] ' if a.dry_run else ''}{a.cmd} {out['entry_id']} "
          f"{'校验通过，未写入' if a.dry_run else 'OK'} -> "
          f"{region}/{out['layer']} (dead_at={out['dead_at']})")
    return 0
