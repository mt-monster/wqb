# DEU 深挖报告：analyst93 → fundamental6 两条新通道打通

> 时间：2026-10-10 17:20–18:35｜区域：**DEU（全程锁定，未换 region）**｜塔纪律：**排除已点亮塔**

---

## 〇、塔筛选（`get_pyramid_alphas`，平台权威）

DEU / D1 本季度已点亮：**`institutions=1` / `model=1` / `other=2`** ⇒ 按纪律排除这3 个 category。

**★ 但实测发现DEU 的「双塔」规律**：`pyramid_short` 显示大多数 category 的数据集都会顺带点亮 OTHER：

| 信号源 | `pyramid_short` | 塔 |
|---|---|---|
| `anl93_*` | `other/analyst` | OTHER ×1.8 + ANALYST ×1.8 = **effective 2** |
| `fnd6_*` | `fundamental/other` | FUNDAMENTAL ×1.8 + OTHER ×1.8 = **effective 2** |

⇒ **「避开 OTHER 塔」这条纪律在 DEU 基本无法执行**；正确做法是看 `pyramid_short` 确认第二个塔值不值得要。

---

## 一、ANALYST：`analyst93`（欧洲分析师历史表现统计）

**为什么选它**：cov 0.6328｜100 字段 VECTOR｜`alphaCount` 122｜**self 池只有 8 条**（几无竞争）。

### 1.1 外部文献依据（查了，两篇都直接命中）

**★ Farago, Hjalmarsson & Zeng (2024)《Analysts Are Good at Ranking Stocks》**
> 共识目标收益是**差的**横截面预测器（1999–2021：预测 2.20%/月 vs 实际 1.15%/月）；
> **但分析师「隐含排序」信息量极大** ⇒ 多空 **0.89%/月, t=5.31**，在 140 个异象策略中排**第 2**。
> 机制 = **within-analyst demeaning**（减去该分析师自己全部覆盖股的均值）⇒ 消除分析师固有偏差。

**★ NOA 异象（Betting Against Analyst Target Price）**
> 乐观分析师数 − 悲观分析师数**有强负向预测力**；买最低 NOA 组合月超额 **0.98%（t=3.80）**，
> **且在大盘/高流动性股上更明显** ⇒ **对 DEU TOP500 结构性有利**。

**★ 论坛（36 赞）**
> 「比起单个分析师修正的幅度（容易被极端预测带偏），**修正的广度**更能反映一致预期的方向性变化」

### 1.2 实测（5 批 W307–W311）

| 构造 | S | fit | sub | 2Y | PPA |
|---|---|---|---|---|---|
| **`multiply(rank(ts_mean(vec_avg(corrrev),132)), rank(ts_mean(vec_avg(recprof2),132)))`** | **1.05** | **0.63** | **1.16** | 0.71 | **✅ 全过** |
| `vec_avg(recprofitabilityprev_analyst_profitability2)` | 0.94 | 0.52 | 0.95 | 0.25 | FAIL |
| 上者 `reverse` 版 | **−0.94** | −0.52 | −0.95 | −0.25 | — |
| `vec_avg(anl93_analyst_correct_revision_ratio)` | 0.73 | 0.36 | 0.76 | **1.36** | FAIL |
| `vec_max(corrrev)` | 0.29 | 0.09 | 0.23 | 1.32 | FAIL |
| `ts_mean(vec_avg(accuracy2),132)` | **0.21** | 0.06 | 0.57 | 0.07 | FAIL |
| `vec_count(corrrev)`（关注度） | **−0.45** | −0.18 | −0.07 | 0.75 | FAIL |

### 1.3 三条语义结论
1. **分析师「历史盈利」正向**（S 0.94，`reverse` 版 −0.94，**正反对照最干净**）⇒ Farago(2024) 的直接体现
2. **关注度负向**（S −0.45）⇒ 关注度高 = 已被充分定价⇒ 与 NOA 异象同机制
3. **长窗平滑在此无效甚至反向**（`accuracy2` 长窗 S 0.21）⇒ **不要照搬 institutions1 的「长窗=三维改善」**

### 1.4 三个发批坑（整批 10 条全废过的）
| 坑 | 症状 | 正解 |
|---|---|---|
| `reverse`/`rank` 作用于 VECTOR | `does not support event inputs` ⇒ **整批 CANCELLED** | 方向算子放**外层**：`reverse(group_rank(vec_avg(f), axis))` |
| `multiply` 里放 `reverse(rank(...))` | **S = 0.0 完全归零**（两负相乘） | 方向改用 `subtract(rank(A), rank(B))` |
| 字段名凭本地库外推 | `unknown variable` ⇒ 整批废 | 逐字核对 `get_datafields` |

---

## 二、FUNDAMENTAL：`fundamental6`（DEU 唯一可用财报库）

**★ 平台实测结论**：DEU 的 FUNDAMENTAL category **只有 `fundamental6` 有覆盖**（196 MATRIX）；
`fundamental31` 平台 `count=0`；`fundamental72/89/17/1/90/93/86` cov 全 0。
且 **`get_datasets(category="fundamental")` 在 DEU 返回 count=0** ⇒ 必须逐个 `get_datafields` 验。

### 2.1 ★ 本category 的唯一有效杠杆 = `ts_delta`（变化/动量）

| 构造 | S | fit | 2Y | sub |
|---|---|---|---|---|
| ROE 水平 `divide(ibq, seqq)` | 0.82 | 0.43 | 0.55 | 0.62 |
| **★ `ts_delta(ROE, 252)`** | **1.04** | **0.60** | **1.17** | 0.75 |
| `multiply(rank(ROE), rank(毛利率))` | 0.50 | 0.20 | 0.70 | 0.40 |
| Sloan 应计 × 毛利率联合 | 0.20 | 0.05 | −0.19 | −0.32 ❌ |
| `ts_delta(ROA, 252)` | 0.99 | 0.57 | 0.96 | 0.51 |

**⇒ 「水平 → 变化」＝ S +0.22、2Y +0.62（2Y 翻倍）。**
**经济逻辑**：DEU 是高效大盘市场（TOP500），**水平量（ROE/毛利率）已被充分定价（public）**，
**只有变化/动量含增量信息** —— 与「形态可靠性 ∝ 1/市场效率」同源。

### 2.2 首次覆盖的四大经典异象
Sloan (1996) 应计｜Cooper/Gulen/Schill (2008) 资产增长｜Novy-Marx (2013) 毛利率｜Fama-French 投资因子
⇒ **实测均弱于 `ts_delta(ROE)`** ⇒ 该category 应走「比率 + 变化」路线。

---

## 三、★★ 本战役的三条 PPA-ready 通道（双闸全过）

| # | alpha id | category | 构造 | **PPA** | **self** | S | fit | 2Y |塔 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `omWGlQVn` | institutions | `ts_sum(mask(importance>1.5)×shares/holdings,132)` | ✅ | 0.6938✅ | 1.33 | 0.84 | **2.58** | inst×1.6+other×1.8 |
| 2 | `58g51G1M` | **analyst93** | `multiply(rank(m132 corrrev), rank(m132 recprof2))` | ✅ **全过** | **0.2530** ✅ | 1.05 | 0.63 | 0.71 | other+analyst ×2 |
| 3 | `3qVPNajg` | **fundamental6** | `ts_delta(ROE, 252)` + fact1 | ✅ **全过** | **0.1849** ✅ | 1.04 | 0.60 | **1.17** | fund+other ×2 |
| 4 | `A1vzo7Ld` | **fundamental6** | `ts_delta(ROE, 252)` + **fact2** | ✅ **全过** | **0.1681** ✅ | 1.00 | 0.57 | 1.11 | fund+other ×2 |

**★ 关键**：#2/#3/#4 的 `checks.fail` 均为 **`[]`（空）**，`failed_ppa_count = 0`。

### 3.1 换轴是「池空时的安全多样化手段」（新结论）
`ts_delta(ROE)` 从 fact1→fact2，**self 从 0.1849 降到 0.1681**（反而更低）。
⇒ 与我先前 institutions1 的「同腿近亲提交后 self 冲 0.99+」**不矛盾** ——
**差别在于本地池有没有同族已提交项**。池只有 8 条 ⇒ 换轴/换窗都安全。

---

## 四、经验沉淀（已写入 skill）

**`~/.workbuddy/skills/wq-brain-ra-deu/references/analyst.md`**新增「`analyst93` 实战手册」：
发批3坑 · 8 条实测构造 · 3 条语义结论 · 4 条杠杆有效性（**长窗无效/换轴无效/multiply 最有效/vec_max 未优于 vec_avg**）

**`references/fundamental.md`** 新增两个章节：
- 「开批前的不可用面复查」：唯一可用集· 3 个必避坑 · 已判死子机制 · 未测的 4 大异象 · 高 aC 字段表 · `*_curcd` 毒药字段
- 「本category 唯一有效杠杆 = `ts_delta`」：突破候选 + 对比表 + 经济逻辑 + 双塔规律 + `multiply` 非普适的警告

---

## 五、下一步（10 颗目标的推进路径）

三条通道都只差**RA 通道的三个数值**（S 1.58 / fitness 1.0 / 2Y 1.58），PPA 通道已通。

**最高成功率的三条路**：
1. **`ts_delta` 窗口/轴/口径网格**（`3qVPNajg` 基础上：66/132/504× fact1/2/3 × ROE/ROA/季度ROE）
2. **`ts_delta` × `ts_rank`/时序归一**（今日尚未在fnd6 上试的算子组合）
3. **sub/盈利质量的 `ts_delta`**（`divide(oancfy,ibq)` 的变化 = 盈利质量改善，动量里最强的一类）

**⚠ 提交前置**：`check_prod_correlation` + **你的授权**（`ALLOW_ALPHA_SUBMIT=False` 全局锁定，提交权在你）。
