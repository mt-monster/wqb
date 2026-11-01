# other545 · KOR / TOP600 / D1 字段画像

> 类型 MATRIX（**字段全部 VECTOR**）· **仅 4 个字段** · 覆盖率 0.8393 · 本地 `n_tests=0`（全 UNTESTED）
> 金字塔 category = **other**（multiplier 1.6，**未点亮塔**）
> 采集：`get_field_catalog(region=KOR, dataset=other545)`，2026-10-30
> ⚠ 约束 5：OTHER 类禁止与 PV / MODEL / OTHER 组腿 ⇒ 只能做 **ATOM 单集**

## 0. 全字段清单（4/4，αC 降序）

| # | 字段 | αC | users | cov | desc |
|---|---|---|---|---|---|
| 1 | `oth545_score` | 11 | 7 | .8393 | **Final composite NEMO 2.0 model score** aggregated from **seven network momentum signals** |
| 2 | `oth545_mpd` | 9 | 7 | .8393 | Score based on **dynamic price momentum**, capturing advanced or machine-learned price momentum |
| 3 | `oth545_mktcap` | 7 | 6 | .8393 | Market capitalization (USD) |
| 4 | `oth545_pln_omen` | 2 | 2 | .8393 | Score based on **NLP-derived network momentum** using text-mined linkages |

**读数**：4 个字段里 **3 个是模型评分**（`score` 复合 / `mpd` 价格动量 / `pln_omen` NLP 网络动量），
1 个是市值（**只可作规模轴**）。αC 全都很低（2–11）⇒ **平台几乎无人挖**，属真正的白空间但也无先例可循。

## 1. 名 vs description 差异

| 名 | 实际 | 按名分类的错误 |
|---|---|---|
| `score` | **七个网络动量信号的复合分** | 名过于笼统，会与其它集的 `score` 混为一谈 |
| `mpd` | machine-learned **price momentum** | 名不含 momentum，极易被当不明缩写跳过 |
| `pln_omen` | **NLP 文本挖掘的网络动量**（`omen` = network momentum 的缩写） | 同上；且与 `mpd` **同属动量族但口径正交**（价格 vs 文本网络） |
| `mktcap` | 市值 | 唯一非信号件 |

⚠ **`score` ⊃ `mpd` ∪ `pln_omen`**（复合分由七个信号聚合）⇒ 三者**不是三条独立腿**，
是一条腿的三档测量；`score` 与 `mpd`/`pln_omen` 同时上 = **同一机制铺量**。

## 2. 五问

| # | 问 | 答 |
|---|---|---|
| 1 时间维度 | 存量/流量 | **存量评分**（daily point-in-time），非变化率 ⇒ 铁律 A 不适用（评分可正可负、无单边恒正） |
| 2 相对性 | 水平/排序 | **排序**：评分绝对量级无意义 ⇒ `vec_avg` 降维后 `group_rank` |
| 3 被定价的是谁 | 广度/强度 | **强度**：网络动量强度（供应商/客户链条上的价格传导） |
| 4 有无博弈 | 拥挤/规模 | **不拥挤**（αC≤11）；但需注意市值字段与评分可能同源（模型可能内嵌规模控制） |
| 5 事件性 | 稀疏 | **否**：cov .839 连续日频 |

## 3. 预处理决策

| 体征 | 决策 |
|---|---|
| **全部 VECTOR** | 必须先 `vec_avg(F)` 降维（唯一合法的 VECTOR 入口，见 skill ②.b 末行） |
| cov .8393（16% NaN） | `vec_avg` 后仍需 `ts_backfill(F, 10)` |
| 评分、可正可负 | `group_rank(·, sector)`；不比 `zscore`（评分分布未知，秩更稳） |
| `mktcap` | **只作规模轴**（`vector_neut` 的规模项），不作信号 |
| 三档同机制 | **一条腿只出 1 颗**：`score` 为主，`mpd` / `pln_omen` 作对照，不同时上 |
| 十年数据 | cov .839 是**横截面**口径；**逐十年份覆盖未验**，须先读 `get_alpha_yearly_stats` longCount |

## 4. 机制（A-2）

**谁在被定价**：**供应链 / 经济链接网络上的滞后传导**——一家公司的价格动量会沿
供应商-客户、同业、文本共现等七条边传导到关联公司，市场对这些二级传导反应滞后。

**为什么会被错**：投资者的注意力与信息处理能力有限（limited attention），
只盯直接持仓标的，不追踪产业链上的间接动量；韩国市场机构覆盖集中在大市值，
中小盘的网络传导几乎无人定价。

**错了多久修复**：**数周至一季**（`ts_mean` 22–66d 窗口）。

**预期方向**：网络动量为**正**（强者继续强）⇒ 直接 `group_rank(vec_avg(score), sector)`，
**不做 reverse**。⚠ 但动量类在韩国有反转风险 ⇒ **铁律 B 正反各测**。

**Boundary Conditions**：链接数据更新频率未知；`score` 七条边权重不透明（黑盒）；
`mktcap` 与 `score` 若同源会使中性化失效。

## 5. 拟用取式（**wave 216 候选**，非本波）

| # | 表达式 | 意图 |
|---|---|---|
| 1 | `group_rank(ts_backfill(vec_avg(oth545_score), 10), sector)` | 复合网络动量（正向） |
| 2 | `reverse(<同>)` | 铁律 B 对照 |
| 3 | `group_rank(ts_backfill(vec_avg(oth545_mpd), 10), sector)` | 纯价格动量分量（口径分离） |
| 4 | `group_rank(ts_backfill(vec_avg(oth545_pln_omen), 10), sector)` | NLP 网络动量分量（与价格正交） |

## 6. 实测记录

（未回测）
