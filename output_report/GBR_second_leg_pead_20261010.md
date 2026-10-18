# GBR 第二条腿挖掘结题（2026-10-10 下午）：PEAD 腿 IS+prod 全过，**卡在 sub-universe**

> 承接已提交的 `3qVP6pNO`（techindi × CROWDING，OTHER 塔）。
> 本轮目标：按用户指令继续挖 GBR 非点亮 category 的可提交 alpha，拿到候选后做极致优化。

---

## 一、本轮探测的 4 个处女池（各 1 波，全部过发批七闸）

| 池 | aCnt | 内容（读 description 判定） | 最强 | 判决 |
|---|---:|---|---:|---|
| socialmedia5 / socialmedia12 | **0** | 社媒情绪分 / 相对声量（SOCIALMEDIA 塔 0/16） | 0.32 | ✗ 弱 |
| earnings_sent_matrix | **1** | 盘中财报电话会语气概率 | 0.46 | ✗ 结构性：TO 0.38 超上限 + 全 sub_LOW |
| institutions25 | 42 | 空头拥挤度 / 空头余额（INSTITUTIONS 塔 0/16） | **0.99（反向）** | ✗ 2Y −0.85 反向 + TO 0.045 令 F 天花板仅 0.35 |
| **earnings6（PEAD）** | 114 | **actual EPS vs estimated EPS**（EARNINGS 塔 0/16） | **S1.68/F1.42/2Y1.64** | ★ 见下 |

## 二、earnings6 PEAD 的突破链（10 波 / 80 条）

```
探针     divide(actual_eps, |estimated_eps|+1) 幅度           S1.17 / F0.80 / 2Y1.91
   ↓ 双窗 add(ts_mean(1), ts_mean(120)) + 原始信号 group_neutralize   S1.25 / F0.90 / 2Y2.20
   ↓ ts_delta(意外比, 252)  ← 盈利意外的同比变化                    S1.38 / F1.10 ✅ F 首破 1.0
   ↓ 窗口细扫 180→230 + tvr 0.13/0.15/0.16 微调
   ↓ ★ ZYAzdx1n（窗 225 / tvr 0.14）
```

| alpha | S | F | 2Y | margin | TO | **prod** | self |
|---|---:|---:|---:|---:|---:|---:|---:|
| **ZYAzdx1n** | **1.68** ✅ | **1.42** ✅ | **1.64** ✅ | 16.6bp | 0.108 | **0.6654** ✅ | 0.040 |

## 三、★ 但被平台闸门否决：`submit_verdict ZYAzdx1n` → **LOW_SUB_UNIVERSE_SHARPE FAIL（0.41 < 限 0.80）**

| 变体 | S | sub-universe | 结论 |
|---|---:|---:|---|
| 全部强变体（S 1.5–1.68） | 1.5–1.68 | **0.41 – 0.51** | ❌ 全不达标 |
| 唯一 sub≥0.8 的变体 | 0.16 | 1.66 | 无强度 |

**修复尝试全部判负**：ts_zscore / ts_rank / ts_quantile 自身历史标准化（S→1.14–1.22）、回填 750/1000 扩覆盖、紧裁剪 0.1 —— **覆盖率驱动的闸门失败，参数调不出来**。

### ★ 新增第 8 类封死形态：**H「sub-universe 塌」**
> IS 三闸全过 + prod 过线，但 `LOW_SUB_UNIVERSE_SHARPE` FAIL。
> **根因**：字段只覆盖 universe 的一个子集（EPS 类字段只有财报季发布过的股票）⇒ 全宇宙有效、子宇宙失效。
> **选池判据新增（关键）**：**字段是否对全 universe 每只股票都有值** —— techindi 的分位桶模型对每只股票都有值（cov=0 但全覆盖）⇒ sub_OK；earnings6 的 EPS 字段是子集 ⇒ sub 塌。

## 四、本轮沉淀的流程教训

1. **元数告警必须当阻断**：`days_from_last_change(x, 120)` 平台签名只接 1 参 ⇒ 整批 8 条全废（平台 ERROR 级联）。已在派发脚本里加 `grep -q "ARITY" && 阻断`。
2. **空头类信号的 GBR 方向与文献相反**：经典「高空头余额 → 低收益」在 GBR 是**反向**（做空高空头拥挤 S −0.74~−0.99），但 2Y −0.85 说明效应近两年翻转。
3. **S ↔ 2Y 跷跷板**在 PEAD 上同样存在（窗 220: S1.51/2Y1.67 ↔ 窗 230: S1.56/2Y1.47），只能靠微调取折中。

## 五、当前记分牌（目标 10 颗）

```
✅ 可提交 1 颗：3qVP6pNO（techindi × CROWDING，已提交 ACTIVE，OTHER 塔点亮）
⛔ 1 颗 IS+prod 全过但 sub-universe 卡死：ZYAzdx1n（earnings6 PEAD）
✗ 本轮另 3 池判弱/结构性死
```

**建议**：下一条腿优先选**「对全 universe 有值」的字段池**（按新判据预筛），
例如 pv20 的 ADV 类、other566 技术指标、pattern_scores —— 避免再撞覆盖率型 sub-universe 塌。
