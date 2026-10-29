# USA · `shortinterest43` 字段画像

> 由 `tools/fields/profile_dataset_fields.py` 生成，输入为 `get_datafields` 原始返回。零平台配额。

## 1 规模与完整性

| 项 | 值 |
|---|---|
| 本次返回字段数 | 32 |
| 平台声明数 `platform_count` | 32 |
| 返回 `count` | 32 |
| 是否完整 `complete` | True |
| 类型分布 | {'MATRIX': 32} |
| 平均 coverage | 0.9994 |
| 判定 | ✅ 完整 |

## 2 可用性分档

### 2.1 coverage

| 档 | 字段数 |
|---|---|
| ≥0.90（可直接做尽） | 32 |

### 2.2 拥挤度（决定 prod 相关性风险）

| 档 | 字段数 |
|---|---|
| 低拥挤（≤50 alpha） | 20 |
| 中拥挤（51–500） | 12 |

零竞争字段（`userCount==0`）：**0** / 32；描述带单位标注：0

## 3 语义结构

| 语义族 | 字段数 | 示例字段 |
|---|---|---|
| 未归类 | 32 | `count_shares_short_exempted`, `quantity_sold_short_exempted`, `shrt43_batsshvol_marketcenter`, `shrt43_batsshvol_svol` |

**时间朝向**（`forecast`=前瞻/预测，`realized`=已实现/事后，`mixed`=差值构造）：

| 朝向 | 字段数 |
|---|---|
| unknown | 32 |

## 4 名字前缀聚类（前 15）

| 前缀 | 字段数 |
|---|---|
| `shrt43_batssh` | 4 |
| `shrt43_byxxsh` | 4 |
| `shrt43_edgash` | 4 |
| `shrt43_edgxsh` | 4 |
| `shrt43_batsshvol` | 3 |
| `shrt43_byxxshvol` | 3 |
| `shrt43_edgashvol` | 3 |
| `shrt43_edgxshvol` | 3 |
| `count_shares` | 1 |
| `quantity_sold` | 1 |
| `total_short` | 1 |
| `volume_short` | 1 |

## 4.5 人工语义族映射（脚本无法归类，本节为权威口径）

> 脚本对 `shrt43_*` 前缀全部判为「未归类」，因为字段名不含标准语义词。
> 下表由人工按 **Cboe 四子交易所披露口径**补齐，是后续机制设计的唯一依据。
> 平台论坛帖 `35577573602455`（MY82844，15 票）已确认 bats/byxx/edga/edgx = **CBOE 四个子交易所**。

| 族 | 字段 | 数量 | 经济含义 | 预定用途 |
|---|---|---|---|---|
| **A 交易所卖空流量** | `shrt43_{batsshvol,byxxshvol,edgashvol,edgxshvol}_svol` + 同名 `_totalvolume` | 8 | 该票在**该所**当日「卖空股数」与「总成交股数」。四所 = BZX / BYX / EDGA / EDGX | **信号腿主力**：同单位相除 = 该所卖空占比（无量纲、ATOM 合规、无需 ε） |
| **B 交易所卖空聚合** | `shrt43_<venue>sh_sumsize_{m,s}_data{1,2}` | 16 | 描述只有 "data1"/"data2"，`m`/`s` 疑为 minute/session 或 mean/sum 两种粒度，data1/2 疑为两个统计口径 | **机制未知**；但 `shrt43_edgxsh_sumsize_m_data2` = **74 用户 / 124 alpha**（全数据集最拥挤）⇒ 说明已有人从此挖到东西，值得一次探针 |
| **C 交易所标识** | `shrt43_<venue>shvol_marketcenter` | 4 | 四所描述统一写 "Bats operated stock exchanges"，是**元数据/标识**而非信号 | **分组轴候选**（若为常量则退化，需实测）；也可作数据完整性校验 |
| **D 豁免卖空** | `count_shares_short_exempted`(EDGX) / `quantity_sold_short_exempted` / `total_short_exempted_shares`(EDGA) / `volume_short_exempted_trades` | 4 | 豁免卖空 = **做市商豁免**（Reg SHO 豁免条款）下的卖空股数 | **零竞争**（1–3 用户）；机制清晰但有 3 个字段描述高度重叠，需先验证是否同源 |

### 4.5.1 频率与结构（决定机制可行性）

- **日频**（描述均为 "for the day" / "during the reported day"）⇒ 与 `shortinterest29`（月频、148 持仓、已判死）**完全不同**。
- **横截面全覆盖**（coverage 0.99–1.0，32 字段中 30 个恰为 1.0）。
- **无 VECTOR** ⇒ 不需要 `vec_*` 聚合，`unitHandling=VERIFY` 下同单位相除即可。
- A 族 = 4 所 × (svol, totalvolume) ⇒ 可构造三个正交维度：
  1. **水平**：某所卖空占比 = `divide(svol, totalvolume)`
  2. **聚合**：四所量加权占比 = `divide(Σsvol, Σtotalvolume)`（等价论坛「按交易量占比加权」做法）
  3. **离散**：跨所占比差 = `subtract(r_edgx, r_batss)` —— 做空活动在交易所间的**偏好分歧**

### 4.5.2 已知的首波实测结果（波 151，2026-10-29）

| 模板 | S | F | TO | 2Y | SUB | inv_ratio | fRA | 判读 |
|---|---|---|---|---|---|---|---|---|
| `reverse(ts_rank(四所量加权占比, 66))` | 1.18 | 0.17 | **100.57%** | **−0.24** | 1.68 | 1.2542 | 4 | 换手爆炸；**近两年失效**（2Y 为负） |
| `subtract(r_edgx, r_batss)` | 1.51 | 0.22 | **130.33%** | 1.45 | 0.61 | 0.4702 | 5 | 换手最差；inv_ratio 0.47 投资域衰减 |
| `reverse(ts_decay_linear(ts_rank(四所量加权占比,66),66))` | 0.34 | 0.07 | 15.35% | −0.05 | 0.15 | 1.1176 | 3 | **平滑即抹信号** |

⇒ **初步结论：纯 SVO ratio（卖空占比）是短期高噪声流量指标**。`ts_rank` 66 日已含时序平滑但 TO 仍 100%，
再加一层 `ts_decay_linear` 66 则 S 崩到 0.34 ⇒ **信号半衰期显著短于 66 日**，属「流量冲击」而非「状态变量」。
论坛作者用 `decay=250` 压换手，本质是拿信号强度换换手，与该数据集的信噪比结构一致。
**下一步必须换维度**：补 `group_zscore` 横截面标准化层（首波全部缺这一层，而 shortinterest3 的成功配方依赖它），
以及转向 B 族 `sumsize`（高拥挤 = 有人挖到）与 D 族豁免卖空（零竞争）。



打分 = 覆盖 40 + 低拥挤 25 + 语义可解释 20 + 前瞻 5（非信号 −30）。**只做排序参考**，仍须过单位闸与机制假设。

| # | 字段 | 类型 | cov | user | alpha | 语义族 | 朝向 | 分 | 描述（截断） |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `count_shares_short_exempted` | MATRIX | 1.000 | 3 | 3 | 未归类 | - | 60.0 | Shares sold short under short-exempt conditions for the symbol on EDGX during the reporte… |
| 2 | `quantity_sold_short_exempted` | MATRIX | 1.000 | 2 | 3 | 未归类 | - | 60.0 | Total number of shares sold short that are exempt from certain trading regulations. |
| 3 | `shrt43_batsshvol_marketcenter` | MATRIX | 1.000 | 22 | 35 | 未归类 | - | 60.0 | Bats operated stock exchanges |
| 4 | `shrt43_byxxshvol_marketcenter` | MATRIX | 1.000 | 13 | 22 | 未归类 | - | 60.0 | Bats operated stock exchanges |
| 5 | `shrt43_edgashvol_marketcenter` | MATRIX | 1.000 | 13 | 14 | 未归类 | - | 60.0 | Bats operated stock exchanges |
| 6 | `shrt43_edgashvol_totalvolume` | MATRIX | 1.000 | 32 | 41 | 未归类 | - | 60.0 | Total number of shares traded for the symbol on EDGA for the given day |
| 7 | `shrt43_edgxshvol_marketcenter` | MATRIX | 1.000 | 8 | 11 | 未归类 | - | 60.0 | Bats operated stock exchanges |
| 8 | `shrt43_batssh_sumsize_m_data2` | MATRIX | 1.000 | 30 | 35 | 未归类 | - | 60.0 | data2 |
| 9 | `shrt43_batssh_sumsize_s_data2` | MATRIX | 1.000 | 29 | 46 | 未归类 | - | 60.0 | data2 |
| 10 | `shrt43_byxxsh_sumsize_m_data2` | MATRIX | 1.000 | 14 | 21 | 未归类 | - | 60.0 | data2 |
| 11 | `shrt43_byxxsh_sumsize_s_data2` | MATRIX | 1.000 | 14 | 31 | 未归类 | - | 60.0 | data2 |
| 12 | `shrt43_edgash_sumsize_m_data1` | MATRIX | 0.990 | 29 | 38 | 未归类 | - | 60.0 | data1 |
| 13 | `shrt43_edgash_sumsize_m_data2` | MATRIX | 0.990 | 18 | 32 | 未归类 | - | 60.0 | data2 |
| 14 | `shrt43_edgash_sumsize_s_data1` | MATRIX | 1.000 | 35 | 50 | 未归类 | - | 60.0 | data1 |
| 15 | `shrt43_edgash_sumsize_s_data2` | MATRIX | 1.000 | 15 | 19 | 未归类 | - | 60.0 | data2 |
| 16 | `shrt43_edgxsh_sumsize_m_data1` | MATRIX | 1.000 | 25 | 27 | 未归类 | - | 60.0 | data1 |
| 17 | `shrt43_edgxsh_sumsize_s_data1` | MATRIX | 1.000 | 26 | 32 | 未归类 | - | 60.0 | data1 |
| 18 | `shrt43_edgxsh_sumsize_s_data2` | MATRIX | 1.000 | 27 | 30 | 未归类 | - | 60.0 | data2 |
| 19 | `total_short_exempted_shares` | MATRIX | 1.000 | 2 | 2 | 未归类 | - | 60.0 | Number of shares sold short under short-exempt conditions for the symbol on EDGA for the … |
| 20 | `volume_short_exempted_trades` | MATRIX | 1.000 | 1 | 2 | 未归类 | - | 60.0 | Sum of shares sold short under exempt classification for the trading day. |
| 21 | `shrt43_batsshvol_svol` | MATRIX | 1.000 | 110 | 164 | 未归类 | - | 52.0 | Number of shares sold short on BZX (BATS) for the symbol on that day |
| 22 | `shrt43_batsshvol_totalvolume` | MATRIX | 1.000 | 157 | 285 | 未归类 | - | 52.0 | Total shares traded on BZX (BATS) for the symbol on that day |
| 23 | `shrt43_byxxshvol_svol` | MATRIX | 1.000 | 67 | 92 | 未归类 | - | 52.0 | Total shares sold short for the symbol on the BYX venue for the day |
| 24 | `shrt43_byxxshvol_totalvolume` | MATRIX | 1.000 | 76 | 117 | 未归类 | - | 52.0 | Total shares traded for the symbol on the BYX venue for the day |
| 25 | `shrt43_edgashvol_svol` | MATRIX | 1.000 | 43 | 59 | 未归类 | - | 52.0 | Total number of shares sold short for the symbol on EDGA for the given day |
