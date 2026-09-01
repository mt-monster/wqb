# Alpha 挖掘优化工具集

本目录包含 IND 区域 REGULAR alpha 挖掘战役的优化工具，基于 2026-08-30 会话经验沉淀。

## 工具清单

### 1. S0 增强预筛（s0_enhanced_screening.py）

**功能**：三层预筛机制，提前判死低潜力数据集

**三层机制**：
1. 平台硬门槛（cov/alphaCount/fields）
2. WebDataScope 社区验证（isos.datafield sharpe/count）
3. 字段级体检（分布形状/覆盖率/频率）

**用法**：
```bash
python tools/s0_enhanced_screening.py --region IND --delay 1 \
    --datasets pv70,ai_news_scores,other567 \
    --zip data/WebData.zip --json-out s0_screen.json
```

**输出**：ATTACK / CAUTION / REJECT 三层分类

---

### 2. 探针批模式（probe_batch_mode.py）

**功能**：2+6 探针批，早期判死节省配额

**核心逻辑**：
- 先跑 2 条探针（最强候选）
- 若全灭（Sharpe<0.5），判死数据集，节省 6 条配额
- 若达标（Sharpe>1.0），继续跑剩余 6 条

**用法**：
```bash
python tools/probe_batch_mode.py --campaign-dir tracking/IND \
    --dataset pv70 --wave 125 --candidates candidates.json
```

**集成到 wave_gate**：
```bash
python tools/wave_gate.py --campaign-dir tracking/IND --dataset pv70 \
    --wave 125 --candidates candidates.json --probe-mode
```

---

### 3. 批量评审工具（batch_get_alpha_metrics）

**功能**：MCP 批量获取 alpha 指标，S4 预筛分层

**优势**：比逐条调用 get_alpha_details 效率高 8 倍

**用法**（MCP 工具）：
```python
# 在 Agent 会话中直接调用
mcp__wq-brain-http__batch_get_alpha_metrics(
    alpha_ids=["58l2or1N", "O07MlNb1", "Wj7o2aNG"]
)
```

**输出**：READY / REVIEW / REJECT 三层预筛

---

### 4. 七槽填槽并发回测（现行：pipeline.py / mcp_7slot_batch.py）

> ⚠️ **five_slot_executor.py 已于 2026-08-31 归档至 `attic/tools_archive/`**（死代码，被 `mcp_7slot_batch.py` 与 `pipeline.py` 的七槽实现取代）。以下为现行用法。

**功能**：真并发七槽填槽（Token-Bucket C≈7 实测），吞吐提升 7 倍

**核心机制**：
1. 7 批×8 条同提（并发纪律权威见 `wqb-concurrency` §8）
2. 统一轮询，即收即补
3. 单批完成立即补充新批

**用法（二选一）**：
```bash
# A. 战役目录正式路径（checkpoint 续跑 + 配额闸）
python <toolkit>/scripts/pipeline.py --campaign-dir tracking/IND run --dataset <ds> --wave 129 --submit

# B. MCP 客户端（跨区临时批）
python tools/mcp_7slot_batch.py \
    --alpha-json tracking/IND/candidates/<wave>_exprs.json \
    --settings-json tracking/IND/config/settings.json \
    --output-csv tracking/IND/results/mcp_7slot_<ds>.csv \
    --max-in-flight 7 --batch-size 8
```

---

### 5. GEM 强制校验（gem_validator.py）

**功能**：确保 S2 候选池来自 brain-makeSomeGem 管道

**校验规则**：
- GEM 候选占比 ≥80%
- 检查 concept/mechanism/field_source 元数据
- 检查表达式结构特征

**用法**：
```bash
python tools/gem_validator.py --candidates candidates.json --wave 129
```

**集成到 wave_gate**：
```bash
python tools/wave_gate.py --campaign-dir tracking/IND --dataset pv70 \
    --wave 125 --candidates candidates.json --gem-validate
```

---

### 6. 成功配方推广引擎（success_formula_engine.py）

**功能**：基于已验证成功配方生成同族变体

**已验证配方**：
- IND-ANALYST-FUNDAMENTAL-WIN（58l2or1N）
  - 主信号：analyst_revision_percentile_score_long_4（60%）
  - 辅助信号：fnd86_earnings_score（40%）
  - 结构：add(multiply(0.6, A), multiply(0.4, B))

**用法**：
```bash
# 生成字段族变体
python tools/success_formula_engine.py --formula IND-ANALYST-FUNDAMENTAL-WIN \
    --output variants.json --max-variants 8

# 生成多样性变体（不同中性化/decay）
python tools/success_formula_engine.py --formula IND-ANALYST-FUNDAMENTAL-WIN \
    --output diversity.json --diversity-mode
```

---

## 集成工作流

### 完整优化战役流程

```bash
# Step 1: S0 增强预筛
python tools/s0_enhanced_screening.py --region IND --delay 1 \
    --datasets pv70,ai_news_scores,other567 \
    --zip data/WebData.zip --json-out s0_screen.json

# Step 2: 生成候选（基于成功配方）
python tools/success_formula_engine.py --formula IND-ANALYST-FUNDAMENTAL-WIN \
    --output candidates.json --max-variants 8

# Step 3: 门禁校验（GEM + 探针批）
python tools/wave_gate.py --campaign-dir tracking/IND --dataset analyst9 \
    --wave 129 --candidates candidates.json \
    --gem-validate --probe-mode --quality-block

# Step 4: 七槽填槽回测（pipeline.py 或 mcp_7slot_batch.py，见 §4）
python <toolkit>/scripts/pipeline.py --campaign-dir tracking/IND run --dataset analyst9 --wave 129 --submit

# Step 5: S4 批量评审（MCP）
# 在 Agent 会话中调用 batch_get_alpha_metrics
```

---

## 预期收益

| 优化项 | 当前状态 | 优化后 | 提升 |
|--------|---------|--------|------|
| 单数据集配额消耗 | 8 条 | 2-4 条（探针批） | **50-75%↓** |
| 单波回测时间 | 40 分钟 | 8 分钟（五槽并发） | **80%↓** |
| S4 评审效率 | 8 条/小时 | 64 条/小时（批量预筛） | **8×↑** |
| 数据集判死准确率 | 50% | 80%（WebDataScope 预筛） | **60%↑** |
| 整体配额利用率 | 12.5% | 40%（预估） | **3.2×↑** |

---

## 注意事项

1. **探针批模式**：仅适用于候选池 >2 条的情况
2. **GEM 校验**：默认不阻断，仅标注；加 `--gem-validate` 启用硬拦截
3. **五槽并发**：需确保平台账户有 ≥5 个并发槽位
4. **批量评审**：单次最多 20 个 alpha ID

---

## 更新日志

- 2026-08-30: 初始版本，基于 IND 区域战役经验沉淀
