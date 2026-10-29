#!/usr/bin/env python
"""数据集字段画像：把 ``get_datafields`` 的原始返回压成一份可决策的画像报告。

S1 体检的**离线**部分（零平台配额）。输入是 ``get_datafields`` 落盘的 JSON
（形如 ``{"results": [...], "count": N, "platform_count": N, "complete": true}``），
也可以是 MCP 外部化 artifact（``*.readable.v1.jsonl``）。

输出四块：

1. **规模与完整性**：字段数、平台声明数、是否完整拉全、类型分布
2. **可用性**：coverage / userCount / alphaCount 分档（拥挤度决定 prod 相关性风险）
3. **语义结构**：经 ``field_semantic_classify`` 分族 + 时间朝向（已实现 vs 预测）
4. **候选短名单**：按「覆盖足够 × 拥挤度低 × 语义可解释」打分排序

用法::

    $WQ_PY tools/profile_dataset_fields.py --region USA --dataset fundamental91 \
        --input tracking/USA/reports/field_profiles/fundamental91_raw.json \
        --out docs/reference/USA/fundamental91_field_profile.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from field_semantic_classify import classify, time_orientation  # noqa: E402

_UNIT_RE = re.compile(r"in\s+(?:USD|dollars?|percent|%|shares?|days?|millions?|billions?)", re.I)
_GROUP_HINTS = re.compile(r"^(?:sector|industry|subindustry|country|exchange|market|currency)$", re.I)


def load_payload(path: Path) -> dict:
    """读 datafields 落盘 JSON 或 MCP artifact。"""
    if path.suffix == ".jsonl" or path.name.endswith(".readable.v1.jsonl"):
        from read_tool_artifact import extract_json, load_text

        data = extract_json(load_text(path))
    else:
        # PowerShell 的 `Out-File -Encoding utf8` 会写 BOM，统一用 utf-8-sig 兜住
        data = json.loads(path.read_text(encoding="utf-8-sig"))

    if isinstance(data, list):
        data = data[0] if len(data) == 1 else {"results": data}
    if not isinstance(data, dict) or "results" not in data:
        raise ValueError(f"{path} 里没有 results 字段（顶层键：{list(data)[:8] if isinstance(data, dict) else type(data)}）")
    return data


def bucket_coverage(cov: float | None) -> str:
    if cov is None:
        return "未知"
    if cov >= 0.90:
        return "≥0.90（可直接做尽）"
    if cov >= 0.70:
        return "0.70–0.90（sub/robust 需关注）"
    if cov >= 0.40:
        return "0.40–0.70（稀疏，慎用）"
    return "<0.40（枯竭）"


def bucket_crowd(user: int | None, alpha: int | None) -> str:
    u = user or 0
    a = alpha or 0
    if u == 0 and a == 0:
        return "零竞争"
    if a <= 50:
        return "低拥挤（≤50 alpha）"
    if a <= 500:
        return "中拥挤（51–500）"
    if a <= 5000:
        return "高拥挤（501–5000）"
    return "极高拥挤（>5000）"


def prefix_of(name: str, depth: int = 2) -> str:
    parts = re.split(r"[_.]", name)
    return "_".join(parts[:depth]) if len(parts) >= depth else name


def score_field(rec: dict) -> float:
    """候选打分：覆盖够 + 拥挤低 + 语义可解释 + 非非信号。"""
    cov = rec.get("coverage") or 0.0
    alpha = rec.get("alphaCount") or 0
    score = 0.0
    score += 40 * min(cov / 0.95, 1.0)
    if alpha == 0:
        score += 25
    elif alpha <= 50:
        score += 20
    elif alpha <= 500:
        score += 12
    elif alpha <= 5000:
        score += 5
    fam, label = classify(rec.get("description", ""), rec.get("id", ""))
    if fam is None:
        score -= 30
    elif fam != "other":
        score += 20
    orient = time_orientation(rec.get("id", ""), rec.get("description", ""))
    if orient == "forecast":
        score += 5  # 前瞻信息比事后已实现信息更有预测力（GLB/analyst_consensus 实证）
    elif orient == "mixed":
        score += 3
    return round(score, 1)


def build_report(region: str, dataset: str, payload: dict, top: int) -> str:
    rows = [r for r in payload.get("results", []) if isinstance(r, dict)]
    count = payload.get("count")
    platform_count = payload.get("platform_count")
    complete = payload.get("complete")

    type_ct = Counter((r.get("type") or "?").upper() for r in rows)
    cov_ct = Counter(bucket_coverage(r.get("coverage")) for r in rows)
    crowd_ct = Counter(bucket_crowd(r.get("userCount"), r.get("alphaCount")) for r in rows)

    fam_ct: Counter = Counter()
    fam_fields: dict[str, list[str]] = defaultdict(list)
    orient_ct: Counter = Counter()
    for r in rows:
        fam, label = classify(r.get("description", ""), r.get("id", ""))
        key = label if fam is not None else label
        fam_ct[key] += 1
        fam_fields[key].append(r.get("id", ""))
        orient_ct[time_orientation(r.get("id", ""), r.get("description", "")) or "unknown"] += 1

    pref_ct = Counter(prefix_of(r.get("id", "")) for r in rows)

    covs = [r.get("coverage") for r in rows if isinstance(r.get("coverage"), (int, float))]
    avg_cov = sum(covs) / len(covs) if covs else 0.0
    zero_comp = sum(1 for r in rows if not (r.get("userCount") or 0))
    units = sum(1 for r in rows if _UNIT_RE.search(r.get("description") or ""))

    scored = sorted(rows, key=score_field, reverse=True)

    out: list[str] = []
    out.append(f"# {region} · `{dataset}` 字段画像\n")
    out.append(f"> 由 `tools/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。\n")

    out.append("## 1 规模与完整性\n")
    out.append("| 项 | 值 |")
    out.append("|---|---|")
    out.append(f"| 本次返回字段数 | {len(rows)} |")
    out.append(f"| 平台声明数 `platform_count` | {platform_count} |")
    out.append(f"| 返回 `count` | {count} |")
    out.append(f"| 是否完整 `complete` | {complete} |")
    out.append(f"| 类型分布 | {dict(type_ct)} |")
    out.append(f"| 平均 coverage | {avg_cov:.4f} |")
    verdict = "✅ 完整" if complete and platform_count in (None, len(rows)) else "⚠️ 不完整，需重拉"
    out.append(f"| 判定 | {verdict} |")

    out.append("\n## 2 可用性分档\n")
    out.append("### 2.1 coverage\n")
    out.append("| 档 | 字段数 |")
    out.append("|---|---|")
    for k, v in cov_ct.most_common():
        out.append(f"| {k} | {v} |")
    out.append("\n### 2.2 拥挤度（决定 prod 相关性风险）\n")
    out.append("| 档 | 字段数 |")
    out.append("|---|---|")
    for k, v in crowd_ct.most_common():
        out.append(f"| {k} | {v} |")
    out.append(f"\n零竞争字段（`userCount==0`）：**{zero_comp}** / {len(rows)}；描述带单位标注：{units}")

    out.append("\n## 3 语义结构\n")
    out.append("| 语义族 | 字段数 | 示例字段 |")
    out.append("|---|---|---|")
    for k, v in fam_ct.most_common():
        samples = ", ".join(f"`{f}`" for f in fam_fields[k][:4])
        out.append(f"| {k} | {v} | {samples} |")
    out.append("\n**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：\n")
    out.append("| 朝向 | 字段数 |")
    out.append("|---|---|")
    for k, v in orient_ct.most_common():
        out.append(f"| {k} | {v} |")

    out.append("\n## 4 名字前缀聚类（前 15）\n")
    out.append("| 前缀 | 字段数 |")
    out.append("|---|---|")
    for k, v in pref_ct.most_common(15):
        out.append(f"| `{k}` | {v} |")

    out.append(f"\n## 5 候选短名单（Top {top}，按打分排序）\n")
    out.append("打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，"
               "仍须过单位闸与机制假设。\n")
    out.append("| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(scored[:top], 1):
        fam, label = classify(r.get("description", ""), r.get("id", ""))
        orient = time_orientation(r.get("id", ""), r.get("description", "")) or "-"
        desc = (r.get("description") or "").replace("|", "/").strip()
        if len(desc) > 90:
            desc = desc[:89] + "…"
        cov = r.get("coverage")
        cov_s = f"{cov:.3f}" if isinstance(cov, (int, float)) else "-"
        out.append(
            f"| {i} | `{r.get('id','')}` | {r.get('type','')} | {cov_s} | "
            f"{r.get('userCount', 0)} | {r.get('alphaCount', 0)} | {label} | {orient} | "
            f"{score_field(r)} | {desc} |"
        )
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="数据集字段画像（离线）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--input", required=True, type=Path, help="get_datafields 落盘 JSON 或 MCP artifact")
    ap.add_argument("--out", type=Path, default=None, help="markdown 输出路径（缺省只打印）")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args(argv)

    payload = load_payload(args.input)
    report = build_report(args.region, args.dataset, payload, args.top)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
        print(f"[profile] 已写 {args.out}（{len(report)} 字符）")
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
