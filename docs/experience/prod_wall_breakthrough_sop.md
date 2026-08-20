# PROD 墙突破标准化 SOP

> 来源: 2026-08-18 EUR 战役复盘 (Wj71Q12o 破 prod 墙成功 ACTIVE)
> 核心认知: 蓝海 userCount 低 ≠ PROD 低; 破墙正解 = 信号层稀释复合

## 1. 问题定义

**PROD_CORRELATION 墙**: alpha 的 IS 指标全部达标, 但 prod_corr > 0.7, 无法提交。

**跨区域共性**:
- USA: option8/option40 IV 族 0.83-0.91, si3 0.957
- KOR: value/quality 种子 0.759-0.7824, dl_riskfree 20+ 冠军 0.82-0.92
- IND: anl39 核心 self_corr 0.78 撞车
- EUR: FCF 镜像 prod 0.9013

## 2. 破墙标准化路径 (EUR 实证)

### Step 1: 确认 IS 强信号
- IS sharpe ≥ 1.58, fitness ≥ 1.0, two_year_sharpe ≥ 1.58
- 若 IS 不达标, 先优化 IS, 再考虑破墙

### Step 2: 找异质分量 (0 配额)
```
compute_mutual_correlation 找 |corr| < 0.3 的异质分量
- 分量不需要自身 IS 强
- 只需与主信号低相关
- 优先选不同数据集/不同信号族
```

### Step 3: 梯度稀释复合
```
结构: rank(ts_rank(主信号, N1)) * w1 + rank(ts_rank(异质分量, N2)) * w2
梯度: w1/w2 = 0.80/0.20 → 0.60/0.40 → 0.40/0.60
每档提交回测验证
```

### Step 4: 每档 check_correlation 验证
```
check_correlation(alpha_id) 验证 prod_corr 变化
- 若 prod_corr 单调下降 → 继续加深稀释
- 若 prod_corr 不降反升 → 停止, 换异质分量
```

### Step 5: 定位甜点
```
目标: prod_corr < 0.7 且 IS 达标
- 分散化红利: IS 不降反升时继续加深
- 若 IS 下降 > 10% → 回退一档
```

## 3. EUR 实证案例 (Wj71Q12o)

| 档位 | 主信号权重 | 异质分量权重 | IS sharpe | prod_corr | 状态 |
|---|---|---|---|---|---|
| 原始 | 1.0 | 0.0 | 1.79 | 0.9013 | 撞墙 |
| 档1 | 0.8 | 0.2 | 1.81 | 0.85 | 改善 |
| 档2 | 0.6 | 0.4 | 1.82 | 0.78 | 改善 |
| 档3 | 0.4 | 0.6 | 1.81 | 0.6847 | **破墙** |

**关键发现**:
- 稀释分量 (pattern gap 镜像) 自身 IS 弱 (sh ~0.5)
- 但与主信号 (FCF 镜像) corr < 0.3
- 分散化红利使 IS 不降反升 (1.79 → 1.81)

## 4. 常见误区

| 误区 | 正解 |
|---|---|
| 蓝海 userCount 低 = PROD 低 | userCount 低 ≠ PROD 低, 需实测 |
| universe 杠杆可破墙 | universe 杠杆不可用, 需信号层稀释 |
| 稀释分量需自身 IS 强 | 稀释分量只需与主信号低相关 |
| 一次稀释到位 | 梯度稀释, 每档验证 |

## 5. 检查清单

- [ ] IS 强信号确认 (sh ≥ 1.58, fit ≥ 1.0, 2y ≥ 1.58)
- [ ] compute_mutual_correlation 找 |corr| < 0.3 异质分量
- [ ] 梯度稀释复合 (0.80/0.20 → 0.40/0.60)
- [ ] 每档 check_correlation 验证
- [ ] 定位 prod < 0.7 且 IS 达标甜点
- [ ] 记录破墙路径到台账

## 6. 相关工具

- `compute_mutual_correlation`: 找异质分量 (0 配额)
- `check_correlation`: 验证 prod_corr 变化
- `check_self_correlation`: 验证 self_corr 变化

## 7. 参考文档

- [2026-08-18 EUR 战役复盘](2026-08-18-eur-campaign-retro.md)
- [project_experience_master.md](project_experience_master.md) §提交硬闸门体系
- [kor_factor_mining_workflow.md](kor_factor_mining_workflow.md) §8.5 KOR PROD 墙实证
