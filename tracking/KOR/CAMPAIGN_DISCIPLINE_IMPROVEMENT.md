# KOR 战役纪律执行流程改进总结

## 改进目标

将"有纪律地切换"原则从人工判断升级为自动化流程，确保：
1. **PROD 墙三档分类**：<0.75 深耕 / 0.75-0.80 暂挂 / >0.80 判死
2. **判死证据链闭环**：设置空间穷尽 + 结构变体穷尽 + 救援武器实测
3. **数据集切换触发器**：满足判死条件自动生成切换建议
4. **候选池状态跟踪**：结构化记录每个数据集的挖掘状态

---

## 新增工具

### 1. campaign_discipline.py - 战役纪律执行器

**核心功能**：
- `assess_dataset(dataset)`: 评估数据集的挖掘状态，生成判死证据链报告
- `decide_switch(dataset)`: 生成数据集切换决策建议
- `pool_manage(action, ...)`: 管理数据集候选池

**PROD 墙三档分类**：
```python
PROD_DEEP_MIN = 0.75      # <0.75: 深耕，继续优化
PROD_SUSPEND_MIN = 0.80   # 0.75-0.80: 暂挂，保留候选池
                          # >0.80: 判死封存
```

**判死证据链四要素**：
1. `prod_wall_structural`: PROD min > 0.80
2. `settings_exhausted`: 设置空间 >= 4 种
3. `structures_exhausted`: 结构变体 >= 5 种
4. `rescue_weapons_exhausted`: 救援武器全部实测

**救援武器清单**（10 种）：
- ts_target_tvr_decay（定目标换手）
- residual_diff_template（残差差分模板）
- vec_avg_to_vec_max（换聚合）
- neutralization_switch（中性化切换）
- inner_outer_neutralization（内细外粗二次中性化）
- weight_perturbation（权重扰动）
- layer_switch（换层）
- subtract_structure（subtract 多空差结构）
- horizon_mix（跨 horizon 组合）
- decay_gradient（decay 梯度扫描）

### 2. review_wave_v2.py - 增强版波次评审

**新增功能**：
- PROD 墙三档分类自动标注
- 判死证据链完整性检查
- 数据集切换建议自动生成
- 候选池状态自动回写

**输出示例**：
```
id         sh    fit   2y   mg_bp   tvr%    rn     PC      cat   walls
VkGz2vrb   1.68  1.04  1.98   7.60  21.10  0.00  0.767  SUSPEND PROD>0.7
GrGz3ZvP   1.63  1.08  1.99   7.20  18.50  0.00  0.922     DEAD PROD>0.7

PROD 分类: DEEP=0 SUSPEND=1 DEAD=1 UNKNOWN=0

[纪律评估] multi_source_model: SUSPEND - PROD 墙 0.767 在 0.75-0.8 区间，建议暂挂保留候选池
```

### 3. wave_planner.py - 波次规划器

**核心功能**：
- `plan_next_wave(current_dataset)`: 基于判死证据链自动规划下一波次
- `generate_deepen_strategy(dataset, evidence)`: 生成深耕策略

**四种规划动作**：
1. **probe**: 无历史数据，开始探针阶段
2. **deepen**: PROD < 0.75，继续深耕（生成设置空间/结构变体/救援武器策略）
3. **suspend**: PROD 0.75-0.80，暂挂保留候选池
4. **switch**: PROD > 0.80 且判死证据链完整，切换下一数据集

---

## 使用流程

### 步骤 1：评估当前数据集

```bash
cd tracking/KOR/scripts
python campaign_discipline.py assess --dataset multi_source_model
```

**输出**：
```json
{
  "dataset": "multi_source_model",
  "category": "SUSPEND",
  "prod_stats": {"min": 0.7668, "max": 0.7668, "avg": 0.7668},
  "death_score": 0,
  "recommendation": "PROD 墙 0.767 在 0.75-0.8 区间，建议暂挂保留候选池",
  "settings_tried": ["STATISTICAL d4 t0.08", "STATISTICAL d6 t0.06", "SECTOR d4 t0.08"],
  "structures_tried": ["rank"],
  "rescue_weapons_remaining": ["ts_target_tvr_decay", "residual_diff_template", ...]
}
```

### 步骤 2：生成切换决策

```bash
python campaign_discipline.py decide --dataset multi_source_model
```

**输出**：
```json
{
  "dataset": "multi_source_model",
  "category": "SUSPEND",
  "switch_trigger": false,
  "recommendation": "PROD 墙 0.767 在 0.75-0.8 区间，建议暂挂保留候选池"
}
```

### 步骤 3：规划下一波次

```bash
python wave_planner.py next --current-dataset multi_source_model --wave 17A
```

**输出**：
```
============================================================
波次规划: SUSPEND
============================================================
数据集: multi_source_model
原因: PROD 0.767 在 0.75-0.8 区间，暂挂保留候选池，待异源杠杆

候选池保留: 2 个 alpha
============================================================
```

### 步骤 4：评审波次（带纪律）

```bash
python review_wave_v2.py --multisim <id> --dataset multi_source_model --tag wave17A --write-ledger
```

---

## 与现有流程的集成

### 改进前 vs 改进后

| 环节 | 改进前 | 改进后 |
|------|--------|--------|
| **PROD 墙判断** | 人工判断，无分类 | 自动三档分类（DEEP/SUSPEND/DEAD） |
| **判死决策** | 人工判断，易遗漏 | 自动检查四要素证据链 |
| **切换触发** | 人工决定，无标准 | 自动触发（death_score >= 3） |
| **深耕策略** | 人工设计，无系统 | 自动生成（设置空间/结构变体/救援武器） |
| **候选池管理** | 简单记录 | 结构化状态跟踪（unexplored/probe/deep/suspend/dead） |

### 与 build_wave.py 的集成

```python
# 在 build_wave.py 中加入纪律检查
from campaign_discipline import assess_dataset

def build_wave_with_discipline(dataset, wave, size=48):
    # 先评估数据集状态
    evidence = assess_dataset(dataset)
    
    if evidence and evidence["category"] == "DEAD" and evidence["death_score"] >= 3:
        print(f"[discipline] {dataset} 已判死，建议切换数据集")
        print(f"[discipline] 证据: PROD {evidence['prod_stats']['min']:.3f}, "
              f"death_score={evidence['death_score']}/4")
        return None
    
    # 继续正常选波流程
    return build_wave(dataset, wave, size)
```

---

## 实证案例

### 案例 1：multi_source_model（SUSPEND）

**状态**：
- PROD min: 0.7668（在 0.75-0.80 区间）
- 设置空间: 3 种已尝试（未穷尽）
- 结构变体: 1 种已尝试（未穷尽）
- 救援武器: 0 种已实测（未穷尽）

**决策**：暂挂保留候选池，待异源杠杆

**候选池**：
- VkGz2vrb: sh1.68/fit1.04/2y1.98/PROD 0.7668
- GrGz3ZvP: sh1.63/fit1.08/2y1.99/PROD 0.922（互相关 0.922，只留一个）

### 案例 2：chart_cnn_alpha（DEAD）

**状态**：
- PROD min: 0.8296（> 0.80）
- 设置空间: 4+ 种已尝试（穷尽）
- 结构变体: 5+ 种已尝试（穷尽）
- 救援武器: 5 条路线全部失败（权重扰动/换层/subtract/降权重分散/内细外粗中性化）

**决策**：判死封存，切换下一数据集

**证据链**：
- 批 Q/R/S/T/U 全撞 PROD 墙 0.80-0.83
- 五条去 PROD 路线全部失败或代价不可接受
- 按战役规则判 PROD 墙死

---

## 下一步行动

1. **将 campaign_discipline.py 集成到 kor_pipeline.py**
   - 在 `stage_review` 后加入纪律评估
   - 在 `stage_submit_poll` 前检查数据集状态

2. **更新 thresholds.json**
   - 加入 PROD 三档阈值配置
   - 加入判死证据链参数

3. **创建数据集候选池初始化脚本**
   - 扫描所有可用数据集
   - 初始化 dataset_pool 状态

4. **与 wq-brain-campaign-toolkit 集成**
   - 将判死证据链检查加入 5 闸预检
   - 将 PROD 三档分类加入探针 v2 三灯判定

---

## 总结

改进后的回测流程完全体现了"有纪律地切换"原则：

- **不频繁切换**：每个数据集至少完成"探针→结构×设置矩阵→判死证据链"三步
- **不恋战**：满足判死条件（PROD>0.8 且证据链完整）立即封存
- **有标准**：PROD 墙三档分类 + 判死证据链四要素，杜绝主观判断
- **有记录**：候选池状态结构化跟踪，每个决策可追溯
