# 分层阈值优化方案（Tiered Threshold Optimization）

**日期**: 2026-08-31  
**提案人**: USER  
**状态**: 已批准实施  

## 1. 背景与问题

当前 IND 区域 REGULAR alpha 挖掘战役（目标 20 个可提交）面临的核心瓶颈：

- **单字段回测阈值过严**: Sharpe≥1.58 且 Fitness≥1.0 的硬闸导致候选池枯竭
- **历史数据**: 112 个回测中仅 3 个（2.7%）达标，且全部因 prod_corr≥0.7 被拒
- **组合空间压缩**: 高 Sharpe 信号往往高度相关，缺乏低相关组合腿

**用户洞察**: 单字段特征工程阶段，Sharpe≥1.0 且 Fitness≥0.8 的信号即可作为组合候选，经多字段正交组合后有望达到提交标准。

## 2. 理论依据

### 2.1 组合信号的 Sharpe 叠加效应

当两个信号满足：
- 各自 Sharpe ≥ 1.0（有独立信息）
- 相关性 ρ < 0.3（低重叠）

组合后预期 Sharpe：
```
S_combo ≈ √(S₁² + S₂² + 2ρS₁S₂)
```

若 S₁=S₂=1.2, ρ=0.2，则 S_combo ≈ 1.67 —— **超过 1.58 阈值**。

### 2.2 分层筛选的经济学逻辑

| 阶段 | 信号性质 | 合理阈值 | 逻辑 |
|:---|:---|:---|:---|
| Wave 1 单字段 | 原始特征暴露 | Sharpe≥1.0, Fitness≥0.8 | 捕捉"有信息但未提纯"的原始信号 |
| Wave 2+ 组合/优化后 | 多字段正交组合 | Sharpe≥1.58, Fitness≥1.0 | 组合后应达到平台提交标准 |

## 3. 分层阈值体系

### 3.1 三层漏斗模型

```
原始回测结果
    │
    ▼
┌─────────────────┐
│ 硬拒绝线         │  Sharpe < 0.5 或 Fitness < 0.3 或 Turnover > 0.6
│ (直接丢弃)       │  → 信息含量过低，组合也无法挽救
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 候选池线         │  Sharpe ≥ 1.0 且 Fitness ≥ 0.8 且 Turnover ≤ 0.4
│ (COMBO_CANDIDATE)│  → 有独立信息，可作为组合腿
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 优选线           │  Sharpe ≥ 1.58 且 Fitness ≥ 1.0 且 prod_corr < 0.7
│ (DIRECT_SUBMIT)  │  → 单字段已达标，优先评审
└─────────────────┘
```

### 3.2 阈值参数表

| 参数 | 原阈值 | 新阈值 | 适用阶段 | 理由 |
|:---|:---|:---|:---|:---|
| **Sharpe (硬拒绝）** | - | < 0.5 | Wave 1 | 信息含量过低 |
| **Sharpe （候选池）** | ≥1.58 | ≥1.0 | Wave 1 | 保留组合潜力股 |
| **Sharpe （优选）** | ≥1.58 | ≥1.58 | Wave 2+ | 平台提交标准 |
| **Fitness （候选池）** | ≥1.0 | ≥0.8 | Wave 1 | 允许轻微过拟合，组合后稀释 |
| **Fitness （优选）** | ≥1.0 | ≥1.0 | Wave 2+ | 平台提交标准 |
| **Turnover** | ≤0.4 | ≤0.4 | 所有阶段 | 高换手是硬约束，组合难救 |
| **prod_corr** | <0.7 | <0.7 | 所有阶段 | 平台红线，不可妥协 |
| **self_corr （组合）** | <0.7 | <0.3 | Wave 2+ | 保证组合多样性 |

## 4. 实施变更

### 4.1 修改文件清单

| 文件 | 变更类型 | 变更内容 |
|:---|:---|:---|
| `tools/quality_predict.py` | 修改 | 新增分层阈值常量与判定逻辑 |
| `tools/wave_gate.py` | 修改 | 集成分层阈值到门禁报告 |
| `tools/s4_prescreen.py` | 修改 | 支持 COMBO_CANDIDATE 分类 |
| `docs/reference/feature_engineering_sop.md` | 更新 | 添加分层阈值说明 |

### 4.2 新增常量定义

```python
# tools/quality_predict.py

# 原阈值（平台提交标准）
SHARPE_GATE = 1.58
FITNESS_GATE = 1.0
SELF_CORR_GATE = 0.7

# 新增：分层阈值（Wave 1 单字段候选池）
SHARPE_COMBO_GATE = 1.0      # 组合候选池 Sharpe 下限
FITNESS_COMBO_GATE = 0.8     # 组合候选池 Fitness 下限
TURNOVER_COMBO_GATE = 0.4    # 组合候选池 Turnover 上限

# 新增：硬拒绝线（直接丢弃）
SHARPE_HARD_REJECT = 0.5
FITNESS_HARD_REJECT = 0.3
TURNOVER_HARD_REJECT = 0.6
```

### 4.3 判定逻辑变更

**原逻辑**（二分类）:
```python
if sharpe >= 1.58 and fitness >= 1.0:
    verdict = "EXPECTED_PASS"
else:
    verdict = "EXPECTED_BLOCK"
```

**新逻辑**（三分类）:
```python
if sharpe < 0.5 or fitness < 0.3 or turnover > 0.6:
    verdict = "HARD_REJECT"  # 直接丢弃
elif sharpe >= 1.58 and fitness >= 1.0 and prod_corr < 0.7:
    verdict = "DIRECT_SUBMIT"  # 快速通道
elif sharpe >= 1.0 and fitness >= 0.8 and turnover <= 0.4:
    verdict = "COMBO_CANDIDATE"  # 组合池
else:
    verdict = "WEAK_SIGNAL"  # 弱信号，仅当组合池不足时考虑
```

## 5. 组合策略优先级

当从候选池选腿组合时，按以下优先级：

| 优先级 | 组合类型 | 示例 | 预期效果 |
|:---|:---|:---|:---|
| P0 | 高 Sharpe + 低相关 | S=1.7 (behavioral) + S=1.2 (risk) | 稀释相关性，保持强度 |
| P1 | 双中等 Sharpe + 极低相关 | S=1.3 + S=1.2, ρ<0.2 | 1+1>2 效应 |
| P2 | 主信号 + 辅助信号 | S=1.5 （主） + S=0.9 （辅助， ρ<0.1) | 辅助信号提供正交信息 |

## 6. 风险控制

放宽阈值不等于无底线。以下情况即使 Sharpe>1.0 也应谨慎：

- **Turnover > 0.5**: 组合后换手叠加，大概率超标
- **prod_corr > 0.6**: 与现有池太像，组合难以稀释到 <0.7
- **Fitness < 0.5**: 过拟合严重，组合后可能拖累整体

## 7. 验证计划

### 7.1 Dry-run 验证

```bash
# 验证 quality_predict.py 分层阈值逻辑
python tools/quality_predict.py --region IND --status UNSUBMITTED --tiered-threshold

# 验证 wave_gate.py 集成
python tools/wave_gate.py --campaign-dir tracking/IND --dataset risk70 --wave 7 --from-db --tiered-threshold
```

### 7.2 回溯性验证

对 IND 区域已完成的 112 个回测重新分类：
- 原 REJECT 池中筛选 S 1.0-1.58 或 F 0.8-1.0 且 T≤0.4 的 alpha
- 检查它们与现有高 Sharpe 信号的 prod_corr
- 若 prod_corr < 0.4，标记为组合腿候选

## 8. 预期收益

| 指标 | 原阈值 | 新阈值 | 变化 |
|:---|:---|:---|:---|
| Wave 1 候选池规模 | ~3 个 | ~15-20 个 | +400-567% |
| 组合多样性 | 低（高相关） | 高（分层筛选） | 显著提升 |
| 配额利用率 | 2.7% | 13-18% | +5-6 倍 |
| 组合空间 | 受限 | 扩大 | 1+1>2 效应 |

## 9. 后续行动

1. **立即实施**: 修改 `quality_predict.py` 和 `wave_gate.py`
2. **Wave 7 应用**: 探索 RISK/PV 数据集时应用新阈值
3. **回溯筛选**: 从 Wave 2-6 的 REJECT 池中抢救组合候选
4. **文档更新**: 同步更新 `feature_engineering_sop.md`

---

**批准**: USER  
**实施**: AI Agent  
**日期**: 2026-08-31
