# -*- coding: utf-8 -*-
"""probe_towers_sa.py — 只读探针：塔位（pyramids）字段结构 + SA/SUPER 现状盘点。

用途（2026-10-05）：
  1) `get_alpha_details()` 的真实字段形状（region/delay 在哪一层、pyramids 字段是否可用）
     —— 为 submit_inventory.py 补塔位字段提供依据。
  2) SA（SUPER）现状：本账户 ACTIVE 的 SUPER 本体/组件、各区域 ACTIVE REGULAR 计数
     （SA 前置条件：单一区域 ≥10 颗 ACTIVE REGULAR）。

⛔ 铁律：只读平台，绝不 POST /alphas/{id}/submit。

用法：
  python tools/probe_towers_sa.py
  python tools/probe_towers_sa.py N1VnJjXg O08EjLVp LLZ6wZO2
"""
import asyncio
import json
import sys

import _pyenv  # noqa: E402

_pyenv.reexec_under_venv()
_pyenv.bootstrap_paths()


def _extract_items(lst):
    """get_user_alphas 返回体里取 alpha 列表（兼容 dict/list 两种形态）。"""
    if isinstance(lst, list):
        return lst
    if isinstance(lst, dict):
        for k in ("alphas", "data", "items", "results"):
            v = lst.get(k)
            if isinstance(v, list):
                return v
            if isinstance(v, dict):
                for k2 in ("alphas", "data", "items", "results"):
                    v2 = v.get(k2)
                    if isinstance(v2, list):
                        return v2
    return []


def _region(a, default="?"):
    """区域在顶层或 nested regular/settings 里都有可能。"""
    if not isinstance(a, dict):
        return default
    if a.get("region"):
        return a.get("region")
    for k in ("regular", "settings", "regularSettings"):
        v = a.get(k)
        if isinstance(v, dict) and v.get("region"):
            return v.get("region")
    return default


def _created(a):
    return (a or {}).get("dateCreated") or (a or {}).get("date_created")


def _settings(a):
    v = (a or {}).get("settings")
    if isinstance(v, dict):
        return v
    for k in ("regular", "regularSettings"):
        w = (a or {}).get(k)
        if isinstance(w, dict) and isinstance(w.get("settings"), dict):
            return w["settings"]
    return {}


def _sel_lim(a):
    return _settings(a).get("selectionLimit")


def _sel_handle(a):
    return _settings(a).get("selectionHandling")


def _delay(a):
    for k in ("delay", "delayDays"):
        if (a or {}).get(k) not in (None, ""):
            return a.get(k)
    for k in ("regular", "settings", "regularSettings"):
        v = (a or {}).get(k)
        if isinstance(v, dict) and v.get("delay") not in (None, ""):
            return v.get("delay")
    return None


async def main(aids):
    from brain_api import BrainApiClient
    brain = BrainApiClient()
    await brain.ensure_authenticated()

    print("=" * 100)
    print("【1】get_alpha_details() 字段结构（找 region/delay/category/pyramids）")
    print("=" * 100)
    for aid in aids:
        try:
            d = await brain.get_alpha_details(aid)
        except Exception as e:  # noqa: BLE001
            print(f"  {aid} ERR {type(e).__name__}: {str(e)[:100]}")
            continue
        if not isinstance(d, dict):
            print(f"  {aid} 返回非 dict: {type(d).__name__}")
            continue
        reg = d.get("regular") if isinstance(d.get("regular"), dict) else {}
        st = d.get("settings") if isinstance(d.get("settings"), dict) else {}
        print(f"\n  {aid}  status={d.get('status')} type={d.get('type')}")
        print(f"    name={d.get('name')!r}  category={d.get('category')!r}")
        print(f"    region(delay,universe,neut) settings={st.get('region')}({st.get('delay')},"
              f"{st.get('universe')},{st.get('neutralization')})")
        print(f"    pyramidThemes = {json.dumps(d.get('pyramidThemes'), ensure_ascii=False, default=str)[:400]}")
        print(f"    themes        = {json.dumps(d.get('themes'), ensure_ascii=False, default=str)[:300]}")
        print(f"    classifications = {json.dumps(d.get('classifications'), ensure_ascii=False, default=str)[:300]}")
        print(f"    tags          = {json.dumps(d.get('tags'), ensure_ascii=False, default=str)[:300]}")
        py = d.get("pyramids")
        s = json.dumps(py, ensure_ascii=False, default=str)
        print(f"    pyramids({type(py).__name__}) = {s[:500]}{'...' if len(s) > 500 else ''}")

    print()
    print("=" * 100)
    print("【2】SA / SUPER 现状（ACTIVE / OS）")
    print("=" * 100)
    for kind in ("SUPER", "REGULAR"):
        try:
            lst = await brain.get_user_alphas(stage="OS", status="ACTIVE",
                                              alpha_type=kind, limit=100)
        except Exception as e:  # noqa: BLE001
            print(f"  type={kind} ERR {type(e).__name__}: {str(e)[:100]}")
            continue
        items = _extract_items(lst)
        print(f"\n  ACTIVE {kind}: {len(items)} 颗")
        by_region = {}
        for a in items:
            r = _region(a)
            by_region[r] = by_region.get(r, 0) + 1
        print(f"    区域分布: {dict(sorted(by_region.items()))}")
        for a in sorted(items, key=lambda x: str(_created(x) or ""), reverse=True)[:15]:
            print(f"    {str(a.get('id'))[:8]:<9} {_region(a):<4} {str(a.get('name') or '')[:32]:<32} "
                  f"S={a.get('sharpe')} F={a.get('fitness')} d={_delay(a)} "
                  f"created={str(_created(a))[:10]} "
                  f"selLim={_sel_lim(a)} selHandle={_sel_handle(a)}")

    print()
    print("=" * 100)
    print("【3】SA 前置条件：单一区域 ACTIVE REGULAR >= 10")
    print("=" * 100)
    try:
        reg = await brain.get_user_alphas(stage="OS", status="ACTIVE",
                                          alpha_type="REGULAR", limit=200)
        regs = _extract_items(reg)
        c = {}
        for a in regs:
            if isinstance(a, dict):
                c[_region(a)] = c.get(_region(a), 0) + 1
        for r, n in sorted(c.items(), key=lambda kv: -kv[1]):
            print(f"    {r:<5} {n:>3} 颗  {'✓ 达标' if n >= 10 else '✗ 不足'}")
    except Exception as e:  # noqa: BLE001
        print(f"  REGULAR 计数 ERR {type(e).__name__}: {str(e)[:100]}")

    print()
    print("=" * 100)
    print("【4】全部 SA（不分 status）——找未提交/非 ACTIVE 的 SA 候选")
    print("=" * 100)
    for stage in ("OS", "IS"):
        try:
            lst = await brain.get_user_alphas(stage=stage, alpha_type="SUPER", limit=100)
        except Exception as e:  # noqa: BLE001
            print(f"  stage={stage} ERR {type(e).__name__}: {str(e)[:100]}")
            continue
        items = _extract_items(lst)
        cs = {}
        for a in items:
            if isinstance(a, dict):
                cs[a.get("status") or "?"] = cs.get(a.get("status") or "?", 0) + 1
        print(f"\n  stage={stage}  SUPER 共 {len(items)} 颗  status 分布={cs}")
        for a in sorted(items, key=lambda x: str(_created(x) or ""), reverse=True)[:12]:
            if not isinstance(a, dict):
                continue
            print(f"    {str(a.get('id'))[:8]:<9} {_region(a):<4} status={str(a.get('status')):<12} "
                  f"stage={a.get('stage')} {str(a.get('name') or '')[:30]:<30} "
                  f"created={str(_created(a))[:10]}")

    return 0


if __name__ == "__main__":
    _pyenv.bootstrap_paths()
    argv = [a for a in sys.argv[1:] if a]
    if not argv:
        argv = ["N1VnJjXg", "O08EjLVp", "LLZ6wZO2"]
    sys.exit(asyncio.run(main(argv)))
