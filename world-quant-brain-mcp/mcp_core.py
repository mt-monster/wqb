"""mcp_core — MCP 服务核心 (2026-08-13 自 main.py 拆分, P2 工具层按域拆分).

持有: FastMCP 实例 (mcp) + 响应瘦身辅助 (_slim_*) + 健康检查路由 + save_config。
工具模块 (tools_*.py) 统一 `from mcp_core import mcp, brain_client, ...`。
"""
import json, re, os, sys, logging
from typing import Dict, List, Optional, Any, Union

from mcp.server.fastmcp import FastMCP, Context
from starlette.responses import JSONResponse

from brain_api import brain_client, load_config, _resolve_config_path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("mcp_core")


def save_config(config: Dict[str, Any]):
    """Save configuration to file using the resolved config path.
    
    This function now uses the write-enabled path resolver to handle
    cases where the default home directory is not writable.
    """
    config_file = _resolve_config_path(for_write=True)
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        logger.error(f"Error saving config file to {config_file}: {e}")


_MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
try:
    _MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
except Exception:
    _MCP_PORT = 8000
_MCP_STREAMABLE_HTTP_PATH = os.getenv("MCP_STREAMABLE_HTTP_PATH", "/mcp")

mcp = FastMCP(
    "brain-platform-mcp",
    "A server for interacting with the WorldQuant BRAIN platform",
    host=_MCP_HOST,
    port=_MCP_PORT,
    streamable_http_path=_MCP_STREAMABLE_HTTP_PATH,
)

# Add health check endpoint for container monitoring
from mcp.server.fastmcp import Context
from starlette.responses import JSONResponse


@mcp.custom_route('/health', methods=['GET'])
async def health_check(context: Context):
    """Health check endpoint for Docker container monitoring."""
    return JSONResponse({
        "status": "healthy",
        "service": "brain-platform-mcp",
        "timestamp": datetime.utcnow().isoformat(),
        "redis_connected": brain_client.redis_client is not None
    })

# ============================================================================
# Response-slimming helpers
# ----------------------------------------------------------------------------
# Keep MCP tool outputs compact so long agent sessions (and any hook /
# transcript evaluators that re-read the conversation) don't blow the context
# window. These ONLY strip noise: fixed help strings, null sub-objects,
# redundant repeated fields, oversized free text, and full daily PnL series.
# The essential ids / metrics / checks / pyramid info are preserved (often in a
# clearer shape). Every helper is defensive: on an unexpected shape or an
# {"error": ...} payload it returns the input unchanged.
# ============================================================================

_RA_2Y_NAMES = ("LOW_2Y_SHARPE", "IS_LADDER_SHARPE")

# WebDataScope-0.10.20/src/scripts/background.js :: getAlphaCheckStates — canonical RA / PPA check names.
_RA_CHECK_NAMES = frozenset([
    "HIGH_TURNOVER", "LOW_TURNOVER", "LOW_FITNESS", "LOW_RETURNS", "LOW_SHARPE",
    "LOW_GLB_AMER_SHARPE", "LOW_GLB_APAC_SHARPE", "LOW_GLB_EMEA_SHARPE", "LOW_ASI_JPN_SHARPE",
    "IS_LADDER_SHARPE",  # ATOM-exempt but still counted in the RA gate
    "LOW_2Y_SHARPE", "LOW_SUB_UNIVERSE_SHARPE", "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_AFTER_COST_ILLIQUID_UNIVERSE_SHARPE", "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
    "LOW_ROBUST_UNIVERSE_RETURNS", "CONCENTRATED_WEIGHT",
])
_PPA_CHECK_NAMES = frozenset([
    "LOW_TURNOVER", "HIGH_TURNOVER", "LOW_SUB_UNIVERSE_SHARPE", "LOW_ROBUST_UNIVERSE_SHARPE",
    "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO", "LOW_ROBUST_UNIVERSE_RETURNS",
    "LOW_INVESTABILITY_CONSTRAINED_SHARPE",
])


def _ra_bad(result):
    # WebDataScope rule: a check counts as failing the RA/PPA gate iff result != "PASS" and result != "PENDING"
    return result != "PASS" and result != "PENDING"


def _truncate(s, n=160):
    if not isinstance(s, str):
        return s
    s2 = s.strip()
    return s2 if len(s2) <= n else s2[:n].rstrip() + "…"


def _unwrap_result(obj):
    """brain_client methods usually return {"result": <payload>}; some return the payload directly."""
    if isinstance(obj, dict) and list(obj.keys()) == ["result"]:
        return obj["result"], True
    return obj, False


def _rewrap(payload, was_wrapped):
    return {"result": payload} if was_wrapped else payload


def _is_error(payload):
    return isinstance(payload, dict) and "error" in payload


def _slim_checks(checks):
    """Compress an is.checks[] array into fail/warning/pass/pending buckets + pyramid info + headline values
    + precomputed RA/PPA failure counts (WebDataScope getAlphaCheckStates). Returns (buckets, pyramids, extracted, ra)."""
    out = {"fail": [], "warning": [], "pass": [], "pending": []}
    pyramids = None
    extracted = {}
    rename = {"LOW_ROBUST_UNIVERSE_SHARPE": "robust_universe_sharpe",
              "LOW_SUB_UNIVERSE_SHARPE": "sub_universe_sharpe"}
    failed_ra = 0
    failed_ppa = 0
    ra_failed_names = []
    ppa_failed_names = []
    for c in checks or []:
        if not isinstance(c, dict):
            continue
        name = c.get("name")
        res = c.get("result")
        val = c.get("value")
        if name == "MATCHES_PYRAMID":
            pyramids = {"effective": c.get("effective"),
                        "list": [{"name": p.get("name"), "multiplier": p.get("multiplier")}
                                 for p in (c.get("pyramids") or []) if isinstance(p, dict)]}
        if name in rename and val is not None:
            extracted[rename[name]] = val
        if name in _RA_2Y_NAMES and val is not None:
            extracted["two_year_sharpe"] = val
            if c.get("year") is not None:
                extracted["two_year_ladder_window"] = c.get("year")
        # --- RA / PPA failure counting (verbatim port of background.js getAlphaCheckStates) ---
        if name in _RA_CHECK_NAMES and _ra_bad(res):
            failed_ra += 1
            ra_failed_names.append(name)
        if (name in _PPA_CHECK_NAMES and _ra_bad(res)) or (name == "LOW_SHARPE" and isinstance(val, (int, float)) and val < 1):
            failed_ppa += 1
            ppa_failed_names.append(name)
        # --- buckets ---
        if res == "FAIL":
            out["fail"].append({k: c.get(k) for k in ("name", "value", "limit", "year", "message", "date")
                                if c.get(k) is not None})
        elif res == "WARNING":
            d = {k: c.get(k) for k in ("name", "value", "limit", "year", "message") if c.get(k) is not None}
            out["warning"].append(d if d else {"name": name})
        elif res == "PENDING":
            out["pending"].append(name)
        elif res in (None, "PASS", "OK"):
            out["pass"].append(name)
        else:
            out["pass"].append(f"{name}:{res}")
    ra = {"failed_ra_count": failed_ra, "failed_ppa_count": failed_ppa,
          "ra_failed": failed_ra > 0, "ppa_failed": failed_ppa > 0}
    if ra_failed_names:
        ra["ra_failed_checks"] = ra_failed_names
    if ppa_failed_names:
        ra["ppa_failed_checks"] = ppa_failed_names
    if pyramids and pyramids.get("list"):
        # WQPPYS: the pyramid leaf names joined, e.g. "sentiment/analyst"
        ra["pyramid_short"] = "/".join((p.get("name") or "").split("/")[-1].lower()
                                       for p in pyramids["list"] if p.get("name"))
    return out, pyramids, extracted, ra


def _slim_alpha(a):
    """Reduce a full alpha object to id / code / settings / key-metrics / checks / pyramids."""
    if not isinstance(a, dict):
        return a
    isd = a.get("is") or {}
    inv = isd.get("investabilityConstrained") or {}
    rn = isd.get("riskNeutralized") or {}
    checks, pyramids, extracted, ra = _slim_checks(isd.get("checks"))
    metrics = {k: isd.get(k) for k in ("sharpe", "fitness", "turnover", "returns", "drawdown",
                                       "margin", "longCount", "shortCount", "pnl", "bookSize", "startDate",
                                       "sharpe_se", "sharpe_t_stat", "selfCorrelation", "prodCorrelation")
               if isd.get(k) is not None}
    # also keep any other small scalar metric the platform may add later (excludes the big sub-dicts/checks)
    for k, v in isd.items():
        if k not in metrics and k not in ("checks", "investabilityConstrained", "riskNeutralized") and isinstance(v, (int, float)):
            metrics[k] = v
    metrics.update(extracted)
    if inv.get("sharpe") is not None:
        metrics["investability_sharpe"] = inv.get("sharpe")
        if inv.get("fitness") is not None:
            metrics["investability_fitness"] = inv.get("fitness")
    if rn.get("sharpe") is not None:
        metrics["risk_neutralized_sharpe"] = rn.get("sharpe")
    reg = a.get("regular")
    code = reg.get("code") if isinstance(reg, dict) else reg
    out = {
        "id": a.get("id"),
        "code": code,
        "status": a.get("status"),
        "stage": a.get("stage"),
        "dateSubmitted": a.get("dateSubmitted"),
        "settings": a.get("settings"),
        "metrics": metrics or None,
        "ra": ra,                 # precomputed Failed RA / Failed PPA (WebDataScope getAlphaCheckStates) — read this instead of recounting checks
        "checks": checks,
        "pyramids": pyramids,
    }
    for k in ("name", "color", "tags"):
        v = a.get(k)
        if v not in (None, "", []):
            out[k] = v
    return {k: v for k, v in out.items() if v is not None}


def _slim_alpha_response(obj):
    payload, w = _unwrap_result(obj)
    if _is_error(payload) or not isinstance(payload, dict):
        return obj
    return _rewrap(_slim_alpha(payload), w)


def _slim_alpha_list(obj):
    payload, w = _unwrap_result(obj)
    if not isinstance(payload, dict) or "results" not in payload:
        return obj
    out = {k: v for k, v in payload.items() if k != "results"}
    out["results"] = [_slim_alpha(a) if isinstance(a, dict) else a for a in payload.get("results", [])]
    return _rewrap(out, w)


def _slim_multisim(obj):
    payload, w = _unwrap_result(obj)
    if not isinstance(payload, dict) or "alpha_results" not in payload:
        return obj
    new_results = []
    for r in payload.get("alpha_results", []):
        if isinstance(r, dict) and isinstance(r.get("details"), dict):
            d = r["details"]
            if list(d.keys()) == ["result"]:
                d = d["result"]
            slim = _slim_alpha(d)
            new_results.append({"alpha_id": r.get("alpha_id"), "location": r.get("location"), **slim})
        else:
            new_results.append(r)
    out = {k: payload.get(k) for k in ("success", "message", "total_requested", "total_created",
                                       "multisimulation_id") if k in payload}
    out["alpha_results"] = new_results
    return _rewrap(out, w)


def _slim_datafields(obj):
    payload, w = _unwrap_result(obj)
    if not isinstance(payload, dict) or "results" not in payload:
        return obj
    fields = []
    for f in payload.get("results", []):
        if not isinstance(f, dict):
            fields.append(f)
            continue
        fields.append({"id": f.get("id"), "type": f.get("type"), "coverage": f.get("coverage"),
                       "userCount": f.get("userCount"), "alphaCount": f.get("alphaCount"),
                       "description": _truncate(f.get("description"), 160)})
    out = {"results": fields, "count": payload.get("count")}
    for k in ("sharpe_filter_applied", "sharpe_filter_removed"):
        if k in payload:
            out[k] = payload[k]
    return _rewrap(out, w)


def _slim_datasets(obj):
    payload, w = _unwrap_result(obj)
    if not isinstance(payload, dict) or "results" not in payload:
        return obj
    ds = []
    for d in payload.get("results", []):
        if not isinstance(d, dict):
            ds.append(d)
            continue
        cat = d.get("category")
        ds.append({"id": d.get("id"), "name": d.get("name"),
                   "category": cat.get("id") if isinstance(cat, dict) else cat,
                   "coverage": d.get("coverage"), "fieldCount": d.get("fieldCount"),
                   "userCount": d.get("userCount"), "alphaCount": d.get("alphaCount"),
                   "valueScore": d.get("valueScore"), "pyramidMultiplier": d.get("pyramidMultiplier"),
                   "description": _truncate(d.get("description"), 200)})
    return _rewrap({"results": ds, "count": payload.get("count")}, w)


def _records_to_dicts(payload):
    schema = payload.get("schema") or {}
    props = [p.get("name") for p in (schema.get("properties") or []) if isinstance(p, dict)]
    recs = payload.get("records") or []
    if props and recs and isinstance(recs[0], list):
        return [dict(zip(props, r)) for r in recs]
    return recs


def _slim_yearly(obj):
    payload, w = _unwrap_result(obj)
    if not isinstance(payload, dict) or "records" not in payload:
        return obj
    return _rewrap({"records": _records_to_dicts(payload)}, w)


def _slim_pnl(obj, max_rows=160):
    payload, w = _unwrap_result(obj)
    if not isinstance(payload, dict) or "records" not in payload:
        return obj
    schema = payload.get("schema") or {}
    props = [p.get("name") for p in (schema.get("properties") or []) if isinstance(p, dict)]
    recs = payload.get("records") or []
    n = len(recs)
    kept = recs
    if n > max_rows:
        stride = max(1, n // max_rows)
        kept = recs[::stride]
        if kept and recs and kept[-1] is not recs[-1]:
            kept = kept + [recs[-1]]
    out = {"properties": props, "records": kept, "num_records_original": n,
           "downsampled": len(kept) != n}
    return _rewrap(out, w)


def _slim_correlation_block(b):
    if not isinstance(b, dict):
        return b
    out = {}
    for k in ("max_correlation", "passes_check"):
        if k in b:
            out[k] = b[k]
    cd = b.get("correlation_data") or {}
    recs = cd.get("records")
    if isinstance(recs, list) and recs and isinstance(recs[0], list) and len(recs[0]) >= 3:
        out["histogram_nonzero"] = [{"range": [r[0], r[1]], "n": r[2]} for r in recs if len(r) >= 3 and r[2]]
        for k in ("max", "min"):
            if cd.get(k) is not None:
                out[k] = cd.get(k)
    elif isinstance(recs, list) and recs and isinstance(recs[0], dict):
        out["top_correlated"] = recs[:5]
        if cd.get("pool_size") is not None:
            out["pool_size"] = cd.get("pool_size")
    # Surface the Self/PowerPool pool-partition metadata (local self-correlation).
    for k in ("correlation_type", "full_os_pool_size", "excluded_power_pool_count", "ppac_ids_cached"):
        if cd.get(k) is not None:
            out[k] = cd.get(k)
    return out


def _slim_check_correlation(obj):
    payload, w = _unwrap_result(obj)
    if _is_error(payload) or not isinstance(payload, dict):
        return obj
    # check_self_correlation top-level shape: {alpha_id, threshold, max_correlation, passes_check, correlation_data, ...}
    if "max_correlation" in payload and "checks" not in payload:
        out = {k: payload.get(k) for k in ("alpha_id", "threshold", "correlation_type", "passes_check", "local_calculation")
               if k in payload}
        out.update(_slim_correlation_block(payload))
        return _rewrap(out, w)
    # check_correlation shape: {alpha_id, threshold, correlation_type, checks: {production:{...}, self:{...}}, all_passed}
    out = {k: payload.get(k) for k in ("alpha_id", "threshold", "correlation_type") if k in payload}
    checks = payload.get("checks")
    if isinstance(checks, dict):
        out["checks"] = {k: _slim_correlation_block(v) for k, v in checks.items()}
    if "all_passed" in payload:
        out["all_passed"] = payload["all_passed"]
    return _rewrap(out, w)


def _slim_pyramids(obj, kind):
    """kind: 'alphas' -> alphaCount, 'multipliers' -> multiplier. Reshape list to {region: {Dn: {cat: val}}}."""
    payload, w = _unwrap_result(obj)
    if not isinstance(payload, dict) or "pyramids" not in payload:
        return obj
    val_key = "alphaCount" if kind == "alphas" else "multiplier"
    nested = {}
    for p in payload.get("pyramids", []):
        if not isinstance(p, dict):
            continue
        cat = p.get("category")
        cat_id = cat.get("id") if isinstance(cat, dict) else cat
        nested.setdefault(p.get("region"), {}).setdefault(f"D{p.get('delay')}", {})[cat_id] = p.get(val_key)
    return _rewrap({"pyramids": nested}, w)


def _slim_text_lookup(obj, fields=("description", "content"), n=4000):
    """Recursively truncate big free-text / raw fields in nested responses (operators, docs, lookINTO, ...)."""
    trunc_keys = set(fields) | {"raw"}
    def fix(o):
        if isinstance(o, dict):
            r = {}
            for k, v in o.items():
                if k in trunc_keys and isinstance(v, str):
                    r[k] = _truncate(v, n)
                else:
                    r[k] = fix(v)
            return r
        if isinstance(o, list):
            return [fix(x) for x in o]
        return o
    return fix(obj)
