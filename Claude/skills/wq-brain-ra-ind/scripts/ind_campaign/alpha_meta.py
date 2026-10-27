# -*- coding: utf-8 -*-
"""alpha_meta.py — 取 alpha 的表达式 / 设置 / 换手 / ATOM 判定（P0-2 镜像批用）

用法::

    <venv-python> <skill>/scripts/ind_campaign/alpha_meta.py <alpha_id> [<alpha_id> ...]

stdout 契约（消费方 = 同目录 `wqb_campaign/transport.py` 的 ``fetch_alpha_meta()``）::

    + <aid> atom=0|1 decay=4 tvr=0.8702 settings={"universe":"TOP500",...} code=<expr>
    x <aid> msg=<原因，<=100 字>

`atom` 用平台硬判据（见 memory `atom-definition-and-screening`）：
`checks` 里**有 `LOW_2Y_SHARPE` 且没有 `IS_LADDER_SHARPE`**（再用单字段来源即成立）。
⚠ 不能用 `pyramids.effective == 1` 代替：同塔的两个数据集也是 effective=1 但非 ATOM
（2026-10-26 逐颗核过）。`effective` 仍打印在 `#` 诊断行里作参考。

`settings` 只含镜像复现需要的 5 个维度（decay 单列，因为派发时必须逐字复现源设置，
否则镜像不是「精确取负」而是另一个实验）。

`tvr` = 换手。镜像的换手与源**逐字相同**（权重 w→−w 不改 Σ|Δw| / Σ|w|），
所以镜像批只读源的值就够了，不必为每条镜像再多打一次详情。

凭据由 ``brain_client`` 从 ``world-quant-brain-mcp/.env`` 读取，本脚本不接触。
"""
import asyncio
import json
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

MISSING = "na"
# 镜像派发时 dispatch 能覆写的设置维度（decay 单独成字段，见 stdout 契约）
_SETTING_KEYS = ("universe", "neutralization", "truncation", "nan_handling", "max_trade")


def _num(x):
    if x is None:
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _check_names(checks):
    """checks 可能是扁平列表（原始 API），也可能是分桶 dict（MCP 精简层）。"""
    if isinstance(checks, dict):
        out = []
        for v in checks.values():
            if isinstance(v, list):
                for c in v:
                    if isinstance(c, dict) and c.get("name"):
                        out.append(c["name"])
        return out
    return [c.get("name") for c in (checks or []) if isinstance(c, dict) and c.get("name")]


def _is_atom(checks):
    """平台 ATOM 硬判据：有 LOW_2Y_SHARPE 且没有 IS_LADDER_SHARPE。

    返回 (atom: 0|1, why: str|None)。checks 为空 ⇒ 判 0 并给出原因（不得当 ATOM 用）。
    """
    names = set(_check_names(checks))
    if not names:
        return 0, "checks 缺失，无法判定 ATOM"
    if "IS_LADDER_SHARPE" in names:
        return 0, "含 IS_LADDER_SHARPE（非单数据集形态）"
    if "LOW_2Y_SHARPE" not in names:
        return 0, "无 LOW_2Y_SHARPE（非平台单数据集口径）"
    return 1, None


def _settings(ad):
    st = ad.get("settings") or {}
    out = {}
    for k in _SETTING_KEYS:
        camel = {"nan_handling": "nanHandling", "max_trade": "maxTrade"}.get(k, k)
        v = st.get(camel)
        if v is not None:
            out[k] = str(v)
    return out


def _tvr(ad):
    isd = ad.get("is") or {}
    v = _num(isd.get("turnover"))
    if v is None:
        v = _num((isd.get("metrics") or {}).get("turnover"))
    if v is None:
        v = _num((ad.get("metrics") or {}).get("turnover"))
    return v


async def _one(aid):
    r = await brain_client._request("GET", f"{brain_client.base_url}/alphas/{aid}")
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}"
    try:
        ad = r.json() if r.text else {}
    except Exception as e:
        return None, f"bad json {type(e).__name__}"
    code = ((ad.get("regular") or {}).get("code") or "").strip()
    if not code:
        return None, "no regular.code"
    isd = ad.get("is") or {}
    checks = isd.get("checks") or ad.get("checks") or []
    atom, why = _is_atom(checks)
    st = ad.get("settings") or {}
    decay = st.get("decay")
    if decay is None:
        return None, "no settings.decay"
    tvr = _tvr(ad)
    eff = (ad.get("pyramids") or {}).get("effective")
    line = ("+ {aid} atom={atom} decay={dec} tvr={tvr} settings={st} code={code}".format(
        aid=aid, atom=atom, dec=int(decay),
        tvr=("na" if tvr is None else f"{tvr:.4f}"),
        st=json.dumps(_settings(ad), ensure_ascii=False, separators=(",", ":")),
        code=code))
    diag = (f"# {aid} effective={eff} atom={atom}" + (f"（{why}）" if why else ""))
    return (line, diag), None


async def main(ids):
    await brain_client.ensure_authenticated()
    for aid in ids:
        try:
            got, err = await _one(aid)
        except Exception as e:
            got, err = None, f"{type(e).__name__}: {e}"
        if got is None:
            print(f"x {aid} msg={str(err)[:100]}", flush=True)
            continue
        line, diag = got
        print(line, flush=True)
        print(diag, flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a.strip()]
    try:
        if not args:
            print("# usage: alpha_meta.py <alpha_id> [<alpha_id> ...]", flush=True)
        else:
            asyncio.run(main(args))
    except Exception as e:   # 任何未捕获异常都要有可读输出（消费方按 x 行记故障）
        print(f"# fatal: {type(e).__name__}: {e}", flush=True)
