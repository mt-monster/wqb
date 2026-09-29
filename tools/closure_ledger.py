# -*- coding: utf-8 -*-
"""closure_ledger.py — skills 审查（reports/skills_review_20260929.md）条目的「处置登记」（评审 → 跟踪 → 关闭证据）。

背景（报告 Part C）：上一轮评审 9 个 P0 完全关闭 0 个，直接原因是没有「评审条目 → 处置 → 关闭证据」的登记，也没有机检证明某条已修。
本工具维护 `docs/skills_review_closure.json`：报告里**每一个**条目 ID（Part A 逐 skill 条目、T0-*、X-*、上一轮 P0-*）都有一条处置。

状态（status）：
  fixed           本轮已改。须有 where（改在哪：仓库相对路径，可带 ::符号；多处用 ` | ` 分隔）与 note（改了什么）
  superseded      被别的改动一并解决（跨 skill 的 X-n、另一条 ID、代码修复）。须有 ref（指向哪条 / 哪个 commit）与 note
  declined        有意不改。须有 note（理由）；范本（🟢）类「无需改」也归这里，理由写「范本，保留」
  needs-platform  依赖平台实测或业务裁定，离线无法定论。须有 verify（怎么复核）与 note（当前保守处置）
  open            尚未处理（收尾时必须为 0）

用法：
  python tools/closure_ledger.py init                 # 从报告抽取全部 ID，缺的补 open（不覆盖已有）
  python tools/closure_ledger.py set --status fixed --where "Claude/skills/x/SKILL.md" --note "…" SB-01 SB-03..SB-05
  python tools/closure_ledger.py summary              # 各前缀各状态计数
  python tools/closure_ledger.py open [PREFIX]        # 列出仍 open 的条目（可按前缀过滤）
  python tools/closure_ledger.py render               # 生成 reports/skills_review_20260929_closure.md
  python tools/closure_ledger.py check [--strict]     # 校验；--strict 要求 open 为 0
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REPORT = REPO / "reports" / "skills_review_20260929.md"
DATA = REPO / "docs" / "skills_review_closure.json"
OUT_MD = REPO / "reports" / "skills_review_20260929_closure.md"

STATUSES = ("fixed", "superseded", "declined", "needs-platform", "open")
_ID = re.compile(r"^(?:[A-Z]{2}-\d{2,3}|T0-\d{1,2}|X-\d{1,2}|P0-\d)$")


def report_ids():
    """报告里的全部条目 ID → {id: {"line", "loc", "cat", "title"}}（同一 ID 出现多次取首个）。"""
    ids = {}
    text = REPORT.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(text, 1):
        m = re.match(r"^\| ((?:[A-Z]{2}|T0|P0)-\d{1,3}) \|(.*)$", line)
        if m and m.group(1) not in ids:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            ids[m.group(1)] = {"line": i, "loc": cells[1] if len(cells) > 1 else "",
                               "cat": cells[2] if len(cells) > 2 else "",
                               "title": (cells[3] if len(cells) > 3 else cells[1])[:90]}
        m = re.match(r"^### (X-\d{1,2})[　 ]+(.*)$", line)
        if m and m.group(1) not in ids:
            ids[m.group(1)] = {"line": i, "loc": "Part B", "cat": "跨 skill", "title": m.group(2)[:90]}
    return ids


def load():
    if not DATA.exists():
        return {"_doc": "", "items": {}}
    return json.loads(DATA.read_text(encoding="utf-8"))


def save(d):
    d["_doc"] = ("skills 审查（reports/skills_review_20260929.md）条目处置登记；由 tools/closure_ledger.py 维护，"
                 "tests/unit/test_closure_ledger.py 守：每个报告 ID 都有条目、状态合法、fixed 有存在的 where、needs-platform 有 verify。")
    d["items"] = dict(sorted(d["items"].items(), key=lambda kv: _sort_key(kv[0])))
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def _sort_key(i):
    m = re.match(r"([A-Z0-9]+)-(\d+)$", i)
    return (m.group(1), int(m.group(2))) if m else (i, 0)


def expand(tokens):
    """`SB-03..SB-05` → 三个 ID；其余原样。"""
    out = []
    for t in tokens:
        m = re.match(r"^([A-Z0-9]+)-(\d+)\.\.(?:\1-)?(\d+)$", t)
        if m:
            a, b = int(m.group(2)), int(m.group(3))
            width = len(m.group(2))
            out += [f"{m.group(1)}-{n:0{width}d}" for n in range(a, b + 1)]
        else:
            out.append(t)
    return out


def check(strict=False):
    d, ids = load()["items"], report_ids()
    errs = []
    for i in ids:
        if i not in d:
            errs.append(f"缺条目：{i}")
    for i, e in d.items():
        if i not in ids:
            errs.append(f"{i} 不在报告里（拼错？）")
            continue
        st = e.get("status")
        if st not in STATUSES:
            errs.append(f"{i} 状态非法：{st!r}")
        elif st == "fixed":
            if not e.get("where") or not e.get("note"):
                errs.append(f"{i} fixed 缺 where / note")
            for w in str(e.get("where", "")).split(" | "):
                path = w.split("::")[0].strip()
                if path and not (REPO / path).exists():
                    errs.append(f"{i} where 指向不存在的文件：{path}")
        elif st == "superseded" and not (e.get("ref") and e.get("note")):
            errs.append(f"{i} superseded 缺 ref / note")
        elif st == "declined" and not e.get("note"):
            errs.append(f"{i} declined 缺 note（理由）")
        elif st == "needs-platform" and not (e.get("verify") and e.get("note")):
            errs.append(f"{i} needs-platform 缺 verify / note")
        elif st == "open" and strict:
            errs.append(f"{i} 仍 open")
    return errs


def cmd_init(_a):
    d, ids = load(), report_ids()
    new = 0
    for i, meta in ids.items():
        if i not in d["items"]:
            d["items"][i] = {"status": "open", "title": meta["title"], "cat": meta["cat"]}
            new += 1
    save(d)
    print(f"报告 {len(ids)} 个 ID；新增 {new} 条 open；共 {len(d['items'])} 条")


def cmd_set(a):
    d = load()
    for i in expand(a.ids):
        if not _ID.match(i):
            sys.exit(f"ID 格式不对：{i}")
        e = d["items"].setdefault(i, {})
        e["status"] = a.status
        for k in ("where", "note", "ref", "verify"):
            v = getattr(a, k)
            if v:
                e[k] = v
    save(d)
    print(f"已处置 {len(expand(a.ids))} 条 → {a.status}")


def cmd_summary(_a):
    d = load()["items"]
    by = collections.defaultdict(collections.Counter)
    for i, e in d.items():
        by[i.split("-")[0]][e.get("status", "?")] += 1
    print(f"{'前缀':6}" + "".join(f"{s:>16}" for s in STATUSES))
    tot = collections.Counter()
    for p in sorted(by):
        print(f"{p:6}" + "".join(f"{by[p][s]:>16}" for s in STATUSES))
        tot.update(by[p])
    print(f"{'合计':6}" + "".join(f"{tot[s]:>16}" for s in STATUSES) + f"   共 {sum(tot.values())}")


def cmd_open(a):
    d = load()["items"]
    n = 0
    for i, e in d.items():
        if e.get("status") == "open" and (not a.prefix or i.startswith(a.prefix)):
            print(f"{i}\t{e.get('cat', '')}\t{e.get('title', '')}")
            n += 1
    print(f"-- {n} 条 open")


def cmd_render(_a):
    d, ids = load()["items"], report_ids()
    cnt = collections.Counter(e.get("status") for e in d.values())
    lines = ["# skills 审查处置台账（闭环）", "",
             "> 对应 `reports/skills_review_20260929.md`。**每个条目 ID 都有去向**；数据源 `docs/skills_review_closure.json`（`tools/closure_ledger.py` 维护，"
             "`tests/unit/test_closure_ledger.py` 守）。生成：`python tools/closure_ledger.py render`。", "",
             "状态：**fixed** 本轮已改 · **superseded** 被别的改动一并解决 · **declined** 有意不改（含范本）· **needs-platform** 依赖平台实测或业务裁定 · **open** 未处理。", "",
             "| 状态 | " + " | ".join(STATUSES) + " | 合计 |", "|---|" + "---|" * (len(STATUSES) + 1),
             "| 条数 | " + " | ".join(str(cnt[s]) for s in STATUSES) + f" | {sum(cnt.values())} |", ""]
    groups = collections.defaultdict(list)
    for i in d:
        groups[i.split("-")[0]].append(i)
    order = ["T0", "X", "P0"] + sorted(p for p in groups if p not in ("T0", "X", "P0"))
    for p in order:
        if p not in groups:
            continue
        lines += [f"## {p}", "", "| ID | 状态 | 位置 / 依据 | 说明 |", "|---|---|---|---|"]
        for i in sorted(groups[p], key=_sort_key):
            e = d[i]
            where = str(e.get("where") or e.get("ref") or e.get("verify") or "").replace("|", "\\|")
            note = (e.get("note") or "").replace("|", "\\|").replace("\n", " ")
            title = (ids.get(i, {}).get("title") or e.get("title") or "").replace("|", "\\|")
            lines.append(f"| {i} | {e.get('status')} | {where} | {note or title} |")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成 {OUT_MD}（{sum(cnt.values())} 条）")


def cmd_check(a):
    errs = check(a.strict)
    for e in errs[:60]:
        print("✗", e)
    print(f"{'通过' if not errs else f'{len(errs)} 处问题'}")
    return 1 if errs else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="skills 审查条目处置登记")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    p = sub.add_parser("set")
    p.add_argument("--status", required=True, choices=STATUSES)
    p.add_argument("--where")
    p.add_argument("--note")
    p.add_argument("--ref")
    p.add_argument("--verify")
    p.add_argument("ids", nargs="+")
    sub.add_parser("summary")
    p = sub.add_parser("open")
    p.add_argument("prefix", nargs="?")
    sub.add_parser("render")
    p = sub.add_parser("check")
    p.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    return {"init": cmd_init, "set": cmd_set, "summary": cmd_summary, "open": cmd_open,
            "render": cmd_render, "check": cmd_check}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
