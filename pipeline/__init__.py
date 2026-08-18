# -*- coding: utf-8 -*-
"""pipeline/__init__.py - 通用战役 Pipeline 包

提供区域无关的战役编排能力：
- CampaignPipeline: 核心 pipeline 类
- RegionConfig: 区域配置
- 自动多样性增强
- 断点续跑
- 台账集成

用法:
  from pipeline import CampaignPipeline, RegionConfig
  
  config = RegionConfig(
      region="GBR",
      universe="TOP700",
      delay=1,
      neutralization="SUBINDUSTRY",
      settings_path="tracking/GBR/config/settings.json",
      ledger_path="tracking/GBR/gbr_d1_campaign_state.json"
  )
  
  pipeline = CampaignPipeline(config)
  result = pipeline.run(...)
"""
from .core import CampaignPipeline, RegionConfig, Checkpoint, LedgerAdapter

__version__ = "1.0.0"
__all__ = ["CampaignPipeline", "RegionConfig", "Checkpoint", "LedgerAdapter"]
