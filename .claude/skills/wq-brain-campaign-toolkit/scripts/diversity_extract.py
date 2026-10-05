# -*- coding: utf-8 -*-
"""diversity_extract.py - 单数据集多样性榨取完整流程

功能：
1. 数据集深度审计（字段分类 + 算子树分桶 + 参数空间映射）
2. 分轮次多样性生成（L1 字段多样性 / L2 算子结构多样性 / L3 参数空间多样性）
3. PPAC 矩阵计算（基于回测结果）
4. 多样性榨取效果评估（结构多样性 + PPAC 关联）

用法:
  python diversity_extract.py --campaign-dir <DIR> --dataset <ds> [--rounds 3] [--size 8] [--max-ppac 0.7]

输出（仅 DB）:
  - diversity_potential / expressions / ledger_kv（matrix/evaluation）
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib.common import CampaignContext, add_campaign_arg, atomic_write
from _lib.diversity_extractor import (
    DiversityPotentialAuditor, DiversityRoundGenerator,
    PPACMatrixCalculator, DiversityExtractionEvaluator, RaPipelineIntegrator
)
from _lib.wqb_store import get_store, load_catalog


def ensure_campaign_dir_structure(campaign_dir, region, dataset):
    """确保静态配置存在（settings/thresholds 仍为文件）；catalog 从 DB 检查。"""
    dirs = ["config", "reference", "cache"]
    for d in dirs:
        os.makedirs(os.path.join(campaign_dir, d), exist_ok=True)

    settings_path = os.path.join(campaign_dir, "config", "settings.json")
    if not os.path.exists(settings_path):
        default_settings = {
            "region": region,
            "universe": "TOP3000",
            "delay": 1,
            "neutralization": "SUBINDUSTRY",
            "decay": 4,
            "truncation": 0.08,
            "maxTrade": 0.05,
            "pasteurization": "on",
            "_multi_sim_batch_size": 8,
            "_concurrency_rule": "seven_slot_filling"
        }
        atomic_write(settings_path, default_settings)
        print(f"[diversity_extract] 创建默认 settings.json: {settings_path}")

    thresholds_path = os.path.join(campaign_dir, "config", "thresholds.json")
    if not os.path.exists(thresholds_path):
        default_thresholds = {
            "review": {"sharpe_min": 1.58, "fitness_min": 1.0, "tvr_min": 0.05, "tvr_max": 0.20},
            "near": {"sharpe_min": 1.0},
            "quick_scan": {"sharpe_min": 1.0},
            "probe_scoring_v2": {"coverage_min": 0.85, "alphaCount_max": 50, "fieldCount_min": 10},
            "hard_gates": {"prod_corr_max": 0.7, "self_corr_max": 0.5, "low_2y_sharpe_min": 1.58},
            "dataset_health": {"coverage_min": 0.65, "usableFields_min": 5}
        }
        atomic_write(thresholds_path, default_thresholds)
        print(f"[diversity_extract] 创建默认 thresholds.json: {thresholds_path}")

    ctx = CampaignContext(campaign_dir)
    cat = load_catalog(ctx, dataset)
    if not cat:
        print(f"[diversity_extract] [INFO] typed catalog 不在 DB，自动 scan_fields: {dataset}")
        try:
            import subprocess
            scan_fields_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_fields.py")
            cmd = [sys.executable, scan_fields_path, "--campaign-dir", campaign_dir, "--dataset", dataset]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[diversity_extract] [ERROR] scan_fields.py 失败: {result.stderr}")
                return False
            if not load_catalog(ctx, dataset):
                print("[diversity_extract] [ERROR] catalog 仍未入库")
                return False
        except Exception as e:
            print(f"[diversity_extract] [ERROR] 自动生成 catalog 失败: {e}")
            return False
    return True


def main():
    ap = argparse.ArgumentParser(description="单数据集多样性榨取完整流程")
    add_campaign_arg(ap)
    ap.add_argument("--dataset", required=True, help="目标数据集")
    ap.add_argument("--rounds", type=int, default=3, help="榨取轮次（默认 3）")
    ap.add_argument("--size", type=int, default=8, help="每轮表达式数量（默认 8）")
    ap.add_argument("--max-ppac", type=float, default=0.7, help="PPAC 阈值（默认 0.7）")
    ap.add_argument("--skip-audit", action="store_true", help="跳过审计，直接使用已有报告")
    ap.add_argument("--skip-generation", action="store_true", help="跳过生成，直接使用已有表达式")
    ap.add_argument("--skip-ppac", action="store_true", help="跳过 PPAC 计算")
    ap.add_argument("--skip-evaluation", action="store_true", help="跳过效果评估")
    ap.add_argument("--integrate-pipeline", action="store_true", help="集成到 wq-brain-ra-pipeline 编排器")
    a = ap.parse_args()

    region = os.path.basename(os.path.abspath(a.campaign_dir)).upper()
    if not ensure_campaign_dir_structure(a.campaign_dir, region, a.dataset):
        print("[diversity_extract] 战役目录结构不完整，流程终止")
        return

    ctx = CampaignContext(a.campaign_dir)
    print(f"[diversity_extract] 开始单数据集多样性榨取: {a.dataset}")
    print(f"[diversity_extract] 轮次: {a.rounds}, 每轮数量: {a.size}, PPAC 阈值: {a.max_ppac}")

    st = get_store(ctx)
    try:
        audit_report = None
        if not a.skip_audit:
            print("\n[diversity_extract] Step 1: 数据集深度审计")
            auditor = DiversityPotentialAuditor(ctx, a.dataset)
            audit_report = auditor.audit()
            st.upsert_diversity(region, a.dataset, audit_report)
            print(f"[diversity_extract] 审计报告 -> db diversity_potential/{region}/{a.dataset}")
            print(f"  字段数: {audit_report['field_count']}")
            print(f"  字段分组: {audit_report['field_groups']}")
            print(f"  多样性得分: {audit_report['diversity_score']}")
            print(f"  推荐轮次: {audit_report['recommended_rounds']}")
        else:
            audit_report = st.get_diversity(region, a.dataset)
            if not audit_report:
                print("[diversity_extract] 审计报告不在 DB，无法跳过审计")
                return
            print(f"[diversity_extract] 加载已有审计报告: db/{region}/{a.dataset}")

        wave_tags = []
        if not a.skip_generation:
            print("\n[diversity_extract] Step 2: 分轮次多样性生成")
            generator = DiversityRoundGenerator(ctx, a.dataset, audit_report)
            round_types = ["L1_field", "L2_operator", "L3_param"]
            for round_num in range(a.rounds):
                round_type = round_types[round_num % len(round_types)]
                wave_tag = f"D{round_num+1:02d}"
                print(f"\n  Round {round_num+1}: {round_type}")
                expressions = generator.generate_round(round_num, round_type, a.size)
                if not expressions:
                    print(f"  [WARN] Round {round_num+1} 未生成表达式")
                    continue
                st.upsert_expressions(
                    region, wave_tag, expressions, dataset=a.dataset, status="diversity")
                st.upsert_ledger(region, f"diversity_wave_meta_{wave_tag}", {
                    "wave": wave_tag, "round_type": round_type, "round_num": round_num + 1,
                    "dataset": a.dataset, "created_at": audit_report.get("audited_at"),
                })
                wave_tags.append(wave_tag)
                print(f"  生成 {len(expressions)} 个表达式 -> db expressions/{region}/{wave_tag}")
        else:
            print("\n[diversity_extract] Step 2: 加载已有表达式")
            for round_num in range(a.rounds):
                wave_tag = f"D{round_num+1:02d}"
                rows = st.list_expressions(region, wave_tag, dataset=a.dataset)
                if rows:
                    wave_tags.append(wave_tag)
                    print(f"  加载 wave {wave_tag} n={len(rows)}")

        if not wave_tags:
            print("[diversity_extract] 没有可用的表达式，流程终止")
            return

        ppac_matrix = None
        if not a.skip_ppac:
            print("\n[diversity_extract] Step 3: PPAC 矩阵计算")
            calculator = PPACMatrixCalculator(ctx)
            ppac_matrix = calculator.compute_matrix(wave_tags)
            st.upsert_ledger(region, f"diversity_matrix_{a.dataset}", ppac_matrix)
            print(f"[diversity_extract] PPAC 矩阵 -> db diversity_matrix_{a.dataset}")
            print(f"  Alpha 数量: {ppac_matrix['alpha_count']}")
            print(f"  平均 PPAC: {ppac_matrix['avg_ppac']}")
            print(f"  最大 PPAC: {ppac_matrix['max_ppac']}")
            print(f"  低 PPAC 比例: {ppac_matrix['low_ppac_ratio']}")
        else:
            ppac_matrix = st.get_ledger(region, f"diversity_matrix_{a.dataset}")
            if not isinstance(ppac_matrix, dict):
                print("[diversity_extract] PPAC 矩阵不存在，使用默认值")
                ppac_matrix = {"avg_ppac": 0.5, "max_ppac": 0.8, "low_ppac_ratio": 0.5}

        evaluation = None
        if not a.skip_evaluation:
            print("\n[diversity_extract] Step 4: 多样性榨取效果评估")
            evaluator = DiversityExtractionEvaluator(ctx, a.dataset)
            evaluation = evaluator.evaluate(wave_tags, ppac_matrix)
            st.upsert_ledger(region, f"diversity_evaluation_{a.dataset}", evaluation)
            print(f"[diversity_extract] 评估报告 -> db diversity_evaluation_{a.dataset}")
            print(f"  总表达式数: {evaluation['total_expressions']}")
            print(f"  结构多样性: {evaluation['structural_metrics']}")
            print(f"  PPAC 多样性: {evaluation['ppac_metrics']}")
            print(f"  评估结论: {evaluation['evaluation']['recommendation']}")
            print(f"  推荐理由: {evaluation['evaluation']['reason']}")

        if a.integrate_pipeline and evaluation:
            print("\n[diversity_extract] 集成到 wq-brain-ra-pipeline 编排器")
            integrator = RaPipelineIntegrator(ctx)
            integration_result = integrator.integrate_with_pipeline(a.dataset, a.rounds, a.size)
            st.upsert_ledger(region, f"pipeline_integration_{a.dataset}", integration_result)
            print(f"[diversity_extract] 集成结果 -> db pipeline_integration_{a.dataset}")
            print(f"  状态更新: {integration_result['state_update']}")
            print(f"  下一步行动: {integration_result['next_action']}")

        print("\n[diversity_extract] 单数据集多样性榨取完成")
    finally:
        st.close()


if __name__ == "__main__":
    main()
