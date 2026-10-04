# -*- coding: utf-8 -*-
"""prod_bucket_scan.py — prod 直方图 n=0 判据预筛（本波 16/16 实证）。

★ 判据：对已回测的 alpha 查 prod 直方图，看 [0.7,0.8) 桶的 n 值：
    n=0  ⇔ 该族存在过线窗口，值得扫窗口网格
    n>=1 ⇔ 该族无论怎么调窗口都过不了 0.70（单钉子卡死）
  实证：d50（10/10）+ d53（6/6）+ d54（4/4）= 16/16 精确。

用法:
  python tools/prod_bucket_scan.py <id1> [<id2> ...]      # 查指定 alpha
  python tools/prod_bucket_scan.py --file ids.txt          # 从文件读每行一个 id
  python tools/prod_bucket_scan.py --file ids.txt --labels labels.txt
  python tools/prod_bucket_scan.py 78NoOeVx --all-buckets  # 打全直方图（D0-P 诊断前置分型用）
输出: 每行 `id  prod_max  n([0.7,0.8))  判定(SCAN/DEAD)`；--all-buckets 另附各桶计数与三型判定
"""
import argparse, asyncio, json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, "world-quant-brain-mcp")


async def fetch_prod(brain, aid, retries=4):
    for _ in range(retries):
        try:
            r = await brain._request("GET", f"{brain.base_url}/alphas/{aid}/correlations/prod")
            t = (r.text or "").strip()
            if t:
                d = r.json()
                if d:
                    return d
        except Exception:
            pass
        await asyncio.sleep(12)
    return {}


def bucket_n(d, lo=0.7, hi=0.8):
    recs = d.get("records") or []
    for row in recs:
        if isinstance(row, (list, tuple)) and len(row) >= 3:
            try:
                if abs(float(row[0]) - lo) < 1e-9 and abs(float(row[1]) - hi) < 1e-9:
                    return int(row[2])
            except Exception:
                continue
    return None


def all_buckets(d):
    """全部桶计数 [(lo, hi, n)]，只回 n>0 的桶（按 lo 升序）。"""
    out = []
    for row in d.get("records") or []:
        if isinstance(row, (list, tuple)) and len(row) >= 3:
            try:
                lo, hi, n = float(row[0]), float(row[1]), int(row[2])
            except Exception:
                continue
            if n > 0:
                out.append((lo, hi, n))
    return sorted(out)


def wall_shape(bs):
    """D0-P 诊断前置第 1 步的三型分型（决策表 decision-table.md D0-P）。

    口径：0.6-0.7 桶计数 = 拥挤度（密墙 vs 钉子）；0.7+ 计数 = 压住过线的钉子数。
    """
    n_6_7 = sum(n for lo, hi, n in bs if 0.59 <= lo < 0.70)
    n_ge7 = sum(n for lo, hi, n in bs if lo >= 0.70)
    if n_ge7 == 0:
        return f"no-0.7+ (n_6_7={n_6_7})"
    if n_6_7 >= 100:
        return f"dense-wall 密墙型 (n_6_7={n_6_7}, n_ge7={n_ge7})"
    if n_6_7 <= 20 and n_ge7 <= 3:
        return f"single-nail 单颗钉子型 (n_6_7={n_6_7}, n_ge7={n_ge7})"
    return f"mid (n_6_7={n_6_7}, n_ge7={n_ge7})"


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--file")
    ap.add_argument("--labels")
    ap.add_argument("--all-buckets", action="store_true",
                    help="额外打印全部非空 prod 直方图桶计数与 D0-P 三型分型（诊断前置用）")
    a = ap.parse_args()

    ids = list(a.ids)
    labels = {}
    if a.file:
        with open(a.file, encoding="utf-8-sig") as f:
            ids += [l.strip().split("\t")[0] for l in f if l.strip()]
        if a.labels and os.path.exists(a.labels):
            with open(a.labels, encoding="utf-8-sig") as f:
                labs = [l.strip() for l in f if l.strip()]
            for i, lab in zip(ids, labs):
                labels[i] = lab

    sys.path.insert(0, "world-quant-brain-mcp")
    from brain_api import brain_client as brain
    await brain.ensure_authenticated()

    sem = asyncio.Semaphore(3)

    async def one(aid):
        async with sem:
            d = await fetch_prod(brain, aid)
            mx = (d.get("schema") or {}).get("max", d.get("max"))
            n = bucket_n(d)
            verdict = "?" if n is None else ("SCAN(过线可期)" if n == 0 else "DEAD(单钉子卡死)")
            bs = all_buckets(d) if a.all_buckets else []
            return aid, mx, n, verdict, bs

    res = await asyncio.gather(*[one(i) for i in ids])
    print(f"{'id':<12}{'label':<14}{'prod_max':<10}{'n[0.7,0.8)':<12}判定")
    for aid, mx, n, v, bs in res:
        print(f"{aid:<12}{labels.get(aid,''):<14}{str(mx):<10}{str(n):<12}{v}")
        if bs:
            print(f"  buckets: " + " ".join(f"[{lo:.1f},{hi:.1f})={n}" for lo, hi, n in bs))
            print(f"  D0-P 分型: {wall_shape(bs)}")


asyncio.run(main())
