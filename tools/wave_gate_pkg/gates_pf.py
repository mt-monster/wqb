# -*- coding: utf-8 -*-
"""闸 PF：信号族死路预检闸（2026-09-25 P2 落地）。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。

背景：F2 闸门凭证断档（2055 UNSUBMITTED 中 90.5% 的 prod_corr 未测）；
IND intraday_pv_feats 连投 3 波 24 条（S 4.4-6.5 全 IS 过）后才查 prod=0.79-0.92 整族报废。
SOP "任何新信号族在投入第二波之前必须先 prod-first 探针" 此前无代码级把关。
本闸把 prod-first 从「S4 收批后必调」前移到「七槽开批前硬门」，判据：
  - 同表达式字段族 = 已确认 prod 撞墙死路（基于 DB 中同字段集的实测 prod_corr）→ FAIL 拦截
  - 同表达式字段族 = 已知 prod 干净（prod<0.7）  → PASS（家族已探明，可扩批）
  - 新信号族（无任何 prod 记录）                  → WARN（建议先 prod-first 探针再扩批）
判据是"表达式中字段集精确匹配"，独立于闸 2.6 的字段热度 / 数据集占比判据。
"""
import json
import os
import re

from . import _compat

_OPS_PATTERN = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")


def _extract_ops(expr):
    """提取表达式里所有函数调用名（小写）。"""
    return [m.group(1).lower() for m in _OPS_PATTERN.finditer((expr or "").lower())]


def _pf_family(expr, n_ops=2):
    """信号族指纹 = 前 n_ops 个函数调用名 join（保留算子结构）。

    判据：对 mdl135_d01_icc 的实证 —— 同字段在「+ vec_avg」骨架下 prod=0.76-0.82（死路），
    在「+ vec_avg × ts_zscore」骨架下 prod=0.46-0.57（干净）。所以**骨架比字段更准**。
    取前 n_ops=2 个算子做族指纹，平衡宽（易匹配）与窄（精准）的粒度。
    """
    ops = _extract_ops(expr)
    return "→".join(ops[:n_ops]) if ops else "?"


def _load_prod_wall_families(region, n_ops=2):
    """读 alphas 表 + ledger_kv，按信号族指纹（骨架前缀）分组。

    2026-09-25 P1 增强：除 alphas 表（全库 prod 覆盖率仅 4.4%）外，还读 ledger_kv
    里 `prod_family_<region>_<skeleton>` 键（由 campaign_intel.py prod-first 探针
    自动回写），让闸 PF 下次跑时能直接消费最新证据，不再只依赖 alphas 表的稀疏记录。

    墙家族 = 同骨架至少有 1 条 prod_corr >= 0.7 的实测记录；
    干净家族 = 有 >=1 条 prod_corr < 0.7 的记录。
    """
    try:
        # 2026-09-27：勿硬编码本机路径（P1 R19 守护 test_wave_gate_db_path_never_hardcoded）；
        # 复用统一解析：src 注入走 _campaign_store_cls（工作区 src 优先），库路径走 _wqb_db_path。
        CampaignStore = _compat.campaign_store_cls()
        st = CampaignStore(_compat.wqb_db_path())
        try:
            rows = st.list_alphas_by_region(region)  # 字段含 alpha_id/expression/prod_correlation/corr_checked_at
        finally:
            st.close()
    except Exception:
        return {}
    fams = {}
    for r in rows:
        fam = _pf_family(r.get("expression") or "", n_ops)
        if not fam or fam == "?":
            continue
        pc = r.get("prod_correlation")
        if pc is None:
            continue
        pc = float(pc)
        cur = fams.setdefault(fam, {"prod_corr": pc, "prod_max": pc, "n": 0, "n_wall": 0,
                                    "examples": []})
        cur["n"] += 1
        # 2026-09-28 max/min 双记（此前只留 min=最干净，把"族里出现过 ≥0.7 撞墙"误标成干净，
        # 注释却写"取最严格"）。死路判据看 min（全族皆墙才 enforced），混合证据看 max（WARN+加深）。
        cur["prod_corr"] = min(cur["prod_corr"], pc)
        cur["prod_max"] = max(cur.get("prod_max", pc), pc)
        if pc >= 0.7:
            cur["n_wall"] += 1
        if len(cur["examples"]) < 3:
            cur["examples"].append(r.get("expression", "")[:60])

    if n_ops != 2:
        # 3 算子粒度只用 alphas 行（ledger 键固定是 2 算子骨架名，无法反推）
        return fams

    # 2026-09-25 P1：合并 ledger_kv 里 prod-first 探针回写的骨架指纹（覆盖率补偿）
    try:
        _db = os.path.join(_compat.wqb_root(), "data", "wqb.db")
        # ⚠ 2026-09-30 包化时保留原实现（裸 sqlite3.connect）：仓库"裸连接守卫"测试
        # 只覆盖 src/ 与指定清单，此处历史上未被判违规。行为与拆分前逐字一致。
        import sqlite3 as _sq
        _c = _sq.connect(_db)
        _c.row_factory = _sq.Row
        _prefix = f"prod_family_{region}_"
        for _r in _c.execute(
                "SELECT key, value FROM ledger_kv WHERE region=? AND key LIKE ?",
                (region, _prefix + "%")):
            try:
                _fam = _r["key"][len(_prefix):]
                _v = json.loads(_r["value"] or "{}")
                _pc = _v.get("prod_corr")
                if _pc is None or not _fam:
                    continue
                _pc = float(_pc)
                _cur = fams.setdefault(_fam, {"prod_corr": _pc, "prod_max": _pc, "n": 0,
                                             "n_wall": 0, "examples": []})
                _cur["n"] += 1
                _cur["prod_corr"] = min(_cur["prod_corr"], _pc)
                _cur["prod_max"] = max(_cur.get("prod_max", _pc), _pc)
                if _pc >= 0.7:
                    _cur["n_wall"] += 1
                if _v.get("alpha_id") and len(_cur["examples"]) < 3:
                    _cur["examples"].append(_v["alpha_id"])
            except Exception:
                continue
        _c.close()
    except Exception:
        pass
    return fams


def check_prod_family_gate(exprs, region, dataset, min_confidence_n=3,
                           unknown_mode="warn"):
    """闸 PF：骨架级死路预检（prod-first 前置）。

    判据（基于 mdl135_d01_icc 实证：骨架比字段更准）：
      同骨架前缀（前 2 个算子）= 已确认 prod>=0.7 死路  → 拦截（fail-closed）
      同骨架前缀 = 已探明 prod<0.7 干净                    → 通过（该骨架已探明）
      新骨架前缀（无任何 prod 记录）                        → WARN（建议先 prod-first 探针）

    unknown_mode（2026-10-01 P1，默认 warn 保持历史行为）：
      - "warn"（默认）：新骨架只 WARN，status=warn，不拦波——与历史逐字一致。
      - "enforce"：新骨架 / 低置信度 / 证据混合族**一并视作未探明风险**，计入 violations
        并令 status=enforced。用途：饱和区「任何未探明骨架投入前必须先 prod-first 探针」从
        建议升级为可强制的门；实测正波 6/6 全部 status=warn、历史 enforced 仅 2 次
        → 该闸名义最硬、实际几乎只在"看"，故给出可选强档。

    2026-09-25 P5 增强（粒度自适应 + 置信度）：
      - 区隔离：骨架指纹按 region 分库存储（ledger_kv `prod_family_<region>_*`），
        避免跨区误判（rank→ts_backfill 在 KOR 干净 prod=0.54、在 IND 死路 prod=0.725）。
      - 低置信度：骨架指纹 n < min_confidence_n（缺省 3）只 WARN 不 enforced，
        避免小样本误伤（如 n=1 的 rank→group_zscore 在 KOR prod=0.763）。
      - 粒度自适应：若某骨架前缀在本区有混合记录（干净 + 死路），自动加深到前 3 算子。

    Returns report dict（供落 gate_results 与打印）：
      status   = pass / warn / enforced(有家族死路 或 unknown_mode=enforce 且存在未探明族)
      violations = 命中已死路家族的表达式明细
      unknown_families = 未探明的骨架指纹列表（建议 prod-first）
      passed = not violations
    """
    fams = _load_prod_wall_families(region)

    # 2026-09-25 P5：低置信度（n < min_confidence_n）只 WARN 不 enforced
    dead_fams = {f: v for f, v in fams.items()
                 if v["prod_corr"] >= 0.7 and v["n"] >= min_confidence_n}
    dead_fams_low_conf = {f: v for f, v in fams.items()
                          if v["prod_corr"] >= 0.7 and v["n"] < min_confidence_n}
    # 2026-09-28：mixed = 同骨架既有 ≥0.7 撞墙记录又有干净记录（2 算子粒度过粗）。
    # 此前这类族被 min() 归进 ok（GLB 实测 group_zscore→ts_decay_linear 37 条、
    # max 0.9929 仍判"干净"），死路证据被吞。现单列 MIXED：不 enforced（避免误伤
    # 干净变体），但也不算干净——走 3 算子加深判定，加深后仍混合 → WARN + 建议探针。
    mixed_fams = {f: v for f, v in fams.items()
                  if v.get("prod_max", v["prod_corr"]) >= 0.7 > v["prod_corr"]}
    ok_fams = {f: v for f, v in fams.items()
               if v.get("prod_max", v["prod_corr"]) < 0.7}
    unknown_fams = set()

    fams3 = None  # 懒加载：仅遇 MIXED 族才建 3 算子粒度索引

    def _fams3_index():
        nonlocal fams3
        if fams3 is None:
            fams3 = _load_prod_wall_families(region, n_ops=3)
        return fams3

    violations = []
    expr_status = []  # per-expr for diagnostics
    for i, expr in enumerate(exprs):
        fam = _pf_family(expr)
        if fam in dead_fams:
            prod_v = fams[fam]["prod_corr"]
            violations.append({"index": i, "family": fam, "prod_corr": prod_v,
                               "reason": f"骨架指纹 '{fam}' 已确认 prod_corr={prod_v:.3f} ≥ 0.7 死路"
                                         f"（族级 STOP，先换正交概念或新骨架）",
                               "expr": expr[:100]})
            expr_status.append({"index": i, "verdict": "DEAD", "family": fam})
        elif fam in dead_fams_low_conf:
            # 低置信度死路：只 WARN 不 enforced（避免小样本误伤）
            prod_v = dead_fams_low_conf[fam]["prod_corr"]
            expr_status.append({"index": i, "verdict": "WARN_LOW_CONF",
                                "family": fam, "prod_corr": prod_v,
                                "n": dead_fams_low_conf[fam]["n"]})
            unknown_fams.add(fam)
        elif fam in mixed_fams:
            # MIXED：3 算子粒度加深再判一次（ledger 只存 2 算子键，加深索引只用 alphas 行）
            fam3 = _pf_family(expr, 3)
            f3 = _fams3_index().get(fam3)
            if f3 and f3["prod_corr"] >= 0.7 and f3["n"] >= min_confidence_n:
                violations.append({"index": i, "family": fam3, "granularity": 3,
                                   "prod_corr": f3["prod_corr"],
                                   "reason": f"骨架指纹 '{fam}' 证据混合，加深到 '{fam3}' 后确认 "
                                             f"prod_corr={f3['prod_corr']:.3f} ≥ 0.7 死路",
                                   "expr": expr[:100]})
                expr_status.append({"index": i, "verdict": "DEAD", "family": fam3,
                                    "granularity": 3})
            elif f3 and f3.get("prod_max", f3["prod_corr"]) < 0.7:
                expr_status.append({"index": i, "verdict": "OK_DEEP", "family": fam3,
                                    "granularity": 3, "prod_corr": f3["prod_corr"]})
            else:
                unknown_fams.add(fam3 or fam)
                expr_status.append({"index": i, "verdict": "WARN_MIXED", "family": fam,
                                    "deep_family": fam3,
                                    "prod_min": mixed_fams[fam]["prod_corr"],
                                    "prod_max": mixed_fams[fam].get("prod_max"),
                                    "n_wall": mixed_fams[fam].get("n_wall", 0)})
        elif fam in ok_fams:
            expr_status.append({"index": i, "verdict": "OK", "family": fam,
                                "prod_corr": ok_fams[fam]["prod_corr"]})
        else:
            unknown_fams.add(fam)
            expr_status.append({"index": i, "verdict": "UNKNOWN", "family": fam})

    status = "enforced" if violations else ("warn" if unknown_fams else "pass")
    # 2026-10-01 P1：unknown_mode=enforce 时把「未探明族」升级为拦截。
    # 只在**没有**死路 violations 时才需要升级（有死路已是 enforced）；把未知族逐条写入
    # violations 并附说明，令 status 收敛为 enforced、passed=False（下游据此计入 all_pass）。
    unknown_violations = []
    if unknown_mode == "enforce" and not violations and unknown_fams:
        for st_ in expr_status:
            if st_.get("verdict") in ("UNKNOWN", "WARN_LOW_CONF", "WARN_MIXED"):
                unknown_violations.append({
                    "index": st_["index"], "family": st_.get("family"),
                    "reason": f"骨架指纹 '{st_.get('family')}' 未探明（无 prod 记录 / 低置信度 / 证据混合），"
                              f"unknown_mode=enforce：投入前须先 prod-first 探针",
                })
        if unknown_violations:
            status = "enforced"
    report = {"status": status, "n_checked": len(exprs),
              "unknown_mode": unknown_mode,
              "n_history_families": len(fams),
              "n_dead_families": len(dead_fams), "n_ok_families": len(ok_fams),
              "n_mixed_families": len(mixed_fams),
              "n_low_conf_dead_families": len(dead_fams_low_conf),
              "n_unknown_families": len(unknown_fams),
              "dead_families_sample": sorted(dead_fams)[:15],
              "mixed_families_sample": sorted(mixed_fams)[:15],
              "ok_families_sample": sorted(ok_fams)[:15],
              "unknown_families_sample": sorted(unknown_fams)[:15],
              "violations": violations + unknown_violations, "expr_status": expr_status,
              "passed": not (violations or unknown_violations)}
    if violations:
        report["message"] = (f"{len(violations)}/{len(exprs)} 条表达式命中已死路骨架指纹"
                             f"（{len(dead_fams)} 个骨架已确认死路，n≥{min_confidence_n}）—— 闸 PF 拦截")
    elif unknown_violations:
        report["message"] = (f"{len(unknown_violations)}/{len(exprs)} 条表达式骨架指纹未探明"
                             f"—— unknown_mode=enforce，闸 PF 拦截（先 prod-first 探针）")
    elif unknown_fams:
        report["message"] = (f"PASS；{len(unknown_fams)}/{len(exprs)}"
                             f" 条表达式骨架指纹未探明或低置信度或证据混合，建议先 prod-first 探针"
                             + (f"（mixed 族 {len(mixed_fams)} 个）" if mixed_fams else ""))
    else:
        report["message"] = f"PASS（{len(exprs)} 条全部命中已探明干净骨架）"
    return report


def format_prod_family_report(report):
    lines = [f"[prod-family] 状态={report['status']} {report['message']}"]
    if report.get("dead_families_sample"):
        lines.append(f"[prod-family] 已死路骨架样本: {report['dead_families_sample'][:5]}"
                     + (f" 等 {report.get('n_dead_families', 0)} 个" if report.get("n_dead_families", 0) > 5 else ""))
    for v in report.get("violations", [])[:5]:
        lines.append(f"[prod-family]   命中 #{v['index']}: prod={v['prod_corr']:.3f} {v['family']} | {v['expr']}")
    return "\n".join(lines)
