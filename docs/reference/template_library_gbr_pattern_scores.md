# GBR / TOP700 / D1 —— `pattern_scores` 技术形态相似度模板库

> 数据集：`pattern_scores`（category = **PV**，全部字段单塔 `GBR/D1/PV`）
> 区域：GBR / TOP700 / D1；族级设置 `INDUSTRY + decay 2~4 + trunc 0.05`
> 建立日期：2026-10-30
> 用途：PV 塔需 2 条（本区实际 0），且 PV 族已验证与估值族近乎正交（pv20 流动性对估值族 0.07–0.13）⇒ 本数据集是 PV 塔的主要剩余入口。

---

## 一、数据集画像（平台实读）

- **字段数 504**，全部 MATRIX，**coverage 0.9747–0.9998**（TOP700 几乎全覆盖，无覆盖风险）
- **拥挤度极低**：userCount 0–76，alphaCount 0–97；多数字段 userCount 个位数
- 值域 **相似度分数 [0,1]**，无量纲 ⇒ 单位闸几乎无风险

### 1.1 字段命名结构

```
<pattern>_<stat>_simscore_lookback<W>
```

| 维度 | 取值 |
|---|---|
| `pattern` | `asc_triangle` / `asc_triangle_down` / `breakaway_gap_up` / `breakaway_gap_down` / `common_gap_up` / `common_gap_down` / `falling_wedge` / `rising_wedge` / `symmetrical_triangle`(up/down) / `v_reversal_bottom` / `v_continuation_top` / `cont_falling_wedge` / `cont_rising_wedge` / `falling_support_flat_resistance` / `rising_support_flat_resistance` |
| `stat` | `mean`（均值相似度）/ `median` / `min` / `max` / `std` / `q95`（95 分位）/ `dynamic`（偏向近期 bar）/ `adaptive` |
| `W` | `60` / `120` |

另有 `avg_similarity_*`（无 `lookback` 后缀）与 `adaptive_similarity_*` 两族命名变体，同样在库内。

### 1.2 字段选择要点

- **同一 `stat` + 同一 `W` 的 up/down 镜像对**是控制变量最干净的多空配对来源（见 T7）：
  - `breakaway_gap_up_mean_simscore_lookback60`（userCount 41）vs `breakaway_gap_down_mean_simscore_lookback60`（userCount 76）—— 两者 coverage 均 0.9998
- `lookback60` 的 coverage 普遍 ≥ `lookback120`（0.9998 vs 0.9953）
- `std` / `max` / `min` 类字段大量 userCount = 0（未开发）

### 1.3 已核实的首发字段

```
breakaway_gap_up_mean_simscore_lookback60     cov 0.9998  u41/a54
breakaway_gap_down_mean_simscore_lookback60   cov 0.9998  u76/a92
avg_similarity_v_reversal_bottom              cov 0.9747  u12/a14
asc_triangle_mean_simscore_lookback120        cov 0.9953  u9/a10
asc_triangle_down_mean_simscore_lookback120   cov 0.9953  u23/a27
avg_similarity_downward_symmetrical_triangle  cov 0.9747  u69/a97
```

---

## 二、经济机制（三条，互不重叠）

### 2.1 技术形态的自我实现（Osler 2003）
限价单与止损单聚集在技术形态的关键位（颈线、趋势线）。当足够多交易者观察同一形态，**形态成立本身会触发订单流**，从而形态具有预测力。⇒ 形态相似度上升 = 形态正在被市场确认 = 后续资金流可期。**给出动量型（正号一阶差分）模板。**

### 2.2 技术形态的信息含量衰减（Lo-Mamaysky-Wang 2000, JF）
用非参数核回归识别 10 类经典形态，发现对美股有统计显著但**经济意义上微弱**的增量预测力，且信息含量随时间衰减、以美国市场为主。⇒ **对 GBR/TOP700 大盘股预期必须保守**；形态"越明显"不一定越好，因为已被套利者提前布局。**给出反转型（负号）与凸性放大（幂变换）两个方向相反的模板，让实测裁决。**

### 2.3 形态清晰度与瓦解（自建，二阶矩）
形态相似度高但**波动大**说明形态"时有时无"，是噪声而非形态；相似度**稳定在高位**才是真形态。⇒ 用 `ts_std_dev` 做清晰度度量（T6），用变异系数倒数做信噪比（T9）。这是纯自建机制，与上述两条论文机制互不重叠。

---

## 三、10 个结构互异模板（硬约束：≥10 且差异须落在骨架/算子几何/矩/分组轴/非线性）

**差异维度标注**：①一阶矩 ②二阶矩 ③秩/分位变换 ④幂（非线性） ⑤双尺度 ⑥跨字段配对 ⑦正交化 ⑧条件化

| # | 名称 | 骨架 | 差异维度 | 来源 | 首发状态 |
|---|---|---|---|---|---|
| **T1** | 形态形成动量 | `ts_delta(ts_backfill(S, 22), 22)` | ①一阶矩 | Osler 2003（自我实现） | 待派 |
| **T2** | 形态历史异常度 | `ts_zscore(ts_backfill(S, 22), 252)` | ①+③时序标准化 | 自建（本会话已多次验证 zscore≫rank 于异常度族） | 待派 |
| **T3** | 形态瓦解反转 | `-ts_delta(ts_backfill(S, 22), 66)` | ①一阶矩反向 + 长窗 | Lo-Mamaysky-Wang 2000（信息衰减/过度反应） | 待派 |
| **T4** | 形态年内极值位置 | `ts_rank(ts_backfill(S, 22), 252)` | ③秩变换 | 自建 | 待派 |
| **T5** | 形态成熟度（长−短窗差） | `subtract(ts_backfill(S_120, 22), ts_backfill(S_60, 22))` | ⑤双尺度（同单位相减） | 自建（形态刚形成 vs 已充分反映） | 待派 |
| **T6** | 形态清晰度 | `-ts_std_dev(ts_backfill(S, 22), 66)` | ②二阶矩 | 自建 | 待派 |
| **T7** | 缺口多空配对 | `subtract(ts_backfill(S_up, 22), ts_backfill(S_down, 22))` | ⑥跨字段配对 | 论坛 `41483078971927` 多空配对 + 缺口回补 | **批 29 已派** |
| **T8** | 凸性放大极端匹配 | `power(ts_backfill(S, 22), 2)` | ④幂（非线性） | 自建 | 待派 |
| **T9** | 形态信噪比 | `divide(ts_mean(S, 66), ts_std_dev(S, 66))` | ②二阶矩比值（同单位相除） | 自建（变异系数倒数） | 待派 |
| **T10** | 跨形态正交残差 | `vector_neut(ts_zscore(ts_backfill(S_A,22),252), rank(ts_backfill(S_B,22)))` | ⑦正交化 | 论坛 `41483078971927` / `41379961189271`（正交化与 PCA 降相关） | 待派 |

### 3.1 合规性自检

| 检查项 | 结果 |
|---|---|
| `add(A,B)` 混信号 | 全部 10 个模板均无 `add` ✅ |
| 加权混合 `multiply(rank(B), 常数)` | 无 ✅ |
| 单位闸（VERIFY） | 全部字段无量纲 [0,1]，`subtract`/`divide` 同单位相除合规 ✅ |
| 幽灵算子 | 仅用 `ts_delta`/`ts_zscore`/`ts_rank`/`ts_std_dev`/`ts_mean`/`ts_av_diff`/`ts_quantile`/`subtract`/`divide`/`power`/`vector_neut`/`ts_backfill`，全在可用集 ✅ |
| 本账号不可访问算子 | 未用 `ts_max`/`ts_min` ✅ |
| 塔位 | 全部单数据集 ⇒ 单塔 `GBR/D1/PV` ✅ |
| PV+PV 混组禁令 | 单数据集内部组合，不涉两个 PV 数据集 ✅ |
| 窗口白名单 | 22 / 66 / 252 / 60 / 120 ✅ |

### 3.2 符号约定（技术分析惯例，供实测比对）

| 形态 | 惯例方向 |
|---|---|
| 上升三角形、上升缺口、V 型底部反转、下降楔形 | **看涨** ⇒ 正号 |
| 下降三角形、下降缺口、上升楔形、V 型顶部持续 | **看跌** ⇒ 负号 |
| 上升楔形（rising wedge） | **看跌**（动能衰竭，与名称直觉相反） |
| 下降楔形（falling wedge） | **看涨** |
| 对称三角形 | 方向由突破决定，不宜单独定号 |

**纪律**：符号错不浪费验证槽——Sharpe 线性于收益序列符号，翻符号即精确取反。因此一律**按上表预取符号**后直接测强化变体；若 S 显著为负则翻转确认。

---

## 四、预注册判据（派发前写死，防事后找理由）

1. **首发 2 条（T7 + 一条探针）若 |S| < 0.6** ⇒ 该数据集形态分数整体信号弱，**不铺满剩余 8 个模板**（参照 `pv20` beta 族双灭后不铺满的先例）。
2. **若任一 |S| ≥ 1.0 且 SUB/S ≥ 0.4754** ⇒ 铺满剩余模板，并按 F 是否 ≥1.0 决定是否需要 `ts_quantile` 外层。
3. **若 T7（多空配对）显著优于单侧模板** ⇒ 说明收益来自"形态方向差"而非"形态强度"，后续模板全部改为配对形式。
4. **若 T2（z-score）优于 T1（差分）** ⇒ 与 `insiders` 族"自身基线异常度唯一存活 / zscore ≫ rank"铁律一致，全族改用标准化而非差分。
5. **4 条跑完若全部 |S|<0.6** ⇒ 该数据集判死，PV 塔转向 `pv173`。

---

## 五、派发设置

```
region=GBR  universe=TOP700  delay=1
neutralization=INDUSTRY
decay=2 (高频日更数据；pv20 已实证 decay 10→2 提 S 22%)
truncation=0.05
nanHandling=OFF  maxTrade=OFF  pasteurization=ON  unitHandling=VERIFY
wait_for_completion=False
```

**decay 选 2 的理由**：形态分数日频更新、无预平滑（不同于 `adv20` 已是 20 日均值），信息半衰期短 ⇒ 高 decay 会抹掉形态形成的过程。参照 pv20 实证（decay 10→2，S +22%）。若 TO 超过 0.70 上限再回调到 4/6。

**注意**：`pattern_scores` 与 pv20 的族级档案（decay 10）不同，原因是数据更新频率不同——**「族级统一档案」的优先级低于「数据频率适配」**。

---

## 六、配额与塔位

- 本数据集所有模板 ⇒ **单塔 `GBR/D1/PV`**，不占任何双塔组合配额
- PV 塔当前实际 **0 条**，需 **2 条**
- 与估值族（FUND）塔位不同源 ⇒ **无塔混风险**

---

## 七、执行记录

### 批 29（`1JPAExeu650mbpuZSotaW64`，decay 2）

| # | 表达式 | alpha | S | F | TO | 2Y | SUB | SUB/S | dd | margin | fRA |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T7 | `subtract(ts_backfill(breakaway_gap_up_mean_simscore_lookback60, 22), ts_backfill(breakaway_gap_down_mean_simscore_lookback60, 22))` | 待回填 | — | — | — | — | — | — | — | — | — |

> 批 29 同日另派 pv20 的 `ts_av_diff` 骨架移植（见 `template_library_gbr_pv20_beta_term_structure.md` §11.5）。

---

## 八、批 29 首发实测 + 互相关突破（2026-10-30）

### 8.1 T7 缺口多空配对：S −1.15，方向与惯例相反

```
subtract(ts_backfill(breakaway_gap_up_mean_simscore_lookback60, 22),
         ts_backfill(breakaway_gap_down_mean_simscore_lookback60, 22))
```

| alpha | S | F | TO | 2Y | SUB | **SUB/S** | dd | margin | fRA |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `LLMO5Gwv` | **−1.15** | −0.57 | 20.07% | −0.91 | −0.82 | **0.713** | **52.42%** | −4.97bp | 4 |

**三条判读**：

1. **信号确实存在且强度过 1.0**（|S| 1.15），且 **SUB/S = 0.713 远过 0.4754 闸**（余量 50%）。按 §四 判据 2 ⇒ **触发铺满条件**。
2. **方向是均值回归，不是技术分析惯例的延续**。`up − down` 为负 ⇒ 反过来「看跌形态相似度 > 看涨形态相似度时，未来收益为正」。机理：向上缺口 = 隔夜过度反应 ⇒ 回补；向下缺口 = 超跌 ⇒ 反弹。**这是短期反转（Lehmann 1990 / Jegadeesh 1990），不是形态延续（Osler 2003 在 GBR 大盘股上不成立）**。
3. **质量差是硬伤**：F 0.57、margin 4.97bp（GBR 中位 11.9bp 的 42%）、dd **52.42%**。S 只是"看起来达标"。

**dd 52% 的第一性归因**：`subtract(up, down)` 是两个 [0,1] 分数之差，取值 [-1,1]，**量级随形态强度剧烈变化**。未做量级归一时，极端配对（up≈1 且 down≈0）会给出满仓信号，造成大回撤。**⇒ 加 `ts_quantile` 外层把差值转成历史分位，是降 dd 的第一手段**（批 30 在测）。

### 8.2 ★★ 互相关：pattern_scores 是唯一与估值族**负相关**的机制

```
compute_mutual_correlation([rKRQbPPE, j2YNnKOQ, bl67R9mK,
                            RRE06nEz, LLMO5Gwv, VkxKd1xV], threshold=0.7, years=4)
```

| | rKRQbPPE | j2YNnKOQ | bl67R9mK | RRE06nEz | LLMO5Gwv | VkxKd1xV |
|---|---:|---:|---:|---:|---:|---:|
| **rKRQbPPE** | 1 | 0.6964 | 0.0358 | 0.0686 | **−0.3059** | 0.1121 |
| **j2YNnKOQ** | 0.6964 | 1 | −0.0343 | 0.1284 | **−0.2811** | 0.1581 |
| **bl67R9mK** | 0.0358 | −0.0343 | 1 | 0.5433 | 0.2108 | 0.5561 |
| **RRE06nEz** | 0.0686 | 0.1284 | 0.5433 | 1 | 0.0713 | **0.9688** |
| **LLMO5Gwv** | −0.3059 | −0.2811 | 0.2108 | 0.0713 | 1 | 0.0582 |
| **VkxKd1xV** | 0.1121 | 0.1581 | 0.5561 | **0.9688** | 0.0582 | 1 |

```
max_mutually_below_subset      = [RRE06nEz, rKRQbPPE, j2YNnKOQ, bl67R9mK, LLMO5Gwv]
max_mutually_below_subset_size = 5
max_subset_exact               = true
```

**四条结构性结论**：

1. **可共存篮子从 2 条扩到 5 条**（`{rKRQbPPE, j2YNnKOQ}` → 上面 5 元组）。这是本会话最大的结构性进展——瓶颈从"只有 2 个正交机制"变成"5 个位置只填了 2 个"。
2. **`LLMO5Gwv` vs 估值族 = −0.31 / −0.28（负相关）**。负相关比"零相关"更有价值：它意味着 pattern_scores 与估值族在同一时点倾向于**反向持仓**，组合层面能对冲。
3. **`RRE06nEz` × `VkxKd1xV` = 0.9688 ⇒ 同一机制的两个 decay 版本，不可同时提交**。`VkxKd1xV` 的 S 更高（1.11 vs 0.91），**应作 `RRE06nEz` 的同机制替换**（不是新增）。
4. **`rKRQbPPE` × `j2YNnKOQ` = 0.6964**，卡在 0.7 线下 0.0036 —— 两条都要保留时不能动这两条的表达式，否则极易破线。

### 8.3 三条候选的"过闸差距"盘点（互相关已解决，只剩强度）

| alpha | 机制 | S | 需提升到 1.58 | SUB/S | 比值状态 | F | 需提升到 1.0 |
|---|---|---:|---:|---:|---|---:|---:|
| `rKRQbPPE` | 估值位移 EBITDA/EV | 2.48 | ✅ 已过 | 0.677 | ✅ | 2.22 | ✅ |
| `j2YNnKOQ` | 估值位移 EBIT/EV | 2.15 | ✅ 已过 | 0.656 | ✅ | 1.80 | ✅ |
| `bl67R9mK` | FUND 换手率 504 分位 | 1.39 | 差 14% | 0.345 | ❌ 差 27% | 1.01 | ✅ |
| `VkxKd1xV` | pv20 流动性 decay 2 | 1.11 | 差 42% | 0.586 | ✅ | 0.71 | 差 29% |
| `LLMO5Gwv` | pattern_scores 缺口配对 | **1.15**（翻符号） | 差 37% | **0.713** | ✅ 余量 50% | 0.57 | 差 43% |

**⇒ 瓶颈已经统一：5 个位置全部只剩"绝对强度不足"，没有一个卡在互相关或塔位上。**

---

## 九、批 30（进行中）：T7 refine 双路

| # | 设计 | 表达式 | 目的 |
|---|---|---|---|
| 1 | 翻转 + 252 日分位层 | `ts_quantile(subtract(ts_backfill(breakaway_gap_down_mean_simscore_lookback60, 22), ts_backfill(breakaway_gap_up_mean_simscore_lookback60, 22)), 252)` | ①直接取正号（等价翻符号）②`ts_quantile` 把 [-1,1] 差值转历史分位 ⇒ 压极端配对、降 dd |
| 2 | 换形态族（对称三角） | `ts_quantile(subtract(ts_backfill(avg_similarity_downward_symmetrical_triangle, 22), ts_backfill(avg_similarity_upward_symmetrical_triangle, 22)), 252)` | 测「均值回归」结论是否**跨形态族稳健**；若同向同强 ⇒ 机制普遍，可放心铺开 |

**判据**：
- 若任一条 S ≥ 1.4 且 F ≥ 0.9 ⇒ 该模板进候选池，继续扫窗口（120 日档）。
- 若两条 S 都在 1.0–1.3 ⇒ 机制成立但强度封顶，转「提高 margin」路线（换慢变形态 / 加长相似度平滑）。
- 若 `ts_quantile` 层把 S 显著压低（< 0.9）⇒ 说明收益来自极端配对而非整体分位，改用 `winsorize` 或 `rank` 压尾。

---

## 十、margin 4.97bp 的第一性诊断（记录，供后续所有形态类模板参考）

margin 低不是"信号弱"，而是**信号的时间结构太短**：
- 缺口是**事件型**（隔夜跳空 → 3~5 日内回补），持有期短、每次交易利润薄
- TO 20.07% 不算高，但 returns 仅 5% ⇒ **每单位换手的收益低**

**⇒ 提高 margin 的唯一正确方向是拉长信号半衰期**，候选手段：
1. 换 `lookback120` 档（信号本身更慢）
2. 用 `avg_similarity_*`（无窗口后缀的长期版本）替代 `*_mean_simscore_lookback60`
3. 对相似度差做 `ts_mean(..., 66)` 平滑（注意：pv20 实证分子平滑有害，但那是因为 `adv20` 已预平滑；形态分数是**未平滑**的原始分数，平滑层有信息增益）

**禁忌**：不要用提高 decay 的方式提 margin——decay 只改持仓权重不改信号半衰期，且已验证 decay 是 S 的杠杆。
---

## 十一、批 30 实测：`ts_quantile` 分位层把 dd 从 52% 压到 4.45%（2026-10-30）

| # | 设计 | alpha | S | F | TO | 2Y | SUB | SUB/S | dd | margin | fRA |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 缺口翻转 + 252 分位 | **`O0AKJXap`** | **1.28** | **0.62** | 22.57% | **0.63** | **0.85** | **0.664** | **4.45%** | 4.71bp | 3 |
| 2 | 对称三角翻转 + 252 分位 | `3qogjvLO` | 0.78 | 0.34 | 18.64% | 0.99 | 0.76 | 0.974 | 11.02% | 3.85bp | 3 |
| — | （对照）缺口配对无分位层 | `LLMO5Gwv` | −1.15 | −0.57 | 20.07% | −0.91 | −0.82 | 0.713 | 52.42% | −4.97bp | 4 |

### 11.1 `ts_quantile` 层带来的四项改善（同一信号，只加分位层）

| 指标 | 无分位层 | 有分位层 | 变化 |
|---|---:|---:|---:|
| S（绝对值） | 1.15 | **1.28** | **+11%** |
| F（绝对值） | 0.57 | **0.62** | +9% |
| **dd** | **52.42%** | **4.45%** | **−91.5%** |
| 2Y | −0.91 | **+0.63** | 由负转正 |
| SUB/S | 0.713 | 0.664 | −7%（仍过闸，余量 40%） |

**机理**：`subtract(up, down)` 取值 [-1,1] 且量级随形态强度剧烈变化；`ts_quantile(..., 252)` 把它转成「当前差值在自身一年的历史分位」⇒ **量级归一、极端配对不再给满仓**。dd 的 91.5% 降幅主要来自这里。

**⇒ 分位层是形态配对类模板的必需层，不是可选优化。**

### 11.2 对称三角族只有 0.78 ⇒ 均值回归效应**只在缺口类成立**

| 形态族 | 配对 S | 判读 |
|---|---:|---|
| 缺口（breakaway gap） | **1.28** | ✅ 反转成立 |
| 对称三角（symmetrical triangle） | 0.78 | ❌ 弱 |

**经济学解释**：缺口是**隔夜过度反应**（流动性冲击未在日内消化）⇒ 有回补的必然性；对称三角是**中性的持续形态**（方向由突破决定）⇒ 没有反转的必然性。**⇒ 后续模板应集中在缺口/跳空族，不要平均铺开到所有形态。**

### 11.3 `O0AKJXap` 逐年归因：2022 是唯一年度灾难

| 年份 | S | returns | dd | margin | TO | longCount |
|---|---:|---:|---:|---:|---:|---:|
| 2014 | 2.38 | 8.24% | 1.35% | 7.18bp | 22.95% | 420 |
| 2015 | 0.71 | 2.53% | 2.79% | 2.25bp | 22.48% | 479 |
| 2016 | 1.80 | 6.71% | 3.09% | 5.91bp | 22.70% | 490 |
| 2017 | 1.38 | 3.38% | 1.70% | 3.06bp | 22.09% | 516 |
| 2018 | 2.08 | 6.00% | 1.35% | 5.30bp | 22.65% | 474 |
| 2019 | 0.50 | 1.79% | 4.33% | 1.59bp | 22.54% | 458 |
| 2020 | 1.72 | 12.16% | 4.25% | 10.65bp | 22.84% | 420 |
| 2021 | 1.63 | 7.08% | 2.69% | 6.21bp | 22.83% | 409 |
| **2022** | **0.17** | **0.88%** | 4.45% | **0.80bp** | 22.18% | 430 |
| 2023 | 1.31 | 4.83% | 1.88% | 4.30bp | 22.46% | 408 |

**三条判读**：

1. **十年零负收益年**（最低 2022 的 +0.88%），年度 S 中位约 1.5。
2. **长期覆盖完全达标**：longCount 408–516 全程稳定，2014→2023 无衰减 ⇒ 满足「近十年都要有数据」硬门槛。
3. **2022 是唯一灾难**（S 0.17、margin 0.80bp）。2Y（2022+2023 窗口）= 0.63 完全由这一年拖累。

**2022 失效的第一性归因**：2022 是 GBR 国债危机（Truss mini-budget）年，市场处于极端波动。**高波动期缺口由真实信息驱动而非流动性 ⇒ 不反转**。这是结构性弱点，不是调参能解决的——只能靠拉长信号半衰期（120 日窗口 / 平滑）来稀释单年冲击，或做波动率条件化。

**⇒ 2Y 从 0.63 到 1.58 需 +151%，是当前最大硬伤，也是批 31/32 的全部目标。**

### 11.4 互相关：加 `ts_quantile` 层后正交性略降但仍远低于 0.7

```
compute_mutual_correlation([rKRQbPPE, j2YNnKOQ, bl67R9mK, O0AKJXap], threshold=0.7, years=4)
→ max_mutually_below_subset = [rKRQbPPE, j2YNnKOQ, bl67R9mK, O0AKJXap]
  size = 4, max_subset_exact = true, pairs_over_threshold = []
```

| `O0AKJXap` 对 | 相关 | 与无分位版（`LLMO5Gwv`）对比 |
|---|---:|---:|
| `rKRQbPPE` | 0.3671 | −0.3059（正交性下降） |
| `j2YNnKOQ` | 0.3951 | −0.2811（正交性下降） |
| `bl67R9mK` | **−0.1725** | 0.2108（**改善**） |

**权衡判定**：分位层让估值族相关从负转正（−0.31 → 0.37），但换来 dd −91.5%、S +11%、2Y 由负转正。**0.37/0.40 远低于 0.7，代价可接受**。

### 11.5 当前 `pattern_scores` 最优候选的过闸差距

| 指标 | `O0AKJXap` | 闸门 | 差距 |
|---|---:|---:|---:|
| S | 1.28 | 1.58 | 差 **23%** |
| F | 0.62 | 1.0 | 差 **38%** |
| **2Y** | **0.63** | 1.58 | 差 **151%** ← 最大硬伤 |
| SUB/S | 0.664 | 0.4754 | ✅ 余量 40% |
| TO | 22.57% | 0.70 | ✅ 余量 3.1× |
| dd | 4.45% | — | ✅ 本会话最低之一 |

---

## 十二、批 31（进行中）：拉长半衰期以压低 2022 单年冲击

| # | 设计 | 表达式 | 目的 |
|---|---|---|---|
| 1 | 120 日窗口配对 | `ts_quantile(subtract(ts_backfill(common_gap_down_mean_simscore_lookback120, 22), ts_backfill(common_gap_up_mean_simscore_lookback120, 22)), 252)` | 换 `common_gap` 族 + `lookback120`（信号本身更慢）⇒ 稀释 2022 单年冲击 |
| 2 | 66 日平滑配对 | `ts_quantile(ts_mean(subtract(...breakaway_gap...60...), 66), 252)` | 对相似度差做 66 日平滑 ⇒ 降噪、拉长持有期、提 margin |

**判据**：
- 若任一条 **2Y ≥ 1.0** ⇒ 半衰期方向正确，批 32 继续加长（`ts_mean(...,252)` 或 `lookback120 + 平滑` 叠加）。
- 若两条 2Y 仍 < 0.8 ⇒ 2022 冲击是结构性的，转「波动率条件化」路线：`divide(<分位信号>, ts_std_dev(<分位信号>, 66))`（同单位相除，合规）。
- 若两条 S 掉到 < 1.0 且 2Y 无改善 ⇒ 该机制在 GBR 的上限确认，封存 `O0AKJXap` 为储备候选。

**注意**：本条 2 的 `ts_mean` 平滑**不违反**「pv20 分子平滑有害」的先例——`adv20` 已是 20 日均值（预平滑），而形态相似度是**未平滑的原始分数**，平滑层在这里有信息增益。
---

## 十三、批 31 结论（已完成）+ 批 34 方向性突破

### 13.1 批 31 双灭，但给出全会话最强的一年后置证据

| alpha | 设计 | S | F | TO | 2Y | SUB | dd | fRA |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `VkxKxJ58` | `common_gap` down−up，`lookback120`，252 分位 | **−1.10** | −0.68 | 12.95% | **−1.44** | −0.83 | 51.67% | 4 |
| `Xg9X96ez` | breakaway 差值 + 66 日 `ts_mean` 平滑 | 0.60 | 0.26 | 7.85% | 0.35 | — | 7.62% | 3 |

**`VkxKxJ58` 逐年 `get_alpha_yearly_stats` 实读（10/10 年全部同号，全负）**：

| 年 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sharpe | −1.52 | −1.92 | −0.65 | −0.68 | −1.15 | −2.57 | −0.70 | −0.94 | −0.94 | −2.28 |

二项分布 p ≈ 2⁻⁹ ≈ 0.002 ⇒ **极强稳定性证据，不是噪声**。持仓 397–521 全程稳定。

⇒ 按「Sharpe 线性于收益序列符号」，翻转即精确取反。`dd 51.67%` 是累积负 PnL 单调下行的假象，**翻转后（实测 `RRE0EArj`）dd 仅 5.31%**。

### 13.2 ★★★ 两个缺口族方向相反（第一性机制确认）

| 数据集 | 族 | 正确方向 | 机理 | 来源 |
|---|---|---|---|---|
| `pattern_scores` | `common_gap` | **`up − down`（延续）** | 普通缺口由流动性不足导致，流动性持续不足 ⇒ 价格漂移延续 | Amihud 2002 |
| `pattern_scores` | `breakaway_gap` | **`down − up`（反转）** | 突破缺口由消息驱动、隔夜过度反应 ⇒ 回补 | Lehmann 1990 / Jegadeesh 1990 |
| `continuation_score` | gap 全族 | **`down − up`（反转）** | 同 breakaway 机理 | 批 34 实测 |

**与经典技术分析定义相反**（经典：common 回补、breakaway 延续）。这是本会话最重要的机制发现，且三族方向互不相同 ⇒ **篮子内互相关天然低**。

### 13.3 ★★★ 批 34：`continuation_score` 首次实测（SECTOR / decay 20 / trunc 0.06）

| alpha | 字段 | S | F | TO | 2Y | SUB | dd | margin | 翻转后 SUB/S |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `vR1aA8R3` | **avg** 统计量配对 `up − down` | **−1.37** | −1.04 | 11.21% | **−1.50** | −0.55 | 73.99% | −12.79bp | **0.401** |
| `j2YNav5k` | **peak** 统计量配对 `up − down` | −1.06 | −0.72 | 11.35% | −0.91 | −0.40 | 59.08% | −10.07bp | 0.377 |

**翻转后（=`RRE0EArj` 级别的候选）**：

| alpha | S | F | 2Y | SUB | SUB/S | margin | risk_neut | 塔 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `vR1aA8R3` 翻转 | **1.37** | **1.04** | **1.50** | 0.55 | 0.401 | **12.79bp** | 0.36 | GBR/D1/PV ✅ |
| `j2YNav5k` 翻转 | 1.06 | 0.72 | 0.91 | 0.40 | 0.377 | 10.07bp | — | GBR/D1/PV ✅ |

**两条都是新 id（未撞已有 alpha）** ⇒ 该方向此前无人做过，是真新机制。

**`vR1aA8R3` 翻转版是本会话最强 PV 候选**：F 已过闸（1.04 ≥ 1.0）、2Y 仅差 5%、S 差 13%、margin 12.79bp 高于 GBR 中位 11.9bp。**唯一硬卡是 SUB/S 0.401 vs 0.4754（差 15.6%）**。

**长期覆盖已核实**：`longCount 448 + shortCount 452`，2014–2023 全期 ⇒ 满足「近十年都有数据」。

### 13.4 ★★ 平台事实纠错：SUB 闸对负 Sharpe alpha 的判法不同

`vR1aA8R3` 的 S = −1.37、SUB = −0.55，而 `LOW_SUB_UNIVERSE_SHARPE` 却列在 **pass**。
推导：limit 口径是 `sub_sharpe >= 0.4754 × sharpe`（**带符号**），−0.55 >= −0.6514 成立 ⇒ pass。
⇒ **负 Sharpe alpha 的 SUB 闸几乎自动通过，不能据此认为「SUB 安全」**；翻转成正向后 0.55 < 0.6514 立刻 fail。
**判读纪律：任何负 Sharpe 候选的 SUB 闸结论一律作废，必须按翻转后的正数重算。**

### 13.5 ★★ 论坛「peak 统计量强 10 倍」在 GBR 不成立

论坛帖 `43298855144855`（ASI）称 `peak` 统计量 S 1.27 vs `average` 0.37（强 10 倍）。GBR 实测相反：
`avg` 翻转后 S **1.37** > `peak` 翻转后 S **1.06**（avg 强 29%）。
⇒ **统计量强弱是区域属性，不可跨区套用**。GBR 大盘股（TOP700）形态更平滑、噪声日少 ⇒ 均值类统计量信息利用率更高，极端时刻（peak）反而被单日异常主导。

### 13.6 `pattern_scores` 的 gap 字段全景（`get_datafields` 实读，504 字段中 gap 相关 ~200 条）

**共四个命名族，全部 PV、coverage 0.9747–0.9998**：

| 族 | 命名范式 | 统计量 | 窗口形态 | 拥挤度代表 |
|---|---|---|---|---|
| A. common gap | `common_gap_{up,down}_{stat}_simscore_lookback{60,120}` | mean/median/min/max/q95/std/dynamic/adaptive | 60 / 120 交易日 | up120 mean **u70/a84**（最热） |
| B. breakaway gap | `breakaway_gap_{up,down}_{stat}_simscore_lookback{60,120}` | 同上 | 60 / 120 交易日 | down60 mean **u76/a92**（最热） |
| C. "typical" gap | `regular_{upward,downward}_gap_{stat}_similarity` | mean/median/min/max/q95/std/dynamic | 无窗口后缀 | 多数 **u0/a0** |
| D. "strong" gap | `{upward,downward}_gap_break_{stat}_similarity` | mean/median/min/max/dynamic | 无窗口后缀 | max u12/a20 |
| E. 长窗口 | `simscore_common_gap_{up,down}_{avg,min,median}_40w`、`simscore_break_gap_{up,down}_{max,q95}_40w` | avg/min/median/max/q95 | **40 周（≈200 日）** | **u0–3 / a0–3（全未开发）** |

**E 族（40 周）的对称可配对**：`simscore_common_gap_up_min_40w`(u1/a1) + `simscore_common_gap_down_min_40w`(u1/a1)；`simscore_common_gap_up_median_40w`(u0/a0) + `simscore_common_gap_down_median_40w`(u1/a1)。
⇒ **40 周长窗口 × min/median 统计量是下一个零拥挤模板方向**（`min` = 形态匹配的**长期下限**，经济含义不同于均值：反映结构性倾向而非当期状态）。

**其它未开发高价值字段**：`min_similarity_upward_common_gap_120`（**u32/a40**，min 统计量里异常热门）、`simscore_break_gap_down_max_40w`(u3/a3)、`regular_*_gap_*`（几乎全 u0/a0）。