---
name: wq-window-valley-break-prod-wall
layer: L4
description: 用「窗口微调 (ts_rank 的 W)」破 prod 相关性墙的完整方法论——当候选 IS 全闸通过但 prod 卡在 0.70-0.72 时使用。核心：先用 prod 直方图 [0.7,0.8) 桶 n 值判族级命运（n=0 可救 / n≥1 必死），再在 n=0 的族上扫窗口网格找谷。含实证谷位表、工具脚本、与秩后裁剪法的分工。
last_verified: 2026-10-29
agent_created: true
---

# 窗口微调破 prod 墙（window valley）

## 职责边界

- **本 skill 负责**：prod 只差 0.001–0.02 时的**窗口维度**手法 —— 直方图 n 值判族命运、`ts_rank` 窗口网格扫谷、谷内 2Y 稳定性核验。
- **本 skill 不做**：prod/self 的**读数与判据**（→ [`wq-prod-corr-read`](../wq-prod-corr-read/SKILL.md)）；改持仓面的通用降 prod 杠杆选择与 self 自锁（→ [`wq-prod-lever-self-lock-guard`](../wq-prod-lever-self-lock-guard/SKILL.md)）；秩后裁剪（→ `wq-post-rank-clip-break-prod-wall`）；提交（→ [`worldquant-submit-alpha`](../worldquant-submit-alpha/SKILL.md)）。
- **上游 / 下游**：上游 = IS 全闸通过、概念本身是新的、prod 微幅超线的候选；下游 = 谷位定稿的候选交回 RA 步 8 提交清单。

## 何时用

候选 **IS 全闸通过**（`checks.fail=[]`）但 **prod 卡在 0.70–0.72**（只差 0.001–0.02），
且信号概念**本身是新的**（不是已有 book 的同族换个包装）。

**与秩后裁剪法的分工**（两个是独立手法，不是替代关系）：

| 手法 | 作用对象 | 2Y 影响 | 适用 |
|---|---|---|---|
| **窗口微调**（本 skill） | `ts_rank` / `ts_*` 的窗口 W | **几乎不动（±0.05）** | prod 与 2Y 双紧、裁剪会毁 2Y 时 |
| 秩后裁剪（`wq-post-rank-clip-break-prod-wall`） | 已排名的权重剖面 | 通常**上升** | 裁剪网格能过、且 2Y 有空间时 |

⇒ **先用本 skill 的 n 值判据决定族命运，再决定是否用裁剪法。**

## 核心机制

**形态**：保持信号概念与外部几何完全不变，只改 `ts_rank(X, W)` 的时间窗口 W。

**为什么有效**：窗口改变**持仓的时间结构**，不改变信号的横截面排序内容。
- prod 相关性 = 与 book 里同族 alpha 的**持仓周期共振度** ⇒ W 变了，共振度变
- 2Y / Sharpe = 依赖信号的横截面预测力 ⇒ W 小改（±20%）几乎不动
- ⇒ **窗口是唯一「只动 prod、不动 2Y」的旋钮**（本区实测：2Y 在谷内稳定 ±0.05）

**为什么不是通用手法**（重要）：
- 只有当该概念在 prod book 的相关性曲线上**存在一个"谷"**时，窗口才有效
- 不同字段/不同几何的谷位置**完全不同**（amt 谷在 [408,480]，qty 无谷、大窗区无谷）
- ⇒ **必须先判 n 值，再扫窗口**

## 前置判据（省 10 批盲试）

查候选的 prod 直方图，看 **`[0.7, 0.8)` 桶的 n 值**：

| n([0.7,0.8)) | 判定 | 动作 |
|---|---|---|
| **n = 0** | 该族**存在过线窗口** | 扫窗口网格（W 下压 8~18%） |
| **n ≥ 1** | **单钉子卡死**，无论怎么调 W 都过不了 | 弃（换概念/几何，别扫窗口） |

**工具**：`tools/prod_bucket_scan.py <id...>`（该脚本在本工作区 `wqb/tools/` 下）——直接打印每条的 `prod_max / n / SCAN|DEAD`。

**实证精度**：KOR 2026-10-04，16/16 精确命中（d50 10/10 + d53 6/6 + d54 4/4），**零例外**。
- n=0 的族（amt 净买入占比 / oth466 净利资产）：全过线
- n=1 的族（qty 净买入占比 / sell_qty/buy_qty）：谷底全部卡在 0.7019–0.7031，**永远差 0.002–0.003**

### ⚠⚠ 跨区反例：`n = 0` 只说明「prod 有救」，**不说明「族有救」**（2026-10-29 GBR）

`n=0` 是**prod 单一维度**的判据，**不覆盖 2Y / 换手 / RA 闸**。GBR `tm_17` 差分骨架实测：`[0.7,0.8)` 桶 **n=0**（按本表判「可扫窗口」），但该死因根本不是 prod —— 三种独立的降换手机制（设置层 `decay` / `ts_target_tvr_decay` / `hump`）一致把 2Y 压到 **1.46–1.47**，可行窗仅 **0.004** 宽。

⇒ **判族命运必须两轴同看**：
1. **prod 轴**：`n([0.7,0.8)) == 0` ⇒ prod 存在过线窗口；
2. **2Y / 换手轴**：先确认该族不存在「换手–2Y 硬互斥」（形态定义见 `wq-wave-preflight-dispatch` §2.3 第三档）。

两轴任一不过 ⇒ 弃族。**别把「n=0」当成活路证明。**

## 执行流程

1. **判 n 值**：`python tools/prod_bucket_scan.py <base_id>`
   - `n ≥ 1` ⇒ 停止，换概念
   - `n = 0` ⇒ 进入第 2 步
2. **定位谷区**：基线窗口通常较大（如 1008/2016/504）。沿 `W → W×0.85` 方向试 2–3 点，看 prod 是否下降
   - 若 prod 随 W 下降 ⇒ 谷在更小 W 方向，继续压
   - 若 prod 不变/上升 ⇒ 该区间不在谷，换区间
3. **细扫谷**：在疑似谷区按 ~5% 步长扫 5–7 个点，记录各自的 prod + n 值
4. **锁定谷底**：取 prod 最低且 **n=0 保持** 的窗口
5. **验证全闸**：对谷底候选重跑 `submit_verdict` + 逐年稳健性 + 落库

## 实证谷位表（KOR / TOP600 / delay1 / STATISTICAL / decay4 / trunc0.08）

| 概念 | 谷区 W | 谷底 prod | 备注 |
|---|---|---|---|
| `net_buy_amt / (buy_amt + sell_amt)`（shrt38） | **[408, 480]** | **0.6929** (W=408) | 谷宽 72 交易日 |
| `consol_net_inc_q / bs_assets_tot_q`（oth466） | **[420, 480]** | **0.6762** (W=420) | 跨数据集，谷位巧合相同 |
| `net_buy_qty / (buy_qty + sell_qty)` | 无谷（n=1） | 0.7031 | 永不过线 |
| `sell_qty / buy_qty` | 无谷（n=1） | 0.7019 | 永不过线 |
| `shrt38_amt / amt_wgt`（绝对规模） | — | S≈0 | 规模类无信号 |

⚠ **禁外推**：谷位随区域/数据/中性化变化，**换区必须重测**。此表仅供 KOR 起步参考。

## 关键陷阱

1. **同族只提 1 颗**：谷内所有窗口变体的 self 相关会互撞（提交第 1 颗后第 2 颗 self 飙高）
   ⇒ 谷内 N 条 = **1 个提交名额**，选 prod 最低者
2. **★★★ `self = prod` 同数值且逐位相同 —— 这是「自己占位」不是 crowd**（2026-10-29 GBR 实证加强）：
   与**自己已提交的 ACTIVE alpha** 同族时，两道闸返回**完全相同的数值**（实测 0.8825/0.8825、0.8718/0.8718）；
   更极端时**表达式不同但 PnL 相同**也会让 self = **1.0**（`subtract(p1,p0)` vs `p1`）。
   ⇒ 看到同值先怀疑自己挡自己，**不要判 crowd、更不要换窗口去救**（换窗口只是在自锁空间里打转）。
   **发批前强制动作**：同数据集同字段族的新波，派仿真之前先跑
   `compute_mutual_correlation(候选 + 同族 OS alpha, threshold=0.7)`；
   若 `max_mutually_below_subset.size == 1` ⇒ **整枝判死**，一颗提交名额都不剩。
   （详见 [`wq-prod-lever-self-lock-guard`](../wq-prod-lever-self-lock-guard/SKILL.md) §一 硬约束 4。）
3. **CLUSTER_TEST 会随同族升高**：同族候选的 CLUSTER_TEST 逼近限 1（实测 0.94–0.96）
4. **验证顺序**：n 判据 → 谷扫描 → prod/self 复测（`refresh`）→ 稳健性 → 落库

## 配套脚本

- `tools/probe/prod_bucket_scan.py` — prod 直方图 n 值判据（SCAN/DEAD）
- `logs/_prod4.py` — 查指定 id 列表的 prod_max + 0.45-0.75 直方图分布
