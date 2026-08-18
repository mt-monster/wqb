# -*- coding: utf-8 -*-
"""pipeline/regions/gbr.py - GBR 区域适配器

提供 GBR 战役的便捷入口，封装区域特定配置。
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from pipeline.core import CampaignPipeline, RegionConfig


def get_gbr_config() -> RegionConfig:
    """获取 GBR 区域配置"""
    base_dir = PROJECT_ROOT / "tracking" / "GBR"
    return RegionConfig(
        region="GBR",
        universe="TOP700",
        delay=1,
        neutralization="SUBINDUSTRY",
        settings_path=str(base_dir / "config" / "settings.json"),
        ledger_path=str(base_dir / "gbr_d1_campaign_state.json"),
        decay=4,
        truncation=0.08,
        max_trade="ON",
        batch_size=8
    )


def run_gbr_pipeline(exprs_file: str, dataset: str, wave: str, **kwargs):
    """运行 GBR pipeline"""
    config = get_gbr_config()
    pipeline = CampaignPipeline(config)
    return pipeline.run(exprs_file, dataset, wave, **kwargs)


def main():
    """CLI 入口"""
    import argparse
    
    ap = argparse.ArgumentParser(description="GBR 战役 Pipeline")
    ap.add_argument("--file", required=True, help="候选表达式文件")
    ap.add_argument("--dataset", required=True, help="数据集名称")
    ap.add_argument("--wave", required=True, help="波次标签")
    ap.add_argument("--submit", action="store_true", help="提交回测")
    ap.add_argument("--enhance-diversity", choices=["auto", "always", "never"],
                    default="auto", help="多样性增强模式")
    ap.add_argument("--fresh", action="store_true", help="强制全新开始")
    ap.add_argument("--dry-run", action="store_true", help="干跑模式")
    
    args = ap.parse_args()
    
    result = run_gbr_pipeline(
        exprs_file=args.file,
        dataset=args.dataset,
        wave=args.wave,
        submit=args.submit,
        enhance_diversity=args.enhance_diversity,
        fresh=args.fresh,
        dry_run=args.dry_run
    )
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
