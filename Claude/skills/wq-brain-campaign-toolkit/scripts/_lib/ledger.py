# -*- coding: utf-8 -*-
"""_lib/ledger.py - LedgerStore：战役台账统一读写（原子写 + 双遍重放 + 幂等 mutation）。

取代 record_*.py 手写脚本（直接 load-改-dump 无原子写/备份/重读合并，已淘汰）。
写操作保证：
  1. 原子写（tmp + os.replace），整夜战役中断不损坏台账
  2. utf-8-sig 编码（带 BOM；读取必须同编码）
  3. 写前自动 .bak 滚动备份
  4. 写时重读合并（update 双遍重放，防并行会话互相覆盖）

mutation 必须幂等：同名键覆盖、列表去重追加。schema 守卫：空 key / "_" 前缀 key 拒绝。
键命名约定见 references/ledger-schema.md。
"""
import datetime
import json
import os
import shutil
import sys

from .common import atomic_write, load_json


def today():
    return datetime.date.today().isoformat()


class LedgerStore:
    def __init__(self, path, encoding="utf-8-sig", backup=True):
        self.path = path
        self.encoding = encoding
        self.bak = path + ".bak"
        self.backup = backup

    def load(self):
        if not os.path.exists(self.path):
            return {}
        return load_json(self.path, encoding=self.encoding)

    def atomic_save(self, d):
        if self.backup and os.path.exists(self.path):
            shutil.copy2(self.path, self.bak)
        atomic_write(self.path, d, encoding=self.encoding)

    def update(self, mutator):
        """读-改-写，且写前在最新快照上重放 mutation（并行会话安全）。"""
        d = self.load()
        mutator(d)          # 第一遍：基于当前状态计算
        fresh = self.load()  # 重读，捕获并行会话在我读写间隙的写入
        mutator(fresh)      # 重放（要求幂等 mutation）
        self.atomic_save(fresh)
        return fresh

    # ---- 常用幂等 mutation（也被 review_wave / score_datasets 复用） ----

    def set_key(self, key, val):
        if not key or key.startswith("_"):
            raise SystemExit("schema 守卫：key 非法（空或 _ 前缀保留）")
        return self.update(lambda d: d.__setitem__(key, val))

    def mark_dead(self, dataset, reason, salvage=None):
        def mut(d):
            counts = [v.get("dead_count", 0) for k, v in d.items()
                      if k.endswith("_dead") and isinstance(v, dict)]
            entry = {"dataset": dataset, "reason": reason,
                     "dead_at": today(), "dead_count": max(counts, default=0) + 1}
            if salvage:
                entry["salvage"] = salvage
            d[f"{dataset}_dead"] = entry
        return self.update(mut)

    def add_wave(self, wave, dataset, note=""):
        def mut(d):
            ws = d.setdefault("waves", [])
            if not any(w.get("wave") == wave for w in ws if isinstance(w, dict)):
                ws.append({"wave": wave, "dataset": dataset,
                           "note": note, "added_at": today()})
        return self.update(mut)

    def submit_ready(self, alpha_id, note=""):
        def mut(d):
            sr = d.setdefault("submit_ready", [])
            if not any((x.get("id") if isinstance(x, dict) else x) == alpha_id for x in sr):
                sr.append({"id": alpha_id, "note": note, "queued_at": today()})
        return self.update(mut)

    def backup_now(self):
        shutil.copy2(self.path, self.bak)
        return self.bak


# ---------------- SQLite 后端（可选，Phase 2） ----------------

class SqliteLedgerStore:
    """LedgerStore 的 SQLite 后端：同接口，存到 wqb.db 的 ledger_kv 表。

    与 JSON 版差异：
      - 无文件锁/原子写问题（SQLite 事务保证）
      - update() 的双遍重放简化为单事务（SQLite 本身行级锁）
      - backup_now() 导出该区域全部 kv 为 JSON 快照
    """

    def __init__(self, region, db_path=None, backup=True):
        self.region = region
        self.db_path = db_path or self._default_db_path()
        self.backup = backup
        self._ensure_table()

    @staticmethod
    def _default_db_path():
        # toolkit 根 -> wqb 工作区根 -> data/wqb.db
        here = os.path.dirname(os.path.abspath(__file__))  # scripts/_lib
        # 工作区根 = 环境变量 WQB_WORKSPACE 或默认
        ws = os.environ.get("WQB_WORKSPACE", r"D:\coding\traeCN_project\wqb")
        return os.path.join(ws, "data", "wqb.db")

    def _conn(self):
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_table(self):
        conn = self._conn()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ledger_kv (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                region VARCHAR(50) NOT NULL,
                key VARCHAR(200) NOT NULL,
                value JSON NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(region, key)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_ledger_kv_region ON ledger_kv(region)")
        conn.commit()
        conn.close()

    def load(self):
        """读出该区域全部 kv 为 dict（与 JSON 版 load() 同结构）。"""
        conn = self._conn()
        rows = conn.execute(
            "SELECT key, value FROM ledger_kv WHERE region = ?", (self.region,)
        ).fetchall()
        conn.close()
        def _parse(v):
            # NUMERIC 列亲和会把标量 JSON 文本('1')转回 int，读取侧需容忍
            if isinstance(v, (str, bytes, bytearray)):
                return json.loads(v)
            return v

        return {r["key"]: _parse(r["value"]) for r in rows}

    def atomic_save(self, d):
        """全量覆盖该区域（先删后插，单事务）。"""
        conn = self._conn()
        with conn:
            conn.execute("DELETE FROM ledger_kv WHERE region = ?", (self.region,))
            for k, v in d.items():
                conn.execute(
                    "INSERT INTO ledger_kv (region, key, value, updated_at) VALUES (?, ?, ?, datetime('now'))",
                    (self.region, k, json.dumps(v, ensure_ascii=False)),
                )
        conn.close()

    def update(self, mutator):
        """读-改-写（单事务，SQLite 行级锁替代双遍重放）。"""
        d = self.load()
        mutator(d)
        self.atomic_save(d)
        return d

    # ---- 与 LedgerStore 相同的幂等 mutation ----

    def set_key(self, key, val):
        if not key or key.startswith("_"):
            raise SystemExit("schema 守卫：key 非法（空或 _ 前缀保留）")
        return self.update(lambda d: d.__setitem__(key, val))

    def mark_dead(self, dataset, reason, salvage=None):
        def mut(d):
            counts = [v.get("dead_count", 0) for k, v in d.items()
                      if k.endswith("_dead") and isinstance(v, dict)]
            entry = {"dataset": dataset, "reason": reason,
                     "dead_at": today(), "dead_count": max(counts, default=0) + 1}
            if salvage:
                entry["salvage"] = salvage
            d[f"{dataset}_dead"] = entry
        return self.update(mut)

    def add_wave(self, wave, dataset, note=""):
        def mut(d):
            ws = d.setdefault("waves", [])
            if not any(w.get("wave") == wave for w in ws if isinstance(w, dict)):
                ws.append({"wave": wave, "dataset": dataset,
                           "note": note, "added_at": today()})
        return self.update(mut)

    def submit_ready(self, alpha_id, note=""):
        def mut(d):
            sr = d.setdefault("submit_ready", [])
            if not any((x.get("id") if isinstance(x, dict) else x) == alpha_id for x in sr):
                sr.append({"id": alpha_id, "note": note, "queued_at": today()})
        return self.update(mut)

    def backup_now(self):
        """导出该区域全部 kv 为 JSON 快照。"""
        d = self.load()
        out = os.path.join(os.path.dirname(self.db_path), f"ledger_kv_{self.region}_backup.json")
        atomic_write(out, d, encoding="utf-8")
        return out


def make_ledger_store(ctx, backend=None):
    """工厂：按环境变量 WQB_LEDGER_BACKEND 或参数选后端。

    backend: 'sqlite'（默认，SqliteLedgerStore）或 'json'（LedgerStore，fallback）。
    ctx: CampaignContext（用 ctx.ledger_path / ctx.region）。
    单轨 DB 模式（2026-08-21）：默认 sqlite；设 WQB_LEDGER_BACKEND=json 回退。
    """
    backend = backend or os.environ.get("WQB_LEDGER_BACKEND", "sqlite")
    if backend == "json":
        return LedgerStore(ctx.ledger_path)
    return SqliteLedgerStore(ctx.region)


# ---------------- CLI（由 campaign.py ledger 转发） ----------------

def cli_main(ctx, argv):
    """argv = ledger 之后的参数。返回退出码。"""
    import argparse
    ap = argparse.ArgumentParser(prog="campaign.py ledger", description="战役台账统一 CLI（原子写）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("keys")
    p = sub.add_parser("get"); p.add_argument("key")
    p = sub.add_parser("set"); p.add_argument("key"); p.add_argument("value")
    p = sub.add_parser("mark-dead"); p.add_argument("dataset")
    p.add_argument("--reason", required=True); p.add_argument("--salvage")
    p = sub.add_parser("add-wave"); p.add_argument("wave"); p.add_argument("--dataset", required=True)
    p.add_argument("--note")
    p = sub.add_parser("set-verdict"); p.add_argument("wave"); p.add_argument("--json", required=True)
    p = sub.add_parser("submit-ready"); p.add_argument("alpha_id"); p.add_argument("--note")
    sub.add_parser("backup")
    a = ap.parse_args(argv)

    store = make_ledger_store(ctx)

    if a.cmd == "keys":
        d = store.load()
        src = getattr(store, "path", f"sqlite:ledger_kv[{ctx.region}]")
        print(f"keys={len(d)}  source={src}")
        for k in sorted(d):
            v = d[k]
            tag = (f"dict:{len(v)}" if isinstance(v, dict)
                   else (f"list:{len(v)}" if isinstance(v, list) else type(v).__name__))
            print(f"  {k}  [{tag}]")
    elif a.cmd == "get":
        d = store.load()
        if a.key not in d:
            print(f"MISSING: {a.key}", file=sys.stderr)
            return 1
        print(json.dumps(d[a.key], ensure_ascii=False, indent=1))
    elif a.cmd == "set":
        try:
            val = json.loads(a.value)
        except json.JSONDecodeError:
            print(f"value 不是合法 JSON: {a.value[:80]}", file=sys.stderr)
            return 1
        store.set_key(a.key, val)
        print(f"set {a.key} OK (keys={len(store.load())})")
    elif a.cmd == "mark-dead":
        store.mark_dead(a.dataset, a.reason, a.salvage)
        print(f"mark-dead {a.dataset} OK -> {store.load()[f'{a.dataset}_dead']}")
    elif a.cmd == "add-wave":
        store.add_wave(a.wave, a.dataset, a.note or "")
        print(f"add-wave {a.wave} OK")
    elif a.cmd == "set-verdict":
        raw = a.json[1:] if a.json.startswith("@") else None
        try:
            val = (load_json(ctx.path(raw), encoding="utf-8-sig") if raw
                   else json.loads(a.json))
        except Exception as e:
            print(f"--json 解析失败: {e}", file=sys.stderr)
            return 1
        key = a.wave if a.wave.endswith("_verdict") else f"wave{a.wave}_verdict"
        val.setdefault("recorded_at", today())
        store.set_key(key, val)
        print(f"set-verdict {key} OK")
    elif a.cmd == "submit-ready":
        store.submit_ready(a.alpha_id, a.note or "")
        print(f"submit-ready {a.alpha_id} OK (total={len(store.load().get('submit_ready', []))})")
    elif a.cmd == "backup":
        print(f"backup -> {store.backup_now()}")
    return 0
