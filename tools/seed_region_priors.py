# -*- coding: utf-8 -*-
"""区域 priors 自动装配器（evidence-driven，不手写、不编造）。

## 背景

`brain-make-some-gem/scripts/trailSomeAlphas/skeletons.py::load_region_priors()`
会读取 `references/regions/<REGION>.md` 的 `## priors` 段并注入 GEM prompt。
实测 **14 个区域里 13 个没有该段**（只有 GBR 有）→ 通道闲置，priors 恒为空。

priors 会进 LLM prompt，**内容必须有数据出处**，手写等于编造。故本脚本只装配
可从 DB 直接验证的三类事实：拥挤度、白空间、已判死。

## 数据来源（全部来自 data/wqb.db）

- `datasets` × `regions`：该区数据集的 status / alpha_count / coverage / category
- `registry_empirical`：该区已判死条目（dead_at 非空）与实证笔记（payload.note）

## 用法

    python tools/seed_region_priors.py                 # 干跑，打印将写入的内容
    python tools/seed_region_priors.py --apply         # 写盘（自动备份 .bak）
    python tools/seed_region_priors.py --region GLB --apply

## 纪律

- 只替换/追加 `## priors` 段，**不动文件其余内容**；
- 写盘前备份 `<REGION>.md.bak_<ts>`；
- 输出限长 1800 字符（`load_region_priors` 截断上限 2000）。
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time

import sys as _sys, os as _os
_sys.path.insert(0, str(_os.path.join(
    _os.path.dirname(_os.path.abspath(__file__)), '..', 'src')))
from wqb.db_conn import connect as db_connect  # 规范工厂（禁裸 sqlite3.connect）
MAX_CHARS = 1800
PRIORS_RE = re.compile(r"^##\s*priors[^\n]*\n(.*?)(?=^##\s|\Z)",
                       re.IGNORECASE | re.MULTILINE | re.DOTALL)


def _default_db() -> str:
    root = os.environ.get("WQB_ROOT") or os.getcwd()
    return os.environ.get("WQB_DB_PATH") or os.path.join(root, "data", "wqb.db")


def _regions_dir() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(
        here, "..", "Claude", "skills", "wq-brain-ra-pipeline",
        "references", "regions"))


def build_priors(conn, region: str) -> str:
    """从 DB 装配该区的 priors 文本（每条都有数据出处）。"""
    lines: list = []

    # 1) 拥挤度：alphaCount 最高的数据集（避开已被挖烂的）
    rows = conn.execute(
        """
        SELECT d.name, d.alpha_count, d.coverage, d.status
        FROM datasets d JOIN regions rg ON rg.id = d.region_id
        WHERE rg.name = ?
        ORDER BY COALESCE(d.alpha_count, 0) DESC LIMIT 5
        """, (region,)).fetchall()
    if rows:
        top = "; ".join(f"{n}(alphaCount={ac or 0}, cov={cov if cov is None else round(cov,2)})"
                        for n, ac, cov, _ in rows[:3])
        lines.append(f"- 拥挤数据集 TOP3（避免重复挖）：{top}")

    # 2) 白空间：未测 + 覆盖达标 + alphaCount 低
    ws = conn.execute(
        """
        SELECT d.name, d.coverage, d.alpha_count
        FROM datasets d JOIN regions rg ON rg.id = d.region_id
        WHERE rg.name = ? AND COALESCE(d.status,'') IN ('untried','')
          AND COALESCE(d.coverage,0) >= 0.6
        ORDER BY COALESCE(d.alpha_count,0) ASC, COALESCE(d.coverage,0) DESC
        LIMIT 5
        """, (region,)).fetchall()
    if ws:
        txt = "; ".join(f"{n}(cov={round(cov,2)}, alphaCount={ac or 0})"
                        for n, cov, ac in ws)
        lines.append(f"- 白空间候选（未测 + 覆盖≥60% + 低 alphaCount）：{txt}")

    # 3) 已判死（dead_at 非空）
    dead = conn.execute(
        """
        SELECT entry_id, family FROM registry_empirical
        WHERE region = ? AND dead_at IS NOT NULL
        ORDER BY updated_at DESC LIMIT 8
        """, (region,)).fetchall()
    if dead:
        names = sorted({str(e or f) for e, f in dead})
        lines.append("- 已判死（勿重试）：" + ", ".join(names[:8]))

    # 4) 实证笔记（payload.note）
    notes = conn.execute(
        """
        SELECT entry_id, payload FROM registry_empirical
        WHERE region = ? AND dead_at IS NULL AND payload IS NOT NULL
        ORDER BY updated_at DESC LIMIT 12
        """, (region,)).fetchall()
    out_notes = []
    for eid, payload in notes:
        m = re.search(r'"note"\s*:\s*"([^"]{4,120})"', str(payload))
        if m:
            out_notes.append(f"{eid}: {m.group(1)}")
        if len(out_notes) >= 5:
            break
    if out_notes:
        lines.append("- 实证笔记：" + " | ".join(out_notes))

    if not lines:
        return ""
    body = "\n".join(lines)
    return body[:MAX_CHARS]


def main() -> int:
    ap = argparse.ArgumentParser(description="区域 priors 自动装配（evidence-driven）")
    ap.add_argument("--region", action="append", default=[], help="区域，可重复；缺省=全部")
    ap.add_argument("--apply", action="store_true", help="写盘（缺省仅干跑）")
    ap.add_argument("--force", action="store_true",
                    help="覆盖已存在的 priors 段（默认只填空，保护人工沉淀）")
    args = ap.parse_args()

    db = _default_db()
    rdir = _regions_dir()
    if not os.path.isfile(db):
        print(f"[priors] 找不到 DB：{db}", file=sys.stderr)
        return 1
    if not os.path.isdir(rdir):
        print(f"[priors] 找不到区域目录：{rdir}", file=sys.stderr)
        return 1

    conn = db_connect(db, readonly=True)     # 只读工具必须 readonly=True
    try:
        targets = [r.upper() for r in args.region] or sorted(
            f[:-3] for f in os.listdir(rdir) if f.endswith(".md"))
        changed, empty, skipped_existing = [], [], []
        for reg in targets:
            path = os.path.join(rdir, f"{reg}.md")
            if not os.path.isfile(path):
                continue
            body = build_priors(conn, reg)
            if not body:
                empty.append(reg)
                print(f"[priors] {reg}: 无可验证事实，跳过（不写空段）")
                continue
            text = open(path, encoding="utf-8").read()
            has_priors = bool(PRIORS_RE.search(text))
            if has_priors and not args.force:
                # 人工沉淀的 priors（如 GBR 的 T-KB-* wins / dead_ends）价值远高于
                # 机器聚合的统计，**默认绝不覆盖**（2026-10-02 教训：曾误覆盖 GBR
                # 1112 字符的人工实证，已还原）。
                skipped_existing.append(reg)
                print(f"[priors] {reg}: 已有人工 priors，跳过（--force 才会覆盖）")
                continue
            section = f"## priors\n{body}\n"
            if has_priors:
                new_text = PRIORS_RE.sub(lambda _m: section, text, count=1)
            else:
                new_text = text.rstrip() + "\n\n" + section
            if new_text == text:
                continue
            if args.apply:
                bak = f"{path}.bak_{time.strftime('%Y%m%d_%H%M%S')}"
                open(bak, "w", encoding="utf-8").write(text)
                open(path, "w", encoding="utf-8").write(new_text)
            changed.append(reg)
            print(f"[priors] {reg}: {len(body)} 字符"
                  + ("（已写盘，备份 .bak）" if args.apply else "（干跑）"))
            if not args.apply:
                print("    " + body.replace("\n", "\n    ")[:600])
    finally:
        conn.close()

    print()
    print(f"[priors] 将变更 {len(changed)} 个区域：{', '.join(changed) or '无'}")
    if skipped_existing:
        print(f"[priors] 保护已有人 priors {len(skipped_existing)} 个：{', '.join(skipped_existing)}")
    if empty:
        print(f"[priors] 无数据跳过 {len(empty)} 个：{', '.join(empty)}")
    if not args.apply and changed:
        print("[priors] 这是干跑；加 --apply 才会写盘。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
