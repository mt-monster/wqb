# -*- coding: utf-8 -*-
"""audit_dataset_coverage.py - 数据集覆盖度审计门（覆盖闸可逆化 + 结论截断对齐）。

## 为什么有这只工具（两条根因，2026-11-09 GBR 实证）

**根因 A：覆盖率闸 = 不可逆的静默硬拦截。**
战役 SOP 的漏斗把「数据集级 coverage」排在第 3 位（塔 → 语义 → 画像 cov<0.6 剔除 → ...）。
它一旦砍掉一个数据集，后面的语义闸、近静态闸、模板设计**永远不会被评估**，而且静默：
不报错、不告警，只留一个「跳过」。被错误前置条件剔除的分支，成本是零感知的。

**根因 B：抽样被截断，但结论没有跟着截断。**
「后 12 波 72 条 0 增席」是真数据，但这 72 条全部抽样自 `cov>0` 的池子；
把「这个方向穷尽」外推成「这个区域穷尽」，就是用一个把储备排除在外的样本证明储备不存在。

## ★ 2026-11-09 实测：coverage 这个字段本身不可信（三层都不可信）

| 层 | 实测 | 结论 |
|---|---|---|
| 数据集级 `get_datasets.coverage` | `techindi_model` = **0.0**，而它有 399 个字段、贡献该战役 10 席中的 2 席 | 不能判存在性 |
| field 级 `/data-fields.coverage` | GBR 177 个集里 **109 个集的所有字段 coverage 全 = 0.0**（含 `techindi_model` / `fundamental1` / `other78`） | 也不能判存在性 |
| 字段目录 `/data-fields.count` | 177/177 个集都返回 >0 个字段 | **只有这一层是真的** |

⇒ 本工具的「有数据」判据 = **字段目录非空**（`fields_seen > 0`）；
`coverage` 只作**辅助标记**：全 0 时打 `cov_metadata_blind`，该集的「有没有持仓」只能靠
一条 `longCount/shortCount` 探针回答，**不许**据此判死。`/data-fields` 返回 0 字段才算 `NO_FIELDS`。

## 「挖过没」的证据口径

- 机械证据：DB `expressions` 里该 region 真有回测行的 dataset（复用
  `tools/gates/category_coverage_audit.load_tested_from_db`，同一判据源，不另造一份）。
- 可选补充：`--evidence-codes-file`（一行一条 alpha 表达式），按字段名匹配。
- **fail-closed**：证据通道一个都没成就把整批标成 `UNTESTED_*` 是错的——那种情况下
  status 只能是 `EVIDENCE_UNKNOWN`，且 `--gate closure` 直接失败（不许用「不知道」冒充「没挖过」）。

## 用法

    # 1) 全量审计（D1）；--reuse-cache 可复用上一次的 field 结果（只重算证据与状态，秒级）
    python tools/gates/audit_dataset_coverage.py --region GBR --universe TOP700 --delay 1 \
        --cache data/dataset_assets/GBR_coverage_audit_d1.json \
        --md reports/dataset_experience/gbr_coverage_audit_20261109.md

    # 2) 派发前跑门：池子里的集必须 field 级验过（不许只有「cov=0」这一条否定）
    python tools/gates/audit_dataset_coverage.py --region GBR --universe TOP700 --delay 1 \
        --reuse-cache data/dataset_assets/GBR_coverage_audit_d1.json --gate coverage

    # 3) 声称「区域穷尽 / 上限 N 席」前跑门：不许有「元数据盲区 + 未探」的集
    python tools/gates/audit_dataset_coverage.py ... --gate closure
    python tools/gates/audit_dataset_coverage.py ... --gate probe      # 只要探针清单

    # 4) 报告措辞门：穷尽类断言必须带 scope 限定
    python tools/gates/audit_dataset_coverage.py --lint-report <report.md>

    # 5) SOP 文本措辞门：skill 文档里「cov<X ⇒ 剔除/判死」的筛选规则（根因 C）
    python tools/gates/audit_dataset_coverage.py --lint-skills          # 默认扫 Claude/skills

退出码：0 = 全过；1 = 门失败；2 = 环境错误（凭证/分页/参数）。
纯标准库 + `tools/lib/api_client`；凭证走 `~/.brain_credentials` / MCP .env，不打印。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime


def _find_repo_root() -> str:
    """向上探测 pyproject.toml + src/wqb 双标记（AGENTS.md §8 禁层数硬编码）。"""
    cur = os.path.dirname(os.path.abspath(__file__))
    for _ in range(8):
        if (os.path.isfile(os.path.join(cur, "pyproject.toml"))
                and os.path.isdir(os.path.join(cur, "src", "wqb"))):
            return cur
        cur = os.path.dirname(cur)
    raise SystemExit("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


REPO_ROOT = _find_repo_root()
for _extra in (os.path.join(REPO_ROOT, "src"),
               os.path.join(REPO_ROOT, "tools", "lib"),
               os.path.join(REPO_ROOT, "tools"),
               os.path.join(REPO_ROOT, "tools", "gates")):
    if os.path.isdir(_extra) and _extra not in sys.path:
        sys.path.insert(0, _extra)

# 网络工具统一在 MCP venv 下跑（tools/README.md 约定）；缺 venv 时原地继续
try:                                                               # pragma: no cover
    import _pyenv
    _pyenv.reexec_under_venv()
except Exception:                                                  # noqa: BLE001
    pass

from api_client import Api, _get_json, load_creds, paginate_all  # noqa: E402

PAGE = 50                      # /data-sets & /data-fields 平台硬上限
DEFAULT_DB = os.path.join(REPO_ROOT, "data", "wqb.db")
SKILLS_ROOT = os.path.join(REPO_ROOT, "Claude", "skills")
COV_KILL_ALLOW = os.path.join(REPO_ROOT, "tools", "gates", "_covskill_allow.json")

STATUS_ORDER = {
    "UNTESTED_BLIND": 0,       # ★ 有字段、coverage 元数据全 0、零回测证据 -> 必须探针
    "UNTESTED_COV_OK": 1,      # 有字段且元数据说有用量、但零回测证据
    "EVIDENCE_UNKNOWN": 2,     # 证据通道全挂 -> 既不能说挖过也不能说没挖过
    "PROBE_FAILED": 2.5,       # 探针跑过但仿真失败 -> 仍然「不知道」，必须重跑
    "NO_FIELDS": 3,            # /data-fields 返回 0 字段（这才是可判死的证据）
    "NO_DATA": 3.5,            # ★ 探针实测 longCount+shortCount = 0（唯一合法的「没数据」）
    "TESTED": 4,               # expressions 有回测记录 / code 匹配到字段 / 探针实测有持仓
    "LIT_EXCLUDED": 5,         # 塔已点亮（规则性排除，与数据无关）
    "UNVERIFIED": 6,           # 字段拉取失败 -> 不可下任何结论
}
UNTESTED_STATUSES = ("UNTESTED_BLIND", "UNTESTED_COV_OK")
# closure 门的阻断集合：未探 + 探针失败。后者 = 还是不知道，绝不许当成「没数据」。
CLOSURE_BLOCKING = UNTESTED_STATUSES + ("PROBE_FAILED",)

BANNED_CLAIMS = (
    ("no_unexplored_axis", r"不再有未探轴"),
    ("exhausted_verified", r"已穷尽验证|穷尽验证"),
    ("spatial_exhausted", r"搜索空间穷尽"),
    ("math_unreachable", r"数学不可达"),
    ("hard_cap_seats", r"上限\s*[=＝]\s*\*{0,2}\d+\*{0,2}\s*席"),
    ("region_exhausted", r"(区域|本区|GBR)\s*(已)?穷尽"),
    ("exhausted_generic", r"已穷尽|穷尽在"),
)
SCOPE_MARKERS = ("scope:", "scope：", "样本:", "样本：", "样本内", "本报告样本",
                 "截断:", "截断：", "条件性", "在已勘测", "候选池=", "候选池：",
                 "只覆盖", "池子内", "不外推")


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _cat(v) -> str:
    if isinstance(v, dict):
        return str(v.get("id") or v.get("name") or "?")
    return str(v or "?")


def _fnum(v, default=None):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


# ----------------------------------------------------------------------------- pull
def pull_datasets(api, region: str, universe: str, delay: int):
    base = ("/data-sets?instrumentType=EQUITY&region=%s&delay=%d&universe=%s"
            % (region, delay, universe))
    r = paginate_all(api, base, limit=PAGE, sleep=0.25)
    rows = []
    for d in r["items"]:
        rows.append({
            "dataset": d.get("id"),
            "name": d.get("name"),
            "category": _cat(d.get("category")),
            "dataset_cov": _fnum(d.get("coverage")),
            "field_count_meta": d.get("fieldCount"),
            "user_count": d.get("userCount"),
            "alpha_count": d.get("alphaCount"),
            "value_score": _fnum(d.get("valueScore")),
            "pyramid_multiplier": _fnum(d.get("pyramidMultiplier")),
            "desc": (d.get("description") or "")[:160],
        })
    return rows, r.get("platform_count"), r.get("complete")


def pull_fields(api, region: str, universe: str, delay: int,
                dataset_id: str, max_pages: int):
    """字段目录实查。只取前 max_pages 页 -> 截断必须被记录（根因 B）。"""
    base = ("/data-fields?instrumentType=EQUITY&region=%s&delay=%d&universe=%s"
            "&dataset.id=%s" % (region, delay, universe, dataset_id))
    items, platform_count, pages, truncated = [], None, 0, False
    offset = 0
    while pages < max_pages:
        try:
            j = _get_json(api, "%s&limit=%d&offset=%d" % (base, PAGE, offset))
        except Exception as e:                                    # pragma: no cover
            return {"ok": False, "error": "%s: %s" % (type(e).__name__, e),
                    "field_names": [], "fields_seen": len(items),
                    "platform_count": platform_count, "pages": pages, "truncated": True}
        pages += 1
        res = j.get("results") or []
        items.extend(res)
        if platform_count is None:
            platform_count = j.get("count")
        offset += len(res)
        if not res or (platform_count is not None and offset >= platform_count):
            break
    if platform_count is not None and len(items) < platform_count:
        truncated = True
    covs = [_fnum(f.get("coverage")) for f in items]
    covs = [c for c in covs if c is not None]
    return {
        "ok": True,
        "field_names": [f.get("id") for f in items if f.get("id")],
        "fields_seen": len(items),
        "platform_count": platform_count,
        "pages": pages,
        "truncated": truncated,
        "max_field_cov": max(covs) if covs else None,
        "n_field_cov_gt0": sum(1 for c in covs if c > 0),
        "n_field_cov_ge60": sum(1 for c in covs if c >= 0.6),
        "field_types": sorted({str(f.get("type")) for f in items if f.get("type")}),
    }


def pull_pyramid(api, delay=None):
    """塔点亮表。★ 必须按 delay 过滤：形态 B 的每条记录都带 delay，跨 delay 求和会把
    D1 的点亮状态套到 D0 上（GBR 实测：D0 十四类**全 0**，聚合后会误判 45 个集「已点亮塔」）。"""
    try:
        j = _get_json(api, "/users/self/activities/pyramid-alphas")
    except Exception as e:                                         # pragma: no cover
        return {"ok": False, "error": "%s: %s" % (type(e).__name__, e), "by_region": {}, "delay_filtered": False}
    by_region: dict = {}
    d = j.get("pyramids") if isinstance(j, dict) else None
    if isinstance(d, dict):                     # 形态 A：{REGION: {TIER: {cat: cnt}}}
        for reg, tiers in d.items():
            flat = by_region.setdefault(str(reg).upper(), {})
            for _tier, cats in (tiers or {}).items():
                if isinstance(cats, dict):
                    for c, v in cats.items():
                        cnt = v.get("count") if isinstance(v, dict) else v
                        try:
                            flat[_cat(c)] = flat.get(_cat(c), 0) + int(cnt or 0)
                        except (TypeError, ValueError):
                            pass
    elif isinstance(d, list):                   # 形态 B（本平台实测）：[{category, region, delay, alphaCount}]
        for it in d:
            if not isinstance(it, dict):
                continue
            if delay is not None and it.get("delay") is not None:
                try:
                    if int(it.get("delay")) != int(delay):
                        continue                                 # ★ 跨 delay 求和 = 把别的 delay 的点亮状态搬过来
                except (TypeError, ValueError):
                    pass
            reg = str(it.get("region") or "").upper()
            cat = _cat(it.get("category"))
            try:
                n = int(it.get("alphaCount") or 0)
            except (TypeError, ValueError):
                n = 0
            flat = by_region.setdefault(reg, {})
            flat[cat] = flat.get(cat, 0) + n
    return {"ok": bool(by_region), "by_region": by_region, "delay_filtered": delay is not None}


def pull_tested_from_db(region: str, db_path=None):
    """机械证据：DB `expressions` 里该 region 真有回测行的 dataset（复用同一判据源）。"""
    try:
        from category_coverage_audit import load_tested_from_db
        return sorted(load_tested_from_db(region, db_path)), "db:expressions"
    except Exception as exc:                                       # noqa: BLE001
        return [], "db:unavailable(%s)" % type(exc).__name__


def load_db_expression_text(region: str, db_path=None):
    """机械证据之二：DB ~expressions~ 里该 region 的**表达式原文**（覆盖 MCP 直连仿真）。"""
    db = db_path or DEFAULT_DB
    if not os.path.isfile(db):
        return "", "db:text:missing"
    try:
        from wqb import db_conn
        conn = db_conn.connect(db, timeout=3, readonly=True)
        try:
            rows = conn.execute(
                "SELECT expression, dataset FROM expressions WHERE upper(region)=? "
                "AND expression IS NOT NULL AND expression != ''", (region.upper(),)
            ).fetchall()
        finally:
            conn.close()
    except Exception as exc:                                       # noqa: BLE001
        return "", "db:text:unavailable(%s)" % type(exc).__name__, {}
    texts = [str(r[0]) for r in rows if r and r[0]]
    null_n = sum(1 for r in rows if not r[1])
    stats = {"rows": len(rows), "dataset_null": null_n,
             "dataset_null_pct": round(100.0 * null_n / len(rows), 1) if rows else None}
    return "\n".join(texts), "db:text(%d)" % len(rows), stats


def load_evidence_codes(path):
    if not path:
        return ""
    if not os.path.isfile(path):
        return ""
    return "\n".join(ln.strip() for ln in open(path, encoding="utf-8") if ln.strip())


def load_probe_results(path):
    """读探针执行器产物 -> {dataset_lower: {data_present, long_count, ...}}。

    接受三种形态：`{"results": {ds: rec}}`（dataset_data_probe.py 产物）、
    `[{dataset: ...}]` 列表、以及裸 `{ds: rec}` 字典。
    解析失败一律返回空表 + 错误标记 —— 由调用方把状态留在 `UNTESTED_*`，
    **不允许**把「读不到探针文件」当成「探过了」。
    """
    if not path:
        return {}, None
    if not os.path.isfile(path):
        return {}, "missing:%s" % path
    try:
        raw = json.load(open(path, encoding="utf-8"))
    except Exception as e:                                          # noqa: BLE001
        return {}, "parse_error:%s" % type(e).__name__
    rows = raw
    if isinstance(raw, dict):
        rows = raw.get("results") if isinstance(raw.get("results"), (dict, list)) else raw
    out = {}
    if isinstance(rows, dict):
        iterable = [(k, v) for k, v in rows.items()]
    elif isinstance(rows, list):
        iterable = [(str(v.get("dataset") or ""), v) for v in rows if isinstance(v, dict)]
    else:
        return {}, "unexpected_shape:%s" % type(rows).__name__
    for k, v in iterable:
        if not k or not isinstance(v, dict):
            continue
        out[str(k).strip().lower()] = v
    return out, None


# ----------------------------------------------------------------------------- audit
def audit(region, universe, delay, lit_threshold, max_field_pages,
          db_path=None, evidence_codes_file=None, reuse_cache=None, verbose=True,
          use_db_expressions=True, probe_results=None):
    api = Api()
    email, pwd = load_creds()
    if not email or not pwd:
        return {"ok": False, "error": "credential missing (`/.brain_credentials / MCP .env)"}
    api.login(email, pwd)

    ds_rows, ds_count, ds_complete = pull_datasets(api, region, universe, delay)
    pyr = pull_pyramid(api, delay)
    flat = pyr.get("by_region", {})
    lit = flat.get(region.upper()) or flat.get(region) or {}

    tested_db, db_src = pull_tested_from_db(region, db_path)
    tested_db_l = {d.strip().lower() for d in tested_db}
    codes_parts, evidence_sources = [], []
    if db_src.startswith("db:expressions"):
        evidence_sources.append(db_src)
    db_text_stats = {}
    if use_db_expressions:
        txt, src, db_text_stats = load_db_expression_text(region, db_path)
        if txt:
            codes_parts.append(txt)
            evidence_sources.append(src)
    file_codes = load_evidence_codes(evidence_codes_file)
    if file_codes:
        codes_parts.append(file_codes)
        evidence_sources.append("codes:%s" % evidence_codes_file)
    codes = "\n".join(codes_parts)
    # 字段名匹配走 token 集合（12k+ 条表达式下逐条正则会慢一个量级）
    code_tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", codes))
    evidence_ok = bool(evidence_sources)

    reuse = {}
    if reuse_cache and os.path.isfile(reuse_cache):
        try:
            prev = json.load(open(reuse_cache, encoding="utf-8"))
            for row in prev.get("rows") or []:
                if row.get("field_verified"):
                    reuse[str(row.get("dataset")).strip().lower()] = row
        except Exception:                                          # noqa: BLE001
            reuse = {}

    probe_map, probe_err = load_probe_results(probe_results)

    out, reused_n = [], 0
    for i, row in enumerate(ds_rows, 1):
        ds = row["dataset"]
        prev = reuse.get(str(ds).strip().lower())
        if prev is not None:
            fs = {"ok": True, "field_names": prev.get("field_names") or [],
                  "fields_seen": prev.get("fields_seen") or 0,
                  "platform_count": prev.get("fields_platform_count"),
                  "truncated": prev.get("fields_sample_truncated"),
                  "max_field_cov": prev.get("max_field_cov"),
                  "n_field_cov_gt0": prev.get("n_field_cov_gt0") or 0,
                  "n_field_cov_ge60": prev.get("n_field_cov_ge60") or 0,
                  "field_types": prev.get("field_types")}
            reused_n += 1
        else:
            fs = pull_fields(api, region, universe, delay, ds, max_field_pages)
            if verbose and i % 20 == 0:
                print("[audit] %d/%d datasets" % (i, len(ds_rows)), flush=True)

        names = fs.get("field_names") or []
        hits = [n for n in names if n and n in code_tokens]
        lit_cnt = int(lit.get(row["category"], 0) or 0)
        fields_seen = fs.get("fields_seen") or 0
        has_fields = bool(fs.get("ok") and fields_seen > 0)
        in_evidence = (ds or "").strip().lower() in tested_db_l or bool(hits)
        blind = bool(has_fields and (fs.get("n_field_cov_gt0") or 0) == 0)

        pr_ok = probe_map.get((ds or "").strip().lower())
        if lit_cnt >= lit_threshold:
            status = "LIT_EXCLUDED"
        elif pr_ok is not None and pr_ok.get("data_present") is True:
            status = "TESTED"
        elif pr_ok is not None and pr_ok.get("data_present") is False:
            status = "NO_DATA"
        elif pr_ok is not None:
            status = "PROBE_FAILED"
        elif not fs.get("ok"):
            status = "UNVERIFIED"
        elif fields_seen == 0:
            status = "NO_FIELDS"
        elif in_evidence:
            status = "TESTED"
        elif not evidence_ok:
            status = "EVIDENCE_UNKNOWN"
        elif blind:
            status = "UNTESTED_BLIND"
        else:
            status = "UNTESTED_COV_OK"

        rec = dict(row)
        rec.update({
            "tier": "D%d" % delay,
            "lit_count": lit_cnt,
            "status": status,
            "field_verified": bool(fs.get("ok") and fields_seen > 0),
            "has_fields": has_fields,
            "cov_metadata_blind": blind,
            "fields_seen": fields_seen,
            "fields_platform_count": fs.get("platform_count"),
            "fields_sample_truncated": fs.get("truncated"),
            "field_types": fs.get("field_types"),
            "max_field_cov": fs.get("max_field_cov"),
            "n_field_cov_gt0": fs.get("n_field_cov_gt0"),
            "n_field_cov_ge60": fs.get("n_field_cov_ge60"),
            "field_names": names[:200],
            "field_names_n": len(names),
            "evidence_hits": hits[:5],
            "evidence_hit_n": len(hits),
            "in_db_evidence": (ds or "").strip().lower() in tested_db_l,
            "reused_field_probe": prev is not None,
            "probe_status": (pr_ok or {}).get("status"),
            "probe_field": (pr_ok or {}).get("field"),
            "probe_expr": (pr_ok or {}).get("expr"),
            "probe_alpha_id": (pr_ok or {}).get("alpha_id"),
            "probe_long_count": (pr_ok or {}).get("long_count"),
            "probe_short_count": (pr_ok or {}).get("short_count"),
            "probe_data_present": (pr_ok or {}).get("data_present"),
        })
        out.append(rec)

    out.sort(key=lambda r: (STATUS_ORDER.get(r["status"], 9),
                            -(r["value_score"] or 0), r["dataset"] or ""))
    counts = {}
    for r in out:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    result = {
        "generated_at": _now(),
        "region": region, "universe": universe, "delay": delay,
        "scope": {
            "universe": universe, "delay": delay, "instrument_type": "EQUITY",
            "datasets_platform_count": ds_count,
            "datasets_pulled": len(ds_rows),
            "datasets_complete": ds_complete,
            "field_sample_pages_cap": max_field_pages,
            "field_sample_truncated_n": sum(1 for r in out if r["fields_sample_truncated"]),
            "field_probe_reused": reused_n,
            "evidence_sources": evidence_sources,
            "evidence_ok": evidence_ok,
            "evidence_db_datasets": len(tested_db_l),
            "evidence_codes_chars": len(codes),
            "evidence_tokens": len(code_tokens),
            "evidence_dataset_column_null": db_text_stats.get("dataset_null"),
            "evidence_dataset_column_null_pct": db_text_stats.get("dataset_null_pct"),
            "evidence_blind_spots": [
                "MCP 直连仿真（create_simulation / create_multi_simulation）不写 "
                "data/wqb.db::expressions ⇒ 本工具的『挖过没』对这类记录盲视："
                "池内『零挖掘记录』不等于没跑过。判『没挖过』前必须回波次日志/仿真台账核对。",
            ],
            "lit_threshold": lit_threshold,
            "pyramid_ok": pyr.get("ok"),
            "coverage_metadata_blind_n": sum(1 for r in out if r["cov_metadata_blind"]),
            "probe_results_file": probe_results,
            "probe_results_error": probe_err,
            "probe_results_n": len(probe_map),
            "probe_data_present_n": sum(1 for v in probe_map.values()
                                        if v.get("data_present") is True),
            "probe_no_data_n": sum(1 for v in probe_map.values()
                                   if v.get("data_present") is False),
            "probe_failed_n": sum(1 for v in probe_map.values()
                                  if v.get("data_present") is None),
            "data_presence_criterion": "fields_seen>0（/data-fields 目录）；coverage 只作辅助标记；"
                                       "持仓有无以探针 longCount+shortCount 为准",
        },
        "counts": counts,
        "probe_only": [{"dataset": r["dataset"], "category": r["category"],
                        "probe_field": r.get("probe_field"),
                        "probe_long_count": r.get("probe_long_count"),
                        "probe_alpha_id": r.get("probe_alpha_id")}
                       for r in out if r["status"] == "TESTED"
                       and r.get("probe_data_present") is True
                       and not r.get("in_db_evidence")
                       and (r.get("evidence_hit_n") or 0) == 0],
        "lit_categories": lit,
        "rows": out,
    }
    return result


# ----------------------------------------------------------------------------- gates
def _waived(ds, waivers):
    return ds in waivers or ds.lower() in {k.lower() for k in waivers}


def gate_coverage(res, waivers):
    """根因 A：池子里的集必须 field 级验过（不许只有「cov=0」这一条否定）。"""
    bad = [r for r in res["rows"]
           if r["status"] == "UNVERIFIED" and not _waived(r["dataset"], waivers)]
    return {"gate": "coverage", "ok": not bad,
            "unverified": [r["dataset"] for r in bad],
            "note": "字段拉取失败的集不可下任何结论；池子里的每个集都必须有 field 级实查记录"}


def gate_closure(res, waivers):
    """根因 B：还有未探（含元数据盲区 / 探针失败）的集时，不许声称穷尽。"""
    untested = [r for r in res["rows"]
                if r["status"] in CLOSURE_BLOCKING and not _waived(r["dataset"], waivers)]
    unknown = [r for r in res["rows"]
               if r["status"] == "EVIDENCE_UNKNOWN" and not _waived(r["dataset"], waivers)]
    return {
        "gate": "closure", "ok": not untested and not unknown,
        "untested_with_fields": [
            {"dataset": r["dataset"], "category": r["category"], "status": r["status"],
             "value_score": r["value_score"], "alpha_count": r["alpha_count"],
             "fields_seen": r["fields_seen"], "cov_metadata_blind": r["cov_metadata_blind"]}
            for r in untested],
        "evidence_unknown": [r["dataset"] for r in unknown],
        "note": ("这些集有真实字段目录、且没有任何回测证据 -> 不构成『已穷尽』；"
                 "EVIDENCE_UNKNOWN = 证据通道挂了；PROBE_FAILED = 探针没跑成。"
                 "两者都是「不知道」，不许用「不知道」冒充「没挖过」，也不许冒充「没数据」"),
    }


def gate_probe(res, waivers):
    """元数据盲区集必须靠 longCount/shortCount 探针定生死。"""
    need = [r for r in res["rows"]
            if r["status"] in ("UNTESTED_BLIND", "PROBE_FAILED")
            and not _waived(r["dataset"], waivers)]
    return {"gate": "probe", "ok": not need,
            "probe_needed": [{"dataset": r["dataset"], "category": r["category"],
                              "value_score": r["value_score"],
                              "alpha_count": r["alpha_count"],
                              "fields_seen": r["fields_seen"]} for r in need],
            "note": ("coverage 全 0 不等于没数据（techindi_model 就是 0.0 且是唯一量产线）；"
                     "只能探针：python tools/probe/dataset_data_probe.py --plan <本清单> "
                     "--out <results.json>，再回灌 --probe-results")}


def lint_report(paths):
    viol, scoped = [], 0
    for path in paths:
        if not os.path.exists(path):
            viol.append({"path": path, "line": 0, "rule": "missing_file",
                         "text": "report not found"})
            continue
        lines = open(path, encoding="utf-8").read().splitlines()
        for i, ln in enumerate(lines):
            hit = next((name for name, pat in BANNED_CLAIMS if re.search(pat, ln)), None)
            if not hit:
                continue
            win = "\n".join(lines[max(0, i - 4): i + 5])
            if any(m in win for m in SCOPE_MARKERS):
                scoped += 1
                continue
            viol.append({"path": path, "line": i + 1, "rule": hit,
                         "text": ln.strip()[:160]})
    return {"gate": "report_lint", "ok": not viol, "violations": viol,
            "scoped_claims": scoped}


# ----------------------------------------------------------------------------- render
def render_md(res, gates=None):
    s = res["scope"]
    L = []
    L.append("# %s 数据集覆盖度审计（D%d / %s）" % (res["region"], res["delay"], s["universe"]))
    L.append("")
    L.append("生成：%s　工具：`tools/gates/audit_dataset_coverage.py`" % res["generated_at"])
    L.append("")
    L.append("## scope（引用本文任何结论前先读这一段）")
    L.append("")
    L.append("- 样本来源：平台 `/data-sets` 全量实拉（`instrumentType=EQUITY region=%s delay=%d "
             "universe=%s`），平台报 %s / 实拉 %d（完整=%s）"
             % (res["region"], res["delay"], s["universe"], s["datasets_platform_count"],
                s["datasets_pulled"], s["datasets_complete"]))
    L.append("- 「有没有数据」判据 = **字段目录 `/data-fields` 非空**（%s）；"
             "coverage **不作为**存在性判据（见下节实测）" % s["data_presence_criterion"])
    L.append("- 「挖过没」证据源：%s（证据条数 %d 个数据集）；证据通道状态 = %s"
             % (", ".join(s["evidence_sources"]) or "无", s["evidence_db_datasets"],
                "OK" if s["evidence_ok"] else "**不可用 ⇒ 不许判『没挖过』**"))
    if s.get("evidence_dataset_column_null"):
        L.append("- ★ 证据链的第四个洞：~expressions.dataset~ 在本区有 **%d 行（%s%%）为 NULL**"
                 "——只按该列取「已测集」会把真实回测记成「没挖过」。"
                 "本工具判据是**表达式原文里的字段名**，不是该列。"
                 % (s["evidence_dataset_column_null"],
                    s.get("evidence_dataset_column_null_pct")))
    for _bs in (s.get("evidence_blind_spots") or []):
        L.append("- ★ 证据盲区：%s" % _bs)
    if s.get("probe_results_n"):
        L.append("- 探针回灌：`%s`（%d 条；实测有数据 %d / 实测无数据 %d / 失败 %d）"
                 % (s["probe_results_file"], s["probe_results_n"],
                    s["probe_data_present_n"], s["probe_no_data_n"], s["probe_failed_n"]))
    elif s.get("probe_results_error"):
        L.append("- 探针回灌：**失败**（`%s`）⇒ 状态保持未探，不冒充结论"
                 % s["probe_results_error"])
    L.append("- 截断条件：字段抽查每集最多 %d 页（%d 集被截断，%d 集复用上次探针）；"
             "**截断存在 ⇒ 本文结论只覆盖该样本**"
             % (s["field_sample_pages_cap"], s["field_sample_truncated_n"],
                s["field_probe_reused"]))
    L.append("")
    L.append("## ★ coverage 三层实测（本区最贵的教训）")
    L.append("")
    L.append("| 层 | 实测 | 可作判据？ |")
    L.append("|---|---|---|")
    L.append("| 数据集级 `coverage` | `techindi_model` = 0.0，却有 399 字段、贡献 10 席中的 2 席 | ✗ |")
    L.append("| field 级 `coverage` | 本区 **%d** 个集「所有字段 coverage 全 0」（%d/%d） | ✗ |"
             % (s["coverage_metadata_blind_n"], s["coverage_metadata_blind_n"],
                s["datasets_pulled"]))
    L.append("| 字段目录 `count` | 有字段即为「有数据」 | ✓ |")
    L.append("")
    L.append("## 计数")
    L.append("")
    L.append("| status | 含义 | 集数 |")
    L.append("|---|---|---|")
    meaning = {
        "UNTESTED_BLIND": "★ 有字段 + coverage 元数据全 0 + 零回测证据 ⇒ 必须探针",
        "UNTESTED_COV_OK": "有字段且元数据说有用量，但零回测证据",
        "EVIDENCE_UNKNOWN": "证据通道不可用 ⇒ 既不能说挖过也不能说没挖过",
        "NO_FIELDS": "/data-fields 返回 0 字段（合法判死后备之一）",
        "NO_DATA": "★ 探针实测 longCount+shortCount = 0（合法判死后备之二）",
        "PROBE_FAILED": "探针仿真失败 ⇒ 仍是「不知道」，必须重跑（不许当成没数据）",
        "TESTED": "expressions 有回测记录 / code 匹配到该集字段",
        "LIT_EXCLUDED": "塔已点亮（规则性排除，与数据无关）",
        "UNVERIFIED": "字段拉取失败 ⇒ 不可下结论",
    }
    for k in sorted(res["counts"], key=lambda x: STATUS_ORDER.get(x, 9)):
        L.append("| `%s` | %s | %d |" % (k, meaning.get(k, ""), res["counts"][k]))
    L.append("")
    pool = [r for r in res["rows"] if r["lit_count"] < s["lit_threshold"]]
    pool_tested = [r for r in pool if r["status"] == "TESTED"]
    pool_untested = [r for r in pool if r["status"] in UNTESTED_STATUSES]
    L.append("## 未点亮塔池（可开采池）")
    L.append("")
    L.append("| 口径 | 集数 |")
    L.append("|---|---|")
    L.append("| 平台全量（D%d / %s） | %d |" % (res["delay"], s["universe"], len(res["rows"])))
    L.append("| 已点亮塔（规则性排除，不参与开采） | %d |" % (len(res["rows"]) - len(pool)))
    L.append("| **可开采池** | **%d** |" % len(pool))
    po_n = len(res.get("probe_only") or [])
    L.append("| 池内已挖掘（**本工具证据通道内**有记录） | %d |" % (len(pool_tested) - po_n))
    L.append("| 池内**有数据但本通道零记录**（探针已证有数据） | %d |" % po_n)
    L.append("| **池内真未探（有字段、零证据）** | **%d** |" % len(pool_untested))
    L.append("| 池内无字段（可判死） | %d |" % sum(1 for r in pool if r["status"] == "NO_FIELDS"))
    L.append("")
    po = res.get("probe_only") or []
    L.append("## ★ 有数据但本通道零记录（探针证明有数据 + 证据通道内无回测记录）")
    L.append("")
    L.append("这些集有探针数据背书，但在**本工具的『挖过没』证据源**里找不到任何回测记录。")
    L.append("★ 别直接读成「一次都没跑过」：MCP 直连仿真不进 ~expressions~ 表，本工具对它盲视；")
    L.append("下结论前先回波次日志核对，否则就是拿「我的台账里没有」冒充「没人跑过」。")
    L.append("")
    L.append("若核对后确实未开采，它们属容量未知区，不能与「已开采但没出东西」的集合并列"
             "用作「本区上限」的证据。")
    L.append("")
    if not po:
        L.append("（空）")
    else:
        L.append("| dataset | category | 探针字段 | longCount | 探针 alpha |")
        L.append("|---|---|---|---:|---|")
        for r in po:
            L.append("| `%s` | %s | `%s` | %s | `%s` |" % (
                r["dataset"], r["category"], r.get("probe_field"),
                r.get("probe_long_count"), r.get("probe_alpha_id")))
        L.append("")
        L.append("**共 %d 个集属于「有数据、本证据通道内零记录」**（口径见上，勿读成"
                 "「没跑过」）。" % len(po))
    L.append("")
    L.append("## ★ 真未探清单（有字段目录、零回测证据）")
    L.append("")
    un = [r for r in res["rows"] if r["status"] in UNTESTED_STATUSES]
    if not un:
        L.append("（空）")
    else:
        L.append("| dataset | category | valueScore | alphaCount | 字段数 | maxCov | 元数据盲区 | status |")
        L.append("|---|---|---|---|---|---|---|---|")
        for r in un:
            L.append("| `%s` | %s | %s | %s | %d/%s | %s | %s | `%s` |" % (
                r["dataset"], r["category"], r["value_score"], r["alpha_count"],
                r["fields_seen"], r["fields_platform_count"], r["max_field_cov"],
                "是" if r["cov_metadata_blind"] else "否", r["status"]))
    L.append("")
    if gates:
        L.append("## 门禁")
        L.append("")
        for g in gates:
            L.append("- `%s`：%s" % (g["gate"], "PASS" if g["ok"] else "FAIL"))
            if not g["ok"]:
                detail = {k: v for k, v in g.items() if k not in ("gate", "ok", "note")}
                L.append("  - `%s`" % json.dumps(detail, ensure_ascii=False)[:900])
        L.append("")
    return "\n".join(L).replace("~", chr(96)) + "\n"


# ----------------------------------------------------------------------------- 门：skill 文档里的「coverage 判死」措辞
# 根因 C：SOP 文本里一句「coverage < 0.6 ⇒ 永久剔除」就够让下一个 agent 重犯同一个错。
# 报告措辞门管「说出口的结论」，这道门管「写进 SOP 的筛选规则」——两者都必须可执行。
_COV_KILL_RE = re.compile(r"(?:\bcov(?:erage)?\b|覆盖率)\s*(?:<|<=|≤|小于)\s*0?\.\d+", re.I)
# 只认「指令性」判死动词：光出现 `UNUSABLE` 是历史分类记录（例如「UNUSABLE×20（cov<0.5 触顶）」），不是让人剔除的规则
_COV_KILL_WORD = re.compile(r"剔除|判死|直接排除|作废", re.I)
_COV_KILL_EXEMPT = re.compile(r"cov-aux-ok|已废止|废止|反例|不得|禁止|误判|不可判|已修|修正|不再", re.I)


def _norm_line(line):
    return re.sub(r"\s+", " ", line).strip()


def lint_skill_docs(paths=None):
    """扫 skill 文档：任何「cov/coverage < 阈值 ⇒ 剔除/判死」的筛选规则都算违规。

    豁免（同行命中任一即可）：
      - `cov-aux-ok` 显式声明「coverage 只作辅助标记」；
      - 反例/更正语境（已废止 / 反例 / 不得 / 禁止 / 误判 / 不可判 / 已修 / 修正 / 不再）。
    历史欠账登记在 tools/gates/_covskill_allow.json（{key: why}），key = "相对路径|规范化片段"。
    """
    roots = [os.path.abspath(p) for p in (paths or [SKILLS_ROOT])]
    allow = {}
    if os.path.isfile(COV_KILL_ALLOW):
        try:
            allow = json.load(open(COV_KILL_ALLOW, encoding="utf-8")).get("allow", {}) or {}
        except Exception as exc:                                   # noqa: BLE001
            return {"gate": "skill_cov_kill", "ok": False,
                    "error": "allow 文件解析失败: %s" % exc,
                    "note": "读不到豁免表时 fail-closed，不当作「没有违规」"}
    bad, allowed, scanned = [], [], 0
    for root in roots:
        if os.path.isfile(root):                                  # 允许直接传单个 .md
            files = [root]
        else:
            files = []
            for dirpath, _dirs, names in os.walk(root):
                files.extend(os.path.join(dirpath, n) for n in names if n.endswith(".md"))
        for p in sorted(files):
            scanned += 1
            rel = os.path.relpath(p, REPO_ROOT).replace("\\", "/")
            with open(p, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if not _COV_KILL_RE.search(line):
                        continue
                    if not _COV_KILL_WORD.search(line):
                        continue
                    if _COV_KILL_EXEMPT.search(line):
                        continue
                    snippet = _norm_line(line)[:120]
                    key = "%s|%s" % (rel, snippet[:80])
                    rec = {"file": rel, "line": i, "snippet": snippet}
                    if key in allow:
                        rec["why"] = allow[key]
                        allowed.append(rec)
                    else:
                        bad.append(rec)
    return {"gate": "skill_cov_kill", "ok": not bad, "scanned_files": scanned,
            "violations": bad, "allowed": allowed,
            "note": "coverage 三层都不可判存在性（techindi_model 数据集级 0.0 却有 399 字段、贡献本战役 10 席中的 2 席）；"
                    "写「cov<X ⇒ 剔除」的 SOP 必须改成「cov 只作辅助标记，判死走 --gate closure」，"
                    "或加 cov-aux-ok 标记。修好后请把 _covskill_allow.json 里的条目删掉。"}


def main(argv=None):
    ap = argparse.ArgumentParser(description="dataset coverage audit gate")
    ap.add_argument("--region", default=None, help="区域（--lint-report 单独使用时可不填）")
    ap.add_argument("--universe", default=None)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--lit-threshold", type=int, default=3,
                    help="category 已提交数达此值即视为塔已点亮（规则性排除）")
    ap.add_argument("--max-field-pages", type=int, default=2,
                    help="每集 field 抽查页数上限（50/页）；截断会被记录进 scope")
    ap.add_argument("--db", default=None, help="本地库路径（缺省 data/wqb.db）")
    ap.add_argument("--evidence-codes-file", default=None,
                    help="补充证据：一行一条 alpha 表达式（按字段名匹配）")
    ap.add_argument("--no-db-expressions", action="store_true",
                    help="不把 DB expressions 原文当证据（缺省开启：它覆盖 MCP 直连仿真）")
    ap.add_argument("--reuse-cache", default=None,
                    help="复用该审计 JSON 里已验过的 field 探针结果（只重算证据与状态）")
    ap.add_argument("--cache", default=None, help="审计 JSON 落盘路径")
    ap.add_argument("--md", default=None, help="审计 Markdown 落盘路径")
    ap.add_argument("--probe-plan", default=None,
                    help="把「必须探针」的集清单落盘（JSON）")
    ap.add_argument("--probe-results", default=None,
                    help="探针执行器产物（{results:{dataset:{data_present,long_count,...}}}）；"
                         "回灌后 UNTESTED_BLIND -> TESTED / NO_DATA，closure 门才有机会过")
    ap.add_argument("--waivers", default=None,
                    help="JSON: {dataset: {reason, date}} —— 显式豁免（有日期有理由才认）")
    ap.add_argument("--gate", choices=["none", "coverage", "closure", "probe", "both"],
                    default="none")
    ap.add_argument("--lint-report", nargs="*", default=None,
                    help="扫描报告里无限定的穷尽类断言（根因 B 的措辞门）")
    ap.add_argument("--lint-skills", nargs="*", default=None,
                    help="扫描 skill 文档里「cov<X ⇒ 剔除/判死」的筛选规则（根因 C：SOP 文本级措辞门）；不带路径默认扫 Claude/skills")
    ap.add_argument("--json", action="store_true", help="stdout 打完整 JSON")
    args = ap.parse_args(argv)

    waivers = {}
    if args.waivers and os.path.exists(args.waivers):
        waivers = json.load(open(args.waivers, encoding="utf-8")) or {}

    if args.lint_skills is not None:
        out = lint_skill_docs(args.lint_skills or None)
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0 if out["ok"] else 1

    lint = lint_report(args.lint_report) if args.lint_report else None
    if args.gate == "none" and lint is not None:
        print(json.dumps(lint, ensure_ascii=False, indent=1))
        return 0 if lint["ok"] else 1

    if not args.region or not args.universe:
        ap.error("--region / --universe 在跑审计或门禁时必填")

    res = audit(args.region, args.universe, args.delay, args.lit_threshold,
                args.max_field_pages, db_path=args.db,
                evidence_codes_file=args.evidence_codes_file,
                reuse_cache=args.reuse_cache,
                use_db_expressions=not args.no_db_expressions,
                probe_results=args.probe_results)
    if not res.get("ok", True):
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 2

    gates = []
    if args.gate in ("coverage", "both"):
        gates.append(gate_coverage(res, waivers))
    if args.gate in ("closure", "both"):
        gates.append(gate_closure(res, waivers))
    if args.gate == "probe":
        gates.append(gate_probe(res, waivers))

    if args.cache:
        os.makedirs(os.path.dirname(os.path.abspath(args.cache)), exist_ok=True)
        with open(args.cache, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
    if args.md:
        os.makedirs(os.path.dirname(os.path.abspath(args.md)), exist_ok=True)
        open(args.md, "w", encoding="utf-8").write(render_md(res, gates))
    if args.probe_plan:
        plan = gate_probe(res, waivers)["probe_needed"]
        os.makedirs(os.path.dirname(os.path.abspath(args.probe_plan)), exist_ok=True)
        with open(args.probe_plan, "w", encoding="utf-8") as f:
            json.dump({"generated_at": _now(), "region": args.region,
                       "universe": args.universe, "delay": args.delay,
                       "probe_needed": plan}, f, ensure_ascii=False, indent=1)

    summary = {
        "region": args.region, "delay": args.delay, "universe": args.universe,
        "scope": res["scope"], "counts": res["counts"],
        "gates": gates, "report_lint": lint,
        "untested": [r["dataset"] for r in res["rows"]
                     if r["status"] in UNTESTED_STATUSES],
    }
    print(json.dumps(res if args.json else summary, ensure_ascii=False, indent=1))
    if lint is not None and not lint["ok"]:
        return 1
    return 0 if all(g["ok"] for g in gates) else 1


if __name__ == "__main__":
    sys.exit(main())
