# -*- coding: utf-8 -*-
"""tower_quota.py — 两塔组合配额闸（派发前必查；用户 2026-10-27 / 2026-10-28 定案）。

**为什么需要它**：USA 一轮实战里 `risk/model` 累积到 6 颗、`risk/other` 占满 3 颗，
都是**挖完才数出来**的 —— 配额规则只存在于口述与记忆里，派发时没有任何东西会拦。
本工具把它变成派发前的确定性闸：读区域台账、给余量、超配即 exit 1。

规则（唯一实现在 :mod:`wqb.profiles.locked`）：
  * 每个两塔组合候选 ≤ ``TOWER_PAIR_QUOTA``（3）；超配封盘，**既有候选仍可提交**；
  * ``{PV,MODEL,OTHER}`` 三者间不得两两组腿（含 PV+PV、三塔同现）→ ``check_tower_mix``；
  * trio 塔 × 其它 category 的组合总量 ≤ ``TOWER_TRIO_CROSS_QUOTA``（5）。

**塔位来源**：平台 ``ra.pyramid_short``（形如 ``"risk/model"``）或 ``pyramids.list``。
本工具**不推断塔位**，只统计人工/Agent 登记进来的组合键 —— 本地 ``backtest_results.dataset``
是分组标签、且跨区污染，不得当塔位用。

状态文件：``tracking/<REGION>/config/tower_pair_quota.json``
    {"_doc": "...", "limit": 3,
     "pairs": {"model/risk": 6, "other/risk": 3},
     "alphas": {"model/risk": ["9qxLOPxr", "88RdZ61v"]}}

用法：
  python tools/tower_quota.py --region USA                      # 配额表 + 余量
  python tools/tower_quota.py --region USA --check "risk/analyst"
  python tools/tower_quota.py --region USA --add "risk/analyst" --alpha-id O0AEjnv7
  python tools/tower_quota.py --region USA --init "risk/model=6" "risk/other=3"
  python tools/tower_quota.py --region USA --json

退出码：0 = 可派 / 操作成功；1 = 该组合已封盘；2 = 塔混违规；3 = 参数或状态文件错误。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _bootstrap_src() -> None:
    """把 `src/` 放上 sys.path：向上探测 pyproject.toml + src/wqb 双标记。"""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists() and (parent / "src" / "wqb").is_dir():
            src = str(parent / "src")
            if src not in sys.path:
                sys.path.insert(0, src)
            return
    raise SystemExit("仓库根未找到（向上未见 pyproject.toml + src/wqb 双标记）")


_bootstrap_src()

from wqb.profiles.locked import (  # noqa: E402
    TOWER_PAIR_QUOTA,
    TOWER_TRIO_CROSS_QUOTA,
    check_tower_mix,
    tower_pair_key,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def state_path(region: str) -> Path:
    return REPO_ROOT / "tracking" / region.upper() / "config" / "tower_pair_quota.json"


def load_state(region: str) -> dict:
    p = state_path(region)
    if not p.exists():
        return {"limit": TOWER_PAIR_QUOTA, "pairs": {}, "alphas": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"状态文件解析失败 {p}: {exc}")
    data.setdefault("limit", TOWER_PAIR_QUOTA)
    data.setdefault("pairs", {})
    data.setdefault("alphas", {})
    # 规范化键（老文件可能写了 'risk/Model'）
    data["pairs"] = {tower_pair_key(k): int(v) for k, v in data["pairs"].items()}
    data["alphas"] = {tower_pair_key(k): list(v) for k, v in data["alphas"].items()}
    return data


def save_state(region: str, data: dict) -> Path:
    p = state_path(region)
    p.parent.mkdir(parents=True, exist_ok=True)
    data["_doc"] = (
        "两塔组合配额台账（用户 2026-10-27/28 定案）。键 = 塔名小写排序后 '/' 连接；"
        "上限 = limit；超配封盘但既有候选仍可提交。塔位来源只认平台 ra.pyramid_short。"
    )
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def pair_row(data: dict, pair: str) -> dict:
    key = tower_pair_key(pair)
    used = int(data["pairs"].get(key, 0))
    limit = int(data.get("limit", TOWER_PAIR_QUOTA))
    return {
        "pair": key,
        "used": used,
        "limit": limit,
        "remaining": max(limit - used, 0),
        "sealed": used >= limit,
        "mix_violation": check_tower_mix(key),
    }


def cmd_table(region: str, data: dict, as_json: bool) -> int:
    rows = [pair_row(data, k) for k in sorted(data["pairs"])]
    sealed = [r["pair"] for r in rows if r["sealed"]]
    out = {
        "region": region.upper(),
        "limit": int(data.get("limit", TOWER_PAIR_QUOTA)),
        "trio_cross_quota": TOWER_TRIO_CROSS_QUOTA,
        "rows": rows,
        "sealed_pairs": sealed,
        "note": "sealed 组合不得再派新候选；既有候选仍可提交",
    }
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print(f"区域 {out['region']}　单组合上限 {out['limit']}　trio×其它上限 {TOWER_TRIO_CROSS_QUOTA}")
    print(f"{'组合':<22}{'已用':>5}{'上限':>6}{'余量':>6}  状态")
    print("-" * 62)
    for r in rows:
        if r["mix_violation"]:
            state = "⛔ 塔混违规"
        elif r["sealed"]:
            state = "⛔ 封盘"
        else:
            state = "✅ 可派"
        print(f"{r['pair']:<22}{r['used']:>5}{r['limit']:>6}{r['remaining']:>6}  {state}")
    if not rows:
        print("（台账为空：用 --init / --add 登记；不登记 = 闸对你是瞎的）")
    print()
    print(f"封盘组合 {len(sealed)} 个" + (f"：{', '.join(sealed)}" if sealed else ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="两塔组合配额闸（派发前必查；塔位只认平台 ra.pyramid_short）"
    )
    ap.add_argument("--region", required=True, help="区域代码，如 USA")
    ap.add_argument("--check", metavar="PAIR", help="查单个组合是否可派（封盘 exit 1）")
    ap.add_argument("--add", metavar="PAIR", help="把该组合计数 +1（需配 --alpha-id）")
    ap.add_argument("--alpha-id", help="与 --add 搭配：登记是哪颗 alpha")
    ap.add_argument("--init", nargs="+", metavar="PAIR=N", help="初始化/覆盖计数，如 risk/model=6")
    ap.add_argument("--json", action="store_true", help="机器可读输出")
    a = ap.parse_args()

    region = a.region.upper()
    data = load_state(region)

    if a.init:
        pairs, alphas = {}, data.get("alphas", {})
        for item in a.init:
            if "=" not in item:
                print(f"--init 需要 PAIR=N 形式，收到 {item!r}", file=sys.stderr)
                return 3
            k, v = item.rsplit("=", 1)
            key = tower_pair_key(k)
            bad = check_tower_mix(key)
            if bad:
                print(bad, file=sys.stderr)
                return 2
            try:
                pairs[key] = int(v)
            except ValueError:
                print(f"N 必须是整数，收到 {v!r}", file=sys.stderr)
                return 3
        data["pairs"] = pairs
        data["alphas"] = alphas
        p = save_state(region, data)
        print(f"已写入 {p}")
        return cmd_table(region, data, a.json)

    if a.add:
        key = tower_pair_key(a.add)
        bad = check_tower_mix(key)
        if bad:
            print(bad, file=sys.stderr)
            return 2
        limit = int(data.get("limit", TOWER_PAIR_QUOTA))
        used = int(data["pairs"].get(key, 0))
        if used >= limit:
            print(
                f"组合 {key} 已用 {used} 颗（上限 {limit}）⇒ 封盘，不得再派该组合新候选",
                file=sys.stderr,
            )
            return 1
        data["pairs"][key] = used + 1
        if a.alpha_id:
            data["alphas"].setdefault(key, []).append(a.alpha_id)
        p = save_state(region, data)
        print(f"已登记 {key} → {used + 1}/{limit}（{p}）")
        return cmd_table(region, data, a.json)

    if a.check:
        r = pair_row(data, a.check)
        if r["mix_violation"]:
            print(r["mix_violation"], file=sys.stderr)
            return 2
        if r["sealed"]:
            print(
                f"组合 {r['pair']} 已用 {r['used']} 颗（上限 {r['limit']}）⇒ 封盘，不得再派该组合新候选",
                file=sys.stderr,
            )
            return 1
        print(f"✅ 组合 {r['pair']} 已用 {r['used']}/{r['limit']}，余量 {r['remaining']} ⇒ 可派")
        return 0

    return cmd_table(region, data, a.json)


if __name__ == "__main__":
    raise SystemExit(main())
