# shortinterest43（USA / TOP3000 / D1）模板库

> **为什么有这份文档**：用户硬约束 —— 「使用模板时一定要保持模板多样性和数量（10 个模板），
> 可以查平台论坛和 ideas 和外部金融论文去补充」。模板单一会把「骨架选错」误判成「字段没信号」。
>
> 塔位：`pyramid_short = shortinterest`（USA D1，本轮 **0/3 未点亮**），单塔 **ATOM 合规**。
>
> 数据集画像见 [`shortinterest43_field_profile.md`](shortinterest43_field_profile.md)（含人工语义族映射）。
>
> 更新日期：2026-10-29

---

## 1. 数据集定位（与已判死的 shortinterest29 的区别）

| 维度 | shortinterest43 | shortinterest29（已判死） |
|---|---|---|
| 频率 | **日频**（"for the day" / "during the reported day"） | 月频聚合 |
| 字段 | 32 全 MATRIX，coverage 0.9994 | 32 全 MATRIX，coverage 0.8838 |
| 实际持仓 | 待首波确认 | **仅 148 只** ⇒ 直接判死 |
| 结构 | 4 个 CBOE 子交易所（BZX/BYX/EDGA/EDGX）× (卖空股数, 总成交股数) | 单一汇总口径 |
| 拥挤度 | 492 用户 / 1527 alpha | 133 用户 / 247 alpha |

**核心可用结构**：同一只票在 4 个交易所各自的「卖空股数 ÷ 该所总成交股数」= 该所的卖空占比。
分子分母同单位（都是股数）⇒ **无量纲、ATOM 合规、不需要 ε**。

---

## 2. 论坛与文献依据

### 2.1 平台论坛帖 `35577573602455`（MY82844，15 票，2025-10-12）

原文可执行要点：
1. **确认 bats/byxx/edga/edgx = CBOE 四个子交易所**（这是本数据集字段理解的唯一权威来源，官方描述很模糊）。
2. **主力模板 = `ts_rank(short volume to volume ratio)`**，作者实测「表现比较明显」，但 **turnover 比较高**，建议 **`decay=250`** 控制。
3. **组合多交易所提升鲁棒性**：可组合 bats+byxx（等权），或**按交易量占比组合 bats+edgx**；作者称**按交易量加权的方式提升更明显**。
4. `institutions20` 结构类似，同样方法有效。
5. short interest 策略有 **short squeeze 风险**，可用 `risk60` 度量（但 risk60 历史短），思路是用 `trade_when` 做仓位控制规避。
6. 作者提到 `tanh(ratio)` 也有作用 —— ⚠ **`tanh` 在 USA 是幽灵算子**（`operator_audit` 实测 19 个之一），不可用；替代走 `signed_power` 或 `winsorize`。

### 2.2 经济解释（本轮实证修正了论坛的隐含假设）

**实测方向**：卖空占比**高 → 后续涨**（不是跌）。证据：`ts_rank(ratio,66)` S **−1.32**，`reverse` 版 S **+1.32**，两者指标精确取负。

**机理**：Cboe 交易所层面披露的 short sale volume 主体是**做市商的库存对冲卖空**，不是方向性做空。
做市商在承接卖压后持有库存，后续价格修复 ⇒ 高卖空占比预示短期反弹。
这与 FINRA 双月披露的 short interest（未平仓空头，方向性看空）**是完全不同的量**，不可混用先验。

⇒ **本数据集的先验方向：reverse（做多高卖空占比）。**

---

## 3. 模板库（14 个，结构互异）

差异维度必须落在 **骨架结构 / 算子几何 / 矩 / 分组轴 / 非线性变换 / 字段族** 上 —— 只换窗口或换常数**不算**新模板。

### 3.1 A 族「交易所卖空流量」（`svol` / `totalvolume`）

`r_v = divide(shrt43_<venue>shvol_svol, shrt43_<venue>shvol_totalvolume)`，4 个所各一个。

| # | 编号 | 骨架 | 经济机制 | 状态 |
|---|---|---|---|---|
| 1 | **P1** | `ts_rank(r_batss, 66)` | 论坛主力模板直译（单所时序分位） | ✅ 已测 S **−1.32** / F −0.20 / TO **102.97%** |
| 2 | **P2** | `reverse(ts_rank(r_batss, 66))` | P1 的符号对照（定方向） | ✅ 已测 S **+1.32** / F 0.20 / TO 102.97% / 2Y 0.19 |
| 3 | **P3** | `reverse(ts_rank(divide(Σ4所svol, Σ4所tv), 66))` | 四所**量加权**聚合（论坛「按交易量占比组合」的等价形式） | ✅ 已测 S 1.18 / F 0.17 / TO 100.57% / **2Y −0.24** |
| 4 | **P4** | `subtract(r_edgx, r_batss)` | **跨所卖空偏好分歧**：做空活动集中在某通道 → 信息含量更高 | ✅ 已测 S **1.51**（本族最高）/ TO **130.33%** / inv_ratio 0.4702 |
| 5 | **P5** | `reverse(ts_decay_linear(ts_rank(divide(Σ4所svol,Σ4所tv),66),66))` | P3 + 平滑层（论坛 decay=250 的算子化形式） | ✅ 已测 S 0.34 / TO 15.35% ⇒ **平滑抹掉 71% 信号** |
| 6 | **P6** | `reverse(ts_zscore(divide(svol_batss, ts_mean(svol_batss,252)), 66))` | **卖空规模**相对自身年度均值的异常（规模维度，非比率维度） | ✅ 已测 S 0.45 / **2Y −1.27** |
| 7 | **P7** | `group_zscore(ts_mean(r_batss, 252), industry)` | 长窗聚合 + **横截面标准化**（补 A 族缺失的层） | 🔄 波 152 在飞 |
| 8 | **P8** | `reverse(group_zscore(ts_mean(r_batss, 66), industry))` | 中窗聚合 + 横截面标准化 + 反向 | 🔄 波 152 在飞 |
| 9 | **P9** | `group_zscore(subtract(r_edgx, r_batss), industry)` | P4 的跨所分歧 + 横截面标准化（P4 的 TO 修正版） | 🔄 波 152 在飞 |
| 10 | **P10** | `group_zscore(ts_covariance(r_batss, r_batss, 22), industry)` | **二阶矩**：卖空占比的时序不确定性（迁移 shortinterest3 的 M1 机制） | 待发 |
| 11 | **P11** | `reverse(ts_decay_linear(group_zscore(ts_covariance(subtract(r_edgx,r_batss), subtract(r_edgx,r_batss), 22), industry), 66))` | 跨所分歧的二阶矩 + 移植 shortinterest3 的 **CW 破解配方**（内层时序、外层截面） | 待发 |
| 12 | **P12** | `group_zscore(divide(ts_mean(svol_batss,22), ts_mean(svol_batss,252)), industry)` | 卖空规模的**短期/长期背离**（同单位相除，无量纲） | 待发 |

### 3.2 B 族「交易所卖空聚合」（`sumsize`，机制未知但最拥挤）

| # | 编号 | 骨架 | 经济机制 | 状态 |
|---|---|---|---|---|
| 13 | **P13** | `divide(shrt43_edgxsh_sumsize_m_data1, Σ4所_sumsize_m_data1)` | EDGX 在该票的**月度卖空份额**（同族同单位相除） | 🔄 波 152 在飞 |
| 14 | **P14** | 同 P13 但 `data2` | data2 口径（`edgxsh_sumsize_m_data2` 是**全数据集最拥挤**字段：74 用户/124 alpha） | 🔄 波 152 在飞 |

> `m` / `s` 推测为 **monthly / session(daily)** 两种粒度；`data1` / `data2` 为两个统计口径。
> 若 `m` 确为月度聚合，则该族是**低频结构量**，可绕开 A 族的换手问题 —— 这是 P13/P14 的核心赌注。

### 3.3 D 族「豁免卖空」（零竞争）

| # | 编号 | 骨架 | 经济机制 | 状态 |
|---|---|---|---|---|
| 15 | **P15** | `divide(volume_short_exempted_trades, quantity_sold_short_exempted)` | 豁免卖空（Reg SHO 做市商豁免）在卖空总量中的占比 | 🔄 波 152 在飞 |
| 16 | **P16** | `group_zscore(divide(count_shares_short_exempted, quantity_sold_short_exempted), industry)` | 同上，换 EDGX 口径 + 横截面标准化 | 待发 |

> D 族 4 个字段仅 1–3 用户 ⇒ **零竞争**。但 3 个字段描述高度重叠（都是 "shares sold short under exempt"），
> 若比值恒为常数则说明同源，需先看 P15 的读数。

---

## 4. 已证实的判读（波 151 首波六条）

### 4.1 换手灾难：这是本数据集的第一约束

6 条中 5 条 **TO > 100%**：P1/P2 102.97%、P3 100.57%、P4 **130.33%**、P6 105.73%。
唯一低换手 P5（15.35%）的 S 只有 0.34。

⇒ **日频交易所层面卖空占比的日间方差 >> 信号**。`fitness = S × sqrt(|R| / max(TO,0.125))` 被高换手压死，
六条 F 全部 ≤0.22。

### 4.2 平滑即抹信号：信号半衰期 < 15 日

P3（ts_rank 66，无额外平滑）S 1.18 / TO 100.57% → 加 `ts_decay_linear(·,66)`（P5）后 TO 降到 15.35% 但 **S 崩到 0.34**。
**平滑抹掉 71% 的信号。**

对照：同一个 `ts_decay_linear(·,66)` 层在 shortinterest3 上是**增益**（S +0.06~+0.21，见 M20/M21）。
差别在于 shortinterest3 的 VECTOR 聚合产物是**低频状态量**，shortinterest43 是**高频流量**。

⇒ **不能照抄 shortinterest3 的平滑配方**。该数据集属「流量冲击」，不是「状态变量」。

### 4.3 近两年失效

P3 的 2Y = **−0.24**、P6 的 2Y = **−1.27**、P1/P2 的 2Y 仅 ±0.19。
只有 P4（跨所差）2Y 1.45 略好但 TO 130%。

⇒ SVO ratio 类信号在 2022–2023 基本失效。**不适合作为长期体制，只可作短周期信号。**

### 4.4 四所聚合提升的是「小票强度」而非整体质量

P3（四所量加权）vs P2（单所 bats）：S 1.18 vs 1.32（降）、TO 100.57% vs 102.97%（持平）、
**SUB 1.68 vs 1.65（升）、inv_ratio 1.2542 vs 1.0833（升）**。

⇒ 论坛「组合多交易所提升鲁棒性」在本轮**未复现**（但论坛是 `decay=250` 设置下的结论，不可直接对比）。
聚合让信号更偏小票/投资域外，与「提升整体质量」是两件事。

### 4.5 首波全部缺失横截面标准化层 —— 这是最大的结构缺陷

P1–P6 全部只用时序算子（`ts_rank`/`ts_zscore`/`ts_mean`/`ts_decay_linear`）+ `divide`/`subtract`，
**没有任何一条做横截面标准化**。

而 shortinterest3 上最强配方（M21，S 2.35 / F 2.59 / fRA 0）恰好是 `group_zscore(内层时序量, industry)`。
⇒ 波 152 的 P7/P8/P9 是必测项。

---

## 5. 禁区

| 禁区 | 证据 |
|---|---|
| **`tanh(ratio)`**（论坛推荐） | USA `operator_audit` 实测 `tanh` 是**幽灵算子**，提交即失败 |
| **`sigmoid` / `s_log_1p`** | 同为幽灵算子 |
| **`add(svol_venue1, svol_venue2)` 当混信号** | 分子分母必须是同族同单位聚合并整体相除（`divide(Σsvol, Σtv)`），不能对**比率**做 add（会把不同分母的比率混加，量纲与权重都失真） |
| **加 ε 防除零** | 同单位相除天然无量纲；分母为 0 交给平台产生 Inf/NaN，由下游 `group_zscore`/`winsorize` 吸收 |
| **用 `decay=250` 设置压换手** | 论坛做法，但本数据集信号半衰期 <15 日 ⇒ 该设置等于拿信号强度换换手，实测 P5 已证明方向不可行 |
| **把 FINRA short interest 的先验（高 = 看空）套上来** | 交易所 short sale volume 主体是做市商对冲，实测方向相反 |

---

## 6. 复现命令

```powershell
# 字段画像（零平台配额）
$env:PYTHONPATH='src;tools'
$env:PYTHONIOENCODING='utf-8'
python 'tools/fields/profile_dataset_fields.py' --region USA --dataset shortinterest43 --input 'tracking\USA\reports\field_profiles\shortinterest43_raw.json' --out 'docs/reference/USA/shortinterest43_field_profile.md' --top 25
```

MCP 预检（派发前必做）：
```
preflight_expressions({alpha_expressions, region:"USA", universe:"TOP3000", delay:1,
                       dataset_id:"shortinterest43", auto_fix_vector:false})
operator_audit({expressions, region:"USA", universe:"TOP3000", delay:1})
```

统一回测设置：`USA / TOP3000 / D1 / decay 0 / truncation 0.08 / neutralization SLOW / nanHandling ON / maxTrade OFF / unitHandling VERIFY`
