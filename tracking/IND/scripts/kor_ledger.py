# -*- coding: utf-8 -*-
"""kor_ledger.py - KOR 战役台账统一 CLI（M17）。

取代 record_p10 / record_dayclose / record_cw_manual / record_whitelist_v2 /
record_poison 等手写脚本。所有写操作保证：
  1. 原子写（tmp + os.replace），整夜战役中断不损坏 169+ 键台账
  2. utf-8-sig 编码（与既有台账一致，带 BOM）
  3. 写前自动 .bak 滚动备份
  4. 写时重读合并（防并行会话互相覆盖：mutation 在最新快照上重放）

用法:
  python kor_ledger.py keys
  python kor_ledger.py get <key>
  python kor_ledger.py set <key> '<json-value>'
  python kor_ledger.py mark-dead <dataset> --reason "..." [--salvage "..."]
  python kor_ledger.py add-wave <wave_id> --dataset <ds> [--note "..."]
  python kor_ledger.py set-verdict <wave_id> --json '<inline-json 或 @文件路径>'
  python kor_ledger.py submit-ready <alpha_id> [--note "..."]
  python kor_ledger.py backup
"""
import argparse, datetime, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEDGER = os.path.join(ROOT, "kor_d1_campaign_state.json")
BAK = LEDGER + ".bak"


def load(path=LEDGER):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def atomic_save(d, path=LEDGER):
    if os.path.exists(path):
        shutil.copy2(path, BAK)  # 滚动备份
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def update(mutator):
    """读-改-写，且写前在最新快照上重放 mutation（并行会话安全）。"""
    d = load()
    mutator(d)  # 第一遍：基于当前状态计算（如 dead_count 递增值）
    fresh = load()  # 重读，捕获并行会话在我读写间隙的写入
    mutator(fresh)  # 重放（幂等 mutation 设计：同名键覆盖、列表去重追加）
    atomic_save(fresh)
    return fresh


def today():
    return datetime.date.today().isoformat()


def cmd_keys(_):
    d = load()
    print(f"keys={len(d)}  file={LEDGER}")
    for k in sorted(d):
        v = d[k]
        tag = f"dict:{len(v)}" if isinstance(v, dict) else (f"list:{len(v)}" if isinstance(v, list) else type(v).__name__)
        print(f"  {k}  [{tag}]")


def cmd_get(a):
    d = load()
    if a.key not in d:
        print(f"MISSING: {a.key}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(d[a.key], ensure_ascii=False, indent=1))


def cmd_set(a):
    try:
        val = json.loads(a.value)
    except json.JSONDecodeError:
        print(f"value 不是合法 JSON: {a.value[:80]}", file=sys.stderr)
        sys.exit(1)
    if not a.key or a.key.startswith("_"):
        print("schema 守卫：key 非法（空或 _ 前缀保留）", file=sys.stderr)
        sys.exit(1)
    update(lambda d: d.__setitem__(a.key, val))
    print(f"set {a.key} OK (keys={len(load())})")


def cmd_mark_dead(a):
    def mut(d):
        counts = [v.get("dead_count", 0) for k, v in d.items()
                  if k.endswith("_dead") and isinstance(v, dict)]
        entry = {"dataset": a.dataset, "reason": a.reason,
                 "dead_at": today(), "dead_count": max(counts, default=0) + 1}
        if a.salvage:
            entry["salvage"] = a.salvage
        d[f"{a.dataset}_dead"] = entry
    update(mut)
    print(f"mark-dead {a.dataset} OK -> {load()[f'{a.dataset}_dead']}")


def cmd_add_wave(a):
    def mut(d):
        ws = d.setdefault("waves", [])
        if not any(w.get("wave") == a.wave for w in ws if isinstance(w, dict)):
            ws.append({"wave": a.wave, "dataset": a.dataset,
                       "note": a.note or "", "added_at": today()})
    update(mut)
    print(f"add-wave {a.wave} OK")


def cmd_set_verdict(a):
    raw = a.json[1:] if a.json.startswith("@") else None
    try:
        val = json.load(open(os.path.join(ROOT, raw), encoding="utf-8-sig")) if raw else json.loads(a.json)
    except Exception as e:
        print(f"--json 解析失败: {e}", file=sys.stderr)
        sys.exit(1)
    key = a.wave if a.wave.endswith("_verdict") else f"wave{a.wave}_verdict"
    val.setdefault("recorded_at", today())
    update(lambda d: d.__setitem__(key, val))
    print(f"set-verdict {key} OK")


def cmd_submit_ready(a):
    def mut(d):
        sr = d.setdefault("submit_ready", [])
        if not any((x.get("id") if isinstance(x, dict) else x) == a.alpha_id for x in sr):
            sr.append({"id": a.alpha_id, "note": a.note or "", "queued_at": today()})
    update(mut)
    print(f"submit-ready {a.alpha_id} OK (total={len(load().get('submit_ready', []))})")


def cmd_backup(_):
    shutil.copy2(LEDGER, BAK)
    print(f"backup -> {BAK}")


def main():
    ap = argparse.ArgumentParser(description="KOR 战役台账统一 CLI（原子写）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("keys")
    p = sub.add_parser("get"); p.add_argument("key"); p.set_defaults(fn=cmd_get)
    p = sub.add_parser("set"); p.add_argument("key"); p.add_argument("value"); p.set_defaults(fn=cmd_set)
    p = sub.add_parser("mark-dead"); p.add_argument("dataset")
    p.add_argument("--reason", required=True); p.add_argument("--salvage")
    p.set_defaults(fn=cmd_mark_dead)
    p = sub.add_parser("add-wave"); p.add_argument("wave"); p.add_argument("--dataset", required=True)
    p.add_argument("--note"); p.set_defaults(fn=cmd_add_wave)
    p = sub.add_parser("set-verdict"); p.add_argument("wave"); p.add_argument("--json", required=True)
    p.set_defaults(fn=cmd_set_verdict)
    p = sub.add_parser("submit-ready"); p.add_argument("alpha_id"); p.add_argument("--note")
    p.set_defaults(fn=cmd_submit_ready)
    sub.add_parser("backup").set_defaults(fn=cmd_backup)
    sub.choices["keys"].set_defaults(fn=cmd_keys)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
