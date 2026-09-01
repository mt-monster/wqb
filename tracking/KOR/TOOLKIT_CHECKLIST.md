# KOR 战役 toolkit 流程强制检查清单

**目的**：根治"手写表达式直接提交 create_multi_simulation"的路径依赖，确保每个 wave 都走完整 campaign-toolkit 流程。

**纪律**：**禁止手写表达式直接提交 create_multi_simulation**。必须走 build_wave.py + gate.py + pipeline.py。

---

## 强制检查清单（每次提交前必须确认）

### S0 白名单锁定
- [ ] `s0_whitelist` ledger 已锁定（白名单外不 generate、不 simulate）
- [ ] 当前数据集在白名单 tier1/tier2 内
- [ ] 当前数据集不在 excluded_dead 清单内

### S1 字段理解
- [ ] `s1_<dataset>_d<delay>` ledger 已写入（字段白名单 + 预处理决策 + ideas_md_path）
- [ ] ideas.md 文档已生成（`output_report/<region>_delay<delay>_<dataset>_ideas.md`）
- [ ] 字段白名单 ≤8 个（每条表达式尽量只用 1-2 个字段）

### S2 合规标记
- [ ] `s2_compliance_w<N>` ledger 已标记（makeSomeGem 或手写合规记录）
- [ ] 合规记录包含：ideas_md_path + field_whitelist + expression_count + generated_at

### S3 toolkit 流程
- [ ] `scan_fields.py --campaign-dir tracking/KOR --dataset <ds>` 已跑（生成 typed catalog）
- [ ] `upsert_expressions` 已写入 expressions 表（region/wave/dataset/expressions）
- [ ] `build_wave.py --campaign-dir tracking/KOR --from-db --dataset <ds> --wave <N>` 已跑（全历史去重 + 骨架配给 linear_mix≤0.5）
- [ ] `gate.py --campaign-dir tracking/KOR --dataset <ds> --from-db --wave <N>` 已跑（5 基础闸 + 多样性闸全过）
- [ ] `pipeline.py --campaign-dir tracking/KOR run --dataset <ds> --wave <N> --submit --review --write-ledger` 已跑（七槽填槽回测）

### S4 评审链
- [ ] `review_wave.py --campaign-dir tracking/KOR --multisim <id> --tag <N> --write-ledger` 已跑（walls 诊断 + 台账回写）
- [ ] AlphaTest 诊断（sharpe/2Y/fitness/turnover/CW/sub_sharpe）
- [ ] Mode B 想法层优先（换字段组合）、Mode A 参数层次之（调 decay/窗口/中性化）
- [ ] 本地 self/PPAC 快筛（check_self_correlation + check_correlation）
- [ ] 归因（收益来源/失败风险）
- [ ] 稳健性/反过拟合闸（brain-alpha-robustness skill）
- [ ] judge 判定（brain-alpha-judge skill，READY 后停下报告等用户确认）

### 硬闸检查
- [ ] sharpe ≥ 1.58
- [ ] 2Y sharpe ≥ 1.58（IS_LADDER_SHARPE）
- [ ] fitness ≥ 1.0
- [ ] prod_corr < 0.7（≥0.7 一律不提交、回 Mode B 换字段组合）
- [ ] self_corr < 0.7
- [ ] CW（CONCENTRATED_WEIGHT）PASS
- [ ] turnover 健康（<80%）

### 多样性评估
- [ ] 算子多样性（欠用算子注入：bucket/if_else/ts_corr/ts_kurtosis 等）
- [ ] 字段多样性（1-2 个字段，不频繁切换数据集）
- [ ] 骨架多样性（linear_mix≤0.5，single/group/event_gated 配给）
- [ ] 预处理多样性（vec_avg/ts_mean/ts_zscore/rank/group_neutralize 等）
- [ ] 收益来源多样性（分析师预期/内部人交易/基本面/价格量等）
- [ ] 失败风险评估（CW 集中/PROD 饱和/2Y 失效/信号稀释等）

---

## 标准 workflow 模板（每次新 wave 必须复制）

```bash
# Wave N 标准流程（不可跳过）
PY=$env:WQ_PY
TK=C:\Users\MENGTAO\.qoder-cn\skills\wq-brain-campaign-toolkit\scripts
CD=tracking/KOR

# 1. S3 前置：生成 typed catalog
& $PY $TK/scan_fields.py --campaign-dir $CD --dataset <ds>

# 2. S3 写入 expressions 表（MCP 工具）
# mcp__wqb-db__upsert_expressions(region="KOR", wave="<N>", dataset="<ds>", expressions=[...])

# 3. S3 选波+预检
& $PY $TK/build_wave.py --campaign-dir $CD --from-db --dataset <ds> --wave <N>
& $PY $TK/gate.py --campaign-dir $CD --dataset <ds> --from-db --wave <N>

# 4. S3 回测（七槽填槽）
& $PY $TK/pipeline.py --campaign-dir $CD run --dataset <ds> --wave <N> --submit --review --write-ledger

# 5. S4 评审
& $PY $TK/review_wave.py --campaign-dir $CD --multisim <id> --tag <N> --write-ledger
```

---

## 历史教训（不可重蹈覆辙）

**Wave 16（other553）**：手写表达式使用 `ts_event_mean` 算子，但该算子在 BRAIN 平台不存在（102 个算子中无 ts_event_* 系列），8/8 ERROR 浪费配额。**这正是 gate.py 5 闸预检能拦截的错误**（闸 1 语法检查 + 闸 4 不可访问算子检查），如果走了 toolkit 流程不会浪费 8 条配额。

**Wave 8-15（insider_feats/fundamental89 等）**：手写表达式直接提交 create_multi_simulation，跳过 build_wave.py 全历史去重 + 骨架配给 + gate.py 5 闸预检，导致：
- 可能重复历史表达式（浪费配额）
- 可能触发 CW 墙（骨架配给强制多样性直击 CW 墙）
- 可能提交语法错误/字段白名单外/VECTOR 未包裹的表达式

---

## 强化措施

1. **每次提交前必须逐项确认检查清单**（不可跳过任何一项）
2. **S2-COMPLIANCE 硬闸不可绕过**（--force 需在台账记录原因）
3. **禁止手写表达式直接提交 create_multi_simulation**（必须走 build_wave.py + gate.py + pipeline.py）
4. **上下文压缩后必须重新读取本检查清单**（防止 toolkit 使用细节丢失）
5. **每波结束后必须跑 review_wave.py + judge 判定**（READY 后停下报告等用户确认）

---

**最后更新**：2026-09-01
**触发原因**：Wave 16 ts_event_mean 算子不存在浪费 8 条配额 + 用户多次批评"总是跳过 toolkit 流程"
