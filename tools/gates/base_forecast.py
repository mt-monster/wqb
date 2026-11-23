#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""base_forecast.py — 每日提交件的 base 预估 + VF 提交前后（全 MCP 取数）。

## ⛔ 口径警告（2026-11-22 用户实测纠正，最优先）

**本工具是 RA（REGULAR）base 模型，禁止用于估 SuperAlpha 的 base。**

- 标定目标 = `get_daily_and_quarterly_payment()['base_payments']` 的日序列（91 天均值 ~$1.7）。
- 该字段是 **RA 口径**：实证 2026-11-20 平台值 **$2.72** == 用户当日 **RA base**（精确一致），
  而用户当日 **SA base = $3.78** 完全不在这条序列里。
- ⇒ 任何「SA 能拿多少 base」的问题，**本工具的输出都无效**。SA base 另建台账
  （`tracking/SA_BASE/` 的 `sa_base_usd` 字段），单颗经验值 ≈ **$0.065/天**（58 颗 → $3.78/天）。
- 即便对 RA，本模型在 2026-11-20 也低估 37%（预测 $1.73 vs 实际 $2.72，约 4σ）⇒
  **输出只可用于同日多候选的相对排序，不可当绝对报价。**

## 这份工具能算什么、不能算什么（先读）

平台**没有公开** base payment 的解析公式。官方只公开三类"输入/输出"：

| 类别 | 字段 | 取法 |
|---|---|---|
| 输入·乘数 | pyramid 倍率（region×delay×数据集类别） | `get_alpha_details().pyramids` / `get_pyramid_multipliers` |
| 输入·乘数 | theme 倍率（当期主题） | `submit_verdict().sim_warnings[MATCHES_THEMES].themes[].multiplier` |
| 输入·档位 | Value Factor / Osmosis Rank | `get_leaderboard(valueFactor, dailyOsmosisRank)` |
| 输入·质量 | S / F / Turnover / prodCorrelation | `get_alpha_details().metrics` |
| 输出 | 每日 base 到账（**RA only**） | `get_daily_and_quarterly_payment()` |
| 代理 | 多样性分（VF 趋势） | `value_factor_trendScore()` |

⇒ 本工具做三件事，并把"确定 / 不确定"分开标：

1. **乘数链精确复算（确定）**：`理论乘数 = (theme + pyramid − 1) × (1 + OsmosisRank)`。
   三项全部来自平台字段，可逐位复现。（乘数链对 RA/SA 都成立，**金额不行**。）
2. **base 经验模型（不确定，用本账户历史标定，仅 RA）**：
   `log(base_day) = b0 + b1·log(1+n) + b2·mean_pc + b3·is_low_pc + b4·log1p(max_F)
   + b5·log1p(mean_S) + b6·mean_mult`
   系数由本账户最近 N 天「当日提交件特征 ↔ 当日 base 到账」OLS 拟合，**各账户不同，不可跨账户搬运**。
   输出带残差 sd 区间；R² 低于 0.3 时只能用于排序，不能用于报价。
3. **VF 提交前后（半确定）**：恒等式 `diversity_score=(A/N)×(P/216)×S_H` 算 ΔP 的方向与幅度；
   `A` 口径未知 ⇒ 给上下界。**diversity_score 只是 VF 的趋势代理，不是 VF 本体**。

## 用法

    python tools/gates/base_forecast.py --calibrate --days 120
    python tools/gates/base_forecast.py --date 2026-11-21
    python tools/gates/base_forecast.py --alpha VkNzob9G,0mPPVEoK
    python tools/gates/base_forecast.py --date 2026-11-21 --vf-only
    python tools/gates/base_forecast.py --date 2026-11-21 --json output_report/base_20261121.json

退出码：0 正常；2 数据不足（无法标定 / 未取到 alpha）；3 参数错。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

CACHE_DIR = os.path.join(_REPO, "cache")
CALIB_FILE = os.path.join(CACHE_DIR, "base_forecast_calib.json")
P_MAX = 216
BASE_CAP_REGULAR = 60.0   # 论坛口径：REGULAR 日 base 上限 $60

FEATURES = ["log1p_n", "mean_pc", "is_low_pc", "log1p_maxF", "log1p_meanS", "mean_mult"]
#: SA 特征：**实测无效**（Adj-R² 0.514→0.519、AIC −440→−438）⇒ 默认不进模型，
#: 只保留 `--with-sa` 供复核。SA 那部分 base 不可由 SA 的 IS 指标解释。
SUPER_FEATURES = ["sa_n", "log1p_sa_maxF", "log1p_sa_maxS", "log1p_sa_maxPC"]


# ------------------------------------------------------------------ MCP
def _client():
    from tools.lib import forum_mcp as FM
    return FM.client()


def _mcp(cli, tool: str, args: Dict[str, Any]) -> Any:
    return cli.call_tool(tool, args)


def _num(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ 取数
def fetch_base_history(cli) -> Dict[str, float]:
    d = _mcp(cli, "get_daily_and_quarterly_payment", {})
    out: Dict[str, float] = {}
    recs = ((((d or {}).get("base_payments") or {}).get("records") or {}).get("records")) or []
    for r in recs:
        if isinstance(r, (list, tuple)) and len(r) >= 2:
            v = _num(r[1])
            if v is not None:
                out[str(r[0])[:10]] = v
    return out


def fetch_submissions(cli, start: str, end: str, max_pages: int = 6) -> List[Dict[str, Any]]:
    """取窗口内已提交的 REGULAR alpha（OS 阶段），带 metrics/pyramids。"""
    out: List[Dict[str, Any]] = []
    for page in range(max_pages):
        d = _mcp(cli, "get_user_alphas", {
            "stage": "OS", "type": "REGULAR", "limit": 100, "offset": page * 100,
            "order": "-dateSubmitted",
            "submission_start_date": f"{start}T00:00:00-05:00",
            "submission_end_date": f"{end}T23:59:59-05:00",
        })
        res = (d or {}).get("results") or []
        if not res:
            break
        out.extend(res)
        if len(res) < 100:
            break
    return out


def fetch_supers(cli, start: str, end: str, max_pages: int = 4) -> List[Dict[str, Any]]:
    """取窗口内已提交的 SUPER alpha（只留预测需要的字段）。"""
    out: List[Dict[str, Any]] = []
    for page in range(max_pages):
        d = _mcp(cli, "get_user_alphas", {
            "stage": "OS", "type": "SUPER", "limit": 100, "offset": page * 100,
            "order": "-dateSubmitted",
            "submission_start_date": f"{start}T00:00:00-05:00",
            "submission_end_date": f"{end}T23:59:59-05:00",
        })
        res = (d or {}).get("results") or []
        out.extend(res)
        if len(res) < 100:
            break
    return out


def fetch_vf(cli, days: int = 30, end_date: Optional[str] = None) -> Dict[str, Any]:
    """多样性分窗口。``end_date`` 给定时用该日 23:59 收口（用于取「提交前」的真前值）。"""
    if end_date:
        end = _dt.datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=_dt.timezone.utc)
    else:
        end = _dt.datetime.now(_dt.timezone.utc)
    start = end - _dt.timedelta(days=days)
    d = _mcp(cli, "value_factor_trendScore", {
        "start_date": start.strftime("%Y-%m-%dT00:00:00Z"),
        "end_date": end.strftime("%Y-%m-%dT23:59:59Z"),
    })
    return d if isinstance(d, dict) else {}


def fetch_leaderboard(cli, user_id: str = "MT38799") -> Dict[str, Any]:
    d = _mcp(cli, "get_leaderboard", {"user_id": user_id})
    res = (d or {}).get("results") or []
    return res[0] if res else {}


def fetch_pyramid_multipliers(cli) -> Dict[str, Any]:
    d = _mcp(cli, "get_pyramid_multipliers", {})
    return (d or {}).get("pyramids") or {}


def fetch_theme_mult(cli, alpha_id: str) -> Tuple[float, List[Dict[str, Any]]]:
    """theme 候选清单（**注意：这是 checks 里列出的主题，不全是命中项**）。

    真正的"是否命中"要看 `checks.pass` 是否含 `MATCHES_THEMES`（见 ``theme_status``）；
    `pending` = 平台尚未评，`warning` = 未命中。旧记录里"×3.89"那次是把列表项当命中项，
    已在本工具里拆开处理。
    """
    d = _mcp(cli, "submit_verdict", {"alpha_id": alpha_id})
    themes: List[Dict[str, Any]] = []
    for w in ((d or {}).get("sim_warnings") or []):
        if isinstance(w, dict) and w.get("name") == "MATCHES_THEMES":
            themes = w.get("themes") or []
    mult = max([_num(t.get("multiplier")) or 1.0 for t in themes], default=1.0)
    return mult, themes


def theme_status(alpha: Dict[str, Any]) -> str:
    """从 checks 三桶判 MATCHES_THEMES 的真实状态。"""
    chk = alpha.get("checks") or {}
    names = lambda v: [x.get("name") if isinstance(x, dict) else x for x in (v or [])]
    if "MATCHES_THEMES" in names(chk.get("pass")):
        return "MATCHED"
    if "MATCHES_THEMES" in names(chk.get("pending")):
        return "PENDING"
    if "MATCHES_THEMES" in names(chk.get("warning")):
        return "WARNING"
    if "MATCHES_THEMES" in names(chk.get("fail")):
        return "FAIL"
    return "ABSENT"


def _theme_region(name: str) -> str:
    head = str(name).split("/")[0].strip().upper()
    if head.startswith("ALL REGION"):
        return "ALL"
    return head


def resolve_theme(alpha: Dict[str, Any], themes: List[Dict[str, Any]]
                  ) -> Tuple[float, bool, Optional[str], List[Dict[str, Any]]]:
    """返回 (可用倍率, 是否未定, 说明, 可归属主题)。

    只有主题名首段与本件 region 相容（同区 / All Regions；GLB 仅 GLB 件）
    才计入，避免把"被检查过但未命中"的条目当成收益。
    """
    st = alpha.get("settings") or {}
    region = str(st.get("region") or "").upper()
    ok = []
    for t in themes:
        if not isinstance(t, dict):
            continue
        tr = _theme_region(t.get("name") or "")
        if tr == region or tr == "ALL":
            ok.append(t)
    if ok:
        return max([_num(t.get("multiplier")) or 1.0 for t in ok]), False, None, ok
    status = theme_status(alpha)
    if status == "MATCHED":
        return 1.0, True, "平台判命中，但清单里没有可归属到本区的倍率 ⇒ 点估计取 1.0，上界按 ×2.0 放宽", []
    return 1.0, False, f"theme {status}（未命中/未评）", []


# ------------------------------------------------------------------ 乘数
def pyramid_terms(alpha: Dict[str, Any], pmap: Dict[str, Any]) -> Tuple[Optional[float], List[str], str]:
    """返回 (生效 pyramid 倍率, 类别名列表, 来源)。

    木桶规则：命中 ≥3 类计 0；否则取最小倍率。
    """
    names: List[str] = []
    mults: List[float] = []
    pys = alpha.get("pyramids") or {}
    for p in ((pys.get("list") or []) if isinstance(pys, dict) else []):
        if isinstance(p, dict) and p.get("name"):
            names.append(str(p["name"]).split("/")[-1])
            m = _num(p.get("multiplier"))
            if m is not None:
                mults.append(m)
    src = "platform"
    if not mults:
        short = ((alpha.get("ra") or {}).get("pyramid_short") or "").strip()
        st = alpha.get("settings") or {}
        region, delay = st.get("region"), st.get("delay")
        if short and region and delay is not None:
            table = ((pmap.get(region) or {}).get(f"D{delay}") or {})
            for cat in [c for c in short.split("/") if c]:
                m = _num(table.get(c.lower()))
                if m is not None:
                    names.append(c)
                    mults.append(m)
            src = "ra.pyramid_short×multiplier_table" if mults else "none"
    if not mults:
        return None, names, "unknown"
    if len(set(names)) >= 3:
        return 0.0, names, src + "/>=3cats→0"
    return min(mults), names, src


def multiplier_chain(theme_mult: float, pyr_mult: Optional[float], os_rank: float) -> Dict[str, Any]:
    pyr = 1.0 if pyr_mult is None else pyr_mult
    combined = theme_mult + pyr - 1.0
    total = combined * (1.0 + os_rank)
    return {
        "theme_mult": theme_mult, "pyramid_mult": pyr_mult, "pyramid_used": pyr,
        "combined_mult": combined, "os_mult": 1.0 + os_rank, "total_mult": total,
    }


# ------------------------------------------------------------------ 标定（纯 python OLS）
def _solve(a: List[List[float]], b: List[float]) -> Optional[List[float]]:
    n = len(a)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(m[r][i]))
        if abs(m[p][i]) < 1e-12:
            return None
        m[i], m[p] = m[p], m[i]
        piv = m[i][i]
        for j in range(i, n + 1):
            m[i][j] /= piv
        for r in range(n):
            if r == i:
                continue
            f = m[r][i]
            if f:
                for j in range(i, n + 1):
                    m[r][j] -= f * m[i][j]
    return [m[i][n] for i in range(n)]


def ols(X: List[List[float]], y: List[float]) -> Dict[str, Any]:
    k = len(X[0])
    XtX = [[sum(X[i][p] * X[i][q] for i in range(len(X))) for q in range(k)] for p in range(k)]
    Xty = [sum(X[i][p] * y[i] for i in range(len(X))) for p in range(k)]
    beta = _solve(XtX, Xty)
    if beta is None:
        return {"ok": False, "reason": "设计矩阵奇异（样本不足或特征共线）"}
    pred = [sum(beta[p] * row[p] for p in range(k)) for row in X]
    resid = [y[i] - pred[i] for i in range(len(y))]
    sse = sum(r * r for r in resid)
    ybar = sum(y) / len(y)
    sst = sum((v - ybar) ** 2 for v in y)
    r2 = 1 - sse / sst if sst else 0.0
    sd = math.sqrt(sse / max(len(y) - k, 1))
    # 系数标准误 / t 值（用于判「这一项到底能不能用来预测」）
    dof = max(len(y) - k, 1)
    s2 = sse / dof
    se: List[float] = []
    tvals: List[float] = []
    for j in range(k):
        e = [1.0 if i == j else 0.0 for i in range(k)]
        col = _solve([row[:] for row in XtX], e)
        v = math.sqrt(s2 * col[j]) if col and col[j] > 0 else float("nan")
        se.append(v)
        tvals.append(beta[j] / v if v and v == v else float("nan"))
    return {"ok": True, "beta": beta, "r2": r2, "resid_sd": sd, "n": len(y), "k": k,
            "se": se, "t": tvals}


def day_features(alphas: List[Dict[str, Any]], pmap: Dict[str, Any], os_rank: float,
                 supers: Optional[List[Dict[str, Any]]] = None) -> Dict[str, float]:
    n = len(alphas)
    supers = supers or []
    pcs, fs, ss, mults = [], [], [], []
    for a in alphas:
        m = a.get("metrics") or {}
        pc, f, s = _num(m.get("prodCorrelation")), _num(m.get("fitness")), _num(m.get("sharpe"))
        if pc is not None:
            pcs.append(pc)
        if f is not None:
            fs.append(f)
        if s is not None:
            ss.append(s)
        pm, _, _ = pyramid_terms(a, pmap)
        mults.append((1.0 if pm is None else pm) * (1.0 + os_rank))
    mean = lambda v: sum(v) / len(v) if v else 0.0
    return {
        "n": n,
        "log1p_n": math.log1p(n),
        "mean_pc": mean(pcs),
        "is_low_pc": 1.0 if pcs and mean(pcs) < 0.25 else 0.0,
        "log1p_maxF": math.log1p(max(fs) if fs else 0.0),
        "log1p_meanS": math.log1p(mean(ss)),
        "mean_mult": mean(mults),
        **_super_block(supers),
    }


def _super_block(supers: List[Dict[str, Any]]) -> Dict[str, float]:
    """当日 SA 的质量块。无 SA ⇒ 全 0（log1p(0)=0，等价于「这天没交 SA」）。"""
    fs, ss, pcs = [], [], []
    for a in supers:
        m = a.get("metrics") or {}
        f, sh, pc = _num(m.get("fitness")), _num(m.get("sharpe")), _num(m.get("prodCorrelation"))
        if f is not None:
            fs.append(f)
        if sh is not None:
            ss.append(sh)
        if pc is not None:
            pcs.append(pc)
    return {
        "sa_n": float(len(supers)),
        "log1p_sa_maxF": math.log1p(max(fs) if fs else 0.0),
        "log1p_sa_maxS": math.log1p(max(ss) if ss else 0.0),
        "log1p_sa_maxPC": math.log1p(max(pcs) if pcs else 0.0),
    }


def calibrate(cli, days: int = 120, lag: int = 0, with_sa: bool = False) -> Dict[str, Any]:
    feature_list = FEATURES + (SUPER_FEATURES if with_sa else [])
    today = _dt.date.today()
    start = (today - _dt.timedelta(days=days)).isoformat()
    end = today.isoformat()
    base = fetch_base_history(cli)
    alphas = fetch_submissions(cli, start, end)
    supers = fetch_supers(cli, start, end)
    lb = fetch_leaderboard(cli)
    os_rank = _num(lb.get("dailyOsmosisRank")) or 0.0
    pmap = fetch_pyramid_multipliers(cli)

    by_day: Dict[str, List[Dict[str, Any]]] = {}
    for a in alphas:
        d = str(a.get("dateSubmitted") or "")[:10]
        if d:
            by_day.setdefault(d, []).append(a)
    sa_by_day: Dict[str, List[Dict[str, Any]]] = {}
    for a in supers:
        d = str(a.get("dateSubmitted") or "")[:10]
        if d:
            sa_by_day.setdefault(d, []).append(a)

    X, y, rows = [], [], []
    for d in sorted(by_day):
        key = (_dt.date.fromisoformat(d) + _dt.timedelta(days=lag)).isoformat()
        b = base.get(key)
        if b is None:
            continue
        feat = day_features(by_day[d], pmap, os_rank, sa_by_day.get(d))
        X.append([feat[k] for k in feature_list])
        y.append(math.log(b))
        rows.append({"date": d, "base_date": key, "base": b, **feat})

    if len(rows) < 12:
        return {"ok": False, "reason": f"样本不足：可用配对 {len(rows)} 天（需 ≥12）", "rows": rows}
    # 去掉零方差列（如窗口内没有 PC<0.25 的日子 ⇒ is_low_pc 恒 0 ⇒ 设计矩阵奇异）
    keep: List[int] = []
    for j in range(len(feature_list)):
        col = [row[j] for row in X]
        mu = sum(col) / len(col)
        if (sum((v - mu) ** 2 for v in col) / len(col)) ** 0.5 > 1e-9:
            keep.append(j)
    if len(keep) < 2:
        return {"ok": False, "reason": "全部特征零方差（当日提交件特征无差异）", "rows": rows}
    feature_names = ["const"] + [feature_list[j] for j in keep]
    Xk = [[1.0] + [row[j] for j in keep] for row in X]
    fit = ols(Xk, y)
    pcs = [r["mean_pc"] for r in rows if r["mean_pc"]]
    cov = {
        "pc_min": min(pcs) if pcs else None, "pc_max": max(pcs) if pcs else None,
        "n_low_pc_days": sum(1 for r in rows if r["is_low_pc"] > 0),
        "n_days": len(rows),
    }
    fit.update({"lag": lag, "rows": rows, "os_rank": os_rank, "features": feature_names,
                "coverage": cov})
    return fit


def recent_anchor(cli, k: int = 5) -> Dict[str, Any]:
    """水平锚：最近 k 个「有付款」日的中位数（用于把模型只当相对变化用）。"""
    hist = fetch_base_history(cli)
    days = sorted(hist)[-k:]
    vals = sorted(hist[d] for d in days)
    med = vals[len(vals) // 2] if vals else 0.0
    return {"days": days, "values": [hist[d] for d in days], "median": med, "n": len(vals)}


# ------------------------------------------------------------------ 预测
def predict_alpha(cli, alpha: Dict[str, Any], calib: Dict[str, Any],
                  os_rank: float, pmap: Dict[str, Any],
                  themes_cache: Dict[str, Tuple[float, List[Dict[str, Any]]]]) -> Dict[str, Any]:
    aid = alpha.get("id")
    st = alpha.get("settings") or {}
    m = alpha.get("metrics") or {}
    pc = _num(m.get("prodCorrelation"))
    f = _num(m.get("fitness"))
    s = _num(m.get("sharpe"))

    if aid not in themes_cache:
        try:
            themes_cache[aid] = fetch_theme_mult(cli, str(aid))
        except Exception:
            themes_cache[aid] = (1.0, [])
    _raw_mult, themes = themes_cache[aid]
    theme_mult, theme_uncertain, theme_note, theme_used = resolve_theme(alpha, themes)
    pyr_mult, cats, pyr_src = pyramid_terms(alpha, pmap)
    chain = multiplier_chain(theme_mult, pyr_mult, os_rank)

    beta = calib["beta"]
    sd = calib["resid_sd"]

    def _base_for(tm: float) -> Tuple[float, float, float]:
        ch = multiplier_chain(tm, pyr_mult, os_rank)
        feat = {
            "const": 1.0,
            "log1p_n": math.log(2.0),
            "mean_pc": pc if pc is not None else 0.65,
            "is_low_pc": 1.0 if (pc is not None and pc < 0.25) else 0.0,
            "log1p_maxF": math.log1p(f or 0.0),
            "log1p_meanS": math.log1p(s or 0.0),
            "mean_mult": ch["total_mult"],
            "sa_n": 0.0, "log1p_sa_maxF": 0.0, "log1p_sa_maxS": 0.0, "log1p_sa_maxPC": 0.0,
        }
        lb_ = sum(beta[i] * feat[k] for i, k in enumerate(calib["features"]))
        return math.exp(lb_), math.exp(lb_ - sd), math.exp(lb_ + sd)

    pt, lo, hi = _base_for(theme_mult)
    if theme_uncertain:
        _, _, hi2 = _base_for(2.0)
        hi = max(hi, hi2)
    return {
        "alpha_id": aid, "submitted": alpha.get("dateSubmitted"),
        "region": st.get("region"), "delay": st.get("delay"),
        "sharpe": s, "fitness": f, "prod_corr": pc, "turnover": _num(m.get("turnover")),
        "theme_mult": theme_mult, "theme_status": theme_status(alpha),
        "theme_uncertain": theme_uncertain, "theme_note": theme_note,
        "themes_all": themes, "themes_used": theme_used,
        "pyramid_cats": cats, "pyramid_mult": pyr_mult, "pyramid_src": pyr_src,
        **chain,
        "base_if_alone": min(pt, BASE_CAP_REGULAR), "base_lo": lo,
        "base_hi": min(hi, BASE_CAP_REGULAR * 1.5),
        "base_pc_assumed": pc is None,
    }


def predict_day(preds: List[Dict[str, Any]], calib: Dict[str, Any]) -> Dict[str, Any]:
    """把当日这一批件当成「一天的提交组合」，算该日 base 总额。"""
    n = len(preds)
    pcs = [p["prod_corr"] for p in preds if p["prod_corr"] is not None]
    fs = [p["fitness"] for p in preds if p["fitness"] is not None]
    ss = [p["sharpe"] for p in preds if p["sharpe"] is not None]
    mults = [p["total_mult"] for p in preds]
    mean = lambda v: sum(v) / len(v) if v else 0.0
    feat = {
        "const": 1.0,
        "log1p_n": math.log1p(n),
        "mean_pc": mean(pcs),
        "is_low_pc": 1.0 if pcs and mean(pcs) < 0.25 else 0.0,
        "log1p_maxF": math.log1p(max(fs) if fs else 0.0),
        "log1p_meanS": math.log1p(mean(ss)),
        "mean_mult": mean(mults),
        "sa_n": 0.0, "log1p_sa_maxF": 0.0, "log1p_sa_maxS": 0.0, "log1p_sa_maxPC": 0.0,
    }
    logb = sum(calib["beta"][i] * feat[k] for i, k in enumerate(calib["features"]))
    pt = min(math.exp(logb), BASE_CAP_REGULAR)
    sd = calib["resid_sd"]
    return {"n": n, "base": pt, "lo": math.exp(logb - sd), "hi": math.exp(logb + sd), "features": feat}


# ------------------------------------------------------------------ VF
def vf_impact(vf: Dict[str, Any], new_cats: Sequence[str], k: int) -> Dict[str, Any]:
    N = int(vf.get("N") or 0)
    A = int(vf.get("A") or 0)
    P = int(vf.get("P") or 0)
    SH = _num(vf.get("S_H")) or 0.0
    pmx = int(vf.get("P_max") or P_MAX)
    before = (A / N) * (P / pmx) * SH if N else 0.0
    P2 = P + len(new_cats)
    lo = (A / (N + k)) * (P2 / pmx) * SH if N else 0.0
    hi = ((A + k) / (N + k)) * (P2 / pmx) * SH if N else 0.0
    return {
        "before": before, "after_lo": lo, "after_hi": hi,
        "delta_lo_pct": (lo / before - 1) * 100 if before else 0.0,
        "delta_hi_pct": (hi / before - 1) * 100 if before else 0.0,
        "N": N, "A": A, "P": P, "P2": P2, "P_max": pmx, "S_H": SH,
        "dP": len(new_cats), "dN": k, "new_categories": list(new_cats),
    }


# ------------------------------------------------------------------ 输出
def _print_report(preds: List[Dict[str, Any]], vfi: Dict[str, Any], calib: Dict[str, Any],
                  lb: Dict[str, Any], batch: Optional[Dict[str, Any]] = None,
                  anchor: Optional[Dict[str, Any]] = None) -> None:
    vf, osr = _num(lb.get("valueFactor")), _num(lb.get("dailyOsmosisRank"))
    print("=" * 100)
    print(f"账户 VF={vf}  OsmosisRank={osr}  ⇒  (1+OS) = {1 + (osr or 0):.2f}")
    print(f"标定: n={calib.get('n')} 天  R²={calib.get('r2', 0):.3f}  "
          f"残差sd={calib.get('resid_sd', 0):.3f} (log) ⇒ 区间倍率 ×{math.exp(calib.get('resid_sd', 0)):.2f}")
    cov = calib.get("coverage") or {}
    if cov.get("pc_min") is not None:
        print(f"标定覆盖: 日均 PC {cov['pc_min']:.2f}–{cov['pc_max']:.2f}；"
              f"PC<0.25 的天数 = {cov['n_low_pc_days']}")
        if not cov["n_low_pc_days"]:
            print("  ⚠ 样本内 0 天落在 PC<0.25 ⇒ 该台阶**无法用本账户数据标定**，"
                  "只能引用社区跨账户案例（×4~5），本表不外推")
    print("-" * 100)
    print(f"{'alpha':<12}{'region':<7}{'S':>6}{'F':>6}{'PC':>7}{'theme':>7}{'pyr':>6}{'乘数':>8}{'单件base':>11}")
    for p in sorted(preds, key=lambda x: -x["total_mult"]):
        pc = p["prod_corr"]
        tmk = "*" if p.get("theme_uncertain") else " "
        print(f"{str(p['alpha_id']):<12}{str(p['region']):<7}"
              f"{(p['sharpe'] or 0):>6.2f}{(p['fitness'] or 0):>6.2f}"
              f"{(pc if pc is not None else -1):>7.3f}"
              f"{p['theme_mult']:>6.2f}{tmk}"
              f"{(p['pyramid_mult'] if p['pyramid_mult'] is not None else -1):>6.2f}"
              f"{p['total_mult']:>8.2f}"
              f"{('$%.2f' % p['base_if_alone']):>11}")
    if any(p.get("theme_uncertain") for p in preds):
        print("  * 平台判 MATCHES_THEMES=PASS，但清单无可归属倍率 ⇒ theme 取 1.0，上界按 ×2.0 放宽")
    print("-" * 100)
    if preds:
        lo_all = min(p["base_lo"] for p in preds)
        hi_all = max(p["base_hi"] for p in preds)
        print(f"单件base = 「该件单独提交一天」的点估计；区间 ${lo_all:.2f}–${hi_all:.2f}（±1 残差sd）")
    if batch:
        print(f"当日批量（n={batch['n']}）预估日 base = ${batch['base']:.2f}"
              f"  [${batch['lo']:.2f}, ${batch['hi']:.2f}]")
    if anchor and preds:
        latest = max(preds, key=lambda p: str(p.get("submitted") or ""))
        others = [p for p in preds if p is not latest]
        base_wo = predict_day(others, calib) if others else None
        rel = (batch["base"] / base_wo["base"] - 1) if base_wo and base_wo["base"] else None
        if rel is not None:
            print(f"锚定口径（推荐）：最近 {anchor['n']} 个有付日中位 ${anchor['median']:.2f}"
                  f" × 新增 {latest['alpha_id']} 的相对变化 {rel * 100:+.2f}% "
                  f"⇒ 日 base ${anchor['median'] * (1 + rel):.2f}（+${anchor['median'] * rel:.2f}/天）")
        else:
            print(f"锚定口径：最近 {anchor['n']} 个有付日中位 ${anchor['median']:.2f}"
                  f"；本件单件相对水平 ×{batch['base'] / max(anchor['median'], 1e-9):.2f}")
        tot = sum(p["base_if_alone"] for p in preds) or 1.0
        for p in sorted(preds, key=lambda x: -x["base_if_alone"]):
            print(f"    {str(p['alpha_id']):<12} 权重 {p['base_if_alone'] / tot * 100:5.1f}%   "
                  f"累计 ΔP 归属 {','.join(p['pyramid_cats']) or '—'}")
    print()
    print(f"VF(多样性分) 提交前 {vfi['before']:.6f}  →  提交后 "
          f"[{vfi['after_lo']:.6f}, {vfi['after_hi']:.6f}]  "
          f"({vfi['delta_lo_pct']:+.2f}% ~ {vfi['delta_hi_pct']:+.2f}%)")
    print(f"  分解: N {vfi['N']}→{vfi['N'] + vfi['dN']}  A {vfi['A']}→[A, A+{vfi['dN']}]  "
          f"P {vfi['P']}→{vfi['P2']}  ΔP={vfi['dP']} {vfi['new_categories'] or ''}")
    print(f"  判读: ΔP≥1 ⇒ 多样性分必升；ΔP=0 ⇒ 至多持平（A 不增则必降 "
          f"{100 / (vfi['N'] + 1):.2f}%）")
    print("=" * 100)


def _print_standard(preds: List[Dict[str, Any]], vfi: Dict[str, Any], lb: Dict[str, Any],
                    batch: Optional[Dict[str, Any]], anchor: Optional[Dict[str, Any]],
                    calib: Dict[str, Any]) -> None:
    """提交汇报的「四数」标准块（用户 2026-11-22 明令，缺一不算汇报）。"""
    osr = _num(lb.get("dailyOsmosisRank")) or 0.0
    vf = _num(lb.get("valueFactor"))
    print(f"VF:   {vfi['before']:.6f} → {vfi['after_lo']:.6f}~{vfi['after_hi']:.6f} "
          f"({vfi['delta_lo_pct']:+.2f}% ~ {vfi['delta_hi_pct']:+.2f}%)   "
          f"N {vfi['N']}→{vfi['N'] + vfi['dN']}  A {vfi['A']}→[A, A+{vfi['dN']}]  "
          f"P {vfi['P']}→{vfi['P2']}  ΔP=+{vfi['dP']} {vfi['new_categories'] or ''}")
    print(f"      valueFactor {vf}（提交当天不变，平台按季更新）")

    latest = max(preds, key=lambda p: str(p.get("submitted") or "")) if preds else None
    others = [p for p in preds if p is not latest]
    base_wo = predict_day(others, calib) if others else None
    rel = (batch["base"] / base_wo["base"] - 1) if (batch and base_wo and base_wo["base"]) else None
    if batch and rel is not None:
        print(f"base: 当日 {len(others)} 颗 ${base_wo['base']:.3f} → {batch['n']} 颗 ${batch['base']:.3f}"
              f"（+${batch['base'] - base_wo['base']:.3f}/天, {rel * 100:+.2f}%）")
        if anchor:
            print(f"      锚定：${anchor['median']:.2f} × {rel * 100:+.2f}% ⇒ "
                  f"${anchor['median'] * (1 + rel):.2f}（+${anchor['median'] * rel:.2f}/天）")
    elif batch:
        print(f"base: 当日 {batch['n']} 颗 预估 ${batch['base']:.3f}  [${batch['lo']:.2f}, ${batch['hi']:.2f}]")
    for p in preds:
        print(f"      单件 {p['alpha_id']} ${p['base_if_alone']:.2f} | 乘数 "
              f"({p['theme_mult']:.2f}+{p['pyramid_used']:.2f}−1)×(1+{osr:.2f}) = {p['total_mult']:.2f}")
    print("      口径：绝对水平＝最近5个有付日中位×模型相对变化，模型只出 Δ（docs/experience/10 §1.4）")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="每日提交件的 base 预估 + VF 前后")
    ap.add_argument("--calibrate", action="store_true", help="重新标定经验模型（写 cache/base_forecast_calib.json）")
    ap.add_argument("--days", type=int, default=120, help="标定回看天数")
    ap.add_argument("--lag", type=int, default=-1, help="base 到账滞后天数；-1=自动试 0/1")
    ap.add_argument("--with-sa", action="store_true",
                    help="把当日 SA 特征并入模型（实测无增益，仅用于复核）")
    ap.add_argument("--alpha", default=None, help="逗号分隔的 alpha id")
    ap.add_argument("--date", default=None, help="取该日（ET）已提交的 REGULAR 件")
    ap.add_argument("--vf-only", action="store_true", help="只报 VF 影响")
    ap.add_argument("--report", action="store_true",
                    help="只输出「提交四数」标准块（VF/base/锚定/单件+乘数），供提交汇报直接粘贴")
    ap.add_argument("--json", default=None)
    a = ap.parse_args(argv)

    cli = _client()

    if a.calibrate:
        lags = (0, 1) if a.lag < 0 else (a.lag,)
        best = None
        for lag in lags:
            r = calibrate(cli, a.days, lag, a.with_sa)
            if r.get("ok") and (best is None or r["r2"] > best["r2"]):
                best = r
        if not best:
            print("[base_forecast] 标定失败：样本不足或设计矩阵奇异")
            for lag in lags:
                r = calibrate(cli, a.days, lag, a.with_sa)
                print(f"   lag={lag}: {r.get('reason') or r.get('ok')} 配对={len(r.get('rows') or [])}")
            return 2
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(CALIB_FILE, "w", encoding="utf-8") as f:
            json.dump({k: best[k] for k in ("beta", "r2", "resid_sd", "n", "features", "lag",
                                            "os_rank", "coverage", "rows", "se", "t")},
                      f, ensure_ascii=False, indent=2)
        print(f"[base_forecast] 标定完成：n={best['n']} lag={best['lag']} R²={best['r2']:.3f} "
              f"resid_sd={best['resid_sd']:.3f}  特征={best['features']}")
        for i, k in enumerate(best["features"]):
            t = best["t"][i]
            flag = "  ★显著" if abs(t) >= 2 else ""
            print(f"   {k:<14}{best['beta'][i]:+.4f}   t={t:+.2f}{flag}")
        print(f"   已写 {CALIB_FILE}")
        rows = best.get("rows") or []
        if rows:
            g: Dict[int, List[float]] = {}
            for r in rows:
                g.setdefault(int(r["n"]), []).append(r["base"])
            print("  数量曲线（当日提交数 → base 均值）：")
            for n in sorted(g):
                v = g[n]
                print(f"    n={n}: {len(v):>3} 天   均值 ${sum(v) / len(v):.2f}"
                      f"   区间 ${min(v):.2f}–${max(v):.2f}")
        if not (a.alpha or a.date):
            return 0

    if not os.path.exists(CALIB_FILE):
        print("[base_forecast] 缺标定文件，先跑 --calibrate")
        return 2
    with open(CALIB_FILE, encoding="utf-8") as f:
        calib = json.load(f)

    lb = fetch_leaderboard(cli)
    os_rank = _num(lb.get("dailyOsmosisRank")) or 0.0
    pmap = fetch_pyramid_multipliers(cli)
    # 「提交前」的真前值：--date 时窗口收在该日之前一天（当日提交已进窗口）
    vf_end = None
    if a.date:
        vf_end = (_dt.date.fromisoformat(a.date) - _dt.timedelta(days=1)).isoformat()
    vf = fetch_vf(cli, 30, vf_end)

    alphas: List[Dict[str, Any]] = []
    if a.alpha:
        for aid in [x.strip() for x in a.alpha.split(",") if x.strip()]:
            d = _mcp(cli, "get_alpha_details", {"alpha_id": aid})
            if isinstance(d, dict) and d.get("id"):
                alphas.append(d)
    elif a.date:
        alphas = fetch_submissions(cli, a.date, a.date)

    if not alphas:
        print("[base_forecast] 没有取到 alpha（--alpha/--date 为空？）")
        return 2

    theme_cache: Dict[str, Tuple[float, List[Dict[str, Any]]]] = {}
    preds = [predict_alpha(cli, x, calib, os_rank, pmap, theme_cache) for x in alphas]

    known = set((vf.get("per_pyramid_counts") or {}).keys())
    new_cats: List[str] = []
    for p, x in zip(preds, alphas):
        st = x.get("settings") or {}
        for c in p["pyramid_cats"]:
            full = f"{st.get('region')}/D{st.get('delay')}/{c.upper()}"
            if full not in known and full not in new_cats:
                new_cats.append(full)
    vfi = vf_impact(vf, new_cats, len(preds))
    batch = predict_day(preds, calib)
    anchor = recent_anchor(cli)

    if a.report:
        _print_standard(preds, vfi, lb, batch, anchor, calib)
    elif not a.vf_only:
        _print_report(preds, vfi, calib, lb, batch, anchor)
    else:
        print(f"VF(多样性分) {vfi['before']:.6f} → [{vfi['after_lo']:.6f}, {vfi['after_hi']:.6f}] "
              f"({vfi['delta_lo_pct']:+.2f}% ~ {vfi['delta_hi_pct']:+.2f}%)  ΔP={vfi['dP']}")

    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"preds": preds, "vf": vfi, "calib": calib, "leaderboard": lb},
                      f, ensure_ascii=False, indent=2)
        print(f"已落盘 {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
