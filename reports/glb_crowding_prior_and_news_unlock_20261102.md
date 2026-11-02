# GLB 拥挤度先验定桩 + NEWS 单塔解锁（2026-11-02）

> 一轮里同时发生三件事：**第 6 颗候选确认通过**、**prod 墙的根因被识别为 alphaCount 而非设置**、**PV 塔判死结论被限定**。
> 全部结论可追溯到本轮 MCP 实测返回值，不使用估计值。

---

## 一、最重要的新认知：`alphaCount` 是 prod 墙的第一预测因子

本轮用 `get_datasets(region="GLB", universe="MINVOL1M", delay=1)` 拉到 **138 个数据集**的完整拥挤度账。把它和已实测的 prod 结果对齐后，规律非常干净：

| 数据集 | alphaCount | 实测结果 |
|---|---:|---|
| `techindi_model` | **178404** | 全族 0.76–0.87 |
| `pv1` | **519971** | （PV 主数据集，PV 单塔 0.8677 的主因） |
| `model110` | 202982 | — |
| `model38` | 145908 | — |
| **`dl_riskfree_returns`** | **22585** | **OTHER 裸信号 prod 地板 0.76–0.87** ❌ |
| `earnings3` | 9922 | `ern3_pre_interval` 门控 **0.7204 / 0.7599** ❌ |
| `sentiment21` | 8672 | 但 `snt21_2neg_conf_low_394` 门控 **0.6585** ✅ |
| `analyst10` | 7521 | — |
| `institutions6` | 6268 | — |
| `risk70` | 62320 | RISK 全族 0.80–0.94 ❌ |
| **`intraday_pv_feats`** | **4595** | **PV 单塔 `kqNrmA9g` 0.8677** ❌ |
| **`fundamental44`** | **4081** | 门控 `fnd44_jones_cf_accruals` **0.5846** ✅ |
| `analyst11` | 4992 | w168 ESG 指标层塌缩 ❌ |
| `risk60` | 5583 | 门控 `rsk60_crowding` **0.6385** ✅ |
| **`news73`** | **337** | **未测（极低拥挤）** |
| **`news48`** | **298** | **未测（极低拥挤）** |
| **`news36`** | **336** | **未测** |
| **`news38`** | **138** | **未测** |
| **`news59`** | **168** | **未测** |
| **`news29`** | **242** | **未测** |
| **`news46`** | **289** | **未测** |

### 判读规则（本轮定桩）

1. **信号腿的 alphaCount 越高，prod 墙越硬**。`dl_riskfree_returns`(22585) / `intraday_pv_feats`(4595) 是目前两个已证死的信号腿数据集，两者都是数万～数千级。
2. **门控腿不受此约束**——`fundamental44`(4081) / `risk60`(5583) / `sentiment21`(8672) 三个高拥挤数据集作**门控**时全部给出 0.58–0.66 的干净 prod。原因是门控腿经 `trade_when` 只做持仓稀疏化，不与既有 alpha 的 PnL 共线。
3. **因此「高 alphaCount」在信号腿位是死亡预判，在门控腿位是中性的。** 这条区分是本轮最有操作价值的一句。

---

## 二、低 alphaCount 有两种，必须区分（`pv98` 陷阱）

不能把「alphaCount 低」直接当机会。本轮拆了 `pv98`（Intraday Tick Data and Statistics，21 字段 / cov 1.0 / alphaCount **766**）：

```
全部 21 个字段 = {close, high, low, open, volume, vwap, market_capitalization}
              × {lagged_0, lagged_1, lagged_2}
```

这是 `pv1`（24 字段，alphaCount **519971**）的**同期 OHLCV 冗余镜像**——没有引入任何新信息，只是把同一批价量数据换了 lag 排列。它 alphaCount 低的真实原因是**挖不出东西**，而不是没人发现。

**⇒ 判据**：低 alphaCount 要通过两道检验才算机会——
- **语义非冗余**：字段不与其他高拥挤数据集同构（对比字段名集合，不是看描述措辞）；
- **引入新维度**：带平台自身没有的信息类型（如 `nws48_nip` 的「未来两小时市场冲击预测」是前瞻量，`nws48_ens` 的「事件新颖度」是信息消化度）。

`pv98` 两道全败 ⇒ **弃**。这条与既有记忆「低拥挤度在有结构缺陷的数据集上是警告信号而非机会信号」（EUR model354 聚合面板教训）同源，但给出了**正向判据**。

---

## 三、PV 塔判死结论必须限定：只对 `intraday_pv_feats` 成立

上一轮 `kqNrmA9g` prod=0.8677 让我把「PV 单塔」整体判死。拥挤度账出来后这个推广是**错的**：

| PV 数据集 | alphaCount | 状态 |
|---|---:|---|
| `pv1` | 519971 | 极高拥挤 |
| `pv13` | 11645 | 高 |
| `pv37` | 8505 | 高 |
| `pv96` | 7134 | 高 |
| **`intraday_pv_feats`** | **4595** | **← `kqNrmA9g` 用的就是这个** |
| `pv53` | 2469 | 中 |
| `pv47` | 1547 | 低 |
| `pv30` | 895 | 低 |
| `pv98` | 766 | 低但冗余（见上） |
| `pv106` | 612 | 低 |
| `pv17` | 554 | 低 |
| `pv29` | 499 | 低 |
| `pv173` | 254 | 低 |
| `pv72` | 79 | 低但 cov 0.2565 |
| `pv149` | 38 | 仅 1 字段 |

**`kqNrmA9g` 用的是 `mean_high_price_return_30m_pre_close_2`（pre_close 30m 族），不是 `pv98`/`pv106`/`pv173`。** 所以：

- ✅ 「PV pre_close 30m 族单塔死」成立（`intraday_pv_feats` 4595）
- ❌ 「PV 塔整体死」**不成立** —— `pv106`(612) / `pv173`(254) / `pv47`(1547) 从未被测试

**⇒ 死路条目 `GLB-PV-SINGLE-TOWER-PROD-08677-20261102` 的作用域需收窄到 `intraday_pv_feats` 的 pre_close 30m 族**，不能覆盖 PV 塔全部数据集。PV 塔差 1 颗点亮，正确动作是换低拥挤 PV 数据集，而不是放弃 PV 塔。

---

## 四、单塔 alpha 允许同塔不同数据集 —— 不占组合配额的关键

塔混约束的真实形态：
- `{PV, MODEL, OTHER}` 三者间两两组合 ✗（含 PV×PV）
- trio 塔 × 非 trio 塔 允许，但组合名总量 ≤5（**已满 5/5**）
- 非 trio × 非 trio 组合数不限，只受「每组合 ≤3」
- **`len(combo)==1` 的单塔不占任何配额**

由此推出一条此前未利用的路径：**单塔 alpha 的信号腿与门控腿可以来自同一塔的两个不同数据集**。
例：`news73`（信号）+ `news48`（门控）→ 塔集合 = `{NEWS}` → 单塔 → **零配额消耗**。

这同时解决了既有死路 `GLB-PURE-SINGLE-TOWER-DEAD-20261028` 指出的问题——
那条死路说「门控与信号同集同源 ⇒ 共线 ⇒ 信号被打平」。**但只要两腿分属同塔的不同数据集，同源问题就消失**（`news73` 是 Dow Jones 文章级情绪、`news48` 是实体级事件情绪，信息加工路径不同）。

⇒ **非 trio 单塔（NEWS / SENTIMENT / EARNINGS / ANALYST / FUNDAMENTAL / INSTITUTIONS）是当前唯一不受配额限制的扩量主路径。**

---

## 五、第 6 颗确认：`xArnqeAw` prod = 0.6335

```
trade_when(rank(ts_mean(snt21_2neg_conf_low_394, 22)) > 0.7,
           signed_power(subtract(group_rank(probability_label1_2quantile_20day_ohlcv_img, country), 0.5), 0.5),
           rank(ts_mean(snt21_2neg_conf_low_394, 22)) < 0.6)
```

| 指标 | 值 |
|---|---|
| sharpe / fitness | 2.74 / 1.42 |
| turnover / 2Y | 21.24% / 2.36 |
| sub-universe | 1.87 |
| **prod** | **0.6335 ✅** |
| 耗时 | 455s（刷新历史 436s） |

prod 直方图：`n_total=914864`；`n[0.6,0.7)=2`；**`n[0.7,0.8)=0`**；`n[0.8,0.9)=0`；`n[0.9,1.0)=0` ⇒ 干净型，无钉子。

**⇒ 确认可提交库存升到 6 颗。**

---

## 六、6 颗互相关全过（平台 self 闸的前置）

`compute_mutual_correlation(threshold=0.7, years=4)`，1023 个日收益点，本地计算：

| 候选 | 塔组合 | S | F | TO | 2Y | **prod** |
|---|---|---:|---:|---:|---:|---:|
| `QPvJ6KVw` | RISK+OTHER | 3.19 | 1.59 | 28.97% | 3.43 | 0.6385 |
| `npv9WLVE` | RISK+OTHER | 3.08 | 1.42 | 60.83% | 3.19 | 0.6638 |
| `RRE3O8r1` | FUND+OTHER | 2.89 | 1.73 | 16.02% | 2.13 | 0.6479 |
| `d5WqeQbx` | FUND+OTHER | 2.71 | 1.43 | 7.55% | 2.68 | 0.5846 |
| `j2Yg2q9j` | OTHER+SENT | 2.73 | 2.02 | 14.69% | 2.85 | 0.6585 |
| **`xArnqeAw`** | **OTHER+SENT** | **2.74** | **1.42** | **21.24%** | **2.36** | **0.6335** |

- `max_pair` = `RRE3O8r1 ↔ d5WqeQbx` **0.6741**（余量 0.0259）
- 第二紧 = `j2Yg2q9j ↔ xArnqeAw` **0.6555**（余量 0.0445）
- `pairs_over_threshold = []`、`all_below_threshold = true`
- `max_mutually_below_subset_size = 6`、`max_subset_exact = true` ⇒ **6 颗可整批提交**

⚠ 但这是**本地 PnL 相关**，平台 `SELF_CORRELATION` 是另一个口径。两对紧邻的必须**相邻提交并立即读回平台 self**。

---

## 七、w170 已就绪：NEWS 单塔 10 个结构互异模板

按硬约束（每波 ≥10 个结构互异模板），已设计并通过两道预检：**语法 10/10 valid**、**字段 10/10 存在**（`unknown_fields=[]`、`vector_fields=[]`）。

信号腿取 `news48`（alphaCount **298**，字段级 4–33），辅腿取 `news73`（337）。同塔不同集 ⇒ 单塔、零配额、非共线。

| # | 骨架 | 矩 | 表达式 |
|---|---|---|---|
| T1 | 水平反转 | 水平 | `-group_zscore(ts_mean(vec_avg(nws48_nip), 5), country)` |
| T2 | 一阶差分动量 | 一阶 | `group_zscore(ts_delta(vec_avg(nws48_qcm), 5), country)` |
| T3 | 二阶波动惩罚 | 二阶 | `-group_rank(ts_std_dev(vec_avg(nws48_ssc), 22), country)` |
| T4 | 时序分位 | 分位 | `group_zscore(ts_rank(vec_avg(nws48_ens), 66), country)` |
| T5 | 协方差背离 | 协方差 | `-group_zscore(ts_covariance(vec_avg(nws48_ssc), vec_avg(nws48_aes), 22), country)` |
| T6 | 比值强度 | 比值 | `group_zscore(divide(vec_avg(nws48_nip), add(vec_avg(nws48_relevance), 1)), country)` |
| T7 | 条件门控 | 条件 | `trade_when(rank(ts_mean(vec_avg(nws48_ens), 22)) > 0.7, group_zscore(vec_avg(nws48_nip), country), 0)` |
| T8 | 时序 z 分数 | 时序标准化 | `group_zscore(ts_zscore(vec_avg(nws73_globalsent_uncertaintyscore), 66), country)` |
| T9 | 排名差分 | 排名一阶 | `group_zscore(ts_delta(rank(vec_avg(nws48_vea)), 22), country)` |
| T10 | 极值差 | 极值离散 | `group_rank(subtract(vec_max(nws73_globalsent_fearscore), vec_min(nws73_globalsent_fearscore)), country)` |

**字段经济含义**（这决定模板不是换参数）：
- `nws48_nip` = 新闻对未来**两小时**市场冲击的预测分（0–100）→ 唯一的前瞻量
- `nws48_ens` = 事件新颖度（0–100），24 小时窗口内该故事有多新 → 信息消化度
- `nws48_qcm` = 多分类器情绪（聚合最相关公司）
- `nws48_ssc` = 故事级整体情绪（0–100）
- `nws48_aes` = 91 日滚动窗口正事件占比 → 长期基调
- `nws48_relevance` = 实体与故事相关度（0–100）
- `nws48_vea` = 91 日非中性事件计数 → 报道密度
- `nws73_globalsent_uncertaintyscore` / `fearscore` = 文章级不确定 / 恐惧分数

**刻意避开的两件事**——
1. 论坛实证「情绪差模板出货一般」⇒ **不用 `sent_positive − sent_negative` 型差构造**，改用比值（T6）、协方差（T5）、极值差（T10）。
2. 论坛实证 `ts_covariance(情绪A, 情绪B, N)` 是有效骨架 ⇒ 采纳为 T5。

设置沿用胜出格：`MINVOL1M / d1 / decay=10 / FAST / trunc=0.08 / nanHandling=OFF / maxTrade=OFF / maxPosition=OFF`。

---

## 八、修订后的 20 颗算术

**塔位现状（GLB/D1）**：`pv 2 / model 3 / other 3 / risk 1 / institutions 1`，其余 9 座 0，点亮门槛 = 3 颗/塔。

| 路径 | 不占配额？ | 单波产能 | 优先级 |
|---|---|---|---|
| 非 trio 单塔（NEWS / SENT / EARN / ANALYST / FUND / INST） | ✅ 是 | 3 颗/塔 | **主路径** |
| 非 trio × 非 trio 双塔 | ✅ 组合数不限 | ~3 颗/组合 | 次路径 |
| trio × 非 trio | ❌ 5 名已满 | 仅剩 6 席 | 收尾（w169 在打） |
| PV/MODEL/OTHER 单塔 | ✅ 是 | — | 三条已证死（受数据集限定） |

6 颗确认 + 20 颗目标 ⇒ **还差 14 颗**。按非 trio 单塔 3 颗/塔计，只需 **5 座塔**（NEWS / SENTIMENT / EARNINGS / ANALYST / FUNDAMENTAL 或 INSTITUTIONS 中的任意 5 座），且**全部零配额消耗**。

⇒ **20 颗在算术上第一次真正可达，瓶颈从「配额」转成「回测吞吐 + 每日 4 颗提交配额」。**

---

## 九、未完成 / 待裁定

1. **提交授权未获（第 6 次）** —— 6 颗确认件一颗未提交，日配额 4 颗/天。
2. **`mLoqmkd5` prod 在测**（第 7 颗，`INST+OTHER`，`investability_ratio=0.4565` 容量衰减过半）。
3. **w169 的 8 条**已跑 523s 仍未出 children，收批后需做门控清洗度归因。
4. **w169 组合配额超配** —— 其 FUND+OTHER 打 2 条（现有 2 ⇒ 将成 4，超 1）、OTHER+SENT 打 2 条（现有 2 ⇒ 将成 4，超 1）。收批后只取前 2 名。
5. **`pv106` / `pv173` / `pv47` 未测** —— PV 塔点亮的真实希望，需单独开波。
6. **`leading gap` 是否除名** —— `QPvJ6KVw` / `npv9WLVE` 2014 空窗、2015 覆盖薄（363 / 50 只）。
