#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全量覆盖闸（EUR 2026-10-20 起，反探针模式）。

三道闸一次过：
  1) 字段全量覆盖闸：本波表达式用到的字段必须覆盖该数据集 100%（或 --coverage 指定阈值）。
  2) 模板族全量闸：本数据集历史已试跑 ≥ --min-families 个模板族。
  3) 边界算子穷举闸：表达式里出现的每个算子，参数必须落在 legal_values/legal_axes 内；
     近闸候选（有 --near-gate 标记）必须已试完 min_coverage 档。

与 tools/wave_gate.py 的关系：
  wave_gate.py     —— 单条表达式静态语法/闸 1–5 校验（现有 fail-closed 硬闸）
  本脚本             —— 覆盖层面的**前置**闸：候选批组装后、送 wave_gate 之前先跑本脚本，
                        确认"字段够全 / 族够多 / 边界够细"，避免探针式挖矿通过 wave_gate
                        但整个数据集仍没扫完。
  串联方式（两条并存）：
    ① 直调：候选批 → 本脚本（--gate-mode enforce）→ wave_gate.py。判死前必查走这条。
    ② 内置（2026-10-20 P0-1 接线）：wave_gate.py 数据驱动接入本模块 —— 战役目录存在
       `reference/boundary_ops_<region>.json` 即启用（无区域字面量分支），enforce 档
       FAIL 计入 all_pass（exit 1）。模式 = wave_gate `--fcov-mode` > `WQB_FCOV_MODE`
       > 随 region_gates 按日缺省；显式降级需要 waiver（waiver_full_coverage_<region>_<wave>）。

口径（2026-10-20 澄清）：
  闸 1「字段 100% 覆盖」= 该数据集**字段全集**内每个字段至少出现在 1 条候选表达式里
  （按批口径）。历史配方（如 analyst7 修订族实配约 128 字段）是既往成果、不是扫描证据——
  本闸守的是派发/判死前的完整性，不回判历史波；要放宽覆盖口径用 `--coverage <1.0`（政策杠杆）。
  字段全集解析顺序：--fields-list > 战役/仓库 reference 的 `{region}_{dataset}_fields.json`
  / `{dataset}_fields.json` > --all-fields > 本地 data/wqb.db（region 关联、只读；库不可用
  或该数据集无行时按「无字段全集」退出码 2）。
  闸 2 的族历史 = 文件系统 ∪ DB `expressions.family`（GEM 落库的模板族，与
  template_families.json 同一范畴；wave_results / gate_results 里的 "family" 是另两套
  词表——库存信号族 / 结构族，不得混入）。

用法:
  python tools/full_coverage_gate.py --region EUR --dataset model238 \\
      --candidates tracking/EUR/candidates/wave_XXX.json --campaign-dir tracking/EUR

  python tools/full_coverage_gate.py --region EUR --dataset model238 \\
      --exprs-file candidates/w98.txt --campaign-dir tracking/EUR --gate-mode enforce

  python tools/full_coverage_gate.py --region EUR --dataset model238 \\
      --expr "rank(ts_mean(x,252))" --mode off

退出码:
  0 = PASS（或 warn 模式下即使有 WARN）
  1 = FAIL（enforce 模式且有任一闸 FAIL）
  2 = ERROR（配置/输入问题）
运行环境: 与 wave_gate.py 一致，Python 3.10+；纯标准库实现，仅字段全集 DB 回退
  经 `src/wqb/db_conn.py`（全库唯一连接工厂，`readonly=True` 字节级只读）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据字段/算子/保留字（与 tools/field_inspect_gate.py 保持同源，避免漂移）
_IDENT_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\b")
_CALL_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\s*\(")
_KWARG_RE = re.compile(r"\b([a-z_][a-z0-9_]*)\s*=")
_RESERVED = {
    "true", "false", "nan", "industry", "subindustry", "sector", "market",
    "country", "exchange", "and", "or", "not", "if", "else", "as",
}

# 从 wave 文件里抓 family 名的两种 pattern
_FAMILY_PATTERNS = [
    re.compile(r'"template_family"\s*:\s*"([^"]+)"'),
    re.compile(r'"family"\s*:\s*"([^"]+)"'),
    re.compile(r'"family_id"\s*:\s*"([^"]+)"'),
]
# 关键：JSON 可能被压缩（无空格），因此冒号两侧允许任意空白；\s* 已足够。


# --------------------------------------------------------------- candidates / fields


def load_expressions(args) -> List[str]:
    """从 --expr / --exprs-file / --candidates 三种入口取表达式。"""
    exprs: List[str] = []
    if args.expr:
        exprs.append(args.expr)
    if args.exprs_file:
        with open(args.exprs_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    exprs.append(line)
    if args.candidates:
        try:
            with open(args.candidates, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            sys.stderr.write(f"[fcg] candidates 读失败 {args.candidates}: {e}\n")
            sys.exit(2)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    exprs.append(item)
                elif isinstance(item, dict) and item.get("expr"):
                    exprs.append(item["expr"])
        elif isinstance(data, dict):
            for key in ("expressions", "exprs", "candidates"):
                if key in data:
                    for item in data[key]:
                        if isinstance(item, str):
                            exprs.append(item)
                        elif isinstance(item, dict) and item.get("expr"):
                            exprs.append(item["expr"])
    return exprs


def extract_ops(expr: str) -> Set[str]:
    ops: Set[str] = set()
    for m in _CALL_RE.finditer(expr):
        name = m.group(1)
        if name not in _RESERVED:
            ops.add(name)
    return ops


def extract_fields(expr: str) -> Set[str]:
    used_ops = extract_ops(expr)
    kwargs = {m.group(1) for m in _KWARG_RE.finditer(expr)}
    fields: Set[str] = set()
    for m in _IDENT_RE.finditer(expr):
        name = m.group(1)
        if name in used_ops or name in kwargs or name in _RESERVED:
            continue
        fields.add(name)
    return fields


def collect_expr_fields(exprs: Iterable[str]) -> Set[str]:
    all_fields: Set[str] = set()
    for expr in exprs:
        all_fields |= extract_fields(expr)
    return all_fields


# --------------------------------------------------------------- 字段全量覆盖闸


def _flatten_field_names(items: Iterable[Any]) -> Set[str]:
    """把字段列表规范化为名字集合：元素可以是字符串，或含 id/name/field_id 键的对象。"""
    names: Set[str] = set()
    for x in items:
        if isinstance(x, str):
            names.add(x)
        elif isinstance(x, dict):
            for key in ("id", "name", "field_id", "fieldName", "field"):
                v = x.get(key)
                if isinstance(v, str) and v:
                    names.add(v)
                    break
    return names


def _parse_fields_list_data(data: Any) -> Set[str]:
    """兼容三种形态：[str...]、[dict...]、{fields/field_names/data: [...] }。"""
    if isinstance(data, list):
        return _flatten_field_names(data)
    if isinstance(data, dict):
        for key in ("fields", "field_names", "data", "items"):
            v = data.get(key)
            if isinstance(v, list):
                return _flatten_field_names(v)
    return set()


def _default_db_path() -> str:
    """本地台账库缺省位（data/wqb.db；WQB_DB_PATH 可换——wave_gate 隔离与测试用）。"""
    return os.environ.get("WQB_DB_PATH") or os.path.join(_REPO_ROOT, "data", "wqb.db")


def _db_ro_connect(db_path: str):
    """只读连接：走 `wqb.db_conn.connect(readonly=True)`（全库唯一连接工厂）。

    2026-10-20 更正：原实现自建裸 sqlite3.connect，被
    `tests/unit/01_store_db/test_db_write_guards.py` 的静态闸拦下（白名单外禁裸连接）。
    `readonly=True` 以 `mode=ro` URI 打开并跳过 `PRAGMA journal_mode=WAL`——字节级只读，
    不碰库文件（WAL 是持久化库级属性）。
    """
    src = os.path.join(_REPO_ROOT, "src")
    if src not in sys.path:
        sys.path.insert(0, src)
    from wqb.db_conn import connect as _wqb_connect
    return _wqb_connect(db_path, readonly=True)


def load_db_field_universe(region: str, dataset: str,
                           db_path: Optional[str] = None) -> Tuple[Optional[Set[str]], str]:
    """从本地 catalog（data/wqb.db）取该区该数据集的字段全集（只读）。

    2026-10-20（P0-1）：字段目录 JSON 只覆盖部分数据集，DB 的 fields×datasets×regions
    是更强的事实源（EUR/analyst7 即只有 DB 侧有全集）。**必须带 region 作用域**——
    `fields` 表无 region 列，同名数据集最多在 13 个区各有一份（见 wqb.region_catalog
    的事故复盘），不带 region 会静默合并跨区字段。
    返回 (字段名集合 | None, 来源标注 | 失败原因)。
    """
    db = db_path or _default_db_path()
    if not os.path.isfile(db):
        return None, f"DB 不存在: {db}"
    try:
        conn = _db_ro_connect(db)
        try:
            rows = conn.execute(
                "SELECT f.field_name FROM fields f "
                "JOIN datasets d ON d.id=f.dataset_id "
                "JOIN regions r ON r.id=d.region_id "
                "WHERE upper(r.name)=? AND lower(d.name)=?",
                (str(region).strip().upper(), str(dataset).strip().lower()),
            ).fetchall()
        finally:
            conn.close()
    except Exception as e:
        return None, f"DB 读失败: {type(e).__name__}: {e}"
    names = {str(r[0]) for r in rows if r[0]}
    if not names:
        return None, f"DB 无 {str(region).upper()}/{dataset} 字段行"
    return names, f"db:{db}"


def resolve_field_source(args) -> Tuple[Optional[Set[str]], str]:
    """解析字段全集：--fields-list > 战役/仓库 reference 目录 > --all-fields > DB 回退。"""
    if args.fields_list:
        try:
            with open(args.fields_list, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            sys.stderr.write(f"[fcg] --fields-list 读失败 {args.fields_list}: {e}\n")
            sys.exit(2)
        fields = _parse_fields_list_data(data)
        if fields:
            return fields, args.fields_list
        sys.stderr.write(f"[fcg] --fields-list 结构不识别（无 id/name/field_id）：{args.fields_list}\n")
        sys.exit(2)

    if args.region:
        ref = Path(_REPO_ROOT) / "tracking" / args.region.upper() / "reference"
        candidates = [ref / f"{args.region.lower()}_{args.dataset}_fields.json",
                      ref / f"{args.dataset}_fields.json"]
        # 2026-10-20：战役目录先行（wave_gate 内置调用与临时战役测试都用得到；
        # 直调 CLI 因 campaign_dir 即 tracking/<REGION>，两条路等价）。
        campaign_dir = getattr(args, "campaign_dir", None)
        if campaign_dir:
            croot = Path(campaign_dir) / "reference"
            candidates = [croot / f"{args.region.lower()}_{args.dataset}_fields.json",
                          croot / f"{args.dataset}_fields.json"] + candidates
        for candidate in candidates:
            if not candidate.exists():
                continue
            try:
                with candidate.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                fields = _parse_fields_list_data(data)
                if fields:
                    return fields, str(candidate)
            except Exception:
                pass

    if args.all_fields:
        return set(args.all_fields.split(",")), "cli:--all-fields"

    # 2026-10-20（P0-1）：字段目录 JSON 缺席时回退本地 catalog（region 关联、只读）。
    if args.region:
        db_fields, db_note = load_db_field_universe(args.region, args.dataset,
                                                    db_path=getattr(args, "db_path", None))
        if db_fields:
            return db_fields, db_note
        if db_note:
            return None, f"未提供字段全集（DB 回退: {db_note}）"

    return None, "未提供字段全集"


def apply_field_gate(
    exprs: List[str],
    known_fields: Set[str],
    coverage: float,
    mode: str,
) -> Dict[str, Any]:
    used = collect_expr_fields(exprs)
    missing = sorted(known_fields - used)
    got = len(known_fields) - len(missing)
    total = len(known_fields)
    coverage_actual = got / total if total else 0.0
    required = total if coverage >= 1.0 else int(round(total * coverage))
    verdict = "PASS" if got >= required else "FAIL"
    if verdict == "FAIL" and mode == "warn":
        verdict = "WARN"
    return {
        "gate": "field_coverage",
        "verdict": verdict,
        "coverage": round(coverage_actual, 4),
        "required": round(coverage, 4),
        "total_fields": total,
        "covered": got,
        "missing_count": len(missing),
        "missing_sample": missing[:20],
        "expr_count": len(exprs),
    }


# --------------------------------------------------------------- 模板族全量闸


def load_wave_history(campaign_dir: str) -> Dict[str, List[str]]:
    """扫 campaign_dir 里的候选/wave 文件，按 dataset 聚合已用的模板族。"""
    family_by_ds: Dict[str, List[str]] = {}
    root = Path(campaign_dir)
    for folder in ("candidates", "cache", "tracking"):
        d = root / folder
        if not d.exists():
            continue
        for fn in d.iterdir():
            if not (fn.suffix == ".json" or fn.suffix == ".txt"):
                continue
            try:
                text = fn.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for m in _FAMILY_PATTERNS:
                for fam in m.findall(text):
                    # 2026-10-20 修补：原逻辑 ds=split("_")[0] 对含下划线的数据集名
                    # （如 insider_agg_matrix）永远截成 "insider"，导致族闸查不到。
                    # 改为同时按「全 stem」与「首 token」两个键登记（加法式，保留原行为）。
                    ds_head = fn.stem.split("_")[0] if "_" in fn.stem else fn.stem
                    for ds in (fn.stem, ds_head):
                        family_by_ds.setdefault(ds, [])
                        if fam not in family_by_ds[ds]:
                            family_by_ds[ds].append(fam)
    return family_by_ds


def load_db_families(region: str, dataset: str, db_path: Optional[str] = None) -> List[str]:
    """从本地库 `expressions.family` 取该区该数据集历史已试模板族（去重排序）。

    2026-10-20（P0-1）：族历史此前只扫战役目录文件（candidates/cache/tracking），而战役
    产物已入库——DB-only 的新波（GEM skeleton 模式落库 family）永远查不到。只读
    `expressions.family`；**不得**混入 wave_results / gate_results 里的 "family"
    （另两套词表：库存信号族 / 结构族）。库不可用/无行时返回 []（与文件史取并集）。
    """
    db = db_path or _default_db_path()
    if not os.path.isfile(db):
        return []
    try:
        conn = _db_ro_connect(db)
        try:
            rows = conn.execute(
                "SELECT DISTINCT family FROM expressions "
                "WHERE upper(region)=? AND lower(dataset)=? "
                "AND family IS NOT NULL AND family != ''",
                (str(region).strip().upper(), str(dataset).strip().lower()),
            ).fetchall()
        finally:
            conn.close()
    except Exception:
        return []
    return sorted({str(r[0]) for r in rows if r[0]})


def apply_family_gate(
    campaign_dir: str,
    dataset: str,
    min_families: int,
    exprs: List[str],
    mode: str,
    db_families: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    history = load_wave_history(campaign_dir) if campaign_dir else {}
    used = set(history.get(dataset, []))
    used |= {str(f) for f in (db_families or []) if f}   # 2026-10-20：∪ DB expressions.family

    current_family: Optional[str] = None
    if args_family_hint := (os.environ.get("WQ_TEMPLATE_FAMILY") or "").strip():
        current_family = args_family_hint

    total = len(used | ({current_family} if current_family else set()))
    verdict = "PASS" if total >= min_families else "FAIL"
    if verdict == "FAIL" and mode == "warn":
        verdict = "WARN"
    return {
        "gate": "template_family",
        "verdict": verdict,
        "used_families": sorted(used),
        "db_families": sorted({str(f) for f in (db_families or []) if f}),
        "min_families": min_families,
        "total": total,
        "gap": max(0, min_families - total),
    }


# --------------------------------------------------------------- 边界算子闸


def load_boundary_config(args) -> Dict[str, Any]:
    if args.boundary_config:
        with open(args.boundary_config, "r", encoding="utf-8") as f:
            return json.load(f)
    default = (Path(_REPO_ROOT) / "tracking" / args.region.upper() / "reference"
               / f"boundary_ops_{args.region.lower()}.json")
    if default.exists():
        with default.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"operators": {}}


def _extract_numeric_args(expr: str) -> List[Tuple[str, float]]:
    """返回 [(op_name, numeric_value), ...]。

    扫描每一个 op(...) 调用段，按逗号切分参数、逐参数判"整段是否是数字"。
    同时识别 `key=value` 具名参数（如 `winsorize(f, std=2)`）：整段是
    `std=2` 时把 2 记为该 op 的数字参数（`key` 本身不是数字，可安全跳过）。
    （直接扫数字 token 会把 `mdl238_global_rank` 里的 238 当参数——故必须整段判）
    """
    num_re = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*$")
    kw_num_re = re.compile(r"^\s*[a-z_][a-z0-9_]*\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*$")
    call_re = re.compile(r"\b([a-z_][a-z0-9_]*)\s*\(([^()]*)\)")
    out: List[Tuple[str, float]] = []
    for m in call_re.finditer(expr):
        op = m.group(1)
        args = m.group(2)
        for piece in args.split(","):
            mm = num_re.match(piece)
            if mm:
                out.append((op, float(mm.group(1))))
                continue
            km = kw_num_re.match(piece)
            if km:
                out.append((op, float(km.group(1))))
    return out


def _extract_axis_args(expr: str) -> List[Tuple[str, str]]:
    """返回 [(op_name, axis_name), ...]。

    实现：逐调用点扫 op(...) 段，然后在**本调用点内**匹配 axis 名。
    之前用一次正则 `op\\([^)]*axis` 会贪婪把外层 rank(...) 也吃进去，
    导致 group_rank(..., exchange) 被错认成 rank(..., exchange)。
    """
    axes = ("industry", "subindustry", "sector", "market", "country", "exchange")
    axis_re = re.compile(r"\b(" + "|".join(axes) + r")\b")
    call_re = re.compile(r"\b([a-z_][a-z0-9_]*)\s*\(([^()]*)\)")
    out: List[Tuple[str, str]] = []
    for m in call_re.finditer(expr):
        op = m.group(1)
        args = m.group(2)
        for am in axis_re.finditer(args):
            out.append((op, am.group(1)))
    return out


def apply_dimension_gate(
    exprs: List[str],
    region: str,
    dataset: str,
    dim_min_size: int,
    tested_by: str,
    db_path: Optional[str],
    mode: str,
) -> Dict[str, Any]:
    """维度级覆盖闸（2026-10-20 新口径，替代字段级 100%）。

    口径：把字段按 semantic_family 分为语义维度（字段数 < dim_min_size 的族并入「其他」），
    要求**每个维度至少被 1 条候选表达式触及**。

    - 主闸：当前候选集是否覆盖全部维度
    - 附报：历史维度覆盖（该族是否有字段真跑过回测，tested_by=backtest 时看 n_tests>0）
    """
    gate = "dimension_coverage"
    path = db_path or os.environ.get("WQB_DB") or str(Path(__file__).resolve().parent.parent / "data" / "wqb.db")
    try:
        con = _db_ro_connect(path)   # 2026-10-27：本处漏改，仍是裸 connect（同文件已有规范工厂）
        con.row_factory = sqlite3.Row
        rows = list(con.execute(
            "SELECT field_name, semantic_family, n_tests, verdict FROM field_profile_full "
            "WHERE region=? AND dataset=?", (region, dataset)))
    except Exception as e:  # noqa: BLE001
        return {"gate": gate, "verdict": "SKIP", "reason": f"DB 读取失败: {e}"}
    finally:
        try:
            con.close()
        except Exception:  # noqa: BLE001
            pass

    if not rows:
        return {"gate": gate, "verdict": "SKIP",
                "reason": f"field_profile_full 无 {region}/{dataset} 记录（先跑 load_field_profiles_to_db.py）"}

    fam: Dict[str, List[str]] = {}
    hist_tested: Dict[str, int] = {}
    for r in rows:
        f = r["semantic_family"] or "其他"
        fam.setdefault(f, []).append(r["field_name"])
        if tested_by == "backtest":
            hit = (r["n_tests"] or 0) > 0
        else:
            hit = (r["verdict"] or "UNTESTED") != "UNTESTED"
        if hit:
            hist_tested[f] = hist_tested.get(f, 0) + 1

    # 小族并入「其他」
    required: Dict[str, List[str]] = {}
    for f, fl in fam.items():
        if len(fl) >= dim_min_size:
            required[f] = fl
    if not required:
        # 小数据集（字段太少，分不出维度）⇒ 退回「整集 = 单一维度」，
        # 等价于要求全部字段都被触及（成本本来就低）
        if len(rows) <= max(10, dim_min_size * 2):
            all_fields = [r["field_name"] for r in rows]
            hit = [x for x in all_fields if any(x in e for e in exprs)]
            miss = [x for x in all_fields if x not in hit]
            covr = len(hit) / len(all_fields) if all_fields else 0
            return {
                "gate": gate,
                "verdict": "PASS" if not miss else ("WARN" if mode != "enforce" else "FAIL"),
                "required_dims": 1, "covered_dims": 0 if miss else 1,
                "coverage": round(covr, 4),
                "missing_dims": ["全字段（小数据集退回字段级）"] if miss else [],
                "missing_sample_fields": {"全字段（小数据集退回字段级）": miss[:6]} if miss else {},
                "hist_tested_dims": {"全字段": sum(1 for r in rows if (r["n_tests"] or 0) > 0)},
                "params": {"dim_min_size": dim_min_size, "tested_by": tested_by,
                           "mode_note": "small-dataset fallback to field-level"},
            }
        return {"gate": gate, "verdict": "SKIP",
                "reason": f"无可判维度（所有族字段数 < {dim_min_size}）"}

    touched: Dict[str, List[str]] = {}
    for expr in exprs:
        for f, fl in required.items():
            hit = [x for x in fl if x in expr]
            if hit:
                touched.setdefault(f, []).extend(hit)

    missing = [f for f in required if f not in touched]
    coverage = (len(required) - len(missing)) / len(required)
    verdict = "PASS" if not missing else ("WARN" if mode != "enforce" else "FAIL")
    return {
        "gate": gate,
        "verdict": verdict,
        "required_dims": len(required),
        "covered_dims": len(required) - len(missing),
        "coverage": round(coverage, 4),
        "missing_dims": missing,
        "missing_sample_fields": {f: required[f][:3] for f in missing},
        "hist_tested_dims": {f: hist_tested.get(f, 0) for f in sorted(required)},
        "params": {"dim_min_size": dim_min_size, "tested_by": tested_by},
    }


def apply_boundary_gate(
    exprs: List[str],
    boundary_cfg: Dict[str, Any],
    near_gate: bool,
    mode: str,
) -> Dict[str, Any]:
    operators = boundary_cfg.get("operators") or {}
    unknown_ops: Set[str] = set()
    illegal: List[Dict[str, Any]] = []
    incomplete: List[Dict[str, Any]] = []

    for expr in exprs:
        ops_here = extract_ops(expr)
        numeric_args = _extract_numeric_args(expr)
        for op in ops_here:
            if op not in operators:
                unknown_ops.add(op)
                continue
            cfg = operators[op]
            kind = cfg.get("kind")
            if kind in ("window", "exponent", "quantile", "std", "threshold", "bins"):
                legal = cfg.get("legal_values", [])
                min_cov = cfg.get("min_coverage_for_near_gate", 1)
                values_here = [v for _o, v in numeric_args if _o == op]
                if legal and values_here:
                    for v in values_here:
                        if v not in legal:
                            illegal.append({
                                "op": op,
                                "expr": expr,
                                "value": v,
                                "legal_values": legal,
                                "msg": f"{op} 参数 {v} 不在合法档 {legal}",
                            })
                if near_gate:
                    if min_cov >= 2 and len(set(values_here)) < min_cov:
                        incomplete.append({
                            "op": op,
                            "min_cov": min_cov,
                            "values_seen": sorted(set(values_here)),
                            "expr": expr,
                            "msg": f"近闸候选要求该算子 ≥{min_cov} 档已试，"
                                   f"本波只见 {sorted(set(values_here))}",
                        })
            elif kind == "axis":
                legal_axes = cfg.get("legal_axes", [])
                must_include = cfg.get("must_include", [])
                axes_here = {a for _op, a in _extract_axis_args(expr) if _op == op}
                illegal_axes = axes_here - set(legal_axes)
                if illegal_axes:
                    illegal.append({
                        "op": op,
                        "expr": expr,
                        "illegal_axes": sorted(illegal_axes),
                        "legal_axes": legal_axes,
                    })
                if near_gate and must_include:
                    missing = [ax for ax in must_include if ax not in axes_here]
                    if missing:
                        incomplete.append({
                            "op": op,
                            "missing_axes": missing,
                            "expr": expr,
                            "msg": f"近闸要求 axis ∈ {must_include}",
                        })

    fail = bool(illegal) or (near_gate and bool(incomplete))
    verdict = "PASS" if not fail else "FAIL"
    if verdict == "FAIL" and mode == "warn":
        verdict = "WARN"
    return {
        "gate": "boundary_ops",
        "verdict": verdict,
        "near_gate": near_gate,
        "unknown_ops": sorted(unknown_ops),
        "illegal_count": len(illegal),
        "illegal": illegal,
        "incomplete_count": len(incomplete),
        "incomplete": incomplete,
    }


# --------------------------------------------------------------- CLI


def main() -> int:
    ap = argparse.ArgumentParser(
        description="EUR 全量覆盖闸（字段/模板族/边界算子 三道一次过）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--region", required=True, help="区域代码（EUR）")
    ap.add_argument("--dataset", required=True, help="数据集名")
    ap.add_argument("--expr", help="单条表达式")
    ap.add_argument("--exprs-file", help="多行表达式文件（每行一条）")
    ap.add_argument("--candidates", help="候选 JSON 文件")
    ap.add_argument("--fields-list", help="字段全集 JSON 文件（含 fields 键或直接是字符串列表）")
    ap.add_argument("--all-fields", help="字段全集，逗号分隔（无字段目录 JSON 时的兜底）")
    ap.add_argument("--boundary-config", help="边界算子配置 JSON")
    ap.add_argument("--campaign-dir", help="战役目录（用于查历史模板族）")
    ap.add_argument("--min-families", type=int, default=3, help="模板族最小数量（默认 3）")
    ap.add_argument("--coverage-mode", choices=["dimension", "field"], default="dimension",
                    help="覆盖闸口径：dimension=维度级（2026-10-20 新默认）｜field=字段级 100%%（近闸深挖时用）")
    ap.add_argument("--dim-min-size", type=int, default=3,
                    help="维度级模式下，字段数 ≥ 该值的语义族才算一个必须覆盖的维度（默认 3）")
    ap.add_argument("--dim-tested-by", choices=["backtest", "verdict"], default="backtest",
                    help="历史维度覆盖的判定：backtest=真跑过(n_tests>0)｜verdict=非 UNTESTED")
    ap.add_argument("--coverage", type=float, default=1.0,
                    help="字段覆盖率要求（默认 1.0 = 全量）")
    ap.add_argument("--gate-mode", choices=["off", "warn", "enforce"], default="warn",
                    help="off=不判定；warn=FAIL 转 WARN；enforce=FAIL 直接 exit 1")
    ap.add_argument("--near-gate", action="store_true",
                    help="近闸模式：要求边界算子已试完 min_coverage 档")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    exprs = load_expressions(args)
    if not exprs:
        sys.stderr.write("[fcg] 无候选表达式——请传 --expr / --exprs-file / --candidates\n")
        return 2

    known_fields, fields_src = resolve_field_source(args)
    if not known_fields:
        sys.stderr.write(f"[fcg] 无字段全集：{fields_src}；请传 --fields-list 或 --all-fields\n")
        return 2

    field_gate = apply_field_gate(exprs, known_fields, args.coverage, args.gate_mode)
    dim_gate = None
    if args.coverage_mode == "dimension":
        dim_gate = apply_dimension_gate(
            exprs, args.region, args.dataset, args.dim_min_size,
            args.dim_tested_by, getattr(args, "db_path", None), args.gate_mode)

    # 2026-10-20（P0-1）：族历史 ∪ DB expressions.family（战役产物已入库，
    # 文件扫描只覆盖 candidates/cache/tracking 三目录的历史布局）。
    db_families = load_db_families(args.region, args.dataset,
                                   db_path=getattr(args, "db_path", None))
    family_gate = apply_family_gate(
        args.campaign_dir or "", args.dataset, args.min_families, exprs, args.gate_mode,
        db_families=db_families,
    )

    boundary_cfg = load_boundary_config(args)
    boundary_gate = apply_boundary_gate(exprs, boundary_cfg, args.near_gate, args.gate_mode)

    gates = [field_gate, family_gate, boundary_gate]
    if dim_gate is not None:
        # 维度模式下，字段闸降级为提示（仍输出，但不参与 fail 判定）
        field_gate["verdict"] = "INFO" if field_gate["verdict"] == "FAIL" else field_gate["verdict"]
        gates = [dim_gate, family_gate, boundary_gate]
    any_fail = any(g["verdict"] == "FAIL" for g in gates)

    result = {
        "ok": not any_fail,
        "region": args.region,
        "dataset": args.dataset,
        "mode": args.gate_mode,
        "fields_source": fields_src,
        "expr_count": len(exprs),
        "gates": gates,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[full_coverage_gate] {args.region}/{args.dataset} mode={args.gate_mode}")
        print(f"  字段全集: {fields_src} ({len(known_fields)} 个)")
        print(f"  表达式: {len(exprs)} 条")
        for g in gates:
            print(f"  {g['gate']:20s} {g['verdict']:4s}", end="")
            if g["gate"] == "field_coverage":
                print(f"  {g['covered']}/{g['total_fields']} = {g['coverage']:.2%} (req≥{g['required']:.2f})")
            elif g["gate"] == "template_family":
                print(f"  {g['total']}/{g['min_families']} gap={g['gap']}")
            elif g["gate"] == "dimension_coverage":
                if g["verdict"] == "SKIP":
                    print(f"  skipped: {g.get('reason','')}")
                else:
                    print(f"  {g['covered_dims']}/{g['required_dims']} = {g['coverage']:.0%}"
                          f"  missing={g.get('missing_dims')}")
            else:
                print(f"  illegal={g.get('illegal_count')} incomplete={g.get('incomplete_count')}"
                      f" near_gate={g.get('near_gate')}")
        if not result["ok"]:
            print("[full_coverage_gate] FAIL —— 请补维度 / 补模板族 / 补边界档 后重跑"
                  "（字段级 100% 仅在 --coverage-mode field 下强制）")

    if any_fail and args.gate_mode == "enforce":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
