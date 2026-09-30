# -*- coding: utf-8 -*-
"""候选解析（DB / JSON / txt / 单条）+ 逐条状态回写。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。
"""
import json
import os
import sys

from ._paths import _campaign_store_cls, _wqb_db_path
from .payload import _env_unknown_only


def parse_candidates(a):
    """候选解析 → [(id_or_index, expr)]；兼容 DB / JSON / txt / 单条。"""
    if getattr(a, "from_db", False):
        CampaignStore = _campaign_store_cls(a.campaign_dir)
        st = CampaignStore(_wqb_db_path(a.campaign_dir))
        try:
            region = a.region
            if not region:
                settings = json.load(open(os.path.join(a.campaign_dir, "config", "settings.json"), encoding="utf-8"))
                region = settings.get("region")
            rows = st.list_expressions(region, str(a.wave), dataset=a.dataset)
            if not rows:
                rows = st.list_expressions(region, str(a.wave))
            # 2026-09-03 修复：--from-db 时保留 expressions.id，避免 gate_results.syntax.items[].id 是 1-N 序号
            # 2026-09-03 修复2：排除 superseded 行（坏行/已提交候选不应再入门禁与回测）
            # 2026-09-09 D12 修复：同时排除 dropped（纪律废弃终态）。此前只排 superseded，
            # Agent dropped 的零 alpha 骨架（含 vec_* 类型不兼容的 11637）仍入门禁，
            # 一条 [TYPE] FAIL 拖垮整波 all_pass。
            items = [{"id": r.get("id"), "expression": r.get("expression")} for r in rows
                     if r.get("expression") and r.get("status") not in ("superseded", "dropped")]
        finally:
            st.close()
        if not items:
            raise SystemExit(f"db 无候选: wave={a.wave} dataset={a.dataset}")
    elif a.candidates:
        d = json.load(open(a.candidates, encoding="utf-8"))
        items = d if isinstance(d, list) else (d.get("expressions") or d.get("exprs") or [])
    elif a.exprs_file:
        items = [ln.strip() for ln in open(a.exprs_file, encoding="utf-8") if ln.strip()]
    elif a.expr:
        items = [a.expr]
    else:
        raise SystemExit("need --from-db / --candidates / --exprs-file / --expr 之一")
    out = []
    for i, it in enumerate(items, 1):
        if isinstance(it, dict):
            e = it.get("expr") or it.get("code") or it.get("expression")
            cid = it.get("id") or it.get("name") or i
        elif isinstance(it, str):
            e, cid = it, i
        else:
            continue
        if e:
            out.append((cid, e))
    if not out:
        raise SystemExit("候选解析为空")
    return out


def _write_back_gate_status(campaign, region, wave, gate_json, seeded):
    """--exprs-file / --candidates / --expr 入库的候选：按 gate.py 逐条结论回写 status。

    2026-09-27 R7/R21：此前候选在门禁**之前**以 gated 入库、结论出来后不回写 ——
    gated 同时表示"送过闸"与"过了闸"，FAIL 候选照样计入积压闸的 pending+gated
    （KOR 真实复现：三次重跑门禁留下 117 条 gated，积压 32% 越过 30% 上限拦下下一波）。
    现在：入库为 pending → 静态闸 1-5 逐条 PASS → gated；FAIL → fail（与 pipeline 坏式
    回写同一状态：build_wave / 去重不再重选；reason 记闸门原因，重跑门禁通过会改回 gated）。
    只因闸门环境缺失而 FAIL 的（issues 全是 [SYNTAX_UNKNOWN]/[ARITY_UNKNOWN]）保持 pending：
    那是"没校验"，不是"式子坏"——同日真实环境复现过 op_arity 不可达时 39/39 全记 fail。
    只动本批入库的式子；批级闸（多样性 / 知识闸）不改逐条状态。
    """
    verdicts = {}
    for it in (gate_json.get("report") or []):
        e = str(it.get("expr") or "").strip()
        if e:
            verdicts[e] = it
    if not verdicts:
        print("[state] gate.py 未回传逐条结论（toolkit 旧版？），候选保持 pending")
        return None
    CampaignStore = _campaign_store_cls(campaign)
    st = CampaignStore(_wqb_db_path(campaign))
    n_gated = n_fail = n_unverified = 0
    try:
        ids = {}
        for row in st.list_expressions(region, str(wave)):
            ex = str(row.get("expression") or "").strip()
            if ex and row.get("id") is not None:
                ids.setdefault(ex, int(row["id"]))
        passed = []
        for e in dict.fromkeys(x.strip() for x in seeded):
            it, eid = verdicts.get(e), ids.get(e)
            if it is None or eid is None:
                continue
            if it.get("pass"):
                passed.append(eid)
            elif _env_unknown_only(it.get("issues")):
                n_unverified += 1
            else:
                reason = ("gate FAIL: " + "；".join(map(str, it.get("issues") or [])))[:200]
                res = st.set_expression_status(region, str(wave), "fail", ids=[eid], reason=reason)
                n_fail += int(res.get("n_updated") or 0)
        if passed:
            res = st.set_expression_status(region, str(wave), "gated", ids=passed,
                                           reason="gate PASS（静态闸 1-5）")
            n_gated += int(res.get("n_updated") or 0)
    finally:
        st.close()
    print(f"[state] 逐条状态回写：gated {n_gated} / fail {n_fail}（FAIL 候选不再计入积压）"
          + (f" / 未判定 {n_unverified}（闸门环境缺失，保持 pending）" if n_unverified else ""))
    return {"gated": n_gated, "fail": n_fail, "unverified": n_unverified}
