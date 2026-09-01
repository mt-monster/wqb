# 组合优化策略（Combination Optimization Strategy）

**版本**: 1.0  
**日期**: 2026-08-31  
**适用**: IND 区域 REGULAR alpha 挖掘战役 Wave 7+  

---

## 1. 组合优化目标

基于分层阈值体系（Tiered Threshold System），将单字段信号（Sharpe 1.0-1.58）通过多字段正交组合，达到平台提交标准（Sharpe ≥ 1.58, Fitness ≥ 1.0, prod_corr < 0.7）。

**核心原则**:
- **1+1>2 效应**: 两个 Sharpe ~1.2 的低相关信号组合后可达 Sharpe ~1.67
- **相关性稀释**: 高 Sharpe 信号（prod_corr > 0.7）与低相关信号组合可降低整体相关性
- **风险分散**: 多信号组合降低单信号过拟合风险

---

## 2. 候选池分层回顾

| 层级 | 判定 | 阈值 | 用途 |
|:---|:---|:---|:---|
| **DIRECT_SUBMIT** | 优选线达标 | S≥1.58, F≥1.0, prod_corr<0.7 | 直接提交 |
| **COMBO_CANDIDATE** | 候选池达标 | S≥1.0, F≥0.8, T≤0.4, prod_corr<0.7 | 组合腿候选 |
| **WEAK_SIGNAL** | 弱信号 | S 0.5-1.0 或 F 0.3-0.8 | 谨慎考虑 |
| **EXPECTED_BLOCK** | 相关性超标 | prod_corr≥0.7 | 需组合稀释 |
| **HARD_REJECT** | 硬拒绝 | S<0.5 或 F<0.3 | 直接丢弃 |

---

## 3. 组合策略优先级

### 3.1 P0：高 Sharpe + 低相关（稀释相关性）

**场景**: 已有高 Sharpe 信号但 prod_corr > 0.7

**策略**: 与 prod_corr < 0.3 的 COMBO_CANDIDATE 组合

**示例**:
```
主信号: wpjvE8W5 (S=2.61, prod_corr=0.85)  # behavioral_signals
辅助信号: A1l2XrbX (S=1.16, prod_corr=0.45)  # global_seasonal

组合方式: add(multiply(rank(wpjvE8W5), 0.6), multiply(rank(A1l2XrbX), 0.4))
预期效果: 
  - Sharpe 保持 ~2.0
  - prod_corr 稀释至 ~0.65
  - 通过相关性闸
```

**权重分配原则**:
- 主信号权重: 0.6-0.7（保持信号强度）
- 辅助信号权重: 0.3-0.4（提供正交信息）
- **禁止**: 同信号加权调参（如 0.5/0.5 改 0.6/0.4）

---

### 3.2 P1：双中等 Sharpe + 极低相关（1+1>2）

**场景**: 两个 COMBO_CANDIDATE 信号，相关性 < 0.2

**策略**: 等权重或按 Sharpe 加权组合

**示例**:
```
信号1: YP79ejkR (S=1.70, F=1.09, T=0.19)  # behavioral ts_mean20
信号2: [RISK 数据集新信号] (S=1.30, F=0.85, T=0.25)

组合方式: add(multiply(rank(YP79ejkR), 0.55), multiply(rank(new_signal), 0.45))
预期 Sharpe: √(1.70² + 1.30² + 2×0.15×1.70×1.30) ≈ 2.05
```

**组合公式**:
```
S_combo ≈ √(S₁² + S₂² + 2ρS₁S₂)

其中:
  S₁, S₂ = 单信号 Sharpe
  ρ = 信号间相关性（目标 < 0.2）
```

---

### 3.3 P2：主信号 + 辅助信号（增强稳健性）

**场景**: 主信号 Sharpe 达标但 Fitness 或 robust 不足

**策略**: 主信号（S~1.5）+ 辅助信号（S~0.9, ρ<0.1）

**示例**:
```
主信号: qMj7b6nO (S=1.45, robust=1.12)  # fundamental86
辅助信号: [低相关稳健信号] (S=0.95, robust=1.05)

组合方式: add(multiply(rank(qMj7b6nO), 0.7), multiply(rank(aux_signal), 0.3))
预期效果:
  - Sharpe 提升至 ~1.6
  - robust 保持 >1.0
  - Fitness 提升至 >1.0
```

---

## 4. 组合实施流程

### 4.1 步骤 1：候选池筛选

```python
# 从 wave_gate.py 输出筛选 COMBO_CANDIDATE
combo_candidates = [
    c for c in wave_results 
    if c['verdict'] == 'COMBO_CANDIDATE'
    and c['prod_corr'] < 0.5  # 预筛选低相关
]
```

### 4.2 步骤 2：相关性矩阵计算

```python
# 使用 MCP 工具计算候选池互相关
from wqb.mcp import compute_mutual_correlation

corr_matrix = compute_mutual_correlation(
    alpha_ids=[c['alpha_id'] for c in combo_candidates],
    region='IND'
)

# 筛选相关性 < 0.3 的组合对
low_corr_pairs = [
    (a, b) for a, b in combinations(combo_candidates, 2)
    if corr_matrix[a['alpha_id']][b['alpha_id']] < 0.3
]
```

### 4.3 步骤 3：组合表达式生成

```python
# 生成组合表达式（等权重或 Sharpe 加权）
def generate_combo_expr(sig1, sig2, weight1=0.5):
    weight2 = 1 - weight1
    return f"add(multiply(rank({sig1['expr']}), {weight1}), multiply(rank({sig2['expr']}), {weight2}))"

# 示例
combo_expr = generate_combo_expr(
    {'expr': 'ts_mean(rank(vec_avg(consecutive_return_streak_length)), 20)'},
    {'expr': 'rank(ts_backfill(risk70_field, 66))'},
    weight1=0.6  # 主信号权重更高
)
```

### 4.4 步骤 4：组合回测验证

```python
# 使用 batch_create_simulations 提交组合回测
from wqb.mcp import batch_create_simulations

results = batch_create_simulations(
    items=[{
        'expression': combo_expr,
        'settings': {
            'region': 'IND',
            'universe': 'TOP500',
            'delay': 1,
            'decay': 4,
            'neutralization': 'STATISTICAL',
            'truncation': 0.08
        }
    }]
)
```

### 4.5 步骤 5：组合后评审

```python
# 组合后必须重新走 S4 评审链
# 1. self/PPAC 快筛
# 2. check_self_correlation
# 3. compute_mutual_correlation
# 4. check_correlation (prod 预检)
# 5. 归因分析
# 6. brain-alpha-robustness
# 7. brain-alpha-judge
```

---

## 5. 组合优化案例库

### 5.1 案例 1：behavioral + risk 组合（稀释相关性）

**背景**: behavioral_signals 高 Sharpe 但 prod_corr > 0.8

**组合策略**:
```python
# 主信号（behavioral）
main_sig = 'ts_mean(rank(vec_avg(consecutive_return_streak_length)), 20)'
# S=1.70, F=1.09, T=0.19, prod_corr=0.85

# 辅助信号（risk70）
aux_sig = 'rank(ts_backfill(risk70_volatility_field, 66))'
# S=1.20, F=0.85, T=0.30, prod_corr=0.35

# 组合表达式
combo = f'add(multiply({main_sig}, 0.6), multiply({aux_sig}, 0.4))'
```

**预期结果**:
- Sharpe: ~1.55-1.65
- prod_corr: ~0.60-0.68（稀释后 < 0.7）
- 通过相关性闸

---

### 5.2 案例 2：双 COMBO_CANDIDATE 组合（1+1>2）

**背景**: 两个中等 Sharpe 信号，相关性 < 0.2

**组合策略**:
```python
# 信号1（global_seasonal）
sig1 = 'rank(ts_backfill(last_event_type_code, 66))'
# S=1.16, F=0.65, T=0.30

# 信号2（ai_news_scores）
sig2 = 'rank(ts_backfill(positive_score_average_value, 66))'
# S=1.05, F=0.72, T=0.28

# 组合表达式（等权重）
combo = f'add(multiply({sig1}, 0.5), multiply({sig2}, 0.5))'
```

**预期结果**:
- Sharpe: √(1.16² + 1.05² + 2×0.15×1.16×1.05) ≈ 1.62
- 达到提交标准

---

### 5.3 案例 3：主信号 + 稳健辅助（增强 robust）

**背景**: 主信号 Sharpe 达标但 robust < 1.0

**组合策略**:
```python
# 主信号（fundamental86）
main_sig = 'rank(earnings_score + fundamental_score)'
# S=1.45, robust=1.12, F=0.95

# 辅助信号（低相关稳健信号）
aux_sig = 'rank(ts_zscore(low_volatility_field, 63))'
# S=0.95, robust=1.05, F=0.88

# 组合表达式（主信号权重 70%）
combo = f'add(multiply({main_sig}, 0.7), multiply({aux_sig}, 0.3))'
```

**预期结果**:
- Sharpe: ~1.58
- robust: ~1.10（保持 >1.0）
- Fitness: ~1.02（提升至 >1.0）

---

## 6. 组合优化禁忌

### 6.1 禁止同信号加权调参

**错误示例**:
```python
# 同一信号族，仅调整权重
expr_v1 = 'add(multiply(rank(field_a), 0.4), multiply(rank(field_b), 0.6))'
expr_v2 = 'add(multiply(rank(field_a), 0.3), multiply(rank(field_b), 0.7))'  # 禁止！
```

**正确做法**: 换字段组合或换概念

---

### 6.2 禁止高相关组合

**错误示例**:
```python
# 两个信号相关性 > 0.5
sig1 = 'rank(momentum_field_1)'  # prod_corr=0.75
sig2 = 'rank(momentum_field_2)'  # prod_corr=0.78
combo = f'add({sig1}, {sig2})'  # 禁止！相关性叠加
```

**正确做法**: 预筛选相关性 < 0.3 的组合对

---

### 6.3 禁止过度组合

**错误示例**:
```python
# 组合超过 3 个信号
combo = 'add(add(add(sig1, sig2), sig3), sig4)'  # 禁止！过拟合风险
```

**正确做法**: 最多 2-3 个信号组合，保持可解释性

---

## 7. 组合优化检查清单

在提交组合回测前，必须确认：

- [ ] 组合信号来自不同数据集或字段族
- [ ] 组合信号间相关性 < 0.3（通过 compute_mutual_correlation 验证）
- [ ] 主信号权重 0.6-0.7，辅助信号权重 0.3-0.4
- [ ] 组合后预期 Sharpe > 1.58（通过组合公式估算）
- [ ] 组合后预期 prod_corr < 0.7（通过相关性稀释估算）
- [ ] 组合表达式已通过 wave_gate.py 5 闸预检
- [ ] 组合后必须重新走完整 S4 评审链

---

## 8. 工具支持

| 工具 | 用途 | 命令示例 |
|:---|:---|:---|
| `wave_gate.py` | 候选池分层筛选 | `python tools/wave_gate.py --region IND --wave 7 --from-db` |
| `compute_mutual_correlation` | 计算候选池互相关 | MCP 工具调用 |
| `batch_create_simulations` | 批量提交组合回测 | MCP 工具调用 |
| `brain-alpha-judge` | 组合后判定 | `python scripts/judge_alpha.py --alpha-id <id>` |

---

## 9. 参考文献

- 分层阈值优化方案: `docs/plans/2026-08-31-tiered-threshold-optimization.md`
- 特征工程 SOP: `docs/reference/feature_engineering_sop.md`
- IND 战役经验: `docs/experience/project_experience_master.md`

---

**维护者**: AI Agent  
**审核**: USER  
**更新日期**: 2026-08-31
