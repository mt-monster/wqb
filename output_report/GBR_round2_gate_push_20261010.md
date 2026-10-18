# GBR 第二轮破闸战报（2026-10-10 下午）：四条腿全部推到闸门边界

> 指令：不破闸不允许停下来；遇难题查论坛+外部论文；算子穷举。
> 本轮共 **18 波 / 140+ 条**，全部过发批七闸。

---

## 一、四条腿的破闸结果（每条都推进到自己的闸门边界）

| 腿 | 最高 S | F | 2Y | prod | sub-universe | **卡在哪个闸** |
|---|---:|---:|---:|---:|---:|---|
| **earnings6 PEAD** | **1.68** ✅ | **1.42** ✅ | **1.64** ✅ | **0.6654** ✅ | 0.41 ❌ | **LOW_SUB_UNIVERSE_SHARPE**（限 0.80） |
| dl_riskfree_returns（industry 轴） | 1.38 | 0.62 | −0.28 | — | 1.0+ ✅ | **2Y 全塌**（短期限信号无长期一致性） |
| other566（AMA 反向） | 1.24 | 0.71 | 1.49 | — | 1.0+ ✅ | **F 不足 0.29 + S↔2Y 跷跷板** |
| pattern_scores（反向） | 0.71 | 0.27 | 1.29 | — | OK ✅ | 强度天花板 |

## 二、earnings6 PEAD：唯一「三闸 + prod 全过」的腿，死于 sub-universe

### 突破链（10 波 / 80 条）
```
探针  divide(actual_eps, |estimated_eps|+1)                    S1.17/F0.80/2Y1.91
 → 双窗 add(ts_mean(1),ts_mean(120)) + 原始信号 group_neutralize  S1.25/F0.90/2Y2.20
 → ts_delta(意外比,252)  ← 盈利意外的同比变化                    S1.38/F1.10 ← F 首破 1.0
 → 窗 180→230 细扫 × tvr 0.13-0.16
 → ★ ZYAzdx1n（窗225/tvr0.14）  S1.68/F1.42/2Y1.64/margin16.6bp，prod 0.6654
```

### sub-universe 修复：论坛 + 外部文献全试过，全判负
| 方法 | 来源 | 结果 |
|---|---|---|
| `hump(..., hump=0.01)` 三档 | 论坛《浅谈用 hump 解决 Sub-universe Sharpe》（50 赞） | sub 仍 0.41 ❌ |
| `ts_decay_linear` 平滑 | 同帖推荐 | sub 0.44，仍 ❌ |
| 紧裁剪 0.05 / 0.1 | 外部 winsorize 文献 | S 反降 ❌ |
| ts_zscore 自身标准化 252/504 | 外部 z-score 稳健化 | S 反降到 1.14-1.22 ❌ |
| 回填 750 / 1000 扩覆盖 | 论坛 trade_when 帖（覆盖率根因） | 无改善 ❌ |

**根因（论坛两篇 + trade_when 帖一致）**：EPS 类字段只覆盖「有财报的子集」⇒ 全宇宙有效、子宇宙失效。
**这是第 8 类封死形态 H「sub-universe 塌」** —— 覆盖率驱动，参数/算子层无解。

## 三、★ 本轮三个可复用技术发现

1. **选池新判据（最重要）**：**字段是否对全 universe 每只股票都有值**。
   - techindi 分位桶模型：cov=0 但每只股票有值 ⇒ sub_OK ✅（已提交腿）
   - earnings6 EPS：只有发过财报的股票有值 ⇒ sub 塌 ❌
   - other566 / dl_riskfree 技术指标：全覆盖 ⇒ sub_OK ✅
2. **分组轴是 sub 的次要因子**：dl_riskfree 从 sector 换 **industry 轴**后 sub 从 LOW → 全部 OK（1.0+）。画像里记录的 S1.41 最优腿正是 industry 轴 + tvr 0.35-0.55，我先前全用 sector 所以复现不出来。
3. **S↔2Y 跷跷板在所有腿上普遍存在**（AMA、PEAD、pattern 都是），只能在中间窗取折中。

## 四、算子穷举的实战记录（本日两次元数事故，均已修）

| 事故 | 症状 | 修法 |
|---|---|---|
| `days_from_last_change(x, 120)` | 平台报 "Invalid number of inputs : 2, should be exactly 1" ⇒ **整批 8 条全废** | 单参签名 |
| `hump(x, 0.01)` | 同类（须写 `hump=0.01` 命名参数） | 命名参数 |

⇒ **元数告警必须当阻断**（已在派发脚本落地 `grep -q "ARITY" && 阻断`），这是「一条语法错毁全批」铁律的自动化。

## 五、下一步的唯一可行方向

要拿到第 2 颗可提交 alpha，**必须找「对全 universe 有值 + 机制不在池子里」的池**，且避开短期限信号（2Y 塌）：
- ✅ 候选：`pv20` 的 ADV 类（成交量，全覆盖、PV 类但非反转）、`other566` 里覆盖率更高的波段字段、`risk60`（借券费率，aCnt=6，全覆盖）
- ❌ 避开：`earnings6`（覆盖率）、`dl_riskfree`（2Y）、`institutions25`（2Y 反向）
