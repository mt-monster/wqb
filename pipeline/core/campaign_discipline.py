# -*- coding: utf-8 -*-
"""pipeline/core/campaign_discipline.py - 通用战役纪律执行器（区域无关）

核心功能：
1. PROD 墙三档分类：<0.75 深耕 / 0.75-0.80 暂挂 / >0.80 判死
2. 判死证据链闭环：设置空间穷尽 + 结构变体穷尽 + 救援武器实测
3. 数据集切换触发器：满足判死条件自动生成切换建议
4. 候选池状态跟踪：结构化记录每个数据集的挖掘状态

用法:
  from pipeline.core.campaign_discipline import CampaignDiscipline
  
  discipline = CampaignDiscipline(ledger_path="tracking/KOR/kor_d1_campaign_state.json")
  evidence = discipline.assess_dataset("chart_cnn_alpha")
  decision = discipline.decide_switch("chart_cnn_alpha")
"""
import collections
import datetime
import json
import os
import re
from typing import Dict, List, Optional, Any

# PROD 墙三档阈值
PROD_DEEP_MIN = 0.75      # <0.75: 深耕，继续优化
PROD_SUSPEND_MIN = 0.80   # 0.75-0.80: 暂挂，保留候选池
                          # >0.80: 判死封存

# 救援武器清单（论坛工具箱）
RESCUE_WEAPONS = [
    "ts_target_tvr_decay",           # 定目标换手
    "residual_diff_template",        # 残差差分模板
    "vec_avg_to_vec_max",            # vec_avg→vec_max 换聚合
    "neutralization_switch",         # 中性化切换
    "inner_outer_neutralization",    # 内细外粗二次中性化
    "weight_perturbation",           # 权重扰动
    "layer_switch",                  # 换层（rank→group_rank→quantile→signed_power）
    "subtract_structure",            # subtract 多空差结构
    "horizon_mix",                   # 跨 horizon 组合
    "decay_gradient",                # decay 梯度扫描
]


class CampaignDiscipline:
    """通用战役纪律执行器"""
    
    def __init__(self, ledger_path: str):
        """初始化
        
        Args:
            ledger_path: 台账文件路径（如 tracking/KOR/kor_d1_campaign_state.json）
        """
        self.ledger_path = ledger_path
        self.bak_path = ledger_path + ".bak"
    
    def _load_ledger(self) -> Dict:
        """加载台账"""
        if not os.path.exists(self.ledger_path):
            return {"waves": [], "dataset_pool": {}}
        with open(self.ledger_path, encoding="utf-8-sig") as f:
            return json.load(f)
    
    def _save_ledger(self, data: Dict):
        """保存台账"""
        import shutil
        if os.path.exists(self.ledger_path):
            shutil.copy2(self.ledger_path, self.bak_path)
        tmp = self.ledger_path + ".tmp"
        with open(tmp, "w", encoding="utf-8-sig") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        os.replace(tmp, self.ledger_path)
    
    def _get_dataset_waves(self, state: Dict, dataset: str) -> List[Dict]:
        """获取指定数据集的所有波次"""
        waves = []
        for w in state.get("waves", []):
            # 格式1：顶层 dataset 字段
            if w.get("dataset") == dataset:
                waves.append(w)
            # 格式2：检查嵌套的 multisims 中的 dataset
            elif any(ms.get("dataset") == dataset for ms in w.get("multisims", [])):
                waves.append(w)
        return waves
    
    def _extract_prod_correlations(self, waves: List[Dict]) -> List[float]:
        """从波次中提取所有 PROD 相关性数据"""
        prods = []
        for w in waves:
            verdict = w.get("verdict", "")
            # 提取 PC0.xxxx 模式
            for m in re.finditer(r"PC\s*0\.(\d+)", verdict):
                prods.append(float(f"0.{m.group(1)}"))
            # 提取 PROD相关=0.xxxx 模式
            for m in re.finditer(r"PROD相关[=:]?\s*0\.(\d+)", verdict):
                prods.append(float(f"0.{m.group(1)}"))
            # 提取 PROD 0.xxxx 模式
            for m in re.finditer(r"PROD\s+0\.(\d+)", verdict):
                prods.append(float(f"0.{m.group(1)}"))
        return prods
    
    def _extract_settings_tried(self, waves: List[Dict]) -> set:
        """提取已尝试的设置组合"""
        settings = set()
        for w in waves:
            for ms in w.get("multisims", []):
                s = ms.get("setting", "")
                if s:
                    settings.add(s)
        return settings
    
    def _extract_structures_tried(self, waves: List[Dict]) -> set:
        """提取已尝试的结构类型"""
        structures = set()
        for w in waves:
            for ms in w.get("multisims", []):
                style = ms.get("style", "")
                if "rank" in style.lower():
                    structures.add("rank")
                if "group_rank" in style.lower():
                    structures.add("group_rank")
                if "quantile" in style.lower():
                    structures.add("quantile")
                if "signed_power" in style.lower():
                    structures.add("signed_power")
                if "subtract" in style.lower():
                    structures.add("subtract")
                if "linear" in style.lower() or "mix" in style.lower():
                    structures.add("linear_mix")
                if "trade_when" in style.lower():
                    structures.add("event_gated")
        return structures
    
    def assess_dataset(self, dataset: str) -> Optional[Dict]:
        """评估数据集的挖掘状态，生成判死证据链报告
        
        Args:
            dataset: 数据集名称
            
        Returns:
            判死证据链报告，包含分类、PROD 统计、判死四要素等
        """
        state = self._load_ledger()
        waves = self._get_dataset_waves(state, dataset)
        
        if not waves:
            return None
        
        # 提取关键指标
        prods = self._extract_prod_correlations(waves)
        settings = self._extract_settings_tried(waves)
        structures = self._extract_structures_tried(waves)
        
        # 统计
        total_waves = len(waves)
        total_multisims = sum(len(w.get("multisims", [])) for w in waves)
        
        # PROD 墙分析
        prod_min = min(prods) if prods else None
        prod_max = max(prods) if prods else None
        prod_avg = sum(prods) / len(prods) if prods else None
        
        # 判死证据链评估
        evidence = {
            "dataset": dataset,
            "total_waves": total_waves,
            "total_multisims": total_multisims,
            "prod_stats": {
                "min": prod_min,
                "max": prod_max,
                "avg": prod_avg,
                "count": len(prods),
            },
            "settings_tried": sorted(settings),
            "structures_tried": sorted(structures),
            "rescue_weapons_tried": [],
            "rescue_weapons_remaining": [],
            "verdicts": [w.get("verdict", "")[:200] for w in waves[-3:]],
        }
        
        # 检查救援武器实测情况
        verdict_text = " ".join(w.get("verdict", "") for w in waves)
        for weapon in RESCUE_WEAPONS:
            if weapon.replace("_", "") in verdict_text.replace("_", "").lower():
                evidence["rescue_weapons_tried"].append(weapon)
            else:
                evidence["rescue_weapons_remaining"].append(weapon)
        
        # 判死判定
        death_criteria = {
            "prod_wall_structural": prod_min is not None and prod_min > PROD_SUSPEND_MIN,
            "settings_exhausted": len(settings) >= 4,
            "structures_exhausted": len(structures) >= 5,
            "rescue_weapons_exhausted": len(evidence["rescue_weapons_remaining"]) == 0,
        }
        evidence["death_criteria"] = death_criteria
        evidence["death_score"] = sum(death_criteria.values())
        
        # 三档分类
        if prod_min is None:
            evidence["category"] = "UNKNOWN"
            evidence["recommendation"] = "需要更多 PROD 相关性数据"
        elif prod_min < PROD_DEEP_MIN:
            evidence["category"] = "DEEP"
            evidence["recommendation"] = f"PROD 墙 {prod_min:.3f} < {PROD_DEEP_MIN}，有突破空间，建议深耕"
        elif prod_min < PROD_SUSPEND_MIN:
            evidence["category"] = "SUSPEND"
            evidence["recommendation"] = f"PROD 墙 {prod_min:.3f} 在 {PROD_DEEP_MIN}-{PROD_SUSPEND_MIN} 区间，建议暂挂保留候选池"
        else:
            evidence["category"] = "DEAD"
            evidence["recommendation"] = f"PROD 墙 {prod_min:.3f} > {PROD_SUSPEND_MIN}，建议判死封存"
        
        # 判死证据链完整性检查
        if evidence["category"] == "DEAD":
            missing = []
            if not death_criteria["settings_exhausted"]:
                missing.append("设置空间未穷尽（<4种）")
            if not death_criteria["structures_exhausted"]:
                missing.append("结构变体未穷尽（<5种）")
            if not death_criteria["rescue_weapons_exhausted"]:
                missing.append(f"救援武器未实测：{', '.join(evidence['rescue_weapons_remaining'][:3])}")
            if missing:
                evidence["death_evidence_gap"] = missing
                evidence["recommendation"] += f"，但证据链不完整：{'；'.join(missing)}"
        
        return evidence
    
    def decide_switch(self, dataset: str) -> Optional[Dict]:
        """生成数据集切换决策建议
        
        Args:
            dataset: 数据集名称
            
        Returns:
            切换决策，包含是否触发切换、下一目标等
        """
        evidence = self.assess_dataset(dataset)
        if not evidence:
            return None
        
        decision = {
            "dataset": dataset,
            "category": evidence["category"],
            "death_score": evidence["death_score"],
            "recommendation": evidence["recommendation"],
            "switch_trigger": False,
            "next_targets": [],
        }
        
        # 切换触发条件
        if evidence["category"] == "DEAD" and evidence["death_score"] >= 3:
            decision["switch_trigger"] = True
            decision["switch_reason"] = "满足判死条件，建议切换下一数据集"
            
            # 推荐下一目标（从台账中获取）
            state = self._load_ledger()
            pool = state.get("dataset_pool", {})
            for ds, info in pool.items():
                if ds != dataset and info.get("status") in ("unexplored", "suspended"):
                    decision["next_targets"].append({
                        "dataset": ds,
                        "status": info.get("status"),
                        "priority": info.get("priority", 99),
                    })
            decision["next_targets"].sort(key=lambda x: x["priority"])
        
        return decision
    
    def update_dataset_pool(self, dataset: str, status: str, priority: int = 99, notes: str = ""):
        """更新数据集候选池状态
        
        Args:
            dataset: 数据集名称
            status: 状态（unexplored/probe/deep/suspend/dead）
            priority: 优先级（数字越小优先级越高）
            notes: 备注
        """
        state = self._load_ledger()
        pool = state.setdefault("dataset_pool", {})
        pool[dataset] = {
            "status": status,
            "priority": priority,
            "notes": notes,
            "updated_at": datetime.date.today().isoformat(),
        }
        self._save_ledger(state)
    
    def get_dataset_pool(self) -> Dict:
        """获取数据集候选池"""
        state = self._load_ledger()
        return state.get("dataset_pool", {})


def prod_category(prod_corr: Optional[float]) -> tuple:
    """PROD 墙三档分类
    
    Args:
        prod_corr: PROD 相关性值
        
    Returns:
        (分类, 说明)
    """
    if prod_corr is None:
        return "UNKNOWN", "需查 PROD 相关性"
    if prod_corr < PROD_DEEP_MIN:
        return "DEEP", f"PROD {prod_corr:.3f} < {PROD_DEEP_MIN}，有突破空间"
    if prod_corr < PROD_SUSPEND_MIN:
        return "SUSPEND", f"PROD {prod_corr:.3f} 在 {PROD_DEEP_MIN}-{PROD_SUSPEND_MIN}，暂挂"
    return "DEAD", f"PROD {prod_corr:.3f} > {PROD_SUSPEND_MIN}，判死"
