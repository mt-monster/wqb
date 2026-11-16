# Osmosis 分配 Review — 官方文档 + 论坛经验对照（2026-11-16）

> 对象：2026-11-15 锁定的 138 颗 / 6 scope 分配。目标：收益最大化。
> 来源：官方《Osmosis Allocation Guide for Consultants》+ 论坛 9 篇（62/70/48/42/39/36/31/24/22 赞）+ 11-02 新鲜复盘帖。

## 1. 收益公式与两个目标（先分清）

收入 = base payment × (Pyramid+Theme 合并倍数) × **Osmosis Multiplier (1–2×)**；后者由 **Daily Osmosis Rank** 决定（各已分配 scope 的「单日毛 PnL 全平台排名」取算术平均，数据来自 2 年前 OS 期同一天，锁后第 8 天生效）。Genius 季度另取 max(四项 Combined)，其中 **Combined Osmosis = after-cost Sharpe**（费后）。

⇒ **两目标分歧**：Daily Rank 用**毛** PnL → 高 IS/高换手不伤 rank；Combined Osmosis 用**费后** → margin 才是硬约束。收益最大化的主杠杆是 rank（每日乘数），margin 是 Genius 侧保险（且只在 Combined Osmosis 是四项 max 之首时才起作用）。

## 2. 官方指南 tips ↔ 我们的 v2 分配器逐条对照（已 1:1 实现）

| 官方 tips | v2 实现 |
|---|---|
| inv 后 Sharpe 衰减 ≥60% 剔除（除独特/异数据集） | `--decay-cut 0.60` ✓ |
| TO>20% 避免，除非 inv 稳健 | `--turnover-cut 0.20` + `inv≥1.5∨OS≥1.0` 豁免 ✓ |
| 消除高互相关 | `ρ≥0.70` 丢 / `0.60–0.70` ×0.5 ✓ |
| ≥3 scope、恰好 100k、≥10 颗 | 6 scope × 100,000 精确 ✓ |
| major scope（USA/GLB）混搭强项区 | USA+GLB+4 小区 ✓ |
| 数据集/算子/中性化分散 | 候选全池打分，无单数据集偏置 ✓ |
| 避免频繁激进重排（按周渐进） | 周任务 +3/−3 渐进 ✓ |
| 优质老 Alpha 也可入池 | 池含全部历史提交 ✓ |
| 「数量多一点的高质量 Alpha 通常更好」 | 20–24 颗/scope ✓ |

**结论：官方口径下当前分配结构无违规项。**

## 3. 论坛经验对照：唯一缺口 = margin 维度

- 62 赞「根本原理」：margin/turnover 是费后能否成立的核心约束；「毛 Sharpe 好看、费后白干」是全配最隐蔽的问题。
- 11-02 复盘帖（最新实证）：**margin ≥1.5× 地板是甜点**——净累计 +26%、日均毛 PnL +4%，代价净 Sharpe −3.5%；并明确「Daily Rank 排毛 PnL，margin 主要是 CB（费后）问题」。
- 评论区（LA79055）：margin 中位仅 ~13bp 的池子，1.5× 硬滤只留 ~46%，会与「每 scope ≥10 颗」冲突，需按 region 调倍数。
- v2 分配器有 inv/TO/decay/corr 四道闸，**唯独没有 margin 闸**。

## 4. 当前分配的费后体检（margin 从缓存补算，地板 10bp）

费后代理 = inv × (1 − 地板/margin)，点数加权：

| scope | wavg_inv | wavg margin | wavg TO | **费后代理** | <10bp 点数占比 | TO>20% 点数 |
|---|---:|---:|---:|---:|---:|---:|
| KOR | 2.474 | 18.9bp | 0.164 | **1.098** | 22% | 26k |
| USA | 2.751 | 16.7bp | 0.106 | **1.071** | 39% | 8k |
| IND | 2.210 | 15.4bp | 0.186 | **0.703** | 66% | 51k |
| DEU | 1.649 | 18.2bp | 0.140 | **0.558** | 5% | 0 |
| GBR | 2.206 | 10.9bp | 0.165 | **0.333** | 56% | 24k |
| GLB | 3.016 | **7.6bp** | **0.262** | **0.246** | **74%** | 55k |

**GLB 是费后结构性最弱**（wavg margin 低于 10bp 地板、TO 26%）：rank 侧它反而是最强 scope（wavg IS 3.57），但 Combined Osmosis（费后）会被拖累。GBR 次弱。KOR/USA/DEU 费后健康。

### GLB/GBR 的可换血空间（池外候选，margin≥12bp & TO≤25%）
- GLB：仅 1 颗（VkaXbmbG，margin 18.2bp，S 3.52，TO 0.117，已过硬闸未入选）⇒ 可单点换掉 **6Xdm3pXL（margin 1.8bp，TO 56.4%，7092 点）**
- GBR：仅 2 颗（rKO0GOVj S 1.65 偏弱；e7QGwrx6 是 SA，被 3qompGeZ 挤出，margin 15.1bp 健康）
- KOR 池外有 **20 颗健康候选**（含 9 颗 SA，O0Aw0Y7Y 24.8bp / RRA9EZKz 45.1bp / 9qjGvaWe 43.1bp）——但 KOR 已是 24/24 满编且费后最优，无换血必要
- DEU 池外 0 颗 —— 印证 DEU 池薄是事实，维持现状

## 5. 逐区判定（收益最大口径）

| scope | 判定 | 依据 |
|---|---|---|
| KOR | **保持** | 费后代理第一（1.098）、n_eff 6.2 最高、SA 锚点刚更新 |
| USA | **保持** | 费后 1.071、TO 最低 0.106、官方点名 major scope |
| IND | **保持** | 费后 0.703 中游；TO>20% 5.1 万点是因 inv 豁免合规，官方口径允许 |
| DEU | **保持** | 池外 0 候选，22 颗已尽力；费后 0.558 尚可 |
| GBR | **保持 + 观察margin** | 56% 点数 <10bp，但池外无更好替代；费后代理 0.333 |
| GLB | **保持 scope（rank 最优），建议 margin 软加权** | IS 3.57 全场最高（rank=毛 PnL，GLB 是加分 scope）；但费后 0.246 垫底，若 Combined Osmosis 进入四项 max 之首会被拖累 |
| EUR | **继续排除** | returns 0.056 最低、wavg_inv 1.326 拉低均值、0 OS |
| MEA | **继续排除，留一个待验证项** | 见 §6 |
| ASI/HKG | **继续排除** | 9/7 颗 <10，无资格 |

**Scope 数量不加**：rank 是算术平均，加弱 scope 必稀释（官方原文 "Performance is not proportional to number of scopes"）。当前 6 scope 已是「质量够格池」的上限。

## 6. MEA「周日独赢」假设（31 赞帖）——不采纳但可验证

论点：周日仅 MEA 开市 ⇒ 配了 MEA 的顾问当天 rank 由 MEA 独立驱动，是避开竞争的窗口。
不采纳理由：MEA wavg_inv 1.261 全场最低 ⇒ 周一至周五（MEA 也交易）每天拉低平均，只为周日 1/7 天的独占收益，期望值为负；且 MEA 已被平台下架，scope PnL 是否仍计算未证实。
待验证（成本低）：若平台仍计算 MEA scope PnL，可临时配 10 颗凑 100k 观察周日 rank 变化两周，再回滚——**默认不做，等用户拍板**。

## 7. 可执行建议（按期望收益排序）

1. **margin 软加权进分配器**（新增 `--margin-floor 10 --margin-soft-weight 0.5`，仿 corr-soft 逻辑）：margin<10bp 的候选权重 ×0.5。预期 GLB/GBR 内部点数向健康成员集中（GLB 74%→约一半），不破 scope 资格（软权重不清零）。**证据**：官方 Genius=after-cost Sharpe + 11-02 帖甜点实证。**影响**：只改善 Combined Osmosis（费后），Daily Rank（毛 PnL）基本不动。
2. **GLB 单点换血**：6Xdm3pXL（1.8bp/TO 56%）→ VkaXbmbG（18.2bp/TO 11.7%，S 3.52），需先跑互相关确认 <0.70。
3. **rank 纪律重申**（36 赞黑箱帖 + 官方）：周一至周三是同一个 2 年前样本，周四才更新；单日 0.10↔0.82 波动禁止归因；评估看 MA5/MA20 + 「改动→锁点→8 天生效→2 周可见」的 5–8 周窗口。
4. Combined Osmosis 资格无忧：需 3 个月内 ≥6 周有效分配，当前连续有效远超门槛。

## 8. 数据边界（本次 review 的限制）

- margin 数据来自 `api_cache` 5 条分页快照（本周刚刷新，1467 颗含全量 is 块），非回源终值；结论对 10bp 量级不敏感。
- per-scope rank 无端点（11-14 已实测），scope 优劣只能用 IS/费后代理比较，无法实测各 scope 实际排名贡献。
