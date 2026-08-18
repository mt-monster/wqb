# -*- coding: utf-8 -*-
"""pipeline/core/campaign_pipeline.py - 通用战役 Pipeline（区域无关）

核心特性：
1. 区域无关：通过 RegionConfig 适配任意区域（GBR/KOR/USA/EUR...）
2. 自动多样性增强：gate 后自动分析 + 增强
3. 完整生命周期：gate → diversity → submit → poll → review → ledger
4. 断点续跑：checkpoint 机制
5. 台账集成：自动写入区域台账

用法:
  from pipeline.core.campaign_pipeline import CampaignPipeline, RegionConfig
  
  config = RegionConfig(
      region="GBR",
      universe="TOP700",
      delay=1,
      neutralization="SUBINDUSTRY",
      settings_path="tracking/GBR/config/settings.json",
      ledger_path="tracking/GBR/gbr_d1_campaign_state.json"
  )
  
  pipeline = CampaignPipeline(config)
  result = pipeline.run(
      exprs_file="tracking/GBR/candidates/gbr_batch8.txt",
      dataset="model106",
      wave="08",
      submit=True,
      enhance_diversity="auto"
  )
"""
import argparse
import datetime
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "docs" / "experience"))

# 导入多样性增强系统
try:
    from wqb.expression.diversity_enhancer import (
        DiversityEnhancer, DiversityMonitor, analyze_diversity, enhance_expressions
    )
    DIVERSITY_AVAILABLE = True
except ImportError:
    print("[WARN] 多样性增强系统不可用，将使用原始流程")
    DIVERSITY_AVAILABLE = False


@dataclass
class RegionConfig:
    """区域配置"""
    region: str
    universe: str
    delay: int
    neutralization: str
    settings_path: str
    ledger_path: str
    decay: int = 4
    truncation: float = 0.08
    max_trade: str = "ON"
    batch_size: int = 8
    submit_limit: int = 4
    submit_window_h: int = 48
    
    def __post_init__(self):
        """加载设置文件"""
        if os.path.exists(self.settings_path):
            with open(self.settings_path, encoding="utf-8") as f:
                settings = json.load(f)
                self.decay = settings.get("decay", self.decay)
                self.truncation = settings.get("truncation", self.truncation)
                self.max_trade = settings.get("maxTrade", self.max_trade)
                self.batch_size = settings.get("_multi_sim_batch_size", self.batch_size)


@dataclass
class Checkpoint:
    """检查点"""
    wave: str
    stages: Dict[str, Any] = field(default_factory=dict)
    batches: List[Dict] = field(default_factory=list)
    diversity: Dict[str, Any] = field(default_factory=dict)
    
    def save(self, path: str):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({
                "wave": self.wave,
                "stages": self.stages,
                "batches": self.batches,
                "diversity": self.diversity
            }, f, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
    
    @classmethod
    def load(cls, path: str, wave: str, fresh: bool = False):
        if fresh or not os.path.exists(path):
            return cls(wave=wave)
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
            return cls(
                wave=d.get("wave", wave),
                stages=d.get("stages", {}),
                batches=d.get("batches", []),
                diversity=d.get("diversity", {})
            )


class LedgerAdapter:
    """台账适配器 - 统一不同区域的台账接口"""
    
    def __init__(self, ledger_path: str):
        self.ledger_path = ledger_path
        self.bak_path = ledger_path + ".bak"
    
    def load(self) -> Dict:
        if not os.path.exists(self.ledger_path):
            return {
                "_schema": "campaign_state/v1",
                "waves": {},
                "dead_datasets": {},
                "submit_ready": [],
                "diversity_history": []
            }
        with open(self.ledger_path, encoding="utf-8-sig") as f:
            return json.load(f)
    
    def save(self, data: Dict):
        import shutil
        if os.path.exists(self.ledger_path):
            shutil.copy2(self.ledger_path, self.bak_path)
        tmp = self.ledger_path + ".tmp"
        with open(tmp, "w", encoding="utf-8-sig") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        os.replace(tmp, self.ledger_path)
    
    def update(self, mutator: Callable[[Dict], None]):
        """读-改-写，且写前在最新快照上重放 mutation"""
        d = self.load()
        mutator(d)
        fresh = self.load()
        mutator(fresh)
        self.save(fresh)
        return fresh
    
    def add_wave(self, wave_id: str, dataset: str, note: str = ""):
        def mut(d):
            d.setdefault("waves", {})[wave_id] = {
                "dataset": dataset,
                "note": note,
                "at": datetime.datetime.now().isoformat(timespec="seconds")
            }
        self.update(mut)
    
    def set_verdict(self, wave_id: str, verdict: Dict):
        def mut(d):
            d.setdefault("waves", {}).setdefault(wave_id, {})["verdict"] = verdict
        self.update(mut)
    
    def add_diversity_audit(self, audit_result: Dict):
        def mut(d):
            d["diversity_audit_latest"] = audit_result
            hist = d.setdefault("diversity_history", [])
            hist.append({
                "at": datetime.datetime.now().isoformat(timespec="seconds"),
                **audit_result
            })
        self.update(mut)
    
    def mark_submit_ready(self, alpha_id: str, note: str = ""):
        def mut(d):
            d.setdefault("submit_ready", []).append({
                "alpha_id": alpha_id,
                "note": note,
                "at": datetime.datetime.now().isoformat(timespec="seconds")
            })
        self.update(mut)


class CampaignPipeline:
    """通用战役 Pipeline"""
    
    def __init__(self, config: RegionConfig):
        self.config = config
        self.ledger = LedgerAdapter(config.ledger_path)
        self.checkpoint_dir = os.path.join(os.path.dirname(config.ledger_path), "results")
        os.makedirs(self.checkpoint_dir, exist_ok=True)
    
    def _get_checkpoint_path(self, wave: str) -> str:
        return os.path.join(self.checkpoint_dir, f"pipeline_{wave}_checkpoint.json")
    
    def stage_gate(self, exprs: List[str], dataset: str) -> List[Dict]:
        """Gate 阶段：字段白名单 + 算子签名检查"""
        print(f"[gate] 检查 {len(exprs)} 个表达式...")
        
        # TODO: 集成 expr_lint.py 或 gate.py
        # 目前简化版：直接通过
        passed = [{"expr": e, "dataset": dataset} for e in exprs]
        print(f"[gate] {len(passed)} 个表达式通过（简化版）")
        return passed
    
    def stage_diversity_enhance(self, ck: Checkpoint, passed: List[Dict], 
                                  enhance_mode: str = "auto") -> List[Dict]:
        """多样性增强阶段"""
        if not DIVERSITY_AVAILABLE:
            print("[diversity] 多样性系统不可用，跳过")
            return passed
        
        if ck.stages.get("diversity", {}).get("done"):
            print(f"[diversity] 已完成（checkpoint），跳过")
            return ck.stages["diversity"]["enhanced"]
        
        exprs = [p["expr"] for p in passed]
        print(f"[diversity] 分析 {len(exprs)} 个表达式的多样性...")
        
        # 分析多样性
        report = analyze_diversity(exprs)
        
        # 记录多样性指标
        diversity_metrics = {
            "analyzed_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "original_count": len(exprs),
            "metrics": report.get("current_metrics", {}),
            "recommendations": report.get("recommendations", [])
        }
        
        # 打印多样性报告
        if "current_metrics" in report:
            m = report["current_metrics"]
            print(f"[diversity] 算子熵={m['operator_entropy']:.3f} "
                  f"覆盖率={m['coverage_rate']:.2%} "
                  f"新颖度={m['novelty_score']:.2%} "
                  f"结构相似度={m['structural_similarity']:.2%}")
        
        # 判断是否需要增强
        need_enhance = False
        if enhance_mode == "always":
            need_enhance = True
        elif enhance_mode == "auto":
            if "current_metrics" in report:
                m = report["current_metrics"]
                if (m['operator_entropy'] < 2.0 or
                    m['coverage_rate'] < 0.5 or
                    m['novelty_score'] < 0.8 or
                    m['structural_similarity'] > 0.7):
                    need_enhance = True
        
        enhanced_exprs = exprs
        if need_enhance:
            print(f"[diversity] 多样性不足，执行增强...")
            enhanced_exprs, enhance_report = enhance_expressions(
                exprs, target_count=len(exprs)
            )
            
            diversity_metrics["enhanced"] = True
            diversity_metrics["enhanced_count"] = len(enhanced_exprs)
            diversity_metrics["enhance_report"] = enhance_report
            
            print(f"[diversity] 增强完成：{len(exprs)} -> {len(enhanced_exprs)}")
            
            if "current_metrics" in enhance_report:
                m = enhance_report["current_metrics"]
                print(f"[diversity] 增强后：算子熵={m['operator_entropy']:.3f} "
                      f"覆盖率={m['coverage_rate']:.2%} "
                      f"新颖度={m['novelty_score']:.2%}")
        else:
            print(f"[diversity] 多样性良好，无需增强")
            diversity_metrics["enhanced"] = False
        
        # 更新checkpoint
        enhanced_passed = [{"expr": e, "dataset": passed[0]["dataset"]} for e in enhanced_exprs]
        ck.stages["diversity"] = {
            "done": True,
            "enhanced": enhanced_passed,
            "metrics": diversity_metrics,
            "at": datetime.datetime.now().isoformat(timespec="seconds")
        }
        
        # 写入台账
        self.ledger.add_diversity_audit(diversity_metrics)
        
        # 如果有建议，打印出来
        if report.get("recommendations"):
            print("[diversity] 改进建议:")
            for rec in report["recommendations"]:
                print(f"  - {rec}")
        
        return enhanced_passed
    
    def stage_submit(self, passed: List[Dict]) -> str:
        """提交阶段 - 返回 multisimulation_id"""
        print(f"[submit] 准备提交 {len(passed)} 个表达式")
        print(f"[submit] 配置: {self.config.region}/{self.config.universe}/D{self.config.delay}")
        print(f"[submit] 中性化: {self.config.neutralization}, decay={self.config.decay}")
        
        # TODO: 集成 MCP create_multi_simulation
        # 目前返回模拟 ID
        mock_id = f"mock_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"[submit] 模拟提交成功: {mock_id}")
        print(f"[submit] 注意：实际提交需要 MCP 集成")
        return mock_id
    
    def stage_poll(self, multisim_id: str, timeout: int = 3600) -> Dict:
        """轮询阶段"""
        print(f"[poll] 轮询 {multisim_id}...")
        # TODO: 集成 MCP 轮询
        return {"status": "PENDING", "note": "需要 MCP 集成"}
    
    def stage_review(self, ck: Checkpoint, results: Dict):
        """评审阶段"""
        print(f"[review] 评审结果...")
        # TODO: 提取指标，判断是否过门槛
        pass
    
    def run(self, exprs_file: str, dataset: str, wave: str,
            submit: bool = False,
            enhance_diversity: str = "auto",
            fresh: bool = False,
            dry_run: bool = False) -> Dict:
        """运行完整 pipeline"""
        
        # 加载表达式
        exprs = []
        with open(exprs_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    exprs.append(line)
        print(f"[load] 加载 {len(exprs)} 个表达式从 {exprs_file}")
        
        # 加载 checkpoint
        ck = Checkpoint.load(self._get_checkpoint_path(wave), wave, fresh=fresh)
        
        # Gate 阶段
        passed = self.stage_gate(exprs, dataset)
        if not passed:
            print("[pipeline] 无表达式通过gate，终止")
            return {"status": "gate_failed"}
        
        # 多样性增强阶段
        if enhance_diversity != "never":
            passed = self.stage_diversity_enhance(ck, passed, enhance_mode=enhance_diversity)
        
        if dry_run:
            print(f"[dry-run] 将提交 {len(passed)} 个表达式")
            for i, p in enumerate(passed, 1):
                print(f"  {i}. {p['expr']}")
            return {"status": "dry_run", "count": len(passed)}
        
        # 提交阶段
        if submit:
            multisim_id = self.stage_submit(passed)
            ck.batches.append({
                "multisim_id": multisim_id,
                "count": len(passed),
                "submitted_at": datetime.datetime.now().isoformat(timespec="seconds")
            })
            
            # 保存 checkpoint
            ck.save(self._get_checkpoint_path(wave))
            
            # 记录到台账
            self.ledger.add_wave(wave, dataset, note=f"submitted {len(passed)} exprs")
            
            return {
                "status": "submitted",
                "multisim_id": multisim_id,
                "count": len(passed)
            }
        
        # 保存 checkpoint
        ck.save(self._get_checkpoint_path(wave))
        
        return {
            "status": "ready",
            "count": len(passed),
            "checkpoint": self._get_checkpoint_path(wave)
        }


def main():
    """CLI 入口"""
    ap = argparse.ArgumentParser(description="通用战役 Pipeline")
    ap.add_argument("--region", required=True, help="区域代码 (GBR/KOR/USA...)")
    ap.add_argument("--universe", required=True, help="Universe (TOP700/TOP600...)")
    ap.add_argument("--delay", type=int, default=1, help="Delay (0/1)")
    ap.add_argument("--neutralization", default="SUBINDUSTRY", help="中性化")
    ap.add_argument("--settings", help="设置文件路径")
    ap.add_argument("--ledger", help="台账文件路径")
    
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
    
    # diversity-report 命令
    sub.add_parser("diversity-report")
    
    args = ap.parse_args()
    
    # 构建配置
    config = RegionConfig(
        region=args.region,
        universe=args.universe,
        delay=args.delay,
        neutralization=args.neutralization,
        settings_path=args.settings or f"tracking/{args.region}/config/settings.json",
        ledger_path=args.ledger or f"tracking/{args.region}/{args.region.lower()}_d1_campaign_state.json"
    )
    
    pipeline = CampaignPipeline(config)
    
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
    
    elif args.cmd == "diversity-report":
        # TODO: 实现多样性报告
        print("[diversity-report] 待实现")


if __name__ == "__main__":
    main()
