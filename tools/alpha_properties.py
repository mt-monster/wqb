# -*- coding: utf-8 -*-
"""alpha_properties.py - Alpha 属性（name/color/tags）存量审计与规范化。

规范单一事实源：`src/wqb/alpha_properties.py`；文档 `docs/alpha_properties_spec.md`。

背景（2026-09-20 审计，见 reports/alpha_properties_audit_20260920.md）：
平台对 `color` 有**硬枚举（仅 5 值）**，对 `tags`/`name` **零约束** → 历史长出
5 类命名 / 3 种颜色 / 6 类标签。本工具负责**存量**的审计与规范化。

子命令
------
  audit       只读审计：统计 name 形态 / color 分布 / 标签合规，列出不合规清单
  normalize   规范化（**默认 dry-run**，加 --apply 才写库）：
                · 补 `CH_REG`/`CH_SUPER`（由 type 推断，确定性）
                · 补 `SRC_<dataset>`（从本地 `alphas`/`expressions` 表取数据集）
                · 补 `W<wave>`（本地可知时）
                · `--fix-color`：color 为空 → `BLUE`（**不动**已有颜色，避免误判健康度）
                · **不改 name**（改名属判断性操作，仅在 audit 中给建议）

安全约定
--------
- 默认 dry-run；`--apply` 前先 `--db-backup`（调 pg 无关，纯文件备份）
- **无条件保留** `RETIRE_*` / `PowerPoolSelected` 等已有标签（只增不改不删）
- 平台侧写操作按颗串行，带 429 退避（走 BrainApiClient）

退出码：0=成功 / 1=失败
运行环境：MCP venv（网络子命令）
"""
import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import time
from collections import Counter
from datetime import datetime

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _add_paths():
    for p in (os.path.join(_REPO, "src"),
              os.environ.get("WQ_MCP_DIR", os.path.join(_REPO, "world-quant-brain-mcp"))):
        if p and p not in sys.path:
            sys.path.insert(0, p)


def _mcp_venv_python():
    """复用 tools/_pyenv 的规范解析（含「$WQ_PY 串仓」防护），不再各抄一份候选列表。

    事故（2026-10-06）：环境残留的 ``WQ_PY`` 指向另一个 wqb 工作区的 venv，只看 ``isfile``
    的候选列表会放行，进程被 re-exec 到错误解释器后卡死。
    """
    _tools = os.path.join(_REPO, "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import _pyenv
    return _pyenv.venv_python()


def _bootstrap_venv():
    py = _mcp_venv_python()
    if py and os.path.abspath(py) != os.path.abspath(sys.executable):
        os.execv(py, [py] + sys.argv)


def _props():
    _add_paths()
    from wqb import alpha_properties as ap
    return ap


def _db():
    _add_paths()
    from wqb.store._common import default_db_path
    return default_db_path()


# ---------------------------------------------------------------- 网络容错

async def _get_json(client, url, retries=4, base_sleep=2.0):
    """带指数退避的 GET。返回 (json, None) 或 (None, error)。

    ★ 必要性：对 100+ 颗 alpha 逐条取详情时，单次 `ProxyError`/`ConnectionError`
      会中断整轮（实测踩到两次）。故每条独立重试，失败只跳过该条。
    """
    import asyncio as _a
    last = None
    for i in range(retries):
        try:
            r = await client._request("GET", url)
            if r.status_code == 200:
                return r.json(), None
            last = f"HTTP {r.status_code}"
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {str(e)[:80]}"
        if i < retries - 1:
            await _a.sleep(base_sleep * (2 ** i))
    return None, last


async def _list_active(client, status="ACTIVE", region=None):
    """列出 alpha（分页，带退避重试）。返回 (items, error)。"""
    import asyncio as _a
    off, items = 0, []
    while off < 3000:
        q = f"{client.base_url}/users/self/alphas?limit=100&offset={off}"
        if status:
            q += f"&status={status}"
        d, err = await _get_json(client, q)
        if err:
            return items, err
        res = (d or {}).get("results", [])
        if not res:
            break
        items.extend(res)
        off += 100
    if region:
        items = [it for it in items if (it.get("settings") or {}).get("region") == region]
    return items, None


# ---------------------------------------------------------------- 本地数据集映射

# ---------------------------------------------------------------- audit

def name_shape(n):
    if n is None or n == "":
        return "空"
    if re.fullmatch(r"[0-9]+(\.[0-9]+)?", str(n)):
        return "PROD数值(违规)"
    if "_prod" in str(n):
        return "含prod复合名"
    if re.fullmatch(r"[A-Z]{3}_[RS]_[a-z0-9_]+_\d{2}", str(n)):
        return "规范"
    return "其它"


def cmd_audit(a):
    _bootstrap_venv()
    _add_paths()
    from brain_api import BrainApiClient
    import asyncio

    ap = _props()

    async def run():
        c = BrainApiClient()
        await c.ensure_authenticated()
        items, err = await _list_active(c, a.status, a.region)
        if err:
            print(f"[warn] 列表失败：{err}")
        rows, failed = [], 0
        for it in items:
            d, e = await _get_json(c, f"{c.base_url}/alphas/{it['id']}")
            if e:
                failed += 1
                continue
            s = d.get("settings") or {}
            rows.append({
                "id": it["id"], "region": s.get("region"), "type": d.get("type"),
                "name": d.get("name"), "color": d.get("color"),
                "tags": list(d.get("tags") or []),
            })
        if failed:
            print(f"[warn] {failed} 颗详情取失败（网络），已跳过")
        return rows

    rows = asyncio.run(run())
    if a.region:
        rows = [r for r in rows if r["region"] == a.region]
    print(f"=== 属性审计：{len(rows)} 颗（status={a.status or 'ALL'}）===")
    print("--- name 形态 ---")
    for k, v in Counter(name_shape(r["name"]) for r in rows).most_common():
        print(f"  {k:16s} {v}")
    print("--- color ---")
    for k, v in Counter(str(r["color"]) for r in rows).most_common():
        print(f"  {k:16s} {v}")
    print("--- tags 合规 ---")
    bad = 0
    for r in rows:
        w = ap.check_tags(r["tags"])
        if w:
            bad += 1
    print(f"  有告警: {bad} / {len(rows)}")
    print("--- 合规告警 Top ---")
    for k, v in Counter(w for r in rows for w in ap.check_tags(r["tags"])).most_common(6):
        print(f"  {v:4d}  {k}")
    if a.limit:
        print(f"--- 明细（前 {a.limit} 条有告警者）---")
        n = 0
        for r in rows:
            w = ap.check_tags(r["tags"])
            if w:
                print(f"  {r['id']:10s} {str(r['region']):5s} {str(r['type']):7s} "
                      f"name={r['name']!r} color={r['color']!r} tags={r['tags']} → {'; '.join(w)}")
                n += 1
                if n >= a.limit:
                    break
    return 0


# ---------------------------------------------------------------- normalize

async def _normalize(a):
    _bootstrap_venv()
    _add_paths()
    from brain_api import BrainApiClient
    ap = _props()
    print("[normalize] SRC 解析器：共享实现 `wqb.alpha_properties.resolve_source_dataset`"
          "（fields 表按字段反查）")

    c = BrainApiClient()
    await c.ensure_authenticated()
    items, err = await _list_active(c, a.status, a.region)
    if err:
        print(f"[normalize] 列表失败：{err}")
    if a.limit:
        items = items[: a.limit]

    print(f"[normalize] 目标 {len(items)} 颗（apply={a.apply}）")
    changed = skipped = failed = fetch_failed = 0
    for it in items:
        aid = it["id"]
        d, e = await _get_json(c, f"{c.base_url}/alphas/{aid}")
        if e:
            fetch_failed += 1
            print(f"  {aid} 详情取失败（{e}），跳过")
            continue
        typ = d.get("type")
        old_tags = [str(t) for t in (d.get("tags") or [])]
        old_color = d.get("color")

        reg = d.get("regular")
        expr = reg.get("code") if isinstance(reg, dict) else None
        keep = [t for t in old_tags
                if not re.match(r"^(CH_|SRC_|W\d|EXPRFAM_|CORR_|TOOL_)", t)]
        # ★ 通道判定：PPA alpha 本身就是 type=REGULAR，按 type 推会误标成普通通道。
        #   旧的 `PowerPoolSelected` 正是 PPA 通道的证据 → 产出 CH_PPA（而非 CH_REG）。
        #   注意 SUPER 不走 PPA 通道，其 CH_SUPER 信息量更高，不做 PPA 覆盖。
        chan = None
        if typ != "SUPER" and "PowerPoolSelected" in old_tags:
            chan = ap.CHANNEL_PPA
        new_tags = ap.build_tags(
            alpha_type=typ,
            channel=chan,
            dataset=ap.resolve_source_dataset(expr, _db()),
            extra=keep,
        )
        new_color = old_color
        if a.fix_color and not old_color:
            new_color = ap.COLOR_PENDING

        if new_tags == old_tags and new_color == old_color:
            skipped += 1
            continue
        print(f"  {aid} {typ:7s} tags {old_tags} → {new_tags}"
              + (f"  color {old_color} → {new_color}" if new_color != old_color else ""))
        if a.apply:
            # ★★★ 事故修复（2026-09-20）：绝不再用 MCP `set_alpha_properties`！
            #   该接口的 payload **无条件包含** `name` 与 `regular.description`
            #   （默认 `None` / 字符串 "None"）→ 未传即等于**要求平台置空**。
            #   实测它把 115 颗 ACTIVE 的 name 全清空、description 全覆写成字符串 'None'。
            #   改用**最小字段 PATCH**：只发要改的键，物理上不可能碰到 name/description。
            payload = {"tags": new_tags}
            if new_color != old_color:
                payload["color"] = new_color
            try:
                r = await c._request("PATCH", f"{c.base_url}/alphas/{aid}", json=payload)
                if r.status_code >= 400:
                    raise RuntimeError(f"HTTP {r.status_code} {str(r.text)[:120]}")
                changed += 1
                time.sleep(0.3)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print(f"     !! 写入失败：{str(e)[:120]}")
        else:
            changed += 1
    print(f"[normalize] {'已写入' if a.apply else 'DRY-RUN 待改'} {changed} / 跳过(已合规) {skipped}"
          + (f" / 写入失败 {failed}" if failed else "")
          + (f" / 详情取失败 {fetch_failed}" if fetch_failed else ""))
    if not a.apply:
        print("  （加 --apply 才写库）")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Alpha 属性（name/color/tags）审计与规范化")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("audit", help="只读审计")
    p.add_argument("--region")
    p.add_argument("--status", default="ACTIVE")
    p.add_argument("--limit", type=int, help="明细最多打印几条")
    p.set_defaults(fn=cmd_audit)

    p = sub.add_parser("normalize", help="规范化（默认 dry-run）")
    p.add_argument("--region")
    p.add_argument("--status", default="ACTIVE")
    p.add_argument("--limit", type=int)
    p.add_argument("--fix-color", action="store_true", help="color 为空 → BLUE（不动已有色）")
    p.add_argument("--apply", action="store_true", help="真正写库")
    p.set_defaults(fn=lambda x: __import__("asyncio").run(_normalize(x)))

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
