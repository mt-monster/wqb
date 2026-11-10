# other335 · KOR / TOP600 / D1 字段画像

> 类型 MATRIX · **10 个字段** · 覆盖率 **0.5728 / 0.6073** · 本地 `n_tests=0`（全 UNTESTED）
> 金字塔 category = **other**（multiplier 1.6，**未点亮塔**）
> 采集：`get_field_catalog(region=KOR, dataset=other335)`，2026-10-30
> ⚠ 约束 5：OTHER 类禁止与 PV / MODEL / OTHER 组腿 ⇒ 只能做 **ATOM 单集**

## 0. 全字段清单（10/10，αC 降序）

| # | 字段 | αC | users | cov | desc |
|---|---|---|---|---|---|
| 1 | `oth335_combined_all_region_mind` | **298** | 177 | **.6073** | **Final composite Wolfe MIND dividend/income score** (daily, PIT) |
| 2 | `oth335_combined_all_region_hedge` | 204 | 128 | **.6073** | Score from the **hedge model** component |
| 3 | `oth335_combined_all_region_linear` | 125 | 81 | **.6073** | Score from the **linear model** component |
| 4 | `oth335_combined_all_region_shield` | 97 | 67 | **.6073** | Score from the **SHIELD (defensive)** model |
| 5 | `oth335_combined_all_region_mktcap` | 45 | 27 | .6073 | Market cap (USD) |
| 6 | `oth335_hc_combined_all_region_linear` | 59 | 35 | **.5728** | Linear model score (PIT) |
| 7 | `oth335_hc_combined_all_region_hedge` | 49 | 27 | .5728 | Hedge model score (PIT) |
| 8 | `oth335_hc_combined_all_region_mind` | 44 | 34 | .5728 | Final composite MIND (PIT) |
| 9 | `oth335_hc_combined_all_region_shield` | 39 | 28 | .5728 | Defensive SHIELD (PIT) |
| 10 | `oth335_hc_combined_all_region_mktcap` | 26 | 14 | .5728 | Market cap (USD) |

**读数**：**两套镜像**（无 `hc_` 前缀 cov .6073 / 带 `hc_` 前缀 cov .5728），**同一批四个模型分**：
`mind`（股息收入复合）/ `hedge`（对冲）/ `linear`（线性）/ `shield`（防御）。
`hc_` 版覆盖**低 3.45pp** 且 αC 更低（44 vs 298）⇒ **`hc_` 版是同一信息的劣化副本，不进候选**。

**⚠ 覆盖红线**：cov .6073 意味着 **39% 的 TOP600 股票在任一时点无值**。
本地政策线 cov<0.60 ⇒ `UNUSABLE`；.6073 只是**擦线通过**，`hc_` 的 .5728 **已在线下 ⇒ 直接排除**。
高缺失 + 模型评分（非原生财务值）⇒ **`ts_backfill` 无法真正修复**（缺的是资产覆盖，不是日历缺口），
预期会撞 **CONCENTRATED_WEIGHT** 或**子宇宙夏普**。

## 1. 名 vs description 差异

| 名 | 实际 | 按名分类的错误 |
|---|---|---|
| `mind` | **Wolfe MIND 股息/收入模型**复合分，不是「心智/情绪」 | `mind` 极易被读成 sentiment 类，实际是 **dividend/income（价值+质量）** 族 |
| `hedge` | 模型的一个**分量**，不是「对冲后的版本」 | 会被误当「已对冲/中性化」的成品，从而跳过中性化 |
| `linear` | 线性模型分量 | 会被当「线性变换」算子说明 |
| `shield` | **防御型（defensive）模型**分量 | 会被当风控/保护字段 |
| `combined_all_region` | **全区域**合成（非 KOR 专用） | 会被当 KOR 本地模型；实际是跨区统一分，KOR 覆盖因此更差 |
| `hc_` 前缀 | 另一路入录（覆盖更低） | 会与主版算成两条腿 = **伪多样性** |

## 2. 五问

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 存量/流量 | **存量评分**（daily PIT），非变化率 |
| 2 相对性 | 水平/排序 | **排序**；且因**跨区合成**，绝对量级更不能跨市场比 ⇒ 必须 `group_rank(·, sector)` |
| 3 被定价的是谁 | 广度/强度 | **强度**：股息/收入吸引力 + 防御性 |
| 4 有无博弈 | 拥挤/规模 | **中等拥挤**（`mind` αC 298，是 other545 的 27 倍）；评分模型内可能含规模控制 |
| 5 事件性 | 稀疏 | **否**，但**覆盖稀疏**（39% 无值）⇒ 与「事件稀疏」不同，用 `ts_backfill` 而非 `trade_when` |

## 3. 预处理决策

| 体征 | 决策 |
|---|---|
| cov .6073 | `ts_backfill(F, 10)` 前置；**并预期 CW 风险**（按 `concentrated_weight_is_data_quality_not_params_v1`：先查覆盖 → 再查类型 → 再查窗口 → 才 `ts_backfill`） |
| `hc_` 版 cov .5728 | ⛔ **排除**（线下 + 劣化副本） |
| `mktcap` | **只作规模轴** |
| 四个分量同族 | **一条腿只出 1 颗**：`mind`（复合，αC 最高）为主；`shield` / `linear` / `hedge` 作**分量对照**，非同波全上 |
| 跨区合成 | 必须 `group_rank(·, sector)`（不用 `zscore`） |
| 十年数据 | 覆盖是**横截面**口径；逐十年份未验 ⇒ 先读 `get_alpha_yearly_stats` longCount |

## 4. 机制（A-2）

**谁在被定价**：韩国市场中**追逐股息/收入（yield-seeking）的散户与养老金资金**，
以及**防御性配置需求**（`shield` 分量）。

**为什么会被错**：韩股长期「低股息、高成长偏好」，股息/收入类标的被系统性低估；
养老金与保险资金的负债端需求使其在特定 regime（利率下行、风险厌恶上升）被重新定价，
而市场对该 regime 切换的定价滞后。

**错了多久修复**：**一季至数季**（股息/收入是慢变量；对应窗口 66–252d）。

**预期方向**：高 MIND 分（高股息/高质量/防御）⇒ 后续**高**收益 ⇒ 正向 `group_rank`。

**Boundary Conditions**：⚠ **覆盖仅 61%**，是最大风险——缺失段可能恰是模型不覆盖的小盘（最肥的那段）；
跨区合成口径与 KOR 本地制度（如韩国分红季节性）不匹配；`shield` 在牛市可能反向。

## 5. 拟用取式（**wave 217 候选**，非本波，优先级低于 545）

| # | 表达式 | 意图 |
|---|---|---|
| 1 | `group_rank(ts_backfill(oth335_combined_all_region_mind, 10), sector)` | 复合 MIND（正向） |
| 2 | `reverse(<同>)` | 铁律 B 对照 |
| 3 | `group_rank(ts_mean(ts_backfill(oth335_combined_all_region_mind, 10), 66), sector)` | 慢变量长窗（股息是慢变量） |
| 4 | `group_rank(ts_backfill(oth335_combined_all_region_shield, 10), sector)` | 防御分量（regime 检验） |

## 6. 实测记录

### D3 波收割（2026-11-08，10/10 COMPLETE，RAM/d4/trunc0.08）

| 臂 | alpha | S | F | 2Y | raF |
|---|---|---:|---:|---:|---:|
| **mind zscore252** | leAPxwGn | **1.14** | 0.91 | 1.19 | 3 |
| mind power2 | pwde0b3q | 1.08 | 0.88 | 1.39 | 3 |
| mind 水平 | GrW5VjXx | 1.00 | 0.79 | 1.49 | 3 |
| shield 水平 | RREwXxzn | 0.93 | 0.71 | 1.62 | 2 |
| mind 反向 | ZYQvZVdx | −1.13 | −0.95 | −1.74 | 5 |

**判定：弱但活**（天花板 S≈1.14，缺口 0.44；正向确证，反向 −1.13）。cov.6073 未触发 CW（longCount 实测达标）。
与 other532(S1.12) 同级 ⇒ **中性化 11 档未扫**（仅 RAM），列入近线补扫队列。十年覆盖待 get_alpha_yearly_stats 复核。
