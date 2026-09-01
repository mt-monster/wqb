# -*- coding: utf-8 -*-
"""s0_enhanced_screening.py - S0 数据集体检增强预筛（WebDataScope 零成本预筛）。

三层预筛机制：
  1. 平台硬门槛（cov/alphaCount/fields）
  2. WebDataScope 社区验证（isos.datafield sharpe/count）
  3. 字段级体检（分布形状/覆盖率/频率）

用法:
    python tools/s0_enhanced_screening.py --region IND --delay 1 \
        --datasets pv70,ai_news_scores,other567 --zip data/WebData.zip
    
    # 输出 JSON 供下游消费
    python tools/s0_enhanced_screening.py --region IND --delay 1 \
        --datasets pv70,ai_news_scores --json-out tracking/IND/cache/s0_screen.json
"""
import argparse
import json
import os
import sys
import zipfile
from typing import Dict, List, Any

# 添加 tools 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from webdata_quality import load_bin, field_inspect, classify_distribution, parse_yearly_distribution


class S0EnhancedScreener:
    """S0 增强预筛器"""
    
    def __init__(self, zip_path: str, region: str, delay: int = 1):
        self.zip_path = zip_path
        self.region = region
        self.delay = delay
        self.key = f"{region}_{delay}"
        self._load_data()
        
    def _load_data(self):
        """加载 WebDataScope 数据包"""
        with zipfile.ZipFile(self.zip_path) as zf:
            self.info = load_bin(zf, 'data/oth/info_data.bin')
            try:
                self.osis = load_bin(zf, 'data/oth/osis_data.bin')
            except KeyError:
                self.osis = None
            self.dsl = json.loads(zf.read('data/dataSetList.json'))
            
        if self.key not in self.info:
            raise ValueError(f"{self.key} 不在数据包中，可用: {sorted(self.info.keys())}")
            
        self.rd = self.info[self.key]
        self.isos = self.rd['isos']
        self.neut = self.rd['neutralization']
        self.mean_sharpe = self.isos['mean']['sharpe_ratio']
        
    def screen_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """
        三层预筛单个数据集
        
        Returns:
            {
                "dataset": str,
                "tier": "ATTACK" | "CAUTION" | "REJECT",
                "reason": str,
                "score": float,
                "layers": {
                    "platform_gate": {...},
                    "webdatascope": {...},
                    "field_health": {...}
                },
                "recommendation": str
            }
        """
        result = {
            "dataset": dataset_id,
            "tier": "REJECT",
            "reason": "",
            "score": 0.0,
            "layers": {},
            "recommendation": ""
        }
        
        # Layer 1: 平台硬门槛（从 isos 获取）
        platform_gate = self._check_platform_gate(dataset_id)
        result["layers"]["platform_gate"] = platform_gate
        if not platform_gate["pass"]:
            result["reason"] = f"platform_gate: {platform_gate['reason']}"
            result["recommendation"] = "跳过 - 不满足平台硬门槛"
            return result
            
        # Layer 2: WebDataScope 社区验证
        wds_score = self._check_webdatascope(dataset_id)
        result["layers"]["webdatascope"] = wds_score
        if not wds_score["pass"]:
            result["reason"] = f"webdatascope: {wds_score['reason']}"
            result["recommendation"] = "跳过 - 社区验证失败"
            return result
            
        # Layer 3: 字段级体检
        field_health = self._check_field_health(dataset_id)
        result["layers"]["field_health"] = field_health
        
        # 综合评分
        score = self._compute_score(platform_gate, wds_score, field_health)
        result["score"] = score
        
        # 分层判定
        if score >= 0.7:
            result["tier"] = "ATTACK"
            result["recommendation"] = "优先攻击 - 高潜力数据集"
        elif score >= 0.4:
            result["tier"] = "CAUTION"
            result["reason"] = field_health.get("warning", "medium_score")
            result["recommendation"] = "谨慎尝试 - 需探针批验证"
        else:
            result["tier"] = "REJECT"
            result["reason"] = f"low_score: {score:.3f}"
            result["recommendation"] = "跳过 - 低潜力数据集"
            
        return result
        
    def _check_platform_gate(self, dataset_id: str) -> Dict[str, Any]:
        """Layer 1: 平台硬门槛"""
        ds_stats = self.isos['dataset'].get(dataset_id, {})
        count = ds_stats.get('count', 0)
        sharpe = ds_stats.get('sharpe_ratio', 0)
        
        # 硬门槛
        if count < 50:
            return {"pass": False, "reason": f"count={count}<50 未验证", "count": count, "sharpe": sharpe}
        if count > 30000:
            return {"pass": False, "reason": f"count={count}>30000 已饱和", "count": count, "sharpe": sharpe}
        if sharpe < self.mean_sharpe * 0.5:
            return {"pass": False, "reason": f"sharpe={sharpe:.3f}<{self.mean_sharpe*0.5:.3f} 低质量", 
                   "count": count, "sharpe": sharpe}
            
        return {"pass": True, "count": count, "sharpe": sharpe}
        
    def _check_webdatascope(self, dataset_id: str) -> Dict[str, Any]:
        """Layer 2: WebDataScope 社区验证"""
        # 检查甜点区字段数量
        sweet_fields = 0
        total_fields = 0
        
        for field, stats in self.isos['datafield'].items():
            if not field.startswith(f"{dataset_id}_"):
                continue
            total_fields += 1
            count = stats.get('count', 0)
            sharpe = stats.get('sharpe_ratio', 0)
            if 100 <= count <= 3000 and sharpe >= self.mean_sharpe * 1.1:
                sweet_fields += 1
                
        if total_fields == 0:
            return {"pass": False, "reason": "no_fields_in_webdatascope", 
                   "sweet_fields": 0, "total_fields": 0}
            
        sweet_ratio = sweet_fields / total_fields if total_fields > 0 else 0
        
        if sweet_fields == 0:
            return {"pass": False, "reason": "no_sweet_spot_fields", 
                   "sweet_fields": 0, "total_fields": total_fields, "sweet_ratio": 0}
            
        return {
            "pass": True,
            "sweet_fields": sweet_fields,
            "total_fields": total_fields,
            "sweet_ratio": sweet_ratio
        }
        
    def _check_field_health(self, dataset_id: str) -> Dict[str, Any]:
        """Layer 3: 字段级体检"""
        # 从 dataSetList 找到对应的数据集文件
        candidates = [n for n in self.dsl 
                     if n.startswith(f'{dataset_id}_{self.region}_') 
                     and f'_Delay{self.delay}' in n]
        
        if not candidates:
            return {"pass": False, "reason": "no_field_inspect_data", 
                   "spread_ratio": 0, "warning": "无字段体检数据"}
            
        fname = candidates[0]
        try:
            with zipfile.ZipFile(self.zip_path) as zf:
                ds_data = load_bin(zf, f'data/{fname}.bin')
        except KeyError:
            return {"pass": False, "reason": "field_bin_not_found",
                   "spread_ratio": 0, "warning": "字段体检文件缺失"}
            
        # 分析分布形状
        shapes = {"spread": 0, "zero_inflated": 0, "point_mass": 0, 
                 "ceiling": 0, "concentrated": 0, "unknown": 0}
        
        for field, fdata in ds_data.items():
            yd = fdata.get('yearly_distribution', '')
            shape = 'unknown'
            if isinstance(yd, str) and (yd.startswith('{') or yd.startswith('[')):
                dist = parse_yearly_distribution(yd)
                if dist:
                    shape, _ = classify_distribution(dist)
            shapes[shape] = shapes.get(shape, 0) + 1
            
        total = sum(shapes.values())
        spread_ratio = shapes.get("spread", 0) / total if total > 0 else 0
        
        # 判定
        warning = None
        if spread_ratio < 0.3:
            warning = f"spread_ratio={spread_ratio:.2f}<0.3 分布形状风险"
        elif shapes.get("zero_inflated", 0) + shapes.get("point_mass", 0) > total * 0.5:
            warning = "稀疏/点质量字段占比过高"
            
        return {
            "pass": spread_ratio >= 0.3,
            "spread_ratio": spread_ratio,
            "shapes": shapes,
            "warning": warning
        }
        
    def _compute_score(self, platform: Dict, wds: Dict, field: Dict) -> float:
        """计算综合得分 (0-1)"""
        score = 0.0
        
        # 平台层 (30%)
        if platform["pass"]:
            sharpe_score = min(platform["sharpe"] / (self.mean_sharpe * 2), 1.0)
            count_score = 1.0 - abs(platform["count"] - 1000) / 30000  # 1000 为最优
            score += 0.3 * (sharpe_score * 0.6 + count_score * 0.4)
            
        # WebDataScope 层 (40%)
        if wds["pass"]:
            score += 0.4 * wds.get("sweet_ratio", 0)
            
        # 字段健康层 (30%)
        if field["pass"]:
            score += 0.3 * field.get("spread_ratio", 0)
            
        return round(score, 3)
        
    def screen_batch(self, dataset_ids: List[str]) -> Dict[str, Any]:
        """批量预筛"""
        results = {
            "region": self.region,
            "delay": self.delay,
            "mean_sharpe": self.mean_sharpe,
            "datasets": {},
            "summary": {"ATTACK": [], "CAUTION": [], "REJECT": []}
        }
        
        for ds in dataset_ids:
            r = self.screen_dataset(ds)
            results["datasets"][ds] = r
            results["summary"][r["tier"]].append(ds)
            
        return results


def main():
    ap = argparse.ArgumentParser(description="S0 数据集体检增强预筛")
    ap.add_argument("--zip", required=True, help="WebDataScope 数据包路径")
    ap.add_argument("--region", required=True)
    ap.add_argument("--delay", type=int, default=1)
    ap.add_argument("--datasets", required=True, help="逗号分隔的数据集列表")
    ap.add_argument("--json-out", help="输出 JSON 路径")
    args = ap.parse_args()
    
    screener = S0EnhancedScreener(args.zip, args.region, args.delay)
    dataset_ids = [d.strip() for d in args.datasets.split(",")]
    
    results = screener.screen_batch(dataset_ids)
    
    # 打印摘要
    print(f"\n{'='*60}")
    print(f"S0 增强预筛结果 - {args.region}/D{args.delay}")
    print(f"{'='*60}")
    print(f"区域平均 Sharpe: {results['mean_sharpe']:.3f}")
    print(f"\n分层统计:")
    print(f"  ATTACK (优先攻击): {len(results['summary']['ATTACK'])}")
    print(f"  CAUTION (谨慎尝试): {len(results['summary']['CAUTION'])}")
    print(f"  REJECT (跳过): {len(results['summary']['REJECT'])}")
    
    print(f"\n详细结果:")
    for ds, r in results["datasets"].items():
        tier_icon = {"ATTACK": "🟢", "CAUTION": "🟡", "REJECT": "🔴"}[r["tier"]]
        print(f"  {tier_icon} {ds:30s} tier={r['tier']:8s} score={r['score']:.3f} {r['recommendation']}")
        if r["reason"]:
            print(f"      reason: {r['reason']}")
            
    # 输出 JSON
    if args.json_out:
        os.makedirs(os.path.dirname(args.json_out), exist_ok=True)
        with open(args.json_out, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nJSON 已写入: {args.json_out}")
        
    # 退出码：有 ATTACK 数据集返回 0，否则返回 1
    sys.exit(0 if results["summary"]["ATTACK"] else 1)


if __name__ == "__main__":
    main()
