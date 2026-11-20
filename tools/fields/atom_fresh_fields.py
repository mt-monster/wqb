# -*- coding: utf-8 -*-
"""atom_fresh_fields.py — 按 onboard 时间找 ATOM 蓝海字段（零仿真，只读平台）。

背景（外部经验，见 docs/experience/06_atom_mining.md §6）：
  老数据集里 alphaCount==0 的字段，多半是被全平台脚本犁过无数遍仍无信号的**死字段**。
  真正的白空间是**近期 onboard 的字段**：prod 相关性低（先发优势）、Pyramid 倍率常 1.3-1.8x、
  套最简单的二阶/三阶单字段模板即可过检（叠加 ATOM 免 IS-Ladder）。

本工具做的事：枚举某区数据集 → 逐集实拉字段 → 按 `dateCreated` 降序 + `alphaCount` 升序 +
覆盖率过滤 → 汇总「最新可挖字段」清单（带数据集倍率、类型、覆盖、ac），供 ATOM 选题直接消费。

用法:
  python tools/fields/atom_fresh_fields.py --region GBR --universe TOP700 --delay 1
  python tools/fields/atom_fresh_fields.py --region GBR --universe TOP700 --delay 1 --min-coverage 0.8 --top 30
  python tools/fields/atom_fresh_fields.py --region USA --universe TOP3000 --delay 1 --category fundamental --top 40
  python tools/fields/atom_fresh_fields.py ... --refresh --json cache/_scratch/atom_fresh_gbr.csv.json

退出码: 0=有候选 / 2=无候选（无字段或全被覆盖率过滤）/ 1=工具故障
缓存: cache/_scratch/atom_fresh_<REGION>_<UNIVERSE>_d<delay>[_<category>].json，默认 TTL 24h；
      字段目录会变（实测 herfindahl_index_holdings 被替换），过期必须重拉（--refresh 强制）。

⚠ 只读：只调 get_datasets / get_datafields，不派仿真、不写库、不提交。
"""
from __future__ import annotations

import argparse
import asyncio
import datetime as _dt
import json
import os
import sys
import time

# 2026-11-19 下沉到 tools/fields/（S11 顶层冻结）：_pyenv 在 tools/ 一层，
# 故把 tools/ 目录（而非脚本所在目录）加进 sys.path。
_TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _TOOLS_DIR)
import _pyenv  # noqa: E402  跨平台解释器 / MCP 目录解析（与 campaign_intel 等一致）

_REPO_ROOT = os.path.dirname(_TOOLS_DIR)


def _bootstrap():
    _pyenv.reexec_under_venv()
    _pyenv.bootstrap_paths()


def _default_cache(region: str, universe: str, delay: int, category: str | None) -> str:
    tag = f"atom_fresh_{region}_{universe}_d{delay}"
    if category:
        tag += f"_{category}"
    return os.path.join(_REPO_ROOT, "cache", "_scratch", tag + ".json")


def _age_hours(path: str) -> float:
    return (time.time() - os.path.getmtime(path)) / 3600.0


async def collect_async(region, universe, delay, category, min_coverage, per_dataset,
                  max_datasets, sleep_s, drop_unknown_coverage=False, data_type=""):
    from brain_api import brain_client  # noqa: F401  延迟导入，保证 bootstrap 已跑

    datasets = await brain_client.get_datasets(
        category=category or None, region=region, delay=delay, universe=universe,
    )
    if isinstance(datasets, dict):
        rows = datasets.get("results") or datasets.get("result") or []
    else:
        rows = datasets or []
    ds_rows = [d for d in rows if isinstance(d, dict) and d.get("id")]
    if max_datasets:
        ds_rows = ds_rows[: int(max_datasets)]

    out = []
    for i, d in enumerate(ds_rows, 1):
        ds_id = d["id"]
        try:
            payload = await brain_client.get_datafields(
                "EQUITY", region, delay, universe, "false", ds_id, data_type, None, False, None,
            )
        except Exception as e:  # 单集失败不中断全量
            print(f"  [{i}/{len(ds_rows)}] {ds_id}: ERR {e}", file=sys.stderr)
            continue
        fields = payload.get("results") if isinstance(payload, dict) else payload
        fields = [f for f in (fields or []) if isinstance(f, dict) and f.get("id")]
        kept = []
        for f in fields:
            try:
                cov = float(f.get("coverage"))
            except (TypeError, ValueError):
                cov = 0.0
            # 2026-11-17 实测：GBR 大量数据集字段级 coverage 元数据报 0（≠真的无数据，
            # 同 covered=0 的数据集级盲区，见 AGENTS §8.11）。cov<=0 一律按「未知」处理：
            # 缺省保留（否则整集被静默清空），--drop-unknown-coverage 才严格剔除。
            if cov <= 0:
                if drop_unknown_coverage:
                    continue
            elif cov < min_coverage:
                continue
            kept.append(f)
        kept.sort(key=lambda f: (str(f.get("dateCreated") or "0000-00-00"),
                                 -float(f.get("alphaCount") or 0)), reverse=True)
        kept = kept[: int(per_dataset)]
        for f in kept:
            out.append({
                "dateCreated": f.get("dateCreated"),
                "dataset": ds_id,
                "category": (d.get("category") or {}).get("id")
                if isinstance(d.get("category"), dict) else d.get("category"),
                "dataset_multiplier": d.get("pyramidMultiplier"),
                "dataset_alphaCount": d.get("alphaCount"),
                "field": f.get("id"),
                "type": f.get("type"),
                "coverage": f.get("coverage"),
                "alphaCount": f.get("alphaCount"),
                "userCount": f.get("userCount"),
                "field_multiplier": f.get("pyramidMultiplier"),
            })
        if i % 20 == 0 or i == len(ds_rows):
            print(f"  [{i}/{len(ds_rows)}] {ds_id}: {len(fields)} 字段, kept {len(kept)}",
                  file=sys.stderr, flush=True)
        if sleep_s:
            time.sleep(sleep_s)
    return out


def _rank(rows, top, exclude_types="SYMBOL"):
    """剔除不可作信号的类型（缺省 SYMBOL：日期/字符串字段）。"""
    ex = {s.strip().upper() for s in (exclude_types or "").split(",") if s.strip()}
    if ex:
        rows = [r for r in rows if str(r.get("type") or "").upper() not in ex]
    rows = sorted(rows, key=lambda r: (str(r.get("dateCreated") or "0000-00-00"),
                                       -float(r.get("alphaCount") or 0)), reverse=True)
    return rows[: int(top)] if top else rows


def _cov_str(v):
    """coverage 展示：<=0 或缺失按「未知」显示为 ?（GBR 普遍盲区，不是无数据）。"""
    try:
        cov = float(v)
    except (TypeError, ValueError):
        return "?"
    return "?" if cov <= 0 else f"{cov:.3f}"


def _render(rows):
    if not rows:
        print("(无候选：检查 --min-coverage 是否过严，或该区字段确实都老)")
        return
    hdr = f"{'onboard':<11} {'dataset':<26} {'cat':<12} {'mult':>5} {'field':<44} {'type':<7} {'cov':>6} {'ac':>5}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{str(r['dateCreated'] or '?'):<11} {str(r['dataset']):<26} {str(r['category']):<12} "
              f"{str(r['dataset_multiplier']):>5} {str(r['field'])[:44]:<44} {str(r['type']):<7} "
              f"{_cov_str(r['coverage']):>6} {str(r['alphaCount']):>5}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="按 onboard 时间找 ATOM 蓝海字段（只读，零仿真）")
    ap.add_argument("--region", required=True)
    ap.add_argument("--universe", required=True)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--category", default=None, help="只扫某 category（如 fundamental / analyst）")
    ap.add_argument("--data-type", default="",
                    help="字段类型过滤：""=全部（缺省，含 VECTOR）/ MATRIX / VECTOR。⚠ 硬写 MATRIX 会让 VECTOR 集显示 0 字段")
    ap.add_argument("--min-coverage", type=float, default=0.5,
                    help="覆盖率下限（缺省 0.5）。⚠ 阈值随宇宙变：USA/TOP3000 常用 0.80，"
                         "GBR/TOP700 字段覆盖普遍 0.44-0.55，用 0.80 会全过滤空")
    ap.add_argument("--per-dataset", type=int, default=3, help="每集最多保留几个最新字段（缺省 3）")
    ap.add_argument("--max-datasets", type=int, default=None, help="只扫前 N 个数据集（快速试跑）")
    ap.add_argument("--top", type=int, default=30, help="最终输出条数（缺省 30）")
    ap.add_argument("--exclude-types", default="SYMBOL",
                    help="剔除的字段类型（逗号分隔，缺省 SYMBOL：日期/字符串不可作信号）；传空串则全保留")
    ap.add_argument("--sleep", type=float, default=0.15, help="逐集间隔秒数（防 429，缺省 0.15）")
    ap.add_argument("--cache-file", default=None)
    ap.add_argument("--ttl-hours", type=float, default=24.0)
    ap.add_argument("--drop-unknown-coverage", action="store_true",
                    help="把 coverage<=0 的字段按无数据剔除（缺省保留：该区元数据普遍报 0）")
    ap.add_argument("--refresh", action="store_true", help="忽略缓存重拉")
    ap.add_argument("--json", default=None, help="把候选写到该 JSON 路径")
    args = ap.parse_args(argv)

    cache = args.cache_file or _default_cache(args.region, args.universe, args.delay, args.category)
    rows = None
    if os.path.exists(cache) and not args.refresh:
        age = _age_hours(cache)
        if age <= args.ttl_hours:
            try:
                rows = json.load(open(cache, encoding="utf-8")).get("rows")
                print(f"[cache] {cache}（{age:.1f}h 前，--refresh 可强制重拉）", file=sys.stderr)
            except Exception:
                rows = None
    if rows is None:
        _bootstrap()
        print(f"[pull] {args.region}/{args.universe}/D{args.delay}"
              f"{' category=' + args.category if args.category else ''} — 逐集实拉字段…",
              file=sys.stderr, flush=True)
        try:
            rows = asyncio.run(collect_async(args.region, args.universe, args.delay, args.category,
                                             args.min_coverage, args.per_dataset,
                                             args.max_datasets, args.sleep,
                                             args.drop_unknown_coverage, args.data_type))
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        json.dump({"generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
                   "scope": {"region": args.region, "universe": args.universe, "delay": args.delay,
                             "category": args.category, "data_type": args.data_type,
                             "min_coverage": args.min_coverage,
                             "drop_unknown_coverage": args.drop_unknown_coverage},
                   "rows": rows}, open(cache, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[cache] 已写 {cache}（{len(rows)} 行）", file=sys.stderr)

    top = _rank(rows, args.top, args.exclude_types)
    _render(top)
    if args.json:
        os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
        json.dump(top, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[json] {args.json}", file=sys.stderr)
    return 0 if top else 2


if __name__ == "__main__":
    sys.exit(main())
