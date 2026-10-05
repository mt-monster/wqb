# -*- coding: utf-8 -*-
"""六维多样性 + 算子类别覆盖 + 质量预估 + 参数变体聚类（--skip-quality 控制）。

从 2026-09-30 单文件 `tools/wave_gate.py` 拆出。本阶段**只标注、不阻断**
（除 --quality-block 显式开启时把 EXPECTED_BLOCK/HARD_REJECT 计入 FAIL）。
"""
import json
import os
import re
import sys

from ._paths import _settings_region, _wqb_db_path

#: 算子的六大类别（用于类别覆盖硬闸：Group/Vector 必须，Logical 仅事件型数据集必须）
OP_CATEGORIES = {
    "Logical": {"or", "and", "not", "is_nan", "less", "equal", "greater", "if_else", "not_equal", "less_equal", "greater_equal"},
    "Group": {"group_mean", "group_rank", "group_backfill", "group_scale", "group_count", "group_zscore", "group_std_dev", "group_sum", "group_neutralize", "group_cartesian_product"},
    "Vector": {"vec_min", "vec_count", "vec_sum", "vec_max", "vec_avg", "vec_stddev", "vec_range"},
    "Time Series": {"ts_corr", "ts_zscore", "ts_returns", "ts_product", "ts_std_dev", "ts_backfill", "days_from_last_change", "last_diff_value", "ts_scale", "ts_step", "ts_sum", "ts_av_diff", "ts_kurtosis", "ts_mean", "ts_arg_max", "ts_rank", "ts_ir", "ts_delay", "ts_quantile", "ts_count_nans", "ts_covariance", "ts_decay_linear", "ts_arg_min", "ts_regression", "ts_max_diff", "kth_element", "hump", "ts_delta"},
    "Cross Sectional": {"winsorize", "rank", "zscore", "scale", "normalize", "quantile"},
    "Arithmetic": {"add", "multiply", "sign", "subtract", "pasteurize", "log", "max", "abs", "divide", "min", "signed_power", "inverse", "sqrt", "reverse", "power", "densify"},
}


def _extract_all_operators(expr):
    """提取表达式中所有算子（函数名）。"""
    return set(re.findall(r"([a-z_]+)\(", expr))


def _tool_import(name):
    """从 tools/ 目录动态 import 一个模块（保持拆分前同口径）。"""
    tools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if tools_dir not in sys.path:
        sys.path.insert(0, tools_dir)
    return __import__(name)


def run_quality_stage(a, campaign, items, syntax, report):
    """执行六维多样性 + 算子类别覆盖 + 质量预估。

    就地写 report 的 diversity / operator_category_coverage /
    operator_category_gate / quality_predict 键。
    返回 quality_block_ids（被建议拦截的候选 id 列表）。
    """
    quality_block_ids = []
    if getattr(a, "batch_type", "explore") in ("repair", "probe") and not a.skip_quality:
        print(f"[qp   ] batch_type={a.batch_type}：跳过质量预估标注（修复/探针批以实测为准）")
        a.skip_quality = True
    if a.skip_quality:
        return quality_block_ids
    try:
        pd_mod = _tool_import("pool_diversity")
        qp_mod = _tool_import("quality_predict")
        import sqlite3 as _sq
        passed_exprs = [e for (cid, e), s in zip(items, syntax) if s["valid"]]
        # 2026-09-13：pool_diversity 已重写为多维标签体系（skeleton_tags），旧 assess
        # 接口被移除 —— 此处降级跳过六维展示（不阻断门禁），保留新版可用的兼容路径。
        _assess = getattr(pd_mod, "assess", None) or getattr(pd_mod, "assess_multidimensional", None)
        if _assess is None:
            print("\n[div  ] pool_diversity.assess 不存在（新版已重写），六维报告跳过")
            report["diversity"] = {"skipped": True, "reason": "assess removed in pooled rewrite"}
        else:
            div_report = _assess(passed_exprs, region=a.region)
            report["diversity"] = div_report
            if div_report.get("issues"):
                print("\n[div  ] 六维多样性风险:")
                for it in div_report["issues"]:
                    print(f"        - {it}")
            elif div_report.get("operator_stats"):
                print(f"\n[div  ] 六维多样性 PASS（算子熵={div_report['operator_stats']['entropy']}, "
                      f"同质占比={div_report['structural_similarity']['homog_ratio']:.0%}）")
            else:
                print("\n[div  ] 新版多样性报告（格式已更新）")

        # 2026-09-04 新增：算子类别覆盖检查（Logical/Group/Vector 至少 1 个）
        all_ops = set()
        for e in passed_exprs:
            all_ops.update(_extract_all_operators(e))

        category_coverage = {}
        for cat, ops in OP_CATEGORIES.items():
            covered = ops & all_ops
            category_coverage[cat] = {"covered": len(covered), "total": len(ops), "ops": sorted(covered)}

        report["operator_category_coverage"] = category_coverage

        # 硬闸：Logical/Group/Vector 至少 1 个
        logical_ok = category_coverage["Logical"]["covered"] >= 1
        group_ok = category_coverage["Group"]["covered"] >= 1
        vector_ok = category_coverage["Vector"]["covered"] >= 1

        # 2026-09-04 优化：MATRIX 数据集豁免 Vector 类别（无 VECTOR 字段可用）
        dataset_data_type = None
        try:
            conn_tmp = _sq.connect(_wqb_db_path(campaign))
            # 2026-10-05 修：原写法 `WHERE name=? LIMIT 1` **无区过滤且无 ORDER**，
            # 同名 dataset 跨区多行（实测 risk70 7 行 / pv1 11 行）⇒ 取到哪个区不确定，
            # data_type 可能来自别区（MATRIX/VECTOR 判定错 ⇒ 误豁免或误杀 Vector 类别闸）。
            _qregion = (a.region or _settings_region(campaign) or "").upper()
            row_tmp = conn_tmp.execute(
                "SELECT d.data_type FROM datasets d JOIN regions g ON g.id = d.region_id "
                "WHERE d.name=? AND g.name=? LIMIT 1",
                (a.dataset, _qregion)
            ).fetchone()
            conn_tmp.close()
            if row_tmp:
                dataset_data_type = row_tmp[0]
        except Exception:
            pass

        vector_required = dataset_data_type != "MATRIX"  # MATRIX 数据集豁免 Vector
        vector_ok = category_coverage["Vector"]["covered"] >= 1 if vector_required else True

        # 2026-09-08：Logical 由硬闸降为条件闸。
        # 依据 859 条过闸样本——if_else 出现率仅 5.1%，trade_when/bucket 未进前 22；
        # 而 group_rank 32.0% / vec_avg 12.6%。强制 Logical 等于强制一槽落在低过闸率区。
        # 只有事件型数据集（有明确事件时点）才把 Logical 缺失判 FAIL，其余出 WARNING。
        logical_required = False
        try:
            from operator_coverage import is_event_type_dataset  # toolkit _lib
            _field_names = None
            try:
                conn_f = _sq.connect(_wqb_db_path(campaign))
                _field_names = [r[0] for r in conn_f.execute(
                    "SELECT f.field_name FROM fields f JOIN datasets d ON d.id=f.dataset_id "
                    "WHERE d.name=?", (a.dataset,)).fetchall()]
                conn_f.close()
            except Exception:
                pass
            logical_required = bool(is_event_type_dataset(
                dataset_name=a.dataset, field_names=_field_names))
        except Exception:
            logical_required = False  # 判不准就不升闸（代价不对称：误升会压垮 sharpe）

        hard_missing = []
        if not group_ok:
            hard_missing.append("Group")
        if not vector_ok:
            hard_missing.append("Vector")
        if logical_required and not logical_ok:
            hard_missing.append("Logical")

        if hard_missing:
            report["operator_category_gate"] = {
                "pass": False,
                "missing": hard_missing,
                "logical_required": logical_required,
                "message": f"算子类别覆盖不足：缺 {', '.join(hard_missing)} 类别"
                            f"（Group/Vector 必须；Logical 仅事件型数据集必须）"
            }
            print(f"[opcat][INFO] 算子类别覆盖不足（提示性，不计入 FAIL）：缺 {', '.join(hard_missing)} 类别")
            print(f"        Logical: {category_coverage['Logical']['covered']}/{category_coverage['Logical']['total']}"
                  f"{'（事件型数据集，必须）' if logical_required else '（非事件型，不强制）'}, "
                  f"Group: {category_coverage['Group']['covered']}/{category_coverage['Group']['total']}, "
                  f"Vector: {category_coverage['Vector']['covered']}/{category_coverage['Vector']['total']}")
        else:
            warns = []
            if not logical_ok and not logical_required:
                warns.append("Logical")
            report["operator_category_gate"] = {"pass": True, "warnings": warns,
                                               "logical_required": logical_required}
            print(f"[opcat] 算子类别覆盖 PASS（Logical {category_coverage['Logical']['covered']}/11, "
                  f"Group {category_coverage['Group']['covered']}/10, Vector {category_coverage['Vector']['covered']}/7）")
            if warns:
                print(f"[opcat] WARNING：本波无 Logical 类算子。非事件型数据集不强制"
                      f"（if_else 在 859 条过闸样本中仅占 5.1%），仅提示。")

        # ---- 质量预估 ----
        qregion = a.region or _settings_region(campaign)
        qconn = _sq.connect(_wqb_db_path(campaign))
        try:
            q_results, _ = qp_mod.predict_all([(e, a.dataset) for e in passed_exprs], qregion, qconn)
        finally:
            qconn.close()
        by_expr = {qr["expr"]: qr for qr in q_results}  # expr 被截断 120 字符，全量表达式前缀匹配
        qp_summary = {"direct_submit": 0, "combo_candidate": 0, "weak_signal": 0,
                      "expected_block": 0, "hard_reject": 0, "blocked": []}
        for (cid, e), s in zip(items, syntax):
            if not s["valid"]:
                continue
            qr = by_expr.get(e[:120])
            if not qr:
                continue
            v = qr["verdict"]
            if v == "DIRECT_SUBMIT":
                qp_summary["direct_submit"] += 1
            elif v == "COMBO_CANDIDATE":
                qp_summary["combo_candidate"] += 1
            elif v == "WEAK_SIGNAL":
                qp_summary["weak_signal"] += 1
            elif v == "HARD_REJECT":
                qp_summary["hard_reject"] += 1
                quality_block_ids.append(cid)
                qp_summary["blocked"].append({"id": cid, "reasons": qr["reasons"], "verdict": v})
                print(f"[qp   ][INFO] ADVISORY_HARD {cid}: {'; '.join(qr['reasons'])}（建议性标注，不判 FAIL）")
            else:  # EXPECTED_BLOCK
                qp_summary["expected_block"] += 1
                quality_block_ids.append(cid)
                qp_summary["blocked"].append({"id": cid, "reasons": qr["reasons"], "verdict": v})
                print(f"[qp   ][INFO] ADVISORY {cid}: {'; '.join(qr['reasons'])}（建议性标注，不判 FAIL）")
        report["quality_predict"] = qp_summary
        print(f"[qp   ] 质量预估（INFO 建议层，2026-09-28 降级——实测把真实过闸者/ACTIVE 原式也判 BLOCK）: "
              f"DIRECT={qp_summary['direct_submit']} COMBO={qp_summary['combo_candidate']} "
              f"WEAK={qp_summary['weak_signal']} ADV_BLOCK={qp_summary['expected_block']} "
              f"ADV_HARD={qp_summary['hard_reject']}"
              + ("（--quality-block：计入 FAIL）" if a.quality_block else "（仅标注）"))
    except Exception as e:
        report["quality_predict"] = {"error": str(e)}
        print(f"[qp   ] 质量预估阶段失败（不阻断门禁）: {e}")
    return quality_block_ids


def run_variant_clustering(a, items, syntax, report):
    """参数变体聚类（2026-09-02 优化点⑤：同骨架同字段仅差参数的归一簇）。

    背景：wave 146 三条全闸通过候选互相关 0.9933-0.9985（max_mutually_below_subset=1），
    Mode A 参数变体不构成多颗额度。此闸在回测前识别变体簇，每簇只留 1 条。
    就地写 report 的 variant_clusters 键。
    """
    if a.skip_quality:
        return
    variant_clusters = {}
    variant_warnings = []

    def _extract_skeleton(expr):
        """提取表达式骨架：去掉数字参数，只留结构。"""
        s = re.sub(r'\d+\.?\d*', 'N', expr)
        s = re.sub(r'\s+', '', s)
        return s

    def _extract_fields(expr):
        """提取表达式中的字段名（vec_avg/vec_sum 包裹的或裸字段）。"""
        fields = set()
        for m in re.finditer(r'vec_(?:avg|sum)\(([a-zA-Z_][\w]*)\)', expr):
            fields.add(m.group(1))
        _ops = {'rank','ts_delta','ts_mean','ts_zscore','ts_backfill','vec_avg','vec_sum',
                'divide','subtract','add','multiply','ts_decay_linear','group_neutralize',
                'ts_std_dev','abs','sign','log','max','min','if_else','ts_rank','scale',
                'group_rank','ts_sum','ts_av_diff','ts_delay','ts_corr','ts_covariance',
                'group_zscore','ts_regression','last_diff_value','kth_element','ts_arg_max',
                'ts_arg_min','ts_max','ts_min','ts_product','inverse','signed_power','tail',
                'trade_when','is_nan','nan_out','purify','densify','winsorize','zscore',
                'ts_count_nans','ts_median','ts_percentile','ts_step','ts_scale','reverse',
                'bucket','industry','sector','subindustry','market','country'}
        for tok in re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{3,}\b', expr):
            if tok.lower() not in _ops and not tok.isdigit():
                fields.add(tok)
        return frozenset(fields)

    passed_items = [(cid, e) for (cid, e), s in zip(items, syntax) if s["valid"]]
    for cid, e in passed_items:
        skel = _extract_skeleton(e)
        fields = _extract_fields(e)
        key = (skel, fields)
        if key not in variant_clusters:
            variant_clusters[key] = []
        variant_clusters[key].append((cid, e))
    for key, cluster in variant_clusters.items():
        if len(cluster) > 1:
            ids = [cid for cid, _ in cluster]
            variant_warnings.append({
                "cluster_ids": ids,
                "count": len(cluster),
                "skeleton_preview": cluster[0][1][:80],
                "fields": sorted(key[1]),
            })
            print(f"[var  ] 参数变体簇 {ids}: {len(cluster)} 条同骨架同字段，建议只留 1 条")
    if variant_warnings:
        report["variant_clusters"] = variant_warnings
        print(f"[var  ] 共发现 {len(variant_warnings)} 个参数变体簇（回测前建议每簇只留 1 条）")
    else:
        print(f"[var  ] 参数变体聚类 PASS（无同骨架同字段变体）")
