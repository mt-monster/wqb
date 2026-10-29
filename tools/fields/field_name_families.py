"""按字段族（剥掉统计后缀 / 哈希后缀）聚类任何 ``get_datafields`` 原始返回。

为什么需要它
------------
``tools/profile_dataset_fields.py`` 的前缀聚类只切到 ``snt21_2neg`` 这一层，
于是 ``snt21_2dts_gen_165`` 这类「族名 + 哈希 + 序号」的字段会整批落进
「未归类」，机制设计的语义分档缺一层。本工具补的就是这一层：

* 先剥统计后缀（mean / median / max / min / std / conf_low / conf_up / ...），
* 再剥尾部纯数字（哈希或序号），
* 剩下的就是「族名」，同族字段共享一份 description 模板。

零平台配额：只读本地已保存的 raw JSON。

用法
----
    python tools/field_name_families.py \
        --input tracking/USA/reports/field_profiles/sentiment21_raw.json \
        --top 40

    # 只看某族，并打印该族全部字段
    python tools/field_name_families.py --input ... --family snt21_2dts --fields

    # 输出 markdown 片段（便于贴进画像文档）
    python tools/field_name_families.py --input ... --markdown
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# 统计/派生后缀：剥掉之后剩下的才是「族名」
STAT_SUFFIXES = (
    "conf_low",
    "conf_up",
    "mean",
    "median",
    "max",
    "min",
    "std",
    "var",
    "sum",
    "count",
    "score",
    "value",
    "rank",
    "zscore",
)

_HASH_TAIL = re.compile(r"[_\-]?\d+$")


def load_fields(path: Path) -> list[dict]:
    """读 ``get_datafields`` 原始返回，容忍多种外层形状。"""
    text = path.read_text(encoding="utf-8-sig")
    data = json.loads(text)
    if isinstance(data, dict):
        for key in ("results", "datafields", "fields", "items"):
            if isinstance(data.get(key), list):
                data = data[key]
                break
        else:
            raise SystemExit(f"{path}: 无法在字典里找到字段列表（键={list(data)[:8]}）")
    if not isinstance(data, list):
        raise SystemExit(f"{path}: 期望 list 或含 results 的 dict，实际 {type(data)}")
    return [f for f in data if isinstance(f, dict)]


def family_of(field_id: str) -> str:
    """字段名 -> 族名：交替剥尾部数字与统计后缀，直到稳定。

    必须交替：``snt21_2neg_conf_low_150`` 先剥数字得 ``snt21_2neg_conf_low``，
    再剥统计后缀得 ``snt21_2neg``。只做一轮会漏掉后半段。
    """
    name = field_id.strip().lower()
    while True:
        before = name
        stripped_hash = _HASH_TAIL.sub("", name)
        if stripped_hash and stripped_hash != name:
            name = stripped_hash
        for suffix in STAT_SUFFIXES:
            tail = "_" + suffix
            if name.endswith(tail) and len(name) > len(tail):
                name = name[: -len(tail)]
                break
        if name == before:
            return name


def pct(value) -> str:
    return "-" if value is None else f"{value:.3f}"


def build_groups(fields: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for f in fields:
        fid = str(f.get("id") or f.get("name") or "")
        if not fid:
            continue
        groups[family_of(fid)].append(f)
    return groups


def summarize(group: list[dict]) -> dict:
    covs = [f.get("coverage") for f in group if isinstance(f.get("coverage"), (int, float))]
    users = [f.get("userCount") for f in group if isinstance(f.get("userCount"), (int, float))]
    alphas = [f.get("alphaCount") for f in group if isinstance(f.get("alphaCount"), (int, float))]
    types = sorted({str(f.get("type")) for f in group if f.get("type")})
    return {
        "n": len(group),
        "cov_avg": sum(covs) / len(covs) if covs else None,
        "cov_min": min(covs) if covs else None,
        "cov_max": max(covs) if covs else None,
        "user_max": max(users) if users else None,
        "alpha_max": max(alphas) if alphas else None,
        "types": "/".join(types) or "-",
    }


def sample_desc(group: list[dict], width: int) -> str:
    for f in group:
        desc = (f.get("description") or "").strip()
        if desc:
            desc = " ".join(desc.split())
            return desc[:width] + ("…" if len(desc) > width else "")
    return "-"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="按字段族聚类 get_datafields 原始返回")
    ap.add_argument("--input", required=True, help="get_datafields 原始 JSON 路径")
    ap.add_argument("--top", type=int, default=30, help="打印前 N 个族（默认 30）")
    ap.add_argument("--width", type=int, default=90, help="样例描述截断宽度")
    ap.add_argument("--family", default=None, help="只打印该族（前缀匹配）的全字段")
    ap.add_argument("--fields", action="store_true", help="配合 --family，列出该族全部字段")
    ap.add_argument("--markdown", action="store_true", help="输出 markdown 表格")
    args = ap.parse_args(argv)

    path = Path(args.input)
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        raise SystemExit(f"文件不存在：{path}")

    fields = load_fields(path)
    groups = build_groups(fields)
    total = sum(len(v) for v in groups.values())
    print(f"字段总数 {len(fields)}（入族 {total}） / 族数 {len(groups)}  ← {path.name}")
    print()

    if args.family:
        wanted = args.family.lower()
        hits = {k: v for k, v in groups.items() if k.startswith(wanted)}
        if not hits:
            print(f"没有族名以 {args.family!r} 开头。可用族名：")
            for name in sorted(groups):
                print("  " + name)
            return 1
        for name in sorted(hits):
            s = summarize(hits[name])
            print(f"## {name}  n={s['n']}  cov={pct(s['cov_min'])}–{pct(s['cov_max'])}  "
                  f"user_max={s['user_max']}  alpha_max={s['alpha_max']}  {s['types']}")
            print(f"   {sample_desc(hits[name], 200)}")
            if args.fields:
                for f in sorted(hits[name], key=lambda x: str(x.get("id"))):
                    print(f"   - {f.get('id'):40s} cov={pct(f.get('coverage'))}  "
                          f"u={f.get('userCount')}  a={f.get('alphaCount')}  "
                          f"{(f.get('description') or '').strip()[:110]}")
            print()
        return 0

    ranked = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    if args.markdown:
        print("| 族 | 字段数 | cov 均值 | cov 区间 | user_max | alpha_max | 类型 | 样例描述 |")
        print("|---|---|---|---|---|---|---|---|")
        for name, group in ranked[: args.top]:
            s = summarize(group)
            print(f"| `{name}` | {s['n']} | {pct(s['cov_avg'])} | "
                  f"{pct(s['cov_min'])}–{pct(s['cov_max'])} | {s['user_max']} | "
                  f"{s['alpha_max']} | {s['types']} | {sample_desc(group, args.width)} |")
        return 0

    header = f"{'族名':32s} {'n':>4s} {'cov均值':>7s} {'cov区间':>15s} {'user':>5s} {'alpha':>6s} 类型"
    print(header)
    print("-" * len(header))
    for name, group in ranked[: args.top]:
        s = summarize(group)
        print(
            f"{name:32s} {s['n']:4d} {pct(s['cov_avg']):>7s} "
            f"{pct(s['cov_min'])+'–'+pct(s['cov_max']):>15s} "
            f"{str(s['user_max']):>5s} {str(s['alpha_max']):>6s} {s['types']}"
        )
    print()
    print(f"（其余 {max(0, len(ranked) - args.top)} 个族未显示；--top 加大或 --family 点名）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
