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

# 导入战役纪律系统
from .campaign_discipline import CampaignDiscipline, prod_category
from .discipline_monitor import DisciplineMonitor
from .improvement_comparator import ImprovementComparator
from .diversity_integrated_monitor import DiversityIntegratedMonitor


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
    """通用战役 Pipeline（集成纪律执行+监控+多样性评估）"""
    
    def __init__(self, config: RegionConfig):
        self.config = config
        self.ledger = LedgerAdapter(config.ledger_path)
        self.checkpoint_dir = os.path.join(os.path.dirname(config.ledger_path), "results")
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        
        # 初始化纪律系统
        self.discipline = CampaignDiscipline(config.ledger_path)
        monitor_dir = os.path.join(os.path.dirname(config.ledger_path), "monitoring")
        self.monitor = DisciplineMonitor(monitor_dir)
        self.comparator = ImprovementComparator(config.ledger_path, monitor_dir)
        self.integrated_monitor = DiversityIntegratedMonitor(
            region=config.region,
            ledger_path=config.ledger_path,
            monitor_dir=monitor_dir
        )
    
    def _get_checkpoint_path(self, wave: str) -> str:
        return os.path.join(self.checkpoint_dir, f"pipeline_{wave}_checkpoint.json")
    
    def stage_gate(self, exprs: List[str], dataset: str) -> List[Dict]:
        """Gate 阶段：字段白名单 + 算子签名检查 + 相关性预判 (2026-08-18 wave33 教训)"""
        print(f"[gate] 检查 {len(exprs)} 个表达式...")
        
        # TODO: 集成 expr_lint.py 或 gate.py
        # 目前简化版：直接通过
        passed = [{"expr": e, "dataset": dataset} for e in exprs]
        print(f"[gate] {len(passed)} 个表达式通过（简化版）")
        
        # 相关性预判前置 (2026-08-18 wave33 教训)
        # 若新候选与 ACTIVE 核心字段重叠 >50% → 标记高风险
        try:
            from tools.corr_precheck import precheck
            region = self.config.region
            results = precheck(exprs, region, threshold=0.5)
            high_risk = [r for r in results if r['risk_level'] == 'HIGH']
            if high_risk:
                print(f"[gate] [WARN] 相关性预判: {len(high_risk)} 条高风险候选")
                for r in high_risk:
                    print(f"[gate] [WARN]   #{r['index']} {r['expr'][:60]}...")
                    for hr in r['high_risk']:
                        print(f"[gate] [WARN]     撞车 {hr['alpha_id']}: 重叠度 {hr['overlap_ratio']:.1%}")
                print(f"[gate] [WARN] 建议: 先跑 compute_mutual_correlation 预判, 或换字段/结构")
                # 将高风险标记写入 passed
                for i, p in enumerate(passed):
                    if results[i]['risk_level'] == 'HIGH':
                        p['corr_risk'] = 'HIGH'
                        p['corr_overlap'] = results[i]['high_risk']
        except Exception as e:
            print(f"[gate] [WARN] 相关性预判失败: {e}")
        
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
        
        # 启动校验 (2026-08-18 EUR 复盘教训)
        # 1. 校验 runner universe 设置与 config 一致
        settings_path = self.config.settings_path
        if os.path.exists(settings_path):
            with open(settings_path, encoding="utf-8") as f:
                settings = json.load(f)
                actual_universe = settings.get("universe")
                if actual_universe != self.config.universe:
                    print(f"[submit] [ERROR] universe 不一致: config={self.config.universe} vs settings={actual_universe}")
                    print(f"[submit] [ERROR] 可能被并行会话篡改, 终止提交")
                    return {"status": "error", "reason": "universe_mismatch"}
        
        # 2. 平台对账硬门: 本地台账 submitted 数 vs 平台 OS 数必须一致
        # TODO: 集成 MCP get_user_alphas 拉取平台 OS 数
        # 目前简化版: 检查本地台账 submit_ready 数量
        ledger_data = self.ledger.load()
        local_submitted = len(ledger_data.get("submit_ready", []))
        print(f"[submit] 本地台账 submitted={local_submitted} (需平台对账)")
        
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
        """评审阶段 - 实现信号强度分层验证策略 (2026-08-18 wave35 教训)
        
        分层验证策略:
        - 第一层: 3 条核心信号探针（不同字段源）
        - 若第一层最好 sh < 1.0 → 停止，换数据集/区域
        - 若第一层最好 sh ≥ 1.0 → 第二层 5 条变体
        - 若第二层最好 sh ≥ 1.3 → 第三层复合/优化
        """
        print(f"[review] 评审结果...")
        
        if not results or 'candidates' not in results:
            print("[review] 无结果数据, 跳过")
            return {"status": "no_results"}
        
        candidates = results['candidates']
        if not candidates:
            print("[review] 候选列表为空, 跳过")
            return {"status": "empty_candidates"}
        
        # 提取指标
        metrics_list = []
        for c in candidates:
            alpha_id = c.get('alpha_id') or c.get('alpha')
            if not alpha_id:
                continue
            # 从结果中提取指标 (需要 MCP 集成, 这里用占位)
            metrics = c.get('metrics', {})
            metrics_list.append({
                'alpha_id': alpha_id,
                'expr': c.get('expr', ''),
                'sharpe': metrics.get('sharpe', 0),
                'fitness': metrics.get('fitness', 0),
                'two_year_sharpe': metrics.get('two_year_sharpe', 0),
                'turnover': metrics.get('turnover', 0),
                'margin': metrics.get('margin', 0),
                'long_count': metrics.get('longCount', 0),
                'short_count': metrics.get('shortCount', 0),
                'sub_universe_sharpe': metrics.get('sub_universe_sharpe', 0),
                'failed_checks': c.get('failed_checks', []),
            })
        
        if not metrics_list:
            print("[review] 无有效指标, 跳过")
            return {"status": "no_metrics"}
        
        # 按 sharpe 排序
        metrics_list.sort(key=lambda x: x['sharpe'], reverse=True)
        best = metrics_list[0]
        
        print(f"[review] 最佳候选: {best['alpha_id']} sh={best['sharpe']:.2f} fit={best['fitness']:.2f} 2y={best['two_year_sharpe']:.2f}")
        
        # 分层验证判断
        layer = ck.stages.get('review', {}).get('layer', 1)
        verdict = {
            'layer': layer,
            'best_sharpe': best['sharpe'],
            'best_alpha': best['alpha_id'],
            'total_candidates': len(metrics_list),
            'metrics_summary': metrics_list[:5],  # 前5名
            'at': datetime.datetime.now().isoformat(timespec="seconds")
        }
        
        # 第一层判断
        if layer == 1:
            if best['sharpe'] < 1.0:
                verdict['action'] = 'STOP'
                verdict['reason'] = f"第一层最好 sh={best['sharpe']:.2f} < 1.0, 信号强度不足, 换数据集/区域"
                print(f"[review] {verdict['reason']}")
            else:
                verdict['action'] = 'CONTINUE_LAYER2'
                verdict['reason'] = f"第一层最好 sh={best['sharpe']:.2f} >= 1.0, 进入第二层 5 条变体"
                print(f"[review] {verdict['reason']}")
        
        # 第二层判断
        elif layer == 2:
            if best['sharpe'] < 1.3:
                verdict['action'] = 'STOP'
                verdict['reason'] = f"第二层最好 sh={best['sharpe']:.2f} < 1.3, 信号强度不足, 换数据集/区域"
                print(f"[review] {verdict['reason']}")
            else:
                verdict['action'] = 'CONTINUE_LAYER3'
                verdict['reason'] = f"第二层最好 sh={best['sharpe']:.2f} >= 1.3, 进入第三层复合/优化"
                print(f"[review] {verdict['reason']}")
        
        # 第三层判断
        elif layer == 3:
            if best['sharpe'] < 1.58:
                verdict['action'] = 'STOP'
                verdict['reason'] = f"第三层最好 sh={best['sharpe']:.2f} < 1.58, 未达提交门槛, 换数据集/区域"
                print(f"[review] {verdict['reason']}")
            else:
                verdict['action'] = 'SUBMIT'
                verdict['reason'] = f"第三层最好 sh={best['sharpe']:.2f} >= 1.58, 达提交门槛"
                print(f"[review] {verdict['reason']}")
        
        # 记录到 checkpoint
        ck.stages['review'] = {
            'done': True,
            'layer': layer,
            'verdict': verdict,
            'at': datetime.datetime.now().isoformat(timespec="seconds")
        }
        
        # 写入台账
        self.ledger.set_verdict(ck.wave, verdict)
        
        return verdict
    
    def run(self, exprs_file: str, dataset: str, wave: str,
            submit: bool = False,
            enhance_diversity: str = "auto",
            fresh: bool = False,
            dry_run: bool = False,
            enable_discipline: bool = True,
            enable_monitoring: bool = True) -> Dict:
        """运行完整 pipeline（集成纪律执行+监控）"""
        
        # 0. 纪律评估（如果启用）
        if enable_discipline:
            print(f"\n[discipline] 评估数据集 {dataset} 状态...")
            evidence = self.discipline.assess_dataset(dataset)
            if evidence:
                print(f"[discipline] 分类: {evidence['category']}")
                print(f"[discipline] 建议: {evidence['recommendation']}")
                
                # 检查是否应该继续
                if evidence['category'] == 'DEAD' and evidence['death_score'] >= 3:
                    print(f"[discipline] 数据集 {dataset} 已判死，建议切换")
                    decision = self.discipline.decide_switch(dataset)
                    if decision and decision.get('switch_trigger'):
                        print(f"[discipline] 切换建议: {decision['switch_reason']}")
                        return {
                            "status": "dataset_dead",
                            "discipline_decision": decision,
                            "recommendation": "切换下一数据集"
                        }
        
        # 1. 开始监控（如果启用）
        if enable_monitoring:
            self.monitor.start_monitoring(wave, dataset)
        
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
            if enable_monitoring:
                self.monitor.complete_monitoring(wave)
            return {"status": "gate_failed"}
        
        # 多样性增强阶段
        if enhance_diversity != "never":
            passed = self.stage_diversity_enhance(ck, passed, enhance_mode=enhance_diversity)
        
        if dry_run:
            print(f"[dry-run] 将提交 {len(passed)} 个表达式")
            for i, p in enumerate(passed, 1):
                print(f"  {i}. {p['expr']}")
            if enable_monitoring:
                self.monitor.complete_monitoring(wave)
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
            
            # 记录监控数据
            if enable_monitoring:
                self.monitor.record_batch(wave, multisim_id, len(passed), 0, 0)
                self.monitor.complete_monitoring(wave)
            
            return {
                "status": "submitted",
                "multisim_id": multisim_id,
                "count": len(passed)
            }
        
        # 保存 checkpoint
        ck.save(self._get_checkpoint_path(wave))
        
        # 完成监控
        if enable_monitoring:
            self.monitor.complete_monitoring(wave)
        
        return {
            "status": "ready",
            "count": len(passed),
            "checkpoint": self._get_checkpoint_path(wave)
        }
    
    def generate_integrated_report(self, waves: int = 10) -> Dict:
        """生成综合的多样性+纪律评估报告（每10轮调用）"""
        return self.integrated_monitor.generate_integrated_report(waves=waves)


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
    p.add_argument("--no-discipline", action="store_true", help="禁用纪律执行")
    p.add_argument("--no-monitoring", action="store_true", help="禁用监控")
    
    # diversity-report 命令
    sub.add_parser("diversity-report")
    
    # integrated-report 命令（每10轮综合评估）
    p = sub.add_parser("integrated-report")
    p.add_argument("--waves", type=int, default=10, help="评估波次数")
    
    # discipline-assess 命令（评估数据集状态）
    p = sub.add_parser("discipline-assess")
    p.add_argument("--dataset", required=True, help="数据集名称")
    
    # discipline-decide 命令（生成切换决策）
    p = sub.add_parser("discipline-decide")
    p.add_argument("--dataset", required=True, help="数据集名称")
    
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
            dry_run=args.dry_run,
            enable_discipline=not args.no_discipline,
            enable_monitoring=not args.no_monitoring
        )
        print(json.dumps(result, ensure_ascii=False, indent=1))
    
    elif args.cmd == "diversity-report":
        # TODO: 实现多样性报告
        print("[diversity-report] 待实现")
    
    elif args.cmd == "integrated-report":
        report = pipeline.generate_integrated_report(waves=args.waves)
        print(json.dumps(report, ensure_ascii=False, indent=1))
    
    elif args.cmd == "discipline-assess":
        evidence = pipeline.discipline.assess_dataset(args.dataset)
        if evidence:
            print(json.dumps(evidence, ensure_ascii=False, indent=2))
        else:
            print(f"数据集 {args.dataset} 无历史数据")
    
    elif args.cmd == "discipline-decide":
        decision = pipeline.discipline.decide_switch(args.dataset)
        if decision:
            print(json.dumps(decision, ensure_ascii=False, indent=2))
        else:
            print(f"数据集 {args.dataset} 无切换决策")


if __name__ == "__main__":
    main()
