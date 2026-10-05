# -*- coding: utf-8 -*-
"""每波门禁编排器：main() 编排（argparse 契约在入口 shim）。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆分而来。本文件只做**编排**：
按序调用各闸位模块，聚合成终止判定并落库。
argparse 契约在入口 shim `tools/wave_gate.py`（位置敏感，见 shim 的 module docstring）；
各闸实现在 `gates_*`。
"""
import json
import os
import subprocess
import sys
import time

from . import _compat
from ._paths import _TOOLKIT_CANDIDATES, find_script
from .candidates import _write_back_gate_status, parse_candidates
from .gates_familyshape import _family_shape_gate
from .gates_inspect import run_inspect_gate, run_prod_saturation_gate, resolve_inspect_mode
from .gates_pf import check_prod_family_gate, format_prod_family_report
from .gates_quality import run_quality_stage, run_variant_clustering
from .gates_semantic import _semantic_gate
from .gates_syntax import run_syntax_gate
from .gates_waiver import _waiver_phase
from .payload import (env_error_exit, gate_error_exit, gate_fail_reasons,
                      parse_gate_payload)


def _tool_import(name):
    """从 tools/ 目录动态 import（与拆分前同口径）。"""
    tools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    return __import__(name)


def main(argv=None, parser_factory=None):
    """编排入口。

    `parser_factory` 由 shim（`tools/wave_gate.py`）注入 —— argparse 契约**必须**
    字面保留在入口脚本内，否则 `wqb.workflow._common.validate_argv` 的静态解析
    会 fail-open（详见 shim 的 module docstring）。
    """
    ap = parser_factory()
    a = ap.parse_args(argv)

    items = parse_candidates(a)
    campaign = a.campaign_dir.rstrip("/\\")
    tag = str(a.wave) if a.wave and a.wave != "0" else str(int(time.time()))

    # 体检硬门缺包策略（2026-09-17 P1-1：由"恒静默放行"升级为可选 fail-closed）
    _inspect_mode = resolve_inspect_mode(a.inspect_mode)

    # 逃生口 → waiver 检查（首屏；见 gates_waiver._waiver_phase）
    _rg = _compat.load_region_gates()
    _wv_region = a.region or _compat.settings_region(campaign) or os.path.basename(campaign).upper()
    _wv_decisions = _waiver_phase(a, campaign, _wv_region, _inspect_mode, _rg)

    # ---- 开波前区域闸（2026-09-17 P0-1 下沉）----
    # signal_floor / stop_rules / backlog 三道闸原先只在 workflow 的 S2/S3 节点生效；
    # 直调本脚本会绕过它们（实证 JPN 2026-09-16）。模式由 toolkit region_gates.resolve_mode 定：
    # --gate-mode > WQB_GATE_MODE > 按日期的缺省（灰度期 warn，2026-10-12 起 enforce）。
    if _rg is None:
        print("[wave_gate] [region-gates] ★未找到 toolkit region_gates，本次跳过开波闸"
              "（设 WQ_TOOLKIT_DIR 可解）", file=sys.stderr)
    else:
        _region_for_gates = a.region
        if not _region_for_gates:
            try:
                with open(os.path.join(campaign, "config", "settings.json"),
                          encoding="utf-8") as f:
                    _region_for_gates = (json.load(f) or {}).get("region")
            except Exception:
                _region_for_gates = None
        if not _region_for_gates:
            _region_for_gates = os.path.basename(campaign).upper()
        _resolve = getattr(_rg, "resolve_mode", None)
        if _resolve is not None:
            _mode, _mode_note = _resolve(a.gate_mode)
            _rep = _rg.run_region_gates(campaign, _region_for_gates, mode=_mode,
                                        dataset=a.dataset, mode_note=_mode_note)
        else:  # 安装位的 toolkit 早于 2026-09-27（没有灰度截止日）：沿用旧缺省，并提示同步
            print("[wave_gate] [region-gates] ★toolkit 安装位过旧（缺 resolve_mode），沿用旧缺省 warn；"
                  "请跑 python tools/sync_skills.py", file=sys.stderr)
            _mode = a.gate_mode or os.environ.get("WQB_GATE_MODE", _rg.MODE_WARN)
            _rep = _rg.run_region_gates(campaign, _region_for_gates, mode=_mode,
                                        dataset=a.dataset)
        if not _rep.get("ok", True):
            print(f"[wave_gate] ★★ 开波被阻断（gate-mode=enforce，命中 "
                  f"{'、'.join(_rep.get('hits') or [])}）", file=sys.stderr)
            sys.exit(2)

    # ---- 0) GEM 候选池校验（可选）----
    gem_report = None
    if a.gem_validate:
        try:
            from gem_validator import GEMValidator
            validator = GEMValidator()
            candidates_for_gem = [{"id": cid, "expression": e} for cid, e in items]
            gem_report = validator.validate_wave(candidates_for_gem, tag, a.min_gem_ratio)
            print(f"[gem  ] GEM 候选: {gem_report['gem_count']}/{gem_report['total']} "
                  f"({gem_report['gem_ratio']:.1%}) => {'PASS' if gem_report['pass'] else 'FAIL'}")
            if not gem_report["pass"]:
                print(f"[gem  ] 非 GEM 候选: {len(gem_report['non_gem_candidates'])} 条")
        except Exception as e:
            print(f"[gem  ] GEM 校验失败（不阻断）: {e}")

    # ---- 0.6) 机制-形状一致性软闸（--template-family 指定时启用，WARN 不阻断）----
    family_shape_report = None
    if a.template_family:
        family_shape_report = _family_shape_gate(items, a, campaign)

    # ---- 0.5) S1 字段候选池强制校验（2026-09-03 落地，防 wave=170 事故）----
    s2_field_report = None
    if a.s2_field_validate:
        try:
            from s2_field_validator import validate_wave_fields
            db_path = _compat.wqb_db_path(campaign)
            # region 缺省时从 settings.json 读取（与 parse_candidates 对齐）
            region = a.region
            if not region:
                settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
                region = settings.get("region")
            exprs_only = [e for _, e in items]
            s2_field_report = validate_wave_fields(
                region, str(tag), a.dataset, exprs_only, db_path
            )
            print(f"[s2fld] {s2_field_report['message']}")
            if s2_field_report["extra"]:
                print(f"[s2fld] 额外字段（非 S1 推荐）: {s2_field_report['extra'][:5]}")
            if s2_field_report["forbidden"]:
                print(f"[s2fld] 禁用字段命中: {s2_field_report['forbidden']}")
            if not s2_field_report["pass"] and a.s2_field_block:
                print(f"[s2fld] BLOCK 模式：计入 FAIL")
        except Exception as e:
            print(f"[s2fld] S1 字段校验失败（不阻断）: {e}")
            s2_field_report = {"pass": True, "message": f"校验异常: {e}"}

    # ---- 0.2) 闸 SEM：字段语义归类硬门（2026-09-28 落地，fail-closed）----
    # 模式解析：CLI > 环境变量 WQB_SEM_MODE > 缺省 enforce（与 WQB_INSPECT_MODE / WQB_GATE_MODE 同构）
    _sem_mode = (os.environ.get("WQB_SEM_MODE") or "enforce").strip().lower()
    if a.skip_semantic_gate or a.semantic_gate == "off":
        _sem_mode = "off"
    elif a.semantic_gate in ("warn", "enforce"):
        _sem_mode = a.semantic_gate
    if _sem_mode == "off":
        print("[sem  ] ⚠ 闸 SEM 已关闭（--skip-semantic-gate / WQB_SEM_MODE=off）："
              "非信号字段（货币代码/汇率/标识符）不会被拦截，语义废产物可能进回测烧配额。")
    sem_report = None
    if _sem_mode != "off":
        try:
            sem_report = _semantic_gate(a, campaign, items)
            items = sem_report["items"]  # 已剔除黑名单命中项
            if sem_report["ledger_missing"]:
                print("[sem  ] %s 缺 s1_semantic_%s 台账。" % (
                    "★★ 闸 SEM 阻断：" if _sem_mode == "enforce" else "[warn] 闸 SEM 告警：", a.dataset),
                    file=sys.stderr)
                print("[sem  ]    修复：python tools/field_semantic_classify.py --region %s "
                      "--dataset %s --write-ledger" % (sem_report["region"], a.dataset), file=sys.stderr)
                if _sem_mode == "enforce":
                    print("[sem  ]    确需放行加 --skip-semantic-gate / --semantic-gate warn "
                          "（会打印醒目告警并在 gate_results 留痕）。", file=sys.stderr)
                    sys.exit(2)
        except SystemExit:
            raise
        except Exception as e:
            print(f"[sem  ] 闸 SEM 异常（不阻断）: {e}")
            sem_report = None

    # ---- 1) 语法校验（PLY 括号/字段 + 算子元数/命名参数）----
    syntax = run_syntax_gate(items)

    # ---- 2) 5 闸 + 多样性（权威实现：toolkit gate.py，从 DB 或 stdin 表达式）----
    try:
        gate_py = find_script(_TOOLKIT_CANDIDATES, "gate.py")
    except FileNotFoundError as e:
        env_error_exit(str(e))
    cmd = [sys.executable, gate_py, "--campaign-dir", campaign, "--dataset", a.dataset,
           "--wave", str(tag), "--batch-type", a.batch_type]
    if a.datasets:
        cmd.extend(["--datasets", a.datasets])
    seeded = None  # 本脚本代为入库的候选（仅这些由本脚本回写逐条状态）
    if a.from_db or (not a.candidates and not a.exprs_file and not a.expr):
        cmd.append("--from-db")
    else:
        # 兼容旧入口：把解析后的表达式 upsert 再 --from-db，避免写 cache json
        CampaignStore = _compat.campaign_store_cls(campaign)
        settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
        region = a.region or settings.get("region")
        st = CampaignStore(_compat.wqb_db_path(campaign))
        try:
            # 2026-09-27 R7：先入 pending，门禁逐条结论出来后再回写 gated / fail（见 _write_back_gate_status）
            st.upsert_expressions(region, str(tag), [e for _, e in items], dataset=a.dataset, status="pending")
        finally:
            st.close()
        seeded = (region, [e for _, e in items])
        cmd.append("--from-db")
    if a.skip_diversity_gate:
        cmd.append("--skip-diversity-gate")
    if a.no_cache:
        cmd.append("--no-cache")
    if a.fix:
        cmd.append("--fix")
    print(f"\n[gate ] {os.path.basename(gate_py)} --from-db --wave {tag}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    gate_json = parse_gate_payload(r.stdout)
    # 三分终态：无结论 = ERROR（环境/实现坏了），有结论才谈 PASS/FAIL（表达式合不合格）。
    if gate_json is None:
        gate_error_exit(  # 不返回：内部 sys.exit(2)
            cmd, r, f"gate.py 退出码 {r.returncode}，stdout 未给出结论 JSON")
    if r.stderr and r.stderr.strip():  # gate.py 未崩但有告警（如入库异常）—— 同样不静默丢弃
        print("[gate ] WARN: gate.py 有 stderr 输出（不阻断）")
        from .payload import _GATE_ERR_TAIL, _echo_block
        _echo_block(r.stderr, "[gate ] stderr|", _GATE_ERR_TAIL)
    gate_pass = bool(gate_json["all_pass"])
    if gate_pass != (r.returncode == 0):  # gate.py 契约：exit 0 <=> all_pass=True
        print(f"[gate ] WARN: gate.py 退出码 {r.returncode} 与 all_pass={gate_pass} 不一致，以 all_pass 为准")
    if not gate_pass:
        reasons = gate_fail_reasons(gate_json)
        print("[gate ] FAIL: 闸门不过（gate.py 正常返回 all_pass=false）"
              + ("；" + "、".join(reasons) if reasons else ""))

    state_writeback = None
    if seeded:
        state_writeback = _write_back_gate_status(campaign, seeded[0], tag, gate_json, seeded[1])

    report = {
        "wave": a.wave, "dataset": a.dataset, "campaign_dir": campaign,
        "gate_exit": r.returncode,
        "syntax": {"total": len(syntax), "passed": sum(1 for s in syntax if s["valid"]),
                   "items": syntax},
        "gate": gate_json,
    }
    if state_writeback is not None:
        report["state_writeback"] = state_writeback
    if _wv_decisions:
        report["waivers"] = [d.to_dict() for d in _wv_decisions]
    if s2_field_report:
        report["s2_field_validation"] = s2_field_report
    # 闸 SEM 落痕（2026-10-01 P0）：此前 sem_report 只用于打印 + 剔式，
    # **从未写进 report** → gate_results 里看不到「剔了哪些式 / 是否因缺台账 exit 2」，
    # get_gate_result 回读拿不到证据，下游以为本步没跑 SEM（实测 846 条非 mcp 记录 0 条含 semantic）。
    # 这里落**脱敏摘要**（removed 全量会撑爆 report_json；只留计数 + 前 10 条样本）。
    if sem_report is not None:
        _sem_removed = sem_report.get("removed") or []
        report["semantic"] = {
            "mode": _sem_mode,
            "region": sem_report.get("region"),
            "dataset": sem_report.get("dataset"),
            "ledger_missing": bool(sem_report.get("ledger_missing")),
            "blocked_field_count": sem_report.get("blocked_field_count", 0),
            "n_removed": len(_sem_removed),
            "n_kept": len(sem_report.get("items") or []),
            "dropped_in_db": sem_report.get("dropped_in_db", 0),
            "removed_sample": [
                {"id": cid, "fields": hit} for cid, _e, hit in _sem_removed[:10]
            ],
        }
    elif _sem_mode == "off":
        report["semantic"] = {"mode": "off", "skipped": True}

    # ---- 2.5) 体检→表达式硬门（2026-09-06 接线；2026-09-17 补 fail-closed 档）----
    inspect_patch, inspect_report, inspect_unavailable, _inspect_mode = run_inspect_gate(
        a, campaign, items, syntax, _inspect_mode)
    report.update(inspect_patch)

    # ---- 2.6) PROD 饱和闸（2026-09-07 P1-1 前移接线）----
    report.update(run_prod_saturation_gate(a, campaign, items))

    # ---- 2.7) 闸 PF：信号族死路预检（2026-09-25 P2 落地）----
    # 2026-10-01 P1：unknown_mode（CLI --pf-unknown-mode > WQB_PF_UNKNOWN_MODE > 缺省 warn）。
    #   warn（默认）= 新骨架只 WARN，保持历史行为；
    #   enforce = 新骨架也拦截（饱和区「先探针后扩批」可强制）。
    _pf_unknown_mode = (a.pf_unknown_mode or os.environ.get("WQB_PF_UNKNOWN_MODE") or "warn").strip().lower()
    if _pf_unknown_mode not in ("warn", "enforce"):
        _pf_unknown_mode = "warn"
    pf_report = None
    try:
        _region = a.region or _compat.settings_region(campaign) or ""
        if _region:
            pf_report = check_prod_family_gate(
                [e for _, e in items], region=_region, dataset=a.dataset,
                unknown_mode=_pf_unknown_mode,
            )
            print("\n" + format_prod_family_report(pf_report))
            report["prod_family"] = pf_report
    except Exception as e:
        print(f"[prod-family] 闸 PF 执行异常（不阻断）: {e}")
        report["prod_family"] = {"status": "error", "error": str(e)}

    # ---- 3) 六维多样性 + 算子类别覆盖 + 质量预估 ----
    quality_block_ids = run_quality_stage(a, campaign, items, syntax, report)

    # ---- 3.5) 参数变体聚类 ----
    run_variant_clustering(a, items, syntax, report)

    def _persist_gate_report(final_all_pass=None):
        """落 gate_results。final_all_pass 非 None 时写 final verdict。

        2026-09-28 修：`store.upsert_gate_result` 取的是 `report.get("all_pass")`，
        而本函数内 all_pass 是在**这次写库之后**才算出来的 → DB 列恒为 0，
        与 report_json 里的真实判定打架。停止规则 C（`gate_results.all_pass 全 0`
        → 判区域信号族死）会因此误杀。故末尾用真实 verdict 再 upsert 一次覆盖。
        """
        try:
            _store = _compat.campaign_store_cls(campaign)
            _settings = json.load(open(os.path.join(campaign, "config", "settings.json"), encoding="utf-8"))
            _region = a.region or _settings.get("region")
            if final_all_pass is not None:
                report["all_pass"] = bool(final_all_pass)
            _st = _store(_compat.wqb_db_path(campaign))
            try:
                _st.upsert_gate_result(_region, str(tag), a.dataset, report)
            finally:
                _st.close()
            print(f"\n[out  ] db gate_results/{_region}/{tag}/{a.dataset}"
                  + (f" all_pass={report['all_pass']}" if final_all_pass is not None else ""))
        except Exception as e:
            print(f"[out  ] gate 入库失败: {e}")

    _persist_gate_report()

    # ---- 4) 探针批规划（可选，**只做结构预判，不跑回测**）----
    # 2026-10-01 P2：本分支在 gate 阶段只调用 dry_run=True 的 select_probe_candidates，
    # 从不真回测，saved_quota 恒 0。原 status 写 "PROBE_ASSIGNED" 会被误读为「探针已派发/
    # 已节省配额」——实际真实探针回测在步 5b（prod-first）与 probe_batch_mode.py。
    # 改名为 PROBE_PLANNED（= 仅规划），并把 decision_reason 写明不执行回测。
    probe_report = None
    if a.probe_mode and len(items) > 2:
        try:
            from probe_batch_mode import ProbeBatchExecutor
            # gate 阶段只做探针分配标记（结构预判），不做真实回测
            executor = ProbeBatchExecutor(
                campaign, a.dataset, 0,  # wave=0 占位，gate 阶段不需要
                datasets_extra=a.datasets or "",
                dry_run=True)
            candidates_for_probe = [{"id": cid, "expression": e} for cid, e in items]
            # 只做探针分配，不执行回测
            probe_candidates = executor.select_probe_candidates(candidates_for_probe, n=2)
            probe_report = {
                "status": "PROBE_PLANNED",
                "probe_ids": [c.get("id") for c in probe_candidates],
                "probe_count": len(probe_candidates),
                "total_count": len(candidates_for_probe),
                "decision_reason": "gate 阶段仅规划探针（dry_run，不回测）；真回测走步 5b prod-first / probe_batch_mode.py",
                "saved_quota": 0,
                "executed": False,
            }
            print(f"[probe] 探针批规划: {probe_report['status']}（gate 阶段不回测，实际探针见步 5b）")
            print(f"[probe] 决策原因: {probe_report['decision_reason']}")
        except Exception as e:
            print(f"[probe] 探针批规划失败（不阻断）: {e}")

    all_pass = all(s["valid"] for s in syntax) and gate_pass
    if a.quality_block and quality_block_ids:
        all_pass = False
    if gem_report and not gem_report["pass"]:
        all_pass = False
    if s2_field_report and not s2_field_report["pass"] and a.s2_field_block:
        all_pass = False
    # 探针批判死数据集 → 整波拦截。
    # 2026-10-01 P2：本分支不再由 gate 阶段产生（gate 只规划 PROBE_PLANNED，status 恒非
    # PROBE_DEAD），但**保留**该判定：它是 probe_batch_mode.py 真回测后的合法终态，
    # 若未来 gate 内联探针结论（或外部注入 probe_report）仍需据此拦波。此处不再是死代码陷阱
    # ——它明确是"外部注入"的接口，注释说明来源。
    if probe_report and probe_report.get("status") == "PROBE_DEAD":
        all_pass = False
        print(f"[done ] 探针批判死数据集，整波拦截")
    # 体检硬门违规硬阻断（有体检数据才可能出现 violations；无数据不阻断）
    if inspect_report and inspect_report.get("violations"):
        all_pass = False
        print(f"[done ] 体检硬门拦截 {len(inspect_report['violations'])} 条违规候选")
    # 体检包缺失 + enforce → fail-closed 整波拦截（2026-09-17 P1-1）
    if inspect_unavailable and _inspect_mode == "enforce":
        all_pass = False
        print("[done ] 体检硬门 fail-closed 拦截：缺体检包（inspect-mode=enforce）")
    # PROD 饱和闸硬阻断（enforced 态才可能 FAIL；unavailable 不阻断）
    prod_sat_report = report.get("prod_saturation")
    if prod_sat_report and prod_sat_report.get("status") == "enforced" and not prod_sat_report.get("passed", True):
        all_pass = False
        n_v = len(prod_sat_report.get("violations") or [])
        print(f"[done ] PROD 饱和闸拦截：{n_v} 条命中饱和字段"
              + ("；当前数据集整判饱和" if prod_sat_report.get("current_dataset_saturated") else ""))
    # 闸 PF 硬阻断：命中已死路信号族 → 整波拦截
    # 2026-10-01 P1：status=enforced 的两种来源——已死路骨架 / unknown_mode=enforce 下未探明骨架；
    # 分别打印原因，避免把「新骨架需先探针」误读成「已实测死路」。
    if pf_report and pf_report.get("status") == "enforced" and pf_report.get("violations"):
        all_pass = False
        n_v = len(pf_report.get("violations") or [])
        if pf_report.get("unknown_mode") == "enforce" and not pf_report.get("n_dead_families"):
            print(f"[done ] 闸 PF 拦截：{n_v} 条骨架指纹未探明（unknown_mode=enforce，须先 prod-first 探针）")
        else:
            print(f"[done ] 闸 PF 拦截：{n_v} 条命中已死路信号族（prod_corr ≥0.7 已实测死路）")
    g = gate_json  # ERROR 已在调用处退出，此处 all_pass 必为 bool（不再有 None 终态）
    qp = report.get("quality_predict") or {}
    qp_note = ""
    if isinstance(qp, dict) and "error" not in qp and qp:
        qp_note = (f" 质量预估 D/C/W/B/H={qp.get('direct_submit')}/{qp.get('combo_candidate')}/"
                   f"{qp.get('weak_signal')}/{qp.get('expected_block')}/{qp.get('hard_reject')}"
                   + (f"（拦截 {len(quality_block_ids)} 条{'计入 FAIL' if a.quality_block else ' 仅标注'}）"
                      if (qp.get('expected_block') or qp.get('hard_reject')) else ""))
    gem_note = f" GEM={gem_report['gem_ratio']:.0%}" if gem_report else ""
    s2fld_note = ""
    if s2_field_report:
        cov = s2_field_report.get("coverage", 0)
        s2fld_note = f" S1字段={cov:.0%}" + ("(BLOCK)" if not s2_field_report["pass"] and a.s2_field_block else "")
    probe_note = f" Probe={probe_report['status']}" if probe_report else ""
    print(f"[done ] 语法 {report['syntax']['passed']}/{report['syntax']['total']}, "
          f"gate all_pass={str(g['all_pass']).lower()} passed={g.get('passed')}/{g.get('total')}"
          f"{qp_note}{gem_note}{s2fld_note}{probe_note} => {'PASS' if all_pass else 'FAIL'}")
    # 用**最终 verdict** 覆盖写一次（首次落库时 all_pass 尚未算出，见 _persist_gate_report 注释）
    _persist_gate_report(final_all_pass=all_pass)
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":  # pragma: no cover - 走 tools/wave_gate.py shim 进入
    main()
