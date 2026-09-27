# -*- coding: utf-8 -*-
"""Sandbox guard for the RA-pipeline dry-run rehearsal (isolated work dir only, see reproduce.sh).

- Blocks outbound network (socket connect) and records attempts.
- Blocks subprocess spawning (Popen) and records attempted argv.
- Snapshots the sandbox tree + DB so each probe can report side effects.

Nothing here touches the real repository: SBX points at a `git archive HEAD` copy.
"""
import hashlib
import json
import os
import socket
import sqlite3
import subprocess

SBX = os.environ["SBX"]
DB = os.path.join(SBX, "data", "wqb.db")

NET_ATTEMPTS = []
SUBPROC_ATTEMPTS = []


def _blocked_connect(self, address, *a, **k):
    NET_ATTEMPTS.append(repr(address))
    raise ConnectionRefusedError(f"[sandbox] network blocked: {address!r}")


def _blocked_create_connection(address, *a, **k):
    NET_ATTEMPTS.append(repr(address))
    raise ConnectionRefusedError(f"[sandbox] network blocked: {address!r}")


socket.socket.connect = _blocked_connect
socket.socket.connect_ex = _blocked_connect
socket.create_connection = _blocked_create_connection

_REAL_POPEN = subprocess.Popen


class _BlockedPopen:
    def __init__(self, args, *a, **k):
        SUBPROC_ATTEMPTS.append(args if isinstance(args, str) else " ".join(map(str, args)))
        raise RuntimeError("[sandbox] subprocess blocked")


def block_subprocess(on=True):
    subprocess.Popen = _BlockedPopen if on else _REAL_POPEN


block_subprocess(True)

_SKIP_DIRS = {".git", "__pycache__"}


def tree_snapshot():
    snap = {}
    for root, dirs, files in os.walk(SBX):
        dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
        rel_root = os.path.relpath(root, SBX)
        snap[rel_root + "/"] = ("dir", 0)
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, SBX)
            if rel.startswith("data" + os.sep + "wqb.db"):
                continue
            try:
                st = os.stat(p)
                snap[rel] = (st.st_size, st.st_mtime_ns)
            except OSError:
                pass
    return snap


def db_digest():
    if not os.path.isfile(DB):
        return None
    conn = sqlite3.connect(DB)
    try:
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        h = hashlib.sha256()
        counts = {}
        for t in tables:
            rows = conn.execute(f'SELECT * FROM "{t}"').fetchall()
            counts[t] = len(rows)
            h.update(t.encode())
            for r in rows:
                h.update(repr(r).encode())
        return h.hexdigest()[:16], counts
    finally:
        conn.close()


def diff(before, after):
    added = sorted(k for k in after if k not in before)
    removed = sorted(k for k in before if k not in after)
    changed = sorted(k for k in after if k in before and after[k] != before[k] and not k.endswith("/"))
    return {"added": added, "removed": removed, "changed": changed}


class Probe:
    """Context manager: records FS/DB/net/subprocess side effects of the enclosed call."""

    def __enter__(self):
        self.t0 = tree_snapshot()
        self.d0 = db_digest()
        self.n0 = len(NET_ATTEMPTS)
        self.s0 = len(SUBPROC_ATTEMPTS)
        return self

    def __exit__(self, *exc):
        t1 = tree_snapshot()
        d1 = db_digest()
        self.fs = diff(self.t0, t1)
        self.db_changed = (self.d0 or (None,))[0] != (d1 or (None,))[0]
        self.db_rows_delta = {}
        if self.d0 and d1:
            for t, n in d1[1].items():
                if self.d0[1].get(t) != n:
                    self.db_rows_delta[t] = (self.d0[1].get(t), n)
        self.net = NET_ATTEMPTS[self.n0:]
        self.subproc = SUBPROC_ATTEMPTS[self.s0:]
        return False

    def summary(self):
        side = []
        if self.fs["added"] or self.fs["changed"] or self.fs["removed"]:
            side.append(f"FS +{len(self.fs['added'])}/~{len(self.fs['changed'])}/-{len(self.fs['removed'])}")
        if self.db_changed:
            side.append(f"DB changed {self.db_rows_delta or '(content)'}")
        if self.net:
            side.append(f"NET x{len(self.net)}")
        if self.subproc:
            side.append(f"SUBPROC x{len(self.subproc)}")
        return "零副作用" if not side else "副作用: " + "; ".join(side)

    def details(self):
        return {"fs": self.fs, "db_changed": self.db_changed, "db_rows_delta": self.db_rows_delta,
                "net": self.net, "subproc": self.subproc}


def dump(obj, limit=1600):
    s = json.dumps(obj, ensure_ascii=False, default=str, indent=1)
    return s if len(s) <= limit else s[:limit] + f"...(+{len(s) - limit} chars)"
