# -*- coding: utf-8 -*-
"""pipeline/core/mcp_integrated_pipeline.py - MCP 集成的完整 Pipeline

集成 MCP create_multi_simulation 提交和轮询，实现真正的端到端自动化。
"""
import json
import os
import sys
import time
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from .campaign_pipeline import CampaignPipeline, RegionConfig, Checkpoint

# 尝试导入 MCP SSE 客户端
try:
    from tools.mcp_5slot_batch import McpClient, normalize_settings
    MCP_AVAILABLE = True
    print("[INFO] 使用 MCP SSE 模式调用 create_multi_simulation")
except ImportError as e:
    print(f"[WARN] 无法导入 MCP SSE 客户端: {e}")
    MCP_AVAILABLE = False


class MCPIntegratedPipeline(CampaignPipeline):
    """MCP 集成的完整 Pipeline"""
    
    def __init__(self, config: RegionConfig):
        super().__init__(config)
        self.mcp_available = MCP_AVAILABLE
    
    def stage_submit(self, passed: List[Dict]) -> str:
        """提交阶段 - 使用 MCP create_multi_simulation"""
        print(f"[submit] 准备提交 {len(passed)} 个表达式")
        print(f"[submit] 配置: {self.config.region}/{self.config.universe}/D{self.config.delay}")
        print(f"[submit] 中性化: {self.config.neutralization}, decay={self.config.decay}")
        
        if not self.mcp_available:
            # 模拟提交
            mock_id = f"mock_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            print(f"[submit] 模拟提交成功: {mock_id}")
            print(f"[submit] 注意：实际提交需要 MCP 集成")
            return mock_id
        
        # 使用 MCP SSE 模式提交
        exprs = [p["expr"] for p in passed]
        
        try:
            client = McpClient()
            
            # 构建设置
            settings = {
                'instrumentType': 'EQUITY',
                'region': self.config.region,
                'universe': self.config.universe,
                'delay': self.config.delay,
                'decay': self.config.decay,
                'neutralization': self.config.neutralization,
                'truncation': self.config.truncation,
                'pasteurization': 'ON',
                'language': 'FASTEXPR',
                'visualization': False,
                'testPeriod': 'P0Y0M',
                'maxTrade': self.config.max_trade,
                'unitHandling': 'VERIFY',
                'nanHandling': 'OFF',
            }
            mcp_settings = normalize_settings(settings)
            mcp_settings['wait_for_completion'] = False
            mcp_settings['validate_fields'] = True
            
            # 构建 payload
            payload = dict(mcp_settings)
            payload['alpha_expressions'] = exprs
            
            result = client.call("create_multi_simulation", payload, timeout=120.0)
            
            print(f"[submit] 提交成功: {result.get('status', 'unknown')}")
            
            # 返回模拟 ID
            location = result.get('location') or result.get('multisimulation_id')
            if location:
                return location.split('/')[-1] if '/' in str(location) else str(location)
            return f"mcp_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            
        except Exception as e:
            print(f"[submit] 提交失败: {e}")
            # 回退到模拟模式
            mock_id = f"fallback_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            return mock_id
    
    def stage_poll(self, multisim_id: str, timeout: int = 3600) -> Dict:
        """轮询阶段 - 使用 MCP 轮询"""
        print(f"[poll] 轮询 {multisim_id}...")
        
        if not self.mcp_available:
            return {"status": "PENDING", "note": "需要 MCP 集成"}
        
        try:
            client = McpClient()
            
            # 1. 获取子模拟列表
            children_result = client.call("get_multisimulation_children", {
                "multisimulation_id": multisim_id
            }, timeout=60.0)
            
            children = children_result.get('children', [])
            if not children:
                return {"status": "PENDING", "note": "无子模拟"}
            
            # 2. 检查每个子模拟的状态
            results = []
            all_complete = True
            
            for child in children:
                child_id = child.get('id') or child.get('location', '').split('/')[-1]
                if not child_id:
                    continue
                    
                # 获取详细状态和错误信息
                detail = client.call("lookINTO_SimError_message", {
                    "simulation_id": child_id
                }, timeout=60.0)
                
                status = detail.get('status', 'UNKNOWN')
                results.append({
                    'id': child_id,
                    'status': status,
                    'detail': detail
                })
                
                if status not in ('COMPLETE', 'ERROR', 'WARNING'):
                    all_complete = False
            
            if all_complete:
                return {
                    "status": "COMPLETE",
                    "children": results,
                    "note": "所有子模拟已完成"
                }
            else:
                return {
                    "status": "PENDING",
                    "children": results,
                    "note": "部分子模拟仍在运行"
                }
                
        except Exception as e:
            print(f"[poll] 轮询失败: {e}")
            return {"status": "ERROR", "error": str(e)}


def create_pipeline(region: str, **kwargs) -> MCPIntegratedPipeline:
    """创建指定区域的 pipeline"""
    # 默认配置
    default_configs = {
        "GBR": {
            "universe": "TOP700",
            "delay": 1,
            "neutralization": "SUBINDUSTRY",
            "settings_path": "tracking/GBR/config/settings.json",
            "ledger_path": "tracking/GBR/gbr_d1_campaign_state.json"
        },
        "KOR": {
            "universe": "TOP600",
            "delay": 1,
            "neutralization": "SECTOR",
            "settings_path": "tracking/KOR/config/settings.json",
            "ledger_path": "tracking/KOR/kor_d1_campaign_state.json"
        },
        "USA": {
            "universe": "TOP3000",
            "delay": 1,
            "neutralization": "INDUSTRY",
            "settings_path": "tracking/USA/config/settings.json",
            "ledger_path": "tracking/USA/usa_d1_campaign_state.json"
        }
    }
    
    if region not in default_configs:
        raise ValueError(f"不支持的区域: {region}，支持: {list(default_configs.keys())}")
    
    # 合并默认配置和用户配置
    cfg_dict = default_configs[region]
    cfg_dict.update(kwargs)
    cfg_dict["region"] = region
    
    config = RegionConfig(**cfg_dict)
    return MCPIntegratedPipeline(config)


def main():
    """CLI 入口"""
    import argparse
    
    ap = argparse.ArgumentParser(description="MCP 集成的通用战役 Pipeline")
    ap.add_argument("--region", required=True, help="区域代码 (GBR/KOR/USA...)")
    ap.add_argument("--universe", help="Universe (覆盖默认)")
    ap.add_argument("--delay", type=int, help="Delay (覆盖默认)")
    ap.add_argument("--neutralization", help="中性化 (覆盖默认)")
    
    sub = ap.add_subparsers(dest="cmd")
    
    # run 命令
    p = sub.add_parser("run")
    p.add_argument("--file", required=True, help="候选表达式文件")
    p.add_argument("--dataset", required=True, help="数据集名称")
    p.add_argument("--wave", required=True, help="波次标签")
    p.add_argument("--submit", action="store_true", help="提交回测")
    p.add_argument("--enhance-diversity", choices=["auto", "always", "never"],
                    default="auto", help="多样性增强模式")
    p.add_argument("--fresh", action="store_true", help="强制全新开始")
    p.add_argument("--dry-run", action="store_true", help="干跑模式")
    
    args = ap.parse_args()
    
    # 构建覆盖配置
    overrides = {}
    if args.universe:
        overrides["universe"] = args.universe
    if args.delay is not None:
        overrides["delay"] = args.delay
    if args.neutralization:
        overrides["neutralization"] = args.neutralization
    
    pipeline = create_pipeline(args.region, **overrides)
    
    if args.cmd == "run":
        result = pipeline.run(
            exprs_file=args.file,
            dataset=args.dataset,
            wave=args.wave,
            submit=args.submit,
            enhance_diversity=args.enhance_diversity,
            fresh=args.fresh,
            dry_run=args.dry_run
        )
        print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
