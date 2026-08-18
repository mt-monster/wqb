# 低优先级探针机制（Low-Priority Probe Mechanism）

## 目的

当某数据集/主题在区域战役中**多次实证弱**（≥2 次 RED），但**结构重构未验证**时，自动降级为低优先级探针，而非直接跳过。保留翻案口子，避免过早判死。

## 触发条件

| 条件 | 说明 |
|------|------|
| ≥2 次 RED | 同一主题（如 credit_risk、news_sentiment）在多个数据集/波次判死 |
| 结构重构未验证 | 未测试过滞后、中性化、交互等变体 |
| 非结构性死结 | 非 PROD 墙/rnf 方向矛盾等不可修复问题 |

## 结构重构三轨

| 轨道 | 模板 | 假设 |
|------|------|------|
| **滞后** | `ts_delay(field, 5/10)` | 信息传导延迟，机构定价效率高但反应链条长 |
| **中性化** | `group_neut(field, country/industry)` | 剥离国家/行业风险，信号被宏观因子淹没 |
| **交互** | `multiply(field, ts_delta(close, 20))` | 条件信号，需价格动量配合 |
| **波动率调整** | `divide(field, ts_std_dev(returns, 20))` | 低波动异象交互 |

## 使用方法

```bash
# 基础用法
python tracking/EUR/scripts/low_priority_probe.py \
    --campaign-dir tracking/EUR \
    --dataset model36 \
    --theme credit_risk \
    --prior-reds wave1,wave6,wave8

# 自定义轨道
python tracking/EUR/scripts/low_priority_probe.py \
    --campaign-dir tracking/EUR \
    --dataset model36 \
    --theme credit_risk \
    --prior-reds wave1,wave6,wave8 \
    --tracks lag_5d,country_neut,momentum_60d
```

## 输出

| 文件 | 说明 |
|------|------|
| `candidates/<region>_wave<N>_<tag>_items.json` | 16 条探针表达式 |
| `scripts/run_wave<N>_<tag>.py` | 五槽填槽 runner |
| 台账 `wave<N>_<tag>_verdict` | `LOW_PRIORITY_PROBE` 状态 |

## 判死标准

探针跑完后，若满足以下条件则正式判死：

```
top sharpe < 1.0 且 rn_fitness < 0.3
```

判死后更新台账：
```json
{
  "verdict": "RED_STRUCTURAL_VERIFIED",
  "note": "信用风险在 EUR 经结构重构验证仍弱：滞后/中性化/交互三轨 16 探针全崩"
}
```

## 与直接跳过的区别

| 策略 | 适用场景 | 风险 |
|------|---------|------|
| **直接跳过** | 结构性死结（PROD 墙、rnf 方向矛盾） | 可能错过区域适应性变体 |
| **低优先级探针** | 多次弱但结构重构未验证 | 消耗 16 条配额，但保留翻案口子 |

## 示例：model36 信用风险

```bash
python tracking/EUR/scripts/low_priority_probe.py \
    --campaign-dir tracking/EUR \
    --dataset model36 \
    --theme credit_risk \
    --prior-reds wave1,wave6,wave8
```

生成：
- `eur_wave20_creditlow_items.json`（16 条）
- `run_wave20_creditlow.py`
- 台账 `wave20_creditlow_verdict`

## 集成到战役流程

```
S0 健康检查 → 发现某主题 ≥2 次 RED
       ↓
S1 判断：结构性死结？→ 是 → 跳过
       ↓ 否
S2 低优先级探针生成（lag/neut/interact 三轨）
       ↓
S3 五槽填槽回测（低优先级槽位）
       ↓
S4 评审：top sharpe > 1.0？→ 是 → 升级为主攻
       ↓ 否
S5 判死：RED_STRUCTURAL_VERIFIED
```
