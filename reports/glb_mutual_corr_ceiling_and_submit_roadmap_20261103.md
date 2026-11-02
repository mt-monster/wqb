# GLB 战役状态与提交路线图（2026-11-03 22:40）

> 结论先行：**当前机制下可提交上限是 10 颗，不是 20 颗。**
> 卡点不是候选数量，而是 **signal 腿的互相关性** —— 15 颗候选里有 6 对互相关 ≥0.70（最高 0.9864），
> 平台 `SELF_CORRELATION` 比的是「与已提交池的最大相关」，所以先提的一颗会把同骨架的另一颗顶到 >0.70。

---

## 1. 互相关天花板（本轮最重要发现）

15 颗候选（13 READY + `0mYE53l8` + `pwdl3OPx`）的两两互相关矩阵：

### 成对 ≥0.70（6 对，必有一方不能提）

| 相关 | A | B | 根因 |
|---:|---|---|---|
| **0.9864** | `9qxR097o` | `N1NO9nRe` | 同 signal 腿 `single_bucket_20day_return_estimate_ohlcv_img_2`，gate 仅换 ern3 字段名 |
| **0.8526** | `xArnqeAw` | `Xg9rMdvl` | 同 gate `snt21_2neg_conf_low_394`；signal 腿换了两条但这两条 OTHER 腿彼此高相关 |
| **0.8503** | `YP1rzw2J` | `RRE3O8r1` | 同 signal 腿 `single_bucket_5day_return_estimate_ohlcv_img` |
| **0.8065** | `npv9WLVE` | `qML1x6vK` | 表达式几乎一字不差（`ts_mean` 窗口 5 vs 22 + decay 差异） |
| **0.7815** | `j2Yg2q9j` | `Xg9rMdvl` | 同 gate，signal 腿 `probability_label1_2quantile_20day` vs `single_bucket_20day_2` |
| **0.7435** | `YP1rzw2J` | `d5WqeQbx` | 同 signal 腿 `single_bucket_20day_2` |

### 成对 [0.60, 0.70)（3 对，可同提但余量仅 0.024–0.045）

`QPvJ6KVw↔qML1x6vK` 0.6762 ｜ `RRE3O8r1↔d5WqeQbx` 0.6741 ｜ `xArnqeAw↔j2Yg2q9j` 0.6555

### 最大互斥子集 = 10

```
bl6qldJ6  pwdl3OPx  qML1x6vK  d5WqeQbx  xArnqeAw
RRE3O8r1  leA0X7lA  j2Yg2q9j  9qxR097o  QPvJ6KVw
```

被排除（不可与上述同提）：`YP1rzw2J` `Xg9rMdvl` `N1NO9nRe` `npv9WLVE`

**根因**：互相关由 **signal 腿**主导，不由 gate 塔主导。把 gate 换成完全不同的数据集
（FUNDAMENTAL / RISK / SENTIMENT / EARNINGS / ANALYST）后，同 signal 腿的两颗仍落在 0.74–0.99。
库存 15 颗实际只压在 5–6 条生产性 OTHER 腿上是：
`single_bucket_20day_2` / `single_bucket_5day` / `probability_label1_2quantile_20day` /
`probability_label1_2quantile_60day` / `predicted_third_quantile_one_day` / `predicted_fourth_quantile_ten_day`

---

## 2. 三日提交路线图（每日额度 4 颗，全互斥 <0.70）

| 日 | 提交 | 塔位变化 | prod 余量 |
|---|---|---|---|
| **第 1 日** | `leA0X7lA` `RRE3O8r1` `d5WqeQbx` `bl6qldJ6` | FUNDAMENTAL 0→3 **点亮** ｜ SENTIMENT 0→1 | 0.6022 / 0.6479 / 0.5846 / 0.5421 |
| **第 2 日** | `xArnqeAw` `j2Yg2q9j` `9qxR097o` `QPvJ6KVw` | SENTIMENT 1→3 **点亮** ｜ EARNINGS 0→1 ｜ RISK 1→2 | 0.6335 / 0.6585 / 0.6502 / 0.6385 |
| **第 3 日** | `qML1x6vK` `pwdl3OPx` | RISK 2→3 **点亮** ｜ ANALYST 0→1 | 0.6867 / 待测 |

- 全程两两互相关 <0.70（最低余量 0.0238 @ `QPvJ6KVw↔qML1x6vK` 0.6762）
- 三日合计 **10 颗**，点亮 **3 座塔**（FUNDAMENTAL / SENTIMENT / RISK，乘数各 1.4）
- 十年覆盖：`leA0X7lA` `RRE3O8r1` `d5WqeQbx` `bl6qldJ6` `xArnqeAw` `j2Yg2q9j` `9qxR097o` `pwdl3OPx` 全 OK；
  `QPvJ6KVw` `qML1x6vK` 2014 `longCount=0`（`rsk60_crowding` 该年才起，属字段特性，非连续空窗）

### 已判不合格 / 待破墙

| alpha | 状态 | 原因 |
|---|---|---|
| `0mYE53l8` | prod **0.7573** FAIL | [0.7,0.8) 内 7 个点，浅偏中；`probability_label1_2quantile_60day` 是 n=10 的重挖腿 ⇒ 进窗口谷破墙队列 |
| `YP1rzw2J` `Xg9rMdvl` `N1NO9nRe` `npv9WLVE` | 合格但互斥被排除 | 与已选件 ≥0.74，只能作替补（若前面某颗提交失败可顶替） |
| `gJeMLdoO` | DEAD | S 0.06 / 6 项 FAIL；ANALYST 门控用 `ts_mean` 原始水平失败 |
| `0mYl5r11` | prod **0.7318** FAIL | [0.7,0.8) 内仅 2 个点、max<0.8 = 浅钉 ⇒ 破墙队列（非判死） |
| INSTITUTIONS 整族 | DEAD | `6XdRKZoO` prod 0.8334，[0.7,0.8) 内 36 个点 |

---

## 3. 塔位账（提完 10 颗后）

| 塔 | 基线 | 提交后 | 门槛 | 状态 |
|---|---:|---:|---:|---|
| FUNDAMENTAL | 0 | 3 | 3 | **点亮** |
| SENTIMENT | 0 | 3 | 3 | **点亮** |
| RISK | 1 | 3 | 3 | **点亮** |
| EARNINGS | 0 | 1 | 3 | 差 2；**结构性不可点亮** |
| ANALYST | 0 | 1 | 3 | 差 2 |
| INSTITUTIONS | 1 | 1 | 3 | 判死 |
| NEWS / MACRO / SOCIALMEDIA / INSIDERS | 0 | 0 | 3 | 各仅 1 条候选在测 |

### EARNINGS 塔为什么点不亮

该塔只有 **2 条独立 signal 腿**（`single_bucket_5day` / `single_bucket_20day_2`），
4 颗候选两两分组后各只能提 1 颗（`9qxR097o↔N1NO9nRe` 0.9864、`0mYl5r11↔d5W0RQZv` 同腿）
⇒ 最多 2 颗，永远差 1 颗。**除非先找到第三条独立的 EARN 可用信号腿。**

---

## 4. 本轮新增机制：w187 `other455` 关系图嵌入（纯 OTHER 单塔，零组合配额）

**经济先验**：Cohen & Frazzini (2008)《Economic Links and Predictable Returns》——
客户/供应商经济关联可预测收益；海通量化的供应链网络因子亦用同一思路。
`other455` 是 **Node2Vec 关系图嵌入的 PCA 得分**（300 MATRIX）+
聚类标签（1200 GROUP），覆盖 4 类关系（competitor / customer / partner / relation）×
5 种嵌入配置（`n2v_p10_q200_w1-5` / `n2v_p10_q50_w1-5` / `n2v_p50_q200_w1-5` /
`n2v_p50_q50_w1-5` / `roam_w1-5`）× 3 个主成分。**全库零测试、覆盖 0.83–0.97。**

- **为什么它可能破局**：机制与现有收益预测模型族完全不同（网络位置 vs 收益预测），
  且是**纯单塔 OTHER ⇒ 不消耗任何组合配额**（当前 trio×非trio 已用满 5 类）
- **分组轴多样性**：可直接用 `other455` 自己的 `kmeans_cluster_{5,10,20}` /
  `pca_fact{K}_cluster_{5,10,20}` 作 `group_rank` 轴（社区帖确认 group 字段可作轴）

12 个结构互异模板（水平 / 双主成分价差 / 簇内相对位置 / 簇内位置时序变化 /
跨关系类型分歧 / 嵌入窗口漂移 / 算法分歧 roam-vs-n2v / 二阶不稳定度 / 绝对载荷 /
簇内对称几何 / 第三主成分残余 / 长窗时序秩），全部通过：

- 括号平衡 ✓ ｜ `op_arity` 零错误 ✓ ｜ 幽灵算子零命中 ✓ ｜ 禁用分组轴零命中 ✓
- 字段存在性 21/21（全 `other455`，MATRIX + GROUP）✓ ｜ DB 精确查重零命中 ✓
- 平台 `validate_expressions`：`valid: true`、`unknown_fields: []` ✓

已派发 3 条（后续 9 条按并发槽释放逐条补发）：`uSRe33z1`(T1) `GipWe2Ju`(T2) `1Ftid1bz`(T3)

---

## 5. 通往 20 颗的唯一路径

```
10 颗（现有库存，三日提完）
  + 需再找 ~10 条「与已提交 10 颗互相关 <0.70」的独立 signal 腿
  = 20 颗
```

**后续波次的唯一 KPI 是「新 signal 腿的独立性」，不是「新候选数」。**
在同一批 OTHER 腿上继续换 gate 是零收益动作（本轮 6 对 ≥0.70 即其代价）。

新腿候选池（按优先级）：

1. `other455` 关系图嵌入 —— 已在测（w187）
2. `techindi_model` 1810 个未测字段（`likelihood_*` / `probability_*` / `predicted_*` /
   `tm_*_r1`），cov 0.974
3. `other496` 434 个指数 beta（cov 平均仅 0.475，覆盖堪忧）
4. 纯 PV 单塔（PV 基线 2、差 1；但历史 46 颗 self-PASS 全被 prod 否决）

---

## 6. 待用户决定

1. **提交授权**（10 颗路线图已就绪，今日额度 4 颗全未动用）
2. **RISK 两颗 2014 空窗**是否算合格（`rsk60_crowding` 2015 才起）
3. **WARNING 级是否放行**（`pwdl3OPx` 仅挂 `LOW_GLB_EMEA_SHARPE` 0.72 / `CLUSTER_TEST` 0.98 两个 WARN）

---

# 追加（2026-11-03 深夜，w188 轮）

## 1. pwdl3OPx prod = 0.5812 通过 ⇒ 最大互斥 10 颗现已五闸全备

| alpha | 塔 | S | F | 2Y | TO% | prod | self |
|---|---|---:|---:|---:|---:|---:|---:|
| leA0X7lA | FUNDAMENTAL | 3.41 | 2.29 | 2.72 | 14.44 | 0.6022 | 0.5110 |
| QPvJ6KVw | RISK | 3.19 | 1.59 | 3.43 | 28.97 | 0.6385 | 0.6120 |
| RRE3O8r1 | FUNDAMENTAL | 2.89 | 1.73 | 2.13 | 16.02 | 0.6479 | 0.4955 |
| xArnqeAw | SENTIMENT | 2.74 | 1.42 | 2.36 | 21.24 | 0.6335 | 0.4665 |
| j2Yg2q9j | SENTIMENT | 2.73 | 2.02 | 2.85 | 14.69 | 0.6585 | 0.5520 |
| d5WqeQbx | FUNDAMENTAL | 2.71 | 1.43 | 2.68 | 7.55 | 0.5846 | 0.4597 |
| pwdl3OPx | ANALYST | 2.70 | 1.36 | 2.95 | 12.83 | 0.5812 PASS | 0.3999 |
| bl6qldJ6 | SENTIMENT | 2.59 | 1.02 | 2.02 | 35.32 | 0.5421 | 0.2775 |
| 9qxR097o | EARNINGS | 2.56 | 1.50 | 2.72 | 9.55 | 0.6502 | 0.5596 |
| qML1x6vK | RISK | 2.50 | 1.55 | 2.33 | 27.42 | 0.6867 | 0.4267 |

塔位账（提完这 10 颗）：FUNDAMENTAL 0→3 点亮 | SENTIMENT 0→3 点亮 | RISK 1→3 点亮 ⇒ 3 座新塔；
EARNINGS 1、ANALYST 1（各差 2 颗，各自只有 1 条可用 signal 腿）。

## 2. glb_submit_v2.py plan 的「今日建议提交集」不可直接采用

脚本建议 leA0X7lA + YP1rzw2J + RRE3O8r1 + d5WqeQbx，但它只查批内 PnL 相关，没有读 4 年互相关矩阵。
实测 YP1rzw2J ↔ RRE3O8r1 = 0.8503（同 signal 腿 single_bucket_5day），两颗只能取一。
正确 Day-1 = leA0X7lA + RRE3O8r1 + d5WqeQbx + bl6qldJ6（FUND 3 颗点亮 + SENT 1 颗）。

## 3. other455 判死（已写入 registry dead_end 第 83 条）

5 个结构互异模板：S = -0.66 / -0.73 / -0.95 / 0.21 / 0.09，TO 仅 4.3-4.7%。
三颗同号负 ⇒ 机制方向真实但量级只有闸门的 42-60%；TO 4.7% 使 F = S·sqrt(4032·margin·TO)，
要过 F>=1.0 需 margin 从 5.1bp 提到 52.8bp（10 倍），不可达。

## 4. 关键修正：纯 techindi 拥挤，但「带门控的 techindi」不拥挤

| 结构 | 代表 | prod |
|---|---|---:|
| 纯 techindi 无门控 signed_power(group_rank(ts_zscore(ts_mean(X,2),504), country), 2.5) | JjeEMEdl 0.7977 / mLoZlKj6 0.8009 / QPvkPaMw 0.7453 / RREQRbA1 0.8206 / O0AYlm2J 0.7652 / 1YNdzx9J 0.8477 / MPYQ7pvo 0.7871 / xAr6JKVp 0.7620 | 0.745-0.848 全 FAIL |
| ANALYST 门控 + techindi 信号腿 | pwdl3OPx（predicted_fourth_quantile_ten_day_return_23） | 0.5812 PASS |

⇒ 拥挤来自「无门控的稠密持仓」，不来自 techindi 字段本身。
推论：纯 OTHER 单数据集 alpha 若不加稀疏门控，prod 结构性地落在 0.75-0.85；
若加同数据集自门控 trade_when(rank(ts_mean(X,22))>t, ..., 0) 则可下探。w188 的 T8 模板正是该假设的直接检验。

## 5. w188 派发（进行中）

8 个结构互异模板，全部基于未测的 _p{M} log-softmax 对数概率字段（不是已拥挤的 q1 回归输出）：

| tag | 模板 | 字段 |
|---|---|---|
| T1 | 最差桶对数概率水平 | tm_19_r1_r5_r10_rh_ah3_d1_r1_q5_p0 |
| T2 | 分布内价差（中桶-最差桶） | tm_19_..._q5_p2 - p0 |
| T3 | 最优桶对数概率水平 | tm_12_..._q5_p4 |
| T4 | 桶序差（最高-次高） | tm_12_..._q5_p4 - p3 |
| T5 | 置信度时序变化（一阶差分） | tm_17_..._q4_p0 |
| T6 | 长期时序秩（去量纲） | tm_17_..._q5_p2 |
| T7 | 二阶不确定度（时间波动） | tm_8_r1_r5_r10_rh_d1_r10_q3_p2 |
| T8 | 自门控稀疏化（纯单塔） | tm_11_..._d1_r10_q4_p2 |

预检：括号 0 偏差、幽灵算子 0、禁用轴 0、check_expression 全空、DB 精确查重 0、
平台 validate_expressions → valid: true / unknown_fields: []。

## 6. techindi_model 字段语义（此前误当成同质分位族）

- tm_{M}_r1_r5_r10_rh[_ah3]_d1_r{H}_q1 = 连续回归输出（需 winsorize）
- ..._q{2..5}（无 _p）= 离散桶归属 0..K-1（不能当连续值直接 rank）
- ..._q{K}_p{M} = log-softmax 对数概率（置信度面，连续）
- 已测 69 个 techindi 字段全集中在 q1 回归与少量桶归属；439 个未测字段以 _p{M} 置信度为主

## 7. 纯单塔只差 prod 的剩余候选（S>=2.4，已排除禁用轴）

| alpha | S | F | 2Y | TO% | 塔 | 处置 |
|---|---:|---:|---:|---:|---|---|
| 3qoz2G9g | 4.15 | 1.81 | 3.28 | 24.3 | OTHER | 已在 prod 队列（fifth-third 价差） |
| 0mY3bpM2 | 3.77 | 1.68 | 2.64 | 21.8 | OTHER | 已在 prod 队列（third_quantile 单腿） |
| P0oa0o7W | 3.10 | 1.37 | 2.07 | 22.8 | OTHER | 未排（fifth 单腿，已知拥挤腿） |
| e75wqEMO | 2.72 | 1.25 | 2.17 | 41.4 | PV | 跳过：历史报告已有 prod 0.79-1.00 |
| 1YN73QeW | 2.56 | 1.29 | 2.20 | 8.3 | INSIDERS | 已在 prod 队列 |
| GrWwjpa0 | 2.56 | 1.29 | 2.20 | 8.3 | INSIDERS | 跳过：与 1YN73QeW 同核 |

omE51bw2（S 4.12）因用 subindustry 轴（GLB 禁用）淘汰；kqN03AZd（S 4.14）属 FUNDAMENTAL+OTHER（已 4 颗封盘）。

## 8. ★★★★★ 互相关结构复核（2026-11-03 23:00）：10 颗是 READY 池内的真上限，但**不是**全局上限

对上表 10 颗 + READY14 其余 4 颗 + 池外 5 颗，共 **19 颗**跑平台 4 年互相关矩阵，
再解**精确最大互斥团**（边 = 相关 < 0.70，Bron–Kerbosch 带界搜索）：

### 8.1 READY14 内部：最大互斥团 = 10（成员与先前名单不同）

| 排名 | alpha | S | prod | 备注 |
|---|---|---:|---:|---|
| 1 | leA0X7lA | 3.41 | 0.6022 | FUNDAMENTAL+OTHER |
| 2 | QPvJ6KVw | 3.19 | 0.6385 | OTHER+RISK |
| 3 | **npv9WLVE** | **3.08** | **0.6638** | OTHER+RISK —— **先前被漏掉** |
| 4 | RRE3O8r1 | 2.89 | 0.6479 | FUNDAMENTAL+OTHER |
| 5 | xArnqeAw | 2.74 | 0.6335 | OTHER+SENTIMENT |
| 6 | j2Yg2q9j | 2.73 | 0.6585 | OTHER+SENTIMENT |
| 7 | d5WqeQbx | 2.71 | 0.5846 | FUNDAMENTAL+OTHER |
| 8 | pwdl3OPx | 2.70 | 0.5812 | ANALYST+OTHER |
| 9 | bl6qldJ6 | 2.59 | 0.5421 | OTHER+SENTIMENT |
| 10 | 9qxR097o | 2.56 | 0.6502 | EARNINGS+OTHER |

**与先前 10 颗名单的唯一差别**：用 `npv9WLVE`（S 3.08, prod 0.6638）替换 `qML1x6vK`（S 2.50, prod 0.6867）。
两者互斥 0.8065 ⇒ 只能取一；npv9WLVE 的 S 高 1.23 倍、prod 低 0.023 ⇒ **纯升级，应改用它**。
塔位完全不变：FUNDAMENTAL 3 / SENTIMENT 3 / RISK 1+2=3 ⇒ 同样点亮 3 座新塔。

### 8.2 READY14 里的 4 颗冗余（互斥对，必须择一）

| 对 | 相关 | 处置 |
|---|---:|---|
| `N1NO9nRe` ↔ `9qxR097o` | **0.9864** | 近重复（同 ern3 门控 + 同 signal 腿）⇒ 视作同一颗，保留 9qxR097o（S 2.56 ≥ 2.54） |
| `xArnqeAw` ↔ `Xg9rMdvl` | 0.8526 | 保留 xArnqeAw（S 2.74 > 2.44） |
| `YP1rzw2J` ↔ `RRE3O8r1` | 0.8503 | 保留 RRE3O8r1（S 2.89 < YP1rzw2J 2.95，但 YP1rzw2J 还与 d5WqeQbx 0.7435 冲突 ⇒ 净亏 1 颗） |
| `npv9WLVE` ↔ `qML1x6vK` | 0.8065 | 保留 npv9WLVE |

### 8.3 ★ 池外 5 颗与 10 团**全部兼容**（最大相关仅 0.15）

| alpha | 对 10 团的最大相关 | 结论 |
|---|---:|---|
| `0mY3bpM2` | 0.115（pwdl3OPx） | 可加；**但 prod 0.7516 未过** |
| `3qoz2G9g` | 0.142（pwdl3OPx） | 可加；与 0mY3bpM2 互斥 0.856 |
| `1YN73QeW` | 0.1509（xArnqeAw） | 可加；INSIDERS 新腿，prod 待测 |
| `P0oa0o7W` | 0.0987（pwdl3OPx） | 可加；与 3qoz2G9g 互斥 0.7294、与 0mY3bpM2 0.6813（相容） |
| `GrWwjpa0` | 0.1509 | 与 1YN73QeW 相关 = 1.0（同核）⇒ 视作同一颗 |

⇒ **理论互斥上限 = 10 + {0mY3bpM2, P0oa0o7W} + 1YN73QeW = 13 颗**，不是 10 颗。

### 8.4 但 0mY3bpM2 的 prod 已实测失败，天花板回到 12

`0mY3bpM2` prod = **0.7516 FAIL**，直方图 `[[0.7,0.8,8]]`（8 个点落在 [0.7,0.8)，浅钉但成片）⇒ 需降 0.052。
该颗与 `3qoz2G9g`（fifth−third 价差）、`P0oa0o7W`（fifth 单腿）同属 techindi 分位族稠密结构，
与 `mLoZlKj6` 0.8009 / `xAr6JKVp` 0.7620 同形 ⇒ 同族大概率同样卡 0.75–0.80。
**唯一高概率突破点是 `1YN73QeW`**（INSIDERS `avg_sell_shares`，TO 仅 8.3%、持仓天然稀疏，与 10 团相关 0.15）。

### 8.5 结论修正（覆盖第 1 节的「可交付上限 10 颗」）

- 「10 颗」是 **READY 池内部的互斥上限**，不是全局上限；
- 真正的瓶颈是 **prod 相关性**（稠密持仓必挤），不是互相关（候选间相关普遍只有 0.1–0.5，远未饱和）；
- 因此**新增 alpha 的正确方向不是「找与库存不相关的信号腿」（已证明很宽松），而是「找能过 prod 的稀疏结构」**；
- 当前可交付 = **10 颗（prod 全部实测 < 0.70）**；`1YN73QeW` / `P0oa0o7W` 若过 prod，可增至 11–12；
- 20 颗目标仍不可达，但缺口从 10 收窄到 8–9。

### 8.6 修订后的三日提交排程（内部/跨日全部 < 0.70）

| 日 | 4 颗 | ΣS | 内部最大相关 | 点灯 |
|---|---|---:|---|---|
| Day-1 | `leA0X7lA` `RRE3O8r1` `d5WqeQbx` `npv9WLVE` | 12.09 | 0.6741（RRE3O8r1↔d5WqeQbx） | **FUNDAMENTAL 3/3 点亮**；RISK 1+1=2 |
| Day-2 | `QPvJ6KVw` `xArnqeAw` `j2Yg2q9j` `bl6qldJ6` | 11.25 | 0.6555（xArnqeAw↔j2Yg2q9j） | **RISK 1+2=3 点亮**；**SENTIMENT 3/3 点亮** |
| Day-3 | `pwdl3OPx` `9qxR097o` | 5.26 | 0.3252 | ANALYST 1、EARNINGS 1（各差 2 颗） |

跨日最大相关 0.5393（npv9WLVE↔QPvJ6KVw）⇒ 三天内累积提交池的自相关仍 < 0.70。
合计 10 颗 / ΣS 28.60，点亮 3 座新塔。`qML1x6vK`(S 2.50) / `N1NO9nRe`(与 9qxR097o 0.9864) /
`Xg9rMdvl`(0.8526) / `YP1rzw2J`(0.8503) 作为备胎，仅在主选 prod 复测掉线时补位。

## 9. ★★★★★ 全库回扫：120 颗「只差 prod」——瓶颈 100% 是 prod，但塔规则把其中绝大多数判死

对全库 GLB 未提交 alpha 做四层漏斗（S≥1.58 ∩ F≥1.0 ∩ 2Y≥1.58 ∩ TO∈[1%,70%]）：

| 层 | 数量 | 含义 |
|---|---:|---|
| 达标未提交总数 | **349** | 四层全过 |
| prod PASS(<0.70) | 26 | 已可提交 |
| prod FAIL(≥0.70) | 153 | 撞 prod 墙 |
| **prod 未测 且 self<0.70** | **120** | **只差一次 prod 测量** |
| self FAIL(≥0.70) | 81 | 撞 self 墙 |
| self 未测 | 1 | — |

⇒ 此前认为「只剩 6 颗纯单塔候选」是**严重低估**：真实是 120 颗。

### 9.1 精选 20 颗跑 4 年互相关 → 理论最大团 19 颗

从 120 颗里挑 S/F/2Y 最高、腿互不重复的 20 颗，与 10 颗交付集共 30 颗求精确最大团：

**19 颗**（10 交付集 + 9 颗新品）。其中 S 最高几颗：

| alpha | S | F | 2Y | 门控字段 | 对 10 团最大相关 |
|---|---:|---:|---:|---|---:|
| `kqonYg0L` | 3.78 | 3.46 | 5.19 | `ts_std_dev(returns,22)` | 0.6503 |
| `MPYO0Kwo` | 3.78 | 3.31 | 4.34 | `capm_beta_1m` | 0.6237 |
| `A1Nn2vPQ` | 3.73 | 3.22 | 4.67 | `ts_std_dev(returns,22)`+`cap` | 0.4603 |
| `npdnZkKd` | 3.56 | 1.42 | 3.79 | 盘中量比 | 0.6502 |
| `WjOMaRnZ` | 3.49 | 1.49 | 4.25 | `rsk60_crowding`+`cap` | 0.5547 |
| `pwdmjaqb` | 3.43 | 2.63 | 4.62 | `mdl239_*` | 0.5649 |
| `88R9ARkm` | 3.21 | 2.96 | **5.44** | 无（纯 RISK `rsk60_offer`） | 0.4902 |

### 9.2 但塔规则把它们判死（台账已生效，我复核一致）

| alpha | 用到的塔 | 违规 |
|---|---|---|
| `MPYO0Kwo` / `9qxYMYQe` / `58Ex5eE5` / `RREM9AQo` | MODEL(`macro_equity_signals` 的 `capm_*` / `bond_regression_beta`) + OTHER | **trio 内部互组** |
| `pwdmjaqb` / `gJe6Mwk0` | MODEL(`model239`) + OTHER | **trio 内部互组** |
| `kqonYg0L` / `A1Nn2vPQ` / `npdnZkKd` | PV(`returns`/`cap`/`adv20`/`intraday_pv_feats`) + OTHER | **trio 内部互组** |
| `WjOMaRnZ` | RISK + PV(`cap`/`adv20`) + OTHER | **三塔同现** |
| `88R9ARkm` / `QPvkqZ0G` / `kqNrb73k` | 纯 RISK ✅ | 合规 —— 但台账仍标 dead，需复查死因 |

**关键工具事实**：`cap` / `returns` / `volume` / `adv20` 虽属基础价格量，在塔账里**会被计入 PV 塔**
（与 `country`/`industry` 这类 GROUP 轴不同）。任何「用 `cap`/`returns` 做门控」的 dl_riskfree 结构都会变成 PV+OTHER ⇒ 判死。
这也解释了为什么历史上大量 `rank(cap) > 0.2` 的门控变体全部无法入库。

### 9.3 合规且仅缺 prod 的只剩 3 颗

| alpha | S | F | TO% | self | 塔 | 组合类型 |
|---|---:|---:|---:|---:|---|---|
| `1YN73QeW` | 2.56 | 1.29 | 8.3 | 0.103 | INSIDERS(`avg_sell_shares`) | **纯单塔，零配额** |
| `O0AOVJoJ` | 2.78 | 2.80 | 10.7 | 0.523 | INSTITUTIONS+OTHER | 若纳入则组合类型 5→6 |
| `P0oa0o7W` | 3.10 | 1.37 | 22.8 | 0.073 | 纯 OTHER(`predicted_fifth_quantile`) | 纯单塔，零配额 |

（`3qoz2G9g` S 4.15 纯 OTHER 合规，但与 `P0oa0o7W` 互斥 0.7294、与已失败的 `0mY3bpM2` 互斥 0.856 ⇒ 只能三选一。）

### 9.4 结论

- **合规可达上限 = 13 颗**（10 已确认 + `1YN73QeW` + `O0AOVJoJ` + `P0oa0o7W`，待 prod）；
- **20 颗在原塔规则下不可达**：理论上限 19 里，有 9 颗因 trio 内部互组/三塔同现被判死，而这些恰恰是 S/F/2Y 最高的一批（S 3.2–3.8、F 2.4–3.5、2Y 4.3–5.4）；
- **要冲 20 颗，唯一真正的杠杆是放宽塔混规则**（例如允许 MODEL+OTHER 或 PV+OTHER，或把「组合类型 ≤5」改成 ≤8）。这不是工程问题，是策略选择，需用户裁定；
- 若不放宽：目标 13 颗，其中 3 颗待 prod，prod 单并发约 5–15 分钟/颗 ⇒ 约 15–45 分钟内可判定完毕。
