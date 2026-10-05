#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""neutralization_scan.py — 固定表达式、扫描 neutralization 档位（2026-10-04）。

动机（论坛 42659822656663《PROD CORRELATION<0.7 实战复盘：mm 结构如何把 corr 从
0.86 压到 0.67》）：**中性化与 universe 是"旋钮组合"，降 prod corr 时必须跟
字段结构一起重配**，单扫表达式几何是盲的。该帖的黄金组合是
「换字段结构 + group 维度 + CROWDING 中性化」，且只有 CROWDING 能同时保住
CLUSTER 与区域 Sharpe。

本脚本对**同一批表达式**逐个 neutralization 档位提交 multi-sim，产出
`--out` 映射文件（档位 → multisim Location + 表达式顺序），供收割时按下标
反查「哪颗 alpha 来自哪个档位」。

为什么不用 MCP 的 create_multi_simulation：neutralization 是**批级参数**，
逐档扫描需多次调用；本脚本一次进程内跑完，且天然保证除 neutralization 外
其余 settings 完全一致（干净隔离）。

用法::

    python tools/research/neutralization_scan.py --path exprs.txt --region KOR \
        --universe TOP600 --decay 4 \
        --neutralizations CROWDING,MARKET,SUBINDUSTRY,REVERSION_AND_MOMENTUM \
        --out logs/_kor_neut_map.json

    # 只打印 payload 不提交
    python tools/research/neutralization_scan.py --path exprs.txt --region KOR \
        --neutralizations CROWDING --dry-run

退出码：0=全部提交成功；2=某档 POST 失败；3=字段预检失败。
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "world-quant-brain-mcp"))

# KOR/D1/TOP600 等常见区的合法档位（get_platform_setting_options 实测，2026-10-04）。
# 脚本不硬性限制——平台会拒非法档位；这里只做默认值与提示。
DEFAULT_NEUTRALIZATIONS = [
    "STATISTICAL",
    "CROWDING",
    "MARKET",
    "SECTOR",
    "INDUSTRY",
    "SUBINDUSTRY",
    "SLOW_AND_FAST",
    "FAST",
    "SLOW",
    "REVERSION_AND_MOMENTUM",
]


def build_settings(a: argparse.Namespace, neutralization: str) -> dict:
    return {
        "instrumentType": "EQUITY",
        "region": a.region,
        "universe": a.universe,
        "delay": a.delay,
        "decay": a.decay,
        "neutralization": neutralization,
        "truncation": a.truncation,
        "pasteurization": "ON",
        "unitHandling": "VERIFY",
        "nanHandling": a.nan_handling,
        "maxTrade": a.max_trade,
        "maxPosition": "OFF",
        "language": "FASTEXPR",
        "visualization": False,
        "startDate": a.start_date,
        "endDate": a.end_date,
    }


def read_exprs(path: str) -> list:
    """按行读表达式；跳过空行 / # 注释 / 含中文的行（否则整批 children 连坐 CANCELLED）。"""
    exprs, skipped = [], []
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if any("一" <= ch <= "鿿" for ch in s):
            skipped.append(s)
            continue
        exprs.append(s)
    for s in skipped:
        print(f"[neut-scan] 跳过非 FASTEXPR 行: {s[:60]}")
    return exprs


def preflight(exprs: list) -> int:
    """发批前三闸（2026-10-04 补）：括号平衡 → 算子名存在性 → 元数。

    血泪教训（同一晚连踩三次，每次都连坐整批 CANCELLED）：
      ① 括号整体失衡 ⇒ 平台 "Unexpected end of input"（`check_expression` 放行！）
      ② 算子名拼错（`tade_when`）⇒ 平台 "unknown operator"
      ③ 只跑元数闸、漏了算子存在性闸
    三闸任一不过即 ABORT，绝不发批。
    """
    sys.path.insert(0, str(ROOT / "src"))
    try:
        from wqb.expression import op_arity as oa
    except Exception as e:
        print(f"[neut-scan] 跳过离线预检（op_arity 不可用: {e}）")
        return 0
    bad = 0
    for i, e in enumerate(exprs, 1):
        errs = []
        bal = e.count("(") - e.count(")")
        if bal:
            errs.append(f"[PAREN] 括号不平衡 balance={bal:+d}")
        errs += list(oa.check_unknown_operators(e))
        try:
            oa.check_expression(e)
        except Exception as ex:
            errs.append(f"[SYNTAX] {ex}")
        if errs:
            bad += 1
            print(f"[neut-scan] 第 {i} 条不通过：")
            for x in errs:
                print(f"          {x}")
    if bad:
        print(f"[neut-scan] ABORT: {bad}/{len(exprs)} 条未过三闸 —— 修完再发，否则整批连坐 CANCELLED。")
    else:
        print(f"[neut-scan] 发批前三闸 OK（{len(exprs)} 条）")
    return bad


async def main_async(a: argparse.Namespace) -> int:
    from brain_api import brain_client as brain  # noqa: E402

    exprs = read_exprs(a.path)
    if not exprs:
        print("[neut-scan] 没有可提交的表达式")
        return 3

    if not a.dry_run and preflight(exprs):
        return 3

    neuts = [x.strip() for x in a.neutralizations.split(",") if x.strip()]
    if not neuts:
        neuts = DEFAULT_NEUTRALIZATIONS

    print(f"[neut-scan] {len(exprs)} 条表达式 × {len(neuts)} 个 neutralization 档位")
    print(f"[neut-scan] 其余 settings 固定: decay={a.decay} trunc={a.truncation} "
          f"nan={a.nan_handling} maxTrade={a.max_trade} {a.universe}/{a.region}D{a.delay}")

    if a.dry_run:
        st = build_settings(a, neuts[0])
        print("[neut-scan] DRY-RUN payload 样例:")
        print(json.dumps({"type": "REGULAR", "settings": st, "regular": exprs[0]},
                         ensure_ascii=False)[:500])
        return 0

    await brain.ensure_authenticated()

    mapping = {
        "region": a.region,
        "universe": a.universe,
        "delay": a.delay,
        "decay": a.decay,
        "truncation": a.truncation,
        "nanHandling": a.nan_handling,
        "maxTrade": a.max_trade,
        "exprs": exprs,
        "batches": {},
    }

    for neut in neuts:
        st = build_settings(a, neut)
        payload = [{"type": "REGULAR", "settings": st, "regular": e} for e in exprs]
        body = payload[0] if len(payload) == 1 else payload
        try:
            r = await brain._request("POST", brain.base_url + "/simulations", json=body)
        except Exception as e:  # 网络/连接异常：单档失败不终止其余档位
            print(f"[neut-scan] {neut}: 请求异常 {type(e).__name__}: {e}")
            mapping["batches"][neut] = {"error": f"{type(e).__name__}: {e}"}
            continue
        if r.status_code >= 400:
            msg = str(brain._response_payload(r))[:400]
            print(f"[neut-scan] {neut}: POST {r.status_code} → {msg}")
            mapping["batches"][neut] = {"error": f"HTTP {r.status_code}", "detail": msg}
            continue
        loc = r.headers.get("Location", "")
        # Location 形如 .../simulations/<id>
        msid = loc.rstrip("/").split("/")[-1] if loc else ""
        print(f"[neut-scan] {neut:24s} -> {msid}")
        mapping["batches"][neut] = {"multisim_id": msid, "location": loc, "n": len(exprs)}

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(mapping, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for v in mapping["batches"].values() if v.get("multisim_id"))
    print(f"[neut-scan] 成功 {ok}/{len(neuts)} 档；映射写入 {out}")
    return 0 if ok else 2


def main() -> int:
    ap = argparse.ArgumentParser(description="固定表达式扫描 neutralization 档位")
    ap.add_argument("--path", required=True, help="表达式文件（每行一条）")
    ap.add_argument("--region", default="KOR")
    ap.add_argument("--universe", default="TOP600")
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--decay", type=int, default=4)
    ap.add_argument("--truncation", type=float, default=0.08)
    ap.add_argument("--nan-handling", default="OFF")
    ap.add_argument("--max-trade", default="OFF")
    ap.add_argument("--start-date", default="2014-01-01")
    ap.add_argument("--end-date", default="2023-12-31")
    ap.add_argument("--neutralizations", default="",
                    help="逗号分隔；缺省用 DEFAULT_NEUTRALIZATIONS")
    ap.add_argument("--out", default="logs/_neut_scan_map.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
