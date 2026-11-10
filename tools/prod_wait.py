# -*- coding: utf-8 -*-
"""等待平台 prod 锁释放并测单个 alpha 的 prod（严格尊重 retry_after，不轮询轰炸）。

背景：prod 端点是**账号级单并发**，被占用时返回
  {"status":"correlation_busy","retry_after":180,"max":null}
旧 check_prod 每 10s 重打 ⇒ 自锁。本脚本按 retry_after 精确退避。

用法：
    python tools/prod_wait.py leMnPeJ2 [--minutes 45]
    python tools/prod_wait.py leMnPeJ2 --peek --tries 8 --interval 20
产出： results/prod_wait_<alpha>.json（带锁）/ results/prod_peek_<alpha>.json（--peek）
落库： python tools/prod_peek_ingest.py <alpha>   ← 用产物里的 at 作 checked_at 写权威表

2026-11-10 审查修复：
  * ``parse()`` 不再在 ``max`` 缺失时扫 ``records``——直方图行形如 ``[low, high, n]``，
    旧实现会把 bin 上界或计数 n 当成 prod 写进产物（P0-3）。
  * peek 与带锁模式都识别 **4xx / data_unavailable 终态**并立即退出，不再重试到超时（P1-7）。
  * 带锁模式去掉「外层 20s 套内层 240s」的嵌套轮询：内层 ``get_production_correlation``
    已自带完整窗口，外层只按 ``retry_after`` 退避（P1-7）。
  * 产物补 ``source`` / ``status`` / ``histogram``，供 ``prod_peek_ingest.py`` 校验后落库。
"""
import argparse, asyncio, json, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "world-quant-brain-mcp"))
from brain_api import BrainApiClient  # noqa: E402

#: 产物统一来源标记（登记于 wqb.store.CORR_SOURCES，2026-11-10）
PEEK_SOURCE = "prod_peek"


def parse(j):
    """只认平台契约里的 ``max`` 字段；缺失即返回 None。

    ⚠ 绝不回退去扫 ``records``：那是直方图 ``[low, high, n]``，取其中最大数值会得到
    bin 上界（如 1.0）或计数 n（成千上万），把它当 prod 写进产物会直接污染判闸。
    """
    if not isinstance(j, dict):
        return None
    sch = j.get("schema") or {}
    for v in ((sch or {}).get("max"), j.get("max"), j.get("max_correlation")):
        if v is None:
            continue
        try:
            f = float(v)
        except (TypeError, ValueError):
            continue
        # 值域校验：相关性必须落在 [0, 1]，越界按「没有」处理
        if 0.0 <= f <= 1.0:
            return f
    return None


def _write_result(path, alpha_id, value, payload, status="ok"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rec = {
        "alpha_id": alpha_id,
        "prod": value,
        "histogram": (payload or {}).get("records"),
        "min": (payload or {}).get("min"),
        "at": time.strftime("%F %T"),
        "source": PEEK_SOURCE,
        "status": status,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    return rec


async def peek(alpha_id, tries, interval):
    """无锁只读探测：直接 GET /alphas/{id}/correlations/prod，不申请本地 correlation_slot。

    用途：本地账号级单并发锁被**别的进程**长期占用时（holder 指向陌生 alpha id），
    有锁路径会立刻返回 correlation_busy 而连一次平台读都发不出去。本模式绕过本地锁，
    只做只读探测：平台算好则返回 {records,max,min}，未算好返回 200 + 空体。
    注意：拿到空体只能说明「平台尚未算好」，**不等于失败，也不触发重算**。
    4xx 是终态（alpha 不存在 / 无权限 / 已提交），立即退出，不浪费剩余 tries。
    """
    b = BrainApiClient(); await b.ensure_authenticated()
    for i in range(1, tries + 1):
        try:
            r = await b._request("GET", f"/alphas/{alpha_id}/correlations/prod")
            code = getattr(r, "status_code", None)
            txt = (getattr(r, "text", "") or "").strip()
            if isinstance(code, int) and 400 <= code < 500:
                print(f"[{i}] HTTP {code} 终态，停止探测：{txt[:160]}", flush=True)
                return
            if code != 200:
                print(f"[{i}] HTTP {code} {txt[:120]}", flush=True)
            elif not txt:
                print(f"[{i}] 空体（平台仍在算）", flush=True)
            else:
                try:
                    j = json.loads(txt)
                except Exception:
                    print(f"[{i}] 非 JSON 体: {txt[:160]}", flush=True)
                else:
                    v = parse(j)
                    if v is not None:
                        print(f"[{i}] ★ prod = {v}", flush=True)
                        out = os.path.join(ROOT, "results", f"prod_peek_{alpha_id}.json")
                        _write_result(out, alpha_id, v, j)
                        print(f"已写 {out}", flush=True)
                        return
                    print(f"[{i}] 有体无 max（不扫直方图）: {txt[:160]}", flush=True)
        except Exception as e:
            print(f"[{i}] EXC {type(e).__name__}: {str(e)[:120]}", flush=True)
        if i < tries:
            await asyncio.sleep(interval)
    print("peek 结束未取到值", flush=True)


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alpha_id")
    ap.add_argument("--minutes", type=float, default=45)
    ap.add_argument("--peek", action="store_true",
                    help="无锁只读探测（不申请 correlation_slot）")
    ap.add_argument("--tries", type=int, default=1, help="peek 模式探测次数")
    ap.add_argument("--interval", type=float, default=60, help="peek 模式间隔秒")
    args = ap.parse_args()

    if args.peek:
        await peek(args.alpha_id, max(1, args.tries), max(5.0, args.interval))
        return

    out = os.path.join(ROOT, "results", f"prod_wait_{args.alpha_id}.json")

    b = BrainApiClient(); await b.ensure_authenticated()
    deadline = time.time() + args.minutes * 60
    n = 0
    while time.time() < deadline:
        n += 1
        try:
            j = await b.get_production_correlation(args.alpha_id)
        except Exception as e:
            print(f"[{n}] EXC {type(e).__name__}: {str(e)[:120]}", flush=True)
            await asyncio.sleep(20); continue
        st = (j or {}).get("status") if isinstance(j, dict) else None
        # 终态：平台明确说「这颗拿不到数」，重试无意义
        if st == "data_unavailable":
            print(f"[{n}] data_unavailable 终态（http={j.get('http_status')}），停止", flush=True)
            return
        if st in ("correlation_busy", "pending"):
            # 内层已自带完整轮询窗口；外层只按平台/本地给出的 retry_after 退避，
            # 不再用固定 20s 去嵌套触发新一轮 240s 计算。
            ra = float((j or {}).get("retry_after") or (180 if st == "correlation_busy" else 195))
            wait = min(max(ra + 5, 30), 320)
            left = int(deadline - time.time())
            print(f"[{n}] {st}，退避 {wait:.0f}s（剩余 {left}s）", flush=True)
            await asyncio.sleep(wait); continue
        v = parse(j)
        if v is not None:
            print(f"[{n}] ★ prod = {v}", flush=True)
            _write_result(out, args.alpha_id, v, j if isinstance(j, dict) else {})
            print(f"已写 {out}", flush=True); return
        print(f"[{n}] status={st} 无值，20s 后重试", flush=True)
        await asyncio.sleep(20)
    print("超时未取到", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
