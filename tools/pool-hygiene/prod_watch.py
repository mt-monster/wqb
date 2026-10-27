# -*- coding: utf-8 -*-
"""prod 候选巡检：对「七闸全过、只差 prod」的候选池重测生产相关性。

背景（2026-10-18）：USA/Analyst 一族的 prod 地板实测在 0.70–0.81，其中
`1YjoKAz6` 已达 0.7094（差 0.0094）。生产池每日漂移实测可达 ±0.29/半天，
所以**唯一零成本路径 = 每日重测，一旦 <0.7 立即提交**（无需重跑仿真）。

用法（仓库根，必须用 $WQ_PY）：
    $WQ_PY tools/pool-hygiene/prod_watch.py --pool tracking/USA/candidates/prod_waitlist.json
    $WQ_PY tools/pool-hygiene/prod_watch.py --pool ... --json        # 机器可读
    $WQ_PY tools/pool-hygiene/prod_watch.py --pool ... --no-write    # 只看不写回

行为：
  1. 逐个 alpha 轮询 `/alphas/{id}/correlations/production`（**异步队列**：202 + Retry-After，
     不是 200 ⇒ 必须轮询，见 gate_attribution._poll_correlation 的同一教训）；
  2. 打印 `id / prod / 闸限 / 余量 / 与上次比 / 状态`；
  3. 状态 = READY(<0.7) / NEAR(<0.75) / BLOCKED；
  4. 默认把 last_prod / last_checked 原子写回池文件（tmp + os.replace）。
  5. 单并发 + 条间 sleep（平台 corr 端点每账号单并发，实测单条可达 ~94s）。

池文件格式（JSON 数组）：
    [{"alpha_id": "...", "note": "...", "expression": "...", "last_prod": 0.7094,
      "last_checked": "2026-10-18T21:00:00"}]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GATE = 0.70
NEAR = 0.75


def _load_pool(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("alphas") or data.get("pool") or []
    if not isinstance(data, list):
        raise SystemExit(f"[prod_watch] 池文件格式不对（应为 JSON 数组）：{path}")
    return data


def _save_pool(path: Path, pool: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(pool, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


async def _prod_corr(brain, alpha_id: str, attempts: int = 10, base_wait: float = 20.0) -> float | None:
    """轮询 production 相关性。202 = 队列未就绪，必须继续等（不能当失败）。

    ⚠ **账号级单并发槽**（2026-10-22）：平台 prod 接口每账号仅 1 个在飞。本脚本
    绕过 MCP 客户端的锁直接轮询 ⇒ 会与 MCP 服务 / 其它脚本抢同一个槽，把对方堵到
    轮询上限（实测事故：一方卡住，另一方空转 800s+ 拿不到数）。故显式申请同一个
    跨进程槽（``wqb.correlation_slot``，token 文件与 MCP 侧同名 ⇒ 跨进程真互斥）；
    拿不到就返回 None（调用方按 UNKNOWN 处置，不编造数字）。
    """
    # 真实端点 = /correlations/prod（MCP brain_mixin_spcread._poll_production_correlation 同源）；
    # `/correlations/production` 会 404。响应顶层直接带 `max`，不在 checks.production 里。
    url = f"{brain.base_url}/alphas/{alpha_id}/correlations/prod"

    try:
        from wqb.correlation_slot import slot as _corr_slot
    except Exception:  # pragma: no cover - 依赖缺失时退回无锁
        _corr_slot = None

    async def _poll() -> float | None:
        for i in range(attempts):
            try:
                r = await brain._request("GET", url)
            except Exception as exc:  # noqa: BLE001
                print(f"[warn] {alpha_id} 请求异常：{exc}", file=sys.stderr)
                return None
            if r.status_code == 200:
                text = (r.text or "").strip()
                if not text:
                    # 空体 200 = 平台仍在计算（MCP 实测：通常 1–5 分钟）
                    await asyncio.sleep(base_wait / 2 if i < 6 else base_wait)
                    continue
                try:
                    body = r.json()
                except Exception:  # noqa: BLE001
                    return None
                val = (body or {}).get("max")
                return float(val) if val is not None else None
            if r.status_code in (202, 429):
                wait = base_wait
                try:
                    wait = float(r.headers.get("Retry-After") or base_wait)
                except Exception:  # noqa: BLE001
                    pass
                await asyncio.sleep(min(max(wait, 5.0), 120.0))
                continue
            print(f"[warn] {alpha_id} 返回 {r.status_code}：{r.text[:160]}", file=sys.stderr)
            return None
        print(f"[warn] {alpha_id} 轮询 {attempts} 次仍未就绪", file=sys.stderr)
        return None

    if _corr_slot is None:
        return await _poll()
    with _corr_slot(f"prod_watch({alpha_id})", ttl_sec=attempts * base_wait + 300.0) as s:
        if not s.get("acquired"):
            print(f"[warn] {alpha_id} 账号级相关性槽被其它进程占用 → 跳过（不排队）",
                  file=sys.stderr)
            return None
        return await _poll()


def _status(v: float | None) -> str:
    if v is None:
        return "UNKNOWN"
    if v < GATE:
        return "READY"
    if v < NEAR:
        return "NEAR"
    return "BLOCKED"


async def _run(args) -> int:
    import _pyenv

    _pyenv.bootstrap_paths()
    from brain_api import BrainApiClient  # noqa: E402

    pool_path = Path(args.pool)
    pool = _load_pool(pool_path)
    if not pool:
        print("[prod_watch] 池为空")
        return 0
    # ⚠ 2026-10-19 修复：此前 `pool = pool[:limit]` 会在末尾把**截断后的池写回文件**，
    # 一次 `--limit 1` 调试就能把 7 条候选削成 1 条（真实发生过）。
    # 现在 limit 只作用于遍历视图，写回永远针对全量 pool。
    work = pool[: args.limit] if args.limit else pool

    brain = BrainApiClient()
    await brain.ensure_authenticated()

    rows, ready = [], []
    for i, item in enumerate(work):
        aid = str(item.get("alpha_id") or "").strip()
        if not aid:
            continue
        prev = item.get("last_prod")
        val = await _prod_corr(brain, aid)
        st = _status(val)
        gap = None if val is None else round(GATE - val, 4)
        delta = None if (val is None or prev is None) else round(val - float(prev), 4)
        rows.append({
            "alpha_id": aid,
            "note": item.get("note", ""),
            "prod": val,
            "gate": GATE,
            "gap": gap,
            "delta": delta,
            "status": st,
        })
        if st == "READY":
            ready.append(aid)
        if val is not None:
            item["last_prod"] = val
            item["last_checked"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        if i < len(work) - 1:
            await asyncio.sleep(args.sleep)

    # ---- 输出 ----
    if args.json:
        print(json.dumps({"checked_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "rows": rows,
                          "ready": ready, "gate": GATE}, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== prod 巡检（闸限 {GATE}）｜{time.strftime('%Y-%m-%d %H:%M')} ===\n")
        print(f"{'alpha':12} {'prod':>8} {'余量':>8} {'较上次':>8}  {'状态':8} 备注")
        print("-" * 78)
        for r in rows:
            p = "-" if r["prod"] is None else f"{r['prod']:.4f}"
            g = "-" if r["gap"] is None else f"{r['gap']:+.4f}"
            d = "-" if r["delta"] is None else f"{r['delta']:+.4f}"
            print(f"{r['alpha_id']:12} {p:>8} {g:>8} {d:>8}  {r['status']:8} {r['note'][:26]}")
        print()
        if ready:
            print(f"★ 可提交：{', '.join(ready)}（prod < {GATE}）")
        else:
            best = min((r for r in rows if r["prod"] is not None), key=lambda x: x["prod"], default=None)
            if best:
                print(f"暂无 READY；最优 {best['alpha_id']} prod={best['prod']:.4f}（差 {best['gap']:+.4f}）")

    if not args.no_write:
        _save_pool(pool_path, pool)
        print(f"[prod_watch] 已回写 {pool_path.relative_to(REPO) if pool_path.is_relative_to(REPO) else pool_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="prod 候选巡检（只读平台 + 回写池文件）")
    ap.add_argument("--pool", required=True, help="候选池 JSON 路径")
    ap.add_argument("--limit", type=int, default=0, help="只查前 N 个（调试用）")
    ap.add_argument("--sleep", type=float, default=8.0, help="条间等待秒数（默认 8）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--no-write", action="store_true", help="不回写池文件")
    return asyncio.run(_run(ap.parse_args()))


if __name__ == "__main__":
    sys.exit(main())
