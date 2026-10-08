# -*- coding: utf-8 -*-
"""mining_ledger.py — 会话内挖掘产出的「第一落点」队列（append-only JSONL）。

为什么需要它（2026-10-06 ``58gkLAkk`` 案）
-----------------------------------------
一颗 alpha 在会话里被挖出来后，若只停留在对话/记忆里，上下文一截断或会话一中断
就**永久丢失**；本地库没有它 ⇒ 所有只扫本地 SQLite 的盘点工具
（``submit_inventory`` / ``scan_backup_ra`` / ``enqueue_propose``）集体失明。
该案的补录只能靠用户事后点名 ID 才被发现。

为什么不直接写 ``submit_ready``
-------------------------------
* **要平台 ID**：``submit_queue.py add`` 需 alpha_id 并触发 PC 相关性计算（实测 1–5 分钟），
  挖掘当下往往只有表达式；
* **DB 写锁**：WAL 单写者可能被长事务占据 ≥30min（``tools/db_lock_audit.py``），
  挖掘侧不该去抢锁；
* **要人工裁决**：入队按用户定案必须人工/策略裁决，不能由挖掘侧自动写。

⇒ 本工具做**零依赖、零阻塞、不碰 DB、不调平台**的第一落点：
挖出一颗 → 立刻 append + fsync 一行。上下文随时断都不丢。

状态机（append-only；同 key **后写覆盖前写**，读取时 last-write-wins）::

    NEW ──► SIM_OK ──► QUEUED ──► DONE
      │        │
      │        └──► SIM_FAIL ──► (attempts < MAX_ATTEMPTS 可重试) ──► SIM_OK
      │                     └──► 超上限 ──► DEAD
      └──► DEAD（人工判死）

用法
----
::

    # 入队：只有表达式（还没仿真）
    python tools/ledger/mining_ledger.py add --expr "rank(ts_zscore(f,66))" \\
        --region DEU --universe TOP500 --delay 1 --neutralization SUBINDUSTRY --decay 8 \\
        --wave deu_w33 --src chat

    # 入队：已有平台 ID
    python tools/ledger/mining_ledger.py add --alpha-id 58gkLAkk --region DEU --src chat

    # 状态推进（仿真成功 / 失败）
    python tools/ledger/mining_ledger.py mark --key <key> --state SIM_OK --alpha-id <id>
    python tools/ledger/mining_ledger.py mark --key <key> --state SIM_FAIL --error "timeout"

    python tools/ledger/mining_ledger.py scan                 # 列出待处理
    python tools/ledger/mining_ledger.py promote --dry-run    # 把有 ID 的推进 submit_ready（默认 dry-run）
    python tools/ledger/mining_ledger.py promote --apply
    python tools/ledger/mining_ledger.py stats
    python tools/ledger/mining_ledger.py selftest             # 自检（临时目录，不碰真实队列）

纪律：脚本**绝不**提交 alpha，也不自动改 ALLOW_ALPHA_SUBMIT。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import sys as _sys
    _src = str(Path(__file__).resolve().parents[2] / "src")
    if _src not in _sys.path:
        _sys.path.insert(0, _src)
    from wqb.paths import find_repo_root  # noqa: E402
    REPO = find_repo_root(__file__)
except Exception:
    REPO = Path(__file__).resolve().parents[2]
DEFAULT_LEDGER = REPO / "results" / "mining_ledger" / "alpha_ledger.jsonl"
FALLBACK_SUFFIX = ".fallback.jsonl"

SCHEMA_V = 1
STATE_NEW = "NEW"
STATE_SIM_OK = "SIM_OK"
STATE_SIM_FAIL = "SIM_FAIL"
STATE_QUEUED = "QUEUED"
STATE_DONE = "DONE"
STATE_DEAD = "DEAD"

#: 扫描器 / promote 认为「尚未闭环」的状态。
#: 语义：NEW=刚挖出（可能只有表达式）；SIM_OK=已仿真有 ID、**待入队**；
#: SIM_FAIL=仿真失败可重试。QUEUED / DONE / DEAD 均视为已闭环，不再扫出。
OPEN_STATES = (STATE_NEW, STATE_SIM_OK, STATE_SIM_FAIL)
#: 失败重试上限（attempts 达到即转 DEAD）
MAX_ATTEMPTS = 3
#: 锁文件超过这个秒数视为陈旧（持有者崩溃残留）并强制清除
STALE_LOCK_SEC = 60.0


# ---------------------------------------------------------------- 键与规范化

def normalize_expr(expr: Optional[str]) -> str:
    """表达式规范化：去掉**字符串字面量之外**的所有空白。**不改大小写**（FASTEXPR 大小写敏感）。

    为什么删而不是压缩：同一表达式换行/缩进/手打空格不同，压缩后仍可能不等
    （``rank( ts_zscore(f, 66) )`` vs ``rank(ts_zscore(f, 66))``），会被当成两颗不同的 alpha。

    为什么保护引号内：``bucket(..., range="0, 1, 0.1")`` 这类字符串常量里的空格是**语义的一部分**，
    删掉会变成另一个表达式。
    """
    s = (expr or "").strip()
    if not s:
        return ""
    parts = re.split(r'("(?:[^"\\]|\\.)*")', s)  # 奇数段 = 双引号字面量
    return "".join(p if i % 2 else re.sub(r"\s+", "", p) for i, p in enumerate(parts))


def make_key(*, expr: Optional[str] = None, alpha_id: Optional[str] = None,
             region: Optional[str] = None, universe: Optional[str] = None,
             delay: Optional[int] = None, decay: Optional[int] = None,
             neutralization: Optional[str] = None) -> str:
    """去重键。

    * 有 alpha_id ⇒ ``id:<alpha_id>``（平台 ID 本身唯一）；
    * 只有表达式 ⇒ ``expr:<sha1(settings|expr)[:16]>``。**settings 五元组参与哈希**：
      同一表达式换 region/universe/delay/decay/neutralization 是**不同**的 alpha。
    """
    if alpha_id and str(alpha_id).strip():
        return "id:" + str(alpha_id).strip()
    e = normalize_expr(expr)
    if not e:
        raise ValueError("expr 与 alpha_id 至少给一个")
    raw = "|".join([
        str(region or ""), str(universe or ""),
        "" if delay is None else str(delay),
        "" if decay is None else str(decay),
        str(neutralization or ""), e,
    ])
    return "expr:" + hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------- 跨平台锁

class _FileLock:
    """``<path>.lock`` + ``O_EXCL`` 自旋锁（跨平台、无第三方依赖）。

    崩溃残留的锁文件会在超过 ``STALE_LOCK_SEC`` 后被清除，避免永久阻塞后续写入。
    """

    #: 默认等待上限。并发挖掘（8+ 线程）时每次 fsync 在 Windows 上可能到百毫秒级，
    #: 10s 实测偶发不够，故放宽到 30s。
    DEFAULT_TIMEOUT = 30.0

    def __init__(self, path: Path, timeout: float = DEFAULT_TIMEOUT):
        self.path = Path(str(path) + ".lock")
        self.timeout = timeout
        self.fd: Optional[int] = None

    def __enter__(self) -> "_FileLock":
        deadline = time.time() + self.timeout
        delay = 0.01  # 指数退避，避免多写者惊群
        while True:
            try:
                self.fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                return self
            except FileExistsError:
                try:  # 陈旧锁清理
                    if time.time() - os.path.getmtime(str(self.path)) > STALE_LOCK_SEC:
                        os.unlink(str(self.path))
                        continue
                except OSError:
                    pass
                if time.time() > deadline:
                    raise TimeoutError(f"拿不到队列锁（{self.timeout}s）：{self.path}")
                time.sleep(delay)
                delay = min(delay * 2, 0.2)

    def __exit__(self, *exc) -> None:
        if self.fd is not None:
            try:
                os.close(self.fd)
            except OSError:
                pass
            self.fd = None
        try:
            os.unlink(str(self.path))
        except OSError:
            pass


# ---------------------------------------------------------------- 写入

def append_record(path: Path, rec: Dict[str, Any]) -> Dict[str, Any]:
    """追加一行并 fsync。``O_APPEND`` 保证单次 write 不会互相覆盖。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    with _FileLock(path):
        with open(path, "ab") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
    return rec


def append_with_fallback(path: Path, rec: Dict[str, Any]) -> Tuple[Dict[str, Any], Optional[str]]:
    """写入失败兜底：主文件写不动就写 ``<path>.fallback.jsonl``，让调用方仍能拿到记录。

    Returns: ``(rec, 实际写入路径 or None 表示彻底失败)``
    """
    try:
        append_record(path, rec)
        return rec, str(path)
    except (OSError, TimeoutError) as e:
        alt = Path(str(path) + FALLBACK_SUFFIX)
        try:
            append_record(alt, rec)
            print(f"[WARN] 主队列写入失败（{e}），已落兜底文件：{alt}", file=sys.stderr)
            return rec, str(alt)
        except (OSError, TimeoutError) as e2:
            print(f"[ERROR] 主队列与兜底文件均写入失败：{e2}", file=sys.stderr)
            return rec, None


# ---------------------------------------------------------------- 读取

def _iter_files(path: Path) -> List[Path]:
    """主文件 + 兜底文件（兜底在后，读取时自然覆盖同名 key）。"""
    out = [path]
    alt = Path(str(path) + FALLBACK_SUFFIX)
    if alt.exists():
        out.append(alt)
    return out


def load(path: Path) -> Tuple[Dict[str, Dict[str, Any]], int]:
    """读取全量并归并到 ``key -> 最新记录``（last-write-wins）。坏行跳过并计数。"""
    merged: Dict[str, Dict[str, Any]] = {}
    bad = 0
    for p in _iter_files(path):
        if not p.exists():
            continue
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    bad += 1
                    continue
                k = r.get("key")
                if not k or not isinstance(r, dict):
                    bad += 1
                    continue
                prev = merged.get(k)
                if prev is None or str(r.get("updated_at") or "") >= str(prev.get("updated_at") or ""):
                    merged[k] = r
    return merged, bad


def open_items(merged: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """待处理项：状态在 OPEN_STATES 且未超重试上限。"""
    out = []
    for r in merged.values():
        st = r.get("state")
        if st not in OPEN_STATES:
            continue
        if st == STATE_SIM_FAIL and int(r.get("attempts") or 0) >= MAX_ATTEMPTS:
            continue
        out.append(r)
    out.sort(key=lambda r: r.get("ts") or "")
    return out


# ---------------------------------------------------------------- 入队 / 标记

def build_record(*, expr=None, alpha_id=None, region=None, universe=None, delay=None,
                 decay=None, neutralization=None, wave=None, src=None, session=None,
                 metrics=None, state=STATE_NEW) -> Dict[str, Any]:
    key = make_key(expr=expr, alpha_id=alpha_id, region=region, universe=universe,
                   delay=delay, decay=decay, neutralization=neutralization)
    now = _now()
    return {
        "v": SCHEMA_V,
        "key": key,
        "ts": now,
        "updated_at": now,
        "kind": "alpha_id" if alpha_id else "expr",
        "expr": normalize_expr(expr) or None,
        "alpha_id": (str(alpha_id).strip() if alpha_id else None),
        "region": region, "universe": universe, "delay": delay, "decay": decay,
        "neutralization": neutralization,
        "wave": wave, "src": src or "chat", "session": session,
        "state": state,
        "attempts": 0,
        "last_error": None,
        "metrics": metrics or {},
    }


def cmd_add(a) -> int:
    path = Path(a.ledger)
    rec = build_record(expr=a.expr, alpha_id=a.alpha_id, region=a.region,
                       universe=a.universe, delay=a.delay, decay=a.decay,
                       neutralization=a.neutralization, wave=a.wave, src=a.src,
                       session=a.session, state=a.state)
    merged, _ = load(path)
    if rec["key"] in merged and not (a.force or a.mark_state):
        prev = merged[rec["key"]]
        print(f"[dedup] 已存在，跳过：key={rec['key']} state={prev.get('state')} "
              f"（加 --force 覆盖，或用 mark 推进状态）")
        return 0
    if a.mark_state:  # add 兼作状态推进
        rec["state"] = a.mark_state
        rec["attempts"] = int(merged.get(rec["key"], {}).get("attempts") or 0)
    _, wrote = append_with_fallback(path, rec)
    print(f"[add] key={rec['key']} state={rec['state']} -> {wrote or '写入失败'}")
    return 0 if wrote else 3


def cmd_mark(a) -> int:
    path = Path(a.ledger)
    merged, _ = load(path)
    prev = merged.get(a.key)
    if prev is None:
        print(f"[mark] 队列里没有 key={a.key}", file=sys.stderr)
        return 2
    rec = dict(prev)
    rec["state"] = a.state
    rec["updated_at"] = _now()
    if a.alpha_id:
        rec["alpha_id"] = a.alpha_id
    if a.metrics_json:
        try:
            rec["metrics"] = json.loads(a.metrics_json)
        except json.JSONDecodeError as e:
            print(f"[mark] metrics 不是合法 JSON：{e}", file=sys.stderr)
            return 2
    if a.state == STATE_SIM_FAIL:
        rec["attempts"] = int(rec.get("attempts") or 0) + 1
        rec["last_error"] = a.error or rec.get("last_error")
        if rec["attempts"] >= MAX_ATTEMPTS and not a.keep_open:
            rec["state"] = STATE_DEAD
            print(f"[mark] attempts 达上限 {MAX_ATTEMPTS} → 转 DEAD（--keep-open 可保留）")
    _, wrote = append_with_fallback(path, rec)
    print(f"[mark] key={a.key} → state={rec['state']} attempts={rec['attempts']}")
    return 0 if wrote else 3


# ---------------------------------------------------------------- 扫描 / 推进

def cmd_scan(a) -> int:
    path = Path(a.ledger)
    merged, bad = load(path)
    items = open_items(merged)
    if a.json:
        print(json.dumps({"total": len(merged), "open": len(items), "bad_lines": bad,
                          "items": items}, ensure_ascii=False, indent=2))
        return 0
    print(f"=== 队列 {path} ===")
    print(f"总记录 {len(merged)}（去重后）｜待处理 {len(items)}｜坏行 {bad}")
    if not items:
        print("  （无待处理）")
        return 0
    print(f"{'key':<24}{'state':<10}{'region':<7}{'att':<5}{'alpha_id':<12}{'wave'}")
    for r in items[:a.limit]:
        print(f"{r['key']:<24}{r.get('state',''):<10}{str(r.get('region') or '-'):<7}"
              f"{r.get('attempts',0):<5}{str(r.get('alpha_id') or '-'):<12}{r.get('wave') or '-'}")
    if len(items) > a.limit:
        print(f"  … 另有 {len(items) - a.limit} 条")
    return 0


def cmd_promote(a) -> int:
    """把「有 alpha_id 且待处理」的记录推进 ``submit_ready``（本地入队，不调平台）。

    默认 dry-run。**入队按用户定案须人工裁决**，故 --apply 需显式给 --approved-by。
    """
    path = Path(a.ledger)
    merged, _ = load(path)
    cands = [r for r in open_items(merged) if r.get("alpha_id")]
    if not cands:
        print("[promote] 没有「有 alpha_id 且待处理」的记录")
        return 0
    print(f"[promote] 候选 {len(cands)} 条" + ("（dry-run，未写入）" if not a.apply else ""))
    for r in cands:
        print(f"  {r['alpha_id']:<12} {r.get('region')}  key={r['key']}")
    if not a.apply:
        print("\n确认后加 --apply --approved-by <你>")
        return 0
    if not a.approved_by:
        print("[promote] --apply 必须带 --approved-by", file=sys.stderr)
        return 2

    sys.path.insert(0, str(REPO / "src"))
    from wqb.store import submit_queue as sq  # noqa: E402
    con = sq.connect()
    ok = 0
    try:
        sq.ensure_table(con)
        for r in cands:
            m = r.get("metrics") or {}
            rec = {
                "alpha_id": r["alpha_id"], "region": r.get("region"),
                "universe": r.get("universe"), "delay": r.get("delay"),
                "decay": r.get("decay"), "neutralization": r.get("neutralization"),
                "expr": r.get("expr"), "sharpe": m.get("sharpe"), "fitness": m.get("fitness"),
                "turnover": m.get("turnover"), "two_year": m.get("two_year"),
                "prod": m.get("prod"), "self": m.get("self"),
            }
            try:
                gate = sq.enqueue(con, rec, note=f"mining-ledger {r.get('wave') or ''} by {a.approved_by}")
            except Exception as e:  # noqa: BLE001
                print(f"  失败 {r['alpha_id']}: {str(e)[:120]}")
                continue
            ok += 1
            r2 = dict(r); r2["state"] = STATE_QUEUED; r2["updated_at"] = _now()
            append_with_fallback(path, r2)
            print(f"  入队 {r['alpha_id']} → {gate}")
        con.commit()
    finally:
        con.close()
    print(f"[promote] 已入队 {ok} 条")
    return 0


def cmd_stats(a) -> int:
    path = Path(a.ledger)
    merged, bad = load(path)
    by_state: Dict[str, int] = {}
    for r in merged.values():
        by_state[r.get("state", "?")] = by_state.get(r.get("state", "?"), 0) + 1
    print(f"队列：{path}")
    print(f"去重后 {len(merged)} 条｜坏行 {bad}")
    for k in sorted(by_state):
        print(f"  {k:<10} {by_state[k]}")
    return 0


# ---------------------------------------------------------------- 自检

def cmd_selftest(_a) -> int:
    """在临时目录跑一遍完整闭环，不碰真实队列。"""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sub" / "alpha_ledger.jsonl"
        # 1) 写入 + 读出
        r1 = build_record(expr="rank(ts_zscore(f, 66))", region="DEU", wave="w1")
        append_with_fallback(p, r1)
        merged, bad = load(p)
        assert len(merged) == 1 and bad == 0, "写入/读取失败"
        assert r1["key"] in merged
        print("✓ 1) 写入并读回")

        # 2) 去重：同表达式同 settings 再入一次
        r2 = build_record(expr="  rank( ts_zscore(f,   66) )  ", region="DEU", wave="w2")
        assert r2["key"] == r1["key"], "规范化后 key 应相同"
        merged, _ = load(p)
        assert r1["key"] in merged, "key 应已存在（去重命中）"
        print("✓ 2) 按 key 去重（空白归一化后一致）")

        # 3) settings 不同 ⇒ 不同 key
        r3 = build_record(expr="rank(ts_zscore(f, 66))", region="DEU", delay=1)
        assert r3["key"] != r1["key"], "settings 必须参与哈希"
        print("✓ 3) settings 五元组参与哈希（换 delay 即不同 alpha）")

        # 4) 状态推进 last-write-wins
        r4 = dict(r1); r4["state"] = STATE_SIM_OK; r4["alpha_id"] = "TESTID1"
        r4["updated_at"] = _now()
        append_with_fallback(p, r4)
        merged, _ = load(p)
        assert merged[r1["key"]]["state"] == STATE_SIM_OK
        assert merged[r1["key"]]["alpha_id"] == "TESTID1"
        print("✓ 4) 状态推进（append-only + last-write-wins）")

        # 5) 断点续扫：DONE 不再出现在待处理里
        r5 = dict(r4); r5["state"] = STATE_DONE; r5["updated_at"] = _now()
        append_with_fallback(p, r5)
        items = open_items(load(p)[0])
        assert not any(i["key"] == r1["key"] for i in items), "DONE 不应再被扫出"
        print("✓ 5) 断点续扫（已 DONE 不重复处理）")

        # 6) 失败重试 + 超上限转 DEAD
        r6 = dict(r1); r6["state"] = STATE_SIM_FAIL; r6["attempts"] = 1
        r6["updated_at"] = _now(); r6["alpha_id"] = None
        append_with_fallback(p, r6)
        assert any(i["key"] == r1["key"] for i in open_items(load(p)[0])), "SIM_FAIL(<上限) 应可重试"
        r7 = dict(r6); r7["attempts"] = MAX_ATTEMPTS; r7["updated_at"] = _now()
        append_with_fallback(p, r7)
        assert not any(i["key"] == r1["key"] for i in open_items(load(p)[0])), "超上限应停止重试"
        print(f"✓ 6) 失败重试（attempts 达 {MAX_ATTEMPTS} 停止）")

        # 7) 并发追加不丢行
        import concurrent.futures
        p2 = Path(td) / "concurrent.jsonl"
        recs = [build_record(expr=f"rank(f{i})", region="GLB", wave="cc") for i in range(30)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(lambda r: append_with_fallback(p2, r), recs))
        n_main = sum(1 for _ in open(p2, "r", encoding="utf-8"))
        fb = Path(str(p2) + FALLBACK_SUFFIX)
        n_fb = sum(1 for _ in open(fb, "r", encoding="utf-8")) if fb.exists() else 0
        assert n_main + n_fb == 30, f"并发追加丢行：主 {n_main} + 兜底 {n_fb} ≠ 30"
        # 兜底文件行数应为 0（锁超时才会落到那里）；非 0 不判失败但要显形
        extra = f"（其中 {n_fb} 行落到兜底文件，说明发生过锁超时）" if n_fb else ""
        print(f"✓ 7) 并发追加不丢行（8 线程 × 30 条 = {n_main}+{n_fb} 行）{extra}")

        # 8) 坏行容错
        p3 = Path(td) / "bad.jsonl"
        p3.write_text('{"key":"k1","state":"NEW","updated_at":"2026-01-01"}\nNOT_JSON\n\n',
                      encoding="utf-8")
        merged3, bad3 = load(p3)
        assert len(merged3) == 1 and bad3 == 1, "坏行应被跳过并计数"
        print("✓ 8) 坏行跳过并计数（不整体崩）")

    print("\n[selftest] 全部通过 ✅")
    return 0


# ---------------------------------------------------------------- CLI

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="挖掘产出第一落点队列（append-only JSONL）")
    ap.add_argument("--ledger", default=str(DEFAULT_LEDGER), help="队列文件路径")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="入队（--expr 或 --alpha-id 二选一）")
    p.add_argument("--expr")
    p.add_argument("--alpha-id")
    p.add_argument("--region"); p.add_argument("--universe")
    p.add_argument("--delay", type=int); p.add_argument("--decay", type=int)
    p.add_argument("--neutralization")
    p.add_argument("--wave", help="来源轮次/波号")
    p.add_argument("--src", default="chat")
    p.add_argument("--session")
    p.add_argument("--state", default=STATE_NEW)
    p.add_argument("--mark-state", help="add 兼作状态推进时指定新状态")
    p.add_argument("--force", action="store_true", help="已存在也强制追加一行")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("mark", help="推进某条的状态")
    p.add_argument("--key", required=True)
    p.add_argument("--state", required=True,
                   choices=[STATE_SIM_OK, STATE_SIM_FAIL, STATE_QUEUED, STATE_DONE, STATE_DEAD])
    p.add_argument("--alpha-id"); p.add_argument("--error")
    p.add_argument("--metrics-json", help='如 \'{"sharpe":1.75,"fitness":1.42}\'')
    p.add_argument("--keep-open", action="store_true")
    p.set_defaults(fn=cmd_mark)

    p = sub.add_parser("scan", help="列出待处理")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_scan)

    p = sub.add_parser("promote", help="把有 ID 的推进 submit_ready（默认 dry-run）")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--approved-by")
    p.set_defaults(fn=cmd_promote)

    p = sub.add_parser("stats"); p.set_defaults(fn=cmd_stats)
    p = sub.add_parser("selftest"); p.set_defaults(fn=cmd_selftest)
    return ap


def main(argv: Optional[List[str]] = None) -> int:
    a = build_parser().parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
