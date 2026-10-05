# EUR · 20 条全闸候选累积进度（真相版）

> **目标**：20 条**未提交**的 regular alpha（全闸 + prod<0.7 + 同族折算后）
> 铁律：只挖不提交（提交权归用户）｜EUR 锁定｜不频繁换数据集｜没灵感先查论坛

## ★ 口径定义（2026-10-05 实测踩坑后确立）

```sql
-- ★ 四个条件缺一不可
WHERE sharpe>=1.58 AND fitness>=1.0 AND two_year_sharpe>=1.58 AND sub_universe_sharpe>=1.0
  AND COALESCE(soft_deleted,0)=0        -- ★ 不是 IS NULL（那是恒假条件！）
  AND status='UNSUBMITTED' AND date_submitted IS NULL   -- ★ 已提交的必须排除
  AND prod_correlation<0.7              -- prod 撞墙的不算
-- 再按「同族铁律」折算：表达式骨架（数字→N）相同的多颗只计 1 条
```

## 进度总览

| 项 | 数量 |
|---|---|
| **净可累积（独立机制，全闸+prod通过+未提交）** | **2** |
| 全闸但 prod 撞墙 | 2 |
| 同族成员（不重复计） | 4 |
| **距目标还差** | **18** |

## 一、✅ 净可累积（2 条独立机制 / 11 颗变体）

### ★★★ 第 3 条（本会话最佳）：`WjegEmQO`
| | |
|---|---|
| 表达式 | `group_zscore(hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)), hump=0.001), subindustry)` |
| 设置 | TOPCS1600 / **decay=160** / INDUSTRY / trunc 0.08 / **maxTrade=ON** |
| **S** | **1.94**（全 EUR 历史最高）|
| **F** | **1.38** |
| **2Y** | **1.59** |
| **sub** | **1.96** |
| **robust** | **1.37** |
| **prod** | **0.5012** PASS（n[.7,.8)=0）|
| **self** | **0.1616** PASS |
| 闸门 | `fail=None`，warning 仅 MATCHES_COMPETITION |

**★ 关键杠杆**：`group_zscore(·, subindustry)` 外层包装（相对裸 hump+rank：S +0.29 / F +0.28 / sub +0.31 / robust +0.27，代价 2Y −0.22）。
同族（**同一骨架、仅分组轴不同 ⇒ 按铁律全部计入同族**）：
`786Jellx`(industry, S1.64/2Y1.75/sub1.58, **prod 0.4837 / self 0.1742**)、
`88PLAMnX`(sector, S1.61/2Y1.71/sub1.61)、`blO97pAZ`(market, S1.62/2Y1.75/sub1.62)
⇒ **提则提 `786Jellx`**（prod 0.4837 最低，且 2Y 1.75 margin 比 X13 的 1.59 厚得多）。

### 第 2 条：`1YZJAMqK`（`group_zscore` 的裸形态，**另一个独立骨架**）
`hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)), hump=0.001)`
+ decay=160/INDUSTRY/trunc0.08/maxTrade=ON
**S1.65 / F1.10 / 2Y1.81 / sub1.65 / prod 0.4791（全区最干净）/ self 未测**
同族：`omWVZ7lm`（decay=40, S1.75/2Y1.76）。

### ⚠⚠ 计数纠正（2026-10-05）
我一度把 `WjegEmQO` 与 `786Jellx` 算成2 条，**实际是同族**（骨架相同，只差分组轴）。
**11 颗全闸候选 → 2 条独立机制**。
判定口径：**同族 = 表达式骨架相同（数字归一 + 分组轴归一）**，只换设置档/分组轴 ⇒ 同族。


| alpha_id | 机制 | S | F | 2Y | sub | **prod** | TO |
|---|---|---|---|---|---|---|---|
| `1YZJAMqK` | **CASSIE `ocf_currliab` 变化量** | 1.65 | 1.10 | 1.81 | 1.65 | **0.4791** | 0.0304 |

`hump(rank(ts_delta(vec_avg(qfl_cassie_convention_ocf_currliab),22)), hump=0.001)`
+ TOPCS1600 / **decay=160** / INDUSTRY / trunc 0.08 / **maxTrade=ON**

同族成员（不重复计）：`omWVZ7lm`（同表达式，decay=40，S1.75/2Y1.76）。

## 二、✗ 全闸但 prod 撞墙（2 条独立机制 / 4 颗）

| alpha_id | 机制 | prod | 结论 |
|---|---|---|---|
| `pw5VPeoX` / `WjeabvQO` / `E5RgROOL` | `netprofit_y2_estimate_change` + `group_zscore` | 0.7572 / 0.7489 / 0.7540 | ❌ 机制层拥挤 |
| `58gazEEk` | 同上 + `hump` | 0.7599 | ❌ |

⇒ **netprofit_y2 族 4/4 全撞 0.75–0.76 ⇒ 整族不必再试。**

## 三、❌ 已纠正的错误记录（务必留档）

| 我曾错误登记 | 真相 |
|---|---|
| `JjQmx9nm`（prod 0.6695，四项全过）| **已于 2026-10-03 提交**（ACTIVE/OS）⇒ 不是存量 |
| `N1VnJjXg` | 与 `omWVZ7lm`/`1YZJAMqK` **同表达式** ⇒ 同族不单计 |
| 「库里一条全闸都没有」 | ❌ 错在 `soft_deleted IS NULL` 恒假；实际全库 48 条 |

**全库视角**：48 条全闸+prod<0.7 中，**35 条早已提交**，真正未提交仅 13 条，
按 region 是 GLB 10 / KOR 2 / EUR 1 ⇒ **EUR 侧本就缺存量**。

## 四、达成 19 条缺口的路径

| 路径 | 状态 | 依据 |
|---|---|---|
| **A. CASSIE 族深挖** | ⏳ wave331 在飞 | 32 字段仅测 11；`ocf_currliab` 已证明能出全闸+prod0.48 |
| **B. CASSIE 变化轴替换** | ✅ wave332 备好 | 45 次历史**全用 `ts_delta`**；`ts_rank`/`ts_std_dev`/`ts_decay_linear`/`ts_corr`/二阶**全未用** |
| **C. 四层嵌套残差** | ✅ wave333 备好 | `JjQmx9nm` 结构 prod 0.6695 通过；换轴找更多 prod<0.7 变体 |
| D. 其他 region | ⛔ EUR 已锁 | 全库未提交 13 条里 EUR 仅 1 |

## 五、本轮进展（wave327–333）

| 波 | 目标 | 结果 |
|---|---|---|
| wave327 | long_term 120d 族补扫 | 找到 `regime4`（四项全优于控制行）|
| wave328 | 设置档首扫（发现 `maxTrade`）| **★ 产出 `1YZJAMqK`** |
| wave329 | `maxTrade` 跨族迁移 | 三族确证（TO 降 43–58%）|
| wave330 | 攻 2Y（decay 方向）| decay=160 → 2Y 1.81、TO −26% |
| wave331 | **CASSIE 21 未测字段** | ⏳ 在飞（W9 债务加权利率 S1.48/2Y2.05 最有希望）|
| wave332 | **变化轴替换**（`ts_rank`/`ts_std_dev` 等全未用轴）| ★★ **产出 `WjegEmQO` S1.94（全 EUR 最高）** |
| wave333 | **四层残差深挖** | 备好待发 |
| wave334 | W9 债务加权利率攻顶 | 备好（S1.48/2Y2.05，被 §100 证伪 subindustry 交叉）|
| wave335 | **model27**（StarMine 信用 PD，独立数据源）| ❌ 全灭，最高 0.68 ⇒ 证「绝对违约概率在 EUR 无效」|
| wave336 | **group_zscore(·,subindustry) 深挖 + 分组轴全扫** | ★ **推翻 skill 判据**：group_zscore 不退化；粒度决定效果 |
| wave337 | subindustry × CASSIE 15 字段 | ★★ **证伪「杠杆可跨字段迁移」**（3 正 / 10 负，最大 −0.81）|
| wave338 | **analyst_base_ref** 分析师预期 | ❌ 全灭 0.61 ★ **根因：信号字段覆盖仅 0.3158**（数据集级 0.832 骗人）|
| wave339 | **analyst45**（覆盖 1.0，投资 idea 跟踪）| ⏳ 在飞 |
