# USA SuperAlpha 可行性实测报告（2026-09-14）

## 结论

**USA 当前无法组出可提交的 SuperAlpha。** 组件数前置（≥10 ACTIVE REGULAR）已满足，但现有 35 颗 ACTIVE REGULAR 存量池在双闸（SELF<0.7 且 PROD<0.7）上结构性无解，实测定点均为 0.78–0.87，远超阈值。**不建议提交**——会白白消耗每日 1 颗的 SUPER 配额。

## 一、前置条件核对

| 检查项 | 要求 | USA 实测 | 结论 |
|---|---|---|---|
| 区域 ACTIVE REGULAR ≥ 10 | ≥10 | **35** | ✅ 满足 |
| 宇宙合法性 | TOP3000/1000/2000/500 | TOP400 被平台 400 拒 | 改用 TOP3000 |
| SUPER 配额 | 1/ET 日 | 今日未用 | 留存，不浪费 |

> 计数陷阱：无过滤 `GET /users/self/alphas` 硬卡前 1000 颗（offset≥1000 → HTTP 400），首次误报 USA=1。改用 `status=ACTIVE` + `type=SUPER` 翻页后得真实值 35 / 52。

## 二、组套配置与双闸实测

工具：`tools/super_build.py`（selection 评分 + combo `1-maxCorr` + combo_power 杠杆，SUBINDUSTRY 中性化——USA 文档最优档）。

| 配置 | alpha_id | IS sharpe / fitness | turnover | **SELF** | **PROD** | 判定 |
|---|---|---|---|---|---|---|
| SUBINDUSTRY, combo5, limit10, self_gate0.7 | `6Xr6k5JO` | 2.49 / 2.56 | 0.140 | **0.8652** | **0.8655** | ❌ BLOCKED |
| SUBINDUSTRY, combo5, limit20, self_gate0.6 | `pwP2q633` | 3.21 / 3.65 | 0.113 | **0.7862** | **0.8573** | ❌ BLOCKED |

## 三、关键发现

1. **双闸此消彼长，无共同可行域**（与 09-14 前 MEMORY 7 档实证一致，本次 live 双证）：
   - 成分 10 → 20，SELF 由 0.865 降至 0.786（成分越多 SELF 越低，符合规律）；
   - 但 **PROD 卡死在 ~0.86 不动**——存量池与生产池高度同质，无论怎么选组件都压不下去。
2. **PROD 是硬瓶颈**：即便取池内 prod 最低的 10–20 颗组件，合成后 PROD 仍 0.86。这说明 USA 现有 35 颗 ACTIVE 与生产信号空间严重重叠。
3. **SELF 下限 ~0.79**：combo_power 已拉满到 5（最大压制），即使 20 组件也只到 0.786，仍超 0.7。

## 四、下一步出路

要在 USA 组出可过双闸的 SA，**唯一路径是先扩入"低 prod 相关新血"**：
- 挖掘与现有 USA 生产池低相关（PROD<0.6 量级）的新质信号，且彼此结构多样（压低 SELF）；
- 入池后再跑 `super_build.py select` 实测，确认 SELF<0.7 且与 PROD 同向压低，方有可行域。

> 纪律：submit 前必用 `probe` 子命令做零成本双闸验证；同步 403 = 零成本，勿在已确认无解的存量池上消耗 SUPER 配额。
