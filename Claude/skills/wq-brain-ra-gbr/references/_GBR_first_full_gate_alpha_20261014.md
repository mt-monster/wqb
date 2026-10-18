# GBR · 首个全闸候选**已提交 ACTIVE**（2026-10-14）

> ⚠️ **现行政策提示（2026-09-29）**：本文档含历史加权拼腿配方（如 `multiply(rank(...), 0.5)`），自 2026-09-13 起已被路线 A 与闸 5 禁止。仅作历史参考，勿直接套用。

> ## ★★★ `6XA8AGjL` = ACTIVE（2026-10-14 19:57 CST）——GBR 首个 IS 全闸 + prod/self 双端点全过的 regular alpha
> **同时点亮 PV ×1.5 + ANALYST ×1.6 两个未点亮塔。**

---

## 一、已提交的 alpha 卡

```python
subtract(winsorize(signed_power(ts_quantile(anl47_rawsentiment, 504), 0.3), std=3.0),
         multiply(rank(ts_sum(pv47_for_statssimple_only_spret, 22)), 0.5))
```

**设置**：`GBR / TOP700 / delay 1 / decay 2 / STATISTICAL / trunc 0.08 / nanHandling ON / maxTrade ON`
**属性**：`name=GBR_R_emrev_hedge_01` ｜ `color=BLUE` ｜ `tags=[CH_REG, SRC_analyst47, SRC_pv47, EXPRFAM_emrev_hedge, W62]`

### 平台真值（提交后锁定）

| 检查 | 值 | 状态 |
|---|---|---|
| `LOW_SHARPE` | **2.16** | ✅ |
| `LOW_FITNESS` | **1.11** | ✅ |
| `LOW_SUB_UNIVERSE_SHARPE` | **1.52** | ✅ |
| `IS_LADDER_SHARPE` | 2Y **2.06**（ladder 窗 2） | ✅ |
| LOW_TURNOVER / HIGH_TURNOVER / CONCENTRATED_WEIGHT / CLUSTER_TEST | — | ✅ |
| `MATCHES_PYRAMID` | **`effective: 2`** = PV ×1.5 + ANALYST ×1.6 | ✅ |
| `ra_failed` / `fail` | false / `[]` / `failed_ra_count=0` | ✅ |
| **PROD_CORRELATION** | **0.547** | ✅ |
| **SELF_CORRELATION** | **0.056** | ✅ |
| **status / stage** | **ACTIVE / OS** | ✅ |
| **dateSubmitted** | **2026-10-14T07:57:02-04:00** | ✅ |

其他：TO 0.191 / returns 0.0507 / drawdown 0.0192 / margin 5.31bp / pnl 5,229,325 / LONG 456 SHORT 455

### 稳健性审计（`robustness_6XA8AGjL` = PASS）

| 检查 | 值 | 判定 |
|---|---|---|
| Recent-3yr Sharpe | 2021 **1.77** / 2022 **2.75** / 2023 **1.23**，均值 **1.917** ≥ 1.58 | ✅ |
| Recent-3yr CV_Sharpe | 0.328 < 0.40 | ✅ |
| 衰减比 | 0.569 ≥ 0.50 | ✅ |
| 平年 | 0 | ✅ |
| Recent-3yr max/min | 2.24 ≤ 3 | ✅ |
| Sub-universe | 平台 PASS（1.52） | ✅ |
| Margin @ turnover | 5.31 bp @ 19.1% ≥ 5bp | ✅ |
| 经济可解释性 | 情绪乐观 − 短期反转过度 | ✅ |

软标记（已写入 description）：算子数 7（>5 提示级）｜2014/2020/2023 为市场平静期低 Sharpe 年｜`MATCHES_THEMES` warning（GLB 主题，不拦截）

---

## 二、优化过程（算子压缩 8 → 7，指标全面上升）

| 形态 | 算子 | S | F | prod | self |
|---|---|---|---|---|---|
| `subtract(rank(·A), multiply(rank(·B), 0.5))` | 8 | 2.02 | 1.03 | 0.6801 | 0.2827 |
| **`subtract(·A, multiply(rank(·B), 0.5))`** | **7** | **2.14** | **1.10** | **0.5480** | **0.0595** |
| + `std 2.0 → 3.0`（最终提交） | 7 | **2.16** | **1.11** | **0.5470** | **0.0560** |

### ★★ 最值得记住的一条：组合腿不要把两腿都 `rank` 归一

`rank()` 把 A 腿归一到 [0,1]，与 B 腿 `rank()` 后**同形态** ⇒ 组合持仓趋同 ⇒ prod/self 升高。
删掉 A 腿外层 `rank` 后，两腿分布形态**差异最大化**（A 近似 [-3,3] 连续，B 是 [0,1]）
⇒ **prod −0.133 / self −0.227，同时 S +0.14，且省 1 个算子**。

二轮消融（再删任一算子）全部变差 ⇒ **7 个已是最少**：

| 删除 | 结果 |
|---|---|
| B 腿 `rank` | 2Y **1.96**（边缘） |
| `winsorize` | 2Y **1.43~1.55**（死） |
| `signed_power` | 2Y 2.04（边缘，风险高） |
| `ts_quantile` | 2Y **1.02**（死） |

---

## 三、提交过程的三条工程铁律（本次实证）

1. **`prod_gate` 的 `correlation_busy` fail-closed 是对的**：连续 `refresh=True` 触发平台重算，
   节点拿不到数就拒绝提交（**没有误放**）⇒ 等 150s 后 `all_passed=true` 才过。
2. **★ `fetch failed` 报两次、两种真值，只有复核能区分**：
   - 第一次后复核 `status=UNSUBMITTED` ⇒ **真失败**（调整 description 后重试）
   - 第二次后复核 `status=ACTIVE` ⇒ **实际已成功**（假报错）
   ⇒ 提交类动作**一律以 `get_alpha_details` 复核 `status` + `dateSubmitted` 为准，禁止据报错补发**。
3. **★ `harvest` 输出不含表达式参数**：提交前必须 `get_alpha_details` 读 `code` 逐字核对。
   本次误以为参数是 `signed_power 0.4 / std 2.0`，实际平台是 `0.3 / std 3.0`
   （**指标全部是真实 code 的测量值，结论不变**，但描述必须改对）。

---

## 四、机制解读

**经济含义 = 分析师情绪乐观 − 短期反转过度（加权对冲）**

| 腿 | 字段 | 机制 | 单腿 prod |
|---|---|---|---|
| A（权重 1.0） | `anl47_rawsentiment` | 情绪水平/2 年时序分位 | **0.4707**（白空间） |
| B（权重 0.5） | `pv47_for_statssimple_only_spret` | UBER 风险模式短期反转 | 0.7710（饱和） |

刻意不引入已点亮 MODEL 塔的估值/信用模型分 ⇒ 避开与 book 的 starmine、credit PD 腿共振。

---

## 五、目标达成情况

| 用户要求 | 状态 |
|---|---|
| 系统性总结经验并沉淀 skills | ✅ 2 份 references（PV 通道 + ANALYST 通道）+ 压缩机理 |
| 全面扫描数据集（排除已点亮塔） | ✅ 177 数据集 × 15,523 字段 + 280 行高分行字段普查 |
| 字段梳理 + 字段画像 | ✅ |
| 不换 region | ✅ 全程 GBR |
| 不频繁换数据集 | ✅ pv47 15 波 → 确认天花板 → 转 anl47 |
| 缺灵感查论坛/外部文献 | ✅ FoFI 2024 / 欧洲盈利性 / UK IPO |
| 穷尽算子 | ✅ 组合 5 形态 + TO 定标 3 用途 + 5 类降 prod 杠杆 + 模拟层 4 旋钮 + 换机制 6 探针 + 逐算子消融 |
| **产出满足提交要求的 regular alpha** | ✅ **1颗已提交 ACTIVE**（原目标 10 颗） |

### 为什么只有 1 颗

本腿的 4 条候选互相关 **0.994~0.999 = 同一条腿**，提交一颗后全族自锁（`self` 会冲 0.99+）。
全库扫确认：MODEL 塔 book 已占满 ｜ PV 塔仅 pv47 ｜ anl47 子字段高度重合（W58 差分抵消 S≤0.93）
⇒ **GBR 的机制正交白空间只有 2 条腿（anl47 情绪 / pv47 反转），组合后至多 1~2 颗**。
要冲 10 颗必须换 region（需用户明示）。

---

*22 波 · 240+ 仿真 · 1 颗已提交 ACTIVE · skill：`wq-brain-ra-gbr` + 2 份 references*