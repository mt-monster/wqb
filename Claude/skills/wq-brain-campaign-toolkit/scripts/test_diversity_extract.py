# -*- coding: utf-8 -*-
"""test_diversity_extract.py - 测试单数据集多样性榨取流程

用法:
  python test_diversity_extract.py --campaign-dir <DIR> --dataset <ds>
"""
import argparse
import os
import subprocess
import sys

def ensure_campaign_dir_structure(campaign_dir, region, dataset):
    """确保战役目录结构完整，如果不存在则自动创建"""
    import os
    import json
    
    # 创建必要的目录
    dirs = [
        "config",
        "reference",
        "candidates",
        "reviews",
        "cache"
    ]
    for d in dirs:
        os.makedirs(os.path.join(campaign_dir, d), exist_ok=True)
    
    # 创建默认的 settings.json（如果不存在）
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
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=1)
        print(f"[TEST] 创建默认 settings.json: {settings_path}")
    
    # 创建默认的 thresholds.json（如果不存在）
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
        with open(thresholds_path, "w", encoding="utf-8") as f:
            json.dump(default_thresholds, f, ensure_ascii=False, indent=1)
        print(f"[TEST] 创建默认 thresholds.json: {thresholds_path}")
    
    # 创建默认的 generation_constraints.json（如果不存在）
    constraints_path = os.path.join(campaign_dir, "reference", f"{region.lower()}_generation_constraints.json")
    if not os.path.exists(constraints_path):
        default_constraints = {
            "operator_stats": {"used": [], "unused": [], "rare": []},
            "injection_rules": {
                "force_explore_ops": [],
                "cap_ops": [],
                "skeleton_quota": {"linear_mix": 0.5, "event_gated": 0.1, "group": 0.1, "ratio": 0.1, "single": 0.2}
            },
            "poison_patterns": []
        }
        with open(constraints_path, "w", encoding="utf-8") as f:
            json.dump(default_constraints, f, ensure_ascii=False, indent=1)
        print(f"[TEST] 创建默认 generation_constraints.json: {constraints_path}")
    
    # 检查 typed catalog，如果不存在则自动生成
    catalog_path = os.path.join(campaign_dir, "reference", f"{region.lower()}_{dataset}_fields.json")
    if not os.path.exists(catalog_path):
        print(f"[TEST] [INFO] typed catalog 不存在，自动生成: {catalog_path}")
        
        # 自动生成 typed catalog
        try:
            import subprocess
            scan_fields_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_fields.py")
            
            if not os.path.exists(scan_fields_path):
                print(f"[TEST] [ERROR] scan_fields.py 不存在: {scan_fields_path}")
                return False
            
            cmd = [
                sys.executable,
                scan_fields_path,
                "--campaign-dir", campaign_dir,
                "--dataset", dataset
            ]
            
            print(f"[TEST] [INFO] 执行命令: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[TEST] [ERROR] scan_fields.py 执行失败: {result.stderr}")
                return False
            
            print(f"[TEST] [INFO] scan_fields.py 执行成功: {result.stdout}")
            
            # 检查 catalog 是否生成成功
            if not os.path.exists(catalog_path):
                print(f"[TEST] [ERROR] typed catalog 生成失败: {catalog_path}")
                return False
            
            print(f"[TEST] [INFO] typed catalog 生成成功: {catalog_path}")
            
        except Exception as e:
            print(f"[TEST] [ERROR] 自动生成 typed catalog 失败: {e}")
            return False
    
    return True


def main():
    ap = argparse.ArgumentParser(description="测试单数据集多样性榨取流程")
    ap.add_argument("--campaign-dir", required=True, help="战役目录路径")
    ap.add_argument("--dataset", required=True, help="目标数据集")
    ap.add_argument("--rounds", type=int, default=3, help="榨取轮次（默认 3）")
    ap.add_argument("--size", type=int, default=8, help="每轮表达式数量（默认 8）")
    a = ap.parse_args()
    
    # 从战役目录名派生 region（如果 settings.json 不存在）
    region = os.path.basename(os.path.abspath(a.campaign_dir)).upper()
    
    # 确保战役目录结构完整
    if not ensure_campaign_dir_structure(a.campaign_dir, region, a.dataset):
        print(f"[TEST] 战役目录结构不完整，流程终止")
        return
    
    # 检查战役目录
    if not os.path.exists(a.campaign_dir):
        print(f"[ERROR] 战役目录不存在: {a.campaign_dir}")
        return
    
    # 检查必要的配置文件
    settings_path = os.path.join(a.campaign_dir, "config", "settings.json")
    if not os.path.exists(settings_path):
        print(f"[ERROR] 配置文件不存在: {settings_path}")
        return
    
    # 检查 typed catalog
    catalog_path = os.path.join(a.campaign_dir, "reference", f"{os.path.basename(a.campaign_dir).lower()}_{a.dataset}_fields.json")
    if not os.path.exists(catalog_path):
        print(f"[WARN] typed catalog 不存在: {catalog_path}")
        print(f"[INFO] 请先运行 scan_fields.py 生成 catalog")
        return
    
    # 执行 diversity_extract.py
    toolkit_scripts = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wq-brain-campaign-toolkit", "scripts")
    diversity_extract_path = os.path.join(toolkit_scripts, "diversity_extract.py")
    
    if not os.path.exists(diversity_extract_path):
        print(f"[ERROR] diversity_extract.py 不存在: {diversity_extract_path}")
        return
    
    cmd = [
        sys.executable,
        diversity_extract_path,
        "--campaign-dir", a.campaign_dir,
        "--dataset", a.dataset,
        "--rounds", str(a.rounds),
        "--size", str(a.size)
    ]
    
    print(f"[TEST] 执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(f"[TEST] 返回码: {result.returncode}")
    print(f"[TEST] 标准输出:\n{result.stdout}")
    if result.stderr:
        print(f"[TEST] 标准错误:\n{result.stderr}")
    
    # 检查输出文件
    region = os.path.basename(a.campaign_dir).lower()
    
    # 检查审计报告
    audit_path = os.path.join(a.campaign_dir, "reference", f"{region}_{a.dataset}_diversity_potential.json")
    if os.path.exists(audit_path):
        print(f"[TEST] ✓ 审计报告已生成: {audit_path}")
    else:
        print(f"[TEST] ✗ 审计报告未生成: {audit_path}")
    
    # 检查表达式文件
    for i in range(a.rounds):
        wave_tag = f"D{i+1:02d}"
        wave_path = os.path.join(a.campaign_dir, "candidates", f"{region}_wave{wave_tag}_exprs.json")
        if os.path.exists(wave_path):
            print(f"[TEST] ✓ 表达式文件已生成: {wave_path}")
        else:
            print(f"[TEST] ✗ 表达式文件未生成: {wave_path}")
    
    # 检查 PPAC 矩阵
    matrix_path = os.path.join(a.campaign_dir, "reviews", f"{region}_diversity_matrix.json")
    if os.path.exists(matrix_path):
        print(f"[TEST] ✓ PPAC 矩阵已生成: {matrix_path}")
    else:
        print(f"[TEST] ✗ PPAC 矩阵未生成: {matrix_path}")
    
    # 检查评估报告
    eval_path = os.path.join(a.campaign_dir, "reviews", f"{region}_diversity_evaluation.json")
    if os.path.exists(eval_path):
        print(f"[TEST] ✓ 评估报告已生成: {eval_path}")
    else:
        print(f"[TEST] ✗ 评估报告未生成: {eval_path}")
    
    print(f"[TEST] 测试完成")

if __name__ == "__main__":
    main()
