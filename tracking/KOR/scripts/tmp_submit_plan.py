# -*- coding: utf-8 -*-
"""SI-SUBMIT v3 —— KOR SI 专项提交清单（2026-09-29 扩池至 18 颗后版）。

池内 18 颗 prod<0.7（含 2 ACTIVE），按「结构族去重」选出提交序。
硬性前置（全部已核）：四闸 PASS / CW PASS / prod<0.7 / description≥100 三段式。

族划分（按 base signal 结构，2026-09-29 扩池后）：
  族 A: vec_avg 比值 + hump + sector/industry
  族 B: vec_sum 比值 + ts_decay_linear + industry
  族 C: vec_sum 比值 + ts_decay_linear + subindustry
  族 D: vec_sum 比值 + ts_decay_linear + industry(长窗 400/900)
  族 F: **净额差** subtract/divide + dl + industry/subindustry  [新增]
  族 G: vec_avg 比值 + ts_decay_linear + subindustry           [新增]

★ 扩池结论：**分组轴是 prod 主导变量**（subindustry 0.57 << industry 0.69 << sector 0.77），
  信号微结构（vec_sum比值 / vec_avg比值 / 净额差）影响很小。

纪律：同族一次只提 1 颗（兄弟连提会互相抬 prod）。

用法: python tmp_submit_plan.py            # 按序提交全量
      python tmp_submit_plan.py --dry      # 只打印计划
      python tmp_submit_plan.py --only=mLmGQEq9,QPbxpJ8K   # 只提指定
"""
import asyncio, json, sys, os
REPO = r"D:\coding\traeCN_project\wqb"
sys.path.insert(0, os.path.join(REPO, "world-quant-brain-mcp"))

PLAN = [
    # order, id,        family, S,    F,    prod,   结构摘要
    (1, "mLmGQEq9", "A", 2.72, 2.12, 0.6011, "hump(group_rank(vec_avg比值), sector) h2.5 dec20"),
    (2, "JjNAkqbn", "B", 2.31, 1.75, 0.6958, "hump(group_rank(dl500(RS), industry), h2.5)"),
    (3, "vRrQ5Npr", "F", 1.76, 1.18, 0.5695, "hump(group_rank(dl500(净额差), subindustry), h2.5)"),
    (4, "QPbxpJ8K", "C", 1.73, 1.15, 0.5753, "hump(group_rank(dl500(RS), subindustry), h2.5)"),
    # 备选（同族或有余额）
    (5, "e7bjnPk6", "G", 1.80, 1.22, 0.5759, "(备G) dl500(vec_avg比值) subindustry h2.5"),
    (6, "VkaWXGmb", "F", 2.35, 1.79, 0.6932, "(备F) dl500(净额差) industry h2.5"),
    (7, "rKOxJLd1", "D", 2.30, 1.74, 0.6932, "(备D) dl400(RS) industry h2.5"),
    (8, "E5pjx9q0", "A", 2.50, 1.85, 0.6002, "(备A) hump(vec_avg比值, industry) h2.5"),
    (9, "omLd9oEJ", "C", 1.86, 1.27, 0.5755, "(备C) dl500(RS) subindustry h2.0"),
    (10, "JjN9nG0n", "C", 1.72, 1.14, 0.5749, "(备C) dl300(RS) subindustry h2.5"),
    (11, "qMxRnNkO", "C", 1.74, 1.16, 0.5807, "(备C) dl1260(RS) subindustry h2.5"),
    (12, "akbpAj99", "D", 2.27, 1.70, 0.6886, "(备D) dl900(RS) industry h2.5"),
    (13, "d5bMPkWY", "A", 1.71, 1.19, 0.4365, "(备A) vec_avg比值 subindustry h3"),
]


async def main():
    dry = "--dry" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = set(a.split("=", 1)[1].split(","))
    from brain_api import brain_client
    await brain_client.ensure_authenticated()
    print("KOR SI 提交计划 v3（族去重；REGULAR 4/ET日）：")
    for row in PLAN:
        o, aid, fam, s, f, prod, desc = row
        mark = "★提" if o <= 4 else "备"
        print(f"  {o}. [{fam}] {mark} {aid}  S={s} F={f} prod={prod}  {desc}")
    if dry:
        return
    for row in PLAN:
        o, aid, fam, s, f, prod, desc = row
        if only and aid not in only:
            continue
        r = await brain_client._request("POST", f"https://api.worldquantbrain.com/alphas/{aid}/submit")
        body = r.text.strip()
        print(f"\n[{o}] [{fam}] {aid} POST {r.status_code} {'(空体=受理)' if not body else ''}")
        if r.status_code in (200, 201) and not body:
            await asyncio.sleep(5)
            r2 = await brain_client._request("POST", f"https://api.worldquantbrain.com/alphas/{aid}/submit")
            print(f"    补发 {r2.status_code}: {r2.text.strip()[:400]}")
        else:
            try:
                for c in r.json().get("is", {}).get("checks", []):
                    if c.get("result") != "PASS":
                        print("    ", json.dumps(c, ensure_ascii=False))
            except Exception:
                print("    ", body[:300])
        await asyncio.sleep(3)


asyncio.run(main())
