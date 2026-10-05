# SA 杠杆与参数-指标对照（决策表 + 证据）

> 主 SOP 见 [`../SKILL.md`](../SKILL.md)。本文把旧版按时间追加的「杠杆」小节改写成**一张决策表 + 证据表**：症状 → 已实证有效 → 已实证无效 → **止损线**。
> 旧版同时并存 5 个「决定性杠杆」（SUBINDUSTRY / decay / 宽篮 / 池新鲜度 / 逐区扫描），靠「优先于上表阅读」这种**阅读顺序补丁**代替改写——这里以决策表统一。
> 所有数字都带（区域，日期，口径）。**区域结论不可迁移**：「在 USA / KOR 观察到」不等于「恒成立」。

## 0. 双闸决策表（先看症状）

| 症状 | 已实证有效的杠杆（区域，日期） | 已实证无效 | 止损线 |
|---|---|---|---|
| **SELF 高**（0.7–0.93） | ① 宽篮（`selectionLimit` ≥ 有效池；USA 12 结构，2026-09-11：V8 / V9 / V11 / V12 SELF 全过）② **窄篮**下 decay↑（KOR 2026-09-11：12 → 300，SELF 0.816 → 过闸）③ `--combo-power 3 / 5`（IND：0.7581 → 0.7508，代码注释口径）④ **错开存量 SA 的 (neutralization, decay)**（KOR 案例 4） | 调 `selectionLimit` 超过有效池（USA 1000 与 50 逐位相同：sh 3.06 / fit 3.62 / to 0.0783）；重提同一 (nu, decay) 组合 | 与存量 SA 近克隆（max_corr ≈ 0.90–0.92 且 top 命中已 ACTIVE SA）→ 换成分 / 换组合，不再磨同一组合 |
| **PROD 高**（≥ 0.7） | ① 逐区扫描中性化（USA KPGvRMg1：MARKET 地板 0.7169 → SUBINDUSTRY 0.6944，2026-08）② **成分池新鲜度**：注入 prod < 0.55 的新血 REGULAR，把池的 prod 分布整体左移（USA / KOR 的统一出路） | decay（PROD 地板由成分池决定；**宽篮**下 decay↑ 反而 PROD↑：3 → 0.85、10 → 0.87、60 → 0.91）；换评分为 `(1-self)*(1-prod)`（decay 250 时 PROD 0.7832）；对**单颗 REGULAR** 用 SUBINDUSTRY（KOR 种子：prod 几乎不变、sharpe / fitness 反而跌破 LOW 闸——它只在 SA 组合层面有效） | **PROD 饱和**（USA 0.85–0.91、KOR 0.78）且没有低 prod 新血 → **停止调参，回 RA 挖新血**（SKILL「组件不足」交接） |
| **组件不足**（`At least 10 component alphas`） | 放宽 gate：`--self-gate` 0.65 → 0.70 → 0.85（GLB 案例：0.65 时三档中性化全撞，有一颗 self_corr ∈ [0.65, 0.70)）；`--turnover-max` 0.5 → 0.6；`--prod-ceiling` 0.7 → 1.0 | 直接加大 `selectionLimit` | 放宽到 0.85 仍不足 → 回 RA 补缺口 N 颗 |
| **子宇宙不过**（`LOW_SUB_UNIVERSE_SHARPE`） | USA：SUBINDUSTRY 才过（STATISTICAL 必挂） | decay 300 虽再降 SELF 却摧毁子宇宙（0.47）；USA 同 nu 同评分会撞克隆 KPGvRMg1 → SELF 0.93，decay 60 只降到 0.83 | USA 的 decay 窗口**双向挤压、无共同可行点** → 换成分池，不再扫 decay |
| **turnover 逼近下限**（SUPER `LOW_TURNOVER` 0.02） | 降 decay（KOR 曲线：decay 300 时 turnover 0.026，已贴近） | — | decay 拉到 200–300 试探 SELF 时同时盯 turnover |
| **IND 独有闸**（`LOW_ROBUST_UNIVERSE_SHARPE`） | 中性化选 STATISTICAL（IND 极差 0.199：STATISTICAL 最优、SUBINDUSTRY 最差） | 照搬 USA 的 SUBINDUSTRY | — |

## 1. 中性化：需扫描的档位 + 已知最优（区域，日期）

**没有可以跨区照搬的缺省。** 已知最优只是「上一次在该区扫描的结果」，新区 / 新池必须重扫。

| 区域 | 已知最优 | 证据 |
|---|---|---|
| USA | SUBINDUSTRY | KPGvRMg1：MARKET 地板 0.7169 → SUBINDUSTRY 0.6944（2026-08）；STATISTICAL 必挂 `LOW_SUB_UNIVERSE_SHARPE`（2026-09-11） |
| GLB | SUBINDUSTRY | A1NQ57NW（2026-09-24） |
| KOR | **STATISTICAL**（最强一颗即 STATISTICAL） | 与 USA / GLB 相反；案例 4 的 STATISTICAL/dec5、dec30 都撞存量同构，SUBINDUSTRY/dec10 才过 SELF |
| IND | STATISTICAL | 2026-09-11：极差 0.199，SUBINDUSTRY 最差；一轮各扫一遍 |

## 2. 篮宽 × decay（USA 12 结构，2026-09-11）——「decay 的作用方向随篮宽而变」

| 篮 | SELF | PROD | decay 效应 |
|---|---|---|---|
| **窄篮**（limit 10，远小于有效池） | **高**（USA 0.83–0.93） | 低（多在 SELF 失败后未揭露） | decay↑ → **SELF↓** |
| **宽篮**（limit ≥ 有效池，如 1000） | **过闸 ✅** | **高**（USA 0.85–0.91） | decay↑ → **PROD↑**（3 → 0.85、10 → 0.87、60 → 0.91） |

- **宽篮是解 SELF 的杠杆**：宽混合信号不等于 book 中任何单颗 alpha。「V8 / V9 / V11 / V12」是 USA 那轮实验里的 12 个结构变体代号（selection 评分 / 门的不同组合），**没有其它定义**；复现请用当前 `super_build.py select` 的参数组合，不要找这些代号。
- **修正旧规律**：早期「decay 越大双降」来自 top-10 **窄篮**实验（2026-09-10 USA 7 档），不可迁移到宽篮。正确记法：**在 USA / KOR 的实验里，decay 对 SELF 是负向杠杆；对 PROD 的方向取决于篮宽（窄篮↓ / 宽篮↑）**——「恒」字不成立（两个区域推不出全局）。

## 3. KOR decay 曲线（2026-09-11，窄篮口径）

同池同配方（仅改 decay；selection 评分 `(1.0 - self_correlation)`，nu = SECTOR）：

| decay | SELF | sharpe | fitness | turnover |
|---|---|---|---|---|
| 12 | 0.8160 ❌ | 3.13 | 4.07 | 0.086 |
| 40 | 0.7740 ❌ | 2.73 | 3.39 | 0.048 |
| 100 | 0.7294 ❌ | 2.38 | 2.82 | 0.033 |
| 200 | 0.7021 ❌ | 2.16 | 2.49 | 0.027 |
| **300** | **过闸 ✅** | 2.07 | 2.36 | 0.026 |

- decay 单调压 SELF（平滑信号 → 与 book 中高频成分去相关），指标同步下降但可预期。**用法**：SELF 差 0.05–0.12 时按斜率先把 decay 拉到 200–300 试探；turnover 会向 `LOW_TURNOVER`（SUPER 0.02）逼近，须同时盯。
- **但 PROD 不吃这一套**：decay = 300 时 PROD 0.7821；混合评分 `(1.0 - self) * (1.0 - prod)` decay = 250 时 PROD 0.7832——**PROD 地板由成分池决定，与评分 / decay 无关**。

### 零成本探针：成分池的 prod 分布

selection 里临时加硬门 `(prod_correlation < 0.6)`：若模拟报 `At least 10 component alphas`，说明**合格（低 prod）成分不足 10 颗**（KOR 13 颗实测如此）。模拟失败是秒级回错、不占提交配额（只占一个仿真槽很短的时间），比等一次完整的 SELF / PROD 探针便宜——**先用它判断这个池还值不值得调参**，再决定是否回 RA 挖新血。

## 4. PROD 结构性饱和（2026-09-11 跨区实测；只有这两个区有数据）

| 区域 | PROD 地板 | 结论 |
|---|---|---|
| USA | **0.85–0.91**（宽篮） | 存量池饱和，调参无解 |
| KOR | **0.78** | 存量池饱和，调参无解 |

**统一出路**：注入低 prod 新血 REGULAR（prod < 0.55 级别），把成分池的 prod 分布整体左移；新血到位后，用「宽篮 + SUBINDUSTRY（USA）+ 低 decay（3–10）」这套已过 SELF 的配置直接重提。

## 5. 其它已验证规则（规则 / 证据 / 适用范围）

| 规则 | 证据 | 适用范围 |
|---|---|---|
| **201 ≠ SA 合法**：错误异步出现在模拟结果 | 2026-09-11：`POST /simulations` 返回 201，`GET /simulations/{id}` → `ERROR`，`At least 10 component alphas are required for Super Alpha.`，`location.property: combo` | 全部区域 |
| **平台对 SUPER 的 SELF / PROD 回带 > 0.7 仍可判 PASS**——只看 `result`，不看 value；但我方铁律 prod ≥ 0.7 不提交 | GLB 0.8094 / KOR 0.8571 = PASS；KOR 0.8938 / 0.9729 = FAIL；分界在 0.86–0.89 之间不稳定，**不要按 value 预判** | SUPER；REGULAR 不适用（REGULAR 的线是 0.7） |
| **组件恰好 10 颗**：selection 是运行时筛选，self_gate / turnover 带会再刷掉一部分 → 必须放宽 gate | GLB A1NQ57NW：0.65 不行、0.70 即成 | 全部区域 |
| **`/users/self/alphas` 的 `region=` 不生效**：拉全量后按 `settings.region` 本地分组 | 2026-09-24 GLB | 全部区域 |
| **追加 SA 的真正约束是池子新鲜度**：13 颗 REGULAR 大多已被 3 颗 SUPER 消耗，新 SA 与存量近克隆风险高；差异化靠 decay / 中性化错开 + 新提 REGULAR 新血 | KOR 案例 4 | KOR；其它区未验证 |
| **提交类 CLI 的「跳过前置」路径也要单测**：`super_build.py submit --skip-precheck` 曾 `UnboundLocalError`（详情拉取被藏进 precheck 分支，2026-09-25 修） | 2026-09-25 | 工程教训 |
