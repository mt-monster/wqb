#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按数据集生成字段画像文档（区域无关，EUR 首发）。

定位（2026-10-20，用户指令「按每个数据集去命名书写字段画像文档」）：
    `tools/fields/field_profile.py` 负责**建画像 / 查画像**；
    本工具负责把画像 + 字段目录 + 本地回测 + 判死台账**渲染成人可读的按数据集文档**。

数据源（全部只读）:
    data/wqb.db
        datasets            数据集元数据（category / coverage / alpha_count / delay）
        fields              字段目录（name / type / coverage / alpha_count / description）
        field_profile_perf  字段级历史实测画像（verdict / best S / 2Y / sub / TO / n_sg）
        backtest_results    本地 COMPLETE 回测（按 alpha_id 去重，后写覆盖先写）
        registry_empirical  dead_end 判死记录（payload.dataset，支持逗号/× 复合归属）
    tracking/<REGION>/config/cells.json              战役 cell 归属
    tracking/<REGION>/reference/*_fields.json         平台快照（确定范围 + 来源留痕）
    tracking/<REGION>/reference/<region>_dataset_ranking.json  排序分 / tier

输出:
    docs/reference/<REGION>/datasets/<dataset>_field_profile.md
    docs/reference/<REGION>/datasets/README.md

默认范围 = 全部有字段目录的数据集；`--active-only` 收窄到 cells ∪ 快照 ∪ 本地已回测。

纪律:
    - 机器段在 BEGIN/END 标记内，`## 人工机制复盘` 在标记外，刷新时保留人工内容。
    - 既有文件**没有标记**时默认不动（`--force` 才把机器段追加到文末），避免覆盖人工文档。
    - 默认 dry-run，`--apply` 才写；只读连接，不写库。
    - 字段语义以 description 为准（复用 field_semantic_type.classify），名字只作对照。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import tempfile
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

# ── 仓库根推导（层数无关；禁止硬编码 parents[N]）───────────────────────
_REPO = next(
    p for p in Path(__file__).resolve().parents
    if (p / "pyproject.toml").exists() and (p / "src" / "wqb").is_dir()
)
for _p in (str(_REPO / "src"), str(_REPO / "tools" / "fields")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from wqb.db_conn import connect as _db_connect  # noqa: E402
from field_profile import family_of, norm_cov  # noqa: E402
from field_semantic_type import SKELETON_HINT, classify  # noqa: E402

BEGIN = "<!-- BEGIN WQB FIELD PROFILE -->"
END = "<!-- END WQB FIELD PROFILE -->"
README_BEGIN = "<!-- BEGIN WQB DATASET PROFILE INDEX -->"
README_END = "<!-- END WQB DATASET PROFILE INDEX -->"

#: 快照 stem → 数据集名的手工别名（其余按 stem / 去掉 region_ 前缀自动解析）
SNAPSHOT_ALIASES = {"insider_agg": "insider_agg_matrix"}

VERDICT_ORDER = {
    "ALIVE": 0, "WEAK": 1, "DEAD": 2, "DEAD_STATIC": 3, "DEAD_TURNOVER": 4,
    "DEAD_COUNT": 5, "UNUSABLE": 6, "AXIS_ONLY": 7, "UNTESTED": 8,
}
SIGNAL_VERDICTS = ("ALIVE", "WEAK")

#: 现有类目级档案（存在才链接；路径相对 `docs/reference/<R>/datasets/`）
_CATEGORY_DOCS = {
    "pv": ("pv_field_profile_20261019.md", "PV 类字段画像与回测档案"),
    "insiders": ("insiders_field_profile_20261020.md", "Insiders 类字段画像"),
    "insights": ("institutions_field_profile_20261020.md", "Institutions 类字段画像"),
    "risk": ("short_interest_risk60_profile_20261020.md", "risk60 证券借贷画像"),
}


# ── 基础工具 ────────────────────────────────────────────────────────────
def _cell(value: Any, default: str = "—") -> str:
    """Markdown 表格单元：转义竖线、压平换行。"""
    if value is None or value == "":
        return default
    return str(value).replace("|", "\\|").replace("\r", "").replace("\n", " ").strip()


def _trunc(text: Any, limit: int) -> str:
    s = _cell(text)
    return s if len(s) <= limit else s[: max(0, limit - 1)].rstrip() + "…"


def _num(value: Any, nd: int = 2, default: str = "—") -> str:
    try:
        if value is None:
            return default
        return f"{float(value):.{nd}f}"
    except (TypeError, ValueError):
        return default


def _pct(value: Any, nd: int = 1, default: str = "—") -> str:
    try:
        if value is None:
            return default
        return f"{float(value) * 100:.{nd}f}%"
    except (TypeError, ValueError):
        return default


def _cov(value: Any) -> Optional[float]:
    try:
        return norm_cov(value)
    except Exception:
        return None


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return None
    except Exception as exc:  # 坏 JSON 不应让整批生成失败
        print(f"[warn] 无法解析 {path}: {type(exc).__name__}", file=sys.stderr)
        return None


def _unpack(value: Any, default: Any = None) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if not value:
        return default
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return default


def _safe_name(dataset: str) -> str:
    """文件名安全化：`/` 与空格替换为 `_`（S16 要求纯 ASCII、小写）。"""
    return re.sub(r"[^A-Za-z0-9_-]+", "_", dataset).strip("_").lower()


def _infer_dataset_names(text: str, names: Iterable[str]) -> List[str]:
    """从自由文本（family / rule）推断数据集名；用于 payload 缺 dataset 的旧记录。"""
    haystack = str(text or "").lower()
    hits: List[str] = []
    for name in sorted({n for n in names if n}, key=len, reverse=True):
        # `_` 视为边界：旧台账常把集名写成 `<dataset>_<probe>`（如 news46_cashless_…）；
        # 多集重叠由下面的「更长命中优先」消歧（insider_agg_matrix 命中时不再收 insider_agg）。
        pattern = r"(?<![a-z0-9])" + re.escape(name.lower()) + r"(?![a-z0-9])"
        if re.search(pattern, haystack):
            hits.append(name)
    # 去掉被更长命中包含的短名（如 pv1 命中 pv106 时）
    return [h for h in hits if not any(h != o and h.lower() in o.lower() for o in hits)]


# ── 数据加载 ────────────────────────────────────────────────────────────
def load_db(db_path: Path, region: str) -> Dict[str, Any]:
    con = _db_connect(str(db_path), readonly=True)
    con.row_factory = None
    try:
        row = con.execute("SELECT id FROM regions WHERE name=?", (region,)).fetchone()
        if not row:
            raise SystemExit(f"[error] 区域 {region} 不在 regions 表")
        rid = row[0]

        datasets: Dict[str, Dict[str, Any]] = {}
        for row in con.execute(
                "SELECT name, category, field_count, coverage, alpha_count, delay, "
                "       value_score, pyramid_multiplier, tier, status, updated_at "
                "FROM datasets WHERE region_id=? AND name IS NOT NULL ORDER BY name", (rid,)):
            name = row[0]
            if name == "_unknown":
                continue
            datasets[name] = {
                "name": name, "category": row[1], "platform_field_count": row[2],
                "coverage": row[3], "alpha_count": row[4], "delay": row[5],
                "value_score": row[6], "pyramid_multiplier": row[7], "tier": row[8],
                "status": row[9], "updated_at": row[10],
            }

        fields: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
        for row in con.execute(
                "SELECT d.name, f.field_name, f.field_type, f.coverage, f.user_count, "
                "       f.alpha_count, f.description "
                "FROM fields f JOIN datasets d ON f.dataset_id=d.id "
                "WHERE d.region_id=? ORDER BY d.name, f.field_name", (rid,)):
            fields[row[0]].append({
                "field": row[1], "type": row[2], "coverage": row[3],
                "user_count": row[4], "alpha_count": row[5], "description": row[6],
            })

        profiles: Dict[Tuple[str, str], Dict[str, Any]] = {}
        for row in con.execute(
                "SELECT dataset, field, ftype, coverage, family, n_tests, to_med, "
                "       best_s, best_2y, best_sub, best_f, verdict, best_s_sg, "
                "       best_2y_sg, best_sub_sg, n_sg, n_skeletons, skeleton_fams "
                "FROM field_profile_perf WHERE region=?", (region,)):
            profiles[(row[0], row[1])] = {
                "dataset": row[0], "field": row[1], "ftype": row[2], "coverage": row[3],
                "family": row[4], "n_tests": row[5], "to_med": row[6],
                "best_s": row[7], "best_2y": row[8], "best_sub": row[9], "best_f": row[10],
                "verdict": row[11], "best_s_sg": row[12], "best_2y_sg": row[13],
                "best_sub_sg": row[14], "n_sg": row[15], "n_skeletons": row[16],
                "skeleton_fams": row[17],
            }

        latest: Dict[str, Dict[str, Any]] = {}
        for row in con.execute(
                "SELECT id, alpha_id, dataset, wave, sharpe, fitness, turnover, "
                "       two_year_sharpe, sub_universe_sharpe, ra_failed_checks, created_at "
                "FROM backtest_results "
                "WHERE region=? AND UPPER(status)='COMPLETE' AND dataset IS NOT NULL "
                "ORDER BY id", (region,)):
            rec = {
                "alpha_id": row[1], "dataset": row[2], "wave": row[3], "sharpe": row[4],
                "fitness": row[5], "turnover": row[6], "two_year": row[7],
                "sub": row[8], "ra_failed_checks": row[9], "created_at": row[10],
            }
            latest[rec["alpha_id"]] = rec
        backtests: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
        for rec in latest.values():
            backtests[rec["dataset"]].append(rec)
        for rows in backtests.values():
            rows.sort(key=lambda r: (-(r["sharpe"] if r["sharpe"] is not None else -1e9),
                                     str(r["alpha_id"])))

        dead_by_ds: Dict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
        region_dead: List[Dict[str, Any]] = []
        for row in con.execute(
                "SELECT entry_id, family, payload, dead_at FROM registry_empirical "
                "WHERE region=? AND layer='dead_end' ORDER BY dead_at, entry_id", (region,)):
            payload = _unpack(row[2], {}) or {}
            raw_ds = payload.get("dataset") or ""
            targets = [x.strip() for x in re.split(r"[,×]", str(raw_ds)) if x.strip()]
            entry = {
                "entry_id": row[0], "family": row[1], "rule": payload.get("rule") or "",
                "evidence": payload.get("evidence") or {}, "wave": payload.get("wave"),
                "dead_at": row[3], "raw_dataset": raw_ds,
                "attribution": "payload" if targets else "region",
            }
            if not targets:
                # 旧记录的 payload 常缺 dataset，但 entry_id / family / rule 里写着数据集名
                # （如 "EUR-ANL39-…" / "shortinterest6 × pattern_scores …"）。
                inferred = _infer_dataset_names(f"{row[0]} {row[1]} {entry['rule']}", datasets)
                if inferred:
                    targets = inferred
                    entry["attribution"] = "inferred"
            if not targets:
                region_dead.append(entry)
            for ds in targets:
                dead_by_ds[ds].append(entry)

        return {
            "datasets": datasets, "fields": fields, "profiles": profiles,
            "backtests": backtests, "dead_by_ds": dead_by_ds, "region_dead": region_dead,
        }
    finally:
        con.close()


def _resolve_snapshot_stem(stem: str, names: Iterable[str]) -> Optional[str]:
    names = set(names)
    for cand in (SNAPSHOT_ALIASES.get(stem), stem,
                 stem[4:] if stem.startswith("eur_") else None):
        if cand and cand in names:
            return cand
    return None


def load_snapshots(ref_dir: Path, dataset_names: Iterable[str]) -> Dict[str, List[str]]:
    """返回 ds → [快照 stem]。支持三种形状：list / {fields: …} / {ds: {fields: …}}。"""
    mapping: Dict[str, List[str]] = collections.defaultdict(list)
    if not ref_dir.is_dir():
        return mapping
    names = set(dataset_names)
    for path in sorted(ref_dir.glob("*_fields.json")):
        stem = path.name[: -len("_fields.json")]
        payload = _read_json(path)
        targets: List[str] = []
        if isinstance(payload, dict) and "fields" not in payload:
            targets = [k for k, v in payload.items()
                       if isinstance(v, dict) and (v.get("fields") or [])]
        elif isinstance(payload, list) and payload:
            ds = _resolve_snapshot_stem(stem, names)
            targets = [ds] if ds else []
        elif isinstance(payload, dict) and payload.get("fields"):
            ds = _resolve_snapshot_stem(stem, names)
            targets = [ds] if ds else []
        for ds in targets:
            ds = SNAPSHOT_ALIASES.get(ds, ds)
            if ds in names:
                mapping[ds].append(stem)
    return mapping


def load_cells(path: Path, dataset_names: Iterable[str]
               ) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, Any]]]:
    """cells.json → (ds → [cell 名], ds → 战役设置覆盖)。

    兼容 dict 形态、`A × B`、`A,B` 与内嵌 JSON 字符串。
    """
    names = set(dataset_names)
    result: Dict[str, List[str]] = collections.defaultdict(list)
    overrides: Dict[str, Dict[str, Any]] = {}
    raw = _read_json(path)
    if not isinstance(raw, dict):
        return result, overrides

    def expand(item: Any) -> List[str]:
        if isinstance(item, dict):
            item = item.get("dataset") or item.get("name") or ""
        if not isinstance(item, str):
            return []
        s = item.strip()
        if s.startswith("{"):
            try:
                return expand(json.loads(s))
            except Exception:
                return []
        return [p.strip() for p in s.replace("×", ",").split(",") if p.strip()]

    for cat, spec in (raw.get("cells") or {}).items():
        items = spec.get("datasets") if isinstance(spec, dict) else spec
        if isinstance(items, dict):
            items = list(items)
        for item in items or []:
            for ds in expand(item):
                if ds in names and cat not in result[ds]:
                    result[ds].append(cat)
        if isinstance(spec, dict):
            for ds, ov in (spec.get("dataset_overrides") or {}).items():
                if ds in names and isinstance(ov, dict):
                    overrides[ds] = {"cell": cat, **ov}
    return result, overrides


def load_ranking(path: Path) -> Dict[str, Dict[str, Any]]:
    raw = _read_json(path)
    if not isinstance(raw, dict):
        return {}
    return {e.get("id"): e for e in raw.get("ranking") or [] if isinstance(e, dict) and e.get("id")}


# ── 统计辅助 ────────────────────────────────────────────────────────────
def attach_profiles(fields: Sequence[Dict[str, Any]],
                    profiles: Dict[Tuple[str, str], Dict[str, Any]]) -> None:
    for f in fields:
        p = profiles.get((f["_dataset"], f["field"])) if "_dataset" in f else None
        if p is None:
            continue
        f["profile"] = p
        f["verdict"] = p["verdict"]
        f["best_s_sg"] = p["best_s_sg"]
        f["best_2y_sg"] = p["best_2y_sg"]
        f["best_sub_sg"] = p["best_sub_sg"]
        f["to_med"] = p["to_med"]
        f["n_sg"] = p["n_sg"]
        f["n_tests"] = p["n_tests"]
        f["family"] = p["family"]
        f["best_s"] = p["best_s"]


def classify_fields(fields: Sequence[Dict[str, Any]]) -> None:
    for f in fields:
        sem, evidence, name_guess, conflict = classify(f.get("description"), f["field"])
        f["sem_type"] = sem
        f["sem_evidence"] = evidence
        f["name_guess"] = name_guess
        f["sem_conflict"] = conflict
        f["family"] = f.get("family") or family_of(f["field"])
        f.setdefault("verdict", None)


def coverage_bucket(cov: Optional[float]) -> str:
    if cov is None:
        return "未知"
    if cov == 0:
        return "0 覆盖"
    if cov < 0.3:
        return "(0, 0.3)"
    if cov < 0.6:
        return "[0.3, 0.6)"
    if cov < 0.9:
        return "[0.6, 0.9)"
    return "[0.9, 1.0]"


def field_priority(f: Dict[str, Any]) -> Tuple[int, float, float, str]:
    v, s = f.get("verdict"), f.get("best_s_sg")
    ac = f.get("alpha_count") or 0
    if v == "ALIVE":
        return (0, -(s or 0), -ac, f["field"])
    if v == "WEAK":
        return (1, -(s or 0), -ac, f["field"])
    if s is not None and s >= 1.0:
        return (2, -s, -ac, f["field"])
    if s is not None:
        return (3, -s, -ac, f["field"])
    return (4, -ac, -(_cov(f.get("coverage")) or 0), f["field"])


def failed_checks(rec: Dict[str, Any]) -> List[str]:
    value = _unpack(rec.get("ra_failed_checks"), [])
    return [str(x) for x in value] if isinstance(value, list) else []


# ── 文档渲染 ────────────────────────────────────────────────────────────
def _related_links(ds: str, meta: Dict[str, Any], docs_dir: Path) -> List[str]:
    links: List[str] = []
    cat = (meta.get("category") or "").lower()
    candidates: List[Tuple[str, str]] = []
    if cat in _CATEGORY_DOCS:
        candidates.append(_CATEGORY_DOCS[cat])
    if ds.startswith("pv") or ds in {"continuation_score", "intraday_pv_feats", "pattern_scores"}:
        candidates.append(_CATEGORY_DOCS["pv"])
    if ds.startswith("insider"):
        candidates.append(_CATEGORY_DOCS["insiders"])
    if ds in {"fund_holdings_panel", "institutions6"}:
        candidates.append(_CATEGORY_DOCS["insights"])
    if ds == "risk60":
        candidates.append(_CATEGORY_DOCS["risk"])
    if ds == "euro_equity_imbalance":
        candidates.append(("imbalance_field_profile_20261020.md", "EUR 股权失衡字段画像"))
    if cat == "analyst":
        candidates.append(("analyst_campaign_20261013.md", "Analyst 战役记录"))
    candidates.extend([
        ("eur_full_field_profile_20261013.md", "EUR 全量字段画像（2026-10-13）"),
        ("mining_experience_by_category.md", "按类别的挖掘经验"),
    ])
    seen = set()
    for filename, label in candidates:
        if filename in seen:
            continue
        seen.add(filename)
        if (docs_dir / filename).exists():
            links.append(f"- [{label}](../{filename})")
    usage = docs_dir.parent / "field_profile_usage_guide.md"
    if usage.exists():
        links.append("- [字段画像使用指南（7 步漏斗与证据等级）](../../field_profile_usage_guide.md)")
    links.append("- [返回数据集画像索引](README.md)")
    return links


def render_doc(ds: str, fields: List[Dict[str, Any]], meta: Dict[str, Any],
               cells: Sequence[str], snapshots: Sequence[str],
               overrides: Optional[Dict[str, Any]],
               ranking: Optional[Dict[str, Any]], backtests: Sequence[Dict[str, Any]],
               dead_ends: Sequence[Dict[str, Any]], docs_dir: Path,
               as_of: str, list_limit: int) -> str:
    # 区域名：meta 恒带 _region（main() 逐集注入）；兜底用「本区」，
    # **不要把 EUR 写死进模板**——本工具对任意区域通用（2026-10-20）。
    region = str(meta.get("_region") or "本区")
    total = len(fields)
    signals = [f for f in fields if f.get("verdict") in SIGNAL_VERDICTS]
    signals.sort(key=lambda f: (-(f.get("best_s_sg") or 0), f["field"]))
    tested = [f for f in fields if (f.get("n_tests") or 0) > 0]
    near = [f for f in tested if f.get("verdict") not in SIGNAL_VERDICTS
            and f.get("best_s_sg") is not None]
    near.sort(key=lambda f: -(f["best_s_sg"] or 0))

    types = collections.Counter(f.get("type") or "UNKNOWN" for f in fields)
    buckets = collections.Counter(coverage_bucket(_cov(f.get("coverage"))) for f in fields)
    sems = collections.Counter(f.get("sem_type") or "unknown" for f in fields)
    fam_stats: Dict[str, Dict[str, Any]] = {}
    for f in fields:
        fam = f.get("family") or family_of(f["field"])
        st = fam_stats.setdefault(fam, {"n": 0, "sig": 0, "best": None, "sample": f["field"]})
        st["n"] += 1
        if f.get("verdict") in SIGNAL_VERDICTS:
            st["sig"] += 1
        s = f.get("best_s_sg")
        if s is not None and (st["best"] is None or s > st["best"]):
            st["best"] = s

    cov_values = [_cov(f.get("coverage")) for f in fields]
    cov_values = [c for c in cov_values if c is not None]
    avg_cov = sum(cov_values) / len(cov_values) if cov_values else None

    lines: List[str] = [BEGIN, ""]
    lines.append(
        f"> 机器生成段：`tools/fields/dataset_profile_doc.py`（只读 `data/wqb.db`）｜快照日 {as_of}｜"
        f"字段 {total} 个")
    lines.append(
        "> 画像口径：`field_profile_perf` 的历史实测（不同设置档混采，**不是复现保证**）；"
        "`ALIVE` 只代表该字段历史测出过 S≥闸线，**不代表可提交**。")
    lines.append("")

    # 一、数据集定位
    lines += ["## 一、数据集定位", "", "| 项 | 值 |", "|---|---|"]
    lines.append(f"| 数据集 | `{_cell(ds)}` |")
    lines.append(f"| 平台类别 | {_cell(meta.get('category'))} |")
    lines.append(f"| 战役 cell | {_cell(', '.join(cells) if cells else None)} |")
    if overrides:
        bt = overrides.get("backtest") or {}
        settings = bt.get("overrides") or {}
        summary = ", ".join(f"{k}={v}" for k, v in settings.items()) or "—"
        lines.append(f"| 战役设置覆盖 | `{_cell(summary)}`（来源 cell {_cell(overrides.get('cell'))}） |")
        if overrides.get("note"):
            lines.append(f"| 战役备注 | {_trunc(overrides.get('note'), 220)} |")
    lines.append(f"| 本地字段数 | {total} |")
    lines.append(f"| 平台字段数 | {_cell(meta.get('platform_field_count'))} |")
    lines.append(f"| 数据集覆盖率 | {_pct(meta.get('coverage'))}（字段均值 {_pct(avg_cov)}） |")
    lines.append(f"| 平台 alpha 数（入库时） | {_cell(meta.get('alpha_count'))} |")
    lines.append(f"| delay | {_cell(meta.get('delay'))} |")
    lines.append(f"| 排序分 / tier | {_num((ranking or {}).get('score'), 2)} / {_cell((ranking or {}).get('tier'))} |")
    lines.append(f"| 本地已完成回测 | {len(backtests)} 条 |")
    lines.append(f"| 快照来源 | {_cell(', '.join(snapshots) if snapshots else None)} |")
    lines.append(f"| 数据集元数据更新 | {_cell(meta.get('updated_at'))} |")
    lines.append("")

    # 二、字段结构总览
    lines += ["## 二、字段结构总览", "", "### 类型与覆盖", "",
              "| 维度 | 分布 |", "|---|---|"]
    lines.append("| 类型 | " + " ｜ ".join(
        f"{k} {v}（{_pct(v / total if total else 0)}）" for k, v in types.most_common()) + " |")
    bucket_order = ["0 覆盖", "(0, 0.3)", "[0.3, 0.6)", "[0.6, 0.9)", "[0.9, 1.0]", "未知"]
    lines.append("| 覆盖率 | " + " ｜ ".join(
        f"{k} {buckets.get(k, 0)}" for k in bucket_order if buckets.get(k)) + " |")
    lines.append("")

    multi_fams = [(fam, st) for fam, st in fam_stats.items() if st["n"] >= 2]
    multi_fams.sort(key=lambda kv: (-kv[1]["n"], -(kv[1]["best"] or 0), kv[0]))
    lines += ["### 命名族（字段数 ≥ 2，Top 12）", ""]
    if multi_fams:
        lines += ["| 命名族 | 字段数 | ALIVE/WEAK | 最高 S(sg) | 示例字段 |",
                  "|---|---:|---:|---:|---|"]
        for fam, st in multi_fams[:12]:
            lines.append(f"| `{_cell(fam)}` | {st['n']} | {st['sig']} | "
                         f"{_num(st['best'])} | `{_cell(st['sample'])}` |")
    else:
        lines.append(f"字段命名高度分散：{total} 个字段落在 {len(fam_stats)} 个命名族，"
                     "**没有多字段族**，本表从略。逐字段见第四节。")
    lines.append("")

    # 三、实测信号
    lines += ["## 三、实测信号字段", ""]
    if signals:
        lines += [f"**ALIVE / WEAK 共 {len(signals)} 个**（按 S(sg) 降序）。", "",
                  "| 字段 | 类型 | 覆盖 | 语义类型 | verdict | S(sg) | 2Y(sg) | sub(sg) | TO 中位 | n_sg | 描述 |",
                  "|---|---|---:|---|---|---:|---:|---:|---:|---:|---|"]
        for f in signals:
            lines.append(
                f"| `{_cell(f['field'])}` | {_cell(f.get('type'))} | {_pct(_cov(f.get('coverage')))} | "
                f"{_cell(f.get('sem_type'))} | **{_cell(f.get('verdict'))}** | "
                f"{_num(f.get('best_s_sg'))} | {_num(f.get('best_2y_sg'))} | "
                f"{_num(f.get('best_sub_sg'))} | {_num(f.get('to_med'), 3)} | "
                f"{_cell(f.get('n_sg'))} | {_trunc(f.get('description'), 120)} |")
        lines.append("")
    else:
        lines += ["本数据集在 `field_profile_perf` 中**没有 ALIVE/WEAK 字段**。", ""]

    if near:
        top_near = near[:5]
        lines += ["### 最接近闸线的已测字段（Top 5）", "",
                  "| 字段 | 覆盖 | verdict | best S(sg) | 2Y(sg) | n_sg |",
                  "|---|---:|---|---:|---:|---:|"]
        for f in top_near:
            lines.append(
                f"| `{_cell(f['field'])}` | {_pct(_cov(f.get('coverage')))} | {_cell(f.get('verdict'))} | "
                f"{_num(f.get('best_s_sg'))} | {_num(f.get('best_2y_sg'))} | {_cell(f.get('n_sg'))} |")
        lines.append("")

    # 四、字段清单
    lines += ["## 四、字段清单", ""]
    ordered = sorted(fields, key=field_priority)
    shown = ordered if total <= 80 else ordered[:list_limit]
    if total > 80:
        lines += [f"共 **{total}** 个字段，下表按「ALIVE/WEAK → 近闸已测（S≥1.0）→ 其他已测 → "
                  f"未测（平台使用度 → 覆盖率）」取前 **{len(shown)}** 个。"
                  f"全量清单查 `field_profile_perf`：`WHERE region='{region}' "
                  f"AND dataset='{ds}'`。", ""]
    else:
        lines += [f"共 **{total}** 个字段（全量）。", ""]
    lines += ["| 字段 | 类型 | 覆盖 | 平台 alpha | 语义类型 | verdict | S(sg) | 2Y(sg) | 描述 |",
              "|---|---|---:|---:|---|---|---:|---:|---|"]
    for f in shown:
        lines.append(
            f"| `{_cell(f['field'])}` | {_cell(f.get('type'))} | {_pct(_cov(f.get('coverage')))} | "
            f"{_cell(f.get('alpha_count'))} | {_cell(f.get('sem_type'))} | {_cell(f.get('verdict'))} | "
            f"{_num(f.get('best_s_sg'))} | {_num(f.get('best_2y_sg'))} | "
            f"{_trunc(f.get('description'), 70)} |")
    lines.append("")

    # 五、本地回测证据
    lines += ["## 五、本地回测证据", ""]
    if backtests:
        waves = sorted({str(r["wave"]) for r in backtests if r.get("wave") is not None})
        best_s = max((r for r in backtests if r.get("sharpe") is not None),
                     key=lambda r: r["sharpe"], default=None)
        best_2y = max((r for r in backtests if r.get("two_year") is not None),
                      key=lambda r: r["two_year"], default=None)
        best_sub = max((r for r in backtests if r.get("sub") is not None),
                       key=lambda r: r["sub"], default=None)
        fc = collections.Counter(c for r in backtests for c in failed_checks(r))
        lines += [
            f"- 已完成回测 **{len(backtests)}** 条，涉及波次：{_cell(', '.join(waves))}",
            f"- 最高 S：**{_num(best_s and best_s['sharpe'])}**"
            f"（`{_cell(best_s and best_s['alpha_id'])}`）"
            f"｜最高 2Y：**{_num(best_2y and best_2y['two_year'])}**"
            f"｜最高 sub：**{_num(best_sub and best_sub['sub'])}**",
            f"- RA 失败项分布：{_cell(' ｜ '.join(f'{k} {v}' for k, v in fc.most_common(10)) if fc else '无（全部 RA 项通过）')}",
            "",
            "### Top 8（按 Sharpe）", "",
            "| alpha | wave | S | Fitness | TO | 2Y | sub | RA 失败项 | 入库日期 |",
            "|---|---|---:|---:|---:|---:|---:|---|---|",
        ]
        for r in [x for x in backtests if x.get("sharpe") is not None][:8]:
            lines.append(
                f"| `{_cell(r['alpha_id'])}` | {_cell(r.get('wave'))} | {_num(r.get('sharpe'))} | "
                f"{_num(r.get('fitness'))} | {_num(r.get('turnover'), 3)} | {_num(r.get('two_year'))} | "
                f"{_num(r.get('sub'))} | {_cell(', '.join(failed_checks(r)) or '—')} | "
                f"{_cell(str(r.get('created_at') or '')[:10])} |")
        lines.append("")
    else:
        msg = f"本数据集在 {region} 尚无已完成的本地回测记录"
        if tested:
            msg += "；第三节的字段 verdict 来自历史平台实测（`field_profile_perf`）"
        else:
            msg += "；`field_profile_perf` 也没有该集字段的实测记录，本页只有结构信息"
        lines += [msg + "。", ""]

    # 六、判死记录
    lines += ["## 六、判死记录（sealed dead_end）", ""]
    if dead_ends:
        attr_label = {"payload": "字段", "inferred": "推断", "region": "区域"}
        lines += ["| entry_id | 归属 | 规则 | wave | dead_at |", "|---|---|---|---|---|"]
        for e in dead_ends:
            lines.append(f"| `{_cell(e['entry_id'])}` | {attr_label.get(e.get('attribution'), '—')} | "
                         f"{_trunc(e.get('rule') or e.get('family'), 180)} | "
                         f"{_cell(e.get('wave'))} | {_cell(e.get('dead_at'))} |")
        lines += ["", "以上是**历史封存记录**；若后续档案或新实测已翻案，以最新证据为准（判死不等于永久禁令）。", ""]
    else:
        lines += ["无针对本数据集的 `dead_end` 记录。", ""]

    # 七、机制映射
    lines += ["## 七、机制映射（description → 骨架建议）", ""]
    lines += ["| 语义类型 | 字段数 | 建议骨架 |", "|---|---:|---|"]
    for sem, n in sems.most_common(8):
        hint = SKELETON_HINT.get(sem, "")
        if sem == "unknown":
            hint = "描述未命中现有规则：人工判量型后再选骨架（勿按名字拍）"
        lines.append(f"| `{_cell(sem)}` | {n} | {_cell(hint)} |")
    lines.append("")
    conflicts = [f for f in signals if f.get("sem_conflict")]
    if conflicts:
        lines += ["### 名字/描述语义冲突的信号字段（名字会骗人）", "",
                  "| 字段 | 名字像 | 实为（description） | 描述证据 |", "|---|---|---|---|"]
        for f in conflicts:
            lines.append(f"| `{_cell(f['field'])}` | {_cell(f.get('name_guess'))} | "
                         f"{_cell(f.get('sem_type'))} | {_trunc(f.get('sem_evidence'), 120)} |")
        lines.append("")

    # 八、可用性与边界
    lines += ["## 八、可用性与边界", ""]
    bullets: List[str] = []
    if meta.get("coverage") is not None and (norm_cov(meta["coverage"]) or 0) < 0.6:
        bullets.append(f"覆盖率 {_pct(meta.get('coverage'))} < 0.6：可挖面偏小，先确认目标宇宙的字段覆盖再发批。")
    n_vector = types.get("VECTOR", 0)
    n_group = types.get("GROUP", 0)
    if n_vector:
        bullets.append(f"含 **{n_vector} 个 VECTOR** 字段：必须先用 `vec_*` 聚合，裸用会被平台拒绝。")
    if n_group:
        bullets.append(f"含 **{n_group} 个 GROUP** 字段：只能作分组轴（`group_*`），不能直接当信号。")
    if signals:
        low_sample = [f for f in signals if (f.get("n_sg") or 0) <= 3]
        if low_sample:
            bullets.append(f"{len(low_sample)} 个信号字段的 `n_sg ≤ 3`：S 只能当下界，需补实测再定论。")
        bullets.append("`ALIVE/WEAK` 是**字段级**历史结论；提交前必须回测 `prod` / `self` 两端点。")
    if not cells and not snapshots and not backtests:
        bullets.append(f"该数据集**未进 {region} cells / 快照 / 本地回测**："
                       "本页仅由平台字段目录生成，本区尚未评估。")
    if not backtests:
        bullets.append("本区尚无本地回测：画像为历史实测，**不是复现证明**，首轮必须用探针批验证。")
    if overrides:
        bullets.append("本数据集有**战役设置覆盖**（见 §一）：发批须以 `tracking/<REGION>/config/cells.json` 为准，"
                       "勿套区域缺省设置。")
    if fields and not any((f.get("n_tests") or 0) > 0 for f in fields):
        bullets.append("`field_profile_perf` 里**没有任何字段被实测过**；本页 verdict 只反映覆盖率/类型门槛"
                       "（UNUSABLE/AXIS_ONLY/UNTESTED），不代表信号强弱。")
    bullets.append("`field_profile_perf` 混合了不同设置档（中性化 / universe / decay），同一字段换档后可能不复现。")
    if conflicts:
        bullets.append("字段语义一律以 `description` 为准；名字会骗人的冲突项已列在 §七。")
    else:
        bullets.append("字段语义一律以 `description` 为准，名字只作对照。")
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")

    # 九、关联档案
    lines += ["## 九、关联档案", ""] + _related_links(ds, meta, docs_dir) + [""]

    lines += [
        "---",
        f"*生成：`python tools/fields/dataset_profile_doc.py --region {region} "
        f"--dataset {ds} --apply` ｜ 快照日 {as_of}*",
        END,
    ]
    return "\n".join(lines) + "\n"


def render_readme(region: str, data: Dict[str, Any],
                  cells: Dict[str, List[str]], snapshots: Dict[str, List[str]],
                  rankings: Dict[str, Dict[str, Any]], docs_dir: Path,
                  out_dir: Path, as_of: str) -> str:
    datasets = data["datasets"]
    fields = data["fields"]
    profiles = data["profiles"]
    backtests = data["backtests"]
    active = set(cells) | set(snapshots) | set(backtests)
    # 索引覆盖「本目录实际存在的画像」，而不是本次生成范围：
    # `--dataset` / `--active-only` 局部刷新时不能把总索引缩成一行。
    available = [ds for ds, flds in fields.items()
                 if flds and (out_dir / f"{_safe_name(ds)}_field_profile.md").exists()]
    rows_scope = sorted(set(available))
    n_catalogued = sum(1 for flds in fields.values() if flds)
    rows = []
    for ds in rows_scope:
        flds = fields.get(ds) or []
        prof = [profiles[(ds, f["field"])] for f in flds if (ds, f["field"]) in profiles]
        alive = sum(1 for p in prof if p["verdict"] == "ALIVE")
        weak = sum(1 for p in prof if p["verdict"] == "WEAK")
        tested = sum(1 for p in prof if (p["n_tests"] or 0) > 0)
        meta = datasets.get(ds, {})
        rk = rankings.get(ds) or {}
        evidence = []
        if cells.get(ds):
            evidence.append("cell")
        if snapshots.get(ds):
            evidence.append("快照")
        if backtests.get(ds):
            evidence.append("回测")
        rows.append({
            "ds": ds, "cat": meta.get("category") or "—", "cells": ", ".join(cells.get(ds, [])) or "—",
            "evidence": "+".join(evidence) or "—",
            "n": len(flds), "cov": meta.get("coverage"), "alpha": meta.get("alpha_count"),
            "tested": tested, "alive": alive, "weak": weak,
            "bt": len(backtests.get(ds, [])), "tier": rk.get("tier") or "—",
            "file": f"{_safe_name(ds)}_field_profile.md",
        })
    rows.sort(key=lambda r: (r["cat"], r["ds"]))
    n_active = sum(1 for r in rows if r["ds"] in active)

    lines = [
        README_BEGIN, "",
        f"# {region} 数据集字段画像索引", "",
        f"> 机器生成：`tools/fields/dataset_profile_doc.py`｜快照日 {as_of}｜"
        f"本目录已有画像 **{len(rows)}** 个（平台有字段目录共 {n_catalogued} 个）；其中 **{n_active}** 个有 {region} "
        f"活动痕迹（cells / 快照 / 本地回测），其余为仅有平台字段目录的待评估集。",
        "> 每个数据集一份 `<dataset>_field_profile.md`；机器段刷新不会覆盖 `## 人工机制复盘`。",
        "> 口径提醒：`field_profile_perf` 是历史实测混采，**ALIVE ≠ 可提交**；"
        "`画像已测` = 该集字段在 `field_profile_perf` 里 `n_tests>0` 的个数（与「本地回测」列无关）；"
        f"`{region} 证据` 列为 `—` 的集尚未在 {region} 侧评估过。",
        "",
        "## 一、索引表", "",
        f"| 数据集 | 平台类别 | 战役 cell | tier | {region} 证据 | 字段数 | 覆盖 | 平台 alpha | 画像已测 | ALIVE | WEAK | 本地回测 | 文档 |",
        "|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| `{_cell(r['ds'])}` | {_cell(r['cat'])} | {_cell(r['cells'])} | {_cell(r['tier'])} | "
            f"{_cell(r['evidence'])} | "
            f"{r['n']} | {_pct(r['cov'])} | {_cell(r['alpha'])} | {r['tested']} | "
            f"{r['alive']} | {r['weak']} | {r['bt']} | [{r['file']}]({r['file']}) |")
    lines.append("")

    lines += ["## 二、无数据集归属的区域级判死记录", ""]
    region_dead = data.get("region_dead") or []
    if region_dead:
        lines += ["| entry_id | 摘要 | dead_at |", "|---|---|---|"]
        for e in region_dead:
            lines.append(f"| `{_cell(e['entry_id'])}` | {_trunc(e.get('rule') or e.get('family'), 160)} | "
                         f"{_cell(e.get('dead_at'))} |")
        lines.append("")
    else:
        lines += ["无。", ""]

    lines += [
        "## 三、刷新方式", "",
        "```bash",
        f"# 全量刷新（全部有字段目录的数据集）",
        f"./world-quant-brain-mcp/.venv/Scripts/python.exe tools/fields/dataset_profile_doc.py "
        f"--region {region} --apply",
        "",
        f"# 只刷新有 {region} 活动痕迹的集（cells ∪ 快照 ∪ 本地回测）",
        f"./world-quant-brain-mcp/.venv/Scripts/python.exe tools/fields/dataset_profile_doc.py "
        f"--region {region} --active-only --apply",
        "",
        "# 单个数据集",
        f"./world-quant-brain-mcp/.venv/Scripts/python.exe tools/fields/dataset_profile_doc.py "
        f"--region {region} --dataset analyst7 --apply",
        "",
        "# 预览（默认 dry-run）",
        f"./world-quant-brain-mcp/.venv/Scripts/python.exe tools/fields/dataset_profile_doc.py --region {region}",
        "```",
        "",
        "## 四、按类别的画像档案", "",
        "> 类目级汇总（跨数据集）。单个数据集的逐字段清单以本目录各自的 `<dataset>_field_profile.md` 为准。",
        "",
    ]
    category_docs = [
        ("pv_field_profile_20261019.md", "PV 类字段画像与回测档案"),
        ("insiders_field_profile_20261020.md", "Insiders 类字段画像"),
        ("institutions_field_profile_20261020.md", "Institutions 类字段画像"),
        ("imbalance_field_profile_20261020.md", "股权失衡（euro_equity_imbalance）字段画像"),
        ("short_interest_risk60_profile_20261020.md", "risk60 证券借贷画像"),
        ("eur_analyst_field_profile_20261018.md", "Analyst 类字段画像（2026-10-18）"),
        ("eur_analyst_field_profile_20261017.md", "Analyst 类字段画像（2026-10-17）"),
    ]
    shown_cat = False
    for filename, label in category_docs:
        if (docs_dir / filename).exists():
            lines.append(f"- [{label}](../{filename})")
            shown_cat = True
    if not shown_cat:
        lines.append("（暂无类目级档案）")
    lines += ["", "## 五、跨数据集入口", ""]
    cross = [
        ("eur_full_field_profile_20261013.md", "EUR 全量字段画像（2026-10-13）"),
        ("dataset_field_profiles_20261013.md", "数据集字段画像汇总（2026-10-13）"),
        ("mining_experience_by_category.md", "按类别的挖掘经验"),
        ("operator_template_ledger.md", "算子模板台账"),
    ]
    for filename, label in cross:
        if (docs_dir / filename).exists():
            lines.append(f"- [{label}](../{filename})")
    usage = docs_dir.parent / "field_profile_usage_guide.md"
    if usage.exists():
        lines.append("- [字段画像使用指南（7 步漏斗与证据等级）](../../field_profile_usage_guide.md)")
    lines += ["", README_END, ""]
    return "\n".join(lines)


# ── 写入 ────────────────────────────────────────────────────────────────
def write_marked(path: Path, block: str, title: str, human_note: str,
                 force: bool) -> str:
    """只替换标记段；返回动作（created / updated / appended / unchanged / skipped）。"""
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    if previous is None:
        content = f"# {title}\n\n{block}\n## 人工机制复盘\n\n{human_note}\n"
        action = "created"
    elif BEGIN in previous and END in previous:
        start, stop = previous.index(BEGIN), previous.index(END) + len(END)
        if stop <= start:
            raise ValueError(f"标记块边界损坏：{path}")
        content = previous[:start] + block.rstrip() + previous[stop:]
        action = "updated"
    elif BEGIN in previous or END in previous:
        raise ValueError(f"标记不完整，保留原文件：{path}")
    elif force:
        content = previous.rstrip() + "\n\n" + block + "\n"
        action = "appended"
    else:
        return "skipped"
    if content == previous:
        return "unchanged"
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix="." + path.name, suffix=".tmp",
                                     delete=False) as fp:
        fp.write(content)
        tmp = Path(fp.name)
    try:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != previous:
            raise RuntimeError(f"文档被另一写入者修改，请重新读取再刷新：{path}")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    return action


def write_plain(path: Path, content: str, force: bool) -> str:
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    if previous is not None and previous == content:
        return "unchanged"
    if previous is not None and README_BEGIN not in previous and not force:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix="." + path.name, suffix=".tmp",
                                     delete=False) as fp:
        fp.write(content)
        tmp = Path(fp.name)
    try:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != previous:
            raise RuntimeError(f"文档被另一写入者修改，请重新读取再刷新：{path}")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    return "updated" if previous is not None else "created"


# ── 主流程 ──────────────────────────────────────────────────────────────
def build_scope(args: argparse.Namespace, data: Dict[str, Any],
                cells: Dict[str, List[str]], snapshots: Dict[str, List[str]]) -> List[str]:
    names = set(data["datasets"])
    if args.dataset:
        wanted = [x.strip() for x in re.split(r"[,\s]+", args.dataset) if x.strip()]
        unknown = [x for x in wanted if x not in names]
        if unknown:
            raise SystemExit(f"[error] 数据集不存在：{', '.join(unknown)}")
        return sorted(set(wanted))
    if args.active_only:
        scope = set(cells) | set(snapshots) | set(data["backtests"])
        return sorted(ds for ds in scope if ds in names and data["fields"].get(ds))
    return sorted(ds for ds, flds in data["fields"].items() if flds)


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="按数据集生成字段画像文档（只读 DB；机器段可刷新，人工段保留）")
    ap.add_argument("--region", default="EUR")
    ap.add_argument("--db", help="库路径（缺省 <repo>/data/wqb.db；测试 / 沙箱隔离用）")
    ap.add_argument("--dataset", help="逗号分隔；省略则按默认范围")
    ap.add_argument("--active-only", action="store_true",
                    help="只覆盖有本区活动痕迹的集（cells ∪ 快照 ∪ 已回测；默认全部有字段目录的集）")
    ap.add_argument("--out-dir", help="缺省 docs/reference/<REGION>/datasets")
    ap.add_argument("--limit", type=int, default=50, help="字段总数 >80 时的表格行数（缺省 50）")
    ap.add_argument("--as-of", default=date.today().isoformat(), help="快照日（写入文档，缺省今天）")
    ap.add_argument("--apply", action="store_true", help="落盘；缺省 dry-run")
    ap.add_argument("--force", action="store_true",
                    help="允许向「无标记的既有文件」追加机器段 / 覆盖 README")
    ap.add_argument("--list", action="store_true", help="只列范围，不渲染")
    args = ap.parse_args(argv)

    region = args.region.upper()
    db_path = Path(args.db).expanduser().resolve() if args.db else _REPO / "data" / "wqb.db"
    if not db_path.exists():
        raise SystemExit(f"[error] 找不到 {db_path}")
    docs_dir = _REPO / "docs" / "reference" / region
    out_dir = Path(args.out_dir) if args.out_dir else docs_dir / "datasets"
    ref_dir = _REPO / "tracking" / region / "reference"

    data = load_db(db_path, region)
    for ds, rows in data["fields"].items():
        for f in rows:
            f["_dataset"] = ds
        attach_profiles(rows, data["profiles"])
        classify_fields(rows)

    snapshots = load_snapshots(ref_dir, data["datasets"])
    cells, overrides = load_cells(
        _REPO / "tracking" / region / "config" / "cells.json", data["datasets"])
    rankings = load_ranking(ref_dir / f"{region.lower()}_dataset_ranking.json")
    scope = build_scope(args, data, cells, snapshots)

    print(f"[scope] {region} → {len(scope)} 个数据集"
          f"（cells {len(cells)} / 快照 {len(snapshots)} / 本地回测 {len(data['backtests'])}）")
    if args.list:
        for ds in scope:
            print(f"  {ds:<32} fields={len(data['fields'].get(ds) or [])} "
                  f"bt={len(data['backtests'].get(ds) or [])}")
        return 0

    actions = collections.Counter()
    for ds in scope:
        flds = data["fields"].get(ds) or []
        meta = dict(data["datasets"].get(ds) or {})
        meta["_region"] = region
        block = render_doc(ds, flds, meta, cells.get(ds, []), snapshots.get(ds, []),
                           overrides.get(ds), rankings.get(ds), data["backtests"].get(ds, []),
                           data["dead_by_ds"].get(ds, []), out_dir.parent, args.as_of, args.limit)
        path = out_dir / f"{_safe_name(ds)}_field_profile.md"
        if not args.apply:
            actions["planned"] += 1
            try:
                shown = path.relative_to(_REPO)
            except ValueError:          # --out-dir 在仓库外（沙箱 / 临时目录）时照实打印
                shown = path
            print(f"  [plan] {shown} ({len(flds)} fields)")
            continue
        action = write_marked(
            path, block, f"{region} × {ds} 字段画像",
            "在此写字段语义、机制假设、已验证/已否证路径与下一步；机器段刷新不会覆盖本段。",
            force=args.force)
        actions[action] += 1
        if action == "skipped":
            print(f"  [skip] {path} 无标记且未加 --force，保持原样", file=sys.stderr)

    readme = render_readme(region, data, cells, snapshots, rankings,
                           out_dir.parent, out_dir, args.as_of)
    readme_path = out_dir / "README.md"
    if args.apply:
        actions[write_plain(readme_path, readme, args.force)] += 1
        print(f"[done] {region}: " + "  ".join(f"{k}={v}" for k, v in sorted(actions.items())))
        print(f"[out]  {out_dir}")
    else:
        print(f"[dry-run] 将写入 {len(scope)} 份文档 + README 到 {out_dir}；"
              f"加 --apply 落盘")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
