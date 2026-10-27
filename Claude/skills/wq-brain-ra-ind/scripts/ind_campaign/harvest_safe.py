# -*- coding: utf-8 -*-
"""harvest_safe.py — 战役收割子进程（transport.harvest 的 stdout 契约实现）

用法::

    <venv-python> <skill>/scripts/ind_campaign/harvest_safe.py <sim_id> <dataset> <label>

⚠ 2026-10-26 迁入技能目录：原住 `cache/_harvest_safe.py`（gitignore + 未跟踪），
两次被清理掉、收割链直接断（"没有任何结果"），而它是 transport 的硬依赖。
现在 `cache/` 位只作历史兼容，transport 优先用本文件。

stdout 契约（消费方 = 同目录 `wqb_campaign/transport.py` 的 ``harvest()``，
正则与状态机逐字依赖下面三行形态）::

    + <alpha_id> S=-1.23 F=0.45 tvr=0.123 2Y=1.58 sub=1.01 rob=1.23
    x <alpha_id> msg=<错误摘要，<=100 字>
    status=<STATUS> children=<N>        # 末行；STATUS=COMPLETE/ERROR/UNKNOWN...

`rob` = LOW_ROBUST_UNIVERSE_SHARPE（IND 的 robust 闸，限值 1.0）。
旧格式（无 rob=）仍被 transport 的 `row6()` 兼容成 None ⇒ 不是硬契约破坏。

状态语义（transport 侧）:
    COMPLETE + children>0 + 行数齐全 -> ok
    COMPLETE + children=0            -> empty（结构性空批）
    COMPLETE + 行数不足               -> partial（限流缺子任务，可重试补齐）
    ERROR                            -> fail（平台侧整批跑不起来；transport 只认 ERROR/FAIL 为终态）
    其它（含 UNKNOWN）                -> running（继续等）

设计要点（均为实测教训）:
- **平台 ``GET /simulations/{id}`` 排队中只返回 ``{"progress": x}``、无 status** ->
  必须打 ``status=UNKNOWN``（打 ``status=None`` 会被 transport 的 ``\\w+`` 正则判成查询失败）。
- **单条批（n=1）平台不写 children**，只在父响应里给 ``alpha`` -> 按 ``children=1`` 报，
  否则 transport 判 empty、单条结果被永久丢弃（2026-10-22 事故）。
- **CANCELLED / FAILED 归一成 ERROR**：transport 只把 ERROR/FAIL 当终态，
  否则整批已死还要白等 8x180s，且毒化表达式自愈（重派剔除黑名单）不会触发。
- **子任务之间 sleep 0.4s 限速**：平台对 alpha 详情端点限流，整批会被打成 0 行。
- 缺 2Y/sub/rob 时回落 -99（sentinel）而不是丢行：下游判闸必然不过，但 alpha 仍在清单里可复查。

凭据由 ``brain_client`` 从 ``world-quant-brain-mcp/.env`` 读取，本脚本不接触。
"""
import asyncio
import os
import sys
from pathlib import Path


def _add_tools_path() -> Path:
    """把仓库 ``tools/`` 放上 sys.path（向上探测 pyproject.toml + src/wqb，与层数无关）。"""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            tools = str(parent / "tools")
            if tools not in sys.path:
                sys.path.insert(0, tools)
            return parent
    raise RuntimeError("repo root not found (needs pyproject.toml + src/wqb)")


REPO_ROOT = _add_tools_path()
import _pyenv  # noqa: E402

_pyenv.bootstrap_paths()
from brain_api import brain_client  # noqa: E402

SLEEP_PER_CHILD = 0.4
MISSING = -99.0


def _num(x):
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _pick(obj, *keys):
    """按顺序取第一个非 None 值（0.0 是合法值，不能用 or 链）。"""
    for k in keys:
        if isinstance(obj, dict):
            v = obj.get(k)
        else:
            v = None
        if v is not None:
            return v
    return None


def _check_value(checks, name):
    for c in checks or []:
        if isinstance(c, dict) and c.get("name") == name:
            return c.get("value")
    return None


def _two_year(is_data, checks):
    """2Y 口径（与 tools/harvest_multisim.py 同序）: checks > is.twoYearSharpe > ladder 近两年均值。"""
    v = _num(_check_value(checks, "LOW_2Y_SHARPE"))
    if v is None:
        v = _num(_check_value(checks, "IS_LADDER_SHARPE"))
    if v is None:
        v = _num(_pick(is_data, "twoYearSharpe")) or None
    if v is None:
        v = _num(_pick(is_data.get("metrics") or {}, "twoYearSharpe"))
    if v is None:
        ladder = is_data.get("ladder") or {}
        seq = ladder.get("sharpe") if isinstance(ladder, dict) else None
        if isinstance(seq, list) and len(seq) >= 2:
            vals = [_num(s.get("value")) for s in seq[-2:] if isinstance(s, dict)]
            vals = [x for x in vals if x is not None]
            if vals:
                v = sum(vals) / len(vals)
    return v


def _sub_universe(is_data, checks):
    v = _num(_pick(is_data, "subUniverseSharpe"))
    if v is None:
        v = _num(_pick(is_data.get("metrics") or {}, "subUniverseSharpe"))
    if v is None:
        v = _num(_check_value(checks, "LOW_SUB_UNIVERSE_SHARPE"))
    return v


def _robust(is_data, checks):
    """robust 闸值（IND 的 LOW_ROBUST_UNIVERSE_SHARPE，限值 1.0）。

    2026-10-26：ATOM 全灭在这道闸上（限值固定 1.0，区域无差异），旧收割完全不取它
    ⇒ 候选选择只能看 S，选出来的都是 robust 0.8x 的废票。checks 在前：那是平台判闸用的同一数值。
    """
    v = _num(_check_value(checks, "LOW_ROBUST_UNIVERSE_SHARPE"))
    if v is None:
        v = _num(_pick(is_data, "robustUniverseSharpe"))
    if v is None:
        v = _num(_pick(is_data.get("metrics") or {}, "robustUniverseSharpe"))
    return v


def _child_loc(c):
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        return c.get("location") or c.get("url") or c.get("id")
    return None


def _abs(loc):
    if loc.startswith("http"):
        return loc
    if loc.startswith("/"):
        return f"{brain_client.base_url}{loc}"
    return f"{brain_client.base_url}/simulations/{loc}"


def _basename(loc):
    return str(loc).rstrip("/").rsplit("/", 1)[-1]


async def _one_child(loc):
    """返回 (row_str | None, err_str | None)。

    2026-10-26 实测（robust 几何冒烟）：**单条批**的 parent `children` 里直接给的是
    **alpha id**（8 位，如 `vROWaP2a`），不是 sim id ⇒ `/simulations/{alpha_id}` 必然
    404。旧实现把这行记成 `x … HTTP 404 on child sim` ⇒ rows=0/1 ⇒ transport 判
    partial，重试 3 轮后接受空结果，**该 alpha 永久丢失**（与上文「单条批不丢」相反）。
    现改为 404 时按 alpha id 直取详情；多表达式批（children 是 sim id）行为不变。
    """
    try:
        r = await brain_client._request("GET", _abs(loc))
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"[:100]
    if r.status_code == 404:
        return await _alpha_row(_basename(loc))
    if r.status_code != 200:
        return None, f"HTTP {r.status_code} on child sim"
    try:
        d = r.json() if r.text else {}
    except Exception as e:
        return None, f"bad child json: {type(e).__name__}"[:100]
    aid = d.get("alpha") or d.get("alphaId")
    if not aid:
        return None, "child sim has no alpha id"
    return await _alpha_row(aid)


async def _alpha_row(aid):
    """GET /alphas/{aid} → (row_str | None, err_str | None)。"""
    try:
        ra = await brain_client._request("GET", f"{brain_client.base_url}/alphas/{aid}")
    except Exception as e:
        return None, f"alpha {aid}: {type(e).__name__}: {e}"[:100]
    if ra.status_code != 200:
        return None, f"alpha {aid}: HTTP {ra.status_code}"
    try:
        ad = ra.json() if ra.text else {}
    except Exception as e:
        return None, f"alpha {aid}: bad json {type(e).__name__}"[:100]
    is_data = ad.get("is") or {}
    m = is_data.get("metrics") or {}
    checks = is_data.get("checks") or ad.get("checks") or []
    s = _num(_pick(is_data, "sharpe"))
    if s is None:
        s = _num(_pick(m, "sharpe"))
    f = _num(_pick(is_data, "fitness"))
    if f is None:
        f = _num(_pick(m, "fitness"))
    tvr = _num(_pick(is_data, "turnover"))
    if tvr is None:
        tvr = _num(_pick(m, "turnover"))
    y2 = _two_year(is_data, checks)
    sub = _sub_universe(is_data, checks)
    rob = _robust(is_data, checks)
    # 零交易 alpha（LOW_FITNESS ERROR / turnover 0）会缺 fitness —— 它仍是**已跑完的仿真**，
    # 必须出行（否则 rows < children 被打成 partial 白等 3x20s，且该 alpha 永久丢出清单）。
    # 只有「取不到 alpha 详情」才算 x（那才是瞬时故障，值得重试）。
    miss = [k for k, v in (("S", s), ("F", f), ("2Y", y2), ("sub", sub), ("rob", rob)) if v is None]
    if miss:
        print(f"# {aid} missing {','.join(miss)} -> sentinel {MISSING}", flush=True)
    s = MISSING if s is None else s
    f = MISSING if f is None else f
    y2 = MISSING if y2 is None else y2
    sub = MISSING if sub is None else sub
    rob = MISSING if rob is None else rob
    tvr_s = f"{tvr:.3f}" if tvr is not None else "na"
    return (f"+ {aid} S={s:.2f} F={f:.2f} tvr={tvr_s} 2Y={y2:.2f} sub={sub:.2f} rob={rob:.2f}", None)


async def main():
    if len(sys.argv) < 2:
        print("status=UNKNOWN children=0")
        return
    sim_id = sys.argv[1]
    ds = sys.argv[2] if len(sys.argv) > 2 else ""
    label = sys.argv[3] if len(sys.argv) > 3 else ""
    tag = f"{ds}:{label}" if ds else label

    try:
        await brain_client.ensure_authenticated()
        r = await brain_client._request("GET", f"{brain_client.base_url}/simulations/{sim_id}")
    except Exception as e:
        print(f"# auth/query failed for {sim_id} ({tag}): {type(e).__name__}: {e}", flush=True)
        print("status=UNKNOWN children=0", flush=True)
        return

    if r.status_code != 200:
        print(f"# HTTP {r.status_code} on parent sim {sim_id} ({tag})", flush=True)
        print("status=UNKNOWN children=0", flush=True)
        return

    try:
        j = r.json() if r.text else {}
    except Exception as e:
        print(f"# bad parent json ({tag}): {type(e).__name__}: {e}", flush=True)
        print("status=UNKNOWN children=0", flush=True)
        return

    st = str(j.get("status") or "").upper()
    kids = [loc for loc in (_child_loc(c) for c in (j.get("children") or [])) if loc]
    # 单条批：平台不写 children，只在父响应体里给 alpha
    single = j.get("alpha") or j.get("alphaId")
    if not kids and single and st in ("COMPLETE", "DONE", "WARNING"):
        kids = [single]

    if st in ("CANCELLED", "CANCELED", "FAILED", "FAIL", "ERROR"):
        out_st = "ERROR"
    elif st in ("COMPLETE", "DONE", "WARNING"):
        out_st = "COMPLETE"
    else:
        out_st = "UNKNOWN"

    n_ok = 0
    if out_st == "COMPLETE":
        for i, loc in enumerate(kids):
            if i:
                await asyncio.sleep(SLEEP_PER_CHILD)
            row, err = await _one_child(loc)
            if row:
                print(row, flush=True)
                n_ok += 1
            elif err:
                print(f"x {loc if not str(loc).startswith('http') else str(loc).rsplit('/', 1)[-1]} msg={err}",
                      flush=True)

    print(f"status={out_st} children={len(kids)}", flush=True)
    print(f"# {tag} status={st or 'None'} rows={n_ok}/{len(kids)}", flush=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:  # 任何未捕获异常都退化成 running，让 transport 重试而不是判死
        print(f"# fatal: {type(e).__name__}: {e}", flush=True)
        print("status=UNKNOWN children=0", flush=True)
