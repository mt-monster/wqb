#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""batch_isolate.py — 批次被平台「连坐」后的**坏臂定位与好臂重投**（2026-11-20 新增）。

为什么需要它（形态 A）
----------------------
平台有两种完全不同的失败形态，处置方式相反：

- **形态 A｜编译期连坐**：某条表达式编译不过（幽灵算子 / 元数违规 / 命名参数违规 /
  字段非法）⇒ 父 multisim 状态 ERROR，出错条 ERROR、**其余全部 CANCELLED**。
  实测一次丢 8~10 个槽位净损失（docs/experience/02_signal_patterns.md §形态A）。
- **形态 B｜运行期逐条**：量纲（UNITS）/ 语义错 ⇒ 该条 WARNING/FAIL，**其余照常出结果**。

本工具只处理形态 A：

    1. 读回批次的子任务状态，判定是否真的连坐（父 ERROR + 存在 CANCELLED 子任务）；
    2. 把「可疑表达式集」二分重投，**递归定位**到具体坏臂（平台不接受 n=1 的数组，
       故单条用裸 dict 提交）；
    3. 只把**好臂**重新组成干净的批派发（坏臂记录进 `--out` 报告，不再重投）。

用法
----
::

    # 只读分析（不触网派发）：给出坏臂与好臂清单 + 建议重投批
    python tools/batch_isolate.py --multisim-id 3JXv... --expr-file logs/batch.txt --plan-only

    # 分析 + 实际重投好臂（派发受通道闸约束：WQB_ALLOW_CLI_DISPATCH=1）
    python tools/batch_isolate.py --multisim-id 3JXv... --expr-file logs/batch.txt \
        --dispatch --out logs/isolate_report.json

⚠ **派发通道**：与 `tools/submit_batch.py` 同纪律 —— CLI 派发默认禁止
（`WQB_ALLOW_CLI_DISPATCH=1` 才放行）；正常路径是本工具出计划、由 MCP
``create_multi_simulation`` 派发（``--plan-only`` 即该用法）。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _pyenv  # noqa: E402  跨平台 MCP 目录解析

MCP_DIR = str(_pyenv.mcp_dir())

#: 坏臂定位的最大二分深度（10 条 ⇒ 深度 4 足够定位到单条）
MAX_DEPTH = 6
#: 每次重投后的等待秒数（平台排队 + 去重注册延迟）
POLL_INTERVAL = 6
#: 单次探测批的等待上限（秒）
PROBE_TIMEOUT = 420
#: 单条探测的等待上限（秒）——单条只需一条 alpha 落定，不必等满批的排队长
PROBE_TIMEOUT_SINGLE = 180


def load_exprs(path: str) -> List[str]:
    """读表达式文件（与 submit_batch.load 同口径：去 BOM、去注释行）。"""
    with open(path, encoding="utf-8-sig") as f:
        return [l.strip().lstrip("﻿") for l in f
                if l.strip() and not l.strip().startswith("#")]


def _client():
    """建 BrainApiClient（429 退避内置）。"""
    os.chdir(MCP_DIR)
    if MCP_DIR not in sys.path:
        sys.path.insert(0, MCP_DIR)
    from brain_api import BrainApiClient  # noqa: E402
    return BrainApiClient()


async def _post(client, exprs: Sequence[str], settings: Dict) -> Optional[str]:
    """提交一批表达式，返回 multisim location；失败返回 None。"""
    body = ([{"type": "REGULAR", "settings": settings, "regular": e} for e in exprs]
            if len(exprs) > 1 else
            {"type": "REGULAR", "settings": settings, "regular": exprs[0]})
    resp = await client._request("POST", f"{client.base_url}/simulations", json=body)
    if resp.status_code == 429:
        wait = client._retry_wait_seconds(resp, 0)
        print(f"  429 并发已满，等 {wait:.0f}s")
        await asyncio.sleep(wait)
        resp = await client._request("POST", f"{client.base_url}/simulations", json=body)
    if resp.status_code != 201:
        print(f"  提交失败 status={resp.status_code}: {resp.text[:200]}")
        return None
    return resp.headers.get("Location", "")


async def _children(client, location: str) -> List[Dict]:
    """读回子任务列表（含 status / alpha / error）。

    ⚠ 平台口径（2026-11-20 实测校正）：``GET /simulations/{multisim_id}`` 的
    ``children`` 元素是**子任务的相对路径或绝对 URL**（形如 ``/simulations/<id>``），
    不是 dict、也不是 alpha id；必须逐个再 GET 才拿得到 status。
    早期版本直接把 child 当绝对 URL 用 ⇒ 拿到 404 的 ``{"detail": ...}``，
    于是「读不到 status」被误判成「无 CANCELLED」⇒ 形态 A 会被漏判。
    """
    def _shape(c: str) -> str:
        if c.startswith("http"):
            return c
        if c.startswith("/"):
            return f"{client.base_url}{c}"
        return f"{client.base_url}/simulations/{c}"

    url = _shape(location)
    resp = await client._request("GET", url)
    if resp.status_code != 200:
        return []
    try:
        data = resp.json()
    except Exception:
        return []
    children = data.get("children") or []
    out: List[Dict] = []
    for c in children:
        cu = _shape(c if isinstance(c, str) else c.get("location", ""))
        try:
            cd = (await client._request("GET", cu)).json()
        except Exception:
            cd = {}
        err = ""
        try:
            err = client._simulation_error_message(cd) or ""
        except Exception:
            err = cd.get("error") or ""
        out.append({
            "location": cu,
            "status": (cd.get("status") or "").upper(),
            "alpha": cd.get("alpha"),
            "error": err,
        })
    return out


async def _self_status(client, location: str) -> Dict:
    """读单个 simulation 自身的状态（单条提交时 children 为空，状态在顶层）。

    ⚠ 2026-11-20 实测修正：平台对**单条**提交的响应**没有 children**（多条的
    children 是子任务相对路径）。早期版本只看 children ⇒ 单条探测恒得「无 CANCELLED」
    ⇒ **坏臂被误判为干净并被重投**（连带整批再次连坐）。故单条必须读自身状态。
    """
    if location.startswith("http"):
        url = location
    elif location.startswith("/"):
        url = f"{client.base_url}{location}"
    else:
        url = f"{client.base_url}/simulations/{location}"
    try:
        resp = await client._request("GET", url)
        if resp.status_code != 200:
            return {}
        data = resp.json()
    except Exception:
        return {}
    err = ""
    try:
        err = client._simulation_error_message(data) or ""
    except Exception:
        err = data.get("error") or ""
    return {"status": (data.get("status") or "").upper(), "error": err,
            "alpha": data.get("alpha")}


async def _probe(client, exprs: Sequence[str], settings: Dict) -> Tuple[bool, str]:
    """探测一批表达式是否「连坐」。

    返回 (poisoned, location)：
      poisoned=True  ⇒ 该批至少含一条编译期坏臂（父 ERROR / 存在 CANCELLED 子任务 / 单条自身 ERROR）
      poisoned=False ⇒ 该批干净（子任务全 COMPLETE / WARNING / FAIL，无 CANCELLED）

    判定口径（2026-11-20 实测）：
      - **父 multisim status=ERROR** 且子任务里出现 CANCELLED ⇒ 形态 A（连坐）——最典型；
      - 父 ERROR 但子任务各自 FAIL/ERROR 而**无 CANCELLED** ⇒ 形态 B（逐条失败），不连坐，
        本批**不算坏**（好臂已正常产出 alpha），只把失败条单独记；
      - **单条提交**：children 为空 ⇒ 读自身 status；ERROR/FAIL ⇒ 编译期坏臂（形态 A 的单条形态）；
      - 子任务全终态且无 CANCELLED ⇒ 不连坐。
    """
    loc = await _post(client, exprs, settings)
    if not loc:
        # 提交失败（含 429 耗尽）——不能判定为「坏臂」，保守视为干净（不误伤好臂）
        return False, ""
    import time
    waited = 0
    timeout = PROBE_TIMEOUT_SINGLE if len(exprs) == 1 else PROBE_TIMEOUT
    TERMINAL = {"COMPLETE", "DONE", "WARNING", "ERROR", "CANCELLED", "FAILED", "FAIL"}
    COMPILE_FAIL = {"ERROR", "FAIL", "FAILED"}
    while waited < timeout:
        kids = await _children(client, loc)
        if kids:
            statuses = [str(k.get("status", "")).upper() for k in kids]
            if "CANCELLED" in statuses:
                return True, loc
            if all(s in TERMINAL for s in statuses):
                # 有 ERROR/FAIL 但无 CANCELLED ⇒ 形态 B（逐条失败），该批不算连坐
                return False, loc
        else:
            # children 为空：单条提交（状态在顶层）或子任务尚未注册
            me = await _self_status(client, loc)
            st = me.get("status")
            if st in COMPILE_FAIL:
                return True, loc          # 单条编译期失败（形态 A 的单条形态）
            if st in TERMINAL:
                return False, loc
        await asyncio.sleep(POLL_INTERVAL)
        waited += POLL_INTERVAL
    return False, loc


async def isolate(client, exprs: List[str], settings: Dict,
                  log=print) -> Tuple[List[str], List[str]]:
    """二分定位坏臂。

    返回 (bad_exprs, good_exprs)。策略：
      - 先探整批；不连坐 ⇒ 全部好臂（零重投成本）；
      - 连坐 ⇒ 对半再探，递归；命中单条 ⇒ 该条为坏臂。
    """
    poisoned, loc = await _probe(client, exprs, settings)
    if not poisoned:
        log(f"  整批不连坐（{len(exprs)} 条）⇒ 无坏臂")
        return [], list(exprs)

    log(f"  整批连坐（{len(exprs)} 条，探针 {loc}）⇒ 二分定位")
    bad: List[str] = []
    good: List[str] = []
    stack: List[Tuple[List[str], int]] = [(list(exprs), 0)]
    while stack:
        chunk, depth = stack.pop()
        if len(chunk) == 1:
            bad.append(chunk[0])
            log(f"    坏臂: {chunk[0][:90]}")
            continue
        if depth >= MAX_DEPTH:
            # 深度用尽仍非单条 ⇒ 整块判坏（保守：宁可多标坏臂，不让坏臂进重投批）
            bad.extend(chunk)
            log(f"    深度上限，整块判坏 {len(chunk)} 条")
            continue
        mid = len(chunk) // 2
        left, right = chunk[:mid], chunk[mid:]
        for part in (left, right):
            p, _ = await _probe(client, part, settings)
            if p:
                stack.append((part, depth + 1))
            else:
                good.extend(part)
                log(f"    干净 {len(part)} 条 ⇒ 直接算好臂")
    return bad, good


def _settings_from(base: Dict, overrides: Dict) -> Dict:
    s = dict(base)
    s.update({k: v for k, v in overrides.items() if v is not None})
    return s


async def _run(args) -> int:
    exprs = load_exprs(args.expr_file)
    if args.expect and len(exprs) != args.expect:
        print(f"[warn] 表达式数 {len(exprs)} 与 --expect {args.expect} 不符")
    base = json.load(open(args.settings, encoding="utf-8")) if args.settings else {}
    settings = _settings_from(base, json.loads(args.overrides) if args.overrides else {})

    print(f"[isolate] 输入 {len(exprs)} 条表达式")
    if args.multisim_id:
        client = _client()
        await client.ensure_authenticated()
        loc = args.multisim_id if args.multisim_id.startswith("http") else f"{client.base_url}/simulations/{args.multisim_id}"
        kids = await _children(client, loc)
        statuses = [str(k.get("status", "")).upper() for k in kids]
        print(f"[isolate] 原批 {len(kids)} 子任务，状态分布: "
              f"{ {s: statuses.count(s) for s in set(statuses)} }")
        if "CANCELLED" not in statuses:
            print("[isolate] 原批无 CANCELLED ⇒ 不是形态 A，无需隔离（形态 B 逐条失败请直接看每条 error）")

    if args.plan_only:
        print("[plan-only] 未派发。计划要点："
              "\n  1) 先用 MCP create_multi_simulation 把 --expr-file 的表达式按「风险分层」小批派发"
              "\n     （新算子/新字段/新参数组合 ⇒ 单独 1~2 条一批先探）"
              "\n  2) 批回来若父状态 ERROR 且子任务含 CANCELLED ⇒ 用本工具 --dispatch 只重投好臂")
        return 0

    if os.environ.get("WQB_ALLOW_CLI_DISPATCH", "") != "1":
        print("[channel-gate] BLOCKED: CLI 派发禁止（与 submit_batch.py 同纪律）。"
              "改用 MCP create_multi_simulation，或由用户显式设 WQB_ALLOW_CLI_DISPATCH=1。",
              file=sys.stderr)
        return 2

    client = _client()
    await client.ensure_authenticated()
    bad, good = await isolate(client, exprs, settings)
    report = {"bad_expressions": bad, "good_expressions": good,
              "total": len(exprs), "bad": len(bad), "good": len(good)}
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[isolate] 报告 → {args.out}")
    print(f"[isolate] 坏臂 {len(bad)} 条 / 好臂 {len(good)} 条")
    for b in bad:
        print(f"  BAD : {b[:110]}")
    if good and args.dispatch:
        loc = await _post(client, good, settings)
        report["good_batch_location"] = loc
        print(f"[isolate] 好臂重投 → {loc or '(失败)'}")
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="批次连坐后的坏臂定位与好臂重投")
    ap.add_argument("--multisim-id", help="已知连坐的 multisim id / location（可省）")
    ap.add_argument("--expr-file", required=True, help="当初派发的表达式文件（顺序即子任务顺序）")
    ap.add_argument("--expect", type=int, default=0, help="预期条数（与文件不符时告警）")
    ap.add_argument("--settings", help="settings JSON 文件（默认档位）")
    ap.add_argument("--overrides", help="settings 覆盖 JSON 串")
    ap.add_argument("--plan-only", action="store_true", help="只出计划不派发")
    ap.add_argument("--dispatch", action="store_true", help="定位后重投好臂（需通道闸放行）")
    ap.add_argument("--out", help="报告 JSON 路径")
    args = ap.parse_args()
    return asyncio.run(_run(args))


if __name__ == "__main__":
    sys.exit(main())
